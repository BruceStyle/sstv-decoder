import tempfile
import unittest
from pathlib import Path

import numpy as np
from scipy import signal

from sstv_decoder.decoder import decode_file, inspect_file
from sstv_decoder.media import AudioError

from .helpers import EXPECTED_RGB, RATE, recording, transcode_audio, wave_bytes


class DecoderTest(unittest.TestCase):
    def decode(self, samples: np.ndarray):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "sample.wav"
            path.write_bytes(wave_bytes(samples))
            return decode_file(path)

    def test_finds_two_frames_and_selects_each_channel(self):
        base = recording()
        stretched = signal.resample_poly(base.astype(np.float32), 1001, 1000).astype(np.int16)
        length = len(base) + len(stretched)
        noise = np.random.default_rng(36).normal(0, 1400, (length, 2)).astype(np.int16)
        noise[:len(base), 1] = base
        noise[len(base):, 0] = stretched
        report = self.decode(noise)
        self.assertEqual(report.robot36_headers, 2)
        self.assertEqual([frame.channel for frame in report.frames], ["right", "left"])
        self.assertAlmostEqual(report.frames[0].start, 2.91, delta=0.003)
        self.assertAlmostEqual(report.frames[1].start, len(base) / RATE + 2.91 * 1.001, delta=0.004)
        for frame in report.frames:
            self.assertEqual(frame.status, "decoded")
            self.assertEqual(frame.image.size, (320, 240))
            colors = np.asarray(frame.image, dtype=np.int16)[35, [40, 120, 200, 280]]
            np.testing.assert_allclose(colors, EXPECTED_RGB, atol=5)

    def test_truncated_scan_is_partial(self):
        report = self.decode(recording(rows=65))
        self.assertEqual(len(report.frames), 1)
        frame = report.frames[0]
        self.assertEqual(frame.status, "partial")
        self.assertEqual(frame.rows, 65)
        self.assertTrue(np.all(np.asarray(frame.image)[65:] == 0))

    def test_reports_unsupported_and_insufficient_signals(self):
        noise = np.random.default_rng(8).normal(0, 3000, RATE * 40).astype(np.int16)
        for samples, expected in [
            (recording(vis=95, rows=0), "unsupported_mode"),
            (recording(rows=0), "insufficient_signal"),
            (np.concatenate((recording(rows=0), noise)), "insufficient_signal"),
            (recording(rows=0, parity_error=True), "no_signal"),
            (noise, "no_signal"),
        ]:
            with self.subTest(status=expected):
                report = self.decode(samples)
                self.assertEqual(report.status, expected)
                self.assertEqual(report.frames, [])

    def test_decodes_multiple_audio_formats(self):
        samples = recording()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wav_path = root / "sample.wav"
            wav_path.write_bytes(wave_bytes(samples))
            for ext, atol in [(".wav", 5), (".flac", 5), (".m4a", 8), (".mp3", 18), (".ogg", 18)]:
                with self.subTest(ext=ext):
                    target = wav_path if ext == ".wav" else transcode_audio(wav_path, root / f"sample{ext}")
                    report = decode_file(target)
                    self.assertEqual(report.status, "ok")
                    self.assertEqual(len(report.frames), 1)
                    frame = report.frames[0]
                    self.assertEqual(frame.status, "decoded")
                    self.assertEqual(frame.image.size, (320, 240))
                    colors = np.asarray(frame.image, dtype=np.int16)[35, [40, 120, 200, 280]]
                    np.testing.assert_allclose(colors, EXPECTED_RGB, atol=atol)

    def test_inspect_file_reports_metadata_and_vis_modes(self):
        combined = np.concatenate((recording(vis=8, rows=10), recording(vis=95, rows=0)))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "inspect.wav"
            path.write_bytes(wave_bytes(combined))
            details = inspect_file(path).details()
            self.assertEqual(details["robot36_headers"], 1)
            self.assertEqual(details["other_vis_codes"], [95])
            self.assertEqual(details["other_modes"], ["PD120"])
            self.assertEqual([h["mode"] for h in details["headers"]], ["Robot 36", "PD120"])
            self.assertEqual(details["audio"]["channels"], 1)

    def test_missing_file_raises_audio_error(self):
        with self.assertRaises(AudioError):
            decode_file(Path("/nonexistent/missing_sstv_file.wav"))

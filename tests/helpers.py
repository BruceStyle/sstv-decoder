"""Test helpers for generating synthetic Robot 36 audio in multiple container formats."""

import io
from pathlib import Path
import subprocess
import wave

import numpy as np

RATE = 24_000
EXPECTED_RGB = np.array([[128, 128, 128], [173, 76, 33], [94, 142, 250], [176, 240, 192]])


def recording(vis: int = 8, rows: int = 240, *, parity_error: bool = False) -> np.ndarray:
    """Generate Robot 36 color bars with an independently specified scan sequence."""
    bits = [(vis >> n) & 1 for n in range(7)]
    parity = (sum(bits) + parity_error) % 2
    segments = [(0, 2000), (1900, 300), (1200, 10), (1900, 300), (1200, 30)]
    segments += [(1100 if bit else 1300, 30) for bit in [*bits, parity]]
    segments.append((1200, 30))
    y = [128, 100, 140, 215]
    red_difference = [128, 180, 95, 100]
    blue_difference = [128, 90, 190, 115]
    for row in range(rows):
        red = row % 2 == 0
        segments.extend([(1200, 9), (1500, 3)])
        segments.extend((1500 + 800 * v / 255, 22) for v in y)
        segments.extend([(1500 if red else 2300, 4.5), (1900, 1.5)])
        segments.extend((1500 + 800 * v / 255, 11) for v in (red_difference if red else blue_difference))
    tone = np.concatenate([np.full(round(ms * RATE / 1000), hz) for hz, ms in segments])
    phase = np.cumsum(tone) * (2 * np.pi / RATE)
    return (np.sin(phase) * (tone > 0) * 18000).astype(np.int16)


def wave_bytes(samples: np.ndarray) -> bytes:
    """Serialize int16 samples into WAV bytes."""
    out = io.BytesIO()
    with wave.open(out, "wb") as wav:
        wav.setnchannels(1 if samples.ndim == 1 else samples.shape[1])
        wav.setsampwidth(2)
        wav.setframerate(RATE)
        wav.writeframes(samples.astype("<i2").tobytes())
    return out.getvalue()


def transcode_audio(wav_path: Path, target_path: Path) -> Path:
    """Transcode a WAV fixture into M4A, MP3, FLAC, or OGG via ffmpeg."""
    ext = target_path.suffix.lower()
    codec_args = {
        ".m4a": ["-c:a", "aac", "-b:a", "192k"],
        ".mp3": ["-c:a", "libmp3lame", "-b:a", "192k"],
        ".flac": ["-c:a", "flac"],
        ".ogg": ["-c:a", "libopus", "-b:a", "128k"],
    }[ext]
    subprocess.run(
        ["ffmpeg", "-v", "error", "-y", "-i", str(wav_path), *codec_args, str(target_path)],
        check=True,
    )
    return target_path

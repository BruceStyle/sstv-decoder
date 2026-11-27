import io
import json
import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from pathlib import Path

from PIL import Image

from sstv_decoder.cli import main as cli_main

from .helpers import recording, wave_bytes


class CLITest(unittest.TestCase):
    def test_cli_inspect_and_decode(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wav_path = root / "pass.wav"
            wav_path.write_bytes(wave_bytes(recording()))
            out_dir = root / "decoded"

            inspect_out = io.StringIO()
            with redirect_stdout(inspect_out):
                code = cli_main(["inspect", str(wav_path)])
            self.assertEqual(code, 0)
            inspect_data = json.loads(inspect_out.getvalue())
            self.assertEqual(inspect_data["robot36_headers"], 1)

            decode_out = io.StringIO()
            with redirect_stdout(decode_out):
                code = cli_main(["decode", str(wav_path), "-o", str(out_dir)])
            self.assertEqual(code, 0)
            decode_data = json.loads(decode_out.getvalue())
            self.assertEqual(decode_data["status"], "ok")
            self.assertTrue((out_dir / "report.json").is_file())
            png_path = out_dir / "frame-01.png"
            self.assertTrue(png_path.is_file())
            with Image.open(png_path) as img:
                self.assertEqual(img.size, (320, 240))

            err = io.StringIO()
            with redirect_stderr(err):
                code = cli_main(["decode", str(wav_path), "-o", str(out_dir)])
            self.assertEqual(code, 1)
            self.assertIn("already exists", err.getvalue())

            overwrite_out = io.StringIO()
            with redirect_stdout(overwrite_out):
                code = cli_main(["decode", str(wav_path), "-o", str(out_dir), "--overwrite"])
            self.assertEqual(code, 0)

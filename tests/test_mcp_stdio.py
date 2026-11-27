import base64
import io
import os
import sys
import tempfile
import unittest
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from PIL import Image

from .helpers import recording, wave_bytes


class StdioMCPTest(unittest.IsolatedAsyncioTestCase):
    async def test_stdio_mcp_tools_end_to_end(self):
        project_root = Path(__file__).resolve().parent.parent
        env = dict(os.environ)
        env["PYTHONPATH"] = str(project_root / "src")
        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "sstv_decoder.mcp_stdio"],
            env=env,
        )

        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            wav_path = root / "sample.wav"
            wav_path.write_bytes(wave_bytes(recording()))
            out_dir = root / "out"

            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()

                    tools_result = await session.list_tools()
                    names = {tool.name for tool in tools_result.tools}
                    self.assertEqual(names, {"decode_sstv_audio", "inspect_sstv_audio", "list_supported_modes"})

                    modes_res = await session.call_tool("list_supported_modes", {})
                    self.assertFalse(modes_res.isError)
                    self.assertEqual(modes_res.structuredContent["decodable_modes"][0]["vis_code"], 8)

                    inspect_res = await session.call_tool("inspect_sstv_audio", {"audio_path": str(wav_path)})
                    self.assertFalse(inspect_res.isError)
                    self.assertEqual(inspect_res.structuredContent["robot36_headers"], 1)

                    decode_res = await session.call_tool(
                        "decode_sstv_audio",
                        {"audio_path": str(wav_path), "output_dir": str(out_dir), "include_images": True},
                    )
                    self.assertFalse(decode_res.isError)
                    self.assertEqual(decode_res.structuredContent["status"], "ok")
                    self.assertTrue((out_dir / "frame-01.png").is_file())
                    self.assertTrue((out_dir / "report.json").is_file())

                    image_items = [item for item in decode_res.content if item.type == "image"]
                    self.assertEqual(len(image_items), 1)
                    img_bytes = base64.b64decode(image_items[0].data)
                    self.assertEqual(Image.open(io.BytesIO(img_bytes)).size, (320, 240))

                    missing_res = await session.call_tool(
                        "decode_sstv_audio",
                        {"audio_path": str(root / "missing.wav")},
                    )
                    self.assertTrue(missing_res.isError)

import io
import unittest

import httpx
from PIL import Image
from starlette.testclient import TestClient

from sstv_decoder.mcp_http import TOOL_NAME, create_app

from .helpers import recording, wave_bytes


class HttpMCPTest(unittest.TestCase):
    def test_mcp_attachment_and_public_url_and_ssrf_protection(self):
        origin = "https://sstv.example.org"
        attachment = "https://sdmntprwestus3.oaiusercontent.com/example.wav"
        public_audio = "https://cdn.example.org/pass.wav"
        seen = []
        data = wave_bytes(recording())

        def files(request: httpx.Request) -> httpx.Response:
            seen.append(str(request.url))
            if request.url.path == "/redirect":
                return httpx.Response(302, headers={"Location": "https://other.example.org/private"})
            if request.url.path == "/redirect-local":
                return httpx.Response(302, headers={"Location": "https://127.0.0.1/secret.wav"})
            return httpx.Response(200, content=data)

        app = create_app(
            public_origin=origin,
            download_transport=httpx.MockTransport(files),
            allow_public_urls=True,
        )
        with TestClient(app, base_url=origin, headers={"Accept": "application/json, text/event-stream"}) as client:
            health = client.get("/health")
            self.assertEqual(health.status_code, 200)
            self.assertEqual(health.json(), {"status": "ok"})

            def rpc(method: str, params: dict) -> dict:
                reply = client.post("/mcp", json={"jsonrpc": "2.0", "id": 1, "method": method, "params": params})
                self.assertEqual(reply.status_code, 200, reply.text)
                return reply.json()["result"]

            rpc("initialize", {
                "protocolVersion": "2025-11-25", "capabilities": {}, "clientInfo": {"name": "test", "version": "1"},
            })
            tool = rpc("tools/list", {})["tools"][0]
            self.assertEqual(tool["_meta"]["openai/fileParams"], ["audio"])
            uri = tool["_meta"]["ui"]["resourceUri"]
            resource = rpc("resources/read", {"uri": uri})["contents"][0]
            self.assertEqual(resource["mimeType"], "text/html;profile=mcp-app")
            self.assertIn("ui/notifications/tool-result", resource["text"])

            # 1. ChatGPT attachment flow
            response = rpc("tools/call", {"name": TOOL_NAME, "arguments": {
                "audio": {"file_id": "file-test", "download_url": attachment, "mime_type": "audio/wav"},
            }})
            self.assertFalse(response.get("isError", False), response)
            frame = response["structuredContent"]["frames"][0]
            image = client.get(frame["png_url"])
            self.assertEqual(image.status_code, 200)
            self.assertEqual(Image.open(io.BytesIO(image.content)).size, (320, 240))
            download = client.get(frame["png_url"] + "?download=1")
            self.assertIn("attachment", download.headers["Content-Disposition"])
            self.assertEqual(download.content, image.content)

            # 2. Generic HTTPS audio_url flow
            response2 = rpc("tools/call", {"name": TOOL_NAME, "arguments": {"audio_url": public_audio}})
            self.assertFalse(response2.get("isError", False), response2)
            self.assertEqual(len(response2["structuredContent"]["frames"]), 1)

            # 3. SSRF & host enforcement checks
            self.assertTrue(rpc("tools/call", {"name": TOOL_NAME, "arguments": {"audio_url": "https://127.0.0.1/a.wav"}})["isError"])
            self.assertTrue(rpc("tools/call", {"name": TOOL_NAME, "arguments": {"audio_url": "https://localhost/a.wav"}})["isError"])
            self.assertTrue(rpc("tools/call", {"name": TOOL_NAME, "arguments": {"audio_url": "http://cdn.example.org/a.wav"}})["isError"])
            self.assertTrue(rpc("tools/call", {"name": TOOL_NAME, "arguments": {"audio_url": "https://cdn.example.org/redirect-local"}})["isError"])
            self.assertTrue(rpc("tools/call", {"name": TOOL_NAME, "arguments": {
                "audio": {"file_id": "f2", "download_url": "https://sdmntprwestus3.oaiusercontent.com.example.org/example.wav"}
            }})["isError"])

            # 4. Attachment redirect to non-oai host should still be rejected even when allow_public_urls=True
            self.assertTrue(rpc("tools/call", {"name": TOOL_NAME, "arguments": {
                "audio": {"file_id": "f3", "download_url": "https://files.oaiusercontent.com/redirect"}
            }})["isError"])
            self.assertIn(attachment, seen)
            self.assertIn(public_audio, seen)

"""Streamable HTTP MCP server for remote AI agents and ChatGPT attachments."""

import asyncio
import base64
from contextlib import asynccontextmanager
from importlib import resources
import io
import ipaddress
import logging
import os
from pathlib import Path
import re
import secrets
import socket
import tempfile
from urllib.parse import urlsplit

import httpx
import mcp.types as types
from mcp.server import Server
from mcp.server.lowlevel.helper_types import ReadResourceContents
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from mcp.server.transport_security import TransportSecuritySettings
from pydantic import AnyUrl
from starlette.applications import Starlette
from starlette.concurrency import run_in_threadpool
from starlette.requests import Request
from starlette.responses import HTMLResponse, JSONResponse, PlainTextResponse, Response
from starlette.routing import Route

from .decoder import decode_file
from .media import MAX_BYTES, AudioError

logger = logging.getLogger("uvicorn.error")

OPENAI_AUDIO_HOST = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.oaiusercontent\.com")
TOOL_NAME = "decode_robot36_audio"
RESULT_URI = AnyUrl("ui://sstv-decoder/results.html")
RESULT_MIME = "text/html;profile=mcp-app"
RESULT_TTL = 30 * 60
MAX_RESULT_BATCHES = 8

FILE_SCHEMA = {
    "type": "object",
    "properties": {
        "download_url": {"type": "string"},
        "file_id": {"type": "string"},
        "mime_type": {"type": "string"},
        "file_name": {"type": "string"},
    },
    "required": ["download_url", "file_id"],
    "additionalProperties": False,
}

FRAME_PROPERTIES = {
    "number": {"type": "integer"},
    "mode": {"type": "string", "const": "Robot 36"},
    "start_seconds": {"type": "number"},
    "end_seconds": {"type": "number"},
    "status": {"type": "string", "enum": ["decoded", "partial"]},
    "method": {"type": "string", "enum": ["instantaneous_frequency", "spectral_reference"]},
    "received_rows": {"type": "integer"},
    "sync_coverage": {"type": "number"},
    "channel": {"type": "string", "enum": ["mono", "left", "right"]},
    "width": {"type": "integer", "const": 320},
    "height": {"type": "integer", "const": 240},
    "png_url": {"type": "string", "format": "uri"},
}

OUTPUT_SCHEMA = {
    "type": "object",
    "properties": {
        "status": {"type": "string", "enum": ["ok", "no_signal", "unsupported_mode", "insufficient_signal"]},
        "robot36_headers": {"type": "integer"},
        "other_vis_codes": {"type": "array", "items": {"type": "integer"}},
        "other_modes": {"type": "array", "items": {"type": "string"}},
        "frames": {
            "type": "array",
            "items": {"type": "object", "properties": FRAME_PROPERTIES, "required": list(FRAME_PROPERTIES)},
        },
    },
    "required": ["status", "robot36_headers", "other_vis_codes", "other_modes", "frames"],
}

MESSAGES = {
    "unsupported_mode": "Detected other SSTV mode(s). This release decodes Robot 36.",
    "insufficient_signal": "Detected a Robot 36 VIS header, but subsequent scan signal was too weak.",
    "no_signal": "No valid Robot 36 signal detected. Upload a clip with ~1 second before the header and subsequent scan.",
}


def _is_global_ip(address: str) -> bool:
    try:
        ip = ipaddress.ip_address(address)
    except ValueError:
        return False
    return (
        ip.is_global
        and not ip.is_private
        and not ip.is_loopback
        and not ip.is_link_local
        and not ip.is_multicast
        and not ip.is_reserved
        and not ip.is_unspecified
    )


def _check_public_host(host: str, resolve_dns: bool) -> bool:
    lowered = host.strip("[]").lower()
    if not lowered or lowered == "localhost" or lowered.endswith((".local", ".internal", ".localhost")):
        return False
    try:
        ipaddress.ip_address(lowered)
        return _is_global_ip(lowered)
    except ValueError:
        pass
    if not resolve_dns:
        return True
    try:
        infos = socket.getaddrinfo(lowered, 443, type=socket.SOCK_STREAM)
    except OSError:
        return False
    return bool(infos) and all(_is_global_ip(info[4][0]) for info in infos)


def _check_download_url(
    url: httpx.URL,
    *,
    allowed_hosts: set[str] | None,
    allow_oai: bool,
    allow_public_urls: bool,
    resolve_dns: bool,
) -> None:
    host = (url.host or "").lower()
    if (
        url.scheme != "https"
        or not host
        or url.port not in (None, 443)
        or url.userinfo
        or url.fragment
    ):
        raise AudioError("Audio download URL must be a clean HTTPS URL on port 443.")

    if allowed_hosts is not None:
        host_allowed = host in allowed_hosts
    elif allow_oai:
        host_allowed = bool(OPENAI_AUDIO_HOST.fullmatch(host))
    elif allow_public_urls:
        host_allowed = _check_public_host(host, resolve_dns=resolve_dns)
    else:
        host_allowed = False

    if not host_allowed:
        logger.warning(
            "SSTV download rejected host=%s https=%s allow_public=%s",
            host if re.fullmatch(r"[A-Za-z0-9.:-]{1,253}", host) else "(unavailable)",
            url.scheme == "https",
            allow_public_urls,
        )
        raise AudioError("Audio download URL host is not permitted by server policy.")


async def _download(
    url: str,
    path: Path,
    *,
    allowed_hosts: set[str] | None,
    allow_oai: bool,
    allow_public_urls: bool,
    transport: httpx.AsyncBaseTransport | None,
) -> None:
    resolve_dns = transport is None
    try:
        target = httpx.URL(url)
        async with asyncio.timeout(40), httpx.AsyncClient(
            transport=transport,
            follow_redirects=False,
            trust_env=False,
            timeout=httpx.Timeout(12, connect=5),
        ) as client:
            for _ in range(4):
                _check_download_url(
                    target,
                    allowed_hosts=allowed_hosts,
                    allow_oai=allow_oai,
                    allow_public_urls=allow_public_urls,
                    resolve_dns=resolve_dns,
                )
                async with client.stream("GET", target, headers={"Accept-Encoding": "identity"}) as response:
                    if response.is_redirect and "location" in response.headers:
                        target = target.join(response.headers["location"])
                        continue
                    response.raise_for_status()
                    if int(response.headers.get("content-length", 0)) > MAX_BYTES:
                        raise AudioError("Recording exceeds 128 MiB limit.")
                    if response.headers.get("content-encoding", "identity").lower() != "identity":
                        raise AudioError("Unexpected content encoding. Please upload the raw audio file.")
                    size = 0
                    with path.open("wb") as recording:
                        async for block in response.aiter_bytes(128 * 1024):
                            size += len(block)
                            if size > MAX_BYTES:
                                raise AudioError("Recording exceeds 128 MiB limit.")
                            recording.write(block)
                    return
    except AudioError:
        raise
    except (TimeoutError, httpx.InvalidURL, httpx.HTTPError) as exc:
        raise AudioError("Unable to download audio attachment. Please retry.") from exc
    raise AudioError("Too many redirects while downloading audio.")


def _decode_to_png(path: Path) -> tuple[dict, list[bytes]]:
    report = decode_file(path)
    pictures = []
    for frame in report.frames:
        with io.BytesIO() as buffer:
            frame.image.save(buffer, "PNG")
            pictures.append(buffer.getvalue())
    return report.details(), pictures


class _MCPRoute:
    def __init__(self, manager: StreamableHTTPSessionManager) -> None:
        self.manager = manager

    async def __call__(self, scope, receive, send) -> None:
        await self.manager.handle_request(scope, receive, send)


def create_app(
    *,
    public_origin: str | None = None,
    download_transport: httpx.AsyncBaseTransport | None = None,
    allow_public_urls: bool | None = None,
) -> Starlette:
    """Create the ASGI Starlette application hosting the Streamable HTTP MCP server."""
    production_domain = os.getenv("VERCEL_PROJECT_PRODUCTION_URL")
    default_origin = f"https://{production_domain}" if production_domain else "http://127.0.0.1:8000"
    origin = (public_origin or os.getenv("SSTV_PUBLIC_ORIGIN", default_origin)).rstrip("/")
    parsed = urlsplit(origin)
    if (
        parsed.scheme not in ("http", "https")
        or not parsed.hostname
        or parsed.username is not None
        or parsed.path
        or parsed.query
        or parsed.fragment
    ):
        raise ValueError("SSTV_PUBLIC_ORIGIN must be an origin such as https://sstv.example.org")

    audio_hosts = os.getenv("SSTV_AUDIO_HOSTS")
    allowed_hosts = None
    if audio_hosts is not None:
        allowed_hosts = {host.strip().lower() for host in audio_hosts.split(",") if host.strip()}

    if allow_public_urls is None:
        allow_public_urls = os.getenv("SSTV_ALLOW_PUBLIC_URLS", "").strip().lower() in ("1", "true", "yes")

    extra_origins = [
        item.strip() for item in os.getenv("SSTV_ALLOWED_ORIGINS", "").split(",") if item.strip()
    ]
    allowed_origins = [origin, "https://chatgpt.com", "https://claude.ai", *extra_origins]

    ui_meta: dict = {"prefersBorder": True, "csp": {"resourceDomains": [origin]}}
    if parsed.scheme == "https":
        ui_meta["domain"] = origin

    package_root = resources.files("sstv_decoder")
    html = package_root.joinpath("result.html").read_text(encoding="utf-8")
    logo_bytes = package_root.joinpath("assets", "logo.png").read_bytes()

    server = Server(
        "sstv-decoder",
        instructions=(
            "Decode a user's Robot 36 SSTV audio recording (attached file or HTTPS audio URL) into 320x240 PNG frames. "
            "If no recording or audio URL is provided, ask the user to attach one."
        ),
    )

    results: dict[str, list[bytes]] = {}
    result_cache = None
    if os.getenv("SSTV_RESULT_CACHE") == "vercel":
        from vercel.functions import AsyncRuntimeCache

        result_cache = AsyncRuntimeCache()
    decoder_slot = asyncio.Semaphore(1)

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name=TOOL_NAME,
                title="Decode Robot 36 SSTV Audio",
                description=(
                    "Decode a Robot 36 SSTV recording (WAV, M4A, MP3, FLAC, OGG, etc.) into downloadable "
                    "320x240 PNG frames with timestamps and signal quality metrics. Accepts either a ChatGPT "
                    "file attachment (`audio`) or an HTTPS `audio_url`."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio": FILE_SCHEMA,
                        "audio_url": {
                            "type": "string",
                            "description": "Direct HTTPS URL to an SSTV audio file.",
                        },
                    },
                    "additionalProperties": False,
                },
                outputSchema=OUTPUT_SCHEMA,
                annotations=types.ToolAnnotations(readOnlyHint=True, destructiveHint=False, openWorldHint=False),
                _meta={
                    "openai/fileParams": ["audio"],
                    "ui": {"resourceUri": str(RESULT_URI), "visibility": ["model"]},
                    "openai/toolInvocation/invoking": "Scanning for Robot 36 SSTV frames…",
                    "openai/toolInvocation/invoked": "SSTV audio processed",
                },
            )
        ]

    @server.list_resources()
    async def list_resources() -> list[types.Resource]:
        return [types.Resource(uri=RESULT_URI, name="Robot 36 Decoded Frames", mimeType=RESULT_MIME)]

    @server.read_resource()
    async def read_resource(uri: AnyUrl):
        if uri != RESULT_URI:
            raise ValueError("Unknown resource")
        return [ReadResourceContents(content=html, mime_type=RESULT_MIME, meta={"ui": ui_meta})]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> types.CallToolResult:
        if name != TOOL_NAME:
            raise ValueError("Unknown tool")

        audio_obj = arguments.get("audio")
        audio_url = arguments.get("audio_url")
        if isinstance(audio_obj, dict) and isinstance(audio_obj.get("download_url"), str):
            target_url = audio_obj["download_url"]
            allow_oai = True
        elif isinstance(audio_url, str) and audio_url.strip():
            target_url = audio_url.strip()
            allow_oai = False
        else:
            return types.CallToolResult(
                isError=True,
                content=[types.TextContent(type="text", text="Provide either `audio` attachment or `audio_url`.")],
            )

        try:
            if decoder_slot.locked():
                raise AudioError("Another recording is currently being decoded. Please try again shortly.")
            async with decoder_slot:
                with tempfile.TemporaryDirectory(prefix="sstv-http-") as folder:
                    path = Path(folder) / "recording"
                    await _download(
                        target_url,
                        path,
                        allowed_hosts=allowed_hosts,
                        allow_oai=allow_oai,
                        allow_public_urls=allow_public_urls,
                        transport=download_transport,
                    )
                    report, pictures = await run_in_threadpool(_decode_to_png, path)
        except (AudioError, OSError) as exc:
            message = str(exc) if isinstance(exc, AudioError) else "Unable to process recording."
            return types.CallToolResult(isError=True, content=[types.TextContent(type="text", text=message)])

        if pictures:
            token = secrets.token_urlsafe(24)
            if result_cache is None:
                if len(results) >= MAX_RESULT_BATCHES:
                    results.pop(next(iter(results)))
                results[token] = pictures
                asyncio.get_running_loop().call_later(RESULT_TTL, results.pop, token, None)
            else:
                for number, picture_bytes in enumerate(pictures, start=1):
                    await result_cache.set(
                        f"sstv:{token}:{number}",
                        base64.b64encode(picture_bytes).decode("ascii"),
                        {"ttl": RESULT_TTL, "name": "SSTV decoded PNG"},
                    )
            links = []
            for frame in report["frames"]:
                number = frame["number"]
                frame["png_url"] = f"{origin}/results/{token}/{number}.png"
                label = "partial" if frame["status"] == "partial" else "decoded"
                links.append(f"[Frame {number} · {label}]({frame['png_url']}?download=1)")
            message = f"Decoded {len(pictures)} Robot 36 frame(s).\n\n" + "\n".join(links)
        else:
            message = MESSAGES[report["status"]]
            if report["other_modes"]:
                message += f" Detected modes: {', '.join(report['other_modes'])}."

        return types.CallToolResult(
            structuredContent=report,
            content=[types.TextContent(type="text", text=message)],
        )

    manager = StreamableHTTPSessionManager(
        app=server,
        json_response=True,
        stateless=True,
        security_settings=TransportSecuritySettings(
            enable_dns_rebinding_protection=True,
            allowed_hosts=[
                parsed.netloc,
                "127.0.0.1:*",
                "localhost:*",
                *([os.environ["VERCEL_URL"]] if os.getenv("VERCEL_URL") else []),
            ],
            allowed_origins=allowed_origins,
        ),
    )

    @asynccontextmanager
    async def lifespan(_: Starlette):
        async with manager.run():
            yield
        results.clear()

    async def index(_: Request) -> HTMLResponse:
        return HTMLResponse(
            f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>SSTV Decoder MCP</title><style>
:root{{color-scheme:light dark;font:16px/1.6 system-ui,sans-serif}}
body{{margin:0}}main{{max-width:42rem;margin:8vh auto;padding:0 1.25rem}}
header{{display:flex;align-items:center;gap:.75rem;margin-bottom:1.5rem}}
header img{{width:2.5rem;height:2.5rem;border-radius:.5rem}}
code{{padding:.15em .4em;border-radius:4px;background:color-mix(in srgb,currentColor 12%,transparent)}}
</style></head><body><main>
<header><img src="/logo.png" alt="SSTV Decoder"><strong>SSTV Decoder MCP Server</strong></header>
<p>Streamable HTTP MCP endpoint: <code>{origin}/mcp</code></p>
<p>Decodes Robot 36 SSTV radio recordings into 320×240 PNG frames with automatic VIS detection and line-sync alignment.</p>
</main></body></html>"""
        )

    async def health(_: Request) -> JSONResponse:
        return JSONResponse({"status": "ok"})

    async def logo(_: Request) -> Response:
        return Response(logo_bytes, media_type="image/png")

    async def domain_challenge(_: Request) -> Response:
        challenge = os.getenv("SSTV_DOMAIN_CHALLENGE_TOKEN")
        if not challenge:
            return Response(status_code=404)
        return PlainTextResponse(challenge, headers={"Cache-Control": "no-store"})

    async def picture(request: Request) -> Response:
        token = request.path_params["token"]
        number = request.path_params["number"]
        if len(token) != 32 or number < 1:
            return Response(status_code=404)
        if result_cache is None:
            images = results.get(token, [])
            image = images[number - 1] if number <= len(images) else None
        else:
            cached = await result_cache.get(f"sstv:{token}:{number}")
            image = base64.b64decode(cached) if cached else None
        if image is None:
            return Response(status_code=404)
        headers = {"Cache-Control": "private, no-store", "Referrer-Policy": "no-referrer"}
        if request.query_params.get("download") == "1":
            headers["Content-Disposition"] = f'attachment; filename="robot36-{number:02d}.png"'
        return Response(image, media_type="image/png", headers=headers)

    return Starlette(
        routes=[
            Route("/", index),
            Route("/health", health),
            Route("/logo.png", logo),
            Route("/.well-known/openai-apps-challenge", domain_challenge),
            Route("/mcp", _MCPRoute(manager), methods=["GET", "POST", "DELETE"]),
            Route("/results/{token}/{number:int}.png", picture),
        ],
        lifespan=lifespan,
    )

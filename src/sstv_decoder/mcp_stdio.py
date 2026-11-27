"""Standard local stdio MCP server for cross-agent SSTV decoding."""

import argparse
import asyncio
import base64
import io
import json
import logging
from pathlib import Path
import sys
import tempfile

import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

from .decoder import VIS_MODES, decode_file, inspect_file
from .media import MAX_BYTES, MAX_DURATION, SUPPORTED_FORMATS, AudioError

logger = logging.getLogger("sstv_decoder.mcp_stdio")

DECODE_TOOL = "decode_sstv_audio"
INSPECT_TOOL = "inspect_sstv_audio"
MODES_TOOL = "list_supported_modes"

STATUS_MESSAGES = {
    "unsupported_mode": "Detected other SSTV mode(s), not Robot 36.",
    "insufficient_signal": "Detected Robot 36 VIS header(s), but the subsequent scan signal was too weak or short to recover an image.",
    "no_signal": "No valid Robot 36 VIS header found. Ensure the recording includes ~1 second before the transmission starts.",
}


def _resolve_output_dir(audio_path: Path, output_dir: str | None, overwrite: bool) -> Path:
    if output_dir:
        target = Path(output_dir).expanduser().resolve()
        if target.exists():
            if not overwrite:
                raise AudioError(f"Output directory already exists: {target}. Pass overwrite=true or pick a new directory.")
            if not target.is_dir():
                raise AudioError(f"Output path exists and is not a directory: {target}.")
        return target

    base = audio_path.parent / f"{audio_path.stem}_sstv"
    if not base.exists():
        return base
    suffix = 2
    while True:
        candidate = audio_path.parent / f"{audio_path.stem}_sstv-{suffix}"
        if not candidate.exists():
            return candidate
        suffix += 1


def _decode_and_save(audio_path: Path, output_dir: Path, overwrite: bool) -> tuple[dict, list[bytes]]:
    report = decode_file(audio_path)
    details = report.details()
    pictures: list[bytes] = []
    if not report.frames:
        details["output_dir"] = None
        details["report_path"] = None
        return details, pictures

    output_dir.parent.mkdir(parents=True, exist_ok=True)
    if overwrite and output_dir.exists():
        staging_parent = output_dir
    else:
        staging_parent = output_dir.parent

    with tempfile.TemporaryDirectory(prefix=".sstv-", dir=staging_parent) as temporary:
        staging = Path(temporary)
        for frame, entry in zip(report.frames, details["frames"], strict=True):
            name = f"frame-{entry['number']:02d}.png"
            buf = io.BytesIO()
            frame.image.save(buf, "PNG")
            png_bytes = buf.getvalue()
            pictures.append(png_bytes)
            (staging / name).write_bytes(png_bytes)
            entry["file"] = name
            entry["file_path"] = str(output_dir / name)

        details["output_dir"] = str(output_dir)
        details["report_path"] = str(output_dir / "report.json")
        report_text = json.dumps(details, ensure_ascii=False, indent=2) + "\n"
        (staging / "report.json").write_text(report_text, encoding="utf-8")

        if overwrite and output_dir.exists():
            for item in staging.iterdir():
                item.replace(output_dir / item.name)
        else:
            staging.rename(output_dir)

    return details, pictures


def create_stdio_server() -> Server:
    """Create the standard local MCP server for SSTV decoding."""
    server = Server(
        "sstv-decoder",
        instructions=(
            "Decode Robot 36 SSTV radio recordings (WAV, M4A, MP3, FLAC, OGG, etc.) into 320x240 PNG images. "
            "Use inspect_sstv_audio to check audio metadata and VIS headers, or decode_sstv_audio to demodulate "
            "and save decoded PNG frames."
        ),
    )

    @server.list_tools()
    async def list_tools() -> list[types.Tool]:
        return [
            types.Tool(
                name=DECODE_TOOL,
                title="Decode SSTV Audio",
                description=(
                    "Decode Robot 36 SSTV transmissions from a local audio file into 320x240 PNG images "
                    "and a report.json summary. Automatically locates VIS headers, aligns line sync, picks "
                    "the stronger stereo channel, and falls back to spectral recovery for weak signals."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_path": {
                            "type": "string",
                            "description": "Path to a local SSTV audio recording (WAV, M4A, MP3, FLAC, OGG, etc.).",
                        },
                        "output_dir": {
                            "type": "string",
                            "description": "Optional directory path to save decoded PNGs and report.json.",
                        },
                        "include_images": {
                            "type": "boolean",
                            "default": True,
                            "description": "Attach decoded PNG frames as inline image content in the tool response.",
                        },
                        "overwrite": {
                            "type": "boolean",
                            "default": False,
                            "description": "Allow writing into an existing output_dir.",
                        },
                    },
                    "required": ["audio_path"],
                    "additionalProperties": False,
                },
                annotations=types.ToolAnnotations(
                    readOnlyHint=False,
                    destructiveHint=False,
                    idempotentHint=False,
                    openWorldHint=False,
                ),
            ),
            types.Tool(
                name=INSPECT_TOOL,
                title="Inspect SSTV Audio",
                description=(
                    "Inspect a local audio recording for stream metadata (format, codec, channels, duration) "
                    "and detect SSTV VIS headers without full frame demodulation."
                ),
                inputSchema={
                    "type": "object",
                    "properties": {
                        "audio_path": {
                            "type": "string",
                            "description": "Path to a local audio recording.",
                        },
                    },
                    "required": ["audio_path"],
                    "additionalProperties": False,
                },
                annotations=types.ToolAnnotations(
                    readOnlyHint=True,
                    destructiveHint=False,
                    openWorldHint=False,
                ),
            ),
            types.Tool(
                name=MODES_TOOL,
                title="List Supported SSTV Modes",
                description="Return supported SSTV modes, accepted audio formats, limits, and known VIS codes.",
                inputSchema={
                    "type": "object",
                    "properties": {},
                    "additionalProperties": False,
                },
                annotations=types.ToolAnnotations(
                    readOnlyHint=True,
                    destructiveHint=False,
                    openWorldHint=False,
                ),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> types.CallToolResult:
        if name == MODES_TOOL:
            payload = {
                "decodable_modes": [
                    {
                        "name": "Robot 36",
                        "vis_code": 8,
                        "resolution": "320x240",
                        "duration_seconds": 36.0,
                        "color_encoding": "YUV alternating lines",
                    }
                ],
                "known_vis_codes": {str(code): label for code, label in VIS_MODES.items()},
                "supported_audio_formats": list(SUPPORTED_FORMATS),
                "limits": {
                    "max_duration_seconds": MAX_DURATION,
                    "max_file_bytes": MAX_BYTES,
                },
            }
            summary = (
                "Supported SSTV decode mode: Robot 36 (VIS 8, 320x240, ~36s). "
                f"Accepted formats via FFmpeg: {', '.join(SUPPORTED_FORMATS)}. "
                f"Limits: {MAX_DURATION // 60} min, {MAX_BYTES // (1024 * 1024)} MiB."
            )
            return types.CallToolResult(
                structuredContent=payload,
                content=[types.TextContent(type="text", text=summary)],
            )

        if name == INSPECT_TOOL:
            raw_path = arguments.get("audio_path")
            if not isinstance(raw_path, str) or not raw_path.strip():
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text="audio_path is required.")],
                )
            try:
                path = Path(raw_path).expanduser().resolve()
                report = await asyncio.to_thread(inspect_file, path)
                details = report.details()
            except (AudioError, OSError) as exc:
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=str(exc))],
                )
            headers = details["headers"]
            if headers:
                lines = [
                    f"- {h['start_seconds']:.3f}s: {h['mode']} (VIS {h['vis_code']}, strength={h['strength']:.3f})"
                    for h in headers
                ]
                header_text = "\n".join(lines)
            else:
                header_text = "No VIS headers detected."
            summary = (
                f"Audio: {details['audio']['format_name']} ({details['audio']['codec_name']}), "
                f"{details['audio']['channels']}ch, {details['audio']['duration_seconds']}s.\n"
                f"Detected VIS headers ({len(headers)}):\n{header_text}"
            )
            return types.CallToolResult(
                structuredContent=details,
                content=[types.TextContent(type="text", text=summary)],
            )

        if name == DECODE_TOOL:
            raw_path = arguments.get("audio_path")
            if not isinstance(raw_path, str) or not raw_path.strip():
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text="audio_path is required.")],
                )
            output_dir_arg = arguments.get("output_dir")
            include_images = bool(arguments.get("include_images", True))
            overwrite = bool(arguments.get("overwrite", False))
            try:
                audio_path = Path(raw_path).expanduser().resolve()
                output_dir = _resolve_output_dir(audio_path, output_dir_arg, overwrite)
                details, pictures = await asyncio.to_thread(_decode_and_save, audio_path, output_dir, overwrite)
            except (AudioError, OSError) as exc:
                return types.CallToolResult(
                    isError=True,
                    content=[types.TextContent(type="text", text=str(exc))],
                )

            contents: list[types.TextContent | types.ImageContent] = []
            if pictures:
                lines = [
                    f"Decoded {len(pictures)} Robot 36 frame(s) to {details['output_dir']}:",
                ]
                for frame in details["frames"]:
                    lines.append(
                        f"- Frame {frame['number']} ({frame['status']}, {frame['method']}): "
                        f"{frame['start_seconds']:.2f}s–{frame['end_seconds']:.2f}s, "
                        f"channel={frame['channel']}, rows={frame['received_rows']}/{frame['height']}, "
                        f"sync={frame['sync_coverage']:.1%}, file={frame['file_path']}"
                    )
                contents.append(types.TextContent(type="text", text="\n".join(lines)))
                if include_images:
                    for png_bytes in pictures:
                        contents.append(
                            types.ImageContent(
                                type="image",
                                data=base64.b64encode(png_bytes).decode("ascii"),
                                mimeType="image/png",
                            )
                        )
            else:
                msg = STATUS_MESSAGES[details["status"]]
                if details["other_modes"]:
                    msg += f" Detected modes: {', '.join(details['other_modes'])}."
                contents.append(types.TextContent(type="text", text=msg))

            return types.CallToolResult(structuredContent=details, content=contents)

        raise ValueError(f"Unknown tool: {name}")

    return server


async def run_stdio_server() -> None:
    """Run the MCP server over stdin/stdout."""
    server = create_stdio_server()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options(),
        )


def main() -> int:
    """Entry point for ``sstv-decoder-mcp``."""
    logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
    parser = argparse.ArgumentParser(description="Run the SSTV Decoder MCP server.")
    parser.add_argument(
        "--transport",
        choices=("stdio", "http"),
        default="stdio",
        help="MCP transport mode (default: stdio).",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Bind host for HTTP transport.")
    parser.add_argument("--port", type=int, default=8000, help="Bind port for HTTP transport.")
    args = parser.parse_args()

    if args.transport == "http":
        import uvicorn
        from .mcp_http import create_app

        uvicorn.run(create_app(), host=args.host, port=args.port, access_log=False)
        return 0

    asyncio.run(run_stdio_server())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

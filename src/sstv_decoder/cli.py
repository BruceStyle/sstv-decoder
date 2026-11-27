"""Unified CLI for local SSTV decoding, inspection, and MCP server startup."""

import argparse
import asyncio
import json
from pathlib import Path
import sys
import tempfile

from .decoder import decode_file, inspect_file
from .media import AudioError


def _cmd_decode(args: argparse.Namespace) -> int:
    audio_path = args.audio.expanduser().resolve()
    output_dir = (args.output or (audio_path.parent / f"{audio_path.stem}_sstv")).expanduser().resolve()
    try:
        if output_dir.exists() and not args.overwrite:
            raise AudioError(f"Output directory already exists: {output_dir}. Pass --overwrite or choose a new -o path.")
        report = decode_file(audio_path)
        details = report.details()
        output_dir.parent.mkdir(parents=True, exist_ok=True)
        staging_parent = output_dir if (args.overwrite and output_dir.exists()) else output_dir.parent
        with tempfile.TemporaryDirectory(prefix=".sstv-", dir=staging_parent) as temporary:
            staging = Path(temporary)
            for frame, entry in zip(report.frames, details["frames"], strict=True):
                name = f"frame-{entry['number']:02d}.png"
                frame.image.save(staging / name)
                entry["file"] = name
            report_text = json.dumps(details, ensure_ascii=False, indent=2) + "\n"
            (staging / "report.json").write_text(report_text, encoding="utf-8")
            if args.overwrite and output_dir.exists():
                for item in staging.iterdir():
                    item.replace(output_dir / item.name)
            else:
                staging.rename(output_dir)
    except (AudioError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(report_text, end="")
    return 0


def _cmd_inspect(args: argparse.Namespace) -> int:
    try:
        report = inspect_file(args.audio)
        print(json.dumps(report.details(), ensure_ascii=False, indent=2))
    except (AudioError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


def _cmd_mcp(args: argparse.Namespace) -> int:
    if args.transport == "http":
        import uvicorn
        from .mcp_http import create_app

        uvicorn.run(create_app(), host=args.host, port=args.port, access_log=False)
        return 0

    from .mcp_stdio import run_stdio_server

    asyncio.run(run_stdio_server())
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="sstv-decoder",
        description="Decode Robot 36 SSTV audio recordings or run an MCP server.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    decode_parser = subparsers.add_parser("decode", help="Decode Robot 36 frames to PNGs and report.json.")
    decode_parser.add_argument("audio", type=Path, help="Path to an SSTV audio recording.")
    decode_parser.add_argument("-o", "--output", type=Path, help="Output directory (default: <stem>_sstv).")
    decode_parser.add_argument("--overwrite", action="store_true", help="Allow writing into an existing directory.")
    decode_parser.set_defaults(func=_cmd_decode)

    inspect_parser = subparsers.add_parser("inspect", help="Inspect audio metadata and detect SSTV VIS headers.")
    inspect_parser.add_argument("audio", type=Path, help="Path to an SSTV audio recording.")
    inspect_parser.set_defaults(func=_cmd_inspect)

    mcp_parser = subparsers.add_parser("mcp", help="Start the SSTV Decoder MCP server.")
    mcp_parser.add_argument(
        "--transport",
        choices=("stdio", "http"),
        default="stdio",
        help="MCP transport mode (default: stdio).",
    )
    mcp_parser.add_argument("--host", default="127.0.0.1", help="Bind host for HTTP transport.")
    mcp_parser.add_argument("--port", type=int, default=8000, help="Bind port for HTTP transport.")
    mcp_parser.set_defaults(func=_cmd_mcp)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))

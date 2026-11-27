# SSTV Decoder

[English](README.md) | [简体中文](README.zh-CN.md) | [Live Showcase (`sstv-decoder.netlify.app`)](https://sstv-decoder.netlify.app) ([`docs/`](docs/index.html))

**A cross-agent open-source Robot 36 SSTV audio decoder** for amateur radio operators and ISS / ARISS satellite listeners.

Works seamlessly across **Cursor, Claude Desktop, Claude Code, OpenAI Codex, Antigravity, Windsurf, ChatGPT**, and plain command-line workflows via **MCP (Model Context Protocol)** and **Agent Skills (`SKILL.md`)**.

> **Showcase Website**: A static bilingual showcase & author page is included in [`docs/`](docs/index.html). Enable GitHub Pages (Source: `Deploy from a branch` → `/docs`) or deploy `docs/` directly to Vercel.

---

## Features

- **Automatic Frame Detection**: Scans full pass recordings for Robot 36 VIS headers (`VIS 8`), no manual timestamps required.
- **Sync Calibration & Stereo Selection**: Fits the `150 ms` scan clock per frame and automatically picks the cleaner channel (`mono`, `left`, or `right`).
- **Weak Signal Recovery**: Falls back to noise-covariance spectral estimation when line sync or carrier strength is weak, tagging outputs as `partial` instead of failing silently.
- **Broad Audio Format Support**: Accepts **WAV, M4A/MP4, MP3, FLAC, OGG/Opus, AAC, AIFF, WebM, WMA** (via FFmpeg), up to 15 minutes and 128 MiB.
- **Dual Open Standards**:
  - **Local `stdio` MCP Server** (`sstv-decoder-mcp`): Zero server setup, decodes local files directly, writes PNGs + `report.json`, and returns inline image previews to multimodal agents.
  - **Remote Streamable HTTP MCP Server** (`sstv-decoder mcp --transport http`): Supports HTTPS `audio_url`, ChatGPT file attachments (`openai/fileParams`), and MCP App result cards.
  - **Universal Agent Skill** (`skills/sstv-decoder/SKILL.md`): Works with any Agent Skills-compatible client (`agentskills.io`).

---

## Prerequisites

1. **Python 3.11+** (or [`uv`](https://docs.astral.sh/uv/) for zero-setup `uvx` execution)
2. **FFmpeg & ffprobe** on `PATH`:
   - macOS: `brew install ffmpeg`
   - Ubuntu/Debian: `sudo apt update && sudo apt install -y ffmpeg`
   - Windows: `winget install Gyan.FFmpeg`

---

## Scope & Quick Start (One Command for Every Agent)

> **Scope note**: `sstv-decoder` takes over **after you have recorded an SSTV radio audio file** (via handheld transceiver, Yagi antenna, or SDR). Pass prediction and satellite tracking are outside its scope; once you hand the recorded audio to your AI agent, header detection, sync calibration, and image decoding run automatically.

Install across **Claude Code, Cursor, OpenAI Codex, Antigravity, Windsurf, GitHub Copilot, Gemini CLI**, and 75+ compatible agents with a single command:

```sh
npx skills add BruceStyle/sstv-decoder
```

---

## Advanced Setup: Local / Remote MCP Server

For clients that prefer MCP (such as Claude Desktop or custom MCP setups), replace `"uvx", "sstv-decoder-mcp"` with `"uvx", "--from", "git+https://github.com/BruceStyle/sstv-decoder", "sstv-decoder-mcp"` before publishing to PyPI.

### 1. Cursor
Add to `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):
```json
{
  "mcpServers": {
    "sstv-decoder": {
      "command": "uvx",
      "args": ["sstv-decoder-mcp"]
    }
  }
}
```

### 2. Claude Desktop
Add to `claude_desktop_config.json`:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
```json
{
  "mcpServers": {
    "sstv-decoder": {
      "command": "uvx",
      "args": ["sstv-decoder-mcp"]
    }
  }
}
```

### 3. Claude Code
```sh
claude mcp add sstv-decoder -- uvx sstv-decoder-mcp
```

### 4. OpenAI Codex
Add to `~/.codex/config.toml`:
```toml
[mcp_servers.sstv-decoder]
command = "uvx"
args = ["sstv-decoder-mcp"]
```

### 5. Antigravity / Windsurf / VS Code
Add `sstv-decoder` to your MCP JSON configuration:
```json
{
  "mcpServers": {
    "sstv-decoder": {
      "command": "uvx",
      "args": ["sstv-decoder-mcp"]
    }
  }
}
```

### 6. ChatGPT & Remote Web Agents (Streamable HTTP MCP)
Run the HTTP server via Docker or Python, expose it over HTTPS, and connect `https://<your-domain>/mcp`:
```sh
uvx sstv-decoder mcp --transport http --host 0.0.0.0 --port 8000
```

---

## CLI Usage

```sh
# Inspect audio metadata & VIS headers without full decoding
uvx sstv-decoder inspect /path/to/iss_pass.m4a

# Decode Robot 36 frames into <stem>_sstv/ or a custom directory
uvx sstv-decoder decode /path/to/iss_pass.m4a -o ./output_frames

# Start local stdio MCP server
uvx sstv-decoder mcp

# Start remote Streamable HTTP MCP server
uvx sstv-decoder mcp --transport http --host 127.0.0.1 --port 8000
```

---

## MCP Tools

### Local `stdio` Server (`sstv-decoder-mcp`)
- `decode_sstv_audio(audio_path, output_dir?, include_images?, overwrite?)`: Decodes Robot 36 frames, saves `frame-01.png` ... and `report.json`, and returns inline PNG `ImageContent` + structured metadata.
- `inspect_sstv_audio(audio_path)`: Probes audio metadata and scans for all SSTV VIS headers.
- `list_supported_modes()`: Lists supported modes, accepted audio formats, limits, and known VIS codes.

### Remote HTTP Server (`/mcp`)
- `decode_robot36_audio(audio?, audio_url?)`: Accepts either ChatGPT file attachments (`openai/fileParams`) or an HTTPS `audio_url`, renders an interactive MCP App preview card (`ui://sstv-decoder/results.html`), and serves temporary PNG downloads.

---

## Self-Hosting (Docker & Environment Variables)

```sh
docker build -t sstv-decoder .
docker run -p 8000:8000 \
  -e SSTV_PUBLIC_ORIGIN=https://sstv.example.org \
  -e SSTV_ALLOW_PUBLIC_URLS=1 \
  sstv-decoder
```

| Variable | Description | Default |
| :--- | :--- | :--- |
| `SSTV_PUBLIC_ORIGIN` | Public HTTPS origin used for result PNG URLs and CSP | `http://127.0.0.1:8000` |
| `SSTV_AUDIO_HOSTS` | Comma-separated host allowlist for remote audio URLs | `*.oaiusercontent.com` (for attachments) |
| `SSTV_ALLOW_PUBLIC_URLS` | Set `1` to allow public HTTPS `audio_url` downloads (SSRF-checked) | `0` |
| `SSTV_ALLOWED_ORIGINS` | Additional allowed CORS/Origin values (comma-separated) | `origin, chatgpt.com, claude.ai` |
| `SSTV_RESULT_CACHE` | Set `vercel` on Vercel to use `AsyncRuntimeCache` | In-memory (30 min TTL) |
| `SSTV_DOMAIN_CHALLENGE_TOKEN` | Optional verification token at `/.well-known/openai-apps-challenge` | Unset |

---

## Development & Publishing to PyPI

PyPI accounts are completely free and do not require a credit card.

```sh
# Install dev environment
uv sync

# Run all unit tests
uv run python -m unittest discover -s tests -v

# Build wheel and source tarball
uv build

# Publish to PyPI (using an API token)
uv publish
```

## License

[MIT](LICENSE)

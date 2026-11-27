---
name: sstv-decoder
description: Decode Robot 36 SSTV (Slow-Scan Television) radio recordings (ISS/ARISS passes, amateur radio audio in WAV, M4A, MP3, FLAC, OGG, etc.) into 320x240 PNG images, inspect VIS headers, and diagnose weak or partial frames. Use whenever a user asks to decode SSTV audio, extract images from ISS/ham radio recordings, check SSTV VIS modes, or troubleshoot SSTV signal quality. (支持将国际空间站 ISS/ARISS 等无线电 SSTV 录音解码为 PNG 图片、检测 VIS 识别头并诊断弱信号)
license: MIT
compatibility: Requires Python 3.11+, uv/uvx (or pip), and FFmpeg/ffprobe on PATH.
metadata:
  author: BruceStyle
  version: "0.1.0"
---

# SSTV Decoder Skill

Decode Robot 36 SSTV transmissions from amateur radio or ISS/ARISS pass recordings into 320×240 PNG images with timestamps, channel selection, and signal quality diagnostics.

## Scope & Capabilities

- **Supported decode mode**: Robot 36 (`VIS 8`, `320×240`, ~36s per frame).
- **Audio formats**: Any common format readable by FFmpeg (`.wav`, `.m4a`, `.mp3`, `.flac`, `.ogg`, `.opus`, `.aac`, `.aiff`, `.webm`), mono/stereo/multi-channel, up to 15 minutes and 128 MiB.
- **Automatic signal recovery**: Locates VIS headers, calibrates line sync against clock drift/Doppler, picks the cleaner stereo channel per frame, and uses spectral reference recovery for weak/noisy signals (`status: "partial"`).
- **Other SSTV modes**: If PD120 (`VIS 95`), Martin, Scottie, etc. are detected, they are reported in `other_vis_codes` / `other_modes` with `status: "unsupported_mode"`.

## Execution Workflow

Follow this priority order depending on what tools are available in your agent runtime:

### 1. Prefer MCP Tools (if configured)
If the `sstv-decoder` MCP server is connected:
- Run `inspect_sstv_audio` first if the user wants to check whether a recording contains SSTV headers or identify which mode was transmitted.
- Run `decode_sstv_audio` with `audio_path` (and optional `output_dir`) to extract PNG frames and `report.json`.
- If running in a remote MCP environment (e.g., `decode_robot36_audio`), pass the uploaded attachment (`audio`) or HTTPS URL (`audio_url`).

### 2. Fallback to CLI via `uvx` or local install
If MCP tools are not available, execute via terminal (works directly from GitHub before PyPI release, or with `uvx sstv-decoder` once installed):
- Check VIS headers and audio metadata:
  ```sh
  uvx --from git+https://github.com/BruceStyle/sstv-decoder sstv-decoder inspect "/path/to/recording.m4a"
  ```
- Decode frames to a folder:
  ```sh
  uvx --from git+https://github.com/BruceStyle/sstv-decoder sstv-decoder decode "/path/to/recording.m4a" -o "/path/to/output_dir"
  ```
*(If `sstv-decoder` is already installed locally or on PyPI, you can run `uvx sstv-decoder ...` or `sstv-decoder ...` directly.)*

## Reporting Results to the User

Always present clear, factual results from `report.json` or tool output:
1. **Frames decoded**: State the count, file paths (and display the image if your client supports it), timestamps (`start_seconds`–`end_seconds`), and selected channel (`mono`, `left`, or `right`).
2. **Quality & status**:
   - `decoded` (`instantaneous_frequency`): Clean reception with strong line sync.
   - `partial` (`spectral_reference` or `< 240` rows): Weak signal or interrupted scan; mention `received_rows/240` and `sync_coverage`.
3. **Non-OK statuses**:
   - `unsupported_mode`: List detected `other_modes` / `other_vis_codes` and explain that v0.1 decodes Robot 36.
   - `insufficient_signal`: A Robot 36 VIS header was found, but line sync or scan duration was too weak/short.
   - `no_signal`: No valid VIS header found.

## Troubleshooting Reference

When the user asks why a pass failed to decode or produced noisy/partial images, consult [references/sstv-modes.md](references/sstv-modes.md).

"""Read bounded audio recordings of common formats via FFmpeg/ffprobe."""

from dataclasses import dataclass
import json
import math
from pathlib import Path
import subprocess

import numpy as np

SAMPLE_RATE = 24_000
MAX_DURATION = 15 * 60
MAX_BYTES = 128 * 1024 * 1024

SUPPORTED_FORMATS = (
    "WAV",
    "M4A / MP4 (AAC, ALAC)",
    "MP3",
    "FLAC",
    "OGG / Opus / Vorbis",
    "AIFF",
    "AAC",
    "WebM",
    "WMA",
)


class AudioError(ValueError):
    """A user-facing recording or decoder error."""


@dataclass(frozen=True)
class AudioInfo:
    """Metadata extracted from a probed audio file."""

    format_name: str
    codec_name: str
    channels: int
    sample_rate: int | None
    duration_seconds: float
    size_bytes: int

    def details(self) -> dict:
        return {
            "format_name": self.format_name,
            "codec_name": self.codec_name,
            "channels": self.channels,
            "sample_rate": self.sample_rate,
            "duration_seconds": round(self.duration_seconds, 3),
            "size_bytes": self.size_bytes,
        }


def _ffmpeg(args: list[str], timeout: int) -> bytes:
    try:
        result = subprocess.run(args, capture_output=True, check=False, timeout=timeout)
    except FileNotFoundError as exc:
        raise AudioError(
            "FFmpeg and ffprobe are required on PATH. "
            "Install via `brew install ffmpeg` (macOS), `sudo apt install ffmpeg` (Linux), "
            "or `winget install Gyan.FFmpeg` (Windows)."
        ) from exc
    except subprocess.TimeoutExpired as exc:
        raise AudioError("Timed out reading the audio recording. Try a shorter clip.") from exc
    if result.returncode:
        raise AudioError("Unable to decode audio file. Please provide a valid audio recording.")
    return result.stdout


def probe_audio(path: Path) -> AudioInfo:
    """Validate bounds and inspect stream metadata using ffprobe."""
    resolved = path.expanduser().resolve()
    if not resolved.is_file():
        raise AudioError(f"Audio file not found: {path}")
    size_bytes = resolved.stat().st_size
    if size_bytes == 0:
        raise AudioError("Audio file is empty.")
    if size_bytes > MAX_BYTES:
        raise AudioError("Recording exceeds 128 MiB limit. Trim the clip around the SSTV transmission.")

    input_options = ["-v", "error", "-protocol_whitelist", "file,pipe"]
    raw = _ffmpeg(
        [
            "ffprobe",
            *input_options,
            "-select_streams",
            "a:0",
            "-show_entries",
            "stream=codec_name,channels,sample_rate:format=format_name,duration",
            "-of",
            "json",
            str(resolved),
        ],
        timeout=20,
    )
    try:
        probe = json.loads(raw)
        stream = probe["streams"][0]
        fmt = probe["format"]
        channels = int(stream["channels"])
        duration = float(fmt["duration"])
        codec_name = str(stream["codec_name"])
        format_name = str(fmt.get("format_name", "unknown"))
        raw_sr = stream.get("sample_rate")
        sample_rate = int(raw_sr) if raw_sr is not None else None
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        raise AudioError("No readable audio stream or valid duration found in file.") from exc

    if channels < 1:
        raise AudioError("Audio stream must have at least 1 channel.")
    if not math.isfinite(duration) or not 0 < duration <= MAX_DURATION:
        raise AudioError("Recording duration must be between 0 and 15 minutes.")

    return AudioInfo(
        format_name=format_name,
        codec_name=codec_name,
        channels=channels,
        sample_rate=sample_rate,
        duration_seconds=duration,
        size_bytes=size_bytes,
    )


def read_audio(path: Path) -> np.ndarray:
    """Decode audio into 24 kHz signed 16-bit PCM preserving up to 2 channels."""
    resolved = path.expanduser().resolve()
    info = probe_audio(resolved)
    target_channels = info.channels if info.channels in (1, 2) else 2

    pcm = _ffmpeg(
        [
            "ffmpeg",
            "-v",
            "error",
            "-protocol_whitelist",
            "file,pipe",
            "-nostdin",
            "-i",
            str(resolved),
            "-map",
            "0:a:0",
            "-vn",
            "-sn",
            "-dn",
            "-threads",
            "1",
            "-ac",
            str(target_channels),
            "-ar",
            str(SAMPLE_RATE),
            "-t",
            str(MAX_DURATION + 0.1),
            "-f",
            "s16le",
            "pipe:1",
        ],
        timeout=30,
    )
    samples = np.frombuffer(pcm, dtype="<i2").reshape(-1, target_channels)
    if not len(samples) or len(samples) > (MAX_DURATION + 0.05) * SAMPLE_RATE:
        raise AudioError("Recording duration must be within 15 minutes.")
    return samples

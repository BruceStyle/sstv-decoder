"""Cross-agent Robot 36 SSTV audio decoder."""

from .decoder import (
    VIS_MODES,
    DecodeReport,
    Frame,
    Header,
    InspectReport,
    ScanClock,
    decode_file,
    inspect_file,
    vis_mode_name,
)
from .media import AudioError, AudioInfo, SUPPORTED_FORMATS, probe_audio, read_audio

__version__ = "0.1.0"

__all__ = [
    "AudioError",
    "AudioInfo",
    "DecodeReport",
    "Frame",
    "Header",
    "InspectReport",
    "SUPPORTED_FORMATS",
    "ScanClock",
    "VIS_MODES",
    "__version__",
    "decode_file",
    "inspect_file",
    "probe_audio",
    "read_audio",
    "vis_mode_name",
]

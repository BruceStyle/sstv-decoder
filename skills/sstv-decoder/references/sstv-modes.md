# SSTV Modes & Troubleshooting Reference

## 1. Robot 36 Specification

- **VIS Code**: `8` (`0x08`, 7-bit LSB-first `0001000`)
- **Resolution**: `320 × 240` pixels
- **Scan Duration**: ~36 seconds (240 lines × `0.150 s` per line)
- **Color Encoding**: YUV with alternating Chroma (`R-Y` on even lines, `B-Y` on odd lines)
- **Line Sync**: 9 ms pulse at `1200 Hz`
- **Luminance / Chrominance Range**: `1500 Hz` (black / min) to `2300 Hz` (white / max)

## 2. Common SSTV VIS Codes

| Mode | Decimal VIS | Hex | Resolution | Approx. Duration | Color Format |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Robot 36** | **8** | `0x08` | `320 × 240` | ~36 s | YUV (alternating) |
| Robot 72 | 12 | `0x0C` | `320 × 240` | ~72 s | YUV |
| Martin 2 | 40 | `0x28` | `320 × 256` | ~58 s | RGB sequential |
| Martin 1 | 44 | `0x2C` | `320 × 256` | ~114 s | RGB sequential |
| Scottie 2 | 56 | `0x38` | `320 × 256` | ~71 s | RGB sequential |
| Scottie 1 | 60 | `0x3C` | `320 × 256` | ~110 s | RGB sequential |
| Scottie DX | 76 | `0x4C` | `320 × 256` | ~269 s | RGB sequential |
| PD50 | 93 | `0x5D` | `320 × 256` | ~50 s | YUV |
| **PD120** | **95** | `0x5F` | `640 × 496` | ~126 s | YUV |
| PD180 | 96 | `0x60` | `640 × 496` | ~187 s | YUV |
| PD160 | 98 | `0x62` | `512 × 400` | ~161 s | YUV |
| PD90 | 99 | `0x63` | `320 × 256` | ~90 s | YUV |

*(Note: ISS/ARISS events frequently use PD120 or Robot 36. Currently `sstv-decoder` v0.1.0 demodulates **Robot 36** and identifies other modes by VIS code.)*

## 3. Weak Signal & Reception Troubleshooting

1. **`no_signal` despite audible SSTV tones**:
   - Check whether the recording started **after** the VIS header (`1900 Hz` leader + `1200 Hz` break + VIS bits). Recordings clipped mid-image miss the header.
   - Ensure the FM receiver was on **145.800 MHz** (ISS downlink) with wide FM (`NFM` / ~12.5–25 kHz) and squelch open or low.
2. **`insufficient_signal` or `partial` frames**:
   - Weak elevation passes, antenna polarization mismatch, or aggressive noise suppression / AGC pumping from phone voice-memo apps can smear `1200 Hz` sync pulses.
   - Record raw audio (WAV or high-bitrate M4A/FLAC) without voice-call noise cancellation whenever possible.
3. **Stereo recordings (`left` vs `right`)**:
   - The decoder automatically evaluates both channels per frame and selects the channel with stronger line sync. Check `channel` in `report.json` if one feed is cleaner (e.g., dual-receiver or SDR + handheld recordings).

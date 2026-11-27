"""Detect Robot 36 VIS headers, fit the scan clock, and demodulate frames."""

from dataclasses import dataclass
from pathlib import Path
from typing import Literal

import numpy as np
from numpy.lib.stride_tricks import sliding_window_view
from PIL import Image
from scipy import linalg, ndimage, signal

from .media import SAMPLE_RATE, AudioInfo, probe_audio, read_audio

MODE = "Robot 36"
VIS = 8
WIDTH = 320
HEIGHT = 240
LINE_SECONDS = 0.150
SYNC_SECONDS = 0.009
MIN_SYNC_ROWS = 12
HEADER_RATE = 6_000
HEADER_HOP = 24

VIS_MODES: dict[int, str] = {
    8: "Robot 36",
    12: "Robot 72",
    40: "Martin 2",
    44: "Martin 1",
    56: "Scottie 2",
    60: "Scottie 1",
    76: "Scottie DX",
    93: "PD50",
    95: "PD120",
    96: "PD180",
    98: "PD160",
    99: "PD90",
}


def vis_mode_name(code: int) -> str:
    """Return a human-readable SSTV mode name for a VIS code."""
    return VIS_MODES.get(code, f"VIS {code}")


@dataclass(frozen=True)
class Header:
    start: float
    code: int
    strength: float


@dataclass(frozen=True)
class ScanClock:
    start: float
    period: float
    rows: int
    coverage: float
    strength: float


@dataclass(frozen=True)
class Frame:
    image: Image.Image
    start: float
    end: float
    rows: int
    channel: str
    status: Literal["decoded", "partial"]
    method: Literal["instantaneous_frequency", "spectral_reference"]
    sync_coverage: float

    def details(self, number: int) -> dict:
        return {
            "number": number,
            "mode": MODE,
            "start_seconds": round(self.start, 3),
            "end_seconds": round(self.end, 3),
            "status": self.status,
            "method": self.method,
            "received_rows": self.rows,
            "sync_coverage": round(self.sync_coverage, 3),
            "channel": self.channel,
            "width": WIDTH,
            "height": HEIGHT,
        }


@dataclass(frozen=True)
class DecodeReport:
    frames: list[Frame]
    robot36_headers: int
    other_vis_codes: list[int]

    @property
    def status(self) -> str:
        if self.frames:
            return "ok"
        if self.robot36_headers:
            return "insufficient_signal"
        if self.other_vis_codes:
            return "unsupported_mode"
        return "no_signal"

    def details(self) -> dict:
        return {
            "status": self.status,
            "robot36_headers": self.robot36_headers,
            "other_vis_codes": self.other_vis_codes,
            "other_modes": [vis_mode_name(code) for code in self.other_vis_codes],
            "frames": [frame.details(i) for i, frame in enumerate(self.frames, 1)],
        }


@dataclass(frozen=True)
class InspectReport:
    audio: AudioInfo
    headers: list[Header]
    robot36_headers: int
    other_vis_codes: list[int]

    def details(self) -> dict:
        return {
            "audio": self.audio.details(),
            "robot36_headers": self.robot36_headers,
            "other_vis_codes": self.other_vis_codes,
            "other_modes": [vis_mode_name(code) for code in self.other_vis_codes],
            "headers": [
                {
                    "start_seconds": round(header.start, 3),
                    "vis_code": header.code,
                    "mode": vis_mode_name(header.code),
                    "strength": round(header.strength, 4),
                }
                for header in self.headers
            ],
        }


def _header_tones(samples: np.ndarray) -> np.ndarray:
    """Return local energy fractions for the VIS tones at 4 ms intervals."""
    audio = signal.resample_poly(samples.astype(np.float32), 1, SAMPLE_RATE // HEADER_RATE)
    window_size = round(0.024 * HEADER_RATE)
    weights = np.hanning(window_size).astype(np.float32)
    phase = (2 * np.pi / HEADER_RATE) * np.arange(window_size)[:, None] * [1100, 1200, 1300, 1900]
    basis = np.concatenate([np.cos(phase), np.sin(phase)], axis=1).astype(np.float32)
    basis *= weights[:, None]
    padded = np.pad(audio, (window_size // 2, window_size // 2 - 1))
    windows = sliding_window_view(padded, window_size)[::HEADER_HOP]
    tones = np.empty((len(windows), 4), np.float32)
    for offset in range(0, len(windows), 4096):
        block = np.ascontiguousarray(windows[offset:offset + 4096])
        projection = block @ basis
        energy = (block ** 2) @ weights
        power = projection[:, :4] ** 2 + projection[:, 4:] ** 2
        tones[offset:offset + len(block)] = 2 * power / (weights.sum() * energy[:, None] + 1e-12)
    return tones


def _headers(samples: np.ndarray) -> list[Header]:
    if len(samples) < SAMPLE_RATE:
        return []
    tones = _header_tones(samples)
    step = HEADER_HOP / HEADER_RATE
    centers = np.rint((0.015 + 0.030 * np.arange(10)) / step).astype(int)
    pilot_offsets = np.rint(np.array([0.045, 0.105, 0.165, 0.225]) / step).astype(int)
    starts = np.arange(pilot_offsets[-1], len(tones) - centers[-1])
    if not len(starts):
        return []
    slots = starts[:, None] + centers
    pilot = tones[starts[:, None] - pilot_offsets, 3].mean(axis=1)
    boundary = tones[slots[:, [0, -1]], 1]
    data = tones[slots[:, 1:-1]]
    bits = data[:, :, 0] > data[:, :, 2]
    winning = np.maximum(data[:, :, 0], data[:, :, 2])
    losing = np.maximum(np.minimum(data[:, :, 0], data[:, :, 2]), data[:, :, 1])
    valid = (
        (pilot > 0.075)
        & (boundary.min(axis=1) > 0.16)
        & (winning.min(axis=1) > 0.14)
        & ((winning > 1.18 * losing).sum(axis=1) >= 8)
        & (bits[:, :7].sum(axis=1) % 2 == bits[:, 7])
    )
    strength = pilot * 0.3 + boundary.mean(axis=1) * 0.2 + winning.mean(axis=1) * 0.5
    peaks, _ = signal.find_peaks(np.pad(np.where(valid, strength, 0), 1), distance=round(0.25 / step))
    return [
        Header(float(starts[i] * step + 0.30), int(bits[i, :7] @ (1 << np.arange(7))), float(strength[i]))
        for i in peaks - 1
    ]


def _scan_headers(samples: np.ndarray) -> list[Header]:
    """Find deduplicated VIS headers across all channels sorted by start time."""
    candidates: list[Header] = []
    for channel in samples.T:
        candidates.extend(_headers(channel))
    unique: list[Header] = []
    for header in sorted(candidates, key=lambda item: item.strength, reverse=True):
        if all(abs(header.start - previous.start) > 0.25 for previous in unique):
            unique.append(header)
    return sorted(unique, key=lambda item: item.start)


def _sync_contrast(audio: np.ndarray) -> np.ndarray:
    """Compare matched 1200 Hz sync power with power away from the sync position."""
    size = round(SYNC_SECONDS * SAMPLE_RATE)
    phase = np.arange(len(audio)) * (2 * np.pi * 1200 / SAMPLE_RATE)

    def moving_sum(values: np.ndarray) -> np.ndarray:
        sums = np.r_[0.0, np.cumsum(values, dtype=np.float64)]
        return sums[size:] - sums[:-size]

    matched = moving_sum(audio * np.cos(phase)) ** 2 + moving_sum(audio * np.sin(phase)) ** 2
    power = 2 * matched / (size * moving_sum(audio ** 2) + 1e-9)
    offset = round(0.040 * SAMPLE_RATE)
    return power[:-2 * offset] - 0.5 * (power[offset:-offset] + power[2 * offset:])


def _fit_clock(audio: np.ndarray, guess: float) -> ScanClock | None:
    margin = 0.035
    origin = max(0, round((guess - margin) * SAMPLE_RATE))
    stop = round((guess + HEIGHT * LINE_SECONDS + 0.18) * SAMPLE_RATE)
    clip = audio[origin:stop].astype(np.float32) / 32768
    if len(clip) < (MIN_SYNC_ROWS + 1) * LINE_SECONDS * SAMPLE_RATE:
        return None
    contrast = _sync_contrast(clip)
    starts = np.arange(-margin, margin + 0.001, 0.001) * SAMPLE_RATE + guess * SAMPLE_RATE - origin
    periods = (LINE_SECONDS + np.arange(-8, 9) * 0.00005) * SAMPLE_RATE
    rows = np.arange(1, HEIGHT)
    grid = np.rint(starts[:, None, None] + periods[None, :, None] * rows).astype(int)
    valid = (grid >= 0) & (grid < len(contrast))
    contrast_at = np.where(valid, contrast[np.clip(grid, 0, len(contrast) - 1)], 0)
    scores = contrast_at.sum(axis=2) / np.maximum(valid.sum(axis=2), 1)
    start_i, period_i = np.unravel_index(scores.argmax(), scores.shape)
    period = periods[period_i]
    start = starts[start_i]
    rough = np.rint(start + period * rows).astype(int)

    # Refine the clock with the observed pulse positions from multiple scan lines.
    radius = round(0.003 * SAMPLE_RATE)
    usable = (rough >= radius) & (rough + radius < len(contrast))
    sample_rows = rows[usable]
    windows = rough[usable, None] + np.arange(-radius, radius + 1)
    strengths = contrast[windows]
    best = strengths.argmax(axis=1)
    found = windows[np.arange(len(best)), best]
    strong = strengths.max(axis=1) > 0.20
    if strong.sum() >= MIN_SYNC_ROWS:
        anchors = np.column_stack((np.ones(strong.sum()), sample_rows[strong]))
        weights = np.sqrt(strengths.max(axis=1)[strong])
        refined_start, refined_period = np.linalg.lstsq(
            anchors * weights[:, None], found[strong] * weights, rcond=None
        )[0]
        if abs(refined_period - period) <= 0.00009 * SAMPLE_RATE:
            start, period = refined_start, refined_period

    aligned = np.rint(start + period * rows).astype(int)
    aligned = aligned[(aligned >= 0) & (aligned < len(contrast))]
    evidence = contrast[aligned]
    mean_strength = evidence.mean() if len(evidence) else 0.0
    if (
        (evidence > 0.20).sum() < MIN_SYNC_ROWS
        or mean_strength < 0.083
        or mean_strength - np.median(scores) < 0.055
    ):
        return None
    start_sample = origin + start
    received = min(HEIGHT, int(np.floor((len(audio) - start_sample + 0.001 * SAMPLE_RATE) / period)))
    return ScanClock(
        float(start_sample / SAMPLE_RATE), float(period / SAMPLE_RATE), received,
        float(np.mean(evidence > 0.20)), float(mean_strength),
    )


def _scan_times(clock: ScanClock, origin: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    rows = (clock.start + np.arange(clock.rows) * clock.period) * SAMPLE_RATE - origin
    scale = SAMPLE_RATE * clock.period / LINE_SECONDS
    y = rows[:, None] + scale * (0.012 + (np.arange(WIDTH) + 0.5) * (0.088 / WIDTH))
    chroma = rows[:, None] + scale * (0.106 + (np.arange(WIDTH // 2) + 0.5) * (0.044 / (WIDTH // 2)))
    return rows, y, chroma


def _intensity(frequency: np.ndarray) -> np.ndarray:
    return np.clip((frequency - 1500) * (255 / 800), 0, 255)


def _spectral_reference(
    audio: np.ndarray, rows: np.ndarray, y: np.ndarray, chroma: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Estimate video tones using a noise covariance fitted on line-sync residuals."""
    fit_rate = SAMPLE_RATE // 2
    mono = signal.resample_poly(audio, 1, 2)
    taps = round(fit_rate * 0.004)
    sync_count = round(fit_rate * 0.007)
    sync_grid = np.rint(rows / 2 + 0.001 * fit_rate).astype(int)[:, None] + np.arange(sync_count)
    sync = mono[sync_grid]
    phase = 2 * np.pi * 1200 / fit_rate * np.arange(sync_count)
    basis = np.column_stack((np.ones(sync_count), np.sin(phase), np.cos(phase)))
    residual = sync - (sync @ np.linalg.pinv(basis).T) @ basis.T
    ac = np.array([np.mean(residual[:, :sync_count - i] * residual[:, i:]) for i in range(taps)])
    covariance = linalg.toeplitz(ac) + np.eye(taps) * max(float(ac[0]) * 0.005, 1e-10)
    inverse = linalg.pinvh(covariance, check_finite=False)
    taper = np.sqrt(np.maximum(np.hanning(taps), 0.04))
    inverse *= taper[:, None] * taper[None, :]
    frequencies = np.arange(1450, 2361, 10, dtype=np.float32)
    phase = (2 * np.pi / fit_rate) * frequencies[:, None] * np.arange(taps)
    cosine, sine = np.cos(phase), np.sin(phase)
    cos_fit, sin_fit = cosine @ inverse, sine @ inverse
    g00 = (cos_fit * cosine).sum(axis=1)
    g11 = (sin_fit * sine).sum(axis=1)
    g01 = (cos_fit * sine).sum(axis=1)
    determinant = np.maximum(g00 * g11 - g01 ** 2, 1e-15)
    padded = np.pad(mono, (taps // 2, taps // 2))
    cos_fit = cos_fit.astype(np.float32)
    sin_fit = sin_fit.astype(np.float32)

    def estimate(times: np.ndarray, sigma: float) -> np.ndarray:
        if not len(times):
            return np.empty_like(times)
        centers = np.clip(np.rint(times.ravel() / 2).astype(int), 0, len(mono) - 1)
        power = np.empty((len(centers), len(frequencies)), dtype=np.float32)
        for offset in range(0, len(centers), 4096):
            block = centers[offset:offset + 4096]
            windows = padded[block[:, None] + np.arange(taps)]
            p, q = windows @ cos_fit.T, windows @ sin_fit.T
            power[offset:offset + len(block)] = (g11 * p ** 2 - 2 * g01 * p * q + g00 * q ** 2) / determinant
        power = ndimage.gaussian_filter1d(power.reshape(*times.shape, -1), sigma, axis=0, mode="nearest")
        peak = np.clip(power.argmax(axis=-1), 1, len(frequencies) - 2)
        left, mid, right = [
            np.log(np.maximum(np.take_along_axis(power, (peak + d)[..., None], axis=-1)[..., 0], 1e-20))
            for d in (-1, 0, 1)
        ]
        curve = left - 2 * mid + right
        correction = np.divide(0.5 * (left - right), curve, out=np.zeros_like(mid), where=curve < -1e-6)
        return _intensity(frequencies[peak] + np.clip(correction, -1, 1) * 10)

    # Smooth red and blue difference samples independently.
    c = np.empty_like(chroma)
    c[::2] = estimate(chroma[::2], 1.0)
    c[1::2] = estimate(chroma[1::2], 1.0)
    return estimate(y, 2.0), c


def _render(y: np.ndarray, chroma: np.ndarray) -> Image.Image:
    rows = len(y)
    colors = np.full((HEIGHT, WIDTH // 2), 128, dtype=np.float32)
    colors[:rows] = chroma
    cr = np.repeat(np.repeat(colors[::2], 2, axis=0), 2, axis=1)[:rows] - 128
    cb = np.repeat(np.repeat(colors[1::2], 2, axis=0), 2, axis=1)[:rows] - 128
    rgb = np.stack((y + 1.402 * cr, y - 0.714136 * cr - 0.344136 * cb, y + 1.772 * cb), axis=-1)
    pixels = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    pixels[:rows] = np.rint(np.clip(rgb, 0, 255)).astype(np.uint8)
    return Image.fromarray(pixels)


def _demodulate(samples: np.ndarray, clock: ScanClock, channel: str) -> Frame:
    origin = max(0, round((clock.start - 0.040) * SAMPLE_RATE))
    stop = round((clock.start + clock.rows * clock.period + 0.040) * SAMPLE_RATE)
    clip = samples[origin:stop].astype(np.float32) / 32768
    rows, y, c = _scan_times(clock, origin)
    passband = signal.butter(5, [950, 2600], fs=SAMPLE_RATE, btype="bandpass", output="sos")
    filtered = signal.sosfiltfilt(passband, clip)
    analytic = signal.hilbert(filtered)
    frequency = np.angle(analytic[1:] * analytic[:-1].conj()) * SAMPLE_RATE / (2 * np.pi)
    frequency = ndimage.uniform_filter1d(frequency, 5)
    time = np.arange(len(frequency)) + 0.5
    fy = np.interp(y, time, frequency)
    video_fraction = np.mean((fy >= 1410) & (fy <= 2390))
    weak = clock.coverage < 0.75 or clock.strength < 0.43 or video_fraction < 0.78
    if weak:
        y_pixels, c_pixels = _spectral_reference(clip, rows, y, c)
    else:
        y_pixels, c_pixels = _intensity(fy), _intensity(np.interp(c, time, frequency))
    return Frame(
        _render(y_pixels, c_pixels), clock.start, min(len(samples) / SAMPLE_RATE, clock.start + clock.rows * clock.period),
        clock.rows, channel, "partial" if weak or clock.rows < HEIGHT else "decoded",
        "spectral_reference" if weak else "instantaneous_frequency", clock.coverage,
    )


def inspect_file(path: Path) -> InspectReport:
    """Inspect an audio file for metadata and SSTV VIS headers without demodulating frames."""
    resolved = path.expanduser().resolve()
    info = probe_audio(resolved)
    samples = read_audio(resolved)
    unique = _scan_headers(samples)
    return InspectReport(
        audio=info,
        headers=unique,
        robot36_headers=sum(header.code == VIS for header in unique),
        other_vis_codes=sorted({header.code for header in unique if header.code != VIS}),
    )


def decode_file(path: Path) -> DecodeReport:
    """Detect Robot 36 VIS headers and demodulate all frames in an audio recording."""
    samples = read_audio(path)
    unique = _scan_headers(samples)

    frames = []
    channels = ("mono",) if samples.shape[1] == 1 else ("left", "right")
    for header in unique:
        if header.code != VIS or (frames and header.start < frames[-1].end - 0.15):
            continue
        clocks = [
            (clock, index) for index, channel in enumerate(samples.T)
            if (clock := _fit_clock(channel, header.start)) is not None
        ]
        if clocks:
            clock, index = max(clocks, key=lambda item: item[0].strength)
            frames.append(_demodulate(samples[:, index], clock, channels[index]))
    return DecodeReport(
        frames, sum(header.code == VIS for header in unique),
        sorted({header.code for header in unique if header.code != VIS}),
    )

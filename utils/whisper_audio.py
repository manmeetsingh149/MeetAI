"""Load WAV for Whisper without calling ffmpeg from PATH."""

import wave

import numpy as np

WHISPER_SAMPLE_RATE = 16000
MIN_PEAK = 1e-4  # skip near-silent audio


def _resample(audio: np.ndarray, src_rate: int, dst_rate: int) -> np.ndarray:
    if src_rate == dst_rate or len(audio) == 0:
        return audio.astype(np.float32)
    new_len = max(1, int(round(len(audio) * dst_rate / src_rate)))
    x_old = np.linspace(0, 1, num=len(audio), endpoint=False)
    x_new = np.linspace(0, 1, num=new_len, endpoint=False)
    return np.interp(x_new, x_old, audio).astype(np.float32)


def load_wav_for_whisper(path: str) -> np.ndarray:
    """Read WAV as float32 mono @ 16 kHz for Whisper."""
    with wave.open(path, "rb") as wf:
        channels = wf.getnchannels()
        sample_width = wf.getsampwidth()
        frame_rate = wf.getframerate()
        n_frames = wf.getnframes()

        if n_frames == 0:
            return np.array([], dtype=np.float32)

        if sample_width != 2:
            raise ValueError(
                f"Expected 16-bit WAV, got sample width {sample_width} in {path}"
            )

        raw = wf.readframes(n_frames)

    audio = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if channels > 1:
        audio = audio.reshape(-1, channels).mean(axis=1)

    if frame_rate != WHISPER_SAMPLE_RATE:
        audio = _resample(audio, frame_rate, WHISPER_SAMPLE_RATE)

    return audio


def is_usable_audio(audio: np.ndarray, min_samples: int) -> bool:
    if audio is None or len(audio) < min_samples:
        return False
    return float(np.max(np.abs(audio))) >= MIN_PEAK


def iter_whisper_segments(
    audio: np.ndarray,
    window_samples: int = 30 * WHISPER_SAMPLE_RATE,
    min_samples: int = 1600,
):
    """Yield non-empty ~30s segments for Whisper (avoids 0-frame encoder crashes)."""
    if not is_usable_audio(audio, min_samples):
        return

    step = max(window_samples, min_samples)
    for start in range(0, len(audio), step):
        segment = audio[start : start + window_samples]
        if is_usable_audio(segment, min_samples):
            yield segment

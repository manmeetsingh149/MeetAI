"""Validate downloaded/converted audio before Whisper transcription."""

import os
import re
import subprocess

from pydub import AudioSegment

from utils.ffmpeg_tools import configure_ffmpeg, get_ffmpeg_exe

MIN_FILE_BYTES = 1024
MIN_DURATION_MS = 500
_DURATION_RE = re.compile(r"Duration:\s*(\d+):(\d+):(\d+)\.(\d+)")


def probe_has_audio_stream(path: str) -> bool:
    """Return True if the file contains at least one audio stream."""
    path = os.path.normpath(os.path.abspath(path))
    configure_ffmpeg()
    ffmpeg = get_ffmpeg_exe()
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", path],
        capture_output=True,
        text=True,
    )
    return "Audio:" in (result.stderr or "")


def _duration_ms_from_ffmpeg(path: str) -> int:
    configure_ffmpeg()
    ffmpeg = get_ffmpeg_exe()
    result = subprocess.run(
        [ffmpeg, "-hide_banner", "-i", path],
        capture_output=True,
        text=True,
    )
    stderr = result.stderr or ""
    match = _DURATION_RE.search(stderr)
    if not match:
        return 0
    h, m, s, cs = (int(match.group(i)) for i in range(1, 5))
    return ((h * 3600 + m * 60 + s) * 1000) + (cs * 10)


def wav_duration_ms(path: str) -> int:
    return len(AudioSegment.from_wav(path))


def validate_audio_file(
    path: str,
    *,
    min_bytes: int = MIN_FILE_BYTES,
    min_duration_ms: int = MIN_DURATION_MS,
    label: str = "Audio",
) -> int:
    """Ensure file exists, has audio, and is long enough for Whisper."""
    path = os.path.normpath(os.path.abspath(path))
    if not os.path.isfile(path):
        raise FileNotFoundError(f"{label} file not found: {path}")

    size = os.path.getsize(path)
    if size < min_bytes:
        raise ValueError(
            f"{label} file is too small ({size} bytes). "
            "The download may have failed or contained no audio track."
        )

    configure_ffmpeg()
    if not probe_has_audio_stream(path):
        raise ValueError(
            f"{label} has no audio stream ({os.path.basename(path)}). "
            "Try another video or run: uv pip install -U yt-dlp"
        )

    if path.lower().endswith(".wav"):
        duration_ms = wav_duration_ms(path)
    else:
        duration_ms = _duration_ms_from_ffmpeg(path)

    if duration_ms < min_duration_ms:
        raise ValueError(
            f"{label} is too short ({duration_ms} ms). "
            "Whisper needs at least half a second of audio."
        )

    return duration_ms

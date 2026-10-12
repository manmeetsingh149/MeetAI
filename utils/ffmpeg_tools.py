"""Bundled FFmpeg for audio conversion (no system install)."""

import os
import shutil
import subprocess

import imageio_ffmpeg

_BIN_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".ffmpeg_bin")
_FFMPEG_EXE = os.path.normpath(os.path.join(_BIN_DIR, "ffmpeg.exe"))


def get_ffmpeg_exe() -> str:
    """Return absolute path to bundled ffmpeg.exe."""
    os.makedirs(_BIN_DIR, exist_ok=True)
    source = os.path.normpath(imageio_ffmpeg.get_ffmpeg_exe())
    if not os.path.isfile(source):
        raise RuntimeError("Bundled FFmpeg binary is missing from imageio-ffmpeg.")

    if not os.path.isfile(_FFMPEG_EXE):
        shutil.copy2(source, _FFMPEG_EXE)

    if not os.path.isfile(_FFMPEG_EXE):
        raise RuntimeError(f"Failed to install bundled FFmpeg at {_FFMPEG_EXE}")

    return _FFMPEG_EXE


def configure_ffmpeg() -> str:
    """
    Wire bundled FFmpeg into PATH, pydub, and subprocess calls.

    Call once at app startup and before any audio processing.
    """
    ffmpeg = get_ffmpeg_exe()
    bin_dir = os.path.dirname(ffmpeg)

    path = os.environ.get("PATH", "")
    if bin_dir not in path.split(os.pathsep):
        os.environ["PATH"] = bin_dir + os.pathsep + path

    try:
        from pydub import AudioSegment

        AudioSegment.converter = ffmpeg
        AudioSegment.ffmpeg = ffmpeg
        # pydub uses ffprobe for some formats; ffmpeg -i works for probing metadata
        AudioSegment.ffprobe = ffmpeg
    except ImportError:
        pass

    return ffmpeg


def prepend_ffmpeg_to_path() -> str:
    """Backward-compatible alias."""
    return configure_ffmpeg()


def convert_to_wav(input_path: str, output_path: str | None = None) -> str:
    """Convert any audio/video file to mono 16 kHz WAV using bundled ffmpeg."""
    input_path = os.path.normpath(os.path.abspath(input_path))
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"Audio file not found: {input_path}")

    if output_path is None:
        output_path = os.path.splitext(input_path)[0] + ".wav"
    output_path = os.path.normpath(os.path.abspath(output_path))
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    configure_ffmpeg()
    ffmpeg = get_ffmpeg_exe()

    cmd = [
        ffmpeg,
        "-y",
        "-i",
        input_path,
        "-map",
        "0:a:0?",
        "-vn",
        "-acodec",
        "pcm_s16le",
        "-ar",
        "16000",
        "-ac",
        "1",
        output_path,
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError as e:
        raise RuntimeError(
            f"Could not run FFmpeg at {ffmpeg}. Reinstall dependencies: uv sync"
        ) from e

    if result.returncode != 0:
        err = (result.stderr or result.stdout or "unknown error").strip()
        raise RuntimeError(f"FFmpeg conversion failed: {err}")

    if not os.path.isfile(output_path):
        raise FileNotFoundError(f"FFmpeg did not create output: {output_path}")

    return output_path

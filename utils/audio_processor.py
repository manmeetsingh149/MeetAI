import os

import yt_dlp
from pydub import AudioSegment

from utils.audio_validate import validate_audio_file
from utils.ffmpeg_tools import configure_ffmpeg, convert_to_wav

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

AUDIO_EXTENSIONS = {".wav", ".webm", ".m4a", ".mp4", ".mp3", ".opus", ".ogg", ".aac", ".flac", ".mkv"}

# Skip Whisper on chunks shorter than this
MIN_CHUNK_MS = 1000


def _resolve_downloaded_file(prepared_path: str, info: dict) -> str:
    """Find the file yt-dlp actually wrote to disk."""
    if os.path.isfile(prepared_path):
        return prepared_path

    base = os.path.splitext(prepared_path)[0]
    for ext in AUDIO_EXTENSIONS:
        candidate = base + ext
        if os.path.isfile(candidate):
            return candidate

    ext = info.get("ext")
    if ext:
        candidate = f"{base}.{ext}"
        if os.path.isfile(candidate):
            return candidate

    raise FileNotFoundError(
        f"Downloaded audio not found (expected near {prepared_path})."
    )


def _download_with_ytdlp(source: str, outtmpl: str) -> tuple[str, dict]:
    """
    Download best audio with yt-dlp.

    Uses Android/web clients to avoid YouTube JS-runtime issues that can
    yield video-only or broken downloads.
    """
    ydl_opts = {
        # Prefer m4a/audio-only formats; never pick a silent file
        "format": "bestaudio[ext=m4a]/bestaudio[acodec!=none]/bestaudio/best",
        "outtmpl": outtmpl,
        "quiet": False,
        "no_warnings": False,
        "noplaylist": True,
        "extractor_args": {
            "youtube": {
                "player_client": ["android", "web"],
            }
        },
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(source, download=True)
        prepared = ydl.prepare_filename(info)

    downloaded = _resolve_downloaded_file(prepared, info)
    validate_audio_file(downloaded, label="Downloaded audio")
    return downloaded, info


def extract_audio_to_wav(source: str) -> tuple[str, list[str]]:
    """
    YouTube URL or local file -> mono 16 kHz WAV.

    Returns (wav_path, intermediate_files_to_cleanup).
    """
    source = source.strip()
    configure_ffmpeg()

    cleanup: list[str] = []
    is_url = source.startswith("http://") or source.startswith("https://")

    if is_url:
        outtmpl = os.path.join(DOWNLOAD_DIR, "%(id)s.%(ext)s")
        print("Downloading audio with yt-dlp...")
        downloaded, _info = _download_with_ytdlp(source, outtmpl)
        cleanup.append(downloaded)
    else:
        if not os.path.isfile(source):
            raise FileNotFoundError(f"Local file not found: {source}")
        downloaded = source
        validate_audio_file(downloaded, label="Input file")

    wav_path = os.path.join(
        DOWNLOAD_DIR,
        os.path.splitext(os.path.basename(downloaded))[0] + "_audio.wav",
    )

    print("Converting to WAV with bundled FFmpeg...")
    convert_to_wav(downloaded, wav_path)
    duration_ms = validate_audio_file(wav_path, label="Converted WAV")
    print(f"Audio length: {duration_ms / 1000:.1f}s")

    if is_url and downloaded != source and os.path.isfile(downloaded):
        try:
            os.remove(downloaded)
            if downloaded in cleanup:
                cleanup.remove(downloaded)
        except OSError:
            pass

    return wav_path, cleanup


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list:
    """Split WAV into chunks; skip segments too short or silent for Whisper."""
    audio = AudioSegment.from_wav(wav_path)
    if len(audio) < MIN_CHUNK_MS:
        raise ValueError(
            f"Audio is only {len(audio)} ms long — not enough for transcription."
        )

    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []

    for i, start in enumerate(range(0, len(audio), chunk_ms)):
        segment = audio[start : start + chunk_ms]
        if len(segment) < MIN_CHUNK_MS:
            continue
        # Skip near-silent segments (prevents Whisper 0-frame tensor crash)
        if segment.dBFS == float("-inf") or segment.max_possible_amplitude == 0:
            continue
        if segment.dBFS < -55:
            print(f"Skipping near-silent segment {i} ({segment.dBFS:.1f} dBFS)")
            continue

        chunk_path = f"{wav_path}_chunk_{i}.wav"
        segment.export(chunk_path, format="wav")

        if not os.path.isfile(chunk_path) or os.path.getsize(chunk_path) < 1024:
            print(f"Skipping invalid chunk file: {chunk_path}")
            continue

        chunks.append(chunk_path)

    if not chunks:
        raise ValueError(
            "No valid audio chunks were produced. The file may be silent or corrupt."
        )

    return chunks


def cleanup_audio_files(paths: list[str]) -> None:
    """Remove temporary audio files."""
    seen = set()
    for path in paths:
        if not path or path in seen:
            continue
        seen.add(path)
        if os.path.isfile(path):
            try:
                os.remove(path)
            except OSError:
                pass


def process_input(source: str) -> tuple[list[str], list[str]]:
    """Process YouTube URL or local file into WAV chunks."""
    source = source.strip()
    cleanup_paths: list[str] = []

    if source.startswith("http://") or source.startswith("https://"):
        print("Detected YouTube URL.")
    else:
        print("Detected local file.")

    wav_path, intermediates = extract_audio_to_wav(source)
    cleanup_paths.extend(intermediates)
    cleanup_paths.append(wav_path)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path)
    cleanup_paths.extend(chunks)
    print(f"Audio ready — {len(chunks)} chunk(s) created.")
    return chunks, cleanup_paths

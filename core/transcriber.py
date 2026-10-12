import os

import numpy as np
import requests
import whisper
from pydub import AudioSegment

from utils.ffmpeg_tools import configure_ffmpeg
from utils.whisper_audio import (
    is_usable_audio,
    iter_whisper_segments,
    load_wav_for_whisper,
)

SARVAM_PIECE_SECONDS = 25
MIN_WHISPER_SAMPLES = 4800  # 0.3s at 16 kHz

WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_STT_TRANSLATE_URL = "https://api.sarvam.ai/speech-to-text-translate"
SARVAM_MODEL = os.getenv("SARVAM_STT_MODEL", "saaras:v2.5")

_model = None


def load_model():
    global _model
    if _model is None:
        print(f"Loading Whisper model: {WHISPER_MODEL} ...")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded.")
    return _model


def _is_empty_tensor_error(exc: BaseException) -> bool:
    msg = str(exc).lower()
    return "reshape" in msg or "0 elements" in msg or "empty" in msg


def _load_whisper_audio(chunk_path: str) -> np.ndarray | None:
    try:
        audio = load_wav_for_whisper(chunk_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"  Could not read chunk {os.path.basename(chunk_path)}: {e}")
        return None
    if not is_usable_audio(audio, MIN_WHISPER_SAMPLES):
        return None
    return audio


def transcribe_chunk_whisper(chunk_path: str) -> str:
    audio = _load_whisper_audio(chunk_path)
    if audio is None:
        print(f"  Skipping empty/silent chunk: {os.path.basename(chunk_path)}")
        return ""

    model = load_model()
    texts: list[str] = []
    segments = list(iter_whisper_segments(audio, min_samples=MIN_WHISPER_SAMPLES))
    if not segments:
        print(f"  Skipping chunk with no speech: {os.path.basename(chunk_path)}")
        return ""

    for i, segment in enumerate(segments, start=1):
        try:
            result = model.transcribe(
                segment,
                task="transcribe",
                fp16=False,
                verbose=False,
            )
            text = result.get("text", "").strip()
            if text:
                texts.append(text)
        except Exception as e:
            if _is_empty_tensor_error(e):
                print(f"  Skipping Whisper segment {i} (no audio frames): {chunk_path}")
                continue
            raise

    return " ".join(texts)


def _send_to_sarvam(piece_path: str) -> str:
    headers = {"api-subscription-key": SARVAM_API_KEY}
    with open(piece_path, "rb") as f:
        files = {"file": (os.path.basename(piece_path), f, "audio/wav")}
        data = {"model": SARVAM_MODEL, "with_diarization": "false"}
        response = requests.post(
            SARVAM_STT_TRANSLATE_URL,
            headers=headers,
            files=files,
            data=data,
            timeout=120,
        )

    if not response.ok:
        print(f"\nSarvam returned {response.status_code}")
        print(f"Response body: {response.text}\n")
        response.raise_for_status()

    return response.json().get("transcript", "")


def transcribe_chunk_sarvam(chunk_path: str) -> str:
    if not SARVAM_API_KEY:
        raise RuntimeError("SARVAM_API_KEY is not set in environment / .env")

    audio = AudioSegment.from_wav(chunk_path)
    if len(audio) < 500:
        return ""

    piece_ms = SARVAM_PIECE_SECONDS * 1000
    full_text = ""
    total_pieces = max(1, (len(audio) + piece_ms - 1) // piece_ms)

    for i, start in enumerate(range(0, len(audio), piece_ms)):
        piece = audio[start : start + piece_ms]
        if len(piece) < 500:
            continue
        piece_path = f"{chunk_path}_sv_{i}.wav"
        piece.export(piece_path, format="wav")
        try:
            print(f"  -> Sarvam piece {i + 1}/{total_pieces} ...")
            full_text += _send_to_sarvam(piece_path) + " "
        finally:
            if os.path.exists(piece_path):
                os.remove(piece_path)

    return full_text.strip()


def transcribe_chunk(chunk_path: str, language: str = "english") -> str:
    if language.lower() == "hinglish":
        return transcribe_chunk_sarvam(chunk_path)
    return transcribe_chunk_whisper(chunk_path)


def transcribe_all(chunks: list, language: str = "english") -> str:
    if not chunks:
        raise ValueError("No audio chunks to transcribe.")

    configure_ffmpeg()
    full_transcript = ""
    engine = "Sarvam AI" if language.lower() == "hinglish" else "Whisper"
    print(f"Using {engine} for transcription.")

    for i, chunk in enumerate(chunks):
        if not os.path.isfile(chunk) or os.path.getsize(chunk) < 1024:
            print(f"Skipping missing/empty file: {chunk}")
            continue
        print(f"Transcribing chunk {i + 1}/{len(chunks)}...")
        text = transcribe_chunk(chunk, language=language)
        if text:
            full_transcript += text + " "

    result = full_transcript.strip()
    if not result:
        raise ValueError(
            "Transcription produced no text. The audio may be silent, too short, "
            "or the download had no usable audio track. Try another video."
        )

    print("Transcription complete.")
    return result

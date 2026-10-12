"""
Document loader — extracts plain text from uploaded files (PDF, DOCX, TXT).
"""

from __future__ import annotations

import io
from pathlib import PurePosixPath


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from PDF bytes using pypdf."""
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(file_bytes))
    pages: list[str] = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text.strip())
    return "\n\n".join(pages)


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from DOCX bytes using python-docx."""
    from docx import Document

    doc = Document(io.BytesIO(file_bytes))
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    return "\n\n".join(paragraphs)


def extract_text_from_txt(file_bytes: bytes) -> str:
    """Decode raw bytes as UTF-8 plain text."""
    return file_bytes.decode("utf-8", errors="replace").strip()


# Map of supported extensions → extractor functions
_EXTRACTORS: dict[str, callable] = {
    ".pdf": extract_text_from_pdf,
    ".docx": extract_text_from_docx,
    ".txt": extract_text_from_txt,
    ".text": extract_text_from_txt,
    ".md": extract_text_from_txt,
}

SUPPORTED_EXTENSIONS: list[str] = list(_EXTRACTORS.keys())


def extract_text(file_name: str, file_bytes: bytes) -> str:
    """
    Detect file type by extension and extract plain text.

    Parameters
    ----------
    file_name : str
        Original filename (used to determine type).
    file_bytes : bytes
        Raw file content.

    Returns
    -------
    str
        Extracted text.

    Raises
    ------
    ValueError
        If the file type is not supported or no text could be extracted.
    """
    suffix = PurePosixPath(file_name).suffix.lower()
    extractor = _EXTRACTORS.get(suffix)

    if extractor is None:
        supported = ", ".join(SUPPORTED_EXTENSIONS)
        raise ValueError(
            f"Unsupported file type '{suffix}'. Supported: {supported}"
        )

    text = extractor(file_bytes)
    if not text:
        raise ValueError(
            f"No text could be extracted from '{file_name}'. "
            "The file may be empty, image-only, or corrupted."
        )

    return text

"""Export meeting results to TXT and PDF."""

import os
import sys

from fpdf import FPDF

FONT_FAMILY = "ReportFont"


def build_report_text(result: dict) -> str:
    sections = [
        ("Title", result.get("title", "")),
        ("Summary", result.get("summary", "")),
        ("Transcript", result.get("transcript", "")),
        ("Action Items", result.get("action_items", "")),
        ("Key Decisions", result.get("key_decisions", "")),
        ("Open Questions", result.get("open_questions", "")),
    ]
    parts = []
    for heading, body in sections:
        parts.append(f"{'=' * 60}\n{heading.upper()}\n{'=' * 60}\n{body}\n")
    return "\n".join(parts)


def export_txt(result: dict) -> bytes:
    return build_report_text(result).encode("utf-8")


def _normalize_pdf_text(text: str) -> str:
    """Replace common Unicode punctuation that breaks built-in PDF fonts."""
    if not text:
        return ""
    text = str(text)
    replacements = {
        "\u2019": "'",
        "\u2018": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u2013": "-",
        "\u2014": "-",
        "\u2026": "...",
        "\u00a0": " ",
        "\u2022": "*",
        "\u2192": "->",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def _find_unicode_fonts() -> tuple[str | None, str | None]:
    """Return (regular_ttf, bold_ttf) paths from system fonts."""
    win = os.environ.get("WINDIR", r"C:\Windows")
    candidates = []

    if sys.platform == "win32":
        fonts_dir = os.path.join(win, "Fonts")
        candidates.extend([
            (os.path.join(fonts_dir, "arial.ttf"), os.path.join(fonts_dir, "arialbd.ttf")),
            (os.path.join(fonts_dir, "segoeui.ttf"), os.path.join(fonts_dir, "segoeuib.ttf")),
            (os.path.join(fonts_dir, "calibri.ttf"), os.path.join(fonts_dir, "calibrib.ttf")),
        ])
    elif sys.platform == "darwin":
        mac_fonts = "/System/Library/Fonts/Supplemental"
        candidates.append(
            (os.path.join(mac_fonts, "Arial.ttf"), os.path.join(mac_fonts, "Arial Bold.ttf"))
        )
    else:
        candidates.extend([
            (
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
                "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
            ),
            (
                "/usr/share/fonts/TTF/DejaVuSans.ttf",
                "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
            ),
        ])

    for regular, bold in candidates:
        if regular and os.path.isfile(regular):
            bold_path = bold if bold and os.path.isfile(bold) else None
            return regular, bold_path

    return None, None


def _setup_pdf_fonts(pdf: FPDF) -> tuple[bool, bool]:
    """Register Unicode TTF fonts. Returns (has_font, has_bold)."""
    regular, bold = _find_unicode_fonts()
    if not regular:
        return False, False

    pdf.add_font(FONT_FAMILY, "", regular)
    if bold:
        pdf.add_font(FONT_FAMILY, "B", bold)
    return True, bool(bold)


def export_pdf(result: dict) -> bytes:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    width = pdf.epw

    has_unicode_font, has_bold = _setup_pdf_fonts(pdf)
    body_size = 10
    heading_size = 12

    sections = [
        ("Title", result.get("title", "")),
        ("Summary", result.get("summary", "")),
        ("Action Items", result.get("action_items", "")),
        ("Key Decisions", result.get("key_decisions", "")),
        ("Open Questions", result.get("open_questions", "")),
    ]

    for heading, body in sections:
        text = str(body or "")
        heading_text = str(heading)

        if not has_unicode_font:
            text = _normalize_pdf_text(text)
            heading_text = _normalize_pdf_text(heading_text)

        if has_unicode_font:
            pdf.set_font(FONT_FAMILY, "B" if has_bold else "", heading_size)
        else:
            pdf.set_font("Helvetica", "B", heading_size)

        pdf.multi_cell(width, 8, heading_text)

        if has_unicode_font:
            pdf.set_font(FONT_FAMILY, "", body_size)
        else:
            pdf.set_font("Helvetica", size=body_size)

        pdf.multi_cell(width, 6, text)
        pdf.ln(4)

    out = pdf.output(dest="S")
    if isinstance(out, (bytes, bytearray)):
        return bytes(out)
    return out.encode("latin-1")

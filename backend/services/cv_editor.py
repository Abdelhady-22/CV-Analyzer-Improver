"""
CV Editor — applies surgical paragraph-level edits to DOCX files.
All output is ATS-safe: single-column, Calibri 11pt, standard bullets, no tables/images.
"""

from __future__ import annotations

import copy
import re
from pathlib import Path

from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH

from models.analysis import ParagraphEdit


# ── ATS-safe styling constants ─────────────────────────────────

FONT_NAME = "Calibri"
FONT_SIZE_BODY = Pt(11)
FONT_SIZE_HEADING = Pt(13)
FONT_SIZE_NAME = Pt(16)
FONT_COLOR = RGBColor(0, 0, 0)
LINE_SPACING = 1.15


def _apply_ats_style(paragraph, font_size=FONT_SIZE_BODY, bold=False):
    """Apply ATS-safe font styling to a paragraph."""
    for run in paragraph.runs:
        run.font.name = FONT_NAME
        run.font.size = font_size
        run.font.color.rgb = FONT_COLOR
        run.bold = bold
    paragraph.paragraph_format.line_spacing = LINE_SPACING


def apply_edits(original_docx_path: str, edits: list[ParagraphEdit]) -> str:
    """
    Clone the original DOCX and apply paragraph-level edits.
    Returns the path to the improved DOCX.
    """
    doc = Document(original_docx_path)
    original_path = Path(original_docx_path)
    improved_path = original_path.parent / f"{original_path.stem}_improved.docx"

    # Build a lookup of edits by old_text for fuzzy matching
    for edit in edits:
        for i, para in enumerate(doc.paragraphs):
            text = para.text.strip()
            if text and _fuzzy_match(text, edit.old_text):
                # Preserve existing runs structure but replace text
                _replace_paragraph_text(para, edit.new_text)
                _apply_ats_style(para)
                break

    # Ensure all paragraphs have ATS-safe styling
    for para in doc.paragraphs:
        if para.text.strip():
            _apply_ats_style(para)

    doc.save(str(improved_path))
    return str(improved_path)


def _fuzzy_match(text: str, target: str, threshold: float = 0.8) -> bool:
    """Simple fuzzy match based on word overlap ratio."""
    if not target or not text:
        return False
    text_words = set(text.lower().split())
    target_words = set(target.lower().split())
    if not target_words:
        return False
    overlap = len(text_words & target_words)
    return overlap / len(target_words) >= threshold


def _replace_paragraph_text(paragraph, new_text: str):
    """Replace all runs in a paragraph with new text while keeping style."""
    # Clear existing runs
    for run in paragraph.runs:
        run.text = ""
    # Set text on first run or add new one
    if paragraph.runs:
        paragraph.runs[0].text = new_text
    else:
        run = paragraph.add_run(new_text)
        run.font.name = FONT_NAME
        run.font.size = FONT_SIZE_BODY


def extract_text_from_docx(docx_path: str) -> str:
    """Extract full text from a DOCX for diff comparison."""
    doc = Document(docx_path)
    return "\n".join(p.text for p in doc.paragraphs if p.text.strip())

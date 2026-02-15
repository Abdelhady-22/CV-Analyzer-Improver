"""
File parsing service — extracts text from PDF and DOCX uploads.
Uses pdfplumber for PDF and python-docx for DOCX.
"""

from __future__ import annotations

from pathlib import Path

import pdfplumber
from docx import Document

from config import get_settings


class FileTooLargeError(Exception):
    pass


class PageCountExceededError(Exception):
    pass


class UnsupportedFileTypeError(Exception):
    pass


def parse_pdf(file_path: str) -> tuple[str, int]:
    """
    Extract text from a PDF file.
    Returns (text, page_count).
    Raises PageCountExceededError if page count exceeds limit.
    """
    max_pages = get_settings().max_page_count
    text_parts: list[str] = []

    with pdfplumber.open(file_path) as pdf:
        page_count = len(pdf.pages)
        if page_count > max_pages:
            raise PageCountExceededError(
                f"PDF has {page_count} pages, max allowed is {max_pages}"
            )
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text_parts.append(page_text)

    return "\n\n".join(text_parts), page_count


def parse_docx(file_path: str) -> tuple[str, int]:
    """
    Extract text from a DOCX file.
    Returns (text, estimated_page_count).
    Page count is estimated from paragraph count (~40 paragraphs per page).
    """
    doc = Document(file_path)
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
    text = "\n".join(paragraphs)

    # Rough page estimate
    estimated_pages = max(1, len(paragraphs) // 40)
    max_pages = get_settings().max_page_count
    if estimated_pages > max_pages:
        raise PageCountExceededError(
            f"DOCX has ~{estimated_pages} pages, max allowed is {max_pages}"
        )

    return text, estimated_pages


def parse_file(file_path: str) -> tuple[str, int]:
    """
    Dispatcher: parse a file based on its extension.
    Returns (text, page_count).
    """
    ext = Path(file_path).suffix.lower()
    if ext == ".pdf":
        return parse_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return parse_docx(file_path)
    else:
        raise UnsupportedFileTypeError(
            f"Unsupported file type: {ext}. Only PDF and DOCX are accepted."
        )


def validate_file_size(file_size_bytes: int) -> None:
    """Raise if file exceeds configured max size."""
    max_mb = get_settings().max_file_size_mb
    max_bytes = max_mb * 1024 * 1024
    if file_size_bytes > max_bytes:
        raise FileTooLargeError(
            f"File size {file_size_bytes / 1024 / 1024:.1f}MB exceeds "
            f"max allowed {max_mb}MB"
        )

"""
Upload route — POST /api/upload
Accept PDF/DOCX, validate size/type, parse text, store in Supabase.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from fastapi import APIRouter, UploadFile, File, HTTPException

from config import ensure_upload_dir, get_settings
from models.cv import CVUploadResponse
from services.parser import (
    parse_file,
    validate_file_size,
    FileTooLargeError,
    PageCountExceededError,
    UnsupportedFileTypeError,
)
from repositories.upload_repo import create_upload

router = APIRouter()

ALLOWED_EXTENSIONS = {".pdf", ".docx", ".doc"}


@router.post("/upload", response_model=CVUploadResponse)
async def upload_cv(file: UploadFile = File(...)):
    """Upload a CV file (PDF or DOCX) for analysis."""

    # Validate file extension
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{ext}'. Accepted: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    # Read file content
    content = await file.read()

    # Validate file size
    try:
        validate_file_size(len(content))
    except FileTooLargeError as e:
        raise HTTPException(status_code=413, detail=str(e))

    # Save to disk
    upload_dir = ensure_upload_dir()
    file_path = upload_dir / file.filename
    with open(file_path, "wb") as f:
        f.write(content)

    # Parse text
    try:
        text, page_count = parse_file(str(file_path))
    except PageCountExceededError as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=str(e))
    except UnsupportedFileTypeError as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        file_path.unlink(missing_ok=True)
        raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")

    # Store in Supabase
    record = create_upload(file.filename, str(file_path))

    return CVUploadResponse(
        upload_id=record["id"],
        filename=file.filename,
        text_preview=text[:500],
        page_count=page_count,
    )

"""
Download routes:
  GET /api/download/{upload_id} — download improved DOCX
  GET /api/download/original/{upload_id} — download original file
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from repositories.upload_repo import get_upload

router = APIRouter()


@router.get("/download/{upload_id}")
async def download_improved_cv(upload_id: str):
    """Download the improved CV (DOCX). Only available after analysis completes."""
    upload = get_upload(upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    if upload.get("status") != "completed":
        raise HTTPException(
            status_code=400,
            detail=f"Analysis not completed yet. Status: {upload.get('status')}",
        )

    improved_path = upload.get("improved_path")
    if not improved_path or not Path(improved_path).exists():
        raise HTTPException(
            status_code=404,
            detail="Improved CV file not found. The original may not have been a DOCX.",
        )

    filename = Path(improved_path).name
    return FileResponse(
        path=improved_path,
        filename=filename,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )


@router.get("/download/original/{upload_id}")
async def download_original_cv(upload_id: str):
    """Download the original uploaded CV file."""
    upload = get_upload(upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    original_path = upload.get("original_path")
    if not original_path or not Path(original_path).exists():
        raise HTTPException(status_code=404, detail="Original file not found")

    filename = upload.get("filename", Path(original_path).name)
    ext = Path(original_path).suffix.lower()

    media_types = {
        ".pdf": "application/pdf",
        ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        ".doc": "application/msword",
    }

    return FileResponse(
        path=original_path,
        filename=filename,
        media_type=media_types.get(ext, "application/octet-stream"),
    )

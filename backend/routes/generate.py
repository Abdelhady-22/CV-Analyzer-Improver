"""
Generate route — POST /api/generate
Build a brand-new CV from structured data.
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from models.cv import StructuredCVData
from models.generation import GenerateCVRequest, GenerateCVResponse
from services.cv_generator import generate_cv
from services.cv_editor import extract_text_from_docx

router = APIRouter()


@router.post("/generate", response_model=GenerateCVResponse)
async def generate_new_cv(request: GenerateCVRequest):
    """Generate a brand-new ATS-optimized CV from structured data."""
    try:
        # Merge target info into cv_data if provided
        cv_data = request.cv_data
        if request.target_industry:
            cv_data.target_industry = request.target_industry
        if request.target_role_level:
            cv_data.target_role_level = request.target_role_level

        # Generate the DOCX
        output_path = generate_cv(cv_data)

        # Extract preview text
        preview = extract_text_from_docx(output_path)

        # Use the filename as the download ID
        filename = Path(output_path).name
        download_id = Path(output_path).stem

        return GenerateCVResponse(
            download_id=download_id,
            filename=filename,
            preview_text=preview[:500],
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate CV: {str(e)}",
        )


@router.get("/generate/download/{download_id}")
async def download_generated_cv(download_id: str):
    """Download a generated CV by its download ID."""
    from config import ensure_upload_dir
    upload_dir = ensure_upload_dir()
    file_path = upload_dir / f"{download_id}.docx"

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Generated CV not found")

    return FileResponse(
        path=str(file_path),
        filename=f"{download_id}.docx",
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    )

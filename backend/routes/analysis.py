"""
Analysis routes:
  POST /api/analyze — run full pipeline (with lock guard)
  GET  /api/analyze/status/{id} — poll pipeline progress
  GET  /api/analyze/result/{id} — get cached result
"""

from __future__ import annotations

import threading
from fastapi import APIRouter, HTTPException, BackgroundTasks

from models.analysis import AnalysisRequest, AnalysisResponse, PipelineStatus
from repositories.upload_repo import get_upload, update_upload_status
from repositories.analysis_repo import create_analysis, get_analysis_by_upload
from services.parser import parse_file
from services.cv_editor import apply_edits, extract_text_from_docx, create_docx_from_text
from services.diff_service import compute_diff
from agents.crew import run_analysis_pipeline, get_pipeline_status

router = APIRouter()


def _run_pipeline_background(
    upload_id: str,
    cv_text: str,
    original_path: str,
    job_title: str = None,
    job_description: str = None,
):
    """Background task: run pipeline, apply edits, persist results."""
    try:
        # Run the CrewAI pipeline
        result = run_analysis_pipeline(
            upload_id, cv_text, job_title, job_description
        )

        # Apply paragraph edits to the DOCX
        improved_path = None
        improved_text = cv_text
        diff_chunks = []

        if result.get("paragraph_edits") and original_path.endswith(".docx"):
            # Original is DOCX — apply surgical edits
            from models.analysis import ParagraphEdit
            edits = [ParagraphEdit(**e) for e in result["paragraph_edits"]]
            improved_path = apply_edits(original_path, edits)
            improved_text = extract_text_from_docx(improved_path)
            diff_chunks = [c.model_dump() for c in compute_diff(cv_text, improved_text)]
        elif result.get("paragraph_edits") and not original_path.endswith(".docx"):
            # Original is PDF — generate a new DOCX from improved text
            from models.analysis import ParagraphEdit
            from pathlib import Path
            # Build improved text by applying edits to the original text
            improved_text = cv_text
            for edit_data in result["paragraph_edits"]:
                old_text = edit_data.get("old_text", "")
                new_text = edit_data.get("new_text", "")
                if old_text and new_text and old_text in improved_text:
                    improved_text = improved_text.replace(old_text, new_text, 1)

            output_docx = str(Path(original_path).parent / f"{Path(original_path).stem}_improved.docx")
            improved_path = create_docx_from_text(improved_text, output_docx)
            diff_chunks = [c.model_dump() for c in compute_diff(cv_text, improved_text)]

        result["rewritten_text"] = improved_text
        result["diff"] = diff_chunks

        # Persist analysis result to Supabase
        create_analysis(upload_id, result)

        # Update upload status
        update_upload_status(upload_id, "completed", improved_path)

    except Exception as e:
        update_upload_status(upload_id, "failed")
        raise


@router.post("/analyze")
async def analyze_cv(request: AnalysisRequest, background_tasks: BackgroundTasks):
    """
    Start the full analysis pipeline for an uploaded CV.
    Lock guard: rejects if status is already 'analyzing'.
    """
    upload = get_upload(request.upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    # Lock guard: prevent double-triggering
    if upload.get("status") == "analyzing":
        raise HTTPException(
            status_code=409,
            detail="Analysis already in progress for this upload",
        )

    # Check for cached result
    cached = get_analysis_by_upload(request.upload_id)
    if cached and upload.get("status") == "completed":
        return {
            "upload_id": request.upload_id,
            "status": "completed",
            "message": "Analysis already completed. Use GET /api/analyze/result/{id} for results.",
        }

    # Parse the file
    file_path = upload.get("original_path", "")
    try:
        cv_text, _ = parse_file(file_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to parse file: {str(e)}")

    # Set status to analyzing
    update_upload_status(request.upload_id, "analyzing")

    # Run pipeline in background
    background_tasks.add_task(
        _run_pipeline_background,
        request.upload_id,
        cv_text,
        file_path,
        request.target_job_title,
        request.job_description,
    )

    return {
        "upload_id": request.upload_id,
        "status": "analyzing",
        "message": "Analysis started. Poll GET /api/analyze/status/{id} for progress.",
    }


@router.get("/analyze/status/{upload_id}")
async def get_analysis_status(upload_id: str):
    """Poll analysis pipeline progress (per-agent steps)."""
    # Check in-memory progress first
    progress = get_pipeline_status(upload_id)
    if progress:
        return progress.model_dump()

    # Fall back to Supabase status
    upload = get_upload(upload_id)
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    return {
        "upload_id": upload_id,
        "overall_status": upload.get("status", "unknown"),
        "steps": [],
    }


@router.get("/analyze/result/{upload_id}", response_model=AnalysisResponse)
async def get_analysis_result(upload_id: str):
    """Get cached analysis result for instant reload."""
    cached = get_analysis_by_upload(upload_id)
    if not cached:
        upload = get_upload(upload_id)
        status = upload.get("status", "unknown") if upload else "not_found"
        raise HTTPException(
            status_code=404,
            detail=f"No analysis found. Current status: {status}",
        )

    upload = get_upload(upload_id)

    # Reconstruct diff if needed
    diff_data = []
    original_text = ""
    improved_text = cached.get("rewritten_text", "")

    if upload and upload.get("original_path"):
        try:
            original_text, _ = parse_file(upload["original_path"])
            if improved_text and improved_text != original_text:
                diff_data = [c.model_dump() for c in compute_diff(original_text, improved_text)]
        except Exception:
            pass

    return AnalysisResponse(
        upload_id=upload_id,
        status="completed",
        inferred_profile=cached.get("inferred_profile"),
        score=cached.get("score"),
        issues=cached.get("issues", []),
        recommendations=cached.get("recommendations", []),
        paragraph_edits=cached.get("paragraph_edits", []),
        diff=diff_data,
        original_text=original_text,
        improved_text=improved_text,
    )

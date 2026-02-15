"""
Analysis repository — CRUD for the `analyses` Supabase table.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from repositories.supabase_client import get_supabase


def create_analysis(upload_id: str, data: dict) -> dict:
    """Insert a new analysis record."""
    record = {
        "id": str(uuid.uuid4()),
        "upload_id": upload_id,
        "inferred_profile": data.get("inferred_profile"),
        "score": data.get("score"),
        "issues": data.get("issues"),
        "recommendations": data.get("recommendations"),
        "paragraph_edits": data.get("paragraph_edits"),
        "rewritten_text": data.get("rewritten_text", ""),
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    result = get_supabase().table("analyses").insert(record).execute()
    return result.data[0] if result.data else record


def get_analysis_by_upload(upload_id: str) -> Optional[dict]:
    """Return cached analysis for a given upload, if exists."""
    result = (
        get_supabase()
        .table("analyses")
        .select("*")
        .eq("upload_id", upload_id)
        .order("created_at", desc=True)
        .limit(1)
        .execute()
    )
    return result.data[0] if result.data else None

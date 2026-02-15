"""
Analysis repository — CRUD for the `analyses` table.
Falls back to in-memory dict when Supabase is not configured.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from repositories.supabase_client import get_supabase

# In-memory fallback store (keyed by upload_id)
_memory_analyses: dict[str, dict] = {}


def create_analysis(upload_id: str, data: dict) -> dict:
    """Insert a new analysis record."""
    record = {
        "id": str(uuid.uuid4()),
        "upload_id": upload_id,
        "result": data,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    db = get_supabase()
    if db:
        try:
            result = db.table("analyses").insert(record).execute()
            return result.data[0] if result.data else record
        except Exception as e:
            print(f"[WARN] Supabase insert failed: {e}")

    # In-memory fallback
    _memory_analyses[upload_id] = data
    return record


def get_analysis_by_upload(upload_id: str) -> Optional[dict]:
    """Return cached analysis for a given upload, if exists."""
    db = get_supabase()
    if db:
        try:
            result = (
                db.table("analyses")
                .select("*")
                .eq("upload_id", upload_id)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )
            if result.data:
                row = result.data[0]
                return row.get("result", row)
        except Exception:
            pass

    return _memory_analyses.get(upload_id)

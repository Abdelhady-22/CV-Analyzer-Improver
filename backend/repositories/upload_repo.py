"""
Upload repository — CRUD for the `uploads` table.
Falls back to in-memory dict when Supabase is not configured.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from repositories.supabase_client import get_supabase

# In-memory fallback store
_memory_uploads: dict[str, dict] = {}


def create_upload(filename: str, original_path: str) -> dict:
    """Insert a new upload record, return the created row."""
    record = {
        "id": str(uuid.uuid4()),
        "filename": filename,
        "original_path": original_path,
        "improved_path": None,
        "status": "uploaded",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    db = get_supabase()
    if db:
        try:
            result = db.table("uploads").insert(record).execute()
            return result.data[0] if result.data else record
        except Exception as e:
            print(f"[WARN] Supabase insert failed: {e}")

    # In-memory fallback
    _memory_uploads[record["id"]] = record
    return record


def get_upload(upload_id: str) -> Optional[dict]:
    db = get_supabase()
    if db:
        try:
            result = (
                db.table("uploads")
                .select("*")
                .eq("id", upload_id)
                .execute()
            )
            return result.data[0] if result.data else None
        except Exception:
            pass

    return _memory_uploads.get(upload_id)


def update_upload_status(upload_id: str, status: str, improved_path: str = None) -> dict:
    update_data = {"status": status}
    if improved_path:
        update_data["improved_path"] = improved_path

    db = get_supabase()
    if db:
        try:
            result = (
                db.table("uploads")
                .update(update_data)
                .eq("id", upload_id)
                .execute()
            )
            return result.data[0] if result.data else {}
        except Exception:
            pass

    # In-memory fallback
    if upload_id in _memory_uploads:
        _memory_uploads[upload_id].update(update_data)
        return _memory_uploads[upload_id]
    return {}

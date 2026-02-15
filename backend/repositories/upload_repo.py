"""
Upload repository — CRUD for the `uploads` Supabase table.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from typing import Optional

from repositories.supabase_client import get_supabase


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
    result = get_supabase().table("uploads").insert(record).execute()
    return result.data[0] if result.data else record


def get_upload(upload_id: str) -> Optional[dict]:
    result = (
        get_supabase()
        .table("uploads")
        .select("*")
        .eq("id", upload_id)
        .execute()
    )
    return result.data[0] if result.data else None


def update_upload_status(upload_id: str, status: str, improved_path: str = None) -> dict:
    update_data = {"status": status}
    if improved_path:
        update_data["improved_path"] = improved_path
    result = (
        get_supabase()
        .table("uploads")
        .update(update_data)
        .eq("id", upload_id)
        .execute()
    )
    return result.data[0] if result.data else {}

"""
Singleton Supabase client, initialized from .env settings.
Returns None if Supabase is not configured (graceful fallback).
"""

from __future__ import annotations

from functools import lru_cache
from typing import Optional

from config import get_settings


@lru_cache()
def get_supabase() -> Optional[object]:
    s = get_settings()
    if not s.supabase_url or not s.supabase_key:
        print("[INFO] Supabase not configured — using in-memory storage.")
        return None
    try:
        from supabase import create_client
        return create_client(s.supabase_url, s.supabase_key)
    except Exception as e:
        print(f"[WARN] Supabase connection failed: {e} — using in-memory storage.")
        return None

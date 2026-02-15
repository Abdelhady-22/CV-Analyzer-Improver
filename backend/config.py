"""
Centralized application configuration.
Reads from .env and exposes typed settings + LLM config helper.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    # LLM
    llm_provider: str = "ollama"
    llm_model: str = "llama3.1"
    ollama_base_url: str = "http://localhost:11434"
    gemini_api_key: str = ""
    openai_api_key: str = ""

    # Supabase
    supabase_url: str = ""
    supabase_key: str = ""

    # Upload limits
    max_file_size_mb: int = 10
    max_page_count: int = 20
    upload_dir: str = "./uploads"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def get_llm_config() -> dict:
    """
    Return provider-specific config dict for CrewAI / LiteLLM.
    Supports: ollama, gemini, openai.
    """
    s = get_settings()
    provider = s.llm_provider.lower()

    if provider == "ollama":
        return {
            "model": f"ollama/{s.llm_model}",
            "base_url": s.ollama_base_url,
        }
    elif provider == "gemini":
        os.environ["GEMINI_API_KEY"] = s.gemini_api_key
        return {
            "model": f"gemini/{s.llm_model}",
        }
    elif provider == "openai":
        os.environ["OPENAI_API_KEY"] = s.openai_api_key
        return {
            "model": s.llm_model,
        }
    else:
        raise ValueError(f"Unsupported LLM_PROVIDER: {provider}")


def ensure_upload_dir() -> Path:
    """Create and return the upload directory path."""
    p = Path(get_settings().upload_dir)
    p.mkdir(parents=True, exist_ok=True)
    return p

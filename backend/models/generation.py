"""
CV generation request/response models.
"""

from __future__ import annotations

from pydantic import BaseModel, Field
from models.cv import StructuredCVData


class GenerateCVRequest(BaseModel):
    """Request body for generating a brand-new CV from structured data."""
    cv_data: StructuredCVData
    target_industry: str = Field(
        "", description="Target industry for keyword optimization"
    )
    target_role_level: str = Field(
        "", description="Target role level (Junior, Mid, Senior, etc.)"
    )


class GenerateCVResponse(BaseModel):
    download_id: str
    filename: str
    preview_text: str = Field(
        "", description="First 500 chars of the generated CV text"
    )

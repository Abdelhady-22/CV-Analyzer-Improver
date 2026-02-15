"""
CV-related Pydantic models: upload responses, structured CV data, inferred profile.
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Sub-models for structured CV data ──────────────────────────


class ExperienceEntry(BaseModel):
    job_title: str
    company: str
    start_date: str
    end_date: str = "Present"
    location: Optional[str] = None
    bullets: list[str] = Field(default_factory=list)


class EducationEntry(BaseModel):
    degree: str
    institution: str
    start_date: str
    end_date: str
    gpa: Optional[str] = None
    location: Optional[str] = None


class CertificationEntry(BaseModel):
    name: str
    issuer: Optional[str] = None
    date: Optional[str] = None


class StructuredCVData(BaseModel):
    """Full structured CV for new-CV generation."""
    full_name: str
    email: str
    phone: Optional[str] = None
    location: Optional[str] = None
    linkedin: Optional[str] = None
    website: Optional[str] = None
    summary: str = ""
    experience: list[ExperienceEntry] = Field(default_factory=list)
    education: list[EducationEntry] = Field(default_factory=list)
    skills: list[str] = Field(default_factory=list)
    certifications: list[CertificationEntry] = Field(default_factory=list)
    target_industry: Optional[str] = None
    target_role_level: Optional[str] = None


# ── Upload response ────────────────────────────────────────────


class CVUploadResponse(BaseModel):
    upload_id: str
    filename: str
    text_preview: str = Field(
        ..., description="First 500 chars of extracted text"
    )
    page_count: int = 0


# ── Inferred profile (agent output contract) ──────────────────


class InferredProfile(BaseModel):
    """Output of the InferAgent — strict contract."""
    industry: str = Field(..., description="E.g. 'Software Engineering', 'Marketing'")
    role_level: str = Field(
        ..., description="E.g. 'Junior', 'Mid-level', 'Senior', 'Lead', 'Executive'"
    )
    years_experience: int = Field(
        ..., description="Estimated total years of experience"
    )
    key_skills: list[str] = Field(
        default_factory=list,
        description="Top skills detected from the CV",
    )

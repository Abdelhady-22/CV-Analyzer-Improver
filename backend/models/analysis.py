"""
Analysis-related Pydantic models:
  AnalysisRequest, scores, issues, recommendations, paragraph edits, rule findings.
"""

from __future__ import annotations

from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


# ── Enums ──────────────────────────────────────────────────────


class Severity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class EditType(str, Enum):
    ADD = "add"
    REMOVE = "remove"
    REWRITE = "rewrite"


# ── Analysis request (with optional job-target context) ────────


class AnalysisRequest(BaseModel):
    upload_id: str
    target_job_title: Optional[str] = Field(
        None, description="Optional target job title for relevance matching"
    )
    job_description: Optional[str] = Field(
        None, description="Optional job description text for keyword matching"
    )


# ── Rule-based scoring (explainable) ──────────────────────────


class RuleFinding(BaseModel):
    """Single deterministic rule result — powers the explainable scoring UI."""
    rule: str = Field(..., description="Rule name, e.g. 'Has Skills Section'")
    passed: bool
    weight: int = Field(..., description="Points added/deducted")
    explanation: str = Field(
        ..., description="Human-readable, e.g. 'Missing Skills section (−8 pts)'"
    )


class RuleBasedScore(BaseModel):
    """60% of total ATS score — deterministic, explainable."""
    score: float = Field(..., ge=0, le=100)
    findings: list[RuleFinding] = Field(default_factory=list)


# ── LLM-based scoring ─────────────────────────────────────────


class LLMScore(BaseModel):
    """40% of total ATS score — AI quality judgment (agent output contract)."""
    score: float = Field(..., ge=0, le=100)
    keyword_score: float = Field(0, ge=0, le=100)
    structure_score: float = Field(0, ge=0, le=100)
    formatting_score: float = Field(0, ge=0, le=100)
    parsing_safety_score: float = Field(0, ge=0, le=100)
    summary: str = Field("", description="Brief AI assessment")


class ATSScore(BaseModel):
    """Combined ATS score shown in UI."""
    overall: float = Field(..., ge=0, le=100)
    rule_based: RuleBasedScore
    llm_based: LLMScore


# ── ATS issues ─────────────────────────────────────────────────


class ATSIssue(BaseModel):
    severity: Severity
    category: str = Field(..., description="E.g. 'keywords', 'structure', 'formatting', 'parsing'")
    description: str
    location: Optional[str] = Field(None, description="Section or paragraph reference")


# ── Recommendations ────────────────────────────────────────────


class Recommendation(BaseModel):
    edit_type: EditType
    section: str
    original_text: Optional[str] = None
    suggested_text: str
    rationale: str


# ── Paragraph-level edits (rewrite agent output contract) ──────


class ParagraphEdit(BaseModel):
    """Surgical edit for cv_editor — maps directly to a DOCX paragraph."""
    section: str
    paragraph_index: int = Field(
        ..., description="0-based index within the section"
    )
    old_text: str
    new_text: str


# ── Diff chunk (for the frontend diff viewer) ─────────────────


class DiffChunk(BaseModel):
    type: str = Field(..., description="'add', 'remove', or 'equal'")
    text: str


# ── Full analysis response ─────────────────────────────────────


class AnalysisResponse(BaseModel):
    upload_id: str
    status: str = Field("completed", description="uploaded|analyzing|completed|failed")
    inferred_profile: Optional[dict] = None
    score: Optional[ATSScore] = None
    issues: list[ATSIssue] = Field(default_factory=list)
    recommendations: list[Recommendation] = Field(default_factory=list)
    paragraph_edits: list[ParagraphEdit] = Field(default_factory=list)
    diff: list[DiffChunk] = Field(default_factory=list)
    original_text: str = ""
    improved_text: str = ""


# ── Pipeline progress (for polling endpoint) ──────────────────


class AgentStep(BaseModel):
    name: str
    status: str = Field("pending", description="pending|running|completed|failed")


class PipelineStatus(BaseModel):
    upload_id: str
    overall_status: str
    steps: list[AgentStep] = Field(default_factory=list)
    error: Optional[str] = None

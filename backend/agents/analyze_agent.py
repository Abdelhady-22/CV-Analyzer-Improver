"""
AnalyzeAgent — performs deep ATS analysis: keyword gaps, structure, formatting, parsing risks.
Output contract: list of ATSIssue dicts.
"""

from __future__ import annotations

from crewai import Agent, Task
from pydantic import BaseModel, Field
from typing import Optional

from config import get_llm_config
from models.analysis import ATSIssue, Severity


class ATSIssueList(BaseModel):
    """Wrapper for agent output — a list of ATS issues."""
    issues: list[ATSIssue] = Field(default_factory=list)


def create_analyze_agent() -> Agent:
    llm_config = get_llm_config()
    return Agent(
        role="ATS Compliance Analyst",
        goal=(
            "Perform a thorough ATS (Applicant Tracking System) compliance "
            "analysis of the CV. Identify issues with keywords, section structure, "
            "formatting, and elements that may cause parsing failures."
        ),
        backstory=(
            "You are a senior talent acquisition specialist who deeply understands "
            "how ATS software (Workday, Greenhouse, Lever, Taleo) parses CVs. "
            "You know exactly what causes parsing failures and what formatting "
            "choices reduce a candidate's chances."
        ),
        llm=llm_config["model"],
        verbose=False,
        allow_delegation=False,
    )


def create_analyze_task(
    agent: Agent,
    cv_text: str,
    inferred_profile: dict,
    job_title: str = None,
    job_description: str = None,
) -> Task:
    context = (
        f"INFERRED PROFILE:\n"
        f"Industry: {inferred_profile.get('industry', 'Unknown')}\n"
        f"Role Level: {inferred_profile.get('role_level', 'Unknown')}\n"
        f"Key Skills: {', '.join(inferred_profile.get('key_skills', []))}\n\n"
    )
    if job_title:
        context += f"TARGET JOB TITLE: {job_title}\n"
    if job_description:
        context += f"JOB DESCRIPTION:\n{job_description[:2000]}\n\n"

    return Task(
        description=(
            f"{context}"
            f"Analyze this CV for ATS compliance issues. Check:\n"
            f"1. KEYWORDS: Missing industry-standard keywords for the role\n"
            f"2. STRUCTURE: Missing or poorly ordered sections\n"
            f"3. FORMATTING: Non-standard fonts, tables, multi-column layouts\n"
            f"4. PARSING RISKS: Elements that may break ATS parsing\n\n"
            f"For each issue, assign a severity (low/medium/high/critical) "
            f"and categorize it.\n\n"
            f"CV TEXT:\n{cv_text[:4000]}"
        ),
        expected_output="A JSON with a list of ATS issues, each with severity, category, description, and location",
        agent=agent,
        output_pydantic=ATSIssueList,
    )

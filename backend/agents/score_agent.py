"""
ScoreAgent — provides AI quality judgment (40% of total ATS score).
Output contract: LLMScore (Pydantic model).
"""

from __future__ import annotations

from crewai import Agent, Task

from config import get_llm_config
from models.analysis import LLMScore


def create_score_agent() -> Agent:
    llm_config = get_llm_config()
    return Agent(
        role="ATS Score Evaluator",
        goal=(
            "Evaluate the overall quality of the CV from an ATS perspective. "
            "Provide numerical scores for keyword optimization, structure quality, "
            "formatting compliance, and parsing safety."
        ),
        backstory=(
            "You are an ATS scoring algorithm expert who can assess how well "
            "a CV will perform when processed by major ATS platforms. You assign "
            "fair, calibrated scores based on industry best practices."
        ),
        llm=llm_config["model"],
        verbose=False,
        allow_delegation=False,
    )


def create_score_task(
    agent: Agent,
    cv_text: str,
    issues: list[dict],
    inferred_profile: dict,
) -> Task:
    issues_summary = "\n".join(
        f"- [{i.get('severity', 'medium')}] {i.get('description', '')}"
        for i in issues[:15]
    )

    return Task(
        description=(
            f"Based on the CV text and the ATS issues identified below, "
            f"provide quality scores (0–100) for:\n"
            f"1. keyword_score — relevance and density of industry keywords\n"
            f"2. structure_score — proper section ordering and completeness\n"
            f"3. formatting_score — ATS-safe formatting compliance\n"
            f"4. parsing_safety_score — likelihood of successful ATS parsing\n"
            f"5. score — overall AI quality score (0–100)\n"
            f"6. summary — brief 1-2 sentence assessment\n\n"
            f"PROFILE: {inferred_profile.get('industry', 'Unknown')} / "
            f"{inferred_profile.get('role_level', 'Unknown')}\n\n"
            f"IDENTIFIED ISSUES:\n{issues_summary}\n\n"
            f"CV TEXT:\n{cv_text[:3000]}"
        ),
        expected_output="A JSON with score, keyword_score, structure_score, formatting_score, parsing_safety_score, and summary",
        agent=agent,
        output_pydantic=LLMScore,
    )

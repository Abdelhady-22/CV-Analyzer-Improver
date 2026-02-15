"""
RecommendAgent — generates actionable edit recommendations with rationale.
Output contract: RecommendationList (Pydantic wrapper).
"""

from __future__ import annotations

from crewai import Agent, Task
from pydantic import BaseModel, Field

from config import get_llm_config
from models.analysis import Recommendation


class RecommendationList(BaseModel):
    """Wrapper for agent output — a list of recommendations."""
    recommendations: list[Recommendation] = Field(default_factory=list)


def create_recommend_agent() -> Agent:
    llm_config = get_llm_config()
    return Agent(
        role="CV Improvement Advisor",
        goal=(
            "Generate specific, actionable edit recommendations for the CV. "
            "Each recommendation must include the section, edit type (add/remove/rewrite), "
            "the original text, suggested replacement, and a clear rationale."
        ),
        backstory=(
            "You are a professional CV consultant who helps candidates optimize "
            "their CVs for ATS systems. You focus on measurable achievements, "
            "strong action verbs, proper keyword placement, and clean formatting."
        ),
        llm=llm_config["model"],
        verbose=False,
        allow_delegation=False,
    )


def create_recommend_task(
    agent: Agent,
    cv_text: str,
    issues: list[dict],
    inferred_profile: dict,
) -> Task:
    issues_summary = "\n".join(
        f"- [{i.get('severity', 'medium')}] {i.get('category', '')}: {i.get('description', '')}"
        for i in issues[:15]
    )

    return Task(
        description=(
            f"Based on the ATS issues below and the CV text, generate a list of "
            f"specific edit recommendations.\n\n"
            f"For each recommendation provide:\n"
            f"- edit_type: 'add', 'remove', or 'rewrite'\n"
            f"- section: which CV section (e.g. 'experience', 'summary', 'skills')\n"
            f"- original_text: the current text (null for 'add')\n"
            f"- suggested_text: the improved text\n"
            f"- rationale: why this change improves ATS performance\n\n"
            f"Focus on:\n"
            f"- Adding measurable achievements with numbers/percentages\n"
            f"- Using strong action verbs\n"
            f"- Including missing keywords for {inferred_profile.get('industry', 'the target industry')}\n"
            f"- Improving section structure\n\n"
            f"ISSUES:\n{issues_summary}\n\n"
            f"CV TEXT:\n{cv_text[:4000]}"
        ),
        expected_output="A JSON with a list of recommendations, each with edit_type, section, original_text, suggested_text, and rationale",
        agent=agent,
        output_pydantic=RecommendationList,
    )

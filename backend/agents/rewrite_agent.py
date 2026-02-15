"""
RewriteAgent — produces surgical paragraph-level edits for cv_editor.
Output contract: ParagraphEditList (maps directly to DOCX paragraphs).
"""

from __future__ import annotations

from crewai import Agent, Task
from pydantic import BaseModel, Field

from config import get_llm_config
from models.analysis import ParagraphEdit


class ParagraphEditList(BaseModel):
    """Wrapper for agent output — surgical paragraph-level edits."""
    edits: list[ParagraphEdit] = Field(default_factory=list)


def create_rewrite_agent() -> Agent:
    llm_config = get_llm_config()
    return Agent(
        role="CV Rewriter",
        goal=(
            "Apply the approved recommendations by producing exact paragraph-level "
            "edits. Each edit specifies the section, paragraph index, old text, and "
            "new improved text. The new text must be ATS-optimized with strong action "
            "verbs, measurable achievements, and proper keywords."
        ),
        backstory=(
            "You are a meticulous CV editor who rewrites paragraphs to maximize "
            "ATS scores. You preserve the candidate's authentic experience while "
            "dramatically improving keyword density, action verbs, and measured "
            "impact statements."
        ),
        llm=llm_config["model"],
        verbose=False,
        allow_delegation=False,
    )


def create_rewrite_task(
    agent: Agent,
    cv_text: str,
    recommendations: list[dict],
) -> Task:
    recs_text = "\n".join(
        f"- [{r.get('edit_type', 'rewrite')}] Section: {r.get('section', 'unknown')} | "
        f"Suggested: {r.get('suggested_text', '')[:100]}..."
        for r in recommendations[:15]
    )

    return Task(
        description=(
            f"Apply the following recommendations as surgical paragraph-level edits.\n\n"
            f"For each edit, output:\n"
            f"- section: the CV section name (e.g. 'experience', 'summary')\n"
            f"- paragraph_index: 0-based index of the paragraph within that section\n"
            f"- old_text: the exact current paragraph text\n"
            f"- new_text: the improved replacement text\n\n"
            f"Rules:\n"
            f"- Use strong action verbs (Spearheaded, Optimized, Delivered, Architected)\n"
            f"- Include measurable achievements where possible\n"
            f"- Keep professional tone\n"
            f"- Do NOT add tables, icons, or graphics\n\n"
            f"RECOMMENDATIONS:\n{recs_text}\n\n"
            f"CV TEXT:\n{cv_text[:4000]}"
        ),
        expected_output="A JSON with a list of paragraph edits, each with section, paragraph_index, old_text, and new_text",
        agent=agent,
        output_pydantic=ParagraphEditList,
    )

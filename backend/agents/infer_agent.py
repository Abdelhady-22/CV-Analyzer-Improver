"""
InferAgent — infers industry, role level, and years of experience from CV text.
Output contract: InferredProfile (Pydantic model).
"""

from __future__ import annotations

from crewai import Agent, Task

from config import get_llm_config
from models.cv import InferredProfile


def create_infer_agent() -> Agent:
    llm_config = get_llm_config()
    return Agent(
        role="CV Industry & Role Classifier",
        goal=(
            "Analyze the CV text and determine the candidate's industry field, "
            "role level (Junior/Mid/Senior/Lead/Executive), estimated years of "
            "experience, and top key skills."
        ),
        backstory=(
            "You are an expert HR analyst who has reviewed thousands of CVs "
            "across all industries. You can accurately classify a candidate's "
            "background from their CV content alone."
        ),
        llm=llm_config["model"],
        verbose=False,
        allow_delegation=False,
    )


def create_infer_task(agent: Agent, cv_text: str) -> Task:
    return Task(
        description=(
            f"Analyze the following CV text and determine:\n"
            f"1. The industry field (e.g. 'Software Engineering', 'Marketing')\n"
            f"2. The role level (Junior, Mid-level, Senior, Lead, Executive)\n"
            f"3. Estimated total years of experience\n"
            f"4. Top key skills detected\n\n"
            f"CV TEXT:\n{cv_text[:4000]}"
        ),
        expected_output="A JSON with industry, role_level, years_experience, and key_skills",
        agent=agent,
        output_pydantic=InferredProfile,
    )

"""
Crew orchestrator — runs the sequential pipeline:
  infer → analyze → deterministic_score + llm_score → recommend → rewrite
"""

from __future__ import annotations

import traceback
from typing import Optional

from crewai import Crew, Process

from agents.infer_agent import create_infer_agent, create_infer_task
from agents.analyze_agent import create_analyze_agent, create_analyze_task
from agents.score_agent import create_score_agent, create_score_task
from agents.recommend_agent import create_recommend_agent, create_recommend_task
from agents.rewrite_agent import create_rewrite_agent, create_rewrite_task
from services.scoring_service import compute_rule_based_score
from models.analysis import ATSScore, AnalysisResponse, PipelineStatus, AgentStep
from models.cv import InferredProfile


# In-memory pipeline progress tracker (per upload)
_pipeline_progress: dict[str, PipelineStatus] = {}


def get_pipeline_status(upload_id: str) -> Optional[PipelineStatus]:
    return _pipeline_progress.get(upload_id)


def _update_step(upload_id: str, step_name: str, status: str):
    """Update a specific step's status in the pipeline tracker."""
    if upload_id in _pipeline_progress:
        for step in _pipeline_progress[upload_id].steps:
            if step.name == step_name:
                step.status = status
                break


def run_analysis_pipeline(
    upload_id: str,
    cv_text: str,
    job_title: Optional[str] = None,
    job_description: Optional[str] = None,
) -> dict:
    """
    Run the full analysis pipeline and return structured results.
    Returns a dict ready to be serialized as AnalysisResponse.
    """
    # Initialize progress tracking
    _pipeline_progress[upload_id] = PipelineStatus(
        upload_id=upload_id,
        overall_status="analyzing",
        steps=[
            AgentStep(name="infer", status="pending"),
            AgentStep(name="analyze", status="pending"),
            AgentStep(name="score", status="pending"),
            AgentStep(name="recommend", status="pending"),
            AgentStep(name="rewrite", status="pending"),
        ],
    )

    try:
        # ── Step 1: Infer ──────────────────────────────────────
        _update_step(upload_id, "infer", "running")
        infer_agent = create_infer_agent()
        infer_task = create_infer_task(infer_agent, cv_text)

        infer_crew = Crew(
            agents=[infer_agent],
            tasks=[infer_task],
            process=Process.sequential,
            verbose=False,
        )
        infer_result = infer_crew.kickoff()
        inferred_profile = _parse_pydantic_output(infer_result, InferredProfile)
        inferred_dict = inferred_profile.model_dump() if inferred_profile else {
            "industry": "General",
            "role_level": "Mid-level",
            "years_experience": 3,
            "key_skills": [],
        }
        _update_step(upload_id, "infer", "completed")

        # ── Step 2: Analyze ────────────────────────────────────
        _update_step(upload_id, "analyze", "running")
        analyze_agent = create_analyze_agent()
        analyze_task = create_analyze_task(
            analyze_agent, cv_text, inferred_dict, job_title, job_description
        )

        analyze_crew = Crew(
            agents=[analyze_agent],
            tasks=[analyze_task],
            process=Process.sequential,
            verbose=False,
        )
        analyze_result = analyze_crew.kickoff()
        issues_output = _parse_pydantic_output(analyze_result)
        issues_list = []
        if issues_output and hasattr(issues_output, "issues"):
            issues_list = [i.model_dump() for i in issues_output.issues]
        elif isinstance(issues_output, list):
            issues_list = issues_output
        _update_step(upload_id, "analyze", "completed")

        # ── Step 3: Score (deterministic + LLM) ────────────────
        _update_step(upload_id, "score", "running")

        # 3a. Deterministic rule-based score (60%)
        rule_score = compute_rule_based_score(cv_text, job_description)

        # 3b. LLM score (40%)
        score_agent = create_score_agent()
        score_task = create_score_task(
            score_agent, cv_text, issues_list, inferred_dict
        )
        score_crew = Crew(
            agents=[score_agent],
            tasks=[score_task],
            process=Process.sequential,
            verbose=False,
        )
        score_result = score_crew.kickoff()
        from models.analysis import LLMScore
        llm_score = _parse_pydantic_output(score_result, LLMScore)
        if not llm_score:
            llm_score = LLMScore(score=50, summary="Unable to compute AI score")

        # Combine: 60% rule + 40% LLM
        combined_score = round(rule_score.score * 0.6 + llm_score.score * 0.4, 1)
        ats_score = ATSScore(
            overall=combined_score,
            rule_based=rule_score,
            llm_based=llm_score,
        )
        _update_step(upload_id, "score", "completed")

        # ── Step 4: Recommend ──────────────────────────────────
        _update_step(upload_id, "recommend", "running")
        recommend_agent = create_recommend_agent()
        recommend_task = create_recommend_task(
            recommend_agent, cv_text, issues_list, inferred_dict
        )
        recommend_crew = Crew(
            agents=[recommend_agent],
            tasks=[recommend_task],
            process=Process.sequential,
            verbose=False,
        )
        recommend_result = recommend_crew.kickoff()
        recs_output = _parse_pydantic_output(recommend_result)
        recs_list = []
        if recs_output and hasattr(recs_output, "recommendations"):
            recs_list = [r.model_dump() for r in recs_output.recommendations]
        _update_step(upload_id, "recommend", "completed")

        # ── Step 5: Rewrite ────────────────────────────────────
        _update_step(upload_id, "rewrite", "running")
        rewrite_agent = create_rewrite_agent()
        rewrite_task = create_rewrite_task(
            rewrite_agent, cv_text, recs_list
        )
        rewrite_crew = Crew(
            agents=[rewrite_agent],
            tasks=[rewrite_task],
            process=Process.sequential,
            verbose=False,
        )
        rewrite_result = rewrite_crew.kickoff()
        edits_output = _parse_pydantic_output(rewrite_result)
        edits_list = []
        if edits_output and hasattr(edits_output, "edits"):
            edits_list = [e.model_dump() for e in edits_output.edits]
        _update_step(upload_id, "rewrite", "completed")

        # ── Finalize ───────────────────────────────────────────
        _pipeline_progress[upload_id].overall_status = "completed"

        return {
            "inferred_profile": inferred_dict,
            "score": ats_score.model_dump(),
            "issues": issues_list,
            "recommendations": recs_list,
            "paragraph_edits": edits_list,
            "rewritten_text": "",  # Will be filled after applying edits
        }

    except Exception as e:
        _pipeline_progress[upload_id].overall_status = "failed"
        _pipeline_progress[upload_id].error = str(e)
        traceback.print_exc()
        raise


def _parse_pydantic_output(result, model_class=None):
    """
    Safely extract pydantic output from CrewAI result.
    Handles both the .pydantic attribute and raw output.
    """
    try:
        if hasattr(result, "pydantic") and result.pydantic:
            return result.pydantic
        if hasattr(result, "json_dict") and result.json_dict:
            if model_class:
                return model_class(**result.json_dict)
            return result.json_dict
        if hasattr(result, "raw") and result.raw:
            import json
            data = json.loads(result.raw)
            if model_class:
                return model_class(**data)
            return data
    except Exception:
        pass
    return None

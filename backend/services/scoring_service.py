"""
Deterministic rule-based ATS scoring service.
Provides 60% of the total score — fully explainable.
"""

from __future__ import annotations

import re
from typing import Optional

from models.analysis import RuleFinding, RuleBasedScore


# ── Rule definitions ──────────────────────────────────────────

REQUIRED_SECTIONS = [
    ("contact", 8, r"(email|phone|address|linkedin)"),
    ("summary", 8, r"(summary|objective|profile|about)"),
    ("experience", 12, r"(experience|work\s*history|employment)"),
    ("education", 8, r"(education|academic|degree|university)"),
    ("skills", 8, r"(skills|competenc|technologies|tools)"),
]

OPTIONAL_SECTIONS = [
    ("certifications", 4, r"(certif|accredit|licens)"),
    ("projects", 4, r"(project|portfolio)"),
]


def _check_section_presence(text: str, sections: list, required: bool) -> list[RuleFinding]:
    """Check if required/optional sections are present."""
    findings = []
    text_lower = text.lower()
    for name, weight, pattern in sections:
        found = bool(re.search(pattern, text_lower))
        label = "Required" if required else "Optional"
        findings.append(
            RuleFinding(
                rule=f"Has {name.title()} Section",
                passed=found,
                weight=weight if found else -weight,
                explanation=(
                    f"{name.title()} section detected ✓"
                    if found
                    else f"Missing {name.title()} section (−{weight} pts)"
                ),
            )
        )
    return findings


def _check_bullet_points(text: str) -> RuleFinding:
    """Check if experience uses bullet points for achievements."""
    bullet_count = len(re.findall(r"^[\s]*[•\-\*▸►]\s+", text, re.MULTILINE))
    passed = bullet_count >= 3
    return RuleFinding(
        rule="Uses Bullet Points",
        passed=passed,
        weight=6 if passed else -6,
        explanation=(
            f"Found {bullet_count} bullet points ✓"
            if passed
            else f"Only {bullet_count} bullet points found — use bullets for achievements (−6 pts)"
        ),
    )


def _check_measurable_impacts(text: str) -> RuleFinding:
    """Check for quantified achievements (numbers, percentages, $)."""
    metrics = re.findall(r"\d+%|\$[\d,]+|\d+\+?\s*(years?|months?|clients?|users?|projects?)", text, re.IGNORECASE)
    passed = len(metrics) >= 2
    return RuleFinding(
        rule="Measurable Achievements",
        passed=passed,
        weight=8 if passed else -8,
        explanation=(
            f"Found {len(metrics)} quantified achievements ✓"
            if passed
            else f"Only {len(metrics)} quantified results — add numbers/percentages (−8 pts)"
        ),
    )


def _check_length(text: str) -> RuleFinding:
    """Check CV length is within ATS-friendly range (300–3000 words)."""
    word_count = len(text.split())
    passed = 300 <= word_count <= 3000
    if word_count < 300:
        expl = f"CV is too short ({word_count} words) — aim for 300–1000 words (−6 pts)"
    elif word_count > 3000:
        expl = f"CV is too long ({word_count} words) — keep under 3000 words (−6 pts)"
    else:
        expl = f"CV length is good ({word_count} words) ✓"
    return RuleFinding(
        rule="Appropriate Length",
        passed=passed,
        weight=6 if passed else -6,
        explanation=expl,
    )


def _check_email_present(text: str) -> RuleFinding:
    """Check for email address in CV."""
    found = bool(re.search(r"[\w.+-]+@[\w-]+\.[\w.-]+", text))
    return RuleFinding(
        rule="Email Address Present",
        passed=found,
        weight=5 if found else -5,
        explanation=(
            "Email address detected ✓" if found
            else "No email address found — critical for ATS contact parsing (−5 pts)"
        ),
    )


def _check_no_graphics_clues(text: str) -> RuleFinding:
    """Check for signs of non-ATS-safe elements in text extraction."""
    bad_signs = re.findall(r"(★|☆|●|◆|▪|🔹|📧|📱|💼|🎓|⭐|\[image\]|\[icon\])", text, re.IGNORECASE)
    passed = len(bad_signs) == 0
    return RuleFinding(
        rule="No Graphics/Icons",
        passed=passed,
        weight=4 if passed else -4,
        explanation=(
            "No emoji/icon markers detected ✓"
            if passed
            else f"Found {len(bad_signs)} graphic/icon markers — ATS may misparse (−4 pts)"
        ),
    )


def _check_keyword_match(text: str, job_description: Optional[str]) -> list[RuleFinding]:
    """If a job description is provided, check keyword overlap."""
    if not job_description:
        return []

    # Extract significant words (>3 chars) from JD
    jd_words = set(
        w.lower()
        for w in re.findall(r"\b[a-zA-Z]{4,}\b", job_description)
    )
    cv_words = set(
        w.lower()
        for w in re.findall(r"\b[a-zA-Z]{4,}\b", text)
    )

    if not jd_words:
        return []

    overlap = jd_words & cv_words
    ratio = len(overlap) / len(jd_words) * 100

    passed = ratio >= 40
    return [
        RuleFinding(
            rule="Job Description Keyword Match",
            passed=passed,
            weight=10 if passed else -10,
            explanation=(
                f"{ratio:.0f}% keyword overlap with job description ✓"
                if passed
                else f"Only {ratio:.0f}% keyword overlap — tailor CV to job description (−10 pts)"
            ),
        )
    ]


def compute_rule_based_score(
    cv_text: str,
    job_description: Optional[str] = None,
) -> RuleBasedScore:
    """
    Run all deterministic rules and return an explainable score.
    Base score starts at 50, rules add or subtract points, clamped to 0–100.
    """
    findings: list[RuleFinding] = []

    # Section checks
    findings.extend(_check_section_presence(cv_text, REQUIRED_SECTIONS, required=True))
    findings.extend(_check_section_presence(cv_text, OPTIONAL_SECTIONS, required=False))

    # Content quality checks
    findings.append(_check_bullet_points(cv_text))
    findings.append(_check_measurable_impacts(cv_text))
    findings.append(_check_length(cv_text))
    findings.append(_check_email_present(cv_text))
    findings.append(_check_no_graphics_clues(cv_text))

    # Job-target checks
    findings.extend(_check_keyword_match(cv_text, job_description))

    # Calculate score
    base = 50
    total_delta = sum(f.weight for f in findings)
    score = max(0, min(100, base + total_delta))

    return RuleBasedScore(score=score, findings=findings)

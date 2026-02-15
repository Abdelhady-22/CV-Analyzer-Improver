/* ── Score Card with animated gauge ── */

import { useEffect, useState } from 'react';
import type { ATSScore } from '../models/types';

interface ScoreCardProps {
    score: ATSScore;
}

function ScoreGauge({
    value,
    label,
    sublabel,
    color,
}: {
    value: number;
    label: string;
    sublabel?: string;
    color: string;
}) {
    const [animated, setAnimated] = useState(0);
    const circumference = 2 * Math.PI * 58;
    const offset = circumference - (animated / 100) * circumference;

    useEffect(() => {
        const timer = setTimeout(() => setAnimated(value), 200);
        return () => clearTimeout(timer);
    }, [value]);

    const getScoreColor = (val: number) => {
        if (val >= 80) return '#10b981';
        if (val >= 60) return '#f59e0b';
        if (val >= 40) return '#f97316';
        return '#ef4444';
    };

    return (
        <div className="score-gauge">
            <svg viewBox="0 0 140 140">
                <circle className="bg" cx="70" cy="70" r="58" />
                <circle
                    className="fg"
                    cx="70"
                    cy="70"
                    r="58"
                    stroke={color || getScoreColor(value)}
                    strokeDasharray={circumference}
                    strokeDashoffset={offset}
                />
            </svg>
            <div className="score-value">
                <span style={{ color: color || getScoreColor(value) }}>{Math.round(animated)}</span>
                <small>/100</small>
            </div>
        </div>
    );
}

function SubScoreBar({ label, value, color }: { label: string; value: number; color: string }) {
    return (
        <div className="sub-score-item">
            <div className="sub-score-label">
                {label}: {Math.round(value)}%
            </div>
            <div className="sub-score-bar">
                <div
                    className="sub-score-fill"
                    style={{ width: `${value}%`, background: color }}
                />
            </div>
        </div>
    );
}

export default function ScoreCard({ score }: ScoreCardProps) {
    return (
        <div className="score-cards-grid fade-in">
            {/* Overall Score */}
            <div className="glass-card score-card">
                <div className="score-label">Overall ATS Score</div>
                <ScoreGauge value={score.overall} label="Overall" color="" />
                <div className="score-sublabel">60% Rules + 40% AI</div>
            </div>

            {/* Rule-Based Score */}
            <div className="glass-card score-card">
                <div className="score-label">Rule-Based Score</div>
                <ScoreGauge value={score.rule_based.score} label="Rules" color="#06b6d4" />
                <div className="score-sublabel">
                    {score.rule_based.findings.filter((f) => f.passed).length}/
                    {score.rule_based.findings.length} rules passed
                </div>
                {/* Findings */}
                <div className="findings-list">
                    {score.rule_based.findings.map((f, i) => (
                        <div key={i} className="finding-row">
                            <div className={`finding-icon ${f.passed ? 'finding-pass' : 'finding-fail'}`}>
                                {f.passed ? '✓' : '✗'}
                            </div>
                            <span className="finding-text">{f.explanation}</span>
                            <span
                                className="finding-weight"
                                style={{ color: f.passed ? '#10b981' : '#ef4444' }}
                            >
                                {f.weight > 0 ? '+' : ''}{f.weight}
                            </span>
                        </div>
                    ))}
                </div>
            </div>

            {/* AI Score with sub-breakdowns */}
            <div className="glass-card score-card">
                <div className="score-label">AI Quality Score</div>
                <ScoreGauge value={score.llm_based.score} label="AI" color="#8b5cf6" />
                <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.75rem' }}>
                    {score.llm_based.summary}
                </p>
                <div className="sub-scores">
                    <SubScoreBar label="Keywords" value={score.llm_based.keyword_score} color="#3b82f6" />
                    <SubScoreBar label="Structure" value={score.llm_based.structure_score} color="#8b5cf6" />
                    <SubScoreBar label="Formatting" value={score.llm_based.formatting_score} color="#06b6d4" />
                    <SubScoreBar label="Parse Safety" value={score.llm_based.parsing_safety_score} color="#10b981" />
                </div>
            </div>
        </div>
    );
}

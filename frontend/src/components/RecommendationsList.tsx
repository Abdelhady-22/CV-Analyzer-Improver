/* ── Recommendations List Component ── */

import { useState } from 'react';
import type { Recommendation } from '../models/types';

interface RecommendationsListProps {
    recommendations: Recommendation[];
}

export default function RecommendationsList({ recommendations }: RecommendationsListProps) {
    const [expanded, setExpanded] = useState<number | null>(null);

    if (recommendations.length === 0) return null;

    return (
        <div className="fade-in">
            <h3 style={{ marginBottom: '1rem' }}>
                💡 Recommendations ({recommendations.length})
            </h3>
            <div className="glass-card" style={{ padding: 0, overflow: 'hidden' }}>
                {recommendations.map((rec, i) => (
                    <div
                        key={i}
                        className="rec-item"
                        onClick={() => setExpanded(expanded === i ? null : i)}
                    >
                        <div className="rec-header">
                            <span className={`rec-type rec-type-${rec.edit_type}`}>
                                {rec.edit_type}
                            </span>
                            <span className="rec-section">{rec.section}</span>
                            <span style={{ marginLeft: 'auto', fontSize: '0.85rem', opacity: 0.5 }}>
                                {expanded === i ? '▾' : '▸'}
                            </span>
                        </div>
                        <div className="rec-detail">{rec.rationale}</div>

                        {expanded === i && (
                            <div className="fade-in">
                                {rec.original_text && (
                                    <div className="rec-snippet rec-old">
                                        <strong>Before:</strong> {rec.original_text}
                                    </div>
                                )}
                                <div className="rec-snippet rec-new">
                                    <strong>After:</strong> {rec.suggested_text}
                                </div>
                            </div>
                        )}
                    </div>
                ))}
            </div>
        </div>
    );
}

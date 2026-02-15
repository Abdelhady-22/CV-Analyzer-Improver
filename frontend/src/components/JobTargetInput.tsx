/* ── Job Target Input (optional, collapsible) ── */

import { useState } from 'react';
import { useAnalysisStore } from '../store/analysisStore';

export default function JobTargetInput() {
    const [expanded, setExpanded] = useState(false);
    const { targetJobTitle, jobDescription, setJobTarget } = useAnalysisStore();

    return (
        <div className="job-target-section">
            <button
                className="job-target-toggle"
                onClick={() => setExpanded(!expanded)}
            >
                <span>{expanded ? '▾' : '▸'}</span>
                <span>🎯 Target a specific job (optional)</span>
            </button>

            {expanded && (
                <div className="job-target-fields fade-in">
                    <div className="form-group">
                        <label className="form-label">Target Job Title</label>
                        <input
                            type="text"
                            className="form-input"
                            placeholder="e.g. Senior Software Engineer"
                            value={targetJobTitle}
                            onChange={(e) => setJobTarget(e.target.value, jobDescription)}
                        />
                    </div>
                    <div className="form-group">
                        <label className="form-label">Job Description</label>
                        <textarea
                            className="form-textarea"
                            placeholder="Paste the job description here for keyword matching..."
                            value={jobDescription}
                            onChange={(e) => setJobTarget(targetJobTitle, e.target.value)}
                        />
                    </div>
                </div>
            )}
        </div>
    );
}

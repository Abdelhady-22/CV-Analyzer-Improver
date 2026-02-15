/* ── Pipeline Progress Component ── */

import type { AgentStep } from '../models/types';

interface PipelineProgressProps {
    steps: AgentStep[];
}

const STEP_LABELS: Record<string, string> = {
    infer: 'Infer',
    analyze: 'Analyze',
    score: 'Score',
    recommend: 'Recommend',
    rewrite: 'Rewrite',
};

const STEP_ICONS: Record<string, string> = {
    pending: '○',
    running: '◎',
    completed: '✓',
    failed: '✗',
};

export default function PipelineProgress({ steps }: PipelineProgressProps) {
    return (
        <div className="pipeline-progress">
            {steps.map((step) => (
                <div key={step.name} className="pipeline-step">
                    <div className={`pipeline-dot ${step.status}`}>
                        {step.status === 'running' ? (
                            <div className="spinner" style={{ width: 16, height: 16, borderWidth: 2 }} />
                        ) : (
                            STEP_ICONS[step.status]
                        )}
                    </div>
                    <span className="pipeline-label">
                        {STEP_LABELS[step.name] || step.name}
                    </span>
                </div>
            ))}
        </div>
    );
}

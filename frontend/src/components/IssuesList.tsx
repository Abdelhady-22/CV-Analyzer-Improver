/* ── Issues List Component ── */

import type { ATSIssue } from '../models/types';

interface IssuesListProps {
    issues: ATSIssue[];
}

export default function IssuesList({ issues }: IssuesListProps) {
    if (issues.length === 0) {
        return (
            <div className="glass-card" style={{ textAlign: 'center', padding: '2rem' }}>
                <span style={{ fontSize: '2rem' }}>🎉</span>
                <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem' }}>
                    No ATS issues found — your CV looks great!
                </p>
            </div>
        );
    }

    // Group by category
    const grouped = issues.reduce<Record<string, ATSIssue[]>>((acc, issue) => {
        const cat = issue.category || 'General';
        if (!acc[cat]) acc[cat] = [];
        acc[cat].push(issue);
        return acc;
    }, {});

    return (
        <div className="issues-section fade-in">
            <h3 style={{ marginBottom: '1rem' }}>
                🔍 ATS Issues ({issues.length})
            </h3>
            {Object.entries(grouped).map(([category, catIssues]) => (
                <div key={category} className="glass-card" style={{ marginBottom: '0.75rem' }}>
                    <h4
                        style={{
                            fontSize: '0.85rem',
                            textTransform: 'uppercase',
                            letterSpacing: '0.05em',
                            color: 'var(--text-muted)',
                            padding: '0.75rem 1rem 0',
                        }}
                    >
                        {category}
                    </h4>
                    {catIssues.map((issue, i) => (
                        <div key={i} className="issue-item">
                            <span className={`badge badge-${issue.severity}`}>{issue.severity}</span>
                            <span style={{ flex: 1, fontSize: '0.9rem', color: 'var(--text-secondary)' }}>
                                {issue.description}
                            </span>
                            {issue.location && (
                                <span className="issue-category">{issue.location}</span>
                            )}
                        </div>
                    ))}
                </div>
            ))}
        </div>
    );
}

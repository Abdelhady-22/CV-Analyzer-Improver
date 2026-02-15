/* ── Analysis Page ── */

import { useNavigate } from 'react-router-dom';
import { useAnalysisStore } from '../store/analysisStore';
import PipelineProgress from '../components/PipelineProgress';
import ATSWarningBanner from '../components/ATSWarningBanner';
import ScoreCard from '../components/ScoreCard';
import IssuesList from '../components/IssuesList';
import RecommendationsList from '../components/RecommendationsList';
import DiffViewer from '../components/DiffViewer';
import { getDownloadURL } from '../services/api';

export default function AnalysisPage() {
    const navigate = useNavigate();
    const {
        uploadResult,
        isAnalyzing,
        analysisResult,
        pipelineSteps,
        error,
    } = useAnalysisStore();

    // No upload yet
    if (!uploadResult && !analysisResult) {
        return (
            <div style={{ textAlign: 'center', padding: '4rem 0' }}>
                <h2 style={{ marginBottom: '1rem' }}>No CV uploaded yet</h2>
                <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                    Upload a CV first to see the analysis results.
                </p>
                <button className="btn btn-primary" onClick={() => navigate('/')}>
                    ← Upload a CV
                </button>
            </div>
        );
    }

    // Still analyzing
    if (isAnalyzing && !analysisResult) {
        return (
            <div className="fade-in">
                <div className="page-header">
                    <h1>Analyzing your CV...</h1>
                    <p>Our AI agents are reviewing your CV step by step.</p>
                </div>
                <div className="glass-card">
                    <PipelineProgress steps={pipelineSteps} />
                </div>
            </div>
        );
    }

    // Error state
    if (error) {
        return (
            <div style={{ textAlign: 'center', padding: '4rem 0' }}>
                <h2 style={{ color: 'var(--accent-red)' }}>Analysis Failed</h2>
                <p style={{ color: 'var(--text-secondary)', marginTop: '0.5rem', marginBottom: '2rem' }}>
                    {error}
                </p>
                <button className="btn btn-primary" onClick={() => navigate('/')}>
                    ← Try Again
                </button>
            </div>
        );
    }

    // Results ready
    if (!analysisResult) return null;

    const downloadReady = analysisResult.status === 'completed';

    return (
        <div className="fade-in">
            <div className="page-header">
                <h1>Analysis Results</h1>
                <p>
                    {uploadResult?.filename || 'Your CV'} — reviewed by 5 AI agents
                </p>
            </div>

            <ATSWarningBanner />

            {/* Inferred Profile */}
            {analysisResult.inferred_profile && (
                <div className="glass-card" style={{ marginBottom: '1.5rem' }}>
                    <h3 style={{ marginBottom: '0.75rem' }}>👤 Detected Profile</h3>
                    <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
                        <div>
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Industry</span>
                            <div style={{ fontWeight: 600 }}>{analysisResult.inferred_profile.industry}</div>
                        </div>
                        <div>
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Level</span>
                            <div style={{ fontWeight: 600 }}>{analysisResult.inferred_profile.role_level}</div>
                        </div>
                        <div>
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Experience</span>
                            <div style={{ fontWeight: 600 }}>{analysisResult.inferred_profile.years_experience} years</div>
                        </div>
                        <div>
                            <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Key Skills</span>
                            <div style={{ display: 'flex', gap: '0.35rem', flexWrap: 'wrap', marginTop: '0.25rem' }}>
                                {analysisResult.inferred_profile.key_skills.slice(0, 6).map((s, i) => (
                                    <span key={i} style={{ padding: '0.15rem 0.5rem', background: 'rgba(59,130,246,0.15)', borderRadius: '999px', fontSize: '0.75rem', color: 'var(--accent-blue)' }}>
                                        {s}
                                    </span>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            )}

            {/* Scores */}
            {analysisResult.score && <ScoreCard score={analysisResult.score} />}

            {/* Issues */}
            <IssuesList issues={analysisResult.issues} />

            {/* Recommendations */}
            <div style={{ marginTop: '1.5rem' }}>
                <RecommendationsList recommendations={analysisResult.recommendations} />
            </div>

            {/* Diff */}
            <div style={{ marginTop: '1.5rem' }}>
                <DiffViewer diff={analysisResult.diff} />
            </div>

            {/* Download */}
            <div style={{ marginTop: '2rem', paddingTop: '1.5rem', borderTop: '1px solid var(--border-color)' }}>
                <h3 style={{ marginBottom: '1rem' }}>📥 Download</h3>
                <div className="download-row">
                    <a
                        href={downloadReady && uploadResult ? getDownloadURL(uploadResult.upload_id) : '#'}
                        className={`btn btn-success ${!downloadReady ? 'btn-primary' : ''}`}
                        style={!downloadReady ? { opacity: 0.5, pointerEvents: 'none' } : {}}
                        download
                    >
                        ⬇ Download Improved CV
                    </a>
                    <button className="btn btn-secondary" onClick={() => navigate('/')}>
                        ↻ Upload Another CV
                    </button>
                    {!downloadReady && (
                        <span style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                            Download available after analysis completes
                        </span>
                    )}
                </div>
            </div>
        </div>
    );
}

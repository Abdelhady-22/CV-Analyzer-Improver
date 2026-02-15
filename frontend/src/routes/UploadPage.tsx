/* ── Upload Page ── */

import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import UploadZone from '../components/UploadZone';
import JobTargetInput from '../components/JobTargetInput';
import { useAnalysisStore } from '../store/analysisStore';
import { uploadCV, analyzeCV, pollAnalysisStatus, getAnalysisResult } from '../services/api';

export default function UploadPage() {
    const navigate = useNavigate();
    const [file, setFile] = useState<File | null>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const {
        setUploadResult,
        setAnalyzing,
        setPipelineSteps,
        setAnalysisResult,
        setError: setStoreError,
        cacheResult,
        targetJobTitle,
        jobDescription,
        uploadResult,
    } = useAnalysisStore();

    const handleFileSelect = async (selectedFile: File) => {
        setFile(selectedFile);
        setError(null);
        setIsUploading(true);

        try {
            const result = await uploadCV(selectedFile);
            setUploadResult(result);
            setIsUploading(false);
        } catch (err: any) {
            setError(err.message);
            setIsUploading(false);
        }
    };

    const handleAnalyze = async () => {
        if (!uploadResult) return;
        setAnalyzing(true);
        setStoreError(null);
        navigate('/analysis');

        try {
            await analyzeCV({
                upload_id: uploadResult.upload_id,
                target_job_title: targetJobTitle || undefined,
                job_description: jobDescription || undefined,
            });

            // Poll for progress
            const interval = setInterval(async () => {
                try {
                    const status = await pollAnalysisStatus(uploadResult.upload_id);
                    if (status.steps?.length) {
                        setPipelineSteps(status.steps);
                    }

                    if (status.overall_status === 'completed' || status.overall_status === 'failed') {
                        clearInterval(interval);
                        if (status.overall_status === 'completed') {
                            const result = await getAnalysisResult(uploadResult.upload_id);
                            setAnalysisResult(result);
                            cacheResult(uploadResult.upload_id, result);
                        } else {
                            setStoreError(status.error || 'Analysis failed');
                        }
                        setAnalyzing(false);
                    }
                } catch {
                    // Keep polling
                }
            }, 2000);
        } catch (err: any) {
            setStoreError(err.message);
            setAnalyzing(false);
        }
    };

    return (
        <div className="fade-in">
            <div className="hero">
                <h1>CV Analyzer & Improver</h1>
                <p>
                    Upload your CV and get instant ATS compliance analysis, actionable
                    recommendations, and an improved version — all powered by AI.
                </p>
                <div className="hero-features">
                    <div className="hero-feature">
                        <div className="hero-feature-icon">📊</div>
                        <span>ATS Scoring</span>
                    </div>
                    <div className="hero-feature">
                        <div className="hero-feature-icon">🔍</div>
                        <span>Issue Detection</span>
                    </div>
                    <div className="hero-feature">
                        <div className="hero-feature-icon">✨</div>
                        <span>AI Rewriting</span>
                    </div>
                    <div className="hero-feature">
                        <div className="hero-feature-icon">📄</div>
                        <span>DOCX Export</span>
                    </div>
                </div>
            </div>

            <UploadZone onFileSelect={handleFileSelect} isUploading={isUploading} selectedFile={file} />

            {error && (
                <div className="warning-banner" style={{ marginTop: '1rem', borderColor: 'rgba(239,68,68,0.3)', background: 'rgba(239,68,68,0.08)', color: '#ef4444' }}>
                    <span className="warning-banner-icon">❌</span>
                    <span>{error}</span>
                </div>
            )}

            {uploadResult && (
                <div className="glass-card fade-in" style={{ marginTop: '1.5rem' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                        <div>
                            <h3>📎 {uploadResult.filename}</h3>
                            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                                {uploadResult.page_count} page{uploadResult.page_count > 1 ? 's' : ''} detected
                            </p>
                        </div>
                        <button className="btn btn-primary" onClick={handleAnalyze}>
                            🚀 Analyze CV
                        </button>
                    </div>

                    <div
                        style={{
                            marginTop: '1rem',
                            padding: '1rem',
                            background: 'var(--bg-glass)',
                            borderRadius: 'var(--radius-sm)',
                            fontSize: '0.85rem',
                            color: 'var(--text-secondary)',
                            maxHeight: '150px',
                            overflow: 'hidden',
                            position: 'relative',
                        }}
                    >
                        {uploadResult.text_preview}
                        <div style={{
                            position: 'absolute',
                            bottom: 0,
                            left: 0,
                            right: 0,
                            height: '3rem',
                            background: 'linear-gradient(transparent, var(--bg-card))',
                        }} />
                    </div>

                    <JobTargetInput />
                </div>
            )}
        </div>
    );
}

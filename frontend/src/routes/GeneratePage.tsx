/* ── Generate CV Page ── */

import { useState } from 'react';
import CVForm from '../components/CVForm';
import type { StructuredCVData } from '../models/types';
import { generateCV, getGeneratedDownloadURL } from '../services/api';

export default function GeneratePage() {
    const [isGenerating, setIsGenerating] = useState(false);
    const [downloadUrl, setDownloadUrl] = useState<string | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [preview, setPreview] = useState<string | null>(null);

    const handleGenerate = async (data: StructuredCVData, industry: string, roleLevel: string) => {
        setIsGenerating(true);
        setError(null);
        setDownloadUrl(null);

        try {
            const result = await generateCV({
                cv_data: data,
                target_industry: industry,
                target_role_level: roleLevel,
            });

            setDownloadUrl(getGeneratedDownloadURL(result.download_id));
            setPreview(result.preview_text);
        } catch (err: any) {
            setError(err.message);
        } finally {
            setIsGenerating(false);
        }
    };

    return (
        <div className="fade-in">
            <div className="page-header">
                <h1>Generate New CV</h1>
                <p>
                    Build an ATS-optimized CV from scratch. Fill in your details and
                    we'll generate a professional DOCX file.
                </p>
            </div>

            {!downloadUrl ? (
                <CVForm onSubmit={handleGenerate} isGenerating={isGenerating} />
            ) : (
                <div className="glass-card fade-in" style={{ textAlign: 'center', padding: '2.5rem' }}>
                    <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🎉</div>
                    <h2 style={{ marginBottom: '0.5rem' }}>CV Generated Successfully!</h2>
                    <p style={{ color: 'var(--text-secondary)', marginBottom: '2rem' }}>
                        Your ATS-optimized CV is ready for download.
                    </p>

                    <div className="download-row" style={{ justifyContent: 'center' }}>
                        <a href={downloadUrl} className="btn btn-success" download>
                            ⬇ Download CV (DOCX)
                        </a>
                        <button
                            className="btn btn-secondary"
                            onClick={() => {
                                setDownloadUrl(null);
                                setPreview(null);
                            }}
                        >
                            ↻ Create Another
                        </button>
                    </div>

                    {preview && (
                        <div
                            style={{
                                marginTop: '2rem',
                                padding: '1rem',
                                background: 'var(--bg-glass)',
                                borderRadius: 'var(--radius-sm)',
                                fontSize: '0.85rem',
                                color: 'var(--text-secondary)',
                                textAlign: 'left',
                                maxHeight: '200px',
                                overflow: 'hidden',
                                position: 'relative',
                            }}
                        >
                            <h4 style={{ marginBottom: '0.5rem', fontSize: '0.85rem' }}>Preview</h4>
                            {preview}
                            <div style={{
                                position: 'absolute',
                                bottom: 0,
                                left: 0,
                                right: 0,
                                height: '3rem',
                                background: 'linear-gradient(transparent, var(--bg-card))',
                            }} />
                        </div>
                    )}
                </div>
            )}

            {error && (
                <div
                    className="warning-banner"
                    style={{
                        marginTop: '1rem',
                        borderColor: 'rgba(239,68,68,0.3)',
                        background: 'rgba(239,68,68,0.08)',
                        color: '#ef4444',
                    }}
                >
                    <span className="warning-banner-icon">❌</span>
                    <span>{error}</span>
                </div>
            )}
        </div>
    );
}

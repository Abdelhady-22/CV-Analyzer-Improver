/* ── API client service ── */

import type {
    CVUploadResponse,
    AnalysisRequest,
    AnalysisResponse,
    PipelineStatus,
    GenerateCVRequest,
    GenerateCVResponse,
} from '../models/types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

// ── Upload ────────────────────────────────────────────────────

export async function uploadCV(file: File): Promise<CVUploadResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const res = await fetch(`${API_URL}/api/upload`, {
        method: 'POST',
        body: formData,
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Upload failed' }));
        throw new Error(err.detail || 'Upload failed');
    }

    return res.json();
}

// ── Analysis ──────────────────────────────────────────────────

export async function analyzeCV(request: AnalysisRequest): Promise<{ upload_id: string; status: string; message: string }> {
    const res = await fetch(`${API_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Analysis failed' }));
        throw new Error(err.detail || 'Analysis failed');
    }

    return res.json();
}

export async function pollAnalysisStatus(uploadId: string): Promise<PipelineStatus> {
    const res = await fetch(`${API_URL}/api/analyze/status/${uploadId}`);
    if (!res.ok) throw new Error('Failed to fetch status');
    return res.json();
}

export async function getAnalysisResult(uploadId: string): Promise<AnalysisResponse> {
    const res = await fetch(`${API_URL}/api/analyze/result/${uploadId}`);
    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Result not ready' }));
        throw new Error(err.detail || 'Result not ready');
    }
    return res.json();
}

// ── Download ──────────────────────────────────────────────────

export function getDownloadURL(uploadId: string): string {
    return `${API_URL}/api/download/${uploadId}`;
}

export function getOriginalDownloadURL(uploadId: string): string {
    return `${API_URL}/api/download/original/${uploadId}`;
}

export function getGeneratedDownloadURL(downloadId: string): string {
    return `${API_URL}/api/generate/download/${downloadId}`;
}

// ── Generate ──────────────────────────────────────────────────

export async function generateCV(request: GenerateCVRequest): Promise<GenerateCVResponse> {
    const res = await fetch(`${API_URL}/api/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(request),
    });

    if (!res.ok) {
        const err = await res.json().catch(() => ({ detail: 'Generation failed' }));
        throw new Error(err.detail || 'Generation failed');
    }

    return res.json();
}

// ── Health ────────────────────────────────────────────────────

export async function checkHealth(): Promise<boolean> {
    try {
        const res = await fetch(`${API_URL}/health`);
        return res.ok;
    } catch {
        return false;
    }
}

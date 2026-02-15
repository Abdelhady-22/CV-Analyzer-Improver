/* ── Zustand store for the multi-step analysis flow ── */

import { create } from 'zustand';
import type {
    CVUploadResponse,
    AnalysisResponse,
    AgentStep,
} from '../models/types';

interface AnalysisStore {
    // Upload state
    uploadResult: CVUploadResponse | null;
    setUploadResult: (result: CVUploadResponse | null) => void;

    // Job target (optional)
    targetJobTitle: string;
    jobDescription: string;
    setJobTarget: (title: string, description: string) => void;

    // Analysis state
    isAnalyzing: boolean;
    analysisResult: AnalysisResponse | null;
    pipelineSteps: AgentStep[];
    error: string | null;
    setAnalyzing: (analyzing: boolean) => void;
    setAnalysisResult: (result: AnalysisResponse | null) => void;
    setPipelineSteps: (steps: AgentStep[]) => void;
    setError: (error: string | null) => void;

    // Cached results (keyed by upload_id)
    cachedResults: Record<string, AnalysisResponse>;
    cacheResult: (uploadId: string, result: AnalysisResponse) => void;
    getCachedResult: (uploadId: string) => AnalysisResponse | undefined;

    // Reset
    reset: () => void;
}

export const useAnalysisStore = create<AnalysisStore>((set, get) => ({
    // Upload state
    uploadResult: null,
    setUploadResult: (result) => set({ uploadResult: result }),

    // Job target
    targetJobTitle: '',
    jobDescription: '',
    setJobTarget: (title, description) =>
        set({ targetJobTitle: title, jobDescription: description }),

    // Analysis state
    isAnalyzing: false,
    analysisResult: null,
    pipelineSteps: [
        { name: 'infer', status: 'pending' },
        { name: 'analyze', status: 'pending' },
        { name: 'score', status: 'pending' },
        { name: 'recommend', status: 'pending' },
        { name: 'rewrite', status: 'pending' },
    ],
    error: null,
    setAnalyzing: (analyzing) => set({ isAnalyzing: analyzing }),
    setAnalysisResult: (result) => set({ analysisResult: result }),
    setPipelineSteps: (steps) => set({ pipelineSteps: steps }),
    setError: (error) => set({ error }),

    // Cached results
    cachedResults: {},
    cacheResult: (uploadId, result) =>
        set((state) => ({
            cachedResults: { ...state.cachedResults, [uploadId]: result },
        })),
    getCachedResult: (uploadId) => get().cachedResults[uploadId],

    // Reset
    reset: () =>
        set({
            uploadResult: null,
            targetJobTitle: '',
            jobDescription: '',
            isAnalyzing: false,
            analysisResult: null,
            pipelineSteps: [
                { name: 'infer', status: 'pending' },
                { name: 'analyze', status: 'pending' },
                { name: 'score', status: 'pending' },
                { name: 'recommend', status: 'pending' },
                { name: 'rewrite', status: 'pending' },
            ],
            error: null,
        }),
}));

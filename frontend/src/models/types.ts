/* ── TypeScript interfaces mirroring backend Pydantic models ── */

// ── CV Models ─────────────────────────────────────────────────

export interface ExperienceEntry {
    job_title: string;
    company: string;
    start_date: string;
    end_date: string;
    location?: string;
    bullets: string[];
}

export interface EducationEntry {
    degree: string;
    institution: string;
    start_date: string;
    end_date: string;
    gpa?: string;
    location?: string;
}

export interface CertificationEntry {
    name: string;
    issuer?: string;
    date?: string;
}

export interface StructuredCVData {
    full_name: string;
    email: string;
    phone?: string;
    location?: string;
    linkedin?: string;
    website?: string;
    summary: string;
    experience: ExperienceEntry[];
    education: EducationEntry[];
    skills: string[];
    certifications: CertificationEntry[];
    target_industry?: string;
    target_role_level?: string;
}

// ── Upload ────────────────────────────────────────────────────

export interface CVUploadResponse {
    upload_id: string;
    filename: string;
    text_preview: string;
    page_count: number;
}

// ── Analysis ──────────────────────────────────────────────────

export interface InferredProfile {
    industry: string;
    role_level: string;
    years_experience: number;
    key_skills: string[];
}

export interface RuleFinding {
    rule: string;
    passed: boolean;
    weight: number;
    explanation: string;
}

export interface RuleBasedScore {
    score: number;
    findings: RuleFinding[];
}

export interface LLMScore {
    score: number;
    keyword_score: number;
    structure_score: number;
    formatting_score: number;
    parsing_safety_score: number;
    summary: string;
}

export interface ATSScore {
    overall: number;
    rule_based: RuleBasedScore;
    llm_based: LLMScore;
}

export interface ATSIssue {
    severity: 'low' | 'medium' | 'high' | 'critical';
    category: string;
    description: string;
    location?: string;
}

export interface Recommendation {
    edit_type: 'add' | 'remove' | 'rewrite';
    section: string;
    original_text?: string;
    suggested_text: string;
    rationale: string;
}

export interface ParagraphEdit {
    section: string;
    paragraph_index: number;
    old_text: string;
    new_text: string;
}

export interface DiffChunk {
    type: 'add' | 'remove' | 'equal';
    text: string;
}

export interface AnalysisResponse {
    upload_id: string;
    status: string;
    inferred_profile?: InferredProfile;
    score?: ATSScore;
    issues: ATSIssue[];
    recommendations: Recommendation[];
    paragraph_edits: ParagraphEdit[];
    diff: DiffChunk[];
    original_text: string;
    improved_text: string;
}

// ── Pipeline Status ───────────────────────────────────────────

export interface AgentStep {
    name: string;
    status: 'pending' | 'running' | 'completed' | 'failed';
}

export interface PipelineStatus {
    upload_id: string;
    overall_status: string;
    steps: AgentStep[];
    error?: string;
}

// ── Generation ────────────────────────────────────────────────

export interface GenerateCVRequest {
    cv_data: StructuredCVData;
    target_industry: string;
    target_role_level: string;
}

export interface GenerateCVResponse {
    download_id: string;
    filename: string;
    preview_text: string;
}

// ── Analysis Request ──────────────────────────────────────────

export interface AnalysisRequest {
    upload_id: string;
    target_job_title?: string;
    job_description?: string;
}

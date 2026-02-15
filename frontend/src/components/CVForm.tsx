/* ── Multi-Step CV Generation Form ── */

import { useState } from 'react';
import type { StructuredCVData, ExperienceEntry, EducationEntry } from '../models/types';

interface CVFormProps {
    onSubmit: (data: StructuredCVData, industry: string, roleLevel: string) => void;
    isGenerating: boolean;
}

const STEPS = ['Contact', 'Summary', 'Experience', 'Education', 'Skills'];

function emptyExperience(): ExperienceEntry {
    return { job_title: '', company: '', start_date: '', end_date: '', location: '', bullets: [''] };
}

function emptyEducation(): EducationEntry {
    return { degree: '', institution: '', start_date: '', end_date: '', gpa: '', location: '' };
}

export default function CVForm({ onSubmit, isGenerating }: CVFormProps) {
    const [step, setStep] = useState(0);
    const [data, setData] = useState<StructuredCVData>({
        full_name: '',
        email: '',
        phone: '',
        location: '',
        linkedin: '',
        website: '',
        summary: '',
        experience: [emptyExperience()],
        education: [emptyEducation()],
        skills: [],
        certifications: [],
    });
    const [skillInput, setSkillInput] = useState('');
    const [industry, setIndustry] = useState('');
    const [roleLevel, setRoleLevel] = useState('');

    const updateField = (field: keyof StructuredCVData, value: any) => {
        setData((prev) => ({ ...prev, [field]: value }));
    };

    const handleSubmit = () => {
        onSubmit(data, industry, roleLevel);
    };

    const addSkill = () => {
        if (skillInput.trim()) {
            updateField('skills', [...data.skills, skillInput.trim()]);
            setSkillInput('');
        }
    };

    const removeSkill = (index: number) => {
        updateField('skills', data.skills.filter((_, i) => i !== index));
    };

    const addExperience = () => {
        updateField('experience', [...data.experience, emptyExperience()]);
    };

    const updateExperience = (index: number, field: keyof ExperienceEntry, value: any) => {
        const updated = [...data.experience];
        (updated[index] as any)[field] = value;
        updateField('experience', updated);
    };

    const removeExperience = (index: number) => {
        updateField('experience', data.experience.filter((_, i) => i !== index));
    };

    const addEducation = () => {
        updateField('education', [...data.education, emptyEducation()]);
    };

    const updateEducation = (index: number, field: keyof EducationEntry, value: any) => {
        const updated = [...data.education];
        (updated[index] as any)[field] = value;
        updateField('education', updated);
    };

    const removeEducation = (index: number) => {
        updateField('education', data.education.filter((_, i) => i !== index));
    };

    const updateBullet = (expIndex: number, bulletIndex: number, value: string) => {
        const updated = [...data.experience];
        updated[expIndex].bullets[bulletIndex] = value;
        updateField('experience', updated);
    };

    const addBullet = (expIndex: number) => {
        const updated = [...data.experience];
        updated[expIndex].bullets.push('');
        updateField('experience', updated);
    };

    const removeBullet = (expIndex: number, bulletIndex: number) => {
        const updated = [...data.experience];
        updated[expIndex].bullets = updated[expIndex].bullets.filter((_, i) => i !== bulletIndex);
        updateField('experience', updated);
    };

    return (
        <div className="glass-card fade-in">
            {/* Step indicators */}
            <div className="form-steps">
                {STEPS.map((_, i) => (
                    <div
                        key={i}
                        className={`form-step-indicator ${i === step ? 'active' : i < step ? 'completed' : ''}`}
                    />
                ))}
            </div>

            <h3 style={{ marginBottom: '1.5rem' }}>{STEPS[step]}</h3>

            {/* Step 0: Contact */}
            {step === 0 && (
                <div>
                    <div className="form-row">
                        <div className="form-group">
                            <label className="form-label">Full Name *</label>
                            <input type="text" className="form-input" value={data.full_name}
                                onChange={(e) => updateField('full_name', e.target.value)} placeholder="John Doe" />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Email *</label>
                            <input type="email" className="form-input" value={data.email}
                                onChange={(e) => updateField('email', e.target.value)} placeholder="john@example.com" />
                        </div>
                    </div>
                    <div className="form-row" style={{ marginTop: '0.75rem' }}>
                        <div className="form-group">
                            <label className="form-label">Phone</label>
                            <input type="tel" className="form-input" value={data.phone || ''}
                                onChange={(e) => updateField('phone', e.target.value)} placeholder="+1 (555) 123-4567" />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Location</label>
                            <input type="text" className="form-input" value={data.location || ''}
                                onChange={(e) => updateField('location', e.target.value)} placeholder="New York, NY" />
                        </div>
                    </div>
                    <div className="form-row" style={{ marginTop: '0.75rem' }}>
                        <div className="form-group">
                            <label className="form-label">LinkedIn</label>
                            <input type="url" className="form-input" value={data.linkedin || ''}
                                onChange={(e) => updateField('linkedin', e.target.value)} placeholder="linkedin.com/in/johndoe" />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Website</label>
                            <input type="url" className="form-input" value={data.website || ''}
                                onChange={(e) => updateField('website', e.target.value)} placeholder="johndoe.com" />
                        </div>
                    </div>
                    <div className="form-row" style={{ marginTop: '0.75rem' }}>
                        <div className="form-group">
                            <label className="form-label">Target Industry</label>
                            <input type="text" className="form-input" value={industry}
                                onChange={(e) => setIndustry(e.target.value)} placeholder="e.g. Software Engineering" />
                        </div>
                        <div className="form-group">
                            <label className="form-label">Target Role Level</label>
                            <select className="form-input" value={roleLevel} onChange={(e) => setRoleLevel(e.target.value)}>
                                <option value="">Select...</option>
                                <option value="Junior">Junior</option>
                                <option value="Mid-level">Mid-level</option>
                                <option value="Senior">Senior</option>
                                <option value="Lead">Lead</option>
                                <option value="Executive">Executive</option>
                            </select>
                        </div>
                    </div>
                </div>
            )}

            {/* Step 1: Summary */}
            {step === 1 && (
                <div className="form-group">
                    <label className="form-label">Professional Summary</label>
                    <textarea
                        className="form-textarea"
                        style={{ minHeight: '150px' }}
                        value={data.summary}
                        onChange={(e) => updateField('summary', e.target.value)}
                        placeholder="Experienced software engineer with 5+ years..."
                    />
                </div>
            )}

            {/* Step 2: Experience */}
            {step === 2 && (
                <div>
                    {data.experience.map((exp, ei) => (
                        <div key={ei} className="dynamic-list-item" style={{ flexDirection: 'column', alignItems: 'stretch' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <strong style={{ fontSize: '0.9rem', color: 'var(--accent-blue)' }}>
                                    Position {ei + 1}
                                </strong>
                                {data.experience.length > 1 && (
                                    <button className="remove-btn" onClick={() => removeExperience(ei)} style={{ marginTop: 0 }}>×</button>
                                )}
                            </div>
                            <div className="form-row" style={{ marginTop: '0.5rem' }}>
                                <div className="form-group">
                                    <label className="form-label">Job Title</label>
                                    <input type="text" className="form-input" value={exp.job_title}
                                        onChange={(e) => updateExperience(ei, 'job_title', e.target.value)} />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Company</label>
                                    <input type="text" className="form-input" value={exp.company}
                                        onChange={(e) => updateExperience(ei, 'company', e.target.value)} />
                                </div>
                            </div>
                            <div className="form-row" style={{ marginTop: '0.5rem' }}>
                                <div className="form-group">
                                    <label className="form-label">Start Date</label>
                                    <input type="text" className="form-input" value={exp.start_date}
                                        onChange={(e) => updateExperience(ei, 'start_date', e.target.value)} placeholder="Jan 2020" />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">End Date</label>
                                    <input type="text" className="form-input" value={exp.end_date}
                                        onChange={(e) => updateExperience(ei, 'end_date', e.target.value)} placeholder="Present" />
                                </div>
                            </div>
                            <div style={{ marginTop: '0.5rem' }}>
                                <label className="form-label">Achievements (bullet points)</label>
                                {exp.bullets.map((b, bi) => (
                                    <div key={bi} style={{ display: 'flex', gap: '0.5rem', marginTop: '0.35rem' }}>
                                        <input type="text" className="form-input" style={{ flex: 1 }} value={b}
                                            onChange={(e) => updateBullet(ei, bi, e.target.value)}
                                            placeholder="Achieved X by doing Y, resulting in Z" />
                                        {exp.bullets.length > 1 && (
                                            <button className="remove-btn" onClick={() => removeBullet(ei, bi)} style={{ marginTop: 0 }}>×</button>
                                        )}
                                    </div>
                                ))}
                                <button className="add-item-btn" style={{ marginTop: '0.5rem' }} onClick={() => addBullet(ei)}>
                                    + Add bullet
                                </button>
                            </div>
                        </div>
                    ))}
                    <button className="add-item-btn" onClick={addExperience}>+ Add experience</button>
                </div>
            )}

            {/* Step 3: Education */}
            {step === 3 && (
                <div>
                    {data.education.map((edu, ei) => (
                        <div key={ei} className="dynamic-list-item" style={{ flexDirection: 'column', alignItems: 'stretch' }}>
                            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                                <strong style={{ fontSize: '0.9rem', color: 'var(--accent-blue)' }}>Education {ei + 1}</strong>
                                {data.education.length > 1 && (
                                    <button className="remove-btn" onClick={() => removeEducation(ei)} style={{ marginTop: 0 }}>×</button>
                                )}
                            </div>
                            <div className="form-row" style={{ marginTop: '0.5rem' }}>
                                <div className="form-group">
                                    <label className="form-label">Degree</label>
                                    <input type="text" className="form-input" value={edu.degree}
                                        onChange={(e) => updateEducation(ei, 'degree', e.target.value)} placeholder="B.Sc. Computer Science" />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">Institution</label>
                                    <input type="text" className="form-input" value={edu.institution}
                                        onChange={(e) => updateEducation(ei, 'institution', e.target.value)} />
                                </div>
                            </div>
                            <div className="form-row" style={{ marginTop: '0.5rem' }}>
                                <div className="form-group">
                                    <label className="form-label">Start Date</label>
                                    <input type="text" className="form-input" value={edu.start_date}
                                        onChange={(e) => updateEducation(ei, 'start_date', e.target.value)} placeholder="Sep 2016" />
                                </div>
                                <div className="form-group">
                                    <label className="form-label">End Date</label>
                                    <input type="text" className="form-input" value={edu.end_date}
                                        onChange={(e) => updateEducation(ei, 'end_date', e.target.value)} placeholder="Jun 2020" />
                                </div>
                            </div>
                        </div>
                    ))}
                    <button className="add-item-btn" onClick={addEducation}>+ Add education</button>
                </div>
            )}

            {/* Step 4: Skills */}
            {step === 4 && (
                <div>
                    <div className="form-group">
                        <label className="form-label">Add Skills</label>
                        <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <input
                                type="text"
                                className="form-input"
                                style={{ flex: 1 }}
                                value={skillInput}
                                onChange={(e) => setSkillInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), addSkill())}
                                placeholder="Type a skill and press Enter"
                            />
                            <button className="btn btn-secondary" onClick={addSkill}>Add</button>
                        </div>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.5rem', marginTop: '1rem' }}>
                        {data.skills.map((skill, i) => (
                            <span
                                key={i}
                                style={{
                                    padding: '0.35rem 0.75rem',
                                    background: 'rgba(59, 130, 246, 0.15)',
                                    borderRadius: '999px',
                                    fontSize: '0.85rem',
                                    color: 'var(--accent-blue)',
                                    display: 'flex',
                                    alignItems: 'center',
                                    gap: '0.4rem',
                                }}
                            >
                                {skill}
                                <span
                                    onClick={() => removeSkill(i)}
                                    style={{ cursor: 'pointer', fontSize: '0.75rem', opacity: 0.7 }}
                                >
                                    ✕
                                </span>
                            </span>
                        ))}
                    </div>
                </div>
            )}

            {/* Navigation */}
            <div className="form-actions">
                <button
                    className="btn btn-secondary"
                    onClick={() => setStep(Math.max(0, step - 1))}
                    disabled={step === 0}
                >
                    ← Previous
                </button>
                {step < STEPS.length - 1 ? (
                    <button className="btn btn-primary" onClick={() => setStep(step + 1)}>
                        Next →
                    </button>
                ) : (
                    <button
                        className="btn btn-success"
                        onClick={handleSubmit}
                        disabled={isGenerating || !data.full_name || !data.email}
                    >
                        {isGenerating ? (
                            <>
                                <div className="spinner" style={{ width: 16, height: 16 }} />
                                Generating...
                            </>
                        ) : (
                            '🚀 Generate CV'
                        )}
                    </button>
                )}
            </div>
        </div>
    );
}

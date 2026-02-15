/* ── Upload Zone Component ── */

import { useCallback, useRef, useState } from 'react';

interface UploadZoneProps {
    onFileSelect: (file: File) => void;
    isUploading: boolean;
    selectedFile: File | null;
}

export default function UploadZone({ onFileSelect, isUploading, selectedFile }: UploadZoneProps) {
    const [dragOver, setDragOver] = useState(false);
    const inputRef = useRef<HTMLInputElement>(null);

    const handleDrop = useCallback(
        (e: React.DragEvent) => {
            e.preventDefault();
            setDragOver(false);
            const file = e.dataTransfer.files[0];
            if (file && isValidFile(file)) onFileSelect(file);
        },
        [onFileSelect]
    );

    const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file && isValidFile(file)) onFileSelect(file);
    };

    const isValidFile = (file: File) => {
        const ext = file.name.split('.').pop()?.toLowerCase();
        return ['pdf', 'docx', 'doc'].includes(ext || '');
    };

    return (
        <div
            className={`upload-zone ${dragOver ? 'drag-over' : ''}`}
            onClick={() => inputRef.current?.click()}
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
        >
            <input
                ref={inputRef}
                type="file"
                accept=".pdf,.docx,.doc"
                onChange={handleChange}
                style={{ display: 'none' }}
            />

            <div className="upload-zone-icon">
                {isUploading ? (
                    <div className="spinner" />
                ) : (
                    <span>📄</span>
                )}
            </div>

            <h3>{isUploading ? 'Uploading...' : 'Drop your CV here'}</h3>
            <p>or click to browse — PDF, DOCX accepted (max 10MB)</p>

            {selectedFile && !isUploading && (
                <div className="upload-zone-file">
                    📎 {selectedFile.name}
                </div>
            )}
        </div>
    );
}

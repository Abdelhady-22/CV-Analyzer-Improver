/* ── Diff Viewer Component ── */

import type { DiffChunk } from '../models/types';

interface DiffViewerProps {
    diff: DiffChunk[];
}

export default function DiffViewer({ diff }: DiffViewerProps) {
    if (diff.length === 0) return null;

    return (
        <div className="fade-in">
            <h3 style={{ marginBottom: '1rem' }}>📝 Before vs After</h3>
            <div className="glass-card diff-viewer">
                {diff.map((chunk, i) => {
                    if (chunk.type === 'equal') {
                        return <span key={i}>{chunk.text}</span>;
                    }
                    return (
                        <span
                            key={i}
                            className={chunk.type === 'add' ? 'diff-add' : 'diff-remove'}
                        >
                            {chunk.text}
                        </span>
                    );
                })}
            </div>
        </div>
    );
}

"""
Diff service — computes line-level text diffs for the frontend viewer.
"""

from __future__ import annotations

from diff_match_patch import diff_match_patch

from models.analysis import DiffChunk


def compute_diff(before: str, after: str) -> list[DiffChunk]:
    """
    Compute line-level diff between two texts.
    Returns a list of DiffChunks suitable for the frontend diff viewer.
    """
    dmp = diff_match_patch()
    diffs = dmp.diff_main(before, after)
    dmp.diff_cleanupSemantic(diffs)

    chunks: list[DiffChunk] = []
    type_map = {-1: "remove", 0: "equal", 1: "add"}

    for op, text in diffs:
        if text.strip():  # Skip pure whitespace diffs
            chunks.append(DiffChunk(type=type_map[op], text=text))

    return chunks

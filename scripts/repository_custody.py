"""Read exact historical inputs without confusing them with the worktree."""

from __future__ import annotations

import hashlib
from pathlib import Path, PurePosixPath
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def historical_bytes(commit: str, path: str, *, root: Path = ROOT) -> bytes:
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("historical custody requires a full lowercase commit SHA")
    relative = PurePosixPath(path)
    if relative.is_absolute() or ".." in relative.parts or not relative.parts:
        raise ValueError(f"invalid historical custody path: {path}")
    result = subprocess.run(
        ["git", "show", f"{commit}:{relative.as_posix()}"], cwd=root,
        capture_output=True, timeout=30,
    )
    if result.returncode:
        raise ValueError(
            f"historical input unavailable: {commit}:{path}; "
            "restore complete Git history rather than substituting HEAD bytes"
        )
    return result.stdout


def historical_sha256(commit: str, path: str, *, root: Path = ROOT) -> str:
    return hashlib.sha256(historical_bytes(commit, path, root=root)).hexdigest()

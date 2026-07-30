#!/usr/bin/env python3
"""Canonical manuscript binding for the governed visual edition.

The YouTube player and descriptive transcript are a generated publication
projection.  They must not change the digest that decides whether the source
chapter has become stale, otherwise inserting a current embed would make that
same video stale immediately.
"""

from __future__ import annotations

import hashlib
import re
from pathlib import Path


MANAGED_BLOCK = re.compile(
    r"\n?<!-- BEGIN MANAGED VISUAL ABSTRACT:(?P<chapter_id>[a-z0-9-]+) -->"
    r".*?"
    r"<!-- END MANAGED VISUAL ABSTRACT:(?P=chapter_id) -->\n?",
    re.DOTALL,
)


def canonicalize_chapter_source(source: str, *, label: str = "chapter") -> str:
    """Return source text with its generated visual block removed."""
    blocks = list(MANAGED_BLOCK.finditer(source))
    if len(blocks) > 1:
        raise ValueError(f"{label} contains multiple managed visual blocks")
    if not blocks:
        return source
    match = blocks[0]
    before = source[: match.start()]
    after = source[match.end() :]
    # The synchronizer inserts one blank line around the managed block. Restore
    # the pre-insertion front-matter/body join exactly.
    if before.endswith("\n---\n") and after.startswith("#"):
        return before + "\n" + after
    return before + after


def canonical_chapter_text(path: Path) -> str:
    """Return chapter source with the generated visual block removed."""
    return canonicalize_chapter_source(
        path.read_text(encoding="utf-8"),
        label=str(path),
    )


def canonical_chapter_sha256(path: Path) -> str:
    return hashlib.sha256(canonical_chapter_text(path).encode("utf-8")).hexdigest()

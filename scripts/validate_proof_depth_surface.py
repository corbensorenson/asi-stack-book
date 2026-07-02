#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "docs" / "proof_depth_classification.md"
CHAPTER = ROOT / "chapters" / "executable-specifications-and-lean-proof-envelope.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "executable-specifications-and-lean-proof-envelope.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"

CODEX_TEST_NAME = "Proof-depth surface synchronization"
COMMAND = "python3 scripts/validate_proof_depth_surface.py"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Proof-depth surface validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def metric(name: str) -> str:
    text = REPORT.read_text(encoding="utf-8")
    match = re.search(rf"^\|\s*{re.escape(name)}\s*\|\s*([^|]+?)\s*\|$", text, re.MULTILINE)
    if not match:
        raise ValueError(f"Missing metric {name!r} in {rel(REPORT)}.")
    return match.group(1).strip()


def proof_depth_fragment() -> str:
    return (
        "Current proof-depth snapshot: "
        f"{metric('Proof targets in manifest')} proof targets, "
        f"{metric('Lean modules scanned')} Lean modules, "
        f"{metric('Theorem declarations classified')} theorem declarations, "
        f"{metric('Derived/decomposed theorem declarations')} derived/decomposed, "
        f"{metric('Direct/projection-style theorem declarations')} direct/projection, "
        f"{metric('Unknown or mixed theorem declarations')} unknown/mixed, and "
        f"{metric('Safety-critical chapter classifications present')} safety-critical chapter classifications present."
    )


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def validate_manifest(fragment: str, errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "executable-specifications-and-lean-proof-envelope":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing proof-envelope chapter.")
        return
    codex_blob = text_blob(chapter.get("codex_tests", []))
    if CODEX_TEST_NAME.lower() not in codex_blob:
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    if "proof-depth" not in codex_blob or "direct/projection" not in codex_blob:
        errors.append("book_structure.json: proof-depth Codex test must name direct/projection boundary.")


def validate_surface(path: Path, phrases: list[str], errors: list[str]) -> None:
    if not path.exists():
        errors.append(f"Missing {rel(path)}.")
        return
    lowered = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore")).lower()
    for phrase in phrases:
        normalized_phrase = re.sub(r"\s+", " ", phrase).lower()
        if normalized_phrase not in lowered:
            errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    errors: list[str] = []
    try:
        fragment = proof_depth_fragment()
    except ValueError as exc:
        fail([str(exc)])

    validate_manifest(fragment, errors)
    shared = [
        fragment,
        "derived/decomposed",
        "direct/projection",
        "projection-only traceability",
        "does not prove semantic adequacy",
    ]
    validate_surface(CHAPTER, shared, errors)
    validate_surface(
        READER,
        [
            fragment,
            "derived/decomposed",
            "direct/projection",
            "proof etiquette",
            "not a proof of semantic adequacy",
        ],
        errors,
    )
    validate_surface(
        OUTLINE,
        [
            CODEX_TEST_NAME,
            fragment,
            "proof-depth classification",
        ],
        errors,
    )
    validate_surface(
        ROADMAP,
        [
            "Proof-depth surface synchronization",
            fragment,
            "does not promote proof-envelope support",
        ],
        errors,
    )
    validate_surface(
        CHANGELOG,
        [
            "Proof-depth surface synchronization",
            fragment,
        ],
        errors,
    )
    validate_surface(
        VALIDATE_BOOK,
        [
            "scripts/validate_proof_depth_surface.py",
            'run_validator("validate_proof_depth_surface.py")',
        ],
        errors,
    )
    if errors:
        fail(errors)
    print("Proof-depth surface validation passed.")


if __name__ == "__main__":
    main()

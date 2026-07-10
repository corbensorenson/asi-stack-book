#!/usr/bin/env python3
from __future__ import annotations

import argparse
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
READER_MANIFEST = ROOT / "editions" / "reader_manuscript" / "v1_0" / "manifest.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"

CODEX_TEST_NAME = "Proof-depth surface synchronization"
COMMAND = "python3 scripts/validate_proof_depth_surface.py"
SNAPSHOT_RE = re.compile(
    r"Current proof-depth snapshot:\s*\d+\s+proof targets,\s*\d+\s+Lean modules,\s*"
    r"\d+\s+theorem declarations,\s*\d+\s+derived/decomposed,\s*"
    r"\d+\s+direct/projection,\s*\d+\s+unknown/mixed,\s+and\s+"
    r"\d+/\d+\s+safety-critical chapter classifications present\."
)


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


def active_spine_differs_from_reader_snapshot() -> bool:
    reader_manifest = load_json(READER_MANIFEST)
    structure = load_json(MANIFEST)
    if not isinstance(reader_manifest, dict) or not isinstance(structure, dict):
        return False
    snapshot = reader_manifest.get("historical_spine_snapshot")
    snapshot_ids = snapshot.get("chapter_ids") if isinstance(snapshot, dict) else None
    if not isinstance(snapshot_ids, list):
        return False
    active_ids = [
        str(chapter.get("id", ""))
        for part in structure.get("parts", [])
        if isinstance(part, dict)
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]
    return active_ids != snapshot_ids


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


def write_current_snapshot(path: Path, fragment: str) -> None:
    text = path.read_text(encoding="utf-8")
    updated, count = SNAPSHOT_RE.subn(fragment, text, count=1)
    if count != 1:
        raise ValueError(f"{rel(path)}: expected one current proof-depth snapshot, found {count}.")
    path.write_text(updated, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--write",
        action="store_true",
        help="refresh the current proof-depth snapshot on validator-owned public surfaces",
    )
    args = parser.parse_args()
    errors: list[str] = []
    try:
        fragment = proof_depth_fragment()
    except ValueError as exc:
        fail([str(exc)])

    if args.write:
        try:
            for path in (CHAPTER, OUTLINE, ROADMAP, CHANGELOG):
                write_current_snapshot(path, fragment)
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
    if not active_spine_differs_from_reader_snapshot():
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
        VALIDATION_REGISTRY,
        [
            "scripts/validate_proof_depth_surface.py",
            '"script": "validate_proof_depth_surface.py"',
        ],
        errors,
    )
    if errors:
        fail(errors)
    print("Proof-depth surface validation passed.")


if __name__ == "__main__":
    main()

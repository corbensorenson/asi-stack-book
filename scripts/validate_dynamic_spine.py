#!/usr/bin/env python3
"""Prove that the active book spine can grow and return without manual renumbering.

The historical v1.0 reader/release records intentionally retain their recorded
44-chapter snapshot. This validator exercises both boundaries in a disposable
workspace: it inserts a cloned fixture chapter, regenerates the live scaffold,
checks the active reader derivation and frozen-reader validation, confirms that
the historical candidate refuses a mixed-spine render, removes the fixture,
and verifies that generated active surfaces return to their original bytes.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
FIXTURE_ID = "dynamic-spine-fixture"
FIXTURE_TITLE = "Dynamic Spine Fixture"
FIXTURE_FILE = Path("chapters") / f"{FIXTURE_ID}.qmd"
DISPOSITIONS = Path("claim_decisions") / "v1_x_core_claim_dispositions.json"
GENERATED_PATHS = (
    Path("_quarto.yml"),
    Path("appendices/A_source_matrix.qmd"),
    Path("appendices/C_claim_evidence_matrix.qmd"),
    Path("appendices/E_codex_test_specs.qmd"),
    Path("appendices/G_corben_source_corpus.qmd"),
    Path("appendices/H_external_sources.qmd"),
    Path("appendices/K_implementation_horizons.qmd"),
)
IGNORED_COPY_NAMES = (
    ".git",
    ".quarto",
    "_site",
    "build",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".DS_Store",
    ".lake",
    "raw",
)


def fail(message: str) -> None:
    print(f"Dynamic spine validation failed: {message}")
    sys.exit(1)


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path.name} must contain an object")
    return value


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        chapter
        for part in structure.get("parts", [])
        if isinstance(part, dict)
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]


def run(workspace: Path, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, *args],
        cwd=workspace,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"{' '.join(args)} exited {result.returncode}:\n{result.stdout.strip()}"
        )
    return result.stdout


def snapshot(workspace: Path) -> dict[Path, str]:
    result: dict[Path, str] = {}
    for relative in GENERATED_PATHS:
        path = workspace / relative
        if not path.exists():
            raise FileNotFoundError(f"generated path is missing: {relative}")
        result[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return result


def insert_fixture(workspace: Path) -> int:
    structure_path = workspace / "book_structure.json"
    structure = load_json(structure_path)
    parts = structure.get("parts")
    if not isinstance(parts, list) or not parts or not isinstance(parts[0], dict):
        raise TypeError("book_structure.json must contain a first part with chapters")
    chapters = parts[0].get("chapters")
    if not isinstance(chapters, list) or not chapters or not isinstance(chapters[0], dict):
        raise TypeError("the first part must contain a source chapter for the fixture")
    if any(chapter.get("id") == FIXTURE_ID for chapter in flatten_chapters(structure)):
        raise ValueError(f"fixture id {FIXTURE_ID!r} already exists in the manifest")

    template = chapters[0]
    fixture = copy.deepcopy(template)
    fixture["id"] = FIXTURE_ID
    fixture["title"] = FIXTURE_TITLE
    fixture["file"] = str(FIXTURE_FILE)
    fixture["core_claim"] = (
        "A manifest-derived fixture chapter can enter and leave a disposable "
        "workspace without manual chapter-number or active-count edits."
    )
    fixture["problem"] = "Fixture-only dynamic-spine regression coverage."
    fixture["insufficient"] = "Static counts would break insertion and removal workflows."
    fixture["minimal_implementation"] = (
        "Add one manifest entry and derive navigation, source, claim, and reader surfaces."
    )
    fixture["beyond_state_of_art"] = (
        "All active surfaces derive chapter identity and count from the manifest while "
        "historical release snapshots remain version-scoped."
    )
    chapters.insert(1, fixture)
    structure_path.write_text(json.dumps(structure, indent=2) + "\n", encoding="utf-8")

    source_path = workspace / str(template["file"])
    fixture_path = workspace / FIXTURE_FILE
    fixture_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source_path, fixture_path)
    add_fixture_disposition(workspace, template, fixture)
    return len(flatten_chapters(structure))


def add_fixture_disposition(
    workspace: Path, template: dict[str, Any], fixture: dict[str, Any]
) -> None:
    """Clone the companion core-claim record for the disposable spine fixture."""
    path = workspace / DISPOSITIONS
    data = load_json(path)
    dispositions = data.get("dispositions")
    if not isinstance(dispositions, list):
        raise TypeError("core-claim disposition set must contain dispositions")
    source = next(
        (
            record
            for record in dispositions
            if isinstance(record, dict) and record.get("chapter_id") == template["id"]
        ),
        None,
    )
    if not isinstance(source, dict):
        raise ValueError("dynamic-spine fixture source chapter lacks a disposition record")

    record = copy.deepcopy(source)
    record.update(
        {
            "claim_id": f"{FIXTURE_ID}.core",
            "chapter_id": FIXTURE_ID,
            "chapter_title": FIXTURE_TITLE,
            "chapter_file": str(FIXTURE_FILE),
            "core_claim": fixture["core_claim"],
            "current_evidence_summary": (
                "Disposable dynamic-spine fixture only; this record exists to exercise "
                "manifest-derived claim bookkeeping and makes no support-state claim."
            ),
        }
    )
    dispositions.append(record)
    summary = data.get("summary")
    if not isinstance(summary, dict):
        raise TypeError("core-claim disposition set must contain a summary")
    summary["manifest_chapter_core_claims"] = len(dispositions)
    summary["chapter_core_claims_remaining_at_argument"] = len(dispositions)
    if record.get("coverage_type") == "accepted_core_transition":
        summary["accepted_core_transition_dispositions"] = int(
            summary.get("accepted_core_transition_dispositions", 0)
        ) + 1
    else:
        summary["accepted_no_promotion_dispositions"] = int(
            summary.get("accepted_no_promotion_dispositions", 0)) + 1
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def assert_fixture_surfaces(workspace: Path, expected_chapter_count: int) -> None:
    structure = load_json(workspace / "book_structure.json")
    chapters = flatten_chapters(structure)
    if len(chapters) != expected_chapter_count:
        raise AssertionError(
            f"fixture manifest has {len(chapters)} chapters; expected {expected_chapter_count}"
        )
    fixture = next((chapter for chapter in chapters if chapter.get("id") == FIXTURE_ID), None)
    if fixture is None or fixture.get("file") != str(FIXTURE_FILE):
        raise AssertionError("fixture chapter is absent or has the wrong file path")

    required_text = {
        Path("_quarto.yml"): str(FIXTURE_FILE),
        Path("appendices/C_claim_evidence_matrix.qmd"): fixture["core_claim"],
        Path("appendices/K_implementation_horizons.qmd"): FIXTURE_TITLE,
    }
    for relative, required in required_text.items():
        text = (workspace / relative).read_text(encoding="utf-8", errors="ignore")
        if required not in text:
            raise AssertionError(f"{relative} did not derive fixture content {required!r}")


def main() -> None:
    try:
        with tempfile.TemporaryDirectory(prefix="asi-stack-dynamic-spine-") as temp_dir:
            workspace = Path(temp_dir) / "workspace"
            shutil.copytree(
                ROOT,
                workspace,
                ignore=shutil.ignore_patterns(*IGNORED_COPY_NAMES),
            )
            run(workspace, "scripts/sync_scaffold.py")
            baseline = snapshot(workspace)
            original_manifest = (workspace / "book_structure.json").read_bytes()
            original_dispositions = (workspace / DISPOSITIONS).read_bytes()
            original_count = len(flatten_chapters(load_json(workspace / "book_structure.json")))

            fixture_count = insert_fixture(workspace)
            if fixture_count != original_count + 1:
                raise AssertionError(
                    f"fixture insertion produced {fixture_count} chapters; expected {original_count + 1}"
                )
            run(workspace, "scripts/sync_scaffold.py")
            assert_fixture_surfaces(workspace, fixture_count)
            run(workspace, "scripts/build_reader_edition.py", "--check")
            run(workspace, "scripts/validate_reader_manuscript_manifest.py")
            run(workspace, "scripts/sync_reader_chapter_review_matrix.py", "--check")
            run(workspace, "scripts/validate_reader_chapter_reconciliation_approval.py")
            historical_check = run(workspace, "scripts/build_curated_reader_edition.py", "--check")
            if "frozen chapters remain valid" not in historical_check:
                raise AssertionError(
                    "historical reader check did not preserve the frozen snapshot after active insertion"
                )

            (workspace / "book_structure.json").write_bytes(original_manifest)
            (workspace / DISPOSITIONS).write_bytes(original_dispositions)
            (workspace / FIXTURE_FILE).unlink()
            run(workspace, "scripts/sync_scaffold.py")
            restored = snapshot(workspace)
            if restored != baseline:
                drift = sorted(
                    str(path) for path in GENERATED_PATHS if restored.get(path) != baseline.get(path)
                )
                raise AssertionError(f"generated surfaces did not return to baseline: {', '.join(drift)}")
            run(workspace, "scripts/build_reader_edition.py", "--check")
            run(workspace, "scripts/validate_reader_manuscript_manifest.py")
            run(workspace, "scripts/sync_reader_chapter_review_matrix.py", "--check")
            run(workspace, "scripts/validate_reader_chapter_reconciliation_approval.py")
    except (AssertionError, FileNotFoundError, OSError, RuntimeError, TypeError, ValueError) as exc:
        fail(str(exc))

    print(
        "Dynamic spine validation passed: manifest insertion/removal exercised "
        f"{original_count} -> {original_count + 1} -> {original_count} chapters with "
        "scaffold and reader derivation restored without manual count edits."
    )


if __name__ == "__main__":
    main()

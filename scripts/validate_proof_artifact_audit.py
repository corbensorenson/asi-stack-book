#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
ROOT_LEAN_MODULE = ROOT / "lean" / "AsiStackProofs.lean"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"
REPORT = ROOT / "docs" / "proof_artifact_audit.md"

LIMITATION_MARKERS = [
    "does not prove",
    "does not implement",
    "does not evaluate",
    "do not prove",
    "do not claim",
    "not a proof",
    "not prove",
    "only the record-level",
    "scope is narrow",
    "finite-record",
    "finite record",
    "not the truth",
    "still require",
]

SECTION_END_RE = re.compile(r"^##\s+", re.MULTILINE)


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    chapters: list[dict[str, Any]] = []
    for part in structure.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                chapters.append(chapter)
    return chapters


def root_imports() -> set[str]:
    imports: set[str] = set()
    for line in ROOT_LEAN_MODULE.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith("import "):
            imports.add(stripped.removeprefix("import ").strip())
    return imports


def formalization_section(text: str) -> str:
    match = re.search(r"^#{2,3}\s+Formalization hooks\s*$", text, flags=re.MULTILINE)
    if not match:
        return ""
    rest = text[match.start() :]
    end = SECTION_END_RE.search(rest, pos=match.end() - match.start() + 1)
    return rest[: end.start()] if end else rest


def has_limitation_boundary(section: str) -> bool:
    lower = section.lower()
    return any(marker in lower for marker in LIMITATION_MARKERS)


def qmd_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def module_stats(module_path: Path) -> dict[str, int]:
    if not module_path.exists():
        return {"theorems": 0, "defs": 0, "structures": 0}
    text = module_path.read_text(encoding="utf-8", errors="ignore")
    return {
        "theorems": len(re.findall(r"\btheorem\s+", text)),
        "defs": len(re.findall(r"\bdef\s+", text)),
        "structures": len(re.findall(r"\bstructure\s+", text)),
    }


def build_report() -> tuple[str, list[str]]:
    structure = read_json(STRUCTURE)
    manifest = read_json(MANIFEST)
    triage = read_json(TRIAGE)

    if not isinstance(structure, dict):
        raise TypeError("book_structure.json must contain an object")
    if not isinstance(manifest, dict) or not isinstance(manifest.get("records"), list):
        raise TypeError("proofs/proof_manifest.json must contain a records list")
    if not isinstance(triage, dict) or not isinstance(triage.get("records"), list):
        raise TypeError("proofs/proof_triage.json must contain a records list")

    records = [record for record in manifest["records"] if isinstance(record, dict)]
    triage_records = [record for record in triage["records"] if isinstance(record, dict)]
    chapters = {chapter["id"]: chapter for chapter in flatten_chapters(structure)}
    imported_modules = root_imports()
    triage_by_tag = {record.get("tag"): record for record in triage_records}
    target_count = len(records)

    errors: list[str] = []
    warnings: list[str] = []
    target_rows: list[str] = []
    chapter_results: dict[str, dict[str, int]] = defaultdict(lambda: Counter())
    module_target_counts = Counter(str(record.get("module_path", "")) for record in records)
    module_rows: list[str] = []

    duplicate_tags = [tag for tag, count in Counter(record.get("tag") for record in records).items() if count > 1]
    for tag in sorted(str(tag) for tag in duplicate_tags):
        errors.append(f"Duplicate proof target tag: {tag}")

    appendix_text = APPENDIX_E.read_text(encoding="utf-8", errors="ignore") if APPENDIX_E.exists() else ""
    if str(target_count) not in appendix_text:
        errors.append(f"Appendix E does not mention the current proof target count {target_count}.")
    if "Proof-readiness validation" not in appendix_text:
        errors.append("Appendix E is missing the Proof-readiness validation repository-level check.")
    if "Proof artifact traceability audit" not in appendix_text:
        errors.append("Appendix E is missing the Proof artifact traceability audit repository-level check.")
    if "Proof target coverage summary" not in appendix_text:
        errors.append("Appendix E is missing the Proof target coverage summary repository-level check.")

    for module_path_str, count in sorted(module_target_counts.items()):
        module_path = ROOT / module_path_str
        stats = module_stats(module_path)
        if not module_path.exists():
            errors.append(f"{module_path_str}: referenced Lean module file is missing.")
        if stats["theorems"] < count:
            errors.append(
                f"{module_path_str}: has {stats['theorems']} theorem declarations for {count} proof targets."
            )
        module_rows.append(
            f"| `{qmd_escape(module_path_str)}` | {count} | {stats['theorems']} | {stats['defs']} | {stats['structures']} |"
        )

    for record in records:
        tag = str(record.get("tag", ""))
        chapter_id = str(record.get("chapter_id", ""))
        module = str(record.get("module", ""))
        module_path = ROOT / str(record.get("module_path", ""))
        status = str(record.get("status", ""))
        chapter = chapters.get(chapter_id)
        trace_bits: list[str] = []

        if not tag.startswith("lean:"):
            errors.append(f"{tag}: proof tag must start with lean:")

        triage_record = triage_by_tag.get(tag)
        if triage_record is None:
            errors.append(f"{tag}: missing proof triage record.")
            trace_bits.append("triage missing")
        else:
            for field in ("chapter_id", "module", "formal_target"):
                if triage_record.get(field) != record.get(field):
                    errors.append(f"{tag}: triage {field} does not match manifest.")
            if triage_record.get("target_status") != status:
                errors.append(f"{tag}: triage target_status does not match manifest status.")
            trace_bits.append("triage ok")

        if status == "implemented":
            if not module_path.exists():
                errors.append(f"{tag}: implemented target missing {record.get('module_path')}.")
            elif module != "AsiStackProofs" and module not in imported_modules:
                errors.append(f"{tag}: implemented module {module} is not imported by lean/AsiStackProofs.lean.")
            else:
                trace_bits.append("module ok")

        if chapter is None:
            errors.append(f"{tag}: chapter {chapter_id!r} is missing from book_structure.json.")
            target_rows.append(f"| `{qmd_escape(tag)}` | `{qmd_escape(chapter_id)}` | `{qmd_escape(module)}` | missing chapter |")
            continue

        chapter_path = ROOT / str(chapter.get("file", ""))
        if not chapter_path.exists():
            errors.append(f"{tag}: chapter file {chapter.get('file')} is missing.")
            target_rows.append(f"| `{qmd_escape(tag)}` | `{qmd_escape(chapter_id)}` | `{qmd_escape(module)}` | missing chapter file |")
            continue

        chapter_text = chapter_path.read_text(encoding="utf-8", errors="ignore")
        section = formalization_section(chapter_text)
        if tag not in chapter_text:
            errors.append(f"{tag}: tag missing from chapter file {chapter.get('file')}.")
            chapter_results[chapter_id]["missing_tag"] += 1
        else:
            chapter_results[chapter_id]["tag_present"] += 1
            trace_bits.append("chapter tag ok")
        if not section:
            errors.append(f"{tag}: chapter {chapter_id} has no Formalization hooks section.")
            chapter_results[chapter_id]["missing_section"] += 1
        elif not has_limitation_boundary(section):
            errors.append(f"{tag}: chapter {chapter_id} formalization section lacks an explicit limitation/non-claim boundary.")
            chapter_results[chapter_id]["missing_limitation"] += 1
        else:
            chapter_results[chapter_id]["limitation_present"] += 1
            trace_bits.append("limitation ok")

        target_rows.append(
            f"| `{qmd_escape(tag)}` | `{qmd_escape(chapter_id)}` | `{qmd_escape(module)}` | {qmd_escape('; '.join(trace_bits))} |"
        )

    chapter_rows = []
    for chapter_id in sorted(chapter_results):
        result = chapter_results[chapter_id]
        chapter_rows.append(
            f"| `{qmd_escape(chapter_id)}` | {result['tag_present']} | {result['limitation_present']} | {result['missing_tag']} | {result['missing_limitation']} |"
        )

    status_counts = Counter(str(record.get("status", "missing")) for record in records)
    triage_counts = Counter(str(record.get("triage", "missing")) for record in triage_records)
    summary_rows = [
        f"| Proof targets audited | {target_count} |",
        f"| Manifest status counts | {qmd_escape(json.dumps(dict(sorted(status_counts.items()))))} |",
        f"| Triage class counts | {qmd_escape(json.dumps(dict(sorted(triage_counts.items()))))} |",
        f"| Lean modules referenced | {len(module_target_counts)} |",
        f"| Chapters with proof targets | {len(chapter_results)} |",
        f"| Validation errors | {len(errors)} |",
        f"| Warnings | {len(warnings)} |",
    ]

    error_text = "\n".join(f"- {qmd_escape(error)}" for error in errors) if errors else "- None."
    warning_text = "\n".join(f"- {qmd_escape(warning)}" for warning in warnings) if warnings else "- None."

    report = f"""# Proof Artifact Audit

Generated by `python3 scripts/validate_proof_artifact_audit.py --write`.

This report audits traceability for implemented proof targets. It checks that the generated manifest, proof triage, Lean module files, root Lean imports, chapter formalization-hook tables, and chapter limitation/non-claim prose stay aligned.

It does **not** prove semantic adequacy, source interpretation, model quality, deployed enforcement, benchmark results, external theorem validity, or broad ASI Stack behavior. A passing audit means the proof artifacts are traceable and explicitly bounded.

## Summary

| Metric | Value |
|---|---:|
{chr(10).join(summary_rows)}

## Checked Boundaries

- Every manifest tag must have a matching proof-triage record with the same chapter, module, target, and status.
- Every implemented target must reference an existing Lean module imported by `lean/AsiStackProofs.lean`.
- Each referenced Lean module must contain at least as many theorem declarations as implemented targets assigned to that module.
- Every implemented target tag must appear in its chapter file.
- Every chapter formalization-hook section with implemented targets must include explicit limitation or non-claim language.
- Appendix E must expose the current proof target count, proof-readiness coverage boundary, and proof artifact traceability audit.

## Module Coverage

| Lean module path | Targets | Theorems | Defs | Structures |
|---|---:|---:|---:|---:|
{chr(10).join(module_rows)}

## Chapter Coverage

| Chapter ID | Tags present | Limitation references | Missing tags | Missing limitation references |
|---|---:|---:|---:|---:|
{chr(10).join(chapter_rows)}

## Target Trace

| Tag | Chapter ID | Lean module | Trace status |
|---|---|---|---|
{chr(10).join(target_rows)}

## Validation Errors

{error_text}

## Warnings

{warning_text}
"""
    return report, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write docs/proof_artifact_audit.md.")
    args = parser.parse_args()

    try:
        report, errors = build_report()
    except Exception as exc:
        print(f"Proof artifact audit failed: {exc}")
        sys.exit(1)

    if args.write:
        REPORT.write_text(report, encoding="utf-8")
    elif not REPORT.exists():
        print(f"{REPORT.relative_to(ROOT)} is missing; run scripts/validate_proof_artifact_audit.py --write")
        sys.exit(1)
    else:
        current = REPORT.read_text(encoding="utf-8")
        if current != report:
            print(f"{REPORT.relative_to(ROOT)} is out of date; run scripts/validate_proof_artifact_audit.py --write")
            sys.exit(1)

    if errors:
        print("Proof artifact audit failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    action = "wrote" if args.write else "validated"
    print(f"Proof artifact audit {action}: {len(read_json(MANIFEST)['records'])} targets.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
from collections import Counter
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "docs" / "proof_envelope_status_ledger.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
ADEQUACY = ROOT / "docs" / "proof_adequacy_review.md"
DEPTH = ROOT / "docs" / "proof_depth_classification.md"
AUDIT = ROOT / "docs" / "proof_artifact_audit.md"

ADEQUACY_ORDER = [
    "adequate finite-record invariant",
    "useful but too narrow",
    "needs richer state-machine or review semantics",
    "needs executable tests first",
    "needs empirical or baseline tests first",
    "research-agenda until artifact import",
]


def fail(errors: list[str]) -> None:
    print("Proof envelope status ledger validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def table_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def section(text: str, start: str, end: str) -> str:
    if start not in text:
        return ""
    body = text.split(start, 1)[1]
    if end in body:
        body = body.split(end, 1)[0]
    return body


def metric(text: str, name: str) -> str | None:
    match = re.search(rf"^\|\s*{re.escape(name)}\s*\|\s*(.*?)\s*\|$", text, re.MULTILINE)
    return match.group(1).strip() if match else None


def parse_adequacy_counts(text: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    body = section(text, "## Summary", "The reviewed targets")
    for line in body.splitlines():
        if not line.startswith("| ") or line.startswith("|---") or "Adequacy class" in line:
            continue
        cells = table_cells(line)
        if len(cells) < 2:
            continue
        try:
            counts[cells[0]] = int(cells[1].replace(",", ""))
        except ValueError:
            continue
    return counts


def qmd_escape(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def adequacy_phrase(counts: Counter[str], code: bool = False) -> str:
    parts: list[str] = []
    for adequacy_class in ADEQUACY_ORDER:
        count = counts.get(adequacy_class, 0)
        label = f"`{adequacy_class}`" if code else adequacy_class
        parts.append(f"{count} {label}")
    return ", ".join(parts[:-1]) + f", and {parts[-1]}"


def build_report() -> tuple[str, list[str]]:
    errors: list[str] = []
    manifest = load_json(MANIFEST)
    if not isinstance(manifest, dict):
        raise TypeError("proofs/proof_manifest.json must contain an object")
    records = manifest.get("records", [])
    if not isinstance(records, list):
        raise TypeError("proofs/proof_manifest.json must contain records")

    adequacy_text = ADEQUACY.read_text(encoding="utf-8")
    depth_text = DEPTH.read_text(encoding="utf-8")
    audit_text = AUDIT.read_text(encoding="utf-8")

    proof_targets = int(manifest.get("proof_target_count", len(records)))
    implemented_targets = sum(1 for record in records if isinstance(record, dict) and record.get("status") == "implemented")
    planned_targets = sum(1 for record in records if isinstance(record, dict) and record.get("status") == "planned")
    recognized_status_targets = sum(
        1
        for record in records
        if isinstance(record, dict) and record.get("status") in {"planned", "scaffolded", "implemented", "blocked", "retired"}
    )
    adequacy_counts = parse_adequacy_counts(adequacy_text)
    adequacy_total = sum(adequacy_counts.values())

    required_depth_metrics = {
        "Proof targets in manifest": metric(depth_text, "Proof targets in manifest"),
        "Lean modules scanned": metric(depth_text, "Lean modules scanned"),
        "Theorem declarations classified": metric(depth_text, "Theorem declarations classified"),
        "Direct/projection-style theorem declarations": metric(depth_text, "Direct/projection-style theorem declarations"),
        "Derived/decomposed theorem declarations": metric(depth_text, "Derived/decomposed theorem declarations"),
        "Unknown or mixed theorem declarations": metric(depth_text, "Unknown or mixed theorem declarations"),
        "Safety-critical theorem declarations": metric(depth_text, "Safety-critical theorem declarations"),
        "Safety-critical chapter classifications present": metric(depth_text, "Safety-critical chapter classifications present"),
    }
    required_audit_metrics = {
        "Proof targets audited": metric(audit_text, "Proof targets audited"),
        "Lean modules referenced": metric(audit_text, "Lean modules referenced"),
        "Chapters with proof targets": metric(audit_text, "Chapters with proof targets"),
        "Validation errors": metric(audit_text, "Validation errors"),
        "Warnings": metric(audit_text, "Warnings"),
    }

    if proof_targets != len(records):
        errors.append(f"Manifest proof_target_count is {proof_targets}; records list has {len(records)}.")
    if recognized_status_targets != proof_targets:
        errors.append(f"Recognized target statuses cover {recognized_status_targets}; expected {proof_targets}.")
    if adequacy_total != proof_targets:
        errors.append(f"Proof adequacy summary covers {adequacy_total} targets; expected {proof_targets}.")
    for adequacy_class in ADEQUACY_ORDER:
        if adequacy_class not in adequacy_counts:
            errors.append(f"Proof adequacy review is missing class {adequacy_class!r}.")
    for name, value in required_depth_metrics.items():
        if value is None:
            errors.append(f"Proof depth classification is missing metric {name!r}.")
    for name, value in required_audit_metrics.items():
        if value is None:
            errors.append(f"Proof artifact audit is missing metric {name!r}.")

    if required_depth_metrics["Proof targets in manifest"] not in {None, str(proof_targets)}:
        errors.append(
            "Proof depth target count "
            f"{required_depth_metrics['Proof targets in manifest']} does not match manifest {proof_targets}."
        )
    if required_audit_metrics["Proof targets audited"] not in {None, str(proof_targets)}:
        errors.append(
            "Proof artifact audit target count "
            f"{required_audit_metrics['Proof targets audited']} does not match manifest {proof_targets}."
        )
    if required_audit_metrics["Validation errors"] not in {None, "0"}:
        errors.append(f"Proof artifact audit reports validation errors: {required_audit_metrics['Validation errors']}.")
    if required_audit_metrics["Warnings"] not in {None, "0"}:
        errors.append(f"Proof artifact audit reports warnings: {required_audit_metrics['Warnings']}.")

    summary_rows = [
        f"| Proof targets in manifest | {proof_targets} |",
        f"| Implemented proof targets | {implemented_targets} |",
        f"| Planned proof targets | {planned_targets} |",
        f"| Lean modules referenced | {required_audit_metrics['Lean modules referenced'] or 'missing'} |",
        f"| Chapters with proof targets | {required_audit_metrics['Chapters with proof targets'] or 'missing'} |",
        f"| Theorem declarations classified | {required_depth_metrics['Theorem declarations classified'] or 'missing'} |",
        f"| Derived/decomposed theorem declarations | {required_depth_metrics['Derived/decomposed theorem declarations'] or 'missing'} |",
        f"| Direct/projection-style theorem declarations | {required_depth_metrics['Direct/projection-style theorem declarations'] or 'missing'} |",
        f"| Unknown or mixed theorem declarations | {required_depth_metrics['Unknown or mixed theorem declarations'] or 'missing'} |",
        f"| Safety-critical theorem declarations | {required_depth_metrics['Safety-critical theorem declarations'] or 'missing'} |",
        f"| Safety-critical chapter classifications present | {required_depth_metrics['Safety-critical chapter classifications present'] or 'missing'} |",
    ]
    adequacy_rows = [
        f"| {qmd_escape(adequacy_class)} | {adequacy_counts.get(adequacy_class, 0)} |"
        for adequacy_class in ADEQUACY_ORDER
    ]

    validation_text = "\n".join(f"- {qmd_escape(error)}" for error in errors) if errors else "- None."
    report = f"""# Proof Envelope Status Ledger

Generated by `python3 scripts/validate_proof_envelope_status_ledger.py --write`.

This ledger keeps the public v1.0 status snapshot readable by moving proof-envelope detail out of the status row. It summarizes the current proof target count, traceability status, adequacy classes, proof-depth metrics, and non-claim boundaries from the generated proof reports.

It does **not** add proof targets, prove semantic adequacy, promote support states, validate external theorem references, prove deployed enforcement, prove benchmark results, or claim broad ASI Stack behavior.

## Summary

| Metric | Value |
|---|---:|
{chr(10).join(summary_rows)}

## Adequacy Snapshot

The current adequacy review classifies {adequacy_phrase(adequacy_counts)}. These classes route follow-through work; they do not change theorem status or chapter support states.

| Adequacy class | Targets |
|---|---:|
{chr(10).join(adequacy_rows)}

## Traceability Reports

- `docs/proof_artifact_audit.md` audits manifest tags, proof triage records, Lean module files, root Lean imports, chapter formalization-hook tables, and limitation prose.
- `docs/proof_adequacy_review.md` classifies semantic adequacy for current proof targets and records the backlog implied by narrow finite-record predicates.
- `docs/proof_depth_classification.md` classifies theorem body shape. `derived_or_decomposed` is stronger than direct projection, but it still does not establish semantic adequacy.
- `lake build` remains the Lean build gate; build success only means the checked finite predicates compile.

## Status Snapshot Contract

The public status row may summarize this ledger instead of listing every follow-through increment. The row must still name the current proof target count, the generated ledger, the proof artifact audit, the proof adequacy review, the proof-depth classifier, `lake build`, the adequacy counts, and the non-promotion boundary.

## Non-Claim Boundary

- No proof-envelope artifact promotes any chapter core claim above `argument`.
- A finite Lean predicate is not automatically an adequate formalization of a full chapter boundary.
- Schemas, tests, benchmarks, source notes, external theorem references, and Lean predicates remain separate evidence lanes with separate authority.
- This ledger is a status-surface cleanup, not a proof-strengthening increment.

## Validation Errors

{validation_text}
"""
    return report, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write docs/proof_envelope_status_ledger.md.")
    args = parser.parse_args()

    try:
        report, errors = build_report()
    except Exception as exc:
        print(f"Proof envelope status ledger failed: {exc}")
        sys.exit(1)

    if args.write:
        LEDGER.write_text(report, encoding="utf-8")
    elif not LEDGER.exists():
        print(f"{LEDGER.relative_to(ROOT)} is missing; run scripts/validate_proof_envelope_status_ledger.py --write")
        sys.exit(1)
    else:
        current = LEDGER.read_text(encoding="utf-8")
        if current != report:
            print(f"{LEDGER.relative_to(ROOT)} is out of date; run scripts/validate_proof_envelope_status_ledger.py --write")
            sys.exit(1)

    if errors:
        fail(errors)

    action = "wrote" if args.write else "validated"
    print(f"Proof envelope status ledger {action}: {len(load_json(MANIFEST)['records'])} targets.")


if __name__ == "__main__":
    main()

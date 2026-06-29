#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEAN_DIR = ROOT / "lean" / "AsiStackProofs"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
REPORT = ROOT / "docs" / "proof_depth_classification.md"

SAFETY_CRITICAL_MODULES = {
    "lean/AsiStackProofs/Alignment.lean",
    "lean/AsiStackProofs/Corrigibility.lean",
    "lean/AsiStackProofs/GovernanceRights.lean",
    "lean/AsiStackProofs/SelfImprovement.lean",
    "lean/AsiStackProofs/ValueConflict.lean",
}
SAFETY_CRITICAL_CHAPTERS = {
    "lean/AsiStackProofs/Alignment.lean": "chapters/constitutional-alignment-substrate.qmd",
    "lean/AsiStackProofs/Corrigibility.lean": "chapters/agency-dignity-and-corrigibility.qmd",
    "lean/AsiStackProofs/GovernanceRights.lean": "chapters/governance-rights-fork-exit-and-audit.qmd",
    "lean/AsiStackProofs/SelfImprovement.lean": "chapters/recursive-self-improvement-boundaries.qmd",
    "lean/AsiStackProofs/ValueConflict.lean": "chapters/moral-uncertainty-and-value-conflict.qmd",
}
CLASSIFICATION_PHRASE = "projection-only traceability"

DECL_RE = re.compile(r"^(?:theorem|lemma|def|structure|inductive|namespace|end)\b", re.MULTILINE)
THEOREM_RE = re.compile(r"^theorem\s+([^\s:{]+)", re.MULTILINE)
DERIVED_PATTERNS = {
    "unfold": re.compile(r"(^|\s)unfold\b"),
    "cases": re.compile(r"(^|\s)cases\b"),
    "rcases": re.compile(r"(^|\s)rcases\b"),
    "rw": re.compile(r"(^|\s)rw\b"),
    "simp": re.compile(r"(^|\s)simp\b"),
    "constructor": re.compile(r"(^|\s)constructor\b"),
    "apply": re.compile(r"(^|\s)apply\b"),
    "have": re.compile(r"(^|\s)have\b"),
    "left": re.compile(r"(^|\s)left\b"),
    "right": re.compile(r"(^|\s)right\b"),
    "by_cases": re.compile(r"(^|\s)by_cases\b"),
    "contradiction": re.compile(r"(^|\s)contradiction\b"),
    "omega": re.compile(r"(^|\s)omega\b"),
    "linarith": re.compile(r"(^|\s)linarith\b"),
    "calc": re.compile(r"(^|\s)calc\b"),
    "induction": re.compile(r"(^|\s)induction\b"),
    "match": re.compile(r"(^|\s)match\b"),
    "split": re.compile(r"(^|\s)split\b"),
    "subst": re.compile(r"(^|\s)subst\b"),
}


@dataclass(frozen=True)
class TheoremRecord:
    module_path: str
    name: str
    depth_class: str
    evidence: str


def read_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def qmd_escape(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def strip_comments(text: str) -> str:
    lines: list[str] = []
    for line in text.splitlines():
        lines.append(line.split("--", 1)[0])
    return "\n".join(lines)


def theorem_blocks(path: Path) -> list[tuple[str, str]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    declarations = list(DECL_RE.finditer(text))
    theorem_starts = list(THEOREM_RE.finditer(text))
    blocks: list[tuple[str, str]] = []
    for match in theorem_starts:
        next_decl_start = len(text)
        for decl in declarations:
            if decl.start() > match.start():
                next_decl_start = decl.start()
                break
        blocks.append((match.group(1), text[match.start() : next_decl_start]))
    return blocks


def classify_body(block: str) -> tuple[str, str]:
    if re.search(r"\b(?:sorry|admit)\b", block):
        return "unknown_or_mixed", "contains sorry/admit marker"

    if ":= by" not in block:
        return "unknown_or_mixed", "no ':= by' body detected"

    body = strip_comments(block.split(":= by", 1)[1]).strip()
    if not body:
        return "unknown_or_mixed", "empty proof body"

    hits = [name for name, pattern in DERIVED_PATTERNS.items() if pattern.search(body)]
    if hits:
        return "derived_or_decomposed", "uses " + ", ".join(sorted(hits))

    direct_markers = ["intro", "intros", "exact", "assumption", "rfl"]
    if any(re.search(rf"(^|\s){marker}\b", body) for marker in direct_markers):
        return "direct_or_projection", "only direct intro/exact/assumption/rfl-style steps detected"

    return "unknown_or_mixed", "no recognized depth pattern"


def load_manifest_rows() -> list[dict[str, Any]]:
    manifest = read_json(MANIFEST)
    if not isinstance(manifest, dict) or not isinstance(manifest.get("records"), list):
        raise TypeError("proofs/proof_manifest.json must contain a records list.")
    rows = [row for row in manifest["records"] if isinstance(row, dict)]
    return rows


def classify_theorems() -> list[TheoremRecord]:
    records: list[TheoremRecord] = []
    for path in sorted(LEAN_DIR.glob("*.lean")):
        for name, block in theorem_blocks(path):
            depth_class, evidence = classify_body(block)
            records.append(
                TheoremRecord(
                    module_path=rel(path),
                    name=name,
                    depth_class=depth_class,
                    evidence=evidence,
                )
            )
    return records


def build_report() -> tuple[str, list[str]]:
    manifest_rows = load_manifest_rows()
    theorem_rows = classify_theorems()
    errors: list[str] = []
    warnings: list[str] = []

    target_counts = Counter(str(row.get("module_path", "")) for row in manifest_rows)
    chapter_by_module: dict[str, set[str]] = defaultdict(set)
    for row in manifest_rows:
        module_path = str(row.get("module_path", ""))
        chapter_id = str(row.get("chapter_id", ""))
        if module_path:
            chapter_by_module[module_path].add(chapter_id)

    theorem_counts: dict[str, Counter[str]] = defaultdict(Counter)
    theorem_names_by_module: dict[str, list[TheoremRecord]] = defaultdict(list)
    for theorem in theorem_rows:
        theorem_counts[theorem.module_path][theorem.depth_class] += 1
        theorem_names_by_module[theorem.module_path].append(theorem)

    all_module_paths = sorted(set(target_counts) | set(theorem_counts))
    missing_safety = sorted(path for path in SAFETY_CRITICAL_MODULES if path not in all_module_paths)
    for path in missing_safety:
        errors.append(f"Safety-critical Lean module {path} is missing from the depth scan.")

    for path in sorted(SAFETY_CRITICAL_MODULES):
        counts = theorem_counts.get(path, Counter())
        projection_count = counts.get("direct_or_projection", 0)
        if projection_count:
            warnings.append(
                f"{path} has {projection_count} direct/projection-style theorem(s) and must remain explicitly scoped."
            )

    module_lines: list[str] = []
    safety_lines: list[str] = []
    safety_chapter_lines: list[str] = []
    theorem_lines: list[str] = []
    required_chapter_classifications = 0
    present_chapter_classifications = 0

    for path in all_module_paths:
        counts = theorem_counts.get(path, Counter())
        chapters = ", ".join(sorted(chapter_by_module.get(path, []))) or "unmapped"
        direct_count = counts.get("direct_or_projection", 0)
        derived_count = counts.get("derived_or_decomposed", 0)
        unknown_count = counts.get("unknown_or_mixed", 0)
        if path in SAFETY_CRITICAL_MODULES and direct_count:
            treatment = "v1-blocking: upgrade or keep explicitly classified as projection-only traceability"
        elif direct_count and derived_count == 0:
            treatment = "traceability hook unless adequacy review narrows claim"
        elif direct_count:
            treatment = "mixed: preserve limitation prose and prioritize projection replacements"
        elif unknown_count:
            treatment = "manual review"
        else:
            treatment = "derived/decomposed by classifier"
        line = (
            f"| `{qmd_escape(path)}` | {qmd_escape(chapters)} | {target_counts.get(path, 0)} | "
            f"{sum(counts.values())} | {direct_count} | {derived_count} | {unknown_count} | {qmd_escape(treatment)} |"
        )
        module_lines.append(line)
        if path in SAFETY_CRITICAL_MODULES:
            safety_lines.append(line)
            chapter_file = SAFETY_CRITICAL_CHAPTERS[path]
            chapter_path = ROOT / chapter_file
            chapter_text = chapter_path.read_text(encoding="utf-8", errors="ignore") if chapter_path.exists() else ""
            classification_required = direct_count > 0
            classification_present = CLASSIFICATION_PHRASE in chapter_text.lower()
            if classification_required:
                required_chapter_classifications += 1
                if classification_present:
                    present_chapter_classifications += 1
                else:
                    errors.append(
                        f"{path}: {chapter_file} must explicitly classify direct/projection Lean hooks as projection-only traceability."
                    )
            safety_chapter_lines.append(
                f"| `{qmd_escape(path)}` | `{qmd_escape(chapter_file)}` | "
                f"{direct_count} | {'yes' if classification_required else 'no'} | "
                f"{'yes' if classification_present else 'no'} |"
            )

    for theorem in sorted(theorem_rows, key=lambda item: (item.module_path, item.name)):
        safety = "yes" if theorem.module_path in SAFETY_CRITICAL_MODULES else "no"
        theorem_lines.append(
            f"| `{qmd_escape(theorem.module_path)}` | `{qmd_escape(theorem.name)}` | "
            f"{qmd_escape(theorem.depth_class)} | {safety} | {qmd_escape(theorem.evidence)} |"
        )

    summary_counts = Counter(theorem.depth_class for theorem in theorem_rows)
    safety_theorems = [
        theorem for theorem in theorem_rows if theorem.module_path in SAFETY_CRITICAL_MODULES
    ]
    safety_counts = Counter(theorem.depth_class for theorem in safety_theorems)
    summary_rows = [
        f"| Proof targets in manifest | {len(manifest_rows)} |",
        f"| Lean modules scanned | {len(all_module_paths)} |",
        f"| Theorem declarations classified | {len(theorem_rows)} |",
        f"| Direct/projection-style theorem declarations | {summary_counts.get('direct_or_projection', 0)} |",
        f"| Derived/decomposed theorem declarations | {summary_counts.get('derived_or_decomposed', 0)} |",
        f"| Unknown or mixed theorem declarations | {summary_counts.get('unknown_or_mixed', 0)} |",
        f"| Safety-critical theorem declarations | {len(safety_theorems)} |",
        f"| Safety-critical direct/projection declarations | {safety_counts.get('direct_or_projection', 0)} |",
        f"| Safety-critical chapter classifications present | {present_chapter_classifications}/{required_chapter_classifications} |",
        f"| Validation errors | {len(errors)} |",
        f"| Warnings | {len(warnings)} |",
    ]

    warning_text = "\n".join(f"- {qmd_escape(warning)}" for warning in warnings) if warnings else "- None."
    error_text = "\n".join(f"- {qmd_escape(error)}" for error in errors) if errors else "- None."

    report = f"""# Proof Depth Classification

Generated by `python3 scripts/validate_proof_depth.py --write`.

This report classifies Lean theorem bodies by proof-shape depth so the book can distinguish traceability hooks from more substantive derived invariants. It is a conservative syntax-level audit. It does **not** prove semantic adequacy, theorem importance, model correctness, deployed enforcement, source interpretation, benchmark validity, or ASI Stack safety.

`direct_or_projection` means the theorem body uses only direct introduction, exact, assumption, or reflexivity-style steps by this classifier. Those theorems may still be useful repository traceability, but they must not be presented as broad safety proofs unless the chapter claim is scoped to the assumed predicate or record field being projected.

`derived_or_decomposed` means the body uses at least one structural proof step such as unfolding, case analysis, rewriting, branching, contradiction handling, or a comparable decomposition tactic. This is stronger than direct projection, but it is still only as good as the formal model being checked.

## Summary

| Metric | Value |
|---|---:|
{chr(10).join(summary_rows)}

## Safety-Critical Modules

The v1.0 roadmap prioritizes these modules because projection-style hooks in alignment, corrigibility, governance rights, self-improvement, or value-conflict chapters can be easily mistaken for stronger safety results.

| Lean module | Chapters | Proof targets | Theorems | Direct/projection | Derived/decomposed | Unknown/mixed | Suggested treatment |
|---|---|---:|---:|---:|---:|---:|---|
{chr(10).join(safety_lines)}

## Safety-Critical Chapter Classification

Safety-critical modules with direct/projection-style theorem declarations must have matching chapter limitation prose that uses the phrase `projection-only traceability`. This makes the v1.0 proof-depth gate auditable in the rendered book rather than only in internal reports.

| Lean module | Chapter file | Direct/projection declarations | Classification required | Classification present |
|---|---|---:|---|---|
{chr(10).join(safety_chapter_lines)}

## Module Classification

| Lean module | Chapters | Proof targets | Theorems | Direct/projection | Derived/decomposed | Unknown/mixed | Suggested treatment |
|---|---|---:|---:|---:|---:|---:|---|
{chr(10).join(module_lines)}

## Theorem Classification

| Lean module | Theorem | Depth class | Safety-critical | Evidence |
|---|---|---|---|---|
{chr(10).join(theorem_lines)}

## Validation Errors

{error_text}

## Warnings

{warning_text}
"""
    return report, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="Write docs/proof_depth_classification.md.")
    args = parser.parse_args()

    try:
        report, errors = build_report()
    except Exception as exc:
        print(f"Proof-depth validation failed: {exc}")
        sys.exit(1)

    if args.write:
        REPORT.write_text(report, encoding="utf-8")
    elif not REPORT.exists():
        print(f"{REPORT.relative_to(ROOT)} is missing; run scripts/validate_proof_depth.py --write")
        sys.exit(1)
    else:
        current = REPORT.read_text(encoding="utf-8")
        if current != report:
            print(f"{REPORT.relative_to(ROOT)} is out of date; run scripts/validate_proof_depth.py --write")
            sys.exit(1)

    if errors:
        print("Proof-depth validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Proof-depth validation passed: "
        f"{len(classify_theorems())} theorem declarations classified."
    )


if __name__ == "__main__":
    main()

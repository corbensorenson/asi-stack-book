#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_proof_depth import CLASSIFICATION_PHRASE, DECL_RE, SAFETY_CRITICAL_MODULES, THEOREM_RE, classify_body


ROOT = Path(__file__).resolve().parents[1]
LEAN_DIR = ROOT / "lean" / "AsiStackProofs"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
CLAIMS = ROOT / "evidence_quality" / "claim_atom_registry.json"
REVIEWS = ROOT / "proofs" / "proof_rationalization_reviews.json"
REGISTRY = ROOT / "proofs" / "proof_rationalization_registry.json"
REPORT = ROOT / "docs" / "proof_rationalization_registry.md"
DOSSIERS = ROOT / "evidence_quality" / "proof_model_dossiers"
ROADMAP_ID = "asi-stack-post-v2-3-claim-proof-sota-challenge-2026-07-14"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalize(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def theorem_blocks(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    declarations = list(DECL_RE.finditer(text))
    rows: list[dict[str, Any]] = []
    for match in THEOREM_RE.finditer(text):
        end = next((decl.start() for decl in declarations if decl.start() > match.start()), len(text))
        block = text[match.start():end]
        signature = block.split(":= by", 1)[0]
        body = block.split(":= by", 1)[1] if ":= by" in block else ""
        depth_class, depth_evidence = classify_body(block)
        rows.append(
            {
                "name": match.group(1),
                "source_start_line": text.count("\n", 0, match.start()) + 1,
                "source_end_line": text.count("\n", 0, end) + 1,
                "signature": normalize(signature),
                "body": body,
                "depth_class": depth_class,
                "depth_evidence": depth_evidence,
                "baseline_block_sha256": digest(block),
            }
        )
    return rows


def current_theorems() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for path in sorted(LEAN_DIR.glob("*.lean")):
        module_path = str(path.relative_to(ROOT))
        for row in theorem_blocks(path):
            theorem_id = f"{module_path}::{row['name']}"
            rows.append({"theorem_id": theorem_id, "module_path": module_path, **row})
    return rows


def initial_baseline() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    manifest = load(MANIFEST)
    targets = [row for row in manifest["records"] if isinstance(row, dict)]
    claims = {row["atom_id"] for row in load(CLAIMS)["atoms"]}
    targets_by_module: dict[str, list[dict[str, Any]]] = defaultdict(list)
    chapter_by_module: dict[str, str] = {}
    for target in targets:
        targets_by_module[target["module_path"]].append(target)
        chapter_by_module[target["module_path"]] = target["chapter_id"]
        claim_id = f"{target['chapter_id']}.core"
        if claim_id not in claims:
            raise ValueError(f"Missing claim atom for proof target: {claim_id}")

    theorem_rows = current_theorems()
    theorem_names = {row["name"] for row in theorem_rows}
    theorem_ids_by_name: dict[str, list[str]] = defaultdict(list)
    for row in theorem_rows:
        theorem_ids_by_name[row["name"]].append(row["theorem_id"])

    baseline_theorems: list[dict[str, Any]] = []
    for row in theorem_rows:
        module_path = row["module_path"]
        if module_path not in chapter_by_module:
            raise ValueError(f"Theorem module has no proof-manifest chapter owner: {module_path}")
        body_identifiers = set(re.findall(r"[A-Za-z_][A-Za-z0-9_'.]*", row["body"]))
        references = sorted((body_identifiers & theorem_names) - {row["name"]})
        dependencies = sorted({item for name in references for item in theorem_ids_by_name[name]})
        baseline_theorems.append(
            {
                "theorem_id": row["theorem_id"],
                "chapter_id": chapter_by_module[module_path],
                "claim_atom_id": f"{chapter_by_module[module_path]}.core",
                "module_path": module_path,
                "name": row["name"],
                "source_start_line": row["source_start_line"],
                "source_end_line": row["source_end_line"],
                "baseline_signature": row["signature"],
                "baseline_block_sha256": row["baseline_block_sha256"],
                "depth_class": row["depth_class"],
                "depth_evidence": row["depth_evidence"],
                "safety_critical_module": module_path in SAFETY_CRITICAL_MODULES,
                "candidate_target_tags": sorted(target["tag"] for target in targets_by_module[module_path]),
                "theorem_dependencies": dependencies,
                "review_state": "machine_candidate",
                "disposition": None,
                "semantic_role": None,
                "assumptions": [],
                "excluded_effects": [],
                "countermodel_refs": [],
                "mutation_refs": [],
                "consumer_refs": [],
                "runtime_consumer_refs": [],
                "replacement_refs": [],
                "review_rationale": None,
            }
        )

    reverse_dependencies: dict[str, list[str]] = defaultdict(list)
    for row in baseline_theorems:
        for dependency in row["theorem_dependencies"]:
            reverse_dependencies[dependency].append(row["theorem_id"])
    for row in baseline_theorems:
        row["theorem_consumers"] = sorted(reverse_dependencies[row["theorem_id"]])

    baseline_targets: list[dict[str, Any]] = []
    theorem_ids_by_module: dict[str, list[str]] = defaultdict(list)
    for row in baseline_theorems:
        theorem_ids_by_module[row["module_path"]].append(row["theorem_id"])
    for target in targets:
        baseline_targets.append(
            {
                "target_id": target["tag"],
                "chapter_id": target["chapter_id"],
                "claim_atom_id": f"{target['chapter_id']}.core",
                "module": target["module"],
                "module_path": target["module_path"],
                "formal_target": target["formal_target"],
                "baseline_status": target["status"],
                "baseline_outline_line": target["outline_line"],
                "candidate_theorem_ids": sorted(theorem_ids_by_module[target["module_path"]]),
                "review_state": "machine_candidate",
                "disposition": None,
                "semantic_role": None,
                "assumptions": [],
                "excluded_effects": [],
                "dependencies": [],
                "countermodel_refs": [],
                "mutation_refs": [],
                "consumer_refs": [],
                "runtime_consumer_refs": [],
                "replacement_refs": [],
                "review_rationale": None,
            }
        )
    return baseline_theorems, baseline_targets


def apply_reviews(rows: list[dict[str, Any]], reviews: dict[str, Any], key: str, id_key: str) -> None:
    overlay = reviews.get(key, {})
    known = {row[id_key] for row in rows}
    unknown = sorted(set(overlay) - known)
    if unknown:
        raise ValueError(f"Unknown {key}: {unknown[:5]}")
    for row in rows:
        patch = overlay.get(row[id_key])
        if patch:
            row.update(patch)


def build() -> tuple[dict[str, Any], str, dict[str, str]]:
    existing = load(REGISTRY) if REGISTRY.exists() else None
    if existing:
        theorem_rows = existing["baseline_theorems"]
        target_rows = existing["baseline_targets"]
    else:
        theorem_rows, target_rows = initial_baseline()
    theorem_rows = json.loads(json.dumps(theorem_rows))
    target_rows = json.loads(json.dumps(target_rows))
    for row in target_rows:
        row.setdefault("semantic_role", None)
        row.setdefault("excluded_effects", [])
        row.setdefault("consumer_refs", [])
    for row in theorem_rows:
        row.setdefault("consumer_refs", [])
    reviews = load(REVIEWS)
    apply_reviews(theorem_rows, reviews, "theorem_reviews", "theorem_id")
    apply_reviews(target_rows, reviews, "target_reviews", "target_id")

    current = {row["theorem_id"]: row for row in current_theorems()}
    for row in theorem_rows:
        now = current.get(row["theorem_id"])
        row["current_present"] = now is not None
        row["current_block_sha256"] = now["baseline_block_sha256"] if now else None
        row["current_matches_baseline"] = bool(now and now["baseline_block_sha256"] == row["baseline_block_sha256"])

    current_targets = {row["tag"]: row for row in load(MANIFEST)["records"]}
    for row in target_rows:
        now = current_targets.get(row["target_id"])
        row["current_present"] = now is not None
        row["current_status"] = now.get("status") if now else None
        row["current_matches_baseline"] = bool(
            now
            and now.get("chapter_id") == row["chapter_id"]
            and now.get("module_path") == row["module_path"]
            and now.get("formal_target") == row["formal_target"]
        )

    theorem_counts = Counter(row["review_state"] for row in theorem_rows)
    target_counts = Counter(row["review_state"] for row in target_rows)
    depth_counts = Counter(row["depth_class"] for row in theorem_rows)
    module_paths = sorted({row["module_path"] for row in theorem_rows} | {row["module_path"] for row in target_rows})
    fully_reviewed_modules = [
        module_path
        for module_path in module_paths
        if all(
            row["review_state"] != "machine_candidate"
            for row in theorem_rows + target_rows
            if row["module_path"] == module_path
        )
    ]
    registry = {
        "schema_version": "asi_stack.proof_rationalization_registry.v0",
        "roadmap_id": ROADMAP_ID,
        "baseline_frozen_at": "2026-07-15",
        "generated_from": [
            "proofs/proof_manifest.json",
            "lean/AsiStackProofs/*.lean",
            "evidence_quality/claim_atom_registry.json",
            "proofs/proof_rationalization_reviews.json",
        ],
        "summary": {
            "baseline_theorem_declaration_count": len(theorem_rows),
            "baseline_proof_target_count": len(target_rows),
            "chapter_count": len({row["chapter_id"] for row in target_rows}),
            "module_count": len(module_paths),
            "fully_reviewed_module_count": len(fully_reviewed_modules),
            "safety_critical_module_count": len(SAFETY_CRITICAL_MODULES),
            "safety_critical_fully_reviewed_module_count": len(set(fully_reviewed_modules) & SAFETY_CRITICAL_MODULES),
            "theorem_review_state_counts": dict(sorted(theorem_counts.items())),
            "target_review_state_counts": dict(sorted(target_counts.items())),
            "depth_class_counts": dict(sorted(depth_counts.items())),
            "missing_current_theorem_count": sum(not row["current_present"] for row in theorem_rows),
            "changed_current_theorem_count": sum(row["current_present"] and not row["current_matches_baseline"] for row in theorem_rows),
            "missing_current_target_count": sum(not row["current_present"] for row in target_rows),
            "changed_current_target_count": sum(row["current_present"] and not row["current_matches_baseline"] for row in target_rows),
            "support_state_effect": "none",
        },
        "baseline_theorems": theorem_rows,
        "baseline_targets": target_rows,
        "non_claims": [
            "Inventory, parsing, depth classification, theorem count, target count, or Lean build success does not establish semantic adequacy.",
            "Candidate target mappings are module-level discovery aids until semantic review names the exact target, assumptions, consumers, countermodels, and mutations.",
            "A retained theorem cannot promote a chapter claim without its separately accepted evidence transition.",
        ],
    }

    chapter_theorems: dict[str, list[dict[str, Any]]] = defaultdict(list)
    chapter_targets: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in theorem_rows:
        chapter_theorems[row["chapter_id"]].append(row)
    for row in target_rows:
        chapter_targets[row["chapter_id"]].append(row)
    dossiers: dict[str, str] = {}
    chapter_lines: list[str] = []
    for chapter_id in sorted(chapter_targets):
        theorems = chapter_theorems[chapter_id]
        targets = chapter_targets[chapter_id]
        pending_theorems = sum(row["review_state"] == "machine_candidate" for row in theorems)
        pending_targets = sum(row["review_state"] == "machine_candidate" for row in targets)
        chapter_lines.append(f"| `{chapter_id}` | {len(targets)} | {len(theorems)} | {pending_targets} | {pending_theorems} |")
        target_lines = "\n".join(
            f"| `{row['target_id']}` | {row['review_state']} | {row.get('disposition') or 'pending'} |"
            for row in targets
        )
        theorem_lines = "\n".join(
            f"| `{row['name']}` | {row['depth_class']} | {row['review_state']} | {row.get('disposition') or 'pending'} |"
            for row in theorems
        )
        dossiers[chapter_id] = f"""# Proof-model dossier: {chapter_id}

Generated from the frozen activation-baseline inventory and semantic review overlay. It is a P2 work surface, not proof of adequacy or a support transition.

## Baseline targets

| Target | Review state | Disposition |
|---|---|---|
{target_lines}

## Baseline theorem declarations

| Theorem | Syntax depth | Review state | Disposition |
|---|---|---|---|
{theorem_lines}

## Required closure

Every retained item needs one claim atom, exact assumptions and exclusions, a semantic role, dependencies, countermodel or negative-case coverage, mutation coverage, a live consumer, and a bounded disposition. Missing fields remain work; absence is not evidence.
"""

    report = f"""# Proof Rationalization Registry

Generated by `python3 scripts/build_proof_rationalization_registry.py` from the frozen P2 activation baseline plus the review overlay.

This inventory freezes the 1,151 theorem declarations and 298 proof targets that P2 must disposition. It preserves retired and replaced baseline items instead of deleting history. Syntax depth, candidate module mappings, counts, and green Lean builds are discovery evidence only; they do not establish semantic adequacy or promote a claim.

## Summary

| Metric | Value |
|---|---:|
| Baseline theorem declarations | {len(theorem_rows)} |
| Baseline proof targets | {len(target_rows)} |
| Chapters | {len(chapter_targets)} |
| Lean modules | {len(module_paths)} |
| Fully reviewed modules | {len(fully_reviewed_modules)} |
| Safety-critical modules fully reviewed | {len(set(fully_reviewed_modules) & SAFETY_CRITICAL_MODULES)}/{len(SAFETY_CRITICAL_MODULES)} |
| Theorem machine candidates | {theorem_counts.get('machine_candidate', 0)} |
| Target machine candidates | {target_counts.get('machine_candidate', 0)} |
| Direct/projection declarations | {depth_counts.get('direct_or_projection', 0)} |
| Derived/decomposed declarations | {depth_counts.get('derived_or_decomposed', 0)} |
| Unknown/mixed declarations | {depth_counts.get('unknown_or_mixed', 0)} |
| Support-state effect | none |

## Chapter work queue

| Chapter | Targets | Theorems | Pending targets | Pending theorems |
|---|---:|---:|---:|---:|
{chr(10).join(chapter_lines)}

## Closure rule

P2 closed on 2026-07-16 only after every baseline target and theorem received a claim-centered semantic disposition; every retained item received exact assumptions, exclusions, dependencies, countermodels or negative cases, mutation coverage, and a live consumer; every retired, merged, or replaced item preserved lineage; and all 298 current targets received an explicit adequacy route in `proofs/p2_closure_audit.json`. The separate chapter dossiers remain under `evidence_quality/proof_model_dossiers/`. Downstream executable, empirical, reproduction, and transfer routes remain mandatory; closure does not promote support.
"""
    return registry, report, dossiers


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    registry, report, dossiers = build()
    if args.check:
        errors: list[str] = []
        if not REGISTRY.exists() or load(REGISTRY) != registry:
            errors.append("proof rationalization registry is stale")
        if not REPORT.exists() or REPORT.read_text(encoding="utf-8") != report:
            errors.append("proof rationalization report is stale")
        for chapter_id, body in dossiers.items():
            path = DOSSIERS / f"{chapter_id}.md"
            if not path.exists() or path.read_text(encoding="utf-8") != body:
                errors.append(f"{chapter_id}: proof-model dossier is stale")
                break
        if errors:
            raise SystemExit("Proof rationalization build check failed:\n - " + "\n - ".join(errors))
        print(f"Proof rationalization build check passed: {len(registry['baseline_theorems'])} theorems, {len(registry['baseline_targets'])} targets.")
        return
    REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    DOSSIERS.mkdir(parents=True, exist_ok=True)
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    REPORT.write_text(report, encoding="utf-8")
    for chapter_id, body in dossiers.items():
        (DOSSIERS / f"{chapter_id}.md").write_text(body, encoding="utf-8")
    print(f"Wrote frozen proof rationalization surfaces: {len(registry['baseline_theorems'])} theorems, {len(registry['baseline_targets'])} targets, {len(dossiers)} dossiers.")


if __name__ == "__main__":
    main()

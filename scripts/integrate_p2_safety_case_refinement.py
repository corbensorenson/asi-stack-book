#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
CHAPTER = "safety-cases-and-structured-assurance"
MODULE = "AsiStackProofs.SafetyCaseRefinement"
TARGETS = {
    "lean:safety_cases.complete_case.reaches_readiness_review": "A reachable case lifecycle binds exact case, context, hazard, evidence, challenge, review, authority, and residual identity before emitting a readiness handoff that assigns no release authority.",
    "lean:safety_cases.missing_context.retains_draft": "Missing deployment context blocks the draft-to-scoped transition without mutating case state.",
    "lean:safety_cases.missing_hazard.requires_case_repair": "Missing hazard or argument structure blocks scope admission without mutating case state.",
    "lean:safety_cases.stale_evidence.requires_repair": "Missing, stale, or assumption-free evidence blocks the scoped-to-evidenced transition.",
    "lean:safety_cases.missing_countercase.requires_review": "Missing countercase review or defeater disposition blocks challenge closure.",
    "lean:safety_cases.missing_independent_review.requires_review": "Missing competence records, conflict disclosure, or independent review blocks reviewed status.",
    "lean:safety_cases.unresolved_defeater.blocks_affected_release": "An unresolved defeater blocks progression, while later invalidation requires cause, affected paths, and complete descendant invalidation before returning a readiness-bound case to challenge.",
    "lean:safety_cases.case_status.cannot_authorize_release": "Case status cannot assign support or an external effect, and missing separation between case status and decision authority rejects the readiness handoff.",
}
PREFIX = "lean/AsiStackProofs/SafetyCases.lean::"
REFS = {
    "countermodel_refs": ["lean/AsiStackProofs/SafetyCaseRefinement.lean#countermodels"],
    "mutation_refs": ["scripts/validate_safety_case_refinement.py#mutations"],
    "consumer_refs": ["docs:safety_case_refinement", "evidence_quality:model_adequacy_dossiers/safety-case-refinement.md"],
    "runtime_consumer_refs": ["scripts/validate_safety_case_refinement.py", "schemas/safety_case_refinement.schema.json", "experiments/safety_case_refinement/results/2026-07-15-local.json", "scripts/validate_safety_case_assurance.py"],
    "replacement_refs": ["proof-model:safety-case-refinement.v1", "lean/AsiStackProofs/SafetyCaseRefinement.lean"],
}


def attach(row: dict) -> None:
    for key, values in REFS.items():
        row[key] = list(dict.fromkeys([*row.get(key, []), *values]))


def main() -> None:
    structure = json.loads(STRUCTURE.read_text())
    chapter = next(chapter for part in structure["parts"] for chapter in part["chapters"] if chapter["id"] == CHAPTER)
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE
            target["target"] = TARGETS[target["tag"]]
    chapter["lean_module"] = "AsiStackProofs.SafetyCases; AsiStackProofs.SafetyCaseRefinement"
    chapter["codex_tests"] = [item for item in chapter["codex_tests"] if not (isinstance(item, dict) and item.get("name") == "Safety-case lifecycle refinement")]
    chapter["codex_tests"].append({
        "name": "Safety-case lifecycle refinement", "implementation_status": "implemented",
        "result_status": "passes the exact eight-case suite, 30 routes, six reachable stages, and 35/35 rejecting mutations; one readiness handoff is invalidated back to challenge with no support or external effect; no argument-truth, hazard-completeness, evidence-adequacy, reviewer-independence, safety, readiness, deployed-invalidation, transfer, or support claim",
    })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n")

    triage = json.loads(TRIAGE.read_text())
    for row in triage["records"]:
        if row["tag"] in TARGETS:
            row["module"] = MODULE
            row["formal_target"] = TARGETS[row["tag"]]
            row["rationale"] = "Reachable six-stage safety-case lifecycle with exact custody, explicit readiness/invalidation boundaries, 30 routes, 35 rejecting mutations, and no support/effect authority."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n")

    reviews = json.loads(REVIEWS.read_text())
    for target in TARGETS:
        row = reviews["target_reviews"][target]
        attach(row)
        row["semantic_role"] = "Reachable draft-to-readiness safety-case lifecycle with exact identity custody and explicit challenge re-entry after descendant-aware invalidation."
        row["assumptions"] = ["Case/version, context, claim, hazard, evidence, countercase, reviewer, authority, residual, affected-path, and invalidation-completeness records are trusted inside the finite authored model."]
        row["excluded_effects"] = ["Argument truth, hazard completeness, causal relevance, evidence adequacy, reviewer competence or independence, control effectiveness, safety, readiness, release authority, deployed invalidation, transfer, and chapter-core support are excluded."]
        row["review_rationale"] = "Strengthen isolated route reductions with a reachable lifecycle, independent replay, thirty routes, descendant-aware invalidation, and 35 rejecting mutations."
    theorem_ids = [key for key in reviews["theorem_reviews"] if key.startswith(PREFIX)]
    for theorem_id in theorem_ids:
        attach(reviews["theorem_reviews"][theorem_id])
    REVIEWS.write_text(json.dumps(reviews, indent=2) + "\n")
    print(f"Integrated Safety Case refinement across {len(TARGETS)} targets and {len(theorem_ids)} frozen declarations.")


if __name__ == "__main__":
    main()

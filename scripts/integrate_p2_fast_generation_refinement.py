#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
MODULE = "AsiStackProofs.FastGenerationRefinement"

TARGETS = {
    "lean:fast_generation.mode_selection.operational_invariant": "Reachable admission binds task, context, consumer, mode, risk, verifier, baseline, quality, latency, resource, fallback, and rights records before fast selection.",
    "lean:fast_generation.verified_speed.failure_blocks_promotion": "Reachable accounting and decision routes block raw-speed promotion without accepted output, task success, matched baseline, complete costs, and an evidence transition.",
    "lean:fast_generation.mode_admission_lifecycle_route": "Eight stages and sixty independently consumed routes govern context binding, selection, drafting, verification or fallback, useful-outcome accounting, decision, and closure.",
    "lean:fast_generation.theseus_import_fixture_bridge": "A digest-bound external validator owns Theseus report counts while Lean owns general reachable raw-speed, fallback, promotion, and closure policy.",
    "lean:fast_generation.task_bundle_fixture_bridge": "A digest-bound external validator owns the three-route task result while Lean owns general task-success, cost-separation, speed-proxy, support-transition, and closure policy.",
}
PREFIX = "lean/AsiStackProofs/FastGeneration.lean::"
RETAINED_NAMES = {
    "promotion_candidate_missing_accepted_output_or_verifier_cost_rejected",
    "failed_acceptance_without_fallback_or_residual_rejected",
    "high_risk_fast_mode_without_verifier_or_override_rejected",
}
REFS = {
    "countermodel_refs": ["lean/AsiStackProofs/FastGenerationRefinement.lean#countermodels"],
    "mutation_refs": ["scripts/validate_fast_generation_refinement.py#route_cases"],
    "consumer_refs": ["docs:fast_generation_refinement", "evidence_quality:model_adequacy_dossiers/fast-generation-refinement.md"],
    "runtime_consumer_refs": [
        "scripts/validate_fast_generation_refinement.py",
        "schemas/fast_generation_refinement.schema.json",
        "experiments/fast_generation_refinement/results/2026-07-15-local.json",
        "scripts/validate_generation_mode_baselines.py",
        "scripts/validate_fast_generation_task_bundle.py",
        "scripts/validate_theseus_generation_mode_import.py",
    ],
    "replacement_refs": ["proof-model:fast-generation.request-to-closure-refinement.v1", "lean/AsiStackProofs/FastGenerationRefinement.lean"],
}


def attach(record: dict) -> None:
    for key, refs in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *refs]))


def main() -> None:
    structure = json.loads(STRUCTURE.read_text(encoding="utf-8"))
    chapter = next(c for part in structure["parts"] for c in part["chapters"] if c["id"] == "fast-generation-architectures")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE
            target["target"] = TARGETS[target["tag"]]
    chapter["lean_module"] = "AsiStackProofs.FastGeneration; AsiStackProofs.FastGenerationRefinement"
    chapter["minimal_implementation"] = (
        "The current minimum contains three retained finite countermodels plus a seventeen-declaration, eight-stage, sixty-route request-to-closure lifecycle; an independent consumer rejecting 51/51 non-accepting mutations and digest-binding the two-valid/four-invalid baseline suite, three-route/four-task accounting bundle, and one-valid/six-invalid Theseus import; one reachable modeled fallback; and no support or external effect. Thirty-five assumed projections, copied fixture facts, and summary bridges are retired. This is bounded local policy/conformance evidence, not model speed, natural-workload usefulness, verifier independence, evaluator adequacy, deployed fallback, serving performance, transfer, or SOTA evidence."
    )
    retired_tests = {
        "Generation-mode admission lifecycle route",
        "Project Theseus generation-mode import validation",
        "Fast generation public-safe task bundle",
    }
    chapter["codex_tests"] = [
        row for row in chapter["codex_tests"]
        if not (isinstance(row, dict) and row.get("name") in retired_tests)
    ]
    chapter["codex_tests"].append({
        "name": "Fast Generation request-to-closure lifecycle refinement",
        "implementation_status": "implemented",
        "result_status": "passes eight stages, all sixty routes, 51/51 non-accepting mutations, three digest-bound bounded suites, one reachable modeled fallback, and support/effect none; no model-speed, useful-throughput, deployed-fallback, serving, transfer, or support claim",
    })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n", encoding="utf-8")

    triage = json.loads(TRIAGE.read_text(encoding="utf-8"))
    for record in triage["records"]:
        if record["tag"] in TARGETS:
            record["module"] = MODULE
            record["formal_target"] = TARGETS[record["tag"]]
            record["rationale"] = "Reachable eight-stage request-to-closure lifecycle, sixty routes, 51 rejecting mutations, three digest-bound bounded suites, and no support/effect authority."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n", encoding="utf-8")

    reviews = json.loads(REVIEWS.read_text(encoding="utf-8"))
    for tag in TARGETS:
        target = reviews["target_reviews"][tag]
        attach(target)
        target["semantic_role"] = "Reachable task/context binding, route admission, generation, verification or fallback, cost/usefulness accounting, evidence decision, and closure lifecycle."
        target["assumptions"] = ["All identities, policy gates, verifier outcomes, task-success fields, costs, baseline facts, evidence-transition facts, consumer acknowledgments, residuals, and digests are trusted inside the finite authored model."]
        target["excluded_effects"] = ["Model speed, output quality, task utility, verifier correctness or independence, deployed fallback, serving behavior, causal attribution, transfer, SOTA, and support are excluded."]
        target["review_rationale"] = "Replace projections and copied report facts with a reachable lifecycle plus an independently implemented digest-bound consumer."

    baseline_ids = [key for key in reviews["theorem_reviews"] if key.startswith(PREFIX)]
    retired = 0
    for key in baseline_ids:
        record = reviews["theorem_reviews"][key]
        attach(record)
        if key.rsplit("::", 1)[1] not in RETAINED_NAMES:
            retired += 1
            record["review_state"] = "terminally_dispositioned"
            record["disposition"] = "replace_with_stronger_model"
            record["review_rationale"] = "Frozen lineage retained; declaration physically retired because it projected an assumed predicate, unfolded one authored fixture, or copied a result fact now subsumed by the reachable refinement and independent consumer."
    REVIEWS.write_text(json.dumps(reviews, indent=2) + "\n", encoding="utf-8")
    print(f"Integrated Fast Generation refinement across {len(TARGETS)} targets and {len(baseline_ids)} frozen declarations; {retired} retired and {len(RETAINED_NAMES)} retained.")


if __name__ == "__main__":
    main()

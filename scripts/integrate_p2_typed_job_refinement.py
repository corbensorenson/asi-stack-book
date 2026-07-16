#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
MODULE = "AsiStackProofs.TypedJobRefinement"
PREFIX = "lean/AsiStackProofs/TypedJobs.lean::"
TARGETS = {
    "lean:jobs.lifecycle.operational_invariant": "A reachable versioned typed-job lifecycle preserves exact job, contract, plan, authority, permission, lease, scheduler, and consumer custody from lock through acknowledged closure without assigning support or external effects.",
    "lean:jobs.lifecycle.failure_blocks_promotion": "Approval, permission, lease, scheduler, retry/idempotency, cancellation, artifact/audit, verification, completion/replay, residual-owner, and consumer-acknowledgment failures block lifecycle progress.",
    "lean:jobs.lifecycle.execution_route_envelope": "An independent consumer covers twenty-eight typed-job lifecycle routes and rejects 42 identity, ordering, authority, approval, permission, lease, retry, cancellation, artifact, audit, adjudication, receipt, replay, residual, and acknowledgment mutations.",
    "lean:jobs.lifecycle.delivery_probe_fixture_bridge": "The versioned lifecycle consumer preserves the exact two-valid/seven-invalid typed-job delivery suite without treating delivery or verification fields as task success, output truth, support, or external effects.",
    "lean:jobs.lifecycle.durable_lifecycle_probe_bridge": "The versioned lifecycle consumer preserves the exact two-valid/nine-invalid durable retry and lease suite without treating declared idempotence, recovery, enforcement, receipt, or replay fields as real service behavior.",
}
RETIRED = {
    PREFIX + "recorded_valid_job_transition_uses_declared_lifecycle_relation",
    PREFIX + "typed_job_delivery_probe_fixture_bridge",
    PREFIX + "typed_job_durable_lifecycle_probe_fixture_bridge",
}
REFS = {
    "countermodel_refs": ["lean/AsiStackProofs/TypedJobRefinement.lean#countermodels"],
    "mutation_refs": ["scripts/validate_typed_job_refinement.py#mutations"],
    "consumer_refs": ["docs:typed_job_refinement", "evidence_quality:model_adequacy_dossiers/typed-job-refinement.md"],
    "runtime_consumer_refs": [
        "scripts/validate_typed_job_refinement.py", "schemas/typed_job_refinement.schema.json",
        "experiments/typed_job_refinement/results/2026-07-15-local.json",
        "scripts/validate_typed_job_delivery_probe.py", "scripts/validate_typed_job_durable_lifecycle_probe.py",
    ],
    "replacement_refs": ["proof-model:typed-job.versioned-execution-closure-refinement.v1", "lean/AsiStackProofs/TypedJobRefinement.lean"],
}


def attach(record: dict) -> None:
    for key, values in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *values]))


def main() -> None:
    structure = json.loads(STRUCTURE.read_text())
    chapter = next(c for p in structure["parts"] for c in p["chapters"] if c["id"] == "labor-os-and-typed-jobs")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE
            target["target"] = TARGETS[target["tag"]]
    chapter["lean_module"] = "AsiStackProofs.TypedJobs; AsiStackProofs.TypedJobRefinement"
    chapter["codex_tests"] = [
        row for row in chapter["codex_tests"]
        if not (isinstance(row, dict) and row.get("name") in {"Typed job lifecycle test", "Job execution route proof", "Typed-job versioned execution and closure refinement"})
    ]
    chapter["codex_tests"].append({
        "name": "Typed-job versioned execution and closure refinement",
        "implementation_status": "implemented",
        "result_status": "passes exact 2/7 delivery and 2/9 durable suites, 28 routes, seven reachable stages, and 42/42 rejecting mutations; support-state effect none; no deployed scheduler, enforcement, recovery, task-success, truth, usefulness, safety, reproduction, or transfer claim",
    })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n")

    triage = json.loads(TRIAGE.read_text())
    for target in triage["records"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE
            target["formal_target"] = TARGETS[target["tag"]]
            target["rationale"] = "Reachable seven-stage typed-job lifecycle with exact identity custody, bounded failure routes, exact legacy-suite consumption, 42 rejecting mutations, and no support or external-effect authority."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n")

    reviews = json.loads(REVIEWS.read_text())
    for target_id in TARGETS:
        record = reviews["target_reviews"][target_id]
        attach(record)
        record["semantic_role"] = "Reachable versioned contract-lock, authorization, dispatch, execution-observation, adjudication, and acknowledged-closure lifecycle with exact custody and no support/effect authority."
        record["assumptions"] = ["Job, contract, plan, authority, permission, lease, scheduler, approval, retry, cancellation, artifact, audit, verification, receipt, replay, residual, and acknowledgment fields are trusted inside the finite authored model."]
        record["excluded_effects"] = ["Scheduler quality, task success, output truth, verification soundness, idempotence or enforcement in fact, durable recovery, cancellation efficacy, receipt/replay truth, usefulness, causality, safety, deployment, reproduction, transfer, SOTA, and chapter-core support are excluded."]
        record["review_rationale"] = "Replace record-validity and summary projections with a reachable versioned lifecycle, exact 2/7 and 2/9 suites, twenty-eight routes, 42 rejecting mutations, and explicit residual/consumer closure custody."
    theorem_ids = [key for key in reviews["theorem_reviews"] if key.startswith(PREFIX)]
    for theorem_id in theorem_ids:
        attach(reviews["theorem_reviews"][theorem_id])
    for theorem_id in RETIRED:
        record = reviews["theorem_reviews"][theorem_id]
        record["review_state"] = "terminally_dispositioned"
        record["disposition"] = "replace_with_stronger_model"
        record["review_rationale"] = "Frozen lineage retained; declaration physically retired because it projected a validity predicate or copied a generic fixture summary now subsumed by the reachable versioned execution/closure refinement."
    REVIEWS.write_text(json.dumps(reviews, indent=2) + "\n")
    print(f"Integrated typed-job refinement across 5 targets and {len(theorem_ids)} frozen declarations; 3 declarations retired.")


if __name__ == "__main__": main()

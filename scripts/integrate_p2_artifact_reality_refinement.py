#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STRUCTURE = ROOT / "book_structure.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
REVIEWS = ROOT / "proofs/proof_rationalization_reviews.json"
MODULE = "AsiStackProofs.ArtifactRealityRefinement"
PREFIX = "lean/AsiStackProofs/ArtifactGraph.lean::"
TARGETS = {
    "lean:artifacts.graph.operational_invariant": "A reachable artifact lifecycle preserves exact artifact, content, parent-job, source, context, transaction, certificate, tool, claim, test, policy, and consumer custody from registration through consumer-acknowledged admission without assigning support or external effects.",
    "lean:artifacts.graph.failure_blocks_promotion": "Missing provenance, replay, observation, cross-check, trap, attestation-limit, trust-root, verifier-separation, recursion-stop, residual, revocation, or consumer obligations block lifecycle progress.",
    "lean:artifacts.graph.replay_packet_bridge": "The refinement preserves exact replay-packet custody and requires replay metadata, sufficient grade, limits, active certificates, and replay validation before reality review.",
    "lean:artifacts.graph.record_reality_sequence_bridge": "The independent consumer preserves the exact one-valid/four-invalid stale/partial/fresh record-reality sequence without assigning support.",
    "lean:artifacts.graph.receipt_faithfulness_fixture_bridge": "The independent consumer preserves the exact three-valid/six-invalid receipt-faithfulness suite while requiring observation, independent cross-checks, trap challenges, and bounded attestation.",
    "lean:artifacts.graph.receipt_repository_audit_fixture_bridge": "The independent consumer preserves the exact four-record/five-mutation repository audit while treating current digest and command checks as bounded observations rather than open-world truth.",
    "lean:artifacts.graph.receipt_repository_challenge_fixture_bridge": "The independent consumer preserves the exact four-response/five-mutation deterministic repository challenge while bounding fingerprint and digest observations to the sampled artifacts.",
    "lean:artifacts.graph.live_attestation_probe_bridge": "The independent consumer preserves one-artifact live attestation with three observation routes and seven mutations without treating a dirty or uncommitted target as attested.",
    "lean:artifacts.graph.randomized_attestation_audit_bridge": "The independent consumer preserves the four-artifact randomized attestation with twelve accepted observation routes and eight mutations without generalizing beyond the sample.",
    "lean:artifacts.graph.epistemic_tcb_fixture_bridge": "The independent consumer preserves the exact three-valid/six-invalid epistemic-TCB suite while requiring a bounded trusted core, roots, verifier separation, recursion stop, and outside-TCB residuals.",
}
RETIRED_NAMES = {
    "produced_artifact_records_parent_job_and_context_refs",
    "artifact_record_reality_sequence_fixture_bridge",
    "receipt_faithfulness_adversarial_fixture_bridge",
    "receipt_repository_audit_fixture_bridge",
    "receipt_repository_challenge_fixture_bridge",
    "artifact_live_attestation_probe_bridge",
    "artifact_randomized_attestation_audit_bridge",
    "epistemic_tcb_fixture_bridge",
}
RETIRED = {PREFIX + name for name in RETIRED_NAMES}
REFS = {
    "countermodel_refs": ["lean/AsiStackProofs/ArtifactRealityRefinement.lean#countermodels"],
    "mutation_refs": ["scripts/validate_artifact_reality_refinement.py#mutations"],
    "consumer_refs": ["docs:artifact_reality_refinement", "evidence_quality:model_adequacy_dossiers/artifact-reality-refinement.md"],
    "runtime_consumer_refs": [
        "scripts/validate_artifact_reality_refinement.py", "schemas/artifact_reality_refinement.schema.json",
        "experiments/artifact_reality_refinement/results/2026-07-15-local.json",
        "scripts/validate_artifact_graph_replay.py", "scripts/validate_artifact_graph_record_reality_sequence.py",
        "scripts/validate_receipt_faithfulness.py", "scripts/validate_receipt_repository_audit.py",
        "scripts/validate_receipt_repository_challenge.py", "scripts/validate_artifact_live_attestation_probe.py",
        "scripts/validate_artifact_randomized_attestation_audit.py", "scripts/validate_epistemic_trusted_computing_base.py",
    ],
    "replacement_refs": ["proof-model:artifact.record-reality-trust-refinement.v1", "lean/AsiStackProofs/ArtifactRealityRefinement.lean"],
}


def attach(record: dict) -> None:
    for key, values in REFS.items():
        record[key] = list(dict.fromkeys([*record.get(key, []), *values]))


def main() -> None:
    structure = json.loads(STRUCTURE.read_text())
    chapter = next(c for p in structure["parts"] for c in p["chapters"] if c["id"] == "artifact-graphs-audit-logs-and-replay")
    for target in chapter["proof_targets"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE; target["target"] = TARGETS[target["tag"]]
    chapter["lean_module"] = "AsiStackProofs.ArtifactGraph; AsiStackProofs.ArtifactRealityRefinement"
    chapter["codex_tests"] = [row for row in chapter["codex_tests"] if not (isinstance(row, dict) and row.get("name") == "Artifact record-reality and trust refinement")]
    chapter["codex_tests"].append({
        "name": "Artifact record-reality and trust refinement", "implementation_status": "implemented",
        "result_status": "passes eight exact bounded suites, 33 routes, seven reachable stages, and 53/53 rejecting mutations; support-state effect none; no open-world provenance, artifact truth, replay correctness, external independence, deployed revocation, usefulness, safety, reproduction, or transfer claim",
    })
    STRUCTURE.write_text(json.dumps(structure, indent=2) + "\n")

    triage = json.loads(TRIAGE.read_text())
    for target in triage["records"]:
        if target["tag"] in TARGETS:
            target["module"] = MODULE; target["formal_target"] = TARGETS[target["tag"]]
            target["rationale"] = "Reachable seven-stage artifact record-reality lifecycle with exact identity custody, eight bounded suites, 33 routes, 53 rejecting mutations, and no support or external-effect authority."
    TRIAGE.write_text(json.dumps(triage, indent=2) + "\n")

    reviews = json.loads(REVIEWS.read_text())
    for target_id in TARGETS:
        record = reviews["target_reviews"][target_id]; attach(record)
        record["semantic_role"] = "Reachable registration, provenance, replay, reality-cross-check, trust-base, revocation, and consumer-admission lifecycle with exact custody and no support/effect authority."
        record["assumptions"] = ["Artifact identities, digests, reference presence, replay grades, certificate state, validation, observation, cross-check, trap, attestation, trust-root, verifier, recursion, residual, revocation, and acknowledgment fields are trusted inside the finite authored model."]
        record["excluded_effects"] = ["Open-world provenance, causal truth, artifact/source/content correctness, replay semantics, verifier correctness, external independence, root security, repository completeness, deployed propagation, usefulness, causality, safety, reproduction, transfer, SOTA, and chapter-core support are excluded."]
        record["review_rationale"] = "Replace one projection and seven copied fixture summaries with a reachable record-reality lifecycle, eight exact bounded suites, thirty-three routes, 53 rejecting mutations, and explicit trust/revocation/consumer custody."
    theorem_ids = [key for key in reviews["theorem_reviews"] if key.startswith(PREFIX)]
    for theorem_id in theorem_ids: attach(reviews["theorem_reviews"][theorem_id])
    for theorem_id in RETIRED:
        record = reviews["theorem_reviews"][theorem_id]
        record["review_state"] = "terminally_dispositioned"; record["disposition"] = "replace_with_stronger_model"
        record["review_rationale"] = "Frozen lineage retained; declaration physically retired because it projected a predicate or normalized a hand-authored fixture summary now subsumed by the reachable artifact record-reality refinement."
    REVIEWS.write_text(json.dumps(reviews, indent=2) + "\n")
    print(f"Integrated artifact-reality refinement across 10 targets and {len(theorem_ids)} frozen declarations; 8 declarations retired.")


if __name__ == "__main__": main()

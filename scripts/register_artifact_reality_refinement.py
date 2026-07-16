#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_artifact_reality_refinement.py"
ARTIFACTS = [
    "scripts/validate_artifact_reality_refinement.py", "schemas/artifact_reality_refinement.schema.json",
    "experiments/artifact_reality_refinement/results/2026-07-15-local.json", "docs/artifact_reality_refinement.md",
    "evidence_quality/model_adequacy_dossiers/artifact-reality-refinement.md", "lean/AsiStackProofs/ArtifactRealityRefinement.lean",
    "scripts/validate_artifact_graph_replay.py", "experiments/artifact_graph_replay/fixtures",
    "scripts/validate_artifact_graph_record_reality_sequence.py", "experiments/artifact_graph_record_reality_sequence/results/2026-07-04-local.json",
    "scripts/validate_receipt_faithfulness.py", "experiments/receipt_faithfulness/results/2026-07-03-local.json",
    "scripts/validate_receipt_repository_audit.py", "experiments/receipt_repository_audit/results/2026-07-03-local.json",
    "scripts/validate_receipt_repository_challenge.py", "experiments/receipt_repository_audit/results/2026-07-04-challenge.json",
    "scripts/validate_artifact_live_attestation_probe.py", "experiments/artifact_live_attestation/results/2026-07-04-local.json",
    "scripts/validate_artifact_randomized_attestation_audit.py", "experiments/artifact_randomized_attestation/results/2026-07-04-local.json",
    "scripts/validate_epistemic_trusted_computing_base.py", "experiments/epistemic_tcb/results/2026-07-03-local.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text()); value["units"] = [u for u in value["units"] if u.get("script") != SCRIPT]
    order = len(value["units"]) + 1
    value["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [], "execution_tier": "deep", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Reachable Lean artifact record-reality lifecycle, eight exact bounded suites, independent consumer, result schema, receipt, and model-adequacy dossier.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject artifact or lineage substitution, replay, authority leakage, provenance gaps, inadequate replay, missing observations/cross-checks/traps/limits, trust-root or verifier laundering, missing recursion/residual/revocation/consumer custody.",
        "output_assertions": ["eight exact bounded suites", "thirty-three routes and seven reachable stages", "fifty-three rejected lifecycle mutations", "one represented reality observation", "no support-state or external-effect authority"],
        "claim_scope": "One finite authored artifact record-reality lifecycle plus eight existing bounded local/synthetic suites only.",
        "negative_controls": "validator_owned_identity_lineage_replay_reality_trust_revocation_mutations",
        "negative_control_cases": ["artifact, content, parent, source, context, transaction, certificate, tool, claim, test, policy, consumer, or event substitution", "provenance, replay, observation, cross-check, trap, or attestation-limit gap", "missing trusted core, root, verifier separation, recursion stop, or outside-TCB residual", "incomplete revocation closure or consumer acknowledgment", "support assignment or external-effect authority leak"],
        "prohibited_inference": "Does not establish open-world provenance, causal truth, artifact/source/content correctness, replay correctness, verifier correctness, external independence, root security, repository completeness, deployed propagation, usefulness, causality, safety, reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "inherited", "semantic_review_state": "checked_structured_artifact_record_reality_trust_lifecycle_not_open_world_truth_replay_deployed_or_support_authority",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required: required.append(artifact)
    value["required_artifacts"] = required; value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__": main()

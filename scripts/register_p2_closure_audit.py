#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_p2_closure_audit.py"
ARTIFACTS = [
    "scripts/validate_p2_closure_audit.py",
    "proofs/p2_closure_audit.json",
    "proofs/proof_rationalization_registry.json",
    "proofs/proof_semantic_rationalization_ledger.json",
    "proofs/proof_manifest.json",
    "proofs/proof_triage.json",
    "docs/proof_adequacy_review.md",
    "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(
        index for index in range(1, len(value["units"]) + 2) if index not in used
    )
    value["units"].append(
        {
            "id": f"{SCRIPT}:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "pr",
            "validation_class": "proof_or_evidence_gate",
            "input_contract": "Frozen P2 proof rationalization, current proof manifest and triage, executed semantic-rationalization target migrations, adequacy routes, ten safety-critical/integration/refinement dossiers and registered consumers, and canonical roadmap state.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Reject incomplete proof dispositions, target or adequacy-route gaps, unauthorized implemented-to-planned migration, missing semantic-model dossiers/consumers, false P2/M3 closure, and support-state laundering.",
            "output_assertions": [
                "1,151/1,151 activation-baseline theorem declarations and 298/298 baseline targets are reviewed and dispositioned",
                "298/298 historical proof targets remain implemented and explicitly adequacy-routed",
                "324 current targets comprise 318 implemented and 6 planned, including the consumer-owned Failure Modes, Governed Operations, Learned Objective Integrity, Observation Trust, Search Substrate, Artifact Steward, Human-AI Organizations, Multi-Agent Dynamics, Embodied Physical Safety, Dangerous Capability Review, Military Interaction Review, Open-Weight Release Review, Communication Influence Review, Objective Lease Governance, Adversarial Model Security, Protected Computation Review, Content Authenticity Review, Replication Containment Review, Institutional Legitimacy Review, Societal Resilience Review, and Durable Semantic Memory Review refinements",
                "the thirty-two richer-semantics targets remain bounded and route to P3/P4 rather than disappearing",
                "ten required safety-critical, integration, and review-named refinement models have dossiers and registered consumers",
                "P2/M3 is completed, P3 is active, and prerequisite M2 is active without support-state movement",
            ],
            "claim_scope": "Completeness and routing of the P2 formal-proof program; not truth of chapter-core, deployed, empirical, causal, reproduction, transfer, or SOTA claims.",
            "negative_controls": "validator_owned_support_baseline_route_richer_semantics_model_and_state_mutations",
            "negative_control_cases": [
                "support-state promotion laundering",
                "activation-baseline target deletion",
                "unrouted richer-semantics class",
                "richer-semantics target-count laundering",
                "required semantic-model omission",
                "false P2 closure state",
            ],
            "prohibited_inference": "Does not establish deployed behavior, effect-complete rollback, evaluator competence, useful throughput, safety, economic optimality, reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.",
            "contract_precision": "exact",
            "semantic_review_state": "checked_complete_formal_disposition_and_forward_routing_not_downstream_evidence_completion",
        }
    )
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {
        "required_artifact_count": len(required),
        "unit_count": len(value["units"]),
    }
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()

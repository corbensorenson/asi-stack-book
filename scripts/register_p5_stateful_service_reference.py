#!/usr/bin/env python3
"""Register the P5 stateful-service reference validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p5_stateful_service_reference.py"
ARTIFACTS = [
    "experiments/effect_complete_service/cases.json",
    "experiments/effect_complete_service/results/2026-07-27-local.json",
    "schemas/effect_complete_service_result.schema.json",
    "scripts/run_p5_stateful_service_reference.py",
    "scripts/validate_p5_stateful_service_reference.py",
    "docs/p5_stateful_service_reference_report.md",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [
        unit for unit in registry["units"] if unit.get("script") != SCRIPT
    ]
    order = len(registry["units"]) + 1
    registry["units"].append(
        {
            "id": f"validate_p5_stateful_service_reference:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "deep",
            "validation_class": "behavioral_fixture",
            "input_contract": (
                "Frozen seven-case service design, commit-bound Python source, "
                "actual linear-model and Adam learning state, prospective "
                "nine-class checkpoint, separate localhost HTTP effect process "
                "and SQLite ledger, durable outbox, and independent observer process."
            ),
            "input_artifacts": ARTIFACTS,
            "output_contract": (
                "Freshly replay all cases and reject learning-control, full-state, "
                "restart, partition, idempotency, revocation, custody, observation, "
                "claim-boundary, schema, source-identity, or receipt drift."
            ),
            "output_assertions": [
                "seven of seven bounded service cases pass",
                "actual model and Adam state improve the authored positive control",
                "all nine state classes mutate",
                "weights-only rollback is rejected",
                "a new process restores nine classes and prior prediction exactly",
                "one partitioned effect remains in an owned outbox",
                "retry produces exactly one external effect",
                "duplicate and revoked retries produce no additional effect",
                "weight and dependency tampering are rejected",
                "a separate observer process reads the effect",
                "source identity binds an exact commit on main",
                "no support-state or release effect",
            ],
            "claim_scope": (
                "The exact authored scalar-model, Python/stdlib, localhost HTTP, "
                "SQLite, and local-filesystem service lifecycle at the attested commit."
            ),
            "negative_controls": (
                "weights_only_restore_partition_duplicate_revocation_weight_tamper_"
                "dependency_tamper_and_deployment_claim_boundary"
            ),
            "negative_control_cases": [
                "weights-only rollback",
                "unavailable external service",
                "duplicate effect retry",
                "revoked credential",
                "tampered model weights",
                "tampered dependency lock",
                "local source attestation presented as deployment",
            ],
            "prohibited_inference": (
                "The slice does not establish natural-task usefulness, large-model "
                "semantic recovery, production or open-network correctness, distributed "
                "consensus, Byzantine tolerance, privacy repair, causal unlearning, "
                "external erasure, legal compliance, independent external reproduction, "
                "transfer, SOTA, AGI, ASI, chapter-core support, deployment, or release."
            ),
            "contract_precision": "exact",
            "semantic_review_state": (
                "bounded_stateful_local_service_mechanism_not_natural_or_deployed"
            ),
        }
    )
    required = list(registry["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    registry["required_artifacts"] = required
    registry["summary"] = {
        "required_artifact_count": len(required),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(registry['units'])} units.")


if __name__ == "__main__":
    main()

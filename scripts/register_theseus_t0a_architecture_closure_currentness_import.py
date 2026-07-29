#!/usr/bin/env python3
"""Register the Theseus T0A currentness validator and its contract."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_theseus_t0a_architecture_closure_currentness_import.py"
ARTIFACTS = [
    "scripts/build_theseus_t0a_architecture_closure_currentness_import.py",
    "scripts/validate_theseus_t0a_architecture_closure_currentness_import.py",
    "experiments/theseus_t0a_architecture_closure_currentness_import/results/2026-07-27-local.json",
    "docs/theseus_t0a_architecture_closure_currentness_import.md",
]
FIELDS = [
    "input_contract",
    "input_artifacts",
    "output_contract",
    "output_assertions",
    "claim_scope",
    "negative_controls",
    "negative_control_cases",
    "prohibited_inference",
    "contract_precision",
    "semantic_review_state",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    unit = next(
        (
            row
            for row in registry["units"]
            if row["script"] == SCRIPT and row.get("args", []) == []
        ),
        None,
    )
    if unit is None:
        order = len(registry["units"]) + 1
        unit = {
            "id": f"{SCRIPT.removesuffix('.py')}:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
        }
        registry["units"].append(unit)
    spec = {
        "execution_tier": "deep",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "One clean published Project Theseus main snapshot, twelve exact file digests, the historical 143-artifact T0A freeze transaction, explicit T0/T0A/T1/T2 states, exact step-9048 model/optimizer/RNG/receipt/plan identities, explicit unavailable step-3480 payload and predecessor-chain flags, a prospective append-only segment-lineage contract, lifecycle-aware currentness gate, evaluator non-consumption, public-safety filter, and no capability/support/release effect.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject source-authority drift, origin-main publication erasure, T0A reopening, T1 reblocking after published activation, T2 activation without behavior, pre-anchor chain or payload invention, anchor/model/optimizer/receipt identity drift, plan-migration or append-only-custody erasure, evaluator-consumption or capability invention, training-launch invention, private copying, support promotion, or release promotion.",
        "output_assertions": [
            "clean 264a31ee main authority published on origin/main",
            "zero commits ahead of origin/main",
            "T0 historical control complete",
            "T0A historical freeze complete with explicit later T1 custody residual",
            "T1 active at exact step 9048 and 69310840 of 1096734920 pretraining positions",
            "T2 blocked until source-disjoint model-only behavior",
            "historical freeze binds 143 artifacts, 15 of 15 contracts, 14 accelerator receipts, and seven of seven CPU replays",
            "the exact step-3480 payload and full step-3480-to-9048 predecessor chain are unavailable",
            "the current model, optimizer, RNG, receipt, stage, and migrated plan identities are exact",
            "every later state-changing segment must publish to the append-only lineage ledger before another launch",
            "private development evaluator freeze v5 is green and unconsumed",
            "141 affected tests passed with 18 hardware-dependent skips",
            "zero protected outcomes/support/release movement",
            "eighteen rejecting mutations",
        ],
        "claim_scope": "Exact sanitized cross-repository dependency and architecture-freeze currentness observation only.",
        "negative_controls": "validator_owned_and_import_bound",
        "negative_control_cases": [
            "source commit substitution",
            "origin-main publication erasure",
            "T0A reopened",
            "T1 reblocked after published activation",
            "T2 unblocked without behavior",
            "pre-anchor predecessor-chain invention",
            "step-3480 payload-availability invention",
            "anchor-step drift",
            "checkpoint-identity drift",
            "optimizer-identity drift",
            "receipt-identity drift",
            "plan-migration erasure",
            "append-only-lineage erasure",
            "evaluator-consumption invention",
            "capability invention",
            "training-launch invention",
            "support promotion",
            "release promotion",
        ],
        "prohibited_inference": "The currentness handoff does not establish a complete pre-anchor replay chain, model behavior, capability, useful throughput, safety, deployment, transfer, AGI, ASI, SOTA, or any support movement. The custody gap is not architecture or optimizer counterevidence.",
        "contract_precision": "exact",
        "semantic_review_state": "internal_public_safe_cross_repository_currentness_audit_not_independent",
    }
    unit.update(spec)
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    overrides["contracts"] = [
        row
        for row in overrides["contracts"]
        if not (row["script"] == SCRIPT and row.get("args", []) == [])
    ]
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(
        json.dumps(registry, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    OVERRIDES.write_text(
        json.dumps(overrides, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(
        f"registered Theseus T0A currentness validator: "
        f"{registry['summary']['unit_count']} units"
    )


if __name__ == "__main__":
    main()

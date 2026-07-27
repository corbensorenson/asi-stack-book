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
        "input_contract": "One clean published Project Theseus main snapshot, nineteen exact file digests including the calibrated contract owner and rejecting tests, historical 123-artifact T0 package currentness comparison, explicit T0/T0A/T1 states, seven CPU/governance replay receipts, the fourteen-receipt accelerator denominator with one exact guarded live-memory-reserve stop, one GREEN registry receipt, public-safety filter, and no outcome/support/release effect.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject source-authority drift, origin-main publication erasure, historical-package denominator shrinkage, stale-package currentness laundering, premature T0A/T1 progression, CPU or accelerator denominator drift, failed-shard erasure, child-start erasure, prospective launch-floor regression, failed-receipt authority elevation, protected-outcome invention, private copying, support promotion, or release promotion.",
        "output_assertions": [
            "clean 653401de main authority published on origin/main",
            "zero commits ahead of origin/main",
            "T0 complete",
            "T0A active",
            "T1 blocked by T0A",
            "99 of 123 historical package artifacts unchanged",
            "24 changed and zero missing",
            "seven of seven CPU/governance replays current and green",
            "thirteen of fourteen accelerator receipts valid",
            "optimizer-matched shard started, then the guard stopped it below its declared live-memory reserve with zero swapout growth",
            "the failed attempt has calibration authority only and binds a prospective 6144 MiB launch floor",
            "zero protected outcomes/support/release movement",
            "eighteen rejecting mutations",
        ],
        "claim_scope": "Exact sanitized cross-repository dependency and architecture-freeze currentness observation only.",
        "negative_controls": "validator_owned_and_import_bound",
        "negative_control_cases": [
            "source commit substitution",
            "dirty-worktree erasure",
            "remote-divergence erasure",
            "origin-main publication erasure",
            "changed-artifact denominator shrink",
            "stale package marked current",
            "T0A marked complete",
            "T1 unblocked",
            "CPU-replay failure invention",
            "accelerator denominator shrink",
            "invalid accelerator receipt erasure",
            "accelerator child-start erasure",
            "prospective launch-floor regression",
            "failed-receipt qualification-authority elevation",
            "protected-outcome invention",
            "private-payload copy",
            "support promotion",
            "release promotion",
        ],
        "prohibited_inference": "The currentness handoff does not establish training readiness, model behavior, capability, useful throughput, safety, deployment, transfer, AGI, ASI, SOTA, or any support movement.",
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

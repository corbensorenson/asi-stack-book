#!/usr/bin/env python3
"""Register the P5 local multi-process reference validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p5_effect_complete_reference.py"
ARTIFACTS = [
    "experiments/effect_complete_reference/cases.json",
    "experiments/effect_complete_reference/results/2026-07-27-local.json",
    "schemas/effect_complete_reference_result.schema.json",
    "scripts/run_p5_effect_complete_reference.py",
    "scripts/validate_p5_effect_complete_reference.py",
    "docs/p5_effect_complete_reference_report.md",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [
        unit for unit in registry["units"] if unit.get("script") != SCRIPT
    ]
    order = len(registry["units"]) + 1
    registry["units"].append(
        {
            "id": f"validate_p5_effect_complete_reference:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "deep",
            "validation_class": "behavioral_fixture",
            "input_contract": "Frozen eight-case design, real subprocess runner, SQLite/WAL ledger, contained filesystem effects, tracked deterministic result, schema, and bounded report.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Freshly replay all eight cases and reject authority, idempotency, crash-recovery, rollback, compensation, full-state, descendant-deletion, result, schema, or claim-boundary drift.",
            "output_assertions": [
                "eight of eight bounded local cases pass",
                "two real concurrent executor processes create one effect",
                "revoked and out-of-scope attempts create no effect",
                "one crash orphan is observed and exactly removed",
                "one irreversible history receives compensation",
                "nine state classes restore byte-exactly",
                "five local descendant storage surfaces are removed",
                "behavior influence privacy and external erasure remain separate",
                "no support-state or release effect",
            ],
            "claim_scope": "The exact deterministic Python, SQLite, subprocess, and local-filesystem vertical slice only.",
            "negative_controls": "fresh_replay_plus_revocation_scope_crash_duplicate_and_claim_axis_cases",
            "negative_control_cases": [
                "concurrent duplicate effect",
                "revoked cached epoch",
                "out-of-scope credential",
                "crash before effect receipt",
                "irreversible effect that requires compensation",
                "behavioral influence privacy and external-erasure laundering",
            ],
            "prohibited_inference": "The local slice does not establish deployed enforcement, complete effect discovery, distributed or Byzantine correctness, real model-state recovery, privacy repair, causal unlearning, external erasure, usefulness, safety, transfer, SOTA, AGI, ASI, chapter-core support, or release authority.",
            "contract_precision": "exact",
            "semantic_review_state": "bounded_real_multiprocess_local_vertical_slice_not_deployed",
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

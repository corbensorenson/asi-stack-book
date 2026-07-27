#!/usr/bin/env python3
"""Register the P5 natural publication-service development-trace validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p5_natural_publication_service_trace.py"
ARTIFACTS = [
    "experiments/p5_natural_publication_service_trace/results/2026-07-27-development.json",
    "schemas/p5_natural_publication_service_trace.schema.json",
    "scripts/validate_p5_natural_publication_service_trace.py",
    "docs/p5_natural_publication_service_development_trace.md",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [
        unit for unit in registry["units"] if unit.get("script") != SCRIPT
    ]
    order = len(registry["units"]) + 1
    registry["units"].append(
        {
            "id": f"validate_p5_natural_publication_service_trace:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "deep",
            "validation_class": "proof_or_evidence_gate",
            "input_contract": (
                "Tracked GitHub API observations for one ordinary maintained-book "
                "change, exact source/build/artifact/deploy/public-monitor identity "
                "joins, receipt-derived latency, explicit measurement coverage, and "
                "outcome-aware development-only classification."
            ),
            "input_artifacts": ARTIFACTS,
            "output_contract": (
                "Reject SHA, workflow, artifact, no-rebuild, monitor, duration, "
                "measurement-coverage, independence, held-out, support, or release-"
                "decision laundering while preserving the natural happy path only "
                "as retrospective development evidence."
            ),
            "output_assertions": [
                "source, build, deploy, artifact, and public monitor share exact custody",
                "the deploy workflow consumes the tested artifact without rebuilding",
                "receipt-derived latency fields are exact",
                "the post-deploy monitor is separate but not institutionally independent",
                "unmeasured safety, blocking, operator, compute, and rollback outcomes stay false",
                "the trace is outcome-aware and ineligible for a held-out denominator",
                "thirteen semantic mutations reject",
                "no support-state or release-decision effect",
            ],
            "claim_scope": (
                "One retrospective natural happy path for the public ASI Stack "
                "publication service at source commit "
                "5575d3cbf5f9dd9edfec8548c4279728b0da3995."
            ),
            "negative_controls": (
                "sha_build_deploy_artifact_rebuild_monitor_prospectivity_heldout_"
                "measurement_independence_support_and_release_laundering"
            ),
            "negative_control_cases": [
                "source SHA mismatch",
                "build SHA mismatch",
                "deploy SHA mismatch",
                "failed build",
                "artifact digest mismatch",
                "deploy rebuild",
                "missing monitor",
                "prospective laundering",
                "held-out laundering",
                "unsafe-release measurement invention",
                "institutional-independence laundering",
                "support promotion",
                "release-decision promotion",
            ],
            "prohibited_inference": (
                "The trace does not establish governed-operations efficacy, "
                "effect-complete rollback, production AI safety, unsafe-release or "
                "false-blocking rates, causal benefit, held-out natural-task "
                "performance, independent reproduction, transfer, SOTA, AGI, ASI, "
                "chapter-core support, or a new release decision."
            ),
            "contract_precision": "exact",
            "semantic_review_state": (
                "retrospective_natural_happy_path_development_observation_only"
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

#!/usr/bin/env python3
"""Reconcile P5 campaign artifacts into existing governed-operations gates."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
REGISTER = "scripts/register_p5_natural_stateful_service_campaign.py"

SHARED = [
    "experiments/governed_operations_argument_exit/preregistration.json",
    "schemas/governed_operations_campaign_preregistration.schema.json",
    "docs/p5_natural_stateful_service_campaign_preregistration.md",
    "docs/p7_2_t4_governed_operations_reader_integration.md",
    "evidence_quality/p7_2_t4_governed_operations_reader_integration.json",
    "docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
    "docs/repository_map.md",
    "appendices/F_changelog.qmd",
    REGISTER,
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    by_script = {row["script"]: row for row in registry["units"]}

    control = by_script["validate_governed_operations_control_contract.py"]
    control.update(
        {
            "input_contract": "One authored identity-bound authority-to-effect control case, an eleven-class packet state inventory, a prospectively frozen unexecuted five-arm/forty-task natural-service campaign with fourteen campaign state classes, and a finite authority/recovery model.",
            "output_contract": "Require five-dimensional authority narrowing, independent containment, exact state/effect reconciliation, fresh independent acceptance, qualified fallback, emergency expiry, thirteen Lean declarations, one completed development positive control, a sealed natural-task population, strong matched baseline, separate evaluator/monitor, and eighteen packet plus fifteen campaign rejecting mutations.",
            "output_assertions": [
                "1 authored safe-hold case",
                "5 authority dimensions narrow",
                "11 packet state classes",
                "14 campaign state classes",
                "5 campaign arms",
                "40 heldout tasks unopened",
                "9 competence gates",
                "13 Lean declarations",
                "33 mutations reject",
                "support/release/publication none",
            ],
            "negative_controls": "validator_owned_thirty_three_packet_and_campaign_identity_authority_containment_state_effect_acceptance_expiry_fallback_source_custody_denominator_matching_independence_and_non_authority_mutations",
            "negative_control_cases": [
                "five authority widenings",
                "identity deletion",
                "command loss",
                "cooperation dependency",
                "state omission",
                "stale acceptance",
                "dependent verifier",
                "active emergency lease",
                "fallback loss",
                "task or outcome opening",
                "denominator shrink",
                "strong baseline deletion",
                "public-effect widening",
                "independence invention",
                "T4 laundering",
                "support and release laundering",
            ],
        }
    )

    integration = by_script[
        "validate_p7_2_t4_governed_operations_reader_integration.py"
    ]
    integration.update(
        {
            "input_contract": "The admitted Operations chapter, nine exact source mappings, two implemented targets, one authored safe-hold case, one prospectively frozen five-arm/forty-task campaign with protected outcomes closed, and adjacent reader surfaces.",
            "output_contract": "Bind exact artifact digests, preserve source/proof/campaign/flagship denominators, require reader handoffs and synthesis, keep the four-chapter first tranche terminal, and reject thirteen integration mutations.",
            "output_assertions": [
                "4 first-tranche chapters terminal",
                "9 source mappings",
                "2 implemented targets",
                "13 Lean declarations",
                "authored case not flagship T4",
                "5 arms and 40 protected tasks frozen",
                "0 natural incidents",
                "13 integration mutations reject",
                "support effect none",
            ],
        }
    )

    for unit in (control, integration):
        for artifact in SHARED:
            if artifact not in unit["input_artifacts"]:
                unit["input_artifacts"].append(artifact)
    for artifact in SHARED:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)

    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(
        "Registered P5 natural stateful-service campaign: "
        f"{registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts."
    )


if __name__ == "__main__":
    main()

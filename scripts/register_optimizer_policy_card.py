#!/usr/bin/env python3
"""Register the governed optimizer-policy card validation unit."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = "validate_optimizer_policy_card.py"
REGISTER = "scripts/register_optimizer_policy_card.py"
ARTIFACTS = [
    "scripts/validate_optimizer_policy_card.py",
    "schemas/optimizer_policy_card.schema.json",
    "tests/fixtures/protocol_records/optimizer_policy_card.valid.json",
    "chapters/governed-model-training-distributed-optimization-and-scaling.qmd",
    "docs/optimizer_landscape_chapter_research_2026_07_21.md",
    "research_backlog_records/governed_optimizer_landscape_2026_07_21.json",
    "new_paper_triage_scenarios/governed_optimizer_landscape_2026_07_21.json",
]


def main() -> None:
    path = ROOT / "validation/registry.json"
    registry = json.loads(path.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    order = max(row["order"] for row in registry["units"]) + 1
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "One authored non-empirical Muon-primary/AdamW-fallback Optimizer Policy Card with exact parameter routing, state closure, schedule/update/approximation/distributed semantics, matched three-seed tuning and rescue, eight evaluation dimensions, three source records, and six non-authorities.",
        "input_artifacts": ARTIFACTS + [REGISTER],
        "output_contract": "Require explicit primary/fallback routing, complete state, content-bound Newton-Schulz approximation, communication accounting, matched tuning, method-specific rescue, positive controls, full evaluation dimensions, source custody, and 18 rejecting mutations.",
        "output_assertions": [
            "Muon primary and AdamW fallback explicit",
            "7 optimizer policy state classes",
            "3 or more seeds",
            "8 evaluation dimensions",
            "3 source records",
            "6 non-authorities",
            "18 mutations reject",
            "no optimizer result or support effect"
        ],
        "claim_scope": "Authored optimizer-policy identity and comparison-readiness record shape only.",
        "negative_controls": "validator_owned_eighteen_identity_routing_state_schedule_approximation_communication_tuning_rescue_evaluation_source_and_authority_mutations",
        "negative_control_cases": [
            "implementation identity erased", "primary family substituted",
            "fallback family substituted", "parameter routing erased",
            "fallback state omitted", "schedule state omitted",
            "approximation identity omitted", "zero orthogonalization iterations",
            "coefficient binding erased", "communication accounting erased",
            "unmatched tuning", "single-seed comparison", "post-outcome rescue",
            "positive controls removed", "evaluation dimension removed",
            "transfer laundering", "source removed",
            "superiority authority invented"
        ],
        "prohibited_inference": "The schema, fixture, or validator does not implement, train, compare, reproduce, qualify, or prove the superiority, transfer, quality, safety, support, release, AGI, or ASI value of any optimizer.",
        "contract_precision": "exact_optimizer_policy_identity_and_nonclaim_contract",
        "semantic_review_state": "checked_optimizer_identity_false_negative_and_nonauthority_boundaries"
    })
    required = registry["required_artifacts"]
    for artifact in ARTIFACTS + [REGISTER]:
        if artifact not in required:
            required.append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {
        "required_artifact_count": len(required),
        "unit_count": len(registry["units"]),
    }
    path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered optimizer policy card: {len(registry['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()

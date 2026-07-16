#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation" / "registry.json"
SCRIPT = "validate_research_foundation.py"
ARTIFACTS = [
    "scripts/validate_research_foundation.py",
    "experiments/research_foundation/foundation.json",
    "experiments/research_foundation/task_corpus.json",
    "experiments/research_foundation/held_out_labels.json",
    "experiments/research_foundation/sacrificial_preflight.json",
    "docs/research_measurement_and_reproduction_foundation.md",
    "roadmap_records/post_v2_3_claim_proof_and_sota_challenge_status.json",
]


def main() -> None:
    value = json.loads(REGISTRY.read_text(encoding="utf-8"))
    existing = next((row for row in value["units"] if row.get("script") == SCRIPT), None)
    value["units"] = [row for row in value["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in value["units"]}
    preferred = existing.get("order") if existing else None
    order = preferred if preferred and preferred not in used else next(index for index in range(1, len(value["units"]) + 2) if index not in used)
    value["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Frozen natural governed-transaction corpus, isolated held-out labels, dated model selection, inference/evaluator/statistics/environment/safety/artifact contracts, and sacrificial parser/evaluator canaries.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Reject corpus or split drift, label leakage, missing current-strong/comparison/local model roles, self-evaluation, weak instrument preflight, support laundering, or invented publication authority.",
        "output_assertions": [
            "24 unique public-safe tasks across governed-work, governed-learning, and assurance-control slices",
            "six sacrificial, six tuning, and twelve isolated held-out tasks",
            "current strong general, independent comparison, and small reproducible model roles",
            "8/10 schema-admissible and 7/8 semantically correct admissible sacrificial canaries with two independent evaluators",
            "statistics, environment, safety, and append-only artifact contracts with no support or publication authority",
        ],
        "claim_scope": "M2 research-instrument and artifact-foundation readiness only; sacrificial cases are non-evidentiary.",
        "negative_controls": "validator_owned_support_split_model_evaluator_publication_and_preflight_floor_mutations",
        "negative_control_cases": ["support laundering","held-out denominator laundering","strong-model omission","single self-evaluator","publication-authority invention","preflight adequacy-floor miss"],
        "prohibited_inference": "Does not establish model capability, corpus representativeness, evaluator validity outside canaries, adequate campaign power, deployed behavior, useful throughput, safety, reproduction, transfer, SOTA, AGI, ASI, or chapter-core support.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_sacrificial_research_foundation_not_outcome_bearing_campaign_evidence",
    })
    required = list(value["required_artifacts"])
    for artifact in ARTIFACTS:
        if artifact not in required:
            required.append(artifact)
    value["units"].sort(key=lambda row: row["order"])
    value["required_artifacts"] = required
    value["summary"] = {"required_artifact_count": len(required), "unit_count": len(value["units"])}
    REGISTRY.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {len(value['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()

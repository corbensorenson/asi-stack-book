#!/usr/bin/env python3
"""Register the frozen P2 task qualification/replacement policy validator."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_task_qualification_and_replacement_policy.py"
ARTIFACTS = [
    "evidence_quality/p2_task_qualification_and_replacement_policy.json",
    "schemas/p2_task_qualification_and_replacement_policy.schema.json",
    "docs/p2_task_qualification_and_replacement_policy.md",
    "scripts/validate_p2_task_qualification_and_replacement_policy.py",
    "scripts/register_p2_task_qualification_and_replacement_policy.py",
    "evidence_quality/p2_development_corpus_preflight.json",
    "experiments/p2_governed_repository_admission/corpus/development_pool.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in registry["units"]}
    order = next(index for index in range(1, len(registry["units"]) + 2) if index not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "Pinned original development denominator and eligible metadata digests; paired exact gold oracle; separated dependency setup; runtime network isolation; dual parser; repeatability; N0 exclusion; deterministic same-language sequential replacement; final custody.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Freeze a non-outcome-aware development-task qualification and replacement policy that fails closed on setup, parser, construct, environment, repeatability, resource, or custody defects.",
        "output_assertions": [
            "two repetitions per paired arm",
            "same sealed environment and runtime network none",
            "exact baseline and human-gold status sets",
            "independently implemented parser required",
            "raw logs retained for every attempt",
            "task exclusions remain N0 with no claim effect",
            "same-language deterministic sequential replacement queue",
            "no outcome-aware candidate skipping",
            "final pool unselected and unopened",
            "thirteen mutations reject"
        ],
        "claim_scope": "Development construct/instrument policy only; no task has been replaced and no empirical support or final-heldout result follows.",
        "negative_controls": "validator_owned_thirteen_oracle_network_parser_log_inference_replacement_seed_queue_custody_and_support_mutations",
        "negative_control_cases": [
            "one repetition",
            "runtime network",
            "patch during dependency setup",
            "baseline subset scoring",
            "gold extras allowed",
            "independent parser removed",
            "raw logs optional",
            "negative inference promotion",
            "candidate skipping",
            "replacement seed drift",
            "queue state erased",
            "final pool opened",
            "support promotion"
        ],
        "prohibited_inference": "A frozen policy, development task pass, task exclusion, or replacement does not establish coding ability, governance benefit, safety, transfer, SOTA, release, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "paired_oracle_dependency_isolation_dual_evaluator_repeatability_exclusion_replacement_resource_and_final_custody_reviewed"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Register the P2 replacement-queue custody validator."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_replacement_queue.py"
ARTIFACTS = [
    "experiments/p2_governed_repository_admission/corpus/replacement_queue.json",
    "experiments/p2_governed_repository_admission/corpus/post_snapshot_eligible_metadata.jsonl",
    "experiments/p2_governed_repository_admission/corpus/development_pool.json",
    "evidence_quality/p2_task_qualification_and_replacement_policy.json",
    "evidence_quality/p2_resource_ceiling.json",
    "evidence_quality/p2_gold_preflight_diagnosis.json",
    "schemas/p2_replacement_queue.schema.json",
    "docs/p2_replacement_queue.md",
    "scripts/build_p2_replacement_queue.py",
    "scripts/validate_p2_replacement_queue.py",
    "scripts/register_p2_replacement_queue.py"
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [row for row in registry["units"] if row.get("script") != SCRIPT]
    used = {row["order"] for row in registry["units"]}
    order = next(index for index in range(1, len(registry["units"]) + 2) if index not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": [],
        "execution_tier": "pr", "validation_class": "proof_or_evidence_gate",
        "input_contract": "Pinned metadata and original-pool digests; frozen pre-outcome policy and resource ceiling; four N0 same-language replacement slots; deterministic hash ordering; no task-content, outcome, or final-pool access.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Freeze and verify the exact sequential candidate queues without favorable selection, candidate reuse, content leakage, or claim promotion.",
        "output_assertions": [
            "four lexicographically ordered replacement slots", "thirty deterministic candidates",
            "same language within each slot", "unique candidate identities and repositories",
            "aggregate and per-slot digests match", "task text patches images and gold outcomes unopened",
            "replacement qualification not started", "final pool unselected and unopened",
            "no support or release effect", "twelve mutations reject"
        ],
        "claim_scope": "Metadata-only development replacement ordering and custody; no task qualification or empirical result follows.",
        "negative_controls": "validator_owned_twelve_order_seed_content_skip_reuse_language_digest_gold_final_and_support_mutations",
        "negative_control_cases": ["slot order swap", "seed drift", "content opened", "candidate skipped", "duplicate repository", "cross language", "queue digest drift", "slot digest drift", "gold opened", "final selected", "support promotion", "candidate removed"],
        "prohibited_inference": "Queue membership or rank does not establish task validity, coding ability, mechanism benefit, safety, transfer, SOTA, release, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "deterministic_metadata_selection_sequential_opening_uniqueness_custody_and_nonpromotion_reviewed"
    })
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()

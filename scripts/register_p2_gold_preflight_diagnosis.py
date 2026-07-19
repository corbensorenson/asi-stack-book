#!/usr/bin/env python3
"""Register the P2 fixed-denominator gold-preflight diagnosis validator."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p2_gold_preflight_diagnosis.py"
ARTIFACTS = [
    "evidence_quality/p2_gold_preflight_diagnosis.json",
    "schemas/p2_gold_preflight_diagnosis.schema.json",
    "docs/p2_gold_preflight_diagnosis.md",
    "scripts/build_p2_gold_preflight_diagnosis.py",
    "scripts/validate_p2_gold_preflight_diagnosis.py",
    "scripts/register_p2_gold_preflight_diagnosis.py",
    "scripts/run_p2_gold_preflight.py",
    "scripts/run_p2_gold_preflight_rescue.py",
    "experiments/p2_governed_repository_admission/gold_preflight/result.json",
    "experiments/p2_governed_repository_admission/gold_preflight_attempt_001_read_only_instrument_failure/result.json",
    "experiments/p2_governed_repository_admission/gold_preflight_attempt_002_pilot_success/result.json",
    "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-raw-log-custody-abort/record.json",
    "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-rust-diagnostic-r1/result.json",
    "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-dependency-diagnostic-r1/result.json",
    "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-java-ipv4-diagnostic-r1/result.json",
    "experiments/p2_governed_repository_admission/gold_preflight_rescue/attempts/2026-07-17-java-surefire-diagnostic-r1/result.json",
    "evidence_quality/p2_task_qualification_and_replacement_policy.json",
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
        "input_contract": "Fixed 12-task natural development denominator; pinned upstream harness and parsers; independent AVA parser; immutable original, pilot, aborted, dependency, filesystem, compile, and Maven rescue attempts; compressed raw logs; N0 exclusion policy; final custody.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Terminally disposition every original development task without dropping failures, promoting instrument defects, weakening the oracle, erasing attempts, reducing the target denominator, opening replacements prematurely, or touching final-heldout custody.",
        "output_assertions": [
            "twelve unique original tasks dispositioned",
            "seven original exact passes",
            "one upstream parser false reject independently recovered",
            "eight qualified development tasks",
            "four N0 exclusions and replacement slots",
            "five qualified languages",
            "eight retained attempt records",
            "sixty-two digest-verified arm logs",
            "resource gate pending peak memory CPU and frozen ceiling",
            "replacement draw not started",
            "final pool unselected and unopened",
            "twelve mutations reject"
        ],
        "claim_scope": "Development gold-oracle instrument/construct diagnosis only; no governed-admission, model, safety, transfer, SOTA, release, AGI, or ASI result.",
        "negative_controls": "validator_owned_twelve_denominator_inference_lineage_raw_custody_resource_replacement_repetition_and_support_mutations",
        "negative_control_cases": [
            "qualified count inflation",
            "replacement count reduction",
            "N0 promotion",
            "claim effect promotion",
            "mechanism negative laundering",
            "attempt erasure",
            "raw-log custody removal",
            "final selection",
            "resource premature pass",
            "replacement premature start",
            "single repetition",
            "support promotion"
        ],
        "prohibited_inference": "A development task pass or exclusion cannot establish or refute the governed-admission mechanism; four replacements and every remaining competence gate are still required.",
        "contract_precision": "exact",
        "semantic_review_state": "fixed_denominator_parser_dependency_compile_external_resource_filesystem_maven_resource_attempt_and_final_custody_reviewed"
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

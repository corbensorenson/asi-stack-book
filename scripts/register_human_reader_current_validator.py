#!/usr/bin/env python3
"""Idempotently register the maintained Human Reader manuscript gate."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
OVERRIDES = ROOT / "validation/unit_contract_overrides.json"
SCRIPT = "validate_human_reader_current.py"
ARTIFACTS = [
    "scripts/validate_human_reader_current.py",
    "scripts/build_human_reader_current.py",
    "scripts/register_human_reader_current_validator.py",
    "editions/reader_manuscript/current/manifest.json",
    "editions/reader_manuscript/current/_quarto.yml",
    "editions/reader_manuscript/current/index.qmd",
    "editions/reader_manuscript/current/chapters/unit-04-security-privacy-and-ai-artifact-custody.qmd",
    "editions/reader_manuscript/current/generated/unit-04-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd",
    "editions/reader_manuscript/current/generated/unit-05-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-06-human-intent-control-and-epistemic-security.qmd",
    "editions/reader_manuscript/current/generated/unit-06-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd",
    "editions/reader_manuscript/current/generated/unit-07-status.qmd",
    "editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd",
    "editions/reader_manuscript/current/generated/unit-23-status.qmd",
    "docs/human_reader_26_unit_outline.md",
    "book_structure.json",
    "roadmap_records/post_v2_3_maintenance_transfer_and_publication_status.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    unit = next((row for row in registry["units"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if unit is None:
        order = max(row["order"] for row in registry["units"]) + 1
        unit = {"id": f"{SCRIPT}:{order}", "order": order, "script": SCRIPT, "args": []}
        registry["units"].append(unit)
    contract = {
        "execution_tier": "pr",
        "validation_class": "proof_or_evidence_gate",
        "input_contract": "The canonical 26-unit outline, all 87 exact technical-owner routes, independent maintained prose sources, and generated compact status panels.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Require exact owner coverage, honest drafting and target-length states, independent prose custody, canonical generated derivatives, preserved support boundaries, and no format or release work.",
        "output_assertions": ["26 Human Reader units", "87 owners routed once", "Units 4, 5, 6, 7, and 23 within their declared word targets", "independent maintained prose", "3 mutations reject", "support and release effects none"],
        "claim_scope": "Independent Human Reader manuscript structure and Units 4, 5, 6, 7, and 23 drafting completeness only.",
        "negative_controls": "validator_owned_route_length_and_support_mutations",
        "negative_control_cases": ["owner-route loss", "false length completion", "support laundering"],
        "prohibited_inference": "Draft or target-length completion does not establish editorial approval, evidence, publication, release, safety, readiness, SOTA, AGI, or ASI.",
        "contract_precision": "exact_high_impact",
        "semantic_review_state": "checked_independent_human_reader_draft_contract",
    }
    unit.update(contract)
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda row: row["order"])
    registry["summary"] = {"required_artifact_count": len(registry["required_artifacts"]), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    overrides = json.loads(OVERRIDES.read_text(encoding="utf-8"))
    keys = [key for key in contract if key not in {"execution_tier", "validation_class"}]
    record = {"script": SCRIPT, "args": [], **{key: contract[key] for key in keys}}
    existing = next((row for row in overrides["contracts"] if row["script"] == SCRIPT and row.get("args", []) == []), None)
    if existing is None:
        overrides["contracts"].append(record)
    else:
        existing.clear()
        existing.update(record)
    OVERRIDES.write_text(json.dumps(overrides, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, {registry['summary']['required_artifact_count']} artifacts.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Register the R16-B current-reader freshness validation unit."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_r16_b_current_reader_freshness.py"
ARTIFACTS = [
    "editions/reader_manuscript/reader_2026_07_26/manifest.json",
    "editions/reader_manuscript/reader_2026_07_26/freshness_report.md",
    "schemas/r16_b_current_reader_freshness.schema.json",
    "scripts/build_r16_b_current_reader_freshness.py",
    "scripts/validate_r16_b_current_reader_freshness.py",
    "scripts/register_r16_b_current_reader_freshness.py",
    "book_structure.json",
    "evidence_quality/current_chapter_role_map.json",
    "products/narrative_unit_crosswalk.json",
    "editions/reader_manuscript/reader_2026_07_18/manifest.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    used = {unit["order"] for unit in registry["units"]}
    order = next(value for value in range(1, len(registry["units"]) + 2) if value not in used)
    registry["units"].append(
        {
            "id": f"{SCRIPT}:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "pr",
            "validation_class": "proof_or_evidence_gate",
            "input_contract": "One exact source commit containing 84 unique manifest chapters, the exact role partition and 22-unit route, eight reader surfaces, and the immutable historical reader manifest.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Content-address all current reader projections and routing without copying the canonical manuscript, rewriting history, fabricating unreviewed formats, or moving support or release authority.",
            "output_assertions": [
                "84 of 84 frozen-commit chapter projections reproduce",
                "22 of 22 narrative units are represented",
                "chapter-role partition remains 11/54/7/12",
                "8 of 8 required reader surfaces reproduce",
                "reader-2026-07-18 manifest identity and digest remain immutable",
                "HTML, PDF, EPUB, DOCX, and audio are honestly deferred",
                "16 scope, identity, digest, format, and authority mutations reject",
                "zero support, release, or publication movement",
            ],
            "claim_scope": "Current manuscript reader-source freshness, organization, reproducibility, and handoff completeness only.",
            "negative_controls": "validator_owned_sixteen_identity_digest_route_surface_history_format_and_authority_mutations",
            "prohibited_inference": "Reader freshness is not publication, format QA, accessibility review, source correctness, claim proof, empirical support, safety, readiness, release, SOTA, AGI, or ASI.",
            "contract_precision": "exact",
            "semantic_review_state": "manual_current_reader_route_surface_history_and_format_disposition_review",
        }
    )
    for artifact in ARTIFACTS:
        if artifact not in registry["required_artifacts"]:
            registry["required_artifacts"].append(artifact)
    registry["units"].sort(key=lambda unit: unit["order"])
    registry["summary"] = {
        "required_artifact_count": len(registry["required_artifacts"]),
        "unit_count": len(registry["units"]),
    }
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")
    print(
        f"Registered {SCRIPT}: {registry['summary']['unit_count']} units, "
        f"{registry['summary']['required_artifact_count']} artifacts."
    )


if __name__ == "__main__":
    main()

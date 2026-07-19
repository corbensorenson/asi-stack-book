#!/usr/bin/env python3
"""Register the reader public-release manifest validator."""

from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_reader_public_release_manifest.py"
ARTIFACTS = [
    "editions/reader_manuscript/reader_2026_07_18/manifest.json",
    "schemas/reader_public_release_manifest.schema.json",
    "docs/reader_release_2026_07_18.md",
    "scripts/validate_reader_public_release_manifest.py",
    "scripts/register_reader_public_release_manifest.py",
]


def main() -> None:
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    units = [
        row for row in data["units"]
        if row.get("script") != SCRIPT and row.get("id") != "reader_public_release_manifest"
    ]
    order = len(units) + 1
    units.append(
        {
            "id": f"{SCRIPT}:{order}",
            "order": order,
            "script": SCRIPT,
            "args": [],
            "execution_tier": "release",
            "validation_class": "reader_artifact_gate",
            "input_contract": "Frozen reader-release manifest, exact PDF/EPUB/DOCX identities, source ancestry, rights state, and format-specific internal QA boundaries.",
            "input_artifacts": ARTIFACTS,
            "output_contract": "Reject identity, rights, accessibility, lineage, or publication-state drift; optionally verify exact local asset bytes.",
            "output_assertions": [
                "three exact format identities",
                "source commit remains ancestral",
                "candidate cannot invent public URLs",
                "published state requires URLs and release commit",
                "rights grant remains none",
                "accessibility residuals remain explicit",
                "three negative mutations reject"
            ],
            "claim_scope": "Public reader artifact identity and internal QA only; no chapter-core, accessibility-conformance, external-review, or canonical-release claim follows.",
            "negative_controls": "validator_owned_hash_rights_and_accessibility_mutations",
            "negative_control_cases": [
                "artifact hash drift",
                "invented rights grant",
                "invented PDF tagging"
            ],
            "prohibited_inference": "Does not establish PDF/UA, screen-reader, Apple Books, Microsoft Word, external-human, legal, peer-review, empirical, safety, AGI, ASI, or chapter-core support.",
            "contract_precision": "exact",
            "semantic_review_state": "checked_reader_identity_rights_qa_and_residual_boundary"
        }
    )
    data["units"] = sorted(units, key=lambda row: row["order"])
    for artifact in ARTIFACTS:
        if artifact not in data["required_artifacts"]:
            data["required_artifacts"].append(artifact)
    data["summary"] = {
        "required_artifact_count": len(data["required_artifacts"]),
        "unit_count": len(data["units"]),
    }
    REGISTRY.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print(f"Registered {SCRIPT}: release tier order {order}.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Register the P8 reader evidence-freeze validator."""

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "validation/registry.json"
SCRIPT = "validate_p8_reader_evidence_freeze.py"
ARTIFACTS = [
    "scripts/build_p8_reader_evidence_freeze.py",
    "scripts/build_p8_docx_contact_sheets.py",
    "scripts/validate_p8_reader_evidence_freeze.py",
    "scripts/register_p8_reader_evidence_freeze.py",
    "schemas/p8_reader_evidence_freeze.schema.json",
    "docs/p8_reader_evidence_freeze_and_release_disposition.md",
    "editions/reader_manuscript/v2_2/manifest.json",
    "editions/reader_manuscript/v2_2/evidence_freeze.json",
    "editions/reader_manuscript/v2_2/format_review_matrix.json",
    "editions/reader_manuscript/v2_2/release_disposition.json",
    "release_records/2026-07-16-post-v2-3-p8-evidence-freeze-ready-not-published.json",
]


def main() -> None:
    registry = json.loads(REGISTRY.read_text())
    registry["units"] = [unit for unit in registry["units"] if unit.get("script") != SCRIPT]
    used = {unit["order"] for unit in registry["units"]}
    order = next(i for i in range(1, len(registry["units"]) + 2) if i not in used)
    registry["units"].append({
        "id": f"{SCRIPT}:{order}",
        "order": order,
        "script": SCRIPT,
        "args": [],
        "execution_tier": "pr",
        "validation_class": "reader_artifact_gate",
        "input_contract": "The exact 55-chapter P8 reader source, four generated format artifacts, current 60-page browser/accessibility reports, and complete DOCX/PDF raster audits.",
        "input_artifacts": ARTIFACTS,
        "output_contract": "Bind the local evidence freeze while preserving separate HTML, EPUB, DOCX, PDF, rights, publication, and support-state dispositions.",
        "output_assertions": [
            "55 frozen chapters and 60 HTML pages",
            "four exact artifact digests",
            "HTML locally approved only",
            "EPUB and DOCX bounded but not release-approved",
            "PDF layout failure preserved",
            "seven mutations rejected",
            "no publication or support movement",
        ],
        "claim_scope": "P8 local reader evidence freeze and format/release disposition only.",
        "negative_controls": "validator_owned_seven_p8_freeze_laundering_mutations",
        "negative_control_cases": [
            "chapter-count inflation",
            "stale HTML page denominator",
            "source digest rewrite",
            "EPUB digest rewrite",
            "support promotion",
            "false publication status",
            "browser-report digest rewrite",
        ],
        "prohibited_inference": "A built format, automated accessibility result, local application inspection, or digest-bound freeze does not establish public release, Word/Preview behavior, screen-reader or device conformance, legal WCAG status, chapter truth, SOTA, deployment, AGI, or ASI.",
        "contract_precision": "exact",
        "semantic_review_state": "checked_per_format_artifact_application_raster_rights_release_and_support_boundaries",
    })
    required = list(registry["required_artifacts"])
    for path in ARTIFACTS:
        if path not in required:
            required.append(path)
    registry["units"].sort(key=lambda unit: unit["order"])
    registry["required_artifacts"] = required
    registry["summary"] = {"required_artifact_count": len(required), "unit_count": len(registry["units"])}
    REGISTRY.write_text(json.dumps(registry, indent=2) + "\n")
    print(f"Registered {SCRIPT}: {len(registry['units'])} units, {len(required)} artifacts.")


if __name__ == "__main__":
    main()

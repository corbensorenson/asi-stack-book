#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
AUDIT = ROOT / "docs" / "v1_0_release_gate_audit.md"

GATES = (
    "Reader artifact gate",
    "Claim-state gate",
    "First measured/replayed result gate",
    "Proof-depth gate",
    "Validator coverage gate",
    "Protocol record gate",
    "External-SOTA prose gate",
    "Beyond-SOTA map gate",
    "Architecture red-team gate",
    "Reproducibility and citability gate",
    "Green release gate",
)

REQUIRED_SECTIONS = (
    "# v1.0 Release Gate Audit",
    "## Gate Matrix",
    "## Release Classification",
    "## Final Release Facts",
    "## Validation Command",
    "## Non-Claims",
)

REQUIRED_FRAGMENTS = (
    "tagged v1.0.0 release-gate audit",
    "Current classification: tagged v1.0.0 living-book evidence-and-reader release boundary.",
    "Source tag: `v1.0.0`.",
    "Source commit: `96d0ca3c6b62f3530202535573941b1f6e50a83d`.",
    "GitHub Release: `https://github.com/corbensorenson/asi-stack-book/releases/tag/v1.0.0`.",
    "Living-book release record: `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`.",
    "all chapter core claims remain at `argument`",
    "DOI/Zenodo remains pending",
    "workflow run `28360079172`",
    "python3 scripts/validate_v1_release_gate_audit.py",
    "does not create a DOI or Zenodo archive",
    "does not approve EPUB, DOCX, PDF, e-reader, audio, or",
    "does not promote any chapter core claim above `argument`",
)

EVIDENCE_REFS = (
    "release_records/2026-06-29-v1-reader-html-855dc277.json",
    "docs/reader_html_artifact_browser_review.md",
    "docs/reader_format_review_matrix.md",
    "docs/core_claim_transition_coverage.md",
    "claim_decisions/v1_0_core_claim_no_promotion.json",
    "docs/evidence_transition_pilot.md",
    "docs/first_measured_replayed_slice.md",
    "docs/costed_route_resource_slice.md",
    "docs/circle_external_receipt_slice.md",
    "evidence_transitions/v1_0_measured/phase5_harness_runner_synthetic_test_backed.json",
    "evidence_transitions/v1_0_measured/costed_route_resource_slice_synthetic_test_backed.json",
    "evidence_transitions/v1_0_measured/circle_external_rope_receipt_prototype_backed.json",
    "docs/proof_depth_classification.md",
    "docs/proof_adequacy_review.md",
    "scripts/validate_validator_coverage.py",
    "experiments/phase5_harness_registry.json",
    "protocols/v1_critical_protocol_crosswalk.json",
    "docs/protocol_record_crosswalk.md",
    "docs/external_sota_positioning_audit.md",
    "docs/v1_0_roadmap.md",
    "docs/v1_progress_ledger.md",
    "docs/architecture_red_team_review.md",
    "docs/release_reproducibility.md",
    "release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json",
    "CITATION.cff",
    ".github/workflows/publish.yml",
    "lean/lean-toolchain",
)

VALIDATOR_REFS = (
    "python3 scripts/validate_core_claim_decisions.py",
    "python3 scripts/validate_evidence_transitions.py",
    "python3 scripts/validate_proof_depth.py",
    "python3 scripts/validate_proof_readiness.py",
    "lake build",
    "python3 scripts/validate_protocol_crosswalk.py",
    "python3 scripts/validate_circle_external_receipt_slice.py",
    "python3 scripts/validate_external_sota_positioning.py --release",
    "python3 scripts/validate_architecture_red_team.py",
    "python3 scripts/validate_release_reproducibility.py",
)

BAD_FINALITY_CLAIMS = (
    "doi has been issued",
    "zenodo archive exists",
    "all reader formats are approved",
    "chapter core claims are synthetic-test-backed",
)


def fail(errors: list[str]) -> None:
    print("v1.0 release gate audit validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> None:
    errors: list[str] = []
    if not AUDIT.exists():
        fail(["Missing docs/v1_0_release_gate_audit.md."])
    text = read(AUDIT)
    lowered = text.lower()

    for section in REQUIRED_SECTIONS:
        if section not in text:
            errors.append(f"Audit missing section: {section}")
    for fragment in REQUIRED_FRAGMENTS:
        if fragment not in text:
            errors.append(f"Audit missing required fragment: {fragment}")
    for gate in GATES:
        if gate not in text:
            errors.append(f"Audit missing gate row for: {gate}")
    gate_rows = re.findall(r"^\|\s*(\d+)\s*\|\s*([^|]+?)\s*\|", text, re.MULTILINE)
    gate_numbers = {int(number) for number, _ in gate_rows if number.isdigit()}
    if gate_numbers != set(range(1, 12)):
        errors.append(f"Audit gate numbers must be 1 through 11, found {sorted(gate_numbers)}.")

    for ref in EVIDENCE_REFS:
        if ref not in text:
            errors.append(f"Audit missing evidence ref: {ref}")
        if not (ROOT / ref).exists():
            errors.append(f"Audit evidence ref does not exist: {ref}")
    for ref in VALIDATOR_REFS:
        if ref not in text:
            errors.append(f"Audit missing validator ref: {ref}")

    release_records = sorted((ROOT / "release_records").glob("*.json"))
    edition_record = ROOT / "release_records" / "2026-06-29-v1-reader-html-855dc277.json"
    living_record = ROOT / "release_records" / "2026-06-29-v1.0.0-living-book-96d0ca3c.json"
    if edition_record not in release_records:
        errors.append("Reader HTML edition release record is missing.")
    if living_record not in release_records:
        errors.append("v1.0.0 living-book release record is missing.")
    try:
        edition = json.loads(edition_record.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - validation diagnostic
        errors.append(f"Reader HTML edition release record is not valid JSON: {exc}")
    else:
        if edition.get("validation_status") != "pass":
            errors.append("Reader HTML edition release record must have validation_status pass.")
        if "does not promote any chapter core claim above argument" not in "\n".join(edition.get("non_claims", [])):
            errors.append("Reader HTML edition release record must preserve chapter-core non-promotion boundary.")
    try:
        living = json.loads(living_record.read_text(encoding="utf-8"))
    except Exception as exc:  # pragma: no cover - validation diagnostic
        errors.append(f"v1.0.0 living-book release record is not valid JSON: {exc}")
    else:
        if living.get("release_state") != "tagged_major_version":
            errors.append("v1.0.0 living-book release record must have release_state tagged_major_version.")
        if living.get("source_commit") != "96d0ca3c6b62f3530202535573941b1f6e50a83d":
            errors.append("v1.0.0 living-book release record must name the exact source commit.")
        if living.get("validation_status") != "pass":
            errors.append("v1.0.0 living-book release record must have validation_status pass.")
        if "does not promote any chapter core claim above argument" not in "\n".join(living.get("non_claims", [])):
            errors.append("v1.0.0 living-book release record must preserve chapter-core non-promotion boundary.")

    for bad_claim in BAD_FINALITY_CLAIMS:
        if bad_claim in lowered:
            errors.append(f"Audit contains unsupported finality claim: {bad_claim}")

    if errors:
        fail(errors)

    print("v1.0 release gate audit validation passed: 11 gates checked with v1.0.0 tag facts and residuals preserved.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "evidence_bundle_completeness" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "evidence_bundle_completeness_probe.md"
CHAPTER = ROOT / "chapters" / "evidence-states-and-claim-discipline.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "evidence-states-and-claim-discipline.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "EvidenceStates.lean"

COMMAND = "python3 scripts/validate_evidence_bundle_completeness_probe.py"
PROOF_TAG = "lean:evidence.bundle.completeness_probe_bridge"
CODEX_TEST_NAME = "Evidence bundle completeness and changelog-consistency probe"
REQUIRED_THEOREMS = ["evidence_bundle_completeness_probe_bridge"]
REQUIRED_NON_CLAIMS = [
    "does not prove evidence truth",
    "does not prove source interpretation",
    "does not prove artifact correctness",
    "does not create a support-state transition",
    "does not promote the chapter support state",
    "does not prove deployed release governance",
]


BUNDLES: list[dict[str, Any]] = [
    {
        "bundle_id": "bundle://valid-no-change-source-note",
        "expect_valid": True,
        "claim_id": "claim://evidence-state-discipline",
        "current_support_state": "argument",
        "requested_support_state": "argument",
        "decision": "record_no_change",
        "accepted_transition_record": False,
        "promotion_blockers": [],
        "evidence_refs": ["source-note://benchmaxxing", "appendix-c://claim-evidence-matrix"],
        "artifact_digest": "sha256:1a4d8b1cde2b8f0e7f4c6a9b3d0e5f1a6c8b2d4e6f0a7b9c1d3e5f7a9b0c2d4e",
        "command": COMMAND,
        "result_ref": "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-02-add-evidence-bundle-completeness-and-changelog-consistency-probe",
        "changelog_consistency": "current",
        "limitations": ["source-note lineage and fixture shape only"],
        "residuals": ["no live claim support changes"],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "none",
        "evidence_truth_claimed": False,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "bundle_id": "bundle://valid-blocked-promotion",
        "expect_valid": True,
        "claim_id": "claim://evidence-bundle-promotion-burden",
        "current_support_state": "argument",
        "requested_support_state": "synthetic-test-backed",
        "decision": "block_promotion",
        "accepted_transition_record": False,
        "promotion_blockers": [
            "missing claim-specific accepted transition record",
            "missing external or independent review",
        ],
        "evidence_refs": ["fixture://support-state-harness", "lean://AsiStackProofs.EvidenceStates"],
        "artifact_digest": "sha256:6f2d9c0a4b7e1d3c5f8a0b2d4e6f1a3c5e7b9d0f2a4c6e8b1d3f5a7c9e0b2d4",
        "command": COMMAND,
        "result_ref": "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-02-add-evidence-bundle-completeness-and-changelog-consistency-probe",
        "changelog_consistency": "current",
        "limitations": ["synthetic fixture validates bundle shape, not claim truth"],
        "residuals": ["independent review and live evidence remain open"],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "none",
        "evidence_truth_claimed": False,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "bundle_id": "invalid://missing-claim-id",
        "expect_valid": False,
        "claim_id": "",
        "current_support_state": "argument",
        "requested_support_state": "argument",
        "decision": "record_no_change",
        "accepted_transition_record": False,
        "promotion_blockers": [],
        "evidence_refs": ["source-note://x"],
        "artifact_digest": "sha256:0a",
        "command": COMMAND,
        "result_ref": "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-02-add-evidence-bundle-completeness-and-changelog-consistency-probe",
        "changelog_consistency": "current",
        "limitations": ["claim id missing"],
        "residuals": ["invalid"],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "none",
        "evidence_truth_claimed": False,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "bundle_id": "invalid://missing-artifact-result",
        "expect_valid": False,
        "claim_id": "claim://missing-artifact",
        "current_support_state": "argument",
        "requested_support_state": "argument",
        "decision": "record_no_change",
        "accepted_transition_record": False,
        "promotion_blockers": [],
        "evidence_refs": ["source-note://x"],
        "artifact_digest": "",
        "command": COMMAND,
        "result_ref": "",
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-02-add-evidence-bundle-completeness-and-changelog-consistency-probe",
        "changelog_consistency": "current",
        "limitations": ["artifact missing"],
        "residuals": ["invalid"],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "none",
        "evidence_truth_claimed": False,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "bundle_id": "invalid://missing-command",
        "expect_valid": False,
        "claim_id": "claim://missing-command",
        "current_support_state": "argument",
        "requested_support_state": "argument",
        "decision": "record_no_change",
        "accepted_transition_record": False,
        "promotion_blockers": [],
        "evidence_refs": ["source-note://x"],
        "artifact_digest": "sha256:2b",
        "command": "",
        "result_ref": "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-02-add-evidence-bundle-completeness-and-changelog-consistency-probe",
        "changelog_consistency": "current",
        "limitations": ["command missing"],
        "residuals": ["invalid"],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "none",
        "evidence_truth_claimed": False,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "bundle_id": "invalid://promotion-without-transition-record",
        "expect_valid": False,
        "claim_id": "claim://unsupported-promotion",
        "current_support_state": "argument",
        "requested_support_state": "synthetic-test-backed",
        "decision": "record_no_change",
        "accepted_transition_record": False,
        "promotion_blockers": [],
        "evidence_refs": ["fixture://x"],
        "artifact_digest": "sha256:3c",
        "command": COMMAND,
        "result_ref": "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-02-add-evidence-bundle-completeness-and-changelog-consistency-probe",
        "changelog_consistency": "current",
        "limitations": ["promotion attempted without transition"],
        "residuals": ["invalid"],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "upward",
        "evidence_truth_claimed": False,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "bundle_id": "invalid://missing-changelog",
        "expect_valid": False,
        "claim_id": "claim://missing-changelog",
        "current_support_state": "argument",
        "requested_support_state": "argument",
        "decision": "record_no_change",
        "accepted_transition_record": False,
        "promotion_blockers": [],
        "evidence_refs": ["source-note://x"],
        "artifact_digest": "sha256:4d",
        "command": COMMAND,
        "result_ref": "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
        "changelog_ref": "",
        "changelog_consistency": "missing",
        "limitations": ["changelog missing"],
        "residuals": ["invalid"],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "none",
        "evidence_truth_claimed": False,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
    {
        "bundle_id": "invalid://missing-limits-nonclaims",
        "expect_valid": False,
        "claim_id": "claim://missing-limits",
        "current_support_state": "argument",
        "requested_support_state": "argument",
        "decision": "record_no_change",
        "accepted_transition_record": False,
        "promotion_blockers": [],
        "evidence_refs": ["source-note://x"],
        "artifact_digest": "sha256:5e",
        "command": COMMAND,
        "result_ref": "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
        "changelog_ref": "appendices/F_changelog.qmd#2026-07-02-add-evidence-bundle-completeness-and-changelog-consistency-probe",
        "changelog_consistency": "current",
        "limitations": [],
        "residuals": [],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "none",
        "evidence_truth_claimed": False,
        "non_claims": [],
    },
    {
        "bundle_id": "invalid://stale-changelog-overclaim",
        "expect_valid": False,
        "claim_id": "claim://stale-overclaim",
        "current_support_state": "argument",
        "requested_support_state": "argument",
        "decision": "record_no_change",
        "accepted_transition_record": False,
        "promotion_blockers": [],
        "evidence_refs": ["source-note://x"],
        "artifact_digest": "sha256:6f",
        "command": COMMAND,
        "result_ref": "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
        "changelog_ref": "appendices/F_changelog.qmd#old-entry",
        "changelog_consistency": "stale",
        "limitations": ["stale changelog"],
        "residuals": ["invalid"],
        "reviewer_refs": ["reviewer://local-maintainer"],
        "support_state_effect": "none",
        "evidence_truth_claimed": True,
        "non_claims": REQUIRED_NON_CLAIMS,
    },
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Evidence bundle completeness probe validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def nonempty_list(record: dict[str, Any], key: str) -> bool:
    return isinstance(record.get(key), list) and bool(record[key])


def bundle_errors(record: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    bundle_id = str(record.get("bundle_id", "<missing>"))

    if not bundle_id.startswith(("bundle://", "invalid://")):
        errors.append(f"{bundle_id}: bundle_id must use bundle:// or invalid://.")
    for key in ("claim_id", "command", "result_ref", "changelog_ref"):
        if not str(record.get(key, "")).strip():
            errors.append(f"{bundle_id}: {key} is required.")
    if not str(record.get("artifact_digest", "")).startswith("sha256:"):
        errors.append(f"{bundle_id}: artifact_digest must be a sha256 digest reference.")
    for key in ("evidence_refs", "limitations", "residuals", "reviewer_refs"):
        if not nonempty_list(record, key):
            errors.append(f"{bundle_id}: {key} is required.")

    current_state = str(record.get("current_support_state", ""))
    requested_state = str(record.get("requested_support_state", ""))
    decision = str(record.get("decision", ""))
    if decision not in {"record_no_change", "block_promotion"}:
        errors.append(f"{bundle_id}: decision must be record_no_change or block_promotion.")
    if decision == "record_no_change" and current_state != requested_state:
        errors.append(f"{bundle_id}: changed requested_support_state must not be recorded as no-change.")
    if decision == "block_promotion" and not nonempty_list(record, "promotion_blockers"):
        errors.append(f"{bundle_id}: blocked promotions need promotion_blockers.")
    if requested_state != current_state and record.get("accepted_transition_record") is True:
        errors.append(f"{bundle_id}: synthetic probe must not accept live support-state transitions.")
    if requested_state != current_state and decision != "block_promotion":
        errors.append(f"{bundle_id}: requested support movement must be blocked in this probe.")
    if record.get("support_state_effect") != "none":
        errors.append(f"{bundle_id}: support_state_effect must remain none.")
    if record.get("changelog_consistency") != "current":
        errors.append(f"{bundle_id}: changelog_consistency must be current.")
    if record.get("evidence_truth_claimed") is not False:
        errors.append(f"{bundle_id}: evidence_truth_claimed must be false.")

    non_claim_text = text_blob(record.get("non_claims", []))
    for phrase in REQUIRED_NON_CLAIMS:
        if phrase.lower() not in non_claim_text:
            errors.append(f"{bundle_id}: non_claims missing {phrase!r}.")
    return errors


def build_expected_result(valid_count: int, invalid_count: int) -> dict[str, Any]:
    return {
        "schema_version": "asi_stack.evidence_bundle_completeness_probe.v0",
        "result_id": "2026-07-02-evidence-bundle-completeness-probe",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "deterministic_synthetic_evidence_bundle_completeness_probe",
        "valid_bundle_count": valid_count,
        "expected_invalid_control_count": invalid_count,
        "bundle_count": len(BUNDLES),
        "negative_controls": {
            "missing_claim_id_rejected": True,
            "missing_artifact_or_result_rejected": True,
            "missing_command_rejected": True,
            "promotion_without_transition_record_rejected": True,
            "missing_changelog_rejected": True,
            "missing_limits_or_nonclaims_rejected": True,
            "stale_changelog_or_truth_overclaim_rejected": True,
        },
        "coverage": {
            "no_change_bundle_present": True,
            "blocked_promotion_bundle_present": True,
            "evidence_refs_required": True,
            "artifact_digest_required": True,
            "command_and_result_required": True,
            "changelog_consistency_required": True,
            "support_state_no_promotion": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.EvidenceStates",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "no_change_bundle_present": True,
                "blocked_promotion_bundle_present": True,
                "negative_controls_rejected": True,
                "changelog_consistency_present": True,
                "support_state_effect_none": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Synthetic evidence-bundle completeness fixture only; no evidence truth, source interpretation, artifact correctness, release governance, or support-state transition is established.",
            "The Evidence States chapter core claim remains at argument support.",
        ],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


def validate_result(expected: dict[str, Any], write_result: bool, errors: list[str]) -> None:
    serialized = json.dumps(expected, indent=2, sort_keys=True) + "\n"
    if write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized, encoding="utf-8")
        return
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}; run {COMMAND} --write-result.")
        return
    current = RESULT.read_text(encoding="utf-8")
    if current != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_manifest(errors: list[str]) -> None:
    value = load_json(MANIFEST)
    chapter = None
    for part in value.get("parts", []):
        for candidate in part.get("chapters", []):
            if candidate.get("id") == "evidence-states-and-claim-discipline":
                chapter = candidate
                break
    if chapter is None:
        errors.append("book_structure.json: missing Evidence States chapter.")
        return
    if CODEX_TEST_NAME.lower() not in text_blob(chapter.get("codex_tests", [])):
        errors.append(f"book_structure.json: codex_tests missing {CODEX_TEST_NAME!r}.")
    proof_tags = {target.get("tag") for target in chapter.get("proof_targets", []) if isinstance(target, dict)}
    if PROOF_TAG not in proof_tags:
        errors.append(f"book_structure.json: proof_targets missing {PROOF_TAG!r}.")


def validate_lean(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8", errors="ignore")
    for theorem in REQUIRED_THEOREMS:
        if not re.search(rf"\btheorem\s+{re.escape(theorem)}\b", text):
            errors.append(f"{rel(LEAN_FILE)} missing theorem {theorem}.")
    for field in (
        "noChangeBundlePresent",
        "blockedPromotionBundlePresent",
        "negativeControlsRejected",
        "changelogConsistencyPresent",
        "supportStateEffectNone",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Evidence Bundle Completeness Probe",
            rel(RESULT),
            "two valid synthetic evidence bundles",
            "seven expected-invalid controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Evidence bundle completeness and changelog-consistency probe",
            rel(RESULT),
            "two valid synthetic evidence bundles",
            "seven expected-invalid controls",
        ],
        READER: [
            "evidence bundle completeness and changelog-consistency probe",
            "two synthetic evidence bundles",
            "not a deployed release-governance result",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Evidence bundle completeness and changelog-consistency probe",
            "deterministic synthetic evidence-bundle fixture",
            "no support-state promotion",
        ],
        CHANGELOG: ["Evidence bundle completeness and changelog-consistency probe", rel(RESULT)],
        VALIDATE_BOOK: [
            "scripts/validate_evidence_bundle_completeness_probe.py",
            "docs/evidence_bundle_completeness_probe.md",
            "experiments/evidence_bundle_completeness/results/2026-07-02-local.json",
            'run_validator("validate_evidence_bundle_completeness_probe.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required evidence bundle completeness surface {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore").lower()
        for phrase in phrases:
            if phrase.lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    valid_count = 0
    invalid_count = 0
    for bundle in BUNDLES:
        expect_valid = bool(bundle.get("expect_valid"))
        current_errors = bundle_errors(bundle)
        if expect_valid:
            valid_count += 1
            errors.extend(current_errors)
        else:
            invalid_count += 1
            if not current_errors:
                errors.append(f"{bundle.get('bundle_id', '<missing>')}: expected-invalid control unexpectedly passed.")

    if valid_count != 2:
        errors.append("Expected exactly two valid synthetic evidence bundles.")
    if invalid_count != 7:
        errors.append("Expected exactly seven expected-invalid controls.")

    expected = build_expected_result(valid_count, invalid_count)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Evidence bundle completeness probe validation passed.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "accepted_transition_review" / "results" / "2026-07-02-local.json"
DOC = ROOT / "docs" / "accepted_transition_review_audit.md"
CHAPTER = ROOT / "chapters" / "evidence-states-and-claim-discipline.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "evidence-states-and-claim-discipline.qmd"
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
MANIFEST = ROOT / "book_structure.json"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
TRANSITION_DIR = ROOT / "evidence_transitions"
NO_PROMOTION_LEDGER = ROOT / "claim_decisions" / "v1_0_core_claim_no_promotion.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "EvidenceStates.lean"

COMMAND = "python3 scripts/validate_accepted_transition_review_audit.py"
PROOF_TAG = "lean:evidence.accepted_transition.review_audit_bridge"
CODEX_TEST_NAME = "Accepted live transition review audit"
REQUIRED_THEOREMS = ["accepted_transition_review_audit_bridge"]
REQUIRED_NON_CLAIMS = [
    "does not prove evidence truth",
    "does not prove reviewer independence",
    "does not prove source interpretation",
    "does not promote chapter core claims",
    "does not approve new support-state transitions",
    "does not prove external review quality",
]

REQUIRED_TRANSITION_FIELDS = [
    "transition_id",
    "claim_id",
    "claim_surface_refs",
    "claim_record_refs",
    "old_support_state",
    "new_support_state",
    "transition_effect",
    "transition_validity_state",
    "scope_boundary",
    "evidence_roles",
    "transition_reason",
    "required_artifacts",
    "artifact_refs",
    "evidence_packet_refs",
    "verification_command",
    "verification_result",
    "negative_results",
    "negative_evidence_refs",
    "downgrade_triggers",
    "promotion_burden",
    "limitations",
    "review_status",
    "reviewer_refs",
    "reviewer_independence",
    "acceptance_blockers",
    "changelog_ref",
    "support_state_effect",
    "non_claims",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Accepted transition review audit validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def flatten_chapters(structure: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        chapter
        for part in structure.get("parts", [])
        for chapter in part.get("chapters", [])
        if isinstance(chapter, dict)
    ]


def nonempty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def nonempty_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def transition_records() -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(TRANSITION_DIR.rglob("*.json")):
        value = load_json(path)
        if not isinstance(value, dict):
            continue
        if value.get("review_status") != "accepted":
            continue
        record = deepcopy(value)
        record["_path"] = rel(path)
        records.append(record)
    return records


def decision_ledger() -> dict[str, Any]:
    value = load_json(NO_PROMOTION_LEDGER)
    if not isinstance(value, dict):
        raise ValueError(f"{rel(NO_PROMOTION_LEDGER)} must contain an object.")
    return value


def transition_errors(
    record: dict[str, Any],
    manifest_core_claim_ids: set[str],
) -> list[str]:
    errors: list[str] = []
    label = str(record.get("_path", record.get("transition_id", "<unknown>")))
    claim_id = str(record.get("claim_id", ""))
    effect = str(record.get("transition_effect", ""))
    old_state = str(record.get("old_support_state", ""))
    new_state = str(record.get("new_support_state", ""))
    support_effect = str(record.get("support_state_effect", ""))

    for field in REQUIRED_TRANSITION_FIELDS:
        if field not in record:
            errors.append(f"{label}: missing required transition field {field}.")
    for field in (
        "claim_surface_refs",
        "claim_record_refs",
        "evidence_roles",
        "required_artifacts",
        "artifact_refs",
        "evidence_packet_refs",
        "negative_results",
        "negative_evidence_refs",
        "downgrade_triggers",
        "limitations",
        "reviewer_refs",
        "non_claims",
    ):
        if not nonempty_list(record.get(field)):
            errors.append(f"{label}: {field} must be a non-empty list.")
    for field in (
        "transition_id",
        "claim_id",
        "scope_boundary",
        "transition_reason",
        "verification_command",
        "verification_result",
        "promotion_burden",
        "reviewer_independence",
        "changelog_ref",
        "support_state_effect",
    ):
        if not nonempty_string(record.get(field)):
            errors.append(f"{label}: {field} must be a non-empty string.")
    if record.get("review_status") != "accepted":
        errors.append(f"{label}: review_status must be accepted.")
    if record.get("transition_validity_state") != "review_accepted":
        errors.append(f"{label}: transition_validity_state must be review_accepted.")
    if record.get("verification_result") != "pass":
        errors.append(f"{label}: verification_result must be pass.")

    if effect == "upward":
        if old_state == new_state:
            errors.append(f"{label}: upward transition must change support state.")
        if claim_id in manifest_core_claim_ids or claim_id.endswith(".core"):
            errors.append(f"{label}: accepted upward transitions must not target chapter core claims.")
        if support_effect != "eligible_for_bounded_evidence_review":
            errors.append(f"{label}: upward transition support_state_effect must be eligible_for_bounded_evidence_review.")
        if record.get("acceptance_blockers") not in ([], None):
            errors.append(f"{label}: accepted upward bounded transitions must not retain acceptance_blockers.")
    elif effect == "no_change":
        if old_state != new_state:
            errors.append(f"{label}: no_change transition must preserve support state.")
        if support_effect not in {
            "argument_only",
            "none",
            "no_support_promotion",
            "blocks_promotion",
            "no_new_support_state_transition",
        }:
            errors.append(f"{label}: no_change support_state_effect must be non-promoting.")
    else:
        errors.append(f"{label}: unsupported accepted transition_effect {effect!r} in this audit.")

    return errors


def ledger_errors(ledger: dict[str, Any], manifest_core_claim_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if ledger.get("review_status") != "accepted":
        errors.append("no-promotion ledger review_status must be accepted.")
    decisions = ledger.get("decisions")
    if not isinstance(decisions, list) or not decisions:
        return ["no-promotion ledger decisions must be a non-empty list."]
    for index, decision in enumerate(decisions):
        label = f"no_promotion.decisions[{index}]"
        if not isinstance(decision, dict):
            errors.append(f"{label}: decision must be an object.")
            continue
        claim_id = str(decision.get("claim_id", ""))
        if claim_id not in manifest_core_claim_ids:
            errors.append(f"{label}: decision claim_id {claim_id!r} is not a current manifest core claim.")
        if decision.get("decision") != "no_promotion":
            errors.append(f"{label}: decision must be no_promotion.")
        if decision.get("current_support_state") != "argument":
            errors.append(f"{label}: current_support_state must be argument.")
        if decision.get("support_state_effect") != "argument_only":
            errors.append(f"{label}: support_state_effect must be argument_only.")
        for field in ("required_evidence", "blockers", "non_claims", "refs"):
            if not nonempty_list(decision.get(field)):
                errors.append(f"{label}: {field} must be a non-empty list.")
    return errors


def mutation_controls(
    records: list[dict[str, Any]],
    ledger: dict[str, Any],
    manifest_core_claim_ids: set[str],
) -> dict[str, bool]:
    controls = {
        "core_upward_transition_rejected": False,
        "missing_changelog_rejected": False,
        "missing_nonclaims_rejected": False,
        "upward_missing_evidence_packet_rejected": False,
        "upward_with_acceptance_blocker_rejected": False,
        "no_change_support_movement_rejected": False,
        "no_promotion_support_effect_rejected": False,
    }
    if not records:
        return controls

    upward = next((record for record in records if record.get("transition_effect") == "upward"), records[0])
    no_change = next((record for record in records if record.get("transition_effect") == "no_change"), records[0])

    core_mutation = deepcopy(upward)
    core_mutation["claim_id"] = sorted(manifest_core_claim_ids)[0]
    controls["core_upward_transition_rejected"] = bool(transition_errors(core_mutation, manifest_core_claim_ids))

    changelog_mutation = deepcopy(no_change)
    changelog_mutation["changelog_ref"] = ""
    controls["missing_changelog_rejected"] = bool(transition_errors(changelog_mutation, manifest_core_claim_ids))

    nonclaim_mutation = deepcopy(no_change)
    nonclaim_mutation["non_claims"] = []
    controls["missing_nonclaims_rejected"] = bool(transition_errors(nonclaim_mutation, manifest_core_claim_ids))

    evidence_mutation = deepcopy(upward)
    evidence_mutation["evidence_packet_refs"] = []
    controls["upward_missing_evidence_packet_rejected"] = bool(
        transition_errors(evidence_mutation, manifest_core_claim_ids)
    )

    blocker_mutation = deepcopy(upward)
    blocker_mutation["acceptance_blockers"] = ["unresolved blocker"]
    controls["upward_with_acceptance_blocker_rejected"] = bool(
        transition_errors(blocker_mutation, manifest_core_claim_ids)
    )

    movement_mutation = deepcopy(no_change)
    movement_mutation["new_support_state"] = "synthetic-test-backed"
    controls["no_change_support_movement_rejected"] = bool(
        transition_errors(movement_mutation, manifest_core_claim_ids)
    )

    ledger_mutation = deepcopy(ledger)
    if isinstance(ledger_mutation.get("decisions"), list) and ledger_mutation["decisions"]:
        ledger_mutation["decisions"][0]["support_state_effect"] = "promote"
    controls["no_promotion_support_effect_rejected"] = bool(
        ledger_errors(ledger_mutation, manifest_core_claim_ids)
    )
    return controls


def build_expected_result(
    records: list[dict[str, Any]],
    ledger: dict[str, Any],
    controls: dict[str, bool],
    manifest_core_claim_ids: set[str],
) -> dict[str, Any]:
    upward = [record for record in records if record.get("transition_effect") == "upward"]
    no_change = [record for record in records if record.get("transition_effect") == "no_change"]
    core_upward = [
        record
        for record in records
        if record.get("transition_effect") == "upward"
        and (record.get("claim_id") in manifest_core_claim_ids or str(record.get("claim_id", "")).endswith(".core"))
    ]
    decisions = ledger.get("decisions", [])
    return {
        "schema_version": "asi_stack.accepted_transition_review_audit.v0",
        "result_id": "2026-07-02-accepted-transition-review-audit",
        "recorded_date": "2026-07-02",
        "command": COMMAND,
        "result_kind": "real_accepted_transition_and_no_promotion_review_audit",
        "accepted_transition_record_count": len(records),
        "accepted_no_change_record_count": len(no_change),
        "accepted_bounded_upward_non_core_transition_count": len(upward),
        "accepted_core_upward_transition_count": len(core_upward),
        "accepted_no_promotion_decision_count": len(decisions) if isinstance(decisions, list) else 0,
        "manifest_core_claim_count": len(manifest_core_claim_ids),
        "expected_invalid_mutation_control_count": len(controls),
        "negative_controls": controls,
        "coverage": {
            "accepted_records_present": bool(records),
            "bounded_upward_transitions_are_non_core": not core_upward,
            "manifest_core_claims_not_promoted": not core_upward,
            "no_promotion_decisions_present": isinstance(decisions, list) and bool(decisions),
            "changelog_refs_present": all(nonempty_string(record.get("changelog_ref")) for record in records),
            "support_state_effect_bounded": True,
            "non_claim_boundaries_present": True,
        },
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.EvidenceStates",
            "proof_tag": PROOF_TAG,
            "theorem_refs": REQUIRED_THEOREMS,
            "expected": {
                "accepted_records_present": True,
                "bounded_upward_non_core_only": True,
                "core_claims_not_promoted": True,
                "no_promotion_decisions_present": True,
                "changelog_refs_present": True,
                "negative_controls_rejected": True,
                "support_state_effect_bounded": True,
                "non_claim_boundary": True,
            },
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "Audit of already accepted transition/no-promotion records only; no new transition is approved.",
            "Reviewer independence remains local maintainer-agent review unless a separate external review record is added.",
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
    if RESULT.read_text(encoding="utf-8") != serialized:
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
        "acceptedRecordsPresent",
        "boundedUpwardNonCoreOnly",
        "coreClaimsNotPromoted",
        "noPromotionDecisionsPresent",
        "changelogRefsPresent",
        "negativeControlsRejected",
        "supportStateEffectBounded",
        "nonClaimBoundary",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing fixture field {field}.")


def validate_surfaces(errors: list[str]) -> None:
    required = {
        DOC: [
            "Accepted Transition Review Audit",
            rel(RESULT),
            "45 accepted transition records",
            "seven bounded non-core upward transitions",
            "seven expected-invalid mutation controls",
            "no support-state transition",
        ],
        CHAPTER: [
            "Accepted live transition review audit",
            rel(RESULT),
            "45 accepted transition records",
            "seven bounded non-core upward transitions",
        ],
        READER: [
            "accepted live transition review audit",
            "45 accepted transition records",
            "not an external review",
        ],
        OUTLINE: [CODEX_TEST_NAME, PROOF_TAG, rel(RESULT)],
        ROADMAP: [
            "Accepted live transition review audit",
            "real accepted-transition audit",
            "no support-state promotion",
        ],
        CHANGELOG: ["Accepted live transition review audit", rel(RESULT)],
        VALIDATE_BOOK: [
            "scripts/validate_accepted_transition_review_audit.py",
            "docs/accepted_transition_review_audit.md",
            "experiments/accepted_transition_review/results/2026-07-02-local.json",
            'run_validator("validate_accepted_transition_review_audit.py")',
        ],
    }
    for path, phrases in required.items():
        if not path.exists():
            errors.append(f"Missing required accepted transition review surface {rel(path)}.")
            continue
        text = re.sub(r"\s+", " ", path.read_text(encoding="utf-8", errors="ignore")).lower()
        for phrase in phrases:
            if re.sub(r"\s+", " ", phrase).lower() not in text:
                errors.append(f"{rel(path)} missing required phrase {phrase!r}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    structure = load_json(MANIFEST)
    if not isinstance(structure, dict):
        fail(["book_structure.json must contain an object."])
    chapters = flatten_chapters(structure)
    manifest_core_claim_ids = {f"{chapter['id']}.core" for chapter in chapters}

    records = transition_records()
    ledger = decision_ledger()
    if not records:
        errors.append("No accepted transition records found.")
    for record in records:
        errors.extend(transition_errors(record, manifest_core_claim_ids))
    errors.extend(ledger_errors(ledger, manifest_core_claim_ids))

    controls = mutation_controls(records, ledger, manifest_core_claim_ids)
    if len(controls) != 7:
        errors.append("Expected exactly seven expected-invalid mutation controls.")
    for name, rejected in controls.items():
        if not rejected:
            errors.append(f"{name}: expected-invalid mutation control unexpectedly passed.")

    expected = build_expected_result(records, ledger, controls, manifest_core_claim_ids)
    validate_result(expected, args.write_result, errors)
    validate_manifest(errors)
    validate_lean(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)
    print("Accepted transition review audit validation passed.")


if __name__ == "__main__":
    main()

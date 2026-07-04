#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "experiments" / "residual_ledger_storage_replay" / "input" / "residual_ledger_records.json"
RESULT = ROOT / "experiments" / "residual_ledger_storage_replay" / "results" / "2026-07-04-local.json"
DOC = ROOT / "docs" / "residual_ledger_storage_replay.md"
CHAPTER = ROOT / "chapters" / "compact-generative-systems-and-residual-honesty.qmd"
READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "compact-generative-systems-and-residual-honesty.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"
NON_CORE_LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
V1_PROGRESS = ROOT / "docs" / "v1_progress_ledger.md"
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "CompactGenerativeSystems.lean"
TRANSITION = (
    ROOT
    / "evidence_transitions"
    / "v1_x_measured"
    / "residual_ledger_storage_replay_no_change.json"
)

COMMAND = "python3 scripts/validate_residual_ledger_storage_replay.py"
CODEX_TEST_NAME = "Residual ledger storage replay"
LEAN_THEOREM = "residual_ledger_storage_replay_bridge"
REQUIRED_NON_CLAIMS = [
    "does not prove deployed residual-ledger storage",
    "does not prove live residual detection",
    "does not promote any chapter core claim",
    "does not prove model quality or benchmark performance",
]


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Residual ledger storage/replay validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


def entry_digest(previous_digest: str, record: dict[str, Any]) -> str:
    material = {"previous_digest": previous_digest, "record": record}
    return hashlib.sha256(canonical(material).encode("utf-8")).hexdigest()


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def require_fragment(owner: str, text: str, fragment: str, errors: list[str]) -> None:
    if fragment not in text:
        errors.append(f"{owner} missing required fragment: {fragment!r}.")


def validate_record_sequence(records: list[dict[str, Any]]) -> tuple[bool, list[str], list[dict[str, Any]]]:
    reasons: list[str] = []
    replay: list[dict[str, Any]] = []
    states: dict[str, dict[str, Any]] = {}
    previous_digest = "GENESIS"

    for index, record in enumerate(records, start=1):
        entry_id = record.get("entry_id", f"entry-{index}")
        if record.get("sequence") != index:
            reasons.append("sequence_gap")
        if not record.get("owner"):
            reasons.append("owner_missing")
        if not record.get("workload_context_ref"):
            reasons.append("workload_context_missing")
        if record.get("review_status") != "accepted":
            reasons.append("review_not_accepted")
        if record.get("support_state_effect") != "none":
            reasons.append("support_state_promotion_attempt")

        non_claims_blob = text_blob(record.get("non_claims", []))
        for phrase in ("does not prove deployed residual-ledger storage", "does not promote any chapter core claim"):
            if phrase not in non_claims_blob:
                reasons.append("non_claim_boundary_missing")

        residual_id = record.get("residual_id")
        event = record.get("event")
        prior = states.get(residual_id)

        if event == "handoff":
            handoff = record.get("handoff") or {}
            if not prior:
                reasons.append("handoff_without_prior_owner")
            elif handoff.get("from_owner") != prior.get("owner") or handoff.get("to_owner") != record.get("owner"):
                reasons.append("handoff_owner_mismatch")
            if handoff.get("review_status") != "accepted":
                reasons.append("handoff_review_missing")
        elif event == "discharge":
            discharge = record.get("discharge") or {}
            if record.get("status") != "discharged":
                reasons.append("discharge_status_missing")
            if not discharge.get("receipt_ref") or discharge.get("review_status") != "accepted":
                reasons.append("discharge_receipt_or_review_missing")
            if prior and prior.get("owner") != record.get("owner"):
                reasons.append("discharge_owner_mismatch")
        elif event != "create":
            reasons.append("unknown_event")

        digest = entry_digest(previous_digest, record)
        replay.append(
            {
                "entry_id": entry_id,
                "sequence": record.get("sequence"),
                "residual_id": residual_id,
                "event": event,
                "owner": record.get("owner"),
                "status": record.get("status"),
                "workload_context_ref": record.get("workload_context_ref"),
                "previous_digest": previous_digest,
                "entry_digest": digest,
            }
        )
        previous_digest = digest

        if residual_id:
            states[residual_id] = {
                "owner": record.get("owner"),
                "status": record.get("status"),
                "entry_id": entry_id,
            }

    return not reasons, sorted(set(reasons)), replay


def build_result(errors: list[str]) -> dict[str, Any]:
    data = load_json(INPUT)
    if data.get("schema_version") != "asi_stack.residual_ledger_storage_replay.input.v0":
        errors.append(f"{rel(INPUT)} has unexpected schema_version.")
    boundary_blob = text_blob(data.get("required_boundaries", []))
    for phrase in (
        "no deployed residual-ledger storage claim",
        "no live residual detection claim",
        "no chapter-core support-state promotion",
        "no model-quality or benchmark claim",
    ):
        if phrase not in boundary_blob:
            errors.append(f"{rel(INPUT)} missing boundary {phrase!r}.")

    valid_records = data.get("valid_records", [])
    if not isinstance(valid_records, list) or len(valid_records) != 4:
        errors.append(f"{rel(INPUT)} must contain 4 valid_records.")
        valid_records = []
    valid, valid_reasons, replay = validate_record_sequence(valid_records)
    if not valid:
        errors.append(f"{rel(INPUT)} valid_records rejected: {valid_reasons}.")

    control_results = []
    for control in data.get("expected_invalid_controls", []):
        control_records = control.get("records", [])
        accepted, reasons, _ = validate_record_sequence(control_records)
        expected_reason = control.get("expected_reason")
        rejected_for_expected_reason = not accepted and expected_reason in reasons
        if accepted:
            errors.append(f"{control.get('control_id')} unexpectedly accepted.")
        if not rejected_for_expected_reason:
            errors.append(
                f"{control.get('control_id')} missing expected reason {expected_reason!r}; got {reasons}."
            )
        control_results.append(
            {
                "control_id": control.get("control_id"),
                "accepted": accepted,
                "rejected_for_expected_reason": rejected_for_expected_reason,
                "reasons": reasons,
            }
        )

    final_digest = replay[-1]["entry_digest"] if replay else None
    owner_handoff_preserved = any(item["event"] == "handoff" for item in replay)
    discharge_review_required = any(item["event"] == "discharge" for item in replay)
    workload_context_preserved = all(item.get("workload_context_ref") for item in replay)
    invalid_controls_rejected = bool(control_results) and all(
        item["rejected_for_expected_reason"] for item in control_results
    )

    summary = {
        "appendOnlyDigestChainComputed": bool(final_digest),
        "sequenceContinuityChecked": valid and not valid_reasons,
        "ownerHandoffPreserved": owner_handoff_preserved,
        "dischargeReviewRequired": discharge_review_required,
        "workloadContextPreserved": workload_context_preserved,
        "invalidControlsRejected": invalid_controls_rejected,
        "supportStateEffectNone": True,
        "nonClaimBoundary": True,
        "liveStorageNotClaimed": True,
        "deployedLedgerNotClaimed": True,
    }

    return {
        "schema_version": "asi_stack.residual_ledger_storage_replay.result.v0",
        "result_id": "2026-07-04-residual-ledger-storage-replay",
        "recorded_date": "2026-07-04",
        "command": COMMAND,
        "input_ref": rel(INPUT),
        "result_kind": "bounded_residual_ledger_storage_replay",
        "valid_entry_count": len(replay),
        "expected_invalid_control_count": len(control_results),
        "replay_entries": replay,
        "control_results": control_results,
        "replay_summary": summary,
        "final_chain_digest": final_digest,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.CompactGenerativeSystems",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_ref": rel(TRANSITION),
        "verification_result": "pass",
        "residuals": [
            "This is a deterministic local storage/replay fixture over an append-only residual ledger event log.",
            "The fixture checks sequence continuity, digest-chain construction, owner handoff, discharge review, workload-context retention, rejected invalid controls, and no-promotion boundaries.",
            "The fixture is not a deployed residual ledger, not live residual detection, not an external replay, and not proof of model quality, benchmark performance, safety, or chapter-core support.",
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
    actual = RESULT.read_text(encoding="utf-8")
    if actual != serialized:
        errors.append(f"{rel(RESULT)} is stale; run {COMMAND} --write-result.")


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): (
            DOC,
            [
                "Residual Ledger Storage Replay",
                COMMAND,
                rel(RESULT),
                "append-only residual ledger event log",
                "owner handoff",
                "discharge review",
                "workload context",
                "not a deployed residual ledger",
            ],
        ),
        rel(CHAPTER): (
            CHAPTER,
            [
                "Residual ledger storage replay",
                COMMAND,
                rel(RESULT),
                "append-only residual ledger event log",
                "owner handoff",
                "discharge review",
                "workload-context retention",
            ],
        ),
        rel(READER): (
            READER,
            [
                "residual-ledger storage replay",
                "not proof of a deployed residual ledger",
                "owner handoff",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented residual-ledger storage replay",
                COMMAND,
                rel(RESULT),
                LEAN_THEOREM,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "bounded residual-ledger storage/replay fixture",
                rel(RESULT),
                "owner handoff, discharge review, workload context",
                "not live or deployed residual-ledger evidence",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add residual ledger storage replay",
                COMMAND,
                rel(RESULT),
                "blocks_promotion",
            ],
        ),
        rel(LEDGER_MD): (
            LEDGER_MD,
            [
                "residual_storage_replay_backed_not_deployed",
                rel(RESULT),
            ],
        ),
        rel(NON_CORE_LEDGER): (
            NON_CORE_LEDGER,
            [
                "compact-generative-systems.residual_ledger_storage_replay",
                rel(TRANSITION),
                "blocks_promotion",
            ],
        ),
        rel(V1_PROGRESS): (
            V1_PROGRESS,
            [
                "residual ledger storage replay",
                rel(RESULT),
                "no support-state promotion",
            ],
        ),
        rel(VALIDATE_BOOK): (
            VALIDATE_BOOK,
            [
                "scripts/validate_residual_ledger_storage_replay.py",
                rel(RESULT),
                'run_validator("validate_residual_ledger_storage_replay.py")',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "ResidualLedgerStorageReplaySummary",
                "residualLedgerStorageReplaySummary",
                LEAN_THEOREM,
            ],
        ),
        rel(TRANSITION): (
            TRANSITION,
            [
                "v1_x_measured.residual_ledger_storage_replay.no_change",
                "blocks_promotion",
                rel(RESULT),
                "not a deployed residual ledger",
            ],
        ),
    }
    for owner, (path, fragments) in surfaces.items():
        if not path.exists():
            errors.append(f"Missing {owner}.")
            continue
        text = path.read_text(encoding="utf-8")
        for fragment in fragments:
            require_fragment(owner, text, fragment, errors)


def validate_book_structure(errors: list[str]) -> None:
    data = load_json(BOOK_STRUCTURE)
    tests: list[dict[str, Any]] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            maybe_tests = value.get("codex_tests")
            if isinstance(maybe_tests, list):
                tests.extend(test for test in maybe_tests if isinstance(test, dict))
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(data)
    matches = [
        test for test in tests if isinstance(test, dict) and test.get("name") == CODEX_TEST_NAME
    ]
    if len(matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain exactly one {CODEX_TEST_NAME!r} test row.")
        return
    blob = text_blob(matches[0])
    for phrase in (
        "implemented",
        COMMAND,
        "not a deployed residual ledger",
        "blocks_promotion",
    ):
        if phrase not in blob:
            errors.append(f"{CODEX_TEST_NAME} codex test row missing {phrase!r}.")


def validate_ledger_json(errors: list[str]) -> None:
    data = load_json(LEDGER_JSON)
    entries = data.get("records", [])
    matches = [
        entry
        for entry in entries
        if isinstance(entry, dict)
        and entry.get("idea_id") == "residual_honesty"
    ]
    if len(matches) != 1:
        errors.append(f"{rel(LEDGER_JSON)} missing residual honesty contribution row.")
        return
    blob = text_blob(matches[0])
    for phrase in (
        "residual_storage_replay_backed_not_deployed",
        rel(RESULT),
        "does not prove deployed residual-ledger storage",
    ):
        if phrase not in blob:
            errors.append(f"{rel(LEDGER_JSON)} residual row missing {phrase!r}.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    if not re.search(rf"theorem\s+{re.escape(LEAN_THEOREM)}\b", text):
        errors.append(f"{rel(LEAN_FILE)} missing theorem {LEAN_THEOREM}.")
    for field in (
        "appendOnlyDigestChainComputed",
        "sequenceContinuityChecked",
        "ownerHandoffPreserved",
        "dischargeReviewRequired",
        "workloadContextPreserved",
        "invalidControlsRejected",
        "supportStateEffectNone",
        "nonClaimBoundary",
        "liveStorageNotClaimed",
        "deployedLedgerNotClaimed",
    ):
        if field not in text:
            errors.append(f"{rel(LEAN_FILE)} missing residual storage/replay field {field}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    if not INPUT.exists():
        errors.append(f"Missing required input {rel(INPUT)}.")
        fail(errors)

    expected = build_result(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(errors)
        validate_book_structure(errors)
        validate_ledger_json(errors)
        validate_lean_shape(errors)

    if errors:
        fail(errors)
    print(
        "Residual ledger storage/replay validation passed: "
        f"{expected['valid_entry_count']} replay entries, "
        f"{expected['expected_invalid_control_count']} invalid controls rejected, "
        "no support-state effect."
    )


if __name__ == "__main__":
    main()

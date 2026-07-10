#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "receipt_repository_audit" / "results" / "2026-07-03-local.json"
DOC = ROOT / "docs" / "receipt_repository_audit.md"
ARTIFACT_CHAPTER = ROOT / "chapters" / "artifact-graphs-audit-logs-and-replay.qmd"
ARTIFACT_READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "artifact-graphs-audit-logs-and-replay.qmd"
)
OUTLINE = ROOT / "docs" / "book_outline.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"
LEDGER_MD = ROOT / "docs" / "contribution_novelty_ledger.md"
LEDGER_JSON = ROOT / "docs" / "contribution_novelty_ledger.json"
VALIDATION_REGISTRY = ROOT / "validation" / "registry.json"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ArtifactGraph.lean"

COMMAND = "python3 scripts/validate_receipt_repository_audit.py"
RESULT_ID = "receipt-repository-audit-2026-07-03-local"
LEAN_THEOREM = "receipt_repository_audit_fixture_bridge"
CODEX_TEST_NAME = "Receipt repository audit"

AUDITED_RECEIPTS = [
    {
        "receipt_id": "resource_flagship_lane",
        "path": "experiments/resource_flagship_lane/results/2026-07-01-local.json",
        "command_field": "command_records",
        "expected_support_state_effect": "none",
        "expect_tracked_artifacts": True,
        "receipt_shape": "local_aggregate_digest_bundle",
    },
    {
        "receipt_id": "theseus_fast_support_lane",
        "path": "experiments/theseus_fast_support_lane/results/2026-07-03-local.json",
        "command_field": "replay_commands",
        "expected_support_state_effect": "none",
        "expect_tracked_artifacts": True,
        "receipt_shape": "public_safe_project_support_bundle",
    },
    {
        "receipt_id": "reference_trace_replay",
        "path": "experiments/reference_trace/replay_results/2026-07-02-resource-flagship.json",
        "command_field": "actual_command_record",
        "expected_support_state_effect": "record_shape_only",
        "expect_tracked_artifacts": True,
        "receipt_shape": "local_reference_trace_replay",
    },
    {
        "receipt_id": "circle_external_rope_receipt_slice",
        "path": "experiments/circle_external_receipt_slice/results/2026-06-29-local.json",
        "command_field": "commands",
        "expected_support_state_effect": "eligible_for_bounded_evidence_review",
        "expect_tracked_artifacts": False,
        "receipt_shape": "external_receipt_fingerprint_summary",
    },
]

REQUIRED_NON_CLAIM_PHRASES = (
    "does not promote",
    "does not prove",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Receipt repository audit validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def command_records(data: dict[str, Any], field: str) -> list[dict[str, Any]]:
    value = data.get(field)
    if field == "actual_command_record" and isinstance(value, dict):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, dict)]
    return []


def command_passes(record: dict[str, Any]) -> bool:
    if "exit_code" in record:
        return record.get("exit_code") == 0
    return str(record.get("verification_result", "")).lower() == "pass"


def support_effect(data: dict[str, Any]) -> str:
    if "support_state_effect" in data:
        return str(data.get("support_state_effect"))
    transition = data.get("support_transition")
    if isinstance(transition, dict):
        return str(transition.get("support_state_effect", ""))
    return ""


def chapter_core_effect(data: dict[str, Any]) -> str:
    return str(data.get("chapter_core_support_effect", "none"))


def artifact_ref_errors(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    refs = data.get("artifact_refs", [])
    if not isinstance(refs, list) or not refs:
        return ["artifact_refs_missing"]
    for ref in refs:
        if not isinstance(ref, str) or not ref:
            errors.append("artifact_ref_invalid")
            continue
        if not (ROOT / ref).exists():
            errors.append(f"artifact_ref_missing={ref}")
    return errors


def tracked_artifact_errors(data: dict[str, Any], expect_tracked: bool) -> tuple[list[str], int]:
    errors: list[str] = []
    tracked = data.get("tracked_artifacts", [])
    if not expect_tracked:
        return errors, 0
    if not isinstance(tracked, list) or not tracked:
        return ["tracked_artifacts_missing"], 0
    checked = 0
    for item in tracked:
        if not isinstance(item, dict):
            errors.append("tracked_artifact_invalid")
            continue
        path_value = item.get("path")
        expected_sha = item.get("sha256")
        if not isinstance(path_value, str) or not path_value:
            errors.append("tracked_artifact_path_missing")
            continue
        path = ROOT / path_value
        if not path.exists():
            errors.append(f"tracked_artifact_missing={path_value}")
            continue
        if not isinstance(expected_sha, str) or not expected_sha:
            errors.append(f"tracked_artifact_sha_missing={path_value}")
            continue
        actual_sha = sha256(path)
        if actual_sha != expected_sha:
            errors.append(f"tracked_artifact_sha_mismatch={path_value}")
            continue
        checked += 1
    return errors, checked


def circle_fingerprint_errors(data: dict[str, Any]) -> tuple[list[str], int]:
    fingerprints = 0
    errors: list[str] = []
    for command in command_records(data, "commands"):
        for key in (
            "receipt_content_fingerprint",
            "normalized_request_fingerprint",
            "contract_pack_fingerprint",
            "pack_content_fingerprint",
            "contract_content_fingerprint",
        ):
            value = command.get(key)
            if isinstance(value, str) and len(value) >= 32:
                fingerprints += 1
    accepted = data.get("accepted_receipt")
    if not isinstance(accepted, dict) or accepted.get("accepted") is not True:
        errors.append("accepted_receipt_missing")
    if fingerprints < 4:
        errors.append("external_receipt_fingerprints_missing")
    return errors, fingerprints


def receipt_rejection_reasons(spec: dict[str, Any], data: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    expected_effect = str(spec["expected_support_state_effect"])
    actual_effect = support_effect(data)
    if actual_effect != expected_effect:
        reasons.append(f"support_state_effect_mismatch={actual_effect}")

    if chapter_core_effect(data) not in {"none", "argument_only"}:
        reasons.append("chapter_core_support_effect_not_none")
    if data.get("evidence_transition_created") is True:
        reasons.append("new_evidence_transition_created")

    non_claims = data.get("non_claims")
    non_claim_text = text_blob(non_claims)
    if not isinstance(non_claims, list) or len(non_claims) < 2:
        reasons.append("non_claims_missing")
    for phrase in REQUIRED_NON_CLAIM_PHRASES:
        if phrase not in non_claim_text:
            reasons.append(f"non_claim_phrase_missing={phrase}")

    commands = command_records(data, str(spec["command_field"]))
    if not commands:
        reasons.append("command_records_missing")
    failed_commands = [
        str(record.get("id") or record.get("command") or "unknown")
        for record in commands
        if not command_passes(record)
    ]
    if failed_commands:
        reasons.append("command_replay_failed=" + ",".join(sorted(failed_commands)))

    if spec.get("receipt_id") == "circle_external_rope_receipt_slice":
        fingerprint_errors, _fingerprint_count = circle_fingerprint_errors(data)
        reasons.extend(fingerprint_errors)
        if data.get("verification_result") != "pass":
            reasons.append("external_receipt_verification_not_pass")
    else:
        reasons.extend(artifact_ref_errors(data))
        tracked_errors, _tracked_count = tracked_artifact_errors(
            data,
            expect_tracked=spec.get("expect_tracked_artifacts") is True,
        )
        reasons.extend(tracked_errors)

    return sorted(set(reasons))


def audit_receipt(spec: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
    path = ROOT / str(spec["path"])
    data = load_json(path)
    reasons = receipt_rejection_reasons(spec, data)
    tracked_errors, tracked_count = tracked_artifact_errors(
        data,
        expect_tracked=spec.get("expect_tracked_artifacts") is True,
    )
    _fingerprint_errors, fingerprint_count = circle_fingerprint_errors(data) if spec.get("receipt_id") == "circle_external_rope_receipt_slice" else ([], 0)
    commands = command_records(data, str(spec["command_field"]))
    row = {
        "receipt_id": spec["receipt_id"],
        "receipt_ref": spec["path"],
        "receipt_shape": spec["receipt_shape"],
        "accepted": not reasons,
        "rejection_reasons": reasons,
        "support_state_effect": support_effect(data),
        "chapter_core_support_effect": chapter_core_effect(data),
        "command_pass_count": sum(1 for record in commands if command_passes(record)),
        "command_count": len(commands),
        "artifact_ref_count": len(data.get("artifact_refs", [])) if isinstance(data.get("artifact_refs"), list) else 0,
        "tracked_artifact_digest_count": tracked_count,
        "external_fingerprint_count": fingerprint_count,
        "non_claim_count": len(data.get("non_claims", [])) if isinstance(data.get("non_claims"), list) else 0,
    }
    return row, tracked_errors


def mutation_controls(specs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    controls: list[dict[str, Any]] = []
    first_spec = specs[0]
    first_data = load_json(ROOT / str(first_spec["path"]))

    missing_artifact = deepcopy(first_data)
    missing_artifact["artifact_refs"] = ["docs/does-not-exist-for-receipt-audit.md"]
    controls.append(
        {
            "control_id": "invalid_missing_artifact_ref",
            "rejected": bool(receipt_rejection_reasons(first_spec, missing_artifact)),
            "rejection_reasons": receipt_rejection_reasons(first_spec, missing_artifact),
        }
    )

    digest_mismatch = deepcopy(first_data)
    if isinstance(digest_mismatch.get("tracked_artifacts"), list) and digest_mismatch["tracked_artifacts"]:
        digest_mismatch["tracked_artifacts"][0]["sha256"] = "0" * 64
    controls.append(
        {
            "control_id": "invalid_tracked_digest_mismatch",
            "rejected": bool(receipt_rejection_reasons(first_spec, digest_mismatch)),
            "rejection_reasons": receipt_rejection_reasons(first_spec, digest_mismatch),
        }
    )

    failed_command = deepcopy(first_data)
    if isinstance(failed_command.get("command_records"), list) and failed_command["command_records"]:
        failed_command["command_records"][0]["exit_code"] = 1
    controls.append(
        {
            "control_id": "invalid_failed_command_replay",
            "rejected": bool(receipt_rejection_reasons(first_spec, failed_command)),
            "rejection_reasons": receipt_rejection_reasons(first_spec, failed_command),
        }
    )

    missing_non_claims = deepcopy(first_data)
    missing_non_claims["non_claims"] = []
    controls.append(
        {
            "control_id": "invalid_missing_non_claims",
            "rejected": bool(receipt_rejection_reasons(first_spec, missing_non_claims)),
            "rejection_reasons": receipt_rejection_reasons(first_spec, missing_non_claims),
        }
    )

    support_promotion = deepcopy(first_data)
    support_promotion["support_state_effect"] = "promote_chapter_core"
    support_promotion["chapter_core_support_effect"] = "promoted"
    support_promotion["evidence_transition_created"] = True
    controls.append(
        {
            "control_id": "invalid_support_promotion_overclaim",
            "rejected": bool(receipt_rejection_reasons(first_spec, support_promotion)),
            "rejection_reasons": receipt_rejection_reasons(first_spec, support_promotion),
        }
    )

    return controls


def build_result(errors: list[str]) -> dict[str, Any]:
    audited_rows: list[dict[str, Any]] = []
    for spec in AUDITED_RECEIPTS:
        path = ROOT / str(spec["path"])
        if not path.exists():
            errors.append(f"Missing audited receipt {spec['path']}.")
            continue
        row, _tracked_errors = audit_receipt(spec)
        audited_rows.append(row)
        if not row["accepted"]:
            errors.append(f"{spec['receipt_id']} rejected: {', '.join(row['rejection_reasons'])}.")

    controls = mutation_controls(AUDITED_RECEIPTS)
    for control in controls:
        if not control["rejected"]:
            errors.append(f"{control['control_id']} mutation control was not rejected.")

    summary = {
        "audited_receipt_count": len(audited_rows),
        "accepted_receipt_count": sum(1 for row in audited_rows if row["accepted"]),
        "digest_checked_receipt_count": sum(1 for row in audited_rows if row["tracked_artifact_digest_count"] > 0),
        "external_fingerprint_receipt_count": sum(1 for row in audited_rows if row["external_fingerprint_count"] > 0),
        "command_replay_receipt_count": sum(1 for row in audited_rows if row["command_pass_count"] > 0),
        "tracked_artifact_digest_count": sum(int(row["tracked_artifact_digest_count"]) for row in audited_rows),
        "mutation_control_count": len(controls),
        "support_state_effect_none_or_record_only": all(
            row["support_state_effect"] in {"none", "record_shape_only", "eligible_for_bounded_evidence_review"}
            and row["chapter_core_support_effect"] in {"none", "argument_only"}
            for row in audited_rows
        ),
        "non_claim_boundary": all(row["non_claim_count"] >= 2 for row in audited_rows),
        "missing_artifact_control_rejected": any(
            control["control_id"] == "invalid_missing_artifact_ref" and control["rejected"]
            for control in controls
        ),
        "digest_mismatch_control_rejected": any(
            control["control_id"] == "invalid_tracked_digest_mismatch" and control["rejected"]
            for control in controls
        ),
        "failed_command_control_rejected": any(
            control["control_id"] == "invalid_failed_command_replay" and control["rejected"]
            for control in controls
        ),
        "missing_non_claims_control_rejected": any(
            control["control_id"] == "invalid_missing_non_claims" and control["rejected"]
            for control in controls
        ),
        "support_promotion_control_rejected": any(
            control["control_id"] == "invalid_support_promotion_overclaim" and control["rejected"]
            for control in controls
        ),
    }

    return {
        "schema_version": "asi_stack.receipt_repository_audit.result.v0",
        "result_id": RESULT_ID,
        "recorded_date": "2026-07-03",
        "command": COMMAND,
        "result_kind": "repository_receipt_reality_audit",
        "audited_receipts": audited_rows,
        "mutation_controls": controls,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ArtifactGraph",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "This audit checks selected existing repository receipts and summaries; it does not replay all upstream systems.",
            "Tracked digest checks cover files in this repository only; the Circle slice remains an external summary with fingerprints.",
            "The audit preserves no-promotion boundaries and does not prove open-world receipt faithfulness.",
        ],
        "non_claims": [
            "does not prove open-world receipt faithfulness",
            "does not prove deployed attestation or audit behavior",
            "does not prove verifier correctness or external project truth",
            "does not promote any chapter core claim",
            "does not create an evidence transition",
        ],
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


def require_fragment(owner: str, text: str, fragment: str, errors: list[str]) -> None:
    if fragment not in text:
        errors.append(f"{owner} missing required fragment: {fragment!r}.")


def validate_surfaces(errors: list[str]) -> None:
    surfaces = {
        rel(DOC): (
            DOC,
            [
                "Receipt Repository Audit",
                COMMAND,
                rel(RESULT),
                "Resource flagship",
                "Theseus/Fast support",
                "Circle external rope",
                "invalid_tracked_digest_mismatch",
                "no support-state promotion",
            ],
        ),
        rel(ARTIFACT_CHAPTER): (
            ARTIFACT_CHAPTER,
            [
                "Receipt repository audit",
                COMMAND,
                rel(RESULT),
                "tracked digest",
                "external receipt fingerprints",
            ],
        ),
        rel(ARTIFACT_READER): (
            ARTIFACT_READER,
            [
                "receipt repository audit",
                "tracked digests",
                "external receipt fingerprints",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented receipt repository audit",
                COMMAND,
                rel(RESULT),
                LEAN_THEOREM,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "receipt repository audit",
                rel(RESULT),
                "tracked digest",
                "Circle external rope",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add receipt repository audit",
                COMMAND,
                rel(RESULT),
                "does not create a support-state transition",
            ],
        ),
        rel(LEDGER_MD): (
            LEDGER_MD,
            [
                "Record-reality gap",
                rel(RESULT),
                "repository_receipt_audit_backed_not_open_world",
            ],
        ),
        rel(VALIDATION_REGISTRY): (
            VALIDATION_REGISTRY,
            [
                "scripts/validate_receipt_repository_audit.py",
                "docs/receipt_repository_audit.md",
                rel(RESULT),
                '"script": "validate_receipt_repository_audit.py"',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "ReceiptRepositoryAuditSummary",
                "receiptRepositoryAuditSummary",
                LEAN_THEOREM,
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


def validate_ledger_json(errors: list[str]) -> None:
    data = load_json(LEDGER_JSON)
    records = data.get("records", [])
    matches = [
        record
        for record in records
        if isinstance(record, dict) and record.get("idea_id") == "receipt_faithfulness_gap"
    ]
    if len(matches) != 1:
        errors.append(f"{rel(LEDGER_JSON)} must contain one receipt_faithfulness_gap row.")
        return
    blob = text_blob(matches[0])
    for phrase in (
        rel(RESULT),
        "repository_receipt_audit_backed_not_open_world",
        "does not prove open-world receipt faithfulness",
    ):
        if phrase not in blob:
            errors.append(f"{rel(LEDGER_JSON)} receipt_faithfulness_gap row missing {phrase!r}.")


def validate_book_structure(errors: list[str]) -> None:
    data = load_json(BOOK_STRUCTURE)
    tests: list[dict[str, Any]] = []
    for part in data.get("parts", []):
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict):
                tests.extend(test for test in chapter.get("codex_tests", []) if isinstance(test, dict))
    matches = [test for test in tests if test.get("name") == CODEX_TEST_NAME]
    if len(matches) != 1:
        errors.append(f"{rel(BOOK_STRUCTURE)} must contain exactly one {CODEX_TEST_NAME!r} test row.")
        return
    blob = text_blob(matches[0])
    for phrase in (COMMAND, "tracked digest", "no support-state promotion"):
        if phrase not in blob:
            errors.append(f"{CODEX_TEST_NAME} codex test row missing {phrase!r}.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    for fragment in (
        "ReceiptRepositoryAuditSummary",
        "receiptRepositoryAuditSummary",
        "ReceiptRepositoryAuditValid",
        LEAN_THEOREM,
        "digestMismatchControlRejected",
        "supportPromotionControlRejected",
    ):
        if fragment not in text:
            errors.append(f"{rel(LEAN_FILE)} missing {fragment}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    expected = build_result(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(errors)
        validate_ledger_json(errors)
        validate_book_structure(errors)
        validate_lean_shape(errors)
    if errors:
        fail(errors)
    print(
        "Receipt repository audit validation passed: "
        f"{expected['trace_summary']['accepted_receipt_count']} receipt record(s), "
        f"{expected['trace_summary']['tracked_artifact_digest_count']} tracked digest check(s), "
        f"{expected['trace_summary']['mutation_control_count']} mutation control(s), "
        "no support-state effect."
    )


if __name__ == "__main__":
    main()

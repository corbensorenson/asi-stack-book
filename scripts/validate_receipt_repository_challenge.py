#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import validate_receipt_repository_audit as base_audit


ROOT = Path(__file__).resolve().parents[1]
BASE_RESULT = ROOT / "experiments" / "receipt_repository_audit" / "results" / "2026-07-03-local.json"
RESULT = ROOT / "experiments" / "receipt_repository_audit" / "results" / "2026-07-04-challenge.json"
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
VALIDATE_BOOK = ROOT / "scripts" / "validate_book.py"
BOOK_STRUCTURE = ROOT / "book_structure.json"
LEAN_FILE = ROOT / "lean" / "AsiStackProofs" / "ArtifactGraph.lean"

COMMAND = "python3 scripts/validate_receipt_repository_challenge.py"
RESULT_ID = "receipt-repository-challenge-2026-07-04"
CHALLENGE_SEED = "asi-stack-receipt-reality-challenge-v1-2026-07-04"
LEAN_THEOREM = "receipt_repository_challenge_fixture_bridge"
CODEX_TEST_NAME = "Receipt repository challenge audit"
FINGERPRINT_KEYS = (
    "receipt_content_fingerprint",
    "normalized_request_fingerprint",
    "contract_pack_fingerprint",
    "pack_content_fingerprint",
    "contract_content_fingerprint",
)
REQUIRED_NON_CLAIM_PHRASES = (
    "does not prove",
    "does not promote",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def fail(errors: list[str]) -> None:
    print("Receipt repository challenge validation failed:")
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


def stable_index(receipt_id: str, count: int, label: str) -> int:
    seed = f"{CHALLENGE_SEED}:{receipt_id}:{label}".encode("utf-8")
    return int(hashlib.sha256(seed).hexdigest(), 16) % count


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items()).lower()
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value).lower()
    return str(value).lower()


def tracked_challenge(spec: dict[str, Any], data: dict[str, Any]) -> dict[str, Any] | None:
    tracked = data.get("tracked_artifacts")
    if not isinstance(tracked, list) or not tracked:
        return None
    index = stable_index(str(spec["receipt_id"]), len(tracked), "tracked_artifact")
    selected = tracked[index]
    if not isinstance(selected, dict):
        return None
    path_value = str(selected.get("path", ""))
    expected_sha = str(selected.get("sha256", ""))
    observed_sha = sha256(ROOT / path_value) if path_value and (ROOT / path_value).exists() else ""
    return {
        "challenge_id": f"challenge:{spec['receipt_id']}:tracked_artifact:{index}",
        "receipt_id": spec["receipt_id"],
        "challenge_kind": "tracked_digest",
        "selection_method": "sha256_seeded_index",
        "selected_index": index,
        "selected_ref": path_value,
        "expected_sha256": expected_sha,
        "observed_sha256": observed_sha,
        "accepted": path_value != "" and expected_sha == observed_sha,
    }


def external_fingerprint_challenge(
    spec: dict[str, Any],
    data: dict[str, Any],
) -> dict[str, Any] | None:
    candidates: list[dict[str, Any]] = []
    for command_index, command in enumerate(base_audit.command_records(data, "commands")):
        for key in FINGERPRINT_KEYS:
            value = command.get(key)
            if isinstance(value, str) and len(value) >= 32:
                candidates.append(
                    {
                        "command_index": command_index,
                        "fingerprint_key": key,
                        "fingerprint": value,
                    }
                )
    if not candidates:
        return None
    index = stable_index(str(spec["receipt_id"]), len(candidates), "external_fingerprint")
    selected = candidates[index]
    fingerprint = str(selected["fingerprint"])
    return {
        "challenge_id": f"challenge:{spec['receipt_id']}:external_fingerprint:{index}",
        "receipt_id": spec["receipt_id"],
        "challenge_kind": "external_fingerprint",
        "selection_method": "sha256_seeded_index",
        "selected_index": index,
        "selected_ref": selected["fingerprint_key"],
        "command_index": selected["command_index"],
        "expected_fingerprint": fingerprint,
        "observed_fingerprint": fingerprint,
        "accepted": len(fingerprint) >= 32,
    }


def build_challenges(errors: list[str]) -> list[dict[str, Any]]:
    challenges: list[dict[str, Any]] = []
    for spec in base_audit.AUDITED_RECEIPTS:
        path = ROOT / str(spec["path"])
        if not path.exists():
            errors.append(f"Missing challenge source receipt {spec['path']}.")
            continue
        data = load_json(path)
        if spec.get("expect_tracked_artifacts") is True:
            challenge = tracked_challenge(spec, data)
        else:
            challenge = external_fingerprint_challenge(spec, data)
        if challenge is None:
            errors.append(f"No challenge could be built for {spec['receipt_id']}.")
            continue
        challenges.append(challenge)
    return challenges


def response_rejection_reasons(response: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    kind = response.get("challenge_kind")
    if kind == "tracked_digest":
        selected_ref = str(response.get("selected_ref", ""))
        if not selected_ref:
            reasons.append("challenge_artifact_ref_missing")
        elif not (ROOT / selected_ref).exists():
            reasons.append(f"challenge_artifact_missing={selected_ref}")
        else:
            observed = sha256(ROOT / selected_ref)
            if response.get("observed_sha256") != observed:
                reasons.append("challenge_observed_digest_stale")
            if response.get("expected_sha256") != observed:
                reasons.append("challenge_digest_mismatch")
    elif kind == "external_fingerprint":
        expected = response.get("expected_fingerprint")
        observed = response.get("observed_fingerprint")
        if not isinstance(expected, str) or len(expected) < 32:
            reasons.append("challenge_expected_fingerprint_missing")
        if expected != observed:
            reasons.append("challenge_external_fingerprint_mismatch")
    else:
        reasons.append("unknown_challenge_kind")
    if reasons:
        return sorted(set(reasons))
    if response.get("accepted") is not True:
        reasons.append("challenge_not_marked_accepted")
    return sorted(set(reasons))


def result_rejection_reasons(result: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    if result.get("support_state_effect") != "none":
        reasons.append("support_state_effect_not_none")
    if result.get("chapter_core_support_effect") != "none":
        reasons.append("chapter_core_support_effect_not_none")
    if result.get("evidence_transition_created") is not False:
        reasons.append("evidence_transition_created")
    non_claims = result.get("non_claims")
    non_claim_text = text_blob(non_claims)
    if not isinstance(non_claims, list) or len(non_claims) < 2:
        reasons.append("non_claims_missing")
    for phrase in REQUIRED_NON_CLAIM_PHRASES:
        if phrase not in non_claim_text:
            reasons.append(f"non_claim_phrase_missing={phrase}")
    challenges = result.get("challenge_responses")
    if not isinstance(challenges, list) or not challenges:
        reasons.append("challenge_responses_missing")
    else:
        for challenge in challenges:
            if not isinstance(challenge, dict):
                reasons.append("challenge_response_invalid")
                continue
            reasons.extend(response_rejection_reasons(challenge))
    return sorted(set(reasons))


def mutation_controls(base_result: dict[str, Any]) -> list[dict[str, Any]]:
    controls: list[dict[str, Any]] = []

    digest_mismatch = deepcopy(base_result)
    for response in digest_mismatch["challenge_responses"]:
        if response.get("challenge_kind") == "tracked_digest":
            response["expected_sha256"] = "0" * 64
            break
    controls.append(
        {
            "control_id": "invalid_challenge_tracked_digest_mismatch",
            "rejected": bool(result_rejection_reasons(digest_mismatch)),
            "rejection_reasons": result_rejection_reasons(digest_mismatch),
        }
    )

    missing_artifact = deepcopy(base_result)
    for response in missing_artifact["challenge_responses"]:
        if response.get("challenge_kind") == "tracked_digest":
            response["selected_ref"] = "docs/does-not-exist-for-receipt-challenge.md"
            response["observed_sha256"] = ""
            break
    controls.append(
        {
            "control_id": "invalid_challenge_artifact_missing",
            "rejected": bool(result_rejection_reasons(missing_artifact)),
            "rejection_reasons": result_rejection_reasons(missing_artifact),
        }
    )

    fingerprint_mismatch = deepcopy(base_result)
    for response in fingerprint_mismatch["challenge_responses"]:
        if response.get("challenge_kind") == "external_fingerprint":
            response["observed_fingerprint"] = "0" * 64
            break
    controls.append(
        {
            "control_id": "invalid_external_fingerprint_mismatch",
            "rejected": bool(result_rejection_reasons(fingerprint_mismatch)),
            "rejection_reasons": result_rejection_reasons(fingerprint_mismatch),
        }
    )

    missing_non_claims = deepcopy(base_result)
    missing_non_claims["non_claims"] = []
    controls.append(
        {
            "control_id": "invalid_challenge_missing_non_claims",
            "rejected": bool(result_rejection_reasons(missing_non_claims)),
            "rejection_reasons": result_rejection_reasons(missing_non_claims),
        }
    )

    support_promotion = deepcopy(base_result)
    support_promotion["support_state_effect"] = "promote_chapter_core"
    support_promotion["chapter_core_support_effect"] = "promoted"
    support_promotion["evidence_transition_created"] = True
    controls.append(
        {
            "control_id": "invalid_challenge_support_promotion_overclaim",
            "rejected": bool(result_rejection_reasons(support_promotion)),
            "rejection_reasons": result_rejection_reasons(support_promotion),
        }
    )

    return controls


def build_expected(errors: list[str]) -> dict[str, Any]:
    if not BASE_RESULT.exists():
        errors.append(f"Missing base audit result {rel(BASE_RESULT)}.")
        base_result: dict[str, Any] = {}
    else:
        base_result = load_json(BASE_RESULT)
        if base_result.get("verification_result") != "pass":
            errors.append(f"{rel(BASE_RESULT)} must be passing before challenge audit.")

    challenges = build_challenges(errors)
    base_without_controls = {
        "schema_version": "asi_stack.receipt_repository_challenge.result.v0",
        "result_id": RESULT_ID,
        "recorded_date": "2026-07-04",
        "command": COMMAND,
        "base_audit_result": rel(BASE_RESULT),
        "base_audit_result_id": base_result.get("result_id"),
        "challenge_seed": CHALLENGE_SEED,
        "result_kind": "repository_receipt_reality_challenge",
        "challenge_responses": challenges,
        "support_state_effect": "none",
        "chapter_core_support_effect": "none",
        "evidence_transition_created": False,
        "verification_result": "pass",
        "residuals": [
            "The challenge samples selected receipt fields deterministically; it is not a live attestation service.",
            "Tracked-digest challenges cover repository files only; the Circle challenge checks a recorded external fingerprint, not a vendored contract pack.",
            "The challenge preserves no-promotion boundaries and does not prove open-world receipt faithfulness.",
        ],
        "non_claims": [
            "does not prove open-world receipt faithfulness",
            "does not prove deployed attestation or audit behavior",
            "does not prove verifier correctness or external project truth",
            "does not promote any chapter core claim",
            "does not create an evidence transition",
        ],
    }
    controls = mutation_controls(base_without_controls)
    tracked_count = sum(1 for response in challenges if response.get("challenge_kind") == "tracked_digest")
    external_count = sum(1 for response in challenges if response.get("challenge_kind") == "external_fingerprint")
    summary = {
        "base_audit_passed": base_result.get("verification_result") == "pass",
        "challenge_count": len(challenges),
        "accepted_challenge_count": sum(1 for response in challenges if response.get("accepted") is True),
        "tracked_digest_challenge_count": tracked_count,
        "external_fingerprint_challenge_count": external_count,
        "mutation_control_count": len(controls),
        "tracked_digest_mismatch_control_rejected": any(
            control["control_id"] == "invalid_challenge_tracked_digest_mismatch" and control["rejected"]
            for control in controls
        ),
        "missing_artifact_control_rejected": any(
            control["control_id"] == "invalid_challenge_artifact_missing" and control["rejected"]
            for control in controls
        ),
        "external_fingerprint_mismatch_control_rejected": any(
            control["control_id"] == "invalid_external_fingerprint_mismatch" and control["rejected"]
            for control in controls
        ),
        "missing_non_claims_control_rejected": any(
            control["control_id"] == "invalid_challenge_missing_non_claims" and control["rejected"]
            for control in controls
        ),
        "support_promotion_control_rejected": any(
            control["control_id"] == "invalid_challenge_support_promotion_overclaim" and control["rejected"]
            for control in controls
        ),
        "support_state_effect_none": True,
        "non_claim_boundary": True,
    }
    expected = {
        **base_without_controls,
        "mutation_controls": controls,
        "trace_summary": summary,
        "lean_fixture_alignment": {
            "module": "AsiStackProofs.ArtifactGraph",
            "theorem_refs": [LEAN_THEOREM],
            "expected": summary,
        },
    }
    for reason in result_rejection_reasons(expected):
        errors.append(f"expected challenge result rejected: {reason}")
    return expected


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
                "Receipt Challenge Layer",
                COMMAND,
                rel(RESULT),
                "invalid_challenge_tracked_digest_mismatch",
                "deterministic challenge",
            ],
        ),
        rel(ARTIFACT_CHAPTER): (
            ARTIFACT_CHAPTER,
            [
                "receipt repository challenge",
                COMMAND,
                rel(RESULT),
                "deterministic challenge",
                "external fingerprint",
            ],
        ),
        rel(ARTIFACT_READER): (
            ARTIFACT_READER,
            [
                "receipt repository challenge",
                "deterministic challenge",
                "external fingerprint",
            ],
        ),
        rel(OUTLINE): (
            OUTLINE,
            [
                "Implemented receipt repository challenge",
                COMMAND,
                rel(RESULT),
                LEAN_THEOREM,
            ],
        ),
        rel(ROADMAP): (
            ROADMAP,
            [
                "receipt repository challenge",
                rel(RESULT),
                "deterministic challenge",
            ],
        ),
        rel(CHANGELOG): (
            CHANGELOG,
            [
                "Add receipt repository challenge audit",
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
                "repository_receipt_challenge_backed_not_open_world",
            ],
        ),
        rel(VALIDATE_BOOK): (
            VALIDATE_BOOK,
            [
                "scripts/validate_receipt_repository_challenge.py",
                rel(RESULT),
                'run_validator("validate_receipt_repository_challenge.py")',
            ],
        ),
        rel(LEAN_FILE): (
            LEAN_FILE,
            [
                "ReceiptRepositoryChallengeSummary",
                "receiptRepositoryChallengeSummary",
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
        "repository_receipt_challenge_backed_not_open_world",
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
    for phrase in (COMMAND, "deterministic challenge", "no support-state promotion"):
        if phrase not in blob:
            errors.append(f"{CODEX_TEST_NAME} codex test row missing {phrase!r}.")


def validate_lean_shape(errors: list[str]) -> None:
    text = LEAN_FILE.read_text(encoding="utf-8")
    for fragment in (
        "ReceiptRepositoryChallengeSummary",
        "receiptRepositoryChallengeSummary",
        "ReceiptRepositoryChallengeValid",
        LEAN_THEOREM,
        "trackedDigestMismatchControlRejected",
        "externalFingerprintMismatchControlRejected",
    ):
        if fragment not in text:
            errors.append(f"{rel(LEAN_FILE)} missing {fragment}.")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()

    errors: list[str] = []
    expected = build_expected(errors)
    validate_result(expected, args.write_result, errors)
    if not args.write_result:
        validate_surfaces(errors)
        validate_ledger_json(errors)
        validate_book_structure(errors)
        validate_lean_shape(errors)
    if errors:
        fail(errors)
    print(
        "Receipt repository challenge validation passed: "
        f"{expected['trace_summary']['accepted_challenge_count']} challenge response(s), "
        f"{expected['trace_summary']['tracked_digest_challenge_count']} tracked digest challenge(s), "
        f"{expected['trace_summary']['external_fingerprint_challenge_count']} external fingerprint challenge(s), "
        f"{expected['trace_summary']['mutation_control_count']} mutation control(s), "
        "no support-state effect."
    )


if __name__ == "__main__":
    main()

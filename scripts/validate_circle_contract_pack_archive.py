#!/usr/bin/env python3
"""Validate the archived public-safe Circle AI contract pack slice.

This validator checks that The ASI Stack carries a pinned, public-safe Circle
contract-pack archive plus a bounded acceptance-policy report. It is deliberately
not a Circle Lean replay and deliberately does not promote model-quality,
runtime, transfer, safety, ASI, or chapter-core claims.
"""

from __future__ import annotations

import copy
import hashlib
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "experiments" / "circle_contract_pack_archive" / "fixtures" / "circle_ai_contract_pack.63b0f511.json"
REPORT = (
    ROOT
    / "experiments"
    / "circle_contract_pack_archive"
    / "fixtures"
    / "circle_ai_acceptance_policy_report.63b0f511.json"
)
RESULT = ROOT / "experiments" / "circle_contract_pack_archive" / "results" / "2026-07-05-local.json"
README = ROOT / "experiments" / "circle_contract_pack_archive" / "README.md"
SUMMARY = ROOT / "docs" / "circle_contract_pack_archive.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "circle_contract_pack_archive_no_change.json"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
STATUS = ROOT / "docs" / "v1_0_candidate_status.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"
README_ROOT = ROOT / "README.md"
INDEX = ROOT / "index.qmd"
CIRCLE_CHAPTER = ROOT / "chapters" / "circle-calculus-and-proof-carrying-ai-contracts.qmd"
CIRCLE_READER = (
    ROOT
    / "editions"
    / "reader_manuscript"
    / "v1_0"
    / "chapters"
    / "circle-calculus-and-proof-carrying-ai-contracts.qmd"
)
CHANGELOG = ROOT / "appendices" / "F_changelog.qmd"

PACK_FILE_SHA256 = "b5488c93109ef120b97fdea7bd5d5605f32b2618c6cbfb9dde9a3328652551c4"
PACK_STABLE_JSON_SHA256 = "10e2dc51e9a6fe2591b2878a293dfdaa2fecf7a2ff588954495f429082724891"
REPORT_FILE_SHA256 = "f1671f5cecdee311185f7e4508b21c139d4ae4bd1fa9610a12827f4d31c7985a"
REPORT_STABLE_JSON_SHA256 = "6f49d87702e1d9e078c806778abfcdfd0efdc762d263a973b78f0b9c15c491a6"
PACK_CONTENT_FINGERPRINT = "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae"
SOURCE_COMMIT = "63b0f511"

EXPECTED_CONTRACTS = {
    "rope_position_distinguishability": ("CC-AI-CONTRACT-ROPE-001", "a0f35d3e89e9b6eac555f0392450f4f75cf7e70f30cff44ec7434f61bd85b468", 75),
    "kv_cache_ring_buffer": ("CC-AI-CONTRACT-KV-001", "bfebf150ce45d1eb124ea553bf2ba8c62008751ebec9f8600b83cc09e0526a46", 54),
    "sparse_attention_coverage": ("CC-AI-CONTRACT-SPARSE-001", "c23809cef9b821b1e4f9cabf53fcac724a0757bf3f86594e1d12710fe0cd9ec1", 141),
    "recurrence_schedule": ("CC-AI-CONTRACT-RECURRENCE-001", "571edd5dce4f7b64441806de323295218a3e2293b3b540dd4772ba34b9371515", 64),
    "strided_candidate_fanout": ("CC-AI-CONTRACT-FANOUT-001", "d4c878563747da9c9f1f55cd689f04e2a0a8e31ce9429a138341ec4e27ee3799", 4),
    "cyclic_memory_residue_winding": ("CC-AI-CONTRACT-MEMORY-001", "a25d841aff585b59519919cad25d89a3f76cd8ddb11fb1549d593f7f2f09c62a", 4),
    "multicoil_phase_feature": ("CC-AI-CONTRACT-PHASE-FEATURE-001", "4b562beab64ec863903e4267f50c90049f0d3fa612f6c1bb2f06ad07e821ffd7", 5),
    "circulant_block_cyclic_mixer": ("CC-AI-CONTRACT-MIXER-001", "b3e3e0cf420d9e8e79a28a55ef8322f9a214c8d5a957dd8b06e5e5373c684ea5", 7),
    "seed_rule_exact_regeneration": ("CC-AI-CONTRACT-SEED-RULE-001", "836594a5f1d448900797e595cb98f0e476c0b9cbd7365fe333cf7ae2622f13c5", 32),
}

FLAGSHIP_REPORT_KINDS = (
    "rope_position_distinguishability",
    "kv_cache_ring_buffer",
    "sparse_attention_coverage",
    "recurrence_schedule",
)

NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not rerun Circle Lean",
    "does not prove deployed proof-contract transport",
    "model quality",
    "context length",
    "runtime speed",
    "memory scaling",
    "deployment safety",
    "transfer",
    "safety",
    "ASI",
)

FULL_ARCHIVE_FRAGMENTS = (
    "Circle contract-pack archive",
    SOURCE_COMMIT,
    PACK_CONTENT_FINGERPRINT,
    PACK_FILE_SHA256,
    REPORT_FILE_SHA256,
    "9 archived contracts",
    "4 acceptance-policy receipts",
    "public_safe_fixture",
    "circle_contract_pack_archive_no_change.json",
) + tuple(value for row in EXPECTED_CONTRACTS.values() for value in row[:2]) + NON_CLAIMS

COMMON_SURFACE_FRAGMENTS = (
    "Circle contract-pack archive",
    SOURCE_COMMIT,
    PACK_CONTENT_FINGERPRINT,
    "9 archived contracts",
    "4 acceptance-policy receipts",
    "circle_contract_pack_archive_no_change.json",
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not rerun Circle Lean",
    "does not prove deployed proof-contract transport",
    "model quality",
    "context length",
    "runtime speed",
    "memory scaling",
    "deployment safety",
    "transfer",
    "safety",
    "ASI",
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_json_sha256(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    lowered = " ".join(text.lower().split())
    for fragment in fragments:
        normalized = " ".join(str(fragment).lower().split())
        if normalized not in lowered:
            errors.append(f"{owner} missing required fragment: {fragment}")


def validate_public_hygiene(owner: str, value: Any, errors: list[str]) -> None:
    blob = text_blob(value)
    forbidden = ("/Users/", "file://", "localhost", "127.0.0.1", "password", "secret", "api_key")
    for fragment in forbidden:
        if fragment in blob:
            errors.append(f"{owner} contains forbidden public-safety fragment {fragment!r}.")


def validate_pack(pack: Any, owner: str, errors: list[str]) -> None:
    if not isinstance(pack, dict):
        errors.append(f"{owner} must contain a JSON object.")
        return
    expected = {
        "schema_id": "circle_calculus.ai_contract_pack.v0",
        "status": "public_safe_fixture",
        "content_fingerprint_algorithm": "sha256-json-v1",
        "pack_content_fingerprint": PACK_CONTENT_FINGERPRINT,
    }
    for key, expected_value in expected.items():
        if pack.get(key) != expected_value:
            errors.append(f"{owner}: {key} must be {expected_value!r}.")
    if "do not prove model quality" not in str(pack.get("claim_boundary", "")):
        errors.append(f"{owner}: claim_boundary must preserve the model-quality non-claim.")
    validate_public_hygiene(owner, pack, errors)

    contracts = pack.get("contracts")
    if not isinstance(contracts, list) or len(contracts) != len(EXPECTED_CONTRACTS):
        errors.append(f"{owner}: expected {len(EXPECTED_CONTRACTS)} contracts.")
        return
    by_kind = {item.get("kind"): item for item in contracts if isinstance(item, dict)}
    if set(by_kind) != set(EXPECTED_CONTRACTS):
        errors.append(f"{owner}: contract kinds do not match the expected archive set.")
    index = pack.get("contract_fingerprint_index")
    if not isinstance(index, dict):
        errors.append(f"{owner}: missing contract_fingerprint_index.")
        return
    for kind, (contract_id, fingerprint, theorem_count) in EXPECTED_CONTRACTS.items():
        item = by_kind.get(kind)
        indexed = index.get(kind)
        if not isinstance(item, dict):
            errors.append(f"{owner}: missing contract kind {kind}.")
            continue
        if item.get("id") != contract_id:
            errors.append(f"{owner}: {kind}.id must be {contract_id}.")
        if item.get("content_fingerprint") != fingerprint:
            errors.append(f"{owner}: {kind}.content_fingerprint must be {fingerprint}.")
        if len(item.get("theorem_ids", [])) != theorem_count:
            errors.append(f"{owner}: {kind} theorem_ids length must be {theorem_count}.")
        if not isinstance(indexed, dict):
            errors.append(f"{owner}: missing fingerprint index for {kind}.")
        else:
            if indexed.get("id") != contract_id or indexed.get("content_fingerprint") != fingerprint:
                errors.append(f"{owner}: fingerprint index mismatch for {kind}.")
        if "not prove model quality" not in text_blob(item.get("not_claimed", "")):
            errors.append(f"{owner}: {kind} must preserve model-quality non-claim text.")


def validate_report(report: Any, pack: dict[str, Any], owner: str, errors: list[str]) -> None:
    if not isinstance(report, dict):
        errors.append(f"{owner} must contain a JSON object.")
        return
    expected = {
        "acceptance_policy_report_schema": "circle_calculus.ai_contract_acceptance_policy_report.v0",
        "policy_id": "circle_ai_flagship_contracts_acceptance_v0",
        "policy_schema": "circle_calculus.ai_contract_acceptance_policy.v0",
        "accepted": True,
        "contract_count": 4,
        "receipt_count": 4,
        "pack_content_fingerprint": PACK_CONTENT_FINGERPRINT,
        "expected_pack_fingerprint": PACK_CONTENT_FINGERPRINT,
    }
    for key, expected_value in expected.items():
        if report.get(key) != expected_value:
            errors.append(f"{owner}: {key} must be {expected_value!r}.")
    validate_public_hygiene(owner, report, errors)
    if "not a claim of model quality" not in str(report.get("not_claimed", "")):
        errors.append(f"{owner}: not_claimed must preserve model-quality boundary.")

    receipts = report.get("receipts")
    if not isinstance(receipts, list) or len(receipts) != len(FLAGSHIP_REPORT_KINDS):
        errors.append(f"{owner}: expected {len(FLAGSHIP_REPORT_KINDS)} receipt records.")
        return
    by_kind = {item.get("kind"): item for item in receipts if isinstance(item, dict)}
    if set(by_kind) != set(FLAGSHIP_REPORT_KINDS):
        errors.append(f"{owner}: receipt kinds do not match the flagship policy set.")
    index = pack.get("contract_fingerprint_index", {}) if isinstance(pack, dict) else {}
    for kind in FLAGSHIP_REPORT_KINDS:
        receipt = by_kind.get(kind)
        if not isinstance(receipt, dict):
            errors.append(f"{owner}: missing receipt for {kind}.")
            continue
        contract_id, fingerprint, _ = EXPECTED_CONTRACTS[kind]
        if receipt.get("accepted") is not True:
            errors.append(f"{owner}: {kind} must remain accepted.")
        if receipt.get("contract_id") != contract_id:
            errors.append(f"{owner}: {kind}.contract_id must be {contract_id}.")
        if receipt.get("contract_content_fingerprint") != fingerprint:
            errors.append(f"{owner}: {kind}.contract_content_fingerprint must be {fingerprint}.")
        indexed = index.get(kind) if isinstance(index, dict) else None
        if not isinstance(indexed, dict) or indexed.get("content_fingerprint") != fingerprint:
            errors.append(f"{owner}: {kind} report fingerprint must match archived pack index.")
        if len(receipt.get("planner_recommendations", [])) != 2:
            errors.append(f"{owner}: {kind} must expose two policy-pinned recommendations.")
        if "do not prove model quality" not in text_blob(receipt.get("not_claimed", "")):
            errors.append(f"{owner}: {kind} receipt must preserve model-quality non-claim.")


def set_path(value: dict[str, Any], path: tuple[str | int, ...], new_value: Any) -> None:
    cursor: Any = value
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = new_value


def validate_negative_controls(pack: dict[str, Any], report: dict[str, Any], errors: list[str]) -> None:
    controls: list[tuple[str, Any, tuple[str | int, ...], Any, str]] = [
        (
            "pack_fingerprint_mismatch",
            copy.deepcopy(pack),
            ("pack_content_fingerprint",),
            "bad",
            "pack_content_fingerprint",
        ),
        (
            "contract_fingerprint_mismatch",
            copy.deepcopy(pack),
            ("contract_fingerprint_index", "rope_position_distinguishability", "content_fingerprint"),
            "bad",
            "fingerprint index mismatch",
        ),
        (
            "unsafe_local_path",
            copy.deepcopy(pack),
            ("source_docs", 0),
            "/Users/private/leak",
            "forbidden public-safety fragment",
        ),
        (
            "acceptance_report_rejected",
            copy.deepcopy(report),
            ("accepted",),
            False,
            "accepted must be True",
        ),
        (
            "acceptance_report_pack_mismatch",
            copy.deepcopy(report),
            ("pack_content_fingerprint",),
            "bad",
            "pack_content_fingerprint",
        ),
    ]

    for case_id, mutated, path, value, expected_fragment in controls:
        set_path(mutated, path, value)
        observed: list[str] = []
        if "report" in case_id:
            validate_report(mutated, pack, case_id, observed)
        else:
            validate_pack(mutated, case_id, observed)
        if not observed:
            errors.append(f"{case_id}: expected invalid mutation passed.")
            continue
        if expected_fragment not in "\n".join(observed):
            errors.append(f"{case_id}: expected {expected_fragment!r}; got {observed}.")


def validate_result(errors: list[str]) -> None:
    result = load_json(RESULT)
    if not isinstance(result, dict):
        errors.append(f"{rel(RESULT)} must contain a JSON object.")
        return
    expected = {
        "result_id": "2026-07-05-circle-contract-pack-archive",
        "slice_id": "circle_contract_pack_archive",
        "source_project": "Circle Calculus",
        "source_commit": SOURCE_COMMIT,
        "archive_status": "public_safe_archived_pack",
        "pack_file_sha256": PACK_FILE_SHA256,
        "pack_stable_json_sha256": PACK_STABLE_JSON_SHA256,
        "report_file_sha256": REPORT_FILE_SHA256,
        "report_stable_json_sha256": REPORT_STABLE_JSON_SHA256,
        "pack_content_fingerprint": PACK_CONTENT_FINGERPRINT,
        "contract_count": 9,
        "acceptance_policy_contract_count": 4,
        "accepted_receipt_count": 4,
        "expected_invalid_control_count": 5,
        "support_state_effect": "blocks_promotion",
        "verification_command": "python3 scripts/validate_circle_contract_pack_archive.py",
        "verification_result": "pass",
        "transition_id": "v1_x_measured.circle_contract_pack_archive.no_change",
        "claim_id": "circle-calculus.contract_pack_archive",
    }
    for key, expected_value in expected.items():
        if result.get(key) != expected_value:
            errors.append(f"{rel(RESULT)}: {key} must be {expected_value!r}.")
    require_fragments(rel(RESULT), text_blob(result), FULL_ARCHIVE_FRAGMENTS, errors)


def validate_transition(errors: list[str]) -> None:
    transition = load_json(TRANSITION)
    if not isinstance(transition, dict):
        errors.append(f"{rel(TRANSITION)} must contain a JSON object.")
        return
    expected = {
        "transition_id": "v1_x_measured.circle_contract_pack_archive.no_change",
        "claim_id": "circle-calculus.contract_pack_archive",
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "review_status": "accepted",
        "support_state_effect": "blocks_promotion",
        "verification_result": "pass",
    }
    for key, expected_value in expected.items():
        if transition.get(key) != expected_value:
            errors.append(f"{rel(TRANSITION)}: {key} must be {expected_value!r}.")
    require_fragments(rel(TRANSITION), text_blob(transition), COMMON_SURFACE_FRAGMENTS, errors)
    if "does not create an upward support-state transition" not in text_blob(transition):
        errors.append(f"{rel(TRANSITION)} must preserve upward support-state boundary text.")


def validate_surfaces(errors: list[str]) -> None:
    for path in (
        README,
        SUMMARY,
        LEDGER,
        ROADMAP,
        STATUS,
        APPENDIX_E,
        README_ROOT,
        INDEX,
        CIRCLE_CHAPTER,
        CIRCLE_READER,
        CHANGELOG,
    ):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
            continue
        fragments = FULL_ARCHIVE_FRAGMENTS if path in (README, SUMMARY) else COMMON_SURFACE_FRAGMENTS
        require_fragments(rel(path), path.read_text(encoding="utf-8"), fragments, errors)


def fail(errors: list[str]) -> None:
    print("Circle contract-pack archive validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def main() -> None:
    errors: list[str] = []
    for path in (PACK, REPORT, RESULT, README, SUMMARY, TRANSITION):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        fail(errors)

    pack = load_json(PACK)
    report = load_json(REPORT)
    if file_sha256(PACK) != PACK_FILE_SHA256:
        errors.append(f"{rel(PACK)} file SHA-256 drifted.")
    if stable_json_sha256(pack) != PACK_STABLE_JSON_SHA256:
        errors.append(f"{rel(PACK)} stable JSON SHA-256 drifted.")
    if file_sha256(REPORT) != REPORT_FILE_SHA256:
        errors.append(f"{rel(REPORT)} file SHA-256 drifted.")
    if stable_json_sha256(report) != REPORT_STABLE_JSON_SHA256:
        errors.append(f"{rel(REPORT)} stable JSON SHA-256 drifted.")

    validate_pack(pack, rel(PACK), errors)
    validate_report(report, pack, rel(REPORT), errors)
    if isinstance(pack, dict) and isinstance(report, dict):
        validate_negative_controls(pack, report, errors)
    validate_result(errors)
    validate_transition(errors)
    validate_surfaces(errors)

    if errors:
        fail(errors)

    print(
        "Circle contract-pack archive validation passed: "
        "9 archived contracts, 4 accepted policy receipts, 5 expected-invalid controls."
    )


if __name__ == "__main__":
    main()

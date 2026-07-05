#!/usr/bin/env python3
"""Validate the public-safe Circle KV-cache receipt slice.

This is a structural evidence-surface check. It keeps the Coil chapter concrete
about Circle KV-cache ring-buffer receipt facts without allowing those facts to
turn into deployed serving, paging, throughput, retrieval-quality, or support-
state claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_kv_cache_receipt_slice" / "results" / "2026-07-05-local.json"
README = ROOT / "experiments" / "circle_kv_cache_receipt_slice" / "README.md"
SUMMARY = ROOT / "docs" / "circle_kv_cache_receipt_slice.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "circle_kv_cache_receipt_no_change.json"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "coil-attention-cyclic-memory-and-recurrence-contracts.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"

EXPECTED = {
    "result_id": "2026-07-05-local-circle-kv-cache-receipt-slice",
    "slice_id": "circle_kv_cache_receipt_slice",
    "git_commit": "63b0f511",
    "contract_id": "CC-AI-CONTRACT-KV-001",
    "kind": "kv_cache_ring_buffer",
    "receipt_schema": "circle_calculus.ai_contract_acceptance_receipt.v0",
    "schema_id": "circle_calculus.ai_contract_pack.v0",
    "pack_content_fingerprint": "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint": "bfebf150ce45d1eb124ea553bf2ba8c62008751ebec9f8600b83cc09e0526a46",
    "pytest_summary": "5 passed in 1.27s",
    "transition_id": "v1_x_measured.circle_kv_cache_receipt.no_change",
    "claim_id": "circle-calculus.kv_cache_ring_buffer_receipt_slice",
}

THEOREMS = ("AIM-T0103", "AIM-T0104", "AIM-T0149")
RECOMMENDATIONS = (
    "KV-DROP-STALE-REQUEST-TOKEN",
    "KV-USE-SINK-ROLLING-WINDOW-REQUEST",
)
OUTPUT_HASHES = {
    "0651d42d9b3c5d8820d747018faff75e83ecd97bc973ac384ae10d1e6ada40f1": 14268,
    "169999b3c44aa082acf0cb8410ce3d921d16d20c486397a79197ae36c761ef4f": 28336,
    "18dec02ed8d5f967f985ff0fc883cf90e0ee9b4d69d714fc4a8de84b07c69547": 3035,
    "d75246f822d76c52d56521b7911e374f6f559526417b4857bea39da7cf89c100": 8266,
    "87fa9996a06e4107cc2e24a8aaa2f3681b65f05c9783972fe74cd0d508fab8fb": 98,
}
NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove deployed KV-cache behavior",
    "serving throughput",
    "memory savings",
    "paging correctness",
    "retrieval quality",
    "model quality",
    "context length",
    "deployment safety",
    "transfer",
    "ASI",
)
SURFACE_FRAGMENTS = (
    EXPECTED["git_commit"],
    EXPECTED["contract_id"],
    EXPECTED["kind"],
    EXPECTED["contract_content_fingerprint"],
    "stale_probe_first_stale_token=12",
    "sink_tokens_retained_by_policy=true",
    "sink_window_exact_policy=true",
    "sink_window_tokens_distinct=true",
    "sink_prefix_disjoint_from_live_window=true",
    "sink_tokens_outside_ordinary_rolling_window=true",
    "theorem_count=54",
    EXPECTED["pytest_summary"],
    "circle_kv_cache_receipt_no_change.json",
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS
READER_FRAGMENTS = (
    "KV-cache receipt",
    "ring-buffer",
    "stale-token recommendation",
    "sink-window",
    "KV-cache contract",
    "Circle commit",
    "three theorem IDs",
    "receipt fingerprint",
    "stale-token diagnostic",
    EXPECTED["pytest_summary"],
) + NON_CLAIMS


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def text_blob(value: Any) -> str:
    if isinstance(value, dict):
        return "\n".join(f"{key}: {text_blob(child)}" for key, child in value.items())
    if isinstance(value, list):
        return "\n".join(text_blob(item) for item in value)
    return str(value)


def require_fragments(owner: str, text: str, fragments: tuple[str, ...], errors: list[str]) -> None:
    lower = " ".join(text.lower().split())
    for fragment in fragments:
        normalized = " ".join(fragment.lower().split())
        if normalized not in lower:
            errors.append(f"{owner} missing required fragment: {fragment}")


def chapter_record(structure: dict[str, Any], chapter_id: str) -> dict[str, Any]:
    for part in structure.get("parts", []):
        if not isinstance(part, dict):
            continue
        for chapter in part.get("chapters", []):
            if isinstance(chapter, dict) and chapter.get("id") == chapter_id:
                return chapter
    return {}


def validate_result(errors: list[str]) -> dict[str, Any]:
    if not RESULT.exists():
        errors.append(f"Missing {rel(RESULT)}.")
        return {}
    result = load_json(RESULT)
    if not isinstance(result, dict):
        errors.append(f"{rel(RESULT)} must contain a JSON object.")
        return {}

    if "/Users/" in text_blob(result):
        errors.append(f"{rel(RESULT)} must not contain absolute local user paths.")
    for key in ("result_id", "slice_id"):
        if result.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} {key} must be {EXPECTED[key]!r}.")

    project = result.get("external_project", {})
    if not isinstance(project, dict) or project.get("git_commit") != EXPECTED["git_commit"]:
        errors.append(f"{rel(RESULT)} must record Circle commit {EXPECTED['git_commit']}.")
    if project.get("worktree_state") != "clean_before_commands":
        errors.append(f"{rel(RESULT)} must record the clean external worktree boundary.")

    receipt = result.get("accepted_receipt", {})
    if not isinstance(receipt, dict):
        errors.append(f"{rel(RESULT)} accepted_receipt must be an object.")
        return result
    for key in ("contract_id", "kind", "receipt_schema", "schema_id", "pack_content_fingerprint", "contract_content_fingerprint"):
        if receipt.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} accepted_receipt.{key} must be {EXPECTED[key]!r}.")
    if receipt.get("accepted") is not True:
        errors.append(f"{rel(RESULT)} accepted_receipt.accepted must be true.")
    if tuple(receipt.get("required_theorem_ids", [])) != THEOREMS:
        errors.append(f"{rel(RESULT)} theorem IDs must remain {THEOREMS}.")
    if tuple(receipt.get("required_recommendation_ids", [])) != RECOMMENDATIONS:
        errors.append(f"{rel(RESULT)} recommendation IDs must remain {RECOMMENDATIONS}.")
    if receipt.get("theorem_count") != 54:
        errors.append(f"{rel(RESULT)} theorem_count must remain 54.")

    fields = receipt.get("evidence_fields", {})
    expected_fields = {
        "cache_size": 16,
        "current": 31,
        "token": 20,
        "slot": 4,
        "current_slot": 15,
        "lag": 11,
        "retained": True,
        "next_overwrite_token": 36,
        "next_overwrite_after_current": True,
        "stale_by_next_overwrite_boundary": False,
        "no_same_slot_overwrite_before_current": True,
        "trace_fresh_iff_next_overwrite_boundary": True,
        "batch_tokens": [20, 24, 29, 31],
        "batch_slots": [4, 8, 13, 15],
        "all_non_future": True,
        "all_retained": True,
        "tokens_distinct": True,
        "slots_distinct": True,
        "ordered_live_window_subrequest": True,
        "duplicate_free_live_window_subrequest": True,
        "stale_requested_count": 0,
        "live_window_start": 16,
        "live_window_length": 16,
        "sink_tokens": [0, 1, 2, 3],
        "sink_tokens_retained_by_policy": True,
        "sink_window_exact_policy": True,
        "sink_window_tokens_distinct": True,
        "sink_prefix_disjoint_from_live_window": True,
        "sink_tokens_outside_ordinary_rolling_window": True,
        "request_token_count": 20,
        "request_token_count_bound": 20,
        "stale_probe_first_stale_token": 12,
    }
    if fields != expected_fields:
        errors.append(f"{rel(RESULT)} evidence_fields drifted from the recorded Circle KV fixture facts.")

    commands = result.get("commands", [])
    if not isinstance(commands, list) or len(commands) != 5:
        errors.append(f"{rel(RESULT)} must record exactly five successful commands.")
    else:
        seen_hashes: dict[str, int] = {}
        command_text = text_blob(commands)
        for command in commands:
            if not isinstance(command, dict):
                errors.append(f"{rel(RESULT)} commands must be objects.")
                continue
            if command.get("verification_result") != "pass":
                errors.append(f"{rel(RESULT)} command {command.get('command')} did not record pass.")
            sha = command.get("output_sha256")
            size = command.get("output_bytes")
            if isinstance(sha, str) and isinstance(size, int):
                seen_hashes[sha] = size
        for sha, size in OUTPUT_HASHES.items():
            if seen_hashes.get(sha) != size:
                errors.append(f"{rel(RESULT)} missing output hash {sha} with byte size {size}.")
        for fragment in (
            "PYTHONPATH=. python3 scripts/kv_cache_certify.py --cache-size 16 --current 31 --token 20",
            "ready=True fields=6 missing=0 theorems=54",
            "accepted true",
            EXPECTED["pytest_summary"],
        ):
            if fragment not in command_text:
                errors.append(f"{rel(RESULT)} command summaries missing {fragment!r}.")

    if result.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)} support_state_effect must remain none.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), NON_CLAIMS, errors)
    if "required --cache-size, --current, and --token" not in text_blob(result.get("discarded_attempts", [])):
        errors.append(f"{rel(RESULT)} discarded_attempts missing required-argument correction boundary.")
    return result


def validate_transition(errors: list[str]) -> None:
    if not TRANSITION.exists():
        errors.append(f"Missing {rel(TRANSITION)}.")
        return
    transition = load_json(TRANSITION)
    if not isinstance(transition, dict):
        errors.append(f"{rel(TRANSITION)} must contain a JSON object.")
        return
    expected_pairs = {
        "transition_id": EXPECTED["transition_id"],
        "claim_id": EXPECTED["claim_id"],
        "old_support_state": "argument",
        "new_support_state": "argument",
        "transition_effect": "no_change",
        "transition_validity_state": "review_accepted",
        "review_status": "accepted",
        "verification_result": "pass",
        "support_state_effect": "blocks_promotion",
    }
    for key, expected in expected_pairs.items():
        if transition.get(key) != expected:
            errors.append(f"{rel(TRANSITION)} {key} must be {expected!r}.")
    require_fragments(
        rel(TRANSITION),
        text_blob(transition),
        (
            EXPECTED["contract_id"],
            EXPECTED["contract_content_fingerprint"],
            "does not create an upward support-state transition",
            "chapter core",
            "above argument",
            "deployed KV-cache behavior",
            "serving throughput",
            "paging correctness",
            "retrieval quality",
        ),
        errors,
    )


def validate_public_surfaces(errors: list[str]) -> None:
    for path in (README, SUMMARY, TRANSITION, LEDGER, STRUCTURE, OUTLINE, CHAPTER, READER, ROADMAP, APPENDIX_E):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
    if errors:
        return

    for path in (SUMMARY, CHAPTER, OUTLINE, ROADMAP, APPENDIX_E, LEDGER):
        text = path.read_text(encoding="utf-8")
        require_fragments(rel(path), text, SURFACE_FRAGMENTS, errors)
    require_fragments(rel(READER), READER.read_text(encoding="utf-8"), READER_FRAGMENTS, errors)

    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        errors.append(f"{rel(STRUCTURE)} must contain an object.")
        return
    chapter = chapter_record(structure, "coil-attention-cyclic-memory-and-recurrence-contracts")
    if chapter.get("evidence_level") != "argument":
        errors.append("Coil chapter evidence_level must remain argument.")
    tests = text_blob(chapter.get("codex_tests", []))
    if "Circle KV-cache receipt-slice validation" not in tests:
        errors.append("Coil chapter manifest is missing the Circle KV-cache receipt-slice test row.")
    if "no deployed KV-cache behavior, serving throughput, memory-savings, paging correctness, retrieval-quality, long-context, model-quality, deployment, transfer, ASI, or support-state-transition claim" not in tests:
        errors.append("Coil chapter manifest test row must preserve KV non-claim boundary.")


def fail(errors: list[str]) -> None:
    print("Circle KV-cache receipt-slice validation failed:")
    for error in errors:
        print(f" - {error}")
    sys.exit(1)


def main() -> None:
    errors: list[str] = []
    validate_result(errors)
    validate_transition(errors)
    validate_public_surfaces(errors)
    if errors:
        fail(errors)
    print("Circle KV-cache receipt-slice validation passed.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the public-safe Circle cyclic-mixer receipt slice.

This is a structural evidence-surface check. It keeps the CoilRA chapter
concrete about Circle circulant parity and block-cyclic parameter-accounting
facts without allowing those facts to turn into model-quality, runtime,
hardware-efficiency, deployment, or support-state claims.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RESULT = ROOT / "experiments" / "circle_cyclic_mixer_receipt_slice" / "results" / "2026-07-05-local.json"
README = ROOT / "experiments" / "circle_cyclic_mixer_receipt_slice" / "README.md"
SUMMARY = ROOT / "docs" / "circle_cyclic_mixer_receipt_slice.md"
TRANSITION = ROOT / "evidence_transitions" / "v1_x_measured" / "circle_cyclic_mixer_receipt_no_change.json"
LEDGER = ROOT / "docs" / "non_core_evidence_ledger.md"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
CHAPTER = ROOT / "chapters" / "coilra-multicoil-rope-and-cyclic-mixers.qmd"
READER = ROOT / "editions" / "reader_manuscript" / "v1_0" / "chapters" / "coilra-multicoil-rope-and-cyclic-mixers.qmd"
ROADMAP = ROOT / "docs" / "v1_x_beyond_sota_roadmap.md"
APPENDIX_E = ROOT / "appendices" / "E_codex_test_specs.qmd"

EXPECTED = {
    "result_id": "2026-07-05-local-circle-cyclic-mixer-receipt-slice",
    "slice_id": "circle_cyclic_mixer_receipt_slice",
    "git_commit": "63b0f511",
    "contract_id": "CC-AI-CONTRACT-MIXER-001",
    "kind": "circulant_block_cyclic_mixer",
    "receipt_schema": "circle_calculus.ai_contract_acceptance_receipt.v0",
    "schema_id": "circle_calculus.ai_contract_pack.v0",
    "pack_content_fingerprint": "df673f8a661fc89a26372685986c92f2221aaa617d6738fce5c2a76bd5d0eeae",
    "contract_content_fingerprint": "b3e3e0cf420d9e8e79a28a55ef8322f9a214c8d5a957dd8b06e5e5373c684ea5",
    "receipt_content_fingerprint": "46ccd26c495445039fe58ec5207c56a621e8dcfed18b5b286aed4cb4c802639d",
    "pytest_summary": "3 passed in 2.49s",
    "contract_ready_pytest_summary": "1 passed in 1.47s",
    "transition_id": "v1_x_measured.circle_cyclic_mixer_receipt.no_change",
    "claim_id": "circle-calculus.cyclic_mixer_receipt_slice",
}

THEOREMS = ("AIT-T0006", "AIT-T0007", "AIT-T0008", "AIT-T0009", "AIRA-T0001", "AIRA-T0002", "AIRA-T0004")
RECOMMENDATIONS = (
    "MIXER-AUDIT-CIRCULANT-DENSE-PARITY",
    "MIXER-AUDIT-BLOCK-CYCLIC-PARAMETER-BUDGET",
)
OUTPUT_HASHES = {
    "32802064ce7f2207f2e13b1b28acb75c6f80c900c334d092f5113f0173fc5ae4": 7224,
    "8537b2fea1fea31ef3d8300c14232e4b11f24aa4c383488b2c3414c1b6bd0956": 15556,
    "050b37495c4f4110c07416bec95599ab39e200caa6e8ddaa05603bb6df4bbbbb": 1950,
    "11315c4e507c3563e99811cbd0f4bc65823113d9d7c07a7cf2f2090d81e1b61e": 1440,
    "541b0292a52421d8f7f1f102d89ef653da212dd58aaaa89746ab4c856b1f8d14": 98,
    "6a188187cc4acf92013e1fe24b04baf7dba1edd907ad7d4feecc4ff2465c741f": 98,
}
NON_CLAIMS = (
    "does not promote any chapter core claim",
    "does not create a support-state transition",
    "does not prove cyclic-mixer model quality",
    "does not prove runtime speed",
    "memory scaling",
    "hardware efficiency",
    "training stability",
    "deployment readiness",
    "transfer",
    "benchmark performance",
    "ASI",
)
SURFACE_FRAGMENTS = (
    EXPECTED["git_commit"],
    EXPECTED["contract_id"],
    EXPECTED["kind"],
    EXPECTED["contract_content_fingerprint"],
    "max_abs_dense_delta=0",
    "dense_parameters=64",
    "circulant_parameters=8",
    "circulant_parameter_ratio=0.125",
    "dense_adapter_parameters=2048",
    "lora_parameters=576",
    "block_cyclic_parameters=128",
    "block_to_dense_ratio=0.0625",
    "theorem_count=7",
    EXPECTED["pytest_summary"],
    EXPECTED["contract_ready_pytest_summary"],
    "circle_cyclic_mixer_receipt_no_change.json",
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS
READER_FRAGMENTS = (
    "cyclic-mixer receipt",
    "dense-reference parity",
    "block-cyclic parameter accounting",
    "max_abs_dense_delta=0",
    "block_to_dense_ratio=0.0625",
    EXPECTED["contract_id"],
    EXPECTED["contract_content_fingerprint"],
    EXPECTED["pytest_summary"],
    EXPECTED["contract_ready_pytest_summary"],
) + THEOREMS + RECOMMENDATIONS + NON_CLAIMS


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

    fixture = result.get("mixer_fixture", {})
    expected_fixture = {
        "period": 8,
        "input_values": [-2, 2, 1, 2, -2, 3, 3, -2],
        "kernel_values": [2, -1, 1, 0, -2, 0, 0, 0],
        "circulant_output": [5, -2, -8, 9, -1, 6, -1, -8],
        "dense_output": [5, -2, -8, 9, -1, 6, -1, -8],
        "max_abs_dense_delta": 0,
        "dense_parameters": 64,
        "circulant_parameters": 8,
        "circulant_parameter_ratio": 0.125,
        "channel_count": 128,
        "block_size": 8,
        "block_loads": [16, 16, 16, 16, 16, 16, 16, 16],
        "dense_adapter_parameters": 2048,
        "lora_parameters": 576,
        "block_cyclic_parameters": 128,
        "block_to_dense_ratio": 0.0625,
        "ordinary_baselines": ["dense_mixer", "low_rank_mixer", "lora_adapter", "no_mixer"],
        "contract_ready_theorem_count": 7,
        "circle_ai_receipt_theorem_count": 7,
    }
    if fixture != expected_fixture:
        errors.append(f"{rel(RESULT)} mixer_fixture drifted from the recorded Circle cyclic-mixer facts.")

    receipt = result.get("accepted_receipt", {})
    if not isinstance(receipt, dict):
        errors.append(f"{rel(RESULT)} accepted_receipt must be an object.")
        return result
    for key in ("contract_id", "kind", "receipt_schema", "schema_id", "pack_content_fingerprint", "contract_content_fingerprint", "receipt_content_fingerprint"):
        if receipt.get(key) != EXPECTED[key]:
            errors.append(f"{rel(RESULT)} accepted_receipt.{key} must be {EXPECTED[key]!r}.")
    if receipt.get("accepted") is not True or receipt.get("request_passed") is not True:
        errors.append(f"{rel(RESULT)} accepted_receipt must preserve accepted=true and request_passed=true.")
    if tuple(receipt.get("required_theorem_ids", [])) != THEOREMS:
        errors.append(f"{rel(RESULT)} theorem IDs must remain {THEOREMS}.")
    if tuple(receipt.get("required_recommendation_ids", [])) != RECOMMENDATIONS:
        errors.append(f"{rel(RESULT)} recommendation IDs must remain {RECOMMENDATIONS}.")
    if receipt.get("theorem_count") != 7:
        errors.append(f"{rel(RESULT)} theorem_count must remain 7.")

    expected_fields = {"block_to_dense_ratio": 0.0625, "max_abs_dense_delta": 0}
    if receipt.get("evidence_fields") != expected_fields:
        errors.append(f"{rel(RESULT)} evidence_fields drifted from the recorded cyclic-mixer receipt facts.")

    recommendations = receipt.get("planner_recommendations", [])
    if not isinstance(recommendations, list) or len(recommendations) != 2:
        errors.append(f"{rel(RESULT)} planner_recommendations must record exactly two recommendations.")
    else:
        ids = [rec.get("id") for rec in recommendations if isinstance(rec, dict)]
        if tuple(ids) != RECOMMENDATIONS:
            errors.append(f"{rel(RESULT)} planner_recommendations must remain {RECOMMENDATIONS}.")
        require_fragments(
            rel(RESULT),
            text_blob(recommendations),
            (
                "not a speed, memory, hardware-efficiency, training-stability, or model-quality proof",
                "not a LoRA replacement theorem, memory-scaling proof, hardware-efficiency proof, or model-quality claim",
            ),
            errors,
        )

    boundary = result.get("circle_ai_certifier_boundary", {})
    if not isinstance(boundary, dict) or boundary.get("request_passed") is not True:
        errors.append(f"{rel(RESULT)} must preserve request_passed=true for the structural/accounting boundary.")
    require_fragments(rel(RESULT), text_blob(boundary), ("unsupported_fields", "accuracy improvement over dense layers", "not model-quality"), errors)

    commands = result.get("commands", [])
    if not isinstance(commands, list) or len(commands) != 6:
        errors.append(f"{rel(RESULT)} must record exactly six successful commands.")
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
            "PYTHONPATH=. python3 scripts/circulant_block_cyclic_mixer_certify.py --format json",
            "ready=True fields=9 missing=0 theorems=7",
            "strict cyclic-mixer acceptance receipt accepted",
            EXPECTED["pytest_summary"],
            EXPECTED["contract_ready_pytest_summary"],
        ):
            if fragment not in command_text:
                errors.append(f"{rel(RESULT)} command summaries missing {fragment!r}.")

    if result.get("support_state_effect") != "none":
        errors.append(f"{rel(RESULT)} support_state_effect must remain none.")
    require_fragments(rel(RESULT), text_blob(result.get("non_claims", [])), NON_CLAIMS, errors)
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
    for path in (str(SUMMARY.relative_to(ROOT)), str(RESULT.relative_to(ROOT)), "scripts/validate_circle_cyclic_mixer_receipt_slice.py"):
        if path not in text_blob(transition):
            errors.append(f"{rel(TRANSITION)} missing artifact ref {path!r}.")
    require_fragments(rel(TRANSITION), text_blob(transition), NON_CLAIMS, errors)
    require_fragments(
        rel(TRANSITION),
        text_blob(transition),
        (
            "max_abs_dense_delta=0",
            "block_to_dense_ratio=0.0625",
            "ordinary dense, LoRA, RoPE, learned, recurrent, or state-space baselines",
            "does not create an upward support-state transition",
            "does not promote the CoilRA chapter core claim",
        ),
        errors,
    )


def validate_surfaces(errors: list[str]) -> None:
    for path in (README, SUMMARY, LEDGER, STRUCTURE, OUTLINE, CHAPTER, READER, ROADMAP, APPENDIX_E):
        if not path.exists():
            errors.append(f"Missing {rel(path)}.")
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        fragments = READER_FRAGMENTS if path == READER else SURFACE_FRAGMENTS
        require_fragments(rel(path), text, fragments, errors)

    structure = load_json(STRUCTURE)
    if not isinstance(structure, dict):
        errors.append(f"{rel(STRUCTURE)} must contain an object.")
        return
    chapter = chapter_record(structure, "coilra-multicoil-rope-and-cyclic-mixers")
    if not chapter:
        errors.append(f"{rel(STRUCTURE)} missing CoilRA chapter record.")
        return
    if chapter.get("evidence_level") != "argument":
        errors.append("CoilRA chapter evidence_level must remain argument.")
    tests = chapter.get("codex_tests", [])
    if not isinstance(tests, list) or not any(
        isinstance(test, dict) and test.get("name") == "Circle cyclic-mixer receipt-slice validation"
        for test in tests
    ):
        errors.append(f"{rel(STRUCTURE)} missing Circle cyclic-mixer receipt-slice Codex test.")
    open_gaps = text_blob(chapter.get("open_evidence_gaps", []))
    require_fragments(
        f"{rel(STRUCTURE)} open_evidence_gaps",
        open_gaps,
        (
            "max_abs_dense_delta=0",
            "block_to_dense_ratio=0.0625",
            "no cyclic mixer benchmark",
            "no model-quality",
            "no support-state transition",
        ),
        errors,
    )


def main() -> None:
    errors: list[str] = []
    validate_result(errors)
    validate_transition(errors)
    validate_surfaces(errors)

    if errors:
        print("Circle cyclic-mixer receipt slice validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Circle cyclic-mixer receipt slice validation passed: "
        "CC-AI-CONTRACT-MIXER-001 max_abs_dense_delta=0, "
        "block_to_dense_ratio=0.0625, no support-state promotion."
    )


if __name__ == "__main__":
    main()

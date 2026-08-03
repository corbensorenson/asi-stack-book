#!/usr/bin/env python3
"""Validate the public-safe Circle cyclic-mixer receipt slice.

This is a structural evidence-surface check. It keeps the CoilRA chapter
concrete about Circle circulant parity and block-cyclic parameter-accounting
facts without allowing those facts to turn into model-quality, runtime,
hardware-efficiency, deployment, or support-state claims.
"""

from __future__ import annotations

import copy
import json
import re
import subprocess
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
LEAN_ROOT = ROOT / "lean"
LEAN_MODULE = LEAN_ROOT / "AsiStackProofs" / "CyclicMixers.lean"

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

LIFECYCLE_THEOREMS = {
    "cyclic_candidate_rejected_event_is_noninterfering",
    "cyclic_candidate_step_preserves_custody",
    "cyclic_candidate_custody_transitive",
    "run_cyclic_candidate_preserves_custody",
    "cyclic_candidate_step_preserves_invariant",
    "run_cyclic_candidate_preserves_invariant",
    "run_cyclic_candidate_append",
    "reference_cyclic_candidate_reaches_canary_eligibility",
    "reference_cyclic_candidate_preserves_zero_authority",
    "reference_regression_retires_through_fallback",
    "missing_baseline_matrix_rejects_without_state_change",
    "incomplete_tradeoff_partition_rejects_without_state_change",
    "hardware_mismatch_without_refusal_rejects_without_state_change",
    "canary_admission_without_fallback_rejects_without_state_change",
    "retired_candidate_is_absorbing_one_step",
    "retired_candidate_is_absorbing_for_any_suffix",
    "structural_summary_collides_across_canary_eligibility",
    "no_structural_summary_classifier_recovers_canary_eligibility",
}

IDENTITY_AND_AUTHORITY_FIELDS = (
    "candidate_digest",
    "expected_candidate_digest",
    "workload_digest",
    "expected_workload_digest",
    "baseline_digest",
    "expected_baseline_digest",
    "tradeoff_digest",
    "expected_tradeoff_digest",
    "hardware_digest",
    "expected_hardware_digest",
    "authority_ceiling",
    "support_assignments",
    "external_effects",
)

REFERENCE_EVENTS = (
    ("certify", 101, True),
    ("bind", 101, 202, 303, True),
    ("tradeoffs", 101, 404, True, True, True, True),
    ("hardware", 101, 505, True, False),
    ("admit", 101, 303, 404, 505, True),
)

LIFECYCLE_EVENTS = (
    *REFERENCE_EVENTS,
    ("certify", 999, True),
    ("certify", 101, False),
    ("bind", 101, 999, 303, True),
    ("bind", 101, 202, 303, False),
    ("tradeoffs", 101, 404, False, True, True, True),
    ("tradeoffs", 101, 404, True, False, True, True),
    ("tradeoffs", 101, 404, True, True, False, True),
    ("tradeoffs", 101, 404, True, True, True, False),
    ("hardware", 101, 505, False, True),
    ("hardware", 101, 505, False, False),
    ("admit", 101, 303, 404, 505, False),
    ("regression", 101, True),
    ("regression", 101, False),
    ("retire", 101, True),
    ("retire", 101, False),
)


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


def reference_candidate() -> dict[str, Any]:
    return {
        "stage": "proposed",
        "candidate_digest": 101,
        "expected_candidate_digest": 101,
        "workload_digest": 202,
        "expected_workload_digest": 202,
        "baseline_digest": 303,
        "expected_baseline_digest": 303,
        "tradeoff_digest": 404,
        "expected_tradeoff_digest": 404,
        "hardware_digest": 505,
        "expected_hardware_digest": 505,
        "structural_receipt_bound": False,
        "baseline_matrix_bound": False,
        "tradeoff_metrics_bound": False,
        "hardware_route_bound": False,
        "fallback_ready": False,
        "receipts": 0,
        "authority_ceiling": 2,
        "support_assignments": 0,
        "external_effects": 0,
    }


def candidate_step(state: dict[str, Any], event: tuple[Any, ...]) -> tuple[str, dict[str, Any]]:
    kind, *args = event
    next_state = copy.deepcopy(state)
    accepted = False
    if kind == "certify":
        candidate, receipt_valid = args
        accepted = (
            state["stage"] == "proposed"
            and candidate == state["candidate_digest"]
            and state["candidate_digest"] == state["expected_candidate_digest"]
            and receipt_valid is True
        )
        if accepted:
            next_state["stage"] = "structure_certified"
            next_state["structural_receipt_bound"] = True
    elif kind == "bind":
        candidate, workload, baseline, complete = args
        accepted = (
            state["stage"] == "structure_certified"
            and candidate == state["candidate_digest"]
            and workload == state["workload_digest"] == state["expected_workload_digest"]
            and baseline == state["baseline_digest"] == state["expected_baseline_digest"]
            and complete is True
        )
        if accepted:
            next_state["stage"] = "baseline_bound"
            next_state["baseline_matrix_bound"] = True
    elif kind == "tradeoffs":
        candidate, tradeoff, quality, runtime, memory, parameters = args
        accepted = (
            state["stage"] == "baseline_bound"
            and candidate == state["candidate_digest"]
            and tradeoff == state["tradeoff_digest"] == state["expected_tradeoff_digest"]
            and all((quality, runtime, memory, parameters))
        )
        if accepted:
            next_state["stage"] = "tradeoffs_recorded"
            next_state["tradeoff_metrics_bound"] = True
    elif kind == "hardware":
        candidate, hardware, kernel_available, refusal_path = args
        accepted = (
            state["stage"] == "tradeoffs_recorded"
            and candidate == state["candidate_digest"]
            and hardware == state["hardware_digest"] == state["expected_hardware_digest"]
            and (kernel_available is True or refusal_path is True)
        )
        if accepted:
            next_state["stage"] = "hardware_qualified"
            next_state["hardware_route_bound"] = True
    elif kind == "admit":
        candidate, baseline, tradeoff, hardware, fallback = args
        accepted = (
            state["stage"] == "hardware_qualified"
            and candidate == state["candidate_digest"]
            and baseline == state["baseline_digest"]
            and tradeoff == state["tradeoff_digest"]
            and hardware == state["hardware_digest"]
            and all(
                (
                    state["structural_receipt_bound"],
                    state["baseline_matrix_bound"],
                    state["tradeoff_metrics_bound"],
                    state["hardware_route_bound"],
                    fallback,
                )
            )
        )
        if accepted:
            next_state["stage"] = "canary_eligible"
            next_state["fallback_ready"] = True
    elif kind == "regression":
        candidate, fallback_applied = args
        accepted = (
            state["stage"] == "canary_eligible"
            and candidate == state["candidate_digest"]
            and state["fallback_ready"] is True
            and fallback_applied is True
        )
        if accepted:
            next_state["stage"] = "retired"
    elif kind == "retire":
        candidate, residual_owned = args
        accepted = (
            state["stage"] != "retired"
            and candidate == state["candidate_digest"]
            and residual_owned is True
        )
        if accepted:
            next_state["stage"] = "retired"
    else:
        raise ValueError(f"unknown cyclic candidate event: {event}")
    if accepted:
        next_state["receipts"] += 1
        return "accepted", next_state
    return "rejected", copy.deepcopy(state)


def run_candidate(state: dict[str, Any], events: tuple[tuple[Any, ...], ...]) -> dict[str, Any]:
    current = copy.deepcopy(state)
    for event in events:
        _, current = candidate_step(current, event)
    return current


def candidate_invariant(state: dict[str, Any]) -> bool:
    if state["support_assignments"] != 0 or state["external_effects"] != 0:
        return False
    required = {
        "structure_certified": ("structural_receipt_bound",),
        "baseline_bound": ("structural_receipt_bound", "baseline_matrix_bound"),
        "tradeoffs_recorded": (
            "structural_receipt_bound",
            "baseline_matrix_bound",
            "tradeoff_metrics_bound",
        ),
        "hardware_qualified": (
            "structural_receipt_bound",
            "baseline_matrix_bound",
            "tradeoff_metrics_bound",
            "hardware_route_bound",
        ),
        "canary_eligible": (
            "structural_receipt_bound",
            "baseline_matrix_bound",
            "tradeoff_metrics_bound",
            "hardware_route_bound",
            "fallback_ready",
        ),
    }
    return all(state[field] is True for field in required.get(state["stage"], ()))


def candidate_key(state: dict[str, Any]) -> tuple[Any, ...]:
    return tuple(state[key] for key in state)


def explore_candidates(roots: tuple[dict[str, Any], ...]) -> dict[tuple[Any, ...], dict[str, Any]]:
    reachable = {candidate_key(root): copy.deepcopy(root) for root in roots}
    frontier = list(reachable.values())
    while frontier:
        state = frontier.pop()
        for event in LIFECYCLE_EVENTS:
            _, next_state = candidate_step(state, event)
            key = candidate_key(next_state)
            if key not in reachable:
                reachable[key] = next_state
                frontier.append(next_state)
    return reachable


def validate_lifecycle(errors: list[str]) -> dict[str, int]:
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z_][A-Za-z0-9_']*)", LEAN_MODULE.read_text()))
    missing = sorted(LIFECYCLE_THEOREMS - theorem_names)
    if missing:
        errors.append(f"CyclicMixers lifecycle theorem surface is missing: {missing}")
    if len(theorem_names) != 23:
        errors.append(f"CyclicMixers theorem count must be 23, observed {len(theorem_names)}")
    completed = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/CyclicMixers.lean"],
        cwd=LEAN_ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    if completed.returncode != 0:
        errors.append(f"CyclicMixers Lean compilation failed: {completed.stdout}{completed.stderr}")

    initial = reference_candidate()
    final = run_candidate(initial, REFERENCE_EVENTS)
    if final["stage"] != "canary_eligible" or final["receipts"] != 5:
        errors.append("reference cyclic candidate did not reach exact canary eligibility")
    regression_route, retired = candidate_step(final, ("regression", 101, True))
    if regression_route != "accepted" or retired["stage"] != "retired":
        errors.append("reference cyclic regression did not retire through fallback")

    split_count = 0
    for index in range(len(REFERENCE_EVENTS) + 1):
        left = REFERENCE_EVENTS[:index]
        right = REFERENCE_EVENTS[index:]
        if run_candidate(initial, REFERENCE_EVENTS) != run_candidate(run_candidate(initial, left), right):
            errors.append(f"cyclic lifecycle composition failed at split {index}")
        else:
            split_count += 1

    roots = [initial]
    for field in (
        "candidate_digest",
        "workload_digest",
        "baseline_digest",
        "tradeoff_digest",
        "hardware_digest",
    ):
        root = reference_candidate()
        root[field] = 999
        roots.append(root)
    reachable = explore_candidates(tuple(roots))
    transition_count = 0
    rejected_count = 0
    retired_states = []
    for state in reachable.values():
        if not candidate_invariant(state):
            errors.append(f"reachable cyclic candidate violates invariant: {state}")
        if state["stage"] == "retired":
            retired_states.append(state)
        for event in LIFECYCLE_EVENTS:
            transition_count += 1
            route, next_state = candidate_step(state, event)
            if any(next_state[field] != state[field] for field in IDENTITY_AND_AUTHORITY_FIELDS):
                errors.append(f"cyclic candidate custody changed through {state['stage']}:{event[0]}")
            if candidate_invariant(state) and not candidate_invariant(next_state):
                errors.append(f"cyclic candidate invariant failed through {state['stage']}:{event[0]}")
            if route == "rejected":
                rejected_count += 1
                if next_state != state:
                    errors.append(f"rejected cyclic event changed state: {state['stage']}:{event}")

    absorbing_transitions = 0
    for state in retired_states:
        for event in LIFECYCLE_EVENTS:
            absorbing_transitions += 1
            _, next_state = candidate_step(state, event)
            if next_state != state:
                errors.append(f"retired cyclic candidate reopened through {event}")

    qualified = run_candidate(initial, REFERENCE_EVENTS[:4])
    structural = run_candidate(initial, REFERENCE_EVENTS[:1])
    if (qualified["candidate_digest"], qualified["structural_receipt_bound"]) != (
        structural["candidate_digest"],
        structural["structural_receipt_bound"],
    ):
        errors.append("structural-summary collision witness drifted")
    if qualified["stage"] != "hardware_qualified" or structural["stage"] == "hardware_qualified":
        errors.append("structural-summary collision no longer separates canary eligibility")

    semantic_mutations = 0
    _, certified = candidate_step(initial, REFERENCE_EVENTS[0])
    for field in IDENTITY_AND_AUTHORITY_FIELDS:
        mutation = copy.deepcopy(certified)
        mutation[field] += 1
        if all(mutation[name] == initial[name] for name in IDENTITY_AND_AUTHORITY_FIELDS):
            errors.append(f"cyclic custody mutation was not detected for {field}")
        else:
            semantic_mutations += 1
    for field in (
        "structural_receipt_bound",
        "baseline_matrix_bound",
        "tradeoff_metrics_bound",
        "hardware_route_bound",
        "fallback_ready",
    ):
        mutation = copy.deepcopy(final)
        mutation[field] = False
        if candidate_invariant(mutation):
            errors.append(f"cyclic stage-coherence mutation was not detected for {field}")
        else:
            semantic_mutations += 1

    return {
        "trace_splits": split_count,
        "reachable_states": len(reachable),
        "reachable_transitions": transition_count,
        "reachable_rejections": rejected_count,
        "retired_states": len(retired_states),
        "absorbing_transitions": absorbing_transitions,
        "semantic_mutations": semantic_mutations,
    }


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
    lifecycle = validate_lifecycle(errors)

    if errors:
        print("Circle cyclic-mixer receipt slice validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)

    print(
        "Circle cyclic-mixer receipt slice validation passed: "
        "CC-AI-CONTRACT-MIXER-001 max_abs_dense_delta=0, "
        "block_to_dense_ratio=0.0625; 23 Lean declarations, "
        f"{lifecycle['trace_splits']}/6 trace splits, {lifecycle['reachable_states']} "
        f"reachable states through {lifecycle['reachable_transitions']} transitions "
        f"({lifecycle['reachable_rejections']} rejections), {lifecycle['retired_states']} "
        f"retired states through {lifecycle['absorbing_transitions']} absorbing transitions, "
        f"and {lifecycle['semantic_mutations']} semantic mutations; no support-state promotion."
    )


if __name__ == "__main__":
    main()

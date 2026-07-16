#!/usr/bin/env python3
"""Replay and consume safety-critical lifecycle decisions at an effect gate."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "experiments" / "safety_critical_lifecycle" / "trace_corpus.json"
RESULT = (
    ROOT
    / "experiments"
    / "safety_critical_lifecycle"
    / "results"
    / "2026-07-15-consumer-local.json"
)

SELECTED_CASES = (
    "valid_alignment_effect",
    "valid_corrigibility_effect",
    "valid_value_conflict_effect",
    "valid_governance_rights_effect",
    "valid_self_improvement_effect",
    "reject_alignment_missing_review",
    "reject_corrigibility_missing_affected_party",
    "reject_value_conflict_missing_residual",
    "reject_governance_missing_exit",
    "reject_self_improvement_self_evaluation",
)

NON_CLAIMS = (
    "This local finite consumer trace is not a deployed effect service or safety system.",
    "A committed fixture effect does not establish moral correctness, legal rights, evaluator quality, or affected-party completeness.",
    "The trace creates no chapter-core support transition, empirical result, reproduction, transfer, deployment, AGI, or ASI claim.",
)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def canonical_sha256(value: Any) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return sha256_bytes(body)


def replay_independently(
    case: dict[str, Any], domain_requirements: dict[str, list[str]]
) -> tuple[bool, str, int, int | None]:
    """A set-based implementation, independent of the state-dict lifecycle checker."""
    recorded = {"protected_predicate"}
    phase = "proposed"
    authority = 3
    support_requested = False
    for index, event in enumerate(case["events"]):
        if event.startswith("record:"):
            recorded.add(event.split(":", 1)[1])
            continue
        if event == "declare_high_impact":
            continue
        if event == "request_support_promotion":
            support_requested = True
            continue
        if event == "commit_effect":
            if not set(domain_requirements[case["domain"]]) <= recorded:
                return False, phase, authority, index
            phase = "effect_committed"
            continue
        if event == "promote_support":
            promotion_ready = (
                phase == "effect_committed"
                and support_requested
                and {"evidence_transition", "non_claim_boundary", "durable_receipt"}
                <= recorded
            )
            if not promotion_ready:
                return False, phase, authority, index
            phase = "promoted"
            continue
        if event.startswith("narrow_authority:"):
            proposed = int(event.split(":", 1)[1])
            if proposed > authority:
                return False, phase, authority, index
            authority = proposed
            continue
        if event.startswith("widen_authority:"):
            proposed = int(event.split(":", 1)[1])
            if proposed > authority:
                return False, phase, authority, index
            authority = proposed
            continue
        if event == "remove_protected_predicate":
            return False, phase, authority, index
        if event == "rollback":
            if "rollback_path" not in recorded or phase not in {
                "effect_committed",
                "promoted",
            }:
                return False, phase, authority, index
            phase = "rolled_back"
            continue
        if event == "revoke":
            authority = 0
            phase = "revoked"
            continue
        return False, phase, authority, index
    return True, phase, authority, None


def build_result(corpus: dict[str, Any]) -> dict[str, Any]:
    cases = {case["id"]: case for case in corpus["cases"]}
    receipts: list[dict[str, Any]] = []
    for case_id in SELECTED_CASES:
        case = cases[case_id]
        accepted, phase, authority, rejected_at = replay_independently(
            case, corpus["domain_requirements"]
        )
        may_commit = accepted and phase == "effect_committed" and authority >= 3
        receipts.append(
            {
                "receipt_id": f"consumer:{case_id}",
                "source_case_id": case_id,
                "domain": case["domain"],
                "trace_sha256": canonical_sha256(case),
                "requested_effect": f"bounded-fixture-effect:{case['domain']}",
                "requested_authority": 3,
                "replay_outcome": "accepted" if accepted else "rejected",
                "rejected_at": rejected_at,
                "final_phase": phase,
                "final_authority": authority,
                "consumer_route": (
                    "commit_proposed_effect" if may_commit else "deny_and_residualize"
                ),
                "effect_count": 1 if may_commit else 0,
                "residual_recorded": not may_commit,
                "support_promotion_claimed": False,
            }
        )
    return {
        "schema_version": "asi_stack.safety_critical_consumer_trace.v1",
        "result_id": "safety-critical-lifecycle-consumer-trace-2026-07-15-local",
        "model_version": corpus["model_version"],
        "consumer_version": "safety-critical-effect-gate.v1",
        "corpus_sha256": sha256_bytes(CORPUS.read_bytes()),
        "selected_case_ids": list(SELECTED_CASES),
        "receipts": receipts,
        "summary": {
            "receipt_count": len(receipts),
            "committed_effect_count": sum(row["effect_count"] for row in receipts),
            "denied_effect_count": sum(
                row["consumer_route"] == "deny_and_residualize" for row in receipts
            ),
            "residual_count": sum(row["residual_recorded"] for row in receipts),
            "support_promotion_count": sum(
                row["support_promotion_claimed"] for row in receipts
            ),
        },
        "support_state_effect": "none",
        "non_claims": list(NON_CLAIMS),
    }


def semantic_errors(value: Any, corpus: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, dict):
        return ["result must be an object"]
    if value.get("schema_version") != "asi_stack.safety_critical_consumer_trace.v1":
        errors.append("wrong schema_version")
    if value.get("model_version") != corpus.get("model_version"):
        errors.append("model_version drift")
    if value.get("corpus_sha256") != sha256_bytes(CORPUS.read_bytes()):
        errors.append("corpus digest mismatch")
    if value.get("selected_case_ids") != list(SELECTED_CASES):
        errors.append("selected case inventory drift")
    if value.get("support_state_effect") != "none":
        errors.append("support_state_effect must remain none")
    non_claims = value.get("non_claims")
    if not isinstance(non_claims, list) or len(non_claims) < 3:
        errors.append("at least three non-claims are required")

    cases = {case["id"]: case for case in corpus.get("cases", [])}
    receipts = value.get("receipts")
    if not isinstance(receipts, list):
        return errors + ["receipts must be a list"]
    receipt_ids = [row.get("receipt_id") for row in receipts if isinstance(row, dict)]
    source_ids = [row.get("source_case_id") for row in receipts if isinstance(row, dict)]
    if len(receipt_ids) != len(receipts) or len(receipt_ids) != len(set(receipt_ids)):
        errors.append("receipt IDs must be present and unique")
    if source_ids != list(SELECTED_CASES):
        errors.append("receipt source order or coverage drift")

    for row in receipts:
        if not isinstance(row, dict):
            errors.append("receipt must be an object")
            continue
        case_id = row.get("source_case_id")
        case = cases.get(case_id)
        if case is None:
            errors.append(f"{case_id}: missing source case")
            continue
        accepted, phase, authority, rejected_at = replay_independently(
            case, corpus["domain_requirements"]
        )
        expected_outcome = "accepted" if accepted else "rejected"
        may_commit = accepted and phase == "effect_committed" and authority >= int(
            row.get("requested_authority", 10**9)
        )
        expected_route = "commit_proposed_effect" if may_commit else "deny_and_residualize"
        if row.get("domain") != case["domain"]:
            errors.append(f"{case_id}: domain mismatch")
        if row.get("trace_sha256") != canonical_sha256(case):
            errors.append(f"{case_id}: trace digest mismatch")
        if row.get("replay_outcome") != expected_outcome:
            errors.append(f"{case_id}: replay outcome mismatch")
        if row.get("rejected_at") != rejected_at:
            errors.append(f"{case_id}: rejection index mismatch")
        if row.get("final_phase") != phase or row.get("final_authority") != authority:
            errors.append(f"{case_id}: final state mismatch")
        if row.get("consumer_route") != expected_route:
            errors.append(f"{case_id}: consumer route mismatch")
        if row.get("effect_count") != (1 if may_commit else 0):
            errors.append(f"{case_id}: effect count violates gate decision")
        if row.get("residual_recorded") is not (not may_commit):
            errors.append(f"{case_id}: denial residual mismatch")
        if row.get("support_promotion_claimed") is not False:
            errors.append(f"{case_id}: fixture consumer cannot claim support promotion")

    expected = build_result(corpus)
    if value.get("summary") != expected["summary"]:
        errors.append("summary does not recompute from receipts")
    return errors


def negative_control_errors(value: dict[str, Any], corpus: dict[str, Any]) -> list[str]:
    controls: list[tuple[str, dict[str, Any]]] = []

    mutated = deepcopy(value)
    mutated["corpus_sha256"] = "0" * 64
    controls.append(("corpus_digest_forgery", mutated))

    mutated = deepcopy(value)
    mutated["receipts"][0]["trace_sha256"] = "f" * 64
    controls.append(("trace_digest_forgery", mutated))

    mutated = deepcopy(value)
    mutated["receipts"][0]["domain"] = "self_improvement"
    controls.append(("domain_substitution", mutated))

    mutated = deepcopy(value)
    mutated["receipts"][5]["replay_outcome"] = "accepted"
    controls.append(("rejected_trace_acceptance_forgery", mutated))

    mutated = deepcopy(value)
    mutated["receipts"][5]["consumer_route"] = "commit_proposed_effect"
    mutated["receipts"][5]["effect_count"] = 1
    mutated["receipts"][5]["residual_recorded"] = False
    controls.append(("effect_on_rejected_trace", mutated))

    mutated = deepcopy(value)
    mutated["receipts"][0]["requested_authority"] = 4
    controls.append(("effect_above_replayed_authority", mutated))

    mutated = deepcopy(value)
    mutated["receipts"][0]["support_promotion_claimed"] = True
    controls.append(("support_promotion_laundering", mutated))

    mutated = deepcopy(value)
    mutated["receipts"].append(deepcopy(mutated["receipts"][0]))
    controls.append(("duplicate_receipt", mutated))

    errors: list[str] = []
    for label, control in controls:
        if not semantic_errors(control, corpus):
            errors.append(f"negative control {label!r} was accepted")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    expected = build_result(corpus)
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(expected, indent=2) + "\n", encoding="utf-8")
    if not RESULT.exists():
        raise SystemExit(f"Missing {RESULT.relative_to(ROOT)}; rerun with --write-result")
    value = json.loads(RESULT.read_text(encoding="utf-8"))
    errors = semantic_errors(value, corpus)
    if value != expected:
        errors.append("tracked result differs from independent recomputation")
    errors.extend(negative_control_errors(value, corpus))
    if errors:
        print("Safety-critical lifecycle consumer trace validation failed:")
        for error in errors:
            print(f" - {error}")
        sys.exit(1)
    summary = value["summary"]
    print(
        "Safety-critical lifecycle consumer trace passed: "
        f"{summary['receipt_count']} receipts, "
        f"{summary['committed_effect_count']} bounded fixture effects, "
        f"{summary['denied_effect_count']} denials with residuals, "
        "8 rejecting mutations, support-state effect none."
    )


if __name__ == "__main__":
    main()

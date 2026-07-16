#!/usr/bin/env python3
"""Check an executable refinement from a real governed-result schema.

This is intentionally not a second hand-authored trace corpus. It consumes the
executed governed repository-change result, validates that concrete artifact
against its public schema, losslessly round-trips the exact fields used by the
abstraction, and rejects semantic mutations at the concrete-schema boundary.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any, Callable

import jsonschema


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "experiments/governed_repository_change_slice/results/2026-07-10-local.json"
SOURCE_SCHEMA = ROOT / "schemas/governed_repository_change_result.schema.json"
LEAN_MODEL = ROOT / "lean/AsiStackProofs/IntegratedReferenceTrace.lean"
RESULT = ROOT / "experiments/integrated_reference_trace/results/2026-07-15-runtime-schema-refinement.json"
RESULT_SCHEMA = ROOT / "schemas/integrated_runtime_schema_refinement.schema.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonical_sha(value: Any) -> str:
    body = json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(body).hexdigest()


def project(source: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    governed = row["governed"]
    verification = governed.get("verification", {})
    return {
        "scenario_id": row["scenario_id"],
        "decision": governed["decision"],
        "expected_decision": governed["expected_decision"],
        "event_log": list(governed["event_log"]),
        "authorization_blocked_before_effect": governed["authorization_blocked_before_effect"],
        "reviewer_independence_blocked_before_effect": governed["reviewer_independence_blocked_before_effect"],
        "rollback_attempted": governed["rollback_attempted"],
        "rollback_exact": governed["rollback_exact"],
        "final_tree_matches_initial_after_refusal": governed["final_tree_matches_initial_after_refusal"],
        "residuals_discovered": governed["residuals_discovered"],
        "unsafe_effect_observed": governed["unsafe_effect_observed"],
        "unsafe_release": governed["unsafe_release"],
        "correct_disposition": governed["correct_disposition"],
        "effect_observed_independently": verification.get("effect_observed_independently", False),
        "independent_identity": verification.get("independent_identity", False),
        "receipt_matches_observed_artifact": verification.get("receipt_matches_observed_artifact", False),
        "unauthorized_changed_paths": list(verification.get("unauthorized_changed_paths", [])),
        "support_state_effect": source["support_state_effect"],
        "evidence_transition_created": source["evidence_transition_created"],
    }


def encode(projection: dict[str, Any]) -> dict[str, Any]:
    """Version and custody-wrap the exact concrete fields used by abstraction."""
    return {
        "adapter_schema": "asi_stack.integrated_runtime_projection.v1",
        "source_pointer": f"/scenario_results/{projection['scenario_id']}/governed",
        "projection": copy.deepcopy(projection),
        "projection_sha256": canonical_sha(projection),
    }


def decode(encoded: dict[str, Any]) -> dict[str, Any]:
    if encoded.get("adapter_schema") != "asi_stack.integrated_runtime_projection.v1":
        raise ValueError("adapter schema drift")
    projection = copy.deepcopy(encoded.get("projection"))
    if canonical_sha(projection) != encoded.get("projection_sha256"):
        raise ValueError("projection custody digest mismatch")
    return projection


def abstract(record: dict[str, Any]) -> dict[str, Any]:
    events = set(record["event_log"])
    effect = "sandboxed_repository_effect_applied" in events
    observed = "independent_effect_observation_completed" in events
    evidence = "evidence_packet_accepted" in events
    exact_rollback = "rollback_exact" in events
    failed_rollback = "rollback_incomplete" in events
    if record["decision"] == "release":
        trace_class = "approved_completion"
    elif record["decision"] == "quarantine":
        trace_class = "failed_rollback_quarantine"
    elif record["rollback_attempted"]:
        trace_class = "exact_rollback"
    else:
        trace_class = "pre_effect_refusal"
    return {
        "scenario_id": record["scenario_id"],
        "trace_class": trace_class,
        "effect_committed": effect,
        "effect_acknowledged": observed and record["effect_observed_independently"],
        "independent_evaluator": record["independent_identity"],
        "evidence_admitted": evidence,
        "rollback_attempted": record["rollback_attempted"],
        "rollback_exact": exact_rollback and record["rollback_exact"],
        "rollback_failed": failed_rollback and not record["rollback_exact"],
        "open_residuals": record["residuals_discovered"] if not record["rollback_exact"] else 0,
        "terminal_receipt": any(name in events for name in ("release_committed", "release_refused", "repository_quarantined")),
        "support_state_effect": record["support_state_effect"],
    }


def refinement_errors(record: dict[str, Any], view: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    events = set(record["event_log"])
    if record["decision"] != record["expected_decision"] or record["correct_disposition"] is not True:
        errors.append("incorrect_disposition")
    if record["support_state_effect"] != "none" or record["evidence_transition_created"] is not False:
        errors.append("support_transition_laundering")
    if record["unsafe_release"] is not False:
        errors.append("unsafe_release")
    if record["authorization_blocked_before_effect"] or record["reviewer_independence_blocked_before_effect"]:
        if view["effect_committed"]:
            errors.append("pre_effect_block_has_effect")
    if view["effect_committed"] and "proposal_receipt_emitted" not in events:
        errors.append("effect_without_proposal_receipt")
    if view["effect_acknowledged"] != (
        "independent_effect_observation_completed" in events
        and record["effect_observed_independently"] is True
    ):
        errors.append("observation_refinement_mismatch")
    if view["trace_class"] == "approved_completion":
        if not all((view["effect_committed"], view["effect_acknowledged"], view["independent_evaluator"], view["evidence_admitted"], view["terminal_receipt"])):
            errors.append("incomplete_approved_trace")
        if record["rollback_attempted"] or record["unauthorized_changed_paths"]:
            errors.append("approved_trace_has_rollback_or_unauthorized_path")
    elif view["trace_class"] == "pre_effect_refusal":
        if view["effect_committed"] or record["rollback_attempted"] or not record["final_tree_matches_initial_after_refusal"]:
            errors.append("invalid_pre_effect_refusal")
        if "effect_refused" not in events:
            errors.append("refusal_receipt_missing")
    elif view["trace_class"] == "exact_rollback":
        if not all((view["effect_committed"], view["effect_acknowledged"], record["rollback_attempted"], view["rollback_exact"], record["final_tree_matches_initial_after_refusal"], view["terminal_receipt"])):
            errors.append("incomplete_exact_rollback")
        if "verification_gate_failed" not in events:
            errors.append("rollback_without_failed_gate")
    elif view["trace_class"] == "failed_rollback_quarantine":
        if not all((view["effect_committed"], view["effect_acknowledged"], record["rollback_attempted"], view["rollback_failed"], view["terminal_receipt"])):
            errors.append("incomplete_quarantine")
        if record["final_tree_matches_initial_after_refusal"] or view["open_residuals"] < 1:
            errors.append("quarantine_erases_failed_rollback_residual")
    return errors


def validate_candidate(source: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    try:
        jsonschema.Draft202012Validator(load(SOURCE_SCHEMA)).validate(source)
    except jsonschema.ValidationError as exc:
        return [f"source_schema:{exc.message}"]
    for row in source["scenario_results"]:
        original = project(source, row)
        encoded = encode(original)
        try:
            decoded = decode(encoded)
        except ValueError as exc:
            errors.append(f"{row.get('scenario_id', 'unknown')}:{exc}")
            continue
        if decoded != original:
            errors.append(f"{row['scenario_id']}:projection_round_trip_mismatch")
        errors.extend(f"{row['scenario_id']}:{error}" for error in refinement_errors(decoded, abstract(decoded)))
    return errors


def mutate(row: dict[str, Any], fn: Callable[[dict[str, Any]], None]) -> dict[str, Any]:
    candidate = copy.deepcopy(row)
    fn(candidate)
    return candidate


def mutation_suite(source: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    by_id = {row["scenario_id"]: index for index, row in enumerate(source["scenario_results"])}
    mutations: list[tuple[str, dict[str, Any]]] = []

    def add(label: str, scenario: str, fn: Callable[[dict[str, Any]], None]) -> None:
        candidate = copy.deepcopy(source)
        index = by_id[scenario]
        candidate["scenario_results"][index] = mutate(candidate["scenario_results"][index], fn)
        mutations.append((label, candidate))

    add("release decision mismatch", "nominal_valid_change", lambda r: r["governed"].__setitem__("expected_decision", "refuse"))
    add("release without effect", "nominal_valid_change", lambda r: r["governed"]["event_log"].remove("sandboxed_repository_effect_applied"))
    add("release without proposal receipt", "nominal_valid_change", lambda r: r["governed"]["event_log"].remove("proposal_receipt_emitted"))
    add("release without observation event", "nominal_valid_change", lambda r: r["governed"]["event_log"].remove("independent_effect_observation_completed"))
    add("release without observed effect", "nominal_valid_change", lambda r: r["governed"]["verification"].__setitem__("effect_observed_independently", False))
    add("release with correlated evaluator", "nominal_valid_change", lambda r: r["governed"]["verification"].__setitem__("independent_identity", False))
    add("release without evidence", "nominal_valid_change", lambda r: r["governed"]["event_log"].remove("evidence_packet_accepted"))
    add("release without terminal receipt", "nominal_valid_change", lambda r: r["governed"]["event_log"].remove("release_committed"))
    add("release with unauthorized path", "nominal_valid_change", lambda r: r["governed"]["verification"].__setitem__("unauthorized_changed_paths", ["secret.txt"]))
    add("unsafe release laundering", "nominal_valid_change", lambda r: r["governed"].__setitem__("unsafe_release", True))
    add("authorization block with effect", "stale_authorization", lambda r: r["governed"]["event_log"].append("sandboxed_repository_effect_applied"))
    add("reviewer block with effect", "correlated_proposer_verifier", lambda r: r["governed"]["event_log"].append("sandboxed_repository_effect_applied"))
    add("refusal without refusal receipt", "stale_authorization", lambda r: r["governed"]["event_log"].remove("effect_refused"))
    add("exact rollback without exact event", "forged_mismatched_receipt", lambda r: r["governed"]["event_log"].remove("rollback_exact"))
    add("exact rollback without restored tree", "hidden_residual_cost", lambda r: r["governed"].__setitem__("final_tree_matches_initial_after_refusal", False))
    add("rollback without failed gate", "hidden_residual_cost", lambda r: r["governed"]["event_log"].remove("verification_gate_failed"))
    add("failed rollback erases residual", "failed_rollback", lambda r: r["governed"].__setitem__("residuals_discovered", 0))
    add("quarantine claims restored tree", "failed_rollback", lambda r: r["governed"].__setitem__("final_tree_matches_initial_after_refusal", True))
    promoted = copy.deepcopy(source)
    promoted["support_state_effect"] = "prototype-backed"
    mutations.append(("support promotion", promoted))
    transitioned = copy.deepcopy(source)
    transitioned["evidence_transition_created"] = True
    mutations.append(("evidence transition invention", transitioned))
    return mutations


def build_result() -> tuple[dict[str, Any], list[str]]:
    source = load(SOURCE)
    errors = validate_candidate(source)
    records = []
    for row in source["scenario_results"]:
        projection = project(source, row)
        encoded = encode(projection)
        view = abstract(decode(encoded))
        records.append({
            "scenario_id": projection["scenario_id"],
            "trace_class": view["trace_class"],
            "projection_sha256": encoded["projection_sha256"],
            "effect_committed": view["effect_committed"],
            "effect_acknowledged": view["effect_acknowledged"],
            "rollback_exact": view["rollback_exact"],
            "rollback_failed": view["rollback_failed"],
            "open_residuals": view["open_residuals"],
            "terminal_receipt": view["terminal_receipt"],
        })
    mutations = mutation_suite(source)
    rejected = 0
    for label, candidate in mutations:
        if validate_candidate(candidate):
            rejected += 1
        else:
            errors.append(f"mutation accepted: {label}")
    classes = {name: sum(row["trace_class"] == name for row in records) for name in (
        "approved_completion", "pre_effect_refusal", "exact_rollback", "failed_rollback_quarantine"
    )}
    result = {
        "schema_version": "asi_stack.integrated_runtime_schema_refinement_result.v1",
        "result_id": "integrated-runtime-schema-refinement-2026-07-15-local",
        "source_result_ref": SOURCE.relative_to(ROOT).as_posix(),
        "source_result_sha256": sha(SOURCE),
        "source_schema_ref": SOURCE_SCHEMA.relative_to(ROOT).as_posix(),
        "source_schema_sha256": sha(SOURCE_SCHEMA),
        "lean_model_ref": LEAN_MODEL.relative_to(ROOT).as_posix(),
        "lean_model_sha256": sha(LEAN_MODEL),
        "scenario_count": len(records),
        "round_trip_count": len(records),
        "trace_class_counts": classes,
        "mutation_count": len(mutations),
        "mutation_rejection_count": rejected,
        "records": records,
        "support_state_effect": "none",
        "non_claims": [
            "This is checked executable refinement for the exact projected fields of one local governed-result schema, not a proof that the runtime implements the Lean model.",
            "Deterministic encoding and lossless projection round-trip do not establish semantic payload truth, complete effect discovery, concurrency, distribution, or deployed enforcement.",
            "The nine source scenarios are synthetic local repository-change cases and do not establish natural-workload performance, safety, reproduction, transfer, or chapter-core support.",
        ],
    }
    try:
        jsonschema.Draft202012Validator(load(RESULT_SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc:
        errors.append(f"result_schema:{exc.message}")
    return result, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result, errors = build_result()
    if errors:
        raise SystemExit("Integrated runtime-schema refinement failed:\n - " + "\n - ".join(errors))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result:
        raise SystemExit("Integrated runtime-schema refinement failed:\n - tracked result is stale; run with --write")
    print(
        f"Integrated runtime-schema refinement passed: {result['scenario_count']} source scenarios round-tripped, "
        f"classes={result['trace_class_counts']}, {result['mutation_rejection_count']} mutations rejected, support effect none."
    )


if __name__ == "__main__":
    main()

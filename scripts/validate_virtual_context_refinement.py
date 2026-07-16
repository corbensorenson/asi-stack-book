#!/usr/bin/env python3
"""Independently consume the reachable Virtual Context ABI refinement."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/VirtualContextRefinement.lean"
PRIOR = ROOT / "experiments/vcm_resolver_certificate_probe/results/2026-07-02-local.json"
ADMISSION_FIXTURES = ROOT / "experiments/context_admission_adequacy/fixtures"
ADMISSION_VALIDATOR = ROOT / "scripts/validate_context_admission_adequacy.py"
SCHEMA = ROOT / "schemas/virtual_context_refinement.schema.json"
RESULT = ROOT / "experiments/virtual_context_refinement/results/2026-07-15-local.json"
IDENTITY = ("request_id", "address", "version", "snapshot", "mount", "mandatory")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory_sha(paths: list[Path]) -> str:
    body = "\n".join(f"{path.name}:{sha(path)}" for path in paths) + "\n"
    return hashlib.sha256(body.encode()).hexdigest()


def initial() -> dict[str, Any]:
    return {"stage": "raw", "request_id": 0, "address": 0, "version": 0,
            "snapshot": 0, "mount": 0, "authority_ceiling": 3,
            "approved_authority": 0, "lease_expiry": 0, "source_hash": 0,
            "derived_hash": 0, "mandatory": False, "resolver_receipt": False,
            "certificate_receipt": False, "materialization_receipt": False,
            "typed_fault_receipt": False, "materialization_emitted": False,
            "logical_time": 0}


def event(kind: str, source: str, target: str, time: int) -> dict[str, Any]:
    return {"kind": kind, "from_stage": source, "to_stage": target,
            "request_id": 101, "address": 201, "version": 301,
            "snapshot": 401, "mount": 501, "requested_authority": 2,
            "lease_expiry": 20, "source_hash": 601, "derived_hash": 701,
            "certificate_source_hash": 601, "mandatory": True,
            "resolver_found": False, "mount_permitted": True,
            "resolver_receipt": False, "certificate_receipt": False,
            "omission_declared": True, "exact_completeness_claimed": False,
            "taint_detected": False, "materialization_receipt": False,
            "typed_fault_receipt": False, "materialization_emitted": False,
            "denial_receipt": False, "logical_time": time}


def traces() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    bind = event("bind_request", "raw", "request_bound", 1)
    hit = event("resolve_hit", "request_bound", "resolved", 2)
    hit.update(resolver_found=True, resolver_receipt=True)
    certify = event("certify", "resolved", "certified", 3)
    certify["certificate_receipt"] = True
    materialize = event("materialize", "certified", "materialized", 4)
    materialize.update(materialization_receipt=True, materialization_emitted=True)
    miss = event("resolve_miss", "request_bound", "typed_fault", 2)
    miss["typed_fault_receipt"] = True
    return [bind, hit, certify, materialize], [copy.deepcopy(bind), miss]


def matches(state: dict[str, Any], row: dict[str, Any]) -> bool:
    return all(state[key] == row[key] for key in IDENTITY)


def errors(state: dict[str, Any], row: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if state["stage"] != row["from_stage"]: out.append("stage_mismatch")
    if state["logical_time"] >= row["logical_time"]: out.append("time_not_monotonic")
    kind = row["kind"]
    if kind == "bind_request":
        if (row["from_stage"], row["to_stage"]) != ("raw", "request_bound"): out.append("bind_stage")
        if any(row[key] <= 0 for key in ("request_id", "address", "version", "snapshot", "mount")): out.append("missing_request_identity")
        if row["requested_authority"] > state["authority_ceiling"]: out.append("authority_widened")
        if row["logical_time"] >= row["lease_expiry"]: out.append("lease_expired_at_bind")
    elif kind == "resolve_hit":
        if (row["from_stage"], row["to_stage"]) != ("request_bound", "resolved"): out.append("hit_stage")
        if not matches(state, row): out.append("request_substitution")
        if not row["resolver_found"]: out.append("resolver_miss_laundered")
        if not row["mount_permitted"]: out.append("mount_denied")
        if row["logical_time"] >= state["lease_expiry"]: out.append("lease_expired")
        if row["source_hash"] <= 0: out.append("source_missing")
        if not row["resolver_receipt"]: out.append("resolver_receipt_missing")
        if row["typed_fault_receipt"]: out.append("fault_on_hit")
        if row["materialization_emitted"]: out.append("early_materialization")
    elif kind == "resolve_miss":
        if (row["from_stage"], row["to_stage"]) != ("request_bound", "typed_fault"): out.append("miss_stage")
        if row["request_id"] != state["request_id"]: out.append("request_substitution")
        if not row["mandatory"]: out.append("optional_miss_laundered")
        if row["resolver_found"]: out.append("hit_routed_as_miss")
        if not row["typed_fault_receipt"]: out.append("typed_fault_receipt_missing")
        if row["materialization_emitted"] or row["materialization_receipt"]: out.append("miss_materialized")
    elif kind == "certify":
        if (row["from_stage"], row["to_stage"]) != ("resolved", "certified"): out.append("certificate_stage")
        if not matches(state, row): out.append("request_substitution")
        if row["source_hash"] != state["source_hash"] or row["certificate_source_hash"] != state["source_hash"]: out.append("certificate_source_mismatch")
        if row["derived_hash"] <= 0: out.append("derived_hash_missing")
        if row["requested_authority"] > state["approved_authority"]: out.append("certificate_authority_escalation")
        if not row["certificate_receipt"]: out.append("certificate_receipt_missing")
        if not row["omission_declared"]: out.append("undeclared_omission")
        if row["exact_completeness_claimed"]: out.append("exact_completeness_overclaim")
        if row["taint_detected"]: out.append("tainted_certificate")
        if row["materialization_emitted"]: out.append("early_materialization")
    elif kind == "materialize":
        if (row["from_stage"], row["to_stage"]) != ("certified", "materialized"): out.append("materialization_stage")
        if not matches(state, row): out.append("request_substitution")
        if row["source_hash"] != state["source_hash"] or row["derived_hash"] != state["derived_hash"]: out.append("materialization_binding_mismatch")
        if row["requested_authority"] > state["approved_authority"]: out.append("materialization_authority_escalation")
        if not state["resolver_receipt"] or not state["certificate_receipt"]: out.append("receipt_custody_missing")
        if row["taint_detected"]: out.append("tainted_materialization")
        if not row["materialization_receipt"]: out.append("materialization_receipt_missing")
        if not row["materialization_emitted"]: out.append("materialization_not_emitted")
        if row["typed_fault_receipt"]: out.append("fault_materialization_conflict")
    else:
        out.append("unknown_event")
    return out


def apply(state: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    nxt = copy.deepcopy(state); nxt["stage"] = row["to_stage"]
    if row["kind"] == "bind_request":
        for key in IDENTITY: nxt[key] = row[key]
        nxt["approved_authority"] = row["requested_authority"]
        nxt["lease_expiry"] = row["lease_expiry"]
    if row["kind"] == "resolve_hit": nxt["source_hash"] = row["source_hash"]
    if row["kind"] == "certify": nxt["derived_hash"] = row["derived_hash"]
    for key in ("resolver_receipt", "certificate_receipt", "materialization_receipt", "typed_fault_receipt", "materialization_emitted"):
        nxt[key] = nxt[key] or row[key]
    nxt["logical_time"] = row["logical_time"]
    return nxt


def run(rows: list[dict[str, Any]]) -> tuple[bool, int | None, list[str], dict[str, Any]]:
    state = initial()
    for index, row in enumerate(rows):
        found = errors(state, row)
        if found: return False, index, found, state
        state = apply(state, row)
    return True, None, [], state


def mutations(base: list[dict[str, Any]], miss: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    out: list[tuple[str, list[dict[str, Any]]]] = []
    def m(name: str, rows: list[dict[str, Any]], index: int, key: str, value: Any) -> None:
        changed = copy.deepcopy(rows); changed[index][key] = value; out.append((name, changed))
    for key in ("request_id", "address", "version", "snapshot", "mount"): m("bind_" + key + "_missing", base, 0, key, 0)
    m("bind_authority_widened", base, 0, "requested_authority", 4)
    m("bind_expired_lease", base, 0, "lease_expiry", 1)
    for key in IDENTITY: m("hit_" + key + "_substitution", base, 1, key, 999 if key != "mandatory" else False)
    for name, key, value in (("not_found", "resolver_found", False), ("mount_denied", "mount_permitted", False), ("expired", "logical_time", 20), ("source_missing", "source_hash", 0), ("receipt_missing", "resolver_receipt", False), ("fault_conflict", "typed_fault_receipt", True), ("early_materialization", "materialization_emitted", True)):
        m("hit_" + name, base, 1, key, value)
    for key in IDENTITY: m("certify_" + key + "_substitution", base, 2, key, 999 if key != "mandatory" else False)
    for name, key, value in (("source", "source_hash", 999), ("certificate_source", "certificate_source_hash", 999), ("derived_missing", "derived_hash", 0), ("authority", "requested_authority", 3), ("receipt", "certificate_receipt", False), ("omission", "omission_declared", False), ("overclaim", "exact_completeness_claimed", True), ("taint", "taint_detected", True), ("early_materialization", "materialization_emitted", True)):
        m("certify_" + name, base, 2, key, value)
    for key in IDENTITY: m("materialize_" + key + "_substitution", base, 3, key, 999 if key != "mandatory" else False)
    for name, key, value in (("source", "source_hash", 999), ("derived", "derived_hash", 999), ("authority", "requested_authority", 3), ("taint", "taint_detected", True), ("receipt", "materialization_receipt", False), ("not_emitted", "materialization_emitted", False), ("fault_conflict", "typed_fault_receipt", True), ("time", "logical_time", 3)):
        m("materialize_" + name, base, 3, key, value)
    for name, key, value in (("request", "request_id", 999), ("optional", "mandatory", False), ("found", "resolver_found", True), ("fault_receipt", "typed_fault_receipt", False), ("emission", "materialization_emitted", True), ("materialization_receipt", "materialization_receipt", True)):
        m("miss_" + name, miss, 1, key, value)
    return out


def prior_receipts(prior: dict[str, Any], issues: list[str]) -> list[dict[str, Any]]:
    rows = prior.get("valid_scenarios", []) + prior.get("expected_invalid_controls", [])
    expected_valid = {
        "valid_resolver_materialization_receipt": (True, "materialize_context", True, False),
        "valid_mandatory_miss_typed_fault": (True, "issue_typed_fault", False, True),
        "invalid_address_mismatch_materialization_denied": (False, "issue_typed_fault", False, True),
        "invalid_version_mismatch_materialization_denied": (False, "issue_typed_fault", False, True),
        "invalid_snapshot_mismatch_materialization_denied": (False, "issue_typed_fault", False, True),
        "invalid_mount_policy_denied": (False, "deny_mount_policy", False, False),
        "invalid_lease_expired_reuse_blocked": (False, "deny_expired_lease", False, False),
        "invalid_certificate_source_binding_mismatch_denied": (False, "reject_source_binding_mismatch", False, False),
        "invalid_certificate_authority_escalation_denied": (False, "reject_authority_escalation", False, False),
        "invalid_certificate_truthfulness_overclaim_denied": (False, "reject_truthfulness_overclaim", False, False),
        "invalid_summary_fidelity_omission_denied": (False, "reject_undeclared_omission", False, False),
    }
    receipts = []
    if {row.get("scenario_id") for row in rows} != set(expected_valid): issues.append("resolver scenario inventory drift")
    for row in rows:
        sid = row.get("scenario_id"); expected = expected_valid.get(sid)
        outcome = row.get("outcome", {}); accepted = expected is not None and (
            row.get("expected_valid"), row.get("actual_route"), outcome.get("materialization_emitted"), outcome.get("typed_fault_emitted")) == expected
        bounded = accepted and row.get("scenario_pass") is True and all(outcome.get(key) is False for key in ("model_called", "network_used", "private_source_read")) and outcome.get("support_state_effect") == "none" and outcome.get("chapter_core_support_effect") == "none"
        if not bounded: issues.append(str(sid) + ": prior resolver receipt drift")
        receipts.append({"scenario_id": sid, "expected_valid": row.get("expected_valid"), "independently_matched": bounded, "route": row.get("actual_route")})
    return receipts


def build() -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []
    base, miss = traces(); ok, _, _, final = run(base); miss_ok, _, _, miss_final = run(miss)
    if not ok or final["stage"] != "materialized" or not final["materialization_emitted"]: issues.append("reference materialization trace rejected")
    if not miss_ok or miss_final["stage"] != "typed_fault" or not miss_final["typed_fault_receipt"] or miss_final["materialization_emitted"]: issues.append("reference mandatory-miss trace rejected")
    mutation_receipts = []
    for mid, rows in mutations(base, miss):
        accepted, index, why, _ = run(rows)
        mutation_receipts.append({"mutation_id": mid, "rejected": not accepted, "failed_event_index": index, "reasons": why})
        if accepted: issues.append(mid + ": mutation accepted")
    prior = load(PRIOR); resolver_receipts = prior_receipts(prior, issues)
    fixture_paths = sorted(ADMISSION_FIXTURES.glob("*.json"))
    admission = subprocess.run(["python3", str(ADMISSION_VALIDATOR)], cwd=ROOT, text=True, capture_output=True)
    if admission.returncode != 0: issues.append("context admission suite failed: " + admission.stdout + admission.stderr)
    valid_names = [path.name for path in fixture_paths if path.name.startswith("valid_")]
    invalid_names = [path.name for path in fixture_paths if path.name.startswith("invalid_")]
    if len(valid_names) != 3 or len(invalid_names) != 5: issues.append("context admission fixture inventory drift")
    result = {
        "schema_version": "asi_stack.virtual_context_refinement.v1",
        "result_id": "virtual-context-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha(LEAN), "prior_resolver_result": sha(PRIOR), "admission_fixture_inventory": inventory_sha(fixture_paths), "admission_validator": sha(ADMISSION_VALIDATOR)},
        "resolver_scenario_count": len(resolver_receipts), "resolver_valid_count": sum(row["expected_valid"] for row in resolver_receipts), "resolver_invalid_count": sum(not row["expected_valid"] for row in resolver_receipts), "resolver_receipts": resolver_receipts,
        "admission_fixture_count": len(fixture_paths), "admission_valid_fixture_count": len(valid_names), "admission_invalid_fixture_count": len(invalid_names), "admission_suite_passed": admission.returncode == 0,
        "materialization_trace_event_count": len(base), "mandatory_miss_trace_event_count": len(miss), "materialization_final_state": final, "mandatory_miss_final_state": miss_final,
        "mutation_count": len(mutation_receipts), "mutation_rejection_count": sum(row["rejected"] for row in mutation_receipts), "mutation_receipts": mutation_receipts,
        "support_state_effect": "none",
        "non_claims": [
            "The equality checks use trusted numeric identifiers and do not establish natural-language address truth, payload meaning, summary fidelity, or certificate truthfulness.",
            "The admission fixture suite is consumed as a distinct prior harness; admission validity is not treated as resolver or materialization correctness.",
            "This packet does not establish a deployed resolver, memory store, context compiler, transaction isolation, deletion enforcement, model-facing context quality, leak prevention, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support."
        ]
    }
    try: jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc: issues.append("result schema: " + exc.message)
    return result, issues


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    result, issues = build()
    if issues: raise SystemExit("Virtual context refinement failed:\n - " + "\n - ".join(issues))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result: raise SystemExit("Virtual context refinement result stale; run --write")
    print(f"Virtual context refinement passed: {result['resolver_valid_count']} valid/{result['resolver_invalid_count']} invalid resolver scenarios, 3/5 admission fixtures, {result['mutation_rejection_count']} mutations rejected, support effect none.")


if __name__ == "__main__": main()

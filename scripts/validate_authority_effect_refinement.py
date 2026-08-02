#!/usr/bin/env python3
"""Consume the reachable authority/effect model against executed local evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/AuthorityEffectRefinement.lean"
AUTHORITY_FIXTURES = ROOT / "experiments/authority_transitions/fixtures"
RUNTIME = ROOT / "experiments/runtime_adapter_effect_probe/results/2026-07-02-local.json"
REVOCATION = ROOT / "experiments/authority_revocation_trace/results/2026-07-03-local.json"
GOVERNED = ROOT / "experiments/governed_repository_change_slice/results/2026-07-10-local.json"
GOVERNED_SCHEMA = ROOT / "schemas/governed_repository_change_result.schema.json"
SCHEMA = ROOT / "schemas/authority_effect_refinement.schema.json"
RESULT = ROOT / "experiments/authority_effect_refinement/results/2026-07-15-local.json"

RANK = {
    "public_read": 1,
    "public_transform": 2,
    "tracked_file_write": 3,
    "local_fixture_execute": 4,
    "external_effect": 5,
    "governance_approval": 6,
}
MINIMUM = {"read": 1, "transform": 2, "write": 3, "execute": 4, "disclose": 5, "approve": 6}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def grant(event: dict[str, Any]) -> dict[str, int]:
    return {key: event[key] for key in ("grant_id", "principal", "operation", "target", "authority", "epoch", "expires", "uses")}


def initial() -> dict[str, Any]:
    return {"caller_ceiling": 3, "epoch": 11, "time": 0, "grant": None, "approved": None, "dispatched": None, "revoked": [], "effects": 0, "observed": 0, "rolled_back": False}


def event(kind: str, time: int) -> dict[str, Any]:
    return {"kind": kind, "grant_id": 71, "principal": 101, "operation": 201, "target": 301, "authority": 3, "epoch": 11, "expires": 20, "uses": 1, "time": time, "owner": True, "approval": True, "dispatch_receipt": True, "effect_receipt": True, "observer": True, "revocation_receipt": True, "rollback_exact": True}


def event_errors(state: dict[str, Any], row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if row["time"] <= state["time"]:
        errors.append("non_monotone_time")
    kind = row["kind"]
    exact = grant(row)
    if kind == "issue":
        if state["grant"] is not None or row["grant_id"] in state["revoked"] or row["grant_id"] <= 0:
            errors.append("invalid_grant_identity")
        if row["authority"] > state["caller_ceiling"] or row["epoch"] != state["epoch"]:
            errors.append("authority_amplification_or_stale_epoch")
        if row["time"] > row["expires"] or row["uses"] <= 0:
            errors.append("expired_or_consumed_grant")
        if not row["owner"] or not row["approval"]:
            errors.append("missing_target_owner_approval")
    elif kind == "approve":
        if state["grant"] != exact or row["grant_id"] in state["revoked"]:
            errors.append("approval_binding_mismatch")
        if row["epoch"] != state["epoch"] or row["time"] > row["expires"] or row["uses"] <= 0:
            errors.append("stale_expired_or_consumed_approval")
        if not row["owner"] or not row["approval"]:
            errors.append("missing_approval_receipt")
    elif kind == "dispatch":
        if state["grant"] != exact or state["approved"] != row["grant_id"]:
            errors.append("dispatch_binding_mismatch")
        if row["grant_id"] in state["revoked"] or row["epoch"] != state["epoch"] or row["time"] > row["expires"] or row["uses"] <= 0:
            errors.append("stale_expired_revoked_or_consumed_dispatch")
        if not row["dispatch_receipt"]:
            errors.append("missing_dispatch_receipt")
    elif kind == "effect":
        if state["grant"] != exact or state["approved"] != row["grant_id"] or state["dispatched"] != row["grant_id"]:
            errors.append("effect_binding_or_handoff_mismatch")
        if row["grant_id"] in state["revoked"] or row["epoch"] != state["epoch"] or row["time"] > row["expires"] or row["uses"] <= 0:
            errors.append("stale_expired_revoked_or_consumed_effect")
        if not row["effect_receipt"]:
            errors.append("missing_effect_receipt")
    elif kind == "observe":
        if state["observed"] >= state["effects"] or not row["observer"] or not row["effect_receipt"]:
            errors.append("invalid_or_nonindependent_observation")
    elif kind == "revoke":
        if state["grant"] != exact or not row["revocation_receipt"]:
            errors.append("invalid_revocation")
    elif kind == "rollback":
        if state["effects"] <= 0 or state["observed"] != state["effects"] or not row["rollback_exact"] or not row["effect_receipt"]:
            errors.append("inexact_or_unobserved_rollback")
    else:
        errors.append("unknown_event")
    return errors


def apply_event(state: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    state = copy.deepcopy(state)
    state["time"] = row["time"]
    kind = row["kind"]
    if kind == "issue":
        state["grant"] = grant(row)
    elif kind == "approve":
        state["approved"] = row["grant_id"]
    elif kind == "dispatch":
        state["dispatched"] = row["grant_id"]
    elif kind == "effect":
        state["grant"]["uses"] -= 1
        state["approved"] = None
        state["dispatched"] = None
        state["effects"] += 1
    elif kind == "observe":
        state["observed"] += 1
    elif kind == "revoke":
        state["revoked"].append(row["grant_id"])
        state["epoch"] += 1
        state["grant"] = state["approved"] = state["dispatched"] = None
    elif kind == "rollback":
        state["effects"] = state["observed"] = 0
        state["rolled_back"] = True
    return state


def state_invariant_errors(state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if state["observed"] > state["effects"]:
        errors.append("observation_exceeds_material_effects")
    active = state["grant"]
    if active is not None:
        if active["authority"] > state["caller_ceiling"]:
            errors.append("live_grant_exceeds_caller_ceiling")
        if active["epoch"] != state["epoch"] or active["grant_id"] in state["revoked"]:
            errors.append("live_grant_is_stale_or_revoked")
    if state["approved"] is not None and (active is None or state["approved"] != active["grant_id"]):
        errors.append("approval_not_bound_to_live_grant")
    if state["dispatched"] is not None and (
        active is None
        or state["approved"] != state["dispatched"]
        or state["dispatched"] != active["grant_id"]
    ):
        errors.append("dispatch_not_bound_to_approval_and_live_grant")
    return errors


def run(rows: list[dict[str, Any]], start: dict[str, Any] | None = None) -> tuple[bool, int | None, list[str], dict[str, Any]]:
    state = copy.deepcopy(start) if start is not None else initial()
    initial_errors = state_invariant_errors(state)
    if initial_errors:
        return False, 0, initial_errors, state
    for index, row in enumerate(rows):
        errors = event_errors(state, row)
        if errors:
            return False, index, errors, state
        state = apply_event(state, row)
        errors = state_invariant_errors(state)
        if errors:
            return False, index, errors, state
    return True, None, [], state


def audit_scenario(scenario_id: str, rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    accepted, _, reasons, final_state = run(rows)
    if not accepted:
        errors.append(f"{scenario_id}: rejected: {reasons}")
    prefix_checks = 0
    for end in range(1, len(rows) + 1):
        prefix_accepted, _, prefix_reasons, _ = run(rows[:end])
        prefix_checks += 1
        if not prefix_accepted:
            errors.append(f"{scenario_id}: prefix {end} rejected: {prefix_reasons}")
    composition_checks = 0
    for split in range(len(rows) + 1):
        left_accepted, _, left_reasons, middle = run(rows[:split])
        right_accepted, _, right_reasons, composed = run(rows[split:], middle)
        composition_checks += 1
        if not left_accepted or not right_accepted or composed != final_state:
            errors.append(
                f"{scenario_id}: composition split {split} drift: "
                f"{left_reasons + right_reasons}"
            )
    return {
        "scenario_id": scenario_id,
        "event_count": len(rows),
        "accepted": accepted,
        "prefix_invariant_check_count": prefix_checks,
        "composition_check_count": composition_checks,
        "final_state": final_state,
    }, errors


def authority_fixture_errors(row: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    decision = row.get("decision")
    permission = row.get("permission_class")
    caller = RANK.get(row.get("caller_ceiling"), -1)
    active = RANK.get(row.get("authority_ceiling"), -1)
    target = RANK.get(row.get("target_required_authority"), -1)
    if permission not in MINIMUM or target < MINIMUM.get(permission, 99):
        errors.append("permission_class_collapse")
    if not row.get("audit_refs") or not row.get("non_claims"):
        errors.append("missing_custody_boundary")
    if decision == "allow":
        if row.get("grant_lifecycle_state") not in {"granted", "used", "receipted"}:
            errors.append("inactive_grant")
        if target > active or active > caller:
            errors.append("authority_widening")
        if not str(row.get("effect_receipt", "")).startswith("receipt://"):
            errors.append("missing_effect_receipt")
    elif decision == "deny":
        if row.get("grant_lifecycle_state") != "denied" or not row.get("denial_reason") or row.get("effect_receipt"):
            errors.append("invalid_denial")
    elif decision == "escalate":
        chain = " ".join(row.get("delegation_chain", [])).lower()
        if row.get("grant_lifecycle_state") not in {"requested", "delegated"} or row.get("effect_receipt") or not row.get("denial_reason") or not any(word in chain for word in ("review", "approval")):
            errors.append("invalid_escalation")
    else:
        errors.append("unknown_decision")
    return errors


def mutation_cases(base: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    cases: list[tuple[str, list[dict[str, Any]]]] = []
    def mutate(name: str, index: int, key: str, value: Any) -> None:
        rows = copy.deepcopy(base)
        rows[index][key] = value
        cases.append((name, rows))
    for key, value in (("grant_id", 0), ("authority", 4), ("epoch", 10), ("expires", 0), ("uses", 0), ("owner", False), ("approval", False), ("time", 0)):
        mutate(f"issue_{key}", 0, key, value)
    for key, value in (("principal", 999), ("operation", 999), ("target", 999), ("authority", 2), ("epoch", 10), ("expires", 1), ("uses", 0), ("owner", False), ("approval", False)):
        mutate(f"approve_{key}", 1, key, value)
    for key, value in (("principal", 999), ("operation", 999), ("target", 999), ("authority", 2), ("epoch", 10), ("expires", 2), ("uses", 0), ("dispatch_receipt", False)):
        mutate(f"dispatch_{key}", 2, key, value)
    for key, value in (("principal", 999), ("operation", 999), ("target", 999), ("epoch", 10), ("expires", 3), ("uses", 0), ("effect_receipt", False)):
        mutate(f"effect_{key}", 3, key, value)
    mutate("observe_nonindependent", 4, "observer", False)
    mutate("observe_missing_receipt", 4, "effect_receipt", False)
    mutate("rollback_inexact", 5, "rollback_exact", False)
    mutate("rollback_missing_receipt", 5, "effect_receipt", False)
    revoked = copy.deepcopy(base[:2]) + [event("revoke", 3), event("dispatch", 4)]
    cases.append(("dispatch_after_revocation", revoked))
    consumed = copy.deepcopy(base[:4]) + [event("effect", 5)]
    consumed[-1]["uses"] = 0
    cases.append(("second_effect_after_one_shot_consumption", consumed))
    revoke_base = copy.deepcopy(base[:2]) + [event("revoke", 3)]
    for key, value in (("principal", 999), ("operation", 999), ("target", 999), ("authority", 2), ("epoch", 10), ("expires", 2), ("uses", 0), ("revocation_receipt", False)):
        rows = copy.deepcopy(revoke_base)
        rows[2][key] = value
        cases.append((f"revoke_{key}", rows))
    effect_after_revoke = copy.deepcopy(revoke_base) + [event("effect", 4)]
    cases.append(("effect_after_revocation", effect_after_revoke))
    reissue_after_revoke = copy.deepcopy(revoke_base) + [event("issue", 4)]
    reissue_after_revoke[-1]["epoch"] = 12
    cases.append(("reissue_same_id_after_revocation", reissue_after_revoke))
    observe_overcount = copy.deepcopy(base[:5]) + [event("observe", 6)]
    cases.append(("observation_exceeds_material_effects", observe_overcount))
    rollback_unobserved = copy.deepcopy(base[:4]) + [event("rollback", 5)]
    cases.append(("rollback_before_independent_observation", rollback_unobserved))
    return cases


def build() -> tuple[dict[str, Any], list[str]]:
    errors: list[str] = []
    runtime = load(RUNTIME)
    revocation = load(REVOCATION)
    governed = load(GOVERNED)
    jsonschema.Draft202012Validator(load(GOVERNED_SCHEMA)).validate(governed)

    fixtures = []
    for path in sorted(AUTHORITY_FIXTURES.glob("*.json")):
        reasons = authority_fixture_errors(load(path))
        expected = not path.name.startswith("invalid_")
        accepted = not reasons
        if accepted != expected:
            errors.append(f"{path.name}: fixture disposition mismatch")
        fixtures.append({"fixture": path.name, "expected_accept": expected, "accepted": accepted, "reasons": reasons, "sha256": sha(path)})

    if runtime.get("pass") is not True or runtime.get("support_state_effect") != "none":
        errors.append("runtime effect evidence drift")
    valid_runtime = runtime.get("valid_scenario", {})
    invalid_runtime = runtime.get("expected_invalid_controls", [])
    if not valid_runtime.get("effect_executed") or not valid_runtime.get("checks", {}).get("rollback_exact"):
        errors.append("runtime effect/rollback is no longer exact")
    if len(invalid_runtime) != 2 or not all(row.get("checks", {}).get("blocked_before_mutation") and row.get("checks", {}).get("state_unchanged") for row in invalid_runtime):
        errors.append("runtime denial evidence drift")
    if revocation.get("trace_entry_count") != 5 or revocation.get("support_state_effect") != "none":
        errors.append("revocation trace drift")
    summary = governed.get("governed_summary", {})
    if governed.get("scenario_count") != 9 or summary.get("unsafe_releases") != 0 or summary.get("releases") != 3:
        errors.append("governed repository evidence drift")

    base = [event("issue", 1), event("approve", 2), event("dispatch", 3), event("effect", 4), event("observe", 5), event("rollback", 6)]
    two_use = [event("issue", 1), event("approve", 2), event("dispatch", 3), event("effect", 4), event("approve", 5), event("dispatch", 6), event("effect", 7), event("observe", 8), event("observe", 9), event("rollback", 10)]
    for row in two_use[:4]:
        row["uses"] = 2
    for row in two_use[4:7]:
        row["uses"] = 1
    for row in two_use[7:]:
        row["uses"] = 0
    revocation_scenario = [event("issue", 1), event("approve", 2), event("dispatch", 3), event("revoke", 4)]
    scenario_receipts = []
    for scenario_id, rows in (
        ("one_use_observe_rollback", base),
        ("two_use_two_observations_rollback", two_use),
        ("dispatch_then_revoke", revocation_scenario),
    ):
        receipt, scenario_errors = audit_scenario(scenario_id, rows)
        scenario_receipts.append(receipt)
        errors.extend(scenario_errors)
    final_state = scenario_receipts[0]["final_state"]
    if not final_state["rolled_back"]:
        errors.append("reference authority trace did not roll back")
    two_use_final = scenario_receipts[1]["final_state"]
    if not two_use_final["rolled_back"] or two_use_final["grant"]["uses"] != 0:
        errors.append("two-use trace did not consume both uses and roll back")
    revoked_final = scenario_receipts[2]["final_state"]
    if revoked_final["grant"] is not None or revoked_final["approved"] is not None or revoked_final["dispatched"] is not None or revoked_final["epoch"] != 12 or revoked_final["revoked"] != [71]:
        errors.append("revocation trace did not close custody and advance the epoch")
    mutation_receipts = []
    rejection_noninterference_count = 0
    for mutation_id, rows in mutation_cases(base):
        accepted_mutation, failed_index, mutation_errors, rejected_state = run(rows)
        noninterfering = False
        if failed_index is not None:
            prefix_accepted, _, _, prefix_state = run(rows[:failed_index])
            noninterfering = prefix_accepted and rejected_state == prefix_state
        if noninterfering:
            rejection_noninterference_count += 1
        mutation_receipts.append({"mutation_id": mutation_id, "rejected": not accepted_mutation, "failed_event_index": failed_index, "state_noninterfering": noninterfering, "reasons": mutation_errors})
        if accepted_mutation:
            errors.append(f"{mutation_id}: mutation accepted")
        if not noninterfering:
            errors.append(f"{mutation_id}: rejection changed state")

    result = {
        "schema_version": "asi_stack.authority_effect_refinement.v1",
        "result_id": "authority-effect-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha(LEAN), "runtime_effect": sha(RUNTIME), "revocation_trace": sha(REVOCATION), "governed_repository": sha(GOVERNED)},
        "authority_fixture_count": len(fixtures),
        "authority_fixture_accepted_count": sum(row["accepted"] for row in fixtures),
        "authority_fixture_rejected_count": sum(not row["accepted"] for row in fixtures),
        "reachable_trace_event_count": len(base),
        "reachable_scenario_count": len(scenario_receipts),
        "reachable_scenario_event_count": sum(row["event_count"] for row in scenario_receipts),
        "invariant_prefix_check_count": sum(row["prefix_invariant_check_count"] for row in scenario_receipts),
        "composition_check_count": sum(row["composition_check_count"] for row in scenario_receipts),
        "executed_local_effect_count": 1,
        "independently_observed_effect_count": 1,
        "exact_rollback_count": 1,
        "pre_effect_denial_count": len(invalid_runtime),
        "revocation_trace_entry_count": revocation["trace_entry_count"],
        "governed_scenario_count": governed["scenario_count"],
        "governed_release_count": summary["releases"],
        "governed_unsafe_release_count": summary["unsafe_releases"],
        "mutation_count": len(mutation_receipts),
        "mutation_rejection_count": sum(row["rejected"] for row in mutation_receipts),
        "rejection_noninterference_count": rejection_noninterference_count,
        "reference_trace_final_state": final_state,
        "scenario_receipts": scenario_receipts,
        "authority_fixture_receipts": fixtures,
        "mutation_receipts": mutation_receipts,
        "support_state_effect": "none",
        "non_claims": [
            "The reachable model uses abstract numeric identities and trusted receipts; it does not prove identity, approval, receipt, observer, or revocation authenticity.",
            "The executed effect is a generated local temporary-file mutation, and the governed repository workload is bounded; neither establishes deployed authorization middleware or production security.",
            "The packet does not establish natural-language authority extraction, complete effect observation, concurrent or distributed revocation safety, reproduction, transfer, safety, or chapter-core support.",
        ],
    }
    try:
        jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc:
        errors.append(f"schema: {exc.message}")
    return result, errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result, errors = build()
    if errors:
        raise SystemExit("Authority effect refinement failed:\n - " + "\n - ".join(errors))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result:
        raise SystemExit("Authority effect refinement result stale; run with --write")
    print(f"Authority effect refinement passed: {result['authority_fixture_count']} fixtures, {result['reachable_scenario_count']} reachable traces/{result['reachable_scenario_event_count']} events, {result['invariant_prefix_check_count']} invariant prefixes, {result['composition_check_count']} batch compositions, {result['mutation_rejection_count']} state-noninterfering mutation rejections, support effect none.")


if __name__ == "__main__":
    main()

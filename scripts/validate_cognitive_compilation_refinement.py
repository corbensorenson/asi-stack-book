#!/usr/bin/env python3
"""Independently consume the reachable Cognitive Compilation refinement."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/CognitiveCompilationRefinement.lean"
ATOM_SCHEMA = ROOT / "schemas/semantic_atom.schema.json"
FIXTURES = ROOT / "experiments/cognitive_compilation_traces/fixtures"
PRIOR_RESULT = ROOT / "experiments/cognitive_compilation_traces/results/2026-07-02-local.md"
SCHEMA = ROOT / "schemas/cognitive_compilation_refinement.schema.json"
RESULT = ROOT / "experiments/cognitive_compilation_refinement/results/2026-07-15-local.json"
IDENTITY = ("plan_id", "obligation_one", "obligation_two", "obligation_three", "constraint_hash")


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inventory_sha(paths: list[Path]) -> str:
    body = "\n".join(f"{path.name}:{sha(path)}" for path in paths) + "\n"
    return hashlib.sha256(body.encode()).hexdigest()


def initial() -> dict[str, Any]:
    return {"stage": "raw", "plan_id": 0, "plan_version": 1,
            "obligation_one": 0, "obligation_two": 0, "obligation_three": 0,
            "constraint_hash": 0, "target_hash": 0, "authority_ceiling": 3,
            "approved_authority": 0, "ledger_version": 1,
            "lowering_receipt": False, "validation_receipt": False,
            "repair_receipt": False, "residual_count": 0, "logical_time": 0}


def event(kind: str, source: str, target: str, time: int) -> dict[str, Any]:
    return {"kind": kind, "from_stage": source, "to_stage": target,
            "plan_id": 101, "input_plan_version": 1, "output_plan_version": 1,
            "obligation_one": 501, "obligation_two": 502, "obligation_three": 503,
            "constraint_hash": 601, "target_hash": 701, "requested_authority": 3,
            "obligations_preserved": True, "lowering_receipt": False,
            "validation_receipt": False, "repair_invalidates_obligation": False,
            "repair_localized": False, "before_obligation_hash": 503,
            "after_obligation_hash": 503, "input_ledger_version": 1,
            "output_ledger_version": 1, "ledger_update_receipt": False,
            "residual_count": 0, "block_receipt": False, "logical_time": time}


def trace() -> list[dict[str, Any]]:
    rows = [event("bind_source", "raw", "source_bound", 1),
            event("type_ir", "source_bound", "ir_typed", 2),
            event("lower_target", "ir_typed", "lowered", 3),
            event("validate_target", "lowered", "validated", 4),
            event("detect_repair", "validated", "repair_required", 5),
            event("apply_repair", "repair_required", "validated", 6),
            event("accept_target", "validated", "accepted", 7)]
    rows[2]["lowering_receipt"] = True
    rows[3]["validation_receipt"] = True
    rows[4]["repair_invalidates_obligation"] = True
    rows[5].update(repair_localized=True, output_ledger_version=2, ledger_update_receipt=True)
    rows[6]["input_ledger_version"] = 2
    return rows


def source_matches(state: dict[str, Any], row: dict[str, Any]) -> bool:
    return all(row[key] == state[key] for key in IDENTITY)


def errors(state: dict[str, Any], row: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if state["stage"] != row["from_stage"]: out.append("stage_mismatch")
    if state["plan_version"] != row["input_plan_version"]: out.append("version_mismatch")
    if state["logical_time"] >= row["logical_time"]: out.append("time_not_monotonic")
    kind = row["kind"]
    if kind == "bind_source":
        if (row["from_stage"], row["to_stage"]) != ("raw", "source_bound"): out.append("bind_stage")
        if any(row[key] <= 0 for key in IDENTITY): out.append("missing_source_identity")
        if row["requested_authority"] > state["authority_ceiling"]: out.append("authority_widened")
    elif kind == "type_ir":
        if (row["from_stage"], row["to_stage"]) != ("source_bound", "ir_typed"): out.append("type_stage")
        if not source_matches(state, row): out.append("source_substitution")
        if row["requested_authority"] != state["approved_authority"]: out.append("authority_changed")
    elif kind == "lower_target":
        if (row["from_stage"], row["to_stage"]) != ("ir_typed", "lowered"): out.append("lower_stage")
        if not source_matches(state, row): out.append("source_substitution")
        if row["target_hash"] <= 0: out.append("target_missing")
        if row["requested_authority"] != state["approved_authority"]: out.append("authority_changed")
        if not row["obligations_preserved"]: out.append("obligation_loss")
        if not row["lowering_receipt"]: out.append("lowering_receipt_missing")
    elif kind == "validate_target":
        if (row["from_stage"], row["to_stage"]) != ("lowered", "validated"): out.append("validation_stage")
        if not source_matches(state, row) or row["target_hash"] != state["target_hash"]: out.append("target_or_source_substitution")
        if not row["obligations_preserved"]: out.append("obligation_check_missing")
        if not state["lowering_receipt"]: out.append("prior_lowering_receipt_missing")
        if not row["validation_receipt"]: out.append("validation_receipt_missing")
    elif kind == "detect_repair":
        if (row["from_stage"], row["to_stage"]) != ("validated", "repair_required"): out.append("repair_detection_stage")
        if not source_matches(state, row) or row["target_hash"] != state["target_hash"]: out.append("target_or_source_substitution")
        if not row["repair_invalidates_obligation"]: out.append("no_material_repair_delta")
        if row["input_ledger_version"] != state["ledger_version"]: out.append("ledger_version_mismatch")
    elif kind == "apply_repair":
        if (row["from_stage"], row["to_stage"]) != ("repair_required", "validated"): out.append("repair_stage")
        if not source_matches(state, row) or row["target_hash"] != state["target_hash"]: out.append("target_or_source_substitution")
        if not row["repair_localized"]: out.append("repair_not_localized")
        if row["before_obligation_hash"] != row["after_obligation_hash"] or row["before_obligation_hash"] != state["obligation_three"]: out.append("repair_obligation_changed")
        if row["input_ledger_version"] != state["ledger_version"]: out.append("ledger_input_mismatch")
        if row["output_ledger_version"] != state["ledger_version"] + 1: out.append("ledger_not_incremented")
        if not row["ledger_update_receipt"]: out.append("ledger_receipt_missing")
        if not row["obligations_preserved"]: out.append("repair_obligation_loss")
    elif kind == "accept_target":
        if (row["from_stage"], row["to_stage"]) != ("validated", "accepted"): out.append("accept_stage")
        if not source_matches(state, row) or row["target_hash"] != state["target_hash"]: out.append("target_or_source_substitution")
        if not state["lowering_receipt"] or not state["validation_receipt"]: out.append("receipt_custody_missing")
        if not row["obligations_preserved"]: out.append("obligation_loss")
        if row["residual_count"] != 0: out.append("open_residual")
        if row["requested_authority"] != state["approved_authority"]: out.append("authority_changed")
    elif kind == "block":
        if row["to_stage"] != "blocked" or not row["block_receipt"]: out.append("invalid_block")
    else: out.append("unknown_event")
    return out


def apply(state: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    nxt = copy.deepcopy(state); nxt["stage"] = row["to_stage"]
    nxt["plan_version"] = row["output_plan_version"]
    if row["kind"] == "bind_source":
        for key in IDENTITY: nxt[key] = row[key]
        nxt["approved_authority"] = row["requested_authority"]
    if row["kind"] == "lower_target": nxt["target_hash"] = row["target_hash"]
    if row["kind"] == "apply_repair": nxt["ledger_version"] = row["output_ledger_version"]
    nxt["lowering_receipt"] |= row["lowering_receipt"]
    nxt["validation_receipt"] |= row["validation_receipt"]
    nxt["repair_receipt"] |= row["ledger_update_receipt"]
    nxt["residual_count"] = row["residual_count"]; nxt["logical_time"] = row["logical_time"]
    return nxt


def run(rows: list[dict[str, Any]]) -> tuple[bool, int | None, list[str], dict[str, Any]]:
    state = initial()
    for index, row in enumerate(rows):
        found = errors(state, row)
        if found: return False, index, found, state
        state = apply(state, row)
    return True, None, [], state


def mutations(base: list[dict[str, Any]]) -> list[tuple[str, list[dict[str, Any]]]]:
    out: list[tuple[str, list[dict[str, Any]]]] = []
    def m(name: str, index: int, key: str, value: Any) -> None:
        rows = copy.deepcopy(base); rows[index][key] = value; out.append((name, rows))
    for key in IDENTITY: m("bind_" + key + "_missing", 0, key, 0)
    m("bind_authority_widened", 0, "requested_authority", 4); m("bind_time", 0, "logical_time", 0)
    for key in IDENTITY: m("type_" + key + "_substitution", 1, key, 999)
    m("type_authority_changed", 1, "requested_authority", 2); m("type_time", 1, "logical_time", 1)
    for key in IDENTITY: m("lower_" + key + "_substitution", 2, key, 999)
    for name, key, value in [("target_missing", "target_hash", 0), ("authority_changed", "requested_authority", 2), ("obligation_loss", "obligations_preserved", False), ("receipt_missing", "lowering_receipt", False)]: m("lower_" + name, 2, key, value)
    for key in (*IDENTITY, "target_hash"): m("validate_" + key + "_substitution", 3, key, 999)
    m("validate_obligation_laundering", 3, "obligations_preserved", False); m("validate_receipt_missing", 3, "validation_receipt", False)
    m("detect_target_substitution", 4, "target_hash", 999); m("detect_no_delta", 4, "repair_invalidates_obligation", False); m("detect_ledger_mismatch", 4, "input_ledger_version", 2)
    for name, key, value in [("target_substitution", "target_hash", 999), ("global", "repair_localized", False), ("before_after", "after_obligation_hash", 999), ("wrong_obligation", "before_obligation_hash", 999), ("ledger_input", "input_ledger_version", 2), ("ledger_increment", "output_ledger_version", 1), ("receipt", "ledger_update_receipt", False), ("obligation_loss", "obligations_preserved", False)]: m("repair_" + name, 5, key, value)
    for name, key, value in [("target_substitution", "target_hash", 999), ("obligation_loss", "obligations_preserved", False), ("residual", "residual_count", 1), ("authority", "requested_authority", 2), ("time", "logical_time", 6)]: m("accept_" + name, 6, key, value)
    return out


def fixture_check(path: Path, value: dict[str, Any], atom_schema: dict[str, Any]) -> tuple[bool, str]:
    for atom in value.get("semantic_atoms", []): jsonschema.Draft202012Validator(atom_schema).validate(atom)
    requirements = set(value["source_plan"]["requirements"])
    atom_obligations = {item for atom in value["semantic_atoms"] for item in atom["obligation_refs"]}
    receipt_ids = {row["receipt_id"] for row in value["lowering_receipts"]}
    atom_receipts = {atom["lowering_receipt"] for atom in value["semantic_atoms"]}
    preserved = {item for row in value["lowering_receipts"] for item in row["preserved_obligations"]}
    audit_ok = value["target_audit"]["validator_status"] == "passed" and value["target_audit"]["obligation_preservation"] == "all_required_obligations_preserved"
    repair = value["repair_trace"]; local = repair["repair_scope"] == "same_atom" and set(repair["changed_atoms"]) == {repair["failed_atom_ref"]}
    obligations_ok = requirements <= atom_obligations and requirements <= preserved and set(repair["before_obligations"]) == set(repair["after_obligations"])
    receipts_ok = atom_receipts <= receipt_ids
    accepted = obligations_ok and receipts_ok and audit_ok and local and bool(repair["ledger_update_ref"])
    failed = []
    if not obligations_ok: failed.append("obligation_preservation")
    if not receipts_ok: failed.append("receipt_identity")
    if not audit_ok: failed.append("target_audit")
    if not local: failed.append("repair_locality")
    return accepted, ",".join(failed) or "bounded_fixture_acceptance"


def build() -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []; paths = sorted(FIXTURES.glob("*.json")); atom_schema = load(ATOM_SCHEMA)
    receipts = []
    for path in paths:
        try: accepted, reason = fixture_check(path, load(path), atom_schema)
        except (KeyError, jsonschema.ValidationError) as exc: accepted, reason = False, "schema_or_shape:" + str(exc)
        expected = path.name.startswith("valid_")
        if accepted != expected: issues.append(path.name + ": independent classification drift")
        receipts.append({"fixture": path.name, "expected_acceptance": expected, "independently_accepted": accepted, "reason": reason})
    if len(paths) != 6 or sum(row["independently_accepted"] for row in receipts) != 2: issues.append("fixture inventory/count drift")
    prior = PRIOR_RESULT.read_text(encoding="utf-8")
    if "2 valid fixture(s), 4 expected-invalid fixture(s)" not in prior: issues.append("prior result drift")
    base = trace(); accepted, _, _, final = run(base)
    if not accepted or final["stage"] != "accepted" or final["ledger_version"] != 2: issues.append("reference trace rejected")
    mutation_receipts = []
    for mid, rows in mutations(base):
        ok, index, why, _ = run(rows); mutation_receipts.append({"mutation_id": mid, "rejected": not ok, "failed_event_index": index, "reasons": why})
        if ok: issues.append(mid + ": mutation accepted")
    result = {"schema_version": "asi_stack.cognitive_compilation_refinement.v1", "result_id": "cognitive-compilation-refinement-2026-07-15-local",
              "source_sha256": {"lean_model": sha(LEAN), "semantic_atom_schema": sha(ATOM_SCHEMA), "fixture_inventory": inventory_sha(paths), "prior_result": sha(PRIOR_RESULT)},
              "fixture_count": len(paths), "accepted_fixture_count": sum(row["independently_accepted"] for row in receipts), "rejected_fixture_count": sum(not row["independently_accepted"] for row in receipts), "fixture_receipts": receipts,
              "reachable_trace_event_count": len(base), "reference_trace_final_state": final,
              "mutation_count": len(mutation_receipts), "mutation_rejection_count": sum(row["rejected"] for row in mutation_receipts), "mutation_receipts": mutation_receipts,
              "support_state_effect": "none", "non_claims": ["Abstract numeric identities establish equality only, not natural-language semantic equivalence or obligation completeness.", "Fixture labels, authority, scope, validator, receipt, and ledger fields are trusted bounded inputs.", "This packet does not establish a source parser, target backend, independent semantic evaluator, compiled behavior, measured repair locality, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support."]}
    try: jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc: issues.append("result schema: " + exc.message)
    return result, issues


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    result, issues = build()
    if issues: raise SystemExit("Cognitive compilation refinement failed:\n - " + "\n - ".join(issues))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result: raise SystemExit("Cognitive compilation refinement result stale; run --write")
    print(f"Cognitive compilation refinement passed: {result['accepted_fixture_count']} accepted/{result['rejected_fixture_count']} rejected fixtures, {result['reachable_trace_event_count']} events, {result['mutation_rejection_count']} mutations rejected, support effect none.")


if __name__ == "__main__": main()

#!/usr/bin/env python3
"""Independently consume the reachable Context Certificate refinement."""
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
LEAN = ROOT / "lean/AsiStackProofs/ContextCertificateRefinement.lean"
CERT_SCHEMA = ROOT / "schemas/semantic_page_certificate.schema.json"
PROTOCOL_FIXTURE = ROOT / "tests/fixtures/protocol_records/semantic_page_certificate.valid.json"
SCENARIO_DIR = ROOT / "experiments/context_admission_adequacy/fixtures"
ADMISSION_VALIDATOR = ROOT / "scripts/validate_context_admission_adequacy.py"
SCHEMA = ROOT / "schemas/context_certificate_refinement.schema.json"
RESULT = ROOT / "experiments/context_certificate_refinement/results/2026-07-15-local.json"


def load(path: Path) -> Any: return json.loads(path.read_text(encoding="utf-8"))
def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()
def inventory_sha(paths: list[Path]) -> str:
    return hashlib.sha256(("\n".join(f"{p.name}:{sha(p)}" for p in paths) + "\n").encode()).hexdigest()


def initial() -> dict[str, Any]:
    return {"stage":"raw", "certificate_id":0, "source_id":0, "source_authority":0,
            "derived_id":0, "derived_authority":0, "loss_contract_id":0,
            "omission_ledger_id":0, "permitted_use_id":0, "lifecycle_epoch":0,
            "source_binding_receipt":False, "certificate_receipt":False,
            "verification_receipt":False, "deletion_closure_required":False,
            "deletion_closure_receipt":False, "evidence_transition_required":False,
            "evidence_transition_receipt":False, "revoked":False, "tainted":False,
            "admitted":False, "logical_time":0}


def event(kind: str, source: str, target: str, time: int) -> dict[str, Any]:
    return {"kind":kind, "from_stage":source, "to_stage":target,
            "certificate_id":101, "source_id":201, "source_authority":3,
            "derived_id":301, "derived_authority":2, "loss_contract_id":401,
            "omission_ledger_id":501, "permitted_use_id":601, "requested_use_id":601,
            "lifecycle_epoch":1, "well_formed":True, "derived_representation":True,
            "source_bindings_declared":True, "loss_contract_declared":True,
            "omissions_declared":True, "permitted_uses_declared":True,
            "source_binding_receipt":False, "certificate_receipt":False,
            "verifier_references_declared":True, "verification_passed":True,
            "verification_receipt":False, "deletion_closure_required":True,
            "deletion_closure_receipt":False, "support_promotion_requested":False,
            "evidence_transition_receipt":False, "revoked":False,
            "revocation_receipt":False, "tainted":False, "admitted":False,
            "logical_time":time}


def trace() -> list[dict[str, Any]]:
    rows = [event("bind_source", "raw", "source_bound", 1),
            event("derive_cell", "source_bound", "derived", 2),
            event("certify_cell", "derived", "certified", 3),
            event("verify_cell", "certified", "verified", 4),
            event("admit_use", "verified", "admitted", 5)]
    rows[1]["source_binding_receipt"] = True
    rows[2]["certificate_receipt"] = True
    rows[3].update(verification_receipt=True, deletion_closure_receipt=True)
    rows[4]["admitted"] = True
    return rows


def cert_matches(state: dict[str, Any], row: dict[str, Any]) -> bool:
    return all(row[k] == state[k] for k in ("certificate_id", "source_id", "source_authority"))


def derived_matches(state: dict[str, Any], row: dict[str, Any]) -> bool:
    return cert_matches(state, row) and all(row[k] == state[k] for k in ("derived_id", "derived_authority"))


def contract_matches(state: dict[str, Any], row: dict[str, Any]) -> bool:
    return derived_matches(state, row) and all(row[k] == state[k] for k in ("loss_contract_id", "omission_ledger_id", "permitted_use_id", "lifecycle_epoch"))


def errors(state: dict[str, Any], row: dict[str, Any]) -> list[str]:
    out: list[str] = []
    if state["stage"] != row["from_stage"]: out.append("stage_mismatch")
    if state["logical_time"] >= row["logical_time"]: out.append("time_not_monotonic")
    kind = row["kind"]
    if kind == "bind_source":
        if (row["from_stage"], row["to_stage"]) != ("raw", "source_bound"): out.append("bind_stage")
        if not row["well_formed"]: out.append("malformed")
        if row["certificate_id"] <= 0 or row["source_id"] <= 0: out.append("source_identity_missing")
        if row["source_authority"] > 4: out.append("source_authority_over_ceiling")
        if row["lifecycle_epoch"] <= 0: out.append("epoch_missing")
        if row["revoked"] or row["tainted"]: out.append("blocked_source")
    elif kind == "derive_cell":
        if (row["from_stage"], row["to_stage"]) != ("source_bound", "derived"): out.append("derive_stage")
        if not cert_matches(state, row): out.append("source_substitution")
        if not row["derived_representation"]: out.append("not_derived")
        if not row["source_bindings_declared"]: out.append("source_bindings_missing")
        if row["derived_id"] <= 0: out.append("derived_identity_missing")
        if row["derived_authority"] > state["source_authority"]: out.append("authority_escalation")
        if not row["source_binding_receipt"]: out.append("source_binding_receipt_missing")
        if row["revoked"] or row["tainted"]: out.append("blocked_derivation")
    elif kind == "certify_cell":
        if (row["from_stage"], row["to_stage"]) != ("derived", "certified"): out.append("certify_stage")
        if not derived_matches(state, row): out.append("derived_substitution")
        if not row["loss_contract_declared"]: out.append("loss_contract_missing")
        if not row["omissions_declared"]: out.append("omission_ledger_missing")
        if not row["permitted_uses_declared"]: out.append("permitted_use_missing")
        if any(row[k] <= 0 for k in ("loss_contract_id", "omission_ledger_id", "permitted_use_id")): out.append("contract_identity_missing")
        if row["lifecycle_epoch"] != state["lifecycle_epoch"]: out.append("stale_epoch")
        if not row["certificate_receipt"]: out.append("certificate_receipt_missing")
        if row["revoked"] or row["tainted"]: out.append("blocked_certificate")
    elif kind == "verify_cell":
        if (row["from_stage"], row["to_stage"]) != ("certified", "verified"): out.append("verify_stage")
        if not contract_matches(state, row): out.append("contract_substitution")
        if not row["verifier_references_declared"]: out.append("verifier_refs_missing")
        if not row["verification_passed"]: out.append("verification_failed")
        if not row["verification_receipt"]: out.append("verification_receipt_missing")
        if row["deletion_closure_required"] != state["deletion_closure_required"]: out.append("deletion_requirement_substitution")
        if row["deletion_closure_required"] and not row["deletion_closure_receipt"]: out.append("deletion_closure_missing")
        if row["revoked"] or row["tainted"]: out.append("blocked_verification")
    elif kind == "admit_use":
        if (row["from_stage"], row["to_stage"]) != ("verified", "admitted"): out.append("admit_stage")
        if not contract_matches(state, row): out.append("contract_substitution")
        if row["requested_use_id"] != state["permitted_use_id"]: out.append("consumer_scope_mismatch")
        if not state["source_binding_receipt"] or not state["certificate_receipt"] or not state["verification_receipt"]: out.append("receipt_custody_missing")
        if state["deletion_closure_required"] and not state["deletion_closure_receipt"]: out.append("deletion_closure_missing")
        if row["support_promotion_requested"] and not row["evidence_transition_receipt"]: out.append("support_promotion_laundering")
        if state["revoked"] or state["tainted"]: out.append("blocked_admission")
        if not row["admitted"]: out.append("admission_receipt_missing")
    else: out.append("unknown_event")
    return out


def apply(state: dict[str, Any], row: dict[str, Any]) -> dict[str, Any]:
    nxt = copy.deepcopy(state); nxt["stage"] = row["to_stage"]
    if row["kind"] == "bind_source":
        for key in ("certificate_id", "source_id", "source_authority", "lifecycle_epoch"): nxt[key] = row[key]
    if row["kind"] == "derive_cell":
        for key in ("derived_id", "derived_authority"): nxt[key] = row[key]
    if row["kind"] == "certify_cell":
        for key in ("loss_contract_id", "omission_ledger_id", "permitted_use_id", "deletion_closure_required"): nxt[key] = row[key]
    for key in ("source_binding_receipt", "certificate_receipt", "verification_receipt", "deletion_closure_receipt", "evidence_transition_receipt", "revoked", "tainted", "admitted"):
        nxt[key] = nxt[key] or row[key]
    nxt["evidence_transition_required"] |= row["support_promotion_requested"]
    nxt["logical_time"] = row["logical_time"]
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
    for name, key, value in (("certificate_missing","certificate_id",0),("source_missing","source_id",0),("authority","source_authority",5),("epoch","lifecycle_epoch",0),("malformed","well_formed",False),("revoked","revoked",True),("tainted","tainted",True),("time","logical_time",0)): m("bind_"+name,0,key,value)
    for name, key, value in (("certificate","certificate_id",999),("source","source_id",999),("source_authority","source_authority",2),("derived_missing","derived_id",0),("authority","derived_authority",4),("not_derived","derived_representation",False),("bindings","source_bindings_declared",False),("receipt","source_binding_receipt",False),("revoked","revoked",True),("tainted","tainted",True),("time","logical_time",1)): m("derive_"+name,1,key,value)
    for name, key, value in (("certificate","certificate_id",999),("source","source_id",999),("source_authority","source_authority",2),("derived","derived_id",999),("derived_authority","derived_authority",1),("loss_decl","loss_contract_declared",False),("omission_decl","omissions_declared",False),("uses_decl","permitted_uses_declared",False),("loss_id","loss_contract_id",0),("omission_id","omission_ledger_id",0),("use_id","permitted_use_id",0),("epoch","lifecycle_epoch",2),("receipt","certificate_receipt",False),("revoked","revoked",True),("tainted","tainted",True)): m("certify_"+name,2,key,value)
    for name, key, value in (("certificate","certificate_id",999),("source","source_id",999),("source_authority","source_authority",2),("derived","derived_id",999),("derived_authority","derived_authority",1),("loss","loss_contract_id",999),("omission","omission_ledger_id",999),("use","permitted_use_id",999),("epoch","lifecycle_epoch",2),("refs","verifier_references_declared",False),("failed","verification_passed",False),("receipt","verification_receipt",False),("requirement","deletion_closure_required",False),("deletion","deletion_closure_receipt",False),("revoked","revoked",True),("tainted","tainted",True),("time","logical_time",3)): m("verify_"+name,3,key,value)
    for name, key, value in (("certificate","certificate_id",999),("source","source_id",999),("source_authority","source_authority",2),("derived","derived_id",999),("derived_authority","derived_authority",1),("loss","loss_contract_id",999),("omission","omission_ledger_id",999),("use","permitted_use_id",999),("epoch","lifecycle_epoch",2),("scope","requested_use_id",999),("promotion","support_promotion_requested",True),("receipt","admitted",False),("time","logical_time",4)): m("admit_"+name,4,key,value)
    return out


def certificate_inventory(paths: list[Path], schema: dict[str, Any], issues: list[str]) -> list[dict[str, Any]]:
    receipts = []
    for path in paths:
        certs = load(path).get("semantic_page_certificates", [])
        if not certs: issues.append(path.name + ": expected at least one certificate"); continue
        for cert in certs:
            try: jsonschema.Draft202012Validator(schema).validate(cert); schema_valid = True
            except jsonschema.ValidationError as exc: schema_valid = False; issues.append(path.name + ": " + exc.message)
            shape_complete = all(bool(cert.get(key)) for key in ("page_id","source_bindings","derived_from","loss_contract","omissions","permitted_uses","validity_window","non_claims"))
            if not shape_complete: issues.append(path.name + ": certificate projection incomplete")
            receipts.append({"fixture":path.name + "#" + cert["page_id"],"schema_valid":schema_valid,"shape_complete":shape_complete,"revocation_state":cert["revocation_state"],"verification_state":cert["verification_state"]})
    return receipts


def build() -> tuple[dict[str, Any], list[str]]:
    issues: list[str] = []; cert_schema = load(CERT_SCHEMA); paths = sorted(SCENARIO_DIR.glob("*.json"))
    protocol = load(PROTOCOL_FIXTURE)
    try: jsonschema.Draft202012Validator(cert_schema).validate(protocol)
    except jsonschema.ValidationError as exc: issues.append("protocol certificate: " + exc.message)
    fixture_receipts = certificate_inventory(paths, cert_schema, issues)
    active = sum(row["revocation_state"] == "active" for row in fixture_receipts)
    stale = sum(row["revocation_state"] == "stale" for row in fixture_receipts)
    if len(paths) != 8 or len(fixture_receipts) != 12 or active != 11 or stale != 1: issues.append("certificate fixture inventory drift")
    admission = subprocess.run(["python3", str(ADMISSION_VALIDATOR)], cwd=ROOT, text=True, capture_output=True)
    if admission.returncode != 0: issues.append("admission suite failed: " + admission.stdout + admission.stderr)
    base = trace(); accepted, _, _, final = run(base)
    if not accepted or final["stage"] != "admitted" or not final["admitted"]: issues.append("reference trace rejected")
    mutation_receipts = []
    for mid, rows in mutations(base):
        ok, index, why, _ = run(rows); mutation_receipts.append({"mutation_id":mid,"rejected":not ok,"failed_event_index":index,"reasons":why})
        if ok: issues.append(mid + ": mutation accepted")
    result = {"schema_version":"asi_stack.context_certificate_refinement.v1","result_id":"context-certificate-refinement-2026-07-15-local",
              "source_sha256":{"lean_model":sha(LEAN),"certificate_schema":sha(CERT_SCHEMA),"protocol_fixture":sha(PROTOCOL_FIXTURE),"scenario_inventory":inventory_sha(paths),"admission_validator":sha(ADMISSION_VALIDATOR)},
              "protocol_fixture_schema_valid":True,"scenario_certificate_count":len(fixture_receipts),"schema_valid_scenario_certificate_count":sum(row["schema_valid"] for row in fixture_receipts),"shape_complete_scenario_certificate_count":sum(row["shape_complete"] for row in fixture_receipts),"active_certificate_count":active,"stale_certificate_count":stale,"scenario_certificate_receipts":fixture_receipts,
              "admission_valid_fixture_count":3,"admission_invalid_fixture_count":5,"admission_suite_passed":admission.returncode == 0,
              "reachable_trace_event_count":len(base),"reference_trace_final_state":final,"mutation_count":len(mutation_receipts),"mutation_rejection_count":sum(row["rejected"] for row in mutation_receipts),"mutation_receipts":mutation_receipts,"support_state_effect":"none",
              "non_claims":["Schema-valid and shape-complete certificates are not thereby truthful, fresh, adequate, or admissible for a consumer.","The eight scenario certificates are inspected separately from the whole-scenario 3/5 admission judgment; certificate shape does not launder scenario validity.","This packet does not establish source or payload truth, transformation or omission fidelity, verifier independence, deployed certificate enforcement, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support."]}
    try: jsonschema.Draft202012Validator(load(SCHEMA)).validate(result)
    except jsonschema.ValidationError as exc: issues.append("result schema: " + exc.message)
    return result, issues


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    result, issues = build()
    if issues: raise SystemExit("Context certificate refinement failed:\n - " + "\n - ".join(issues))
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    elif not RESULT.exists() or load(RESULT) != result: raise SystemExit("Context certificate refinement result stale; run --write")
    print(f"Context certificate refinement passed: 12 schema-valid certificate projections across 8 scenarios kept separate from 3/5 admission fixtures, 5 reachable events, {result['mutation_rejection_count']} mutations rejected, support effect none.")


if __name__ == "__main__": main()

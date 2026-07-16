#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ProceduralMemoryRefinement.lean"
SCHEMA = ROOT / "schemas/procedural_memory_refinement.schema.json"
RESULT = ROOT / "experiments/procedural_memory_refinement/results/2026-07-15-local.json"
LOOP = ROOT / "experiments/procedural_memory_loop/fixtures"
PROMOTION = ROOT / "experiments/procedural_trace_promotion/fixtures"
COMMAND = "python3 scripts/validate_procedural_memory_refinement.py"

STAGES = ["idle", "clustered", "abstracted", "verified", "qualified", "routable", "retired"]
KINDS = {
    "idle": "clusterTraces", "clustered": "bindAbstraction", "abstracted": "verifyProcedure",
    "verified": "qualifyProcedure", "qualified": "publishRoute", "routable": "retireProcedure",
    "retired": "retireProcedure",
}
ACCEPTED = {
    "accept_cluster", "accept_abstraction", "accept_verification",
    "accept_qualification", "accept_route", "accept_retirement",
}
BINDING_FIELDS = {
    "procedureId", "procedureVersion", "sourceSetDigest", "traceClusterDigest",
    "abstractionDigest", "regressionSuiteDigest", "scfDigest", "policyDigest", "consumerDigest",
}
LINEAGE_FIELDS = {"sourceSetDigest", "traceClusterDigest", "abstractionDigest", "regressionSuiteDigest", "scfDigest"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet() -> dict[str, Any]:
    return {
        "procedureId": 701, "procedureVersion": 3, "sourceSetDigest": 801,
        "traceClusterDigest": 802, "abstractionDigest": 803, "regressionSuiteDigest": 804,
        "scfDigest": 805, "policyDigest": 806, "consumerDigest": 807, "eventDigest": 1,
        "comparableTracesPresent": True, "negativeExamplesPreserved": True,
        "sourceReceiptsPresent": True, "effectReceiptsPresent": True, "invariantPresent": True,
        "parametersPresent": True, "preconditionsPresent": True, "postconditionsPresent": True,
        "verificationPassed": True, "regressionFailed": False, "benchmarkFloorPreserved": True,
        "activeScfPresent": True, "rollbackPlanPresent": True, "rollbackRehearsed": True,
        "monitoringPlanPresent": True, "residualsPresent": True, "nonClaimsPresent": True,
        "consumerAcknowledgmentPresent": True, "retirementTriggered": True,
        "retirementReceiptPresent": True, "supportAssignmentRequested": False,
        "externalEffectRequested": False,
    }


def state(stage: str, last_event: int = 0) -> dict[str, Any]:
    p = packet()
    return {"stage": stage, "lastEventDigest": last_event, **{key: p[key] for key in BINDING_FIELDS}}


def route(stage: str, kind: str, p: dict[str, Any], last_event: int = 0) -> str:
    s = state(stage, last_event)
    if kind != KINDS[stage]: return "reject_wrong_stage"
    if any(p[key] != s[key] for key in BINDING_FIELDS - LINEAGE_FIELDS): return "reject_procedure_substitution"
    if any(p[key] != s[key] for key in LINEAGE_FIELDS): return "reject_lineage_substitution"
    if p["eventDigest"] == last_event: return "reject_event_replay"
    if p["supportAssignmentRequested"] or p["externalEffectRequested"]: return "reject_authority_leak"
    checks = {
        "idle": [("comparableTracesPresent", False, "request_comparable_traces"),
                 ("negativeExamplesPreserved", False, "request_negative_examples"),
                 ("sourceReceiptsPresent", False, "request_source_receipts"),
                 ("effectReceiptsPresent", False, "request_effect_receipts")],
        "clustered": [("invariantPresent", False, "request_invariant"),
                      ("parametersPresent", False, "request_parameters"),
                      ("preconditionsPresent", False, "request_preconditions"),
                      ("postconditionsPresent", False, "request_postconditions")],
        "abstracted": [("verificationPassed", False, "request_verification"),
                       ("regressionFailed", True, "quarantine_regression_failure"),
                       ("benchmarkFloorPreserved", False, "request_benchmark_floor")],
        "verified": [("activeScfPresent", False, "request_active_scf"),
                     ("rollbackPlanPresent", False, "request_rollback_plan"),
                     ("rollbackRehearsed", False, "request_rollback_rehearsal")],
        "qualified": [("monitoringPlanPresent", False, "request_monitoring_plan"),
                      ("residualsPresent", False, "request_residuals"),
                      ("nonClaimsPresent", False, "request_non_claims"),
                      ("consumerAcknowledgmentPresent", False, "request_consumer_acknowledgment")],
        "routable": [("retirementTriggered", False, "request_retirement_trigger"),
                     ("retirementReceiptPresent", False, "request_retirement_receipt")],
    }
    if stage == "retired": return "reject_wrong_stage"
    for field, bad, answer in checks[stage]:
        if p[field] is bad: return answer
    return {"idle": "accept_cluster", "clustered": "accept_abstraction", "abstracted": "accept_verification",
            "verified": "accept_qualification", "qualified": "accept_route", "routable": "accept_retirement"}[stage]


def run(command: str) -> tuple[int, str]:
    proc = subprocess.run(command.split(), cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return proc.returncode, proc.stdout


def build() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for stage_name in STAGES[:-1]:
        p = packet(); p["eventDigest"] = STAGES.index(stage_name) + 1
        cases.append({"case_id": f"{stage_name}_accepted", "expected_route": route(stage_name, KINDS[stage_name], p)})
    negative_specs = [
        ("idle", "comparableTracesPresent", False), ("idle", "negativeExamplesPreserved", False),
        ("idle", "sourceReceiptsPresent", False), ("idle", "effectReceiptsPresent", False),
        ("clustered", "invariantPresent", False), ("clustered", "parametersPresent", False),
        ("clustered", "preconditionsPresent", False), ("clustered", "postconditionsPresent", False),
        ("abstracted", "verificationPassed", False), ("abstracted", "regressionFailed", True),
        ("abstracted", "benchmarkFloorPreserved", False), ("verified", "activeScfPresent", False),
        ("verified", "rollbackPlanPresent", False), ("verified", "rollbackRehearsed", False),
        ("qualified", "monitoringPlanPresent", False), ("qualified", "residualsPresent", False),
        ("qualified", "nonClaimsPresent", False), ("qualified", "consumerAcknowledgmentPresent", False),
        ("routable", "retirementTriggered", False), ("routable", "retirementReceiptPresent", False),
    ]
    for stage_name, field, value in negative_specs:
        p = packet(); p["eventDigest"] = 90; p[field] = value
        cases.append({"case_id": f"{stage_name}_{field}", "expected_route": route(stage_name, KINDS[stage_name], p)})
    for case_id, stage_name, kind, mutate in [
        ("wrong_stage", "idle", "publishRoute", None), ("event_replay", "idle", "clusterTraces", ("eventDigest", 0)),
        ("support_leak", "idle", "clusterTraces", ("supportAssignmentRequested", True)),
        ("effect_leak", "idle", "clusterTraces", ("externalEffectRequested", True)),
        ("procedure_substitution", "idle", "clusterTraces", ("procedureId", 999)),
        ("lineage_substitution", "idle", "clusterTraces", ("sourceSetDigest", 999)),
    ]:
        p = packet()
        if mutate: p[mutate[0]] = mutate[1]
        cases.append({"case_id": case_id, "expected_route": route(stage_name, kind, p)})
    mutations: list[dict[str, Any]] = []
    for field in sorted(BINDING_FIELDS):
        p = packet(); p[field] += 1000
        mutations.append({"mutation_id": field, "rejected": route("idle", "clusterTraces", p) not in ACCEPTED})
    for stage_name, field, value in negative_specs:
        p = packet(); p["eventDigest"] = 91; p[field] = value
        mutations.append({"mutation_id": f"{stage_name}_{field}", "rejected": route(stage_name, KINDS[stage_name], p) not in ACCEPTED})
    for field, value in [("eventDigest", 0), ("supportAssignmentRequested", True), ("externalEffectRequested", True)]:
        p = packet(); p[field] = value
        mutations.append({"mutation_id": field, "rejected": route("idle", "clusterTraces", p) not in ACCEPTED})
    mutations.append({"mutation_id": "wrong_kind", "rejected": route("idle", "publishRoute", packet()) not in ACCEPTED})
    loop_valid = len(list(LOOP.glob("valid_*.json"))); loop_invalid = len(list(LOOP.glob("invalid_*.json")))
    promotion_invalid = len(list(PROMOTION.glob("invalid_*.json")))
    command_receipts = []
    for command in ("python3 scripts/validate_procedural_memory_loop.py", "python3 scripts/validate_procedural_trace_promotion.py"):
        code, output = run(command)
        command_receipts.append({"command": command, "exit_code": code, "output_sha256": hashlib.sha256(output.encode()).hexdigest()})
        if code: raise RuntimeError(output)
    result = {
        "schema_version": "asi_stack.procedural_memory_refinement.v1",
        "result_id": "procedural-memory-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha(LEAN)},
        "input_suites": [
            {"suite_id": "procedural_memory_loop", "valid_count": loop_valid, "expected_invalid_count": loop_invalid},
            {"suite_id": "procedural_trace_promotion", "valid_count": 1, "expected_invalid_count": promotion_invalid},
        ],
        "reachable_stage_count": 7, "route_case_count": len(cases), "route_coverage": cases,
        "mutation_count": len(mutations), "mutation_rejection_count": sum(row["rejected"] for row in mutations),
        "mutation_receipts": mutations, "command_receipts": command_receipts,
        "witness": {"terminal_stage": "retired", "receipt_count": 6, "qualified_route_count": 1,
                    "support_assignment_count": 0, "external_effect_count": 0},
        "support_state_effect": "none",
        "non_claims": ["no natural trace-mining result", "no generated-tool correctness", "no deployed routing or retirement", "no support promotion"],
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    result = build(); errors: list[str] = []
    if result["mutation_count"] != result["mutation_rejection_count"]: errors.append("a mutation was accepted")
    if result["route_case_count"] != 32: errors.append(f"route count drifted: {result['route_case_count']}")
    lean = LEAN.read_text()
    for fragment in ("inductive Stage", "def routeFor", "apply_event_cannot_assign_support_or_external_effect", "full_procedure_lifecycle_reaches_retirement"):
        if fragment not in lean: errors.append(f"Lean model missing {fragment}")
    jsonschema.validate(result, json.loads(SCHEMA.read_text()))
    serialized = json.dumps(result, indent=2) + "\n"
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(serialized)
    elif not RESULT.exists() or RESULT.read_text() != serialized: errors.append(f"{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write")
    if errors:
        print("Procedural-memory refinement failed:"); [print(f" - {error}") for error in errors]; sys.exit(1)
    print(f"Procedural-memory refinement passed: 2 exact suites, 7 stages, 32 routes, {result['mutation_count']} mutations rejected, support effect none.")


if __name__ == "__main__": main()

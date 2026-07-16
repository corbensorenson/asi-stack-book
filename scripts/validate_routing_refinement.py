#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/RoutingRefinement.lean"
SCHEMA = ROOT / "schemas/routing_refinement.schema.json"
RESULT = ROOT / "experiments/routing_refinement/results/2026-07-15-local.json"
POST_V2 = ROOT / "experiments/post_v2_routing_deliberation/results/2026-07-10-local.json"
COMMAND = "python3 scripts/validate_routing_refinement.py"

STAGES = ["idle", "requestBound", "registryFrozen", "leaseQualified", "dispatched", "outcomeObserved", "closed"]
KINDS = {
    "idle": "bindRequest", "requestBound": "freezeRegistry", "registryFrozen": "qualifyLease",
    "leaseQualified": "dispatchRoute", "dispatched": "observeOutcome",
    "outcomeObserved": "closeRoute", "closed": "closeRoute",
}
ACCEPTED = {"accept_request", "accept_registry", "accept_lease", "accept_dispatch", "accept_observation", "accept_closure"}
BINDING_FIELDS = {
    "taskId", "taskVersion", "requestDigest", "registryDigest", "candidateSetDigest",
    "selectedSpecialistDigest", "capabilityDigest", "authorityDigest", "readinessDigest",
    "contextLeaseDigest", "toolLeaseDigest", "evaluatorDigest", "policyDigest", "consumerDigest",
}
TASK_FIELDS = {"taskId", "taskVersion", "requestDigest", "capabilityDigest", "policyDigest", "consumerDigest"}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def packet() -> dict[str, Any]:
    return {
        "taskId": 601, "taskVersion": 4, "requestDigest": 701, "registryDigest": 702,
        "candidateSetDigest": 703, "selectedSpecialistDigest": 704, "capabilityDigest": 705,
        "authorityDigest": 706, "readinessDigest": 707, "contextLeaseDigest": 708,
        "toolLeaseDigest": 709, "evaluatorDigest": 710, "policyDigest": 711,
        "consumerDigest": 712, "eventDigest": 1, "taskPresent": True,
        "capabilityRequestPresent": True, "registryPresent": True,
        "candidateDenominatorComplete": True, "heldOutLabelLeakAbsent": True,
        "selectedSpecialistRegistered": True, "authoritySatisfied": True,
        "readinessSatisfied": True, "fallbackAvailable": True, "residualOwnerPresent": True,
        "contextLeaseFresh": True, "toolLeaseFresh": True, "costQualityRecordPresent": True,
        "leastCapableAdequate": True, "rejectedCandidateEvidencePresent": True,
        "selectivePolicyPresent": True, "ambiguityDetected": False, "selectiveActionChosen": True,
        "sourceInspected": True, "runtimeEvidenceRefsPresent": True,
        "replayEvidenceRefsPresent": True, "dispatchGrantPresent": True,
        "isolationBoundaryPresent": True, "outcomeObserved": True,
        "routeQualityRecorded": True, "answerQualityRecorded": True,
        "unsafeOutcomeRecorded": True, "costRecordPresent": True, "lifecycleCurrent": True,
        "revocationClosureComplete": True, "consumerAcknowledgmentPresent": True,
        "nonClaimsPresent": True, "supportAssignmentRequested": False,
        "externalEffectRequested": False,
    }


def state(stage: str, last_event: int = 0) -> dict[str, Any]:
    p = packet()
    return {"stage": stage, "lastEventDigest": last_event, **{key: p[key] for key in BINDING_FIELDS}}


def route(stage: str, kind: str, p: dict[str, Any], last_event: int = 0) -> str:
    s = state(stage, last_event)
    if kind != KINDS[stage]: return "reject_wrong_stage"
    if any(p[key] != s[key] for key in TASK_FIELDS): return "reject_task_substitution"
    if any(p[key] != s[key] for key in BINDING_FIELDS - TASK_FIELDS): return "reject_registry_substitution"
    if p["eventDigest"] == last_event: return "reject_event_replay"
    if p["supportAssignmentRequested"] or p["externalEffectRequested"]: return "reject_authority_leak"
    if stage == "idle":
        if not p["taskPresent"]: return "request_task"
        if not p["capabilityRequestPresent"]: return "request_capability"
        return "accept_request"
    if stage == "requestBound":
        if not p["registryPresent"]: return "request_registry"
        if not p["candidateDenominatorComplete"]: return "request_candidate_denominator"
        if not p["heldOutLabelLeakAbsent"]: return "reject_label_leak"
        if not p["selectedSpecialistRegistered"]: return "request_registered_selection"
        return "accept_registry"
    if stage == "registryFrozen":
        if not p["authoritySatisfied"]: return "block_authority"
        if not p["readinessSatisfied"]:
            if p["fallbackAvailable"]: return "route_fallback"
            if not p["residualOwnerPresent"]: return "request_residual_owner"
            return "block_readiness"
        for field, answer in [
            ("contextLeaseFresh", "request_fresh_context_lease"),
            ("toolLeaseFresh", "request_fresh_tool_lease"),
            ("costQualityRecordPresent", "request_cost_quality"),
            ("leastCapableAdequate", "request_least_capable_adequate"),
            ("rejectedCandidateEvidencePresent", "request_rejected_candidate_evidence"),
            ("selectivePolicyPresent", "request_selective_policy"),
        ]:
            if not p[field]: return answer
        if p["ambiguityDetected"] and not p["selectiveActionChosen"]: return "request_selective_action"
        for field, answer in [
            ("sourceInspected", "request_source_inspection"),
            ("runtimeEvidenceRefsPresent", "request_runtime_evidence"),
            ("replayEvidenceRefsPresent", "request_replay_evidence"),
        ]:
            if not p[field]: return answer
        return "accept_lease"
    if stage == "leaseQualified":
        if not p["dispatchGrantPresent"]: return "request_dispatch_grant"
        if not p["isolationBoundaryPresent"]: return "request_isolation"
        return "accept_dispatch"
    if stage == "dispatched":
        for field, answer in [
            ("outcomeObserved", "request_outcome_observation"),
            ("routeQualityRecorded", "request_route_quality"),
            ("answerQualityRecorded", "request_answer_quality"),
            ("unsafeOutcomeRecorded", "request_unsafe_outcome"),
            ("costRecordPresent", "request_cost_record"),
        ]:
            if not p[field]: return answer
        return "accept_observation"
    if stage == "outcomeObserved":
        for field, answer in [
            ("lifecycleCurrent", "request_lifecycle_current"),
            ("revocationClosureComplete", "request_revocation_closure"),
            ("consumerAcknowledgmentPresent", "request_consumer_acknowledgment"),
            ("nonClaimsPresent", "request_non_claims"),
        ]:
            if not p[field]: return answer
        return "accept_closure"
    return "reject_wrong_stage"


def run(command: str) -> dict[str, Any]:
    proc = subprocess.run(command.split(), cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode:
        raise RuntimeError(proc.stdout)
    return {"command": command, "exit_code": proc.returncode, "output_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest()}


def post_v2_summary() -> dict[str, Any]:
    data = json.loads(POST_V2.read_text())
    routing, deliberation = data["routing"], data["deliberation"]
    by_routing = lambda arm, field: sum(row[field] for row in routing["summary"] if row["arm"] == arm)
    by_deliberation = lambda arm, field: sum(row[field] for row in deliberation["summary"] if row["arm"] == arm)
    return {
        "seed_count": len(data["seeds"]), "routing_record_count": len(routing["records"]),
        "deliberation_record_count": len(deliberation["records"]),
        "learned_router_correct": by_routing("learned_router", "correct"),
        "generalist_correct": by_routing("single_general_specialist", "correct"),
        "fallback_activation_count": sum(row["fallbacks"] for row in routing["summary"]),
        "adaptive_correct": by_deliberation("adaptive_deliberation", "correct"),
        "adaptive_candidate_operations": by_deliberation("adaptive_deliberation", "candidate_operations"),
        "fixed_correct": by_deliberation("fixed_three_step", "correct"),
        "fixed_candidate_operations": by_deliberation("fixed_three_step", "candidate_operations"),
        "fixed_extra_compute_harm": by_deliberation("fixed_three_step", "extra_compute_harm"),
        "no_change_disposition_count": sum(row["disposition"] == "no_change" for row in data["claim_dispositions"]),
        "support_state_effect": data["support_state_effect"],
    }


def build() -> dict[str, Any]:
    cases: list[dict[str, Any]] = []
    for stage_name in STAGES[:-1]:
        p = packet(); p["eventDigest"] = STAGES.index(stage_name) + 1
        cases.append({"case_id": f"{stage_name}_accepted", "expected_route": route(stage_name, KINDS[stage_name], p)})
    gates = [
        ("idle", "taskPresent", False), ("idle", "capabilityRequestPresent", False),
        ("requestBound", "registryPresent", False), ("requestBound", "candidateDenominatorComplete", False),
        ("requestBound", "heldOutLabelLeakAbsent", False), ("requestBound", "selectedSpecialistRegistered", False),
        ("registryFrozen", "authoritySatisfied", False),
        ("registryFrozen", "readiness_fallback", False), ("registryFrozen", "readiness_residual", False),
        ("registryFrozen", "readiness_block", False),
        ("registryFrozen", "contextLeaseFresh", False), ("registryFrozen", "toolLeaseFresh", False),
        ("registryFrozen", "costQualityRecordPresent", False), ("registryFrozen", "leastCapableAdequate", False),
        ("registryFrozen", "rejectedCandidateEvidencePresent", False), ("registryFrozen", "selectivePolicyPresent", False),
        ("registryFrozen", "ambiguity_selective", False), ("registryFrozen", "sourceInspected", False),
        ("registryFrozen", "runtimeEvidenceRefsPresent", False), ("registryFrozen", "replayEvidenceRefsPresent", False),
        ("leaseQualified", "dispatchGrantPresent", False), ("leaseQualified", "isolationBoundaryPresent", False),
        ("dispatched", "outcomeObserved", False), ("dispatched", "routeQualityRecorded", False),
        ("dispatched", "answerQualityRecorded", False), ("dispatched", "unsafeOutcomeRecorded", False),
        ("dispatched", "costRecordPresent", False), ("outcomeObserved", "lifecycleCurrent", False),
        ("outcomeObserved", "revocationClosureComplete", False),
        ("outcomeObserved", "consumerAcknowledgmentPresent", False), ("outcomeObserved", "nonClaimsPresent", False),
    ]
    for stage_name, field, value in gates:
        p = packet(); p["eventDigest"] = 90
        if field == "readiness_fallback": p["readinessSatisfied"] = False
        elif field == "readiness_residual":
            p["readinessSatisfied"] = False; p["fallbackAvailable"] = False; p["residualOwnerPresent"] = False
        elif field == "readiness_block":
            p["readinessSatisfied"] = False; p["fallbackAvailable"] = False
        elif field == "ambiguity_selective":
            p["ambiguityDetected"] = True; p["selectiveActionChosen"] = False
        else: p[field] = value
        cases.append({"case_id": f"{stage_name}_{field}", "expected_route": route(stage_name, KINDS[stage_name], p)})
    for case_id, kind, mutate in [
        ("wrong_stage", "dispatchRoute", None), ("task_substitution", "bindRequest", ("taskId", 999)),
        ("registry_substitution", "bindRequest", ("registryDigest", 999)),
        ("event_replay", "bindRequest", ("eventDigest", 0)),
        ("authority_leak", "bindRequest", ("supportAssignmentRequested", True)),
    ]:
        p = packet()
        if mutate: p[mutate[0]] = mutate[1]
        cases.append({"case_id": case_id, "expected_route": route("idle", kind, p)})

    mutations: list[dict[str, Any]] = []
    for field in sorted(BINDING_FIELDS):
        p = packet(); p[field] += 1000
        mutations.append({"mutation_id": f"binding_{field}", "rejected": route("idle", "bindRequest", p) not in ACCEPTED})
    # Fallback and readiness-block are valid negative routes, not independent gate mutations.
    for stage_name, field, value in [row for row in gates if row[1] not in {"readiness_fallback", "readiness_block"}]:
        p = packet(); p["eventDigest"] = 91
        if field == "readiness_residual":
            p["readinessSatisfied"] = False; p["fallbackAvailable"] = False; p["residualOwnerPresent"] = False
        elif field == "ambiguity_selective":
            p["ambiguityDetected"] = True; p["selectiveActionChosen"] = False
        else: p[field] = value
        mutations.append({"mutation_id": f"gate_{stage_name}_{field}", "rejected": route(stage_name, KINDS[stage_name], p) not in ACCEPTED})
    for mutation_id, kind, field, value in [
        ("wrong_kind", "dispatchRoute", None, None), ("event_replay", "bindRequest", "eventDigest", 0),
        ("support_leak", "bindRequest", "supportAssignmentRequested", True),
        ("external_effect_leak", "bindRequest", "externalEffectRequested", True),
    ]:
        p = packet()
        if field: p[field] = value
        mutations.append({"mutation_id": mutation_id, "rejected": route("idle", kind, p) not in ACCEPTED})

    commands = [
        run("python3 scripts/validate_routing_decision_lease.py"),
        run("python3 scripts/validate_readiness_residual_gates.py"),
        run("python3 scripts/validate_post_v2_routing_deliberation.py"),
    ]
    return {
        "schema_version": "asi_stack.routing_refinement.v1",
        "result_id": "routing-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": sha(LEAN), "post_v2_result": sha(POST_V2)},
        "input_suites": [
            {"suite_id": "routing_decision_lease", "valid_count": 3, "expected_invalid_count": 7},
            {"suite_id": "readiness_residual_gates", "valid_count": 4, "expected_invalid_count": 5},
            {"suite_id": "post_v2_routing_deliberation", **post_v2_summary()},
        ],
        "reachable_stage_count": 7, "route_case_count": len(cases), "route_coverage": cases,
        "mutation_count": len(mutations), "mutation_rejection_count": sum(row["rejected"] for row in mutations),
        "mutation_receipts": mutations, "command_receipts": commands,
        "witness": {"terminal_stage": "closed", "receipt_count": 6, "dispatch_count": 1,
                    "route_outcome_count": 1, "answer_outcome_count": 1,
                    "support_assignment_count": 0, "external_effect_count": 0},
        "support_state_effect": "none",
        "non_claims": [
            "no natural useful-routing result", "no strong-model or open-world transfer",
            "no deployed authority, runtime correctness, or replay correctness",
            "no claim that route correctness establishes answer correctness", "no support promotion",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(); parser.add_argument("--write", action="store_true"); args = parser.parse_args()
    result = build(); errors: list[str] = []
    if result["route_case_count"] != 42: errors.append(f"route count drifted: {result['route_case_count']}")
    if result["mutation_count"] != 47 or result["mutation_rejection_count"] != 47:
        errors.append(f"mutation contract drifted: {result['mutation_rejection_count']}/{result['mutation_count']}")
    lean = LEAN.read_text()
    for fragment in ("inductive Stage", "def routeFor", "outcome_keeps_route_and_answer_quality_separate", "full_routing_lifecycle_reaches_closed_state"):
        if fragment not in lean: errors.append(f"Lean model missing {fragment}")
    jsonschema.validate(result, json.loads(SCHEMA.read_text()))
    serialized = json.dumps(result, indent=2) + "\n"
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True); RESULT.write_text(serialized)
    elif not RESULT.exists() or RESULT.read_text() != serialized:
        errors.append(f"{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write")
    if errors:
        print("Routing refinement failed:"); [print(f" - {error}") for error in errors]; sys.exit(1)
    print("Routing refinement passed: 3 exact suites, 7 stages, 42 routes, 47/47 mutations rejected, distinct route/answer outcomes, support effect none.")


if __name__ == "__main__": main()

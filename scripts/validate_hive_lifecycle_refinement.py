#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

import jsonschema

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/HiveLifecycleRefinement.lean"
SCHEMA = ROOT / "schemas/hive_lifecycle_refinement.schema.json"
RESULT = ROOT / "experiments/hive_lifecycle_refinement/results/2026-07-15-local.json"
COMMAND = "python3 scripts/validate_hive_lifecycle_refinement.py"

STAGES = [
    "requested",
    "policyBound",
    "nodeSelected",
    "leased",
    "executed",
    "reconciled",
    "closed",
]
KINDS = {
    "requested": "bindPolicy",
    "policyBound": "selectNode",
    "nodeSelected": "issueLease",
    "leased": "execute",
    "executed": "reconcile",
    "reconciled": "close",
    "closed": "close",
}
NEXT_STAGE = dict(zip(STAGES[:-1], STAGES[1:]))
ACCEPTED = {
    "accept_policy",
    "accept_selection",
    "accept_lease",
    "accept_execution",
    "accept_reconciliation",
    "accept_closure",
}
IDENTITY_FIELDS = (
    "jobId",
    "jobVersion",
    "principalDigest",
    "contractDigest",
    "nodeRegistryDigest",
    "candidateSetDigest",
    "selectedNodeDigest",
    "policyDigest",
    "authorityDigest",
    "leaseDigest",
    "evaluatorDigest",
    "consumerDigest",
    "residualDigest",
)
JOB_FIELDS = {
    "jobId",
    "jobVersion",
    "principalDigest",
    "contractDigest",
    "policyDigest",
    "authorityDigest",
    "evaluatorDigest",
    "consumerDigest",
    "residualDigest",
}
NODE_FIELDS = {
    "nodeRegistryDigest",
    "candidateSetDigest",
    "selectedNodeDigest",
    "leaseDigest",
}
THEOREMS = (
    "accepted_step_is_accepted",
    "accepted_step_applies_event",
    "apply_event_preserves_full_identity",
    "accepted_step_preserves_full_identity",
    "accepted_step_preserves_support_and_external_effect_counts",
    "accepted_step_adds_exactly_one_receipt",
    "accepted_step_advances_stage",
    "accepted_run_preserves_full_identity",
    "accepted_run_preserves_support_count",
    "accepted_run_preserves_external_effect_count",
    "accepted_run_accounts_exact_receipts",
    "accepted_run_has_accepted_trace",
    "hive_run_append",
    "closed_state_accepts_no_event",
    "apply_event_preserves_job_node_lease_identity",
    "apply_event_cannot_assign_support_or_external_effect",
    "accepted_step_adds_one_receipt",
    "malformed_job_rejected",
    "missing_data_policy_blocks_binding",
    "incomplete_candidate_denominator_blocks_selection",
    "overprivileged_node_blocks_selection",
    "external_access_without_lease_blocks_issue",
    "missing_sandbox_blocks_lease",
    "high_risk_without_bound_approval_blocks_execution",
    "partitioned_stale_grant_quarantines_before_mutation",
    "partition_without_no_mutation_evidence_blocks",
    "missing_effect_receipt_blocks_reconciliation",
    "missing_useful_outcome_blocks_reconciliation",
    "missing_dropout_recovery_blocks_closure",
    "missing_revocation_closure_blocks_closure",
    "full_hive_lifecycle_reaches_closed_state",
)


def packet() -> dict[str, Any]:
    values: dict[str, Any] = {
        "jobId": 1001,
        "jobVersion": 2,
        "principalDigest": 1002,
        "contractDigest": 1003,
        "nodeRegistryDigest": 1004,
        "candidateSetDigest": 1005,
        "selectedNodeDigest": 1006,
        "policyDigest": 1007,
        "authorityDigest": 1008,
        "leaseDigest": 1009,
        "evaluatorDigest": 1010,
        "consumerDigest": 1011,
        "residualDigest": 1012,
        "eventDigest": 1,
    }
    for field in (
        "jobWellFormed",
        "identityPolicy",
        "dataPolicy",
        "toolPolicy",
        "approvalPolicy",
        "deviceRegistry",
        "schedulerPolicy",
        "candidateDenominator",
        "leastAuthority",
        "dataLocality",
        "costBudget",
        "energyBudget",
        "dropoutPlan",
        "federationLease",
        "sandbox",
        "leaseScope",
        "evidenceObligations",
        "expiration",
        "revocationPath",
        "boundApproval",
        "freshGrant",
        "deniedBeforeMutation",
        "stateUnchanged",
        "executionGrant",
        "monitor",
        "artifactReceipt",
        "effectReceipt",
        "resourceReceipt",
        "auditReceipt",
        "usefulOutcome",
        "residualOwner",
        "dropoutRecovery",
        "revocationClosure",
        "descendantClosure",
        "consumerAcknowledgment",
        "nonClaims",
    ):
        values[field] = True
    for field in (
        "externalAccess",
        "highRisk",
        "partitionDetected",
        "staleGrantPossible",
        "supportAssignmentRequested",
        "externalEffectRequested",
    ):
        values[field] = False
    return values


def initial_state() -> dict[str, Any]:
    state = {field: packet()[field] for field in IDENTITY_FIELDS}
    state.update(
        stage="requested",
        lastEventDigest=0,
        receiptCount=0,
        dispatchCount=0,
        usefulOutcomeCount=0,
        quarantineCount=0,
        recoveryCount=0,
        supportAssignmentCount=0,
        externalEffectCount=0,
    )
    return state


def route(state: dict[str, Any], kind: str, event: dict[str, Any]) -> str:
    stage = state["stage"]
    if kind != KINDS[stage]:
        return "reject_wrong_stage"
    if any(event[field] != state[field] for field in JOB_FIELDS):
        return "reject_job_substitution"
    if any(event[field] != state[field] for field in NODE_FIELDS):
        return "reject_node_substitution"
    if event["eventDigest"] == state["lastEventDigest"]:
        return "reject_event_replay"
    if event["supportAssignmentRequested"] or event["externalEffectRequested"]:
        return "reject_authority_leak"
    checks = {
        "requested": [
            ("jobWellFormed", "reject_malformed_job"),
            ("identityPolicy", "require_identity_policy"),
            ("dataPolicy", "require_data_policy"),
            ("toolPolicy", "require_tool_policy"),
            ("approvalPolicy", "require_approval_policy"),
        ],
        "policyBound": [
            ("deviceRegistry", "require_device_registry"),
            ("schedulerPolicy", "require_scheduler_policy"),
            ("candidateDenominator", "require_candidate_denominator"),
            ("leastAuthority", "require_least_authority"),
            ("dataLocality", "require_data_locality"),
            ("costBudget", "require_cost_budget"),
            ("energyBudget", "require_energy_budget"),
            ("dropoutPlan", "require_dropout_plan"),
        ],
        "nodeSelected": [
            ("sandbox", "require_sandbox"),
            ("leaseScope", "require_lease_scope"),
            ("evidenceObligations", "require_evidence_obligations"),
            ("expiration", "require_expiration"),
            ("revocationPath", "require_revocation_path"),
        ],
        "executed": [
            ("artifactReceipt", "require_artifact_receipt"),
            ("effectReceipt", "require_effect_receipt"),
            ("resourceReceipt", "require_resource_receipt"),
            ("auditReceipt", "require_audit_receipt"),
            ("usefulOutcome", "require_useful_outcome"),
            ("residualOwner", "require_residual_owner"),
        ],
        "reconciled": [
            ("dropoutRecovery", "require_dropout_recovery"),
            ("revocationClosure", "require_revocation_closure"),
            ("descendantClosure", "require_descendant_closure"),
            ("consumerAcknowledgment", "require_consumer_acknowledgment"),
            ("nonClaims", "require_non_claims"),
        ],
    }
    if stage == "nodeSelected" and event["externalAccess"] and not event["federationLease"]:
        return "require_federation_lease"
    if stage == "leased":
        if event["highRisk"] and not event["boundApproval"]:
            return "require_bound_approval"
        if not event["freshGrant"]:
            return "require_fresh_grant"
        if event["partitionDetected"] and event["staleGrantPossible"]:
            if event["deniedBeforeMutation"] and event["stateUnchanged"]:
                return "quarantine_partition"
            return "require_no_mutation_evidence"
        if not event["executionGrant"]:
            return "require_execution_grant"
        if not event["monitor"]:
            return "require_monitor"
        return "accept_execution"
    if stage == "closed":
        return "reject_wrong_stage"
    for field, failure in checks[stage]:
        if not event[field]:
            return failure
    return {
        "requested": "accept_policy",
        "policyBound": "accept_selection",
        "nodeSelected": "accept_lease",
        "executed": "accept_reconciliation",
        "reconciled": "accept_closure",
    }[stage]


def step(state: dict[str, Any], kind: str, event: dict[str, Any]) -> dict[str, Any] | None:
    if state["stage"] == "closed" or route(state, kind, event) not in ACCEPTED:
        return None
    next_state = dict(state)
    next_state["stage"] = NEXT_STAGE[state["stage"]]
    next_state["lastEventDigest"] = event["eventDigest"]
    next_state["receiptCount"] += 1
    if state["stage"] == "leased":
        next_state["dispatchCount"] += 1
    if state["stage"] == "executed":
        next_state["usefulOutcomeCount"] += 1
    if state["stage"] == "reconciled":
        next_state["recoveryCount"] += 1
    return next_state


def run_trace(
    state: dict[str, Any], events: list[tuple[str, dict[str, Any]]]
) -> dict[str, Any] | None:
    current = dict(state)
    for kind, event in events:
        next_state = step(current, kind, event)
        if next_state is None:
            return None
        current = next_state
    return current


def canonical_events() -> list[tuple[str, dict[str, Any]]]:
    events = []
    for index, stage in enumerate(STAGES[:-1], start=1):
        event = packet()
        event["eventDigest"] = index
        events.append((KINDS[stage], event))
    return events


def run_command(command: list[str], cwd: Path = ROOT) -> dict[str, Any]:
    process = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if process.returncode:
        raise RuntimeError(process.stdout)
    return {
        "command": " ".join(command),
        "exit_code": process.returncode,
        "output_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
    }


def mutate(stage: str, field: str) -> dict[str, Any]:
    event = packet()
    event["eventDigest"] = STAGES.index(stage) + 1
    if field == "external_no_lease":
        event["externalAccess"] = True
        event["federationLease"] = False
    elif field == "high_risk_no_approval":
        event["highRisk"] = True
        event["boundApproval"] = False
    elif field == "partition_quarantine":
        event["partitionDetected"] = True
        event["staleGrantPossible"] = True
    elif field == "partition_no_mutation":
        event["partitionDetected"] = True
        event["staleGrantPossible"] = True
        event["deniedBeforeMutation"] = False
    else:
        event[field] = False
    return event


def build() -> dict[str, Any]:
    lean_text = LEAN.read_text()
    theorem_surface = re.findall(r"^theorem\s+([A-Za-z0-9_']+)", lean_text, re.MULTILINE)
    if tuple(theorem_surface) != THEOREMS:
        raise ValueError("Lean theorem surface drifted")
    if re.search(r"\b(?:sorry|admit|axiom)\b", lean_text):
        raise ValueError("Lean source contains a forbidden proof placeholder")

    gates = (
        [("requested", field) for field in ("jobWellFormed", "identityPolicy", "dataPolicy", "toolPolicy", "approvalPolicy")]
        + [("policyBound", field) for field in ("deviceRegistry", "schedulerPolicy", "candidateDenominator", "leastAuthority", "dataLocality", "costBudget", "energyBudget", "dropoutPlan")]
        + [("nodeSelected", "external_no_lease")]
        + [("nodeSelected", field) for field in ("sandbox", "leaseScope", "evidenceObligations", "expiration", "revocationPath")]
        + [("leased", field) for field in ("high_risk_no_approval", "freshGrant", "partition_quarantine", "partition_no_mutation", "executionGrant", "monitor")]
        + [("executed", field) for field in ("artifactReceipt", "effectReceipt", "resourceReceipt", "auditReceipt", "usefulOutcome", "residualOwner")]
        + [("reconciled", field) for field in ("dropoutRecovery", "revocationClosure", "descendantClosure", "consumerAcknowledgment", "nonClaims")]
    )

    stage_states = [initial_state()]
    current = initial_state()
    events = canonical_events()
    route_cases = []
    for stage, (kind, event) in zip(STAGES[:-1], events):
        route_cases.append({"case_id": f"{stage}_accepted", "expected_route": route(current, kind, event)})
        next_state = step(current, kind, event)
        if next_state is None:
            raise ValueError(f"canonical lifecycle rejected at {stage}")
        current = next_state
        stage_states.append(current)

    for stage, field in gates:
        state = stage_states[STAGES.index(stage)]
        route_cases.append(
            {
                "case_id": f"{stage}_{field}",
                "expected_route": route(state, KINDS[stage], mutate(stage, field)),
            }
        )
    generic_cases = (
        ("wrong_stage", "requested", "close", None),
        ("job_substitution", "requested", "bindPolicy", "jobId"),
        ("node_substitution", "requested", "bindPolicy", "selectedNodeDigest"),
        ("event_replay", "requested", "bindPolicy", "eventDigest"),
        ("authority_leak", "requested", "bindPolicy", "supportAssignmentRequested"),
    )
    for case_id, stage, kind, field in generic_cases:
        state = stage_states[STAGES.index(stage)]
        event = packet()
        if field == "eventDigest":
            event[field] = state["lastEventDigest"]
        elif field == "supportAssignmentRequested":
            event[field] = True
        elif field:
            event[field] += 1000
        route_cases.append({"case_id": case_id, "expected_route": route(state, kind, event)})

    mutations = []
    for stage in STAGES[:-1]:
        state = stage_states[STAGES.index(stage)]
        for field in IDENTITY_FIELDS:
            event = packet()
            event["eventDigest"] = STAGES.index(stage) + 1
            event[field] += 1000
            mutations.append(
                {
                    "mutation_id": f"binding_{stage}_{field}",
                    "rejected": step(state, KINDS[stage], event) is None,
                }
            )
    for stage, field in gates:
        state = stage_states[STAGES.index(stage)]
        mutations.append(
            {
                "mutation_id": f"gate_{stage}_{field}",
                "rejected": step(state, KINDS[stage], mutate(stage, field)) is None,
            }
        )
    for stage in STAGES[:-1]:
        state = stage_states[STAGES.index(stage)]
        expected = KINDS[stage]
        wrong_kind = "bindPolicy" if expected == "close" else "close"
        for label, kind, field in (
            ("wrong_kind", wrong_kind, None),
            ("replay", expected, "eventDigest"),
            ("support", expected, "supportAssignmentRequested"),
            ("effect", expected, "externalEffectRequested"),
        ):
            event = packet()
            event["eventDigest"] = STAGES.index(stage) + 1
            if field == "eventDigest":
                event[field] = state["lastEventDigest"]
            elif field:
                event[field] = True
            mutations.append(
                {
                    "mutation_id": f"{label}_{stage}",
                    "rejected": step(state, kind, event) is None,
                }
            )
    final = stage_states[-1]
    for kind in sorted(set(KINDS.values())):
        event = packet()
        event["eventDigest"] = 99
        mutations.append(
            {
                "mutation_id": f"post_closed_{kind}",
                "rejected": step(final, kind, event) is None,
            }
        )

    identity = {field: initial_state()[field] for field in IDENTITY_FIELDS}
    identity_checks = sum(
        {field: state[field] for field in IDENTITY_FIELDS} == identity for state in stage_states
    )
    non_authority_checks = sum(
        state["supportAssignmentCount"] == 0 and state["externalEffectCount"] == 0
        for state in stage_states
    )
    composition_checks = 0
    for split in range(len(events) + 1):
        middle = run_trace(initial_state(), events[:split])
        if middle is not None and run_trace(middle, events[split:]) == final:
            composition_checks += 1

    witness = {
        "terminal_stage": final["stage"],
        "receipt_count": final["receiptCount"],
        "dispatch_count": final["dispatchCount"],
        "useful_outcome_count": final["usefulOutcomeCount"],
        "recovery_count": final["recoveryCount"],
        "support_assignment_count": final["supportAssignmentCount"],
        "external_effect_count": final["externalEffectCount"],
    }
    expected_witness = {
        "terminal_stage": "closed",
        "receipt_count": 6,
        "dispatch_count": 1,
        "useful_outcome_count": 1,
        "recovery_count": 1,
        "support_assignment_count": 0,
        "external_effect_count": 0,
    }
    if witness != expected_witness:
        raise ValueError(f"independent lifecycle witness drifted: {witness}")

    return {
        "schema_version": "asi_stack.hive_lifecycle_refinement.v2",
        "result_id": "hive-lifecycle-refinement-2026-07-15-local",
        "source_sha256": {"lean_model": hashlib.sha256(LEAN.read_bytes()).hexdigest()},
        "lean_theorem_count": len(theorem_surface),
        "lean_theorem_surface": theorem_surface,
        "input_suites": [
            {"suite_id": "hive_admission", "valid_count": 2, "expected_invalid_count": 8},
            {"suite_id": "partitioned_authority", "valid_count": 3, "expected_invalid_count": 6},
        ],
        "reachable_stage_count": len(stage_states),
        "trace_event_count": len(events),
        "trace_composition_split_count": composition_checks,
        "identity_field_count": len(IDENTITY_FIELDS),
        "identity_preservation_check_count": identity_checks,
        "non_authority_preservation_check_count": non_authority_checks,
        "terminal_rejection_count": len(set(KINDS.values())),
        "route_case_count": len(route_cases),
        "route_coverage": route_cases,
        "mutation_count": len(mutations),
        "mutation_rejection_count": sum(item["rejected"] for item in mutations),
        "mutation_receipts": mutations,
        "command_receipts": [
            run_command(["lake", "env", "lean", "AsiStackProofs/HiveLifecycleRefinement.lean"], ROOT / "lean"),
            run_command(["python3", "scripts/validate_hive_admission.py"]),
            run_command(["python3", "scripts/validate_partitioned_authority_fixture.py"]),
        ],
        "witness": witness,
        "support_state_effect": "none",
        "non_claims": [
            "no deployed scheduler or federation",
            "no real device, portal, authority-service, or sandbox enforcement",
            "no partition tolerance, availability, security, or privacy result",
            "no measured energy, dropout recovery, useful-work, or transfer result",
            "no support promotion",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    errors = []
    result = build()
    if result["route_case_count"] != 47:
        errors.append("route count drifted")
    if result["lean_theorem_count"] != 31:
        errors.append("Lean theorem count drifted")
    if result["trace_composition_split_count"] != 7:
        errors.append("trace composition contract drifted")
    if result["identity_preservation_check_count"] != 7:
        errors.append("identity preservation contract drifted")
    if result["non_authority_preservation_check_count"] != 7:
        errors.append("non-authority preservation contract drifted")
    if result["terminal_rejection_count"] != 6:
        errors.append("terminal rejection contract drifted")
    if result["mutation_count"] != 144 or result["mutation_rejection_count"] != 144:
        errors.append("mutation contract drifted")
    jsonschema.validate(result, json.loads(SCHEMA.read_text()))
    serialized = json.dumps(result, indent=2) + "\n"
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized)
    elif not RESULT.exists() or RESULT.read_text() != serialized:
        errors.append(f"{RESULT.relative_to(ROOT)} stale; run {COMMAND} --write")
    if errors:
        print("Hive lifecycle refinement failed:\n - " + "\n - ".join(errors))
        sys.exit(1)
    print(
        "Hive lifecycle refinement passed: 31 Lean theorems, 2 exact suites, "
        "7 stages, 7 trace splits, 47 routes, 144/144 mutations rejected, "
        "support effect none."
    )


if __name__ == "__main__":
    main()

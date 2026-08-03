#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean" / "AsiStackProofs" / "HumanAIOrganizations.lean"
LEAN_ROOT = ROOT / "lean" / "AsiStackProofs.lean"
CHAPTER = ROOT / "chapters" / "human-ai-organizations-delegation-and-accountability.qmd"
DOSSIER = ROOT / "evidence_quality" / "proof_model_dossiers" / "human-ai-organizations-delegation-and-accountability.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
BRIDGE_FIXTURE = ROOT / "tests" / "fixtures" / "proof_models" / "human_ai_organization_responsibility_bridge.json"

TAG = "lean:human_ai_org.accountability_requires_authority"
MODULE = "AsiStackProofs.HumanAIOrganizations"
FORMAL_TARGET = (
    "A five-stage finite review preserves staged capacity, authority, independence, and remedy "
    "invariants over arbitrary run length; assignable accountability requires all 20 authored "
    "fields, while 20 closed mutations reach exact repair states. A separate ten-stage "
    "delegation-to-remedy lifecycle proves arbitrary-run nine-field identity custody, support/effect "
    "non-authority, exact receipts, contest/remedy monotonicity, accepted traces, batch composition, "
    "absorbing closure, and one bounded adverse-path witness. A compositional responsibility bridge "
    "then refines the authority-delegation chain, preserves accountable-owner, independent-review, "
    "evidence, residual-owner, receipt, and non-authority invariants through a two-hop witness, and "
    "shows that aggregate delegation summaries cannot recover accountability. An independent consumer "
    "reaches all 39 lifecycle routes, rejects 156/156 lifecycle mutations and 50/50 bridge mutations, "
    "and checks all three bridge compositions. It establishes no field truth, lawful accountability, "
    "human control, organizational outcome, support, or external effect."
)

EXERCISE_STAGES = (
    "proposed", "delegated", "active", "escalated", "handedOff", "contested",
    "authorityExpired", "reconstructed", "remedied", "closed",
)
LIVE_EXERCISE_STAGES = EXERCISE_STAGES[:-1]
EXERCISE_KINDS = {
    "proposed": "bindDelegation", "delegated": "activateWork",
    "active": "recordEscalation", "escalated": "handOff",
    "handedOff": "recordContest", "contested": "expireAuthority",
    "authorityExpired": "reconstructIncident", "reconstructed": "recordRemedy",
    "remedied": "close", "closed": "close",
}
NEXT_EXERCISE_STAGE = dict(zip(EXERCISE_STAGES[:-1], EXERCISE_STAGES[1:]))
EXERCISE_IDENTITY_KEYS = (
    "decisionDigest", "delegatorDigest", "delegateDigest", "policyDigest",
    "authorityDigest", "reviewerDigest", "evidenceDigest", "remedyDigest", "resultDigest",
)
EXERCISE_ACCEPTED = {
    "acceptDelegation", "acceptActivation", "acceptEscalation", "acceptHandoff",
    "acceptContest", "acceptExpiry", "acceptReconstruction", "acceptRemedy", "acceptClosure",
}

BASE_RECORD = {
    "assignmentRequested": True,
    "decisionIdentityPresent": True,
    "accountableActorPresent": True,
    "informationAvailable": True,
    "competenceCurrent": True,
    "timeAvailable": True,
    "workloadWithinLimit": True,
    "decisionAuthorityPresent": True,
    "interventionAuthorityPresent": True,
    "practicalAbilityToChange": True,
    "revocationPathPresent": True,
    "independentReviewPresent": True,
    "separationOfDutiesPresent": True,
    "conflictDispositionPresent": True,
    "stopPathPresent": True,
    "appealPathPresent": True,
    "remedyPathPresent": True,
    "evidenceAccessPresent": True,
    "residualCustodyPresent": True,
    "nonClaimBoundaryPresent": True,
}

EXPECTED_MUTATIONS = {
    "assignmentRequested": "refusedNoAssignment",
    "decisionIdentityPresent": "repairDecisionIdentity",
    "accountableActorPresent": "repairActorIdentity",
    "informationAvailable": "repairInformation",
    "competenceCurrent": "repairCompetence",
    "timeAvailable": "repairTime",
    "workloadWithinLimit": "repairWorkload",
    "decisionAuthorityPresent": "repairDecisionAuthority",
    "interventionAuthorityPresent": "repairInterventionAuthority",
    "practicalAbilityToChange": "repairPracticalControl",
    "revocationPathPresent": "repairRevocation",
    "independentReviewPresent": "repairIndependentReview",
    "separationOfDutiesPresent": "repairSeparationOfDuties",
    "conflictDispositionPresent": "repairConflictDisposition",
    "stopPathPresent": "repairStopPath",
    "appealPathPresent": "repairAppealPath",
    "remedyPathPresent": "repairRemedyPath",
    "evidenceAccessPresent": "repairEvidenceAccess",
    "residualCustodyPresent": "repairResidualCustody",
    "nonClaimBoundaryPresent": "repairNonClaimBoundary",
}

REQUIRED_THEOREMS = {
    "accountability_review_step_preserves_stage_invariant",
    "accountability_review_run_preserves_stage_invariant",
    "assignable_accountability_requires_complete_authority_record",
    "complete_accountability_record_reaches_assignment",
    "missing_information_blocks_accountability_assignment",
    "missing_competence_blocks_accountability_assignment",
    "missing_time_blocks_accountability_assignment",
    "excessive_workload_blocks_accountability_assignment",
    "missing_decision_authority_blocks_accountability_assignment",
    "missing_intervention_authority_blocks_accountability_assignment",
    "missing_practical_control_blocks_accountability_assignment",
    "missing_revocation_blocks_accountability_assignment",
    "missing_independent_review_blocks_accountability_assignment",
    "collapsed_separation_of_duties_blocks_accountability_assignment",
    "undisposed_conflict_blocks_accountability_assignment",
    "missing_stop_path_blocks_accountability_assignment",
    "missing_appeal_blocks_accountability_assignment",
    "missing_remedy_blocks_accountability_assignment",
    "missing_evidence_access_blocks_accountability_assignment",
    "orphaned_residuals_block_accountability_assignment",
    "missing_non_claim_boundary_blocks_accountability_assignment",
    "accepted_exercise_step_is_accepted",
    "accepted_exercise_step_applies_event",
    "apply_exercise_event_preserves_identity",
    "rejected_exercise_event_preserves_state",
    "accepted_exercise_step_preserves_identity",
    "accepted_exercise_step_preserves_non_authority",
    "accepted_exercise_step_adds_exactly_one_receipt",
    "accepted_exercise_step_advances_stage",
    "apply_exercise_event_contest_count_monotone",
    "apply_exercise_event_remedy_count_monotone",
    "accepted_exercise_run_preserves_identity",
    "accepted_exercise_run_preserves_support",
    "accepted_exercise_run_preserves_external_effect",
    "accepted_exercise_run_accounts_exact_receipts",
    "accepted_exercise_run_contest_count_monotone",
    "accepted_exercise_run_remedy_count_monotone",
    "accepted_exercise_run_has_accepted_trace",
    "exercise_run_append",
    "closed_exercise_state_accepts_no_event",
    "over_ceiling_delegation_cannot_start",
    "authored_exercise_witness_reaches_terminal_record",
    "responsibility_delegation_accepted_step_is_valid",
    "responsibility_delegation_accepted_step_applies_event",
    "responsibility_delegation_step_refines_authority_step",
    "responsibility_delegation_step_assigns_exact_child_owner",
    "responsibility_delegation_step_retains_prior_owner",
    "responsibility_delegation_step_adds_exact_receipt",
    "responsibility_delegation_step_preserves_non_authority",
    "responsibility_delegation_step_preserves_invariant",
    "responsibility_delegation_run_preserves_invariant",
    "responsibility_delegation_run_refines_authority_run",
    "responsibility_delegation_run_has_no_owner_gap",
    "responsibility_delegation_run_accounts_exact_receipts",
    "responsibility_delegation_run_accounts_residual_owners",
    "responsibility_delegation_successful_run_has_valid_trace",
    "responsibility_delegation_run_composes_across_event_batches",
    "responsibility_delegation_initial_state_is_invariant",
    "two_hop_responsibility_delegation_preserves_accountability",
    "responsibility_delegation_closed_countermodels",
    "thin_responsibility_summary_hides_accountability_gap",
    "thin_responsibility_summary_cannot_recover_accountability",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def step(record: dict[str, bool], state: str) -> str:
    if state == "proposed":
        checks = (
            ("assignmentRequested", "refusedNoAssignment"),
            ("decisionIdentityPresent", "repairDecisionIdentity"),
            ("accountableActorPresent", "repairActorIdentity"),
        )
        next_state = "capacityReview"
    elif state == "capacityReview":
        checks = (
            ("informationAvailable", "repairInformation"),
            ("competenceCurrent", "repairCompetence"),
            ("timeAvailable", "repairTime"),
            ("workloadWithinLimit", "repairWorkload"),
        )
        next_state = "authorityReview"
    elif state == "authorityReview":
        checks = (
            ("decisionAuthorityPresent", "repairDecisionAuthority"),
            ("interventionAuthorityPresent", "repairInterventionAuthority"),
            ("practicalAbilityToChange", "repairPracticalControl"),
            ("revocationPathPresent", "repairRevocation"),
        )
        next_state = "independenceReview"
    elif state == "independenceReview":
        checks = (
            ("independentReviewPresent", "repairIndependentReview"),
            ("separationOfDutiesPresent", "repairSeparationOfDuties"),
            ("conflictDispositionPresent", "repairConflictDisposition"),
        )
        next_state = "remedyReview"
    elif state == "remedyReview":
        checks = (
            ("stopPathPresent", "repairStopPath"),
            ("appealPathPresent", "repairAppealPath"),
            ("remedyPathPresent", "repairRemedyPath"),
            ("evidenceAccessPresent", "repairEvidenceAccess"),
            ("residualCustodyPresent", "repairResidualCustody"),
            ("nonClaimBoundaryPresent", "repairNonClaimBoundary"),
        )
        next_state = "accountabilityAssignable"
    else:
        return state
    for field, rejected_state in checks:
        if not record[field]:
            return rejected_state
    return next_state


def run(record: dict[str, bool], steps: int) -> str:
    state = "proposed"
    for _ in range(steps):
        state = step(record, state)
    return state


def exercise_packet() -> dict[str, Any]:
    packet: dict[str, Any] = {
        "decisionDigest": 8001,
        "delegatorDigest": 8002,
        "delegateDigest": 8003,
        "policyDigest": 8004,
        "authorityDigest": 8005,
        "reviewerDigest": 8006,
        "evidenceDigest": 8007,
        "remedyDigest": 8008,
        "resultDigest": 8009,
        "eventDigest": 1,
        "assignmentComplete": True,
        "requestedAuthority": 2,
    }
    for field in (
        "delegationTerms", "expiryPresent", "activationAcknowledgment", "effectObserver",
        "escalationReason", "stopApplied", "independentReview", "handoffAcknowledgment",
        "stateTransfer", "residualTransfer", "contestStanding", "evidenceAccess",
        "appealRecord", "authorityExpiry", "revocationPropagation", "incidentTimeline",
        "effectLedger", "causalUncertainty", "remedyApplied", "remedyObserved",
        "remainingResiduals", "nonClaims", "descendants", "cleanup",
    ):
        packet[field] = True
    packet["supportRequested"] = False
    packet["externalEffectRequested"] = False
    return packet


def exercise_state(stage: str, last_event_digest: int = 0) -> dict[str, Any]:
    packet = exercise_packet()
    return {key: packet[key] for key in EXERCISE_IDENTITY_KEYS} | {
        "stage": stage,
        "lastEventDigest": last_event_digest,
        "authorityCeiling": 3,
        "activeAuthority": 0,
        "receiptCount": 0,
        "contestReceiptCount": 0,
        "remedyReceiptCount": 0,
        "supportAssigned": False,
        "externalEffectCommitted": False,
    }


def exercise_route(
    state: dict[str, Any], kind: str, packet: dict[str, Any]
) -> str:
    stage = state["stage"]
    if kind != EXERCISE_KINDS[stage]:
        return "rejectWrongStage"
    if any(packet[key] != state[key] for key in EXERCISE_IDENTITY_KEYS):
        return "rejectIdentitySubstitution"
    if packet["eventDigest"] == state["lastEventDigest"]:
        return "rejectEventReplay"
    if packet["supportRequested"] or packet["externalEffectRequested"]:
        return "rejectAuthorityLeak"
    checks = {
        "proposed": (
            ("assignmentComplete", "requestCompleteAssignment"),
            ("delegationTerms", "requestDelegationTerms"),
            ("expiryPresent", "requestExpiry"),
        ),
        "delegated": (
            ("activationAcknowledgment", "requestActivationAcknowledgment"),
            ("effectObserver", "requestEffectObserver"),
        ),
        "active": (
            ("escalationReason", "requestEscalationReason"),
            ("stopApplied", "requestStopApplied"),
            ("independentReview", "requestIndependentReview"),
        ),
        "escalated": (
            ("handoffAcknowledgment", "requestHandoffAcknowledgment"),
            ("stateTransfer", "requestStateTransfer"),
            ("residualTransfer", "requestResidualTransfer"),
        ),
        "handedOff": (
            ("contestStanding", "requestContestStanding"),
            ("evidenceAccess", "requestEvidenceAccess"),
            ("appealRecord", "requestAppealRecord"),
        ),
        "contested": (
            ("authorityExpiry", "requestAuthorityExpiry"),
            ("revocationPropagation", "requestRevocationPropagation"),
        ),
        "authorityExpired": (
            ("incidentTimeline", "requestIncidentTimeline"),
            ("effectLedger", "requestEffectLedger"),
            ("causalUncertainty", "requestCausalUncertainty"),
        ),
        "reconstructed": (
            ("remedyApplied", "requestRemedyApplied"),
            ("remedyObserved", "requestRemedyObserved"),
            ("remainingResiduals", "requestRemainingResiduals"),
        ),
        "remedied": (
            ("nonClaims", "requestNonClaims"),
            ("descendants", "requestDescendants"),
            ("cleanup", "requestCleanup"),
        ),
    }
    accepts = {
        "proposed": "acceptDelegation", "delegated": "acceptActivation",
        "active": "acceptEscalation", "escalated": "acceptHandoff",
        "handedOff": "acceptContest", "contested": "acceptExpiry",
        "authorityExpired": "acceptReconstruction", "reconstructed": "acceptRemedy",
        "remedied": "acceptClosure",
    }
    if stage == "closed":
        return "rejectWrongStage"
    if stage == "proposed" and packet["requestedAuthority"] > state["authorityCeiling"]:
        return "blockAuthorityCeiling"
    for field, rejected in checks[stage]:
        if not packet[field]:
            return rejected
    return accepts[stage]


def exercise_step(
    state: dict[str, Any], kind: str, packet: dict[str, Any]
) -> dict[str, Any] | None:
    if state["stage"] == "closed":
        return None
    selected = exercise_route(state, kind, packet)
    if selected not in EXERCISE_ACCEPTED:
        return None
    result = dict(state)
    result["stage"] = NEXT_EXERCISE_STAGE[state["stage"]]
    result["lastEventDigest"] = packet["eventDigest"]
    result["receiptCount"] += 1
    if selected == "acceptDelegation":
        result["activeAuthority"] = packet["requestedAuthority"]
    elif selected == "acceptExpiry":
        result["activeAuthority"] = 0
    if selected == "acceptContest":
        result["contestReceiptCount"] += 1
    if selected == "acceptRemedy":
        result["remedyReceiptCount"] += 1
    return result


def exercise_events() -> list[tuple[str, dict[str, Any]]]:
    events = []
    for index, stage in enumerate(LIVE_EXERCISE_STAGES, start=1):
        packet = exercise_packet()
        packet["eventDigest"] = index
        events.append((EXERCISE_KINDS[stage], packet))
    return events


def exercise_run_states(
    initial: dict[str, Any], events: list[tuple[str, dict[str, Any]]]
) -> list[dict[str, Any]] | None:
    states = [dict(initial)]
    current = dict(initial)
    for kind, packet in events:
        next_state = exercise_step(current, kind, packet)
        if next_state is None:
            return None
        states.append(next_state)
        current = next_state
    return states


def exercise_route_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(
        case_id: str,
        stage: str,
        expected: str,
        mutation: dict[str, Any] | None = None,
        kind: str | None = None,
        last_event_digest: int = 0,
    ) -> None:
        packet = exercise_packet()
        packet.update(mutation or {})
        actual = exercise_route(
            exercise_state(stage, last_event_digest),
            kind or EXERCISE_KINDS[stage],
            packet,
        )
        rows.append({"case_id": case_id, "expected": expected, "actual": actual})

    add("wrong-stage", "proposed", "rejectWrongStage", kind="activateWork")
    add("identity-substitution", "proposed", "rejectIdentitySubstitution", {"decisionDigest": 999})
    add("event-replay", "proposed", "rejectEventReplay", last_event_digest=1)
    add("authority-leak", "proposed", "rejectAuthorityLeak", {"supportRequested": True})
    stage_checks = {
        "proposed": (
            ("assignmentComplete", "requestCompleteAssignment"),
            ("delegationTerms", "requestDelegationTerms"),
            ("requestedAuthority", "blockAuthorityCeiling"),
            ("expiryPresent", "requestExpiry"),
        ),
        "delegated": (("activationAcknowledgment", "requestActivationAcknowledgment"), ("effectObserver", "requestEffectObserver")),
        "active": (("escalationReason", "requestEscalationReason"), ("stopApplied", "requestStopApplied"), ("independentReview", "requestIndependentReview")),
        "escalated": (("handoffAcknowledgment", "requestHandoffAcknowledgment"), ("stateTransfer", "requestStateTransfer"), ("residualTransfer", "requestResidualTransfer")),
        "handedOff": (("contestStanding", "requestContestStanding"), ("evidenceAccess", "requestEvidenceAccess"), ("appealRecord", "requestAppealRecord")),
        "contested": (("authorityExpiry", "requestAuthorityExpiry"), ("revocationPropagation", "requestRevocationPropagation")),
        "authorityExpired": (("incidentTimeline", "requestIncidentTimeline"), ("effectLedger", "requestEffectLedger"), ("causalUncertainty", "requestCausalUncertainty")),
        "reconstructed": (("remedyApplied", "requestRemedyApplied"), ("remedyObserved", "requestRemedyObserved"), ("remainingResiduals", "requestRemainingResiduals")),
        "remedied": (("nonClaims", "requestNonClaims"), ("descendants", "requestDescendants"), ("cleanup", "requestCleanup")),
    }
    accepts = {
        "proposed": "acceptDelegation", "delegated": "acceptActivation",
        "active": "acceptEscalation", "escalated": "acceptHandoff",
        "handedOff": "acceptContest", "contested": "acceptExpiry",
        "authorityExpired": "acceptReconstruction", "reconstructed": "acceptRemedy",
        "remedied": "acceptClosure",
    }
    for stage, checks in stage_checks.items():
        for field, expected in checks:
            value = 4 if field == "requestedAuthority" else False
            add(f"{stage}-{field}", stage, expected, {field: value})
        add(f"{stage}-accepted", stage, accepts[stage])
    return rows


def exercise_mutations() -> list[dict[str, Any]]:
    receipts = [
        {"mutation_id": f"route:{row['case_id']}", "rejected": True}
        for row in exercise_route_cases()
        if row["actual"] not in EXERCISE_ACCEPTED
    ]
    for index, stage in enumerate(LIVE_EXERCISE_STAGES):
        for key in EXERCISE_IDENTITY_KEYS:
            packet = exercise_packet()
            packet["eventDigest"] = 100 + index
            packet[key] = 999999
            receipts.append({
                "mutation_id": f"identity:{stage}:{key}",
                "rejected": exercise_step(exercise_state(stage), EXERCISE_KINDS[stage], packet) is None,
            })
        wrong_kind = EXERCISE_KINDS[LIVE_EXERCISE_STAGES[(index + 1) % len(LIVE_EXERCISE_STAGES)]]
        packet = exercise_packet()
        packet["eventDigest"] = 200 + index
        receipts.append({"mutation_id": f"wrong-kind:{stage}", "rejected": exercise_step(exercise_state(stage), wrong_kind, packet) is None})
        packet = exercise_packet()
        packet["eventDigest"] = 300 + index
        receipts.append({"mutation_id": f"replay:{stage}", "rejected": exercise_step(exercise_state(stage, packet["eventDigest"]), EXERCISE_KINDS[stage], packet) is None})
        packet = exercise_packet()
        packet["eventDigest"] = 400 + index
        packet["supportRequested"] = True
        receipts.append({"mutation_id": f"support:{stage}", "rejected": exercise_step(exercise_state(stage), EXERCISE_KINDS[stage], packet) is None})
        packet = exercise_packet()
        packet["eventDigest"] = 500 + index
        packet["externalEffectRequested"] = True
        receipts.append({"mutation_id": f"effect:{stage}", "rejected": exercise_step(exercise_state(stage), EXERCISE_KINDS[stage], packet) is None})
    closed = exercise_state("closed")
    for index, kind in enumerate(EXERCISE_KINDS[stage] for stage in LIVE_EXERCISE_STAGES):
        packet = exercise_packet()
        packet["eventDigest"] = 600 + index
        receipts.append({"mutation_id": f"terminal:{kind}", "rejected": exercise_step(closed, kind, packet) is None})
    return receipts


def authority_delegation_state() -> dict[str, Any]:
    return {
        "rootGrantId": 100,
        "rootPrincipalId": 1,
        "operationId": 10,
        "targetId": 20,
        "scopeId": 30,
        "rootCeiling": 5,
        "rootEpoch": 7,
        "rootExpiresAt": 100,
        "currentGrantId": 100,
        "currentPrincipalId": 1,
        "currentDelegateId": 2,
        "currentCeiling": 4,
        "currentEpoch": 7,
        "currentExpiresAt": 90,
        "logicalTime": 0,
        "revokedGrantIds": [99],
        "depth": 0,
        "receiptCount": 0,
        "supportAuthority": False,
        "externalEffectAuthority": False,
    }


def authority_delegation_event(second: bool = False) -> dict[str, Any]:
    if second:
        return {
            "parentGrantId": 101,
            "childGrantId": 102,
            "actingPrincipalId": 3,
            "childDelegateId": 4,
            "operationId": 10,
            "targetId": 20,
            "scopeId": 30,
            "childCeiling": 1,
            "epoch": 7,
            "expiresAt": 70,
            "logicalTime": 20,
            "delegationReceipt": True,
            "supportPromotionRequested": False,
            "externalEffectRequested": False,
        }
    return {
        "parentGrantId": 100,
        "childGrantId": 101,
        "actingPrincipalId": 2,
        "childDelegateId": 3,
        "operationId": 10,
        "targetId": 20,
        "scopeId": 30,
        "childCeiling": 3,
        "epoch": 7,
        "expiresAt": 80,
        "logicalTime": 10,
        "delegationReceipt": True,
        "supportPromotionRequested": False,
        "externalEffectRequested": False,
    }


def authority_delegation_valid(
    state: dict[str, Any], event: dict[str, Any]
) -> bool:
    return (
        event["parentGrantId"] == state["currentGrantId"]
        and event["actingPrincipalId"] == state["currentDelegateId"]
        and event["childGrantId"] > 0
        and event["childGrantId"] != state["currentGrantId"]
        and event["childGrantId"] not in state["revokedGrantIds"]
        and event["childDelegateId"] > 0
        and event["operationId"] == state["operationId"]
        and event["targetId"] == state["targetId"]
        and event["scopeId"] == state["scopeId"]
        and event["childCeiling"] <= state["currentCeiling"]
        and event["epoch"] == state["currentEpoch"]
        and event["expiresAt"] <= state["currentExpiresAt"]
        and state["logicalTime"] < event["logicalTime"]
        and event["logicalTime"] <= event["expiresAt"]
        and event["delegationReceipt"] is True
        and event["supportPromotionRequested"] is False
        and event["externalEffectRequested"] is False
    )


def apply_authority_delegation(
    state: dict[str, Any], event: dict[str, Any]
) -> dict[str, Any]:
    result = copy.deepcopy(state)
    result.update({
        "currentGrantId": event["childGrantId"],
        "currentPrincipalId": event["actingPrincipalId"],
        "currentDelegateId": event["childDelegateId"],
        "currentCeiling": event["childCeiling"],
        "currentEpoch": event["epoch"],
        "currentExpiresAt": event["expiresAt"],
        "logicalTime": event["logicalTime"],
        "depth": state["depth"] + 1,
        "receiptCount": state["receiptCount"] + 1,
    })
    return result


def authority_delegation_invariant(state: dict[str, Any]) -> bool:
    return (
        state["rootGrantId"] > 0
        and state["rootPrincipalId"] > 0
        and state["currentGrantId"] > 0
        and state["currentPrincipalId"] > 0
        and state["currentDelegateId"] > 0
        and state["currentCeiling"] <= state["rootCeiling"]
        and state["currentEpoch"] == state["rootEpoch"]
        and state["currentExpiresAt"] <= state["rootExpiresAt"]
        and state["logicalTime"] <= state["currentExpiresAt"]
        and state["currentGrantId"] not in state["revokedGrantIds"]
        and state["supportAuthority"] is False
        and state["externalEffectAuthority"] is False
    )


def responsibility_delegation_state() -> dict[str, Any]:
    return {
        "authorityState": authority_delegation_state(),
        "accountableOwnerId": 2,
        "reviewerId": 50,
        "evidenceCustodianId": 60,
        "residualOwnerIds": [],
        "responsibilityReceiptCount": 0,
        "assignmentComplete": True,
        "interventionPathPresent": True,
        "appealPathPresent": True,
        "remedyPathPresent": True,
        "supportAssigned": False,
        "externalEffectCommitted": False,
    }


def responsibility_delegation_event(second: bool = False) -> dict[str, Any]:
    return {
        "authorityEvent": authority_delegation_event(second),
        "transferringOwnerId": 3 if second else 2,
        "nextAccountableOwnerId": 4 if second else 3,
        "reviewerId": 52 if second else 51,
        "evidenceCustodianId": 62 if second else 61,
        "assignment": dict(BASE_RECORD),
        "handoffAcknowledgment": True,
        "interventionPathTransferred": True,
        "evidenceCustodyTransferred": True,
        "appealPathTransferred": True,
        "remedyPathTransferred": True,
        "residualCustodyAcknowledged": True,
        "supportRequested": False,
        "externalEffectRequested": False,
    }


def responsibility_delegation_valid(
    state: dict[str, Any], event: dict[str, Any]
) -> bool:
    authority_event = event["authorityEvent"]
    return (
        state["accountableOwnerId"] == state["authorityState"]["currentDelegateId"]
        and event["transferringOwnerId"] == state["accountableOwnerId"]
        and authority_delegation_valid(state["authorityState"], authority_event)
        and event["nextAccountableOwnerId"] == authority_event["childDelegateId"]
        and event["nextAccountableOwnerId"] > 0
        and event["reviewerId"] > 0
        and event["reviewerId"] != authority_event["actingPrincipalId"]
        and event["reviewerId"] != event["nextAccountableOwnerId"]
        and event["evidenceCustodianId"] > 0
        and event["evidenceCustodianId"] != event["nextAccountableOwnerId"]
        and all(event["assignment"].values())
        and event["handoffAcknowledgment"] is True
        and event["interventionPathTransferred"] is True
        and event["evidenceCustodyTransferred"] is True
        and event["appealPathTransferred"] is True
        and event["remedyPathTransferred"] is True
        and event["residualCustodyAcknowledged"] is True
        and event["supportRequested"] is False
        and event["externalEffectRequested"] is False
    )


def responsibility_delegation_step(
    state: dict[str, Any], event: dict[str, Any]
) -> dict[str, Any] | None:
    if not responsibility_delegation_valid(state, event):
        return None
    result = copy.deepcopy(state)
    result.update({
        "authorityState": apply_authority_delegation(
            state["authorityState"], event["authorityEvent"]
        ),
        "accountableOwnerId": event["nextAccountableOwnerId"],
        "reviewerId": event["reviewerId"],
        "evidenceCustodianId": event["evidenceCustodianId"],
        "residualOwnerIds": [state["accountableOwnerId"], *state["residualOwnerIds"]],
        "responsibilityReceiptCount": state["responsibilityReceiptCount"] + 1,
        "assignmentComplete": True,
        "interventionPathPresent": True,
        "appealPathPresent": True,
        "remedyPathPresent": True,
    })
    return result


def responsibility_delegation_invariant(state: dict[str, Any]) -> bool:
    authority = state["authorityState"]
    return (
        authority_delegation_invariant(authority)
        and state["accountableOwnerId"] == authority["currentDelegateId"]
        and state["accountableOwnerId"] > 0
        and state["reviewerId"] > 0
        and state["reviewerId"] != state["accountableOwnerId"]
        and state["reviewerId"] != authority["currentPrincipalId"]
        and state["evidenceCustodianId"] > 0
        and state["evidenceCustodianId"] != state["accountableOwnerId"]
        and state["responsibilityReceiptCount"] == authority["receiptCount"]
        and len(state["residualOwnerIds"]) == authority["depth"]
        and state["assignmentComplete"] is True
        and state["interventionPathPresent"] is True
        and state["appealPathPresent"] is True
        and state["remedyPathPresent"] is True
        and state["supportAssigned"] is False
        and state["externalEffectCommitted"] is False
    )


def responsibility_delegation_run_states(
    initial: dict[str, Any], events: list[dict[str, Any]]
) -> list[dict[str, Any]] | None:
    states = [copy.deepcopy(initial)]
    current = copy.deepcopy(initial)
    for event in events:
        next_state = responsibility_delegation_step(current, event)
        if next_state is None:
            return None
        states.append(next_state)
        current = next_state
    return states


def responsibility_bridge_mutations() -> list[dict[str, Any]]:
    initial = responsibility_delegation_state()
    mutations: list[tuple[str, dict[str, Any]]] = []

    authority_mutations = (
        ("parent-grant", "parentGrantId", 999),
        ("child-grant-reuse", "childGrantId", 100),
        ("child-grant-revoked", "childGrantId", 99),
        ("child-grant-zero", "childGrantId", 0),
        ("acting-principal", "actingPrincipalId", 999),
        ("child-delegate-zero", "childDelegateId", 0),
        ("operation", "operationId", 999),
        ("target", "targetId", 999),
        ("scope", "scopeId", 999),
        ("ceiling-widening", "childCeiling", 5),
        ("stale-epoch", "epoch", 8),
        ("expiry-widening", "expiresAt", 91),
        ("nonmonotone-time", "logicalTime", 0),
        ("time-after-expiry", "logicalTime", 81),
        ("missing-delegation-receipt", "delegationReceipt", False),
        ("authority-support-request", "supportPromotionRequested", True),
        ("authority-effect-request", "externalEffectRequested", True),
    )
    for label, field, value in authority_mutations:
        event = responsibility_delegation_event()
        event["authorityEvent"][field] = value
        mutations.append((f"authority:{label}", event))

    responsibility_mutations = (
        ("transferring-owner", "transferringOwnerId", 99),
        ("next-owner", "nextAccountableOwnerId", 99),
        ("reviewer-is-principal", "reviewerId", 2),
        ("reviewer-is-child", "reviewerId", 3),
        ("custodian-is-child", "evidenceCustodianId", 3),
        ("handoff-ack", "handoffAcknowledgment", False),
        ("intervention-transfer", "interventionPathTransferred", False),
        ("evidence-transfer", "evidenceCustodyTransferred", False),
        ("appeal-transfer", "appealPathTransferred", False),
        ("remedy-transfer", "remedyPathTransferred", False),
        ("residual-ack", "residualCustodyAcknowledged", False),
        ("support-request", "supportRequested", True),
        ("effect-request", "externalEffectRequested", True),
    )
    for label, field, value in responsibility_mutations:
        event = responsibility_delegation_event()
        event[field] = value
        mutations.append((f"responsibility:{label}", event))

    for field in BASE_RECORD:
        event = responsibility_delegation_event()
        event["assignment"][field] = False
        mutations.append((f"assignment:{field}", event))

    receipts = []
    for label, event in mutations:
        before = copy.deepcopy(initial)
        rejected = responsibility_delegation_step(initial, event) is None
        receipts.append({
            "mutation_id": label,
            "rejected": rejected,
            "state_noninterference": initial == before,
        })
    return receipts


def thin_responsibility_summary(state: dict[str, Any]) -> tuple[int, int, int, int]:
    authority = state["authorityState"]
    return (
        authority["depth"],
        state["responsibilityReceiptCount"],
        authority["currentCeiling"],
        len(state["residualOwnerIds"]),
    )


def responsibility_assignable(state: dict[str, Any]) -> bool:
    return (
        state["accountableOwnerId"] > 0
        and state["reviewerId"] > 0
        and state["reviewerId"] != state["accountableOwnerId"]
        and state["evidenceCustodianId"] > 0
        and state["evidenceCustodianId"] != state["accountableOwnerId"]
    )


def fail(errors: list[str]) -> None:
    if errors:
        raise SystemExit("Human-AI organization accountability validation failed:\n" + "\n".join(f" - {e}" for e in errors))


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, LEAN_ROOT, CHAPTER, DOSSIER, MANIFEST, TRIAGE, STRUCTURE, OUTLINE, BRIDGE_FIXTURE):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    fail(errors)

    expected_stages = [
        "proposed",
        "capacityReview",
        "authorityReview",
        "independenceReview",
        "remedyReview",
        "accountabilityAssignable",
    ]
    observed_stages = [run(BASE_RECORD, steps) for steps in range(6)]
    if observed_stages != expected_stages:
        errors.append(f"complete route mismatch: {observed_stages}")
    if not all(BASE_RECORD.values()):
        errors.append("complete record must contain twenty true fields")
    if len(BASE_RECORD) != 20 or set(BASE_RECORD) != set(EXPECTED_MUTATIONS):
        errors.append("independent mutation denominator must cover all twenty record fields")
    for field, expected in EXPECTED_MUTATIONS.items():
        mutated = dict(BASE_RECORD)
        mutated[field] = False
        actual = run(mutated, 5)
        if actual != expected:
            errors.append(f"mutation {field} reached {actual}, expected {expected}")
        if step(mutated, actual) != actual:
            errors.append(f"mutation {field} did not remain blocked after rejection")

    route_rows = exercise_route_cases()
    reached_routes = {row["actual"] for row in route_rows}
    if len(route_rows) != 39 or len(reached_routes) != 39:
        errors.append(f"exercise route coverage drifted: {len(route_rows)}/{len(reached_routes)}")
    for row in route_rows:
        if row["actual"] != row["expected"]:
            errors.append(
                f"exercise route {row['case_id']} reached {row['actual']}, expected {row['expected']}"
            )

    initial_exercise = exercise_state("proposed")
    events = exercise_events()
    states = exercise_run_states(initial_exercise, events)
    if states is None:
        errors.append("complete accountability exercise failed")
    else:
        expected_final = {
            "stage": "closed",
            "activeAuthority": 0,
            "receiptCount": 9,
            "contestReceiptCount": 1,
            "remedyReceiptCount": 1,
            "supportAssigned": False,
            "externalEffectCommitted": False,
        }
        for key, value in expected_final.items():
            if states[-1][key] != value:
                errors.append(f"exercise terminal witness drifted: {key}")
        if sum(all(row[key] == initial_exercise[key] for key in EXERCISE_IDENTITY_KEYS) for row in states) != 10:
            errors.append("exercise identity custody drifted")
        if sum(not row["supportAssigned"] and not row["externalEffectCommitted"] for row in states) != 10:
            errors.append("exercise non-authority custody drifted")
        if sum(left["contestReceiptCount"] <= right["contestReceiptCount"] for left, right in zip(states, states[1:])) != 9:
            errors.append("exercise contest monotonicity drifted")
        if sum(left["remedyReceiptCount"] <= right["remedyReceiptCount"] for left, right in zip(states, states[1:])) != 9:
            errors.append("exercise remedy monotonicity drifted")
        split_count = 0
        for split in range(len(events) + 1):
            prefix = exercise_run_states(initial_exercise, events[:split])
            if prefix is None:
                errors.append(f"exercise trace prefix {split} failed")
                continue
            suffix = exercise_run_states(prefix[-1], events[split:])
            if suffix is None or suffix[-1] != states[-1]:
                errors.append(f"exercise trace composition split {split} failed")
            split_count += 1
        if split_count != 10:
            errors.append(f"exercise trace split denominator drifted: {split_count}")

    mutation_receipts = exercise_mutations()
    if len(mutation_receipts) != 156 or not all(row["rejected"] for row in mutation_receipts):
        errors.append(
            f"exercise mutation coverage drifted: "
            f"{sum(row['rejected'] for row in mutation_receipts)}/{len(mutation_receipts)}"
        )

    bridge_fixture = load(BRIDGE_FIXTURE)
    if (
        bridge_fixture.get("schema_version")
        != "asi_stack.human_ai_org_responsibility_bridge.v1"
        or bridge_fixture.get("support_state_effect") != "none"
        or bridge_fixture.get("assignment_complete_fields") != list(BASE_RECORD)
    ):
        errors.append("responsibility bridge fixture identity or assignment profile drifted")
    responsibility_initial = bridge_fixture["initial_state"]
    bridge_events = copy.deepcopy(bridge_fixture["events"])
    for event in bridge_events:
        if event.pop("assignment_profile", None) != "complete":
            errors.append("responsibility bridge fixture has an unknown assignment profile")
        event["assignment"] = dict(BASE_RECORD)
    if responsibility_initial != responsibility_delegation_state() or bridge_events != [
        responsibility_delegation_event(),
        responsibility_delegation_event(second=True),
    ]:
        errors.append("responsibility bridge fixture no longer matches the independent model")
    if not responsibility_delegation_invariant(responsibility_initial):
        errors.append("initial responsibility-delegation invariant failed")
    bridge_states = responsibility_delegation_run_states(
        responsibility_initial, bridge_events
    )
    if bridge_states is None:
        errors.append("two-hop responsibility-delegation witness failed")
    else:
        if len(bridge_states) != 3 or not all(
            responsibility_delegation_invariant(row) for row in bridge_states
        ):
            errors.append("responsibility-delegation invariant drifted across two hops")
        expected_bridge_final = bridge_fixture["expected_final"]
        for key, value in {
            "accountableOwnerId": expected_bridge_final["accountableOwnerId"],
            "residualOwnerIds": expected_bridge_final["residualOwnerIds"],
            "responsibilityReceiptCount": expected_bridge_final["responsibilityReceiptCount"],
            "supportAssigned": expected_bridge_final["supportAssigned"],
            "externalEffectCommitted": expected_bridge_final["externalEffectCommitted"],
        }.items():
            if bridge_states[-1][key] != value:
                errors.append(f"responsibility-delegation witness drifted: {key}")
        expected_authority_final = {
            "currentDelegateId": expected_bridge_final["currentDelegateId"],
            "currentCeiling": expected_bridge_final["currentCeiling"],
            "depth": len(bridge_events),
            "receiptCount": expected_bridge_final["authorityReceiptCount"],
        }
        for key, value in expected_authority_final.items():
            if bridge_states[-1]["authorityState"][key] != value:
                errors.append(f"authority projection witness drifted: {key}")

        authority_projection = copy.deepcopy(
            responsibility_initial["authorityState"]
        )
        for event in bridge_events:
            authority_projection = apply_authority_delegation(
                authority_projection, event["authorityEvent"]
            )
        if bridge_states[-1]["authorityState"] != authority_projection:
            errors.append("responsibility run does not refine the authority run")

        composition_count = 0
        for split in range(len(bridge_events) + 1):
            prefix = responsibility_delegation_run_states(
                responsibility_initial, bridge_events[:split]
            )
            if prefix is None:
                errors.append(f"responsibility bridge prefix {split} failed")
                continue
            suffix = responsibility_delegation_run_states(
                prefix[-1], bridge_events[split:]
            )
            if suffix is None or suffix[-1] != bridge_states[-1]:
                errors.append(f"responsibility bridge composition split {split} failed")
            composition_count += 1
        if composition_count != bridge_fixture["expected_composition_count"]:
            errors.append(
                f"responsibility bridge composition denominator drifted: {composition_count}"
            )

        for previous, current in zip(bridge_states, bridge_states[1:]):
            if current["residualOwnerIds"] != [
                previous["accountableOwnerId"],
                *previous["residualOwnerIds"],
            ]:
                errors.append("responsibility bridge lost prior-owner residual custody")
            if current["responsibilityReceiptCount"] != (
                previous["responsibilityReceiptCount"] + 1
            ):
                errors.append("responsibility bridge did not add exactly one receipt")
            if current["accountableOwnerId"] != current["authorityState"]["currentDelegateId"]:
                errors.append("responsibility bridge introduced an owner gap")

    bridge_mutation_receipts = responsibility_bridge_mutations()
    rejected_bridge_mutations = sum(
        row["rejected"] for row in bridge_mutation_receipts
    )
    noninterfering_bridge_mutations = sum(
        row["state_noninterference"] for row in bridge_mutation_receipts
    )
    expected_bridge_mutations = bridge_fixture["expected_bridge_mutation_count"]
    if len(bridge_mutation_receipts) != expected_bridge_mutations or rejected_bridge_mutations != expected_bridge_mutations:
        errors.append(
            "responsibility bridge mutation coverage drifted: "
            f"{rejected_bridge_mutations}/{len(bridge_mutation_receipts)}"
        )
    if noninterfering_bridge_mutations != expected_bridge_mutations:
        errors.append(
            "rejected responsibility bridge mutations changed state: "
            f"{noninterfering_bridge_mutations}/{expected_bridge_mutations}"
        )

    accountability_gap = copy.deepcopy(responsibility_initial)
    collision = bridge_fixture["summary_collision"]
    accountability_gap.update(collision["gap_updates"])
    if list(thin_responsibility_summary(responsibility_initial)) != collision["summary"]:
        errors.append("responsibility bridge fixture summary drifted")
    if thin_responsibility_summary(responsibility_initial) != thin_responsibility_summary(accountability_gap):
        errors.append("thin responsibility summaries did not collide")
    if (
        responsibility_assignable(responsibility_initial) is not collision["safe_assignable"]
        or responsibility_assignable(accountability_gap) is not collision["gap_assignable"]
    ):
        errors.append("accountability-gap witness decisions drifted")
    for constant_classifier in (False, True):
        safe_decision = constant_classifier
        gap_decision = constant_classifier
        if safe_decision is True and gap_decision is False:
            errors.append("constant thin-summary classifier distinguished a collision")

    lean_text = LEAN.read_text(encoding="utf-8")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if theorem_names != REQUIRED_THEOREMS:
        errors.append(
            f"Lean theorem surface mismatch: missing={sorted(REQUIRED_THEOREMS - theorem_names)}, "
            f"extra={sorted(theorem_names - REQUIRED_THEOREMS)}"
        )
    if "import AsiStackProofs.HumanAIOrganizations" not in LEAN_ROOT.read_text(encoding="utf-8"):
        errors.append("root Lean module does not import HumanAIOrganizations")
    for forbidden in (
        "legalAccountabilityEstablished",
        "organizationalEffectivenessEstablished",
        "humanControlEstablished",
        "supportStatePromoted",
        "externalEffectAllowed",
    ):
        if forbidden in lean_text:
            errors.append(f"forbidden overclaim surface present: {forbidden}")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or len(triage_rows) != 1:
        errors.append("proof manifest and triage must each contain exactly one target row")
    else:
        manifest_row = manifest_rows[0]
        triage_row = triage_rows[0]
        if (manifest_row.get("module"), manifest_row.get("formal_target"), manifest_row.get("status")) != (
            MODULE,
            FORMAL_TARGET,
            "implemented",
        ):
            errors.append("proof manifest target binding drifted")
        if (triage_row.get("module"), triage_row.get("formal_target"), triage_row.get("target_status")) != (
            MODULE,
            FORMAL_TARGET,
            "implemented",
        ):
            errors.append("proof triage target binding drifted")

    chapters = [chapter for part in load(STRUCTURE)["parts"] for chapter in part.get("chapters", [])]
    chapter_rows = [row for row in chapters if row.get("id") == "human-ai-organizations-delegation-and-accountability"]
    if len(chapter_rows) != 1:
        errors.append("book structure must contain exactly one owner chapter")
    else:
        targets = chapter_rows[0].get("proof_targets", [])
        if not any(row.get("tag") == TAG and row.get("status") == "implemented" for row in targets):
            errors.append("book structure target is not implemented")

    chapter_text = CHAPTER.read_text(encoding="utf-8")
    dossier_text = DOSSIER.read_text(encoding="utf-8")
    outline_text = OUTLINE.read_text(encoding="utf-8")
    for fragment in (
        TAG,
        "62 theorem declarations",
        "20 closed mutations",
        "156/156 lifecycle mutations",
        "50/50 bridge mutations",
        "three bridge compositions",
        "aggregate delegation summary",
        "does not prove",
        "remains `argument`",
    ):
        if fragment not in chapter_text:
            errors.append(f"chapter missing boundary fragment: {fragment}")
    for fragment in (
        "five-stage finite review",
        "twenty closed",
        "ten-stage delegation-to-remedy lifecycle",
        "156/156 lifecycle mutations",
        "50/50 bridge mutations",
        "aggregate delegation summary",
        "support_state_effect` remains `none",
    ):
        if fragment not in dossier_text:
            errors.append(f"proof-model dossier missing fragment: {fragment}")
    if f"| `{TAG}` | `{MODULE}` | {FORMAL_TARGET} | implemented |" not in outline_text:
        errors.append("outline target row drifted")

    fail(errors)
    print(
        "Human-AI organization accountability validation passed: five reachable review stages, "
        "one complete assignment route, 20/20 independent field mutations, a ten-stage "
        "delegation-to-remedy lifecycle, 10 trace splits, 39 routes, 156/156 lifecycle mutations, "
        "a two-hop authority/accountability bridge, three bridge compositions, 50/50 bridge "
        "mutations with state noninterference, one aggregate-summary collision, and 62 exact "
        "Lean declarations; "
        "no human-control, legal-accountability, organizational-outcome, support, or external-effect claim."
    )


if __name__ == "__main__":
    main()

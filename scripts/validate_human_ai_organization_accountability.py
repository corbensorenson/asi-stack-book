#!/usr/bin/env python3
from __future__ import annotations

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

TAG = "lean:human_ai_org.accountability_requires_authority"
MODULE = "AsiStackProofs.HumanAIOrganizations"
FORMAL_TARGET = (
    "A five-stage finite review preserves staged capacity, authority, independence, and remedy "
    "invariants over arbitrary run length; assignable accountability requires all 20 authored "
    "fields, while 20 closed mutations reach exact repair states. A separate ten-stage "
    "delegation-to-remedy lifecycle proves arbitrary-run nine-field identity custody, support/effect "
    "non-authority, exact receipts, contest/remedy monotonicity, accepted traces, batch composition, "
    "absorbing closure, and one bounded adverse-path witness; an independent consumer reaches all "
    "39 routes and rejects 156/156 lifecycle mutations. It establishes no field truth, lawful "
    "accountability, human control, organizational outcome, support, or external effect."
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


def fail(errors: list[str]) -> None:
    if errors:
        raise SystemExit("Human-AI organization accountability validation failed:\n" + "\n".join(f" - {e}" for e in errors))


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, LEAN_ROOT, CHAPTER, DOSSIER, MANIFEST, TRIAGE, STRUCTURE, OUTLINE):
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
        "42 theorem declarations",
        "20 closed mutations",
        "156/156 lifecycle mutations",
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
        "and 42 exact Lean declarations; "
        "no human-control, legal-accountability, organizational-outcome, support, or external-effect claim."
    )


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Validate the projection-aware, non-aggregating evidence-transition lifecycle."""

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
LEAN = ROOT / "lean/AsiStackProofs/EvidenceTransitionRefinement.lean"
SCHEMA = ROOT / "schemas/evidence_transition_refinement.schema.json"
RESULT = ROOT / "experiments/evidence_transition_refinement/results/2026-07-26-local.json"
COMMAND = "python3 scripts/validate_evidence_transition_refinement.py"

KINDS = {
    "requested": "freezeProjections",
    "projectionsFrozen": "bindEvidence",
    "evidenceBound": "recordReview",
    "reviewed": "decide",
    "decided": "handOff",
    "handedOff": "acknowledge",
}
ACCEPTED = {
    "acceptProjectionFreeze",
    "acceptEvidenceBinding",
    "acceptReview",
    "acceptDecision",
    "acceptHandoff",
    "acceptAcknowledgment",
}


def packet() -> dict[str, Any]:
    return {
        "atom": "claim:asi-stack:evidence-transition",
        "proposition": "sha256:proposition-v3",
        "obligation": "sha256:obligation-v2",
        "predicate": "sha256:predicate-v4",
        "current_state": "argument",
        "proposed_state": "syntheticTestBacked",
        "intent": "promote",
        "event": "event:111",
        "scope": True,
        "assumptions": True,
        "non_claims": True,
        "dependencies": True,
        "evidence_refs": True,
        "evidence_roles": True,
        "artifact_bindings": True,
        "source_grounding": True,
        "prototype_inspection": True,
        "synthetic_validation": True,
        "empirical_validation": True,
        "external_literature": True,
        "negative_evidence": True,
        "downgrade_trigger": True,
        "supersession_lineage": True,
        "independent_review": True,
        "projection_alignment": True,
        "dissent": True,
        "limitations": True,
        "residuals": True,
        "changelog": True,
        "ledger_handoff": True,
        "acknowledgment": True,
        "support_assignment_requested": False,
        "external_effect_requested": False,
        "parent_movement_requested": False,
        "descendant_movement_requested": False,
    }


def state(stage: str, *, event: str = "event:0") -> dict[str, Any]:
    p = packet()
    return {
        "stage": stage,
        "atom": p["atom"],
        "proposition": p["proposition"],
        "obligation": p["obligation"],
        "predicate": p["predicate"],
        "current_state": p["current_state"],
        "last_event": event,
    }


def state_category_matches(p: dict[str, Any]) -> bool:
    if p["intent"] == "deprecate":
        return p["proposed_state"] == "deprecated"
    if p["intent"] == "refute":
        return p["proposed_state"] == "refuted"
    return p["proposed_state"] not in {"deprecated", "refuted"}


def evidence_for_target(p: dict[str, Any]) -> bool:
    fields = {
        "sourceDerived": "source_grounding",
        "prototypeBacked": "prototype_inspection",
        "syntheticTestBacked": "synthetic_validation",
        "empiricalTestBacked": "empirical_validation",
        "externalLiteratureBacked": "external_literature",
        "deprecated": "negative_evidence",
        "refuted": "negative_evidence",
    }
    field = fields.get(p["proposed_state"])
    return True if field is None else bool(p[field])


def route(stage: str, kind: str, p: dict[str, Any], s: dict[str, Any]) -> str:
    if kind != KINDS[stage]:
        return "rejectWrongStage"
    if p["atom"] != s["atom"]:
        return "rejectAtomSubstitution"
    if any(p[key] != s[key] for key in ("proposition", "obligation", "predicate")):
        return "rejectProjectionSubstitution"
    if p["current_state"] != s["current_state"]:
        return "rejectStateCategorySubstitution"
    if p["event"] == s["last_event"]:
        return "rejectEventReplay"
    if any(
        p[key]
        for key in (
            "support_assignment_requested",
            "external_effect_requested",
            "parent_movement_requested",
            "descendant_movement_requested",
        )
    ):
        return "rejectAuthorityLeak"
    if not state_category_matches(p):
        return "rejectStateCategorySubstitution"
    if stage == "requested":
        for field, outcome in (
            ("scope", "requestScope"),
            ("assumptions", "requestAssumptions"),
            ("non_claims", "requestNonClaims"),
            ("dependencies", "requestDependencies"),
        ):
            if not p[field]:
                return outcome
        return "acceptProjectionFreeze"
    if stage == "projectionsFrozen":
        for field, outcome in (
            ("evidence_refs", "requestEvidenceRefs"),
            ("evidence_roles", "requestEvidenceRoles"),
            ("artifact_bindings", "requestArtifactBindings"),
        ):
            if not p[field]:
                return outcome
        if not evidence_for_target(p):
            return {
                "sourceDerived": "requestSourceGrounding",
                "prototypeBacked": "requestPrototypeInspection",
                "syntheticTestBacked": "requestSyntheticValidation",
                "empiricalTestBacked": "requestEmpiricalValidation",
                "externalLiteratureBacked": "requestExternalLiterature",
                "deprecated": "requestNegativeEvidence",
                "refuted": "requestNegativeEvidence",
            }[p["proposed_state"]]
        if p["intent"] in {"narrow", "downgrade", "deprecate", "refute"}:
            for field, outcome in (
                ("negative_evidence", "requestNegativeEvidence"),
                ("downgrade_trigger", "requestDowngradeTrigger"),
                ("supersession_lineage", "requestSupersessionLineage"),
            ):
                if not p[field]:
                    return outcome
        return "acceptEvidenceBinding"
    if stage == "evidenceBound":
        for field, outcome in (
            ("independent_review", "requestIndependentReview"),
            ("projection_alignment", "requestProjectionAlignment"),
            ("dissent", "requestDissent"),
        ):
            if not p[field]:
                return outcome
        return "acceptReview"
    if stage == "reviewed":
        for field, outcome in (
            ("limitations", "requestLimitations"),
            ("residuals", "requestResiduals"),
            ("changelog", "requestChangelog"),
        ):
            if not p[field]:
                return outcome
        return "acceptDecision"
    if stage == "decided":
        return "acceptHandoff" if p["ledger_handoff"] else "requestLedgerHandoff"
    return "acceptAcknowledgment" if p["acknowledgment"] else "requestAcknowledgment"


def route_cases() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    def add(
        case_id: str,
        stage: str,
        expected: str,
        mutation: dict[str, Any] | None = None,
        *,
        kind: str | None = None,
        last_event: str = "event:0",
    ) -> None:
        p = packet()
        p.update(mutation or {})
        actual = route(stage, kind or KINDS[stage], p, state(stage, event=last_event))
        rows.append(
            {
                "case_id": case_id,
                "stage": stage,
                "expected_route": expected,
                "actual_route": actual,
                "accepted": actual in ACCEPTED,
            }
        )

    add("wrong-stage", "requested", "rejectWrongStage", kind="bindEvidence")
    add("atom-substitution", "requested", "rejectAtomSubstitution", {"atom": "claim:other"})
    for field in ("proposition", "obligation", "predicate"):
        add(f"{field}-substitution", "requested", "rejectProjectionSubstitution", {field: "sha256:other"})
    add("state-substitution", "requested", "rejectStateCategorySubstitution", {"current_state": "unsupported"})
    add("event-replay", "requested", "rejectEventReplay", last_event="event:111")
    for field in (
        "support_assignment_requested",
        "external_effect_requested",
        "parent_movement_requested",
        "descendant_movement_requested",
    ):
        add(field, "requested", "rejectAuthorityLeak", {field: True})
    add("terminal-intent-mismatch", "requested", "rejectStateCategorySubstitution", {"proposed_state": "refuted"})
    for field, outcome in (
        ("scope", "requestScope"),
        ("assumptions", "requestAssumptions"),
        ("non_claims", "requestNonClaims"),
        ("dependencies", "requestDependencies"),
    ):
        add(f"requested-{field}", "requested", outcome, {field: False})
    add("requested-accepted", "requested", "acceptProjectionFreeze")
    for field, outcome in (
        ("evidence_refs", "requestEvidenceRefs"),
        ("evidence_roles", "requestEvidenceRoles"),
        ("artifact_bindings", "requestArtifactBindings"),
    ):
        add(f"evidence-{field}", "projectionsFrozen", outcome, {field: False})
    for target, field, outcome in (
        ("sourceDerived", "source_grounding", "requestSourceGrounding"),
        ("prototypeBacked", "prototype_inspection", "requestPrototypeInspection"),
        ("syntheticTestBacked", "synthetic_validation", "requestSyntheticValidation"),
        ("empiricalTestBacked", "empirical_validation", "requestEmpiricalValidation"),
        ("externalLiteratureBacked", "external_literature", "requestExternalLiterature"),
    ):
        add(f"target-{target}", "projectionsFrozen", outcome, {"proposed_state": target, field: False})
    for field, outcome in (
        ("negative_evidence", "requestNegativeEvidence"),
        ("downgrade_trigger", "requestDowngradeTrigger"),
        ("supersession_lineage", "requestSupersessionLineage"),
    ):
        add(f"adverse-{field}", "projectionsFrozen", outcome, {"intent": "downgrade", "proposed_state": "argument", field: False})
    add("evidence-accepted", "projectionsFrozen", "acceptEvidenceBinding")
    for field, outcome in (
        ("independent_review", "requestIndependentReview"),
        ("projection_alignment", "requestProjectionAlignment"),
        ("dissent", "requestDissent"),
    ):
        add(f"review-{field}", "evidenceBound", outcome, {field: False})
    add("review-accepted", "evidenceBound", "acceptReview")
    for field, outcome in (
        ("limitations", "requestLimitations"),
        ("residuals", "requestResiduals"),
        ("changelog", "requestChangelog"),
    ):
        add(f"decision-{field}", "reviewed", outcome, {field: False})
    add("decision-accepted", "reviewed", "acceptDecision")
    add("handoff-missing", "decided", "requestLedgerHandoff", {"ledger_handoff": False})
    add("handoff-accepted", "decided", "acceptHandoff")
    add("ack-missing", "handedOff", "requestAcknowledgment", {"acknowledgment": False})
    add("ack-accepted", "handedOff", "acceptAcknowledgment")
    return rows


def run_lean() -> dict[str, Any]:
    # Build the named Lake target so this check is valid in a fresh checkout
    # where imported modules do not yet have cached `.olean` artifacts.
    command = ["lake", "build", "AsiStackProofs.EvidenceTransitionRefinement"]
    completed = subprocess.run(
        command,
        cwd=ROOT / "lean",
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if completed.returncode:
        raise RuntimeError(completed.stdout)
    return {
        "command": " ".join(command),
        "exit_code": 0,
        # Lake's success output differs between a cold build and an up-to-date
        # cache. Bind the receipt to the verified source instead of unstable
        # progress text.
        "source_sha256": hashlib.sha256(LEAN.read_bytes()).hexdigest(),
    }


def build(errors: list[str]) -> dict[str, Any]:
    rows = route_cases()
    for row in rows:
        if row["actual_route"] != row["expected_route"]:
            errors.append(f"{row['case_id']}: {row['actual_route']} != {row['expected_route']}")
    lean_text = LEAN.read_text()
    route_body = re.search(r"inductive Route where(?P<body>.*?)deriving DecidableEq", lean_text, re.S)
    if not route_body:
        raise RuntimeError("Lean route declaration missing")
    declared = set(re.findall(r"\|\s+([A-Za-z][A-Za-z0-9]*)", route_body.group("body")))
    reached = {row["actual_route"] for row in rows}
    negative = [row for row in rows if not row["accepted"]]
    if declared != reached:
        errors.append(f"route coverage drifted: missing={sorted(declared - reached)}, extra={sorted(reached - declared)}")
    return {
        "schema_version": "asi_stack.evidence_transition_refinement.result.v1",
        "result_id": "2026-07-26-evidence-transition-refinement",
        "recorded_date": "2026-07-26",
        "command": COMMAND,
        "model": {
            "lean_module": str(LEAN.relative_to(ROOT)),
            "stage_count": 6,
            "route_count": len(declared),
            "reached_route_count": len(reached),
            "route_case_count": len(rows),
            "rejected_mutation_count": len(negative),
            "projection_count": 3,
            "evidence_dimension_count": 8,
            "support_assignment_count": 0,
            "parent_or_descendant_movement_count": 0,
            "external_effect_count": 0,
        },
        "route_cases": rows,
        "lean_verification": run_lean(),
        "support_state_effect": "none",
        "external_effect": "none",
        "residuals": [
            "Finite authored lifecycle only; it does not establish that evidence is true, sufficient, independent, current, representative, or causally complete.",
            "The three projections are digest-bound identities; their semantic equivalence still requires review and cannot be inferred from matching hashes.",
            "Support states remain heterogeneous public summaries beside a non-aggregating evidence vector; the model establishes no total ordering or automatic promotion.",
            "The handoff is a bounded recommendation to the claim ledger, not a support assignment, parent or descendant update, release decision, or external action.",
        ],
        "non_claims": [
            "no claim truth, evidence truth, reviewer independence, model capability, safety, release readiness, deployment, AGI, ASI, support assignment, inherited movement, or external effect",
            "no inference from route coverage or green validation to open-world completeness or adequate real-world evidence",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write-result", action="store_true")
    args = parser.parse_args()
    errors: list[str] = []
    result = build(errors)
    jsonschema.validate(result, json.loads(SCHEMA.read_text()))
    serialized = json.dumps(result, indent=2) + "\n"
    if args.write_result:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized)
    elif not RESULT.exists() or RESULT.read_text() != serialized:
        errors.append(f"{RESULT.relative_to(ROOT)} stale; run {COMMAND} --write-result")
    if errors:
        print("Evidence transition refinement failed:\n - " + "\n - ".join(errors))
        sys.exit(1)
    print(
        f"Evidence transition refinement passed: {result['model']['stage_count']} stages, "
        f"{result['model']['route_count']} routes, "
        f"{result['model']['rejected_mutation_count']} rejecting cases; "
        "three projections preserved; support/inheritance/effect authority none."
    )


if __name__ == "__main__":
    main()

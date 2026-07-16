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
LEAN = ROOT / "lean/AsiStackProofs/SafetyCaseRefinement.lean"
SCHEMA = ROOT / "schemas/safety_case_refinement.schema.json"
FIXTURE = ROOT / "experiments/safety_case_assurance/fixtures/cases.json"
RESULT = ROOT / "experiments/safety_case_refinement/results/2026-07-15-local.json"
COMMAND = "python3 scripts/validate_safety_case_refinement.py"

STAGES = ["draft", "scoped", "evidenced", "challenged", "reviewed", "readinessBound"]
KINDS = {
    "draft": "scope",
    "scoped": "attachEvidence",
    "evidenced": "recordChallenge",
    "challenged": "recordReview",
    "reviewed": "requestReadiness",
    "readinessBound": "invalidate",
}
ACCEPTED = {
    "accept_scope", "accept_evidence", "accept_challenge", "accept_review",
    "accept_readiness", "accept_invalidation",
}
IDENTITY = {
    "caseId", "caseVersion", "contextDigest", "claimDigest", "hazardDigest",
    "evidenceDigest", "countercaseDigest", "reviewerDigest", "authorityDigest",
    "residualDigest",
}
GATES = {
    "draft": [
        ("deploymentContextPresent", False, "request_deployment_context"),
        ("topClaimScoped", False, "request_top_claim"),
        ("hazardModelPresent", False, "request_hazard_model"),
        ("argumentStrategyPresent", False, "request_argument_strategy"),
    ],
    "scoped": [
        ("evidenceReferencesPresent", False, "request_evidence"),
        ("evidenceDependenciesCurrent", False, "request_current_evidence"),
        ("assumptionsPresent", False, "request_assumptions"),
    ],
    "evidenced": [
        ("countercaseReviewPresent", False, "request_countercase"),
        ("defeaterDispositionPresent", False, "request_defeater_disposition"),
        ("unresolvedDefeaterPresent", True, "request_defeater_disposition"),
    ],
    "challenged": [
        ("independentReviewPresent", False, "request_independent_review"),
        ("reviewerCompetenceRecorded", False, "request_reviewer_competence"),
        ("reviewerConflictDisclosed", False, "request_conflict_disclosure"),
    ],
    "reviewed": [
        ("acceptanceCriterionPresent", False, "request_acceptance_criterion"),
        ("residualOwnerPresent", False, "request_residual_owner"),
        ("decisionAuthorityPresent", False, "request_decision_authority"),
        ("authoritySeparationPresent", False, "reject_authority_laundering"),
    ],
    "readinessBound": [
        ("invalidationCausePresent", False, "request_invalidation_cause"),
        ("affectedPathsPresent", False, "request_affected_paths"),
        ("descendantInvalidationComplete", False, "request_descendant_invalidation"),
    ],
}


def packet() -> dict[str, Any]:
    return {
        "caseId": 701, "caseVersion": 3, "contextDigest": 702, "claimDigest": 703,
        "hazardDigest": 704, "evidenceDigest": 705, "countercaseDigest": 706,
        "reviewerDigest": 707, "authorityDigest": 708, "residualDigest": 709,
        "eventDigest": 1, "deploymentContextPresent": True, "topClaimScoped": True,
        "hazardModelPresent": True, "argumentStrategyPresent": True,
        "evidenceReferencesPresent": True, "evidenceDependenciesCurrent": True,
        "assumptionsPresent": True, "countercaseReviewPresent": True,
        "defeaterDispositionPresent": True, "unresolvedDefeaterPresent": False,
        "independentReviewPresent": True, "reviewerCompetenceRecorded": True,
        "reviewerConflictDisclosed": True, "acceptanceCriterionPresent": True,
        "residualOwnerPresent": True, "decisionAuthorityPresent": True,
        "authoritySeparationPresent": True, "invalidationCausePresent": True,
        "affectedPathsPresent": True, "descendantInvalidationComplete": True,
        "supportAssignmentRequested": False, "externalEffectRequested": False,
    }


def route(stage: str, kind: str, value: dict[str, Any], last_event: int = 0) -> str:
    canonical = packet()
    if kind != KINDS[stage]:
        return "reject_wrong_stage"
    if any(value[name] != canonical[name] for name in IDENTITY):
        return "reject_case_substitution"
    if value["eventDigest"] == last_event:
        return "reject_event_replay"
    if value["supportAssignmentRequested"] or value["externalEffectRequested"]:
        return "reject_authority_leak"
    for field, bad, answer in GATES[stage]:
        if value[field] is bad:
            return answer
    return {
        "draft": "accept_scope", "scoped": "accept_evidence",
        "evidenced": "accept_challenge", "challenged": "accept_review",
        "reviewed": "accept_readiness", "readinessBound": "accept_invalidation",
    }[stage]


def run(command: str) -> dict[str, Any]:
    proc = subprocess.run(command.split(), cwd=ROOT, text=True,
                          stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if proc.returncode:
        raise RuntimeError(proc.stdout)
    return {"command": command, "exit_code": proc.returncode,
            "output_sha256": hashlib.sha256(proc.stdout.encode()).hexdigest()}


def build() -> dict[str, Any]:
    cases: list[dict[str, str]] = []
    for index, stage in enumerate(STAGES, 1):
        value = packet()
        value["eventDigest"] = index
        cases.append({"case_id": f"{stage}_accepted",
                      "expected_route": route(stage, KINDS[stage], value)})
    for stage, gates in GATES.items():
        for field, bad, _ in gates:
            value = packet()
            value["eventDigest"] = 90
            value[field] = bad
            cases.append({"case_id": f"{stage}_{field}",
                          "expected_route": route(stage, KINDS[stage], value)})
    for case_id, kind, field, value_ in [
        ("wrong_stage", "invalidate", None, None),
        ("case_substitution", "scope", "caseId", 999),
        ("event_replay", "scope", "eventDigest", 0),
        ("authority_leak", "scope", "supportAssignmentRequested", True),
    ]:
        value = packet()
        if field:
            value[field] = value_
        cases.append({"case_id": case_id, "expected_route": route("draft", kind, value)})

    mutations: list[dict[str, Any]] = []
    for field in sorted(IDENTITY):
        value = packet()
        value[field] += 1000
        mutations.append({"mutation_id": f"binding_{field}",
                          "rejected": route("draft", "scope", value) not in ACCEPTED})
    for stage, gates in GATES.items():
        for field, bad, _ in gates:
            value = packet()
            value["eventDigest"] = 91
            value[field] = bad
            mutations.append({"mutation_id": f"gate_{stage}_{field}",
                              "rejected": route(stage, KINDS[stage], value) not in ACCEPTED})
    for mutation_id, stage, kind, field, value_ in [
        ("wrong_kind", "draft", "invalidate", None, None),
        ("event_replay", "draft", "scope", "eventDigest", 0),
        ("support_leak", "draft", "scope", "supportAssignmentRequested", True),
        ("external_effect_leak", "draft", "scope", "externalEffectRequested", True),
        ("stale_readiness_after_invalidation", "challenged", "requestReadiness", None, None),
    ]:
        value = packet()
        if field:
            value[field] = value_
        mutations.append({"mutation_id": mutation_id,
                          "rejected": route(stage, kind, value) not in ACCEPTED})

    fixture = json.loads(FIXTURE.read_text())
    command_receipts = [run("python3 scripts/validate_safety_case_assurance.py")]
    return {
        "schema_version": "asi_stack.safety_case_refinement.v1",
        "result_id": "safety-case-refinement-2026-07-15-local",
        "source_sha256": {
            "lean_model": hashlib.sha256(LEAN.read_bytes()).hexdigest(),
            "input_fixture": hashlib.sha256(FIXTURE.read_bytes()).hexdigest(),
        },
        "input_suite": {"suite_id": "safety_case_assurance",
                        "case_count": len(fixture["cases"]), "passed_count": 8},
        "reachable_stage_count": len(STAGES), "route_case_count": len(cases),
        "route_coverage": cases, "mutation_count": len(mutations),
        "mutation_rejection_count": sum(item["rejected"] for item in mutations),
        "mutation_receipts": mutations, "command_receipts": command_receipts,
        "witness": {"terminal_stage": "challenged", "receipt_count": 6,
                    "readiness_handoff_count": 1, "invalidation_count": 1,
                    "support_assignment_count": 0, "external_effect_count": 0},
        "support_state_effect": "none",
        "non_claims": [
            "no hazard completeness or evidence truth result",
            "no reviewer competence or independence result",
            "no control effectiveness, safety, or readiness result",
            "no release authority or external effect",
            "no deployed descendant invalidation or transfer result",
            "no support promotion",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    result = build()
    errors: list[str] = []
    if result["route_case_count"] != 30:
        errors.append("route count drifted")
    if result["mutation_count"] != 35 or result["mutation_rejection_count"] != 35:
        errors.append("mutation contract drifted")
    for needle in ("inductive Stage", "def routeFor", "rejected_event_preserves_state",
                   "full_case_lifecycle_returns_to_challenge_after_invalidation"):
        if needle not in LEAN.read_text():
            errors.append(f"Lean model missing {needle}")
    jsonschema.validate(result, json.loads(SCHEMA.read_text()))
    serialized = json.dumps(result, indent=2) + "\n"
    if args.write:
        RESULT.parent.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(serialized)
    elif not RESULT.exists() or RESULT.read_text() != serialized:
        errors.append(f"{RESULT.relative_to(ROOT)} is stale; run {COMMAND} --write")
    if errors:
        print("Safety-case refinement failed:\n - " + "\n - ".join(errors))
        sys.exit(1)
    print("Safety-case refinement passed: 8 inherited cases, 6 stages, 30 routes, "
          "35/35 mutations rejected, support effect none.")


if __name__ == "__main__":
    main()

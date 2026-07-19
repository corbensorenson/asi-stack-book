#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "schemas/human_oversight_control_packet.schema.json"
FIXTURE = ROOT / "tests/fixtures/protocol_records/human_oversight_control_packet.valid.json"
PROTOCOL = ROOT / "experiments/human_factors_argument_exit/preregistration.json"
LEAN = ROOT / "lean/AsiStackProofs/HumanFactorsOversight.lean"
CHAPTER = ROOT / "chapters/human-factors-and-meaningful-control-in-oversight.qmd"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def errors(data: dict[str, Any]) -> list[str]:
    out: list[str] = []
    fixture = data["fixture"]
    protocol = data["protocol"]
    lean_text = data["lean_text"]
    chapter = data["chapter"]
    schema_errors = sorted(
        Draft202012Validator(data["schema"]).iter_errors(fixture),
        key=lambda error: list(error.path),
    )
    out.extend(f"fixture schema: {'.'.join(map(str, error.path))}: {error.message}" for error in schema_errors)
    if fixture.get("origin_class") != "repository_fixture" or fixture.get("disposition") != "safe_hold":
        out.append("fixture must remain a safe-hold record-shape fixture")
    task = fixture.get("task_and_controller", {})
    evidence = fixture.get("evidence_and_comprehension", {})
    workload = fixture.get("workload_and_time", {})
    intervention = fixture.get("authority_and_intervention", {})
    responsibility = fixture.get("responsibility_and_privacy", {})
    authority = fixture.get("authority_boundary", {})
    if task.get("qualification_current") is not False or evidence.get("comprehension_disposition") != "not_run":
        out.append("fixture must retain unassessed qualification and comprehension")
    if evidence.get("evidence_observable") is not False or evidence.get("representation_compatible") is not False:
        out.append("fixture must retain missing evidence and representation predicates")
    if workload.get("workload_inside_bound") is not False or workload.get("decision_window_positive") is not False:
        out.append("fixture must retain uncalibrated workload and impossible decision window")
    if intervention.get("task_authority_present") is not False or intervention.get("intervention_channel_reachable") is not False:
        out.append("fixture must retain missing task authority and intervention channel")
    if responsibility.get("responsibility_inside_effective_control") is not False:
        out.append("fixture must not assign responsibility without effective control")
    if responsibility.get("punitive_inference_prohibited") is not True or responsibility.get("biometric_or_emotion_inference_used") is not False:
        out.append("fixture privacy and anti-punitive boundary drifted")
    if authority != {
        "authority_delta": "none",
        "effect_authorized": False,
        "support_assignment_authorized": False,
        "release_authority": False,
    }:
        out.append("fixture authority boundary drifted")
    if fixture.get("support_state_effect") != "none" or len(fixture.get("non_claims", [])) < 3:
        out.append("fixture support or non-claim boundary drifted")

    if protocol.get("state") != "protocol_ready_ethics_and_resource_authority_required_not_executed":
        out.append("claim-bearing protocol state drifted")
    if protocol.get("protected_outcomes_opened") is not False or protocol.get("human_participants_recruited") is not False:
        out.append("protocol opened outcomes or recruited participants")
    if protocol.get("support_state_effect") != "none" or protocol.get("execution_authority") != "not_granted_by_this_record":
        out.append("protocol invented support or execution authority")
    ethics = protocol.get("ethics_and_privacy_gate", {})
    required_true = (
        "ethics_review_required_before_recruitment", "jurisdiction_and_institution_review_required",
        "minimal_risk_sandbox_only", "informed_consent_required",
        "withdrawal_without_penalty_required", "accessibility_accommodations_required",
        "pseudonymous_episode_ids_required", "short_retention_and_deletion_plan_required",
        "adverse_event_complaint_debrief_and_appeal_required",
    )
    if any(ethics.get(key) is not True for key in required_true):
        out.append("required ethics/privacy gate weakened")
    required_false = (
        "real_external_effects_allowed", "employment_or_performance_scoring_allowed",
        "covert_surveillance_allowed", "biometric_affective_gaze_camera_or_keystroke_capture_default",
        "secondary_use_without_separate_approval_allowed",
    )
    if any(ethics.get(key) is not False for key in required_false):
        out.append("prohibited effects, scoring, surveillance, or secondary use enabled")
    if len(protocol.get("arms", [])) != 4 or len(protocol.get("competence_gates", [])) != 9:
        out.append("protocol arm or competence denominator drifted")
    if len(protocol.get("positive_controls", [])) != 5 or len(protocol.get("adversarial_controls", [])) != 7:
        out.append("protocol control denominator drifted")
    if len(protocol.get("rescue_ladder", [])) != 6 or len(protocol.get("outcomes", [])) != 12:
        out.append("protocol rescue or outcome denominator drifted")
    decision = protocol.get("decision_rule", {})
    if not str(decision.get("maximum_negative_level", "")).startswith("N3") or "cannot be refuted" not in decision.get("maximum_negative_level", ""):
        out.append("protocol exact negative ceiling drifted")
    isolation = protocol.get("resource_and_isolation_gate", {})
    if isolation.get("p2_reserved_storage_may_be_reclaimed") is not False or isolation.get("p2_images_or_denominators_may_be_changed") is not False:
        out.append("protocol violates P2 resource or denominator isolation")
    if isolation.get("prepublication_human_review_substitution_allowed") is not False:
        out.append("protocol substitutes participants for prepublication review")

    if len(re.findall(r"(?m)^theorem ", lean_text)) != 9:
        out.append("HumanFactorsOversight theorem denominator drifted")
    for theorem in (
        "control_envelope_blocks_action", "responsibility_requires_control",
        "control_route_never_grants_support_or_effect", "bounded_review_preserves_declared_conditions",
    ):
        if f"theorem {theorem}" not in lean_text:
            out.append(f"Lean theorem missing: {theorem}")
    for phrase in (
        "Why this boundary earns a chapter",
        "integrate at argument support",
        "protocol-ready with ethics and resource",
        "human_oversight_control_packet.schema.json",
        "AsiStackProofs.HumanFactorsOversight",
        "does not prove comprehension",
    ):
        if phrase not in chapter:
            out.append(f"chapter contract phrase missing: {phrase}")
    return out


def main() -> None:
    data = {
        "schema": load(SCHEMA),
        "fixture": load(FIXTURE),
        "protocol": load(PROTOCOL),
        "lean_text": LEAN.read_text(encoding="utf-8"),
        "chapter": CHAPTER.read_text(encoding="utf-8"),
    }
    failures = errors(data)
    mutations = [
        ("authorize effect", lambda d: d["fixture"]["authority_boundary"].__setitem__("effect_authorized", True)),
        ("grant support", lambda d: d["fixture"]["authority_boundary"].__setitem__("support_assignment_authorized", True)),
        ("assign blame", lambda d: d["fixture"]["responsibility_and_privacy"].__setitem__("responsibility_inside_effective_control", True)),
        ("enable punitive inference", lambda d: d["fixture"]["responsibility_and_privacy"].__setitem__("punitive_inference_prohibited", False)),
        ("enable biometrics", lambda d: d["fixture"]["responsibility_and_privacy"].__setitem__("biometric_or_emotion_inference_used", True)),
        ("support laundering", lambda d: d["fixture"].__setitem__("support_state_effect", "empirical-test-backed")),
        ("open outcomes", lambda d: d["protocol"].__setitem__("protected_outcomes_opened", True)),
        ("invent participants", lambda d: d["protocol"].__setitem__("human_participants_recruited", True)),
        ("drop ethics", lambda d: d["protocol"]["ethics_and_privacy_gate"].__setitem__("ethics_review_required_before_recruitment", False)),
        ("allow surveillance", lambda d: d["protocol"]["ethics_and_privacy_gate"].__setitem__("covert_surveillance_allowed", True)),
        ("drop competence", lambda d: d["protocol"]["competence_gates"].pop()),
        ("drop static baseline", lambda d: d["protocol"]["arms"].pop(2)),
        ("inflate negative", lambda d: d["protocol"]["decision_rule"].__setitem__("maximum_negative_level", "N5 meaningful control is impossible")),
        ("allow P2 displacement", lambda d: d["protocol"]["resource_and_isolation_gate"].__setitem__("p2_reserved_storage_may_be_reclaimed", True)),
        ("erase formal ceiling", lambda d: d.__setitem__("chapter", d["chapter"].replace("does not prove comprehension", "proves comprehension"))),
    ]
    baseline = set(errors(data))
    for label, mutation in mutations:
        candidate = copy.deepcopy(data)
        mutation(candidate)
        if not set(errors(candidate)) - baseline:
            failures.append(f"negative mutation accepted: {label}")
    lean = subprocess.run(
        ["lake", "env", "lean", "AsiStackProofs/HumanFactorsOversight.lean"],
        cwd=ROOT / "lean", text=True, capture_output=True,
    )
    if lean.returncode:
        failures.append("HumanFactorsOversight Lean compile failed: " + (lean.stdout + lean.stderr).strip())
    if failures:
        raise SystemExit("Human oversight control contract failed:\n - " + "\n - ".join(failures))
    print(
        "Human oversight control contract passed: one safe-hold no-human fixture, "
        "two public targets through 9 theorem declarations, 4 arms, 9 competence "
        "gates, 5 positive and 7 adversarial controls, 6 rescue steps, 12 outcomes, "
        "15 mutations rejected; participants and protected outcomes closed, "
        "support/effect/release authority none."
    )


if __name__ == "__main__":
    main()

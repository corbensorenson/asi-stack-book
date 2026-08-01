#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable


ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean" / "AsiStackProofs" / "MilitaryInteractionReview.lean"
LEAN_ROOT = ROOT / "lean" / "AsiStackProofs.lean"
CHAPTER = ROOT / "chapters" / "military-ai-autonomous-weapons-and-strategic-stability.qmd"
DOSSIER = ROOT / "evidence_quality" / "proof_model_dossiers" / "military-ai-autonomous-weapons-and-strategic-stability.md"
MANIFEST = ROOT / "proofs" / "proof_manifest.json"
TRIAGE = ROOT / "proofs" / "proof_triage.json"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs" / "book_outline.md"
FIXTURE = ROOT / "tests" / "fixtures" / "proof_models" / "military_interaction_dossier.json"

TAG = "lean:military-ai-autonomous-weapons-and-strategic-stability.admission_boundary"
MODULE = "AsiStackProofs.MilitaryInteractionReview"
FORMAL_TARGET = (
    "An eight-step finite review preserves accumulated public-safe scope, bounded authority, "
    "meaningful human judgment, observation, safe-posture, interaction, custody, and non-authorizing "
    "boundary obligations; a complete authored dossier reaches only a Project Theseus public-safe "
    "simulation, while 45 admission-axis mutations block readiness and receive exact repair or refusal "
    "dispositions. Decision-time, off-ramp, and expiry shortfalls remain rejecting under adverse "
    "monotone changes. Human-interface presence cannot recover meaningful judgment, and identical "
    "component evidence cannot recover strategic-interaction review. No theorem authorizes a weapon "
    "or establishes lawful use, meaningful human control in practice, escalation reduction, strategic "
    "stability, safety, support, release, transfer, or external effect."
)


Predicate = Callable[[dict[str, Any]], bool]
Mutation = Callable[[dict[str, Any]], None]
Axis = tuple[str, Predicate, str, Mutation]

GROUPS: list[list[Axis]] = [
    [
        ("simulationRequest", lambda d: d["simulationRequested"], "refusedNoSimulation", lambda d: d.update(simulationRequested=False)),
        ("nonOperationalScenario", lambda d: d["publicSafeNonOperationalScenario"], "refuseOperationalScenario", lambda d: d.update(publicSafeNonOperationalScenario=False)),
        ("missionIdentity", lambda d: d["missionIdentityBound"], "bindMissionIdentity", lambda d: d.update(missionIdentityBound=False)),
        ("decisionRole", lambda d: d["decisionRoleBound"], "bindDecisionRole", lambda d: d.update(decisionRoleBound=False)),
        ("affectedPopulation", lambda d: d["affectedPopulationBound"], "bindAffectedPopulation", lambda d: d.update(affectedPopulationBound=False)),
        ("legalBoundary", lambda d: d["legalBoundaryRecorded"], "recordLegalBoundary", lambda d: d.update(legalBoundaryRecorded=False)),
    ],
    [
        ("accountableAuthority", lambda d: d["accountableAuthorityBound"], "bindAccountableAuthority", lambda d: d.update(accountableAuthorityBound=False)),
        ("effectEnvelope", lambda d: d["effectEnvelopeBound"], "bindEffectEnvelope", lambda d: d.update(effectEnvelopeBound=False)),
        ("authorityExpansion", lambda d: not d["authorityExpansionRequested"], "refuseAuthorityExpansion", lambda d: d.update(authorityExpansionRequested=True)),
    ],
    [
        ("humanInterface", lambda d: d["humanInterfacePresent"], "addHumanInterface", lambda d: d.update(humanInterfacePresent=False)),
        ("humanAuthority", lambda d: d["humanAuthorityPresent"], "restoreHumanAuthority", lambda d: d.update(humanAuthorityPresent=False)),
        ("decisionTime", lambda d: d["requiredDecisionTime"] > 0 and d["requiredDecisionTime"] <= d["availableDecisionTime"], "restoreDecisionTime", lambda d: d.update(availableDecisionTime=2)),
        ("humanInformation", lambda d: d["humanInformationSufficient"], "restoreHumanInformation", lambda d: d.update(humanInformationSufficient=False)),
        ("humanCompetence", lambda d: d["humanCompetenceBound"], "bindHumanCompetence", lambda d: d.update(humanCompetenceBound=False)),
        ("humanAttention", lambda d: d["humanAttentionAvailable"], "restoreHumanAttention", lambda d: d.update(humanAttentionAvailable=False)),
        ("interventionReachability", lambda d: d["interventionReachable"], "restoreInterventionReachability", lambda d: d.update(interventionReachable=False)),
        ("alternatives", lambda d: d["alternativesPresent"], "restoreAlternatives", lambda d: d.update(alternativesPresent=False)),
        ("independentJudgment", lambda d: d["independentJudgmentPossible"], "restoreIndependentJudgment", lambda d: d.update(independentJudgmentPossible=False)),
    ],
    [
        ("sensorProvenance", lambda d: d["sensorProvenanceBound"], "bindSensorProvenance", lambda d: d.update(sensorProvenanceBound=False)),
        ("sensorDependencies", lambda d: d["sensorDependenciesRecorded"], "recordSensorDependencies", lambda d: d.update(sensorDependenciesRecorded=False)),
        ("uncertaintyVisibility", lambda d: d["uncertaintyVisible"], "exposeUncertainty", lambda d: d.update(uncertaintyVisible=False)),
        ("corroborationPolicy", lambda d: d["corroborationPolicyBound"], "bindCorroborationPolicy", lambda d: d.update(corroborationPolicyBound=False)),
    ],
    [
        ("abstentionRoute", lambda d: d["abstentionRoutePresent"], "addAbstentionRoute", lambda d: d.update(abstentionRoutePresent=False)),
        ("communicationLossPosture", lambda d: d["communicationLossPosturePresent"], "recordCommunicationLossPosture", lambda d: d.update(communicationLossPosturePresent=False)),
        ("integrityFailurePosture", lambda d: d["integrityFailurePosturePresent"], "recordIntegrityFailurePosture", lambda d: d.update(integrityFailurePosturePresent=False)),
        ("suspensionAuthority", lambda d: d["suspensionAuthorityPresent"], "bindSuspensionAuthority", lambda d: d.update(suspensionAuthorityPresent=False)),
    ],
    [
        ("adversaryModelSet", lambda d: d["adversaryModelSetPresent"], "addAdversaryModelSet", lambda d: d.update(adversaryModelSetPresent=False)),
        ("doctrineVariants", lambda d: d["doctrineVariantsPresent"], "addDoctrineVariants", lambda d: d.update(doctrineVariantsPresent=False)),
        ("reciprocalEffects", lambda d: d["reciprocalEffectsTracked"], "trackReciprocalEffects", lambda d: d.update(reciprocalEffectsTracked=False)),
        ("offRamps", lambda d: d["requiredOffRampCount"] > 0 and d["requiredOffRampCount"] <= d["availableOffRampCount"], "restoreOffRamps", lambda d: d.update(availableOffRampCount=1)),
        ("proliferationResidual", lambda d: d["proliferationResidualTracked"], "trackProliferationResidual", lambda d: d.update(proliferationResidualTracked=False)),
    ],
    [
        ("independentReview", lambda d: d["independentReviewPresent"], "assignIndependentReview", lambda d: d.update(independentReviewPresent=False)),
        ("restrictedEvidenceCustody", lambda d: d["restrictedEvidenceCustodyPresent"], "assignRestrictedEvidenceCustody", lambda d: d.update(restrictedEvidenceCustodyPresent=False)),
        ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiredDossier", lambda d: d.update(expiresAt=4)),
        ("publicMaximumInference", lambda d: d["publicMaximumInferencePresent"], "recordPublicMaximumInference", lambda d: d.update(publicMaximumInferencePresent=False)),
        ("incidentAndRemedy", lambda d: d["incidentAndRemedyRoutePresent"], "addIncidentAndRemedyRoute", lambda d: d.update(incidentAndRemedyRoutePresent=False)),
        ("decommissionRoute", lambda d: d["decommissionRoutePresent"], "addDecommissionRoute", lambda d: d.update(decommissionRoutePresent=False)),
        ("residualCustody", lambda d: d["residualCustodyPresent"], "assignResidualCustody", lambda d: d.update(residualCustodyPresent=False)),
        ("nonClaimBoundary", lambda d: d["nonClaimBoundaryPresent"], "recordNonClaimBoundary", lambda d: d.update(nonClaimBoundaryPresent=False)),
        ("weaponAuthorization", lambda d: not d["weaponAuthorizationRequested"], "refuseWeaponAuthorization", lambda d: d.update(weaponAuthorizationRequested=True)),
        ("lawfulUseClaim", lambda d: not d["lawfulUseClaimRequested"], "refuseLawfulUseClaim", lambda d: d.update(lawfulUseClaimRequested=True)),
        ("strategicStabilityClaim", lambda d: not d["strategicStabilityClaimRequested"], "refuseStrategicStabilityClaim", lambda d: d.update(strategicStabilityClaimRequested=True)),
        ("supportAssignment", lambda d: not d["supportAssignmentRequested"], "refuseSupportAssignment", lambda d: d.update(supportAssignmentRequested=True)),
        ("releaseAuthority", lambda d: not d["releaseAuthorityRequested"], "refuseReleaseAuthority", lambda d: d.update(releaseAuthorityRequested=True)),
        ("operationalDetailPublication", lambda d: not d["operationalDetailPublicationRequested"], "refuseOperationalDetailPublication", lambda d: d.update(operationalDetailPublicationRequested=True)),
    ],
]

REQUIRED_THEOREMS = {
    "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant",
    "simulation_eligibility_requires_admissible_dossier",
    "admissible_dossier_is_ready",
    "complete_dossier_is_ready",
    "complete_dossier_reaches_only_public_safe_simulation",
    "every_admission_axis_mutation_blocks_readiness",
    "every_admission_axis_mutation_has_exact_repair_disposition",
    "every_admission_axis_mutation_reaches_repair_state",
    "every_admission_axis_mutation_blocks_simulation_eligibility",
    "readiness_requires_scope",
    "readiness_requires_bounded_authority",
    "readiness_requires_meaningful_human_judgment",
    "readiness_requires_observation_trust_record",
    "readiness_requires_safe_posture",
    "readiness_requires_interaction_case",
    "readiness_requires_custody_and_non_authorizing_boundary",
    "expired_dossier_remains_expired_when_time_advances",
    "decision_time_shortfall_persists_when_available_time_decreases",
    "off_ramp_shortfall_persists_when_available_routes_decrease",
    "same_human_interface_can_hide_opposite_judgment_results",
    "interface_presence_cannot_recover_meaningful_judgment",
    "identical_component_evidence_can_require_opposite_interaction_reviews",
    "component_evidence_cannot_recover_interaction_review",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def fail(errors: list[str]) -> None:
    if errors:
        raise SystemExit(
            "Military-interaction review validation failed:\n"
            + "\n".join(f" - {error}" for error in errors)
        )


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for group in GROUPS for _, predicate, _, _ in group)


def exact_repair(dossier: dict[str, Any]) -> str:
    for group in GROUPS:
        for _, predicate, route, _ in group:
            if not predicate(dossier):
                return route
    return "eligibleForTheseusPublicSafeSimulation"


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, LEAN_ROOT, CHAPTER, DOSSIER, MANIFEST, TRIAGE, STRUCTURE, OUTLINE, FIXTURE):
        if not path.exists():
            errors.append(f"missing {path.relative_to(ROOT)}")
    fail(errors)

    complete = load(FIXTURE)
    axes = [axis for group in GROUPS for axis in group]
    if len(axes) != 45 or len({axis[0] for axis in axes}) != 45:
        errors.append("independent mutation denominator must contain 45 unique axes")
    if not ready(complete) or exact_repair(complete) != "eligibleForTheseusPublicSafeSimulation":
        errors.append("complete dossier must reach only public-safe Theseus simulation eligibility")
    for axis, _, expected, mutate in axes:
        candidate = deepcopy(complete)
        mutate(candidate)
        if ready(candidate):
            errors.append(f"{axis} mutation remained ready")
        if exact_repair(candidate) != expected:
            errors.append(f"{axis} mutation reached {exact_repair(candidate)}, expected {expected}")

    expired = deepcopy(complete)
    expired.update(currentTick=9, expiresAt=8)
    for later_tick in range(9, 15):
        if later_tick <= expired["expiresAt"]:
            errors.append(f"later tick {later_tick} laundered expiry")
    time_shortfall = deepcopy(complete)
    time_shortfall.update(requiredDecisionTime=4, availableDecisionTime=3)
    for less_time in range(4):
        if time_shortfall["requiredDecisionTime"] <= less_time:
            errors.append(f"lower decision time {less_time} laundered shortfall")
    off_ramp_shortfall = deepcopy(complete)
    off_ramp_shortfall.update(requiredOffRampCount=3, availableOffRampCount=2)
    for fewer_routes in range(3):
        if off_ramp_shortfall["requiredOffRampCount"] <= fewer_routes:
            errors.append(f"lower off-ramp count {fewer_routes} laundered shortfall")

    ceremonial = deepcopy(complete)
    ceremonial["availableDecisionTime"] = 0
    meaningful = lambda d: all(predicate(d) for _, predicate, _, _ in GROUPS[2])
    if complete["humanInterfacePresent"] != ceremonial["humanInterfacePresent"]:
        errors.append("interface witnesses no longer share interface presence")
    if not meaningful(complete) or meaningful(ceremonial):
        errors.append("same-interface witnesses no longer require opposite judgment results")

    component = {"accuracyClass": 4, "latencyClass": 4, "reliabilityClass": 4}
    stable = {"component": component, "adversaryEscalates": False, "offRampSurvives": True}
    unstable = {"component": deepcopy(component), "adversaryEscalates": True, "offRampSurvives": True}
    hold = lambda row: row["adversaryEscalates"] or not row["offRampSurvives"]
    if stable["component"] != unstable["component"] or hold(stable) or not hold(unstable):
        errors.append("component-evidence collision no longer produces opposite interaction reviews")

    lean_text = LEAN.read_text(encoding="utf-8")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if theorem_names != REQUIRED_THEOREMS:
        errors.append(
            f"Lean theorem surface mismatch: missing={sorted(REQUIRED_THEOREMS - theorem_names)}, "
            f"extra={sorted(theorem_names - REQUIRED_THEOREMS)}"
        )
    if "import AsiStackProofs.MilitaryInteractionReview" not in LEAN_ROOT.read_text(encoding="utf-8"):
        errors.append("root Lean module does not import MilitaryInteractionReview")
    for forbidden in (
        "weaponAuthorized",
        "lawfulUseEstablished",
        "meaningfulHumanControlEstablished",
        "escalationReduced",
        "strategicStabilityEstablished",
        "safetyEstablished",
        "supportStatePromoted",
        "releaseAuthorized",
        "externalEffectAllowed",
    ):
        if forbidden in lean_text:
            errors.append(f"forbidden overclaim surface present: {forbidden}")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or len(triage_rows) != 1:
        errors.append("proof manifest and triage must each contain exactly one target row")
    else:
        if (manifest_rows[0].get("module"), manifest_rows[0].get("formal_target"), manifest_rows[0].get("status")) != (MODULE, FORMAL_TARGET, "implemented"):
            errors.append("proof manifest target binding drifted")
        if (triage_rows[0].get("module"), triage_rows[0].get("formal_target"), triage_rows[0].get("target_status")) != (MODULE, FORMAL_TARGET, "implemented"):
            errors.append("proof triage target binding drifted")

    chapters = [chapter for part in load(STRUCTURE)["parts"] for chapter in part.get("chapters", [])]
    owners = [row for row in chapters if row.get("id") == "military-ai-autonomous-weapons-and-strategic-stability"]
    if len(owners) != 1:
        errors.append("book structure must contain exactly one owner chapter")
    elif not any(row.get("tag") == TAG and row.get("status") == "implemented" for row in owners[0].get("proof_targets", [])):
        errors.append("book structure target is not implemented")

    chapter_text = CHAPTER.read_text(encoding="utf-8")
    chapter_flat = re.sub(r"\s+", " ", chapter_text)
    dossier_flat = re.sub(r"\s+", " ", DOSSIER.read_text(encoding="utf-8"))
    for fragment in (
        TAG,
        "24 theorem declarations",
        "45 admission-axis mutations",
        "interface-presence impossibility result",
        "component-evidence impossibility result",
        "Chapter support remains `argument`",
        "Project Theseus public-safe simulation",
    ):
        if fragment not in chapter_flat:
            errors.append(f"chapter missing boundary fragment: {fragment}")
    for fragment in (
        "45 exact mutation dispositions",
        "three arithmetic monotonicity controls",
        "two impossibility results",
        "support_state_effect` remains `none",
    ):
        if fragment not in dossier_flat:
            errors.append(f"proof-model dossier missing fragment: {fragment}")
    if f"| `{TAG}` | `{MODULE}` | {FORMAL_TARGET} | implemented |" not in OUTLINE.read_text(encoding="utf-8"):
        errors.append("outline target row drifted")

    fail(errors)
    print(
        "Military-interaction review validation passed: eight-step finite lifecycle, "
        "45/45 exact repair dispositions, three monotonic rejection controls, two "
        "non-identifiability results, and 24 exact Lean declarations; no weapon "
        "authorization, lawful-use, meaningful-control, escalation-reduction, strategic-"
        "stability, safety, support, release, transfer, or external-effect claim."
    )


if __name__ == "__main__":
    main()

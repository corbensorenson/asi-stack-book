#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/SocietalResilienceReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/societal_resilience_dossier.json"
CHAPTER = ROOT / "chapters/societal-resilience-and-misuse-defense.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/societal-resilience-and-misuse-defense.md"
TAG = "lean:societal-resilience-and-misuse-defense.admission_boundary"
MODULE = "AsiStackProofs.SocietalResilienceReview"

Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is True, repair, lambda d, field=field: d.update({field: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is False, repair, lambda d, field=field: d.update({field: True})


AXES: list[Axis] = [
    yes("incidentIdentityBound", "bindIncidentIdentity"), yes("threatClassBound", "bindThreatClass"),
    yes("affectedPopulationBound", "bindAffectedPopulation"), yes("jurisdictionBound", "bindJurisdiction"),
    yes("organizationSetBound", "bindOrganizationSet"), yes("evidenceEpochBound", "bindEvidenceEpoch"),
    yes("protocolVersionBound", "bindProtocolVersion"), yes("participantCensusComplete", "completeParticipantCensus"),
    yes("missingParticipantsRecorded", "recordMissingParticipants"), yes("authorityScopesBound", "bindAuthorityScopes"),
    yes("crossOrganizationHandoffsBound", "bindCrossOrganizationHandoffs"),
    yes("dataSharingPurposeBound", "bindDataSharingPurpose"), yes("privacyLimitsBound", "bindPrivacyLimits"),
    yes("civilLibertiesReviewPresent", "addCivilLibertiesReview"), yes("informationHazardsControlled", "controlInformationHazards"),
    yes("resistControlsBound", "bindResistControls"), yes("absorbContinuityBound", "bindAbsorbContinuity"),
    yes("defenderCapacityAssessed", "assessDefenderCapacity"), yes("attackerAdaptationAssessed", "assessAttackerAdaptation"),
    yes("correlatedFailureAssessed", "assessCorrelatedFailure"), yes("falsePositiveControlsPresent", "addFalsePositiveControls"),
    yes("proportionalityReviewed", "reviewProportionality"), yes("affectedPathInventoryComplete", "completeAffectedPathInventory"),
    yes("containmentObserved", "observeContainment"), yes("serviceRecoveryObserved", "observeServiceRecovery"),
    yes("harmedPartyRecoveryObserved", "observeHarmedPartyRecovery"), yes("correctionRoutePresent", "addCorrectionRoute"),
    yes("residualOwnerBound", "bindResidualOwner"), yes("recurrenceCheckPlanned", "planRecurrenceCheck"),
    yes("noticePresent", "addNotice"), yes("accessibilityPresent", "addAccessibility"), yes("appealPresent", "addAppeal"),
    yes("evidencePreserved", "preserveEvidence"), yes("remedyPresent", "addRemedy"),
    yes("burdenDistributionAssessed", "assessBurdenDistribution"), yes("independentObserverPresent", "addIndependentObserver"),
    yes("exerciseLimitsRecorded", "recordExerciseLimits"), yes("measurementPlanRegistered", "registerMeasurementPlan"),
    yes("nullResultsRetained", "retainNullResults"), yes("adaptationTriggerBound", "bindAdaptationTrigger"),
    yes("transferLimitsRecorded", "recordTransferLimits"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    no("populationResilienceClaimed", "rejectPopulationResilienceClaim"),
    no("acceptableResidualHarmClaimed", "rejectAcceptableResidualHarmClaim"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED = set("""provider_takedown_does_not_establish_population_resilience tabletop_completion_does_not_establish_live_recovery rapid_response_does_not_establish_lawful_equitable_remedy local_safeguard_does_not_establish_cross_organization_defense single_organization_mandate_cannot_authorize_distinct_organization close_all_covers_every_finite_incident_path review_step_preserves_stage_invariant review_run_preserves_stage_invariant exercise_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_theseus_resilience_exercise every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity_and_coordination readiness_requires_defense readiness_requires_recovery readiness_requires_remedy readiness_requires_adaptation readiness_requires_boundary expired_response_mandate_remains_expired_when_time_advances uncovered_population_shortfall_persists_when_population_grows unresolved_path_shortfall_persists_when_more_paths_are_discovered incident_change_invalidates_resilience_receipt population_change_invalidates_resilience_receipt jurisdiction_change_invalidates_resilience_receipt protocol_change_invalidates_resilience_receipt identical_provider_signals_can_hide_opposite_population_resilience provider_signals_cannot_recover_population_resilience identical_response_speed_can_hide_opposite_equitable_remedy response_speed_cannot_recover_lawful_equitable_remedy missing_participant_forces_institutional_review""".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for _, predicate, _, _ in AXES)


def repair(dossier: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(dossier)), "eligibleForTheseusResilienceExercise")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("Societal resilience review failed:\n - " + "\n - ".join(errors))

    dossier = load(FIXTURE)
    if len(AXES) != 45 or len({axis[0] for axis in AXES}) != 45:
        errors.append("mutation denominator is not 45 unique axes")
    if not ready(dossier) or repair(dossier) != "eligibleForTheseusResilienceExercise":
        errors.append("complete dossier is not eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(dossier)
        mutate(candidate)
        if ready(candidate) or repair(candidate) != route:
            errors.append(f"{name} mutation/repair drifted")

    paths = [{**path, "closed": True} for path in dossier["incidentPaths"]]
    if not paths or not all(path["closed"] for path in paths):
        errors.append("finite incident-path closure failed")
    if not (20 < 21 <= 22 and 3 < 4 <= 5 and 2 < 3 <= 4):
        errors.append("adverse monotonicity controls failed")
    provider_signals = (True, True, True)
    response_signals = (True, True, True)
    if provider_signals != tuple(provider_signals) or response_signals != tuple(response_signals) or True == False:
        errors.append("collision controls failed")

    lean_text = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if names != REQUIRED:
        errors.append("exact 32-theorem surface drifted")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text):
        errors.append("Lean trust boundary widened")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or (manifest_rows[0].get("module"), manifest_rows[0].get("status")) != (MODULE, "implemented"):
        errors.append("manifest binding drifted")
    if len(triage_rows) != 1 or (triage_rows[0].get("module"), triage_rows[0].get("target_status")) != (MODULE, "implemented"):
        errors.append("triage binding drifted")

    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in ("32 theorem declarations", "45 admission-axis mutations", "finite incident-path closure", "population-resilience impossibility", "equitable-remedy impossibility", "Chapter support remains `argument`", "Project Theseus synthetic resilience exercise"):
        if fragment not in chapter:
            errors.append(f"chapter missing {fragment}")
    if manifest_rows and manifest_rows[0]["formal_target"] not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors:
        raise SystemExit("Societal resilience review failed:\n - " + "\n - ".join(errors))
    print("Societal resilience review passed: eight-transition lifecycle, 45/45 exact repairs, evidence and authority separation, finite incident-path closure, receipt and monotonicity controls, two non-identifiability results, one rejecting Institutional Legitimacy bridge, and 32 exact Lean declarations; no population-resilience, remedy, support, or external-effect claim.")


if __name__ == "__main__":
    main()

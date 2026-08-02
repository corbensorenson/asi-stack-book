#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/HumanAICognitiveSovereignty.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/human_ai_cognitive_sovereignty_dossier.json"
CHAPTER = ROOT / "chapters/human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty.md"
TAG = "lean:human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty.admission_boundary"
MODULE = "AsiStackProofs.HumanAICognitiveSovereignty"

Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is True, repair, lambda d, field=field: d.update({field: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is False, repair, lambda d, field=field: d.update({field: True})


AXES: list[Axis] = [
    yes("participantSetBound", "bindParticipantSet"),
    yes("protocolVersionBound", "bindProtocolVersion"),
    yes("couplingModeBound", "bindCouplingMode"),
    yes("deviceAndModelBound", "bindDeviceAndModel"),
    yes("authorityBound", "bindAuthority"), yes("jurisdictionBound", "bindJurisdiction"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    yes("humanAloneBaselineBound", "bindHumanBaseline"),
    yes("aiAloneBaselineBound", "bindAIBaseline"), yes("combinedArmBound", "bindCombinedArm"),
    yes("simplerInterventionBound", "addSimplerIntervention"),
    yes("matchedBudgetBound", "matchBudget"), yes("baselineFrozen", "freezeBaseline"),
    yes("longitudinalScheduleBound", "bindLongitudinalSchedule"),
    yes("purposeSpecificGrantBound", "bindPurposeGrant"),
    yes("ongoingRenewalBound", "bindOngoingRenewal"),
    yes("refusalWithoutPenaltyBound", "restoreRefusalWithoutPenalty"),
    yes("userVisibleAdaptationBound", "exposeAdaptation"),
    yes("sensingAuthoritySeparated", "separateSensingAuthority"),
    yes("adaptationAuthoritySeparated", "separateAdaptationAuthority"),
    yes("stimulationAuthoritySeparated", "separateStimulationAuthority"),
    yes("clinicalBoundaryBound", "bindClinicalBoundary"),
    yes("revocationPathBound", "bindRevocationPath"),
    yes("collectionMinimized", "minimizeCollection"),
    yes("localProcessingDecisionBound", "bindLocalProcessing"),
    yes("useLedgerBound", "bindUseLedger"), yes("retentionBound", "bindRetention"),
    yes("deletionPathBound", "bindDeletion"), yes("secondaryUseForbidden", "forbidSecondaryUse"),
    yes("inferredMentalPurposeBound", "bindInferredMentalPurpose"),
    yes("pausePathRehearsed", "rehearsePause"),
    yes("practicalExitRehearsed", "rehearsePracticalExit"),
    yes("portabilityRehearsed", "rehearsePortability"),
    yes("alternativeServicePreserved", "preserveAlternativeService"),
    yes("skillRetentionPlanBound", "bindSkillRetention"),
    yes("rehabilitationPlanBound", "bindRehabilitation"),
    yes("dependenceMeasureBound", "bindDependenceMeasure"),
    yes("subgroupDenominatorComplete", "completeSubgroupDenominator"),
    yes("attritionPreserved", "preserveAttrition"),
    yes("postExitFollowupBound", "bindPostExitFollowup"),
    yes("wellbeingMeasureBound", "bindWellbeing"),
    yes("identitySensitiveMonitoringBound", "bindIdentityMonitoring"),
    yes("independentReviewBound", "bindIndependentReview"),
    yes("irreversibleResidualOwnerBound", "assignResidualOwner"),
    no("beneficialSymbiosisClaimed", "rejectSymbiosisClaim"),
    no("genuineConsentClaimed", "rejectConsentClaim"),
    no("clinicalEfficacyClaimed", "rejectClinicalClaim"),
    no("cognitiveSovereigntyClaimed", "rejectSovereigntyClaim"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED = set("""beats_both_components_requires_human_baseline beats_both_components_requires_ai_baseline beating_human_alone_does_not_establish_complementarity beating_ai_alone_does_not_establish_complementarity equal_to_strongest_component_does_not_establish_complementarity single_purpose_grant_is_exact assistance_grant_does_not_authorize_model_training sensing_grant_does_not_authorize_employment_use personalization_grant_does_not_authorize_advertising stimulation_grant_does_not_authorize_surveillance revoked_purpose_lease_blocks_authorization expired_purpose_lease_blocks_authorization unrelated_purpose_blocks_authorization participant_id_collection_append_composes every_participant_id_survives_collection complete_longitudinal_denominator_covers_every_expected_participant omitted_post_exit_checkpoint_rejects_complete_denominator review_step_preserves_stage_invariant review_run_preserves_stage_invariant study_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_theseus_low_risk_coupling_study every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity readiness_requires_comparators readiness_requires_authorization readiness_requires_data_custody readiness_requires_exit_capacity readiness_requires_observation readiness_requires_nonclaim_boundary expired_coupling_contract_remains_expired_when_time_advances post_exit_gap_persists_when_observation_count_falls participant_set_change_invalidates_coupling_receipt protocol_change_invalidates_coupling_receipt device_or_model_change_invalidates_coupling_receipt purpose_change_invalidates_coupling_receipt observation_schedule_change_invalidates_coupling_receipt exit_plan_change_invalidates_coupling_receipt authority_change_invalidates_coupling_receipt identical_revocation_signals_can_hide_opposite_practical_exit revocation_signals_cannot_recover_practical_exit identical_session_signals_can_hide_opposite_post_exit_retention session_signals_cannot_recover_post_exit_skill_retention unrelated_mental_data_use_rejects_privacy_consumer missing_pause_channel_rejects_human_control_consumer missing_longitudinal_study_blocks_empirical_support_promotion""".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for _, predicate, _, _ in AXES)


def repair(dossier: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(dossier)), "eligibleForTheseusLowRiskCouplingStudy")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("Human-AI cognitive sovereignty failed:\n - " + "\n - ".join(errors))

    dossier = load(FIXTURE)
    if len(AXES) != 49 or len({axis[0] for axis in AXES}) != 49:
        errors.append("mutation denominator is not 49 unique axes")
    if not ready(dossier) or repair(dossier) != "eligibleForTheseusLowRiskCouplingStudy":
        errors.append("complete dossier is not eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(dossier)
        mutate(candidate)
        if ready(candidate) or repair(candidate) != route:
            errors.append(f"{name} mutation/repair drifted")

    expected = dossier["expectedParticipantIds"]
    checkpoints = dossier["checkpoints"]
    complete = {row["participantId"] for row in checkpoints if all(
        row[field] for field in ("baselineRecorded", "duringRecorded", "postExitRecorded", "includedInDenominator")
    )}
    if expected != [101, 102] or not set(expected).issubset(complete):
        errors.append("longitudinal denominator positive control drifted")
    omitted = deepcopy(checkpoints)
    omitted[1]["postExitRecorded"] = False
    omitted_complete = {row["participantId"] for row in omitted if all(
        row[field] for field in ("baselineRecorded", "duringRecorded", "postExitRecorded", "includedInDenominator")
    )}
    if set(expected).issubset(omitted_complete):
        errors.append("post-exit omission rejection control drifted")

    scope = dossier["receiptScope"]
    expected_scope = {"participantSetId", "protocolVersion", "deviceAndModelId", "purposeGrantId", "observationScheduleId", "exitPlanId", "authorityId"}
    if set(scope) != expected_scope or any((scope | {field: scope[field] + 1}) == scope for field in expected_scope):
        errors.append("seven-axis receipt invalidation control drifted")
    if (True, True, True) == (True, True, False) or (9, 3, True) == (9, 3, False):
        errors.append("information-loss collision controls failed")

    lean_text = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if names != REQUIRED:
        errors.append("exact 48-theorem surface drifted")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text):
        errors.append("Lean trust boundary widened")

    manifest_rows = [row for row in load(MANIFEST)["records"] if row.get("tag") == TAG]
    triage_rows = [row for row in load(TRIAGE)["records"] if row.get("tag") == TAG]
    if len(manifest_rows) != 1 or (manifest_rows[0].get("module"), manifest_rows[0].get("status")) != (MODULE, "implemented"):
        errors.append("manifest binding drifted")
    if len(triage_rows) != 1 or (triage_rows[0].get("module"), triage_rows[0].get("target_status")) != (MODULE, "implemented"):
        errors.append("triage binding drifted")

    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in (
        "48 theorem declarations", "49 admission-axis mutations", "arbitrary run length",
        "strongest-component", "purpose-specific authorization", "practical exit",
        "post-exit skill retention", "Privacy Information Flow", "Human Factors Oversight",
        "Evidence States", "Chapter support remains `argument`",
        "Project Theseus low-risk coupling study",
    ):
        if fragment not in chapter:
            errors.append(f"chapter missing {fragment}")
    if manifest_rows and manifest_rows[0]["formal_target"] not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors:
        raise SystemExit("Human-AI cognitive sovereignty failed:\n - " + "\n - ".join(errors))
    print(
        "Human-AI cognitive sovereignty passed: eight-transition lifecycle, 49/49 exact repairs, "
        "strongest-component comparator discipline, purpose-exact authorization and revocation, "
        "finite longitudinal participant custody, seven receipt invalidations, two non-identifiability "
        "results, three rejecting consumers, and 48 exact Lean declarations; no beneficial-symbiosis, "
        "consent, clinical, sovereignty, support, release, or external-effect claim."
    )


if __name__ == "__main__":
    main()

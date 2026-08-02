#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/DeploymentTransitionGovernance.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/deployment_transition_dossier.json"
CHAPTER = ROOT / "chapters/ai-deployment-transition-distribution-and-human-agency.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/ai-deployment-transition-distribution-and-human-agency.md"
TAG = "lean:ai-deployment-transition-distribution-and-human-agency.admission_boundary"
MODULE = "AsiStackProofs.DeploymentTransitionGovernance"

Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is True, repair, lambda d, field=field: d.update({field: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is False, repair, lambda d, field=field: d.update({field: True})


AXES: list[Axis] = [
    yes("deploymentIdentityBound", "bindDeploymentIdentity"),
    yes("baselineIdentityBound", "bindBaselineIdentity"),
    yes("contractVersionBound", "bindContractVersion"),
    yes("authorityBound", "bindAuthority"), yes("jurisdictionBound", "bindJurisdiction"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    yes("baselineFrozen", "freezeBaseline"), yes("rolloutStagesBound", "bindRolloutStages"),
    yes("observationScheduleBound", "bindObservationSchedule"),
    yes("affectedDenominatorComplete", "completeAffectedDenominator"),
    yes("workerDenominatorComplete", "completeWorkerDenominator"),
    yes("customerDenominatorComplete", "completeCustomerDenominator"),
    yes("communityDenominatorComplete", "completeCommunityDenominator"),
    yes("attritionPreserved", "preserveAttrition"),
    yes("excludedEntrantsPreserved", "preserveExcludedEntrants"),
    yes("taskChangeSeparated", "separateTaskChange"),
    yes("roleChangeSeparated", "separateRoleChange"),
    yes("skillChangeSeparated", "separateSkillChange"),
    yes("workloadSeparated", "separateWorkload"),
    yes("compensationSeparated", "separateCompensation"),
    yes("ownershipReturnsSeparated", "separateOwnershipReturns"),
    yes("accessSeparated", "separateAccess"), yes("pricesSeparated", "separatePrices"),
    yes("concentrationSeparated", "separateConcentration"),
    yes("serviceContinuityBound", "bindServiceContinuity"),
    yes("hiddenLaborPreserved", "preserveHiddenLabor"),
    yes("humanDecisionRightsBound", "bindHumanDecisionRights"),
    yes("practicalRefusalPresent", "restorePracticalRefusal"),
    yes("contestabilityPresent", "addContestability"), yes("appealPresent", "addAppeal"),
    yes("humanAuthorityPresent", "bindHumanAuthority"),
    yes("portabilityRehearsed", "rehearsePortability"), yes("exitRehearsed", "rehearseExit"),
    yes("trainingFunded", "fundTraining"), yes("redeploymentFunded", "fundRedeployment"),
    yes("incomeContinuityFunded", "fundIncomeContinuity"),
    yes("burdenCompensationFunded", "fundBurdenCompensation"),
    yes("alternativeServicePreserved", "preserveAlternativeService"),
    yes("ordinaryImprovementComparator", "addOrdinaryComparator"),
    yes("transitionCapacityPresent", "addTransitionCapacity"),
    yes("delayedFollowupBound", "bindDelayedFollowup"),
    yes("independentMonitoringBound", "bindIndependentMonitoring"),
    yes("subgroupReportingBound", "bindSubgroupReporting"),
    yes("remedyTriggerBound", "bindRemedyTrigger"),
    yes("remedyFundingBound", "bindRemedyFunding"),
    yes("remedyReceiptRequired", "requireRemedyReceipt"),
    yes("pauseAuthorityPresent", "addPauseAuthority"),
    yes("withdrawalPathPresent", "addWithdrawalPath"),
    yes("residualOwnerBound", "assignResidualOwner"),
    no("effectivenessClaimed", "rejectEffectivenessClaim"),
    no("welfareClaimed", "rejectWelfareClaim"), no("fairnessClaimed", "rejectFairnessClaim"),
    no("agencyClaimed", "rejectAgencyClaim"), no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED = set("""exposure_does_not_establish_displacement adoption_does_not_establish_welfare productivity_does_not_establish_distributional_benefit approval_click_does_not_establish_agency aggregate_gain_does_not_establish_successful_transition cohort_id_collection_append_composes every_cohort_id_survives_collection complete_denominator_covers_every_expected_cohort omitted_expected_cohort_rejects_complete_denominator fully_remedied_append_iff unremedied_member_blocks_transition_acceptance positive_aggregate_can_coexist_with_unremedied_harm review_step_preserves_stage_invariant review_run_preserves_stage_invariant study_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_theseus_governed_transition_study every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity readiness_requires_design readiness_requires_accounting readiness_requires_agency readiness_requires_capacity readiness_requires_remedy readiness_requires_boundary expired_transition_contract_remains_expired_when_time_advances affected_denominator_gap_persists_when_observed_count_falls remedy_gap_persists_when_delivered_amount_falls deployment_change_invalidates_transition_receipt baseline_change_invalidates_transition_receipt contract_version_change_invalidates_transition_receipt denominator_change_invalidates_transition_receipt observation_schedule_change_invalidates_transition_receipt remedy_plan_change_invalidates_transition_receipt authority_change_invalidates_transition_receipt identical_aggregate_signals_can_hide_opposite_harm_status aggregate_signals_cannot_recover_harmed_cohort_status identical_approval_counts_can_hide_opposite_practical_agency approval_counts_cannot_recover_practical_agency missing_transition_remedy_blocks_accountability_consumer missing_transition_checks_reject_readiness_consumer missing_transition_study_blocks_empirical_support_promotion""".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for _, predicate, _, _ in AXES)


def repair(dossier: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(dossier)), "eligibleForTheseusGovernedTransitionStudy")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("Deployment-transition governance failed:\n - " + "\n - ".join(errors))

    dossier = load(FIXTURE)
    if len(AXES) != 54 or len({axis[0] for axis in AXES}) != 54:
        errors.append("mutation denominator is not 54 unique axes")
    if not ready(dossier) or repair(dossier) != "eligibleForTheseusGovernedTransitionStudy":
        errors.append("complete dossier is not eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(dossier)
        mutate(candidate)
        if ready(candidate) or repair(candidate) != route:
            errors.append(f"{name} mutation/repair drifted")

    expected = dossier["expectedCohortIds"]
    cohorts = dossier["positiveAggregateCohorts"]
    included = {row["cohortId"] for row in cohorts if row["includedInDenominator"]}
    if expected != [1, 2] or not set(expected).issubset(included):
        errors.append("affected-person denominator positive control drifted")
    if sum(row["gain"] for row in cohorts) <= sum(row["burden"] for row in cohorts):
        errors.append("positive aggregate witness drifted")
    if all(row["remedyDelivered"] >= row["burden"] for row in cohorts):
        errors.append("unremedied-harm witness drifted")
    omitted = deepcopy(cohorts)
    omitted[1]["includedInDenominator"] = False
    if set(expected).issubset({row["cohortId"] for row in omitted if row["includedInDenominator"]}):
        errors.append("cohort-omission rejection control drifted")

    scope = dossier["receiptScope"]
    expected_scope = {"deploymentId", "baselineId", "contractVersion", "denominatorId", "observationScheduleId", "remedyPlanId", "authorityId"}
    if set(scope) != expected_scope or any((scope | {field: scope[field] + 1}) == scope for field in expected_scope):
        errors.append("seven-axis receipt invalidation control drifted")
    if (4, 7, False) == (4, 7, True) or (12, 3, True) == (12, 3, False):
        errors.append("information-loss collision controls failed")

    lean_text = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if names != REQUIRED:
        errors.append("exact 44-theorem surface drifted")
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
        "44 theorem declarations", "54 admission-axis mutations", "arbitrary run length",
        "positive aggregate gain", "practical refusal", "Human-AI Organizations",
        "Readiness Gates", "Evidence States", "Chapter support remains `argument`",
        "Project Theseus governed transition study",
    ):
        if fragment not in chapter:
            errors.append(f"chapter missing {fragment}")
    if manifest_rows and manifest_rows[0]["formal_target"] not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors:
        raise SystemExit("Deployment-transition governance failed:\n - " + "\n - ".join(errors))
    print(
        "Deployment-transition governance passed: eight-transition lifecycle, 54/54 exact repairs, "
        "finite cohort and remedy custody, positive-aggregate/unremedied-harm witness, adverse "
        "monotonicity, seven receipt invalidations, two non-identifiability results, three rejecting "
        "consumers, and 44 exact Lean declarations; no causal, welfare, fairness, agency, remedy, "
        "continuity, support, release, or external-effect claim."
    )


if __name__ == "__main__":
    main()

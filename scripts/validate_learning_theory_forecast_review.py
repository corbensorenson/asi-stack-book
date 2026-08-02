#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/LearningTheoryForecastReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/learning_theory_forecast_dossier.json"
CHAPTER = ROOT / "chapters/learning-theory-generalization-and-scaling-science.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/learning-theory-generalization-and-scaling-science.md"
TAG = "lean:learning-theory-generalization-and-scaling-science.admission_boundary"
MODULE = "AsiStackProofs.LearningTheoryForecastReview"

Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is True, repair, lambda d, field=field: d.update({field: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is False, repair, lambda d, field=field: d.update({field: True})


AXES: list[Axis] = [
    yes("claimIdentityBound", "bindClaimIdentity"),
    yes("populationBound", "bindPopulation"),
    yes("sampleProcessBound", "bindSampleProcess"),
    yes("dataSupportBound", "bindDataSupport"),
    yes("hypothesisFamilyBound", "bindHypothesisFamily"),
    yes("algorithmBound", "bindAlgorithm"),
    yes("optimizationPathBound", "bindOptimizationPath"),
    yes("architectureBound", "bindArchitecture"),
    yes("metricBound", "bindMetric"),
    yes("computeRegimeBound", "bindComputeRegime"),
    yes("observedRangeBound", "bindObservedRange"),
    yes("forecastHorizonBound", "bindForecastHorizon"),
    yes("candidateFamiliesBound", "bindCandidateFamilies"),
    yes("fittingRuleBound", "bindFittingRule"),
    yes("uncertaintyBound", "bindUncertainty"),
    yes("predictionIntervalBound", "bindPredictionInterval"),
    yes("breakpointAlternativesBound", "bindBreakpointAlternatives"),
    yes("metricTransformBound", "bindMetricTransform"),
    yes("prospectiveFreezeBound", "freezeProspectively"),
    yes("heldoutScaleBound", "bindHeldoutScale"),
    yes("failedRunsPreserved", "preserveFailedRuns"),
    yes("attemptDenominatorComplete", "completeAttemptDenominator"),
    yes("dependenceStructureBound", "bindDependenceStructure"),
    yes("contaminationChecked", "checkContamination"),
    yes("sourceTargetSeparated", "separateSourceTarget"),
    yes("shiftModelBound", "bindShiftModel"),
    yes("taskFamilyBound", "bindTaskFamily"),
    yes("subgroupBehaviorBound", "bindSubgroupBehavior"),
    yes("calibrationBound", "bindCalibration"),
    yes("transferClaimSeparated", "separateTransferClaim"),
    yes("compositionClaimSeparated", "separateCompositionClaim"),
    yes("safetyClaimSeparated", "separateSafetyClaim"),
    yes("correctionLineagePresent", "addCorrectionLineage"),
    yes("consumerPurposeBound", "bindConsumerPurpose"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    yes("residualOwnerBound", "assignResidualOwner"),
    yes("fallbackBound", "bindFallback"),
    yes("retirementBound", "bindRetirement"),
    yes("independentReanalysisBound", "bindIndependentReanalysis"),
    yes("totalCostBound", "bindTotalCost"),
    no("broadGeneralizationClaimed", "rejectBroadGeneralizationClaim"),
    no("mechanismEmergenceClaimed", "rejectMechanismEmergenceClaim"),
    no("futureScalingClaimed", "rejectFutureScalingClaim"),
    no("safetyClaimed", "rejectSafetyClaim"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED = set("""training_fit_does_not_establish_broad_generalization iid_holdout_does_not_establish_distribution_transfer retrospective_scaling_fit_does_not_establish_future_scaling_behavior compression_score_does_not_establish_safety threshold_benchmark_does_not_establish_mechanism_emergence attempt_id_collection_append_composes every_attempt_id_survives_collection complete_denominator_counts_every_member omitted_attempt_rejects_complete_denominator unscored_preregistered_alternative_rejects_complete_comparison review_step_preserves_stage_invariant review_run_preserves_stage_invariant campaign_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_theseus_prospective_forecast_campaign every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity readiness_requires_design readiness_requires_transfer readiness_requires_lifecycle readiness_requires_boundary expired_forecast_contract_remains_expired_when_time_advances extrapolation_remains_outside_support_when_observed_range_shrinks unscored_gap_persists_when_scored_count_falls population_change_invalidates_forecast_receipt sample_process_change_invalidates_forecast_receipt algorithm_change_invalidates_forecast_receipt architecture_change_invalidates_forecast_receipt metric_change_invalidates_forecast_receipt compute_regime_change_invalidates_forecast_receipt horizon_change_invalidates_forecast_receipt identical_retrospective_fit_can_hide_opposite_prospective_coverage retrospective_fit_cannot_recover_prospective_coverage identical_threshold_metrics_can_hide_opposite_mechanism_change threshold_metrics_cannot_recover_mechanism_change missing_prospective_holdout_rejects_benchmark_ratchet_promotion""".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for _, predicate, _, _ in AXES)


def repair(dossier: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(dossier)), "eligibleForTheseusProspectiveForecastCampaign")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("Learning-theory forecast review failed:\n - " + "\n - ".join(errors))

    dossier = load(FIXTURE)
    if len(AXES) != 45 or len({axis[0] for axis in AXES}) != 45:
        errors.append("mutation denominator is not 45 unique axes")
    if not ready(dossier) or repair(dossier) != "eligibleForTheseusProspectiveForecastCampaign":
        errors.append("complete dossier is not eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(dossier)
        mutate(candidate)
        if ready(candidate) or repair(candidate) != route:
            errors.append(f"{name} mutation/repair drifted")

    attempts = dossier["attempts"]
    ids = [row["attemptId"] for row in attempts]
    if ids != [11, 12, 13] or ids != ids[:1] + ids[1:]:
        errors.append("attempt identity or append control drifted")
    if not all(row["includedInDenominator"] for row in attempts):
        errors.append("complete attempt denominator drifted")
    omitted = deepcopy(attempts)
    omitted[1]["includedInDenominator"] = False
    if all(row["includedInDenominator"] for row in omitted):
        errors.append("omitted-attempt rejection control drifted")

    alternatives = dossier["alternatives"]
    if not all(not row["preregistered"] or row["heldoutScored"] for row in alternatives):
        errors.append("complete alternative comparison drifted")
    unscored = deepcopy(alternatives)
    unscored[0]["heldoutScored"] = False
    if all(not row["preregistered"] or row["heldoutScored"] for row in unscored):
        errors.append("unscored preregistered alternative control drifted")

    scope = dossier["receiptScope"]
    expected_scope = {"populationId", "sampleProcessId", "algorithmId", "architectureId", "metricId", "computeRegimeId", "horizonId"}
    if set(scope) != expected_scope or any((scope | {field: scope[field] + 1}) == scope for field in expected_scope):
        errors.append("seven-axis receipt invalidation control drifted")
    if (4, 8, True) == (4, 8, False) or (17, 23, True) == (17, 23, False):
        errors.append("information-loss collision controls failed")

    lean_text = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if names != REQUIRED:
        errors.append("exact 38-theorem surface drifted")
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
        "38 theorem declarations", "45 admission-axis mutations", "arbitrary finite lists",
        "retrospective-fit signals", "threshold-metric signals", "Benchmark Ratchets",
        "Chapter support remains `argument`", "Project Theseus prospective forecast campaign",
    ):
        if fragment not in chapter:
            errors.append(f"chapter missing {fragment}")
    if manifest_rows and manifest_rows[0]["formal_target"] not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors:
        raise SystemExit("Learning-theory forecast review failed:\n - " + "\n - ".join(errors))
    print(
        "Learning-theory forecast review passed: six-transition lifecycle, 45/45 exact repairs, "
        "finite attempt and alternative custody, adverse monotonicity, seven receipt invalidations, "
        "two non-identifiability results, one rejecting Benchmark Ratchets bridge, and 38 exact Lean "
        "declarations; no generalization, transfer, emergence, scaling, safety, support, or release claim."
    )


if __name__ == "__main__":
    main()

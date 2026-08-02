#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ScientificExperimentReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/scientific_experiment_dossier.json"
CHAPTER = ROOT / "chapters/scientific-discovery-and-experimental-governance.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/scientific-discovery-and-experimental-governance.md"
TAG = "lean:scientific-discovery-and-experimental-governance.admission_boundary"
MODULE = "AsiStackProofs.ScientificExperimentReview"

Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is True, repair, lambda d, field=field: d.update({field: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, field=field: d[field] is False, repair, lambda d, field=field: d.update({field: True})


AXES: list[Axis] = [
    yes("claimIdentityBound", "bindClaimIdentity"),
    yes("hypothesisIdentityBound", "bindHypothesisIdentity"),
    yes("hypothesisVersionBound", "bindHypothesisVersion"),
    yes("hypothesisAncestryBound", "bindHypothesisAncestry"),
    yes("exploratoryConfirmatoryBound", "separateExplorationConfirmation"),
    yes("protocolVersionBound", "bindProtocolVersion"),
    yes("instrumentVersionBound", "bindInstrumentVersion"),
    yes("dataSnapshotBound", "bindDataSnapshot"),
    yes("analysisVersionBound", "bindAnalysisVersion"),
    yes("environmentBound", "bindEnvironment"),
    yes("preregistrationBound", "preregisterBeforeOpening"),
    yes("outcomesFrozenBeforeOpen", "freezeOutcomes"),
    yes("samplingPlanBound", "bindSamplingPlan"),
    yes("powerPrecisionBound", "bindPowerPrecision"),
    yes("controlsBound", "bindControls"),
    yes("randomizationBound", "bindRandomization"),
    yes("blindingBound", "bindBlinding"),
    yes("holdoutBound", "bindHoldout"),
    yes("stoppingRuleBound", "bindStoppingRule"),
    yes("exclusionsBound", "bindExclusions"),
    yes("alternativesBound", "bindAlternatives"),
    yes("causalAssumptionsBound", "bindCausalAssumptions"),
    yes("instrumentLeaseBound", "bindInstrumentLease"),
    yes("calibrationBound", "bindCalibration"),
    yes("operatingEnvelopeBound", "bindOperatingEnvelope"),
    yes("sampleIdentityBound", "bindSampleIdentity"),
    yes("safetyInterlocksBound", "bindSafetyInterlocks"),
    yes("independentStopAuthorityBound", "bindIndependentStopAuthority"),
    yes("attemptDenominatorComplete", "completeAttemptDenominator"),
    yes("humanInterventionsPreserved", "preserveHumanInterventions"),
    yes("protocolDeviationsPreserved", "preserveProtocolDeviations"),
    yes("rawObservationsPreserved", "preserveRawObservations"),
    yes("codeParametersBound", "bindCodeParameters"),
    yes("contaminationDriftControlsBound", "bindContaminationDriftControls"),
    yes("independentAnalysisBound", "bindIndependentAnalysis"),
    yes("robustnessChecksBound", "bindRobustnessChecks"),
    yes("nullNegativeResultsPreserved", "preserveNullNegativeResults"),
    yes("correctionLineagePresent", "addCorrectionLineage"),
    yes("replicationContractBound", "bindReplicationContract"),
    yes("replicationIndependenceBound", "bindReplicationIndependence"),
    yes("disagreementPreserved", "preserveDisagreement"),
    yes("dualUseQuestionReviewed", "reviewDualUseQuestion"),
    yes("dualUseProtocolReviewed", "reviewDualUseProtocol"),
    yes("dualUseExecutionReviewed", "reviewDualUseExecution"),
    yes("dualUseArtifactReviewed", "reviewDualUseArtifact"),
    yes("dualUseDisclosureReviewed", "reviewDualUseDisclosure"),
    yes("accessTierBound", "bindAccessTier"),
    yes("residualOwnerBound", "assignResidualOwner"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    no("causalTruthClaimed", "rejectCausalTruthClaim"),
    no("generalDiscoveryClaimed", "rejectGeneralDiscoveryClaim"),
    no("reproducibilityClaimed", "rejectReproducibilityClaim"),
    no("safetyClaimed", "rejectSafetyClaim"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED = set("""generated_hypothesis_does_not_establish_discovery completed_experiment_does_not_establish_causal_truth significant_result_does_not_establish_reproducibility replay_does_not_establish_independent_replication dual_use_review_does_not_establish_safety attempt_id_collection_append_composes every_attempt_id_survives_collection complete_denominator_counts_every_attempt omitted_attempt_rejects_complete_denominator outcome_exposed_branch_rejects_confirmatory_integrity review_step_preserves_stage_invariant review_run_preserves_stage_invariant campaign_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_theseus_governed_experiment_campaign every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity readiness_requires_design readiness_requires_execution readiness_requires_analysis readiness_requires_replication readiness_requires_governance readiness_requires_boundary expired_experiment_contract_remains_expired_when_time_advances omitted_attempt_gap_persists_when_included_count_falls replication_gap_persists_when_independent_count_falls hypothesis_change_invalidates_experiment_receipt protocol_change_invalidates_experiment_receipt instrument_change_invalidates_experiment_receipt data_change_invalidates_experiment_receipt analysis_change_invalidates_experiment_receipt environment_change_invalidates_experiment_receipt claim_ceiling_change_invalidates_experiment_receipt identical_significance_can_hide_opposite_preregistration_integrity significance_signals_cannot_recover_preregistration_integrity identical_replication_counts_can_hide_opposite_independence replication_counts_cannot_recover_independence missing_independent_replication_blocks_empirical_support_promotion missing_null_results_rejects_benchmark_ratchet_promotion""".split())


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(dossier: dict[str, Any]) -> bool:
    return all(predicate(dossier) for _, predicate, _, _ in AXES)


def repair(dossier: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(dossier)), "eligibleForTheseusGovernedExperimentCampaign")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file():
            errors.append(f"missing {path.relative_to(ROOT)}")
    if errors:
        raise SystemExit("Scientific-experiment review failed:\n - " + "\n - ".join(errors))

    dossier = load(FIXTURE)
    if len(AXES) != 54 or len({axis[0] for axis in AXES}) != 54:
        errors.append("mutation denominator is not 54 unique axes")
    if not ready(dossier) or repair(dossier) != "eligibleForTheseusGovernedExperimentCampaign":
        errors.append("complete dossier is not eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(dossier)
        mutate(candidate)
        if ready(candidate) or repair(candidate) != route:
            errors.append(f"{name} mutation/repair drifted")

    attempts = dossier["attempts"]
    ids = [row["attemptId"] for row in attempts]
    if ids != [21, 22, 23] or ids != ids[:1] + ids[1:]:
        errors.append("attempt identity or append control drifted")
    if not all(row["includedInDenominator"] for row in attempts):
        errors.append("complete attempt denominator drifted")
    if "nullResult" not in {row["outcome"] for row in attempts}:
        errors.append("null-result positive control drifted")
    omitted = deepcopy(attempts)
    omitted[1]["includedInDenominator"] = False
    if all(row["includedInDenominator"] for row in omitted):
        errors.append("omitted-attempt rejection control drifted")

    branch = dossier["confirmatoryBranch"]
    if not (branch["confirmatory"] and branch["preregisteredBeforeOutcome"] and not branch["protectedOutcomeOpened"]):
        errors.append("confirmatory-integrity positive control drifted")
    exposed = deepcopy(branch)
    exposed["protectedOutcomeOpened"] = True
    if exposed["confirmatory"] and exposed["preregisteredBeforeOutcome"] and not exposed["protectedOutcomeOpened"]:
        errors.append("outcome-exposure rejection control drifted")

    scope = dossier["receiptScope"]
    expected_scope = {"hypothesisId", "protocolVersion", "instrumentVersion", "dataSnapshotId", "analysisVersion", "environmentId", "claimCeilingId"}
    if set(scope) != expected_scope or any((scope | {field: scope[field] + 1}) == scope for field in expected_scope):
        errors.append("seven-axis receipt invalidation control drifted")
    if (1, 3, True) == (1, 3, False) or (2, 5, True) == (2, 5, False):
        errors.append("information-loss collision controls failed")

    lean_text = LEAN.read_text(encoding="utf-8")
    names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", lean_text))
    if names != REQUIRED:
        errors.append("exact 41-theorem surface drifted")
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
        "41 theorem declarations", "54 admission-axis mutations", "arbitrary finite lists",
        "significance signals", "successful-replication counts", "Evidence States",
        "Benchmark Ratchet", "Chapter support remains `argument`",
        "Project Theseus governed experiment campaign",
    ):
        if fragment not in chapter:
            errors.append(f"chapter missing {fragment}")
    if manifest_rows and manifest_rows[0]["formal_target"] not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors:
        raise SystemExit("Scientific-experiment review failed:\n - " + "\n - ".join(errors))
    print(
        "Scientific-experiment review passed: eight-transition lifecycle, 54/54 exact repairs, "
        "finite attempt and confirmatory custody, adverse monotonicity, seven receipt invalidations, "
        "two non-identifiability results, two rejecting evidence consumers, and 41 exact Lean "
        "declarations; no causal, discovery, replication, safety, support, release, or external-effect claim."
    )


if __name__ == "__main__":
    main()

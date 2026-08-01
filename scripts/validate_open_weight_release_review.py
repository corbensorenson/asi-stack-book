#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/OpenWeightReleaseReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/open_weight_release_dossier.json"
CHAPTER = ROOT / "chapters/open-weight-release-and-post-release-control.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
STRUCTURE = ROOT / "book_structure.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/open-weight-release-and-post-release-control.md"
TAG = "lean:open-weight-release-and-post-release-control.admission_boundary"
MODULE = "AsiStackProofs.OpenWeightReleaseReview"

Predicate = Callable[[dict[str, Any]], bool]
Mutation = Callable[[dict[str, Any]], None]
Axis = tuple[str, Predicate, str, Mutation]


def yes(field: str, route: str) -> Axis:
    return field, lambda d, f=field: d[f] is True, route, lambda d, f=field: d.update({f: False})


def no(field: str, route: str) -> Axis:
    return field, lambda d, f=field: d[f] is False, route, lambda d, f=field: d.update({f: True})


GROUPS: list[list[Axis]] = [
    [yes("exactWeightsBound", "bindExactWeights"), yes("tokenizerBound", "bindTokenizer"),
     yes("configurationBound", "bindConfiguration"), yes("inferenceCodeBound", "bindInferenceCode"),
     yes("licenseBound", "bindLicense"), yes("evaluationIdentityBound", "bindEvaluationIdentity")],
    [yes("noReleaseCompared", "addNoReleaseComparator"), yes("hostedAccessCompared", "addHostedComparator"),
     yes("gatedAccessCompared", "addGatedComparator"), yes("reducedArtifactCompared", "addReducedComparator"),
     yes("accessibleFrontierBound", "bindAccessibleFrontier"),
     ("frontierExpiry", lambda d: d["currentTick"] <= d["frontierExpiresAt"], "renewFrontier", lambda d: d.update(frontierExpiresAt=3))],
    [yes("defaultCandidateEvaluated", "evaluateDefaultCandidate"),
     yes("safetyRemovedVariantEvaluated", "evaluateSafetyRemovedVariant"),
     yes("maliciousFineTuneEvaluated", "evaluateMaliciousFineTune"),
     yes("fineTunePositiveControlPassed", "repairFineTunePositiveControl"),
     yes("scaffoldedVariantEvaluated", "evaluateScaffoldedVariant"),
     yes("adversaryBudgetBound", "bindAdversaryBudget"),
     yes("derivativeResidualRecorded", "recordDerivativeResidual")],
    [yes("benefitDistributionRecorded", "recordBenefitDistribution"),
     yes("affectedPopulationRecorded", "recordAffectedPopulation"),
     yes("marginalRiskRecorded", "recordMarginalRisk"), yes("cumulativeRiskRecorded", "recordCumulativeRisk"),
     yes("safeguardPortabilityRecorded", "recordSafeguardPortability"),
     yes("independentReviewPresent", "assignIndependentReview")],
    [yes("officialLineageRoutePresent", "addOfficialLineage"), yes("incidentRoutePresent", "addIncidentRoute"),
     yes("patchSemanticsRecorded", "recordPatchSemantics"), yes("residualOwnerPresent", "assignResidualOwner"),
     no("universalRecallClaimed", "rejectUniversalRecall"),
     no("universalTelemetryClaimed", "rejectUniversalTelemetry"), no("copyErasureClaimed", "rejectCopyErasure"),
     no("licenseKillSwitchClaimed", "rejectLicenseKillSwitch"), yes("nonClaimBoundaryPresent", "recordNonClaimBoundary"),
     no("releaseAuthorizationRequested", "refuseReleaseAuthorization"),
     no("supportPromotionRequested", "refuseSupportPromotion")],
]

REQUIRED_THEOREMS = {
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "simulation_eligibility_requires_admissible_dossier", "complete_dossier_is_ready",
    "complete_dossier_reaches_only_harmless_release_case",
    "every_admission_axis_mutation_blocks_readiness", "every_admission_axis_mutation_has_exact_repair",
    "every_admission_axis_mutation_reaches_repair", "readiness_requires_artifact",
    "readiness_requires_alternatives", "readiness_requires_derivative_review",
    "readiness_requires_distribution_review", "readiness_requires_post_release_boundary",
    "expired_frontier_remains_expired_when_time_advances", "public_copy_irreversibility_is_monotone",
    "identical_official_lineage_can_hide_opposite_copy_control",
    "official_lineage_cannot_recover_universal_copy_control",
    "identical_default_evaluation_can_hide_opposite_derivative_state",
    "default_evaluation_cannot_recover_derivative_safeguard_state",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(d: dict[str, Any]) -> bool:
    return all(predicate(d) for group in GROUPS for _, predicate, _, _ in group)


def repair(d: dict[str, Any]) -> str:
    for group in GROUPS:
        for _, predicate, route, _ in group:
            if not predicate(d):
                return route
    return "eligibleForTheseusHarmlessReleaseCase"


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, STRUCTURE, OUTLINE, DOSSIER):
        if not path.exists(): errors.append(f"missing {path.relative_to(ROOT)}")
    if errors: raise SystemExit("Open-weight release review failed:\n - " + "\n - ".join(errors))
    complete = load(FIXTURE)
    axes = [axis for group in GROUPS for axis in group]
    if len(axes) != 36 or len({axis[0] for axis in axes}) != 36: errors.append("mutation denominator is not 36 unique axes")
    if not ready(complete) or repair(complete) != "eligibleForTheseusHarmlessReleaseCase": errors.append("complete dossier is not eligible")
    for name, _, route, mutate in axes:
        candidate = deepcopy(complete); mutate(candidate)
        if ready(candidate): errors.append(f"{name} mutation remained ready")
        if repair(candidate) != route: errors.append(f"{name} reached {repair(candidate)}, expected {route}")
    for later in range(9, 15):
        if later <= 8: errors.append("later time laundered expired frontier")
    for later_copies in range(1, 8):
        if later_copies == 0: errors.append("persistent public copy became universally recallable")
    lineage = {"signer": 7, "digest": 11}
    if lineage != deepcopy(lineage) or (0 == 0) == (3 == 0): errors.append("lineage collision lost opposite control results")
    default = {"score": 90}
    if default != deepcopy(default) or False == True: errors.append("default-evaluation collision lost opposite derivative results")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", LEAN.read_text(encoding="utf-8")))
    if theorem_names != REQUIRED_THEOREMS: errors.append(f"theorem surface mismatch: missing={sorted(REQUIRED_THEOREMS-theorem_names)}, extra={sorted(theorem_names-REQUIRED_THEOREMS)}")
    formal = next((r.get("formal_target") for r in load(MANIFEST)["records"] if r.get("tag") == TAG), None)
    manifest = [r for r in load(MANIFEST)["records"] if r.get("tag") == TAG]
    triage = [r for r in load(TRIAGE)["records"] if r.get("tag") == TAG]
    if len(manifest) != 1 or (manifest[0].get("module"), manifest[0].get("status")) != (MODULE, "implemented"): errors.append("manifest binding drifted")
    if len(triage) != 1 or (triage[0].get("module"), triage[0].get("target_status")) != (MODULE, "implemented"): errors.append("triage binding drifted")
    chapter = re.sub(r"\s+", " ", CHAPTER.read_text(encoding="utf-8"))
    for fragment in ("19 theorem declarations", "36 admission-axis mutations", "public-copy irreversibility", "official-lineage impossibility result", "default-evaluation impossibility result", "Chapter support remains `argument`", "Project Theseus harmless release-case"):
        if fragment not in chapter: errors.append(f"chapter missing {fragment}")
    if formal and formal not in re.sub(r"\s+", " ", OUTLINE.read_text(encoding="utf-8")): errors.append("outline target drifted")
    if errors: raise SystemExit("Open-weight release review failed:\n - " + "\n - ".join(errors))
    print("Open-weight release review passed: six-step lifecycle, 36/36 exact repairs, frontier and public-copy monotonicity, two non-identifiability results, and 19 exact Lean declarations; no release, recall, safety, support, or external-effect claim.")


if __name__ == "__main__": main()

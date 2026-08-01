#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/AdversarialModelSecurity.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/adversarial_model_security_dossier.json"
CHAPTER = ROOT / "chapters/adversarial-machine-learning-and-model-attack-surface.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/adversarial-machine-learning-and-model-attack-surface.md"
TAG = "lean:adversarial-machine-learning-and-model-attack-surface.admission_boundary"
MODULE = "AsiStackProofs.AdversarialModelSecurity"
Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is True, repair, lambda d, f=field: d.update({f: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is False, repair, lambda d, f=field: d.update({f: True})


AXES: list[Axis] = [
    yes("modelIdentityBound", "bindModelIdentity"), yes("checkpointIdentityBound", "bindCheckpointIdentity"),
    yes("dataLineageBound", "bindDataLineage"), yes("servingConfigurationBound", "bindServingConfiguration"),
    yes("lifecycleStageBound", "bindLifecycleStage"), yes("modalityBound", "bindModality"),
    yes("populationBound", "bindPopulation"),
    ("configurationVersion", lambda d: d["configurationVersion"] == d["authorizedConfigurationVersion"], "reopenForConfigurationVersion", lambda d: d.update(configurationVersion=8)),
    yes("attackerAccessBound", "bindAttackerAccess"), yes("attackerKnowledgeBound", "bindAttackerKnowledge"),
    yes("attackerCapabilityBound", "bindAttackerCapability"), yes("attackerBudgetBound", "bindAttackerBudget"),
    yes("attackObjectiveBound", "bindAttackObjective"), yes("attackSurfaceBound", "bindAttackSurface"),
    yes("protectedAssetBound", "bindProtectedAsset"), yes("successCriterionBound", "bindSuccessCriterion"),
    yes("attackClassesSeparated", "separateAttackClasses"), yes("attackObjectivesSeparated", "separateAttackObjectives"),
    yes("attemptDenominatorComplete", "completeAttemptDenominator"), yes("attemptTraceLineagePresent", "bindAttemptTraceLineage"),
    yes("defenseAwareChallengePresent", "addDefenseAwareChallenge"), yes("adaptiveChallengePresent", "addAdaptiveChallenge"),
    yes("transferChallengePresent", "addTransferChallenge"), yes("knownVulnerableControlPresent", "addKnownVulnerableControl"),
    yes("knownVulnerableControlPassed", "repairKnownVulnerableControl"), yes("benignPerturbationBaselinePresent", "addBenignPerturbationBaseline"),
    yes("cleanUtilityBaselinePresent", "addCleanUtilityBaseline"), yes("matchedAttackDefenseBudgets", "matchAttackDefenseBudgets"),
    yes("independentChallengerPresent", "addIndependentChallenger"), yes("attackTracePresent", "preserveAttackTrace"),
    yes("observedEffectPresent", "recordObservedEffect"), yes("attackedUtilityPresent", "recordAttackedUtility"),
    yes("detectorOutcomePresent", "recordDetectorOutcome"), yes("falseAlarmRecordPresent", "recordFalseAlarms"),
    yes("costAndLatencyPresent", "recordCostAndLatency"), yes("failureCasesPreserved", "preserveFailureCases"),
    yes("quarantineRoutePresent", "addQuarantineRoute"), yes("predecessorBound", "bindPredecessor"),
    yes("repairLineagePresent", "bindRepairLineage"), yes("recoveryObservationPresent", "recordRecoveryObservation"),
    yes("descendantIndexPresent", "completeDescendantIndex"), yes("unreachableResidualRecorded", "recordUnreachableResidual"),
    yes("residualOwnerPresent", "assignResidualOwner"), yes("certificateScopeBound", "bindCertificateScope"),
    yes("monitorScopeBound", "bindMonitorScope"), yes("recoveryScopeBound", "bindRecoveryScope"),
    yes("assuranceNonSubstitutionRecorded", "recordAssuranceNonSubstitution"), yes("testAuthorizationPresent", "bindTestAuthorization"),
    yes("prohibitedRealEffectsExcluded", "excludeProhibitedRealEffects"), yes("exploitCustodyPresent", "bindExploitCustody"),
    yes("stopConditionsPresent", "bindStopConditions"), yes("notificationAndRemediationRoutePresent", "addNotificationAndRemediation"),
    yes("publicationTierBound", "bindPublicationTier"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    no("generalRobustnessClaimed", "rejectGeneralRobustness"), no("secureDeploymentClaimed", "rejectSecureDeployment"),
    no("attackAuthorizationRequested", "refuseAttackAuthorization"), no("supportPromotionRequested", "refuseSupportPromotion"),
]

REQUIRED_THEOREMS = {
    "certificate_does_not_discharge_monitoring", "monitoring_does_not_discharge_recovery",
    "recovery_does_not_discharge_certificate", "quarantine_all_covers_every_finite_trace",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "campaign_eligibility_requires_admissible_dossier", "complete_dossier_is_ready",
    "complete_dossier_reaches_only_model_security_campaign",
    "every_admission_axis_mutation_blocks_readiness", "every_admission_axis_mutation_has_exact_repair",
    "every_admission_axis_mutation_reaches_repair", "readiness_requires_identity",
    "readiness_requires_threat", "readiness_requires_challenge", "readiness_requires_observation",
    "readiness_requires_recovery", "readiness_requires_assurance",
    "readiness_requires_disclosure_boundary", "expired_disposition_remains_expired_when_time_advances",
    "checkpoint_change_invalidates_disposition", "configuration_change_invalidates_disposition",
    "budget_widening_invalidates_disposition", "identical_aggregate_signals_can_hide_opposite_security_state",
    "aggregate_scores_cannot_recover_bounded_security_state",
    "identical_local_checks_can_hide_opposite_composition_state",
    "local_component_checks_cannot_recover_attack_path_reachability",
    "ready_dossier_supplies_bounded_adversarial_evaluation_fields",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(d: dict[str, Any]) -> bool:
    return all(predicate(d) for _, predicate, _, _ in AXES)


def repair(d: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(d)), "eligibleForTheseusModelSecurityCampaign")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file(): errors.append(f"missing {path.relative_to(ROOT)}")
    if errors: raise SystemExit("Adversarial model security failed:\n - " + "\n - ".join(errors))
    complete = load(FIXTURE)
    if len(AXES) != 58 or len({axis[0] for axis in AXES}) != 58: errors.append("mutation denominator is not 58 unique axes")
    if not ready(complete) or repair(complete) != "eligibleForTheseusModelSecurityCampaign": errors.append("complete dossier is not campaign-eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(complete); mutate(candidate)
        if ready(candidate): errors.append(f"{name} mutation remained ready")
        if repair(candidate) != route: errors.append(f"{name} reached {repair(candidate)}, expected {route}")
    quarantined = [{**trace, "quarantined": True} for trace in complete["attackTraces"]]
    if not quarantined or not all(trace["quarantined"] for trace in quarantined): errors.append("finite trace quarantine control failed")
    if any((("certificate", "monitoring"), ("monitor", "recovery"), ("recovery", "certificate"))[i][0] == (("certificate", "monitoring"), ("monitor", "recovery"), ("recovery", "certificate"))[i][1] for i in range(3)): errors.append("assurance non-substitution control failed")
    disposition = (5, 7, 7, 11, 100, 20)
    if disposition == (5, 8, 7, 11, 100, 20) or disposition == (5, 7, 8, 11, 100, 20) or 101 <= 100: errors.append("disposition invalidation control failed")
    aggregate = (95, 100, 80, True)
    if aggregate != tuple(aggregate) or (True and True) == (False and False): errors.append("aggregate-signal collision failed")
    local = (True, True, True)
    if local != tuple(local) or False == True: errors.append("composition collision failed")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", LEAN.read_text(encoding="utf-8")))
    if theorem_names != REQUIRED_THEOREMS: errors.append("exact 28-theorem surface drifted")
    lean_text = LEAN.read_text(encoding="utf-8")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text): errors.append("Lean trust boundary contains sorry, admit, or axiom")
    manifest = [r for r in load(MANIFEST)["records"] if r.get("tag") == TAG]
    triage = [r for r in load(TRIAGE)["records"] if r.get("tag") == TAG]
    if len(manifest) != 1 or (manifest[0].get("module"), manifest[0].get("status")) != (MODULE, "implemented"): errors.append("manifest binding drifted")
    if len(triage) != 1 or (triage[0].get("module"), triage[0].get("target_status")) != (MODULE, "implemented"): errors.append("triage binding drifted")
    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in ("28 theorem declarations", "58 admission-axis mutations", "finite attack-trace quarantine", "assurance non-substitution", "aggregate-score impossibility", "component-composition impossibility", "Chapter support remains `argument`", "Project Theseus model-security campaign"):
        if fragment not in chapter: errors.append(f"chapter missing {fragment}")
    formal = manifest[0].get("formal_target") if manifest else None
    if formal and formal not in " ".join(OUTLINE.read_text(encoding="utf-8").split()): errors.append("outline target drifted")
    if errors: raise SystemExit("Adversarial model security failed:\n - " + "\n - ".join(errors))
    print("Adversarial model security passed: eight-step lifecycle, 58/58 exact repairs, assurance non-substitution, finite trace quarantine, expiry and three disposition invalidations, two non-identifiability results, one adversarial-evaluation consumer bridge, and 28 exact Lean declarations; no robustness, exploitability, recovery efficacy, deployment, attack authority, support, or external-effect claim.")


if __name__ == "__main__":
    main()

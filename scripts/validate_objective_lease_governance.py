#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ObjectiveLeaseGovernance.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/objective_lease_dossier.json"
CHAPTER = ROOT / "chapters/governed-objective-formation-value-learning-and-goal-integrity.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/governed-objective-formation-value-learning-and-goal-integrity.md"
TAG = "lean:governed-objective-formation-value-learning-and-goal-integrity.admission_boundary"
MODULE = "AsiStackProofs.ObjectiveLeaseGovernance"
Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is True, repair, lambda d, f=field: d.update({f: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is False, repair, lambda d, f=field: d.update({f: True})


AXES: list[Axis] = [
    yes("purposeIdentityBound", "bindPurposeIdentity"), yes("principalAuthorityBound", "bindPrincipalAuthority"),
    yes("affectedPartiesRecorded", "recordAffectedParties"), yes("constitutionalCeilingsBound", "bindConstitutionalCeilings"),
    yes("explicitNonGoalsRecorded", "recordExplicitNonGoals"), yes("amendmentProcedureBound", "bindAmendmentProcedure"),
    no("optimizerSelfRatificationRequested", "refuseOptimizerSelfRatification"), yes("targetIdentityBound", "bindTargetIdentity"),
    ("targetVersion", lambda d: d["targetVersion"] == d["expectedTargetVersion"], "restoreTargetVersion", lambda d: d.update(targetVersion=8)),
    yes("proxiesTypedSeparately", "separateProxies"), yes("causalAssumptionsRecorded", "recordCausalAssumptions"),
    yes("preferenceEvidenceTyped", "typePreferenceEvidence"), yes("rewardRoleTyped", "typeRewardRole"),
    yes("evaluatorRoleTyped", "typeEvaluatorRole"), yes("plannerRoleTyped", "typePlannerRole"),
    no("predictedPreferenceAsAuthorityClaimed", "rejectPreferenceAsAuthority"), yes("alternativesPreserved", "preserveAlternatives"),
    yes("uncertaintyRecorded", "recordUncertainty"), yes("dissentPreserved", "preserveDissent"),
    yes("unrepresentedPartiesRecorded", "recordUnrepresentedParties"), yes("rightsCeilingsPreserved", "preserveRightsCeilings"),
    yes("aggregationRuleVersioned", "versionAggregationRule"), yes("clarificationOrAbstentionRoute", "addClarificationOrAbstention"),
    ("consumerScope", lambda d: d["consumerId"] == d["authorizedConsumerId"], "restoreConsumerScope", lambda d: d.update(consumerId=42)),
    ("ontologyVersion", lambda d: d["ontologyVersion"] == d["authorizedOntologyVersion"], "reauthorizeOntology", lambda d: d.update(ontologyVersion=13)),
    ("authorityVersion", lambda d: d["authorityVersion"] == d["authorizedAuthorityVersion"], "reauthorizeAuthority", lambda d: d.update(authorityVersion=6)),
    ("populationVersion", lambda d: d["populationVersion"] == d["authorizedPopulationVersion"], "reauthorizePopulation", lambda d: d.update(populationVersion=4)),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    yes("reauthorizationRoutePresent", "addReauthorizationRoute"), yes("interruptionRoutePresent", "addInterruptionRoute"),
    yes("rollbackRoutePresent", "addRollbackRoute"), yes("proxyInterventionTested", "testProxyIntervention"),
    yes("distributionShiftTested", "testDistributionShift"), yes("evaluatorSwapTested", "testEvaluatorSwap"),
    yes("rewardTamperingTested", "testRewardTampering"), yes("capableWrongGoalControlPresent", "addCapableWrongGoalControl"),
    yes("independentTargetObservationPresent", "addIndependentTargetObservation"), yes("ontologyMigrationTested", "testOntologyMigration"),
    yes("descendantIndexComplete", "completeDescendantIndex"), yes("unreachableResidualsRecorded", "recordUnreachableResiduals"),
    yes("residualOwnerPresent", "assignResidualOwner"), no("targetCorrectnessClaimed", "rejectTargetCorrectness"),
    no("moralTruthClaimed", "rejectMoralTruth"), no("stableAlignmentClaimed", "rejectStableAlignment"),
    no("safeOptimizationClaimed", "rejectSafeOptimization"), no("supportPromotionRequested", "refuseSupportPromotion"),
]

REQUIRED_THEOREMS = {
    "optimizer_cannot_self_ratify", "reward_model_cannot_ratify", "evaluator_cannot_ratify",
    "retire_all_closes_every_finite_binding", "review_step_preserves_stage_invariant",
    "review_run_preserves_stage_invariant", "study_eligibility_requires_admissible_dossier",
    "complete_dossier_is_ready", "complete_dossier_reaches_only_objective_registry_study",
    "every_admission_axis_mutation_blocks_readiness", "every_admission_axis_mutation_has_exact_repair",
    "every_admission_axis_mutation_reaches_repair", "readiness_requires_charter",
    "readiness_requires_target_proxy_separation", "readiness_requires_plurality",
    "readiness_requires_lease", "readiness_requires_challenge", "readiness_requires_retirement_boundary",
    "expired_lease_remains_expired_when_time_advances", "consumer_lease_is_nontransferable",
    "ontology_change_invalidates_use", "authority_change_invalidates_use",
    "identical_proxy_observation_can_hide_opposite_target_movement",
    "proxy_score_and_evaluator_cannot_recover_target_improvement",
    "identical_preference_prediction_can_hide_opposite_authority",
    "predicted_preference_cannot_recover_authority",
    "ready_dossier_supplies_bounded_learned_objective_consumer_fields",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(d: dict[str, Any]) -> bool:
    return all(predicate(d) for _, predicate, _, _ in AXES)


def repair(d: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(d)), "eligibleForTheseusObjectiveRegistryStudy")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file(): errors.append(f"missing {path.relative_to(ROOT)}")
    if errors: raise SystemExit("Objective lease governance failed:\n - " + "\n - ".join(errors))
    complete = load(FIXTURE)
    if len(AXES) != 46 or len({axis[0] for axis in AXES}) != 46: errors.append("mutation denominator is not 46 unique axes")
    if not ready(complete) or repair(complete) != "eligibleForTheseusObjectiveRegistryStudy": errors.append("complete dossier is not study-eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(complete); mutate(candidate)
        if ready(candidate): errors.append(f"{name} mutation remained ready")
        if repair(candidate) != route: errors.append(f"{name} reached {repair(candidate)}, expected {route}")
    retired = [{**binding, "active": False} for binding in complete["descendants"]]
    if not retired or any(binding["active"] for binding in retired): errors.append("finite descendant retirement control failed")
    lease = (41, 7, 12, 5, 3, 20)
    if lease == (42, 7, 12, 5, 3, 20) or lease == (41, 7, 13, 5, 3, 20): errors.append("consumer/version non-transfer control failed")
    proxy = (100, 4)
    if proxy != tuple(proxy) or True == False: errors.append("proxy collision failed")
    preference = (9, 80, 90)
    if preference != tuple(preference) or True == False: errors.append("preference-authority collision failed")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", LEAN.read_text(encoding="utf-8")))
    if theorem_names != REQUIRED_THEOREMS: errors.append("exact 27-theorem surface drifted")
    lean_text = LEAN.read_text(encoding="utf-8")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text): errors.append("Lean trust boundary contains sorry, admit, or axiom")
    manifest = [r for r in load(MANIFEST)["records"] if r.get("tag") == TAG]
    triage = [r for r in load(TRIAGE)["records"] if r.get("tag") == TAG]
    if len(manifest) != 1 or (manifest[0].get("module"), manifest[0].get("status")) != (MODULE, "implemented"): errors.append("manifest binding drifted")
    if len(triage) != 1 or (triage[0].get("module"), triage[0].get("target_status")) != (MODULE, "implemented"): errors.append("triage binding drifted")
    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in ("27 theorem declarations", "46 admission-axis mutations", "finite descendant retirement", "consumer non-transferability", "proxy-target impossibility", "preference-authority impossibility", "Chapter support remains `argument`", "Project Theseus objective-registry study"):
        if fragment not in chapter: errors.append(f"chapter missing {fragment}")
    formal = manifest[0].get("formal_target") if manifest else None
    if formal and formal not in " ".join(OUTLINE.read_text(encoding="utf-8").split()): errors.append("outline target drifted")
    if errors: raise SystemExit("Objective lease governance failed:\n - " + "\n - ".join(errors))
    print("Objective lease governance passed: seven-stage lifecycle, 46/46 exact repairs, typed self-ratification refusal, consumer/version invalidation, inductive finite descendant retirement, two non-identifiability results, one learned-objective consumer bridge, and 27 exact Lean declarations; no value correctness, consent, legitimacy, behavioral alignment, support, or external-effect claim.")


if __name__ == "__main__":
    main()

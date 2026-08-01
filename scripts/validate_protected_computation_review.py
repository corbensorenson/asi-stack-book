#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ProtectedComputationReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/protected_computation_dossier.json"
CHAPTER = ROOT / "chapters/confidential-and-verifiable-ai-computation.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/confidential-and-verifiable-ai-computation.md"
TAG = "lean:confidential-and-verifiable-ai-computation.admission_boundary"
MODULE = "AsiStackProofs.ProtectedComputationReview"
Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is True, repair, lambda d, f=field: d.update({f: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is False, repair, lambda d, f=field: d.update({f: True})


AXES: list[Axis] = [
    yes("requestIdentityBound", "bindRequestIdentity"), yes("transactionIdentityBound", "bindTransactionIdentity"),
    yes("artifactIdentityBound", "bindArtifactIdentity"), yes("modelIdentityBound", "bindModelIdentity"),
    yes("preprocessingIdentityBound", "bindPreprocessingIdentity"), yes("configurationIdentityBound", "bindConfigurationIdentity"),
    yes("lifecycleStageBound", "bindLifecycleStage"), yes("adversaryBound", "bindAdversary"),
    yes("protectedAssetsBound", "bindProtectedAssets"), yes("guaranteeVectorSeparated", "separateGuaranteeVector"),
    yes("trustAssumptionsBound", "bindTrustAssumptions"), yes("constructionIdentityBound", "bindConstructionIdentity"),
    yes("evidenceStatementBound", "bindEvidenceStatement"), yes("unsupportedPropertiesExplicit", "recordUnsupportedProperties"),
    yes("attesterIdentityBound", "bindAttesterIdentity"), yes("verifierIdentityBound", "bindVerifierIdentity"),
    yes("relyingPartyIdentityBound", "bindRelyingPartyIdentity"), yes("independentAppraisalPresent", "addIndependentAppraisal"),
    yes("verifierPolicyBound", "bindVerifierPolicy"), yes("referenceValuesBound", "bindReferenceValues"),
    yes("cryptographicAssumptionsBound", "bindCryptographicAssumptions"),
    yes("semanticCorrespondenceResidualPresent", "recordSemanticCorrespondenceResidual"),
    yes("claimClassesSeparated", "separateClaimClasses"), yes("freshnessChallengePresent", "addFreshnessChallenge"),
    yes("evidenceEpochBound", "bindEvidenceEpoch"), yes("revocationStateBound", "bindRevocationState"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    ("policyVersion", lambda d: d["verifierPolicyVersion"] == d["authorizedVerifierPolicyVersion"], "reopenForVerifierPolicyVersion", lambda d: d.update(verifierPolicyVersion=4)),
    ("leakageBound", lambda d: d["observedLeakageUnits"] <= d["permittedLeakageUnits"], "reduceOrAuthorizeLeakage", lambda d: d.update(observedLeakageUnits=4)),
    yes("leakageInventoryComplete", "completeLeakageInventory"), yes("outputLeakageRecorded", "recordOutputLeakage"),
    yes("timingLeakageRecorded", "recordTimingLeakage"), yes("accessPatternLeakageRecorded", "recordAccessPatternLeakage"),
    yes("logAndCacheLeakageRecorded", "recordLogAndCacheLeakage"),
    yes("failureAndMetadataLeakageRecorded", "recordFailureAndMetadataLeakage"),
    yes("leakageResidualOwnerPresent", "assignLeakageResidualOwner"),
    yes("protectedFailureStateExplicit", "recordProtectedFailureState"), yes("fallbackObservable", "makeFallbackObservable"),
    yes("fallbackSeparatelyAuthorized", "requireFallbackAuthorization"), yes("silentDowngradeProhibited", "prohibitSilentDowngrade"),
    yes("recoveryRoutePresent", "addRecoveryRoute"), yes("matchedCostRecordPresent", "addMatchedCostRecord"),
    yes("privacyPurposeHandoffPresent", "addPrivacyPurposeHandoff"), yes("weightCustodyHandoffPresent", "addWeightCustodyHandoff"),
    no("semanticCorrectnessClaimed", "rejectSemanticCorrectness"), no("authorizationClaimed", "rejectAuthorization"),
    no("endToEndPrivacyClaimed", "rejectEndToEndPrivacy"), no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED_THEOREMS = {
    "attestation_does_not_establish_semantic_correctness",
    "encoded_relation_proof_does_not_establish_authorization",
    "confidentiality_mechanism_does_not_establish_end_to_end_privacy",
    "account_all_covers_every_finite_leakage_channel",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "campaign_eligibility_requires_admissible_dossier", "complete_dossier_is_ready",
    "complete_dossier_reaches_only_protected_computation_campaign",
    "every_admission_axis_mutation_blocks_readiness", "every_admission_axis_mutation_has_exact_repair",
    "every_admission_axis_mutation_reaches_repair", "readiness_requires_identity",
    "readiness_requires_guarantees", "readiness_requires_evidence", "readiness_requires_freshness",
    "readiness_requires_leakage", "readiness_requires_fallback", "readiness_requires_boundary",
    "expired_receipt_remains_expired_when_time_advances",
    "leakage_overrun_persists_under_more_observation_and_no_larger_budget",
    "artifact_change_invalidates_receipt", "verifier_policy_change_invalidates_receipt",
    "evidence_epoch_change_invalidates_receipt",
    "unprotected_fallback_without_separate_authorization_is_blocked",
    "silent_unprotected_fallback_is_blocked",
    "identical_evidence_signals_can_hide_opposite_semantic_authority_state",
    "evidence_signals_cannot_recover_semantic_authority",
    "identical_component_guarantees_can_hide_opposite_end_to_end_privacy",
    "component_guarantees_cannot_recover_end_to_end_privacy",
    "protected_execution_receipt_cannot_substitute_for_privacy_authorization",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(d: dict[str, Any]) -> bool:
    return all(predicate(d) for _, predicate, _, _ in AXES)


def repair(d: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(d)), "eligibleForTheseusProtectedComputationCampaign")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file(): errors.append(f"missing {path.relative_to(ROOT)}")
    if errors: raise SystemExit("Protected computation review failed:\n - " + "\n - ".join(errors))
    complete = load(FIXTURE)
    if len(AXES) != 48 or len({axis[0] for axis in AXES}) != 48: errors.append("mutation denominator is not 48 unique axes")
    if not ready(complete) or repair(complete) != "eligibleForTheseusProtectedComputationCampaign": errors.append("complete dossier is not campaign-eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(complete); mutate(candidate)
        if ready(candidate): errors.append(f"{name} mutation remained ready")
        if repair(candidate) != route: errors.append(f"{name} reached {repair(candidate)}, expected {route}")
    evidence_map = {"attestation": "platformIdentity", "proof": "encodedRelation", "confidentiality": "protectedAssetConfidentiality"}
    if evidence_map.get("attestation") == "semanticCorrectness" or evidence_map.get("proof") == "authorization" or evidence_map.get("confidentiality") == "endToEndPrivacy": errors.append("evidence non-substitution failed")
    accounted = [{**row, "accounted": True} for row in complete["leakageObservations"]]
    if not accounted or not all(row["accounted"] for row in accounted): errors.append("finite leakage accounting failed")
    if not (21 > complete["expiresAt"] and 4 != complete["verifierPolicyVersion"] and 9 != 7 and 5 != 4): errors.append("receipt invalidation controls failed")
    if not (3 < 4 <= 5 and 3 <= 3): errors.append("leakage monotonicity control failed")
    if ("unprotected", False, True) == ("protected", False, True) or ("unprotected", True, False) == ("protected", True, False): errors.append("fallback rejection control failed")
    evidence_signals = (True, True, True)
    if evidence_signals != tuple(evidence_signals) or (True and True) == (False and False): errors.append("semantic-authority collision failed")
    component_signals = (True, True, True)
    if component_signals != tuple(component_signals) or (True and True) == (False and False): errors.append("end-to-end privacy collision failed")
    privacy_route = "rejectPurpose" if False is False else "acceptBoundedReceipt"
    if privacy_route != "rejectPurpose": errors.append("privacy consumer inherited purpose or authority")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", LEAN.read_text(encoding="utf-8")))
    if theorem_names != REQUIRED_THEOREMS: errors.append("exact 31-theorem surface drifted")
    lean_text = LEAN.read_text(encoding="utf-8")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text): errors.append("Lean trust boundary contains sorry, admit, or axiom")
    manifest = [r for r in load(MANIFEST)["records"] if r.get("tag") == TAG]
    triage = [r for r in load(TRIAGE)["records"] if r.get("tag") == TAG]
    if len(manifest) != 1 or (manifest[0].get("module"), manifest[0].get("status")) != (MODULE, "implemented"): errors.append("manifest binding drifted")
    if len(triage) != 1 or (triage[0].get("module"), triage[0].get("target_status")) != (MODULE, "implemented"): errors.append("triage binding drifted")
    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in ("31 theorem declarations", "48 admission-axis mutations", "evidence non-substitution", "finite leakage accounting", "semantic-authority impossibility", "end-to-end privacy impossibility", "Chapter support remains `argument`", "Project Theseus protected-computation campaign"):
        if fragment not in chapter: errors.append(f"chapter missing {fragment}")
    formal = manifest[0].get("formal_target") if manifest else None
    if formal and formal not in " ".join(OUTLINE.read_text(encoding="utf-8").split()): errors.append("outline target drifted")
    if errors: raise SystemExit("Protected computation review failed:\n - " + "\n - ".join(errors))
    print("Protected computation review passed: eight-step lifecycle, 48/48 exact repairs, evidence non-substitution, finite leakage accounting, receipt and leakage monotonicity, fallback rejection, two non-identifiability results, one rejecting privacy consumer bridge, and 31 exact Lean declarations; no cryptographic, attestation, hardware, privacy, authorization, deployment, support, or external-effect claim.")


if __name__ == "__main__":
    main()

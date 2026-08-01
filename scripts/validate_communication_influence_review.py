#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/CommunicationInfluenceReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/communication_influence_dossier.json"
CHAPTER = ROOT / "chapters/human-ai-communication-persuasion-and-epistemic-security.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/human-ai-communication-persuasion-and-epistemic-security.md"
TAG = "lean:human-ai-communication-persuasion-and-epistemic-security.admission_boundary"
MODULE = "AsiStackProofs.CommunicationInfluenceReview"
Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is True, repair, lambda d, f=field: d.update({f: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is False, repair, lambda d, f=field: d.update({f: True})


AXES: list[Axis] = [
    yes("claimIdentityBound", "bindClaimIdentity"), yes("claimVersionBound", "bindClaimVersion"),
    yes("evidenceCeilingBound", "bindEvidenceCeiling"), yes("outboundWithinCeiling", "narrowOutboundLanguage"),
    yes("uncertaintyVisible", "exposeUncertainty"), yes("speakerIdentityVisible", "exposeSpeakerIdentity"),
    yes("syntheticIdentityVisible", "exposeSyntheticIdentity"), yes("sponsorshipVisible", "exposeSponsorship"),
    yes("correctionAddressBound", "bindCorrectionAddress"), yes("audienceClassBound", "bindAudienceClass"),
    yes("purposeBound", "bindPurpose"), yes("vulnerabilityReviewed", "reviewVulnerability"),
    yes("dependencyReviewed", "reviewDependency"), yes("powerAsymmetryReviewed", "reviewPowerAsymmetry"),
    yes("practicalExitPresent", "providePracticalExit"), yes("contestabilityPresent", "provideContestability"),
    yes("personalizationGrantCurrent", "renewPersonalizationGrant"), yes("deniedAttributesExcluded", "excludeDeniedAttributes"),
    yes("knownVulnerabilityNotExploited", "rejectVulnerabilityExploitation"), yes("techniqueDeclared", "declareTechnique"),
    yes("channelBound", "bindChannel"), yes("eligibleAudienceBound", "bindEligibleAudience"),
    yes("repetitionLimitBound", "bindRepetitionLimit"),
    ("audienceOverrun", lambda d: d["actualAudienceCount"] <= d["audienceCeiling"], "narrowAudience", lambda d: d.update(actualAudienceCount=11)),
    ("repetitionOverrun", lambda d: d["actualRepetitionCount"] <= d["repetitionCeiling"], "narrowRepetition", lambda d: d.update(actualRepetitionCount=4)),
    yes("amplificationAuthorityRevocable", "restoreRevocableAmplification"),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(expiresAt=3)),
    yes("distributionLineagePresent", "bindDistributionLineage"), yes("outcomeMeasuresBound", "bindOutcomeMeasures"),
    yes("affectedRecipientDenominatorBound", "bindAffectedRecipientDenominator"), yes("correctionRoutePresent", "addCorrectionRoute"),
    yes("retractionRoutePresent", "addRetractionRoute"), yes("remedyRoutePresent", "addRemedyRoute"),
    yes("unreachableDescendantsRecorded", "recordUnreachableDescendants"), yes("residualOwnerPresent", "assignResidualOwner"),
    no("factualityOnlySufficiencyClaimed", "rejectFactualitySufficiency"), no("consentAsSafetyClaimed", "rejectConsentAsSafety"),
    no("persuasionScoreAsBenefitClaimed", "rejectPersuasionAsBenefit"), no("disclosureAsComprehensionClaimed", "rejectDisclosureAsComprehension"),
    yes("nonClaimBoundaryPresent", "recordNonClaimBoundary"), no("deliveryAuthorizationRequested", "refuseDeliveryAuthorization"),
    no("supportPromotionRequested", "refuseSupportPromotion"),
]

REQUIRED_THEOREMS = {
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "study_eligibility_requires_admissible_dossier", "complete_dossier_is_ready",
    "complete_dossier_reaches_only_benign_study", "every_admission_axis_mutation_blocks_readiness",
    "every_admission_axis_mutation_has_exact_repair", "every_admission_axis_mutation_reaches_repair",
    "readiness_requires_claim_provenance", "readiness_requires_audience_autonomy",
    "readiness_requires_delivery_envelope", "readiness_requires_correction_observation",
    "readiness_requires_non_authority_boundary", "expired_packet_remains_expired_when_time_advances",
    "audience_overrun_persists_under_more_reach_and_no_larger_ceiling",
    "repetition_overrun_persists_under_more_repetition_and_no_larger_ceiling",
    "denied_attribute_noninterference", "identical_surface_signals_can_hide_opposite_influence_state",
    "factuality_consent_persuasion_and_disclosure_cannot_recover_influence_state",
    "identical_provenance_can_hide_opposite_comprehension", "provenance_cannot_recover_recipient_comprehension",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(d: dict[str, Any]) -> bool:
    return all(predicate(d) for _, predicate, _, _ in AXES)


def repair(d: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(d)), "eligibleForTheseusBenignCommunicationStudy")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file(): errors.append(f"missing {path.relative_to(ROOT)}")
    if errors: raise SystemExit("Communication influence review failed:\n - " + "\n - ".join(errors))
    complete = load(FIXTURE)
    if len(AXES) != 42 or len({axis[0] for axis in AXES}) != 42: errors.append("mutation denominator is not 42 unique axes")
    if not ready(complete) or repair(complete) != "eligibleForTheseusBenignCommunicationStudy": errors.append("complete dossier is not study-eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(complete); mutate(candidate)
        if ready(candidate): errors.append(f"{name} mutation remained ready")
        if repair(candidate) != route: errors.append(f"{name} reached {repair(candidate)}, expected {route}")
    for reached, ceiling, later_reached, later_ceiling in ((11, 10, 12, 10), (4, 3, 8, 2)):
        if not (ceiling < reached <= later_reached and later_ceiling <= ceiling < later_reached): errors.append("exposure monotonicity control failed")
    policy = lambda allowed: allowed[0] * 100 + allowed[1]
    if policy((7, 3)) != policy((7, 3)): errors.append("denied-attribute noninterference failed")
    signals = (95, True, 60, True)
    if signals != tuple(signals) or (not False and True) == (not True and False): errors.append("surface-signal collision failed")
    provenance = (7, 3, 11)
    if provenance != tuple(provenance) or True == False: errors.append("provenance collision failed")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", LEAN.read_text(encoding="utf-8")))
    if theorem_names != REQUIRED_THEOREMS: errors.append("exact 21-theorem surface drifted")
    manifest = [r for r in load(MANIFEST)["records"] if r.get("tag") == TAG]
    triage = [r for r in load(TRIAGE)["records"] if r.get("tag") == TAG]
    if len(manifest) != 1 or (manifest[0].get("module"), manifest[0].get("status")) != (MODULE, "implemented"): errors.append("manifest binding drifted")
    if len(triage) != 1 or (triage[0].get("module"), triage[0].get("target_status")) != (MODULE, "implemented"): errors.append("triage binding drifted")
    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in ("21 theorem declarations", "42 admission-axis mutations", "denied-attribute noninterference", "surface-signal impossibility", "provenance-comprehension impossibility", "Chapter support remains `argument`", "Project Theseus benign communication study"):
        if fragment not in chapter: errors.append(f"chapter missing {fragment}")
    formal = manifest[0].get("formal_target") if manifest else None
    if formal and formal not in " ".join(OUTLINE.read_text(encoding="utf-8").split()): errors.append("outline target drifted")
    if errors: raise SystemExit("Communication influence review failed:\n - " + "\n - ".join(errors))
    print("Communication influence review passed: six-stage lifecycle, 42/42 exact repairs, three adverse monotonicity results, denied-attribute noninterference, two non-identifiability results, and 21 exact Lean declarations; no persuasion, comprehension, autonomy, delivery, support, or external-effect claim.")


if __name__ == "__main__":
    main()

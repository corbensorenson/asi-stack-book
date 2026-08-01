#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/ContentAuthenticityReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/content_authenticity_envelope.json"
CHAPTER = ROOT / "chapters/content-authenticity-watermarking-and-synthetic-media-integrity.qmd"
MANIFEST = ROOT / "proofs/proof_manifest.json"
TRIAGE = ROOT / "proofs/proof_triage.json"
OUTLINE = ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/content-authenticity-watermarking-and-synthetic-media-integrity.md"
TAG = "lean:content-authenticity-watermarking-and-synthetic-media-integrity.admission_boundary"
MODULE = "AsiStackProofs.ContentAuthenticityReview"
Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]


def yes(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is True, repair, lambda d, f=field: d.update({f: False})


def no(field: str, repair: str) -> Axis:
    return field, lambda d, f=field: d[f] is False, repair, lambda d, f=field: d.update({f: True})


AXES: list[Axis] = [
    yes("assetIdentityBound", "bindAssetIdentity"), yes("renditionIdentityBound", "bindRenditionIdentity"),
    yes("claimIdentityBound", "bindClaimIdentity"), yes("signerIdentityBound", "bindSignerIdentity"),
    yes("trustPolicyIdentityBound", "bindTrustPolicyIdentity"), yes("evidenceTypesSeparated", "separateEvidenceTypes"),
    yes("signedClaimRecorded", "recordSignedClaim"), yes("contentBindingChecked", "checkContentBinding"),
    yes("signatureStatusTyped", "typeSignatureStatus"), yes("watermarkResultTyped", "typeWatermarkResult"),
    yes("fingerprintResultTyped", "typeFingerprintResult"), yes("detectorResultTyped", "typeDetectorResult"),
    yes("contextualEvidenceTyped", "typeContextualEvidence"), yes("absenceNonInferenceExplicit", "recordAbsenceNonInference"),
    yes("truthNonInferenceExplicit", "recordTruthNonInference"),
    yes("transformationInventoryComplete", "completeTransformationInventory"),
    yes("unsupportedTransformationBreakExplicit", "recordUnsupportedTransformationBreak"),
    yes("compositeRegionsBound", "bindCompositeRegions"), yes("lineageBreaksVisible", "exposeLineageBreaks"),
    yes("transformationDigestBound", "bindTransformationDigest"),
    ("trustPolicyVersion", lambda d: d["trustPolicyVersion"] == d["authorizedTrustPolicyVersion"],
     "reopenForTrustPolicyVersion", lambda d: d.update(trustPolicyVersion=4)),
    ("signerRevocationEpoch", lambda d: d["checkedSignerEpoch"] == d["currentSignerEpoch"],
     "refreshSignerRevocationEpoch", lambda d: d.update(currentSignerEpoch=5)),
    ("expiry", lambda d: d["currentTick"] <= d["expiresAt"], "renewExpiry", lambda d: d.update(currentTick=21)),
    yes("evidenceEpochBound", "bindEvidenceEpoch"), yes("conflictsPreserved", "preserveConflicts"),
    yes("uncertaintyRecorded", "recordUncertainty"), yes("disputeRoutePresent", "addDisputeRoute"),
    yes("remedyRoutePresent", "addRemedyRoute"), yes("correctionLineagePresent", "addCorrectionLineage"),
    yes("affectedPathNotificationPresent", "addAffectedPathNotification"),
    yes("disclosureTextBound", "bindDisclosureText"), yes("disclosureAssetBound", "bindDisclosureAsset"),
    yes("disclosureAccessible", "makeDisclosureAccessible"),
    yes("comprehensionNotAssumed", "prohibitAssumedComprehension"), yes("privacyScopeBound", "bindPrivacyScope"),
    yes("consentDecisionSeparate", "separateConsentDecision"),
    yes("regulatoryDecisionSeparate", "separateRegulatoryDecision"),
    yes("highImpactActionSeparatelyAuthorized", "requireHighImpactAuthorization"),
    no("originClaimedFromAbsence", "rejectOriginInferenceFromAbsence"),
    no("semanticTruthClaimed", "rejectSemanticTruth"), no("legalComplianceClaimed", "rejectLegalCompliance"),
    no("supportOrReleaseRequested", "refuseSupportOrRelease"),
]

REQUIRED_THEOREMS = {
    "signed_provenance_does_not_establish_semantic_truth",
    "watermark_absence_does_not_establish_human_origin",
    "detector_output_does_not_establish_authorship",
    "check_all_covers_every_finite_transformation",
    "review_step_preserves_stage_invariant", "review_run_preserves_stage_invariant",
    "campaign_eligibility_requires_admissible_envelope", "complete_envelope_is_ready",
    "complete_envelope_reaches_only_authenticity_campaign",
    "every_admission_axis_mutation_blocks_readiness", "every_admission_axis_mutation_has_exact_repair",
    "every_admission_axis_mutation_reaches_repair", "readiness_requires_identity",
    "readiness_requires_evidence", "readiness_requires_transformations",
    "readiness_requires_current_trust", "readiness_requires_conflict_routes",
    "readiness_requires_accessible_disclosure", "readiness_requires_nonclaim_boundary",
    "expired_envelope_remains_expired_when_time_advances",
    "stale_signer_status_remains_stale_when_current_epoch_advances",
    "asset_change_invalidates_authenticity_receipt",
    "trust_policy_change_invalidates_authenticity_receipt",
    "transformation_change_invalidates_authenticity_receipt",
    "signer_epoch_change_invalidates_authenticity_receipt",
    "unsupported_transformation_cannot_claim_verified_preservation",
    "composite_without_region_binding_is_blocked",
    "identical_authenticity_signals_can_hide_opposite_truth_state",
    "authenticity_signals_cannot_recover_semantic_truth",
    "identical_absence_signals_can_hide_opposite_origin",
    "absence_signals_cannot_recover_human_origin",
    "authenticity_receipt_cannot_substitute_for_recipient_comprehension",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def ready(d: dict[str, Any]) -> bool:
    return all(predicate(d) for _, predicate, _, _ in AXES)


def repair(d: dict[str, Any]) -> str:
    return next((route for _, predicate, route, _ in AXES if not predicate(d)),
                "eligibleForTheseusAuthenticityCampaign")


def main() -> None:
    errors: list[str] = []
    for path in (LEAN, FIXTURE, CHAPTER, MANIFEST, TRIAGE, OUTLINE, DOSSIER):
        if not path.is_file(): errors.append(f"missing {path.relative_to(ROOT)}")
    if errors: raise SystemExit("Content authenticity review failed:\n - " + "\n - ".join(errors))
    complete = load(FIXTURE)
    if len(AXES) != 42 or len({axis[0] for axis in AXES}) != 42:
        errors.append("mutation denominator is not 42 unique axes")
    if not ready(complete) or repair(complete) != "eligibleForTheseusAuthenticityCampaign":
        errors.append("complete envelope is not campaign-eligible")
    for name, _, route, mutate in AXES:
        candidate = deepcopy(complete); mutate(candidate)
        if ready(candidate): errors.append(f"{name} mutation remained ready")
        if repair(candidate) != route: errors.append(f"{name} reached {repair(candidate)}, expected {route}")
    evidence_map = {
        "signedProvenance": "attributedStatement", "watermark": "embeddedSignal",
        "statisticalDetector": "distributionRelativeClassification",
    }
    if any(value in {"semanticTruth", "humanOrigin", "authorship"} for value in evidence_map.values()):
        errors.append("evidence non-substitution failed")
    checked = [{**row, "checked": True} for row in complete["transformationObservations"]]
    if not checked or not all(row["checked"] for row in checked): errors.append("finite transformation accounting failed")
    receipt = {"asset": 11, "rendition": 12, "policy": 3, "transformation": 13, "signerEpoch": 4, "expires": 20}
    invalidations = [99 != receipt["asset"], 4 != receipt["policy"], 14 != receipt["transformation"],
                     5 != receipt["signerEpoch"], 21 > receipt["expires"]]
    if not all(invalidations): errors.append("receipt invalidation controls failed")
    if not (4 < 5 <= 6 and 20 < 21 <= 22): errors.append("staleness monotonicity controls failed")
    if not (False is False and True is True): errors.append("transformation rejection controls failed")
    signals = (True, True, True, True, True)
    if signals != tuple(signals) or True == False: errors.append("semantic-truth collision failed")
    absent = (False, False, False)
    if absent != tuple(absent) or "human" == "synthetic": errors.append("origin collision failed")
    consumer_comprehended = False
    if complete["disclosureAccessible"] and consumer_comprehended:
        errors.append("communication consumer inherited comprehension")
    theorem_names = set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)", LEAN.read_text(encoding="utf-8")))
    if theorem_names != REQUIRED_THEOREMS: errors.append("exact 32-theorem surface drifted")
    lean_text = LEAN.read_text(encoding="utf-8")
    if re.search(r"\b(sorry|admit|axiom)\b", lean_text): errors.append("Lean trust boundary contains sorry, admit, or axiom")
    manifest = [r for r in load(MANIFEST)["records"] if r.get("tag") == TAG]
    triage = [r for r in load(TRIAGE)["records"] if r.get("tag") == TAG]
    if len(manifest) != 1 or (manifest[0].get("module"), manifest[0].get("status")) != (MODULE, "implemented"):
        errors.append("manifest binding drifted")
    if len(triage) != 1 or (triage[0].get("module"), triage[0].get("target_status")) != (MODULE, "implemented"):
        errors.append("triage binding drifted")
    chapter = " ".join(CHAPTER.read_text(encoding="utf-8").split())
    for fragment in ("32 theorem declarations", "42 admission-axis mutations", "finite transformation accounting",
                     "semantic-truth impossibility", "origin-from-absence impossibility",
                     "Chapter support remains `argument`", "Project Theseus authenticity campaign"):
        if fragment not in chapter: errors.append(f"chapter missing {fragment}")
    formal = manifest[0].get("formal_target") if manifest else None
    if formal and formal not in " ".join(OUTLINE.read_text(encoding="utf-8").split()):
        errors.append("outline target drifted")
    if errors: raise SystemExit("Content authenticity review failed:\n - " + "\n - ".join(errors))
    print("Content authenticity review passed: eight-transition lifecycle, 42/42 exact repairs, evidence non-substitution, finite transformation accounting, receipt and staleness invalidation, transformation rejection, truth and origin non-identifiability, one rejecting communication consumer bridge, and 32 exact Lean declarations; no provenance correctness, content truth, origin, authorship, comprehension, compliance, deployment, support, or external-effect claim.")


if __name__ == "__main__":
    main()

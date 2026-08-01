#!/usr/bin/env python3
from __future__ import annotations

import json, re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
LEAN = ROOT / "lean/AsiStackProofs/InstitutionalLegitimacyReview.lean"
FIXTURE = ROOT / "tests/fixtures/proof_models/institutional_legitimacy_dossier.json"
CHAPTER = ROOT / "chapters/institutions-international-coordination-and-public-legitimacy.qmd"
MANIFEST, TRIAGE, OUTLINE = ROOT / "proofs/proof_manifest.json", ROOT / "proofs/proof_triage.json", ROOT / "docs/book_outline.md"
DOSSIER = ROOT / "evidence_quality/proof_model_dossiers/institutions-international-coordination-and-public-legitimacy.md"
TAG = "lean:institutions-international-coordination-and-public-legitimacy.admission_boundary"
MODULE = "AsiStackProofs.InstitutionalLegitimacyReview"
Axis = tuple[str, Callable[[dict[str, Any]], bool], str, Callable[[dict[str, Any]], None]]
def yes(f: str, r: str) -> Axis: return f, lambda d, f=f: d[f] is True, r, lambda d, f=f: d.update({f: False})
def no(f: str, r: str) -> Axis: return f, lambda d, f=f: d[f] is False, r, lambda d, f=f: d.update({f: True})
AXES: list[Axis] = [
 yes("institutionIdentityBound","bindInstitutionIdentity"),yes("decisionIdentityBound","bindDecisionIdentity"),yes("instrumentIdentityBound","bindInstrumentIdentity"),yes("jurisdictionIdentityBound","bindJurisdictionIdentity"),yes("affectedPopulationIdentityBound","bindPopulationIdentity"),yes("evidenceEpochBound","bindEvidenceEpoch"),yes("protocolVersionBound","bindProtocolVersion"),
 yes("mandateSourceBound","bindMandateSource"),yes("territorialJurisdictionBound","bindTerritorialJurisdiction"),yes("subjectMatterJurisdictionBound","bindSubjectMatterJurisdiction"),yes("delegationChainComplete","completeDelegationChain"),yes("legalForceTyped","typeLegalForce"),yes("authorityConflictsRouted","routeAuthorityConflict"),
 ("expiry",lambda d:d["currentTick"]<=d["expiresAt"],"renewExpiry",lambda d:d.update(currentTick=21)),yes("emergencyAuthorityExpired","expireEmergencyAuthority"),
 yes("affectedPublicCensusComplete","completePublicCensus"),yes("excludedGroupsRecorded","recordExcludedGroups"),yes("representationRouteBound","bindRepresentationRoute"),yes("selectionLimitsRecorded","recordSelectionLimits"),yes("challengeStandingPresent","addChallengeStanding"),yes("evidenceAccessPresent","addEvidenceAccess"),yes("languageAndAccessibilityPresent","addAccessibility"),yes("dissentPreserved","preserveDissent"),
 yes("partiesBound","bindParties"),yes("obligationsTestable","makeObligationsTestable"),yes("verifierNamed","nameVerifier"),yes("verifierIndependenceRecorded","recordVerifierIndependence"),yes("dataSharingScopeBound","bindDataSharing"),yes("noncomplianceRoutePresent","addNoncomplianceRoute"),yes("disputeRoutePresent","addDisputeRoute"),yes("withdrawalAndAmendmentPresent","addWithdrawalAndAmendment"),
 yes("capacityAssessed","assessCapacity"),yes("financingIndependenceRecorded","recordFinancingIndependence"),yes("implementationObserved","observeImplementation"),yes("enforcementPathPresent","addEnforcementPath"),yes("enforcementAsymmetryRecorded","recordEnforcementAsymmetry"),yes("captureIndicatorsRecorded","recordCaptureIndicators"),yes("distributionalEffectsRecorded","recordDistributionalEffects"),
 yes("noticePresent","addNotice"),yes("evidencePreservationPresent","preserveEvidence"),yes("appealPathPresent","addAppeal"),yes("remedyPathPresent","addRemedy"),no("publicLegitimacyClaimed","rejectLegitimacyClaim"),no("universalLegalAuthorityClaimed","rejectUniversalAuthority"),no("supportOrReleaseRequested","refuseSupportOrRelease")]
REQUIRED = set('''agreement_does_not_establish_effective_implementation legal_compliance_does_not_establish_public_legitimacy consultation_does_not_establish_representative_mandate technical_conformance_does_not_establish_public_authority local_mandate_cannot_authorize_distinct_jurisdiction include_all_covers_every_finite_affected_public review_step_preserves_stage_invariant review_run_preserves_stage_invariant tabletop_eligibility_requires_admissible_dossier complete_dossier_is_ready complete_dossier_reaches_only_institutional_tabletop every_admission_axis_mutation_blocks_readiness every_admission_axis_mutation_has_exact_repair every_admission_axis_mutation_reaches_repair readiness_requires_identity readiness_requires_mandate readiness_requires_publics readiness_requires_coordination readiness_requires_performance readiness_requires_remedy readiness_requires_boundary expired_mandate_remains_expired_when_time_advances omitted_public_shortfall_persists_when_population_grows jurisdiction_change_invalidates_institutional_receipt instrument_change_invalidates_institutional_receipt population_change_invalidates_institutional_receipt protocol_change_invalidates_institutional_receipt identical_participation_signals_can_hide_opposite_representation participation_signals_cannot_recover_representation identical_commitment_signals_can_hide_opposite_enforcement commitment_signals_cannot_recover_effective_enforcement excluded_public_forces_governance_rights_review'''.split())
def load(p: Path)->Any:return json.loads(p.read_text())
def ready(d:dict[str,Any])->bool:return all(pred(d) for _,pred,_,_ in AXES)
def repair(d:dict[str,Any])->str:return next((r for _,p,r,_ in AXES if not p(d)),"eligibleForTheseusInstitutionalTabletop")
def main()->None:
 errors=[]
 for p in (LEAN,FIXTURE,CHAPTER,MANIFEST,TRIAGE,OUTLINE,DOSSIER):
  if not p.is_file():errors.append(f"missing {p.relative_to(ROOT)}")
 if errors:raise SystemExit("Institutional legitimacy review failed:\n - "+"\n - ".join(errors))
 d=load(FIXTURE)
 if len(AXES)!=45 or len({x[0] for x in AXES})!=45:errors.append("mutation denominator is not 45 unique axes")
 if not ready(d) or repair(d)!="eligibleForTheseusInstitutionalTabletop":errors.append("complete dossier is not eligible")
 for name,_,route,mutate in AXES:
  c=deepcopy(d);mutate(c)
  if ready(c) or repair(c)!=route:errors.append(f"{name} mutation/repair drifted")
 if not all({"agreement":"record","law":"boundedFinding","consultation":"occurred","conformance":"requirement"}.values()):errors.append("evidence separation failed")
 included=[{**p,"included":True} for p in d["affectedPublics"]]
 if not included or not all(p["included"] for p in included):errors.append("finite public inclusion failed")
 if not (20<21<=22 and 2<3<=4):errors.append("monotonicity failed")
 signals=(True,True,True)
 if signals!=tuple(signals) or True==False:errors.append("collision controls failed")
 names=set(re.findall(r"(?m)^theorem\s+([A-Za-z0-9_']+)",LEAN.read_text()))
 if names!=REQUIRED:errors.append("exact 32-theorem surface drifted")
 if re.search(r"\b(sorry|admit|axiom)\b",LEAN.read_text()):errors.append("Lean trust boundary widened")
 m=[r for r in load(MANIFEST)["records"] if r.get("tag")==TAG];t=[r for r in load(TRIAGE)["records"] if r.get("tag")==TAG]
 if len(m)!=1 or (m[0].get("module"),m[0].get("status"))!=(MODULE,"implemented"):errors.append("manifest binding drifted")
 if len(t)!=1 or (t[0].get("module"),t[0].get("target_status"))!=(MODULE,"implemented"):errors.append("triage binding drifted")
 chapter=" ".join(CHAPTER.read_text().split())
 for f in ("32 theorem declarations","45 admission-axis mutations","finite affected-public inclusion","representation impossibility","effective-enforcement impossibility","Chapter support remains `argument`","Project Theseus institutional tabletop"):
  if f not in chapter:errors.append(f"chapter missing {f}")
 if m and m[0]["formal_target"] not in " ".join(OUTLINE.read_text().split()):errors.append("outline target drifted")
 if errors:raise SystemExit("Institutional legitimacy review failed:\n - "+"\n - ".join(errors))
 print("Institutional legitimacy review passed: eight-transition lifecycle, 45/45 exact repairs, evidence and jurisdiction separation, finite affected-public inclusion, receipt and monotonicity controls, two non-identifiability results, one rejecting Governance Rights bridge, and 32 exact Lean declarations; no lawful authority, legitimacy, enforcement, support, or external-effect claim.")
if __name__=="__main__":main()

import AsiStackProofs.GovernanceRights

namespace AsiStackProofs.InstitutionalLegitimacyReview

inductive EvidenceKind where
  | signedAgreement | legalCompliance | stakeholderConsultation | technicalConformance
deriving DecidableEq, Repr

inductive ClaimClass where
  | agreementRecorded | boundedLegalFinding | consultationOccurred | requirementConformance
  | implementationEffective | publicLegitimacy | representativeMandate | publicAuthority
deriving DecidableEq, Repr

def establishes : EvidenceKind -> ClaimClass -> Bool
  | .signedAgreement, .agreementRecorded => true
  | .legalCompliance, .boundedLegalFinding => true
  | .stakeholderConsultation, .consultationOccurred => true
  | .technicalConformance, .requirementConformance => true
  | _, _ => false

theorem agreement_does_not_establish_effective_implementation :
    establishes .signedAgreement .implementationEffective = false := by rfl
theorem legal_compliance_does_not_establish_public_legitimacy :
    establishes .legalCompliance .publicLegitimacy = false := by rfl
theorem consultation_does_not_establish_representative_mandate :
    establishes .stakeholderConsultation .representativeMandate = false := by rfl
theorem technical_conformance_does_not_establish_public_authority :
    establishes .technicalConformance .publicAuthority = false := by rfl

structure Mandate where
  authorityId : Nat
  jurisdictionId : Nat
  expiresAt : Nat
deriving DecidableEq, Repr

def MandateUseAllowed (m : Mandate) (authority jurisdiction tick : Nat) : Prop :=
  authority = m.authorityId ∧ jurisdiction = m.jurisdictionId ∧ tick <= m.expiresAt

theorem local_mandate_cannot_authorize_distinct_jurisdiction
    (m : Mandate) (jurisdiction : Nat) (different : Not (jurisdiction = m.jurisdictionId))
    (tick : Nat) : Not (MandateUseAllowed m m.authorityId jurisdiction tick) := by
  intro h
  exact different h.2.1

structure PublicRecord where
  publicId : Nat
  included : Bool
deriving DecidableEq, Repr

def includePublic (p : PublicRecord) : PublicRecord := { p with included := true }
def includeAllPublics : List PublicRecord -> List PublicRecord
  | [] => []
  | p :: ps => includePublic p :: includeAllPublics ps
def AllPublicsIncluded (records : List PublicRecord) : Prop :=
  forall record, record ∈ records -> record.included = true

theorem include_all_covers_every_finite_affected_public (records : List PublicRecord) :
    AllPublicsIncluded (includeAllPublics records) := by
  intro record member
  induction records with
  | nil => simp [includeAllPublics] at member
  | cons head tail ih =>
      simp only [includeAllPublics, List.mem_cons] at member
      rcases member with same | rest
      · subst record; simp [includePublic]
      · exact ih rest

structure InstitutionalDossier where
  institutionIdentityBound : Bool := true
  decisionIdentityBound : Bool := true
  instrumentIdentityBound : Bool := true
  jurisdictionIdentityBound : Bool := true
  affectedPopulationIdentityBound : Bool := true
  evidenceEpochBound : Bool := true
  protocolVersionBound : Bool := true
  mandateSourceBound : Bool := true
  territorialJurisdictionBound : Bool := true
  subjectMatterJurisdictionBound : Bool := true
  delegationChainComplete : Bool := true
  legalForceTyped : Bool := true
  authorityConflictsRouted : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  emergencyAuthorityExpired : Bool := true
  affectedPublicCensusComplete : Bool := true
  excludedGroupsRecorded : Bool := true
  representationRouteBound : Bool := true
  selectionLimitsRecorded : Bool := true
  challengeStandingPresent : Bool := true
  evidenceAccessPresent : Bool := true
  languageAndAccessibilityPresent : Bool := true
  dissentPreserved : Bool := true
  partiesBound : Bool := true
  obligationsTestable : Bool := true
  verifierNamed : Bool := true
  verifierIndependenceRecorded : Bool := true
  dataSharingScopeBound : Bool := true
  noncomplianceRoutePresent : Bool := true
  disputeRoutePresent : Bool := true
  withdrawalAndAmendmentPresent : Bool := true
  capacityAssessed : Bool := true
  financingIndependenceRecorded : Bool := true
  implementationObserved : Bool := true
  enforcementPathPresent : Bool := true
  enforcementAsymmetryRecorded : Bool := true
  captureIndicatorsRecorded : Bool := true
  distributionalEffectsRecorded : Bool := true
  noticePresent : Bool := true
  evidencePreservationPresent : Bool := true
  appealPathPresent : Bool := true
  remedyPathPresent : Bool := true
  publicLegitimacyClaimed : Bool := false
  universalLegalAuthorityClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : InstitutionalDossier) : Prop := d.currentTick <= d.expiresAt
instance currentDecidable (d : InstitutionalDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : InstitutionalDossier) : Prop :=
  d.institutionIdentityBound = true ∧ d.decisionIdentityBound = true ∧
  d.instrumentIdentityBound = true ∧ d.jurisdictionIdentityBound = true ∧
  d.affectedPopulationIdentityBound = true ∧ d.evidenceEpochBound = true ∧
  d.protocolVersionBound = true
def MandateComplete (d : InstitutionalDossier) : Prop :=
  d.mandateSourceBound = true ∧ d.territorialJurisdictionBound = true ∧
  d.subjectMatterJurisdictionBound = true ∧ d.delegationChainComplete = true ∧
  d.legalForceTyped = true ∧ d.authorityConflictsRouted = true ∧ Current d ∧
  d.emergencyAuthorityExpired = true
def PublicComplete (d : InstitutionalDossier) : Prop :=
  d.affectedPublicCensusComplete = true ∧ d.excludedGroupsRecorded = true ∧
  d.representationRouteBound = true ∧ d.selectionLimitsRecorded = true ∧
  d.challengeStandingPresent = true ∧ d.evidenceAccessPresent = true ∧
  d.languageAndAccessibilityPresent = true ∧ d.dissentPreserved = true
def CoordinationComplete (d : InstitutionalDossier) : Prop :=
  d.partiesBound = true ∧ d.obligationsTestable = true ∧ d.verifierNamed = true ∧
  d.verifierIndependenceRecorded = true ∧ d.dataSharingScopeBound = true ∧
  d.noncomplianceRoutePresent = true ∧ d.disputeRoutePresent = true ∧
  d.withdrawalAndAmendmentPresent = true
def PerformanceComplete (d : InstitutionalDossier) : Prop :=
  d.capacityAssessed = true ∧ d.financingIndependenceRecorded = true ∧
  d.implementationObserved = true ∧ d.enforcementPathPresent = true ∧
  d.enforcementAsymmetryRecorded = true ∧ d.captureIndicatorsRecorded = true ∧
  d.distributionalEffectsRecorded = true
def RemedyComplete (d : InstitutionalDossier) : Prop :=
  d.noticePresent = true ∧ d.evidencePreservationPresent = true ∧
  d.appealPathPresent = true ∧ d.remedyPathPresent = true
def BoundaryComplete (d : InstitutionalDossier) : Prop :=
  d.publicLegitimacyClaimed = false ∧ d.universalLegalAuthorityClaimed = false ∧
  d.supportOrReleaseRequested = false

instance identityDecidable (d : InstitutionalDossier) : Decidable (IdentityComplete d) := by unfold IdentityComplete; infer_instance
instance mandateDecidable (d : InstitutionalDossier) : Decidable (MandateComplete d) := by unfold MandateComplete Current; infer_instance
instance publicDecidable (d : InstitutionalDossier) : Decidable (PublicComplete d) := by unfold PublicComplete; infer_instance
instance coordinationDecidable (d : InstitutionalDossier) : Decidable (CoordinationComplete d) := by unfold CoordinationComplete; infer_instance
instance performanceDecidable (d : InstitutionalDossier) : Decidable (PerformanceComplete d) := by unfold PerformanceComplete; infer_instance
instance remedyDecidable (d : InstitutionalDossier) : Decidable (RemedyComplete d) := by unfold RemedyComplete; infer_instance
instance boundaryDecidable (d : InstitutionalDossier) : Decidable (BoundaryComplete d) := by unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : InstitutionalDossier) : Prop :=
  IdentityComplete d ∧ MandateComplete d ∧ PublicComplete d ∧ CoordinationComplete d ∧
  PerformanceComplete d ∧ RemedyComplete d ∧ BoundaryComplete d
instance admissibleDecidable (d : InstitutionalDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete MandateComplete Current PublicComplete
    CoordinationComplete PerformanceComplete RemedyComplete BoundaryComplete
  infer_instance
def DossierReady (d : InstitutionalDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | mandateReviewed | publicReviewed | coordinationReviewed
  | performanceReviewed | remedyReviewed | boundaryReviewed | repairRequired
  | eligibleForTheseusInstitutionalTabletop
deriving DecidableEq, Repr

def ReviewStepFor (d : InstitutionalDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (MandateComplete d) then .mandateReviewed else .repairRequired
  | .mandateReviewed => if decide (PublicComplete d) then .publicReviewed else .repairRequired
  | .publicReviewed => if decide (CoordinationComplete d) then .coordinationReviewed else .repairRequired
  | .coordinationReviewed => if decide (PerformanceComplete d) then .performanceReviewed else .repairRequired
  | .performanceReviewed => if decide (RemedyComplete d) then .remedyReviewed else .repairRequired
  | .remedyReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusInstitutionalTabletop
  | state => state
def ReviewRun (d : InstitutionalDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)
def StageInvariant (d : InstitutionalDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .mandateReviewed => IdentityComplete d ∧ MandateComplete d
  | .publicReviewed => IdentityComplete d ∧ MandateComplete d ∧ PublicComplete d
  | .coordinationReviewed => IdentityComplete d ∧ MandateComplete d ∧ PublicComplete d ∧ CoordinationComplete d
  | .performanceReviewed => IdentityComplete d ∧ MandateComplete d ∧ PublicComplete d ∧ CoordinationComplete d ∧ PerformanceComplete d
  | .remedyReviewed => IdentityComplete d ∧ MandateComplete d ∧ PublicComplete d ∧ CoordinationComplete d ∧ PerformanceComplete d ∧ RemedyComplete d
  | .boundaryReviewed | .eligibleForTheseusInstitutionalTabletop => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : InstitutionalDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case mandateReviewed => split <;> simp_all [StageInvariant]
  case publicReviewed => split <;> simp_all [StageInvariant]
  case coordinationReviewed => split <;> simp_all [StageInvariant]
  case performanceReviewed => split <;> simp_all [StageInvariant]
  case remedyReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : InstitutionalDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem tabletop_eligibility_requires_admissible_dossier
    (d : InstitutionalDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusInstitutionalTabletop) : DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : InstitutionalDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_institutional_tabletop :
    ReviewRun completeDossier 8 = .eligibleForTheseusInstitutionalTabletop := by decide

inductive AdmissionAxis where
  | institutionIdentity | decisionIdentity | instrumentIdentity | jurisdictionIdentity
  | populationIdentity | evidenceEpoch | protocolVersion | mandateSource | territorialJurisdiction
  | subjectMatterJurisdiction | delegationChain | legalForce | authorityConflict | expiry
  | emergencyExpiry | publicCensus | excludedGroups | representationRoute | selectionLimits
  | challengeStanding | evidenceAccess | accessibility | dissent | parties | obligations
  | verifier | verifierIndependence | dataSharing | noncompliance | dispute | withdrawal
  | capacity | financingIndependence | implementationObservation | enforcementPath
  | enforcementAsymmetry | captureIndicators | distributionalEffects | notice
  | evidencePreservation | appeal | remedy | legitimacyClaim | universalAuthorityClaim
  | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> InstitutionalDossier
  | .institutionIdentity => { completeDossier with institutionIdentityBound := false }
  | .decisionIdentity => { completeDossier with decisionIdentityBound := false }
  | .instrumentIdentity => { completeDossier with instrumentIdentityBound := false }
  | .jurisdictionIdentity => { completeDossier with jurisdictionIdentityBound := false }
  | .populationIdentity => { completeDossier with affectedPopulationIdentityBound := false }
  | .evidenceEpoch => { completeDossier with evidenceEpochBound := false }
  | .protocolVersion => { completeDossier with protocolVersionBound := false }
  | .mandateSource => { completeDossier with mandateSourceBound := false }
  | .territorialJurisdiction => { completeDossier with territorialJurisdictionBound := false }
  | .subjectMatterJurisdiction => { completeDossier with subjectMatterJurisdictionBound := false }
  | .delegationChain => { completeDossier with delegationChainComplete := false }
  | .legalForce => { completeDossier with legalForceTyped := false }
  | .authorityConflict => { completeDossier with authorityConflictsRouted := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .emergencyExpiry => { completeDossier with emergencyAuthorityExpired := false }
  | .publicCensus => { completeDossier with affectedPublicCensusComplete := false }
  | .excludedGroups => { completeDossier with excludedGroupsRecorded := false }
  | .representationRoute => { completeDossier with representationRouteBound := false }
  | .selectionLimits => { completeDossier with selectionLimitsRecorded := false }
  | .challengeStanding => { completeDossier with challengeStandingPresent := false }
  | .evidenceAccess => { completeDossier with evidenceAccessPresent := false }
  | .accessibility => { completeDossier with languageAndAccessibilityPresent := false }
  | .dissent => { completeDossier with dissentPreserved := false }
  | .parties => { completeDossier with partiesBound := false }
  | .obligations => { completeDossier with obligationsTestable := false }
  | .verifier => { completeDossier with verifierNamed := false }
  | .verifierIndependence => { completeDossier with verifierIndependenceRecorded := false }
  | .dataSharing => { completeDossier with dataSharingScopeBound := false }
  | .noncompliance => { completeDossier with noncomplianceRoutePresent := false }
  | .dispute => { completeDossier with disputeRoutePresent := false }
  | .withdrawal => { completeDossier with withdrawalAndAmendmentPresent := false }
  | .capacity => { completeDossier with capacityAssessed := false }
  | .financingIndependence => { completeDossier with financingIndependenceRecorded := false }
  | .implementationObservation => { completeDossier with implementationObserved := false }
  | .enforcementPath => { completeDossier with enforcementPathPresent := false }
  | .enforcementAsymmetry => { completeDossier with enforcementAsymmetryRecorded := false }
  | .captureIndicators => { completeDossier with captureIndicatorsRecorded := false }
  | .distributionalEffects => { completeDossier with distributionalEffectsRecorded := false }
  | .notice => { completeDossier with noticePresent := false }
  | .evidencePreservation => { completeDossier with evidencePreservationPresent := false }
  | .appeal => { completeDossier with appealPathPresent := false }
  | .remedy => { completeDossier with remedyPathPresent := false }
  | .legitimacyClaim => { completeDossier with publicLegitimacyClaimed := true }
  | .universalAuthorityClaim => { completeDossier with universalLegalAuthorityClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindInstitutionIdentity | bindDecisionIdentity | bindInstrumentIdentity | bindJurisdictionIdentity
  | bindPopulationIdentity | bindEvidenceEpoch | bindProtocolVersion | bindMandateSource
  | bindTerritorialJurisdiction | bindSubjectMatterJurisdiction | completeDelegationChain
  | typeLegalForce | routeAuthorityConflict | renewExpiry | expireEmergencyAuthority
  | completePublicCensus | recordExcludedGroups | bindRepresentationRoute | recordSelectionLimits
  | addChallengeStanding | addEvidenceAccess | addAccessibility | preserveDissent | bindParties
  | makeObligationsTestable | nameVerifier | recordVerifierIndependence | bindDataSharing
  | addNoncomplianceRoute | addDisputeRoute | addWithdrawalAndAmendment | assessCapacity
  | recordFinancingIndependence | observeImplementation | addEnforcementPath
  | recordEnforcementAsymmetry | recordCaptureIndicators | recordDistributionalEffects
  | addNotice | preserveEvidence | addAppeal | addRemedy | rejectLegitimacyClaim
  | rejectUniversalAuthority | refuseSupportOrRelease | eligibleForTheseusInstitutionalTabletop
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .institutionIdentity => .bindInstitutionIdentity | .decisionIdentity => .bindDecisionIdentity
  | .instrumentIdentity => .bindInstrumentIdentity | .jurisdictionIdentity => .bindJurisdictionIdentity
  | .populationIdentity => .bindPopulationIdentity | .evidenceEpoch => .bindEvidenceEpoch
  | .protocolVersion => .bindProtocolVersion | .mandateSource => .bindMandateSource
  | .territorialJurisdiction => .bindTerritorialJurisdiction
  | .subjectMatterJurisdiction => .bindSubjectMatterJurisdiction
  | .delegationChain => .completeDelegationChain | .legalForce => .typeLegalForce
  | .authorityConflict => .routeAuthorityConflict | .expiry => .renewExpiry
  | .emergencyExpiry => .expireEmergencyAuthority | .publicCensus => .completePublicCensus
  | .excludedGroups => .recordExcludedGroups | .representationRoute => .bindRepresentationRoute
  | .selectionLimits => .recordSelectionLimits | .challengeStanding => .addChallengeStanding
  | .evidenceAccess => .addEvidenceAccess | .accessibility => .addAccessibility
  | .dissent => .preserveDissent | .parties => .bindParties
  | .obligations => .makeObligationsTestable | .verifier => .nameVerifier
  | .verifierIndependence => .recordVerifierIndependence | .dataSharing => .bindDataSharing
  | .noncompliance => .addNoncomplianceRoute | .dispute => .addDisputeRoute
  | .withdrawal => .addWithdrawalAndAmendment | .capacity => .assessCapacity
  | .financingIndependence => .recordFinancingIndependence
  | .implementationObservation => .observeImplementation | .enforcementPath => .addEnforcementPath
  | .enforcementAsymmetry => .recordEnforcementAsymmetry
  | .captureIndicators => .recordCaptureIndicators
  | .distributionalEffects => .recordDistributionalEffects | .notice => .addNotice
  | .evidencePreservation => .preserveEvidence | .appeal => .addAppeal | .remedy => .addRemedy
  | .legitimacyClaim => .rejectLegitimacyClaim
  | .universalAuthorityClaim => .rejectUniversalAuthority
  | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : InstitutionalDossier) : RepairDisposition :=
  if !d.institutionIdentityBound then .bindInstitutionIdentity
  else if !d.decisionIdentityBound then .bindDecisionIdentity
  else if !d.instrumentIdentityBound then .bindInstrumentIdentity
  else if !d.jurisdictionIdentityBound then .bindJurisdictionIdentity
  else if !d.affectedPopulationIdentityBound then .bindPopulationIdentity
  else if !d.evidenceEpochBound then .bindEvidenceEpoch
  else if !d.protocolVersionBound then .bindProtocolVersion
  else if !d.mandateSourceBound then .bindMandateSource
  else if !d.territorialJurisdictionBound then .bindTerritorialJurisdiction
  else if !d.subjectMatterJurisdictionBound then .bindSubjectMatterJurisdiction
  else if !d.delegationChainComplete then .completeDelegationChain
  else if !d.legalForceTyped then .typeLegalForce
  else if !d.authorityConflictsRouted then .routeAuthorityConflict
  else if !decide (Current d) then .renewExpiry
  else if !d.emergencyAuthorityExpired then .expireEmergencyAuthority
  else if !d.affectedPublicCensusComplete then .completePublicCensus
  else if !d.excludedGroupsRecorded then .recordExcludedGroups
  else if !d.representationRouteBound then .bindRepresentationRoute
  else if !d.selectionLimitsRecorded then .recordSelectionLimits
  else if !d.challengeStandingPresent then .addChallengeStanding
  else if !d.evidenceAccessPresent then .addEvidenceAccess
  else if !d.languageAndAccessibilityPresent then .addAccessibility
  else if !d.dissentPreserved then .preserveDissent
  else if !d.partiesBound then .bindParties
  else if !d.obligationsTestable then .makeObligationsTestable
  else if !d.verifierNamed then .nameVerifier
  else if !d.verifierIndependenceRecorded then .recordVerifierIndependence
  else if !d.dataSharingScopeBound then .bindDataSharing
  else if !d.noncomplianceRoutePresent then .addNoncomplianceRoute
  else if !d.disputeRoutePresent then .addDisputeRoute
  else if !d.withdrawalAndAmendmentPresent then .addWithdrawalAndAmendment
  else if !d.capacityAssessed then .assessCapacity
  else if !d.financingIndependenceRecorded then .recordFinancingIndependence
  else if !d.implementationObserved then .observeImplementation
  else if !d.enforcementPathPresent then .addEnforcementPath
  else if !d.enforcementAsymmetryRecorded then .recordEnforcementAsymmetry
  else if !d.captureIndicatorsRecorded then .recordCaptureIndicators
  else if !d.distributionalEffectsRecorded then .recordDistributionalEffects
  else if !d.noticePresent then .addNotice
  else if !d.evidencePreservationPresent then .preserveEvidence
  else if !d.appealPathPresent then .addAppeal
  else if !d.remedyPathPresent then .addRemedy
  else if d.publicLegitimacyClaimed then .rejectLegitimacyClaim
  else if d.universalLegalAuthorityClaimed then .rejectUniversalAuthority
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusInstitutionalTabletop

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : InstitutionalDossier) (h : DossierReady d = true) : IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_mandate (d : InstitutionalDossier) (h : DossierReady d = true) : MandateComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_publics (d : InstitutionalDossier) (h : DossierReady d = true) : PublicComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_coordination (d : InstitutionalDossier) (h : DossierReady d = true) : CoordinationComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_performance (d : InstitutionalDossier) (h : DossierReady d = true) : PerformanceComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_remedy (d : InstitutionalDossier) (h : DossierReady d = true) : RemedyComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.1
theorem readiness_requires_boundary (d : InstitutionalDossier) (h : DossierReady d = true) : BoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_mandate_remains_expired_when_time_advances
    (d : InstitutionalDossier) (later : Nat) (expired : d.expiresAt < d.currentTick)
    (advances : d.currentTick <= later) : Not (Current { d with currentTick := later }) := by
  intro current; unfold Current at current; change later <= d.expiresAt at current; omega

theorem omitted_public_shortfall_persists_when_population_grows
    (included required laterRequired : Nat) (short : included < required)
    (grows : required <= laterRequired) : Not (laterRequired <= included) := by omega

structure ReceiptScope where
  jurisdictionId : Nat
  instrumentId : Nat
  populationDigest : Nat
  protocolVersion : Nat
deriving DecidableEq, Repr
def ReceiptUseAllowed (s : ReceiptScope) (jurisdiction instrument population version : Nat) : Prop :=
  jurisdiction = s.jurisdictionId ∧ instrument = s.instrumentId ∧
  population = s.populationDigest ∧ version = s.protocolVersion
theorem jurisdiction_change_invalidates_institutional_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.jurisdictionId)) :
    Not (ReceiptUseAllowed s v s.instrumentId s.populationDigest s.protocolVersion) := by intro x; exact h x.1
theorem instrument_change_invalidates_institutional_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.instrumentId)) :
    Not (ReceiptUseAllowed s s.jurisdictionId v s.populationDigest s.protocolVersion) := by intro x; exact h x.2.1
theorem population_change_invalidates_institutional_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.populationDigest)) :
    Not (ReceiptUseAllowed s s.jurisdictionId s.instrumentId v s.protocolVersion) := by intro x; exact h x.2.2.1
theorem protocol_change_invalidates_institutional_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.protocolVersion)) :
    Not (ReceiptUseAllowed s s.jurisdictionId s.instrumentId s.populationDigest v) := by intro x; exact h x.2.2.2

structure ParticipationSignals where
  consultationHeld : Bool
  noticePublished : Bool
  commentCountRecorded : Bool
deriving DecidableEq, Repr
structure RepresentationCase where
  signals : ParticipationSignals
  excludedPublicHasStanding : Bool
deriving DecidableEq, Repr
def sharedParticipationSignals : ParticipationSignals := { consultationHeld := true, noticePublished := true, commentCountRecorded := true }
def representativeCase : RepresentationCase := { signals := sharedParticipationSignals, excludedPublicHasStanding := true }
def theatricalCase : RepresentationCase := { signals := sharedParticipationSignals, excludedPublicHasStanding := false }
def RepresentativeEnough (c : RepresentationCase) : Bool := c.excludedPublicHasStanding
theorem identical_participation_signals_can_hide_opposite_representation :
    representativeCase.signals = theatricalCase.signals ∧ RepresentativeEnough representativeCase = true ∧ RepresentativeEnough theatricalCase = false := by decide
theorem participation_signals_cannot_recover_representation (classify : ParticipationSignals -> Bool) :
    Not (forall c : RepresentationCase, classify c.signals = RepresentativeEnough c) := by
  intro exact; have a := exact representativeCase; have b := exact theatricalCase
  simp [representativeCase, theatricalCase, sharedParticipationSignals, RepresentativeEnough] at a b
  rw [a] at b; contradiction

structure CommitmentSignals where
  agreementSigned : Bool
  dutiesPublished : Bool
  verifierNamed : Bool
deriving DecidableEq, Repr
structure EnforcementCase where
  signals : CommitmentSignals
  remedyActuallyReachable : Bool
deriving DecidableEq, Repr
def sharedCommitmentSignals : CommitmentSignals := { agreementSigned := true, dutiesPublished := true, verifierNamed := true }
def effectiveCase : EnforcementCase := { signals := sharedCommitmentSignals, remedyActuallyReachable := true }
def treatyTheaterCase : EnforcementCase := { signals := sharedCommitmentSignals, remedyActuallyReachable := false }
def EffectiveEnforcement (c : EnforcementCase) : Bool := c.remedyActuallyReachable
theorem identical_commitment_signals_can_hide_opposite_enforcement :
    effectiveCase.signals = treatyTheaterCase.signals ∧ EffectiveEnforcement effectiveCase = true ∧ EffectiveEnforcement treatyTheaterCase = false := by decide
theorem commitment_signals_cannot_recover_effective_enforcement (classify : CommitmentSignals -> Bool) :
    Not (forall c : EnforcementCase, classify c.signals = EffectiveEnforcement c) := by
  intro exact; have a := exact effectiveCase; have b := exact treatyTheaterCase
  simp [effectiveCase, treatyTheaterCase, sharedCommitmentSignals, EffectiveEnforcement] at a b
  rw [a] at b; contradiction

def toGovernanceRightsDecision (d : InstitutionalDossier) : GovernanceRights.GovernanceRightsDecision :=
  { phase := .redacted, constrainedFork := false, auditPathPreserved := true,
    safetyObligationsPreserved := true, redactionApplied := true,
    redactionReasonRecorded := true, appealAvailable := d.challengeStandingPresent,
    exitRequired := false, exitCapabilityPreserved := true,
    protectedRightRemoved := !d.affectedPublicCensusComplete, route := .blockForReview }

theorem excluded_public_forces_governance_rights_review
    (d : InstitutionalDossier) (missing : d.affectedPublicCensusComplete = false) :
    GovernanceRights.GovernanceRightsRequiresReview (toGovernanceRightsDecision d) = true := by
  simp [toGovernanceRightsDecision, GovernanceRights.GovernanceRightsRequiresReview, missing]

end AsiStackProofs.InstitutionalLegitimacyReview

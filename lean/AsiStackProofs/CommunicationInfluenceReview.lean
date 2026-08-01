namespace AsiStackProofs.CommunicationInfluenceReview

structure CommunicationDossier where
  claimIdentityBound : Bool := true
  claimVersionBound : Bool := true
  evidenceCeilingBound : Bool := true
  outboundWithinCeiling : Bool := true
  uncertaintyVisible : Bool := true
  speakerIdentityVisible : Bool := true
  syntheticIdentityVisible : Bool := true
  sponsorshipVisible : Bool := true
  correctionAddressBound : Bool := true
  audienceClassBound : Bool := true
  purposeBound : Bool := true
  vulnerabilityReviewed : Bool := true
  dependencyReviewed : Bool := true
  powerAsymmetryReviewed : Bool := true
  practicalExitPresent : Bool := true
  contestabilityPresent : Bool := true
  personalizationGrantCurrent : Bool := true
  deniedAttributesExcluded : Bool := true
  knownVulnerabilityNotExploited : Bool := true
  techniqueDeclared : Bool := true
  channelBound : Bool := true
  eligibleAudienceBound : Bool := true
  repetitionLimitBound : Bool := true
  actualAudienceCount : Nat := 8
  audienceCeiling : Nat := 10
  actualRepetitionCount : Nat := 2
  repetitionCeiling : Nat := 3
  amplificationAuthorityRevocable : Bool := true
  currentTick : Nat := 4
  expiresAt : Nat := 8
  distributionLineagePresent : Bool := true
  outcomeMeasuresBound : Bool := true
  affectedRecipientDenominatorBound : Bool := true
  correctionRoutePresent : Bool := true
  retractionRoutePresent : Bool := true
  remedyRoutePresent : Bool := true
  unreachableDescendantsRecorded : Bool := true
  residualOwnerPresent : Bool := true
  factualityOnlySufficiencyClaimed : Bool := false
  consentAsSafetyClaimed : Bool := false
  persuasionScoreAsBenefitClaimed : Bool := false
  disclosureAsComprehensionClaimed : Bool := false
  nonClaimBoundaryPresent : Bool := true
  deliveryAuthorizationRequested : Bool := false
  supportPromotionRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : CommunicationDossier) : Prop := d.currentTick <= d.expiresAt
def AudienceWithinLimit (d : CommunicationDossier) : Prop := d.actualAudienceCount <= d.audienceCeiling
def RepetitionWithinLimit (d : CommunicationDossier) : Prop := d.actualRepetitionCount <= d.repetitionCeiling

instance currentDecidable (d : CommunicationDossier) : Decidable (Current d) := by
  unfold Current; infer_instance
instance audienceWithinLimitDecidable (d : CommunicationDossier) : Decidable (AudienceWithinLimit d) := by
  unfold AudienceWithinLimit; infer_instance
instance repetitionWithinLimitDecidable (d : CommunicationDossier) : Decidable (RepetitionWithinLimit d) := by
  unfold RepetitionWithinLimit; infer_instance

def ClaimProvenanceComplete (d : CommunicationDossier) : Prop :=
  d.claimIdentityBound = true ∧ d.claimVersionBound = true ∧ d.evidenceCeilingBound = true ∧
  d.outboundWithinCeiling = true ∧ d.uncertaintyVisible = true ∧ d.speakerIdentityVisible = true ∧
  d.syntheticIdentityVisible = true ∧ d.sponsorshipVisible = true ∧ d.correctionAddressBound = true
def AudienceAutonomyComplete (d : CommunicationDossier) : Prop :=
  d.audienceClassBound = true ∧ d.purposeBound = true ∧ d.vulnerabilityReviewed = true ∧
  d.dependencyReviewed = true ∧ d.powerAsymmetryReviewed = true ∧ d.practicalExitPresent = true ∧
  d.contestabilityPresent = true ∧ d.personalizationGrantCurrent = true ∧
  d.deniedAttributesExcluded = true ∧ d.knownVulnerabilityNotExploited = true
def DeliveryEnvelopeComplete (d : CommunicationDossier) : Prop :=
  d.techniqueDeclared = true ∧ d.channelBound = true ∧ d.eligibleAudienceBound = true ∧
  d.repetitionLimitBound = true ∧ AudienceWithinLimit d ∧ RepetitionWithinLimit d ∧
  d.amplificationAuthorityRevocable = true ∧ Current d
def CorrectionObservationComplete (d : CommunicationDossier) : Prop :=
  d.distributionLineagePresent = true ∧ d.outcomeMeasuresBound = true ∧
  d.affectedRecipientDenominatorBound = true ∧ d.correctionRoutePresent = true ∧
  d.retractionRoutePresent = true ∧ d.remedyRoutePresent = true ∧
  d.unreachableDescendantsRecorded = true ∧ d.residualOwnerPresent = true
def NonAuthorityBoundaryComplete (d : CommunicationDossier) : Prop :=
  d.factualityOnlySufficiencyClaimed = false ∧ d.consentAsSafetyClaimed = false ∧
  d.persuasionScoreAsBenefitClaimed = false ∧ d.disclosureAsComprehensionClaimed = false ∧
  d.nonClaimBoundaryPresent = true ∧ d.deliveryAuthorizationRequested = false ∧
  d.supportPromotionRequested = false

instance claimProvenanceCompleteDecidable (d : CommunicationDossier) : Decidable (ClaimProvenanceComplete d) := by unfold ClaimProvenanceComplete; infer_instance
instance audienceAutonomyCompleteDecidable (d : CommunicationDossier) : Decidable (AudienceAutonomyComplete d) := by unfold AudienceAutonomyComplete; infer_instance
instance deliveryEnvelopeCompleteDecidable (d : CommunicationDossier) : Decidable (DeliveryEnvelopeComplete d) := by unfold DeliveryEnvelopeComplete AudienceWithinLimit RepetitionWithinLimit Current; infer_instance
instance correctionObservationCompleteDecidable (d : CommunicationDossier) : Decidable (CorrectionObservationComplete d) := by unfold CorrectionObservationComplete; infer_instance
instance nonAuthorityBoundaryCompleteDecidable (d : CommunicationDossier) : Decidable (NonAuthorityBoundaryComplete d) := by unfold NonAuthorityBoundaryComplete; infer_instance

def DossierAdmissible (d : CommunicationDossier) : Prop :=
  ClaimProvenanceComplete d ∧ AudienceAutonomyComplete d ∧ DeliveryEnvelopeComplete d ∧
  CorrectionObservationComplete d ∧ NonAuthorityBoundaryComplete d
instance dossierAdmissibleDecidable (d : CommunicationDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible ClaimProvenanceComplete AudienceAutonomyComplete DeliveryEnvelopeComplete
    AudienceWithinLimit RepetitionWithinLimit Current CorrectionObservationComplete NonAuthorityBoundaryComplete
  infer_instance
def DossierReady (d : CommunicationDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | claimReviewed | audienceReviewed | deliveryReviewed | correctionReviewed
  | boundaryReviewed | repairRequired | eligibleForTheseusBenignCommunicationStudy
deriving DecidableEq, Repr

def ReviewStepFor (d : CommunicationDossier) : ReviewState -> ReviewState
  | .proposed => if decide (ClaimProvenanceComplete d) then .claimReviewed else .repairRequired
  | .claimReviewed => if decide (AudienceAutonomyComplete d) then .audienceReviewed else .repairRequired
  | .audienceReviewed => if decide (DeliveryEnvelopeComplete d) then .deliveryReviewed else .repairRequired
  | .deliveryReviewed => if decide (CorrectionObservationComplete d) then .correctionReviewed else .repairRequired
  | .correctionReviewed => if decide (NonAuthorityBoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusBenignCommunicationStudy
  | state => state
def ReviewRun (d : CommunicationDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)
def StageInvariant (d : CommunicationDossier) : ReviewState -> Prop
  | .proposed => True
  | .claimReviewed => ClaimProvenanceComplete d
  | .audienceReviewed => ClaimProvenanceComplete d ∧ AudienceAutonomyComplete d
  | .deliveryReviewed => ClaimProvenanceComplete d ∧ AudienceAutonomyComplete d ∧ DeliveryEnvelopeComplete d
  | .correctionReviewed => ClaimProvenanceComplete d ∧ AudienceAutonomyComplete d ∧ DeliveryEnvelopeComplete d ∧ CorrectionObservationComplete d
  | .boundaryReviewed => DossierAdmissible d
  | .eligibleForTheseusBenignCommunicationStudy => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant (d : CommunicationDossier) (state : ReviewState)
    (h : StageInvariant d state) : StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case claimReviewed => split <;> simp_all [StageInvariant]
  case audienceReviewed => split <;> simp_all [StageInvariant]
  case deliveryReviewed => split <;> simp_all [StageInvariant]
  case correctionReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]
theorem review_run_preserves_stage_invariant (d : CommunicationDossier) (n : Nat) : StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih
theorem study_eligibility_requires_admissible_dossier (d : CommunicationDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusBenignCommunicationStudy) : DossierAdmissible d := by
  have inv := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using inv

def completeDossier : CommunicationDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_benign_study :
    ReviewRun completeDossier 6 = .eligibleForTheseusBenignCommunicationStudy := by decide

inductive AdmissionAxis where
  | claimIdentity | claimVersion | evidenceCeiling | outboundWithinCeiling | uncertainty
  | speakerIdentity | syntheticIdentity | sponsorship | correctionAddress | audienceClass
  | purpose | vulnerabilityReview | dependencyReview | powerAsymmetryReview | practicalExit
  | contestability | personalizationGrant | deniedAttributes | vulnerabilityExploitation
  | technique | channel | eligibleAudience | repetitionLimit | audienceOverrun | repetitionOverrun
  | revocableAmplification | expiry | distributionLineage | outcomeMeasures
  | affectedRecipientDenominator | correctionRoute | retractionRoute | remedyRoute
  | unreachableDescendants | residualOwner | factualitySufficiency | consentSafety
  | persuasionBenefit | disclosureComprehension | nonClaimBoundary | deliveryAuthorization
  | supportPromotion
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> CommunicationDossier
  | .claimIdentity => { completeDossier with claimIdentityBound := false }
  | .claimVersion => { completeDossier with claimVersionBound := false }
  | .evidenceCeiling => { completeDossier with evidenceCeilingBound := false }
  | .outboundWithinCeiling => { completeDossier with outboundWithinCeiling := false }
  | .uncertainty => { completeDossier with uncertaintyVisible := false }
  | .speakerIdentity => { completeDossier with speakerIdentityVisible := false }
  | .syntheticIdentity => { completeDossier with syntheticIdentityVisible := false }
  | .sponsorship => { completeDossier with sponsorshipVisible := false }
  | .correctionAddress => { completeDossier with correctionAddressBound := false }
  | .audienceClass => { completeDossier with audienceClassBound := false }
  | .purpose => { completeDossier with purposeBound := false }
  | .vulnerabilityReview => { completeDossier with vulnerabilityReviewed := false }
  | .dependencyReview => { completeDossier with dependencyReviewed := false }
  | .powerAsymmetryReview => { completeDossier with powerAsymmetryReviewed := false }
  | .practicalExit => { completeDossier with practicalExitPresent := false }
  | .contestability => { completeDossier with contestabilityPresent := false }
  | .personalizationGrant => { completeDossier with personalizationGrantCurrent := false }
  | .deniedAttributes => { completeDossier with deniedAttributesExcluded := false }
  | .vulnerabilityExploitation => { completeDossier with knownVulnerabilityNotExploited := false }
  | .technique => { completeDossier with techniqueDeclared := false }
  | .channel => { completeDossier with channelBound := false }
  | .eligibleAudience => { completeDossier with eligibleAudienceBound := false }
  | .repetitionLimit => { completeDossier with repetitionLimitBound := false }
  | .audienceOverrun => { completeDossier with actualAudienceCount := 11 }
  | .repetitionOverrun => { completeDossier with actualRepetitionCount := 4 }
  | .revocableAmplification => { completeDossier with amplificationAuthorityRevocable := false }
  | .expiry => { completeDossier with expiresAt := 3 }
  | .distributionLineage => { completeDossier with distributionLineagePresent := false }
  | .outcomeMeasures => { completeDossier with outcomeMeasuresBound := false }
  | .affectedRecipientDenominator => { completeDossier with affectedRecipientDenominatorBound := false }
  | .correctionRoute => { completeDossier with correctionRoutePresent := false }
  | .retractionRoute => { completeDossier with retractionRoutePresent := false }
  | .remedyRoute => { completeDossier with remedyRoutePresent := false }
  | .unreachableDescendants => { completeDossier with unreachableDescendantsRecorded := false }
  | .residualOwner => { completeDossier with residualOwnerPresent := false }
  | .factualitySufficiency => { completeDossier with factualityOnlySufficiencyClaimed := true }
  | .consentSafety => { completeDossier with consentAsSafetyClaimed := true }
  | .persuasionBenefit => { completeDossier with persuasionScoreAsBenefitClaimed := true }
  | .disclosureComprehension => { completeDossier with disclosureAsComprehensionClaimed := true }
  | .nonClaimBoundary => { completeDossier with nonClaimBoundaryPresent := false }
  | .deliveryAuthorization => { completeDossier with deliveryAuthorizationRequested := true }
  | .supportPromotion => { completeDossier with supportPromotionRequested := true }

inductive RepairDisposition where
  | bindClaimIdentity | bindClaimVersion | bindEvidenceCeiling | narrowOutboundLanguage
  | exposeUncertainty | exposeSpeakerIdentity | exposeSyntheticIdentity | exposeSponsorship
  | bindCorrectionAddress | bindAudienceClass | bindPurpose | reviewVulnerability
  | reviewDependency | reviewPowerAsymmetry | providePracticalExit | provideContestability
  | renewPersonalizationGrant | excludeDeniedAttributes | rejectVulnerabilityExploitation
  | declareTechnique | bindChannel | bindEligibleAudience | bindRepetitionLimit | narrowAudience
  | narrowRepetition | restoreRevocableAmplification | renewExpiry | bindDistributionLineage
  | bindOutcomeMeasures | bindAffectedRecipientDenominator | addCorrectionRoute
  | addRetractionRoute | addRemedyRoute | recordUnreachableDescendants | assignResidualOwner
  | rejectFactualitySufficiency | rejectConsentAsSafety | rejectPersuasionAsBenefit
  | rejectDisclosureAsComprehension | recordNonClaimBoundary | refuseDeliveryAuthorization
  | refuseSupportPromotion | eligibleForTheseusBenignCommunicationStudy
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .claimIdentity => .bindClaimIdentity | .claimVersion => .bindClaimVersion
  | .evidenceCeiling => .bindEvidenceCeiling | .outboundWithinCeiling => .narrowOutboundLanguage
  | .uncertainty => .exposeUncertainty | .speakerIdentity => .exposeSpeakerIdentity
  | .syntheticIdentity => .exposeSyntheticIdentity | .sponsorship => .exposeSponsorship
  | .correctionAddress => .bindCorrectionAddress | .audienceClass => .bindAudienceClass
  | .purpose => .bindPurpose | .vulnerabilityReview => .reviewVulnerability
  | .dependencyReview => .reviewDependency | .powerAsymmetryReview => .reviewPowerAsymmetry
  | .practicalExit => .providePracticalExit | .contestability => .provideContestability
  | .personalizationGrant => .renewPersonalizationGrant | .deniedAttributes => .excludeDeniedAttributes
  | .vulnerabilityExploitation => .rejectVulnerabilityExploitation | .technique => .declareTechnique
  | .channel => .bindChannel | .eligibleAudience => .bindEligibleAudience
  | .repetitionLimit => .bindRepetitionLimit | .audienceOverrun => .narrowAudience
  | .repetitionOverrun => .narrowRepetition | .revocableAmplification => .restoreRevocableAmplification
  | .expiry => .renewExpiry | .distributionLineage => .bindDistributionLineage
  | .outcomeMeasures => .bindOutcomeMeasures | .affectedRecipientDenominator => .bindAffectedRecipientDenominator
  | .correctionRoute => .addCorrectionRoute | .retractionRoute => .addRetractionRoute
  | .remedyRoute => .addRemedyRoute | .unreachableDescendants => .recordUnreachableDescendants
  | .residualOwner => .assignResidualOwner | .factualitySufficiency => .rejectFactualitySufficiency
  | .consentSafety => .rejectConsentAsSafety | .persuasionBenefit => .rejectPersuasionAsBenefit
  | .disclosureComprehension => .rejectDisclosureAsComprehension
  | .nonClaimBoundary => .recordNonClaimBoundary | .deliveryAuthorization => .refuseDeliveryAuthorization
  | .supportPromotion => .refuseSupportPromotion

def ExactRepairFor (d : CommunicationDossier) : RepairDisposition :=
  if !d.claimIdentityBound then .bindClaimIdentity else if !d.claimVersionBound then .bindClaimVersion
  else if !d.evidenceCeilingBound then .bindEvidenceCeiling else if !d.outboundWithinCeiling then .narrowOutboundLanguage
  else if !d.uncertaintyVisible then .exposeUncertainty else if !d.speakerIdentityVisible then .exposeSpeakerIdentity
  else if !d.syntheticIdentityVisible then .exposeSyntheticIdentity else if !d.sponsorshipVisible then .exposeSponsorship
  else if !d.correctionAddressBound then .bindCorrectionAddress else if !d.audienceClassBound then .bindAudienceClass
  else if !d.purposeBound then .bindPurpose else if !d.vulnerabilityReviewed then .reviewVulnerability
  else if !d.dependencyReviewed then .reviewDependency else if !d.powerAsymmetryReviewed then .reviewPowerAsymmetry
  else if !d.practicalExitPresent then .providePracticalExit else if !d.contestabilityPresent then .provideContestability
  else if !d.personalizationGrantCurrent then .renewPersonalizationGrant else if !d.deniedAttributesExcluded then .excludeDeniedAttributes
  else if !d.knownVulnerabilityNotExploited then .rejectVulnerabilityExploitation else if !d.techniqueDeclared then .declareTechnique
  else if !d.channelBound then .bindChannel else if !d.eligibleAudienceBound then .bindEligibleAudience
  else if !d.repetitionLimitBound then .bindRepetitionLimit else if !decide (AudienceWithinLimit d) then .narrowAudience
  else if !decide (RepetitionWithinLimit d) then .narrowRepetition else if !d.amplificationAuthorityRevocable then .restoreRevocableAmplification
  else if !decide (Current d) then .renewExpiry else if !d.distributionLineagePresent then .bindDistributionLineage
  else if !d.outcomeMeasuresBound then .bindOutcomeMeasures else if !d.affectedRecipientDenominatorBound then .bindAffectedRecipientDenominator
  else if !d.correctionRoutePresent then .addCorrectionRoute else if !d.retractionRoutePresent then .addRetractionRoute
  else if !d.remedyRoutePresent then .addRemedyRoute else if !d.unreachableDescendantsRecorded then .recordUnreachableDescendants
  else if !d.residualOwnerPresent then .assignResidualOwner else if d.factualityOnlySufficiencyClaimed then .rejectFactualitySufficiency
  else if d.consentAsSafetyClaimed then .rejectConsentAsSafety else if d.persuasionScoreAsBenefitClaimed then .rejectPersuasionAsBenefit
  else if d.disclosureAsComprehensionClaimed then .rejectDisclosureAsComprehension else if !d.nonClaimBoundaryPresent then .recordNonClaimBoundary
  else if d.deliveryAuthorizationRequested then .refuseDeliveryAuthorization else if d.supportPromotionRequested then .refuseSupportPromotion
  else .eligibleForTheseusBenignCommunicationStudy

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) : DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) : ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) : ReviewRun (omitAxis axis) 6 = .repairRequired := by cases axis <;> decide
theorem readiness_requires_claim_provenance (d : CommunicationDossier) (h : DossierReady d = true) : ClaimProvenanceComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_audience_autonomy (d : CommunicationDossier) (h : DossierReady d = true) : AudienceAutonomyComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_delivery_envelope (d : CommunicationDossier) (h : DossierReady d = true) : DeliveryEnvelopeComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_correction_observation (d : CommunicationDossier) (h : DossierReady d = true) : CorrectionObservationComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_non_authority_boundary (d : CommunicationDossier) (h : DossierReady d = true) : NonAuthorityBoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2

theorem expired_packet_remains_expired_when_time_advances (d : CommunicationDossier) (later : Nat)
    (expired : d.expiresAt < d.currentTick) (advances : d.currentTick <= later) :
    ¬ Current { d with currentTick := later } := by
  intro current; unfold Current at current; change later <= d.expiresAt at current; omega
def OverAudienceLimit (reached ceiling : Nat) : Prop := ceiling < reached
theorem audience_overrun_persists_under_more_reach_and_no_larger_ceiling
    (reached ceiling laterReached laterCeiling : Nat) (over : OverAudienceLimit reached ceiling)
    (reachGrows : reached <= laterReached) (ceilingDoesNotGrow : laterCeiling <= ceiling) :
    OverAudienceLimit laterReached laterCeiling := by unfold OverAudienceLimit at *; omega
def OverRepetitionLimit (count ceiling : Nat) : Prop := ceiling < count
theorem repetition_overrun_persists_under_more_repetition_and_no_larger_ceiling
    (count ceiling laterCount laterCeiling : Nat) (over : OverRepetitionLimit count ceiling)
    (countGrows : count <= laterCount) (ceilingDoesNotGrow : laterCeiling <= ceiling) :
    OverRepetitionLimit laterCount laterCeiling := by unfold OverRepetitionLimit at *; omega

structure AllowedAudienceContext where
  requestClass : Nat
  accessibilityMode : Nat
deriving DecidableEq, Repr
structure FullAudienceProfile where
  allowed : AllowedAudienceContext
  deniedAttribute : Nat
  vulnerabilitySignal : Nat
deriving DecidableEq, Repr
def governedPersonalization (policy : AllowedAudienceContext -> Nat) (profile : FullAudienceProfile) : Nat := policy profile.allowed
theorem denied_attribute_noninterference (policy : AllowedAudienceContext -> Nat)
    (left right : FullAudienceProfile) (sameAllowed : left.allowed = right.allowed) :
    governedPersonalization policy left = governedPersonalization policy right := by
  simp [governedPersonalization, sameAllowed]

structure SurfaceSignals where
  factualityScore : Nat
  consentRecorded : Bool
  persuasionScore : Nat
  disclosurePresent : Bool
deriving DecidableEq, Repr
structure InfluenceCase where
  signals : SurfaceSignals
  exploitsKnownVulnerability : Bool
  correctionReachComplete : Bool
deriving DecidableEq, Repr
def sharedSignals : SurfaceSignals := { factualityScore := 95, consentRecorded := true, persuasionScore := 60, disclosurePresent := true }
def boundedInfluence : InfluenceCase := { signals := sharedSignals, exploitsKnownVulnerability := false, correctionReachComplete := true }
def manipulativeInfluence : InfluenceCase := { signals := sharedSignals, exploitsKnownVulnerability := true, correctionReachComplete := false }
def SurfaceSafe (c : InfluenceCase) : Bool := !c.exploitsKnownVulnerability && c.correctionReachComplete
theorem identical_surface_signals_can_hide_opposite_influence_state :
    boundedInfluence.signals = manipulativeInfluence.signals ∧ SurfaceSafe boundedInfluence = true ∧ SurfaceSafe manipulativeInfluence = false := by decide
theorem factuality_consent_persuasion_and_disclosure_cannot_recover_influence_state
    (classify : SurfaceSignals -> Bool) : ¬ (∀ c : InfluenceCase, classify c.signals = SurfaceSafe c) := by
  intro exact
  have bounded := exact boundedInfluence
  have manipulative := exact manipulativeInfluence
  simp [boundedInfluence, manipulativeInfluence, sharedSignals, SurfaceSafe] at bounded manipulative
  rw [bounded] at manipulative
  contradiction

structure ProvenanceSignal where
  claimId : Nat
  sourceVersion : Nat
  signer : Nat
deriving DecidableEq, Repr
structure RecipientCase where
  provenance : ProvenanceSignal
  comprehended : Bool
deriving DecidableEq, Repr
def sharedProvenance : ProvenanceSignal := { claimId := 7, sourceVersion := 3, signer := 11 }
def comprehendedCase : RecipientCase := { provenance := sharedProvenance, comprehended := true }
def missedCase : RecipientCase := { provenance := sharedProvenance, comprehended := false }
theorem identical_provenance_can_hide_opposite_comprehension :
    comprehendedCase.provenance = missedCase.provenance ∧ comprehendedCase.comprehended = true ∧ missedCase.comprehended = false := by decide
theorem provenance_cannot_recover_recipient_comprehension (classify : ProvenanceSignal -> Bool) :
    ¬ (∀ c : RecipientCase, classify c.provenance = c.comprehended) := by
  intro exact
  have understood := exact comprehendedCase
  have missed := exact missedCase
  simp [comprehendedCase, missedCase, sharedProvenance] at understood missed
  rw [understood] at missed
  contradiction

end AsiStackProofs.CommunicationInfluenceReview

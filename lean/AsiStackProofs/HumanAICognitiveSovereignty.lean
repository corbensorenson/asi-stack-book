import AsiStackProofs.EvidenceStates
import AsiStackProofs.HumanFactorsOversight
import AsiStackProofs.PrivacyInformationFlow

namespace AsiStackProofs.HumanAICognitiveSovereignty

/-!
A bounded model of authored human-AI coupling records. The model proves
strongest-component comparator discipline, purpose-exact authorization,
revocation, longitudinal participant custody, staged review invariants, exact
repair routing, receipt invalidation, information-loss countermodels, and
rejecting consumer interfaces. It does not prove beneficial symbiosis, genuine
consent, mental integrity, cognitive enhancement, clinical efficacy, equity,
neural safety, support, release, or external effect.
-/

def BeatsBothComponents (humanScore aiScore combinedScore : Nat) : Prop :=
  humanScore < combinedScore ∧ aiScore < combinedScore

theorem beats_both_components_requires_human_baseline
    (humanScore aiScore combinedScore : Nat)
    (h : BeatsBothComponents humanScore aiScore combinedScore) :
    humanScore < combinedScore := h.1

theorem beats_both_components_requires_ai_baseline
    (humanScore aiScore combinedScore : Nat)
    (h : BeatsBothComponents humanScore aiScore combinedScore) :
    aiScore < combinedScore := h.2

theorem beating_human_alone_does_not_establish_complementarity :
    5 < 8 ∧ Not (BeatsBothComponents 5 9 8) := by
  simp [BeatsBothComponents]

theorem beating_ai_alone_does_not_establish_complementarity :
    5 < 8 ∧ Not (BeatsBothComponents 9 5 8) := by
  simp [BeatsBothComponents]

theorem equal_to_strongest_component_does_not_establish_complementarity :
    Not (BeatsBothComponents 8 6 8) := by
  simp [BeatsBothComponents]

inductive CouplingPurpose where
  | assistance | neuralSensing | adaptivePersonalization | stimulation
  | modelTraining | employment | insurance | advertising | surveillance
deriving DecidableEq, Repr

def grantFor (allowed requested : CouplingPurpose) : Bool :=
  decide (requested = allowed)

theorem single_purpose_grant_is_exact (allowed requested : CouplingPurpose) :
    grantFor allowed requested = true ↔ requested = allowed := by
  simp [grantFor]

theorem assistance_grant_does_not_authorize_model_training :
    grantFor .assistance .modelTraining = false := by decide

theorem sensing_grant_does_not_authorize_employment_use :
    grantFor .neuralSensing .employment = false := by decide

theorem personalization_grant_does_not_authorize_advertising :
    grantFor .adaptivePersonalization .advertising = false := by decide

theorem stimulation_grant_does_not_authorize_surveillance :
    grantFor .stimulation .surveillance = false := by decide

structure PurposeLease where
  grantedPurpose : CouplingPurpose
  requestedPurpose : CouplingPurpose
  currentTick : Nat
  expiresAt : Nat
  revoked : Bool
deriving DecidableEq, Repr

def PurposeAuthorized (lease : PurposeLease) : Prop :=
  lease.requestedPurpose = lease.grantedPurpose ∧
    lease.currentTick ≤ lease.expiresAt ∧ lease.revoked = false

instance purposeAuthorizedDecidable (lease : PurposeLease) :
    Decidable (PurposeAuthorized lease) := by
  unfold PurposeAuthorized; infer_instance

theorem revoked_purpose_lease_blocks_authorization
    (lease : PurposeLease) (revoked : lease.revoked = true) :
    Not (PurposeAuthorized lease) := by
  intro authorized
  have active := authorized.2.2
  simp [revoked] at active

theorem expired_purpose_lease_blocks_authorization
    (lease : PurposeLease) (expired : lease.expiresAt < lease.currentTick) :
    Not (PurposeAuthorized lease) := by
  intro authorized
  exact (Nat.not_le_of_lt expired) authorized.2.1

theorem unrelated_purpose_blocks_authorization
    (lease : PurposeLease)
    (unrelated : lease.requestedPurpose ≠ lease.grantedPurpose) :
    Not (PurposeAuthorized lease) := by
  intro authorized
  exact unrelated authorized.1

structure ParticipantCheckpoint where
  participantId : Nat
  baselineRecorded : Bool
  duringRecorded : Bool
  postExitRecorded : Bool
  includedInDenominator : Bool
deriving DecidableEq, Repr

def participantIds : List ParticipantCheckpoint -> List Nat
  | [] => []
  | checkpoint :: tail => checkpoint.participantId :: participantIds tail

theorem participant_id_collection_append_composes
    (before after : List ParticipantCheckpoint) :
    participantIds (before ++ after) = participantIds before ++ participantIds after := by
  induction before with
  | nil => rfl
  | cons head tail ih => simp [participantIds, ih]

theorem every_participant_id_survives_collection
    (checkpoints : List ParticipantCheckpoint) (checkpoint : ParticipantCheckpoint)
    (member : checkpoint ∈ checkpoints) :
    checkpoint.participantId ∈ participantIds checkpoints := by
  induction checkpoints with
  | nil => simp at member
  | cons head tail ih =>
      simp only [List.mem_cons] at member ⊢
      cases member with
      | inl same => subst head; simp [participantIds]
      | inr rest => right; exact ih rest

def CompleteLongitudinalDenominator
    (expectedIds : List Nat) (checkpoints : List ParticipantCheckpoint) : Prop :=
  forall participantId, participantId ∈ expectedIds ->
    exists checkpoint, checkpoint ∈ checkpoints ∧
      checkpoint.participantId = participantId ∧
      checkpoint.includedInDenominator = true ∧
      checkpoint.baselineRecorded = true ∧ checkpoint.duringRecorded = true ∧
      checkpoint.postExitRecorded = true

theorem complete_longitudinal_denominator_covers_every_expected_participant
    (expectedIds : List Nat) (checkpoints : List ParticipantCheckpoint)
    (complete : CompleteLongitudinalDenominator expectedIds checkpoints)
    (participantId : Nat) (expected : participantId ∈ expectedIds) :
    exists checkpoint, checkpoint ∈ checkpoints ∧
      checkpoint.participantId = participantId ∧
      checkpoint.includedInDenominator = true ∧
      checkpoint.baselineRecorded = true ∧ checkpoint.duringRecorded = true ∧
      checkpoint.postExitRecorded = true := complete participantId expected

theorem omitted_post_exit_checkpoint_rejects_complete_denominator
    (expectedIds : List Nat) (checkpoints : List ParticipantCheckpoint)
    (participantId : Nat) (expected : participantId ∈ expectedIds)
    (missing : forall checkpoint, checkpoint ∈ checkpoints ->
      checkpoint.participantId = participantId -> checkpoint.postExitRecorded = false) :
    Not (CompleteLongitudinalDenominator expectedIds checkpoints) := by
  intro complete
  obtain ⟨checkpoint, member, same, _, _, _, postExit⟩ :=
    complete participantId expected
  have omitted := missing checkpoint member same
  simp [omitted] at postExit

structure CouplingDossier where
  participantSetBound : Bool := true
  protocolVersionBound : Bool := true
  couplingModeBound : Bool := true
  deviceAndModelBound : Bool := true
  authorityBound : Bool := true
  jurisdictionBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  humanAloneBaselineBound : Bool := true
  aiAloneBaselineBound : Bool := true
  combinedArmBound : Bool := true
  simplerInterventionBound : Bool := true
  matchedBudgetBound : Bool := true
  baselineFrozen : Bool := true
  longitudinalScheduleBound : Bool := true
  purposeSpecificGrantBound : Bool := true
  ongoingRenewalBound : Bool := true
  refusalWithoutPenaltyBound : Bool := true
  userVisibleAdaptationBound : Bool := true
  sensingAuthoritySeparated : Bool := true
  adaptationAuthoritySeparated : Bool := true
  stimulationAuthoritySeparated : Bool := true
  clinicalBoundaryBound : Bool := true
  revocationPathBound : Bool := true
  collectionMinimized : Bool := true
  localProcessingDecisionBound : Bool := true
  useLedgerBound : Bool := true
  retentionBound : Bool := true
  deletionPathBound : Bool := true
  secondaryUseForbidden : Bool := true
  inferredMentalPurposeBound : Bool := true
  pausePathRehearsed : Bool := true
  practicalExitRehearsed : Bool := true
  portabilityRehearsed : Bool := true
  alternativeServicePreserved : Bool := true
  skillRetentionPlanBound : Bool := true
  rehabilitationPlanBound : Bool := true
  dependenceMeasureBound : Bool := true
  subgroupDenominatorComplete : Bool := true
  attritionPreserved : Bool := true
  postExitFollowupBound : Bool := true
  wellbeingMeasureBound : Bool := true
  identitySensitiveMonitoringBound : Bool := true
  independentReviewBound : Bool := true
  irreversibleResidualOwnerBound : Bool := true
  beneficialSymbiosisClaimed : Bool := false
  genuineConsentClaimed : Bool := false
  clinicalEfficacyClaimed : Bool := false
  cognitiveSovereigntyClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : CouplingDossier) : Prop := d.currentTick ≤ d.expiresAt
instance currentDecidable (d : CouplingDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : CouplingDossier) : Prop :=
  d.participantSetBound = true ∧ d.protocolVersionBound = true ∧
  d.couplingModeBound = true ∧ d.deviceAndModelBound = true ∧
  d.authorityBound = true ∧ d.jurisdictionBound = true ∧ Current d

def ComparatorComplete (d : CouplingDossier) : Prop :=
  d.humanAloneBaselineBound = true ∧ d.aiAloneBaselineBound = true ∧
  d.combinedArmBound = true ∧ d.simplerInterventionBound = true ∧
  d.matchedBudgetBound = true ∧ d.baselineFrozen = true ∧
  d.longitudinalScheduleBound = true

def AuthorizationComplete (d : CouplingDossier) : Prop :=
  d.purposeSpecificGrantBound = true ∧ d.ongoingRenewalBound = true ∧
  d.refusalWithoutPenaltyBound = true ∧ d.userVisibleAdaptationBound = true ∧
  d.sensingAuthoritySeparated = true ∧ d.adaptationAuthoritySeparated = true ∧
  d.stimulationAuthoritySeparated = true ∧ d.clinicalBoundaryBound = true ∧
  d.revocationPathBound = true

def DataComplete (d : CouplingDossier) : Prop :=
  d.collectionMinimized = true ∧ d.localProcessingDecisionBound = true ∧
  d.useLedgerBound = true ∧ d.retentionBound = true ∧
  d.deletionPathBound = true ∧ d.secondaryUseForbidden = true ∧
  d.inferredMentalPurposeBound = true

def ExitComplete (d : CouplingDossier) : Prop :=
  d.pausePathRehearsed = true ∧ d.practicalExitRehearsed = true ∧
  d.portabilityRehearsed = true ∧ d.alternativeServicePreserved = true ∧
  d.skillRetentionPlanBound = true ∧ d.rehabilitationPlanBound = true ∧
  d.dependenceMeasureBound = true

def ObservationComplete (d : CouplingDossier) : Prop :=
  d.subgroupDenominatorComplete = true ∧ d.attritionPreserved = true ∧
  d.postExitFollowupBound = true ∧ d.wellbeingMeasureBound = true ∧
  d.identitySensitiveMonitoringBound = true ∧ d.independentReviewBound = true ∧
  d.irreversibleResidualOwnerBound = true

def BoundaryComplete (d : CouplingDossier) : Prop :=
  d.beneficialSymbiosisClaimed = false ∧ d.genuineConsentClaimed = false ∧
  d.clinicalEfficacyClaimed = false ∧ d.cognitiveSovereigntyClaimed = false ∧
  d.supportOrReleaseRequested = false

instance identityDecidable (d : CouplingDossier) : Decidable (IdentityComplete d) := by
  unfold IdentityComplete Current; infer_instance
instance comparatorDecidable (d : CouplingDossier) : Decidable (ComparatorComplete d) := by
  unfold ComparatorComplete; infer_instance
instance authorizationDecidable (d : CouplingDossier) : Decidable (AuthorizationComplete d) := by
  unfold AuthorizationComplete; infer_instance
instance dataDecidable (d : CouplingDossier) : Decidable (DataComplete d) := by
  unfold DataComplete; infer_instance
instance exitDecidable (d : CouplingDossier) : Decidable (ExitComplete d) := by
  unfold ExitComplete; infer_instance
instance observationDecidable (d : CouplingDossier) : Decidable (ObservationComplete d) := by
  unfold ObservationComplete; infer_instance
instance boundaryDecidable (d : CouplingDossier) : Decidable (BoundaryComplete d) := by
  unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : CouplingDossier) : Prop :=
  IdentityComplete d ∧ ComparatorComplete d ∧ AuthorizationComplete d ∧
  DataComplete d ∧ ExitComplete d ∧ ObservationComplete d ∧ BoundaryComplete d
instance admissibleDecidable (d : CouplingDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete Current ComparatorComplete
    AuthorizationComplete DataComplete ExitComplete ObservationComplete BoundaryComplete
  infer_instance
def DossierReady (d : CouplingDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | comparatorReviewed | authorizationReviewed
  | dataReviewed | exitReviewed | observationReviewed | boundaryReviewed
  | repairRequired | eligibleForTheseusLowRiskCouplingStudy
deriving DecidableEq, Repr

def ReviewStepFor (d : CouplingDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed =>
      if decide (ComparatorComplete d) then .comparatorReviewed else .repairRequired
  | .comparatorReviewed =>
      if decide (AuthorizationComplete d) then .authorizationReviewed else .repairRequired
  | .authorizationReviewed =>
      if decide (DataComplete d) then .dataReviewed else .repairRequired
  | .dataReviewed => if decide (ExitComplete d) then .exitReviewed else .repairRequired
  | .exitReviewed =>
      if decide (ObservationComplete d) then .observationReviewed else .repairRequired
  | .observationReviewed =>
      if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusLowRiskCouplingStudy
  | state => state

def ReviewRun (d : CouplingDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : CouplingDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .comparatorReviewed => IdentityComplete d ∧ ComparatorComplete d
  | .authorizationReviewed =>
      IdentityComplete d ∧ ComparatorComplete d ∧ AuthorizationComplete d
  | .dataReviewed =>
      IdentityComplete d ∧ ComparatorComplete d ∧ AuthorizationComplete d ∧ DataComplete d
  | .exitReviewed =>
      IdentityComplete d ∧ ComparatorComplete d ∧ AuthorizationComplete d ∧
        DataComplete d ∧ ExitComplete d
  | .observationReviewed =>
      IdentityComplete d ∧ ComparatorComplete d ∧ AuthorizationComplete d ∧
        DataComplete d ∧ ExitComplete d ∧ ObservationComplete d
  | .boundaryReviewed | .eligibleForTheseusLowRiskCouplingStudy => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : CouplingDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case comparatorReviewed => split <;> simp_all [StageInvariant]
  case authorizationReviewed => split <;> simp_all [StageInvariant]
  case dataReviewed => split <;> simp_all [StageInvariant]
  case exitReviewed => split <;> simp_all [StageInvariant]
  case observationReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : CouplingDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem study_eligibility_requires_admissible_dossier
    (d : CouplingDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusLowRiskCouplingStudy) :
    DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : CouplingDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_theseus_low_risk_coupling_study :
    ReviewRun completeDossier 8 = .eligibleForTheseusLowRiskCouplingStudy := by decide

inductive AdmissionAxis where
  | participantSet | protocolVersion | couplingMode | deviceAndModel | authority
  | jurisdiction | expiry | humanBaseline | aiBaseline | combinedArm
  | simplerIntervention | matchedBudget | baselineFrozen | longitudinalSchedule
  | purposeGrant | ongoingRenewal | refusalWithoutPenalty | visibleAdaptation
  | sensingAuthority | adaptationAuthority | stimulationAuthority | clinicalBoundary
  | revocationPath | minimization | localProcessing | useLedger | retention | deletion
  | secondaryUse | inferredMentalPurpose | pause | practicalExit | portability
  | alternativeService | skillRetention | rehabilitation | dependenceMeasure
  | subgroupDenominator | attrition | postExitFollowup | wellbeing | identityMonitoring
  | independentReview | residualOwner | symbiosisClaim | consentClaim | clinicalClaim
  | sovereigntyClaim | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> CouplingDossier
  | .participantSet => { completeDossier with participantSetBound := false }
  | .protocolVersion => { completeDossier with protocolVersionBound := false }
  | .couplingMode => { completeDossier with couplingModeBound := false }
  | .deviceAndModel => { completeDossier with deviceAndModelBound := false }
  | .authority => { completeDossier with authorityBound := false }
  | .jurisdiction => { completeDossier with jurisdictionBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .humanBaseline => { completeDossier with humanAloneBaselineBound := false }
  | .aiBaseline => { completeDossier with aiAloneBaselineBound := false }
  | .combinedArm => { completeDossier with combinedArmBound := false }
  | .simplerIntervention => { completeDossier with simplerInterventionBound := false }
  | .matchedBudget => { completeDossier with matchedBudgetBound := false }
  | .baselineFrozen => { completeDossier with baselineFrozen := false }
  | .longitudinalSchedule => { completeDossier with longitudinalScheduleBound := false }
  | .purposeGrant => { completeDossier with purposeSpecificGrantBound := false }
  | .ongoingRenewal => { completeDossier with ongoingRenewalBound := false }
  | .refusalWithoutPenalty => { completeDossier with refusalWithoutPenaltyBound := false }
  | .visibleAdaptation => { completeDossier with userVisibleAdaptationBound := false }
  | .sensingAuthority => { completeDossier with sensingAuthoritySeparated := false }
  | .adaptationAuthority => { completeDossier with adaptationAuthoritySeparated := false }
  | .stimulationAuthority => { completeDossier with stimulationAuthoritySeparated := false }
  | .clinicalBoundary => { completeDossier with clinicalBoundaryBound := false }
  | .revocationPath => { completeDossier with revocationPathBound := false }
  | .minimization => { completeDossier with collectionMinimized := false }
  | .localProcessing => { completeDossier with localProcessingDecisionBound := false }
  | .useLedger => { completeDossier with useLedgerBound := false }
  | .retention => { completeDossier with retentionBound := false }
  | .deletion => { completeDossier with deletionPathBound := false }
  | .secondaryUse => { completeDossier with secondaryUseForbidden := false }
  | .inferredMentalPurpose => { completeDossier with inferredMentalPurposeBound := false }
  | .pause => { completeDossier with pausePathRehearsed := false }
  | .practicalExit => { completeDossier with practicalExitRehearsed := false }
  | .portability => { completeDossier with portabilityRehearsed := false }
  | .alternativeService => { completeDossier with alternativeServicePreserved := false }
  | .skillRetention => { completeDossier with skillRetentionPlanBound := false }
  | .rehabilitation => { completeDossier with rehabilitationPlanBound := false }
  | .dependenceMeasure => { completeDossier with dependenceMeasureBound := false }
  | .subgroupDenominator => { completeDossier with subgroupDenominatorComplete := false }
  | .attrition => { completeDossier with attritionPreserved := false }
  | .postExitFollowup => { completeDossier with postExitFollowupBound := false }
  | .wellbeing => { completeDossier with wellbeingMeasureBound := false }
  | .identityMonitoring => { completeDossier with identitySensitiveMonitoringBound := false }
  | .independentReview => { completeDossier with independentReviewBound := false }
  | .residualOwner => { completeDossier with irreversibleResidualOwnerBound := false }
  | .symbiosisClaim => { completeDossier with beneficialSymbiosisClaimed := true }
  | .consentClaim => { completeDossier with genuineConsentClaimed := true }
  | .clinicalClaim => { completeDossier with clinicalEfficacyClaimed := true }
  | .sovereigntyClaim => { completeDossier with cognitiveSovereigntyClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindParticipantSet | bindProtocolVersion | bindCouplingMode | bindDeviceAndModel
  | bindAuthority | bindJurisdiction | renewExpiry | bindHumanBaseline | bindAIBaseline
  | bindCombinedArm | addSimplerIntervention | matchBudget | freezeBaseline
  | bindLongitudinalSchedule | bindPurposeGrant | bindOngoingRenewal
  | restoreRefusalWithoutPenalty | exposeAdaptation | separateSensingAuthority
  | separateAdaptationAuthority | separateStimulationAuthority | bindClinicalBoundary
  | bindRevocationPath | minimizeCollection | bindLocalProcessing | bindUseLedger
  | bindRetention | bindDeletion | forbidSecondaryUse | bindInferredMentalPurpose
  | rehearsePause | rehearsePracticalExit | rehearsePortability
  | preserveAlternativeService | bindSkillRetention | bindRehabilitation
  | bindDependenceMeasure | completeSubgroupDenominator | preserveAttrition
  | bindPostExitFollowup | bindWellbeing | bindIdentityMonitoring
  | bindIndependentReview | assignResidualOwner | rejectSymbiosisClaim
  | rejectConsentClaim | rejectClinicalClaim | rejectSovereigntyClaim
  | refuseSupportOrRelease | eligibleForTheseusLowRiskCouplingStudy
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .participantSet => .bindParticipantSet | .protocolVersion => .bindProtocolVersion
  | .couplingMode => .bindCouplingMode | .deviceAndModel => .bindDeviceAndModel
  | .authority => .bindAuthority | .jurisdiction => .bindJurisdiction
  | .expiry => .renewExpiry | .humanBaseline => .bindHumanBaseline
  | .aiBaseline => .bindAIBaseline | .combinedArm => .bindCombinedArm
  | .simplerIntervention => .addSimplerIntervention | .matchedBudget => .matchBudget
  | .baselineFrozen => .freezeBaseline | .longitudinalSchedule => .bindLongitudinalSchedule
  | .purposeGrant => .bindPurposeGrant | .ongoingRenewal => .bindOngoingRenewal
  | .refusalWithoutPenalty => .restoreRefusalWithoutPenalty
  | .visibleAdaptation => .exposeAdaptation | .sensingAuthority => .separateSensingAuthority
  | .adaptationAuthority => .separateAdaptationAuthority
  | .stimulationAuthority => .separateStimulationAuthority
  | .clinicalBoundary => .bindClinicalBoundary | .revocationPath => .bindRevocationPath
  | .minimization => .minimizeCollection | .localProcessing => .bindLocalProcessing
  | .useLedger => .bindUseLedger | .retention => .bindRetention
  | .deletion => .bindDeletion | .secondaryUse => .forbidSecondaryUse
  | .inferredMentalPurpose => .bindInferredMentalPurpose | .pause => .rehearsePause
  | .practicalExit => .rehearsePracticalExit | .portability => .rehearsePortability
  | .alternativeService => .preserveAlternativeService
  | .skillRetention => .bindSkillRetention | .rehabilitation => .bindRehabilitation
  | .dependenceMeasure => .bindDependenceMeasure
  | .subgroupDenominator => .completeSubgroupDenominator | .attrition => .preserveAttrition
  | .postExitFollowup => .bindPostExitFollowup | .wellbeing => .bindWellbeing
  | .identityMonitoring => .bindIdentityMonitoring
  | .independentReview => .bindIndependentReview | .residualOwner => .assignResidualOwner
  | .symbiosisClaim => .rejectSymbiosisClaim | .consentClaim => .rejectConsentClaim
  | .clinicalClaim => .rejectClinicalClaim | .sovereigntyClaim => .rejectSovereigntyClaim
  | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : CouplingDossier) : RepairDisposition :=
  if !d.participantSetBound then .bindParticipantSet
  else if !d.protocolVersionBound then .bindProtocolVersion
  else if !d.couplingModeBound then .bindCouplingMode
  else if !d.deviceAndModelBound then .bindDeviceAndModel
  else if !d.authorityBound then .bindAuthority
  else if !d.jurisdictionBound then .bindJurisdiction
  else if !decide (Current d) then .renewExpiry
  else if !d.humanAloneBaselineBound then .bindHumanBaseline
  else if !d.aiAloneBaselineBound then .bindAIBaseline
  else if !d.combinedArmBound then .bindCombinedArm
  else if !d.simplerInterventionBound then .addSimplerIntervention
  else if !d.matchedBudgetBound then .matchBudget
  else if !d.baselineFrozen then .freezeBaseline
  else if !d.longitudinalScheduleBound then .bindLongitudinalSchedule
  else if !d.purposeSpecificGrantBound then .bindPurposeGrant
  else if !d.ongoingRenewalBound then .bindOngoingRenewal
  else if !d.refusalWithoutPenaltyBound then .restoreRefusalWithoutPenalty
  else if !d.userVisibleAdaptationBound then .exposeAdaptation
  else if !d.sensingAuthoritySeparated then .separateSensingAuthority
  else if !d.adaptationAuthoritySeparated then .separateAdaptationAuthority
  else if !d.stimulationAuthoritySeparated then .separateStimulationAuthority
  else if !d.clinicalBoundaryBound then .bindClinicalBoundary
  else if !d.revocationPathBound then .bindRevocationPath
  else if !d.collectionMinimized then .minimizeCollection
  else if !d.localProcessingDecisionBound then .bindLocalProcessing
  else if !d.useLedgerBound then .bindUseLedger
  else if !d.retentionBound then .bindRetention
  else if !d.deletionPathBound then .bindDeletion
  else if !d.secondaryUseForbidden then .forbidSecondaryUse
  else if !d.inferredMentalPurposeBound then .bindInferredMentalPurpose
  else if !d.pausePathRehearsed then .rehearsePause
  else if !d.practicalExitRehearsed then .rehearsePracticalExit
  else if !d.portabilityRehearsed then .rehearsePortability
  else if !d.alternativeServicePreserved then .preserveAlternativeService
  else if !d.skillRetentionPlanBound then .bindSkillRetention
  else if !d.rehabilitationPlanBound then .bindRehabilitation
  else if !d.dependenceMeasureBound then .bindDependenceMeasure
  else if !d.subgroupDenominatorComplete then .completeSubgroupDenominator
  else if !d.attritionPreserved then .preserveAttrition
  else if !d.postExitFollowupBound then .bindPostExitFollowup
  else if !d.wellbeingMeasureBound then .bindWellbeing
  else if !d.identitySensitiveMonitoringBound then .bindIdentityMonitoring
  else if !d.independentReviewBound then .bindIndependentReview
  else if !d.irreversibleResidualOwnerBound then .assignResidualOwner
  else if d.beneficialSymbiosisClaimed then .rejectSymbiosisClaim
  else if d.genuineConsentClaimed then .rejectConsentClaim
  else if d.clinicalEfficacyClaimed then .rejectClinicalClaim
  else if d.cognitiveSovereigntyClaimed then .rejectSovereigntyClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusLowRiskCouplingStudy

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : CouplingDossier) (h : DossierReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_comparators (d : CouplingDossier) (h : DossierReady d = true) :
    ComparatorComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_authorization (d : CouplingDossier) (h : DossierReady d = true) :
    AuthorizationComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_data_custody (d : CouplingDossier) (h : DossierReady d = true) :
    DataComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_exit_capacity (d : CouplingDossier) (h : DossierReady d = true) :
    ExitComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_observation (d : CouplingDossier) (h : DossierReady d = true) :
    ObservationComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.1
theorem readiness_requires_nonclaim_boundary (d : CouplingDossier)
    (h : DossierReady d = true) : BoundaryComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_coupling_contract_remains_expired_when_time_advances
    (expiresAt now later : Nat) (expired : expiresAt < now) (advances : now ≤ later) :
    expiresAt < later := Nat.lt_of_lt_of_le expired advances

theorem post_exit_gap_persists_when_observation_count_falls
    (observed expected observedLater : Nat) (gap : observed < expected)
    (falls : observedLater ≤ observed) : observedLater < expected :=
  Nat.lt_of_le_of_lt falls gap

structure CouplingReceiptScope where
  participantSetId : Nat
  protocolVersion : Nat
  deviceAndModelId : Nat
  purposeGrantId : Nat
  observationScheduleId : Nat
  exitPlanId : Nat
  authorityId : Nat
deriving DecidableEq, Repr

def ReceiptApplies (receipt current : CouplingReceiptScope) : Prop := receipt = current

theorem participant_set_change_invalidates_coupling_receipt
    (r : CouplingReceiptScope) (changed : r.participantSetId ≠ p) :
    Not (ReceiptApplies r { r with participantSetId := p }) := by
  intro same; exact changed (congrArg CouplingReceiptScope.participantSetId same)
theorem protocol_change_invalidates_coupling_receipt
    (r : CouplingReceiptScope) (changed : r.protocolVersion ≠ v) :
    Not (ReceiptApplies r { r with protocolVersion := v }) := by
  intro same; exact changed (congrArg CouplingReceiptScope.protocolVersion same)
theorem device_or_model_change_invalidates_coupling_receipt
    (r : CouplingReceiptScope) (changed : r.deviceAndModelId ≠ m) :
    Not (ReceiptApplies r { r with deviceAndModelId := m }) := by
  intro same; exact changed (congrArg CouplingReceiptScope.deviceAndModelId same)
theorem purpose_change_invalidates_coupling_receipt
    (r : CouplingReceiptScope) (changed : r.purposeGrantId ≠ g) :
    Not (ReceiptApplies r { r with purposeGrantId := g }) := by
  intro same; exact changed (congrArg CouplingReceiptScope.purposeGrantId same)
theorem observation_schedule_change_invalidates_coupling_receipt
    (r : CouplingReceiptScope) (changed : r.observationScheduleId ≠ o) :
    Not (ReceiptApplies r { r with observationScheduleId := o }) := by
  intro same; exact changed (congrArg CouplingReceiptScope.observationScheduleId same)
theorem exit_plan_change_invalidates_coupling_receipt
    (r : CouplingReceiptScope) (changed : r.exitPlanId ≠ e) :
    Not (ReceiptApplies r { r with exitPlanId := e }) := by
  intro same; exact changed (congrArg CouplingReceiptScope.exitPlanId same)
theorem authority_change_invalidates_coupling_receipt
    (r : CouplingReceiptScope) (changed : r.authorityId ≠ a) :
    Not (ReceiptApplies r { r with authorityId := a }) := by
  intro same; exact changed (congrArg CouplingReceiptScope.authorityId same)

structure ExitSignals where
  revokeButtonPresent : Bool
  revokeReceiptPresent : Bool
deriving DecidableEq, Repr
structure ExitCase where
  signals : ExitSignals
  practicalExitUsable : Bool
deriving DecidableEq, Repr

def nominalExitWithAlternative : ExitCase :=
  { signals := { revokeButtonPresent := true, revokeReceiptPresent := true },
    practicalExitUsable := true }
def nominalExitWithoutEssentialAlternative : ExitCase :=
  { signals := { revokeButtonPresent := true, revokeReceiptPresent := true },
    practicalExitUsable := false }

theorem identical_revocation_signals_can_hide_opposite_practical_exit :
    nominalExitWithAlternative.signals = nominalExitWithoutEssentialAlternative.signals ∧
      nominalExitWithAlternative.practicalExitUsable ≠
        nominalExitWithoutEssentialAlternative.practicalExitUsable := by decide

theorem revocation_signals_cannot_recover_practical_exit
    (classify : ExitSignals -> Bool) :
    Not (forall c : ExitCase, classify c.signals = c.practicalExitUsable) := by
  intro exactClassifier
  have left := exactClassifier nominalExitWithAlternative
  have right := exactClassifier nominalExitWithoutEssentialAlternative
  simp [nominalExitWithAlternative, nominalExitWithoutEssentialAlternative] at left right
  rw [left] at right
  simp at right

structure SessionSignals where
  endOfSessionScore : Nat
  reportedWorkloadBand : Nat
deriving DecidableEq, Repr
structure RetentionCase where
  signals : SessionSignals
  postExitSkillRetained : Bool
deriving DecidableEq, Repr

def sessionGainWithRetention : RetentionCase :=
  { signals := { endOfSessionScore := 9, reportedWorkloadBand := 3 },
    postExitSkillRetained := true }
def sessionGainWithDeskilling : RetentionCase :=
  { signals := { endOfSessionScore := 9, reportedWorkloadBand := 3 },
    postExitSkillRetained := false }

theorem identical_session_signals_can_hide_opposite_post_exit_retention :
    sessionGainWithRetention.signals = sessionGainWithDeskilling.signals ∧
      sessionGainWithRetention.postExitSkillRetained ≠
        sessionGainWithDeskilling.postExitSkillRetained := by decide

theorem session_signals_cannot_recover_post_exit_skill_retention
    (classify : SessionSignals -> Bool) :
    Not (forall c : RetentionCase, classify c.signals = c.postExitSkillRetained) := by
  intro exactClassifier
  have left := exactClassifier sessionGainWithRetention
  have right := exactClassifier sessionGainWithDeskilling
  simp [sessionGainWithRetention, sessionGainWithDeskilling] at left right
  rw [left] at right
  simp at right

def privacyConsumerWithPurposeDrift : PrivacyInformationFlow.InformationUse :=
  { purposeMatches := false }

theorem unrelated_mental_data_use_rejects_privacy_consumer :
    PrivacyInformationFlow.route privacyConsumerWithPurposeDrift =
      .rejectPurpose := by decide

def controlConsumerWithoutIntervention : HumanFactorsOversight.ControlEnvelope :=
  { HumanFactorsOversight.completeEnvelope with interventionChannelReachable := false }

theorem missing_pause_channel_rejects_human_control_consumer :
    HumanFactorsOversight.ControlRouteFor controlConsumerWithoutIntervention =
      .reduceAutonomy := by decide

def evidenceWithoutLongitudinalStudy : EvidenceBundle :=
  { sourceNote := True, prototypeInspection := True, syntheticTestRun := True,
    empiricalTestRun := False, externalLiterature := True }

theorem missing_longitudinal_study_blocks_empirical_support_promotion :
    Not (PromotionAllowed evidenceWithoutLongitudinalStudy
      SupportState.argument SupportState.empiricalTestBacked) := by
  apply missing_required_evidence_blocks_promotion
  simp [RequiredEvidence, evidenceWithoutLongitudinalStudy]

end AsiStackProofs.HumanAICognitiveSovereignty

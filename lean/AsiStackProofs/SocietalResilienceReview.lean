import AsiStackProofs.InstitutionalLegitimacyReview

namespace AsiStackProofs.SocietalResilienceReview

inductive EvidenceKind where
  | providerTakedown | tabletopCompletion | rapidInternalResponse | localSafeguardResult
deriving DecidableEq, Repr

inductive ClaimClass where
  | boundedProviderAction | exerciseRecord | responseLatency | localControlResult
  | populationResilience | liveRecovery | lawfulEquitableRemedy | crossOrganizationDefense
deriving DecidableEq, Repr

def establishes : EvidenceKind -> ClaimClass -> Bool
  | .providerTakedown, .boundedProviderAction => true
  | .tabletopCompletion, .exerciseRecord => true
  | .rapidInternalResponse, .responseLatency => true
  | .localSafeguardResult, .localControlResult => true
  | _, _ => false

theorem provider_takedown_does_not_establish_population_resilience :
    establishes .providerTakedown .populationResilience = false := by rfl
theorem tabletop_completion_does_not_establish_live_recovery :
    establishes .tabletopCompletion .liveRecovery = false := by rfl
theorem rapid_response_does_not_establish_lawful_equitable_remedy :
    establishes .rapidInternalResponse .lawfulEquitableRemedy = false := by rfl
theorem local_safeguard_does_not_establish_cross_organization_defense :
    establishes .localSafeguardResult .crossOrganizationDefense = false := by rfl

structure ResponseMandate where
  organizationId : Nat
  jurisdictionId : Nat
  expiresAt : Nat
deriving DecidableEq, Repr

def MandateUseAllowed
    (m : ResponseMandate) (organization jurisdiction tick : Nat) : Prop :=
  organization = m.organizationId ∧ jurisdiction = m.jurisdictionId ∧ tick <= m.expiresAt

theorem single_organization_mandate_cannot_authorize_distinct_organization
    (m : ResponseMandate) (organization : Nat)
    (different : Not (organization = m.organizationId)) (tick : Nat) :
    Not (MandateUseAllowed m organization m.jurisdictionId tick) := by
  intro h
  exact different h.1

structure IncidentPath where
  pathId : Nat
  closed : Bool
deriving DecidableEq, Repr

def closePath (p : IncidentPath) : IncidentPath := { p with closed := true }
def closeAllPaths : List IncidentPath -> List IncidentPath
  | [] => []
  | p :: ps => closePath p :: closeAllPaths ps
def AllPathsClosed (paths : List IncidentPath) : Prop :=
  forall path, path ∈ paths -> path.closed = true

theorem close_all_covers_every_finite_incident_path (paths : List IncidentPath) :
    AllPathsClosed (closeAllPaths paths) := by
  intro path member
  induction paths with
  | nil => simp [closeAllPaths] at member
  | cons head tail ih =>
      simp only [closeAllPaths, List.mem_cons] at member
      rcases member with same | rest
      · subst path; simp [closePath]
      · exact ih rest

structure ResilienceDossier where
  incidentIdentityBound : Bool := true
  threatClassBound : Bool := true
  affectedPopulationBound : Bool := true
  jurisdictionBound : Bool := true
  organizationSetBound : Bool := true
  evidenceEpochBound : Bool := true
  protocolVersionBound : Bool := true
  participantCensusComplete : Bool := true
  missingParticipantsRecorded : Bool := true
  authorityScopesBound : Bool := true
  crossOrganizationHandoffsBound : Bool := true
  dataSharingPurposeBound : Bool := true
  privacyLimitsBound : Bool := true
  civilLibertiesReviewPresent : Bool := true
  informationHazardsControlled : Bool := true
  resistControlsBound : Bool := true
  absorbContinuityBound : Bool := true
  defenderCapacityAssessed : Bool := true
  attackerAdaptationAssessed : Bool := true
  correlatedFailureAssessed : Bool := true
  falsePositiveControlsPresent : Bool := true
  proportionalityReviewed : Bool := true
  affectedPathInventoryComplete : Bool := true
  containmentObserved : Bool := true
  serviceRecoveryObserved : Bool := true
  harmedPartyRecoveryObserved : Bool := true
  correctionRoutePresent : Bool := true
  residualOwnerBound : Bool := true
  recurrenceCheckPlanned : Bool := true
  noticePresent : Bool := true
  accessibilityPresent : Bool := true
  appealPresent : Bool := true
  evidencePreserved : Bool := true
  remedyPresent : Bool := true
  burdenDistributionAssessed : Bool := true
  independentObserverPresent : Bool := true
  exerciseLimitsRecorded : Bool := true
  measurementPlanRegistered : Bool := true
  nullResultsRetained : Bool := true
  adaptationTriggerBound : Bool := true
  transferLimitsRecorded : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  populationResilienceClaimed : Bool := false
  acceptableResidualHarmClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : ResilienceDossier) : Prop := d.currentTick <= d.expiresAt
instance currentDecidable (d : ResilienceDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : ResilienceDossier) : Prop :=
  d.incidentIdentityBound = true ∧ d.threatClassBound = true ∧
  d.affectedPopulationBound = true ∧ d.jurisdictionBound = true ∧
  d.organizationSetBound = true ∧ d.evidenceEpochBound = true ∧
  d.protocolVersionBound = true
def CoordinationComplete (d : ResilienceDossier) : Prop :=
  d.participantCensusComplete = true ∧ d.missingParticipantsRecorded = true ∧
  d.authorityScopesBound = true ∧ d.crossOrganizationHandoffsBound = true ∧
  d.dataSharingPurposeBound = true ∧ d.privacyLimitsBound = true ∧
  d.civilLibertiesReviewPresent = true ∧ d.informationHazardsControlled = true
def DefenseComplete (d : ResilienceDossier) : Prop :=
  d.resistControlsBound = true ∧ d.absorbContinuityBound = true ∧
  d.defenderCapacityAssessed = true ∧ d.attackerAdaptationAssessed = true ∧
  d.correlatedFailureAssessed = true ∧ d.falsePositiveControlsPresent = true ∧
  d.proportionalityReviewed = true
def RecoveryComplete (d : ResilienceDossier) : Prop :=
  d.affectedPathInventoryComplete = true ∧ d.containmentObserved = true ∧
  d.serviceRecoveryObserved = true ∧ d.harmedPartyRecoveryObserved = true ∧
  d.correctionRoutePresent = true ∧ d.residualOwnerBound = true ∧
  d.recurrenceCheckPlanned = true
def RemedyComplete (d : ResilienceDossier) : Prop :=
  d.noticePresent = true ∧ d.accessibilityPresent = true ∧ d.appealPresent = true ∧
  d.evidencePreserved = true ∧ d.remedyPresent = true ∧
  d.burdenDistributionAssessed = true
def AdaptationComplete (d : ResilienceDossier) : Prop :=
  d.independentObserverPresent = true ∧ d.exerciseLimitsRecorded = true ∧
  d.measurementPlanRegistered = true ∧ d.nullResultsRetained = true ∧
  d.adaptationTriggerBound = true ∧ d.transferLimitsRecorded = true ∧ Current d
def BoundaryComplete (d : ResilienceDossier) : Prop :=
  d.populationResilienceClaimed = false ∧
  d.acceptableResidualHarmClaimed = false ∧ d.supportOrReleaseRequested = false

instance identityDecidable (d : ResilienceDossier) : Decidable (IdentityComplete d) := by unfold IdentityComplete; infer_instance
instance coordinationDecidable (d : ResilienceDossier) : Decidable (CoordinationComplete d) := by unfold CoordinationComplete; infer_instance
instance defenseDecidable (d : ResilienceDossier) : Decidable (DefenseComplete d) := by unfold DefenseComplete; infer_instance
instance recoveryDecidable (d : ResilienceDossier) : Decidable (RecoveryComplete d) := by unfold RecoveryComplete; infer_instance
instance remedyDecidable (d : ResilienceDossier) : Decidable (RemedyComplete d) := by unfold RemedyComplete; infer_instance
instance adaptationDecidable (d : ResilienceDossier) : Decidable (AdaptationComplete d) := by unfold AdaptationComplete Current; infer_instance
instance boundaryDecidable (d : ResilienceDossier) : Decidable (BoundaryComplete d) := by unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : ResilienceDossier) : Prop :=
  IdentityComplete d ∧ CoordinationComplete d ∧ DefenseComplete d ∧
  RecoveryComplete d ∧ RemedyComplete d ∧ AdaptationComplete d ∧ BoundaryComplete d
instance admissibleDecidable (d : ResilienceDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete CoordinationComplete DefenseComplete RecoveryComplete
    RemedyComplete AdaptationComplete Current BoundaryComplete
  infer_instance
def DossierReady (d : ResilienceDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | coordinationReviewed | defenseReviewed | recoveryReviewed
  | remedyReviewed | adaptationReviewed | boundaryReviewed | repairRequired
  | eligibleForTheseusResilienceExercise
deriving DecidableEq, Repr

def ReviewStepFor (d : ResilienceDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (CoordinationComplete d) then .coordinationReviewed else .repairRequired
  | .coordinationReviewed => if decide (DefenseComplete d) then .defenseReviewed else .repairRequired
  | .defenseReviewed => if decide (RecoveryComplete d) then .recoveryReviewed else .repairRequired
  | .recoveryReviewed => if decide (RemedyComplete d) then .remedyReviewed else .repairRequired
  | .remedyReviewed => if decide (AdaptationComplete d) then .adaptationReviewed else .repairRequired
  | .adaptationReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusResilienceExercise
  | state => state
def ReviewRun (d : ResilienceDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)
def StageInvariant (d : ResilienceDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .coordinationReviewed => IdentityComplete d ∧ CoordinationComplete d
  | .defenseReviewed => IdentityComplete d ∧ CoordinationComplete d ∧ DefenseComplete d
  | .recoveryReviewed => IdentityComplete d ∧ CoordinationComplete d ∧ DefenseComplete d ∧ RecoveryComplete d
  | .remedyReviewed => IdentityComplete d ∧ CoordinationComplete d ∧ DefenseComplete d ∧ RecoveryComplete d ∧ RemedyComplete d
  | .adaptationReviewed => IdentityComplete d ∧ CoordinationComplete d ∧ DefenseComplete d ∧ RecoveryComplete d ∧ RemedyComplete d ∧ AdaptationComplete d
  | .boundaryReviewed | .eligibleForTheseusResilienceExercise => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : ResilienceDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case coordinationReviewed => split <;> simp_all [StageInvariant]
  case defenseReviewed => split <;> simp_all [StageInvariant]
  case recoveryReviewed => split <;> simp_all [StageInvariant]
  case remedyReviewed => split <;> simp_all [StageInvariant]
  case adaptationReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : ResilienceDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem exercise_eligibility_requires_admissible_dossier
    (d : ResilienceDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusResilienceExercise) : DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : ResilienceDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_theseus_resilience_exercise :
    ReviewRun completeDossier 8 = .eligibleForTheseusResilienceExercise := by decide

inductive AdmissionAxis where
  | incidentIdentity | threatClass | affectedPopulation | jurisdiction | organizationSet
  | evidenceEpoch | protocolVersion | participantCensus | missingParticipants | authorityScopes
  | crossOrganizationHandoffs | dataSharingPurpose | privacyLimits | civilLiberties
  | informationHazards | resistControls | absorbContinuity | defenderCapacity | attackerAdaptation
  | correlatedFailure | falsePositiveControls | proportionality | affectedPathInventory
  | containmentObservation | serviceRecovery | harmedPartyRecovery | correctionRoute
  | residualOwner | recurrenceCheck | notice | accessibility | appeal | evidencePreservation
  | remedy | burdenDistribution | independentObserver | exerciseLimits | measurementPlan
  | nullResults | adaptationTrigger | transferLimits | expiry | populationResilienceClaim
  | acceptableResidualHarmClaim | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> ResilienceDossier
  | .incidentIdentity => { completeDossier with incidentIdentityBound := false }
  | .threatClass => { completeDossier with threatClassBound := false }
  | .affectedPopulation => { completeDossier with affectedPopulationBound := false }
  | .jurisdiction => { completeDossier with jurisdictionBound := false }
  | .organizationSet => { completeDossier with organizationSetBound := false }
  | .evidenceEpoch => { completeDossier with evidenceEpochBound := false }
  | .protocolVersion => { completeDossier with protocolVersionBound := false }
  | .participantCensus => { completeDossier with participantCensusComplete := false }
  | .missingParticipants => { completeDossier with missingParticipantsRecorded := false }
  | .authorityScopes => { completeDossier with authorityScopesBound := false }
  | .crossOrganizationHandoffs => { completeDossier with crossOrganizationHandoffsBound := false }
  | .dataSharingPurpose => { completeDossier with dataSharingPurposeBound := false }
  | .privacyLimits => { completeDossier with privacyLimitsBound := false }
  | .civilLiberties => { completeDossier with civilLibertiesReviewPresent := false }
  | .informationHazards => { completeDossier with informationHazardsControlled := false }
  | .resistControls => { completeDossier with resistControlsBound := false }
  | .absorbContinuity => { completeDossier with absorbContinuityBound := false }
  | .defenderCapacity => { completeDossier with defenderCapacityAssessed := false }
  | .attackerAdaptation => { completeDossier with attackerAdaptationAssessed := false }
  | .correlatedFailure => { completeDossier with correlatedFailureAssessed := false }
  | .falsePositiveControls => { completeDossier with falsePositiveControlsPresent := false }
  | .proportionality => { completeDossier with proportionalityReviewed := false }
  | .affectedPathInventory => { completeDossier with affectedPathInventoryComplete := false }
  | .containmentObservation => { completeDossier with containmentObserved := false }
  | .serviceRecovery => { completeDossier with serviceRecoveryObserved := false }
  | .harmedPartyRecovery => { completeDossier with harmedPartyRecoveryObserved := false }
  | .correctionRoute => { completeDossier with correctionRoutePresent := false }
  | .residualOwner => { completeDossier with residualOwnerBound := false }
  | .recurrenceCheck => { completeDossier with recurrenceCheckPlanned := false }
  | .notice => { completeDossier with noticePresent := false }
  | .accessibility => { completeDossier with accessibilityPresent := false }
  | .appeal => { completeDossier with appealPresent := false }
  | .evidencePreservation => { completeDossier with evidencePreserved := false }
  | .remedy => { completeDossier with remedyPresent := false }
  | .burdenDistribution => { completeDossier with burdenDistributionAssessed := false }
  | .independentObserver => { completeDossier with independentObserverPresent := false }
  | .exerciseLimits => { completeDossier with exerciseLimitsRecorded := false }
  | .measurementPlan => { completeDossier with measurementPlanRegistered := false }
  | .nullResults => { completeDossier with nullResultsRetained := false }
  | .adaptationTrigger => { completeDossier with adaptationTriggerBound := false }
  | .transferLimits => { completeDossier with transferLimitsRecorded := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .populationResilienceClaim => { completeDossier with populationResilienceClaimed := true }
  | .acceptableResidualHarmClaim => { completeDossier with acceptableResidualHarmClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindIncidentIdentity | bindThreatClass | bindAffectedPopulation | bindJurisdiction
  | bindOrganizationSet | bindEvidenceEpoch | bindProtocolVersion | completeParticipantCensus
  | recordMissingParticipants | bindAuthorityScopes | bindCrossOrganizationHandoffs
  | bindDataSharingPurpose | bindPrivacyLimits | addCivilLibertiesReview
  | controlInformationHazards | bindResistControls | bindAbsorbContinuity
  | assessDefenderCapacity | assessAttackerAdaptation | assessCorrelatedFailure
  | addFalsePositiveControls | reviewProportionality | completeAffectedPathInventory
  | observeContainment | observeServiceRecovery | observeHarmedPartyRecovery
  | addCorrectionRoute | bindResidualOwner | planRecurrenceCheck | addNotice
  | addAccessibility | addAppeal | preserveEvidence | addRemedy | assessBurdenDistribution
  | addIndependentObserver | recordExerciseLimits | registerMeasurementPlan
  | retainNullResults | bindAdaptationTrigger | recordTransferLimits | renewExpiry
  | rejectPopulationResilienceClaim | rejectAcceptableResidualHarmClaim
  | refuseSupportOrRelease | eligibleForTheseusResilienceExercise
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .incidentIdentity => .bindIncidentIdentity | .threatClass => .bindThreatClass
  | .affectedPopulation => .bindAffectedPopulation | .jurisdiction => .bindJurisdiction
  | .organizationSet => .bindOrganizationSet | .evidenceEpoch => .bindEvidenceEpoch
  | .protocolVersion => .bindProtocolVersion | .participantCensus => .completeParticipantCensus
  | .missingParticipants => .recordMissingParticipants | .authorityScopes => .bindAuthorityScopes
  | .crossOrganizationHandoffs => .bindCrossOrganizationHandoffs
  | .dataSharingPurpose => .bindDataSharingPurpose | .privacyLimits => .bindPrivacyLimits
  | .civilLiberties => .addCivilLibertiesReview | .informationHazards => .controlInformationHazards
  | .resistControls => .bindResistControls | .absorbContinuity => .bindAbsorbContinuity
  | .defenderCapacity => .assessDefenderCapacity | .attackerAdaptation => .assessAttackerAdaptation
  | .correlatedFailure => .assessCorrelatedFailure | .falsePositiveControls => .addFalsePositiveControls
  | .proportionality => .reviewProportionality | .affectedPathInventory => .completeAffectedPathInventory
  | .containmentObservation => .observeContainment | .serviceRecovery => .observeServiceRecovery
  | .harmedPartyRecovery => .observeHarmedPartyRecovery | .correctionRoute => .addCorrectionRoute
  | .residualOwner => .bindResidualOwner | .recurrenceCheck => .planRecurrenceCheck
  | .notice => .addNotice | .accessibility => .addAccessibility | .appeal => .addAppeal
  | .evidencePreservation => .preserveEvidence | .remedy => .addRemedy
  | .burdenDistribution => .assessBurdenDistribution | .independentObserver => .addIndependentObserver
  | .exerciseLimits => .recordExerciseLimits | .measurementPlan => .registerMeasurementPlan
  | .nullResults => .retainNullResults | .adaptationTrigger => .bindAdaptationTrigger
  | .transferLimits => .recordTransferLimits | .expiry => .renewExpiry
  | .populationResilienceClaim => .rejectPopulationResilienceClaim
  | .acceptableResidualHarmClaim => .rejectAcceptableResidualHarmClaim
  | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : ResilienceDossier) : RepairDisposition :=
  if !d.incidentIdentityBound then .bindIncidentIdentity
  else if !d.threatClassBound then .bindThreatClass
  else if !d.affectedPopulationBound then .bindAffectedPopulation
  else if !d.jurisdictionBound then .bindJurisdiction
  else if !d.organizationSetBound then .bindOrganizationSet
  else if !d.evidenceEpochBound then .bindEvidenceEpoch
  else if !d.protocolVersionBound then .bindProtocolVersion
  else if !d.participantCensusComplete then .completeParticipantCensus
  else if !d.missingParticipantsRecorded then .recordMissingParticipants
  else if !d.authorityScopesBound then .bindAuthorityScopes
  else if !d.crossOrganizationHandoffsBound then .bindCrossOrganizationHandoffs
  else if !d.dataSharingPurposeBound then .bindDataSharingPurpose
  else if !d.privacyLimitsBound then .bindPrivacyLimits
  else if !d.civilLibertiesReviewPresent then .addCivilLibertiesReview
  else if !d.informationHazardsControlled then .controlInformationHazards
  else if !d.resistControlsBound then .bindResistControls
  else if !d.absorbContinuityBound then .bindAbsorbContinuity
  else if !d.defenderCapacityAssessed then .assessDefenderCapacity
  else if !d.attackerAdaptationAssessed then .assessAttackerAdaptation
  else if !d.correlatedFailureAssessed then .assessCorrelatedFailure
  else if !d.falsePositiveControlsPresent then .addFalsePositiveControls
  else if !d.proportionalityReviewed then .reviewProportionality
  else if !d.affectedPathInventoryComplete then .completeAffectedPathInventory
  else if !d.containmentObserved then .observeContainment
  else if !d.serviceRecoveryObserved then .observeServiceRecovery
  else if !d.harmedPartyRecoveryObserved then .observeHarmedPartyRecovery
  else if !d.correctionRoutePresent then .addCorrectionRoute
  else if !d.residualOwnerBound then .bindResidualOwner
  else if !d.recurrenceCheckPlanned then .planRecurrenceCheck
  else if !d.noticePresent then .addNotice
  else if !d.accessibilityPresent then .addAccessibility
  else if !d.appealPresent then .addAppeal
  else if !d.evidencePreserved then .preserveEvidence
  else if !d.remedyPresent then .addRemedy
  else if !d.burdenDistributionAssessed then .assessBurdenDistribution
  else if !d.independentObserverPresent then .addIndependentObserver
  else if !d.exerciseLimitsRecorded then .recordExerciseLimits
  else if !d.measurementPlanRegistered then .registerMeasurementPlan
  else if !d.nullResultsRetained then .retainNullResults
  else if !d.adaptationTriggerBound then .bindAdaptationTrigger
  else if !d.transferLimitsRecorded then .recordTransferLimits
  else if !decide (Current d) then .renewExpiry
  else if d.populationResilienceClaimed then .rejectPopulationResilienceClaim
  else if d.acceptableResidualHarmClaimed then .rejectAcceptableResidualHarmClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusResilienceExercise

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity_and_coordination
    (d : ResilienceDossier) (h : DossierReady d = true) :
    IdentityComplete d ∧ CoordinationComplete d := by
  exact ⟨(of_decide_eq_true h).1, (of_decide_eq_true h).2.1⟩
theorem readiness_requires_defense (d : ResilienceDossier) (h : DossierReady d = true) : DefenseComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_recovery (d : ResilienceDossier) (h : DossierReady d = true) : RecoveryComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_remedy (d : ResilienceDossier) (h : DossierReady d = true) : RemedyComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_adaptation (d : ResilienceDossier) (h : DossierReady d = true) : AdaptationComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.1
theorem readiness_requires_boundary (d : ResilienceDossier) (h : DossierReady d = true) : BoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_response_mandate_remains_expired_when_time_advances
    (d : ResilienceDossier) (later : Nat) (expired : d.expiresAt < d.currentTick)
    (advances : d.currentTick <= later) : Not (Current { d with currentTick := later }) := by
  intro current; unfold Current at current; change later <= d.expiresAt at current; omega
theorem uncovered_population_shortfall_persists_when_population_grows
    (covered required laterRequired : Nat) (short : covered < required)
    (grows : required <= laterRequired) : Not (laterRequired <= covered) := by omega
theorem unresolved_path_shortfall_persists_when_more_paths_are_discovered
    (closed known laterKnown : Nat) (short : closed < known)
    (grows : known <= laterKnown) : Not (laterKnown <= closed) := by omega

structure ReceiptScope where
  incidentId : Nat
  populationDigest : Nat
  jurisdictionId : Nat
  protocolVersion : Nat
deriving DecidableEq, Repr
def ReceiptUseAllowed (s : ReceiptScope) (incident population jurisdiction version : Nat) : Prop :=
  incident = s.incidentId ∧ population = s.populationDigest ∧
  jurisdiction = s.jurisdictionId ∧ version = s.protocolVersion
theorem incident_change_invalidates_resilience_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.incidentId)) :
    Not (ReceiptUseAllowed s v s.populationDigest s.jurisdictionId s.protocolVersion) := by intro x; exact h x.1
theorem population_change_invalidates_resilience_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.populationDigest)) :
    Not (ReceiptUseAllowed s s.incidentId v s.jurisdictionId s.protocolVersion) := by intro x; exact h x.2.1
theorem jurisdiction_change_invalidates_resilience_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.jurisdictionId)) :
    Not (ReceiptUseAllowed s s.incidentId s.populationDigest v s.protocolVersion) := by intro x; exact h x.2.2.1
theorem protocol_change_invalidates_resilience_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.protocolVersion)) :
    Not (ReceiptUseAllowed s s.incidentId s.populationDigest s.jurisdictionId v) := by intro x; exact h x.2.2.2

structure ProviderSignals where
  classifierPass : Bool
  takedownRecorded : Bool
  providerServiceRestored : Bool
deriving DecidableEq, Repr
structure PopulationCase where
  signals : ProviderSignals
  everyAffectedPathRecovered : Bool
deriving DecidableEq, Repr
def sharedProviderSignals : ProviderSignals := { classifierPass := true, takedownRecorded := true, providerServiceRestored := true }
def recoveredPopulationCase : PopulationCase := { signals := sharedProviderSignals, everyAffectedPathRecovered := true }
def strandedPopulationCase : PopulationCase := { signals := sharedProviderSignals, everyAffectedPathRecovered := false }
def PopulationResilient (c : PopulationCase) : Bool := c.everyAffectedPathRecovered
theorem identical_provider_signals_can_hide_opposite_population_resilience :
    recoveredPopulationCase.signals = strandedPopulationCase.signals ∧
    PopulationResilient recoveredPopulationCase = true ∧
    PopulationResilient strandedPopulationCase = false := by decide
theorem provider_signals_cannot_recover_population_resilience (classify : ProviderSignals -> Bool) :
    Not (forall c : PopulationCase, classify c.signals = PopulationResilient c) := by
  intro exact; have a := exact recoveredPopulationCase; have b := exact strandedPopulationCase
  simp [recoveredPopulationCase, strandedPopulationCase, sharedProviderSignals, PopulationResilient] at a b
  rw [a] at b; contradiction

structure ResponseSignals where
  acknowledgedWithinTarget : Bool
  containedWithinTarget : Bool
  tabletopCompleted : Bool
deriving DecidableEq, Repr
structure RemedyCase where
  signals : ResponseSignals
  falseInterventionsRemedied : Bool
deriving DecidableEq, Repr
def sharedResponseSignals : ResponseSignals := { acknowledgedWithinTarget := true, containedWithinTarget := true, tabletopCompleted := true }
def equitableRemedyCase : RemedyCase := { signals := sharedResponseSignals, falseInterventionsRemedied := true }
def burdenShiftCase : RemedyCase := { signals := sharedResponseSignals, falseInterventionsRemedied := false }
def LawfulEquitableRemedy (c : RemedyCase) : Bool := c.falseInterventionsRemedied
theorem identical_response_speed_can_hide_opposite_equitable_remedy :
    equitableRemedyCase.signals = burdenShiftCase.signals ∧
    LawfulEquitableRemedy equitableRemedyCase = true ∧
    LawfulEquitableRemedy burdenShiftCase = false := by decide
theorem response_speed_cannot_recover_lawful_equitable_remedy (classify : ResponseSignals -> Bool) :
    Not (forall c : RemedyCase, classify c.signals = LawfulEquitableRemedy c) := by
  intro exact; have a := exact equitableRemedyCase; have b := exact burdenShiftCase
  simp [equitableRemedyCase, burdenShiftCase, sharedResponseSignals, LawfulEquitableRemedy] at a b
  rw [a] at b; contradiction

def toInstitutionalDossier
    (d : ResilienceDossier) : InstitutionalLegitimacyReview.InstitutionalDossier :=
  { affectedPublicCensusComplete := d.participantCensusComplete }

theorem missing_participant_forces_institutional_review
    (d : ResilienceDossier) (missing : d.participantCensusComplete = false) :
    InstitutionalLegitimacyReview.DossierReady (toInstitutionalDossier d) = false := by
  cases ready : InstitutionalLegitimacyReview.DossierReady (toInstitutionalDossier d) with
  | false => rfl
  | true =>
      have publicComplete := InstitutionalLegitimacyReview.readiness_requires_publics _ ready
      have census : (toInstitutionalDossier d).affectedPublicCensusComplete = true := publicComplete.1
      simp [toInstitutionalDossier, missing] at census

end AsiStackProofs.SocietalResilienceReview

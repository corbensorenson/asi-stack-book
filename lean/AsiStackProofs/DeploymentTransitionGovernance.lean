import AsiStackProofs.EvidenceStates
import AsiStackProofs.HumanAIOrganizations
import AsiStackProofs.ReadinessGates

namespace AsiStackProofs.DeploymentTransitionGovernance

/-!
A bounded model of authored AI deployment-transition records. The model proves
population and burden custody, staged review invariants, exact repair routing,
scope invalidation, information-loss countermodels, and rejecting consumer
interfaces. It does not prove deployment effectiveness, causal attribution,
welfare, fairness, meaningful agency, lawful remedy, service continuity,
support, release, or external effect.
-/

inductive TransitionSignal where
  | exposureEstimated | adoptionObserved | productivityIncreased
  | approvalClicked | aggregateGainReported
deriving DecidableEq, Repr

inductive TransitionInference where
  | insufficient | boundedObservation | eligibleForGovernedStudy
deriving DecidableEq, Repr

def InferenceFromSingleSignal (_ : TransitionSignal) : TransitionInference := .insufficient

theorem exposure_does_not_establish_displacement :
    InferenceFromSingleSignal .exposureEstimated = .insufficient := rfl
theorem adoption_does_not_establish_welfare :
    InferenceFromSingleSignal .adoptionObserved = .insufficient := rfl
theorem productivity_does_not_establish_distributional_benefit :
    InferenceFromSingleSignal .productivityIncreased = .insufficient := rfl
theorem approval_click_does_not_establish_agency :
    InferenceFromSingleSignal .approvalClicked = .insufficient := rfl
theorem aggregate_gain_does_not_establish_successful_transition :
    InferenceFromSingleSignal .aggregateGainReported = .insufficient := rfl

structure CohortOutcome where
  cohortId : Nat
  gain : Nat
  burden : Nat
  remedyDelivered : Nat
  includedInDenominator : Bool
deriving DecidableEq, Repr

def cohortIds : List CohortOutcome -> List Nat
  | [] => []
  | cohort :: tail => cohort.cohortId :: cohortIds tail

theorem cohort_id_collection_append_composes (before after : List CohortOutcome) :
    cohortIds (before ++ after) = cohortIds before ++ cohortIds after := by
  induction before with
  | nil => rfl
  | cons head tail ih => simp [cohortIds, ih]

theorem every_cohort_id_survives_collection
    (cohorts : List CohortOutcome) (cohort : CohortOutcome)
    (member : cohort ∈ cohorts) : cohort.cohortId ∈ cohortIds cohorts := by
  induction cohorts with
  | nil => simp at member
  | cons head tail ih =>
      simp only [List.mem_cons] at member ⊢
      cases member with
      | inl same => subst head; simp [cohortIds]
      | inr rest => right; exact ih rest

def CompleteAffectedDenominator
    (expectedIds : List Nat) (cohorts : List CohortOutcome) : Prop :=
  forall cohortId, cohortId ∈ expectedIds ->
    exists cohort, cohort ∈ cohorts ∧ cohort.cohortId = cohortId ∧
      cohort.includedInDenominator = true

theorem complete_denominator_covers_every_expected_cohort
    (expectedIds : List Nat) (cohorts : List CohortOutcome)
    (complete : CompleteAffectedDenominator expectedIds cohorts)
    (cohortId : Nat) (expected : cohortId ∈ expectedIds) :
    exists cohort, cohort ∈ cohorts ∧ cohort.cohortId = cohortId ∧
      cohort.includedInDenominator = true := complete cohortId expected

theorem omitted_expected_cohort_rejects_complete_denominator
    (expectedIds : List Nat) (cohorts : List CohortOutcome) (cohortId : Nat)
    (expected : cohortId ∈ expectedIds)
    (missing : forall cohort, cohort ∈ cohorts -> cohort.cohortId = cohortId ->
      cohort.includedInDenominator = false) :
    Not (CompleteAffectedDenominator expectedIds cohorts) := by
  intro complete
  obtain ⟨cohort, member, same, included⟩ := complete cohortId expected
  have omitted := missing cohort member same
  simp [omitted] at included

def FullyRemedied (cohorts : List CohortOutcome) : Prop :=
  forall cohort, cohort ∈ cohorts -> cohort.burden ≤ cohort.remedyDelivered

theorem fully_remedied_append_iff (before after : List CohortOutcome) :
    FullyRemedied (before ++ after) ↔ FullyRemedied before ∧ FullyRemedied after := by
  constructor
  · intro complete
    constructor
    · intro cohort member
      exact complete cohort (by simp [member])
    · intro cohort member
      exact complete cohort (by simp [member])
  · intro complete cohort member
    simp only [List.mem_append] at member
    cases member with
    | inl left => exact complete.1 cohort left
    | inr right => exact complete.2 cohort right

theorem unremedied_member_blocks_transition_acceptance
    (cohorts : List CohortOutcome) (cohort : CohortOutcome)
    (member : cohort ∈ cohorts) (gap : cohort.remedyDelivered < cohort.burden) :
    Not (FullyRemedied cohorts) := by
  intro complete
  exact (Nat.not_le_of_lt gap) (complete cohort member)

def totalGain : List CohortOutcome -> Nat
  | [] => 0
  | cohort :: tail => cohort.gain + totalGain tail

def totalBurden : List CohortOutcome -> Nat
  | [] => 0
  | cohort :: tail => cohort.burden + totalBurden tail

def ownerGain : CohortOutcome :=
  { cohortId := 1, gain := 100, burden := 0, remedyDelivered := 0,
    includedInDenominator := true }
def harmedWorker : CohortOutcome :=
  { cohortId := 2, gain := 0, burden := 10, remedyDelivered := 0,
    includedInDenominator := true }
def positiveAggregateWithUnremediedWorker : List CohortOutcome := [ownerGain, harmedWorker]

theorem positive_aggregate_can_coexist_with_unremedied_harm :
    totalBurden positiveAggregateWithUnremediedWorker <
      totalGain positiveAggregateWithUnremediedWorker ∧
    Not (FullyRemedied positiveAggregateWithUnremediedWorker) := by
  constructor
  · decide
  · apply unremedied_member_blocks_transition_acceptance _ harmedWorker
    · simp [positiveAggregateWithUnremediedWorker]
    · decide

structure TransitionDossier where
  deploymentIdentityBound : Bool := true
  baselineIdentityBound : Bool := true
  contractVersionBound : Bool := true
  authorityBound : Bool := true
  jurisdictionBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  baselineFrozen : Bool := true
  rolloutStagesBound : Bool := true
  observationScheduleBound : Bool := true
  affectedDenominatorComplete : Bool := true
  workerDenominatorComplete : Bool := true
  customerDenominatorComplete : Bool := true
  communityDenominatorComplete : Bool := true
  attritionPreserved : Bool := true
  excludedEntrantsPreserved : Bool := true
  taskChangeSeparated : Bool := true
  roleChangeSeparated : Bool := true
  skillChangeSeparated : Bool := true
  workloadSeparated : Bool := true
  compensationSeparated : Bool := true
  ownershipReturnsSeparated : Bool := true
  accessSeparated : Bool := true
  pricesSeparated : Bool := true
  concentrationSeparated : Bool := true
  serviceContinuityBound : Bool := true
  hiddenLaborPreserved : Bool := true
  humanDecisionRightsBound : Bool := true
  practicalRefusalPresent : Bool := true
  contestabilityPresent : Bool := true
  appealPresent : Bool := true
  humanAuthorityPresent : Bool := true
  portabilityRehearsed : Bool := true
  exitRehearsed : Bool := true
  trainingFunded : Bool := true
  redeploymentFunded : Bool := true
  incomeContinuityFunded : Bool := true
  burdenCompensationFunded : Bool := true
  alternativeServicePreserved : Bool := true
  ordinaryImprovementComparator : Bool := true
  transitionCapacityPresent : Bool := true
  delayedFollowupBound : Bool := true
  independentMonitoringBound : Bool := true
  subgroupReportingBound : Bool := true
  remedyTriggerBound : Bool := true
  remedyFundingBound : Bool := true
  remedyReceiptRequired : Bool := true
  pauseAuthorityPresent : Bool := true
  withdrawalPathPresent : Bool := true
  residualOwnerBound : Bool := true
  effectivenessClaimed : Bool := false
  welfareClaimed : Bool := false
  fairnessClaimed : Bool := false
  agencyClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : TransitionDossier) : Prop := d.currentTick ≤ d.expiresAt
instance currentDecidable (d : TransitionDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : TransitionDossier) : Prop :=
  d.deploymentIdentityBound = true ∧ d.baselineIdentityBound = true ∧
  d.contractVersionBound = true ∧ d.authorityBound = true ∧
  d.jurisdictionBound = true ∧ Current d

def DesignComplete (d : TransitionDossier) : Prop :=
  d.baselineFrozen = true ∧ d.rolloutStagesBound = true ∧
  d.observationScheduleBound = true ∧ d.affectedDenominatorComplete = true ∧
  d.workerDenominatorComplete = true ∧ d.customerDenominatorComplete = true ∧
  d.communityDenominatorComplete = true ∧ d.attritionPreserved = true ∧
  d.excludedEntrantsPreserved = true

def AccountingComplete (d : TransitionDossier) : Prop :=
  d.taskChangeSeparated = true ∧ d.roleChangeSeparated = true ∧
  d.skillChangeSeparated = true ∧ d.workloadSeparated = true ∧
  d.compensationSeparated = true ∧ d.ownershipReturnsSeparated = true ∧
  d.accessSeparated = true ∧ d.pricesSeparated = true ∧
  d.concentrationSeparated = true ∧ d.serviceContinuityBound = true ∧
  d.hiddenLaborPreserved = true

def AgencyComplete (d : TransitionDossier) : Prop :=
  d.humanDecisionRightsBound = true ∧ d.practicalRefusalPresent = true ∧
  d.contestabilityPresent = true ∧ d.appealPresent = true ∧
  d.humanAuthorityPresent = true ∧ d.portabilityRehearsed = true ∧
  d.exitRehearsed = true

def CapacityComplete (d : TransitionDossier) : Prop :=
  d.trainingFunded = true ∧ d.redeploymentFunded = true ∧
  d.incomeContinuityFunded = true ∧ d.burdenCompensationFunded = true ∧
  d.alternativeServicePreserved = true ∧ d.ordinaryImprovementComparator = true ∧
  d.transitionCapacityPresent = true

def RemedyComplete (d : TransitionDossier) : Prop :=
  d.delayedFollowupBound = true ∧ d.independentMonitoringBound = true ∧
  d.subgroupReportingBound = true ∧ d.remedyTriggerBound = true ∧
  d.remedyFundingBound = true ∧ d.remedyReceiptRequired = true ∧
  d.pauseAuthorityPresent = true ∧ d.withdrawalPathPresent = true ∧
  d.residualOwnerBound = true

def BoundaryComplete (d : TransitionDossier) : Prop :=
  d.effectivenessClaimed = false ∧ d.welfareClaimed = false ∧
  d.fairnessClaimed = false ∧ d.agencyClaimed = false ∧
  d.supportOrReleaseRequested = false

instance identityDecidable (d : TransitionDossier) : Decidable (IdentityComplete d) := by
  unfold IdentityComplete Current; infer_instance
instance designDecidable (d : TransitionDossier) : Decidable (DesignComplete d) := by
  unfold DesignComplete; infer_instance
instance accountingDecidable (d : TransitionDossier) : Decidable (AccountingComplete d) := by
  unfold AccountingComplete; infer_instance
instance agencyDecidable (d : TransitionDossier) : Decidable (AgencyComplete d) := by
  unfold AgencyComplete; infer_instance
instance capacityDecidable (d : TransitionDossier) : Decidable (CapacityComplete d) := by
  unfold CapacityComplete; infer_instance
instance remedyDecidable (d : TransitionDossier) : Decidable (RemedyComplete d) := by
  unfold RemedyComplete; infer_instance
instance boundaryDecidable (d : TransitionDossier) : Decidable (BoundaryComplete d) := by
  unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : TransitionDossier) : Prop :=
  IdentityComplete d ∧ DesignComplete d ∧ AccountingComplete d ∧
  AgencyComplete d ∧ CapacityComplete d ∧ RemedyComplete d ∧ BoundaryComplete d
instance admissibleDecidable (d : TransitionDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete Current DesignComplete AccountingComplete
    AgencyComplete CapacityComplete RemedyComplete BoundaryComplete
  infer_instance
def DossierReady (d : TransitionDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | designReviewed | accountingReviewed
  | agencyReviewed | capacityReviewed | remedyReviewed | boundaryReviewed
  | repairRequired | eligibleForTheseusGovernedTransitionStudy
deriving DecidableEq, Repr

def ReviewStepFor (d : TransitionDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (DesignComplete d) then .designReviewed else .repairRequired
  | .designReviewed => if decide (AccountingComplete d) then .accountingReviewed else .repairRequired
  | .accountingReviewed => if decide (AgencyComplete d) then .agencyReviewed else .repairRequired
  | .agencyReviewed => if decide (CapacityComplete d) then .capacityReviewed else .repairRequired
  | .capacityReviewed => if decide (RemedyComplete d) then .remedyReviewed else .repairRequired
  | .remedyReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusGovernedTransitionStudy
  | state => state

def ReviewRun (d : TransitionDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : TransitionDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .designReviewed => IdentityComplete d ∧ DesignComplete d
  | .accountingReviewed =>
      IdentityComplete d ∧ DesignComplete d ∧ AccountingComplete d
  | .agencyReviewed =>
      IdentityComplete d ∧ DesignComplete d ∧ AccountingComplete d ∧ AgencyComplete d
  | .capacityReviewed =>
      IdentityComplete d ∧ DesignComplete d ∧ AccountingComplete d ∧
        AgencyComplete d ∧ CapacityComplete d
  | .remedyReviewed =>
      IdentityComplete d ∧ DesignComplete d ∧ AccountingComplete d ∧
        AgencyComplete d ∧ CapacityComplete d ∧ RemedyComplete d
  | .boundaryReviewed | .eligibleForTheseusGovernedTransitionStudy => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : TransitionDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case designReviewed => split <;> simp_all [StageInvariant]
  case accountingReviewed => split <;> simp_all [StageInvariant]
  case agencyReviewed => split <;> simp_all [StageInvariant]
  case capacityReviewed => split <;> simp_all [StageInvariant]
  case remedyReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : TransitionDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem study_eligibility_requires_admissible_dossier
    (d : TransitionDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusGovernedTransitionStudy) :
    DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : TransitionDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_theseus_governed_transition_study :
    ReviewRun completeDossier 8 = .eligibleForTheseusGovernedTransitionStudy := by decide

inductive AdmissionAxis where
  | deploymentIdentity | baselineIdentity | contractVersion | authority | jurisdiction | expiry
  | baselineFrozen | rolloutStages | observationSchedule | affectedDenominator
  | workerDenominator | customerDenominator | communityDenominator | attrition
  | excludedEntrants | taskChange | roleChange | skillChange | workload | compensation
  | ownershipReturns | access | prices | concentration | serviceContinuity | hiddenLabor
  | humanDecisionRights | practicalRefusal | contestability | appeal | humanAuthority
  | portability | exit | training | redeployment | incomeContinuity | burdenCompensation
  | alternativeService | ordinaryComparator | transitionCapacity | delayedFollowup
  | independentMonitoring | subgroupReporting | remedyTrigger | remedyFunding | remedyReceipt
  | pauseAuthority | withdrawalPath | residualOwner | effectivenessClaim | welfareClaim
  | fairnessClaim | agencyClaim | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> TransitionDossier
  | .deploymentIdentity => { completeDossier with deploymentIdentityBound := false }
  | .baselineIdentity => { completeDossier with baselineIdentityBound := false }
  | .contractVersion => { completeDossier with contractVersionBound := false }
  | .authority => { completeDossier with authorityBound := false }
  | .jurisdiction => { completeDossier with jurisdictionBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .baselineFrozen => { completeDossier with baselineFrozen := false }
  | .rolloutStages => { completeDossier with rolloutStagesBound := false }
  | .observationSchedule => { completeDossier with observationScheduleBound := false }
  | .affectedDenominator => { completeDossier with affectedDenominatorComplete := false }
  | .workerDenominator => { completeDossier with workerDenominatorComplete := false }
  | .customerDenominator => { completeDossier with customerDenominatorComplete := false }
  | .communityDenominator => { completeDossier with communityDenominatorComplete := false }
  | .attrition => { completeDossier with attritionPreserved := false }
  | .excludedEntrants => { completeDossier with excludedEntrantsPreserved := false }
  | .taskChange => { completeDossier with taskChangeSeparated := false }
  | .roleChange => { completeDossier with roleChangeSeparated := false }
  | .skillChange => { completeDossier with skillChangeSeparated := false }
  | .workload => { completeDossier with workloadSeparated := false }
  | .compensation => { completeDossier with compensationSeparated := false }
  | .ownershipReturns => { completeDossier with ownershipReturnsSeparated := false }
  | .access => { completeDossier with accessSeparated := false }
  | .prices => { completeDossier with pricesSeparated := false }
  | .concentration => { completeDossier with concentrationSeparated := false }
  | .serviceContinuity => { completeDossier with serviceContinuityBound := false }
  | .hiddenLabor => { completeDossier with hiddenLaborPreserved := false }
  | .humanDecisionRights => { completeDossier with humanDecisionRightsBound := false }
  | .practicalRefusal => { completeDossier with practicalRefusalPresent := false }
  | .contestability => { completeDossier with contestabilityPresent := false }
  | .appeal => { completeDossier with appealPresent := false }
  | .humanAuthority => { completeDossier with humanAuthorityPresent := false }
  | .portability => { completeDossier with portabilityRehearsed := false }
  | .exit => { completeDossier with exitRehearsed := false }
  | .training => { completeDossier with trainingFunded := false }
  | .redeployment => { completeDossier with redeploymentFunded := false }
  | .incomeContinuity => { completeDossier with incomeContinuityFunded := false }
  | .burdenCompensation => { completeDossier with burdenCompensationFunded := false }
  | .alternativeService => { completeDossier with alternativeServicePreserved := false }
  | .ordinaryComparator => { completeDossier with ordinaryImprovementComparator := false }
  | .transitionCapacity => { completeDossier with transitionCapacityPresent := false }
  | .delayedFollowup => { completeDossier with delayedFollowupBound := false }
  | .independentMonitoring => { completeDossier with independentMonitoringBound := false }
  | .subgroupReporting => { completeDossier with subgroupReportingBound := false }
  | .remedyTrigger => { completeDossier with remedyTriggerBound := false }
  | .remedyFunding => { completeDossier with remedyFundingBound := false }
  | .remedyReceipt => { completeDossier with remedyReceiptRequired := false }
  | .pauseAuthority => { completeDossier with pauseAuthorityPresent := false }
  | .withdrawalPath => { completeDossier with withdrawalPathPresent := false }
  | .residualOwner => { completeDossier with residualOwnerBound := false }
  | .effectivenessClaim => { completeDossier with effectivenessClaimed := true }
  | .welfareClaim => { completeDossier with welfareClaimed := true }
  | .fairnessClaim => { completeDossier with fairnessClaimed := true }
  | .agencyClaim => { completeDossier with agencyClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindDeploymentIdentity | bindBaselineIdentity | bindContractVersion | bindAuthority
  | bindJurisdiction | renewExpiry | freezeBaseline | bindRolloutStages
  | bindObservationSchedule | completeAffectedDenominator | completeWorkerDenominator
  | completeCustomerDenominator | completeCommunityDenominator | preserveAttrition
  | preserveExcludedEntrants | separateTaskChange | separateRoleChange | separateSkillChange
  | separateWorkload | separateCompensation | separateOwnershipReturns | separateAccess
  | separatePrices | separateConcentration | bindServiceContinuity | preserveHiddenLabor
  | bindHumanDecisionRights | restorePracticalRefusal | addContestability | addAppeal
  | bindHumanAuthority | rehearsePortability | rehearseExit | fundTraining | fundRedeployment
  | fundIncomeContinuity | fundBurdenCompensation | preserveAlternativeService
  | addOrdinaryComparator | addTransitionCapacity | bindDelayedFollowup
  | bindIndependentMonitoring | bindSubgroupReporting | bindRemedyTrigger | bindRemedyFunding
  | requireRemedyReceipt | addPauseAuthority | addWithdrawalPath | assignResidualOwner
  | rejectEffectivenessClaim | rejectWelfareClaim | rejectFairnessClaim | rejectAgencyClaim
  | refuseSupportOrRelease | eligibleForTheseusGovernedTransitionStudy
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .deploymentIdentity => .bindDeploymentIdentity | .baselineIdentity => .bindBaselineIdentity
  | .contractVersion => .bindContractVersion | .authority => .bindAuthority
  | .jurisdiction => .bindJurisdiction | .expiry => .renewExpiry
  | .baselineFrozen => .freezeBaseline | .rolloutStages => .bindRolloutStages
  | .observationSchedule => .bindObservationSchedule
  | .affectedDenominator => .completeAffectedDenominator
  | .workerDenominator => .completeWorkerDenominator
  | .customerDenominator => .completeCustomerDenominator
  | .communityDenominator => .completeCommunityDenominator
  | .attrition => .preserveAttrition | .excludedEntrants => .preserveExcludedEntrants
  | .taskChange => .separateTaskChange | .roleChange => .separateRoleChange
  | .skillChange => .separateSkillChange | .workload => .separateWorkload
  | .compensation => .separateCompensation | .ownershipReturns => .separateOwnershipReturns
  | .access => .separateAccess | .prices => .separatePrices
  | .concentration => .separateConcentration | .serviceContinuity => .bindServiceContinuity
  | .hiddenLabor => .preserveHiddenLabor | .humanDecisionRights => .bindHumanDecisionRights
  | .practicalRefusal => .restorePracticalRefusal | .contestability => .addContestability
  | .appeal => .addAppeal | .humanAuthority => .bindHumanAuthority
  | .portability => .rehearsePortability | .exit => .rehearseExit
  | .training => .fundTraining | .redeployment => .fundRedeployment
  | .incomeContinuity => .fundIncomeContinuity
  | .burdenCompensation => .fundBurdenCompensation
  | .alternativeService => .preserveAlternativeService
  | .ordinaryComparator => .addOrdinaryComparator | .transitionCapacity => .addTransitionCapacity
  | .delayedFollowup => .bindDelayedFollowup
  | .independentMonitoring => .bindIndependentMonitoring
  | .subgroupReporting => .bindSubgroupReporting | .remedyTrigger => .bindRemedyTrigger
  | .remedyFunding => .bindRemedyFunding | .remedyReceipt => .requireRemedyReceipt
  | .pauseAuthority => .addPauseAuthority | .withdrawalPath => .addWithdrawalPath
  | .residualOwner => .assignResidualOwner | .effectivenessClaim => .rejectEffectivenessClaim
  | .welfareClaim => .rejectWelfareClaim | .fairnessClaim => .rejectFairnessClaim
  | .agencyClaim => .rejectAgencyClaim | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : TransitionDossier) : RepairDisposition :=
  if !d.deploymentIdentityBound then .bindDeploymentIdentity
  else if !d.baselineIdentityBound then .bindBaselineIdentity
  else if !d.contractVersionBound then .bindContractVersion
  else if !d.authorityBound then .bindAuthority
  else if !d.jurisdictionBound then .bindJurisdiction
  else if !decide (Current d) then .renewExpiry
  else if !d.baselineFrozen then .freezeBaseline
  else if !d.rolloutStagesBound then .bindRolloutStages
  else if !d.observationScheduleBound then .bindObservationSchedule
  else if !d.affectedDenominatorComplete then .completeAffectedDenominator
  else if !d.workerDenominatorComplete then .completeWorkerDenominator
  else if !d.customerDenominatorComplete then .completeCustomerDenominator
  else if !d.communityDenominatorComplete then .completeCommunityDenominator
  else if !d.attritionPreserved then .preserveAttrition
  else if !d.excludedEntrantsPreserved then .preserveExcludedEntrants
  else if !d.taskChangeSeparated then .separateTaskChange
  else if !d.roleChangeSeparated then .separateRoleChange
  else if !d.skillChangeSeparated then .separateSkillChange
  else if !d.workloadSeparated then .separateWorkload
  else if !d.compensationSeparated then .separateCompensation
  else if !d.ownershipReturnsSeparated then .separateOwnershipReturns
  else if !d.accessSeparated then .separateAccess
  else if !d.pricesSeparated then .separatePrices
  else if !d.concentrationSeparated then .separateConcentration
  else if !d.serviceContinuityBound then .bindServiceContinuity
  else if !d.hiddenLaborPreserved then .preserveHiddenLabor
  else if !d.humanDecisionRightsBound then .bindHumanDecisionRights
  else if !d.practicalRefusalPresent then .restorePracticalRefusal
  else if !d.contestabilityPresent then .addContestability
  else if !d.appealPresent then .addAppeal
  else if !d.humanAuthorityPresent then .bindHumanAuthority
  else if !d.portabilityRehearsed then .rehearsePortability
  else if !d.exitRehearsed then .rehearseExit
  else if !d.trainingFunded then .fundTraining
  else if !d.redeploymentFunded then .fundRedeployment
  else if !d.incomeContinuityFunded then .fundIncomeContinuity
  else if !d.burdenCompensationFunded then .fundBurdenCompensation
  else if !d.alternativeServicePreserved then .preserveAlternativeService
  else if !d.ordinaryImprovementComparator then .addOrdinaryComparator
  else if !d.transitionCapacityPresent then .addTransitionCapacity
  else if !d.delayedFollowupBound then .bindDelayedFollowup
  else if !d.independentMonitoringBound then .bindIndependentMonitoring
  else if !d.subgroupReportingBound then .bindSubgroupReporting
  else if !d.remedyTriggerBound then .bindRemedyTrigger
  else if !d.remedyFundingBound then .bindRemedyFunding
  else if !d.remedyReceiptRequired then .requireRemedyReceipt
  else if !d.pauseAuthorityPresent then .addPauseAuthority
  else if !d.withdrawalPathPresent then .addWithdrawalPath
  else if !d.residualOwnerBound then .assignResidualOwner
  else if d.effectivenessClaimed then .rejectEffectivenessClaim
  else if d.welfareClaimed then .rejectWelfareClaim
  else if d.fairnessClaimed then .rejectFairnessClaim
  else if d.agencyClaimed then .rejectAgencyClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusGovernedTransitionStudy

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : TransitionDossier) (h : DossierReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_design (d : TransitionDossier) (h : DossierReady d = true) :
    DesignComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_accounting (d : TransitionDossier) (h : DossierReady d = true) :
    AccountingComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_agency (d : TransitionDossier) (h : DossierReady d = true) :
    AgencyComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_capacity (d : TransitionDossier) (h : DossierReady d = true) :
    CapacityComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_remedy (d : TransitionDossier) (h : DossierReady d = true) :
    RemedyComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.1
theorem readiness_requires_boundary (d : TransitionDossier) (h : DossierReady d = true) :
    BoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_transition_contract_remains_expired_when_time_advances
    (expiresAt now later : Nat) (expired : expiresAt < now) (advances : now ≤ later) :
    expiresAt < later := Nat.lt_of_lt_of_le expired advances

theorem affected_denominator_gap_persists_when_observed_count_falls
    (observed expected observedLater : Nat) (gap : observed < expected)
    (falls : observedLater ≤ observed) : observedLater < expected :=
  Nat.lt_of_le_of_lt falls gap

theorem remedy_gap_persists_when_delivered_amount_falls
    (delivered burden deliveredLater : Nat) (gap : delivered < burden)
    (falls : deliveredLater ≤ delivered) : deliveredLater < burden :=
  Nat.lt_of_le_of_lt falls gap

structure TransitionReceiptScope where
  deploymentId : Nat
  baselineId : Nat
  contractVersion : Nat
  denominatorId : Nat
  observationScheduleId : Nat
  remedyPlanId : Nat
  authorityId : Nat
deriving DecidableEq, Repr

def ReceiptApplies (receipt current : TransitionReceiptScope) : Prop := receipt = current

theorem deployment_change_invalidates_transition_receipt
    (r : TransitionReceiptScope) (changed : r.deploymentId ≠ d) :
    Not (ReceiptApplies r { r with deploymentId := d }) := by
  intro same; exact changed (congrArg TransitionReceiptScope.deploymentId same)
theorem baseline_change_invalidates_transition_receipt
    (r : TransitionReceiptScope) (changed : r.baselineId ≠ b) :
    Not (ReceiptApplies r { r with baselineId := b }) := by
  intro same; exact changed (congrArg TransitionReceiptScope.baselineId same)
theorem contract_version_change_invalidates_transition_receipt
    (r : TransitionReceiptScope) (changed : r.contractVersion ≠ v) :
    Not (ReceiptApplies r { r with contractVersion := v }) := by
  intro same; exact changed (congrArg TransitionReceiptScope.contractVersion same)
theorem denominator_change_invalidates_transition_receipt
    (r : TransitionReceiptScope) (changed : r.denominatorId ≠ p) :
    Not (ReceiptApplies r { r with denominatorId := p }) := by
  intro same; exact changed (congrArg TransitionReceiptScope.denominatorId same)
theorem observation_schedule_change_invalidates_transition_receipt
    (r : TransitionReceiptScope) (changed : r.observationScheduleId ≠ o) :
    Not (ReceiptApplies r { r with observationScheduleId := o }) := by
  intro same; exact changed (congrArg TransitionReceiptScope.observationScheduleId same)
theorem remedy_plan_change_invalidates_transition_receipt
    (r : TransitionReceiptScope) (changed : r.remedyPlanId ≠ m) :
    Not (ReceiptApplies r { r with remedyPlanId := m }) := by
  intro same; exact changed (congrArg TransitionReceiptScope.remedyPlanId same)
theorem authority_change_invalidates_transition_receipt
    (r : TransitionReceiptScope) (changed : r.authorityId ≠ a) :
    Not (ReceiptApplies r { r with authorityId := a }) := by
  intro same; exact changed (congrArg TransitionReceiptScope.authorityId same)

structure DistributionSignals where
  productivityBand : Nat
  aggregateGainBand : Nat
deriving DecidableEq, Repr
structure DistributionCase where
  signals : DistributionSignals
  unremediedHarmedCohort : Bool
deriving DecidableEq, Repr

def sameAggregateNoHarm : DistributionCase :=
  { signals := { productivityBand := 4, aggregateGainBand := 7 },
    unremediedHarmedCohort := false }
def sameAggregateHiddenHarm : DistributionCase :=
  { signals := { productivityBand := 4, aggregateGainBand := 7 },
    unremediedHarmedCohort := true }

theorem identical_aggregate_signals_can_hide_opposite_harm_status :
    sameAggregateNoHarm.signals = sameAggregateHiddenHarm.signals ∧
      sameAggregateNoHarm.unremediedHarmedCohort ≠
        sameAggregateHiddenHarm.unremediedHarmedCohort := by decide

theorem aggregate_signals_cannot_recover_harmed_cohort_status
    (classify : DistributionSignals -> Bool) :
    Not (forall c : DistributionCase,
      classify c.signals = c.unremediedHarmedCohort) := by
  intro exactClassifier
  have left := exactClassifier sameAggregateNoHarm
  have right := exactClassifier sameAggregateHiddenHarm
  simp [sameAggregateNoHarm, sameAggregateHiddenHarm] at left right
  rw [left] at right
  simp at right

structure AgencySignals where
  approvalClicks : Nat
  humanReviewCount : Nat
deriving DecidableEq, Repr
structure AgencyCase where
  signals : AgencySignals
  practicalRefusalUsable : Bool
deriving DecidableEq, Repr

def nominalApprovalWithExit : AgencyCase :=
  { signals := { approvalClicks := 12, humanReviewCount := 3 },
    practicalRefusalUsable := true }
def nominalApprovalUnderCoercion : AgencyCase :=
  { signals := { approvalClicks := 12, humanReviewCount := 3 },
    practicalRefusalUsable := false }

theorem identical_approval_counts_can_hide_opposite_practical_agency :
    nominalApprovalWithExit.signals = nominalApprovalUnderCoercion.signals ∧
      nominalApprovalWithExit.practicalRefusalUsable ≠
        nominalApprovalUnderCoercion.practicalRefusalUsable := by decide

theorem approval_counts_cannot_recover_practical_agency
    (classify : AgencySignals -> Bool) :
    Not (forall c : AgencyCase, classify c.signals = c.practicalRefusalUsable) := by
  intro exactClassifier
  have left := exactClassifier nominalApprovalWithExit
  have right := exactClassifier nominalApprovalUnderCoercion
  simp [nominalApprovalWithExit, nominalApprovalUnderCoercion] at left right
  rw [left] at right
  simp at right

def organizationWithoutTransitionRemedy : HumanAIOrganizations.AccountabilityAssignment :=
  { remedyPathPresent := false }

theorem missing_transition_remedy_blocks_accountability_consumer :
    HumanAIOrganizations.AccountabilityReviewRun organizationWithoutTransitionRemedy 5 =
      .repairRemedyPath := by decide

def readinessWithoutTransitionChecks : ReadinessGates.GateReview :=
  { allRequiredGatesPass := false, decision := .canary }

theorem missing_transition_checks_reject_readiness_consumer :
    Not (ReadinessGates.PromotionGateValid readinessWithoutTransitionChecks) := by
  apply ReadinessGates.promoted_decision_with_failed_required_gates_rejected
  · trivial
  · rfl

def evidenceWithoutTransitionStudy : EvidenceBundle :=
  { sourceNote := True, prototypeInspection := True, syntheticTestRun := True,
    empiricalTestRun := False, externalLiterature := True }

theorem missing_transition_study_blocks_empirical_support_promotion :
    Not (PromotionAllowed evidenceWithoutTransitionStudy
      SupportState.argument SupportState.empiricalTestBacked) := by
  apply missing_required_evidence_blocks_promotion
  simp [RequiredEvidence, evidenceWithoutTransitionStudy]

end AsiStackProofs.DeploymentTransitionGovernance

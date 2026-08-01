import AsiStackProofs.LearnedObjectiveIntegrity

namespace AsiStackProofs.ObjectiveLeaseGovernance

inductive RatifierRole where
  | humanPrincipal
  | boundedInstitution
  | optimizer
  | rewardModel
  | evaluator
deriving DecidableEq, Repr

def mayRatifyObjective : RatifierRole -> Bool
  | .humanPrincipal | .boundedInstitution => true
  | .optimizer | .rewardModel | .evaluator => false

theorem optimizer_cannot_self_ratify : mayRatifyObjective .optimizer = false := by rfl
theorem reward_model_cannot_ratify : mayRatifyObjective .rewardModel = false := by rfl
theorem evaluator_cannot_ratify : mayRatifyObjective .evaluator = false := by rfl

structure DescendantBinding where
  bindingId : Nat
  consumerId : Nat
  active : Bool
deriving DecidableEq, Repr

def retireBinding (binding : DescendantBinding) : DescendantBinding :=
  { binding with active := false }

def retireAll : List DescendantBinding -> List DescendantBinding
  | [] => []
  | binding :: rest => retireBinding binding :: retireAll rest

def AllRetired (bindings : List DescendantBinding) : Prop :=
  forall binding, binding ∈ bindings -> binding.active = false

theorem retire_all_closes_every_finite_binding (bindings : List DescendantBinding) :
    AllRetired (retireAll bindings) := by
  intro binding member
  induction bindings with
  | nil => simp [retireAll] at member
  | cons head tail ih =>
      simp only [retireAll, List.mem_cons] at member
      rcases member with same | inTail
      · subst binding
        simp [retireBinding]
      · exact ih inTail

structure ObjectiveDossier where
  purposeIdentityBound : Bool := true
  principalAuthorityBound : Bool := true
  affectedPartiesRecorded : Bool := true
  constitutionalCeilingsBound : Bool := true
  explicitNonGoalsRecorded : Bool := true
  amendmentProcedureBound : Bool := true
  optimizerSelfRatificationRequested : Bool := false
  targetIdentityBound : Bool := true
  targetVersion : Nat := 7
  expectedTargetVersion : Nat := 7
  proxiesTypedSeparately : Bool := true
  causalAssumptionsRecorded : Bool := true
  preferenceEvidenceTyped : Bool := true
  rewardRoleTyped : Bool := true
  evaluatorRoleTyped : Bool := true
  plannerRoleTyped : Bool := true
  predictedPreferenceAsAuthorityClaimed : Bool := false
  alternativesPreserved : Bool := true
  uncertaintyRecorded : Bool := true
  dissentPreserved : Bool := true
  unrepresentedPartiesRecorded : Bool := true
  rightsCeilingsPreserved : Bool := true
  aggregationRuleVersioned : Bool := true
  clarificationOrAbstentionRoute : Bool := true
  consumerId : Nat := 41
  authorizedConsumerId : Nat := 41
  ontologyVersion : Nat := 12
  authorizedOntologyVersion : Nat := 12
  authorityVersion : Nat := 5
  authorizedAuthorityVersion : Nat := 5
  populationVersion : Nat := 3
  authorizedPopulationVersion : Nat := 3
  currentTick : Nat := 10
  expiresAt : Nat := 20
  reauthorizationRoutePresent : Bool := true
  interruptionRoutePresent : Bool := true
  rollbackRoutePresent : Bool := true
  proxyInterventionTested : Bool := true
  distributionShiftTested : Bool := true
  evaluatorSwapTested : Bool := true
  rewardTamperingTested : Bool := true
  capableWrongGoalControlPresent : Bool := true
  independentTargetObservationPresent : Bool := true
  ontologyMigrationTested : Bool := true
  descendantIndexComplete : Bool := true
  descendants : List DescendantBinding := [
    { bindingId := 1, consumerId := 41, active := true },
    { bindingId := 2, consumerId := 42, active := true },
    { bindingId := 3, consumerId := 43, active := true }
  ]
  unreachableResidualsRecorded : Bool := true
  residualOwnerPresent : Bool := true
  targetCorrectnessClaimed : Bool := false
  moralTruthClaimed : Bool := false
  stableAlignmentClaimed : Bool := false
  safeOptimizationClaimed : Bool := false
  supportPromotionRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : ObjectiveDossier) : Prop := d.currentTick <= d.expiresAt
def ConsumerBound (d : ObjectiveDossier) : Prop := d.consumerId = d.authorizedConsumerId
def VersionsCurrent (d : ObjectiveDossier) : Prop :=
  d.targetVersion = d.expectedTargetVersion ∧
  d.ontologyVersion = d.authorizedOntologyVersion ∧
  d.authorityVersion = d.authorizedAuthorityVersion ∧
  d.populationVersion = d.authorizedPopulationVersion

instance currentDecidable (d : ObjectiveDossier) : Decidable (Current d) := by
  unfold Current; infer_instance
instance consumerBoundDecidable (d : ObjectiveDossier) : Decidable (ConsumerBound d) := by
  unfold ConsumerBound; infer_instance
instance versionsCurrentDecidable (d : ObjectiveDossier) : Decidable (VersionsCurrent d) := by
  unfold VersionsCurrent; infer_instance

def CharterComplete (d : ObjectiveDossier) : Prop :=
  d.purposeIdentityBound = true ∧ d.principalAuthorityBound = true ∧
  d.affectedPartiesRecorded = true ∧ d.constitutionalCeilingsBound = true ∧
  d.explicitNonGoalsRecorded = true ∧ d.amendmentProcedureBound = true ∧
  d.optimizerSelfRatificationRequested = false

def TargetProxyComplete (d : ObjectiveDossier) : Prop :=
  d.targetIdentityBound = true ∧ d.proxiesTypedSeparately = true ∧
  d.causalAssumptionsRecorded = true ∧ d.preferenceEvidenceTyped = true ∧
  d.rewardRoleTyped = true ∧ d.evaluatorRoleTyped = true ∧ d.plannerRoleTyped = true ∧
  d.predictedPreferenceAsAuthorityClaimed = false

def PluralityComplete (d : ObjectiveDossier) : Prop :=
  d.alternativesPreserved = true ∧ d.uncertaintyRecorded = true ∧
  d.dissentPreserved = true ∧ d.unrepresentedPartiesRecorded = true ∧
  d.rightsCeilingsPreserved = true ∧ d.aggregationRuleVersioned = true ∧
  d.clarificationOrAbstentionRoute = true

def LeaseComplete (d : ObjectiveDossier) : Prop :=
  ConsumerBound d ∧ VersionsCurrent d ∧ Current d ∧
  d.reauthorizationRoutePresent = true ∧ d.interruptionRoutePresent = true ∧
  d.rollbackRoutePresent = true

def ChallengeComplete (d : ObjectiveDossier) : Prop :=
  d.proxyInterventionTested = true ∧ d.distributionShiftTested = true ∧
  d.evaluatorSwapTested = true ∧ d.rewardTamperingTested = true ∧
  d.capableWrongGoalControlPresent = true ∧
  d.independentTargetObservationPresent = true ∧ d.ontologyMigrationTested = true

def RetirementBoundaryComplete (d : ObjectiveDossier) : Prop :=
  d.descendantIndexComplete = true ∧ d.unreachableResidualsRecorded = true ∧
  d.residualOwnerPresent = true ∧ d.targetCorrectnessClaimed = false ∧
  d.moralTruthClaimed = false ∧ d.stableAlignmentClaimed = false ∧
  d.safeOptimizationClaimed = false ∧ d.supportPromotionRequested = false

instance charterCompleteDecidable (d : ObjectiveDossier) : Decidable (CharterComplete d) := by
  unfold CharterComplete; infer_instance
instance targetProxyCompleteDecidable (d : ObjectiveDossier) : Decidable (TargetProxyComplete d) := by
  unfold TargetProxyComplete; infer_instance
instance pluralityCompleteDecidable (d : ObjectiveDossier) : Decidable (PluralityComplete d) := by
  unfold PluralityComplete; infer_instance
instance leaseCompleteDecidable (d : ObjectiveDossier) : Decidable (LeaseComplete d) := by
  unfold LeaseComplete ConsumerBound VersionsCurrent Current; infer_instance
instance challengeCompleteDecidable (d : ObjectiveDossier) : Decidable (ChallengeComplete d) := by
  unfold ChallengeComplete; infer_instance
instance retirementBoundaryCompleteDecidable (d : ObjectiveDossier) : Decidable (RetirementBoundaryComplete d) := by
  unfold RetirementBoundaryComplete; infer_instance

def DossierAdmissible (d : ObjectiveDossier) : Prop :=
  CharterComplete d ∧ TargetProxyComplete d ∧ PluralityComplete d ∧ LeaseComplete d ∧
  ChallengeComplete d ∧ RetirementBoundaryComplete d

instance dossierAdmissibleDecidable (d : ObjectiveDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible CharterComplete TargetProxyComplete PluralityComplete LeaseComplete
    ConsumerBound VersionsCurrent Current ChallengeComplete RetirementBoundaryComplete
  infer_instance

def DossierReady (d : ObjectiveDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed
  | charterReviewed
  | targetProxyReviewed
  | pluralityReviewed
  | leaseReviewed
  | challengeReviewed
  | boundaryReviewed
  | repairRequired
  | eligibleForTheseusObjectiveRegistryStudy
deriving DecidableEq, Repr

def ReviewStepFor (d : ObjectiveDossier) : ReviewState -> ReviewState
  | .proposed => if decide (CharterComplete d) then .charterReviewed else .repairRequired
  | .charterReviewed =>
      if decide (TargetProxyComplete d) then .targetProxyReviewed else .repairRequired
  | .targetProxyReviewed =>
      if decide (PluralityComplete d) then .pluralityReviewed else .repairRequired
  | .pluralityReviewed => if decide (LeaseComplete d) then .leaseReviewed else .repairRequired
  | .leaseReviewed =>
      if decide (ChallengeComplete d) then .challengeReviewed else .repairRequired
  | .challengeReviewed =>
      if decide (RetirementBoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusObjectiveRegistryStudy
  | state => state

def ReviewRun (d : ObjectiveDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : ObjectiveDossier) : ReviewState -> Prop
  | .proposed => True
  | .charterReviewed => CharterComplete d
  | .targetProxyReviewed => CharterComplete d ∧ TargetProxyComplete d
  | .pluralityReviewed => CharterComplete d ∧ TargetProxyComplete d ∧ PluralityComplete d
  | .leaseReviewed =>
      CharterComplete d ∧ TargetProxyComplete d ∧ PluralityComplete d ∧ LeaseComplete d
  | .challengeReviewed =>
      CharterComplete d ∧ TargetProxyComplete d ∧ PluralityComplete d ∧ LeaseComplete d ∧
      ChallengeComplete d
  | .boundaryReviewed | .eligibleForTheseusObjectiveRegistryStudy => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant (d : ObjectiveDossier) (state : ReviewState)
    (h : StageInvariant d state) : StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case charterReviewed => split <;> simp_all [StageInvariant]
  case targetProxyReviewed => split <;> simp_all [StageInvariant]
  case pluralityReviewed => split <;> simp_all [StageInvariant]
  case leaseReviewed => split <;> simp_all [StageInvariant]
  case challengeReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : ObjectiveDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem study_eligibility_requires_admissible_dossier (d : ObjectiveDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusObjectiveRegistryStudy) : DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : ObjectiveDossier := {}

theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_objective_registry_study :
    ReviewRun completeDossier 7 = .eligibleForTheseusObjectiveRegistryStudy := by decide

inductive AdmissionAxis where
  | purposeIdentity | principalAuthority | affectedParties | constitutionalCeilings
  | explicitNonGoals | amendmentProcedure | optimizerSelfRatification | targetIdentity
  | targetVersion | proxySeparation | causalAssumptions | preferenceEvidenceTyping
  | rewardRoleTyping | evaluatorRoleTyping | plannerRoleTyping | preferenceAsAuthority
  | alternatives | uncertainty | dissent | unrepresentedParties | rightsCeilings
  | aggregationRule | clarificationOrAbstention | consumerScope | ontologyVersion
  | authorityVersion | populationVersion | expiry | reauthorizationRoute | interruptionRoute
  | rollbackRoute | proxyIntervention | distributionShift | evaluatorSwap | rewardTampering
  | capableWrongGoalControl | independentTargetObservation | ontologyMigration
  | descendantIndex | unreachableResiduals | residualOwner | targetCorrectness
  | moralTruth | stableAlignment | safeOptimization | supportPromotion
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> ObjectiveDossier
  | .purposeIdentity => { completeDossier with purposeIdentityBound := false }
  | .principalAuthority => { completeDossier with principalAuthorityBound := false }
  | .affectedParties => { completeDossier with affectedPartiesRecorded := false }
  | .constitutionalCeilings => { completeDossier with constitutionalCeilingsBound := false }
  | .explicitNonGoals => { completeDossier with explicitNonGoalsRecorded := false }
  | .amendmentProcedure => { completeDossier with amendmentProcedureBound := false }
  | .optimizerSelfRatification => { completeDossier with optimizerSelfRatificationRequested := true }
  | .targetIdentity => { completeDossier with targetIdentityBound := false }
  | .targetVersion => { completeDossier with targetVersion := 8 }
  | .proxySeparation => { completeDossier with proxiesTypedSeparately := false }
  | .causalAssumptions => { completeDossier with causalAssumptionsRecorded := false }
  | .preferenceEvidenceTyping => { completeDossier with preferenceEvidenceTyped := false }
  | .rewardRoleTyping => { completeDossier with rewardRoleTyped := false }
  | .evaluatorRoleTyping => { completeDossier with evaluatorRoleTyped := false }
  | .plannerRoleTyping => { completeDossier with plannerRoleTyped := false }
  | .preferenceAsAuthority => { completeDossier with predictedPreferenceAsAuthorityClaimed := true }
  | .alternatives => { completeDossier with alternativesPreserved := false }
  | .uncertainty => { completeDossier with uncertaintyRecorded := false }
  | .dissent => { completeDossier with dissentPreserved := false }
  | .unrepresentedParties => { completeDossier with unrepresentedPartiesRecorded := false }
  | .rightsCeilings => { completeDossier with rightsCeilingsPreserved := false }
  | .aggregationRule => { completeDossier with aggregationRuleVersioned := false }
  | .clarificationOrAbstention => { completeDossier with clarificationOrAbstentionRoute := false }
  | .consumerScope => { completeDossier with consumerId := 42 }
  | .ontologyVersion => { completeDossier with ontologyVersion := 13 }
  | .authorityVersion => { completeDossier with authorityVersion := 6 }
  | .populationVersion => { completeDossier with populationVersion := 4 }
  | .expiry => { completeDossier with currentTick := 21 }
  | .reauthorizationRoute => { completeDossier with reauthorizationRoutePresent := false }
  | .interruptionRoute => { completeDossier with interruptionRoutePresent := false }
  | .rollbackRoute => { completeDossier with rollbackRoutePresent := false }
  | .proxyIntervention => { completeDossier with proxyInterventionTested := false }
  | .distributionShift => { completeDossier with distributionShiftTested := false }
  | .evaluatorSwap => { completeDossier with evaluatorSwapTested := false }
  | .rewardTampering => { completeDossier with rewardTamperingTested := false }
  | .capableWrongGoalControl => { completeDossier with capableWrongGoalControlPresent := false }
  | .independentTargetObservation => { completeDossier with independentTargetObservationPresent := false }
  | .ontologyMigration => { completeDossier with ontologyMigrationTested := false }
  | .descendantIndex => { completeDossier with descendantIndexComplete := false }
  | .unreachableResiduals => { completeDossier with unreachableResidualsRecorded := false }
  | .residualOwner => { completeDossier with residualOwnerPresent := false }
  | .targetCorrectness => { completeDossier with targetCorrectnessClaimed := true }
  | .moralTruth => { completeDossier with moralTruthClaimed := true }
  | .stableAlignment => { completeDossier with stableAlignmentClaimed := true }
  | .safeOptimization => { completeDossier with safeOptimizationClaimed := true }
  | .supportPromotion => { completeDossier with supportPromotionRequested := true }

inductive RepairDisposition where
  | bindPurposeIdentity | bindPrincipalAuthority | recordAffectedParties
  | bindConstitutionalCeilings | recordExplicitNonGoals | bindAmendmentProcedure
  | refuseOptimizerSelfRatification | bindTargetIdentity | restoreTargetVersion
  | separateProxies | recordCausalAssumptions | typePreferenceEvidence | typeRewardRole
  | typeEvaluatorRole | typePlannerRole | rejectPreferenceAsAuthority | preserveAlternatives
  | recordUncertainty | preserveDissent | recordUnrepresentedParties | preserveRightsCeilings
  | versionAggregationRule | addClarificationOrAbstention | restoreConsumerScope
  | reauthorizeOntology | reauthorizeAuthority | reauthorizePopulation | renewExpiry
  | addReauthorizationRoute | addInterruptionRoute | addRollbackRoute | testProxyIntervention
  | testDistributionShift | testEvaluatorSwap | testRewardTampering
  | addCapableWrongGoalControl | addIndependentTargetObservation | testOntologyMigration
  | completeDescendantIndex | recordUnreachableResiduals | assignResidualOwner
  | rejectTargetCorrectness | rejectMoralTruth | rejectStableAlignment | rejectSafeOptimization
  | refuseSupportPromotion | eligibleForTheseusObjectiveRegistryStudy
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .purposeIdentity => .bindPurposeIdentity | .principalAuthority => .bindPrincipalAuthority
  | .affectedParties => .recordAffectedParties | .constitutionalCeilings => .bindConstitutionalCeilings
  | .explicitNonGoals => .recordExplicitNonGoals | .amendmentProcedure => .bindAmendmentProcedure
  | .optimizerSelfRatification => .refuseOptimizerSelfRatification | .targetIdentity => .bindTargetIdentity
  | .targetVersion => .restoreTargetVersion | .proxySeparation => .separateProxies
  | .causalAssumptions => .recordCausalAssumptions | .preferenceEvidenceTyping => .typePreferenceEvidence
  | .rewardRoleTyping => .typeRewardRole | .evaluatorRoleTyping => .typeEvaluatorRole
  | .plannerRoleTyping => .typePlannerRole | .preferenceAsAuthority => .rejectPreferenceAsAuthority
  | .alternatives => .preserveAlternatives | .uncertainty => .recordUncertainty
  | .dissent => .preserveDissent | .unrepresentedParties => .recordUnrepresentedParties
  | .rightsCeilings => .preserveRightsCeilings | .aggregationRule => .versionAggregationRule
  | .clarificationOrAbstention => .addClarificationOrAbstention | .consumerScope => .restoreConsumerScope
  | .ontologyVersion => .reauthorizeOntology | .authorityVersion => .reauthorizeAuthority
  | .populationVersion => .reauthorizePopulation | .expiry => .renewExpiry
  | .reauthorizationRoute => .addReauthorizationRoute | .interruptionRoute => .addInterruptionRoute
  | .rollbackRoute => .addRollbackRoute | .proxyIntervention => .testProxyIntervention
  | .distributionShift => .testDistributionShift | .evaluatorSwap => .testEvaluatorSwap
  | .rewardTampering => .testRewardTampering | .capableWrongGoalControl => .addCapableWrongGoalControl
  | .independentTargetObservation => .addIndependentTargetObservation
  | .ontologyMigration => .testOntologyMigration | .descendantIndex => .completeDescendantIndex
  | .unreachableResiduals => .recordUnreachableResiduals | .residualOwner => .assignResidualOwner
  | .targetCorrectness => .rejectTargetCorrectness | .moralTruth => .rejectMoralTruth
  | .stableAlignment => .rejectStableAlignment | .safeOptimization => .rejectSafeOptimization
  | .supportPromotion => .refuseSupportPromotion

def ExactRepairFor (d : ObjectiveDossier) : RepairDisposition :=
  if !d.purposeIdentityBound then .bindPurposeIdentity
  else if !d.principalAuthorityBound then .bindPrincipalAuthority
  else if !d.affectedPartiesRecorded then .recordAffectedParties
  else if !d.constitutionalCeilingsBound then .bindConstitutionalCeilings
  else if !d.explicitNonGoalsRecorded then .recordExplicitNonGoals
  else if !d.amendmentProcedureBound then .bindAmendmentProcedure
  else if d.optimizerSelfRatificationRequested then .refuseOptimizerSelfRatification
  else if !d.targetIdentityBound then .bindTargetIdentity
  else if d.targetVersion != d.expectedTargetVersion then .restoreTargetVersion
  else if !d.proxiesTypedSeparately then .separateProxies
  else if !d.causalAssumptionsRecorded then .recordCausalAssumptions
  else if !d.preferenceEvidenceTyped then .typePreferenceEvidence
  else if !d.rewardRoleTyped then .typeRewardRole
  else if !d.evaluatorRoleTyped then .typeEvaluatorRole
  else if !d.plannerRoleTyped then .typePlannerRole
  else if d.predictedPreferenceAsAuthorityClaimed then .rejectPreferenceAsAuthority
  else if !d.alternativesPreserved then .preserveAlternatives
  else if !d.uncertaintyRecorded then .recordUncertainty
  else if !d.dissentPreserved then .preserveDissent
  else if !d.unrepresentedPartiesRecorded then .recordUnrepresentedParties
  else if !d.rightsCeilingsPreserved then .preserveRightsCeilings
  else if !d.aggregationRuleVersioned then .versionAggregationRule
  else if !d.clarificationOrAbstentionRoute then .addClarificationOrAbstention
  else if d.consumerId != d.authorizedConsumerId then .restoreConsumerScope
  else if d.ontologyVersion != d.authorizedOntologyVersion then .reauthorizeOntology
  else if d.authorityVersion != d.authorizedAuthorityVersion then .reauthorizeAuthority
  else if d.populationVersion != d.authorizedPopulationVersion then .reauthorizePopulation
  else if !decide (Current d) then .renewExpiry
  else if !d.reauthorizationRoutePresent then .addReauthorizationRoute
  else if !d.interruptionRoutePresent then .addInterruptionRoute
  else if !d.rollbackRoutePresent then .addRollbackRoute
  else if !d.proxyInterventionTested then .testProxyIntervention
  else if !d.distributionShiftTested then .testDistributionShift
  else if !d.evaluatorSwapTested then .testEvaluatorSwap
  else if !d.rewardTamperingTested then .testRewardTampering
  else if !d.capableWrongGoalControlPresent then .addCapableWrongGoalControl
  else if !d.independentTargetObservationPresent then .addIndependentTargetObservation
  else if !d.ontologyMigrationTested then .testOntologyMigration
  else if !d.descendantIndexComplete then .completeDescendantIndex
  else if !d.unreachableResidualsRecorded then .recordUnreachableResiduals
  else if !d.residualOwnerPresent then .assignResidualOwner
  else if d.targetCorrectnessClaimed then .rejectTargetCorrectness
  else if d.moralTruthClaimed then .rejectMoralTruth
  else if d.stableAlignmentClaimed then .rejectStableAlignment
  else if d.safeOptimizationClaimed then .rejectSafeOptimization
  else if d.supportPromotionRequested then .refuseSupportPromotion
  else .eligibleForTheseusObjectiveRegistryStudy

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide

theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide

theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 7 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_charter (d : ObjectiveDossier) (h : DossierReady d = true) :
    CharterComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_target_proxy_separation (d : ObjectiveDossier)
    (h : DossierReady d = true) : TargetProxyComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_plurality (d : ObjectiveDossier) (h : DossierReady d = true) :
    PluralityComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_lease (d : ObjectiveDossier) (h : DossierReady d = true) :
    LeaseComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_challenge (d : ObjectiveDossier) (h : DossierReady d = true) :
    ChallengeComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_retirement_boundary (d : ObjectiveDossier)
    (h : DossierReady d = true) : RetirementBoundaryComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.2

theorem expired_lease_remains_expired_when_time_advances (d : ObjectiveDossier) (later : Nat)
    (expired : d.expiresAt < d.currentTick) (advances : d.currentTick <= later) :
    Not (Current { d with currentTick := later }) := by
  intro current
  unfold Current at current
  change later <= d.expiresAt at current
  omega

structure ObjectiveLease where
  consumerId : Nat
  targetVersion : Nat
  ontologyVersion : Nat
  authorityVersion : Nat
  populationVersion : Nat
  expiresAt : Nat
deriving DecidableEq, Repr

def issueLease (d : ObjectiveDossier) : ObjectiveLease :=
  { consumerId := d.authorizedConsumerId
    targetVersion := d.expectedTargetVersion
    ontologyVersion := d.authorizedOntologyVersion
    authorityVersion := d.authorizedAuthorityVersion
    populationVersion := d.authorizedPopulationVersion
    expiresAt := d.expiresAt }

def LeaseUseAllowed (lease : ObjectiveLease) (consumer target ontology authority population tick : Nat) : Prop :=
  consumer = lease.consumerId ∧ target = lease.targetVersion ∧
  ontology = lease.ontologyVersion ∧ authority = lease.authorityVersion ∧
  population = lease.populationVersion ∧ tick <= lease.expiresAt

theorem consumer_lease_is_nontransferable (lease : ObjectiveLease)
    (otherConsumer : Nat) (different : Not (otherConsumer = lease.consumerId)) :
    Not (LeaseUseAllowed lease otherConsumer lease.targetVersion lease.ontologyVersion
      lease.authorityVersion lease.populationVersion lease.expiresAt) := by
  intro allowed
  exact different allowed.1

theorem ontology_change_invalidates_use (lease : ObjectiveLease) (changedOntology : Nat)
    (different : Not (changedOntology = lease.ontologyVersion)) :
    Not (LeaseUseAllowed lease lease.consumerId lease.targetVersion changedOntology
      lease.authorityVersion lease.populationVersion lease.expiresAt) := by
  intro allowed
  exact different allowed.2.2.1

theorem authority_change_invalidates_use (lease : ObjectiveLease) (changedAuthority : Nat)
    (different : Not (changedAuthority = lease.authorityVersion)) :
    Not (LeaseUseAllowed lease lease.consumerId lease.targetVersion lease.ontologyVersion
      changedAuthority lease.populationVersion lease.expiresAt) := by
  intro allowed
  exact different allowed.2.2.2.1

structure ProxyObservation where
  proxyScore : Nat
  evaluatorVersion : Nat
deriving DecidableEq, Repr

structure TargetCase where
  observation : ProxyObservation
  targetImproved : Bool
deriving DecidableEq, Repr

def sharedProxyObservation : ProxyObservation := { proxyScore := 100, evaluatorVersion := 4 }
def alignedProxyCase : TargetCase := { observation := sharedProxyObservation, targetImproved := true }
def exploitedProxyCase : TargetCase := { observation := sharedProxyObservation, targetImproved := false }

theorem identical_proxy_observation_can_hide_opposite_target_movement :
    alignedProxyCase.observation = exploitedProxyCase.observation ∧
    alignedProxyCase.targetImproved = true ∧ exploitedProxyCase.targetImproved = false := by decide

theorem proxy_score_and_evaluator_cannot_recover_target_improvement
    (classify : ProxyObservation -> Bool) :
    Not (forall c : TargetCase, classify c.observation = c.targetImproved) := by
  intro exact
  have aligned := exact alignedProxyCase
  have exploited := exact exploitedProxyCase
  simp [alignedProxyCase, exploitedProxyCase, sharedProxyObservation] at aligned exploited
  rw [aligned] at exploited
  contradiction

structure PreferencePrediction where
  optionId : Nat
  predictedPreference : Nat
  confidence : Nat
deriving DecidableEq, Repr

structure AuthorityCase where
  prediction : PreferencePrediction
  authorized : Bool
deriving DecidableEq, Repr

def sharedPrediction : PreferencePrediction :=
  { optionId := 9, predictedPreference := 80, confidence := 90 }
def authorizedPreferenceCase : AuthorityCase := { prediction := sharedPrediction, authorized := true }
def unauthorizedPreferenceCase : AuthorityCase := { prediction := sharedPrediction, authorized := false }

theorem identical_preference_prediction_can_hide_opposite_authority :
    authorizedPreferenceCase.prediction = unauthorizedPreferenceCase.prediction ∧
    authorizedPreferenceCase.authorized = true ∧ unauthorizedPreferenceCase.authorized = false := by decide

theorem predicted_preference_cannot_recover_authority
    (classify : PreferencePrediction -> Bool) :
    Not (forall c : AuthorityCase, classify c.prediction = c.authorized) := by
  intro exact
  have authorized := exact authorizedPreferenceCase
  have unauthorized := exact unauthorizedPreferenceCase
  simp [authorizedPreferenceCase, unauthorizedPreferenceCase, sharedPrediction] at authorized unauthorized
  rw [authorized] at unauthorized
  contradiction

def toLearnedObjectivePacket (d : ObjectiveDossier) : LearnedObjectiveIntegrity.Packet :=
  { LearnedObjectiveIntegrity.canonicalPacket with
    outerTargetDigest := d.expectedTargetVersion
    outerTargetPresent := DossierReady d
    authorityBounded := DossierReady d
    expiryPresent := decide (Current d)
    rollbackPresent := d.rollbackRoutePresent
    descendantCustodyPresent := d.descendantIndexComplete
    residualOwnerPresent := d.residualOwnerPresent
    objectiveIdentityAsserted := false
    absenceOfDeceptionAsserted := false
    supportAssignmentRequested := false
    externalAuthorityRequested := false }

theorem ready_dossier_supplies_bounded_learned_objective_consumer_fields
    (d : ObjectiveDossier) (ready : DossierReady d = true) :
    let packet := toLearnedObjectivePacket d
    packet.outerTargetPresent = true ∧ packet.authorityBounded = true ∧
    packet.expiryPresent = true ∧ packet.rollbackPresent = true ∧
    packet.descendantCustodyPresent = true ∧ packet.residualOwnerPresent = true ∧
    packet.objectiveIdentityAsserted = false ∧ packet.absenceOfDeceptionAsserted = false ∧
    packet.supportAssignmentRequested = false ∧ packet.externalAuthorityRequested = false := by
  have lease := readiness_requires_lease d ready
  have boundary := readiness_requires_retirement_boundary d ready
  have current : Current d := lease.2.2.1
  have rollback : d.rollbackRoutePresent = true := lease.2.2.2.2.2
  have descendants : d.descendantIndexComplete = true := boundary.1
  have owner : d.residualOwnerPresent = true := boundary.2.2.1
  simp [toLearnedObjectivePacket, ready, current, rollback, descendants, owner]

end AsiStackProofs.ObjectiveLeaseGovernance

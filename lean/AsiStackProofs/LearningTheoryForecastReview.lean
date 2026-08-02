import AsiStackProofs.BenchmarkRatchets

namespace AsiStackProofs.LearningTheoryForecastReview

/-!
A bounded review model for learning-theory and scaling forecasts. The model
proves finite attempt custody, prospective forecast admission, scope expiry,
receipt invalidation, and information-loss boundaries over authored records.
It does not establish generalization, transfer, emergence, scaling accuracy,
calibration, safety, or deployment readiness.
-/

inductive EvidenceKind where
  | trainingFit | iidHoldout | retrospectiveScalingFit | compressionScore
  | thresholdBenchmark
deriving DecidableEq, Repr

inductive ClaimClass where
  | boundedTrainingFit | localHoldoutResult | fittedScalingRelation
  | codedDescriptionLength | thresholdMetricResult | broadGeneralization
  | distributionTransfer | mechanismEmergence | futureScalingBehavior | safety
deriving DecidableEq, Repr

def establishes : EvidenceKind -> ClaimClass -> Bool
  | .trainingFit, .boundedTrainingFit => true
  | .iidHoldout, .localHoldoutResult => true
  | .retrospectiveScalingFit, .fittedScalingRelation => true
  | .compressionScore, .codedDescriptionLength => true
  | .thresholdBenchmark, .thresholdMetricResult => true
  | _, _ => false

theorem training_fit_does_not_establish_broad_generalization :
    establishes .trainingFit .broadGeneralization = false := by rfl
theorem iid_holdout_does_not_establish_distribution_transfer :
    establishes .iidHoldout .distributionTransfer = false := by rfl
theorem retrospective_scaling_fit_does_not_establish_future_scaling_behavior :
    establishes .retrospectiveScalingFit .futureScalingBehavior = false := by rfl
theorem compression_score_does_not_establish_safety :
    establishes .compressionScore .safety = false := by rfl
theorem threshold_benchmark_does_not_establish_mechanism_emergence :
    establishes .thresholdBenchmark .mechanismEmergence = false := by rfl

structure AttemptRecord where
  attemptId : Nat
  includedInDenominator : Bool
deriving DecidableEq, Repr

def collectAttemptIds : List AttemptRecord -> List Nat
  | [] => []
  | attempt :: tail => attempt.attemptId :: collectAttemptIds tail

theorem attempt_id_collection_append_composes (before after : List AttemptRecord) :
    collectAttemptIds (before ++ after) = collectAttemptIds before ++ collectAttemptIds after := by
  induction before with
  | nil => rfl
  | cons head tail ih => simp [collectAttemptIds, ih]

theorem every_attempt_id_survives_collection
    (attempts : List AttemptRecord) (attempt : AttemptRecord)
    (member : attempt ∈ attempts) : attempt.attemptId ∈ collectAttemptIds attempts := by
  induction attempts with
  | nil => simp at member
  | cons head tail ih =>
      simp only [List.mem_cons] at member
      simp only [collectAttemptIds, List.mem_cons]
      rcases member with same | rest
      · left; exact congrArg AttemptRecord.attemptId same
      · right; exact ih rest

def CompleteAttemptDenominator (attempts : List AttemptRecord) : Prop :=
  forall attempt, attempt ∈ attempts -> attempt.includedInDenominator = true

theorem complete_denominator_counts_every_member
    (attempts : List AttemptRecord) (complete : CompleteAttemptDenominator attempts)
    (attempt : AttemptRecord) (member : attempt ∈ attempts) :
    attempt.includedInDenominator = true := complete attempt member

theorem omitted_attempt_rejects_complete_denominator
    (attempts : List AttemptRecord) (attempt : AttemptRecord)
    (member : attempt ∈ attempts) (omitted : attempt.includedInDenominator = false) :
    Not (CompleteAttemptDenominator attempts) := by
  intro complete
  have counted := complete attempt member
  simp [omitted] at counted

structure ForecastAlternative where
  modelId : Nat
  preregistered : Bool
  heldoutScored : Bool
deriving DecidableEq, Repr

def EveryPreregisteredAlternativeScored (alternatives : List ForecastAlternative) : Prop :=
  forall candidate, candidate ∈ alternatives ->
    candidate.preregistered = true -> candidate.heldoutScored = true

theorem unscored_preregistered_alternative_rejects_complete_comparison
    (alternatives : List ForecastAlternative) (candidate : ForecastAlternative)
    (member : candidate ∈ alternatives) (registered : candidate.preregistered = true)
    (unscored : candidate.heldoutScored = false) :
    Not (EveryPreregisteredAlternativeScored alternatives) := by
  intro complete
  have scored := complete candidate member registered
  simp [unscored] at scored

structure ForecastDossier where
  claimIdentityBound : Bool := true
  populationBound : Bool := true
  sampleProcessBound : Bool := true
  dataSupportBound : Bool := true
  hypothesisFamilyBound : Bool := true
  algorithmBound : Bool := true
  optimizationPathBound : Bool := true
  architectureBound : Bool := true
  metricBound : Bool := true
  computeRegimeBound : Bool := true
  observedRangeBound : Bool := true
  forecastHorizonBound : Bool := true
  candidateFamiliesBound : Bool := true
  fittingRuleBound : Bool := true
  uncertaintyBound : Bool := true
  predictionIntervalBound : Bool := true
  breakpointAlternativesBound : Bool := true
  metricTransformBound : Bool := true
  prospectiveFreezeBound : Bool := true
  heldoutScaleBound : Bool := true
  failedRunsPreserved : Bool := true
  attemptDenominatorComplete : Bool := true
  dependenceStructureBound : Bool := true
  contaminationChecked : Bool := true
  sourceTargetSeparated : Bool := true
  shiftModelBound : Bool := true
  taskFamilyBound : Bool := true
  subgroupBehaviorBound : Bool := true
  calibrationBound : Bool := true
  transferClaimSeparated : Bool := true
  compositionClaimSeparated : Bool := true
  safetyClaimSeparated : Bool := true
  correctionLineagePresent : Bool := true
  consumerPurposeBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  residualOwnerBound : Bool := true
  fallbackBound : Bool := true
  retirementBound : Bool := true
  independentReanalysisBound : Bool := true
  totalCostBound : Bool := true
  broadGeneralizationClaimed : Bool := false
  mechanismEmergenceClaimed : Bool := false
  futureScalingClaimed : Bool := false
  safetyClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : ForecastDossier) : Prop := d.currentTick <= d.expiresAt
instance currentDecidable (d : ForecastDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : ForecastDossier) : Prop :=
  d.claimIdentityBound = true ∧ d.populationBound = true ∧
  d.sampleProcessBound = true ∧ d.dataSupportBound = true ∧
  d.hypothesisFamilyBound = true ∧ d.algorithmBound = true ∧
  d.optimizationPathBound = true ∧ d.architectureBound = true ∧
  d.metricBound = true ∧ d.computeRegimeBound = true

def DesignComplete (d : ForecastDossier) : Prop :=
  d.observedRangeBound = true ∧ d.forecastHorizonBound = true ∧
  d.candidateFamiliesBound = true ∧ d.fittingRuleBound = true ∧
  d.uncertaintyBound = true ∧ d.predictionIntervalBound = true ∧
  d.breakpointAlternativesBound = true ∧ d.metricTransformBound = true ∧
  d.prospectiveFreezeBound = true ∧ d.heldoutScaleBound = true ∧
  d.failedRunsPreserved = true ∧ d.attemptDenominatorComplete = true

def TransferComplete (d : ForecastDossier) : Prop :=
  d.dependenceStructureBound = true ∧ d.contaminationChecked = true ∧
  d.sourceTargetSeparated = true ∧ d.shiftModelBound = true ∧
  d.taskFamilyBound = true ∧ d.subgroupBehaviorBound = true ∧
  d.calibrationBound = true ∧ d.transferClaimSeparated = true ∧
  d.compositionClaimSeparated = true ∧ d.safetyClaimSeparated = true

def LifecycleComplete (d : ForecastDossier) : Prop :=
  d.correctionLineagePresent = true ∧ d.consumerPurposeBound = true ∧ Current d ∧
  d.residualOwnerBound = true ∧ d.fallbackBound = true ∧
  d.retirementBound = true ∧ d.independentReanalysisBound = true ∧
  d.totalCostBound = true

def BoundaryComplete (d : ForecastDossier) : Prop :=
  d.broadGeneralizationClaimed = false ∧ d.mechanismEmergenceClaimed = false ∧
  d.futureScalingClaimed = false ∧ d.safetyClaimed = false ∧
  d.supportOrReleaseRequested = false

instance identityDecidable (d : ForecastDossier) : Decidable (IdentityComplete d) := by
  unfold IdentityComplete; infer_instance
instance designDecidable (d : ForecastDossier) : Decidable (DesignComplete d) := by
  unfold DesignComplete; infer_instance
instance transferDecidable (d : ForecastDossier) : Decidable (TransferComplete d) := by
  unfold TransferComplete; infer_instance
instance lifecycleDecidable (d : ForecastDossier) : Decidable (LifecycleComplete d) := by
  unfold LifecycleComplete Current; infer_instance
instance boundaryDecidable (d : ForecastDossier) : Decidable (BoundaryComplete d) := by
  unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : ForecastDossier) : Prop :=
  IdentityComplete d ∧ DesignComplete d ∧ TransferComplete d ∧
  LifecycleComplete d ∧ BoundaryComplete d
instance admissibleDecidable (d : ForecastDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete DesignComplete TransferComplete
    LifecycleComplete Current BoundaryComplete
  infer_instance
def DossierReady (d : ForecastDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | designReviewed | transferReviewed
  | lifecycleReviewed | boundaryReviewed | repairRequired
  | eligibleForTheseusProspectiveForecastCampaign
deriving DecidableEq, Repr

def ReviewStepFor (d : ForecastDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (DesignComplete d) then .designReviewed else .repairRequired
  | .designReviewed => if decide (TransferComplete d) then .transferReviewed else .repairRequired
  | .transferReviewed => if decide (LifecycleComplete d) then .lifecycleReviewed else .repairRequired
  | .lifecycleReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusProspectiveForecastCampaign
  | state => state

def ReviewRun (d : ForecastDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : ForecastDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .designReviewed => IdentityComplete d ∧ DesignComplete d
  | .transferReviewed => IdentityComplete d ∧ DesignComplete d ∧ TransferComplete d
  | .lifecycleReviewed =>
      IdentityComplete d ∧ DesignComplete d ∧ TransferComplete d ∧ LifecycleComplete d
  | .boundaryReviewed | .eligibleForTheseusProspectiveForecastCampaign => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : ForecastDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case designReviewed => split <;> simp_all [StageInvariant]
  case transferReviewed => split <;> simp_all [StageInvariant]
  case lifecycleReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : ForecastDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem campaign_eligibility_requires_admissible_dossier
    (d : ForecastDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusProspectiveForecastCampaign) :
    DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : ForecastDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_theseus_prospective_forecast_campaign :
    ReviewRun completeDossier 6 = .eligibleForTheseusProspectiveForecastCampaign := by decide

inductive AdmissionAxis where
  | claimIdentity | population | sampleProcess | dataSupport | hypothesisFamily
  | algorithm | optimizationPath | architecture | metric | computeRegime
  | observedRange | forecastHorizon | candidateFamilies | fittingRule | uncertainty
  | predictionInterval | breakpointAlternatives | metricTransform | prospectiveFreeze
  | heldoutScale | failedRuns | attemptDenominator | dependenceStructure | contamination
  | sourceTargetSeparation | shiftModel | taskFamily | subgroupBehavior | calibration
  | transferSeparation | compositionSeparation | safetySeparation | correctionLineage
  | consumerPurpose | expiry | residualOwner | fallback | retirement
  | independentReanalysis | totalCost | broadGeneralizationClaim | mechanismEmergenceClaim
  | futureScalingClaim | safetyClaim | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> ForecastDossier
  | .claimIdentity => { completeDossier with claimIdentityBound := false }
  | .population => { completeDossier with populationBound := false }
  | .sampleProcess => { completeDossier with sampleProcessBound := false }
  | .dataSupport => { completeDossier with dataSupportBound := false }
  | .hypothesisFamily => { completeDossier with hypothesisFamilyBound := false }
  | .algorithm => { completeDossier with algorithmBound := false }
  | .optimizationPath => { completeDossier with optimizationPathBound := false }
  | .architecture => { completeDossier with architectureBound := false }
  | .metric => { completeDossier with metricBound := false }
  | .computeRegime => { completeDossier with computeRegimeBound := false }
  | .observedRange => { completeDossier with observedRangeBound := false }
  | .forecastHorizon => { completeDossier with forecastHorizonBound := false }
  | .candidateFamilies => { completeDossier with candidateFamiliesBound := false }
  | .fittingRule => { completeDossier with fittingRuleBound := false }
  | .uncertainty => { completeDossier with uncertaintyBound := false }
  | .predictionInterval => { completeDossier with predictionIntervalBound := false }
  | .breakpointAlternatives => { completeDossier with breakpointAlternativesBound := false }
  | .metricTransform => { completeDossier with metricTransformBound := false }
  | .prospectiveFreeze => { completeDossier with prospectiveFreezeBound := false }
  | .heldoutScale => { completeDossier with heldoutScaleBound := false }
  | .failedRuns => { completeDossier with failedRunsPreserved := false }
  | .attemptDenominator => { completeDossier with attemptDenominatorComplete := false }
  | .dependenceStructure => { completeDossier with dependenceStructureBound := false }
  | .contamination => { completeDossier with contaminationChecked := false }
  | .sourceTargetSeparation => { completeDossier with sourceTargetSeparated := false }
  | .shiftModel => { completeDossier with shiftModelBound := false }
  | .taskFamily => { completeDossier with taskFamilyBound := false }
  | .subgroupBehavior => { completeDossier with subgroupBehaviorBound := false }
  | .calibration => { completeDossier with calibrationBound := false }
  | .transferSeparation => { completeDossier with transferClaimSeparated := false }
  | .compositionSeparation => { completeDossier with compositionClaimSeparated := false }
  | .safetySeparation => { completeDossier with safetyClaimSeparated := false }
  | .correctionLineage => { completeDossier with correctionLineagePresent := false }
  | .consumerPurpose => { completeDossier with consumerPurposeBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .residualOwner => { completeDossier with residualOwnerBound := false }
  | .fallback => { completeDossier with fallbackBound := false }
  | .retirement => { completeDossier with retirementBound := false }
  | .independentReanalysis => { completeDossier with independentReanalysisBound := false }
  | .totalCost => { completeDossier with totalCostBound := false }
  | .broadGeneralizationClaim => { completeDossier with broadGeneralizationClaimed := true }
  | .mechanismEmergenceClaim => { completeDossier with mechanismEmergenceClaimed := true }
  | .futureScalingClaim => { completeDossier with futureScalingClaimed := true }
  | .safetyClaim => { completeDossier with safetyClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindClaimIdentity | bindPopulation | bindSampleProcess | bindDataSupport
  | bindHypothesisFamily | bindAlgorithm | bindOptimizationPath | bindArchitecture
  | bindMetric | bindComputeRegime | bindObservedRange | bindForecastHorizon
  | bindCandidateFamilies | bindFittingRule | bindUncertainty | bindPredictionInterval
  | bindBreakpointAlternatives | bindMetricTransform | freezeProspectively
  | bindHeldoutScale | preserveFailedRuns | completeAttemptDenominator
  | bindDependenceStructure | checkContamination | separateSourceTarget
  | bindShiftModel | bindTaskFamily | bindSubgroupBehavior | bindCalibration
  | separateTransferClaim | separateCompositionClaim | separateSafetyClaim
  | addCorrectionLineage | bindConsumerPurpose | renewExpiry | assignResidualOwner
  | bindFallback | bindRetirement | bindIndependentReanalysis | bindTotalCost
  | rejectBroadGeneralizationClaim | rejectMechanismEmergenceClaim
  | rejectFutureScalingClaim | rejectSafetyClaim | refuseSupportOrRelease
  | eligibleForTheseusProspectiveForecastCampaign
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .claimIdentity => .bindClaimIdentity | .population => .bindPopulation
  | .sampleProcess => .bindSampleProcess | .dataSupport => .bindDataSupport
  | .hypothesisFamily => .bindHypothesisFamily | .algorithm => .bindAlgorithm
  | .optimizationPath => .bindOptimizationPath | .architecture => .bindArchitecture
  | .metric => .bindMetric | .computeRegime => .bindComputeRegime
  | .observedRange => .bindObservedRange | .forecastHorizon => .bindForecastHorizon
  | .candidateFamilies => .bindCandidateFamilies | .fittingRule => .bindFittingRule
  | .uncertainty => .bindUncertainty | .predictionInterval => .bindPredictionInterval
  | .breakpointAlternatives => .bindBreakpointAlternatives
  | .metricTransform => .bindMetricTransform | .prospectiveFreeze => .freezeProspectively
  | .heldoutScale => .bindHeldoutScale | .failedRuns => .preserveFailedRuns
  | .attemptDenominator => .completeAttemptDenominator
  | .dependenceStructure => .bindDependenceStructure | .contamination => .checkContamination
  | .sourceTargetSeparation => .separateSourceTarget | .shiftModel => .bindShiftModel
  | .taskFamily => .bindTaskFamily | .subgroupBehavior => .bindSubgroupBehavior
  | .calibration => .bindCalibration | .transferSeparation => .separateTransferClaim
  | .compositionSeparation => .separateCompositionClaim
  | .safetySeparation => .separateSafetyClaim | .correctionLineage => .addCorrectionLineage
  | .consumerPurpose => .bindConsumerPurpose | .expiry => .renewExpiry
  | .residualOwner => .assignResidualOwner | .fallback => .bindFallback
  | .retirement => .bindRetirement | .independentReanalysis => .bindIndependentReanalysis
  | .totalCost => .bindTotalCost
  | .broadGeneralizationClaim => .rejectBroadGeneralizationClaim
  | .mechanismEmergenceClaim => .rejectMechanismEmergenceClaim
  | .futureScalingClaim => .rejectFutureScalingClaim
  | .safetyClaim => .rejectSafetyClaim | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : ForecastDossier) : RepairDisposition :=
  if !d.claimIdentityBound then .bindClaimIdentity
  else if !d.populationBound then .bindPopulation
  else if !d.sampleProcessBound then .bindSampleProcess
  else if !d.dataSupportBound then .bindDataSupport
  else if !d.hypothesisFamilyBound then .bindHypothesisFamily
  else if !d.algorithmBound then .bindAlgorithm
  else if !d.optimizationPathBound then .bindOptimizationPath
  else if !d.architectureBound then .bindArchitecture
  else if !d.metricBound then .bindMetric
  else if !d.computeRegimeBound then .bindComputeRegime
  else if !d.observedRangeBound then .bindObservedRange
  else if !d.forecastHorizonBound then .bindForecastHorizon
  else if !d.candidateFamiliesBound then .bindCandidateFamilies
  else if !d.fittingRuleBound then .bindFittingRule
  else if !d.uncertaintyBound then .bindUncertainty
  else if !d.predictionIntervalBound then .bindPredictionInterval
  else if !d.breakpointAlternativesBound then .bindBreakpointAlternatives
  else if !d.metricTransformBound then .bindMetricTransform
  else if !d.prospectiveFreezeBound then .freezeProspectively
  else if !d.heldoutScaleBound then .bindHeldoutScale
  else if !d.failedRunsPreserved then .preserveFailedRuns
  else if !d.attemptDenominatorComplete then .completeAttemptDenominator
  else if !d.dependenceStructureBound then .bindDependenceStructure
  else if !d.contaminationChecked then .checkContamination
  else if !d.sourceTargetSeparated then .separateSourceTarget
  else if !d.shiftModelBound then .bindShiftModel
  else if !d.taskFamilyBound then .bindTaskFamily
  else if !d.subgroupBehaviorBound then .bindSubgroupBehavior
  else if !d.calibrationBound then .bindCalibration
  else if !d.transferClaimSeparated then .separateTransferClaim
  else if !d.compositionClaimSeparated then .separateCompositionClaim
  else if !d.safetyClaimSeparated then .separateSafetyClaim
  else if !d.correctionLineagePresent then .addCorrectionLineage
  else if !d.consumerPurposeBound then .bindConsumerPurpose
  else if !decide (Current d) then .renewExpiry
  else if !d.residualOwnerBound then .assignResidualOwner
  else if !d.fallbackBound then .bindFallback
  else if !d.retirementBound then .bindRetirement
  else if !d.independentReanalysisBound then .bindIndependentReanalysis
  else if !d.totalCostBound then .bindTotalCost
  else if d.broadGeneralizationClaimed then .rejectBroadGeneralizationClaim
  else if d.mechanismEmergenceClaimed then .rejectMechanismEmergenceClaim
  else if d.futureScalingClaimed then .rejectFutureScalingClaim
  else if d.safetyClaimed then .rejectSafetyClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusProspectiveForecastCampaign

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 6 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : ForecastDossier) (h : DossierReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_design (d : ForecastDossier) (h : DossierReady d = true) :
    DesignComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_transfer (d : ForecastDossier) (h : DossierReady d = true) :
    TransferComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_lifecycle (d : ForecastDossier) (h : DossierReady d = true) :
    LifecycleComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_boundary (d : ForecastDossier) (h : DossierReady d = true) :
    BoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2

theorem expired_forecast_contract_remains_expired_when_time_advances
    (d : ForecastDossier) (later : Nat) (expired : d.expiresAt < d.currentTick)
    (advances : d.currentTick <= later) : Not (Current { d with currentTick := later }) := by
  intro current; unfold Current at current; change later <= d.expiresAt at current; omega

theorem extrapolation_remains_outside_support_when_observed_range_shrinks
    (observedMax target smallerMax : Nat) (outside : observedMax < target)
    (shrinks : smallerMax <= observedMax) : Not (target <= smallerMax) := by omega

theorem unscored_gap_persists_when_scored_count_falls
    (required scored fewer : Nat) (gap : scored < required) (falls : fewer <= scored) :
    Not (required <= fewer) := by omega

structure ReceiptScope where
  populationId : Nat
  sampleProcessId : Nat
  algorithmId : Nat
  architectureId : Nat
  metricId : Nat
  computeRegimeId : Nat
  horizonId : Nat
deriving DecidableEq, Repr

def ReceiptUseAllowed
    (s : ReceiptScope) (population sample algorithm architecture metric compute horizon : Nat) : Prop :=
  population = s.populationId ∧ sample = s.sampleProcessId ∧
  algorithm = s.algorithmId ∧ architecture = s.architectureId ∧
  metric = s.metricId ∧ compute = s.computeRegimeId ∧ horizon = s.horizonId

theorem population_change_invalidates_forecast_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.populationId)) :
    Not (ReceiptUseAllowed s v s.sampleProcessId s.algorithmId s.architectureId
      s.metricId s.computeRegimeId s.horizonId) := by intro x; exact h x.1
theorem sample_process_change_invalidates_forecast_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.sampleProcessId)) :
    Not (ReceiptUseAllowed s s.populationId v s.algorithmId s.architectureId
      s.metricId s.computeRegimeId s.horizonId) := by intro x; exact h x.2.1
theorem algorithm_change_invalidates_forecast_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.algorithmId)) :
    Not (ReceiptUseAllowed s s.populationId s.sampleProcessId v s.architectureId
      s.metricId s.computeRegimeId s.horizonId) := by intro x; exact h x.2.2.1
theorem architecture_change_invalidates_forecast_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.architectureId)) :
    Not (ReceiptUseAllowed s s.populationId s.sampleProcessId s.algorithmId v
      s.metricId s.computeRegimeId s.horizonId) := by intro x; exact h x.2.2.2.1
theorem metric_change_invalidates_forecast_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.metricId)) :
    Not (ReceiptUseAllowed s s.populationId s.sampleProcessId s.algorithmId
      s.architectureId v s.computeRegimeId s.horizonId) := by intro x; exact h x.2.2.2.2.1
theorem compute_regime_change_invalidates_forecast_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.computeRegimeId)) :
    Not (ReceiptUseAllowed s s.populationId s.sampleProcessId s.algorithmId
      s.architectureId s.metricId v s.horizonId) := by intro x; exact h x.2.2.2.2.2.1
theorem horizon_change_invalidates_forecast_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.horizonId)) :
    Not (ReceiptUseAllowed s s.populationId s.sampleProcessId s.algorithmId
      s.architectureId s.metricId s.computeRegimeId v) := by intro x; exact h x.2.2.2.2.2.2

structure RetrospectiveFitSignals where
  observedFitError : Nat
  observedRangeWidth : Nat
deriving DecidableEq, Repr
structure ProspectiveForecastCase where
  signals : RetrospectiveFitSignals
  heldoutCovered : Bool
deriving DecidableEq, Repr
def sharedFitSignals : RetrospectiveFitSignals := ⟨2, 100⟩
def coveredForecastCase : ProspectiveForecastCase := ⟨sharedFitSignals, true⟩
def missedForecastCase : ProspectiveForecastCase := ⟨sharedFitSignals, false⟩
def HeldoutCovered (c : ProspectiveForecastCase) : Bool := c.heldoutCovered

theorem identical_retrospective_fit_can_hide_opposite_prospective_coverage :
    coveredForecastCase.signals = missedForecastCase.signals ∧
    HeldoutCovered coveredForecastCase = true ∧
    HeldoutCovered missedForecastCase = false := by decide

theorem retrospective_fit_cannot_recover_prospective_coverage
    (classify : RetrospectiveFitSignals -> Bool) :
    Not (forall c : ProspectiveForecastCase, classify c.signals = HeldoutCovered c) := by
  intro exact
  have a := exact coveredForecastCase
  have b := exact missedForecastCase
  simp [coveredForecastCase, missedForecastCase, sharedFitSignals, HeldoutCovered] at a b
  rw [a] at b
  contradiction

structure ThresholdSignals where
  belowThresholdScore : Nat
  aboveThresholdScore : Nat
deriving DecidableEq, Repr
structure EmergenceCase where
  signals : ThresholdSignals
  underlyingMechanismChanged : Bool
deriving DecidableEq, Repr
def sharedThresholdSignals : ThresholdSignals := ⟨0, 1⟩
def smoothThresholdCase : EmergenceCase := ⟨sharedThresholdSignals, false⟩
def mechanismChangeCase : EmergenceCase := ⟨sharedThresholdSignals, true⟩
def MechanismChanged (c : EmergenceCase) : Bool := c.underlyingMechanismChanged

theorem identical_threshold_metrics_can_hide_opposite_mechanism_change :
    smoothThresholdCase.signals = mechanismChangeCase.signals ∧
    MechanismChanged smoothThresholdCase = false ∧
    MechanismChanged mechanismChangeCase = true := by decide

theorem threshold_metrics_cannot_recover_mechanism_change
    (classify : ThresholdSignals -> Bool) :
    Not (forall c : EmergenceCase, classify c.signals = MechanismChanged c) := by
  intro exact
  have a := exact smoothThresholdCase
  have b := exact mechanismChangeCase
  simp [smoothThresholdCase, mechanismChangeCase, sharedThresholdSignals, MechanismChanged] at a b
  rw [a] at b
  contradiction

def forecastRatchetReview (prospectiveHoldoutPresent : Bool) :
    BenchmarkRatchets.RatchetDecisionReview :=
  { lifecycle := .frontier
    benchmarkSaturated := false
    contaminationSuspected := false
    transferOrMutationCheckPresent := prospectiveHoldoutPresent
    regressionRecordsPreserved := true
    negativeResultsPreserved := true
    decision := .promoteReadiness }

theorem missing_prospective_holdout_rejects_benchmark_ratchet_promotion
    (present : Bool) (missing : present = false) :
    Not (BenchmarkRatchets.RatchetDecisionAccepted (forecastRatchetReview present)) := by
  intro accepted
  have required :=
    BenchmarkRatchets.accepted_readiness_promotion_requires_transfer_negative_and_regression_records
      accepted (by rfl)
  simp [forecastRatchetReview, missing] at required

end AsiStackProofs.LearningTheoryForecastReview

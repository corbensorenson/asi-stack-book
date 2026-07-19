namespace AsiStackProofs.PolicyOptimizationRefinement

inductive Stage where
  | draft | scoped | stateBound | updated | evaluated | adjudicated | leaseBound
deriving DecidableEq, Repr

inductive EventKind where
  | scopeUpdate | bindTrainingState | recordUpdate | recordEvaluation
  | adjudicateUpdate | requestBoundedLease | triggerReadmission
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectIdentitySubstitution | rejectReplay | rejectAuthorityLeak
  | requestTargetPolicy | requestBaseline | requestObjective | requestPermittedDelta
  | requestAuthorityCeiling | requestRiskTier | requestConsumer | acceptScope
  | requestDataset | requestFeedbackBoundary | requestHoldout | requestContaminationCheck
  | requestBaseCheckpoint | requestOptimizer | requestScheduler | requestRng
  | requestCacheInventory | requestBackupInventory | requestDescendantInventory
  | requestRollbackSnapshot | acceptStateBinding
  | requestCandidateCheckpoint | requestUpdateReceipt | requestCompleteDenominator
  | requestFailureLog | requestResourceCost | rejectStateLineageGap | acceptUpdateReceipt
  | requestIndependentEvaluator | requestTargetEvaluation | requestStrongBaseline
  | requestCausalAblation | requestRewardHackProbe | requestRegressionSuite
  | requestForgettingTest | requestSafetyRightsTest | requestUncertainty | acceptEvaluation
  | requestResidualOwner | requestCounterevidence | requestRollbackCriterion
  | requestRollbackRehearsal | requestMonitoringPlan | rejectImprovementInference
  | rejectReleaseAuthorityLaundering | acceptAdjudication
  | requestPermittedConsumer | requestBoundedLeaseRecord | requestCheckpointBinding
  | requestExpiry | requestRollbackHandle | requestNoSupportAuthority | acceptBoundedLease
  | requestMaterialChangeTrigger | requestDescendantInvalidation
  | requestOrdinaryRouteBlock | requestEffectCompleteRollback
  | rejectSuccessorVersion | acceptReadmission
deriving DecidableEq, Repr

structure Packet where
  updateId : Nat
  targetPolicyDigest : Nat
  baselineDigest : Nat
  objectiveDigest : Nat
  datasetDigest : Nat
  feedbackDigest : Nat
  baseCheckpointDigest : Nat
  candidateCheckpointDigest : Nat
  optimizerDigest : Nat
  schedulerDigest : Nat
  rngDigest : Nat
  evaluatorDigest : Nat
  rollbackDigest : Nat
  consumerDigest : Nat
  authorityDigest : Nat
  currentVersion : Nat
  successorVersion : Nat
  eventDigest : Nat
  targetPolicyPresent : Bool
  baselinePresent : Bool
  objectivePresent : Bool
  permittedDeltaPresent : Bool
  authorityCeilingPresent : Bool
  riskTierPresent : Bool
  consumerPresent : Bool
  datasetPresent : Bool
  feedbackBoundaryPresent : Bool
  holdoutPresent : Bool
  contaminationCheckPresent : Bool
  baseCheckpointPresent : Bool
  optimizerPresent : Bool
  schedulerPresent : Bool
  rngPresent : Bool
  cacheInventoryPresent : Bool
  backupInventoryPresent : Bool
  descendantInventoryPresent : Bool
  rollbackSnapshotPresent : Bool
  candidateCheckpointPresent : Bool
  updateReceiptPresent : Bool
  completeDenominatorPresent : Bool
  failureLogPresent : Bool
  resourceCostPresent : Bool
  stateLineageComplete : Bool
  independentEvaluatorPresent : Bool
  targetEvaluationPresent : Bool
  strongBaselinePresent : Bool
  causalAblationPresent : Bool
  rewardHackProbePresent : Bool
  regressionSuitePresent : Bool
  forgettingTestPresent : Bool
  safetyRightsTestPresent : Bool
  uncertaintyPresent : Bool
  residualOwnerPresent : Bool
  counterevidencePresent : Bool
  rollbackCriterionPresent : Bool
  rollbackRehearsalPresent : Bool
  monitoringPlanPresent : Bool
  noImprovementInferenceRecorded : Bool
  noReleaseAuthorityRecorded : Bool
  permittedConsumerPresent : Bool
  boundedLeaseRecordPresent : Bool
  checkpointDigestBound : Bool
  expiryPresent : Bool
  rollbackHandlePresent : Bool
  noSupportAuthorityRecorded : Bool
  materialChangeTriggerPresent : Bool
  descendantInvalidationComplete : Bool
  ordinaryRouteBlocked : Bool
  effectCompleteRollbackPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure State where
  stage : Stage
  updateId : Nat
  targetPolicyDigest : Nat
  baselineDigest : Nat
  objectiveDigest : Nat
  datasetDigest : Nat
  feedbackDigest : Nat
  baseCheckpointDigest : Nat
  candidateCheckpointDigest : Nat
  optimizerDigest : Nat
  schedulerDigest : Nat
  rngDigest : Nat
  evaluatorDigest : Nat
  rollbackDigest : Nat
  consumerDigest : Nat
  authorityDigest : Nat
  version : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  boundedLeaseCount : Nat
  readmissionCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .draft => .scopeUpdate
  | .scoped => .bindTrainingState
  | .stateBound => .recordUpdate
  | .updated => .recordEvaluation
  | .evaluated => .adjudicateUpdate
  | .adjudicated => .requestBoundedLease
  | .leaseBound => .triggerReadmission

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.updateId = packet.updateId &&
  state.targetPolicyDigest = packet.targetPolicyDigest &&
  state.baselineDigest = packet.baselineDigest &&
  state.objectiveDigest = packet.objectiveDigest &&
  state.datasetDigest = packet.datasetDigest &&
  state.feedbackDigest = packet.feedbackDigest &&
  state.baseCheckpointDigest = packet.baseCheckpointDigest &&
  state.candidateCheckpointDigest = packet.candidateCheckpointDigest &&
  state.optimizerDigest = packet.optimizerDigest &&
  state.schedulerDigest = packet.schedulerDigest && state.rngDigest = packet.rngDigest &&
  state.evaluatorDigest = packet.evaluatorDigest && state.rollbackDigest = packet.rollbackDigest &&
  state.consumerDigest = packet.consumerDigest && state.authorityDigest = packet.authorityDigest &&
  state.version = packet.currentVersion

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if kind != expectedKind state.stage then .rejectWrongStage
  else if identityMatches state packet = false then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectReplay
  else if packet.supportAssignmentRequested || packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .draft =>
      if packet.targetPolicyPresent = false then .requestTargetPolicy
      else if packet.baselinePresent = false then .requestBaseline
      else if packet.objectivePresent = false then .requestObjective
      else if packet.permittedDeltaPresent = false then .requestPermittedDelta
      else if packet.authorityCeilingPresent = false then .requestAuthorityCeiling
      else if packet.riskTierPresent = false then .requestRiskTier
      else if packet.consumerPresent = false then .requestConsumer
      else .acceptScope
  | .scoped =>
      if packet.datasetPresent = false then .requestDataset
      else if packet.feedbackBoundaryPresent = false then .requestFeedbackBoundary
      else if packet.holdoutPresent = false then .requestHoldout
      else if packet.contaminationCheckPresent = false then .requestContaminationCheck
      else if packet.baseCheckpointPresent = false then .requestBaseCheckpoint
      else if packet.optimizerPresent = false then .requestOptimizer
      else if packet.schedulerPresent = false then .requestScheduler
      else if packet.rngPresent = false then .requestRng
      else if packet.cacheInventoryPresent = false then .requestCacheInventory
      else if packet.backupInventoryPresent = false then .requestBackupInventory
      else if packet.descendantInventoryPresent = false then .requestDescendantInventory
      else if packet.rollbackSnapshotPresent = false then .requestRollbackSnapshot
      else .acceptStateBinding
  | .stateBound =>
      if packet.candidateCheckpointPresent = false then .requestCandidateCheckpoint
      else if packet.updateReceiptPresent = false then .requestUpdateReceipt
      else if packet.completeDenominatorPresent = false then .requestCompleteDenominator
      else if packet.failureLogPresent = false then .requestFailureLog
      else if packet.resourceCostPresent = false then .requestResourceCost
      else if packet.stateLineageComplete = false then .rejectStateLineageGap
      else .acceptUpdateReceipt
  | .updated =>
      if packet.independentEvaluatorPresent = false then .requestIndependentEvaluator
      else if packet.targetEvaluationPresent = false then .requestTargetEvaluation
      else if packet.strongBaselinePresent = false then .requestStrongBaseline
      else if packet.causalAblationPresent = false then .requestCausalAblation
      else if packet.rewardHackProbePresent = false then .requestRewardHackProbe
      else if packet.regressionSuitePresent = false then .requestRegressionSuite
      else if packet.forgettingTestPresent = false then .requestForgettingTest
      else if packet.safetyRightsTestPresent = false then .requestSafetyRightsTest
      else if packet.uncertaintyPresent = false then .requestUncertainty
      else .acceptEvaluation
  | .evaluated =>
      if packet.residualOwnerPresent = false then .requestResidualOwner
      else if packet.counterevidencePresent = false then .requestCounterevidence
      else if packet.rollbackCriterionPresent = false then .requestRollbackCriterion
      else if packet.rollbackRehearsalPresent = false then .requestRollbackRehearsal
      else if packet.monitoringPlanPresent = false then .requestMonitoringPlan
      else if packet.noImprovementInferenceRecorded = false then .rejectImprovementInference
      else if packet.noReleaseAuthorityRecorded = false then .rejectReleaseAuthorityLaundering
      else .acceptAdjudication
  | .adjudicated =>
      if packet.permittedConsumerPresent = false then .requestPermittedConsumer
      else if packet.boundedLeaseRecordPresent = false then .requestBoundedLeaseRecord
      else if packet.checkpointDigestBound = false then .requestCheckpointBinding
      else if packet.expiryPresent = false then .requestExpiry
      else if packet.rollbackHandlePresent = false then .requestRollbackHandle
      else if packet.noSupportAuthorityRecorded = false then .requestNoSupportAuthority
      else .acceptBoundedLease
  | .leaseBound =>
      if packet.materialChangeTriggerPresent = false then .requestMaterialChangeTrigger
      else if packet.descendantInvalidationComplete = false then .requestDescendantInvalidation
      else if packet.ordinaryRouteBlocked = false then .requestOrdinaryRouteBlock
      else if packet.effectCompleteRollbackPresent = false then .requestEffectCompleteRollback
      else if packet.successorVersion != state.version + 1 then .rejectSuccessorVersion
      else .acceptReadmission

def accepted : Route -> Bool
  | .acceptScope | .acceptStateBinding | .acceptUpdateReceipt | .acceptEvaluation
  | .acceptAdjudication | .acceptBoundedLease | .acceptReadmission => true
  | _ => false

def nextStage : Stage -> Stage
  | .draft => .scoped
  | .scoped => .stateBound
  | .stateBound => .updated
  | .updated => .evaluated
  | .evaluated => .adjudicated
  | .adjudicated => .leaseBound
  | .leaseBound => .scoped

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       version := if route = .acceptReadmission then packet.successorVersion else state.version
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       boundedLeaseCount := state.boundedLeaseCount + (if route = .acceptBoundedLease then 1 else 0)
       readmissionCount := state.readmissionCount + (if route = .acceptReadmission then 1 else 0) }, route)
  else (state, route)

theorem rejected_event_preserves_complete_state
    (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = false) :
    applyEvent state kind packet = (state, routeFor state kind packet) := by
  simp [applyEvent, h]

theorem accepted_event_increments_receipt_count
    (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = true) :
    (applyEvent state kind packet).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, h]

def canonicalPacket : Packet := {
  updateId := 901, targetPolicyDigest := 902, baselineDigest := 903,
  objectiveDigest := 904, datasetDigest := 905, feedbackDigest := 906,
  baseCheckpointDigest := 907, candidateCheckpointDigest := 908,
  optimizerDigest := 909, schedulerDigest := 910, rngDigest := 911,
  evaluatorDigest := 912, rollbackDigest := 913, consumerDigest := 914,
  authorityDigest := 915, currentVersion := 1, successorVersion := 1, eventDigest := 1,
  targetPolicyPresent := true, baselinePresent := true, objectivePresent := true,
  permittedDeltaPresent := true, authorityCeilingPresent := true, riskTierPresent := true,
  consumerPresent := true, datasetPresent := true, feedbackBoundaryPresent := true,
  holdoutPresent := true, contaminationCheckPresent := true, baseCheckpointPresent := true,
  optimizerPresent := true, schedulerPresent := true, rngPresent := true,
  cacheInventoryPresent := true, backupInventoryPresent := true,
  descendantInventoryPresent := true, rollbackSnapshotPresent := true,
  candidateCheckpointPresent := true, updateReceiptPresent := true,
  completeDenominatorPresent := true, failureLogPresent := true, resourceCostPresent := true,
  stateLineageComplete := true, independentEvaluatorPresent := true,
  targetEvaluationPresent := true, strongBaselinePresent := true, causalAblationPresent := true,
  rewardHackProbePresent := true, regressionSuitePresent := true, forgettingTestPresent := true,
  safetyRightsTestPresent := true, uncertaintyPresent := true, residualOwnerPresent := true,
  counterevidencePresent := true, rollbackCriterionPresent := true,
  rollbackRehearsalPresent := true, monitoringPlanPresent := true,
  noImprovementInferenceRecorded := true, noReleaseAuthorityRecorded := true,
  permittedConsumerPresent := true, boundedLeaseRecordPresent := true,
  checkpointDigestBound := true, expiryPresent := true, rollbackHandlePresent := true,
  noSupportAuthorityRecorded := true, materialChangeTriggerPresent := true,
  descendantInvalidationComplete := true, ordinaryRouteBlocked := true,
  effectCompleteRollbackPresent := true, supportAssignmentRequested := false,
  externalEffectRequested := false }

def canonicalState (stage : Stage) : State := {
  stage := stage, updateId := 901, targetPolicyDigest := 902, baselineDigest := 903,
  objectiveDigest := 904, datasetDigest := 905, feedbackDigest := 906,
  baseCheckpointDigest := 907, candidateCheckpointDigest := 908,
  optimizerDigest := 909, schedulerDigest := 910, rngDigest := 911,
  evaluatorDigest := 912, rollbackDigest := 913, consumerDigest := 914,
  authorityDigest := 915, version := 1, lastEventDigest := 0, receiptCount := 0,
  boundedLeaseCount := 0, readmissionCount := 0, supportAssignmentCount := 0,
  externalEffectCount := 0 }

def canonicalLifecycleState : State :=
  let s1 := (applyEvent (canonicalState .draft) .scopeUpdate
    { canonicalPacket with eventDigest := 1 }).1
  let s2 := (applyEvent s1 .bindTrainingState
    { canonicalPacket with eventDigest := 2 }).1
  let s3 := (applyEvent s2 .recordUpdate
    { canonicalPacket with eventDigest := 3 }).1
  let s4 := (applyEvent s3 .recordEvaluation
    { canonicalPacket with eventDigest := 4 }).1
  let s5 := (applyEvent s4 .adjudicateUpdate
    { canonicalPacket with eventDigest := 5 }).1
  let s6 := (applyEvent s5 .requestBoundedLease
    { canonicalPacket with eventDigest := 6 }).1
  (applyEvent s6 .triggerReadmission
    { canonicalPacket with eventDigest := 7, successorVersion := 2 }).1

def causalAblationBlockedLifecycleState : State :=
  let s1 := (applyEvent (canonicalState .draft) .scopeUpdate
    { canonicalPacket with eventDigest := 1 }).1
  let s2 := (applyEvent s1 .bindTrainingState
    { canonicalPacket with eventDigest := 2 }).1
  let s3 := (applyEvent s2 .recordUpdate
    { canonicalPacket with eventDigest := 3 }).1
  let s4 := (applyEvent s3 .recordEvaluation
    { canonicalPacket with eventDigest := 4, causalAblationPresent := false }).1
  let s5 := (applyEvent s4 .adjudicateUpdate
    { canonicalPacket with eventDigest := 5 }).1
  let s6 := (applyEvent s5 .requestBoundedLease
    { canonicalPacket with eventDigest := 6 }).1
  (applyEvent s6 .triggerReadmission
    { canonicalPacket with eventDigest := 7, successorVersion := 2 }).1

theorem policy_update_full_cycle_composes :
    canonicalLifecycleState.stage = .scoped ∧
    canonicalLifecycleState.version = 2 ∧
    canonicalLifecycleState.receiptCount = 7 ∧
    canonicalLifecycleState.boundedLeaseCount = 1 ∧
    canonicalLifecycleState.readmissionCount = 1 ∧
    canonicalLifecycleState.supportAssignmentCount = 0 ∧
    canonicalLifecycleState.externalEffectCount = 0 := by native_decide

theorem policy_update_failed_evaluation_blocks_downstream_handoff :
    causalAblationBlockedLifecycleState.stage = .updated ∧
    causalAblationBlockedLifecycleState.version = 1 ∧
    causalAblationBlockedLifecycleState.receiptCount = 3 ∧
    causalAblationBlockedLifecycleState.boundedLeaseCount = 0 ∧
    causalAblationBlockedLifecycleState.readmissionCount = 0 ∧
    causalAblationBlockedLifecycleState.supportAssignmentCount = 0 ∧
    causalAblationBlockedLifecycleState.externalEffectCount = 0 := by native_decide

theorem policy_update_lifecycle_routes :
    routeFor (canonicalState .scoped) .bindTrainingState
        { canonicalPacket with optimizerPresent := false } = .requestOptimizer ∧
    routeFor (canonicalState .updated) .recordEvaluation
        { canonicalPacket with targetEvaluationPresent := false } = .requestTargetEvaluation ∧
    routeFor (canonicalState .updated) .recordEvaluation
        { canonicalPacket with causalAblationPresent := false } = .requestCausalAblation ∧
    routeFor (canonicalState .leaseBound) .triggerReadmission
        { canonicalPacket with effectCompleteRollbackPresent := false, successorVersion := 2 } =
          .requestEffectCompleteRollback ∧
    routeFor (canonicalState .adjudicated) .requestBoundedLease
        { canonicalPacket with noSupportAuthorityRecorded := false } = .requestNoSupportAuthority ∧
    routeFor (canonicalState .adjudicated) .requestBoundedLease canonicalPacket =
        .acceptBoundedLease ∧
    routeFor (canonicalState .leaseBound) .triggerReadmission
        { canonicalPacket with successorVersion := 2 } = .acceptReadmission := by native_decide

end AsiStackProofs.PolicyOptimizationRefinement

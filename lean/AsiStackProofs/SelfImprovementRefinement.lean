namespace AsiStackProofs.SelfImprovementRefinement

set_option maxRecDepth 4000

inductive Stage where
  | draft | scoped | proposalBound | implementationReviewed
  | evaluated | adjudicated | replacementBound | outcomeReconciled
deriving DecidableEq, Repr

inductive EventKind where
  | scopeTransition | bindProposal | reviewImplementation | recordEvaluation
  | adjudicateProposal | authorizeReplacementHandoff
  | reconcileReplacementOutcome | triggerReadmission
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectIdentitySubstitution | rejectReplay | rejectAuthorityLeak
  | requestConsumer | requestUse | requestSelfModel | requestMutablePartition
  | requestProtectedPartition | requestAuthorityEnvelope | requestOptimizationTarget
  | requestRiskClass | requestEvaluationHorizon | requestRecursiveDepth
  | requestStopAuthority | requestSupportCeiling | requestStateInventory
  | requestUnknownStateResidual | requestRightsPremises | requestEvaluatorPolicy
  | requestBaselinePolicy | acceptScope
  | requestProposal | requestChangeIdentity | requestDiff | requestLineage
  | requestDependencies | requestProposer | requestImplementer | requestMechanism
  | requestExpectedEffects | requestNonGoals | requestCheaperInterventions
  | rejectSelfRatifiedObjective | acceptProposalBinding
  | requestImplementationArtifact | requestObservedMutationSet
  | requestProtectedInvariantReview | requestBoundaryDeltaReview
  | requestAuthorityDelta | requestSecurityDelta | requestDataPrivacyDelta
  | requestResourceDelta | requestEvaluatorDelta | requestRightsDelta
  | rejectProtectedWeakening | rejectAuthorityWidening | acceptImplementationReview
  | requestFullStateSnapshot | requestModelState | requestOptimizerState
  | requestSchedulerState | requestRngState | requestCacheState
  | requestPromptPolicyState | requestToolCredentialState
  | requestEvaluatorBenchmarkState | requestEnvironmentState
  | requestCheckpointBackupState | requestExternalEffectState
  | requestDescendantState | requestRollbackAuthority | requestCompensationPlan
  | requestIrreversibleResiduals | acceptStateBinding
  | requestStrongBaseline | requestNaturalTaskDistribution | requestFreshHoldout
  | requestContaminationChecks | requestIndependentEvaluator
  | requestEvaluatorDependencies | requestIndependentMonitor
  | requestMonitorDependencies | requestUsefulOutcome | requestRegressions
  | requestUnsafeReleaseMeasure | requestDeceptionProbe | requestDelayedOutcome
  | requestTotalCost | requestEvidenceBundle | acceptEvaluation
  | requestGovernanceApproval | requestEvidenceTransition
  | requestPermittedConsumer | requestBoundedScope | requestTrafficAllocation
  | requestCanaryPlan | requestMonitorWindow | requestStopPath
  | requestRollbackDryRun | requestResidualOwner
  | rejectCandidatePromotionAuthority | acceptAdjudication
  | requestReplacementTransaction | requestTransactionOwner | requestCanaryReceipt
  | requestObservedEffectReceipt | requestMonitorReceipt
  | requestRollbackOrCommitDisposition | requestExactInventoryRestoration
  | requestSemanticRecoverySeparation | requestDescendantInvalidation
  | requestExternalRemediation | requestCompensationReceipt
  | requestIncidentDisclosure | requestAppendOnlyOutcome
  | rejectSupportPromotion | rejectReleaseAuthority | acceptOutcomeReconciliation
  | requestMaterialChangeTrigger | requestAffectedPath
  | requestReadmissionDescendantInvalidation | requestOrdinaryRouteBlock
  | requestStaleGateExpiration | requestNewStateInventory
  | requestRerunRequirement | rejectSuccessorVersion | acceptReadmission
deriving DecidableEq, Repr

structure Packet where
  transitionId : Nat
  selfModelDigest : Nat
  consumerDigest : Nat
  mutablePartitionDigest : Nat
  protectedPartitionDigest : Nat
  authorityDigest : Nat
  objectiveDigest : Nat
  proposalDigest : Nat
  implementationDigest : Nat
  evaluatorDigest : Nat
  monitorDigest : Nat
  baselineDigest : Nat
  stateInventoryDigest : Nat
  replacementTransactionDigest : Nat
  residualDigest : Nat
  evidencePolicyDigest : Nat
  stopAuthorityDigest : Nat
  currentVersion : Nat
  successorVersion : Nat
  eventDigest : Nat
  consumerPresent : Bool
  usePresent : Bool
  selfModelPresent : Bool
  mutablePartitionPresent : Bool
  protectedPartitionPresent : Bool
  authorityEnvelopePresent : Bool
  optimizationTargetPresent : Bool
  riskClassPresent : Bool
  evaluationHorizonPresent : Bool
  recursiveDepthPresent : Bool
  stopAuthorityPresent : Bool
  supportCeilingPresent : Bool
  stateInventoryPresent : Bool
  unknownStateResidualPresent : Bool
  rightsPremisesPresent : Bool
  evaluatorPolicyPresent : Bool
  baselinePolicyPresent : Bool
  proposalPresent : Bool
  changeIdentityPresent : Bool
  diffPresent : Bool
  lineagePresent : Bool
  dependenciesPresent : Bool
  proposerPresent : Bool
  implementerPresent : Bool
  mechanismPresent : Bool
  expectedEffectsPresent : Bool
  nonGoalsPresent : Bool
  cheaperInterventionsPresent : Bool
  noSelfRatifiedObjectiveRecorded : Bool
  implementationArtifactPresent : Bool
  observedMutationSetPresent : Bool
  protectedInvariantReviewPresent : Bool
  boundaryDeltaReviewPresent : Bool
  authorityDeltaPresent : Bool
  securityDeltaPresent : Bool
  dataPrivacyDeltaPresent : Bool
  resourceDeltaPresent : Bool
  evaluatorDeltaPresent : Bool
  rightsDeltaPresent : Bool
  noProtectedWeakeningRecorded : Bool
  noAuthorityWideningRecorded : Bool
  fullStateSnapshotPresent : Bool
  modelStatePresent : Bool
  optimizerStatePresent : Bool
  schedulerStatePresent : Bool
  rngStatePresent : Bool
  cacheStatePresent : Bool
  promptPolicyStatePresent : Bool
  toolCredentialStatePresent : Bool
  evaluatorBenchmarkStatePresent : Bool
  environmentStatePresent : Bool
  checkpointBackupStatePresent : Bool
  externalEffectStatePresent : Bool
  descendantStatePresent : Bool
  rollbackAuthorityPresent : Bool
  compensationPlanPresent : Bool
  irreversibleResidualsPresent : Bool
  strongBaselinePresent : Bool
  naturalTaskDistributionPresent : Bool
  freshHoldoutPresent : Bool
  contaminationChecksPresent : Bool
  independentEvaluatorPresent : Bool
  evaluatorDependenciesPresent : Bool
  independentMonitorPresent : Bool
  monitorDependenciesPresent : Bool
  usefulOutcomePresent : Bool
  regressionsPresent : Bool
  unsafeReleaseMeasurePresent : Bool
  deceptionProbePresent : Bool
  delayedOutcomePresent : Bool
  totalCostPresent : Bool
  evidenceBundlePresent : Bool
  governanceApprovalPresent : Bool
  evidenceTransitionPresent : Bool
  permittedConsumerPresent : Bool
  boundedScopePresent : Bool
  trafficAllocationPresent : Bool
  canaryPlanPresent : Bool
  monitorWindowPresent : Bool
  stopPathPresent : Bool
  rollbackDryRunPresent : Bool
  residualOwnerPresent : Bool
  noCandidatePromotionAuthorityRecorded : Bool
  replacementTransactionPresent : Bool
  transactionOwnerPresent : Bool
  canaryReceiptPresent : Bool
  observedEffectReceiptPresent : Bool
  monitorReceiptPresent : Bool
  rollbackOrCommitDispositionPresent : Bool
  exactInventoryRestorationPresent : Bool
  semanticRecoverySeparated : Bool
  descendantInvalidationPresent : Bool
  externalRemediationPresent : Bool
  compensationReceiptPresent : Bool
  incidentDisclosurePresent : Bool
  appendOnlyOutcomePresent : Bool
  noSupportPromotionRecorded : Bool
  noReleaseAuthorityRecorded : Bool
  materialChangeTriggerPresent : Bool
  affectedPathPresent : Bool
  readmissionDescendantInvalidationPresent : Bool
  ordinaryRouteBlocked : Bool
  staleGateExpirationPresent : Bool
  newStateInventoryPresent : Bool
  rerunRequirementPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure State where
  stage : Stage
  transitionId : Nat
  selfModelDigest : Nat
  consumerDigest : Nat
  mutablePartitionDigest : Nat
  protectedPartitionDigest : Nat
  authorityDigest : Nat
  objectiveDigest : Nat
  proposalDigest : Nat
  implementationDigest : Nat
  evaluatorDigest : Nat
  monitorDigest : Nat
  baselineDigest : Nat
  stateInventoryDigest : Nat
  replacementTransactionDigest : Nat
  residualDigest : Nat
  evidencePolicyDigest : Nat
  stopAuthorityDigest : Nat
  version : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  replacementHandoffCount : Nat
  outcomeReconciliationCount : Nat
  readmissionCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .draft => .scopeTransition | .scoped => .bindProposal
  | .proposalBound => .reviewImplementation | .implementationReviewed => .recordEvaluation
  | .evaluated => .adjudicateProposal | .adjudicated => .authorizeReplacementHandoff
  | .replacementBound => .reconcileReplacementOutcome
  | .outcomeReconciled => .triggerReadmission

def identityMatches (s : State) (p : Packet) : Bool :=   s.transitionId = p.transitionId && s.selfModelDigest = p.selfModelDigest &&
  s.consumerDigest = p.consumerDigest && s.mutablePartitionDigest = p.mutablePartitionDigest &&
  s.protectedPartitionDigest = p.protectedPartitionDigest && s.authorityDigest = p.authorityDigest &&
  s.objectiveDigest = p.objectiveDigest && s.proposalDigest = p.proposalDigest &&
  s.implementationDigest = p.implementationDigest && s.evaluatorDigest = p.evaluatorDigest &&
  s.monitorDigest = p.monitorDigest && s.baselineDigest = p.baselineDigest &&
  s.stateInventoryDigest = p.stateInventoryDigest &&
  s.replacementTransactionDigest = p.replacementTransactionDigest &&
  s.residualDigest = p.residualDigest && s.evidencePolicyDigest = p.evidencePolicyDigest &&
  s.stopAuthorityDigest = p.stopAuthorityDigest && s.version = p.currentVersion

def routeFor (s : State) (k : EventKind) (p : Packet) : Route :=   if k != expectedKind s.stage then .rejectWrongStage
  else if identityMatches s p = false then .rejectIdentitySubstitution
  else if p.eventDigest = s.lastEventDigest then .rejectReplay
  else if p.supportAssignmentRequested || p.externalEffectRequested then .rejectAuthorityLeak
  else match s.stage with
  | .draft =>
    if !p.consumerPresent then .requestConsumer else if !p.usePresent then .requestUse
    else if !p.selfModelPresent then .requestSelfModel else if !p.mutablePartitionPresent then .requestMutablePartition
    else if !p.protectedPartitionPresent then .requestProtectedPartition else if !p.authorityEnvelopePresent then .requestAuthorityEnvelope
    else if !p.optimizationTargetPresent then .requestOptimizationTarget else if !p.riskClassPresent then .requestRiskClass
    else if !p.evaluationHorizonPresent then .requestEvaluationHorizon else if !p.recursiveDepthPresent then .requestRecursiveDepth
    else if !p.stopAuthorityPresent then .requestStopAuthority else if !p.supportCeilingPresent then .requestSupportCeiling
    else if !p.stateInventoryPresent then .requestStateInventory else if !p.unknownStateResidualPresent then .requestUnknownStateResidual
    else if !p.rightsPremisesPresent then .requestRightsPremises else if !p.evaluatorPolicyPresent then .requestEvaluatorPolicy
    else if !p.baselinePolicyPresent then .requestBaselinePolicy else .acceptScope
  | .scoped =>
    if !p.proposalPresent then .requestProposal else if !p.changeIdentityPresent then .requestChangeIdentity
    else if !p.diffPresent then .requestDiff else if !p.lineagePresent then .requestLineage
    else if !p.dependenciesPresent then .requestDependencies else if !p.proposerPresent then .requestProposer
    else if !p.implementerPresent then .requestImplementer else if !p.mechanismPresent then .requestMechanism
    else if !p.expectedEffectsPresent then .requestExpectedEffects else if !p.nonGoalsPresent then .requestNonGoals
    else if !p.cheaperInterventionsPresent then .requestCheaperInterventions
    else if !p.noSelfRatifiedObjectiveRecorded then .rejectSelfRatifiedObjective else .acceptProposalBinding
  | .proposalBound =>
    if !p.implementationArtifactPresent then .requestImplementationArtifact
    else if !p.observedMutationSetPresent then .requestObservedMutationSet
    else if !p.protectedInvariantReviewPresent then .requestProtectedInvariantReview
    else if !p.boundaryDeltaReviewPresent then .requestBoundaryDeltaReview
    else if !p.authorityDeltaPresent then .requestAuthorityDelta else if !p.securityDeltaPresent then .requestSecurityDelta
    else if !p.dataPrivacyDeltaPresent then .requestDataPrivacyDelta else if !p.resourceDeltaPresent then .requestResourceDelta
    else if !p.evaluatorDeltaPresent then .requestEvaluatorDelta else if !p.rightsDeltaPresent then .requestRightsDelta
    else if !p.noProtectedWeakeningRecorded then .rejectProtectedWeakening
    else if !p.noAuthorityWideningRecorded then .rejectAuthorityWidening else .acceptImplementationReview
  | .implementationReviewed =>
    if !p.fullStateSnapshotPresent then .requestFullStateSnapshot else if !p.modelStatePresent then .requestModelState
    else if !p.optimizerStatePresent then .requestOptimizerState else if !p.schedulerStatePresent then .requestSchedulerState
    else if !p.rngStatePresent then .requestRngState else if !p.cacheStatePresent then .requestCacheState
    else if !p.promptPolicyStatePresent then .requestPromptPolicyState else if !p.toolCredentialStatePresent then .requestToolCredentialState
    else if !p.evaluatorBenchmarkStatePresent then .requestEvaluatorBenchmarkState else if !p.environmentStatePresent then .requestEnvironmentState
    else if !p.checkpointBackupStatePresent then .requestCheckpointBackupState else if !p.externalEffectStatePresent then .requestExternalEffectState
    else if !p.descendantStatePresent then .requestDescendantState else if !p.rollbackAuthorityPresent then .requestRollbackAuthority
    else if !p.compensationPlanPresent then .requestCompensationPlan else if !p.irreversibleResidualsPresent then .requestIrreversibleResiduals
    else .acceptStateBinding
  | .evaluated =>
    if !p.strongBaselinePresent then .requestStrongBaseline else if !p.naturalTaskDistributionPresent then .requestNaturalTaskDistribution
    else if !p.freshHoldoutPresent then .requestFreshHoldout else if !p.contaminationChecksPresent then .requestContaminationChecks
    else if !p.independentEvaluatorPresent then .requestIndependentEvaluator else if !p.evaluatorDependenciesPresent then .requestEvaluatorDependencies
    else if !p.independentMonitorPresent then .requestIndependentMonitor else if !p.monitorDependenciesPresent then .requestMonitorDependencies
    else if !p.usefulOutcomePresent then .requestUsefulOutcome else if !p.regressionsPresent then .requestRegressions
    else if !p.unsafeReleaseMeasurePresent then .requestUnsafeReleaseMeasure else if !p.deceptionProbePresent then .requestDeceptionProbe
    else if !p.delayedOutcomePresent then .requestDelayedOutcome else if !p.totalCostPresent then .requestTotalCost
    else if !p.evidenceBundlePresent then .requestEvidenceBundle else .acceptEvaluation
  | .adjudicated =>
    if !p.governanceApprovalPresent then .requestGovernanceApproval else if !p.evidenceTransitionPresent then .requestEvidenceTransition
    else if !p.permittedConsumerPresent then .requestPermittedConsumer else if !p.boundedScopePresent then .requestBoundedScope
    else if !p.trafficAllocationPresent then .requestTrafficAllocation else if !p.canaryPlanPresent then .requestCanaryPlan
    else if !p.monitorWindowPresent then .requestMonitorWindow else if !p.stopPathPresent then .requestStopPath
    else if !p.rollbackDryRunPresent then .requestRollbackDryRun else if !p.residualOwnerPresent then .requestResidualOwner
    else if !p.noCandidatePromotionAuthorityRecorded then .rejectCandidatePromotionAuthority else .acceptAdjudication
  | .replacementBound =>
    if !p.replacementTransactionPresent then .requestReplacementTransaction else if !p.transactionOwnerPresent then .requestTransactionOwner
    else if !p.canaryReceiptPresent then .requestCanaryReceipt else if !p.observedEffectReceiptPresent then .requestObservedEffectReceipt
    else if !p.monitorReceiptPresent then .requestMonitorReceipt else if !p.rollbackOrCommitDispositionPresent then .requestRollbackOrCommitDisposition
    else if !p.exactInventoryRestorationPresent then .requestExactInventoryRestoration
    else if !p.semanticRecoverySeparated then .requestSemanticRecoverySeparation
    else if !p.descendantInvalidationPresent then .requestDescendantInvalidation
    else if !p.externalRemediationPresent then .requestExternalRemediation else if !p.compensationReceiptPresent then .requestCompensationReceipt
    else if !p.incidentDisclosurePresent then .requestIncidentDisclosure else if !p.appendOnlyOutcomePresent then .requestAppendOnlyOutcome
    else if !p.noSupportPromotionRecorded then .rejectSupportPromotion else if !p.noReleaseAuthorityRecorded then .rejectReleaseAuthority
    else .acceptOutcomeReconciliation
  | .outcomeReconciled =>
    if !p.materialChangeTriggerPresent then .requestMaterialChangeTrigger else if !p.affectedPathPresent then .requestAffectedPath
    else if !p.readmissionDescendantInvalidationPresent then .requestReadmissionDescendantInvalidation
    else if !p.ordinaryRouteBlocked then .requestOrdinaryRouteBlock else if !p.staleGateExpirationPresent then .requestStaleGateExpiration
    else if !p.newStateInventoryPresent then .requestNewStateInventory else if !p.rerunRequirementPresent then .requestRerunRequirement
    else if p.successorVersion != s.version + 1 then .rejectSuccessorVersion else .acceptReadmission
def accepted : Route -> Bool
  | .acceptScope | .acceptProposalBinding | .acceptImplementationReview | .acceptStateBinding
  | .acceptEvaluation | .acceptAdjudication | .acceptOutcomeReconciliation | .acceptReadmission => true
  | _ => false

def nextStage : Stage -> Stage
  | .draft => .scoped | .scoped => .proposalBound | .proposalBound => .implementationReviewed
  | .implementationReviewed => .evaluated | .evaluated => .adjudicated
  | .adjudicated => .replacementBound | .replacementBound => .outcomeReconciled
  | .outcomeReconciled => .scoped

def canonicalPacket : Packet := {
  transitionId := 2101, selfModelDigest := 2102, consumerDigest := 2103,
  mutablePartitionDigest := 2104, protectedPartitionDigest := 2105, authorityDigest := 2106,
  objectiveDigest := 2107, proposalDigest := 2108, implementationDigest := 2109, evaluatorDigest := 2110,
  monitorDigest := 2111, baselineDigest := 2112, stateInventoryDigest := 2113,
  replacementTransactionDigest := 2114, residualDigest := 2115, evidencePolicyDigest := 2116,
  stopAuthorityDigest := 2117, currentVersion := 1, successorVersion := 1, eventDigest := 1,
  consumerPresent := true, usePresent := true, selfModelPresent := true, mutablePartitionPresent := true,
  protectedPartitionPresent := true, authorityEnvelopePresent := true, optimizationTargetPresent := true,
  riskClassPresent := true, evaluationHorizonPresent := true, recursiveDepthPresent := true,
  stopAuthorityPresent := true, supportCeilingPresent := true, stateInventoryPresent := true,
  unknownStateResidualPresent := true, rightsPremisesPresent := true, evaluatorPolicyPresent := true,
  baselinePolicyPresent := true, proposalPresent := true, changeIdentityPresent := true, diffPresent := true,
  lineagePresent := true, dependenciesPresent := true, proposerPresent := true, implementerPresent := true,
  mechanismPresent := true, expectedEffectsPresent := true, nonGoalsPresent := true,
  cheaperInterventionsPresent := true, noSelfRatifiedObjectiveRecorded := true,
  implementationArtifactPresent := true, observedMutationSetPresent := true,
  protectedInvariantReviewPresent := true, boundaryDeltaReviewPresent := true,
  authorityDeltaPresent := true, securityDeltaPresent := true, dataPrivacyDeltaPresent := true,
  resourceDeltaPresent := true, evaluatorDeltaPresent := true, rightsDeltaPresent := true,
  noProtectedWeakeningRecorded := true, noAuthorityWideningRecorded := true,
  fullStateSnapshotPresent := true, modelStatePresent := true, optimizerStatePresent := true,
  schedulerStatePresent := true, rngStatePresent := true, cacheStatePresent := true,
  promptPolicyStatePresent := true, toolCredentialStatePresent := true,
  evaluatorBenchmarkStatePresent := true, environmentStatePresent := true,
  checkpointBackupStatePresent := true, externalEffectStatePresent := true,
  descendantStatePresent := true, rollbackAuthorityPresent := true, compensationPlanPresent := true,
  irreversibleResidualsPresent := true, strongBaselinePresent := true,
  naturalTaskDistributionPresent := true, freshHoldoutPresent := true, contaminationChecksPresent := true,
  independentEvaluatorPresent := true, evaluatorDependenciesPresent := true,
  independentMonitorPresent := true, monitorDependenciesPresent := true, usefulOutcomePresent := true,
  regressionsPresent := true, unsafeReleaseMeasurePresent := true, deceptionProbePresent := true,
  delayedOutcomePresent := true, totalCostPresent := true, evidenceBundlePresent := true,
  governanceApprovalPresent := true, evidenceTransitionPresent := true, permittedConsumerPresent := true,
  boundedScopePresent := true, trafficAllocationPresent := true, canaryPlanPresent := true,
  monitorWindowPresent := true, stopPathPresent := true, rollbackDryRunPresent := true,
  residualOwnerPresent := true, noCandidatePromotionAuthorityRecorded := true,
  replacementTransactionPresent := true, transactionOwnerPresent := true, canaryReceiptPresent := true,
  observedEffectReceiptPresent := true, monitorReceiptPresent := true,
  rollbackOrCommitDispositionPresent := true, exactInventoryRestorationPresent := true,
  semanticRecoverySeparated := true, descendantInvalidationPresent := true,
  externalRemediationPresent := true, compensationReceiptPresent := true, incidentDisclosurePresent := true,
  appendOnlyOutcomePresent := true, noSupportPromotionRecorded := true, noReleaseAuthorityRecorded := true,
  materialChangeTriggerPresent := true, affectedPathPresent := true,
  readmissionDescendantInvalidationPresent := true, ordinaryRouteBlocked := true,
  staleGateExpirationPresent := true, newStateInventoryPresent := true, rerunRequirementPresent := true,
  supportAssignmentRequested := false, externalEffectRequested := false }

def canonicalState (stage : Stage) : State := {
  stage := stage, transitionId := 2101,
  selfModelDigest := 2102, consumerDigest := 2103, mutablePartitionDigest := 2104,
  protectedPartitionDigest := 2105, authorityDigest := 2106, objectiveDigest := 2107,
  proposalDigest := 2108, implementationDigest := 2109, evaluatorDigest := 2110,
  monitorDigest := 2111, baselineDigest := 2112, stateInventoryDigest := 2113,
  replacementTransactionDigest := 2114, residualDigest := 2115, evidencePolicyDigest := 2116,
  stopAuthorityDigest := 2117, version := 1, lastEventDigest := 0, receiptCount := 0,
  replacementHandoffCount := 0, outcomeReconciliationCount := 0, readmissionCount := 0,
  supportAssignmentCount := 0, externalEffectCount := 0 }

def applyEvent (s : State) (k : EventKind) (p : Packet) : State × Route :=
  let route := routeFor s k p
  if accepted route then
    ({ s with
       stage := nextStage s.stage
       version := if route = .acceptReadmission then p.successorVersion else s.version
       lastEventDigest := p.eventDigest
       receiptCount := s.receiptCount + 1
       replacementHandoffCount := s.replacementHandoffCount +
         (if route = .acceptAdjudication then 1 else 0)
       outcomeReconciliationCount := s.outcomeReconciliationCount +
         (if route = .acceptOutcomeReconciliation then 1 else 0)
       readmissionCount := s.readmissionCount + (if route = .acceptReadmission then 1 else 0) }, route)
  else (s, route)

def packetAt (version event successor : Nat) : Packet :=
  { canonicalPacket with
    currentVersion := version
    eventDigest := event
    successorVersion := successor }

def fullRun : State :=
  let s0 := canonicalState .draft
  let s1 := (applyEvent s0 .scopeTransition (packetAt 1 1 1)).1
  let s2 := (applyEvent s1 .bindProposal (packetAt 1 2 1)).1
  let s3 := (applyEvent s2 .reviewImplementation (packetAt 1 3 1)).1
  let s4 := (applyEvent s3 .recordEvaluation (packetAt 1 4 1)).1
  let s5 := (applyEvent s4 .adjudicateProposal (packetAt 1 5 1)).1
  let s6 := (applyEvent s5 .authorizeReplacementHandoff (packetAt 1 6 1)).1
  let s7 := (applyEvent s6 .reconcileReplacementOutcome (packetAt 1 7 1)).1
  (applyEvent s7 .triggerReadmission (packetAt 1 8 2)).1

theorem self_improvement_refinement_routes :
  routeFor (canonicalState .proposalBound) .reviewImplementation
      { canonicalPacket with noProtectedWeakeningRecorded := false } = .rejectProtectedWeakening ∧
  routeFor (canonicalState .proposalBound) .reviewImplementation
      { canonicalPacket with noAuthorityWideningRecorded := false } = .rejectAuthorityWidening ∧
  routeFor (canonicalState .evaluated) .adjudicateProposal
      { canonicalPacket with independentEvaluatorPresent := false } = .requestIndependentEvaluator ∧
  routeFor (canonicalState .replacementBound) .reconcileReplacementOutcome
      { canonicalPacket with descendantInvalidationPresent := false } = .requestDescendantInvalidation ∧
  routeFor (canonicalState .adjudicated) .authorizeReplacementHandoff canonicalPacket = .acceptAdjudication ∧
  routeFor (canonicalState .outcomeReconciled) .triggerReadmission
      { canonicalPacket with successorVersion := 2 } = .acceptReadmission := by native_decide

theorem self_improvement_full_lifecycle_witness :
    fullRun.stage = .scoped ∧ fullRun.version = 2 ∧ fullRun.receiptCount = 8 ∧
    fullRun.replacementHandoffCount = 1 ∧ fullRun.outcomeReconciliationCount = 1 ∧
    fullRun.readmissionCount = 1 ∧ fullRun.supportAssignmentCount = 0 ∧
    fullRun.externalEffectCount = 0 := by native_decide

end AsiStackProofs.SelfImprovementRefinement

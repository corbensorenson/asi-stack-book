namespace AsiStackProofs.OpenEndedImprovementRefinement

inductive Stage where
  | draft | scoped | generationBound | archiveBound | evaluated | adjudicated | governorBound
deriving DecidableEq, Repr

inductive EventKind where
  | scopeCampaign | bindGeneration | recordArchive | recordEvaluation
  | adjudicateCampaign | requestGovernorHandoff | triggerReadmission
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectIdentitySubstitution | rejectReplay | rejectAuthorityLeak
  | requestConsumer | requestPurpose | requestObjective | requestObjectiveLegitimacy
  | requestRepresentation | requestController | requestTaskPolicy | requestCandidatePolicy
  | requestEvaluatorPolicy | requestExposurePolicy | requestArchivePolicy | requestHazardPolicy
  | requestResourceBudget | requestOpportunityBudget | requestStopOwner | requestHorizon
  | requestSupportCeiling | acceptScope
  | requestTaskGenerator | requestCandidateGenerator | requestSeedParentMutationLineage
  | requestMatchedBaselines | requestTaskDenominator | requestCandidateDenominator
  | requestRetentionTiers | rejectControllerSelfRatification | acceptGenerationBinding
  | requestAttemptRecords | requestCandidateLineage | requestExposureRecords
  | requestResourceRecords | requestTypedDispositions | requestFailureHistory
  | requestNullUnsafeTimeoutRecords | requestPayloadCustody | rejectBudgetReset
  | requestArchiveSampling | acceptArchiveRecord
  | requestIndependentQualifier | requestQualifierDependencies | requestFreshHoldout
  | requestCalibration | requestDisagreementRecord | requestExposureAccounting
  | requestStrongBaseline | requestMechanismAblation | requestHazardProbe
  | requestSeparateUsefulnessTransfer | rejectScoreAsAdmission | acceptEvaluation
  | requestTotalCost | requestOpportunityCost | requestResidualOwner | requestCounterevidence
  | requestStopObservation | requestStopEffectReceipt | requestQuarantineEffectReceipt
  | requestRecoveryPath | rejectUsefulImprovementInference
  | rejectReleaseAuthorityLaundering | acceptAdjudication
  | requestPermittedConsumer | requestGovernorHandoffRecord | requestCandidateBinding
  | requestExpiry | requestMonitor | rejectCandidateAuthorityGrant
  | rejectSupportAuthorityLaundering | acceptGovernorHandoff
  | requestMaterialChangeTrigger | requestDescendantInvalidation
  | requestOrdinaryRouteBlock | requestCumulativeBudgetCarry
  | requestRerunRequirement | requestPayloadReceiptCustody
  | rejectSuccessorVersion | acceptReadmission
deriving DecidableEq, Repr

structure Packet where
  campaignId : Nat
  objectiveDigest : Nat
  representationDigest : Nat
  controllerDigest : Nat
  taskPolicyDigest : Nat
  candidatePolicyDigest : Nat
  generatorDigest : Nat
  evaluatorDigest : Nat
  qualifierDigest : Nat
  archiveDigest : Nat
  budgetDigest : Nat
  stopAuthorityDigest : Nat
  hazardPolicyDigest : Nat
  consumerDigest : Nat
  authorityDigest : Nat
  currentVersion : Nat
  successorVersion : Nat
  eventDigest : Nat
  consumerPresent : Bool
  purposePresent : Bool
  objectivePresent : Bool
  objectiveLegitimacyRecordPresent : Bool
  representationPresent : Bool
  controllerVersionPresent : Bool
  taskPolicyPresent : Bool
  candidatePolicyPresent : Bool
  evaluatorPolicyPresent : Bool
  exposurePolicyPresent : Bool
  archivePolicyPresent : Bool
  hazardPolicyPresent : Bool
  resourceBudgetPresent : Bool
  opportunityBudgetPresent : Bool
  stopOwnerPresent : Bool
  horizonPresent : Bool
  supportCeilingPresent : Bool
  taskGeneratorPresent : Bool
  candidateGeneratorPresent : Bool
  seedParentMutationLineagePresent : Bool
  matchedBaselinesPresent : Bool
  taskDenominatorComplete : Bool
  candidateDenominatorComplete : Bool
  retentionTiersPresent : Bool
  noControllerSelfRatificationRecorded : Bool
  attemptRecordsComplete : Bool
  candidateLineageComplete : Bool
  exposureRecordsComplete : Bool
  resourceRecordsComplete : Bool
  typedDispositionsComplete : Bool
  failureHistoryPreserved : Bool
  nullUnsafeTimeoutRecordsPreserved : Bool
  payloadCustodyPresent : Bool
  cumulativeBudgetAcrossDescendants : Bool
  archiveSamplingPresent : Bool
  independentQualifierPresent : Bool
  qualifierDependenciesPresent : Bool
  freshHoldoutPresent : Bool
  calibrationPresent : Bool
  disagreementRecordPresent : Bool
  evaluatorExposureAccounted : Bool
  strongBaselinePresent : Bool
  mechanismAblationPresent : Bool
  hazardProbePresent : Bool
  usefulnessTransferSeparated : Bool
  noScoreAsAdmissionRecorded : Bool
  totalCostPresent : Bool
  opportunityCostPresent : Bool
  residualOwnerPresent : Bool
  counterevidencePresent : Bool
  stopTriggerObserved : Bool
  stopEffectReceiptPresent : Bool
  quarantineEffectReceiptPresent : Bool
  recoveryPathPresent : Bool
  noUsefulImprovementInferenceRecorded : Bool
  noReleaseAuthorityRecorded : Bool
  permittedConsumerPresent : Bool
  governorHandoffRecordPresent : Bool
  candidateDigestBound : Bool
  expiryPresent : Bool
  monitorPresent : Bool
  noCandidateAuthorityGrantRecorded : Bool
  noSupportAuthorityRecorded : Bool
  materialChangeTriggerPresent : Bool
  descendantInvalidationComplete : Bool
  ordinaryRouteBlocked : Bool
  cumulativeBudgetCarried : Bool
  rerunRequirementPresent : Bool
  payloadReceiptCustodyPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure State where
  stage : Stage
  campaignId : Nat
  objectiveDigest : Nat
  representationDigest : Nat
  controllerDigest : Nat
  taskPolicyDigest : Nat
  candidatePolicyDigest : Nat
  generatorDigest : Nat
  evaluatorDigest : Nat
  qualifierDigest : Nat
  archiveDigest : Nat
  budgetDigest : Nat
  stopAuthorityDigest : Nat
  hazardPolicyDigest : Nat
  consumerDigest : Nat
  authorityDigest : Nat
  version : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  governorHandoffCount : Nat
  readmissionCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .draft => .scopeCampaign
  | .scoped => .bindGeneration
  | .generationBound => .recordArchive
  | .archiveBound => .recordEvaluation
  | .evaluated => .adjudicateCampaign
  | .adjudicated => .requestGovernorHandoff
  | .governorBound => .triggerReadmission

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.campaignId = packet.campaignId && state.objectiveDigest = packet.objectiveDigest &&
  state.representationDigest = packet.representationDigest &&
  state.controllerDigest = packet.controllerDigest &&
  state.taskPolicyDigest = packet.taskPolicyDigest &&
  state.candidatePolicyDigest = packet.candidatePolicyDigest &&
  state.generatorDigest = packet.generatorDigest && state.evaluatorDigest = packet.evaluatorDigest &&
  state.qualifierDigest = packet.qualifierDigest && state.archiveDigest = packet.archiveDigest &&
  state.budgetDigest = packet.budgetDigest &&
  state.stopAuthorityDigest = packet.stopAuthorityDigest &&
  state.hazardPolicyDigest = packet.hazardPolicyDigest &&
  state.consumerDigest = packet.consumerDigest && state.authorityDigest = packet.authorityDigest &&
  state.version = packet.currentVersion

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if kind != expectedKind state.stage then .rejectWrongStage
  else if identityMatches state packet = false then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectReplay
  else if packet.supportAssignmentRequested || packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .draft =>
      if packet.consumerPresent = false then .requestConsumer
      else if packet.purposePresent = false then .requestPurpose
      else if packet.objectivePresent = false then .requestObjective
      else if packet.objectiveLegitimacyRecordPresent = false then .requestObjectiveLegitimacy
      else if packet.representationPresent = false then .requestRepresentation
      else if packet.controllerVersionPresent = false then .requestController
      else if packet.taskPolicyPresent = false then .requestTaskPolicy
      else if packet.candidatePolicyPresent = false then .requestCandidatePolicy
      else if packet.evaluatorPolicyPresent = false then .requestEvaluatorPolicy
      else if packet.exposurePolicyPresent = false then .requestExposurePolicy
      else if packet.archivePolicyPresent = false then .requestArchivePolicy
      else if packet.hazardPolicyPresent = false then .requestHazardPolicy
      else if packet.resourceBudgetPresent = false then .requestResourceBudget
      else if packet.opportunityBudgetPresent = false then .requestOpportunityBudget
      else if packet.stopOwnerPresent = false then .requestStopOwner
      else if packet.horizonPresent = false then .requestHorizon
      else if packet.supportCeilingPresent = false then .requestSupportCeiling
      else .acceptScope
  | .scoped =>
      if packet.taskGeneratorPresent = false then .requestTaskGenerator
      else if packet.candidateGeneratorPresent = false then .requestCandidateGenerator
      else if packet.seedParentMutationLineagePresent = false then .requestSeedParentMutationLineage
      else if packet.matchedBaselinesPresent = false then .requestMatchedBaselines
      else if packet.taskDenominatorComplete = false then .requestTaskDenominator
      else if packet.candidateDenominatorComplete = false then .requestCandidateDenominator
      else if packet.retentionTiersPresent = false then .requestRetentionTiers
      else if packet.noControllerSelfRatificationRecorded = false then .rejectControllerSelfRatification
      else .acceptGenerationBinding
  | .generationBound =>
      if packet.attemptRecordsComplete = false then .requestAttemptRecords
      else if packet.candidateLineageComplete = false then .requestCandidateLineage
      else if packet.exposureRecordsComplete = false then .requestExposureRecords
      else if packet.resourceRecordsComplete = false then .requestResourceRecords
      else if packet.typedDispositionsComplete = false then .requestTypedDispositions
      else if packet.failureHistoryPreserved = false then .requestFailureHistory
      else if packet.nullUnsafeTimeoutRecordsPreserved = false then .requestNullUnsafeTimeoutRecords
      else if packet.payloadCustodyPresent = false then .requestPayloadCustody
      else if packet.cumulativeBudgetAcrossDescendants = false then .rejectBudgetReset
      else if packet.archiveSamplingPresent = false then .requestArchiveSampling
      else .acceptArchiveRecord
  | .archiveBound =>
      if packet.independentQualifierPresent = false then .requestIndependentQualifier
      else if packet.qualifierDependenciesPresent = false then .requestQualifierDependencies
      else if packet.freshHoldoutPresent = false then .requestFreshHoldout
      else if packet.calibrationPresent = false then .requestCalibration
      else if packet.disagreementRecordPresent = false then .requestDisagreementRecord
      else if packet.evaluatorExposureAccounted = false then .requestExposureAccounting
      else if packet.strongBaselinePresent = false then .requestStrongBaseline
      else if packet.mechanismAblationPresent = false then .requestMechanismAblation
      else if packet.hazardProbePresent = false then .requestHazardProbe
      else if packet.usefulnessTransferSeparated = false then .requestSeparateUsefulnessTransfer
      else if packet.noScoreAsAdmissionRecorded = false then .rejectScoreAsAdmission
      else .acceptEvaluation
  | .evaluated =>
      if packet.totalCostPresent = false then .requestTotalCost
      else if packet.opportunityCostPresent = false then .requestOpportunityCost
      else if packet.residualOwnerPresent = false then .requestResidualOwner
      else if packet.counterevidencePresent = false then .requestCounterevidence
      else if packet.stopTriggerObserved = false then .requestStopObservation
      else if packet.stopEffectReceiptPresent = false then .requestStopEffectReceipt
      else if packet.quarantineEffectReceiptPresent = false then .requestQuarantineEffectReceipt
      else if packet.recoveryPathPresent = false then .requestRecoveryPath
      else if packet.noUsefulImprovementInferenceRecorded = false then .rejectUsefulImprovementInference
      else if packet.noReleaseAuthorityRecorded = false then .rejectReleaseAuthorityLaundering
      else .acceptAdjudication
  | .adjudicated =>
      if packet.permittedConsumerPresent = false then .requestPermittedConsumer
      else if packet.governorHandoffRecordPresent = false then .requestGovernorHandoffRecord
      else if packet.candidateDigestBound = false then .requestCandidateBinding
      else if packet.expiryPresent = false then .requestExpiry
      else if packet.monitorPresent = false then .requestMonitor
      else if packet.noCandidateAuthorityGrantRecorded = false then .rejectCandidateAuthorityGrant
      else if packet.noSupportAuthorityRecorded = false then .rejectSupportAuthorityLaundering
      else .acceptGovernorHandoff
  | .governorBound =>
      if packet.materialChangeTriggerPresent = false then .requestMaterialChangeTrigger
      else if packet.descendantInvalidationComplete = false then .requestDescendantInvalidation
      else if packet.ordinaryRouteBlocked = false then .requestOrdinaryRouteBlock
      else if packet.cumulativeBudgetCarried = false then .requestCumulativeBudgetCarry
      else if packet.rerunRequirementPresent = false then .requestRerunRequirement
      else if packet.payloadReceiptCustodyPresent = false then .requestPayloadReceiptCustody
      else if packet.successorVersion != state.version + 1 then .rejectSuccessorVersion
      else .acceptReadmission

def accepted : Route -> Bool
  | .acceptScope | .acceptGenerationBinding | .acceptArchiveRecord | .acceptEvaluation
  | .acceptAdjudication | .acceptGovernorHandoff | .acceptReadmission => true
  | _ => false

def nextStage : Stage -> Stage
  | .draft => .scoped
  | .scoped => .generationBound
  | .generationBound => .archiveBound
  | .archiveBound => .evaluated
  | .evaluated => .adjudicated
  | .adjudicated => .governorBound
  | .governorBound => .scoped

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       version := if route = .acceptReadmission then packet.successorVersion else state.version
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       governorHandoffCount := state.governorHandoffCount +
         (if route = .acceptGovernorHandoff then 1 else 0)
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
  campaignId := 1201, objectiveDigest := 1202, representationDigest := 1203,
  controllerDigest := 1204, taskPolicyDigest := 1205, candidatePolicyDigest := 1206,
  generatorDigest := 1207, evaluatorDigest := 1208, qualifierDigest := 1209,
  archiveDigest := 1210, budgetDigest := 1211, stopAuthorityDigest := 1212,
  hazardPolicyDigest := 1213, consumerDigest := 1214, authorityDigest := 1215,
  currentVersion := 1, successorVersion := 1, eventDigest := 1,
  consumerPresent := true, purposePresent := true, objectivePresent := true,
  objectiveLegitimacyRecordPresent := true, representationPresent := true,
  controllerVersionPresent := true, taskPolicyPresent := true, candidatePolicyPresent := true,
  evaluatorPolicyPresent := true, exposurePolicyPresent := true, archivePolicyPresent := true,
  hazardPolicyPresent := true, resourceBudgetPresent := true, opportunityBudgetPresent := true,
  stopOwnerPresent := true, horizonPresent := true, supportCeilingPresent := true,
  taskGeneratorPresent := true, candidateGeneratorPresent := true,
  seedParentMutationLineagePresent := true, matchedBaselinesPresent := true,
  taskDenominatorComplete := true, candidateDenominatorComplete := true,
  retentionTiersPresent := true, noControllerSelfRatificationRecorded := true,
  attemptRecordsComplete := true, candidateLineageComplete := true,
  exposureRecordsComplete := true, resourceRecordsComplete := true,
  typedDispositionsComplete := true, failureHistoryPreserved := true,
  nullUnsafeTimeoutRecordsPreserved := true, payloadCustodyPresent := true,
  cumulativeBudgetAcrossDescendants := true, archiveSamplingPresent := true,
  independentQualifierPresent := true, qualifierDependenciesPresent := true,
  freshHoldoutPresent := true, calibrationPresent := true, disagreementRecordPresent := true,
  evaluatorExposureAccounted := true, strongBaselinePresent := true,
  mechanismAblationPresent := true, hazardProbePresent := true,
  usefulnessTransferSeparated := true, noScoreAsAdmissionRecorded := true,
  totalCostPresent := true, opportunityCostPresent := true, residualOwnerPresent := true,
  counterevidencePresent := true, stopTriggerObserved := true, stopEffectReceiptPresent := true,
  quarantineEffectReceiptPresent := true, recoveryPathPresent := true,
  noUsefulImprovementInferenceRecorded := true, noReleaseAuthorityRecorded := true,
  permittedConsumerPresent := true, governorHandoffRecordPresent := true,
  candidateDigestBound := true, expiryPresent := true, monitorPresent := true,
  noCandidateAuthorityGrantRecorded := true, noSupportAuthorityRecorded := true,
  materialChangeTriggerPresent := true, descendantInvalidationComplete := true,
  ordinaryRouteBlocked := true, cumulativeBudgetCarried := true,
  rerunRequirementPresent := true, payloadReceiptCustodyPresent := true,
  supportAssignmentRequested := false, externalEffectRequested := false }

def canonicalState (stage : Stage) : State := {
  stage := stage, campaignId := 1201, objectiveDigest := 1202,
  representationDigest := 1203, controllerDigest := 1204, taskPolicyDigest := 1205,
  candidatePolicyDigest := 1206, generatorDigest := 1207, evaluatorDigest := 1208,
  qualifierDigest := 1209, archiveDigest := 1210, budgetDigest := 1211,
  stopAuthorityDigest := 1212, hazardPolicyDigest := 1213, consumerDigest := 1214,
  authorityDigest := 1215, version := 1, lastEventDigest := 0, receiptCount := 0,
  governorHandoffCount := 0, readmissionCount := 0, supportAssignmentCount := 0,
  externalEffectCount := 0 }

def canonicalLifecycleState : State :=
  let s1 := (applyEvent (canonicalState .draft) .scopeCampaign
    { canonicalPacket with eventDigest := 1 }).1
  let s2 := (applyEvent s1 .bindGeneration
    { canonicalPacket with eventDigest := 2 }).1
  let s3 := (applyEvent s2 .recordArchive
    { canonicalPacket with eventDigest := 3 }).1
  let s4 := (applyEvent s3 .recordEvaluation
    { canonicalPacket with eventDigest := 4 }).1
  let s5 := (applyEvent s4 .adjudicateCampaign
    { canonicalPacket with eventDigest := 5 }).1
  let s6 := (applyEvent s5 .requestGovernorHandoff
    { canonicalPacket with eventDigest := 6 }).1
  (applyEvent s6 .triggerReadmission
    { canonicalPacket with eventDigest := 7, successorVersion := 2 }).1

def budgetResetBlockedLifecycleState : State :=
  let s1 := (applyEvent (canonicalState .draft) .scopeCampaign
    { canonicalPacket with eventDigest := 1 }).1
  let s2 := (applyEvent s1 .bindGeneration
    { canonicalPacket with eventDigest := 2 }).1
  let s3 := (applyEvent s2 .recordArchive
    { canonicalPacket with eventDigest := 3, cumulativeBudgetAcrossDescendants := false }).1
  let s4 := (applyEvent s3 .recordEvaluation
    { canonicalPacket with eventDigest := 4 }).1
  let s5 := (applyEvent s4 .adjudicateCampaign
    { canonicalPacket with eventDigest := 5 }).1
  let s6 := (applyEvent s5 .requestGovernorHandoff
    { canonicalPacket with eventDigest := 6 }).1
  (applyEvent s6 .triggerReadmission
    { canonicalPacket with eventDigest := 7, successorVersion := 2 }).1

theorem open_ended_improvement_full_cycle_composes :
    canonicalLifecycleState.stage = .scoped ∧
    canonicalLifecycleState.version = 2 ∧
    canonicalLifecycleState.receiptCount = 7 ∧
    canonicalLifecycleState.governorHandoffCount = 1 ∧
    canonicalLifecycleState.readmissionCount = 1 ∧
    canonicalLifecycleState.supportAssignmentCount = 0 ∧
    canonicalLifecycleState.externalEffectCount = 0 := by native_decide

theorem open_ended_improvement_budget_reset_blocks_handoff_and_readmission :
    budgetResetBlockedLifecycleState.stage = .generationBound ∧
    budgetResetBlockedLifecycleState.version = 1 ∧
    budgetResetBlockedLifecycleState.receiptCount = 2 ∧
    budgetResetBlockedLifecycleState.governorHandoffCount = 0 ∧
    budgetResetBlockedLifecycleState.readmissionCount = 0 ∧
    budgetResetBlockedLifecycleState.supportAssignmentCount = 0 ∧
    budgetResetBlockedLifecycleState.externalEffectCount = 0 := by native_decide

theorem open_ended_improvement_lifecycle_routes :
    routeFor (canonicalState .archiveBound) .recordEvaluation
        { canonicalPacket with independentQualifierPresent := false } =
          .requestIndependentQualifier ∧
    routeFor (canonicalState .generationBound) .recordArchive
        { canonicalPacket with failureHistoryPreserved := false } = .requestFailureHistory ∧
    routeFor (canonicalState .generationBound) .recordArchive
        { canonicalPacket with cumulativeBudgetAcrossDescendants := false } = .rejectBudgetReset ∧
    routeFor (canonicalState .evaluated) .adjudicateCampaign
        { canonicalPacket with stopEffectReceiptPresent := false } = .requestStopEffectReceipt ∧
    routeFor (canonicalState .adjudicated) .requestGovernorHandoff
        { canonicalPacket with noCandidateAuthorityGrantRecorded := false } =
          .rejectCandidateAuthorityGrant ∧
    routeFor (canonicalState .adjudicated) .requestGovernorHandoff canonicalPacket =
        .acceptGovernorHandoff ∧
    routeFor (canonicalState .governorBound) .triggerReadmission
        { canonicalPacket with successorVersion := 2 } = .acceptReadmission := by native_decide

end AsiStackProofs.OpenEndedImprovementRefinement

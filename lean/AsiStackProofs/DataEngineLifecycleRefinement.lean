namespace AsiStackProofs.DataEngineLifecycleRefinement

inductive Stage where
  | draft | scoped | admitted | stateBound | updated | deletionAssessed | adjudicated | custodyBound
deriving DecidableEq, Repr

inductive EventKind where
  | scopeCustody | admitData | bindFullState | recordUpdate
  | assessDeletion | adjudicateClaims | bindCustody | triggerReadmission
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectIdentitySubstitution | rejectReplay | rejectAuthorityLeak
  | requestDatum | requestCohort | requestProvenance | requestRights
  | requestAuthority | requestConsumer | requestRiskTier | requestScope | acceptScope
  | requestSplitExclusions | requestContaminationCheck | requestRetention
  | requestDeletionScope | requestTransformationLineage | requestSyntheticLineage
  | requestEvaluationExclusions | requestCoverageResidual | requestDistributionResidual
  | requestExpiry | acceptAdmission
  | requestModelState | requestOptimizerState | requestSchedulerState | requestRngState
  | requestCacheState | requestBackupState | requestDescendantState
  | requestCheckpointAuthority | requestPreStateDigest | requestSelectionRule | acceptStateBinding
  | requestUpdateDisposition | requestSelectedCheckpoint | requestCompleteDenominator
  | requestFailureLog | requestCostRecord | requestBestFinalRecord
  | requestRollbackReceipt | rejectDeclaredSurfaceRollbackMismatch
  | requestDescendantInvalidation | rejectSupportAuthorityLaundering | acceptUpdateRecord
  | requestDeletionRequest | requestAffectedCohort | requestPropagationRecord
  | requestReplicaBackupRecord | requestExternalDescendantResidual
  | requestBehavioralStatus | requestInfluenceStatus | requestPrivacyStatus
  | requestStorageStatus | requestLegalStatus | acceptDeletionAssessment
  | requestAxisSeparation | rejectBehaviorAsInfluence | rejectBehaviorAsPrivacy
  | rejectLineageAsStorage | requestUncertainty | requestResidualOwner
  | requestCounterevidence | rejectErasureInference | rejectReleaseAuthorityLaundering
  | acceptClaimAdjudication
  | requestPermittedConsumer | requestBoundedCustodyRecord | requestDatasetCheckpointBinding
  | requestCustodyExpiry | requestMonitor | requestRevocationPath
  | rejectCustodySupportLaundering | acceptBoundedCustody
  | requestMaterialChangeTrigger | requestCompleteInvalidation
  | requestOrdinaryRouteBlock | requestRerunRequirement
  | requestRollbackOrRevocationReceipt | rejectSuccessorVersion | acceptReadmission
deriving DecidableEq, Repr

structure Packet where
  datumDigest : Nat
  cohortDigest : Nat
  provenanceDigest : Nat
  rightsDigest : Nat
  authorityDigest : Nat
  splitDigest : Nat
  datasetDigest : Nat
  modelDigest : Nat
  baseCheckpointDigest : Nat
  selectedCheckpointDigest : Nat
  optimizerDigest : Nat
  schedulerDigest : Nat
  rngDigest : Nat
  cacheDigest : Nat
  backupDigest : Nat
  lineageDigest : Nat
  descendantDigest : Nat
  deletionRequestDigest : Nat
  evaluatorDigest : Nat
  consumerDigest : Nat
  currentVersion : Nat
  successorVersion : Nat
  eventDigest : Nat
  datumPresent : Bool
  cohortPresent : Bool
  provenancePresent : Bool
  rightsPresent : Bool
  authorityPresent : Bool
  consumerPresent : Bool
  riskTierPresent : Bool
  scopePresent : Bool
  splitExclusionsPresent : Bool
  contaminationCheckPresent : Bool
  retentionPresent : Bool
  deletionScopePresent : Bool
  transformationLineagePresent : Bool
  syntheticLineagePresent : Bool
  evaluationExclusionsPresent : Bool
  coverageResidualPresent : Bool
  distributionResidualPresent : Bool
  expiryPresent : Bool
  modelStatePresent : Bool
  optimizerStatePresent : Bool
  schedulerStatePresent : Bool
  rngStatePresent : Bool
  cacheStatePresent : Bool
  backupStatePresent : Bool
  descendantStatePresent : Bool
  checkpointAuthorityPresent : Bool
  preStateDigestPresent : Bool
  selectionRulePresent : Bool
  updateDispositionPresent : Bool
  selectedCheckpointPresent : Bool
  completeDenominatorPresent : Bool
  failureLogPresent : Bool
  costRecordPresent : Bool
  bestFinalRecordPresent : Bool
  rollbackReceiptPresent : Bool
  declaredSurfaceRollbackExact : Bool
  descendantInvalidationPresent : Bool
  noSupportAuthorityRecorded : Bool
  deletionRequestPresent : Bool
  affectedCohortPresent : Bool
  propagationRecordPresent : Bool
  replicaBackupRecordPresent : Bool
  externalDescendantResidualPresent : Bool
  behavioralStatusPresent : Bool
  influenceStatusPresent : Bool
  privacyStatusPresent : Bool
  storageStatusPresent : Bool
  legalStatusPresent : Bool
  axesSeparated : Bool
  behaviorUsedAsInfluenceEvidence : Bool
  behaviorUsedAsPrivacyEvidence : Bool
  lineageUsedAsStorageEvidence : Bool
  uncertaintyPresent : Bool
  residualOwnerPresent : Bool
  counterevidencePresent : Bool
  noErasureInferenceRecorded : Bool
  noReleaseAuthorityRecorded : Bool
  permittedConsumerPresent : Bool
  boundedCustodyRecordPresent : Bool
  datasetCheckpointBound : Bool
  custodyExpiryPresent : Bool
  monitorPresent : Bool
  revocationPathPresent : Bool
  noCustodySupportAuthorityRecorded : Bool
  materialChangeTriggerPresent : Bool
  completeInvalidationPresent : Bool
  ordinaryRouteBlocked : Bool
  rerunRequirementPresent : Bool
  rollbackOrRevocationReceiptPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure State where
  stage : Stage
  datumDigest : Nat
  cohortDigest : Nat
  provenanceDigest : Nat
  rightsDigest : Nat
  authorityDigest : Nat
  splitDigest : Nat
  datasetDigest : Nat
  modelDigest : Nat
  baseCheckpointDigest : Nat
  selectedCheckpointDigest : Nat
  optimizerDigest : Nat
  schedulerDigest : Nat
  rngDigest : Nat
  cacheDigest : Nat
  backupDigest : Nat
  lineageDigest : Nat
  descendantDigest : Nat
  deletionRequestDigest : Nat
  evaluatorDigest : Nat
  consumerDigest : Nat
  version : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  boundedCustodyCount : Nat
  readmissionCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .draft => .scopeCustody
  | .scoped => .admitData
  | .admitted => .bindFullState
  | .stateBound => .recordUpdate
  | .updated => .assessDeletion
  | .deletionAssessed => .adjudicateClaims
  | .adjudicated => .bindCustody
  | .custodyBound => .triggerReadmission

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.datumDigest = packet.datumDigest && state.cohortDigest = packet.cohortDigest &&
  state.provenanceDigest = packet.provenanceDigest && state.rightsDigest = packet.rightsDigest &&
  state.authorityDigest = packet.authorityDigest && state.splitDigest = packet.splitDigest &&
  state.datasetDigest = packet.datasetDigest && state.modelDigest = packet.modelDigest &&
  state.baseCheckpointDigest = packet.baseCheckpointDigest &&
  state.selectedCheckpointDigest = packet.selectedCheckpointDigest &&
  state.optimizerDigest = packet.optimizerDigest && state.schedulerDigest = packet.schedulerDigest &&
  state.rngDigest = packet.rngDigest && state.cacheDigest = packet.cacheDigest &&
  state.backupDigest = packet.backupDigest && state.lineageDigest = packet.lineageDigest &&
  state.descendantDigest = packet.descendantDigest &&
  state.deletionRequestDigest = packet.deletionRequestDigest &&
  state.evaluatorDigest = packet.evaluatorDigest && state.consumerDigest = packet.consumerDigest &&
  state.version = packet.currentVersion

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if kind != expectedKind state.stage then .rejectWrongStage
  else if identityMatches state packet = false then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectReplay
  else if packet.supportAssignmentRequested || packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .draft =>
      if packet.datumPresent = false then .requestDatum
      else if packet.cohortPresent = false then .requestCohort
      else if packet.provenancePresent = false then .requestProvenance
      else if packet.rightsPresent = false then .requestRights
      else if packet.authorityPresent = false then .requestAuthority
      else if packet.consumerPresent = false then .requestConsumer
      else if packet.riskTierPresent = false then .requestRiskTier
      else if packet.scopePresent = false then .requestScope
      else .acceptScope
  | .scoped =>
      if packet.splitExclusionsPresent = false then .requestSplitExclusions
      else if packet.contaminationCheckPresent = false then .requestContaminationCheck
      else if packet.retentionPresent = false then .requestRetention
      else if packet.deletionScopePresent = false then .requestDeletionScope
      else if packet.transformationLineagePresent = false then .requestTransformationLineage
      else if packet.syntheticLineagePresent = false then .requestSyntheticLineage
      else if packet.evaluationExclusionsPresent = false then .requestEvaluationExclusions
      else if packet.coverageResidualPresent = false then .requestCoverageResidual
      else if packet.distributionResidualPresent = false then .requestDistributionResidual
      else if packet.expiryPresent = false then .requestExpiry
      else .acceptAdmission
  | .admitted =>
      if packet.modelStatePresent = false then .requestModelState
      else if packet.optimizerStatePresent = false then .requestOptimizerState
      else if packet.schedulerStatePresent = false then .requestSchedulerState
      else if packet.rngStatePresent = false then .requestRngState
      else if packet.cacheStatePresent = false then .requestCacheState
      else if packet.backupStatePresent = false then .requestBackupState
      else if packet.descendantStatePresent = false then .requestDescendantState
      else if packet.checkpointAuthorityPresent = false then .requestCheckpointAuthority
      else if packet.preStateDigestPresent = false then .requestPreStateDigest
      else if packet.selectionRulePresent = false then .requestSelectionRule
      else .acceptStateBinding
  | .stateBound =>
      if packet.updateDispositionPresent = false then .requestUpdateDisposition
      else if packet.selectedCheckpointPresent = false then .requestSelectedCheckpoint
      else if packet.completeDenominatorPresent = false then .requestCompleteDenominator
      else if packet.failureLogPresent = false then .requestFailureLog
      else if packet.costRecordPresent = false then .requestCostRecord
      else if packet.bestFinalRecordPresent = false then .requestBestFinalRecord
      else if packet.rollbackReceiptPresent = false then .requestRollbackReceipt
      else if packet.declaredSurfaceRollbackExact = false then .rejectDeclaredSurfaceRollbackMismatch
      else if packet.descendantInvalidationPresent = false then .requestDescendantInvalidation
      else if packet.noSupportAuthorityRecorded = false then .rejectSupportAuthorityLaundering
      else .acceptUpdateRecord
  | .updated =>
      if packet.deletionRequestPresent = false then .requestDeletionRequest
      else if packet.affectedCohortPresent = false then .requestAffectedCohort
      else if packet.propagationRecordPresent = false then .requestPropagationRecord
      else if packet.replicaBackupRecordPresent = false then .requestReplicaBackupRecord
      else if packet.externalDescendantResidualPresent = false then .requestExternalDescendantResidual
      else if packet.behavioralStatusPresent = false then .requestBehavioralStatus
      else if packet.influenceStatusPresent = false then .requestInfluenceStatus
      else if packet.privacyStatusPresent = false then .requestPrivacyStatus
      else if packet.storageStatusPresent = false then .requestStorageStatus
      else if packet.legalStatusPresent = false then .requestLegalStatus
      else .acceptDeletionAssessment
  | .deletionAssessed =>
      if packet.axesSeparated = false then .requestAxisSeparation
      else if packet.behaviorUsedAsInfluenceEvidence then .rejectBehaviorAsInfluence
      else if packet.behaviorUsedAsPrivacyEvidence then .rejectBehaviorAsPrivacy
      else if packet.lineageUsedAsStorageEvidence then .rejectLineageAsStorage
      else if packet.uncertaintyPresent = false then .requestUncertainty
      else if packet.residualOwnerPresent = false then .requestResidualOwner
      else if packet.counterevidencePresent = false then .requestCounterevidence
      else if packet.noErasureInferenceRecorded = false then .rejectErasureInference
      else if packet.noReleaseAuthorityRecorded = false then .rejectReleaseAuthorityLaundering
      else .acceptClaimAdjudication
  | .adjudicated =>
      if packet.permittedConsumerPresent = false then .requestPermittedConsumer
      else if packet.boundedCustodyRecordPresent = false then .requestBoundedCustodyRecord
      else if packet.datasetCheckpointBound = false then .requestDatasetCheckpointBinding
      else if packet.custodyExpiryPresent = false then .requestCustodyExpiry
      else if packet.monitorPresent = false then .requestMonitor
      else if packet.revocationPathPresent = false then .requestRevocationPath
      else if packet.noCustodySupportAuthorityRecorded = false then .rejectCustodySupportLaundering
      else .acceptBoundedCustody
  | .custodyBound =>
      if packet.materialChangeTriggerPresent = false then .requestMaterialChangeTrigger
      else if packet.completeInvalidationPresent = false then .requestCompleteInvalidation
      else if packet.ordinaryRouteBlocked = false then .requestOrdinaryRouteBlock
      else if packet.rerunRequirementPresent = false then .requestRerunRequirement
      else if packet.rollbackOrRevocationReceiptPresent = false then .requestRollbackOrRevocationReceipt
      else if packet.successorVersion != state.version + 1 then .rejectSuccessorVersion
      else .acceptReadmission

def accepted : Route -> Bool
  | .acceptScope | .acceptAdmission | .acceptStateBinding | .acceptUpdateRecord
  | .acceptDeletionAssessment | .acceptClaimAdjudication | .acceptBoundedCustody
  | .acceptReadmission => true
  | _ => false

def nextStage : Stage -> Stage
  | .draft => .scoped
  | .scoped => .admitted
  | .admitted => .stateBound
  | .stateBound => .updated
  | .updated => .deletionAssessed
  | .deletionAssessed => .adjudicated
  | .adjudicated => .custodyBound
  | .custodyBound => .scoped

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       version := if route = .acceptReadmission then packet.successorVersion else state.version
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       boundedCustodyCount := state.boundedCustodyCount +
         (if route = .acceptBoundedCustody then 1 else 0)
       readmissionCount := state.readmissionCount + (if route = .acceptReadmission then 1 else 0) }, route)
  else (state, route)

def canonicalPacket : Packet := {
  datumDigest := 1001, cohortDigest := 1002, provenanceDigest := 1003,
  rightsDigest := 1004, authorityDigest := 1005, splitDigest := 1006,
  datasetDigest := 1007, modelDigest := 1008, baseCheckpointDigest := 1009,
  selectedCheckpointDigest := 1010, optimizerDigest := 1011, schedulerDigest := 1012,
  rngDigest := 1013, cacheDigest := 1014, backupDigest := 1015,
  lineageDigest := 1016, descendantDigest := 1017, deletionRequestDigest := 1018,
  evaluatorDigest := 1019, consumerDigest := 1020, currentVersion := 1,
  successorVersion := 1, eventDigest := 1, datumPresent := true, cohortPresent := true,
  provenancePresent := true, rightsPresent := true, authorityPresent := true,
  consumerPresent := true, riskTierPresent := true, scopePresent := true,
  splitExclusionsPresent := true, contaminationCheckPresent := true,
  retentionPresent := true, deletionScopePresent := true,
  transformationLineagePresent := true, syntheticLineagePresent := true,
  evaluationExclusionsPresent := true, coverageResidualPresent := true,
  distributionResidualPresent := true, expiryPresent := true, modelStatePresent := true,
  optimizerStatePresent := true, schedulerStatePresent := true, rngStatePresent := true,
  cacheStatePresent := true, backupStatePresent := true, descendantStatePresent := true,
  checkpointAuthorityPresent := true, preStateDigestPresent := true,
  selectionRulePresent := true, updateDispositionPresent := true,
  selectedCheckpointPresent := true, completeDenominatorPresent := true,
  failureLogPresent := true, costRecordPresent := true, bestFinalRecordPresent := true,
  rollbackReceiptPresent := true, declaredSurfaceRollbackExact := true,
  descendantInvalidationPresent := true, noSupportAuthorityRecorded := true,
  deletionRequestPresent := true, affectedCohortPresent := true,
  propagationRecordPresent := true, replicaBackupRecordPresent := true,
  externalDescendantResidualPresent := true, behavioralStatusPresent := true,
  influenceStatusPresent := true, privacyStatusPresent := true, storageStatusPresent := true,
  legalStatusPresent := true, axesSeparated := true,
  behaviorUsedAsInfluenceEvidence := false, behaviorUsedAsPrivacyEvidence := false,
  lineageUsedAsStorageEvidence := false, uncertaintyPresent := true,
  residualOwnerPresent := true, counterevidencePresent := true,
  noErasureInferenceRecorded := true, noReleaseAuthorityRecorded := true,
  permittedConsumerPresent := true, boundedCustodyRecordPresent := true,
  datasetCheckpointBound := true, custodyExpiryPresent := true, monitorPresent := true,
  revocationPathPresent := true, noCustodySupportAuthorityRecorded := true,
  materialChangeTriggerPresent := true, completeInvalidationPresent := true,
  ordinaryRouteBlocked := true, rerunRequirementPresent := true,
  rollbackOrRevocationReceiptPresent := true, supportAssignmentRequested := false,
  externalEffectRequested := false }

def canonicalState (stage : Stage) : State := {
  stage := stage, datumDigest := 1001, cohortDigest := 1002, provenanceDigest := 1003,
  rightsDigest := 1004, authorityDigest := 1005, splitDigest := 1006,
  datasetDigest := 1007, modelDigest := 1008, baseCheckpointDigest := 1009,
  selectedCheckpointDigest := 1010, optimizerDigest := 1011, schedulerDigest := 1012,
  rngDigest := 1013, cacheDigest := 1014, backupDigest := 1015,
  lineageDigest := 1016, descendantDigest := 1017, deletionRequestDigest := 1018,
  evaluatorDigest := 1019, consumerDigest := 1020, version := 1, lastEventDigest := 0,
  receiptCount := 0, boundedCustodyCount := 0, readmissionCount := 0,
  supportAssignmentCount := 0, externalEffectCount := 0 }

theorem data_engine_lifecycle_routes :
    routeFor (canonicalState .draft) .scopeCustody
        { canonicalPacket with provenancePresent := false } = .requestProvenance ∧
    routeFor (canonicalState .admitted) .bindFullState
        { canonicalPacket with optimizerStatePresent := false } = .requestOptimizerState ∧
    routeFor (canonicalState .stateBound) .recordUpdate
        { canonicalPacket with declaredSurfaceRollbackExact := false } =
          .rejectDeclaredSurfaceRollbackMismatch ∧
    routeFor (canonicalState .deletionAssessed) .adjudicateClaims
        { canonicalPacket with behaviorUsedAsInfluenceEvidence := true } =
          .rejectBehaviorAsInfluence ∧
    routeFor (canonicalState .deletionAssessed) .adjudicateClaims
        { canonicalPacket with behaviorUsedAsPrivacyEvidence := true } =
          .rejectBehaviorAsPrivacy ∧
    routeFor (canonicalState .deletionAssessed) .adjudicateClaims
        { canonicalPacket with lineageUsedAsStorageEvidence := true } =
          .rejectLineageAsStorage ∧
    routeFor (canonicalState .adjudicated) .bindCustody canonicalPacket =
          .acceptBoundedCustody ∧
    routeFor (canonicalState .custodyBound) .triggerReadmission
        { canonicalPacket with successorVersion := 2 } = .acceptReadmission := by native_decide

end AsiStackProofs.DataEngineLifecycleRefinement

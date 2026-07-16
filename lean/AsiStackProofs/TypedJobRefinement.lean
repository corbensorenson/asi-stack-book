namespace AsiStackProofs.TypedJobRefinement

inductive Stage where
  | idle
  | locked
  | authorized
  | dispatched
  | executed
  | adjudicated
  | closed
deriving DecidableEq, Repr

inductive EventKind where
  | lockJob
  | authorizeJob
  | dispatchJob
  | executeJob
  | adjudicateJob
  | closeJob
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage
  | rejectJobSubstitution
  | rejectContractSubstitution
  | rejectEventReplay
  | rejectAuthorityLeak
  | requestLockedContract
  | requestApproval
  | requestPermissions
  | requestActiveLease
  | requestSchedulerSlot
  | requestDispatch
  | requestIdempotencyKey
  | rejectRetryAuthorityWidening
  | requestCancellationAcknowledgment
  | rejectPostCancellationExecution
  | requestOutputArtifacts
  | requestAuditTrail
  | requestVerification
  | requestCompletionReceipt
  | requestReplayReference
  | requestResidualOwner
  | requestConsumerAcknowledgment
  | acceptLock
  | acceptAuthorization
  | acceptDispatch
  | acceptExecution
  | acceptAdjudication
  | acceptClosure
deriving DecidableEq, Repr

structure Packet where
  jobId : Nat
  jobVersion : Nat
  contractDigest : Nat
  planNodeDigest : Nat
  authorityDigest : Nat
  permissionDigest : Nat
  leaseEpoch : Nat
  schedulerDigest : Nat
  consumerDigest : Nat
  eventDigest : Nat
  parentContractPresent : Bool
  planNodePresent : Bool
  contractLocked : Bool
  approvalRequired : Bool
  approvalRecorded : Bool
  permissionsSatisfied : Bool
  leaseActive : Bool
  schedulerSlotAvailable : Bool
  dispatchRequested : Bool
  retryAttempted : Bool
  idempotencyKeyPresent : Bool
  retryAuthorityUnchanged : Bool
  cancellationRequested : Bool
  cancellationAcknowledged : Bool
  outputDelivered : Bool
  artifactRefsPresent : Bool
  auditTrailPresent : Bool
  verificationPassed : Bool
  completionReceiptPresent : Bool
  replayReferencePresent : Bool
  residualOwnerPresent : Bool
  consumerAcknowledgmentPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  jobId : Nat
  jobVersion : Nat
  contractDigest : Nat
  planNodeDigest : Nat
  authorityDigest : Nat
  permissionDigest : Nat
  leaseEpoch : Nat
  schedulerDigest : Nat
  consumerDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  executionObservationCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .idle => .lockJob
  | .locked => .authorizeJob
  | .authorized => .dispatchJob
  | .dispatched => .executeJob
  | .executed => .adjudicateJob
  | .adjudicated => .closeJob
  | .closed => .closeJob

def exactJobBinding (state : State) (packet : Packet) : Bool :=
  packet.jobId == state.jobId &&
  packet.jobVersion == state.jobVersion &&
  packet.consumerDigest == state.consumerDigest

def exactContractBinding (state : State) (packet : Packet) : Bool :=
  packet.contractDigest == state.contractDigest &&
  packet.planNodeDigest == state.planNodeDigest &&
  packet.authorityDigest == state.authorityDigest &&
  packet.permissionDigest == state.permissionDigest &&
  packet.leaseEpoch == state.leaseEpoch &&
  packet.schedulerDigest == state.schedulerDigest

def routeFor (state : State) (event : Event) : Route :=
  if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactJobBinding state event.packet then .rejectJobSubstitution
  else if ! exactContractBinding state event.packet then .rejectContractSubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectEventReplay
  else if event.packet.supportAssignmentRequested || event.packet.externalEffectRequested then
    .rejectAuthorityLeak
  else match state.stage with
  | .idle =>
      if ! event.packet.parentContractPresent || ! event.packet.planNodePresent ||
          ! event.packet.contractLocked then .requestLockedContract
      else .acceptLock
  | .locked =>
      if event.packet.approvalRequired && ! event.packet.approvalRecorded then
        .requestApproval
      else if ! event.packet.permissionsSatisfied then .requestPermissions
      else if ! event.packet.leaseActive then .requestActiveLease
      else .acceptAuthorization
  | .authorized =>
      if ! event.packet.leaseActive then .requestActiveLease
      else if ! event.packet.schedulerSlotAvailable then .requestSchedulerSlot
      else if ! event.packet.dispatchRequested then .requestDispatch
      else .acceptDispatch
  | .dispatched =>
      if event.packet.cancellationRequested && ! event.packet.cancellationAcknowledged then
        .requestCancellationAcknowledgment
      else if event.packet.cancellationAcknowledged && event.packet.outputDelivered then
        .rejectPostCancellationExecution
      else if event.packet.retryAttempted && ! event.packet.idempotencyKeyPresent then
        .requestIdempotencyKey
      else if event.packet.retryAttempted && ! event.packet.retryAuthorityUnchanged then
        .rejectRetryAuthorityWidening
      else if ! event.packet.outputDelivered || ! event.packet.artifactRefsPresent then
        .requestOutputArtifacts
      else if ! event.packet.auditTrailPresent then .requestAuditTrail
      else .acceptExecution
  | .executed =>
      if ! event.packet.verificationPassed then .requestVerification
      else if ! event.packet.completionReceiptPresent then .requestCompletionReceipt
      else if ! event.packet.replayReferencePresent then .requestReplayReference
      else if ! event.packet.residualOwnerPresent then .requestResidualOwner
      else .acceptAdjudication
  | .adjudicated =>
      if ! event.packet.consumerAcknowledgmentPresent then .requestConsumerAcknowledgment
      else .acceptClosure
  | .closed => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptLock
  | .acceptAuthorization
  | .acceptDispatch
  | .acceptExecution
  | .acceptAdjudication
  | .acceptClosure => true
  | _ => false

def advanceStage : Stage -> Stage
  | .idle => .locked
  | .locked => .authorized
  | .authorized => .dispatched
  | .dispatched => .executed
  | .executed => .adjudicated
  | .adjudicated => .closed
  | .closed => .closed

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advanceStage state.stage
       lastEventDigest := event.packet.eventDigest
       receiptCount := state.receiptCount + 1
       executionObservationCount :=
         if state.stage == .dispatched then state.executionObservationCount + 1
         else state.executionObservationCount }, route)
  else (state, route)

theorem apply_event_preserves_job_and_contract_identity
    (state : State) (event : Event) :
    (applyEvent state event).1.jobId = state.jobId ∧
    (applyEvent state event).1.jobVersion = state.jobVersion ∧
    (applyEvent state event).1.contractDigest = state.contractDigest ∧
    (applyEvent state event).1.planNodeDigest = state.planNodeDigest ∧
    (applyEvent state event).1.authorityDigest = state.authorityDigest ∧
    (applyEvent state event).1.permissionDigest = state.permissionDigest ∧
    (applyEvent state event).1.leaseEpoch = state.leaseEpoch := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_effect
    (state : State) (event : Event) :
    (applyEvent state event).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state event).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, h]

theorem accepted_step_adds_exactly_one_receipt
    (state : State) (event : Event)
    (h : accepted (routeFor state event) = true) :
    (applyEvent state event).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, h]

def canonicalPacket : Packet :=
  { jobId := 501
    jobVersion := 3
    contractDigest := 601
    planNodeDigest := 602
    authorityDigest := 603
    permissionDigest := 604
    leaseEpoch := 7
    schedulerDigest := 605
    consumerDigest := 606
    eventDigest := 1
    parentContractPresent := true
    planNodePresent := true
    contractLocked := true
    approvalRequired := true
    approvalRecorded := true
    permissionsSatisfied := true
    leaseActive := true
    schedulerSlotAvailable := true
    dispatchRequested := true
    retryAttempted := true
    idempotencyKeyPresent := true
    retryAuthorityUnchanged := true
    cancellationRequested := false
    cancellationAcknowledged := false
    outputDelivered := true
    artifactRefsPresent := true
    auditTrailPresent := true
    verificationPassed := true
    completionReceiptPresent := true
    replayReferencePresent := true
    residualOwnerPresent := true
    consumerAcknowledgmentPresent := true
    supportAssignmentRequested := false
    externalEffectRequested := false }

def initialState : State :=
  { stage := .idle
    jobId := 501
    jobVersion := 3
    contractDigest := 601
    planNodeDigest := 602
    authorityDigest := 603
    permissionDigest := 604
    leaseEpoch := 7
    schedulerDigest := 605
    consumerDigest := 606
    lastEventDigest := 0
    receiptCount := 0
    executionObservationCount := 0
    supportAssignmentCount := 0
    externalEffectCount := 0 }

def lockEvent : Event := { kind := .lockJob, packet := canonicalPacket }
def lockedState : State := (applyEvent initialState lockEvent).1
def authorizeEvent : Event := { kind := .authorizeJob, packet := { canonicalPacket with eventDigest := 2 } }
def authorizedState : State := (applyEvent lockedState authorizeEvent).1
def dispatchEvent : Event := { kind := .dispatchJob, packet := { canonicalPacket with eventDigest := 3 } }
def dispatchedState : State := (applyEvent authorizedState dispatchEvent).1
def executeEvent : Event := { kind := .executeJob, packet := { canonicalPacket with eventDigest := 4 } }
def executedState : State := (applyEvent dispatchedState executeEvent).1
def adjudicateEvent : Event := { kind := .adjudicateJob, packet := { canonicalPacket with eventDigest := 5 } }
def adjudicatedState : State := (applyEvent executedState adjudicateEvent).1
def closeEvent : Event := { kind := .closeJob, packet := { canonicalPacket with eventDigest := 6 } }
def finalState : State := (applyEvent adjudicatedState closeEvent).1

def missingApprovalEvent : Event :=
  { kind := .authorizeJob, packet := { canonicalPacket with eventDigest := 20, approvalRecorded := false } }
def expiredLeaseEvent : Event :=
  { kind := .dispatchJob, packet := { canonicalPacket with eventDigest := 21, leaseActive := false } }
def missingIdempotencyEvent : Event :=
  { kind := .executeJob, packet := { canonicalPacket with eventDigest := 22, idempotencyKeyPresent := false } }
def widenedRetryEvent : Event :=
  { kind := .executeJob, packet := { canonicalPacket with eventDigest := 23, retryAuthorityUnchanged := false } }
def unacknowledgedCancellationEvent : Event :=
  { kind := .executeJob, packet := { canonicalPacket with eventDigest := 24, cancellationRequested := true } }
def postCancellationOutputEvent : Event :=
  { kind := .executeJob, packet := { canonicalPacket with eventDigest := 25, cancellationAcknowledged := true } }
def missingArtifactsEvent : Event :=
  { kind := .executeJob, packet := { canonicalPacket with eventDigest := 26, artifactRefsPresent := false } }
def unverifiedAdjudicationEvent : Event :=
  { kind := .adjudicateJob, packet := { canonicalPacket with eventDigest := 27, verificationPassed := false } }
def missingReplayEvent : Event :=
  { kind := .adjudicateJob, packet := { canonicalPacket with eventDigest := 28, replayReferencePresent := false } }
def missingConsumerAckEvent : Event :=
  { kind := .closeJob, packet := { canonicalPacket with eventDigest := 29, consumerAcknowledgmentPresent := false } }

theorem approval_required_job_cannot_authorize_without_record :
    routeFor lockedState missingApprovalEvent = .requestApproval := by rfl

theorem expired_lease_cannot_dispatch :
    routeFor authorizedState expiredLeaseEvent = .requestActiveLease := by rfl

theorem retry_requires_idempotency_key :
    routeFor dispatchedState missingIdempotencyEvent = .requestIdempotencyKey := by rfl

theorem retry_cannot_widen_authority :
    routeFor dispatchedState widenedRetryEvent = .rejectRetryAuthorityWidening := by rfl

theorem cancellation_requires_acknowledgment :
    routeFor dispatchedState unacknowledgedCancellationEvent = .requestCancellationAcknowledgment := by rfl

theorem acknowledged_cancellation_rejects_post_cancel_output :
    routeFor dispatchedState postCancellationOutputEvent = .rejectPostCancellationExecution := by rfl

theorem execution_requires_artifact_refs :
    routeFor dispatchedState missingArtifactsEvent = .requestOutputArtifacts := by rfl

theorem adjudication_requires_verification :
    routeFor executedState unverifiedAdjudicationEvent = .requestVerification := by rfl

theorem evidence_ready_adjudication_requires_replay_reference :
    routeFor executedState missingReplayEvent = .requestReplayReference := by rfl

theorem closure_requires_consumer_acknowledgment :
    routeFor adjudicatedState missingConsumerAckEvent = .requestConsumerAcknowledgment := by rfl

theorem full_typed_job_lifecycle_reaches_closed_state :
    finalState.stage = .closed ∧
    finalState.receiptCount = 6 ∧
    finalState.executionObservationCount = 1 ∧
    finalState.supportAssignmentCount = 0 ∧
    finalState.externalEffectCount = 0 := by
  native_decide

end AsiStackProofs.TypedJobRefinement

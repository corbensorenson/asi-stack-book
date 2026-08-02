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
  else if state.stage == .closed then .rejectWrongStage
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

def stageRank : Stage -> Nat
  | .idle => 0
  | .locked => 1
  | .authorized => 2
  | .dispatched => 3
  | .executed => 4
  | .adjudicated => 5
  | .closed => 6

def expectedExecutionObservations : Stage -> Nat
  | .idle | .locked | .authorized | .dispatched => 0
  | .executed | .adjudicated | .closed => 1

def LifecycleInvariant (state : State) : Prop :=
  state.receiptCount = stageRank state.stage ∧
  state.executionObservationCount = expectedExecutionObservations state.stage ∧
  state.supportAssignmentCount = 0 ∧
  state.externalEffectCount = 0

def FullCustodyEqual (before after : State) : Prop :=
  after.jobId = before.jobId ∧
  after.jobVersion = before.jobVersion ∧
  after.contractDigest = before.contractDigest ∧
  after.planNodeDigest = before.planNodeDigest ∧
  after.authorityDigest = before.authorityDigest ∧
  after.permissionDigest = before.permissionDigest ∧
  after.leaseEpoch = before.leaseEpoch ∧
  after.schedulerDigest = before.schedulerDigest ∧
  after.consumerDigest = before.consumerDigest

def runEvents : State -> List Event -> State
  | state, [] => state
  | state, event :: rest => runEvents (applyEvent state event).1 rest

theorem rejected_event_is_state_noninterfering
    {state : State} {event : Event}
    (rejected : accepted (routeFor state event) = false) :
    (applyEvent state event).1 = state := by
  simp [applyEvent, rejected]

theorem closed_state_accepts_no_event
    {state : State} {event : Event}
    (closed : state.stage = .closed) :
    accepted (routeFor state event) = false := by
  simp [routeFor, expectedKind, accepted, closed]

theorem apply_event_preserves_lifecycle_invariant
    {state : State} {event : Event}
    (safe : LifecycleInvariant state) :
    LifecycleInvariant (applyEvent state event).1 := by
  by_cases acceptedRoute : accepted (routeFor state event) = true
  · rcases safe with ⟨receipts, observations, support, effects⟩
    cases stageEq : state.stage <;>
      simp [applyEvent, acceptedRoute, LifecycleInvariant, stageRank,
        expectedExecutionObservations, advanceStage, stageEq, receipts,
        observations, support, effects]
    have rejected := closed_state_accepts_no_event (event := event) stageEq
    simp [rejected] at acceptedRoute
  · have rejected : accepted (routeFor state event) = false := by
      cases route : accepted (routeFor state event) <;> simp_all
    simpa [rejected_event_is_state_noninterfering rejected] using safe

theorem apply_event_preserves_full_custody
    (state : State) (event : Event) :
    FullCustodyEqual state (applyEvent state event).1 := by
  by_cases acceptedRoute : accepted (routeFor state event) = true <;>
    simp [applyEvent, acceptedRoute, FullCustodyEqual]

theorem run_events_preserves_lifecycle_invariant
    {state : State} {events : List Event}
    (safe : LifecycleInvariant state) :
    LifecycleInvariant (runEvents state events) := by
  induction events generalizing state with
  | nil => simpa [runEvents] using safe
  | cons event rest ih =>
      simpa [runEvents] using ih (apply_event_preserves_lifecycle_invariant safe)

theorem run_events_preserves_full_custody
    (state : State) (events : List Event) :
    FullCustodyEqual state (runEvents state events) := by
  induction events generalizing state with
  | nil => simp [runEvents, FullCustodyEqual]
  | cons event rest ih =>
      have head := apply_event_preserves_full_custody state event
      have tail := ih (applyEvent state event).1
      rcases head with ⟨h1, h2, h3, h4, h5, h6, h7, h8, h9⟩
      rcases tail with ⟨t1, t2, t3, t4, t5, t6, t7, t8, t9⟩
      exact ⟨t1.trans h1, t2.trans h2, t3.trans h3, t4.trans h4,
        t5.trans h5, t6.trans h6, t7.trans h7, t8.trans h8, t9.trans h9⟩

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

theorem initial_state_satisfies_lifecycle_invariant :
    LifecycleInvariant initialState := by
  simp [LifecycleInvariant, initialState, stageRank,
    expectedExecutionObservations]

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

def canonicalLifecycle : List Event :=
  [lockEvent, authorizeEvent, dispatchEvent, executeEvent,
    adjudicateEvent, closeEvent]

theorem canonical_run_reaches_exact_closed_state :
    runEvents initialState canonicalLifecycle = finalState := by
  native_decide

theorem reachable_closed_state_has_exact_modeled_accounting
    {events : List Event}
    (closed : (runEvents initialState events).stage = .closed) :
    (runEvents initialState events).receiptCount = 6 ∧
    (runEvents initialState events).executionObservationCount = 1 ∧
    (runEvents initialState events).supportAssignmentCount = 0 ∧
    (runEvents initialState events).externalEffectCount = 0 := by
  have safe := run_events_preserves_lifecycle_invariant
    (events := events) initial_state_satisfies_lifecycle_invariant
  simpa [LifecycleInvariant, closed, stageRank,
    expectedExecutionObservations] using safe

theorem wrong_stage_event_is_rejected_without_state_change :
    applyEvent initialState authorizeEvent =
      (initialState, .rejectWrongStage) := by
  native_decide

theorem substituted_job_is_rejected_without_state_change :
    applyEvent initialState
      { lockEvent with packet := { canonicalPacket with jobId := 999 } } =
      (initialState, .rejectJobSubstitution) := by
  native_decide

theorem substituted_contract_is_rejected_without_state_change :
    applyEvent initialState
      { lockEvent with packet := { canonicalPacket with contractDigest := 999 } } =
      (initialState, .rejectContractSubstitution) := by
  native_decide

theorem repeated_event_digest_is_rejected_without_state_change :
    applyEvent lockedState
      { authorizeEvent with packet := { canonicalPacket with eventDigest := 1 } } =
      (lockedState, .rejectEventReplay) := by
  native_decide

theorem support_assignment_request_is_rejected_without_state_change :
    applyEvent initialState
      { lockEvent with
          packet := { canonicalPacket with supportAssignmentRequested := true } } =
      (initialState, .rejectAuthorityLeak) := by
  native_decide

theorem external_effect_request_is_rejected_without_state_change :
    applyEvent initialState
      { lockEvent with
          packet := { canonicalPacket with externalEffectRequested := true } } =
      (initialState, .rejectAuthorityLeak) := by
  native_decide

theorem execution_without_audit_is_rejected_without_state_change :
    applyEvent dispatchedState
      { executeEvent with packet := { canonicalPacket with
          eventDigest := 30, auditTrailPresent := false } } =
      (dispatchedState, .requestAuditTrail) := by
  native_decide

theorem adjudication_without_completion_receipt_is_rejected_without_state_change :
    applyEvent executedState
      { adjudicateEvent with packet := { canonicalPacket with
          eventDigest := 31, completionReceiptPresent := false } } =
      (executedState, .requestCompletionReceipt) := by
  native_decide

theorem adjudication_without_residual_owner_is_rejected_without_state_change :
    applyEvent executedState
      { adjudicateEvent with packet := { canonicalPacket with
          eventDigest := 32, residualOwnerPresent := false } } =
      (executedState, .requestResidualOwner) := by
  native_decide

end AsiStackProofs.TypedJobRefinement

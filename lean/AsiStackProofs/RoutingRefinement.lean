namespace AsiStackProofs.RoutingRefinement

inductive Stage where
  | idle | requestBound | registryFrozen | leaseQualified
  | dispatched | outcomeObserved | closed
deriving DecidableEq, Repr

inductive EventKind where
  | bindRequest | freezeRegistry | qualifyLease | dispatchRoute
  | observeOutcome | closeRoute
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectTaskSubstitution | rejectRegistrySubstitution
  | rejectEventReplay | rejectAuthorityLeak
  | requestTask | requestCapability | requestRegistry
  | requestCandidateDenominator | rejectLabelLeak
  | requestRegisteredSelection | blockAuthority | blockReadiness
  | requestFreshContextLease | requestFreshToolLease | requestCostQuality
  | requestLeastCapableAdequate | requestRejectedCandidateEvidence
  | requestSelectivePolicy | requestSelectiveAction | routeFallback
  | requestResidualOwner | requestSourceInspection | requestRuntimeEvidence
  | requestReplayEvidence | requestDispatchGrant | requestIsolation
  | requestOutcomeObservation | requestRouteQuality | requestAnswerQuality
  | requestUnsafeOutcome | requestCostRecord | requestLifecycleCurrent
  | requestRevocationClosure | requestConsumerAcknowledgment
  | requestNonClaims | acceptRequest | acceptRegistry | acceptLease
  | acceptDispatch | acceptObservation | acceptClosure
deriving DecidableEq, Repr

structure Packet where
  taskId : Nat
  taskVersion : Nat
  requestDigest : Nat
  registryDigest : Nat
  candidateSetDigest : Nat
  selectedSpecialistDigest : Nat
  capabilityDigest : Nat
  authorityDigest : Nat
  readinessDigest : Nat
  contextLeaseDigest : Nat
  toolLeaseDigest : Nat
  evaluatorDigest : Nat
  policyDigest : Nat
  consumerDigest : Nat
  eventDigest : Nat
  taskPresent : Bool
  capabilityRequestPresent : Bool
  registryPresent : Bool
  candidateDenominatorComplete : Bool
  heldOutLabelLeakAbsent : Bool
  selectedSpecialistRegistered : Bool
  authoritySatisfied : Bool
  readinessSatisfied : Bool
  fallbackAvailable : Bool
  residualOwnerPresent : Bool
  contextLeaseFresh : Bool
  toolLeaseFresh : Bool
  costQualityRecordPresent : Bool
  leastCapableAdequate : Bool
  rejectedCandidateEvidencePresent : Bool
  selectivePolicyPresent : Bool
  ambiguityDetected : Bool
  selectiveActionChosen : Bool
  sourceInspected : Bool
  runtimeEvidenceRefsPresent : Bool
  replayEvidenceRefsPresent : Bool
  dispatchGrantPresent : Bool
  isolationBoundaryPresent : Bool
  outcomeObserved : Bool
  routeQualityRecorded : Bool
  answerQualityRecorded : Bool
  unsafeOutcomeRecorded : Bool
  costRecordPresent : Bool
  lifecycleCurrent : Bool
  revocationClosureComplete : Bool
  consumerAcknowledgmentPresent : Bool
  nonClaimsPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  taskId : Nat
  taskVersion : Nat
  requestDigest : Nat
  registryDigest : Nat
  candidateSetDigest : Nat
  selectedSpecialistDigest : Nat
  capabilityDigest : Nat
  authorityDigest : Nat
  readinessDigest : Nat
  contextLeaseDigest : Nat
  toolLeaseDigest : Nat
  evaluatorDigest : Nat
  policyDigest : Nat
  consumerDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  dispatchCount : Nat
  routeOutcomeCount : Nat
  answerOutcomeCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .idle => .bindRequest
  | .requestBound => .freezeRegistry
  | .registryFrozen => .qualifyLease
  | .leaseQualified => .dispatchRoute
  | .dispatched => .observeOutcome
  | .outcomeObserved => .closeRoute
  | .closed => .closeRoute

def exactTaskBinding (state : State) (packet : Packet) : Bool :=
  packet.taskId == state.taskId && packet.taskVersion == state.taskVersion &&
  packet.requestDigest == state.requestDigest &&
  packet.capabilityDigest == state.capabilityDigest &&
  packet.policyDigest == state.policyDigest &&
  packet.consumerDigest == state.consumerDigest

def exactRegistryBinding (state : State) (packet : Packet) : Bool :=
  packet.registryDigest == state.registryDigest &&
  packet.candidateSetDigest == state.candidateSetDigest &&
  packet.selectedSpecialistDigest == state.selectedSpecialistDigest &&
  packet.authorityDigest == state.authorityDigest &&
  packet.readinessDigest == state.readinessDigest &&
  packet.contextLeaseDigest == state.contextLeaseDigest &&
  packet.toolLeaseDigest == state.toolLeaseDigest &&
  packet.evaluatorDigest == state.evaluatorDigest

def routeFor (state : State) (event : Event) : Route :=
  if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactTaskBinding state event.packet then .rejectTaskSubstitution
  else if ! exactRegistryBinding state event.packet then .rejectRegistrySubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectEventReplay
  else if event.packet.supportAssignmentRequested || event.packet.externalEffectRequested then
    .rejectAuthorityLeak
  else match state.stage with
  | .idle =>
      if ! event.packet.taskPresent then .requestTask
      else if ! event.packet.capabilityRequestPresent then .requestCapability
      else .acceptRequest
  | .requestBound =>
      if ! event.packet.registryPresent then .requestRegistry
      else if ! event.packet.candidateDenominatorComplete then .requestCandidateDenominator
      else if ! event.packet.heldOutLabelLeakAbsent then .rejectLabelLeak
      else if ! event.packet.selectedSpecialistRegistered then .requestRegisteredSelection
      else .acceptRegistry
  | .registryFrozen =>
      if ! event.packet.authoritySatisfied then .blockAuthority
      else if ! event.packet.readinessSatisfied then
        if event.packet.fallbackAvailable then .routeFallback
        else if ! event.packet.residualOwnerPresent then .requestResidualOwner
        else .blockReadiness
      else if ! event.packet.contextLeaseFresh then .requestFreshContextLease
      else if ! event.packet.toolLeaseFresh then .requestFreshToolLease
      else if ! event.packet.costQualityRecordPresent then .requestCostQuality
      else if ! event.packet.leastCapableAdequate then .requestLeastCapableAdequate
      else if ! event.packet.rejectedCandidateEvidencePresent then
        .requestRejectedCandidateEvidence
      else if ! event.packet.selectivePolicyPresent then .requestSelectivePolicy
      else if event.packet.ambiguityDetected && ! event.packet.selectiveActionChosen then
        .requestSelectiveAction
      else if ! event.packet.sourceInspected then .requestSourceInspection
      else if ! event.packet.runtimeEvidenceRefsPresent then .requestRuntimeEvidence
      else if ! event.packet.replayEvidenceRefsPresent then .requestReplayEvidence
      else .acceptLease
  | .leaseQualified =>
      if ! event.packet.dispatchGrantPresent then .requestDispatchGrant
      else if ! event.packet.isolationBoundaryPresent then .requestIsolation
      else .acceptDispatch
  | .dispatched =>
      if ! event.packet.outcomeObserved then .requestOutcomeObservation
      else if ! event.packet.routeQualityRecorded then .requestRouteQuality
      else if ! event.packet.answerQualityRecorded then .requestAnswerQuality
      else if ! event.packet.unsafeOutcomeRecorded then .requestUnsafeOutcome
      else if ! event.packet.costRecordPresent then .requestCostRecord
      else .acceptObservation
  | .outcomeObserved =>
      if ! event.packet.lifecycleCurrent then .requestLifecycleCurrent
      else if ! event.packet.revocationClosureComplete then .requestRevocationClosure
      else if ! event.packet.consumerAcknowledgmentPresent then
        .requestConsumerAcknowledgment
      else if ! event.packet.nonClaimsPresent then .requestNonClaims
      else .acceptClosure
  | .closed => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptRequest | .acceptRegistry | .acceptLease | .acceptDispatch
  | .acceptObservation | .acceptClosure => true
  | _ => false

def advanceStage : Stage -> Stage
  | .idle => .requestBound | .requestBound => .registryFrozen
  | .registryFrozen => .leaseQualified | .leaseQualified => .dispatched
  | .dispatched => .outcomeObserved | .outcomeObserved => .closed
  | .closed => .closed

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advanceStage state.stage
       lastEventDigest := event.packet.eventDigest
       receiptCount := state.receiptCount + 1
       dispatchCount :=
         if state.stage == .leaseQualified then state.dispatchCount + 1
         else state.dispatchCount
       routeOutcomeCount :=
         if state.stage == .dispatched then state.routeOutcomeCount + 1
         else state.routeOutcomeCount
       answerOutcomeCount :=
         if state.stage == .dispatched then state.answerOutcomeCount + 1
         else state.answerOutcomeCount }, route)
  else (state, route)

theorem apply_event_preserves_task_registry_and_lease_identity
    (state : State) (event : Event) :
    (applyEvent state event).1.taskId = state.taskId ∧
    (applyEvent state event).1.requestDigest = state.requestDigest ∧
    (applyEvent state event).1.registryDigest = state.registryDigest ∧
    (applyEvent state event).1.candidateSetDigest = state.candidateSetDigest ∧
    (applyEvent state event).1.selectedSpecialistDigest = state.selectedSpecialistDigest ∧
    (applyEvent state event).1.contextLeaseDigest = state.contextLeaseDigest ∧
    (applyEvent state event).1.toolLeaseDigest = state.toolLeaseDigest := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_effect
    (state : State) (event : Event) :
    (applyEvent state event).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state event).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state event) = true <;> simp [applyEvent, h]

theorem accepted_step_adds_exactly_one_receipt
    (state : State) (event : Event) (h : accepted (routeFor state event) = true) :
    (applyEvent state event).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, h]

def canonicalPacket : Packet :=
  { taskId := 601, taskVersion := 4, requestDigest := 701, registryDigest := 702
    candidateSetDigest := 703, selectedSpecialistDigest := 704
    capabilityDigest := 705, authorityDigest := 706, readinessDigest := 707
    contextLeaseDigest := 708, toolLeaseDigest := 709, evaluatorDigest := 710
    policyDigest := 711, consumerDigest := 712, eventDigest := 1
    taskPresent := true, capabilityRequestPresent := true, registryPresent := true
    candidateDenominatorComplete := true, heldOutLabelLeakAbsent := true
    selectedSpecialistRegistered := true, authoritySatisfied := true
    readinessSatisfied := true, fallbackAvailable := true, residualOwnerPresent := true
    contextLeaseFresh := true, toolLeaseFresh := true, costQualityRecordPresent := true
    leastCapableAdequate := true, rejectedCandidateEvidencePresent := true
    selectivePolicyPresent := true, ambiguityDetected := false, selectiveActionChosen := true
    sourceInspected := true, runtimeEvidenceRefsPresent := true
    replayEvidenceRefsPresent := true, dispatchGrantPresent := true
    isolationBoundaryPresent := true, outcomeObserved := true
    routeQualityRecorded := true, answerQualityRecorded := true
    unsafeOutcomeRecorded := true, costRecordPresent := true
    lifecycleCurrent := true, revocationClosureComplete := true
    consumerAcknowledgmentPresent := true, nonClaimsPresent := true
    supportAssignmentRequested := false, externalEffectRequested := false }

def initialState : State :=
  { stage := .idle, taskId := 601, taskVersion := 4, requestDigest := 701
    registryDigest := 702, candidateSetDigest := 703, selectedSpecialistDigest := 704
    capabilityDigest := 705, authorityDigest := 706, readinessDigest := 707
    contextLeaseDigest := 708, toolLeaseDigest := 709, evaluatorDigest := 710
    policyDigest := 711, consumerDigest := 712, lastEventDigest := 0
    receiptCount := 0, dispatchCount := 0, routeOutcomeCount := 0
    answerOutcomeCount := 0, supportAssignmentCount := 0, externalEffectCount := 0 }

def requestEvent : Event := { kind := .bindRequest, packet := canonicalPacket }
def requestState : State := (applyEvent initialState requestEvent).1
def registryEvent : Event := { kind := .freezeRegistry, packet := { canonicalPacket with eventDigest := 2 } }
def registryState : State := (applyEvent requestState registryEvent).1
def leaseEvent : Event := { kind := .qualifyLease, packet := { canonicalPacket with eventDigest := 3 } }
def leaseState : State := (applyEvent registryState leaseEvent).1
def dispatchEvent : Event := { kind := .dispatchRoute, packet := { canonicalPacket with eventDigest := 4 } }
def dispatchState : State := (applyEvent leaseState dispatchEvent).1
def outcomeEvent : Event := { kind := .observeOutcome, packet := { canonicalPacket with eventDigest := 5 } }
def outcomeState : State := (applyEvent dispatchState outcomeEvent).1
def closeEvent : Event := { kind := .closeRoute, packet := { canonicalPacket with eventDigest := 6 } }
def finalState : State := (applyEvent outcomeState closeEvent).1

theorem registry_freeze_requires_complete_candidate_denominator :
    routeFor requestState { registryEvent with packet := { canonicalPacket with eventDigest := 20, candidateDenominatorComplete := false } } =
      .requestCandidateDenominator := by rfl

theorem held_out_label_leak_blocks_registry_freeze :
    routeFor requestState { registryEvent with packet := { canonicalPacket with eventDigest := 21, heldOutLabelLeakAbsent := false } } =
      .rejectLabelLeak := by rfl

theorem missing_authority_blocks_lease :
    routeFor registryState { leaseEvent with packet := { canonicalPacket with eventDigest := 22, authoritySatisfied := false } } =
      .blockAuthority := by rfl

theorem failed_readiness_with_fallback_routes_to_fallback :
    routeFor registryState { leaseEvent with packet := { canonicalPacket with eventDigest := 23, readinessSatisfied := false } } =
      .routeFallback := by rfl

theorem failed_readiness_without_fallback_requires_residual_owner :
    routeFor registryState { leaseEvent with packet := { canonicalPacket with eventDigest := 24, readinessSatisfied := false, fallbackAvailable := false, residualOwnerPresent := false } } =
      .requestResidualOwner := by rfl

theorem stale_context_lease_blocks_qualification :
    routeFor registryState { leaseEvent with packet := { canonicalPacket with eventDigest := 25, contextLeaseFresh := false } } =
      .requestFreshContextLease := by rfl

theorem overprivileged_selection_requires_least_capable_justification :
    routeFor registryState { leaseEvent with packet := { canonicalPacket with eventDigest := 26, leastCapableAdequate := false } } =
      .requestLeastCapableAdequate := by rfl

theorem ambiguous_task_requires_selective_action :
    routeFor registryState { leaseEvent with packet := { canonicalPacket with eventDigest := 27, ambiguityDetected := true, selectiveActionChosen := false } } =
      .requestSelectiveAction := by rfl

theorem unavailable_runtime_evidence_blocks_lease :
    routeFor registryState { leaseEvent with packet := { canonicalPacket with eventDigest := 28, runtimeEvidenceRefsPresent := false } } =
      .requestRuntimeEvidence := by rfl

theorem missing_replay_evidence_blocks_lease :
    routeFor registryState { leaseEvent with packet := { canonicalPacket with eventDigest := 29, replayEvidenceRefsPresent := false } } =
      .requestReplayEvidence := by rfl

theorem dispatch_requires_separate_grant :
    routeFor leaseState { dispatchEvent with packet := { canonicalPacket with eventDigest := 30, dispatchGrantPresent := false } } =
      .requestDispatchGrant := by rfl

theorem outcome_keeps_route_and_answer_quality_separate :
    routeFor dispatchState { outcomeEvent with packet := { canonicalPacket with eventDigest := 31, answerQualityRecorded := false } } =
      .requestAnswerQuality := by rfl

theorem closure_requires_revocation_propagation :
    routeFor outcomeState { closeEvent with packet := { canonicalPacket with eventDigest := 32, revocationClosureComplete := false } } =
      .requestRevocationClosure := by rfl

theorem full_routing_lifecycle_reaches_closed_state :
    finalState.stage = .closed ∧ finalState.receiptCount = 6 ∧
    finalState.dispatchCount = 1 ∧ finalState.routeOutcomeCount = 1 ∧
    finalState.answerOutcomeCount = 1 ∧ finalState.supportAssignmentCount = 0 ∧
    finalState.externalEffectCount = 0 := by native_decide

end AsiStackProofs.RoutingRefinement

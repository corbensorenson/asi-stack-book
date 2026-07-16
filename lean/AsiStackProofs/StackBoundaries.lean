namespace AsiStackProofs.StackBoundaries

structure Layer where
  hasExternalActionAuthority : Bool
deriving DecidableEq, Repr

structure Handoff where
  authorized : Bool
deriving DecidableEq, Repr

inductive LayerOutput where
  | internalArtifact
  | externalAction (handoff : Handoff)
deriving DecidableEq, Repr

def ExternalActionAllowed (layer : Layer) : LayerOutput -> Prop
  | .internalArtifact => True
  | .externalAction handoff =>
      layer.hasExternalActionAuthority = true ∨ handoff.authorized = true

theorem layer_without_external_authority_requires_authorized_handoff
    {layer : Layer} {handoff : Handoff} :
    layer.hasExternalActionAuthority = false ->
    ExternalActionAllowed layer (.externalAction handoff) ->
    handoff.authorized = true := by
  intro noAuthority allowed
  cases allowed with
  | inl hasAuthority =>
      rw [noAuthority] at hasAuthority
      contradiction
  | inr authorized =>
      exact authorized

structure StackTraceStep where
  layer : Layer
  output : LayerOutput
deriving DecidableEq, Repr

def StackTraceValid (trace : List StackTraceStep) : Prop :=
  ∀ step, step ∈ trace -> ExternalActionAllowed step.layer step.output

theorem valid_stack_trace_rejects_unauthorized_external_handoff
    {trace : List StackTraceStep} {layer : Layer} {handoff : Handoff} :
    ({ layer := layer, output := .externalAction handoff } : StackTraceStep) ∈ trace ->
    layer.hasExternalActionAuthority = false ->
    handoff.authorized = false ->
    ¬ StackTraceValid trace := by
  intro present noAuthority unauthorized validTrace
  unfold StackTraceValid at validTrace
  have allowed :=
    validTrace ({ layer := layer, output := .externalAction handoff } : StackTraceStep) present
  have authorized :=
    layer_without_external_authority_requires_authorized_handoff noAuthority allowed
  rw [unauthorized] at authorized
  contradiction

inductive AuthorityLevel where
  | none
  | read
  | write
  | execute
  | admin
deriving DecidableEq, Repr

def AuthorityLevel.rank : AuthorityLevel -> Nat
  | .none => 0
  | .read => 1
  | .write => 2
  | .execute => 3
  | .admin => 4

structure HandoffRequest where
  callerCeiling : AuthorityLevel
  requested : AuthorityLevel
deriving DecidableEq, Repr

def HandoffAccepted (request : HandoffRequest) : Prop :=
  request.requested.rank <= request.callerCeiling.rank

theorem handoff_exceeding_caller_ceiling_rejected
    {request : HandoffRequest} :
    request.callerCeiling.rank < request.requested.rank ->
    ¬ HandoffAccepted request := by
  intro exceeds accepted
  exact Nat.not_le_of_gt exceeds accepted

inductive LayerContractAdmissionRoute where
  | noLayerContractRequested
  | requestLayerIdentity
  | requestLifecycleState
  | requestOwner
  | requestResponsibility
  | requestInputArtifacts
  | requestOutputArtifacts
  | requestAuthorityCeiling
  | requestHandoffProtocol
  | requestInvariant
  | requestFailureMode
  | requestEvidenceGate
  | blockExternalActionBoundary
  | requestSourceMapping
  | requestSupportBoundary
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | admitLayerContract
deriving DecidableEq, Repr

structure LayerContractAdmissionReview where
  contractRequested : Bool
  layerIdRecorded : Bool
  lifecycleStateRecorded : Bool
  ownerRecorded : Bool
  responsibilityRecorded : Bool
  inputArtifactsRecorded : Bool
  outputArtifactsRecorded : Bool
  authorityCeilingRecorded : Bool
  handoffProtocolRecorded : Bool
  invariantRecorded : Bool
  failureModeRecorded : Bool
  evidenceGateRecorded : Bool
  externalActionPossible : Bool
  externalActionAuthorityRecorded : Bool
  authorizedHandoffRecorded : Bool
  sourceMappingRecorded : Bool
  supportStateEffectRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def LayerContractAdmissionRouteFor
    (review : LayerContractAdmissionReview) :
    LayerContractAdmissionRoute :=
  if review.contractRequested = false then
    .noLayerContractRequested
  else if review.layerIdRecorded = false then
    .requestLayerIdentity
  else if review.lifecycleStateRecorded = false then
    .requestLifecycleState
  else if review.ownerRecorded = false then
    .requestOwner
  else if review.responsibilityRecorded = false then
    .requestResponsibility
  else if review.inputArtifactsRecorded = false then
    .requestInputArtifacts
  else if review.outputArtifactsRecorded = false then
    .requestOutputArtifacts
  else if review.authorityCeilingRecorded = false then
    .requestAuthorityCeiling
  else if review.handoffProtocolRecorded = false then
    .requestHandoffProtocol
  else if review.invariantRecorded = false then
    .requestInvariant
  else if review.failureModeRecorded = false then
    .requestFailureMode
  else if review.evidenceGateRecorded = false then
    .requestEvidenceGate
  else if review.externalActionPossible = true ∧
      review.externalActionAuthorityRecorded = false ∧
        review.authorizedHandoffRecorded = false then
    .blockExternalActionBoundary
  else if review.sourceMappingRecorded = false then
    .requestSourceMapping
  else if review.supportStateEffectRecorded = false then
    .requestSupportBoundary
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    .requestEvidenceTransition
  else if review.nonClaimBoundaryRecorded = false then
    .preserveNonClaimBoundary
  else
    .admitLayerContract

def completeLayerContractAdmissionReview :
    LayerContractAdmissionReview := {
  contractRequested := true
  layerIdRecorded := true
  lifecycleStateRecorded := true
  ownerRecorded := true
  responsibilityRecorded := true
  inputArtifactsRecorded := true
  outputArtifactsRecorded := true
  authorityCeilingRecorded := true
  handoffProtocolRecorded := true
  invariantRecorded := true
  failureModeRecorded := true
  evidenceGateRecorded := true
  externalActionPossible := false
  externalActionAuthorityRecorded := true
  authorizedHandoffRecorded := true
  sourceMappingRecorded := true
  supportStateEffectRecorded := true
  supportPromotionRequested := false
  evidenceTransitionRecorded := true
  nonClaimBoundaryRecorded := true
}

/-! ## Reachable authority-handoff-effect trace

The original propositions state local order facts. This transition system
models the reachable path from a layer request through target-owner grant,
receipt-bound dispatch, material effect, independent observation, revocation,
denial, and exact rollback.
-/

inductive BoundaryEventKind where
  | request
  | authorize
  | dispatch
  | commitEffect
  | observe
  | revoke
  | deny
  | rollback
deriving DecidableEq, Repr

structure BoundaryState where
  callerCeiling : Nat
  activeGrant : Option Nat
  authorityEpoch : Nat
  revoked : Bool
  pendingRequest : Option Nat
  dispatchReceipt : Bool
  materialEffects : Nat
  observedEffects : Nat
  rolledBack : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure BoundaryEvent where
  kind : BoundaryEventKind
  requestedAuthority : Nat
  grantAuthority : Nat
  authorityEpoch : Nat
  logicalTime : Nat
  targetOwnerApproved : Bool
  receiptPresent : Bool
  independentObservation : Bool
  rollbackExact : Bool
deriving DecidableEq, Repr

def BoundaryEventValid (state : BoundaryState) (event : BoundaryEvent) : Bool :=
  decide (state.logicalTime ≤ event.logicalTime) &&
  match event.kind with
  | .request =>
      decide (event.requestedAuthority != 0) &&
        decide (state.pendingRequest = none) &&
        decide (state.activeGrant = none)
  | .authorize =>
      decide (state.pendingRequest = some event.requestedAuthority) &&
        decide (event.grantAuthority = event.requestedAuthority) &&
        decide (event.grantAuthority ≤ state.callerCeiling) &&
        decide (event.authorityEpoch = state.authorityEpoch) &&
        event.targetOwnerApproved && !state.revoked && event.receiptPresent
  | .dispatch =>
      decide (state.activeGrant = some event.grantAuthority) &&
        decide (event.authorityEpoch = state.authorityEpoch) &&
        !state.revoked && event.receiptPresent
  | .commitEffect =>
      decide (state.activeGrant = some event.grantAuthority) &&
        decide (event.authorityEpoch = state.authorityEpoch) &&
        state.dispatchReceipt && !state.revoked && event.receiptPresent
  | .observe =>
      decide (state.observedEffects < state.materialEffects) &&
        event.independentObservation && event.receiptPresent
  | .revoke =>
      decide (event.authorityEpoch = state.authorityEpoch) && event.receiptPresent
  | .deny =>
      decide (state.pendingRequest = some event.requestedAuthority) &&
        decide (state.materialEffects = 0) && event.receiptPresent
  | .rollback =>
      decide (0 < state.materialEffects) &&
        decide (state.observedEffects = state.materialEffects) &&
        event.rollbackExact && event.receiptPresent

def ApplyBoundaryEvent (state : BoundaryState) (event : BoundaryEvent) : BoundaryState :=
  match event.kind with
  | .request => { state with pendingRequest := some event.requestedAuthority, logicalTime := event.logicalTime }
  | .authorize => { state with activeGrant := some event.grantAuthority, logicalTime := event.logicalTime }
  | .dispatch => { state with dispatchReceipt := true, logicalTime := event.logicalTime }
  | .commitEffect => { state with materialEffects := state.materialEffects + 1, logicalTime := event.logicalTime }
  | .observe => { state with observedEffects := state.observedEffects + 1, logicalTime := event.logicalTime }
  | .revoke => { state with activeGrant := none, authorityEpoch := state.authorityEpoch + 1, revoked := true, dispatchReceipt := false, logicalTime := event.logicalTime }
  | .deny => { state with pendingRequest := none, logicalTime := event.logicalTime }
  | .rollback => { state with materialEffects := 0, observedEffects := 0, rolledBack := true, logicalTime := event.logicalTime }

def BoundaryStep (state : BoundaryState) (event : BoundaryEvent) : Option BoundaryState :=
  if BoundaryEventValid state event then some (ApplyBoundaryEvent state event) else none

def BoundaryRun : BoundaryState → List BoundaryEvent → Option BoundaryState
  | state, [] => some state
  | state, event :: tail =>
      match BoundaryStep state event with
      | none => none
      | some next => BoundaryRun next tail

theorem accepted_authorization_respects_caller_ceiling
    {state next : BoundaryState} {event : BoundaryEvent}
    (kind : event.kind = BoundaryEventKind.authorize)
    (accepted : BoundaryStep state event = some next) :
    event.grantAuthority ≤ state.callerCeiling := by
  unfold BoundaryStep at accepted
  split at accepted
  · rename_i valid
    simp [BoundaryEventValid, kind] at valid
    omega
  · simp at accepted

theorem accepted_effect_requires_live_grant_and_dispatch
    {state next : BoundaryState} {event : BoundaryEvent}
    (kind : event.kind = BoundaryEventKind.commitEffect)
    (accepted : BoundaryStep state event = some next) :
    state.activeGrant = some event.grantAuthority ∧
      state.dispatchReceipt = true ∧ state.revoked = false := by
  unfold BoundaryStep at accepted
  split at accepted
  · rename_i valid
    simp [BoundaryEventValid, kind] at valid
    exact ⟨valid.2.1.1.1.1, valid.2.1.1.2, valid.2.1.2⟩
  · simp at accepted

def boundaryInitial : BoundaryState where
  callerCeiling := 3
  activeGrant := none
  authorityEpoch := 11
  revoked := false
  pendingRequest := none
  dispatchReceipt := false
  materialEffects := 0
  observedEffects := 0
  rolledBack := false
  logicalTime := 0

def boundaryBaseEvent : BoundaryEvent where
  kind := .request
  requestedAuthority := 3
  grantAuthority := 3
  authorityEpoch := 11
  logicalTime := 1
  targetOwnerApproved := true
  receiptPresent := true
  independentObservation := true
  rollbackExact := true

def reachableEffectTrace : List BoundaryEvent := [
  boundaryBaseEvent,
  { boundaryBaseEvent with kind := .authorize, logicalTime := 2 },
  { boundaryBaseEvent with kind := .dispatch, logicalTime := 3 },
  { boundaryBaseEvent with kind := .commitEffect, logicalTime := 4 },
  { boundaryBaseEvent with kind := .observe, logicalTime := 5 },
  { boundaryBaseEvent with kind := .rollback, logicalTime := 6 } ]

theorem reachable_effect_trace_rolls_back_exactly :
    BoundaryRun boundaryInitial reachableEffectTrace = some
      { boundaryInitial with
        activeGrant := some 3
        pendingRequest := some 3
        dispatchReceipt := true
        rolledBack := true
        logicalTime := 6 } := by
  decide

theorem over_ceiling_authorization_is_rejected :
    BoundaryStep { boundaryInitial with
        pendingRequest := some 4 }
      { boundaryBaseEvent with
        kind := .authorize
        requestedAuthority := 4
        grantAuthority := 4
        logicalTime := 2 } = none := by
  decide

theorem effect_without_dispatch_receipt_is_rejected :
    BoundaryStep { boundaryInitial with
        activeGrant := some 3 }
      { boundaryBaseEvent with
        kind := .commitEffect
        logicalTime := 4 } = none := by
  decide

theorem revoked_grant_effect_is_rejected :
    BoundaryStep { boundaryInitial with
      activeGrant := none
      authorityEpoch := 12
      revoked := true
      logicalTime := 3 }
      { boundaryBaseEvent with
        kind := .commitEffect
        authorityEpoch := 11
        logicalTime := 4 } = none := by
  decide

end AsiStackProofs.StackBoundaries

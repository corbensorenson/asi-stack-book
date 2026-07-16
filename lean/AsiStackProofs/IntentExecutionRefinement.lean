namespace AsiStackProofs.IntentExecutionRefinement

inductive VerticalLayer where
  | intent | command | plan | job | authorized | dispatched
  | effectAttempted | effectObserved | artifactBound | verified
  | delivered | blocked | residualized | rolledBack | quarantined
deriving DecidableEq, Repr

inductive VerticalEventKind where
  | lowerCommand | lowerPlan | lowerJob | authorize | dispatch
  | attemptEffect | observeEffect | bindArtifact | verify | deliver
  | block | residualize | rollback | quarantine
deriving DecidableEq, Repr

structure VerticalState where
  layer : VerticalLayer
  rootContract : Nat
  currentArtifact : Nat
  authorityCeiling : Nat
  activeAuthority : Nat
  requiredApproval : Bool
  approvalPresent : Bool
  dispatchReceipt : Bool
  attemptedEffects : Nat
  observedEffects : Nat
  artifactBound : Bool
  verificationComplete : Bool
  delivered : Bool
  openResiduals : Nat
  stopped : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure VerticalEvent where
  kind : VerticalEventKind
  fromLayer : VerticalLayer
  toLayer : VerticalLayer
  rootContract : Nat
  parentArtifact : Nat
  outputArtifact : Nat
  requestedAuthority : Nat
  approvalReceipt : Bool
  dispatchReceipt : Bool
  hiddenOverrideApplied : Bool
  effectDelta : Nat
  observationDelta : Nat
  observationReceipt : Bool
  artifactParentBound : Bool
  independentVerifier : Bool
  verificationReceipt : Bool
  deliveryReceipt : Bool
  blockReceipt : Bool
  residualDelta : Nat
  rollbackExact : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def EventSpecificValid (state : VerticalState) (event : VerticalEvent) : Bool :=
  match event.kind with
  | .lowerCommand =>
      decide (event.fromLayer = .intent) && decide (event.toLayer = .command)
  | .lowerPlan =>
      decide (event.fromLayer = .command) && decide (event.toLayer = .plan)
  | .lowerJob =>
      decide (event.fromLayer = .plan) && decide (event.toLayer = .job)
  | .authorize =>
      decide (event.fromLayer = .job) && decide (event.toLayer = .authorized) &&
        (!state.requiredApproval || event.approvalReceipt)
  | .dispatch =>
      decide (event.fromLayer = .authorized) && decide (event.toLayer = .dispatched) &&
        state.approvalPresent && event.dispatchReceipt
  | .attemptEffect =>
      decide (event.fromLayer = .dispatched) && decide (event.toLayer = .effectAttempted) &&
        state.dispatchReceipt && decide (event.effectDelta = 1)
  | .observeEffect =>
      decide (event.fromLayer = .effectAttempted) && decide (event.toLayer = .effectObserved) &&
        decide (state.observedEffects < state.attemptedEffects) &&
        decide (event.observationDelta = 1) && event.observationReceipt
  | .bindArtifact =>
      decide (event.fromLayer = .effectObserved) && decide (event.toLayer = .artifactBound) &&
        decide (0 < state.observedEffects) && event.artifactParentBound
  | .verify =>
      decide (event.fromLayer = .artifactBound) && decide (event.toLayer = .verified) &&
        state.artifactBound && event.independentVerifier && event.verificationReceipt
  | .deliver =>
      decide (event.fromLayer = .verified) && decide (event.toLayer = .delivered) &&
        state.verificationComplete &&
        decide (state.observedEffects = state.attemptedEffects) &&
        event.deliveryReceipt
  | .block =>
      decide (event.toLayer = .blocked) && event.blockReceipt &&
        decide (event.effectDelta = 0)
  | .residualize =>
      decide (event.toLayer = .residualized) && decide (0 < event.residualDelta)
  | .rollback =>
      decide (event.toLayer = .rolledBack) && decide (0 < state.attemptedEffects) &&
        decide (state.observedEffects = state.attemptedEffects) &&
        event.rollbackExact
  | .quarantine =>
      decide (event.toLayer = .quarantined) && event.blockReceipt &&
        decide (0 < event.residualDelta)

def VerticalEventValid (state : VerticalState) (event : VerticalEvent) : Prop :=
  state.layer = event.fromLayer ∧
    state.rootContract = event.rootContract ∧
    state.currentArtifact = event.parentArtifact ∧
    state.logicalTime < event.logicalTime ∧
    event.requestedAuthority ≤ state.authorityCeiling ∧
    event.hiddenOverrideApplied = false ∧
    EventSpecificValid state event = true

instance verticalEventValidDecidable (state : VerticalState) (event : VerticalEvent) :
    Decidable (VerticalEventValid state event) := by
  unfold VerticalEventValid
  infer_instance

def ApplyVerticalEvent (state : VerticalState) (event : VerticalEvent) : VerticalState :=
  { state with
    layer := event.toLayer
    currentArtifact := event.outputArtifact
    activeAuthority := event.requestedAuthority
    approvalPresent := state.approvalPresent || event.approvalReceipt
    dispatchReceipt := state.dispatchReceipt || event.dispatchReceipt
    attemptedEffects := state.attemptedEffects + event.effectDelta
    observedEffects := state.observedEffects + event.observationDelta
    artifactBound := state.artifactBound || event.artifactParentBound
    verificationComplete := state.verificationComplete || event.verificationReceipt
    delivered := state.delivered || event.deliveryReceipt
    openResiduals := state.openResiduals + event.residualDelta
    stopped := state.stopped || event.blockReceipt
    logicalTime := event.logicalTime }

def VerticalStep (state : VerticalState) (event : VerticalEvent) : Option VerticalState :=
  if VerticalEventValid state event then some (ApplyVerticalEvent state event) else none

def VerticalRun : VerticalState → List VerticalEvent → Option VerticalState
  | state, [] => some state
  | state, event :: tail =>
      match VerticalStep state event with
      | none => none
      | some next => VerticalRun next tail

theorem accepted_step_is_valid
    {state next : VerticalState} {event : VerticalEvent}
    (accepted : VerticalStep state event = some next) :
    VerticalEventValid state event := by
  unfold VerticalStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_step_preserves_root_and_parent
    {state next : VerticalState} {event : VerticalEvent}
    (accepted : VerticalStep state event = some next) :
    state.rootContract = event.rootContract ∧
      state.currentArtifact = event.parentArtifact := by
  rcases accepted_step_is_valid accepted with ⟨_, root, parent, _⟩
  exact ⟨root, parent⟩

theorem accepted_step_cannot_widen_authority
    {state next : VerticalState} {event : VerticalEvent}
    (accepted : VerticalStep state event = some next) :
    event.requestedAuthority ≤ state.authorityCeiling := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, ceiling, _⟩
  exact ceiling

theorem accepted_dispatch_requires_approval_and_receipt
    {state next : VerticalState} {event : VerticalEvent}
    (kind : event.kind = .dispatch)
    (accepted : VerticalStep state event = some next) :
    state.approvalPresent = true ∧ event.dispatchReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, _, _, specific⟩
  simp [EventSpecificValid, kind] at specific
  exact ⟨specific.1.2, specific.2⟩

theorem accepted_effect_requires_prior_dispatch
    {state next : VerticalState} {event : VerticalEvent}
    (kind : event.kind = .attemptEffect)
    (accepted : VerticalStep state event = some next) :
    state.dispatchReceipt = true ∧ event.effectDelta = 1 := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, _, _, specific⟩
  simp [EventSpecificValid, kind] at specific
  exact ⟨specific.1.2, specific.2⟩

theorem accepted_delivery_requires_verified_observed_effect
    {state next : VerticalState} {event : VerticalEvent}
    (kind : event.kind = .deliver)
    (accepted : VerticalStep state event = some next) :
    state.verificationComplete = true ∧
      state.observedEffects = state.attemptedEffects ∧
      event.deliveryReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, _, _, specific⟩
  simp [EventSpecificValid, kind] at specific
  exact ⟨specific.1.1.2, specific.1.2, specific.2⟩

def verticalInitial : VerticalState where
  layer := .intent
  rootContract := 101
  currentArtifact := 1001
  authorityCeiling := 3
  activeAuthority := 0
  requiredApproval := true
  approvalPresent := false
  dispatchReceipt := false
  attemptedEffects := 0
  observedEffects := 0
  artifactBound := false
  verificationComplete := false
  delivered := false
  openResiduals := 0
  stopped := false
  logicalTime := 0

def baseEvent : VerticalEvent where
  kind := .lowerCommand
  fromLayer := .intent
  toLayer := .command
  rootContract := 101
  parentArtifact := 1001
  outputArtifact := 1002
  requestedAuthority := 3
  approvalReceipt := false
  dispatchReceipt := false
  hiddenOverrideApplied := false
  effectDelta := 0
  observationDelta := 0
  observationReceipt := false
  artifactParentBound := false
  independentVerifier := false
  verificationReceipt := false
  deliveryReceipt := false
  blockReceipt := false
  residualDelta := 0
  rollbackExact := false
  logicalTime := 1

def verticalDeliveredTrace : List VerticalEvent := [
  baseEvent,
  { baseEvent with
      kind := .lowerPlan
      fromLayer := .command
      toLayer := .plan
      parentArtifact := 1002
      outputArtifact := 1003
      logicalTime := 2 },
  { baseEvent with
      kind := .lowerJob
      fromLayer := .plan
      toLayer := .job
      parentArtifact := 1003
      outputArtifact := 1004
      logicalTime := 3 },
  { baseEvent with
      kind := .authorize
      fromLayer := .job
      toLayer := .authorized
      parentArtifact := 1004
      outputArtifact := 1005
      approvalReceipt := true
      logicalTime := 4 },
  { baseEvent with
      kind := .dispatch
      fromLayer := .authorized
      toLayer := .dispatched
      parentArtifact := 1005
      outputArtifact := 1006
      dispatchReceipt := true
      logicalTime := 5 },
  { baseEvent with
      kind := .attemptEffect
      fromLayer := .dispatched
      toLayer := .effectAttempted
      parentArtifact := 1006
      outputArtifact := 1007
      effectDelta := 1
      logicalTime := 6 },
  { baseEvent with
      kind := .observeEffect
      fromLayer := .effectAttempted
      toLayer := .effectObserved
      parentArtifact := 1007
      outputArtifact := 1008
      observationDelta := 1
      observationReceipt := true
      logicalTime := 7 },
  { baseEvent with
      kind := .bindArtifact
      fromLayer := .effectObserved
      toLayer := .artifactBound
      parentArtifact := 1008
      outputArtifact := 1009
      artifactParentBound := true
      logicalTime := 8 },
  { baseEvent with
      kind := .verify
      fromLayer := .artifactBound
      toLayer := .verified
      parentArtifact := 1009
      outputArtifact := 1010
      independentVerifier := true
      verificationReceipt := true
      logicalTime := 9 },
  { baseEvent with
      kind := .deliver
      fromLayer := .verified
      toLayer := .delivered
      parentArtifact := 1010
      outputArtifact := 1011
      deliveryReceipt := true
      logicalTime := 10 }
]

theorem full_vertical_trace_reaches_exact_delivery :
    VerticalRun verticalInitial verticalDeliveredTrace = some
      { verticalInitial with
        layer := .delivered
        currentArtifact := 1011
        activeAuthority := 3
        approvalPresent := true
        dispatchReceipt := true
        attemptedEffects := 1
        observedEffects := 1
        artifactBound := true
        verificationComplete := true
        delivered := true
        logicalTime := 10 } := by
  native_decide

theorem missing_approval_authorization_is_rejected :
    VerticalStep
      { verticalInitial with
          layer := .job
          currentArtifact := 1004
          logicalTime := 3 }
      { baseEvent with
          kind := .authorize
          fromLayer := .job
          toLayer := .authorized
          parentArtifact := 1004
          outputArtifact := 1005
          logicalTime := 4 } = none := by
  native_decide

theorem authority_widening_is_rejected :
    VerticalStep verticalInitial { baseEvent with requestedAuthority := 4 } = none := by
  native_decide

theorem hidden_override_is_rejected :
    VerticalStep verticalInitial { baseEvent with hiddenOverrideApplied := true } = none := by
  native_decide

theorem effect_without_dispatch_is_rejected :
    VerticalStep
      { verticalInitial with
          layer := .dispatched
          currentArtifact := 1006
          logicalTime := 5 }
      { baseEvent with
          kind := .attemptEffect
          fromLayer := .dispatched
          toLayer := .effectAttempted
          parentArtifact := 1006
          outputArtifact := 1007
          effectDelta := 1
          logicalTime := 6 } = none := by
  native_decide

theorem delivery_without_verification_is_rejected :
    VerticalStep
      { verticalInitial with
          layer := .verified
          currentArtifact := 1010
          approvalPresent := true
          dispatchReceipt := true
          attemptedEffects := 1
          observedEffects := 1
          logicalTime := 9 }
      { baseEvent with
          kind := .deliver
          fromLayer := .verified
          toLayer := .delivered
          parentArtifact := 1010
          outputArtifact := 1011
          deliveryReceipt := true
          logicalTime := 10 } = none := by
  native_decide

end AsiStackProofs.IntentExecutionRefinement

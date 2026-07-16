namespace AsiStackProofs.IntentResolutionRefinement

inductive IntentStage where
  | received | parsed | clarified | authorityReviewed | accepted
  | recontractRequired | rejected
deriving DecidableEq, Repr

inductive IntentEventKind where
  | parse | clarify | reviewAuthority | compile | continueContract
  | detectMaterialDelta | acceptRecontract | reject
deriving DecidableEq, Repr

structure IntentState where
  stage : IntentStage
  rootIntent : Nat
  contractVersion : Nat
  constraintHash : Nat
  stopHash : Nat
  authorityCeiling : Nat
  approvedAuthority : Nat
  ambiguityOpen : Bool
  contractAccepted : Bool
  recontractRequired : Bool
  blocked : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure IntentEvent where
  kind : IntentEventKind
  fromStage : IntentStage
  toStage : IntentStage
  rootIntent : Nat
  inputVersion : Nat
  outputVersion : Nat
  sourceConstraintHash : Nat
  sourceStopHash : Nat
  outputConstraintHash : Nat
  outputStopHash : Nat
  requestedAuthority : Nat
  prohibitedAction : Bool
  hiddenOverride : Bool
  ambiguityPresent : Bool
  clarificationReceipt : Bool
  authorityReceipt : Bool
  meansExpanded : Bool
  authorityExpanded : Bool
  evidenceWeakened : Bool
  stopDropped : Bool
  affectedPartiesExpanded : Bool
  supportPromotionRequested : Bool
  recontractReceipt : Bool
  blockReceipt : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def MaterialDelta (event : IntentEvent) : Bool :=
  event.meansExpanded || event.authorityExpanded || event.evidenceWeakened ||
    event.stopDropped || event.affectedPartiesExpanded ||
      event.supportPromotionRequested

def EventSpecificValid (state : IntentState) (event : IntentEvent) : Bool :=
  match event.kind with
  | .parse =>
      decide (event.fromStage = .received) && decide (event.toStage = .parsed) &&
        decide (0 < event.sourceConstraintHash) && decide (0 < event.sourceStopHash) &&
        !event.prohibitedAction && !event.hiddenOverride
  | .clarify =>
      decide (event.fromStage = .parsed) && decide (event.toStage = .clarified) &&
        state.ambiguityOpen && event.ambiguityPresent && event.clarificationReceipt
  | .reviewAuthority =>
      decide (event.toStage = .authorityReviewed) &&
        decide (event.fromStage = .parsed ∨ event.fromStage = .clarified) &&
        !state.ambiguityOpen && event.authorityReceipt &&
        decide (event.requestedAuthority ≤ state.authorityCeiling)
  | .compile =>
      decide (event.fromStage = .authorityReviewed) &&
        decide (event.toStage = .accepted) &&
        decide (event.sourceConstraintHash = state.constraintHash) &&
        decide (event.sourceStopHash = state.stopHash) &&
        decide (event.outputConstraintHash = state.constraintHash) &&
        decide (event.outputStopHash = state.stopHash) &&
        decide (event.requestedAuthority = state.approvedAuthority) &&
        !event.hiddenOverride && !event.prohibitedAction && !event.ambiguityPresent
  | .continueContract =>
      decide (event.fromStage = .accepted) && decide (event.toStage = .accepted) &&
        !MaterialDelta event && !state.recontractRequired
  | .detectMaterialDelta =>
      decide (event.fromStage = .accepted) &&
        decide (event.toStage = .recontractRequired) && MaterialDelta event
  | .acceptRecontract =>
      decide (event.fromStage = .recontractRequired) &&
        decide (event.toStage = .accepted) && state.recontractRequired &&
        event.recontractReceipt && decide (state.contractVersion < event.outputVersion) &&
        decide (0 < event.outputConstraintHash) && decide (0 < event.outputStopHash) &&
        decide (event.requestedAuthority ≤ state.authorityCeiling)
  | .reject =>
      decide (event.toStage = .rejected) && event.blockReceipt

def IntentEventValid (state : IntentState) (event : IntentEvent) : Prop :=
  state.stage = event.fromStage ∧
    state.rootIntent = event.rootIntent ∧
    state.contractVersion = event.inputVersion ∧
    state.logicalTime < event.logicalTime ∧
    EventSpecificValid state event = true

instance intentEventValidDecidable (state : IntentState) (event : IntentEvent) :
    Decidable (IntentEventValid state event) := by
  unfold IntentEventValid
  infer_instance

def ApplyIntentEvent (state : IntentState) (event : IntentEvent) : IntentState :=
  { state with
    stage := event.toStage
    contractVersion := event.outputVersion
    constraintHash := if event.outputConstraintHash = 0 then state.constraintHash else event.outputConstraintHash
    stopHash := if event.outputStopHash = 0 then state.stopHash else event.outputStopHash
    approvedAuthority := if event.authorityReceipt then event.requestedAuthority else state.approvedAuthority
    ambiguityOpen := if event.kind = .clarify then false else state.ambiguityOpen || event.ambiguityPresent
    contractAccepted := event.toStage = .accepted
    recontractRequired := event.toStage = .recontractRequired
    blocked := state.blocked || event.blockReceipt
    logicalTime := event.logicalTime }

def IntentStep (state : IntentState) (event : IntentEvent) : Option IntentState :=
  if IntentEventValid state event then some (ApplyIntentEvent state event) else none

def IntentRun : IntentState → List IntentEvent → Option IntentState
  | state, [] => some state
  | state, event :: tail =>
      match IntentStep state event with
      | none => none
      | some next => IntentRun next tail

theorem accepted_step_is_valid
    {state next : IntentState} {event : IntentEvent}
    (accepted : IntentStep state event = some next) :
    IntentEventValid state event := by
  unfold IntentStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_compile_preserves_constraints_stops_and_authority
    {state next : IntentState} {event : IntentEvent}
    (kind : event.kind = .compile)
    (accepted : IntentStep state event = some next) :
    event.outputConstraintHash = state.constraintHash ∧
      event.outputStopHash = state.stopHash ∧
      event.requestedAuthority = state.approvedAuthority := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, specific⟩
  simp [EventSpecificValid, kind] at specific
  have fields :
      event.fromStage = .authorityReviewed ∧ event.toStage = .accepted ∧
        event.sourceConstraintHash = state.constraintHash ∧
        event.sourceStopHash = state.stopHash ∧
        event.outputConstraintHash = state.constraintHash ∧
        event.outputStopHash = state.stopHash ∧
        event.requestedAuthority = state.approvedAuthority ∧
        event.hiddenOverride = false ∧ event.prohibitedAction = false ∧
        event.ambiguityPresent = false := by
    simpa [and_assoc] using specific
  rcases fields with ⟨_, _, _, _, outputConstraint, outputStop, authority, _⟩
  exact ⟨outputConstraint, outputStop, authority⟩

theorem accepted_material_delta_requires_recontract_state
    {state next : IntentState} {event : IntentEvent}
    (kind : event.kind = .detectMaterialDelta)
    (accepted : IntentStep state event = some next) :
    MaterialDelta event = true ∧ event.toStage = .recontractRequired := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, specific⟩
  simp [EventSpecificValid, kind] at specific
  have fields :
      event.fromStage = .accepted ∧ event.toStage = .recontractRequired ∧
        MaterialDelta event = true := by
    simpa [and_assoc] using specific
  exact ⟨fields.2.2, fields.2.1⟩

theorem accepted_recontract_increments_version_and_respects_ceiling
    {state next : IntentState} {event : IntentEvent}
    (kind : event.kind = .acceptRecontract)
    (accepted : IntentStep state event = some next) :
    state.contractVersion < event.outputVersion ∧
      event.requestedAuthority ≤ state.authorityCeiling := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, specific⟩
  simp [EventSpecificValid, kind] at specific
  have fields :
      event.fromStage = .recontractRequired ∧ event.toStage = .accepted ∧
        state.recontractRequired = true ∧ event.recontractReceipt = true ∧
        state.contractVersion < event.outputVersion ∧
        0 < event.outputConstraintHash ∧ 0 < event.outputStopHash ∧
        event.requestedAuthority ≤ state.authorityCeiling := by
    simpa [and_assoc] using specific
  exact ⟨fields.2.2.2.2.1, fields.2.2.2.2.2.2.2⟩

def initialState : IntentState where
  stage := .received
  rootIntent := 101
  contractVersion := 1
  constraintHash := 0
  stopHash := 0
  authorityCeiling := 3
  approvedAuthority := 0
  ambiguityOpen := false
  contractAccepted := false
  recontractRequired := false
  blocked := false
  logicalTime := 0

def baseEvent : IntentEvent where
  kind := .parse
  fromStage := .received
  toStage := .parsed
  rootIntent := 101
  inputVersion := 1
  outputVersion := 1
  sourceConstraintHash := 501
  sourceStopHash := 601
  outputConstraintHash := 501
  outputStopHash := 601
  requestedAuthority := 3
  prohibitedAction := false
  hiddenOverride := false
  ambiguityPresent := false
  clarificationReceipt := false
  authorityReceipt := false
  meansExpanded := false
  authorityExpanded := false
  evidenceWeakened := false
  stopDropped := false
  affectedPartiesExpanded := false
  supportPromotionRequested := false
  recontractReceipt := false
  blockReceipt := false
  logicalTime := 1

def acceptedIntentTrace : List IntentEvent := [
  baseEvent,
  { baseEvent with
      kind := .reviewAuthority
      fromStage := .parsed
      toStage := .authorityReviewed
      authorityReceipt := true
      logicalTime := 2 },
  { baseEvent with
      kind := .compile
      fromStage := .authorityReviewed
      toStage := .accepted
      authorityReceipt := true
      logicalTime := 3 }
]

theorem exact_intent_trace_reaches_accepted_contract :
    IntentRun initialState acceptedIntentTrace = some
      { initialState with
        stage := .accepted
        constraintHash := 501
        stopHash := 601
        approvedAuthority := 3
        contractAccepted := true
        logicalTime := 3 } := by
  native_decide

def acceptedState : IntentState :=
  { initialState with
      stage := .accepted
      constraintHash := 501
      stopHash := 601
      approvedAuthority := 3
      contractAccepted := true
      logicalTime := 3 }

theorem missing_intent_payload_is_rejected :
    IntentStep initialState { baseEvent with sourceConstraintHash := 0 } = none := by
  native_decide

theorem prohibited_action_is_rejected :
    IntentStep initialState { baseEvent with prohibitedAction := true } = none := by
  native_decide

theorem hidden_override_is_rejected :
    IntentStep initialState { baseEvent with hiddenOverride := true } = none := by
  native_decide

theorem authority_widening_is_rejected :
    IntentStep
      { initialState with stage := .parsed, constraintHash := 501, stopHash := 601, logicalTime := 1 }
      { baseEvent with
          kind := .reviewAuthority
          fromStage := .parsed
          toStage := .authorityReviewed
          requestedAuthority := 4
          authorityReceipt := true
          logicalTime := 2 } = none := by
  native_decide

theorem compiled_constraint_substitution_is_rejected :
    IntentStep
      { initialState with stage := .authorityReviewed, constraintHash := 501, stopHash := 601, approvedAuthority := 3, logicalTime := 2 }
      { baseEvent with
          kind := .compile
          fromStage := .authorityReviewed
          toStage := .accepted
          outputConstraintHash := 999
          authorityReceipt := true
          logicalTime := 3 } = none := by
  native_decide

theorem material_delta_cannot_silently_continue :
    IntentStep acceptedState
      { baseEvent with
          kind := .continueContract
          fromStage := .accepted
          toStage := .accepted
          meansExpanded := true
          logicalTime := 4 } = none := by
  native_decide

theorem recontract_without_receipt_is_rejected :
    IntentStep
      { acceptedState with stage := .recontractRequired, recontractRequired := true, logicalTime := 4 }
      { baseEvent with
          kind := .acceptRecontract
          fromStage := .recontractRequired
          toStage := .accepted
          inputVersion := 1
          outputVersion := 2
          logicalTime := 5 } = none := by
  native_decide

end AsiStackProofs.IntentResolutionRefinement

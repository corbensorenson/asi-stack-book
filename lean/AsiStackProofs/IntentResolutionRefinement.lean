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
        decide (event.outputVersion = event.inputVersion) &&
        decide (event.outputConstraintHash = event.sourceConstraintHash) &&
        decide (event.outputStopHash = event.sourceStopHash) &&
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
  match event.kind with
  | .parse =>
      { state with
        stage := event.toStage
        constraintHash := event.outputConstraintHash
        stopHash := event.outputStopHash
        ambiguityOpen := event.ambiguityPresent
        contractAccepted := false
        recontractRequired := false
        logicalTime := event.logicalTime }
  | .clarify =>
      { state with
        stage := event.toStage
        ambiguityOpen := false
        contractAccepted := false
        recontractRequired := false
        logicalTime := event.logicalTime }
  | .reviewAuthority =>
      { state with
        stage := event.toStage
        approvedAuthority := event.requestedAuthority
        contractAccepted := false
        recontractRequired := false
        logicalTime := event.logicalTime }
  | .compile | .continueContract =>
      { state with
        stage := event.toStage
        contractAccepted := true
        recontractRequired := false
        logicalTime := event.logicalTime }
  | .detectMaterialDelta =>
      { state with
        stage := event.toStage
        contractAccepted := false
        recontractRequired := true
        logicalTime := event.logicalTime }
  | .acceptRecontract =>
      { state with
        stage := event.toStage
        contractVersion := event.outputVersion
        constraintHash := event.outputConstraintHash
        stopHash := event.outputStopHash
        approvedAuthority := event.requestedAuthority
        contractAccepted := true
        recontractRequired := false
        logicalTime := event.logicalTime }
  | .reject =>
      { state with
        stage := event.toStage
        contractAccepted := false
        recontractRequired := false
        blocked := true
        logicalTime := event.logicalTime }

def IntentStep (state : IntentState) (event : IntentEvent) : Option IntentState :=
  if IntentEventValid state event then some (ApplyIntentEvent state event) else none

def IntentRun : IntentState → List IntentEvent → Option IntentState
  | state, [] => some state
  | state, event :: tail =>
      match IntentStep state event with
      | none => none
      | some next => IntentRun next tail

def IntentTraceValid : IntentState → List IntentEvent → Prop
  | _, [] => True
  | state, event :: tail =>
      IntentEventValid state event ∧
        IntentTraceValid (ApplyIntentEvent state event) tail

theorem accepted_step_is_valid
    {state next : IntentState} {event : IntentEvent}
    (accepted : IntentStep state event = some next) :
    IntentEventValid state event := by
  unfold IntentStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_step_applies_event
    {state next : IntentState} {event : IntentEvent}
    (accepted : IntentStep state event = some next) :
    next = ApplyIntentEvent state event := by
  unfold IntentStep at accepted
  split at accepted
  · exact Option.some.inj accepted |>.symm
  · simp at accepted

theorem apply_event_preserves_root_intent
    (state : IntentState) (event : IntentEvent) :
    (ApplyIntentEvent state event).rootIntent = state.rootIntent := by
  unfold ApplyIntentEvent
  split <;> rfl

theorem apply_event_preserves_authority_ceiling
    (state : IntentState) (event : IntentEvent) :
    (ApplyIntentEvent state event).authorityCeiling = state.authorityCeiling := by
  unfold ApplyIntentEvent
  split <;> rfl

theorem accepted_step_preserves_approved_authority_ceiling
    {state next : IntentState} {event : IntentEvent}
    (bounded : state.approvedAuthority ≤ state.authorityCeiling)
    (accepted : IntentStep state event = some next) :
    next.approvedAuthority ≤ next.authorityCeiling := by
  have valid := accepted_step_is_valid accepted
  have applies := accepted_step_applies_event accepted
  subst next
  rcases valid with ⟨_, _, _, _, specific⟩
  cases kind : event.kind
  · simpa [ApplyIntentEvent, kind] using bounded
  · simpa [ApplyIntentEvent, kind] using bounded
  · simp [EventSpecificValid, kind] at specific
    have fields :
        event.toStage = .authorityReviewed ∧
          (event.fromStage = .parsed ∨ event.fromStage = .clarified) ∧
          state.ambiguityOpen = false ∧ event.authorityReceipt = true ∧
          event.requestedAuthority ≤ state.authorityCeiling := by
      simpa [and_assoc] using specific
    simpa [ApplyIntentEvent, kind] using fields.2.2.2.2
  · simpa [ApplyIntentEvent, kind] using bounded
  · simpa [ApplyIntentEvent, kind] using bounded
  · simpa [ApplyIntentEvent, kind] using bounded
  · simp [EventSpecificValid, kind] at specific
    have fields :
        event.fromStage = .recontractRequired ∧ event.toStage = .accepted ∧
          state.recontractRequired = true ∧ event.recontractReceipt = true ∧
          state.contractVersion < event.outputVersion ∧
          0 < event.outputConstraintHash ∧ 0 < event.outputStopHash ∧
          event.requestedAuthority ≤ state.authorityCeiling := by
      simpa [and_assoc] using specific
    simpa [ApplyIntentEvent, kind] using fields.2.2.2.2.2.2.2
  · simpa [ApplyIntentEvent, kind] using bounded

theorem successful_run_preserves_root_and_ceiling
    {state final : IntentState} {events : List IntentEvent}
    (ran : IntentRun state events = some final) :
    final.rootIntent = state.rootIntent ∧
      final.authorityCeiling = state.authorityCeiling := by
  induction events generalizing state with
  | nil =>
      simp [IntentRun] at ran
      subst final
      exact ⟨rfl, rfl⟩
  | cons event tail ih =>
      cases stepped : IntentStep state event with
      | none => simp [IntentRun, stepped] at ran
      | some next =>
          have tailRan : IntentRun next tail = some final := by
            simpa [IntentRun, stepped] using ran
          rcases ih tailRan with ⟨root, ceiling⟩
          have applies := accepted_step_applies_event stepped
          subst next
          exact ⟨root.trans (apply_event_preserves_root_intent state event),
            ceiling.trans (apply_event_preserves_authority_ceiling state event)⟩

theorem successful_run_preserves_approved_authority_ceiling
    {state final : IntentState} {events : List IntentEvent}
    (bounded : state.approvedAuthority ≤ state.authorityCeiling)
    (ran : IntentRun state events = some final) :
    final.approvedAuthority ≤ final.authorityCeiling := by
  induction events generalizing state with
  | nil =>
      simp [IntentRun] at ran
      subst final
      exact bounded
  | cons event tail ih =>
      cases stepped : IntentStep state event with
      | none => simp [IntentRun, stepped] at ran
      | some next =>
          have tailRan : IntentRun next tail = some final := by
            simpa [IntentRun, stepped] using ran
          exact ih (accepted_step_preserves_approved_authority_ceiling bounded stepped)
            tailRan

theorem successful_run_has_valid_trace
    {state final : IntentState} {events : List IntentEvent}
    (ran : IntentRun state events = some final) :
    IntentTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : IntentStep state event with
      | none => simp [IntentRun, stepped] at ran
      | some next =>
          have tailRan : IntentRun next tail = some final := by
            simpa [IntentRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          subst next
          exact ⟨accepted_step_is_valid stepped, ih tailRan⟩

theorem run_composes_across_intent_batches
    (state : IntentState) (left right : List IntentEvent) :
    IntentRun state (left ++ right) =
      match IntentRun state left with
      | none => none
      | some middle => IntentRun middle right := by
  induction left generalizing state with
  | nil => simp [IntentRun]
  | cons event tail ih =>
      cases stepped : IntentStep state event <;>
        simp [IntentRun, stepped, ih]

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

structure IntentMeaning where
  desiredOutcome : Nat
  allowedMeans : Nat
  forbiddenMeans : Nat
  authorityBasis : Nat
  authorityCeiling : Nat
  affectedParties : Nat
  privacyBoundary : Nat
  acceptanceEvidence : Nat
  stopConditions : Nat
  permittedConsumers : Nat
deriving DecidableEq, Repr

structure ThinCommand where
  desiredOutcome : Nat
  allowedMeans : Nat
  authorityCeiling : Nat
  stopConditions : Nat
deriving DecidableEq, Repr

structure LosslessCommand where
  desiredOutcome : Nat
  allowedMeans : Nat
  forbiddenMeans : Nat
  authorityBasis : Nat
  authorityCeiling : Nat
  affectedParties : Nat
  privacyBoundary : Nat
  acceptanceEvidence : Nat
  stopConditions : Nat
  permittedConsumers : Nat
deriving DecidableEq, Repr

def ThinLower (intent : IntentMeaning) : ThinCommand :=
  { desiredOutcome := intent.desiredOutcome
    allowedMeans := intent.allowedMeans
    authorityCeiling := intent.authorityCeiling
    stopConditions := intent.stopConditions }

def LosslessLower (intent : IntentMeaning) : LosslessCommand :=
  { desiredOutcome := intent.desiredOutcome
    allowedMeans := intent.allowedMeans
    forbiddenMeans := intent.forbiddenMeans
    authorityBasis := intent.authorityBasis
    authorityCeiling := intent.authorityCeiling
    affectedParties := intent.affectedParties
    privacyBoundary := intent.privacyBoundary
    acceptanceEvidence := intent.acceptanceEvidence
    stopConditions := intent.stopConditions
    permittedConsumers := intent.permittedConsumers }

def collisionIntentA : IntentMeaning :=
  { desiredOutcome := 1, allowedMeans := 2, forbiddenMeans := 3,
    authorityBasis := 4, authorityCeiling := 5, affectedParties := 6,
    privacyBoundary := 7, acceptanceEvidence := 8, stopConditions := 9,
    permittedConsumers := 10 }

def collisionIntentB : IntentMeaning :=
  { collisionIntentA with
    affectedParties := 60
    privacyBoundary := 70
    acceptanceEvidence := 80
    permittedConsumers := 100 }

theorem thin_lowering_has_distinct_intent_collision :
    collisionIntentA ≠ collisionIntentB ∧
      ThinLower collisionIntentA = ThinLower collisionIntentB := by
  decide

theorem no_thin_decoder_recovers_both_colliding_intents
    (decode : ThinCommand -> IntentMeaning) :
    decode (ThinLower collisionIntentA) ≠ collisionIntentA ∨
      decode (ThinLower collisionIntentB) ≠ collisionIntentB := by
  rcases thin_lowering_has_distinct_intent_collision with ⟨distinct, collision⟩
  by_cases recoversA : decode (ThinLower collisionIntentA) = collisionIntentA
  · right
    intro recoversB
    apply distinct
    calc
      collisionIntentA = decode (ThinLower collisionIntentA) := recoversA.symm
      _ = decode (ThinLower collisionIntentB) := congrArg decode collision
      _ = collisionIntentB := recoversB
  · exact Or.inl recoversA

theorem lossless_lowering_is_injective :
    Function.Injective LosslessLower := by
  intro left right equal
  cases left
  cases right
  simp [LosslessLower] at equal ⊢
  exact equal

theorem affected_party_change_changes_lossless_lowering
    (intent : IntentMeaning) (changed : Nat)
    (different : changed ≠ intent.affectedParties) :
    LosslessLower { intent with affectedParties := changed } ≠ LosslessLower intent := by
  intro equal
  have same := congrArg LosslessCommand.affectedParties equal
  simp [LosslessLower] at same
  exact different same

theorem privacy_change_changes_lossless_lowering
    (intent : IntentMeaning) (changed : Nat)
    (different : changed ≠ intent.privacyBoundary) :
    LosslessLower { intent with privacyBoundary := changed } ≠ LosslessLower intent := by
  intro equal
  have same := congrArg LosslessCommand.privacyBoundary equal
  simp [LosslessLower] at same
  exact different same

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

theorem initial_approved_authority_is_within_ceiling :
    initialState.approvedAuthority ≤ initialState.authorityCeiling := by
  decide

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

def clarifiedIntentTrace : List IntentEvent := [
  { baseEvent with ambiguityPresent := true },
  { baseEvent with
      kind := .clarify
      fromStage := .parsed
      toStage := .clarified
      ambiguityPresent := true
      clarificationReceipt := true
      logicalTime := 2 },
  { baseEvent with
      kind := .reviewAuthority
      fromStage := .clarified
      toStage := .authorityReviewed
      authorityReceipt := true
      logicalTime := 3 },
  { baseEvent with
      kind := .compile
      fromStage := .authorityReviewed
      toStage := .accepted
      authorityReceipt := true
      logicalTime := 4 }
]

def continuedIntentTrace : List IntentEvent := acceptedIntentTrace ++ [
  { baseEvent with
      kind := .continueContract
      fromStage := .accepted
      toStage := .accepted
      logicalTime := 4 }
]

def rejectedIntentTrace : List IntentEvent := [
  { baseEvent with
      kind := .reject
      fromStage := .received
      toStage := .rejected
      outputConstraintHash := 0
      outputStopHash := 0
      blockReceipt := true }
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

theorem clarified_trace_reaches_same_bounded_contract :
    IntentRun initialState clarifiedIntentTrace = some
      { initialState with
        stage := .accepted
        constraintHash := 501
        stopHash := 601
        approvedAuthority := 3
        ambiguityOpen := false
        contractAccepted := true
        logicalTime := 4 } := by
  native_decide

theorem unchanged_contract_continues_without_payload_rewrite :
    IntentRun initialState continuedIntentTrace = some
      { initialState with
        stage := .accepted
        constraintHash := 501
        stopHash := 601
        approvedAuthority := 3
        contractAccepted := true
        logicalTime := 4 } := by
  native_decide

theorem rejection_blocks_without_materializing_contract_payload :
    IntentRun initialState rejectedIntentTrace = some
      { initialState with
        stage := .rejected
        blocked := true
        logicalTime := 1 } := by
  native_decide

theorem every_successful_reference_trace_preserves_authority_ceiling :
    ∀ final, IntentRun initialState acceptedIntentTrace = some final →
      final.approvedAuthority ≤ final.authorityCeiling := by
  intro final ran
  exact successful_run_preserves_approved_authority_ceiling
    initial_approved_authority_is_within_ceiling ran

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

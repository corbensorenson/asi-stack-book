namespace AsiStackProofs.CommandSemanticRefinement

/-!
A finite reachable semantic-interface model. Hashes, provenance labels,
confidence labels, approvals, and receipts are abstract trusted inputs; this
model does not claim natural-language semantic equivalence or deployment.
-/

inductive CommandStage where
  | raw | fieldsBound | precedenceChecked | authorityBound
  | planningValidated | dispatchReady | blocked
deriving DecidableEq, Repr

inductive SlotProvenance where
  | humanIntent | policy | source | boundedDefault | untrustedData | hiddenInstruction
deriving DecidableEq, Repr

inductive SlotConfidence where
  | confirmed | policyImposed | sourceDerived | defaulted | inferred | missing
deriving DecidableEq, Repr

def SlotConfidence.dispatchEligible : SlotConfidence -> Bool
  | .confirmed | .policyImposed | .sourceDerived | .defaulted => true
  | .inferred | .missing => false

def SlotConfidence.authorityEligible : SlotConfidence -> Bool
  | .confirmed | .policyImposed => true
  | .sourceDerived | .defaulted | .inferred | .missing => false

def SlotProvenance.controlEligible : SlotProvenance -> Bool
  | .humanIntent | .policy | .source | .boundedDefault => true
  | .untrustedData | .hiddenInstruction => false

structure SemanticSlot where
  valueHash : Nat
  provenance : SlotProvenance
  confidence : SlotConfidence
deriving DecidableEq, Repr

def SemanticSlot.requiredEligible (slot : SemanticSlot) : Bool :=
  decide (0 < slot.valueHash) && slot.provenance.controlEligible &&
    slot.confidence.dispatchEligible

def SemanticSlot.authorityReady (slot : SemanticSlot) : Bool :=
  decide (0 < slot.valueHash) && slot.provenance.controlEligible &&
    slot.confidence.authorityEligible

inductive CommandEventKind where
  | bindFields | checkPrecedence | bindAuthority | validatePlanning
  | requestDispatch | block
deriving DecidableEq, Repr

structure CommandState where
  stage : CommandStage
  rootIntent : Nat
  commandVersion : Nat
  objective : SemanticSlot
  constraints : SemanticSlot
  outputContract : SemanticSlot
  verification : SemanticSlot
  failureBehavior : SemanticSlot
  authority : SemanticSlot
  authorityCeiling : Nat
  approvedAuthority : Nat
  hiddenOverrideSeen : Bool
  planningValidationReceipt : Bool
  dispatchReceipt : Bool
  blocked : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure CommandEvent where
  kind : CommandEventKind
  fromStage : CommandStage
  toStage : CommandStage
  rootIntent : Nat
  inputVersion : Nat
  outputVersion : Nat
  objective : SemanticSlot
  constraints : SemanticSlot
  outputContract : SemanticSlot
  verification : SemanticSlot
  failureBehavior : SemanticSlot
  authority : SemanticSlot
  requestedAuthority : Nat
  constraintSourceHash : Nat
  hiddenOverrideApplied : Bool
  blockerCount : Nat
  approvalReceipt : Bool
  planningValidationReceipt : Bool
  dispatchReceipt : Bool
  blockReceipt : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def SlotsMatchState (state : CommandState) (event : CommandEvent) : Bool :=
  decide (event.objective = state.objective) &&
    decide (event.constraints = state.constraints) &&
    decide (event.outputContract = state.outputContract) &&
    decide (event.verification = state.verification) &&
    decide (event.failureBehavior = state.failureBehavior) &&
    decide (event.authority = state.authority)

def EventSpecificValid (state : CommandState) (event : CommandEvent) : Bool :=
  match event.kind with
  | .bindFields =>
      decide (event.fromStage = .raw) && decide (event.toStage = .fieldsBound) &&
        event.objective.requiredEligible && event.constraints.requiredEligible &&
        event.outputContract.requiredEligible && event.verification.requiredEligible &&
        event.failureBehavior.requiredEligible && decide (0 < event.authority.valueHash)
  | .checkPrecedence =>
      decide (event.fromStage = .fieldsBound) &&
        decide (event.toStage = .precedenceChecked) && SlotsMatchState state event &&
        decide (event.constraintSourceHash = state.constraints.valueHash) &&
        !event.hiddenOverrideApplied
  | .bindAuthority =>
      decide (event.fromStage = .precedenceChecked) &&
        decide (event.toStage = .authorityBound) && SlotsMatchState state event &&
        event.authority.authorityReady &&
        decide (event.requestedAuthority ≤ state.authorityCeiling) &&
        event.approvalReceipt
  | .validatePlanning =>
      decide (event.fromStage = .authorityBound) &&
        decide (event.toStage = .planningValidated) && SlotsMatchState state event &&
        decide (event.requestedAuthority = state.approvedAuthority) &&
        !event.hiddenOverrideApplied && decide (event.blockerCount = 0) &&
        event.planningValidationReceipt
  | .requestDispatch =>
      decide (event.fromStage = .planningValidated) &&
        decide (event.toStage = .dispatchReady) && SlotsMatchState state event &&
        state.planningValidationReceipt &&
        decide (event.requestedAuthority = state.approvedAuthority) &&
        event.approvalReceipt && decide (event.blockerCount = 0) &&
        event.dispatchReceipt
  | .block =>
      decide (event.toStage = .blocked) && event.blockReceipt

def CommandEventValid (state : CommandState) (event : CommandEvent) : Prop :=
  state.stage = event.fromStage ∧
    state.rootIntent = event.rootIntent ∧
    state.commandVersion = event.inputVersion ∧
    state.logicalTime < event.logicalTime ∧
    EventSpecificValid state event = true

instance commandEventValidDecidable (state : CommandState) (event : CommandEvent) :
    Decidable (CommandEventValid state event) := by
  unfold CommandEventValid
  infer_instance

def ApplyCommandEvent (state : CommandState) (event : CommandEvent) : CommandState :=
  { state with
    stage := event.toStage
    commandVersion := event.outputVersion
    objective := if event.kind = .bindFields then event.objective else state.objective
    constraints := if event.kind = .bindFields then event.constraints else state.constraints
    outputContract := if event.kind = .bindFields then event.outputContract else state.outputContract
    verification := if event.kind = .bindFields then event.verification else state.verification
    failureBehavior := if event.kind = .bindFields then event.failureBehavior else state.failureBehavior
    authority := if event.kind = .bindFields then event.authority else state.authority
    approvedAuthority := if event.kind = .bindAuthority then event.requestedAuthority else state.approvedAuthority
    hiddenOverrideSeen := state.hiddenOverrideSeen || event.hiddenOverrideApplied
    planningValidationReceipt := state.planningValidationReceipt || event.planningValidationReceipt
    dispatchReceipt := state.dispatchReceipt || event.dispatchReceipt
    blocked := state.blocked || event.blockReceipt
    logicalTime := event.logicalTime }

def CommandStep (state : CommandState) (event : CommandEvent) : Option CommandState :=
  if CommandEventValid state event then some (ApplyCommandEvent state event) else none

def CommandRun : CommandState → List CommandEvent → Option CommandState
  | state, [] => some state
  | state, event :: tail =>
      match CommandStep state event with
      | none => none
      | some next => CommandRun next tail

theorem accepted_step_is_valid
    {state next : CommandState} {event : CommandEvent}
    (accepted : CommandStep state event = some next) :
    CommandEventValid state event := by
  unfold CommandStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_planning_validation_preserves_all_slots_and_authority
    {state next : CommandState} {event : CommandEvent}
    (kind : event.kind = .validatePlanning)
    (accepted : CommandStep state event = some next) :
    event.objective = state.objective ∧
      event.constraints = state.constraints ∧
      event.outputContract = state.outputContract ∧
      event.verification = state.verification ∧
      event.failureBehavior = state.failureBehavior ∧
      event.authority = state.authority ∧
      event.requestedAuthority = state.approvedAuthority := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, specific⟩
  simp [EventSpecificValid, kind, SlotsMatchState, and_assoc] at specific
  have fields :
      event.fromStage = .authorityBound ∧
        event.toStage = .planningValidated ∧
        event.objective = state.objective ∧
        event.constraints = state.constraints ∧
        event.outputContract = state.outputContract ∧
        event.verification = state.verification ∧
        event.failureBehavior = state.failureBehavior ∧
        event.authority = state.authority ∧
        event.requestedAuthority = state.approvedAuthority ∧
        event.hiddenOverrideApplied = false ∧ event.blockerCount = 0 ∧
        event.planningValidationReceipt = true := by
    simpa [and_assoc] using specific
  exact ⟨fields.2.2.1, fields.2.2.2.1, fields.2.2.2.2.1,
    fields.2.2.2.2.2.1, fields.2.2.2.2.2.2.1,
    fields.2.2.2.2.2.2.2.1, fields.2.2.2.2.2.2.2.2.1⟩

theorem accepted_dispatch_requires_validated_authority_and_receipts
    {state next : CommandState} {event : CommandEvent}
    (kind : event.kind = .requestDispatch)
    (accepted : CommandStep state event = some next) :
    state.planningValidationReceipt = true ∧
      event.requestedAuthority = state.approvedAuthority ∧
      event.approvalReceipt = true ∧ event.dispatchReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, specific⟩
  simp [EventSpecificValid, kind, SlotsMatchState, and_assoc] at specific
  have fields :
      event.fromStage = .planningValidated ∧
        event.toStage = .dispatchReady ∧
        event.objective = state.objective ∧
        event.constraints = state.constraints ∧
        event.outputContract = state.outputContract ∧
        event.verification = state.verification ∧
        event.failureBehavior = state.failureBehavior ∧
        event.authority = state.authority ∧
        state.planningValidationReceipt = true ∧
        event.requestedAuthority = state.approvedAuthority ∧
        event.approvalReceipt = true ∧ event.blockerCount = 0 ∧
        event.dispatchReceipt = true := by
    simpa [and_assoc] using specific
  exact ⟨fields.2.2.2.2.2.2.2.2.1,
    fields.2.2.2.2.2.2.2.2.2.1,
    fields.2.2.2.2.2.2.2.2.2.2.1,
    fields.2.2.2.2.2.2.2.2.2.2.2.2⟩

def emptySlot : SemanticSlot := { valueHash := 0, provenance := .untrustedData, confidence := .missing }
def objectiveSlot : SemanticSlot := { valueHash := 501, provenance := .humanIntent, confidence := .confirmed }
def constraintSlot : SemanticSlot := { valueHash := 502, provenance := .policy, confidence := .policyImposed }
def outputSlot : SemanticSlot := { valueHash := 503, provenance := .humanIntent, confidence := .confirmed }
def verificationSlot : SemanticSlot := { valueHash := 504, provenance := .policy, confidence := .policyImposed }
def failureSlot : SemanticSlot := { valueHash := 505, provenance := .policy, confidence := .policyImposed }
def authoritySlot : SemanticSlot := { valueHash := 506, provenance := .humanIntent, confidence := .confirmed }

def initialState : CommandState where
  stage := .raw
  rootIntent := 101
  commandVersion := 1
  objective := emptySlot
  constraints := emptySlot
  outputContract := emptySlot
  verification := emptySlot
  failureBehavior := emptySlot
  authority := emptySlot
  authorityCeiling := 3
  approvedAuthority := 0
  hiddenOverrideSeen := false
  planningValidationReceipt := false
  dispatchReceipt := false
  blocked := false
  logicalTime := 0

def baseEvent : CommandEvent where
  kind := .bindFields
  fromStage := .raw
  toStage := .fieldsBound
  rootIntent := 101
  inputVersion := 1
  outputVersion := 1
  objective := objectiveSlot
  constraints := constraintSlot
  outputContract := outputSlot
  verification := verificationSlot
  failureBehavior := failureSlot
  authority := authoritySlot
  requestedAuthority := 3
  constraintSourceHash := 502
  hiddenOverrideApplied := false
  blockerCount := 0
  approvalReceipt := false
  planningValidationReceipt := false
  dispatchReceipt := false
  blockReceipt := false
  logicalTime := 1

def successfulCommandTrace : List CommandEvent := [
  baseEvent,
  { baseEvent with
      kind := .checkPrecedence
      fromStage := .fieldsBound
      toStage := .precedenceChecked
      logicalTime := 2 },
  { baseEvent with
      kind := .bindAuthority
      fromStage := .precedenceChecked
      toStage := .authorityBound
      approvalReceipt := true
      logicalTime := 3 },
  { baseEvent with
      kind := .validatePlanning
      fromStage := .authorityBound
      toStage := .planningValidated
      planningValidationReceipt := true
      logicalTime := 4 },
  { baseEvent with
      kind := .requestDispatch
      fromStage := .planningValidated
      toStage := .dispatchReady
      approvalReceipt := true
      dispatchReceipt := true
      logicalTime := 5 }
]

theorem exact_command_trace_reaches_receipted_dispatch :
    CommandRun initialState successfulCommandTrace = some
      { initialState with
        stage := .dispatchReady
        objective := objectiveSlot
        constraints := constraintSlot
        outputContract := outputSlot
        verification := verificationSlot
        failureBehavior := failureSlot
        authority := authoritySlot
        approvedAuthority := 3
        planningValidationReceipt := true
        dispatchReceipt := true
        logicalTime := 5 } := by
  native_decide

def fieldsBoundState : CommandState :=
  { initialState with
    stage := .fieldsBound
    objective := objectiveSlot
    constraints := constraintSlot
    outputContract := outputSlot
    verification := verificationSlot
    failureBehavior := failureSlot
    authority := authoritySlot
    logicalTime := 1 }

def precedenceCheckedState : CommandState :=
  { fieldsBoundState with
    stage := .precedenceChecked
    logicalTime := 2 }

def authorityBoundState : CommandState :=
  { precedenceCheckedState with
    stage := .authorityBound
    approvedAuthority := 3
    logicalTime := 3 }

def planningValidatedState : CommandState :=
  { authorityBoundState with
    stage := .planningValidated
    planningValidationReceipt := true
    logicalTime := 4 }

theorem missing_required_output_is_rejected :
    CommandStep initialState
      { baseEvent with outputContract := { outputSlot with valueHash := 0 } } = none := by
  native_decide

theorem hidden_instruction_provenance_is_rejected :
    CommandStep initialState
      { baseEvent with constraints := { constraintSlot with provenance := .hiddenInstruction } } = none := by
  native_decide

theorem applied_hidden_override_is_rejected :
    CommandStep fieldsBoundState
      { baseEvent with
        kind := .checkPrecedence
        fromStage := .fieldsBound
        toStage := .precedenceChecked
        hiddenOverrideApplied := true
        logicalTime := 2 } = none := by
  native_decide

theorem inferred_authority_is_rejected :
    CommandStep precedenceCheckedState
      { baseEvent with
        kind := .bindAuthority
        fromStage := .precedenceChecked
        toStage := .authorityBound
        authority := { authoritySlot with confidence := .inferred }
        approvalReceipt := true
        logicalTime := 3 } = none := by
  native_decide

theorem authority_widening_is_rejected :
    CommandStep precedenceCheckedState
      { baseEvent with
        kind := .bindAuthority
        fromStage := .precedenceChecked
        toStage := .authorityBound
        requestedAuthority := 4
        approvalReceipt := true
        logicalTime := 3 } = none := by
  native_decide

theorem constraint_substitution_before_planning_is_rejected :
    CommandStep authorityBoundState
      { baseEvent with
        kind := .validatePlanning
        fromStage := .authorityBound
        toStage := .planningValidated
        constraints := { constraintSlot with valueHash := 999 }
        planningValidationReceipt := true
        logicalTime := 4 } = none := by
  native_decide

theorem dispatch_without_validation_receipt_is_rejected :
    CommandStep { planningValidatedState with planningValidationReceipt := false }
      { baseEvent with
        kind := .requestDispatch
        fromStage := .planningValidated
        toStage := .dispatchReady
        approvalReceipt := true
        dispatchReceipt := true
        logicalTime := 5 } = none := by
  native_decide

theorem dispatch_without_receipt_is_rejected :
    CommandStep planningValidatedState
      { baseEvent with
        kind := .requestDispatch
        fromStage := .planningValidated
        toStage := .dispatchReady
        approvalReceipt := true
        logicalTime := 5 } = none := by
  native_decide

end AsiStackProofs.CommandSemanticRefinement

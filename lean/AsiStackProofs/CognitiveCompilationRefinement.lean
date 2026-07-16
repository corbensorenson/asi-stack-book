namespace AsiStackProofs.CognitiveCompilationRefinement

/-!
A finite reachable source-plan-to-target refinement with exact abstract
obligation identities and localized repair custody. Numeric identities,
authority, scope, and receipt fields are trusted inputs; this is not a natural-
language compiler or a proof of target behavior.
-/

inductive CompilationStage where
  | raw | sourceBound | irTyped | lowered | validated | repairRequired
  | accepted | blocked
deriving DecidableEq, Repr

inductive CompilationEventKind where
  | bindSource | typeIR | lowerTarget | validateTarget
  | detectRepair | applyRepair | acceptTarget | block
deriving DecidableEq, Repr

structure CompilationState where
  stage : CompilationStage
  planId : Nat
  planVersion : Nat
  obligationOne : Nat
  obligationTwo : Nat
  obligationThree : Nat
  constraintHash : Nat
  targetHash : Nat
  authorityCeiling : Nat
  approvedAuthority : Nat
  ledgerVersion : Nat
  loweringReceipt : Bool
  validationReceipt : Bool
  repairReceipt : Bool
  residualCount : Nat
  logicalTime : Nat
deriving DecidableEq, Repr

structure CompilationEvent where
  kind : CompilationEventKind
  fromStage : CompilationStage
  toStage : CompilationStage
  planId : Nat
  inputPlanVersion : Nat
  outputPlanVersion : Nat
  obligationOne : Nat
  obligationTwo : Nat
  obligationThree : Nat
  constraintHash : Nat
  targetHash : Nat
  requestedAuthority : Nat
  obligationsPreserved : Bool
  loweringReceipt : Bool
  validationReceipt : Bool
  repairInvalidatesObligation : Bool
  repairLocalized : Bool
  beforeObligationHash : Nat
  afterObligationHash : Nat
  inputLedgerVersion : Nat
  outputLedgerVersion : Nat
  ledgerUpdateReceipt : Bool
  residualCount : Nat
  blockReceipt : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def SourceMatches (state : CompilationState) (event : CompilationEvent) : Bool :=
  decide (event.planId = state.planId) &&
    decide (event.obligationOne = state.obligationOne) &&
    decide (event.obligationTwo = state.obligationTwo) &&
    decide (event.obligationThree = state.obligationThree) &&
    decide (event.constraintHash = state.constraintHash)

def TargetMatches (state : CompilationState) (event : CompilationEvent) : Bool :=
  SourceMatches state event && decide (event.targetHash = state.targetHash)

def CompilationEventSpecificValid
    (state : CompilationState) (event : CompilationEvent) : Bool :=
  match event.kind with
  | .bindSource =>
      decide (event.fromStage = .raw) && decide (event.toStage = .sourceBound) &&
        decide (0 < event.planId) && decide (0 < event.obligationOne) &&
        decide (0 < event.obligationTwo) && decide (0 < event.obligationThree) &&
        decide (0 < event.constraintHash) &&
        decide (event.requestedAuthority ≤ state.authorityCeiling)
  | .typeIR =>
      decide (event.fromStage = .sourceBound) && decide (event.toStage = .irTyped) &&
        SourceMatches state event &&
        decide (event.requestedAuthority = state.approvedAuthority)
  | .lowerTarget =>
      decide (event.fromStage = .irTyped) && decide (event.toStage = .lowered) &&
        SourceMatches state event && decide (0 < event.targetHash) &&
        decide (event.requestedAuthority = state.approvedAuthority) &&
        event.obligationsPreserved && event.loweringReceipt
  | .validateTarget =>
      decide (event.fromStage = .lowered) && decide (event.toStage = .validated) &&
        TargetMatches state event && event.obligationsPreserved &&
        state.loweringReceipt && event.validationReceipt
  | .detectRepair =>
      decide (event.fromStage = .validated) &&
        decide (event.toStage = .repairRequired) && TargetMatches state event &&
        event.repairInvalidatesObligation &&
        decide (event.inputLedgerVersion = state.ledgerVersion)
  | .applyRepair =>
      decide (event.fromStage = .repairRequired) &&
        decide (event.toStage = .validated) && TargetMatches state event &&
        event.repairLocalized &&
        decide (event.beforeObligationHash = event.afterObligationHash) &&
        decide (event.beforeObligationHash = state.obligationThree) &&
        decide (event.inputLedgerVersion = state.ledgerVersion) &&
        decide (event.outputLedgerVersion = state.ledgerVersion + 1) &&
        event.ledgerUpdateReceipt && event.obligationsPreserved
  | .acceptTarget =>
      decide (event.fromStage = .validated) && decide (event.toStage = .accepted) &&
        TargetMatches state event && state.loweringReceipt &&
        state.validationReceipt && event.obligationsPreserved &&
        decide (event.residualCount = 0) &&
        decide (event.requestedAuthority = state.approvedAuthority)
  | .block => decide (event.toStage = .blocked) && event.blockReceipt

def CompilationEventValid
    (state : CompilationState) (event : CompilationEvent) : Prop :=
  state.stage = event.fromStage ∧
    state.planVersion = event.inputPlanVersion ∧
    state.logicalTime < event.logicalTime ∧
    CompilationEventSpecificValid state event = true

instance compilationEventValidDecidable
    (state : CompilationState) (event : CompilationEvent) :
    Decidable (CompilationEventValid state event) := by
  unfold CompilationEventValid
  infer_instance

def ApplyCompilationEvent
    (state : CompilationState) (event : CompilationEvent) : CompilationState :=
  { state with
    stage := event.toStage
    planId := if event.kind = .bindSource then event.planId else state.planId
    planVersion := event.outputPlanVersion
    obligationOne := if event.kind = .bindSource then event.obligationOne else state.obligationOne
    obligationTwo := if event.kind = .bindSource then event.obligationTwo else state.obligationTwo
    obligationThree := if event.kind = .bindSource then event.obligationThree else state.obligationThree
    constraintHash := if event.kind = .bindSource then event.constraintHash else state.constraintHash
    targetHash := if event.kind = .lowerTarget then event.targetHash else state.targetHash
    approvedAuthority := if event.kind = .bindSource then event.requestedAuthority else state.approvedAuthority
    ledgerVersion := if event.kind = .applyRepair then event.outputLedgerVersion else state.ledgerVersion
    loweringReceipt := state.loweringReceipt || event.loweringReceipt
    validationReceipt := state.validationReceipt || event.validationReceipt
    repairReceipt := state.repairReceipt || event.ledgerUpdateReceipt
    residualCount := event.residualCount
    logicalTime := event.logicalTime }

def CompilationStep
    (state : CompilationState) (event : CompilationEvent) : Option CompilationState :=
  if CompilationEventValid state event then some (ApplyCompilationEvent state event) else none

def CompilationRun : CompilationState → List CompilationEvent → Option CompilationState
  | state, [] => some state
  | state, event :: tail =>
      match CompilationStep state event with
      | none => none
      | some next => CompilationRun next tail

theorem accepted_step_is_valid
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    CompilationEventValid state event := by
  unfold CompilationStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_target_preserves_exact_source_and_target
    {state next : CompilationState} {event : CompilationEvent}
    (kind : event.kind = .acceptTarget)
    (accepted : CompilationStep state event = some next) :
    event.planId = state.planId ∧
      event.obligationOne = state.obligationOne ∧
      event.obligationTwo = state.obligationTwo ∧
      event.obligationThree = state.obligationThree ∧
      event.constraintHash = state.constraintHash ∧
      event.targetHash = state.targetHash := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, specific⟩
  simp [CompilationEventSpecificValid, kind, TargetMatches, SourceMatches,
    and_assoc] at specific
  exact ⟨specific.2.2.1, specific.2.2.2.1, specific.2.2.2.2.1,
    specific.2.2.2.2.2.1, specific.2.2.2.2.2.2.1,
    specific.2.2.2.2.2.2.2.1⟩

theorem accepted_repair_requires_local_exact_ledger_update
    {state next : CompilationState} {event : CompilationEvent}
    (kind : event.kind = .applyRepair)
    (accepted : CompilationStep state event = some next) :
    event.repairLocalized = true ∧
      event.beforeObligationHash = event.afterObligationHash ∧
      event.beforeObligationHash = state.obligationThree ∧
      event.outputLedgerVersion = state.ledgerVersion + 1 ∧
      event.ledgerUpdateReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, specific⟩
  simp [CompilationEventSpecificValid, kind, TargetMatches, SourceMatches,
    and_assoc] at specific
  have fields :
      event.fromStage = .repairRequired ∧ event.toStage = .validated ∧
        event.planId = state.planId ∧
        event.obligationOne = state.obligationOne ∧
        event.obligationTwo = state.obligationTwo ∧
        event.obligationThree = state.obligationThree ∧
        event.constraintHash = state.constraintHash ∧
        event.targetHash = state.targetHash ∧ event.repairLocalized = true ∧
        event.beforeObligationHash = event.afterObligationHash ∧
        event.beforeObligationHash = state.obligationThree ∧
        event.inputLedgerVersion = state.ledgerVersion ∧
        event.outputLedgerVersion = state.ledgerVersion + 1 ∧
        event.ledgerUpdateReceipt = true ∧ event.obligationsPreserved = true := by
    simpa [and_assoc] using specific
  rcases fields with ⟨_, _, _, _, _, _, _, _, localized, beforeAfter,
    beforeState, _, outputLedger, receipt, _⟩
  exact ⟨localized, beforeAfter, beforeState, outputLedger, receipt⟩

def initialState : CompilationState where
  stage := .raw
  planId := 0
  planVersion := 1
  obligationOne := 0
  obligationTwo := 0
  obligationThree := 0
  constraintHash := 0
  targetHash := 0
  authorityCeiling := 3
  approvedAuthority := 0
  ledgerVersion := 1
  loweringReceipt := false
  validationReceipt := false
  repairReceipt := false
  residualCount := 0
  logicalTime := 0

def baseEvent
    (kind : CompilationEventKind) (fromStage toStage : CompilationStage)
    (time : Nat) : CompilationEvent where
  kind := kind
  fromStage := fromStage
  toStage := toStage
  planId := 101
  inputPlanVersion := 1
  outputPlanVersion := 1
  obligationOne := 501
  obligationTwo := 502
  obligationThree := 503
  constraintHash := 601
  targetHash := 701
  requestedAuthority := 3
  obligationsPreserved := true
  loweringReceipt := false
  validationReceipt := false
  repairInvalidatesObligation := false
  repairLocalized := false
  beforeObligationHash := 503
  afterObligationHash := 503
  inputLedgerVersion := 1
  outputLedgerVersion := 1
  ledgerUpdateReceipt := false
  residualCount := 0
  blockReceipt := false
  logicalTime := time

def bindEvent : CompilationEvent := baseEvent .bindSource .raw .sourceBound 1
def typeEvent : CompilationEvent := baseEvent .typeIR .sourceBound .irTyped 2
def lowerEvent : CompilationEvent :=
  { baseEvent .lowerTarget .irTyped .lowered 3 with loweringReceipt := true }
def validateEvent : CompilationEvent :=
  { baseEvent .validateTarget .lowered .validated 4 with validationReceipt := true }
def detectRepairEvent : CompilationEvent :=
  { baseEvent .detectRepair .validated .repairRequired 5 with repairInvalidatesObligation := true }
def applyRepairEvent : CompilationEvent :=
  { baseEvent .applyRepair .repairRequired .validated 6 with
    repairLocalized := true, outputLedgerVersion := 2, ledgerUpdateReceipt := true }
def acceptEvent : CompilationEvent :=
  { baseEvent .acceptTarget .validated .accepted 7 with inputLedgerVersion := 2 }

def referenceTrace : List CompilationEvent :=
  [bindEvent, typeEvent, lowerEvent, validateEvent, detectRepairEvent,
    applyRepairEvent, acceptEvent]

theorem localized_repair_trace_reaches_accepted_target :
    (CompilationRun initialState referenceTrace).map (fun state => state.stage) =
      some .accepted := by
  native_decide

def spliceRun (before : List CompilationEvent) (event : CompilationEvent)
    (after : List CompilationEvent) : Option CompilationState :=
  CompilationRun initialState (before ++ event :: after)

theorem dropped_obligation_rejected :
    spliceRun [bindEvent] { typeEvent with obligationTwo := 999 }
      [lowerEvent, validateEvent, detectRepairEvent, applyRepairEvent, acceptEvent] = none := by
  native_decide

theorem widened_authority_rejected :
    CompilationRun initialState [{ bindEvent with requestedAuthority := 4 }] = none := by
  native_decide

theorem missing_lowering_receipt_rejected :
    spliceRun [bindEvent, typeEvent] { lowerEvent with loweringReceipt := false }
      [validateEvent, acceptEvent] = none := by
  native_decide

theorem validator_pass_without_preservation_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent]
      { validateEvent with obligationsPreserved := false } [acceptEvent] = none := by
  native_decide

theorem global_repair_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent, validateEvent, detectRepairEvent]
      { applyRepairEvent with repairLocalized := false }
      [acceptEvent] = none := by
  native_decide

theorem repair_without_ledger_increment_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent, validateEvent, detectRepairEvent]
      { applyRepairEvent with outputLedgerVersion := 1 }
      [acceptEvent] = none := by
  native_decide

theorem target_substitution_at_accept_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent, validateEvent]
      { acceptEvent with targetHash := 999 } [] = none := by
  native_decide

theorem residual_target_acceptance_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent, validateEvent]
      { acceptEvent with residualCount := 1 } [] = none := by
  native_decide

end AsiStackProofs.CognitiveCompilationRefinement

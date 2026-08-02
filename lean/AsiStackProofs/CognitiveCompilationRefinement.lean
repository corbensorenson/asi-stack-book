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
  validatedPlanVersion : Nat
  loweringReceipt : Bool
  validationReceipt : Bool
  repairReceipt : Bool
  residualCount : Nat
  supportAuthority : Bool
  externalEffectAuthority : Bool
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
  supportPromotionRequested : Bool
  externalEffectRequested : Bool
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
        decide (event.requestedAuthority ≤ state.authorityCeiling) &&
        decide (event.outputPlanVersion = event.inputPlanVersion) &&
        decide (event.residualCount = 0)
  | .typeIR =>
      decide (event.fromStage = .sourceBound) && decide (event.toStage = .irTyped) &&
        SourceMatches state event &&
        decide (event.requestedAuthority = state.approvedAuthority) &&
        decide (event.outputPlanVersion = event.inputPlanVersion) &&
        decide (event.residualCount = state.residualCount)
  | .lowerTarget =>
      decide (event.fromStage = .irTyped) && decide (event.toStage = .lowered) &&
        SourceMatches state event && decide (0 < event.targetHash) &&
        decide (event.requestedAuthority = state.approvedAuthority) &&
        event.obligationsPreserved && event.loweringReceipt &&
        decide (event.outputPlanVersion = event.inputPlanVersion) &&
        decide (event.residualCount = state.residualCount)
  | .validateTarget =>
      decide (event.fromStage = .lowered) && decide (event.toStage = .validated) &&
        TargetMatches state event && event.obligationsPreserved &&
        state.loweringReceipt && event.validationReceipt &&
        decide (event.outputPlanVersion = event.inputPlanVersion) &&
        decide (event.residualCount = state.residualCount)
  | .detectRepair =>
      decide (event.fromStage = .validated) &&
        decide (event.toStage = .repairRequired) && TargetMatches state event &&
        event.repairInvalidatesObligation &&
        decide (event.inputLedgerVersion = state.ledgerVersion) &&
        decide (event.outputPlanVersion = event.inputPlanVersion) &&
        decide (0 < event.residualCount)
  | .applyRepair =>
      decide (event.fromStage = .repairRequired) &&
        decide (event.toStage = .lowered) && TargetMatches state event &&
        event.repairLocalized &&
        decide (event.beforeObligationHash = event.afterObligationHash) &&
        decide (event.beforeObligationHash = state.obligationThree) &&
        decide (event.inputLedgerVersion = state.ledgerVersion) &&
        decide (event.outputLedgerVersion = state.ledgerVersion + 1) &&
        decide (event.outputPlanVersion = state.planVersion + 1) &&
        event.ledgerUpdateReceipt && event.obligationsPreserved &&
        decide (event.residualCount = 0)
  | .acceptTarget =>
      decide (event.fromStage = .validated) && decide (event.toStage = .accepted) &&
        TargetMatches state event && state.loweringReceipt &&
        state.validationReceipt && event.obligationsPreserved &&
        decide (state.validatedPlanVersion = state.planVersion) &&
        decide (event.outputPlanVersion = event.inputPlanVersion) &&
        decide (event.residualCount = 0) &&
        decide (event.requestedAuthority = state.approvedAuthority)
  | .block => decide (event.toStage = .blocked) && event.blockReceipt &&
      decide (event.outputPlanVersion = event.inputPlanVersion) &&
      decide (event.residualCount = state.residualCount)

def CompilationEventValid
    (state : CompilationState) (event : CompilationEvent) : Prop :=
  state.stage = event.fromStage ∧
    state.planVersion = event.inputPlanVersion ∧
    state.logicalTime < event.logicalTime ∧
    event.supportPromotionRequested = false ∧
    event.externalEffectRequested = false ∧
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
    validatedPlanVersion := if event.kind = .validateTarget then event.outputPlanVersion else state.validatedPlanVersion
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

def SourceIdentity (state : CompilationState) : Nat × Nat × Nat × Nat × Nat × Nat :=
  (state.planId, state.obligationOne, state.obligationTwo,
    state.obligationThree, state.constraintHash, state.authorityCeiling)

def CompilationTraceValid : CompilationState -> List CompilationEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      CompilationEventValid state event ∧
        CompilationTraceValid (ApplyCompilationEvent state event) tail

def CompleteCompilationCustody (state : CompilationState) : Prop :=
  state.loweringReceipt = true ∧ state.validationReceipt = true ∧
    state.repairReceipt = true

theorem accepted_step_is_valid
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    CompilationEventValid state event := by
  unfold CompilationStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_step_applies_event
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    next = ApplyCompilationEvent state event := by
  unfold CompilationStep at accepted
  split at accepted
  · exact Option.some.inj accepted |>.symm
  · simp at accepted

theorem accepted_step_cannot_request_support
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    event.supportPromotionRequested = false := by
  exact (accepted_step_is_valid accepted).2.2.2.1

theorem accepted_step_cannot_request_external_effect
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    event.externalEffectRequested = false := by
  exact (accepted_step_is_valid accepted).2.2.2.2.1

theorem apply_nonbinding_event_preserves_source_identity
    (state : CompilationState) (event : CompilationEvent)
    (notBind : event.kind ≠ .bindSource) :
    SourceIdentity (ApplyCompilationEvent state event) = SourceIdentity state := by
  cases kind : event.kind <;>
    simp_all [ApplyCompilationEvent, SourceIdentity]

theorem accepted_bound_step_is_not_source_binding
    {state next : CompilationState} {event : CompilationEvent}
    (bound : state.stage ≠ .raw)
    (accepted : CompilationStep state event = some next) :
    event.kind ≠ .bindSource := by
  intro bind
  rcases accepted_step_is_valid accepted with ⟨stage, _, _, _, _, specific⟩
  simp [CompilationEventSpecificValid, bind, and_assoc] at specific
  exact bound (stage.trans specific.1)

theorem accepted_bound_step_preserves_source_identity
    {state next : CompilationState} {event : CompilationEvent}
    (bound : state.stage ≠ .raw)
    (accepted : CompilationStep state event = some next) :
    SourceIdentity next = SourceIdentity state := by
  rw [accepted_step_applies_event accepted]
  exact apply_nonbinding_event_preserves_source_identity state event
    (accepted_bound_step_is_not_source_binding bound accepted)

theorem accepted_step_leaves_raw_stage
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    next.stage ≠ .raw := by
  have valid := accepted_step_is_valid accepted
  have applies := accepted_step_applies_event accepted
  subst next
  rcases valid with ⟨_, _, _, _, _, specific⟩
  cases kind : event.kind <;>
    simp_all [CompilationEventSpecificValid, ApplyCompilationEvent]

theorem successful_bound_run_preserves_source_identity
    {state final : CompilationState} {events : List CompilationEvent}
    (bound : state.stage ≠ .raw)
    (ran : CompilationRun state events = some final) :
    SourceIdentity final = SourceIdentity state := by
  induction events generalizing state with
  | nil =>
      simp [CompilationRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : CompilationStep state event with
      | none => simp [CompilationRun, stepped] at ran
      | some next =>
          have tailRan : CompilationRun next tail = some final := by
            simpa [CompilationRun, stepped] using ran
          calc
            SourceIdentity final = SourceIdentity next :=
              ih (accepted_step_leaves_raw_stage stepped) tailRan
            _ = SourceIdentity state :=
              accepted_bound_step_preserves_source_identity bound stepped

theorem accepted_step_preserves_support_authority
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    next.supportAuthority = state.supportAuthority := by
  rw [accepted_step_applies_event accepted]
  rfl

theorem accepted_step_preserves_external_effect_authority
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    next.externalEffectAuthority = state.externalEffectAuthority := by
  rw [accepted_step_applies_event accepted]
  rfl

theorem successful_run_preserves_support_authority
    {state final : CompilationState} {events : List CompilationEvent}
    (ran : CompilationRun state events = some final) :
    final.supportAuthority = state.supportAuthority := by
  induction events generalizing state with
  | nil =>
      simp [CompilationRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : CompilationStep state event with
      | none => simp [CompilationRun, stepped] at ran
      | some next =>
          have tailRan : CompilationRun next tail = some final := by
            simpa [CompilationRun, stepped] using ran
          calc
            final.supportAuthority = next.supportAuthority := ih tailRan
            _ = state.supportAuthority := accepted_step_preserves_support_authority stepped

theorem successful_run_preserves_external_effect_authority
    {state final : CompilationState} {events : List CompilationEvent}
    (ran : CompilationRun state events = some final) :
    final.externalEffectAuthority = state.externalEffectAuthority := by
  induction events generalizing state with
  | nil =>
      simp [CompilationRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : CompilationStep state event with
      | none => simp [CompilationRun, stepped] at ran
      | some next =>
          have tailRan : CompilationRun next tail = some final := by
            simpa [CompilationRun, stepped] using ran
          calc
            final.externalEffectAuthority = next.externalEffectAuthority := ih tailRan
            _ = state.externalEffectAuthority :=
              accepted_step_preserves_external_effect_authority stepped

theorem successful_run_has_valid_trace
    {state final : CompilationState} {events : List CompilationEvent}
    (ran : CompilationRun state events = some final) :
    CompilationTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : CompilationStep state event with
      | none => simp [CompilationRun, stepped] at ran
      | some next =>
          have tailRan : CompilationRun next tail = some final := by
            simpa [CompilationRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          exact ⟨accepted_step_is_valid stepped, by
            simpa [applies] using ih tailRan⟩

theorem compilation_runs_compose
    (state : CompilationState) (left right : List CompilationEvent) :
    CompilationRun state (left ++ right) =
      match CompilationRun state left with
      | none => none
      | some middle => CompilationRun middle right := by
  induction left generalizing state with
  | nil => simp [CompilationRun]
  | cons event tail ih =>
      cases stepped : CompilationStep state event <;>
        simp [CompilationRun, stepped, ih]

theorem apply_event_preserves_complete_compilation_custody
    (state : CompilationState) (event : CompilationEvent)
    (custody : CompleteCompilationCustody state) :
    CompleteCompilationCustody (ApplyCompilationEvent state event) := by
  rcases custody with ⟨lowering, validation, repair⟩
  simp [CompleteCompilationCustody, ApplyCompilationEvent, lowering,
    validation, repair]

theorem successful_run_preserves_complete_compilation_custody
    {state final : CompilationState} {events : List CompilationEvent}
    (custody : CompleteCompilationCustody state)
    (ran : CompilationRun state events = some final) :
    CompleteCompilationCustody final := by
  induction events generalizing state with
  | nil =>
      simp [CompilationRun] at ran
      subst final
      exact custody
  | cons event tail ih =>
      cases stepped : CompilationStep state event with
      | none => simp [CompilationRun, stepped] at ran
      | some next =>
          have tailRan : CompilationRun next tail = some final := by
            simpa [CompilationRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          subst next
          exact ih (apply_event_preserves_complete_compilation_custody state event custody)
            tailRan

theorem accepted_step_plan_version_monotone
    {state next : CompilationState} {event : CompilationEvent}
    (accepted : CompilationStep state event = some next) :
    state.planVersion ≤ next.planVersion := by
  have valid := accepted_step_is_valid accepted
  have applies := accepted_step_applies_event accepted
  subst next
  rcases valid with ⟨version, _, _, _, _, specific⟩
  cases kind : event.kind <;>
    simp_all [CompilationEventSpecificValid, ApplyCompilationEvent]

theorem successful_run_plan_version_monotone
    {state final : CompilationState} {events : List CompilationEvent}
    (ran : CompilationRun state events = some final) :
    state.planVersion ≤ final.planVersion := by
  induction events generalizing state with
  | nil =>
      simp [CompilationRun] at ran
      subst final
      exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : CompilationStep state event with
      | none => simp [CompilationRun, stepped] at ran
      | some next =>
          have tailRan : CompilationRun next tail = some final := by
            simpa [CompilationRun, stepped] using ran
          exact Nat.le_trans (accepted_step_plan_version_monotone stepped) (ih tailRan)

theorem accepted_repair_increments_plan_and_ledger_versions
    {state next : CompilationState} {event : CompilationEvent}
    (kind : event.kind = .applyRepair)
    (accepted : CompilationStep state event = some next) :
    next.planVersion = state.planVersion + 1 ∧
      next.ledgerVersion = state.ledgerVersion + 1 := by
  have valid := accepted_step_is_valid accepted
  rw [accepted_step_applies_event accepted]
  rcases valid with ⟨_, _, _, _, _, specific⟩
  simp_all [CompilationEventSpecificValid, ApplyCompilationEvent]

theorem accepted_target_requires_current_plan_validation
    {state next : CompilationState} {event : CompilationEvent}
    (kind : event.kind = .acceptTarget)
    (accepted : CompilationStep state event = some next) :
    state.validatedPlanVersion = state.planVersion := by
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, _, specific⟩
  simp_all [CompilationEventSpecificValid]

theorem accepted_target_closes_residuals
    {state next : CompilationState} {event : CompilationEvent}
    (kind : event.kind = .acceptTarget)
    (accepted : CompilationStep state event = some next) :
    next.residualCount = 0 := by
  have valid := accepted_step_is_valid accepted
  rw [accepted_step_applies_event accepted]
  rcases valid with ⟨_, _, _, _, _, specific⟩
  simp_all [CompilationEventSpecificValid, ApplyCompilationEvent]

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
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, _, specific⟩
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
  rcases accepted_step_is_valid accepted with ⟨_, _, _, _, _, specific⟩
  simp [CompilationEventSpecificValid, kind, TargetMatches, SourceMatches,
    and_assoc] at specific
  have fields :
      event.fromStage = .repairRequired ∧ event.toStage = .lowered ∧
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
        event.outputPlanVersion = state.planVersion + 1 ∧
        event.ledgerUpdateReceipt = true ∧ event.obligationsPreserved = true ∧
        event.residualCount = 0 := by
    simpa [and_assoc] using specific
  rcases fields with ⟨_, _, _, _, _, _, _, _, localized, beforeAfter,
    beforeState, _, outputLedger, _, receipt, _, _⟩
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
  validatedPlanVersion := 0
  loweringReceipt := false
  validationReceipt := false
  repairReceipt := false
  residualCount := 0
  supportAuthority := false
  externalEffectAuthority := false
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
  supportPromotionRequested := false
  externalEffectRequested := false
  blockReceipt := false
  logicalTime := time

def bindEvent : CompilationEvent := baseEvent .bindSource .raw .sourceBound 1
def typeEvent : CompilationEvent := baseEvent .typeIR .sourceBound .irTyped 2
def lowerEvent : CompilationEvent :=
  { baseEvent .lowerTarget .irTyped .lowered 3 with loweringReceipt := true }
def validateEvent : CompilationEvent :=
  { baseEvent .validateTarget .lowered .validated 4 with validationReceipt := true }
def detectRepairEvent : CompilationEvent :=
  { baseEvent .detectRepair .validated .repairRequired 5 with
    repairInvalidatesObligation := true, residualCount := 1 }
def applyRepairEvent : CompilationEvent :=
  { baseEvent .applyRepair .repairRequired .lowered 6 with
    outputPlanVersion := 2, repairLocalized := true, outputLedgerVersion := 2,
    ledgerUpdateReceipt := true }
def revalidateEvent : CompilationEvent :=
  { baseEvent .validateTarget .lowered .validated 7 with
    inputPlanVersion := 2, outputPlanVersion := 2, inputLedgerVersion := 2,
    validationReceipt := true }
def acceptEvent : CompilationEvent :=
  { baseEvent .acceptTarget .validated .accepted 8 with
    inputPlanVersion := 2, outputPlanVersion := 2, inputLedgerVersion := 2 }
def acceptWithoutRepairEvent : CompilationEvent :=
  baseEvent .acceptTarget .validated .accepted 5

def referenceTrace : List CompilationEvent :=
  [bindEvent, typeEvent, lowerEvent, validateEvent, detectRepairEvent,
    applyRepairEvent, revalidateEvent, acceptEvent]

theorem localized_repair_trace_reaches_accepted_target :
    (CompilationRun initialState referenceTrace).map (fun state => state.stage) =
      some .accepted := by
  native_decide

def spliceRun (before : List CompilationEvent) (event : CompilationEvent)
    (after : List CompilationEvent) : Option CompilationState :=
  CompilationRun initialState (before ++ event :: after)

theorem dropped_obligation_rejected :
    spliceRun [bindEvent] { typeEvent with obligationTwo := 999 }
      [lowerEvent, validateEvent, detectRepairEvent, applyRepairEvent,
        revalidateEvent, acceptEvent] = none := by
  native_decide

theorem widened_authority_rejected :
    CompilationRun initialState [{ bindEvent with requestedAuthority := 4 }] = none := by
  native_decide

theorem missing_lowering_receipt_rejected :
    spliceRun [bindEvent, typeEvent] { lowerEvent with loweringReceipt := false }
      [validateEvent, acceptWithoutRepairEvent] = none := by
  native_decide

theorem validator_pass_without_preservation_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent]
      { validateEvent with obligationsPreserved := false }
      [acceptWithoutRepairEvent] = none := by
  native_decide

theorem global_repair_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent, validateEvent, detectRepairEvent]
      { applyRepairEvent with repairLocalized := false }
      [revalidateEvent, acceptEvent] = none := by
  native_decide

theorem repair_without_ledger_increment_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent, validateEvent, detectRepairEvent]
      { applyRepairEvent with outputLedgerVersion := 1 }
      [revalidateEvent, acceptEvent] = none := by
  native_decide

theorem target_substitution_at_accept_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent, validateEvent]
      { acceptWithoutRepairEvent with targetHash := 999 } [] = none := by
  native_decide

theorem residual_target_acceptance_rejected :
    spliceRun [bindEvent, typeEvent, lowerEvent, validateEvent]
      { acceptWithoutRepairEvent with residualCount := 1 } [] = none := by
  native_decide

end AsiStackProofs.CognitiveCompilationRefinement

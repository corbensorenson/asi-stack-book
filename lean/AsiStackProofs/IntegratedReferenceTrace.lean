namespace AsiStackProofs.IntegratedReferenceTrace

/-!
A bounded cross-layer join model for the integrated reference architecture.
Every accepted handoff joins parent artifact, canonical state, authority,
effect, acknowledgement, evidence, residual, rollback, and terminal custody.
-/

inductive Layer where
  | request
  | intent
  | context
  | plan
  | route
  | authorize
  | job
  | adapter
  | effect
  | observe
  | evaluate
  | evidence
  | terminal
  | quarantine
deriving DecidableEq, Repr

inductive EventKind where
  | advance
  | commitEffect
  | acknowledge
  | evaluate
  | evidence
  | rollback
  | terminal
  | quarantine
deriving DecidableEq, Repr

structure TraceState where
  currentLayer : Layer
  authorityCeiling : Nat
  activeAuthority : Nat
  canonicalState : Nat
  lastArtifact : Nat
  materialEffects : Nat
  acknowledgedEffects : Nat
  openResiduals : Nat
  supportLevel : Nat
  observationComplete : Bool
  evaluationComplete : Bool
  terminalReceipt : Bool
  rolledBack : Bool
  logicalTime : Nat
  revokedAt : Option Nat
deriving DecidableEq, Repr

structure TraceEvent where
  kind : EventKind
  fromLayer : Layer
  toLayer : Layer
  logicalTime : Nat
  parentArtifact : Nat
  producedArtifact : Nat
  stateBefore : Nat
  stateAfter : Nat
  requestedAuthority : Nat
  effectDelta : Nat
  acknowledgementDelta : Nat
  rollbackDelta : Nat
  residualCreated : Nat
  residualDischarged : Nat
  supportBefore : Nat
  supportAfter : Nat
  gateRequired : Bool
  gatePresent : Bool
  independentObservation : Bool
  independentEvaluator : Bool
  evidenceTransitionPresent : Bool
  acceptedReview : Bool
  residualOwnerPresent : Bool
  rollbackReady : Bool
  rollbackExact : Bool
  receiptPresent : Bool
  nonClaimPresent : Bool
deriving DecidableEq, Repr

def AdvancePair (fromLayer toLayer : Layer) : Bool :=
  match fromLayer, toLayer with
  | .request, .intent => true
  | .intent, .context => true
  | .context, .plan => true
  | .plan, .route => true
  | .route, .authorize => true
  | .authorize, .job => true
  | .job, .adapter => true
  | _, _ => false

def AuthorityValid (state : TraceState) (event : TraceEvent) : Bool :=
  decide (event.requestedAuthority ≤ state.activeAuthority) &&
    decide (state.activeAuthority ≤ state.authorityCeiling)

def ParentStateJoinValid (state : TraceState) (event : TraceEvent) : Bool :=
  decide (event.fromLayer = state.currentLayer) &&
    decide (event.parentArtifact = state.lastArtifact) &&
    decide (event.stateBefore = state.canonicalState)

def CustodyValid (state : TraceState) (event : TraceEvent) : Bool :=
  decide (event.producedArtifact != 0) &&
    decide (state.logicalTime ≤ event.logicalTime) &&
    decide (event.residualDischarged ≤ state.openResiduals + event.residualCreated) &&
    decide (event.supportBefore = state.supportLevel) &&
    event.residualOwnerPresent &&
    event.nonClaimPresent &&
    (!event.gateRequired || event.gatePresent)

def CommonValid (state : TraceState) (event : TraceEvent) : Bool :=
  AuthorityValid state event &&
    ParentStateJoinValid state event &&
    CustodyValid state event

def AdvanceValid (event : TraceEvent) : Bool :=
  AdvancePair event.fromLayer event.toLayer &&
    decide (event.effectDelta = 0) &&
    decide (event.acknowledgementDelta = 0) &&
    decide (event.rollbackDelta = 0) &&
    decide (event.supportAfter = event.supportBefore)

def EffectValid (state : TraceState) (event : TraceEvent) : Bool :=
  decide (event.fromLayer = Layer.adapter) &&
    decide (event.toLayer = Layer.effect) &&
    decide (0 < event.effectDelta) &&
    decide (event.acknowledgementDelta = 0) &&
    decide (event.rollbackDelta = 0) &&
    event.rollbackReady &&
    decide (event.supportAfter = event.supportBefore) &&
    match state.revokedAt with
    | none => true
    | some revokedAt => decide (event.logicalTime < revokedAt)

def AcknowledgeValid (state : TraceState) (event : TraceEvent) : Bool :=
  decide (event.fromLayer = Layer.effect) &&
    decide (event.toLayer = Layer.observe) &&
    decide (event.effectDelta = 0) &&
    decide (0 < event.acknowledgementDelta) &&
    decide (state.acknowledgedEffects + event.acknowledgementDelta ≤ state.materialEffects) &&
    decide (event.rollbackDelta = 0) &&
    event.independentObservation &&
    decide (event.supportAfter = event.supportBefore)

def EvaluationValid (event : TraceEvent) : Bool :=
  decide (event.fromLayer = Layer.observe) &&
    decide (event.toLayer = Layer.evaluate) &&
    decide (event.effectDelta = 0) &&
    decide (event.acknowledgementDelta = 0) &&
    decide (event.rollbackDelta = 0) &&
    event.independentEvaluator &&
    decide (event.supportAfter = event.supportBefore)

def EvidenceValid (state : TraceState) (event : TraceEvent) : Bool :=
  decide (event.fromLayer = Layer.evaluate) &&
    decide (event.toLayer = Layer.evidence) &&
    state.evaluationComplete &&
    decide (event.effectDelta = 0) &&
    decide (event.acknowledgementDelta = 0) &&
    decide (event.rollbackDelta = 0) &&
    (if decide (event.supportAfter = event.supportBefore) then true
      else event.evidenceTransitionPresent && event.acceptedReview)

def RollbackValid (state : TraceState) (event : TraceEvent) : Bool :=
  decide (event.toLayer = Layer.terminal) &&
    decide (event.effectDelta = 0) &&
    decide (event.acknowledgementDelta = 0) &&
    decide (event.rollbackDelta = state.materialEffects) &&
    event.rollbackReady &&
    event.rollbackExact &&
    event.receiptPresent &&
    decide (event.supportAfter = event.supportBefore)

def TerminalValid (state : TraceState) (event : TraceEvent) : Bool :=
  decide (event.fromLayer = Layer.evidence) &&
    decide (event.toLayer = Layer.terminal) &&
    state.observationComplete &&
    state.evaluationComplete &&
    decide (state.materialEffects = state.acknowledgedEffects) &&
    decide (event.effectDelta = 0) &&
    decide (event.acknowledgementDelta = 0) &&
    decide (event.rollbackDelta = 0) &&
    event.receiptPresent &&
    decide (event.supportAfter = event.supportBefore)

def QuarantineValid (event : TraceEvent) : Bool :=
  decide (event.toLayer = Layer.quarantine) &&
    decide (event.effectDelta = 0) &&
    decide (event.acknowledgementDelta = 0) &&
    decide (event.rollbackDelta = 0) &&
    event.receiptPresent &&
    decide (event.supportAfter = event.supportBefore)

def KindValid (state : TraceState) (event : TraceEvent) : Bool :=
  match event.kind with
  | .advance => AdvanceValid event
  | .commitEffect => EffectValid state event
  | .acknowledge => AcknowledgeValid state event
  | .evaluate => EvaluationValid event
  | .evidence => EvidenceValid state event
  | .rollback => RollbackValid state event
  | .terminal => TerminalValid state event
  | .quarantine => QuarantineValid event

def EventValid (state : TraceState) (event : TraceEvent) : Bool :=
  CommonValid state event && KindValid state event

def ApplyEvent (state : TraceState) (event : TraceEvent) : TraceState :=
  { state with
    currentLayer := event.toLayer
    activeAuthority := event.requestedAuthority
    canonicalState := event.stateAfter
    lastArtifact := event.producedArtifact
    materialEffects :=
      if event.kind = EventKind.rollback then 0
      else state.materialEffects + event.effectDelta
    acknowledgedEffects :=
      if event.kind = EventKind.rollback then 0
      else state.acknowledgedEffects + event.acknowledgementDelta
    openResiduals := state.openResiduals + event.residualCreated - event.residualDischarged
    supportLevel := event.supportAfter
    observationComplete := state.observationComplete || event.kind = EventKind.acknowledge
    evaluationComplete := state.evaluationComplete || event.kind = EventKind.evaluate
    terminalReceipt := state.terminalReceipt || event.receiptPresent
    rolledBack := state.rolledBack || event.kind = EventKind.rollback
    logicalTime := event.logicalTime }

def LayerClosed : Layer -> Bool
  | .terminal | .quarantine => true
  | _ => false

def Step (state : TraceState) (event : TraceEvent) : Option TraceState :=
  if LayerClosed state.currentLayer then none
  else if EventValid state event then some (ApplyEvent state event) else none

def Run : TraceState → List TraceEvent → Option TraceState
  | state, [] => some state
  | state, event :: tail =>
      match Step state event with
      | none => none
      | some next => Run next tail

def TraceAccepted : TraceState -> List TraceEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      EventValid state event = true ∧
      TraceAccepted (ApplyEvent state event) tail

def ResidualCreatedTotal : List TraceEvent -> Nat
  | [] => 0
  | event :: tail => event.residualCreated + ResidualCreatedTotal tail

def ResidualDischargedTotal : List TraceEvent -> Nat
  | [] => 0
  | event :: tail => event.residualDischarged + ResidualDischargedTotal tail

def EffectAccountingValid (state : TraceState) : Prop :=
  state.acknowledgedEffects <= state.materialEffects

theorem common_valid_authority_bound
    {state : TraceState} {event : TraceEvent}
    (valid : CommonValid state event = true) :
    event.requestedAuthority ≤ state.activeAuthority := by
  simp [CommonValid] at valid
  have authority : AuthorityValid state event = true := valid.1.1
  simp [AuthorityValid] at authority
  exact authority.1

theorem common_valid_parent_join
    {state : TraceState} {event : TraceEvent}
    (valid : CommonValid state event = true) :
    event.parentArtifact = state.lastArtifact := by
  simp [CommonValid] at valid
  have join : ParentStateJoinValid state event = true := valid.1.2
  simp [ParentStateJoinValid] at join
  exact join.1.2

theorem common_valid_state_join
    {state : TraceState} {event : TraceEvent}
    (valid : CommonValid state event = true) :
    event.stateBefore = state.canonicalState := by
  simp [CommonValid] at valid
  have join : ParentStateJoinValid state event = true := valid.1.2
  simp [ParentStateJoinValid] at join
  exact join.2

theorem accepted_step_is_valid
    {state next : TraceState} {event : TraceEvent}
    (accepted : Step state event = some next) :
    EventValid state event = true := by
  unfold Step at accepted
  split at accepted
  · simp at accepted
  · split at accepted
    · assumption
    · simp at accepted

theorem accepted_step_applies_event
    {state next : TraceState} {event : TraceEvent}
    (accepted : Step state event = some next) :
    next = ApplyEvent state event := by
  unfold Step at accepted
  split at accepted
  · simp at accepted
  · split at accepted
    · exact Option.some.inj accepted |>.symm
    · simp at accepted

theorem accepted_step_authority_nonincreasing
    {state next : TraceState} {event : TraceEvent}
    (accepted : Step state event = some next) :
    next.activeAuthority ≤ state.activeAuthority := by
  have parts : CommonValid state event = true ∧ KindValid state event = true := by
    simpa [EventValid] using accepted_step_is_valid accepted
  rw [accepted_step_applies_event accepted]
  exact common_valid_authority_bound parts.1

theorem accepted_step_preserves_ceiling
    {state next : TraceState} {event : TraceEvent}
    (accepted : Step state event = some next) :
    next.authorityCeiling = state.authorityCeiling := by
  rw [accepted_step_applies_event accepted]
  rfl

theorem accepted_step_joins_parent_and_state
    {state next : TraceState} {event : TraceEvent}
    (accepted : Step state event = some next) :
    event.parentArtifact = state.lastArtifact ∧
      event.stateBefore = state.canonicalState ∧
      next.lastArtifact = event.producedArtifact ∧
      next.canonicalState = event.stateAfter := by
  have parts : CommonValid state event = true ∧ KindValid state event = true := by
    simpa [EventValid] using accepted_step_is_valid accepted
  rw [accepted_step_applies_event accepted]
  exact ⟨common_valid_parent_join parts.1, common_valid_state_join parts.1, rfl, rfl⟩

theorem accepted_step_logical_time_monotone
    {state next : TraceState} {event : TraceEvent}
    (accepted : Step state event = some next) :
    state.logicalTime <= next.logicalTime := by
  have valid := accepted_step_is_valid accepted
  simp [EventValid, CommonValid, CustodyValid] at valid
  rw [accepted_step_applies_event accepted]
  simp [ApplyEvent]
  omega

theorem accepted_step_preserves_residual_accounting
    {state next : TraceState} {event : TraceEvent}
    (accepted : Step state event = some next) :
    next.openResiduals + event.residualDischarged =
      state.openResiduals + event.residualCreated := by
  have valid := accepted_step_is_valid accepted
  simp [EventValid, CommonValid, CustodyValid] at valid
  rw [accepted_step_applies_event accepted]
  simp [ApplyEvent]
  omega

theorem accepted_step_preserves_effect_accounting
    {state next : TraceState} {event : TraceEvent}
    (accounted : EffectAccountingValid state)
    (accepted : Step state event = some next) :
    EffectAccountingValid next := by
  have parts : CommonValid state event = true ∧ KindValid state event = true := by
    simpa [EventValid] using accepted_step_is_valid accepted
  have kindValid := parts.2
  rw [accepted_step_applies_event accepted]
  cases selectedKind : event.kind <;>
    simp [KindValid, selectedKind, AdvanceValid, EffectValid, AcknowledgeValid,
      EvaluationValid, EvidenceValid, RollbackValid, TerminalValid,
      QuarantineValid] at kindValid <;>
    simp [EffectAccountingValid, ApplyEvent, selectedKind] at accounted ⊢ <;>
    omega

theorem closed_layer_accepts_no_event
    (state : TraceState) (event : TraceEvent)
    (closed : LayerClosed state.currentLayer = true) :
    Step state event = none := by
  simp [Step, closed]

theorem accepted_trace_authority_nonincreasing
    {initial final : TraceState} {events : List TraceEvent}
    (accepted : Run initial events = some final) :
    final.activeAuthority ≤ initial.activeAuthority := by
  induction events generalizing initial with
  | nil =>
      simp [Run] at accepted
      simp_all
  | cons event tail inductionHypothesis =>
      unfold Run at accepted
      split at accepted
      case h_1 => contradiction
      case h_2 next stepAccepted =>
        exact Nat.le_trans (inductionHypothesis accepted)
          (accepted_step_authority_nonincreasing stepAccepted)

theorem accepted_trace_preserves_ceiling
    {initial final : TraceState} {events : List TraceEvent}
    (accepted : Run initial events = some final) :
    final.authorityCeiling = initial.authorityCeiling := by
  induction events generalizing initial with
  | nil => simp [Run] at accepted; subst final; rfl
  | cons event tail ih =>
      cases stepped : Step initial event with
      | none => simp [Run, stepped] at accepted
      | some next =>
          have tailRun : Run next tail = some final := by
            simpa [Run, stepped] using accepted
          exact (ih tailRun).trans (accepted_step_preserves_ceiling stepped)

theorem accepted_trace_logical_time_monotone
    {initial final : TraceState} {events : List TraceEvent}
    (accepted : Run initial events = some final) :
    initial.logicalTime <= final.logicalTime := by
  induction events generalizing initial with
  | nil => simp [Run] at accepted; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : Step initial event with
      | none => simp [Run, stepped] at accepted
      | some next =>
          have tailRun : Run next tail = some final := by
            simpa [Run, stepped] using accepted
          exact Nat.le_trans (accepted_step_logical_time_monotone stepped)
            (ih tailRun)

theorem accepted_trace_preserves_effect_accounting
    {initial final : TraceState} {events : List TraceEvent}
    (accounted : EffectAccountingValid initial)
    (accepted : Run initial events = some final) :
    EffectAccountingValid final := by
  induction events generalizing initial with
  | nil => simp [Run] at accepted; subst final; exact accounted
  | cons event tail ih =>
      cases stepped : Step initial event with
      | none => simp [Run, stepped] at accepted
      | some next =>
          have tailRun : Run next tail = some final := by
            simpa [Run, stepped] using accepted
          exact ih (accepted_step_preserves_effect_accounting accounted stepped)
            tailRun

theorem accepted_trace_preserves_residual_accounting
    {initial final : TraceState} {events : List TraceEvent}
    (accepted : Run initial events = some final) :
    final.openResiduals + ResidualDischargedTotal events =
      initial.openResiduals + ResidualCreatedTotal events := by
  induction events generalizing initial with
  | nil => simp [Run] at accepted; subst final; simp [ResidualDischargedTotal,
      ResidualCreatedTotal]
  | cons event tail ih =>
      cases stepped : Step initial event with
      | none => simp [Run, stepped] at accepted
      | some next =>
          have tailRun : Run next tail = some final := by
            simpa [Run, stepped] using accepted
          have stepAccounting := accepted_step_preserves_residual_accounting stepped
          have tailAccounting := ih tailRun
          simp only [ResidualDischargedTotal, ResidualCreatedTotal]
          omega

theorem accepted_run_has_valid_trace
    {initial final : TraceState} {events : List TraceEvent}
    (accepted : Run initial events = some final) :
    TraceAccepted initial events := by
  induction events generalizing initial with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : Step initial event with
      | none => simp [Run, stepped] at accepted
      | some next =>
          have tailRun : Run next tail = some final := by
            simpa [Run, stepped] using accepted
          exact ⟨accepted_step_is_valid stepped, by
            rw [← accepted_step_applies_event stepped]
            exact ih tailRun⟩

theorem run_append
    (state : TraceState) (first second : List TraceEvent) :
    Run state (first ++ second) =
      match Run state first with
      | none => none
      | some middle => Run middle second := by
  induction first generalizing state with
  | nil => rfl
  | cons event tail inductionHypothesis =>
      simp only [List.cons_append, Run]
      split
      · rfl
      · rename_i next stepAccepted
        exact inductionHypothesis next

def initialState : TraceState where
  currentLayer := .request
  authorityCeiling := 3
  activeAuthority := 3
  canonicalState := 1000
  lastArtifact := 100
  materialEffects := 0
  acknowledgedEffects := 0
  openResiduals := 0
  supportLevel := 1
  observationComplete := false
  evaluationComplete := false
  terminalReceipt := false
  rolledBack := false
  logicalTime := 0
  revokedAt := none

def baseEvent : TraceEvent where
  kind := .advance
  fromLayer := .request
  toLayer := .intent
  logicalTime := 1
  parentArtifact := 100
  producedArtifact := 101
  stateBefore := 1000
  stateAfter := 1001
  requestedAuthority := 3
  effectDelta := 0
  acknowledgementDelta := 0
  rollbackDelta := 0
  residualCreated := 0
  residualDischarged := 0
  supportBefore := 1
  supportAfter := 1
  gateRequired := false
  gatePresent := false
  independentObservation := false
  independentEvaluator := false
  evidenceTransitionPresent := false
  acceptedReview := false
  residualOwnerPresent := true
  rollbackReady := true
  rollbackExact := false
  receiptPresent := false
  nonClaimPresent := true

def completeTrace : List TraceEvent :=
  [ baseEvent,
    { baseEvent with
        fromLayer := .intent
        toLayer := .context
        logicalTime := 2
        parentArtifact := 101
        producedArtifact := 102
        stateBefore := 1001
        stateAfter := 1002 },
    { baseEvent with
        fromLayer := .context
        toLayer := .plan
        logicalTime := 3
        parentArtifact := 102
        producedArtifact := 103
        stateBefore := 1002
        stateAfter := 1003
        residualCreated := 1 },
    { baseEvent with
        fromLayer := .plan
        toLayer := .route
        logicalTime := 4
        parentArtifact := 103
        producedArtifact := 104
        stateBefore := 1003
        stateAfter := 1004
        requestedAuthority := 2 },
    { baseEvent with
        fromLayer := .route
        toLayer := .authorize
        logicalTime := 5
        parentArtifact := 104
        producedArtifact := 105
        stateBefore := 1004
        stateAfter := 1005
        requestedAuthority := 2
        gateRequired := true
        gatePresent := true },
    { baseEvent with
        fromLayer := .authorize
        toLayer := .job
        logicalTime := 6
        parentArtifact := 105
        producedArtifact := 106
        stateBefore := 1005
        stateAfter := 1006
        requestedAuthority := 1 },
    { baseEvent with
        fromLayer := .job
        toLayer := .adapter
        logicalTime := 7
        parentArtifact := 106
        producedArtifact := 107
        stateBefore := 1006
        stateAfter := 1007
        requestedAuthority := 1 },
    { baseEvent with
        kind := .commitEffect
        fromLayer := .adapter
        toLayer := .effect
        logicalTime := 8
        parentArtifact := 107
        producedArtifact := 108
        stateBefore := 1007
        stateAfter := 1008
        requestedAuthority := 1
        effectDelta := 1
        gateRequired := true
        gatePresent := true },
    { baseEvent with
        kind := .acknowledge
        fromLayer := .effect
        toLayer := .observe
        logicalTime := 9
        parentArtifact := 108
        producedArtifact := 109
        stateBefore := 1008
        stateAfter := 1009
        requestedAuthority := 1
        acknowledgementDelta := 1
        independentObservation := true },
    { baseEvent with
        kind := .evaluate
        fromLayer := .observe
        toLayer := .evaluate
        logicalTime := 10
        parentArtifact := 109
        producedArtifact := 110
        stateBefore := 1009
        stateAfter := 1010
        requestedAuthority := 1
        independentEvaluator := true },
    { baseEvent with
        kind := .evidence
        fromLayer := .evaluate
        toLayer := .evidence
        logicalTime := 11
        parentArtifact := 110
        producedArtifact := 111
        stateBefore := 1010
        stateAfter := 1011
        requestedAuthority := 1
        residualDischarged := 1 },
    { baseEvent with
        kind := .terminal
        fromLayer := .evidence
        toLayer := .terminal
        logicalTime := 12
        parentArtifact := 111
        producedArtifact := 112
        stateBefore := 1011
        stateAfter := 1012
        requestedAuthority := 1
        receiptPresent := true } ]

def completeFinal : TraceState where
  currentLayer := .terminal
  authorityCeiling := 3
  activeAuthority := 1
  canonicalState := 1012
  lastArtifact := 112
  materialEffects := 1
  acknowledgedEffects := 1
  openResiduals := 0
  supportLevel := 1
  observationComplete := true
  evaluationComplete := true
  terminalReceipt := true
  rolledBack := false
  logicalTime := 12
  revokedAt := none

theorem complete_cross_layer_trace_is_accepted :
    Run initialState completeTrace = some completeFinal := by
  decide

theorem parent_fork_is_rejected :
    Step initialState { baseEvent with parentArtifact := 999 } = none := by
  decide

theorem authority_widening_is_rejected :
    Step initialState { baseEvent with requestedAuthority := 4 } = none := by
  decide

theorem missing_gate_is_rejected :
    Step { initialState with
      currentLayer := .route
      lastArtifact := 104
      canonicalState := 1004
      activeAuthority := 2
      logicalTime := 4 }
      { baseEvent with
        fromLayer := .route
        toLayer := .authorize
        logicalTime := 5
        parentArtifact := 104
        producedArtifact := 105
        stateBefore := 1004
        stateAfter := 1005
        requestedAuthority := 2
        gateRequired := true
        gatePresent := false } = none := by
  decide

theorem effect_at_revocation_tie_is_rejected :
    Step { initialState with
      currentLayer := .adapter
      lastArtifact := 107
      canonicalState := 1007
      activeAuthority := 1
      logicalTime := 7
      revokedAt := some 8 }
      { baseEvent with
        kind := .commitEffect
        fromLayer := .adapter
        toLayer := .effect
        logicalTime := 8
        parentArtifact := 107
        producedArtifact := 108
        stateBefore := 1007
        stateAfter := 1008
        requestedAuthority := 1
        effectDelta := 1
        gateRequired := true
        gatePresent := true } = none := by
  decide

theorem terminal_with_unacknowledged_effect_is_rejected :
    Step { completeFinal with
      currentLayer := .evidence
      acknowledgedEffects := 0
      terminalReceipt := false
      logicalTime := 11
      lastArtifact := 111
      canonicalState := 1011 }
      { baseEvent with
        kind := .terminal
        fromLayer := .evidence
        toLayer := .terminal
        logicalTime := 12
        parentArtifact := 111
        producedArtifact := 112
        stateBefore := 1011
        stateAfter := 1012
        requestedAuthority := 1
        receiptPresent := true } = none := by
  decide

theorem residual_erasure_is_rejected :
    Step initialState { baseEvent with residualDischarged := 1 } = none := by
  decide

/-! ## Logical-time concurrency and effect closure

This second transition system gives independently identified effects a shared
revocation epoch and mutually exclusive terminal custody. Equal logical times
model linearizable races with revocation taking precedence over attempts. It
does not claim distributed-clock or network-partition semantics.
-/

inductive ConcurrentEffectKind where
  | attempt
  | observe
  | acknowledge
  | compensate
  | residualize
  | revoke
deriving DecidableEq, Repr

structure ConcurrentEffectState where
  authorityEpoch : Nat
  revokedAt : Option Nat
  attempted : List Nat
  observed : List Nat
  acknowledged : List Nat
  compensated : List Nat
  residualized : List Nat
  logicalTime : Nat
deriving DecidableEq, Repr

structure ConcurrentEffectEvent where
  kind : ConcurrentEffectKind
  effectId : Nat
  authorityEpoch : Nat
  logicalTime : Nat
  receiptPresent : Bool
deriving DecidableEq, Repr

def FreshFor (effectId : Nat) (items : List Nat) : Bool :=
  decide (effectId ∉ items)

def TerminalFresh (state : ConcurrentEffectState) (effectId : Nat) : Bool :=
  FreshFor effectId state.acknowledged &&
    FreshFor effectId state.compensated &&
    FreshFor effectId state.residualized

def BeforeRevocation (state : ConcurrentEffectState) (event : ConcurrentEffectEvent) : Bool :=
  match state.revokedAt with
  | none => true
  | some revokedAt => decide (event.logicalTime < revokedAt)

def ConcurrentEffectEventValid
    (state : ConcurrentEffectState) (event : ConcurrentEffectEvent) : Bool :=
  decide (state.logicalTime ≤ event.logicalTime) &&
  match event.kind with
  | .attempt =>
      decide (event.effectId != 0) &&
        decide (event.authorityEpoch = state.authorityEpoch) &&
        BeforeRevocation state event
  | .observe =>
      decide (event.effectId ∈ state.attempted) &&
        FreshFor event.effectId state.observed
  | .acknowledge =>
      decide (event.effectId ∈ state.observed) &&
        TerminalFresh state event.effectId && event.receiptPresent
  | .compensate =>
      decide (event.effectId ∈ state.observed) &&
        TerminalFresh state event.effectId && event.receiptPresent
  | .residualize =>
      decide (event.effectId ∈ state.observed) &&
        TerminalFresh state event.effectId && event.receiptPresent
  | .revoke => decide (event.authorityEpoch = state.authorityEpoch)

def ApplyConcurrentEffectEvent
    (state : ConcurrentEffectState) (event : ConcurrentEffectEvent) : ConcurrentEffectState :=
  match event.kind with
  | .attempt =>
      { state with
        attempted := if event.effectId ∈ state.attempted then state.attempted else event.effectId :: state.attempted
        logicalTime := event.logicalTime }
  | .observe => { state with observed := event.effectId :: state.observed, logicalTime := event.logicalTime }
  | .acknowledge => { state with acknowledged := event.effectId :: state.acknowledged, logicalTime := event.logicalTime }
  | .compensate => { state with compensated := event.effectId :: state.compensated, logicalTime := event.logicalTime }
  | .residualize => { state with residualized := event.effectId :: state.residualized, logicalTime := event.logicalTime }
  | .revoke => { state with authorityEpoch := state.authorityEpoch + 1, revokedAt := some event.logicalTime, logicalTime := event.logicalTime }

def ConcurrentEffectStep
    (state : ConcurrentEffectState) (event : ConcurrentEffectEvent) : Option ConcurrentEffectState :=
  if ConcurrentEffectEventValid state event
  then some (ApplyConcurrentEffectEvent state event)
  else none

def ConcurrentEffectRun :
    ConcurrentEffectState → List ConcurrentEffectEvent → Option ConcurrentEffectState
  | state, [] => some state
  | state, event :: tail =>
      match ConcurrentEffectStep state event with
      | none => none
      | some next => ConcurrentEffectRun next tail

def ConcurrentEffectTraceAccepted :
    ConcurrentEffectState -> List ConcurrentEffectEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      ConcurrentEffectEventValid state event = true ∧
      ConcurrentEffectTraceAccepted (ApplyConcurrentEffectEvent state event) tail

def EffectClosed (state : ConcurrentEffectState) (effectId : Nat) : Prop :=
  effectId ∈ state.acknowledged ∨
    effectId ∈ state.compensated ∨
    effectId ∈ state.residualized

theorem accepted_concurrent_attempt_precedes_revocation
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (kind : event.kind = ConcurrentEffectKind.attempt)
    (revoked : state.revokedAt = some event.logicalTime)
    (accepted : ConcurrentEffectStep state event = some next) : False := by
  simp [ConcurrentEffectStep, ConcurrentEffectEventValid, kind, BeforeRevocation, revoked] at accepted

theorem accepted_concurrent_step_is_valid
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (accepted : ConcurrentEffectStep state event = some next) :
    ConcurrentEffectEventValid state event = true := by
  unfold ConcurrentEffectStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_concurrent_step_applies_event
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (accepted : ConcurrentEffectStep state event = some next) :
    next = ApplyConcurrentEffectEvent state event := by
  unfold ConcurrentEffectStep at accepted
  split at accepted
  · exact Option.some.inj accepted |>.symm
  · simp at accepted

theorem accepted_concurrent_step_logical_time_monotone
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (accepted : ConcurrentEffectStep state event = some next) :
    state.logicalTime <= next.logicalTime := by
  have valid := accepted_concurrent_step_is_valid accepted
  have timeValid : state.logicalTime <= event.logicalTime := by
    change (decide (state.logicalTime <= event.logicalTime) && _) = true at valid
    exact of_decide_eq_true (Bool.and_eq_true_iff.mp valid).1
  rw [accepted_concurrent_step_applies_event accepted]
  cases kindEq : event.kind <;>
    simpa [ApplyConcurrentEffectEvent, kindEq] using timeValid

theorem accepted_concurrent_step_authority_epoch_monotone
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (accepted : ConcurrentEffectStep state event = some next) :
    state.authorityEpoch <= next.authorityEpoch := by
  rw [accepted_concurrent_step_applies_event accepted]
  cases kindEq : event.kind <;> simp [ApplyConcurrentEffectEvent, kindEq]

theorem accepted_observation_has_attempt
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (kind : event.kind = ConcurrentEffectKind.observe)
    (accepted : ConcurrentEffectStep state event = some next) :
    event.effectId ∈ state.attempted := by
  unfold ConcurrentEffectStep at accepted
  split at accepted
  · rename_i valid
    simp [ConcurrentEffectEventValid, kind] at valid
    exact valid.2.1
  · simp at accepted

theorem accepted_attempt_records_idempotency_key
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (kind : event.kind = ConcurrentEffectKind.attempt)
    (accepted : ConcurrentEffectStep state event = some next) :
    event.effectId ∈ next.attempted := by
  unfold ConcurrentEffectStep at accepted
  split at accepted
  · cases accepted
    by_cases present : event.effectId ∈ state.attempted <;>
      simp [ApplyConcurrentEffectEvent, kind, present]
  · simp at accepted

theorem accepted_acknowledgement_closes_effect
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (kind : event.kind = ConcurrentEffectKind.acknowledge)
    (accepted : ConcurrentEffectStep state event = some next) :
    EffectClosed next event.effectId := by
  unfold ConcurrentEffectStep at accepted
  split at accepted
  · cases accepted
    simp [ApplyConcurrentEffectEvent, kind, EffectClosed]
  · simp at accepted

theorem accepted_compensation_closes_effect
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (kind : event.kind = ConcurrentEffectKind.compensate)
    (accepted : ConcurrentEffectStep state event = some next) :
    EffectClosed next event.effectId := by
  unfold ConcurrentEffectStep at accepted
  split at accepted
  · cases accepted
    simp [ApplyConcurrentEffectEvent, kind, EffectClosed]
  · simp at accepted

theorem accepted_residualization_closes_effect
    {state next : ConcurrentEffectState} {event : ConcurrentEffectEvent}
    (kind : event.kind = ConcurrentEffectKind.residualize)
    (accepted : ConcurrentEffectStep state event = some next) :
    EffectClosed next event.effectId := by
  unfold ConcurrentEffectStep at accepted
  split at accepted
  · cases accepted
    simp [ApplyConcurrentEffectEvent, kind, EffectClosed]
  · simp at accepted

theorem accepted_concurrent_run_logical_time_monotone
    {initial final : ConcurrentEffectState} {events : List ConcurrentEffectEvent}
    (accepted : ConcurrentEffectRun initial events = some final) :
    initial.logicalTime <= final.logicalTime := by
  induction events generalizing initial with
  | nil => simp [ConcurrentEffectRun] at accepted; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : ConcurrentEffectStep initial event with
      | none => simp [ConcurrentEffectRun, stepped] at accepted
      | some next =>
          have tailRun : ConcurrentEffectRun next tail = some final := by
            simpa [ConcurrentEffectRun, stepped] using accepted
          exact Nat.le_trans (accepted_concurrent_step_logical_time_monotone stepped)
            (ih tailRun)

theorem accepted_concurrent_run_authority_epoch_monotone
    {initial final : ConcurrentEffectState} {events : List ConcurrentEffectEvent}
    (accepted : ConcurrentEffectRun initial events = some final) :
    initial.authorityEpoch <= final.authorityEpoch := by
  induction events generalizing initial with
  | nil => simp [ConcurrentEffectRun] at accepted; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : ConcurrentEffectStep initial event with
      | none => simp [ConcurrentEffectRun, stepped] at accepted
      | some next =>
          have tailRun : ConcurrentEffectRun next tail = some final := by
            simpa [ConcurrentEffectRun, stepped] using accepted
          exact Nat.le_trans
            (accepted_concurrent_step_authority_epoch_monotone stepped)
            (ih tailRun)

theorem accepted_concurrent_run_has_valid_trace
    {initial final : ConcurrentEffectState} {events : List ConcurrentEffectEvent}
    (accepted : ConcurrentEffectRun initial events = some final) :
    ConcurrentEffectTraceAccepted initial events := by
  induction events generalizing initial with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : ConcurrentEffectStep initial event with
      | none => simp [ConcurrentEffectRun, stepped] at accepted
      | some next =>
          have tailRun : ConcurrentEffectRun next tail = some final := by
            simpa [ConcurrentEffectRun, stepped] using accepted
          exact ⟨accepted_concurrent_step_is_valid stepped, by
            rw [← accepted_concurrent_step_applies_event stepped]
            exact ih tailRun⟩

theorem concurrent_effect_run_append
    (state : ConcurrentEffectState)
    (first second : List ConcurrentEffectEvent) :
    ConcurrentEffectRun state (first ++ second) =
      (ConcurrentEffectRun state first).bind fun middle =>
        ConcurrentEffectRun middle second := by
  induction first generalizing state with
  | nil => simp [ConcurrentEffectRun]
  | cons event tail ih =>
      simp only [List.cons_append, ConcurrentEffectRun]
      cases ConcurrentEffectStep state event <;> simp [ih]

def concurrentInitial : ConcurrentEffectState where
  authorityEpoch := 7
  revokedAt := none
  attempted := []
  observed := []
  acknowledged := []
  compensated := []
  residualized := []
  logicalTime := 0

def oneEffectAcknowledgement : List ConcurrentEffectEvent := [
  ⟨.attempt, 1, 7, 1, false⟩,
  ⟨.observe, 1, 7, 2, false⟩,
  ⟨.acknowledge, 1, 7, 3, true⟩ ]

def oneEffectFinal : ConcurrentEffectState where
  authorityEpoch := 7
  revokedAt := none
  attempted := [1]
  observed := [1]
  acknowledged := [1]
  compensated := []
  residualized := []
  logicalTime := 3

def AuthoredEffectProjection
    (layerState : TraceState) (effectState : ConcurrentEffectState) : Prop :=
  layerState.materialEffects = effectState.attempted.length ∧
    layerState.acknowledgedEffects = effectState.acknowledged.length ∧
    layerState.openResiduals = effectState.residualized.length

theorem authored_one_effect_projection_witness :
    Run initialState completeTrace = some completeFinal ∧
    ConcurrentEffectRun concurrentInitial oneEffectAcknowledgement = some oneEffectFinal ∧
    AuthoredEffectProjection completeFinal oneEffectFinal := by
  exact ⟨complete_cross_layer_trace_is_accepted, by decide,
    by simp [AuthoredEffectProjection, completeFinal, oneEffectFinal]⟩

def twoEffectInterleaving : List ConcurrentEffectEvent := [
  ⟨.attempt, 1, 7, 1, false⟩,
  ⟨.attempt, 2, 7, 1, false⟩,
  ⟨.observe, 2, 7, 2, false⟩,
  ⟨.observe, 1, 7, 2, false⟩,
  ⟨.acknowledge, 1, 7, 3, true⟩,
  ⟨.residualize, 2, 7, 3, true⟩ ]

def twoEffectFinal : ConcurrentEffectState where
  authorityEpoch := 7
  revokedAt := none
  attempted := [2, 1]
  observed := [1, 2]
  acknowledged := [1]
  compensated := []
  residualized := [2]
  logicalTime := 3

theorem two_effect_interleaving_is_closed :
    ConcurrentEffectRun concurrentInitial twoEffectInterleaving = some twoEffectFinal := by
  decide

theorem same_time_revocation_blocks_attempt :
    ConcurrentEffectRun concurrentInitial [
      ⟨.revoke, 0, 7, 5, true⟩,
      ⟨.attempt, 1, 7, 5, false⟩ ] = none := by
  decide

theorem exact_attempt_retry_is_idempotent :
    ConcurrentEffectRun concurrentInitial [
      ⟨.attempt, 1, 7, 1, false⟩,
      ⟨.attempt, 1, 7, 2, false⟩ ] =
      some { concurrentInitial with attempted := [1], logicalTime := 2 } := by
  decide

theorem one_effect_acknowledged_and_other_residualized :
    EffectClosed twoEffectFinal 1 ∧ EffectClosed twoEffectFinal 2 := by
  simp [EffectClosed, twoEffectFinal]

end AsiStackProofs.IntegratedReferenceTrace

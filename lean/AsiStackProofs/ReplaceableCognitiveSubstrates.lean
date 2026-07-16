namespace AsiStackProofs.ReplaceableCognitiveSubstrates

/-!
A finite Cognitive Kernel ABI model. Kernel identifiers and families are data;
the control plane, not the kernel, owns effect commitment, authority ceilings,
checkpoint identity, migration, revocation, and evidence custody.
-/

inductive KernelFamily where
  | transformer
  | selectiveStateSpace
  | recurrent
  | kan
  | programSynthesizer
deriving DecidableEq, Repr

inductive ABIEventKind where
  | propose
  | commit
  | migrate
  | revoke
deriving DecidableEq, Repr

structure ABIState where
  activeKernel : Nat
  activeFamily : KernelFamily
  authorityCeiling : Nat
  checkpointSchema : Nat
  checkpointDigest : Nat
  pendingKernel : Option Nat
  committedEffects : Nat
  revokedKernel : Option Nat
deriving DecidableEq, Repr

structure ABIEvent where
  kind : ABIEventKind
  actorKernel : Nat
  targetKernel : Nat
  targetFamily : KernelFamily
  fallbackKernel : Nat
  fallbackFamily : KernelFamily
  requestedAuthority : Nat
  checkpointSchema : Nat
  checkpointDigest : Nat
  proposalOnly : Bool
  effectObserved : Bool
  migrationCompatible : Bool
  fallbackReady : Bool
  evaluatorIndependent : Bool
  assistanceDeclared : Bool
  lifecycleCostDeclared : Bool
  evidenceTransitionPresent : Bool
  residualOwnerPresent : Bool
  effectReceiptPresent : Bool
  rollbackReady : Bool
deriving DecidableEq, Repr

def CommonCustodyComplete (event : ABIEvent) : Bool :=
  event.fallbackReady &&
    event.evaluatorIndependent &&
    event.assistanceDeclared &&
    event.lifecycleCostDeclared &&
    event.residualOwnerPresent &&
    event.rollbackReady

def ExactCheckpoint (state : ABIState) (event : ABIEvent) : Bool :=
  decide (event.checkpointSchema = state.checkpointSchema) &&
    decide (event.checkpointDigest = state.checkpointDigest)

def ActorAdmitted (state : ABIState) (event : ABIEvent) : Bool :=
  decide (event.actorKernel = state.activeKernel) &&
    decide (state.revokedKernel != some event.actorKernel) &&
    decide (event.requestedAuthority ≤ state.authorityCeiling)

def ProposalValid (state : ABIState) (event : ABIEvent) : Bool :=
  ActorAdmitted state event &&
    decide (state.revokedKernel != some event.targetKernel) &&
    ExactCheckpoint state event &&
    CommonCustodyComplete event &&
    event.proposalOnly &&
    !event.effectObserved &&
    !event.effectReceiptPresent

def CommitValid (state : ABIState) (event : ABIEvent) : Bool :=
  ActorAdmitted state event &&
    decide (state.pendingKernel = some event.actorKernel) &&
    decide (event.targetKernel = event.actorKernel) &&
    ExactCheckpoint state event &&
    CommonCustodyComplete event &&
    !event.proposalOnly &&
    event.effectObserved &&
    event.effectReceiptPresent &&
    event.evidenceTransitionPresent

def MigrationValid (state : ABIState) (event : ABIEvent) : Bool :=
  ActorAdmitted state event &&
    decide (state.pendingKernel = some event.targetKernel) &&
    decide (state.revokedKernel != some event.targetKernel) &&
    ExactCheckpoint state event &&
    CommonCustodyComplete event &&
    event.proposalOnly &&
    !event.effectObserved &&
    !event.effectReceiptPresent &&
    event.migrationCompatible &&
    decide (event.targetKernel != event.actorKernel)

def RevocationValid (state : ABIState) (event : ABIEvent) : Bool :=
  ActorAdmitted state event &&
    decide (event.targetKernel = event.fallbackKernel) &&
    decide (event.fallbackKernel != event.actorKernel) &&
    decide (state.revokedKernel != some event.fallbackKernel) &&
    ExactCheckpoint state event &&
    CommonCustodyComplete event &&
    event.proposalOnly &&
    !event.effectObserved &&
    !event.effectReceiptPresent

def EventValid (state : ABIState) (event : ABIEvent) : Bool :=
  match event.kind with
  | .propose => ProposalValid state event
  | .commit => CommitValid state event
  | .migrate => MigrationValid state event
  | .revoke => RevocationValid state event

def ApplyEvent (state : ABIState) (event : ABIEvent) : ABIState :=
  match event.kind with
  | .propose => { state with pendingKernel := some event.targetKernel }
  | .commit =>
      { state with
        pendingKernel := none
        committedEffects := state.committedEffects + 1 }
  | .migrate =>
      { state with
        activeKernel := event.targetKernel
        activeFamily := event.targetFamily
        pendingKernel := none }
  | .revoke =>
      { state with
        activeKernel := event.fallbackKernel
        activeFamily := event.fallbackFamily
        pendingKernel := none
        revokedKernel := some event.actorKernel }

def Step (state : ABIState) (event : ABIEvent) : Option ABIState :=
  if EventValid state event then
    some (ApplyEvent state event)
  else
    none

def Run : ABIState → List ABIEvent → Option ABIState
  | state, [] => some state
  | state, event :: tail =>
      match Step state event with
      | none => none
      | some next => Run next tail

theorem apply_event_preserves_authority (state : ABIState) (event : ABIEvent) :
    (ApplyEvent state event).authorityCeiling = state.authorityCeiling := by
  unfold ApplyEvent
  cases event.kind <;> rfl

theorem apply_event_preserves_checkpoint_schema (state : ABIState) (event : ABIEvent) :
    (ApplyEvent state event).checkpointSchema = state.checkpointSchema := by
  unfold ApplyEvent
  cases event.kind <;> rfl

theorem apply_event_preserves_checkpoint_digest (state : ABIState) (event : ABIEvent) :
    (ApplyEvent state event).checkpointDigest = state.checkpointDigest := by
  unfold ApplyEvent
  cases event.kind <;> rfl

theorem accepted_step_preserves_authority
    {state next : ABIState} {event : ABIEvent}
    (accepted : Step state event = some next) :
    next.authorityCeiling = state.authorityCeiling := by
  unfold Step at accepted
  split at accepted
  · cases accepted
    exact apply_event_preserves_authority state event
  · simp at accepted

theorem accepted_step_preserves_checkpoint_schema
    {state next : ABIState} {event : ABIEvent}
    (accepted : Step state event = some next) :
    next.checkpointSchema = state.checkpointSchema := by
  unfold Step at accepted
  split at accepted
  · cases accepted
    exact apply_event_preserves_checkpoint_schema state event
  · simp at accepted

theorem accepted_step_preserves_checkpoint_digest
    {state next : ABIState} {event : ABIEvent}
    (accepted : Step state event = some next) :
    next.checkpointDigest = state.checkpointDigest := by
  unfold Step at accepted
  split at accepted
  · cases accepted
    exact apply_event_preserves_checkpoint_digest state event
  · simp at accepted

theorem accepted_proposal_does_not_commit_effect
    {state next : ABIState} {event : ABIEvent}
    (proposal : event.kind = ABIEventKind.propose)
    (accepted : Step state event = some next) :
    next.committedEffects = state.committedEffects := by
  unfold Step at accepted
  split at accepted
  · cases accepted
    unfold ApplyEvent
    rw [proposal]
  · simp at accepted

theorem revoked_kernel_cannot_propose
    (state : ABIState) (event : ABIEvent)
    (proposal : event.kind = ABIEventKind.propose)
    (revoked : state.revokedKernel = some event.actorKernel) :
    Step state event = none := by
  unfold Step
  have invalid : EventValid state event = false := by
    simp [EventValid, proposal, ProposalValid, ActorAdmitted, revoked]
  simp [invalid]

theorem incompatible_migration_is_rejected
    (state : ABIState) (event : ABIEvent)
    (migration : event.kind = ABIEventKind.migrate)
    (incompatible : event.migrationCompatible = false) :
    Step state event = none := by
  unfold Step
  have invalid : EventValid state event = false := by
    simp [EventValid, migration, MigrationValid, incompatible]
  simp [invalid]

theorem run_preserves_authority
    {initial final : ABIState} {events : List ABIEvent}
    (accepted : Run initial events = some final) :
    final.authorityCeiling = initial.authorityCeiling := by
  induction events generalizing initial with
  | nil => simp [Run] at accepted; simp_all
  | cons event tail inductionHypothesis =>
      simp [Run] at accepted
      split at accepted
      case h_1 => contradiction
      case h_2 next stepAccepted =>
        calc
          final.authorityCeiling = next.authorityCeiling :=
            inductionHypothesis accepted
          _ = initial.authorityCeiling := accepted_step_preserves_authority stepAccepted

theorem run_preserves_exact_checkpoint
    {initial final : ABIState} {events : List ABIEvent}
    (accepted : Run initial events = some final) :
    final.checkpointSchema = initial.checkpointSchema ∧
      final.checkpointDigest = initial.checkpointDigest := by
  induction events generalizing initial with
  | nil => simp [Run] at accepted; simp_all
  | cons event tail inductionHypothesis =>
      simp [Run] at accepted
      split at accepted
      case h_1 => contradiction
      case h_2 next stepAccepted =>
        have tailInvariant := inductionHypothesis accepted
        exact ⟨tailInvariant.1.trans (accepted_step_preserves_checkpoint_schema stepAccepted),
          tailInvariant.2.trans (accepted_step_preserves_checkpoint_digest stepAccepted)⟩

def initialState : ABIState where
  activeKernel := 1
  activeFamily := .transformer
  authorityCeiling := 2
  checkpointSchema := 7
  checkpointDigest := 7001
  pendingKernel := none
  committedEffects := 0
  revokedKernel := none

def baseEvent : ABIEvent where
  kind := .propose
  actorKernel := 1
  targetKernel := 2
  targetFamily := .selectiveStateSpace
  fallbackKernel := 1
  fallbackFamily := .transformer
  requestedAuthority := 1
  checkpointSchema := 7
  checkpointDigest := 7001
  proposalOnly := true
  effectObserved := false
  migrationCompatible := true
  fallbackReady := true
  evaluatorIndependent := true
  assistanceDeclared := true
  lifecycleCostDeclared := true
  evidenceTransitionPresent := false
  residualOwnerPresent := true
  effectReceiptPresent := false
  rollbackReady := true

def mixedKernelTrace : List ABIEvent :=
  [ baseEvent,
    { baseEvent with kind := .migrate },
    { baseEvent with actorKernel := 2 },
    { baseEvent with
        kind := .commit
        actorKernel := 2
        targetKernel := 2
        proposalOnly := false
        effectObserved := true
        evidenceTransitionPresent := true
        effectReceiptPresent := true },
    { baseEvent with
        actorKernel := 2
        targetKernel := 3
        targetFamily := .kan
        fallbackKernel := 2
        fallbackFamily := .selectiveStateSpace },
    { baseEvent with
        kind := .migrate
        actorKernel := 2
        targetKernel := 3
        targetFamily := .kan
        fallbackKernel := 2
        fallbackFamily := .selectiveStateSpace },
    { baseEvent with
        kind := .revoke
        actorKernel := 3
        targetKernel := 2
        targetFamily := .selectiveStateSpace
        fallbackKernel := 2
        fallbackFamily := .selectiveStateSpace },
    { baseEvent with
        actorKernel := 2
        targetKernel := 2
        targetFamily := .selectiveStateSpace
        fallbackKernel := 1
        fallbackFamily := .transformer },
    { baseEvent with
        kind := .commit
        actorKernel := 2
        targetKernel := 2
        targetFamily := .selectiveStateSpace
        proposalOnly := false
        effectObserved := true
        evidenceTransitionPresent := true
        effectReceiptPresent := true } ]

def mixedKernelFinal : ABIState where
  activeKernel := 2
  activeFamily := .selectiveStateSpace
  authorityCeiling := 2
  checkpointSchema := 7
  checkpointDigest := 7001
  pendingKernel := none
  committedEffects := 2
  revokedKernel := some 3

theorem mixed_kernel_trace_is_accepted :
    Run initialState mixedKernelTrace = some mixedKernelFinal := by
  decide

theorem proposal_with_observed_effect_is_rejected :
    Step initialState { baseEvent with effectObserved := true } = none := by
  decide

theorem authority_widening_is_rejected :
    Step initialState { baseEvent with requestedAuthority := 3 } = none := by
  decide

theorem omitted_cost_is_rejected :
    Step initialState { baseEvent with lifecycleCostDeclared := false } = none := by
  decide

theorem incompatible_fixture_migration_is_rejected :
    Step { initialState with pendingKernel := some 2 }
      { baseEvent with kind := .migrate, migrationCompatible := false } = none := by
  decide

end AsiStackProofs.ReplaceableCognitiveSubstrates

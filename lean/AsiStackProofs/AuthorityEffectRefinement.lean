namespace AsiStackProofs.AuthorityEffectRefinement

/-!
A reachable authority model for exact grant binding, time/epoch freshness,
approval, dispatch, one-shot use, independent effect observation, revocation,
and rollback. Natural-language interpretation, identity proof, deployed
enforcement, and security are deliberately outside this finite model.
-/

structure Grant where
  grantId : Nat
  principalId : Nat
  operationId : Nat
  targetId : Nat
  authority : Nat
  epoch : Nat
  expiresAt : Nat
  remainingUses : Nat
deriving DecidableEq, Repr

inductive AuthorityEventKind where
  | issue | approve | dispatch | commitEffect | observe | revoke | rollback
deriving DecidableEq, Repr

structure AuthorityState where
  callerCeiling : Nat
  authorityEpoch : Nat
  logicalTime : Nat
  activeGrant : Option Grant
  approvedGrantId : Option Nat
  dispatchedGrantId : Option Nat
  revokedGrantIds : List Nat
  materialEffects : Nat
  observedEffects : Nat
  rolledBack : Bool
deriving DecidableEq, Repr

structure AuthorityEvent where
  kind : AuthorityEventKind
  grantId : Nat
  principalId : Nat
  operationId : Nat
  targetId : Nat
  authority : Nat
  authorityEpoch : Nat
  expiresAt : Nat
  remainingUses : Nat
  logicalTime : Nat
  targetOwnerApproved : Bool
  approvalReceipt : Bool
  dispatchReceipt : Bool
  effectReceipt : Bool
  independentObservation : Bool
  revocationReceipt : Bool
  rollbackExact : Bool
deriving DecidableEq, Repr

def AuthorityEvent.grant (event : AuthorityEvent) : Grant := {
  grantId := event.grantId
  principalId := event.principalId
  operationId := event.operationId
  targetId := event.targetId
  authority := event.authority
  epoch := event.authorityEpoch
  expiresAt := event.expiresAt
  remainingUses := event.remainingUses
}

def AuthorityEventValid (state : AuthorityState) (event : AuthorityEvent) : Bool :=
  decide (state.logicalTime < event.logicalTime) &&
  match event.kind with
  | .issue =>
      decide (state.activeGrant = none) &&
        decide (event.grantId ∉ state.revokedGrantIds) &&
        decide (0 < event.grantId) &&
        decide (event.authority ≤ state.callerCeiling) &&
        decide (event.authorityEpoch = state.authorityEpoch) &&
        decide (event.logicalTime ≤ event.expiresAt) &&
        decide (0 < event.remainingUses) &&
        event.targetOwnerApproved && event.approvalReceipt
  | .approve =>
      decide (state.activeGrant = some event.grant) &&
        decide (event.grantId ∉ state.revokedGrantIds) &&
        decide (event.authorityEpoch = state.authorityEpoch) &&
        decide (event.logicalTime ≤ event.expiresAt) &&
        decide (0 < event.remainingUses) &&
        event.targetOwnerApproved && event.approvalReceipt
  | .dispatch =>
      decide (state.activeGrant = some event.grant) &&
        decide (state.approvedGrantId = some event.grantId) &&
        decide (event.grantId ∉ state.revokedGrantIds) &&
        decide (event.authorityEpoch = state.authorityEpoch) &&
        decide (event.logicalTime ≤ event.expiresAt) &&
        decide (0 < event.remainingUses) && event.dispatchReceipt
  | .commitEffect =>
      decide (state.activeGrant = some event.grant) &&
        decide (state.approvedGrantId = some event.grantId) &&
        decide (state.dispatchedGrantId = some event.grantId) &&
        decide (event.grantId ∉ state.revokedGrantIds) &&
        decide (event.authorityEpoch = state.authorityEpoch) &&
        decide (event.logicalTime ≤ event.expiresAt) &&
        decide (0 < event.remainingUses) && event.effectReceipt
  | .observe =>
      decide (state.observedEffects < state.materialEffects) &&
        event.independentObservation && event.effectReceipt
  | .revoke =>
      decide (state.activeGrant = some event.grant) && event.revocationReceipt
  | .rollback =>
      decide (0 < state.materialEffects) &&
        decide (state.observedEffects = state.materialEffects) &&
        event.rollbackExact && event.effectReceipt

def ApplyAuthorityEvent (state : AuthorityState) (event : AuthorityEvent) : AuthorityState :=
  match event.kind with
  | .issue => { state with activeGrant := some event.grant, logicalTime := event.logicalTime }
  | .approve => { state with approvedGrantId := some event.grantId, logicalTime := event.logicalTime }
  | .dispatch => { state with dispatchedGrantId := some event.grantId, logicalTime := event.logicalTime }
  | .commitEffect =>
      { state with
          activeGrant := some { event.grant with remainingUses := event.remainingUses - 1 }
          approvedGrantId := none
          dispatchedGrantId := none
          materialEffects := state.materialEffects + 1
          logicalTime := event.logicalTime }
  | .observe =>
      { state with
          observedEffects := state.observedEffects + 1
          logicalTime := event.logicalTime }
  | .revoke =>
      { state with
          authorityEpoch := state.authorityEpoch + 1
          activeGrant := none
          approvedGrantId := none
          dispatchedGrantId := none
          revokedGrantIds := event.grantId :: state.revokedGrantIds
          logicalTime := event.logicalTime }
  | .rollback =>
      { state with
          materialEffects := 0
          observedEffects := 0
          rolledBack := true
          logicalTime := event.logicalTime }

def AuthorityStep (state : AuthorityState) (event : AuthorityEvent) : Option AuthorityState :=
  if AuthorityEventValid state event then some (ApplyAuthorityEvent state event) else none

def AuthorityRun : AuthorityState → List AuthorityEvent → Option AuthorityState
  | state, [] => some state
  | state, event :: tail =>
      match AuthorityStep state event with
      | none => none
      | some next => AuthorityRun next tail

theorem accepted_step_is_valid
    {state next : AuthorityState} {event : AuthorityEvent}
    (accepted : AuthorityStep state event = some next) :
    AuthorityEventValid state event = true := by
  unfold AuthorityStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_issue_respects_caller_ceiling_and_epoch
    {state next : AuthorityState} {event : AuthorityEvent}
    (kind : event.kind = .issue)
    (accepted : AuthorityStep state event = some next) :
    event.authority ≤ state.callerCeiling ∧
      event.authorityEpoch = state.authorityEpoch := by
  have valid := accepted_step_is_valid accepted
  simp [AuthorityEventValid, kind] at valid
  have fields :
      state.activeGrant = none ∧
        event.grantId ∉ state.revokedGrantIds ∧
        0 < event.grantId ∧
        event.authority ≤ state.callerCeiling ∧
        event.authorityEpoch = state.authorityEpoch ∧
        event.logicalTime ≤ event.expiresAt ∧
        0 < event.remainingUses ∧
        event.targetOwnerApproved = true ∧ event.approvalReceipt = true := by
    simpa [and_assoc] using valid.2
  rcases fields with ⟨_, _, _, ceiling, epoch, _⟩
  exact ⟨ceiling, epoch⟩

theorem accepted_dispatch_is_exactly_bound_and_fresh
    {state next : AuthorityState} {event : AuthorityEvent}
    (kind : event.kind = .dispatch)
    (accepted : AuthorityStep state event = some next) :
    state.activeGrant = some event.grant ∧
      state.approvedGrantId = some event.grantId ∧
      event.grantId ∉ state.revokedGrantIds ∧
      event.authorityEpoch = state.authorityEpoch ∧
      event.logicalTime ≤ event.expiresAt ∧
      0 < event.remainingUses ∧ event.dispatchReceipt = true := by
  have valid := accepted_step_is_valid accepted
  simp [AuthorityEventValid, kind] at valid
  simpa [and_assoc] using valid.2

theorem accepted_effect_requires_exact_live_grant_approval_and_dispatch
    {state next : AuthorityState} {event : AuthorityEvent}
    (kind : event.kind = .commitEffect)
    (accepted : AuthorityStep state event = some next) :
    state.activeGrant = some event.grant ∧
      state.approvedGrantId = some event.grantId ∧
      state.dispatchedGrantId = some event.grantId ∧
      event.grantId ∉ state.revokedGrantIds ∧
      event.authorityEpoch = state.authorityEpoch ∧
      event.logicalTime ≤ event.expiresAt ∧
      0 < event.remainingUses ∧ event.effectReceipt = true := by
  have valid := accepted_step_is_valid accepted
  simp [AuthorityEventValid, kind] at valid
  simpa [and_assoc] using valid.2

def initialState : AuthorityState where
  callerCeiling := 3
  authorityEpoch := 11
  logicalTime := 0
  activeGrant := none
  approvedGrantId := none
  dispatchedGrantId := none
  revokedGrantIds := []
  materialEffects := 0
  observedEffects := 0
  rolledBack := false

def issueEvent : AuthorityEvent where
  kind := .issue
  grantId := 71
  principalId := 101
  operationId := 201
  targetId := 301
  authority := 3
  authorityEpoch := 11
  expiresAt := 20
  remainingUses := 1
  logicalTime := 1
  targetOwnerApproved := true
  approvalReceipt := true
  dispatchReceipt := false
  effectReceipt := false
  independentObservation := false
  revocationReceipt := false
  rollbackExact := false

def successfulAuthorityTrace : List AuthorityEvent := [
  issueEvent,
  { issueEvent with kind := .approve, logicalTime := 2 },
  { issueEvent with kind := .dispatch, logicalTime := 3, dispatchReceipt := true },
  { issueEvent with kind := .commitEffect, logicalTime := 4, effectReceipt := true },
  { issueEvent with
      kind := .observe
      remainingUses := 0
      logicalTime := 5
      effectReceipt := true
      independentObservation := true },
  { issueEvent with
      kind := .rollback
      remainingUses := 0
      logicalTime := 6
      effectReceipt := true
      rollbackExact := true }
]

theorem exact_bound_authority_trace_reaches_observed_exact_rollback :
    AuthorityRun initialState successfulAuthorityTrace = some
      { initialState with
        activeGrant := some { issueEvent.grant with remainingUses := 0 }
        materialEffects := 0
        observedEffects := 0
        rolledBack := true
        logicalTime := 6 } := by
  native_decide

def activeState : AuthorityState :=
  { initialState with activeGrant := some issueEvent.grant, logicalTime := 1 }

def approvedState : AuthorityState :=
  { activeState with approvedGrantId := some issueEvent.grantId, logicalTime := 2 }

def dispatchedState : AuthorityState :=
  { approvedState with dispatchedGrantId := some issueEvent.grantId, logicalTime := 3 }

def revokedState : AuthorityState :=
  { initialState with
      authorityEpoch := 12
      logicalTime := 4
      revokedGrantIds := [issueEvent.grantId] }

theorem authority_widening_is_rejected :
    AuthorityStep initialState { issueEvent with authority := 4 } = none := by
  native_decide

theorem confused_deputy_principal_substitution_is_rejected :
    AuthorityStep approvedState
      { issueEvent with
          kind := .dispatch
          principalId := 999
          logicalTime := 3
          dispatchReceipt := true } = none := by
  native_decide

theorem expired_grant_dispatch_is_rejected :
    AuthorityStep approvedState
      { issueEvent with
          kind := .dispatch
          expiresAt := 2
          logicalTime := 3
          dispatchReceipt := true } = none := by
  native_decide

theorem stale_epoch_dispatch_is_rejected :
    AuthorityStep approvedState
      { issueEvent with
          kind := .dispatch
          authorityEpoch := 10
          logicalTime := 3
          dispatchReceipt := true } = none := by
  native_decide

theorem revoked_grant_dispatch_is_rejected :
    AuthorityStep revokedState
      { issueEvent with
          kind := .dispatch
          authorityEpoch := 12
          logicalTime := 5
          dispatchReceipt := true } = none := by
  native_decide

theorem effect_without_dispatch_is_rejected :
    AuthorityStep approvedState
      { issueEvent with kind := .commitEffect, logicalTime := 3, effectReceipt := true } = none := by
  native_decide

theorem consumed_one_shot_grant_cannot_effect_again :
    AuthorityStep
      { dispatchedState with
          activeGrant := some { issueEvent.grant with remainingUses := 0 }
          logicalTime := 4 }
      { issueEvent with
          kind := .commitEffect
          remainingUses := 0
          logicalTime := 5
          effectReceipt := true } = none := by
  native_decide

end AsiStackProofs.AuthorityEffectRefinement

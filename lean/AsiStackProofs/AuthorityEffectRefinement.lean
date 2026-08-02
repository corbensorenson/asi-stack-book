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

def AuthorityStateInvariant (state : AuthorityState) : Prop :=
  state.observedEffects ≤ state.materialEffects ∧
    (∀ grant, state.activeGrant = some grant →
      grant.authority ≤ state.callerCeiling ∧
        grant.epoch = state.authorityEpoch ∧
          grant.grantId ∉ state.revokedGrantIds) ∧
    (∀ grantId, state.approvedGrantId = some grantId →
      ∃ grant, state.activeGrant = some grant ∧ grant.grantId = grantId) ∧
    (∀ grantId, state.dispatchedGrantId = some grantId →
      state.approvedGrantId = some grantId ∧
        ∃ grant, state.activeGrant = some grant ∧ grant.grantId = grantId)

def AuthorityTraceValid : AuthorityState → List AuthorityEvent → Prop
  | _, [] => True
  | state, event :: tail =>
      AuthorityEventValid state event = true ∧
        AuthorityTraceValid (ApplyAuthorityEvent state event) tail

theorem accepted_step_is_valid
    {state next : AuthorityState} {event : AuthorityEvent}
    (accepted : AuthorityStep state event = some next) :
    AuthorityEventValid state event = true := by
  unfold AuthorityStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_step_applies_event
    {state next : AuthorityState} {event : AuthorityEvent}
    (accepted : AuthorityStep state event = some next) :
    next = ApplyAuthorityEvent state event := by
  unfold AuthorityStep at accepted
  split at accepted
  · exact Option.some.inj accepted |>.symm
  · simp at accepted

theorem apply_event_preserves_caller_ceiling
    (state : AuthorityState) (event : AuthorityEvent) :
    (ApplyAuthorityEvent state event).callerCeiling = state.callerCeiling := by
  unfold ApplyAuthorityEvent
  split <;> rfl

theorem apply_event_preserves_revoked_grant
    {state : AuthorityState} {event : AuthorityEvent} {grantId : Nat}
    (revoked : grantId ∈ state.revokedGrantIds) :
    grantId ∈ (ApplyAuthorityEvent state event).revokedGrantIds := by
  unfold ApplyAuthorityEvent
  split <;> simp [revoked]

theorem invariant_without_active_grant_has_no_custody
    {state : AuthorityState}
    (safe : AuthorityStateInvariant state)
    (inactive : state.activeGrant = none) :
    state.approvedGrantId = none ∧ state.dispatchedGrantId = none := by
  rcases safe with ⟨_, _, approved, dispatched⟩
  constructor
  · cases approval : state.approvedGrantId with
    | none => rfl
    | some grantId =>
        rcases approved grantId approval with ⟨grant, active, _⟩
        rw [inactive] at active
        contradiction
  · cases dispatch : state.dispatchedGrantId with
    | none => rfl
    | some grantId =>
        rcases dispatched grantId dispatch with ⟨_, grant, active, _⟩
        rw [inactive] at active
        contradiction

theorem accepted_step_preserves_state_invariant
    {state next : AuthorityState} {event : AuthorityEvent}
    (safe : AuthorityStateInvariant state)
    (accepted : AuthorityStep state event = some next) :
    AuthorityStateInvariant next := by
  have valid := accepted_step_is_valid accepted
  have applies := accepted_step_applies_event accepted
  subst next
  rcases safe with ⟨observed, live, approved, dispatched⟩
  cases kind : event.kind
  · simp [AuthorityEventValid, kind] at valid
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
    rcases fields with
      ⟨active, notRevoked, _, ceiling, epoch, _, _, _, _⟩
    have noCustody := invariant_without_active_grant_has_no_custody
      ⟨observed, live, approved, dispatched⟩ active
    simp only [AuthorityStateInvariant, ApplyAuthorityEvent, kind]
    refine ⟨observed, ?_, ?_, ?_⟩
    · intro grant grantActive
      simp at grantActive
      subst grant
      exact ⟨ceiling, epoch, notRevoked⟩
    · simp [noCustody.1]
    · simp [noCustody.2]
  · simp [AuthorityEventValid, kind] at valid
    have fields :
        state.activeGrant = some event.grant ∧
          event.grantId ∉ state.revokedGrantIds ∧
          event.authorityEpoch = state.authorityEpoch ∧
          event.logicalTime ≤ event.expiresAt ∧
          0 < event.remainingUses ∧
          event.targetOwnerApproved = true ∧ event.approvalReceipt = true := by
      simpa [and_assoc] using valid.2
    rcases fields with ⟨active, _, _, _, _, _, _⟩
    simp only [AuthorityStateInvariant, ApplyAuthorityEvent, kind]
    refine ⟨observed, live, ?_, ?_⟩
    intro grantId approvedId
    simp at approvedId
    subst grantId
    exact ⟨event.grant, active, rfl⟩
    intro grantId dispatchedId
    rcases dispatched grantId dispatchedId with
      ⟨_, grant, grantActive, grantIdentity⟩
    have grantEq : grant = event.grant :=
      Option.some.inj (grantActive.symm.trans active)
    subst grant
    have idEq : event.grantId = grantId := by
      simpa [AuthorityEvent.grant] using grantIdentity
    exact ⟨congrArg some idEq, event.grant, active, idEq⟩
  · simp [AuthorityEventValid, kind] at valid
    have fields :
        state.activeGrant = some event.grant ∧
          state.approvedGrantId = some event.grantId ∧
          event.grantId ∉ state.revokedGrantIds ∧
          event.authorityEpoch = state.authorityEpoch ∧
          event.logicalTime ≤ event.expiresAt ∧
          0 < event.remainingUses ∧ event.dispatchReceipt = true := by
      simpa [and_assoc] using valid.2
    rcases fields with ⟨active, approvedId, _, _, _, _, _⟩
    simp only [AuthorityStateInvariant, ApplyAuthorityEvent, kind]
    refine ⟨observed, live, approved, ?_⟩
    intro grantId dispatchedId
    simp at dispatchedId
    subst grantId
    exact ⟨approvedId, event.grant, active, rfl⟩
  · simp [AuthorityEventValid, kind] at valid
    have fields :
        state.activeGrant = some event.grant ∧
          state.approvedGrantId = some event.grantId ∧
          state.dispatchedGrantId = some event.grantId ∧
          event.grantId ∉ state.revokedGrantIds ∧
          event.authorityEpoch = state.authorityEpoch ∧
          event.logicalTime ≤ event.expiresAt ∧
          0 < event.remainingUses ∧ event.effectReceipt = true := by
      simpa [and_assoc] using valid.2
    rcases fields with
      ⟨active, _, _, notRevoked, epoch, _, _, _⟩
    have grantSafe := live event.grant active
    simp only [AuthorityStateInvariant, ApplyAuthorityEvent, kind]
    refine ⟨Nat.le.step observed, ?_, ?_, ?_⟩
    · intro grant grantActive
      simp at grantActive
      subst grant
      exact ⟨grantSafe.1, epoch, notRevoked⟩
    · simp
    · simp
  · simp [AuthorityEventValid, kind] at valid
    simp only [AuthorityStateInvariant, ApplyAuthorityEvent, kind]
    exact ⟨Nat.succ_le_of_lt valid.2.1.1, live, approved, dispatched⟩
  · simp only [AuthorityStateInvariant, ApplyAuthorityEvent, kind]
    refine ⟨observed, ?_, ?_, ?_⟩ <;> simp
  · simp only [AuthorityStateInvariant, ApplyAuthorityEvent, kind]
    exact ⟨Nat.zero_le _, live, approved, dispatched⟩

theorem successful_run_preserves_state_invariant
    {state final : AuthorityState} {events : List AuthorityEvent}
    (safe : AuthorityStateInvariant state)
    (ran : AuthorityRun state events = some final) :
    AuthorityStateInvariant final := by
  induction events generalizing state with
  | nil =>
      simp [AuthorityRun] at ran
      subst final
      exact safe
  | cons event tail ih =>
      cases stepped : AuthorityStep state event with
      | none => simp [AuthorityRun, stepped] at ran
      | some next =>
          have tailRan : AuthorityRun next tail = some final := by
            simpa [AuthorityRun, stepped] using ran
          exact ih (accepted_step_preserves_state_invariant safe stepped) tailRan

theorem successful_run_preserves_caller_ceiling
    {state final : AuthorityState} {events : List AuthorityEvent}
    (ran : AuthorityRun state events = some final) :
    final.callerCeiling = state.callerCeiling := by
  induction events generalizing state with
  | nil =>
      simp [AuthorityRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : AuthorityStep state event with
      | none => simp [AuthorityRun, stepped] at ran
      | some next =>
          have tailRan : AuthorityRun next tail = some final := by
            simpa [AuthorityRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          calc
            final.callerCeiling = next.callerCeiling := ih tailRan
            _ = (ApplyAuthorityEvent state event).callerCeiling := by rw [applies]
            _ = state.callerCeiling := apply_event_preserves_caller_ceiling state event

theorem successful_run_has_valid_trace
    {state final : AuthorityState} {events : List AuthorityEvent}
    (ran : AuthorityRun state events = some final) :
    AuthorityTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : AuthorityStep state event with
      | none => simp [AuthorityRun, stepped] at ran
      | some next =>
          have tailRan : AuthorityRun next tail = some final := by
            simpa [AuthorityRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          subst next
          exact ⟨accepted_step_is_valid stepped, ih tailRan⟩

theorem run_composes_across_event_batches
    (state : AuthorityState) (left right : List AuthorityEvent) :
    AuthorityRun state (left ++ right) =
      match AuthorityRun state left with
      | none => none
      | some middle => AuthorityRun middle right := by
  induction left generalizing state with
  | nil => simp [AuthorityRun]
  | cons event tail ih =>
      cases stepped : AuthorityStep state event <;>
        simp [AuthorityRun, stepped, ih]

theorem successful_run_preserves_revoked_grant
    {state final : AuthorityState} {events : List AuthorityEvent} {grantId : Nat}
    (revoked : grantId ∈ state.revokedGrantIds)
    (ran : AuthorityRun state events = some final) :
    grantId ∈ final.revokedGrantIds := by
  induction events generalizing state with
  | nil =>
      simp [AuthorityRun] at ran
      subst final
      exact revoked
  | cons event tail ih =>
      cases stepped : AuthorityStep state event with
      | none => simp [AuthorityRun, stepped] at ran
      | some next =>
          have tailRan : AuthorityRun next tail = some final := by
            simpa [AuthorityRun, stepped] using ran
          have applies := accepted_step_applies_event stepped
          subst next
          exact ih (apply_event_preserves_revoked_grant revoked) tailRan

def NoEffectForGrant (grantId : Nat) (events : List AuthorityEvent) : Prop :=
  ∀ event, event ∈ events → event.kind = .commitEffect → event.grantId ≠ grantId

theorem revoked_grant_cannot_commit_effect_in_successful_suffix
    {state final : AuthorityState} {events : List AuthorityEvent} {grantId : Nat}
    (revoked : grantId ∈ state.revokedGrantIds)
    (ran : AuthorityRun state events = some final) :
    NoEffectForGrant grantId events := by
  unfold NoEffectForGrant
  induction events generalizing state with
  | nil => simp
  | cons event tail ih =>
      intro candidate present effectKind sameGrant
      cases stepped : AuthorityStep state event with
      | none => simp [AuthorityRun, stepped] at ran
      | some next =>
          have tailRan : AuthorityRun next tail = some final := by
            simpa [AuthorityRun, stepped] using ran
          rcases List.mem_cons.mp present with same | inTail
          · subst candidate
            have valid := accepted_step_is_valid stepped
            simp [AuthorityEventValid, effectKind] at valid
            have fields :
                state.activeGrant = some event.grant ∧
                  state.approvedGrantId = some event.grantId ∧
                  state.dispatchedGrantId = some event.grantId ∧
                  event.grantId ∉ state.revokedGrantIds ∧
                  event.authorityEpoch = state.authorityEpoch ∧
                  event.logicalTime ≤ event.expiresAt ∧
                  0 < event.remainingUses ∧ event.effectReceipt = true := by
              simpa [and_assoc] using valid.2
            exact fields.2.2.2.1 (sameGrant ▸ revoked)
          · have applies := accepted_step_applies_event stepped
            subst next
            exact ih (apply_event_preserves_revoked_grant revoked) tailRan candidate
              inTail effectKind sameGrant

def UsesGrantAuthority (event : AuthorityEvent) : Prop :=
  event.kind = .approve ∨ event.kind = .dispatch ∨ event.kind = .commitEffect

def NoAuthorityUseForGrant (grantId : Nat) (events : List AuthorityEvent) : Prop :=
  ∀ event, event ∈ events → UsesGrantAuthority event → event.grantId ≠ grantId

theorem accepted_grant_use_is_not_revoked
    {state next : AuthorityState} {event : AuthorityEvent}
    (accepted : AuthorityStep state event = some next)
    (uses : UsesGrantAuthority event) :
    event.grantId ∉ state.revokedGrantIds := by
  have valid := accepted_step_is_valid accepted
  rcases uses with approve | dispatch | effect
  · simp [AuthorityEventValid, approve] at valid
    have fields :
        state.activeGrant = some event.grant ∧
          event.grantId ∉ state.revokedGrantIds ∧
          event.authorityEpoch = state.authorityEpoch ∧
          event.logicalTime ≤ event.expiresAt ∧
          0 < event.remainingUses ∧
          event.targetOwnerApproved = true ∧ event.approvalReceipt = true := by
      simpa [and_assoc] using valid.2
    exact fields.2.1
  · simp [AuthorityEventValid, dispatch] at valid
    have fields :
        state.activeGrant = some event.grant ∧
          state.approvedGrantId = some event.grantId ∧
          event.grantId ∉ state.revokedGrantIds ∧
          event.authorityEpoch = state.authorityEpoch ∧
          event.logicalTime ≤ event.expiresAt ∧
          0 < event.remainingUses ∧ event.dispatchReceipt = true := by
      simpa [and_assoc] using valid.2
    exact fields.2.2.1
  · simp [AuthorityEventValid, effect] at valid
    have fields :
        state.activeGrant = some event.grant ∧
          state.approvedGrantId = some event.grantId ∧
          state.dispatchedGrantId = some event.grantId ∧
          event.grantId ∉ state.revokedGrantIds ∧
          event.authorityEpoch = state.authorityEpoch ∧
          event.logicalTime ≤ event.expiresAt ∧
          0 < event.remainingUses ∧ event.effectReceipt = true := by
      simpa [and_assoc] using valid.2
    exact fields.2.2.2.1

theorem revoked_grant_cannot_be_used_in_successful_suffix
    {state final : AuthorityState} {events : List AuthorityEvent} {grantId : Nat}
    (revoked : grantId ∈ state.revokedGrantIds)
    (ran : AuthorityRun state events = some final) :
    NoAuthorityUseForGrant grantId events := by
  unfold NoAuthorityUseForGrant
  induction events generalizing state with
  | nil => simp
  | cons event tail ih =>
      intro candidate present uses sameGrant
      cases stepped : AuthorityStep state event with
      | none => simp [AuthorityRun, stepped] at ran
      | some next =>
          have tailRan : AuthorityRun next tail = some final := by
            simpa [AuthorityRun, stepped] using ran
          rcases List.mem_cons.mp present with same | inTail
          · subst candidate
            exact (accepted_grant_use_is_not_revoked stepped uses) (sameGrant ▸ revoked)
          · have applies := accepted_step_applies_event stepped
            subst next
            exact ih (apply_event_preserves_revoked_grant revoked) tailRan candidate
              inTail uses sameGrant

theorem rejected_step_returns_no_successor
    (state : AuthorityState) (event : AuthorityEvent)
    (rejected : AuthorityEventValid state event = false) :
    AuthorityStep state event = none := by
  simp [AuthorityStep, rejected]

theorem accepted_rollback_clears_effect_accounting
    {state next : AuthorityState} {event : AuthorityEvent}
    (kind : event.kind = .rollback)
    (accepted : AuthorityStep state event = some next) :
    next.materialEffects = 0 ∧ next.observedEffects = 0 ∧ next.rolledBack = true := by
  have applies := accepted_step_applies_event accepted
  subst next
  simp [ApplyAuthorityEvent, kind]

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

theorem initial_state_satisfies_authority_invariant :
    AuthorityStateInvariant initialState := by
  simp [AuthorityStateInvariant, initialState]

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

def twoUseIssueEvent : AuthorityEvent := { issueEvent with remainingUses := 2 }

def successfulTwoUseTrace : List AuthorityEvent := [
  twoUseIssueEvent,
  { twoUseIssueEvent with kind := .approve, logicalTime := 2 },
  { twoUseIssueEvent with kind := .dispatch, logicalTime := 3, dispatchReceipt := true },
  { twoUseIssueEvent with kind := .commitEffect, logicalTime := 4, effectReceipt := true },
  { twoUseIssueEvent with kind := .approve, remainingUses := 1, logicalTime := 5 },
  { twoUseIssueEvent with
      kind := .dispatch
      remainingUses := 1
      logicalTime := 6
      dispatchReceipt := true },
  { twoUseIssueEvent with
      kind := .commitEffect
      remainingUses := 1
      logicalTime := 7
      effectReceipt := true },
  { twoUseIssueEvent with
      kind := .observe
      remainingUses := 0
      logicalTime := 8
      effectReceipt := true
      independentObservation := true },
  { twoUseIssueEvent with
      kind := .observe
      remainingUses := 0
      logicalTime := 9
      effectReceipt := true
      independentObservation := true },
  { twoUseIssueEvent with
      kind := .rollback
      remainingUses := 0
      logicalTime := 10
      effectReceipt := true
      rollbackExact := true }
]

def successfulRevocationTrace : List AuthorityEvent := [
  issueEvent,
  { issueEvent with kind := .approve, logicalTime := 2 },
  { issueEvent with kind := .dispatch, logicalTime := 3, dispatchReceipt := true },
  { issueEvent with kind := .revoke, logicalTime := 4, revocationReceipt := true }
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

theorem two_use_trace_reaches_two_observations_and_exact_rollback :
    AuthorityRun initialState successfulTwoUseTrace = some
      { initialState with
        activeGrant := some { twoUseIssueEvent.grant with remainingUses := 0 }
        materialEffects := 0
        observedEffects := 0
        rolledBack := true
        logicalTime := 10 } := by
  native_decide

theorem revocation_trace_closes_custody_and_advances_epoch :
    AuthorityRun initialState successfulRevocationTrace = some
      { initialState with
        authorityEpoch := 12
        activeGrant := none
        approvedGrantId := none
        dispatchedGrantId := none
        revokedGrantIds := [issueEvent.grantId]
        logicalTime := 4 } := by
  native_decide

theorem every_successful_reference_trace_preserves_authority_invariant :
    ∀ final, AuthorityRun initialState successfulAuthorityTrace = some final →
      AuthorityStateInvariant final := by
  intro final ran
  exact successful_run_preserves_state_invariant
    initial_state_satisfies_authority_invariant ran

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

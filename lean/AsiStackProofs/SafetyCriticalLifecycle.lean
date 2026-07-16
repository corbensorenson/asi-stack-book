namespace AsiStackProofs.SafetyCriticalLifecycle

/-!
A shared transition system for the five safety-critical proof surfaces.

The older chapter-local modules remain useful as finite route specifications, but
their smallest "operational invariant" theorems merely projected assumptions.
This module instead makes admission a property of the transition function.  A
successful trace therefore carries evidence about what the machine actually
accepted, while rejected traces serve as executable countermodels.
-/

def traceCorpusSha256 : String :=
  "991bf35d88008e2ff3e356e15a689d38db9a81b700f75fa4a6fff57e4c03a1af"

inductive Domain where
  | alignment
  | corrigibility
  | valueConflict
  | governanceRights
  | selfImprovement
deriving DecidableEq, Repr

inductive Phase where
  | proposed
  | evidenceReady
  | effectCommitted
  | promoted
  | residualized
  | rolledBack
  | revoked
deriving DecidableEq, Repr

inductive Requirement where
  | protectedPredicate
  | operationalTest
  | affectedParty
  | materialNotice
  | preEffectReview
  | currentApproval
  | boundedDelegation
  | correctionPath
  | rollbackPath
  | residualRecord
  | accountablePrincipal
  | auditMaterial
  | appealPath
  | exitExport
  | forkSafetyReview
  | forkObligations
  | dissentPayload
  | durableReceipt
  | independentEvaluator
  | monitorWindow
  | evidenceTransition
  | nonClaimBoundary
deriving DecidableEq, Repr

structure Evidence where
  protectedPredicate : Bool := false
  operationalTest : Bool := false
  affectedParty : Bool := false
  materialNotice : Bool := false
  preEffectReview : Bool := false
  currentApproval : Bool := false
  boundedDelegation : Bool := false
  correctionPath : Bool := false
  rollbackPath : Bool := false
  residualRecord : Bool := false
  accountablePrincipal : Bool := false
  auditMaterial : Bool := false
  appealPath : Bool := false
  exitExport : Bool := false
  forkSafetyReview : Bool := false
  forkObligations : Bool := false
  dissentPayload : Bool := false
  durableReceipt : Bool := false
  independentEvaluator : Bool := false
  monitorWindow : Bool := false
  evidenceTransition : Bool := false
  nonClaimBoundary : Bool := false
deriving DecidableEq, Repr

def recordRequirement (evidence : Evidence) : Requirement -> Evidence
  | .protectedPredicate => { evidence with protectedPredicate := true }
  | .operationalTest => { evidence with operationalTest := true }
  | .affectedParty => { evidence with affectedParty := true }
  | .materialNotice => { evidence with materialNotice := true }
  | .preEffectReview => { evidence with preEffectReview := true }
  | .currentApproval => { evidence with currentApproval := true }
  | .boundedDelegation => { evidence with boundedDelegation := true }
  | .correctionPath => { evidence with correctionPath := true }
  | .rollbackPath => { evidence with rollbackPath := true }
  | .residualRecord => { evidence with residualRecord := true }
  | .accountablePrincipal => { evidence with accountablePrincipal := true }
  | .auditMaterial => { evidence with auditMaterial := true }
  | .appealPath => { evidence with appealPath := true }
  | .exitExport => { evidence with exitExport := true }
  | .forkSafetyReview => { evidence with forkSafetyReview := true }
  | .forkObligations => { evidence with forkObligations := true }
  | .dissentPayload => { evidence with dissentPayload := true }
  | .durableReceipt => { evidence with durableReceipt := true }
  | .independentEvaluator => { evidence with independentEvaluator := true }
  | .monitorWindow => { evidence with monitorWindow := true }
  | .evidenceTransition => { evidence with evidenceTransition := true }
  | .nonClaimBoundary => { evidence with nonClaimBoundary := true }

def Evidence.alignmentReady (e : Evidence) : Bool :=
  e.protectedPredicate && e.operationalTest && e.preEffectReview &&
    e.correctionPath && e.rollbackPath && e.independentEvaluator

def Evidence.corrigibilityReady (e : Evidence) : Bool :=
  e.affectedParty && e.materialNotice && e.preEffectReview &&
    e.currentApproval && e.boundedDelegation && e.correctionPath &&
    e.rollbackPath && e.accountablePrincipal

def Evidence.valueConflictReady (e : Evidence) : Bool :=
  e.preEffectReview && e.residualRecord && e.dissentPayload &&
    e.correctionPath && e.accountablePrincipal

def Evidence.governanceRightsReady (e : Evidence) : Bool :=
  e.protectedPredicate && e.auditMaterial && e.appealPath && e.exitExport &&
    e.forkSafetyReview && e.forkObligations && e.dissentPayload &&
    e.durableReceipt && e.correctionPath

def Evidence.selfImprovementReady (e : Evidence) : Bool :=
  e.protectedPredicate && e.preEffectReview && e.independentEvaluator &&
    e.rollbackPath && e.monitorWindow && e.evidenceTransition

def Evidence.readyFor (e : Evidence) : Domain -> Bool
  | .alignment => e.alignmentReady
  | .corrigibility => e.corrigibilityReady
  | .valueConflict => e.valueConflictReady
  | .governanceRights => e.governanceRightsReady
  | .selfImprovement => e.selfImprovementReady

def Evidence.promotionReady (e : Evidence) : Bool :=
  e.evidenceTransition && e.nonClaimBoundary && e.durableReceipt

structure State where
  domain : Domain
  phase : Phase := .proposed
  evidence : Evidence := {}
  highImpact : Bool := false
  supportPromotionRequested : Bool := false
  authority : Nat
  authorityCeiling : Nat
deriving DecidableEq, Repr

def State.invariant (state : State) : Prop :=
  state.evidence.protectedPredicate = true ∧
    state.authority ≤ state.authorityCeiling

def State.effectReady (state : State) : Bool :=
  state.evidence.readyFor state.domain &&
    decide (state.authority ≤ state.authorityCeiling)

def State.promotionReady (state : State) : Bool :=
  state.phase == .effectCommitted &&
    state.supportPromotionRequested &&
    state.evidence.promotionReady

inductive Event where
  | record (requirement : Requirement)
  | declareHighImpact
  | requestSupportPromotion
  | commitEffect
  | promoteSupport
  | narrowAuthority (newScope : Nat)
  | widenAuthority (newScope : Nat)
  | removeProtectedPredicate
  | rollback
  | revoke
deriving DecidableEq, Repr

def step (state : State) : Event -> Option State
  | .record requirement =>
      some { state with evidence := recordRequirement state.evidence requirement }
  | .declareHighImpact => some { state with highImpact := true }
  | .requestSupportPromotion =>
      some { state with supportPromotionRequested := true }
  | .commitEffect =>
      if state.effectReady then
        some { state with phase := .effectCommitted }
      else
        none
  | .promoteSupport =>
      if state.promotionReady then
        some { state with phase := .promoted }
      else
        none
  | .narrowAuthority newScope =>
      if newScope ≤ state.authority then
        some { state with authority := newScope }
      else
        none
  | .widenAuthority newScope =>
      if state.authority < newScope then none
      else some { state with authority := newScope }
  | .removeProtectedPredicate => none
  | .rollback =>
      if state.evidence.rollbackPath &&
          (state.phase == .effectCommitted || state.phase == .promoted) then
        some { state with phase := .rolledBack }
      else
        none
  | .revoke => some { state with authority := 0, phase := .revoked }

def run : State -> List Event -> Option State
  | state, [] => some state
  | state, event :: rest =>
      match step state event with
      | none => none
      | some next => run next rest

theorem protected_predicate_removal_is_unrepresentable
    (state : State) :
    step state .removeProtectedPredicate = none := by
  rfl

theorem authority_widening_is_rejected
    (state : State) (newScope : Nat)
    (wider : state.authority < newScope) :
    step state (.widenAuthority newScope) = none := by
  simp [step, wider]

theorem successful_effect_commit_was_ready
    {state next : State}
    (accepted : step state .commitEffect = some next) :
    state.effectReady = true := by
  simp [step] at accepted
  exact accepted.1

theorem successful_support_promotion_was_ready
    {state next : State}
    (accepted : step state .promoteSupport = some next) :
    state.promotionReady = true := by
  simp [step] at accepted
  exact accepted.1

theorem step_preserves_protected_predicate
    {state next : State} {event : Event}
    (predicateProtected : state.evidence.protectedPredicate = true)
    (accepted : step state event = some next) :
    next.evidence.protectedPredicate = true := by
  cases event with
  | record requirement =>
      cases requirement <;> simp [step, recordRequirement] at accepted <;>
        subst next <;> simp_all
  | declareHighImpact =>
      simp [step] at accepted
      subst next
      exact predicateProtected
  | requestSupportPromotion =>
      simp [step] at accepted
      subst next
      exact predicateProtected
  | commitEffect =>
      simp [step] at accepted
      obtain ⟨_, rfl⟩ := accepted
      exact predicateProtected
  | promoteSupport =>
      simp [step] at accepted
      obtain ⟨_, rfl⟩ := accepted
      exact predicateProtected
  | narrowAuthority newScope =>
      simp [step] at accepted
      obtain ⟨_, rfl⟩ := accepted
      exact predicateProtected
  | widenAuthority newScope =>
      simp [step] at accepted
      obtain ⟨_, rfl⟩ := accepted
      exact predicateProtected
  | removeProtectedPredicate => simp [step] at accepted
  | rollback =>
      simp [step] at accepted
      obtain ⟨_, rfl⟩ := accepted
      exact predicateProtected
  | revoke =>
      simp [step] at accepted
      subst next
      exact predicateProtected

theorem step_never_increases_authority
    {state next : State} {event : Event}
    (accepted : step state event = some next) :
    next.authority ≤ state.authority := by
  cases event with
  | record requirement =>
      simp [step] at accepted
      subst next
      exact Nat.le_refl _
  | declareHighImpact =>
      simp [step] at accepted
      subst next
      exact Nat.le_refl _
  | requestSupportPromotion =>
      simp [step] at accepted
      subst next
      exact Nat.le_refl _
  | commitEffect =>
      simp [step] at accepted
      obtain ⟨_, rfl⟩ := accepted
      exact Nat.le_refl _
  | promoteSupport =>
      simp [step] at accepted
      obtain ⟨_, rfl⟩ := accepted
      exact Nat.le_refl _
  | narrowAuthority newScope =>
      simp [step] at accepted
      rw [← accepted.2]
      exact accepted.1
  | widenAuthority newScope =>
      simp [step] at accepted
      rw [← accepted.2]
      exact accepted.1
  | removeProtectedPredicate => simp [step] at accepted
  | rollback =>
      simp [step] at accepted
      obtain ⟨_, rfl⟩ := accepted
      exact Nat.le_refl _
  | revoke =>
      simp [step] at accepted
      subst next
      exact Nat.zero_le _

theorem step_preserves_authority_ceiling
    {state next : State} {event : Event}
    (accepted : step state event = some next) :
    next.authorityCeiling = state.authorityCeiling := by
  cases event with
  | record requirement => simp [step] at accepted; subst next; rfl
  | declareHighImpact => simp [step] at accepted; subst next; rfl
  | requestSupportPromotion => simp [step] at accepted; subst next; rfl
  | commitEffect => simp [step] at accepted; obtain ⟨_, rfl⟩ := accepted; rfl
  | promoteSupport => simp [step] at accepted; obtain ⟨_, rfl⟩ := accepted; rfl
  | narrowAuthority newScope => simp [step] at accepted; obtain ⟨_, rfl⟩ := accepted; rfl
  | widenAuthority newScope => simp [step] at accepted; obtain ⟨_, rfl⟩ := accepted; rfl
  | removeProtectedPredicate => simp [step] at accepted
  | rollback => simp [step] at accepted; obtain ⟨_, rfl⟩ := accepted; rfl
  | revoke => simp [step] at accepted; subst next; rfl

theorem step_preserves_invariant
    {state next : State} {event : Event}
    (invariant : state.invariant)
    (accepted : step state event = some next) :
    next.invariant := by
  constructor
  · exact step_preserves_protected_predicate invariant.1 accepted
  · rw [step_preserves_authority_ceiling accepted]
    exact Nat.le_trans (step_never_increases_authority accepted) invariant.2

theorem run_preserves_invariant
    {state next : State} {trace : List Event}
    (invariant : state.invariant)
    (accepted : run state trace = some next) :
    next.invariant := by
  induction trace generalizing state with
  | nil =>
      simp [run] at accepted
      simpa [accepted] using invariant
  | cons event rest inductionHypothesis =>
      simp [run] at accepted
      split at accepted
      · contradiction
      · rename_i intermediate stepAccepted
        exact inductionHypothesis
          (step_preserves_invariant invariant stepAccepted) accepted

theorem run_append
    (state : State) (left right : List Event) :
    run state (left ++ right) =
      match run state left with
      | none => none
      | some intermediate => run intermediate right := by
  induction left generalizing state with
  | nil => simp [run]
  | cons event rest inductionHypothesis =>
      simp [run]
      split
      · rfl
      · rename_i intermediate stepAccepted
        exact inductionHypothesis intermediate

def initialState (domain : Domain) : State :=
  { domain := domain,
    evidence := { protectedPredicate := true },
    authority := 3,
    authorityCeiling := 3 }

def alignmentEvidenceTrace : List Event :=
  [.record .operationalTest, .record .preEffectReview,
   .record .correctionPath, .record .rollbackPath,
   .record .independentEvaluator, .commitEffect]

def corrigibilityEvidenceTrace : List Event :=
  [.record .affectedParty, .record .materialNotice,
   .record .preEffectReview, .record .currentApproval,
   .record .boundedDelegation, .record .correctionPath,
   .record .rollbackPath, .record .accountablePrincipal,
   .commitEffect]

def valueConflictEvidenceTrace : List Event :=
  [.record .preEffectReview, .record .residualRecord,
   .record .dissentPayload, .record .correctionPath,
   .record .accountablePrincipal, .commitEffect]

def governanceRightsEvidenceTrace : List Event :=
  [.record .auditMaterial, .record .appealPath, .record .exitExport,
   .record .forkSafetyReview, .record .forkObligations,
   .record .dissentPayload, .record .durableReceipt,
   .record .correctionPath, .commitEffect]

def selfImprovementEvidenceTrace : List Event :=
  [.record .preEffectReview, .record .independentEvaluator,
   .record .rollbackPath, .record .monitorWindow,
   .record .evidenceTransition, .commitEffect]

theorem alignment_complete_trace_commits :
    (run (initialState .alignment) alignmentEvidenceTrace).isSome = true := by
  native_decide

theorem corrigibility_complete_trace_commits :
    (run (initialState .corrigibility) corrigibilityEvidenceTrace).isSome = true := by
  native_decide

theorem value_conflict_complete_trace_commits :
    (run (initialState .valueConflict) valueConflictEvidenceTrace).isSome = true := by
  native_decide

theorem governance_rights_complete_trace_commits :
    (run (initialState .governanceRights) governanceRightsEvidenceTrace).isSome = true := by
  native_decide

theorem self_improvement_complete_trace_commits :
    (run (initialState .selfImprovement) selfImprovementEvidenceTrace).isSome = true := by
  native_decide

theorem alignment_missing_review_is_rejected :
    run (initialState .alignment)
      [.record .operationalTest, .record .correctionPath,
       .record .rollbackPath, .record .independentEvaluator,
       .commitEffect] = none := by
  native_decide

theorem corrigibility_missing_affected_party_is_rejected :
    run (initialState .corrigibility)
      [.record .materialNotice, .record .preEffectReview,
       .record .currentApproval, .record .boundedDelegation,
       .record .correctionPath, .record .rollbackPath,
       .record .accountablePrincipal, .commitEffect] = none := by
  native_decide

theorem value_conflict_missing_residual_is_rejected :
    run (initialState .valueConflict)
      [.record .preEffectReview, .record .dissentPayload,
       .record .correctionPath, .record .accountablePrincipal,
       .commitEffect] = none := by
  native_decide

theorem governance_rights_missing_exit_is_rejected :
    run (initialState .governanceRights)
      [.record .auditMaterial, .record .appealPath,
       .record .forkSafetyReview, .record .forkObligations,
       .record .dissentPayload, .record .durableReceipt,
       .record .correctionPath, .commitEffect] = none := by
  native_decide

theorem self_improvement_without_independent_evaluator_is_rejected :
    run (initialState .selfImprovement)
      [.record .preEffectReview, .record .rollbackPath,
       .record .monitorWindow, .record .evidenceTransition,
       .commitEffect] = none := by
  native_decide

theorem support_promotion_without_receipt_and_nonclaim_is_rejected :
    run (initialState .alignment)
      (alignmentEvidenceTrace ++
        [.requestSupportPromotion, .record .evidenceTransition,
         .promoteSupport]) = none := by
  native_decide

end AsiStackProofs.SafetyCriticalLifecycle

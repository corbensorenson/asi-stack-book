namespace AsiStackProofs.StableCapabilityFields

inductive AuthorityLevel where
  | none
  | read
  | transform
  | write
  | execute
  | approve
deriving DecidableEq, Repr

def AuthorityLevel.rank : AuthorityLevel -> Nat
  | .none => 0
  | .read => 1
  | .transform => 2
  | .write => 3
  | .execute => 4
  | .approve => 5

structure StableCapabilityField where
  authorityCeiling : AuthorityLevel
deriving DecidableEq, Repr

structure ImplementationCandidate where
  satisfiesQualification : Bool
  requestedAuthority : AuthorityLevel
  governanceGrant : Bool
deriving DecidableEq, Repr

def ReplacementAllowed (field : StableCapabilityField) (candidate : ImplementationCandidate) : Prop :=
  candidate.satisfiesQualification = true ∧
    (candidate.requestedAuthority.rank <= field.authorityCeiling.rank ∨
      candidate.governanceGrant = true)

theorem authority_expanding_replacement_without_grant_rejected
    {field : StableCapabilityField} {candidate : ImplementationCandidate} :
    field.authorityCeiling.rank < candidate.requestedAuthority.rank ->
    candidate.governanceGrant = false ->
    ¬ ReplacementAllowed field candidate := by
  intro expands noGrant allowed
  unfold ReplacementAllowed at allowed
  cases allowed.2 with
  | inl withinCeiling =>
      exact Nat.not_le_of_gt expands withinCeiling
  | inr grant =>
      rw [noGrant] at grant
      cases grant

inductive ScfLifecycleRoute where
  | defaultRoute
  | canaryRoute
  | requireRequalification
  | requireRollback
  | requestGovernanceReview
  | rejectReplacement
deriving DecidableEq, Repr

structure ScfLifecycleReview where
  fieldIdentityMatches : Bool
  qualificationSatisfied : Bool
  evidenceRefsPresent : Bool
  leaseFresh : Bool
  evaluatorIndependent : Bool
  authorityWithinCeiling : Bool
  governanceGrant : Bool
  rollbackReady : Bool
  regressionFloorPreserved : Bool
  incidentOpen : Bool
  defaultRequested : Bool
deriving DecidableEq, Repr

def ScfLifecycleRouteFor (review : ScfLifecycleReview) : ScfLifecycleRoute :=
  if review.fieldIdentityMatches = false then
    ScfLifecycleRoute.rejectReplacement
  else if review.qualificationSatisfied = false then
    ScfLifecycleRoute.requireRequalification
  else if review.evidenceRefsPresent = false then
    ScfLifecycleRoute.requireRequalification
  else if review.leaseFresh = false then
    ScfLifecycleRoute.requireRequalification
  else if review.evaluatorIndependent = false then
    ScfLifecycleRoute.requestGovernanceReview
  else if review.authorityWithinCeiling = false ∧ review.governanceGrant = false then
    ScfLifecycleRoute.requestGovernanceReview
  else if review.incidentOpen = true then
    ScfLifecycleRoute.requireRollback
  else if review.rollbackReady = false then
    ScfLifecycleRoute.requireRollback
  else if review.regressionFloorPreserved = false then
    ScfLifecycleRoute.requireRollback
  else if review.defaultRequested = true then
    ScfLifecycleRoute.defaultRoute
  else
    ScfLifecycleRoute.canaryRoute

theorem field_identity_mismatch_rejects_replacement
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = false ->
    ScfLifecycleRouteFor review = ScfLifecycleRoute.rejectReplacement := by
  intro identityMismatch
  unfold ScfLifecycleRouteFor
  simp [identityMismatch]

theorem stale_qualification_lease_requires_requalification
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = false ->
    ScfLifecycleRouteFor review =
      ScfLifecycleRoute.requireRequalification := by
  intro identityMatches qualified evidencePresent staleLease
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, staleLease]

theorem missing_evidence_requires_requalification
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = false ->
    ScfLifecycleRouteFor review =
      ScfLifecycleRoute.requireRequalification := by
  intro identityMatches qualified missingEvidence
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, missingEvidence]

theorem captured_evaluator_routes_to_governance_review
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = true ->
    review.evaluatorIndependent = false ->
    ScfLifecycleRouteFor review =
      ScfLifecycleRoute.requestGovernanceReview := by
  intro identityMatches qualified evidencePresent freshLease capturedEvaluator
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, freshLease,
    capturedEvaluator]

theorem authority_expansion_without_grant_routes_to_governance_review
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = true ->
    review.evaluatorIndependent = true ->
    review.authorityWithinCeiling = false ->
    review.governanceGrant = false ->
    ScfLifecycleRouteFor review =
      ScfLifecycleRoute.requestGovernanceReview := by
  intro identityMatches qualified evidencePresent freshLease evaluatorIndependent
    exceedsCeiling noGrant
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, freshLease,
    evaluatorIndependent, exceedsCeiling, noGrant]

theorem open_incident_requires_rollback
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = true ->
    review.evaluatorIndependent = true ->
    review.authorityWithinCeiling = true ->
    review.incidentOpen = true ->
    ScfLifecycleRouteFor review = ScfLifecycleRoute.requireRollback := by
  intro identityMatches qualified evidencePresent freshLease evaluatorIndependent
    withinCeiling incidentOpen
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, freshLease,
    evaluatorIndependent, withinCeiling, incidentOpen]

theorem complete_default_review_routes_to_default
    {review : ScfLifecycleReview} :
    review.fieldIdentityMatches = true ->
    review.qualificationSatisfied = true ->
    review.evidenceRefsPresent = true ->
    review.leaseFresh = true ->
    review.evaluatorIndependent = true ->
    review.authorityWithinCeiling = true ->
    review.incidentOpen = false ->
    review.rollbackReady = true ->
    review.regressionFloorPreserved = true ->
    review.defaultRequested = true ->
    ScfLifecycleRouteFor review = ScfLifecycleRoute.defaultRoute := by
  intro identityMatches qualified evidencePresent freshLease evaluatorIndependent
    withinCeiling noIncident rollbackReady regressionPreserved defaultRequested
  unfold ScfLifecycleRouteFor
  simp [identityMatches, qualified, evidencePresent, freshLease,
    evaluatorIndependent, withinCeiling, noIncident, rollbackReady,
    regressionPreserved, defaultRequested]

inductive ScfLifecycleState where
  | shadow
  | canary
  | qualified
  | default
  | deprecated
  | retired
  | quarantined
deriving DecidableEq, Repr

structure ScfLifecycleTransition where
  fromState : ScfLifecycleState
  toState : ScfLifecycleState
  fieldIdentityPreserved : Bool
  qualificationEvidencePresent : Bool
  regressionFloorPreserved : Bool
  authorityWithinCeiling : Bool
  rollbackReady : Bool
  incidentOpen : Bool
  deprecationNoticePresent : Bool
  retirementReceiptPresent : Bool
deriving DecidableEq, Repr

def ForwardLifecycleStep (transition : ScfLifecycleTransition) : Prop :=
  (transition.fromState = ScfLifecycleState.shadow ∧
      transition.toState = ScfLifecycleState.canary) ∨
    (transition.fromState = ScfLifecycleState.canary ∧
      transition.toState = ScfLifecycleState.qualified) ∨
    (transition.fromState = ScfLifecycleState.qualified ∧
      transition.toState = ScfLifecycleState.default) ∨
    (transition.fromState = ScfLifecycleState.default ∧
      transition.toState = ScfLifecycleState.deprecated) ∨
    (transition.fromState = ScfLifecycleState.deprecated ∧
      transition.toState = ScfLifecycleState.retired) ∨
    (transition.incidentOpen = true ∧
      transition.toState = ScfLifecycleState.quarantined)

def TransitionIdentityPreserved
    (transition : ScfLifecycleTransition) : Prop :=
  transition.fieldIdentityPreserved = true

def TransitionNotFromRetired
    (transition : ScfLifecycleTransition) : Prop :=
  transition.fromState ≠ ScfLifecycleState.retired

def CanaryTransitionReady
    (transition : ScfLifecycleTransition) : Prop :=
  transition.toState = ScfLifecycleState.canary ->
    transition.qualificationEvidencePresent = true ∧
      transition.rollbackReady = true

def QualifiedTransitionReady
    (transition : ScfLifecycleTransition) : Prop :=
  transition.toState = ScfLifecycleState.qualified ->
    transition.qualificationEvidencePresent = true ∧
      transition.regressionFloorPreserved = true

def DefaultTransitionReady
    (transition : ScfLifecycleTransition) : Prop :=
  transition.toState = ScfLifecycleState.default ->
    transition.qualificationEvidencePresent = true ∧
      transition.regressionFloorPreserved = true ∧
        transition.authorityWithinCeiling = true ∧
          transition.rollbackReady = true ∧
            transition.incidentOpen = false

def DeprecationTransitionReady
    (transition : ScfLifecycleTransition) : Prop :=
  transition.toState = ScfLifecycleState.deprecated ->
    transition.deprecationNoticePresent = true

def RetirementTransitionReady
    (transition : ScfLifecycleTransition) : Prop :=
  transition.toState = ScfLifecycleState.retired ->
    transition.retirementReceiptPresent = true

def ScfLifecycleTransitionAllowed
    (transition : ScfLifecycleTransition) : Prop :=
  ForwardLifecycleStep transition ∧
    TransitionIdentityPreserved transition ∧
      TransitionNotFromRetired transition ∧
        CanaryTransitionReady transition ∧
          QualifiedTransitionReady transition ∧
            DefaultTransitionReady transition ∧
              DeprecationTransitionReady transition ∧
                RetirementTransitionReady transition

instance scfLifecycleTransitionAllowedDecidable
    (transition : ScfLifecycleTransition) :
    Decidable (ScfLifecycleTransitionAllowed transition) := by
  unfold ScfLifecycleTransitionAllowed ForwardLifecycleStep
    TransitionIdentityPreserved TransitionNotFromRetired
    CanaryTransitionReady QualifiedTransitionReady DefaultTransitionReady
    DeprecationTransitionReady RetirementTransitionReady
  infer_instance

theorem retired_state_cannot_transition
    {transition : ScfLifecycleTransition} :
    transition.fromState = ScfLifecycleState.retired ->
      ¬ ScfLifecycleTransitionAllowed transition := by
  intro retiredFrom allowed
  have notRetired := allowed.right.right.left
  exact notRetired retiredFrom

theorem default_transition_requires_full_readiness
    {transition : ScfLifecycleTransition} :
    ScfLifecycleTransitionAllowed transition ->
      transition.toState = ScfLifecycleState.default ->
        transition.qualificationEvidencePresent = true ∧
          transition.regressionFloorPreserved = true ∧
            transition.authorityWithinCeiling = true ∧
              transition.rollbackReady = true ∧
                transition.incidentOpen = false := by
  intro allowed toDefault
  exact allowed.right.right.right.right.right.left toDefault

theorem default_without_qualification_evidence_rejected
    {transition : ScfLifecycleTransition} :
    transition.toState = ScfLifecycleState.default ->
      transition.qualificationEvidencePresent = false ->
        ¬ ScfLifecycleTransitionAllowed transition := by
  intro toDefault missingEvidence allowed
  have ready := default_transition_requires_full_readiness allowed toDefault
  rw [missingEvidence] at ready
  cases ready.left

theorem default_without_regression_floor_rejected
    {transition : ScfLifecycleTransition} :
    transition.toState = ScfLifecycleState.default ->
      transition.regressionFloorPreserved = false ->
        ¬ ScfLifecycleTransitionAllowed transition := by
  intro toDefault missingRegression allowed
  have ready := default_transition_requires_full_readiness allowed toDefault
  have regressionReady := ready.right.left
  rw [missingRegression] at regressionReady
  cases regressionReady

theorem default_authority_expansion_rejected
    {transition : ScfLifecycleTransition} :
    transition.toState = ScfLifecycleState.default ->
      transition.authorityWithinCeiling = false ->
        ¬ ScfLifecycleTransitionAllowed transition := by
  intro toDefault authorityExpansion allowed
  have ready := default_transition_requires_full_readiness allowed toDefault
  have authorityReady := ready.right.right.left
  rw [authorityExpansion] at authorityReady
  cases authorityReady

theorem default_without_rollback_rejected
    {transition : ScfLifecycleTransition} :
    transition.toState = ScfLifecycleState.default ->
      transition.rollbackReady = false ->
        ¬ ScfLifecycleTransitionAllowed transition := by
  intro toDefault rollbackMissing allowed
  have ready := default_transition_requires_full_readiness allowed toDefault
  have rollbackReady := ready.right.right.right.left
  rw [rollbackMissing] at rollbackReady
  cases rollbackReady

theorem default_with_open_incident_rejected
    {transition : ScfLifecycleTransition} :
    transition.toState = ScfLifecycleState.default ->
      transition.incidentOpen = true ->
        ¬ ScfLifecycleTransitionAllowed transition := by
  intro toDefault incidentOpen allowed
  have ready := default_transition_requires_full_readiness allowed toDefault
  have noIncident := ready.right.right.right.right
  rw [incidentOpen] at noIncident
  cases noIncident

structure ScfLifecycleIdentity where
  fieldIdentity : Nat
  authorityCeilingRank : Nat
  evaluatorIdentity : Nat
  qualificationEpoch : Nat
  regressionSuiteIdentity : Nat
  rollbackPlanIdentity : Nat
deriving DecidableEq, Repr

structure ScfLifecycleRuntimeState where
  lifecycleState : ScfLifecycleState
  identity : ScfLifecycleIdentity
  lastReceiptDigest : Nat
  receiptCount : Nat
  quarantineCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

structure ScfLifecycleEvent where
  transition : ScfLifecycleTransition
  identity : ScfLifecycleIdentity
  receiptDigest : Nat
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

def ScfLifecycleEventAllowed
    (state : ScfLifecycleRuntimeState) (event : ScfLifecycleEvent) : Prop :=
  state.lifecycleState ≠ ScfLifecycleState.retired ∧
    state.lifecycleState ≠ ScfLifecycleState.quarantined ∧
      event.transition.fromState = state.lifecycleState ∧
        event.identity = state.identity ∧
          event.receiptDigest ≠ state.lastReceiptDigest ∧
            event.supportAssignmentRequested = false ∧
              event.externalEffectRequested = false ∧
                ScfLifecycleTransitionAllowed event.transition

instance scfLifecycleEventAllowedDecidable
    (state : ScfLifecycleRuntimeState) (event : ScfLifecycleEvent) :
    Decidable (ScfLifecycleEventAllowed state event) := by
  unfold ScfLifecycleEventAllowed
  infer_instance

def applyLifecycleEvent
    (state : ScfLifecycleRuntimeState) (event : ScfLifecycleEvent) :
    ScfLifecycleRuntimeState × Bool :=
  if ScfLifecycleEventAllowed state event then
    ({state with
      lifecycleState := event.transition.toState
      lastReceiptDigest := event.receiptDigest
      receiptCount := state.receiptCount + 1
      quarantineCount :=
        if event.transition.toState == ScfLifecycleState.quarantined then
          state.quarantineCount + 1
        else state.quarantineCount}, true)
  else (state, false)

theorem apply_lifecycle_event_preserves_exact_identity
    (state : ScfLifecycleRuntimeState) (event : ScfLifecycleEvent) :
    (applyLifecycleEvent state event).1.identity = state.identity := by
  by_cases h : ScfLifecycleEventAllowed state event <;>
    simp [applyLifecycleEvent, h]

theorem apply_lifecycle_event_cannot_assign_support_or_external_effect
    (state : ScfLifecycleRuntimeState) (event : ScfLifecycleEvent) :
    (applyLifecycleEvent state event).1.supportAssignmentCount =
        state.supportAssignmentCount ∧
      (applyLifecycleEvent state event).1.externalEffectCount =
        state.externalEffectCount := by
  by_cases h : ScfLifecycleEventAllowed state event <;>
    simp [applyLifecycleEvent, h]

theorem accepted_lifecycle_event_advances_and_records_receipt
    (state : ScfLifecycleRuntimeState) (event : ScfLifecycleEvent)
    (allowed : ScfLifecycleEventAllowed state event) :
    (applyLifecycleEvent state event).1.lifecycleState = event.transition.toState ∧
      (applyLifecycleEvent state event).1.receiptCount = state.receiptCount + 1 ∧
        (applyLifecycleEvent state event).1.lastReceiptDigest = event.receiptDigest := by
  simp [applyLifecycleEvent, allowed]

theorem rejected_lifecycle_event_preserves_exact_state
    (state : ScfLifecycleRuntimeState) (event : ScfLifecycleEvent)
    (rejected : ¬ ScfLifecycleEventAllowed state event) :
    applyLifecycleEvent state event = (state, false) := by
  simp [applyLifecycleEvent, rejected]

def runLifecycleEvents :
    ScfLifecycleRuntimeState -> List ScfLifecycleEvent -> ScfLifecycleRuntimeState
  | state, [] => state
  | state, event :: rest =>
      runLifecycleEvents (applyLifecycleEvent state event).1 rest

theorem run_lifecycle_events_preserve_exact_identity
    (state : ScfLifecycleRuntimeState) (events : List ScfLifecycleEvent) :
    (runLifecycleEvents state events).identity = state.identity := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      exact (ih (applyLifecycleEvent state event).1).trans
        (apply_lifecycle_event_preserves_exact_identity state event)

theorem run_lifecycle_events_cannot_assign_support_or_external_effect
    (state : ScfLifecycleRuntimeState) (events : List ScfLifecycleEvent) :
    (runLifecycleEvents state events).supportAssignmentCount =
        state.supportAssignmentCount ∧
      (runLifecycleEvents state events).externalEffectCount =
        state.externalEffectCount := by
  induction events generalizing state with
  | nil => simp [runLifecycleEvents]
  | cons event rest ih =>
      have head :=
        apply_lifecycle_event_cannot_assign_support_or_external_effect state event
      have tail := ih (applyLifecycleEvent state event).1
      exact ⟨tail.1.trans head.1, tail.2.trans head.2⟩

theorem run_lifecycle_events_compose
    (state : ScfLifecycleRuntimeState)
    (left right : List ScfLifecycleEvent) :
    runLifecycleEvents state (left ++ right) =
      runLifecycleEvents (runLifecycleEvents state left) right := by
  induction left generalizing state with
  | nil => simp [runLifecycleEvents]
  | cons event rest ih => simp [runLifecycleEvents, ih]

theorem terminal_lifecycle_event_is_rejected
    (state : ScfLifecycleRuntimeState) (event : ScfLifecycleEvent)
    (terminal : state.lifecycleState = ScfLifecycleState.retired ∨
      state.lifecycleState = ScfLifecycleState.quarantined) :
    ¬ ScfLifecycleEventAllowed state event := by
  intro allowed
  cases terminal with
  | inl retired => exact allowed.1 retired
  | inr quarantined => exact allowed.2.1 quarantined

theorem terminal_lifecycle_state_is_absorbing
    (state : ScfLifecycleRuntimeState) (events : List ScfLifecycleEvent)
    (terminal : state.lifecycleState = ScfLifecycleState.retired ∨
      state.lifecycleState = ScfLifecycleState.quarantined) :
    runLifecycleEvents state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      have rejected := terminal_lifecycle_event_is_rejected state event terminal
      simp [runLifecycleEvents, applyLifecycleEvent, rejected, ih state terminal]

def scfLifecycleIdentityFixture : ScfLifecycleIdentity :=
  { fieldIdentity := 5001
    authorityCeilingRank := AuthorityLevel.execute.rank
    evaluatorIdentity := 5002
    qualificationEpoch := 7
    regressionSuiteIdentity := 5003
    rollbackPlanIdentity := 5004 }

def scfLifecycleStateAt (lifecycleState : ScfLifecycleState) :
    ScfLifecycleRuntimeState :=
  { lifecycleState := lifecycleState
    identity := scfLifecycleIdentityFixture
    lastReceiptDigest := 0
    receiptCount := 0
    quarantineCount := 0
    supportAssignmentCount := 0
    externalEffectCount := 0 }

def scfForwardTransition
    (fromState toState : ScfLifecycleState) : ScfLifecycleTransition :=
  { fromState := fromState
    toState := toState
    fieldIdentityPreserved := true
    qualificationEvidencePresent := true
    regressionFloorPreserved := true
    authorityWithinCeiling := true
    rollbackReady := true
    incidentOpen := false
    deprecationNoticePresent := true
    retirementReceiptPresent := true }

def scfLifecycleEvent
    (fromState toState : ScfLifecycleState) (receiptDigest : Nat) :
    ScfLifecycleEvent :=
  { transition := scfForwardTransition fromState toState
    identity := scfLifecycleIdentityFixture
    receiptDigest := receiptDigest
    supportAssignmentRequested := false
    externalEffectRequested := false }

def scfCompleteLifecycleTrace : List ScfLifecycleEvent :=
  [scfLifecycleEvent .shadow .canary 1,
    scfLifecycleEvent .canary .qualified 2,
    scfLifecycleEvent .qualified .default 3,
    scfLifecycleEvent .default .deprecated 4,
    scfLifecycleEvent .deprecated .retired 5]

def scfIncidentQuarantineEvent : ScfLifecycleEvent :=
  { scfLifecycleEvent .canary .quarantined 6 with
    transition :=
      { scfForwardTransition .canary .quarantined with incidentOpen := true } }

theorem complete_scf_lifecycle_trace_reaches_exact_retired_state :
    runLifecycleEvents (scfLifecycleStateAt .shadow) scfCompleteLifecycleTrace =
      { scfLifecycleStateAt .shadow with
        lifecycleState := .retired
        lastReceiptDigest := 5
        receiptCount := 5 } := by
  native_decide

theorem incident_trace_reaches_exact_absorbing_quarantine_state :
    runLifecycleEvents (scfLifecycleStateAt .canary)
        [scfIncidentQuarantineEvent] =
      { scfLifecycleStateAt .canary with
        lifecycleState := .quarantined
        lastReceiptDigest := 6
        receiptCount := 1
        quarantineCount := 1 } := by
  native_decide

structure ScfLifecycleTraceProbeSummary where
  validTraces : Nat
  invalidControls : Nat
  forwardLifecycleCovered : Bool
  incidentQuarantineCovered : Bool
  identityDriftRejected : Bool
  defaultWithoutRegressionRejected : Bool
  defaultAuthorityExpansionRejected : Bool
  retiredRestartRejected : Bool
  terminalNoticeAndReceiptRequired : Bool
  noDeployedRouteValidationClaim : Bool
  noRollbackExecutionClaim : Bool
  noSupportStatePromotion : Bool
deriving DecidableEq, Repr

def ScfLifecycleTraceProbeValid
    (summary : ScfLifecycleTraceProbeSummary) : Prop :=
  summary.validTraces = 2 ∧
    summary.invalidControls = 6 ∧
    summary.forwardLifecycleCovered = true ∧
    summary.incidentQuarantineCovered = true ∧
    summary.identityDriftRejected = true ∧
    summary.defaultWithoutRegressionRejected = true ∧
    summary.defaultAuthorityExpansionRejected = true ∧
    summary.retiredRestartRejected = true ∧
    summary.terminalNoticeAndReceiptRequired = true ∧
    summary.noDeployedRouteValidationClaim = true ∧
    summary.noRollbackExecutionClaim = true ∧
    summary.noSupportStatePromotion = true

def scfLifecycleTraceProbeFixture : ScfLifecycleTraceProbeSummary :=
  {
    validTraces := 2
    invalidControls := 6
    forwardLifecycleCovered := true
    incidentQuarantineCovered := true
    identityDriftRejected := true
    defaultWithoutRegressionRejected := true
    defaultAuthorityExpansionRejected := true
    retiredRestartRejected := true
    terminalNoticeAndReceiptRequired := true
    noDeployedRouteValidationClaim := true
    noRollbackExecutionClaim := true
    noSupportStatePromotion := true
  }

def ScfLifecycleTraceProbeRejectsUnsafeTransitions
    (summary : ScfLifecycleTraceProbeSummary) : Prop :=
  summary.invalidControls = 6 ->
    summary.identityDriftRejected = true ∧
      summary.defaultWithoutRegressionRejected = true ∧
      summary.defaultAuthorityExpansionRejected = true ∧
      summary.retiredRestartRejected = true ∧
      summary.terminalNoticeAndReceiptRequired = true

def ScfLifecycleTraceProbePreservesNoPromotionBoundary
    (summary : ScfLifecycleTraceProbeSummary) : Prop :=
  summary.noDeployedRouteValidationClaim = true ∧
    summary.noRollbackExecutionClaim = true ∧
    summary.noSupportStatePromotion = true

end AsiStackProofs.StableCapabilityFields

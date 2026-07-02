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

theorem replacement_requires_field_qualification
    {field : StableCapabilityField} {candidate : ImplementationCandidate} :
    ReplacementAllowed field candidate ->
    candidate.satisfiesQualification = true := by
  intro allowed
  exact allowed.1

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

theorem allowed_transition_preserves_field_identity
    {transition : ScfLifecycleTransition} :
    ScfLifecycleTransitionAllowed transition ->
      transition.fieldIdentityPreserved = true := by
  intro allowed
  exact allowed.right.left

theorem allowed_transition_must_be_forward_or_quarantine
    {transition : ScfLifecycleTransition} :
    ScfLifecycleTransitionAllowed transition ->
      ForwardLifecycleStep transition := by
  intro allowed
  exact allowed.left

theorem retired_state_cannot_transition
    {transition : ScfLifecycleTransition} :
    transition.fromState = ScfLifecycleState.retired ->
      ¬ ScfLifecycleTransitionAllowed transition := by
  intro retiredFrom allowed
  have notRetired := allowed.right.right.left
  exact notRetired retiredFrom

theorem canary_transition_requires_evidence_and_rollback
    {transition : ScfLifecycleTransition} :
    ScfLifecycleTransitionAllowed transition ->
      transition.toState = ScfLifecycleState.canary ->
        transition.qualificationEvidencePresent = true ∧
          transition.rollbackReady = true := by
  intro allowed toCanary
  exact allowed.right.right.right.left toCanary

theorem qualified_transition_requires_evidence_and_regression_floor
    {transition : ScfLifecycleTransition} :
    ScfLifecycleTransitionAllowed transition ->
      transition.toState = ScfLifecycleState.qualified ->
        transition.qualificationEvidencePresent = true ∧
          transition.regressionFloorPreserved = true := by
  intro allowed toQualified
  exact allowed.right.right.right.right.left toQualified

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

theorem deprecated_transition_requires_notice
    {transition : ScfLifecycleTransition} :
    ScfLifecycleTransitionAllowed transition ->
      transition.toState = ScfLifecycleState.deprecated ->
        transition.deprecationNoticePresent = true := by
  intro allowed toDeprecated
  exact allowed.right.right.right.right.right.right.left toDeprecated

theorem retirement_transition_requires_receipt
    {transition : ScfLifecycleTransition} :
    ScfLifecycleTransitionAllowed transition ->
      transition.toState = ScfLifecycleState.retired ->
        transition.retirementReceiptPresent = true := by
  intro allowed toRetired
  exact allowed.right.right.right.right.right.right.right toRetired

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

theorem scf_lifecycle_trace_probe_fixture_valid :
    ScfLifecycleTraceProbeValid scfLifecycleTraceProbeFixture := by
  unfold ScfLifecycleTraceProbeValid scfLifecycleTraceProbeFixture
  simp

def ScfLifecycleTraceProbeRejectsUnsafeTransitions
    (summary : ScfLifecycleTraceProbeSummary) : Prop :=
  summary.invalidControls = 6 ->
    summary.identityDriftRejected = true ∧
      summary.defaultWithoutRegressionRejected = true ∧
      summary.defaultAuthorityExpansionRejected = true ∧
      summary.retiredRestartRejected = true ∧
      summary.terminalNoticeAndReceiptRequired = true

theorem scf_lifecycle_trace_probe_rejects_unsafe_transitions :
    ScfLifecycleTraceProbeRejectsUnsafeTransitions
      scfLifecycleTraceProbeFixture := by
  unfold ScfLifecycleTraceProbeRejectsUnsafeTransitions
    scfLifecycleTraceProbeFixture
  intro _
  simp

def ScfLifecycleTraceProbePreservesNoPromotionBoundary
    (summary : ScfLifecycleTraceProbeSummary) : Prop :=
  summary.noDeployedRouteValidationClaim = true ∧
    summary.noRollbackExecutionClaim = true ∧
    summary.noSupportStatePromotion = true

theorem scf_lifecycle_trace_probe_preserves_no_promotion_boundary :
    ScfLifecycleTraceProbePreservesNoPromotionBoundary
      scfLifecycleTraceProbeFixture := by
  unfold ScfLifecycleTraceProbePreservesNoPromotionBoundary
    scfLifecycleTraceProbeFixture
  simp

end AsiStackProofs.StableCapabilityFields

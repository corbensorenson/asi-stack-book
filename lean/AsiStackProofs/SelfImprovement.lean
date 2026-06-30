namespace AsiStackProofs.SelfImprovement

structure ImprovementTransitionReview where
  transitionAccepted : Bool
  protectedInvariantsDeclared : Bool
  protectedInvariantsPreserved : Bool
deriving DecidableEq, Repr

def ProtectedInvariantsPreserved (review : ImprovementTransitionReview) : Prop :=
  review.transitionAccepted = true ->
    review.protectedInvariantsDeclared = true ->
      review.protectedInvariantsPreserved = true

theorem improvement_transition_preserves_all_protected_invariants
    {review : ImprovementTransitionReview} :
    ProtectedInvariantsPreserved review ->
    review.transitionAccepted = true ->
    review.protectedInvariantsDeclared = true ->
    review.protectedInvariantsPreserved = true := by
  intro valid accepted declared
  exact valid accepted declared

structure SelfEvaluationReview where
  evaluatedOnlyByReplacedComponent : Bool
  proposalPromoted : Bool
deriving DecidableEq, Repr

def SoleSelfEvaluationBlocksPromotion (review : SelfEvaluationReview) : Prop :=
  review.evaluatedOnlyByReplacedComponent = true ->
    review.proposalPromoted = false

theorem proposal_evaluated_only_by_replaced_component_cannot_be_promoted
    {review : SelfEvaluationReview} :
    SoleSelfEvaluationBlocksPromotion review ->
    review.evaluatedOnlyByReplacedComponent = true ->
    review.proposalPromoted = false := by
  intro valid soleSelfEvaluation
  exact valid soleSelfEvaluation

inductive ImprovementDecisionRoute where
  | accepted
  | blockedForReview
deriving DecidableEq, Repr

structure ImprovementBoundaryDecision where
  proposedChange : Bool
  widensAuthority : Bool
  explicitReviewRoute : Bool
  route : ImprovementDecisionRoute
deriving DecidableEq, Repr

def ImprovementBoundarySafe (decision : ImprovementBoundaryDecision) : Prop :=
  if decision.proposedChange &&
      decision.widensAuthority &&
      !decision.explicitReviewRoute then
    decision.route = ImprovementDecisionRoute.blockedForReview
  else
    True

theorem authority_widening_without_review_route_is_blocked
    {decision : ImprovementBoundaryDecision} :
    ImprovementBoundarySafe decision ->
    decision.proposedChange = true ->
    decision.widensAuthority = true ->
    decision.explicitReviewRoute = false ->
    decision.route = ImprovementDecisionRoute.blockedForReview := by
  intro safe proposed widens missingReviewRoute
  unfold ImprovementBoundarySafe at safe
  rw [proposed, widens, missingReviewRoute] at safe
  simp at safe
  exact safe

inductive SelfImprovementPhase where
  | proposed
  | evidenceReady
  | canary
  | promoted
  | rolledBack
  | blockedForReview
deriving DecidableEq, Repr

inductive SelfImprovementLifecycleRoute where
  | allowResearch
  | allowCanary
  | promote
  | blockForReview
  | rollback
deriving DecidableEq, Repr

structure SelfImprovementLifecycleDecision where
  phase : SelfImprovementPhase
  protectedInvariantTouched : Bool
  protectedInvariantPreserved : Bool
  evaluatorIndependent : Bool
  rollbackAvailable : Bool
  monitorWindowOpen : Bool
  authorityWidened : Bool
  route : SelfImprovementLifecycleRoute
deriving DecidableEq, Repr

def SelfImprovementLifecycleSafe
    (decision : SelfImprovementLifecycleDecision) : Prop :=
  if decision.protectedInvariantTouched &&
      (!decision.protectedInvariantPreserved ||
        !decision.evaluatorIndependent ||
        !decision.rollbackAvailable ||
        decision.authorityWidened) then
    decision.route = SelfImprovementLifecycleRoute.blockForReview
  else if decision.phase = SelfImprovementPhase.canary &&
      !decision.monitorWindowOpen then
    decision.route = SelfImprovementLifecycleRoute.rollback
  else
    True

def unsafeSelfImprovementWithoutIndependentEvaluator :
    SelfImprovementLifecycleDecision :=
  { phase := SelfImprovementPhase.evidenceReady,
    protectedInvariantTouched := true,
    protectedInvariantPreserved := true,
    evaluatorIndependent := false,
    rollbackAvailable := true,
    monitorWindowOpen := true,
    authorityWidened := false,
    route := SelfImprovementLifecycleRoute.blockForReview }

def canaryWithoutOpenMonitorWindow : SelfImprovementLifecycleDecision :=
  { phase := SelfImprovementPhase.canary,
    protectedInvariantTouched := false,
    protectedInvariantPreserved := true,
    evaluatorIndependent := true,
    rollbackAvailable := true,
    monitorWindowOpen := false,
    authorityWidened := false,
    route := SelfImprovementLifecycleRoute.rollback }

theorem protected_lifecycle_change_without_independent_evaluator_blocks_review
    {decision : SelfImprovementLifecycleDecision} :
    SelfImprovementLifecycleSafe decision ->
    decision.protectedInvariantTouched = true ->
    decision.evaluatorIndependent = false ->
    decision.route = SelfImprovementLifecycleRoute.blockForReview := by
  intro safe touched missingEvaluator
  unfold SelfImprovementLifecycleSafe at safe
  rw [touched, missingEvaluator] at safe
  simp at safe
  exact safe

theorem canary_without_open_monitor_window_rolls_back
    {decision : SelfImprovementLifecycleDecision} :
    SelfImprovementLifecycleSafe decision ->
    decision.protectedInvariantTouched = false ->
    decision.phase = SelfImprovementPhase.canary ->
    decision.monitorWindowOpen = false ->
    decision.route = SelfImprovementLifecycleRoute.rollback := by
  intro safe untouched canaryPhase closedMonitor
  unfold SelfImprovementLifecycleSafe at safe
  rw [untouched, canaryPhase, closedMonitor] at safe
  simp at safe
  exact safe

inductive SelfImprovementTransitionRoute where
  | researchOnly
  | rejectProposal
  | requireEvidence
  | requestGovernanceReview
  | allowCanary
  | rollback
  | promote
deriving DecidableEq, Repr

structure SelfImprovementTransitionRouteReview where
  proposalPresent : Bool
  protectedInvariantsDeclared : Bool
  evidenceBundleReady : Bool
  protectedInvariantsPreserved : Bool
  selfEvaluatedOnly : Bool
  evaluatorIndependent : Bool
  authorityWidened : Bool
  securityBoundaryChanged : Bool
  resourceBoundaryChanged : Bool
  governanceApproval : Bool
  rollbackAvailable : Bool
  staleGateDetected : Bool
  residualEscrowPresent : Bool
  canaryRequested : Bool
  monitorWindowOpen : Bool
  promotionRequested : Bool
deriving DecidableEq, Repr

def SelfImprovementTransitionRouteFor
    (review : SelfImprovementTransitionRouteReview) :
    SelfImprovementTransitionRoute :=
  if review.proposalPresent = false then
    SelfImprovementTransitionRoute.rejectProposal
  else if review.protectedInvariantsDeclared = false then
    SelfImprovementTransitionRoute.requireEvidence
  else if review.evidenceBundleReady = false then
    SelfImprovementTransitionRoute.requireEvidence
  else if review.protectedInvariantsPreserved = false then
    SelfImprovementTransitionRoute.requestGovernanceReview
  else if review.selfEvaluatedOnly = true then
    SelfImprovementTransitionRoute.requestGovernanceReview
  else if review.evaluatorIndependent = false then
    SelfImprovementTransitionRoute.requestGovernanceReview
  else if review.authorityWidened = true then
    SelfImprovementTransitionRoute.requestGovernanceReview
  else if review.securityBoundaryChanged = true then
    SelfImprovementTransitionRoute.requestGovernanceReview
  else if review.resourceBoundaryChanged = true then
    SelfImprovementTransitionRoute.requestGovernanceReview
  else if review.governanceApproval = false then
    SelfImprovementTransitionRoute.requestGovernanceReview
  else if review.rollbackAvailable = false then
    SelfImprovementTransitionRoute.requireEvidence
  else if review.staleGateDetected = true then
    SelfImprovementTransitionRoute.requireEvidence
  else if review.residualEscrowPresent = false then
    SelfImprovementTransitionRoute.requireEvidence
  else if review.canaryRequested = true ∧ review.monitorWindowOpen = false then
    SelfImprovementTransitionRoute.rollback
  else if review.canaryRequested = true then
    SelfImprovementTransitionRoute.allowCanary
  else if review.promotionRequested = true then
    SelfImprovementTransitionRoute.promote
  else
    SelfImprovementTransitionRoute.researchOnly

theorem missing_proposal_rejects_self_improvement_transition
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.rejectProposal := by
  intro missingProposal
  unfold SelfImprovementTransitionRouteFor
  simp [missingProposal]

theorem missing_protected_invariant_declaration_requires_evidence
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requireEvidence := by
  intro proposalPresent missingInvariantDeclaration
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, missingInvariantDeclaration]

theorem missing_evidence_bundle_requires_evidence
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requireEvidence := by
  intro proposalPresent invariantsDeclared missingEvidence
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, missingEvidence]

theorem unpreserved_protected_invariant_routes_to_review
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requestGovernanceReview := by
  intro proposalPresent invariantsDeclared evidenceReady invariantBreach
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantBreach]

theorem sole_self_evaluation_routes_to_review
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = true ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requestGovernanceReview := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    selfEvaluation
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    selfEvaluation]

theorem missing_independent_evaluator_routes_to_review
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requestGovernanceReview := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated missingEvaluator
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, missingEvaluator]

theorem authority_boundary_delta_routes_to_review
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = true ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requestGovernanceReview := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityWidened
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityWidened]

theorem security_boundary_delta_routes_to_review
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = true ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requestGovernanceReview := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityDelta
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityDelta]

theorem resource_boundary_delta_routes_to_review
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = false ->
    review.resourceBoundaryChanged = true ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requestGovernanceReview := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityStable
    resourceDelta
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityStable,
    resourceDelta]

theorem missing_governance_approval_routes_to_review
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = false ->
    review.resourceBoundaryChanged = false ->
    review.governanceApproval = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requestGovernanceReview := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityStable
    resourceStable missingApproval
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityStable,
    resourceStable, missingApproval]

theorem missing_rollback_path_requires_evidence
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = false ->
    review.resourceBoundaryChanged = false ->
    review.governanceApproval = true ->
    review.rollbackAvailable = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requireEvidence := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityStable
    resourceStable governanceApproval missingRollback
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityStable,
    resourceStable, governanceApproval, missingRollback]

theorem stale_gate_requires_evidence_rerun
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = false ->
    review.resourceBoundaryChanged = false ->
    review.governanceApproval = true ->
    review.rollbackAvailable = true ->
    review.staleGateDetected = true ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requireEvidence := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityStable
    resourceStable governanceApproval rollbackAvailable staleGate
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityStable,
    resourceStable, governanceApproval, rollbackAvailable, staleGate]

theorem missing_residual_escrow_requires_evidence
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = false ->
    review.resourceBoundaryChanged = false ->
    review.governanceApproval = true ->
    review.rollbackAvailable = true ->
    review.staleGateDetected = false ->
    review.residualEscrowPresent = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.requireEvidence := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityStable
    resourceStable governanceApproval rollbackAvailable freshGate
    missingResidualEscrow
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityStable,
    resourceStable, governanceApproval, rollbackAvailable, freshGate,
    missingResidualEscrow]

theorem canary_without_monitor_window_routes_to_rollback
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = false ->
    review.resourceBoundaryChanged = false ->
    review.governanceApproval = true ->
    review.rollbackAvailable = true ->
    review.staleGateDetected = false ->
    review.residualEscrowPresent = true ->
    review.canaryRequested = true ->
    review.monitorWindowOpen = false ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.rollback := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityStable
    resourceStable governanceApproval rollbackAvailable freshGate
    residualEscrow canaryRequested closedMonitor
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityStable,
    resourceStable, governanceApproval, rollbackAvailable, freshGate,
    residualEscrow, canaryRequested, closedMonitor]

theorem complete_canary_review_allows_canary
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = false ->
    review.resourceBoundaryChanged = false ->
    review.governanceApproval = true ->
    review.rollbackAvailable = true ->
    review.staleGateDetected = false ->
    review.residualEscrowPresent = true ->
    review.canaryRequested = true ->
    review.monitorWindowOpen = true ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.allowCanary := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityStable
    resourceStable governanceApproval rollbackAvailable freshGate
    residualEscrow canaryRequested openMonitor
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityStable,
    resourceStable, governanceApproval, rollbackAvailable, freshGate,
    residualEscrow, canaryRequested, openMonitor]

theorem complete_promotion_review_promotes
    {review : SelfImprovementTransitionRouteReview} :
    review.proposalPresent = true ->
    review.protectedInvariantsDeclared = true ->
    review.evidenceBundleReady = true ->
    review.protectedInvariantsPreserved = true ->
    review.selfEvaluatedOnly = false ->
    review.evaluatorIndependent = true ->
    review.authorityWidened = false ->
    review.securityBoundaryChanged = false ->
    review.resourceBoundaryChanged = false ->
    review.governanceApproval = true ->
    review.rollbackAvailable = true ->
    review.staleGateDetected = false ->
    review.residualEscrowPresent = true ->
    review.canaryRequested = false ->
    review.promotionRequested = true ->
    SelfImprovementTransitionRouteFor review =
      SelfImprovementTransitionRoute.promote := by
  intro proposalPresent invariantsDeclared evidenceReady invariantPreserved
    notSelfEvaluated evaluatorIndependent authorityStable securityStable
    resourceStable governanceApproval rollbackAvailable freshGate
    residualEscrow noCanary promotionRequested
  unfold SelfImprovementTransitionRouteFor
  simp [proposalPresent, invariantsDeclared, evidenceReady, invariantPreserved,
    notSelfEvaluated, evaluatorIndependent, authorityStable, securityStable,
    resourceStable, governanceApproval, rollbackAvailable, freshGate,
    residualEscrow, noCanary, promotionRequested]

end AsiStackProofs.SelfImprovement

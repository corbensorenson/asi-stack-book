namespace AsiStackProofs.GovernanceRights

structure GovernanceTransitionReview where
  transitionAccepted : Bool
  auditCapabilityRequired : Bool
  exitCapabilityRequired : Bool
  auditCapabilityPreserved : Bool
  exitCapabilityPreserved : Bool
deriving DecidableEq, Repr

def RequiredAuditAndExitPreserved (review : GovernanceTransitionReview) : Prop :=
  (review.transitionAccepted = true ->
    review.auditCapabilityRequired = true ->
      review.auditCapabilityPreserved = true) ∧
        (review.transitionAccepted = true ->
          review.exitCapabilityRequired = true ->
            review.exitCapabilityPreserved = true)

theorem governance_transition_preserves_required_audit_and_exit_capabilities
    {review : GovernanceTransitionReview} :
    RequiredAuditAndExitPreserved review ->
    review.transitionAccepted = true ->
    review.auditCapabilityRequired = true ->
    review.exitCapabilityRequired = true ->
    review.auditCapabilityPreserved = true ∧
      review.exitCapabilityPreserved = true := by
  intro valid accepted auditRequired exitRequired
  exact ⟨valid.1 accepted auditRequired, valid.2 accepted exitRequired⟩

structure ProtectedRightRemovalReview where
  protectedRight : Bool
  rightRemoved : Bool
  rejectedOrMarkedInvalid : Bool
deriving DecidableEq, Repr

def ProtectedRightRemovalInvalid
    (review : ProtectedRightRemovalReview) : Prop :=
  review.protectedRight = true ->
    review.rightRemoved = true ->
      review.rejectedOrMarkedInvalid = true

theorem transition_removing_protected_right_is_rejected_or_invalid
    {review : ProtectedRightRemovalReview} :
    ProtectedRightRemovalInvalid review ->
    review.protectedRight = true ->
    review.rightRemoved = true ->
    review.rejectedOrMarkedInvalid = true := by
  intro valid rightProtected removed
  exact valid rightProtected removed

inductive ForkDecisionRoute where
  | allowed
  | blockedForReview
deriving DecidableEq, Repr

structure ForkGovernanceDecision where
  constrainedFork : Bool
  auditPathPreserved : Bool
  safetyObligationsPreserved : Bool
  route : ForkDecisionRoute
deriving DecidableEq, Repr

def ForkGovernanceSafe (decision : ForkGovernanceDecision) : Prop :=
  if decision.constrainedFork &&
      (!decision.auditPathPreserved || !decision.safetyObligationsPreserved) then
    decision.route = ForkDecisionRoute.blockedForReview
  else
    True

theorem constrained_fork_without_audit_path_routes_to_review
    {decision : ForkGovernanceDecision} :
    ForkGovernanceSafe decision ->
    decision.constrainedFork = true ->
    decision.auditPathPreserved = false ->
    decision.route = ForkDecisionRoute.blockedForReview := by
  intro safe constrained missingAudit
  unfold ForkGovernanceSafe at safe
  rw [constrained, missingAudit] at safe
  simp at safe
  exact safe

inductive GovernanceRightsPhase where
  | requested
  | redacted
  | forkReview
  | exitReview
  | preserved
  | blockedForReview
  | residualized
deriving DecidableEq, Repr

inductive GovernanceRightsRoute where
  | allow
  | blockForReview
  | preserveExitResidual
deriving DecidableEq, Repr

structure GovernanceRightsDecision where
  phase : GovernanceRightsPhase
  constrainedFork : Bool
  auditPathPreserved : Bool
  safetyObligationsPreserved : Bool
  redactionApplied : Bool
  redactionReasonRecorded : Bool
  appealAvailable : Bool
  exitRequired : Bool
  exitCapabilityPreserved : Bool
  protectedRightRemoved : Bool
  route : GovernanceRightsRoute
deriving DecidableEq, Repr

def GovernanceRightsRequiresReview
    (decision : GovernanceRightsDecision) : Bool :=
  (decision.constrainedFork &&
    (!decision.auditPathPreserved || !decision.safetyObligationsPreserved)) ||
      (decision.redactionApplied &&
        (!decision.redactionReasonRecorded || !decision.appealAvailable)) ||
      decision.protectedRightRemoved

def GovernanceRightsSafe (decision : GovernanceRightsDecision) : Prop :=
  if GovernanceRightsRequiresReview decision then
    decision.route = GovernanceRightsRoute.blockForReview
  else if decision.exitRequired && !decision.exitCapabilityPreserved then
    decision.route = GovernanceRightsRoute.preserveExitResidual
  else
    True

def unsafeForkWithoutSafetyObligations :
    GovernanceRightsDecision :=
  { phase := GovernanceRightsPhase.forkReview,
    constrainedFork := true,
    auditPathPreserved := true,
    safetyObligationsPreserved := false,
    redactionApplied := false,
    redactionReasonRecorded := true,
    appealAvailable := true,
    exitRequired := false,
    exitCapabilityPreserved := true,
    protectedRightRemoved := false,
    route := GovernanceRightsRoute.blockForReview }

def redactionWithoutAppealPath :
    GovernanceRightsDecision :=
  { phase := GovernanceRightsPhase.redacted,
    constrainedFork := false,
    auditPathPreserved := true,
    safetyObligationsPreserved := true,
    redactionApplied := true,
    redactionReasonRecorded := true,
    appealAvailable := false,
    exitRequired := false,
    exitCapabilityPreserved := true,
    protectedRightRemoved := false,
    route := GovernanceRightsRoute.blockForReview }

def missingExitCapabilityResidualized :
    GovernanceRightsDecision :=
  { phase := GovernanceRightsPhase.residualized,
    constrainedFork := false,
    auditPathPreserved := true,
    safetyObligationsPreserved := true,
    redactionApplied := false,
    redactionReasonRecorded := true,
    appealAvailable := true,
    exitRequired := true,
    exitCapabilityPreserved := false,
    protectedRightRemoved := false,
    route := GovernanceRightsRoute.preserveExitResidual }

theorem constrained_fork_without_safety_obligations_routes_to_review
    {decision : GovernanceRightsDecision} :
    GovernanceRightsSafe decision ->
    decision.constrainedFork = true ->
    decision.safetyObligationsPreserved = false ->
    decision.route = GovernanceRightsRoute.blockForReview := by
  intro safe constrained missingSafety
  unfold GovernanceRightsSafe GovernanceRightsRequiresReview at safe
  rw [constrained, missingSafety] at safe
  simp at safe
  exact safe

theorem redaction_without_appeal_path_routes_to_review
    {decision : GovernanceRightsDecision} :
    GovernanceRightsSafe decision ->
    decision.redactionApplied = true ->
    decision.appealAvailable = false ->
    decision.route = GovernanceRightsRoute.blockForReview := by
  intro safe redacted missingAppeal
  unfold GovernanceRightsSafe GovernanceRightsRequiresReview at safe
  rw [redacted, missingAppeal] at safe
  simp at safe
  exact safe

theorem missing_exit_capability_preserves_exit_residual
    {decision : GovernanceRightsDecision} :
    GovernanceRightsSafe decision ->
    GovernanceRightsRequiresReview decision = false ->
    decision.exitRequired = true ->
    decision.exitCapabilityPreserved = false ->
    decision.route = GovernanceRightsRoute.preserveExitResidual := by
  intro safe noReviewRequired exitRequired missingExit
  unfold GovernanceRightsSafe at safe
  rw [noReviewRequired, exitRequired, missingExit] at safe
  simp at safe
  exact safe

end AsiStackProofs.GovernanceRights

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

end AsiStackProofs.GovernanceRights

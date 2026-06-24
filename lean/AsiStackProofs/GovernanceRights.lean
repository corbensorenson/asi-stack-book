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

end AsiStackProofs.GovernanceRights

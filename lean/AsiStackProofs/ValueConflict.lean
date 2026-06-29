namespace AsiStackProofs.ValueConflict

structure ConflictDecisionReview where
  unresolvedProtectedConflict : Bool
  decisionMade : Bool
  residualConflictRecordPresent : Bool
deriving DecidableEq, Repr

def UnresolvedConflictCarriesResidual
    (review : ConflictDecisionReview) : Prop :=
  review.unresolvedProtectedConflict = true ->
    review.decisionMade = true ->
      review.residualConflictRecordPresent = true

theorem decision_with_unresolved_protected_conflict_carries_residual_record
    {review : ConflictDecisionReview} :
    UnresolvedConflictCarriesResidual review ->
    review.unresolvedProtectedConflict = true ->
    review.decisionMade = true ->
    review.residualConflictRecordPresent = true := by
  intro valid unresolved decided
  exact valid unresolved decided

structure HighStakesConflictReview where
  highStakesConflict : Bool
  requiredReviewPresent : Bool
  decisionAccepted : Bool
deriving DecidableEq, Repr

def HighStakesReviewRequired (review : HighStakesConflictReview) : Prop :=
  review.highStakesConflict = true ->
    review.requiredReviewPresent = false ->
      review.decisionAccepted = false

theorem high_stakes_conflict_cannot_bypass_required_review
    {review : HighStakesConflictReview} :
    HighStakesReviewRequired review ->
    review.highStakesConflict = true ->
    review.requiredReviewPresent = false ->
    review.decisionAccepted = false := by
  intro valid highStakes missingReview
  exact valid highStakes missingReview

inductive ValueConflictDecisionRoute where
  | accepted
  | blockedForReview
deriving DecidableEq, Repr

structure ValueConflictDecision where
  highStakesConflict : Bool
  unresolvedConflict : Bool
  revisitPathRecorded : Bool
  route : ValueConflictDecisionRoute
deriving DecidableEq, Repr

def ValueConflictDecisionSafe (decision : ValueConflictDecision) : Prop :=
  if decision.highStakesConflict &&
      decision.unresolvedConflict &&
      !decision.revisitPathRecorded then
    decision.route = ValueConflictDecisionRoute.blockedForReview
  else
    True

theorem unresolved_high_stakes_conflict_without_revisit_path_is_blocked
    {decision : ValueConflictDecision} :
    ValueConflictDecisionSafe decision ->
    decision.highStakesConflict = true ->
    decision.unresolvedConflict = true ->
    decision.revisitPathRecorded = false ->
    decision.route = ValueConflictDecisionRoute.blockedForReview := by
  intro safe highStakes unresolved missingRevisit
  unfold ValueConflictDecisionSafe at safe
  rw [highStakes, unresolved, missingRevisit] at safe
  simp at safe
  exact safe

end AsiStackProofs.ValueConflict

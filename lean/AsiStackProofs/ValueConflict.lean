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

end AsiStackProofs.ValueConflict

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

end AsiStackProofs.SelfImprovement

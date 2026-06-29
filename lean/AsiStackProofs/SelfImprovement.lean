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

end AsiStackProofs.SelfImprovement

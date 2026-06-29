namespace AsiStackProofs.Alignment

structure ConstitutionalPredicateReview where
  activePredicate : Bool
  planAdmitted : Bool
  planSatisfiesPredicate : Bool
deriving DecidableEq, Repr

def AdmittedPlanSatisfiesActivePredicate
    (review : ConstitutionalPredicateReview) : Prop :=
  review.activePredicate = true ->
    review.planAdmitted = true ->
      review.planSatisfiesPredicate = true

theorem admitted_plan_satisfies_every_active_constitutional_predicate
    {review : ConstitutionalPredicateReview} :
    AdmittedPlanSatisfiesActivePredicate review ->
    review.activePredicate = true ->
    review.planAdmitted = true ->
    review.planSatisfiesPredicate = true := by
  intro valid active admitted
  exact valid active admitted

structure SelfModificationPredicateReview where
  protectedPredicate : Bool
  weakensPredicate : Bool
  modificationRejected : Bool
deriving DecidableEq, Repr

def ProtectedPredicateWeakeningRejected
    (review : SelfModificationPredicateReview) : Prop :=
  review.protectedPredicate = true ->
    review.weakensPredicate = true ->
      review.modificationRejected = true

theorem self_modification_that_weakens_protected_predicate_is_rejected
    {review : SelfModificationPredicateReview} :
    ProtectedPredicateWeakeningRejected review ->
    review.protectedPredicate = true ->
    review.weakensPredicate = true ->
    review.modificationRejected = true := by
  intro valid predicateProtected weakens
  exact valid predicateProtected weakens

inductive ConstitutionalChangeRoute where
  | accepted
  | blockedForReview
deriving DecidableEq, Repr

structure ConstitutionalChangeDecision where
  protectedPredicate : Bool
  weakensPredicate : Bool
  independentReviewerPresent : Bool
  route : ConstitutionalChangeRoute
deriving DecidableEq, Repr

def ConstitutionalChangeSafe (decision : ConstitutionalChangeDecision) : Prop :=
  if decision.protectedPredicate && decision.weakensPredicate && !decision.independentReviewerPresent then
    decision.route = ConstitutionalChangeRoute.blockedForReview
  else
    True

def unsafeWeakeningWithoutReviewBlocked : ConstitutionalChangeDecision where
  protectedPredicate := true
  weakensPredicate := true
  independentReviewerPresent := false
  route := ConstitutionalChangeRoute.blockedForReview

theorem protected_predicate_weakening_without_reviewer_routes_to_review
    {decision : ConstitutionalChangeDecision} :
    ConstitutionalChangeSafe decision ->
    decision.protectedPredicate = true ->
    decision.weakensPredicate = true ->
    decision.independentReviewerPresent = false ->
    decision.route = ConstitutionalChangeRoute.blockedForReview := by
  intro safe predicateProtected weakens missingReviewer
  unfold ConstitutionalChangeSafe at safe
  rw [predicateProtected, weakens, missingReviewer] at safe
  simp at safe
  exact safe

end AsiStackProofs.Alignment

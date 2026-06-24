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

end AsiStackProofs.Alignment

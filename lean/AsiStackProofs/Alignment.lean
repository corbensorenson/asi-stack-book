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

inductive ConstitutionalTransitionPhase where
  | proposed
  | migrationReady
  | active
  | blockedForReview
  | residualized
  | rolledBack
deriving DecidableEq, Repr

inductive ConstitutionalTransitionRoute where
  | accept
  | blockForReview
  | preserveResidual
  | rollback
deriving DecidableEq, Repr

structure ConstitutionalTransitionDecision where
  phase : ConstitutionalTransitionPhase
  sourceVersion : Nat
  targetVersion : Nat
  protectedPredicateChanged : Bool
  protectedPredicatePreserved : Bool
  independentReview : Bool
  rollbackAvailable : Bool
  conflictDetected : Bool
  conflictRouted : Bool
  selfModification : Bool
  weakensPredicate : Bool
  route : ConstitutionalTransitionRoute
deriving DecidableEq, Repr

def ConstitutionalTransitionRequiresReview
    (decision : ConstitutionalTransitionDecision) : Bool :=
  (decision.selfModification && decision.weakensPredicate) ||
    (decision.protectedPredicateChanged &&
      (!decision.protectedPredicatePreserved ||
        !decision.independentReview ||
        !decision.rollbackAvailable))

def ConstitutionalTransitionSafe
    (decision : ConstitutionalTransitionDecision) : Prop :=
  if ConstitutionalTransitionRequiresReview decision then
    decision.route = ConstitutionalTransitionRoute.blockForReview
  else if decision.conflictDetected && !decision.conflictRouted then
    decision.route = ConstitutionalTransitionRoute.preserveResidual
  else
    True

def unsafeConstitutionalMigrationWithoutRollback :
    ConstitutionalTransitionDecision :=
  { phase := ConstitutionalTransitionPhase.migrationReady,
    sourceVersion := 1,
    targetVersion := 2,
    protectedPredicateChanged := true,
    protectedPredicatePreserved := true,
    independentReview := true,
    rollbackAvailable := false,
    conflictDetected := false,
    conflictRouted := true,
    selfModification := false,
    weakensPredicate := false,
    route := ConstitutionalTransitionRoute.blockForReview }

def constitutionalConflictWithoutRouteResidualized :
    ConstitutionalTransitionDecision :=
  { phase := ConstitutionalTransitionPhase.residualized,
    sourceVersion := 1,
    targetVersion := 1,
    protectedPredicateChanged := false,
    protectedPredicatePreserved := true,
    independentReview := true,
    rollbackAvailable := true,
    conflictDetected := true,
    conflictRouted := false,
    selfModification := false,
    weakensPredicate := false,
    route := ConstitutionalTransitionRoute.preserveResidual }

theorem protected_migration_without_rollback_routes_to_review
    {decision : ConstitutionalTransitionDecision} :
    ConstitutionalTransitionSafe decision ->
    decision.protectedPredicateChanged = true ->
    decision.rollbackAvailable = false ->
    decision.route = ConstitutionalTransitionRoute.blockForReview := by
  intro safe changed missingRollback
  unfold ConstitutionalTransitionSafe ConstitutionalTransitionRequiresReview at safe
  rw [changed, missingRollback] at safe
  simp at safe
  exact safe

theorem accepted_transition_cannot_drop_protected_predicate
    {decision : ConstitutionalTransitionDecision} :
    ConstitutionalTransitionSafe decision ->
    decision.route = ConstitutionalTransitionRoute.accept ->
    decision.protectedPredicateChanged = true ->
    decision.protectedPredicatePreserved = false ->
    False := by
  intro safe accepted changed dropped
  unfold ConstitutionalTransitionSafe ConstitutionalTransitionRequiresReview at safe
  rw [changed, dropped] at safe
  simp at safe
  rw [accepted] at safe
  contradiction

theorem detected_conflict_without_route_preserves_residual
    {decision : ConstitutionalTransitionDecision} :
    ConstitutionalTransitionSafe decision ->
    ConstitutionalTransitionRequiresReview decision = false ->
    decision.conflictDetected = true ->
    decision.conflictRouted = false ->
    decision.route = ConstitutionalTransitionRoute.preserveResidual := by
  intro safe noReviewRequired conflict missingRoute
  unfold ConstitutionalTransitionSafe at safe
  rw [noReviewRequired, conflict, missingRoute] at safe
  simp at safe
  exact safe

end AsiStackProofs.Alignment

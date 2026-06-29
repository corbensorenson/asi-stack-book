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

inductive ValueConflictReviewPhase where
  | proposed
  | bounded
  | escalated
  | denied
  | residualized
  | deprecatedPremise
deriving DecidableEq, Repr

inductive ValueConflictReviewRoute where
  | allowBounded
  | blockForReview
  | preserveDissentResidual
  | narrowAuthority
deriving DecidableEq, Repr

structure ValueConflictReviewDecision where
  phase : ValueConflictReviewPhase
  highStakesConflict : Bool
  unresolvedConflict : Bool
  stakeholderDisagreement : Bool
  reviewPresent : Bool
  residualUncertaintyRecorded : Bool
  dissentPayloadPreserved : Bool
  boundedDecision : Bool
  authorityNarrowed : Bool
  reversibleAction : Bool
  revisitPathRecorded : Bool
  deprecatedPremise : Bool
  route : ValueConflictReviewRoute
deriving DecidableEq, Repr

def ValueConflictReviewRequiresReview
    (decision : ValueConflictReviewDecision) : Bool :=
  decision.highStakesConflict &&
    decision.unresolvedConflict &&
      (!decision.reviewPresent ||
        !decision.residualUncertaintyRecorded ||
        !decision.revisitPathRecorded)

def ValueConflictReviewSafe
    (decision : ValueConflictReviewDecision) : Prop :=
  if ValueConflictReviewRequiresReview decision then
    decision.route = ValueConflictReviewRoute.blockForReview
  else if decision.boundedDecision && !decision.dissentPayloadPreserved then
    decision.route = ValueConflictReviewRoute.preserveDissentResidual
  else if decision.unresolvedConflict && !decision.authorityNarrowed then
    decision.route = ValueConflictReviewRoute.narrowAuthority
  else
    True

def highStakesConflictWithoutResidual :
    ValueConflictReviewDecision :=
  { phase := ValueConflictReviewPhase.escalated,
    highStakesConflict := true,
    unresolvedConflict := true,
    stakeholderDisagreement := true,
    reviewPresent := true,
    residualUncertaintyRecorded := false,
    dissentPayloadPreserved := true,
    boundedDecision := false,
    authorityNarrowed := true,
    reversibleAction := false,
    revisitPathRecorded := true,
    deprecatedPremise := false,
    route := ValueConflictReviewRoute.blockForReview }

def boundedDecisionWithoutDissentResidualized :
    ValueConflictReviewDecision :=
  { phase := ValueConflictReviewPhase.bounded,
    highStakesConflict := false,
    unresolvedConflict := true,
    stakeholderDisagreement := true,
    reviewPresent := true,
    residualUncertaintyRecorded := true,
    dissentPayloadPreserved := false,
    boundedDecision := true,
    authorityNarrowed := true,
    reversibleAction := true,
    revisitPathRecorded := true,
    deprecatedPremise := false,
    route := ValueConflictReviewRoute.preserveDissentResidual }

def unresolvedConflictWithoutAuthorityNarrowing :
    ValueConflictReviewDecision :=
  { phase := ValueConflictReviewPhase.residualized,
    highStakesConflict := false,
    unresolvedConflict := true,
    stakeholderDisagreement := true,
    reviewPresent := true,
    residualUncertaintyRecorded := true,
    dissentPayloadPreserved := true,
    boundedDecision := false,
    authorityNarrowed := false,
    reversibleAction := true,
    revisitPathRecorded := true,
    deprecatedPremise := false,
    route := ValueConflictReviewRoute.narrowAuthority }

theorem high_stakes_unresolved_conflict_without_residual_blocks
    {decision : ValueConflictReviewDecision} :
    ValueConflictReviewSafe decision ->
    decision.highStakesConflict = true ->
    decision.unresolvedConflict = true ->
    decision.residualUncertaintyRecorded = false ->
    decision.route = ValueConflictReviewRoute.blockForReview := by
  intro safe highStakes unresolved missingResidual
  unfold ValueConflictReviewSafe ValueConflictReviewRequiresReview at safe
  rw [highStakes, unresolved, missingResidual] at safe
  simp at safe
  exact safe

theorem bounded_decision_without_dissent_preserves_residual
    {decision : ValueConflictReviewDecision} :
    ValueConflictReviewSafe decision ->
    ValueConflictReviewRequiresReview decision = false ->
    decision.boundedDecision = true ->
    decision.dissentPayloadPreserved = false ->
    decision.route = ValueConflictReviewRoute.preserveDissentResidual := by
  intro safe noReviewRequired bounded missingDissent
  unfold ValueConflictReviewSafe at safe
  rw [noReviewRequired, bounded, missingDissent] at safe
  simp at safe
  exact safe

theorem unresolved_conflict_without_authority_narrowing_routes_to_narrowing
    {decision : ValueConflictReviewDecision} :
    ValueConflictReviewSafe decision ->
    ValueConflictReviewRequiresReview decision = false ->
    decision.boundedDecision = false ->
    decision.unresolvedConflict = true ->
    decision.authorityNarrowed = false ->
    decision.route = ValueConflictReviewRoute.narrowAuthority := by
  intro safe noReviewRequired notBounded unresolved notNarrowed
  unfold ValueConflictReviewSafe at safe
  rw [noReviewRequired, notBounded, unresolved, notNarrowed] at safe
  simp at safe
  exact safe

end AsiStackProofs.ValueConflict

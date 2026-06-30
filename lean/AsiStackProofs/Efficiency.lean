namespace AsiStackProofs.Efficiency

structure RouteComparisonReview where
  selectedCost : Nat
  candidateCost : Nat
  candidateAuthorized : Bool
  candidateSatisfiesQuality : Bool
deriving DecidableEq, Repr

def LowerCostAuthorizedQualityCandidate (review : RouteComparisonReview) : Prop :=
  review.candidateCost < review.selectedCost ∧
    review.candidateAuthorized = true ∧
      review.candidateSatisfiesQuality = true

def MinimumViableRoute (reviews : List RouteComparisonReview) : Prop :=
  ∀ review, review ∈ reviews -> ¬ LowerCostAuthorizedQualityCandidate review

theorem minimum_viable_route_has_no_lower_cost_authorized_quality_candidate
    {reviews : List RouteComparisonReview} {review : RouteComparisonReview} :
    MinimumViableRoute reviews ->
    review ∈ reviews ->
    ¬ LowerCostAuthorizedQualityCandidate review := by
  intro minimumViable reviewPresent
  exact minimumViable review reviewPresent

theorem lower_cost_authorized_quality_candidate_rejects_minimum_viable_route
    {reviews : List RouteComparisonReview} {review : RouteComparisonReview} :
    review ∈ reviews ->
    LowerCostAuthorizedQualityCandidate review ->
    ¬ MinimumViableRoute reviews := by
  intro reviewPresent lowerCostCandidate minimumViable
  have rejected := minimumViable review reviewPresent
  exact rejected lowerCostCandidate

structure ResidualPromotionReview where
  openObligations : Bool
  promotionCandidate : Bool
  residualRecordPresent : Bool
deriving DecidableEq, Repr

def OpenObligationPromotionValid (review : ResidualPromotionReview) : Prop :=
  review.openObligations = true ->
    review.promotionCandidate = true ->
      review.residualRecordPresent = true

theorem routed_or_compressed_result_with_open_obligations_requires_residual_record
    {review : ResidualPromotionReview} :
    OpenObligationPromotionValid review ->
    review.openObligations = true ->
    review.promotionCandidate = true ->
    review.residualRecordPresent = true := by
  intro valid obligationsOpen promoted
  exact valid obligationsOpen promoted

theorem open_obligation_promotion_without_residual_record_rejected
    {review : ResidualPromotionReview} :
    review.openObligations = true ->
    review.promotionCandidate = true ->
    review.residualRecordPresent = false ->
    ¬ OpenObligationPromotionValid review := by
  intro obligationsOpen promoted missingResidual valid
  have residual := valid obligationsOpen promoted
  rw [missingResidual] at residual
  cases residual

end AsiStackProofs.Efficiency

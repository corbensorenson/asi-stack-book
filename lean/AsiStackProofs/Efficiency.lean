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

/-! ## Executable finite route selection

The selector below minimizes a complete seven-class modeled cost only among
routes whose declared authority, quality, utility, and residual obligations
are admissible. The declarations are trusted inputs: this model does not prove
that a cost estimate or quality judgment is true in a deployed workload.
-/

structure CostVector where
  model : Nat
  context : Nat
  verification : Nat
  repair : Nat
  humanReview : Nat
  regression : Nat
  rollback : Nat
deriving DecidableEq, Repr

def CostVector.total (cost : CostVector) : Nat :=
  cost.model + cost.context + cost.verification + cost.repair +
    cost.humanReview + cost.regression + cost.rollback

def CostVector.add (left right : CostVector) : CostVector := {
  model := left.model + right.model
  context := left.context + right.context
  verification := left.verification + right.verification
  repair := left.repair + right.repair
  humanReview := left.humanReview + right.humanReview
  regression := left.regression + right.regression
  rollback := left.rollback + right.rollback
}

theorem total_cost_is_additive (left right : CostVector) :
    (left.add right).total = left.total + right.total := by
  simp [CostVector.add, CostVector.total]
  omega

theorem total_cost_is_componentwise_monotone
    {left right : CostVector}
    (model : left.model ≤ right.model)
    (context : left.context ≤ right.context)
    (verification : left.verification ≤ right.verification)
    (repair : left.repair ≤ right.repair)
    (humanReview : left.humanReview ≤ right.humanReview)
    (regression : left.regression ≤ right.regression)
    (rollback : left.rollback ≤ right.rollback) :
    left.total ≤ right.total := by
  simp only [CostVector.total]
  omega

structure RouteCandidate where
  routeId : Nat
  cost : CostVector
  authorized : Bool
  qualityPassed : Bool
  utilityPreserved : Bool
  openObligations : Bool
  residualRecorded : Bool
deriving DecidableEq, Repr

def RouteEligible (candidate : RouteCandidate) : Prop :=
  candidate.authorized = true ∧
    candidate.qualityPassed = true ∧
      candidate.utilityPreserved = true ∧
        (candidate.openObligations = true → candidate.residualRecorded = true)

instance routeEligibleDecidable (candidate : RouteCandidate) :
    Decidable (RouteEligible candidate) := by
  unfold RouteEligible
  infer_instance

def SelectMinimumEligible : List RouteCandidate → Option RouteCandidate
  | [] => none
  | candidate :: tail =>
      match SelectMinimumEligible tail with
      | none => if RouteEligible candidate then some candidate else none
      | some best =>
          if RouteEligible candidate ∧ candidate.cost.total < best.cost.total
          then some candidate
          else some best

theorem selected_route_is_a_listed_eligible_candidate
    {candidates : List RouteCandidate} {selected : RouteCandidate}
    (selection : SelectMinimumEligible candidates = some selected) :
    selected ∈ candidates ∧ RouteEligible selected := by
  induction candidates generalizing selected with
  | nil => simp [SelectMinimumEligible] at selection
  | cons candidate tail ih =>
      simp only [SelectMinimumEligible] at selection
      cases tailSelection : SelectMinimumEligible tail with
      | none =>
          simp [tailSelection] at selection
          rcases selection with ⟨eligible, rfl⟩
          exact ⟨by simp, eligible⟩
      | some best =>
          have bestFacts := ih tailSelection
          simp [tailSelection] at selection
          split at selection
          · rename_i better
            simp at selection
            subst selected
            exact ⟨by simp, better.1⟩
          · simp at selection
            subst selected
            exact ⟨by simp [bestFacts.1], bestFacts.2⟩

theorem no_selected_route_means_no_eligible_candidate
    {candidates : List RouteCandidate}
    (selection : SelectMinimumEligible candidates = none) :
    ∀ candidate, candidate ∈ candidates → ¬ RouteEligible candidate := by
  induction candidates with
  | nil => simp
  | cons head tail ih =>
      simp only [SelectMinimumEligible] at selection
      cases tailSelection : SelectMinimumEligible tail with
      | none =>
          simp [tailSelection] at selection
          intro candidate present eligible
          simp at present
          rcases present with rfl | inTail
          · exact selection eligible
          · exact ih tailSelection candidate inTail eligible
      | some best =>
          by_cases better : RouteEligible head ∧ head.cost.total < best.cost.total <;>
            simp [tailSelection, better] at selection

theorem selected_route_has_minimum_modeled_cost
    {candidates : List RouteCandidate} {selected : RouteCandidate}
    (selection : SelectMinimumEligible candidates = some selected) :
    ∀ candidate, candidate ∈ candidates → RouteEligible candidate →
      selected.cost.total ≤ candidate.cost.total := by
  induction candidates generalizing selected with
  | nil => simp [SelectMinimumEligible] at selection
  | cons head tail ih =>
      simp only [SelectMinimumEligible] at selection
      cases tailSelection : SelectMinimumEligible tail with
      | none =>
          simp [tailSelection] at selection
          rcases selection with ⟨headEligible, rfl⟩
          intro candidate present eligible
          simp at present
          rcases present with rfl | inTail
          · exact Nat.le_refl _
          · exact False.elim
              (no_selected_route_means_no_eligible_candidate tailSelection
                candidate inTail eligible)
      | some best =>
          have bestMinimum := ih tailSelection
          simp [tailSelection] at selection
          split at selection
          · rename_i headBetter
            simp at selection
            subst selected
            intro candidate present eligible
            simp at present
            rcases present with rfl | inTail
            · exact Nat.le_refl _
            · exact Nat.le_trans (Nat.le_of_lt headBetter.2)
                (bestMinimum candidate inTail eligible)
          · rename_i notBetter
            simp at selection
            subst selected
            intro candidate present eligible
            simp at present
            rcases present with rfl | inTail
            · apply Nat.le_of_not_gt
              intro lower
              exact notBetter ⟨eligible, lower⟩
            · exact bestMinimum candidate inTail eligible

def boundedTransformRoute : RouteCandidate := {
  routeId := 20
  cost := {
    model := 24
    context := 6
    verification := 9
    repair := 3
    humanReview := 0
    regression := 4
    rollback := 2
  }
  authorized := true
  qualityPassed := true
  utilityPreserved := true
  openObligations := true
  residualRecorded := true
}

def cheapFailedRoute : RouteCandidate := {
  routeId := 10
  cost := {
    model := 8
    context := 2
    verification := 2
    repair := 0
    humanReview := 0
    regression := 0
    rollback := 0
  }
  authorized := true
  qualityPassed := false
  utilityPreserved := false
  openObligations := true
  residualRecorded := true
}

def authorityBypassRoute : RouteCandidate := {
  routeId := 30
  cost := {
    model := 18
    context := 3
    verification := 4
    repair := 0
    humanReview := 0
    regression := 0
    rollback := 0
  }
  authorized := false
  qualityPassed := true
  utilityPreserved := true
  openObligations := false
  residualRecorded := true
}

def manualReviewRoute : RouteCandidate := {
  routeId := 40
  cost := {
    model := 85
    context := 18
    verification := 12
    repair := 0
    humanReview := 22
    regression := 5
    rollback := 2
  }
  authorized := true
  qualityPassed := true
  utilityPreserved := true
  openObligations := false
  residualRecorded := true
}

theorem finite_selector_reaches_bounded_minimum_witness :
    SelectMinimumEligible
      [cheapFailedRoute, boundedTransformRoute, authorityBypassRoute,
        manualReviewRoute] = some boundedTransformRoute := by
  decide

theorem cheaper_unauthorized_route_does_not_displace_eligible_minimum :
    SelectMinimumEligible [boundedTransformRoute, authorityBypassRoute] =
      some boundedTransformRoute := by
  decide

theorem cheaper_failed_quality_route_does_not_displace_eligible_minimum :
    SelectMinimumEligible [cheapFailedRoute, boundedTransformRoute] =
      some boundedTransformRoute := by
  decide

end AsiStackProofs.Efficiency

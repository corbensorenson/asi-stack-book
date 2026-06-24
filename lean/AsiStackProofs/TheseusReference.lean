namespace AsiStackProofs.TheseusReference

structure ImplementationReferenceClaimReview where
  implementationReferenceClaim : Bool
  reportRefPresent : Bool
  configOrToolRefPresent : Bool
  dashboardProseOnly : Bool
deriving DecidableEq, Repr

def ImplementationReferenceClaimHasArtifactSurface
    (review : ImplementationReferenceClaimReview) : Prop :=
  review.implementationReferenceClaim = true ->
    (review.reportRefPresent = true ∨
      review.configOrToolRefPresent = true) ∧
        review.dashboardProseOnly = false

theorem implementation_reference_claim_names_report_config_or_tool_not_dashboard_only
    {review : ImplementationReferenceClaimReview} :
    ImplementationReferenceClaimHasArtifactSurface review ->
    review.implementationReferenceClaim = true ->
    (review.reportRefPresent = true ∨
      review.configOrToolRefPresent = true) ∧
        review.dashboardProseOnly = false := by
  intro valid referenceClaim
  exact valid referenceClaim

structure GateBeforePromotionReview where
  capabilityOrSelfEvolutionPromotion : Bool
  requiredGateReportsPresent : Bool
  requiredGateReportsPassing : Bool
  promotionAccepted : Bool
deriving DecidableEq, Repr

def MissingOrFailingGateReportsBlockPromotion
    (review : GateBeforePromotionReview) : Prop :=
  review.capabilityOrSelfEvolutionPromotion = true ->
    (review.requiredGateReportsPresent = false ∨
      review.requiredGateReportsPassing = false) ->
        review.promotionAccepted = false

theorem capability_or_self_evolution_promotion_blocked_without_passing_gate_reports
    {review : GateBeforePromotionReview} :
    MissingOrFailingGateReportsBlockPromotion review ->
    review.capabilityOrSelfEvolutionPromotion = true ->
    (review.requiredGateReportsPresent = false ∨
      review.requiredGateReportsPassing = false) ->
    review.promotionAccepted = false := by
  intro valid promoted missingOrFailing
  exact valid promoted missingOrFailing

end AsiStackProofs.TheseusReference

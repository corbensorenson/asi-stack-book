namespace AsiStackProofs.Routing

inductive RouteOutcome where
  | selected
  | fallback
  | residual
  | promoted
deriving DecidableEq, Repr

structure SpecialistRoute where
  authoritySatisfied : Bool
  readinessSatisfied : Bool
  outcome : RouteOutcome
deriving DecidableEq, Repr

def SelectedRouteAdmissible (route : SpecialistRoute) : Prop :=
  route.outcome = RouteOutcome.selected ->
    route.authoritySatisfied = true ∧ route.readinessSatisfied = true

theorem selected_specialist_satisfies_authority_and_readiness
    {route : SpecialistRoute} :
    SelectedRouteAdmissible route ->
    route.outcome = RouteOutcome.selected ->
      route.authoritySatisfied = true ∧ route.readinessSatisfied = true := by
  intro admissible selected
  exact admissible selected

theorem selected_route_without_authority_or_readiness_rejected
    {route : SpecialistRoute} :
    route.outcome = RouteOutcome.selected ->
      (route.authoritySatisfied = false ∨ route.readinessSatisfied = false) ->
        ¬ SelectedRouteAdmissible route := by
  intro selected missingGate admissible
  have required := admissible selected
  cases missingGate with
  | inl missingAuthority =>
      rw [missingAuthority] at required
      cases required.1
  | inr missingReadiness =>
      rw [missingReadiness] at required
      cases required.2

def ReadinessFailureHandled (route : SpecialistRoute) : Prop :=
  route.readinessSatisfied = false ->
    route.outcome = RouteOutcome.fallback ∨ route.outcome = RouteOutcome.residual

theorem failed_readiness_routes_to_fallback_or_residual_not_promotion
    {route : SpecialistRoute} :
    ReadinessFailureHandled route ->
    route.readinessSatisfied = false ->
      (route.outcome = RouteOutcome.fallback ∨
        route.outcome = RouteOutcome.residual) ∧
        route.outcome ≠ RouteOutcome.promoted := by
  intro handled failedReadiness
  have routed := handled failedReadiness
  constructor
  · exact routed
  · intro promoted
    cases routed with
    | inl fallback =>
        rw [promoted] at fallback
        cases fallback
    | inr residual =>
        rw [promoted] at residual
        cases residual

inductive RoutingDecisionRoute where
  | noRouteRequested
  | rejectMissingCapabilityRequest
  | requestSpecialistRegistry
  | blockAuthorityMismatch
  | routeToFallback
  | requestResidualOwner
  | residualizeNoFallback
  | requestFreshLease
  | requestCostQualityRecord
  | requestLeastCapableAdequateJustification
  | requestRejectedCandidateEvidence
  | preserveNonClaimBoundary
  | selectSpecialist
deriving DecidableEq, Repr

structure RoutingDecisionReview where
  routeRequested : Bool
  capabilityRequestPresent : Bool
  specialistRegistered : Bool
  authoritySatisfied : Bool
  readinessSatisfied : Bool
  fallbackAvailable : Bool
  residualOwnerPresent : Bool
  freshLeasePresent : Bool
  costQualityRecordPresent : Bool
  selectedSpecialistIsLeastCapableAdequate : Bool
  rejectedCandidateEvidencePresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def RoutingDecisionRouteFor
    (review : RoutingDecisionReview) :
    RoutingDecisionRoute :=
  if review.routeRequested = false then
    RoutingDecisionRoute.noRouteRequested
  else if review.capabilityRequestPresent = false then
    RoutingDecisionRoute.rejectMissingCapabilityRequest
  else if review.specialistRegistered = false then
    RoutingDecisionRoute.requestSpecialistRegistry
  else if review.authoritySatisfied = false then
    RoutingDecisionRoute.blockAuthorityMismatch
  else if review.readinessSatisfied = false then
    if review.fallbackAvailable = true then
      RoutingDecisionRoute.routeToFallback
    else if review.residualOwnerPresent = false then
      RoutingDecisionRoute.requestResidualOwner
    else
      RoutingDecisionRoute.residualizeNoFallback
  else if review.freshLeasePresent = false then
    RoutingDecisionRoute.requestFreshLease
  else if review.costQualityRecordPresent = false then
    RoutingDecisionRoute.requestCostQualityRecord
  else if review.selectedSpecialistIsLeastCapableAdequate = false then
    RoutingDecisionRoute.requestLeastCapableAdequateJustification
  else if review.rejectedCandidateEvidencePresent = false then
    RoutingDecisionRoute.requestRejectedCandidateEvidence
  else if review.nonClaimBoundaryPresent = false then
    RoutingDecisionRoute.preserveNonClaimBoundary
  else
    RoutingDecisionRoute.selectSpecialist

def completeRoutingDecisionReview : RoutingDecisionReview where
  routeRequested := true
  capabilityRequestPresent := true
  specialistRegistered := true
  authoritySatisfied := true
  readinessSatisfied := true
  fallbackAvailable := true
  residualOwnerPresent := true
  freshLeasePresent := true
  costQualityRecordPresent := true
  selectedSpecialistIsLeastCapableAdequate := true
  rejectedCandidateEvidencePresent := true
  nonClaimBoundaryPresent := true

theorem no_route_request_stays_no_route :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          routeRequested := false } =
      RoutingDecisionRoute.noRouteRequested := by
  simp [RoutingDecisionRouteFor]

theorem missing_capability_request_rejects_route :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          capabilityRequestPresent := false } =
      RoutingDecisionRoute.rejectMissingCapabilityRequest := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem missing_specialist_registry_requests_registry :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          specialistRegistered := false } =
      RoutingDecisionRoute.requestSpecialistRegistry := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem authority_mismatch_blocks_route_selection :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          authoritySatisfied := false } =
      RoutingDecisionRoute.blockAuthorityMismatch := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem readiness_failure_with_fallback_routes_to_fallback :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          readinessSatisfied := false } =
      RoutingDecisionRoute.routeToFallback := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem readiness_failure_without_fallback_or_residual_owner_requests_owner :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          readinessSatisfied := false
          fallbackAvailable := false
          residualOwnerPresent := false } =
      RoutingDecisionRoute.requestResidualOwner := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem readiness_failure_without_fallback_residualizes_when_owner_present :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          readinessSatisfied := false
          fallbackAvailable := false } =
      RoutingDecisionRoute.residualizeNoFallback := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem missing_fresh_lease_requests_lease :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          freshLeasePresent := false } =
      RoutingDecisionRoute.requestFreshLease := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem missing_cost_quality_record_requests_record :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          costQualityRecordPresent := false } =
      RoutingDecisionRoute.requestCostQualityRecord := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem overprivileged_selection_requests_least_capable_justification :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          selectedSpecialistIsLeastCapableAdequate := false } =
      RoutingDecisionRoute.requestLeastCapableAdequateJustification := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem missing_rejected_candidate_evidence_requests_evidence :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          rejectedCandidateEvidencePresent := false } =
      RoutingDecisionRoute.requestRejectedCandidateEvidence := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem route_without_nonclaim_boundary_preserves_boundary :
    RoutingDecisionRouteFor
        { completeRoutingDecisionReview with
          nonClaimBoundaryPresent := false } =
      RoutingDecisionRoute.preserveNonClaimBoundary := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

theorem complete_routing_decision_selects_specialist :
    RoutingDecisionRouteFor completeRoutingDecisionReview =
      RoutingDecisionRoute.selectSpecialist := by
  simp [RoutingDecisionRouteFor, completeRoutingDecisionReview]

end AsiStackProofs.Routing

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

end AsiStackProofs.Routing

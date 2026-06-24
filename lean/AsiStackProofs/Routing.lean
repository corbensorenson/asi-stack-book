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

end AsiStackProofs.Routing

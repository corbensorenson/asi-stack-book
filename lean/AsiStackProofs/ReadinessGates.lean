namespace AsiStackProofs.ReadinessGates

inductive GateDecision where
  | reject
  | quarantine
  | shadow
  | canary
  | qualify
  | defaultReady
  | retire
  | rerun
deriving DecidableEq, Repr

def PromotedDecision : GateDecision -> Prop
  | .canary => True
  | .qualify => True
  | .defaultReady => True
  | _ => False

structure GateReview where
  allRequiredGatesPass : Bool
  decision : GateDecision
deriving DecidableEq, Repr

def PromotionGateValid (review : GateReview) : Prop :=
  PromotedDecision review.decision -> review.allRequiredGatesPass = true

theorem promoted_decision_requires_all_required_gates
    {review : GateReview} :
    PromotionGateValid review ->
    PromotedDecision review.decision ->
    review.allRequiredGatesPass = true := by
  intro valid promoted
  exact valid promoted

inductive ReadinessState where
  | candidate
  | shadow
  | canary
  | qualified
  | defaultReady
  | quarantined
  | retired
deriving DecidableEq, Repr

structure RouteSelection where
  state : ReadinessState
  ordinaryRouteSelected : Bool
deriving DecidableEq, Repr

def OrdinaryRouteSelectionAllowed (selection : RouteSelection) : Prop :=
  selection.ordinaryRouteSelected = true ∧
    selection.state ≠ ReadinessState.quarantined

theorem quarantined_module_cannot_be_selected_for_ordinary_route
    {selection : RouteSelection} :
    selection.state = ReadinessState.quarantined ->
    ¬ OrdinaryRouteSelectionAllowed selection := by
  intro quarantined selected
  unfold OrdinaryRouteSelectionAllowed at selected
  exact selected.2 quarantined

end AsiStackProofs.ReadinessGates

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

theorem promoted_decision_with_failed_required_gates_rejected
    {review : GateReview} :
    PromotedDecision review.decision ->
    review.allRequiredGatesPass = false ->
    ¬ PromotionGateValid review := by
  intro promoted gatesFailed valid
  have gatesPass := valid promoted
  rw [gatesFailed] at gatesPass
  contradiction

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

structure ReadinessTransitionReview where
  strongerStateRequested : Bool
  transitionAccepted : Bool
  gateEvidenceFresh : Bool
  residualEscrowCarried : Bool
  fallbackPathPresent : Bool
  expiryRecorded : Bool
deriving DecidableEq, Repr

def StrongerReadinessTransitionValid
    (review : ReadinessTransitionReview) : Prop :=
  review.strongerStateRequested = true ->
    review.transitionAccepted = true ->
      review.gateEvidenceFresh = true ∧
        review.residualEscrowCarried = true ∧
          review.fallbackPathPresent = true ∧
            review.expiryRecorded = true

theorem accepted_stronger_transition_missing_required_record_rejected
    {review : ReadinessTransitionReview} :
    review.strongerStateRequested = true ->
    review.transitionAccepted = true ->
    (review.gateEvidenceFresh = false ∨
      review.residualEscrowCarried = false ∨
        review.fallbackPathPresent = false ∨
          review.expiryRecorded = false) ->
    ¬ StrongerReadinessTransitionValid review := by
  intro stronger accepted missing valid
  unfold StrongerReadinessTransitionValid at valid
  have complete := valid stronger accepted
  cases complete with
  | intro evidenceFresh rest =>
      cases rest with
      | intro residualCarried rest =>
          cases rest with
          | intro fallbackPresent expiryRecorded =>
              cases missing with
              | inl evidenceMissing =>
                  rw [evidenceMissing] at evidenceFresh
                  contradiction
              | inr restMissing =>
                  cases restMissing with
                  | inl residualMissing =>
                      rw [residualMissing] at residualCarried
                      contradiction
                  | inr restMissing =>
                      cases restMissing with
                      | inl fallbackMissing =>
                          rw [fallbackMissing] at fallbackPresent
                          contradiction
                      | inr expiryMissing =>
                          rw [expiryMissing] at expiryRecorded
                          contradiction

structure QuarantineRoutingReview where
  targetQuarantined : Bool
  ordinaryRouteSelected : Bool
  diagnosticRouteSelected : Bool
  fallbackPathPresent : Bool
deriving DecidableEq, Repr

def QuarantineRoutingValid (review : QuarantineRoutingReview) : Prop :=
  review.targetQuarantined = true ->
    review.ordinaryRouteSelected = false ∧
      (review.diagnosticRouteSelected = true ->
        review.fallbackPathPresent = true)

theorem quarantined_target_ordinary_or_unbacked_diagnostic_route_rejected
    {review : QuarantineRoutingReview} :
    review.targetQuarantined = true ->
    (review.ordinaryRouteSelected = true ∨
      (review.diagnosticRouteSelected = true ∧
        review.fallbackPathPresent = false)) ->
    ¬ QuarantineRoutingValid review := by
  intro quarantined invalid valid
  unfold QuarantineRoutingValid at valid
  have routeBoundary := valid quarantined
  cases routeBoundary with
  | intro ordinaryBlocked diagnosticRequiresFallback =>
      cases invalid with
      | inl ordinarySelected =>
          rw [ordinarySelected] at ordinaryBlocked
          contradiction
      | inr diagnosticInvalid =>
          cases diagnosticInvalid with
          | intro diagnosticSelected fallbackMissing =>
              have fallbackPresent := diagnosticRequiresFallback diagnosticSelected
              rw [fallbackMissing] at fallbackPresent
              contradiction

structure StaleGateReuseReview where
  promotedDecisionAccepted : Bool
  gateExpired : Bool
  architectureChanged : Bool
  rerunRecorded : Bool
  residualRecorded : Bool
deriving DecidableEq, Repr

def StaleGateReuseValid (review : StaleGateReuseReview) : Prop :=
  review.promotedDecisionAccepted = true ->
    (review.gateExpired = true ∨ review.architectureChanged = true) ->
      review.rerunRecorded = true ∧
        review.residualRecorded = true

theorem stale_gate_reuse_without_rerun_or_residual_rejected
    {review : StaleGateReuseReview} :
    review.promotedDecisionAccepted = true ->
    (review.gateExpired = true ∨ review.architectureChanged = true) ->
    (review.rerunRecorded = false ∨
      review.residualRecorded = false) ->
    ¬ StaleGateReuseValid review := by
  intro accepted stale missing valid
  unfold StaleGateReuseValid at valid
  have complete := valid accepted stale
  cases complete with
  | intro rerunRecorded residualRecorded =>
      cases missing with
      | inl rerunMissing =>
          rw [rerunMissing] at rerunRecorded
          contradiction
      | inr residualMissing =>
          rw [residualMissing] at residualRecorded
          contradiction

end AsiStackProofs.ReadinessGates

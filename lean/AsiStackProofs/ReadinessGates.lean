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
  | superseded
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

structure ReadinessLifecycleTransition where
  fromState : ReadinessState
  toState : ReadinessState
  gateEvidenceFresh : Bool
  residualEscrowCarried : Bool
  fallbackPathPresent : Bool
  expiryRecorded : Bool
  regressionFloorPreserved : Bool
  authorityScopePreserved : Bool
  ordinaryRouteAllowed : Bool
  diagnosticRouteAllowed : Bool
  supersessionRecordPresent : Bool
  retirementReceiptPresent : Bool
deriving DecidableEq, Repr

def ReadinessForwardStep
    (transition : ReadinessLifecycleTransition) : Prop :=
  (transition.fromState = ReadinessState.candidate ∧
      transition.toState = ReadinessState.shadow) ∨
    (transition.fromState = ReadinessState.shadow ∧
      transition.toState = ReadinessState.canary) ∨
    (transition.fromState = ReadinessState.canary ∧
      transition.toState = ReadinessState.qualified) ∨
    (transition.fromState = ReadinessState.qualified ∧
      transition.toState = ReadinessState.defaultReady) ∨
    (transition.toState = ReadinessState.quarantined) ∨
    (transition.toState = ReadinessState.superseded) ∨
    (transition.toState = ReadinessState.retired)

def ReadinessTransitionNotFromRetired
    (transition : ReadinessLifecycleTransition) : Prop :=
  transition.fromState ≠ ReadinessState.retired

def ReadinessTransitionCoreRecordsPresent
    (transition : ReadinessLifecycleTransition) : Prop :=
  transition.gateEvidenceFresh = true ∧
    transition.residualEscrowCarried = true ∧
      transition.fallbackPathPresent = true ∧
        transition.expiryRecorded = true

def QualifiedReadinessReady
    (transition : ReadinessLifecycleTransition) : Prop :=
  transition.toState = ReadinessState.qualified ->
    transition.regressionFloorPreserved = true

def DefaultReadinessReady
    (transition : ReadinessLifecycleTransition) : Prop :=
  transition.toState = ReadinessState.defaultReady ->
    transition.regressionFloorPreserved = true ∧
      transition.authorityScopePreserved = true ∧
        transition.ordinaryRouteAllowed = true

def QuarantineReadinessReady
    (transition : ReadinessLifecycleTransition) : Prop :=
  transition.toState = ReadinessState.quarantined ->
    transition.ordinaryRouteAllowed = false ∧
      transition.diagnosticRouteAllowed = true ∧
        transition.fallbackPathPresent = true

def SupersessionReadinessReady
    (transition : ReadinessLifecycleTransition) : Prop :=
  transition.toState = ReadinessState.superseded ->
    transition.supersessionRecordPresent = true ∧
      transition.residualEscrowCarried = true

def RetirementReadinessReady
    (transition : ReadinessLifecycleTransition) : Prop :=
  transition.toState = ReadinessState.retired ->
    transition.retirementReceiptPresent = true ∧
      transition.residualEscrowCarried = true

def ReadinessLifecycleTransitionAllowed
    (transition : ReadinessLifecycleTransition) : Prop :=
  ReadinessForwardStep transition ∧
    ReadinessTransitionNotFromRetired transition ∧
      ReadinessTransitionCoreRecordsPresent transition ∧
        QualifiedReadinessReady transition ∧
          DefaultReadinessReady transition ∧
            QuarantineReadinessReady transition ∧
              SupersessionReadinessReady transition ∧
                RetirementReadinessReady transition

theorem readiness_lifecycle_transition_must_be_forward_or_terminal
    {transition : ReadinessLifecycleTransition} :
    ReadinessLifecycleTransitionAllowed transition ->
      ReadinessForwardStep transition := by
  intro allowed
  exact allowed.left

theorem retired_readiness_state_cannot_transition
    {transition : ReadinessLifecycleTransition} :
    transition.fromState = ReadinessState.retired ->
      ¬ ReadinessLifecycleTransitionAllowed transition := by
  intro retiredFrom allowed
  have notRetired := allowed.right.left
  exact notRetired retiredFrom

theorem allowed_readiness_transition_requires_core_records
    {transition : ReadinessLifecycleTransition} :
    ReadinessLifecycleTransitionAllowed transition ->
      transition.gateEvidenceFresh = true ∧
        transition.residualEscrowCarried = true ∧
          transition.fallbackPathPresent = true ∧
            transition.expiryRecorded = true := by
  intro allowed
  exact allowed.right.right.left

theorem qualified_readiness_requires_regression_floor
    {transition : ReadinessLifecycleTransition} :
    ReadinessLifecycleTransitionAllowed transition ->
      transition.toState = ReadinessState.qualified ->
        transition.regressionFloorPreserved = true := by
  intro allowed toQualified
  exact allowed.right.right.right.left toQualified

theorem default_readiness_requires_regression_authority_and_route
    {transition : ReadinessLifecycleTransition} :
    ReadinessLifecycleTransitionAllowed transition ->
      transition.toState = ReadinessState.defaultReady ->
        transition.regressionFloorPreserved = true ∧
          transition.authorityScopePreserved = true ∧
            transition.ordinaryRouteAllowed = true := by
  intro allowed toDefault
  exact allowed.right.right.right.right.left toDefault

theorem default_readiness_without_regression_floor_rejected
    {transition : ReadinessLifecycleTransition} :
    transition.toState = ReadinessState.defaultReady ->
      transition.regressionFloorPreserved = false ->
        ¬ ReadinessLifecycleTransitionAllowed transition := by
  intro toDefault regressionMissing allowed
  have defaultReady :=
    default_readiness_requires_regression_authority_and_route allowed toDefault
  rw [regressionMissing] at defaultReady
  cases defaultReady.left

theorem default_readiness_without_authority_scope_rejected
    {transition : ReadinessLifecycleTransition} :
    transition.toState = ReadinessState.defaultReady ->
      transition.authorityScopePreserved = false ->
        ¬ ReadinessLifecycleTransitionAllowed transition := by
  intro toDefault authorityMissing allowed
  have defaultReady :=
    default_readiness_requires_regression_authority_and_route allowed toDefault
  have authorityReady := defaultReady.right.left
  rw [authorityMissing] at authorityReady
  cases authorityReady

theorem quarantine_transition_blocks_ordinary_and_requires_fallback
    {transition : ReadinessLifecycleTransition} :
    ReadinessLifecycleTransitionAllowed transition ->
      transition.toState = ReadinessState.quarantined ->
        transition.ordinaryRouteAllowed = false ∧
          transition.diagnosticRouteAllowed = true ∧
            transition.fallbackPathPresent = true := by
  intro allowed toQuarantined
  exact allowed.right.right.right.right.right.left toQuarantined

theorem quarantined_lifecycle_transition_with_ordinary_route_rejected
    {transition : ReadinessLifecycleTransition} :
    transition.toState = ReadinessState.quarantined ->
      transition.ordinaryRouteAllowed = true ->
        ¬ ReadinessLifecycleTransitionAllowed transition := by
  intro toQuarantined ordinaryAllowed allowed
  have quarantineReady :=
    quarantine_transition_blocks_ordinary_and_requires_fallback
      allowed toQuarantined
  rw [ordinaryAllowed] at quarantineReady
  cases quarantineReady.left

theorem supersession_requires_record_and_residual_escrow
    {transition : ReadinessLifecycleTransition} :
    ReadinessLifecycleTransitionAllowed transition ->
      transition.toState = ReadinessState.superseded ->
        transition.supersessionRecordPresent = true ∧
          transition.residualEscrowCarried = true := by
  intro allowed toSuperseded
  exact allowed.right.right.right.right.right.right.left toSuperseded

theorem supersession_without_record_rejected
    {transition : ReadinessLifecycleTransition} :
    transition.toState = ReadinessState.superseded ->
      transition.supersessionRecordPresent = false ->
        ¬ ReadinessLifecycleTransitionAllowed transition := by
  intro toSuperseded recordMissing allowed
  have supersessionReady :=
    supersession_requires_record_and_residual_escrow allowed toSuperseded
  rw [recordMissing] at supersessionReady
  cases supersessionReady.left

theorem retirement_requires_receipt_and_residual_escrow
    {transition : ReadinessLifecycleTransition} :
    ReadinessLifecycleTransitionAllowed transition ->
      transition.toState = ReadinessState.retired ->
        transition.retirementReceiptPresent = true ∧
          transition.residualEscrowCarried = true := by
  intro allowed toRetired
  exact allowed.right.right.right.right.right.right.right toRetired

theorem retirement_without_receipt_rejected
    {transition : ReadinessLifecycleTransition} :
    transition.toState = ReadinessState.retired ->
      transition.retirementReceiptPresent = false ->
        ¬ ReadinessLifecycleTransitionAllowed transition := by
  intro toRetired receiptMissing allowed
  have retirementReady :=
    retirement_requires_receipt_and_residual_escrow allowed toRetired
  rw [receiptMissing] at retirementReady
  cases retirementReady.left

end AsiStackProofs.ReadinessGates

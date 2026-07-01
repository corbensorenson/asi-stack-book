namespace AsiStackProofs.ResourceEconomics

structure BudgetGateReview where
  requiredSafetyGate : Bool
  requiredVerificationGate : Bool
  safetyGateDisabled : Bool
  verificationGateDisabled : Bool
deriving DecidableEq, Repr

def RequiredGatesPreserved (review : BudgetGateReview) : Prop :=
  (review.requiredSafetyGate = true -> review.safetyGateDisabled = false) ∧
    (review.requiredVerificationGate = true -> review.verificationGateDisabled = false)

theorem task_budget_cannot_disable_required_safety_or_verification_gates
    {review : BudgetGateReview} :
    RequiredGatesPreserved review ->
    review.requiredSafetyGate = true ->
    review.requiredVerificationGate = true ->
    review.safetyGateDisabled = false ∧ review.verificationGateDisabled = false := by
  intro preserved safetyRequired verificationRequired
  exact ⟨preserved.1 safetyRequired, preserved.2 verificationRequired⟩

theorem required_safety_gate_disabled_rejects_budget_gate_preservation
    {review : BudgetGateReview} :
    review.requiredSafetyGate = true ->
    review.safetyGateDisabled = true ->
    ¬ RequiredGatesPreserved review := by
  intro safetyRequired disabled preserved
  have preservedSafety := preserved.1 safetyRequired
  rw [disabled] at preservedSafety
  cases preservedSafety

inductive RiskClass where
  | low
  | medium
  | high
  | critical
deriving DecidableEq, Repr

def HighRisk : RiskClass -> Prop
  | .high => True
  | .critical => True
  | _ => False

inductive BudgetDecision where
  | dispatch
  | escalate
  | defer
  | shrinkScope
  | reject
  | residual
deriving DecidableEq, Repr

def BlockedOrEscalated : BudgetDecision -> Prop
  | .escalate => True
  | .defer => True
  | .shrinkScope => True
  | .reject => True
  | .residual => True
  | .dispatch => False

structure VerificationBudgetReview where
  riskClass : RiskClass
  verificationBudgetSufficient : Bool
  decision : BudgetDecision
deriving DecidableEq, Repr

def HighRiskVerificationBudgetValid (review : VerificationBudgetReview) : Prop :=
  HighRisk review.riskClass ->
    review.verificationBudgetSufficient = false ->
      BlockedOrEscalated review.decision

theorem high_risk_task_with_insufficient_verification_budget_is_not_dispatched
    {review : VerificationBudgetReview} :
    HighRiskVerificationBudgetValid review ->
    HighRisk review.riskClass ->
    review.verificationBudgetSufficient = false ->
    BlockedOrEscalated review.decision := by
  intro valid highRisk insufficient
  exact valid highRisk insufficient

theorem high_risk_insufficient_budget_dispatch_rejected
    {review : VerificationBudgetReview} :
    HighRisk review.riskClass ->
    review.verificationBudgetSufficient = false ->
    review.decision = BudgetDecision.dispatch ->
    ¬ HighRiskVerificationBudgetValid review := by
  intro highRisk insufficient dispatched valid
  have blocked := valid highRisk insufficient
  rw [dispatched] at blocked
  cases blocked

inductive CostedRoute where
  | frontierManualReview
  | boundedTransformPlusVerifier
  | cheapUnverifiedTransform
  | hiddenResidualAutoMerge
deriving DecidableEq, Repr

structure CostedRouteAssessment where
  route : CostedRoute
  costTenths : Nat
  verificationPassed : Bool
  adequateOutcome : Bool
  promotionCandidate : Bool
  budgetDispatchable : Bool
  residualOwned : Bool
  hiddenCostDisplaced : Bool
  fallbackVisible : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def CostedRouteEligible (assessment : CostedRouteAssessment) : Prop :=
  assessment.verificationPassed = true ∧
    assessment.adequateOutcome = true ∧
    assessment.promotionCandidate = true ∧
    assessment.budgetDispatchable = true ∧
    assessment.residualOwned = true ∧
    assessment.hiddenCostDisplaced = false ∧
    assessment.fallbackVisible = true ∧
    assessment.nonClaimBoundary = true

def CostedRouteEligibleFlag (assessment : CostedRouteAssessment) : Bool :=
  assessment.verificationPassed &&
    assessment.adequateOutcome &&
    assessment.promotionCandidate &&
    assessment.budgetDispatchable &&
    assessment.residualOwned &&
    (! assessment.hiddenCostDisplaced) &&
    assessment.fallbackVisible &&
    assessment.nonClaimBoundary

def costedRouteFixtureAssessment : CostedRoute -> CostedRouteAssessment
  | .frontierManualReview =>
      { route := .frontierManualReview,
        costTenths := 430,
        verificationPassed := true,
        adequateOutcome := true,
        promotionCandidate := true,
        budgetDispatchable := true,
        residualOwned := true,
        hiddenCostDisplaced := false,
        fallbackVisible := true,
        nonClaimBoundary := true }
  | .boundedTransformPlusVerifier =>
      { route := .boundedTransformPlusVerifier,
        costTenths := 142,
        verificationPassed := true,
        adequateOutcome := true,
        promotionCandidate := true,
        budgetDispatchable := true,
        residualOwned := true,
        hiddenCostDisplaced := false,
        fallbackVisible := true,
        nonClaimBoundary := true }
  | .cheapUnverifiedTransform =>
      { route := .cheapUnverifiedTransform,
        costTenths := 23,
        verificationPassed := false,
        adequateOutcome := false,
        promotionCandidate := false,
        budgetDispatchable := false,
        residualOwned := true,
        hiddenCostDisplaced := false,
        fallbackVisible := true,
        nonClaimBoundary := true }
  | .hiddenResidualAutoMerge =>
      { route := .hiddenResidualAutoMerge,
        costTenths := 82,
        verificationPassed := true,
        adequateOutcome := false,
        promotionCandidate := true,
        budgetDispatchable := false,
        residualOwned := false,
        hiddenCostDisplaced := true,
        fallbackVisible := true,
        nonClaimBoundary := true }

def CostedRouteFixtureSelected : CostedRoute :=
  .boundedTransformPlusVerifier

theorem costed_route_fixture_selected_is_eligible :
    CostedRouteEligible (costedRouteFixtureAssessment CostedRouteFixtureSelected) := by
  simp [CostedRouteFixtureSelected, costedRouteFixtureAssessment, CostedRouteEligible]

theorem cheap_unverified_transform_rejected_by_fixture :
    ¬ CostedRouteEligible (costedRouteFixtureAssessment .cheapUnverifiedTransform) := by
  intro eligible
  simp [costedRouteFixtureAssessment, CostedRouteEligible] at eligible

theorem hidden_residual_auto_merge_rejected_by_fixture :
    ¬ CostedRouteEligible (costedRouteFixtureAssessment .hiddenResidualAutoMerge) := by
  intro eligible
  simp [costedRouteFixtureAssessment, CostedRouteEligible] at eligible

theorem selected_route_is_lowest_cost_eligible_in_fixture
    {route : CostedRoute} :
    CostedRouteEligible (costedRouteFixtureAssessment route) ->
      (costedRouteFixtureAssessment CostedRouteFixtureSelected).costTenths ≤
        (costedRouteFixtureAssessment route).costTenths := by
  intro eligible
  cases route <;>
    simp [CostedRouteFixtureSelected, costedRouteFixtureAssessment,
      CostedRouteEligible] at eligible ⊢ <;>
    decide

structure RouteSelectorState where
  bestRoute : Option CostedRoute
  bestCostTenths : Nat
  eligibleSeen : Nat
  rejectedCheaperSeen : Nat
deriving DecidableEq, Repr

def emptyRouteSelectorState : RouteSelectorState :=
  { bestRoute := none,
    bestCostTenths := 0,
    eligibleSeen := 0,
    rejectedCheaperSeen := 0 }

def considerCostedRoute (state : RouteSelectorState) (route : CostedRoute) :
    RouteSelectorState :=
  let assessment := costedRouteFixtureAssessment route
  if CostedRouteEligibleFlag assessment then
    match state.bestRoute with
    | none =>
        { bestRoute := some route,
          bestCostTenths := assessment.costTenths,
          eligibleSeen := state.eligibleSeen + 1,
          rejectedCheaperSeen := state.rejectedCheaperSeen }
    | some _ =>
        if assessment.costTenths < state.bestCostTenths then
          { bestRoute := some route,
            bestCostTenths := assessment.costTenths,
            eligibleSeen := state.eligibleSeen + 1,
            rejectedCheaperSeen := state.rejectedCheaperSeen }
        else
          { state with eligibleSeen := state.eligibleSeen + 1 }
  else
    if assessment.costTenths <
        (costedRouteFixtureAssessment CostedRouteFixtureSelected).costTenths then
      { state with rejectedCheaperSeen := state.rejectedCheaperSeen + 1 }
    else
      state

def costedRouteFixtureTraceFinalState : RouteSelectorState :=
  let s0 := emptyRouteSelectorState
  let s1 := considerCostedRoute s0 .cheapUnverifiedTransform
  let s2 := considerCostedRoute s1 .hiddenResidualAutoMerge
  let s3 := considerCostedRoute s2 .frontierManualReview
  considerCostedRoute s3 .boundedTransformPlusVerifier

theorem costed_route_fixture_trace_selects_lowest_eligible_route :
    costedRouteFixtureTraceFinalState.bestRoute = some CostedRouteFixtureSelected ∧
      costedRouteFixtureTraceFinalState.bestCostTenths = 142 ∧
      costedRouteFixtureTraceFinalState.eligibleSeen = 2 ∧
      costedRouteFixtureTraceFinalState.rejectedCheaperSeen = 2 := by
  simp [costedRouteFixtureTraceFinalState, considerCostedRoute,
    emptyRouteSelectorState, CostedRouteFixtureSelected,
    costedRouteFixtureAssessment, CostedRouteEligibleFlag]

structure WorkflowTraceSummary where
  stepCount : Nat
  selectedRouteCount : Nat
  totalCostTenths : Nat
  reviewMinutesUsed : Nat
  verificationMinutesUsed : Nat
  expectedInvalidControlCount : Nat
  highRiskFirst : Bool
  displacedCostsResidualized : Bool
  physicalFeasibilityOverclaimRejected : Bool
  latencyOnlySelectionRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def WorkflowTraceValid (summary : WorkflowTraceSummary) : Prop :=
  summary.stepCount = 3 ∧
    summary.selectedRouteCount = 3 ∧
    summary.totalCostTenths = 1197 ∧
    summary.reviewMinutesUsed = 26 ∧
    summary.verificationMinutesUsed = 21 ∧
    summary.expectedInvalidControlCount = 4 ∧
    summary.highRiskFirst = true ∧
    summary.displacedCostsResidualized = true ∧
    summary.physicalFeasibilityOverclaimRejected = true ∧
    summary.latencyOnlySelectionRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

def resourceWorkflowTraceFixture : WorkflowTraceSummary :=
  { stepCount := 3,
    selectedRouteCount := 3,
    totalCostTenths := 1197,
    reviewMinutesUsed := 26,
    verificationMinutesUsed := 21,
    expectedInvalidControlCount := 4,
    highRiskFirst := true,
    displacedCostsResidualized := true,
    physicalFeasibilityOverclaimRejected := true,
    latencyOnlySelectionRejected := true,
    supportStateEffectNone := true,
    nonClaimBoundary := true }

theorem resource_workflow_trace_fixture_valid :
    WorkflowTraceValid resourceWorkflowTraceFixture := by
  simp [WorkflowTraceValid, resourceWorkflowTraceFixture]

theorem resource_workflow_trace_fixture_preserves_high_risk_ordering :
    resourceWorkflowTraceFixture.highRiskFirst = true := by
  rfl

theorem resource_workflow_trace_fixture_residualizes_displaced_costs :
    resourceWorkflowTraceFixture.displacedCostsResidualized = true := by
  rfl

theorem resource_workflow_trace_fixture_rejects_physical_feasibility_overclaim :
    resourceWorkflowTraceFixture.physicalFeasibilityOverclaimRejected = true := by
  rfl

theorem resource_workflow_trace_fixture_rejects_latency_only_selection :
    resourceWorkflowTraceFixture.latencyOnlySelectionRejected = true := by
  rfl

theorem resource_workflow_trace_fixture_has_no_support_promotion :
    resourceWorkflowTraceFixture.supportStateEffectNone = true := by
  rfl

inductive WorkflowStep where
  | highRiskReleaseGate
  | sourceCrosswalkRefresh
  | lowRiskIndexCleanup
deriving DecidableEq, Repr

inductive WorkflowSelectedRoute where
  | humanVerifierReleaseGate
  | boundedCrosswalkRefresh
  | localIndexCleanup
deriving DecidableEq, Repr

structure WorkflowDispatchEvent where
  step : WorkflowStep
  selectedRoute : WorkflowSelectedRoute
  dispatchOrder : Nat
  costTenths : Nat
  reviewMinutes : Nat
  verificationMinutes : Nat
  highRisk : Bool
  protectedOverheadPaid : Bool
  residualsOwned : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def resourceWorkflowTraceFixtureEvents : List WorkflowDispatchEvent :=
  [
    { step := .highRiskReleaseGate,
      selectedRoute := .humanVerifierReleaseGate,
      dispatchOrder := 1,
      costTenths := 732,
      reviewMinutes := 18,
      verificationMinutes := 12,
      highRisk := true,
      protectedOverheadPaid := true,
      residualsOwned := true,
      nonClaimBoundary := true },
    { step := .sourceCrosswalkRefresh,
      selectedRoute := .boundedCrosswalkRefresh,
      dispatchOrder := 2,
      costTenths := 382,
      reviewMinutes := 8,
      verificationMinutes := 6,
      highRisk := false,
      protectedOverheadPaid := true,
      residualsOwned := true,
      nonClaimBoundary := true },
    { step := .lowRiskIndexCleanup,
      selectedRoute := .localIndexCleanup,
      dispatchOrder := 3,
      costTenths := 83,
      reviewMinutes := 0,
      verificationMinutes := 3,
      highRisk := false,
      protectedOverheadPaid := true,
      residualsOwned := true,
      nonClaimBoundary := true }
  ]

def workflowTraceCostTenths : List WorkflowDispatchEvent -> Nat
  | [] => 0
  | event :: rest => event.costTenths + workflowTraceCostTenths rest

def workflowTraceReviewMinutes : List WorkflowDispatchEvent -> Nat
  | [] => 0
  | event :: rest => event.reviewMinutes + workflowTraceReviewMinutes rest

def workflowTraceVerificationMinutes : List WorkflowDispatchEvent -> Nat
  | [] => 0
  | event :: rest => event.verificationMinutes + workflowTraceVerificationMinutes rest

def workflowTraceHighRiskFirst (events : List WorkflowDispatchEvent) : Bool :=
  events.all (fun high =>
    events.all (fun low =>
      if high.highRisk && (! low.highRisk) then
        decide (high.dispatchOrder < low.dispatchOrder)
      else
        true))

def workflowTraceGuardsPreserved (events : List WorkflowDispatchEvent) : Bool :=
  events.all (fun event =>
    event.protectedOverheadPaid && event.residualsOwned && event.nonClaimBoundary)

theorem resource_workflow_trace_fixture_events_roll_up_to_summary :
    workflowTraceCostTenths resourceWorkflowTraceFixtureEvents =
        resourceWorkflowTraceFixture.totalCostTenths ∧
      workflowTraceReviewMinutes resourceWorkflowTraceFixtureEvents =
        resourceWorkflowTraceFixture.reviewMinutesUsed ∧
      workflowTraceVerificationMinutes resourceWorkflowTraceFixtureEvents =
        resourceWorkflowTraceFixture.verificationMinutesUsed ∧
      resourceWorkflowTraceFixtureEvents.length =
        resourceWorkflowTraceFixture.selectedRouteCount := by
  native_decide

theorem resource_workflow_trace_fixture_events_keep_high_risk_first :
    workflowTraceHighRiskFirst resourceWorkflowTraceFixtureEvents = true := by
  native_decide

theorem resource_workflow_trace_fixture_events_preserve_guard_flags :
    workflowTraceGuardsPreserved resourceWorkflowTraceFixtureEvents = true := by
  native_decide

end AsiStackProofs.ResourceEconomics

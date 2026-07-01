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

structure ServingMemoryAccounting where
  aggregateThroughputClaimed : Bool
  kvCacheBudgetRecorded : Bool
  batchingScopeRecorded : Bool
  singleRequestVerifiedOutputSeparated : Bool
  modelQualityClaimedFromThroughput : Bool
  supportStateEffectNone : Bool
deriving DecidableEq, Repr

def ServingMemoryAccountingValid (record : ServingMemoryAccounting) : Prop :=
  (record.aggregateThroughputClaimed = true ->
    record.kvCacheBudgetRecorded = true ∧
      record.batchingScopeRecorded = true ∧
      record.singleRequestVerifiedOutputSeparated = true) ∧
    record.modelQualityClaimedFromThroughput = false ∧
    record.supportStateEffectNone = true

theorem aggregate_serving_throughput_requires_single_request_boundary
    {record : ServingMemoryAccounting} :
    ServingMemoryAccountingValid record ->
    record.aggregateThroughputClaimed = true ->
      record.kvCacheBudgetRecorded = true ∧
        record.batchingScopeRecorded = true ∧
        record.singleRequestVerifiedOutputSeparated = true := by
  intro valid claimed
  exact valid.1 claimed

theorem serving_memory_throughput_quality_overclaim_rejected
    {record : ServingMemoryAccounting} :
    record.modelQualityClaimedFromThroughput = true ->
    ¬ ServingMemoryAccountingValid record := by
  intro qualityClaim valid
  have noQualityClaim := valid.2.1
  rw [qualityClaim] at noQualityClaim
  cases noQualityClaim

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
  capacityBudgetOverrunRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def WorkflowTraceValid (summary : WorkflowTraceSummary) : Prop :=
  summary.stepCount = 3 ∧
    summary.selectedRouteCount = 3 ∧
    summary.totalCostTenths = 1197 ∧
    summary.reviewMinutesUsed = 26 ∧
    summary.verificationMinutesUsed = 21 ∧
    summary.expectedInvalidControlCount = 5 ∧
    summary.highRiskFirst = true ∧
    summary.displacedCostsResidualized = true ∧
    summary.physicalFeasibilityOverclaimRejected = true ∧
    summary.latencyOnlySelectionRejected = true ∧
    summary.capacityBudgetOverrunRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

def resourceWorkflowTraceFixture : WorkflowTraceSummary :=
  { stepCount := 3,
    selectedRouteCount := 3,
    totalCostTenths := 1197,
    reviewMinutesUsed := 26,
    verificationMinutesUsed := 21,
    expectedInvalidControlCount := 5,
    highRiskFirst := true,
    displacedCostsResidualized := true,
    physicalFeasibilityOverclaimRejected := true,
    latencyOnlySelectionRejected := true,
    capacityBudgetOverrunRejected := true,
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

theorem resource_workflow_trace_fixture_rejects_capacity_budget_overrun :
    resourceWorkflowTraceFixture.capacityBudgetOverrunRejected = true := by
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

structure CapacitySmoothingReviewTrace where
  stepCount : Nat
  finalCapacity : Nat
  finalReviewCapacity : Nat
  protectedReviewPaid : Bool
  displacedReviewCostResidualized : Bool
  lowRiskBlockedProtectedReview : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def CapacitySmoothingReviewTraceValid (trace : CapacitySmoothingReviewTrace) : Prop :=
  trace.stepCount = 3 ∧
    trace.finalCapacity = 3 ∧
    trace.finalReviewCapacity = 3 ∧
    trace.protectedReviewPaid = true ∧
    trace.displacedReviewCostResidualized = true ∧
    trace.lowRiskBlockedProtectedReview = false ∧
    trace.supportStateEffectNone = true ∧
    trace.nonClaimBoundary = true

def capacitySmoothingReviewerTraceFixture : CapacitySmoothingReviewTrace :=
  { stepCount := 3,
    finalCapacity := 3,
    finalReviewCapacity := 3,
    protectedReviewPaid := true,
    displacedReviewCostResidualized := true,
    lowRiskBlockedProtectedReview := false,
    supportStateEffectNone := true,
    nonClaimBoundary := true }

theorem capacity_smoothing_reviewer_trace_fixture_valid :
    CapacitySmoothingReviewTraceValid capacitySmoothingReviewerTraceFixture := by
  simp [CapacitySmoothingReviewTraceValid, capacitySmoothingReviewerTraceFixture]

theorem capacity_smoothing_reviewer_trace_preserves_review_capacity :
    capacitySmoothingReviewerTraceFixture.finalReviewCapacity = 3 := by
  rfl

theorem capacity_smoothing_reviewer_trace_preserves_protected_review_overhead :
    capacitySmoothingReviewerTraceFixture.protectedReviewPaid = true := by
  rfl

theorem capacity_smoothing_reviewer_trace_residualizes_displaced_review_costs :
    capacitySmoothingReviewerTraceFixture.displacedReviewCostResidualized = true := by
  rfl

theorem capacity_smoothing_reviewer_trace_has_no_support_promotion :
    capacitySmoothingReviewerTraceFixture.supportStateEffectNone = true := by
  rfl

structure ReviewerCapacityDecision where
  blockedProtectedReview : Bool
  admittedLowRiskReview : Bool
  highRiskWorkAdmitted : Bool
  protectedReviewPaid : Bool
  displacedReviewCostResidualized : Bool
deriving DecidableEq, Repr

def ReviewerCapacityDecisionValid (decision : ReviewerCapacityDecision) : Prop :=
  (decision.blockedProtectedReview = true -> decision.admittedLowRiskReview = false) ∧
    (decision.highRiskWorkAdmitted = true -> decision.protectedReviewPaid = true) ∧
    (decision.blockedProtectedReview = true -> decision.displacedReviewCostResidualized = true)

theorem blocked_protected_review_rejects_low_risk_review_dispatch
    {decision : ReviewerCapacityDecision} :
    decision.blockedProtectedReview = true ->
    decision.admittedLowRiskReview = true ->
    ¬ ReviewerCapacityDecisionValid decision := by
  intro blocked admitted valid
  have noLowRisk := valid.1 blocked
  rw [admitted] at noLowRisk
  cases noLowRisk

theorem high_risk_review_without_protected_overhead_rejected
    {decision : ReviewerCapacityDecision} :
    decision.highRiskWorkAdmitted = true ->
    decision.protectedReviewPaid = false ->
    ¬ ReviewerCapacityDecisionValid decision := by
  intro highRisk noProtected valid
  have paid := valid.2.1 highRisk
  rw [noProtected] at paid
  cases paid

theorem blocked_protected_review_requires_displaced_cost_residual
    {decision : ReviewerCapacityDecision} :
    decision.blockedProtectedReview = true ->
    decision.displacedReviewCostResidualized = false ->
    ¬ ReviewerCapacityDecisionValid decision := by
  intro blocked notResidualized valid
  have residualized := valid.2.2 blocked
  rw [notResidualized] at residualized
  cases residualized

structure LoadSmoothingWorkloadSummary where
  taskCount : Nat
  routeCount : Nat
  baselinePeakCapacityOverrun : Nat
  baselineTotalOverrun : Nat
  selectedPeakCapacityOverrun : Nat
  selectedTotalOverrun : Nat
  selectedDeferredTaskTicks : Nat
  selectedResidualizedDeferredTaskTicks : Nat
  negativeProtectedReviewViolations : Nat
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def LoadSmoothingWorkloadValid (summary : LoadSmoothingWorkloadSummary) : Prop :=
  summary.taskCount = 10 ∧
    summary.routeCount = 3 ∧
    summary.baselinePeakCapacityOverrun = 2 ∧
    summary.baselineTotalOverrun = 5 ∧
    summary.selectedPeakCapacityOverrun = 0 ∧
    summary.selectedTotalOverrun = 0 ∧
    summary.selectedDeferredTaskTicks = 7 ∧
    summary.selectedResidualizedDeferredTaskTicks = 7 ∧
    summary.negativeProtectedReviewViolations = 3 ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

def resourceLoadSmoothingWorkloadFixture : LoadSmoothingWorkloadSummary :=
  { taskCount := 10,
    routeCount := 3,
    baselinePeakCapacityOverrun := 2,
    baselineTotalOverrun := 5,
    selectedPeakCapacityOverrun := 0,
    selectedTotalOverrun := 0,
    selectedDeferredTaskTicks := 7,
    selectedResidualizedDeferredTaskTicks := 7,
    negativeProtectedReviewViolations := 3,
    supportStateEffectNone := true,
    nonClaimBoundary := true }

theorem resource_load_smoothing_workload_fixture_valid :
    LoadSmoothingWorkloadValid resourceLoadSmoothingWorkloadFixture := by
  simp [LoadSmoothingWorkloadValid, resourceLoadSmoothingWorkloadFixture]

theorem resource_load_smoothing_workload_reduces_overrun :
    resourceLoadSmoothingWorkloadFixture.selectedTotalOverrun <
      resourceLoadSmoothingWorkloadFixture.baselineTotalOverrun := by
  simp [resourceLoadSmoothingWorkloadFixture]

theorem resource_load_smoothing_workload_rejects_review_erasure :
    0 < resourceLoadSmoothingWorkloadFixture.negativeProtectedReviewViolations := by
  simp [resourceLoadSmoothingWorkloadFixture]

theorem resource_load_smoothing_workload_residualizes_deferrals :
    resourceLoadSmoothingWorkloadFixture.selectedDeferredTaskTicks =
      resourceLoadSmoothingWorkloadFixture.selectedResidualizedDeferredTaskTicks := by
  rfl

theorem resource_load_smoothing_workload_has_no_support_promotion :
    resourceLoadSmoothingWorkloadFixture.supportStateEffectNone = true := by
  rfl

end AsiStackProofs.ResourceEconomics

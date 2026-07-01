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

structure WorkflowTraceSummary where
  stepCount : Nat
  selectedRouteCount : Nat
  totalCostTenths : Nat
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

end AsiStackProofs.ResourceEconomics

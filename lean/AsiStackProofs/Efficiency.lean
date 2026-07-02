namespace AsiStackProofs.Efficiency

structure RouteComparisonReview where
  selectedCost : Nat
  candidateCost : Nat
  candidateAuthorized : Bool
  candidateSatisfiesQuality : Bool
deriving DecidableEq, Repr

def LowerCostAuthorizedQualityCandidate (review : RouteComparisonReview) : Prop :=
  review.candidateCost < review.selectedCost ∧
    review.candidateAuthorized = true ∧
      review.candidateSatisfiesQuality = true

def MinimumViableRoute (reviews : List RouteComparisonReview) : Prop :=
  ∀ review, review ∈ reviews -> ¬ LowerCostAuthorizedQualityCandidate review

theorem minimum_viable_route_has_no_lower_cost_authorized_quality_candidate
    {reviews : List RouteComparisonReview} {review : RouteComparisonReview} :
    MinimumViableRoute reviews ->
    review ∈ reviews ->
    ¬ LowerCostAuthorizedQualityCandidate review := by
  intro minimumViable reviewPresent
  exact minimumViable review reviewPresent

theorem lower_cost_authorized_quality_candidate_rejects_minimum_viable_route
    {reviews : List RouteComparisonReview} {review : RouteComparisonReview} :
    review ∈ reviews ->
    LowerCostAuthorizedQualityCandidate review ->
    ¬ MinimumViableRoute reviews := by
  intro reviewPresent lowerCostCandidate minimumViable
  have rejected := minimumViable review reviewPresent
  exact rejected lowerCostCandidate

structure ResidualPromotionReview where
  openObligations : Bool
  promotionCandidate : Bool
  residualRecordPresent : Bool
deriving DecidableEq, Repr

def OpenObligationPromotionValid (review : ResidualPromotionReview) : Prop :=
  review.openObligations = true ->
    review.promotionCandidate = true ->
      review.residualRecordPresent = true

theorem routed_or_compressed_result_with_open_obligations_requires_residual_record
    {review : ResidualPromotionReview} :
    OpenObligationPromotionValid review ->
    review.openObligations = true ->
    review.promotionCandidate = true ->
    review.residualRecordPresent = true := by
  intro valid obligationsOpen promoted
  exact valid obligationsOpen promoted

theorem open_obligation_promotion_without_residual_record_rejected
    {review : ResidualPromotionReview} :
    review.openObligations = true ->
    review.promotionCandidate = true ->
    review.residualRecordPresent = false ->
    ¬ OpenObligationPromotionValid review := by
  intro obligationsOpen promoted missingResidual valid
  have residual := valid obligationsOpen promoted
  rw [missingResidual] at residual
  cases residual

inductive EfficiencyClaimAdmissionRoute where
  | noEfficiencyClaimRequested
  | requestTaskContract
  | requestQualityPredicate
  | requestSelectedRoute
  | requestCandidateSet
  | requestLowerCostComparisons
  | requestCostClassLedger
  | requestCompleteVisibleCosts
  | requestVerificationResult
  | blockFailedQuality
  | blockAuthorityBypass
  | requestResidualRecord
  | requestFallbackRoute
  | requestHiddenCostAudit
  | requestBenchmarkOrTrace
  | requestNegativeControls
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | admitEfficiencyClaim
deriving DecidableEq, Repr

structure EfficiencyClaimAdmissionReview where
  efficiencyClaimRequested : Bool
  taskContractRecorded : Bool
  qualityPredicateRecorded : Bool
  selectedRouteRecorded : Bool
  candidateSetRecorded : Bool
  lowerCostComparisonsRecorded : Bool
  costClassesRecorded : Bool
  visibleCostsComplete : Bool
  verificationResultRecorded : Bool
  qualityPassed : Bool
  authorityPreserved : Bool
  residualsRecorded : Bool
  fallbackRouteRecorded : Bool
  hiddenCostAuditRecorded : Bool
  benchmarkOrTraceRecorded : Bool
  negativeControlsRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def EfficiencyClaimAdmissionRouteFor
    (review : EfficiencyClaimAdmissionReview) :
    EfficiencyClaimAdmissionRoute :=
  if review.efficiencyClaimRequested = false then
    .noEfficiencyClaimRequested
  else if review.taskContractRecorded = false then
    .requestTaskContract
  else if review.qualityPredicateRecorded = false then
    .requestQualityPredicate
  else if review.selectedRouteRecorded = false then
    .requestSelectedRoute
  else if review.candidateSetRecorded = false then
    .requestCandidateSet
  else if review.lowerCostComparisonsRecorded = false then
    .requestLowerCostComparisons
  else if review.costClassesRecorded = false then
    .requestCostClassLedger
  else if review.visibleCostsComplete = false then
    .requestCompleteVisibleCosts
  else if review.verificationResultRecorded = false then
    .requestVerificationResult
  else if review.qualityPassed = false then
    .blockFailedQuality
  else if review.authorityPreserved = false then
    .blockAuthorityBypass
  else if review.residualsRecorded = false then
    .requestResidualRecord
  else if review.fallbackRouteRecorded = false then
    .requestFallbackRoute
  else if review.hiddenCostAuditRecorded = false then
    .requestHiddenCostAudit
  else if review.benchmarkOrTraceRecorded = false then
    .requestBenchmarkOrTrace
  else if review.negativeControlsRecorded = false then
    .requestNegativeControls
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    .requestEvidenceTransition
  else if review.nonClaimBoundaryRecorded = false then
    .preserveNonClaimBoundary
  else
    .admitEfficiencyClaim

def completeEfficiencyClaimAdmissionReview :
    EfficiencyClaimAdmissionReview := {
  efficiencyClaimRequested := true
  taskContractRecorded := true
  qualityPredicateRecorded := true
  selectedRouteRecorded := true
  candidateSetRecorded := true
  lowerCostComparisonsRecorded := true
  costClassesRecorded := true
  visibleCostsComplete := true
  verificationResultRecorded := true
  qualityPassed := true
  authorityPreserved := true
  residualsRecorded := true
  fallbackRouteRecorded := true
  hiddenCostAuditRecorded := true
  benchmarkOrTraceRecorded := true
  negativeControlsRecorded := true
  supportPromotionRequested := false
  evidenceTransitionRecorded := true
  nonClaimBoundaryRecorded := true
}

theorem no_efficiency_claim_request_stays_idle :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        efficiencyClaimRequested := false } =
      .noEfficiencyClaimRequested := by
  simp [EfficiencyClaimAdmissionRouteFor]

theorem missing_task_contract_requests_contract :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        taskContractRecorded := false } =
      .requestTaskContract := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_quality_predicate_requests_predicate :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        qualityPredicateRecorded := false } =
      .requestQualityPredicate := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_selected_route_requests_route_record :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        selectedRouteRecorded := false } =
      .requestSelectedRoute := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_candidate_set_requests_candidate_set :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        candidateSetRecorded := false } =
      .requestCandidateSet := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_lower_cost_comparisons_requests_comparisons :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        lowerCostComparisonsRecorded := false } =
      .requestLowerCostComparisons := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_cost_classes_requests_cost_ledger :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        costClassesRecorded := false } =
      .requestCostClassLedger := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem incomplete_visible_costs_request_complete_costs :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        visibleCostsComplete := false } =
      .requestCompleteVisibleCosts := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_verification_result_requests_verification :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        verificationResultRecorded := false } =
      .requestVerificationResult := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem failed_quality_blocks_efficiency_claim :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        qualityPassed := false } =
      .blockFailedQuality := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem authority_bypass_blocks_efficiency_claim :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        authorityPreserved := false } =
      .blockAuthorityBypass := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_residuals_request_residual_record :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        residualsRecorded := false } =
      .requestResidualRecord := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_fallback_route_requests_fallback :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        fallbackRouteRecorded := false } =
      .requestFallbackRoute := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_hidden_cost_audit_requests_audit :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        hiddenCostAuditRecorded := false } =
      .requestHiddenCostAudit := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_benchmark_or_trace_requests_trace :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        benchmarkOrTraceRecorded := false } =
      .requestBenchmarkOrTrace := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem missing_negative_controls_requests_controls :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        negativeControlsRecorded := false } =
      .requestNegativeControls := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem promotion_request_without_efficiency_evidence_transition_requests_transition :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        supportPromotionRequested := true
        evidenceTransitionRecorded := false } =
      .requestEvidenceTransition := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem efficiency_claim_without_nonclaim_boundary_preserves_boundary :
    EfficiencyClaimAdmissionRouteFor
      { completeEfficiencyClaimAdmissionReview with
        nonClaimBoundaryRecorded := false } =
      .preserveNonClaimBoundary := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

theorem complete_efficiency_claim_admission_allows_claim_record :
    EfficiencyClaimAdmissionRouteFor completeEfficiencyClaimAdmissionReview =
      .admitEfficiencyClaim := by
  simp [EfficiencyClaimAdmissionRouteFor, completeEfficiencyClaimAdmissionReview]

structure EfficiencyRouteSearchProbeSummary where
  validTraces : Nat
  invalidControls : Nat
  candidateRoutesChecked : Nat
  minimumVerifiedRouteSelection : Bool
  cheapFailedQualityRejected : Bool
  hiddenResidualRejected : Bool
  authorityBypassRejected : Bool
  compressionUtilityRejected : Bool
  hiddenCostClassAudit : Bool
  noRouteSearchCompletenessClaim : Bool
  noMeasuredEfficiencyClaim : Bool
  noSupportStatePromotion : Bool
deriving DecidableEq, Repr

def EfficiencyRouteSearchProbeValid
    (summary : EfficiencyRouteSearchProbeSummary) : Prop :=
  summary.validTraces = 2 ∧
    summary.invalidControls = 6 ∧
    summary.candidateRoutesChecked = 14 ∧
    summary.minimumVerifiedRouteSelection = true ∧
    summary.cheapFailedQualityRejected = true ∧
    summary.hiddenResidualRejected = true ∧
    summary.authorityBypassRejected = true ∧
    summary.compressionUtilityRejected = true ∧
    summary.hiddenCostClassAudit = true ∧
    summary.noRouteSearchCompletenessClaim = true ∧
    summary.noMeasuredEfficiencyClaim = true ∧
    summary.noSupportStatePromotion = true

def efficiencyRouteSearchProbeFixture :
    EfficiencyRouteSearchProbeSummary :=
  {
    validTraces := 2
    invalidControls := 6
    candidateRoutesChecked := 14
    minimumVerifiedRouteSelection := true
    cheapFailedQualityRejected := true
    hiddenResidualRejected := true
    authorityBypassRejected := true
    compressionUtilityRejected := true
    hiddenCostClassAudit := true
    noRouteSearchCompletenessClaim := true
    noMeasuredEfficiencyClaim := true
    noSupportStatePromotion := true
  }

theorem efficiency_route_search_probe_fixture_valid :
    EfficiencyRouteSearchProbeValid efficiencyRouteSearchProbeFixture := by
  unfold EfficiencyRouteSearchProbeValid efficiencyRouteSearchProbeFixture
  simp

def EfficiencyRouteSearchProbeRejectsInvalidSavings
    (summary : EfficiencyRouteSearchProbeSummary) : Prop :=
  summary.invalidControls = 6 ->
    summary.cheapFailedQualityRejected = true ∧
      summary.hiddenResidualRejected = true ∧
      summary.authorityBypassRejected = true ∧
      summary.compressionUtilityRejected = true

theorem efficiency_route_search_probe_rejects_invalid_savings :
    EfficiencyRouteSearchProbeRejectsInvalidSavings
      efficiencyRouteSearchProbeFixture := by
  unfold EfficiencyRouteSearchProbeRejectsInvalidSavings
    efficiencyRouteSearchProbeFixture
  intro _
  simp

def EfficiencyRouteSearchProbePreservesNoPromotionBoundary
    (summary : EfficiencyRouteSearchProbeSummary) : Prop :=
  summary.noRouteSearchCompletenessClaim = true ∧
    summary.noMeasuredEfficiencyClaim = true ∧
    summary.noSupportStatePromotion = true

theorem efficiency_route_search_probe_preserves_no_promotion_boundary :
    EfficiencyRouteSearchProbePreservesNoPromotionBoundary
      efficiencyRouteSearchProbeFixture := by
  unfold EfficiencyRouteSearchProbePreservesNoPromotionBoundary
    efficiencyRouteSearchProbeFixture
  simp

end AsiStackProofs.Efficiency

namespace AsiStackProofs.SearchSubstrates

structure SubstrateAdoptionRecord where
  baselineRefsPresent : Bool
  measuredTargetDeclared : Bool
  falsificationCriterionDeclared : Bool
deriving DecidableEq, Repr

def AdoptionFieldsComplete (record : SubstrateAdoptionRecord) : Prop :=
  record.baselineRefsPresent = true ∧
    record.measuredTargetDeclared = true ∧
      record.falsificationCriterionDeclared = true

theorem substrate_adoption_record_missing_required_field_rejected
    {record : SubstrateAdoptionRecord} :
    (record.baselineRefsPresent = false ∨
      record.measuredTargetDeclared = false ∨
        record.falsificationCriterionDeclared = false) ->
    ¬ AdoptionFieldsComplete record := by
  intro missing complete
  unfold AdoptionFieldsComplete at complete
  cases complete with
  | intro baselinesPresent targetAndFalsification =>
      cases targetAndFalsification with
      | intro targetDeclared falsificationDeclared =>
          cases missing with
          | inl baselinesMissing =>
              rw [baselinesMissing] at baselinesPresent
              contradiction
          | inr targetOrFalsification =>
              cases targetOrFalsification with
              | inl targetMissing =>
                  rw [targetMissing] at targetDeclared
                  contradiction
              | inr falsificationMissing =>
                  rw [falsificationMissing] at falsificationDeclared
                  contradiction

inductive AdoptionState where
  | exploratory
  | blocked
  | canary
  | qualified
  | retired
  | refuted
deriving DecidableEq, Repr

def NonCoreState : AdoptionState -> Prop
  | .exploratory => True
  | .blocked => True
  | .canary => True
  | .retired => True
  | .refuted => True
  | .qualified => False

structure SubstratePromotionReview where
  passingEvidence : Bool
  adoptionState : AdoptionState
deriving DecidableEq, Repr

def UnprovenSubstrateRemainsNonCore (review : SubstratePromotionReview) : Prop :=
  review.passingEvidence = false -> NonCoreState review.adoptionState

theorem unproven_qualified_record_contradicts_noncore_invariant
    {review : SubstratePromotionReview} :
    review.passingEvidence = false ->
    review.adoptionState = AdoptionState.qualified ->
    ¬ UnprovenSubstrateRemainsNonCore review := by
  intro noEvidence qualified valid
  unfold UnprovenSubstrateRemainsNonCore at valid
  have nonCore := valid noEvidence
  rw [qualified] at nonCore
  simp [NonCoreState] at nonCore

def CoreAdoptionValid (review : SubstratePromotionReview) : Prop :=
  review.adoptionState = AdoptionState.qualified -> review.passingEvidence = true

theorem qualified_substrate_without_passing_evidence_rejected
    {review : SubstratePromotionReview} :
    review.adoptionState = AdoptionState.qualified ->
    review.passingEvidence = false ->
    ¬ CoreAdoptionValid review := by
  intro qualified noEvidence valid
  unfold CoreAdoptionValid at valid
  have evidence := valid qualified
  rw [noEvidence] at evidence
  contradiction

structure SubstrateConsumerAxisReview where
  consumerRequestsAxis : Bool
  axisMeasured : Bool
  axisBlocked : Bool
  consumerApproved : Bool
deriving DecidableEq, Repr

def ConsumerAxisRelianceValid
    (review : SubstrateConsumerAxisReview) : Prop :=
  review.consumerRequestsAxis = true ->
    (review.axisMeasured = false ∨ review.axisBlocked = true) ->
      review.consumerApproved = false

theorem consumer_axis_reliance_without_measurement_or_unblocked_axis_rejected
    {review : SubstrateConsumerAxisReview} :
    review.consumerRequestsAxis = true ->
    (review.axisMeasured = false ∨ review.axisBlocked = true) ->
    review.consumerApproved = true ->
    ¬ ConsumerAxisRelianceValid review := by
  intro requested unsupported approved valid
  unfold ConsumerAxisRelianceValid at valid
  have rejected := valid requested unsupported
  rw [approved] at rejected
  contradiction

structure SubstrateCanaryEvidenceReview where
  canaryPromoted : Bool
  workloadRefPresent : Bool
  baselineRefPresent : Bool
  negativeControlPresent : Bool
  resultReportPresent : Bool
deriving DecidableEq, Repr

def CanaryPromotionEvidenceComplete
    (review : SubstrateCanaryEvidenceReview) : Prop :=
  review.canaryPromoted = true ->
    review.workloadRefPresent = true ∧
      review.baselineRefPresent = true ∧
        review.negativeControlPresent = true ∧
          review.resultReportPresent = true

theorem canary_substrate_without_complete_evidence_packet_rejected
    {review : SubstrateCanaryEvidenceReview} :
    review.canaryPromoted = true ->
    (review.workloadRefPresent = false ∨
      review.baselineRefPresent = false ∨
        review.negativeControlPresent = false ∨
          review.resultReportPresent = false) ->
    ¬ CanaryPromotionEvidenceComplete review := by
  intro promoted missing valid
  unfold CanaryPromotionEvidenceComplete at valid
  have complete := valid promoted
  cases complete with
  | intro workloadPresent baselineAndRest =>
      cases baselineAndRest with
      | intro baselinePresent negativeAndReport =>
          cases negativeAndReport with
          | intro negativePresent reportPresent =>
              cases missing with
              | inl workloadMissing =>
                  rw [workloadMissing] at workloadPresent
                  contradiction
              | inr baselineOrRest =>
                  cases baselineOrRest with
                  | inl baselineMissing =>
                      rw [baselineMissing] at baselinePresent
                      contradiction
                  | inr negativeOrReport =>
                      cases negativeOrReport with
                      | inl negativeMissing =>
                          rw [negativeMissing] at negativePresent
                          contradiction
                      | inr reportMissing =>
                          rw [reportMissing] at reportPresent
                          contradiction

inductive TraceAdoptionState where
  | exploratory
  | structuralOnly
  | blocked
  | canary
  | qualified
  | retired
  | refuted
deriving DecidableEq, Repr

inductive AxisStatus where
  | planned
  | structuralOnly
  | unmeasured
  | measuredNegative
  | measuredPositive
deriving DecidableEq, Repr

inductive PermissionEffect where
  | planningOnly
  | diagnosticOnly
  | blocked
  | retired
  | canaryRouteAllowed
  | qualifiedRouteAllowed
deriving DecidableEq, Repr

inductive TraceRoute where
  | acceptExploratoryRegistration
  | acceptStructuralOnlyReceipt
  | acceptConsumerAxisBlocked
  | acceptNegativeControlRetirement
  | permitMeasuredCanary
  | permitMeasuredQualification
  | rejectMissingBaseline
  | rejectMissingFalsification
  | rejectIncompletePacket
  | rejectTheoremSpillover
  | rejectUnmeasuredAxisRouting
  | rejectFailedNegativeControlPromotion
  | rejectMissingFallback
  | rejectSupportPromotion
  | rejectMissingNonClaimBoundary
  | rejectIncompleteMeasuredEvidence
  | rejectIncoherentState
deriving DecidableEq, Repr

def TraceRoute.accepted : TraceRoute -> Bool
  | .acceptExploratoryRegistration
  | .acceptStructuralOnlyReceipt
  | .acceptConsumerAxisBlocked
  | .acceptNegativeControlRetirement
  | .permitMeasuredCanary
  | .permitMeasuredQualification => true
  | _ => false

def TraceRoute.permitsConsumer : TraceRoute -> Bool
  | .permitMeasuredCanary | .permitMeasuredQualification => true
  | _ => false

structure SubstrateAdoptionTraceInput where
  baselinePresent : Bool
  negativeControlPresent : Bool
  falsificationPresent : Bool
  proofBoundaryPresent : Bool
  fallbackPresent : Bool
  retirementPathPresent : Bool
  residualsPresent : Bool
  supportStateEffectNone : Bool
  chapterCoreEffectNone : Bool
  evidenceTransitionAbsent : Bool
  nonClaimBoundaryPresent : Bool
  workloadPresent : Bool
  resultReportPresent : Bool
  failedNegativeControl : Bool
  axisStatus : AxisStatus
  permissionEffect : PermissionEffect
  adoptionState : TraceAdoptionState
deriving DecidableEq, Repr

def classifyAdoptionTrace (input : SubstrateAdoptionTraceInput) : TraceRoute :=
  if ! input.baselinePresent then .rejectMissingBaseline
  else if ! input.falsificationPresent then .rejectMissingFalsification
  else if ! input.negativeControlPresent || ! input.proofBoundaryPresent ||
      ! input.retirementPathPresent || ! input.residualsPresent then
    .rejectIncompletePacket
  else if ! input.fallbackPresent then .rejectMissingFallback
  else if ! input.supportStateEffectNone || ! input.chapterCoreEffectNone ||
      ! input.evidenceTransitionAbsent then
    .rejectSupportPromotion
  else if ! input.nonClaimBoundaryPresent then .rejectMissingNonClaimBoundary
  else if input.failedNegativeControl && input.permissionEffect != .retired then
    .rejectFailedNegativeControlPromotion
  else if input.axisStatus = .structuralOnly &&
      input.permissionEffect = .qualifiedRouteAllowed then
    .rejectTheoremSpillover
  else if (input.axisStatus = .planned || input.axisStatus = .unmeasured ||
      input.axisStatus = .measuredNegative) &&
      (input.permissionEffect = .canaryRouteAllowed ||
        input.permissionEffect = .qualifiedRouteAllowed) then
    .rejectUnmeasuredAxisRouting
  else match input.permissionEffect with
  | .planningOnly =>
      if input.adoptionState = .exploratory then .acceptExploratoryRegistration
      else .rejectIncoherentState
  | .diagnosticOnly =>
      if input.axisStatus = .structuralOnly &&
          input.adoptionState = .structuralOnly then .acceptStructuralOnlyReceipt
      else .rejectIncoherentState
  | .blocked =>
      if input.adoptionState = .blocked then .acceptConsumerAxisBlocked
      else .rejectIncoherentState
  | .retired =>
      if input.failedNegativeControl &&
          (input.adoptionState = .retired || input.adoptionState = .refuted) then
        .acceptNegativeControlRetirement
      else .rejectIncoherentState
  | .canaryRouteAllowed =>
      if input.axisStatus = .measuredPositive && input.workloadPresent &&
          input.resultReportPresent && input.adoptionState = .canary then
        .permitMeasuredCanary
      else .rejectIncompleteMeasuredEvidence
  | .qualifiedRouteAllowed =>
      if input.axisStatus = .measuredPositive && input.workloadPresent &&
          input.resultReportPresent && input.adoptionState = .qualified then
        .permitMeasuredQualification
      else .rejectIncompleteMeasuredEvidence

theorem consumer_permission_routes_are_exact (route : TraceRoute) :
    route.permitsConsumer = true ↔
      route = .permitMeasuredCanary ∨ route = .permitMeasuredQualification := by
  cases route <;> decide

theorem rejection_routes_never_permit_a_consumer (route : TraceRoute)
    (rejected : route.accepted = false) :
    route.permitsConsumer = false := by
  cases route <;> simp_all [TraceRoute.accepted, TraceRoute.permitsConsumer]

def baseTraceInput : SubstrateAdoptionTraceInput :=
  { baselinePresent := true
    negativeControlPresent := true
    falsificationPresent := true
    proofBoundaryPresent := true
    fallbackPresent := true
    retirementPathPresent := true
    residualsPresent := true
    supportStateEffectNone := true
    chapterCoreEffectNone := true
    evidenceTransitionAbsent := true
    nonClaimBoundaryPresent := true
    workloadPresent := false
    resultReportPresent := false
    failedNegativeControl := false
    axisStatus := .planned
    permissionEffect := .planningOnly
    adoptionState := .exploratory }

def validExploratoryRegistration : SubstrateAdoptionTraceInput := baseTraceInput

def validStructuralOnlyReceipt : SubstrateAdoptionTraceInput :=
  { baseTraceInput with
    axisStatus := .structuralOnly
    permissionEffect := .diagnosticOnly
    adoptionState := .structuralOnly }

def validConsumerAxisBlocked : SubstrateAdoptionTraceInput :=
  { baseTraceInput with
    axisStatus := .unmeasured
    permissionEffect := .blocked
    adoptionState := .blocked }

def validNegativeControlRetirement : SubstrateAdoptionTraceInput :=
  { baseTraceInput with
    workloadPresent := true
    resultReportPresent := true
    failedNegativeControl := true
    axisStatus := .measuredNegative
    permissionEffect := .retired
    adoptionState := .refuted }

def invalidMissingBaseline : SubstrateAdoptionTraceInput :=
  { baseTraceInput with baselinePresent := false }

def invalidMissingFalsification : SubstrateAdoptionTraceInput :=
  { baseTraceInput with falsificationPresent := false }

def invalidTheoremSpillover : SubstrateAdoptionTraceInput :=
  { baseTraceInput with
    axisStatus := .structuralOnly
    permissionEffect := .qualifiedRouteAllowed
    adoptionState := .qualified }

def invalidUnmeasuredAxisRouting : SubstrateAdoptionTraceInput :=
  { baseTraceInput with
    axisStatus := .unmeasured
    permissionEffect := .canaryRouteAllowed
    adoptionState := .canary }

def invalidFailedNegativeControlPromotion : SubstrateAdoptionTraceInput :=
  { validNegativeControlRetirement with
    permissionEffect := .qualifiedRouteAllowed
    adoptionState := .qualified }

def invalidMissingFallback : SubstrateAdoptionTraceInput :=
  { baseTraceInput with
    workloadPresent := true
    resultReportPresent := true
    fallbackPresent := false
    axisStatus := .measuredPositive
    permissionEffect := .canaryRouteAllowed
    adoptionState := .canary }

def invalidSupportPromotion : SubstrateAdoptionTraceInput :=
  { validStructuralOnlyReceipt with supportStateEffectNone := false }

def invalidMissingNonClaimBoundary : SubstrateAdoptionTraceInput :=
  { validConsumerAxisBlocked with nonClaimBoundaryPresent := false }

theorem valid_exploratory_registration_route_derived :
    classifyAdoptionTrace validExploratoryRegistration =
      .acceptExploratoryRegistration := by decide

theorem valid_structural_only_receipt_route_derived :
    classifyAdoptionTrace validStructuralOnlyReceipt =
      .acceptStructuralOnlyReceipt := by decide

theorem valid_consumer_axis_blocked_route_derived :
    classifyAdoptionTrace validConsumerAxisBlocked =
      .acceptConsumerAxisBlocked := by decide

theorem valid_negative_control_retirement_route_derived :
    classifyAdoptionTrace validNegativeControlRetirement =
      .acceptNegativeControlRetirement := by decide

theorem invalid_missing_baseline_route_rejected :
    classifyAdoptionTrace invalidMissingBaseline = .rejectMissingBaseline := by decide

theorem invalid_missing_falsification_route_rejected :
    classifyAdoptionTrace invalidMissingFalsification =
      .rejectMissingFalsification := by decide

theorem invalid_theorem_spillover_route_rejected :
    classifyAdoptionTrace invalidTheoremSpillover = .rejectTheoremSpillover := by decide

theorem invalid_unmeasured_axis_route_rejected :
    classifyAdoptionTrace invalidUnmeasuredAxisRouting =
      .rejectUnmeasuredAxisRouting := by decide

theorem invalid_failed_negative_control_promotion_route_rejected :
    classifyAdoptionTrace invalidFailedNegativeControlPromotion =
      .rejectFailedNegativeControlPromotion := by decide

theorem invalid_missing_fallback_route_rejected :
    classifyAdoptionTrace invalidMissingFallback = .rejectMissingFallback := by decide

theorem invalid_support_promotion_route_rejected :
    classifyAdoptionTrace invalidSupportPromotion = .rejectSupportPromotion := by decide

theorem invalid_missing_non_claim_boundary_route_rejected :
    classifyAdoptionTrace invalidMissingNonClaimBoundary =
      .rejectMissingNonClaimBoundary := by decide

end AsiStackProofs.SearchSubstrates

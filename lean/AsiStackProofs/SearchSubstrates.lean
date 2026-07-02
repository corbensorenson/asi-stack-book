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

theorem substrate_adoption_record_includes_baseline_measured_target_and_falsification
    {record : SubstrateAdoptionRecord} :
    AdoptionFieldsComplete record ->
    record.baselineRefsPresent = true ∧
      record.measuredTargetDeclared = true ∧
        record.falsificationCriterionDeclared = true := by
  intro complete
  exact complete

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

theorem substrate_without_passing_evidence_remains_non_core
    {review : SubstratePromotionReview} :
    UnprovenSubstrateRemainsNonCore review ->
    review.passingEvidence = false ->
      NonCoreState review.adoptionState := by
  intro valid noEvidence
  exact valid noEvidence

theorem unproven_qualified_substrate_rejected
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

theorem qualified_substrate_requires_passing_evidence
    {review : SubstratePromotionReview} :
    CoreAdoptionValid review ->
    review.adoptionState = AdoptionState.qualified ->
      review.passingEvidence = true := by
  intro valid qualified
  exact valid qualified

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

structure SubstrateAdoptionTraceSummary where
  validTraceCount : Nat
  expectedInvalidControlCount : Nat
  exploratoryRegistrationPresent : Bool
  structuralOnlyReceiptPresent : Bool
  consumerAxisBlockedPresent : Bool
  negativeControlRetirementPresent : Bool
  missingBaselineRejected : Bool
  theoremSpilloverRejected : Bool
  failedNegativeControlPromotionRejected : Bool
  unmeasuredAxisAllowedRejected : Bool
  fallbackRequired : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def SubstrateAdoptionTraceValid
    (summary : SubstrateAdoptionTraceSummary) : Prop :=
  summary.validTraceCount = 4 ∧
    summary.expectedInvalidControlCount = 8 ∧
      summary.exploratoryRegistrationPresent = true ∧
        summary.structuralOnlyReceiptPresent = true ∧
          summary.consumerAxisBlockedPresent = true ∧
            summary.negativeControlRetirementPresent = true ∧
              summary.missingBaselineRejected = true ∧
                summary.theoremSpilloverRejected = true ∧
                  summary.failedNegativeControlPromotionRejected = true ∧
                    summary.unmeasuredAxisAllowedRejected = true ∧
                      summary.fallbackRequired = true ∧
                        summary.supportStateEffectNone = true ∧
                          summary.nonClaimBoundary = true

def substrateAdoptionTraceFixture : SubstrateAdoptionTraceSummary := {
  validTraceCount := 4
  expectedInvalidControlCount := 8
  exploratoryRegistrationPresent := true
  structuralOnlyReceiptPresent := true
  consumerAxisBlockedPresent := true
  negativeControlRetirementPresent := true
  missingBaselineRejected := true
  theoremSpilloverRejected := true
  failedNegativeControlPromotionRejected := true
  unmeasuredAxisAllowedRejected := true
  fallbackRequired := true
  supportStateEffectNone := true
  nonClaimBoundary := true
}

theorem substrate_adoption_trace_fixture_valid :
    SubstrateAdoptionTraceValid substrateAdoptionTraceFixture := by
  unfold SubstrateAdoptionTraceValid substrateAdoptionTraceFixture
  simp

theorem substrate_adoption_trace_rejects_axis_laundering
    {summary : SubstrateAdoptionTraceSummary} :
    SubstrateAdoptionTraceValid summary ->
      summary.theoremSpilloverRejected = true ∧
        summary.unmeasuredAxisAllowedRejected = true := by
  intro valid
  unfold SubstrateAdoptionTraceValid at valid
  rcases valid with ⟨_,
    _,
    _,
    _,
    _,
    _,
    _,
    theoremSpilloverRejected,
    _,
    unmeasuredAxisAllowedRejected,
    _,
    _,
    _⟩
  exact ⟨theoremSpilloverRejected, unmeasuredAxisAllowedRejected⟩

theorem substrate_adoption_trace_preserves_no_promotion_boundary
    {summary : SubstrateAdoptionTraceSummary} :
    SubstrateAdoptionTraceValid summary ->
      summary.failedNegativeControlPromotionRejected = true ∧
        summary.fallbackRequired = true ∧
          summary.supportStateEffectNone = true ∧
            summary.nonClaimBoundary = true := by
  intro valid
  unfold SubstrateAdoptionTraceValid at valid
  rcases valid with ⟨_,
    _,
    _,
    _,
    _,
    _,
    _,
    _,
    failedNegativeControlPromotionRejected,
    _,
    fallbackRequired,
    supportStateEffectNone,
    nonClaimBoundary⟩
  exact ⟨failedNegativeControlPromotionRejected,
    fallbackRequired,
    supportStateEffectNone,
    nonClaimBoundary⟩

end AsiStackProofs.SearchSubstrates

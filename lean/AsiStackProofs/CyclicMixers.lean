namespace AsiStackProofs.CyclicMixers

structure CyclicMixerClaimReview where
  structuralInvariantRecorded : Bool
  qualityClaimSeparate : Bool
  runtimeClaimSeparate : Bool
  memoryClaimSeparate : Bool
  parameterClaimSeparate : Bool
deriving DecidableEq, Repr

def StructuralClaimSeparated (review : CyclicMixerClaimReview) : Prop :=
  review.structuralInvariantRecorded = true ∧
    review.qualityClaimSeparate = true ∧
      review.runtimeClaimSeparate = true ∧
        review.memoryClaimSeparate = true ∧
          review.parameterClaimSeparate = true

theorem cyclic_mixer_claim_records_structure_separately_from_quality_runtime_memory_and_parameters
    {review : CyclicMixerClaimReview} :
    StructuralClaimSeparated review ->
    review.structuralInvariantRecorded = true ∧
      review.qualityClaimSeparate = true ∧
        review.runtimeClaimSeparate = true ∧
          review.memoryClaimSeparate = true ∧
            review.parameterClaimSeparate = true := by
  intro separated
  exact separated

theorem cyclic_mixer_claim_missing_claim_partition_rejected
    {review : CyclicMixerClaimReview} :
    (review.structuralInvariantRecorded = false ∨
      review.qualityClaimSeparate = false ∨
        review.runtimeClaimSeparate = false ∨
          review.memoryClaimSeparate = false ∨
            review.parameterClaimSeparate = false) ->
    ¬ StructuralClaimSeparated review := by
  intro missing separated
  unfold StructuralClaimSeparated at separated
  cases separated with
  | intro structureRecorded qualityAndRest =>
      cases qualityAndRest with
      | intro qualitySeparate runtimeAndRest =>
          cases runtimeAndRest with
          | intro runtimeSeparate memoryAndParameter =>
              cases memoryAndParameter with
              | intro memorySeparate parameterSeparate =>
                  cases missing with
                  | inl structureMissing =>
                      rw [structureMissing] at structureRecorded
                      contradiction
                  | inr qualityOrRest =>
                      cases qualityOrRest with
                      | inl qualityMissing =>
                          rw [qualityMissing] at qualitySeparate
                          contradiction
                      | inr runtimeOrRest =>
                          cases runtimeOrRest with
                          | inl runtimeMissing =>
                              rw [runtimeMissing] at runtimeSeparate
                              contradiction
                          | inr memoryOrParameter =>
                              cases memoryOrParameter with
                              | inl memoryMissing =>
                                  rw [memoryMissing] at memorySeparate
                                  contradiction
                              | inr parameterMissing =>
                                  rw [parameterMissing] at parameterSeparate
                                  contradiction

structure CyclicSubstratePromotionReview where
  baselineRefsPresent : Bool
  tradeoffMetricsRecorded : Bool
  substratePromoted : Bool
deriving DecidableEq, Repr

def BaselinesAndTradeoffsRequired (review : CyclicSubstratePromotionReview) : Prop :=
  review.substratePromoted = true ->
    review.baselineRefsPresent = true ∧
      review.tradeoffMetricsRecorded = true

theorem cyclic_substrate_promotion_requires_baselines_and_tradeoff_metrics
    {review : CyclicSubstratePromotionReview} :
    BaselinesAndTradeoffsRequired review ->
    review.substratePromoted = true ->
    review.baselineRefsPresent = true ∧
      review.tradeoffMetricsRecorded = true := by
  intro valid promoted
  exact valid promoted

theorem cyclic_substrate_promotion_without_baselines_or_tradeoffs_rejected
    {review : CyclicSubstratePromotionReview} :
    review.substratePromoted = true ->
    (review.baselineRefsPresent = false ∨
      review.tradeoffMetricsRecorded = false) ->
    ¬ BaselinesAndTradeoffsRequired review := by
  intro promoted missing valid
  unfold BaselinesAndTradeoffsRequired at valid
  have required := valid promoted
  cases required with
  | intro baselinesPresent tradeoffsPresent =>
      cases missing with
      | inl baselinesMissing =>
          rw [baselinesMissing] at baselinesPresent
          contradiction
      | inr tradeoffsMissing =>
          rw [tradeoffsMissing] at tradeoffsPresent
          contradiction

structure CyclicAliasDiagnosticReview where
  adoptionCandidate : Bool
  cyclicSlotOrPhaseReused : Bool
  residueRecorded : Bool
  windingRecorded : Bool
  aliasResidualVisible : Bool
deriving DecidableEq, Repr

def CyclicAliasDiagnosticValid
    (review : CyclicAliasDiagnosticReview) : Prop :=
  review.adoptionCandidate = true ->
    review.cyclicSlotOrPhaseReused = true ->
      (review.residueRecorded = true ∧ review.windingRecorded = true) ∨
        review.aliasResidualVisible = true

theorem cyclic_alias_diagnostic_without_winding_or_visible_residual_rejected
    {review : CyclicAliasDiagnosticReview} :
    review.adoptionCandidate = true ->
    review.cyclicSlotOrPhaseReused = true ->
    (review.residueRecorded = false ∨ review.windingRecorded = false) ->
    review.aliasResidualVisible = false ->
    ¬ CyclicAliasDiagnosticValid review := by
  intro candidate reused missing residualHidden valid
  unfold CyclicAliasDiagnosticValid at valid
  have boundary := valid candidate reused
  cases boundary with
  | inl structureRecorded =>
      cases structureRecorded with
      | intro residuePresent windingPresent =>
          cases missing with
          | inl residueMissing =>
              rw [residueMissing] at residuePresent
              contradiction
          | inr windingMissing =>
              rw [windingMissing] at windingPresent
              contradiction
  | inr residualVisible =>
      rw [residualHidden] at residualVisible
      contradiction

structure CyclicTradeoffPacketReview where
  adoptionCandidate : Bool
  structuralReceiptPresent : Bool
  baselineMatrixPresent : Bool
  resourceCostsRecorded : Bool
  metricsRecorded : Bool
  tradeoffPacketPresent : Bool
deriving DecidableEq, Repr

def CyclicTradeoffPacketValid
    (review : CyclicTradeoffPacketReview) : Prop :=
  review.adoptionCandidate = true ->
    review.structuralReceiptPresent = true ∧
      review.baselineMatrixPresent = true ∧
        review.resourceCostsRecorded = true ∧
          review.metricsRecorded = true ∧
            review.tradeoffPacketPresent = true

theorem cyclic_adoption_without_complete_tradeoff_packet_rejected
    {review : CyclicTradeoffPacketReview} :
    review.adoptionCandidate = true ->
    (review.structuralReceiptPresent = false ∨
      review.baselineMatrixPresent = false ∨
        review.resourceCostsRecorded = false ∨
          review.metricsRecorded = false ∨
            review.tradeoffPacketPresent = false) ->
    ¬ CyclicTradeoffPacketValid review := by
  intro candidate missing valid
  unfold CyclicTradeoffPacketValid at valid
  have complete := valid candidate
  cases complete with
  | intro receiptPresent baselineAndRest =>
      cases baselineAndRest with
      | intro baselinePresent resourceAndRest =>
          cases resourceAndRest with
          | intro resourcePresent metricsAndPacket =>
              cases metricsAndPacket with
              | intro metricsPresent packetPresent =>
                  cases missing with
                  | inl receiptMissing =>
                      rw [receiptMissing] at receiptPresent
                      contradiction
                  | inr baselineOrRest =>
                      cases baselineOrRest with
                      | inl baselineMissing =>
                          rw [baselineMissing] at baselinePresent
                          contradiction
                      | inr resourceOrRest =>
                          cases resourceOrRest with
                          | inl resourceMissing =>
                              rw [resourceMissing] at resourcePresent
                              contradiction
                          | inr metricsOrPacket =>
                              cases metricsOrPacket with
                              | inl metricsMissing =>
                                  rw [metricsMissing] at metricsPresent
                                  contradiction
                              | inr packetMissing =>
                                  rw [packetMissing] at packetPresent
                                  contradiction

structure CyclicHardwareBoundaryReview where
  adoptionCandidate : Bool
  hardwareMismatchReported : Bool
  hardwareRefusalPathPresent : Bool
deriving DecidableEq, Repr

def CyclicHardwareBoundaryValid
    (review : CyclicHardwareBoundaryReview) : Prop :=
  review.adoptionCandidate = true ->
    review.hardwareMismatchReported = true ->
      review.hardwareRefusalPathPresent = true

theorem hardware_mismatch_without_refusal_path_rejected
    {review : CyclicHardwareBoundaryReview} :
    review.adoptionCandidate = true ->
    review.hardwareMismatchReported = true ->
    review.hardwareRefusalPathPresent = false ->
    ¬ CyclicHardwareBoundaryValid review := by
  intro candidate mismatch missingRefusal valid
  unfold CyclicHardwareBoundaryValid at valid
  have refusalPath := valid candidate mismatch
  rw [missingRefusal] at refusalPath
  contradiction

end AsiStackProofs.CyclicMixers

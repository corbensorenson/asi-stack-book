namespace AsiStackProofs.CoilAttentionMemory

structure CyclicMemoryAliasReview where
  cyclicSlotReused : Bool
  residueRecorded : Bool
  windingRecorded : Bool
  aliasResidualVisible : Bool
deriving DecidableEq, Repr

def AliasBoundaryValid (review : CyclicMemoryAliasReview) : Prop :=
  review.cyclicSlotReused = true ->
    (review.residueRecorded = true ∧ review.windingRecorded = true) ∨
      review.aliasResidualVisible = true

theorem cyclic_memory_claim_records_residue_and_winding_or_visible_alias_residual
    {review : CyclicMemoryAliasReview} :
    AliasBoundaryValid review ->
    review.cyclicSlotReused = true ->
    (review.residueRecorded = true ∧ review.windingRecorded = true) ∨
      review.aliasResidualVisible = true := by
  intro valid reused
  exact valid reused

theorem reused_cyclic_slot_without_winding_or_residual_rejected
    {review : CyclicMemoryAliasReview} :
    review.cyclicSlotReused = true ->
    (review.residueRecorded = false ∨ review.windingRecorded = false) ->
    review.aliasResidualVisible = false ->
    ¬ AliasBoundaryValid review := by
  intro reused missingStructure residualHidden valid
  unfold AliasBoundaryValid at valid
  have boundary := valid reused
  cases boundary with
  | inl structureRecorded =>
      cases structureRecorded with
      | intro residuePresent windingPresent =>
          cases missingStructure with
          | inl residueMissing =>
              rw [residueMissing] at residuePresent
              contradiction
          | inr windingMissing =>
              rw [windingMissing] at windingPresent
              contradiction
  | inr residualVisible =>
      rw [residualHidden] at residualVisible
      contradiction

structure RetrievalQualityPromotionReview where
  sparseCoverageFact : Bool
  freshnessFact : Bool
  semanticQualityEvidence : Bool
  retrievalQualityPromoted : Bool
deriving DecidableEq, Repr

def CoverageFreshnessAloneBlocksQualityPromotion
    (review : RetrievalQualityPromotionReview) : Prop :=
  review.sparseCoverageFact = true ->
    review.freshnessFact = true ->
      review.semanticQualityEvidence = false ->
        review.retrievalQualityPromoted = false

theorem sparse_coverage_or_freshness_alone_cannot_promote_retrieval_quality
    {review : RetrievalQualityPromotionReview} :
    CoverageFreshnessAloneBlocksQualityPromotion review ->
    review.sparseCoverageFact = true ->
    review.freshnessFact = true ->
    review.semanticQualityEvidence = false ->
    review.retrievalQualityPromoted = false := by
  intro valid sparse fresh noQualityEvidence
  exact valid sparse fresh noQualityEvidence

theorem structure_only_retrieval_quality_promotion_rejected
    {review : RetrievalQualityPromotionReview} :
    review.sparseCoverageFact = true ->
    review.freshnessFact = true ->
    review.semanticQualityEvidence = false ->
    review.retrievalQualityPromoted = true ->
    ¬ CoverageFreshnessAloneBlocksQualityPromotion review := by
  intro sparse fresh noQualityEvidence promoted valid
  unfold CoverageFreshnessAloneBlocksQualityPromotion at valid
  have blocked := valid sparse fresh noQualityEvidence
  rw [promoted] at blocked
  contradiction

structure RecurrenceAdmissionReview where
  recurrenceEnabled : Bool
  workBudgetRecorded : Bool
  exitConditionRecorded : Bool
  fallbackRecorded : Bool
deriving DecidableEq, Repr

def RecurrenceAdmissionValid (review : RecurrenceAdmissionReview) : Prop :=
  review.recurrenceEnabled = true ->
    review.workBudgetRecorded = true ∧
      review.exitConditionRecorded = true ∧
        review.fallbackRecorded = true

theorem recurrence_without_budget_exit_or_fallback_rejected
    {review : RecurrenceAdmissionReview} :
    review.recurrenceEnabled = true ->
    (review.workBudgetRecorded = false ∨
      review.exitConditionRecorded = false ∨
        review.fallbackRecorded = false) ->
    ¬ RecurrenceAdmissionValid review := by
  intro enabled missing valid
  unfold RecurrenceAdmissionValid at valid
  have recorded := valid enabled
  cases recorded with
  | intro budgetRecorded exitAndFallback =>
      cases exitAndFallback with
      | intro exitRecorded fallbackRecorded =>
          cases missing with
          | inl budgetMissing =>
              rw [budgetMissing] at budgetRecorded
              contradiction
          | inr exitOrFallback =>
              cases exitOrFallback with
              | inl exitMissing =>
                  rw [exitMissing] at exitRecorded
                  contradiction
              | inr fallbackMissing =>
                  rw [fallbackMissing] at fallbackRecorded
                  contradiction

structure FreshnessAdmissionReview where
  staleReadDetected : Bool
  admittedAsFresh : Bool
  residualEscrowRecorded : Bool
deriving DecidableEq, Repr

def StaleReadAdmissionValid (review : FreshnessAdmissionReview) : Prop :=
  review.staleReadDetected = true ->
    review.admittedAsFresh = true ->
      review.residualEscrowRecorded = true

theorem stale_read_admitted_as_fresh_without_residual_rejected
    {review : FreshnessAdmissionReview} :
    review.staleReadDetected = true ->
    review.admittedAsFresh = true ->
    review.residualEscrowRecorded = false ->
    ¬ StaleReadAdmissionValid review := by
  intro stale admitted missingResidual valid
  unfold StaleReadAdmissionValid at valid
  have residual := valid stale admitted
  rw [missingResidual] at residual
  contradiction

end AsiStackProofs.CoilAttentionMemory

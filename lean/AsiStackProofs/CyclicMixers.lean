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

inductive CyclicCandidateStage where
  | proposed
  | structureCertified
  | baselineBound
  | tradeoffsRecorded
  | hardwareQualified
  | canaryEligible
  | retired
deriving DecidableEq, Repr

structure CyclicCandidateState where
  stage : CyclicCandidateStage := .proposed
  candidateDigest : Nat := 101
  expectedCandidateDigest : Nat := 101
  workloadDigest : Nat := 202
  expectedWorkloadDigest : Nat := 202
  baselineDigest : Nat := 303
  expectedBaselineDigest : Nat := 303
  tradeoffDigest : Nat := 404
  expectedTradeoffDigest : Nat := 404
  hardwareDigest : Nat := 505
  expectedHardwareDigest : Nat := 505
  structuralReceiptBound : Bool := false
  baselineMatrixBound : Bool := false
  tradeoffMetricsBound : Bool := false
  hardwareRouteBound : Bool := false
  fallbackReady : Bool := false
  receipts : Nat := 0
  authorityCeiling : Nat := 2
  supportAssignments : Nat := 0
  externalEffects : Nat := 0
deriving DecidableEq, Repr

inductive CyclicCandidateEvent where
  | certifyStructure (candidateDigest : Nat) (receiptValid : Bool)
  | bindBaselines (candidateDigest workloadDigest baselineDigest : Nat)
      (baselineMatrixComplete : Bool)
  | recordTradeoffs (candidateDigest tradeoffDigest : Nat)
      (quality runtime memory parameters : Bool)
  | qualifyHardware (candidateDigest hardwareDigest : Nat)
      (kernelAvailable refusalPathPresent : Bool)
  | admitCanary (candidateDigest baselineDigest tradeoffDigest hardwareDigest : Nat)
      (fallbackPrepared : Bool)
  | reportRegression (candidateDigest : Nat) (fallbackApplied : Bool)
  | retire (candidateDigest : Nat) (residualOwned : Bool)
deriving DecidableEq, Repr

def cyclicCandidateStep
    (state : CyclicCandidateState) (event : CyclicCandidateEvent) :
    Bool × CyclicCandidateState :=
  match event with
  | .certifyStructure candidate receiptValid =>
      if state.stage = .proposed ∧
          candidate = state.candidateDigest ∧
          state.candidateDigest = state.expectedCandidateDigest ∧
          receiptValid = true then
        (true, { state with
          stage := .structureCertified
          structuralReceiptBound := true
          receipts := state.receipts + 1 })
      else (false, state)
  | .bindBaselines candidate workload baseline matrixComplete =>
      if state.stage = .structureCertified ∧
          candidate = state.candidateDigest ∧
          workload = state.workloadDigest ∧
          state.workloadDigest = state.expectedWorkloadDigest ∧
          baseline = state.baselineDigest ∧
          state.baselineDigest = state.expectedBaselineDigest ∧
          matrixComplete = true then
        (true, { state with
          stage := .baselineBound
          baselineMatrixBound := true
          receipts := state.receipts + 1 })
      else (false, state)
  | .recordTradeoffs candidate tradeoff quality runtime memory parameters =>
      if state.stage = .baselineBound ∧
          candidate = state.candidateDigest ∧
          tradeoff = state.tradeoffDigest ∧
          state.tradeoffDigest = state.expectedTradeoffDigest ∧
          quality = true ∧ runtime = true ∧ memory = true ∧ parameters = true then
        (true, { state with
          stage := .tradeoffsRecorded
          tradeoffMetricsBound := true
          receipts := state.receipts + 1 })
      else (false, state)
  | .qualifyHardware candidate hardware kernelAvailable refusalPathPresent =>
      if state.stage = .tradeoffsRecorded ∧
          candidate = state.candidateDigest ∧
          hardware = state.hardwareDigest ∧
          state.hardwareDigest = state.expectedHardwareDigest ∧
          (kernelAvailable = true ∨ refusalPathPresent = true) then
        (true, { state with
          stage := .hardwareQualified
          hardwareRouteBound := true
          receipts := state.receipts + 1 })
      else (false, state)
  | .admitCanary candidate baseline tradeoff hardware fallbackPrepared =>
      if state.stage = .hardwareQualified ∧
          candidate = state.candidateDigest ∧
          baseline = state.baselineDigest ∧
          tradeoff = state.tradeoffDigest ∧
          hardware = state.hardwareDigest ∧
          state.structuralReceiptBound = true ∧
          state.baselineMatrixBound = true ∧
          state.tradeoffMetricsBound = true ∧
          state.hardwareRouteBound = true ∧
          fallbackPrepared = true then
        (true, { state with
          stage := .canaryEligible
          fallbackReady := true
          receipts := state.receipts + 1 })
      else (false, state)
  | .reportRegression candidate fallbackApplied =>
      if state.stage = .canaryEligible ∧
          candidate = state.candidateDigest ∧
          state.fallbackReady = true ∧
          fallbackApplied = true then
        (true, { state with stage := .retired, receipts := state.receipts + 1 })
      else (false, state)
  | .retire candidate residualOwned =>
      if state.stage ≠ .retired ∧
          candidate = state.candidateDigest ∧ residualOwned = true then
        (true, { state with stage := .retired, receipts := state.receipts + 1 })
      else (false, state)

def runCyclicCandidate
    (state : CyclicCandidateState) (events : List CyclicCandidateEvent) :
    CyclicCandidateState :=
  events.foldl (fun current event => (cyclicCandidateStep current event).2) state

def CyclicCandidateCustody
    (before after : CyclicCandidateState) : Prop :=
  after.candidateDigest = before.candidateDigest ∧
    after.expectedCandidateDigest = before.expectedCandidateDigest ∧
    after.workloadDigest = before.workloadDigest ∧
    after.expectedWorkloadDigest = before.expectedWorkloadDigest ∧
    after.baselineDigest = before.baselineDigest ∧
    after.expectedBaselineDigest = before.expectedBaselineDigest ∧
    after.tradeoffDigest = before.tradeoffDigest ∧
    after.expectedTradeoffDigest = before.expectedTradeoffDigest ∧
    after.hardwareDigest = before.hardwareDigest ∧
    after.expectedHardwareDigest = before.expectedHardwareDigest ∧
    after.authorityCeiling = before.authorityCeiling ∧
    after.supportAssignments = before.supportAssignments ∧
    after.externalEffects = before.externalEffects

def CyclicCandidateInvariant (state : CyclicCandidateState) : Prop :=
  state.supportAssignments = 0 ∧
    state.externalEffects = 0 ∧
    (state.stage = .structureCertified -> state.structuralReceiptBound = true) ∧
    (state.stage = .baselineBound ->
      state.structuralReceiptBound = true ∧ state.baselineMatrixBound = true) ∧
    (state.stage = .tradeoffsRecorded ->
      state.structuralReceiptBound = true ∧ state.baselineMatrixBound = true ∧
        state.tradeoffMetricsBound = true) ∧
    (state.stage = .hardwareQualified ->
      state.structuralReceiptBound = true ∧ state.baselineMatrixBound = true ∧
        state.tradeoffMetricsBound = true ∧ state.hardwareRouteBound = true) ∧
    (state.stage = .canaryEligible ->
      state.structuralReceiptBound = true ∧ state.baselineMatrixBound = true ∧
        state.tradeoffMetricsBound = true ∧ state.hardwareRouteBound = true ∧
          state.fallbackReady = true)

def referenceCyclicCandidate : CyclicCandidateState := {}

def referenceCyclicCandidateEvents : List CyclicCandidateEvent := [
  .certifyStructure 101 true,
  .bindBaselines 101 202 303 true,
  .recordTradeoffs 101 404 true true true true,
  .qualifyHardware 101 505 true false,
  .admitCanary 101 303 404 505 true
]

theorem cyclic_candidate_rejected_event_is_noninterfering
    (state : CyclicCandidateState) (event : CyclicCandidateEvent)
    (h : (cyclicCandidateStep state event).1 = false) :
    (cyclicCandidateStep state event).2 = state := by
  cases event <;> simp [cyclicCandidateStep] at h ⊢ <;>
    repeat' first | split | simp_all

theorem cyclic_candidate_step_preserves_custody
    (state : CyclicCandidateState) (event : CyclicCandidateEvent) :
    CyclicCandidateCustody state (cyclicCandidateStep state event).2 := by
  cases event <;> simp [CyclicCandidateCustody, cyclicCandidateStep] <;>
    repeat' first | split | simp_all

theorem cyclic_candidate_custody_transitive
    {initial middle final : CyclicCandidateState}
    (h₁ : CyclicCandidateCustody initial middle)
    (h₂ : CyclicCandidateCustody middle final) :
    CyclicCandidateCustody initial final := by
  unfold CyclicCandidateCustody at *
  rcases h₁ with ⟨h₁a, h₁b, h₁c, h₁d, h₁e, h₁f, h₁g, h₁h, h₁i, h₁j,
    h₁k, h₁l, h₁m⟩
  rcases h₂ with ⟨h₂a, h₂b, h₂c, h₂d, h₂e, h₂f, h₂g, h₂h, h₂i, h₂j,
    h₂k, h₂l, h₂m⟩
  exact ⟨h₂a.trans h₁a, h₂b.trans h₁b, h₂c.trans h₁c,
    h₂d.trans h₁d, h₂e.trans h₁e, h₂f.trans h₁f, h₂g.trans h₁g,
    h₂h.trans h₁h, h₂i.trans h₁i, h₂j.trans h₁j, h₂k.trans h₁k,
    h₂l.trans h₁l, h₂m.trans h₁m⟩

theorem run_cyclic_candidate_preserves_custody
    (state : CyclicCandidateState) (events : List CyclicCandidateEvent) :
    CyclicCandidateCustody state (runCyclicCandidate state events) := by
  induction events generalizing state with
  | nil => simp [runCyclicCandidate, CyclicCandidateCustody]
  | cons event rest ih =>
      exact cyclic_candidate_custody_transitive
        (cyclic_candidate_step_preserves_custody state event)
        (ih (cyclicCandidateStep state event).2)

theorem cyclic_candidate_step_preserves_invariant
    (state : CyclicCandidateState) (event : CyclicCandidateEvent)
    (h : CyclicCandidateInvariant state) :
    CyclicCandidateInvariant (cyclicCandidateStep state event).2 := by
  cases event <;>
    simp [CyclicCandidateInvariant, cyclicCandidateStep] at * <;>
    repeat' first | split | simp_all

theorem run_cyclic_candidate_preserves_invariant
    (state : CyclicCandidateState) (events : List CyclicCandidateEvent)
    (h : CyclicCandidateInvariant state) :
    CyclicCandidateInvariant (runCyclicCandidate state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (cyclicCandidateStep state event).2
        (cyclic_candidate_step_preserves_invariant state event h)

theorem run_cyclic_candidate_append
    (state : CyclicCandidateState)
    (left right : List CyclicCandidateEvent) :
    runCyclicCandidate state (left ++ right) =
      runCyclicCandidate (runCyclicCandidate state left) right := by
  simp [runCyclicCandidate, List.foldl_append]

theorem reference_cyclic_candidate_reaches_canary_eligibility :
    (runCyclicCandidate referenceCyclicCandidate referenceCyclicCandidateEvents).stage =
      .canaryEligible := by
  decide

theorem reference_cyclic_candidate_preserves_zero_authority :
    let final := runCyclicCandidate referenceCyclicCandidate referenceCyclicCandidateEvents
    final.authorityCeiling = 2 ∧ final.supportAssignments = 0 ∧
      final.externalEffects = 0 ∧ final.receipts = 5 := by
  decide

theorem reference_regression_retires_through_fallback :
    let eligible := runCyclicCandidate referenceCyclicCandidate referenceCyclicCandidateEvents
    (cyclicCandidateStep eligible (.reportRegression 101 true)).2.stage = .retired := by
  decide

theorem missing_baseline_matrix_rejects_without_state_change :
    let certified := (cyclicCandidateStep referenceCyclicCandidate
      (.certifyStructure 101 true)).2
    cyclicCandidateStep certified (.bindBaselines 101 202 303 false) =
      (false, certified) := by
  decide

theorem incomplete_tradeoff_partition_rejects_without_state_change :
    let baselineBound := runCyclicCandidate referenceCyclicCandidate
      (referenceCyclicCandidateEvents.take 2)
    cyclicCandidateStep baselineBound
      (.recordTradeoffs 101 404 true true false true) = (false, baselineBound) := by
  decide

theorem hardware_mismatch_without_refusal_rejects_without_state_change :
    let measured := runCyclicCandidate referenceCyclicCandidate
      (referenceCyclicCandidateEvents.take 3)
    cyclicCandidateStep measured (.qualifyHardware 101 505 false false) =
      (false, measured) := by
  decide

theorem canary_admission_without_fallback_rejects_without_state_change :
    let qualified := runCyclicCandidate referenceCyclicCandidate
      (referenceCyclicCandidateEvents.take 4)
    cyclicCandidateStep qualified (.admitCanary 101 303 404 505 false) =
      (false, qualified) := by
  decide

theorem retired_candidate_is_absorbing_one_step
    (state : CyclicCandidateState) (event : CyclicCandidateEvent)
    (h : state.stage = .retired) :
    (cyclicCandidateStep state event).2 = state := by
  cases event <;> simp [cyclicCandidateStep, h] <;>
    repeat' first | split | simp_all

theorem retired_candidate_is_absorbing_for_any_suffix
    (state : CyclicCandidateState) (events : List CyclicCandidateEvent)
    (h : state.stage = .retired) :
    runCyclicCandidate state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      rw [show runCyclicCandidate state (event :: rest) =
        runCyclicCandidate (cyclicCandidateStep state event).2 rest by rfl]
      rw [retired_candidate_is_absorbing_one_step state event h]
      exact ih state h

def cyclicStructuralSummary (state : CyclicCandidateState) : Nat × Bool :=
  (state.candidateDigest, state.structuralReceiptBound)

def CanaryAdmissible (state : CyclicCandidateState) : Prop :=
  state.stage = .hardwareQualified ∧
    state.structuralReceiptBound = true ∧
    state.baselineMatrixBound = true ∧
    state.tradeoffMetricsBound = true ∧
    state.hardwareRouteBound = true

def fullyQualifiedCyclicCandidate : CyclicCandidateState :=
  runCyclicCandidate referenceCyclicCandidate (referenceCyclicCandidateEvents.take 4)

def structurallyOnlyCyclicCandidate : CyclicCandidateState :=
  (cyclicCandidateStep referenceCyclicCandidate (.certifyStructure 101 true)).2

theorem structural_summary_collides_across_canary_eligibility :
    cyclicStructuralSummary fullyQualifiedCyclicCandidate =
        cyclicStructuralSummary structurallyOnlyCyclicCandidate ∧
      CanaryAdmissible fullyQualifiedCyclicCandidate ∧
      ¬ CanaryAdmissible structurallyOnlyCyclicCandidate := by
  simp [cyclicStructuralSummary, fullyQualifiedCyclicCandidate,
    structurallyOnlyCyclicCandidate, CanaryAdmissible, runCyclicCandidate,
    referenceCyclicCandidateEvents, referenceCyclicCandidate,
    cyclicCandidateStep]

theorem no_structural_summary_classifier_recovers_canary_eligibility :
    ¬ ∃ classify : Nat × Bool -> Bool,
      ∀ state : CyclicCandidateState,
        classify (cyclicStructuralSummary state) = true ↔ CanaryAdmissible state := by
  intro proposed
  rcases proposed with ⟨classify, exact⟩
  have collision := structural_summary_collides_across_canary_eligibility
  have eligible := (exact fullyQualifiedCyclicCandidate).2 collision.2.1
  have ineligible := (exact structurallyOnlyCyclicCandidate).1
  rw [collision.1] at eligible
  exact collision.2.2 (ineligible eligible)

end AsiStackProofs.CyclicMixers

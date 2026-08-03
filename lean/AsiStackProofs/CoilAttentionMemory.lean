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

/-! ## Versioned cyclic-memory and bounded-recurrence lifecycle

This model covers authored finite address, freshness, fallback, and recurrence
semantics. It does not establish that a deployed cache reports true epochs or
positions, that recurrence is useful, or that retrieval quality improves.
-/

structure CyclicAddress where
  residue : Nat
  winding : Nat
deriving DecidableEq, Repr

def residueOnly (address : CyclicAddress) : Nat := address.residue

def addressZero : CyclicAddress := { residue := 7, winding := 0 }
def addressOne : CyclicAddress := { residue := 7, winding := 1 }

theorem residue_collision_addresses_are_distinct : addressZero ≠ addressOne := by
  decide

theorem residue_only_projection_collides :
    residueOnly addressZero = residueOnly addressOne := by rfl

theorem residue_only_projection_is_not_injective :
    ¬ Function.Injective residueOnly := by
  intro injective
  exact residue_collision_addresses_are_distinct
    (injective residue_only_projection_collides)

theorem no_residue_only_decoder_recovers_every_cyclic_address :
    ¬ ∃ decode : Nat -> CyclicAddress,
      ∀ address : CyclicAddress, decode (residueOnly address) = address := by
  rintro ⟨decode, recovers⟩
  have zeroRecovered := recovers addressZero
  have oneRecovered := recovers addressOne
  rw [residue_only_projection_collides] at zeroRecovered
  exact residue_collision_addresses_are_distinct (zeroRecovered.symm.trans oneRecovered)

def completeAddressEncode (address : CyclicAddress) : Nat × Nat :=
  (address.residue, address.winding)

def completeAddressDecode (encoded : Nat × Nat) : CyclicAddress :=
  { residue := encoded.1, winding := encoded.2 }

theorem complete_address_encoding_round_trips (address : CyclicAddress) :
    completeAddressDecode (completeAddressEncode address) = address := by
  cases address
  rfl

theorem complete_address_encoding_is_injective :
    Function.Injective completeAddressEncode := by
  exact Function.LeftInverse.injective complete_address_encoding_round_trips

inductive MemoryLifecycleStage where
  | written
  | readRequested
  | freshValidated
  | staleDetected
  | consumed
  | fallback
  | recurring
  | closed
deriving DecidableEq, Repr

inductive MemoryLifecycleEvent where
  | requestRead
  | classifyRead
  | consumeFresh
  | useFallback
  | startRecurrence
  | recur
  | exitRecurrence
  | close
deriving DecidableEq, Repr

inductive MemoryLifecycleRoute where
  | accepted
  | rejectStage
  | rejectStale
  | rejectBudget
deriving DecidableEq, Repr

structure MemoryLifecycleState where
  stage : MemoryLifecycleStage := .written
  memoryDigest : Nat := 5201
  requestDigest : Nat := 5202
  slotEpoch : Nat := 31
  requestedEpoch : Nat := 31
  slotResidue : Nat := 7
  requestedResidue : Nat := 7
  slotWinding : Nat := 4
  requestedWinding : Nat := 4
  recurrenceBudget : Nat := 2
  recurrenceSteps : Nat := 0
  supportAssignments : Nat := 0
  externalEffects : Nat := 0
deriving DecidableEq, Repr

def MemoryCustodyPreserved
    (before after : MemoryLifecycleState) : Prop :=
  after.memoryDigest = before.memoryDigest ∧
    after.requestDigest = before.requestDigest ∧
    after.slotEpoch = before.slotEpoch ∧
    after.requestedEpoch = before.requestedEpoch ∧
    after.slotResidue = before.slotResidue ∧
    after.requestedResidue = before.requestedResidue ∧
    after.slotWinding = before.slotWinding ∧
    after.requestedWinding = before.requestedWinding ∧
    after.recurrenceBudget = before.recurrenceBudget ∧
    after.supportAssignments = before.supportAssignments ∧
    after.externalEffects = before.externalEffects

def MemoryLifecycleInvariant (state : MemoryLifecycleState) : Prop :=
  state.recurrenceSteps ≤ state.recurrenceBudget ∧
    state.supportAssignments = 0 ∧
    state.externalEffects = 0

def StalePathContained (state : MemoryLifecycleState) : Prop :=
  state.stage = .staleDetected ∨
    state.stage = .fallback ∨
    state.stage = .recurring ∨
    state.stage = .closed

def exactFreshRead (state : MemoryLifecycleState) : Bool :=
  state.slotEpoch == state.requestedEpoch &&
    state.slotResidue == state.requestedResidue &&
      state.slotWinding == state.requestedWinding

def MemoryStageCoherent (state : MemoryLifecycleState) : Prop :=
  (state.stage = .freshValidated -> exactFreshRead state = true) ∧
    (state.stage = .staleDetected -> exactFreshRead state = false)

def memoryLifecycleStep
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent) :
    MemoryLifecycleRoute × MemoryLifecycleState :=
  match event with
  | .requestRead =>
      if state.stage == .written then
        (.accepted, { state with stage := .readRequested })
      else (.rejectStage, state)
  | .classifyRead =>
      if state.stage != .readRequested then (.rejectStage, state)
      else if exactFreshRead state then
        (.accepted, { state with stage := .freshValidated })
      else (.accepted, { state with stage := .staleDetected })
  | .consumeFresh =>
      if state.stage == .staleDetected then (.rejectStale, state)
      else if state.stage == .freshValidated then
        (.accepted, { state with stage := .consumed })
      else (.rejectStage, state)
  | .useFallback =>
      if state.stage == .staleDetected then
        (.accepted, { state with stage := .fallback })
      else (.rejectStage, state)
  | .startRecurrence =>
      if state.stage != .consumed && state.stage != .fallback then
        (.rejectStage, state)
      else if state.recurrenceBudget == 0 then (.rejectBudget, state)
      else (.accepted, { state with stage := .recurring })
  | .recur =>
      if state.stage != .recurring then (.rejectStage, state)
      else if state.recurrenceSteps >= state.recurrenceBudget then
        (.rejectBudget, state)
      else (.accepted, { state with recurrenceSteps := state.recurrenceSteps + 1 })
  | .exitRecurrence =>
      if state.stage == .recurring then
        (.accepted, { state with stage := .closed })
      else (.rejectStage, state)
  | .close =>
      if state.stage == .consumed || state.stage == .fallback then
        (.accepted, { state with stage := .closed })
      else (.rejectStage, state)

def runMemoryLifecycle :
    MemoryLifecycleState -> List MemoryLifecycleEvent -> MemoryLifecycleState
  | state, [] => state
  | state, event :: rest =>
      runMemoryLifecycle (memoryLifecycleStep state event).2 rest

theorem memory_lifecycle_rejected_event_is_noninterfering
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent)
    (h : (memoryLifecycleStep state event).1 ≠ .accepted) :
    (memoryLifecycleStep state event).2 = state := by
  cases event <;>
    simp_all [memoryLifecycleStep] <;>
    repeat' first | split | simp_all

theorem memory_lifecycle_step_preserves_identity_and_authority
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent) :
    let next := (memoryLifecycleStep state event).2
    next.memoryDigest = state.memoryDigest ∧
      next.requestDigest = state.requestDigest ∧
      next.slotEpoch = state.slotEpoch ∧
      next.requestedEpoch = state.requestedEpoch ∧
      next.slotResidue = state.slotResidue ∧
      next.requestedResidue = state.requestedResidue ∧
      next.slotWinding = state.slotWinding ∧
      next.requestedWinding = state.requestedWinding ∧
      next.recurrenceBudget = state.recurrenceBudget ∧
      next.supportAssignments = state.supportAssignments ∧
      next.externalEffects = state.externalEffects := by
  cases event <;>
    simp [memoryLifecycleStep] <;>
    repeat' first | split | simp_all

theorem memory_lifecycle_step_preserves_custody
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent) :
    MemoryCustodyPreserved state (memoryLifecycleStep state event).2 := by
  exact memory_lifecycle_step_preserves_identity_and_authority state event

theorem memory_custody_transitive
    {initial middle final : MemoryLifecycleState}
    (h₁ : MemoryCustodyPreserved initial middle)
    (h₂ : MemoryCustodyPreserved middle final) :
    MemoryCustodyPreserved initial final := by
  unfold MemoryCustodyPreserved at *
  rcases h₁ with ⟨h₁a, h₁b, h₁c, h₁d, h₁e, h₁f, h₁g, h₁h, h₁i, h₁j, h₁k⟩
  rcases h₂ with ⟨h₂a, h₂b, h₂c, h₂d, h₂e, h₂f, h₂g, h₂h, h₂i, h₂j, h₂k⟩
  constructor
  · exact h₂a.trans h₁a
  constructor
  · exact h₂b.trans h₁b
  constructor
  · exact h₂c.trans h₁c
  constructor
  · exact h₂d.trans h₁d
  constructor
  · exact h₂e.trans h₁e
  constructor
  · exact h₂f.trans h₁f
  constructor
  · exact h₂g.trans h₁g
  constructor
  · exact h₂h.trans h₁h
  constructor
  · exact h₂i.trans h₁i
  constructor
  · exact h₂j.trans h₁j
  · exact h₂k.trans h₁k

theorem run_memory_lifecycle_preserves_custody
    (state : MemoryLifecycleState) (events : List MemoryLifecycleEvent) :
    MemoryCustodyPreserved state (runMemoryLifecycle state events) := by
  induction events generalizing state with
  | nil =>
      simp [runMemoryLifecycle, MemoryCustodyPreserved]
  | cons event rest ih =>
      exact memory_custody_transitive
        (memory_lifecycle_step_preserves_custody state event)
        (ih (memoryLifecycleStep state event).2)

theorem memory_lifecycle_step_preserves_invariant
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent)
    (h : MemoryLifecycleInvariant state) :
    MemoryLifecycleInvariant (memoryLifecycleStep state event).2 := by
  cases event <;>
    simp [MemoryLifecycleInvariant, memoryLifecycleStep] at * <;>
    repeat' first | split | simp_all
  omega

theorem run_memory_lifecycle_preserves_invariant
    (state : MemoryLifecycleState) (events : List MemoryLifecycleEvent)
    (h : MemoryLifecycleInvariant state) :
    MemoryLifecycleInvariant (runMemoryLifecycle state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (memoryLifecycleStep state event).2
        (memory_lifecycle_step_preserves_invariant state event h)

theorem memory_lifecycle_step_recurrence_monotone
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent) :
    state.recurrenceSteps ≤ (memoryLifecycleStep state event).2.recurrenceSteps := by
  cases event <;>
    simp [memoryLifecycleStep] <;>
    repeat' first | split | simp_all

theorem run_memory_lifecycle_recurrence_monotone
    (state : MemoryLifecycleState) (events : List MemoryLifecycleEvent) :
    state.recurrenceSteps ≤ (runMemoryLifecycle state events).recurrenceSteps := by
  induction events generalizing state with
  | nil => simp [runMemoryLifecycle]
  | cons event rest ih =>
      exact Nat.le_trans
        (memory_lifecycle_step_recurrence_monotone state event)
        (ih (memoryLifecycleStep state event).2)

theorem memory_lifecycle_step_preserves_stage_coherence
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent)
    (h : MemoryStageCoherent state) :
    MemoryStageCoherent (memoryLifecycleStep state event).2 := by
  cases event <;>
    simp [MemoryStageCoherent, memoryLifecycleStep, exactFreshRead] at * <;>
    repeat' first | split | simp_all
  assumption

theorem run_memory_lifecycle_preserves_stage_coherence
    (state : MemoryLifecycleState) (events : List MemoryLifecycleEvent)
    (h : MemoryStageCoherent state) :
    MemoryStageCoherent (runMemoryLifecycle state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (memoryLifecycleStep state event).2
        (memory_lifecycle_step_preserves_stage_coherence state event h)

theorem stale_path_containment_survives_one_step
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent)
    (h : StalePathContained state) :
    StalePathContained (memoryLifecycleStep state event).2 := by
  rcases h with h | h | h | h <;>
    cases event <;>
    simp [StalePathContained, memoryLifecycleStep, h] <;>
    repeat' first | split | simp_all

theorem stale_path_containment_survives_arbitrary_suffix
    (state : MemoryLifecycleState) (events : List MemoryLifecycleEvent)
    (h : StalePathContained state) :
    StalePathContained (runMemoryLifecycle state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (memoryLifecycleStep state event).2
        (stale_path_containment_survives_one_step state event h)

theorem stale_path_excludes_fresh_consumption
    (state : MemoryLifecycleState) (h : StalePathContained state) :
    state.stage ≠ .freshValidated ∧ state.stage ≠ .consumed := by
  rcases h with h | h | h | h <;> simp_all

theorem stale_detection_excludes_fresh_consumption_after_any_suffix
    (state : MemoryLifecycleState) (events : List MemoryLifecycleEvent)
    (h : state.stage = .staleDetected) :
    let final := runMemoryLifecycle state events
    final.stage ≠ .freshValidated ∧ final.stage ≠ .consumed := by
  apply stale_path_excludes_fresh_consumption
  apply stale_path_containment_survives_arbitrary_suffix
  exact Or.inl h

theorem closed_memory_lifecycle_step_is_absorbing
    (state : MemoryLifecycleState) (event : MemoryLifecycleEvent)
    (h : state.stage = .closed) :
    (memoryLifecycleStep state event).2 = state := by
  cases event <;> simp [memoryLifecycleStep, h]

theorem closed_memory_lifecycle_suffix_is_absorbing
    (state : MemoryLifecycleState) (events : List MemoryLifecycleEvent)
    (h : state.stage = .closed) :
    runMemoryLifecycle state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      rw [runMemoryLifecycle, closed_memory_lifecycle_step_is_absorbing state event h]
      exact ih state h

theorem run_memory_lifecycle_append
    (state : MemoryLifecycleState)
    (left right : List MemoryLifecycleEvent) :
    runMemoryLifecycle state (left ++ right) =
      runMemoryLifecycle (runMemoryLifecycle state left) right := by
  induction left generalizing state with
  | nil => rfl
  | cons event rest ih =>
      simp only [List.cons_append, runMemoryLifecycle]
      exact ih (memoryLifecycleStep state event).2

theorem same_residue_different_winding_is_not_fresh
    (state : MemoryLifecycleState)
    (hResidue : state.slotResidue = state.requestedResidue)
    (hWinding : state.slotWinding ≠ state.requestedWinding) :
    exactFreshRead state = false := by
  simp [exactFreshRead, hResidue, hWinding]

theorem stale_classification_blocks_fresh_consumption
    (state : MemoryLifecycleState) (h : state.stage = .staleDetected) :
    memoryLifecycleStep state .consumeFresh = (.rejectStale, state) := by
  simp [memoryLifecycleStep, h]

theorem recurrence_at_budget_is_rejected_noninterferingly
    (state : MemoryLifecycleState)
    (hStage : state.stage = .recurring)
    (hBudget : state.recurrenceBudget ≤ state.recurrenceSteps) :
    memoryLifecycleStep state .recur = (.rejectBudget, state) := by
  simp [memoryLifecycleStep, hStage, hBudget]

def freshMemoryTrace : List MemoryLifecycleEvent :=
  [.requestRead, .classifyRead, .consumeFresh, .startRecurrence,
    .recur, .recur, .exitRecurrence]

def staleAliasState : MemoryLifecycleState :=
  { ({} : MemoryLifecycleState) with requestedWinding := 5 }

def staleFallbackTrace : List MemoryLifecycleEvent :=
  [.requestRead, .classifyRead, .useFallback, .close]

theorem fresh_trace_reaches_bounded_recurrence_closure :
    let final := runMemoryLifecycle ({} : MemoryLifecycleState) freshMemoryTrace
    final.stage = .closed ∧
      final.recurrenceSteps = 2 ∧
      final.recurrenceBudget = 2 ∧
      final.supportAssignments = 0 ∧
      final.externalEffects = 0 := by native_decide

theorem third_recurrence_step_is_rejected_without_state_change :
    let atBudget := runMemoryLifecycle ({} : MemoryLifecycleState)
      [.requestRead, .classifyRead, .consumeFresh, .startRecurrence,
        .recur, .recur]
    memoryLifecycleStep atBudget .recur = (.rejectBudget, atBudget) := by
  native_decide

theorem stale_alias_trace_uses_fallback_and_closes :
    let classified := runMemoryLifecycle staleAliasState
      [.requestRead, .classifyRead]
    let final := runMemoryLifecycle staleAliasState staleFallbackTrace
    classified.stage = .staleDetected ∧
      (memoryLifecycleStep classified .consumeFresh).1 = .rejectStale ∧
      final.stage = .closed ∧
      final.recurrenceSteps = 0 ∧
      final.supportAssignments = 0 ∧
      final.externalEffects = 0 := by native_decide

end AsiStackProofs.CoilAttentionMemory

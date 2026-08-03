namespace AsiStackProofs.BenchmarkRatchets

structure CapabilityPromotionReview where
  capabilityPromotion : Bool
  benchmarkEvidencePresent : Bool
  regressionRecordsPreserved : Bool
deriving DecidableEq, Repr

def CapabilityPromotionHasBenchmarkAndRegressionEvidence
    (review : CapabilityPromotionReview) : Prop :=
  review.capabilityPromotion = true ->
    review.benchmarkEvidencePresent = true ∧
      review.regressionRecordsPreserved = true

structure SaturatedBenchmarkPromotionReview where
  benchmarkSaturated : Bool
  soleEvidenceForHigherReadiness : Bool
  higherReadinessPromoted : Bool
deriving DecidableEq, Repr

def SaturatedBenchmarkAloneBlocksHigherReadinessPromotion
    (review : SaturatedBenchmarkPromotionReview) : Prop :=
  review.benchmarkSaturated = true ->
    review.soleEvidenceForHigherReadiness = true ->
      review.higherReadinessPromoted = false

inductive BenchmarkLifecycle where
  | candidate
  | frontier
  | regressionFloor
  | contaminated
  | retired
deriving DecidableEq, Repr

inductive RatchetDecision where
  | keepFrontier
  | promoteReadiness
  | moveToRegressionFloor
  | quarantine
  | blockPromotion
deriving DecidableEq, Repr

structure RatchetDecisionReview where
  lifecycle : BenchmarkLifecycle
  benchmarkSaturated : Bool
  contaminationSuspected : Bool
  transferOrMutationCheckPresent : Bool
  regressionRecordsPreserved : Bool
  negativeResultsPreserved : Bool
  decision : RatchetDecision
deriving DecidableEq, Repr

def RatchetDecisionAccepted (review : RatchetDecisionReview) : Prop :=
  match review.decision with
  | .promoteReadiness =>
      review.regressionRecordsPreserved = true ∧
        review.transferOrMutationCheckPresent = true ∧
          review.negativeResultsPreserved = true ∧
            review.contaminationSuspected = false
  | .moveToRegressionFloor =>
      review.benchmarkSaturated = true ∧
        review.regressionRecordsPreserved = true
  | .quarantine =>
      review.contaminationSuspected = true
  | .blockPromotion => True
  | .keepFrontier => True

theorem accepted_readiness_promotion_requires_transfer_negative_and_regression_records
    {review : RatchetDecisionReview} :
    RatchetDecisionAccepted review ->
    review.decision = RatchetDecision.promoteReadiness ->
    review.transferOrMutationCheckPresent = true ∧
      review.negativeResultsPreserved = true ∧
        review.regressionRecordsPreserved = true := by
  intro accepted promoted
  unfold RatchetDecisionAccepted at accepted
  rw [promoted] at accepted
  exact And.intro accepted.2.1 (And.intro accepted.2.2.1 accepted.1)

theorem accepted_saturated_floor_requires_regression_records
    {review : RatchetDecisionReview} :
    RatchetDecisionAccepted review ->
    review.decision = RatchetDecision.moveToRegressionFloor ->
    review.benchmarkSaturated = true ∧
      review.regressionRecordsPreserved = true := by
  intro accepted floor
  unfold RatchetDecisionAccepted at accepted
  rw [floor] at accepted
  exact accepted

theorem contaminated_review_cannot_promote_readiness
    {review : RatchetDecisionReview} :
    RatchetDecisionAccepted review ->
    review.contaminationSuspected = true ->
    review.decision = RatchetDecision.promoteReadiness ->
    False := by
  intro accepted contaminated promoted
  unfold RatchetDecisionAccepted at accepted
  rw [promoted] at accepted
  simp [contaminated] at accepted

structure AntiGoodhartFixtureBridgeSummary where
  validFixtureCount : Nat
  expectedInvalidFixtureCount : Nat
  promotionReadyValidCount : Nat
  regressionFloorValidCount : Nat
  missingGoodhartChecksRejected : Bool
  policyFromBlockedRatchetRejected : Bool
  rewardAsTruthRejected : Bool
  saturatedPromotionRejected : Bool
  releaseWithoutApprovalRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def AntiGoodhartFixtureBridgeValid
    (summary : AntiGoodhartFixtureBridgeSummary) : Prop :=
  summary.validFixtureCount = 2 ∧
    summary.expectedInvalidFixtureCount = 5 ∧
    summary.promotionReadyValidCount = 1 ∧
    summary.regressionFloorValidCount = 1 ∧
    summary.missingGoodhartChecksRejected = true ∧
    summary.policyFromBlockedRatchetRejected = true ∧
    summary.rewardAsTruthRejected = true ∧
    summary.saturatedPromotionRejected = true ∧
    summary.releaseWithoutApprovalRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

def benchmarkAntiGoodhartFixtureBridge :
    AntiGoodhartFixtureBridgeSummary :=
  { validFixtureCount := 2,
    expectedInvalidFixtureCount := 5,
    promotionReadyValidCount := 1,
    regressionFloorValidCount := 1,
    missingGoodhartChecksRejected := true,
    policyFromBlockedRatchetRejected := true,
    rewardAsTruthRejected := true,
    saturatedPromotionRejected := true,
    releaseWithoutApprovalRejected := true,
    supportStateEffectNone := true,
    nonClaimBoundary := true }

/-! ## Versioned benchmark-ratchet lifecycle

This transition system covers authored finite instrument custody and disposition
semantics. It does not establish benchmark validity, contamination detection,
transfer quality, capability improvement, or deployed release enforcement.
-/

inductive RatchetStage where
  | registered
  | baselineLocked
  | evaluationRecorded
  | integrityReviewed
  | transferReviewed
  | dispositioned
  | closed
deriving DecidableEq, Repr

inductive RatchetEvent where
  | lockBaseline
  | recordEvaluation
  | reviewIntegrity
  | reviewTransfer
  | decide
  | close
deriving DecidableEq, Repr

inductive RatchetRoute where
  | accepted
  | rejectStage
  | rejectEvidence
deriving DecidableEq, Repr

inductive RatchetOutcome where
  | none
  | candidateForIndependentReview
  | regressionFloor
  | quarantine
deriving DecidableEq, Repr

structure RatchetLifecycleState where
  stage : RatchetStage := .registered
  instrumentDigest : Nat := 6101
  datasetVersion : Nat := 6102
  harnessVersion : Nat := 6103
  claimDigest : Nat := 6104
  authorityCeiling : Nat := 1
  benchmarkSaturated : Bool := false
  contaminationSuspected : Bool := false
  transferOrMutationCheckPresent : Bool := true
  regressionRecordsPreserved : Bool := true
  negativeResultsPreserved : Bool := true
  outcome : RatchetOutcome := .none
  receiptCount : Nat := 0
  supportAssignments : Nat := 0
  externalEffects : Nat := 0
deriving DecidableEq, Repr

def ratchetLifecycleStep
    (state : RatchetLifecycleState) (event : RatchetEvent) :
    RatchetRoute × RatchetLifecycleState :=
  match event with
  | .lockBaseline =>
      if state.stage == .registered then
        (.accepted, { state with
          stage := .baselineLocked
          receiptCount := state.receiptCount + 1 })
      else (.rejectStage, state)
  | .recordEvaluation =>
      if state.stage == .baselineLocked then
        (.accepted, { state with
          stage := .evaluationRecorded
          receiptCount := state.receiptCount + 1 })
      else (.rejectStage, state)
  | .reviewIntegrity =>
      if state.stage != .evaluationRecorded then (.rejectStage, state)
      else if state.contaminationSuspected then
        (.accepted, { state with
          stage := .dispositioned
          outcome := .quarantine
          receiptCount := state.receiptCount + 1 })
      else
        (.accepted, { state with
          stage := .integrityReviewed
          receiptCount := state.receiptCount + 1 })
  | .reviewTransfer =>
      if state.stage != .integrityReviewed then (.rejectStage, state)
      else if !state.transferOrMutationCheckPresent then (.rejectEvidence, state)
      else
        (.accepted, { state with
          stage := .transferReviewed
          receiptCount := state.receiptCount + 1 })
  | .decide =>
      if state.stage != .transferReviewed then (.rejectStage, state)
      else if state.contaminationSuspected then
        (.accepted, { state with
          stage := .dispositioned
          outcome := .quarantine
          receiptCount := state.receiptCount + 1 })
      else if !state.regressionRecordsPreserved || !state.negativeResultsPreserved then
        (.rejectEvidence, state)
      else if state.benchmarkSaturated then
        (.accepted, { state with
          stage := .dispositioned
          outcome := .regressionFloor
          receiptCount := state.receiptCount + 1 })
      else
        (.accepted, { state with
          stage := .dispositioned
          outcome := .candidateForIndependentReview
          receiptCount := state.receiptCount + 1 })
  | .close =>
      if state.stage == .dispositioned then
        (.accepted, { state with
          stage := .closed
          receiptCount := state.receiptCount + 1 })
      else (.rejectStage, state)

def runRatchetLifecycle :
    RatchetLifecycleState -> List RatchetEvent -> RatchetLifecycleState
  | state, [] => state
  | state, event :: rest =>
      runRatchetLifecycle (ratchetLifecycleStep state event).2 rest

theorem ratchet_rejected_event_is_noninterfering
    (state : RatchetLifecycleState) (event : RatchetEvent)
    (h : (ratchetLifecycleStep state event).1 ≠ .accepted) :
    (ratchetLifecycleStep state event).2 = state := by
  cases event <;>
    simp_all [ratchetLifecycleStep] <;>
    repeat' first | split | simp_all

theorem ratchet_step_preserves_identity_and_authority
    (state : RatchetLifecycleState) (event : RatchetEvent) :
    let next := (ratchetLifecycleStep state event).2
    next.instrumentDigest = state.instrumentDigest ∧
      next.datasetVersion = state.datasetVersion ∧
      next.harnessVersion = state.harnessVersion ∧
      next.claimDigest = state.claimDigest ∧
      next.authorityCeiling = state.authorityCeiling ∧
      next.benchmarkSaturated = state.benchmarkSaturated ∧
      next.contaminationSuspected = state.contaminationSuspected ∧
      next.transferOrMutationCheckPresent = state.transferOrMutationCheckPresent ∧
      next.regressionRecordsPreserved = state.regressionRecordsPreserved ∧
      next.negativeResultsPreserved = state.negativeResultsPreserved ∧
      next.supportAssignments = state.supportAssignments ∧
      next.externalEffects = state.externalEffects := by
  cases event <;>
    simp [ratchetLifecycleStep] <;>
    repeat' first | split | simp_all

theorem ratchet_accepted_step_adds_exactly_one_receipt
    (state : RatchetLifecycleState) (event : RatchetEvent)
    (h : (ratchetLifecycleStep state event).1 = .accepted) :
    (ratchetLifecycleStep state event).2.receiptCount = state.receiptCount + 1 := by
  cases event <;>
    simp_all [ratchetLifecycleStep] <;>
    repeat' first | split | simp_all

theorem run_ratchet_lifecycle_append
    (state : RatchetLifecycleState) (left right : List RatchetEvent) :
    runRatchetLifecycle state (left ++ right) =
      runRatchetLifecycle (runRatchetLifecycle state left) right := by
  induction left generalizing state with
  | nil => rfl
  | cons event rest ih =>
      simp only [List.cons_append, runRatchetLifecycle]
      exact ih (ratchetLifecycleStep state event).2

theorem contaminated_decision_cannot_recommend_promotion
    (state : RatchetLifecycleState)
    (hStage : state.stage = .transferReviewed)
    (hContaminated : state.contaminationSuspected = true) :
    let next := (ratchetLifecycleStep state .decide).2
    next.outcome = .quarantine ∧ next.outcome ≠ .candidateForIndependentReview := by
  simp [ratchetLifecycleStep, hStage, hContaminated]

theorem saturated_decision_routes_to_regression_floor
    (state : RatchetLifecycleState)
    (hStage : state.stage = .transferReviewed)
    (hClean : state.contaminationSuspected = false)
    (hRegression : state.regressionRecordsPreserved = true)
    (hNegative : state.negativeResultsPreserved = true)
    (hSaturated : state.benchmarkSaturated = true) :
    (ratchetLifecycleStep state .decide).2.outcome = .regressionFloor := by
  simp [ratchetLifecycleStep, hStage, hClean, hRegression, hNegative, hSaturated]

theorem missing_transfer_check_rejected_noninterferingly
    (state : RatchetLifecycleState)
    (hStage : state.stage = .integrityReviewed)
    (hMissing : state.transferOrMutationCheckPresent = false) :
    ratchetLifecycleStep state .reviewTransfer = (.rejectEvidence, state) := by
  simp [ratchetLifecycleStep, hStage, hMissing]

theorem missing_preserved_evidence_rejects_disposition
    (state : RatchetLifecycleState)
    (hStage : state.stage = .transferReviewed)
    (hClean : state.contaminationSuspected = false)
    (hMissing : state.regressionRecordsPreserved = false ∨
      state.negativeResultsPreserved = false) :
    ratchetLifecycleStep state .decide = (.rejectEvidence, state) := by
  rcases hMissing with hRegression | hNegative
  · simp [ratchetLifecycleStep, hStage, hClean, hRegression]
  · simp [ratchetLifecycleStep, hStage, hClean, hNegative]

def cleanPromotionTrace : List RatchetEvent :=
  [.lockBaseline, .recordEvaluation, .reviewIntegrity, .reviewTransfer, .decide, .close]

def saturatedRatchetState : RatchetLifecycleState :=
  { ({} : RatchetLifecycleState) with benchmarkSaturated := true }

def contaminatedRatchetState : RatchetLifecycleState :=
  { ({} : RatchetLifecycleState) with contaminationSuspected := true }

theorem clean_trace_reaches_closed_independent_review_candidate :
    let final := runRatchetLifecycle ({} : RatchetLifecycleState) cleanPromotionTrace
    final.stage = .closed ∧
      final.outcome = .candidateForIndependentReview ∧
      final.receiptCount = 6 ∧
      final.supportAssignments = 0 ∧
      final.externalEffects = 0 := by native_decide

theorem saturated_trace_reaches_closed_regression_floor :
    let final := runRatchetLifecycle saturatedRatchetState cleanPromotionTrace
    final.stage = .closed ∧
      final.outcome = .regressionFloor ∧
      final.receiptCount = 6 ∧
      final.supportAssignments = 0 ∧
      final.externalEffects = 0 := by native_decide

theorem contaminated_trace_quarantines_before_transfer :
    let final := runRatchetLifecycle contaminatedRatchetState
      [.lockBaseline, .recordEvaluation, .reviewIntegrity, .close]
    final.stage = .closed ∧
      final.outcome = .quarantine ∧
      final.receiptCount = 4 ∧
      final.supportAssignments = 0 ∧
      final.externalEffects = 0 := by native_decide

theorem closed_ratchet_is_absorbing
    (state : RatchetLifecycleState) (h : state.stage = .closed)
    (event : RatchetEvent) :
    ratchetLifecycleStep state event = (.rejectStage, state) := by
  cases event <;> simp [ratchetLifecycleStep, h]

end AsiStackProofs.BenchmarkRatchets

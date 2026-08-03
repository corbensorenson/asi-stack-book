namespace AsiStackProofs.PrototypeRoadmap

structure PhaseClaimPromotionReview where
  milestoneReached : Bool
  claimPromotionAccepted : Bool
  evidenceArtifactsPresent : Bool
deriving DecidableEq, Repr

def PhaseMilestonePromotionValid (review : PhaseClaimPromotionReview) : Prop :=
  review.milestoneReached = true ->
    review.claimPromotionAccepted = true ->
      review.evidenceArtifactsPresent = true

theorem phase_milestone_cannot_promote_claim_without_evidence_artifacts
    {review : PhaseClaimPromotionReview} :
    PhaseMilestonePromotionValid review ->
    review.milestoneReached = true ->
    review.evidenceArtifactsPresent = false ->
      review.claimPromotionAccepted = false := by
  intro valid reached noEvidence
  cases promoted : review.claimPromotionAccepted with
  | false =>
      rfl
  | true =>
      have evidence := valid reached promoted
      rw [noEvidence] at evidence
      contradiction

inductive PrototypePhaseRoute where
  | reject
  | researchOnly
  | integrate
  | evidenceReview
deriving DecidableEq, Repr

structure PrototypePhaseGateReview where
  phaseProposed : Bool
  sourceMatrixReady : Bool
  artifactGraphReady : Bool
  claimLedgerReady : Bool
  authorityControlsReady : Bool
  acceptanceGatesPassed : Bool
  evidenceRefsPresent : Bool
  evidenceTransitionRecordPresent : Bool
  residualsClosed : Bool
  independentEvaluatorPresent : Bool
  supportPromotionRequested : Bool
  irreversibleAuthorityRequested : Bool
  selfImprovementPhase : Bool
deriving DecidableEq, Repr

def PrototypePhaseRouteFor (review : PrototypePhaseGateReview) : PrototypePhaseRoute :=
  if review.phaseProposed = false then
    PrototypePhaseRoute.reject
  else if review.sourceMatrixReady = false then
    PrototypePhaseRoute.reject
  else if review.artifactGraphReady = false then
    PrototypePhaseRoute.reject
  else if review.claimLedgerReady = false then
    PrototypePhaseRoute.reject
  else if review.authorityControlsReady = false then
    PrototypePhaseRoute.reject
  else if review.selfImprovementPhase = true && review.independentEvaluatorPresent = false then
    PrototypePhaseRoute.reject
  else if review.irreversibleAuthorityRequested = true && review.independentEvaluatorPresent = false then
    PrototypePhaseRoute.reject
  else if review.acceptanceGatesPassed = false then
    PrototypePhaseRoute.researchOnly
  else if review.residualsClosed = false then
    PrototypePhaseRoute.researchOnly
  else if review.supportPromotionRequested = true then
    if review.evidenceRefsPresent = true && review.evidenceTransitionRecordPresent = true then
      PrototypePhaseRoute.evidenceReview
    else
      PrototypePhaseRoute.reject
  else
    PrototypePhaseRoute.integrate

theorem missing_source_matrix_rejects_phase_route
    {review : PrototypePhaseGateReview} :
    review.phaseProposed = true ->
    review.sourceMatrixReady = false ->
      PrototypePhaseRouteFor review = PrototypePhaseRoute.reject := by
  intro proposed missingSource
  simp [PrototypePhaseRouteFor, proposed, missingSource]

theorem self_improvement_without_independent_evaluator_rejected
    {review : PrototypePhaseGateReview} :
    review.phaseProposed = true ->
    review.sourceMatrixReady = true ->
    review.artifactGraphReady = true ->
    review.claimLedgerReady = true ->
    review.authorityControlsReady = true ->
    review.selfImprovementPhase = true ->
    review.independentEvaluatorPresent = false ->
      PrototypePhaseRouteFor review = PrototypePhaseRoute.reject := by
  intro proposed source artifact ledger authority selfImprovement missingEvaluator
  simp [
    PrototypePhaseRouteFor,
    proposed,
    source,
    artifact,
    ledger,
    authority,
    selfImprovement,
    missingEvaluator,
  ]

theorem failed_acceptance_gates_keep_phase_research_only
    {review : PrototypePhaseGateReview} :
    review.phaseProposed = true ->
    review.sourceMatrixReady = true ->
    review.artifactGraphReady = true ->
    review.claimLedgerReady = true ->
    review.authorityControlsReady = true ->
    review.selfImprovementPhase = false ->
    review.irreversibleAuthorityRequested = false ->
    review.acceptanceGatesPassed = false ->
      PrototypePhaseRouteFor review = PrototypePhaseRoute.researchOnly := by
  intro proposed source artifact ledger authority notSelf noIrreversible failedGates
  simp [
    PrototypePhaseRouteFor,
    proposed,
    source,
    artifact,
    ledger,
    authority,
    notSelf,
    noIrreversible,
    failedGates,
  ]

theorem support_promotion_without_evidence_transition_rejected
    {review : PrototypePhaseGateReview} :
    review.phaseProposed = true ->
    review.sourceMatrixReady = true ->
    review.artifactGraphReady = true ->
    review.claimLedgerReady = true ->
    review.authorityControlsReady = true ->
    review.selfImprovementPhase = false ->
    review.irreversibleAuthorityRequested = false ->
    review.acceptanceGatesPassed = true ->
    review.residualsClosed = true ->
    review.supportPromotionRequested = true ->
    review.evidenceTransitionRecordPresent = false ->
      PrototypePhaseRouteFor review = PrototypePhaseRoute.reject := by
  intro proposed source artifact ledger authority notSelf noIrreversible gates residuals promotion missingTransition
  cases evidenceRefs : review.evidenceRefsPresent <;>
    simp [
      PrototypePhaseRouteFor,
      proposed,
      source,
      artifact,
      ledger,
      authority,
      notSelf,
      noIrreversible,
      gates,
      residuals,
      promotion,
      evidenceRefs,
      missingTransition,
    ]

theorem accepted_non_promoting_phase_integrates
    {review : PrototypePhaseGateReview} :
    review.phaseProposed = true ->
    review.sourceMatrixReady = true ->
    review.artifactGraphReady = true ->
    review.claimLedgerReady = true ->
    review.authorityControlsReady = true ->
    review.selfImprovementPhase = false ->
    review.irreversibleAuthorityRequested = false ->
    review.acceptanceGatesPassed = true ->
    review.residualsClosed = true ->
    review.supportPromotionRequested = false ->
      PrototypePhaseRouteFor review = PrototypePhaseRoute.integrate := by
  intro proposed source artifact ledger authority notSelf noIrreversible gates residuals noPromotion
  simp [
    PrototypePhaseRouteFor,
    proposed,
    source,
    artifact,
    ledger,
    authority,
    notSelf,
    noIrreversible,
    gates,
    residuals,
    noPromotion,
  ]

inductive PrototypePhaseGateFixtureBridgeRoute where
  | rejectBridge
  | acceptBridge
deriving DecidableEq, Repr

structure PrototypePhaseGateFixtureBridgeSummary where
  validPhaseAcceptanceFixture : Bool
  validResearchOnlyFixture : Bool
  missingArtifactRejected : Bool
  dependencyInversionRejected : Bool
  selfImprovementWithoutEvaluatorRejected : Bool
  promotionWithoutTransitionRejected : Bool
  debtWithoutRetirementRejected : Bool
  missingNonClaimBoundaryRejected : Bool
  supportStateEffectNone : Bool
  noPhaseCompletionClaim : Bool
deriving DecidableEq, Repr

def PrototypePhaseGateFixtureBridgeComplete
    (summary : PrototypePhaseGateFixtureBridgeSummary) : Bool :=
  summary.validPhaseAcceptanceFixture &&
  summary.validResearchOnlyFixture &&
  summary.missingArtifactRejected &&
  summary.dependencyInversionRejected &&
  summary.selfImprovementWithoutEvaluatorRejected &&
  summary.promotionWithoutTransitionRejected &&
  summary.debtWithoutRetirementRejected &&
  summary.missingNonClaimBoundaryRejected &&
  summary.supportStateEffectNone &&
  summary.noPhaseCompletionClaim

def PrototypePhaseGateFixtureBridgeRouteFor
    (summary : PrototypePhaseGateFixtureBridgeSummary) :
    PrototypePhaseGateFixtureBridgeRoute :=
  if PrototypePhaseGateFixtureBridgeComplete summary then
    PrototypePhaseGateFixtureBridgeRoute.acceptBridge
  else
    PrototypePhaseGateFixtureBridgeRoute.rejectBridge

theorem missing_non_claim_boundary_rejects_prototype_fixture_bridge
    {summary : PrototypePhaseGateFixtureBridgeSummary} :
    summary.missingNonClaimBoundaryRejected = false ->
      PrototypePhaseGateFixtureBridgeRouteFor summary =
        PrototypePhaseGateFixtureBridgeRoute.rejectBridge := by
  intro missingBoundary
  simp [
    PrototypePhaseGateFixtureBridgeRouteFor,
    PrototypePhaseGateFixtureBridgeComplete,
    missingBoundary,
  ]

theorem complete_prototype_phase_gate_fixture_bridge_accepts
    {summary : PrototypePhaseGateFixtureBridgeSummary} :
    summary.validPhaseAcceptanceFixture = true ->
    summary.validResearchOnlyFixture = true ->
    summary.missingArtifactRejected = true ->
    summary.dependencyInversionRejected = true ->
    summary.selfImprovementWithoutEvaluatorRejected = true ->
    summary.promotionWithoutTransitionRejected = true ->
    summary.debtWithoutRetirementRejected = true ->
    summary.missingNonClaimBoundaryRejected = true ->
    summary.supportStateEffectNone = true ->
    summary.noPhaseCompletionClaim = true ->
      PrototypePhaseGateFixtureBridgeRouteFor summary =
        PrototypePhaseGateFixtureBridgeRoute.acceptBridge := by
  intro validAcceptance validResearch missingArtifact dependencyInversion
    selfImprovement promotion debt nonClaim supportNone noCompletion
  simp [
    PrototypePhaseGateFixtureBridgeRouteFor,
    PrototypePhaseGateFixtureBridgeComplete,
    validAcceptance,
    validResearch,
    missingArtifact,
    dependencyInversion,
    selfImprovement,
    promotion,
    debt,
    nonClaim,
    supportNone,
    noCompletion,
  ]

theorem accepted_prototype_phase_gate_fixture_bridge_preserves_non_claims
    {summary : PrototypePhaseGateFixtureBridgeSummary} :
    PrototypePhaseGateFixtureBridgeRouteFor summary =
      PrototypePhaseGateFixtureBridgeRoute.acceptBridge ->
      summary.supportStateEffectNone = true ∧
        summary.noPhaseCompletionClaim = true := by
  intro accepted
  unfold PrototypePhaseGateFixtureBridgeRouteFor at accepted
  cases complete : PrototypePhaseGateFixtureBridgeComplete summary with
  | false =>
      simp [complete] at accepted
  | true =>
      unfold PrototypePhaseGateFixtureBridgeComplete at complete
      repeat
        first
        | cases h : summary.validPhaseAcceptanceFixture <;> simp [h] at complete
        | cases h : summary.validResearchOnlyFixture <;> simp [h] at complete
        | cases h : summary.missingArtifactRejected <;> simp [h] at complete
        | cases h : summary.dependencyInversionRejected <;> simp [h] at complete
        | cases h : summary.selfImprovementWithoutEvaluatorRejected <;> simp [h] at complete
        | cases h : summary.promotionWithoutTransitionRejected <;> simp [h] at complete
        | cases h : summary.debtWithoutRetirementRejected <;> simp [h] at complete
        | cases h : summary.missingNonClaimBoundaryRejected <;> simp [h] at complete
        | cases h : summary.supportStateEffectNone <;> simp [h] at complete
        | cases h : summary.noPhaseCompletionClaim <;> simp [h] at complete
      exact ⟨rfl, rfl⟩

structure PrototypeDependency where
  predecessorOrdinal : Nat
  successorOrdinal : Nat
deriving DecidableEq, Repr

def PrototypeDependencyValid (dependency : PrototypeDependency) : Prop :=
  dependency.predecessorOrdinal < dependency.successorOrdinal

def PrototypeDependencyPlanValid (dependencies : List PrototypeDependency) : Prop :=
  ∀ dependency ∈ dependencies, PrototypeDependencyValid dependency

theorem valid_prototype_dependency_cannot_be_self_referential
    {dependency : PrototypeDependency}
    (h : PrototypeDependencyValid dependency) :
    dependency.predecessorOrdinal ≠ dependency.successorOrdinal := by
  intro equal
  unfold PrototypeDependencyValid at h
  rw [equal] at h
  exact (Nat.lt_irrefl dependency.successorOrdinal) h

theorem adjacent_prototype_dependencies_compose_strict_order
    {first middle last : Nat}
    (firstBeforeMiddle : first < middle)
    (middleBeforeLast : middle < last) :
    first < last := by
  exact Nat.lt_trans firstBeforeMiddle middleBeforeLast

inductive PrototypePhaseExecutionStage where
  | proposed
  | dependenciesBound
  | executing
  | evaluated
  | integrated
  | evidenceReview
  | rolledBack
deriving DecidableEq, Repr, BEq

structure PrototypePhaseExecutionState where
  stage : PrototypePhaseExecutionStage
  phaseId : Nat
  expectedPhaseId : Nat
  planVersion : Nat
  expectedPlanVersion : Nat
  dependencyDigest : Nat
  expectedDependencyDigest : Nat
  dependencyCount : Nat
  satisfiedDependencyCount : Nat
  artifactDigest : Nat
  expectedArtifactDigest : Nat
  selfImprovementPhase : Bool
  supportPromotionRequested : Bool
  dependencyOrderValid : Bool
  requiredArtifactsPresent : Bool
  rollbackPlanPresent : Bool
  independentEvaluatorPresent : Bool
  acceptanceGatesPassed : Bool
  residualsClosed : Bool
  phaseDebtRecorded : Bool
  retirementConditionRecorded : Bool
  evidenceRefsPresent : Bool
  evidenceTransitionRecordPresent : Bool
  nonClaimsRecorded : Bool
  receipts : Nat
  authorityCeiling : Nat
  expectedAuthorityCeiling : Nat
  supportAssignments : Nat
  externalEffects : Nat
deriving DecidableEq, Repr

inductive PrototypePhaseExecutionEvent where
  | bindDependencies
      (phaseId planVersion dependencyDigest satisfiedDependencyCount : Nat)
      (dependencyOrderValid : Bool)
  | beginExecution
      (phaseId planVersion artifactDigest : Nat)
      (requiredArtifactsPresent rollbackPlanPresent : Bool)
  | recordEvaluation
      (phaseId planVersion : Nat)
      (independentEvaluatorPresent acceptanceGatesPassed : Bool)
  | integrate
      (phaseId planVersion : Nat)
      (residualsClosed phaseDebtRecorded retirementConditionRecorded nonClaimsRecorded : Bool)
  | requestEvidenceReview
      (phaseId planVersion : Nat)
      (residualsClosed phaseDebtRecorded retirementConditionRecorded : Bool)
      (evidenceRefsPresent evidenceTransitionRecordPresent nonClaimsRecorded : Bool)
  | rollback
      (phaseId planVersion : Nat)
      (residualOwned : Bool)
deriving DecidableEq, Repr

def PrototypePhaseExecutionCustody (state : PrototypePhaseExecutionState) : Prop :=
  state.phaseId = state.expectedPhaseId ∧
    state.planVersion = state.expectedPlanVersion ∧
      state.dependencyDigest = state.expectedDependencyDigest ∧
        state.artifactDigest = state.expectedArtifactDigest ∧
          state.authorityCeiling = state.expectedAuthorityCeiling

def PrototypePhaseExecutionInvariant (state : PrototypePhaseExecutionState) : Prop :=
  PrototypePhaseExecutionCustody state ∧
    state.supportAssignments = 0 ∧
      state.externalEffects = 0 ∧
        match state.stage with
        | .proposed => True
        | .dependenciesBound =>
            state.dependencyOrderValid = true ∧
              state.satisfiedDependencyCount = state.dependencyCount
        | .executing =>
            state.dependencyOrderValid = true ∧
              state.satisfiedDependencyCount = state.dependencyCount ∧
                state.requiredArtifactsPresent = true ∧
                  state.rollbackPlanPresent = true
        | .evaluated =>
            state.dependencyOrderValid = true ∧
              state.satisfiedDependencyCount = state.dependencyCount ∧
                state.requiredArtifactsPresent = true ∧
                  state.rollbackPlanPresent = true ∧
                    state.independentEvaluatorPresent = true
        | .integrated =>
            state.dependencyOrderValid = true ∧
              state.satisfiedDependencyCount = state.dependencyCount ∧
                state.requiredArtifactsPresent = true ∧
                  state.rollbackPlanPresent = true ∧
                    state.independentEvaluatorPresent = true ∧
                      state.acceptanceGatesPassed = true ∧
                        state.residualsClosed = true ∧
                          state.supportPromotionRequested = false ∧
                            (state.phaseDebtRecorded = false ∨
                              state.retirementConditionRecorded = true) ∧
                              state.nonClaimsRecorded = true
        | .evidenceReview =>
            state.dependencyOrderValid = true ∧
              state.satisfiedDependencyCount = state.dependencyCount ∧
                state.requiredArtifactsPresent = true ∧
                  state.rollbackPlanPresent = true ∧
                    state.independentEvaluatorPresent = true ∧
                      state.acceptanceGatesPassed = true ∧
                        state.residualsClosed = true ∧
                          state.supportPromotionRequested = true ∧
                            state.evidenceRefsPresent = true ∧
                              state.evidenceTransitionRecordPresent = true ∧
                                (state.phaseDebtRecorded = false ∨
                                  state.retirementConditionRecorded = true) ∧
                                  state.nonClaimsRecorded = true
        | .rolledBack => True

def prototypePhaseExecutionStep
    (state : PrototypePhaseExecutionState)
    (event : PrototypePhaseExecutionEvent) :
    Bool × PrototypePhaseExecutionState :=
  match event with
  | .bindDependencies phase plan dependency satisfied orderValid =>
      if state.stage = .proposed ∧
          phase = state.phaseId ∧ plan = state.planVersion ∧
          dependency = state.dependencyDigest ∧
          dependency = state.expectedDependencyDigest ∧
          satisfied = state.dependencyCount ∧ orderValid = true then
        (true, {
          state with
          stage := .dependenciesBound
          satisfiedDependencyCount := satisfied
          dependencyOrderValid := true
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .beginExecution phase plan artifact artifactsPresent rollbackPresent =>
      if state.stage = .dependenciesBound ∧
          phase = state.phaseId ∧ plan = state.planVersion ∧
          artifact = state.artifactDigest ∧ artifact = state.expectedArtifactDigest ∧
          artifactsPresent = true ∧ rollbackPresent = true then
        (true, {
          state with
          stage := .executing
          requiredArtifactsPresent := true
          rollbackPlanPresent := true
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .recordEvaluation phase plan evaluatorPresent gatesPassed =>
      if state.stage = .executing ∧
          phase = state.phaseId ∧ plan = state.planVersion ∧
          evaluatorPresent = true then
        (true, {
          state with
          stage := .evaluated
          independentEvaluatorPresent := true
          acceptanceGatesPassed := gatesPassed
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .integrate phase plan residuals debt retirement nonClaims =>
      if state.stage = .evaluated ∧
          phase = state.phaseId ∧ plan = state.planVersion ∧
          state.acceptanceGatesPassed = true ∧
          state.supportPromotionRequested = false ∧
          residuals = true ∧
          (debt = false ∨ retirement = true) ∧
          nonClaims = true then
        (true, {
          state with
          stage := .integrated
          residualsClosed := true
          phaseDebtRecorded := debt
          retirementConditionRecorded := retirement
          nonClaimsRecorded := true
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .requestEvidenceReview phase plan residuals debt retirement evidence transition nonClaims =>
      if state.stage = .evaluated ∧
          phase = state.phaseId ∧ plan = state.planVersion ∧
          state.acceptanceGatesPassed = true ∧
          state.supportPromotionRequested = true ∧
          residuals = true ∧
          (debt = false ∨ retirement = true) ∧
          evidence = true ∧ transition = true ∧ nonClaims = true then
        (true, {
          state with
          stage := .evidenceReview
          residualsClosed := true
          phaseDebtRecorded := debt
          retirementConditionRecorded := retirement
          evidenceRefsPresent := true
          evidenceTransitionRecordPresent := true
          nonClaimsRecorded := true
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .rollback phase plan residualOwned =>
      if state.stage ≠ .integrated ∧ state.stage ≠ .evidenceReview ∧
          state.stage ≠ .rolledBack ∧
          phase = state.phaseId ∧ plan = state.planVersion ∧
          residualOwned = true then
        (true, {
          state with
          stage := .rolledBack
          receipts := state.receipts + 1
        })
      else
        (false, state)

def runPrototypePhaseExecution :
    PrototypePhaseExecutionState ->
      List PrototypePhaseExecutionEvent -> PrototypePhaseExecutionState
  | state, [] => state
  | state, event :: rest =>
      runPrototypePhaseExecution (prototypePhaseExecutionStep state event).2 rest

def referencePrototypePhaseExecution : PrototypePhaseExecutionState := {
  stage := .proposed
  phaseId := 41
  expectedPhaseId := 41
  planVersion := 3
  expectedPlanVersion := 3
  dependencyDigest := 701
  expectedDependencyDigest := 701
  dependencyCount := 4
  satisfiedDependencyCount := 0
  artifactDigest := 811
  expectedArtifactDigest := 811
  selfImprovementPhase := false
  supportPromotionRequested := false
  dependencyOrderValid := false
  requiredArtifactsPresent := false
  rollbackPlanPresent := false
  independentEvaluatorPresent := false
  acceptanceGatesPassed := false
  residualsClosed := false
  phaseDebtRecorded := false
  retirementConditionRecorded := false
  evidenceRefsPresent := false
  evidenceTransitionRecordPresent := false
  nonClaimsRecorded := false
  receipts := 0
  authorityCeiling := 1
  expectedAuthorityCeiling := 1
  supportAssignments := 0
  externalEffects := 0
}

def referencePrototypePhaseExecutionEvents : List PrototypePhaseExecutionEvent := [
  .bindDependencies 41 3 701 4 true,
  .beginExecution 41 3 811 true true,
  .recordEvaluation 41 3 true true,
  .integrate 41 3 true false false true
]

def referencePrototypePromotionExecution : PrototypePhaseExecutionState := {
  referencePrototypePhaseExecution with supportPromotionRequested := true
}

def referencePrototypePromotionEvents : List PrototypePhaseExecutionEvent := [
  .bindDependencies 41 3 701 4 true,
  .beginExecution 41 3 811 true true,
  .recordEvaluation 41 3 true true,
  .requestEvidenceReview 41 3 true false false true true true
]

theorem prototype_phase_rejected_event_is_noninterfering
    (state : PrototypePhaseExecutionState)
    (event : PrototypePhaseExecutionEvent)
    (h : (prototypePhaseExecutionStep state event).1 = false) :
    (prototypePhaseExecutionStep state event).2 = state := by
  cases event with
  | bindDependencies phase plan dependency satisfied orderValid =>
      by_cases gate : state.stage = .proposed ∧
        phase = state.phaseId ∧ plan = state.planVersion ∧
        dependency = state.dependencyDigest ∧
        dependency = state.expectedDependencyDigest ∧
        satisfied = state.dependencyCount ∧ orderValid = true
      · have dependencyEq :
          state.dependencyDigest = state.expectedDependencyDigest :=
            gate.2.2.2.1.symm.trans gate.2.2.2.2.1
        simp [prototypePhaseExecutionStep, gate, dependencyEq] at h
      · simp [prototypePhaseExecutionStep, gate]
  | beginExecution phase plan artifact artifactsPresent rollbackPresent =>
      by_cases gate : state.stage = .dependenciesBound ∧
        phase = state.phaseId ∧ plan = state.planVersion ∧
        artifact = state.artifactDigest ∧ artifact = state.expectedArtifactDigest ∧
        artifactsPresent = true ∧ rollbackPresent = true
      · have artifactEq : state.artifactDigest = state.expectedArtifactDigest :=
          gate.2.2.2.1.symm.trans gate.2.2.2.2.1
        simp [prototypePhaseExecutionStep, gate, artifactEq] at h
      · simp [prototypePhaseExecutionStep, gate]
  | recordEvaluation phase plan evaluatorPresent gatesPassed =>
      by_cases gate : state.stage = .executing ∧
        phase = state.phaseId ∧ plan = state.planVersion ∧ evaluatorPresent = true
      · simp [prototypePhaseExecutionStep, gate] at h
      · simp [prototypePhaseExecutionStep, gate]
  | integrate phase plan residuals debt retirement nonClaims =>
      by_cases gate : state.stage = .evaluated ∧
        phase = state.phaseId ∧ plan = state.planVersion ∧
        state.acceptanceGatesPassed = true ∧
        state.supportPromotionRequested = false ∧ residuals = true ∧
        (debt = false ∨ retirement = true) ∧ nonClaims = true
      · simp [prototypePhaseExecutionStep, gate] at h
      · simp [prototypePhaseExecutionStep, gate]
  | requestEvidenceReview phase plan residuals debt retirement evidence transition nonClaims =>
      by_cases gate : state.stage = .evaluated ∧
        phase = state.phaseId ∧ plan = state.planVersion ∧
        state.acceptanceGatesPassed = true ∧
        state.supportPromotionRequested = true ∧ residuals = true ∧
        (debt = false ∨ retirement = true) ∧ evidence = true ∧
        transition = true ∧ nonClaims = true
      · simp [prototypePhaseExecutionStep, gate] at h
      · simp [prototypePhaseExecutionStep, gate]
  | rollback phase plan residualOwned =>
      by_cases gate : state.stage ≠ .integrated ∧ state.stage ≠ .evidenceReview ∧
        state.stage ≠ .rolledBack ∧ phase = state.phaseId ∧
        plan = state.planVersion ∧ residualOwned = true
      · simp [prototypePhaseExecutionStep, gate] at h
      · simp [prototypePhaseExecutionStep, gate]

theorem prototype_phase_execution_step_preserves_custody
    (state : PrototypePhaseExecutionState)
    (event : PrototypePhaseExecutionEvent)
    (h : PrototypePhaseExecutionCustody state) :
    PrototypePhaseExecutionCustody (prototypePhaseExecutionStep state event).2 := by
  cases event <;>
    simp [prototypePhaseExecutionStep, PrototypePhaseExecutionCustody] at h ⊢ <;>
    split <;> simp_all

theorem run_prototype_phase_execution_preserves_custody
    (state : PrototypePhaseExecutionState)
    (events : List PrototypePhaseExecutionEvent)
    (h : PrototypePhaseExecutionCustody state) :
    PrototypePhaseExecutionCustody (runPrototypePhaseExecution state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (prototypePhaseExecutionStep state event).2
        (prototype_phase_execution_step_preserves_custody state event h)

theorem prototype_phase_execution_step_preserves_invariant
    (state : PrototypePhaseExecutionState)
    (event : PrototypePhaseExecutionEvent)
    (h : PrototypePhaseExecutionInvariant state) :
    PrototypePhaseExecutionInvariant (prototypePhaseExecutionStep state event).2 := by
  cases event <;>
    simp [prototypePhaseExecutionStep, PrototypePhaseExecutionInvariant,
      PrototypePhaseExecutionCustody] at h ⊢ <;>
    split <;> simp_all

theorem run_prototype_phase_execution_preserves_invariant
    (state : PrototypePhaseExecutionState)
    (events : List PrototypePhaseExecutionEvent)
    (h : PrototypePhaseExecutionInvariant state) :
    PrototypePhaseExecutionInvariant (runPrototypePhaseExecution state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (prototypePhaseExecutionStep state event).2
        (prototype_phase_execution_step_preserves_invariant state event h)

theorem run_prototype_phase_execution_append
    (state : PrototypePhaseExecutionState)
    (left right : List PrototypePhaseExecutionEvent) :
    runPrototypePhaseExecution state (left ++ right) =
      runPrototypePhaseExecution (runPrototypePhaseExecution state left) right := by
  induction left generalizing state with
  | nil => rfl
  | cons event rest ih =>
      simp [runPrototypePhaseExecution, ih]

theorem reference_prototype_phase_execution_reaches_integrated :
    (runPrototypePhaseExecution referencePrototypePhaseExecution
      referencePrototypePhaseExecutionEvents).stage = .integrated := by
  rfl

theorem reference_prototype_phase_execution_has_no_support_or_external_effect :
    let final := runPrototypePhaseExecution referencePrototypePhaseExecution
      referencePrototypePhaseExecutionEvents
    final.supportAssignments = 0 ∧ final.externalEffects = 0 := by
  decide

theorem reference_prototype_phase_execution_has_exact_receipt_count :
    (runPrototypePhaseExecution referencePrototypePhaseExecution
      referencePrototypePhaseExecutionEvents).receipts = 4 := by
  rfl

theorem reference_prototype_promotion_reaches_evidence_review :
    (runPrototypePhaseExecution referencePrototypePromotionExecution
      referencePrototypePromotionEvents).stage = .evidenceReview := by
  rfl

theorem reference_prototype_promotion_has_no_support_or_external_effect :
    let final := runPrototypePhaseExecution referencePrototypePromotionExecution
      referencePrototypePromotionEvents
    final.supportAssignments = 0 ∧ final.externalEffects = 0 := by
  decide

theorem incomplete_dependency_count_rejects_without_state_change :
    prototypePhaseExecutionStep referencePrototypePhaseExecution
      (.bindDependencies 41 3 701 3 true) =
        (false, referencePrototypePhaseExecution) := by
  decide

theorem dependency_inversion_rejects_without_state_change :
    prototypePhaseExecutionStep referencePrototypePhaseExecution
      (.bindDependencies 41 3 701 4 false) =
        (false, referencePrototypePhaseExecution) := by
  decide

theorem missing_rollback_plan_rejects_execution_without_state_change :
    let bound := (prototypePhaseExecutionStep referencePrototypePhaseExecution
      (.bindDependencies 41 3 701 4 true)).2
    prototypePhaseExecutionStep bound (.beginExecution 41 3 811 true false) =
      (false, bound) := by
  decide

theorem self_improvement_without_independent_execution_evaluator_rejected :
    let proposed := { referencePrototypePhaseExecution with selfImprovementPhase := true }
    let executing := runPrototypePhaseExecution proposed
      [
        .bindDependencies 41 3 701 4 true,
        .beginExecution 41 3 811 true true
      ]
    prototypePhaseExecutionStep executing (.recordEvaluation 41 3 false true) =
      (false, executing) := by
  decide

theorem failed_execution_acceptance_gates_reject_integration :
    let evaluated := runPrototypePhaseExecution referencePrototypePhaseExecution
      [
        .bindDependencies 41 3 701 4 true,
        .beginExecution 41 3 811 true true,
        .recordEvaluation 41 3 true false
      ]
    prototypePhaseExecutionStep evaluated (.integrate 41 3 true false false true) =
      (false, evaluated) := by
  decide

theorem phase_debt_without_retirement_condition_rejects_integration :
    let evaluated := runPrototypePhaseExecution referencePrototypePhaseExecution
      (referencePrototypePhaseExecutionEvents.take 3)
    prototypePhaseExecutionStep evaluated (.integrate 41 3 true true false true) =
      (false, evaluated) := by
  decide

theorem promotion_without_evidence_transition_rejects_review_handoff :
    let proposed := { referencePrototypePhaseExecution with
      supportPromotionRequested := true }
    let evaluated := runPrototypePhaseExecution proposed
      [
        .bindDependencies 41 3 701 4 true,
        .beginExecution 41 3 811 true true,
        .recordEvaluation 41 3 true true
      ]
    prototypePhaseExecutionStep evaluated
      (.requestEvidenceReview 41 3 true false false true false true) =
        (false, evaluated) := by
  decide

theorem integrated_prototype_phase_is_absorbing_one_step
    (state : PrototypePhaseExecutionState)
    (event : PrototypePhaseExecutionEvent)
    (h : state.stage = .integrated) :
    prototypePhaseExecutionStep state event = (false, state) := by
  cases event <;> simp [prototypePhaseExecutionStep, h]

theorem evidence_review_prototype_phase_is_absorbing_one_step
    (state : PrototypePhaseExecutionState)
    (event : PrototypePhaseExecutionEvent)
    (h : state.stage = .evidenceReview) :
    prototypePhaseExecutionStep state event = (false, state) := by
  cases event <;> simp [prototypePhaseExecutionStep, h]

theorem rolled_back_prototype_phase_is_absorbing_one_step
    (state : PrototypePhaseExecutionState)
    (event : PrototypePhaseExecutionEvent)
    (h : state.stage = .rolledBack) :
    prototypePhaseExecutionStep state event = (false, state) := by
  cases event <;> simp [prototypePhaseExecutionStep, h]

theorem integrated_prototype_phase_is_absorbing_for_any_suffix
    (state : PrototypePhaseExecutionState)
    (events : List PrototypePhaseExecutionEvent)
    (h : state.stage = .integrated) :
    runPrototypePhaseExecution state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      rw [show runPrototypePhaseExecution state (event :: rest) =
        runPrototypePhaseExecution (prototypePhaseExecutionStep state event).2 rest by rfl]
      rw [integrated_prototype_phase_is_absorbing_one_step state event h]
      exact ih state h

theorem evidence_review_prototype_phase_is_absorbing_for_any_suffix
    (state : PrototypePhaseExecutionState)
    (events : List PrototypePhaseExecutionEvent)
    (h : state.stage = .evidenceReview) :
    runPrototypePhaseExecution state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      rw [show runPrototypePhaseExecution state (event :: rest) =
        runPrototypePhaseExecution (prototypePhaseExecutionStep state event).2 rest by rfl]
      rw [evidence_review_prototype_phase_is_absorbing_one_step state event h]
      exact ih state h

theorem rolled_back_prototype_phase_is_absorbing_for_any_suffix
    (state : PrototypePhaseExecutionState)
    (events : List PrototypePhaseExecutionEvent)
    (h : state.stage = .rolledBack) :
    runPrototypePhaseExecution state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      rw [show runPrototypePhaseExecution state (event :: rest) =
        runPrototypePhaseExecution (prototypePhaseExecutionStep state event).2 rest by rfl]
      rw [rolled_back_prototype_phase_is_absorbing_one_step state event h]
      exact ih state h

def prototypePhaseThinSummary
    (state : PrototypePhaseExecutionState) : Nat × Nat :=
  (state.dependencyCount, state.receipts)

def PrototypePhaseIntegrated (state : PrototypePhaseExecutionState) : Prop :=
  state.stage = .integrated

def integratedReferencePrototypePhase : PrototypePhaseExecutionState :=
  runPrototypePhaseExecution referencePrototypePhaseExecution
    referencePrototypePhaseExecutionEvents

def unintegratedPrototypePhaseWithEqualSummary : PrototypePhaseExecutionState := {
  referencePrototypePhaseExecution with
  stage := .evaluated
  satisfiedDependencyCount := 4
  dependencyOrderValid := true
  requiredArtifactsPresent := true
  rollbackPlanPresent := true
  independentEvaluatorPresent := true
  acceptanceGatesPassed := true
  receipts := 4
}

theorem prototype_phase_thin_summary_collides_across_integration :
    prototypePhaseThinSummary integratedReferencePrototypePhase =
        prototypePhaseThinSummary unintegratedPrototypePhaseWithEqualSummary ∧
      PrototypePhaseIntegrated integratedReferencePrototypePhase ∧
      ¬ PrototypePhaseIntegrated unintegratedPrototypePhaseWithEqualSummary := by
  simp [prototypePhaseThinSummary, integratedReferencePrototypePhase,
    unintegratedPrototypePhaseWithEqualSummary, PrototypePhaseIntegrated,
    runPrototypePhaseExecution, referencePrototypePhaseExecutionEvents,
    referencePrototypePhaseExecution, prototypePhaseExecutionStep]

theorem no_prototype_phase_thin_summary_classifier_recovers_integration :
    ¬ ∃ classify : Nat × Nat -> Bool,
      ∀ state : PrototypePhaseExecutionState,
        classify (prototypePhaseThinSummary state) = true ↔
          PrototypePhaseIntegrated state := by
  intro proposed
  rcases proposed with ⟨classify, exactResult⟩
  have collision := prototype_phase_thin_summary_collides_across_integration
  have integrated := (exactResult integratedReferencePrototypePhase).2 collision.2.1
  have proposedRejected := (exactResult unintegratedPrototypePhaseWithEqualSummary).1
  rw [collision.1] at integrated
  exact collision.2.2 (proposedRejected integrated)

end AsiStackProofs.PrototypeRoadmap

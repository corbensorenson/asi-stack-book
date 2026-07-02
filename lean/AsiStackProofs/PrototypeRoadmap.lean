namespace AsiStackProofs.PrototypeRoadmap

structure PhaseUnlockReview where
  dependentPhaseUnlocked : Bool
  acceptanceGatesDeclared : Bool
  acceptanceGatesPassed : Bool
deriving DecidableEq, Repr

def PhaseUnlockValid (review : PhaseUnlockReview) : Prop :=
  review.dependentPhaseUnlocked = true ->
    review.acceptanceGatesDeclared = true ∧
      review.acceptanceGatesPassed = true

theorem roadmap_phase_unlock_requires_passing_acceptance_gates
    {review : PhaseUnlockReview} :
    PhaseUnlockValid review ->
    review.dependentPhaseUnlocked = true ->
      review.acceptanceGatesDeclared = true ∧
        review.acceptanceGatesPassed = true := by
  intro valid unlocked
  exact valid unlocked

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

theorem accepted_phase_claim_promotion_requires_evidence_artifacts
    {review : PhaseClaimPromotionReview} :
    PhaseMilestonePromotionValid review ->
    review.milestoneReached = true ->
    review.claimPromotionAccepted = true ->
      review.evidenceArtifactsPresent = true := by
  intro valid reached accepted
  exact valid reached accepted

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

end AsiStackProofs.PrototypeRoadmap

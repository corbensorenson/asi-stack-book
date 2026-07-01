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

end AsiStackProofs.PrototypeRoadmap

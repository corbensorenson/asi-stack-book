namespace AsiStackProofs.Replacement

structure ReplacementCommit where
  qualificationEvidence : Bool
  rollbackMetadata : Bool
  regressionPassed : Bool
deriving DecidableEq, Repr

def CommitPrerequisitesPresent (commit : ReplacementCommit) : Prop :=
  commit.qualificationEvidence = true ∧
    commit.rollbackMetadata = true

def PromotionAllowed (commit : ReplacementCommit) : Prop :=
  CommitPrerequisitesPresent commit ∧
    commit.regressionPassed = true

theorem replacement_commit_requires_evidence_and_rollback
    {commit : ReplacementCommit} :
    PromotionAllowed commit ->
    commit.qualificationEvidence = true ∧ commit.rollbackMetadata = true := by
  intro allowed
  exact allowed.1

theorem failed_regression_blocks_replacement_promotion
    {commit : ReplacementCommit} :
    commit.regressionPassed = false ->
    ¬ PromotionAllowed commit := by
  intro failed promoted
  unfold PromotionAllowed at promoted
  rw [failed] at promoted
  cases promoted.2

inductive ReplacementTransactionRoute where
  | rejectProposal
  | requirePrecheck
  | requestGovernanceReview
  | canaryOnly
  | quarantineCandidate
  | rollbackRequired
  | commitDefault
deriving DecidableEq, Repr

structure ReplacementTransactionReview where
  priorArtifactPresent : Bool
  candidateArtifactPresent : Bool
  identityPreserved : Bool
  authorityWithinField : Bool
  governanceApproval : Bool
  qualificationEvidence : Bool
  evaluatorIndependent : Bool
  regressionPassed : Bool
  rollbackReceiptPresent : Bool
  rollbackDryRunPassed : Bool
  residualEscrowPresent : Bool
  monitorIncident : Bool
  defaultRequested : Bool
deriving DecidableEq, Repr

def ReplacementTransactionRouteFor
    (review : ReplacementTransactionReview) : ReplacementTransactionRoute :=
  if review.priorArtifactPresent = false then
    ReplacementTransactionRoute.rejectProposal
  else if review.candidateArtifactPresent = false then
    ReplacementTransactionRoute.rejectProposal
  else if review.identityPreserved = false then
    ReplacementTransactionRoute.requirePrecheck
  else if review.authorityWithinField = false ∧ review.governanceApproval = false then
    ReplacementTransactionRoute.requestGovernanceReview
  else if review.qualificationEvidence = false then
    ReplacementTransactionRoute.requirePrecheck
  else if review.evaluatorIndependent = false then
    ReplacementTransactionRoute.requestGovernanceReview
  else if review.regressionPassed = false then
    ReplacementTransactionRoute.quarantineCandidate
  else if review.rollbackReceiptPresent = false then
    ReplacementTransactionRoute.requirePrecheck
  else if review.rollbackDryRunPassed = false then
    ReplacementTransactionRoute.canaryOnly
  else if review.residualEscrowPresent = false then
    ReplacementTransactionRoute.requirePrecheck
  else if review.monitorIncident = true then
    ReplacementTransactionRoute.rollbackRequired
  else if review.defaultRequested = true then
    ReplacementTransactionRoute.commitDefault
  else
    ReplacementTransactionRoute.canaryOnly

theorem missing_prior_artifact_rejects_replacement
    {review : ReplacementTransactionReview} :
    review.priorArtifactPresent = false ->
    ReplacementTransactionRouteFor review =
      ReplacementTransactionRoute.rejectProposal := by
  intro missingPrior
  unfold ReplacementTransactionRouteFor
  simp [missingPrior]

theorem authority_expansion_without_approval_routes_to_review
    {review : ReplacementTransactionReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.identityPreserved = true ->
    review.authorityWithinField = false ->
    review.governanceApproval = false ->
    ReplacementTransactionRouteFor review =
      ReplacementTransactionRoute.requestGovernanceReview := by
  intro priorPresent candidatePresent identityPreserved authorityExpansion
    noApproval
  unfold ReplacementTransactionRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityExpansion,
    noApproval]

theorem captured_evaluator_routes_replacement_to_review
    {review : ReplacementTransactionReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.identityPreserved = true ->
    review.authorityWithinField = true ->
    review.qualificationEvidence = true ->
    review.evaluatorIndependent = false ->
    ReplacementTransactionRouteFor review =
      ReplacementTransactionRoute.requestGovernanceReview := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified capturedEvaluator
  unfold ReplacementTransactionRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, capturedEvaluator]

theorem failed_regression_routes_to_quarantine
    {review : ReplacementTransactionReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.identityPreserved = true ->
    review.authorityWithinField = true ->
    review.qualificationEvidence = true ->
    review.evaluatorIndependent = true ->
    review.regressionPassed = false ->
    ReplacementTransactionRouteFor review =
      ReplacementTransactionRoute.quarantineCandidate := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified evaluatorIndependent failedRegression
  unfold ReplacementTransactionRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, evaluatorIndependent, failedRegression]

theorem missing_rollback_receipt_requires_precheck
    {review : ReplacementTransactionReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.identityPreserved = true ->
    review.authorityWithinField = true ->
    review.qualificationEvidence = true ->
    review.evaluatorIndependent = true ->
    review.regressionPassed = true ->
    review.rollbackReceiptPresent = false ->
    ReplacementTransactionRouteFor review =
      ReplacementTransactionRoute.requirePrecheck := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified evaluatorIndependent regressionPassed missingRollbackReceipt
  unfold ReplacementTransactionRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, evaluatorIndependent, regressionPassed, missingRollbackReceipt]

theorem failed_rollback_dry_run_routes_to_canary_only
    {review : ReplacementTransactionReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.identityPreserved = true ->
    review.authorityWithinField = true ->
    review.qualificationEvidence = true ->
    review.evaluatorIndependent = true ->
    review.regressionPassed = true ->
    review.rollbackReceiptPresent = true ->
    review.rollbackDryRunPassed = false ->
    ReplacementTransactionRouteFor review =
      ReplacementTransactionRoute.canaryOnly := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified evaluatorIndependent regressionPassed rollbackReceipt
    failedDryRun
  unfold ReplacementTransactionRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, evaluatorIndependent, regressionPassed, rollbackReceipt,
    failedDryRun]

theorem monitor_incident_requires_rollback
    {review : ReplacementTransactionReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.identityPreserved = true ->
    review.authorityWithinField = true ->
    review.qualificationEvidence = true ->
    review.evaluatorIndependent = true ->
    review.regressionPassed = true ->
    review.rollbackReceiptPresent = true ->
    review.rollbackDryRunPassed = true ->
    review.residualEscrowPresent = true ->
    review.monitorIncident = true ->
    ReplacementTransactionRouteFor review =
      ReplacementTransactionRoute.rollbackRequired := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified evaluatorIndependent regressionPassed rollbackReceipt dryRun
    residualEscrow incident
  unfold ReplacementTransactionRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, evaluatorIndependent, regressionPassed, rollbackReceipt, dryRun,
    residualEscrow, incident]

theorem complete_replacement_review_commits_default
    {review : ReplacementTransactionReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.identityPreserved = true ->
    review.authorityWithinField = true ->
    review.qualificationEvidence = true ->
    review.evaluatorIndependent = true ->
    review.regressionPassed = true ->
    review.rollbackReceiptPresent = true ->
    review.rollbackDryRunPassed = true ->
    review.residualEscrowPresent = true ->
    review.monitorIncident = false ->
    review.defaultRequested = true ->
    ReplacementTransactionRouteFor review =
      ReplacementTransactionRoute.commitDefault := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified evaluatorIndependent regressionPassed rollbackReceipt dryRun
    residualEscrow noIncident defaultRequested
  unfold ReplacementTransactionRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, evaluatorIndependent, regressionPassed, rollbackReceipt, dryRun,
    residualEscrow, noIncident, defaultRequested]

end AsiStackProofs.Replacement

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

inductive ReplacementLifecycleRoute where
  | rejectProposal
  | requirePrecheck
  | requireFreshEvidence
  | requestGovernanceReview
  | quarantineCandidate
  | canaryOnly
  | rollbackRequired
  | requireResidualOwner
  | requireDeprecationNotice
  | requireRetirementReceipt
  | blockForNonClaimBoundary
  | commitDefault
deriving DecidableEq, Repr

structure ReplacementLifecycleReview where
  priorArtifactPresent : Bool
  candidateArtifactPresent : Bool
  fieldIdentityPreserved : Bool
  authorityNonWidening : Bool
  governanceApproval : Bool
  qualificationEvidence : Bool
  evidenceFresh : Bool
  regressionFloorPreserved : Bool
  canaryScopeDeclared : Bool
  canaryPassed : Bool
  monitorWindowDeclared : Bool
  monitorWindowClean : Bool
  rollbackHandlePresent : Bool
  rollbackDryRunPassed : Bool
  irreversibleEffectsPresent : Bool
  irreversibleEffectsOwned : Bool
  residualOwnerPresent : Bool
  deprecationRequested : Bool
  deprecationNoticePresent : Bool
  retirementRequested : Bool
  retirementReceiptPresent : Bool
  nonClaimBoundaryPresent : Bool
  defaultPromotionRequested : Bool
deriving DecidableEq, Repr

def ReplacementLifecycleRouteFor
    (review : ReplacementLifecycleReview) : ReplacementLifecycleRoute :=
  if review.priorArtifactPresent = false then
    ReplacementLifecycleRoute.rejectProposal
  else if review.candidateArtifactPresent = false then
    ReplacementLifecycleRoute.rejectProposal
  else if review.fieldIdentityPreserved = false then
    ReplacementLifecycleRoute.quarantineCandidate
  else if review.authorityNonWidening = false ∧
      review.governanceApproval = false then
    ReplacementLifecycleRoute.requestGovernanceReview
  else if review.qualificationEvidence = false then
    ReplacementLifecycleRoute.requirePrecheck
  else if review.evidenceFresh = false then
    ReplacementLifecycleRoute.requireFreshEvidence
  else if review.regressionFloorPreserved = false then
    ReplacementLifecycleRoute.quarantineCandidate
  else if review.canaryScopeDeclared = false then
    ReplacementLifecycleRoute.requirePrecheck
  else if review.canaryPassed = false then
    ReplacementLifecycleRoute.canaryOnly
  else if review.monitorWindowDeclared = false then
    ReplacementLifecycleRoute.requirePrecheck
  else if review.monitorWindowClean = false then
    ReplacementLifecycleRoute.rollbackRequired
  else if review.rollbackHandlePresent = false then
    ReplacementLifecycleRoute.requirePrecheck
  else if review.rollbackDryRunPassed = false then
    ReplacementLifecycleRoute.canaryOnly
  else if review.irreversibleEffectsPresent = true ∧
      review.irreversibleEffectsOwned = false then
    ReplacementLifecycleRoute.requireResidualOwner
  else if review.residualOwnerPresent = false then
    ReplacementLifecycleRoute.requireResidualOwner
  else if review.deprecationRequested = true ∧
      review.deprecationNoticePresent = false then
    ReplacementLifecycleRoute.requireDeprecationNotice
  else if review.retirementRequested = true ∧
      review.retirementReceiptPresent = false then
    ReplacementLifecycleRoute.requireRetirementReceipt
  else if review.nonClaimBoundaryPresent = false then
    ReplacementLifecycleRoute.blockForNonClaimBoundary
  else if review.defaultPromotionRequested = true then
    ReplacementLifecycleRoute.commitDefault
  else
    ReplacementLifecycleRoute.canaryOnly

theorem lifecycle_missing_candidate_rejects_replacement
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.rejectProposal := by
  intro priorPresent missingCandidate
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, missingCandidate]

theorem lifecycle_identity_mismatch_quarantines_candidate
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.quarantineCandidate := by
  intro priorPresent candidatePresent identityMismatch
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityMismatch]

theorem lifecycle_authority_widening_without_governance_requests_review
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = false ->
    review.governanceApproval = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requestGovernanceReview := by
  intro priorPresent candidatePresent identityPreserved authorityWidening
    noApproval
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWidening,
    noApproval]

theorem lifecycle_stale_evidence_requires_fresh_evidence
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requireFreshEvidence := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified staleEvidence
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, staleEvidence]

theorem lifecycle_failed_regression_floor_quarantines_candidate
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.quarantineCandidate := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorFailed
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorFailed]

theorem lifecycle_missing_canary_scope_requires_precheck
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requirePrecheck := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved missingCanaryScope
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, missingCanaryScope]

theorem lifecycle_failed_canary_stays_canary_only
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.canaryOnly := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared failedCanary
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, failedCanary]

theorem lifecycle_missing_monitor_window_requires_precheck
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requirePrecheck := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    missingMonitor
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    missingMonitor]

theorem lifecycle_monitor_incident_requires_rollback
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.rollbackRequired := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorIncident
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorIncident]

theorem lifecycle_missing_rollback_handle_requires_precheck
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = true ->
    review.rollbackHandlePresent = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requirePrecheck := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorClean missingRollback
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorClean, missingRollback]

theorem lifecycle_failed_rollback_dry_run_stays_canary_only
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = true ->
    review.rollbackHandlePresent = true ->
    review.rollbackDryRunPassed = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.canaryOnly := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorClean rollbackHandle rollbackDryRunFailed
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorClean, rollbackHandle, rollbackDryRunFailed]

theorem lifecycle_unowned_irreversible_effect_requires_residual_owner
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = true ->
    review.rollbackHandlePresent = true ->
    review.rollbackDryRunPassed = true ->
    review.irreversibleEffectsPresent = true ->
    review.irreversibleEffectsOwned = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requireResidualOwner := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorClean rollbackHandle rollbackDryRun irreversible
    unowned
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorClean, rollbackHandle, rollbackDryRun, irreversible,
    unowned]

theorem lifecycle_missing_residual_owner_requires_owner
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = true ->
    review.rollbackHandlePresent = true ->
    review.rollbackDryRunPassed = true ->
    review.irreversibleEffectsPresent = false ->
    review.residualOwnerPresent = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requireResidualOwner := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorClean rollbackHandle rollbackDryRun noIrreversible
    missingOwner
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorClean, rollbackHandle, rollbackDryRun,
    noIrreversible, missingOwner]

theorem lifecycle_deprecation_without_notice_requires_notice
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = true ->
    review.rollbackHandlePresent = true ->
    review.rollbackDryRunPassed = true ->
    review.irreversibleEffectsPresent = false ->
    review.residualOwnerPresent = true ->
    review.deprecationRequested = true ->
    review.deprecationNoticePresent = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requireDeprecationNotice := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorClean rollbackHandle rollbackDryRun noIrreversible
    ownerPresent deprecationRequested noNotice
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorClean, rollbackHandle, rollbackDryRun,
    noIrreversible, ownerPresent, deprecationRequested, noNotice]

theorem lifecycle_retirement_without_receipt_requires_receipt
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = true ->
    review.rollbackHandlePresent = true ->
    review.rollbackDryRunPassed = true ->
    review.irreversibleEffectsPresent = false ->
    review.residualOwnerPresent = true ->
    review.deprecationRequested = false ->
    review.retirementRequested = true ->
    review.retirementReceiptPresent = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.requireRetirementReceipt := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorClean rollbackHandle rollbackDryRun noIrreversible
    ownerPresent noDeprecation retirementRequested missingReceipt
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorClean, rollbackHandle, rollbackDryRun,
    noIrreversible, ownerPresent, noDeprecation, retirementRequested,
    missingReceipt]

theorem lifecycle_missing_nonclaim_boundary_blocks_promotion
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = true ->
    review.rollbackHandlePresent = true ->
    review.rollbackDryRunPassed = true ->
    review.irreversibleEffectsPresent = false ->
    review.residualOwnerPresent = true ->
    review.deprecationRequested = false ->
    review.retirementRequested = false ->
    review.nonClaimBoundaryPresent = false ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.blockForNonClaimBoundary := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorClean rollbackHandle rollbackDryRun noIrreversible
    ownerPresent noDeprecation noRetirement missingBoundary
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorClean, rollbackHandle, rollbackDryRun,
    noIrreversible, ownerPresent, noDeprecation, noRetirement,
    missingBoundary]

theorem complete_replacement_lifecycle_commits_default
    {review : ReplacementLifecycleReview} :
    review.priorArtifactPresent = true ->
    review.candidateArtifactPresent = true ->
    review.fieldIdentityPreserved = true ->
    review.authorityNonWidening = true ->
    review.qualificationEvidence = true ->
    review.evidenceFresh = true ->
    review.regressionFloorPreserved = true ->
    review.canaryScopeDeclared = true ->
    review.canaryPassed = true ->
    review.monitorWindowDeclared = true ->
    review.monitorWindowClean = true ->
    review.rollbackHandlePresent = true ->
    review.rollbackDryRunPassed = true ->
    review.irreversibleEffectsPresent = false ->
    review.residualOwnerPresent = true ->
    review.deprecationRequested = false ->
    review.retirementRequested = false ->
    review.nonClaimBoundaryPresent = true ->
    review.defaultPromotionRequested = true ->
    ReplacementLifecycleRouteFor review =
      ReplacementLifecycleRoute.commitDefault := by
  intro priorPresent candidatePresent identityPreserved authorityWithin
    qualified freshEvidence floorPreserved canaryDeclared canaryPassed
    monitorDeclared monitorClean rollbackHandle rollbackDryRun noIrreversible
    ownerPresent noDeprecation noRetirement boundaryPresent defaultRequested
  unfold ReplacementLifecycleRouteFor
  simp [priorPresent, candidatePresent, identityPreserved, authorityWithin,
    qualified, freshEvidence, floorPreserved, canaryDeclared, canaryPassed,
    monitorDeclared, monitorClean, rollbackHandle, rollbackDryRun,
    noIrreversible, ownerPresent, noDeprecation, noRetirement, boundaryPresent,
    defaultRequested]

structure ReplacementTraceProbeSummary where
  traceStepCount : Nat
  traceTransactionCount : Nat
  negativeControlCount : Nat
  canaryKeptNonDefault : Bool
  monitorTriggerRollbackPresent : Bool
  rollbackDryRunPresent : Bool
  authorityWideningRejected : Bool
  failedRegressionRejected : Bool
  missingRollbackRejected : Bool
  residualsRecorded : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def ReplacementTraceProbeValid
    (summary : ReplacementTraceProbeSummary) : Prop :=
  summary.traceStepCount = 6 ∧
    summary.traceTransactionCount = 2 ∧
      summary.negativeControlCount = 3 ∧
        summary.canaryKeptNonDefault = true ∧
          summary.monitorTriggerRollbackPresent = true ∧
            summary.rollbackDryRunPresent = true ∧
              summary.authorityWideningRejected = true ∧
                summary.failedRegressionRejected = true ∧
                  summary.missingRollbackRejected = true ∧
                    summary.residualsRecorded = true ∧
                      summary.supportStateEffectNone = true ∧
                        summary.nonClaimBoundary = true

def replacementTraceProbeFixture : ReplacementTraceProbeSummary := {
  traceStepCount := 6
  traceTransactionCount := 2
  negativeControlCount := 3
  canaryKeptNonDefault := true
  monitorTriggerRollbackPresent := true
  rollbackDryRunPresent := true
  authorityWideningRejected := true
  failedRegressionRejected := true
  missingRollbackRejected := true
  residualsRecorded := true
  supportStateEffectNone := true
  nonClaimBoundary := true
}

theorem replacement_trace_probe_fixture_valid :
    ReplacementTraceProbeValid replacementTraceProbeFixture := by
  unfold ReplacementTraceProbeValid replacementTraceProbeFixture
  simp

theorem replacement_trace_probe_rejects_authority_widening :
    replacementTraceProbeFixture.authorityWideningRejected = true := by
  rfl

theorem replacement_trace_probe_preserves_no_promotion_boundary :
    replacementTraceProbeFixture.supportStateEffectNone = true ∧
      replacementTraceProbeFixture.nonClaimBoundary = true := by
  exact And.intro rfl rfl

end AsiStackProofs.Replacement

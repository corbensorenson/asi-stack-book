namespace AsiStackProofs.SecurityKernel

inductive ClearanceLevel where
  | publicData
  | internalData
  | restricted
  | secret
deriving DecidableEq, Repr

def ClearanceLevel.rank : ClearanceLevel -> Nat
  | .publicData => 0
  | .internalData => 1
  | .restricted => 2
  | .secret => 3

structure ExecutionBoundary where
  authorized : Bool
  permitsSecretSubstitution : Bool
  clearance : ClearanceLevel
deriving DecidableEq, Repr

structure SecretHandle where
  requiredClearance : ClearanceLevel
deriving DecidableEq, Repr

def SecretSubstitutionAllowed (boundary : ExecutionBoundary) (handle : SecretHandle) : Prop :=
  boundary.authorized = true ∧
    boundary.permitsSecretSubstitution = true ∧
    handle.requiredClearance.rank <= boundary.clearance.rank

theorem secret_substitution_requires_authorized_boundary
    {boundary : ExecutionBoundary} {handle : SecretHandle} :
    SecretSubstitutionAllowed boundary handle ->
    boundary.authorized = true := by
  intro allowed
  exact allowed.1

structure ContextPacket where
  clearance : ClearanceLevel
deriving DecidableEq, Repr

structure DigitalScif where
  isProtected : Bool
  requiredClearance : ClearanceLevel
deriving DecidableEq, Repr

def ScifAdmissionAllowed (packet : ContextPacket) (scif : DigitalScif) : Prop :=
  scif.isProtected = false ∨ scif.requiredClearance.rank <= packet.clearance.rank

theorem insufficient_clearance_blocks_protected_scif_entry
    {packet : ContextPacket} {scif : DigitalScif} :
    scif.isProtected = true ->
    packet.clearance.rank < scif.requiredClearance.rank ->
    ¬ ScifAdmissionAllowed packet scif := by
  intro isProtected insufficient allowed
  cases allowed with
  | inl unprotected =>
      rw [isProtected] at unprotected
      contradiction
  | inr enoughClearance =>
      exact Nat.not_le_of_gt insufficient enoughClearance

inductive SecurityKernelRoute where
  | denyUse
  | requestApproval
  | spawnScif
  | sanitizeAndCommit
  | recordLeakResidual
  | revokeHandle
  | allowUse
deriving DecidableEq, Repr

structure AuthorityUseReview where
  handlePresent : Bool
  leaseActive : Bool
  approvalPresent : Bool
  boundaryAuthorized : Bool
  permitsSecretSubstitution : Bool
  clearanceSufficient : Bool
  scifRequired : Bool
  scifSpawned : Bool
  rawOutputSanitized : Bool
  promptInjectionDetected : Bool
  residualLeakRisk : Bool
  revocationRequested : Bool
deriving DecidableEq, Repr

def SecurityKernelRouteFor
    (review : AuthorityUseReview) : SecurityKernelRoute :=
  if review.handlePresent = false then
    SecurityKernelRoute.denyUse
  else if review.revocationRequested = true then
    SecurityKernelRoute.revokeHandle
  else if review.leaseActive = false then
    SecurityKernelRoute.denyUse
  else if review.approvalPresent = false then
    SecurityKernelRoute.requestApproval
  else if review.boundaryAuthorized = false then
    SecurityKernelRoute.denyUse
  else if review.permitsSecretSubstitution = false then
    SecurityKernelRoute.denyUse
  else if review.clearanceSufficient = false then
    SecurityKernelRoute.denyUse
  else if review.promptInjectionDetected = true then
    SecurityKernelRoute.recordLeakResidual
  else if review.scifRequired = true ∧ review.scifSpawned = false then
    SecurityKernelRoute.spawnScif
  else if review.rawOutputSanitized = false then
    SecurityKernelRoute.sanitizeAndCommit
  else if review.residualLeakRisk = true then
    SecurityKernelRoute.recordLeakResidual
  else
    SecurityKernelRoute.allowUse

theorem missing_handle_denies_authority_use
    {review : AuthorityUseReview} :
    review.handlePresent = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.denyUse := by
  intro missingHandle
  unfold SecurityKernelRouteFor
  simp [missingHandle]

theorem revocation_request_revokes_handle
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = true ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.revokeHandle := by
  intro handlePresent revocationRequested
  unfold SecurityKernelRouteFor
  simp [handlePresent, revocationRequested]

theorem inactive_lease_denies_authority_use
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.denyUse := by
  intro handlePresent noRevocation inactiveLease
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, inactiveLease]

theorem missing_approval_requests_approval
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.requestApproval := by
  intro handlePresent noRevocation leaseActive missingApproval
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, missingApproval]

theorem unauthorized_boundary_denies_authority_use
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = true ->
    review.boundaryAuthorized = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.denyUse := by
  intro handlePresent noRevocation leaseActive approvalPresent
    unauthorized
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, approvalPresent,
    unauthorized]

theorem missing_secret_substitution_permission_denies_authority_use
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = true ->
    review.boundaryAuthorized = true ->
    review.permitsSecretSubstitution = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.denyUse := by
  intro handlePresent noRevocation leaseActive approvalPresent
    boundaryAuthorized missingPermission
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, approvalPresent,
    boundaryAuthorized, missingPermission]

theorem insufficient_clearance_denies_authority_use
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = true ->
    review.boundaryAuthorized = true ->
    review.permitsSecretSubstitution = true ->
    review.clearanceSufficient = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.denyUse := by
  intro handlePresent noRevocation leaseActive approvalPresent
    boundaryAuthorized permitsSubstitution insufficientClearance
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, approvalPresent,
    boundaryAuthorized, permitsSubstitution, insufficientClearance]

theorem prompt_injection_records_leak_residual
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = true ->
    review.boundaryAuthorized = true ->
    review.permitsSecretSubstitution = true ->
    review.clearanceSufficient = true ->
    review.promptInjectionDetected = true ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.recordLeakResidual := by
  intro handlePresent noRevocation leaseActive approvalPresent
    boundaryAuthorized permitsSubstitution clearanceSufficient
    promptInjection
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, approvalPresent,
    boundaryAuthorized, permitsSubstitution, clearanceSufficient,
    promptInjection]

theorem missing_required_scif_routes_to_scif_spawn
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = true ->
    review.boundaryAuthorized = true ->
    review.permitsSecretSubstitution = true ->
    review.clearanceSufficient = true ->
    review.promptInjectionDetected = false ->
    review.scifRequired = true ->
    review.scifSpawned = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.spawnScif := by
  intro handlePresent noRevocation leaseActive approvalPresent
    boundaryAuthorized permitsSubstitution clearanceSufficient
    noPromptInjection scifRequired missingScif
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, approvalPresent,
    boundaryAuthorized, permitsSubstitution, clearanceSufficient,
    noPromptInjection, scifRequired, missingScif]

theorem unsanitized_output_routes_to_sanitization
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = true ->
    review.boundaryAuthorized = true ->
    review.permitsSecretSubstitution = true ->
    review.clearanceSufficient = true ->
    review.promptInjectionDetected = false ->
    review.scifRequired = false ->
    review.rawOutputSanitized = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.sanitizeAndCommit := by
  intro handlePresent noRevocation leaseActive approvalPresent
    boundaryAuthorized permitsSubstitution clearanceSufficient
    noPromptInjection noScifRequired unsanitizedOutput
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, approvalPresent,
    boundaryAuthorized, permitsSubstitution, clearanceSufficient,
    noPromptInjection, noScifRequired, unsanitizedOutput]

theorem residual_risk_records_leak_residual
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = true ->
    review.boundaryAuthorized = true ->
    review.permitsSecretSubstitution = true ->
    review.clearanceSufficient = true ->
    review.promptInjectionDetected = false ->
    review.scifRequired = false ->
    review.rawOutputSanitized = true ->
    review.residualLeakRisk = true ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.recordLeakResidual := by
  intro handlePresent noRevocation leaseActive approvalPresent
    boundaryAuthorized permitsSubstitution clearanceSufficient
    noPromptInjection noScifRequired sanitizedOutput residualRisk
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, approvalPresent,
    boundaryAuthorized, permitsSubstitution, clearanceSufficient,
    noPromptInjection, noScifRequired, sanitizedOutput, residualRisk]

theorem clean_authorized_use_is_allowed
    {review : AuthorityUseReview} :
    review.handlePresent = true ->
    review.revocationRequested = false ->
    review.leaseActive = true ->
    review.approvalPresent = true ->
    review.boundaryAuthorized = true ->
    review.permitsSecretSubstitution = true ->
    review.clearanceSufficient = true ->
    review.promptInjectionDetected = false ->
    review.scifRequired = false ->
    review.rawOutputSanitized = true ->
    review.residualLeakRisk = false ->
    SecurityKernelRouteFor review =
      SecurityKernelRoute.allowUse := by
  intro handlePresent noRevocation leaseActive approvalPresent
    boundaryAuthorized permitsSubstitution clearanceSufficient
    noPromptInjection noScifRequired sanitizedOutput noResidualRisk
  unfold SecurityKernelRouteFor
  simp [handlePresent, noRevocation, leaseActive, approvalPresent,
    boundaryAuthorized, permitsSubstitution, clearanceSufficient,
    noPromptInjection, noScifRequired, sanitizedOutput, noResidualRisk]

inductive ScifCommitRoute where
  | blockCommit
  | commitSanitizedSummary
  | commitSanitizedRefusal
deriving DecidableEq, Repr

structure ScifCommitReview where
  secretInCandidateOutput : Bool
  handleInCandidateOutput : Bool
  lifecycleComplete : Bool
  contextScoped : Bool
  approvalActive : Bool
  residualBoundaryPresent : Bool
  promptInjectionObserved : Bool
deriving DecidableEq, Repr

def ScifCommitRouteFor
    (review : ScifCommitReview) : ScifCommitRoute :=
  if review.secretInCandidateOutput = true then
    ScifCommitRoute.blockCommit
  else if review.handleInCandidateOutput = true then
    ScifCommitRoute.blockCommit
  else if review.lifecycleComplete = false then
    ScifCommitRoute.blockCommit
  else if review.contextScoped = false then
    ScifCommitRoute.blockCommit
  else if review.approvalActive = false then
    ScifCommitRoute.blockCommit
  else if review.residualBoundaryPresent = false then
    ScifCommitRoute.blockCommit
  else if review.promptInjectionObserved = true then
    ScifCommitRoute.commitSanitizedRefusal
  else
    ScifCommitRoute.commitSanitizedSummary

theorem scif_commit_secret_output_blocks_commit
    {review : ScifCommitReview} :
    review.secretInCandidateOutput = true ->
    ScifCommitRouteFor review =
      ScifCommitRoute.blockCommit := by
  intro secretInOutput
  unfold ScifCommitRouteFor
  simp [secretInOutput]

theorem scif_commit_handle_output_blocks_commit
    {review : ScifCommitReview} :
    review.secretInCandidateOutput = false ->
    review.handleInCandidateOutput = true ->
    ScifCommitRouteFor review =
      ScifCommitRoute.blockCommit := by
  intro noSecret handleInOutput
  unfold ScifCommitRouteFor
  simp [noSecret, handleInOutput]

theorem scif_commit_missing_zeroize_blocks_commit
    {review : ScifCommitReview} :
    review.secretInCandidateOutput = false ->
    review.handleInCandidateOutput = false ->
    review.lifecycleComplete = false ->
    ScifCommitRouteFor review =
      ScifCommitRoute.blockCommit := by
  intro noSecret noHandle missingLifecycle
  unfold ScifCommitRouteFor
  simp [noSecret, noHandle, missingLifecycle]

theorem scif_commit_overbroad_context_blocks_commit
    {review : ScifCommitReview} :
    review.secretInCandidateOutput = false ->
    review.handleInCandidateOutput = false ->
    review.lifecycleComplete = true ->
    review.contextScoped = false ->
    ScifCommitRouteFor review =
      ScifCommitRoute.blockCommit := by
  intro noSecret noHandle lifecycleComplete overbroadContext
  unfold ScifCommitRouteFor
  simp [noSecret, noHandle, lifecycleComplete, overbroadContext]

theorem scif_commit_inactive_approval_blocks_commit
    {review : ScifCommitReview} :
    review.secretInCandidateOutput = false ->
    review.handleInCandidateOutput = false ->
    review.lifecycleComplete = true ->
    review.contextScoped = true ->
    review.approvalActive = false ->
    ScifCommitRouteFor review =
      ScifCommitRoute.blockCommit := by
  intro noSecret noHandle lifecycleComplete contextScoped inactiveApproval
  unfold ScifCommitRouteFor
  simp [noSecret, noHandle, lifecycleComplete, contextScoped, inactiveApproval]

theorem scif_commit_missing_residual_blocks_commit
    {review : ScifCommitReview} :
    review.secretInCandidateOutput = false ->
    review.handleInCandidateOutput = false ->
    review.lifecycleComplete = true ->
    review.contextScoped = true ->
    review.approvalActive = true ->
    review.residualBoundaryPresent = false ->
    ScifCommitRouteFor review =
      ScifCommitRoute.blockCommit := by
  intro noSecret noHandle lifecycleComplete contextScoped approvalActive
    missingResidual
  unfold ScifCommitRouteFor
  simp [noSecret, noHandle, lifecycleComplete, contextScoped, approvalActive,
    missingResidual]

theorem scif_commit_prompt_injection_routes_to_sanitized_refusal
    {review : ScifCommitReview} :
    review.secretInCandidateOutput = false ->
    review.handleInCandidateOutput = false ->
    review.lifecycleComplete = true ->
    review.contextScoped = true ->
    review.approvalActive = true ->
    review.residualBoundaryPresent = true ->
    review.promptInjectionObserved = true ->
    ScifCommitRouteFor review =
      ScifCommitRoute.commitSanitizedRefusal := by
  intro noSecret noHandle lifecycleComplete contextScoped approvalActive
    residualBoundary promptInjection
  unfold ScifCommitRouteFor
  simp [noSecret, noHandle, lifecycleComplete, contextScoped, approvalActive,
    residualBoundary, promptInjection]

theorem scif_commit_clean_sanitized_output_commits_summary
    {review : ScifCommitReview} :
    review.secretInCandidateOutput = false ->
    review.handleInCandidateOutput = false ->
    review.lifecycleComplete = true ->
    review.contextScoped = true ->
    review.approvalActive = true ->
    review.residualBoundaryPresent = true ->
    review.promptInjectionObserved = false ->
    ScifCommitRouteFor review =
      ScifCommitRoute.commitSanitizedSummary := by
  intro noSecret noHandle lifecycleComplete contextScoped approvalActive
    residualBoundary noPromptInjection
  unfold ScifCommitRouteFor
  simp [noSecret, noHandle, lifecycleComplete, contextScoped, approvalActive,
    residualBoundary, noPromptInjection]

end AsiStackProofs.SecurityKernel

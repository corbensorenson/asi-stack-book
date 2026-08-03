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

/-! ## Versioned authority-use transaction lifecycle

This finite model separates lease issuance, mediated substitution, execution,
sanitization, independent declassification, zeroization, commit, and descendant
revocation. It trusts the event fields: a checked record is not evidence of
runtime complete mediation, secret non-disclosure, isolation, or side-channel
control.
-/

inductive AuthorityTransactionStage where
  | requested
  | leased
  | injected
  | executed
  | sanitized
  | declassified
  | zeroized
  | committed
  | revoked
deriving DecidableEq, Repr

inductive AuthorityTransactionEventKind where
  | issueLease
  | injectSecret
  | recordExecution
  | recordSanitization
  | recordDeclassification
  | recordZeroization
  | commitOutput
  | propagateRevocation
deriving DecidableEq, Repr

structure AuthorityTransactionState where
  transactionId : Nat
  handleId : Nat
  secretClassId : Nat
  purposeId : Nat
  destinationId : Nat
  principalId : Nat
  kernelId : Nat
  declassifierId : Nat
  version : Nat
  baseAuthorityCeiling : Nat
  currentAuthorityCeiling : Nat
  stage : AuthorityTransactionStage
  descendantCount : Nat
  revokedDescendantCount : Nat
  descendantIds : List Nat
  revokedDescendantIds : List Nat
  sanitizerReceiptCount : Nat
  declassificationReceiptCount : Nat
  zeroizationReceiptCount : Nat
  commitReceiptCount : Nat
  revocationReceiptCount : Nat
  residualCount : Nat
  expiresAt : Nat
  now : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

structure AuthorityTransactionEvent where
  kind : AuthorityTransactionEventKind
  transactionId : Nat
  handleId : Nat
  secretClassId : Nat
  purposeId : Nat
  destinationId : Nat
  actorId : Nat
  expectedVersion : Nat
  targetVersion : Nat
  requestedAuthorityCeiling : Nat
  requestedExpiry : Nat
  observedNow : Nat
  approvalPresent : Bool
  contextScoped : Bool
  boundaryMediated : Bool
  substitutionAuthorized : Bool
  executionReceiptPresent : Bool
  outputContainsSecret : Bool
  outputContainsHandle : Bool
  sanitizerReceiptPresent : Bool
  declassificationReceiptPresent : Bool
  disclosureAuthorized : Bool
  zeroizationReceiptPresent : Bool
  commitReceiptPresent : Bool
  revocationReceiptPresent : Bool
  requestedRevokedDescendantCount : Nat
  requestedRevokedDescendantIds : List Nat
  residualPresent : Bool
  claimsSecurity : Bool
  requestsSupportAssignment : Bool
  requestsExternalEffect : Bool
deriving DecidableEq, Repr

def AuthorityTransactionEventAdmissible
    (state : AuthorityTransactionState)
    (event : AuthorityTransactionEvent) : Prop :=
  event.transactionId = state.transactionId ∧
    event.handleId = state.handleId ∧
    event.secretClassId = state.secretClassId ∧
    event.purposeId = state.purposeId ∧
    event.destinationId = state.destinationId ∧
    event.expectedVersion = state.version ∧
    state.now ≤ event.observedNow ∧
    event.claimsSecurity = false ∧
    event.requestsSupportAssignment = false ∧
    event.requestsExternalEffect = false ∧
    match event.kind with
    | AuthorityTransactionEventKind.issueLease =>
        state.stage = AuthorityTransactionStage.requested ∧
          event.actorId = state.principalId ∧
          event.approvalPresent = true ∧
          event.requestedAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
          event.observedNow < event.requestedExpiry ∧
          event.targetVersion = state.version + 1
    | AuthorityTransactionEventKind.injectSecret =>
        state.stage = AuthorityTransactionStage.leased ∧
          event.actorId = state.kernelId ∧
          event.contextScoped = true ∧
          event.boundaryMediated = true ∧
          event.substitutionAuthorized = true ∧
          event.observedNow < state.expiresAt ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AuthorityTransactionEventKind.recordExecution =>
        state.stage = AuthorityTransactionStage.injected ∧
          event.actorId = state.kernelId ∧
          event.boundaryMediated = true ∧
          event.executionReceiptPresent = true ∧
          event.observedNow < state.expiresAt ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AuthorityTransactionEventKind.recordSanitization =>
        state.stage = AuthorityTransactionStage.executed ∧
          event.actorId = state.kernelId ∧
          event.outputContainsSecret = false ∧
          event.outputContainsHandle = false ∧
          event.sanitizerReceiptPresent = true ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AuthorityTransactionEventKind.recordDeclassification =>
        state.stage = AuthorityTransactionStage.sanitized ∧
          event.actorId = state.declassifierId ∧
          state.declassifierId ≠ state.principalId ∧
          state.declassifierId ≠ state.kernelId ∧
          event.declassificationReceiptPresent = true ∧
          event.disclosureAuthorized = true ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AuthorityTransactionEventKind.recordZeroization =>
        state.stage = AuthorityTransactionStage.declassified ∧
          event.actorId = state.kernelId ∧
          event.zeroizationReceiptPresent = true ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AuthorityTransactionEventKind.commitOutput =>
        state.stage = AuthorityTransactionStage.zeroized ∧
          event.actorId = state.kernelId ∧
          event.commitReceiptPresent = true ∧
          event.residualPresent = true ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | AuthorityTransactionEventKind.propagateRevocation =>
        state.stage = AuthorityTransactionStage.committed ∧
          event.actorId = state.kernelId ∧
          event.revocationReceiptPresent = true ∧
          state.descendantIds.Nodup ∧
          state.descendantCount = state.descendantIds.length ∧
          event.requestedRevokedDescendantCount = state.descendantCount ∧
          event.requestedRevokedDescendantIds = state.descendantIds ∧
          event.residualPresent = true ∧
          event.requestedAuthorityCeiling = 0 ∧
          event.targetVersion = state.version + 1

instance authorityTransactionEventAdmissibleDecidable
    (state : AuthorityTransactionState) (event : AuthorityTransactionEvent) :
    Decidable (AuthorityTransactionEventAdmissible state event) := by
  unfold AuthorityTransactionEventAdmissible
  cases event.kind <;> infer_instance

def AdvanceAuthorityTransaction
    (state : AuthorityTransactionState)
    (event : AuthorityTransactionEvent) : AuthorityTransactionState :=
  match event.kind with
  | AuthorityTransactionEventKind.issueLease =>
      { state with
        stage := AuthorityTransactionStage.leased
        version := event.targetVersion
        currentAuthorityCeiling := event.requestedAuthorityCeiling
        expiresAt := event.requestedExpiry
        now := event.observedNow }
  | AuthorityTransactionEventKind.injectSecret =>
      { state with
        stage := AuthorityTransactionStage.injected
        now := event.observedNow }
  | AuthorityTransactionEventKind.recordExecution =>
      { state with
        stage := AuthorityTransactionStage.executed
        now := event.observedNow }
  | AuthorityTransactionEventKind.recordSanitization =>
      { state with
        stage := AuthorityTransactionStage.sanitized
        sanitizerReceiptCount := state.sanitizerReceiptCount + 1
        now := event.observedNow }
  | AuthorityTransactionEventKind.recordDeclassification =>
      { state with
        stage := AuthorityTransactionStage.declassified
        declassificationReceiptCount := state.declassificationReceiptCount + 1
        now := event.observedNow }
  | AuthorityTransactionEventKind.recordZeroization =>
      { state with
        stage := AuthorityTransactionStage.zeroized
        zeroizationReceiptCount := state.zeroizationReceiptCount + 1
        now := event.observedNow }
  | AuthorityTransactionEventKind.commitOutput =>
      { state with
        stage := AuthorityTransactionStage.committed
        commitReceiptCount := state.commitReceiptCount + 1
        residualCount := state.residualCount + 1
        now := event.observedNow }
  | AuthorityTransactionEventKind.propagateRevocation =>
      { state with
        stage := AuthorityTransactionStage.revoked
        version := event.targetVersion
        currentAuthorityCeiling := 0
        revokedDescendantCount := event.requestedRevokedDescendantCount
        revokedDescendantIds := event.requestedRevokedDescendantIds
        revocationReceiptCount := state.revocationReceiptCount + 1
        residualCount := state.residualCount + 1
        now := event.observedNow }

def ApplyAuthorityTransactionEvent
    (state : AuthorityTransactionState)
    (event : AuthorityTransactionEvent) : Option AuthorityTransactionState :=
  if AuthorityTransactionEventAdmissible state event then
    some (AdvanceAuthorityTransaction state event)
  else
    none

def RunAuthorityTransactionEvents :
    AuthorityTransactionState -> List AuthorityTransactionEvent ->
      Option AuthorityTransactionState
  | state, [] => some state
  | state, event :: tail =>
      match ApplyAuthorityTransactionEvent state event with
      | none => none
      | some next => RunAuthorityTransactionEvents next tail

def ProcessAuthorityTransactionEvent
    (state : AuthorityTransactionState)
    (event : AuthorityTransactionEvent) : AuthorityTransactionState × Bool :=
  match ApplyAuthorityTransactionEvent state event with
  | some next => (next, true)
  | none => (state, false)

def AuthorityTransactionTraceValid :
    AuthorityTransactionState → List AuthorityTransactionEvent → Prop
  | _, [] => True
  | state, event :: tail =>
      ∃ next, ApplyAuthorityTransactionEvent state event = some next ∧
        AuthorityTransactionTraceValid next tail

theorem accepted_authority_transaction_event_is_admissible
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    AuthorityTransactionEventAdmissible state event := by
  unfold ApplyAuthorityTransactionEvent at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_authority_transaction_event_is_exact_advance
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    next = AdvanceAuthorityTransaction state event := by
  unfold ApplyAuthorityTransactionEvent at accepted
  split at accepted
  · simp at accepted
    exact accepted.symm
  · simp at accepted

theorem accepted_authority_transaction_event_preserves_custody
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    next.transactionId = state.transactionId ∧
      next.handleId = state.handleId ∧
      next.secretClassId = state.secretClassId ∧
      next.purposeId = state.purposeId ∧
      next.destinationId = state.destinationId ∧
      next.principalId = state.principalId ∧
      next.kernelId = state.kernelId ∧
      next.declassifierId = state.declassifierId ∧
      next.baseAuthorityCeiling = state.baseAuthorityCeiling := by
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  subst next
  cases kind : event.kind <;> simp [AdvanceAuthorityTransaction, kind]

theorem accepted_authority_transaction_event_is_non_authorizing
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    event.claimsSecurity = false ∧
      event.requestsSupportAssignment = false ∧
      event.requestsExternalEffect = false ∧
      next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectCount = state.externalEffectCount := by
  have admissible :=
    accepted_authority_transaction_event_is_admissible accepted
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, noSecurity, noSupport,
    noEffect, _⟩
  subst next
  exact ⟨noSecurity, noSupport, noEffect,
    by cases kind : event.kind <;> simp [AdvanceAuthorityTransaction, kind],
    by cases kind : event.kind <;> simp [AdvanceAuthorityTransaction, kind]⟩

theorem accepted_authority_transaction_event_never_widens_authority
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling := by
  have admissible :=
    accepted_authority_transaction_event_is_admissible accepted
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  subst next
  cases kind : event.kind with
  | issueLease =>
      simp [kind] at route
      simpa [AdvanceAuthorityTransaction, kind] using route.2.2.2.1
  | injectSecret => simp [AdvanceAuthorityTransaction, kind]
  | recordExecution => simp [AdvanceAuthorityTransaction, kind]
  | recordSanitization => simp [AdvanceAuthorityTransaction, kind]
  | recordDeclassification => simp [AdvanceAuthorityTransaction, kind]
  | recordZeroization => simp [AdvanceAuthorityTransaction, kind]
  | commitOutput => simp [AdvanceAuthorityTransaction, kind]
  | propagateRevocation => simp [AdvanceAuthorityTransaction, kind]

theorem accepted_authority_transaction_event_preserves_descendant_inventory
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    next.descendantCount = state.descendantCount ∧
      next.descendantIds = state.descendantIds := by
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  subst next
  cases kind : event.kind <;> simp [AdvanceAuthorityTransaction, kind]

theorem rejected_authority_transaction_event_preserves_exact_state
    (state : AuthorityTransactionState)
    (event : AuthorityTransactionEvent)
    (rejected : ApplyAuthorityTransactionEvent state event = none) :
    ProcessAuthorityTransactionEvent state event = (state, false) := by
  simp [ProcessAuthorityTransactionEvent, rejected]

theorem accepted_lease_is_bounded_versioned_and_unexpired
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (kind : event.kind = AuthorityTransactionEventKind.issueLease)
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    state.stage = AuthorityTransactionStage.requested ∧
      event.approvalPresent = true ∧
      next.version = state.version + 1 ∧
      next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
      next.now < next.expiresAt := by
  have admissible :=
    accepted_authority_transaction_event_is_admissible accepted
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨requested, _, approval, bounded, future, versioned⟩
  subst next
  simp [AdvanceAuthorityTransaction, kind, requested, approval, bounded, future,
    versioned]

theorem accepted_secret_injection_is_scoped_mediated_and_preexpiry
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (kind : event.kind = AuthorityTransactionEventKind.injectSecret)
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    state.stage = AuthorityTransactionStage.leased ∧
      event.actorId = state.kernelId ∧
      event.contextScoped = true ∧
      event.boundaryMediated = true ∧
      event.substitutionAuthorized = true ∧
      event.observedNow < state.expiresAt ∧
      next.stage = AuthorityTransactionStage.injected := by
  have admissible :=
    accepted_authority_transaction_event_is_admissible accepted
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨leased, kernel, scopedContext, mediated, authorized, future, _, _⟩
  subst next
  simp [AdvanceAuthorityTransaction, kind, leased, kernel, scopedContext, mediated,
    authorized, future]

theorem accepted_sanitization_excludes_raw_secret_and_handle
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (kind : event.kind = AuthorityTransactionEventKind.recordSanitization)
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    state.stage = AuthorityTransactionStage.executed ∧
      event.outputContainsSecret = false ∧
      event.outputContainsHandle = false ∧
      event.sanitizerReceiptPresent = true ∧
      next.sanitizerReceiptCount = state.sanitizerReceiptCount + 1 := by
  have admissible :=
    accepted_authority_transaction_event_is_admissible accepted
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨executed, _, noSecret, noHandle, receipt, _, _⟩
  subst next
  simp [AdvanceAuthorityTransaction, kind, executed, noSecret, noHandle, receipt]

theorem accepted_declassification_is_independent_and_post_sanitization
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (kind : event.kind = AuthorityTransactionEventKind.recordDeclassification)
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    state.stage = AuthorityTransactionStage.sanitized ∧
      event.actorId = state.declassifierId ∧
      state.declassifierId ≠ state.principalId ∧
      state.declassifierId ≠ state.kernelId ∧
      event.declassificationReceiptPresent = true ∧
      event.disclosureAuthorized = true ∧
      next.declassificationReceiptCount =
        state.declassificationReceiptCount + 1 := by
  have admissible :=
    accepted_authority_transaction_event_is_admissible accepted
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨sanitized, actor, notPrincipal, notKernel, receipt,
    authorized, _, _⟩
  subst next
  simp [AdvanceAuthorityTransaction, kind, sanitized, actor, notPrincipal,
    notKernel, receipt, authorized]

theorem accepted_commit_requires_zeroization_and_preserves_residual
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (kind : event.kind = AuthorityTransactionEventKind.commitOutput)
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    state.stage = AuthorityTransactionStage.zeroized ∧
      event.commitReceiptPresent = true ∧
      event.residualPresent = true ∧
      next.stage = AuthorityTransactionStage.committed ∧
      next.commitReceiptCount = state.commitReceiptCount + 1 ∧
      next.residualCount = state.residualCount + 1 := by
  have admissible :=
    accepted_authority_transaction_event_is_admissible accepted
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨zeroized, _, receipt, residual, _, _⟩
  subst next
  simp [AdvanceAuthorityTransaction, kind, zeroized, receipt, residual]

theorem accepted_revocation_covers_descendants_and_closes_authority
    {state next : AuthorityTransactionState}
    {event : AuthorityTransactionEvent}
    (kind : event.kind = AuthorityTransactionEventKind.propagateRevocation)
    (accepted : ApplyAuthorityTransactionEvent state event = some next) :
    state.stage = AuthorityTransactionStage.committed ∧
      event.revocationReceiptPresent = true ∧
      state.descendantIds.Nodup ∧
      state.descendantCount = state.descendantIds.length ∧
      next.revokedDescendantCount = state.descendantCount ∧
      next.revokedDescendantIds = state.descendantIds ∧
      next.revokedDescendantCount = next.revokedDescendantIds.length ∧
      next.currentAuthorityCeiling = 0 ∧
      next.stage = AuthorityTransactionStage.revoked ∧
      next.revocationReceiptCount = state.revocationReceiptCount + 1 := by
  have admissible :=
    accepted_authority_transaction_event_is_admissible accepted
  have exactAdvance :=
    accepted_authority_transaction_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨committed, _, receipt, unique, countMatches,
    countRequested, idsRequested, _, _, _⟩
  subst next
  simp [AdvanceAuthorityTransaction, kind, committed, receipt, unique,
    countMatches, countRequested, idsRequested]

theorem authority_transaction_run_preserves_custody_non_authority_and_narrowing
    {initial final : AuthorityTransactionState}
    {events : List AuthorityTransactionEvent}
    (run : RunAuthorityTransactionEvents initial events = some final) :
    final.transactionId = initial.transactionId ∧
      final.handleId = initial.handleId ∧
      final.secretClassId = initial.secretClassId ∧
      final.purposeId = initial.purposeId ∧
      final.destinationId = initial.destinationId ∧
      final.principalId = initial.principalId ∧
      final.kernelId = initial.kernelId ∧
      final.declassifierId = initial.declassifierId ∧
      final.baseAuthorityCeiling = initial.baseAuthorityCeiling ∧
      final.currentAuthorityCeiling ≤ initial.currentAuthorityCeiling ∧
      final.supportAssignmentCount = initial.supportAssignmentCount ∧
      final.externalEffectCount = initial.externalEffectCount := by
  induction events generalizing initial with
  | nil => simp [RunAuthorityTransactionEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunAuthorityTransactionEvents] at run
      cases step : ApplyAuthorityTransactionEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          have custody :=
            accepted_authority_transaction_event_preserves_custody step
          have boundary :=
            accepted_authority_transaction_event_is_non_authorizing step
          have narrowed :=
            accepted_authority_transaction_event_never_widens_authority step
          have tailFacts := ih run
          rcases custody with ⟨transaction, handle, secretClass, purpose,
            destination, principal, kernel, declassifier, base⟩
          rcases boundary with ⟨_, _, _, support, effects⟩
          rcases tailFacts with ⟨ttransaction, thandle, tsecretClass, tpurpose,
            tdestination, tprincipal, tkernel, tdeclassifier, tbase, tnarrowed,
            tsupport, teffects⟩
          exact ⟨ttransaction.trans transaction, thandle.trans handle,
            tsecretClass.trans secretClass, tpurpose.trans purpose,
            tdestination.trans destination, tprincipal.trans principal,
            tkernel.trans kernel, tdeclassifier.trans declassifier,
            tbase.trans base, Nat.le_trans tnarrowed narrowed,
            tsupport.trans support, teffects.trans effects⟩

theorem authority_transaction_run_preserves_descendant_inventory
    {initial final : AuthorityTransactionState}
    {events : List AuthorityTransactionEvent}
    (run : RunAuthorityTransactionEvents initial events = some final) :
    final.descendantCount = initial.descendantCount ∧
      final.descendantIds = initial.descendantIds := by
  induction events generalizing initial with
  | nil =>
      simp [RunAuthorityTransactionEvents] at run
      subst final
      exact ⟨rfl, rfl⟩
  | cons event tail ih =>
      simp only [RunAuthorityTransactionEvents] at run
      cases step : ApplyAuthorityTransactionEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          have head :=
            accepted_authority_transaction_event_preserves_descendant_inventory step
          have rest := ih run
          exact ⟨rest.1.trans head.1, rest.2.trans head.2⟩

theorem successful_authority_transaction_run_has_valid_trace
    {initial final : AuthorityTransactionState}
    {events : List AuthorityTransactionEvent}
    (run : RunAuthorityTransactionEvents initial events = some final) :
    AuthorityTransactionTraceValid initial events := by
  induction events generalizing initial with
  | nil => trivial
  | cons event tail ih =>
      simp only [RunAuthorityTransactionEvents] at run
      cases step : ApplyAuthorityTransactionEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          exact ⟨next, step, ih run⟩

theorem revoked_authority_transaction_state_rejects_every_event
    (state : AuthorityTransactionState)
    (event : AuthorityTransactionEvent)
    (revoked : state.stage = AuthorityTransactionStage.revoked) :
    ¬ AuthorityTransactionEventAdmissible state event := by
  intro admissible
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  cases kind : event.kind <;> simp [kind, revoked] at route

theorem revoked_authority_transaction_state_has_no_nonempty_run
    (state : AuthorityTransactionState)
    (event : AuthorityTransactionEvent)
    (tail : List AuthorityTransactionEvent)
    (revoked : state.stage = AuthorityTransactionStage.revoked) :
    RunAuthorityTransactionEvents state (event :: tail) = none := by
  have rejected :=
    revoked_authority_transaction_state_rejects_every_event state event revoked
  simp [RunAuthorityTransactionEvents, ApplyAuthorityTransactionEvent, rejected]

theorem authority_transaction_runs_compose
    (initial : AuthorityTransactionState)
    (before after : List AuthorityTransactionEvent) :
    RunAuthorityTransactionEvents initial (before ++ after) =
      match RunAuthorityTransactionEvents initial before with
      | none => none
      | some middle => RunAuthorityTransactionEvents middle after := by
  induction before generalizing initial with
  | nil => simp [RunAuthorityTransactionEvents]
  | cons event tail ih =>
      simp only [List.cons_append, RunAuthorityTransactionEvents]
      cases step : ApplyAuthorityTransactionEvent initial event with
      | none => simp
      | some next => simp [ih]

def initialAuthorityTransactionState : AuthorityTransactionState := {
  transactionId := 79
  handleId := 83
  secretClassId := 89
  purposeId := 97
  destinationId := 101
  principalId := 103
  kernelId := 107
  declassifierId := 109
  version := 1
  baseAuthorityCeiling := 7
  currentAuthorityCeiling := 7
  stage := AuthorityTransactionStage.requested
  descendantCount := 3
  revokedDescendantCount := 0
  descendantIds := [113, 127, 131]
  revokedDescendantIds := []
  sanitizerReceiptCount := 0
  declassificationReceiptCount := 0
  zeroizationReceiptCount := 0
  commitReceiptCount := 0
  revocationReceiptCount := 0
  residualCount := 0
  expiresAt := 0
  now := 20
  supportAssignmentCount := 0
  externalEffectCount := 0
}

def issueAuthorityLeaseEvent : AuthorityTransactionEvent := {
  kind := AuthorityTransactionEventKind.issueLease
  transactionId := 79
  handleId := 83
  secretClassId := 89
  purposeId := 97
  destinationId := 101
  actorId := 103
  expectedVersion := 1
  targetVersion := 2
  requestedAuthorityCeiling := 5
  requestedExpiry := 40
  observedNow := 21
  approvalPresent := true
  contextScoped := false
  boundaryMediated := false
  substitutionAuthorized := false
  executionReceiptPresent := false
  outputContainsSecret := false
  outputContainsHandle := false
  sanitizerReceiptPresent := false
  declassificationReceiptPresent := false
  disclosureAuthorized := false
  zeroizationReceiptPresent := false
  commitReceiptPresent := false
  revocationReceiptPresent := false
  requestedRevokedDescendantCount := 0
  requestedRevokedDescendantIds := []
  residualPresent := false
  claimsSecurity := false
  requestsSupportAssignment := false
  requestsExternalEffect := false
}

def injectAuthoritySecretEvent : AuthorityTransactionEvent := {
  issueAuthorityLeaseEvent with
  kind := AuthorityTransactionEventKind.injectSecret
  actorId := 107
  expectedVersion := 2
  targetVersion := 2
  requestedAuthorityCeiling := 5
  contextScoped := true
  boundaryMediated := true
  substitutionAuthorized := true
  observedNow := 22
}

def recordAuthorityExecutionEvent : AuthorityTransactionEvent := {
  injectAuthoritySecretEvent with
  kind := AuthorityTransactionEventKind.recordExecution
  executionReceiptPresent := true
  observedNow := 23
}

def recordAuthoritySanitizationEvent : AuthorityTransactionEvent := {
  recordAuthorityExecutionEvent with
  kind := AuthorityTransactionEventKind.recordSanitization
  executionReceiptPresent := false
  sanitizerReceiptPresent := true
  observedNow := 24
}

def recordAuthorityDeclassificationEvent : AuthorityTransactionEvent := {
  recordAuthoritySanitizationEvent with
  kind := AuthorityTransactionEventKind.recordDeclassification
  actorId := 109
  sanitizerReceiptPresent := false
  declassificationReceiptPresent := true
  disclosureAuthorized := true
  observedNow := 25
}

def recordAuthorityZeroizationEvent : AuthorityTransactionEvent := {
  recordAuthorityDeclassificationEvent with
  kind := AuthorityTransactionEventKind.recordZeroization
  actorId := 107
  declassificationReceiptPresent := false
  disclosureAuthorized := false
  zeroizationReceiptPresent := true
  observedNow := 26
}

def commitAuthorityOutputEvent : AuthorityTransactionEvent := {
  recordAuthorityZeroizationEvent with
  kind := AuthorityTransactionEventKind.commitOutput
  zeroizationReceiptPresent := false
  commitReceiptPresent := true
  residualPresent := true
  observedNow := 27
}

def propagateAuthorityRevocationEvent : AuthorityTransactionEvent := {
  commitAuthorityOutputEvent with
  kind := AuthorityTransactionEventKind.propagateRevocation
  expectedVersion := 2
  targetVersion := 3
  requestedAuthorityCeiling := 0
  commitReceiptPresent := false
  revocationReceiptPresent := true
  requestedRevokedDescendantCount := 3
  requestedRevokedDescendantIds := [113, 127, 131]
  observedNow := 28
}

def completeAuthorityTransactionTrace : List AuthorityTransactionEvent :=
  [issueAuthorityLeaseEvent, injectAuthoritySecretEvent,
    recordAuthorityExecutionEvent, recordAuthoritySanitizationEvent,
    recordAuthorityDeclassificationEvent, recordAuthorityZeroizationEvent,
    commitAuthorityOutputEvent, propagateAuthorityRevocationEvent]

def committedAuthorityTransactionState : AuthorityTransactionState := {
  initialAuthorityTransactionState with
  version := 2
  currentAuthorityCeiling := 5
  stage := AuthorityTransactionStage.committed
  sanitizerReceiptCount := 1
  declassificationReceiptCount := 1
  zeroizationReceiptCount := 1
  commitReceiptCount := 1
  residualCount := 1
  expiresAt := 40
  now := 27
}

def substitutedDescendantRevocationEvent : AuthorityTransactionEvent := {
  propagateAuthorityRevocationEvent with
  requestedRevokedDescendantIds := [113, 127, 137]
}

def RevocationCountSummary (event : AuthorityTransactionEvent) : Nat :=
  event.requestedRevokedDescendantCount

def RevocationAdmitted
    (state : AuthorityTransactionState)
    (event : AuthorityTransactionEvent) : Bool :=
  decide (AuthorityTransactionEventAdmissible state event)

theorem complete_authority_transaction_prefix_reaches_exact_committed_state :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      [issueAuthorityLeaseEvent, injectAuthoritySecretEvent,
        recordAuthorityExecutionEvent, recordAuthoritySanitizationEvent,
        recordAuthorityDeclassificationEvent, recordAuthorityZeroizationEvent,
        commitAuthorityOutputEvent] = some committedAuthorityTransactionState := by
  decide

theorem complete_authority_transaction_trace_reaches_exact_revoked_state :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      completeAuthorityTransactionTrace =
      some {
        initialAuthorityTransactionState with
        version := 3
        currentAuthorityCeiling := 0
        stage := AuthorityTransactionStage.revoked
        revokedDescendantCount := 3
        revokedDescendantIds := [113, 127, 131]
        sanitizerReceiptCount := 1
        declassificationReceiptCount := 1
        zeroizationReceiptCount := 1
        commitReceiptCount := 1
        revocationReceiptCount := 1
        residualCount := 2
        expiresAt := 40
        now := 28
      } := by
  decide

theorem authority_transaction_stale_version_is_rejected :
    ApplyAuthorityTransactionEvent initialAuthorityTransactionState
      { issueAuthorityLeaseEvent with expectedVersion := 0 } = none := by
  decide

theorem authority_transaction_ambient_context_is_rejected :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      [issueAuthorityLeaseEvent,
        { injectAuthoritySecretEvent with contextScoped := false }] = none := by
  decide

theorem authority_transaction_unmediated_injection_is_rejected :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      [issueAuthorityLeaseEvent,
        { injectAuthoritySecretEvent with boundaryMediated := false }] = none := by
  decide

theorem authority_transaction_expired_injection_is_rejected :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      [issueAuthorityLeaseEvent,
        { injectAuthoritySecretEvent with observedNow := 40 }] = none := by
  decide

theorem authority_transaction_secret_output_is_rejected :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      [issueAuthorityLeaseEvent, injectAuthoritySecretEvent,
        recordAuthorityExecutionEvent,
        { recordAuthoritySanitizationEvent with outputContainsSecret := true }] =
      none := by
  decide

theorem authority_transaction_self_declassification_is_rejected :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      [issueAuthorityLeaseEvent, injectAuthoritySecretEvent,
        recordAuthorityExecutionEvent, recordAuthoritySanitizationEvent,
        { recordAuthorityDeclassificationEvent with actorId := 103 }] = none := by
  decide

theorem authority_transaction_commit_before_zeroization_is_rejected :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      [issueAuthorityLeaseEvent, injectAuthoritySecretEvent,
        recordAuthorityExecutionEvent, recordAuthoritySanitizationEvent,
        recordAuthorityDeclassificationEvent, commitAuthorityOutputEvent] = none := by
  decide

theorem authority_transaction_partial_descendant_revocation_is_rejected :
    RunAuthorityTransactionEvents initialAuthorityTransactionState
      [issueAuthorityLeaseEvent, injectAuthoritySecretEvent,
        recordAuthorityExecutionEvent, recordAuthoritySanitizationEvent,
        recordAuthorityDeclassificationEvent, recordAuthorityZeroizationEvent,
        commitAuthorityOutputEvent,
        { propagateAuthorityRevocationEvent with
          requestedRevokedDescendantCount := 2 }] = none := by
  decide

theorem authority_transaction_same_count_descendant_substitution_is_rejected :
    ApplyAuthorityTransactionEvent committedAuthorityTransactionState
      substitutedDescendantRevocationEvent = none := by
  decide

theorem authority_transaction_duplicate_descendant_inventory_is_rejected :
    ApplyAuthorityTransactionEvent
      { committedAuthorityTransactionState with
        descendantIds := [113, 113, 131] }
      { propagateAuthorityRevocationEvent with
        requestedRevokedDescendantIds := [113, 113, 131] } = none := by
  decide

theorem authority_transaction_revocation_count_summary_collides :
    RevocationCountSummary propagateAuthorityRevocationEvent =
        RevocationCountSummary substitutedDescendantRevocationEvent ∧
      propagateAuthorityRevocationEvent.requestedRevokedDescendantIds ≠
        substitutedDescendantRevocationEvent.requestedRevokedDescendantIds := by
  decide

theorem authority_transaction_exact_inventory_separates_count_collision :
    RevocationAdmitted committedAuthorityTransactionState
        propagateAuthorityRevocationEvent = true ∧
      RevocationAdmitted committedAuthorityTransactionState
        substitutedDescendantRevocationEvent = false := by
  decide

theorem no_exact_revocation_admission_classifier_from_count_only :
    ¬ ∃ classify : Nat → Bool,
      ∀ event : AuthorityTransactionEvent,
        classify (RevocationCountSummary event) =
          RevocationAdmitted committedAuthorityTransactionState event := by
  intro ⟨classify, exact⟩
  have good := exact propagateAuthorityRevocationEvent
  have bad := exact substitutedDescendantRevocationEvent
  have collision := authority_transaction_revocation_count_summary_collides
  have separated := authority_transaction_exact_inventory_separates_count_collision
  rw [separated.1] at good
  rw [separated.2] at bad
  rw [collision.1] at good
  simp_all

theorem authority_transaction_security_claim_laundering_is_rejected :
    ApplyAuthorityTransactionEvent initialAuthorityTransactionState
      { issueAuthorityLeaseEvent with claimsSecurity := true } = none := by
  decide

end AsiStackProofs.SecurityKernel

namespace AsiStackProofs.TypedJobs

inductive JobState where
  | draft
  | locked
  | awaitingApproval
  | dispatchable
  | running
  | adjudicating
  | delivered
  | failed
  | blocked
  | replayed
  | retired
deriving DecidableEq, Repr

structure JobTransition where
  fromState : JobState
  toState : JobState
deriving DecidableEq, Repr

def ValidTransition : JobTransition -> Prop
  | { fromState := .draft, toState := .locked } => True
  | { fromState := .locked, toState := .awaitingApproval } => True
  | { fromState := .locked, toState := .dispatchable } => True
  | { fromState := .awaitingApproval, toState := .dispatchable } => True
  | { fromState := .awaitingApproval, toState := .blocked } => True
  | { fromState := .dispatchable, toState := .running } => True
  | { fromState := .running, toState := .adjudicating } => True
  | { fromState := .running, toState := .failed } => True
  | { fromState := .running, toState := .blocked } => True
  | { fromState := .adjudicating, toState := .delivered } => True
  | { fromState := .delivered, toState := .replayed } => True
  | { fromState := .delivered, toState := .retired } => True
  | { fromState := .failed, toState := .retired } => True
  | { fromState := .blocked, toState := .retired } => True
  | { fromState := .replayed, toState := .retired } => True
  | _ => False

structure TransitionRecord where
  transition : JobTransition
  recordedAsValid : Bool
deriving DecidableEq, Repr

def TransitionRecordValid (record : TransitionRecord) : Prop :=
  record.recordedAsValid = true -> ValidTransition record.transition

theorem recorded_valid_job_transition_uses_declared_lifecycle_relation
    {record : TransitionRecord} :
    TransitionRecordValid record ->
    record.recordedAsValid = true ->
    ValidTransition record.transition := by
  intro valid markedValid
  exact valid markedValid

structure ApprovalRecord where
  approvalRequired : Bool
  approvalRecorded : Bool
  targetState : JobState
deriving DecidableEq, Repr

def ExecutionAllowed (record : ApprovalRecord) : Prop :=
  record.targetState = JobState.running ∧
    (record.approvalRequired = false ∨ record.approvalRecorded = true)

theorem job_requiring_approval_cannot_run_without_approval
    {record : ApprovalRecord} :
    record.approvalRequired = true ->
    record.approvalRecorded = false ->
    ¬ ExecutionAllowed record := by
  intro required missing allowed
  unfold ExecutionAllowed at allowed
  cases allowed.2 with
  | inl notRequired =>
      rw [required] at notRequired
      cases notRequired
  | inr approved =>
      rw [missing] at approved
      cases approved

inductive JobExecutionRoute where
  | rejectJob
  | requestContract
  | requireApproval
  | blockDispatch
  | routeToScheduler
  | runJob
  | adjudicateOutput
  | recordFailure
  | recordResidual
  | deliverEvidenceReady
  | retireJob
deriving DecidableEq, Repr

structure JobExecutionReview where
  jobPresent : Bool
  contractLocked : Bool
  lifecycleValid : Bool
  approvalRequired : Bool
  approvalRecorded : Bool
  permissionsSatisfied : Bool
  schedulerSlotAvailable : Bool
  dispatchRequested : Bool
  runningObserved : Bool
  outputDelivered : Bool
  verificationPassed : Bool
  residualKnown : Bool
  failureObserved : Bool
  retireRequested : Bool
deriving DecidableEq, Repr

def JobExecutionRouteFor
    (review : JobExecutionReview) : JobExecutionRoute :=
  if review.jobPresent = false then
    JobExecutionRoute.rejectJob
  else if review.contractLocked = false then
    JobExecutionRoute.requestContract
  else if review.lifecycleValid = false then
    JobExecutionRoute.blockDispatch
  else if review.approvalRequired = true ∧ review.approvalRecorded = false then
    JobExecutionRoute.requireApproval
  else if review.permissionsSatisfied = false then
    JobExecutionRoute.blockDispatch
  else if review.failureObserved = true then
    JobExecutionRoute.recordFailure
  else if review.residualKnown = true then
    JobExecutionRoute.recordResidual
  else if review.outputDelivered = true ∧ review.verificationPassed = false then
    JobExecutionRoute.adjudicateOutput
  else if review.outputDelivered = true ∧ review.verificationPassed = true then
    JobExecutionRoute.deliverEvidenceReady
  else if review.dispatchRequested = true ∧
      review.schedulerSlotAvailable = false then
    JobExecutionRoute.routeToScheduler
  else if review.dispatchRequested = true ∧
      review.schedulerSlotAvailable = true then
    JobExecutionRoute.runJob
  else if review.retireRequested = true then
    JobExecutionRoute.retireJob
  else
    JobExecutionRoute.requestContract

theorem missing_job_rejects_job_execution
    {review : JobExecutionReview} :
    review.jobPresent = false ->
    JobExecutionRouteFor review = JobExecutionRoute.rejectJob := by
  intro missingJob
  unfold JobExecutionRouteFor
  simp [missingJob]

theorem unlocked_contract_requests_job_contract
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = false ->
    JobExecutionRouteFor review = JobExecutionRoute.requestContract := by
  intro jobPresent contractUnlocked
  unfold JobExecutionRouteFor
  simp [jobPresent, contractUnlocked]

theorem invalid_lifecycle_blocks_job_dispatch
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = false ->
    JobExecutionRouteFor review = JobExecutionRoute.blockDispatch := by
  intro jobPresent contractLocked invalidLifecycle
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, invalidLifecycle]

theorem missing_approval_requires_job_approval
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = true ->
    review.approvalRecorded = false ->
    JobExecutionRouteFor review = JobExecutionRoute.requireApproval := by
  intro jobPresent contractLocked lifecycleValid approvalRequired
    approvalMissing
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalRequired,
    approvalMissing]

theorem missing_permissions_block_job_dispatch
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = false ->
    review.permissionsSatisfied = false ->
    JobExecutionRouteFor review = JobExecutionRoute.blockDispatch := by
  intro jobPresent contractLocked lifecycleValid approvalNotRequired
    permissionsMissing
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalNotRequired,
    permissionsMissing]

theorem observed_failure_records_job_failure
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = false ->
    review.permissionsSatisfied = true ->
    review.failureObserved = true ->
    JobExecutionRouteFor review = JobExecutionRoute.recordFailure := by
  intro jobPresent contractLocked lifecycleValid approvalNotRequired
    permissionsSatisfied failureObserved
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalNotRequired,
    permissionsSatisfied, failureObserved]

theorem known_job_residual_records_residual
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = false ->
    review.permissionsSatisfied = true ->
    review.failureObserved = false ->
    review.residualKnown = true ->
    JobExecutionRouteFor review = JobExecutionRoute.recordResidual := by
  intro jobPresent contractLocked lifecycleValid approvalNotRequired
    permissionsSatisfied noFailure residualKnown
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalNotRequired,
    permissionsSatisfied, noFailure, residualKnown]

theorem delivered_unverified_output_routes_to_adjudication
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = false ->
    review.permissionsSatisfied = true ->
    review.failureObserved = false ->
    review.residualKnown = false ->
    review.outputDelivered = true ->
    review.verificationPassed = false ->
    JobExecutionRouteFor review = JobExecutionRoute.adjudicateOutput := by
  intro jobPresent contractLocked lifecycleValid approvalNotRequired
    permissionsSatisfied noFailure noResidual outputDelivered
    verificationFailed
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalNotRequired,
    permissionsSatisfied, noFailure, noResidual, outputDelivered,
    verificationFailed]

theorem delivered_verified_output_is_evidence_ready
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = false ->
    review.permissionsSatisfied = true ->
    review.failureObserved = false ->
    review.residualKnown = false ->
    review.outputDelivered = true ->
    review.verificationPassed = true ->
    JobExecutionRouteFor review = JobExecutionRoute.deliverEvidenceReady := by
  intro jobPresent contractLocked lifecycleValid approvalNotRequired
    permissionsSatisfied noFailure noResidual outputDelivered verificationPassed
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalNotRequired,
    permissionsSatisfied, noFailure, noResidual, outputDelivered,
    verificationPassed]

theorem dispatch_without_scheduler_slot_routes_to_scheduler
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = false ->
    review.permissionsSatisfied = true ->
    review.failureObserved = false ->
    review.residualKnown = false ->
    review.outputDelivered = false ->
    review.dispatchRequested = true ->
    review.schedulerSlotAvailable = false ->
    JobExecutionRouteFor review = JobExecutionRoute.routeToScheduler := by
  intro jobPresent contractLocked lifecycleValid approvalNotRequired
    permissionsSatisfied noFailure noResidual noOutput dispatchRequested
    noSlot
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalNotRequired,
    permissionsSatisfied, noFailure, noResidual, noOutput, dispatchRequested,
    noSlot]

theorem dispatch_with_scheduler_slot_runs_job
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = false ->
    review.permissionsSatisfied = true ->
    review.failureObserved = false ->
    review.residualKnown = false ->
    review.outputDelivered = false ->
    review.dispatchRequested = true ->
    review.schedulerSlotAvailable = true ->
    JobExecutionRouteFor review = JobExecutionRoute.runJob := by
  intro jobPresent contractLocked lifecycleValid approvalNotRequired
    permissionsSatisfied noFailure noResidual noOutput dispatchRequested
    slotAvailable
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalNotRequired,
    permissionsSatisfied, noFailure, noResidual, noOutput, dispatchRequested,
    slotAvailable]

theorem complete_retirement_review_retires_job
    {review : JobExecutionReview} :
    review.jobPresent = true ->
    review.contractLocked = true ->
    review.lifecycleValid = true ->
    review.approvalRequired = false ->
    review.permissionsSatisfied = true ->
    review.failureObserved = false ->
    review.residualKnown = false ->
    review.outputDelivered = false ->
    review.dispatchRequested = false ->
    review.retireRequested = true ->
    JobExecutionRouteFor review = JobExecutionRoute.retireJob := by
  intro jobPresent contractLocked lifecycleValid approvalNotRequired
    permissionsSatisfied noFailure noResidual noOutput dispatchNotRequested
    retireRequested
  unfold JobExecutionRouteFor
  simp [jobPresent, contractLocked, lifecycleValid, approvalNotRequired,
    permissionsSatisfied, noFailure, noResidual, noOutput, dispatchNotRequested,
    retireRequested]

structure TypedJobDeliveryProbeSummary where
  verifiedDeliveryTracePresent : Bool
  deliveredNotEvidenceReadyTracePresent : Bool
  negativeControlsRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def TypedJobDeliveryProbeSummaryValid
    (summary : TypedJobDeliveryProbeSummary) : Prop :=
  summary.verifiedDeliveryTracePresent = true ∧
    summary.deliveredNotEvidenceReadyTracePresent = true ∧
    summary.negativeControlsRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

theorem typed_job_delivery_probe_fixture_bridge
    {summary : TypedJobDeliveryProbeSummary} :
    TypedJobDeliveryProbeSummaryValid summary ->
      summary.verifiedDeliveryTracePresent = true ∧
        summary.deliveredNotEvidenceReadyTracePresent = true ∧
        summary.negativeControlsRejected = true ∧
        summary.supportStateEffectNone = true ∧
        summary.nonClaimBoundary = true := by
  intro valid
  exact valid

inductive DurableLifecycleOutcome where
  | acceptEvidenceReadyRetry
  | acceptBlockedLeaseExpiry
  | rejectMissingIdempotency
  | rejectAuthorityWidening
  | rejectPermissionOverreach
  | rejectExpiredLeaseDispatch
  | rejectMissingCompletionReceipt
  | rejectMissingReplayRef
  | rejectMissingResidualOwner
  | rejectMissingNonClaimBoundary
  | rejectSupportPromotion
deriving DecidableEq, Repr

structure DurableLifecycleReview where
  retryAttempted : Bool
  idempotencyKeyPresent : Bool
  authorityUnchanged : Bool
  permissionsSatisfied : Bool
  leaseActive : Bool
  dispatchRequested : Bool
  outputDelivered : Bool
  evidenceReadyRequested : Bool
  completionReceiptPresent : Bool
  replayRefPresent : Bool
  blockedTrace : Bool
  residualOwnerPresent : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def DurableLifecycleRouteFor
    (review : DurableLifecycleReview) : DurableLifecycleOutcome :=
  if review.supportStateEffectNone = false then
    DurableLifecycleOutcome.rejectSupportPromotion
  else if review.nonClaimBoundary = false then
    DurableLifecycleOutcome.rejectMissingNonClaimBoundary
  else if review.retryAttempted = true ∧
      review.idempotencyKeyPresent = false then
    DurableLifecycleOutcome.rejectMissingIdempotency
  else if review.retryAttempted = true ∧
      review.authorityUnchanged = false then
    DurableLifecycleOutcome.rejectAuthorityWidening
  else if review.permissionsSatisfied = false then
    DurableLifecycleOutcome.rejectPermissionOverreach
  else if review.dispatchRequested = true ∧ review.leaseActive = false then
    DurableLifecycleOutcome.rejectExpiredLeaseDispatch
  else if review.evidenceReadyRequested = true ∧
      review.completionReceiptPresent = false then
    DurableLifecycleOutcome.rejectMissingCompletionReceipt
  else if review.evidenceReadyRequested = true ∧
      review.replayRefPresent = false then
    DurableLifecycleOutcome.rejectMissingReplayRef
  else if review.blockedTrace = true ∧ review.residualOwnerPresent = false then
    DurableLifecycleOutcome.rejectMissingResidualOwner
  else if review.retryAttempted = true ∧
      review.evidenceReadyRequested = true ∧
      review.outputDelivered = true then
    DurableLifecycleOutcome.acceptEvidenceReadyRetry
  else if review.blockedTrace = true ∧
      review.leaseActive = false ∧
      review.residualOwnerPresent = true then
    DurableLifecycleOutcome.acceptBlockedLeaseExpiry
  else
    DurableLifecycleOutcome.rejectMissingCompletionReceipt

theorem durable_retry_without_idempotency_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = true ->
    review.idempotencyKeyPresent = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectMissingIdempotency := by
  intro supportStateNone nonClaim retry missingKey
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, retry, missingKey]

theorem durable_retry_authority_widening_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = true ->
    review.idempotencyKeyPresent = true ->
    review.authorityUnchanged = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectAuthorityWidening := by
  intro supportStateNone nonClaim retry keyPresent authorityWidened
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, retry, keyPresent, authorityWidened]

theorem durable_retry_permission_overreach_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = true ->
    review.idempotencyKeyPresent = true ->
    review.authorityUnchanged = true ->
    review.permissionsSatisfied = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectPermissionOverreach := by
  intro supportStateNone nonClaim retry keyPresent authorityUnchanged
    permissionsMissing
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, retry, keyPresent, authorityUnchanged,
    permissionsMissing]

theorem durable_expired_lease_dispatch_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = false ->
    review.permissionsSatisfied = true ->
    review.dispatchRequested = true ->
    review.leaseActive = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectExpiredLeaseDispatch := by
  intro supportStateNone nonClaim noRetry permissionsSatisfied
    dispatchRequested leaseExpired
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, noRetry, permissionsSatisfied,
    dispatchRequested, leaseExpired]

theorem durable_evidence_ready_missing_completion_receipt_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = false ->
    review.permissionsSatisfied = true ->
    review.dispatchRequested = true ->
    review.leaseActive = true ->
    review.evidenceReadyRequested = true ->
    review.completionReceiptPresent = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectMissingCompletionReceipt := by
  intro supportStateNone nonClaim noRetry permissionsSatisfied
    dispatchRequested leaseActive evidenceReady missingReceipt
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, noRetry, permissionsSatisfied,
    dispatchRequested, leaseActive, evidenceReady, missingReceipt]

theorem durable_evidence_ready_missing_replay_ref_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = false ->
    review.permissionsSatisfied = true ->
    review.dispatchRequested = true ->
    review.leaseActive = true ->
    review.evidenceReadyRequested = true ->
    review.completionReceiptPresent = true ->
    review.replayRefPresent = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectMissingReplayRef := by
  intro supportStateNone nonClaim noRetry permissionsSatisfied
    dispatchRequested leaseActive evidenceReady receiptPresent missingReplay
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, noRetry, permissionsSatisfied,
    dispatchRequested, leaseActive, evidenceReady, receiptPresent,
    missingReplay]

theorem durable_blocked_without_residual_owner_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = false ->
    review.permissionsSatisfied = true ->
    review.dispatchRequested = false ->
    review.evidenceReadyRequested = false ->
    review.blockedTrace = true ->
    review.residualOwnerPresent = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectMissingResidualOwner := by
  intro supportStateNone nonClaim noRetry permissionsSatisfied
    dispatchNotRequested notEvidenceReady blocked missingResidualOwner
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, noRetry, permissionsSatisfied,
    dispatchNotRequested, notEvidenceReady, blocked, missingResidualOwner]

theorem durable_missing_non_claim_boundary_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectMissingNonClaimBoundary := by
  intro supportStateNone missingBoundary
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, missingBoundary]

theorem durable_support_promotion_rejected
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = false ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.rejectSupportPromotion := by
  intro supportPromotion
  unfold DurableLifecycleRouteFor
  simp [supportPromotion]

theorem durable_retry_complete_trace_accepted
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = true ->
    review.idempotencyKeyPresent = true ->
    review.authorityUnchanged = true ->
    review.permissionsSatisfied = true ->
    review.dispatchRequested = true ->
    review.leaseActive = true ->
    review.evidenceReadyRequested = true ->
    review.completionReceiptPresent = true ->
    review.replayRefPresent = true ->
    review.blockedTrace = false ->
    review.outputDelivered = true ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.acceptEvidenceReadyRetry := by
  intro supportStateNone nonClaim retry keyPresent authorityUnchanged
    permissionsSatisfied dispatchRequested leaseActive evidenceReady
    receiptPresent replayPresent notBlocked outputDelivered
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, retry, keyPresent, authorityUnchanged,
    permissionsSatisfied, dispatchRequested, leaseActive, evidenceReady,
    receiptPresent, replayPresent, notBlocked, outputDelivered]

theorem durable_expired_lease_blocked_trace_accepted
    {review : DurableLifecycleReview} :
    review.supportStateEffectNone = true ->
    review.nonClaimBoundary = true ->
    review.retryAttempted = false ->
    review.permissionsSatisfied = true ->
    review.dispatchRequested = false ->
    review.evidenceReadyRequested = false ->
    review.blockedTrace = true ->
    review.leaseActive = false ->
    review.residualOwnerPresent = true ->
    DurableLifecycleRouteFor review =
      DurableLifecycleOutcome.acceptBlockedLeaseExpiry := by
  intro supportStateNone nonClaim noRetry permissionsSatisfied
    dispatchNotRequested notEvidenceReady blocked leaseExpired residualOwner
  unfold DurableLifecycleRouteFor
  simp [supportStateNone, nonClaim, noRetry, permissionsSatisfied,
    dispatchNotRequested, notEvidenceReady, blocked, leaseExpired,
    residualOwner]

structure TypedJobDurableLifecycleProbeSummary where
  retryResumeTracePresent : Bool
  expiredLeaseBlockTracePresent : Bool
  negativeControlsRejected : Bool
  completionAndReplayBoundaries : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def TypedJobDurableLifecycleProbeSummaryValid
    (summary : TypedJobDurableLifecycleProbeSummary) : Prop :=
  summary.retryResumeTracePresent = true ∧
    summary.expiredLeaseBlockTracePresent = true ∧
    summary.negativeControlsRejected = true ∧
    summary.completionAndReplayBoundaries = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

theorem typed_job_durable_lifecycle_probe_fixture_bridge
    {summary : TypedJobDurableLifecycleProbeSummary} :
    TypedJobDurableLifecycleProbeSummaryValid summary ->
      summary.retryResumeTracePresent = true ∧
        summary.expiredLeaseBlockTracePresent = true ∧
        summary.negativeControlsRejected = true ∧
        summary.completionAndReplayBoundaries = true ∧
        summary.supportStateEffectNone = true ∧
        summary.nonClaimBoundary = true := by
  intro valid
  exact valid

end AsiStackProofs.TypedJobs

namespace AsiStackProofs.ContextTransactions

structure MemoryEvent where
  eventId : String
  committed : Bool
deriving DecidableEq, Repr

structure SnapshotView where
  visibleEventIds : List String
deriving DecidableEq, Repr

def EventVisibleInSnapshot
    (event : MemoryEvent) (snapshot : SnapshotView) : Prop :=
  event.eventId ∈ snapshot.visibleEventIds

structure SnapshotRead where
  event : MemoryEvent
  snapshot : SnapshotView
deriving DecidableEq, Repr

def SnapshotReadValid (read : SnapshotRead) : Prop :=
  read.event.committed = true ∧
    EventVisibleInSnapshot read.event read.snapshot

theorem snapshot_read_sees_committed_event_in_declared_view
    {read : SnapshotRead} :
    SnapshotReadValid read ->
      read.event.committed = true ∧
        EventVisibleInSnapshot read.event read.snapshot := by
  intro valid
  exact valid

structure DerivedContext where
  sourceTainted : Bool
  declassificationAuthorized : Bool
  derivedTainted : Bool
deriving DecidableEq, Repr

def TaintPropagationValid (context : DerivedContext) : Prop :=
  context.sourceTainted = true ->
    context.declassificationAuthorized = false ->
    context.derivedTainted = true

theorem tainted_source_taints_derivative_without_declassification
    {context : DerivedContext} :
    TaintPropagationValid context ->
    context.sourceTainted = true ->
    context.declassificationAuthorized = false ->
    context.derivedTainted = true := by
  intro valid sourceTainted noDeclassification
  exact valid sourceTainted noDeclassification

theorem untainted_derivative_from_tainted_source_requires_declassification
    {context : DerivedContext} :
    TaintPropagationValid context ->
    context.sourceTainted = true ->
    context.derivedTainted = false ->
    context.declassificationAuthorized = true := by
  intro valid sourceTainted derivedUntainted
  cases declassification : context.declassificationAuthorized with
  | false =>
      have mustTaint :
          context.derivedTainted = true :=
        valid sourceTainted declassification
      rw [derivedUntainted] at mustTaint
      cases mustTaint
  | true =>
      rfl

structure ContextMaterializationRecord where
  materializationReady : Bool
  deletionObligationOpen : Bool
  deletionClosureRecorded : Bool
  declassificationAuthorized : Bool
  residualRecordPresent : Bool
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def DeletionClosureSatisfied (record : ContextMaterializationRecord) : Prop :=
  record.deletionObligationOpen = false ∨
    record.deletionClosureRecorded = true ∨
      record.declassificationAuthorized = true

def ContextMaterializationAllowed (record : ContextMaterializationRecord) : Prop :=
  record.materializationReady = true ∧
    record.nonClaimsPresent = true ∧
      DeletionClosureSatisfied record

inductive ContextMaterializationRoute where
  | materialize
  | blockForDeletionClosure
  | holdForResidual
  | blockForResidualRecord
deriving DecidableEq, Repr

def ContextMaterializationRouteFor
    (record : ContextMaterializationRecord) : ContextMaterializationRoute :=
  if record.materializationReady then
    if record.deletionObligationOpen &&
        !record.deletionClosureRecorded &&
          !record.declassificationAuthorized then
      ContextMaterializationRoute.blockForDeletionClosure
    else
      ContextMaterializationRoute.materialize
  else if record.residualRecordPresent then
    ContextMaterializationRoute.holdForResidual
  else
    ContextMaterializationRoute.blockForResidualRecord

theorem open_deletion_without_closure_or_declassification_blocks_materialization
    {record : ContextMaterializationRecord} :
    record.deletionObligationOpen = true ->
    record.deletionClosureRecorded = false ->
    record.declassificationAuthorized = false ->
    ¬ ContextMaterializationAllowed record := by
  intro openDeletion missingClosure noDeclassification allowed
  rcases allowed with ⟨_ready, _nonClaims, closureSatisfied⟩
  unfold DeletionClosureSatisfied at closureSatisfied
  rcases closureSatisfied with noOpenDeletion | closureRecorded | declassified
  · rw [openDeletion] at noOpenDeletion
    cases noOpenDeletion
  · rw [missingClosure] at closureRecorded
    cases closureRecorded
  · rw [noDeclassification] at declassified
    cases declassified

theorem ready_open_deletion_without_closure_routes_to_deletion_block
    {record : ContextMaterializationRecord} :
    record.materializationReady = true ->
    record.deletionObligationOpen = true ->
    record.deletionClosureRecorded = false ->
    record.declassificationAuthorized = false ->
    ContextMaterializationRouteFor record =
      ContextMaterializationRoute.blockForDeletionClosure := by
  intro ready openDeletion missingClosure noDeclassification
  unfold ContextMaterializationRouteFor
  rw [ready, openDeletion, missingClosure, noDeclassification]
  simp

inductive ContextTransactionRoute where
  | rejectMissingSnapshot
  | rejectStaleSnapshot
  | rejectBranchLeak
  | rejectMountFault
  | requestTaintReview
  | blockDeletedMaterialization
  | rejectInvisibleCommittedRead
  | requestReplayBoundary
  | requestEvidenceTransition
  | requestNonClaimBoundary
  | admitCommittedRead
deriving DecidableEq, Repr

structure ContextTransactionReview where
  snapshotPresent : Bool
  snapshotCurrent : Bool
  sourceBranchMatches : Bool
  targetBranchMatches : Bool
  mountPolicySatisfied : Bool
  mountRepairRecorded : Bool
  sourceTainted : Bool
  declassificationRecorded : Bool
  materializesDeletedCell : Bool
  deletionClosureRecorded : Bool
  committedRead : Bool
  readSetVisible : Bool
  replayBoundaryRecorded : Bool
  supportPromotionRequested : Bool
  evidenceTransitionRecorded : Bool
  nonClaimsRecorded : Bool
deriving DecidableEq, Repr

def ContextTransactionRouteFor
    (review : ContextTransactionReview) : ContextTransactionRoute :=
  if review.snapshotPresent = false then
    ContextTransactionRoute.rejectMissingSnapshot
  else if review.snapshotCurrent = false then
    ContextTransactionRoute.rejectStaleSnapshot
  else if review.sourceBranchMatches = false ∨
      review.targetBranchMatches = false then
    ContextTransactionRoute.rejectBranchLeak
  else if review.mountPolicySatisfied = false ∧
      review.mountRepairRecorded = false then
    ContextTransactionRoute.rejectMountFault
  else if review.sourceTainted = true ∧
      review.declassificationRecorded = false then
    ContextTransactionRoute.requestTaintReview
  else if review.materializesDeletedCell = true ∧
      review.deletionClosureRecorded = false then
    ContextTransactionRoute.blockDeletedMaterialization
  else if review.committedRead = true ∧
      review.readSetVisible = false then
    ContextTransactionRoute.rejectInvisibleCommittedRead
  else if review.replayBoundaryRecorded = false then
    ContextTransactionRoute.requestReplayBoundary
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionRecorded = false then
    ContextTransactionRoute.requestEvidenceTransition
  else if review.nonClaimsRecorded = false then
    ContextTransactionRoute.requestNonClaimBoundary
  else
    ContextTransactionRoute.admitCommittedRead

theorem missing_snapshot_rejects_context_transaction
    {review : ContextTransactionReview} :
    review.snapshotPresent = false ->
      ContextTransactionRouteFor review =
        ContextTransactionRoute.rejectMissingSnapshot := by
  intro missingSnapshot
  unfold ContextTransactionRouteFor
  simp [missingSnapshot]

theorem stale_snapshot_rejects_context_transaction
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = false ->
        ContextTransactionRouteFor review =
          ContextTransactionRoute.rejectStaleSnapshot := by
  intro snapshotPresent staleSnapshot
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, staleSnapshot]

theorem source_branch_mismatch_rejects_context_transaction
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = false ->
          ContextTransactionRouteFor review =
            ContextTransactionRoute.rejectBranchLeak := by
  intro snapshotPresent snapshotCurrent sourceMismatch
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMismatch]

theorem target_branch_mismatch_rejects_context_transaction
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = false ->
            ContextTransactionRouteFor review =
              ContextTransactionRoute.rejectBranchLeak := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMismatch
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMismatch]

theorem mount_fault_without_repair_rejects_context_transaction
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = true ->
            review.mountPolicySatisfied = false ->
              review.mountRepairRecorded = false ->
                ContextTransactionRouteFor review =
                  ContextTransactionRoute.rejectMountFault := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMatches
    mountFault missingRepair
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMatches,
    mountFault, missingRepair]

theorem tainted_transaction_without_declassification_routes_to_review
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = true ->
            review.mountPolicySatisfied = true ->
              review.sourceTainted = true ->
                review.declassificationRecorded = false ->
                  ContextTransactionRouteFor review =
                    ContextTransactionRoute.requestTaintReview := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMatches
    mountSatisfied tainted missingDeclassification
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMatches,
    mountSatisfied, tainted, missingDeclassification]

theorem deleted_cell_without_closure_blocks_materialization_route
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = true ->
            review.mountPolicySatisfied = true ->
              review.sourceTainted = false ->
                review.materializesDeletedCell = true ->
                  review.deletionClosureRecorded = false ->
                    ContextTransactionRouteFor review =
                      ContextTransactionRoute.blockDeletedMaterialization := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMatches
    mountSatisfied untainted deletedCell missingClosure
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMatches,
    mountSatisfied, untainted, deletedCell, missingClosure]

theorem committed_read_without_visible_read_set_rejected
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = true ->
            review.mountPolicySatisfied = true ->
              review.sourceTainted = false ->
                review.materializesDeletedCell = false ->
                  review.committedRead = true ->
                    review.readSetVisible = false ->
                      ContextTransactionRouteFor review =
                        ContextTransactionRoute.rejectInvisibleCommittedRead := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMatches
    mountSatisfied untainted noDeletedCell committedRead invisibleReadSet
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMatches,
    mountSatisfied, untainted, noDeletedCell, committedRead, invisibleReadSet]

theorem missing_replay_boundary_requests_replay_boundary
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = true ->
            review.mountPolicySatisfied = true ->
              review.sourceTainted = false ->
                review.materializesDeletedCell = false ->
                  review.committedRead = true ->
                    review.readSetVisible = true ->
                      review.replayBoundaryRecorded = false ->
                        ContextTransactionRouteFor review =
                          ContextTransactionRoute.requestReplayBoundary := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMatches
    mountSatisfied untainted noDeletedCell committedRead visibleReadSet
    missingReplayBoundary
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMatches,
    mountSatisfied, untainted, noDeletedCell, committedRead, visibleReadSet,
    missingReplayBoundary]

theorem support_promotion_without_transition_requests_evidence_transition
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = true ->
            review.mountPolicySatisfied = true ->
              review.sourceTainted = false ->
                review.materializesDeletedCell = false ->
                  review.committedRead = true ->
                    review.readSetVisible = true ->
                      review.replayBoundaryRecorded = true ->
                        review.supportPromotionRequested = true ->
                          review.evidenceTransitionRecorded = false ->
                            ContextTransactionRouteFor review =
                              ContextTransactionRoute.requestEvidenceTransition := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMatches
    mountSatisfied untainted noDeletedCell committedRead visibleReadSet
    replayBoundary supportPromotion missingTransition
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMatches,
    mountSatisfied, untainted, noDeletedCell, committedRead, visibleReadSet,
    replayBoundary, supportPromotion, missingTransition]

theorem missing_non_claim_boundary_requests_non_claim_boundary
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = true ->
            review.mountPolicySatisfied = true ->
              review.sourceTainted = false ->
                review.materializesDeletedCell = false ->
                  review.committedRead = true ->
                    review.readSetVisible = true ->
                      review.replayBoundaryRecorded = true ->
                        review.supportPromotionRequested = false ->
                          review.nonClaimsRecorded = false ->
                            ContextTransactionRouteFor review =
                              ContextTransactionRoute.requestNonClaimBoundary := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMatches
    mountSatisfied untainted noDeletedCell committedRead visibleReadSet
    replayBoundary noPromotion missingNonClaims
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMatches,
    mountSatisfied, untainted, noDeletedCell, committedRead, visibleReadSet,
    replayBoundary, noPromotion, missingNonClaims]

theorem complete_context_transaction_admits_committed_read
    {review : ContextTransactionReview} :
    review.snapshotPresent = true ->
      review.snapshotCurrent = true ->
        review.sourceBranchMatches = true ->
          review.targetBranchMatches = true ->
            review.mountPolicySatisfied = true ->
              review.sourceTainted = false ->
                review.materializesDeletedCell = false ->
                  review.committedRead = true ->
                    review.readSetVisible = true ->
                      review.replayBoundaryRecorded = true ->
                        review.supportPromotionRequested = false ->
                          review.nonClaimsRecorded = true ->
                            ContextTransactionRouteFor review =
                              ContextTransactionRoute.admitCommittedRead := by
  intro snapshotPresent snapshotCurrent sourceMatches targetMatches
    mountSatisfied untainted noDeletedCell committedRead visibleReadSet
    replayBoundary noPromotion nonClaims
  unfold ContextTransactionRouteFor
  simp [snapshotPresent, snapshotCurrent, sourceMatches, targetMatches,
    mountSatisfied, untainted, noDeletedCell, committedRead, visibleReadSet,
    replayBoundary, noPromotion, nonClaims]

structure MemoryStoreHarnessSummary where
  validFixtureCount : Nat
  expectedInvalidFixtureCount : Nat
  readVisibilityChecked : Bool
  branchIsolationChecked : Bool
  mountVisibilityChecked : Bool
  deletionClosureChecked : Bool
  taintPropagationChecked : Bool
  replayBoundaryRecorded : Bool
  unauthorizedMountRejected : Bool
  deletedMaterializationRejected : Bool
  supportPromotionRejected : Bool
  chapterCoreSupportPromoted : Bool
deriving DecidableEq, Repr

def MemoryStoreHarnessSummaryAccepted
    (summary : MemoryStoreHarnessSummary) : Prop :=
  summary.validFixtureCount = 3 ∧
    summary.expectedInvalidFixtureCount = 6 ∧
      summary.readVisibilityChecked = true ∧
        summary.branchIsolationChecked = true ∧
          summary.mountVisibilityChecked = true ∧
            summary.deletionClosureChecked = true ∧
              summary.taintPropagationChecked = true ∧
                summary.replayBoundaryRecorded = true ∧
                  summary.unauthorizedMountRejected = true ∧
                    summary.deletedMaterializationRejected = true ∧
                      summary.supportPromotionRejected = true ∧
                        summary.chapterCoreSupportPromoted = false

def currentMemoryStoreHarnessSummary : MemoryStoreHarnessSummary :=
  {
    validFixtureCount := 3
    expectedInvalidFixtureCount := 6
    readVisibilityChecked := true
    branchIsolationChecked := true
    mountVisibilityChecked := true
    deletionClosureChecked := true
    taintPropagationChecked := true
    replayBoundaryRecorded := true
    unauthorizedMountRejected := true
    deletedMaterializationRejected := true
    supportPromotionRejected := true
    chapterCoreSupportPromoted := false
  }

theorem current_memory_store_harness_summary_accepted :
    MemoryStoreHarnessSummaryAccepted currentMemoryStoreHarnessSummary := by
  unfold MemoryStoreHarnessSummaryAccepted currentMemoryStoreHarnessSummary
  simp

theorem accepted_memory_store_harness_summary_requires_invalid_controls
    {summary : MemoryStoreHarnessSummary} :
    MemoryStoreHarnessSummaryAccepted summary ->
      summary.expectedInvalidFixtureCount = 6 := by
  intro accepted
  rcases accepted with ⟨_validCount, invalidCount, _readVisibility,
    _branchIsolation, _mountVisibility, _deletionClosure, _taintPropagation,
    _replayBoundary, _unauthorizedMount, _deletedMaterialization,
    _supportPromotion, _noCorePromotion⟩
  exact invalidCount

theorem memory_store_harness_summary_with_support_promotion_rejected
    {summary : MemoryStoreHarnessSummary} :
    summary.chapterCoreSupportPromoted = true ->
      ¬ MemoryStoreHarnessSummaryAccepted summary := by
  intro promoted accepted
  rcases accepted with ⟨_validCount, _invalidCount, _readVisibility,
    _branchIsolation, _mountVisibility, _deletionClosure, _taintPropagation,
    _replayBoundary, _unauthorizedMount, _deletedMaterialization,
    _supportPromotion, noCorePromotion⟩
  rw [promoted] at noCorePromotion
  cases noCorePromotion

end AsiStackProofs.ContextTransactions

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

end AsiStackProofs.ContextTransactions

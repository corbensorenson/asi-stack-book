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

end AsiStackProofs.ContextTransactions

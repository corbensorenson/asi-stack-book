namespace AsiStackProofs.VirtualContextABI

structure ContextReference where
  semanticAddress : String
  version : String
  snapshotId : String
deriving DecidableEq, Repr

structure SnapshotBinding where
  semanticAddress : String
  version : String
  snapshotId : String
deriving DecidableEq, Repr

def ReferenceMatchesBinding
    (reference : ContextReference) (binding : SnapshotBinding) : Prop :=
  binding.semanticAddress = reference.semanticAddress ∧
    binding.version = reference.version ∧
    binding.snapshotId = reference.snapshotId

def SnapshotContains
    (reference : ContextReference) (bindings : List SnapshotBinding) : Prop :=
  ∃ binding, binding ∈ bindings ∧ ReferenceMatchesBinding reference binding

inductive ResolutionState where
  | resolved
  | miss
deriving DecidableEq, Repr

structure ResolutionRecord where
  reference : ContextReference
  bindings : List SnapshotBinding
  state : ResolutionState
deriving DecidableEq, Repr

def ResolutionValid (record : ResolutionRecord) : Prop :=
  record.state = ResolutionState.resolved ->
    SnapshotContains record.reference record.bindings

theorem resolved_context_reference_has_valid_snapshot_binding
    {record : ResolutionRecord} :
    ResolutionValid record ->
    record.state = ResolutionState.resolved ->
    SnapshotContains record.reference record.bindings := by
  intro valid resolved
  exact valid resolved

inductive FaultState where
  | none
  | typedFault
  | residual
  | quarantine
deriving DecidableEq, Repr

structure LookupRecord where
  mandatory : Bool
  resolved : Bool
  faultState : FaultState
  materializationEmitted : Bool
deriving DecidableEq, Repr

def MandatoryMissHandled (lookup : LookupRecord) : Prop :=
  lookup.mandatory = true ->
    lookup.resolved = false ->
    lookup.faultState = FaultState.typedFault ∧
      lookup.materializationEmitted = false

theorem mandatory_context_miss_produces_typed_fault_not_best_effort
    {lookup : LookupRecord} :
    MandatoryMissHandled lookup ->
    lookup.mandatory = true ->
    lookup.resolved = false ->
    lookup.faultState = FaultState.typedFault ∧
      lookup.materializationEmitted = false := by
  intro handled mandatory miss
  exact handled mandatory miss

end AsiStackProofs.VirtualContextABI

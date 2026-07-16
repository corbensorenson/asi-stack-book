namespace AsiStackProofs.ContextTransactionRefinement

/-!
Finite reachable snapshot/write/commit/read/derive/materialize semantics.
Numeric identities, policy decisions, taint and deletion facts, authority
epochs, and receipts are trusted abstract inputs. The model does not establish
deployed storage, serializability, content truth, erasure, or side-channel safety.
-/

inductive TransactionStage where
  | raw | snapshotBound | writeStaged | committed | readVisible | derived
  | materialized | blocked | quarantined
deriving DecidableEq, Repr

inductive TransactionEventKind where
  | bindSnapshot | stageWrite | commitWrite | readSnapshot | deriveContext
  | materialize | block | quarantine
deriving DecidableEq, Repr

structure TransactionState where
  stage : TransactionStage
  transactionId : Nat
  snapshotId : Nat
  snapshotEpoch : Nat
  branchId : Nat
  mountId : Nat
  cellId : Nat
  authorityEpoch : Nat
  committedVersion : Nat
  visibleVersion : Nat
  sourceTainted : Bool
  derivedTainted : Bool
  declassificationAuthorized : Bool
  deletionObligationOpen : Bool
  deletionClosureReceipt : Bool
  snapshotReceipt : Bool
  writeReceipt : Bool
  commitReceipt : Bool
  readReceipt : Bool
  derivationReceipt : Bool
  replayReceipt : Bool
  auditReceipt : Bool
  materializationReceipt : Bool
  evidenceTransitionReceipt : Bool
  materialized : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure TransactionEvent where
  kind : TransactionEventKind
  fromStage : TransactionStage
  toStage : TransactionStage
  transactionId : Nat
  snapshotId : Nat
  snapshotEpoch : Nat
  branchId : Nat
  mountId : Nat
  cellId : Nat
  authorityEpoch : Nat
  inputVersion : Nat
  outputVersion : Nat
  snapshotPresent : Bool
  snapshotCurrent : Bool
  branchMatches : Bool
  mountPermitted : Bool
  writeCommitted : Bool
  readVisible : Bool
  sourceTainted : Bool
  derivedTainted : Bool
  declassificationAuthorized : Bool
  declassificationReceipt : Bool
  deletionObligationOpen : Bool
  deletionClosureReceipt : Bool
  snapshotReceipt : Bool
  writeReceipt : Bool
  commitReceipt : Bool
  readReceipt : Bool
  derivationReceipt : Bool
  replayReceipt : Bool
  auditReceipt : Bool
  materializationReceipt : Bool
  supportPromotionRequested : Bool
  evidenceTransitionReceipt : Bool
  materialized : Bool
  blockReceipt : Bool
  quarantineReceipt : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def SnapshotIdentityMatches (state : TransactionState) (event : TransactionEvent) : Bool :=
  decide (event.transactionId = state.transactionId) &&
    decide (event.snapshotId = state.snapshotId) &&
    decide (event.snapshotEpoch = state.snapshotEpoch) &&
    decide (event.branchId = state.branchId) &&
    decide (event.mountId = state.mountId) &&
    decide (event.authorityEpoch = state.authorityEpoch)

def CellIdentityMatches (state : TransactionState) (event : TransactionEvent) : Bool :=
  SnapshotIdentityMatches state event && decide (event.cellId = state.cellId)

def TransactionEventSpecificValid (state : TransactionState) (event : TransactionEvent) : Bool :=
  match event.kind with
  | .bindSnapshot =>
      decide (event.fromStage = .raw) && decide (event.toStage = .snapshotBound) &&
        decide (0 < event.transactionId) && decide (0 < event.snapshotId) &&
        decide (0 < event.snapshotEpoch) && decide (0 < event.branchId) &&
        decide (0 < event.mountId) && decide (0 < event.authorityEpoch) &&
        event.snapshotPresent && event.snapshotCurrent && event.branchMatches &&
        event.mountPermitted && event.snapshotReceipt && event.replayReceipt &&
        event.auditReceipt && !event.materialized
  | .stageWrite =>
      decide (event.fromStage = .snapshotBound) && decide (event.toStage = .writeStaged) &&
        SnapshotIdentityMatches state event && decide (0 < event.cellId) &&
        decide (event.inputVersion = state.committedVersion) && event.writeReceipt &&
        event.branchMatches && event.mountPermitted && !event.materialized
  | .commitWrite =>
      decide (event.fromStage = .writeStaged) && decide (event.toStage = .committed) &&
        CellIdentityMatches state event &&
        decide (event.inputVersion = state.committedVersion) &&
        decide (event.outputVersion = state.committedVersion + 1) &&
        event.writeCommitted && event.commitReceipt && event.auditReceipt &&
        !event.materialized
  | .readSnapshot =>
      decide (event.fromStage = .committed) && decide (event.toStage = .readVisible) &&
        CellIdentityMatches state event &&
        decide (event.inputVersion = state.committedVersion) &&
        event.writeCommitted && event.readVisible && event.readReceipt &&
        event.replayReceipt && event.branchMatches && event.mountPermitted &&
        !event.materialized
  | .deriveContext =>
      decide (event.fromStage = .readVisible) && decide (event.toStage = .derived) &&
        CellIdentityMatches state event &&
        decide (event.inputVersion = state.visibleVersion) &&
        decide (event.sourceTainted = state.sourceTainted) &&
        (!event.sourceTainted || event.derivedTainted ||
          (event.declassificationAuthorized && event.declassificationReceipt)) &&
        decide (event.deletionObligationOpen = state.deletionObligationOpen) &&
        (!event.deletionObligationOpen || event.deletionClosureReceipt) &&
        event.derivationReceipt && !event.materialized
  | .materialize =>
      decide (event.fromStage = .derived) && decide (event.toStage = .materialized) &&
        CellIdentityMatches state event &&
        decide (event.inputVersion = state.visibleVersion) &&
        state.snapshotReceipt && state.writeReceipt && state.commitReceipt &&
        state.readReceipt && state.derivationReceipt && state.replayReceipt &&
        state.auditReceipt &&
        (!state.sourceTainted || state.derivedTainted || state.declassificationAuthorized) &&
        (!state.deletionObligationOpen || state.deletionClosureReceipt) &&
        (!event.supportPromotionRequested || event.evidenceTransitionReceipt) &&
        event.materializationReceipt && event.materialized
  | .block => decide (event.toStage = .blocked) && event.blockReceipt && !event.materialized
  | .quarantine => decide (event.toStage = .quarantined) &&
      event.quarantineReceipt && event.derivedTainted && !event.materialized

def TransactionEventValid (state : TransactionState) (event : TransactionEvent) : Prop :=
  state.stage = event.fromStage ∧ state.logicalTime < event.logicalTime ∧
    TransactionEventSpecificValid state event = true

instance transactionEventValidDecidable (state : TransactionState) (event : TransactionEvent) :
    Decidable (TransactionEventValid state event) := by
  unfold TransactionEventValid
  infer_instance

def ApplyTransactionEvent (state : TransactionState) (event : TransactionEvent) : TransactionState :=
  { state with
    stage := event.toStage
    transactionId := if event.kind = .bindSnapshot then event.transactionId else state.transactionId
    snapshotId := if event.kind = .bindSnapshot then event.snapshotId else state.snapshotId
    snapshotEpoch := if event.kind = .bindSnapshot then event.snapshotEpoch else state.snapshotEpoch
    branchId := if event.kind = .bindSnapshot then event.branchId else state.branchId
    mountId := if event.kind = .bindSnapshot then event.mountId else state.mountId
    authorityEpoch := if event.kind = .bindSnapshot then event.authorityEpoch else state.authorityEpoch
    cellId := if event.kind = .stageWrite then event.cellId else state.cellId
    committedVersion := if event.kind = .commitWrite then event.outputVersion else state.committedVersion
    visibleVersion := if event.kind = .readSnapshot then event.inputVersion else state.visibleVersion
    sourceTainted := if event.kind = .stageWrite then event.sourceTainted else state.sourceTainted
    derivedTainted := state.derivedTainted || event.derivedTainted
    declassificationAuthorized := state.declassificationAuthorized || event.declassificationAuthorized
    deletionObligationOpen := if event.kind = .stageWrite then event.deletionObligationOpen else state.deletionObligationOpen
    deletionClosureReceipt := state.deletionClosureReceipt || event.deletionClosureReceipt
    snapshotReceipt := state.snapshotReceipt || event.snapshotReceipt
    writeReceipt := state.writeReceipt || event.writeReceipt
    commitReceipt := state.commitReceipt || event.commitReceipt
    readReceipt := state.readReceipt || event.readReceipt
    derivationReceipt := state.derivationReceipt || event.derivationReceipt
    replayReceipt := state.replayReceipt || event.replayReceipt
    auditReceipt := state.auditReceipt || event.auditReceipt
    materializationReceipt := state.materializationReceipt || event.materializationReceipt
    evidenceTransitionReceipt := state.evidenceTransitionReceipt || event.evidenceTransitionReceipt
    materialized := state.materialized || event.materialized
    logicalTime := event.logicalTime }

def TransactionStep (state : TransactionState) (event : TransactionEvent) : Option TransactionState :=
  if TransactionEventValid state event then some (ApplyTransactionEvent state event) else none

def TransactionRun : TransactionState → List TransactionEvent → Option TransactionState
  | state, [] => some state
  | state, event :: tail =>
      match TransactionStep state event with
      | none => none
      | some next => TransactionRun next tail

theorem accepted_step_is_valid
    {state next : TransactionState} {event : TransactionEvent}
    (accepted : TransactionStep state event = some next) : TransactionEventValid state event := by
  unfold TransactionStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_snapshot_read_preserves_snapshot_branch_mount_and_version
    {state next : TransactionState} {event : TransactionEvent}
    (kind : event.kind = .readSnapshot)
    (accepted : TransactionStep state event = some next) :
    event.transactionId = state.transactionId ∧ event.snapshotId = state.snapshotId ∧
      event.snapshotEpoch = state.snapshotEpoch ∧ event.branchId = state.branchId ∧
      event.mountId = state.mountId ∧ event.cellId = state.cellId ∧
      event.inputVersion = state.committedVersion ∧ event.readReceipt = true ∧
      event.replayReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, specific⟩
  simp [TransactionEventSpecificValid, kind, CellIdentityMatches,
    SnapshotIdentityMatches, and_assoc] at specific
  have fields :
      event.fromStage = .committed ∧ event.toStage = .readVisible ∧
        event.transactionId = state.transactionId ∧ event.snapshotId = state.snapshotId ∧
        event.snapshotEpoch = state.snapshotEpoch ∧ event.branchId = state.branchId ∧
        event.mountId = state.mountId ∧ event.authorityEpoch = state.authorityEpoch ∧
        event.cellId = state.cellId ∧ event.inputVersion = state.committedVersion ∧
        event.writeCommitted = true ∧ event.readVisible = true ∧
        event.readReceipt = true ∧ event.replayReceipt = true ∧
        event.branchMatches = true ∧ event.mountPermitted = true ∧
        event.materialized = false := by simpa [and_assoc] using specific
  rcases fields with ⟨_, _, tx, snapshot, epoch, branch, mount, _, cell, version,
    _, _, readReceipt, replayReceipt, _, _, _⟩
  exact ⟨tx, snapshot, epoch, branch, mount, cell, version, readReceipt, replayReceipt⟩

theorem accepted_untainted_derivation_from_tainted_source_requires_declassification
    {state next : TransactionState} {event : TransactionEvent}
    (kind : event.kind = .deriveContext)
    (accepted : TransactionStep state event = some next)
    (tainted : event.sourceTainted = true)
    (untainted : event.derivedTainted = false) :
    event.declassificationAuthorized = true ∧ event.declassificationReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, specific⟩
  simp [TransactionEventSpecificValid, kind, CellIdentityMatches,
    SnapshotIdentityMatches, tainted, untainted, and_assoc] at specific
  have fields :
      event.fromStage = .readVisible ∧ event.toStage = .derived ∧
        event.transactionId = state.transactionId ∧ event.snapshotId = state.snapshotId ∧
        event.snapshotEpoch = state.snapshotEpoch ∧ event.branchId = state.branchId ∧
        event.mountId = state.mountId ∧ event.authorityEpoch = state.authorityEpoch ∧
        event.cellId = state.cellId ∧ event.inputVersion = state.visibleVersion ∧
        state.sourceTainted = true ∧
        event.declassificationAuthorized = true ∧
        event.declassificationReceipt = true ∧
        event.deletionObligationOpen = state.deletionObligationOpen ∧
        (!event.deletionObligationOpen || event.deletionClosureReceipt) = true ∧
        event.derivationReceipt = true ∧ event.materialized = false := by
    simpa [and_assoc] using specific
  rcases fields with ⟨_, _, _, _, _, _, _, _, _, _, _, authorized, receipt, _, _, _, _⟩
  exact ⟨authorized, receipt⟩

theorem accepted_materialization_preserves_transaction_custody
    {state next : TransactionState} {event : TransactionEvent}
    (kind : event.kind = .materialize)
    (accepted : TransactionStep state event = some next) :
    event.transactionId = state.transactionId ∧ event.snapshotId = state.snapshotId ∧
      event.branchId = state.branchId ∧ event.mountId = state.mountId ∧
      event.cellId = state.cellId ∧ event.inputVersion = state.visibleVersion ∧
      state.snapshotReceipt = true ∧ state.writeReceipt = true ∧
      state.commitReceipt = true ∧ state.readReceipt = true ∧
      state.derivationReceipt = true ∧ state.replayReceipt = true ∧
      state.auditReceipt = true ∧ event.materializationReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, specific⟩
  simp [TransactionEventSpecificValid, kind, CellIdentityMatches,
    SnapshotIdentityMatches, and_assoc] at specific
  have fields :
      event.fromStage = .derived ∧ event.toStage = .materialized ∧
        event.transactionId = state.transactionId ∧ event.snapshotId = state.snapshotId ∧
        event.snapshotEpoch = state.snapshotEpoch ∧ event.branchId = state.branchId ∧
        event.mountId = state.mountId ∧ event.authorityEpoch = state.authorityEpoch ∧
        event.cellId = state.cellId ∧ event.inputVersion = state.visibleVersion ∧
        state.snapshotReceipt = true ∧ state.writeReceipt = true ∧
        state.commitReceipt = true ∧ state.readReceipt = true ∧
        state.derivationReceipt = true ∧ state.replayReceipt = true ∧
        state.auditReceipt = true ∧
        (!state.sourceTainted || state.derivedTainted || state.declassificationAuthorized) = true ∧
        (!state.deletionObligationOpen || state.deletionClosureReceipt) = true ∧
        (!event.supportPromotionRequested || event.evidenceTransitionReceipt) = true ∧
        event.materializationReceipt = true ∧ event.materialized = true := by
    simpa [and_assoc] using specific
  rcases fields with ⟨_, _, tx, snapshot, _, branch, mount, _, cell, version,
    snapshotReceipt, writeReceipt, commitReceipt, readReceipt, deriveReceipt,
    replayReceipt, auditReceipt, _, _, _, materialReceipt, _⟩
  exact ⟨tx, snapshot, branch, mount, cell, version, snapshotReceipt, writeReceipt,
    commitReceipt, readReceipt, deriveReceipt, replayReceipt, auditReceipt, materialReceipt⟩

def initialState : TransactionState where
  stage := .raw
  transactionId := 0
  snapshotId := 0
  snapshotEpoch := 0
  branchId := 0
  mountId := 0
  cellId := 0
  authorityEpoch := 0
  committedVersion := 0
  visibleVersion := 0
  sourceTainted := false
  derivedTainted := false
  declassificationAuthorized := false
  deletionObligationOpen := false
  deletionClosureReceipt := false
  snapshotReceipt := false
  writeReceipt := false
  commitReceipt := false
  readReceipt := false
  derivationReceipt := false
  replayReceipt := false
  auditReceipt := false
  materializationReceipt := false
  evidenceTransitionReceipt := false
  materialized := false
  logicalTime := 0

def baseEvent (kind : TransactionEventKind) (fromStage toStage : TransactionStage)
    (time : Nat) : TransactionEvent where
  kind := kind
  fromStage := fromStage
  toStage := toStage
  transactionId := 101
  snapshotId := 201
  snapshotEpoch := 1
  branchId := 301
  mountId := 401
  cellId := 501
  authorityEpoch := 1
  inputVersion := 0
  outputVersion := 0
  snapshotPresent := true
  snapshotCurrent := true
  branchMatches := true
  mountPermitted := true
  writeCommitted := false
  readVisible := false
  sourceTainted := false
  derivedTainted := false
  declassificationAuthorized := false
  declassificationReceipt := false
  deletionObligationOpen := false
  deletionClosureReceipt := false
  snapshotReceipt := false
  writeReceipt := false
  commitReceipt := false
  readReceipt := false
  derivationReceipt := false
  replayReceipt := false
  auditReceipt := false
  materializationReceipt := false
  supportPromotionRequested := false
  evidenceTransitionReceipt := false
  materialized := false
  blockReceipt := false
  quarantineReceipt := false
  logicalTime := time

def bindEvent := { baseEvent .bindSnapshot .raw .snapshotBound 1 with
  snapshotReceipt := true, replayReceipt := true, auditReceipt := true }
def stageEvent := { baseEvent .stageWrite .snapshotBound .writeStaged 2 with writeReceipt := true }
def commitEvent := { baseEvent .commitWrite .writeStaged .committed 3 with
  outputVersion := 1, writeCommitted := true, commitReceipt := true, auditReceipt := true }
def readEvent := { baseEvent .readSnapshot .committed .readVisible 4 with
  inputVersion := 1, writeCommitted := true, readVisible := true,
  readReceipt := true, replayReceipt := true }
def deriveEvent := { baseEvent .deriveContext .readVisible .derived 5 with
  inputVersion := 1, derivationReceipt := true }
def materializeEvent := { baseEvent .materialize .derived .materialized 6 with
  inputVersion := 1, materializationReceipt := true, materialized := true }
def successTrace := [bindEvent, stageEvent, commitEvent, readEvent, deriveEvent, materializeEvent]

theorem exact_transaction_trace_materializes :
    (TransactionRun initialState successTrace).map (fun state =>
      (state.stage, state.committedVersion, state.visibleVersion, state.materialized)) =
      some (.materialized, 1, 1, true) := by native_decide

def spliceRun (before : List TransactionEvent) (event : TransactionEvent)
    (after : List TransactionEvent) := TransactionRun initialState (before ++ event :: after)

theorem missing_snapshot_rejected :
    spliceRun [] { bindEvent with snapshotPresent := false } [stageEvent, commitEvent, readEvent, deriveEvent, materializeEvent] = none := by native_decide
theorem stale_snapshot_rejected :
    spliceRun [] { bindEvent with snapshotCurrent := false } [stageEvent, commitEvent, readEvent, deriveEvent, materializeEvent] = none := by native_decide
theorem branch_substitution_rejected :
    spliceRun [bindEvent] { stageEvent with branchId := 999 } [commitEvent, readEvent, deriveEvent, materializeEvent] = none := by native_decide
theorem mount_substitution_rejected :
    spliceRun [bindEvent] { stageEvent with mountId := 999 } [commitEvent, readEvent, deriveEvent, materializeEvent] = none := by native_decide
theorem unauthorized_mount_rejected :
    spliceRun [bindEvent] { stageEvent with mountPermitted := false } [commitEvent, readEvent, deriveEvent, materializeEvent] = none := by native_decide
theorem uncommitted_write_rejected :
    spliceRun [bindEvent, stageEvent] { commitEvent with writeCommitted := false } [readEvent, deriveEvent, materializeEvent] = none := by native_decide
theorem commit_version_skip_rejected :
    spliceRun [bindEvent, stageEvent] { commitEvent with outputVersion := 2 } [readEvent, deriveEvent, materializeEvent] = none := by native_decide
theorem invisible_read_rejected :
    spliceRun [bindEvent, stageEvent, commitEvent] { readEvent with readVisible := false } [deriveEvent, materializeEvent] = none := by native_decide
theorem stale_read_version_rejected :
    spliceRun [bindEvent, stageEvent, commitEvent] { readEvent with inputVersion := 0 } [deriveEvent, materializeEvent] = none := by native_decide
theorem missing_replay_receipt_rejected :
    spliceRun [bindEvent, stageEvent, commitEvent] { readEvent with replayReceipt := false } [deriveEvent, materializeEvent] = none := by native_decide
theorem taint_laundering_rejected :
    spliceRun [bindEvent] { stageEvent with sourceTainted := true }
      [commitEvent, readEvent, { deriveEvent with sourceTainted := true }, materializeEvent] = none := by native_decide
def falseDeclassificationEvent : TransactionEvent :=
  { { deriveEvent with sourceTainted := true } with
    declassificationAuthorized := true, declassificationReceipt := false }
theorem false_declassification_rejected :
    spliceRun [bindEvent] { stageEvent with sourceTainted := true }
      [commitEvent, readEvent, falseDeclassificationEvent, materializeEvent] = none := by native_decide
theorem open_deletion_rejected :
    spliceRun [bindEvent] { stageEvent with deletionObligationOpen := true }
      [commitEvent, readEvent, { deriveEvent with deletionObligationOpen := true }, materializeEvent] = none := by native_decide
theorem missing_materialization_receipt_rejected :
    spliceRun [bindEvent, stageEvent, commitEvent, readEvent, deriveEvent]
      { materializeEvent with materializationReceipt := false } [] = none := by native_decide
theorem support_promotion_without_transition_rejected :
    spliceRun [bindEvent, stageEvent, commitEvent, readEvent, deriveEvent]
      { materializeEvent with supportPromotionRequested := true } [] = none := by native_decide

end AsiStackProofs.ContextTransactionRefinement

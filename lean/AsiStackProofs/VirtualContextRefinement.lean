namespace AsiStackProofs.VirtualContextRefinement

/-!
Finite reachable resolver/certificate/materialization semantics. All numeric
identities, authority levels, lease times, certificate flags, and receipts are
trusted abstract inputs. The model does not establish address truth, payload
semantics, certificate truthfulness, or deployed memory-store behavior.
-/

inductive ContextStage where
  | raw | requestBound | resolved | certified | materialized | typedFault | denied
deriving DecidableEq, Repr

inductive ContextEventKind where
  | bindRequest | resolveHit | resolveMiss | certify | materialize | deny
deriving DecidableEq, Repr

structure ContextState where
  stage : ContextStage
  requestId : Nat
  address : Nat
  version : Nat
  snapshot : Nat
  mount : Nat
  authorityCeiling : Nat
  approvedAuthority : Nat
  leaseExpiry : Nat
  sourceHash : Nat
  derivedHash : Nat
  mandatory : Bool
  resolverReceipt : Bool
  certificateReceipt : Bool
  materializationReceipt : Bool
  typedFaultReceipt : Bool
  materializationEmitted : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

structure ContextEvent where
  kind : ContextEventKind
  fromStage : ContextStage
  toStage : ContextStage
  requestId : Nat
  address : Nat
  version : Nat
  snapshot : Nat
  mount : Nat
  requestedAuthority : Nat
  leaseExpiry : Nat
  sourceHash : Nat
  derivedHash : Nat
  certificateSourceHash : Nat
  mandatory : Bool
  resolverFound : Bool
  mountPermitted : Bool
  resolverReceipt : Bool
  certificateReceipt : Bool
  omissionDeclared : Bool
  exactCompletenessClaimed : Bool
  taintDetected : Bool
  materializationReceipt : Bool
  typedFaultReceipt : Bool
  materializationEmitted : Bool
  denialReceipt : Bool
  logicalTime : Nat
deriving DecidableEq, Repr

def RequestMatches (state : ContextState) (event : ContextEvent) : Bool :=
  decide (event.requestId = state.requestId) &&
    decide (event.address = state.address) &&
    decide (event.version = state.version) &&
    decide (event.snapshot = state.snapshot) &&
    decide (event.mount = state.mount) &&
    decide (event.mandatory = state.mandatory)

def ContextEventSpecificValid (state : ContextState) (event : ContextEvent) : Bool :=
  match event.kind with
  | .bindRequest =>
      decide (event.fromStage = .raw) && decide (event.toStage = .requestBound) &&
        decide (0 < event.requestId) && decide (0 < event.address) &&
        decide (0 < event.version) && decide (0 < event.snapshot) &&
        decide (0 < event.mount) &&
        decide (event.requestedAuthority ≤ state.authorityCeiling) &&
        decide (event.logicalTime < event.leaseExpiry)
  | .resolveHit =>
      decide (event.fromStage = .requestBound) && decide (event.toStage = .resolved) &&
        RequestMatches state event && event.resolverFound && event.mountPermitted &&
        decide (event.logicalTime < state.leaseExpiry) &&
        decide (0 < event.sourceHash) && event.resolverReceipt &&
        !event.typedFaultReceipt && !event.materializationEmitted
  | .resolveMiss =>
      decide (event.fromStage = .requestBound) && decide (event.toStage = .typedFault) &&
        decide (event.requestId = state.requestId) && event.mandatory &&
        !event.resolverFound && event.typedFaultReceipt &&
        !event.materializationEmitted && !event.materializationReceipt
  | .certify =>
      decide (event.fromStage = .resolved) && decide (event.toStage = .certified) &&
        RequestMatches state event && decide (event.sourceHash = state.sourceHash) &&
        decide (event.certificateSourceHash = state.sourceHash) &&
        decide (0 < event.derivedHash) &&
        decide (event.requestedAuthority ≤ state.approvedAuthority) &&
        event.certificateReceipt && event.omissionDeclared &&
        !event.exactCompletenessClaimed && !event.taintDetected &&
        !event.materializationEmitted
  | .materialize =>
      decide (event.fromStage = .certified) && decide (event.toStage = .materialized) &&
        RequestMatches state event && decide (event.sourceHash = state.sourceHash) &&
        decide (event.derivedHash = state.derivedHash) &&
        decide (event.requestedAuthority ≤ state.approvedAuthority) &&
        state.resolverReceipt && state.certificateReceipt &&
        !event.taintDetected && event.materializationReceipt &&
        event.materializationEmitted && !event.typedFaultReceipt
  | .deny => decide (event.toStage = .denied) && event.denialReceipt &&
      !event.materializationEmitted

def ContextEventValid (state : ContextState) (event : ContextEvent) : Prop :=
  state.stage = event.fromStage ∧ state.logicalTime < event.logicalTime ∧
    ContextEventSpecificValid state event = true

instance contextEventValidDecidable (state : ContextState) (event : ContextEvent) :
    Decidable (ContextEventValid state event) := by
  unfold ContextEventValid
  infer_instance

def ApplyContextEvent (state : ContextState) (event : ContextEvent) : ContextState :=
  { state with
    stage := event.toStage
    requestId := if event.kind = .bindRequest then event.requestId else state.requestId
    address := if event.kind = .bindRequest then event.address else state.address
    version := if event.kind = .bindRequest then event.version else state.version
    snapshot := if event.kind = .bindRequest then event.snapshot else state.snapshot
    mount := if event.kind = .bindRequest then event.mount else state.mount
    approvedAuthority := if event.kind = .bindRequest then event.requestedAuthority else state.approvedAuthority
    leaseExpiry := if event.kind = .bindRequest then event.leaseExpiry else state.leaseExpiry
    sourceHash := if event.kind = .resolveHit then event.sourceHash else state.sourceHash
    derivedHash := if event.kind = .certify then event.derivedHash else state.derivedHash
    mandatory := if event.kind = .bindRequest then event.mandatory else state.mandatory
    resolverReceipt := state.resolverReceipt || event.resolverReceipt
    certificateReceipt := state.certificateReceipt || event.certificateReceipt
    materializationReceipt := state.materializationReceipt || event.materializationReceipt
    typedFaultReceipt := state.typedFaultReceipt || event.typedFaultReceipt
    materializationEmitted := state.materializationEmitted || event.materializationEmitted
    logicalTime := event.logicalTime }

def ContextStep (state : ContextState) (event : ContextEvent) : Option ContextState :=
  if ContextEventValid state event then some (ApplyContextEvent state event) else none

def ContextRun : ContextState → List ContextEvent → Option ContextState
  | state, [] => some state
  | state, event :: tail =>
      match ContextStep state event with
      | none => none
      | some next => ContextRun next tail

theorem accepted_step_is_valid
    {state next : ContextState} {event : ContextEvent}
    (accepted : ContextStep state event = some next) : ContextEventValid state event := by
  unfold ContextStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_materialization_preserves_binding_and_authority
    {state next : ContextState} {event : ContextEvent}
    (kind : event.kind = .materialize)
    (accepted : ContextStep state event = some next) :
    event.requestId = state.requestId ∧ event.address = state.address ∧
      event.version = state.version ∧ event.snapshot = state.snapshot ∧
      event.mount = state.mount ∧ event.sourceHash = state.sourceHash ∧
      event.derivedHash = state.derivedHash ∧
      event.requestedAuthority ≤ state.approvedAuthority ∧
      event.materializationReceipt = true := by
  rcases accepted_step_is_valid accepted with ⟨_, _, specific⟩
  simp [ContextEventSpecificValid, kind, RequestMatches, and_assoc] at specific
  have fields :
      event.fromStage = .certified ∧ event.toStage = .materialized ∧
        event.requestId = state.requestId ∧ event.address = state.address ∧
        event.version = state.version ∧ event.snapshot = state.snapshot ∧
        event.mount = state.mount ∧ event.mandatory = state.mandatory ∧
        event.sourceHash = state.sourceHash ∧ event.derivedHash = state.derivedHash ∧
        event.requestedAuthority ≤ state.approvedAuthority ∧
        state.resolverReceipt = true ∧ state.certificateReceipt = true ∧
        event.taintDetected = false ∧ event.materializationReceipt = true ∧
        event.materializationEmitted = true ∧ event.typedFaultReceipt = false := by
    simpa [and_assoc] using specific
  rcases fields with ⟨_, _, request, address, version, snapshot, mount, _, source,
    derived, authority, _, _, _, receipt, _, _⟩
  exact ⟨request, address, version, snapshot, mount, source, derived, authority, receipt⟩

theorem accepted_mandatory_miss_emits_fault_without_materialization
    {state next : ContextState} {event : ContextEvent}
    (kind : event.kind = .resolveMiss)
    (accepted : ContextStep state event = some next) :
    event.mandatory = true ∧ event.typedFaultReceipt = true ∧
      event.materializationEmitted = false ∧ event.materializationReceipt = false := by
  rcases accepted_step_is_valid accepted with ⟨_, _, specific⟩
  simp [ContextEventSpecificValid, kind, and_assoc] at specific
  exact ⟨specific.2.2.2.1, specific.2.2.2.2.2.1,
    specific.2.2.2.2.2.2.1, specific.2.2.2.2.2.2.2⟩

def initialState : ContextState where
  stage := .raw
  requestId := 0
  address := 0
  version := 0
  snapshot := 0
  mount := 0
  authorityCeiling := 3
  approvedAuthority := 0
  leaseExpiry := 0
  sourceHash := 0
  derivedHash := 0
  mandatory := false
  resolverReceipt := false
  certificateReceipt := false
  materializationReceipt := false
  typedFaultReceipt := false
  materializationEmitted := false
  logicalTime := 0

def baseEvent (kind : ContextEventKind) (fromStage toStage : ContextStage)
    (time : Nat) : ContextEvent where
  kind := kind
  fromStage := fromStage
  toStage := toStage
  requestId := 101
  address := 201
  version := 301
  snapshot := 401
  mount := 501
  requestedAuthority := 2
  leaseExpiry := 20
  sourceHash := 601
  derivedHash := 701
  certificateSourceHash := 601
  mandatory := true
  resolverFound := false
  mountPermitted := true
  resolverReceipt := false
  certificateReceipt := false
  omissionDeclared := true
  exactCompletenessClaimed := false
  taintDetected := false
  materializationReceipt := false
  typedFaultReceipt := false
  materializationEmitted := false
  denialReceipt := false
  logicalTime := time

def bindEvent : ContextEvent := baseEvent .bindRequest .raw .requestBound 1
def hitEvent : ContextEvent :=
  { baseEvent .resolveHit .requestBound .resolved 2 with
    resolverFound := true, resolverReceipt := true }
def certifyEvent : ContextEvent :=
  { baseEvent .certify .resolved .certified 3 with certificateReceipt := true }
def materializeEvent : ContextEvent :=
  { baseEvent .materialize .certified .materialized 4 with
    materializationReceipt := true, materializationEmitted := true }
def missEvent : ContextEvent :=
  { baseEvent .resolveMiss .requestBound .typedFault 2 with typedFaultReceipt := true }

def successTrace := [bindEvent, hitEvent, certifyEvent, materializeEvent]
def missTrace := [bindEvent, missEvent]

theorem exact_resolver_trace_materializes :
    (ContextRun initialState successTrace).map (fun state =>
      (state.stage, state.materializationEmitted)) =
      some (.materialized, true) := by
  native_decide

theorem mandatory_miss_trace_faults_without_packet :
    (ContextRun initialState missTrace).map (fun state =>
      (state.stage, state.typedFaultReceipt, state.materializationEmitted)) =
      some (.typedFault, true, false) := by
  native_decide

def spliceRun (before : List ContextEvent) (event : ContextEvent)
    (after : List ContextEvent) := ContextRun initialState (before ++ event :: after)

theorem address_substitution_rejected :
    spliceRun [bindEvent] { hitEvent with address := 999 } [certifyEvent, materializeEvent] = none := by native_decide
theorem version_substitution_rejected :
    spliceRun [bindEvent] { hitEvent with version := 999 } [certifyEvent, materializeEvent] = none := by native_decide
theorem snapshot_substitution_rejected :
    spliceRun [bindEvent] { hitEvent with snapshot := 999 } [certifyEvent, materializeEvent] = none := by native_decide
theorem mount_substitution_rejected :
    spliceRun [bindEvent] { hitEvent with mount := 999 } [certifyEvent, materializeEvent] = none := by native_decide
theorem expired_lease_rejected :
    ContextRun initialState [{ bindEvent with leaseExpiry := 1 }] = none := by native_decide
theorem certificate_binding_substitution_rejected :
    spliceRun [bindEvent, hitEvent] { certifyEvent with certificateSourceHash := 999 } [materializeEvent] = none := by native_decide
theorem certificate_authority_escalation_rejected :
    spliceRun [bindEvent, hitEvent] { certifyEvent with requestedAuthority := 3 } [materializeEvent] = none := by native_decide
theorem exact_completeness_overclaim_rejected :
    spliceRun [bindEvent, hitEvent] { certifyEvent with exactCompletenessClaimed := true } [materializeEvent] = none := by native_decide
theorem undeclared_omission_rejected :
    spliceRun [bindEvent, hitEvent] { certifyEvent with omissionDeclared := false } [materializeEvent] = none := by native_decide
theorem mandatory_miss_without_fault_receipt_rejected :
    spliceRun [bindEvent] { missEvent with typedFaultReceipt := false } [] = none := by native_decide
theorem materialization_without_certificate_receipt_rejected :
    spliceRun [bindEvent, hitEvent] { certifyEvent with certificateReceipt := false } [materializeEvent] = none := by native_decide
theorem tainted_materialization_rejected :
    spliceRun [bindEvent, hitEvent] { certifyEvent with taintDetected := true } [materializeEvent] = none := by native_decide

end AsiStackProofs.VirtualContextRefinement

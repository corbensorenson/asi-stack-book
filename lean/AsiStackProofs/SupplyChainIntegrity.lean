namespace AsiStackProofs.SupplyChainIntegrity

inductive SupplyChainAdmissionRoute where
  | retainAsSupplyChainDraft
  | requireLineageRepair
  | requireAccountableReview
  | quarantineArtifact
  | releaseToCustodyReview
deriving DecidableEq, Repr

structure SupplyChainRecord where
  artifactIdentityRecorded : Bool
  artifactDigestRecorded : Bool
  lineageRecorded : Bool
  supplierScopeRecorded : Bool
  buildOrTrainingProvenanceRecorded : Bool
  signatureRequired : Bool
  signatureVerified : Bool
  componentInventoryRecorded : Bool
  advisoryStateRecorded : Bool
  unresolvedCriticalAdvisory : Bool
  revocationPathRecorded : Bool
  residualOwnerRecorded : Bool
  artifactAdmissionRequested : Bool
deriving DecidableEq, Repr

def SupplyChainAdmissionRouteFor (record : SupplyChainRecord) : SupplyChainAdmissionRoute :=
  if record.artifactIdentityRecorded = false then
    SupplyChainAdmissionRoute.retainAsSupplyChainDraft
  else if record.artifactDigestRecorded = false then
    SupplyChainAdmissionRoute.requireLineageRepair
  else if record.lineageRecorded = false then
    SupplyChainAdmissionRoute.requireLineageRepair
  else if record.supplierScopeRecorded = false then
    SupplyChainAdmissionRoute.requireAccountableReview
  else if record.buildOrTrainingProvenanceRecorded = false then
    SupplyChainAdmissionRoute.requireLineageRepair
  else if record.signatureRequired = true && record.signatureVerified = false then
    SupplyChainAdmissionRoute.quarantineArtifact
  else if record.componentInventoryRecorded = false then
    SupplyChainAdmissionRoute.requireAccountableReview
  else if record.advisoryStateRecorded = false then
    SupplyChainAdmissionRoute.requireAccountableReview
  else if record.unresolvedCriticalAdvisory = true then
    SupplyChainAdmissionRoute.quarantineArtifact
  else if record.revocationPathRecorded = false then
    SupplyChainAdmissionRoute.requireLineageRepair
  else if record.residualOwnerRecorded = false then
    SupplyChainAdmissionRoute.requireAccountableReview
  else if record.artifactAdmissionRequested = true then
    SupplyChainAdmissionRoute.releaseToCustodyReview
  else
    SupplyChainAdmissionRoute.retainAsSupplyChainDraft

theorem unresolved_critical_advisory_quarantines_requested_artifact
    {record : SupplyChainRecord} :
    record.artifactIdentityRecorded = true ->
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.supplierScopeRecorded = true ->
    record.buildOrTrainingProvenanceRecorded = true ->
    record.signatureRequired = false ->
    record.componentInventoryRecorded = true ->
    record.advisoryStateRecorded = true ->
    record.unresolvedCriticalAdvisory = true ->
    record.artifactAdmissionRequested = true ->
    SupplyChainAdmissionRouteFor record = SupplyChainAdmissionRoute.quarantineArtifact := by
  intro artifactIdentity artifactDigest lineage supplierScope buildOrTraining
    signatureNotRequired componentInventory advisoryState unresolvedAdvisory admissionRequested
  unfold SupplyChainAdmissionRouteFor
  simp [artifactIdentity, artifactDigest, lineage, supplierScope, buildOrTraining,
    signatureNotRequired, componentInventory, advisoryState, unresolvedAdvisory]

theorem required_unverified_signature_quarantines_artifact
    {record : SupplyChainRecord} :
    record.artifactIdentityRecorded = true ->
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.supplierScopeRecorded = true ->
    record.buildOrTrainingProvenanceRecorded = true ->
    record.signatureRequired = true ->
    record.signatureVerified = false ->
    SupplyChainAdmissionRouteFor record = SupplyChainAdmissionRoute.quarantineArtifact := by
  intro artifactIdentity artifactDigest lineage supplierScope buildOrTraining
    signatureRequired signatureUnverified
  unfold SupplyChainAdmissionRouteFor
  simp [artifactIdentity, artifactDigest, lineage, supplierScope, buildOrTraining,
    signatureRequired, signatureUnverified]

theorem complete_requested_artifact_reaches_custody_review
    {record : SupplyChainRecord} :
    record.artifactIdentityRecorded = true ->
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.supplierScopeRecorded = true ->
    record.buildOrTrainingProvenanceRecorded = true ->
    record.signatureRequired = true ->
    record.signatureVerified = true ->
    record.componentInventoryRecorded = true ->
    record.advisoryStateRecorded = true ->
    record.unresolvedCriticalAdvisory = false ->
    record.revocationPathRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.artifactAdmissionRequested = true ->
    SupplyChainAdmissionRouteFor record =
      SupplyChainAdmissionRoute.releaseToCustodyReview := by
  intro identity digest lineage supplier provenance signatureRequired
    signatureVerified inventory advisory noCritical revocation residual requested
  unfold SupplyChainAdmissionRouteFor
  simp [identity, digest, lineage, supplier, provenance, signatureRequired,
    signatureVerified, inventory, advisory, noCritical, revocation, residual,
    requested]

theorem missing_lineage_requires_repair
    {record : SupplyChainRecord} :
    record.artifactIdentityRecorded = true ->
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = false ->
    SupplyChainAdmissionRouteFor record =
      SupplyChainAdmissionRoute.requireLineageRepair := by
  intro identity digest missingLineage
  unfold SupplyChainAdmissionRouteFor
  simp [identity, digest, missingLineage]

theorem missing_component_inventory_requires_review
    {record : SupplyChainRecord} :
    record.artifactIdentityRecorded = true ->
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.supplierScopeRecorded = true ->
    record.buildOrTrainingProvenanceRecorded = true ->
    record.signatureRequired = false ->
    record.componentInventoryRecorded = false ->
    SupplyChainAdmissionRouteFor record =
      SupplyChainAdmissionRoute.requireAccountableReview := by
  intro identity digest lineage supplier provenance noSignature missingInventory
  unfold SupplyChainAdmissionRouteFor
  simp [identity, digest, lineage, supplier, provenance, noSignature,
    missingInventory]

theorem missing_revocation_path_requires_repair
    {record : SupplyChainRecord} :
    record.artifactIdentityRecorded = true ->
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.supplierScopeRecorded = true ->
    record.buildOrTrainingProvenanceRecorded = true ->
    record.signatureRequired = false ->
    record.componentInventoryRecorded = true ->
    record.advisoryStateRecorded = true ->
    record.unresolvedCriticalAdvisory = false ->
    record.revocationPathRecorded = false ->
    SupplyChainAdmissionRouteFor record =
      SupplyChainAdmissionRoute.requireLineageRepair := by
  intro identity digest lineage supplier provenance noSignature inventory
    advisory noCritical missingRevocation
  unfold SupplyChainAdmissionRouteFor
  simp [identity, digest, lineage, supplier, provenance, noSignature, inventory,
    advisory, noCritical, missingRevocation]

theorem missing_residual_owner_requires_review
    {record : SupplyChainRecord} :
    record.artifactIdentityRecorded = true ->
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.supplierScopeRecorded = true ->
    record.buildOrTrainingProvenanceRecorded = true ->
    record.signatureRequired = false ->
    record.componentInventoryRecorded = true ->
    record.advisoryStateRecorded = true ->
    record.unresolvedCriticalAdvisory = false ->
    record.revocationPathRecorded = true ->
    record.residualOwnerRecorded = false ->
    SupplyChainAdmissionRouteFor record =
      SupplyChainAdmissionRoute.requireAccountableReview := by
  intro identity digest lineage supplier provenance noSignature inventory
    advisory noCritical revocation missingResidual
  unfold SupplyChainAdmissionRouteFor
  simp [identity, digest, lineage, supplier, provenance, noSignature, inventory,
    advisory, noCritical, revocation, missingResidual]

/-! ## Reachable supply-chain lifecycle

The route function above classifies one authored record. This transition model
adds the bounded proposition that one artifact keeps its declared identity,
provenance identity, and authority ceiling while it is bound, reviewed,
admitted or quarantined, and eventually revoked. The model treats the event
fields as inputs; it does not establish that a signature, advisory feed,
inventory, supplier, or revocation mechanism is truthful in deployment.
-/

inductive SupplyChainStage where
  | received
  | provenanceBound
  | reviewedClean
  | quarantined
  | admitted
  | revoked
deriving DecidableEq, Repr

inductive SupplyChainEventKind where
  | bindProvenance
  | reviewClean
  | reviewCritical
  | admit
  | revoke
deriving DecidableEq, Repr

structure SupplyChainState where
  stage : SupplyChainStage
  artifactId : Nat
  artifactDigest : Nat
  lineageId : Nat
  supplierId : Nat
  buildOrTrainingId : Nat
  authorityCeiling : Nat
  activeAuthority : Nat
  admissionReceiptCount : Nat
  invalidationReceiptCount : Nat
  supportAssignmentCount : Nat
  externalEffectAuthorityCount : Nat
deriving DecidableEq, Repr

structure SupplyChainEvent where
  kind : SupplyChainEventKind
  artifactId : Nat
  artifactDigest : Nat
  lineageId : Nat
  supplierId : Nat
  buildOrTrainingId : Nat
  requestedAuthority : Nat
  signatureVerified : Bool
  componentInventoryComplete : Bool
  advisoryReviewIndependent : Bool
  criticalAdvisoryPresent : Bool
  revocationPathPresent : Bool
  residualOwnerPresent : Bool
  nonClaimBoundaryPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectAuthorityRequested : Bool
deriving DecidableEq, Repr

structure SupplyChainIdentity where
  artifactId : Nat
  artifactDigest : Nat
  lineageId : Nat
  supplierId : Nat
  buildOrTrainingId : Nat
  authorityCeiling : Nat
deriving DecidableEq, Repr

def supplyChainIdentity (state : SupplyChainState) : SupplyChainIdentity := {
  artifactId := state.artifactId
  artifactDigest := state.artifactDigest
  lineageId := state.lineageId
  supplierId := state.supplierId
  buildOrTrainingId := state.buildOrTrainingId
  authorityCeiling := state.authorityCeiling
}

def SupplyChainEventValid
    (state : SupplyChainState) (event : SupplyChainEvent) : Prop :=
  event.artifactId = state.artifactId ∧
    event.artifactDigest = state.artifactDigest ∧
    event.lineageId = state.lineageId ∧
    event.supplierId = state.supplierId ∧
    event.buildOrTrainingId = state.buildOrTrainingId ∧
    event.requestedAuthority ≤ state.authorityCeiling ∧
    event.supportAssignmentRequested = false ∧
    event.externalEffectAuthorityRequested = false ∧
    event.revocationPathPresent = true ∧
    event.residualOwnerPresent = true ∧
    event.nonClaimBoundaryPresent = true ∧
    match state.stage, event.kind with
    | .received, .bindProvenance =>
        event.signatureVerified = true ∧
          event.componentInventoryComplete = true
    | .provenanceBound, .reviewClean =>
        event.advisoryReviewIndependent = true ∧
          event.criticalAdvisoryPresent = false
    | .provenanceBound, .reviewCritical =>
        event.advisoryReviewIndependent = true ∧
          event.criticalAdvisoryPresent = true
    | .reviewedClean, .admit => True
    | .admitted, .revoke => True
    | _, _ => False

instance supplyChainEventValidDecidable
    (state : SupplyChainState) (event : SupplyChainEvent) :
    Decidable (SupplyChainEventValid state event) := by
  cases hstage : state.stage <;> cases hkind : event.kind <;>
    simp [SupplyChainEventValid, hstage, hkind] <;> infer_instance

def applySupplyChainEvent
    (state : SupplyChainState) (event : SupplyChainEvent) : SupplyChainState :=
  match event.kind with
  | .bindProvenance => { state with stage := .provenanceBound }
  | .reviewClean => { state with stage := .reviewedClean }
  | .reviewCritical => { state with stage := .quarantined }
  | .admit =>
      { state with stage := .admitted
                   activeAuthority := event.requestedAuthority
                   admissionReceiptCount := state.admissionReceiptCount + 1 }
  | .revoke =>
      { state with stage := .revoked
                   activeAuthority := 0
                   invalidationReceiptCount := state.invalidationReceiptCount + 1 }

def SupplyChainStep
    (state : SupplyChainState) (event : SupplyChainEvent) : Option SupplyChainState :=
  if SupplyChainEventValid state event then
    some (applySupplyChainEvent state event)
  else none

def SupplyChainRun : SupplyChainState → List SupplyChainEvent → Option SupplyChainState
  | state, [] => some state
  | state, event :: tail =>
      match SupplyChainStep state event with
      | none => none
      | some next => SupplyChainRun next tail

def SupplyChainTraceValid : SupplyChainState → List SupplyChainEvent → Prop
  | _, [] => True
  | state, event :: tail =>
      SupplyChainEventValid state event ∧
        SupplyChainTraceValid (applySupplyChainEvent state event) tail

theorem accepted_supply_chain_step_is_valid
    {state next : SupplyChainState} {event : SupplyChainEvent}
    (stepped : SupplyChainStep state event = some next) :
    SupplyChainEventValid state event := by
  unfold SupplyChainStep at stepped
  split at stepped
  · assumption
  · simp at stepped

theorem accepted_supply_chain_step_applies_event
    {state next : SupplyChainState} {event : SupplyChainEvent}
    (stepped : SupplyChainStep state event = some next) :
    next = applySupplyChainEvent state event := by
  unfold SupplyChainStep at stepped
  split at stepped
  · exact Option.some.inj stepped |>.symm
  · simp at stepped

theorem apply_supply_chain_event_preserves_identity
    (state : SupplyChainState) (event : SupplyChainEvent) :
    supplyChainIdentity (applySupplyChainEvent state event) =
      supplyChainIdentity state := by
  cases h : event.kind <;>
    simp [applySupplyChainEvent, supplyChainIdentity, h]

theorem accepted_supply_chain_step_preserves_non_authority
    {state next : SupplyChainState} {event : SupplyChainEvent}
    (stepped : SupplyChainStep state event = some next) :
    next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectAuthorityCount = state.externalEffectAuthorityCount := by
  have applies := accepted_supply_chain_step_applies_event stepped
  subst next
  cases h : event.kind <;> simp [applySupplyChainEvent, h]

theorem accepted_supply_chain_step_respects_authority_ceiling
    {state next : SupplyChainState} {event : SupplyChainEvent}
    (bounded : state.activeAuthority ≤ state.authorityCeiling)
    (stepped : SupplyChainStep state event = some next) :
    next.activeAuthority ≤ next.authorityCeiling := by
  have valid := accepted_supply_chain_step_is_valid stepped
  have applies := accepted_supply_chain_step_applies_event stepped
  subst next
  rcases valid with ⟨_, _, _, _, _, requestedBound, _⟩
  cases h : event.kind <;>
    simp [applySupplyChainEvent, h, bounded, requestedBound]

theorem successful_supply_chain_run_preserves_identity
    {state final : SupplyChainState} {events : List SupplyChainEvent}
    (ran : SupplyChainRun state events = some final) :
    supplyChainIdentity final = supplyChainIdentity state := by
  induction events generalizing state with
  | nil =>
      simp [SupplyChainRun] at ran
      subst final
      rfl
  | cons event tail ih =>
      cases stepped : SupplyChainStep state event with
      | none => simp [SupplyChainRun, stepped] at ran
      | some next =>
          have tailRan : SupplyChainRun next tail = some final := by
            simpa [SupplyChainRun, stepped] using ran
          calc
            supplyChainIdentity final = supplyChainIdentity next := ih tailRan
            _ = supplyChainIdentity state := by
              have applies := accepted_supply_chain_step_applies_event stepped
              subst next
              exact apply_supply_chain_event_preserves_identity state event

theorem successful_supply_chain_run_preserves_non_authority
    {state final : SupplyChainState} {events : List SupplyChainEvent}
    (ran : SupplyChainRun state events = some final) :
    final.supportAssignmentCount = state.supportAssignmentCount ∧
      final.externalEffectAuthorityCount = state.externalEffectAuthorityCount := by
  induction events generalizing state with
  | nil =>
      simp [SupplyChainRun] at ran
      subst final
      exact ⟨rfl, rfl⟩
  | cons event tail ih =>
      cases stepped : SupplyChainStep state event with
      | none => simp [SupplyChainRun, stepped] at ran
      | some next =>
          have tailRan : SupplyChainRun next tail = some final := by
            simpa [SupplyChainRun, stepped] using ran
          have tailPreserved := ih tailRan
          have stepPreserved := accepted_supply_chain_step_preserves_non_authority stepped
          exact ⟨tailPreserved.1.trans stepPreserved.1,
            tailPreserved.2.trans stepPreserved.2⟩

theorem successful_supply_chain_run_respects_authority_ceiling
    {state final : SupplyChainState} {events : List SupplyChainEvent}
    (bounded : state.activeAuthority ≤ state.authorityCeiling)
    (ran : SupplyChainRun state events = some final) :
    final.activeAuthority ≤ final.authorityCeiling := by
  induction events generalizing state with
  | nil =>
      simp [SupplyChainRun] at ran
      subst final
      exact bounded
  | cons event tail ih =>
      cases stepped : SupplyChainStep state event with
      | none => simp [SupplyChainRun, stepped] at ran
      | some next =>
          have tailRan : SupplyChainRun next tail = some final := by
            simpa [SupplyChainRun, stepped] using ran
          exact ih
            (accepted_supply_chain_step_respects_authority_ceiling bounded stepped)
            tailRan

theorem successful_supply_chain_run_has_valid_trace
    {state final : SupplyChainState} {events : List SupplyChainEvent}
    (ran : SupplyChainRun state events = some final) :
    SupplyChainTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : SupplyChainStep state event with
      | none => simp [SupplyChainRun, stepped] at ran
      | some next =>
          have tailRan : SupplyChainRun next tail = some final := by
            simpa [SupplyChainRun, stepped] using ran
          have applies := accepted_supply_chain_step_applies_event stepped
          exact ⟨accepted_supply_chain_step_is_valid stepped, by
            simpa [applies] using ih tailRan⟩

theorem supply_chain_run_composes
    {state middle final : SupplyChainState}
    {front back : List SupplyChainEvent}
    (first : SupplyChainRun state front = some middle)
    (second : SupplyChainRun middle back = some final) :
    SupplyChainRun state (front ++ back) = some final := by
  induction front generalizing state middle with
  | nil =>
      simp [SupplyChainRun] at first
      subst middle
      exact second
  | cons event tail ih =>
      cases stepped : SupplyChainStep state event with
      | none => simp [SupplyChainRun, stepped] at first
      | some next =>
          have tailFirst : SupplyChainRun next tail = some middle := by
            simpa [SupplyChainRun, stepped] using first
          simpa [SupplyChainRun, stepped] using ih tailFirst second

theorem quarantined_artifact_cannot_be_admitted
    {state : SupplyChainState} {event : SupplyChainEvent}
    (quarantined : state.stage = .quarantined)
    (admit : event.kind = .admit) :
    SupplyChainStep state event = none := by
  simp [SupplyChainStep, SupplyChainEventValid, quarantined, admit]

theorem accepted_admission_requires_clean_review
    {state next : SupplyChainState} {event : SupplyChainEvent}
    (admit : event.kind = .admit)
    (stepped : SupplyChainStep state event = some next) :
    state.stage = .reviewedClean := by
  have valid := accepted_supply_chain_step_is_valid stepped
  cases h : state.stage <;>
    simp [SupplyChainEventValid, h, admit] at valid ⊢

theorem accepted_admission_records_authority_and_receipt
    {state next : SupplyChainState} {event : SupplyChainEvent}
    (admit : event.kind = .admit)
    (stepped : SupplyChainStep state event = some next) :
    next.stage = .admitted ∧
      next.activeAuthority = event.requestedAuthority ∧
      next.admissionReceiptCount = state.admissionReceiptCount + 1 := by
  have applies := accepted_supply_chain_step_applies_event stepped
  subst next
  simp [applySupplyChainEvent, admit]

theorem accepted_revocation_zeros_authority_and_records_invalidation
    {state next : SupplyChainState} {event : SupplyChainEvent}
    (revoke : event.kind = .revoke)
    (stepped : SupplyChainStep state event = some next) :
    next.stage = .revoked ∧
      next.activeAuthority = 0 ∧
      next.invalidationReceiptCount = state.invalidationReceiptCount + 1 := by
  have applies := accepted_supply_chain_step_applies_event stepped
  subst next
  simp [applySupplyChainEvent, revoke]

def supplyChainInitialState : SupplyChainState := {
  stage := .received
  artifactId := 10
  artifactDigest := 20
  lineageId := 30
  supplierId := 40
  buildOrTrainingId := 50
  authorityCeiling := 3
  activeAuthority := 0
  admissionReceiptCount := 0
  invalidationReceiptCount := 0
  supportAssignmentCount := 0
  externalEffectAuthorityCount := 0
}

def supplyChainEvent (kind : SupplyChainEventKind) : SupplyChainEvent := {
  kind := kind
  artifactId := 10
  artifactDigest := 20
  lineageId := 30
  supplierId := 40
  buildOrTrainingId := 50
  requestedAuthority := 2
  signatureVerified := true
  componentInventoryComplete := true
  advisoryReviewIndependent := true
  criticalAdvisoryPresent := false
  revocationPathPresent := true
  residualOwnerPresent := true
  nonClaimBoundaryPresent := true
  supportAssignmentRequested := false
  externalEffectAuthorityRequested := false
}

def admittedThenRevokedEvents : List SupplyChainEvent :=
  [.bindProvenance, .reviewClean, .admit, .revoke].map supplyChainEvent

def criticalAdvisoryEvents : List SupplyChainEvent :=
  [.bindProvenance, .reviewCritical].map fun kind =>
    if kind = .reviewCritical then
      { supplyChainEvent kind with criticalAdvisoryPresent := true }
    else supplyChainEvent kind

def revokedSupplyChainFinalState : SupplyChainState :=
  { supplyChainInitialState with
    stage := .revoked
    activeAuthority := 0
    admissionReceiptCount := 1
    invalidationReceiptCount := 1 }

def quarantinedSupplyChainFinalState : SupplyChainState :=
  { supplyChainInitialState with stage := .quarantined }

theorem admitted_then_revoked_run_reaches_zero_authority :
    ∃ final,
      SupplyChainRun supplyChainInitialState admittedThenRevokedEvents = some final ∧
      final.stage = .revoked ∧
      final.activeAuthority = 0 ∧
      final.admissionReceiptCount = 1 ∧
      final.invalidationReceiptCount = 1 := by
  refine ⟨revokedSupplyChainFinalState, ?_⟩
  native_decide

theorem critical_advisory_run_reaches_quarantine :
    ∃ final,
      SupplyChainRun supplyChainInitialState criticalAdvisoryEvents = some final ∧
      final.stage = .quarantined ∧
      final.activeAuthority = 0 := by
  refine ⟨quarantinedSupplyChainFinalState, ?_⟩
  native_decide

end AsiStackProofs.SupplyChainIntegrity

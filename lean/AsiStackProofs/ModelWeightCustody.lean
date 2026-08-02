namespace AsiStackProofs.ModelWeightCustody

inductive WeightLoadRoute where
  | retainAsCustodyDraft
  | requireCustodyRepair
  | requireAccountableReview
  | blockRequestedLoad
  | releaseToReadinessReview
deriving DecidableEq, Repr

structure WeightCustodyRecord where
  modelIdentityRecorded : Bool
  artifactLineageRecorded : Bool
  custodyAuthorityRecorded : Bool
  encryptedArtifactRecorded : Bool
  keyReleasePolicyRecorded : Bool
  attestationRequired : Bool
  attestationValid : Bool
  environmentIdentityRecorded : Bool
  accessScopeRecorded : Bool
  revocationPathRecorded : Bool
  residualOwnerRecorded : Bool
  loadRequested : Bool
deriving DecidableEq, Repr

def WeightLoadRouteFor (record : WeightCustodyRecord) : WeightLoadRoute :=
  if record.modelIdentityRecorded = false then
    WeightLoadRoute.retainAsCustodyDraft
  else if record.artifactLineageRecorded = false then
    WeightLoadRoute.requireCustodyRepair
  else if record.custodyAuthorityRecorded = false then
    WeightLoadRoute.requireAccountableReview
  else if record.encryptedArtifactRecorded = false then
    WeightLoadRoute.requireCustodyRepair
  else if record.keyReleasePolicyRecorded = false then
    WeightLoadRoute.requireAccountableReview
  else if record.environmentIdentityRecorded = false then
    WeightLoadRoute.requireAccountableReview
  else if record.accessScopeRecorded = false then
    WeightLoadRoute.requireAccountableReview
  else if record.revocationPathRecorded = false then
    WeightLoadRoute.requireCustodyRepair
  else if record.residualOwnerRecorded = false then
    WeightLoadRoute.requireCustodyRepair
  else if record.attestationRequired = true && record.attestationValid = false then
    WeightLoadRoute.blockRequestedLoad
  else if record.loadRequested = true then
    WeightLoadRoute.releaseToReadinessReview
  else
    WeightLoadRoute.retainAsCustodyDraft

theorem required_invalid_attestation_blocks_requested_load
    {record : WeightCustodyRecord} :
    record.modelIdentityRecorded = true ->
    record.artifactLineageRecorded = true ->
    record.custodyAuthorityRecorded = true ->
    record.encryptedArtifactRecorded = true ->
    record.keyReleasePolicyRecorded = true ->
    record.attestationRequired = true ->
    record.attestationValid = false ->
    record.environmentIdentityRecorded = true ->
    record.accessScopeRecorded = true ->
    record.revocationPathRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.loadRequested = true ->
    WeightLoadRouteFor record = WeightLoadRoute.blockRequestedLoad := by
  intro modelIdentity artifactLineage custodyAuthority encryptedArtifact
    keyReleasePolicy attestationRequired invalidAttestation environmentIdentity
    accessScope revocationPath residualOwner loadRequested
  unfold WeightLoadRouteFor
  simp [modelIdentity, artifactLineage, custodyAuthority, encryptedArtifact,
    keyReleasePolicy, attestationRequired, invalidAttestation,
    environmentIdentity, accessScope, revocationPath, residualOwner]

theorem missing_lineage_requires_custody_repair
    {record : WeightCustodyRecord} :
    record.modelIdentityRecorded = true ->
    record.artifactLineageRecorded = false ->
    WeightLoadRouteFor record = WeightLoadRoute.requireCustodyRepair := by
  intro modelIdentity missingLineage
  unfold WeightLoadRouteFor
  simp [modelIdentity, missingLineage]

inductive CustodyLifecycleRoute where
  | retainAsDraft
  | requireLineageRepair
  | requirePolicyReview
  | requireFreshAttestation
  | requireDependencyReview
  | requireIndependentObservation
  | rejectReleaseLaundering
  | recordIrreversibleRelease
  | admitBoundedLoad
deriving DecidableEq, Repr

structure CustodyLifecycleRecord where
  artifactDigestRecorded : Bool
  lineageRecorded : Bool
  policyDigestRecorded : Bool
  verifierIdentityRecorded : Bool
  measurementRecorded : Bool
  recipientScopeRecorded : Bool
  expiryRecorded : Bool
  attestationCurrent : Bool
  attestationValid : Bool
  verifierDependenciesRecorded : Bool
  independentLoadObservationRecorded : Bool
  residualOwnerRecorded : Bool
  revocationSemanticsRecorded : Bool
  noAuthorityGrantRecorded : Bool
  loadRequested : Bool
  distributionRequested : Bool
  irreversibilityAcknowledged : Bool
deriving DecidableEq, Repr

def CustodyLifecycleRouteFor
    (record : CustodyLifecycleRecord) : CustodyLifecycleRoute :=
  if record.artifactDigestRecorded = false then
    CustodyLifecycleRoute.retainAsDraft
  else if record.lineageRecorded = false then
    CustodyLifecycleRoute.requireLineageRepair
  else if record.policyDigestRecorded = false then
    CustodyLifecycleRoute.requirePolicyReview
  else if record.verifierIdentityRecorded = false then
    CustodyLifecycleRoute.requirePolicyReview
  else if record.measurementRecorded = false then
    CustodyLifecycleRoute.requirePolicyReview
  else if record.recipientScopeRecorded = false then
    CustodyLifecycleRoute.requirePolicyReview
  else if record.expiryRecorded = false || record.attestationCurrent = false then
    CustodyLifecycleRoute.requireFreshAttestation
  else if record.attestationValid = false then
    CustodyLifecycleRoute.requireFreshAttestation
  else if record.verifierDependenciesRecorded = false then
    CustodyLifecycleRoute.requireDependencyReview
  else if record.loadRequested = true &&
      record.independentLoadObservationRecorded = false then
    CustodyLifecycleRoute.requireIndependentObservation
  else if record.residualOwnerRecorded = false then
    CustodyLifecycleRoute.requirePolicyReview
  else if record.revocationSemanticsRecorded = false then
    CustodyLifecycleRoute.requirePolicyReview
  else if record.distributionRequested = true &&
      record.noAuthorityGrantRecorded = false then
    CustodyLifecycleRoute.rejectReleaseLaundering
  else if record.distributionRequested = true &&
      record.irreversibilityAcknowledged = true then
    CustodyLifecycleRoute.recordIrreversibleRelease
  else if record.distributionRequested = true then
    CustodyLifecycleRoute.rejectReleaseLaundering
  else if record.loadRequested = true then
    CustodyLifecycleRoute.admitBoundedLoad
  else
    CustodyLifecycleRoute.retainAsDraft

theorem complete_observed_load_is_bounded
    {record : CustodyLifecycleRecord} :
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.policyDigestRecorded = true ->
    record.verifierIdentityRecorded = true ->
    record.measurementRecorded = true ->
    record.recipientScopeRecorded = true ->
    record.expiryRecorded = true ->
    record.attestationCurrent = true ->
    record.attestationValid = true ->
    record.verifierDependenciesRecorded = true ->
    record.independentLoadObservationRecorded = true ->
    record.residualOwnerRecorded = true ->
    record.revocationSemanticsRecorded = true ->
    record.loadRequested = true ->
    record.distributionRequested = false ->
    CustodyLifecycleRouteFor record = CustodyLifecycleRoute.admitBoundedLoad := by
  intro artifact lineage policy verifier measurement recipient expiry current
    valid dependencies observation residual revocation load noDistribution
  unfold CustodyLifecycleRouteFor
  simp [artifact, lineage, policy, verifier, measurement, recipient, expiry,
    current, valid, dependencies, observation, residual, revocation, load,
    noDistribution]

theorem missing_lineage_blocks_lifecycle
    {record : CustodyLifecycleRecord} :
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = false ->
    CustodyLifecycleRouteFor record = CustodyLifecycleRoute.requireLineageRepair := by
  intro artifact missingLineage
  unfold CustodyLifecycleRouteFor
  simp [artifact, missingLineage]

theorem stale_attestation_requires_refresh
    {record : CustodyLifecycleRecord} :
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.policyDigestRecorded = true ->
    record.verifierIdentityRecorded = true ->
    record.measurementRecorded = true ->
    record.recipientScopeRecorded = true ->
    record.expiryRecorded = true ->
    record.attestationCurrent = false ->
    CustodyLifecycleRouteFor record =
      CustodyLifecycleRoute.requireFreshAttestation := by
  intro artifact lineage policy verifier measurement recipient expiry stale
  unfold CustodyLifecycleRouteFor
  simp [artifact, lineage, policy, verifier, measurement, recipient, expiry, stale]

theorem undisclosed_verifier_dependencies_require_review
    {record : CustodyLifecycleRecord} :
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.policyDigestRecorded = true ->
    record.verifierIdentityRecorded = true ->
    record.measurementRecorded = true ->
    record.recipientScopeRecorded = true ->
    record.expiryRecorded = true ->
    record.attestationCurrent = true ->
    record.attestationValid = true ->
    record.verifierDependenciesRecorded = false ->
    CustodyLifecycleRouteFor record =
      CustodyLifecycleRoute.requireDependencyReview := by
  intro artifact lineage policy verifier measurement recipient expiry current
    valid missingDependencies
  unfold CustodyLifecycleRouteFor
  simp [artifact, lineage, policy, verifier, measurement, recipient, expiry,
    current, valid, missingDependencies]

theorem unobserved_load_requires_observation
    {record : CustodyLifecycleRecord} :
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.policyDigestRecorded = true ->
    record.verifierIdentityRecorded = true ->
    record.measurementRecorded = true ->
    record.recipientScopeRecorded = true ->
    record.expiryRecorded = true ->
    record.attestationCurrent = true ->
    record.attestationValid = true ->
    record.verifierDependenciesRecorded = true ->
    record.loadRequested = true ->
    record.independentLoadObservationRecorded = false ->
    CustodyLifecycleRouteFor record =
      CustodyLifecycleRoute.requireIndependentObservation := by
  intro artifact lineage policy verifier measurement recipient expiry current
    valid dependencies load missingObservation
  unfold CustodyLifecycleRouteFor
  simp [artifact, lineage, policy, verifier, measurement, recipient, expiry,
    current, valid, dependencies, load, missingObservation]

theorem distribution_cannot_launder_load_authority
    {record : CustodyLifecycleRecord} :
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.policyDigestRecorded = true ->
    record.verifierIdentityRecorded = true ->
    record.measurementRecorded = true ->
    record.recipientScopeRecorded = true ->
    record.expiryRecorded = true ->
    record.attestationCurrent = true ->
    record.attestationValid = true ->
    record.verifierDependenciesRecorded = true ->
    record.loadRequested = false ->
    record.residualOwnerRecorded = true ->
    record.revocationSemanticsRecorded = true ->
    record.distributionRequested = true ->
    record.noAuthorityGrantRecorded = false ->
    CustodyLifecycleRouteFor record =
      CustodyLifecycleRoute.rejectReleaseLaundering := by
  intro artifact lineage policy verifier measurement recipient expiry current
    valid dependencies noLoad residual revocation distribution authorityLaundering
  unfold CustodyLifecycleRouteFor
  simp [artifact, lineage, policy, verifier, measurement, recipient, expiry,
    current, valid, dependencies, noLoad, residual, revocation, distribution,
    authorityLaundering]

theorem acknowledged_distribution_records_irreversibility
    {record : CustodyLifecycleRecord} :
    record.artifactDigestRecorded = true ->
    record.lineageRecorded = true ->
    record.policyDigestRecorded = true ->
    record.verifierIdentityRecorded = true ->
    record.measurementRecorded = true ->
    record.recipientScopeRecorded = true ->
    record.expiryRecorded = true ->
    record.attestationCurrent = true ->
    record.attestationValid = true ->
    record.verifierDependenciesRecorded = true ->
    record.loadRequested = false ->
    record.residualOwnerRecorded = true ->
    record.revocationSemanticsRecorded = true ->
    record.noAuthorityGrantRecorded = true ->
    record.distributionRequested = true ->
    record.irreversibilityAcknowledged = true ->
    CustodyLifecycleRouteFor record =
      CustodyLifecycleRoute.recordIrreversibleRelease := by
  intro artifact lineage policy verifier measurement recipient expiry current
    valid dependencies noLoad residual revocation noAuthority distribution
    irreversibility
  unfold CustodyLifecycleRouteFor
  simp [artifact, lineage, policy, verifier, measurement, recipient, expiry,
    current, valid, dependencies, noLoad, residual, revocation, noAuthority,
    distribution, irreversibility]

/-! ## Versioned attestation-to-erasure lifecycle

The lifecycle orders attestation, key release, bounded load, independent load
observation, descendant-key revocation, and erasure. All evidence fields remain
trusted finite inputs; no theorem establishes genuine hardware attestation,
weight confidentiality, extraction resistance, or deployed erasure.
-/

inductive WeightCustodyStage where
  | sealed
  | attested
  | keyReleased
  | loaded
  | observed
  | revoked
  | erased
deriving DecidableEq, Repr

inductive WeightCustodyEventKind where
  | recordAttestation
  | releaseKey
  | loadWeights
  | observeLoad
  | revokeKey
  | recordErasure
deriving DecidableEq, Repr

structure WeightCustodyState where
  artifactId : Nat
  policyId : Nat
  environmentId : Nat
  recipientId : Nat
  custodianId : Nat
  verifierId : Nat
  keyServiceId : Nat
  loaderId : Nat
  observerId : Nat
  version : Nat
  baseAuthorityCeiling : Nat
  currentAuthorityCeiling : Nat
  stage : WeightCustodyStage
  descendantKeyCount : Nat
  revokedDescendantKeyCount : Nat
  keyActive : Bool
  attestationExpiresAt : Nat
  observationReceiptCount : Nat
  revocationReceiptCount : Nat
  erasureReceiptCount : Nat
  residualCount : Nat
  now : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

structure WeightCustodyEvent where
  kind : WeightCustodyEventKind
  artifactId : Nat
  policyId : Nat
  environmentId : Nat
  recipientId : Nat
  actorId : Nat
  expectedVersion : Nat
  targetVersion : Nat
  requestedAuthorityCeiling : Nat
  observedNow : Nat
  requestedAttestationExpiry : Nat
  measurementPresent : Bool
  attestationValid : Bool
  policyAuthorizationPresent : Bool
  keyReleaseReceiptPresent : Bool
  loadReceiptPresent : Bool
  distributionRequested : Bool
  independentObservationPresent : Bool
  observationReceiptPresent : Bool
  revocationReceiptPresent : Bool
  requestedRevokedDescendantKeyCount : Nat
  erasureReceiptPresent : Bool
  residualPresent : Bool
  claimsHardwareTrust : Bool
  claimsConfidentiality : Bool
  requestsSupportAssignment : Bool
  requestsExternalEffect : Bool
deriving DecidableEq, Repr

def WeightCustodyEventAdmissible
    (state : WeightCustodyState) (event : WeightCustodyEvent) : Prop :=
  event.artifactId = state.artifactId ∧
    event.policyId = state.policyId ∧
    event.environmentId = state.environmentId ∧
    event.recipientId = state.recipientId ∧
    event.expectedVersion = state.version ∧
    state.now ≤ event.observedNow ∧
    event.claimsHardwareTrust = false ∧
    event.claimsConfidentiality = false ∧
    event.requestsSupportAssignment = false ∧
    event.requestsExternalEffect = false ∧
    match event.kind with
    | WeightCustodyEventKind.recordAttestation =>
        state.stage = WeightCustodyStage.sealed ∧
          event.actorId = state.verifierId ∧
          state.verifierId ≠ state.custodianId ∧
          event.measurementPresent = true ∧
          event.attestationValid = true ∧
          event.observedNow < event.requestedAttestationExpiry ∧
          event.targetVersion = state.version ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling
    | WeightCustodyEventKind.releaseKey =>
        state.stage = WeightCustodyStage.attested ∧
          event.actorId = state.keyServiceId ∧
          event.policyAuthorizationPresent = true ∧
          event.keyReleaseReceiptPresent = true ∧
          event.observedNow < state.attestationExpiresAt ∧
          event.requestedAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
          event.targetVersion = state.version + 1
    | WeightCustodyEventKind.loadWeights =>
        state.stage = WeightCustodyStage.keyReleased ∧
          state.keyActive = true ∧
          event.actorId = state.loaderId ∧
          event.loadReceiptPresent = true ∧
          event.distributionRequested = false ∧
          event.observedNow < state.attestationExpiresAt ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling ∧
          event.targetVersion = state.version
    | WeightCustodyEventKind.observeLoad =>
        state.stage = WeightCustodyStage.loaded ∧
          event.actorId = state.observerId ∧
          state.observerId ≠ state.loaderId ∧
          state.observerId ≠ state.keyServiceId ∧
          event.independentObservationPresent = true ∧
          event.observationReceiptPresent = true ∧
          event.requestedAuthorityCeiling = state.currentAuthorityCeiling ∧
          event.targetVersion = state.version
    | WeightCustodyEventKind.revokeKey =>
        state.stage = WeightCustodyStage.observed ∧
          event.actorId = state.keyServiceId ∧
          event.revocationReceiptPresent = true ∧
          event.requestedRevokedDescendantKeyCount = state.descendantKeyCount ∧
          event.requestedAuthorityCeiling = 0 ∧
          event.targetVersion = state.version + 1
    | WeightCustodyEventKind.recordErasure =>
        state.stage = WeightCustodyStage.revoked ∧
          state.keyActive = false ∧
          state.revokedDescendantKeyCount = state.descendantKeyCount ∧
          event.actorId = state.loaderId ∧
          event.erasureReceiptPresent = true ∧
          event.residualPresent = true ∧
          event.requestedAuthorityCeiling = 0 ∧
          event.targetVersion = state.version

instance weightCustodyEventAdmissibleDecidable
    (state : WeightCustodyState) (event : WeightCustodyEvent) :
    Decidable (WeightCustodyEventAdmissible state event) := by
  unfold WeightCustodyEventAdmissible
  cases event.kind <;> infer_instance

def AdvanceWeightCustody
    (state : WeightCustodyState) (event : WeightCustodyEvent) :
    WeightCustodyState :=
  match event.kind with
  | WeightCustodyEventKind.recordAttestation =>
      { state with
        stage := WeightCustodyStage.attested
        attestationExpiresAt := event.requestedAttestationExpiry
        now := event.observedNow }
  | WeightCustodyEventKind.releaseKey =>
      { state with
        stage := WeightCustodyStage.keyReleased
        version := event.targetVersion
        currentAuthorityCeiling := event.requestedAuthorityCeiling
        keyActive := true
        now := event.observedNow }
  | WeightCustodyEventKind.loadWeights =>
      { state with
        stage := WeightCustodyStage.loaded
        now := event.observedNow }
  | WeightCustodyEventKind.observeLoad =>
      { state with
        stage := WeightCustodyStage.observed
        observationReceiptCount := state.observationReceiptCount + 1
        now := event.observedNow }
  | WeightCustodyEventKind.revokeKey =>
      { state with
        stage := WeightCustodyStage.revoked
        version := event.targetVersion
        currentAuthorityCeiling := 0
        keyActive := false
        revokedDescendantKeyCount := event.requestedRevokedDescendantKeyCount
        revocationReceiptCount := state.revocationReceiptCount + 1
        now := event.observedNow }
  | WeightCustodyEventKind.recordErasure =>
      { state with
        stage := WeightCustodyStage.erased
        erasureReceiptCount := state.erasureReceiptCount + 1
        residualCount := state.residualCount + 1
        now := event.observedNow }

def ApplyWeightCustodyEvent
    (state : WeightCustodyState) (event : WeightCustodyEvent) :
    Option WeightCustodyState :=
  if WeightCustodyEventAdmissible state event then
    some (AdvanceWeightCustody state event)
  else none

def RunWeightCustodyEvents :
    WeightCustodyState -> List WeightCustodyEvent -> Option WeightCustodyState
  | state, [] => some state
  | state, event :: tail =>
      match ApplyWeightCustodyEvent state event with
      | none => none
      | some next => RunWeightCustodyEvents next tail

theorem accepted_weight_custody_event_is_admissible
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    WeightCustodyEventAdmissible state event := by
  unfold ApplyWeightCustodyEvent at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem accepted_weight_custody_event_is_exact_advance
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    next = AdvanceWeightCustody state event := by
  unfold ApplyWeightCustodyEvent at accepted
  split at accepted
  · simp at accepted
    exact accepted.symm
  · simp at accepted

theorem accepted_weight_custody_event_preserves_identity
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    next.artifactId = state.artifactId ∧ next.policyId = state.policyId ∧
      next.environmentId = state.environmentId ∧
      next.recipientId = state.recipientId ∧
      next.custodianId = state.custodianId ∧
      next.verifierId = state.verifierId ∧
      next.keyServiceId = state.keyServiceId ∧
      next.loaderId = state.loaderId ∧ next.observerId = state.observerId ∧
      next.baseAuthorityCeiling = state.baseAuthorityCeiling := by
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  subst next
  cases kind : event.kind <;> simp [AdvanceWeightCustody, kind]

theorem accepted_weight_custody_event_is_non_authorizing
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    event.claimsHardwareTrust = false ∧
      event.claimsConfidentiality = false ∧
      event.requestsSupportAssignment = false ∧
      event.requestsExternalEffect = false ∧
      next.supportAssignmentCount = state.supportAssignmentCount ∧
      next.externalEffectCount = state.externalEffectCount := by
  have admissible := accepted_weight_custody_event_is_admissible accepted
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, noTrust, noConfidentiality,
    noSupport, noEffect, _⟩
  subst next
  exact ⟨noTrust, noConfidentiality, noSupport, noEffect,
    by cases kind : event.kind <;> simp [AdvanceWeightCustody, kind],
    by cases kind : event.kind <;> simp [AdvanceWeightCustody, kind]⟩

theorem accepted_weight_custody_event_never_widens_authority
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling := by
  have admissible := accepted_weight_custody_event_is_admissible accepted
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  subst next
  cases kind : event.kind with
  | recordAttestation => simp [AdvanceWeightCustody, kind]
  | releaseKey =>
      simp [kind] at route
      simpa [AdvanceWeightCustody, kind] using route.2.2.2.2.2.1
  | loadWeights => simp [AdvanceWeightCustody, kind]
  | observeLoad => simp [AdvanceWeightCustody, kind]
  | revokeKey => simp [AdvanceWeightCustody, kind]
  | recordErasure => simp [AdvanceWeightCustody, kind]

theorem accepted_attestation_is_independent_and_future_bounded
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (kind : event.kind = WeightCustodyEventKind.recordAttestation)
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    state.stage = WeightCustodyStage.sealed ∧
      event.actorId = state.verifierId ∧ state.verifierId ≠ state.custodianId ∧
      event.measurementPresent = true ∧ event.attestationValid = true ∧
      next.now < next.attestationExpiresAt := by
  have admissible := accepted_weight_custody_event_is_admissible accepted
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨sealed, actor, independent, measurement, valid, future, _, _⟩
  subst next
  simp [AdvanceWeightCustody, kind, sealed, actor, independent, measurement,
    valid, future]

theorem accepted_key_release_is_current_bounded_and_versioned
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (kind : event.kind = WeightCustodyEventKind.releaseKey)
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    state.stage = WeightCustodyStage.attested ∧
      event.policyAuthorizationPresent = true ∧
      event.keyReleaseReceiptPresent = true ∧
      event.observedNow < state.attestationExpiresAt ∧
      next.currentAuthorityCeiling ≤ state.currentAuthorityCeiling ∧
      next.version = state.version + 1 ∧ next.keyActive = true := by
  have admissible := accepted_weight_custody_event_is_admissible accepted
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨attested, _, authorized, receipt, current, bounded, versioned⟩
  subst next
  simp [AdvanceWeightCustody, kind, attested, authorized, receipt, current,
    bounded, versioned]

theorem accepted_load_requires_active_key_receipt_and_no_distribution
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (kind : event.kind = WeightCustodyEventKind.loadWeights)
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    state.stage = WeightCustodyStage.keyReleased ∧ state.keyActive = true ∧
      event.actorId = state.loaderId ∧ event.loadReceiptPresent = true ∧
      event.distributionRequested = false ∧
      event.observedNow < state.attestationExpiresAt ∧
      next.stage = WeightCustodyStage.loaded := by
  have admissible := accepted_weight_custody_event_is_admissible accepted
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨released, active, actor, receipt, noDistribution, current, _, _⟩
  subst next
  simp [AdvanceWeightCustody, kind, released, active, actor, receipt,
    noDistribution, current]

theorem accepted_load_observation_is_independent
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (kind : event.kind = WeightCustodyEventKind.observeLoad)
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    state.stage = WeightCustodyStage.loaded ∧
      event.actorId = state.observerId ∧ state.observerId ≠ state.loaderId ∧
      state.observerId ≠ state.keyServiceId ∧
      next.observationReceiptCount = state.observationReceiptCount + 1 := by
  have admissible := accepted_weight_custody_event_is_admissible accepted
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨loaded, actor, notLoader, notKeyService, _, _, _, _⟩
  subst next
  simp [AdvanceWeightCustody, kind, loaded, actor, notLoader, notKeyService]

theorem accepted_key_revocation_closes_authority_and_descendants
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (kind : event.kind = WeightCustodyEventKind.revokeKey)
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    state.stage = WeightCustodyStage.observed ∧
      event.revocationReceiptPresent = true ∧
      next.keyActive = false ∧ next.currentAuthorityCeiling = 0 ∧
      next.revokedDescendantKeyCount = state.descendantKeyCount ∧
      next.revocationReceiptCount = state.revocationReceiptCount + 1 := by
  have admissible := accepted_weight_custody_event_is_admissible accepted
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨observed, _, receipt, descendants, _, _⟩
  subst next
  simp [AdvanceWeightCustody, kind, observed, receipt, descendants]

theorem accepted_erasure_follows_complete_revocation_and_records_residual
    {state next : WeightCustodyState} {event : WeightCustodyEvent}
    (kind : event.kind = WeightCustodyEventKind.recordErasure)
    (accepted : ApplyWeightCustodyEvent state event = some next) :
    state.stage = WeightCustodyStage.revoked ∧ state.keyActive = false ∧
      state.revokedDescendantKeyCount = state.descendantKeyCount ∧
      event.erasureReceiptPresent = true ∧ event.residualPresent = true ∧
      next.stage = WeightCustodyStage.erased ∧
      next.erasureReceiptCount = state.erasureReceiptCount + 1 ∧
      next.residualCount = state.residualCount + 1 := by
  have admissible := accepted_weight_custody_event_is_admissible accepted
  have exactAdvance := accepted_weight_custody_event_is_exact_advance accepted
  rcases admissible with ⟨_, _, _, _, _, _, _, _, _, _, route⟩
  rw [kind] at route
  rcases route with ⟨revoked, inactive, complete, _, receipt, residual, _, _⟩
  subst next
  simp [AdvanceWeightCustody, kind, revoked, inactive, complete, receipt, residual]

theorem weight_custody_run_preserves_identity_non_authority_and_narrowing
    {initial final : WeightCustodyState} {events : List WeightCustodyEvent}
    (run : RunWeightCustodyEvents initial events = some final) :
    final.artifactId = initial.artifactId ∧ final.policyId = initial.policyId ∧
      final.environmentId = initial.environmentId ∧
      final.recipientId = initial.recipientId ∧
      final.custodianId = initial.custodianId ∧
      final.verifierId = initial.verifierId ∧
      final.keyServiceId = initial.keyServiceId ∧
      final.loaderId = initial.loaderId ∧ final.observerId = initial.observerId ∧
      final.baseAuthorityCeiling = initial.baseAuthorityCeiling ∧
      final.currentAuthorityCeiling ≤ initial.currentAuthorityCeiling ∧
      final.supportAssignmentCount = initial.supportAssignmentCount ∧
      final.externalEffectCount = initial.externalEffectCount := by
  induction events generalizing initial with
  | nil => simp [RunWeightCustodyEvents] at run; subst final; simp
  | cons event tail ih =>
      simp only [RunWeightCustodyEvents] at run
      cases step : ApplyWeightCustodyEvent initial event with
      | none => simp [step] at run
      | some next =>
          simp [step] at run
          have identity := accepted_weight_custody_event_preserves_identity step
          have boundary := accepted_weight_custody_event_is_non_authorizing step
          have narrowed := accepted_weight_custody_event_never_widens_authority step
          have tailFacts := ih run
          rcases identity with ⟨artifact, policy, environment, recipient,
            custodian, verifier, keyService, loader, observer, base⟩
          rcases boundary with ⟨_, _, _, _, support, effects⟩
          rcases tailFacts with ⟨tartifact, tpolicy, tenvironment, trecipient,
            tcustodian, tverifier, tkeyService, tloader, tobserver, tbase,
            tnarrowed, tsupport, teffects⟩
          exact ⟨tartifact.trans artifact, tpolicy.trans policy,
            tenvironment.trans environment, trecipient.trans recipient,
            tcustodian.trans custodian, tverifier.trans verifier,
            tkeyService.trans keyService, tloader.trans loader,
            tobserver.trans observer, tbase.trans base,
            Nat.le_trans tnarrowed narrowed, tsupport.trans support,
            teffects.trans effects⟩

theorem weight_custody_runs_compose
    (initial : WeightCustodyState)
    (before after : List WeightCustodyEvent) :
    RunWeightCustodyEvents initial (before ++ after) =
      match RunWeightCustodyEvents initial before with
      | none => none
      | some middle => RunWeightCustodyEvents middle after := by
  induction before generalizing initial with
  | nil => simp [RunWeightCustodyEvents]
  | cons event tail ih =>
      simp only [List.cons_append, RunWeightCustodyEvents]
      cases step : ApplyWeightCustodyEvent initial event with
      | none => simp
      | some next => simp [ih]

def initialWeightCustodyState : WeightCustodyState := {
  artifactId := 113, policyId := 127, environmentId := 131, recipientId := 137
  custodianId := 139, verifierId := 149, keyServiceId := 151
  loaderId := 157, observerId := 163, version := 1
  baseAuthorityCeiling := 6, currentAuthorityCeiling := 6
  stage := WeightCustodyStage.sealed, descendantKeyCount := 4
  revokedDescendantKeyCount := 0, keyActive := false
  attestationExpiresAt := 0, observationReceiptCount := 0
  revocationReceiptCount := 0, erasureReceiptCount := 0, residualCount := 0
  now := 30, supportAssignmentCount := 0, externalEffectCount := 0
}

def weightAttestationEvent : WeightCustodyEvent := {
  kind := WeightCustodyEventKind.recordAttestation
  artifactId := 113, policyId := 127, environmentId := 131, recipientId := 137
  actorId := 149, expectedVersion := 1, targetVersion := 1
  requestedAuthorityCeiling := 6, observedNow := 31
  requestedAttestationExpiry := 50, measurementPresent := true
  attestationValid := true, policyAuthorizationPresent := false
  keyReleaseReceiptPresent := false, loadReceiptPresent := false
  distributionRequested := false, independentObservationPresent := false
  observationReceiptPresent := false, revocationReceiptPresent := false
  requestedRevokedDescendantKeyCount := 0, erasureReceiptPresent := false
  residualPresent := false, claimsHardwareTrust := false
  claimsConfidentiality := false, requestsSupportAssignment := false
  requestsExternalEffect := false
}

def weightKeyReleaseEvent : WeightCustodyEvent := {
  weightAttestationEvent with
  kind := WeightCustodyEventKind.releaseKey
  actorId := 151, expectedVersion := 1, targetVersion := 2
  requestedAuthorityCeiling := 4, observedNow := 32
  policyAuthorizationPresent := true, keyReleaseReceiptPresent := true
  measurementPresent := false, attestationValid := false
}

def weightLoadEvent : WeightCustodyEvent := {
  weightKeyReleaseEvent with
  kind := WeightCustodyEventKind.loadWeights
  actorId := 157, expectedVersion := 2, targetVersion := 2
  loadReceiptPresent := true, policyAuthorizationPresent := false
  keyReleaseReceiptPresent := false, observedNow := 33
}

def weightObservationEvent : WeightCustodyEvent := {
  weightLoadEvent with
  kind := WeightCustodyEventKind.observeLoad
  actorId := 163, loadReceiptPresent := false
  independentObservationPresent := true, observationReceiptPresent := true
  observedNow := 34
}

def weightRevocationEvent : WeightCustodyEvent := {
  weightObservationEvent with
  kind := WeightCustodyEventKind.revokeKey
  actorId := 151, targetVersion := 3, requestedAuthorityCeiling := 0
  independentObservationPresent := false, observationReceiptPresent := false
  revocationReceiptPresent := true, requestedRevokedDescendantKeyCount := 4
  observedNow := 35
}

def weightErasureEvent : WeightCustodyEvent := {
  weightRevocationEvent with
  kind := WeightCustodyEventKind.recordErasure
  actorId := 157, expectedVersion := 3, targetVersion := 3
  revocationReceiptPresent := false, erasureReceiptPresent := true
  residualPresent := true, observedNow := 36
}

def completeWeightCustodyTrace : List WeightCustodyEvent :=
  [weightAttestationEvent, weightKeyReleaseEvent, weightLoadEvent,
    weightObservationEvent, weightRevocationEvent, weightErasureEvent]

theorem complete_weight_custody_trace_reaches_exact_erased_state :
    RunWeightCustodyEvents initialWeightCustodyState completeWeightCustodyTrace =
      some { initialWeightCustodyState with
        version := 3
        currentAuthorityCeiling := 0, stage := WeightCustodyStage.erased
        revokedDescendantKeyCount := 4, keyActive := false
        attestationExpiresAt := 50, observationReceiptCount := 1
        revocationReceiptCount := 1, erasureReceiptCount := 1
        residualCount := 1, now := 36 } := by
  decide

theorem weight_custody_stale_version_is_rejected :
    ApplyWeightCustodyEvent initialWeightCustodyState
      { weightAttestationEvent with expectedVersion := 0 } = none := by decide

theorem weight_custody_self_attestation_is_rejected :
    ApplyWeightCustodyEvent initialWeightCustodyState
      { weightAttestationEvent with actorId := 139 } = none := by decide

theorem weight_custody_expired_key_release_is_rejected :
    RunWeightCustodyEvents initialWeightCustodyState
      [weightAttestationEvent,
        { weightKeyReleaseEvent with observedNow := 50 }] = none := by decide

theorem weight_custody_authority_widening_is_rejected :
    RunWeightCustodyEvents initialWeightCustodyState
      [weightAttestationEvent,
        { weightKeyReleaseEvent with requestedAuthorityCeiling := 7 }] = none := by decide

theorem weight_custody_distribution_during_load_is_rejected :
    RunWeightCustodyEvents initialWeightCustodyState
      [weightAttestationEvent, weightKeyReleaseEvent,
        { weightLoadEvent with distributionRequested := true }] = none := by decide

theorem weight_custody_self_observation_is_rejected :
    RunWeightCustodyEvents initialWeightCustodyState
      [weightAttestationEvent, weightKeyReleaseEvent, weightLoadEvent,
        { weightObservationEvent with actorId := 157 }] = none := by decide

theorem weight_custody_partial_descendant_revocation_is_rejected :
    RunWeightCustodyEvents initialWeightCustodyState
      [weightAttestationEvent, weightKeyReleaseEvent, weightLoadEvent,
        weightObservationEvent,
        { weightRevocationEvent with requestedRevokedDescendantKeyCount := 3 }] =
      none := by decide

theorem weight_custody_erasure_before_revocation_is_rejected :
    RunWeightCustodyEvents initialWeightCustodyState
      [weightAttestationEvent, weightKeyReleaseEvent, weightLoadEvent,
        weightObservationEvent, weightErasureEvent] = none := by decide

theorem weight_custody_confidentiality_laundering_is_rejected :
    ApplyWeightCustodyEvent initialWeightCustodyState
      { weightAttestationEvent with claimsConfidentiality := true } = none := by decide

end AsiStackProofs.ModelWeightCustody

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

end AsiStackProofs.ModelWeightCustody

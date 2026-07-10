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

end AsiStackProofs.ModelWeightCustody

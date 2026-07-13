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

end AsiStackProofs.SupplyChainIntegrity

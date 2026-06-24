namespace AsiStackProofs.ArtifactCompression

structure ArtifactUseRecord where
  compressedArtifactUsedForTask : Bool
  taskProbePassed : Bool
  routedToFallback : Bool
deriving DecidableEq, Repr

def ProbeOrFallbackSatisfied (record : ArtifactUseRecord) : Prop :=
  record.taskProbePassed = true ∨ record.routedToFallback = true

def CompressedArtifactUseValid (record : ArtifactUseRecord) : Prop :=
  record.compressedArtifactUsedForTask = true -> ProbeOrFallbackSatisfied record

theorem compressed_artifact_use_requires_probe_or_fallback
    {record : ArtifactUseRecord} :
    CompressedArtifactUseValid record ->
    record.compressedArtifactUsedForTask = true ->
    record.taskProbePassed = true ∨ record.routedToFallback = true := by
  intro valid used
  exact valid used

structure CompressionMetadataRecord where
  residualMetadataPresent : Bool
  fallbackMetadataPresent : Bool
  promotionCandidate : Bool
deriving DecidableEq, Repr

def CompressionMetadataComplete (record : CompressionMetadataRecord) : Prop :=
  record.residualMetadataPresent = true ∧ record.fallbackMetadataPresent = true

def CompressionPromotionMetadataValid (record : CompressionMetadataRecord) : Prop :=
  record.promotionCandidate = true -> CompressionMetadataComplete record

theorem promoted_compression_record_cannot_omit_residual_or_fallback_metadata
    {record : CompressionMetadataRecord} :
    CompressionPromotionMetadataValid record ->
    record.promotionCandidate = true ->
    record.residualMetadataPresent = true ∧ record.fallbackMetadataPresent = true := by
  intro valid promoted
  exact valid promoted

end AsiStackProofs.ArtifactCompression

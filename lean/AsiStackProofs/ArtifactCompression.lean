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

theorem invalid_compressed_artifact_use_without_probe_or_fallback_rejected
    {record : ArtifactUseRecord} :
    record.compressedArtifactUsedForTask = true ->
    record.taskProbePassed = false ->
    record.routedToFallback = false ->
    ¬ CompressedArtifactUseValid record := by
  intro used probeFailed fallbackMissing valid
  unfold CompressedArtifactUseValid at valid
  unfold ProbeOrFallbackSatisfied at valid
  have satisfied := valid used
  cases satisfied with
  | inl passed =>
      rw [probeFailed] at passed
      contradiction
  | inr fallback =>
      rw [fallbackMissing] at fallback
      contradiction

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

theorem promotion_candidate_missing_residual_or_fallback_rejected
    {record : CompressionMetadataRecord} :
    record.promotionCandidate = true ->
    (record.residualMetadataPresent = false ∨ record.fallbackMetadataPresent = false) ->
    ¬ CompressionPromotionMetadataValid record := by
  intro promoted missing valid
  unfold CompressionPromotionMetadataValid at valid
  unfold CompressionMetadataComplete at valid
  have complete := valid promoted
  cases complete with
  | intro residualPresent fallbackPresent =>
      cases missing with
      | inl residualMissing =>
          rw [residualMissing] at residualPresent
          contradiction
      | inr fallbackMissing =>
          rw [fallbackMissing] at fallbackPresent
          contradiction

end AsiStackProofs.ArtifactCompression

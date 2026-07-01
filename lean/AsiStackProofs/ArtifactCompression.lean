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

inductive CompressionAdmissionRoute where
  | noUseRequested
  | requestFullArtifactPreservation
  | requestCompressionManifest
  | requestUseEnvelope
  | requestAccessPattern
  | blockUnadmittedState
  | requestDecoderDeterminismRecord
  | blockExactReplayWithoutReadiness
  | requestTaskProbe
  | routeToFallback
  | requestFallbackArtifact
  | requestResidualMetadata
  | requestUtilityEvidence
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | admitCompressedArtifact
deriving DecidableEq, Repr

structure CompressionAdmissionReview where
  useRequested : Bool
  fullArtifactPreserved : Bool
  compressionManifestPresent : Bool
  declaredUseEnvelopePresent : Bool
  accessPatternDeclared : Bool
  admissionStateAllowsUse : Bool
  decoderDeterminismRecordPresent : Bool
  exactReplayRequired : Bool
  exactReplayReady : Bool
  taskProbeRequired : Bool
  taskProbePassed : Bool
  fallbackArtifactPresent : Bool
  residualMetadataPresent : Bool
  utilityEvidencePresent : Bool
  supportPromotionRequested : Bool
  evidenceTransitionPresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def CompressionAdmissionRouteFor
    (review : CompressionAdmissionReview) :
    CompressionAdmissionRoute :=
  if review.useRequested = false then
    CompressionAdmissionRoute.noUseRequested
  else if review.fullArtifactPreserved = false then
    CompressionAdmissionRoute.requestFullArtifactPreservation
  else if review.compressionManifestPresent = false then
    CompressionAdmissionRoute.requestCompressionManifest
  else if review.declaredUseEnvelopePresent = false then
    CompressionAdmissionRoute.requestUseEnvelope
  else if review.accessPatternDeclared = false then
    CompressionAdmissionRoute.requestAccessPattern
  else if review.admissionStateAllowsUse = false then
    CompressionAdmissionRoute.blockUnadmittedState
  else if review.decoderDeterminismRecordPresent = false then
    CompressionAdmissionRoute.requestDecoderDeterminismRecord
  else if review.exactReplayRequired = true ∧ review.exactReplayReady = false then
    CompressionAdmissionRoute.blockExactReplayWithoutReadiness
  else if review.taskProbeRequired = true ∧ review.taskProbePassed = false then
    if review.fallbackArtifactPresent = true then
      CompressionAdmissionRoute.routeToFallback
    else
      CompressionAdmissionRoute.requestFallbackArtifact
  else if review.residualMetadataPresent = false then
    CompressionAdmissionRoute.requestResidualMetadata
  else if review.utilityEvidencePresent = false then
    CompressionAdmissionRoute.requestUtilityEvidence
  else if review.supportPromotionRequested = true ∧ review.evidenceTransitionPresent = false then
    CompressionAdmissionRoute.requestEvidenceTransition
  else if review.nonClaimBoundaryPresent = false then
    CompressionAdmissionRoute.preserveNonClaimBoundary
  else
    CompressionAdmissionRoute.admitCompressedArtifact

def completeCompressionAdmissionReview : CompressionAdmissionReview where
  useRequested := true
  fullArtifactPreserved := true
  compressionManifestPresent := true
  declaredUseEnvelopePresent := true
  accessPatternDeclared := true
  admissionStateAllowsUse := true
  decoderDeterminismRecordPresent := true
  exactReplayRequired := true
  exactReplayReady := true
  taskProbeRequired := true
  taskProbePassed := true
  fallbackArtifactPresent := true
  residualMetadataPresent := true
  utilityEvidencePresent := true
  supportPromotionRequested := false
  evidenceTransitionPresent := true
  nonClaimBoundaryPresent := true

theorem no_compressed_use_request_stays_idle :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          useRequested := false } =
      CompressionAdmissionRoute.noUseRequested := by
  simp [CompressionAdmissionRouteFor]

theorem missing_full_artifact_requests_preservation :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          fullArtifactPreserved := false } =
      CompressionAdmissionRoute.requestFullArtifactPreservation := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem missing_compression_manifest_requests_manifest :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          compressionManifestPresent := false } =
      CompressionAdmissionRoute.requestCompressionManifest := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem missing_use_envelope_requests_envelope :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          declaredUseEnvelopePresent := false } =
      CompressionAdmissionRoute.requestUseEnvelope := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem missing_access_pattern_requests_access_pattern :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          accessPatternDeclared := false } =
      CompressionAdmissionRoute.requestAccessPattern := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem unadmitted_state_blocks_compressed_use :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          admissionStateAllowsUse := false } =
      CompressionAdmissionRoute.blockUnadmittedState := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem missing_decoder_determinism_requests_record :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          decoderDeterminismRecordPresent := false } =
      CompressionAdmissionRoute.requestDecoderDeterminismRecord := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem exact_replay_without_readiness_blocks_use :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          exactReplayReady := false } =
      CompressionAdmissionRoute.blockExactReplayWithoutReadiness := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem failed_required_probe_with_fallback_routes_to_fallback :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          taskProbePassed := false } =
      CompressionAdmissionRoute.routeToFallback := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem failed_required_probe_without_fallback_requests_artifact :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          taskProbePassed := false
          fallbackArtifactPresent := false } =
      CompressionAdmissionRoute.requestFallbackArtifact := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem missing_residual_metadata_requests_residual_record :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          residualMetadataPresent := false } =
      CompressionAdmissionRoute.requestResidualMetadata := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem missing_utility_evidence_requests_evidence :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          utilityEvidencePresent := false } =
      CompressionAdmissionRoute.requestUtilityEvidence := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem promotion_request_without_transition_requests_transition :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          supportPromotionRequested := true
          evidenceTransitionPresent := false } =
      CompressionAdmissionRoute.requestEvidenceTransition := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem compressed_use_without_nonclaim_boundary_preserves_boundary :
    CompressionAdmissionRouteFor
        { completeCompressionAdmissionReview with
          nonClaimBoundaryPresent := false } =
      CompressionAdmissionRoute.preserveNonClaimBoundary := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

theorem complete_compression_admission_allows_compressed_artifact :
    CompressionAdmissionRouteFor completeCompressionAdmissionReview =
      CompressionAdmissionRoute.admitCompressedArtifact := by
  simp [CompressionAdmissionRouteFor, completeCompressionAdmissionReview]

end AsiStackProofs.ArtifactCompression

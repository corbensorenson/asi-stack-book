namespace AsiStackProofs.CompactGenerativeSystems

structure CompactGenerativeRecord where
  unresolvedObligations : Bool
  residualRecordsPresent : Bool
  lossyRepresentation : Bool
  markedExact : Bool
  verificationEvidencePresent : Bool
deriving DecidableEq, Repr

def ResidualHonestyValid (record : CompactGenerativeRecord) : Prop :=
  record.unresolvedObligations = true -> record.residualRecordsPresent = true

theorem unresolved_obligations_require_residual_records
    {record : CompactGenerativeRecord} :
    ResidualHonestyValid record ->
    record.unresolvedObligations = true ->
    record.residualRecordsPresent = true := by
  intro valid unresolved
  exact valid unresolved

theorem unresolved_obligations_without_residual_records_rejected
    {record : CompactGenerativeRecord} :
    record.unresolvedObligations = true ->
    record.residualRecordsPresent = false ->
    ¬ ResidualHonestyValid record := by
  intro unresolved missingResidual valid
  have residual := valid unresolved
  rw [missingResidual] at residual
  cases residual

def ExactnessClaimValid (record : CompactGenerativeRecord) : Prop :=
  record.lossyRepresentation = true ->
    record.verificationEvidencePresent = false ->
      record.markedExact = false

theorem lossy_representation_without_verification_cannot_be_marked_exact
    {record : CompactGenerativeRecord} :
    ExactnessClaimValid record ->
    record.lossyRepresentation = true ->
    record.verificationEvidencePresent = false ->
    record.markedExact = false := by
  intro valid lossy missingEvidence
  exact valid lossy missingEvidence

theorem lossy_unverified_representation_marked_exact_rejected
    {record : CompactGenerativeRecord} :
    record.lossyRepresentation = true ->
    record.verificationEvidencePresent = false ->
    record.markedExact = true ->
    ¬ ExactnessClaimValid record := by
  intro lossy missingEvidence exactMarked valid
  have notExact := valid lossy missingEvidence
  rw [exactMarked] at notExact
  cases notExact

inductive CompactAdmissionRoute where
  | requestSourceArtifact
  | requestCompressionBoundary
  | requestResidualRecord
  | blockLossyExactnessOverclaim
  | requestReconstructionEvidence
  | requestFallbackPath
  | requestVerifierCost
  | requestSemanticProvenance
  | requestMigrationRecord
  | requestEvidenceTransition
  | preserveNonClaimBoundary
  | admitCompactRepresentation
deriving DecidableEq, Repr

structure CompactAdmissionReview where
  sourceArtifactPresent : Bool
  compressionBoundaryDeclared : Bool
  residualRecordPresent : Bool
  lossyRepresentation : Bool
  markedExact : Bool
  verificationEvidencePresent : Bool
  reconstructionEvidencePresent : Bool
  fallbackPathPresent : Bool
  verifierCostRecorded : Bool
  semanticNodeGrounded : Bool
  semanticProvenancePresent : Bool
  hierarchyChanged : Bool
  migrationRecordPresent : Bool
  supportPromotionRequested : Bool
  evidenceTransitionPresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def CompactAdmissionRouteFor
    (review : CompactAdmissionReview) :
    CompactAdmissionRoute :=
  if review.sourceArtifactPresent = false then
    CompactAdmissionRoute.requestSourceArtifact
  else if review.compressionBoundaryDeclared = false then
    CompactAdmissionRoute.requestCompressionBoundary
  else if review.residualRecordPresent = false then
    CompactAdmissionRoute.requestResidualRecord
  else if review.lossyRepresentation = true ∧
      review.markedExact = true ∧
        review.verificationEvidencePresent = false then
    CompactAdmissionRoute.blockLossyExactnessOverclaim
  else if review.reconstructionEvidencePresent = false then
    CompactAdmissionRoute.requestReconstructionEvidence
  else if review.fallbackPathPresent = false then
    CompactAdmissionRoute.requestFallbackPath
  else if review.verifierCostRecorded = false then
    CompactAdmissionRoute.requestVerifierCost
  else if review.semanticNodeGrounded = true ∧
      review.semanticProvenancePresent = false then
    CompactAdmissionRoute.requestSemanticProvenance
  else if review.hierarchyChanged = true ∧
      review.migrationRecordPresent = false then
    CompactAdmissionRoute.requestMigrationRecord
  else if review.supportPromotionRequested = true ∧
      review.evidenceTransitionPresent = false then
    CompactAdmissionRoute.requestEvidenceTransition
  else if review.nonClaimBoundaryPresent = false then
    CompactAdmissionRoute.preserveNonClaimBoundary
  else
    CompactAdmissionRoute.admitCompactRepresentation

def completeCompactAdmissionReview : CompactAdmissionReview where
  sourceArtifactPresent := true
  compressionBoundaryDeclared := true
  residualRecordPresent := true
  lossyRepresentation := false
  markedExact := false
  verificationEvidencePresent := true
  reconstructionEvidencePresent := true
  fallbackPathPresent := true
  verifierCostRecorded := true
  semanticNodeGrounded := true
  semanticProvenancePresent := true
  hierarchyChanged := true
  migrationRecordPresent := true
  supportPromotionRequested := false
  evidenceTransitionPresent := true
  nonClaimBoundaryPresent := true

theorem missing_source_artifact_requests_source :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          sourceArtifactPresent := false } =
      CompactAdmissionRoute.requestSourceArtifact := by
  simp [CompactAdmissionRouteFor]

theorem missing_compression_boundary_requests_boundary :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          compressionBoundaryDeclared := false } =
      CompactAdmissionRoute.requestCompressionBoundary := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem missing_residual_record_requests_residual :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          residualRecordPresent := false } =
      CompactAdmissionRoute.requestResidualRecord := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem lossy_exact_claim_without_verification_blocks_admission :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          lossyRepresentation := true
          markedExact := true
          verificationEvidencePresent := false } =
      CompactAdmissionRoute.blockLossyExactnessOverclaim := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem missing_reconstruction_evidence_requests_evidence :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          reconstructionEvidencePresent := false } =
      CompactAdmissionRoute.requestReconstructionEvidence := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem missing_fallback_path_requests_fallback :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          fallbackPathPresent := false } =
      CompactAdmissionRoute.requestFallbackPath := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem missing_verifier_cost_requests_cost_record :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          verifierCostRecorded := false } =
      CompactAdmissionRoute.requestVerifierCost := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem grounded_semantic_node_without_provenance_requests_provenance :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          semanticProvenancePresent := false } =
      CompactAdmissionRoute.requestSemanticProvenance := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem hierarchy_change_without_migration_requests_migration :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          migrationRecordPresent := false } =
      CompactAdmissionRoute.requestMigrationRecord := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem support_promotion_without_transition_requests_transition :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          supportPromotionRequested := true
          evidenceTransitionPresent := false } =
      CompactAdmissionRoute.requestEvidenceTransition := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem missing_nonclaim_boundary_preserves_boundary :
    CompactAdmissionRouteFor
        { completeCompactAdmissionReview with
          nonClaimBoundaryPresent := false } =
      CompactAdmissionRoute.preserveNonClaimBoundary := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

theorem complete_compact_admission_allows_representation :
    CompactAdmissionRouteFor completeCompactAdmissionReview =
      CompactAdmissionRoute.admitCompactRepresentation := by
  simp [CompactAdmissionRouteFor, completeCompactAdmissionReview]

inductive CompactGVRFixtureReceipt where
  | literalBaseline
  | repeatGeneratorPlusRepair
  | lossySummaryMarkedExact
  | negativeRateNoFallback
  | boundedSearchOverrun
deriving DecidableEq, Repr

structure CompactGVRFixtureAssessment where
  serializedBytes : Nat
  exactReconstruction : Bool
  fallbackPresent : Bool
  residualVisible : Bool
  searchWithinBound : Bool
  eligible : Bool
deriving DecidableEq, Repr

def compactGVRFixtureAssessment :
    CompactGVRFixtureReceipt -> CompactGVRFixtureAssessment
  | .literalBaseline =>
      { serializedBytes := 368
        exactReconstruction := true
        fallbackPresent := true
        residualVisible := true
        searchWithinBound := true
        eligible := false }
  | .repeatGeneratorPlusRepair =>
      { serializedBytes := 78
        exactReconstruction := true
        fallbackPresent := true
        residualVisible := true
        searchWithinBound := true
        eligible := true }
  | .lossySummaryMarkedExact =>
      { serializedBytes := 55
        exactReconstruction := false
        fallbackPresent := true
        residualVisible := true
        searchWithinBound := true
        eligible := false }
  | .negativeRateNoFallback =>
      { serializedBytes := 485
        exactReconstruction := true
        fallbackPresent := false
        residualVisible := true
        searchWithinBound := true
        eligible := false }
  | .boundedSearchOverrun =>
      { serializedBytes := 72
        exactReconstruction := false
        fallbackPresent := true
        residualVisible := true
        searchWithinBound := false
        eligible := false }

def CompactGVRFixtureSelected : CompactGVRFixtureReceipt :=
  .repeatGeneratorPlusRepair

theorem compact_gvr_fixture_selected_is_eligible :
    (compactGVRFixtureAssessment CompactGVRFixtureSelected).eligible = true := by
  rfl

theorem lossy_marked_exact_fixture_rejected :
    (compactGVRFixtureAssessment
      CompactGVRFixtureReceipt.lossySummaryMarkedExact).eligible = false := by
  rfl

theorem negative_rate_without_fallback_fixture_rejected :
    (compactGVRFixtureAssessment
      CompactGVRFixtureReceipt.negativeRateNoFallback).eligible = false := by
  rfl

theorem bounded_search_overrun_fixture_rejected :
    (compactGVRFixtureAssessment
      CompactGVRFixtureReceipt.boundedSearchOverrun).eligible = false := by
  rfl

theorem compact_gvr_fixture_selected_beats_literal_baseline :
    (compactGVRFixtureAssessment CompactGVRFixtureSelected).serializedBytes <
      (compactGVRFixtureAssessment
        CompactGVRFixtureReceipt.literalBaseline).serializedBytes := by
  decide

structure ResidualConservationFixtureSummary where
  acceptedResidualRecorded : Bool
  deferredResidualOwned : Bool
  dischargedResidualHasReceipt : Bool
  hiddenResidualRejected : Bool
  erasedResidualRejected : Bool
  unownedMovedResidualRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def residualConservationFixtureSummary :
    ResidualConservationFixtureSummary where
  acceptedResidualRecorded := true
  deferredResidualOwned := true
  dischargedResidualHasReceipt := true
  hiddenResidualRejected := true
  erasedResidualRejected := true
  unownedMovedResidualRejected := true
  supportStateEffectNone := true
  nonClaimBoundary := true

def ResidualConservationFixtureValid
    (summary : ResidualConservationFixtureSummary) : Prop :=
  summary.acceptedResidualRecorded = true ∧
    summary.deferredResidualOwned = true ∧
    summary.dischargedResidualHasReceipt = true ∧
    summary.hiddenResidualRejected = true ∧
    summary.erasedResidualRejected = true ∧
    summary.unownedMovedResidualRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

theorem residual_honesty_conservation_fixture_bridge :
    ResidualConservationFixtureValid
      residualConservationFixtureSummary := by
  unfold ResidualConservationFixtureValid
  unfold residualConservationFixtureSummary
  simp

end AsiStackProofs.CompactGenerativeSystems

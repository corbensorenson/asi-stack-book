namespace AsiStackProofs.ArtifactGraph

inductive ProvenanceStatus where
  | complete
  | incomplete
  | missing
  | blocked
deriving DecidableEq, Repr

structure ArtifactRecord where
  produced : Bool
  parentJobPresent : Bool
  sourceRefsPresent : Bool
  contextRefsPresent : Bool
  provenanceStatus : ProvenanceStatus
deriving DecidableEq, Repr

def ProducedArtifactTraceable (record : ArtifactRecord) : Prop :=
  record.produced = true ->
    record.parentJobPresent = true ∧
      record.sourceRefsPresent = true ∧
        record.contextRefsPresent = true

theorem produced_artifact_missing_trace_refs_rejected
    {record : ArtifactRecord} :
    record.produced = true ->
      (record.parentJobPresent = false ∨
        record.sourceRefsPresent = false ∨
          record.contextRefsPresent = false) ->
        ¬ ProducedArtifactTraceable record := by
  intro produced missingRef traceable
  have required := traceable produced
  cases missingRef with
  | inl parentMissing =>
      rw [parentMissing] at required
      cases required.1
  | inr rest =>
      cases rest with
      | inl sourceMissing =>
          rw [sourceMissing] at required
          cases required.2.1
      | inr contextMissing =>
          rw [contextMissing] at required
          cases required.2.2

def RequiredProvenanceComplete (record : ArtifactRecord) : Prop :=
  record.parentJobPresent = true ∧
    record.sourceRefsPresent = true ∧
      record.contextRefsPresent = true ∧
        record.provenanceStatus = ProvenanceStatus.complete

def PromotedClaimSupportAllowed (record : ArtifactRecord) : Prop :=
  record.produced = true ∧ RequiredProvenanceComplete record

theorem missing_required_provenance_blocks_promoted_claim_support
    {record : ArtifactRecord} :
    (record.parentJobPresent = false ∨
      record.sourceRefsPresent = false ∨
        record.contextRefsPresent = false ∨
          record.provenanceStatus = ProvenanceStatus.missing) ->
    ¬ PromotedClaimSupportAllowed record := by
  intro missing promoted
  unfold PromotedClaimSupportAllowed RequiredProvenanceComplete at promoted
  cases missing with
  | inl parentMissing =>
      rw [parentMissing] at promoted
      cases promoted.2.1
  | inr rest =>
      cases rest with
      | inl sourceMissing =>
          rw [sourceMissing] at promoted
          cases promoted.2.2.1
      | inr rest =>
          cases rest with
          | inl contextMissing =>
              rw [contextMissing] at promoted
              cases promoted.2.2.2.1
          | inr statusMissing =>
              rw [statusMissing] at promoted
              cases promoted.2.2.2.2

theorem incomplete_or_blocked_provenance_blocks_promoted_claim_support
    {record : ArtifactRecord} :
    (record.provenanceStatus = ProvenanceStatus.incomplete ∨
      record.provenanceStatus = ProvenanceStatus.blocked) ->
    ¬ PromotedClaimSupportAllowed record := by
  intro badStatus promoted
  unfold PromotedClaimSupportAllowed RequiredProvenanceComplete at promoted
  cases badStatus with
  | inl incomplete =>
      rw [incomplete] at promoted
      cases promoted.2.2.2.2
  | inr blocked =>
      rw [blocked] at promoted
      cases promoted.2.2.2.2

inductive ReplayGrade where
  | blocked
  | unattempted
  | partialReplay
  | semanticReplay
  | byteExact
deriving DecidableEq, Repr

def ReplayGrade.rank : ReplayGrade -> Nat
  | .blocked => 0
  | .unattempted => 0
  | .partialReplay => 1
  | .semanticReplay => 2
  | .byteExact => 3

structure ReplayGradeReview where
  observed : ReplayGrade
  required : ReplayGrade
deriving DecidableEq, Repr

def ReplayGradeSufficient (review : ReplayGradeReview) : Prop :=
  review.required.rank <= review.observed.rank

theorem replay_grade_below_requirement_blocks_sufficiency
    {review : ReplayGradeReview} :
    review.observed.rank < review.required.rank ->
      ¬ ReplayGradeSufficient review := by
  intro belowRequired sufficient
  exact (Nat.not_lt_of_ge sufficient) belowRequired

inductive ArtifactGraphRoute where
  | rejectMissingArtifact
  | requireParentJob
  | requireSourceRefs
  | requireContextRefs
  | requireContextTransactionRefs
  | requireSemanticCertificateRefs
  | requireToolRefs
  | requireClaimLinks
  | requireTestLinks
  | requireAuditEvents
  | requireReplayMetadata
  | requireReplayGradeUpgrade
  | requireReplayLimits
  | requireEvidenceGate
  | blockStaleCertificate
  | blockPromotion
  | requireNonClaimBoundary
  | admitArtifact
deriving DecidableEq, Repr

structure ArtifactGraphReview where
  artifactProduced : Bool
  parentJobPresent : Bool
  sourceRefsPresent : Bool
  contextRefsPresent : Bool
  contextTransactionRefsPresent : Bool
  semanticCertificateRefsPresent : Bool
  toolRefsPresent : Bool
  claimRefsPresent : Bool
  testRefsPresent : Bool
  auditEventsPresent : Bool
  replayMetadataPresent : Bool
  replayGradeSufficient : Bool
  replayLimitsDeclared : Bool
  evidenceGateDeclared : Bool
  staleCertificatePresent : Bool
  promotionRequested : Bool
  promotionAllowed : Bool
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def ArtifactGraphRouteFor
    (review : ArtifactGraphReview) : ArtifactGraphRoute :=
  if review.artifactProduced = false then
    ArtifactGraphRoute.rejectMissingArtifact
  else if review.parentJobPresent = false then
    ArtifactGraphRoute.requireParentJob
  else if review.sourceRefsPresent = false then
    ArtifactGraphRoute.requireSourceRefs
  else if review.contextRefsPresent = false then
    ArtifactGraphRoute.requireContextRefs
  else if review.contextTransactionRefsPresent = false then
    ArtifactGraphRoute.requireContextTransactionRefs
  else if review.semanticCertificateRefsPresent = false then
    ArtifactGraphRoute.requireSemanticCertificateRefs
  else if review.toolRefsPresent = false then
    ArtifactGraphRoute.requireToolRefs
  else if review.claimRefsPresent = false then
    ArtifactGraphRoute.requireClaimLinks
  else if review.testRefsPresent = false then
    ArtifactGraphRoute.requireTestLinks
  else if review.auditEventsPresent = false then
    ArtifactGraphRoute.requireAuditEvents
  else if review.replayMetadataPresent = false then
    ArtifactGraphRoute.requireReplayMetadata
  else if review.replayGradeSufficient = false then
    ArtifactGraphRoute.requireReplayGradeUpgrade
  else if review.replayLimitsDeclared = false then
    ArtifactGraphRoute.requireReplayLimits
  else if review.evidenceGateDeclared = false then
    ArtifactGraphRoute.requireEvidenceGate
  else if review.staleCertificatePresent = true then
    ArtifactGraphRoute.blockStaleCertificate
  else if review.promotionRequested = true ∧
      review.promotionAllowed = false then
    ArtifactGraphRoute.blockPromotion
  else if review.nonClaimsPresent = false then
    ArtifactGraphRoute.requireNonClaimBoundary
  else
    ArtifactGraphRoute.admitArtifact

theorem missing_artifact_rejects_artifact_graph_route
    {review : ArtifactGraphReview} :
    review.artifactProduced = false ->
      ArtifactGraphRouteFor review =
        ArtifactGraphRoute.rejectMissingArtifact := by
  intro missingArtifact
  unfold ArtifactGraphRouteFor
  simp [missingArtifact]

theorem produced_artifact_without_parent_requires_parent_job
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = false ->
        ArtifactGraphRouteFor review =
          ArtifactGraphRoute.requireParentJob := by
  intro produced missingParent
  unfold ArtifactGraphRouteFor
  simp [produced, missingParent]

theorem produced_artifact_without_source_refs_requires_source_refs
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = false ->
          ArtifactGraphRouteFor review =
            ArtifactGraphRoute.requireSourceRefs := by
  intro produced parentPresent missingSources
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, missingSources]

theorem produced_artifact_without_context_refs_requires_context_refs
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = false ->
            ArtifactGraphRouteFor review =
              ArtifactGraphRoute.requireContextRefs := by
  intro produced parentPresent sourcesPresent missingContext
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, missingContext]

theorem missing_context_transaction_refs_requires_transaction_refs
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = false ->
              ArtifactGraphRouteFor review =
                ArtifactGraphRoute.requireContextTransactionRefs := by
  intro produced parentPresent sourcesPresent contextPresent
    missingTransactions
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    missingTransactions]

theorem missing_semantic_certificate_refs_requires_certificate_refs
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = false ->
                ArtifactGraphRouteFor review =
                  ArtifactGraphRoute.requireSemanticCertificateRefs := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    missingCertificates
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, missingCertificates]

theorem missing_tool_refs_require_tool_refs
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = false ->
                  ArtifactGraphRouteFor review =
                    ArtifactGraphRoute.requireToolRefs := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent missingTools
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, missingTools]

theorem missing_claim_links_requires_claim_links
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = false ->
                    ArtifactGraphRouteFor review =
                      ArtifactGraphRoute.requireClaimLinks := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent missingClaims
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, missingClaims]

theorem missing_test_links_requires_test_links
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = false ->
                      ArtifactGraphRouteFor review =
                        ArtifactGraphRoute.requireTestLinks := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent missingTests
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    missingTests]

theorem missing_audit_events_require_audit_events
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = false ->
                        ArtifactGraphRouteFor review =
                          ArtifactGraphRoute.requireAuditEvents := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent missingAudit
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, missingAudit]

theorem missing_replay_metadata_requires_metadata
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = false ->
                          ArtifactGraphRouteFor review =
                            ArtifactGraphRoute.requireReplayMetadata := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    missingReplayMetadata
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, missingReplayMetadata]

theorem insufficient_replay_grade_requires_upgrade
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = true ->
                          review.replayGradeSufficient = false ->
                            ArtifactGraphRouteFor review =
                              ArtifactGraphRoute.requireReplayGradeUpgrade := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    replayMetadata insufficientReplay
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, replayMetadata, insufficientReplay]

theorem missing_replay_limits_require_replay_limits
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = true ->
                          review.replayGradeSufficient = true ->
                            review.replayLimitsDeclared = false ->
                              ArtifactGraphRouteFor review =
                                ArtifactGraphRoute.requireReplayLimits := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    replayMetadata replaySufficient missingReplayLimits
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, replayMetadata, replaySufficient,
    missingReplayLimits]

theorem missing_evidence_gate_requires_evidence_gate
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = true ->
                          review.replayGradeSufficient = true ->
                            review.replayLimitsDeclared = true ->
                              review.evidenceGateDeclared = false ->
                                ArtifactGraphRouteFor review =
                                  ArtifactGraphRoute.requireEvidenceGate := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    replayMetadata replaySufficient replayLimits missingGate
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, replayMetadata, replaySufficient,
    replayLimits, missingGate]

theorem stale_certificate_blocks_artifact_reuse
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = true ->
                          review.replayGradeSufficient = true ->
                            review.replayLimitsDeclared = true ->
                              review.evidenceGateDeclared = true ->
                                review.staleCertificatePresent = true ->
                                  ArtifactGraphRouteFor review =
                                    ArtifactGraphRoute.blockStaleCertificate := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    replayMetadata replaySufficient replayLimits evidenceGate staleCertificate
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, replayMetadata, replaySufficient,
    replayLimits, evidenceGate, staleCertificate]

theorem promotion_without_permission_blocks_artifact_promotion
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = true ->
                          review.replayGradeSufficient = true ->
                            review.replayLimitsDeclared = true ->
                              review.evidenceGateDeclared = true ->
                                review.staleCertificatePresent = false ->
                                  review.promotionRequested = true ->
                                    review.promotionAllowed = false ->
                                      ArtifactGraphRouteFor review =
                                        ArtifactGraphRoute.blockPromotion := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    replayMetadata replaySufficient replayLimits evidenceGate noStaleCertificate
    promotionRequested promotionBlocked
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, replayMetadata, replaySufficient,
    replayLimits, evidenceGate, noStaleCertificate, promotionRequested,
    promotionBlocked]

theorem missing_non_claim_boundary_requires_boundary
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = true ->
                          review.replayGradeSufficient = true ->
                            review.replayLimitsDeclared = true ->
                              review.evidenceGateDeclared = true ->
                                review.staleCertificatePresent = false ->
                                  review.promotionRequested = false ->
                                    review.nonClaimsPresent = false ->
                                      ArtifactGraphRouteFor review =
                                        ArtifactGraphRoute.requireNonClaimBoundary := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    replayMetadata replaySufficient replayLimits evidenceGate noStaleCertificate
    noPromotion missingNonClaims
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, replayMetadata, replaySufficient,
    replayLimits, evidenceGate, noStaleCertificate, noPromotion, missingNonClaims]

theorem complete_artifact_graph_route_admits_artifact
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = true ->
                          review.replayGradeSufficient = true ->
                            review.replayLimitsDeclared = true ->
                              review.evidenceGateDeclared = true ->
                                review.staleCertificatePresent = false ->
                                  review.promotionRequested = false ->
                                    review.nonClaimsPresent = true ->
                                      ArtifactGraphRouteFor review =
                                        ArtifactGraphRoute.admitArtifact := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    replayMetadata replaySufficient replayLimits evidenceGate noStaleCertificate
    noPromotion nonClaims
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, replayMetadata, replaySufficient,
    replayLimits, evidenceGate, noStaleCertificate, noPromotion, nonClaims]

theorem complete_promoted_artifact_route_admits_artifact
    {review : ArtifactGraphReview} :
    review.artifactProduced = true ->
      review.parentJobPresent = true ->
        review.sourceRefsPresent = true ->
          review.contextRefsPresent = true ->
            review.contextTransactionRefsPresent = true ->
              review.semanticCertificateRefsPresent = true ->
                review.toolRefsPresent = true ->
                  review.claimRefsPresent = true ->
                    review.testRefsPresent = true ->
                      review.auditEventsPresent = true ->
                        review.replayMetadataPresent = true ->
                          review.replayGradeSufficient = true ->
                            review.replayLimitsDeclared = true ->
                              review.evidenceGateDeclared = true ->
                                review.staleCertificatePresent = false ->
                                  review.promotionRequested = true ->
                                    review.promotionAllowed = true ->
                                      review.nonClaimsPresent = true ->
                                        ArtifactGraphRouteFor review =
                                          ArtifactGraphRoute.admitArtifact := by
  intro produced parentPresent sourcesPresent contextPresent transactionsPresent
    certificatesPresent toolsPresent claimsPresent testsPresent auditPresent
    replayMetadata replaySufficient replayLimits evidenceGate noStaleCertificate
    promotionRequested promotionAllowed nonClaims
  unfold ArtifactGraphRouteFor
  simp [produced, parentPresent, sourcesPresent, contextPresent,
    transactionsPresent, certificatesPresent, toolsPresent, claimsPresent,
    testsPresent, auditPresent, replayMetadata, replaySufficient,
    replayLimits, evidenceGate, noStaleCertificate, promotionRequested,
    promotionAllowed, nonClaims]

def ReplayGrade.requiresReplayEvidenceChecks : ReplayGrade -> Bool
  | .semanticReplay => true
  | .byteExact => true
  | .blocked => false
  | .unattempted => false
  | .partialReplay => false

inductive ArtifactReplayPacketRoute where
  | requireParentJobMatch
  | requireJobOutputReference
  | requireContextTransactionReference
  | requireSemanticCertificateReference
  | requireCertificateTransactionLink
  | requireCertificateArtifactLink
  | requireSourceCoverage
  | requireAuditChain
  | requireReplayGradeMatch
  | requireEnvironmentConfirmation
  | requireObservedArtifact
  | requireCompleteProvenance
  | requireReplayCheckedAudit
  | blockIncompleteReplayPromotion
  | requireCommittedTransaction
  | requireReplayValidatedTransaction
  | requireVerifiedCertificate
  | requireActiveCertificate
  | requireReusableJobLifecycle
  | requireNonClaimBoundary
  | recordOnlyBlocksPromotion
  | admitBoundedReview
deriving DecidableEq, Repr

structure ArtifactReplayPacketReview where
  parentJobMatches : Bool
  jobOutputsArtifact : Bool
  transactionReferencedByArtifact : Bool
  certificateReferencedByArtifact : Bool
  certificateReferencesTransaction : Bool
  certificateReferencesArtifact : Bool
  sourceRefsCovered : Bool
  auditChainComplete : Bool
  replayGradeMatchesArtifact : Bool
  replayGrade : ReplayGrade
  environmentConfirmed : Bool
  observedArtifactPresent : Bool
  provenanceComplete : Bool
  replayCheckedInAudit : Bool
  promotionRequested : Bool
  supportReviewRequested : Bool
  transactionCommitted : Bool
  transactionReplayValidated : Bool
  certificateVerified : Bool
  certificateActive : Bool
  jobReusableLifecycle : Bool
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def ArtifactReplayPacketRouteFor
    (review : ArtifactReplayPacketReview) : ArtifactReplayPacketRoute :=
  if review.parentJobMatches = false then
    ArtifactReplayPacketRoute.requireParentJobMatch
  else if review.jobOutputsArtifact = false then
    ArtifactReplayPacketRoute.requireJobOutputReference
  else if review.transactionReferencedByArtifact = false then
    ArtifactReplayPacketRoute.requireContextTransactionReference
  else if review.certificateReferencedByArtifact = false then
    ArtifactReplayPacketRoute.requireSemanticCertificateReference
  else if review.certificateReferencesTransaction = false then
    ArtifactReplayPacketRoute.requireCertificateTransactionLink
  else if review.certificateReferencesArtifact = false then
    ArtifactReplayPacketRoute.requireCertificateArtifactLink
  else if review.sourceRefsCovered = false then
    ArtifactReplayPacketRoute.requireSourceCoverage
  else if review.auditChainComplete = false then
    ArtifactReplayPacketRoute.requireAuditChain
  else if review.replayGradeMatchesArtifact = false then
    ArtifactReplayPacketRoute.requireReplayGradeMatch
  else if review.replayGrade.requiresReplayEvidenceChecks = true then
    if review.environmentConfirmed = false then
      ArtifactReplayPacketRoute.requireEnvironmentConfirmation
    else if review.observedArtifactPresent = false then
      ArtifactReplayPacketRoute.requireObservedArtifact
    else if review.provenanceComplete = false then
      ArtifactReplayPacketRoute.requireCompleteProvenance
    else if review.replayCheckedInAudit = false then
      ArtifactReplayPacketRoute.requireReplayCheckedAudit
    else if review.supportReviewRequested = true ∨
        review.promotionRequested = true then
      if review.transactionCommitted = false then
        ArtifactReplayPacketRoute.requireCommittedTransaction
      else if review.transactionReplayValidated = false then
        ArtifactReplayPacketRoute.requireReplayValidatedTransaction
      else if review.certificateVerified = false then
        ArtifactReplayPacketRoute.requireVerifiedCertificate
      else if review.certificateActive = false then
        ArtifactReplayPacketRoute.requireActiveCertificate
      else if review.jobReusableLifecycle = false then
        ArtifactReplayPacketRoute.requireReusableJobLifecycle
      else if review.nonClaimsPresent = false then
        ArtifactReplayPacketRoute.requireNonClaimBoundary
      else
        ArtifactReplayPacketRoute.admitBoundedReview
    else if review.certificateActive = false then
      ArtifactReplayPacketRoute.requireActiveCertificate
    else if review.jobReusableLifecycle = false then
      ArtifactReplayPacketRoute.requireReusableJobLifecycle
    else if review.nonClaimsPresent = false then
      ArtifactReplayPacketRoute.requireNonClaimBoundary
    else
      ArtifactReplayPacketRoute.admitBoundedReview
  else if review.supportReviewRequested = true ∨
      review.promotionRequested = true then
    ArtifactReplayPacketRoute.blockIncompleteReplayPromotion
  else if review.certificateActive = false then
    ArtifactReplayPacketRoute.requireActiveCertificate
  else if review.jobReusableLifecycle = false then
    ArtifactReplayPacketRoute.requireReusableJobLifecycle
  else if review.nonClaimsPresent = false then
    ArtifactReplayPacketRoute.requireNonClaimBoundary
  else
    ArtifactReplayPacketRoute.recordOnlyBlocksPromotion

theorem replay_packet_parent_job_mismatch_requires_parent_match
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = false ->
      ArtifactReplayPacketRouteFor review =
        ArtifactReplayPacketRoute.requireParentJobMatch := by
  intro mismatch
  unfold ArtifactReplayPacketRouteFor
  simp [mismatch]

theorem replay_packet_missing_audit_chain_requires_audit_chain
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = true ->
      review.jobOutputsArtifact = true ->
        review.transactionReferencedByArtifact = true ->
          review.certificateReferencedByArtifact = true ->
            review.certificateReferencesTransaction = true ->
              review.certificateReferencesArtifact = true ->
                review.sourceRefsCovered = true ->
                  review.auditChainComplete = false ->
                    ArtifactReplayPacketRouteFor review =
                      ArtifactReplayPacketRoute.requireAuditChain := by
  intro parentMatch jobOutput transactionRef certificateRef certTransaction
    certArtifact sourceCovered missingAudit
  unfold ArtifactReplayPacketRouteFor
  simp [parentMatch, jobOutput, transactionRef, certificateRef,
    certTransaction, certArtifact, sourceCovered, missingAudit]

theorem byte_exact_replay_missing_observed_artifact_requires_observation
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = true ->
      review.jobOutputsArtifact = true ->
        review.transactionReferencedByArtifact = true ->
          review.certificateReferencedByArtifact = true ->
            review.certificateReferencesTransaction = true ->
              review.certificateReferencesArtifact = true ->
                review.sourceRefsCovered = true ->
                  review.auditChainComplete = true ->
                    review.replayGradeMatchesArtifact = true ->
                      review.replayGrade = ReplayGrade.byteExact ->
                        review.environmentConfirmed = true ->
                          review.observedArtifactPresent = false ->
                            ArtifactReplayPacketRouteFor review =
                              ArtifactReplayPacketRoute.requireObservedArtifact := by
  intro parentMatch jobOutput transactionRef certificateRef certTransaction
    certArtifact sourceCovered auditComplete gradeMatches byteExact
    environmentConfirmed missingObservation
  unfold ArtifactReplayPacketRouteFor
  simp [parentMatch, jobOutput, transactionRef, certificateRef,
    certTransaction, certArtifact, sourceCovered, auditComplete, gradeMatches,
    byteExact, environmentConfirmed, missingObservation,
    ReplayGrade.requiresReplayEvidenceChecks]

theorem stale_certificate_in_replay_packet_requires_active_certificate
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = true ->
      review.jobOutputsArtifact = true ->
        review.transactionReferencedByArtifact = true ->
          review.certificateReferencedByArtifact = true ->
            review.certificateReferencesTransaction = true ->
              review.certificateReferencesArtifact = true ->
                review.sourceRefsCovered = true ->
                  review.auditChainComplete = true ->
                    review.replayGradeMatchesArtifact = true ->
                      review.replayGrade = ReplayGrade.byteExact ->
                        review.environmentConfirmed = true ->
                          review.observedArtifactPresent = true ->
                            review.provenanceComplete = true ->
                              review.replayCheckedInAudit = true ->
                                review.supportReviewRequested = false ->
                                  review.promotionRequested = false ->
                                    review.certificateActive = false ->
                                      ArtifactReplayPacketRouteFor review =
                                        ArtifactReplayPacketRoute.requireActiveCertificate := by
  intro parentMatch jobOutput transactionRef certificateRef certTransaction
    certArtifact sourceCovered auditComplete gradeMatches byteExact
    environmentConfirmed observed provenanceComplete replayChecked noSupportReview
    noPromotion staleCertificate
  unfold ArtifactReplayPacketRouteFor
  simp [parentMatch, jobOutput, transactionRef, certificateRef,
    certTransaction, certArtifact, sourceCovered, auditComplete, gradeMatches,
    byteExact, environmentConfirmed, observed, provenanceComplete,
    replayChecked, noSupportReview, noPromotion, staleCertificate,
    ReplayGrade.requiresReplayEvidenceChecks]

theorem support_review_without_replay_validated_transaction_requires_validation
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = true ->
      review.jobOutputsArtifact = true ->
        review.transactionReferencedByArtifact = true ->
          review.certificateReferencedByArtifact = true ->
            review.certificateReferencesTransaction = true ->
              review.certificateReferencesArtifact = true ->
                review.sourceRefsCovered = true ->
                  review.auditChainComplete = true ->
                    review.replayGradeMatchesArtifact = true ->
                      review.replayGrade = ReplayGrade.byteExact ->
                        review.environmentConfirmed = true ->
                          review.observedArtifactPresent = true ->
                            review.provenanceComplete = true ->
                              review.replayCheckedInAudit = true ->
                                review.supportReviewRequested = true ->
                                  review.transactionCommitted = true ->
                                    review.transactionReplayValidated = false ->
                                      ArtifactReplayPacketRouteFor review =
                                        ArtifactReplayPacketRoute.requireReplayValidatedTransaction := by
  intro parentMatch jobOutput transactionRef certificateRef certTransaction
    certArtifact sourceCovered auditComplete gradeMatches byteExact
    environmentConfirmed observed provenanceComplete replayChecked
    supportReview transactionCommitted unvalidatedTransaction
  unfold ArtifactReplayPacketRouteFor
  simp [parentMatch, jobOutput, transactionRef, certificateRef,
    certTransaction, certArtifact, sourceCovered, auditComplete, gradeMatches,
    byteExact, environmentConfirmed, observed, provenanceComplete,
    replayChecked, supportReview, transactionCommitted, unvalidatedTransaction,
    ReplayGrade.requiresReplayEvidenceChecks]

theorem partial_replay_promotion_request_blocks_packet_promotion
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = true ->
      review.jobOutputsArtifact = true ->
        review.transactionReferencedByArtifact = true ->
          review.certificateReferencedByArtifact = true ->
            review.certificateReferencesTransaction = true ->
              review.certificateReferencesArtifact = true ->
                review.sourceRefsCovered = true ->
                  review.auditChainComplete = true ->
                    review.replayGradeMatchesArtifact = true ->
                      review.replayGrade = ReplayGrade.partialReplay ->
                        review.promotionRequested = true ->
                          ArtifactReplayPacketRouteFor review =
                            ArtifactReplayPacketRoute.blockIncompleteReplayPromotion := by
  intro parentMatch jobOutput transactionRef certificateRef certTransaction
    certArtifact sourceCovered auditComplete gradeMatches partialReplay
    promotionRequested
  unfold ArtifactReplayPacketRouteFor
  simp [parentMatch, jobOutput, transactionRef, certificateRef,
    certTransaction, certArtifact, sourceCovered, auditComplete, gradeMatches,
    partialReplay, promotionRequested,
    ReplayGrade.requiresReplayEvidenceChecks]

theorem partial_replay_record_only_blocks_promotion_without_rejecting_record
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = true ->
      review.jobOutputsArtifact = true ->
        review.transactionReferencedByArtifact = true ->
          review.certificateReferencedByArtifact = true ->
            review.certificateReferencesTransaction = true ->
              review.certificateReferencesArtifact = true ->
                review.sourceRefsCovered = true ->
                  review.auditChainComplete = true ->
                    review.replayGradeMatchesArtifact = true ->
                      review.replayGrade = ReplayGrade.partialReplay ->
                        review.supportReviewRequested = false ->
                          review.promotionRequested = false ->
                            review.certificateActive = true ->
                              review.jobReusableLifecycle = true ->
                                review.nonClaimsPresent = true ->
                                  ArtifactReplayPacketRouteFor review =
                                    ArtifactReplayPacketRoute.recordOnlyBlocksPromotion := by
  intro parentMatch jobOutput transactionRef certificateRef certTransaction
    certArtifact sourceCovered auditComplete gradeMatches partialReplay
    noSupportReview noPromotion activeCertificate reusableLifecycle nonClaims
  unfold ArtifactReplayPacketRouteFor
  simp [parentMatch, jobOutput, transactionRef, certificateRef,
    certTransaction, certArtifact, sourceCovered, auditComplete, gradeMatches,
    partialReplay, noSupportReview, noPromotion, activeCertificate,
    reusableLifecycle, nonClaims, ReplayGrade.requiresReplayEvidenceChecks]

theorem complete_byte_exact_replay_packet_admits_bounded_review
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = true ->
      review.jobOutputsArtifact = true ->
        review.transactionReferencedByArtifact = true ->
          review.certificateReferencedByArtifact = true ->
            review.certificateReferencesTransaction = true ->
              review.certificateReferencesArtifact = true ->
                review.sourceRefsCovered = true ->
                  review.auditChainComplete = true ->
                    review.replayGradeMatchesArtifact = true ->
                      review.replayGrade = ReplayGrade.byteExact ->
                        review.environmentConfirmed = true ->
                          review.observedArtifactPresent = true ->
                            review.provenanceComplete = true ->
                              review.replayCheckedInAudit = true ->
                                review.supportReviewRequested = false ->
                                  review.promotionRequested = false ->
                                    review.certificateActive = true ->
                                      review.jobReusableLifecycle = true ->
                                        review.nonClaimsPresent = true ->
                                          ArtifactReplayPacketRouteFor review =
                                            ArtifactReplayPacketRoute.admitBoundedReview := by
  intro parentMatch jobOutput transactionRef certificateRef certTransaction
    certArtifact sourceCovered auditComplete gradeMatches byteExact
    environmentConfirmed observed provenanceComplete replayChecked noSupportReview
    noPromotion activeCertificate reusableLifecycle nonClaims
  unfold ArtifactReplayPacketRouteFor
  simp [parentMatch, jobOutput, transactionRef, certificateRef,
    certTransaction, certArtifact, sourceCovered, auditComplete, gradeMatches,
    byteExact, environmentConfirmed, observed, provenanceComplete,
    replayChecked, noSupportReview, noPromotion, activeCertificate,
    reusableLifecycle, nonClaims, ReplayGrade.requiresReplayEvidenceChecks]

theorem complete_support_review_packet_admits_bounded_review
    {review : ArtifactReplayPacketReview} :
    review.parentJobMatches = true ->
      review.jobOutputsArtifact = true ->
        review.transactionReferencedByArtifact = true ->
          review.certificateReferencedByArtifact = true ->
            review.certificateReferencesTransaction = true ->
              review.certificateReferencesArtifact = true ->
                review.sourceRefsCovered = true ->
                  review.auditChainComplete = true ->
                    review.replayGradeMatchesArtifact = true ->
                      review.replayGrade = ReplayGrade.byteExact ->
                        review.environmentConfirmed = true ->
                          review.observedArtifactPresent = true ->
                            review.provenanceComplete = true ->
                              review.replayCheckedInAudit = true ->
                                review.supportReviewRequested = true ->
                                  review.transactionCommitted = true ->
                                    review.transactionReplayValidated = true ->
                                      review.certificateVerified = true ->
                                        review.certificateActive = true ->
                                          review.jobReusableLifecycle = true ->
                                            review.nonClaimsPresent = true ->
                                              ArtifactReplayPacketRouteFor review =
                                                ArtifactReplayPacketRoute.admitBoundedReview := by
  intro parentMatch jobOutput transactionRef certificateRef certTransaction
    certArtifact sourceCovered auditComplete gradeMatches byteExact
    environmentConfirmed observed provenanceComplete replayChecked supportReview
    transactionCommitted transactionValidated certificateVerified
    activeCertificate reusableLifecycle nonClaims
  unfold ArtifactReplayPacketRouteFor
  simp [parentMatch, jobOutput, transactionRef, certificateRef,
    certTransaction, certArtifact, sourceCovered, auditComplete, gradeMatches,
    byteExact, environmentConfirmed, observed, provenanceComplete,
    replayChecked, supportReview, transactionCommitted, transactionValidated,
    certificateVerified, activeCertificate, reusableLifecycle, nonClaims,
    ReplayGrade.requiresReplayEvidenceChecks]

inductive RecordRealitySequenceRoute where
  | rejectSupportStateEffect
  | requireNonClaimBoundary
  | blockStaleCertificate
  | blockIncompleteReplay
  | requireReplayValidatedTransaction
  | requireDigestVerification
  | requireIndependentCheck
  | eligibleForBoundedReview
deriving DecidableEq, Repr

structure RecordRealitySequenceEvent where
  replayGrade : ReplayGrade
  provenanceComplete : Bool
  certificateActive : Bool
  transactionReplayValidated : Bool
  artifactDigestVerified : Bool
  independentCheckPresent : Bool
  supportStateEffectNone : Bool
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def RecordRealitySequenceRouteFor
    (event : RecordRealitySequenceEvent) : RecordRealitySequenceRoute :=
  if event.supportStateEffectNone = false then
    RecordRealitySequenceRoute.rejectSupportStateEffect
  else if event.nonClaimsPresent = false then
    RecordRealitySequenceRoute.requireNonClaimBoundary
  else if event.certificateActive = false then
    RecordRealitySequenceRoute.blockStaleCertificate
  else if event.replayGrade.requiresReplayEvidenceChecks = false then
    RecordRealitySequenceRoute.blockIncompleteReplay
  else if event.provenanceComplete = false then
    RecordRealitySequenceRoute.blockIncompleteReplay
  else if event.transactionReplayValidated = false then
    RecordRealitySequenceRoute.requireReplayValidatedTransaction
  else if event.artifactDigestVerified = false then
    RecordRealitySequenceRoute.requireDigestVerification
  else if event.independentCheckPresent = false then
    RecordRealitySequenceRoute.requireIndependentCheck
  else
    RecordRealitySequenceRoute.eligibleForBoundedReview

theorem stale_certificate_sequence_event_blocks_bounded_review
    {event : RecordRealitySequenceEvent} :
    event.supportStateEffectNone = true ->
      event.nonClaimsPresent = true ->
        event.certificateActive = false ->
          RecordRealitySequenceRouteFor event =
            RecordRealitySequenceRoute.blockStaleCertificate := by
  intro supportEffect nonClaims staleCertificate
  unfold RecordRealitySequenceRouteFor
  simp [supportEffect, nonClaims, staleCertificate]

theorem incomplete_replay_sequence_event_blocks_bounded_review
    {event : RecordRealitySequenceEvent} :
    event.supportStateEffectNone = true ->
      event.nonClaimsPresent = true ->
        event.certificateActive = true ->
          event.replayGrade = ReplayGrade.partialReplay ->
            RecordRealitySequenceRouteFor event =
              RecordRealitySequenceRoute.blockIncompleteReplay := by
  intro supportEffect nonClaims activeCertificate partialReplay
  unfold RecordRealitySequenceRouteFor
  simp [supportEffect, nonClaims, activeCertificate, partialReplay,
    ReplayGrade.requiresReplayEvidenceChecks]

theorem fresh_byte_exact_sequence_event_restores_bounded_review
    {event : RecordRealitySequenceEvent} :
    event.supportStateEffectNone = true ->
      event.nonClaimsPresent = true ->
        event.certificateActive = true ->
          event.replayGrade = ReplayGrade.byteExact ->
            event.provenanceComplete = true ->
              event.transactionReplayValidated = true ->
                event.artifactDigestVerified = true ->
                  event.independentCheckPresent = true ->
                    RecordRealitySequenceRouteFor event =
                      RecordRealitySequenceRoute.eligibleForBoundedReview := by
  intro supportEffect nonClaims activeCertificate byteExact provenance
    transactionValidated digestVerified independentCheck
  unfold RecordRealitySequenceRouteFor
  simp [supportEffect, nonClaims, activeCertificate, byteExact, provenance,
    transactionValidated, digestVerified, independentCheck,
    ReplayGrade.requiresReplayEvidenceChecks]

structure RecordRealitySequenceSummary where
  validSequenceCount : Nat
  expectedInvalidControlCount : Nat
  invalidControlsRejected : Nat
  validEventCount : Nat
  staleCertificateBlocked : Bool
  incompleteReplayBlocked : Bool
  supportEffectRejected : Bool
  missingNonClaimRejected : Bool
  missingReplayValidatedTransactionRejected : Bool
  freshReplayRestoresAfterBlock : Bool
  validSequencesEndEligible : Bool
  supportStateEffectNone : Bool
  chapterCoreSupportEffectNone : Bool
  evidenceTransitionCreated : Bool
deriving DecidableEq, Repr

def artifactRecordRealitySequenceSummary :
    RecordRealitySequenceSummary where
  validSequenceCount := 1
  expectedInvalidControlCount := 4
  invalidControlsRejected := 4
  validEventCount := 4
  staleCertificateBlocked := true
  incompleteReplayBlocked := true
  supportEffectRejected := true
  missingNonClaimRejected := true
  missingReplayValidatedTransactionRejected := true
  freshReplayRestoresAfterBlock := true
  validSequencesEndEligible := true
  supportStateEffectNone := true
  chapterCoreSupportEffectNone := true
  evidenceTransitionCreated := false

def RecordRealitySequenceFixtureValid
    (summary : RecordRealitySequenceSummary) : Prop :=
  summary.validSequenceCount = 1 ∧
    summary.expectedInvalidControlCount = 4 ∧
    summary.invalidControlsRejected = 4 ∧
    summary.validEventCount = 4 ∧
    summary.staleCertificateBlocked = true ∧
    summary.incompleteReplayBlocked = true ∧
    summary.supportEffectRejected = true ∧
    summary.missingNonClaimRejected = true ∧
    summary.missingReplayValidatedTransactionRejected = true ∧
    summary.freshReplayRestoresAfterBlock = true ∧
    summary.validSequencesEndEligible = true ∧
    summary.supportStateEffectNone = true ∧
    summary.chapterCoreSupportEffectNone = true ∧
    summary.evidenceTransitionCreated = false

structure ReceiptFaithfulnessFixtureSummary where
  crossCheckedReceiptRecordAccepted : Bool
  attestationLimitedRecordOnlyAccepted : Bool
  trapDetectedBlockedReceiptAccepted : Bool
  shapeValidRealityFalseRejected : Bool
  trapReceiptNegativeControlRejected : Bool
  independentCrossCheckRequired : Bool
  attestationLimitsRecorded : Bool
  supportPromotionFromReceiptShapeRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def receiptFaithfulnessFixtureSummary :
    ReceiptFaithfulnessFixtureSummary where
  crossCheckedReceiptRecordAccepted := true
  attestationLimitedRecordOnlyAccepted := true
  trapDetectedBlockedReceiptAccepted := true
  shapeValidRealityFalseRejected := true
  trapReceiptNegativeControlRejected := true
  independentCrossCheckRequired := true
  attestationLimitsRecorded := true
  supportPromotionFromReceiptShapeRejected := true
  supportStateEffectNone := true
  nonClaimBoundary := true

def ReceiptFaithfulnessFixtureValid
    (summary : ReceiptFaithfulnessFixtureSummary) : Prop :=
  summary.crossCheckedReceiptRecordAccepted = true ∧
    summary.attestationLimitedRecordOnlyAccepted = true ∧
    summary.trapDetectedBlockedReceiptAccepted = true ∧
    summary.shapeValidRealityFalseRejected = true ∧
    summary.trapReceiptNegativeControlRejected = true ∧
    summary.independentCrossCheckRequired = true ∧
    summary.attestationLimitsRecorded = true ∧
    summary.supportPromotionFromReceiptShapeRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

structure ReceiptRepositoryAuditSummary where
  auditedReceiptCount : Nat
  acceptedReceiptCount : Nat
  digestCheckedReceiptCount : Nat
  externalFingerprintReceiptCount : Nat
  commandReplayReceiptCount : Nat
  trackedArtifactDigestCount : Nat
  mutationControlCount : Nat
  supportStateEffectNoneOrRecordOnly : Bool
  nonClaimBoundary : Bool
  missingArtifactControlRejected : Bool
  digestMismatchControlRejected : Bool
  failedCommandControlRejected : Bool
  missingNonClaimsControlRejected : Bool
  supportPromotionControlRejected : Bool
deriving DecidableEq, Repr

def receiptRepositoryAuditSummary :
    ReceiptRepositoryAuditSummary where
  auditedReceiptCount := 4
  acceptedReceiptCount := 4
  digestCheckedReceiptCount := 3
  externalFingerprintReceiptCount := 1
  commandReplayReceiptCount := 4
  trackedArtifactDigestCount := 55
  mutationControlCount := 5
  supportStateEffectNoneOrRecordOnly := true
  nonClaimBoundary := true
  missingArtifactControlRejected := true
  digestMismatchControlRejected := true
  failedCommandControlRejected := true
  missingNonClaimsControlRejected := true
  supportPromotionControlRejected := true

def ReceiptRepositoryAuditValid
    (summary : ReceiptRepositoryAuditSummary) : Prop :=
  summary.auditedReceiptCount = 4 ∧
    summary.acceptedReceiptCount = 4 ∧
    summary.digestCheckedReceiptCount = 3 ∧
    summary.externalFingerprintReceiptCount = 1 ∧
    summary.commandReplayReceiptCount = 4 ∧
    summary.trackedArtifactDigestCount = 55 ∧
    summary.mutationControlCount = 5 ∧
    summary.supportStateEffectNoneOrRecordOnly = true ∧
    summary.nonClaimBoundary = true ∧
    summary.missingArtifactControlRejected = true ∧
    summary.digestMismatchControlRejected = true ∧
    summary.failedCommandControlRejected = true ∧
    summary.missingNonClaimsControlRejected = true ∧
    summary.supportPromotionControlRejected = true

structure ReceiptRepositoryChallengeSummary where
  baseAuditPassed : Bool
  challengeCount : Nat
  acceptedChallengeCount : Nat
  trackedDigestChallengeCount : Nat
  externalFingerprintChallengeCount : Nat
  mutationControlCount : Nat
  trackedDigestMismatchControlRejected : Bool
  missingArtifactControlRejected : Bool
  externalFingerprintMismatchControlRejected : Bool
  missingNonClaimsControlRejected : Bool
  supportPromotionControlRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def receiptRepositoryChallengeSummary :
    ReceiptRepositoryChallengeSummary where
  baseAuditPassed := true
  challengeCount := 4
  acceptedChallengeCount := 4
  trackedDigestChallengeCount := 3
  externalFingerprintChallengeCount := 1
  mutationControlCount := 5
  trackedDigestMismatchControlRejected := true
  missingArtifactControlRejected := true
  externalFingerprintMismatchControlRejected := true
  missingNonClaimsControlRejected := true
  supportPromotionControlRejected := true
  supportStateEffectNone := true
  nonClaimBoundary := true

def ReceiptRepositoryChallengeValid
    (summary : ReceiptRepositoryChallengeSummary) : Prop :=
  summary.baseAuditPassed = true ∧
    summary.challengeCount = 4 ∧
    summary.acceptedChallengeCount = 4 ∧
    summary.trackedDigestChallengeCount = 3 ∧
    summary.externalFingerprintChallengeCount = 1 ∧
    summary.mutationControlCount = 5 ∧
    summary.trackedDigestMismatchControlRejected = true ∧
    summary.missingArtifactControlRejected = true ∧
    summary.externalFingerprintMismatchControlRejected = true ∧
    summary.missingNonClaimsControlRejected = true ∧
    summary.supportPromotionControlRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

structure ArtifactLiveAttestationSummary where
  targetArtifactCount : Nat
  observationRouteCount : Nat
  acceptedObservationRouteCount : Nat
  mutationControlCount : Nat
  filesystemDigestMatchesTarget : Bool
  gitBlobDigestMatchesTarget : Bool
  commandReplayPassed : Bool
  observerRoutesIndependent : Bool
  sameComponentSelfCheckRejected : Bool
  trapReceiptRejected : Bool
  attestationLimitsRecorded : Bool
  supportStateEffectNone : Bool
  chapterCoreSupportEffectNone : Bool
  noUpwardTransition : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def artifactLiveAttestationSummary :
    ArtifactLiveAttestationSummary where
  targetArtifactCount := 1
  observationRouteCount := 3
  acceptedObservationRouteCount := 3
  mutationControlCount := 7
  filesystemDigestMatchesTarget := true
  gitBlobDigestMatchesTarget := true
  commandReplayPassed := true
  observerRoutesIndependent := true
  sameComponentSelfCheckRejected := true
  trapReceiptRejected := true
  attestationLimitsRecorded := true
  supportStateEffectNone := true
  chapterCoreSupportEffectNone := true
  noUpwardTransition := true
  nonClaimBoundary := true

def ArtifactLiveAttestationValid
    (summary : ArtifactLiveAttestationSummary) : Prop :=
  summary.targetArtifactCount = 1 ∧
    summary.observationRouteCount = 3 ∧
    summary.acceptedObservationRouteCount = 3 ∧
    summary.mutationControlCount = 7 ∧
    summary.filesystemDigestMatchesTarget = true ∧
    summary.gitBlobDigestMatchesTarget = true ∧
    summary.commandReplayPassed = true ∧
    summary.observerRoutesIndependent = true ∧
    summary.sameComponentSelfCheckRejected = true ∧
    summary.trapReceiptRejected = true ∧
    summary.attestationLimitsRecorded = true ∧
    summary.supportStateEffectNone = true ∧
    summary.chapterCoreSupportEffectNone = true ∧
    summary.noUpwardTransition = true ∧
    summary.nonClaimBoundary = true

structure ArtifactRandomizedAttestationSummary where
  candidateArtifactCount : Nat
  selectedArtifactCount : Nat
  observationRouteCount : Nat
  acceptedObservationRouteCount : Nat
  trapReceiptCount : Nat
  mutationControlCount : Nat
  mutationControlsRejected : Nat
  seededSelectionReproducible : Bool
  sampleBeyondOneArtifact : Bool
  observerRoutesIndependent : Bool
  filesystemDigestsMatch : Bool
  gitObjectDigestsMatch : Bool
  commandReplaysPassed : Bool
  trapReceiptsRejected : Bool
  sameComponentSelfCheckRejected : Bool
  attestationLimitsRecorded : Bool
  supportStateEffectNone : Bool
  chapterCoreSupportEffectNone : Bool
  noUpwardTransition : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def artifactRandomizedAttestationSummary :
    ArtifactRandomizedAttestationSummary where
  candidateArtifactCount := 6
  selectedArtifactCount := 4
  observationRouteCount := 12
  acceptedObservationRouteCount := 12
  trapReceiptCount := 4
  mutationControlCount := 8
  mutationControlsRejected := 8
  seededSelectionReproducible := true
  sampleBeyondOneArtifact := true
  observerRoutesIndependent := true
  filesystemDigestsMatch := true
  gitObjectDigestsMatch := true
  commandReplaysPassed := true
  trapReceiptsRejected := true
  sameComponentSelfCheckRejected := true
  attestationLimitsRecorded := true
  supportStateEffectNone := true
  chapterCoreSupportEffectNone := true
  noUpwardTransition := true
  nonClaimBoundary := true

def ArtifactRandomizedAttestationValid
    (summary : ArtifactRandomizedAttestationSummary) : Prop :=
  summary.candidateArtifactCount = 6 ∧
    summary.selectedArtifactCount = 4 ∧
    summary.observationRouteCount = 12 ∧
    summary.acceptedObservationRouteCount = 12 ∧
    summary.trapReceiptCount = 4 ∧
    summary.mutationControlCount = 8 ∧
    summary.mutationControlsRejected = 8 ∧
    summary.seededSelectionReproducible = true ∧
    summary.sampleBeyondOneArtifact = true ∧
    summary.observerRoutesIndependent = true ∧
    summary.filesystemDigestsMatch = true ∧
    summary.gitObjectDigestsMatch = true ∧
    summary.commandReplaysPassed = true ∧
    summary.trapReceiptsRejected = true ∧
    summary.sameComponentSelfCheckRejected = true ∧
    summary.attestationLimitsRecorded = true ∧
    summary.supportStateEffectNone = true ∧
    summary.chapterCoreSupportEffectNone = true ∧
    summary.noUpwardTransition = true ∧
    summary.nonClaimBoundary = true

structure EpistemicTcbFixtureSummary where
  minimalTrustBaseAccepted : Bool
  delegatedVerifierRecordOnlyAccepted : Bool
  outsideTcbBlockedRecordAccepted : Bool
  missingRootOfTrustRejected : Bool
  selfVerifierLaunderingRejected : Bool
  unboundedTrustPropagationRejected : Bool
  recursionStopRequired : Bool
  outsideTcbResidualsRequired : Bool
  supportPromotionFromTcbShapeRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def epistemicTcbFixtureSummary :
    EpistemicTcbFixtureSummary where
  minimalTrustBaseAccepted := true
  delegatedVerifierRecordOnlyAccepted := true
  outsideTcbBlockedRecordAccepted := true
  missingRootOfTrustRejected := true
  selfVerifierLaunderingRejected := true
  unboundedTrustPropagationRejected := true
  recursionStopRequired := true
  outsideTcbResidualsRequired := true
  supportPromotionFromTcbShapeRejected := true
  supportStateEffectNone := true
  nonClaimBoundary := true

def EpistemicTcbFixtureValid
    (summary : EpistemicTcbFixtureSummary) : Prop :=
  summary.minimalTrustBaseAccepted = true ∧
    summary.delegatedVerifierRecordOnlyAccepted = true ∧
    summary.outsideTcbBlockedRecordAccepted = true ∧
    summary.missingRootOfTrustRejected = true ∧
    summary.selfVerifierLaunderingRejected = true ∧
    summary.unboundedTrustPropagationRejected = true ∧
    summary.recursionStopRequired = true ∧
    summary.outsideTcbResidualsRequired = true ∧
    summary.supportPromotionFromTcbShapeRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

end AsiStackProofs.ArtifactGraph

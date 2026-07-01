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

theorem produced_artifact_records_parent_job_and_context_refs
    {record : ArtifactRecord} :
    ProducedArtifactTraceable record ->
    record.produced = true ->
      record.parentJobPresent = true ∧
        record.sourceRefsPresent = true ∧
          record.contextRefsPresent = true := by
  intro traceable produced
  exact traceable produced

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

end AsiStackProofs.ArtifactGraph

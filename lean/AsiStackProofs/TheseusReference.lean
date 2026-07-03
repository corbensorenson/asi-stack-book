namespace AsiStackProofs.TheseusReference

structure ImplementationReferenceClaimReview where
  implementationReferenceClaim : Bool
  reportRefPresent : Bool
  configOrToolRefPresent : Bool
  dashboardProseOnly : Bool
deriving DecidableEq, Repr

def ImplementationReferenceClaimHasArtifactSurface
    (review : ImplementationReferenceClaimReview) : Prop :=
  review.implementationReferenceClaim = true ->
    (review.reportRefPresent = true ∨
      review.configOrToolRefPresent = true) ∧
        review.dashboardProseOnly = false

theorem implementation_reference_claim_names_report_config_or_tool_not_dashboard_only
    {review : ImplementationReferenceClaimReview} :
    ImplementationReferenceClaimHasArtifactSurface review ->
    review.implementationReferenceClaim = true ->
    (review.reportRefPresent = true ∨
      review.configOrToolRefPresent = true) ∧
        review.dashboardProseOnly = false := by
  intro valid referenceClaim
  exact valid referenceClaim

theorem implementation_reference_claim_without_artifact_surface_rejected
    {review : ImplementationReferenceClaimReview} :
    review.implementationReferenceClaim = true ->
    ((review.reportRefPresent = false ∧
      review.configOrToolRefPresent = false) ∨
        review.dashboardProseOnly = true) ->
    ¬ ImplementationReferenceClaimHasArtifactSurface review := by
  intro referenceClaim missing valid
  unfold ImplementationReferenceClaimHasArtifactSurface at valid
  have artifactSurface := valid referenceClaim
  cases artifactSurface with
  | intro refs dashboardNotOnly =>
      cases missing with
      | inl missingRefs =>
          cases missingRefs with
          | intro reportMissing configMissing =>
              cases refs with
              | inl reportPresent =>
                  rw [reportMissing] at reportPresent
                  contradiction
              | inr configPresent =>
                  rw [configMissing] at configPresent
                  contradiction
      | inr dashboardOnly =>
          rw [dashboardOnly] at dashboardNotOnly
          contradiction

structure GateBeforePromotionReview where
  capabilityOrSelfEvolutionPromotion : Bool
  requiredGateReportsPresent : Bool
  requiredGateReportsPassing : Bool
  promotionAccepted : Bool
deriving DecidableEq, Repr

def MissingOrFailingGateReportsBlockPromotion
    (review : GateBeforePromotionReview) : Prop :=
  review.capabilityOrSelfEvolutionPromotion = true ->
    (review.requiredGateReportsPresent = false ∨
      review.requiredGateReportsPassing = false) ->
        review.promotionAccepted = false

theorem capability_or_self_evolution_promotion_blocked_without_passing_gate_reports
    {review : GateBeforePromotionReview} :
    MissingOrFailingGateReportsBlockPromotion review ->
    review.capabilityOrSelfEvolutionPromotion = true ->
    (review.requiredGateReportsPresent = false ∨
      review.requiredGateReportsPassing = false) ->
    review.promotionAccepted = false := by
  intro valid promoted missingOrFailing
  exact valid promoted missingOrFailing

theorem accepted_promotion_with_missing_or_failing_gate_reports_rejected
    {review : GateBeforePromotionReview} :
    MissingOrFailingGateReportsBlockPromotion review ->
    review.capabilityOrSelfEvolutionPromotion = true ->
    (review.requiredGateReportsPresent = false ∨
      review.requiredGateReportsPassing = false) ->
    ¬ review.promotionAccepted = true := by
  intro valid promoted missingOrFailing accepted
  have blocked := valid promoted missingOrFailing
  rw [blocked] at accepted
  contradiction

structure PublicReportBundleReview where
  bundleCitedAsImported : Bool
  goalContractPresent : Bool
  compilerArtifactPresent : Bool
  workBoardItemPresent : Bool
  gateRecordPresent : Bool
  residualRecordPresent : Bool
  nonClaimRecorded : Bool
  reviewNotePresent : Bool
  publicationBoundaryRecorded : Bool
deriving DecidableEq, Repr

def PublicReportBundleImportValid
    (review : PublicReportBundleReview) : Prop :=
  review.bundleCitedAsImported = true ->
    review.goalContractPresent = true ∧
      review.compilerArtifactPresent = true ∧
        review.workBoardItemPresent = true ∧
          review.gateRecordPresent = true ∧
            review.residualRecordPresent = true ∧
              review.nonClaimRecorded = true ∧
                review.reviewNotePresent = true ∧
                  review.publicationBoundaryRecorded = true

theorem imported_report_bundle_missing_required_artifact_rejected
    {review : PublicReportBundleReview} :
    review.bundleCitedAsImported = true ->
    (review.goalContractPresent = false ∨
      review.compilerArtifactPresent = false ∨
        review.workBoardItemPresent = false ∨
          review.gateRecordPresent = false ∨
            review.residualRecordPresent = false ∨
              review.nonClaimRecorded = false ∨
                review.reviewNotePresent = false ∨
                  review.publicationBoundaryRecorded = false) ->
    ¬ PublicReportBundleImportValid review := by
  intro imported missing valid
  unfold PublicReportBundleImportValid at valid
  have complete := valid imported
  cases complete with
  | intro goalPresent rest =>
      cases rest with
      | intro compilerPresent rest =>
          cases rest with
          | intro workBoardPresent rest =>
              cases rest with
              | intro gatePresent rest =>
                  cases rest with
                  | intro residualPresent rest =>
                      cases rest with
                      | intro nonClaimPresent rest =>
                          cases rest with
                          | intro reviewPresent publicationBoundaryPresent =>
                              cases missing with
                              | inl goalMissing =>
                                  rw [goalMissing] at goalPresent
                                  contradiction
                              | inr restMissing =>
                                  cases restMissing with
                                  | inl compilerMissing =>
                                      rw [compilerMissing] at compilerPresent
                                      contradiction
                                  | inr restMissing =>
                                      cases restMissing with
                                      | inl workBoardMissing =>
                                          rw [workBoardMissing] at workBoardPresent
                                          contradiction
                                      | inr restMissing =>
                                          cases restMissing with
                                          | inl gateMissing =>
                                              rw [gateMissing] at gatePresent
                                              contradiction
                                          | inr restMissing =>
                                              cases restMissing with
                                              | inl residualMissing =>
                                                  rw [residualMissing] at residualPresent
                                                  contradiction
                                              | inr restMissing =>
                                                  cases restMissing with
                                                  | inl nonClaimMissing =>
                                                      rw [nonClaimMissing] at nonClaimPresent
                                                      contradiction
                                                  | inr restMissing =>
                                                      cases restMissing with
                                                      | inl reviewMissing =>
                                                          rw [reviewMissing] at reviewPresent
                                                          contradiction
                                                      | inr publicationBoundaryMissing =>
                                                          rw [publicationBoundaryMissing] at publicationBoundaryPresent
                                                          contradiction

structure ReplayReadinessReview where
  rowMarkedReplayReady : Bool
  commandPresent : Bool
  environmentNotesPresent : Bool
  inputBoundaryPresent : Bool
  artifactChecksumPresent : Bool
  expectedOutputClassPresent : Bool
  failureBehaviorPresent : Bool
deriving DecidableEq, Repr

def ReplayReadyRecordValid (review : ReplayReadinessReview) : Prop :=
  review.rowMarkedReplayReady = true ->
    review.commandPresent = true ∧
      review.environmentNotesPresent = true ∧
        review.inputBoundaryPresent = true ∧
          review.artifactChecksumPresent = true ∧
            review.expectedOutputClassPresent = true ∧
              review.failureBehaviorPresent = true

theorem replay_ready_without_replay_boundary_artifacts_rejected
    {review : ReplayReadinessReview} :
    review.rowMarkedReplayReady = true ->
    (review.commandPresent = false ∨
      review.environmentNotesPresent = false ∨
        review.inputBoundaryPresent = false ∨
          review.artifactChecksumPresent = false ∨
            review.expectedOutputClassPresent = false ∨
              review.failureBehaviorPresent = false) ->
    ¬ ReplayReadyRecordValid review := by
  intro replayReady missing valid
  unfold ReplayReadyRecordValid at valid
  have complete := valid replayReady
  cases complete with
  | intro commandPresent rest =>
      cases rest with
      | intro environmentPresent rest =>
          cases rest with
          | intro inputBoundaryPresent rest =>
              cases rest with
              | intro checksumPresent rest =>
                  cases rest with
                  | intro expectedOutputPresent failureBehaviorPresent =>
                      cases missing with
                      | inl commandMissing =>
                          rw [commandMissing] at commandPresent
                          contradiction
                      | inr restMissing =>
                          cases restMissing with
                          | inl environmentMissing =>
                              rw [environmentMissing] at environmentPresent
                              contradiction
                          | inr restMissing =>
                              cases restMissing with
                              | inl inputBoundaryMissing =>
                                  rw [inputBoundaryMissing] at inputBoundaryPresent
                                  contradiction
                              | inr restMissing =>
                                  cases restMissing with
                                  | inl checksumMissing =>
                                      rw [checksumMissing] at checksumPresent
                                      contradiction
                                  | inr restMissing =>
                                      cases restMissing with
                                      | inl expectedOutputMissing =>
                                          rw [expectedOutputMissing] at expectedOutputPresent
                                          contradiction
                                      | inr failureBehaviorMissing =>
                                          rw [failureBehaviorMissing] at failureBehaviorPresent
                                          contradiction

structure PublicSafeTheseusArtifactReview where
  publicArtifactPublished : Bool
  privatePayloadCopied : Bool
  supportPromotionClaimed : Bool
  acceptedEvidenceTransitionPresent : Bool
  nonClaimsPresent : Bool
deriving DecidableEq, Repr

def PublicSafeTheseusArtifactValid
    (review : PublicSafeTheseusArtifactReview) : Prop :=
  review.publicArtifactPublished = true ->
    review.privatePayloadCopied = false ∧
      (review.supportPromotionClaimed = true ->
        review.acceptedEvidenceTransitionPresent = true) ∧
          review.nonClaimsPresent = true

theorem public_theseus_artifact_with_private_payload_or_support_overclaim_rejected
    {review : PublicSafeTheseusArtifactReview} :
    review.publicArtifactPublished = true ->
    (review.privatePayloadCopied = true ∨
      (review.supportPromotionClaimed = true ∧
        review.acceptedEvidenceTransitionPresent = false) ∨
          review.nonClaimsPresent = false) ->
    ¬ PublicSafeTheseusArtifactValid review := by
  intro published invalid valid
  unfold PublicSafeTheseusArtifactValid at valid
  have complete := valid published
  cases complete with
  | intro privatePayloadNotCopied rest =>
      cases rest with
      | intro supportPromotionRequiresTransition nonClaimsPresent =>
          cases invalid with
          | inl privateCopied =>
              rw [privateCopied] at privatePayloadNotCopied
              contradiction
          | inr supportOrNonClaims =>
              cases supportOrNonClaims with
              | inl supportOverclaim =>
                  cases supportOverclaim with
                  | intro supportClaimed transitionMissing =>
                      have transitionPresent := supportPromotionRequiresTransition supportClaimed
                      rw [transitionMissing] at transitionPresent
                      contradiction
              | inr nonClaimsMissing =>
                  rw [nonClaimsMissing] at nonClaimsPresent
                  contradiction

inductive TheseusReportBundleAuditRoute where
  | rejectAudit
  | acceptFixtureAudit
deriving DecidableEq, Repr

structure TheseusReportBundleAuditSummary where
  publicSafeFixtureBundleCited : Bool
  goalContractPresent : Bool
  compilerArtifactPresent : Bool
  workBoardItemPresent : Bool
  gateRecordPresent : Bool
  residualRecordPresent : Bool
  nonClaimRecorded : Bool
  reviewNotePresent : Bool
  publicationBoundaryRecorded : Bool
  replayReadinessRowsComplete : Bool
  crosswalkRowsComplete : Bool
  gateMappingsComplete : Bool
  workBoardContractComplete : Bool
  artifactGapsVisible : Bool
  interventionLadderOrdered : Bool
  supportStateEffectNone : Bool
  noLiveReplayClaim : Bool
  noSupportPromotionClaim : Bool
deriving DecidableEq, Repr

def TheseusReportBundleAuditComplete
    (summary : TheseusReportBundleAuditSummary) : Bool :=
  summary.publicSafeFixtureBundleCited &&
  summary.goalContractPresent &&
  summary.compilerArtifactPresent &&
  summary.workBoardItemPresent &&
  summary.gateRecordPresent &&
  summary.residualRecordPresent &&
  summary.nonClaimRecorded &&
  summary.reviewNotePresent &&
  summary.publicationBoundaryRecorded &&
  summary.replayReadinessRowsComplete &&
  summary.crosswalkRowsComplete &&
  summary.gateMappingsComplete &&
  summary.workBoardContractComplete &&
  summary.artifactGapsVisible &&
  summary.interventionLadderOrdered &&
  summary.supportStateEffectNone &&
  summary.noLiveReplayClaim &&
  summary.noSupportPromotionClaim

def TheseusReportBundleAuditRouteFor
    (summary : TheseusReportBundleAuditSummary) :
    TheseusReportBundleAuditRoute :=
  if TheseusReportBundleAuditComplete summary then
    TheseusReportBundleAuditRoute.acceptFixtureAudit
  else
    TheseusReportBundleAuditRoute.rejectAudit

def PublicReportBundleReviewOfAuditSummary
    (summary : TheseusReportBundleAuditSummary) :
    PublicReportBundleReview :=
  {
    bundleCitedAsImported := summary.publicSafeFixtureBundleCited,
    goalContractPresent := summary.goalContractPresent,
    compilerArtifactPresent := summary.compilerArtifactPresent,
    workBoardItemPresent := summary.workBoardItemPresent,
    gateRecordPresent := summary.gateRecordPresent,
    residualRecordPresent := summary.residualRecordPresent,
    nonClaimRecorded := summary.nonClaimRecorded,
    reviewNotePresent := summary.reviewNotePresent,
    publicationBoundaryRecorded := summary.publicationBoundaryRecorded
  }

theorem hidden_artifact_gap_rejects_theseus_report_bundle_audit
    {summary : TheseusReportBundleAuditSummary} :
    summary.artifactGapsVisible = false ->
      TheseusReportBundleAuditRouteFor summary =
        TheseusReportBundleAuditRoute.rejectAudit := by
  intro hiddenGap
  simp [
    TheseusReportBundleAuditRouteFor,
    TheseusReportBundleAuditComplete,
    hiddenGap,
  ]

theorem complete_theseus_report_bundle_audit_accepts
    {summary : TheseusReportBundleAuditSummary} :
    summary.publicSafeFixtureBundleCited = true ->
    summary.goalContractPresent = true ->
    summary.compilerArtifactPresent = true ->
    summary.workBoardItemPresent = true ->
    summary.gateRecordPresent = true ->
    summary.residualRecordPresent = true ->
    summary.nonClaimRecorded = true ->
    summary.reviewNotePresent = true ->
    summary.publicationBoundaryRecorded = true ->
    summary.replayReadinessRowsComplete = true ->
    summary.crosswalkRowsComplete = true ->
    summary.gateMappingsComplete = true ->
    summary.workBoardContractComplete = true ->
    summary.artifactGapsVisible = true ->
    summary.interventionLadderOrdered = true ->
    summary.supportStateEffectNone = true ->
    summary.noLiveReplayClaim = true ->
    summary.noSupportPromotionClaim = true ->
      TheseusReportBundleAuditRouteFor summary =
        TheseusReportBundleAuditRoute.acceptFixtureAudit := by
  intro cited goal compiler workBoard gate residual nonClaim review
    publication replayReady crosswalk gateMappings workBoardContract
    artifactGaps ladder supportNone noLiveReplay noSupportPromotion
  simp [
    TheseusReportBundleAuditRouteFor,
    TheseusReportBundleAuditComplete,
    cited,
    goal,
    compiler,
    workBoard,
    gate,
    residual,
    nonClaim,
    review,
    publication,
    replayReady,
    crosswalk,
    gateMappings,
    workBoardContract,
    artifactGaps,
    ladder,
    supportNone,
    noLiveReplay,
    noSupportPromotion,
  ]

theorem accepted_theseus_report_bundle_audit_preserves_public_boundaries
    {summary : TheseusReportBundleAuditSummary} :
    TheseusReportBundleAuditRouteFor summary =
      TheseusReportBundleAuditRoute.acceptFixtureAudit ->
      summary.supportStateEffectNone = true ∧
        summary.noLiveReplayClaim = true ∧
          summary.noSupportPromotionClaim = true := by
  intro accepted
  unfold TheseusReportBundleAuditRouteFor at accepted
  cases complete : TheseusReportBundleAuditComplete summary with
  | false =>
      simp [complete] at accepted
  | true =>
      unfold TheseusReportBundleAuditComplete at complete
      repeat
        first
        | cases h : summary.publicSafeFixtureBundleCited <;> simp [h] at complete
        | cases h : summary.goalContractPresent <;> simp [h] at complete
        | cases h : summary.compilerArtifactPresent <;> simp [h] at complete
        | cases h : summary.workBoardItemPresent <;> simp [h] at complete
        | cases h : summary.gateRecordPresent <;> simp [h] at complete
        | cases h : summary.residualRecordPresent <;> simp [h] at complete
        | cases h : summary.nonClaimRecorded <;> simp [h] at complete
        | cases h : summary.reviewNotePresent <;> simp [h] at complete
        | cases h : summary.publicationBoundaryRecorded <;> simp [h] at complete
        | cases h : summary.replayReadinessRowsComplete <;> simp [h] at complete
        | cases h : summary.crosswalkRowsComplete <;> simp [h] at complete
        | cases h : summary.gateMappingsComplete <;> simp [h] at complete
        | cases h : summary.workBoardContractComplete <;> simp [h] at complete
        | cases h : summary.artifactGapsVisible <;> simp [h] at complete
        | cases h : summary.interventionLadderOrdered <;> simp [h] at complete
        | cases h : summary.supportStateEffectNone <;> simp [h] at complete
        | cases h : summary.noLiveReplayClaim <;> simp [h] at complete
        | cases h : summary.noSupportPromotionClaim <;> simp [h] at complete
      exact ⟨rfl, rfl, rfl⟩

theorem complete_theseus_report_bundle_audit_satisfies_public_bundle_review
    {summary : TheseusReportBundleAuditSummary} :
    summary.publicSafeFixtureBundleCited = true ->
    summary.goalContractPresent = true ->
    summary.compilerArtifactPresent = true ->
    summary.workBoardItemPresent = true ->
    summary.gateRecordPresent = true ->
    summary.residualRecordPresent = true ->
    summary.nonClaimRecorded = true ->
    summary.reviewNotePresent = true ->
    summary.publicationBoundaryRecorded = true ->
      PublicReportBundleImportValid
        (PublicReportBundleReviewOfAuditSummary summary) := by
  intro cited goal compiler workBoard gate residual nonClaim review
    publication
  unfold PublicReportBundleImportValid
  unfold PublicReportBundleReviewOfAuditSummary
  intro citedAsImported
  simp [
    goal,
    compiler,
    workBoard,
    gate,
    residual,
    nonClaim,
    review,
    publication,
  ]

structure TheseusPublicTaskBundleImportSummary where
  sourceReportCount : Nat
  publicTaskCount : Nat
  metadataCaseManifestRows : Nat
  publicTrainingRows : Nat
  externalInferenceCalls : Nat
  operatorGateCount : Nat
  operatorGatesPassed : Nat
  benchmarkGateCount : Nat
  benchmarkGatesPassed : Nat
  residualCount : Nat
  taskLevelRegressions : Nat
  promptsExported : Bool
  testsExported : Bool
  solutionsExported : Bool
  candidateCodeExported : Bool
  tracesExported : Bool
  scoreLabelsExported : Bool
  localCheckoutDirty : Bool
  cleanLiveReplayClaimed : Bool
  missingArtifactsVisible : Bool
  supportStateEffectNone : Bool
  evidenceTransitionCreated : Bool
deriving DecidableEq, Repr

def TheseusPublicTaskBundleImportPublicSafe
    (summary : TheseusPublicTaskBundleImportSummary) : Prop :=
  summary.publicTrainingRows = 0 ∧
    summary.externalInferenceCalls = 0 ∧
      summary.promptsExported = false ∧
        summary.testsExported = false ∧
          summary.solutionsExported = false ∧
            summary.candidateCodeExported = false ∧
              summary.tracesExported = false ∧
                summary.scoreLabelsExported = false

def TheseusPublicTaskBundleImportGatesComplete
    (summary : TheseusPublicTaskBundleImportSummary) : Prop :=
  summary.operatorGateCount = summary.operatorGatesPassed ∧
    summary.benchmarkGateCount = summary.benchmarkGatesPassed ∧
      summary.operatorGateCount = 12 ∧
        summary.benchmarkGateCount = 18

def TheseusPublicTaskBundleImportPreservesBoundaries
    (summary : TheseusPublicTaskBundleImportSummary) : Prop :=
  summary.sourceReportCount = 7 ∧
    summary.publicTaskCount = 64 ∧
      summary.metadataCaseManifestRows = 64 ∧
        summary.residualCount = 19 ∧
          summary.taskLevelRegressions = 0 ∧
            summary.localCheckoutDirty = true ∧
              summary.cleanLiveReplayClaimed = false ∧
                summary.missingArtifactsVisible = true ∧
                  summary.supportStateEffectNone = true ∧
                    summary.evidenceTransitionCreated = false

def TheseusPublicTaskBundleImportValid
    (summary : TheseusPublicTaskBundleImportSummary) : Prop :=
  TheseusPublicTaskBundleImportPublicSafe summary ∧
    TheseusPublicTaskBundleImportGatesComplete summary ∧
      TheseusPublicTaskBundleImportPreservesBoundaries summary

def theseusPublicTaskBundleImportFixture :
    TheseusPublicTaskBundleImportSummary := {
  sourceReportCount := 7
  publicTaskCount := 64
  metadataCaseManifestRows := 64
  publicTrainingRows := 0
  externalInferenceCalls := 0
  operatorGateCount := 12
  operatorGatesPassed := 12
  benchmarkGateCount := 18
  benchmarkGatesPassed := 18
  residualCount := 19
  taskLevelRegressions := 0
  promptsExported := false
  testsExported := false
  solutionsExported := false
  candidateCodeExported := false
  tracesExported := false
  scoreLabelsExported := false
  localCheckoutDirty := true
  cleanLiveReplayClaimed := false
  missingArtifactsVisible := true
  supportStateEffectNone := true
  evidenceTransitionCreated := false
}

theorem theseus_public_task_bundle_import_fixture_public_safe :
    TheseusPublicTaskBundleImportPublicSafe
      theseusPublicTaskBundleImportFixture := by
  simp [TheseusPublicTaskBundleImportPublicSafe,
    theseusPublicTaskBundleImportFixture]

theorem theseus_public_task_bundle_import_fixture_gates_complete :
    TheseusPublicTaskBundleImportGatesComplete
      theseusPublicTaskBundleImportFixture := by
  simp [TheseusPublicTaskBundleImportGatesComplete,
    theseusPublicTaskBundleImportFixture]

theorem theseus_public_task_bundle_import_fixture_preserves_no_promotion_boundary :
    TheseusPublicTaskBundleImportPreservesBoundaries
      theseusPublicTaskBundleImportFixture := by
  simp [TheseusPublicTaskBundleImportPreservesBoundaries,
    theseusPublicTaskBundleImportFixture]

theorem theseus_public_task_bundle_import_fixture_valid :
    TheseusPublicTaskBundleImportValid
      theseusPublicTaskBundleImportFixture := by
  simp [TheseusPublicTaskBundleImportValid,
    TheseusPublicTaskBundleImportPublicSafe,
    TheseusPublicTaskBundleImportGatesComplete,
    TheseusPublicTaskBundleImportPreservesBoundaries,
    theseusPublicTaskBundleImportFixture]

theorem theseus_public_task_bundle_import_clean_replay_overclaim_rejected :
    ¬ TheseusPublicTaskBundleImportValid
      { theseusPublicTaskBundleImportFixture with
        cleanLiveReplayClaimed := true } := by
  intro valid
  simp [TheseusPublicTaskBundleImportValid,
    TheseusPublicTaskBundleImportPreservesBoundaries,
    TheseusPublicTaskBundleImportPublicSafe,
    TheseusPublicTaskBundleImportGatesComplete,
    theseusPublicTaskBundleImportFixture] at valid

structure TheseusFastSupportAggregateSummary where
  supportLaneCount : Nat
  commandReplayCount : Nat
  nestedSupportReplayCommandCount : Nat
  trackedArtifactCount : Nat
  publicTaskCount : Nat
  expectedInvalidOrRejectedControlCount : Nat
  noPromotionDecisionCount : Nat
  generationModeImportIncluded : Bool
  supportReplayProbeIncluded : Bool
  theseusPublicTaskBundleIncluded : Bool
  fastGenerationTaskBundleIncluded : Bool
  cleanLiveReplayClaimed : Bool
  modelQualityClaimed : Bool
  generationSpeedClaimed : Bool
  usefulSolutionModelClaimed : Bool
  chapterCorePromotionClaimed : Bool
  supportStatePromotionClaimed : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def TheseusFastSupportAggregateCarriesCounts
    (summary : TheseusFastSupportAggregateSummary) : Prop :=
  summary.supportLaneCount = 2 ∧
    summary.commandReplayCount = 4 ∧
      summary.nestedSupportReplayCommandCount = 2 ∧
        summary.trackedArtifactCount = 16 ∧
          summary.publicTaskCount = 68 ∧
            summary.expectedInvalidOrRejectedControlCount = 14 ∧
              summary.noPromotionDecisionCount = 2

def TheseusFastSupportAggregateIncludesSurfaces
    (summary : TheseusFastSupportAggregateSummary) : Prop :=
  summary.generationModeImportIncluded = true ∧
    summary.supportReplayProbeIncluded = true ∧
      summary.theseusPublicTaskBundleIncluded = true ∧
        summary.fastGenerationTaskBundleIncluded = true

def TheseusFastSupportAggregatePreservesBoundaries
    (summary : TheseusFastSupportAggregateSummary) : Prop :=
  summary.cleanLiveReplayClaimed = false ∧
    summary.modelQualityClaimed = false ∧
      summary.generationSpeedClaimed = false ∧
        summary.usefulSolutionModelClaimed = false ∧
          summary.chapterCorePromotionClaimed = false ∧
            summary.supportStatePromotionClaimed = false ∧
              summary.nonClaimBoundaryRecorded = true

def TheseusFastSupportAggregateValid
    (summary : TheseusFastSupportAggregateSummary) : Prop :=
  TheseusFastSupportAggregateCarriesCounts summary ∧
    TheseusFastSupportAggregateIncludesSurfaces summary ∧
      TheseusFastSupportAggregatePreservesBoundaries summary

def theseusFastSupportAggregateFixture :
    TheseusFastSupportAggregateSummary := {
  supportLaneCount := 2
  commandReplayCount := 4
  nestedSupportReplayCommandCount := 2
  trackedArtifactCount := 16
  publicTaskCount := 68
  expectedInvalidOrRejectedControlCount := 14
  noPromotionDecisionCount := 2
  generationModeImportIncluded := true
  supportReplayProbeIncluded := true
  theseusPublicTaskBundleIncluded := true
  fastGenerationTaskBundleIncluded := true
  cleanLiveReplayClaimed := false
  modelQualityClaimed := false
  generationSpeedClaimed := false
  usefulSolutionModelClaimed := false
  chapterCorePromotionClaimed := false
  supportStatePromotionClaimed := false
  nonClaimBoundaryRecorded := true
}

theorem theseus_fast_support_aggregate_fixture_valid :
    TheseusFastSupportAggregateValid
      theseusFastSupportAggregateFixture := by
  simp [TheseusFastSupportAggregateValid,
    TheseusFastSupportAggregateCarriesCounts,
    TheseusFastSupportAggregateIncludesSurfaces,
    TheseusFastSupportAggregatePreservesBoundaries,
    theseusFastSupportAggregateFixture]

theorem theseus_fast_support_aggregate_preserves_no_promotion :
    TheseusFastSupportAggregatePreservesBoundaries
      theseusFastSupportAggregateFixture := by
  simp [TheseusFastSupportAggregatePreservesBoundaries,
    theseusFastSupportAggregateFixture]

theorem theseus_fast_support_aggregate_carries_task_and_control_counts :
    theseusFastSupportAggregateFixture.publicTaskCount = 68 ∧
      theseusFastSupportAggregateFixture.expectedInvalidOrRejectedControlCount = 14 ∧
        theseusFastSupportAggregateFixture.noPromotionDecisionCount = 2 := by
  simp [theseusFastSupportAggregateFixture]

theorem theseus_fast_support_aggregate_clean_replay_overclaim_rejected :
    ¬ TheseusFastSupportAggregateValid
      { theseusFastSupportAggregateFixture with
        cleanLiveReplayClaimed := true } := by
  intro valid
  simp [TheseusFastSupportAggregateValid,
    TheseusFastSupportAggregateCarriesCounts,
    TheseusFastSupportAggregateIncludesSurfaces,
    TheseusFastSupportAggregatePreservesBoundaries,
    theseusFastSupportAggregateFixture] at valid

end AsiStackProofs.TheseusReference

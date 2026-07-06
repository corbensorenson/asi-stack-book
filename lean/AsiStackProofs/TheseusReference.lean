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

structure TheseusArtifactRetentionReplayImportSummary where
  sourceReportDigestRecorded : Bool
  triggerStateGreen : Bool
  eligibleActionCount : Nat
  passedReplayCount : Nat
  failedReplayCount : Nat
  pointerVerifiedCount : Nat
  defeaterVerifiedCount : Nat
  jsonParseVerifiedCount : Nat
  hardGapCount : Nat
  expectedHashMatchesDecodedHash : Bool
  archiveExists : Bool
  resolverVerified : Bool
  compressionRecordVerified : Bool
  payloadBytes : Nat
  archivedBytes : Nat
  recordCountCompressedArtifact : Nat
  recordCountCompressionReceipt : Nat
  recordCountProofContractReceipt : Nat
  recordCountClaim : Nat
  recordCountArtifactGraph : Nat
  recordCountEvidenceTransition : Nat
  recordCountDefeater : Nat
  privatePayloadCopied : Bool
  pathFieldsRedacted : Bool
  publicTrainingRowsWritten : Nat
  externalInferenceCalls : Nat
  fallbackReturnCount : Nat
  chapterCorePromotionClaimed : Bool
  cleanLiveReplayClaimed : Bool
  modelQualityClaimed : Bool
  benchmarkPerformanceClaimed : Bool
  deployedResidualLedgerClaimed : Bool
  deployedArtifactGraphClaimed : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def TheseusArtifactRetentionReplayImportReplayValid
    (summary : TheseusArtifactRetentionReplayImportSummary) : Prop :=
  summary.sourceReportDigestRecorded = true ∧
    summary.triggerStateGreen = true ∧
      summary.eligibleActionCount = 1 ∧
        summary.passedReplayCount = 1 ∧
          summary.failedReplayCount = 0 ∧
            summary.pointerVerifiedCount = 1 ∧
              summary.defeaterVerifiedCount = 1 ∧
                summary.jsonParseVerifiedCount = 1 ∧
                  summary.hardGapCount = 0 ∧
                    summary.expectedHashMatchesDecodedHash = true ∧
                      summary.archiveExists = true ∧
                        summary.resolverVerified = true ∧
                          summary.compressionRecordVerified = true ∧
                            summary.payloadBytes = 41943527 ∧
                              summary.archivedBytes = 2389576

def TheseusArtifactRetentionReplayImportRecordsPresent
    (summary : TheseusArtifactRetentionReplayImportSummary) : Prop :=
  summary.recordCountCompressedArtifact = 1 ∧
    summary.recordCountCompressionReceipt = 1 ∧
      summary.recordCountProofContractReceipt = 1 ∧
        summary.recordCountClaim = 1 ∧
          summary.recordCountArtifactGraph = 1 ∧
            summary.recordCountEvidenceTransition = 1 ∧
              summary.recordCountDefeater = 1

def TheseusArtifactRetentionReplayImportPublicSafe
    (summary : TheseusArtifactRetentionReplayImportSummary) : Prop :=
  summary.privatePayloadCopied = false ∧
    summary.pathFieldsRedacted = true ∧
      summary.publicTrainingRowsWritten = 0 ∧
        summary.externalInferenceCalls = 0 ∧
          summary.fallbackReturnCount = 0

def TheseusArtifactRetentionReplayImportPreservesBoundaries
    (summary : TheseusArtifactRetentionReplayImportSummary) : Prop :=
  summary.chapterCorePromotionClaimed = false ∧
    summary.cleanLiveReplayClaimed = false ∧
      summary.modelQualityClaimed = false ∧
        summary.benchmarkPerformanceClaimed = false ∧
          summary.deployedResidualLedgerClaimed = false ∧
            summary.deployedArtifactGraphClaimed = false ∧
              summary.nonClaimBoundaryRecorded = true

def TheseusArtifactRetentionReplayImportValid
    (summary : TheseusArtifactRetentionReplayImportSummary) : Prop :=
  TheseusArtifactRetentionReplayImportReplayValid summary ∧
    TheseusArtifactRetentionReplayImportRecordsPresent summary ∧
      TheseusArtifactRetentionReplayImportPublicSafe summary ∧
        TheseusArtifactRetentionReplayImportPreservesBoundaries summary

def theseusArtifactRetentionReplayImportFixture :
    TheseusArtifactRetentionReplayImportSummary := {
  sourceReportDigestRecorded := true
  triggerStateGreen := true
  eligibleActionCount := 1
  passedReplayCount := 1
  failedReplayCount := 0
  pointerVerifiedCount := 1
  defeaterVerifiedCount := 1
  jsonParseVerifiedCount := 1
  hardGapCount := 0
  expectedHashMatchesDecodedHash := true
  archiveExists := true
  resolverVerified := true
  compressionRecordVerified := true
  payloadBytes := 41943527
  archivedBytes := 2389576
  recordCountCompressedArtifact := 1
  recordCountCompressionReceipt := 1
  recordCountProofContractReceipt := 1
  recordCountClaim := 1
  recordCountArtifactGraph := 1
  recordCountEvidenceTransition := 1
  recordCountDefeater := 1
  privatePayloadCopied := false
  pathFieldsRedacted := true
  publicTrainingRowsWritten := 0
  externalInferenceCalls := 0
  fallbackReturnCount := 0
  chapterCorePromotionClaimed := false
  cleanLiveReplayClaimed := false
  modelQualityClaimed := false
  benchmarkPerformanceClaimed := false
  deployedResidualLedgerClaimed := false
  deployedArtifactGraphClaimed := false
  nonClaimBoundaryRecorded := true
}

theorem theseus_artifact_retention_replay_import_fixture_valid :
    TheseusArtifactRetentionReplayImportValid
      theseusArtifactRetentionReplayImportFixture := by
  simp [
    TheseusArtifactRetentionReplayImportValid,
    TheseusArtifactRetentionReplayImportReplayValid,
    TheseusArtifactRetentionReplayImportRecordsPresent,
    TheseusArtifactRetentionReplayImportPublicSafe,
    TheseusArtifactRetentionReplayImportPreservesBoundaries,
    theseusArtifactRetentionReplayImportFixture,
  ]

theorem theseus_artifact_retention_replay_import_hash_mismatch_rejected :
    ¬ TheseusArtifactRetentionReplayImportValid
      { theseusArtifactRetentionReplayImportFixture with
        expectedHashMatchesDecodedHash := false } := by
  intro valid
  simp [
    TheseusArtifactRetentionReplayImportValid,
    TheseusArtifactRetentionReplayImportReplayValid,
    TheseusArtifactRetentionReplayImportRecordsPresent,
    TheseusArtifactRetentionReplayImportPublicSafe,
    TheseusArtifactRetentionReplayImportPreservesBoundaries,
    theseusArtifactRetentionReplayImportFixture,
  ] at valid

theorem theseus_artifact_retention_replay_import_core_promotion_rejected :
    ¬ TheseusArtifactRetentionReplayImportValid
      { theseusArtifactRetentionReplayImportFixture with
        chapterCorePromotionClaimed := true } := by
  intro valid
  simp [
    TheseusArtifactRetentionReplayImportValid,
    TheseusArtifactRetentionReplayImportReplayValid,
    TheseusArtifactRetentionReplayImportRecordsPresent,
    TheseusArtifactRetentionReplayImportPublicSafe,
    TheseusArtifactRetentionReplayImportPreservesBoundaries,
    theseusArtifactRetentionReplayImportFixture,
  ] at valid

structure TheseusModuleDefinitionOfDoneImportSummary where
  triggerGreen : Bool
  moduleRecordsReady : Nat
  moduleRecordCount : Nat
  majorSurfaceCount : Nat
  hardGapCount : Nat
  warningCount : Nat
  bookStandardSourcesPresent : Nat
  bookStandardSourceCount : Nat
  sourceBacklogWorkCardCount : Nat
  sourceBacklogRouteSmokePassed : Bool
  negativeEvidenceLinked : Bool
  privatePayloadCopied : Bool
  rawReportCopied : Bool
  pathFieldsRedacted : Bool
  chapterCorePromotion : Bool
  capabilityClaim : Bool
  cleanLiveReplayClaimed : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def TheseusModuleDefinitionOfDoneImportRecordsReady
    (summary : TheseusModuleDefinitionOfDoneImportSummary) : Prop :=
  summary.triggerGreen = true ∧
    summary.moduleRecordsReady = 22 ∧
      summary.moduleRecordCount = 22 ∧
        summary.majorSurfaceCount = 22 ∧
          summary.hardGapCount = 0 ∧
            summary.warningCount = 0 ∧
              summary.bookStandardSourcesPresent = 7 ∧
                summary.bookStandardSourceCount = 7 ∧
                  summary.sourceBacklogWorkCardCount = 20 ∧
                    summary.sourceBacklogRouteSmokePassed = true ∧
                      summary.negativeEvidenceLinked = true

def TheseusModuleDefinitionOfDoneImportPublicSafe
    (summary : TheseusModuleDefinitionOfDoneImportSummary) : Prop :=
  summary.privatePayloadCopied = false ∧
    summary.rawReportCopied = false ∧
      summary.pathFieldsRedacted = true ∧
        summary.nonClaimBoundaryRecorded = true

def TheseusModuleDefinitionOfDoneImportPreservesBoundaries
    (summary : TheseusModuleDefinitionOfDoneImportSummary) : Prop :=
  summary.chapterCorePromotion = false ∧
    summary.capabilityClaim = false ∧
      summary.cleanLiveReplayClaimed = false

def TheseusModuleDefinitionOfDoneImportValid
    (summary : TheseusModuleDefinitionOfDoneImportSummary) : Prop :=
  TheseusModuleDefinitionOfDoneImportRecordsReady summary ∧
    TheseusModuleDefinitionOfDoneImportPublicSafe summary ∧
      TheseusModuleDefinitionOfDoneImportPreservesBoundaries summary

def theseusModuleDefinitionOfDoneImportFixture :
    TheseusModuleDefinitionOfDoneImportSummary := {
  triggerGreen := true
  moduleRecordsReady := 22
  moduleRecordCount := 22
  majorSurfaceCount := 22
  hardGapCount := 0
  warningCount := 0
  bookStandardSourcesPresent := 7
  bookStandardSourceCount := 7
  sourceBacklogWorkCardCount := 20
  sourceBacklogRouteSmokePassed := true
  negativeEvidenceLinked := true
  privatePayloadCopied := false
  rawReportCopied := false
  pathFieldsRedacted := true
  chapterCorePromotion := false
  capabilityClaim := false
  cleanLiveReplayClaimed := false
  nonClaimBoundaryRecorded := true
}

theorem theseus_module_definition_of_done_import_fixture_valid :
    TheseusModuleDefinitionOfDoneImportValid
      theseusModuleDefinitionOfDoneImportFixture := by
  simp [
    TheseusModuleDefinitionOfDoneImportValid,
    TheseusModuleDefinitionOfDoneImportRecordsReady,
    TheseusModuleDefinitionOfDoneImportPublicSafe,
    TheseusModuleDefinitionOfDoneImportPreservesBoundaries,
    theseusModuleDefinitionOfDoneImportFixture,
  ]

theorem theseus_module_definition_of_done_import_core_promotion_rejected :
    ¬ TheseusModuleDefinitionOfDoneImportValid
      { theseusModuleDefinitionOfDoneImportFixture with
        chapterCorePromotion := true } := by
  intro valid
  simp [
    TheseusModuleDefinitionOfDoneImportValid,
    TheseusModuleDefinitionOfDoneImportRecordsReady,
    TheseusModuleDefinitionOfDoneImportPublicSafe,
    TheseusModuleDefinitionOfDoneImportPreservesBoundaries,
    theseusModuleDefinitionOfDoneImportFixture,
  ] at valid

theorem theseus_module_definition_of_done_import_capability_overclaim_rejected :
    ¬ TheseusModuleDefinitionOfDoneImportValid
      { theseusModuleDefinitionOfDoneImportFixture with
        capabilityClaim := true } := by
  intro valid
  simp [
    TheseusModuleDefinitionOfDoneImportValid,
    TheseusModuleDefinitionOfDoneImportRecordsReady,
    TheseusModuleDefinitionOfDoneImportPublicSafe,
    TheseusModuleDefinitionOfDoneImportPreservesBoundaries,
    theseusModuleDefinitionOfDoneImportFixture,
  ] at valid

structure TheseusProjectRegistryImportSummary where
  entryCount : Nat
  registeredPathCount : Nat
  surfaceCount : Nat
  coverageComplete : Bool
  unregisteredActiveSources : Nat
  unclassifiedDuplicateFamilies : Nat
  staleReportOutputs : Nat
  missingReportOutputs : Nat
  generatedSourceArtifacts : Nat
  registryGovernanceViolations : Nat
  registryHardGovernanceViolations : Nat
  externalInferenceCalls : Nat
  rawReportCopied : Bool
  privatePayloadCopied : Bool
  pathFieldsRedacted : Bool
  cleanLiveReplayClaimed : Bool
  chapterCorePromotion : Bool
  modelQualityClaim : Bool
  deploymentClaim : Bool
  capabilityClaim : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def TheseusProjectRegistryImportRegistryHealthy
    (summary : TheseusProjectRegistryImportSummary) : Prop :=
  summary.entryCount = 5662 ∧
    summary.registeredPathCount = 5662 ∧
      summary.surfaceCount = 24 ∧
        summary.coverageComplete = true ∧
          summary.unregisteredActiveSources = 0 ∧
            summary.unclassifiedDuplicateFamilies = 0 ∧
              summary.staleReportOutputs = 0 ∧
                summary.missingReportOutputs = 0 ∧
                  summary.generatedSourceArtifacts = 0 ∧
                    summary.registryGovernanceViolations = 0 ∧
                      summary.registryHardGovernanceViolations = 0

def TheseusProjectRegistryImportPublicSafe
    (summary : TheseusProjectRegistryImportSummary) : Prop :=
  summary.externalInferenceCalls = 0 ∧
    summary.rawReportCopied = false ∧
      summary.privatePayloadCopied = false ∧
        summary.pathFieldsRedacted = true ∧
          summary.nonClaimBoundaryRecorded = true

def TheseusProjectRegistryImportPreservesBoundaries
    (summary : TheseusProjectRegistryImportSummary) : Prop :=
  summary.cleanLiveReplayClaimed = false ∧
    summary.chapterCorePromotion = false ∧
      summary.modelQualityClaim = false ∧
        summary.deploymentClaim = false ∧
          summary.capabilityClaim = false

def TheseusProjectRegistryImportValid
    (summary : TheseusProjectRegistryImportSummary) : Prop :=
  TheseusProjectRegistryImportRegistryHealthy summary ∧
    TheseusProjectRegistryImportPublicSafe summary ∧
      TheseusProjectRegistryImportPreservesBoundaries summary

def theseusProjectRegistryImportFixture :
    TheseusProjectRegistryImportSummary := {
  entryCount := 5662
  registeredPathCount := 5662
  surfaceCount := 24
  coverageComplete := true
  unregisteredActiveSources := 0
  unclassifiedDuplicateFamilies := 0
  staleReportOutputs := 0
  missingReportOutputs := 0
  generatedSourceArtifacts := 0
  registryGovernanceViolations := 0
  registryHardGovernanceViolations := 0
  externalInferenceCalls := 0
  rawReportCopied := false
  privatePayloadCopied := false
  pathFieldsRedacted := true
  cleanLiveReplayClaimed := false
  chapterCorePromotion := false
  modelQualityClaim := false
  deploymentClaim := false
  capabilityClaim := false
  nonClaimBoundaryRecorded := true
}

theorem theseus_project_registry_import_fixture_valid :
    TheseusProjectRegistryImportValid
      theseusProjectRegistryImportFixture := by
  simp [
    TheseusProjectRegistryImportValid,
    TheseusProjectRegistryImportRegistryHealthy,
    TheseusProjectRegistryImportPublicSafe,
    TheseusProjectRegistryImportPreservesBoundaries,
    theseusProjectRegistryImportFixture,
  ]

theorem theseus_project_registry_import_unregistered_sources_rejected :
    ¬ TheseusProjectRegistryImportValid
      { theseusProjectRegistryImportFixture with
        unregisteredActiveSources := 1 } := by
  intro valid
  simp [
    TheseusProjectRegistryImportValid,
    TheseusProjectRegistryImportRegistryHealthy,
    TheseusProjectRegistryImportPublicSafe,
    TheseusProjectRegistryImportPreservesBoundaries,
    theseusProjectRegistryImportFixture,
  ] at valid

theorem theseus_project_registry_import_clean_replay_overclaim_rejected :
    ¬ TheseusProjectRegistryImportValid
      { theseusProjectRegistryImportFixture with
        cleanLiveReplayClaimed := true } := by
  intro valid
  simp [
    TheseusProjectRegistryImportValid,
    TheseusProjectRegistryImportRegistryHealthy,
    TheseusProjectRegistryImportPublicSafe,
    TheseusProjectRegistryImportPreservesBoundaries,
    theseusProjectRegistryImportFixture,
  ] at valid

theorem theseus_project_registry_import_core_promotion_rejected :
    ¬ TheseusProjectRegistryImportValid
      { theseusProjectRegistryImportFixture with
        chapterCorePromotion := true } := by
  intro valid
  simp [
    TheseusProjectRegistryImportValid,
    TheseusProjectRegistryImportRegistryHealthy,
    TheseusProjectRegistryImportPublicSafe,
    TheseusProjectRegistryImportPreservesBoundaries,
    theseusProjectRegistryImportFixture,
  ] at valid

theorem theseus_project_registry_import_private_payload_rejected :
    ¬ TheseusProjectRegistryImportValid
      { theseusProjectRegistryImportFixture with
        privatePayloadCopied := true } := by
  intro valid
  simp [
    TheseusProjectRegistryImportValid,
    TheseusProjectRegistryImportRegistryHealthy,
    TheseusProjectRegistryImportPublicSafe,
    TheseusProjectRegistryImportPreservesBoundaries,
    theseusProjectRegistryImportFixture,
  ] at valid

structure TheseusBookCrosswalkImportSummary where
  triggerGreen : Bool
  sourceSyncSmokePassed : Bool
  publicSafeEvidenceSmokePassed : Bool
  theseusToBookEvidenceCount : Nat
  roadmapBacklogItemCount : Nat
  sourceSyncReviewDecisionCount : Nat
  changedSourceFileCount : Nat
  removedSourceFileCount : Nat
  stalePhaseCount : Nat
  publicReportPointerRows : Nat
  publicSourceOrConfigPointerRows : Nat
  pointerOnlySupportRows : Nat
  missingSourceBasisCount : Nat
  donePhaseMissingEvidenceCount : Nat
  publicTrainingRowsWritten : Nat
  externalInferenceCalls : Nat
  fallbackReturnCount : Nat
  rawReportCopied : Bool
  privatePayloadCopied : Bool
  pathFieldsRedacted : Bool
  chapterCorePromotion : Bool
  cleanLiveReplayClaimed : Bool
  deploymentClaim : Bool
  modelQualityClaim : Bool
  capabilityClaim : Bool
  newSupportStateArgument : Bool
  supportStateBlocksPromotion : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def TheseusBookCrosswalkImportPointerOnly
    (summary : TheseusBookCrosswalkImportSummary) : Prop :=
  summary.triggerGreen = true ∧
    summary.sourceSyncSmokePassed = true ∧
      summary.publicSafeEvidenceSmokePassed = true ∧
        summary.theseusToBookEvidenceCount = 53 ∧
          summary.roadmapBacklogItemCount = 20 ∧
            summary.sourceSyncReviewDecisionCount = 134 ∧
              summary.publicReportPointerRows = 46 ∧
                summary.publicSourceOrConfigPointerRows = 7 ∧
                  summary.pointerOnlySupportRows = 53 ∧
                    summary.missingSourceBasisCount = 0 ∧
                      summary.donePhaseMissingEvidenceCount = 0 ∧
                        summary.newSupportStateArgument = true ∧
                          summary.supportStateBlocksPromotion = true

def TheseusBookCrosswalkImportPublicSafe
    (summary : TheseusBookCrosswalkImportSummary) : Prop :=
  summary.rawReportCopied = false ∧
    summary.privatePayloadCopied = false ∧
      summary.pathFieldsRedacted = true ∧
        summary.publicTrainingRowsWritten = 0 ∧
          summary.externalInferenceCalls = 0 ∧
            summary.fallbackReturnCount = 0

def TheseusBookCrosswalkImportPreservesBoundaries
    (summary : TheseusBookCrosswalkImportSummary) : Prop :=
  summary.chapterCorePromotion = false ∧
    summary.cleanLiveReplayClaimed = false ∧
      summary.deploymentClaim = false ∧
        summary.modelQualityClaim = false ∧
          summary.capabilityClaim = false ∧
            summary.nonClaimBoundaryRecorded = true

def TheseusBookCrosswalkImportValid
    (summary : TheseusBookCrosswalkImportSummary) : Prop :=
  TheseusBookCrosswalkImportPointerOnly summary ∧
    TheseusBookCrosswalkImportPublicSafe summary ∧
      TheseusBookCrosswalkImportPreservesBoundaries summary

def theseusBookCrosswalkImportFixture :
    TheseusBookCrosswalkImportSummary := {
  triggerGreen := true
  sourceSyncSmokePassed := true
  publicSafeEvidenceSmokePassed := true
  theseusToBookEvidenceCount := 53
  roadmapBacklogItemCount := 20
  sourceSyncReviewDecisionCount := 134
  changedSourceFileCount := 9
  removedSourceFileCount := 0
  stalePhaseCount := 0
  publicReportPointerRows := 46
  publicSourceOrConfigPointerRows := 7
  pointerOnlySupportRows := 53
  missingSourceBasisCount := 0
  donePhaseMissingEvidenceCount := 0
  publicTrainingRowsWritten := 0
  externalInferenceCalls := 0
  fallbackReturnCount := 0
  rawReportCopied := false
  privatePayloadCopied := false
  pathFieldsRedacted := true
  chapterCorePromotion := false
  cleanLiveReplayClaimed := false
  deploymentClaim := false
  modelQualityClaim := false
  capabilityClaim := false
  newSupportStateArgument := true
  supportStateBlocksPromotion := true
  nonClaimBoundaryRecorded := true
}

theorem theseus_book_crosswalk_import_fixture_valid :
    TheseusBookCrosswalkImportValid
      theseusBookCrosswalkImportFixture := by
  simp [
    TheseusBookCrosswalkImportValid,
    TheseusBookCrosswalkImportPointerOnly,
    TheseusBookCrosswalkImportPublicSafe,
    TheseusBookCrosswalkImportPreservesBoundaries,
    theseusBookCrosswalkImportFixture,
  ]

theorem theseus_book_crosswalk_import_pointer_only_preserves_argument :
    theseusBookCrosswalkImportFixture.pointerOnlySupportRows = 53 ∧
      theseusBookCrosswalkImportFixture.newSupportStateArgument = true ∧
      theseusBookCrosswalkImportFixture.supportStateBlocksPromotion = true := by
  simp [theseusBookCrosswalkImportFixture]

theorem theseus_book_crosswalk_import_source_sync_failure_rejected :
    ¬ TheseusBookCrosswalkImportValid
      { theseusBookCrosswalkImportFixture with
        sourceSyncSmokePassed := false } := by
  intro valid
  simp [
    TheseusBookCrosswalkImportValid,
    TheseusBookCrosswalkImportPointerOnly,
    TheseusBookCrosswalkImportPublicSafe,
    TheseusBookCrosswalkImportPreservesBoundaries,
    theseusBookCrosswalkImportFixture,
  ] at valid

theorem theseus_book_crosswalk_import_public_safety_failure_rejected :
    ¬ TheseusBookCrosswalkImportValid
      { theseusBookCrosswalkImportFixture with
        publicTrainingRowsWritten := 1 } := by
  intro valid
  simp [
    TheseusBookCrosswalkImportValid,
    TheseusBookCrosswalkImportPointerOnly,
    TheseusBookCrosswalkImportPublicSafe,
    TheseusBookCrosswalkImportPreservesBoundaries,
    theseusBookCrosswalkImportFixture,
  ] at valid

theorem theseus_book_crosswalk_import_core_promotion_rejected :
    ¬ TheseusBookCrosswalkImportValid
      { theseusBookCrosswalkImportFixture with
        chapterCorePromotion := true } := by
  intro valid
  simp [
    TheseusBookCrosswalkImportValid,
    TheseusBookCrosswalkImportPointerOnly,
    TheseusBookCrosswalkImportPublicSafe,
    TheseusBookCrosswalkImportPreservesBoundaries,
    theseusBookCrosswalkImportFixture,
  ] at valid

theorem theseus_book_crosswalk_import_clean_replay_overclaim_rejected :
    ¬ TheseusBookCrosswalkImportValid
      { theseusBookCrosswalkImportFixture with
        cleanLiveReplayClaimed := true } := by
  intro valid
  simp [
    TheseusBookCrosswalkImportValid,
    TheseusBookCrosswalkImportPointerOnly,
    TheseusBookCrosswalkImportPublicSafe,
    TheseusBookCrosswalkImportPreservesBoundaries,
    theseusBookCrosswalkImportFixture,
  ] at valid

structure TheseusWorkBoardImportSummary where
  taskRows : Nat
  eventRows : Nat
  evidenceRows : Nat
  sqliteTables : Nat
  executionLedgerRows : Nat
  unattendedImprovementRows : Nat
  feedbackRows : Nat
  externalInferenceCalls : Nat
  publicTrainingRowsWritten : Nat
  rawReportsCopied : Bool
  sqlitePayloadCopied : Bool
  taskPayloadsCopied : Bool
  privatePayloadCopied : Bool
  pathFieldsRedacted : Bool
  staleSnapshotImport : Bool
  staleStatusBlocksCurrentnessClaim : Bool
  boardStepExecutedByImport : Bool
  cleanLiveReplayClaimed : Bool
  freshCurrentnessClaimed : Bool
  chapterCorePromotion : Bool
  modelQualityClaim : Bool
  deploymentClaim : Bool
  capabilityClaim : Bool
  unattendedSafetyClaim : Bool
  selfEvolutionSafetyClaim : Bool
  newSupportStateArgument : Bool
  supportStateBlocksPromotion : Bool
  nonClaimBoundaryRecorded : Bool
deriving DecidableEq, Repr

def TheseusWorkBoardImportMetadataOnly
    (summary : TheseusWorkBoardImportSummary) : Prop :=
  summary.taskRows = 130 ∧
    summary.eventRows = 412 ∧
      summary.evidenceRows = 133 ∧
        summary.sqliteTables = 5 ∧
          summary.executionLedgerRows = 1 ∧
            summary.unattendedImprovementRows = 4 ∧
              summary.feedbackRows = 72 ∧
                summary.staleSnapshotImport = true ∧
                  summary.staleStatusBlocksCurrentnessClaim = true ∧
                    summary.boardStepExecutedByImport = false ∧
                      summary.newSupportStateArgument = true ∧
                        summary.supportStateBlocksPromotion = true

def TheseusWorkBoardImportPublicSafe
    (summary : TheseusWorkBoardImportSummary) : Prop :=
  summary.externalInferenceCalls = 0 ∧
    summary.publicTrainingRowsWritten = 0 ∧
      summary.rawReportsCopied = false ∧
        summary.sqlitePayloadCopied = false ∧
          summary.taskPayloadsCopied = false ∧
            summary.privatePayloadCopied = false ∧
              summary.pathFieldsRedacted = true

def TheseusWorkBoardImportPreservesBoundaries
    (summary : TheseusWorkBoardImportSummary) : Prop :=
  summary.cleanLiveReplayClaimed = false ∧
    summary.freshCurrentnessClaimed = false ∧
      summary.chapterCorePromotion = false ∧
        summary.modelQualityClaim = false ∧
          summary.deploymentClaim = false ∧
            summary.capabilityClaim = false ∧
              summary.unattendedSafetyClaim = false ∧
                summary.selfEvolutionSafetyClaim = false ∧
                  summary.nonClaimBoundaryRecorded = true

def TheseusWorkBoardImportValid
    (summary : TheseusWorkBoardImportSummary) : Prop :=
  TheseusWorkBoardImportMetadataOnly summary ∧
    TheseusWorkBoardImportPublicSafe summary ∧
      TheseusWorkBoardImportPreservesBoundaries summary

def theseusWorkBoardImportFixture :
    TheseusWorkBoardImportSummary := {
  taskRows := 130
  eventRows := 412
  evidenceRows := 133
  sqliteTables := 5
  executionLedgerRows := 1
  unattendedImprovementRows := 4
  feedbackRows := 72
  externalInferenceCalls := 0
  publicTrainingRowsWritten := 0
  rawReportsCopied := false
  sqlitePayloadCopied := false
  taskPayloadsCopied := false
  privatePayloadCopied := false
  pathFieldsRedacted := true
  staleSnapshotImport := true
  staleStatusBlocksCurrentnessClaim := true
  boardStepExecutedByImport := false
  cleanLiveReplayClaimed := false
  freshCurrentnessClaimed := false
  chapterCorePromotion := false
  modelQualityClaim := false
  deploymentClaim := false
  capabilityClaim := false
  unattendedSafetyClaim := false
  selfEvolutionSafetyClaim := false
  newSupportStateArgument := true
  supportStateBlocksPromotion := true
  nonClaimBoundaryRecorded := true
}

theorem theseus_work_board_import_fixture_valid :
    TheseusWorkBoardImportValid
      theseusWorkBoardImportFixture := by
  simp [
    TheseusWorkBoardImportValid,
    TheseusWorkBoardImportMetadataOnly,
    TheseusWorkBoardImportPublicSafe,
    TheseusWorkBoardImportPreservesBoundaries,
    theseusWorkBoardImportFixture,
  ]

theorem theseus_work_board_import_stale_snapshot_blocks_currentness :
    theseusWorkBoardImportFixture.staleSnapshotImport = true ∧
      theseusWorkBoardImportFixture.staleStatusBlocksCurrentnessClaim = true ∧
      theseusWorkBoardImportFixture.freshCurrentnessClaimed = false := by
  simp [theseusWorkBoardImportFixture]

theorem theseus_work_board_import_clean_replay_overclaim_rejected :
    ¬ TheseusWorkBoardImportValid
      { theseusWorkBoardImportFixture with
        cleanLiveReplayClaimed := true } := by
  intro valid
  simp [
    TheseusWorkBoardImportValid,
    TheseusWorkBoardImportMetadataOnly,
    TheseusWorkBoardImportPublicSafe,
    TheseusWorkBoardImportPreservesBoundaries,
    theseusWorkBoardImportFixture,
  ] at valid

theorem theseus_work_board_import_private_payload_rejected :
    ¬ TheseusWorkBoardImportValid
      { theseusWorkBoardImportFixture with
        privatePayloadCopied := true } := by
  intro valid
  simp [
    TheseusWorkBoardImportValid,
    TheseusWorkBoardImportMetadataOnly,
    TheseusWorkBoardImportPublicSafe,
    TheseusWorkBoardImportPreservesBoundaries,
    theseusWorkBoardImportFixture,
  ] at valid

theorem theseus_work_board_import_core_promotion_rejected :
    ¬ TheseusWorkBoardImportValid
      { theseusWorkBoardImportFixture with
        chapterCorePromotion := true } := by
  intro valid
  simp [
    TheseusWorkBoardImportValid,
    TheseusWorkBoardImportMetadataOnly,
    TheseusWorkBoardImportPublicSafe,
    TheseusWorkBoardImportPreservesBoundaries,
    theseusWorkBoardImportFixture,
  ] at valid

theorem theseus_work_board_import_public_training_rows_rejected :
    ¬ TheseusWorkBoardImportValid
      { theseusWorkBoardImportFixture with
        publicTrainingRowsWritten := 1 } := by
  intro valid
  simp [
    TheseusWorkBoardImportValid,
    TheseusWorkBoardImportMetadataOnly,
    TheseusWorkBoardImportPublicSafe,
    TheseusWorkBoardImportPreservesBoundaries,
    theseusWorkBoardImportFixture,
  ] at valid

end AsiStackProofs.TheseusReference

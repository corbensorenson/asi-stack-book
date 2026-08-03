namespace AsiStackProofs.LivingBook

structure ChapterManifestReview where
  chapterInManifest : Bool
  outlineProofTargetsPresent : Bool
  claimPlaceholdersGenerated : Bool
deriving DecidableEq, Repr

def ManifestChapterHasDraftingArtifacts (review : ChapterManifestReview) : Prop :=
  review.chapterInManifest = true ->
    review.outlineProofTargetsPresent = true ∧
      review.claimPlaceholdersGenerated = true

theorem manifest_chapter_missing_outline_targets_or_claim_placeholders_rejected
    {review : ChapterManifestReview} :
    review.chapterInManifest = true ->
    (review.outlineProofTargetsPresent = false ∨
      review.claimPlaceholdersGenerated = false) ->
    ¬ ManifestChapterHasDraftingArtifacts review := by
  intro inManifest missing valid
  unfold ManifestChapterHasDraftingArtifacts at valid
  have artifacts := valid inManifest
  cases artifacts with
  | intro outlinePresent claimPlaceholdersPresent =>
      cases missing with
      | inl outlineMissing =>
          rw [outlineMissing] at outlinePresent
          contradiction
      | inr claimsMissing =>
          rw [claimsMissing] at claimPlaceholdersPresent
          contradiction

structure StructuralUpdateReview where
  structuralUpdate : Bool
  scaffoldRegenerated : Bool
  proofManifestRegenerated : Bool
  updateMarkedValid : Bool
deriving DecidableEq, Repr

def StructuralUpdateValid (review : StructuralUpdateReview) : Prop :=
  review.structuralUpdate = true ->
    review.updateMarkedValid = true ->
      review.scaffoldRegenerated = true ∧
        review.proofManifestRegenerated = true

theorem structural_update_marked_valid_without_sync_artifacts_rejected
    {review : StructuralUpdateReview} :
    review.structuralUpdate = true ->
    review.updateMarkedValid = true ->
    (review.scaffoldRegenerated = false ∨
      review.proofManifestRegenerated = false) ->
    ¬ StructuralUpdateValid review := by
  intro structural validUpdate missing valid
  unfold StructuralUpdateValid at valid
  have artifacts := valid structural validUpdate
  cases artifacts with
  | intro scaffold proofManifest =>
      cases missing with
      | inl scaffoldMissing =>
          rw [scaffoldMissing] at scaffold
          contradiction
      | inr proofManifestMissing =>
          rw [proofManifestMissing] at proofManifest
          contradiction

structure ReleaseReadinessReview where
  releaseMarkedReady : Bool
  renderValidated : Bool
  validationCommandsRecorded : Bool
  changelogRefsPresent : Bool
  residualsRecorded : Bool
deriving DecidableEq, Repr

def ReleaseReadinessValid (review : ReleaseReadinessReview) : Prop :=
  review.releaseMarkedReady = true ->
    review.renderValidated = true ∧
      review.validationCommandsRecorded = true ∧
        review.changelogRefsPresent = true ∧
          review.residualsRecorded = true

theorem release_ready_without_validation_changelog_or_residuals_rejected
    {review : ReleaseReadinessReview} :
    review.releaseMarkedReady = true ->
    (review.renderValidated = false ∨
      review.validationCommandsRecorded = false ∨
        review.changelogRefsPresent = false ∨
          review.residualsRecorded = false) ->
    ¬ ReleaseReadinessValid review := by
  intro ready missing valid
  unfold ReleaseReadinessValid at valid
  have complete := valid ready
  cases complete with
  | intro renderValid commandsAndRest =>
      cases commandsAndRest with
      | intro commandsRecorded changelogAndResiduals =>
          cases changelogAndResiduals with
          | intro changelogPresent residualsPresent =>
              cases missing with
              | inl renderMissing =>
                  rw [renderMissing] at renderValid
                  contradiction
              | inr commandsOrRest =>
                  cases commandsOrRest with
                  | inl commandsMissing =>
                      rw [commandsMissing] at commandsRecorded
                      contradiction
                  | inr changelogOrResiduals =>
                      cases changelogOrResiduals with
                      | inl changelogMissing =>
                          rw [changelogMissing] at changelogPresent
                          contradiction
                      | inr residualsMissing =>
                          rw [residualsMissing] at residualsPresent
                          contradiction

structure DerivedArtifactReview where
  derivedArtifactPublished : Bool
  sourceCommitRecorded : Bool
  stripPolicyRecorded : Bool
  reviewStateRecorded : Bool
  supportStateEffectRecorded : Bool
deriving DecidableEq, Repr

def DerivedArtifactPublicationValid
    (review : DerivedArtifactReview) : Prop :=
  review.derivedArtifactPublished = true ->
    review.sourceCommitRecorded = true ∧
      review.stripPolicyRecorded = true ∧
        review.reviewStateRecorded = true ∧
          review.supportStateEffectRecorded = true

theorem derived_artifact_without_source_review_or_support_boundary_rejected
    {review : DerivedArtifactReview} :
    review.derivedArtifactPublished = true ->
    (review.sourceCommitRecorded = false ∨
      review.stripPolicyRecorded = false ∨
        review.reviewStateRecorded = false ∨
          review.supportStateEffectRecorded = false) ->
    ¬ DerivedArtifactPublicationValid review := by
  intro published missing valid
  unfold DerivedArtifactPublicationValid at valid
  have complete := valid published
  cases complete with
  | intro sourceCommit stripAndRest =>
      cases stripAndRest with
      | intro stripPolicy reviewAndSupport =>
          cases reviewAndSupport with
          | intro reviewState supportEffect =>
              cases missing with
              | inl sourceMissing =>
                  rw [sourceMissing] at sourceCommit
                  contradiction
              | inr stripOrRest =>
                  cases stripOrRest with
                  | inl stripMissing =>
                      rw [stripMissing] at stripPolicy
                      contradiction
                  | inr reviewOrSupport =>
                      cases reviewOrSupport with
                      | inl reviewMissing =>
                          rw [reviewMissing] at reviewState
                          contradiction
                      | inr supportMissing =>
                          rw [supportMissing] at supportEffect
                          contradiction

structure ChangePacketReview where
  publicSurfaceChange : Bool
  validationCommandsRecorded : Bool
  changelogRefsPresent : Bool
  supportStateEffectRecorded : Bool
  nonClaimsRecorded : Bool
  derivedArtifactTarget : Bool
  derivedArtifactBoundaryRecorded : Bool
  readerArtifactEqualAuthority : Bool
  supportPromotionClaimed : Bool
  evidenceTransitionRefsPresent : Bool
deriving DecidableEq, Repr

def ChangePacketValid (review : ChangePacketReview) : Prop :=
  review.publicSurfaceChange = true ->
    review.validationCommandsRecorded = true ∧
      review.changelogRefsPresent = true ∧
        review.supportStateEffectRecorded = true ∧
          review.nonClaimsRecorded = true ∧
            (review.derivedArtifactTarget = true ->
              review.derivedArtifactBoundaryRecorded = true ∧
                review.readerArtifactEqualAuthority = false) ∧
              (review.supportPromotionClaimed = true ->
                review.evidenceTransitionRefsPresent = true)

theorem change_packet_public_surface_records_required_boundaries
    {review : ChangePacketReview} :
    ChangePacketValid review ->
    review.publicSurfaceChange = true ->
    review.validationCommandsRecorded = true ∧
      review.changelogRefsPresent = true ∧
        review.supportStateEffectRecorded = true ∧
          review.nonClaimsRecorded = true := by
  intro valid surfaceChange
  have complete := valid surfaceChange
  cases complete with
  | intro commands changelogAndRest =>
      cases changelogAndRest with
      | intro changelog supportAndRest =>
          cases supportAndRest with
          | intro support nonClaimsAndRest =>
              cases nonClaimsAndRest with
              | intro nonClaims _ =>
                  exact ⟨commands, changelog, support, nonClaims⟩

theorem change_packet_without_validation_changelog_support_or_nonclaims_rejected
    {review : ChangePacketReview} :
    review.publicSurfaceChange = true ->
    (review.validationCommandsRecorded = false ∨
      review.changelogRefsPresent = false ∨
        review.supportStateEffectRecorded = false ∨
          review.nonClaimsRecorded = false) ->
    ¬ ChangePacketValid review := by
  intro surfaceChange missing valid
  have required :=
    change_packet_public_surface_records_required_boundaries valid surfaceChange
  cases required with
  | intro commands changelogAndRest =>
      cases changelogAndRest with
      | intro changelog supportAndRest =>
          cases supportAndRest with
          | intro support nonClaims =>
              cases missing with
              | inl commandsMissing =>
                  rw [commandsMissing] at commands
                  contradiction
              | inr changelogOrRest =>
                  cases changelogOrRest with
                  | inl changelogMissing =>
                      rw [changelogMissing] at changelog
                      contradiction
                  | inr supportOrNonClaims =>
                      cases supportOrNonClaims with
                      | inl supportMissing =>
                          rw [supportMissing] at support
                          contradiction
                      | inr nonClaimsMissing =>
                          rw [nonClaimsMissing] at nonClaims
                          contradiction

theorem derived_artifact_equal_authority_change_packet_rejected
    {review : ChangePacketReview} :
    review.publicSurfaceChange = true ->
    review.derivedArtifactTarget = true ->
    review.readerArtifactEqualAuthority = true ->
    ¬ ChangePacketValid review := by
  intro surfaceChange derivedTarget equalAuthority valid
  unfold ChangePacketValid at valid
  have complete := valid surfaceChange
  cases complete with
  | intro _ changelogAndRest =>
      cases changelogAndRest with
      | intro _ supportAndRest =>
          cases supportAndRest with
          | intro _ nonClaimsAndRest =>
              cases nonClaimsAndRest with
              | intro _ derivedAndPromotion =>
                  cases derivedAndPromotion with
                  | intro derivedBoundary _ =>
                      have boundary := derivedBoundary derivedTarget
                      cases boundary with
                      | intro _ notEqual =>
                          rw [equalAuthority] at notEqual
                          contradiction

theorem support_promotion_without_evidence_transition_rejected
    {review : ChangePacketReview} :
    review.publicSurfaceChange = true ->
    review.supportPromotionClaimed = true ->
    review.evidenceTransitionRefsPresent = false ->
    ¬ ChangePacketValid review := by
  intro surfaceChange promotion noEvidence valid
  unfold ChangePacketValid at valid
  have complete := valid surfaceChange
  cases complete with
  | intro _ changelogAndRest =>
      cases changelogAndRest with
      | intro _ supportAndRest =>
          cases supportAndRest with
          | intro _ nonClaimsAndRest =>
              cases nonClaimsAndRest with
              | intro _ derivedAndPromotion =>
                  cases derivedAndPromotion with
                  | intro _ promotionBoundary =>
                      have evidence := promotionBoundary promotion
                      rw [noEvidence] at evidence
                      contradiction

inductive ReaderReleaseCandidateRoute where
  | requestArtifactReview
  | requestAccessibilityReview
  | requestAudioArtifactReview
  | requestReleaseApproval
  | rejectSupportPromotion
  | approveRelease
deriving DecidableEq, Repr

structure ReaderReleaseCandidateReview where
  htmlRendered : Bool
  epubRendered : Bool
  docxRendered : Bool
  pdfRendered : Bool
  htmlBrowserReviewed : Bool
  epubApplicationReviewed : Bool
  docxApplicationReviewed : Bool
  pdfPageReviewed : Bool
  finalFigureReviewed : Bool
  chapterReconciliationApproved : Bool
  keyboardOnlyReviewed : Bool
  accessibilityTreeReviewed : Bool
  screenReaderReviewed : Bool
  wcagConformanceReviewed : Bool
  audioFilesGenerated : Bool
  audioListeningReviewed : Bool
  chapterMarkersTimecoded : Bool
  audioEmbeddedEpubChecked : Bool
  audioReleaseRecordCreated : Bool
  readerReleaseApprovalRecorded : Bool
  approvedEditionReleaseRecordCreated : Bool
  chapterSupportPromotionClaimed : Bool
  nonClaimsRecorded : Bool
  releaseBlockersRecorded : Bool
deriving DecidableEq, Repr

def ReaderReleaseCandidateLocalReviewComplete
    (review : ReaderReleaseCandidateReview) : Bool :=
  review.htmlRendered &&
    review.epubRendered &&
      review.docxRendered &&
        review.pdfRendered &&
          review.htmlBrowserReviewed &&
            review.epubApplicationReviewed &&
              review.docxApplicationReviewed &&
                review.pdfPageReviewed &&
                  review.finalFigureReviewed &&
                    review.chapterReconciliationApproved &&
                      review.keyboardOnlyReviewed &&
                        review.accessibilityTreeReviewed &&
                          review.nonClaimsRecorded &&
                            review.releaseBlockersRecorded

def ReaderReleaseCandidateAccessibilityComplete
    (review : ReaderReleaseCandidateReview) : Bool :=
  review.screenReaderReviewed && review.wcagConformanceReviewed

def ReaderReleaseCandidateAudioComplete
    (review : ReaderReleaseCandidateReview) : Bool :=
  review.audioFilesGenerated &&
    review.audioListeningReviewed &&
      review.chapterMarkersTimecoded &&
        review.audioEmbeddedEpubChecked &&
          review.audioReleaseRecordCreated

def ReaderReleaseCandidateApprovalComplete
    (review : ReaderReleaseCandidateReview) : Bool :=
  review.readerReleaseApprovalRecorded &&
    review.approvedEditionReleaseRecordCreated

def ReaderReleaseCandidateRouteFor
    (review : ReaderReleaseCandidateReview) : ReaderReleaseCandidateRoute :=
  if review.chapterSupportPromotionClaimed = true then
    ReaderReleaseCandidateRoute.rejectSupportPromotion
  else if ReaderReleaseCandidateLocalReviewComplete review = false then
    ReaderReleaseCandidateRoute.requestArtifactReview
  else if ReaderReleaseCandidateAccessibilityComplete review = false then
    ReaderReleaseCandidateRoute.requestAccessibilityReview
  else if ReaderReleaseCandidateAudioComplete review = false then
    ReaderReleaseCandidateRoute.requestAudioArtifactReview
  else if ReaderReleaseCandidateApprovalComplete review = false then
    ReaderReleaseCandidateRoute.requestReleaseApproval
  else
    ReaderReleaseCandidateRoute.approveRelease

theorem local_reader_artifacts_do_not_clear_missing_accessibility_review
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    ReaderReleaseCandidateAccessibilityComplete review = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestAccessibilityReview := by
  intro noPromotion localComplete missingAccessibility
  unfold ReaderReleaseCandidateRouteFor
  simp [noPromotion, localComplete, missingAccessibility]

theorem reader_release_candidate_missing_screen_reader_routes_to_accessibility_review
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    review.screenReaderReviewed = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestAccessibilityReview := by
  intro noPromotion localComplete missingScreenReader
  unfold ReaderReleaseCandidateRouteFor ReaderReleaseCandidateAccessibilityComplete
  simp [noPromotion, localComplete, missingScreenReader]

theorem reader_release_candidate_missing_wcag_routes_to_accessibility_review
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    review.wcagConformanceReviewed = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestAccessibilityReview := by
  intro noPromotion localComplete missingWcag
  unfold ReaderReleaseCandidateRouteFor ReaderReleaseCandidateAccessibilityComplete
  simp [noPromotion, localComplete, missingWcag]

theorem reader_release_candidate_missing_audio_routes_to_audio_review
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    ReaderReleaseCandidateAccessibilityComplete review = true ->
    ReaderReleaseCandidateAudioComplete review = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestAudioArtifactReview := by
  intro noPromotion localComplete accessibilityComplete missingAudio
  unfold ReaderReleaseCandidateRouteFor
  simp [noPromotion, localComplete, accessibilityComplete, missingAudio]

theorem reader_release_candidate_missing_audio_files_routes_to_audio_review
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    ReaderReleaseCandidateAccessibilityComplete review = true ->
    review.audioFilesGenerated = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestAudioArtifactReview := by
  intro noPromotion localComplete accessibilityComplete missingAudioFiles
  unfold ReaderReleaseCandidateRouteFor ReaderReleaseCandidateAudioComplete
  simp [
    noPromotion,
    localComplete,
    accessibilityComplete,
    missingAudioFiles,
  ]

theorem reader_release_candidate_missing_chapter_markers_routes_to_audio_review
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    ReaderReleaseCandidateAccessibilityComplete review = true ->
    review.chapterMarkersTimecoded = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestAudioArtifactReview := by
  intro noPromotion localComplete accessibilityComplete missingChapterMarkers
  unfold ReaderReleaseCandidateRouteFor ReaderReleaseCandidateAudioComplete
  simp [
    noPromotion,
    localComplete,
    accessibilityComplete,
    missingChapterMarkers,
  ]

theorem reader_release_candidate_missing_approval_routes_to_release_approval
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    ReaderReleaseCandidateAccessibilityComplete review = true ->
    ReaderReleaseCandidateAudioComplete review = true ->
    ReaderReleaseCandidateApprovalComplete review = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestReleaseApproval := by
  intro noPromotion localComplete accessibilityComplete audioComplete missingApproval
  unfold ReaderReleaseCandidateRouteFor
  simp [
    noPromotion,
    localComplete,
    accessibilityComplete,
    audioComplete,
    missingApproval,
  ]

theorem reader_release_candidate_missing_reader_release_approval_routes_to_release_approval
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    ReaderReleaseCandidateAccessibilityComplete review = true ->
    ReaderReleaseCandidateAudioComplete review = true ->
    review.readerReleaseApprovalRecorded = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestReleaseApproval := by
  intro noPromotion localComplete accessibilityComplete audioComplete missingApproval
  unfold ReaderReleaseCandidateRouteFor ReaderReleaseCandidateApprovalComplete
  simp [
    noPromotion,
    localComplete,
    accessibilityComplete,
    audioComplete,
    missingApproval,
  ]

theorem reader_release_candidate_missing_approved_record_routes_to_release_approval
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = false ->
    ReaderReleaseCandidateLocalReviewComplete review = true ->
    ReaderReleaseCandidateAccessibilityComplete review = true ->
    ReaderReleaseCandidateAudioComplete review = true ->
    review.approvedEditionReleaseRecordCreated = false ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.requestReleaseApproval := by
  intro noPromotion localComplete accessibilityComplete audioComplete missingReleaseRecord
  unfold ReaderReleaseCandidateRouteFor ReaderReleaseCandidateApprovalComplete
  simp [
    noPromotion,
    localComplete,
    accessibilityComplete,
    audioComplete,
    missingReleaseRecord,
  ]

theorem reader_release_candidate_support_promotion_claim_rejected
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = true ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.rejectSupportPromotion := by
  intro promotionClaimed
  unfold ReaderReleaseCandidateRouteFor
  simp [promotionClaimed]

structure ManifestChapter where
  stableId : Nat
  partId : Nat
  titleDigest : Nat
deriving DecidableEq, Repr

structure NumberedManifestChapter where
  ordinal : Nat
  stableId : Nat
  partId : Nat
  titleDigest : Nat
deriving DecidableEq, Repr

def numberManifestFrom : Nat -> List ManifestChapter -> List NumberedManifestChapter
  | _, [] => []
  | next, chapter :: rest =>
      {
        ordinal := next
        stableId := chapter.stableId
        partId := chapter.partId
        titleDigest := chapter.titleDigest
      } :: numberManifestFrom (next + 1) rest

def numberManifest (chapters : List ManifestChapter) : List NumberedManifestChapter :=
  numberManifestFrom 1 chapters

def ConsecutiveManifestOrdinals : Nat -> List NumberedManifestChapter -> Prop
  | _, [] => True
  | next, chapter :: rest =>
      chapter.ordinal = next ∧ ConsecutiveManifestOrdinals (next + 1) rest

theorem number_manifest_preserves_length
    (next : Nat) (chapters : List ManifestChapter) :
    (numberManifestFrom next chapters).length = chapters.length := by
  induction chapters generalizing next with
  | nil => rfl
  | cons chapter rest ih =>
      simp [numberManifestFrom, ih]

theorem number_manifest_preserves_stable_id_order
    (next : Nat) (chapters : List ManifestChapter) :
    (numberManifestFrom next chapters).map (fun chapter => chapter.stableId) =
      chapters.map (fun chapter => chapter.stableId) := by
  induction chapters generalizing next with
  | nil => rfl
  | cons chapter rest ih =>
      simp [numberManifestFrom, ih]

theorem number_manifest_derives_consecutive_ordinals
    (next : Nat) (chapters : List ManifestChapter) :
    ConsecutiveManifestOrdinals next (numberManifestFrom next chapters) := by
  induction chapters generalizing next with
  | nil => trivial
  | cons chapter rest ih =>
      simp [numberManifestFrom, ConsecutiveManifestOrdinals, ih]

inductive ManifestChangeStage where
  | proposed
  | structureSynced
  | evidenceSynced
  | validated
  | acceptedCurrent
  | rolledBack
deriving DecidableEq, Repr, BEq

structure ManifestChangeState where
  stage : ManifestChangeStage
  changeDigest : Nat
  expectedChangeDigest : Nat
  priorManifestDigest : Nat
  candidateManifestDigest : Nat
  expectedCandidateManifestDigest : Nat
  priorChapterCount : Nat
  candidateChapterCount : Nat
  renderedChapterCount : Nat
  stableIdsUnique : Bool
  scaffoldSynced : Bool
  outlineSynced : Bool
  proofManifestSynced : Bool
  sourceMatrixSynced : Bool
  renderValidated : Bool
  validatorsPassed : Bool
  changelogRecorded : Bool
  nonClaimsRecorded : Bool
  receipts : Nat
  authorityCeiling : Nat
  expectedAuthorityCeiling : Nat
  supportAssignments : Nat
  publicationEffects : Nat
deriving DecidableEq, Repr

inductive ManifestChangeEvent where
  | synchronizeStructure
      (changeDigest candidateManifestDigest renderedChapterCount : Nat)
      (stableIdsUnique : Bool)
  | synchronizeEvidence
      (changeDigest : Nat)
      (outlineSynced proofManifestSynced sourceMatrixSynced : Bool)
  | validateCurrent
      (changeDigest : Nat)
      (renderValidated validatorsPassed : Bool)
  | acceptCurrent
      (changeDigest : Nat)
      (changelogRecorded nonClaimsRecorded : Bool)
  | rollback
      (changeDigest : Nat)
      (residualOwned : Bool)
deriving DecidableEq, Repr

def ManifestChangeCustody (state : ManifestChangeState) : Prop :=
  state.changeDigest = state.expectedChangeDigest ∧
    state.candidateManifestDigest = state.expectedCandidateManifestDigest ∧
      state.authorityCeiling = state.expectedAuthorityCeiling

def ManifestChangeInvariant (state : ManifestChangeState) : Prop :=
  ManifestChangeCustody state ∧
    state.supportAssignments = 0 ∧
      state.publicationEffects = 0 ∧
        match state.stage with
        | .proposed => True
        | .structureSynced =>
            state.stableIdsUnique = true ∧
              state.scaffoldSynced = true ∧
                state.renderedChapterCount = state.candidateChapterCount
        | .evidenceSynced =>
            state.stableIdsUnique = true ∧
              state.scaffoldSynced = true ∧
                state.renderedChapterCount = state.candidateChapterCount ∧
                  state.outlineSynced = true ∧
                    state.proofManifestSynced = true ∧
                      state.sourceMatrixSynced = true
        | .validated =>
            state.stableIdsUnique = true ∧
              state.scaffoldSynced = true ∧
                state.renderedChapterCount = state.candidateChapterCount ∧
                  state.outlineSynced = true ∧
                    state.proofManifestSynced = true ∧
                      state.sourceMatrixSynced = true ∧
                        state.renderValidated = true ∧
                          state.validatorsPassed = true
        | .acceptedCurrent =>
            state.stableIdsUnique = true ∧
              state.scaffoldSynced = true ∧
                state.renderedChapterCount = state.candidateChapterCount ∧
                  state.outlineSynced = true ∧
                    state.proofManifestSynced = true ∧
                      state.sourceMatrixSynced = true ∧
                        state.renderValidated = true ∧
                          state.validatorsPassed = true ∧
                            state.changelogRecorded = true ∧
                              state.nonClaimsRecorded = true
        | .rolledBack => True

def manifestChangeStep
    (state : ManifestChangeState) (event : ManifestChangeEvent) :
    Bool × ManifestChangeState :=
  match event with
  | .synchronizeStructure change candidate rendered unique =>
      if state.stage = .proposed ∧
          change = state.changeDigest ∧
          candidate = state.candidateManifestDigest ∧
          candidate = state.expectedCandidateManifestDigest ∧
          rendered = state.candidateChapterCount ∧
          unique = true then
        (true, {
          state with
          stage := .structureSynced
          renderedChapterCount := rendered
          stableIdsUnique := true
          scaffoldSynced := true
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .synchronizeEvidence change outline proofManifest sourceMatrix =>
      if state.stage = .structureSynced ∧
          change = state.changeDigest ∧
          outline = true ∧ proofManifest = true ∧ sourceMatrix = true then
        (true, {
          state with
          stage := .evidenceSynced
          outlineSynced := true
          proofManifestSynced := true
          sourceMatrixSynced := true
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .validateCurrent change renderPassed validatorsPassed =>
      if state.stage = .evidenceSynced ∧
          change = state.changeDigest ∧
          renderPassed = true ∧ validatorsPassed = true then
        (true, {
          state with
          stage := .validated
          renderValidated := true
          validatorsPassed := true
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .acceptCurrent change changelog nonClaims =>
      if state.stage = .validated ∧
          change = state.changeDigest ∧
          changelog = true ∧ nonClaims = true then
        (true, {
          state with
          stage := .acceptedCurrent
          changelogRecorded := true
          nonClaimsRecorded := true
          receipts := state.receipts + 1
        })
      else
        (false, state)
  | .rollback change residualOwned =>
      if state.stage ≠ .acceptedCurrent ∧
          state.stage ≠ .rolledBack ∧
          change = state.changeDigest ∧ residualOwned = true then
        (true, {
          state with
          stage := .rolledBack
          candidateManifestDigest := state.priorManifestDigest
          expectedCandidateManifestDigest := state.priorManifestDigest
          candidateChapterCount := state.priorChapterCount
          renderedChapterCount := state.priorChapterCount
          receipts := state.receipts + 1
        })
      else
        (false, state)

def runManifestChange :
    ManifestChangeState -> List ManifestChangeEvent -> ManifestChangeState
  | state, [] => state
  | state, event :: rest =>
      runManifestChange (manifestChangeStep state event).2 rest

def referenceManifestChange : ManifestChangeState := {
  stage := .proposed
  changeDigest := 701
  expectedChangeDigest := 701
  priorManifestDigest := 800
  candidateManifestDigest := 801
  expectedCandidateManifestDigest := 801
  priorChapterCount := 83
  candidateChapterCount := 84
  renderedChapterCount := 0
  stableIdsUnique := false
  scaffoldSynced := false
  outlineSynced := false
  proofManifestSynced := false
  sourceMatrixSynced := false
  renderValidated := false
  validatorsPassed := false
  changelogRecorded := false
  nonClaimsRecorded := false
  receipts := 0
  authorityCeiling := 1
  expectedAuthorityCeiling := 1
  supportAssignments := 0
  publicationEffects := 0
}

def referenceManifestChangeEvents : List ManifestChangeEvent := [
  .synchronizeStructure 701 801 84 true,
  .synchronizeEvidence 701 true true true,
  .validateCurrent 701 true true,
  .acceptCurrent 701 true true
]

theorem manifest_change_rejected_event_is_noninterfering
    (state : ManifestChangeState) (event : ManifestChangeEvent)
    (h : (manifestChangeStep state event).1 = false) :
    (manifestChangeStep state event).2 = state := by
  cases event with
  | synchronizeStructure change candidate rendered unique =>
      by_cases gate : state.stage = .proposed ∧
        change = state.changeDigest ∧
        candidate = state.candidateManifestDigest ∧
        candidate = state.expectedCandidateManifestDigest ∧
        rendered = state.candidateChapterCount ∧ unique = true
      · have candidateEq :
          state.candidateManifestDigest = state.expectedCandidateManifestDigest :=
            gate.2.2.1.symm.trans gate.2.2.2.1
        simp [manifestChangeStep, gate, candidateEq] at h
      · simp [manifestChangeStep, gate]
  | synchronizeEvidence change outline proofManifest sourceMatrix =>
      by_cases gate : state.stage = .structureSynced ∧
        change = state.changeDigest ∧
        outline = true ∧ proofManifest = true ∧ sourceMatrix = true
      · simp [manifestChangeStep, gate] at h
      · simp [manifestChangeStep, gate]
  | validateCurrent change renderPassed validatorsPassed =>
      by_cases gate : state.stage = .evidenceSynced ∧
        change = state.changeDigest ∧
        renderPassed = true ∧ validatorsPassed = true
      · simp [manifestChangeStep, gate] at h
      · simp [manifestChangeStep, gate]
  | acceptCurrent change changelog nonClaims =>
      by_cases gate : state.stage = .validated ∧
        change = state.changeDigest ∧
        changelog = true ∧ nonClaims = true
      · simp [manifestChangeStep, gate] at h
      · simp [manifestChangeStep, gate]
  | rollback change residualOwned =>
      by_cases gate : state.stage ≠ .acceptedCurrent ∧
        state.stage ≠ .rolledBack ∧
        change = state.changeDigest ∧ residualOwned = true
      · simp [manifestChangeStep, gate] at h
      · simp [manifestChangeStep, gate]

theorem manifest_change_step_preserves_custody
    (state : ManifestChangeState) (event : ManifestChangeEvent)
    (h : ManifestChangeCustody state) :
    ManifestChangeCustody (manifestChangeStep state event).2 := by
  cases event <;>
    simp [manifestChangeStep, ManifestChangeCustody] at h ⊢ <;>
    split <;> simp_all

theorem run_manifest_change_preserves_custody
    (state : ManifestChangeState) (events : List ManifestChangeEvent)
    (h : ManifestChangeCustody state) :
    ManifestChangeCustody (runManifestChange state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (manifestChangeStep state event).2
        (manifest_change_step_preserves_custody state event h)

theorem manifest_change_step_preserves_invariant
    (state : ManifestChangeState) (event : ManifestChangeEvent)
    (h : ManifestChangeInvariant state) :
    ManifestChangeInvariant (manifestChangeStep state event).2 := by
  cases event <;>
    simp [manifestChangeStep, ManifestChangeInvariant, ManifestChangeCustody] at h ⊢ <;>
    split <;> simp_all

theorem run_manifest_change_preserves_invariant
    (state : ManifestChangeState) (events : List ManifestChangeEvent)
    (h : ManifestChangeInvariant state) :
    ManifestChangeInvariant (runManifestChange state events) := by
  induction events generalizing state with
  | nil => exact h
  | cons event rest ih =>
      exact ih (manifestChangeStep state event).2
        (manifest_change_step_preserves_invariant state event h)

theorem run_manifest_change_append
    (state : ManifestChangeState)
    (left right : List ManifestChangeEvent) :
    runManifestChange state (left ++ right) =
      runManifestChange (runManifestChange state left) right := by
  induction left generalizing state with
  | nil => rfl
  | cons event rest ih =>
      simp [runManifestChange, ih]

theorem reference_manifest_change_reaches_accepted_current :
    (runManifestChange referenceManifestChange referenceManifestChangeEvents).stage =
      .acceptedCurrent := by
  rfl

theorem reference_manifest_change_has_no_support_or_publication_authority :
    let final := runManifestChange referenceManifestChange referenceManifestChangeEvents
    final.supportAssignments = 0 ∧ final.publicationEffects = 0 := by
  decide

theorem reference_manifest_change_has_exact_receipt_count :
    (runManifestChange referenceManifestChange referenceManifestChangeEvents).receipts = 4 := by
  rfl

theorem missing_proof_manifest_sync_rejects_without_state_change :
    let synchronized := (manifestChangeStep referenceManifestChange
      (.synchronizeStructure 701 801 84 true)).2
    manifestChangeStep synchronized (.synchronizeEvidence 701 true false true) =
      (false, synchronized) := by
  decide

theorem duplicate_stable_ids_reject_structure_sync_without_state_change :
    manifestChangeStep referenceManifestChange
      (.synchronizeStructure 701 801 84 false) =
        (false, referenceManifestChange) := by
  decide

theorem failed_render_rejects_validation_without_state_change :
    let synchronized := runManifestChange referenceManifestChange
      (referenceManifestChangeEvents.take 2)
    manifestChangeStep synchronized (.validateCurrent 701 false true) =
      (false, synchronized) := by
  decide

theorem accepted_manifest_change_is_absorbing_one_step
    (state : ManifestChangeState) (event : ManifestChangeEvent)
    (h : state.stage = .acceptedCurrent) :
    manifestChangeStep state event = (false, state) := by
  cases event <;> simp [manifestChangeStep, h]

theorem rolled_back_manifest_change_is_absorbing_one_step
    (state : ManifestChangeState) (event : ManifestChangeEvent)
    (h : state.stage = .rolledBack) :
    manifestChangeStep state event = (false, state) := by
  cases event <;> simp [manifestChangeStep, h]

theorem accepted_manifest_change_is_absorbing_for_any_suffix
    (state : ManifestChangeState) (events : List ManifestChangeEvent)
    (h : state.stage = .acceptedCurrent) :
    runManifestChange state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      rw [show runManifestChange state (event :: rest) =
        runManifestChange (manifestChangeStep state event).2 rest by rfl]
      rw [accepted_manifest_change_is_absorbing_one_step state event h]
      exact ih state h

theorem rolled_back_manifest_change_is_absorbing_for_any_suffix
    (state : ManifestChangeState) (events : List ManifestChangeEvent)
    (h : state.stage = .rolledBack) :
    runManifestChange state events = state := by
  induction events generalizing state with
  | nil => rfl
  | cons event rest ih =>
      rw [show runManifestChange state (event :: rest) =
        runManifestChange (manifestChangeStep state event).2 rest by rfl]
      rw [rolled_back_manifest_change_is_absorbing_one_step state event h]
      exact ih state h

def manifestChangeThinSummary (state : ManifestChangeState) : Nat × Nat :=
  (state.candidateManifestDigest, state.candidateChapterCount)

def ManifestChangeAccepted (state : ManifestChangeState) : Prop :=
  state.stage = .acceptedCurrent

def acceptedReferenceManifestChange : ManifestChangeState :=
  runManifestChange referenceManifestChange referenceManifestChangeEvents

theorem manifest_thin_summary_collides_across_acceptance :
    manifestChangeThinSummary acceptedReferenceManifestChange =
        manifestChangeThinSummary referenceManifestChange ∧
      ManifestChangeAccepted acceptedReferenceManifestChange ∧
      ¬ ManifestChangeAccepted referenceManifestChange := by
  simp [manifestChangeThinSummary, acceptedReferenceManifestChange,
    ManifestChangeAccepted, runManifestChange, referenceManifestChangeEvents,
    referenceManifestChange, manifestChangeStep]

theorem no_manifest_thin_summary_classifier_recovers_acceptance :
    ¬ ∃ classify : Nat × Nat -> Bool,
      ∀ state : ManifestChangeState,
        classify (manifestChangeThinSummary state) = true ↔
          ManifestChangeAccepted state := by
  intro proposed
  rcases proposed with ⟨classify, exactResult⟩
  have collision := manifest_thin_summary_collides_across_acceptance
  have accepted := (exactResult acceptedReferenceManifestChange).2 collision.2.1
  have proposedRejected := (exactResult referenceManifestChange).1
  rw [collision.1] at accepted
  exact collision.2.2 (proposedRejected accepted)

end AsiStackProofs.LivingBook

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

theorem every_manifest_chapter_has_outline_targets_and_claim_placeholders
    {review : ChapterManifestReview} :
    ManifestChapterHasDraftingArtifacts review ->
    review.chapterInManifest = true ->
    review.outlineProofTargetsPresent = true ∧
      review.claimPlaceholdersGenerated = true := by
  intro valid inManifest
  exact valid inManifest

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

theorem structural_update_without_regenerated_scaffold_and_proof_manifest_is_invalid
    {review : StructuralUpdateReview} :
    StructuralUpdateValid review ->
    review.structuralUpdate = true ->
    review.updateMarkedValid = true ->
    review.scaffoldRegenerated = true ∧
      review.proofManifestRegenerated = true := by
  intro valid structural validUpdate
  exact valid structural validUpdate

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

def curatedReaderBlockedCandidateFixture : ReaderReleaseCandidateReview := {
  htmlRendered := true,
  epubRendered := true,
  docxRendered := true,
  pdfRendered := true,
  htmlBrowserReviewed := true,
  epubApplicationReviewed := true,
  docxApplicationReviewed := true,
  pdfPageReviewed := true,
  finalFigureReviewed := true,
  chapterReconciliationApproved := true,
  keyboardOnlyReviewed := true,
  accessibilityTreeReviewed := true,
  screenReaderReviewed := false,
  wcagConformanceReviewed := false,
  audioFilesGenerated := false,
  audioListeningReviewed := false,
  chapterMarkersTimecoded := false,
  audioEmbeddedEpubChecked := false,
  audioReleaseRecordCreated := false,
  readerReleaseApprovalRecorded := false,
  approvedEditionReleaseRecordCreated := false,
  chapterSupportPromotionClaimed := false,
  nonClaimsRecorded := true,
  releaseBlockersRecorded := true
}

theorem curated_reader_blocked_candidate_fixture_routes_to_accessibility_review :
    ReaderReleaseCandidateRouteFor curatedReaderBlockedCandidateFixture =
      ReaderReleaseCandidateRoute.requestAccessibilityReview := by
  rfl

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

theorem reader_release_candidate_support_promotion_claim_rejected
    {review : ReaderReleaseCandidateReview} :
    review.chapterSupportPromotionClaimed = true ->
      ReaderReleaseCandidateRouteFor review =
        ReaderReleaseCandidateRoute.rejectSupportPromotion := by
  intro promotionClaimed
  unfold ReaderReleaseCandidateRouteFor
  simp [promotionClaimed]

end AsiStackProofs.LivingBook

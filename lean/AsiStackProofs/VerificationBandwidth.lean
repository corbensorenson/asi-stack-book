namespace AsiStackProofs.VerificationBandwidth

inductive AdequacyState where
  | unknown
  | adequateForDrafting
  | adequateForLocalCheck
  | inadequateForVerification
  | escalated
deriving DecidableEq, Repr

structure ContextPacketReview where
  packetAdmitted : Bool
  adequacyState : AdequacyState
deriving DecidableEq, Repr

theorem admitted_context_packet_may_still_be_marked_inadequate :
    ∃ review : ContextPacketReview,
      review.packetAdmitted = true ∧
        review.adequacyState = AdequacyState.inadequateForVerification := by
  exact ⟨{
    packetAdmitted := true,
    adequacyState := AdequacyState.inadequateForVerification
  }, rfl, rfl⟩

structure ClaimSupportReview where
  highRiskClaim : Bool
  contextInadequate : Bool
  verifiedSupportAssigned : Bool
deriving DecidableEq, Repr

def InadequateContextBlocksVerifiedSupport
    (review : ClaimSupportReview) : Prop :=
  review.highRiskClaim = true ->
    review.contextInadequate = true ->
      review.verifiedSupportAssigned = false

theorem high_risk_claim_with_inadequate_context_cannot_receive_verified_support
    {review : ClaimSupportReview} :
    InadequateContextBlocksVerifiedSupport review ->
    review.highRiskClaim = true ->
    review.contextInadequate = true ->
    review.verifiedSupportAssigned = false := by
  intro valid highRisk inadequate
  exact valid highRisk inadequate

inductive VerificationAdequacyRoute where
  | rejectClaim
  | requestContext
  | requirePairwiseCheck
  | requireVerificationArtifacts
  | escalateRisk
  | blockVerifiedSupport
  | recordResidual
  | allowDraftSupport
  | allowVerifiedSupport
deriving DecidableEq, Repr

structure VerificationAdequacyReview where
  claimPresent : Bool
  contextAdmitted : Bool
  contextAdequateForClaim : Bool
  highRiskClaim : Bool
  pairwiseCheckRequired : Bool
  pairwiseCheckComplete : Bool
  verificationArtifactsPresent : Bool
  negativeEvidenceOpen : Bool
  contradictionDetected : Bool
  residualKnown : Bool
  draftSupportRequested : Bool
  verifiedSupportRequested : Bool
deriving DecidableEq, Repr

def VerificationAdequacyRouteFor
    (review : VerificationAdequacyReview) : VerificationAdequacyRoute :=
  if review.claimPresent = false then
    VerificationAdequacyRoute.rejectClaim
  else if review.contextAdmitted = false then
    VerificationAdequacyRoute.requestContext
  else if review.highRiskClaim = true ∧
      review.contextAdequateForClaim = false then
    VerificationAdequacyRoute.blockVerifiedSupport
  else if review.pairwiseCheckRequired = true ∧
      review.pairwiseCheckComplete = false then
    VerificationAdequacyRoute.requirePairwiseCheck
  else if review.verifiedSupportRequested = true ∧
      review.verificationArtifactsPresent = false then
    VerificationAdequacyRoute.requireVerificationArtifacts
  else if review.negativeEvidenceOpen = true then
    VerificationAdequacyRoute.escalateRisk
  else if review.contradictionDetected = true then
    VerificationAdequacyRoute.blockVerifiedSupport
  else if review.residualKnown = true then
    VerificationAdequacyRoute.recordResidual
  else if review.verifiedSupportRequested = true then
    VerificationAdequacyRoute.allowVerifiedSupport
  else if review.draftSupportRequested = true then
    VerificationAdequacyRoute.allowDraftSupport
  else
    VerificationAdequacyRoute.requestContext

theorem missing_claim_rejects_verification_adequacy_review
    {review : VerificationAdequacyReview} :
    review.claimPresent = false ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.rejectClaim := by
  intro missingClaim
  unfold VerificationAdequacyRouteFor
  simp [missingClaim]

theorem unadmitted_context_requests_context
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = false ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.requestContext := by
  intro claimPresent contextNotAdmitted
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextNotAdmitted]

theorem high_risk_inadequate_context_blocks_verified_route
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = true ->
    review.highRiskClaim = true ->
    review.contextAdequateForClaim = false ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.blockVerifiedSupport := by
  intro claimPresent contextAdmitted highRisk inadequateContext
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextAdmitted, highRisk, inadequateContext]

theorem missing_pairwise_check_requires_pairwise_check
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = true ->
    review.highRiskClaim = false ->
    review.pairwiseCheckRequired = true ->
    review.pairwiseCheckComplete = false ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.requirePairwiseCheck := by
  intro claimPresent contextAdmitted notHighRisk pairwiseRequired
    pairwiseMissing
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextAdmitted, notHighRisk, pairwiseRequired,
    pairwiseMissing]

theorem missing_verification_artifacts_require_artifacts
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = true ->
    review.highRiskClaim = false ->
    review.pairwiseCheckRequired = false ->
    review.verifiedSupportRequested = true ->
    review.verificationArtifactsPresent = false ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.requireVerificationArtifacts := by
  intro claimPresent contextAdmitted notHighRisk pairwiseNotRequired
    verifiedRequested artifactsMissing
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextAdmitted, notHighRisk, pairwiseNotRequired,
    verifiedRequested, artifactsMissing]

theorem open_negative_evidence_escalates_risk
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = true ->
    review.highRiskClaim = false ->
    review.pairwiseCheckRequired = false ->
    review.verifiedSupportRequested = false ->
    review.negativeEvidenceOpen = true ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.escalateRisk := by
  intro claimPresent contextAdmitted notHighRisk pairwiseNotRequired
    verifiedNotRequested negativeEvidence
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextAdmitted, notHighRisk, pairwiseNotRequired,
    verifiedNotRequested, negativeEvidence]

theorem detected_contradiction_blocks_verified_support_route
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = true ->
    review.highRiskClaim = false ->
    review.pairwiseCheckRequired = false ->
    review.verifiedSupportRequested = false ->
    review.negativeEvidenceOpen = false ->
    review.contradictionDetected = true ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.blockVerifiedSupport := by
  intro claimPresent contextAdmitted notHighRisk pairwiseNotRequired
    verifiedNotRequested noNegativeEvidence contradiction
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextAdmitted, notHighRisk, pairwiseNotRequired,
    verifiedNotRequested, noNegativeEvidence, contradiction]

theorem known_verification_residual_records_residual
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = true ->
    review.highRiskClaim = false ->
    review.pairwiseCheckRequired = false ->
    review.verifiedSupportRequested = false ->
    review.negativeEvidenceOpen = false ->
    review.contradictionDetected = false ->
    review.residualKnown = true ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.recordResidual := by
  intro claimPresent contextAdmitted notHighRisk pairwiseNotRequired
    verifiedNotRequested noNegativeEvidence noContradiction residualKnown
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextAdmitted, notHighRisk, pairwiseNotRequired,
    verifiedNotRequested, noNegativeEvidence, noContradiction, residualKnown]

theorem complete_verified_review_allows_verified_support
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = true ->
    review.contextAdequateForClaim = true ->
    review.highRiskClaim = true ->
    review.pairwiseCheckRequired = true ->
    review.pairwiseCheckComplete = true ->
    review.verifiedSupportRequested = true ->
    review.verificationArtifactsPresent = true ->
    review.negativeEvidenceOpen = false ->
    review.contradictionDetected = false ->
    review.residualKnown = false ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.allowVerifiedSupport := by
  intro claimPresent contextAdmitted contextAdequate highRisk
    pairwiseRequired pairwiseComplete verifiedRequested artifactsPresent
    noNegativeEvidence noContradiction noResidual
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextAdmitted, contextAdequate, highRisk,
    pairwiseRequired, pairwiseComplete, verifiedRequested, artifactsPresent,
    noNegativeEvidence, noContradiction, noResidual]

theorem complete_draft_review_allows_draft_support
    {review : VerificationAdequacyReview} :
    review.claimPresent = true ->
    review.contextAdmitted = true ->
    review.highRiskClaim = false ->
    review.pairwiseCheckRequired = false ->
    review.verifiedSupportRequested = false ->
    review.negativeEvidenceOpen = false ->
    review.contradictionDetected = false ->
    review.residualKnown = false ->
    review.draftSupportRequested = true ->
    VerificationAdequacyRouteFor review =
      VerificationAdequacyRoute.allowDraftSupport := by
  intro claimPresent contextAdmitted notHighRisk pairwiseNotRequired
    verifiedNotRequested noNegativeEvidence noContradiction noResidual
    draftRequested
  unfold VerificationAdequacyRouteFor
  simp [claimPresent, contextAdmitted, notHighRisk, pairwiseNotRequired,
    verifiedNotRequested, noNegativeEvidence, noContradiction, noResidual,
    draftRequested]

structure ContradictionProbeSummary where
  validContradictionTracePresent : Bool
  draftingOnlyTracePresent : Bool
  negativeControlsRejected : Bool
  supportStateEffectNone : Bool
  nonClaimBoundary : Bool
deriving DecidableEq, Repr

def ContradictionProbeSummaryValid
    (summary : ContradictionProbeSummary) : Prop :=
  summary.validContradictionTracePresent = true ∧
    summary.draftingOnlyTracePresent = true ∧
    summary.negativeControlsRejected = true ∧
    summary.supportStateEffectNone = true ∧
    summary.nonClaimBoundary = true

theorem verification_bandwidth_contradiction_probe_fixture_bridge
    {summary : ContradictionProbeSummary} :
    ContradictionProbeSummaryValid summary ->
      summary.validContradictionTracePresent = true ∧
        summary.draftingOnlyTracePresent = true ∧
        summary.negativeControlsRejected = true ∧
        summary.supportStateEffectNone = true ∧
        summary.nonClaimBoundary = true := by
  intro valid
  exact valid

end AsiStackProofs.VerificationBandwidth

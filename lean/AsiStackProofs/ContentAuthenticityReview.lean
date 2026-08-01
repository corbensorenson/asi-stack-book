import AsiStackProofs.CommunicationInfluenceReview

namespace AsiStackProofs.ContentAuthenticityReview

inductive EvidenceKind where
  | signedProvenance
  | watermark
  | statisticalDetector
deriving DecidableEq, Repr

inductive ClaimClass where
  | attributedStatement
  | embeddedSignal
  | distributionRelativeClassification
  | semanticTruth
  | humanOrigin
  | authorship
deriving DecidableEq, Repr

def establishes : EvidenceKind -> ClaimClass -> Bool
  | .signedProvenance, .attributedStatement => true
  | .watermark, .embeddedSignal => true
  | .statisticalDetector, .distributionRelativeClassification => true
  | _, _ => false

theorem signed_provenance_does_not_establish_semantic_truth :
    establishes .signedProvenance .semanticTruth = false := by rfl

theorem watermark_absence_does_not_establish_human_origin :
    establishes .watermark .humanOrigin = false := by rfl

theorem detector_output_does_not_establish_authorship :
    establishes .statisticalDetector .authorship = false := by rfl

structure TransformationObservation where
  transformationId : Nat
  checked : Bool
deriving DecidableEq, Repr

def checkTransformation (observation : TransformationObservation) : TransformationObservation :=
  { observation with checked := true }

def checkAllTransformations : List TransformationObservation -> List TransformationObservation
  | [] => []
  | observation :: rest => checkTransformation observation :: checkAllTransformations rest

def AllTransformationsChecked (observations : List TransformationObservation) : Prop :=
  forall observation, observation ∈ observations -> observation.checked = true

theorem check_all_covers_every_finite_transformation
    (observations : List TransformationObservation) :
    AllTransformationsChecked (checkAllTransformations observations) := by
  intro observation member
  induction observations with
  | nil => simp [checkAllTransformations] at member
  | cons head tail ih =>
      simp only [checkAllTransformations, List.mem_cons] at member
      rcases member with same | inTail
      · subst observation
        simp [checkTransformation]
      · exact ih inTail

structure AuthenticityEnvelope where
  assetIdentityBound : Bool := true
  renditionIdentityBound : Bool := true
  claimIdentityBound : Bool := true
  signerIdentityBound : Bool := true
  trustPolicyIdentityBound : Bool := true
  evidenceTypesSeparated : Bool := true
  signedClaimRecorded : Bool := true
  contentBindingChecked : Bool := true
  signatureStatusTyped : Bool := true
  watermarkResultTyped : Bool := true
  fingerprintResultTyped : Bool := true
  detectorResultTyped : Bool := true
  contextualEvidenceTyped : Bool := true
  absenceNonInferenceExplicit : Bool := true
  truthNonInferenceExplicit : Bool := true
  transformationInventoryComplete : Bool := true
  unsupportedTransformationBreakExplicit : Bool := true
  compositeRegionsBound : Bool := true
  lineageBreaksVisible : Bool := true
  transformationDigestBound : Bool := true
  trustPolicyVersion : Nat := 3
  authorizedTrustPolicyVersion : Nat := 3
  checkedSignerEpoch : Nat := 4
  currentSignerEpoch : Nat := 4
  currentTick : Nat := 10
  expiresAt : Nat := 20
  evidenceEpochBound : Bool := true
  conflictsPreserved : Bool := true
  uncertaintyRecorded : Bool := true
  disputeRoutePresent : Bool := true
  remedyRoutePresent : Bool := true
  correctionLineagePresent : Bool := true
  affectedPathNotificationPresent : Bool := true
  disclosureTextBound : Bool := true
  disclosureAssetBound : Bool := true
  disclosureAccessible : Bool := true
  comprehensionNotAssumed : Bool := true
  privacyScopeBound : Bool := true
  consentDecisionSeparate : Bool := true
  regulatoryDecisionSeparate : Bool := true
  highImpactActionSeparatelyAuthorized : Bool := true
  originClaimedFromAbsence : Bool := false
  semanticTruthClaimed : Bool := false
  legalComplianceClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def TrustPolicyCurrent (d : AuthenticityEnvelope) : Prop :=
  d.trustPolicyVersion = d.authorizedTrustPolicyVersion

def SignerStatusCurrent (d : AuthenticityEnvelope) : Prop :=
  d.checkedSignerEpoch = d.currentSignerEpoch

def NotExpired (d : AuthenticityEnvelope) : Prop := d.currentTick <= d.expiresAt

instance trustPolicyCurrentDecidable (d : AuthenticityEnvelope) :
    Decidable (TrustPolicyCurrent d) := by unfold TrustPolicyCurrent; infer_instance
instance signerStatusCurrentDecidable (d : AuthenticityEnvelope) :
    Decidable (SignerStatusCurrent d) := by unfold SignerStatusCurrent; infer_instance
instance notExpiredDecidable (d : AuthenticityEnvelope) : Decidable (NotExpired d) := by
  unfold NotExpired; infer_instance

def IdentityComplete (d : AuthenticityEnvelope) : Prop :=
  d.assetIdentityBound = true ∧ d.renditionIdentityBound = true ∧
  d.claimIdentityBound = true ∧ d.signerIdentityBound = true ∧
  d.trustPolicyIdentityBound = true

def EvidenceComplete (d : AuthenticityEnvelope) : Prop :=
  d.evidenceTypesSeparated = true ∧ d.signedClaimRecorded = true ∧
  d.contentBindingChecked = true ∧ d.signatureStatusTyped = true ∧
  d.watermarkResultTyped = true ∧ d.fingerprintResultTyped = true ∧
  d.detectorResultTyped = true ∧ d.contextualEvidenceTyped = true ∧
  d.absenceNonInferenceExplicit = true ∧ d.truthNonInferenceExplicit = true

def TransformationComplete (d : AuthenticityEnvelope) : Prop :=
  d.transformationInventoryComplete = true ∧
  d.unsupportedTransformationBreakExplicit = true ∧
  d.compositeRegionsBound = true ∧ d.lineageBreaksVisible = true ∧
  d.transformationDigestBound = true

def TrustComplete (d : AuthenticityEnvelope) : Prop :=
  TrustPolicyCurrent d ∧ SignerStatusCurrent d ∧ NotExpired d ∧
  d.evidenceEpochBound = true

def ConflictComplete (d : AuthenticityEnvelope) : Prop :=
  d.conflictsPreserved = true ∧ d.uncertaintyRecorded = true ∧
  d.disputeRoutePresent = true ∧ d.remedyRoutePresent = true ∧
  d.correctionLineagePresent = true ∧ d.affectedPathNotificationPresent = true

def DisclosureComplete (d : AuthenticityEnvelope) : Prop :=
  d.disclosureTextBound = true ∧ d.disclosureAssetBound = true ∧
  d.disclosureAccessible = true ∧ d.comprehensionNotAssumed = true ∧
  d.privacyScopeBound = true

def BoundaryComplete (d : AuthenticityEnvelope) : Prop :=
  d.consentDecisionSeparate = true ∧ d.regulatoryDecisionSeparate = true ∧
  d.highImpactActionSeparatelyAuthorized = true ∧
  d.originClaimedFromAbsence = false ∧ d.semanticTruthClaimed = false ∧
  d.legalComplianceClaimed = false ∧ d.supportOrReleaseRequested = false

instance identityCompleteDecidable (d : AuthenticityEnvelope) :
    Decidable (IdentityComplete d) := by unfold IdentityComplete; infer_instance
instance evidenceCompleteDecidable (d : AuthenticityEnvelope) :
    Decidable (EvidenceComplete d) := by unfold EvidenceComplete; infer_instance
instance transformationCompleteDecidable (d : AuthenticityEnvelope) :
    Decidable (TransformationComplete d) := by unfold TransformationComplete; infer_instance
instance trustCompleteDecidable (d : AuthenticityEnvelope) : Decidable (TrustComplete d) := by
  unfold TrustComplete TrustPolicyCurrent SignerStatusCurrent NotExpired; infer_instance
instance conflictCompleteDecidable (d : AuthenticityEnvelope) :
    Decidable (ConflictComplete d) := by unfold ConflictComplete; infer_instance
instance disclosureCompleteDecidable (d : AuthenticityEnvelope) :
    Decidable (DisclosureComplete d) := by unfold DisclosureComplete; infer_instance
instance boundaryCompleteDecidable (d : AuthenticityEnvelope) :
    Decidable (BoundaryComplete d) := by unfold BoundaryComplete; infer_instance

def EnvelopeAdmissible (d : AuthenticityEnvelope) : Prop :=
  IdentityComplete d ∧ EvidenceComplete d ∧ TransformationComplete d ∧ TrustComplete d ∧
  ConflictComplete d ∧ DisclosureComplete d ∧ BoundaryComplete d

instance envelopeAdmissibleDecidable (d : AuthenticityEnvelope) :
    Decidable (EnvelopeAdmissible d) := by
  unfold EnvelopeAdmissible IdentityComplete EvidenceComplete TransformationComplete
    TrustComplete TrustPolicyCurrent SignerStatusCurrent NotExpired ConflictComplete
    DisclosureComplete BoundaryComplete
  infer_instance

def EnvelopeReady (d : AuthenticityEnvelope) : Bool := decide (EnvelopeAdmissible d)

inductive ReviewState where
  | proposed
  | identityReviewed
  | evidenceReviewed
  | transformationsReviewed
  | trustReviewed
  | conflictsReviewed
  | disclosureReviewed
  | boundaryReviewed
  | repairRequired
  | eligibleForTheseusAuthenticityCampaign
deriving DecidableEq, Repr

def ReviewStepFor (d : AuthenticityEnvelope) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (EvidenceComplete d) then .evidenceReviewed else .repairRequired
  | .evidenceReviewed =>
      if decide (TransformationComplete d) then .transformationsReviewed else .repairRequired
  | .transformationsReviewed => if decide (TrustComplete d) then .trustReviewed else .repairRequired
  | .trustReviewed => if decide (ConflictComplete d) then .conflictsReviewed else .repairRequired
  | .conflictsReviewed =>
      if decide (DisclosureComplete d) then .disclosureReviewed else .repairRequired
  | .disclosureReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusAuthenticityCampaign
  | state => state

def ReviewRun (d : AuthenticityEnvelope) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : AuthenticityEnvelope) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .evidenceReviewed => IdentityComplete d ∧ EvidenceComplete d
  | .transformationsReviewed =>
      IdentityComplete d ∧ EvidenceComplete d ∧ TransformationComplete d
  | .trustReviewed =>
      IdentityComplete d ∧ EvidenceComplete d ∧ TransformationComplete d ∧ TrustComplete d
  | .conflictsReviewed =>
      IdentityComplete d ∧ EvidenceComplete d ∧ TransformationComplete d ∧ TrustComplete d ∧
      ConflictComplete d
  | .disclosureReviewed =>
      IdentityComplete d ∧ EvidenceComplete d ∧ TransformationComplete d ∧ TrustComplete d ∧
      ConflictComplete d ∧ DisclosureComplete d
  | .boundaryReviewed | .eligibleForTheseusAuthenticityCampaign => EnvelopeAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : AuthenticityEnvelope) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case evidenceReviewed => split <;> simp_all [StageInvariant]
  case transformationsReviewed => split <;> simp_all [StageInvariant]
  case trustReviewed => split <;> simp_all [StageInvariant]
  case conflictsReviewed => split <;> simp_all [StageInvariant]
  case disclosureReviewed => split <;> simp_all [StageInvariant, EnvelopeAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : AuthenticityEnvelope) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem campaign_eligibility_requires_admissible_envelope
    (d : AuthenticityEnvelope) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusAuthenticityCampaign) :
    EnvelopeAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeEnvelope : AuthenticityEnvelope := {}

theorem complete_envelope_is_ready : EnvelopeReady completeEnvelope = true := by decide

theorem complete_envelope_reaches_only_authenticity_campaign :
    ReviewRun completeEnvelope 8 = .eligibleForTheseusAuthenticityCampaign := by decide

inductive AdmissionAxis where
  | assetIdentity | renditionIdentity | claimIdentity | signerIdentity | trustPolicyIdentity
  | evidenceTypeSeparation | signedClaim | contentBinding | signatureStatus | watermarkResult
  | fingerprintResult | detectorResult | contextualEvidence | absenceNonInference
  | truthNonInference | transformationInventory | unsupportedTransformationBreak
  | compositeRegions | lineageBreakVisibility | transformationDigest | trustPolicyVersion
  | signerRevocationEpoch | expiry | evidenceEpoch | conflictPreservation | uncertainty
  | disputeRoute | remedyRoute | correctionLineage | affectedPathNotification
  | disclosureText | disclosureAsset | disclosureAccessibility | comprehensionBoundary
  | privacyScope | consentSeparation | regulatorySeparation | highImpactAuthorization
  | originFromAbsence | semanticTruth | legalCompliance | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> AuthenticityEnvelope
  | .assetIdentity => { completeEnvelope with assetIdentityBound := false }
  | .renditionIdentity => { completeEnvelope with renditionIdentityBound := false }
  | .claimIdentity => { completeEnvelope with claimIdentityBound := false }
  | .signerIdentity => { completeEnvelope with signerIdentityBound := false }
  | .trustPolicyIdentity => { completeEnvelope with trustPolicyIdentityBound := false }
  | .evidenceTypeSeparation => { completeEnvelope with evidenceTypesSeparated := false }
  | .signedClaim => { completeEnvelope with signedClaimRecorded := false }
  | .contentBinding => { completeEnvelope with contentBindingChecked := false }
  | .signatureStatus => { completeEnvelope with signatureStatusTyped := false }
  | .watermarkResult => { completeEnvelope with watermarkResultTyped := false }
  | .fingerprintResult => { completeEnvelope with fingerprintResultTyped := false }
  | .detectorResult => { completeEnvelope with detectorResultTyped := false }
  | .contextualEvidence => { completeEnvelope with contextualEvidenceTyped := false }
  | .absenceNonInference => { completeEnvelope with absenceNonInferenceExplicit := false }
  | .truthNonInference => { completeEnvelope with truthNonInferenceExplicit := false }
  | .transformationInventory => { completeEnvelope with transformationInventoryComplete := false }
  | .unsupportedTransformationBreak =>
      { completeEnvelope with unsupportedTransformationBreakExplicit := false }
  | .compositeRegions => { completeEnvelope with compositeRegionsBound := false }
  | .lineageBreakVisibility => { completeEnvelope with lineageBreaksVisible := false }
  | .transformationDigest => { completeEnvelope with transformationDigestBound := false }
  | .trustPolicyVersion => { completeEnvelope with trustPolicyVersion := 4 }
  | .signerRevocationEpoch => { completeEnvelope with currentSignerEpoch := 5 }
  | .expiry => { completeEnvelope with currentTick := 21 }
  | .evidenceEpoch => { completeEnvelope with evidenceEpochBound := false }
  | .conflictPreservation => { completeEnvelope with conflictsPreserved := false }
  | .uncertainty => { completeEnvelope with uncertaintyRecorded := false }
  | .disputeRoute => { completeEnvelope with disputeRoutePresent := false }
  | .remedyRoute => { completeEnvelope with remedyRoutePresent := false }
  | .correctionLineage => { completeEnvelope with correctionLineagePresent := false }
  | .affectedPathNotification =>
      { completeEnvelope with affectedPathNotificationPresent := false }
  | .disclosureText => { completeEnvelope with disclosureTextBound := false }
  | .disclosureAsset => { completeEnvelope with disclosureAssetBound := false }
  | .disclosureAccessibility => { completeEnvelope with disclosureAccessible := false }
  | .comprehensionBoundary => { completeEnvelope with comprehensionNotAssumed := false }
  | .privacyScope => { completeEnvelope with privacyScopeBound := false }
  | .consentSeparation => { completeEnvelope with consentDecisionSeparate := false }
  | .regulatorySeparation => { completeEnvelope with regulatoryDecisionSeparate := false }
  | .highImpactAuthorization =>
      { completeEnvelope with highImpactActionSeparatelyAuthorized := false }
  | .originFromAbsence => { completeEnvelope with originClaimedFromAbsence := true }
  | .semanticTruth => { completeEnvelope with semanticTruthClaimed := true }
  | .legalCompliance => { completeEnvelope with legalComplianceClaimed := true }
  | .supportOrRelease => { completeEnvelope with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindAssetIdentity | bindRenditionIdentity | bindClaimIdentity | bindSignerIdentity
  | bindTrustPolicyIdentity | separateEvidenceTypes | recordSignedClaim | checkContentBinding
  | typeSignatureStatus | typeWatermarkResult | typeFingerprintResult | typeDetectorResult
  | typeContextualEvidence | recordAbsenceNonInference | recordTruthNonInference
  | completeTransformationInventory | recordUnsupportedTransformationBreak
  | bindCompositeRegions | exposeLineageBreaks | bindTransformationDigest
  | reopenForTrustPolicyVersion | refreshSignerRevocationEpoch | renewExpiry
  | bindEvidenceEpoch | preserveConflicts | recordUncertainty | addDisputeRoute
  | addRemedyRoute | addCorrectionLineage | addAffectedPathNotification
  | bindDisclosureText | bindDisclosureAsset | makeDisclosureAccessible
  | prohibitAssumedComprehension | bindPrivacyScope | separateConsentDecision
  | separateRegulatoryDecision | requireHighImpactAuthorization
  | rejectOriginInferenceFromAbsence | rejectSemanticTruth | rejectLegalCompliance
  | refuseSupportOrRelease | eligibleForTheseusAuthenticityCampaign
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .assetIdentity => .bindAssetIdentity
  | .renditionIdentity => .bindRenditionIdentity
  | .claimIdentity => .bindClaimIdentity
  | .signerIdentity => .bindSignerIdentity
  | .trustPolicyIdentity => .bindTrustPolicyIdentity
  | .evidenceTypeSeparation => .separateEvidenceTypes
  | .signedClaim => .recordSignedClaim
  | .contentBinding => .checkContentBinding
  | .signatureStatus => .typeSignatureStatus
  | .watermarkResult => .typeWatermarkResult
  | .fingerprintResult => .typeFingerprintResult
  | .detectorResult => .typeDetectorResult
  | .contextualEvidence => .typeContextualEvidence
  | .absenceNonInference => .recordAbsenceNonInference
  | .truthNonInference => .recordTruthNonInference
  | .transformationInventory => .completeTransformationInventory
  | .unsupportedTransformationBreak => .recordUnsupportedTransformationBreak
  | .compositeRegions => .bindCompositeRegions
  | .lineageBreakVisibility => .exposeLineageBreaks
  | .transformationDigest => .bindTransformationDigest
  | .trustPolicyVersion => .reopenForTrustPolicyVersion
  | .signerRevocationEpoch => .refreshSignerRevocationEpoch
  | .expiry => .renewExpiry
  | .evidenceEpoch => .bindEvidenceEpoch
  | .conflictPreservation => .preserveConflicts
  | .uncertainty => .recordUncertainty
  | .disputeRoute => .addDisputeRoute
  | .remedyRoute => .addRemedyRoute
  | .correctionLineage => .addCorrectionLineage
  | .affectedPathNotification => .addAffectedPathNotification
  | .disclosureText => .bindDisclosureText
  | .disclosureAsset => .bindDisclosureAsset
  | .disclosureAccessibility => .makeDisclosureAccessible
  | .comprehensionBoundary => .prohibitAssumedComprehension
  | .privacyScope => .bindPrivacyScope
  | .consentSeparation => .separateConsentDecision
  | .regulatorySeparation => .separateRegulatoryDecision
  | .highImpactAuthorization => .requireHighImpactAuthorization
  | .originFromAbsence => .rejectOriginInferenceFromAbsence
  | .semanticTruth => .rejectSemanticTruth
  | .legalCompliance => .rejectLegalCompliance
  | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : AuthenticityEnvelope) : RepairDisposition :=
  if !d.assetIdentityBound then .bindAssetIdentity
  else if !d.renditionIdentityBound then .bindRenditionIdentity
  else if !d.claimIdentityBound then .bindClaimIdentity
  else if !d.signerIdentityBound then .bindSignerIdentity
  else if !d.trustPolicyIdentityBound then .bindTrustPolicyIdentity
  else if !d.evidenceTypesSeparated then .separateEvidenceTypes
  else if !d.signedClaimRecorded then .recordSignedClaim
  else if !d.contentBindingChecked then .checkContentBinding
  else if !d.signatureStatusTyped then .typeSignatureStatus
  else if !d.watermarkResultTyped then .typeWatermarkResult
  else if !d.fingerprintResultTyped then .typeFingerprintResult
  else if !d.detectorResultTyped then .typeDetectorResult
  else if !d.contextualEvidenceTyped then .typeContextualEvidence
  else if !d.absenceNonInferenceExplicit then .recordAbsenceNonInference
  else if !d.truthNonInferenceExplicit then .recordTruthNonInference
  else if !d.transformationInventoryComplete then .completeTransformationInventory
  else if !d.unsupportedTransformationBreakExplicit then .recordUnsupportedTransformationBreak
  else if !d.compositeRegionsBound then .bindCompositeRegions
  else if !d.lineageBreaksVisible then .exposeLineageBreaks
  else if !d.transformationDigestBound then .bindTransformationDigest
  else if d.trustPolicyVersion != d.authorizedTrustPolicyVersion then
    .reopenForTrustPolicyVersion
  else if d.checkedSignerEpoch != d.currentSignerEpoch then .refreshSignerRevocationEpoch
  else if !decide (NotExpired d) then .renewExpiry
  else if !d.evidenceEpochBound then .bindEvidenceEpoch
  else if !d.conflictsPreserved then .preserveConflicts
  else if !d.uncertaintyRecorded then .recordUncertainty
  else if !d.disputeRoutePresent then .addDisputeRoute
  else if !d.remedyRoutePresent then .addRemedyRoute
  else if !d.correctionLineagePresent then .addCorrectionLineage
  else if !d.affectedPathNotificationPresent then .addAffectedPathNotification
  else if !d.disclosureTextBound then .bindDisclosureText
  else if !d.disclosureAssetBound then .bindDisclosureAsset
  else if !d.disclosureAccessible then .makeDisclosureAccessible
  else if !d.comprehensionNotAssumed then .prohibitAssumedComprehension
  else if !d.privacyScopeBound then .bindPrivacyScope
  else if !d.consentDecisionSeparate then .separateConsentDecision
  else if !d.regulatoryDecisionSeparate then .separateRegulatoryDecision
  else if !d.highImpactActionSeparatelyAuthorized then .requireHighImpactAuthorization
  else if d.originClaimedFromAbsence then .rejectOriginInferenceFromAbsence
  else if d.semanticTruthClaimed then .rejectSemanticTruth
  else if d.legalComplianceClaimed then .rejectLegalCompliance
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusAuthenticityCampaign

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    EnvelopeReady (omitAxis axis) = false := by cases axis <;> decide

theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide

theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : AuthenticityEnvelope) (h : EnvelopeReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1

theorem readiness_requires_evidence (d : AuthenticityEnvelope) (h : EnvelopeReady d = true) :
    EvidenceComplete d := by exact (of_decide_eq_true h).2.1

theorem readiness_requires_transformations
    (d : AuthenticityEnvelope) (h : EnvelopeReady d = true) : TransformationComplete d := by
  exact (of_decide_eq_true h).2.2.1

theorem readiness_requires_current_trust
    (d : AuthenticityEnvelope) (h : EnvelopeReady d = true) : TrustComplete d := by
  exact (of_decide_eq_true h).2.2.2.1

theorem readiness_requires_conflict_routes
    (d : AuthenticityEnvelope) (h : EnvelopeReady d = true) : ConflictComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.1

theorem readiness_requires_accessible_disclosure
    (d : AuthenticityEnvelope) (h : EnvelopeReady d = true) : DisclosureComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.2.1

theorem readiness_requires_nonclaim_boundary
    (d : AuthenticityEnvelope) (h : EnvelopeReady d = true) : BoundaryComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_envelope_remains_expired_when_time_advances
    (d : AuthenticityEnvelope) (later : Nat) (expired : d.expiresAt < d.currentTick)
    (advances : d.currentTick <= later) : Not (NotExpired { d with currentTick := later }) := by
  intro current
  unfold NotExpired at current
  change later <= d.expiresAt at current
  omega

theorem stale_signer_status_remains_stale_when_current_epoch_advances
    (d : AuthenticityEnvelope) (later : Nat)
    (stale : d.checkedSignerEpoch < d.currentSignerEpoch)
    (advances : d.currentSignerEpoch <= later) :
    Not (SignerStatusCurrent { d with currentSignerEpoch := later }) := by
  intro current
  unfold SignerStatusCurrent at current
  change d.checkedSignerEpoch = later at current
  omega

structure ReceiptScope where
  assetId : Nat
  renditionId : Nat
  trustPolicyVersion : Nat
  transformationDigest : Nat
  signerEpoch : Nat
  expiresAt : Nat
deriving DecidableEq, Repr

def ReceiptUseAllowed (scope : ReceiptScope)
    (asset rendition policy transformation signerEpoch tick : Nat) : Prop :=
  asset = scope.assetId ∧ rendition = scope.renditionId ∧
  policy = scope.trustPolicyVersion ∧ transformation = scope.transformationDigest ∧
  signerEpoch = scope.signerEpoch ∧ tick <= scope.expiresAt

theorem asset_change_invalidates_authenticity_receipt
    (scope : ReceiptScope) (asset : Nat) (different : Not (asset = scope.assetId)) :
    Not (ReceiptUseAllowed scope asset scope.renditionId scope.trustPolicyVersion
      scope.transformationDigest scope.signerEpoch scope.expiresAt) := by
  intro allowed
  exact different allowed.1

theorem trust_policy_change_invalidates_authenticity_receipt
    (scope : ReceiptScope) (policy : Nat)
    (different : Not (policy = scope.trustPolicyVersion)) :
    Not (ReceiptUseAllowed scope scope.assetId scope.renditionId policy
      scope.transformationDigest scope.signerEpoch scope.expiresAt) := by
  intro allowed
  exact different allowed.2.2.1

theorem transformation_change_invalidates_authenticity_receipt
    (scope : ReceiptScope) (transformation : Nat)
    (different : Not (transformation = scope.transformationDigest)) :
    Not (ReceiptUseAllowed scope scope.assetId scope.renditionId scope.trustPolicyVersion
      transformation scope.signerEpoch scope.expiresAt) := by
  intro allowed
  exact different allowed.2.2.2.1

theorem signer_epoch_change_invalidates_authenticity_receipt
    (scope : ReceiptScope) (epoch : Nat) (different : Not (epoch = scope.signerEpoch)) :
    Not (ReceiptUseAllowed scope scope.assetId scope.renditionId scope.trustPolicyVersion
      scope.transformationDigest epoch scope.expiresAt) := by
  intro allowed
  exact different allowed.2.2.2.2.1

inductive TransformationDisposition where
  | verifiedPreservation
  | verifiedDerivation
  | explicitLineageBreak
  | unresolvedRelationship
deriving DecidableEq, Repr

structure TransformationDecision where
  supported : Bool
  inputBindingVerified : Bool
  outputBindingVerified : Bool
  composite : Bool
  regionsBound : Bool
  disposition : TransformationDisposition
deriving DecidableEq, Repr

def TransformationDispositionAllowed (decision : TransformationDecision) : Prop :=
  (decision.disposition = .verifiedPreservation ->
      decision.supported = true ∧ decision.inputBindingVerified = true ∧
      decision.outputBindingVerified = true) ∧
  (decision.composite = true -> decision.regionsBound = true)

theorem unsupported_transformation_cannot_claim_verified_preservation
    (decision : TransformationDecision) (unsupported : decision.supported = false) :
    Not (TransformationDispositionAllowed
      { decision with disposition := .verifiedPreservation }) := by
  intro allowed
  have supported := allowed.1 rfl
  simp [unsupported] at supported

theorem composite_without_region_binding_is_blocked
    (decision : TransformationDecision) (composite : decision.composite = true)
    (unbound : decision.regionsBound = false) :
    Not (TransformationDispositionAllowed decision) := by
  intro allowed
  have regions := allowed.2 composite
  simp [unbound] at regions

structure TechnicalSignals where
  signatureValid : Bool
  bindingIntact : Bool
  watermarkDetected : Bool
  detectorPositive : Bool
  disclosurePresent : Bool
deriving DecidableEq, Repr

structure TruthCase where
  signals : TechnicalSignals
  semanticTruth : Bool
deriving DecidableEq, Repr

def sharedTechnicalSignals : TechnicalSignals :=
  { signatureValid := true, bindingIntact := true, watermarkDetected := true,
    detectorPositive := true, disclosurePresent := true }

def trueClaimCase : TruthCase := { signals := sharedTechnicalSignals, semanticTruth := true }
def falseClaimCase : TruthCase := { signals := sharedTechnicalSignals, semanticTruth := false }

theorem identical_authenticity_signals_can_hide_opposite_truth_state :
    trueClaimCase.signals = falseClaimCase.signals ∧
    trueClaimCase.semanticTruth = true ∧ falseClaimCase.semanticTruth = false := by decide

theorem authenticity_signals_cannot_recover_semantic_truth
    (classify : TechnicalSignals -> Bool) :
    Not (forall c : TruthCase, classify c.signals = c.semanticTruth) := by
  intro exact
  have trueCase := exact trueClaimCase
  have falseCase := exact falseClaimCase
  simp [trueClaimCase, falseClaimCase, sharedTechnicalSignals] at trueCase falseCase
  rw [trueCase] at falseCase
  contradiction

inductive Origin where
  | human
  | synthetic
deriving DecidableEq, Repr

structure AbsenceSignals where
  credentialPresent : Bool
  watermarkDetected : Bool
  detectorPositive : Bool
deriving DecidableEq, Repr

structure OriginCase where
  signals : AbsenceSignals
  origin : Origin
deriving DecidableEq, Repr

def noSignals : AbsenceSignals :=
  { credentialPresent := false, watermarkDetected := false, detectorPositive := false }
def humanWithoutSignals : OriginCase := { signals := noSignals, origin := .human }
def syntheticWithoutSignals : OriginCase := { signals := noSignals, origin := .synthetic }
def IsHumanOrigin (c : OriginCase) : Bool := c.origin == .human

theorem identical_absence_signals_can_hide_opposite_origin :
    humanWithoutSignals.signals = syntheticWithoutSignals.signals ∧
    IsHumanOrigin humanWithoutSignals = true ∧
    IsHumanOrigin syntheticWithoutSignals = false := by decide

theorem absence_signals_cannot_recover_human_origin (classify : AbsenceSignals -> Bool) :
    Not (forall c : OriginCase, classify c.signals = IsHumanOrigin c) := by
  intro exact
  have human := exact humanWithoutSignals
  have synthetic := exact syntheticWithoutSignals
  simp [humanWithoutSignals, syntheticWithoutSignals, noSignals, IsHumanOrigin] at human synthetic
  rw [human] at synthetic
  contradiction

def toRecipientCase (d : AuthenticityEnvelope) :
    CommunicationInfluenceReview.RecipientCase :=
  { provenance :=
      { claimId := 7, sourceVersion := d.trustPolicyVersion, signer := 11 }
    comprehended := false }

def AuthenticityConsumerReady (d : AuthenticityEnvelope) : Bool :=
  d.disclosureAccessible && (toRecipientCase d).comprehended

theorem authenticity_receipt_cannot_substitute_for_recipient_comprehension
    (d : AuthenticityEnvelope) : AuthenticityConsumerReady d = false := by
  simp [AuthenticityConsumerReady, toRecipientCase]

end AsiStackProofs.ContentAuthenticityReview

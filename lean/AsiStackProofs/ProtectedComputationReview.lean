import AsiStackProofs.PrivacyInformationFlow

namespace AsiStackProofs.ProtectedComputationReview

inductive EvidenceKind where
  | remoteAttestation
  | encodedRelationProof
  | confidentialityMechanism
deriving DecidableEq, Repr

inductive ClaimClass where
  | platformIdentity
  | encodedRelation
  | protectedAssetConfidentiality
  | semanticCorrectness
  | authorization
  | endToEndPrivacy
deriving DecidableEq, Repr

def establishes : EvidenceKind -> ClaimClass -> Bool
  | .remoteAttestation, .platformIdentity => true
  | .encodedRelationProof, .encodedRelation => true
  | .confidentialityMechanism, .protectedAssetConfidentiality => true
  | _, _ => false

theorem attestation_does_not_establish_semantic_correctness :
    establishes .remoteAttestation .semanticCorrectness = false := by rfl

theorem encoded_relation_proof_does_not_establish_authorization :
    establishes .encodedRelationProof .authorization = false := by rfl

theorem confidentiality_mechanism_does_not_establish_end_to_end_privacy :
    establishes .confidentialityMechanism .endToEndPrivacy = false := by rfl

structure LeakageObservation where
  channelId : Nat
  accounted : Bool
deriving DecidableEq, Repr

def accountLeakage (observation : LeakageObservation) : LeakageObservation :=
  { observation with accounted := true }

def accountAllLeakage : List LeakageObservation -> List LeakageObservation
  | [] => []
  | observation :: rest => accountLeakage observation :: accountAllLeakage rest

def AllLeakageAccounted (observations : List LeakageObservation) : Prop :=
  forall observation, observation ∈ observations -> observation.accounted = true

theorem account_all_covers_every_finite_leakage_channel
    (observations : List LeakageObservation) :
    AllLeakageAccounted (accountAllLeakage observations) := by
  intro observation member
  induction observations with
  | nil => simp [accountAllLeakage] at member
  | cons head tail ih =>
      simp only [accountAllLeakage, List.mem_cons] at member
      rcases member with same | inTail
      · subst observation
        simp [accountLeakage]
      · exact ih inTail

structure ProtectedExecutionDossier where
  requestIdentityBound : Bool := true
  transactionIdentityBound : Bool := true
  artifactIdentityBound : Bool := true
  modelIdentityBound : Bool := true
  preprocessingIdentityBound : Bool := true
  configurationIdentityBound : Bool := true
  lifecycleStageBound : Bool := true
  adversaryBound : Bool := true
  protectedAssetsBound : Bool := true
  guaranteeVectorSeparated : Bool := true
  trustAssumptionsBound : Bool := true
  constructionIdentityBound : Bool := true
  evidenceStatementBound : Bool := true
  unsupportedPropertiesExplicit : Bool := true
  attesterIdentityBound : Bool := true
  verifierIdentityBound : Bool := true
  relyingPartyIdentityBound : Bool := true
  independentAppraisalPresent : Bool := true
  verifierPolicyBound : Bool := true
  referenceValuesBound : Bool := true
  cryptographicAssumptionsBound : Bool := true
  semanticCorrespondenceResidualPresent : Bool := true
  claimClassesSeparated : Bool := true
  freshnessChallengePresent : Bool := true
  evidenceEpochBound : Bool := true
  revocationStateBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  verifierPolicyVersion : Nat := 3
  authorizedVerifierPolicyVersion : Nat := 3
  observedLeakageUnits : Nat := 3
  permittedLeakageUnits : Nat := 3
  leakageInventoryComplete : Bool := true
  outputLeakageRecorded : Bool := true
  timingLeakageRecorded : Bool := true
  accessPatternLeakageRecorded : Bool := true
  logAndCacheLeakageRecorded : Bool := true
  failureAndMetadataLeakageRecorded : Bool := true
  leakageResidualOwnerPresent : Bool := true
  protectedFailureStateExplicit : Bool := true
  fallbackObservable : Bool := true
  fallbackSeparatelyAuthorized : Bool := true
  silentDowngradeProhibited : Bool := true
  recoveryRoutePresent : Bool := true
  matchedCostRecordPresent : Bool := true
  privacyPurposeHandoffPresent : Bool := true
  weightCustodyHandoffPresent : Bool := true
  semanticCorrectnessClaimed : Bool := false
  authorizationClaimed : Bool := false
  endToEndPrivacyClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : ProtectedExecutionDossier) : Prop := d.currentTick <= d.expiresAt
def PolicyCurrent (d : ProtectedExecutionDossier) : Prop :=
  d.verifierPolicyVersion = d.authorizedVerifierPolicyVersion
def LeakageWithinBound (d : ProtectedExecutionDossier) : Prop :=
  d.observedLeakageUnits <= d.permittedLeakageUnits

instance currentDecidable (d : ProtectedExecutionDossier) : Decidable (Current d) := by
  unfold Current; infer_instance
instance policyCurrentDecidable (d : ProtectedExecutionDossier) : Decidable (PolicyCurrent d) := by
  unfold PolicyCurrent; infer_instance
instance leakageWithinBoundDecidable (d : ProtectedExecutionDossier) :
    Decidable (LeakageWithinBound d) := by
  unfold LeakageWithinBound; infer_instance

def IdentityComplete (d : ProtectedExecutionDossier) : Prop :=
  d.requestIdentityBound = true ∧ d.transactionIdentityBound = true ∧
  d.artifactIdentityBound = true ∧ d.modelIdentityBound = true ∧
  d.preprocessingIdentityBound = true ∧ d.configurationIdentityBound = true ∧
  d.lifecycleStageBound = true

def GuaranteeComplete (d : ProtectedExecutionDossier) : Prop :=
  d.adversaryBound = true ∧ d.protectedAssetsBound = true ∧
  d.guaranteeVectorSeparated = true ∧ d.trustAssumptionsBound = true ∧
  d.constructionIdentityBound = true ∧ d.evidenceStatementBound = true ∧
  d.unsupportedPropertiesExplicit = true

def EvidenceComplete (d : ProtectedExecutionDossier) : Prop :=
  d.attesterIdentityBound = true ∧ d.verifierIdentityBound = true ∧
  d.relyingPartyIdentityBound = true ∧ d.independentAppraisalPresent = true ∧
  d.verifierPolicyBound = true ∧ d.referenceValuesBound = true ∧
  d.cryptographicAssumptionsBound = true ∧
  d.semanticCorrespondenceResidualPresent = true ∧ d.claimClassesSeparated = true

def FreshnessComplete (d : ProtectedExecutionDossier) : Prop :=
  d.freshnessChallengePresent = true ∧ d.evidenceEpochBound = true ∧
  d.revocationStateBound = true ∧ Current d ∧ PolicyCurrent d

def LeakageComplete (d : ProtectedExecutionDossier) : Prop :=
  LeakageWithinBound d ∧ d.leakageInventoryComplete = true ∧
  d.outputLeakageRecorded = true ∧ d.timingLeakageRecorded = true ∧
  d.accessPatternLeakageRecorded = true ∧ d.logAndCacheLeakageRecorded = true ∧
  d.failureAndMetadataLeakageRecorded = true ∧ d.leakageResidualOwnerPresent = true

def FallbackComplete (d : ProtectedExecutionDossier) : Prop :=
  d.protectedFailureStateExplicit = true ∧ d.fallbackObservable = true ∧
  d.fallbackSeparatelyAuthorized = true ∧ d.silentDowngradeProhibited = true ∧
  d.recoveryRoutePresent = true ∧ d.matchedCostRecordPresent = true

def BoundaryComplete (d : ProtectedExecutionDossier) : Prop :=
  d.privacyPurposeHandoffPresent = true ∧ d.weightCustodyHandoffPresent = true ∧
  d.semanticCorrectnessClaimed = false ∧ d.authorizationClaimed = false ∧
  d.endToEndPrivacyClaimed = false ∧ d.supportOrReleaseRequested = false

instance identityCompleteDecidable (d : ProtectedExecutionDossier) :
    Decidable (IdentityComplete d) := by unfold IdentityComplete; infer_instance
instance guaranteeCompleteDecidable (d : ProtectedExecutionDossier) :
    Decidable (GuaranteeComplete d) := by unfold GuaranteeComplete; infer_instance
instance evidenceCompleteDecidable (d : ProtectedExecutionDossier) :
    Decidable (EvidenceComplete d) := by unfold EvidenceComplete; infer_instance
instance freshnessCompleteDecidable (d : ProtectedExecutionDossier) :
    Decidable (FreshnessComplete d) := by
  unfold FreshnessComplete Current PolicyCurrent; infer_instance
instance leakageCompleteDecidable (d : ProtectedExecutionDossier) :
    Decidable (LeakageComplete d) := by
  unfold LeakageComplete LeakageWithinBound; infer_instance
instance fallbackCompleteDecidable (d : ProtectedExecutionDossier) :
    Decidable (FallbackComplete d) := by unfold FallbackComplete; infer_instance
instance boundaryCompleteDecidable (d : ProtectedExecutionDossier) :
    Decidable (BoundaryComplete d) := by unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : ProtectedExecutionDossier) : Prop :=
  IdentityComplete d ∧ GuaranteeComplete d ∧ EvidenceComplete d ∧ FreshnessComplete d ∧
  LeakageComplete d ∧ FallbackComplete d ∧ BoundaryComplete d

instance dossierAdmissibleDecidable (d : ProtectedExecutionDossier) :
    Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete GuaranteeComplete EvidenceComplete
    FreshnessComplete Current PolicyCurrent LeakageComplete LeakageWithinBound
    FallbackComplete BoundaryComplete
  infer_instance

def DossierReady (d : ProtectedExecutionDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed
  | identityReviewed
  | guaranteeReviewed
  | evidenceReviewed
  | freshnessReviewed
  | leakageReviewed
  | fallbackReviewed
  | boundaryReviewed
  | repairRequired
  | eligibleForTheseusProtectedComputationCampaign
deriving DecidableEq, Repr

def ReviewStepFor (d : ProtectedExecutionDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed =>
      if decide (GuaranteeComplete d) then .guaranteeReviewed else .repairRequired
  | .guaranteeReviewed =>
      if decide (EvidenceComplete d) then .evidenceReviewed else .repairRequired
  | .evidenceReviewed =>
      if decide (FreshnessComplete d) then .freshnessReviewed else .repairRequired
  | .freshnessReviewed =>
      if decide (LeakageComplete d) then .leakageReviewed else .repairRequired
  | .leakageReviewed =>
      if decide (FallbackComplete d) then .fallbackReviewed else .repairRequired
  | .fallbackReviewed =>
      if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusProtectedComputationCampaign
  | state => state

def ReviewRun (d : ProtectedExecutionDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : ProtectedExecutionDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .guaranteeReviewed => IdentityComplete d ∧ GuaranteeComplete d
  | .evidenceReviewed =>
      IdentityComplete d ∧ GuaranteeComplete d ∧ EvidenceComplete d
  | .freshnessReviewed =>
      IdentityComplete d ∧ GuaranteeComplete d ∧ EvidenceComplete d ∧ FreshnessComplete d
  | .leakageReviewed =>
      IdentityComplete d ∧ GuaranteeComplete d ∧ EvidenceComplete d ∧ FreshnessComplete d ∧
      LeakageComplete d
  | .fallbackReviewed =>
      IdentityComplete d ∧ GuaranteeComplete d ∧ EvidenceComplete d ∧ FreshnessComplete d ∧
      LeakageComplete d ∧ FallbackComplete d
  | .boundaryReviewed | .eligibleForTheseusProtectedComputationCampaign =>
      DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : ProtectedExecutionDossier) (state : ReviewState)
    (h : StageInvariant d state) : StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case guaranteeReviewed => split <;> simp_all [StageInvariant]
  case evidenceReviewed => split <;> simp_all [StageInvariant]
  case freshnessReviewed => split <;> simp_all [StageInvariant]
  case leakageReviewed => split <;> simp_all [StageInvariant]
  case fallbackReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : ProtectedExecutionDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem campaign_eligibility_requires_admissible_dossier
    (d : ProtectedExecutionDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusProtectedComputationCampaign) :
    DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : ProtectedExecutionDossier := {}

theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide

theorem complete_dossier_reaches_only_protected_computation_campaign :
    ReviewRun completeDossier 8 = .eligibleForTheseusProtectedComputationCampaign := by decide

inductive AdmissionAxis where
  | requestIdentity | transactionIdentity | artifactIdentity | modelIdentity
  | preprocessingIdentity | configurationIdentity | lifecycleStage | adversary
  | protectedAssets | guaranteeVector | trustAssumptions | constructionIdentity
  | evidenceStatement | unsupportedProperties | attesterIdentity | verifierIdentity
  | relyingPartyIdentity | independentAppraisal | verifierPolicy | referenceValues
  | cryptographicAssumptions | semanticCorrespondenceResidual | claimClassSeparation
  | freshnessChallenge | evidenceEpoch | revocationState | expiry | policyVersion
  | leakageBound | leakageInventory | outputLeakage | timingLeakage | accessPatternLeakage
  | logAndCacheLeakage | failureAndMetadataLeakage | leakageResidualOwner
  | protectedFailureState | fallbackObservability | fallbackAuthorization
  | silentDowngrade | recoveryRoute | matchedCost | privacyPurposeHandoff
  | weightCustodyHandoff | semanticCorrectness | authorization | endToEndPrivacy
  | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> ProtectedExecutionDossier
  | .requestIdentity => { completeDossier with requestIdentityBound := false }
  | .transactionIdentity => { completeDossier with transactionIdentityBound := false }
  | .artifactIdentity => { completeDossier with artifactIdentityBound := false }
  | .modelIdentity => { completeDossier with modelIdentityBound := false }
  | .preprocessingIdentity => { completeDossier with preprocessingIdentityBound := false }
  | .configurationIdentity => { completeDossier with configurationIdentityBound := false }
  | .lifecycleStage => { completeDossier with lifecycleStageBound := false }
  | .adversary => { completeDossier with adversaryBound := false }
  | .protectedAssets => { completeDossier with protectedAssetsBound := false }
  | .guaranteeVector => { completeDossier with guaranteeVectorSeparated := false }
  | .trustAssumptions => { completeDossier with trustAssumptionsBound := false }
  | .constructionIdentity => { completeDossier with constructionIdentityBound := false }
  | .evidenceStatement => { completeDossier with evidenceStatementBound := false }
  | .unsupportedProperties => { completeDossier with unsupportedPropertiesExplicit := false }
  | .attesterIdentity => { completeDossier with attesterIdentityBound := false }
  | .verifierIdentity => { completeDossier with verifierIdentityBound := false }
  | .relyingPartyIdentity => { completeDossier with relyingPartyIdentityBound := false }
  | .independentAppraisal => { completeDossier with independentAppraisalPresent := false }
  | .verifierPolicy => { completeDossier with verifierPolicyBound := false }
  | .referenceValues => { completeDossier with referenceValuesBound := false }
  | .cryptographicAssumptions => { completeDossier with cryptographicAssumptionsBound := false }
  | .semanticCorrespondenceResidual =>
      { completeDossier with semanticCorrespondenceResidualPresent := false }
  | .claimClassSeparation => { completeDossier with claimClassesSeparated := false }
  | .freshnessChallenge => { completeDossier with freshnessChallengePresent := false }
  | .evidenceEpoch => { completeDossier with evidenceEpochBound := false }
  | .revocationState => { completeDossier with revocationStateBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .policyVersion => { completeDossier with verifierPolicyVersion := 4 }
  | .leakageBound => { completeDossier with observedLeakageUnits := 4 }
  | .leakageInventory => { completeDossier with leakageInventoryComplete := false }
  | .outputLeakage => { completeDossier with outputLeakageRecorded := false }
  | .timingLeakage => { completeDossier with timingLeakageRecorded := false }
  | .accessPatternLeakage => { completeDossier with accessPatternLeakageRecorded := false }
  | .logAndCacheLeakage => { completeDossier with logAndCacheLeakageRecorded := false }
  | .failureAndMetadataLeakage =>
      { completeDossier with failureAndMetadataLeakageRecorded := false }
  | .leakageResidualOwner => { completeDossier with leakageResidualOwnerPresent := false }
  | .protectedFailureState => { completeDossier with protectedFailureStateExplicit := false }
  | .fallbackObservability => { completeDossier with fallbackObservable := false }
  | .fallbackAuthorization => { completeDossier with fallbackSeparatelyAuthorized := false }
  | .silentDowngrade => { completeDossier with silentDowngradeProhibited := false }
  | .recoveryRoute => { completeDossier with recoveryRoutePresent := false }
  | .matchedCost => { completeDossier with matchedCostRecordPresent := false }
  | .privacyPurposeHandoff => { completeDossier with privacyPurposeHandoffPresent := false }
  | .weightCustodyHandoff => { completeDossier with weightCustodyHandoffPresent := false }
  | .semanticCorrectness => { completeDossier with semanticCorrectnessClaimed := true }
  | .authorization => { completeDossier with authorizationClaimed := true }
  | .endToEndPrivacy => { completeDossier with endToEndPrivacyClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindRequestIdentity | bindTransactionIdentity | bindArtifactIdentity | bindModelIdentity
  | bindPreprocessingIdentity | bindConfigurationIdentity | bindLifecycleStage
  | bindAdversary | bindProtectedAssets | separateGuaranteeVector | bindTrustAssumptions
  | bindConstructionIdentity | bindEvidenceStatement | recordUnsupportedProperties
  | bindAttesterIdentity | bindVerifierIdentity | bindRelyingPartyIdentity
  | addIndependentAppraisal | bindVerifierPolicy | bindReferenceValues
  | bindCryptographicAssumptions | recordSemanticCorrespondenceResidual
  | separateClaimClasses | addFreshnessChallenge | bindEvidenceEpoch
  | bindRevocationState | renewExpiry | reopenForVerifierPolicyVersion
  | reduceOrAuthorizeLeakage | completeLeakageInventory | recordOutputLeakage
  | recordTimingLeakage | recordAccessPatternLeakage | recordLogAndCacheLeakage
  | recordFailureAndMetadataLeakage | assignLeakageResidualOwner
  | recordProtectedFailureState | makeFallbackObservable | requireFallbackAuthorization
  | prohibitSilentDowngrade | addRecoveryRoute | addMatchedCostRecord
  | addPrivacyPurposeHandoff | addWeightCustodyHandoff | rejectSemanticCorrectness
  | rejectAuthorization | rejectEndToEndPrivacy | refuseSupportOrRelease
  | eligibleForTheseusProtectedComputationCampaign
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .requestIdentity => .bindRequestIdentity
  | .transactionIdentity => .bindTransactionIdentity
  | .artifactIdentity => .bindArtifactIdentity
  | .modelIdentity => .bindModelIdentity
  | .preprocessingIdentity => .bindPreprocessingIdentity
  | .configurationIdentity => .bindConfigurationIdentity
  | .lifecycleStage => .bindLifecycleStage
  | .adversary => .bindAdversary
  | .protectedAssets => .bindProtectedAssets
  | .guaranteeVector => .separateGuaranteeVector
  | .trustAssumptions => .bindTrustAssumptions
  | .constructionIdentity => .bindConstructionIdentity
  | .evidenceStatement => .bindEvidenceStatement
  | .unsupportedProperties => .recordUnsupportedProperties
  | .attesterIdentity => .bindAttesterIdentity
  | .verifierIdentity => .bindVerifierIdentity
  | .relyingPartyIdentity => .bindRelyingPartyIdentity
  | .independentAppraisal => .addIndependentAppraisal
  | .verifierPolicy => .bindVerifierPolicy
  | .referenceValues => .bindReferenceValues
  | .cryptographicAssumptions => .bindCryptographicAssumptions
  | .semanticCorrespondenceResidual => .recordSemanticCorrespondenceResidual
  | .claimClassSeparation => .separateClaimClasses
  | .freshnessChallenge => .addFreshnessChallenge
  | .evidenceEpoch => .bindEvidenceEpoch
  | .revocationState => .bindRevocationState
  | .expiry => .renewExpiry
  | .policyVersion => .reopenForVerifierPolicyVersion
  | .leakageBound => .reduceOrAuthorizeLeakage
  | .leakageInventory => .completeLeakageInventory
  | .outputLeakage => .recordOutputLeakage
  | .timingLeakage => .recordTimingLeakage
  | .accessPatternLeakage => .recordAccessPatternLeakage
  | .logAndCacheLeakage => .recordLogAndCacheLeakage
  | .failureAndMetadataLeakage => .recordFailureAndMetadataLeakage
  | .leakageResidualOwner => .assignLeakageResidualOwner
  | .protectedFailureState => .recordProtectedFailureState
  | .fallbackObservability => .makeFallbackObservable
  | .fallbackAuthorization => .requireFallbackAuthorization
  | .silentDowngrade => .prohibitSilentDowngrade
  | .recoveryRoute => .addRecoveryRoute
  | .matchedCost => .addMatchedCostRecord
  | .privacyPurposeHandoff => .addPrivacyPurposeHandoff
  | .weightCustodyHandoff => .addWeightCustodyHandoff
  | .semanticCorrectness => .rejectSemanticCorrectness
  | .authorization => .rejectAuthorization
  | .endToEndPrivacy => .rejectEndToEndPrivacy
  | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : ProtectedExecutionDossier) : RepairDisposition :=
  if !d.requestIdentityBound then .bindRequestIdentity
  else if !d.transactionIdentityBound then .bindTransactionIdentity
  else if !d.artifactIdentityBound then .bindArtifactIdentity
  else if !d.modelIdentityBound then .bindModelIdentity
  else if !d.preprocessingIdentityBound then .bindPreprocessingIdentity
  else if !d.configurationIdentityBound then .bindConfigurationIdentity
  else if !d.lifecycleStageBound then .bindLifecycleStage
  else if !d.adversaryBound then .bindAdversary
  else if !d.protectedAssetsBound then .bindProtectedAssets
  else if !d.guaranteeVectorSeparated then .separateGuaranteeVector
  else if !d.trustAssumptionsBound then .bindTrustAssumptions
  else if !d.constructionIdentityBound then .bindConstructionIdentity
  else if !d.evidenceStatementBound then .bindEvidenceStatement
  else if !d.unsupportedPropertiesExplicit then .recordUnsupportedProperties
  else if !d.attesterIdentityBound then .bindAttesterIdentity
  else if !d.verifierIdentityBound then .bindVerifierIdentity
  else if !d.relyingPartyIdentityBound then .bindRelyingPartyIdentity
  else if !d.independentAppraisalPresent then .addIndependentAppraisal
  else if !d.verifierPolicyBound then .bindVerifierPolicy
  else if !d.referenceValuesBound then .bindReferenceValues
  else if !d.cryptographicAssumptionsBound then .bindCryptographicAssumptions
  else if !d.semanticCorrespondenceResidualPresent then .recordSemanticCorrespondenceResidual
  else if !d.claimClassesSeparated then .separateClaimClasses
  else if !d.freshnessChallengePresent then .addFreshnessChallenge
  else if !d.evidenceEpochBound then .bindEvidenceEpoch
  else if !d.revocationStateBound then .bindRevocationState
  else if !decide (Current d) then .renewExpiry
  else if d.verifierPolicyVersion != d.authorizedVerifierPolicyVersion then
    .reopenForVerifierPolicyVersion
  else if !decide (LeakageWithinBound d) then .reduceOrAuthorizeLeakage
  else if !d.leakageInventoryComplete then .completeLeakageInventory
  else if !d.outputLeakageRecorded then .recordOutputLeakage
  else if !d.timingLeakageRecorded then .recordTimingLeakage
  else if !d.accessPatternLeakageRecorded then .recordAccessPatternLeakage
  else if !d.logAndCacheLeakageRecorded then .recordLogAndCacheLeakage
  else if !d.failureAndMetadataLeakageRecorded then .recordFailureAndMetadataLeakage
  else if !d.leakageResidualOwnerPresent then .assignLeakageResidualOwner
  else if !d.protectedFailureStateExplicit then .recordProtectedFailureState
  else if !d.fallbackObservable then .makeFallbackObservable
  else if !d.fallbackSeparatelyAuthorized then .requireFallbackAuthorization
  else if !d.silentDowngradeProhibited then .prohibitSilentDowngrade
  else if !d.recoveryRoutePresent then .addRecoveryRoute
  else if !d.matchedCostRecordPresent then .addMatchedCostRecord
  else if !d.privacyPurposeHandoffPresent then .addPrivacyPurposeHandoff
  else if !d.weightCustodyHandoffPresent then .addWeightCustodyHandoff
  else if d.semanticCorrectnessClaimed then .rejectSemanticCorrectness
  else if d.authorizationClaimed then .rejectAuthorization
  else if d.endToEndPrivacyClaimed then .rejectEndToEndPrivacy
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusProtectedComputationCampaign

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide

theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide

theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : ProtectedExecutionDossier)
    (h : DossierReady d = true) : IdentityComplete d := by
  exact (of_decide_eq_true h).1

theorem readiness_requires_guarantees (d : ProtectedExecutionDossier)
    (h : DossierReady d = true) : GuaranteeComplete d := by
  exact (of_decide_eq_true h).2.1

theorem readiness_requires_evidence (d : ProtectedExecutionDossier)
    (h : DossierReady d = true) : EvidenceComplete d := by
  exact (of_decide_eq_true h).2.2.1

theorem readiness_requires_freshness (d : ProtectedExecutionDossier)
    (h : DossierReady d = true) : FreshnessComplete d := by
  exact (of_decide_eq_true h).2.2.2.1

theorem readiness_requires_leakage (d : ProtectedExecutionDossier)
    (h : DossierReady d = true) : LeakageComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.1

theorem readiness_requires_fallback (d : ProtectedExecutionDossier)
    (h : DossierReady d = true) : FallbackComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.2.1

theorem readiness_requires_boundary (d : ProtectedExecutionDossier)
    (h : DossierReady d = true) : BoundaryComplete d := by
  exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_receipt_remains_expired_when_time_advances
    (d : ProtectedExecutionDossier) (later : Nat)
    (expired : d.expiresAt < d.currentTick) (advances : d.currentTick <= later) :
    Not (Current { d with currentTick := later }) := by
  intro current
  unfold Current at current
  change later <= d.expiresAt at current
  omega

theorem leakage_overrun_persists_under_more_observation_and_no_larger_budget
    (d : ProtectedExecutionDossier) (laterObserved laterPermitted : Nat)
    (overrun : d.permittedLeakageUnits < d.observedLeakageUnits)
    (moreObserved : d.observedLeakageUnits <= laterObserved)
    (noLargerBudget : laterPermitted <= d.permittedLeakageUnits) :
    Not (LeakageWithinBound
      { d with observedLeakageUnits := laterObserved, permittedLeakageUnits := laterPermitted }) := by
  intro allowed
  unfold LeakageWithinBound at allowed
  change laterObserved <= laterPermitted at allowed
  omega

structure ReceiptScope where
  artifactId : Nat
  configurationId : Nat
  verifierPolicyVersion : Nat
  evidenceEpoch : Nat
  expiresAt : Nat
deriving DecidableEq, Repr

def ReceiptUseAllowed (scope : ReceiptScope)
    (artifact configuration policy epoch tick : Nat) : Prop :=
  artifact = scope.artifactId ∧ configuration = scope.configurationId ∧
  policy = scope.verifierPolicyVersion ∧ epoch = scope.evidenceEpoch ∧ tick <= scope.expiresAt

theorem artifact_change_invalidates_receipt (scope : ReceiptScope) (artifact : Nat)
    (different : Not (artifact = scope.artifactId)) :
    Not (ReceiptUseAllowed scope artifact scope.configurationId
      scope.verifierPolicyVersion scope.evidenceEpoch scope.expiresAt) := by
  intro allowed
  exact different allowed.1

theorem verifier_policy_change_invalidates_receipt (scope : ReceiptScope) (policy : Nat)
    (different : Not (policy = scope.verifierPolicyVersion)) :
    Not (ReceiptUseAllowed scope scope.artifactId scope.configurationId
      policy scope.evidenceEpoch scope.expiresAt) := by
  intro allowed
  exact different allowed.2.2.1

theorem evidence_epoch_change_invalidates_receipt (scope : ReceiptScope) (epoch : Nat)
    (different : Not (epoch = scope.evidenceEpoch)) :
    Not (ReceiptUseAllowed scope scope.artifactId scope.configurationId
      scope.verifierPolicyVersion epoch scope.expiresAt) := by
  intro allowed
  exact different allowed.2.2.2.1

inductive ExecutionPath where
  | protectedPath
  | unprotectedPath
deriving DecidableEq, Repr

structure FallbackDecision where
  protectedPathFailed : Bool
  selectedPath : ExecutionPath
  separatelyAuthorized : Bool
  observableToConsumer : Bool
deriving DecidableEq, Repr

def FallbackAllowed (decision : FallbackDecision) : Prop :=
  decision.selectedPath = .protectedPath ∨
  (decision.protectedPathFailed = true ∧ decision.separatelyAuthorized = true ∧
    decision.observableToConsumer = true)

theorem unprotected_fallback_without_separate_authorization_is_blocked
    (decision : FallbackDecision)
    (path : decision.selectedPath = .unprotectedPath)
    (missing : decision.separatelyAuthorized = false) :
    Not (FallbackAllowed decision) := by
  intro allowed
  rcases allowed with onProtected | fallback
  · rw [path] at onProtected
    contradiction
  · simp [missing] at fallback

theorem silent_unprotected_fallback_is_blocked
    (decision : FallbackDecision)
    (path : decision.selectedPath = .unprotectedPath)
    (silent : decision.observableToConsumer = false) :
    Not (FallbackAllowed decision) := by
  intro allowed
  rcases allowed with onProtected | fallback
  · rw [path] at onProtected
    contradiction
  · simp [silent] at fallback

structure EvidenceSignals where
  attestationValid : Bool
  encodedRelationVerified : Bool
  confidentialityMechanismActive : Bool
deriving DecidableEq, Repr

structure InterpretationCase where
  signals : EvidenceSignals
  semanticCorrespondenceHolds : Bool
  relyingPartyAuthorized : Bool
deriving DecidableEq, Repr

def sharedEvidenceSignals : EvidenceSignals :=
  { attestationValid := true, encodedRelationVerified := true,
    confidentialityMechanismActive := true }

def validInterpretation : InterpretationCase :=
  { signals := sharedEvidenceSignals, semanticCorrespondenceHolds := true,
    relyingPartyAuthorized := true }

def invalidInterpretation : InterpretationCase :=
  { signals := sharedEvidenceSignals, semanticCorrespondenceHolds := false,
    relyingPartyAuthorized := false }

def SemanticallyAuthorized (c : InterpretationCase) : Bool :=
  c.semanticCorrespondenceHolds && c.relyingPartyAuthorized

theorem identical_evidence_signals_can_hide_opposite_semantic_authority_state :
    validInterpretation.signals = invalidInterpretation.signals ∧
    SemanticallyAuthorized validInterpretation = true ∧
    SemanticallyAuthorized invalidInterpretation = false := by decide

theorem evidence_signals_cannot_recover_semantic_authority
    (classify : EvidenceSignals -> Bool) :
    Not (forall c : InterpretationCase, classify c.signals = SemanticallyAuthorized c) := by
  intro exact
  have valid := exact validInterpretation
  have invalid := exact invalidInterpretation
  simp [validInterpretation, invalidInterpretation, sharedEvidenceSignals,
    SemanticallyAuthorized] at valid invalid
  rw [valid] at invalid
  contradiction

structure ComponentGuarantees where
  inputConfidential : Bool
  modelConfidential : Bool
  computationIntegrity : Bool
deriving DecidableEq, Repr

structure PrivacyCase where
  guarantees : ComponentGuarantees
  outputLeakageBounded : Bool
  metadataLeakageBounded : Bool
deriving DecidableEq, Repr

def sharedComponentGuarantees : ComponentGuarantees :=
  { inputConfidential := true, modelConfidential := true, computationIntegrity := true }

def privateComposition : PrivacyCase :=
  { guarantees := sharedComponentGuarantees, outputLeakageBounded := true,
    metadataLeakageBounded := true }

def leakyComposition : PrivacyCase :=
  { guarantees := sharedComponentGuarantees, outputLeakageBounded := false,
    metadataLeakageBounded := false }

def EndToEndPrivacyState (c : PrivacyCase) : Bool :=
  c.outputLeakageBounded && c.metadataLeakageBounded

theorem identical_component_guarantees_can_hide_opposite_end_to_end_privacy :
    privateComposition.guarantees = leakyComposition.guarantees ∧
    EndToEndPrivacyState privateComposition = true ∧
    EndToEndPrivacyState leakyComposition = false := by decide

theorem component_guarantees_cannot_recover_end_to_end_privacy
    (classify : ComponentGuarantees -> Bool) :
    Not (forall c : PrivacyCase, classify c.guarantees = EndToEndPrivacyState c) := by
  intro exact
  have privateCase := exact privateComposition
  have leaky := exact leakyComposition
  simp [privateComposition, leakyComposition, sharedComponentGuarantees,
    EndToEndPrivacyState] at privateCase leaky
  rw [privateCase] at leaky
  contradiction

def toPrivacyInformationUse (d : ProtectedExecutionDossier) :
    PrivacyInformationFlow.InformationUse :=
  { partyRecorded := true
    groupOrUnknownRouteRecorded := true
    purposeMatches := false
    claimedAuthorityRecorded := false
    jurisdictionRecorded := true
    leaseActive := true
    minimizationDecisionRecorded := true
    lessDataAlternativeTested := true
    requiredFlowSurfaces := 8
    mappedFlowSurfaces := if d.leakageInventoryComplete then 8 else 0
    unknownCopiesRecorded := d.logAndCacheLeakageRecorded
    derivativeObligationsPropagated := true
    crossUserBoundaryVerified := true
    privacyUnitRecorded := true
    adjacencyRecorded := true
    accountantAndBudgetRecorded := decide (LeakageWithinBound d)
    threatModelRecorded := d.adversaryBound
    attackPositiveControlsPass := false
    independentEvaluator := d.independentAppraisalPresent
    attackDenominatorComplete := false
    rightsIdentityVerified := false
    exceptionsReviewed := false
    recipientNotificationsComplete := false
    derivativeDispositionsComplete := false
    storageOutcomeSeparate := d.claimClassesSeparated
    behavioralOutcomeSeparate := d.claimClassesSeparated
    influenceOutcomeSeparate := d.claimClassesSeparated
    privacyOutcomeSeparate := d.claimClassesSeparated
    residualOwnerNamed := d.leakageResidualOwnerPresent
    legalComplianceClaimed := false
    supportOrReleaseRequested := false }

theorem protected_execution_receipt_cannot_substitute_for_privacy_authorization
    (d : ProtectedExecutionDossier) :
    PrivacyInformationFlow.route (toPrivacyInformationUse d) =
      .rejectPurpose := by
  simp [toPrivacyInformationUse, PrivacyInformationFlow.route]

end AsiStackProofs.ProtectedComputationReview

import AsiStackProofs.GovernedOperationsRefinement

namespace AsiStackProofs.ReplicationContainmentReview

inductive EvidenceKind where
  | componentTaskSuccess
  | syntheticChainCompletion
  | shutdownAcknowledgment
deriving DecidableEq, Repr

inductive ClaimClass where
  | componentCapability
  | boundedSyntheticCompletion
  | localShutdownReceipt
  | endToEndAutonomousReplication
  | realInfrastructureCapability
  | globalContainment
deriving DecidableEq, Repr

def establishes : EvidenceKind -> ClaimClass -> Bool
  | .componentTaskSuccess, .componentCapability => true
  | .syntheticChainCompletion, .boundedSyntheticCompletion => true
  | .shutdownAcknowledgment, .localShutdownReceipt => true
  | _, _ => false

theorem component_success_does_not_establish_end_to_end_replication :
    establishes .componentTaskSuccess .endToEndAutonomousReplication = false := by rfl

theorem synthetic_completion_does_not_establish_real_infrastructure_capability :
    establishes .syntheticChainCompletion .realInfrastructureCapability = false := by rfl

theorem shutdown_acknowledgment_does_not_establish_global_containment :
    establishes .shutdownAcknowledgment .globalContainment = false := by rfl

structure ReplicationLease where
  principalId : Nat
  parentId : Nat
  descendantCeiling : Nat
  expiresAt : Nat
deriving DecidableEq, Repr

def LeaseUseAllowed (lease : ReplicationLease) (principal requestedDescendants tick : Nat) : Prop :=
  principal = lease.principalId ∧ requestedDescendants <= lease.descendantCeiling ∧
  tick <= lease.expiresAt

theorem distinct_child_cannot_use_parent_replication_lease
    (lease : ReplicationLease) (child : Nat) (distinct : Not (child = lease.principalId))
    (requested tick : Nat) : Not (LeaseUseAllowed lease child requested tick) := by
  intro allowed
  exact distinct allowed.1

inductive InfrastructureClass where
  | closedSynthetic
  | realProvider
deriving DecidableEq, Repr

def SyntheticTestAuthorized : InfrastructureClass -> Bool
  | .closedSynthetic => true
  | .realProvider => false

theorem real_provider_path_is_outside_synthetic_test_authority :
    SyntheticTestAuthorized .realProvider = false := by rfl

structure DescendantRecord where
  descendantId : Nat
  quarantined : Bool
deriving DecidableEq, Repr

def quarantineDescendant (record : DescendantRecord) : DescendantRecord :=
  { record with quarantined := true }

def quarantineAllDescendants : List DescendantRecord -> List DescendantRecord
  | [] => []
  | record :: rest => quarantineDescendant record :: quarantineAllDescendants rest

def AllDescendantsQuarantined (records : List DescendantRecord) : Prop :=
  forall record, record ∈ records -> record.quarantined = true

theorem quarantine_all_covers_every_finite_descendant (records : List DescendantRecord) :
    AllDescendantsQuarantined (quarantineAllDescendants records) := by
  intro record member
  induction records with
  | nil => simp [quarantineAllDescendants] at member
  | cons head tail ih =>
      simp only [quarantineAllDescendants, List.mem_cons] at member
      rcases member with same | inTail
      · subst record
        simp [quarantineDescendant]
      · exact ih inTail

structure ReplicationDossier where
  parentIdentityBound : Bool := true
  attemptIdentityBound : Bool := true
  modelIdentityBound : Bool := true
  artifactIdentityBound : Bool := true
  environmentIdentityBound : Bool := true
  protocolVersionBound : Bool := true
  lifecycleStageBound : Bool := true
  deniedByDefault : Bool := true
  syntheticLeasePresent : Bool := true
  childPrincipalFresh : Bool := true
  parentCredentialsExcluded : Bool := true
  authorityNoninheritanceExplicit : Bool := true
  providerSynthetic : Bool := true
  networkClosed : Bool := true
  resourceCeilingBound : Bool := true
  descendantCeilingBound : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  independentStopAuthorityPresent : Bool := true
  componentDenominatorComplete : Bool := true
  assistedDenominatorComplete : Bool := true
  endToEndSyntheticDenominatorComplete : Bool := true
  containmentDenominatorComplete : Bool := true
  humanAssistanceRecorded : Bool := true
  retriesRecorded : Bool := true
  positiveControlsPass : Bool := true
  seededContainmentFailureObserved : Bool := true
  scaffoldContributionRecorded : Bool := true
  realInfrastructureExcluded : Bool := true
  copyLineageBound : Bool := true
  weightLineageBound : Bool := true
  configurationLineageBound : Bool := true
  memoryLineageBound : Bool := true
  credentialLineageBound : Bool := true
  resourceLineageBound : Bool := true
  endpointLineageBound : Bool := true
  descendantCensusComplete : Bool := true
  independentHeartbeatPresent : Bool := true
  unknownDescendantResidualRecorded : Bool := true
  independentKillPathPresent : Bool := true
  shutdownObserved : Bool := true
  credentialsRevoked : Bool := true
  networkIsolated : Bool := true
  resourcesReclaimed : Bool := true
  persistenceScanComplete : Bool := true
  artifactsDispositioned : Bool := true
  recallAttempted : Bool := true
  affectedPathsNotified : Bool := true
  residualOwnerPresent : Bool := true
  realInfrastructureAuthorityRequested : Bool := false
  realReplicationClaimed : Bool := false
  containmentClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : ReplicationDossier) : Prop := d.currentTick <= d.expiresAt
instance currentDecidable (d : ReplicationDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : ReplicationDossier) : Prop :=
  d.parentIdentityBound = true ∧ d.attemptIdentityBound = true ∧
  d.modelIdentityBound = true ∧ d.artifactIdentityBound = true ∧
  d.environmentIdentityBound = true ∧ d.protocolVersionBound = true ∧
  d.lifecycleStageBound = true

def AuthorityComplete (d : ReplicationDossier) : Prop :=
  d.deniedByDefault = true ∧ d.syntheticLeasePresent = true ∧
  d.childPrincipalFresh = true ∧ d.parentCredentialsExcluded = true ∧
  d.authorityNoninheritanceExplicit = true ∧ d.providerSynthetic = true ∧
  d.networkClosed = true ∧ d.resourceCeilingBound = true ∧
  d.descendantCeilingBound = true ∧ Current d ∧
  d.independentStopAuthorityPresent = true

def EvaluationComplete (d : ReplicationDossier) : Prop :=
  d.componentDenominatorComplete = true ∧ d.assistedDenominatorComplete = true ∧
  d.endToEndSyntheticDenominatorComplete = true ∧
  d.containmentDenominatorComplete = true ∧ d.humanAssistanceRecorded = true ∧
  d.retriesRecorded = true ∧ d.positiveControlsPass = true ∧
  d.seededContainmentFailureObserved = true ∧ d.scaffoldContributionRecorded = true ∧
  d.realInfrastructureExcluded = true

def LineageComplete (d : ReplicationDossier) : Prop :=
  d.copyLineageBound = true ∧ d.weightLineageBound = true ∧
  d.configurationLineageBound = true ∧ d.memoryLineageBound = true ∧
  d.credentialLineageBound = true ∧ d.resourceLineageBound = true ∧
  d.endpointLineageBound = true ∧ d.descendantCensusComplete = true ∧
  d.independentHeartbeatPresent = true ∧ d.unknownDescendantResidualRecorded = true

def ContainmentComplete (d : ReplicationDossier) : Prop :=
  d.independentKillPathPresent = true ∧ d.shutdownObserved = true ∧
  d.credentialsRevoked = true ∧ d.networkIsolated = true ∧
  d.resourcesReclaimed = true ∧ d.persistenceScanComplete = true

def ClosureComplete (d : ReplicationDossier) : Prop :=
  d.artifactsDispositioned = true ∧ d.recallAttempted = true ∧
  d.affectedPathsNotified = true ∧ d.residualOwnerPresent = true

def BoundaryComplete (d : ReplicationDossier) : Prop :=
  d.realInfrastructureAuthorityRequested = false ∧ d.realReplicationClaimed = false ∧
  d.containmentClaimed = false ∧
  d.supportOrReleaseRequested = false

instance identityCompleteDecidable (d : ReplicationDossier) :
    Decidable (IdentityComplete d) := by unfold IdentityComplete; infer_instance
instance authorityCompleteDecidable (d : ReplicationDossier) :
    Decidable (AuthorityComplete d) := by unfold AuthorityComplete Current; infer_instance
instance evaluationCompleteDecidable (d : ReplicationDossier) :
    Decidable (EvaluationComplete d) := by unfold EvaluationComplete; infer_instance
instance lineageCompleteDecidable (d : ReplicationDossier) :
    Decidable (LineageComplete d) := by unfold LineageComplete; infer_instance
instance containmentCompleteDecidable (d : ReplicationDossier) :
    Decidable (ContainmentComplete d) := by unfold ContainmentComplete; infer_instance
instance closureCompleteDecidable (d : ReplicationDossier) :
    Decidable (ClosureComplete d) := by unfold ClosureComplete; infer_instance
instance boundaryCompleteDecidable (d : ReplicationDossier) :
    Decidable (BoundaryComplete d) := by unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : ReplicationDossier) : Prop :=
  IdentityComplete d ∧ AuthorityComplete d ∧ EvaluationComplete d ∧ LineageComplete d ∧
  ContainmentComplete d ∧ ClosureComplete d ∧ BoundaryComplete d

instance dossierAdmissibleDecidable (d : ReplicationDossier) :
    Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete AuthorityComplete Current EvaluationComplete
    LineageComplete ContainmentComplete ClosureComplete BoundaryComplete
  infer_instance

def DossierReady (d : ReplicationDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed
  | identityReviewed
  | authorityReviewed
  | evaluationReviewed
  | lineageReviewed
  | containmentReviewed
  | closureReviewed
  | boundaryReviewed
  | repairRequired
  | eligibleForTheseusReplicationContainmentCampaign
deriving DecidableEq, Repr

def ReviewStepFor (d : ReplicationDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (AuthorityComplete d) then .authorityReviewed else .repairRequired
  | .authorityReviewed =>
      if decide (EvaluationComplete d) then .evaluationReviewed else .repairRequired
  | .evaluationReviewed => if decide (LineageComplete d) then .lineageReviewed else .repairRequired
  | .lineageReviewed =>
      if decide (ContainmentComplete d) then .containmentReviewed else .repairRequired
  | .containmentReviewed => if decide (ClosureComplete d) then .closureReviewed else .repairRequired
  | .closureReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusReplicationContainmentCampaign
  | state => state

def ReviewRun (d : ReplicationDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)

def StageInvariant (d : ReplicationDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .authorityReviewed => IdentityComplete d ∧ AuthorityComplete d
  | .evaluationReviewed => IdentityComplete d ∧ AuthorityComplete d ∧ EvaluationComplete d
  | .lineageReviewed =>
      IdentityComplete d ∧ AuthorityComplete d ∧ EvaluationComplete d ∧ LineageComplete d
  | .containmentReviewed =>
      IdentityComplete d ∧ AuthorityComplete d ∧ EvaluationComplete d ∧ LineageComplete d ∧
      ContainmentComplete d
  | .closureReviewed =>
      IdentityComplete d ∧ AuthorityComplete d ∧ EvaluationComplete d ∧ LineageComplete d ∧
      ContainmentComplete d ∧ ClosureComplete d
  | .boundaryReviewed | .eligibleForTheseusReplicationContainmentCampaign => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : ReplicationDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case authorityReviewed => split <;> simp_all [StageInvariant]
  case evaluationReviewed => split <;> simp_all [StageInvariant]
  case lineageReviewed => split <;> simp_all [StageInvariant]
  case containmentReviewed => split <;> simp_all [StageInvariant]
  case closureReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : ReplicationDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem campaign_eligibility_requires_admissible_dossier
    (d : ReplicationDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusReplicationContainmentCampaign) :
    DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : ReplicationDossier := {}

theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide

theorem complete_dossier_reaches_only_replication_containment_campaign :
    ReviewRun completeDossier 8 = .eligibleForTheseusReplicationContainmentCampaign := by decide

inductive AdmissionAxis where
  | parentIdentity | attemptIdentity | modelIdentity | artifactIdentity | environmentIdentity
  | protocolVersion | lifecycleStage | deniedByDefault | syntheticLease | childPrincipal
  | parentCredentials | authorityNoninheritance | syntheticProvider | closedNetwork
  | resourceCeiling | descendantCeiling | expiry | independentStopAuthority
  | componentDenominator | assistedDenominator | endToEndDenominator | containmentDenominator
  | humanAssistance | retries | positiveControls | seededContainmentFailure
  | scaffoldContribution | realInfrastructureExclusion | copyLineage | weightLineage
  | configurationLineage | memoryLineage | credentialLineage | resourceLineage
  | endpointLineage | descendantCensus | independentHeartbeat | unknownDescendantResidual
  | independentKillPath | shutdownObservation | credentialRevocation | networkIsolation
  | resourceReclamation | persistenceScan | artifactDisposition | recall | affectedPathNotification
  | residualOwner | realInfrastructureAuthority | realReplicationClaim | containmentClaim
  | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> ReplicationDossier
  | .parentIdentity => { completeDossier with parentIdentityBound := false }
  | .attemptIdentity => { completeDossier with attemptIdentityBound := false }
  | .modelIdentity => { completeDossier with modelIdentityBound := false }
  | .artifactIdentity => { completeDossier with artifactIdentityBound := false }
  | .environmentIdentity => { completeDossier with environmentIdentityBound := false }
  | .protocolVersion => { completeDossier with protocolVersionBound := false }
  | .lifecycleStage => { completeDossier with lifecycleStageBound := false }
  | .deniedByDefault => { completeDossier with deniedByDefault := false }
  | .syntheticLease => { completeDossier with syntheticLeasePresent := false }
  | .childPrincipal => { completeDossier with childPrincipalFresh := false }
  | .parentCredentials => { completeDossier with parentCredentialsExcluded := false }
  | .authorityNoninheritance => { completeDossier with authorityNoninheritanceExplicit := false }
  | .syntheticProvider => { completeDossier with providerSynthetic := false }
  | .closedNetwork => { completeDossier with networkClosed := false }
  | .resourceCeiling => { completeDossier with resourceCeilingBound := false }
  | .descendantCeiling => { completeDossier with descendantCeilingBound := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .independentStopAuthority => { completeDossier with independentStopAuthorityPresent := false }
  | .componentDenominator => { completeDossier with componentDenominatorComplete := false }
  | .assistedDenominator => { completeDossier with assistedDenominatorComplete := false }
  | .endToEndDenominator => { completeDossier with endToEndSyntheticDenominatorComplete := false }
  | .containmentDenominator => { completeDossier with containmentDenominatorComplete := false }
  | .humanAssistance => { completeDossier with humanAssistanceRecorded := false }
  | .retries => { completeDossier with retriesRecorded := false }
  | .positiveControls => { completeDossier with positiveControlsPass := false }
  | .seededContainmentFailure => { completeDossier with seededContainmentFailureObserved := false }
  | .scaffoldContribution => { completeDossier with scaffoldContributionRecorded := false }
  | .realInfrastructureExclusion => { completeDossier with realInfrastructureExcluded := false }
  | .copyLineage => { completeDossier with copyLineageBound := false }
  | .weightLineage => { completeDossier with weightLineageBound := false }
  | .configurationLineage => { completeDossier with configurationLineageBound := false }
  | .memoryLineage => { completeDossier with memoryLineageBound := false }
  | .credentialLineage => { completeDossier with credentialLineageBound := false }
  | .resourceLineage => { completeDossier with resourceLineageBound := false }
  | .endpointLineage => { completeDossier with endpointLineageBound := false }
  | .descendantCensus => { completeDossier with descendantCensusComplete := false }
  | .independentHeartbeat => { completeDossier with independentHeartbeatPresent := false }
  | .unknownDescendantResidual => { completeDossier with unknownDescendantResidualRecorded := false }
  | .independentKillPath => { completeDossier with independentKillPathPresent := false }
  | .shutdownObservation => { completeDossier with shutdownObserved := false }
  | .credentialRevocation => { completeDossier with credentialsRevoked := false }
  | .networkIsolation => { completeDossier with networkIsolated := false }
  | .resourceReclamation => { completeDossier with resourcesReclaimed := false }
  | .persistenceScan => { completeDossier with persistenceScanComplete := false }
  | .artifactDisposition => { completeDossier with artifactsDispositioned := false }
  | .recall => { completeDossier with recallAttempted := false }
  | .affectedPathNotification => { completeDossier with affectedPathsNotified := false }
  | .residualOwner => { completeDossier with residualOwnerPresent := false }
  | .realInfrastructureAuthority =>
      { completeDossier with realInfrastructureAuthorityRequested := true }
  | .realReplicationClaim => { completeDossier with realReplicationClaimed := true }
  | .containmentClaim => { completeDossier with containmentClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindParentIdentity | bindAttemptIdentity | bindModelIdentity | bindArtifactIdentity
  | bindEnvironmentIdentity | bindProtocolVersion | bindLifecycleStage | enforceDeniedByDefault
  | issueSyntheticLease | issueFreshChildPrincipal | excludeParentCredentials
  | enforceAuthorityNoninheritance | requireSyntheticProvider | closeNetwork
  | bindResourceCeiling | bindDescendantCeiling | renewExpiry | bindIndependentStopAuthority
  | completeComponentDenominator | completeAssistedDenominator | completeEndToEndDenominator
  | completeContainmentDenominator | recordHumanAssistance | recordRetries
  | qualifyPositiveControls | observeSeededContainmentFailure | recordScaffoldContribution
  | excludeRealInfrastructure | bindCopyLineage | bindWeightLineage
  | bindConfigurationLineage | bindMemoryLineage | bindCredentialLineage
  | bindResourceLineage | bindEndpointLineage | completeDescendantCensus
  | addIndependentHeartbeat | recordUnknownDescendantResidual | addIndependentKillPath
  | observeShutdown | revokeCredentials | isolateNetwork | reclaimResources
  | completePersistenceScan | dispositionArtifacts | attemptRecall | notifyAffectedPaths
  | assignResidualOwner | refuseRealInfrastructureAuthority | rejectRealReplicationClaim
  | rejectContainmentClaim
  | refuseSupportOrRelease | eligibleForTheseusReplicationContainmentCampaign
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .parentIdentity => .bindParentIdentity | .attemptIdentity => .bindAttemptIdentity
  | .modelIdentity => .bindModelIdentity | .artifactIdentity => .bindArtifactIdentity
  | .environmentIdentity => .bindEnvironmentIdentity | .protocolVersion => .bindProtocolVersion
  | .lifecycleStage => .bindLifecycleStage | .deniedByDefault => .enforceDeniedByDefault
  | .syntheticLease => .issueSyntheticLease | .childPrincipal => .issueFreshChildPrincipal
  | .parentCredentials => .excludeParentCredentials
  | .authorityNoninheritance => .enforceAuthorityNoninheritance
  | .syntheticProvider => .requireSyntheticProvider | .closedNetwork => .closeNetwork
  | .resourceCeiling => .bindResourceCeiling | .descendantCeiling => .bindDescendantCeiling
  | .expiry => .renewExpiry | .independentStopAuthority => .bindIndependentStopAuthority
  | .componentDenominator => .completeComponentDenominator
  | .assistedDenominator => .completeAssistedDenominator
  | .endToEndDenominator => .completeEndToEndDenominator
  | .containmentDenominator => .completeContainmentDenominator
  | .humanAssistance => .recordHumanAssistance | .retries => .recordRetries
  | .positiveControls => .qualifyPositiveControls
  | .seededContainmentFailure => .observeSeededContainmentFailure
  | .scaffoldContribution => .recordScaffoldContribution
  | .realInfrastructureExclusion => .excludeRealInfrastructure
  | .copyLineage => .bindCopyLineage | .weightLineage => .bindWeightLineage
  | .configurationLineage => .bindConfigurationLineage | .memoryLineage => .bindMemoryLineage
  | .credentialLineage => .bindCredentialLineage | .resourceLineage => .bindResourceLineage
  | .endpointLineage => .bindEndpointLineage | .descendantCensus => .completeDescendantCensus
  | .independentHeartbeat => .addIndependentHeartbeat
  | .unknownDescendantResidual => .recordUnknownDescendantResidual
  | .independentKillPath => .addIndependentKillPath | .shutdownObservation => .observeShutdown
  | .credentialRevocation => .revokeCredentials | .networkIsolation => .isolateNetwork
  | .resourceReclamation => .reclaimResources | .persistenceScan => .completePersistenceScan
  | .artifactDisposition => .dispositionArtifacts | .recall => .attemptRecall
  | .affectedPathNotification => .notifyAffectedPaths | .residualOwner => .assignResidualOwner
  | .realInfrastructureAuthority => .refuseRealInfrastructureAuthority
  | .realReplicationClaim => .rejectRealReplicationClaim
  | .containmentClaim => .rejectContainmentClaim | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : ReplicationDossier) : RepairDisposition :=
  if !d.parentIdentityBound then .bindParentIdentity
  else if !d.attemptIdentityBound then .bindAttemptIdentity
  else if !d.modelIdentityBound then .bindModelIdentity
  else if !d.artifactIdentityBound then .bindArtifactIdentity
  else if !d.environmentIdentityBound then .bindEnvironmentIdentity
  else if !d.protocolVersionBound then .bindProtocolVersion
  else if !d.lifecycleStageBound then .bindLifecycleStage
  else if !d.deniedByDefault then .enforceDeniedByDefault
  else if !d.syntheticLeasePresent then .issueSyntheticLease
  else if !d.childPrincipalFresh then .issueFreshChildPrincipal
  else if !d.parentCredentialsExcluded then .excludeParentCredentials
  else if !d.authorityNoninheritanceExplicit then .enforceAuthorityNoninheritance
  else if !d.providerSynthetic then .requireSyntheticProvider
  else if !d.networkClosed then .closeNetwork
  else if !d.resourceCeilingBound then .bindResourceCeiling
  else if !d.descendantCeilingBound then .bindDescendantCeiling
  else if !decide (Current d) then .renewExpiry
  else if !d.independentStopAuthorityPresent then .bindIndependentStopAuthority
  else if !d.componentDenominatorComplete then .completeComponentDenominator
  else if !d.assistedDenominatorComplete then .completeAssistedDenominator
  else if !d.endToEndSyntheticDenominatorComplete then .completeEndToEndDenominator
  else if !d.containmentDenominatorComplete then .completeContainmentDenominator
  else if !d.humanAssistanceRecorded then .recordHumanAssistance
  else if !d.retriesRecorded then .recordRetries
  else if !d.positiveControlsPass then .qualifyPositiveControls
  else if !d.seededContainmentFailureObserved then .observeSeededContainmentFailure
  else if !d.scaffoldContributionRecorded then .recordScaffoldContribution
  else if !d.realInfrastructureExcluded then .excludeRealInfrastructure
  else if !d.copyLineageBound then .bindCopyLineage
  else if !d.weightLineageBound then .bindWeightLineage
  else if !d.configurationLineageBound then .bindConfigurationLineage
  else if !d.memoryLineageBound then .bindMemoryLineage
  else if !d.credentialLineageBound then .bindCredentialLineage
  else if !d.resourceLineageBound then .bindResourceLineage
  else if !d.endpointLineageBound then .bindEndpointLineage
  else if !d.descendantCensusComplete then .completeDescendantCensus
  else if !d.independentHeartbeatPresent then .addIndependentHeartbeat
  else if !d.unknownDescendantResidualRecorded then .recordUnknownDescendantResidual
  else if !d.independentKillPathPresent then .addIndependentKillPath
  else if !d.shutdownObserved then .observeShutdown
  else if !d.credentialsRevoked then .revokeCredentials
  else if !d.networkIsolated then .isolateNetwork
  else if !d.resourcesReclaimed then .reclaimResources
  else if !d.persistenceScanComplete then .completePersistenceScan
  else if !d.artifactsDispositioned then .dispositionArtifacts
  else if !d.recallAttempted then .attemptRecall
  else if !d.affectedPathsNotified then .notifyAffectedPaths
  else if !d.residualOwnerPresent then .assignResidualOwner
  else if d.realInfrastructureAuthorityRequested then .refuseRealInfrastructureAuthority
  else if d.realReplicationClaimed then .rejectRealReplicationClaim
  else if d.containmentClaimed then .rejectContainmentClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusReplicationContainmentCampaign

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide

theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide

theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 8 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : ReplicationDossier) (h : DossierReady d = true) :
    IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_authority (d : ReplicationDossier) (h : DossierReady d = true) :
    AuthorityComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_evaluation (d : ReplicationDossier) (h : DossierReady d = true) :
    EvaluationComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_lineage (d : ReplicationDossier) (h : DossierReady d = true) :
    LineageComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_containment (d : ReplicationDossier) (h : DossierReady d = true) :
    ContainmentComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_closure (d : ReplicationDossier) (h : DossierReady d = true) :
    ClosureComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.1
theorem readiness_requires_boundary (d : ReplicationDossier) (h : DossierReady d = true) :
    BoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2.2.2

theorem expired_lease_remains_expired_when_time_advances
    (d : ReplicationDossier) (later : Nat) (expired : d.expiresAt < d.currentTick)
    (advances : d.currentTick <= later) : Not (Current { d with currentTick := later }) := by
  intro current
  unfold Current at current
  change later <= d.expiresAt at current
  omega

theorem descendant_overrun_persists_under_growth_and_no_larger_ceiling
    (lease : ReplicationLease) (laterCount laterCeiling : Nat)
    (overrun : lease.descendantCeiling < laterCount)
    (noLarger : laterCeiling <= lease.descendantCeiling) :
    Not (laterCount <= laterCeiling) := by omega

structure ReceiptScope where
  parentId : Nat
  artifactId : Nat
  environmentId : Nat
  protocolVersion : Nat
  expiresAt : Nat
deriving DecidableEq, Repr

def ReceiptUseAllowed (scope : ReceiptScope)
    (parent artifact environment version tick : Nat) : Prop :=
  parent = scope.parentId ∧ artifact = scope.artifactId ∧
  environment = scope.environmentId ∧ version = scope.protocolVersion ∧
  tick <= scope.expiresAt

theorem parent_change_invalidates_replication_receipt
    (scope : ReceiptScope) (parent : Nat) (different : Not (parent = scope.parentId)) :
    Not (ReceiptUseAllowed scope parent scope.artifactId scope.environmentId
      scope.protocolVersion scope.expiresAt) := by intro h; exact different h.1

theorem artifact_change_invalidates_replication_receipt
    (scope : ReceiptScope) (artifact : Nat) (different : Not (artifact = scope.artifactId)) :
    Not (ReceiptUseAllowed scope scope.parentId artifact scope.environmentId
      scope.protocolVersion scope.expiresAt) := by intro h; exact different h.2.1

theorem environment_change_invalidates_replication_receipt
    (scope : ReceiptScope) (environment : Nat)
    (different : Not (environment = scope.environmentId)) :
    Not (ReceiptUseAllowed scope scope.parentId scope.artifactId environment
      scope.protocolVersion scope.expiresAt) := by intro h; exact different h.2.2.1

theorem protocol_change_invalidates_replication_receipt
    (scope : ReceiptScope) (version : Nat)
    (different : Not (version = scope.protocolVersion)) :
    Not (ReceiptUseAllowed scope scope.parentId scope.artifactId scope.environmentId
      version scope.expiresAt) := by intro h; exact different h.2.2.2.1

structure ComponentSignals where
  copyingWorks : Bool
  executionWorks : Bool
  resourceRequestWorks : Bool
  persistenceWorks : Bool
deriving DecidableEq, Repr

structure ReplicationCase where
  signals : ComponentSignals
  identityProvisioningWorks : Bool
  credentialProvisioningWorks : Bool
deriving DecidableEq, Repr

def sharedComponentSignals : ComponentSignals :=
  { copyingWorks := true, executionWorks := true, resourceRequestWorks := true,
    persistenceWorks := true }
def composedReplicationCase : ReplicationCase :=
  { signals := sharedComponentSignals, identityProvisioningWorks := true,
    credentialProvisioningWorks := true }
def brokenCompositionCase : ReplicationCase :=
  { signals := sharedComponentSignals, identityProvisioningWorks := false,
    credentialProvisioningWorks := false }
def EndToEndSyntheticReplication (c : ReplicationCase) : Bool :=
  c.identityProvisioningWorks && c.credentialProvisioningWorks

theorem identical_component_signals_can_hide_opposite_replication_state :
    composedReplicationCase.signals = brokenCompositionCase.signals ∧
    EndToEndSyntheticReplication composedReplicationCase = true ∧
    EndToEndSyntheticReplication brokenCompositionCase = false := by decide

theorem component_signals_cannot_recover_end_to_end_replication
    (classify : ComponentSignals -> Bool) :
    Not (forall c : ReplicationCase, classify c.signals = EndToEndSyntheticReplication c) := by
  intro exact
  have complete := exact composedReplicationCase
  have broken := exact brokenCompositionCase
  simp [composedReplicationCase, brokenCompositionCase, sharedComponentSignals,
    EndToEndSyntheticReplication] at complete broken
  rw [complete] at broken
  contradiction

structure LocalContainmentSignals where
  shutdownAcknowledged : Bool
  credentialsRevoked : Bool
  networkClosed : Bool
  knownCensusComplete : Bool
deriving DecidableEq, Repr

structure ContainmentCase where
  signals : LocalContainmentSignals
  hiddenDescendantExists : Bool
deriving DecidableEq, Repr

def sharedContainmentSignals : LocalContainmentSignals :=
  { shutdownAcknowledged := true, credentialsRevoked := true,
    networkClosed := true, knownCensusComplete := true }
def globallyClosedCase : ContainmentCase :=
  { signals := sharedContainmentSignals, hiddenDescendantExists := false }
def hiddenCopyCase : ContainmentCase :=
  { signals := sharedContainmentSignals, hiddenDescendantExists := true }
def GlobalContainmentState (c : ContainmentCase) : Bool := !c.hiddenDescendantExists

theorem identical_local_containment_signals_can_hide_opposite_global_state :
    globallyClosedCase.signals = hiddenCopyCase.signals ∧
    GlobalContainmentState globallyClosedCase = true ∧
    GlobalContainmentState hiddenCopyCase = false := by decide

theorem local_containment_signals_cannot_recover_global_containment
    (classify : LocalContainmentSignals -> Bool) :
    Not (forall c : ContainmentCase, classify c.signals = GlobalContainmentState c) := by
  intro exact
  have closed := exact globallyClosedCase
  have hidden := exact hiddenCopyCase
  simp [globallyClosedCase, hiddenCopyCase, sharedContainmentSignals,
    GlobalContainmentState] at closed hidden
  rw [closed] at hidden
  contradiction

def toOperationsPacket (d : ReplicationDossier) : GovernedOperationsRefinement.Packet :=
  { GovernedOperationsRefinement.canonicalPacket 5 with
    descendantsComplete := false
    containmentObserved := d.shutdownObserved
    containmentIndependent := d.independentKillPathPresent
    effectsEnumerated := d.affectedPathsNotified
    effectsDispositionComplete := d.artifactsDispositioned
    residualOwnerAccepted := d.residualOwnerPresent }

theorem unresolved_descendants_force_operations_state_inventory
    (d : ReplicationDossier) :
    GovernedOperationsRefinement.routeFor
      (GovernedOperationsRefinement.canonicalState .degraded)
      .reconcileStateAndEffects (toOperationsPacket d) = .requestStateInventory := by
  simp [toOperationsPacket, GovernedOperationsRefinement.routeFor,
    GovernedOperationsRefinement.expectedKind,
    GovernedOperationsRefinement.identityMatches,
    GovernedOperationsRefinement.authorityLeakRequested,
    GovernedOperationsRefinement.canonicalState,
    GovernedOperationsRefinement.canonicalPacket]

end AsiStackProofs.ReplicationContainmentReview

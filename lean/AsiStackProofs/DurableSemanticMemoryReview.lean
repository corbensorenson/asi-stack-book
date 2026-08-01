import AsiStackProofs.ContextTransactions

namespace AsiStackProofs.DurableSemanticMemoryReview

/-!
A bounded review model for durable semantic memory. The model proves custody,
revision, migration, retrieval, replay, and non-substitution properties over
authored records. It does not establish truth, useful recall, complete memory,
behavioral forgetting, or release readiness.
-/

inductive EvidenceKind where
  | retrievalBenchmark | persistenceReplay | storageDeletionReceipt | graphConnectivity
deriving DecidableEq, Repr

inductive ClaimClass where
  | boundedRetrievalUtility | restartReproduction | storageDeletion | graphReachability
  | semanticTruth | completeMemory | behavioralForgetting | decisionAuthority
deriving DecidableEq, Repr

def establishes : EvidenceKind -> ClaimClass -> Bool
  | .retrievalBenchmark, .boundedRetrievalUtility => true
  | .persistenceReplay, .restartReproduction => true
  | .storageDeletionReceipt, .storageDeletion => true
  | .graphConnectivity, .graphReachability => true
  | _, _ => false

theorem retrieval_benchmark_does_not_establish_semantic_truth :
    establishes .retrievalBenchmark .semanticTruth = false := by rfl
theorem persistence_replay_does_not_establish_complete_memory :
    establishes .persistenceReplay .completeMemory = false := by rfl
theorem storage_deletion_does_not_establish_behavioral_forgetting :
    establishes .storageDeletionReceipt .behavioralForgetting = false := by rfl
theorem graph_connectivity_does_not_establish_decision_authority :
    establishes .graphConnectivity .decisionAuthority = false := by rfl

structure SemanticIdentity where
  objectId : Nat
  aliasDigest : Nat
  representationDigest : Nat
deriving DecidableEq, Repr

def rebuildRepresentation
    (identity : SemanticIdentity) (newAlias newRepresentation : Nat) : SemanticIdentity :=
  { identity with aliasDigest := newAlias, representationDigest := newRepresentation }

theorem representation_rebuild_preserves_semantic_object_identity
    (identity : SemanticIdentity) (newAlias newRepresentation : Nat) :
    (rebuildRepresentation identity newAlias newRepresentation).objectId = identity.objectId := by
  rfl

theorem equal_aliases_do_not_force_equal_semantic_objects :
    let left : SemanticIdentity := ⟨1, 7, 11⟩
    let right : SemanticIdentity := ⟨2, 7, 11⟩
    left.aliasDigest = right.aliasDigest ∧ left.objectId ≠ right.objectId := by decide

structure ParentRecord where
  objectId : Nat
  provenanceIds : List Nat
  permittedPurposes : List Nat
deriving DecidableEq, Repr

def collectProvenance : List ParentRecord -> List Nat
  | [] => []
  | parent :: tail => parent.provenanceIds ++ collectProvenance tail

theorem every_parent_provenance_id_survives_collection
    (parents : List ParentRecord) (parent : ParentRecord) (sourceId : Nat)
    (parentMember : parent ∈ parents) (sourceMember : sourceId ∈ parent.provenanceIds) :
    sourceId ∈ collectProvenance parents := by
  induction parents with
  | nil => simp at parentMember
  | cons head tail ih =>
      simp only [List.mem_cons] at parentMember
      simp only [collectProvenance, List.mem_append]
      rcases parentMember with same | rest
      · subst parent; exact Or.inl sourceMember
      · exact Or.inr (ih rest)

def ParentAuthorizes (parent : ParentRecord) (purpose : Nat) : Bool :=
  decide (purpose ∈ parent.permittedPurposes)

def AllParentsAuthorize : List ParentRecord -> Nat -> Bool
  | [], _ => true
  | parent :: tail, purpose => ParentAuthorizes parent purpose && AllParentsAuthorize tail purpose

theorem derived_use_cannot_exceed_any_parent_authority
    (parents : List ParentRecord) (parent : ParentRecord) (purpose : Nat)
    (allAuthorize : AllParentsAuthorize parents purpose = true)
    (parentMember : parent ∈ parents) : ParentAuthorizes parent purpose = true := by
  induction parents with
  | nil => simp at parentMember
  | cons head tail ih =>
      simp only [AllParentsAuthorize, Bool.and_eq_true] at allAuthorize
      simp only [List.mem_cons] at parentMember
      rcases parentMember with same | rest
      · subst parent; exact allAuthorize.1
      · exact ih allAuthorize.2 rest

structure MigrationEntry where
  objectId : Nat
  mappedExactly : Bool
  lossRecorded : Bool
  affectedConsumersInvalidated : Bool
deriving DecidableEq, Repr

def MigrationEntryAdmissible (entry : MigrationEntry) : Prop :=
  entry.mappedExactly = true ∨
    (entry.lossRecorded = true ∧ entry.affectedConsumersInvalidated = true)

def MigrationAdmissible (entries : List MigrationEntry) : Prop :=
  forall entry, entry ∈ entries -> MigrationEntryAdmissible entry

theorem lossy_migration_without_consumer_invalidation_is_rejected
    (entries : List MigrationEntry) (entry : MigrationEntry)
    (member : entry ∈ entries) (notExact : entry.mappedExactly = false)
    (_lossy : entry.lossRecorded = true)
    (notInvalidated : entry.affectedConsumersInvalidated = false) :
    Not (MigrationAdmissible entries) := by
  intro admissible
  rcases admissible entry member with exact | residual
  · rw [notExact] at exact; contradiction
  · simp [notInvalidated] at residual

structure RetrievalCandidate where
  objectId : Nat
  provenancePresent : Bool
  supportCurrent : Bool
  rightsAllowUse : Bool
  contradictionStateIncluded : Bool
  retracted : Bool
deriving DecidableEq, Repr

def CandidateAdmissible (candidate : RetrievalCandidate) : Prop :=
  candidate.provenancePresent = true ∧ candidate.supportCurrent = true ∧
  candidate.rightsAllowUse = true ∧ candidate.contradictionStateIncluded = true ∧
  candidate.retracted = false

def RetrievalUseReceipt
    (candidates : List RetrievalCandidate) (usedObjectIds : List Nat) : Prop :=
  forall objectId, objectId ∈ usedObjectIds ->
    exists candidate, candidate ∈ candidates ∧ candidate.objectId = objectId ∧
      CandidateAdmissible candidate

theorem every_used_object_has_current_authorized_provenance
    (candidates : List RetrievalCandidate) (usedObjectIds : List Nat)
    (receipt : RetrievalUseReceipt candidates usedObjectIds)
    (objectId : Nat) (used : objectId ∈ usedObjectIds) :
    exists candidate, candidate ∈ candidates ∧ candidate.objectId = objectId ∧
      candidate.provenancePresent = true ∧ candidate.supportCurrent = true ∧
      candidate.rightsAllowUse = true := by
  rcases receipt objectId used with ⟨candidate, member, same, admissible⟩
  exact ⟨candidate, member, same, admissible.1, admissible.2.1, admissible.2.2.1⟩

structure MemoryState where
  eventDigests : List Nat
  version : Nat
deriving DecidableEq, Repr

structure MemoryEvent where
  digest : Nat
deriving DecidableEq, Repr

def applyMemoryEvent (state : MemoryState) (event : MemoryEvent) : MemoryState :=
  { eventDigests := state.eventDigests ++ [event.digest], version := state.version + 1 }

def replayMemory : MemoryState -> List MemoryEvent -> MemoryState
  | state, [] => state
  | state, event :: tail => replayMemory (applyMemoryEvent state event) tail

theorem replay_append_composes_exactly
    (state : MemoryState) (before after : List MemoryEvent) :
    replayMemory state (before ++ after) = replayMemory (replayMemory state before) after := by
  induction before generalizing state with
  | nil => rfl
  | cons head tail ih => simp [replayMemory, ih]

structure MemoryDossier where
  semanticObjectIdBound : Bool := true
  sourceOccurrenceIdBound : Bool := true
  aliasCollisionRecorded : Bool := true
  ontologyVersionBound : Bool := true
  relationSchemaVersionBound : Bool := true
  evidenceEpochBound : Bool := true
  provenanceComplete : Bool := true
  temporalValidityBound : Bool := true
  supportStateBound : Bool := true
  contradictionsRetained : Bool := true
  supersessionLineagePresent : Bool := true
  rightsBound : Bool := true
  dependencyIndexComplete : Bool := true
  migrationMappingComplete : Bool := true
  unmappedCasesRecorded : Bool := true
  lossyCasesRecorded : Bool := true
  affectedConsumersIndexed : Bool := true
  consumerInvalidationPlanned : Bool := true
  rollbackOrDualReadPresent : Bool := true
  retrievalPlanBound : Bool := true
  consumerPurposeBound : Bool := true
  freshnessChecked : Bool := true
  rightsChecked : Bool := true
  contradictionsIncluded : Bool := true
  selectionReasonsRecorded : Bool := true
  useReceiptPresent : Bool := true
  compactionLineagePresent : Bool := true
  retentionPolicyBound : Bool := true
  deletionDutiesBound : Bool := true
  backupStateBound : Bool := true
  restartReplayTested : Bool := true
  recoveryResidualRecorded : Bool := true
  descendantRepairPlanPresent : Bool := true
  currentTick : Nat := 10
  expiresAt : Nat := 20
  semanticTruthClaimed : Bool := false
  completeMemoryClaimed : Bool := false
  behavioralForgettingClaimed : Bool := false
  supportOrReleaseRequested : Bool := false
deriving DecidableEq, Repr

def Current (d : MemoryDossier) : Prop := d.currentTick <= d.expiresAt
instance currentDecidable (d : MemoryDossier) : Decidable (Current d) := by
  unfold Current; infer_instance

def IdentityComplete (d : MemoryDossier) : Prop :=
  d.semanticObjectIdBound = true ∧ d.sourceOccurrenceIdBound = true ∧
  d.aliasCollisionRecorded = true ∧ d.ontologyVersionBound = true ∧
  d.relationSchemaVersionBound = true ∧ d.evidenceEpochBound = true
def RevisionComplete (d : MemoryDossier) : Prop :=
  d.provenanceComplete = true ∧ d.temporalValidityBound = true ∧
  d.supportStateBound = true ∧ d.contradictionsRetained = true ∧
  d.supersessionLineagePresent = true ∧ d.rightsBound = true ∧
  d.dependencyIndexComplete = true
def MigrationComplete (d : MemoryDossier) : Prop :=
  d.migrationMappingComplete = true ∧ d.unmappedCasesRecorded = true ∧
  d.lossyCasesRecorded = true ∧ d.affectedConsumersIndexed = true ∧
  d.consumerInvalidationPlanned = true ∧ d.rollbackOrDualReadPresent = true
def RetrievalComplete (d : MemoryDossier) : Prop :=
  d.retrievalPlanBound = true ∧ d.consumerPurposeBound = true ∧
  d.freshnessChecked = true ∧ d.rightsChecked = true ∧
  d.contradictionsIncluded = true ∧ d.selectionReasonsRecorded = true ∧
  d.useReceiptPresent = true
def RetentionComplete (d : MemoryDossier) : Prop :=
  d.compactionLineagePresent = true ∧ d.retentionPolicyBound = true ∧
  d.deletionDutiesBound = true ∧ d.backupStateBound = true ∧
  d.restartReplayTested = true ∧ d.recoveryResidualRecorded = true ∧
  d.descendantRepairPlanPresent = true ∧ Current d
def BoundaryComplete (d : MemoryDossier) : Prop :=
  d.semanticTruthClaimed = false ∧ d.completeMemoryClaimed = false ∧
  d.behavioralForgettingClaimed = false ∧ d.supportOrReleaseRequested = false

instance identityDecidable (d : MemoryDossier) : Decidable (IdentityComplete d) := by unfold IdentityComplete; infer_instance
instance revisionDecidable (d : MemoryDossier) : Decidable (RevisionComplete d) := by unfold RevisionComplete; infer_instance
instance migrationDecidable (d : MemoryDossier) : Decidable (MigrationComplete d) := by unfold MigrationComplete; infer_instance
instance retrievalDecidable (d : MemoryDossier) : Decidable (RetrievalComplete d) := by unfold RetrievalComplete; infer_instance
instance retentionDecidable (d : MemoryDossier) : Decidable (RetentionComplete d) := by unfold RetentionComplete Current; infer_instance
instance boundaryDecidable (d : MemoryDossier) : Decidable (BoundaryComplete d) := by unfold BoundaryComplete; infer_instance

def DossierAdmissible (d : MemoryDossier) : Prop :=
  IdentityComplete d ∧ RevisionComplete d ∧ MigrationComplete d ∧
  RetrievalComplete d ∧ RetentionComplete d ∧ BoundaryComplete d
instance admissibleDecidable (d : MemoryDossier) : Decidable (DossierAdmissible d) := by
  unfold DossierAdmissible IdentityComplete RevisionComplete MigrationComplete
    RetrievalComplete RetentionComplete Current BoundaryComplete
  infer_instance
def DossierReady (d : MemoryDossier) : Bool := decide (DossierAdmissible d)

inductive ReviewState where
  | proposed | identityReviewed | revisionReviewed | migrationReviewed | retrievalReviewed
  | retentionReviewed | boundaryReviewed | repairRequired | eligibleForTheseusMemoryReplay
deriving DecidableEq, Repr

def ReviewStepFor (d : MemoryDossier) : ReviewState -> ReviewState
  | .proposed => if decide (IdentityComplete d) then .identityReviewed else .repairRequired
  | .identityReviewed => if decide (RevisionComplete d) then .revisionReviewed else .repairRequired
  | .revisionReviewed => if decide (MigrationComplete d) then .migrationReviewed else .repairRequired
  | .migrationReviewed => if decide (RetrievalComplete d) then .retrievalReviewed else .repairRequired
  | .retrievalReviewed => if decide (RetentionComplete d) then .retentionReviewed else .repairRequired
  | .retentionReviewed => if decide (BoundaryComplete d) then .boundaryReviewed else .repairRequired
  | .boundaryReviewed => .eligibleForTheseusMemoryReplay
  | state => state
def ReviewRun (d : MemoryDossier) : Nat -> ReviewState
  | 0 => .proposed
  | n + 1 => ReviewStepFor d (ReviewRun d n)
def StageInvariant (d : MemoryDossier) : ReviewState -> Prop
  | .proposed => True
  | .identityReviewed => IdentityComplete d
  | .revisionReviewed => IdentityComplete d ∧ RevisionComplete d
  | .migrationReviewed => IdentityComplete d ∧ RevisionComplete d ∧ MigrationComplete d
  | .retrievalReviewed => IdentityComplete d ∧ RevisionComplete d ∧ MigrationComplete d ∧ RetrievalComplete d
  | .retentionReviewed => IdentityComplete d ∧ RevisionComplete d ∧ MigrationComplete d ∧ RetrievalComplete d ∧ RetentionComplete d
  | .boundaryReviewed | .eligibleForTheseusMemoryReplay => DossierAdmissible d
  | .repairRequired => True

theorem review_step_preserves_stage_invariant
    (d : MemoryDossier) (state : ReviewState) (h : StageInvariant d state) :
    StageInvariant d (ReviewStepFor d state) := by
  cases state <;> simp only [ReviewStepFor]
  case proposed => split <;> simp_all [StageInvariant]
  case identityReviewed => split <;> simp_all [StageInvariant]
  case revisionReviewed => split <;> simp_all [StageInvariant]
  case migrationReviewed => split <;> simp_all [StageInvariant]
  case retrievalReviewed => split <;> simp_all [StageInvariant]
  case retentionReviewed => split <;> simp_all [StageInvariant, DossierAdmissible]
  all_goals simp_all [StageInvariant]

theorem review_run_preserves_stage_invariant (d : MemoryDossier) (n : Nat) :
    StageInvariant d (ReviewRun d n) := by
  induction n with
  | zero => simp [ReviewRun, StageInvariant]
  | succ n ih => simpa [ReviewRun] using review_step_preserves_stage_invariant d _ ih

theorem replay_eligibility_requires_admissible_dossier
    (d : MemoryDossier) (n : Nat)
    (h : ReviewRun d n = .eligibleForTheseusMemoryReplay) : DossierAdmissible d := by
  have invariant := review_run_preserves_stage_invariant d n
  simpa [h, StageInvariant] using invariant

def completeDossier : MemoryDossier := {}
theorem complete_dossier_is_ready : DossierReady completeDossier = true := by decide
theorem complete_dossier_reaches_only_theseus_memory_replay :
    ReviewRun completeDossier 7 = .eligibleForTheseusMemoryReplay := by decide

inductive AdmissionAxis where
  | semanticObjectId | sourceOccurrenceId | aliasCollision | ontologyVersion
  | relationSchemaVersion | evidenceEpoch | provenance | temporalValidity | supportState
  | contradictions | supersessionLineage | rights | dependencyIndex | migrationMapping
  | unmappedCases | lossyCases | affectedConsumers | consumerInvalidation | rollbackOrDualRead
  | retrievalPlan | consumerPurpose | freshness | rightsCheck | contradictionInclusion
  | selectionReasons | useReceipt | compactionLineage | retentionPolicy | deletionDuties
  | backupState | restartReplay | recoveryResidual | descendantRepair | expiry
  | semanticTruthClaim | completeMemoryClaim | behavioralForgettingClaim | supportOrRelease
deriving DecidableEq, Repr

def omitAxis : AdmissionAxis -> MemoryDossier
  | .semanticObjectId => { completeDossier with semanticObjectIdBound := false }
  | .sourceOccurrenceId => { completeDossier with sourceOccurrenceIdBound := false }
  | .aliasCollision => { completeDossier with aliasCollisionRecorded := false }
  | .ontologyVersion => { completeDossier with ontologyVersionBound := false }
  | .relationSchemaVersion => { completeDossier with relationSchemaVersionBound := false }
  | .evidenceEpoch => { completeDossier with evidenceEpochBound := false }
  | .provenance => { completeDossier with provenanceComplete := false }
  | .temporalValidity => { completeDossier with temporalValidityBound := false }
  | .supportState => { completeDossier with supportStateBound := false }
  | .contradictions => { completeDossier with contradictionsRetained := false }
  | .supersessionLineage => { completeDossier with supersessionLineagePresent := false }
  | .rights => { completeDossier with rightsBound := false }
  | .dependencyIndex => { completeDossier with dependencyIndexComplete := false }
  | .migrationMapping => { completeDossier with migrationMappingComplete := false }
  | .unmappedCases => { completeDossier with unmappedCasesRecorded := false }
  | .lossyCases => { completeDossier with lossyCasesRecorded := false }
  | .affectedConsumers => { completeDossier with affectedConsumersIndexed := false }
  | .consumerInvalidation => { completeDossier with consumerInvalidationPlanned := false }
  | .rollbackOrDualRead => { completeDossier with rollbackOrDualReadPresent := false }
  | .retrievalPlan => { completeDossier with retrievalPlanBound := false }
  | .consumerPurpose => { completeDossier with consumerPurposeBound := false }
  | .freshness => { completeDossier with freshnessChecked := false }
  | .rightsCheck => { completeDossier with rightsChecked := false }
  | .contradictionInclusion => { completeDossier with contradictionsIncluded := false }
  | .selectionReasons => { completeDossier with selectionReasonsRecorded := false }
  | .useReceipt => { completeDossier with useReceiptPresent := false }
  | .compactionLineage => { completeDossier with compactionLineagePresent := false }
  | .retentionPolicy => { completeDossier with retentionPolicyBound := false }
  | .deletionDuties => { completeDossier with deletionDutiesBound := false }
  | .backupState => { completeDossier with backupStateBound := false }
  | .restartReplay => { completeDossier with restartReplayTested := false }
  | .recoveryResidual => { completeDossier with recoveryResidualRecorded := false }
  | .descendantRepair => { completeDossier with descendantRepairPlanPresent := false }
  | .expiry => { completeDossier with currentTick := 21 }
  | .semanticTruthClaim => { completeDossier with semanticTruthClaimed := true }
  | .completeMemoryClaim => { completeDossier with completeMemoryClaimed := true }
  | .behavioralForgettingClaim => { completeDossier with behavioralForgettingClaimed := true }
  | .supportOrRelease => { completeDossier with supportOrReleaseRequested := true }

inductive RepairDisposition where
  | bindSemanticObjectId | bindSourceOccurrenceId | recordAliasCollision
  | bindOntologyVersion | bindRelationSchemaVersion | bindEvidenceEpoch
  | completeProvenance | bindTemporalValidity | bindSupportState | retainContradictions
  | addSupersessionLineage | bindRights | completeDependencyIndex | completeMigrationMapping
  | recordUnmappedCases | recordLossyCases | indexAffectedConsumers
  | planConsumerInvalidation | addRollbackOrDualRead | bindRetrievalPlan
  | bindConsumerPurpose | checkFreshness | checkRights | includeContradictions
  | recordSelectionReasons | addUseReceipt | addCompactionLineage | bindRetentionPolicy
  | bindDeletionDuties | bindBackupState | testRestartReplay | recordRecoveryResidual
  | planDescendantRepair | renewExpiry | rejectSemanticTruthClaim
  | rejectCompleteMemoryClaim | rejectBehavioralForgettingClaim | refuseSupportOrRelease
  | eligibleForTheseusMemoryReplay
deriving DecidableEq, Repr

def repairForAxis : AdmissionAxis -> RepairDisposition
  | .semanticObjectId => .bindSemanticObjectId | .sourceOccurrenceId => .bindSourceOccurrenceId
  | .aliasCollision => .recordAliasCollision | .ontologyVersion => .bindOntologyVersion
  | .relationSchemaVersion => .bindRelationSchemaVersion | .evidenceEpoch => .bindEvidenceEpoch
  | .provenance => .completeProvenance | .temporalValidity => .bindTemporalValidity
  | .supportState => .bindSupportState | .contradictions => .retainContradictions
  | .supersessionLineage => .addSupersessionLineage | .rights => .bindRights
  | .dependencyIndex => .completeDependencyIndex | .migrationMapping => .completeMigrationMapping
  | .unmappedCases => .recordUnmappedCases | .lossyCases => .recordLossyCases
  | .affectedConsumers => .indexAffectedConsumers | .consumerInvalidation => .planConsumerInvalidation
  | .rollbackOrDualRead => .addRollbackOrDualRead | .retrievalPlan => .bindRetrievalPlan
  | .consumerPurpose => .bindConsumerPurpose | .freshness => .checkFreshness
  | .rightsCheck => .checkRights | .contradictionInclusion => .includeContradictions
  | .selectionReasons => .recordSelectionReasons | .useReceipt => .addUseReceipt
  | .compactionLineage => .addCompactionLineage | .retentionPolicy => .bindRetentionPolicy
  | .deletionDuties => .bindDeletionDuties | .backupState => .bindBackupState
  | .restartReplay => .testRestartReplay | .recoveryResidual => .recordRecoveryResidual
  | .descendantRepair => .planDescendantRepair | .expiry => .renewExpiry
  | .semanticTruthClaim => .rejectSemanticTruthClaim
  | .completeMemoryClaim => .rejectCompleteMemoryClaim
  | .behavioralForgettingClaim => .rejectBehavioralForgettingClaim
  | .supportOrRelease => .refuseSupportOrRelease

def ExactRepairFor (d : MemoryDossier) : RepairDisposition :=
  if !d.semanticObjectIdBound then .bindSemanticObjectId
  else if !d.sourceOccurrenceIdBound then .bindSourceOccurrenceId
  else if !d.aliasCollisionRecorded then .recordAliasCollision
  else if !d.ontologyVersionBound then .bindOntologyVersion
  else if !d.relationSchemaVersionBound then .bindRelationSchemaVersion
  else if !d.evidenceEpochBound then .bindEvidenceEpoch
  else if !d.provenanceComplete then .completeProvenance
  else if !d.temporalValidityBound then .bindTemporalValidity
  else if !d.supportStateBound then .bindSupportState
  else if !d.contradictionsRetained then .retainContradictions
  else if !d.supersessionLineagePresent then .addSupersessionLineage
  else if !d.rightsBound then .bindRights
  else if !d.dependencyIndexComplete then .completeDependencyIndex
  else if !d.migrationMappingComplete then .completeMigrationMapping
  else if !d.unmappedCasesRecorded then .recordUnmappedCases
  else if !d.lossyCasesRecorded then .recordLossyCases
  else if !d.affectedConsumersIndexed then .indexAffectedConsumers
  else if !d.consumerInvalidationPlanned then .planConsumerInvalidation
  else if !d.rollbackOrDualReadPresent then .addRollbackOrDualRead
  else if !d.retrievalPlanBound then .bindRetrievalPlan
  else if !d.consumerPurposeBound then .bindConsumerPurpose
  else if !d.freshnessChecked then .checkFreshness
  else if !d.rightsChecked then .checkRights
  else if !d.contradictionsIncluded then .includeContradictions
  else if !d.selectionReasonsRecorded then .recordSelectionReasons
  else if !d.useReceiptPresent then .addUseReceipt
  else if !d.compactionLineagePresent then .addCompactionLineage
  else if !d.retentionPolicyBound then .bindRetentionPolicy
  else if !d.deletionDutiesBound then .bindDeletionDuties
  else if !d.backupStateBound then .bindBackupState
  else if !d.restartReplayTested then .testRestartReplay
  else if !d.recoveryResidualRecorded then .recordRecoveryResidual
  else if !d.descendantRepairPlanPresent then .planDescendantRepair
  else if !decide (Current d) then .renewExpiry
  else if d.semanticTruthClaimed then .rejectSemanticTruthClaim
  else if d.completeMemoryClaimed then .rejectCompleteMemoryClaim
  else if d.behavioralForgettingClaimed then .rejectBehavioralForgettingClaim
  else if d.supportOrReleaseRequested then .refuseSupportOrRelease
  else .eligibleForTheseusMemoryReplay

theorem every_admission_axis_mutation_blocks_readiness (axis : AdmissionAxis) :
    DossierReady (omitAxis axis) = false := by cases axis <;> decide
theorem every_admission_axis_mutation_has_exact_repair (axis : AdmissionAxis) :
    ExactRepairFor (omitAxis axis) = repairForAxis axis := by cases axis <;> decide
theorem every_admission_axis_mutation_reaches_repair (axis : AdmissionAxis) :
    ReviewRun (omitAxis axis) 7 = .repairRequired := by cases axis <;> decide

theorem readiness_requires_identity (d : MemoryDossier) (h : DossierReady d = true) : IdentityComplete d := by exact (of_decide_eq_true h).1
theorem readiness_requires_revision (d : MemoryDossier) (h : DossierReady d = true) : RevisionComplete d := by exact (of_decide_eq_true h).2.1
theorem readiness_requires_migration (d : MemoryDossier) (h : DossierReady d = true) : MigrationComplete d := by exact (of_decide_eq_true h).2.2.1
theorem readiness_requires_retrieval (d : MemoryDossier) (h : DossierReady d = true) : RetrievalComplete d := by exact (of_decide_eq_true h).2.2.2.1
theorem readiness_requires_retention (d : MemoryDossier) (h : DossierReady d = true) : RetentionComplete d := by exact (of_decide_eq_true h).2.2.2.2.1
theorem readiness_requires_boundary (d : MemoryDossier) (h : DossierReady d = true) : BoundaryComplete d := by exact (of_decide_eq_true h).2.2.2.2.2

theorem expired_memory_contract_remains_expired_when_time_advances
    (d : MemoryDossier) (later : Nat) (expired : d.expiresAt < d.currentTick)
    (advances : d.currentTick <= later) : Not (Current { d with currentTick := later }) := by
  intro current; unfold Current at current; change later <= d.expiresAt at current; omega

structure ReceiptScope where
  objectId : Nat
  ontologyVersion : Nat
  evidenceEpoch : Nat
  consumerPurpose : Nat
deriving DecidableEq, Repr

def ReceiptUseAllowed (s : ReceiptScope) (object ontology epoch purpose : Nat) : Prop :=
  object = s.objectId ∧ ontology = s.ontologyVersion ∧
  epoch = s.evidenceEpoch ∧ purpose = s.consumerPurpose

theorem object_change_invalidates_memory_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.objectId)) :
    Not (ReceiptUseAllowed s v s.ontologyVersion s.evidenceEpoch s.consumerPurpose) := by intro x; exact h x.1
theorem ontology_change_invalidates_memory_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.ontologyVersion)) :
    Not (ReceiptUseAllowed s s.objectId v s.evidenceEpoch s.consumerPurpose) := by intro x; exact h x.2.1
theorem evidence_epoch_change_invalidates_memory_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.evidenceEpoch)) :
    Not (ReceiptUseAllowed s s.objectId s.ontologyVersion v s.consumerPurpose) := by intro x; exact h x.2.2.1
theorem consumer_purpose_change_invalidates_memory_receipt
    (s : ReceiptScope) (v : Nat) (h : Not (v = s.consumerPurpose)) :
    Not (ReceiptUseAllowed s s.objectId s.ontologyVersion s.evidenceEpoch v) := by intro x; exact h x.2.2.2

structure SummarySignals where
  summaryDigest : Nat
  retrievalScore : Nat
deriving DecidableEq, Repr
structure HistoryCase where
  signals : SummarySignals
  unresolvedContradiction : Bool
deriving DecidableEq, Repr
def sharedSummarySignals : SummarySignals := ⟨7, 91⟩
def conflictFreeCase : HistoryCase := ⟨sharedSummarySignals, false⟩
def hiddenConflictCase : HistoryCase := ⟨sharedSummarySignals, true⟩
def ConflictFree (c : HistoryCase) : Bool := !c.unresolvedContradiction
theorem identical_summary_signals_can_hide_opposite_contradiction_state :
    conflictFreeCase.signals = hiddenConflictCase.signals ∧
    ConflictFree conflictFreeCase = true ∧ ConflictFree hiddenConflictCase = false := by decide
theorem summary_signals_cannot_recover_contradiction_state (classify : SummarySignals -> Bool) :
    Not (forall c : HistoryCase, classify c.signals = ConflictFree c) := by
  intro exact; have a := exact conflictFreeCase; have b := exact hiddenConflictCase
  simp [conflictFreeCase, hiddenConflictCase, sharedSummarySignals, ConflictFree] at a b
  rw [a] at b; contradiction

structure DeletionSignals where
  storageObjectAbsent : Bool
  retrievalIndexAbsent : Bool
  backupTombstonePresent : Bool
deriving DecidableEq, Repr
structure ForgettingCase where
  signals : DeletionSignals
  learnedInfluenceAbsent : Bool
deriving DecidableEq, Repr
def sharedDeletionSignals : DeletionSignals := ⟨true, true, true⟩
def unlearnedCase : ForgettingCase := ⟨sharedDeletionSignals, true⟩
def influencePersistsCase : ForgettingCase := ⟨sharedDeletionSignals, false⟩
def BehaviorallyForgotten (c : ForgettingCase) : Bool := c.learnedInfluenceAbsent
theorem identical_deletion_signals_can_hide_opposite_learned_influence :
    unlearnedCase.signals = influencePersistsCase.signals ∧
    BehaviorallyForgotten unlearnedCase = true ∧
    BehaviorallyForgotten influencePersistsCase = false := by decide
theorem deletion_signals_cannot_recover_behavioral_forgetting (classify : DeletionSignals -> Bool) :
    Not (forall c : ForgettingCase, classify c.signals = BehaviorallyForgotten c) := by
  intro exact; have a := exact unlearnedCase; have b := exact influencePersistsCase
  simp [unlearnedCase, influencePersistsCase, sharedDeletionSignals, BehaviorallyForgotten] at a b
  rw [a] at b; contradiction

def toContextMaterializationRecord
    (d : MemoryDossier) : ContextTransactions.ContextMaterializationRecord :=
  { materializationReady := d.useReceiptPresent
    deletionObligationOpen := d.deletionDutiesBound
    deletionClosureRecorded := false
    declassificationAuthorized := false
    residualRecordPresent := d.recoveryResidualRecorded
    nonClaimsPresent := !d.semanticTruthClaimed }

theorem open_memory_deletion_duty_blocks_context_materialization
    (d : MemoryDossier) (ready : d.useReceiptPresent = true)
    (openDuty : d.deletionDutiesBound = true) :
    ContextTransactions.ContextMaterializationRouteFor (toContextMaterializationRecord d) =
      .blockForDeletionClosure := by
  apply ContextTransactions.ready_open_deletion_without_closure_routes_to_deletion_block
  · simpa [toContextMaterializationRecord] using ready
  · simpa [toContextMaterializationRecord] using openDuty
  · rfl
  · rfl

end AsiStackProofs.DurableSemanticMemoryReview

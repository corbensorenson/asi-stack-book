namespace AsiStackProofs.DataEngines

inductive DataAdmissionDecision where
  | block
  | quarantine
  | experimentalOnly
  | eligible
deriving DecidableEq, Repr

structure DataAdmissionReview where
  provenanceRecorded : Bool
  authorityRecorded : Bool
  splitExclusionsRecorded : Bool
  contaminationCheckRecorded : Bool
  retentionPolicyRecorded : Bool
  deletionScopeRecorded : Bool
  evaluationRefsPresent : Bool
  residualsRecorded : Bool
  decision : DataAdmissionDecision
deriving DecidableEq, Repr

def DataAdmissionComplete (review : DataAdmissionReview) : Prop :=
  review.provenanceRecorded = true ∧
    review.authorityRecorded = true ∧
      review.splitExclusionsRecorded = true ∧
        review.contaminationCheckRecorded = true ∧
          review.retentionPolicyRecorded = true ∧
            review.deletionScopeRecorded = true ∧
              review.evaluationRefsPresent = true ∧
                review.residualsRecorded = true

def DataAdmissionRouteFor (review : DataAdmissionReview) : DataAdmissionDecision :=
  if review.provenanceRecorded = false ∨ review.authorityRecorded = false then
    DataAdmissionDecision.block
  else if review.splitExclusionsRecorded = false ∨ review.contaminationCheckRecorded = false then
    DataAdmissionDecision.quarantine
  else if review.retentionPolicyRecorded = false ∨ review.deletionScopeRecorded = false ∨
      review.evaluationRefsPresent = false ∨ review.residualsRecorded = false then
    DataAdmissionDecision.experimentalOnly
  else
    DataAdmissionDecision.eligible

theorem missing_provenance_or_authority_blocks_data_admission
    {review : DataAdmissionReview} :
    review.provenanceRecorded = false ∨ review.authorityRecorded = false ->
    DataAdmissionRouteFor review = DataAdmissionDecision.block := by
  intro missing
  unfold DataAdmissionRouteFor
  simp [missing]

theorem missing_split_exclusion_or_contamination_check_quarantines_data
    {review : DataAdmissionReview} :
    review.provenanceRecorded = true ->
    review.authorityRecorded = true ->
    (review.splitExclusionsRecorded = false ∨ review.contaminationCheckRecorded = false) ->
    DataAdmissionRouteFor review = DataAdmissionDecision.quarantine := by
  intro provenance authority missing
  unfold DataAdmissionRouteFor
  simp [provenance, authority, missing]

theorem complete_data_record_routes_to_eligible
    {review : DataAdmissionReview} :
    DataAdmissionComplete review ->
    DataAdmissionRouteFor review = DataAdmissionDecision.eligible := by
  intro complete
  rcases complete with ⟨provenance, authority, exclusions, contamination,
    retention, deletion, evaluation, residuals⟩
  simp [DataAdmissionRouteFor, provenance, authority, exclusions, contamination,
    retention, deletion, evaluation, residuals]

inductive FullStateUpdateRoute where
  | requireInventoryRepair
  | requireCheckpointAuthorityRepair
  | requireRollbackRepair
  | releaseToEvidenceReview
deriving DecidableEq, Repr

structure FullStateUpdateReview where
  modelStateRecorded : Bool
  optimizerStateRecorded : Bool
  schedulerStateRecorded : Bool
  rngStateRecorded : Bool
  cacheStateRecorded : Bool
  backupStateRecorded : Bool
  descendantStateRecorded : Bool
  prospectiveCheckpointAuthorityRecorded : Bool
  rollbackExactRecorded : Bool
deriving DecidableEq, Repr

def FullStateUpdateRouteFor (review : FullStateUpdateReview) : FullStateUpdateRoute :=
  if review.modelStateRecorded = false ∨ review.optimizerStateRecorded = false ∨
      review.schedulerStateRecorded = false ∨ review.rngStateRecorded = false ∨
      review.cacheStateRecorded = false ∨ review.backupStateRecorded = false ∨
      review.descendantStateRecorded = false then
    FullStateUpdateRoute.requireInventoryRepair
  else if review.prospectiveCheckpointAuthorityRecorded = false then
    FullStateUpdateRoute.requireCheckpointAuthorityRepair
  else if review.rollbackExactRecorded = false then
    FullStateUpdateRoute.requireRollbackRepair
  else
    FullStateUpdateRoute.releaseToEvidenceReview

theorem complete_full_state_update_reaches_evidence_review
    {review : FullStateUpdateReview} :
    review.modelStateRecorded = true ->
    review.optimizerStateRecorded = true ->
    review.schedulerStateRecorded = true ->
    review.rngStateRecorded = true ->
    review.cacheStateRecorded = true ->
    review.backupStateRecorded = true ->
    review.descendantStateRecorded = true ->
    review.prospectiveCheckpointAuthorityRecorded = true ->
    review.rollbackExactRecorded = true ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.releaseToEvidenceReview := by
  intro model optimizer scheduler rng cache backup descendant authority rollback
  simp [FullStateUpdateRouteFor, model, optimizer, scheduler, rng, cache, backup,
    descendant, authority, rollback]

theorem missing_optimizer_state_requires_inventory_repair
    {review : FullStateUpdateReview} :
    review.optimizerStateRecorded = false ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.requireInventoryRepair := by
  intro missing
  simp [FullStateUpdateRouteFor, missing]

theorem missing_scheduler_state_requires_inventory_repair
    {review : FullStateUpdateReview} :
    review.schedulerStateRecorded = false ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.requireInventoryRepair := by
  intro missing
  simp [FullStateUpdateRouteFor, missing]

theorem missing_rng_state_requires_inventory_repair
    {review : FullStateUpdateReview} :
    review.rngStateRecorded = false ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.requireInventoryRepair := by
  intro missing
  simp [FullStateUpdateRouteFor, missing]

theorem missing_cache_state_requires_inventory_repair
    {review : FullStateUpdateReview} :
    review.cacheStateRecorded = false ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.requireInventoryRepair := by
  intro missing
  simp [FullStateUpdateRouteFor, missing]

theorem missing_backup_state_requires_inventory_repair
    {review : FullStateUpdateReview} :
    review.backupStateRecorded = false ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.requireInventoryRepair := by
  intro missing
  simp [FullStateUpdateRouteFor, missing]

theorem missing_descendant_state_requires_inventory_repair
    {review : FullStateUpdateReview} :
    review.descendantStateRecorded = false ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.requireInventoryRepair := by
  intro missing
  simp [FullStateUpdateRouteFor, missing]

theorem missing_prospective_checkpoint_authority_requires_repair
    {review : FullStateUpdateReview} :
    review.modelStateRecorded = true ->
    review.optimizerStateRecorded = true ->
    review.schedulerStateRecorded = true ->
    review.rngStateRecorded = true ->
    review.cacheStateRecorded = true ->
    review.backupStateRecorded = true ->
    review.descendantStateRecorded = true ->
    review.prospectiveCheckpointAuthorityRecorded = false ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.requireCheckpointAuthorityRepair := by
  intro model optimizer scheduler rng cache backup descendant missingAuthority
  simp [FullStateUpdateRouteFor, model, optimizer, scheduler, rng, cache, backup,
    descendant, missingAuthority]

theorem rollback_mismatch_requires_repair
    {review : FullStateUpdateReview} :
    review.modelStateRecorded = true ->
    review.optimizerStateRecorded = true ->
    review.schedulerStateRecorded = true ->
    review.rngStateRecorded = true ->
    review.cacheStateRecorded = true ->
    review.backupStateRecorded = true ->
    review.descendantStateRecorded = true ->
    review.prospectiveCheckpointAuthorityRecorded = true ->
    review.rollbackExactRecorded = false ->
    FullStateUpdateRouteFor review = FullStateUpdateRoute.requireRollbackRepair := by
  intro model optimizer scheduler rng cache backup descendant authority mismatch
  simp [FullStateUpdateRouteFor, model, optimizer, scheduler, rng, cache, backup,
    descendant, authority, mismatch]

inductive UnlearningClaimRoute where
  | boundedBehavioralLineageReport
  | rejectInfluenceLaundering
  | rejectPrivacyLaundering
  | rejectStorageLaundering
deriving DecidableEq, Repr

structure UnlearningClaimReview where
  behavioralChangeObserved : Bool
  lineagePropagationObserved : Bool
  influenceEvidenceRecorded : Bool
  influenceReductionClaimed : Bool
  privacyEvidenceRecorded : Bool
  privacyErasureClaimed : Bool
  storageErasureVerified : Bool
  storageErasureClaimed : Bool
deriving DecidableEq, Repr

def UnlearningClaimRouteFor (review : UnlearningClaimReview) : UnlearningClaimRoute :=
  if review.influenceReductionClaimed = true ∧ review.influenceEvidenceRecorded = false then
    UnlearningClaimRoute.rejectInfluenceLaundering
  else if review.privacyErasureClaimed = true ∧ review.privacyEvidenceRecorded = false then
    UnlearningClaimRoute.rejectPrivacyLaundering
  else if review.storageErasureClaimed = true ∧ review.storageErasureVerified = false then
    UnlearningClaimRoute.rejectStorageLaundering
  else
    UnlearningClaimRoute.boundedBehavioralLineageReport

theorem behavioral_change_cannot_launder_influence_reduction
    {review : UnlearningClaimReview} :
    review.behavioralChangeObserved = true ->
    review.influenceReductionClaimed = true ->
    review.influenceEvidenceRecorded = false ->
    UnlearningClaimRouteFor review = UnlearningClaimRoute.rejectInfluenceLaundering := by
  intro _ claimed missingEvidence
  simp [UnlearningClaimRouteFor, claimed, missingEvidence]

theorem behavioral_change_cannot_launder_privacy_erasure
    {review : UnlearningClaimReview} :
    review.behavioralChangeObserved = true ->
    review.privacyErasureClaimed = true ->
    review.privacyEvidenceRecorded = false ->
    review.influenceReductionClaimed = false ->
    UnlearningClaimRouteFor review = UnlearningClaimRoute.rejectPrivacyLaundering := by
  intro _ claimed missingEvidence noInfluenceClaim
  simp [UnlearningClaimRouteFor, claimed, missingEvidence, noInfluenceClaim]

theorem lineage_propagation_cannot_launder_storage_erasure
    {review : UnlearningClaimReview} :
    review.lineagePropagationObserved = true ->
    review.storageErasureClaimed = true ->
    review.storageErasureVerified = false ->
    review.influenceReductionClaimed = false ->
    review.privacyErasureClaimed = false ->
    UnlearningClaimRouteFor review = UnlearningClaimRoute.rejectStorageLaundering := by
  intro _ claimed notVerified noInfluenceClaim noPrivacyClaim
  simp [UnlearningClaimRouteFor, claimed, notVerified, noInfluenceClaim, noPrivacyClaim]

end AsiStackProofs.DataEngines

namespace AsiStackProofs.GovernedModelTraining

inductive RunRoute where
  | rejectIdentity
  | rejectFrozenInputs
  | rejectTopology
  | rejectNumerics
  | requestStateInventory
  | rejectTornCheckpoint
  | rejectResumeDrift
  | rejectSelectionLeakage
  | requestQualification
  | acceptHandoff
deriving DecidableEq, Repr

structure TrainingRun where
  contractDigest : Nat := 8101
  expectedContractDigest : Nat := 8101
  architectureDigest : Nat := 8102
  expectedArchitectureDigest : Nat := 8102
  dataLeaseDigest : Nat := 8103
  expectedDataLeaseDigest : Nat := 8103
  objectiveDigest : Nat := 8104
  expectedObjectiveDigest : Nat := 8104
  topologyDigest : Nat := 8105
  expectedTopologyDigest : Nat := 8105
  numericPolicyDigest : Nat := 8106
  expectedNumericPolicyDigest : Nat := 8106
  inputsFrozenBeforeRun : Bool := true
  topologyRecorded : Bool := true
  collectivesRecorded : Bool := true
  optimizerSemanticsRecorded : Bool := true
  numericalPolicyRecorded : Bool := true
  failureDenominatorComplete : Bool := true
  requiredStateClasses : Nat := 10
  checkpointedStateClasses : Nat := 10
  checkpointLogicalStepConsistent : Bool := true
  checkpointDurablyCommitted : Bool := true
  resumeDataCursorExact : Bool := true
  resumeRngStateExact : Bool := true
  resumeSchedulerStateExact : Bool := true
  resumeScalerStateExact : Bool := true
  resumeTopologyDispositionRecorded : Bool := true
  validationOnlySelection : Bool := true
  allCandidateCheckpointsRetained : Bool := true
  failedRunsRetained : Bool := true
  qualificationEvaluatorIndependent : Bool := true
  qualificationUnopenedAtSelection : Bool := true
  supportPromotionRequested : Bool := false
  releaseRequested : Bool := false
deriving DecidableEq, Repr

def exactIdentity (r : TrainingRun) : Bool :=
  r.contractDigest == r.expectedContractDigest &&
  r.architectureDigest == r.expectedArchitectureDigest &&
  r.dataLeaseDigest == r.expectedDataLeaseDigest &&
  r.objectiveDigest == r.expectedObjectiveDigest

def exactTopologyAndNumerics (r : TrainingRun) : Bool :=
  r.topologyDigest == r.expectedTopologyDigest &&
  r.numericPolicyDigest == r.expectedNumericPolicyDigest

def completeCheckpoint (r : TrainingRun) : Bool :=
  decide (r.checkpointedStateClasses = r.requiredStateClasses) &&
  r.checkpointLogicalStepConsistent && r.checkpointDurablyCommitted

def resumeAccounted (r : TrainingRun) : Bool :=
  r.resumeDataCursorExact && r.resumeRngStateExact &&
  r.resumeSchedulerStateExact && r.resumeScalerStateExact &&
  r.resumeTopologyDispositionRecorded

def selectionSeparatedFromQualification (r : TrainingRun) : Bool :=
  r.validationOnlySelection && r.allCandidateCheckpointsRetained &&
  r.failedRunsRetained && r.qualificationEvaluatorIndependent &&
  r.qualificationUnopenedAtSelection

def authorityLeakRequested (r : TrainingRun) : Bool :=
  r.supportPromotionRequested || r.releaseRequested

def handoffRoute (r : TrainingRun) : RunRoute :=
  if ! exactIdentity r then .rejectIdentity
  else if ! r.inputsFrozenBeforeRun then .rejectFrozenInputs
  else if ! r.topologyRecorded || ! r.collectivesRecorded ||
          ! r.optimizerSemanticsRecorded then .rejectTopology
  else if ! r.numericalPolicyRecorded || ! exactTopologyAndNumerics r then
    .rejectNumerics
  else if r.checkpointedStateClasses != r.requiredStateClasses then
    .requestStateInventory
  else if ! r.checkpointLogicalStepConsistent ||
          ! r.checkpointDurablyCommitted then .rejectTornCheckpoint
  else if ! resumeAccounted r then .rejectResumeDrift
  else if ! r.validationOnlySelection || ! r.allCandidateCheckpointsRetained ||
          ! r.failedRunsRetained then .rejectSelectionLeakage
  else if ! r.qualificationEvaluatorIndependent ||
          ! r.qualificationUnopenedAtSelection then .requestQualification
  else if ! r.failureDenominatorComplete || authorityLeakRequested r then
    .requestQualification
  else .acceptHandoff

theorem accepted_handoff_requires_exact_identity
    (r : TrainingRun) (h : handoffRoute r = .acceptHandoff) :
    exactIdentity r = true := by
  cases hId : exactIdentity r <;> simp_all [handoffRoute]

theorem accepted_handoff_requires_complete_checkpoint
    (r : TrainingRun) (h : handoffRoute r = .acceptHandoff) :
    completeCheckpoint r = true := by
  unfold handoffRoute at h
  repeat' first | split at h | simp_all [completeCheckpoint]

theorem accepted_handoff_requires_resume_accounting
    (r : TrainingRun) (h : handoffRoute r = .acceptHandoff) :
    resumeAccounted r = true := by
  unfold handoffRoute at h
  repeat' first | split at h | simp_all

theorem accepted_handoff_separates_selection_and_qualification
    (r : TrainingRun) (h : handoffRoute r = .acceptHandoff) :
    selectionSeparatedFromQualification r = true := by
  unfold handoffRoute at h
  repeat' first | split at h | simp_all [selectionSeparatedFromQualification]

theorem missing_state_class_requests_inventory :
    handoffRoute { ({} : TrainingRun) with checkpointedStateClasses := 9 } =
      .requestStateInventory := by native_decide

theorem torn_checkpoint_rejects_handoff :
    handoffRoute { ({} : TrainingRun) with checkpointLogicalStepConsistent := false } =
      .rejectTornCheckpoint := by native_decide

theorem undurable_async_checkpoint_rejects_handoff :
    handoffRoute { ({} : TrainingRun) with checkpointDurablyCommitted := false } =
      .rejectTornCheckpoint := by native_decide

theorem data_cursor_drift_rejects_resume :
    handoffRoute { ({} : TrainingRun) with resumeDataCursorExact := false } =
      .rejectResumeDrift := by native_decide

theorem rng_drift_rejects_resume :
    handoffRoute { ({} : TrainingRun) with resumeRngStateExact := false } =
      .rejectResumeDrift := by native_decide

theorem hidden_failed_run_rejects_selection :
    handoffRoute { ({} : TrainingRun) with failedRunsRetained := false } =
      .rejectSelectionLeakage := by native_decide

theorem opened_qualification_requests_new_qualification :
    handoffRoute { ({} : TrainingRun) with qualificationUnopenedAtSelection := false } =
      .requestQualification := by native_decide

theorem support_laundering_requests_qualification :
    handoffRoute { ({} : TrainingRun) with supportPromotionRequested := true } =
      .requestQualification := by native_decide

theorem complete_authored_run_accepts_bounded_handoff_without_authority :
    handoffRoute ({} : TrainingRun) = .acceptHandoff ∧
    authorityLeakRequested ({} : TrainingRun) = false := by native_decide

end AsiStackProofs.GovernedModelTraining

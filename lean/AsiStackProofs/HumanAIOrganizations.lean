namespace AsiStackProofs.HumanAIOrganizations

inductive AccountabilityReviewState where
  | proposed
  | capacityReview
  | authorityReview
  | independenceReview
  | remedyReview
  | refusedNoAssignment
  | repairDecisionIdentity
  | repairActorIdentity
  | repairInformation
  | repairCompetence
  | repairTime
  | repairWorkload
  | repairDecisionAuthority
  | repairInterventionAuthority
  | repairPracticalControl
  | repairRevocation
  | repairIndependentReview
  | repairSeparationOfDuties
  | repairConflictDisposition
  | repairStopPath
  | repairAppealPath
  | repairRemedyPath
  | repairEvidenceAccess
  | repairResidualCustody
  | repairNonClaimBoundary
  | accountabilityAssignable
deriving DecidableEq, Repr

structure AccountabilityAssignment where
  assignmentRequested : Bool := true
  decisionIdentityPresent : Bool := true
  accountableActorPresent : Bool := true
  informationAvailable : Bool := true
  competenceCurrent : Bool := true
  timeAvailable : Bool := true
  workloadWithinLimit : Bool := true
  decisionAuthorityPresent : Bool := true
  interventionAuthorityPresent : Bool := true
  practicalAbilityToChange : Bool := true
  revocationPathPresent : Bool := true
  independentReviewPresent : Bool := true
  separationOfDutiesPresent : Bool := true
  conflictDispositionPresent : Bool := true
  stopPathPresent : Bool := true
  appealPathPresent : Bool := true
  remedyPathPresent : Bool := true
  evidenceAccessPresent : Bool := true
  residualCustodyPresent : Bool := true
  nonClaimBoundaryPresent : Bool := true
deriving DecidableEq, Repr

def AccountabilityAssignmentComplete (record : AccountabilityAssignment) : Bool :=
  record.assignmentRequested && record.decisionIdentityPresent &&
    record.accountableActorPresent && record.informationAvailable &&
      record.competenceCurrent && record.timeAvailable &&
        record.workloadWithinLimit && record.decisionAuthorityPresent &&
          record.interventionAuthorityPresent && record.practicalAbilityToChange &&
            record.revocationPathPresent && record.independentReviewPresent &&
              record.separationOfDutiesPresent && record.conflictDispositionPresent &&
                record.stopPathPresent && record.appealPathPresent &&
                  record.remedyPathPresent && record.evidenceAccessPresent &&
                    record.residualCustodyPresent && record.nonClaimBoundaryPresent

def AccountabilityReviewStepFor
    (record : AccountabilityAssignment) :
    AccountabilityReviewState -> AccountabilityReviewState
  | .proposed =>
      if ! record.assignmentRequested then .refusedNoAssignment
      else if ! record.decisionIdentityPresent then .repairDecisionIdentity
      else if ! record.accountableActorPresent then .repairActorIdentity
      else .capacityReview
  | .capacityReview =>
      if ! record.informationAvailable then .repairInformation
      else if ! record.competenceCurrent then .repairCompetence
      else if ! record.timeAvailable then .repairTime
      else if ! record.workloadWithinLimit then .repairWorkload
      else .authorityReview
  | .authorityReview =>
      if ! record.decisionAuthorityPresent then .repairDecisionAuthority
      else if ! record.interventionAuthorityPresent then .repairInterventionAuthority
      else if ! record.practicalAbilityToChange then .repairPracticalControl
      else if ! record.revocationPathPresent then .repairRevocation
      else .independenceReview
  | .independenceReview =>
      if ! record.independentReviewPresent then .repairIndependentReview
      else if ! record.separationOfDutiesPresent then .repairSeparationOfDuties
      else if ! record.conflictDispositionPresent then .repairConflictDisposition
      else .remedyReview
  | .remedyReview =>
      if ! record.stopPathPresent then .repairStopPath
      else if ! record.appealPathPresent then .repairAppealPath
      else if ! record.remedyPathPresent then .repairRemedyPath
      else if ! record.evidenceAccessPresent then .repairEvidenceAccess
      else if ! record.residualCustodyPresent then .repairResidualCustody
      else if ! record.nonClaimBoundaryPresent then .repairNonClaimBoundary
      else .accountabilityAssignable
  | state => state

def AccountabilityReviewRun
    (record : AccountabilityAssignment) : Nat -> AccountabilityReviewState
  | 0 => .proposed
  | steps + 1 => AccountabilityReviewStepFor record (AccountabilityReviewRun record steps)

def AccountabilityStageInvariant
    (record : AccountabilityAssignment) : AccountabilityReviewState -> Prop
  | .proposed => True
  | .capacityReview =>
      record.assignmentRequested = true ∧
      record.decisionIdentityPresent = true ∧
      record.accountableActorPresent = true
  | .authorityReview =>
      record.assignmentRequested = true ∧
      record.decisionIdentityPresent = true ∧
      record.accountableActorPresent = true ∧
      record.informationAvailable = true ∧
      record.competenceCurrent = true ∧
      record.timeAvailable = true ∧
      record.workloadWithinLimit = true
  | .independenceReview =>
      record.assignmentRequested = true ∧
      record.decisionIdentityPresent = true ∧
      record.accountableActorPresent = true ∧
      record.informationAvailable = true ∧
      record.competenceCurrent = true ∧
      record.timeAvailable = true ∧
      record.workloadWithinLimit = true ∧
      record.decisionAuthorityPresent = true ∧
      record.interventionAuthorityPresent = true ∧
      record.practicalAbilityToChange = true ∧
      record.revocationPathPresent = true
  | .remedyReview =>
      record.assignmentRequested = true ∧
      record.decisionIdentityPresent = true ∧
      record.accountableActorPresent = true ∧
      record.informationAvailable = true ∧
      record.competenceCurrent = true ∧
      record.timeAvailable = true ∧
      record.workloadWithinLimit = true ∧
      record.decisionAuthorityPresent = true ∧
      record.interventionAuthorityPresent = true ∧
      record.practicalAbilityToChange = true ∧
      record.revocationPathPresent = true ∧
      record.independentReviewPresent = true ∧
      record.separationOfDutiesPresent = true ∧
      record.conflictDispositionPresent = true
  | .accountabilityAssignable => AccountabilityAssignmentComplete record = true
  | _ => True

theorem accountability_review_step_preserves_stage_invariant
    (record : AccountabilityAssignment)
    (state : AccountabilityReviewState)
    (invariant : AccountabilityStageInvariant record state) :
    AccountabilityStageInvariant record (AccountabilityReviewStepFor record state) := by
  cases state <;> simp only [AccountabilityReviewStepFor]
  all_goals
    repeat' split
  all_goals
    simp_all [AccountabilityStageInvariant, AccountabilityAssignmentComplete]

theorem accountability_review_run_preserves_stage_invariant
    (record : AccountabilityAssignment) (steps : Nat) :
    AccountabilityStageInvariant record (AccountabilityReviewRun record steps) := by
  induction steps with
  | zero => simp [AccountabilityReviewRun, AccountabilityStageInvariant]
  | succ steps ih =>
      simpa [AccountabilityReviewRun] using
        accountability_review_step_preserves_stage_invariant record
          (AccountabilityReviewRun record steps) ih

theorem assignable_accountability_requires_complete_authority_record
    (record : AccountabilityAssignment) (steps : Nat)
    (assignable :
      AccountabilityReviewRun record steps = .accountabilityAssignable) :
    AccountabilityAssignmentComplete record = true := by
  have invariant := accountability_review_run_preserves_stage_invariant record steps
  simpa [assignable, AccountabilityStageInvariant] using invariant

theorem complete_accountability_record_reaches_assignment :
    AccountabilityReviewRun ({} : AccountabilityAssignment) 5 =
      .accountabilityAssignable := by decide

theorem missing_information_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with informationAvailable := false } 2 =
        .repairInformation := by decide

theorem missing_competence_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with competenceCurrent := false } 2 =
        .repairCompetence := by decide

theorem missing_time_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with timeAvailable := false } 2 =
        .repairTime := by decide

theorem excessive_workload_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with workloadWithinLimit := false } 2 =
        .repairWorkload := by decide

theorem missing_decision_authority_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with decisionAuthorityPresent := false } 3 =
        .repairDecisionAuthority := by decide

theorem missing_intervention_authority_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with interventionAuthorityPresent := false } 3 =
        .repairInterventionAuthority := by decide

theorem missing_practical_control_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with practicalAbilityToChange := false } 3 =
        .repairPracticalControl := by decide

theorem missing_revocation_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with revocationPathPresent := false } 3 =
        .repairRevocation := by decide

theorem missing_independent_review_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with independentReviewPresent := false } 4 =
        .repairIndependentReview := by decide

theorem collapsed_separation_of_duties_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with separationOfDutiesPresent := false } 4 =
        .repairSeparationOfDuties := by decide

theorem undisposed_conflict_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with conflictDispositionPresent := false } 4 =
        .repairConflictDisposition := by decide

theorem missing_stop_path_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with stopPathPresent := false } 5 =
        .repairStopPath := by decide

theorem missing_appeal_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with appealPathPresent := false } 5 =
        .repairAppealPath := by decide

theorem missing_remedy_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with remedyPathPresent := false } 5 =
        .repairRemedyPath := by decide

theorem missing_evidence_access_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with evidenceAccessPresent := false } 5 =
        .repairEvidenceAccess := by decide

theorem orphaned_residuals_block_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with residualCustodyPresent := false } 5 =
        .repairResidualCustody := by decide

theorem missing_non_claim_boundary_blocks_accountability_assignment :
    AccountabilityReviewRun
      { ({} : AccountabilityAssignment) with nonClaimBoundaryPresent := false } 5 =
        .repairNonClaimBoundary := by decide

end AsiStackProofs.HumanAIOrganizations

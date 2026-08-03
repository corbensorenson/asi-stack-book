import AsiStackProofs.Authority

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

inductive ExerciseStage where
  | proposed | delegated | active | escalated | handedOff | contested
  | authorityExpired | reconstructed | remedied | closed
deriving DecidableEq, Repr

inductive ExerciseEventKind where
  | bindDelegation | activateWork | recordEscalation | handOff
  | recordContest | expireAuthority | reconstructIncident | recordRemedy | close
deriving DecidableEq, Repr

inductive ExerciseRoute where
  | rejectWrongStage | rejectIdentitySubstitution | rejectEventReplay
  | rejectAuthorityLeak | requestCompleteAssignment | requestDelegationTerms
  | blockAuthorityCeiling | requestExpiry | requestActivationAcknowledgment
  | requestEffectObserver | requestEscalationReason | requestStopApplied
  | requestIndependentReview | requestHandoffAcknowledgment
  | requestStateTransfer | requestResidualTransfer | requestContestStanding
  | requestEvidenceAccess | requestAppealRecord | requestAuthorityExpiry
  | requestRevocationPropagation | requestIncidentTimeline | requestEffectLedger
  | requestCausalUncertainty | requestRemedyApplied | requestRemedyObserved
  | requestRemainingResiduals | requestNonClaims | requestDescendants
  | requestCleanup | acceptDelegation | acceptActivation | acceptEscalation
  | acceptHandoff | acceptContest | acceptExpiry | acceptReconstruction
  | acceptRemedy | acceptClosure
deriving DecidableEq, Repr

structure ExerciseState where
  stage : ExerciseStage
  decisionDigest : Nat
  delegatorDigest : Nat
  delegateDigest : Nat
  policyDigest : Nat
  authorityDigest : Nat
  reviewerDigest : Nat
  evidenceDigest : Nat
  remedyDigest : Nat
  resultDigest : Nat
  lastEventDigest : Nat
  authorityCeiling : Nat := 3
  activeAuthority : Nat := 0
  receiptCount : Nat := 0
  contestReceiptCount : Nat := 0
  remedyReceiptCount : Nat := 0
  supportAssigned : Bool := false
  externalEffectCommitted : Bool := false
deriving DecidableEq, Repr

structure ExercisePacket where
  decisionDigest : Nat := 8001
  delegatorDigest : Nat := 8002
  delegateDigest : Nat := 8003
  policyDigest : Nat := 8004
  authorityDigest : Nat := 8005
  reviewerDigest : Nat := 8006
  evidenceDigest : Nat := 8007
  remedyDigest : Nat := 8008
  resultDigest : Nat := 8009
  eventDigest : Nat := 1
  assignment : AccountabilityAssignment := {}
  delegationTerms : Bool := true
  requestedAuthority : Nat := 2
  expiryPresent : Bool := true
  activationAcknowledgment : Bool := true
  effectObserver : Bool := true
  escalationReason : Bool := true
  stopApplied : Bool := true
  independentReview : Bool := true
  handoffAcknowledgment : Bool := true
  stateTransfer : Bool := true
  residualTransfer : Bool := true
  contestStanding : Bool := true
  evidenceAccess : Bool := true
  appealRecord : Bool := true
  authorityExpiry : Bool := true
  revocationPropagation : Bool := true
  incidentTimeline : Bool := true
  effectLedger : Bool := true
  causalUncertainty : Bool := true
  remedyApplied : Bool := true
  remedyObserved : Bool := true
  remainingResiduals : Bool := true
  nonClaims : Bool := true
  descendants : Bool := true
  cleanup : Bool := true
  supportRequested : Bool := false
  externalEffectRequested : Bool := false
deriving DecidableEq, Repr

structure ExerciseIdentity where
  decisionDigest : Nat
  delegatorDigest : Nat
  delegateDigest : Nat
  policyDigest : Nat
  authorityDigest : Nat
  reviewerDigest : Nat
  evidenceDigest : Nat
  remedyDigest : Nat
  resultDigest : Nat
deriving DecidableEq, Repr

def exerciseIdentity (state : ExerciseState) : ExerciseIdentity :=
  { decisionDigest := state.decisionDigest
    delegatorDigest := state.delegatorDigest
    delegateDigest := state.delegateDigest
    policyDigest := state.policyDigest
    authorityDigest := state.authorityDigest
    reviewerDigest := state.reviewerDigest
    evidenceDigest := state.evidenceDigest
    remedyDigest := state.remedyDigest
    resultDigest := state.resultDigest }

def expectedExerciseKind : ExerciseStage -> ExerciseEventKind
  | .proposed => .bindDelegation
  | .delegated => .activateWork
  | .active => .recordEscalation
  | .escalated => .handOff
  | .handedOff => .recordContest
  | .contested => .expireAuthority
  | .authorityExpired => .reconstructIncident
  | .reconstructed => .recordRemedy
  | .remedied => .close
  | .closed => .close

def exerciseAccepted : ExerciseRoute -> Bool
  | .acceptDelegation | .acceptActivation | .acceptEscalation
  | .acceptHandoff | .acceptContest | .acceptExpiry
  | .acceptReconstruction | .acceptRemedy | .acceptClosure => true
  | _ => false

def exerciseRoute (state : ExerciseState) (kind : ExerciseEventKind)
    (packet : ExercisePacket) : ExerciseRoute :=
  if kind != expectedExerciseKind state.stage then .rejectWrongStage
  else if packet.decisionDigest != state.decisionDigest ||
      packet.delegatorDigest != state.delegatorDigest ||
      packet.delegateDigest != state.delegateDigest ||
      packet.policyDigest != state.policyDigest ||
      packet.authorityDigest != state.authorityDigest ||
      packet.reviewerDigest != state.reviewerDigest ||
      packet.evidenceDigest != state.evidenceDigest ||
      packet.remedyDigest != state.remedyDigest ||
      packet.resultDigest != state.resultDigest then .rejectIdentitySubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectEventReplay
  else if packet.supportRequested || packet.externalEffectRequested then
    .rejectAuthorityLeak
  else match state.stage with
  | .proposed =>
      if !AccountabilityAssignmentComplete packet.assignment then
        .requestCompleteAssignment
      else if !packet.delegationTerms then .requestDelegationTerms
      else if state.authorityCeiling < packet.requestedAuthority then
        .blockAuthorityCeiling
      else if !packet.expiryPresent then .requestExpiry
      else .acceptDelegation
  | .delegated =>
      if !packet.activationAcknowledgment then .requestActivationAcknowledgment
      else if !packet.effectObserver then .requestEffectObserver
      else .acceptActivation
  | .active =>
      if !packet.escalationReason then .requestEscalationReason
      else if !packet.stopApplied then .requestStopApplied
      else if !packet.independentReview then .requestIndependentReview
      else .acceptEscalation
  | .escalated =>
      if !packet.handoffAcknowledgment then .requestHandoffAcknowledgment
      else if !packet.stateTransfer then .requestStateTransfer
      else if !packet.residualTransfer then .requestResidualTransfer
      else .acceptHandoff
  | .handedOff =>
      if !packet.contestStanding then .requestContestStanding
      else if !packet.evidenceAccess then .requestEvidenceAccess
      else if !packet.appealRecord then .requestAppealRecord
      else .acceptContest
  | .contested =>
      if !packet.authorityExpiry then .requestAuthorityExpiry
      else if !packet.revocationPropagation then .requestRevocationPropagation
      else .acceptExpiry
  | .authorityExpired =>
      if !packet.incidentTimeline then .requestIncidentTimeline
      else if !packet.effectLedger then .requestEffectLedger
      else if !packet.causalUncertainty then .requestCausalUncertainty
      else .acceptReconstruction
  | .reconstructed =>
      if !packet.remedyApplied then .requestRemedyApplied
      else if !packet.remedyObserved then .requestRemedyObserved
      else if !packet.remainingResiduals then .requestRemainingResiduals
      else .acceptRemedy
  | .remedied =>
      if !packet.nonClaims then .requestNonClaims
      else if !packet.descendants then .requestDescendants
      else if !packet.cleanup then .requestCleanup
      else .acceptClosure
  | .closed => .rejectWrongStage

def advanceExerciseStage : ExerciseStage -> ExerciseStage
  | .proposed => .delegated
  | .delegated => .active
  | .active => .escalated
  | .escalated => .handedOff
  | .handedOff => .contested
  | .contested => .authorityExpired
  | .authorityExpired => .reconstructed
  | .reconstructed => .remedied
  | .remedied => .closed
  | .closed => .closed

def applyExerciseEvent (state : ExerciseState) (kind : ExerciseEventKind)
    (packet : ExercisePacket) : ExerciseState × ExerciseRoute :=
  let selectedRoute := exerciseRoute state kind packet
  if exerciseAccepted selectedRoute then
    ({state with
      stage := advanceExerciseStage state.stage
      lastEventDigest := packet.eventDigest
      activeAuthority := if selectedRoute == .acceptDelegation then
          packet.requestedAuthority
        else if selectedRoute == .acceptExpiry then 0
        else state.activeAuthority
      receiptCount := state.receiptCount + 1
      contestReceiptCount := if selectedRoute == .acceptContest then
        state.contestReceiptCount + 1 else state.contestReceiptCount
      remedyReceiptCount := if selectedRoute == .acceptRemedy then
        state.remedyReceiptCount + 1 else state.remedyReceiptCount}, selectedRoute)
  else (state, selectedRoute)

structure ExerciseEvent where
  kind : ExerciseEventKind
  packet : ExercisePacket
deriving DecidableEq, Repr

def ExerciseStep (state : ExerciseState) (event : ExerciseEvent) :
    Option ExerciseState :=
  if state.stage = .closed then none
  else if exerciseAccepted (exerciseRoute state event.kind event.packet) then
    some (applyExerciseEvent state event.kind event.packet).1
  else none

def ExerciseRun : ExerciseState -> List ExerciseEvent -> Option ExerciseState
  | state, [] => some state
  | state, event :: tail =>
      match ExerciseStep state event with
      | none => none
      | some next => ExerciseRun next tail

def ExerciseTraceAccepted : ExerciseState -> List ExerciseEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      exerciseAccepted (exerciseRoute state event.kind event.packet) = true ∧
      ExerciseTraceAccepted
        (applyExerciseEvent state event.kind event.packet).1 tail

theorem accepted_exercise_step_is_accepted
    {state next : ExerciseState} {event : ExerciseEvent}
    (stepped : ExerciseStep state event = some next) :
    exerciseAccepted (exerciseRoute state event.kind event.packet) = true := by
  unfold ExerciseStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · assumption
    · simp at stepped

theorem accepted_exercise_step_applies_event
    {state next : ExerciseState} {event : ExerciseEvent}
    (stepped : ExerciseStep state event = some next) :
    next = (applyExerciseEvent state event.kind event.packet).1 := by
  unfold ExerciseStep at stepped
  split at stepped
  · simp at stepped
  · split at stepped
    · exact Option.some.inj stepped |>.symm
    · simp at stepped

theorem apply_exercise_event_preserves_identity (state : ExerciseState)
    (event : ExerciseEvent) :
    exerciseIdentity
      (applyExerciseEvent state event.kind event.packet).1 =
      exerciseIdentity state := by
  by_cases acceptedRoute :
      exerciseAccepted (exerciseRoute state event.kind event.packet) = true <;>
    simp [applyExerciseEvent, acceptedRoute, exerciseIdentity]

theorem rejected_exercise_event_preserves_state (state : ExerciseState)
    (event : ExerciseEvent)
    (rejected :
      exerciseAccepted (exerciseRoute state event.kind event.packet) = false) :
    (applyExerciseEvent state event.kind event.packet).1 = state := by
  simp [applyExerciseEvent, rejected]

theorem accepted_exercise_step_preserves_identity
    {state next : ExerciseState} {event : ExerciseEvent}
    (stepped : ExerciseStep state event = some next) :
    exerciseIdentity next = exerciseIdentity state := by
  rw [accepted_exercise_step_applies_event stepped]
  exact apply_exercise_event_preserves_identity state event

theorem accepted_exercise_step_preserves_non_authority
    {state next : ExerciseState} {event : ExerciseEvent}
    (stepped : ExerciseStep state event = some next) :
    next.supportAssigned = state.supportAssigned ∧
    next.externalEffectCommitted = state.externalEffectCommitted := by
  rw [accepted_exercise_step_applies_event stepped]
  simp [applyExerciseEvent, accepted_exercise_step_is_accepted stepped]

theorem accepted_exercise_step_adds_exactly_one_receipt
    {state next : ExerciseState} {event : ExerciseEvent}
    (stepped : ExerciseStep state event = some next) :
    next.receiptCount = state.receiptCount + 1 := by
  rw [accepted_exercise_step_applies_event stepped]
  simp [applyExerciseEvent, accepted_exercise_step_is_accepted stepped]

theorem accepted_exercise_step_advances_stage
    {state next : ExerciseState} {event : ExerciseEvent}
    (stepped : ExerciseStep state event = some next) :
    next.stage = advanceExerciseStage state.stage := by
  rw [accepted_exercise_step_applies_event stepped]
  simp [applyExerciseEvent, accepted_exercise_step_is_accepted stepped]

theorem apply_exercise_event_contest_count_monotone (state : ExerciseState)
    (event : ExerciseEvent) :
    state.contestReceiptCount <=
      (applyExerciseEvent state event.kind event.packet).1.contestReceiptCount := by
  cases routed : exerciseRoute state event.kind event.packet <;>
    simp [applyExerciseEvent, routed, exerciseAccepted]

theorem apply_exercise_event_remedy_count_monotone (state : ExerciseState)
    (event : ExerciseEvent) :
    state.remedyReceiptCount <=
      (applyExerciseEvent state event.kind event.packet).1.remedyReceiptCount := by
  cases routed : exerciseRoute state event.kind event.packet <;>
    simp [applyExerciseEvent, routed, exerciseAccepted]

theorem accepted_exercise_run_preserves_identity
    {state final : ExerciseState} {events : List ExerciseEvent}
    (ran : ExerciseRun state events = some final) :
    exerciseIdentity final = exerciseIdentity state := by
  induction events generalizing state with
  | nil => simp [ExerciseRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ExerciseStep state event with
      | none => simp [ExerciseRun, stepped] at ran
      | some next =>
          have tailRan : ExerciseRun next tail = some final := by
            simpa [ExerciseRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_exercise_step_preserves_identity stepped)

theorem accepted_exercise_run_preserves_support
    {state final : ExerciseState} {events : List ExerciseEvent}
    (ran : ExerciseRun state events = some final) :
    final.supportAssigned = state.supportAssigned := by
  induction events generalizing state with
  | nil => simp [ExerciseRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ExerciseStep state event with
      | none => simp [ExerciseRun, stepped] at ran
      | some next =>
          have tailRan : ExerciseRun next tail = some final := by
            simpa [ExerciseRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_exercise_step_preserves_non_authority stepped).1

theorem accepted_exercise_run_preserves_external_effect
    {state final : ExerciseState} {events : List ExerciseEvent}
    (ran : ExerciseRun state events = some final) :
    final.externalEffectCommitted = state.externalEffectCommitted := by
  induction events generalizing state with
  | nil => simp [ExerciseRun] at ran; subst final; rfl
  | cons event tail ih =>
      cases stepped : ExerciseStep state event with
      | none => simp [ExerciseRun, stepped] at ran
      | some next =>
          have tailRan : ExerciseRun next tail = some final := by
            simpa [ExerciseRun, stepped] using ran
          exact (ih tailRan).trans
            (accepted_exercise_step_preserves_non_authority stepped).2

theorem accepted_exercise_run_accounts_exact_receipts
    {state final : ExerciseState} {events : List ExerciseEvent}
    (ran : ExerciseRun state events = some final) :
    final.receiptCount = state.receiptCount + events.length := by
  induction events generalizing state with
  | nil => simp [ExerciseRun] at ran; subst final; simp
  | cons event tail ih =>
      cases stepped : ExerciseStep state event with
      | none => simp [ExerciseRun, stepped] at ran
      | some next =>
          have tailRan : ExerciseRun next tail = some final := by
            simpa [ExerciseRun, stepped] using ran
          calc
            final.receiptCount = next.receiptCount + tail.length := ih tailRan
            _ = (state.receiptCount + 1) + tail.length := by
              rw [accepted_exercise_step_adds_exactly_one_receipt stepped]
            _ = state.receiptCount + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem accepted_exercise_run_contest_count_monotone
    {state final : ExerciseState} {events : List ExerciseEvent}
    (ran : ExerciseRun state events = some final) :
    state.contestReceiptCount <= final.contestReceiptCount := by
  induction events generalizing state with
  | nil => simp [ExerciseRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : ExerciseStep state event with
      | none => simp [ExerciseRun, stepped] at ran
      | some next =>
          have tailRan : ExerciseRun next tail = some final := by
            simpa [ExerciseRun, stepped] using ran
          have stepMonotone : state.contestReceiptCount <=
              next.contestReceiptCount := by
            rw [accepted_exercise_step_applies_event stepped]
            exact apply_exercise_event_contest_count_monotone state event
          exact Nat.le_trans stepMonotone (ih tailRan)

theorem accepted_exercise_run_remedy_count_monotone
    {state final : ExerciseState} {events : List ExerciseEvent}
    (ran : ExerciseRun state events = some final) :
    state.remedyReceiptCount <= final.remedyReceiptCount := by
  induction events generalizing state with
  | nil => simp [ExerciseRun] at ran; subst final; exact Nat.le_refl _
  | cons event tail ih =>
      cases stepped : ExerciseStep state event with
      | none => simp [ExerciseRun, stepped] at ran
      | some next =>
          have tailRan : ExerciseRun next tail = some final := by
            simpa [ExerciseRun, stepped] using ran
          have stepMonotone : state.remedyReceiptCount <=
              next.remedyReceiptCount := by
            rw [accepted_exercise_step_applies_event stepped]
            exact apply_exercise_event_remedy_count_monotone state event
          exact Nat.le_trans stepMonotone (ih tailRan)

theorem accepted_exercise_run_has_accepted_trace
    {state final : ExerciseState} {events : List ExerciseEvent}
    (ran : ExerciseRun state events = some final) :
    ExerciseTraceAccepted state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : ExerciseStep state event with
      | none => simp [ExerciseRun, stepped] at ran
      | some next =>
          have tailRan : ExerciseRun next tail = some final := by
            simpa [ExerciseRun, stepped] using ran
          exact ⟨accepted_exercise_step_is_accepted stepped, by
            rw [← accepted_exercise_step_applies_event stepped]
            exact ih tailRan⟩

theorem exercise_run_append (state : ExerciseState)
    (first second : List ExerciseEvent) :
    ExerciseRun state (first ++ second) =
      (ExerciseRun state first).bind fun intermediate =>
        ExerciseRun intermediate second := by
  induction first generalizing state with
  | nil => simp [ExerciseRun]
  | cons event tail ih =>
      simp only [List.cons_append, ExerciseRun]
      cases ExerciseStep state event <;> simp [ih]

theorem closed_exercise_state_accepts_no_event
    (state : ExerciseState) (event : ExerciseEvent)
    (closed : state.stage = .closed) :
    ExerciseStep state event = none := by
  simp [ExerciseStep, closed]

def initialExerciseState : ExerciseState :=
  { stage := .proposed
    decisionDigest := 8001
    delegatorDigest := 8002
    delegateDigest := 8003
    policyDigest := 8004
    authorityDigest := 8005
    reviewerDigest := 8006
    evidenceDigest := 8007
    remedyDigest := 8008
    resultDigest := 8009
    lastEventDigest := 0 }

def exerciseEventAt (kind : ExerciseEventKind) (digest : Nat) : ExerciseEvent :=
  { kind := kind, packet := { eventDigest := digest } }

def completeExerciseEvents : List ExerciseEvent :=
  [ exerciseEventAt .bindDelegation 1
  , exerciseEventAt .activateWork 2
  , exerciseEventAt .recordEscalation 3
  , exerciseEventAt .handOff 4
  , exerciseEventAt .recordContest 5
  , exerciseEventAt .expireAuthority 6
  , exerciseEventAt .reconstructIncident 7
  , exerciseEventAt .recordRemedy 8
  , exerciseEventAt .close 9 ]

def completeExerciseFinal : ExerciseState :=
  { initialExerciseState with
    stage := .closed
    lastEventDigest := 9
    activeAuthority := 0
    receiptCount := 9
    contestReceiptCount := 1
    remedyReceiptCount := 1 }

theorem over_ceiling_delegation_cannot_start :
    ExerciseStep initialExerciseState
      { kind := .bindDelegation
        packet := { requestedAuthority := 4, eventDigest := 1 } } = none := by
  decide

theorem authored_exercise_witness_reaches_terminal_record :
    ExerciseRun initialExerciseState completeExerciseEvents =
      some completeExerciseFinal := by
  decide

/-!
Organizational responsibility refinement over the authority-delegation chain.
This finite bridge proves that an accepted authored handoff cannot erase the
current accountable owner, widen authority, collapse the named reviewer into
the delegator or delegate, orphan prior responsibility, or create support or
external-effect authority. It does not establish that any identity, assignment,
review, evidence, intervention, appeal, or remedy is authentic or usable.
-/

structure ResponsibilityDelegationState where
  authorityState : Authority.DelegationState
  accountableOwnerId : Nat
  reviewerId : Nat
  evidenceCustodianId : Nat
  residualOwnerIds : List Nat
  responsibilityReceiptCount : Nat
  assignmentComplete : Bool
  interventionPathPresent : Bool
  appealPathPresent : Bool
  remedyPathPresent : Bool
  supportAssigned : Bool
  externalEffectCommitted : Bool
deriving DecidableEq, Repr

structure ResponsibilityDelegationEvent where
  authorityEvent : Authority.DelegationEvent
  transferringOwnerId : Nat
  nextAccountableOwnerId : Nat
  reviewerId : Nat
  evidenceCustodianId : Nat
  assignment : AccountabilityAssignment := {}
  handoffAcknowledgment : Bool := true
  interventionPathTransferred : Bool := true
  evidenceCustodyTransferred : Bool := true
  appealPathTransferred : Bool := true
  remedyPathTransferred : Bool := true
  residualCustodyAcknowledged : Bool := true
  supportRequested : Bool := false
  externalEffectRequested : Bool := false
deriving DecidableEq, Repr

def ValidResponsibilityDelegationEvent
    (state : ResponsibilityDelegationState)
    (event : ResponsibilityDelegationEvent) : Prop :=
  state.accountableOwnerId = state.authorityState.currentDelegateId ∧
    event.transferringOwnerId = state.accountableOwnerId ∧
    Authority.ValidDelegationEvent state.authorityState event.authorityEvent ∧
    event.nextAccountableOwnerId = event.authorityEvent.childDelegateId ∧
    0 < event.nextAccountableOwnerId ∧
    0 < event.reviewerId ∧
    event.reviewerId ≠ event.authorityEvent.actingPrincipalId ∧
    event.reviewerId ≠ event.nextAccountableOwnerId ∧
    0 < event.evidenceCustodianId ∧
    event.evidenceCustodianId ≠ event.nextAccountableOwnerId ∧
    AccountabilityAssignmentComplete event.assignment = true ∧
    event.handoffAcknowledgment = true ∧
    event.interventionPathTransferred = true ∧
    event.evidenceCustodyTransferred = true ∧
    event.appealPathTransferred = true ∧
    event.remedyPathTransferred = true ∧
    event.residualCustodyAcknowledged = true ∧
    event.supportRequested = false ∧
    event.externalEffectRequested = false

instance responsibilityDelegationEventValidityDecidable
    (state : ResponsibilityDelegationState)
    (event : ResponsibilityDelegationEvent) :
    Decidable (ValidResponsibilityDelegationEvent state event) := by
  unfold ValidResponsibilityDelegationEvent
  infer_instance

def ApplyResponsibilityDelegationEvent
    (state : ResponsibilityDelegationState)
    (event : ResponsibilityDelegationEvent) : ResponsibilityDelegationState :=
  { state with
      authorityState :=
        Authority.ApplyDelegationEvent state.authorityState event.authorityEvent
      accountableOwnerId := event.nextAccountableOwnerId
      reviewerId := event.reviewerId
      evidenceCustodianId := event.evidenceCustodianId
      residualOwnerIds := state.accountableOwnerId :: state.residualOwnerIds
      responsibilityReceiptCount := state.responsibilityReceiptCount + 1
      assignmentComplete := true
      interventionPathPresent := true
      appealPathPresent := true
      remedyPathPresent := true }

def ResponsibilityDelegationStep
    (state : ResponsibilityDelegationState)
    (event : ResponsibilityDelegationEvent) :
    Option ResponsibilityDelegationState :=
  if ValidResponsibilityDelegationEvent state event then
    some (ApplyResponsibilityDelegationEvent state event)
  else
    none

def ResponsibilityDelegationRun :
    ResponsibilityDelegationState -> List ResponsibilityDelegationEvent ->
      Option ResponsibilityDelegationState
  | state, [] => some state
  | state, event :: tail =>
      match ResponsibilityDelegationStep state event with
      | none => none
      | some next => ResponsibilityDelegationRun next tail

def ResponsibilityDelegationTraceValid :
    ResponsibilityDelegationState -> List ResponsibilityDelegationEvent -> Prop
  | _, [] => True
  | state, event :: tail =>
      ValidResponsibilityDelegationEvent state event ∧
        ResponsibilityDelegationTraceValid
          (ApplyResponsibilityDelegationEvent state event) tail

def ResponsibilityDelegationNonAuthority
    (state : ResponsibilityDelegationState) : Prop :=
  state.supportAssigned = false ∧
    state.externalEffectCommitted = false ∧
    Authority.DelegationNonAuthority state.authorityState

instance responsibilityDelegationNonAuthorityDecidable
    (state : ResponsibilityDelegationState) :
    Decidable (ResponsibilityDelegationNonAuthority state) := by
  unfold ResponsibilityDelegationNonAuthority
  infer_instance

structure ResponsibilityDelegationInvariant
    (state : ResponsibilityDelegationState) : Prop where
  authorityInvariant : Authority.DelegationStateInvariant state.authorityState
  accountableMatchesDelegate :
    state.accountableOwnerId = state.authorityState.currentDelegateId
  accountableOwnerPositive : 0 < state.accountableOwnerId
  reviewerPositive : 0 < state.reviewerId
  reviewerIndependentFromOwner : state.reviewerId ≠ state.accountableOwnerId
  reviewerIndependentFromPrincipal :
    state.reviewerId ≠ state.authorityState.currentPrincipalId
  evidenceCustodianPositive : 0 < state.evidenceCustodianId
  evidenceCustodianIndependentFromOwner :
    state.evidenceCustodianId ≠ state.accountableOwnerId
  receiptAligned :
    state.responsibilityReceiptCount = state.authorityState.receiptCount
  residualDepthAligned :
    state.residualOwnerIds.length = state.authorityState.depth
  assignmentComplete : state.assignmentComplete = true
  interventionPathPresent : state.interventionPathPresent = true
  appealPathPresent : state.appealPathPresent = true
  remedyPathPresent : state.remedyPathPresent = true
  nonAuthority : ResponsibilityDelegationNonAuthority state

theorem responsibility_delegation_accepted_step_is_valid
    {state next : ResponsibilityDelegationState}
    {event : ResponsibilityDelegationEvent}
    (accepted : ResponsibilityDelegationStep state event = some next) :
    ValidResponsibilityDelegationEvent state event := by
  unfold ResponsibilityDelegationStep at accepted
  split at accepted
  · assumption
  · simp at accepted

theorem responsibility_delegation_accepted_step_applies_event
    {state next : ResponsibilityDelegationState}
    {event : ResponsibilityDelegationEvent}
    (accepted : ResponsibilityDelegationStep state event = some next) :
    next = ApplyResponsibilityDelegationEvent state event := by
  unfold ResponsibilityDelegationStep at accepted
  split at accepted
  · exact (Option.some.inj accepted).symm
  · simp at accepted

theorem responsibility_delegation_step_refines_authority_step
    {state next : ResponsibilityDelegationState}
    {event : ResponsibilityDelegationEvent}
    (accepted : ResponsibilityDelegationStep state event = some next) :
    Authority.DelegationStep state.authorityState event.authorityEvent =
      some next.authorityState := by
  have valid := responsibility_delegation_accepted_step_is_valid accepted
  have applies := responsibility_delegation_accepted_step_applies_event accepted
  rw [applies]
  rcases valid with ⟨_, _, authorityValid, _⟩
  simp [ApplyResponsibilityDelegationEvent, Authority.DelegationStep,
    authorityValid]

theorem responsibility_delegation_step_assigns_exact_child_owner
    {state next : ResponsibilityDelegationState}
    {event : ResponsibilityDelegationEvent}
    (accepted : ResponsibilityDelegationStep state event = some next) :
    next.accountableOwnerId = event.authorityEvent.childDelegateId := by
  have valid := responsibility_delegation_accepted_step_is_valid accepted
  have applies := responsibility_delegation_accepted_step_applies_event accepted
  rw [applies]
  exact valid.2.2.2.1

theorem responsibility_delegation_step_retains_prior_owner
    {state next : ResponsibilityDelegationState}
    {event : ResponsibilityDelegationEvent}
    (accepted : ResponsibilityDelegationStep state event = some next) :
    next.residualOwnerIds =
      state.accountableOwnerId :: state.residualOwnerIds := by
  rw [responsibility_delegation_accepted_step_applies_event accepted]
  rfl

theorem responsibility_delegation_step_adds_exact_receipt
    {state next : ResponsibilityDelegationState}
    {event : ResponsibilityDelegationEvent}
    (accepted : ResponsibilityDelegationStep state event = some next) :
    next.responsibilityReceiptCount =
      state.responsibilityReceiptCount + 1 := by
  rw [responsibility_delegation_accepted_step_applies_event accepted]
  rfl

theorem responsibility_delegation_step_preserves_non_authority
    {state next : ResponsibilityDelegationState}
    {event : ResponsibilityDelegationEvent}
    (bounded : ResponsibilityDelegationNonAuthority state)
    (accepted : ResponsibilityDelegationStep state event = some next) :
    ResponsibilityDelegationNonAuthority next := by
  have authorityAccepted :=
    responsibility_delegation_step_refines_authority_step accepted
  have applies := responsibility_delegation_accepted_step_applies_event accepted
  rw [applies] at authorityAccepted
  have authorityBounded := Authority.delegation_step_preserves_non_authority
    bounded.2.2 authorityAccepted
  rw [applies]
  exact ⟨bounded.1, bounded.2.1, authorityBounded⟩

theorem responsibility_delegation_step_preserves_invariant
    {state next : ResponsibilityDelegationState}
    {event : ResponsibilityDelegationEvent}
    (safe : ResponsibilityDelegationInvariant state)
    (accepted : ResponsibilityDelegationStep state event = some next) :
    ResponsibilityDelegationInvariant next := by
  have valid := responsibility_delegation_accepted_step_is_valid accepted
  have authorityAccepted :=
    responsibility_delegation_step_refines_authority_step accepted
  have applies := responsibility_delegation_accepted_step_applies_event accepted
  have preservedNonAuthority :=
    responsibility_delegation_step_preserves_non_authority
      safe.nonAuthority accepted
  rw [applies] at authorityAccepted
  rw [applies] at preservedNonAuthority
  rcases valid with
    ⟨ownerMatches, transferringOwner, authorityValid, nextOwner,
      nextOwnerPositive, reviewerPositive, reviewerNotPrincipal,
      reviewerNotOwner, custodianPositive, custodianNotOwner,
      assignmentComplete, handoffAcknowledgment, interventionTransferred,
      evidenceTransferred, appealTransferred, remedyTransferred,
      residualAcknowledged, noSupport, noEffect⟩
  rw [applies]
  exact {
    authorityInvariant := Authority.delegation_step_preserves_invariant
      safe.authorityInvariant authorityAccepted
    accountableMatchesDelegate := by
      simp [ApplyResponsibilityDelegationEvent,
        Authority.ApplyDelegationEvent, nextOwner]
    accountableOwnerPositive := nextOwnerPositive
    reviewerPositive := reviewerPositive
    reviewerIndependentFromOwner := reviewerNotOwner
    reviewerIndependentFromPrincipal := by
      simpa [ApplyResponsibilityDelegationEvent,
        Authority.ApplyDelegationEvent] using reviewerNotPrincipal
    evidenceCustodianPositive := custodianPositive
    evidenceCustodianIndependentFromOwner := custodianNotOwner
    receiptAligned := by
      simp [ApplyResponsibilityDelegationEvent,
        Authority.ApplyDelegationEvent, safe.receiptAligned]
    residualDepthAligned := by
      simp [ApplyResponsibilityDelegationEvent,
        Authority.ApplyDelegationEvent, safe.residualDepthAligned]
    assignmentComplete := rfl
    interventionPathPresent := rfl
    appealPathPresent := rfl
    remedyPathPresent := rfl
    nonAuthority := preservedNonAuthority }

theorem responsibility_delegation_run_preserves_invariant
    {state final : ResponsibilityDelegationState}
    {events : List ResponsibilityDelegationEvent}
    (safe : ResponsibilityDelegationInvariant state)
    (ran : ResponsibilityDelegationRun state events = some final) :
    ResponsibilityDelegationInvariant final := by
  induction events generalizing state with
  | nil =>
      simp [ResponsibilityDelegationRun] at ran
      subst final
      exact safe
  | cons event tail ih =>
      cases stepped : ResponsibilityDelegationStep state event with
      | none => simp [ResponsibilityDelegationRun, stepped] at ran
      | some next =>
          have tailRan : ResponsibilityDelegationRun next tail = some final := by
            simpa [ResponsibilityDelegationRun, stepped] using ran
          exact ih
            (responsibility_delegation_step_preserves_invariant safe stepped)
            tailRan

theorem responsibility_delegation_run_refines_authority_run
    {state final : ResponsibilityDelegationState}
    {events : List ResponsibilityDelegationEvent}
    (ran : ResponsibilityDelegationRun state events = some final) :
    Authority.DelegationRun state.authorityState
      (events.map (fun event => event.authorityEvent)) =
        some final.authorityState := by
  induction events generalizing state with
  | nil =>
      simp [ResponsibilityDelegationRun] at ran
      subst final
      simp [Authority.DelegationRun]
  | cons event tail ih =>
      cases stepped : ResponsibilityDelegationStep state event with
      | none => simp [ResponsibilityDelegationRun, stepped] at ran
      | some next =>
          have tailRan : ResponsibilityDelegationRun next tail = some final := by
            simpa [ResponsibilityDelegationRun, stepped] using ran
          have authorityStepped :=
            responsibility_delegation_step_refines_authority_step stepped
          simp [Authority.DelegationRun, authorityStepped, ih tailRan]

theorem responsibility_delegation_run_has_no_owner_gap
    {state final : ResponsibilityDelegationState}
    {events : List ResponsibilityDelegationEvent}
    (safe : ResponsibilityDelegationInvariant state)
    (ran : ResponsibilityDelegationRun state events = some final) :
    0 < final.accountableOwnerId ∧
      final.accountableOwnerId = final.authorityState.currentDelegateId := by
  have finalSafe := responsibility_delegation_run_preserves_invariant safe ran
  exact ⟨finalSafe.accountableOwnerPositive,
    finalSafe.accountableMatchesDelegate⟩

theorem responsibility_delegation_run_accounts_exact_receipts
    {state final : ResponsibilityDelegationState}
    {events : List ResponsibilityDelegationEvent}
    (ran : ResponsibilityDelegationRun state events = some final) :
    final.responsibilityReceiptCount =
      state.responsibilityReceiptCount + events.length := by
  induction events generalizing state with
  | nil =>
      simp [ResponsibilityDelegationRun] at ran
      subst final
      simp
  | cons event tail ih =>
      cases stepped : ResponsibilityDelegationStep state event with
      | none => simp [ResponsibilityDelegationRun, stepped] at ran
      | some next =>
          have tailRan : ResponsibilityDelegationRun next tail = some final := by
            simpa [ResponsibilityDelegationRun, stepped] using ran
          calc
            final.responsibilityReceiptCount =
                next.responsibilityReceiptCount + tail.length := ih tailRan
            _ = (state.responsibilityReceiptCount + 1) + tail.length := by
              rw [responsibility_delegation_step_adds_exact_receipt stepped]
            _ = state.responsibilityReceiptCount + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem responsibility_delegation_run_accounts_residual_owners
    {state final : ResponsibilityDelegationState}
    {events : List ResponsibilityDelegationEvent}
    (ran : ResponsibilityDelegationRun state events = some final) :
    final.residualOwnerIds.length =
      state.residualOwnerIds.length + events.length := by
  induction events generalizing state with
  | nil =>
      simp [ResponsibilityDelegationRun] at ran
      subst final
      simp
  | cons event tail ih =>
      cases stepped : ResponsibilityDelegationStep state event with
      | none => simp [ResponsibilityDelegationRun, stepped] at ran
      | some next =>
          have tailRan : ResponsibilityDelegationRun next tail = some final := by
            simpa [ResponsibilityDelegationRun, stepped] using ran
          calc
            final.residualOwnerIds.length =
                next.residualOwnerIds.length + tail.length := ih tailRan
            _ = (state.residualOwnerIds.length + 1) + tail.length := by
              rw [responsibility_delegation_step_retains_prior_owner stepped]
              simp
            _ = state.residualOwnerIds.length + (event :: tail).length := by
              simp only [List.length_cons]
              omega

theorem responsibility_delegation_successful_run_has_valid_trace
    {state final : ResponsibilityDelegationState}
    {events : List ResponsibilityDelegationEvent}
    (ran : ResponsibilityDelegationRun state events = some final) :
    ResponsibilityDelegationTraceValid state events := by
  induction events generalizing state with
  | nil => trivial
  | cons event tail ih =>
      cases stepped : ResponsibilityDelegationStep state event with
      | none => simp [ResponsibilityDelegationRun, stepped] at ran
      | some next =>
          have tailRan : ResponsibilityDelegationRun next tail = some final := by
            simpa [ResponsibilityDelegationRun, stepped] using ran
          have applies :=
            responsibility_delegation_accepted_step_applies_event stepped
          exact ⟨responsibility_delegation_accepted_step_is_valid stepped, by
            rw [← applies]
            exact ih tailRan⟩

theorem responsibility_delegation_run_composes_across_event_batches
    (state : ResponsibilityDelegationState)
    (left right : List ResponsibilityDelegationEvent) :
    ResponsibilityDelegationRun state (left ++ right) =
      match ResponsibilityDelegationRun state left with
      | none => none
      | some middle => ResponsibilityDelegationRun middle right := by
  induction left generalizing state with
  | nil => simp [ResponsibilityDelegationRun]
  | cons event tail ih =>
      cases stepped : ResponsibilityDelegationStep state event <;>
        simp [ResponsibilityDelegationRun, stepped, ih]

def responsibilityDelegationInitialState : ResponsibilityDelegationState :=
  { authorityState := Authority.delegationInitialState
    accountableOwnerId := 2
    reviewerId := 50
    evidenceCustodianId := 60
    residualOwnerIds := []
    responsibilityReceiptCount := 0
    assignmentComplete := true
    interventionPathPresent := true
    appealPathPresent := true
    remedyPathPresent := true
    supportAssigned := false
    externalEffectCommitted := false }

def firstResponsibilityDelegationEvent : ResponsibilityDelegationEvent :=
  { authorityEvent := Authority.firstDelegationEvent
    transferringOwnerId := 2
    nextAccountableOwnerId := 3
    reviewerId := 51
    evidenceCustodianId := 61 }

def secondResponsibilityDelegationEvent : ResponsibilityDelegationEvent :=
  { authorityEvent := Authority.secondDelegationEvent
    transferringOwnerId := 3
    nextAccountableOwnerId := 4
    reviewerId := 52
    evidenceCustodianId := 62 }

def twoHopResponsibilityDelegationTrace :
    List ResponsibilityDelegationEvent :=
  [firstResponsibilityDelegationEvent, secondResponsibilityDelegationEvent]

theorem responsibility_delegation_initial_state_is_invariant :
    ResponsibilityDelegationInvariant responsibilityDelegationInitialState := by
  exact {
    authorityInvariant := Authority.delegation_initial_state_is_invariant
    accountableMatchesDelegate := by native_decide
    accountableOwnerPositive := by native_decide
    reviewerPositive := by native_decide
    reviewerIndependentFromOwner := by native_decide
    reviewerIndependentFromPrincipal := by native_decide
    evidenceCustodianPositive := by native_decide
    evidenceCustodianIndependentFromOwner := by native_decide
    receiptAligned := by native_decide
    residualDepthAligned := by native_decide
    assignmentComplete := by native_decide
    interventionPathPresent := by native_decide
    appealPathPresent := by native_decide
    remedyPathPresent := by native_decide
    nonAuthority := by native_decide }

theorem two_hop_responsibility_delegation_preserves_accountability :
    ∃ final,
      ResponsibilityDelegationRun responsibilityDelegationInitialState
        twoHopResponsibilityDelegationTrace = some final ∧
      final.accountableOwnerId = 4 ∧
      final.authorityState.currentDelegateId = 4 ∧
      final.authorityState.currentCeiling = .read ∧
      final.residualOwnerIds = [3, 2] ∧
      final.responsibilityReceiptCount = 2 ∧
      final.authorityState.receiptCount = 2 ∧
      ResponsibilityDelegationNonAuthority final := by
  refine ⟨ApplyResponsibilityDelegationEvent
    (ApplyResponsibilityDelegationEvent responsibilityDelegationInitialState
      firstResponsibilityDelegationEvent)
    secondResponsibilityDelegationEvent, ?_⟩
  native_decide

theorem responsibility_delegation_closed_countermodels :
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with transferringOwnerId := 99 } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with nextAccountableOwnerId := 99 } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with reviewerId := 2 } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with reviewerId := 3 } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with evidenceCustodianId := 3 } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with
            assignment := { ({} : AccountabilityAssignment) with
              informationAvailable := false } } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with handoffAcknowledgment := false } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with
            interventionPathTransferred := false } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with
            evidenceCustodyTransferred := false } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with appealPathTransferred := false } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with remedyPathTransferred := false } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with
            residualCustodyAcknowledged := false } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with supportRequested := true } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with externalEffectRequested := true } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with
            authorityEvent := { Authority.firstDelegationEvent with
              childCeiling := .approve } } = none ∧
    ResponsibilityDelegationStep responsibilityDelegationInitialState
        { firstResponsibilityDelegationEvent with
            authorityEvent := { Authority.firstDelegationEvent with epoch := 8 } } = none := by
  native_decide

structure ThinResponsibilitySummary where
  delegationDepth : Nat
  receiptCount : Nat
  ceilingRank : Nat
  residualCount : Nat
deriving DecidableEq, Repr

def thinResponsibilitySummaryOf
    (state : ResponsibilityDelegationState) : ThinResponsibilitySummary :=
  { delegationDepth := state.authorityState.depth
    receiptCount := state.responsibilityReceiptCount
    ceilingRank := state.authorityState.currentCeiling.rank
    residualCount := state.residualOwnerIds.length }

def responsibilityAssignableFor
    (state : ResponsibilityDelegationState) : Bool :=
  decide (0 < state.accountableOwnerId ∧
    0 < state.reviewerId ∧
    state.reviewerId ≠ state.accountableOwnerId ∧
    0 < state.evidenceCustodianId ∧
    state.evidenceCustodianId ≠ state.accountableOwnerId)

def responsibilityGapState : ResponsibilityDelegationState :=
  { responsibilityDelegationInitialState with
      accountableOwnerId := 0
      reviewerId := 0
      evidenceCustodianId := 0 }

theorem thin_responsibility_summary_hides_accountability_gap :
    thinResponsibilitySummaryOf responsibilityDelegationInitialState =
      thinResponsibilitySummaryOf responsibilityGapState ∧
    responsibilityAssignableFor responsibilityDelegationInitialState = true ∧
    responsibilityAssignableFor responsibilityGapState = false := by
  native_decide

theorem thin_responsibility_summary_cannot_recover_accountability
    (classify : ThinResponsibilitySummary -> Bool) :
    classify (thinResponsibilitySummaryOf responsibilityDelegationInitialState) ≠ true ∨
      classify (thinResponsibilitySummaryOf responsibilityGapState) ≠ false := by
  have same :
      thinResponsibilitySummaryOf responsibilityDelegationInitialState =
        thinResponsibilitySummaryOf responsibilityGapState :=
    thin_responsibility_summary_hides_accountability_gap.1
  by_cases accepted :
      classify (thinResponsibilitySummaryOf responsibilityDelegationInitialState) = true
  · right
    rw [← same]
    simp [accepted]
  · exact Or.inl accepted

end AsiStackProofs.HumanAIOrganizations

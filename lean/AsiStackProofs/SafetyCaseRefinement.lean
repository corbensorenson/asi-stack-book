namespace AsiStackProofs.SafetyCaseRefinement

inductive Stage where
  | draft | scoped | evidenced | challenged | reviewed | readinessBound
deriving DecidableEq, Repr

inductive EventKind where
  | scope | attachEvidence | recordChallenge | recordReview | requestReadiness | invalidate
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectCaseSubstitution | rejectEventReplay | rejectAuthorityLeak
  | requestDeploymentContext | requestTopClaim | requestHazardModel | requestArgumentStrategy
  | requestEvidence | requestCurrentEvidence | requestAssumptions
  | requestCountercase | requestDefeaterDisposition
  | requestIndependentReview | requestReviewerCompetence | requestConflictDisclosure
  | requestAcceptanceCriterion | requestResidualOwner | requestDecisionAuthority
  | rejectAuthorityLaundering | requestInvalidationCause | requestAffectedPaths
  | requestDescendantInvalidation
  | acceptScope | acceptEvidence | acceptChallenge | acceptReview | acceptReadiness | acceptInvalidation
deriving DecidableEq, Repr

structure Packet where
  caseId : Nat
  caseVersion : Nat
  contextDigest : Nat
  claimDigest : Nat
  hazardDigest : Nat
  evidenceDigest : Nat
  countercaseDigest : Nat
  reviewerDigest : Nat
  authorityDigest : Nat
  residualDigest : Nat
  eventDigest : Nat
  deploymentContextPresent : Bool
  topClaimScoped : Bool
  hazardModelPresent : Bool
  argumentStrategyPresent : Bool
  evidenceReferencesPresent : Bool
  evidenceDependenciesCurrent : Bool
  assumptionsPresent : Bool
  countercaseReviewPresent : Bool
  defeaterDispositionPresent : Bool
  unresolvedDefeaterPresent : Bool
  independentReviewPresent : Bool
  reviewerCompetenceRecorded : Bool
  reviewerConflictDisclosed : Bool
  acceptanceCriterionPresent : Bool
  residualOwnerPresent : Bool
  decisionAuthorityPresent : Bool
  authoritySeparationPresent : Bool
  invalidationCausePresent : Bool
  affectedPathsPresent : Bool
  descendantInvalidationComplete : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
deriving DecidableEq, Repr

structure State where
  stage : Stage
  caseId : Nat
  caseVersion : Nat
  contextDigest : Nat
  claimDigest : Nat
  hazardDigest : Nat
  evidenceDigest : Nat
  countercaseDigest : Nat
  reviewerDigest : Nat
  authorityDigest : Nat
  residualDigest : Nat
  lastEventDigest : Nat
  receiptCount : Nat
  readinessHandoffCount : Nat
  invalidationCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .draft => .scope
  | .scoped => .attachEvidence
  | .evidenced => .recordChallenge
  | .challenged => .recordReview
  | .reviewed => .requestReadiness
  | .readinessBound => .invalidate

def identityMatches (state : State) (packet : Packet) : Bool :=
  state.caseId = packet.caseId && state.caseVersion = packet.caseVersion &&
  state.contextDigest = packet.contextDigest && state.claimDigest = packet.claimDigest &&
  state.hazardDigest = packet.hazardDigest && state.evidenceDigest = packet.evidenceDigest &&
  state.countercaseDigest = packet.countercaseDigest && state.reviewerDigest = packet.reviewerDigest &&
  state.authorityDigest = packet.authorityDigest && state.residualDigest = packet.residualDigest

def routeFor (state : State) (kind : EventKind) (packet : Packet) : Route :=
  if kind != expectedKind state.stage then .rejectWrongStage
  else if identityMatches state packet = false then .rejectCaseSubstitution
  else if packet.eventDigest = state.lastEventDigest then .rejectEventReplay
  else if packet.supportAssignmentRequested || packet.externalEffectRequested then .rejectAuthorityLeak
  else match state.stage with
  | .draft =>
      if packet.deploymentContextPresent = false then .requestDeploymentContext
      else if packet.topClaimScoped = false then .requestTopClaim
      else if packet.hazardModelPresent = false then .requestHazardModel
      else if packet.argumentStrategyPresent = false then .requestArgumentStrategy
      else .acceptScope
  | .scoped =>
      if packet.evidenceReferencesPresent = false then .requestEvidence
      else if packet.evidenceDependenciesCurrent = false then .requestCurrentEvidence
      else if packet.assumptionsPresent = false then .requestAssumptions
      else .acceptEvidence
  | .evidenced =>
      if packet.countercaseReviewPresent = false then .requestCountercase
      else if packet.defeaterDispositionPresent = false || packet.unresolvedDefeaterPresent then
        .requestDefeaterDisposition
      else .acceptChallenge
  | .challenged =>
      if packet.independentReviewPresent = false then .requestIndependentReview
      else if packet.reviewerCompetenceRecorded = false then .requestReviewerCompetence
      else if packet.reviewerConflictDisclosed = false then .requestConflictDisclosure
      else .acceptReview
  | .reviewed =>
      if packet.acceptanceCriterionPresent = false then .requestAcceptanceCriterion
      else if packet.residualOwnerPresent = false then .requestResidualOwner
      else if packet.decisionAuthorityPresent = false then .requestDecisionAuthority
      else if packet.authoritySeparationPresent = false then .rejectAuthorityLaundering
      else .acceptReadiness
  | .readinessBound =>
      if packet.invalidationCausePresent = false then .requestInvalidationCause
      else if packet.affectedPathsPresent = false then .requestAffectedPaths
      else if packet.descendantInvalidationComplete = false then .requestDescendantInvalidation
      else .acceptInvalidation

def accepted : Route -> Bool
  | .acceptScope | .acceptEvidence | .acceptChallenge | .acceptReview
  | .acceptReadiness | .acceptInvalidation => true
  | _ => false

def nextStage : Stage -> Stage
  | .draft => .scoped
  | .scoped => .evidenced
  | .evidenced => .challenged
  | .challenged => .reviewed
  | .reviewed => .readinessBound
  | .readinessBound => .challenged

def applyEvent (state : State) (kind : EventKind) (packet : Packet) : State × Route :=
  let route := routeFor state kind packet
  if accepted route then
    ({ state with
       stage := nextStage state.stage
       lastEventDigest := packet.eventDigest
       receiptCount := state.receiptCount + 1
       readinessHandoffCount := state.readinessHandoffCount + (if route = .acceptReadiness then 1 else 0)
       invalidationCount := state.invalidationCount + (if route = .acceptInvalidation then 1 else 0) }, route)
  else (state, route)

theorem rejected_event_preserves_state (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = false) :
    (applyEvent state kind packet).1 = state := by simp [applyEvent, h]

theorem accepted_event_adds_one_receipt (state : State) (kind : EventKind) (packet : Packet)
    (h : accepted (routeFor state kind packet) = true) :
    (applyEvent state kind packet).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, h]

theorem event_cannot_assign_support_or_external_effect (state : State) (kind : EventKind)
    (packet : Packet) :
    (applyEvent state kind packet).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state kind packet).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state kind packet) = true <;> simp [applyEvent, h]

def canonicalPacket : Packet :=
  { caseId := 701, caseVersion := 3, contextDigest := 702, claimDigest := 703,
    hazardDigest := 704, evidenceDigest := 705, countercaseDigest := 706,
    reviewerDigest := 707, authorityDigest := 708, residualDigest := 709, eventDigest := 1,
    deploymentContextPresent := true, topClaimScoped := true, hazardModelPresent := true,
    argumentStrategyPresent := true, evidenceReferencesPresent := true,
    evidenceDependenciesCurrent := true, assumptionsPresent := true,
    countercaseReviewPresent := true, defeaterDispositionPresent := true,
    unresolvedDefeaterPresent := false, independentReviewPresent := true,
    reviewerCompetenceRecorded := true, reviewerConflictDisclosed := true,
    acceptanceCriterionPresent := true, residualOwnerPresent := true,
    decisionAuthorityPresent := true, authoritySeparationPresent := true,
    invalidationCausePresent := true, affectedPathsPresent := true,
    descendantInvalidationComplete := true, supportAssignmentRequested := false,
    externalEffectRequested := false }

def canonicalState (stage : Stage) : State :=
  { stage := stage, caseId := 701, caseVersion := 3, contextDigest := 702,
    claimDigest := 703, hazardDigest := 704, evidenceDigest := 705,
    countercaseDigest := 706, reviewerDigest := 707, authorityDigest := 708,
    residualDigest := 709, lastEventDigest := 0, receiptCount := 0,
    readinessHandoffCount := 0, invalidationCount := 0,
    supportAssignmentCount := 0, externalEffectCount := 0 }

theorem missing_hazard_blocks_scope :
  routeFor (canonicalState .draft) .scope { canonicalPacket with hazardModelPresent := false } =
    .requestHazardModel := by rfl

theorem stale_evidence_blocks_evidence_stage :
  routeFor (canonicalState .scoped) .attachEvidence
    { canonicalPacket with evidenceDependenciesCurrent := false } = .requestCurrentEvidence := by rfl

theorem unresolved_defeater_blocks_challenge_stage :
  routeFor (canonicalState .evidenced) .recordChallenge
    { canonicalPacket with unresolvedDefeaterPresent := true } = .requestDefeaterDisposition := by rfl

theorem conflicted_review_blocks_review_stage :
  routeFor (canonicalState .challenged) .recordReview
    { canonicalPacket with reviewerConflictDisclosed := false } = .requestConflictDisclosure := by rfl

theorem case_status_cannot_launder_release_authority :
  routeFor (canonicalState .reviewed) .requestReadiness
    { canonicalPacket with authoritySeparationPresent := false } = .rejectAuthorityLaundering := by rfl

theorem incomplete_descendant_invalidation_blocks_reentry :
  routeFor (canonicalState .readinessBound) .invalidate
    { canonicalPacket with descendantInvalidationComplete := false } =
    .requestDescendantInvalidation := by rfl

def eventPacket (digest : Nat) : Packet := { canonicalPacket with eventDigest := digest }

theorem full_case_lifecycle_returns_to_challenge_after_invalidation :
  let s0 := canonicalState .draft
  let s1 := (applyEvent s0 .scope (eventPacket 1)).1
  let s2 := (applyEvent s1 .attachEvidence (eventPacket 2)).1
  let s3 := (applyEvent s2 .recordChallenge (eventPacket 3)).1
  let s4 := (applyEvent s3 .recordReview (eventPacket 4)).1
  let s5 := (applyEvent s4 .requestReadiness (eventPacket 5)).1
  let s6 := (applyEvent s5 .invalidate (eventPacket 6)).1
  s6.stage = .challenged ∧ s6.receiptCount = 6 ∧ s6.readinessHandoffCount = 1 ∧
    s6.invalidationCount = 1 ∧ s6.supportAssignmentCount = 0 ∧ s6.externalEffectCount = 0 := by
  native_decide

end AsiStackProofs.SafetyCaseRefinement

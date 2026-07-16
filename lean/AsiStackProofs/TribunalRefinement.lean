namespace AsiStackProofs.TribunalRefinement

inductive Stage where
  | idle
  | requested
  | dossierBound
  | panelRun
  | verdictIssued
  | acknowledged
  | appealResolved
deriving DecidableEq, Repr

inductive EventKind where
  | requestReview
  | bindDossier
  | runPanel
  | issueVerdict
  | acknowledgeVerdict
  | resolveAppeal
deriving DecidableEq, Repr

inductive Verdict where
  | none
  | acceptScoped
  | revise
  | reject
  | block
  | abstain
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage
  | rejectCaseSubstitution
  | rejectEvidenceSubstitution
  | rejectEventReplay
  | rejectAuthorityLeak
  | requestReview
  | requestDossierAndEvidence
  | requestAdversarialProbe
  | requestIndependentPanel
  | requestIndependenceGraph
  | requestFalsification
  | preserveAbstention
  | preserveVeto
  | rejectChangedEvidenceReuse
  | rejectDefaultApproval
  | preserveDissent
  | requestActionsAndConstraints
  | requestResidual
  | requestAppealPath
  | handoffToEvidenceOwner
  | requestConsumerAcknowledgment
  | requestAppealResolution
  | acceptReviewRequest
  | acceptDossierBinding
  | acceptPanelRun
  | acceptVerdict
  | acceptAcknowledgment
  | acceptAppealResolution
deriving DecidableEq, Repr

structure Packet where
  caseId : Nat
  caseVersion : Nat
  targetDigest : Nat
  evidenceVersion : Nat
  evidenceDigest : Nat
  dossierDigest : Nat
  panelDigest : Nat
  policyDigest : Nat
  consumerDigest : Nat
  verdictVersion : Nat
  eventDigest : Nat
  reviewRequired : Bool
  reviewRequested : Bool
  dossierPresent : Bool
  evidenceRefsPresent : Bool
  highRisk : Bool
  adversarialProbePresent : Bool
  reviewerCount : Nat
  independenceGroupCount : Nat
  independenceGraphAcyclic : Bool
  sharedEvidenceRiskRecorded : Bool
  falsificationAttempted : Bool
  abstentionPresent : Bool
  abstentionPreserved : Bool
  vetoPresent : Bool
  vetoPreserved : Bool
  priorVerdictReused : Bool
  evidenceUnchanged : Bool
  reuseGuardPresent : Bool
  defaultApprovalUsed : Bool
  dissentPresent : Bool
  dissentPreserved : Bool
  actionRequired : Bool
  requiredActionsPresent : Bool
  constraintsPresent : Bool
  residualPresent : Bool
  appealAvailable : Bool
  appealRequested : Bool
  appealRecorded : Bool
  supportChangeRequested : Bool
  evidenceOwnerHandoffPresent : Bool
  consumerAcknowledgmentPresent : Bool
  supportAssignmentRequested : Bool
  externalEffectRequested : Bool
  verdict : Verdict
deriving DecidableEq, Repr

structure Event where
  kind : EventKind
  packet : Packet
deriving DecidableEq, Repr

structure State where
  stage : Stage
  caseId : Nat
  caseVersion : Nat
  targetDigest : Nat
  evidenceVersion : Nat
  evidenceDigest : Nat
  dossierDigest : Nat
  panelDigest : Nat
  policyDigest : Nat
  consumerDigest : Nat
  verdictVersion : Nat
  lastEventDigest : Nat
  panelAccepted : Bool
  verdict : Verdict
  receiptCount : Nat
  supportAssignmentCount : Nat
  externalEffectCount : Nat
deriving DecidableEq, Repr

def expectedKind : Stage -> EventKind
  | .idle => .requestReview
  | .requested => .bindDossier
  | .dossierBound => .runPanel
  | .panelRun => .issueVerdict
  | .verdictIssued => .acknowledgeVerdict
  | .acknowledged => .resolveAppeal
  | .appealResolved => .resolveAppeal

def exactCaseBinding (state : State) (packet : Packet) : Bool :=
  packet.caseId == state.caseId &&
  packet.caseVersion == state.caseVersion &&
  packet.targetDigest == state.targetDigest &&
  packet.policyDigest == state.policyDigest &&
  packet.consumerDigest == state.consumerDigest &&
  packet.verdictVersion == state.verdictVersion

def exactEvidenceBinding (state : State) (packet : Packet) : Bool :=
  packet.evidenceVersion == state.evidenceVersion &&
  packet.evidenceDigest == state.evidenceDigest &&
  packet.dossierDigest == state.dossierDigest &&
  packet.panelDigest == state.panelDigest

def actionVerdict : Verdict -> Bool
  | .revise | .reject | .block => true
  | .none | .acceptScoped | .abstain => false

def routeFor (state : State) (event : Event) : Route :=
  if event.kind != expectedKind state.stage then .rejectWrongStage
  else if ! exactCaseBinding state event.packet then .rejectCaseSubstitution
  else if state.stage != .idle && ! exactEvidenceBinding state event.packet then
    .rejectEvidenceSubstitution
  else if event.packet.eventDigest == state.lastEventDigest then .rejectEventReplay
  else if event.packet.supportAssignmentRequested || event.packet.externalEffectRequested then
    .rejectAuthorityLeak
  else match state.stage with
  | .idle =>
      if event.packet.reviewRequired && ! event.packet.reviewRequested then .requestReview
      else .acceptReviewRequest
  | .requested =>
      if ! event.packet.dossierPresent || ! event.packet.evidenceRefsPresent then
        .requestDossierAndEvidence
      else .acceptDossierBinding
  | .dossierBound =>
      if event.packet.highRisk && ! event.packet.adversarialProbePresent then
        .requestAdversarialProbe
      else if event.packet.highRisk && event.packet.reviewerCount < 3 then
        .requestIndependentPanel
      else if event.packet.independenceGroupCount != event.packet.reviewerCount ||
          ! event.packet.independenceGraphAcyclic ||
          ! event.packet.sharedEvidenceRiskRecorded then
        .requestIndependenceGraph
      else if ! event.packet.falsificationAttempted then .requestFalsification
      else if event.packet.abstentionPresent && ! event.packet.abstentionPreserved then
        .preserveAbstention
      else if event.packet.vetoPresent && ! event.packet.vetoPreserved then .preserveVeto
      else .acceptPanelRun
  | .panelRun =>
      if event.packet.priorVerdictReused &&
          (! event.packet.evidenceUnchanged || ! event.packet.reuseGuardPresent) then
        .rejectChangedEvidenceReuse
      else if event.packet.defaultApprovalUsed then .rejectDefaultApproval
      else if event.packet.dissentPresent && ! event.packet.dissentPreserved then
        .preserveDissent
      else if (event.packet.actionRequired || actionVerdict event.packet.verdict) &&
          (! event.packet.requiredActionsPresent || ! event.packet.constraintsPresent) then
        .requestActionsAndConstraints
      else if ! event.packet.residualPresent then .requestResidual
      else if ! event.packet.appealAvailable then .requestAppealPath
      else if event.packet.supportChangeRequested &&
          ! event.packet.evidenceOwnerHandoffPresent then
        .handoffToEvidenceOwner
      else if event.packet.verdict == .none then .rejectDefaultApproval
      else .acceptVerdict
  | .verdictIssued =>
      if event.packet.verdict != state.verdict then .rejectCaseSubstitution
      else if ! event.packet.consumerAcknowledgmentPresent then
        .requestConsumerAcknowledgment
      else .acceptAcknowledgment
  | .acknowledged =>
      if event.packet.verdict != state.verdict then .rejectCaseSubstitution
      else if event.packet.appealRequested && ! event.packet.appealRecorded then
        .requestAppealResolution
      else .acceptAppealResolution
  | .appealResolved => .rejectWrongStage

def accepted : Route -> Bool
  | .acceptReviewRequest
  | .acceptDossierBinding
  | .acceptPanelRun
  | .acceptVerdict
  | .acceptAcknowledgment
  | .acceptAppealResolution => true
  | _ => false

def advanceStage : Stage -> Stage
  | .idle => .requested
  | .requested => .dossierBound
  | .dossierBound => .panelRun
  | .panelRun => .verdictIssued
  | .verdictIssued => .acknowledged
  | .acknowledged => .appealResolved
  | .appealResolved => .appealResolved

def applyEvent (state : State) (event : Event) : State × Route :=
  let route := routeFor state event
  if accepted route then
    ({ state with
       stage := advanceStage state.stage
       lastEventDigest := event.packet.eventDigest
       panelAccepted := if state.stage == .dossierBound then true else state.panelAccepted
       verdict := if state.stage == .panelRun then event.packet.verdict else state.verdict
       receiptCount := state.receiptCount + 1 }, route)
  else (state, route)

theorem apply_event_preserves_case_and_evidence_identity
    (state : State) (event : Event) :
    (applyEvent state event).1.caseId = state.caseId ∧
    (applyEvent state event).1.caseVersion = state.caseVersion ∧
    (applyEvent state event).1.targetDigest = state.targetDigest ∧
    (applyEvent state event).1.evidenceVersion = state.evidenceVersion ∧
    (applyEvent state event).1.evidenceDigest = state.evidenceDigest := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, h]

theorem apply_event_cannot_assign_support_or_external_effect
    (state : State) (event : Event) :
    (applyEvent state event).1.supportAssignmentCount = state.supportAssignmentCount ∧
    (applyEvent state event).1.externalEffectCount = state.externalEffectCount := by
  by_cases h : accepted (routeFor state event) = true <;>
    simp [applyEvent, h]

theorem accepted_step_adds_exactly_one_receipt
    (state : State) (event : Event)
    (h : accepted (routeFor state event) = true) :
    (applyEvent state event).1.receiptCount = state.receiptCount + 1 := by
  simp [applyEvent, h]

def canonicalPacket : Packet :=
  { caseId := 71
    caseVersion := 4
    targetDigest := 101
    evidenceVersion := 9
    evidenceDigest := 201
    dossierDigest := 202
    panelDigest := 203
    policyDigest := 301
    consumerDigest := 401
    verdictVersion := 2
    eventDigest := 1
    reviewRequired := true
    reviewRequested := true
    dossierPresent := true
    evidenceRefsPresent := true
    highRisk := true
    adversarialProbePresent := true
    reviewerCount := 3
    independenceGroupCount := 3
    independenceGraphAcyclic := true
    sharedEvidenceRiskRecorded := true
    falsificationAttempted := true
    abstentionPresent := true
    abstentionPreserved := true
    vetoPresent := true
    vetoPreserved := true
    priorVerdictReused := true
    evidenceUnchanged := true
    reuseGuardPresent := true
    defaultApprovalUsed := false
    dissentPresent := true
    dissentPreserved := true
    actionRequired := true
    requiredActionsPresent := true
    constraintsPresent := true
    residualPresent := true
    appealAvailable := true
    appealRequested := true
    appealRecorded := true
    supportChangeRequested := true
    evidenceOwnerHandoffPresent := true
    consumerAcknowledgmentPresent := true
    supportAssignmentRequested := false
    externalEffectRequested := false
    verdict := .revise }

def initialState : State :=
  { stage := .idle
    caseId := 71
    caseVersion := 4
    targetDigest := 101
    evidenceVersion := 9
    evidenceDigest := 201
    dossierDigest := 202
    panelDigest := 203
    policyDigest := 301
    consumerDigest := 401
    verdictVersion := 2
    lastEventDigest := 0
    panelAccepted := false
    verdict := .none
    receiptCount := 0
    supportAssignmentCount := 0
    externalEffectCount := 0 }

def requestEvent : Event := { kind := .requestReview, packet := canonicalPacket }
def requestedState : State := (applyEvent initialState requestEvent).1
def bindEvent : Event := { kind := .bindDossier, packet := { canonicalPacket with eventDigest := 2 } }
def dossierState : State := (applyEvent requestedState bindEvent).1
def panelEvent : Event := { kind := .runPanel, packet := { canonicalPacket with eventDigest := 3 } }
def panelState : State := (applyEvent dossierState panelEvent).1
def verdictEvent : Event := { kind := .issueVerdict, packet := { canonicalPacket with eventDigest := 4 } }
def verdictState : State := (applyEvent panelState verdictEvent).1
def acknowledgeEvent : Event := { kind := .acknowledgeVerdict, packet := { canonicalPacket with eventDigest := 5 } }
def acknowledgedState : State := (applyEvent verdictState acknowledgeEvent).1
def appealEvent : Event := { kind := .resolveAppeal, packet := { canonicalPacket with eventDigest := 6 } }
def finalState : State := (applyEvent acknowledgedState appealEvent).1

def noProbePanelEvent : Event :=
  { kind := .runPanel
    packet := { canonicalPacket with
      eventDigest := 30
      adversarialProbePresent := false } }
def sharedGroupPanelEvent : Event :=
  { kind := .runPanel
    packet := { canonicalPacket with
      eventDigest := 31
      independenceGroupCount := 2 } }
def defaultApprovalVerdictEvent : Event :=
  { kind := .issueVerdict
    packet := { canonicalPacket with
      eventDigest := 32
      defaultApprovalUsed := true } }
def erasedDissentVerdictEvent : Event :=
  { kind := .issueVerdict
    packet := { canonicalPacket with
      eventDigest := 33
      dissentPreserved := false } }
def changedEvidenceReuseEvent : Event :=
  { kind := .issueVerdict
    packet := { canonicalPacket with
      eventDigest := 34
      evidenceUnchanged := false } }
def missingActionVerdictEvent : Event :=
  { kind := .issueVerdict
    packet := { canonicalPacket with
      eventDigest := 35
      requiredActionsPresent := false } }
def missingOwnerHandoffEvent : Event :=
  { kind := .issueVerdict
    packet := { canonicalPacket with
      eventDigest := 36
      evidenceOwnerHandoffPresent := false } }
def missingAppealResolutionEvent : Event :=
  { kind := .resolveAppeal
    packet := { canonicalPacket with
      eventDigest := 37
      appealRecorded := false } }

theorem high_risk_without_probe_requests_adversarial_review :
    routeFor dossierState noProbePanelEvent = .requestAdversarialProbe := by rfl

theorem shared_independence_group_requests_graph_repair :
    routeFor dossierState sharedGroupPanelEvent = .requestIndependenceGraph := by rfl

theorem default_approval_is_rejected :
    routeFor panelState defaultApprovalVerdictEvent = .rejectDefaultApproval := by rfl

theorem unpreserved_dissent_blocks_verdict :
    routeFor panelState erasedDissentVerdictEvent = .preserveDissent := by rfl

theorem changed_evidence_blocks_prior_verdict_reuse :
    routeFor panelState changedEvidenceReuseEvent = .rejectChangedEvidenceReuse := by rfl

theorem action_verdict_requires_actions_and_constraints :
    routeFor panelState missingActionVerdictEvent = .requestActionsAndConstraints := by rfl

theorem support_change_requires_evidence_owner_handoff :
    routeFor panelState missingOwnerHandoffEvent = .handoffToEvidenceOwner := by rfl

theorem requested_appeal_requires_resolution_record :
    routeFor acknowledgedState missingAppealResolutionEvent = .requestAppealResolution := by rfl

theorem full_tribunal_lifecycle_reaches_appeal_resolution :
    finalState.stage = .appealResolved ∧
    finalState.receiptCount = 6 ∧
    finalState.panelAccepted = true ∧
    finalState.verdict = .revise ∧
    finalState.supportAssignmentCount = 0 ∧
    finalState.externalEffectCount = 0 := by
  native_decide

end AsiStackProofs.TribunalRefinement

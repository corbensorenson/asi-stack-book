import AsiStackProofs.EvidenceStates

namespace AsiStackProofs.EvidenceTransitionRefinement

inductive Stage where
  | requested | projectionsFrozen | evidenceBound | reviewed | decided | handedOff
deriving DecidableEq, Repr

inductive EventKind where
  | freezeProjections | bindEvidence | recordReview | decide | handOff | acknowledge
deriving DecidableEq, Repr

inductive Intent where
  | preserve | promote | narrow | downgrade | deprecate | refute
deriving DecidableEq, Repr

inductive Route where
  | rejectWrongStage | rejectAtomSubstitution | rejectProjectionSubstitution
  | rejectEventReplay | rejectAuthorityLeak | rejectStateCategorySubstitution
  | requestScope | requestAssumptions | requestNonClaims | requestDependencies
  | requestEvidenceRefs | requestEvidenceRoles | requestArtifactBindings
  | requestSourceGrounding | requestPrototypeInspection | requestSyntheticValidation
  | requestEmpiricalValidation | requestExternalLiterature
  | requestNegativeEvidence | requestDowngradeTrigger | requestSupersessionLineage
  | requestIndependentReview | requestProjectionAlignment | requestDissent
  | requestLimitations | requestResiduals | requestChangelog
  | requestLedgerHandoff | requestAcknowledgment
  | acceptProjectionFreeze | acceptEvidenceBinding | acceptReview
  | acceptDecision | acceptHandoff | acceptAcknowledgment
deriving DecidableEq, Repr

structure State where
  stage : Stage
  atomDigest : Nat
  propositionDigest : Nat
  obligationDigest : Nat
  predicateDigest : Nat
  currentState : SupportState
  lastEventDigest : Nat
deriving DecidableEq, Repr

structure Packet where
  atomDigest : Nat := 7101
  propositionDigest : Nat := 7102
  obligationDigest : Nat := 7103
  predicateDigest : Nat := 7104
  currentState : SupportState := .argument
  proposedState : SupportState := .syntheticTestBacked
  intent : Intent := .promote
  eventDigest : Nat := 111
  scope : Bool := true
  assumptions : Bool := true
  nonClaims : Bool := true
  dependencies : Bool := true
  evidenceRefs : Bool := true
  evidenceRoles : Bool := true
  artifactBindings : Bool := true
  sourceGrounding : Bool := true
  prototypeInspection : Bool := true
  syntheticValidation : Bool := true
  empiricalValidation : Bool := true
  externalLiterature : Bool := true
  negativeEvidence : Bool := true
  downgradeTrigger : Bool := true
  supersessionLineage : Bool := true
  independentReview : Bool := true
  projectionAlignment : Bool := true
  dissent : Bool := true
  limitations : Bool := true
  residuals : Bool := true
  changelog : Bool := true
  ledgerHandoff : Bool := true
  acknowledgment : Bool := true
  supportAssignmentRequested : Bool := false
  externalEffectRequested : Bool := false
  parentMovementRequested : Bool := false
  descendantMovementRequested : Bool := false
deriving DecidableEq, Repr

def expectedKind : Stage → EventKind
  | .requested => .freezeProjections
  | .projectionsFrozen => .bindEvidence
  | .evidenceBound => .recordReview
  | .reviewed => .decide
  | .decided => .handOff
  | .handedOff => .acknowledge

def stateCategoryMatches (p : Packet) : Bool :=
  match p.intent, p.proposedState with
  | .deprecate, .deprecated => true
  | .refute, .refuted => true
  | .deprecate, _ => false
  | .refute, _ => false
  | _, .deprecated => false
  | _, .refuted => false
  | _, _ => true

def evidenceForTarget (p : Packet) : Bool :=
  match p.proposedState with
  | .sourceDerived => p.sourceGrounding
  | .prototypeBacked => p.prototypeInspection
  | .syntheticTestBacked => p.syntheticValidation
  | .empiricalTestBacked => p.empiricalValidation
  | .externalLiteratureBacked => p.externalLiterature
  | .deprecated | .refuted => p.negativeEvidence
  | .unsupported | .argument => true

def adverseIntent : Intent → Bool
  | .narrow | .downgrade | .deprecate | .refute => true
  | _ => false

def route (s : State) (kind : EventKind) (p : Packet) : Route :=
  if kind != expectedKind s.stage then .rejectWrongStage
  else if p.atomDigest != s.atomDigest then .rejectAtomSubstitution
  else if p.propositionDigest != s.propositionDigest ||
      p.obligationDigest != s.obligationDigest ||
      p.predicateDigest != s.predicateDigest then .rejectProjectionSubstitution
  else if p.currentState != s.currentState then .rejectStateCategorySubstitution
  else if p.eventDigest = s.lastEventDigest then .rejectEventReplay
  else if p.supportAssignmentRequested || p.externalEffectRequested ||
      p.parentMovementRequested || p.descendantMovementRequested then .rejectAuthorityLeak
  else if !stateCategoryMatches p then .rejectStateCategorySubstitution
  else match s.stage with
  | .requested =>
      if !p.scope then .requestScope
      else if !p.assumptions then .requestAssumptions
      else if !p.nonClaims then .requestNonClaims
      else if !p.dependencies then .requestDependencies
      else .acceptProjectionFreeze
  | .projectionsFrozen =>
      if !p.evidenceRefs then .requestEvidenceRefs
      else if !p.evidenceRoles then .requestEvidenceRoles
      else if !p.artifactBindings then .requestArtifactBindings
      else if !evidenceForTarget p then
        match p.proposedState with
        | .sourceDerived => .requestSourceGrounding
        | .prototypeBacked => .requestPrototypeInspection
        | .syntheticTestBacked => .requestSyntheticValidation
        | .empiricalTestBacked => .requestEmpiricalValidation
        | .externalLiteratureBacked => .requestExternalLiterature
        | .deprecated | .refuted => .requestNegativeEvidence
        | .unsupported | .argument => .requestEvidenceRefs
      else if adverseIntent p.intent && !p.negativeEvidence then .requestNegativeEvidence
      else if adverseIntent p.intent && !p.downgradeTrigger then .requestDowngradeTrigger
      else if adverseIntent p.intent && !p.supersessionLineage then .requestSupersessionLineage
      else .acceptEvidenceBinding
  | .evidenceBound =>
      if !p.independentReview then .requestIndependentReview
      else if !p.projectionAlignment then .requestProjectionAlignment
      else if !p.dissent then .requestDissent
      else .acceptReview
  | .reviewed =>
      if !p.limitations then .requestLimitations
      else if !p.residuals then .requestResiduals
      else if !p.changelog then .requestChangelog
      else .acceptDecision
  | .decided =>
      if !p.ledgerHandoff then .requestLedgerHandoff
      else .acceptHandoff
  | .handedOff =>
      if !p.acknowledgment then .requestAcknowledgment
      else .acceptAcknowledgment

def accepted : Route → Bool
  | .acceptProjectionFreeze | .acceptEvidenceBinding | .acceptReview
  | .acceptDecision | .acceptHandoff | .acceptAcknowledgment => true
  | _ => false

def completeState (stage : Stage) : State where
  stage := stage
  atomDigest := 7101
  propositionDigest := 7102
  obligationDigest := 7103
  predicateDigest := 7104
  currentState := .argument
  lastEventDigest := 0

def completePacket : Packet := {}

theorem authority_or_inheritance_request_never_accepts
    (s : State) (kind : EventKind) (p : Packet)
    (h : p.supportAssignmentRequested || p.externalEffectRequested ||
        p.parentMovementRequested || p.descendantMovementRequested = true) :
    accepted (route s kind p) = false := by
  by_cases h₁ : kind != expectedKind s.stage
  · simp [route, h₁, accepted]
  by_cases h₂ : p.atomDigest != s.atomDigest
  · simp [route, h₁, h₂, accepted]
  by_cases h₃ : p.propositionDigest != s.propositionDigest ||
      p.obligationDigest != s.obligationDigest ||
      p.predicateDigest != s.predicateDigest
  · simp [route, h₁, h₂, h₃, accepted]
  by_cases h₄ : p.currentState != s.currentState
  · simp [route, h₁, h₂, h₃, h₄, accepted]
  by_cases h₅ : p.eventDigest = s.lastEventDigest
  · simp [route, h₁, h₂, h₃, h₄, h₅, accepted]
  simp_all [route, accepted]

theorem projection_substitution_never_accepts
    (s : State) (kind : EventKind) (p : Packet)
    (h : p.propositionDigest != s.propositionDigest ||
        p.obligationDigest != s.obligationDigest ||
        p.predicateDigest != s.predicateDigest) :
    accepted (route s kind p) = false := by
  by_cases h₁ : kind != expectedKind s.stage
  · simp [route, h₁, accepted]
  by_cases h₂ : p.atomDigest != s.atomDigest
  · simp [route, h₁, h₂, accepted]
  simp [route, h₁, h₂, h, accepted]

theorem target_evidence_is_state_specific :
    evidenceForTarget { completePacket with proposedState := .sourceDerived, sourceGrounding := false, syntheticValidation := true } = false ∧
    evidenceForTarget { completePacket with proposedState := .syntheticTestBacked, sourceGrounding := true, syntheticValidation := false } = false ∧
    evidenceForTarget { completePacket with proposedState := .externalLiteratureBacked, empiricalValidation := true, externalLiterature := false } = false := by native_decide

theorem adverse_transition_without_negative_evidence_cannot_bind :
    route (completeState .projectionsFrozen) .bindEvidence
      { completePacket with intent := .downgrade, proposedState := .argument, negativeEvidence := false } =
      .requestNegativeEvidence := by native_decide

theorem terminal_label_requires_matching_intent :
    route (completeState .requested) .freezeProjections
      { completePacket with intent := .promote, proposedState := .refuted } =
      .rejectStateCategorySubstitution := by native_decide

theorem complete_transition_reaches_bounded_handoff :
    route (completeState .requested) .freezeProjections completePacket = .acceptProjectionFreeze ∧
    route (completeState .projectionsFrozen) .bindEvidence completePacket = .acceptEvidenceBinding ∧
    route (completeState .evidenceBound) .recordReview completePacket = .acceptReview ∧
    route (completeState .reviewed) .decide completePacket = .acceptDecision ∧
    route (completeState .decided) .handOff completePacket = .acceptHandoff ∧
    route (completeState .handedOff) .acknowledge completePacket = .acceptAcknowledgment ∧
    completePacket.supportAssignmentRequested = false ∧
    completePacket.externalEffectRequested = false ∧
    completePacket.parentMovementRequested = false ∧
    completePacket.descendantMovementRequested = false := by native_decide

end AsiStackProofs.EvidenceTransitionRefinement

namespace AsiStackProofs

inductive SupportState where
  | unsupported
  | argument
  | sourceDerived
  | prototypeBacked
  | syntheticTestBacked
  | empiricalTestBacked
  | externalLiteratureBacked
  | deprecated
  | refuted
deriving DecidableEq, Repr

inductive TransitionEffect where
  | noChange
  | upward
  | downward
  | deprecated
  | refuted
deriving DecidableEq, Repr

structure EvidenceBundle where
  sourceNote : Prop
  prototypeInspection : Prop
  syntheticTestRun : Prop
  empiricalTestRun : Prop
  externalLiterature : Prop

def rank : SupportState -> Nat
  | .unsupported => 0
  | .argument => 1
  | .sourceDerived => 2
  | .prototypeBacked => 3
  | .syntheticTestBacked => 4
  | .empiricalTestBacked => 5
  | .externalLiteratureBacked => 5
  | .deprecated => 0
  | .refuted => 0

def RequiredEvidence : SupportState -> EvidenceBundle -> Prop
  | .unsupported, _ => True
  | .argument, _ => True
  | .sourceDerived, bundle => bundle.sourceNote
  | .prototypeBacked, bundle => bundle.prototypeInspection
  | .syntheticTestBacked, bundle => bundle.syntheticTestRun
  | .empiricalTestBacked, bundle => bundle.empiricalTestRun
  | .externalLiteratureBacked, bundle => bundle.externalLiterature
  | .deprecated, _ => False
  | .refuted, _ => False

def PromotionAllowed (bundle : EvidenceBundle) (fromState toState : SupportState) : Prop :=
  And (rank fromState < rank toState) (RequiredEvidence toState bundle)

def TerminalState : SupportState -> Prop
  | .deprecated => True
  | .refuted => True
  | _ => False

def TerminalEffectFor : SupportState -> TransitionEffect -> Prop
  | .deprecated, .deprecated => True
  | .refuted, .refuted => True
  | _, _ => False

structure EvidenceTransitionRecord where
  oldState : SupportState
  newState : SupportState
  effect : TransitionEffect
  acceptedReview : Prop
  negativeEvidence : Prop
  downgradeTrigger : Prop

def AcceptedTerminalTransition (record : EvidenceTransitionRecord) : Prop :=
  And (TerminalEffectFor record.newState record.effect)
    (And record.acceptedReview record.negativeEvidence)

def AcceptedDowngradeTransition (record : EvidenceTransitionRecord) : Prop :=
  And (record.effect = TransitionEffect.downward)
    (And (rank record.newState < rank record.oldState)
      (And record.negativeEvidence record.downgradeTrigger))

theorem support_state_transition_requires_evidence
    {bundle : EvidenceBundle} {fromState toState : SupportState} :
    PromotionAllowed bundle fromState toState -> RequiredEvidence toState bundle := by
  intro allowed
  exact allowed.2

theorem missing_required_evidence_blocks_promotion
    {bundle : EvidenceBundle} {fromState toState : SupportState} :
    Not (RequiredEvidence toState bundle) -> Not (PromotionAllowed bundle fromState toState) := by
  intro missing allowed
  exact missing allowed.2

theorem no_self_promotion (bundle : EvidenceBundle) (state : SupportState) :
    Not (PromotionAllowed bundle state state) := by
  intro allowed
  exact Nat.lt_irrefl (rank state) allowed.1

theorem unsupported_can_promote_to_argument (bundle : EvidenceBundle) :
    PromotionAllowed bundle SupportState.unsupported SupportState.argument := by
  constructor
  · decide
  · trivial

theorem terminal_state_cannot_be_promotion_target
    {bundle : EvidenceBundle} {fromState toState : SupportState} :
    TerminalState toState -> Not (PromotionAllowed bundle fromState toState) := by
  intro terminal allowed
  cases toState <;> simp [TerminalState] at terminal
  · cases fromState <;> simp [PromotionAllowed, rank] at allowed
  · cases fromState <;> simp [PromotionAllowed, rank] at allowed

theorem accepted_terminal_transition_requires_negative_evidence
    {record : EvidenceTransitionRecord} :
    AcceptedTerminalTransition record -> record.negativeEvidence := by
  intro accepted
  exact accepted.2.2

theorem accepted_downgrade_transition_requires_negative_evidence_and_trigger
    {record : EvidenceTransitionRecord} :
    AcceptedDowngradeTransition record -> And record.negativeEvidence record.downgradeTrigger := by
  intro accepted
  exact accepted.2.2

theorem terminal_effect_for_implies_terminal_state
    {state : SupportState} {effect : TransitionEffect} :
    TerminalEffectFor state effect -> TerminalState state := by
  intro terminalEffect
  cases state <;> cases effect <;> simp [TerminalEffectFor, TerminalState] at terminalEffect ⊢

theorem accepted_terminal_transition_blocks_promotion_to_new_state
    {bundle : EvidenceBundle} {record : EvidenceTransitionRecord} :
    AcceptedTerminalTransition record -> Not (PromotionAllowed bundle record.oldState record.newState) := by
  intro accepted
  exact terminal_state_cannot_be_promotion_target (terminal_effect_for_implies_terminal_state accepted.1)

inductive EvidenceTransitionRoute where
  | allowNoChange
  | rejectMissingClaimRecord
  | requestScopeBoundary
  | requestSupportStateEffect
  | blockSupportStateEffectMismatch
  | requestAcceptedReview
  | requestRequiredEvidence
  | requestNegativeEvidence
  | requestDowngradeTrigger
  | requestTerminalEffect
  | requestChangelogRef
  | preserveNonClaimBoundary
  | acceptTransition
deriving DecidableEq, Repr

structure EvidenceTransitionReview where
  transitionRequested : Bool
  claimRecordPresent : Bool
  scopeBoundaryPresent : Bool
  supportStateEffectDeclared : Bool
  supportStateEffectMatchesRecord : Bool
  oldState : SupportState
  newState : SupportState
  effect : TransitionEffect
  acceptedReviewPresent : Bool
  sourceNotePresent : Bool
  prototypeInspectionPresent : Bool
  syntheticTestRunPresent : Bool
  empiricalTestRunPresent : Bool
  externalLiteraturePresent : Bool
  negativeEvidenceRefsPresent : Bool
  downgradeTriggerPresent : Bool
  changelogRefPresent : Bool
  nonClaimBoundaryPresent : Bool
deriving DecidableEq, Repr

def EvidenceAvailableFor :
    SupportState -> EvidenceTransitionReview -> Bool
  | .unsupported, _ => true
  | .argument, _ => true
  | .sourceDerived, review => review.sourceNotePresent
  | .prototypeBacked, review => review.prototypeInspectionPresent
  | .syntheticTestBacked, review => review.syntheticTestRunPresent
  | .empiricalTestBacked, review => review.empiricalTestRunPresent
  | .externalLiteratureBacked, review => review.externalLiteraturePresent
  | .deprecated, _ => false
  | .refuted, _ => false

def TerminalStateBool : SupportState -> Bool
  | .deprecated => true
  | .refuted => true
  | _ => false

def TerminalEffectMatches :
    SupportState -> TransitionEffect -> Bool
  | .deprecated, .deprecated => true
  | .refuted, .refuted => true
  | _, _ => false

def EvidenceTransitionRouteFor
    (review : EvidenceTransitionReview) :
    EvidenceTransitionRoute :=
  if review.transitionRequested = false then
    EvidenceTransitionRoute.allowNoChange
  else if review.claimRecordPresent = false then
    EvidenceTransitionRoute.rejectMissingClaimRecord
  else if review.scopeBoundaryPresent = false then
    EvidenceTransitionRoute.requestScopeBoundary
  else if review.supportStateEffectDeclared = false then
    EvidenceTransitionRoute.requestSupportStateEffect
  else if review.supportStateEffectMatchesRecord = false then
    EvidenceTransitionRoute.blockSupportStateEffectMismatch
  else if TerminalStateBool review.newState = true then
    if TerminalEffectMatches review.newState review.effect = false then
      EvidenceTransitionRoute.requestTerminalEffect
    else if review.negativeEvidenceRefsPresent = false then
      EvidenceTransitionRoute.requestNegativeEvidence
    else if review.acceptedReviewPresent = false then
      EvidenceTransitionRoute.requestAcceptedReview
    else if review.changelogRefPresent = false then
      EvidenceTransitionRoute.requestChangelogRef
    else if review.nonClaimBoundaryPresent = false then
      EvidenceTransitionRoute.preserveNonClaimBoundary
    else
      EvidenceTransitionRoute.acceptTransition
  else if review.effect = TransitionEffect.upward then
    if review.acceptedReviewPresent = false then
      EvidenceTransitionRoute.requestAcceptedReview
    else if EvidenceAvailableFor review.newState review = false then
      EvidenceTransitionRoute.requestRequiredEvidence
    else if review.nonClaimBoundaryPresent = false then
      EvidenceTransitionRoute.preserveNonClaimBoundary
    else
      EvidenceTransitionRoute.acceptTransition
  else if review.effect = TransitionEffect.downward then
    if review.negativeEvidenceRefsPresent = false then
      EvidenceTransitionRoute.requestNegativeEvidence
    else if review.downgradeTriggerPresent = false then
      EvidenceTransitionRoute.requestDowngradeTrigger
    else if review.changelogRefPresent = false then
      EvidenceTransitionRoute.requestChangelogRef
    else if review.nonClaimBoundaryPresent = false then
      EvidenceTransitionRoute.preserveNonClaimBoundary
    else
      EvidenceTransitionRoute.acceptTransition
  else if review.nonClaimBoundaryPresent = false then
    EvidenceTransitionRoute.preserveNonClaimBoundary
  else
    EvidenceTransitionRoute.acceptTransition

def completeEvidenceTransitionReview : EvidenceTransitionReview where
  transitionRequested := true
  claimRecordPresent := true
  scopeBoundaryPresent := true
  supportStateEffectDeclared := true
  supportStateEffectMatchesRecord := true
  oldState := SupportState.argument
  newState := SupportState.syntheticTestBacked
  effect := TransitionEffect.upward
  acceptedReviewPresent := true
  sourceNotePresent := true
  prototypeInspectionPresent := true
  syntheticTestRunPresent := true
  empiricalTestRunPresent := true
  externalLiteraturePresent := true
  negativeEvidenceRefsPresent := true
  downgradeTriggerPresent := true
  changelogRefPresent := true
  nonClaimBoundaryPresent := true

theorem no_requested_transition_allows_no_change :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          transitionRequested := false } =
      EvidenceTransitionRoute.allowNoChange := by
  simp [EvidenceTransitionRouteFor]

theorem missing_claim_record_rejects_evidence_transition :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          claimRecordPresent := false } =
      EvidenceTransitionRoute.rejectMissingClaimRecord := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview]

theorem missing_scope_boundary_requests_scope_boundary :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          scopeBoundaryPresent := false } =
      EvidenceTransitionRoute.requestScopeBoundary := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview]

theorem missing_support_state_effect_requests_effect_record :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          supportStateEffectDeclared := false } =
      EvidenceTransitionRoute.requestSupportStateEffect := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview]

theorem mismatched_support_state_effect_blocks_transition :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          supportStateEffectMatchesRecord := false } =
      EvidenceTransitionRoute.blockSupportStateEffectMismatch := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview]

theorem upward_transition_without_review_requests_review :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          acceptedReviewPresent := false } =
      EvidenceTransitionRoute.requestAcceptedReview := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    TerminalStateBool]

theorem source_derived_without_source_note_requests_required_evidence :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          newState := SupportState.sourceDerived
          sourceNotePresent := false } =
      EvidenceTransitionRoute.requestRequiredEvidence := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    EvidenceAvailableFor, TerminalStateBool]

theorem synthetic_test_backed_without_test_run_requests_required_evidence :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          syntheticTestRunPresent := false } =
      EvidenceTransitionRoute.requestRequiredEvidence := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    EvidenceAvailableFor, TerminalStateBool]

theorem downward_transition_without_negative_evidence_requests_negative_evidence :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          effect := TransitionEffect.downward
          oldState := SupportState.syntheticTestBacked
          newState := SupportState.argument
          negativeEvidenceRefsPresent := false } =
      EvidenceTransitionRoute.requestNegativeEvidence := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    TerminalStateBool]

theorem downward_transition_without_trigger_requests_downgrade_trigger :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          effect := TransitionEffect.downward
          oldState := SupportState.syntheticTestBacked
          newState := SupportState.argument
          downgradeTriggerPresent := false } =
      EvidenceTransitionRoute.requestDowngradeTrigger := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    TerminalStateBool]

theorem terminal_refutation_with_wrong_effect_requests_terminal_effect :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          newState := SupportState.refuted
          effect := TransitionEffect.noChange } =
      EvidenceTransitionRoute.requestTerminalEffect := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    TerminalStateBool, TerminalEffectMatches]

theorem terminal_refutation_without_negative_evidence_requests_negative_evidence :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          newState := SupportState.refuted
          effect := TransitionEffect.refuted
          negativeEvidenceRefsPresent := false } =
      EvidenceTransitionRoute.requestNegativeEvidence := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    TerminalStateBool, TerminalEffectMatches]

theorem terminal_refutation_without_changelog_requests_changelog :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          newState := SupportState.refuted
          effect := TransitionEffect.refuted
          changelogRefPresent := false } =
      EvidenceTransitionRoute.requestChangelogRef := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    TerminalStateBool, TerminalEffectMatches]

theorem transition_without_nonclaims_preserves_nonclaim_boundary :
    EvidenceTransitionRouteFor
        { completeEvidenceTransitionReview with
          nonClaimBoundaryPresent := false } =
      EvidenceTransitionRoute.preserveNonClaimBoundary := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    EvidenceAvailableFor, TerminalStateBool]

theorem complete_synthetic_test_backed_transition_accepts :
    EvidenceTransitionRouteFor completeEvidenceTransitionReview =
      EvidenceTransitionRoute.acceptTransition := by
  simp [EvidenceTransitionRouteFor, completeEvidenceTransitionReview,
    EvidenceAvailableFor, TerminalStateBool]

end AsiStackProofs

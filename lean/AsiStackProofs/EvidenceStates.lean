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

end AsiStackProofs

namespace AsiStackProofs

inductive SupportState where
  | unsupported
  | argument
  | sourceDerived
  | prototypeBacked
  | syntheticTestBacked
  | empiricalTestBacked
  | externalLiteratureBacked
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

def RequiredEvidence : SupportState -> EvidenceBundle -> Prop
  | .unsupported, _ => True
  | .argument, _ => True
  | .sourceDerived, bundle => bundle.sourceNote
  | .prototypeBacked, bundle => bundle.prototypeInspection
  | .syntheticTestBacked, bundle => bundle.syntheticTestRun
  | .empiricalTestBacked, bundle => bundle.empiricalTestRun
  | .externalLiteratureBacked, bundle => bundle.externalLiterature

def PromotionAllowed (bundle : EvidenceBundle) (fromState toState : SupportState) : Prop :=
  And (rank fromState < rank toState) (RequiredEvidence toState bundle)

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

end AsiStackProofs

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

def rank : SupportState -> Nat
  | .unsupported => 0
  | .argument => 1
  | .sourceDerived => 2
  | .prototypeBacked => 3
  | .syntheticTestBacked => 4
  | .empiricalTestBacked => 5
  | .externalLiteratureBacked => 5

def CanPromote (fromState toState : SupportState) : Prop :=
  rank fromState < rank toState

theorem no_self_promotion (state : SupportState) : ¬ CanPromote state state := by
  unfold CanPromote
  exact Nat.lt_irrefl (rank state)

theorem unsupported_can_promote_to_argument :
    CanPromote SupportState.unsupported SupportState.argument := by
  unfold CanPromote rank
  decide

end AsiStackProofs

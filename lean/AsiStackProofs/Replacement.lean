namespace AsiStackProofs.Replacement

structure ReplacementCommit where
  qualificationEvidence : Bool
  rollbackMetadata : Bool
  regressionPassed : Bool
deriving DecidableEq, Repr

def CommitPrerequisitesPresent (commit : ReplacementCommit) : Prop :=
  commit.qualificationEvidence = true ∧
    commit.rollbackMetadata = true

def PromotionAllowed (commit : ReplacementCommit) : Prop :=
  CommitPrerequisitesPresent commit ∧
    commit.regressionPassed = true

theorem replacement_commit_requires_evidence_and_rollback
    {commit : ReplacementCommit} :
    PromotionAllowed commit ->
    commit.qualificationEvidence = true ∧ commit.rollbackMetadata = true := by
  intro allowed
  exact allowed.1

theorem failed_regression_blocks_replacement_promotion
    {commit : ReplacementCommit} :
    commit.regressionPassed = false ->
    ¬ PromotionAllowed commit := by
  intro failed promoted
  unfold PromotionAllowed at promoted
  rw [failed] at promoted
  cases promoted.2

end AsiStackProofs.Replacement

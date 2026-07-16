namespace AsiStackProofs.FastGeneration

/- Frozen finite countermodels retained from the activation baseline. The
reachable model lives in FastGenerationRefinement. -/

structure AccelerationAccountingRecord where
  proposedOutputRecorded : Bool
  acceptedOutputRecorded : Bool
  verifierCostRecorded : Bool
  fallbackCostRecorded : Bool
  taskSuccessRecorded : Bool
  baselineRecorded : Bool
  promotionCandidate : Bool
deriving DecidableEq, Repr

def AccelerationAccountingComplete (record : AccelerationAccountingRecord) : Prop :=
  record.proposedOutputRecorded = true ∧ record.acceptedOutputRecorded = true ∧
  record.verifierCostRecorded = true ∧ record.fallbackCostRecorded = true ∧
  record.taskSuccessRecorded = true ∧ record.baselineRecorded = true

def AccelerationPromotionAccountingValid (record : AccelerationAccountingRecord) : Prop :=
  record.promotionCandidate = true -> AccelerationAccountingComplete record

theorem promotion_candidate_missing_accepted_output_or_verifier_cost_rejected
    {record : AccelerationAccountingRecord} :
    record.promotionCandidate = true ->
    (record.acceptedOutputRecorded = false ∨ record.verifierCostRecorded = false) ->
    ¬ AccelerationPromotionAccountingValid record := by
  intro promoted missing valid
  have complete := valid promoted
  rcases complete with ⟨_, accepted, verifier, _⟩
  rcases missing with missing | missing
  · rw [missing] at accepted
    contradiction
  · rw [missing] at verifier
    contradiction

structure FailedAcceptanceRecord where
  acceleratedDraftProduced : Bool
  acceptanceFailed : Bool
  fallbackRouted : Bool
  residualRecorded : Bool
  promotionCandidate : Bool
deriving DecidableEq, Repr

def FailedAcceptanceHandled (record : FailedAcceptanceRecord) : Prop :=
  record.acceleratedDraftProduced = true -> record.acceptanceFailed = true ->
  record.fallbackRouted = true ∧ record.residualRecorded = true ∧
  record.promotionCandidate = false

theorem failed_acceptance_without_fallback_or_residual_rejected
    {record : FailedAcceptanceRecord} :
    record.acceleratedDraftProduced = true -> record.acceptanceFailed = true ->
    (record.fallbackRouted = false ∨ record.residualRecorded = false ∨
      record.promotionCandidate = true) -> ¬ FailedAcceptanceHandled record := by
  intro produced failed missing valid
  rcases valid produced failed with ⟨fallback, residual, blocked⟩
  rcases missing with missing | missing | promoted
  · rw [missing] at fallback
    contradiction
  · rw [missing] at residual
    contradiction
  · rw [promoted] at blocked
    contradiction

inductive GenerationRiskTier where | low | medium | high | critical
deriving DecidableEq, Repr

def HighRiskGeneration : GenerationRiskTier -> Prop
  | .high | .critical => True
  | _ => False

structure HighRiskFastModeRecord where
  riskTier : GenerationRiskTier
  fastModeSelected : Bool
  verifierRecorded : Bool
  riskOverrideRecorded : Bool
  slowerFallbackAllowed : Bool
deriving DecidableEq, Repr

def HighRiskFastModeReviewValid (record : HighRiskFastModeRecord) : Prop :=
  HighRiskGeneration record.riskTier -> record.fastModeSelected = true ->
  record.verifierRecorded = true ∧ record.riskOverrideRecorded = true ∧
  record.slowerFallbackAllowed = true

theorem high_risk_fast_mode_without_verifier_or_override_rejected
    {record : HighRiskFastModeRecord} :
    HighRiskGeneration record.riskTier -> record.fastModeSelected = true ->
    (record.verifierRecorded = false ∨ record.riskOverrideRecorded = false ∨
      record.slowerFallbackAllowed = false) -> ¬ HighRiskFastModeReviewValid record := by
  intro highRisk selected missing valid
  rcases valid highRisk selected with ⟨verifier, override, fallback⟩
  rcases missing with missing | missing | missing
  · rw [missing] at verifier
    contradiction
  · rw [missing] at override
    contradiction
  · rw [missing] at fallback
    contradiction

end AsiStackProofs.FastGeneration

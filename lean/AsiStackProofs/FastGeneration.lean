namespace AsiStackProofs.FastGeneration

structure GenerationRouteRecord where
  generationModeRecorded : Bool
  verifierRecorded : Bool
  acceptancePredicateRecorded : Bool
  riskTierRecorded : Bool
  fallbackRecorded : Bool
  promotionCandidate : Bool
deriving DecidableEq, Repr

def RoutePromotionFieldsComplete (record : GenerationRouteRecord) : Prop :=
  record.generationModeRecorded = true ∧
    record.verifierRecorded = true ∧
    record.acceptancePredicateRecorded = true ∧
    record.riskTierRecorded = true ∧
    record.fallbackRecorded = true

def FastGenerationRoutePromotionValid (record : GenerationRouteRecord) : Prop :=
  record.promotionCandidate = true -> RoutePromotionFieldsComplete record

theorem promoted_fast_generation_route_records_required_fields
    {record : GenerationRouteRecord} :
    FastGenerationRoutePromotionValid record ->
    record.promotionCandidate = true ->
    record.generationModeRecorded = true ∧
      record.verifierRecorded = true ∧
      record.acceptancePredicateRecorded = true ∧
      record.riskTierRecorded = true ∧
      record.fallbackRecorded = true := by
  intro valid promoted
  exact valid promoted

structure SpeedPromotionRecord where
  rawTokensPerSecondClaimed : Bool
  acceptedOrVerifiedTokenEvidencePresent : Bool
  taskSuccessEvidencePresent : Bool
  baselinePresent : Bool
  promoted : Bool
deriving DecidableEq, Repr

def MissingVerifiedSpeedEvidence (record : SpeedPromotionRecord) : Prop :=
  record.acceptedOrVerifiedTokenEvidencePresent = false ∨
    record.taskSuccessEvidencePresent = false ∨
    record.baselinePresent = false

def RawSpeedPromotionValid (record : SpeedPromotionRecord) : Prop :=
  record.rawTokensPerSecondClaimed = true ->
    MissingVerifiedSpeedEvidence record ->
    record.promoted = false

theorem raw_tokens_per_second_cannot_promote_without_verified_evidence
    {record : SpeedPromotionRecord} :
    RawSpeedPromotionValid record ->
    record.rawTokensPerSecondClaimed = true ->
    MissingVerifiedSpeedEvidence record ->
    record.promoted = false := by
  intro valid rawClaim missingEvidence
  exact valid rawClaim missingEvidence

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
  record.proposedOutputRecorded = true ∧
    record.acceptedOutputRecorded = true ∧
      record.verifierCostRecorded = true ∧
        record.fallbackCostRecorded = true ∧
          record.taskSuccessRecorded = true ∧
            record.baselineRecorded = true

def AccelerationPromotionAccountingValid
    (record : AccelerationAccountingRecord) : Prop :=
  record.promotionCandidate = true -> AccelerationAccountingComplete record

theorem promoted_acceleration_records_accepted_output_and_costs
    {record : AccelerationAccountingRecord} :
    AccelerationPromotionAccountingValid record ->
    record.promotionCandidate = true ->
    record.proposedOutputRecorded = true ∧
      record.acceptedOutputRecorded = true ∧
        record.verifierCostRecorded = true ∧
          record.fallbackCostRecorded = true ∧
            record.taskSuccessRecorded = true ∧
              record.baselineRecorded = true := by
  intro valid promoted
  exact valid promoted

theorem promotion_candidate_missing_accepted_output_or_verifier_cost_rejected
    {record : AccelerationAccountingRecord} :
    record.promotionCandidate = true ->
    (record.acceptedOutputRecorded = false ∨ record.verifierCostRecorded = false) ->
    ¬ AccelerationPromotionAccountingValid record := by
  intro promoted missing valid
  unfold AccelerationPromotionAccountingValid at valid
  unfold AccelerationAccountingComplete at valid
  have complete := valid promoted
  cases complete with
  | intro _ acceptedAndRest =>
      cases acceptedAndRest with
      | intro acceptedPresent verifierAndRest =>
          cases verifierAndRest with
          | intro verifierPresent _ =>
              cases missing with
              | inl acceptedMissing =>
                  rw [acceptedMissing] at acceptedPresent
                  contradiction
              | inr verifierMissing =>
                  rw [verifierMissing] at verifierPresent
                  contradiction

structure FailedAcceptanceRecord where
  acceleratedDraftProduced : Bool
  acceptanceFailed : Bool
  fallbackRouted : Bool
  residualRecorded : Bool
  promotionCandidate : Bool
deriving DecidableEq, Repr

def FailedAcceptanceHandled (record : FailedAcceptanceRecord) : Prop :=
  record.acceleratedDraftProduced = true ->
    record.acceptanceFailed = true ->
      record.fallbackRouted = true ∧
        record.residualRecorded = true ∧
          record.promotionCandidate = false

theorem failed_acceptance_routes_fallback_records_residual_and_blocks_promotion
    {record : FailedAcceptanceRecord} :
    FailedAcceptanceHandled record ->
    record.acceleratedDraftProduced = true ->
    record.acceptanceFailed = true ->
    record.fallbackRouted = true ∧
      record.residualRecorded = true ∧
        record.promotionCandidate = false := by
  intro valid produced failed
  exact valid produced failed

theorem failed_acceptance_without_fallback_or_residual_rejected
    {record : FailedAcceptanceRecord} :
    record.acceleratedDraftProduced = true ->
    record.acceptanceFailed = true ->
    (record.fallbackRouted = false ∨ record.residualRecorded = false ∨
      record.promotionCandidate = true) ->
    ¬ FailedAcceptanceHandled record := by
  intro produced failed missing valid
  unfold FailedAcceptanceHandled at valid
  have handled := valid produced failed
  cases handled with
  | intro fallbackPresent residualAndPromotion =>
      cases residualAndPromotion with
      | intro residualPresent promotionBlocked =>
          cases missing with
          | inl fallbackMissing =>
              rw [fallbackMissing] at fallbackPresent
              contradiction
          | inr residualOrPromotion =>
              cases residualOrPromotion with
              | inl residualMissing =>
                  rw [residualMissing] at residualPresent
                  contradiction
              | inr promoted =>
                  rw [promoted] at promotionBlocked
                  contradiction

inductive GenerationRiskTier where
  | low
  | medium
  | high
  | critical
deriving DecidableEq, Repr

def HighRiskGeneration : GenerationRiskTier -> Prop
  | .high => True
  | .critical => True
  | _ => False

structure HighRiskFastModeRecord where
  riskTier : GenerationRiskTier
  fastModeSelected : Bool
  verifierRecorded : Bool
  riskOverrideRecorded : Bool
  slowerFallbackAllowed : Bool
deriving DecidableEq, Repr

def HighRiskFastModeReviewValid (record : HighRiskFastModeRecord) : Prop :=
  HighRiskGeneration record.riskTier ->
    record.fastModeSelected = true ->
      record.verifierRecorded = true ∧
        record.riskOverrideRecorded = true ∧
          record.slowerFallbackAllowed = true

theorem high_risk_fast_mode_records_verifier_override_and_fallback
    {record : HighRiskFastModeRecord} :
    HighRiskFastModeReviewValid record ->
    HighRiskGeneration record.riskTier ->
    record.fastModeSelected = true ->
    record.verifierRecorded = true ∧
      record.riskOverrideRecorded = true ∧
        record.slowerFallbackAllowed = true := by
  intro valid highRisk selected
  exact valid highRisk selected

theorem high_risk_fast_mode_without_verifier_or_override_rejected
    {record : HighRiskFastModeRecord} :
    HighRiskGeneration record.riskTier ->
    record.fastModeSelected = true ->
    (record.verifierRecorded = false ∨ record.riskOverrideRecorded = false ∨
      record.slowerFallbackAllowed = false) ->
    ¬ HighRiskFastModeReviewValid record := by
  intro highRisk selected missing valid
  unfold HighRiskFastModeReviewValid at valid
  have complete := valid highRisk selected
  cases complete with
  | intro verifierPresent overrideAndFallback =>
      cases overrideAndFallback with
      | intro overridePresent fallbackPresent =>
          cases missing with
          | inl verifierMissing =>
              rw [verifierMissing] at verifierPresent
              contradiction
          | inr overrideOrFallback =>
              cases overrideOrFallback with
              | inl overrideMissing =>
                  rw [overrideMissing] at overridePresent
                  contradiction
              | inr fallbackMissing =>
                  rw [fallbackMissing] at fallbackPresent
                  contradiction

end AsiStackProofs.FastGeneration

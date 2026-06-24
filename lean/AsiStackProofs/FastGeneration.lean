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

end AsiStackProofs.FastGeneration

namespace AsiStackProofs.StackBoundaries

structure Layer where
  hasExternalActionAuthority : Bool
deriving DecidableEq, Repr

structure Handoff where
  authorized : Bool
deriving DecidableEq, Repr

inductive LayerOutput where
  | internalArtifact
  | externalAction (handoff : Handoff)
deriving DecidableEq, Repr

def ExternalActionAllowed (layer : Layer) : LayerOutput -> Prop
  | .internalArtifact => True
  | .externalAction handoff =>
      layer.hasExternalActionAuthority = true ∨ handoff.authorized = true

theorem layer_without_external_authority_requires_authorized_handoff
    {layer : Layer} {handoff : Handoff} :
    layer.hasExternalActionAuthority = false ->
    ExternalActionAllowed layer (.externalAction handoff) ->
    handoff.authorized = true := by
  intro noAuthority allowed
  cases allowed with
  | inl hasAuthority =>
      rw [noAuthority] at hasAuthority
      contradiction
  | inr authorized =>
      exact authorized

structure StackTraceStep where
  layer : Layer
  output : LayerOutput
deriving DecidableEq, Repr

def StackTraceValid (trace : List StackTraceStep) : Prop :=
  ∀ step, step ∈ trace -> ExternalActionAllowed step.layer step.output

theorem valid_stack_trace_rejects_unauthorized_external_handoff
    {trace : List StackTraceStep} {layer : Layer} {handoff : Handoff} :
    ({ layer := layer, output := .externalAction handoff } : StackTraceStep) ∈ trace ->
    layer.hasExternalActionAuthority = false ->
    handoff.authorized = false ->
    ¬ StackTraceValid trace := by
  intro present noAuthority unauthorized validTrace
  unfold StackTraceValid at validTrace
  have allowed :=
    validTrace ({ layer := layer, output := .externalAction handoff } : StackTraceStep) present
  have authorized :=
    layer_without_external_authority_requires_authorized_handoff noAuthority allowed
  rw [unauthorized] at authorized
  contradiction

inductive AuthorityLevel where
  | none
  | read
  | write
  | execute
  | admin
deriving DecidableEq, Repr

def AuthorityLevel.rank : AuthorityLevel -> Nat
  | .none => 0
  | .read => 1
  | .write => 2
  | .execute => 3
  | .admin => 4

structure HandoffRequest where
  callerCeiling : AuthorityLevel
  requested : AuthorityLevel
deriving DecidableEq, Repr

def HandoffAccepted (request : HandoffRequest) : Prop :=
  request.requested.rank <= request.callerCeiling.rank

theorem handoff_exceeding_caller_ceiling_rejected
    {request : HandoffRequest} :
    request.callerCeiling.rank < request.requested.rank ->
    ¬ HandoffAccepted request := by
  intro exceeds accepted
  exact Nat.not_le_of_gt exceeds accepted

end AsiStackProofs.StackBoundaries

namespace AsiStackProofs.PlanForge

structure DependencyEdge where
  dependencyIndex : Nat
  dependentIndex : Nat
deriving DecidableEq, Repr

def EdgePrecedes (edge : DependencyEdge) : Prop :=
  edge.dependencyIndex < edge.dependentIndex

structure PlanGraph where
  edges : List DependencyEdge
  acyclicCertificate : Bool
deriving DecidableEq, Repr

def DependenciesPrecede (graph : PlanGraph) : Prop :=
  ∀ edge, edge ∈ graph.edges -> EdgePrecedes edge

def Dispatchable (graph : PlanGraph) : Prop :=
  graph.acyclicCertificate = true ∧
    DependenciesPrecede graph

theorem dispatchable_plan_graph_is_index_acyclic_and_ordered
    {graph : PlanGraph} :
    Dispatchable graph ->
      graph.acyclicCertificate = true ∧ DependenciesPrecede graph := by
  intro dispatchable
  exact dispatchable

theorem dispatchable_plan_graph_orders_member_edges
    {graph : PlanGraph} {edge : DependencyEdge} :
    Dispatchable graph ->
    edge ∈ graph.edges ->
    edge.dependencyIndex < edge.dependentIndex := by
  intro dispatchable member
  exact dispatchable.2 edge member

theorem dependency_precedence_blocks_self_dependency
    {edge : DependencyEdge} :
    EdgePrecedes edge ->
    edge.dependencyIndex ≠ edge.dependentIndex := by
  intro precedes sameIndex
  unfold EdgePrecedes at precedes
  rw [sameIndex] at precedes
  exact (Nat.lt_irrefl edge.dependentIndex) precedes

inductive NodeOutcome where
  | promoted
  | escalated
  | residual
deriving DecidableEq, Repr

structure PlanNode where
  qualityPredicatePassed : Bool
  outcome : NodeOutcome
deriving DecidableEq, Repr

def ValidNodeOutcome (node : PlanNode) : Prop :=
  node.qualityPredicatePassed = true ∨
    node.outcome = NodeOutcome.escalated ∨
    node.outcome = NodeOutcome.residual

theorem failed_quality_predicate_routes_to_escalation_or_residual
    {node : PlanNode} :
    ValidNodeOutcome node ->
    node.qualityPredicatePassed = false ->
    node.outcome = NodeOutcome.escalated ∨
      node.outcome = NodeOutcome.residual := by
  intro valid failed
  cases valid with
  | inl passed =>
      rw [failed] at passed
      cases passed
  | inr fallback =>
      exact fallback

end AsiStackProofs.PlanForge

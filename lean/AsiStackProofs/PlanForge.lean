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

/-! ## Executable dependency-graph boundary

The legacy `PlanGraph` trusts an acyclicity certificate. The executable graph
below checks the actual finite edge list against a declared node count and a
topological index order. Strictly increasing dependency paths cannot cycle.
This is a graph-representation result only: node meanings, missing edges,
dependency truth, planner quality, and scheduler behavior remain outside the
model.
-/

structure ExecutablePlanGraph where
  graphId : Nat
  nodeCount : Nat
  edges : List DependencyEdge
  declaredAcyclic : Bool
  declaredDependenciesOrdered : Bool
deriving DecidableEq, Repr

def EdgeAdmissibleForNodeCount
    (nodeCount : Nat) (edge : DependencyEdge) : Bool :=
  decide (edge.dependencyIndex < nodeCount) &&
    decide (edge.dependentIndex < nodeCount) &&
      decide (edge.dependencyIndex < edge.dependentIndex)

def VerifiedPlanGraph (graph : ExecutablePlanGraph) : Bool :=
  graph.declaredAcyclic && graph.declaredDependenciesOrdered &&
    decide (0 < graph.nodeCount) &&
      graph.edges.all (EdgeAdmissibleForNodeCount graph.nodeCount)

inductive DependencyReachable
    (edges : List DependencyEdge) : Nat -> Nat -> Prop where
  | edge {dependency dependent : Nat} :
      { dependencyIndex := dependency
        dependentIndex := dependent } ∈ edges ->
      DependencyReachable edges dependency dependent
  | trans {start middle finish : Nat} :
      DependencyReachable edges start middle ->
      DependencyReachable edges middle finish ->
      DependencyReachable edges start finish

theorem verified_plan_graph_member_edge_is_bounded_and_ordered
    {graph : ExecutablePlanGraph} {edge : DependencyEdge}
    (verified : VerifiedPlanGraph graph = true)
    (member : edge ∈ graph.edges) :
    edge.dependencyIndex < graph.nodeCount ∧
      edge.dependentIndex < graph.nodeCount ∧
        edge.dependencyIndex < edge.dependentIndex := by
  simp [VerifiedPlanGraph, List.all_eq_true,
    EdgeAdmissibleForNodeCount] at verified
  have checked := verified.2 edge member
  exact ⟨checked.1.1, checked.1.2, checked.2⟩

theorem verified_plan_graph_dependency_paths_strictly_increase
    {graph : ExecutablePlanGraph} {start finish : Nat}
    (verified : VerifiedPlanGraph graph = true)
    (reachable : DependencyReachable graph.edges start finish) :
    start < finish := by
  induction reachable with
  | edge member =>
      exact
        (verified_plan_graph_member_edge_is_bounded_and_ordered
          verified member).2.2
  | trans _ _ increasingLeft increasingRight =>
      exact Nat.lt_trans increasingLeft increasingRight

theorem verified_plan_graph_excludes_dependency_cycles
    {graph : ExecutablePlanGraph} {node : Nat}
    (verified : VerifiedPlanGraph graph = true) :
    ¬ DependencyReachable graph.edges node node := by
  intro cycle
  exact (Nat.lt_irrefl node)
    (verified_plan_graph_dependency_paths_strictly_increase verified cycle)

inductive PlanGraphAdmissionDecision where
  | reject
  | admit
deriving DecidableEq, Repr

def PlanGraphAdmissionDecisionFor
    (graph : ExecutablePlanGraph) : PlanGraphAdmissionDecision :=
  if VerifiedPlanGraph graph then .admit else .reject

theorem verified_plan_graph_routes_to_admission
    {graph : ExecutablePlanGraph}
    (verified : VerifiedPlanGraph graph = true) :
    PlanGraphAdmissionDecisionFor graph = .admit := by
  simp [PlanGraphAdmissionDecisionFor, verified]

def diamondPlanGraph : ExecutablePlanGraph where
  graphId := 1003
  nodeCount := 4
  edges := [
    { dependencyIndex := 0, dependentIndex := 1 },
    { dependencyIndex := 0, dependentIndex := 2 },
    { dependencyIndex := 1, dependentIndex := 3 },
    { dependencyIndex := 2, dependentIndex := 3 }
  ]
  declaredAcyclic := true
  declaredDependenciesOrdered := true

def selfDependentPlanGraph : ExecutablePlanGraph where
  graphId := 1003
  nodeCount := 4
  edges := [
    { dependencyIndex := 0, dependentIndex := 1 },
    { dependencyIndex := 0, dependentIndex := 2 },
    { dependencyIndex := 1, dependentIndex := 1 },
    { dependencyIndex := 2, dependentIndex := 3 }
  ]
  declaredAcyclic := true
  declaredDependenciesOrdered := true

def reverseDependencyPlanGraph : ExecutablePlanGraph :=
  { diamondPlanGraph with
      edges := [{ dependencyIndex := 2, dependentIndex := 1 }] }

def outOfBoundsPlanGraph : ExecutablePlanGraph :=
  { diamondPlanGraph with
      edges := [{ dependencyIndex := 3, dependentIndex := 4 }] }

theorem diamond_plan_graph_is_verified :
    VerifiedPlanGraph diamondPlanGraph = true := by
  decide

theorem diamond_plan_graph_has_reachable_join :
    DependencyReachable diamondPlanGraph.edges 0 3 := by
  exact DependencyReachable.trans
    (DependencyReachable.edge
      (dependency := 0) (dependent := 1) (by simp [diamondPlanGraph]))
    (DependencyReachable.edge
      (dependency := 1) (dependent := 3) (by simp [diamondPlanGraph]))

theorem self_dependency_graph_is_rejected :
    PlanGraphAdmissionDecisionFor selfDependentPlanGraph = .reject := by
  decide

theorem reverse_dependency_graph_is_rejected :
    PlanGraphAdmissionDecisionFor reverseDependencyPlanGraph = .reject := by
  decide

theorem out_of_bounds_graph_is_rejected :
    PlanGraphAdmissionDecisionFor outOfBoundsPlanGraph = .reject := by
  decide

structure ThinPlanGraphSummary where
  graphId : Nat
  nodeCount : Nat
  edgeCount : Nat
  declaredAcyclic : Bool
  declaredDependenciesOrdered : Bool
deriving DecidableEq, Repr

def ThinPlanGraphSummaryOf
    (graph : ExecutablePlanGraph) : ThinPlanGraphSummary :=
  { graphId := graph.graphId
    nodeCount := graph.nodeCount
    edgeCount := graph.edges.length
    declaredAcyclic := graph.declaredAcyclic
    declaredDependenciesOrdered := graph.declaredDependenciesOrdered }

theorem thin_plan_graph_summary_has_admission_collision :
    diamondPlanGraph ≠ selfDependentPlanGraph ∧
      ThinPlanGraphSummaryOf diamondPlanGraph =
        ThinPlanGraphSummaryOf selfDependentPlanGraph ∧
      PlanGraphAdmissionDecisionFor diamondPlanGraph = .admit ∧
      PlanGraphAdmissionDecisionFor selfDependentPlanGraph = .reject := by
  decide

theorem no_thin_plan_graph_classifier_recovers_both_decisions
    (classify : ThinPlanGraphSummary -> PlanGraphAdmissionDecision) :
    classify (ThinPlanGraphSummaryOf diamondPlanGraph) ≠
        PlanGraphAdmissionDecisionFor diamondPlanGraph ∨
      classify (ThinPlanGraphSummaryOf selfDependentPlanGraph) ≠
        PlanGraphAdmissionDecisionFor selfDependentPlanGraph := by
  have collision := thin_plan_graph_summary_has_admission_collision.2.1
  have separated :
      PlanGraphAdmissionDecisionFor diamondPlanGraph ≠
        PlanGraphAdmissionDecisionFor selfDependentPlanGraph := by
    decide
  by_cases recoversDiamond :
      classify (ThinPlanGraphSummaryOf diamondPlanGraph) =
        PlanGraphAdmissionDecisionFor diamondPlanGraph
  · right
    intro recoversSelfDependent
    apply separated
    calc
      PlanGraphAdmissionDecisionFor diamondPlanGraph =
          classify (ThinPlanGraphSummaryOf diamondPlanGraph) :=
        recoversDiamond.symm
      _ = classify (ThinPlanGraphSummaryOf selfDependentPlanGraph) :=
        congrArg classify collision
      _ = PlanGraphAdmissionDecisionFor selfDependentPlanGraph :=
        recoversSelfDependent
  · exact Or.inl recoversDiamond

structure CompletePlanGraphTransport where
  graphId : Nat
  nodeCount : Nat
  edges : List DependencyEdge
  declaredAcyclic : Bool
  declaredDependenciesOrdered : Bool
deriving DecidableEq, Repr

def CompletePlanGraphTransportOf
    (graph : ExecutablePlanGraph) : CompletePlanGraphTransport :=
  { graphId := graph.graphId
    nodeCount := graph.nodeCount
    edges := graph.edges
    declaredAcyclic := graph.declaredAcyclic
    declaredDependenciesOrdered := graph.declaredDependenciesOrdered }

def ExecutablePlanGraphOf
    (transport : CompletePlanGraphTransport) : ExecutablePlanGraph :=
  { graphId := transport.graphId
    nodeCount := transport.nodeCount
    edges := transport.edges
    declaredAcyclic := transport.declaredAcyclic
    declaredDependenciesOrdered := transport.declaredDependenciesOrdered }

theorem complete_plan_graph_transport_round_trips
    (graph : ExecutablePlanGraph) :
    ExecutablePlanGraphOf (CompletePlanGraphTransportOf graph) = graph := by
  cases graph
  rfl

theorem complete_plan_graph_transport_is_injective :
    Function.Injective CompletePlanGraphTransportOf := by
  intro left right equal
  calc
    left = ExecutablePlanGraphOf (CompletePlanGraphTransportOf left) :=
      (complete_plan_graph_transport_round_trips left).symm
    _ = ExecutablePlanGraphOf (CompletePlanGraphTransportOf right) :=
      congrArg ExecutablePlanGraphOf equal
    _ = right := complete_plan_graph_transport_round_trips right

theorem complete_plan_graph_transport_preserves_admission
    (graph : ExecutablePlanGraph) :
    PlanGraphAdmissionDecisionFor
        (ExecutablePlanGraphOf (CompletePlanGraphTransportOf graph)) =
      PlanGraphAdmissionDecisionFor graph := by
  rw [complete_plan_graph_transport_round_trips]

def ProjectExecutablePlanGraphToLegacy
    (graph : ExecutablePlanGraph) : PlanGraph :=
  { edges := graph.edges
    acyclicCertificate := VerifiedPlanGraph graph }

theorem verified_plan_graph_projects_to_legacy_dispatchable
    {graph : ExecutablePlanGraph}
    (verified : VerifiedPlanGraph graph = true) :
    Dispatchable (ProjectExecutablePlanGraphToLegacy graph) := by
  constructor
  · simpa [ProjectExecutablePlanGraphToLegacy] using verified
  · intro edge member
    exact
      (verified_plan_graph_member_edge_is_bounded_and_ordered
        verified member).2.2

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

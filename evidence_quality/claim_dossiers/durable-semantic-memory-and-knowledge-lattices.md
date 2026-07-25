# Claim Dossier: Durable Semantic Memory and Knowledge Lattices

Chapter ID: `durable-semantic-memory-and-knowledge-lattices`

Status: P1 semantic review pending

Core support state: `argument`

This dossier is generated from the manifest and review overlay. Inclusion is not proof or promotion.

| Atom | Role | Type | Review | Proposition |
|---|---|---|---|---|
| `durable-semantic-memory-and-knowledge-lattices.core` | `core` | `composite` | `semantically_reviewed` | Durable semantic memory should be admitted through a versioned knowledge-lattice contract that binds object and relation identity, ontology, provenance, support state, temporal validity, authority and rights, merge and supersession, contradiction, retrieval route, compaction and forgetting, restart recovery, consumer use, and residual uncertainty; retrieval quality, graph connectivity, model recall, persistence, or a fluent answer alone establishes neither truth, complete memory, safe consolidation, erasure, nor decision authority. |
| `durable-semantic-memory-and-knowledge-lattices.problem.001` | `problem` | `source-synthesis` | `semantically_reviewed` | Long-lived AI systems need semantic objects that survive restarts, support graph and associative retrieval, evolve across ontology versions, preserve provenance, merge and retract conflicting assertions, forget under policy, and remain distinguishable from transient context and model weights. |
| `durable-semantic-memory-and-knowledge-lattices.insufficiency.001` | `insufficiency` | `composite` | `semantically_reviewed` | Vector stores, knowledge graphs, GraphRAG, conversational memory, long-context models, and learned memory can improve retrieval, but none automatically supplies stable object identity, temporal validity, typed relations, provenance-preserving revision, ontology migration, poisoning controls, rights propagation, compaction, and restart-consistent persistence. |
| `durable-semantic-memory-and-knowledge-lattices.minimum.001` | `minimum` | `executable` | `semantically_reviewed` | The smallest honest implementation boundary for Durable Semantic Memory and Knowledge Lattices is: Implement a versioned semantic-object schema, event-sourced store, validator, and replay fixture with typed nodes and relations, temporal validity, provenance, contradiction, supersession, ontology version, rights, and transactional snapshots. Compare exact, vector, graph, and hybrid retrieval on update-heavy tasks with injected collisions, stale facts, conflicting sources, poisoning, deletion, compaction, crash, and restart while measuring utility, provenance survival, contradiction calibration, rights closure, latency, and residuals. |
| `durable-semantic-memory-and-knowledge-lattices.beyond_sota.001` | `beyond_sota` | `composite` | `semantically_reviewed` | At maturity, the operational contract is a replaceable knowledge-lattice service whose semantic state is durable but never treated as unquestionable truth. Exact, vector, graph, associative, temporal, and learned retrieval may evolve behind a stable contract while object identity, ontology versions, provenance, contradiction, temporal validity, rights, actual use, compaction, forgetting, deletion, backup, restart, and consumer invalidation remain distinct and replayable across migrations. |
| `durable-semantic-memory-and-knowledge-lattices.mechanism.001` | `mechanism` | `composite` | `semantically_reviewed` | Assign stable semantic identities to entities, events, claims, relations, procedures, and source objects while retaining aliases, uncertainty, and collision records. |
| `durable-semantic-memory-and-knowledge-lattices.mechanism.002` | `mechanism` | `composite` | `semantically_reviewed` | Version ontologies and relation schemas; migrate through explicit mappings that preserve losses, unresolved cases, and invalidated consumers. |
| `durable-semantic-memory-and-knowledge-lattices.mechanism.003` | `mechanism` | `composite` | `semantically_reviewed` | Represent provenance, support, temporal scope, authority, rights, contradictions, supersession, retraction, and derived dependencies on every memory object. |
| `durable-semantic-memory-and-knowledge-lattices.mechanism.004` | `mechanism` | `composite` | `semantically_reviewed` | Combine exact, vector, graph, associative, temporal, and learned navigation under a retrieval plan that records which objects were actually used. |
| `durable-semantic-memory-and-knowledge-lattices.mechanism.005` | `mechanism` | `composite` | `semantically_reviewed` | Consolidate, compact, expire, forget, and recover transactionally, separating storage erasure, retrieval suppression, behavioral forgetting, influence, privacy, and backup state. |
| `durable-semantic-memory-and-knowledge-lattices.interface.001` | `interface` | `executable` | `semantically_reviewed` | Virtual Context ABI materializes bounded consumer packets; this chapter owns the durable semantic substrate it reads. |
| `durable-semantic-memory-and-knowledge-lattices.interface.002` | `interface` | `executable` | `semantically_reviewed` | Context Transactions owns isolation, commit, mounts, taint, and crash semantics across state changes. |
| `durable-semantic-memory-and-knowledge-lattices.interface.003` | `interface` | `executable` | `semantically_reviewed` | Claim Ledgers owns belief support and revision; durable memory stores the semantic objects and relations those claims reference. |
| `durable-semantic-memory-and-knowledge-lattices.interface.004` | `interface` | `executable` | `semantically_reviewed` | Procedural Memory owns reusable action trajectories; Artifact Graphs owns generic evidence lineage. |
| `durable-semantic-memory-and-knowledge-lattices.interface.005` | `interface` | `executable` | `semantically_reviewed` | Privacy/Data Rights and Data Engines govern rights, deletion, learned influence, and descendant obligations. |
| `durable-semantic-memory-and-knowledge-lattices.invariant.001` | `invariant` | `formal` | `semantically_reviewed` | Object identity, source identity, semantic equivalence, and aliasing remain distinct. |
| `durable-semantic-memory-and-knowledge-lattices.invariant.002` | `invariant` | `formal` | `semantically_reviewed` | No merge erases provenance, contradiction, uncertainty, temporal scope, or rights. |
| `durable-semantic-memory-and-knowledge-lattices.invariant.003` | `invariant` | `formal` | `semantically_reviewed` | Ontology migration records unmapped and lossy cases and invalidates affected consumers. |
| `durable-semantic-memory-and-knowledge-lattices.invariant.004` | `invariant` | `formal` | `semantically_reviewed` | Retrieval records actual use; storage presence does not imply influence or belief. |
| `durable-semantic-memory-and-knowledge-lattices.invariant.005` | `invariant` | `formal` | `semantically_reviewed` | Restart recovery, compaction, forgetting, deletion, and model unlearning remain separate claims. |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.001` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: entity collision |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.002` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: duplicate identity |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.003` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: stale truth |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.004` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: ontology drift |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.005` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: relation poisoning |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.006` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: provenance loss |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.007` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: contradiction collapse |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.008` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: false supersession |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.009` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: retrieval popularity bias |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.010` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: privacy leakage |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.011` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: compaction damage |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.012` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: incomplete forgetting |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.013` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: crash inconsistency |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.014` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: backup resurrection |
| `durable-semantic-memory-and-knowledge-lattices.failure_mode.015` | `failure_mode` | `causal` | `semantically_reviewed` | For Durable Semantic Memory and Knowledge Lattices, a material failure mode is: memory-to-context authority laundering |
| `durable-semantic-memory-and-knowledge-lattices.formal.durable-semantic-memory-and-knowledge-lattices-admission-boundary` | `formal_target` | `formal` | `semantically_reviewed` | A finite Durable Semantic Memory and Knowledge Lattices record may hand off only when identity, authority, version, required checks, and residual ownership are present; no theorem grants empirical effectiveness or release authority. |

## Argument-exit state

No promotion-or-refutation campaign is frozen yet. P1 must first replace every machine candidate with a semantic review and adjudicate every prose-only candidate.

## Non-claims

- This dossier does not establish semantic adequacy, implementation behavior, empirical benefit, transfer, safety, or SOTA status.
- All support movement requires a separate accepted evidence-transition record.

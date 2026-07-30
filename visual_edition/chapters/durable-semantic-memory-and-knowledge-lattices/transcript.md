# Descriptive transcript — Durable Semantic Memory and Knowledge Lattices

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/durable-semantic-memory-and-knowledge-lattices.html>

Video ID: `asi-video-durable-semantic-memory-and-knowledge-lattices`

Lifecycle: scripted local derivative; no YouTube publication is authorized

Current support: `argument` — `Design rationale`

## 00:00–00:48 — Problem and shortcut

**Visual description.** The chapter title resolves into two labeled cards: the problem and the shortcut that does not solve it.

**Narration.** This chapter asks a specific question: Long-lived AI systems need semantic objects that survive restarts, support graph and associative retrieval, evolve across ontology versions, preserve provenance, merge and retract conflicting assertions, forget under policy, and remain distinguishable from transient context and model weights. The tempting shortcut is insufficient: Vector stores, knowledge graphs, GraphRAG, conversational memory, long-context models, and learned memory can improve retrieval, but none automatically supplies stable object identity, temporal validity, typed relations, provenance-preserving revision, ontology migration, poisoning controls, rights propagation, compaction, and restart-consistent persistence.

## 00:48–01:45 — Operating mechanism

**Visual description.** A labeled state machine diagram exposes four distinct responsibilities and their explicit relationships.

**Narration.** The chapter's core claim is this: Durable semantic memory should be admitted through a versioned knowledge-lattice contract that binds object and relation identity, ontology, provenance, support state, temporal validity, authority and rights, merge and supersession, contradiction, retrieval route, compaction and forgetting, restart recovery, consumer use, and residual uncertainty; retrieval quality, graph connectivity, model recall, persistence, or a fluent answer alone establishes neither truth, complete memory, safe consolidation, erasure, nor decision authority. Assign stable semantic identities to entities, events, claims, relations, procedures, and source objects while retaining aliases, uncertainty, and collision records. Version ontologies and relation schemas; migrate through explicit mappings that preserve losses, unresolved cases, and invalidated consumers.

## 01:45–02:42 — Concrete state transition

**Visual description.** Four numbered state nodes move left to right; an observed receipt and an open residual remain separately labeled.

**Narration.** A concrete implementation trace makes the proposal testable. Implement a versioned semantic-object schema, event-sourced store, validator, and replay fixture with typed nodes and relations, temporal validity, provenance, contradiction, supersession, ontology version, rights, and transactional snapshots. Compare exact, vector, graph, and hybrid retrieval on update-heavy tasks with injected collisions, stale facts, conflicting sources, poisoning, deletion, compaction, crash, and restart while measuring utility, provenance survival, contradiction calibration, rights closure, latency, and residuals. Version ontologies and relation schemas; migrate through explicit mappings that preserve losses, unresolved cases, and invalidated consumers. Represent provenance, support, temporal scope, authority, rights, contradictions, supersession, retraction, and derived dependencies on every memory object.

## 02:42–02:57 — Failure boundary

**Visual description.** Four failure cards meet a red fail-closed boundary labeled RECORD THE RESIDUAL.

**Narration.** The design can still fail. entity collision duplicate identity stale truth ontology drift The correct response is to stop, narrow, quarantine, compensate, or retain an owned residual rather than narrate uncertainty away.

## 02:57–03:40 — Evidence state

**Visual description.** A double-rule proof boundary names the claim label and support state beside three unresolved proof targets.

**Narration.** This chapter remains Design rationale at argument support. Its contracts, examples, tests, or local artifacts establish only their encoded scope. The chapter names proof targets rather than pretending they are already closed. A finite Durable Semantic Memory and Knowledge Lattices record may hand off only when identity, authority, version, required checks, and residual ownership are present; no theorem grants empirical effectiveness or release authority. No merge erases provenance, contradiction, uncertainty, temporal scope, or rights. Ontology migration records unmapped and lossy cases and invalidates affected consumers.

## 03:40–04:08 — Non-claims

**Visual description.** Four muted non-claim rows, each marked by a red stop bar, state what the visual does not establish.

**Narration.** No chapter claim or evidence state is promoted by this visual. A named mechanism is not proof of correct implementation or useful deployment. A local check or formal model does not establish real-world enforcement. No safety, transfer, state-of-the-art, AGI, or ASI conclusion follows. These boundaries matter because an explanatory derivative is useful only if it preserves the evidence ceiling of its source.

## 04:08–04:43 — Handoff

**Visual description.** The source end card states the live chapter, evidence ceiling, canonical URL, and successor chapter.

**Narration.** At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result. The next chapter is Context Transactions, Snapshots, Mounts, and Taint. It takes responsibility for Long-lived agents and parallel workers mutate durable context through multiple stores, branches, indexes, caches, summaries, and recovery paths. Read the live chapter for its complete source mappings, interfaces, invariants, failure modes, tests, and open evidence gaps.

## Source and evidence boundary

At most, this visual explains the chapter's design rationale at argument support; it adds no empirical, deployment, safety, transfer, state-of-the-art, AGI, or ASI result.

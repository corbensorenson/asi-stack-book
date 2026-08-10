---
title: "Question-Compiled Semantic Addressing"
subtitle: "A Governed Architecture for Stable Semantic Identity, Multi-Facet Address Atlases, Active Disambiguation, and Compiled AI Routing"
author: "Corben Sorenson"
date: "July 12, 2026"
version: "1.0"
status: "Conceptual architecture / design rationale"
canonical-source-id: "qcsa_whitepaper"
---

# Question-Compiled Semantic Addressing

## A Governed Architecture for Stable Semantic Identity, Multi-Facet Address Atlases, Active Disambiguation, and Compiled AI Routing

**Corben Sorenson**  
Technical Whitepaper, Version 1.0  
July 12, 2026

> **Evidence status.** This paper presents a target architecture and research program. It does not report an implementation, benchmark result, proof of semantic correctness, or validated performance advantage. Its claims are design hypotheses grounded in adjacent literature through July 12, 2026.

> **Core thesis.** **Store by stable identity. Index by plural semantic addresses. Find by adaptive questions. Reason over a typed evidence graph. Execute through compiled physical routes.**

---

## Abstract

Contemporary AI systems assign flat identifiers to tokens, documents, memories, tools, experts, and other objects, then learn most useful structure indirectly inside dense parameters. Hierarchical softmax, tree tokenizers, semantic identifiers, generative retrieval, vector quantization, hyperbolic representation learning, active learning, knowledge graphs, and sparse routing each recover part of the missing structure. Yet these lines of work usually optimize a single boundary: vocabulary prediction, compression, retrieval, recommendation, ontology geometry, or expert selection. They also tend to conflate at least two of three fundamentally different roles: the durable identity of an object, its semantic position in a learned organization, and its current physical location or execution route.

This paper proposes **Question-Compiled Semantic Addressing (QCSA)**, a governed architecture that separates those roles. Every durable semantic object receives a stable, opaque identity. The system learns multiple task-scoped, versioned semantic virtual addresses over an evidence-bearing typed hypergraph. A probabilistic question compiler navigates uncertainty by selecting internal discriminators or external clarification questions that maximize expected information value subject to cost, latency, privacy, and risk. A translation layer then compiles semantic addresses into physical route plans for memory shards, retrieval indexes, specialist models, tools, permissions, and output decoders. Addresses are variable-length, adaptive-arity, soft before commitment, error-detecting, and explicitly migratable; they are certificates or leases, not permanent identities.

The resulting architecture generalizes the original intuition of a 20-Questions tree without inheriting its brittleness. A path through a partition is treated as a cached answer trace, while the underlying knowledge substrate remains a multi-relational graph rather than a single taxonomy. The same addressing fabric can support contextual disambiguation, multilingual and multimodal grounding, coarse-to-fine generation, rare-concept sharing, sparse computation, auditable memory, and governed self-reorganization. The proposal goes beyond current semantic-ID systems by introducing identity-address-route indirection, multi-facet address atlases, active question compilation, semantic address certificates, open-world concept expressions, and lifecycle-safe address migration as one integrated systems contract.

## Executive conclusion

The binary-tree framing is useful but incomplete. Binary encoding is not the source of intelligence, Unicode bits are not semantic structure, and one universal tree cannot represent the overlapping, contextual, disputed, and temporal organization of real knowledge. The strongest logical conclusion is a layered addressing architecture with three kinds of indirection:

1. **Stable semantic identity** answers *what object is being referred to?*
2. **Semantic virtual addresses** answer *under which useful conceptual views can it be found or composed?*
3. **Physical route plans** answer *where and how should the system retrieve, process, verify, or realize it now?*

The 20-Questions idea survives as the navigation algorithm. A question is a test that partitions a posterior over candidate meanings; an address is a reusable trace through one such partitioning view. Questions and addresses are therefore related, but not interchangeable: the best question order depends on context, available evidence, cost, and risk, while a stored address is only one compiled index path.

The full architecture is not a replacement tokenizer. It is a **semantic control plane** for an advanced AI stack. It should govern how surface signals become semantic objects, how uncertain objects are clarified, how concepts share structure, how memories and tools are routed, how outputs are generated from semantic commitments, and how the organization can evolve without breaking identity or auditability.

## Contents

1. Problem and originating intuition
2. From a 20-Questions tree to a semantic address fabric
3. State of the art and the remaining systems gap
4. Design axioms
5. Reference architecture
6. Formal model
7. Semantic object identity and the evidence-bearing hypergraph
8. Multi-facet semantic address atlases
9. The question compiler and active navigator
10. Semantic-to-physical address translation
11. Compositional representation and semantic-first generation
12. Learning, consolidation, and migration
13. Multilingual and multimodal grounding
14. Governance, security, and residual honesty
15. Failure modes and mitigations
16. Evaluation and falsification program
17. Beyond-state-of-the-art contribution boundary
18. Integration surfaces for advanced AI systems
19. Limitations and non-claims
20. Conclusion

---

# 1. Problem and originating intuition

## 1.1 Flat identifiers discard useful structure

A conventional language model maps a token to an integer and uses that integer to select an embedding. The integer itself is arbitrary. The same pattern recurs elsewhere: a document has a document ID, a memory has a key, an expert has an index, a tool has a registry name, and a knowledge-base entity has a URI or row identifier. Structure may be learned around those identifiers, but it is not carried by the identifier or governed by a common addressing contract.

This creates five recurring costs.

- **No inherited meaning.** Related objects do not necessarily share any representational prefix or reusable path.
- **Repeated search.** The system repeatedly rediscovers which objects, memories, experts, or tools are relevant.
- **Weak lifecycle semantics.** Re-clustering or reorganizing an index can invalidate references or silently change what an identifier means.
- **Opaque routing.** A route to an expert, shard, or decoder is usually a transient activation rather than an inspectable semantic decision.
- **Fragmented governance.** Provenance, authority, permitted use, uncertainty, and versioning are handled separately at each subsystem, if at all.

Hierarchical codes offer an apparent remedy: assign each object a path such as `7/3/12/4`, where early positions represent broad distinctions and later positions represent finer ones. A balanced tree can reduce an output decision from a large flat classification to a small number of local decisions. Information theory, variable-length codes, hierarchical softmax, and error-correcting output codes provide the classical foundation for that intuition [1-6].

The deeper opportunity is not merely fewer logits. It is to make *addressability itself* part of the model's architecture.

## 1.2 The 20-Questions formulation

The originating thought experiment can be written as a sequence of discriminating questions:

```text
Is it physical?
  Is it living?
    Is it an animal?
      Is it a mammal?
        Is it canine?
          -> dog
```

The answers form a bit string or categorical path. Under ideal noiseless binary questions, a balanced policy can identify one of N equally likely alternatives in approximately log2(N) answers. Generalized binary search formalizes a related strategy by selecting queries that divide the remaining hypothesis set as evenly as possible, and information-theoretic active learning chooses queries by expected information gain [14, 15].

This framing contains a real architectural insight:

> **Identification can be performed as adaptive uncertainty reduction rather than flat enumeration.**

It also exposes the first major limitation. Human-readable questions such as “Is it alive?” are often ambiguous, culturally loaded, task dependent, or inapplicable. Viruses, corporations, fictional entities, legal persons, software agents, processes, and composite events do not fit cleanly into a rigid chain. A wrong answer near the root can eliminate the correct concept. A single question order is rarely optimal for every prior distribution, modality, or task.

## 1.3 The binary-address formulation

The same tree can be viewed from the opposite direction. Once an object is known, the answer trace becomes a reusable address:

```text
DOG -> physical / living / animal / mammal / canine / dog
```

This is stronger than a flat token ID because prefixes can be shared and because coarse-to-fine prediction, inherited parameters, and structured retrieval become possible. Yet a single fixed address still fails in several ways:

- A dog is also a companion, a trainable agent, a predator, a cultural symbol, a legal property category, and a word with linguistic properties.
- “Bank” is a surface form for multiple senses; the string is not the concept.
- A concept can be classified under several parents, while a tree grants only one.
- The optimal semantic organization differs from the optimal frequency code, hardware partition, load-balanced shard assignment, or safety policy.
- Meanings and workloads change, so addresses must migrate.

These failures point to the final architecture: **stable identity plus multiple learned addresses over a graph, with questions used dynamically to resolve uncertainty and addresses compiled into execution routes.**

# 2. From a 20-Questions tree to a semantic address fabric

## 2.1 Questions and addresses are procedural and declarative views

A fixed decision tree makes the relation look exact: each question outcome chooses an edge, and the sequence of outcomes names a leaf. In a practical AI system, the relationship is looser and more useful:

- A **semantic address** is a declarative index path through one versioned conceptual view.
- A **question policy** is a procedural program that chooses the next test from the current posterior, task, evidence, and cost model.

An address can be understood as a cached answer trace through a particular view, but many question sequences can identify the same object. The best sequence may skip address levels, query another facet, ask a multiclass question, inspect a sensor, retrieve a source, or ask a human. Therefore QCSA does not “decompile” every address into a fixed English questionnaire. It treats addresses as reusable partitions and questions as adaptive operations over those partitions.

## 2.2 Why binary is not the governing principle

Binary trees are elegant because each decision is simple and because a balanced binary code has logarithmic depth. Neural systems, however, pay for depth, serialization, error propagation, and poor accelerator utilization. Adaptive softmax is explicitly hardware-aware [4]. Recent tree-structured diffusion work shows that wide child prediction can drastically shrink full-vocabulary output heads; one 2026 system uses branching factor 512 and reports roughly halved peak GPU memory under matched parameter budgets [30]. Recent semantic-ID systems also show that hard early assignments propagate mistakes, while soft routing and variable-length termination improve boundary cases [31-33].

QCSA therefore adopts four rules:

1. **Branching factor is adaptive, not sacred.** Binary, 8-way, 32-way, or 512-way decisions may be appropriate at different nodes and hardware boundaries.
2. **Depth is variable.** Refinement stops when the consumer's required adequacy is reached, not when an arbitrary fixed code length is exhausted.
3. **Routing is soft before commitment.** The system may carry a posterior over several paths and harden only when a downstream action requires it.
4. **Redundancy is allowed.** Cross-facet agreement, checksums, or error-correcting symbols can detect or recover from path errors.

## 2.3 Why a graph is the truth substrate and trees are indexes

Hierarchical embeddings demonstrate that tree-like and partial-order structure can be represented compactly in specialized geometries [10-13]. Knowledge graphs demonstrate the value of typed relations among entities, events, concepts, and claims [40]. But ordinary knowledge is not one tree. It contains multiple inheritance, n-ary events, temporal validity, causal links, composition, contradiction, uncertain hypotheses, provenance, and perspective.

QCSA therefore uses a **typed, temporal, evidence-bearing hypergraph** as the durable semantic substrate. Hierarchical trees or DAGs are compiled as indexes over that substrate. A semantic object may occur in multiple atlas views, while one stable identity links those occurrences.

The central separation is:

```text
Identity:        what object is this?
Semantic view:  under which conceptual partition is it being used?
Physical route: where and how should it be processed now?
```

This resembles the separation between a stable name, a virtual address, and a physical address in mature computing systems. The indirection is not overhead; it is what permits reorganization without referential collapse.

# 3. State of the art and the remaining systems gap

QCSA is a synthesis built on substantial prior work. Its contribution cannot be “a binary tree for vocabulary,” because that family of ideas is established. The relevant frontier is the integration of semantic identity, learned hierarchical codes, active navigation, graph reasoning, lifecycle governance, and runtime routing.

## 3.1 Hierarchical output prediction

Hierarchical language models factor a large output distribution into decisions along a tree [2, 3]. Adaptive softmax partitions words by frequency and computational cost for efficient GPU training [4]. Binary-code neural translation predicts compact output codes and uses error-correcting or hybrid designs to limit error propagation [6]. These methods establish that path prediction can reduce output cost, but their code paths are primarily output mechanisms. They do not define a persistent, multi-system semantic identity layer.

## 3.2 Discrete codes and coarse-to-fine representations

Vector quantization, product quantization, and VQ-VAE show how continuous representations can be mapped into compact discrete codebooks [7, 8]. Matryoshka representation learning shows that one representation can expose nested granularities for different resource budgets [9]. These approaches establish useful mechanisms for compact codes and coarse-to-fine access. They do not by themselves solve identity stability, multiple semantic views, address migration, or question-driven disambiguation.

## 3.3 Hierarchical geometry and knowledge graphs

Order embeddings, Poincare embeddings, entailment cones, and relation-specific hyperbolic cones model taxonomies, partial orders, and multiple hierarchical relations [10-13]. Knowledge graphs provide typed relational structure and can include entities, events, and abstract concepts [40]. These approaches model semantic structure, but they generally do not turn that structure into a unified address and routing protocol spanning model output, memory, tools, experts, and generation.

## 3.4 Generative retrieval and semantic identifiers

Differentiable Search Index generates document identifiers directly [21]. MINDER uses multiple identifier views to improve generative retrieval [22]. TIGER, VQ-Rec, and SEATER represent items with learned semantic code tuples or tree-structured identifiers [23-25]. RPG shows that longer semantic IDs can be generated in parallel and constrained by a graph of valid IDs [26].

The 2026 literature reveals the central failure modes of the paradigm. DIGER argues that static, separately trained semantic IDs create an objective mismatch and that end-to-end learning can suffer codebook collapse [31]. ReSID optimizes for predictive sufficiency and prefix-conditional uncertainty rather than generic semantic reconstruction [32]. CapsID replaces hard nearest-neighbor assignment with soft capsule routing and confidence-driven variable length because early hard choices collapse multi-faceted semantics at cluster boundaries [33]. Work on identifier ambiguity shows that generative retrieval can fail when identifiers are not distinctive enough for decoding [34].

These findings strongly support QCSA's soft, task-aware, variable-length design. They also expose a deeper gap: most semantic-ID systems use the learned code as both object identifier and decoder target. When the codebook changes, identity and representation change together.

## 3.5 Tree tokenization and hierarchical generation

TreeTok induces morphological character trees and uses top-down vocabulary matching [27]. ToaST builds binary split trees over byte n-grams and optimizes vocabulary selection for compression; its authors report lower token counts and improved results in their experiments [28]. HDLM predicts progressively finer semantic scales in a diffusion process [29]. TDLM predicts child nodes in a vocabulary tree rather than the entire vocabulary, shrinking the output head and memory footprint [30].

These results make tree-structured surface decomposition and output prediction technically credible. They do not establish that token trees are concept trees. Surface forms, morphemes, and bytes are evidence for meaning, not stable meaning itself.

## 3.6 Active questions and sparse routing

Generalized binary search and Bayesian active learning formalize query selection by hypothesis reduction or information gain [14, 15]. Routing Transformer and Switch Transformer demonstrate content-based sparse attention and expert routing [35, 36]. These systems reduce computation by selecting subsets of information or parameters. They do not normally produce durable semantic address certificates, preserve identity across route changes, or expose question selection and route translation as one governed control plane.

## 3.7 Multilingual and token-free models

CANINE and ByT5 show that character- and byte-level models can avoid a fixed subword vocabulary and improve robustness or multilingual coverage, though longer surface sequences create tradeoffs [16, 17]. ChineseBERT uses glyph and pinyin features to improve Chinese representations [18]. Cross-lingual alignment research shows that multilingual spaces can align but remain uneven across scripts, typology, and concept types [19, 20].

The implication is not that all languages should share a Unicode-bit tree. It is that language-specific surface evidence should resolve into a shared but probabilistic semantic identity layer.

## 3.8 The unresolved systems gap

No reviewed approach in this literature, to the best of this paper's search, combines all of the following as one architecture:

- stable semantic identity separated from learned address;
- multiple contextual and task-scoped addresses per object;
- a graph or hypergraph as the durable knowledge substrate;
- active questions as an adaptive decoder of semantic uncertainty;
- semantic-to-physical route translation for memories, experts, tools, and generation;
- address certificates carrying provenance, adequacy, authority, uncertainty, permitted use, and lifecycle state;
- governed address migration with old-address resolution and rollback;
- open-world concept creation and compositional semantic expressions.

That integrated gap is the target of QCSA.

# 4. Design axioms

QCSA is governed by twelve axioms. They are stronger than implementation preferences because violating any one recreates a known failure mode.

## Axiom 1: Identity is not an address

A stable Semantic Object ID must survive re-clustering, renaming, translation, ontology revision, model replacement, and physical relocation. An address is a versioned representation of an object's position in one view.

## Axiom 2: An address is not a physical route

Semantic similarity, access frequency, hardware topology, model capacity, security boundaries, and data locality optimize different objectives. A translation layer maps semantic virtual addresses to physical route plans. It may change without changing identity or semantic classification.

## Axiom 3: Trees are indexes; the graph is the knowledge substrate

A tree supplies efficient partition and navigation. The durable substrate must support multiple parents, typed relations, n-ary events, temporal state, provenance, contradiction, and uncertainty.

## Axiom 4: One object may have multiple valid addresses

Ontological, functional, causal, linguistic, perceptual, procedural, policy, and workload views can all be useful. No single “true path” is assumed.

## Axiom 5: Addresses are contextual leases

An address is issued for a task, consumer, atlas epoch, and adequacy target. It carries confidence, permitted use, and expiry or revalidation conditions. A route useful for retrieval may be inadequate for a legal claim or irreversible action.

## Axiom 6: Questions are selected by value, not by fixed order

The next discriminator should maximize expected reduction in decision-relevant uncertainty after accounting for compute, latency, privacy, interaction cost, and failure risk. Natural-language questions are used only when external information is actually needed.

## Axiom 7: Uncertainty remains explicit until a commitment boundary

Soft path distributions, candidate beams, and abstention are first-class. Early ambiguity must not be hidden by a clean-looking leaf.

## Axiom 8: Unknown and novel concepts are first-class outcomes

The resolver may emit “unresolved,” create a provisional object, or compose a new expression. It must not force every input into the nearest known leaf.

## Axiom 9: Surface encoding is not semantic identity

Bytes, characters, morphemes, glyphs, radicals, phonemes, image patches, and sensor features belong to grounding encoders. Shared semantic identity is resolved above those modality-specific structures.

## Axiom 10: Semantics are consumer-relative and evidence-bearing

No address is adequate in the abstract. It is adequate for a consumer and purpose under stated evidence, loss, and uncertainty. A semantic node is not automatically a true proposition.

## Axiom 11: Reorganization must be referentially safe

Atlas updates are versioned releases with migration maps, compatibility checks, shadow evaluation, rollback, and immutable audit. Old addresses must either resolve to the same stable object or fail explicitly.

## Axiom 12: Compression may not hide residual burden

Short addresses, shared path deltas, and compact semantic plans are useful only when collisions, omitted distinctions, verifier cost, repair cost, migration cost, and fallback are recorded.

# 5. Reference architecture

QCSA is best understood as a semantic control plane with ten cooperating components.

![Figure 1. QCSA reference architecture.](assets/figure_1_reference_architecture.png)

## 5.1 Surface and grounding gateways

Modality-specific encoders preserve exact input and extract evidence:

- bytes, characters, subwords, morphology, syntax, glyphs, and pronunciation for language;
- regions, objects, geometry, and temporal tracks for vision;
- acoustic events and speaker features for audio;
- state, action, affordance, and causal observations for embodied systems;
- schemas, types, symbols, and execution traces for code and tools.

The gateway is reversible where exact reconstruction matters. It does not claim that byte or glyph structure is itself the concept hierarchy.

## 5.2 Contextual semantic resolver

The resolver maps an occurrence in context to a posterior over stable semantic objects and compositional expressions. It distinguishes at least four things:

1. **Surface occurrence:** the span, region, event segment, or sensor observation.
2. **Semantic type:** a reusable concept such as `financial institution`.
3. **World instance:** a particular bank, person, event, document, or tool.
4. **Proposition or expression:** a compositional structure such as “the bank approved the loan yesterday.”

This separation prevents a word string from becoming the permanent identity of all its senses. The resolver may emit several candidates, create a provisional object, or request clarification.

## 5.3 Stable semantic object registry

The registry assigns opaque, durable Semantic Object IDs (SOIDs). A SOID names an object record, not a tree position. Records can represent concepts, entities, events, relations, propositions, memories, documents, tools, policies, capabilities, or artifact obligations.

The registry maintains aliases, definitions, provenance, lifecycle state, namespace, merge and split history, and links to atlas addresses. The ID should remain stable even when the preferred name, embedding, ontology, or route changes.

## 5.4 Typed evidence-bearing semantic hypergraph

The hypergraph stores typed edges and hyperedges such as:

- `is_a`, `part_of`, `instance_of`, `causes`, `enables`, `prevents`;
- `used_for`, `located_in`, `precedes`, `contradicts`, `supports`;
- `expressed_as`, `translated_as`, `observed_by`, `derived_from`;
- `authorized_for`, `prohibited_for`, `requires_approval`, `supersedes`.

Claims and evidence are separated. An edge may be asserted, hypothesized, disputed, time-bounded, source-scoped, or revoked. This prevents a semantic map from laundering uncertain information into apparent truth.

## 5.5 Multi-facet semantic address atlas

The atlas is a family of learned, versioned hierarchical views over the hypergraph. Each facet optimizes a declared purpose, for example:

- ontological kind;
- function and affordance;
- causal role;
- compositional structure;
- linguistic realization;
- perceptual similarity;
- task or workflow role;
- security and authority class;
- resource and routing affinity.

A semantic object can have several soft, variable-length addresses in each relevant facet. The atlas may use trees, DAG indexes, product codebooks, residual quantizers, or hyperbolic partitions internally. Its contract is more important than a particular learning algorithm.

## 5.6 Question compiler and active navigator

The navigator maintains a posterior over candidate objects, expressions, or routes. It chooses an internal test, retrieval, sensor action, tool call, or external question expected to improve the decision most per unit cost and risk. It supports beams, backtracking, noisy answers, and abstention.

## 5.7 Semantic address certificate service

A Semantic Address Certificate (SAC) is the consumable representation returned to downstream systems. It binds:

- stable object or expression identity;
- context and task;
- atlas epoch and facet versions;
- one or more weighted paths;
- confidence, entropy, and unresolved residuals;
- provenance and grounding evidence;
- permitted uses and authority ceiling;
- expiry, revalidation, and migration references;
- integrity or signature data.

The SAC is a lease to use a representation, not a declaration of universal truth.

## 5.8 Semantic-to-physical translation and routing plane

The translator compiles SOIDs and SACs into a physical route plan. Targets can include:

- memory shards and retrieval indexes;
- specialist models or mixture-of-experts partitions;
- tools, APIs, simulators, or proof systems;
- safety filters and approval workflows;
- language or modality decoders;
- compute tiers and latency budgets.

The translator applies policy and resource constraints. A semantic alias cannot by itself grant a capability.

## 5.9 Compositional representation engine

The engine constructs a contextual representation from stable identity, shared path deltas, relation messages, and an object-specific residual. It also supports concept expressions so that novel combinations do not require a new permanent leaf for every possible meaning.

## 5.10 Lifecycle, governance, and audit plane

Atlas updates, object merges, object splits, address migrations, policy changes, and route translations produce signed receipts. High-impact changes use shadow evaluation, staged release, compatibility tests, approval, rollback, and residual ledgers.

# 6. Formal model

This section provides one rigorous formulation. It is an architectural specification, not a claim that the formulation is unique or complete.

## 6.1 Semantic substrate

Let the durable semantic substrate be a typed temporal hypergraph:

$$
\mathcal{G}^{(t)} = (\mathcal{S}, \mathcal{R}, \mathcal{E}^{(t)}, \mathcal{P}, \mathcal{V})
$$

where:

- `S` is the set of semantic objects;
- `R` is the set of relation and hyperrelation types;
- `E(t)` is the time-indexed set of relation instances;
- `P` contains provenance, source, and evidential records;
- `V` contains validity, authority, and lifecycle state.

A stable identity function maps each object to an opaque identifier:

$$
\iota: \mathcal{S} \rightarrow \mathcal{U}
$$

The identifier is invariant under changes to names, embeddings, addresses, and physical placement.

## 6.2 Address atlas

Let `F` be a set of semantic facets and `e` an atlas epoch. Each facet exposes a hierarchical index view:

$$
T_f^{(e)} = (N_f^{(e)}, E_f^{(e)}, \rho_f^{(e)})
$$

For object `s`, context `x`, and task `tau`, a soft variable-length address is:

$$
A_f^{(e)}(s \mid x, \tau) = \big((z_1, \pi_1), \ldots, (z_L, \pi_L)\big)
$$

where `z_l` is a branch code and `pi_l` is the associated probability or confidence. The length `L`, branching factor, and termination rule may vary by object, node, task, and consumer.

The full contextual address set is:

$$
\mathcal{A}^{(e)}(s \mid x, \tau) = \{(f, w_f, A_f^{(e)}) : f \in F_{x,\tau}\}
$$

where `w_f` gates the relevance of each facet.

## 6.3 Question policy

Let `H` denote the current interaction and evidence history, `S` the target semantic object, and `Y_q` the possible answer to query `q`. A cost- and risk-aware myopic policy is:

$$
q^* = \arg\max_q \left[I(S;Y_q \mid x,\tau,H) - \lambda_c C(q) - \lambda_r R(q) - \lambda_p P(q)\right]
$$

`C(q)` is computational or interaction cost, `R(q)` is action risk, and `P(q)` is privacy or disclosure cost. Longer-horizon policies may optimize expected downstream utility rather than one-step information gain.

## 6.4 Semantic-to-physical translation

The route compiler is a policy-constrained mapping:

$$
\mathcal{T}: (\iota(s), \mathrm{SAC}, \tau, \mathrm{policy}, \mathrm{resources}) \rightarrow \mathrm{RoutePlan}
$$

The route plan may include parallel targets, fallback routes, approval gates, latency budgets, and verification obligations. It is versioned independently from the semantic atlas.

## 6.5 Compositional representation

A contextual vector representation can inherit shared refinements along several addresses:

$$
h(s \mid x,\tau) = h_{\mathrm{id}}(s) + \sum_f w_f(x,\tau) \sum_{\ell=1}^{L_f} \Delta_{f,\ell,z_\ell} + m_{\mathcal{G}}(s,x) + r(s,x,\tau)
$$

where `h_id` is an identity embedding, `Delta` are shared path deltas, `m_G` is a graph-derived message, and `r` is a bounded context-specific residual. The architecture shares information without assuming that a path fully determines meaning.

## 6.6 Multi-objective learning

A representative objective is:

$$
\begin{aligned}
\mathcal{L} ={}& \mathcal{L}_{task}
+ \lambda_{rel}\mathcal{L}_{relation}
+ \lambda_{ground}\mathcal{L}_{grounding}
+ \lambda_{rate}\mathbb{E}[L]
+ \lambda_{balance}\mathcal{L}_{balance} \\
&+ \lambda_{cal}\mathcal{L}_{calibration}
+ \lambda_{rob}\mathcal{L}_{robustness}
+ \lambda_{mig}\mathcal{L}_{migration}
+ \lambda_{gov}\mathcal{L}_{contract}
+ \lambda_{res}\mathcal{L}_{residual}.
\end{aligned}
$$

The terms respectively measure downstream utility, graph-relation preservation, multimodal grounding, address rate, branch utilization, uncertainty calibration, error recovery, stability across epochs, governance constraints, and visible residual burden. No single scalarization is universally correct; the system should publish a Pareto profile and consumer-specific weights.

## 6.7 Migration invariant

For an address migration map `M` from epoch `e` to `e+1`, referential safety requires:

$$
\mathrm{resolve}_{e+1}(M_{e\rightarrow e+1}(A_e(s))) = \iota(s)
$$

or an explicit typed failure. Silent resolution to another stable object is forbidden.

# 7. Semantic object identity and the evidence-bearing hypergraph

## 7.1 What receives an identity

The phrase “concept identity” can become too narrow. An advanced AI system must address not only dictionary-like concepts but also concrete referents, events, propositions, procedures, memories, tools, policies, and artifact obligations. QCSA therefore uses **semantic object** as the general category.

A semantic object record has a stable identity and a declared kind:

| Kind | Example | Identity requirement |
|---|---|---|
| Concept type | domestic dog | persists across names and languages |
| Entity instance | a particular animal | persists across observations and aliases |
| Event instance | a specific transaction | persists across reports and revisions |
| Relation type | causes | stable schema identity |
| Proposition | “X caused Y” | separate from whether it is believed |
| Concept expression | “red electric delivery vehicle” | compositional, possibly ephemeral |
| Document or memory | a report or episode | versioned source identity |
| Tool or capability | a theorem prover | bound to policy and runtime identity |
| Artifact obligation | “preserve requirement R17” | stable across compilation and repair |

This broadening is important because a unified address fabric should route more than lexical items. A plan may need to resolve a requirement, retrieve supporting evidence, select a tool, activate a specialist, and generate a statement. All of those operations can use semantic identity and address without pretending that all objects are the same ontological kind.

## 7.2 Occurrence, type, instance, and expression

A resolver must not collapse four distinct levels:

- **Occurrence:** the exact mention, image region, sensor segment, or code reference in context.
- **Type:** a reusable abstraction or category.
- **Instance:** a specific world or system object.
- **Expression:** a structured composition of objects, roles, quantities, time, modality, and operators.

For example, in “The fisherman sat on the bank,” the word occurrence `bank` resolves to a river-edge concept type; it may also refer to a particular location instance. The entire sentence resolves to an event expression with roles for agent, posture, location, and time. Storing only a leaf for `bank` would discard both contextual sense and compositional structure.

QCSA therefore treats concept expressions as first-class. Expressions can be DAGs or typed programs containing operators such as conjunction, negation, quantification, modality, temporal ordering, causal attribution, and role binding. They may be assigned temporary or durable SOIDs depending on reuse and governance requirements.

## 7.3 Identity creation, merge, and split

Open-world learning requires controlled identity lifecycle operations.

### Creation

A novel object begins as a **provisional semantic object** with a local namespace, source evidence, confidence, and collision search. It is not immediately promoted to a global canonical identity.

### Merge

Two records may be merged when evidence indicates coreference or semantic equivalence. The merge preserves both original IDs as aliases or tombstoned redirects, records the evidence and authority for the merge, and never rewrites historical receipts without lineage.

### Split

An overloaded record may split into several identities when distinctions become operationally important. The original ID becomes an ambiguous parent or deprecated alias; old occurrences are re-resolved only with explicit uncertainty and migration receipts.

### Non-identity

Similarity is not identity. Translation equivalence, synonymy, shared embedding neighborhoods, and common function are evidence, not proof that two records are the same object.

## 7.4 Evidence and belief are not ontology

A semantic substrate can become dangerous when a tidy graph visually converts claims into facts. QCSA separates:

- object definitions and type declarations;
- asserted propositions;
- evidence supporting or attacking those propositions;
- source and derivation lineage;
- current belief or support state;
- authority to use the proposition for a particular purpose.

The graph can therefore represent competing hypotheses without forcing an early collapse. An address may route a verifier to the relevant claim cluster while the SAC explicitly states that the claim is disputed or under-supported.

## 7.5 Typed hyperedges and role structure

Binary triples are useful but insufficient for many events. A purchase, experiment, legal decision, or tool invocation can involve multiple participants, roles, times, quantities, conditions, and receipts. QCSA allows an event or relation instance to be a semantic object connected through typed role edges:

```text
EVENT: purchase-781
  buyer       -> entity-A
  seller      -> entity-B
  asset       -> artifact-C
  price       -> quantity-D
  occurred_at -> time-E
  source      -> document-F
```

This structure supports address compilation by event type, participant role, causal function, policy class, or workflow stage without duplicating the event's identity.

# 8. Multi-facet semantic address atlases

## 8.1 Why one hierarchy is structurally wrong

A single hierarchy must choose what to privilege. A frequency tree shortens common accesses. A morphological tree preserves surface constituents. A semantic similarity tree groups neighboring embeddings. An ontology groups `is-a` relations. A hardware tree balances shards. A policy tree groups authority classes. These objectives conflict.

QCSA resolves the conflict through **plural addresses plus translation**, not by seeking one perfect tree. Each atlas facet declares:

- its consumer and optimization target;
- its source relation types and grounding data;
- its allowed branching and depth;
- its confidence and termination policy;
- its stability budget and migration cadence;
- its prohibited uses.

This makes an address inspectable as a designed representation rather than a mysterious integer sequence.

## 8.2 Semantic virtual addresses

A semantic virtual address (SVA) is a path in an atlas view, not a storage location. An illustrative address set for a dog might include:

```text
ontological:  physical / organism / animal / mammal / canine / dog
functional:   agent / mobile / trainable / companion-or-worker
ecological:   organism / terrestrial / social / predator-scavenger
linguistic:   concrete-count-noun / animate / inflecting-lexeme
policy:       animal / domesticated / welfare-protected / jurisdiction-dependent
```

The labels shown here are human-readable glosses. A learned system may use latent codewords, but every production atlas should support post hoc characterization, probe results, representative members, and known failure regions.

## 8.3 Soft membership and boundary objects

Hard nearest-centroid routing creates brittle boundaries. An item near a partition border may be assigned to one code even when several facets are equally relevant; later code positions then inherit the early mistake. Recent semantic-ID research explicitly identifies this failure and reports benefits from soft routing and confidence-driven length [33].

QCSA represents each level as a distribution over branches. A SAC can carry top-k paths or a compact lattice of alternatives. Downstream consumers choose a commitment policy:

- retrieval may explore several paths in parallel;
- low-risk generation may use a weighted mixture;
- a high-risk tool call may require one path to exceed a calibrated threshold;
- an unresolved identity may trigger a question or abstention.

## 8.4 Variable depth and semantic adequacy

A fixed-length code allocates equal detail to unequal problems. QCSA terminates refinement when the address is adequate for the consumer.

- A broad topical retrieval may stop at `medicine / cardiology`.
- A medication order may require a specific compound, formulation, dose, route, patient, and time.
- A language generator may need the concept but not the physical shard.
- A security decision may need policy and authority facets even when ontological detail is shallow.

Address length is therefore conditioned on residual entropy, task utility, and risk. A short code is not automatically superior; it is superior only if the omitted distinctions are irrelevant or explicitly residualized.

## 8.5 Adaptive arity

The branching factor at node `n` should be selected under a joint cost model:

```text
expected compute
+ serial depth cost
+ branch-classification error
+ load imbalance
+ migration instability
+ accelerator inefficiency
+ required semantic purity
```

Wide branching may be efficient on GPUs and for high-entropy partitions. Narrow branching may be appropriate when evidence supports a natural discriminator or when human clarification is binary. The atlas may use mixed arity within one view.

## 8.6 Multiple paths within one facet

Some structures are DAGs rather than trees. QCSA permits an object to appear under multiple parents within one facet, while a canonical path may be selected for compact access. Alternate paths remain in the certificate or graph. This avoids forcing `bat` to choose between `mammal`, `flying entity`, `nocturnal organism`, and `echolocating agent` as its only meaningful route.

## 8.7 Cross-facet error detection

Plural addresses create redundancy. That redundancy can be used as an error-detecting code. If an ontological path indicates `financial institution` while a linguistic and contextual path indicates `river edge`, the inconsistency becomes a trigger for re-resolution rather than a hidden representation conflict.

A production system can learn compatibility factors among facets and calculate a consistency score. It can also append explicit check symbols or relation constraints. The goal is not to force perfect agreement—different facets legitimately differ—but to detect combinations that are improbable or policy-inconsistent.

## 8.8 Address atlas as a published artifact

An atlas epoch should be a versioned artifact containing:

- codebooks, topology, and branching metadata;
- facet definitions and intended consumers;
- training data and objective summaries;
- representative and boundary examples;
- branch utilization and calibration metrics;
- migration maps from supported prior epochs;
- known collisions, blind spots, and prohibited uses;
- signatures and rollback references.

This turns semantic organization into a reviewable systems object rather than an untracked side effect of training.

![Figure 2. Stable identity, plural semantic virtual addresses, and compiled physical routes.](assets/figure_2_identity_address_route.png)

# 9. The question compiler and active navigator

## 9.1 The role of questions

The question compiler operationalizes the 20-Questions intuition without hard-coding a questionnaire. Its job is to decide what evidence to acquire next when the current semantic posterior is inadequate.

A “question” may be:

- a learned internal discriminator over latent features;
- a multiclass branch prediction;
- a retrieval query to a memory or knowledge source;
- a sensor action or experiment;
- a tool invocation;
- a request to another model or specialist;
- a natural-language clarification to a human.

The last option is the most visible but should often be the last resort. Internal evidence gathering can be cheaper and less disruptive.

## 9.2 Decision-relative uncertainty

The navigator should not minimize entropy for its own sake. It should reduce uncertainty that matters to the downstream decision. If two candidate meanings lead to the same safe action, clarification may have no value. If a small ambiguity changes legal authority or physical risk, clarification may be mandatory.

The objective therefore combines information gain with expected utility, cost, privacy, and risk. A policy can prioritize:

- expected regret reduction;
- probability of crossing an action threshold;
- verification value;
- route-cost reduction;
- safety or authority disambiguation;
- human burden.

## 9.3 Fixed paths versus adaptive policies

A stored SVA offers a default path, but the navigator may choose a different sequence. Suppose a candidate set contains a financial bank, river bank, blood bank, and aircraft bank. The highest-value first question depends on context:

- In a fishing narrative, location and physical-landform evidence may resolve the sense without asking anything.
- In an aviation log, motion and control-state evidence dominate.
- In a financial workflow, the presence of account identifiers may be decisive.
- In an underspecified user query, a natural-language question may be needed.

The address atlas supplies candidate partitions; the question compiler chooses the route through them.

## 9.4 Noisy answers and recoverable routing

Real answers are noisy. Sensors fail, users misunderstand questions, retrieved evidence conflicts, and learned discriminators misclassify. A rigid tree treats one early error as irreversible. QCSA instead uses:

- posterior updates rather than hard elimination;
- beam search over candidate paths;
- backtracking when later evidence conflicts;
- repeated or cross-facet checks for high-risk decisions;
- error-correcting redundancy;
- explicit `unknown`, `conflicting`, and `abstain` states.

The navigator also records the evidence that changed the posterior, making the identification trace auditable.

## 9.5 Machine questions and human-readable explanations

Internal discriminators need not correspond to clean natural-language concepts. A learned hyperplane may separate candidates efficiently without a concise verbal label. QCSA allows such tests, but distinguishes three levels of interpretability:

1. **Operational:** the test's inputs, outputs, calibration, and effects are inspectable.
2. **Extensional:** representative objects and counterexamples characterize the partition.
3. **Intensional:** a faithful human-readable description exists.

A system must not fabricate an intensional explanation merely because it can describe representative examples. For human-facing clarification, the question compiler should generate a natural-language question whose answer mapping is validated against the intended partition.

## 9.6 Parallel questioning

Not every question must be serial. Several cheap, independent tests can run in parallel, especially when latency dominates. The compiler can select a batch that maximizes joint information under a resource budget. This is analogous to parallel semantic-ID prediction [26], but applied to evidence acquisition and disambiguation rather than only code generation.

## 9.7 Question trace as a reusable artifact

Successful question traces can become procedural memory. The system can learn that a certain task family is efficiently resolved by a particular evidence bundle or discriminator order. Reuse is governed by context similarity and versioning; a once-effective question sequence is not promoted to a timeless ontology rule.

![Figure 3. Address-guided active navigation under uncertainty.](assets/figure_3_question_navigation.png)

# 10. Semantic-to-physical address translation

## 10.1 The second indirection layer

Semantic addresses should not directly encode machine locations. A route optimized for an ontology may overload one expert; a balanced expert assignment may destroy semantic continuity; a security boundary may require data to remain in a jurisdiction or trusted enclave. These concerns belong to a physical translation layer.

The semantic-to-physical translator resembles a compiler or memory-management unit. It accepts semantic intent and constraints, then emits an executable route plan.

## 10.2 Route-plan contents

A route plan can specify:

- target memories or indexes and query forms;
- specialist models, expert partitions, or adapters;
- tools and API operations;
- permitted data fields and redactions;
- compute tier, latency ceiling, and token budget;
- parallel branches and join conditions;
- validator and verifier requirements;
- human approval gates;
- fallback and abstention paths;
- audit and receipt obligations.

The route plan is temporary and task-specific. It does not redefine the semantic object.

## 10.3 Routing to memory

A memory system can index records by stable SOID, semantic addresses, temporal context, source, and authority. The translator chooses which views to query and how broad the search should be. A coarse address may retrieve a candidate neighborhood; graph relations and stable identity then refine the result.

This is more robust than using one embedding vector as both similarity model and durable key. Retrieval-augmented models and external-memory language models demonstrate the value of non-parametric access [37, 38], while QCSA adds explicit identity, address lifecycle, and consumer policy.

## 10.4 Routing to experts and models

Sparse models route tokens or representations to a subset of parameters [35, 36]. QCSA can route semantic objects or expressions instead of only surface tokens. A causal-mechanism facet might select a simulation expert; a proof-obligation facet might select a theorem prover; a policy facet might require a safety critic.

The router still learns from end-to-end performance, but it emits a semantic route receipt. Load balancing remains a physical objective handled by translation, not by mutating concept identity.

## 10.5 Routing to tools and authority

Tool selection is not merely semantic similarity. It requires capability, permission, effect, data sensitivity, and approval. The translator intersects the SAC's semantic content with a capability and policy graph. An alias, embedding neighbor, or address prefix cannot grant authority.

For example, resolving “delete this project” to a `deletion` concept does not authorize deletion. The route plan must bind the target artifact identity, user authority, scope, confirmation policy, reversible or irreversible effect, and audit requirements.

## 10.6 Routing to generation

For output, the translator selects a semantic planner, language or modality decoder, style adapter, safety constraints, and verification path. A multilingual system can keep the SOID and semantic plan fixed while choosing a language-specific realization route.

## 10.7 Physical remapping without semantic migration

Hardware changes should normally alter only the route translation tables. Moving a memory shard, replacing an expert, or changing a decoder does not require a new semantic atlas epoch. This isolation reduces blast radius and enables rollback.

# 11. Compositional representation and semantic-first generation

## 11.1 Inherited deltas plus residuals

Hierarchical representations can share parameters along paths. A simple formulation constructs an object's representation from:

```text
stable identity core
+ selected facet path deltas
+ graph messages
+ context-specific residual
```

This can improve parameter sharing for rare objects and permit coarse-to-fine access. It also makes the residual explicit: the system does not claim that ancestry exhausts the object's meaning.

## 11.2 Why leaves are not enough

The space of possible meanings is combinatorial. Creating a permanent leaf for every event, quantified statement, novel tool plan, or compositional phrase is impossible and undesirable. QCSA combines stable objects through typed semantic expressions.

An expression can represent:

- `DOG` modified by `RED` and `SMALL`;
- an event with agent, patient, instrument, location, and time;
- a conditional policy;
- a mathematical proposition;
- a plan with dependencies and constraints;
- a claim linked to evidence and uncertainty.

Frequently reused expressions may be promoted to durable semantic objects, but promotion is an optimization and governance decision, not a requirement for reasoning.

## 11.3 Semantic-first generation

A maximal QCSA system does not jump directly from prompt tokens to output tokens. It performs a governed coarse-to-fine process:

1. resolve input occurrences into objects and expressions;
2. form a task and communicative-intent representation;
3. construct or retrieve a semantic plan;
4. refine uncertain concepts through questions or evidence;
5. bind claims, sources, authority, and residuals;
6. compile the semantic plan to a language or modality route;
7. realize the output;
8. round-trip the output through the resolver;
9. compare intended and recovered semantic commitments;
10. repair, qualify, or abstain if the mismatch exceeds tolerance.

Hierarchical diffusion models provide evidence that coarse-to-fine semantic refinement can be integrated into generation [29, 30]. QCSA extends the idea from vocabulary levels to a typed semantic plan and lifecycle-aware address system.

## 11.4 Round-trip semantic validation

Surface fluency is not semantic preservation. After generation, the system re-resolves the output and compares:

- object identities;
- role assignments;
- negation, modality, quantity, and time;
- claim support and citation bindings;
- authority and permitted-use constraints;
- omitted residuals and qualifications.

This is a translation-validation pattern: it cannot prove open-domain meaning, but it can catch a class of structural losses before release.

## 11.5 Coarse-to-fine decoding without serial address bottlenecks

A long address need not be generated one symbol at a time. Independent facets can be predicted in parallel; local refinement can occur only where uncertainty remains; valid combinations can be constrained by the hypergraph; and a final decoder can use the full posterior rather than one greedy path. This avoids making semantic addressing another slow autoregressive sequence.

# 12. Learning, consolidation, and migration

## 12.1 Three timescales

QCSA separates learning into three timescales.

### Fast: contextual resolution and routing

For each task, the system computes posteriors, selects facets, asks questions, and produces route plans. These decisions are ephemeral and logged.

### Medium: model and codebook adaptation

Encoders, discriminators, and address codebooks learn from outcomes. Soft routing and exploration prevent premature collapse. Changes remain in a candidate atlas until evaluated.

### Slow: governed atlas release

A new atlas epoch is published only after stability, calibration, migration, security, and consumer tests. Stable identity records remain independent.

## 12.2 Bootstrap sources

An atlas can be initialized from several signals:

- multilingual and multimodal embeddings;
- curated ontologies and taxonomies;
- knowledge-graph relations;
- morphology, syntax, and surface structure;
- retrieval and co-use patterns;
- tool and workflow traces;
- human distinctions and corrections;
- causal or simulation structure;
- policy and authority classifications.

No source is treated as ground truth by default. Curated structure can seed a facet; learned data can propose revisions; evidence and authority determine adoption.

## 12.3 Alternating optimization

A practical training program can alternate among:

1. resolver and grounding updates;
2. graph-relation representation updates;
3. soft atlas partition updates;
4. task-conditioned routing updates;
5. question-policy updates;
6. codebook balance and calibration updates;
7. migration and compatibility evaluation.

End-to-end gradients are useful but not sufficient. DIGER's codebook-collapse findings illustrate the risk of directly coupling task gradients to discrete identifiers without exploration and balancing [31]. QCSA therefore combines differentiable soft assignments with explicit utilization, stability, and lifecycle losses.

## 12.4 Objective separation and Pareto release

A single tree cannot jointly optimize semantic purity, retrieval quality, question count, memory balance, output speed, route stability, and policy clarity. The atlas builder should expose a Pareto frontier rather than hide tradeoffs inside one loss. A release record should state which objectives improved, regressed, or remained unmeasured.

## 12.5 Migration process

An atlas release follows a controlled process:

1. freeze the candidate epoch;
2. generate object-level old-to-new address maps;
3. detect collisions, splits, merges, and orphaned paths;
4. replay representative workloads and historical receipts;
5. test old-address resolution and typed failures;
6. shadow-run new routing without effects;
7. compare calibration, utility, load, and safety metrics;
8. approve, stage, or reject the epoch;
9. retain rollback and dual-resolution windows;
10. expire compatibility only under an explicit policy.

## 12.6 Identity-preserving split and merge

When a semantic distinction changes, the atlas may reclassify objects without changing SOIDs. When the underlying object model itself changes, registry operations are required.

- **Readdress:** same object, new view or path.
- **Merge:** two SOIDs become one canonical object with retained aliases and history.
- **Split:** one SOID becomes several, with the original preserved as ambiguous or deprecated.

Conflating these operations is a major source of silent semantic drift.

## 12.7 Continual learning and catastrophic semantic drift

Continual learning can improve the resolver while destabilizing the atlas. QCSA measures:

- address churn per object and facet;
- neighborhood preservation;
- old-query compatibility;
- route-plan divergence;
- branch utilization shift;
- calibration drift;
- migration burden on memories and artifacts.

High churn is not necessarily wrong, but it must be justified by utility and evidence. Stable concepts should not rotate through addresses merely because an embedding model changed.

# 13. Multilingual and multimodal grounding

## 13.1 The shared layer belongs above the surface codec

A universal byte layer is valuable because it is lossless and script agnostic. Byte- and character-level models demonstrate that useful language modeling does not require a fixed subword vocabulary [16, 17]. But the byte sequence for `dog` does not structurally resemble the byte sequence for `狗`, `perro`, or an image of a dog. Unicode is an interchange standard, not a semantic ontology.

QCSA therefore uses a layered pipeline:

```text
exact surface or sensor representation
        -> language/modality-specific structural features
        -> contextual grounding and disambiguation
        -> shared semantic object or expression posterior
```

The shared layer begins only after contextual resolution.

## 13.2 Language-specific evidence remains useful

English morphology, Chinese glyph and pinyin features, Arabic root-pattern structure, agglutinative morphology, sign-language motion, and domain-specific notation all provide useful evidence. ChineseBERT's use of glyph and pinyin information is one example of script-specific structure improving learned representations [18]. QCSA preserves those features in grounding encoders and provenance; it does not force them into one cross-language tree.

## 13.3 Cross-lingual identity is probabilistic

Translation equivalents do not always have identical extension, connotation, register, legal meaning, or cultural role. Multilingual models exhibit partial alignment, but alignment can vary by language pair, script, and concept type [19, 20].

A cross-lingual SAC can therefore distinguish:

- exact or near-exact identity;
- broader or narrower relation;
- context-dependent translation;
- culturally specific concept;
- lexical gap;
- uncertain alignment.

One shared SOID should be used only when the system has adequate evidence that the occurrences refer to the same semantic object for the intended consumer.

## 13.4 Multimodal grounding

A semantic object can be grounded in text, images, audio, action, simulation, and sensor traces. The hypergraph records those groundings separately. This enables cross-modal retrieval without claiming that all modalities produce identical internal representations.

A concept such as `door` may be grounded through:

- lexical forms across languages;
- visual shape and articulation;
- tactile and proprioceptive interaction;
- affordances such as opening, closing, blocking, or permitting passage;
- architectural and policy roles;
- specific observed instances.

Different facets can emphasize different groundings. The stable identity links them.

## 13.5 Grounding tests

Cross-lingual and multimodal identity should be tested through interventions and behavior, not only embedding proximity. Candidate tests include:

- retrieval across languages and modalities;
- role and relation preservation;
- contrastive disambiguation of near-neighbors;
- action prediction from perceptual evidence;
- translation under cultural and legal distinctions;
- round-trip realization;
- human correction and concept intervention.

# 14. Governance, security, and residual honesty

## 14.1 Semantic structure is an authority surface

A semantic address fabric influences what a system retrieves, which expert it trusts, which tool it selects, and which output it produces. It is therefore a security and governance boundary. A poisoned address can misroute evidence; a malicious alias can create privilege confusion; a silent atlas migration can change behavior at scale.

QCSA treats semantic artifacts with the same discipline applied to code, policies, and model releases.

## 14.2 Semantic Address Certificate

A SAC is the core use contract. A minimal certificate includes:

```yaml
certificate_id: sac:...
subject:
  soid: soid:...
  occurrence_or_expression: ...
context_ref: ...
task_ref: ...
atlas_epoch: ...
facets:
  - facet_id: ontology
    paths:
      - codes: [12, 4, 9, 2]
        probability: 0.83
      - codes: [12, 7, 1]
        probability: 0.12
    termination_reason: adequate_for_consumer
confidence:
  posterior_entropy: ...
  calibration_class: ...
provenance: [...]
grounding_refs: [...]
residuals: [...]
permitted_uses: [...]
authority_ceiling: ...
validity:
  issued_at: ...
  expires_at: ...
  revalidation_trigger: ...
migration_refs: [...]
integrity:
  digest: ...
  signature: ...
```

The certificate can be compact on the hot path while resolving to a fuller record for audit.

## 14.3 Capability separation

Semantic resolution never grants authority. The route translator must independently check capability and policy. This prevents attacks in which an adversary induces the model to classify an operation under a benign address to bypass controls.

A tool route should bind:

- authenticated actor and delegation chain;
- target object identity;
- operation and scope;
- data sensitivity;
- reversibility and effect class;
- required approvals;
- policy version;
- execution receipt.

## 14.4 Provenance and taint propagation

Addresses derived from untrusted sources carry taint or source labels. Downstream representations and generated claims preserve the influence chain. A high-confidence semantic classification from an untrusted source may be useful for exploration but insufficient for a consequential claim or action.

## 14.5 Atlas poisoning and adversarial examples

Attackers may try to:

- cluster malicious objects near trusted concepts;
- create aliases that collide with privileged objects;
- manipulate usage data to shift route codes;
- exploit boundary instability;
- induce branch overload or denial of service;
- infer sensitive information from route patterns;
- cause semantic and physical route disagreement.

Mitigations include signed training manifests, adversarial holdouts, source weighting, anomaly detection, branch-level access controls, rate limits, privacy-preserving telemetry, shadow evaluation, and immutable migration logs.

## 14.6 Residual honesty

A semantic address compresses. It necessarily omits distinctions. The system must record what remains unresolved and what a consumer would need to recover or verify.

Examples of residuals include:

- unresolved sense alternatives;
- missing temporal scope;
- uncertain cross-lingual equivalence;
- unverified causal relation;
- boundary proximity in a codebook;
- omitted graph neighborhood;
- stale atlas epoch;
- lack of authority for a requested action;
- inability to reconstruct the exact surface form.

A clean path without these residuals can be more misleading than a flat ID.

## 14.7 Privacy

Semantic addresses can reveal sensitive traits even when raw data is hidden. A policy facet, medical facet, or behavioral route may be highly identifying. QCSA therefore requires data minimization, facet-level access control, private query mechanisms where appropriate, retention limits, and audit of inference from address patterns.

# 15. Failure modes and mitigations

| Failure mode | Mechanism | Required mitigation |
|---|---|---|
| Ontological capture | one hierarchy becomes the presumed truth | plural facets, disputed relations, consumer-scoped adequacy |
| Early route error | a wrong high-level branch propagates | soft routing, beams, backtracking, cross-facet checks |
| Codebook collapse | few codes absorb most objects | exploration, utilization loss, capacity controls, delayed hardening |
| Identifier collision | distinct objects share an inadequate code | stable SOID, discriminative residual, ambiguity tests |
| Address drift | re-training silently changes meaning | atlas epochs, migration maps, compatibility and rollback |
| Polysemy collapse | one surface form receives one address | contextual occurrence resolution and sense-specific SOIDs |
| Concept explosion | every composition becomes a leaf | typed concept expressions and promotion policy |
| Load imbalance | semantic clusters overload resources | separate physical translation and dynamic sharding |
| Semantic laundering | a graph path appears to prove a claim | evidence/belief separation and authority ceilings |
| Alias privilege escalation | a name or neighbor inherits authority | capability checks on stable target identity |
| Route leakage | access paths reveal sensitive traits | facet access control, privacy budgets, telemetry minimization |
| Adversarial atlas poisoning | manipulated data shifts partitions | signed data lineage, robust training, shadow releases |
| Overcompression | short paths hide important distinctions | residual records, consumer adequacy thresholds, fallback |
| Human-question mismatch | generated wording does not match test | validate answer-to-partition mapping; allow “other/unknown” |
| Self-reorganization instability | recursive updates cause cascading drift | slow release cadence, invariant tests, staged authority |
| False interpretability | latent split receives a convenient story | separate operational, extensional, and intensional evidence |
| Graph incompleteness | absence is treated as negation | open-world semantics and explicit unknown state |
| Cross-language false equivalence | translations are merged too aggressively | relation types for exact, broader, narrower, contextual |

## 15.1 Strongest architectural objection

The strongest objection is that QCSA may move ambiguity into a complex infrastructure without improving model behavior. A richly typed address certificate can describe a wrong resolution with impressive precision. Multiple facets can multiply maintenance cost. Translation layers can add latency. Graphs can be incomplete, and learned splits can remain opaque.

This objection is valid. QCSA earns its cost only if the explicit structure improves at least one measurable frontier—quality, compute, memory, disambiguation, transfer, auditability, repair locality, or safety—without unacceptable regressions. The architecture therefore includes a falsification program rather than treating structure itself as success.

# 16. Evaluation and falsification program

The target architecture is maximal, but its claims should be tested through separable workstreams. Each workstream compares QCSA against strong flat, hierarchical, retrieval, and routing baselines under matched resources.

## 16.1 Workstream A: identity and contextual resolution

Tasks:

- word-sense disambiguation;
- entity linking and coreference;
- event and relation extraction;
- open-world entity discovery;
- concept-expression parsing;
- multilingual sense alignment.

Metrics:

- accuracy and calibrated selective risk;
- identity consistency across paraphrase and language;
- false merge and false split rates;
- novel-object detection;
- correction persistence;
- provenance completeness.

Critical ablation: stable SOID plus mutable address versus address-as-identity.

## 16.2 Workstream B: atlas quality

Compare:

- random balanced trees;
- Huffman or frequency trees;
- semantic k-means trees;
- residual-quantized IDs;
- hyperbolic or order-based indexes;
- single-facet and multi-facet QCSA atlases.

Measure:

- prefix purity and task utility;
- branch utilization;
- path length and entropy;
- boundary calibration;
- rare-object sharing;
- collision and ambiguity rate;
- robustness to perturbations;
- migration stability.

Critical ablations include branching factors 2, 4, 8, 16, 32, 128, and hardware-appropriate wider nodes; fixed versus variable depth; hard versus soft routing; and one path versus multiple paths.

## 16.3 Workstream C: active question navigation

Evaluate fixed taxonomic question order, generalized binary search, information-gain policies, expected-regret policies, and learned long-horizon policies.

Measure:

- number and cost of questions;
- user burden;
- decision error after each question;
- recovery from one wrong answer;
- calibration under noisy answers;
- privacy cost;
- rate of unnecessary clarification;
- downstream utility.

A key test is whether the question compiler asks fewer, more relevant questions than a language model prompted to “play 20 Questions.”

## 16.4 Workstream D: retrieval and memory

Compare dense retrieval, sparse retrieval, hierarchical indexes, generative retrieval, and QCSA hybrid retrieval.

Measure:

- recall and ranking quality;
- identifier ambiguity;
- latency and memory;
- cold-start and tail performance;
- update and deletion behavior;
- stable-reference preservation across reindexing;
- provenance and authority filtering;
- recovery from stale addresses.

## 16.5 Workstream E: expert and tool routing

Integrate the translation plane with sparse experts and tool registries. Compare token-level routers, embedding similarity, supervised tool selection, and QCSA semantic routing.

Measure:

- task quality at matched compute;
- expert load balance;
- route stability under paraphrase;
- permission violations;
- fallback quality;
- route interpretability;
- latency and throughput;
- blast radius under expert replacement.

## 16.6 Workstream F: semantic-first generation

Compare direct autoregressive generation, hierarchical vocabulary generation, diffusion coarse-to-fine generation, and semantic-plan-first generation.

Measure:

- semantic preservation under round trip;
- role, quantity, negation, and temporal accuracy;
- citation and claim-binding accuracy;
- multilingual realization consistency;
- output quality and latency;
- repair locality;
- frequency of required fallback to direct generation.

## 16.7 Workstream G: governance and migration

Simulate atlas updates, object merges and splits, physical relocation, adversarial aliases, and policy changes.

Measure:

- old-address resolution correctness;
- silent semantic misrouting rate;
- migration coverage;
- rollback success;
- audit completeness;
- unauthorized capability activation;
- residual preservation;
- operational cost of maintaining epochs.

## 16.8 Required baselines and ablations

At minimum, experiments should include:

1. flat IDs with full softmax or dense lookup;
2. random balanced tree;
3. frequency or Huffman tree;
4. one semantic tree;
5. residual-quantized semantic ID;
6. multi-view identifiers without stable identity indirection;
7. QCSA without active questions;
8. QCSA without physical translation;
9. QCSA without soft routing;
10. QCSA without migration governance;
11. full QCSA.

## 16.9 Success criteria

QCSA should not be declared successful because its diagrams are coherent. It must achieve at least one meaningful Pareto improvement:

- better task quality at matched compute;
- lower compute or memory at matched quality;
- better calibrated disambiguation;
- better rare-object or cold-start generalization;
- better multilingual or multimodal transfer;
- lower repair and update blast radius;
- stronger auditability or policy compliance with bounded overhead.

## 16.10 Falsification criteria

The research program should reject or narrow the architecture if:

- learned addresses are no better than random or frequency trees after matched tuning;
- multiple facets add cost without utility;
- question policies do not outperform direct inference or simple clarification heuristics;
- identity-address indirection does not reduce migration errors;
- semantic routing does not improve quality, compute, or governance;
- address certificates create documentation overhead without preventing failures;
- semantic-first generation consistently loses quality or latency without compensating benefits.

# 17. Beyond-state-of-the-art contribution boundary

## 17.1 What is not claimed as novel

The following components have clear precedent and are not claimed as inventions of this paper:

- hierarchical softmax and tree output prediction [2-4];
- error-correcting output codes and binary code prediction [5, 6];
- vector and residual quantization [7, 8, 25];
- hierarchical and hyperbolic representation learning [10-13];
- active learning and generalized binary search [14, 15];
- token-free and subcharacter modeling [16-18];
- generative retrieval and semantic IDs [21-26, 31-34];
- tree tokenization and hierarchical diffusion generation [27-30];
- sparse attention and expert routing [35, 36];
- retrieval-augmented external memory [37, 38];
- concept bottlenecks and intervention [39];
- knowledge graphs [40].

## 17.2 The proposed contribution

QCSA's potentially original contribution is the integrated systems abstraction:

> **A governed AI system gives every durable semantic object a stable identity; represents it through multiple task-scoped, versioned, probabilistic semantic virtual addresses over an evidence-bearing hypergraph; resolves uncertainty through a cost- and risk-aware question compiler; and translates semantic addresses into physical routes for memory, experts, tools, permissions, and generation while preserving migration, provenance, authority, and residual uncertainty.**

The design advances beyond the surveyed state of the art in eight linked ways.

### 1. Identity-address-route separation

Current semantic-ID systems commonly use the learned code as the item's identifier and decoder target. QCSA inserts two layers of indirection so representations and hardware can change without redefining the object.

### 2. Multi-facet address atlas over a graph

Rather than one tree or a few text identifier views, QCSA compiles many declared hierarchical indexes over a typed temporal hypergraph and lets context select their weights.

### 3. Questions as a first-class semantic decoder

The system treats active evidence acquisition as the procedural counterpart to stored addresses, with cost, risk, privacy, and human burden in the objective.

### 4. Semantic Address Certificates

Addresses carry provenance, confidence, residuals, authority ceilings, permitted uses, validity, and migration state. They are governed leases, not bare code tuples.

### 5. Unified semantic routing

The same address substrate can route memory, experts, tools, approval, and generation. Physical translation remains separate so hardware and security can optimize independently.

### 6. Lifecycle-safe self-reorganization

Atlas learning is paired with epoch releases, migration invariants, old-address resolution, shadow evaluation, and rollback.

### 7. Open-world compositional semantics

The architecture supports provisional objects and typed concept expressions instead of requiring every possible meaning to be a leaf.

### 8. Semantic-first generation with round-trip validation

Generation begins from semantic objects, relations, and commitments, then realizes and re-resolves the output to detect structural loss.

## 17.3 Novelty discipline

This paper's literature review is broad but not an exhaustive patent or publication search. The contribution should therefore be described as a **proposed architecture and synthesis** until independent prior-art review and empirical evaluation establish narrower novelty and utility claims.

# 18. Integration surfaces for advanced AI systems

QCSA is most valuable as a cross-cutting substrate rather than an isolated model head.

## 18.1 Planning and semantic intermediate representation

Plan nodes, requirements, constraints, claims, and repair targets can receive stable semantic identities. Their addresses support dependency grouping, specialist routing, and localized repair. The physical translator lowers semantic obligations into executable jobs while preserving source identity and validators.

## 18.2 Context and memory

Context requests can specify SOIDs, facet patterns, atlas epochs, authority ceilings, and adequacy targets. Returned packets carry SACs and bounded graph neighborhoods rather than anonymous prompt text. Memory reindexing does not break stable references.

## 18.3 Claims and evidence

Propositions, evidence, sources, and support states remain distinct semantic objects. Addresses accelerate retrieval and comparison, while certificates prevent a semantic match from becoming automatic evidential authority.

## 18.4 Specialist routing

Semantic facets can select reasoning, simulation, proof, coding, policy, or domain experts. Route translation handles load, cost, hardware, and permissions separately.

## 18.5 Tool use and execution

Tool descriptions, capabilities, effects, preconditions, and policies become addressable. The question compiler can acquire missing parameters; the translator emits capability-checked route plans and execution receipts.

## 18.6 Compression and compact generation

Shared path deltas and semantic plans can reduce repeated representation, but every compact object carries residual, reconstruction, verification, and fallback obligations. The semantic address is a compact lease, not proof of adequacy.

## 18.7 Recursive improvement

A self-improving system may propose new facets, partitions, questions, or translations. It may not silently mutate stable identity or activate a new atlas epoch. Improvement proposals must pass migration, utility, security, and rollback gates before gaining authority.

## 18.8 Inter-stack exchange

Different systems may use different atlases. They can exchange stable namespace-qualified identities, signed address certificates, and mapping manifests. Cross-stack translation should preserve uncertainty rather than pretending that one ontology is universal.

# 19. Limitations and non-claims

QCSA does not solve semantics by naming it. Several limitations remain fundamental.

- **Grounding remains hard.** Stable IDs can preserve a wrong interpretation.
- **Open-world completeness is impossible to certify generally.** The graph will be partial and contested.
- **Learned partitions may be opaque.** Operational audit does not guarantee intuitive human meaning.
- **Multi-facet systems are expensive.** Training, storage, migration, and governance overhead may outweigh benefits in some workloads.
- **Active questions can burden users.** A poor question policy may interrupt rather than help.
- **Address sharing can create correlated errors.** Inherited deltas may spread a mistaken abstraction.
- **Semantic-first generation may add latency.** Round-trip validation and repair are not free.
- **Stable identity is a governance commitment.** Merge and split decisions can remain disputed.
- **Security remains adversarial.** Signed certificates do not guarantee clean training data or correct policies.
- **No implementation is presented.** All performance and safety benefits remain hypotheses.

The paper specifically does **not** claim:

- that binary trees are intrinsically intelligent;
- that Unicode bits encode meaning;
- that one universal ontology exists;
- that a semantic address is a proof of truth;
- that QCSA should immediately replace modern tokenizers;
- that hierarchical codes always outperform flat outputs;
- that interpretability or safety follows automatically from structure;
- that the architecture has been benchmarked or validated.

# 20. Conclusion

The 20-Questions intuition identifies a deep property of intelligence: efficient cognition often depends on choosing distinctions that reduce uncertainty rather than comparing every possibility independently. The semantic-address intuition identifies the complementary property: once a distinction has been learned, it should become reusable structure rather than disappear into an arbitrary ID.

Taken alone, each idea is incomplete. A rigid question tree is brittle. A single semantic tree is reductive. A binary code over Unicode is semantically arbitrary. A learned semantic ID becomes unstable when it is also used as identity. A knowledge graph can be expressive but expensive to navigate. A sparse router can be efficient but semantically opaque.

Question-Compiled Semantic Addressing combines the useful parts while separating conflicting roles.

- Stable identity preserves reference.
- A typed evidence-bearing hypergraph represents plural relations and uncertainty.
- Multi-facet semantic virtual addresses provide compact, learned, coarse-to-fine indexes.
- A question compiler actively resolves what the current evidence cannot.
- Semantic Address Certificates bind address use to context, provenance, confidence, authority, and lifecycle.
- A translation layer compiles semantic intent into physical routes for memory, experts, tools, and generation.
- Migration governance allows the organization to improve without breaking history.

The final logical conclusion is therefore larger than tree tokenization and more disciplined than a universal semantic tree:

> **Advanced AI should treat semantic addressability as a governed systems primitive. Identity should be stable, addresses plural and learned, questions adaptive, knowledge relational, and execution routes compiled.**

A concise form of the architecture is:

> **Store by identity. Index by address. Find by questions. Reason over a graph. Execute by compiled routes.**

---

# Appendix A. Normative record sketches

## A.1 Semantic Object Record

```yaml
soid: soid:namespace:opaque-id
kind: concept | entity | event | relation | proposition | expression | document | memory | tool | policy | obligation
canonical_label: ...
definition:
  text: ...
  scope: ...
aliases:
  - form: ...
    language: ...
    relation: exact | synonym | broader | narrower | contextual | deprecated
lifecycle:
  state: provisional | active | disputed | deprecated | merged | split | revoked
  created_at: ...
  supersedes: [...]
  superseded_by: [...]
groundings: [...]
relations: [...]
propositions: [...]
provenance: [...]
authority: ...
atlas_links: [...]
integrity:
  digest: ...
  signature: ...
```

## A.2 Semantic Address Certificate

```yaml
sac_id: sac:...
subject_soid: soid:...
occurrence_ref: ...
expression_ref: ...
context_ref: ...
task_ref: ...
consumer_class: ...
atlas_epoch: atlas:...
facet_addresses:
  - facet_id: ...
    facet_version: ...
    weight: ...
    candidate_paths:
      - codes: [...]
        probability: ...
        labels_or_probes: [...]
    termination_reason: ...
confidence:
  entropy: ...
  calibration_bin: ...
  boundary_score: ...
consistency:
  cross_facet_score: ...
  violated_constraints: [...]
provenance: [...]
grounding_refs: [...]
residuals: [...]
permitted_uses: [...]
prohibited_uses: [...]
authority_ceiling: ...
validity:
  issued_at: ...
  expires_at: ...
  revalidate_on: [...]
migration_refs: [...]
integrity:
  digest: ...
  signature: ...
```

## A.3 Address Migration Record

```yaml
migration_id: migration:...
from_epoch: atlas:e
to_epoch: atlas:e+1
subject_soid: soid:...
old_addresses: [...]
new_addresses: [...]
operation: readdress | merge-view | split-view | deprecate | unresolved
compatibility:
  old_resolves_to_same_soid: true | false
  consumer_tests: [...]
  known_breaks: [...]
reason: ...
evidence: [...]
approvals: [...]
rollback_ref: ...
integrity: ...
```

# Appendix B. Reference inference protocol

```text
function QCSA_RESOLVE_AND_ROUTE(input, context, task, consumer, policy):
    occurrences = SURFACE_GATEWAY.parse(input)
    posterior = RESOLVER.resolve(occurrences, context, task)

    while not adequate(posterior, consumer, policy):
        candidates = ATLAS.propose_tests(posterior, task, consumer)
        q = QUESTION_COMPILER.select(candidates,
                                     information_value=True,
                                     cost_budget=policy.cost_budget,
                                     risk_budget=policy.risk_budget,
                                     privacy_budget=policy.privacy_budget)
        if q is NONE:
            return typed_fault("insufficient semantic adequacy", posterior)
        evidence = EXECUTE_TEST_OR_ASK(q)
        posterior = RESOLVER.update(posterior, evidence)

    subjects = REGISTRY.bind_or_create(posterior, policy)
    addresses = ATLAS.issue_addresses(subjects, context, task, consumer)
    sac = CERTIFICATE_SERVICE.issue(subjects, addresses,
                                    provenance=posterior.provenance,
                                    residuals=posterior.residuals,
                                    policy=policy)
    route_plan = TRANSLATOR.compile(sac, task, consumer, policy, RESOURCES.state())
    receipt = EXECUTOR.run(route_plan)
    return {subjects, sac, route_plan, receipt}
```

# Appendix C. Research artifact set

A full implementation program should produce at least the following inspectable artifacts:

1. semantic object schema and registry implementation;
2. typed hypergraph schema with evidence and lifecycle state;
3. atlas manifest, facet contracts, and epoch package;
4. learned codebooks and topology files;
5. resolver calibration report;
6. question-policy trace corpus;
7. Semantic Address Certificate schema and validators;
8. semantic-to-physical route-plan schema;
9. migration map and compatibility harness;
10. adversarial alias and poisoning suite;
11. multilingual and multimodal grounding suite;
12. semantic round-trip generation validator;
13. resource and latency ledger;
14. residual and fallback ledger;
15. benchmark report with baselines and ablations;
16. rollback and disaster-recovery exercise.

# Appendix D. Glossary

**Address atlas.** A versioned family of hierarchical semantic index views over the durable hypergraph.

**Address epoch.** An immutable released version of one or more atlas facets.

**Concept expression.** A typed composition of semantic objects, roles, operators, time, quantity, and modality.

**Facet.** A declared semantic view optimized for a consumer or relation family.

**Physical route plan.** A task-specific executable plan selecting memories, experts, tools, policies, decoders, and verifiers.

**Question compiler.** The policy that selects the next evidence-acquisition operation under uncertainty, cost, risk, and privacy.

**Semantic Address Certificate (SAC).** A governed lease binding stable identity to contextual addresses, confidence, provenance, permitted use, authority, lifecycle, and residuals.

**Semantic Object ID (SOID).** A stable opaque identifier for a durable concept, entity, event, proposition, expression, memory, tool, policy, or obligation.

**Semantic virtual address (SVA).** A versioned path or soft path distribution in one atlas facet; it is not identity or physical location.

**Typed evidence-bearing hypergraph.** The durable relational substrate containing objects, typed relations, events, claims, evidence, provenance, time, and lifecycle state.

# References

[1] C. E. Shannon, “A Mathematical Theory of Communication,” *Bell System Technical Journal*, vol. 27, 1948.

[2] F. Morin and Y. Bengio, “Hierarchical Probabilistic Neural Network Language Model,” *AISTATS*, 2005.

[3] A. Mnih and G. E. Hinton, “A Scalable Hierarchical Distributed Language Model,” *Advances in Neural Information Processing Systems*, 2009.

[4] E. Grave, A. Joulin, M. Cissé, D. Grangier, and H. Jégou, “Efficient Softmax Approximation for GPUs,” *ICML*, 2017. arXiv:1609.04309.

[5] T. G. Dietterich and G. Bakiri, “Solving Multiclass Learning Problems via Error-Correcting Output Codes,” *Journal of Artificial Intelligence Research*, vol. 2, 1995. arXiv:cs/9501101.

[6] Y. Oda, P. Arthur, G. Neubig, K. Yoshino, and S. Nakamura, “Neural Machine Translation via Binary Code Prediction,” *ACL*, 2017. arXiv:1704.06918.

[7] A. van den Oord, O. Vinyals, and K. Kavukcuoglu, “Neural Discrete Representation Learning,” *NeurIPS*, 2017. arXiv:1711.00937.

[8] H. Jégou, M. Douze, and C. Schmid, “Product Quantization for Nearest Neighbor Search,” *IEEE Transactions on Pattern Analysis and Machine Intelligence*, vol. 33, no. 1, 2011.

[9] A. Kusupati et al., “Matryoshka Representation Learning,” *NeurIPS*, 2022. arXiv:2205.13147.

[10] I. Vendrov, R. Kiros, S. Fidler, and R. Urtasun, “Order-Embeddings of Images and Language,” *ICLR*, 2016. arXiv:1511.06361.

[11] M. Nickel and D. Kiela, “Poincaré Embeddings for Learning Hierarchical Representations,” *NeurIPS*, 2017. arXiv:1705.08039.

[12] O.-E. Ganea, G. Bécigneul, and T. Hofmann, “Hyperbolic Entailment Cones for Learning Hierarchical Embeddings,” *ICML*, 2018. arXiv:1804.01882.

[13] Y. Bai et al., “Modeling Heterogeneous Hierarchies with Relation-Specific Hyperbolic Cones,” *NeurIPS*, 2021. arXiv:2110.14923.

[14] R. D. Nowak, “The Geometry of Generalized Binary Search,” *IEEE Transactions on Information Theory*, 2011. arXiv:0910.4397.

[15] N. Houlsby, F. Huszár, Z. Ghahramani, and M. Lengyel, “Bayesian Active Learning for Classification and Preference Learning,” 2011. arXiv:1112.5745.

[16] J. H. Clark et al., “CANINE: Pre-training an Efficient Tokenization-Free Encoder for Language Representation,” *Transactions of the ACL*, 2022. arXiv:2103.06874.

[17] L. Xue et al., “ByT5: Towards a Token-Free Future with Pre-trained Byte-to-Byte Models,” *Transactions of the ACL*, 2022. arXiv:2105.13626.

[18] Z. Sun et al., “ChineseBERT: Chinese Pretraining Enhanced by Glyph and Pinyin Information,” *ACL-IJCNLP*, 2021. arXiv:2106.16038.

[19] S. Cao, N. Kitaev, and D. Klein, “Multilingual Alignment of Contextual Word Representations,” *ICLR*, 2020. arXiv:2002.03518.

[20] X. Peng and A. Søgaard, “Concept Space Alignment in Multilingual Large Language Models,” 2024. arXiv:2410.01079.

[21] Y. Tay et al., “Transformer Memory as a Differentiable Search Index,” *NeurIPS*, 2022. arXiv:2202.06991.

[22] Y. Li, N. Yang, L. Wang, F. Wei, and W. Li, “Multiview Identifiers Enhanced Generative Retrieval,” *ACL*, 2023. arXiv:2305.16675.

[23] S. Rajput et al., “Recommender Systems with Generative Retrieval,” *NeurIPS*, 2023. arXiv:2305.05065.

[24] Z. Si et al., “Generative Retrieval with Semantic Tree-Structured Item Identifiers via Contrastive Learning,” 2023. arXiv:2309.13375.

[25] Y. Hou, Z. He, J. McAuley, and W. X. Zhao, “Learning Vector-Quantized Item Representation for Transferable Sequential Recommenders,” 2022. arXiv:2210.12316.

[26] Y. Hou et al., “Generating Long Semantic IDs in Parallel for Recommendation,” *KDD*, 2025. arXiv:2506.05781.

[27] Q. Zhu, X. Hu, P. Ji, W. Wu, and K. Tu, “Unsupervised Morphological Tree Tokenizer,” *Findings of ACL*, 2025. arXiv:2406.15245.

[28] C. W. Schmidt et al., “Tokenization with Split Trees,” 2026. arXiv:2605.22705.

[29] C. Zhou et al., “Next Semantic Scale Prediction via Hierarchical Diffusion Language Models,” *NeurIPS*, 2025. arXiv:2510.08632.

[30] Z. Wu, H. Yang, J. Dong, and V. Tarokh, “Rethinking Token Prediction: Tree-Structured Diffusion Language Model,” 2026. arXiv:2604.03537.

[31] J. Fu et al., “Differentiable Semantic ID for Generative Recommendation,” accepted to *SIGIR*, 2026. arXiv:2601.19711.

[32] Y. Liang et al., “Rethinking Generative Recommender Tokenizer: Recsys-Native Encoding and Semantic Quantization Beyond LLMs,” 2026. arXiv:2602.02338.

[33] W. Cheng et al., “CapsID: Soft-Routed Variable-Length Semantic IDs for Generative Recommendation,” 2026. arXiv:2605.05096.

[34] A. Bracher and S. Vakulenko, “Generative Retrieval Overcomes Limitations of Dense Retrieval but Struggles with Identifier Ambiguity,” 2026. arXiv:2604.05764.

[35] A. Roy, M. Saffar, A. Vaswani, and D. Grangier, “Efficient Content-Based Sparse Attention with Routing Transformers,” *Transactions of the ACL*, 2021. arXiv:2003.05997.

[36] W. Fedus, B. Zoph, and N. Shazeer, “Switch Transformers: Scaling to Trillion Parameter Models with Simple and Efficient Sparsity,” *JMLR*, 2022. arXiv:2101.03961.

[37] P. Lewis et al., “Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks,” *NeurIPS*, 2020. arXiv:2005.11401.

[38] S. Borgeaud et al., “Improving Language Models by Retrieving from Trillions of Tokens,” *ICML*, 2022. arXiv:2112.04426.

[39] P. W. Koh et al., “Concept Bottleneck Models,” *ICML*, 2020. arXiv:2007.04612.

[40] A. Hogan et al., “Knowledge Graphs,” *ACM Computing Surveys*, vol. 54, no. 4, 2021. doi:10.1145/3447772.

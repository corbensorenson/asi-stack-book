---
title: "Semantic and Epistemic State for Long-Lived AI Agents"
subtitle: "Identity, Context, Evidence, Belief Revision, and Semantic Migration"
author: "Corben Sorenson"
date: "2026-08-15"
document-class: "research-paper"
series: "Governed Intelligence"
series-order: 2
bibliography: ../references/references.bib
link-citations: true
toc: true
number-sections: true
abstract: |
  Long-lived AI agents require more than storage and retrieval. They must preserve what their terms mean across changing models and ontologies, distinguish source evidence from derived representations, maintain defeasible claims, assemble task-specific context without erasing omissions, and revise dependent commitments when concepts, sources, evaluators, or world state change. Existing work provides powerful components: retrieval-augmented generation, tiered agent memory, knowledge graphs, provenance standards, belief revision, truth-maintenance systems, and claim-evidence interfaces. Yet agent architectures often collapse several different states into one memory surface. A passage is retrieved and treated as believed; an embedding becomes a semantic identity; a summary inherits the authority of its source; a proof is read as evidence for an unstated interpretation; or a changed ontology silently retargets old plans. This paper presents a semantic and epistemic state architecture built around noninheritance among six projections: source state, semantic state, storage state, active-context state, epistemic commitment, and action authority. Persistent semantic identifiers refer to concept lineages rather than names, embeddings, or locations. Immutable concept versions and explicit contexts preserve historical interpretation while allowing plural theories, branches, and contested meanings. Evidence records bind provenance, valid time, observation time, scope, rights, transformations, and uncertainty. Claims have stable identity and typed justification artifacts—formal proof, source-bound interpretation, procedural replay, empirical evidence, monitoring evidence, or speculation—each with a distinct maximum inference. Belief revision preserves append-only history while allowing expansion, contraction, contradiction, and partial inconsistency. Context assembly is formulated as a governed compilation problem with mandatory obligations, explicit omissions, exact-source escalation, snapshot coherence, privacy constraints, and typed insufficiency. Semantic migration computes impact cones over dependent claims, memories, plans, and interfaces. The architecture is evaluated through context-adequacy, evidence-laundering, semantic-migration, and evaluator-dependence benchmarks. It is not a claim that a canonical ontology can capture open-world meaning or that provenance makes evidence true. Its contribution is a testable separation of the states that a persistent agent must otherwise risk confusing.
keywords:
  - agent memory
  - semantic identity
  - provenance
  - belief revision
  - context management
  - knowledge representation
  - claim evidence
  - ontology evolution
---

# Introduction: Semantic Continuity Is Not Memory Size

A long-lived agent can remember a great deal and still lose track of what its memories mean.

Suppose an assistant stores the statement, “The project’s release candidate is approved.” Months later the project changes names, the approval applies only to a draft artifact, the approving reviewer’s authority expires, and the underlying release policy is revised. A retrieval system may still find the sentence. A vector index may rank it highly. A summarizer may compress it into “release approved.” None of those operations establishes that the old statement remains true, that the current artifact is the same object, that the reviewer’s decision applies to the present use, or that the sentence may authorize publication.

The problem is not simply stale memory. It is the collapse of different kinds of state.

- The **source** may still exist as a historical record.
- The **semantic object** may have changed version or split into several objects.
- A **representation** may omit limitations that remain present in the source.
- The system’s current **epistemic commitment** may have been narrowed or defeated.
- A task-specific **context packet** may include the statement for explanation but not for decision.
- **Action authority** may remain absent even when the proposition is well supported.

Modern research provides many pieces of the solution. Retrieval-augmented generation connects language models to external corpora [@lewis2020rag; @guu2020realm; @borgeaud2022retro]. MemGPT and cognitive architectures for language agents treat context as a tiered or actively managed resource [@packer2023memgpt; @sumers2023coala]. Belief revision and truth-maintenance systems describe how commitments change under new information [@agm1985; @doyle1979tms; @gardenfors1988knowledge]. PROV-O provides a standard vocabulary for provenance [@w3c2013provo]. Model Cards and Datasheets make scope and lineage visible in model and dataset reporting [@mitchell2019modelcards; @gebru2021datasheets]. Recent claim-evidence interfaces and evidence-ledger systems make support relations more inspectable [@chen2026evidenceledger; @martinboyle2026papertrail].

Yet these components are often integrated through an undifferentiated memory abstraction. A “memory” may be a raw event, a model-generated summary, a preference, a retrieved document, a system instruction, a belief, a task commitment, or a cached answer. Once those states share one namespace and one ranking function, an implementation detail can become an epistemic or authority transition.

This paper proposes a semantic and epistemic state architecture for persistent agents. Its central rule is:

> **Identity, representation, evidence, commitment, context, and authority are different states. No one automatically inherits the status of another.**

A name is not an identity. An embedding is not a concept. A source passage is not a belief. A proof is not the truth of its natural-language interpretation. A retrieved item is not automatically admissible context. A supported claim is not permission to act.

The architecture is designed around four needs.

First, semantic identity must survive changes to labels, representations, models, indexes, and physical location. Second, evidence and claims must retain provenance, scope, and defeaters rather than collapsing into one confidence score. Third, active context must be compiled for a particular task and consumer while preserving mandatory obligations and explicit omissions. Fourth, changes to concepts, sources, evaluators, or ontologies must propagate through dependent commitments without rewriting history.

The proposal does not assume that there is one correct global ontology. It supports plural theories, local contexts, disputed mappings, and explicit incompatibility. Nor does it claim that record structure makes semantic judgment reliable. The system can preserve a wrong interpretation perfectly. Its value must be measured against simpler retrieval, graph, and human-curation baselines.

# Scope and Standard Terminology

The paper concerns persistent AI systems that operate across multiple tasks and versions. The system may use language models, symbolic components, databases, tools, human review, or combinations of them. The architecture is independent of any one model family.

**Semantic object.** A governed referent such as a concept, entity, event type, proposition, procedure, policy, or capability whose identity is intended to persist across representations.

**Persistent semantic identifier.** A stable identifier for a semantic object or lineage. It is not derived solely from a name, embedding, location, or current description.

**Concept version.** An immutable statement of the semantic commitments associated with an object at a time. Later versions can refine, fork, deprecate, or contradict earlier versions without overwriting them.

**Representation.** A view of an object for a particular consumer or use: label, embedding, summary, exact passage, graph neighborhood, formal statement, executable schema, or other encoding.

**Source.** An artifact, observation channel, instrument, human report, database, procedure, or event from which evidence is derived.

**Evidence.** A source-bound artifact that may support, contradict, qualify, or fail to address a claim. Evidence is not identical to the source, because selection and transformation can alter what is presented.

**Claim.** A stable proposition identity with content, scope, modality, time, context, and support relations.

**Justification artifact.** The object through which a claim is supported: proof, source interpretation, procedural replay, empirical observation, monitoring record, or heuristic synthesis.

**Epistemic commitment.** The system’s governed stance toward a claim under a declared context and evidence set. Commitments are defeasible and consumer-relative.

**Context.** A task-specific admitted set of representations, obligations, and unresolved items made available to a model or other consumer.

**World branch.** A named actual, predicted, planned, simulated, counterfactual, fictional, or normative state. Branch identity prevents hypothetical content from silently entering actuality.

**Defeater.** Evidence or condition that blocks, narrows, suspends, or reverses a support relation or commitment.

**Semantic migration.** A versioned transformation of concepts, mappings, representations, or dependent artifacts after a material change.

**Authority.** Permission to create an external effect. Authority remains outside the epistemic state model except as a constraint on admissibility and use.

# Related Work and Novelty Boundary

## Retrieval and agent memory

Retrieval-augmented generation and retrieval-enhanced pretraining allow models to condition on external text rather than relying entirely on parameters [@lewis2020rag; @guu2020realm; @borgeaud2022retro]. These systems improve access to information, but retrieval success does not establish that the selected material is current, admissible, semantically sufficient, or correctly used.

MemGPT treats context management through an operating-system analogy, while CoALA proposes a broader cognitive architecture with memory and action modules [@packer2023memgpt; @sumers2023coala]. The present work builds on tiered memory but distinguishes source, semantic, storage, context, belief, and authority states. It also treats eviction, summarization, and retrieval as provenance-bearing transformations rather than only memory-management decisions.

“Lost in the Middle” demonstrates that nominal context length does not guarantee reliable use of information at all positions [@liu2023lostmiddle]. That result motivates explicit context obligations and adequacy testing rather than token-count reasoning.

## Knowledge representation and belief revision

Knowledge graphs, ontologies, and truth-maintenance systems provide explicit objects and dependencies. Doyle’s truth-maintenance system records justifications and updates dependent beliefs [@doyle1979tms]. AGM theory formalizes belief expansion, contraction, and revision [@agm1985]. The present architecture inherits their emphasis on dependency and change, but adds agent-specific representation, context admission, provenance, evaluator identity, and consumer-relative authority boundaries.

## Provenance and reporting

PROV-O describes entities, activities, and agents in provenance graphs [@w3c2013provo]. Model Cards and Datasheets document intended use, composition, and limitations [@mitchell2019modelcards; @gebru2021datasheets]. These standards improve traceability but do not themselves specify how an agent should convert provenance into a current commitment or context decision.

## Claim-evidence interfaces

Evidence-ledger adjudication pairs claims with evidence packets and support relations [@chen2026evidenceledger]. PaperTrail studies a claim-evidence interface for scholarly work and shows that increased caution does not necessarily overcome the cognitive burden of verification [@martinboyle2026papertrail]. These findings reinforce two points: claim-evidence alignment is valuable, and the presentation and review burden are part of the system rather than an afterthought.

## Precise contribution

The paper does not claim to invent retrieval, memory tiers, belief revision, provenance, ontologies, or claim-evidence matrices. It contributes their integration through a **state-separation model** and a **semantic migration lifecycle**. The architecture asks which object exists, which representation is being used, what evidence supports which exact claim, what the system is committed to under which context, and what changes when any dependency moves.

# State Separation Model

Let the persistent agent state at logical time \(t\) be

\[
\mathcal{S}_t = (\Omega_t, \Sigma_t, M_t, C_t, B_t, A_t),
\]

where:

- \(\Omega_t\) is source and event state;
- \(\Sigma_t\) is semantic identity and version state;
- \(M_t\) is storage and representation state;
- \(C_t\) is active-context state;
- \(B_t\) is epistemic commitment state;
- \(A_t\) is authority state.

The six projections can refer to one another but must not collapse.

## Source state

Source state preserves what was observed, received, or produced, along with origin, exact location, time, rights, integrity, and transformations. A source record can remain historically valid even when its content is no longer current.

## Semantic state

Semantic state identifies the object or claim being discussed and the version of its meaning. It contains relations, mappings, contexts, and migration history. Semantic state does not assert that a claim is true.

## Storage state

Storage state records where and how information is represented: raw bytes, exact passage, summary, embedding, graph node, cache, model parameter, or archived derivative. Placement and compactness are operational properties, not epistemic status.

## Active-context state

Context state records what a consumer currently receives, in what order and representation, under which snapshot, purpose, permissions, and omissions. Presence in context does not make an item believed or authoritative.

## Epistemic state

Epistemic state records claims, support relations, defeaters, uncertainty, disagreement, and current commitments. A claim can be supported but inactive for a task, contradicted but historically important, or unresolved despite repeated retrieval.

## Authority state

Authority state records permissions for effects. It can depend on claims and context but cannot be derived from them automatically. A system can know that a transaction is likely beneficial and still lack permission to execute it.

## Prohibited substitutions

The architecture forbids several common substitutions:

- label equality → semantic identity;
- embedding similarity → equivalence;
- retrieval → evidence adequacy;
- source citation → entailment;
- proof check → correct interpretation;
- repeated mention → belief;
- context inclusion → action authority;
- cache hit → current validity;
- deletion from one store → global erasure.

These are not metaphysical prohibitions. They are engineering obligations to record an explicit transition whenever one state is used to justify another.

# Persistent Semantic Identity and Versioning

A persistent system needs stable reference, but stable reference does not require one timeless essence.

## Lineage and immutable versions

A semantic object has a stable lineage identifier and immutable versions:

\[
O = (id, v_1, v_2, \ldots, v_n).
\]

Each version can specify:

- object kind;
- lexical interfaces;
- constitutive or definitional constraints;
- diagnostic and prototypical features;
- relations and roles;
- context and theory;
- valid time;
- grounding methods;
- known exclusions and exceptions;
- source and governance history.

A later version does not rewrite earlier usage. Historical claims remain interpretable under the semantic basis that existed when they were made.

## Labels, embeddings, and indexes

Names and embeddings are many-to-many interfaces. One term may refer to several objects; one object may have several names; two embeddings may be close for reasons unrelated to identity. Indexes provide task-specific access paths, not canonical meaning.

The system can maintain multiple task-specific indexes over the same object lineage: ontological, causal, linguistic, functional, policy, or workload-oriented. An index entry carries its epoch and mapping to the stable identifier. An index migration must either preserve the referent or fail explicitly; silent retargeting is forbidden.

## Contexts and plural theories

Meaning can be context-dependent. The same term may have different definitions across jurisdictions, scientific theories, communities, or granularities. The architecture represents context rather than forcing premature global merge.

Mappings across contexts are typed:

- exact;
- broader or narrower;
- overlapping;
- translated;
- analogous;
- successor;
- disputed;
- incompatible.

Mappings can be directional, expiring, and consumer-specific. Interoperability does not require one ontology to dominate every other.

## Instances, situations, and worlds

Concepts should remain distinct from instances and situations. A medical diagnosis category is not a patient. A planned deployment is not an observed deployment. A fictional or counterfactual event is not actual history.

World branches name the modality of state. Crossing from planned or predicted to actual requires an observation, adoption, or authorized effect event. Model confidence does not perform that transition.

## Provisional objects and merge/split history

Open-world systems need provisional objects. When evidence is insufficient to decide whether two mentions identify the same object, the system may preserve both and record candidate mappings. Later merge or split decisions leave lineage and dependent-artifact dispositions. They do not erase the earlier ambiguity.

# Evidence, Provenance, Grounding, and Source Authority

Evidence is useful only when a consumer can tell what it is evidence of.

An evidence record can be represented as

\[
E = (s, l, x, \tau_v, \tau_o, \tau_r, m, r, u, d),
\]

where \(s\) is source identity, \(l\) location, \(x\) extract or observation, \(\tau_v\) valid time, \(\tau_o\) observation time, \(\tau_r\) record time, \(m\) method, \(r\) rights and access conditions, \(u\) uncertainty, and \(d\) derivation history.

## Source and evidence packet

The source is the broader artifact or channel. An evidence packet is a selected, transformed presentation for a claim. Selection is consequential: a passage can omit an exception in the next paragraph; a table summary can hide subgroup variation; a sensor aggregate can erase a transient event.

Evidence packets therefore retain exact source references, transformation identity, omissions, and permitted uses. A summary is not decompression. If a consumer requires a distinction that the summary does not preserve, the system must retrieve a stronger representation or return insufficiency.

## Provenance is not truth

A cryptographic digest can establish byte identity. A signature can establish a signer under a key policy. A provenance graph can establish a declared derivation. None establishes that the source is accurate, that the signer was competent, that the extract entails the claim, or that the evidence remains applicable.

Provenance is necessary for challenge and invalidation. It is not a substitute for epistemic evaluation.

## Grounding adapters

Evidence enters from documents, sensors, databases, simulations, proofs, human judgments, or tools. Each grounding adapter declares input domain, calibration, output semantics, known failures, qualified contexts, recency, and independence.

Several agreeing model outputs may share data, prompts, providers, and assumptions. Agreement is therefore not counted as independent evidence merely because the outputs are textually distinct.

## Source interpretation mappings

Source-bound claims often require interpretation. A regulation, policy, or scientific method does not mechanically map to one proposition. The architecture uses a versioned interpretation record containing source span, jurisdiction or domain, effective time, applicability, definitions, exceptions, assumptions, competing interpretations, reviewer identity, and allowed consumers.

A source interpretation can be well documented and still wrong. Its value is that disagreement becomes addressable rather than hidden inside a citation.

## Rights and information flow

Evidence access and evidence use are different permissions. A source may be readable for one purpose but not reusable in a public artifact, training set, or downstream decision. Context assembly and semantic migration must preserve rights, confidentiality, retention, and deletion obligations alongside epistemic state.

# Claims and Typed Justification Artifacts

A claim is not merely a sentence. It is an identity-bearing proposition under scope and context.

A claim record contains:

- stable claim identifier;
- proposition or structured content;
- semantic basis and context;
- modality and quantification;
- valid time and population;
- assumptions;
- evidence relations;
- defeaters and disagreements;
- current commitment state;
- allowed consumers and maximum inference;
- expiry and review triggers.

## Justification classes

The architecture treats justification as a sum type rather than one confidence ladder.

### Formal proof

A formal artifact can establish a statement under a named logic, theory, checker, dependencies, and assumptions. It does not establish that the formal statement matches the intended natural-language claim, that the premises describe the world, or that the result authorizes action.

### Source-bound interpretation

A source span plus an interpretation mapping can establish what a document is reasonably taken to say under a declared reading. It does not establish that the source is true or uniquely authoritative.

### Procedural replay

A deterministic or controlled procedure can reproduce an output under pinned inputs and environment. Reproducibility does not establish that the procedure answers the right question.

### Empirical evidence

An experiment or observation can support a claim under its population, instrument, design, and uncertainty. It does not automatically transfer across distributions or consumers.

### Monitoring evidence

Operational logs and outcomes can support claims about observed behavior during a period. Monitoring is conditioned on what the instrumentation can see and on the system not defeating or bypassing it.

### Speculative synthesis

A model-generated hypothesis or explanation can be useful while remaining explicitly noncommittal. It may guide retrieval or experiment without updating the active commitment state.

## Maximum inference

Each justification artifact states the strongest inference a downstream consumer may make. A unit test may support “these cases passed under this environment,” not “the system is correct.” A citation may support “this source contains this statement,” not “the statement is true.” A proof may support “the theorem checks under these assumptions,” not “deployment is safe.”

Maximum inference prevents evidence laundering: the silent promotion of a narrow result into a broader claim.

## Claim-to-surface coverage

Structured claims and rendered prose should be linked in both directions. Material prose without a claim identity becomes an unregistered-assertion residual. A structured claim that never appears in the reader-facing artifact becomes a hidden-claim residual. Bidirectional coverage reduces the opportunity to place strong language outside the auditable claim surface.

# Belief Revision, Contradiction, and Bounded Commitment

A persistent epistemic system needs to change its mind without rewriting its history.

## Commitment states

A useful state set includes:

- mentioned;
- proposed;
- supported;
- contradicted;
- disputed;
- unknown;
- suspended;
- retired.

These labels are not universal truth grades. They are positions in a governed lifecycle, indexed by claim version, evidence set, context, evaluator policy, and time.

## Expansion, contraction, and revision

Belief expansion adds a claim without removing existing commitments. Contraction withdraws a commitment. Revision incorporates new evidence while restoring acceptable consistency where possible. The architecture draws on classical belief-revision distinctions [@agm1985; @gardenfors1988knowledge] but operates over versioned claims and heterogeneous justification artifacts.

A contradiction opens a bounded process:

1. identify the conflicting claim versions and contexts;
2. extract dependency and interpretation slices;
3. inspect source, mapping, and evaluator lineage;
4. generate candidate dispositions;
5. preserve disagreement and unresolved alternatives;
6. invalidate dependent commitments where required;
7. record the new state without deleting the old one.

## Partial inconsistency

Open-world systems cannot always restore global consistency. Time or resource limits may leave a local conflict unresolved. The correct output is partial inconsistency with an owned residual, not forced consensus or silent deletion.

## Entrenchment and authority

Some commitments are expensive to revise because many artifacts depend on them or because they encode protected policies. Entrenchment can inform review priority but should not make a claim irretractable. High centrality may be evidence that a claim deserves stronger scrutiny, not that it is more true.

Changes to constitutional or authority-bearing commitments require a different process from ordinary factual revision. Epistemic evidence can motivate a policy review; it cannot enact the policy change by itself.

## Append-only history, defeasible conclusions

Events and prior decisions remain append-only for audit. Current conclusions remain defeasible. This combination supports both accountability and correction: the system can say what it believed, why it changed, and which descendants became stale.

# Context Compilation and Admission

A model’s context window is not the system’s memory. It is a temporary working set compiled from a larger, versioned state.

The context compiler receives a task, consumer, snapshot, authority envelope, token and latency budgets, privacy constraints, and evidence obligations. It returns an admitted context package or a typed insufficiency state.

Let candidate representation \(r_i\) have cost vector \(c_i\), expected task value \(v_i\), and obligation coverage \(g_i\). The compiler solves a constrained selection problem:

\[
\max_{S \subseteq R} \; U(S)
\]

subject to:

\[
\sum_{r_i \in S} c_i \leq B,
\]

and mandatory obligations \(G_{\text{protected}}\) being satisfied. The objective is not merely relevance. It includes evidence adequacy, source fidelity, contradiction visibility, privacy, interference, latency, and fallback.

## Protected obligations

Some content must be represented before discretionary optimization:

- authenticated system policy;
- the active task and accepted interpretation;
- hard constraints and non-goals;
- corrections and commitments;
- action-authority boundaries;
- required source and quotation obligations;
- known contradictions or defeaters relevant to the decision;
- recovery and stop conditions.

Content cannot self-designate as protected. Protection follows from authenticated policy, principal authority, task structure, or a qualified transformation.

## Adequacy and admission

Adequacy asks whether a representation preserves the distinctions needed for an obligation. Admission asks whether that representation may enter the context for the current principal, purpose, and consumer.

A quotation can be adequate but inadmissible because of privacy. A summary can be admissible for planning but inadequate for citation. A source can be relevant but stale. A policy can be current but outside the requester’s authority.

The compiler preserves these distinctions rather than reducing them to a single relevance score.

## Representation ladder

One semantic object may have several representations:

- persistent handle;
- routing capsule;
- compact synthesis;
- evidence bundle;
- exact passages;
- complete source;
- runtime or model-native materialization.

No representation dominates every use. The compiler selects the cheapest eligible view that satisfies the consumer’s obligations. When exact detail is required, it escalates rather than asking a generative model to reconstruct omitted information.

## Snapshot coherence

The context package binds immutable source versions and a logical snapshot. It records read-your-writes behavior, branch-local changes, stale dependencies, and invalidation. A task that spans several turns should not silently mix old policy, new data, and a summary generated under a different source state.

## Typed insufficiency

When the protected set does not fit, the system should not drop an obligation and continue as if the task were merely lower quality. It returns a typed state such as:

- insufficient context budget;
- unresolved contradiction;
- required source unavailable;
- stale evidence;
- authorization missing;
- privacy conflict;
- verifier unavailable;
- feasibility unknown.

The caller can narrow the task, add resources, change the consumer, seek authorization, or abstain. Explicit insufficiency is more useful than a fluent answer whose missing premises are invisible.

## Verification bandwidth

The amount of text that fits in context differs from the amount of task-relevant checking the system can perform. A long document can crowd out one decisive exception. Pairwise checks may leave higher-order constraints untested. A hierarchy can reduce work while losing boundary information.

The architecture therefore represents an obligation graph and allocates checking work to the edges and subgraphs that matter. Context length, retrieval, and verification compute are related but distinct resources. “Everything was loaded” is not evidence that everything constrained the answer.

# Memory Lifecycle and Representation Residency

Persistence and retrieval are different decisions. A durable source can remain archived while a compact representation occupies active memory. Conversely, frequently retrieved content can remain epistemically weak.

## Lifecycle states

Representations may be:

- source-retained;
- derived;
- indexed;
- hot;
- warm;
- cold;
- frozen;
- stale;
- quarantined;
- deleted with residuals;
- retired.

These are storage and lifecycle states, not truth grades.

## Summarization and residuals

A summary records source versions, transformation, covered claims, omissions, uncertainty, contradictions, permitted uses, expiry, and exact-source fallback. It can reduce working-set cost without inheriting the audit authority of what it omits.

The system should maintain a **loss manifest**: distinctions known to be removed or unresolved. Unknown loss remains possible; the manifest is not a completeness proof.

## Goal-relative residency

Task relevance can change as goals change. A goal-aware cache may promote or demote representations, but it should not mutate durable evidence or protected commitments. Relevance decisions carry the goal version, evaluator, threshold, cost, and fallback. Hysteresis can reduce thrashing, while freeze/thaw transitions preserve a resolvable source and require fresh authorization and validity checks.

## Negative and contradicted memory

Rejected claims, failed routes, and contradictions should not disappear merely because they are inconvenient for generation. Negative memory preserves why an item was rejected and under what scope. It can prevent recurrence and support later review. It should not be retrieved indiscriminately or used to generalize beyond its evidence.

## Deletion and derivative closure

Deletion can mean removal of a source, an index entry, an active representation, a cache, a model derivative, or a downstream artifact. These are different claims. A deletion transaction identifies known descendants, legal or policy constraints, retained tombstones, cryptographic-key disposition, unavailable copies, and unlearning limits.

Removing an object from active retrieval is not proof that it no longer influences model parameters or external recipients.

## Cache validity

A cache key should bind semantic version, source snapshot, representation, compiler, tokenizer or serializer, principal, purpose, policy, rights, and consumer where those dimensions affect validity. A cache hit is a computational reuse event, not an epistemic transition. Material change invalidates or narrows dependent caches.

# Active Information Acquisition

A persistent agent should sometimes ask a question rather than load more of the same context.

Active acquisition selects among retrieval, database query, sensor action, tool call, specialist consultation, human clarification, or experiment. The selection objective is expected improvement in a downstream decision after cost, latency, privacy, risk, and burden.

For candidate question \(q\), let \(\Delta D(q)\) be expected decision improvement and \(C(q)\) its complete cost. A simple policy chooses

\[
q^* = \arg\max_q \left[\Delta D(q) - C(q)\right],
\]

subject to authority and safety constraints. The expression is a policy skeleton, not a calibrated universal rule.

## Posterior-preserving navigation

Active navigation should not delete alternatives merely because one question favors a path. It maintains candidate interpretations, unresolved identities, and branch-specific evidence until the consumer requires commitment.

## Clarification as a first-class action

Human clarification is not failure. Some ambiguity is cheaper and safer to resolve through a concise question than through broad retrieval or inference. The system should state which decision the answer would change and what default applies if clarification is unavailable.

## Experiments and interventions

Some questions cannot be answered from existing sources. A controlled experiment or intervention can generate evidence, but it requires its own authority, design, safety, and interpretation. The epistemic layer may propose an experiment; it cannot treat the proposed result as evidence before execution.

## Acquisition failures

Active acquisition can be gamed or misdirected. The agent may ask questions that confirm its preferred hypothesis, retrieve sources that mirror the same error, burden humans with low-value requests, or choose evidence that is easy to verify rather than decision-relevant. The system should retain the candidate denominator, selection policy, and rejected alternatives for high-consequence cases.

# Semantic Migration and Ontology Evolution

Long-lived semantic systems must change. The issue is not whether concepts evolve, but whether that evolution is explicit enough to preserve historical meaning and dependent obligations.

## Migration triggers

Migration can be triggered by:

- changed source or standard;
- new evidence;
- discovered ambiguity or collision;
- changed jurisdiction or domain;
- model or evaluator update;
- object merge or split;
- schema or ontology revision;
- changed world state;
- rights or policy change;
- incident or adversarial finding.

## Semantic transaction

A semantic migration transaction contains:

- immutable parent version;
- proposed new version or mapping;
- reason and evidence;
- semantic diff;
- affected contexts and consumers;
- dependency and impact cone;
- migration plan for claims, memories, plans, tools, and interfaces;
- compatibility and counterexample tests;
- authority and review;
- shadow or staged use;
- rollback or fork path;
- unresolved residuals.

## Semantic diff

The diff distinguishes:

- definitional change;
- extension change;
- entailment change;
- grounding change;
- temporal or contextual change;
- normative change;
- mapping change;
- operational change.

A documentation correction differs from a breaking revision. A broader concept can preserve some uses while invalidating others. A change to one label may be semantically neutral; a change to an exception can alter many dependent decisions.

## Impact cones

Dependencies are property-specific. A source-version change may invalidate a citation claim while leaving an unrelated geometric property intact. Unknown dependencies fail wide because a suspiciously small impact cone can hide unsafe reuse.

Reliance annotations are themselves fallible artifacts. They require provenance, review, tests, expiry, and incident history.

## Merge, split, fork, deprecate

- **Merge** combines objects while preserving aliases, origin, disagreement, and migration.
- **Split** creates more precise objects and routes dependent claims to the appropriate descendants.
- **Fork** preserves incompatible theories or contexts without forcing agreement.
- **Deprecation** discourages new use while retaining historical interpretation.
- **Revocation** blocks specified operational uses and can trigger descendant review.

No operation erases the record of the earlier semantic state.

## Historical replay

A historical artifact should be interpretable under the concept, source, and evaluator versions that existed when it was produced. The system separately reports whether the artifact remains valid under the current preferred basis. Historical validity, present truth, and current authorization are different statuses.

# Adversarial Review and Evaluator Dependence

Multi-model review can expose omissions and counterarguments, but role prompts do not create independent judgment.

A review process should declare:

- target artifact and use;
- source universe and omissions;
- reviewer identities and versions;
- model, provider, data, tool, prompt, memory, and organizational dependencies;
- attack roles and information exposure;
- cycle and cost budgets;
- support categories;
- escalation and human authority.

## Dossier boundary

Review is bounded by what reviewers can inspect. Absence from a dossier is not refutation. Unsupported-within-dossier differs from false. A reviewer can request expansion, preserve an open claim, or route to experiment.

## Claim extraction

Atomic claims improve addressability, but extraction can omit modality, exceptions, causal structure, tables, or relationships. Claims therefore retain source spans and uncertainty. Excessive fragmentation can also manufacture apparent coverage.

## Reviewer dependence

Two prompts to the same model are not independent because the roles differ. Providers, training data, retrieval systems, and organizational incentives create shared failure modes. An independence vector is more useful than a Boolean label.

## Stability and consensus

Stable prose can remain wrong. Consensus can reflect shared bias. Edit distance, embedding similarity, and agreement are stopping or routing signals, not correctness criteria. Disagreement can open a residual, request new evidence, or narrow the claim rather than being averaged away.

## Human review burden

A long claim-evidence packet can reduce trust while failing to change behavior because review is cognitively expensive [@martinboyle2026papertrail]. The system should present the minimum sufficient decision surface: contested claims, decisive evidence, limitations, unresolved items, and the exact authority the reviewer is asked to exercise. Deeper traces remain available without becoming the default interface.

# Cross-Modal Case Study: Evidence, Canon, and Generated Media

The distinction among source, commitment, and generated artifact becomes vivid in a multi-modal project.

Suppose a team produces an investigative report and accompanying video.

1. An **evidence store** preserves source-derived statements, exact passages, images, tables, modality, quotation scope, and provenance.
2. A rebuildable **evidence view** resolves entities, clusters related material, and proposes summaries. It can be regenerated when extractors change.
3. A draft **project canon** proposes accepted facts, entity identities, timelines, and uncertainty.
4. An authorized **active canon** records the commitments that may constrain generation.
5. Section and scene contracts declare required and forbidden claims, evidence duties, time, entities, props, continuity, and acceptable variance.
6. Text and visual generators produce artifacts plus structured deltas.
7. Validators act as sensors, checking schema, contradiction, source grounding, identity continuity, and omissions.
8. Human reviewers adjudicate conflicts and approve bounded deviations.
9. A provenance bundle links final artifacts to evidence, canon versions, generation routes, findings, repairs, and unresolved residuals.

The architecture prevents several substitutions. An extractor’s output does not become canon. Canon does not become evidence. A fluent script does not make a claim true. A visually consistent shot does not establish identity. A content credential can preserve provenance without establishing accuracy.

This case is not a separate media architecture. It demonstrates that semantic and epistemic state must survive cross-modal production and that generated artifacts remain downstream projections of governed commitments.

# Benchmark and Evaluation Program

The proposed architecture should be tested as a collection of mechanisms rather than as one all-or-nothing ontology.

## Context adequacy benchmark

Construct tasks containing:

- rare decisive constraints;
- negation and exceptions;
- contradictory sources;
- stale and current evidence;
- exact quotation requirements;
- privacy-restricted evidence;
- long distractor material;
- changed task goals;
- insufficient context budgets.

Compare long-context prompting, ordinary retrieval, human-authored summaries, graph retrieval, and the governed context compiler. Measure obligation recall, unsupported output, contradiction retention, false contradiction, exact-source use, privacy violations, latency, tokens, and abstention.

## Evidence-laundering benchmark

Use claim records that are syntactically valid but contain:

- wrong claim identity;
- sibling or parent support inheritance;
- proof of a weaker statement;
- source that mentions but does not entail the claim;
- outdated evaluator;
- omitted limitation;
- broad negative inference from a narrow result.

Compare schema-only validation with claim identity, justification competence, and maximum-inference checks. The benchmark should include positive and negative controls and independent source labels where possible, building on current claim-evidence research [@chen2026evidenceledger].

## Belief-revision benchmark

Introduce new evidence, source corrections, competing interpretations, and partial inconsistency. Measure whether the system:

- preserves prior history;
- updates the exact claim;
- invalidates appropriate descendants;
- retains disagreement;
- avoids unnecessary global retraction;
- exposes unresolved residuals.

## Semantic-migration benchmark

Change definitions, ontologies, evaluator versions, and task contexts. Test merge, split, fork, deprecation, and revocation. Measure historical replay, mapping accuracy, stale-use rate, over-invalidation, missed descendants, and migration cost.

## Evaluator-dependence study

Compare:

- repeated prompts to one model;
- different models from one family;
- different providers;
- deterministic checks;
- source-grounded specialist review;
- qualified human review.

Measure error correlation, disagreement utility, false confidence, review burden, and incremental decision value.

# Threat Model

## Semantic capture

A central ontology can become institutional power. Maintainers may force local or minority meanings into one schema, hide contested mappings, or make interoperability conditional on adopting their definitions.

## Identity collision and laundering

Aliases, embeddings, or merges can cause distinct objects to share evidence or permissions. Conversely, renaming can be used to escape incidents and residuals.

## Source and provenance attacks

Sources can be poisoned, stale, selectively quoted, rights-encumbered, or fabricated. A provenance graph can faithfully preserve a malicious derivation.

## Certified delusion

A proof, parser, or deterministic procedure can validate the wrong formalization. Shared semantic compilers and verifiers can make the error systematic.

## Context manipulation

Attackers can self-designate content as mandatory, hide instructions in retrieved data, crowd out decisive evidence, or exploit summary loss. Context policy must bind protection to authenticated authority rather than content claims.

## Memory poisoning and fixation

Repeated exposure can increase retrieval priority without increasing truth. Negative memories can be flooded to induce paralysis. Stale high-centrality summaries can dominate current evidence.

## Review monoculture

Multiple reviewers may share the same data, model, organization, and incentives. Consensus can hide dependence and suppress unusual but correct objections.

## Deletion overclaim

Removing known copies can be presented as total erasure. Backups, logs, models, external recipients, and descendants may remain outside control.

## Governance burden

Rich semantic records can consume more effort than they save. Operators may bypass the system or reduce it to checkbox compliance. Complexity should scale with consequence and be removed when it does not change decisions.

# Limitations, Falsifiers, and Contraction Rules

The architecture cannot solve semantic grounding in the general case. Persistent identifiers are governed conventions, not metaphysical guarantees. Concept versions can be incomplete. Source interpretations can be wrong. Evidence can be unavailable. Reviewers can be captured. Open-world dependency graphs can miss descendants.

The proposal should contract when:

- ordinary retrieval plus source links matches context adequacy at lower cost;
- a conventional relational database preserves identity and migration without the richer semantic layer;
- claim-identity checks do not reduce evidence laundering beyond schema validation and human review;
- active acquisition adds latency and burden without improving decisions;
- semantic migration produces more over-invalidation than useful precision;
- the review surface overwhelms users and causes rubber-stamping;
- provenance records are not used by any behavior-changing consumer.

Some domains may not need stable conceptual identity beyond ordinary versioned schemas. Some tasks are best served by direct source inspection. Some disputes cannot be resolved technically and should remain institutional or human questions.

The strongest simpler baseline is a well-engineered system with versioned documents, relational storage, conventional RAG, source links, ordinary access control, human review, and explicit update procedures. The proposed architecture earns its cost only if it reduces stale use, semantic drift, claim laundering, context omission, or migration failure under matched conditions.

# Conclusion

Persistent agents need more than memory. They need semantic continuity, evidence discipline, defeasible commitment, context adequacy, and controlled revision.

This paper separates source, semantic, storage, context, epistemic, and authority states. Stable identifiers refer to governed lineages rather than labels or embeddings. Claims carry typed justification artifacts and maximum inferences. Context is compiled for a consumer and snapshot, with mandatory obligations, explicit omissions, and exact-source escalation. Belief revision preserves append-only history while changing current commitments. Semantic migration propagates concept, source, evaluator, and ontology changes through dependent claims and artifacts.

The proposal does not make meaning objective or evidence true. It creates explicit places where those judgments can be represented, tested, and challenged. Its success depends on whether the additional state separation changes real outcomes compared with simpler retrieval and database systems.

A final distinction remains outside this paper. Even when an experience is represented accurately and a claim is responsibly revised, the system has not yet decided what should become a durable lesson. Whether a failure belongs in memory, procedure, tool, parameters, evaluator, environment, or nowhere yet is a causal adaptation problem rather than an epistemic one.

# Appendix A: Canonical Record Sketches

## Semantic object

```yaml
semantic_object:
  lineage_id: semantic:uuid
  kind: concept | entity | event | claim | procedure | policy
  versions:
    - version: semantic-version:hash
      parent: semantic-version:hash | null
      context: context:version
      lexical_interfaces: []
      constraints: []
      relations: []
      exclusions: []
      grounding_contracts: []
      valid_time: interval
      sources: []
      governance_event: event:uuid
```

## Claim record

```yaml
claim:
  id: claim:uuid
  proposition: structured-content
  semantic_basis: []
  scope: population-and-context
  valid_time: interval
  assumptions: []
  support_relations: []
  defeaters: []
  commitment_state: proposed | supported | contradicted | disputed | unknown | suspended | retired
  maximum_inference: string
  allowed_consumers: []
  expires_at: timestamp | null
  review_triggers: []
```

## Context package

```yaml
context_package:
  id: context:uuid
  task: task:uuid
  consumer: consumer:version
  snapshot: snapshot:uuid
  protected_obligations: []
  admitted_representations: []
  omitted_frontier: []
  contradictions: []
  unresolved_items: []
  budgets: {}
  rights_and_privacy: []
  insufficiency_state: null | typed-state
  materialization_identity: runtime:hash
```

# Appendix B: Intellectual Lineage and Supersession

This paper consolidates eleven earlier author manuscripts. Their role is intellectual lineage, not independent empirical confirmation.

| Legacy source | Material retained | Material narrowed or retired |
|---|---|---|
| Platonic World Model | Semantic continuity, concept lineages, immutable versions, contexts, world branches, grounding, migration | Metaphysical or timeless-essence implications |
| Question-Compiled Semantic Addressing | Identity/address/route separation, plural indexes, active questions, migration | Unmeasured routing advantage and specialized branding |
| Virtual Context Memory | State separation, protected context obligations, snapshots, typed insufficiency, exact-source fallback | Infinite-context and lossless semantic-compression implications |
| Spinoza | Typed justification artifacts, interpretation records, claim graph, bounded revision, certified-delusion risk | Total truth ladder and compliance-oracle language |
| Spinoza Composer | Evidence versus approved canon, cross-modal contracts, causal and presentation time, provenance | Style-cloning and media-production projections |
| Aletheia / Proof-Carrying Workbench | Claim-native artifacts, semantic custody, constraint capsules, recertification | Truth-manufacturing and deterministic claim-extraction claims |
| Unified Adaptive Tribunal | Dossier-bounded review, omission search, disagreement, human handoff | Consensus, stability, and unsupported quantitative claims |
| Verification Bandwidth | Availability versus checking capacity, obligation graphs, coherency horizon | Universal two-body laws, quadratic necessity, half-context optimum |
| TreeLLM | External semantic memory, learned navigation, versioned graph and private overlays | Frozen roots, one true lattice, unsupported implementation and performance claims |
| Context Engineer | Governed context supply, representation tiers, compartment lifecycle, declassification | Military branding and unverified synthetic results |
| Black Hole Context Manager | Tiered residency, goal-relative relevance, hysteresis, freeze/thaw, source fallback | Semantic-mass score and production-ready pseudocode claims |

# References

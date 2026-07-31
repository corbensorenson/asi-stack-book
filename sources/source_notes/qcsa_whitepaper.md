# Source Note: Question-Compiled Semantic Addressing

| Field | Value |
|---|---|
| Source ID | `qcsa_whitepaper` |
| Source title | Question-Compiled Semantic Addressing |
| Ingestion date | 2026-07-11 |
| Source version / URL | Version 1.0, dated 2026-07-12 as supplied; local canonical source SHA-256 `d9e594d40dfd62c899ab25e9d395d34c702dac12e8afd75eed133392f78c0c8c` |
| Ingestion basis | The complete 1,709-line Corben-authored whitepaper was inspected at `sources/raw/question_compiled_semantic_addressing_whitepaper.md`; raw source text is local-only and not published by this ingestion. |
| Evidence boundary | The source itself remains conceptual architecture and design rationale at `argument`. A later local reference package, bounded synthetic evaluation, and governed vertical replay are repository evidence, not evidence supplied by the whitepaper; they establish no matched-resource advantage, formal semantic-correctness proof, safety validation, or production transfer. |

## Thesis

Question-Compiled Semantic Addressing (QCSA) treats semantic addressability as a
governed control-plane primitive. Durable objects receive stable opaque Semantic
Object IDs (SOIDs); one object can receive plural, task-scoped, versioned
semantic virtual addresses (SVAs) in a multi-facet atlas; a question compiler
acquires the next decision-relevant evidence under cost, risk, privacy, and
interaction constraints; and a separate translator compiles semantic intent
into temporary physical route plans. The durable knowledge substrate is a
typed, temporal, evidence-bearing hypergraph. Trees are efficient indexes over
that substrate, not the truth substrate itself.

The key separation is:

> Store by stable identity. Index by plural semantic addresses. Find by adaptive
> questions. Reason over a typed evidence graph. Execute through compiled
> physical routes.

This is a successor synthesis to TreeLLM and the folded Semantic Representation
Leasing material. It is not a synonym for binary tokenization, hierarchical
softmax, a universal concept tree, or a tokenizer replacement.

## Claim Boundary and Status

- QCSA is a conceptual architecture, formal model, artifact specification,
  inference protocol, governance design, and falsifiable research program.
- Stable identity, plural addresses, active questions, and compiled routes are
  proposed separations; the paper does not establish universal semantic
  identity, correct grounding, useful compression, routing advantage,
  interpretability, authority safety, or self-reorganization safety.
- The local reference package and synthetic runs are later repository evidence,
  not evidence supplied by the paper. Their matched-advantage and resource
  gates failed, so they cannot retroactively make the whitepaper empirical.
- Binary paths, trees, latent codewords, and hierarchical generation remain
  admissible implementations or indexes; none is the canonical truth
  substrate or durable identity by itself.

## Conceptual Primitives and Distinctions

- **Identity / address / route:** what object persists, how a consumer locates
  it semantically, and where/how the current task executes are separate.
- **Occurrence / type / instance / expression:** contextual evidence,
  reusable category, concrete referent, and compositional semantic program are
  not interchangeable records.
- **Graph / atlas / path:** the typed evidence-bearing hypergraph is the
  substrate; an atlas is a consumer-oriented index; one SVA is a defeasible
  path through an atlas epoch.
- **Question / commitment:** evidence acquisition can remain adaptive and
  posterior-preserving until one consumer's consequence requires commitment.
- **Semantic migration / physical remapping:** reorganization of meaning needs
  epoch migration; moving shards, experts, decoders, or compute normally does
  not.
- **Ontology / evidence / belief / authority:** a graph object, support for a
  proposition, present epistemic standing, and permission to act are distinct.

## Required Terminology

- Question-Compiled Semantic Addressing (QCSA)
- Semantic Object ID (SOID)
- Semantic virtual address (SVA)
- Multi-facet semantic address atlas
- Semantic Address Certificate (SAC)
- Question compiler / active navigator
- Typed temporal evidence-bearing hypergraph
- Semantic-to-physical route compiler
- Atlas epoch and migration record
- Open-world concept expression

## Mechanisms

- Separate surface occurrence, reusable semantic type, world instance, and
  compositional expression before binding a stable identity.
- Maintain SOIDs independently of names, embeddings, semantic atlas positions,
  model versions, physical storage, and execution routes.
- Represent concepts, entities, events, propositions, expressions, memories,
  tools, policies, and obligations in a typed temporal hypergraph whose claims,
  evidence, belief state, provenance, authority, and lifecycle remain distinct.
- Compile multiple consumer-declared atlas facets—ontological, functional,
  causal, linguistic, perceptual, procedural, policy, and workload—rather than
  treating one hierarchy as universally true.
- Use soft, variable-length, adaptive-arity address paths; preserve top-k paths,
  cross-facet inconsistency, `unknown`, `conflicting`, and `abstain` until a
  consumer-specific commitment boundary.
- Issue Semantic Address Certificates (SACs) that bind SOID, occurrence or
  expression, context, task, consumer, atlas epoch, facet paths, confidence,
  provenance, grounding, residuals, allowed and prohibited uses, authority
  ceiling, validity, migration, digest, and signature.
- Select internal discriminators, retrievals, sensor actions, tool calls,
  specialist requests, or human clarification by expected decision value after
  compute, latency, privacy, burden, and risk costs.
- Compile SACs into task-specific physical plans for memory, experts, models,
  tools, approval, compute, generation, validation, fallback, and receipts;
  semantic resolution never grants capability authority.
- Treat compact semantic paths and inherited deltas as scoped leases that must
  retain object-specific residuals, verifier cost, fallback, collision risk,
  migration cost, and consumer adequacy.
- Release atlas updates on a slow governed timescale with immutable epochs,
  migration maps, old-address compatibility, shadow evaluation, staged
  authority, rollback, and explicit typed failure instead of silent retargeting.
- Support open-world provisional objects, controlled merge/split history,
  multilingual and multimodal grounding above surface codecs, and typed
  compositional expressions instead of forcing every meaning into a leaf.
- Re-resolve generated output and compare object identity, roles, negation,
  modality, quantity, time, claim/citation bindings, authority, and residuals as
  a bounded translation-validation pattern.

## Interfaces, Artifacts, and State Machines

- `SemanticObjectRecord` owns stable kind, namespace, aliases, provenance,
  lifecycle, and merge/split lineage without treating similarity as identity.
- `AtlasEpoch` owns facet contracts, codebooks, topology, calibration,
  representative/boundary cases, utilization, known collisions, prohibited
  uses, migration maps, signatures, and rollback.
- `SemanticAddressCertificate` binds one resolution to occurrence/expression,
  consumer, task, epoch, weighted paths, confidence, evidence, grounding,
  residuals, allowed/prohibited uses, authority ceiling, expiry, and migration.
- `QuestionTrace` binds posterior before/after, candidate question or batch,
  expected decision value, costs, acquired evidence, noise/conflict,
  backtracking, commitment, and unresolved alternatives.
- `PhysicalRoutePlan` binds memory/model/tool targets, redactions, resources,
  joins, validators, approval, fallback, abstention, and receipts without
  redefining the semantic object or granting itself authority.
- `AddressMigrationRecord` binds old/new epochs, address mapping, same-SOID
  check, affected consumers/descendants, compatibility, failures, rollback,
  and explicit unresolved cases.

## Assumptions, Invariants, and Conditional Results

- Names, embeddings, codes, paths, models, languages, and locations cannot
  serve as stable semantic identity without an explicit governed identity rule.
- Every old address either resolves to the same SOID after migration or fails
  explicitly; silent retargeting is forbidden.
- A shorter or cleaner address is an improvement only when omitted
  distinctions, collisions, verification, repair, migration, and fallback are
  included in the account.
- A semantic certificate can constrain use and preserve lineage but cannot
  establish that the object, proposition, grounding, or action is correct.
- Internal discriminators may be operationally useful without a faithful
  natural-language intensional explanation.
- Active questions are valuable only when they improve a downstream decision
  frontier after compute, latency, privacy, risk, and human burden.
- A route plan remains subordinate to capability, policy, and effect authority.

## Algorithms and Implementation Program

1. Resolve surface evidence into candidate occurrences, types, instances, and
   expressions while preserving ambiguity and provenance.
2. Retrieve a stable SOID or create a provisional local object after collision
   search; govern later merge or split without historical rewrite.
3. Materialize relevant facet candidates from the current atlas epoch and
   retain soft paths, variable depth, mixed arity, and cross-facet conflict.
4. If consumer adequacy is insufficient, select one question or parallel batch
   by expected decision value minus resource, privacy, risk, and burden costs;
   update rather than hard-delete the posterior.
5. Issue a SAC only at the named commitment boundary, then compile a temporary
   physical plan through separate authority and resource policy.
6. For generation, construct a typed semantic expression, decode it, re-resolve
   the output, and compare identity, roles, operators, claims, and residuals.
7. Keep contextual resolution fast, resolver/codebook learning medium, and
   atlas publication slow; publish new epochs only with compatibility,
   migration, staged use, rollback, and descendant repair.

## Normative Artifacts Proposed

1. Semantic Object Record and SOID registry.
2. Typed hypergraph schema with evidence and lifecycle state.
3. Atlas manifest, facet contracts, codebooks, and immutable epoch package.
4. Resolver calibration and boundary report.
5. Question-policy trace corpus.
6. Semantic Address Certificate schema and validator.
7. Semantic-to-physical route-plan schema and receipt.
8. Address migration record, compatibility harness, and rollback exercise.
9. Adversarial alias, collision, poisoning, stale-epoch, and route-disagreement
   suites.
10. Multilingual and multimodal grounding suite.
11. Semantic round-trip generation validator.
12. Resource, latency, residual, fallback, and benchmark ledgers.

These are implementation targets, not artifacts that this source supplies.

## Local Implementation And Evaluation Update (2026-07-13)

The source boundary above remains unchanged, but the repository has now built
and evaluated the proposed artifact family as a separate, bounded evidence
lane. The standard-library reference package implements all twelve frozen QCSA
lanes and replays byte-identically. Its 60-case held-out synthetic evaluation
ran the full method, seven baselines, five ablations, and three seeds, producing
2,340 predictions. A governed vertical trace then joined thirteen stages from
intent and semantic IR through a real temporary-file effect, independent byte
observation, same-SOID migration, and byte-exact rollback.

The outcome is mixed and deliberately narrow:

- QCSA and the selected best baseline both reached `1.000000` task-decision
  accuracy, so the preregistered matched-advantage gate failed.
- QCSA used `1.913386` times the baseline operation count, so both frozen
  resource ceilings failed.
- Plural facets, identity/address indirection, certificate/residual/authority
  fields, migration compatibility, and task calibration earned bounded
  fixture-level promote dispositions for later evidence review.
- Removing active questions did not reduce object or task accuracy. Because the
  workload is template-generated, the task saturates at 1.000, the evaluator is
  internal, and verifier-cost bookkeeping is confounded, this is N2
  proxy/regime evidence—not an exact or broad refutation of active questioning.
- The vertical trace rejected all 10 adversarial paths and performed one exact
  rollback, but remains synthetic, local, internally observed, and limited to
  one reversible temporary-file effect.

Canonical records are
`experiments/qcsa_reference/results/evaluation_results.json`,
`claim_decisions/qcsa_reference_evaluation_dispositions.json`,
`docs/qcsa_reference_evaluation_report.md`,
`experiments/qcsa_vertical_reference/results/vertical_result.json`, and
`docs/qcsa_governed_vertical_reference_report.md`. These records improve the
nine existing chapter owners; they do not promote any chapter-core claim above
`argument` and do not warrant a standalone QCSA chapter.

## Evidence and Falsification Boundary

- The source supplies a coherent architecture, formal notation, normative
  record sketches, an inference protocol, failure analysis, baselines,
  ablations, success criteria, and falsification criteria.
- Its literature review positions established components, but it is not an
  exhaustive patent or publication search and does not prove novelty.
- Success requires a meaningful matched-resource Pareto gain in task quality,
  compute or memory, calibrated disambiguation, tail generalization, transfer,
  repair locality, or governance value.
- The proposal should be narrowed or rejected if learned addresses do not beat
  matched random/frequency trees, plural facets add cost without utility,
  active questions do not beat direct inference or simple clarification,
  identity-address indirection does not reduce migration errors, semantic
  routing does not improve a measured frontier, SAC overhead prevents no
  failures, or semantic-first generation loses quality/latency without benefit.
- Every ASI Stack core claim remains at `argument`; ingestion creates no
  source-derived, prototype-backed, test-backed, mechanized, safety, production,
  AGI, or ASI result.

## Failure Modes

- Ontological capture by one apparently canonical hierarchy.
- Early route errors hidden by hard commitment or clean-looking paths.
- Codebook collapse, identifier ambiguity, concept explosion, and load
  imbalance.
- Silent address drift or migration from one SOID to another.
- Polysemy collapse and cross-language false equivalence.
- Semantic laundering: a graph location or address is mistaken for evidential
  truth or action authority.
- Alias-driven privilege escalation and semantic/physical route disagreement.
- Adversarial atlas poisoning, branch overload, privacy leakage, and inference
  of sensitive traits from address patterns.
- False interpretability when a latent partition receives a convenient story.
- Overcompression that hides omitted distinctions and reconstruction burden.
- Governance infrastructure that precisely documents wrong resolutions without
  improving behavior enough to justify its cost.

## Threats, Misuse, and Governance Costs

- Semantic aliases and apparently nearby concepts can become confused-deputy
  paths into privileged tools or data.
- Address patterns, facets, and question traces may reveal sensitive traits
  even when raw content is withheld.
- Atlas owners can encode institutional or cultural power into a seemingly
  technical hierarchy; plural facets reduce but do not remove capture.
- Certificates, migration, calibration, graph storage, question acquisition,
  verification, and fallback can cost more than the retrieval or routing
  benefit. Total-cost and missed-help comparisons are mandatory.
- A richly audited but systematically wrong resolver can scale error more
  efficiently; governance record completeness is not semantic correctness.

## Book Chapters Supported

| Chapter | QCSA contribution | Passage basis | Boundary |
|---|---|---|---|
| `cognitive-compilation-and-semantic-ir` | SOIDs and SACs as typed IR references; question traces as evidence-acquisition programs; physical route plans as target lowering. | §§5–6, 9–10, 18.1; Appendix B | Design contract only; no compiler implementation or semantic-preservation result. |
| `virtual-context-abi` | SOID-addressed context objects, plural SVA leases, atlas epochs, bounded graph materializations, SAC adequacy/residual fields, revalidation, and typed faults. | Axioms 1–12; §§5.2–5.7, 8–9; Appendix A | Does not establish VCM adequacy, retrieval quality, or context safety. |
| `routing-heads-and-specialist-cores` | Semantic-to-physical expert/model routing while load, hardware, resources, permissions, fallback, and abstention remain separate physical-policy concerns. | §§5.8, 9–10, 16.3–16.5, 18.4 | Does not establish routing accuracy, efficiency, transfer, or production safety. |
| `compact-generative-systems-and-residual-honesty` | Successor synthesis for Semantic Representation Leasing: plural address leases, path deltas, open-world expressions, semantic-first generation, round-trip validation, and explicit residual burden. | Axiom 12; §§8, 11, 14.6, 16.6, 18.6 | Does not establish compression, model quality, latency, or semantic preservation. |
| `runtime-adapters-tool-permissions-and-human-approval` | Hard separation between semantic resolution and capability authority; route plans bind actor, target, scope, policy, reversibility, approvals, and receipts. | §§10.2, 10.5, 14.1–14.5, 18.5 | An address, alias, certificate, or semantic match never authorizes an effect. |
| `claim-ledgers-and-belief-revision` | Ontology, propositions, evidence, provenance, belief state, contradiction, support, and permitted use remain distinct graph objects. | §§5.4, 7.4–7.5, 14.4, 18.3 | A semantic address is neither truth nor support-state evidence. |
| `data-engines-continual-learning-and-unlearning` | Fast/medium/slow learning split, candidate atlases, epoch authority, migration compatibility, identity-preserving readdressing, merge/split lineage, and drift tests. | Axiom 11; §§7.3, 12, 14.5, 16.7 | Does not establish forgetting, influence removal, privacy erasure, or storage erasure. |
| `inter-stack-protocols-identity-and-economic-exchange` | Namespace-qualified SOIDs, signed SACs, atlas/mapping manifests, epoch negotiation, and uncertainty-preserving cross-stack translation. | §§7.3, 14.2, 18.8; Appendix A | Federation does not establish equivalence, trust, authorization, truth, or settlement. |
| `integrated-reference-architecture` | QCSA as the semantic control plane joining grounding, context, planning, memory, routing, tools, generation, evidence, and lifecycle governance. | §§5, 18; Appendix B | The source is a reference architecture; the separate local vertical trace implements one bounded reversible path but establishes no validated advantage or production transfer. |
| `governed-world-models-and-reality-grounding` | Uses qualified semantic addresses, observation provenance, atlas epochs, uncertainty, contradiction, and revalidation to keep model state answerable to changing reality. | Axioms 1–12; §§5–10, 14, 18 | Semantic resolution is not a reality oracle or validated world-model controller. |
| `white-box-evidence-interpretability-and-activation-governance` | Treats internal semantic structures as versioned, defeasible evidence inputs whose use remains separate from action authority. | §§5–8, 10, 14, 18 | No interpretability method, causal validation, or governance efficacy result. |
| `durable-semantic-memory-and-knowledge-lattices` | Supplies stable semantic identities, evidence-bearing temporal hypergraphs, plural versioned addresses, migration records, contradiction state, and explicit residuals for a durable knowledge substrate. | Axioms 1–12; §§5–8, 12–14, 18; Appendices A–B | No durable-memory truth, deletion completeness, restart equivalence, retrieval-quality, or production-transfer result. |

## Chapter Decision

Keep the active 54-chapter architecture. QCSA is intentionally cross-cutting and
its strongest contribution is the identity–address–route contract between
existing chapter owners. A standalone chapter would still duplicate the
context, routing, representation, tool, claim, learning, federation, and
integration chapters. The later implementation and evaluation strengthen those
existing owners but do not create a distinct chapter thesis: matched advantage
failed on the frozen proxy, the active-question ablation is N2 proxy/regime
evidence rather than a refutation, and production transfer remains open.
Reconsider a dedicated chapter only if a future natural-
task, learned-model, independently assessed program creates a chapter-owning
body of evidence that cannot be folded coherently into the nine owners.

This decision preserves the executed Semantic Representation Leasing fold.
QCSA supersedes the earlier framing as the richer source synthesis but does not
silently replace TreeLLM lineage or satisfy the fold's empirical restoration
conditions.

## Claims To Add Or Update

- Add a section-level design rationale: advanced AI should separate stable
  semantic identity, plural versioned semantic addresses, and task-specific
  physical route plans; use active questions to reduce decision-relevant
  uncertainty; and govern address issuance and migration with evidence-bearing
  certificates, compatibility checks, residuals, and rollback.
- Add the hard invariant that semantic resolution cannot grant execution
  authority.
- Add the migration invariant that an old address must resolve to the same SOID
  in the new epoch or fail explicitly; silent retargeting is forbidden.
- Add the evidential invariant that graph position, address confidence, and
  certificate integrity do not establish proposition truth or support state.
- Add the compression invariant that a shorter path is acceptable only when
  omitted distinctions, collisions, verification, repair, migration, and
  fallback remain visible.

## Cross-Paper Synthesis and Tensions

- TreeLLM supplies hierarchical semantic representation lineage; QCSA replaces
  one canonical tree with stable identity, a graph substrate, plural atlases,
  active navigation, and separate physical lowering.
- VCM supplies typed context materialization; QCSA supplies the SOID/SVA/SAC
  identity and addressing contract VCM may consume.
- Cognitive Compilation treats question traces as evidence-acquisition IR and
  route plans as target lowering, while Talos and Runtime retain execution
  authority.
- SCF supplies epoch, qualification, migration, and replacement discipline;
  QCSA specializes those controls for semantic objects and atlases.
- The Platonic World Model provides a richer constitutional semantics and
  grounding plane; QCSA provides a more operational address/navigation fabric.
  Neither makes semantic identity metaphysically final.
- Relational Dimension Compilation can type the roles and dimensions inside
  QCSA expressions, while QCSA supplies durable identity and address custody.
- Compact Generative Systems can exploit inherited path deltas, but QCSA's
  residual and round-trip rules prevent the hierarchy from claiming complete
  semantic compression.

## Section-Family Coverage

- §§1–4: originating intuition, SOTA boundary, and twelve axioms → source note,
  Cognitive Compilation, VCM, Durable Semantic Memory, and Integrated
  Architecture.
- §§5–6: ten-subsystem reference architecture and formal model → chapter
  owners plus normative artifact/research program; equations remain proposed.
- §§7–8: semantic identity, typed hypergraph, and plural atlas geometry →
  Durable Semantic Memory and VCM.
- §§9–10: active navigator and semantic-to-physical translation → Cognitive
  Compilation, Routing, Runtime, and Procedural Memory.
- §11: compositional representation, semantic-first generation, and round-trip
  validation → Compact Generative Systems and Cognitive Compilation.
- §§12–13: three-timescale learning, migration, multilingual and multimodal
  grounding → Data Engines, World Models, and Perception/grounding owners.
- §§14–15: certificates, authority, taint, poisoning, privacy, residuals, and
  failure analysis → VCM, Security, Runtime, Privacy, Memory, and Failure Modes.
- §16: seven workstreams, baselines, ablations, success, and falsification →
  Benchmark Ratchets and Open Research Agenda; the local synthetic result is
  separately bounded.
- §§17–20: contribution boundary, eight integrations, limitations, conclusion
  → source note and existing chapter owners; no standalone chapter warranted.
- Appendices A–C: record sketches, inference protocol, and research artifact
  set → schemas/fixtures and research obligations; not paper-supplied results.
- Appendix D and references: terminology and prior-art candidates → glossary
  and independent external-source backlog.

## Closure Status

Section-family closure completed 2026-07-31 against the current 84-chapter
manuscript. The final repair added object-level identity distinctions and
plural atlas geometry to Durable Semantic Memory, decision-relative noisy and
parallel question compilation to Cognitive Compilation, and three-timescale
atlas learning plus referentially safe physical/semantic remapping to Data
Engines. All remaining paper formulas, normative record sketches, inference
protocol detail, benchmark workstreams, and reference candidates have explicit
research or source-note destinations.

Closure creates no claim that QCSA beats a matched baseline, that active
questioning works generally, that semantic round trips preserve meaning, or
that the architecture is safe, private, efficient, deployed, or supported
above the already recorded narrow fixture dispositions.

## Open Questions

- What is the smallest SOID/SAC/atlas slice that can test identity-address
  indirection without first building the whole architecture?
- Which held-out workload makes active questions, fallback, abstention, and
  direct inference materially diverge under matched cost?
- Which authority surface should be the first consumer: memory retrieval,
  expert routing, tool routing, or semantic-first generation?
- How should atlas migration test downstream descendants, caches, backups,
  audit receipts, and cross-stack mappings?
- Can round-trip semantic validation detect meaningful structural loss without
  becoming a self-confirming evaluator?
- Which QCSA reference papers should be independently ingested into Appendix H
  instead of being cited only through this author paper's literature review?

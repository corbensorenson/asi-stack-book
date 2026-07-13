# ASI Stack Post-v2.2 Implementation and Book Completion Roadmap

Roadmap ID: `asi-stack-post-v2-2-implementation-completion-2026-07-13`

Authority: Corben Sorenson

Status: active canonical successor roadmap; unfinished work only

Predecessor: `docs/post_v2_1_residual_and_transfer_roadmap.md`, completed for
the immutable v2.2.0 release and retained as execution history

## Goal to point at

> Move The ASI Stack from a deeply specified and internally tested living book
> toward a coherent, runnable reference implementation. Implement the new
> Question-Compiled Semantic Addressing (QCSA) contracts first, because they
> supply the identity, address, evidence-acquisition, route-compilation, and
> migration spine needed to join the existing chapters without collapsing
> their authority boundaries. Evaluate that implementation against matched
> baselines and adversarial controls, then use it in one governed end-to-end
> vertical slice. Reconcile every result into existing chapter owners, close
> the selected implementation and book-product gaps, and complete a clean
> release transaction if the results warrant one. Preserve failed attempts,
> negative results, costs, residuals, and non-claims. Do not add a chapter or
> promote a support state merely because code now exists.

This is the canonical long-running goal for the post-v2.2 cycle.

## What “completed” means

Completion means the selected public-safe reference implementation, its
evidence packet, the canonical HTML book, its machine records, and its release
surfaces agree and pass their registered gates. It does **not** mean that ASI,
AGI, universal semantic understanding, production safety, open-world transfer,
or every mature endpoint described by the book has been achieved.

The project may honestly complete this roadmap with negative QCSA results. A
well-replayed falsification, a narrowed design, or a no-release decision is a
valid terminal outcome. An attractive demo without matched baselines,
authority separation, migration checks, cost accounting, or residuals is not.

## Authority and truth hierarchy

1. Exact tags, immutable release assets, release records, and tag-bound rights
   snapshots govern historical releases.
2. `book_structure.json`, claim/evidence records, the validation registry,
   experiment freezes/results, and
   `roadmap_records/post_v2_2_implementation_completion_status.json` govern the
   current cycle within their domains.
3. Generated scaffolds and public status projections must reproduce those
   authorities.
4. README, the landing page, readiness notes, chapters, and appendices must
   describe the machine state without upgrading it.

The v2.2.0 release remains immutable. This roadmap activates later work; it
does not rewrite the v2.2.0 tag, archive, release record, rights snapshot, or
completion declaration.

## Baseline at activation

- Latest immutable release: `v2.2.0` at commit
  `e3d5348993cc5083604c85bd699bb0e36eb00de1`.
- Active architecture: 54 chapters and 280 public-safe source records.
- All 54 chapter-core claims remain at `argument`; zero are promoted.
- QCSA is passage-reviewed and integrated into nine existing chapters as
  design rationale, but the repository contains no QCSA implementation,
  matched benchmark, semantic-correctness proof, or measured advantage.
- The QCSA source note proposes twelve normative artifact/evaluation lanes.
- The post-v2.1 residual ledger retains nine narrowed or persisted empirical
  residuals, two locally closed residuals, and three activation-absent
  infrastructure lanes.
- Canonical HTML is the selected public book product. EPUB, DOCX, PDF, audio,
  and a separately released curated reader remain outside this roadmap unless
  explicitly activated by amendment.

## Operating principles

1. **Implementation before more architecture.** Build the smallest coherent
   QCSA and vertical-stack artifacts before introducing new abstractions.
2. **Existing owners before new chapters.** The nine QCSA chapter owners and
   the integrated reference architecture receive implementation results first.
3. **Identity, address, truth, and authority remain separate.** SOIDs identify;
   SVAs index; evidence supports claims; route plans request effects; only an
   independent authority decision permits an effect.
4. **Matched comparisons before advantage claims.** Random/frequency trees,
   single hierarchies, direct inference, flat retrieval, and simple
   clarification remain real baselines.
5. **Migrations are part of correctness.** Old-address compatibility,
   descendants, caches, receipts, backups, and explicit failure are tested.
6. **Useful throughput and governance cost travel together.** Quality, unsafe
   release, latency, questions, verifier cost, fallback, abstention, repair,
   and human burden are reported as one frontier.
7. **Negative knowledge is a deliverable.** Failed models, poor facets,
   collisions, evaluator disagreements, regressions, and no-change decisions
   remain in the permanent packet.
8. **No outcome-driven scope expansion.** Freeze workloads, baselines,
   thresholds, budgets, and decision rules before held-out outcomes are read.

## Scope and explicit non-goals

### In scope

- all twelve QCSA normative lanes, implemented at a bounded public-safe scale;
- one preregistered matched-baseline QCSA evaluation;
- one governed vertical reference path across semantic IR, context, claims,
  routing, tools/authority, artifacts, and lifecycle migration;
- structural Lean invariants where finite formalization materially clarifies a
  boundary;
- updates to the nine existing QCSA chapter owners, the integrated reference
  architecture, Appendix C, test/proof hooks, source crosswalks, evidence
  vectors, residuals, and changelog;
- canonical HTML, AI/Human reading modes, and current public truth surfaces;
- a warranted content release or an explicit no-release terminal record.

### Not required for completion

- a new QCSA chapter;
- a production database, distributed service, hardware enclave, or paid cloud;
- external-human prepublication review or outreach;
- universal multilingual or multimodal coverage;
- production tool execution or irreversible real-world effects;
- promotion of any chapter-core claim;
- a DOI, v1.0.0 archive backfill, optional book formats, AGI, or ASI.

## Execution board

| Priority | Initial state | Purpose | Terminal authority |
|---|---|---|---|
| P0 — Activate implementation truth | completed | Install this roadmap, status record, validators, and current public pointers without changing v2.2 history. | Clean deployed public-truth attestation. |
| P1 — Implement the QCSA artifact stack | preregistered | Build the twelve bounded artifacts with schemas, fixtures, replay, and negative controls. | Exact artifact manifest and rejecting validation suite. |
| P2 — Evaluate QCSA and its ablations | pending | Test usefulness, cost, calibration, migration, and failure prevention against matched baselines. | Frozen result ledger and claim-bounded disposition. |
| P3 — Build the governed vertical reference path | pending | Connect QCSA to existing stack owners without merging identity, evidence, or authority. | End-to-end replay, rollback/migration exercise, and residual ledger. |
| P4 — Complete evidence and book reconciliation | pending | Fold implementation results into chapters/products and close selected evidence-floor gaps. | Machine/prose agreement with no unsupported promotion. |
| P5 — Release or honest no-release closure | pending | Validate, publish if warranted, attest, archive, and mark the roadmap terminal. | Exact release transaction or explicit no-release record. |

## P0 — Activate implementation truth

### Required work

- install this roadmap, its schema-bound status record, and a registered
  validator with rejecting mutations;
- update README, landing page, current readiness/reproducibility guidance, and
  the v2.2 completion declaration with a dated successor pointer;
- keep v2.2.0 named as the latest immutable release and `/latest/` mutable;
- preserve all 54 core claims at `argument`;
- identify the nine QCSA chapter owners and twelve implementation lanes exactly;
- run the full deep registry, Lean, render, browser, build, deploy, and public
  attestation chain.

P0 changes planning authority only. It is no implementation or evidence result.

## P1 — Implement the QCSA artifact stack

All artifacts live under one bounded, dependency-light reference package and
one experiment namespace. Prefer standard-library or already pinned
dependencies. Every artifact has a schema, valid fixture, expected-invalid
fixture, deterministic serialization, content digest, version, owner, and
non-claim boundary.

| ID | Artifact | Minimum completion gate |
|---|---|---|
| `QI-01` | Semantic Object Record and SOID registry | Stable opaque IDs; separate occurrence, type, instance, proposition, expression, tool, policy, and obligation kinds; alias/merge/split lineage; duplicate and silent-retarget controls. |
| `QI-02` | Typed temporal evidence hypergraph | Typed nodes/edges; proposition, evidence, provenance, belief, authority, lifecycle, and permitted-use fields remain distinct; contradiction and dangling-reference controls. |
| `QI-03` | Atlas manifest and immutable epoch package | At least three consumer-declared facets; soft variable-length paths; top-k/unknown/conflicting/abstain; codebook digest; candidate versus authoritative epoch. |
| `QI-04` | Semantic Address Certificate | Bind SOID, occurrence/expression, context, task, consumer, epoch, paths, confidence, provenance, grounding, residuals, uses, authority ceiling, validity, migration, digest, and signature fixture. |
| `QI-05` | Question compiler trace | Select internal discriminator, retrieval, bounded tool/sensor fixture, specialist request, or clarification by expected decision value net of compute, latency, privacy, burden, and risk. |
| `QI-06` | Semantic-to-physical route plan and receipt | Lower a valid certificate into model/retrieval/tool/approval/verification/fallback steps; semantic resolution cannot grant authority; every attempted effect receives a receipt. |
| `QI-07` | Migration and rollback record | Immutable epochs; same-SOID compatibility or explicit typed failure; merge/split lineage; shadow evaluation; descendants/caches/backups/receipts inventory; exact rollback. |
| `QI-08` | Adversarial addressing suite | Alias escalation, collision, poisoning, stale epoch, branch overload, route disagreement, certificate tampering, privacy leakage, and missing-residual controls. |
| `QI-09` | Bounded multilingual/multimodal grounding suite | Public-safe paired labels and synthetic modality descriptors; false-equivalence and unsupported-grounding controls; no universal grounding claim. |
| `QI-10` | Semantic round-trip validator | Compare identity, roles, negation, modality, quantity, time, claim/citation bindings, authority, and residuals; include evaluator-disagreement and self-confirmation controls. |
| `QI-11` | Resource and governance ledger | Record latency, bytes/tokens, questions, retrievals, model/tool calls, verifier cost, fallback, abstention, repair, migration, and human burden. |
| `QI-12` | Content-addressed artifact manifest | Bind code, schemas, fixtures, corpora, seeds, configs, results, logs, and environment; reject missing or mutated descendants. |

### P1 implementation constraints

- Use stable IDs and deterministic fixtures; do not smuggle labels into IDs.
- Keep cryptographic-signature behavior explicitly fixture-level unless a real
  verified signing implementation is introduced and reviewed.
- Use adapters for retrieval/model/tool behavior so deterministic unit tests do
  not depend on network access or nondeterministic model availability.
- Fail closed on malformed schema, stale epoch, authority mismatch, unknown
  migration, unresolved collision, or missing receipt.
- Preserve raw candidate and failure artifacts in an excluded/no-grant evidence
  lane when publication or provenance requires it.

## P2 — Evaluate QCSA and its ablations

### Frozen workload

Create a public-safe corpus with train/development/held-out separation and at
least six families:

1. polysemy and same-name/different-object identity;
2. paraphrase and cross-language reference;
3. compositional expressions with roles, negation, modality, quantity, or time;
4. evidence conflict and proposition revision;
5. expert/retrieval/tool route ambiguity with authority differences;
6. atlas migration, merge/split, stale-address, and descendant compatibility.

Include tail concepts, open-world unknowns, deliberate collisions, poisoned
aliases, privacy-sensitive attributes, route disagreement, and cases where the
correct result is fallback, abstention, or human clarification.

### Matched baselines and ablations

- direct inference/retrieval with no semantic address layer;
- flat embedding or lexical retrieval under matched corpus and budget;
- one fixed hierarchy;
- random and frequency-derived trees;
- direct clarification without a learned/adaptive question policy;
- QCSA without plural facets;
- QCSA without active questions;
- QCSA without stable identity/address indirection;
- QCSA without certificate/residual/authority fields;
- QCSA without migration compatibility.

### Metrics

Report per family and in aggregate:

- object-resolution and task-decision accuracy;
- calibration, selective risk, fallback, abstention, and clarification rate;
- questions, retrievals, tool/model calls, latency, bytes/tokens, verifier and
  human burden;
- collision, poisoning, stale-epoch, migration, authority, and route-disagreement
  failures prevented and missed;
- semantic round-trip structural loss and evaluator disagreement;
- repair locality, compatibility, rollback identity, and residual count;
- a Pareto frontier rather than one blended score.

### Decision rules

Preregister exact thresholds before held-out execution. At minimum:

- no performance-advantage claim without a matched-resource Pareto improvement
  reproduced across seeds and multiple families;
- no semantic-preservation claim from the same generator/evaluator pair alone;
- no safety claim from certificate integrity, graph position, or blocked fixture
  behavior;
- no authority claim unless the separate authority route rejects semantic
  alias/address escalation;
- narrow or reject QCSA where its overhead adds no decision, migration, or
  governance value.

P2 closes with a `promote`, `narrow`, `no_change`, `demote`, or `refute`
disposition for each reached non-core claim. Core claims move only through the
ordinary evidence-transition process and are expected to remain unchanged
unless every dimension actually qualifies.

## P3 — Governed vertical reference path

Build one public-safe task that crosses existing chapter boundaries:

```text
intent -> semantic IR -> SOID/SVA resolution -> evidence graph
       -> question compiler -> context materialization -> route plan
       -> independent authority decision -> bounded adapter action
       -> verification -> artifact/receipt graph -> migration/rollback replay
```

### Required properties

- typed artifacts and content digests at every handoff;
- no hidden state transfer between identity, evidence, routing, and authority;
- least-authority adapter behavior with approval expiry and irreversible-effect
  refusal;
- claim ledger updates that preserve contradiction and provenance;
- effect inventory, first-effect observation, rollback, descendant
  invalidation, and residual custody;
- replay from a clean environment;
- negative paths for stale certificate, poisoned alias, wrong SOID, conflicting
  evidence, inadequate context, authority widening, verifier disagreement,
  migration ambiguity, and incomplete rollback;
- one readable trace used by the Integrated Reference Architecture chapter.

The reference path may use local files and deterministic adapters. It must not
be represented as production deployment or open-world system validation.

## P4 — Evidence and book completion

### Chapter reconciliation

Update existing owners first:

- `cognitive-compilation-and-semantic-ir`;
- `virtual-context-abi`;
- `claim-ledgers-and-belief-revision`;
- `runtime-adapters-tool-permissions-and-human-approval`;
- `inter-stack-protocols-identity-and-economic-exchange`;
- `routing-heads-and-specialist-cores`;
- `compact-generative-systems-and-residual-honesty`;
- `data-engines-continual-learning-and-unlearning`;
- `integrated-reference-architecture`.

Also update the prototype roadmap, living-book methodology, and open research
agenda when the implementation changes their concrete next actions.

### Evidence-floor closure

- every implemented QCSA/vertical artifact has a registered validator and
  rejecting negative controls;
- every affected chapter names what was built, what passed, what failed, what
  remains residual, and what would justify stronger support;
- Appendix C, evidence vectors, non-core transitions, per-chapter evidence
  plans, proof/test manifests, source appendices, and residual ledgers agree;
- finite Lean work is added only for invariants such as identity stability,
  migration non-retargeting, evidence/address separation, and
  resolution-without-authority;
- local replay does not become external independence, production transfer, or
  universal validity;
- the old QCSA ingestion validator is strengthened or paired with an
  implementation validator so “no implementation” text cannot remain current
  after artifacts exist.

### New-chapter gate

Keep 54 chapters unless all of these become true:

1. QCSA has a working artifact stack and measured result;
2. it owns a distinct reader question and lifecycle not cleanly owned by the
   nine current chapters;
3. at least two current chapters would otherwise duplicate substantial core
   mechanism prose;
4. source, proof, test, implementation-horizon, and handoff contracts are ready;
5. the change improves the narrative and reference projections;
6. validation and render pass after the manifest change.

Even then, a consolidation or dedicated chapter is optional, not automatic.

### Book-product closure

- canonical HTML and both reading modes remain coherent over all active chapters;
- current README, landing page, citation, readiness, reproducibility, rights,
  roadmap, release, and version-index surfaces agree;
- source and evidence counts are generated, not hand-maintained;
- no prepublication external-human review is required or claimed;
- optional formats retain explicit blockers and are not silently promoted;
- no duplicate active roadmap or stale candidate identity remains.

## P5 — Release or honest no-release closure

Select a version only after P1–P4 dispositions and release scope are known. A
release is warranted for a meaningful implementation/evidence/book delta even
when the empirical result is negative. If no release is warranted, publish an
exact no-release record and keep the mutable channel truthful.

Any release must bind one clean tested commit to:

- deep validation registry and Lean results;
- clean Quarto render and full browser checks;
- canonical public status and product projections;
- commit-bound tested bundle;
- deployment without rebuilding;
- public status/chapter-graph attestation;
- exact citation/version metadata and tag-bound rights routing;
- release record, completion declaration, and version-index row;
- deterministic immutable site archive and public redownload SHA-256.

## Milestones

| Milestone | State at activation | Completion evidence |
|---|---|---|
| M0 — Roadmap authority installed | completed | Roadmap, schema, status record, validator, registered contract, and goal. |
| M1 — Public activation reconciled | completed | Commit `65120df163822a423952fe43a2231e5c65125327`; build `29228034217`; deploy/attest `29228280321`. |
| M2 — QCSA implementation frozen | in progress | Architecture decision record, package manifest, schemas, fixtures, budgets, and test plan. |
| M3 — QCSA artifact stack implemented | pending | `QI-01` through `QI-12` pass deterministic replay and negative controls. |
| M4 — QCSA evaluation dispositioned | pending | Frozen held-out results, baselines, ablations, costs, residuals, and decisions. |
| M5 — Vertical reference path complete | pending | Clean replay, adversarial paths, migration/rollback exercise, and readable trace. |
| M6 — Book/evidence reconciliation complete | pending | Chapters, appendices, ledgers, vectors, tests/proofs, products, and changelog agree. |
| M7 — Release/no-release transaction complete | pending | Immutable release chain or exact no-release declaration; roadmap terminal. |

## Risk register

| Risk | Trigger | Required response |
|---|---|---|
| Demo masquerades as evidence | One curated trace is used to imply general quality. | Keep it as implementation evidence; require P2 held-out comparisons. |
| Label leakage | SOIDs, paths, facets, or questions encode answers. | Regenerate identifiers, audit split isolation, and invalidate descendants. |
| Evaluator self-confirmation | Generator and round-trip judge share method or labels. | Add an independent implementation and preserve disagreements. |
| Semantic laundering | Address, graph position, or SAC becomes truth/authority. | Fail validation and add explicit claim/authority decisions. |
| Migration retargeting | Old address silently changes object identity. | Block release, restore epoch, replay descendants, and record residuals. |
| Governance overhead dominates | QCSA adds cost without useful gain or failure prevention. | Narrow or reject the affected design claim. |
| Scope explosion | Full ontology, production graph, or universal grounding is attempted. | Return to the bounded corpus and twelve exact lanes. |
| Chapter sprawl | QCSA is added as a chapter before it owns distinct evidence/lifecycle. | Enforce the six-part new-chapter gate. |
| Hidden effect | Adapter changes a surface absent from the inventory. | Quarantine, repair observer coverage, rerun rollback, preserve failure. |
| Release overclaim | Code existence is represented as safety, transfer, or ASI progress. | Block release until language and records are corrected. |

## Definition of done

This roadmap is complete only when:

- P0–P5 and M0–M7 are terminal and the machine record agrees;
- all twelve QCSA lanes have implemented artifacts or explicit evidence-backed
  rejection/narrowing dispositions;
- the matched evaluation and its baselines/ablations are frozen, replayed, and
  dispositioned without outcome-driven changes;
- the governed vertical path replays from intent through migration/rollback and
  preserves identity/evidence/authority separation;
- every affected claim, chapter, appendix, vector, test/proof hook, source,
  residual, product, and changelog surface agrees;
- no core claim, new chapter, optional format, rights grant, independence
  statement, safety statement, or transfer statement exceeds its evidence;
- the complete local and hosted validation/proof/render/browser chain passes;
- the deployed site publicly attests the exact completion commit; and
- a warranted immutable release is archive/redownload verified, or an exact
  no-release decision is recorded.

Completion does not require favorable results, external-human prepublication
review, production deployment, optional formats, DOI work, universal semantic
grounding, AGI, or ASI.

## Canonical execution prompt

> Execute `docs/post_v2_2_implementation_completion_roadmap.md` to completion.
> Implement QCSA first as twelve bounded, schema-validated, replayable artifact
> lanes; freeze and run matched baselines and ablations; then build one governed
> vertical reference path across the existing ASI Stack owners. Preserve
> identity/address/evidence/authority separation, failures, costs, residuals,
> and negative results. Improve existing chapters before adding any chapter,
> move support only through accepted evidence transitions, keep optional
> formats and prepublication external-human review out of scope, and do not
> stop until the definition of done is honestly satisfied through a clean
> release or exact no-release closure.

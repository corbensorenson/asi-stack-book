# Source Note: Spinoza Composer / Spinoza Trinity

| Field | Value |
|---|---|
| Source ID | `spinoza_composer` |
| Source family | Ten-tab, roughly 15,500-word lineage from narrative/compliance Trinity through style-cloning and “media foundry” variants to the bounded-coherence v3.0 operational edition |
| Ingestion date | 2026-06-24; section-family fidelity audit completed 2026-07-31 |
| Source version / URL | Multiple February 2026 drafts; controlling claim boundary is “A Bounded-Coherence Foundry for Multi-Modal Media Production,” v3.0 dated 2026-02-07; https://docs.google.com/document/d/1pWHPNCFL5dnphZxKUhj5c_yk3juskWQZPTzPjxE7nEE |
| Canonical local cache | `sources/raw/google_docs/spinoza_composer.txt`; raw text is not published by this note |
| Evidence boundary | Architecture and product specifications, pseudocode, schemas, workflow designs, estimated costs, illustrative target metrics, proposed baselines, and self-red-team revisions. No Composer implementation, extraction run, evidence/canon graph, section or scene compiler, visual continuity system, style adapter, benchmark, user study, ROI result, video deployment, or content-credential export is present. |

## Thesis

Spinoza Composer treats text and media production as **bounded probabilistic
compilation**. Evidence, artifact commitments, section plans, scene plans,
generated outputs, validation observations, model/backend choices, human
decisions, and delivery state remain separate artifacts linked through a
dependency graph. The stable substrate is not one model or one mutable
“knowledge graph”; it is an append-only evidence store, rebuildable evidence
views, a versioned human-approved canon, explicit section/scene contracts, and
an audit bundle that survives model replacement and partial failure.

Its strongest insight is about handoffs. Research can contradict a script; a
script can contradict visuals; shots can drift from one another; a fluent
renderer can invent facts while preserving style; and external provenance
metadata can be stripped. Cross-modal consistency therefore needs typed
contracts and observable deltas at every boundary rather than a single final
judge or “source of truth.”

The controlling v3.0 draft deliberately narrows the earlier family. It no
longer promises deterministic rendering, zero violations, immutable semantic
graphs, autonomous filmmaking, perfect style cloning, or global coherence. It
models validators as probabilistic sensors, bounds lookback and retries,
separates append-only records from recomputable views, declares video optional,
forecasts cost, supports predeclared degraded delivery, and makes human canon
authority explicit. The book should preserve that correction path.

## Claim Boundary and Variant Lineage

The ten tabs are related architectural revisions. Repeated mechanisms do not
count as independent evidence, and labels such as “gold master,” “definitive,”
and “product-grade” do not imply working software.

| Tabs | Lineage role | Durable contribution or disposition |
|---|---|---|
| 1–2 | Trinity narrative/compliance baseline | Ingestor/engine/composer split, world graph versus agent-relative belief, causal state history, valid/invalid/conditional transitions, event-to-semantics bridge, Dream/Audit modes, and continuity metrics. Retain representation and workflow; reject deterministic prose and proof-like claims. |
| 3 | scalability and temporal correction | Recursive extraction, active shards and ghost references, weighted soft constraints, AMR checking, causal time versus narrative order, logical-debt patches, and solver-timeout fallback. Retain time separation and scoped shards; reject the claim that an LLM fallback preserves verification. |
| 4–5 | style-cloning editions | Hierarchical communities, weighted relaxation formula, style profiles/adapters, self-checked patches, MVP steps, watermarking, and style metrics. Preserve style as a rights-bearing asset and logic/render separation; reject unverified training-time, hardware, complexity, fidelity, authorship, and “archiving consciousness” claims. |
| 6 | grand-unified media-foundry sketch | Supply-chain framing, pairwise checks, routing, optional visual director, proof bundle, and source map. Retain cross-modal custody; RAIV and “two-body limit” are heuristic labels, not validated theory. |
| 7 | detailed four-phase v1.0 spec | Information classes, version clocks, pairwise validation, format profiles, model-tier routing, local style storage, scene decomposition, visual state buffer, rejection sampling, post-production, costs, and failure inventory. Retain record fields and baselines; all prices and success rates are estimates. |
| 8 | v1.1 evidence/canon correction | Evidence Graph versus Canon Graph, typed conflicts, hard/soft/interpretive constraints, local and global checks, separately approved deviations, section/scene contracts, element/reference packs, stakes profiles, audit bundle, and explicit non-goals. Strong architectural precursor. |
| 9 | v1.2 external-comparator enrichment | Schema-first extraction, entity resolution, community summaries, guarded repair loops, quality instrumentation, content credentials, and capability-class routing. Retain mechanisms; vendor/tool references are comparators, not implemented dependencies or results. |
| 10 | v3.0 controlling operational edition | Append-only evidence plus versioned views, draft/active canon, conflict-first review, poison recovery, disagreement-aware validators, false-positive control, synthesis budgets, bounded video tiers, cost forecasts, partial-delivery taxonomy, roles, rollback, disclosures, baselines, success criteria, and text-first MVP. This boundary controls earlier conflicts. |

The source does not establish that a graph is ground truth, that pairwise checks
solve global consistency, that AMR preserves every relevant meaning, that a
visual verifier reliably detects identity or object state, that reference
conditioning yields continuity, or that a style adapter preserves voice. It
does not establish the stated cost, quality, HCSR, PCR, contradiction,
continuity, or productivity targets.

## Conceptual Primitives

- **Evidence Store (ES).** Append-only source-derived records retaining raw and
  normalized claim, structured fields where possible, modality, polarity,
  confidence, exact pointer, extractor/version/config, quotation scope,
  conflicts, and taint/security flags.
- **Evidence View (EV).** Rebuildable projection for resolved entities,
  aliases, clusters, communities, summaries, and search. A changed resolver or
  clustering model generates a new view; it does not rewrite evidence.
- **Draft Canon.** Machine-assembled candidate commitments derived from
  evidence, heuristics, and user intent. It cannot constrain accepted output
  merely because an extractor proposed it.
- **Active Canon / Canon Store (CS).** Versioned human- or policy-approved
  artifact commitments, rules, entity/state definitions, uncertainty, and
  continuity constraints. Approval is scoped to one project and stakes mode.
- **Dependency Graph (DG).** Links evidence, views, canon nodes, contracts,
  generated segments, shots, validations, disclosures, and final artifacts so
  source taint or canon change can trigger bounded regeneration.
- **World/fact versus belief scope.** Objective artifact commitments,
  narrator/source assertions, reported speech, character/agent beliefs,
  opinion, estimate, fiction canon, and instructions are different modalities.
- **Causal time versus presentation time.** State changes advance on a causal
  timeline while a renderer may reveal them in a different narrative order.
  Flashback placement cannot rewrite causal state.
- **Logical debt.** Deferred constraint violation recorded during a low-
  friction drafting mode. It remains a blocker, warning, or explicit accepted
  deviation; silence is not resolution.
- **Deviation proposal.** Candidate change to a soft constraint with claimed
  benefit, cost, severity, reversibility, and downstream delta. The generator
  cannot approve its own proposal or alter hard canon implicitly.
- **Section Contract.** Required and forbidden claims, evidence/synthesis
  state, entity/state assumptions, uncertainty language, format/tone, risk,
  retry, time, and human-intervention budgets for a text unit.
- **Scene Contract.** Required entity and element identities, props, actions,
  setting, time, lighting, continuity locks, forbidden elements, duration,
  camera hints, and acceptable variance for a visual unit.
- **Element Pack.** Hashed/versioned reference frames, character sheets, prop
  turnarounds, location plates, palette, and camera/style constraints. It is a
  conditioning and audit asset, not a guarantee of visual identity.
- **Continuity Buffer.** Observed entities, attributes, props, positions,
  lighting, and uncertainty extracted from accepted frames/shots for the next
  boundary check. Observations remain fallible and distinct from canon.
- **Capability-class route.** Planner, writer, extractor, verifier, and vision-
  verifier roles selected by constraint density, conflict load, failure
  history, stakes, cost, and backend availability rather than vendor name.
- **Synthesis budget.** Maximum ungrounded or explicitly assumptive content
  permitted for a project or segment before disclosure, review, downgrade, or
  abort.
- **Provenance & Audit Bundle.** Inputs, hashes, evidence and canon exports,
  view/version history, contracts, prompts/templates, routes, validations,
  repairs, deviations, element packs, continuity observations, backend pins,
  human approvals, costs, residuals, and final artifact hashes.
- **External content credential.** Portable signed provenance metadata such as
  C2PA-compatible records. It complements but cannot replace the internal
  bundle because metadata may be incomplete, stripped, or valid while content
  is false.

## Mechanisms

### Append-only evidence, rebuildable interpretation, governed commitment

The final architecture corrects the earlier “immutable Evidence Graph” phrase.
Extraction records are append-only, but entity resolution, deduplication,
community detection, confidence aggregation, and summaries are fallible views
that must be rebuilt when models, policies, or sources change. Canon is a
separate governed commitment layer. This prevents an extractor's hallucinated
merge or summary from becoming history.

Each ingested statement records modality and quotation scope. Quoted or
imperative source text remains data rather than execution policy. Suspect spans
are quarantined; source snapshots are retained where rights permit; extraction
uses schema-only output and no tool authority; disagreement is a signal for
review rather than truth. When a source is poisoned, taint propagates through
the dependency graph to views, canon, contracts, and outputs, and only the
affected closure is rebuilt and reapproved.

### Draft canon, conflict-first review, and impact-aware deltas

Users interact with continuity bibles, claim ledgers, and diffs rather than raw
graph topology. Machine-assembled Draft Canon becomes Active Canon only after
the designated authority accepts exact commitments and uncertainty. Review is
prioritized by conflicts, centrality, stakes, outliers, and impact radius;
sampling and trusted-source rules reduce routine burden but remain auditable.

Every canon delta shows source/change reason, affected descendants, available
accept/reject/uncertain routes, and rollback. Restoring an old canon version
does not silently make newer outputs current; those outputs retain stale-versus-
current badges and require regeneration or explicit bounded acceptance.

### Contracted text compilation and validators as sensors

Before generation, each section receives a contract. The generator produces a
candidate and a structured state/claim delta. Deterministic checks validate
schema, identifiers, pointers, and required fields. NLI or model judges inspect
possible contradiction, relevance, and groundedness. Diverse validators may
vote, but disagreement triggers escalation and confidence gates; it is not
averaged into truth. Low-confidence minor findings can be warnings, while
high-impact uncertainty cannot silently pass.

The validator paradox is explicit: the same model class that generated a
mistake may also miss it. Evaluation therefore reports false positives, false
negatives, judge dependence, disagreement, escalation, retries, and human
overrides. A repair loop is bounded by retry, time, cost, and intervention
budgets and must end in pass, warning with policy, fail, escalation, alternate
backend, or residual—not infinite “self-healing.”

### Local interaction checks, global lints, and time

Pairwise checks are a cheap local filter for reachability, possession,
knowledge, and rule preconditions among interacting entities. Global passes
check conservation, location exclusivity, entity lifecycle, temporal order,
reference resolution, unresolved claims, and cross-segment dependencies. The
pairwise route does not solve higher-order or long-range consistency; it lowers
the cost of finding a subset of violations.

The source's causal/presentation time distinction is retained. A flashback can
be rendered later while reading an earlier causal snapshot. State vectors,
valid time, presentation position, and transaction/version time therefore need
separate fields. “Ghost references,” active shards, community summaries, and
lazy loading are candidate retrieval optimizations, not proof that the omitted
graph cannot matter.

### Soft deviations and logical debt

Dream mode may log constraint debt rather than interrupt drafting. Audit mode
offers a patch, explicit canon change, uncertainty label, rejection, or retained
anomaly. An automated repair proposal is simulated and checked before user
review, but it never self-approves a canon change.

The early rigidity coefficient, resonance score, and RAIV formula are useful as
examples of typed tradeoff inputs, not validated decision rules. A model-rated
“story value” or sentiment score can reward spectacle and launder a violation.
Only soft constraints are eligible, the rubric and threshold are prospective,
the deviation and downstream cost remain visible, and high-stakes modes can
forbid the route entirely.

### Visual compilation, continuity, and bounded degradation

Text is decomposed into scene/shot contracts that refer to stable Element Pack
identities. Backend selection escalates from simple generation to reference-
conditioned image-to-video, stock, diagrams, CGI, or manual work depending on
identity risk and prior failures. A vision route extracts observed state into a
continuity buffer, compares it to the contract, and records pass/warn/fail plus
confidence and disagreement.

The final paper wisely narrows video into V0 slides/diagrams, V1 short-form, and
V2 hybrid longer-form routes. Retry caps and total human/spend limits are fixed
before generation. Budget exhaustion uses a preselected terminal policy:
**Finish-Low** with visible warnings/watermarks, **Finish-Hybrid** with reliable
substitutes, or **Stop-Clean** with completed segments plus the script/shot list
for the rest. Completion probability and p50/p90 cost forecasts are decision
inputs, not promises.

### Style assets, rights, and output provenance

Style samples, adapters, prompts, and profiles are a distinct asset family with
ownership/license, consent, permitted transformations, locality, disclosure,
expiry, deletion, and model-compatibility constraints. Lexical fingerprints,
perplexity, LoRA/QLoRA, and local storage do not establish authorial identity,
ethical permission, privacy, fidelity, or non-infringement. The source's named-
author imitation examples and “archiving consciousness” language are rejected
as claims.

The internal audit bundle answers why each fact, canon choice, section, scene,
or visual element exists. External credentials can expose origin and
transformation metadata across tools, but the internal bundle remains because
distribution pipelines may strip credentials and a valid signature does not
prove content accuracy or consent.

## Interfaces and State Machines

Evidence moves through captured, extracted, quarantined, contested, tainted,
superseded, and retained/tombstoned states. Views move through built, current,
stale, rebuilding, failed, and retired. Canon nodes move through draft,
reviewed, active, uncertain, disputed, changed, rolled-back, and retired.
Sections and shots move through contracted, generated, observed, validated,
warned, failed, repairing, escalated, accepted, disclosed, and residual.

Source/Data owners control admission, rights, snapshots, and taint. Claim
Ledgers own evidence and canon commitment state. Planning/Cognitive Compilation
own section and scene decomposition. Routing owns capability proposals.
Artifact Graphs own dependency, lineage, replay grade, and stale closure.
Authenticity owners control external credentials and disclosure. Security and
Privacy own untrusted ingest, style assets, collaboration roles, access,
retention, and deletion. Resource Economics owns retry, model, human, storage,
and opportunity cost. Accountable humans own canon approval, high-impact
deviation, disclosure acceptance, partial-delivery policy, and publication.

## Evidence

The source family contains detailed schemas, workflow phases, equations,
pseudocode, UX patterns, state distinctions, security threats, model/backend
routing ideas, output formats, evaluation metrics, baseline plans, target
thresholds, and extensive revision in response to criticism. The later drafts
correct several important conceptual errors: evidence versus canon, immutable
events versus mutable views, local checks versus global coherence, validators
as sensors, generator versus approval authority, and full delivery versus
bounded degradation.

All numerical statements remain proposals or illustrations. This includes
complexity reductions, 50-page/30-minute style training, first-pass video
success, per-video dollar costs, routing savings, contradiction reduction,
provenance improvement, review-time reduction, HCSR/PCR floors, retry budgets,
human-review caps, benchmark targets, and MVP success criteria. The source
contains no artifacts that establish them.

## Evaluation and Falsifiers

A serious Composer study freezes contracts and authority before outcomes and
compares against prompted LLM+RAG+self-critique, conventional human continuity
practice, current video generation plus human cleanup, and ablated Composer
variants. It should report:

- extraction precision/recall, entity resolution, conflict preservation,
  quotation/instruction separation, and poison recovery closure;
- evidence-to-canon decision quality, review burden, false accepts/rejects,
  and rollback/staleness propagation;
- section/scene contract coverage, local and global violation rates, validator
  calibration, judge dependence, and repair success;
- factual provenance coverage, synthesis and unresolved rates, usefulness of
  pointers, and metadata survival;
- identity/prop/timeline/audio/visual drift, first-pass success, retry and
  escalation rates, and human intervention by content tier;
- style utility together with rights, privacy, consent, attribution, and
  unwanted imitation outcomes;
- completion, partial-delivery usefulness, cost forecast calibration, p50/p90
  spend, latency, storage, review, and rework; and
- delayed publication errors and real production outcomes, not only internal
  validator agreement.

The architecture should be narrowed or rejected if evidence/canon separation
does not reduce harmful commitment errors; contracts increase rework without
improving accepted outputs; validators are too correlated or noisy; dependency
closure misses poisoned descendants; visual retries exceed reliable hybrid
production; style features create disproportionate rights/privacy harms; or a
simpler continuity bible plus accountable editor matches quality and cost.

## Failure Modes

- **Evidence/canon collapse:** an extracted or summarized statement silently
  becomes an artifact commitment.
- **View mutation:** entity-resolution or community-summary output rewrites
  append-only source history.
- **Instruction smuggling:** quoted imperatives or malicious documents become
  runtime/canon authority.
- **Conflict erasure:** one source or model-confidence score removes contested
  alternatives.
- **Graph grooming tax:** users spend more time repairing topology than making
  the artifact.
- **Validator paradox:** correlated model judges miss the same error or create
  false-positive “Jira for prose.”
- **Pairwise sufficiency theater:** local interaction checks are narrated as
  global or higher-order consistency.
- **Shard omission:** lazy loading excludes a distant dependency that matters.
- **Self-approved deviation:** a generator assigns high narrative value to its
  own violation.
- **Logical-debt laundering:** deferred violations disappear at publication.
- **Repair loop:** retries consume cost without changing the failure cause.
- **Synthesis escape:** ungrounded content stays below the disclosure surface
  through atomization or denominator gaming.
- **Visual state hallucination:** the vision verifier writes a wrong continuity
  buffer that compounds across shots.
- **Reference-pack overclaim:** conditioning assets are treated as identity
  guarantees.
- **Style appropriation:** a style adapter is trained or shared without rights,
  consent, disclosure, privacy, or deletion controls.
- **Credential theater:** signed metadata is treated as factuality, consent, or
  complete internal lineage.
- **Budget surprise:** retries and human work exceed the declared limit without
  a typed overage or partial-delivery decision.
- **Polished partial failure:** a complete-looking export hides missing,
  degraded, contested, or unreviewed segments.

## Book Chapters Supported

- `artifact-graphs-audit-logs-and-replay` (Artifact Graphs, Audit Logs, and Replay)

The deep audit also reconciles adjacent ideas against Cognitive Compilation,
Claim Ledgers, Content Authenticity, Routing, and Resource Economics. Those
chapters already own the relevant generic mechanisms and comparators; this
source remains manifest-assigned only where it contributes the distinct
cross-modal artifact lineage.

## Claims To Add Or Update

- Separate append-only evidence records, rebuildable interpretation views,
  draft canon, active canon, and output dependency closure.
- Record statement modality and quotation/instruction scope so source text
  cannot self-promote into behavioral or canon authority.
- Treat Section and Scene Contracts as cross-modal compilation artifacts with
  required, forbidden, uncertainty, state, provenance, budget, and acceptance
  fields.
- Treat semantic and vision validators as fallible sensors with disagreement,
  calibration, false-positive/negative, and escalation records.
- Add predeclared video tiers, retry/human/spend budgets, and Finish-Low,
  Finish-Hybrid, and Stop-Clean terminal routes.
- Preserve Element Pack and continuity-buffer lineage without claiming visual
  identity guarantees.
- Keep internal audit bundles distinct from portable content credentials.
- Preserve style assets as rights-bearing governed objects and reject the
  source's unvalidated fidelity, hardware, cost, and authorship claims.

## Section-Family Closure Ledger

| Section family | Disposition |
|---|---|
| Continuity crisis, handoffs, and non-goals | Added to Artifact Graphs as cross-modal custody pressure. |
| Ingestor/world graph/narrative tree | Recast as append-only evidence, versioned views, scoped beliefs, and causal history; retained in note and Artifact Graphs. |
| Evidence versus canon | Added directly to Artifact Graphs; final event/view correction controls earlier “immutable graph” language. |
| State sharding, community summaries, ghost refs | Retained as retrieval optimizations with omission residuals; no complexity result. |
| Weighted relaxation, RAIV, Dream/Audit, logical debt | Retained as governed soft-deviation workflow; formulas are unvalidated heuristics and cannot self-approve. |
| Causal versus narrative time | Integrated as a bitemporal/presentation-time artifact requirement. |
| AMR/event-to-semantics bridge | Retained as candidate semantic IR with explicit bridge-verification limits. |
| Section contracts and polymorphic formats | Added to Artifact Graphs and cross-referenced to Cognitive Compilation; no new chapter needed. |
| Model-tier/capability routing | Retained in source note; existing Routing chapter already owns vendor-independent specialist routing. |
| Style cloning, Mimic, LoRA/QLoRA, watermark | Routed to style-asset rights and authenticity boundaries; performance and consciousness language rejected. |
| Scene contracts, Element Packs, continuity buffer | Added to Artifact Graphs as visual artifact custody. |
| Pairwise checks, global lint, guarded repair | Added with local/global and validator-sensor distinctions. |
| Provenance/audit bundle and C2PA | Added to Artifact Graphs; external credential remains complementary and non-truth-bearing. |
| Security, poison recovery, collaboration roles | Added to dependency-closure and interface duties; no security result. |
| Video tiers, budgets, forecasts, partial delivery | Added as explicit terminal-state and residual design. |
| Metrics, baselines, cost/ROI, target thresholds | Retained as research obligations; no result promoted. |
| MVP and phased delivery | Retained as implementation ordering, not project readiness evidence. |

## Open Questions

- Can evidence/canon separation improve real review outcomes without creating an
  unsustainable canon-maintenance burden?
- How should higher-order, long-range, and cross-modal constraints be sampled
  when pairwise and bounded-lookback checks are insufficient?
- Which validator families are independent enough to make disagreement useful?
- Can a vision route distinguish an absent object from occlusion, camera angle,
  or extraction failure well enough for continuity custody?
- What dependency granularity permits safe incremental regeneration without
  missing semantic effects?
- Which partial-delivery policies remain honest and useful for high-stakes
  content?
- How should style likeness, authorship, consent, privacy, licensing, and
  deletion be evaluated independently of surface similarity?

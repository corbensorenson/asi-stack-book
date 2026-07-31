# Source Note: Proof of Belief / The Spinoza Architecture

| Field | Value |
|---|---|
| Source ID | `spinoza` |
| Source family | Twelve-tab, roughly 26,600-word lineage from v2.1 through v4.2 plus a separately authored v5.0 deployment rewrite and a phenomenology-inspired extension memo |
| Ingestion date | 2026-06-24; section-family fidelity audit completed 2026-07-31 |
| Source version / URL | Multiple February 2026 drafts; the controlling bounded architecture is v4.2 dated 2026-02-08; https://docs.google.com/document/d/1Y90DBgxsOJImMXi4aOrwxtbyjlkVZpCzu1YJy_SFatk |
| Canonical local cache | `sources/raw/google_docs/spinoza.txt`; raw text is not published by this note |
| Evidence boundary | Architecture prose, formal sketches, pseudocode, worked compliance examples, proposed schemas, threat models, benchmark designs, target ranges, illustrative economics, and editorial red-team corrections. No Spinoza implementation, autoformalizer, proof engine, FIMO registry, belief-maintenance service, semantic-escape benchmark, compliance pilot, user study, security assessment, or production deployment is present. |

## Thesis

Spinoza is a governed epistemic engine for bounded, high-cost-error domains. It
separates heuristic proposal from artifact-specific verification and from
durable belief maintenance. A claim becomes a commitment only through a typed
justification: a kernel-checkable proof, an explicit mapping to versioned
normative text, a replayable deterministic procedure, or a clearly
non-committal speculative route. The system keeps proposition identity,
interpretation, justification, tier, validity, provenance, entrenchment,
compartment, dependencies, and governance history in a persistent hypergraph.

The deepest idea is not “attach a theorem prover to an LLM.” It is that formal
validity, semantic fidelity, source authority, reproducibility, persistence,
revision, action authority, and public wording are different questions. A
proof of the wrong formalization is a **certified delusion**. A citation without
an applicability and interpretation record is not compliance. A procedure can
be perfectly replayable while encoding the wrong standard. An unresolved
contradiction cannot be hidden by choosing the artifact with the strongest
badge.

The revision lineage matters. Early drafts claim that symbolic truth, vector
anchors, strict gatekeeping, and graph surgery yield an inherently consistent
auditable mind that can rewrite its own axioms. Later drafts progressively
remove those claims, make formal scope explicit, treat autoformalization as the
dominant risk, add unknown and timeout routes, prohibit autonomous foundational
change, introduce norm-anchored rather than “compliant” claims, and measure
semantic escape, silence, fatigue, proof laundering, and total utility. The
book should use that bounded final interpretation.

## Claim Boundary and Variant Lineage

The twelve tabs are revisions and critiques of one source family, not twelve
independent corroborating papers. “Final,” “gold,” “release candidate,” and the
separately generated v5.0 label communicate editorial intent, not empirical
maturity.

| Tabs | Lineage role | Durable contribution or disposition |
|---|---|---|
| 1 | v2.1 maximalist baseline | Neural proof-sketch proposer, symbolic gatekeeper, graph revision, personality weights, anomaly buffer, and self-rewriting vision. Retain proposer/verifier/reviser separation; reject “cannot believe what it cannot prove,” global consistency, vector-grounding, and autonomous axiom replacement claims. |
| 2 | v3.0 first de-risking | Three-valued verifier result, tiered epistemology, grounding regress, proof cache, constitutional sandbox, and bounded-domain prototype. Retain unknown and governance routes; proof caching does not settle invalidation or semantic adequacy. |
| 3 | v3.1 full system model | Typed formal scope, proof-carrying hypergraph, mandatory provenance, bounded autoformalization, explicit AGM-style revision, output tiers, protected axioms, threats, falsifiable metrics, and implementation stages. This is the first coherent engineering specification. |
| 4 | v3.2 semantic and operational hardening | Interactive/analyst modes, round-trip semantic validation, proof-cache lifecycle, silence/paralysis and cost-of-error utility, schema evolution, law-change handling, anti-proof-laundering compartments, and latency policy. Retain the mechanisms, not the claim that rendering alone prevents mismatch. |
| 5 | v3.3 product/legal correction | Deterministic “Ugly English,” multi-candidate alignment, trusted templates, a norm-anchored Tier 2a, semantic isolation, executive/audit dual output, semantic-escape and confirmation-fatigue metrics, and GDPR cases. Retain citation-plus-interpretation discipline; reject “citation-backed compliance” as a truth label. |
| 6–7 | v4.0/v4.1 operational specification | Proof/citation/procedure hypergraph, FIMO, hardened TTR, trust decay, quantified coverage, stratified re-audit, adversarial grinding detection, governed schema/axiom/bridge evolution, bounded revision, running cases, structs, algorithms, and append-only logs. Proposed thresholds and trust packs are unvalidated design parameters. |
| 8 | separately authored v5.0 deployment rewrite | “When not to use Spinoza,” integration/economic framing, cold-start curve, ROI example, and GDPR pilot targets. Preserve the decision variables and falsifiable study design; treat all observed-production language, dollar figures, coverage curves, error reductions, and pilot baselines as hypothetical or unsupported. |
| 9–10 | compact v4.0/v4.1 gold candidates | Formalized multi-factor TTR, CDIT, least-privilege bridges, three T2a subtiers, contradiction arbitration, explicit SER construction, threats, and output contract. These govern the technical interpretation before tab 12. |
| 11 | extension memo | Intentional noema/noesis fields, lifeworld anchor sets, bridge compatibility, a metacognitive monitoring tier, and user trust calibration. Retain operational meaning/proposal metadata and background-assumption review; philosophical analogy is lineage, not evidence. |
| 12 | v4.2 controlling bounded draft | Integrates intentional structure, lifeworld-aware compartments, T0 monitoring claims, FIMO, CDIT, TTR trust vector, cross-tier arbitration, threats, outputs, and falsifiable metrics. Its claim boundary controls where earlier drafts conflict. |

The source does not establish that LLMs cannot reason, that vectors are never
useful epistemically, that theorem proving makes claims true in the world, that
AGM postulates solve natural belief revision, that deterministic rendering is
semantically reversible, or that law can be compiled into unique conclusions.
It does not prove reductions in error, review time, or cost. It supplies a
governed architecture and an evaluation program.

## Conceptual Primitives

- **System 1 / proposer.** Untrusted generator of candidate formalizations,
  proof sketches, citations, interpretation mappings, retrieval hints, and
  revision proposals. Embeddings and models may prioritize candidates but do
  not assign commitment state.
- **System 2 / verifier and binder.** Artifact-specific checker. It kernel-
  checks proof terms, validates pinned citation spans and FIMOs, replays
  deterministic procedures, or checks monitoring logs. Checker acceptance is
  bounded to the exact artifact and scope.
- **System 3 / maintainer.** Contradiction detector and bounded reviser. It
  extracts a conflict slice, searches candidate retractions within a budget,
  applies entrenchment policy, invalidates dependents, rechecks the remaining
  compartment, and records partial inconsistency when the budget ends.
- **Commitment hypergraph.** Persistent proposition nodes plus proof,
  citation, procedure, challenge, and revision hyperedges. Nodes carry
  statement, tier, origin, validity, compartment, entrenchment, version pins,
  artifacts, dependencies, and audit refs.
- **T1 certified object.** Exact formal statement plus kernel-checkable proof
  under a named theory, checker, dependencies, and version. It does not prove
  the natural-language interpretation, premises, model-world fit, safety, or
  authorization.
- **T2a norm-anchored object.** Versioned normative span plus a FIMO. Subtiers
  distinguish anchor-only, explicitly mapped, and conflict-checked cases. The
  source's older “citation-backed compliance” name is too strong.
- **T2 procedure object.** Pinned deterministic or tightly controlled run with
  inputs, toolchain, outputs, logs, and checksum. Reproducibility is not
  correctness of the encoded standard.
- **T3 speculative object.** Labeled heuristic synthesis that cannot update the
  active commitment graph without a separate promotion route.
- **T0 metacognitive object.** Proposed monitoring commitment about the
  system—such as semantic-escape threshold breach or bridge centrality—bound
  to deterministic logs. It may trigger review; it is not epistemically
  superior to T1–T3 and should not be irretractable by default.
- **Formal Interpretation Mapping Object (FIMO).** Versioned mapping from exact
  norm spans through jurisdiction, effective time, applicability, exceptions,
  definitions, term bindings, interpretation mode, conflict policy,
  assumptions, creator/reviewer, and canonical hash to one bounded claim.
- **Intentional structure.** Pinned intended meaning and scenario suite
  (“noema-like”) plus proposal-act metadata such as prompt, sources, and
  retrieval path (“noesis-like”). These operational fields record intended
  reference and production context; they do not measure consciousness.
- **Theory compartment.** Versioned logical/normative context in which a claim
  and proof are valid. A pinned background-assumption or “lifeworld” set makes
  normally implicit defaults reviewable.
- **Bridge object.** Least-privilege cross-compartment import listing symbols,
  allowed lemma shapes, exclusions, proof/tests, budgets, compatibility with
  background assumptions, version, and authority.
- **Trusted Template Registry (TTR).** Registry for restricted formalization,
  FIMO, and procedure templates. Trust is a vector of correctness evidence,
  drift resistance, approved contexts, reviewer quality, coverage, centrality,
  and adversarial signals, not a click count.
- **Certified delusion.** A checker-valid artifact whose formal target or
  interpretation does not match the intended question.
- **Semantic escape.** A committed mapping that passes the alignment route but
  later fails a labeled positive/negative scenario or confuser case.

## Mechanisms

### Artifact-class commitment rather than one confidence ladder

The tier table is best understood as a sum type over justification artifacts,
not a total ordering of truth. A proof, norm mapping, procedure trace, and
speculative synthesis answer different questions. Each record carries its own
scope, assumptions, checker, expiry, allowed consumers, downgrade conditions,
and nonclaims. Green/yellow/red status is defined inside the tier and
compartment; it can never mean blanket “safe” or “compliant.”

This also corrects the source's T0 wording. Monitoring claims about the system
are valuable, but making them categorically non-retractable or placing them
above formal and empirical artifacts would create a self-authorization path.
They should behave as typed alerts with named metrics, thresholds, windows,
detectors, owners, expiry, and appeal.

### Round-trip alignment plus counterexamples

A candidate formal statement is rendered through a deterministic template that
preserves quantifiers, negations, scope, conditions, and exceptions. Ambiguous
queries produce several side-by-side candidates and a semantic diff. The later
CDIT addition generates positive, negative, boundary, and quantifier/exception
confuser scenarios. A mismatch rejects or quarantines the mapping rather than
letting a persuasive paraphrase proceed.

Neither route proves semantic equivalence. A renderer and scenario generator
can share the same defective schema or omit the same concept. The record must
retain the original prose, formal candidate, renderer version, scenario suite,
reviewer role, disagreement, uncovered semantic frontier, and later escapes.

### Norm anchoring without false legal authority

FIMO makes applicability and interpretation inspectable. It pins the corpus,
span, hash, jurisdiction, effective range, subject scope, exceptions,
definitions, term bindings, interpretation mode, conflict policy, assumptions,
review state, and competing norms. A disputed mapping is forked or downgraded;
the system does not resolve contestation by recency or model confidence.

The three T2a subtiers are useful because relevance, explicit mapping, and
conflict review are different achievements. Even T2a-C remains a documented
reading under a declared competing-norm set, not legal advice, legitimacy, or
unique compliance truth.

### Template automation under fatigue and grinding

The TTR exists because confirming every routine mapping creates rubber-
stamping. Promotion requires diverse parameter coverage, repeated CDIT passes,
low rollback/escape rates, correct compartment/version scope, and qualified
review. Trust decays with time, source or schema drift, conflicts, anomalies,
and centrality. Sampling favors rare buckets, boundaries, drift, and high-
impact templates. Bursts, implausibly fast approvals, and repeated slot values
are grinding signals.

The source's suggested entropy, unique-value, bucket, pairwise-coverage,
hundred-use, cold-start, and trust-pack numbers are examples only. Deployment
must calibrate them prospectively against error costs, fatigue, escapes,
coverage manipulation, reviewer dependence, and domain shift.

### Bounded revision and explicit arbitration

When a contradiction appears, the maintainer extracts an unsat core or
dependency slice, generates candidate retraction sets under a budget, applies a
declared entrenchment policy, marks retracted nodes inactive, invalidates
dependent artifacts, and rechecks locally. Budget exhaustion returns partial
inconsistency and queues bounded residual work. It does not silently restore a
consistent-looking view.

Cross-artifact conflicts use an explicit matrix. A procedure that contradicts
a proof may expose model/scope mismatch; a proof and norm mapping may require
separate contexts; two norm mappings may remain disputed; speculation never
overrules a commitment. Available outcomes include quarantine, downgrade,
fork, replay, escalation, supersession, and persistent conflict. Protected
axioms and bridges change only through impact analysis, regression, signed
approval, versioned release, migration, and rollback.

### Semantic isolation and governed bridges

Proofs do not escape their theory compartments implicitly. Each bridge grants
only named symbols and lemma shapes, forbids specific imports, binds regression
tests and a rate/centrality budget, and records the background assumptions on
both sides. This turns proof laundering and hidden normative imports into
inspectable attack surfaces. Bridge centrality and failure history can trigger
monitoring or review without granting the monitor authority to approve the
bridge.

### Operating modes and output custody

Interactive mode uses seconds-scale budgets, caches, shallow revision, and
lower-commitment routes. Analyst mode permits asynchronous proof, norm search,
conflict review, and deeper revision. The decision surface shows tier,
compartment, result semantics, assumptions, and top artifacts; the expandable
trail retains proofs, FIMOs, logs, version pins, revisions, arbitration, and
approvals. Structured summaries may be drafted only from bound fields.

## Interfaces and State Machines

Proposition nodes move through proposed, aligned, verified/bound, active,
quarantined, disputed, retracted, superseded, expired, and retired states.
Mappings move through proposed, rendered, scenario-tested, confirmed,
template-eligible, auto-confirmable, drifted, disputed, demoted, and retired.
Revision events move through detected, sliced, candidates-generated,
selected, applied, rechecked, partially-inconsistent, escalated, and closed.

Claim Ledgers own stable proposition identity and history. Evidence States own
support movement. Formal kernels and procedure runners own exact checker
results. Constitutional/governance owners control protected axioms, schemas,
bridges, keys, and releases. Context owners provide pinned dossiers. Security,
privacy, rights, and legal owners constrain source and artifact use.
Accountable humans own contested interpretation, high-impact approval, appeal,
and remedy. Spinoza may propose or block routes; it does not grant action or
publication authority.

## Evidence

The source family contains detailed architecture, equations and AGM sketches,
versioned node/edge/FIMO/template structs, alignment and revision pseudocode,
worked GDPR scenarios, threat models, role and operating-mode distinctions,
metric definitions, comparator tables, deployment plans, and extensive
self-critique. Its strongest evidence is conceptual and editorial: successive
drafts identify and correct certified-delusion, nagware, proof-laundering,
Tier-1-emptiness, schema-maintenance, latency, and false-authority failures.

The v5.0 tab describes several failure patterns and economic quantities as if
observed in deployment, but the cache provides no reports, data, code, sample
records, or independent sources for them. Its $30K–$100K setup cost, per-query
costs, 10x error-reduction example, 845% ROI, 200-confirmation coverage curve,
100-DPA pilot, law-firm labels, and target table are scenarios or targets. They
must not be presented as completed evidence.

## Evaluation and Falsifiers

A faithful evaluation compares LLM-only, RAG, citation-only, stateless
LLM+prover, human review, and Spinoza variants under matched source access,
tasks, latency, human work, and downstream consequences. It reports:

- certification and norm-mapping coverage by task and tier;
- semantic escape on independently authored intended statements, positive,
  negative, boundary, and confuser scenarios;
- contradiction persistence, belief churn, dependency invalidation, and proof
  reuse after source/schema/bridge drift;
- silence/paralysis and actionable utility, without letting T3 verbosity hide
  refusal;
- confirmation fatigue, review quality, reviewer dependence, adversarial
  grinding, template drift, and rollback incidence;
- proof-laundering attacks across compartments and bridges;
- complete compute, latency, storage, privacy, maintenance, governance,
  migration, dispute, appeal, and human-review cost; and
- delayed workflow outcomes and cost-of-error-weighted utility.

The architecture should be narrowed or rejected if deterministic rendering and
CDIT do not beat simpler semantic review; FIMOs add paperwork without better
error localization or audit outcomes; TTR automation recreates rubber-
stamping; bounded revision leaves damaging stale dependents; compartments or
bridges amplify omissions; or a simpler accountable editor/checklist achieves
equal useful and safety outcomes at lower total cost.

## Failure Modes

- **Certified delusion:** a valid proof, citation binding, or procedure checks
  the wrong target.
- **Tier collapse:** formal, normative, procedural, and speculative artifacts
  borrow one another's authority.
- **Citation-as-compliance:** relevance or a signed FIMO is narrated as unique
  legal truth or approval.
- **Renderer monoculture:** formalizer, deterministic renderer, scenario
  generator, and reviewer share the same missing concept.
- **Nagware collapse:** confirmations become fast ritual rather than review.
- **Template grinding:** repeated easy cases manufacture trust without diverse
  coverage or hard boundaries.
- **Cold-start theater:** vendor “trust packs” arrive with unverifiable scope,
  independence, or regression quality.
- **Proof laundering:** a theorem crosses a compartment through an overbroad
  bridge or hidden definition import.
- **Entrenchment capture:** protected or high-centrality nodes become
  practically unrevisable because the system itself assigned their cost.
- **Partial-consistency concealment:** revision times out while the UI shows a
  clean materialized graph.
- **Governance capture:** insiders approve unsafe templates, bridges, schemas,
  axioms, or corpus versions.
- **Supply-chain compromise:** prover libraries, solver binaries, corpora,
  logs, or governance keys are corrupted.
- **Monitoring self-authority:** T0 alerts become unretractable truths or grant
  their own governance effects.
- **Lifeworld essentialism:** provisional cultural or organizational defaults
  become frozen universal assumptions.
- **Green-badge authority:** a scoped result is mistaken for safety,
  compliance, permission, or real-world correctness.
- **Cost and privacy invisibility:** review, storage, dispute, migration,
  sensitive dossiers, and delayed decisions disappear from evaluation.

## Book Chapters Supported

- `spinoza-verification-and-proof-carrying-claims` (Proof-Carrying Claims and Adversarial Review)
- `claim-ledgers-and-belief-revision` (Claim Ledgers and Belief Revision)
- `evidence-states-and-claim-discipline` (Evidence States and Claim Discipline)
- `verification-bandwidth-and-context-adequacy` (Verification Bandwidth and Context Adequacy)
- `virtual-context-abi` (The Virtual Context ABI: Typed Pages, Cells, and Certificates)
- `failure-modes-of-ungoverned-intelligence` (Failure Modes of Ungoverned Intelligence)
- `constitutional-alignment-substrate` (Constitutional Alignment: Agency, Dignity, and Corrigibility)
- `moral-uncertainty-and-value-conflict` (Moral Uncertainty, Value Conflict, and Contestable Governance)
- `fast-generation-architectures` (Fast Generation Architectures)
- `compact-generative-systems-and-residual-honesty` (Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `artifact-steward-agents-and-living-project-governance` (Artifact Steward Agents and Living Project Governance)
- `executable-specifications-and-lean-proof-envelope` (Executable Specifications and Lean Proof Envelope)
- `integrated-reference-architecture` (Integrated Reference Architecture)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Treat proof, norm mapping, deterministic procedure, monitoring, and
  speculation as distinct justification classes rather than a total truth
  ladder.
- Preserve exact FIMO applicability, exceptions, interpretation, conflict,
  assumption, pinning, and review fields without calling a bound claim
  compliant.
- Add deterministic rendering plus independently constructed counterexample
  scenarios and confusers to the semantic-mapping gate.
- Model template trust as coverage-, drift-, centrality-, reviewer-, and
  adversary-sensitive, with decay and stratified re-audit.
- Preserve explicit cross-tier and cross-compartment arbitration outcomes:
  quarantine, downgrade, fork, replay, escalation, supersession, or persistent
  conflict.
- Treat intended meaning and proposal-act metadata as auditable fields, not
  consciousness claims.
- Keep monitoring alerts subordinate to named governance owners and make
  partial inconsistency visible after bounded revision.
- Carry the source's deployment and ROI numbers only as unvalidated targets or
  illustrative scenarios.

## Section-Family Closure Ledger

| Section family | Disposition |
|---|---|
| Problem, scope, non-goals, and when-not-to-use | Integrated into the source boundary and existing chapter scope/objection language. |
| Proposer/verifier/maintainer architecture | Already canonical in Verification and Claim Ledgers; deep note adds exact responsibilities and failure boundaries. |
| Commitment tiers and subtiers | Added to Proof-Carrying Claims as artifact classes with non-aggregation and authority boundaries. |
| Hypergraph objects and justification edges | Retained here and in Claim Ledgers; no duplicate schema chapter needed. |
| Round-trip rendering, semantic diffs, and CDIT | Added to Proof-Carrying Claims with the shared-blind-spot residual. |
| FIMO and norm conflicts | Added to Proof-Carrying Claims; constitutional/legal owners retain interpretation authority. |
| TTR, coverage, decay, re-audit, grinding, trust packs | Added to Proof-Carrying Claims; numeric thresholds retained only as research parameters. |
| Bounded AGM revision and entrenchment | Already owned by Claim Ledgers; deep note preserves partial-inconsistency and self-assigned-entrenchment risks. |
| Compartments, bridges, lifeworld anchors | Added to Proof-Carrying Claims as least-privilege semantic imports; philosophical language remains lineage only. |
| T0 monitoring and trust calibration | Retained with a corrective boundary: typed alert, not superior or irretractable truth. |
| Threat model, governance, schema/axiom evolution | Integrated into proof and claim-governance interfaces; no deployed security claim. |
| Operating modes, UX, outputs, and audit trail | Integrated into the chapter's route and interface contract. |
| Metrics, baselines, pilot, and falsifiers | Retained as concrete research obligations; no source-reported result promoted. |
| Pseudocode and worked GDPR cases | Retained in this note as implementation/test design; examples do not establish legal conclusions. |
| v5.0 economics and cold-start numbers | Explicitly preserved as hypothetical targets and rejected as evidence. |

## Open Questions

- Can independent scenario authors measure semantic escape without sharing the
  formalizer's ontology and omissions?
- Which FIMO fields can be mechanically validated, and which require named
  institutional or legal judgment?
- How should entrenchment be learned or governed without protecting early
  mistakes and incumbent norms?
- Can template automation reduce fatigue without concentrating reviewer,
  schema, and vendor dependence?
- What is the smallest bridge language that permits useful cross-domain
  reasoning while keeping imported assumptions inspectable?
- When does durable commitment maintenance outperform version control,
  structured checklists, and accountable human editorial review?

# Source Note: Aletheia / Proof-Carrying Workbench Lineage

| Field | Value |
|---|---|
| Source ID | `aletheia` |
| Source title | Aletheia, Aletheia Foundry, and Proof-Carrying Workbench (PCW) |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1H6M_IPbuu86FOQurv2rLQ97EYQVdThZ2U7njl0DBpIE |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/aletheia.txt` (1,757 lines; approximately 11,080 words). The raw text is not published. |
| Evidence role | Corben-authored architecture and correction lineage. It is design rationale, not independent corroboration or implementation evidence. |

## Thesis

The useful through-line is not the original promise of a truth-manufacturing
machine. It is a proof-carrying work architecture in which consequential AI
outputs become contracted, compiled, least-privilege artifacts with explicit
claims, evidence objects, replay information, policy decisions, and bounded
release gates. The lineage progressively corrects its own weakest assumptions:
byte hashes become semantic-scope records, vague tribunals become separated
assurance classes and adversarial batteries, free prose becomes a claim-native
release surface, ambient secrets become mediated capabilities, and long-lived
memory becomes governed commitments subject to revision and recertification.

That architecture can make omissions, scope drift, unsupported actionability,
privilege use, stale commitments, and failed verification easier to observe.
It cannot manufacture truth, make arbitrary natural-language claim extraction
deterministic, prove semantic equivalence, make cited interpretations uniquely
correct, establish reviewer independence, or turn a complete audit bundle into
a safe or useful outcome.

## Version and correction lineage

The cache contains four related papers, not four independent sources:

| Version family | Distinct contribution | Controlling correction |
|---|---|---|
| Aletheia v1.0, “Autopoietic, Thermodynamically Constrained, Federated Epistemic Engine” | Active context acquisition; layered symbols, primitives, compounds, and human views; explicit unknowns or *aporea*; hypothesis, pre-mortem, review, and bounded recursive work. | Its immutable primitive set, scalar intervention score, “live oracle,” thermodynamic laws, universal web-search rule, majority/unanimity truth logic, and numerical performance claims are proposals or overclaims, not results. |
| Aletheia Foundry v1.0 | Artifacts over answers; signed job contract; typed task graph; least-privilege slices; capability handles; claim and evidence objects; release bundles; policy and schema change control. | A contract hash protects bytes, not meaning. A verification tier must not collapse formal proof, procedural replay, and sourced interpretation into one confidence ladder. |
| Proof-Carrying Workbench v1.1, red-team hardened | Rename after the public Aletheia collision; structured Intent Manifest; structure-preserving rendering; claim-native artifacts; Interactive and Analyst modes; Constraint Capsules; response contracts; reviewer blinding; trusted templates; explicit trusted computing base; semantic-escape measurement. | “Machine-checkable claim” means schema-checkable and routed to an appropriate verifier, not automatically true. Trusted templates reduce repetitive review only inside a bounded, revocable scope. |
| Proof-Carrying Workbench v1.2, self-contained | Four-plane architecture; explicit threats and trust boundaries; phase exit artifacts; manifest-to-graph and graph-to-claim checks; dry runs; worked example; risk-to-mode policy; recertification and incident response. | This is the controlling design version. Its “deterministic claim surface,” primitive-registry compile errors, source allowlists, risk table, and assurance policy are illustrative architecture choices rather than universally valid rules or validated thresholds. |

The later PCW versions supersede the earlier promotional language wherever the
two conflict. Repetition across versions supplies revision history, not extra
evidence.

## Mechanisms

### Contract and semantic custody

- Represent the requested job with a signed contract and a separate Intent
  Manifest containing definitions, scope, systems in and out, jurisdiction,
  time window, assumptions, exclusions, acceptance criteria, output classes,
  risk, data clearance, tools, budgets, evidence requirements, and publication
  policy.
- Treat the contract hash as byte integrity only. Validate semantic continuity
  across Manifest, execution graph, context slices, claims, verification, and
  release. Preserve ambiguous or unmapped requirements as residuals.
- Carry non-summarizable constraints as typed Constraint Capsules into every
  affected slice and claim dependency. A capsule is still a fallible authored
  policy object; presence does not establish correctness or compliance.

### Compiled, least-privilege work

- Compile a proposal into a typed dependency graph whose nodes declare inputs,
  outputs, context, capabilities, isolation, route, verifier, and exit
  artifact. Perform dry-run resolution of tools, versions, permissions,
  quotas, network policy, and environmental constraints before effects.
- Keep probabilistic proposal separate from deterministic schema, policy,
  capability, and artifact checks. An unresolved primitive may be rejected,
  decomposed, clarified, or retained as an unsupported open-world task; it is
  not evidence that every useful job belongs to a closed primitive registry.
- Give workers scoped context slices and opaque capability handles. The
  capability proxy holds secrets, validates parameters, enforces caller-bound
  policy, logs the invocation, normalizes errors, and returns sanitized data or
  a protected reference. “Secretless” depends on the entire response and log
  path, not merely withholding a token from the prompt.

### Claim-native artifacts and evidence classes

- Make structured claims first-class release objects with stable identity,
  type, predicate or proposition, parameters, qualifiers, dependencies,
  evidence references, justification class, actionability, and policy state.
- Bind narrative assertions to claim IDs and claims back to exact narrative or
  artifact spans. Measure both directions. Material prose that is not bound is
  an `unregistered_assertion` residual; a structured claim with no rendered
  surface is a hidden-claim residual. Neither is silently accepted.
- Do not call open-ended claim extraction deterministic. Schemas can make the
  declared claim surface deterministic to enumerate, but whether natural
  language contains another material assertion remains a semantic judgment.
  Use required claim categories, perturbation tests, independent sampling,
  omission search, and a complete residual denominator.
- Preserve formal, procedural, source-bound, and heuristic justification as
  different classes rather than a single scalar. Formal checking is bounded by
  the modeled property; procedure replay reproduces a process; source binding
  preserves a documented interpretation; heuristic synthesis remains labeled
  and non-authoritative.

### Bounded verification and governed commitments

- Match verification method to the claim and risk. Keep verifiers blind to
  generation traces where practical, expose the contract, claims, and evidence
  needed for review, and run explicit negation, scope, time, jurisdiction,
  exception, omission, actionability, and privilege-escalation attacks.
- Bound review rounds and compilation attempts. Failure to converge produces a
  typed “cannot satisfy” artifact naming missing information and residuals,
  not a silent downgrade or confident answer.
- Separate volatile working memory, durable epistemic commitments, policy
  anchors, and ordinary artifact retention. Contradiction triggers a proposed
  minimal-conflict analysis, dependency invalidation, quarantine, new-evidence
  request, and human escalation; it does not make entrenchment scores or a
  model-generated minimal set infallible.
- Use pre-reviewed template packs for common work only with parameter and
  boundary coverage, allowed scopes, required capsules and claim categories,
  adversarial-test selection, audit sampling, expiry, trust decay, revocation,
  and recertification. A template reduces repeated process; it does not grant
  new authority or inherit truth.
- Re-evaluate affected releases when a material source, policy, schema,
  template, tool, checker, capability, or threat model changes. Preserve the
  old bounded result and mark current applicability separately.

### Release, observability, and incident response

- A release bundle joins the output artifact, structured claim set, evidence
  objects, provenance, policy decisions, tool events, replay manifest,
  limitations, unresolved residuals, and exact version identities.
- Interactive work may be fast and restricted, but it cannot create durable
  commitments or high-consequence effects merely because the interface is
  conversational. Analyst mode adds stronger evidence and review duties; mode
  is not itself assurance.
- Record policy decisions, capability calls, graph events, verification
  outcomes, rollbacks, and release state in privacy-aware append-only logs.
  Incident handling can invalidate handles, rotate secrets, freeze template
  promotion, flag releases, recertify, or revoke trust.

## Interfaces and invariants

The source spans many layers, so the book should preserve interfaces rather
than create one monolithic Aletheia chapter:

1. Human Intent owns the semantic contract and ambiguity boundary.
2. Cognitive Compilation and planning own the typed graph proposal and dry
   run, not effect authority.
3. Virtual Context and runtime security own slices, capsules, capability
   handles, response contracts, isolation, and secret custody.
4. Claim Ledgers own durable claim identity, narrative/claim surface coverage,
   commitments, contradiction, revision, and recertification state.
5. Spinoza and Verification Bandwidth own method-relative adequacy,
   interpretation custody, bounded adversarial review, and unresolved proof
   obligations.
6. Human Factors owns whether review capacity and approval are meaningful;
   trusted templates do not erase this duty.
7. Artifact Graphs, reproducibility, and publication own release-bundle
   lineage and surface synchronization.
8. Scientific Discovery applies the dossier, unknown-preservation, and
   correction-history pattern without treating it as a discovery result.

Cross-cutting invariants are: structure never expands authority; provenance is
not evidence validity; a hash is not semantic identity; a citation is not
truth; a verifier cannot authorize its own consequence; omitted claims remain
visible; failed convergence remains an artifact; changed dependencies can
stale a release; and no assurance class imports the certainty of another.

## Evidence

The source supplies detailed architecture, schemas, threats, workflows,
illustrative JSON, and one narrative OAuth example. It contains no local PCW
implementation, corpus, model run, live capability proxy, independent
reviewer, human study, adversarial-battery result, semantic-escape estimate,
replay-rate estimate, claim-coverage estimate, leak result, useful-throughput
comparison, deployment, or independent replication in this repository.

The book may cite this source as Corben-authored design lineage. It may not use
it to promote a chapter to source-derived, prototype-backed, test-backed,
externally corroborated, safe, general, or production-ready status.

## Failure Modes

- **Contract-hash theater:** identical bytes conceal changed interpretation,
  defaults, environment, or downstream rendering.
- **Verification by omission:** easy claims are registered while dangerous,
  normative, negative, or actionable assertions remain only in prose.
- **Claim granularity gaming:** one mega-claim hides unsupported subclaims, or
  excessive fragmentation inflates apparent assurance coverage.
- **Assurance laundering:** a proof, successful replay, citation, reviewer
  agreement, or policy pass is presented as more than its own scope warrants.
- **Closed-world compiler theater:** unfamiliar but valid work is rejected or
  silently forced into the wrong primitive because the registry is treated as
  complete.
- **Verifier dependence:** reviewers share prompts, models, data, tools,
  assumptions, or incentives and create false independence.
- **Template nagware or template capture:** repetitive prompts induce rubber
  stamping, while trusted packs drift, broaden scope, or become authority
  shortcuts.
- **Capability side channels:** secrets leak through outputs, errors, logs,
  timing, handles, caches, or downstream artifacts despite opaque credentials.
- **Memory-to-belief laundering:** repeated or persistent text becomes a
  durable commitment without allowed evidence and explicit promotion.
- **Silent non-convergence:** budgets expire and the system emits a plausible
  answer rather than a typed unknown or incomplete release.
- **Recertification gaps:** changed tools, sources, policies, templates, or
  checkers leave earlier releases looking current.
- **Audit completeness theater:** a signed release bundle is internally
  consistent yet semantically wrong, unsafe, useless, or unauthorized.

## Explicitly rejected or bounded claims

- No fixed set of roughly 300 semantic primitives is shown to be immutable,
  universal, sufficient, or optimal.
- No scalar intervention score is a truth, safety, or resource optimum.
- Shannon coding, free-energy language, entropy, or thermodynamic metaphors do
  not prove the paper's cognitive laws or decay schedule.
- Mandatory online retrieval is not a universal route and can increase
  poisoning, privacy, latency, rights, and availability risk.
- A “live oracle,” model tribunal, majority, or unanimity does not establish
  truth or reviewer independence.
- A cryptographic digest establishes integrity under its key and algorithm,
  not semantic equivalence, evidence validity, authorization, or safety.
- Claim extraction from arbitrary prose cannot be assumed deterministic or
  complete; only an authored structured claim array is deterministically
  enumerable.
- Source allowlists do not establish source truth, completeness, currency, or
  interpretation correctness.
- Risk classes and allowed assurance mappings are policy examples, not
  validated universal thresholds.
- The paper's early five-percent simulation-failure target and other numerical
  goals are unvalidated targets, not measurements.
- The architecture does not establish safe general intelligence, autonomous
  scientific truth discovery, omniscience, AGI, or ASI.

## Section-family closure

| Section family | Disposition |
|---|---|
| Original Aletheia thesis, active context, semantic layers, intervention routing, recursive clarification | Retained as historical design lineage; useful uncertainty, context, and bounded-work ideas are already owned by stack, routing, context, and intent chapters. Fixed primitives, scores, web-search mandates, and thermodynamic laws are rejected. |
| Hypothesis generation, pre-mortem, Bubble-Up, aporea, federated failure taxonomy | The book already owns explicit alternatives, attacks, escalation, typed unknowns, and durable residuals. Source note retains the names; no duplicate prose is warranted. |
| Tribunal, double-blind review, evidence links, live oracles | Mapped to Spinoza and scalable oversight with dependence, competence, scope, and authority corrections. Consensus and oracle language is bounded. |
| SparkStream consolidation, pruning, dreaming, harvesting | Mapped to governed memory, consolidation, maintenance-learning windows, retention, and provenance. Sleep/idle time and internal simulation confer no learning or mutation authority. |
| Foundry contract, graph, context, capabilities, verification, release bundle | Existing intent, compilation, context, runtime, verification, artifact, and publication chapters already own these mechanisms. |
| Semantic Scope Lock, Intent Manifest, Constraint Capsules, perturbation checks | Existing Intent-to-Execution, VCM, Kernel English, and Spinoza prose already contains the stronger contract and semantic-escape model. Retained with exact source lineage. |
| Claim-native artifacts and deterministic claim surface | Added explicitly to Claim Ledgers as a bidirectional release-surface contract, while rejecting deterministic open-domain extraction and preserving unregistered assertions as residuals. |
| Assurance levels and risk policy | Existing Spinoza commitment classes are more precise. PCW supplies lineage only; its example risk table remains non-normative. |
| Trusted Template Packs and nagware collapse | Existing Spinoza template registry and Human Factors approval-fatigue treatment already own the useful mechanism and limitations. No duplicate section added. |
| Commitment promotion, belief revision, recertification | Existing Claim Ledgers and Evidence States own transitions and dependency repair. Added source refs and limits; no automatic promotion rule is imported. |
| Operating modes, telemetry, incident response, metrics, worked example, JSON appendices | Retained as implementation and evaluation obligations. The examples are illustrative and supply no result. |

## Book Chapters Supported

- `asi-is-a-stack-not-a-model`: four-plane, artifact-over-answer stack framing.
- `the-efficient-asi-hypothesis`: risk-, uncertainty-, and cost-sensitive
  routing as a hypothesis requiring comparison.
- `claim-ledgers-and-belief-revision`: claim-native release surfaces,
  commitments, contradictions, revision, staleness, and recertification.
- `spinoza-verification-and-proof-carrying-claims`: assurance-class separation,
  interpretation custody, adversarial review, semantic escape, and trusted
  templates.
- `intent-to-execution-contracts`: semantic scope, exclusions, acceptance
  criteria, dry runs, and no authority expansion.
- `virtual-context-abi-and-context-transactions`: least-privilege slices and
  always-propagated constraint objects.
- `runtime-adapters-tool-permissions-and-human-approval`: mediated
  capabilities, response contracts, and incident revocation.
- `human-factors-and-meaningful-control-in-oversight`: review capacity,
  approval fatigue, and the limits of templates.
- `scientific-discovery-and-experimental-governance`: claim dossiers,
  explicit unknowns, correction history, and bounded evidence authority.

The source is not added to every receiving chapter's primary-source list when
the idea is already fully sourced by a more direct paper. This avoids turning
repeated author-side convergence into apparent independent corroboration.

## Claims To Add Or Update

- Add the bidirectional claim-native release rule to Claim Ledgers: structured
  claims point to rendered spans, material narrative assertions point to claim
  IDs, and unmatched material in either direction remains a typed residual.
- State explicitly that a deterministic structured claim surface is not
  deterministic or complete extraction from arbitrary natural language.
- Preserve semantic-scope, assurance-class, template-trust, capability, and
  recertification ideas in their current canonical chapters rather than
  duplicating them in an Aletheia chapter.
- Keep all Aletheia/PCW-derived statements at design-rationale support until a
  real implementation and independently evaluated natural workload exist.

## Research obligations and falsifiers

1. Build natural, adversarial release artifacts containing negation, nested
   qualification, exception, implicit actionability, normative statements,
   tables, code comments, captions, and cross-section dependencies.
2. Compare free prose, one-way extracted claims, authored claim-native output,
   and bidirectional claim-surface gating on omission, false registration,
   semantic drift, usefulness, latency, reviewer burden, and unsafe release.
3. Keep the full assertion denominator, disagreements, adjudication protocol,
   model and prompt lineage, and residuals. Do not score only extracted claims.
4. Perturb scope, definitions, time, jurisdiction, exceptions, claim
   granularity, actionability, capabilities, sources, policies, templates, and
   checker versions; measure whether affected releases are found and correctly
   narrowed, blocked, or recertified.
5. Test template packs under distribution shift and adversarial slot values;
   measure both approval-fatigue reduction and escape rate against strong
   human-authored and static policy baselines.
6. Test capability response and logging paths for explicit, indirect, error,
   timing, cache, and artifact leakage rather than checking only prompts.
7. Falsify the design if the governed route cannot materially reduce harmful
   omission or scope drift at acceptable useful throughput and total cost, or
   if simpler editorial and CI controls perform as well.

## Open Questions

- Which assertions are material enough to require registration, and who owns
  that taxonomy for each release class?
- Can a claim-native authoring interface reduce the open-ended extraction
  problem without making prose unusably rigid or encouraging mega-claims?
- How should bidirectional coverage be sampled when exhaustive semantic review
  is impossible?
- When does a changed dependency require full recertification rather than a
  narrower affected-closure review?
- Which template-trust signals resist gaming while avoiding permanent human
  review of routine work?
- How can reviewer and tool dependence be measured when different providers
  share training data, model families, retrieval corpora, or evaluators?

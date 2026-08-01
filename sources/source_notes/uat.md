# Source Note: Unified Adaptive Tribunal

| Field | Value |
|---|---|
| Source ID | `uat` |
| Source title | Unified Adaptive Tribunal (UAT) |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1R7wKo2qg5waosEa-SwC-JKF77qoDiiEp1Df4Gbap0VE |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/uat.txt` (481 lines; approximately 4,932 words). Raw text is not published. |
| Evidence role | Corben-authored multi-model review correction lineage; no implemented tribunal or empirical result. |

## Thesis

The final useful thesis is deliberately weaker than the original paper's
promotional framing. A multi-model review workflow can help a qualified human
inspect a source-bounded artifact when it separates structural coverage,
retrieval, counterargument, claim decomposition, support review, omission
search, revision, compression, and adjudication into visible stages. Its
dossier is a declared evidence boundary rather than ground truth; its models
are potentially dependent reviewers; its stability metrics are stopping
signals rather than correctness; and its output remains a review candidate,
not “pre-verified” truth.

## Version and correction lineage

The cache contains three related tabs:

1. The original expansive UAT paper proposes multi-flagship competition,
   synthesis, hierarchy, relays, adaptive classification, rating-based
   consensus, and mandated verbosity. It also contains numerous unsupported
   percentage, cost, interaction-count, superiority, and “preeminent” claims.
2. UAT v3.1 reframes the system as a human-in-the-loop reference architecture
   for assisted knowledge engineering. It introduces structural, retrieval,
   and dialectical priors; a bounded dossier; probabilistic proposition
   extraction; explicit support labels; logic/citation/omission attacks; a
   three-cycle cap; and SME handoffs.
3. The public v1.0 release restates v3.1 with operational guidance, cost and
   latency estimates, deployment checklist, and the important limitations of
   correlated hallucination, decomposition loss, plateau trapping, and
   consensus bias.

The public architecture controls conflicts with the original. Repeated text
across v3.1 and public v1.0 is one lineage, not corroboration.

## Mechanisms

- Freeze the target, intended use, source universe, dossier construction
  method, omissions, time boundary, rights, risk, reviewer roles, budgets, and
  human authority before review outcomes.
- Generate separable candidate views: a dependency or structure map, a source
  dossier, and an anti-premise or counterargument set. Role prompts do not
  prove cognitive diversity; record actual model, data, prompt, tool,
  infrastructure, and organization dependence.
- Treat the dossier as the automated review's bounded evidence world. Expose
  its search queries, retrieval system, source versions, ranking, exclusions,
  transformations, conflicts, quality review, and omitted frontier. Permit a
  governed dossier-expansion request rather than equating absence with false.
- Extract candidate material claims with exact prose spans and uncertainty.
  Subject–verb–object triplets are a weak representation for qualified,
  conditional, causal, comparative, normative, negative, modal, tabular, and
  cross-sentence claims.
- Keep direct source support, inference, unsupported-within-dossier,
  contradicted, disputed, ambiguous, and not-assessed distinct. Semantic
  similarity to an excerpt cannot by itself establish entailment or source
  validity.
- Run bounded logic, citation, source-quality, scope, exception,
  counterexample, omission, actionability, and persuasion attacks. Reviewers
  see enough original intent to test scope, while hidden generation details may
  reduce anchoring where that tradeoff is deliberate.
- Use edit distance, representation similarity, claim-graph change, and cycle
  budgets only to route continuation, escalation, abstention, or residuals.
  Stable prose can be wrong; unstable prose can be improving.
- Compress only under bidirectional claim/surface coverage and source,
  qualifier, contradiction, dissent, limitation, and residual preservation.
  Constant proposition count is neither necessary nor sufficient for fidelity.
- Present the accountable human with dossier boundaries, unresolved claims,
  disagreements, attacks, omissions, costs, and decision options. An approval
  receipt does not establish reviewer competence, attention, independence, or
  sufficient time.

## Interfaces and invariants

`spinoza-verification-and-proof-carrying-claims` owns the complete tribunal and
verification-event contract. Claim Ledgers owns proposition identity and
revision; Evidence States owns support movement; Verification Bandwidth owns
adequacy; Human Factors owns meaningful review capacity; Scientific Discovery
owns hypothesis generation and novel-evidence routes; Benchmark Ratchets owns
comparative evaluation and anti-Goodhart pressure.

Invariants are: dossier presence is not truth; omission remains visible;
reviewer count is not independence; consensus is not evidence; stability is
not correctness; cycle termination is not convergence to truth; absence from a
dossier is not refutation; compression cannot erase scope or dissent; the
tribunal cannot promote its own output; and human adjudication cannot repair an
uninspectable or overload-inducing process by name alone.

## Evidence

The source supplies architecture prose, prompts, pseudocode, example
hyperparameters, operational guidance, and self-identified failure modes. It
does not provide a codebase, task corpus, frozen dossiers, model outputs,
source-quality labels, proposition annotations, reviewer-dependence audit,
human study, cost records, attack results, benchmark, or independent
replication. The original claims of 15–20% role deviation, 25–35% error
correlation, 30–50% flaw amplification, 30–40% innovation, 40–50% error
abatement, 50% resilience, 28% depth gain, 37% bias mitigation, 25% coherence,
35% efficiency, $5–15 cost, or 20–50 interactions have no reproducible support
here. The later 3–5x token and 2–4-minute estimates are also unverified.

## Failure Modes

- Retrieval or source capture turns widely repeated errors, SEO spam,
  selection bias, stale evidence, or majority narratives into “verified” text.
- Model dependence is hidden behind provider names or role prompts.
- Claim extraction misses nuance, implicit assumptions, tables, negatives,
  exceptions, minority evidence, or dangerous actionable claims.
- Unsupported-within-dossier claims are deleted even when true, novel,
  important, or evidence-seeking rather than preserved for expansion or study.
- Withholding the original request from reviewers prevents detection of scope,
  purpose, acceptance, authority, or affected-party mismatch.
- Rating, verbosity, confidence, familiarity, and polished synthesis dominate
  evidence and minority dissent.
- Edit and embedding stability trap a wrong plateau or reward paraphrase;
  fixed thresholds and three cycles are not calibrated across domains.
- Atomic Proposition Density is gamed through claim splitting, merging,
  deletion, or loss of relationships and uncertainty.
- The process overloads the SME, who rubber-stamps a longer and more persuasive
  artifact under the false label “pre-audited.”
- High cost and latency produce selective bypass, hidden route shopping, or
  silent downgrade to a weaker process.
- Indexed-source bias excludes emerging research, oral knowledge, affected
  communities, local evidence, negative results, and lawful private sources.

## Explicitly rejected or bounded claims

- UAT is not demonstrated as preeminent, Pareto-superior, inherently scalable,
  production-standard, industrial, resilient, or superior to single-model,
  human-editorial, or simpler verification workflows.
- Ensemble-learning, game-theory, adaptive-control, GAN, and Nash-equilibrium
  analogies do not provide a theorem or empirical result for LLM reviewers.
- Different model brands, role names, or rotations do not establish reviewer
  diversity, competence, independence, or unbiased judgment.
- A dossier excerpt plus semantic match does not make a proposition verified;
  the source, interpretation, entailment, scope, and claim can all be wrong.
- `unsupported` means unsupported within the declared dossier and method, not
  hallucinated, false, worthless, or safe to delete.
- UAT is not structurally incapable of proposing novel hypotheses; rather, a
  dossier-bounded review cannot verify new empirical knowledge without a new
  evidence route.
- Levenshtein below 5%, embedding cosine above 0.98, three cycles, confidence
  0.8/0.9/0.7, stable proposition count, 100% citation coverage, and named
  tooling are illustrative, unvalidated parameters.
- A guard model “safe” result does not establish instructional fidelity,
  security, harmlessness, policy compliance, or release authority.
- Human final sign-off does not turn a flawed dossier, extraction, or review
  process into truth.

## Section-family closure

| Section family | Disposition |
|---|---|
| Original red-team assumptions and hazards | Preserved as dependence, prompt injection, bloat, human fallibility, cost, domain mismatch, and correlated-error failure classes; all quantitative proxies rejected. |
| Original five-phase competition/synthesis/hierarchy/relay flow | Superseded by the narrower public architecture; retained only as candidate review baselines, not the canonical mechanism. |
| Rating, consensus, verbosity, and theoretical-superiority sections | Explicitly rejected as evidence or termination authority. |
| Structural, retrieval, and dialectical priors | Integrated in Spinoza as dossier construction, competing interpretations, attack sets, and role/dependence records. |
| Atomic proposition extraction and three support tiers | Integrated in Claim Ledgers and Evidence States with richer states, exact spans, uncertainty, and no delete-by-absence rule. |
| Bounded adversarial siege and double lock | Integrated in Spinoza; stability and cycle cap are termination signals only. |
| Atomic compression | Integrated in claim-native surface and residual-honesty contracts; proposition count alone is rejected. |
| SME adjudication and final sign-off | Integrated in Human Factors with competence, capacity, information, deadline, authority, and intervention conditions. |
| Known limitations, cost, deployment checklist | Retained as research obligations; figures and product maturity labels remain unsupported. |

## Book Chapters Supported

- `spinoza-verification-and-proof-carrying-claims`
- `claim-ledgers-and-belief-revision`
- `evidence-states-and-claim-discipline`
- `verification-bandwidth-and-coherency-horizons`
- `human-factors-and-meaningful-control-in-oversight`
- `scientific-discovery-and-experimental-governance`
- `benchmark-ratchets-and-anti-goodhart-evidence`
- `moral-uncertainty-and-value-conflict`: bounded review, omitted-frontier, disagreement, and SME-handoff structure only; model consensus does not settle moral uncertainty.

No new UAT chapter or prose section is warranted. The current Spinoza chapter
already contains the corrected dossier, dependence, adversarial, termination,
dissent, consequence, cost, and evaluation contracts, including the specific
warning that edit stability and claim density are not truth.

## Claims To Add Or Update

- Retain UAT as the author-side lineage for a dossier-bounded, human-adjudicated
  review protocol and for its unusually candid failure list.
- Keep the public architecture's correction above the original promotional
  tribunal and avoid double counting repeated versions.
- Preserve `unsupported-within-dossier`, omitted frontier, reviewer dependence,
  and non-convergence as explicit states rather than deletion or consensus.
- Do not promote any claimed improvement, cost, threshold, production, or
  auditability result.

## Research obligations and falsifiers

1. Freeze natural high-stakes and ordinary editing tasks, source universes,
   dossier builders, claim annotations, model/prompts, reviewer roles, budgets,
   human qualifications, and downstream decisions.
2. Compare direct model, self-critique, citation-only, single strong reviewer,
   independent human editor, original tribunal variants, public UAT, and the
   book's governed verification route at matched information and cost.
3. Inject source poisoning, correlated myths, minority evidence, emerging
   results, implicit and nested claims, omitted negatives, prompt attacks,
   wrong scope, stable wrong drafts, persuasive unsupported prose, reviewer
   dependence, and human overload.
4. Measure claim recall and precision, entailment, source validity, omission,
   disagreement, false deletion, false acceptance, useful quality, downstream
   error, unsafe release, latency, money, energy, privacy, and human burden.
5. Ablate each prior, dossier review, extraction, attack class, independence
   control, stopping signal, compression check, and human handoff.
6. Falsify the mechanism if a single strong or human editorial baseline
   matches it, if dependence removes the benefit, or if review cost and false
   deletion outweigh improvements.

## Open Questions

- How should the dossier frontier expand without allowing route shopping after
  an unfavorable verdict?
- What claim representation captures relationships and qualifications without
  making review economically impossible?
- Which reviewer-dependence dimensions predict correlated error in practice?
- How can emerging, minority, local, or non-indexed evidence receive fair
  treatment without weakening source and provenance discipline?
- What interface lets an SME see the decisive uncertainty and omitted frontier
  instead of only a polished draft and a queue of tags?

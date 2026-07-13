# ASI Stack Post-v2.3 Quality Floor and Reader Completion Roadmap

Roadmap ID: `asi-stack-post-v2-3-quality-floor-reader-completion-2026-07-13`

Authority: Corben Sorenson

Status: completed 2026-07-13; canonical execution history; successor activated
2026-07-13 at
`docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md`

Predecessor: `docs/post_v2_2_implementation_completion_roadmap.md`, completed
for immutable `v2.3.0` and retained as execution history

Machine status:
`roadmap_records/post_v2_3_quality_floor_and_reader_completion_status.json`

## Goal to point at

> Restore one finished quality floor across all 54 chapters before adding more
> architectural breadth. Deepen the ten post-v1-spine chapters until each has
> a defensible idea delta, substantive architecture and objection treatment,
> owned formal coverage, executable or exactly blocked evidence work, and
> reader-grade prose. Preserve the frozen 44-chapter v1.0 curated manuscript;
> create and reconcile a new 54-chapter curated-reader successor instead of
> rewriting history. Remove source-tree drift, adjudicate completed empirical
> results through the existing evidence-transition machinery, then run only
> the next preregistered campaigns and release transaction that the resulting
> evidence warrants. Do not manufacture depth with prose volume, theorem
> counts, citation counts, version numbers, or unsupported promotion.

This was the sole active roadmap after v2.3.0 and is now completed execution
history. Its clean-handoff, reader-format, external-grounding, and
evidence-renewal successor is
`docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md`, with
machine state in
`roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json`.
The v2, v2.1, post-v2.1, post-v2.2, and post-v2.3 programs remain completed
history and are not reopened by that successor.

## Why this roadmap exists

The external review identified four findings with operational force:

1. the ten post-v1-spine chapters are materially shorter than the other 44 and
   have narrower registered proof coverage;
2. two of the ten borrow another chapter's Lean module as their only formal
   owner;
3. there is no current-spine, 54-chapter curated-reader successor.

It also raised two useful governance concerns: evidence-transition review must
keep pace with completed campaigns, and minor-version cadence must not become a
substitute for coherent product completion.

Several raw claims in the review require calibration. At activation, the book's
own tokenization gives a 2,713-word median for the ten chapters and a 4,943.5-word
median for the other 44; different tokenizers produce slightly different
counts. The ten have between three and eleven assigned source records, not a
uniform absence of literature. The proof audit exposes one registered proof
artifact for each of the ten; declaration counts are not a semantic-adequacy
measure. Most importantly, `editions/reader_manuscript/v1_0` is deliberately a
frozen 44-chapter historical snapshot. Its policy explicitly requires a later
edition directory when the active spine changes. The deficiency is therefore
the absence of that later 54-chapter edition, not corruption of the v1.0
snapshot. The alleged orphan HTML is also not an orphan: it is a declared
historical redirect in `_quarto.yml`, `docs/chapter_history_ledger.md`, and
`docs/chapter_consolidation_url_history_policy.md`, alongside nine other
consolidation redirects. Removing it would break the project's explicit URL
preservation contract.

The roadmap accepts the substantive depth, ownership, reader-parity, and cadence
findings while refusing the bad incentives their proxies could create. It
converts the false orphan finding into a stronger general hygiene control.

## Completion contract

The roadmap is complete only when all of the following are true:

- every one of the ten named chapters passes the semantic depth packet and the
  cohort floor without padding;
- every one owns a chapter-specific Lean module with useful derived coverage,
  negative cases, explicit limitations, and an executable fixture or an exact
  blocker;
- a new curated-reader successor maps and reconciles all 54 active chapter IDs,
  while the v1.0 historical snapshot remains unchanged;
- the selected reader text artifact passes its declared application,
  accessibility, reconciliation, and release-record gates, or an exact blocked
  terminal record explains why it cannot ship;
- every tracked chapter HTML file is either a manifest source or an explicitly
  declared, validated historical redirect, and the hygiene gate rejects any
  undeclared rendered artifact;
- every completed empirical result with plausible transition relevance has an
  explicit `promote`, `narrow`, `no_change`, or `refute` adjudication under the
  existing evidence schema;
- any new governance-tax or residual-honesty campaign is preregistered before
  outcomes are opened and preserves costs, failures, residuals, and non-claims;
- public truth, version semantics, validation, render, deployment, and release
  records agree; and
- all 54 chapter-core support states remain at their evidence-earned level.

Completion may honestly end with no new content release, a blocked reader
artifact, negative experiments, or no support-state transitions. It may not end
with incomplete dispositions, denominator laundering, or silent scope changes.

## Authority and history boundaries

1. Exact tags, archives, release records, and rights snapshots govern immutable
   historical releases.
2. `book_structure.json` governs the active chapter spine.
3. Claim/evidence ledgers and accepted evidence transitions govern support.
4. This roadmap and its machine record govern work order and completion.
5. Reader manuscripts are parallel derivative prose sources; the live book
   remains canonical for claim meaning, evidence, formal/test status, and
   release truth.
6. Generated reader files, dashboard summaries, and public prose must reproduce
   those authorities without upgrading them.

The v1.0 curated-reader directory, v2.3.0 tag, source archive, and release record
are immutable history. This cycle creates successors; it does not rewrite them.

## Activation baseline

### Book and evidence

- Latest immutable release: `v2.3.0` at
  `e27661166e9105f37cb36d63b15795f80715ca24`.
- Active spine: 54 chapters and 280 public-safe source records.
- Core evidence: all 54 chapter-core claims remain at `argument`.
- Current generated Human projection: 54 chapters.
- Curated v1.0 historical manuscript: 44 reconciled chapter records, status
  `drafting`, intentionally frozen to its historical spine.
- Current 54-chapter curated-reader successor: absent.

### Depth cohort

The ten chapters in this cycle are:

1. `scalable-oversight-and-adversarial-ai-control`;
2. `model-weight-custody-and-hardware-roots-of-trust`;
3. `ai-supply-chain-integrity-and-lifecycle-provenance`;
4. `open-ended-improvement-engines`;
5. `inter-stack-protocols-identity-and-economic-exchange`;
6. `governed-deliberation-and-test-time-scaling`;
7. `capability-thresholds-and-deployment-commitments`;
8. `adversarial-evaluation-sandbagging-and-training-time-deception`;
9. `safety-cases-and-structured-assurance`; and
10. `data-engines-continual-learning-and-unlearning`.

Using the activation validator's stable prose-token method:

- ten-chapter range: 2,333–3,890 words;
- ten-chapter median: 2,713 words;
- comparison-cohort lower quartile: 4,486.75 words;
- comparison-cohort median: 4,943.5 words.

These are diagnostic baselines, not quality claims. They become valid
completion gates only in combination with the semantic packet below.

### Formal ownership

Eight chapters point to chapter-specific modules. Two do not:

- `open-ended-improvement-engines` borrows `AsiStackProofs.SelfImprovement`;
- `adversarial-evaluation-sandbagging-and-training-time-deception` borrows
  `AsiStackProofs.PolicyOptimization`.

The canonical proof-artifact audit records one proof artifact per chapter for
all ten. This proves traceability, not adequate chapter coverage.

### Hygiene

Ten tracked `.html` files under `chapters/` are deliberate historical redirect
stubs. `chapters/unified-adaptive-tribunal-and-adversarial-review.html` is one of
them. It has an explicit Quarto resource entry, canonical destination, history
ledger row, and consolidation policy. The confirmed orphan count is zero. The
missing control is a general validator that rejects a tracked chapter HTML file
unless all of those declarations agree.

## Operating principles

1. **Depth before breadth.** No new chapter is added while any of the ten
   quality packets is incomplete. A documented merge, deletion, or scope
   correction is allowed if it reduces incoherence.
2. **Semantic adequacy before proxy counts.** Word, source, and theorem floors
   are necessary anti-regression signals, never sufficient completion evidence.
3. **Primary comparators before citation volume.** Each claimed novelty delta
   must be passage-reviewed against its strongest relevant neighbors.
4. **Owned formal boundaries before borrowed labels.** A chapter may cite a
   neighbor's theorem, but its completion gate requires an owned module and an
   explicit cross-module relation.
5. **Executable bridge or exact blocker.** Every formal or architectural claim
   names the fixture, harness, experiment, or missing dependency that would
   test it.
6. **Historical reader editions do not mutate.** The current-spine edition is a
   new versioned directory with its own reconciliation and release record.
7. **Generated and curated counts remain separate.** Public surfaces may say
   “54 generated Human chapters” and “44 historical curated records,” but may
   not combine them into a single completion percentage.
8. **Evidence transitions are adjudicated, never inferred.** Positive deltas,
   recommendation flags, and chapter prose do not move support by themselves.
9. **Version numbers describe coherent deltas.** They do not reward activity
   volume or conceal unfinished product surfaces.
10. **No external-human prepublication gate.** Internal semantic review,
    automated checks, application-level artifact inspection, and exact
    residuals are required; outside readers are not a prerequisite.

## Execution board

| Priority | Activation state | Purpose | Terminal authority |
|---|---|---|---|
| P0 — Authority, baseline, freeze, and hygiene | completed | Install the successor, preserve history, measure the real gap, and reject source-tree drift. | Machine status, public pointers, hygiene validator. |
| P1 — Ten-chapter semantic depth | completed | Bring the ten new-surface chapters to the established conceptual and editorial floor. | Ten signed-off quality packets and cohort audit. |
| P2 — Owned formal and executable depth | completed | Replace narrow or borrowed formal coverage with chapter-owned, semantically reviewed boundaries. | Ten owned modules, proof review, Lean build, fixtures/blockers. |
| P3 — Current-spine curated reader | completed | Create, reconcile, inspect, and release or honestly block a 54-chapter reader successor. | Versioned reader manifest and exact edition release/block record. |
| P4 — Evidence adjudication and next campaigns | completed | Reviewed all completed candidates, then executed the two prospectively frozen evidence campaigns. Both campaign comparisons ended in preserved protocol-failure `no_change` dispositions. | Transition ledger plus frozen/result campaign packets. |
| P5 — Coherent release and closure | completed | Reconciled the whole project and recorded an honest no-public-living-book-release decision; the separately governed exact local reader release remains intact. | No-release record, completion declaration, and validation receipts. |

## P0 — Authority, baseline, freeze, and hygiene

### Required work

- install this roadmap, schema-bound status record, registered validator, and
  rejecting mutations;
- add a dated successor pointer to the v2.3 completion declaration while
  preserving its release facts;
- update README, landing page, publication readiness, and public status
  contract to distinguish completed v2.3.0 from this active cycle;
- record the exact ten-chapter cohort, depth baseline, formal ownership,
  44-record historical reader snapshot, and absent 54-record successor;
- preserve all ten intentional historical redirect stubs;
- add a general validator that rejects tracked `.html` files under `chapters/`
  unless each is a valid redirect with a declared Quarto resource, canonical
  destination, and chapter-history entry;
- freeze chapter growth until P1–P3 pass; and
- preserve all support states, release artifacts, and optional-format claims.

P0 is planning and hygiene only. It creates no book-content result, proof
adequacy result, reader release, or evidence transition.

## P1 — Ten-chapter semantic depth

### The quality packet

Each chapter must receive one reviewable packet containing all of the following.

#### 1. Crisp claim and scope

- one sentence naming the chapter's distinct architectural responsibility;
- an explicit authority ceiling and non-claim boundary;
- one falsifier or disconfirming observation; and
- a scope check showing why the material belongs in this chapter rather than a
  neighbor or a new chapter.

#### 2. Audited prior-art delta

- at least three genuinely distinct primary-source comparator families unless
  a documented scarcity exception is approved;
- passage-reviewed source notes for every comparator used to claim novelty;
- a strongest-neighbor table with `already known`, `book delta`, `remaining
  uncertainty`, and `test implication`; and
- no credit for duplicated versions, surveys substituting for primary work, or
  bibliography growth unconnected to prose.

The chapter-specific comparator review must include the hardest relevant
alternative, such as compound-AI/service composition, capability and
object-security traditions, evaluator capture, sandbagging, prompt-injection
limits, deployment assurance, data-deletion causality, or governance overhead.

#### 3. Four-part idea-depth treatment

- the crisp claim;
- the audited prior-art delta;
- at least two non-obvious consequences derived across adjacent stack layers;
  and
- the strongest objection or countermodel, answered with the remaining
  residual rather than a rhetorical dismissal.

#### 4. Architecture that can be built or rejected

The prose must make the mechanism, interfaces, invariants, failure modes,
minimum viable implementation, mature endpoint, proof hooks, test hooks,
source crosswalk, and next-chapter handoff mutually consistent. At least one
worked trace must cross a real interface and include a refusal, fallback,
quarantine, rollback, or abstention path.

#### 5. Evidence route

- one minimum executable fixture or experiment;
- at least one matched baseline or negative control where the claim is
  comparative;
- explicit metrics for utility, harm, cost, latency, governance burden, and
  residuals when applicable;
- a support-state disposition rule; and
- an exact blocker when execution is not yet possible.

#### 6. Human-reading treatment

The Human Reading Path must preserve the idea delta, strongest objection,
worked example, evidence boundary, and handoff in calmer prose. It may compress
apparatus but may not silently strengthen the claim.

#### 7. Review surfaces

Update the book outline, chapter review, source matrix, claim/evidence matrix,
proof adequacy review, per-chapter evidence plan, reader delta, and changelog as
the packet requires. A packet is incomplete when the chapter prose changes but
its governing review surfaces remain stale.

### Cohort floor

After apparatus and code fences are removed using the frozen activation
tokenizer:

- no one of the ten may remain below 4,487 words; and
- the ten-chapter median must reach at least 4,944 words.

These thresholds cannot complete a packet by themselves. The validator must
also reject repeated/template prose, redundant restatement, citation dumping,
decorative diagrams, duplicate objections, and text added only to reach the
floor. If a chapter can make its full case more concisely, it needs an explicit
semantic-review exception that identifies what the comparison cohort covers
that is genuinely inapplicable; the cohort median still applies.

### Chapter-specific burden

| Chapter | Depth burden that must be visible at completion |
|---|---|
| Scalable oversight | Correlated evaluators, weak-supervisor limits, direct-review baseline, independent outcomes, escalation and abstention. |
| Weight custody | Threat model, key/weight lifecycle, hardware-root limits, revocation, extraction and insider paths, recovery. |
| Supply-chain integrity | Identity/lineage/signature separation, derivative and revocation propagation, stale BOM/advisory controls, deployment handoff. |
| Open-ended improvement | Archive dynamics, novelty versus usefulness, evaluator evolution/capture, resource/stop budgets, negative-knowledge retention. |
| Inter-stack protocols | Identity, authority, evidence, settlement, replay, privacy, revocation, and protocol-version failure remain separate. |
| Governed deliberation | When extra compute helps or harms, candidate diversity, verifier independence, stop rules, fallback, abstention, full cost. |
| Capability thresholds | Measurement uncertainty, threshold gaming, binding commitments, downgrade/rollback, organizational and technical enforcement. |
| Adversarial evaluation | Selection-context shifts, sandbagging, monitor interference, training-time versus inference-time evidence, independent replay. |
| Safety cases | Claim-argument-evidence structure, defeaters, living updates, assurance independence, residual acceptance, release coupling. |
| Data engines | Full-state lineage, forgetting, influence/privacy/storage distinctions, descendant invalidation, checkpoint authority, rollback. |

## P2 — Owned formal and executable depth

### Ownership gate

Each chapter must own one Lean module whose name is bound in
`book_structure.json`, the proof manifest, and the proof adequacy review. The
two borrowed mappings must become:

- `AsiStackProofs.AdversarialEvaluation`; and
- `AsiStackProofs.OpenEndedImprovement`.

Other modules may be imported, but a borrowed module cannot be the chapter's
only formal owner.

### Semantic-adequacy gate

Each owned module must model the chapter's actual record, state, trace, or
lifecycle and provide, at minimum:

- one derived positive admissibility or preservation result;
- two distinct derived negative-case or blocking results;
- one lifecycle, transition, or trace result;
- one cross-layer invariant, non-escalation result, rollback property, or
  explicit impossibility boundary; and
- an explicit limitation explaining what the finite model does not establish.

As an anti-regression signal, the module should contain at least five
derived/decomposed theorem declarations. The number is not sufficient: five
renamed projections fail the gate.

### Executable bridge

Every module must bind to at least one schema/fixture/harness row that exercises
the same fields and one expected-invalid case. The bridge records whether the
test is implemented, synthetic, local, deployed, or blocked. Formal truth over
a finite record must not be described as model behavior, evaluator quality, or
production safety.

### Review and build

- update `docs/proof_adequacy_review.md` and the proof artifact audit;
- require mutation tests for missing fields, authority widening, evidence
  laundering, and false rollback where applicable;
- run the full Lean build and proof validators; and
- preserve all non-claims and support states unless a separate evidence
  transition is accepted.

## P3 — Current-spine curated reader

### Edition identity

Do not add the ten chapters to `editions/reader_manuscript/v1_0`. That directory
is a frozen historical snapshot and its regeneration policy forbids rendering
it against a divergent active spine.

Create a new versioned successor, provisionally
`editions/reader_manuscript/v2_0`, with:

- all 54 active chapter IDs in manifest order;
- its own source commit, generated baseline, overlays, curation contract,
  chapter records, review matrix, reconciliation approval, format matrix,
  blockers, and release record;
- merge/split lineage for every chapter whose identity changed after the v1.0
  snapshot; and
- an explicit relationship to the immutable v1.0 historical manuscript.

The final directory/version is chosen prospectively and cannot be renamed in
response to artifact outcomes.

### 54/54 chapter-text gate

Every active chapter must have exactly one curated record and file. Each record
must preserve:

- claim meaning and support state;
- implementation horizon and unrun-test boundaries;
- source and formal-coverage boundaries;
- strongest objection, material residuals, and worked example;
- reader stakes, payoff, and next-chapter continuity; and
- any key-figure caption, text equivalent, alt text, and non-claim boundary.

The generated Human projection and curated manuscript report separate counts
and statuses. No surface may call generated coverage curated coverage.

### Text release ladder

Select one initial current-spine text artifact before rendering. Canonical
curated HTML is the default candidate; EPUB, DOCX, PDF, audio, and embedded
audio remain separate formats with separate gates.

For the selected format:

1. freeze the exact manuscript source and format profile;
2. reconcile 54/54 chapter meaning;
3. render and structurally inspect the exact artifact;
4. run application/browser layout review across representative and risk-based
   pages plus all chapter entry points;
5. run automated accessibility-tree, keyboard, language, heading, landmark,
   link, image-alt, table-header, contrast, reflow, and duplicate-ID checks;
6. record what was and was not screen-reader or application reviewed without
   laundering automation as a human review;
7. resolve or preserve every blocker; and
8. create an exact edition release record or an exact blocked terminal record.

External-human prepublication review is not required. The release may say that
no independent human or institutional review occurred; it may not claim one.

## P4 — Evidence adjudication and next campaigns

### Completed-result adjudication first

Before opening a new campaign, build one transition-candidate ledger covering
all completed post-v2 and QCSA results that were flagged as promotion candidates
or could plausibly support a narrower claim. Every row must record:

- exact result and immutable evidence references;
- candidate claim and owner;
- comparator, cohort, cost, independence, transfer, and validity limits;
- counterevidence and residuals;
- one disposition: `promote`, `narrow`, `no_change`, or `refute`;
- whether an accepted evidence-transition record exists; and
- the exact chapter/appendix/ledger changes the disposition permits.

The governed-work flagship is not missing from the repository: its accepted
record is currently a bounded `no_change` transition and the core dispositions
preserve no support effect. Audit whether a narrower non-core claim satisfies
the transition schema, but do not presume that it does. The five QCSA
`promote` recommendations are review inputs, not transitions.

### Next campaign selection

Only after the candidate ledger is complete, choose at most two next campaigns:

1. **Governance tax on useful natural work.** Compare governed and matched
   baseline systems on broader natural tasks and stronger available models;
   report useful throughput, unsafe release, false acceptance, abstention,
   quarantine, latency, token/tool cost, human burden, rollback, and residuals
   together.
2. **Residual honesty under pressure.** Test whether systems retain, discover,
   route, and reopen material residuals when reward, time, context, or evaluator
   pressure favors premature closure; include a simple disclosure baseline,
   adversarial omission controls, independent outcome checks, and governance
   cost.

Each selected campaign must freeze workload, splits, models, prompts, budgets,
baselines, evaluators, independence limits, harms, stop rules, transition rules,
and result schema before outcomes are opened. Real effects require
effect-complete rollback across changed files, state, caches, descendants, and
receipts.

Negative results and failed pilots remain permanent artifacts. No campaign is
required to produce a promotion.

### Terminal P4 disposition

The candidate ledger adjudicates all 21 identified post-v2, post-v2.1, and
QCSA candidates: five exact non-core promotions, eight narrowings, six
no-change decisions, and two exact refutations. Every row has an accepted
transition record, and all 54 chapter-core claims remain at `argument`.

Both selected campaigns were frozen before model outputs were opened and
completed all 36 planned calls with zero retries. All 36 calls exhausted their
256-token cap; 34 ended inside an unclosed reasoning block, while two closed
reasoning but still emitted no requested final JSON object. The governance
comparison therefore produced no admissible
release denominator, while the residual-pressure comparison produced no
admissible disclosure denominator. Both are accepted `no_change` dispositions;
the raw outputs, evaluator receipts, costs, failures, future burdens, and
non-claims remain permanent artifacts. The independent local rollback harness
passed 12/12 exact nine-surface restorations and detected 12/12 omission
controls, but that result applies only to the declared harness.

## P5 — Coherent release and closure

### Version discipline

- Patch releases repair reproducibility, security, rights, citation, or
  publication defects without claiming a new coherent content/evidence cycle.
- A minor content release requires completed P1–P4 reconciliation, current
  reader-parity disposition, one stable architecture delta, and an exact
  release note describing what did and did not change.
- A major release changes the architecture, edition contract, or book thesis
  materially and requires explicit migration guidance.
- No version is selected merely because enough commits accumulated.
- Immutable historical tags are never moved or rewritten.

### Closure transaction

1. reconcile chapters, outline, source matrix, evidence matrix, proof review,
   reader manifests, public status, and changelog;
2. run the full validation registry, schema checks, source checks, Lean build,
   Quarto render, AI/Human projections, browser/application checks, and selected
   reader-format gates;
3. choose release or honest no-release based on the frozen criteria;
4. if releasing, build once, deploy the tested bundle without rebuilding,
   attest it publicly, archive it immutably, and record tag/commit/digest/rights;
5. write the completion declaration and mark every priority/milestone terminal;
   and
6. activate no successor silently.

### Terminal P5 disposition

The cycle closes without a new public living-book version. The editorial and
formal quality floor, 54-chapter curated-reader successor, evidence
adjudication, and two preregistered campaign dispositions are coherent and
complete, but they do not create a new book architecture, thesis, or
chapter-core evidence state. Both new model comparisons also ended in retained
structured-output protocol failures. Minting a minor version for accumulated
maintenance would therefore violate this roadmap's own version discipline.

The exact 54-chapter curated HTML archive remains approved under its separate
local edition record. `v2.3.0` remains the latest immutable public living-book
release. No new source tag, public deployment, immutable public site archive,
rights grant, or source-commit claim is created by this closure. The terminal
authority is
`release_records/2026-07-13-post-v2-3-quality-reader-cycle-no-public-release.json`,
with the complete residual and non-claim statement in
`docs/post_v2_3_quality_floor_reader_completion_declaration.md`.

## Milestones

| Milestone | Activation state | Completion evidence |
|---|---|---|
| M0 — Critique calibrated | completed | Exact cohort, reader-history, proof-ownership, evidence-disposition, and hygiene audit. |
| M1 — Successor authority active | completed | Roadmap, schema, status, validator, public pointers, no support or release effect. |
| M2 — Source tree clean | completed | False orphan finding resolved and declared-redirect hygiene guard passing. |
| M3 — Ten semantic packets complete | completed | Ten packet records, depth cohort gate, outline/review/source reconciliation. |
| M4 — Ten owned formal packets complete | completed | Ten owned modules, semantic review, fixture bridges, Lean/build gates. |
| M5 — 54-chapter reader source reconciled | completed | New versioned manifest, 54 records/files, zero meaning divergence. |
| M6 — Reader text artifact dispositioned | completed | Exact release or blocked record for the selected format. |
| M7 — Evidence candidates adjudicated | completed | Complete 21-row candidate ledger and accepted promote/narrow/no-change/refute records. |
| M8 — Selected campaigns dispositioned | completed | Frozen preregistration, 36 retained model outputs, independent evaluator receipts, exact costs, two accepted `no_change` transitions, and explicit protocol-failure residuals. |
| M9 — Cycle reconciled and closed | completed | Full local validation, exact no-public-release transaction, public-truth reconciliation, and completion declaration. |

## Stop and amendment rules

- A new chapter requires an amendment proving that the need cannot be met by
  deepening, merging, or reframing an existing owner; no such amendment may be
  accepted before M3–M6.
- A new empirical campaign requires completed candidate adjudication and a
  frozen preregistration.
- A new reader format requires a prospective format-profile amendment and its
  own application/release gates.
- A support-state change requires an accepted evidence transition; roadmap
  completion is never one.
- A blocker that survives three genuinely different resolution attempts is
  recorded with artifacts, residuals, and the smallest authority needed to
  continue.
- Scope may shrink after negative results. It may not expand to rescue a desired
  outcome.

## Definition of done

The project can point to this roadmap as complete when:

- P0–P5 and M0–M9 are terminal and machine/prose state agrees;
- all ten chapter packets pass both semantic and cohort floors;
- all ten have owned, semantically adequate formal surfaces and executable
  bridges or exact blockers;
- the v1.0 historical reader is intact and the 54-chapter successor is fully
  reconciled;
- the selected reader text format has an exact release or blocked record;
- no undeclared chapter HTML or duplicate active roadmap remains;
- completed evidence candidates and selected campaigns are fully dispositioned;
- no citation, theorem, test, reader artifact, review, release, or support state
  is overstated;
- the full local and hosted release chain passes for any published artifact;
  and
- the completion declaration names all residuals, non-claims, and any next
  work without activating it.

## Canonical execution prompt

> Complete `docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md` in
> priority order. Preserve immutable v1.0 reader and v2.3.0 release history.
> Add no chapter until all ten depth and reader-parity gates pass. For each of
> the ten chapters, finish the semantic packet, primary-comparator audit,
> strongest objection, worked trace, evidence route, Human Reading Path, owned
> Lean module, negative cases, executable bridge, review surfaces, and cohort
> floor without padding. Create a new versioned 54-chapter curated-reader
> successor; do not mutate the 44-chapter historical v1.0 spine. Adjudicate all
> completed evidence candidates before preregistering at most the governance-tax
> and residual-honesty campaigns. Preserve costs, failures, residuals,
> rollback, non-claims, and all support-state boundaries. Release only an exact
> tested coherent artifact; otherwise write an honest blocked or no-release
> record. Stop only when every priority and milestone has a terminal artifact
> and the full validation, Lean, render, reader, public-truth, and attestation
> gates agree.

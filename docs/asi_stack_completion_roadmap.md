# ASI Stack Completion Roadmap

Roadmap ID: `asi-stack-completion-2026-07-10`

Authority: Corben Sorenson

Status: completed historical v2.0.0 roadmap

Active successor: `docs/post_v2_evidence_roadmap.md`

Supersedes for execution priority: the open-ended sequencing in
`docs/v1_x_beyond_sota_roadmap.md`

Preserves as subordinate workstreams:
`docs/historical_project_incorporation_roadmap.md` and
`docs/external_ai_review_remediation_program.md`

## Goal to point at

> Finish **The ASI Stack: A Governed Systems Architecture for Advanced AI,
> with ASI as the Stress Case** as one coherent, technically serious living
> book and research artifact. Preserve one manifest-driven source of truth;
> produce a readable narrative book, a complete architecture reference, and an
> auditable evidence/proof/release registry; fold the strongest ideas from the
> historical projects into existing chapter owners before adding chapters;
> deepen the three defended contributions through source-grounded argument,
> executable traces, bounded proofs, adversarial controls, and honest residuals;
> keep every claim at the support state it has actually earned; and publish the
> completed work through a reproducible build, deploy, attestation, citation,
> licensing, and immutable-archive process. No external human review or outreach
> is a prepublication gate. The author declares completion only after every
> exit criterion in this roadmap is either passed or explicitly rejected with a
> durable reason.

This paragraph is the preserved historical goal that governed v2.0.0. New
post-v2 task prompts should point to `docs/post_v2_evidence_roadmap.md`.

## Product decision

The project is one source system with three deliberate products:

1. **Narrative technical book.** A bounded, edited route that explains the
   thesis, running example, architecture, objections, failure stories, and
   consequences without exposing the full research scaffold in every chapter.
2. **Architecture reference specification.** The complete manifest in canonical
   order, with interfaces, authority ceilings, invariants, failure modes,
   implementation horizons, protocols, proofs, tests, and source crosswalks.
3. **Evidence, proof, and release registry.** Machine-readable and readable
   records for claim states, evidence-quality dimensions, transitions, sources,
   proof scope, test results, residuals, versions, and deployed artifacts.

The narrative projection may omit reference chapters from its reading spine,
but it may not delete them from the reference or silently change their claim
state. The registry describes evidence; it is not itself proof that the records
are true.

## Contribution decision

Depth is concentrated in three contributions:

1. **Governed-cognition interface contracts:** typed boundaries that separate
   intelligence, authority, evidence, memory, planning, execution, and release.
2. **Public claim-state transition discipline:** explicit support states,
   multidimensional evidence quality, promotion blockers, demotion, and
   reproducible transition records.
3. **Record/reality reconciliation and residual honesty:** effect observation,
   artifact identity, replay, rollback, revocation, causal order, and residual
   conservation when records and the world disagree.

Verification bandwidth and governance economics are the shared empirical
lane. Other chapters support, integrate, or challenge these contributions; they
are not separate flagship novelty claims by default.

## Author decisions now locked

| Decision | Selected policy | Consequence |
|---|---|---|
| Title positioning | Retain **The ASI Stack**; reframe the subtitle around governed advanced-AI systems and make ASI the stress case. | Current public source uses the reframed subtitle. Historical v1.0.0 records retain the former title. |
| Prepublication review | Author-only completion process; no external-human outreach or review gate before completion. | Existing specialist packets are preserved for possible post-publication use. Their absence cannot block completion and cannot be represented as independent review. |
| v1.0.0 site archive | Do not backfill. | No archive will be fabricated from a later render. The v1.0.0 source tag/release remains historical; immutable full-site archives begin with the next eligible clean tag. |
| Licensing | Delayed opening with a predefined final split. | The active manuscript remains all-rights-reserved. At the first author-declared completed major release, cleared author-owned prose/figures are intended for CC BY 4.0 and cleared software-like artifacts for Apache-2.0; mixed, imported, private, local-project, trademark, and third-party material stays excluded unless separately cleared. |
| Contributions | Closed during prepublication. | No pull request, issue, or unsolicited material is accepted as manuscript input before completion. A future contribution policy must match the operative outbound licenses. |

The licensing row is a publishing policy, not legal advice or a claim of current
clearance. The operative grant remains `LICENSE.md` until a final-release
change installs exact texts, notices, file routing, and release snapshots.

## Non-negotiable invariants

- `book_structure.json` is the only authority for active chapter identity,
  order, titles, and file paths.
- Quarto source is canonical; deployed pages and all derivatives are products
  of the tested source commit.
- Active counts are generated. Historical counts appear only inside explicit
  historical scope.
- A logical layer is a responsibility and authority boundary, not a mandatory
  separate model or process.
- Claim label, support state, evidence-quality vector, proof scope, and release
  state remain separate dimensions.
- No source note, schema, passing linter, finite Lean theorem, synthetic
  fixture, local replay, reviewer opinion, or public deployment is silently
  upgraded into stronger evidence.
- Every material action has an authority source, causal predecessor, observed
  effect or refusal, residual disposition, and rollback/revocation route.
- New chapters are exceptional. Existing chapter owners are improved first;
  a new chapter must own a distinct interface, invariant, artifact type, or
  failure family that cannot be integrated cleanly elsewhere.
- Private raw source exports and uncleared historical-project material never
  enter the public repository.
- No prepublication external-human review, solicitation, contribution, or
  reader approval is required or claimed.

## Workstream A — Coherent public release

Outcome: source, tested artifact, deployment, and public status all describe
the same book state.

Required work:

- keep one generated canonical status object for active version, source commit,
  tree state, product profile, chapter/source/claim counts, and transitions;
- keep README, landing, status, product routes, sidebar, and rendered chapter
  graph consistent with that object;
- build Pages from an empty output directory;
- upload a content-addressed tested bundle only after the deep gate passes;
- deploy that exact bundle without rebuilding;
- attest the root, `/latest/`, version index, product routes, chapter order,
  H1 uniqueness, commit marker, and count consistency on the public site; and
- retain the failed/stale public observation as history rather than rewriting
  it after the fact.

Exit criterion: one clean commit completes the real GitHub
build → deploy → attest chain, and a fresh deployed crawl agrees with its
canonical status. CI failure or public disagreement reopens this workstream.

## Workstream B — Narrative book completion

Outcome: a reader can understand and remember the book's argument without
traversing the full reference scaffold.

Required work:

- preserve the bounded narrative spine unless an authorial coherence pass
  records a stronger route;
- establish one running governed-change example that accumulates across the
  narrative rather than restarting in each chapter;
- ensure each narrative chapter has a question, mechanism, concrete failure,
  strongest objection, evidence-changing condition, and specific handoff;
- cut repeated caveats after their first authoritative statement and link back
  to the owning boundary;
- move large inventories, schema fields, theorem lists, and validation detail
  into the reference or registry;
- make part openings and transitions explain why the next layer is necessary;
- inspect figures, tables, mobile/desktop layout, keyboard paths, contrast,
  headings, link text, and text equivalents; and
- stabilize prose before generating final EPUB, DOCX, PDF, or audio artifacts.

Exit criterion: the narrative projection renders cleanly, every selected
chapter satisfies its editorial contract, no high-priority continuity issue is
open, repetition is bounded, figures are legible and necessary, and all omitted
chapters remain discoverable in the reference.

## Workstream C — Architecture reference completion

Outcome: every active chapter owns a precise architectural job and composes
with adjacent chapters.

For every chapter, finish one coherent packet containing:

- problem and insufficiency of current approaches;
- core claim and strongest objection;
- mechanism and typed inputs/outputs;
- authority, state, and lifecycle boundaries;
- invariants and weakening conditions;
- failure modes and attractive invalid cases;
- minimum viable implementation;
- mature endpoint without present-tense overclaiming;
- proof, test, evidence, and source route;
- at least one useful interface/lifecycle diagram; and
- a handoff that consumes the preceding artifact and creates the next need.

Apply the historical-project roadmap existing-chapter first. Treat all mined
projects as one local lineage, not independent replication. The first priority
packets are Evidence States, Benchmark Ratchets, Artifact Graphs, Integrated
Reference Architecture, System Boundaries, and Cognitive Compilation. Decide
Durable Semantic Memory and Knowledge Lattices only after independent
literature and ownership tests show that existing memory/context/artifact
chapters cannot own it.

Exit criterion: all 54 active chapters have complete packets, source/outline/
manifest/appendix/proof/evidence crosswalks agree, no concept has competing
definitions, and every project-mining packet has a completed, rejected,
deferred, or superseded disposition.

## Workstream D — Evidence and empirical depth

Outcome: the book demonstrates its methods on bounded real operations and
states exactly what those demonstrations do not generalize to.

Required work:

- maintain the governed repository-change vertical slice with real disposable
  Git mutations, authority checks, independent effect observation, attacks,
  refusal, rollback, quarantine, and a simpler matched baseline;
- connect one event vocabulary to authority monotonicity,
  revocation-before-effect, evidence-transition integrity, residual
  conservation, and causal order;
- measure success, unsafe effects, false accepts/rejects, cost, latency,
  operator burden, rollback, and residual discovery for the governed and
  simpler routes;
- repeat or expand only when the next run changes transfer distance, adversarial
  strength, coverage, independence, or reproducibility;
- treat negative, null, demoting, and refuting outcomes as useful results; and
- populate evidence-quality vector deltas for any future accepted transition.

Exit criterion: the flagship slice and invariant suite reproduce from tracked
inputs, every expected-invalid mutation is rejected, governance overhead and
benefit are reported together, residuals remain visible, and each affected
core claim has an explicit promote/narrow/demote/refute/no-change disposition.
No blanket core-claim promotion is required.

## Workstream E — Formal depth

Outcome: formal artifacts clarify finite guarantees without being marketed as
runtime safety.

Required work:

- lead public proof summaries with adequacy class and claim scope, not theorem
  count;
- deepen the four cross-stack invariants on the same trace vocabulary used by
  the vertical slice;
- state clock, concurrency, revocation-tie, missing-event, and adversarial-log
  assumptions explicitly;
- keep Lean/Python fixture bridges exact where both are claimed;
- test proof/prose correspondence and reject theorem presence as evidence of
  deployment enforcement; and
- retire or narrow proof targets that are only field projections when a deeper
  invariant is the actual claim.

Exit criterion: Lean builds cleanly, the proof manifest and prose agree, each
high-impact target has an adequacy review, mutation controls fail as expected,
and public language never exceeds the proved finite model.

## Workstream F — Sources, prior art, and terminology

Outcome: the book is modern, source-grounded, and candid about lineage.

Required work:

- keep external sources in source notes and Appendix H with chapter routing;
- use primary sources for technical comparisons whenever available;
- distinguish local-project lineage, author-supplied material, external
  literature, implementation evidence, and review input;
- audit the three defended contributions against the closest prior art;
- reduce coined terms that do not buy a precise interface or failure boundary;
- state novelty as positioning until a stronger comparison justifies more; and
- refresh time-sensitive standards, protocols, threat models, and governance
  references as part of the living update cadence.

Exit criterion: every generalized chapter claim has an appropriate external
comparator or an explicit gap; every source used in prose is traceable to an
ingested note; terminology has one owner and definition; and no bibliography
entry is treated as evidence merely because it is listed.

## Workstream G — Release, archive, license, and citation

Outcome: completed editions are reproducible, correctly named, and governed by
unambiguous rights and version records.

Required work:

- preserve v1.0.0's former title, tag, source commit, and no-site-archive state;
- begin immutable full-site archives with the next eligible clean release;
- build archives only from the exact tested tag-bound bundle, upload without
  overwrite, redownload, verify SHA-256, and record the public URL and digest;
- keep `/latest/` explicitly mutable and version-index metadata distinct from
  immutable storage;
- preserve the reframed title across current source, site, repository
  description, and the next release's citation metadata while keeping former
  title lineage;
- keep the active drafting repository all-rights-reserved;
- before the completed major release, perform record-level ownership and
  mixed-rights review, resolve or exclude every non-cleared route, install exact
  CC BY 4.0 and Apache-2.0 texts/notices for the selected lanes, and snapshot
  the routing policy in the release record;
- keep contributions closed until a compatible inbound policy is deliberately
  opened; and
- create only the formats actually rendered and inspected.

Exit criterion: the final tag, commit, citation, title, product manifests,
license snapshot, tested bundle, deployed site, immutable archive, checksums,
and release record all identify the same artifact state.

## Execution order

1. **Close the coherence release.** Commit, push, merge, observe the real
   build/deploy/attest chain, and repair any failure before proceeding.
2. **Complete the six highest-leverage historical-project packets.** This
   prevents later chapters from laundering local lineage into capability
   evidence.
3. **Finish the narrative spine and chapter transitions.** Do prose and
   structure before final-format work.
4. **Finish remaining reference packets in dependency order.** Open at most
   three packets at once: evidence owner, execution/model owner, support lane.
5. **Deepen the flagship empirical and formal lanes.** Prefer one material
   execution or source-grounded result over more planning surfaces.
6. **Run the final source, terminology, claim, and product reconciliation.**
7. **Declare a major-release candidate.** Freeze prose and perform the single
   format, rights, citation, archive, and publication pass.
8. **Declare completion.** Record every exit criterion, unresolved residual,
   and non-claim. Only then invite ordinary public readership or optional
   post-publication specialist critique.

## Stop rules

Stop and record a defer/reject decision when:

- a proposed chapter has no unique ownership boundary;
- a source cannot be lawfully or reliably ingested;
- a test cannot distinguish the claimed mechanism from a simpler baseline;
- a proof target does not constrain the behavior claimed in prose;
- a metric can improve while the governed objective worsens;
- an artifact would only restate a status already owned elsewhere;
- a format will be regenerated by unsettled prose; or
- a requested support-state change lacks a complete accepted transition.

Do not stop merely because the honest result is negative. Narrowing, demotion,
refutation, and explicit residuals are valid completion outcomes.

## Definition of done

The book is complete only when all of the following are true:

- the canonical manifest, outline, chapters, appendices, products, status, and
  deployed site agree;
- all active chapters satisfy the reference packet contract;
- the narrative book is coherent, bounded, and free of open high-priority
  continuity defects;
- the three defended contributions have explicit prior-art, argument,
  mechanism, objection, evidence, and residual records;
- the flagship vertical slice and invariant suite reproduce and report both
  benefit and governance tax;
- every core claim has a current evidence-quality vector and explicit final
  disposition, without required blanket promotion;
- proof summaries match finite formal scope and the Lean workspace builds;
- all validators, schemas, fixtures, negative controls, clean render, browser
  checks, and public attestation pass for the same commit;
- title and historical-title lineage are consistent;
- rights routing is resolved for every released file, with mixed material
  excluded or separately cleared;
- every published format and archive is tied to exact bytes and checksums;
- no private source material, fabricated evidence, unearned review, or
  overclaim appears; and
- the author records a final completion declaration and remaining residuals.

External human review is not in this definition of done. If post-publication
review later finds an error, the living-book process reopens the affected
chapter, claim, proof, source, or artifact without rewriting the historical
release record.

## Current baseline and immediate next action

The roadmap completed on 2026-07-10 for tag `v2.0.0` and source commit
`52e54b71681f3d04644a4142875718d7b55f6dbd`. Build run `29131665495` and
deploy/attest run `29131819091` agree on the exact clean tested bundle. The
immutable rendered-site archive was published to the exact-tag GitHub Release,
redownloaded, and verified at SHA-256
`5772aa8e47df279bbb38e38b2a3564489f6b3f3f65f8ff2df373f318e2c9eaf9`.
The completion evidence ledger and `docs/v2_0_completion_declaration.md` bind
the final title, citation, license snapshot, products, residuals, and
non-claims to that artifact state.

There is no remaining action in this roadmap. Future living-book work starts a
new post-v2 update cycle and reopens only affected contracts; it must not
rewrite this historical completion state.

## Non-claims

This roadmap is an execution authority, not evidence that its outcomes already
exist. It does not prove ASI, AGI, model quality, alignment, runtime safety,
economic value, novelty, external validity, legal compliance, ownership,
publication quality, or final completion. It authorizes no support-state
promotion by itself.

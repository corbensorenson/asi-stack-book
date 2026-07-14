# ASI Stack Post-v2.3 Clean Handoff, Reader Formats, and Evidence Renewal Roadmap

Roadmap ID: `asi-stack-post-v2-3-handoff-reader-formats-evidence-renewal-2026-07-13`

Authority: Corben Sorenson

Status: active canonical successor roadmap; unfinished work only

Machine status:
`roadmap_records/post_v2_3_handoff_reader_formats_and_evidence_renewal_status.json`

Predecessor:
`docs/post_v2_3_quality_floor_and_reader_completion_roadmap.md`, completed
2026-07-13 without a new public living-book release

Latest immutable public living-book release: `v2.3.0`

## Goal to point at

> Turn the completed post-v2.3 work into a durable, cleanly handed-off source
> state; extend the exact 54-chapter reader from its approved local HTML archive
> into only those additional text formats that pass format-specific gates;
> deepen external anchoring where a named comparator changes a chapter's claim,
> boundary, objection, or test; repair the failed natural-work evidence protocol
> before spending another campaign; refresh one genuinely current Project
> Theseus evidence lane; and close with an exact edition release, public release,
> blocked record, or no-release record. Preserve every negative result, historical
> release, support-state boundary, and rights boundary. Do not turn citation
> counts, format counts, commits, or version numbers into proxies for quality.

This roadmap contains only work that remained unfinished after the post-v2.3
quality/reader cycle. It does not reopen that completed cycle. It also does not
assume that the next public living-book version is `v2.4`: extending reader
formats may justify a new edition record without changing the canonical
living-book version.

## Critique adjudication

| Claude finding | Current-tree judgment | Roadmap treatment |
|---|---|---|
| The completed cycle is still uncommitted. | **Valid and urgent.** At activation, `HEAD` is `cb7493ae57d576a8bf5fcc54f375683ecf929b54`, with 166 dirty paths: 97 tracked modifications and 69 untracked paths. | P0 makes a coherent, verified clean handoff the first execution transaction. It forbids starting a new empirical campaign while the completed cycle exists only as an anonymous working-tree state. |
| The 54-chapter reader should advance beyond HTML. | **Valid, with a scope correction.** The v2.0 reader has one approved exact local HTML archive; EPUB, DOCX, PDF, audio, and embedded audio remain explicitly deferred. | P1 attempts EPUB, PDF, and DOCX against one frozen 54-chapter source. Each format has its own artifact, application, accessibility, digest, blocker, and release decision. Audio remains deferred. |
| The ten newer chapters need deeper external anchoring. | **Partly valid.** The chapters now have three to eight assigned `ext_` source records and completed comparator packets, so they are not ungrounded. They remain less broadly anchored than several mature chapters. Raw citation volume is not a quality criterion. | P2 builds a claim-specific source-gap matrix and adds only passage-reviewed primary comparators that alter the prior-art delta, strongest objection, failure boundary, or evidence design. |
| Reasoning-trace faithfulness, world models/JEPA, foundations, and Tier-2 items remain. | **Valid as an audit queue, not automatic chapter growth.** Earlier scans routed these topics but current ownership and insertion completeness must be rechecked against the 54-chapter spine. | P2 improves existing owners first, records explicit accept/narrow/defer/reject dispositions, and requires an ownership test before any new chapter proposal. |
| Governance tax on natural work should remain the flagship. | **Valid only after protocol repair.** The prior 36-call cycle produced no admissible structured denominator because every response exhausted the 256-token cap. | P3 freezes a non-evidentiary protocol-repair preflight before any new outcome-bearing campaign. A failed preflight ends in a blocked record, not another uninterpretable campaign. |
| Carry the two QCSA refutations into novelty positioning. | **Valid public-truth reconciliation.** The evidence and non-core ledgers already expose both exact refutations, while the contribution novelty ledger still says a true refutation is missing. | P0 reconciles the novelty ledger and its validator without implying a chapter-core refutation or general QCSA failure. |
| Import the next Theseus parity export. | **Partly stale.** A bounded accelerator-parity manifest import already exists. Currentness, live replay, current work-board state, and artifact truth remain open. | P3 selects one fresh public-safe currentness lane—prefer a current work-board/export or clean replay—only if its authority, digest, publication boundary, and non-claims are explicit. |
| `v2_0/manifest.json` lacks an explicit status. | **Already resolved.** It currently records `status: released` and `release_state: released_exact_curated_html`. | P0 adds a regression guard for status/release-state parity; no fake work item remains. |
| External readers should be required before completion. | **Rejected by author policy.** No external-human prepublication review or outreach is required. | Internal semantic review, exact application-level artifact inspection, automated accessibility evidence, and honest review boundaries remain mandatory. No independent review is claimed. |

## Activation baseline

### Repository and release truth

- `HEAD`: `cb7493ae57d576a8bf5fcc54f375683ecf929b54`.
- Working tree: 166 dirty paths, comprising 97 tracked modifications and 69
  untracked paths.
- Active spine: 54 chapters; chapter-order digest
  `73436ead9fd12b866b2b688d3d5c3849a8a2d556069a4f4c67c8f141af955182`.
- Public-safe source inventory: 280 records.
- Chapter-core evidence: 54 of 54 at `argument`; zero chapter-core promotions
  and zero chapter-core refutations.
- Non-core evidence: 19 upward transitions, 56 accepted promotion-blocking
  decisions, and two exact QCSA fixture refutations.
- Latest immutable public living-book release: `v2.3.0` at
  `e27661166e9105f37cb36d63b15795f80715ca24`.
- Completed post-v2.3 terminal decision: no new public living-book release.

### Reader truth

- Immutable historical curated reader: v1.0, 44 records.
- Current-spine curated reader: v2.0, 54 records, `status: released`.
- Approved format: one exact local canonical HTML archive.
- Archive SHA-256:
  `a2caa97fb9281e1fdfc9a9dda626141d4a876df776c9cbc7408f978751736b50`.
- Deferred formats: EPUB, DOCX, PDF, audio, and embedded audio.
- The HTML record grants no new public license and claims no public deployment,
  independent review, screen-reader review, or legal WCAG certification.

### Evidence truth

- The two post-v2.3 campaigns completed 36 calls with zero retries.
- All 36 outputs hit the 256-token cap; 34 ended in an unclosed reasoning block
  and two closed reasoning without producing final JSON.
- Governance usefulness therefore has no admissible release denominator.
- Residual honesty under pressure has no admissible disclosure denominator.
- Both campaign dispositions remain `no_change`.
- The local rollback harness passed its exact declared slice; it does not prove
  production, remote-effect, or semantic rollback.

## Operating principles

1. **Clean handoff before new evidence spend.** The completed cycle must become
   a reviewable commit series with a clean tree and observed CI/Pages outcome
   before a new outcome-bearing campaign begins.
2. **One frozen source per format family.** EPUB, PDF, and DOCX must derive from
   the same digest-bound v2.0 reader source or be versioned as a later reader
   edition. Mutable live prose may not silently change a frozen candidate.
3. **Format-specific approval.** An approved HTML archive says nothing about
   EPUB navigation, PDF pagination, DOCX styles, or audio treatment.
4. **Existing chapters before new chapters.** Trace faithfulness, world models,
   JEPA, foundations, and Tier-2 material first receive explicit owners and
   section-level tests. A new chapter requires a distinct interface, invariant,
   artifact, failure mode, and proof/evidence program.
5. **Comparator value before citation count.** A new source must change the
   prior-art delta, boundary, objection, or test. Bibliography growth alone does
   not complete P2.
6. **Protocol validity before outcomes.** Structured-output success, evaluator
   separation, denominator integrity, cost capture, and stop rules must pass a
   non-evidentiary preflight before a campaign is opened.
7. **Refutations remain scoped.** The two QCSA refutations apply to their exact
   frozen claims, corpus, implementations, and accounting rules. They are not a
   refutation of QCSA as a family.
8. **Fresh imports need currentness.** A repeated or stale Theseus report cannot
   satisfy the currentness lane merely because its schema validates.
9. **Release names follow coherent deltas.** A reader-format extension does not
   force a new living-book minor version. Tags are never chosen to reward work
   volume.
10. **No external-human prepublication gate.** The project may state that no
    independent review occurred. It may not invent one or require outreach
    before the author considers the book complete.

## Execution board

| Priority | Activation state | Purpose | Terminal authority |
|---|---|---|---|
| P0 — Authority, truth repair, and clean handoff | completed | Activate this successor, reconcile the novelty/status drift, verify the complete dirty cycle, commit coherently, push, and observe the resulting hosted chain. | Clean-tree receipt, commit series, CI/Pages receipts, reconciled public pointers. |
| P1 — 54-chapter multi-format reader | in progress | Produce and disposition EPUB, PDF, and DOCX from one frozen v2.0 reader source; keep audio deferred. | Per-format manifests, exact artifacts, review matrices, and release/block records. |
| P2 — Selective external anchoring and completeness residuals | pending | Close source-specific gaps in the ten newer chapters and audit the trace/world-model/foundations/Tier-2 queue without citation padding or automatic chapter growth. | Passage-reviewed source notes, owner matrix, insertion/disposition records, reconciled chapters and appendices. |
| P3 — Evidence protocol repair and current implementation transfer | pending | Repair the failed natural-work protocol, run at most one warranted flagship campaign, reconcile scoped refutations, and import one fresh Theseus currentness lane. | Frozen preflight/preregistration, exact results or blocker, transition dispositions, currentness import record. |
| P4 — Product reconciliation, release decision, and closure | pending | Reconcile all products and choose exact edition release, public release, blocked closure, or no-release without version or rights laundering. | Terminal declaration, release/block/no-release record, full validation and attestation receipts. |

## P0 — Authority, truth repair, and clean handoff

### Required work

1. Install this prose roadmap and machine status as the sole active successor.
2. Preserve the predecessor roadmap, declaration, no-release record, v1.0
   reader, v2.0 HTML archive, and v2.3.0 release as immutable history.
3. Reconcile `docs/contribution_novelty_ledger.json` and `.md` so the
   support-state-discipline row records the two exact non-core QCSA refutations,
   removes the obsolete claim that no true refutation exists, keeps all 54
   chapter-core claims at `argument`, and removes independent/external review as
   a prepublication requirement.
4. Require `editions/reader_manuscript/v2_0/manifest.json` to keep both
   `status: released` and `release_state: released_exact_curated_html`; reject a
   missing status, a false multi-format release state, or a v1.0 mutation.
5. Freeze the exact working-tree inventory before commit. Review untracked
   files, generated artifacts, large binaries, credentials, private source
   material, license routing, and ignored paths. Nothing enters a commit merely
   because it is dirty.
6. Split the completed cycle into coherent commits where practical: chapter and
   source depth; Lean/executable bridges; reader v2.0; evidence transitions and
   campaign records; roadmap/declaration/release truth; and this successor
   authority. If preserving atomic validation requires fewer commits, record
   that rationale.
7. Before the first push, run the registry, Lean, Quarto, reader, public-truth,
   browser, rights, secret, and diff-integrity gates over the exact commit tip.
8. Push only the tested commit tip. Observe build, deploy, and attestation
   results. A mutable root/`latest` update is not an immutable release.
9. End P0 with a clean working tree or an exact residual inventory explaining
   each intentionally retained local-only path.

### P0 completion gate

P0 is complete only when the cycle is addressable by commit, the remote branch
contains the intended commits, the hosted result matches the tested source or
is explicitly blocked, public roadmap pointers name this successor, the
novelty/status drift is repaired, and no private or unreviewed artifact was
published. Commit count is not a quality metric.

Completed 2026-07-13. The durable receipt is
`docs/post_v2_3_clean_handoff_receipt.md`. Commit
`c2db70988cb3b06860c2994c0bb2e7f3e2874544` passed the commit-bound build,
was deployed without rebuilding, and passed the deployed public-status and
54-chapter graph attestation. The handoff changed no support state, release,
tag, license, or immutable archive identity. P1 is now the active priority.

## P1 — 54-chapter multi-format reader

### Source and version lock

- Preserve the exact approved v2.0 HTML artifact and record.
- Freeze one digest-bound 54-chapter reader source for EPUB, PDF, and DOCX.
- If the reader prose changes materially after the freeze, create a new reader
  edition version or amendment record; do not rewrite the approved HTML record.
- Select format profiles before rendering and record dependencies, locale,
  fonts, toolchain versions, commands, and deterministic inputs.

M2 completed 2026-07-13 through
`editions/reader_manuscript/v2_0/text_format_profile.json`. It binds the exact
54-chapter source, approved HTML predecessor, generated Quarto profile,
toolchain, bounded static-Mermaid route, EPUB/Apple Books path, Typst/Preview
PDF path, deterministic narrative-proposal DOCX reference, and
LibreOffice/page-raster path. The successful pre-freeze EPUB is explicitly a
renderer preflight and must be regenerated; it is not a release candidate.

### EPUB gate

- Validate package, mimetype, container, OPF metadata, language, identifier,
  manifest, spine, landmarks, navigation, chapter order, and cover handling.
- Check all 54 chapter entry points, internal links, footnotes/endnotes, images,
  alt text, tables, code, mathematical content, and key figures.
- Test narrow and wide reflow, font scaling, dark/light presentation where the
  application permits, search/text extraction, and at least one locally
  available EPUB application path.
- Record automation separately from application inspection. Do not claim
  screen-reader or device review that did not occur.

M3 completed 2026-07-13 with a blocked EPUB disposition. The exact tracked
EPUB passes package, metadata, navigation, landmark, spine, chapter-order,
link, image, table, code, note, and reader-boundary automation. Two independent
full renders converge byte-for-byte after stable edition metadata, one package
link repair, one body-matter landmark repair, and two digest-verified pinned
Mermaid/RoughJS state-diagram rasters. Apple Books inspection remains blocked:
the Computer Use native accessibility bridge failed before application state
capture on both the application-name route and a clean-reset bundle-identifier
route. No Apple Books, reflow, font-scaling, theme, search, text-interaction,
screen-reader, device-family, or publication approval is claimed. M3 is
terminally dispositioned as `blocked`; P1 remains active for PDF and DOCX.

### PDF gate

- Record page size, fonts and embedding, bookmarks/outline, metadata, page
  count, links, destinations, heading order, text extraction order, and
  replacement-character checks.
- Raster-review every page for clipping, collision, overflow, blank/near-blank
  pages, orphaned headings, stranded captions, code/table overflow, figure
  legibility, and source-appendix path wrapping.
- Inspect risk pages in a real local PDF viewer and preserve the exact viewer,
  command, screenshots, page list, and residuals.

M4 completed 2026-07-13 with a blocked PDF disposition. The exact tracked,
US-letter PDF is 13,897,492 bytes with SHA-256
`55764db2301e85838233b6357ac81e37dc78b3657c022189778238b7ec770676`.
Automated inspection covers all 565 pages and 270,359 word boxes, confirms four
embedded font rows, 1,142 outline entries and named destinations, 1,418 link
annotations with none unresolved, all 54 chapter titles in order, no
replacement characters, no live-only markers, no blank, low-ink, near-edge,
or out-of-bounds content, and 29 page-complete contact sheets. Internal visual
review covered every page plus all 68 native-resolution Mermaid figures; two
corrupted rasterization candidates and four root-viewBox geometry defects were
rejected and repaired. Two independent full renders converge byte-for-byte
after two diagnosed Mermaid/RoughJS state-diagram pins and fixed-length Typst
date, XMP instance, and trailer-ID canonicalization. Preview inspection remains
blocked because both native control-bridge routes failed before application
state capture. No Preview navigation, bookmark, link, search, selection/copy,
zoom/fit, assistive-technology, Microsoft application, independent-human,
publication, rights, or support-state approval is claimed. M4 is terminally
dispositioned as `blocked`; P1 remains active for DOCX.

### DOCX gate

- Validate OOXML package integrity, styles, headings, section breaks, lists,
  tables, alt text, links, media, equations, metadata, language, and reading
  order.
- Convert with the pinned office path and review every page raster for clipping,
  collisions, blank pages, figure placement, table overflow, and heading drift.
- If Word, LibreOffice, or another local application is available, record the
  exact application-level inspection. Do not infer Microsoft Word approval from
  package validity or LibreOffice conversion.

### Shared release boundary

Each format receives one of `approved_exact_local_artifact`,
`approved_public_artifact`, or `blocked`, with exact digest, bytes, source
snapshot, toolchain, inspection evidence, blockers, rights snapshot,
non-claims, and support-state effect. Approval of one format cannot clear
another. Audio and embedded audio remain deferred unless this roadmap is
amended prospectively.

## P2 — Selective external anchoring and completeness residuals

### Ten-chapter source audit

For each of the ten post-v1-spine chapters, create one row that records:

- the distinct claim and strongest currently assigned primary comparator;
- assigned and prose-used external source IDs;
- passage-review state and exact passage references;
- the strongest omitted or weakly treated neighboring approach;
- whether a new source would change the chapter's delta, objection, boundary,
  mechanism, or evidence design;
- a terminal disposition: `insert`, `narrow`, `already_covered`, `watch`,
  `defer`, or `reject`; and
- the exact chapter, source-note, Appendix C/H, outline, reader, and test changes
  permitted by that disposition.

The ten chapters are scalable oversight, model-weight custody, AI supply-chain
integrity, open-ended improvement, inter-stack protocols, governed
deliberation, capability thresholds, adversarial evaluation, safety cases, and
data engines. No minimum citation count completes a row.

### Cross-cutting residual queue

1. **Reasoning-trace faithfulness.** Improve Artifact Graphs, Adversarial
   Evaluation, Governed Deliberation, and Policy Optimization with a shared
   distinction among private reasoning, reported rationale, action trace,
   receipt, monitorability evidence, and authoritative effect. Add
   trace/action inconsistency and hidden-computation controls. Do not treat a
   chain of thought as an authoritative receipt.
2. **World models, JEPA, and energy-based prediction.** First test ownership in
   Mathematical and Search Substrates, Planning, Data Engines, and the
   Integrated Reference Architecture. Cover predictive state, imagination,
   model-predictive control, causal/interventional limits, prediction-error
   ledgers, versioning, sim-to-real boundaries, and adoption tests. A new
   chapter is permitted only if these owners cannot hold the distinct interface
   without duplication.
3. **Foundations family.** Reconcile CAIS, embedded agency, corrigibility
   limits, Goodhart pressure, and record-level guarantee limits in existing
   opener, alignment, self-improvement, evidence, and integrated-architecture
   owners. Keep philosophical or mathematical limits separate from claims that
   a finite schema solves them.
4. **Tier-2 disposition audit.** Recheck the 37 earlier section-level routes
   against current chapter text and source notes. Preserve completed insertions;
   list only genuinely missing, shallow, superseded, or rejected rows in the
   active queue.

### P2 completion gate

P2 is complete when every scoped source gap has a passage-reviewed artifact or
an honest disposition; all accepted insertions appear in live and reader prose
with source/evidence boundaries; Appendix H, Appendix C, the outline, source
inventory, and source notes agree; no source was added merely to raise a count;
and any proposed chapter passes the ownership test before manifest mutation.

## P3 — Evidence protocol repair and current implementation transfer

### Governance-tax flagship

1. Preserve the prior 36 raw outputs and both `no_change` transitions.
2. Diagnose the structured-output failure without editing the historical
   records. Separate reasoning budget from final-answer budget, use a grammar or
   schema-constrained final channel where the runtime supports it, and make
   truncation an explicit failure state.
3. Run a sacrificial, non-evidentiary preflight on tasks outside every future
   evaluation split. The preflight must demonstrate complete parseability,
   terminal-state capture, cost/latency capture, and evaluator routing across
   all planned arms before preregistration.
4. If two materially different protocol repairs fail the preflight, stop and
   record a blocker. Do not spend the outcome-bearing budget.
5. If the preflight passes, freeze a broader natural-task corpus, models,
   revisions, prompts, tools, matched authority, baseline/governed routes,
   attacks, seeds, budgets, stop rules, utility/harm/cost metrics, evaluator
   independence limits, rollback surfaces, and transition thresholds before
   opening outcomes.
6. Report useful throughput, task quality, unsafe release, false acceptance,
   abstention, quarantine, latency, token/tool cost, governance burden,
   rollback, and residuals together. Zero unsafe releases with zero releases is
   not safety evidence.
7. Accept `promote`, `narrow`, `no_change`, or `refute` exactly as the frozen
   rule dictates. No positive outcome is required.

### QCSA reconciliation and future burden

- Surface the two exact refutations in the contribution novelty ledger.
- Preserve the five exact non-core QCSA upward transitions and their narrow
  boundaries.
- Do not rerun the same saturated synthetic task-decision label. Any future
  QCSA workload must make downstream decisions depend on correct identity,
  include ambiguous cases where clarification can matter, use matched resource
  accounting, and remain a distinct preregistered program.

### Project Theseus currentness lane

- Do not repeat the already accepted accelerator-parity manifest import.
- Prefer one fresh current work-board/export, clean replay, or archived public
  fixture that closes a named stale/currentness residual.
- Freeze source authority, revision, file set, public-safety policy, digest,
  environment, command, expected outputs, artifact-truth checks, negative
  controls, and non-claims before import.
- Keep private payloads, training rows, prompts, solutions, checkpoints, and
  restricted paths out of the public repository.
- A valid import is implementation-reference evidence only unless a separate
  evidence transition clears currentness, replay, comparator, independence,
  transfer, and support-state gates.

## P4 — Product reconciliation, release decision, and closure

### Reconciliation

Reconcile the live book, narrative product, architecture reference, evidence
registry, 54-chapter reader, outline, source inventory, Appendices C/F/H/J/K,
proof and evidence plans, novelty and evidence ledgers, public status, release
profiles, rights inventory, and roadmap machine state. Preserve v1.0, v2.3.0,
the v2.0 HTML record, and all negative outcomes exactly.

### Terminal decision

Choose among:

1. an exact local multi-format reader edition record;
2. an exact public reader-edition release with tested artifacts, explicit
   rights routing, build-once deployment, attestation, and immutable archive;
3. a coherent public living-book release only if the content/evidence delta
   independently satisfies minor-version rules;
4. a blocked record naming the smallest missing authority or dependency; or
5. an honest no-release record.

The roadmap does not preauthorize a public license grant, tag, deployment,
archive, or version. A public release requires the exact authority and tested
artifact transaction appropriate to that effect.

### Validation and closure

Run the registered validation tiers, schema/fixture gates, source and
publication checks, Lean build, Quarto render, AI/Human/product projections,
all-view/all-viewport browser checks, exact reader-format gates, rights and
secret checks, deterministic artifact replay, and terminal release validator.
Write a completion declaration with every priority and milestone terminal,
every residual and non-claim visible, and no silent successor activation.

## Milestones

| Milestone | Activation state | Completion evidence |
|---|---|---|
| M0 — Critique calibrated and successor installed | completed | This roadmap, machine status, predecessor pointer, and stale/already-fixed finding table. |
| M1 — Completed cycle cleanly handed off | completed | Reviewed commit series, clean tree or exact local residual inventory, remote branch, observed CI/Pages result. |
| M2 — Reader source and format profiles frozen | completed | One 54-chapter source digest, pinned toolchain, prospective EPUB/PDF/DOCX profiles. |
| M3 — EPUB dispositioned | completed | Exact EPUB artifact plus pass/block record and application/accessibility evidence. |
| M4 — PDF dispositioned | completed | Exact PDF artifact plus page-complete inspection and pass/block record. |
| M5 — DOCX dispositioned | pending | Exact DOCX artifact plus package/application/layout evidence and pass/block record. |
| M6 — Source and completeness residuals dispositioned | pending | Ten-chapter matrix plus trace/world-model/foundations/Tier-2 insertion or rejection artifacts. |
| M7 — Evidence/currentness work dispositioned | pending | Protocol preflight and at most one flagship campaign; QCSA novelty reconciliation; one fresh Theseus currentness import or exact blocker. |
| M8 — Products reconciled and cycle closed | pending | Full validation, exact release/block/no-release record, completion declaration, no silent successor. |

## Stop and amendment rules

- P1 may attempt EPUB, PDF, and DOCX in parallel after the source freeze, but a
  failure in one format cannot be hidden by success in another.
- Audio or embedded audio requires a prospective roadmap amendment with its own
  narration, pronunciation, timecode, listening, metadata, package, and release
  gates.
- A new chapter requires a written ownership test and manifest amendment after
  existing owners are improved.
- A new empirical campaign requires a passing non-evidentiary protocol preflight
  and frozen preregistration before outcome visibility.
- A second outcome-bearing campaign requires a roadmap amendment; P3 authorizes
  at most one.
- Two materially different failed protocol repairs terminate the campaign lane
  as blocked.
- A support-state change requires an accepted evidence transition. A commit,
  source note, format artifact, proof build, or roadmap milestone is never one.
- Scope may narrow after failure. It may not expand to rescue a preferred
  conclusion.
- No outside reader, reviewer, institution, or outreach step is a
  prepublication dependency.

## Definition of done

This roadmap is complete only when:

- the post-v2.3 cycle is preserved in coherent commits and the intended remote
  handoff is observed;
- the working tree is clean or every retained local-only residual is explicit;
- the v2.0 manifest status remains exact and the contribution novelty ledger
  records the two scoped QCSA refutations;
- EPUB, PDF, and DOCX each have an exact approved or blocked terminal record;
- all 54 curated chapter identities and the approved HTML archive remain intact;
- the ten-chapter external-grounding matrix and the trace/world-model/
  foundations/Tier-2 audit contain only source-specific, passage-reviewed work
  or honest dispositions;
- no new chapter was added without the ownership test;
- the governance-tax protocol either passes preflight and yields a fully
  adjudicated preregistered campaign or ends with an exact blocker;
- one fresh Theseus currentness lane is imported and bounded, or its smallest
  exact blocker is recorded;
- all 54 chapter-core claims remain at their evidence-earned states unless a
  separate accepted transition changes one;
- the full local validation, Lean, render, projection, browser, format, rights,
  release, and attestation gates agree; and
- the terminal declaration chooses an exact release, blocked, or no-release
  outcome without silently activating another roadmap.

## Canonical execution prompt

> Complete
> `docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md`
> in priority order. Begin by turning the completed 166-path post-v2.3 working
> tree into a reviewed, validated, coherent commit series and observing the
> intended remote build/deploy chain. Preserve v1.0, v2.3.0, the completed
> post-v2.3 no-release record, the exact v2.0 HTML archive, all negative results,
> and all support-state boundaries. Freeze one 54-chapter reader source, then
> disposition EPUB, PDF, and DOCX independently with exact artifacts,
> application/accessibility evidence, rights snapshots, blockers, and release
> records; keep audio deferred. Deepen external anchoring only where a
> passage-reviewed primary comparator changes the prior-art delta, objection,
> boundary, or test. Improve existing owners before proposing a new chapter.
> Reconcile the two exact QCSA refutations into novelty positioning. Repair and
> pass a non-evidentiary structured-output preflight before spending one
> governance-tax flagship campaign, and stop after two materially different
> failed repairs. Import one fresh public-safe Theseus currentness lane rather
> than repeating the existing accelerator-parity record. Close only when every
> priority and milestone has an exact release, blocked, or no-release artifact
> and the registry, Lean, Quarto, browser, reader-format, rights, public-truth,
> and attestation gates agree. Do not require external-human prepublication
> review and do not infer a `v2.4` living-book release from format work alone.

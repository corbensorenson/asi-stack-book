# Living Update Workflow

The book order is manifest-driven.

## Source of Truth

- `book_structure.json` controls front matter, parts, chapter order, chapter IDs, chapter file paths, and appendix order.
- `_quarto.yml` is generated. Do not edit it by hand.
- Chapter filenames use stable slugs, not numbers.
- Quarto generates displayed chapter numbers during render.

## Contributor entry point and current projection previews

`scripts/book.py` wraps the existing registry and its named consumers. The
registry now records 19 current projection owners and their dependency edges.
A plan lists changed inputs, affected outputs, rebuild commands, review
boundaries and registered checks. It also exposes units without declared input
coverage; targeted checks do not replace the complete HTML publication gate.
Every selected check names the projection or input that selected it and shows
its capabilities, side effects, review state, prerequisites and wall-time
ceiling. An unreviewed default remains unknown; a time budget is not an estimate
of how long a check will take.

```bash
python3 scripts/book.py doctor --tier pr
python3 scripts/book.py plan --changed chapters/executable-specifications-and-lean-proof-envelope.qmd
python3 scripts/book.py plan --base HEAD
python3 scripts/book.py check --changed chapters/executable-specifications-and-lean-proof-envelope.qmd
python3 scripts/book.py check --full --tier deep
python3 scripts/book.py projections
python3 scripts/book.py history
python3 scripts/book.py html --site build/project_improvements_site --local --plan
python3 scripts/book.py html --site build/project_improvements_site --local
```

Use `--changed` for a proposed or untracked path; `--base` inspects tracked index
and working-tree changes. A new source can be planned with both its inventory
and note paths; a proof change with its `lean/AsiStackProofs/` path; a chapter
admission with its manifest and chapter paths. Inspect the plan before running
the checks. Review-required entries preserve claim-census, prose, maturity and
synopsis decisions; the entry point does not approve their hashes or execute
their rebuild commands. Historical terminal records are excluded from the
current rebuild graph. `history --select <unit-id>` runs a reviewed read-only
retained-history consumer rather than replacing its receipt.

For common changes, preview the owners with explicit inputs:

```bash
python3 scripts/book.py plan --changed chapters/planning-as-a-control-layer.qmd
python3 scripts/book.py plan --changed sources/source_inventory.json --changed sources/source_notes/new-source.md
python3 scripts/book.py plan --changed lean/AsiStackProofs/StackBoundaries.lean
python3 scripts/book.py plan --changed book_structure.json --changed chapters/new-ai-topic.qmd
```

The `html` command consumes the post-render check interfaces in the canonical
Pages workflow. It checks installed reader integrity, paper routes, product projections, release channels,
public status, static Human view and every strict browser page/viewport pair.
`--plan` previews their budgets and side effects without writing or executing.
Run it after the existing HTML render/install/build pipeline has produced the
site. By default the channel/status checks require a clean tested-commit
record. Explicit `--local` permits a dirty-worktree diagnostic and relaxes only
those two clean-commit requirements. Browser reports/screenshots and bounded
logs are ignored outputs under `build/`; other selected consumers are read-only.
Missing or changed workflow interfaces fail until the adapter is reviewed.
Missing capabilities, check failures and changes to the site or declared
inputs fail the aggregate result. An HTML check neither runs the full source
CI tier nor supplies clean render provenance or publication approval.

`sync_scaffold.py --check`, `sync_paper_library.py --check` and the default
`build_human_reader_current.py` check generated outputs without rewriting them.
The scaffold reports exact changed paths and before/after identities. A normal
scaffold sync preserves timestamps when bytes are unchanged and installs each
changed file through a complete temporary file. This is individual-file
replacement; whole chapter birth and multi-file publication remain separately
governed transactions. The full HTML pipeline remains owned by
`.github/workflows/build-pages-artifact.yml`, including reader installation,
paper routes, canonical status, product/channel checks and the mandatory
browser gate. The command surface does not create another publication owner.

The HTML publication workflow installs the pinned Python publication/schema
dependencies, Node/browser runtime and Quarto. Its source gate checks the book,
public-safe publication surface, source appendices/mappings, outline, current
reader, editorial packets, claim census and executable deployment contract.
It then renders the technical book, reader and paper library and runs the
existing status, product, channel, browser and artifact-integrity checks.
Research runtime installation, the full deep registry and Lean work remain
owned by the scheduled/manual deep-validation and research workflows. HTML
publication does not rerun those campaigns or renew their dated evidence.
This separation prevents an expired research-installer review from blocking
publication of an otherwise checked manuscript. The deploy workflow still
accepts only the successful build's exact commit-bound artifact, rechecks
current-main eligibility, and attests the deployed status.

The public reader installer builds its replacement in a sibling staging
container outside the publishable site, validates the complete payload,
current crosswalk, route map and surrounding-site links, then swaps the
`reader/` directory in one namespace operation. It shares the rendered-site
lock with channel generation. `--check` compares installed bytes and metadata
without writing; the Pages workflow runs that check after installation.
`reader-install-manifest.json` is generated integrity metadata, not approval
or an evidence transition. Unknown added files or damaged receipts block
replacement. A legacy reader is adopted only when all bytes exactly match
the known current payload; otherwise preserve the existing site and build a
fresh output. If directory fsync fails after exchange, the command reports
failure and retains the prior tree plus an uncertainty receipt outside the
site. Process interruption evidence does not establish physical power-loss
behavior or certify all filesystems.

## Sequence-level generated-directory custody checks

`tests/test_generated_directory_stateful.py` checks the actual shared installer
used by product and immutable-archive owners against an independently specified
namespace/ownership model. It generates proposal changes, publication attempts,
read-only checks, source-guard refusal, preparation failure, exceptions after
namespace installation, lost receipts and external file/directory/link edits.
Guided starting states cover absent, receipted, legacy, changed-input,
different-family and foreign-object cases. Fixed regression sequences retain
important joins independently of the generated search.

The model predicts eligibility before calling the producer. It observes node
types and bytes without the producer's inventory/ownership functions, derives
receipt expectations directly from the documented wire format, and checks
both returned and installed receipts with JSON type-sensitive comparisons.
Refusals, checks and no-ops preserve the prior namespace and modification
metadata. An exception after namespace installation must retain a complete new
generation, the displaced prior tree and an uncertainty journal; that outcome
is not reported as successful publication or proven durability.

The broad search uses a deterministic 60-example/50-step budget, with no
example database and no per-example wall-time deadline. Local suite verification
uses a separate 300-second process-group budget; CI job timing remains owned
by its workflows. Targeted sensitivity machines use a 20-example/10-step budget
against deliberately broken ownership and source-guard behavior. They start
from a known custody prefix and shrink the generated continuation. The fixed
prefix is not itself shrunk, and no globally minimal sequence is claimed.
The resulting full continuations are replayed against the real installer.

The first broad search missed the ownership mutant because a synthetic reset
action dominated exploration; that action was removed. A later refactor changed
the deterministic search and it missed the mutant again. Targeted sensitivity
checks and fixed regressions therefore enforce the named boundary independently
of broad search coverage. The initial replay parser also stopped at construction;
it now requires and replays every action through teardown. Those inadequate
observations are retained and excluded from current acceptance. Bounded generated
search does not guarantee all lifecycle joins or schedules are covered. Reader,
channel and bundle owners share lower-level exchange/inventory primitives but
retain their separate consumers and observations.

JSON/SHA-256, the receipt wire specification, the OS, Python and Hypothesis are
shared dependencies. This separates the custody decision and filesystem oracle
from the producer; it does not establish independent institutions, cryptographic
correctness, natural workload performance, concurrent scheduling, hardware
power-loss behavior, source truth or claim support. Family-specific authority,
archive identity and publication decisions remain with their existing owners.

The publication/schema profile pins Hypothesis 6.168.3 and its required
SortedContainers 2.4.0 dependency. The new tests fail rather than skip when the
runtime is absent. The shared CI action is configured to install this profile and run
all infrastructure tests in every tier once its prerequisites pass. For a fresh local stateful-test profile:

```bash
python3.11 -m venv build/stateful-validation-env
build/stateful-validation-env/bin/python -m pip install -r ci/publication_requirements.txt
build/stateful-validation-env/bin/python -m unittest discover -s tests -p test_generated_directory_stateful.py -v
```

The full infrastructure suite additionally requires the documented Node CLI.
The [Hypothesis stateful-testing documentation](https://hypothesis.readthedocs.io/en/latest/stateful.html)
explains the generation/shrinking mechanism; [the pinned release](https://pypi.org/project/hypothesis/6.168.3/)
names its supported Python versions. The observed macOS wheel identities do not
qualify Linux/hosted tiers or renew the separate action/Elan review deadline.

## Chapter revision and source-review dates

Chapter front matter owns `last_updated`: the author-declared date of the last
substantive prose or source-integration revision. Update that one field when
making such a revision. Formatting, generator runs, Git timestamps and renders
do not establish a new revision event. Existing dates remain declarations;
this implementation does not independently reconstruct or verify their history.

The generated Quarto configuration applies `assets/filters/chapter-freshness.lua`
to canonical chapters. It projects **Chapter revision** into the Chapter status
table and replaces legacy literal **Last updated** rows. Older manuscript tables
remain intact as historical presentation inputs; changing their literal date
has no effect on the rendered date. New chapter scaffolds omit that duplicate
row. A newly created draft records its actual UTC scaffold-creation date; this
is not a source review or proof of manuscript quality. Normal syncs keep
existing declarations. An explicit template rewrite preserves the recorded
revision and scoped review events; the author must deliberately update the
front-matter revision when making a substantive change. Non-chapter pages do
not acquire chapter metadata.

A separately conducted source review may be recorded with both of these fields:

```yaml
last_updated: "2026-07-16"
source_reviewed_on: "2026-08-09"
source_review_scope: "Only the two assigned mechanism passages"
```

**Source review** and **Source review scope** appear separately. Without a
recorded review event, the table says **Not recorded in chapter metadata; see
source records**. This does not assert that nobody has reviewed the sources.
Keep review custody, source readiness and evidence reconciliation in their
existing owners; neither date promotes support, proves a claim or establishes
comprehensive/current source coverage. Do not bulk-stamp chapters or substitute
the latest unrelated commit date.

`validate_chapter_dod.py` rejects duplicate front-matter keys, malformed,
non-calendar or future UTC dates and incomplete review/date pairs.
`validate_live_human_view.py` independently reads canonical front matter and
checks the rendered status table: exactly one revision and review value, the
matching scope when declared, and no surviving legacy date row. Contradictory,
duplicate, missing or explicitly hidden values fail. This is static HTML
structure/text validation; browser visibility and accessibility retain their
separate consumer. The Quarto filter also aborts rendering on invalid dates,
incomplete review pairs, a missing/ambiguous status section or multiple metadata
tables. For prose-only status sections it inserts a date table without changing
the original prose. Dates are not
render-time freshness assertions.

## Roadmap Continuity

Current projection checks and historical replay have different owners.
`build_visual_edition_manifest.py --check`, `build_youtube_ledger.py --check`
and `sync_manim_v2_production_ledger.py --check` verify current chapter/media
bindings without producing media or renewing a review. A source change keeps
an old derivative stale until its actual gates are completed. The October 2
reconciliation changed three current chapter hashes and their parent-manifest
bindings only; generation-two stages and every publication state stayed the
same.

The W3 inheritance and P6.9 raw-scaffold builders now default to non-writing
replay against their retained commit inputs. They refuse terminal replacement.
Current W3 regression checks run separately from its original token totals.
Use these commands to inspect history; do not regenerate a closure merely
because today's chapter bytes changed.

- A living-book roadmap may close only in the same transaction that activates
  one exact successor roadmap and reconciles its prose roadmap, machine status,
  schema, validator, outline authority, public pointers, and changelog entry.
- The active successor must contain unfinished work only. Completed roadmaps
  remain immutable execution history and do not reacquire the active marker.
- If no immediate experiment or publication campaign remains, activate a
  maintenance and evidence-renewal successor with explicit source, benchmark,
  dependency, artifact, claim, and release revalidation triggers.
- Zero active successors discards current planning context; multiple active
  successors create ambiguous authority. Both states are invalid at closure.
- Roadmap activation or continuity is planning authority only. It does not
  create evidence, support movement, a release, a deployment, or a rights
  grant.

## Maintained X Article Synopsis

- Treat `docs/x_article_synopsis_contract.md` as the durable contract for the
  public synopsis of at most 9,999 words and exact 5:2 header derivative.
- Generate or refresh the synopsis only from an evidence-reconciled book state.
  The first visible body line must be the canonical live-book URL, and every
  substantive article claim must map to a chapter atom, support state, evidence
  lane, artifact, and book anchor.
- Every public book release must either refresh and validate the synopsis or
  record an exact `not_refreshed` disposition. Claim promotion, narrowing,
  refutation, deprecation, chapter/URL changes, decisive evidence changes, and
  relevant X composer changes also make the derivative stale.
- Re-check X's current official Article guidance and the live composer at each
  refresh. Repository readiness does not authorize publishing, editing,
  unpublishing, or deleting content on X; those external mutations require
  Corben's explicit authorization.
- Preserve the canonical Markdown, claim crosswalk, exact word count, header
  dimensions/digest/provenance/alt text, composer-preview receipt, and
  publication or `ready_not_published` record.

## Add a Part

```bash
python3 scripts/add_part.py --title "Part IV - New Research Track"
python3 scripts/sync_scaffold.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_book.py
```

The sync step creates only a generated starting point for a missing chapter. To regenerate the v0.2 manuscript baseline from the manifest, run:

```bash
python3 scripts/draft_v02_from_manifest.py
```

Use that command intentionally; it rewrites all chapter files from `book_structure.json`.

## Add a Chapter

```bash
python3 scripts/add_chapter.py \
  --part planning-memory-reasoning-execution \
  --title "New AI Topic" \
  --after planning-as-a-control-layer \
  --proposal-output build/chapter-proposals/new-ai-topic.json
```

This command now prepares a **non-admitted proposal** by default. It rejects
invalid/colliding IDs, unknown sources and invalid adjacency; it never writes
`book_structure.json` or a chapter. `--dry-run` remains a compatibility alias
for the same proposal behavior. Printed handoff notes describe the proposed
slot. Optional proposal JSON belongs below ignored `build/`; existing unknown
content and linked paths are preserved by refusal.

Author the complete candidate in a separate patch directory below `build/`.
Source-root and ancestor patches are refused before enumeration. Choose a
separate, fresh stage outside the candidate tree; nested staging is refused.
Include the complete candidate `book_structure.json`, substantive chapter,
adjacent handoff repairs, claim-at-birth ownership, required concept/source
artifacts, the intended Human Reader route and all affected current projections.
Retain every existing manifest owner, order and support state; the candidate
manifest introduces only the proposed insertion. Inspect the dependency plan
for the manifest and chapter paths before preparing the candidate. Do not run
the full-manuscript drafting generator to manufacture admission completeness.

```bash
python3 scripts/prepare_chapter_admission.py \
  --proposal build/chapter-proposals/new-ai-topic.json \
  --candidate build/chapter-candidates/new-ai-topic \
  --stage build/chapter-admission/new-ai-topic-review \
  --validate
```

The staging command copies dirty tracked source and explicitly registered new
files into an independent workspace, with local Git history for retained-byte
checks. Unknown untracked directories and private caches are excluded. The
patch cannot replace validators, tests, schemas, CI, Lean or
skill/prompt owners. It also cannot change experiments, source inventory or
notes, evidence transitions, release/review records, authority/status or
roadmap records, archived custody, or retained reader snapshots. Only the
`editions/reader_manuscript/current/` reader subtree belongs to this admission
payload. Paths containing `raw`, `results`, `attempts` or `protected` are
refused. Update any required source, evidence, authority or checking owner
through its separate workflow before creating a fresh proposal; a chapter
birth is not authority to rewrite those records. A narrow exception allows
`validation/registry.json` to add candidate data files to `required_artifacts`
and update only its matching artifact count. Existing entries and their order,
all validator units, arguments, tiers, contracts and other fields must survive
unchanged. Every newly installed file must be registered; new entries must
refer to ordinary candidate data files. The staged candidate is bound to inspected source/patch bytes,
and registered birth checks run with bounded logs and process groups. `--full`
runs the complete deep tier, including PR checks. Omitting both flags only
prepares an unvalidated workspace. Source or patch drift, incomplete runner
reports and validators that rewrite staged source cannot produce acceptance.

These three staging modes remain **not admitted**. `admission.json` distinguishes
prepared, rejected and interrupted candidates; preparation preserves canonical
source and recognizable diagnostics. Choose a fresh stage for another attempt;
the command never deletes previous diagnostics. Passing checks cannot substitute
for the authored semantic and reader-route decisions.

The explicit `--install` mode runs the entire deep gate itself, then installs
only the inspected candidate patch. It does not adopt a previously saved stage
or receipt. It holds an exclusive lease on the existing repository directory
through preparation, validation and installation, without changing Git HEAD
or the index. Source bytes, modes, HEAD/index identity and full-report identity
are checked before installation. The manifest is replaced last, after the
other birth files. Changed existing objects are retained in the stage; new
targets use exclusive installation rather than overwriting a later object.

```bash
python3 scripts/prepare_chapter_admission.py \
  --proposal build/chapter-proposals/new-ai-topic.json \
  --candidate build/chapter-candidates/new-ai-topic \
  --stage build/chapter-admission/new-ai-topic-install \
  --install
```

This is a recoverable multi-file transaction. Before its first canonical write,
it creates `build/chapter-admission-active.json`. Cooperating book, registry,
scaffold, product and browser-report commands refuse a pending transaction.
CI holds a shared directory lease through each Quarto render. For manual
rendering, use `python3 scripts/admission_guard.py --run quarto render`; the
generated Quarto pre-render check detects pending admission at startup, but
does not itself hold a lease throughout an unwrapped manual render.

The command wrapper uses an independent supervisor. It inherits the directory
lease, watches a private cancellation pipe, and stops the owned command group
before releasing the lease, including after wrapper death or leader exit.
Commands do not inherit the lease/control descriptors. If cleanup cannot be
confirmed, the supervisor retains the lease and reports the problem; inspect
that owned process group before further canonical work. The lease is not a
security sandbox: a command escaping its process group, killing the supervisor
itself, manual source edits and physical power loss remain outside this check.

An interrupted installation keeps its marker, journal, payloads and displaced
objects. Inspect it with `python3 scripts/recover_chapter_admission.py`;
explicitly restore with `python3 scripts/recover_chapter_admission.py --rollback`.
Rollback preflights every target before restoring any, restores the original
manifest first and refuses to overwrite later edits to installed objects.
It preserves concurrent edits to displaced original objects. Unknown/nonempty
directories and unrecognized control objects are retained for inspection.
Do not delete the marker or force-copy files around the recovery mechanism.

Twenty authored transaction/lease controls pass locally, including an abrupt
process exit after the manifest swap. Their full-runner observations are
synthetic; an actual incomplete candidate also rejected without admission.
A real valid birth through all actual consumers, Linux behavior and physical
power-loss qualification remain unobserved. D02 stays open. The directory lease
coordinates participating commands; manual editors do not acquire it, and
byte/object checks detect observed changes rather than preventing all outside
writes. Installation grants no publication or support-state promotion.

## Reorder, Merge, or Remove Chapters

Edit `book_structure.json` only.

- Reorder: move the chapter object inside the desired part.
- Move to another part: move the chapter object between part arrays.
- Merge: move useful source IDs and claims into the surviving chapter, run `python3 scripts/chapter_adjacency_report.py --if-removing <chapter-id>` to identify the predecessor Handoff repair, then remove the obsolete chapter object.
- Remove: remove the chapter object, then decide whether to keep or delete the old `.qmd` file as archival material.

After edits:

```bash
python3 scripts/chapter_adjacency_report.py --chapter <changed-chapter-id>
python3 scripts/sync_scaffold.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_chapter_handoffs.py
python3 scripts/validate_book.py
quarto render --to html
```

## Bring in a New AI Paper

1. Decide the source storage and public-safety policy before adding text:
   - `repo_public_note_only` for public-safe notes without raw source publication.
   - `repo_public_source_allowed` only when publication is explicitly allowed.
   - `connector_only`, `local_private_cache`, `external_url_only`, or `blocked` when raw text should not enter the public repo.
2. Add or update the paper metadata in `sources/source_inventory.json` with a stable source ID.
3. Create or update a `research_backlog_record` when the source changes chapter boundaries, evidence state, proof/test backlog, or publication risk.
4. Use the `new_paper_triage_scenario` decision surface before prose changes:
   - update an existing chapter when the source strengthens an existing boundary,
   - propose a new chapter only when it owns a distinct interface, invariant, artifact type, or failure mode,
   - route to appendix/backlog when it is useful but not chapter-owning,
   - defer unread external literature,
   - reject duplicate or superseded variants.
5. Create `sources/source_notes/<source-id>.md` only after actually reading the source or a permitted connector/export.
6. Update `book_structure.json` only after the chapter decision is clear:
   - add the source ID to an existing chapter's `source_ids`, or
   - prepare a non-admitted chapter proposal with `scripts/add_chapter.py`, then
     author and check its complete candidate through the staged workflow above.
7. Record required pre-drafting work, chapter-decision refs, deduplication state, evidence-transition preconditions, promotion blockers, and non-claims before strengthening chapter prose.
8. Update Appendix C only through `scripts/sync_scaffold.py` unless a claim's support state changes after source ingestion, proof, or testing.
9. Run the relevant checks:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_book.py
quarto render --to html
```

10. Update `appendices/F_changelog.qmd`.

Do not mark claims as source-derived or test-backed until the source has actually been ingested, mapped to the claim, passage-reviewed or accepted through an evidence transition, and any claimed test has actually run.

### Publish a Corben paper in the live library

Publishing an author manuscript is a separate decision from mining it. Add the
source ID to `papers/paper_library.json` only after explicit publication
authority, exact source custody, a SHA-256 receipt, and a source note exist.
Then run:

```bash
python3 scripts/sync_paper_library.py
python3 scripts/sync_scaffold.py
python3 scripts/validate_paper_library.py
quarto render --to html
quarto render papers --to html
python3 scripts/validate_paper_library.py --site _site
```

The second Quarto command builds the unnumbered sibling site at
`_site/papers/`. Keeping it outside the main Quarto book prevents author
manuscripts from becoming Chapters 86 onward or changing the canonical
85-chapter count. Each reader page must retain the exact source download,
digest, source-note boundary, current chapter lineage, and rights statement.
The rendered-site check rejects broken local links, altered exact-source bytes,
source-format `.qmd` leaks, missing Appendix G routes, and accidental numbering
of manuscripts as Chapters 86 onward.
Publishing an original manuscript does not validate its claims or move a book
support state.

## Bring in Conversation-Mined Context

1. Move the raw packet under `sources/inbox/` so it remains local-only unless explicitly approved for publication.
2. Read provenance and limitations first.
3. Extract only public-safe author intent, terminology, architecture lineage, deduplication decisions, and recovery tasks.
4. Update `docs/book_outline.md`, `book_structure.json`, appendices, or docs only when the mined context changes the future writing plan.
5. Do not quote private conversation wording verbatim or mark claims as source-derived from conversation context.
6. Update the source inventory, outline, roadmap, or existing ingestion ledger that owns the result, then update the changelog. Create a standalone public-safe ingestion report only when a validator, evidence transition, or governance decision consumes it.

## Prepare a Major-Version Reader Edition

The October 2, 2026 maintenance audit found the retained audio-script candidate
stale: it contains 89 script files where the current generator would produce
94, and its companion table/diagram/code totals no longer match. The two
release-only audio gates correctly reject that candidate. This is an unopened
derivative-preparation blocker, not a current HTML failure or permission to
regenerate narration. At an approved major-version freeze, rebuild from that
exact frozen content and perform the existing script/treatment review before
claiming currency or approval.

This workflow is dormant during ordinary manuscript work. Do not render EPUB,
PDF, DOCX, e-reader, or audio derivatives for minor content changes or routine
validation. Open it only after the active roadmap records an approved
major-version content freeze; until then, use the live HTML/Human view and spend
work on manuscript quality, sources, proofs, and executable evidence.

The live book remains the canonical source. Reader, research, and audio editions are derived from a tagged live-book state.

1. Confirm the live-book gate passes:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/validate_book.py
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

2. Check the reader-edition derivation:

```bash
python3 scripts/build_reader_edition.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_spine.py --check
```

3. Generate the local reader manuscript source:

```bash
python3 scripts/build_reader_edition.py
```

Review `build/reader_edition/READER_RELEASE_CHECKLIST.md`, `build/reader_edition/companion_notes.md`, and `build/reader_edition/reader_delta_report.md` alongside the generated manuscript. The delta report includes a zero-active-operation note when no overlays exist, or operation digests and before/after excerpts when active overlays exist; treat those excerpts as evidence of derivation, not as editable patches.

If the reader manuscript needs human-edition prose that should not change the AI/research source, edit the tracked overlay files under `editions/reader_overlays/` and regenerate. Do not preserve changes by editing `build/reader_edition/` or by hand-patching `reader_delta_report.md`; the report is generated review evidence for the overlay and strip transformations.

4. Attempt selected local reader renders and write a render report:

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
```

Use `--include-pdf` or add `pdf` to `--formats` only when local PDF dependencies are available.

5. Review the generated manuscript for continuity before publishing EPUB, DOCX, PDF, or HTML from `build/reader_edition/`.
6. Record only the formats that actually render successfully.
7. For audio, create and review a narration script from the reader edition before producing MP3, M4B, or audio-embedded EPUB artifacts.

Do not report an ebook, PDF, DOCX, or audiobook as complete just because the profile lists it as a target.

## Prepare a Major-Version Audio Script

Audio is downstream of the reader edition, not the live book directly.

1. Confirm the reader release candidate was generated and reviewed for human continuity.
2. Generate or check the narration-script workspace:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
python3 scripts/validate_reader_audio_script_probe_manifest.py
```

3. Confirm the generated `audio_manifest.json` reports a passing implementation-horizon script status, meaning every manifest chapter script keeps both `Minimum Viable Implementation` and `Mature Research Target`.
4. Review `build/audio_script/AUDIO_RELEASE_CHECKLIST.md`, `build/audio_script/companion_notes.md`, and `build/audio_script/chapter_markers.md`, then replace generated narration notes for tables, diagrams, images, code, and schemas with spoken summaries or companion-note references.
5. Keep the pronunciation glossary current.
6. Produce MP3, M4B, or audio-embedded EPUB only after the exact script is reviewed.
7. Add an `edition_release` record under `release_records/` that lists exactly which audio artifacts were produced and checked.

The generated audio script and the tracked audio-script probe are not
audiobooks and do not imply that any audio artifact exists.

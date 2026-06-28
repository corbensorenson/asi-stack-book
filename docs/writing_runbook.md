# Writing Runbook

This is the operating runbook for turning the scaffold into the full living book.

## Start Every Major Writing Run

1. Read `prompts/MASTER_CODEX_PROMPT.md`.
2. Read `skills/asi-stack-book/SKILL.md`.
3. Read `book_structure.json`.
4. Read `docs/book_outline.md`, including the part-level and chapter-level source loading queues.
5. Read `sources/cache/cache_manifest.json` and `docs/source_readiness_report.md`.
6. Read the chapter files in scope.
7. Read source notes and raw cache files only for the sources in scope.
8. Read `docs/prewriting_readiness.md` and `docs/external_literature_queue.md` when starting a full-book or part-level writing run.

## Source Hierarchy

Use source material in this order:

1. Local raw source cache under `sources/raw/` when available.
2. Google Drive connector export/fetch when the local cache is missing or stale.
3. `sources/source_inventory.json` metadata when source text is unavailable.
4. Handoff notes only as planning/context, not as source-derived evidence.
5. Conversation-mined packets only as author intent, architecture lineage, terminology, and recovery cues, not as external evidence or quotable source text.

Use the source queue in `docs/book_outline.md` to decide what is in scope:

- Primary sources are loaded first for chapter claims and mechanisms.
- Supporting sources are loaded after primary sources for synthesis, variants, failure modes, and cross-layer context.
- Variant sources are used to compare versions or recover missing details.
- Connector or recovery sources must be loaded through Google Drive or kept as explicit blockers before source-derived claims.

Do not mark a claim as `source-derived` unless the actual source text was read, the claim-source mapping is recorded, and passage review or an accepted evidence transition supports the narrower move. Do not publish private conversation wording verbatim unless the user explicitly approves that exact text.

## Chapter Drafting Loop

For each chapter:

1. Read assigned source text or source notes.
2. Extract source-backed mechanisms, claims, failure modes, and evidence.
3. Decide which claims remain design hypotheses.
4. Draft the chapter as one architecture layer, not a pasted anthology.
5. Update the chapter source crosswalk.
6. Update Appendix C if claim text, claim label, or support state changes.
7. Update glossary terms introduced by the chapter.
8. Add planned proof/code hooks when a mechanism can be formalized or tested.
9. Update `appendices/F_changelog.qmd`.
10. Run validation and render.

## Three-Audience Writing Rule

Write every chapter for three audiences without maintaining three separate books:

- AIs and writing agents use the live-only scaffolding: status tables, drafting guardrails, source queues, claim/evidence states, proof hooks, schemas, and test plans.
- Human researchers use the complete live book, including matrices, source crosswalks, residuals, and appendices.
- Interested human readers use the live-site `Human view` and generated reader/audio editions derived from the same source after live-only scaffolding is stripped.

The reader-facing spine is the prose outside the headings listed in `editions/release_profiles.json` under `reader_release.strip_headings`. Do not put a caveat that changes the meaning of a claim only inside `Drafting guardrail`, `Source crosswalk`, `Codex test plan`, `Formalization hooks`, or `Claim-source mapping status`, because those sections are removed from reader and audio editions. Keep essential uncertainty in the main prose.

Every manifest chapter must contain exactly one `.asi-human-only` `Human Reading Path` bridge after `Drafting guardrail` and before `Problem`. The source heading is a machine-checkable marker; live Human view and generated reader editions present the bridge as unheaded prose. The bridge gives interested readers a concise route into the chapter while leaving support-state limits in the ordinary prose, and it must contain at least 170 words of chapter-specific orientation excluding the source-only heading. Its opening sentence must contain at least 11 words and its closing sentence must contain at least 11 words so the bridge begins and ends as book prose rather than clipped slogans; no more than three of its final five sentences should be short taglines. Write it as direct book prose, not meta-reader scaffolding: avoid phrases such as `For a human reader`, `For the reader`, `This chapter`, `the book`, `this book`, `Part I`, `Part II`, `Part III`, `Part IV`, `previous chapters`, `previous layers`, `closing move`, `The reader should`, `The human point`, `The human test`, `The human caveat`, repeated transition formulas such as `The next question is`, repeated bridge formulas such as `The useful`, `The practical`, `The point is`, and `useful only when`, or any self-referential `chapter` phrasing inside the bridge body. Use `.asi-ai-only` or `.asi-live-only` fenced divs only for scaffold material that should disappear from Human view and reader releases. Reader generation unwraps human-only blocks and removes AI-only blocks; neither block type should be used to hide support-state limits from any audience.

Major-version reader and audio work stays downstream of the live book. Generated reader workspaces include `READER_RELEASE_CHECKLIST.md`, `companion_notes.md`, and `reader_delta_report.md`; the live Human view consumes the tracked `assets/reader-overlays.html` payload generated from the same overlay manifest; generated audio workspaces include `AUDIO_RELEASE_CHECKLIST.md`, `companion_notes.md`, `chapter_markers.md`, and `pronunciation_glossary.md`. Use those files to review continuity, reader overlay deltas, e-reader behavior, spoken treatment of diagrams/tables/code, and release-record residuals before claiming EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts. Reader-only prose changes belong in tracked overlay operations or canonical chapter source, then regeneration; generated reader manuscripts and generated delta reports are not editable source.

When writing chapters, assume the reader spine may become a relaxed human-consumption bundle: reader HTML, EPUB, PDF, DOCX, optional e-reader conversions, and a later audio script. Dense live-only machinery can stay in the live book, but the main prose should carry enough transitions, caveats, diagram explanations, examples, and implementation-horizon sections to survive stripping and narration.

When revising diagrams, add a concise diagram walkthrough note after the primary Mermaid block. The note should explain how to read the boundary, loop, state machine, or evidence flow without claiming that the diagram itself proves implementation, benchmark, safety, or runtime behavior. Use a chapter-specific bold label such as `How to read the route ledger:` rather than repeating one generic label across the book. Every chapter is under this validator ratchet.

When revising chapter endings, add or preserve `## Handoff` sections. A good handoff should come after `Summary`, name the next manifest chapter title exactly, avoid numbered chapter references, and explain the architectural reason the following boundary follows in chapter-specific language rather than formulas such as `the next boundary`, `the next move`, `the next question`, `the handoff is`, or `the handoff moves`. `python3 scripts/validate_chapter_handoffs.py` enforces this for all manifest chapters; the final chapter should close the book-level arc instead of naming a later chapter.

Problem, insufficiency, and summary sections should speak in direct systems language rather than describing "this chapter" as an object. Use layer, boundary, record, contract, evaluator, runtime, route, field, or artifact names so the human-readable spine reads like a book, not scaffold commentary.

Run `python3 scripts/validate_human_reading_paths.py`, `python3 scripts/validate_reader_evidence_boundaries.py --check`, `python3 scripts/sync_reader_overlay_asset.py --check`, `python3 scripts/validate_reader_overlays.py --check`, and `python3 scripts/validate_reader_spine.py --check` before treating a generated reader manuscript as a major-version candidate. The checks verify that each source chapter has one Human Reading Path bridge, that generated reader chapters keep it as ordinary prose after the manifest title, that generated reader Core Claim sections strip raw live core-claim markers and repeated support boilerplate while preserving claim text and an inline support boundary, that semantic reader overlays apply cleanly, update the live Human-view payload, and produce a delta report, that the human-readable layer survives stripping, that required chapter sections remain, that each major reader-facing section clears its word-count and substantial-prose-paragraph floor, that live-only terms do not leak into chapter prose, that generated reader chapters avoid self-referential meta phrases such as `this chapter` and `the chapter`, that generated reader paragraphs do not open with the repeated compact evidence-boundary phrase, and that every generated reader chapter preserves one chapter-specific Handoff after `Summary` with manifest-order continuity. After rendering the live site, run `python3 scripts/validate_live_human_view.py` to check that every rendered book page carries the Human view toggle, embedded overlay payload, and headings/block classes needed for Human view filtering. When browser automation is available, also run `node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports` so every manifest chapter proves URL mode, local persistence, live-section hiding, TOC hiding, raw core-claim marker and support-boilerplate hiding/restoration, bridge visibility, rendered Mermaid visibility, reading-mode control visibility, page-level horizontal overflow, overlay payload availability, and AI-view restoration across desktop and mobile viewports in an actual browser.

When a tagged major version is actually being packaged, follow `docs/major_version_release_runbook.md`. It is the release sequence for live/research, reader, ebook/document, and audio artifacts.

## Per-Chapter Definition of Done

Each chapter must maintain these sections:

- Chapter status
- Drafting guardrail
- Problem
- Why existing approaches are insufficient
- Core Claim
- Mechanism
- Interfaces
- Invariants
- Failure modes
- Minimum Viable Implementation
- Beyond the State of the Art
- Codex test plan
- Source crosswalk
- Summary

The scaffold-level contract is enforced by `python3 scripts/validate_chapter_dod.py`, including guards against missing or duplicated DoD headings, out-of-order chapter sections, generic mature-endpoint boilerplate, generic evidence-gate caveats, generated summary boilerplate, repeated forward-transition formulas such as `The next chapter`, mechanical backward handoffs such as `The previous chapter` in problem openings, summary self-reference such as `This chapter` or `The chapter`, stale run-language such as `This pass`, summary crosswalk references, source-crosswalk boilerplate, scaffold placeholders, and too-thin `Problem`, `Why existing approaches are insufficient`, `Mechanism`, `Interfaces`, `Invariants`, `Failure modes`, `Minimum Viable Implementation`, `Beyond the State of the Art`, or `Summary` sections. `scripts/validate_repeated_prose.py` also rejects generic problem and insufficiency formulas such as `The book needs a place`, `The book needs`, `The stack needs`, `The ASI Stack needs`, `The problem is`, `The insufficiency is`, `The stack should`, `The record should`, and `The response is`, repeated mature-endpoint formulas such as `At maturity,`, `The mature version is`, `The mature version of`, `The mature product surface would include:`, `The final product surface would include:`, `would expose:`, `The operational contract is`, `Support should stay at`, `At that mature boundary`, `In that final product`, `Failure closure:`, `detect and route failure modes such as`, `This is a target architecture, not a current-result claim`, and `It remains beyond the chapter's present support state`, repeated MVI formulas such as `The next useful implementation step is`, `The next useful fixture set is`, `The next useful fixture is`, `Passing the fixture`, `Passing schema validation only`, `That would`, `without claiming`, `does not prove`, `do not prove`, `proves only`, `prove only`, `cannot prove`, `The accompanying Lean module is`, `The Lean predicates do not`, `These proofs do not implement`, and `The Lean coverage stays at`, generic interface formulae such as `The interface is the`, `The interface is a`, `The interface is an`, `The public schema now records`, `The interface should`, `The interface should also record`, `The interface should distinguish`, `The interface should expose`, `The interface should carry`, `The interface should also`, and `The contract should also`, generic mechanism evidence-boundary formulae such as `None of those passages show` and `The reviewed passages sharpen the`, and generic summary formulae such as `The evidence map is narrower now`. A complete manuscript chapter must also keep source-derived claims mapped to source notes, keep support states honest, and avoid reporting tests, proofs, benchmarks, or external literature unless those artifacts exist. `Problem` should name the stakes, boundary, and failure pressure that make the chapter necessary in at least 130 words; `Why existing approaches are insufficient` should explain the concrete failure of current practice in at least 130 words; `Mechanism` should describe the actual architecture of the layer in at least 300 words; `Interfaces` should name the handoff record, consumers, refusal path, and evidence boundary; `Invariants` should name concrete preserved boundaries in at least 110 words; `Failure modes` should name concrete ways the chapter can fail in at least 110 words; `Minimum Viable Implementation` should name the smallest honest slice, fixture or trace path, and a non-promotion boundary in at least 125 words; `Summary` should close the mechanism in at least 130 words without becoming a live-scaffold recap; `Beyond the State of the Art` should name the chapter-specific mature product-level end state in at least 200 words without implying that the end state has already been implemented.

The repeated-prose guard also rejects `The support state remains argument` and `The passage-reviewed mappings support discussion` as support-boundary formulas; write the evidence limit in chapter-specific language instead. It also rejects generic practical-purpose openers such as `The practical point is`, `The practical test is`, `The practical rule is`, `The practical purpose is`, and `The practical problem is`; name the actual field, right, substrate, verification limit, or evaluation pressure directly. Avoid `The stack should`, `The record should`, `The response is`, and `The minimum should` as reader-visible obligation formulas; name the actual layer, record, gate, artifact, ledger, receipt, packet, card, checklist, evaluation, mitigation, protocol, or accounting surface that carries the requirement. For invariant and failure-mode sections, name the boundary or failure directly in the chapter's own vocabulary rather than opening with generic formulas such as `Another invariant is`, `A second invariant is`, `The strongest invariant is`, `The key invariant is`, `The subtle failure is`, `The subtle failure mode is`, or `Another failure is`.

`book_structure.json` carries both `minimal_implementation` and `beyond_state_of_art` for every chapter. Treat those fields as the source-of-truth implementation endpoints when adding, moving, merging, or redrafting chapters. The minimum field answers, "what can we honestly build first?" The beyond field answers, "what does the final product-level surface look like once this idea is fully operational, governed, evidence-bearing, failure-aware, and composed with the rest of the ASI stack?" `scripts/sync_scaffold.py` publishes those fields into Appendix K, `Implementation Horizons`, so full-book writing goals can see the first-build slice and mature endpoint for every chapter in one generated matrix. New chapters should not pass validation until both fields are specific enough to guide writing, proofs, tests, and release-triage work.

## Claim Labels

Claim labels describe what kind of statement is being made. Support states describe what currently supports it.

| Label | Use |
|---|---|
| `Demonstrated` | A recorded artifact, derivation, implementation, or source-backed example demonstrates the claim in scope. |
| `Measured` | The claim reports a recorded measurement or benchmark result. |
| `Mechanized` | The claim is expressed as runnable code, an executable schema, or a formal proof target. |
| `Hypothesized` | The claim is testable but still needs evidence. |
| `Design rationale` | The claim is an architectural choice supported by reasoning and constraints. |
| `Speculative` | The claim is exploratory and cannot support deployment guarantees. |

## Evidence Movement Rules

| Movement | Required basis |
|---|---|
| `argument` -> `source-derived` | Actual source text read, mapped to the claim, passage-reviewed or accepted through an evidence transition, and bounded by recorded limitations. |
| `source-derived` -> `prototype-backed` | Prototype or code inspected. |
| `prototype-backed` -> `synthetic-test-backed` | Test implemented and run on synthetic cases. |
| `synthetic-test-backed` -> `empirical-test-backed` | Realistic external or field-like test run. |
| any state -> `unsupported` | Source missing, contradiction found, or claim overreaches evidence. |
| any state -> `deprecated` chapter/status | Claim or chapter superseded, failed, or merged. |
| any state -> `refuted` | Later evidence or tests contradict the claim; preserve the negative result. |

Promoted evidence records should include the relevant evidence bundle fields: source hash, code revision, environment manifest, baseline, test command, metrics, raw logs, negative results, ablations, failure reproduction, artifacts, provenance, conclusion, limitations, and release notes.

## End Every Major Writing Run

Run:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/build_reader_edition.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/build_audio_script.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
```

For release or PDF checks:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```

For a major-version reader release candidate:

```bash
python3 scripts/validate_release_profiles.py
python3 scripts/build_reader_edition.py --check
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/sync_reader_overlay_asset.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/build_reader_edition.py
```

For an audio-script candidate after the reader manuscript is reviewed:

```bash
python3 scripts/build_audio_script.py --check
python3 scripts/build_audio_script.py
```

These commands generate source workspaces only. Do not claim EPUB, PDF, DOCX, AZW3, MOBI, MP3, M4B, or audio-embedded EPUB artifacts until the specific render, conversion, or audio-generation command succeeds and a release record under `release_records/` states the result.

The audio-script check must keep both `Minimum Viable Implementation` and `Beyond the State of the Art` in every chapter script; those sections explain the smallest honest starting slice and the mature target product for listeners as well as readers.

Then commit and push only tracked source, metadata, notes, scripts, and public-safe artifacts.

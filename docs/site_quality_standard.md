# Site Quality Standard

The public GitHub Pages site should be treated as a technical product, not just rendered markdown.

## Reader Experience

- The landing page must communicate title, thesis, current maturity, and reading path within the first screen.
- Parts and chapters must be easy to scan.
- Appendices must be visible as the evidence and governance layer of the book.
- Support states must be explained before readers encounter major claims.
- The site must not imply source ingestion or testing is complete when it is not.
- The top-of-page reading-mode switch must render on every book page, default to `AI view`, persist the reader's selected mode locally, support shareable `?view=human` and `?view=ai` URLs, expose an assistive status update for screen readers, remain visible and unclipped on desktop and mobile viewports, avoid page-level horizontal overflow, and provide `Human view` by hiding the reader-release live-only chapter headings, their page-TOC entries, internal Human Reading Path TOC entries, raw bracketed core-claim markers, repeated support-state boilerplate, and visible section numbers that would otherwise expose gaps from stripped scaffold sections without claiming a reviewed reader artifact exists. Static post-render validation must check the rendered hooks, and browser smoke validation should exercise representative rendered pages by default and every manifest chapter across desktop and mobile viewports with `--all-chapters --all-viewports` when Playwright/Chrome is available.
- Every manifest chapter must include exactly one `.asi-human-only` `Human Reading Path` bridge after `Drafting guardrail` and before `Problem`, giving interested readers a substantive route into the chapter without moving evidence caveats out of the reader spine. The source heading is a machine-checkable marker; live Human view and generated reader editions present the bridge as unheaded prose. The bridge should read as direct book prose rather than saying what "this chapter," "the book," or "the reader" should do, should avoid self-referential `chapter` phrasing and part/chapter sequencing scaffolds such as `Part I`, `Part II`, `previous chapters`, or `closing move` inside the bridge body, should contain at least 170 words of chapter-specific orientation before the technical machinery resumes, should open with a complete sentence of at least 11 words, should close with a complete sentence of at least 11 words, should not end with four or more clipped short sentences in its final five sentences, and should avoid repeated bridge formulas such as `The useful`, `The practical`, `The point is`, and `useful only when`, excluding the source-only heading.
- Optional `.asi-human-only`, `.asi-ai-only`, and `.asi-live-only` blocks must follow the release profile policy: human-only prose is retained for reader editions, AI/live-only material is hidden or stripped, and meaning-critical caveats stay in the ordinary reader spine.
- Generated reader chapters must strip each live chapter's raw core-claim marker and repeated support boilerplate while preserving the claim text and a compact plain-language support-state boundary in the Core Claim section, so the Human view and reader releases cannot become more confident than the live evidence state after scaffold stripping. The generated reader spine should also read as direct manuscript prose: `scripts/validate_reader_spine.py --check` rejects live-only terms, internal-tool phrasing such as `Codex workflow`, scaffold labels such as `source crosswalk`, hyphenated source-review jargon such as `source-note`, self-referential reader meta-phrases such as `this chapter` and `the chapter`, missing or generic reader Handoff continuity, and sections that fall below reader-facing word/prose-paragraph floors after stripping.
- Chapter summaries should close with substantive reader-facing synthesis rather than title restatement or scaffold prose. `scripts/validate_chapter_dod.py` requires every manifest chapter summary to contain at least 130 words and continues to reject self-referential chapter phrasing, mechanical section handoffs, and live crosswalk references. `scripts/validate_repeated_prose.py` rejects generic summary formulas such as `The evidence map is narrower now`.
- Chapter `Problem` sections should give both humans and research agents a substantive entry point by naming the stakes, boundary, and failure pressure for the mechanism. `scripts/validate_chapter_dod.py` requires at least 130 words in every manifest chapter `Problem` section, and `scripts/validate_repeated_prose.py` rejects generic meta-openers such as `The book needs a place`.
- Chapter `Why existing approaches are insufficient` sections should make the insufficiency concrete enough for human readers to understand why the proposed layer is necessary rather than decorative. `scripts/validate_chapter_dod.py` requires at least 130 words in every manifest chapter insufficiency section.
- Insufficiency sections should argue from the architecture rather than from manuscript scaffolding. `scripts/validate_chapter_dod.py` rejects self-referential `this chapter` / `the chapter` phrasing there, matching the existing guard on `Problem` and `Summary`.
- Chapter `Mechanism` sections should carry the real architecture of the layer, not just a short list or diagram placeholder. `scripts/validate_chapter_dod.py` requires at least 300 words in every manifest chapter mechanism section, and `scripts/validate_repeated_prose.py` rejects generic evidence-boundary formulas such as `None of those passages show` and `The reviewed passages sharpen the`.
- Chapter `Interfaces` sections should be usable as systems handoff contracts, naming the record surface, consumers, refusal path, and evidence boundary where relevant. `scripts/validate_chapter_dod.py` requires at least 130 words in every manifest chapter `Interfaces` section, and `scripts/validate_repeated_prose.py` rejects generic interface phrasing such as `The interface is the`, `The interface is a`, `The interface is an`, `The public schema now records`, and `The interface should also record`.
- Chapter `Invariants` and `Failure modes` sections should be substantial enough to name the preserved boundary and the concrete ways the mechanism can fail. `scripts/validate_chapter_dod.py` requires at least 110 words in both `Invariants` and `Failure modes` for every manifest chapter.
- Chapter `Minimum Viable Implementation` sections should identify the smallest honest artifact, fixture, trace, schema, or validation slice that can begin the idea without implying capability, safety, benchmark, or runtime success. `scripts/validate_chapter_dod.py` requires at least 125 words in every manifest chapter MVI section, and `scripts/validate_repeated_prose.py` rejects known MVI formulas such as `The next useful implementation step is`, `The next useful fixture set is`, `The next useful fixture is`, `Passing the fixture`, `Passing schema validation only`, `That would`, `without claiming`, `does not prove`, `do not prove`, `proves only`, `prove only`, `cannot prove`, `The accompanying Lean module is`, `The Lean predicates do not`, `These proofs do not implement`, and `The Lean coverage stays at`.
- Chapter `Beyond the State of the Art` sections should describe the mature product-level endpoint without implying that it already exists. `scripts/validate_chapter_dod.py` requires at least 200 words in every manifest chapter mature-endpoint section, and `scripts/validate_repeated_prose.py` rejects known mature-endpoint formulas such as `At maturity,`, `The mature version is`, `The mature version of`, `The mature product surface would include:`, `The final product surface would include:`, `would expose:`, `The operational contract is`, `Support should stay at`, `At that mature boundary`, `In that final product`, `Failure closure:`, `detect and route failure modes such as`, `This is a target architecture, not a current-result claim`, and `It remains beyond the chapter's present support state`.
- Ratcheted chapters should close with a reader-facing `Handoff` section after `Summary` that names the next manifest chapter title and explains why the following boundary follows from the current one without using numbered chapter references or generic transition formulas such as `the next boundary`, `the next move`, `the next question`, `the handoff is`, or `the handoff moves`. `scripts/validate_chapter_handoffs.py` enforces this for all manifest source chapters, and `scripts/validate_reader_spine.py --check` enforces the same continuity after reader-edition stripping; the final chapter closes the book-level arc instead of naming a later chapter.
- After manifest structural edits, `scripts/chapter_adjacency_report.py` should be used to identify the predecessor/current Handoff repairs so chapter insertions, removals, merges, and moves do not require hand-renumbering or full-book transition hunting.

## Visual Standards

- Use restrained technical styling.
- Prefer high contrast, readable line length, and stable spacing.
- Avoid decorative visuals that do not explain the architecture.
- Diagrams should clarify interfaces, loops, and evidence flow, with enough named states, labeled transitions, and concrete handoffs to explain a mechanism rather than merely satisfy coverage. Chapter Mermaid diagrams must clear the substantive visual floor enforced by `scripts/validate_visual_coverage.py`, including at least 12 non-comment lines, and the real-browser Human-view gate should confirm that each rendered chapter exposes at least one visible nonblank Mermaid SVG in both Human and AI projections.
- Every chapter must include a `Diagram reading note` near its primary Mermaid diagram so Human view, reader editions, and future audio treatment have a concise prose walkthrough for the visual boundary being shown.
- Tables should remain readable on narrow screens and should not widen the page; wide generated tables may scroll inside the content column.

## Release Standards

Before a public update:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_chapter_dod.py
python3 scripts/validate_chapter_handoffs.py
python3 scripts/validate_book.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_v1_status_snapshot.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_evidence_boundaries.py --check
python3 scripts/validate_reader_spine.py --check
python3 scripts/build_reader_edition.py --check
python3 scripts/render_reader_formats.py --check
python3 scripts/build_audio_script.py --check
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_proof_artifact_audit.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_repeated_prose.py
(cd lean && lake build)
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

For full local release:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```

Check:

- home page loads,
- one representative chapter loads,
- the representative chapter can switch between `AI view` and `Human view`,
- `?view=human` opens the representative chapter in Human view,
- the all-chapter, all-viewport browser smoke validator passes or explicitly reports that browser automation is unavailable,
- Appendix A loads,
- Appendix C loads,
- no raw private source files are tracked,
- GitHub Pages workflow succeeds.

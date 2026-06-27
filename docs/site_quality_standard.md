# Site Quality Standard

The public GitHub Pages site should be treated as a technical product, not just rendered markdown.

## Reader Experience

- The landing page must communicate title, thesis, current maturity, and reading path within the first screen.
- Parts and chapters must be easy to scan.
- Appendices must be visible as the evidence and governance layer of the book.
- Support states must be explained before readers encounter major claims.
- The site must not imply source ingestion or testing is complete when it is not.
- The top-of-page reading-mode switch must default to `AI view`, persist the reader's selected mode locally, support shareable `?view=human` and `?view=ai` URLs, expose an assistive status update for screen readers, and provide `Human view` by hiding the reader-release live-only chapter headings, their page-TOC entries, internal Human Reading Path TOC entries, and visible section numbers that would otherwise expose gaps from stripped scaffold sections without claiming a reviewed reader artifact exists.
- Every manifest chapter must include exactly one `.asi-human-only` `Human Reading Path` bridge after `Drafting guardrail` and before `Problem`, giving interested readers a substantive route into the chapter without moving evidence caveats out of the reader spine. The source heading is a machine-checkable marker; live Human view and generated reader editions present the bridge as unheaded prose. The bridge should read as direct book prose rather than saying what "this chapter" or "the reader" should do, should avoid self-referential `chapter` phrasing inside the bridge body, and should contain at least 90 words of chapter-specific orientation before the technical machinery resumes.
- Optional `.asi-human-only`, `.asi-ai-only`, and `.asi-live-only` blocks must follow the release profile policy: human-only prose is retained for reader editions, AI/live-only material is hidden or stripped, and meaning-critical caveats stay in the ordinary reader spine.

## Visual Standards

- Use restrained technical styling.
- Prefer high contrast, readable line length, and stable spacing.
- Avoid decorative visuals that do not explain the architecture.
- Diagrams should clarify interfaces, loops, and evidence flow, with enough named states and transitions to explain a mechanism rather than merely satisfy coverage.
- Tables should remain readable on narrow screens.

## Release Standards

Before a public update:

```bash
python3 scripts/validate_book.py
python3 scripts/validate_reading_mode_toggle.py
python3 scripts/validate_human_reading_paths.py
quarto render --to html
python3 scripts/validate_live_human_view.py
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
- Appendix A loads,
- Appendix C loads,
- no raw private source files are tracked,
- GitHub Pages workflow succeeds.

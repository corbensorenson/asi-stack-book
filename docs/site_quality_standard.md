# Site Quality Standard

The public GitHub Pages site should be treated as a technical product, not just rendered markdown.

## Reader Experience

- The landing page must communicate title, thesis, current maturity, and reading path within the first screen.
- Parts and chapters must be easy to scan.
- Appendices must be visible as the evidence and governance layer of the book.
- Support states must be explained before readers encounter major claims.
- The site must not imply source ingestion or testing is complete when it is not.
- The top-of-page reading-mode switch must default to `AI view` and provide `Human view` by hiding the reader-release live-only chapter headings without claiming a reviewed reader artifact exists.

## Visual Standards

- Use restrained technical styling.
- Prefer high contrast, readable line length, and stable spacing.
- Avoid decorative visuals that do not explain the architecture.
- Diagrams should clarify interfaces, loops, and evidence flow.
- Tables should remain readable on narrow screens.

## Release Standards

Before a public update:

```bash
python3 scripts/validate_book.py
python3 scripts/validate_reading_mode_toggle.py
quarto render --to html
```

For full local release:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render
```

Check:

- home page loads,
- one representative chapter loads,
- Appendix A loads,
- Appendix C loads,
- no raw private source files are tracked,
- GitHub Pages workflow succeeds.

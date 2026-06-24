# Google Sites Living Book Plan

## Recommended model

Use Quarto as the canonical book source. Use Google Sites as the public hub.

Google Sites should contain:
- landing page,
- book summary,
- chapter index,
- latest release link,
- source/document links,
- changelog summary,
- embedded or linked Quarto site,
- contact/about page.

## Do not make Google Sites the source of truth

Google Sites is convenient for fast edits and public presentation, but Quarto is better for:
- version control,
- reproducible renders,
- code blocks,
- diagrams,
- appendices,
- PDF/HTML output,
- automated validation,
- claim/evidence tracking.

## Publication workflows

### Preferred workflow
1. Edit Quarto locally.
2. Render with `quarto render`.
3. Publish `_site/` to a static host.
4. Link or embed the hosted book from Google Sites.
5. Store PDFs and source exports in Google Drive if desired.
6. Update the Google Sites landing page for each release.

### Google Sites-only fallback
1. Render chapters locally.
2. Copy chapter summaries into Google Sites pages.
3. Link full HTML/PDF files stored elsewhere.
4. Embed diagrams or interactive pages as allowed.
5. Keep Quarto as canonical source anyway.

## Release cadence

- `v0.1`: scaffold + Part I + source matrix.
- `v0.2`: all chapter skeletons + diagrams.
- `v0.5`: full rough draft.
- `v0.8`: evidence/test specs integrated.
- `v1.0`: public living book release.

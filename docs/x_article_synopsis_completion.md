# X Article Synopsis Completion and Publication Disposition

Date: 2026-07-16; source refreshed 2026-07-17  
Roadmap priority: P9  
Milestones: M12 and M13  
Decision: **local source current; unpublished platform draft stale and refresh required**

The local article source was refreshed on 2026-07-17 to preserve the N0–N5
competence ceilings. Draft `2077875347220041728` predates that change. It remains
historical and unpublished, but it is no longer publishable without replacement
or update plus a new platform preflight.

## Completed canonical package

The maintained synopsis is complete at
`editions/x_article/asi_stack_synopsis.md`. It contains 5,329 canonical visible
words, opens with the exact live-book URL, and carries 24 stable claim markers.
`editions/x_article/claim_crosswalk.json` maps every marker to a chapter-core
claim atom, support state, evidence lane, named artifacts, article anchor, and
claim boundary. The article includes the book's strongest negative and blocked
results; it does not turn those results into architecture-wide proof.

The canonical header at
`editions/x_article/asi_stack_synopsis_header.png` is an exact 2000×800 RGB PNG
with a 5:2 ratio. Its provenance record contains canonical alt text and the
generation and resize history. The canonical image, not X's 1200×480 JPEG
derivative, is the maintained source of truth.

## Current-composer preflight

The signed-in X Article composer accepted the title and full body without
observed truncation. It reported 5,196 words, preserved the exact top live-book
link, accepted the header, and produced usable desktop and 390×844 mobile
previews without horizontal overflow. The unpublished draft identifier is
`2077875347220041728`.

Two platform limitations remain explicit. Plain-text import preserved paragraph
breaks and heading text but did not import Markdown heading or emphasis
semantics. The Article header editor exposed crop and remove controls but no
image-description field, so the locally maintained header alt text could not be
entered or read back. Audience controls were not opened because publication was
not authorized.

## Terminal boundary

No publish control was activated. No public Article URL exists. No commit, push,
tag, deployment, archive deposit, license change, or living-book release was
performed. Composer acceptance and visual previews do not prove the book's
claims, platform accessibility, audience reach, or future X behavior. No
chapter-core support state changed.

The package is governed by `editions/x_article/manifest.json`, validated by
`scripts/validate_x_article_synopsis.py`, and terminally recorded in
`release_records/2026-07-16-x-article-synopsis-ready-not-published.json`.
Future publication is owned by the active maintenance, transfer, and publication
roadmap and requires Corben's explicit action-time authorization.

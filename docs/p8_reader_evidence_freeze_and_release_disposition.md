# P8 reader evidence freeze and release disposition

Date: 2026-07-16  
Roadmap: `docs/post_v2_3_claim_proof_and_sota_challenge_roadmap.md`  
Priority / milestone: P8 / M11  
Terminal state: `evidence_freeze_ready_not_published_multiformat_release_not_approved`

## Decision

P8 is complete as a local, digest-bound evidence freeze. It is not a public
release. The evidence-reconciled reader source contains all 55 current chapters
and produces 60 HTML pages. HTML is the only format approved as an exact local
artifact in this cycle. EPUB and DOCX have useful bounded inspection evidence
but are not release-approved. PDF is a preserved failed format attempt because
full-page raster review found real diagram overflow and clipping.

No commit, tag, push, deployment, DOI deposit, archive deposit, public reader
release, living-book release, license grant, or external publication occurred.
No reader-format result changes any chapter or claim support state.

## Exact freeze

The authority chain is:

1. `editions/reader_manuscript/v2_2/manifest.json`
2. `editions/reader_manuscript/v2_2/evidence_freeze.json`
3. `editions/reader_manuscript/v2_2/format_review_matrix.json`
4. `editions/reader_manuscript/v2_2/release_disposition.json`
5. `release_records/2026-07-16-post-v2-3-p8-evidence-freeze-ready-not-published.json`

The freeze contains 84 source files, including 55 chapter sources, plus exact
HTML, EPUB, DOCX, and PDF artifacts. Every source file, evidence report, and
format artifact is bound by SHA-256. The validator recomputes those digests,
parses the document containers, checks the format-specific evidence, and rejects
seven attempted forms of state or evidence laundering.

## Format decisions

| Format | Exact result | Inspection that actually ran | Release decision |
|---|---|---|---|
| HTML | 60 pages; 55 chapter entry pages | Chromium desktop/mobile sweep, accessibility-tree probe, keyboard traversal, contrast and WCAG-preparation automation | Approved exact local artifact; not published |
| EPUB | 63 XHTML entries and 82 images; valid container | Structural inspection plus bounded Apple Books import, open, Preface render, accessibility-tree text exposure, and forward navigation | Bounded local application inspection; not release-approved |
| DOCX | 726 rendered pages; 81 media entries | Package inspection and visual review of every page through 16 contact sheets, with selected full-resolution checks | Built and fully raster-inspected; page-6 layout residual; not release-approved |
| PDF | 912 pages; untagged | Structural parsing and visual review of every page through 19 contact sheets, with selected full-resolution checks | Failed layout; not release-approved |
| Audio | Not generated | None | Not selected |
| Embedded audio | Not generated | None | Not selected |

## HTML evidence boundary

All 60 HTML pages passed at desktop and mobile widths, yielding 120 page-view
pairs with zero browser failures. The accessibility-tree probe also passed all
120 pairs with no unnamed interactive elements, image-alt failures, table-header
failures, duplicate IDs, or live/raw claim-marker leaks. Keyboard traversal
found no trap candidates and reached the skip link in every pair. The
WCAG-preparation probe sampled 4,624 rendered text combinations, found zero
contrast failures, and observed a minimum ratio of 4.69.

These are automated preparation and artifact checks. They are not screen-reader
review, device coverage, independent-human review, third-party certification,
or a legal claim of WCAG conformance. The legacy wrapper's request to rewrite a
49-page v1.0 manifest was rejected: the current 60-page report is validated
directly, while the historical record remains immutable.

## EPUB evidence boundary

The exact EPUB has SHA-256
`7264862f21ce4c1ea029d44966cc988840ab36e8275465ea363ef9707f6e7fb0`.
Its container is internally valid, begins with the required uncompressed
`mimetype` entry, and contains 63 XHTML entries and 82 images. The exact file
was imported into Apple Books. The cover opened, the Preface rendered as
readable text, the application accessibility tree exposed its heading and body,
and forward navigation worked.

This was a bounded local application inspection. It does not establish complete
chapter traversal, broad device behavior, distribution-store acceptance,
screen-reader quality, or assistive-technology conformance.

## DOCX evidence boundary

The corrected DOCX has SHA-256
`512b054a7afcc53423a3d7efc55826c48f722a9b159dd3620eaece1863b56371`.
After installing the missing SVG conversion dependency, it rebuilt with zero
conversion warnings. The package contains 81 media entries. The canonical Word
renderer produced 726 page images. Every page was visually covered by 16
contact sheets; there were no blank pages and no detected outer-edge ink pages.

Page 6 remains an editorial layout residual: a heading sits on a nearly empty
page before its diagram. The artifact was not inspected in Microsoft Word, so
no Word-application or public-release claim is made.

## PDF failure boundary

The preserved PDF attempt has SHA-256
`0fb3b95209f50ceee7d20ef70599d7bbf5c987430ba79ea541f9928f1aae9c97`.
It parses as 912 pages but is untagged. All pages were rasterized and covered by
19 contact sheets. The raster audit flagged two near-blank pages and 72 pages
with outer-edge ink. Full-resolution review confirmed that the page-48
architecture diagram is cut across the page/bottom boundary and the page-50
diagram extends beyond the right edge. Preview automation timed out twice.

The visual failures are independently sufficient to reject the PDF even without
Preview. This is evidence of a serious attempt and a terminal failed-format
disposition, not evidence of a usable PDF edition.

## Rights, release, and scientific boundary

Rights remain governed by `LICENSE.md`; this cycle creates no public license
grant. The local evidence freeze is the exact input to P9's synopsis work, but
it is not canonical claim, source, proof, experiment, or release authority for
the live book. Format construction, page count, and validation breadth do not
prove the book's scientific claims. P8 changes no support state and confers no
publication authority.


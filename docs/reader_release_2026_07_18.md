# Reader release 2026-07-18

Status: **published and byte-for-byte redownload verified**

This reader edition closes the repeated “ready but not released” loop identified
in the Round 15 review. It packages the current human-facing manuscript as PDF,
EPUB, and DOCX without changing the canonical living-book release identity.
The canonical evidence release remains `v2.3.0`; the reader tag is
`reader-2026-07-18` and is not marked latest.

Public release: <https://github.com/corbensorenson/asi-stack-book/releases/tag/reader-2026-07-18>

Release tag/commit: `reader-2026-07-18` / `0921a92484cd2a429790f180a4d3ce7bd304446b`

## Exact published artifacts

| Format | Bytes | SHA-256 | Internal QA |
|---|---:|---|---|
| [PDF](https://github.com/corbensorenson/asi-stack-book/releases/download/reader-2026-07-18/the-asi-stack-reader-2026-07-18.pdf) | 13,022,967 | `249a7e745fdb302398b532bd03d898b8bc6f07f96fbc6ad3794df69d3d1e1192` | 923/923 pages rasterized; 20/20 contact sheets reviewed; zero blank pages; page 1 is the only conservative low-ink flag |
| [EPUB](https://github.com/corbensorenson/asi-stack-book/releases/download/reader-2026-07-18/the-asi-stack-reader-2026-07-18.epub) | 10,129,904 | `c5ea58db02310c966ac0760348cc476ed6fba75446c7527105c0a9c4778a108f` | ZIP integrity passes; 152 entries, 64 XHTML entries/spine items, 82 images, and navigation across all chapters and appendices |
| [DOCX](https://github.com/corbensorenson/asi-stack-book/releases/download/reader-2026-07-18/the-asi-stack-reader-2026-07-18.docx) | 8,622,060 | `3b446abce2722aed960ce0b8d3cbdc7470486df7b9ba3b56f892acdefd8b4ee8` | LibreOffice render produced 737 pages; 16/16 contact sheets reviewed; zero blank, low-ink, or edge-ink pages |

The PDF source renderer inserted one interior page containing only the printed
pagination token `708`, with no XObjects or annotations. The bounded repair
script rejected any content-bearing page and removed only that page. The final
PDF has 923 pages and no blank raster pages. The stack map and lifecycle figures
that previously clipped now fit their page bounds.

## Rights and accessibility boundary

Copyright 2026 Corben Sorenson. All rights reserved. This release makes no new
license grant. The PDF is not tagged; the EPUB has not been reviewed in a native
reading application or with assistive technology; and the DOCX has not been
reviewed in Microsoft Word. These are explicit compatibility and accessibility
residuals, not hidden approvals. No PDF/UA, screen-reader, Apple Books,
Microsoft Word, external-human, peer-review, or legal-review claim is made.

## Reproduction commands

```bash
python3 scripts/build_reader_edition.py --profile reader_release
python3 scripts/validate_reader_spine.py --check
python3 scripts/remove_verified_pagination_only_pdf_page.py INPUT OUTPUT --page 708 --expected-pagination 708
python3 scripts/validate_reader_public_release_manifest.py --check-assets build/reader_release_2026_07_18/assets
```

The tracked manifest is
`editions/reader_manuscript/reader_2026_07_18/manifest.json`. GitHub accepted all
three assets, and each public download was redownloaded and compared against the
local approved artifact. Byte counts and SHA-256 digests matched in all three
cases. The release is intentionally not marked latest; `v2.3.0` remains the
canonical immutable living-book evidence release.

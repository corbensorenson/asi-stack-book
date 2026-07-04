# Reader Visual Identity Review

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_visual_identity.py
```

Tracked result: `editions/reader_manuscript/v1_0/visual_identity_manifest.json`

This source-level review checks the shared reader visual system before a final visual-art review exists. It covers the stylesheet tokens, key-figure presentation shell, mobile/print behavior, SVG accessibility metadata, palette diversity, and the existing contrast/readability manifest. It is not manual aesthetic review, not e-reader visual review, not DOCX/PDF application review, not final figure-artifact approval, and not reader release approval.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_source_level_visual_identity_review` |
| Stylesheet variables checked | 9 |
| CSS color count | 18 |
| SVG color count | 43 |
| Combined color count | 54 |
| Non-neutral color families | 5 |
| Color-family mix | copper-amber: 2, green: 3, neutral: 28, purple: 4, rose-red: 2, teal-blue: 15 |
| Key figures checked | 10 |
| SVG role/title/desc/viewBox coverage | 10 / 10 / 10 / 10 |
| Draft non-release boundaries | 10 |
| Minimum text contrast ratio | 5.19 |
| Minimum flow-line contrast ratio | 3.96 |
| Minimum marker contrast ratio | 3.96 |
| Minimum SVG text size | 15.0 px |

## Style Gates

- Shared theme tokens exist for ink, muted text, accent, copper, borders, figure background, figure rule, and figure shadow.
- Live `.asi-key-figure` blocks and curated-reader `reader-fig-*` figures share one presentation shell.
- Wide diagrams are horizontally contained on mobile, and print CSS avoids page breaks inside figures.
- The reading-mode switch, screen-reader-only helper class, table overflow, and inline-code wrapping are present in the public stylesheet.
- The palette is not a one-note hue family: the source-level mix includes neutral, teal-blue, copper-amber, green, rose-red, and purple families.

## Figure Gates

All ten draft key figures use `role="img"`, `aria-labelledby="title desc"`, `<title id="title">`, `<desc id="desc">`, and the standard `0 0 1200 760` viewBox. Each carries a draft/non-release boundary in the SVG source and remains a draft reader aid.

## Non-Claims

- This review does not approve final figure art.
- This review does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts.
- This review does not prove visual quality in every target application.
- This review does not promote any chapter core claim or support state.

# Reader Key-Figure Geometry Review

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_key_figure_geometry.py
```

Tracked result: `editions/reader_manuscript/v1_0/key_figure_geometry_manifest.json`

This CI-friendly source-geometry review checks the ten draft key figures for stable SVG layout bounds before final visual-art review exists. It parses the SVG source and checks the standard viewBox, visible content bounds, text-anchor bounds, entity counts, and visible draft/non-release status. It is not raster review, not manual aesthetic review, not e-reader visual review, not DOCX/PDF application review, not final figure-artifact approval, and not reader release approval.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_source_geometry_review` |
| Key figures checked | 10 |
| Standard viewBox count | 10 |
| Content bounds passed | 10 |
| Text-anchor bounds passed | 10 |
| Minimum visible text nodes | 25 |
| Minimum visible rectangles | 8 |
| Minimum visible connector paths | 8 |
| Minimum content width | 1016.0 px |
| Minimum content height | 532.0 px |
| Minimum content edge margin | 22.0 px |
| Maximum text anchor x | 1064.0 px |
| Maximum text anchor y | 738.0 px |

## Gate

Each draft key figure must keep the `0 0 1200 760` viewBox, keep visible content within the source-layout safety bounds, include at least 25 visible text nodes, 7 visible rectangles, and 8 visible connector paths, and preserve visible `draft visual asset` / `not release-reviewed` status text.

## Non-Claims

- This review does not render or raster-inspect the figures.
- This review does not approve final figure art.
- This review does not approve EPUB, DOCX, PDF, e-reader, audio, or reader release artifacts.
- This review does not prove visual quality in every target application.
- This review does not promote any chapter core claim or support state.

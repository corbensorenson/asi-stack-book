# Reader Key-Figure EPUB Layout Review

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_key_figure_epub_layout.py --write-manifest --write-doc
```

This local probe combines the current ignored curated-reader EPUB package with the local Chromium EPUB XHTML browser review report. It checks the ten draft key-figure XHTML entries, their packaged SVG references, figure-boundary paragraphs, release-boundary text, alt text, and desktop/e-reader-like viewport browser results. It is not dedicated e-reader device review, not e-reader application approval, not final figure-artifact approval, and not reader release approval.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_local_epub_key_figure_xhtml_layout_probe` |
| Key-figure XHTML entries | 10 |
| Browser page-view pairs | 20 |
| Failed page-view pairs | 0 |
| Minimum body text characters | 15628 |
| Minimum alt-text words | 23 |
| Maximum horizontal overflow | 0 px |
| Minimum image count | 2 |
| Image failures | 0 |
| Figure boundaries | 10 |
| Release boundaries | 10 |

## Per-Figure XHTML Entries

| Figure | XHTML entry | Alt words | Desktop overflow | E-reader overflow |
|---|---|---:|---:|---:|
| `asi_stack_control_plane` | `EPUB/text/ch003.xhtml` | 23 | 0 px | 0 px |
| `authority_to_effect_path` | `EPUB/text/ch005.xhtml` | 23 | 0 px | 0 px |
| `evidence_state_ladder` | `EPUB/text/ch007.xhtml` | 27 | 0 px | 0 px |
| `intent_to_artifact_trace` | `EPUB/text/ch015.xhtml` | 29 | 0 px | 0 px |
| `context_transaction_lifecycle` | `EPUB/text/ch019.xhtml` | 35 | 0 px | 0 px |
| `readiness_residual_quarantine_map` | `EPUB/text/ch028.xhtml` | 35 | 0 px | 0 px |
| `route_selection_budget_tradeoff` | `EPUB/text/ch033.xhtml` | 32 | 0 px | 0 px |
| `compression_and_generation_acceptance` | `EPUB/text/ch030.xhtml` | 32 | 0 px | 0 px |
| `cyclic_substrate_adoption_gate` | `EPUB/text/ch037.xhtml` | 33 | 0 px | 0 px |
| `living_book_release_pipeline` | `EPUB/text/ch045.xhtml` | 27 | 0 px | 0 px |

## Residuals

- This probe checks the ten key-figure XHTML entries, not a real e-reader device or app.
- It does not replace dedicated e-reader review, manual visual review, or final figure-artifact approval.
- Figure-artifact approval and reader release approval still require an edition release record naming exact reviewed artifacts.

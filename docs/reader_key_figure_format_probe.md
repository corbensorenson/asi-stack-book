# Reader Key-Figure Format Probe

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_key_figure_format_probe.py --write-manifest --write-doc
```

This probe inspects the current ignored curated-reader EPUB, DOCX, and PDF artifacts for the ten draft key figures. It checks package/text survival only: packaged SVG titles in EPUB, rasterized figure IDs and boundaries in DOCX, and extracted captions and figure-boundary paragraphs in PDF. It is not final figure-artifact approval, not e-reader review, not application review, not manual PDF review, and not reader release approval.

## Summary

| Format | Checks | Result |
|---|---|---:|
| EPUB | packaged SVG entries | 10 |
| EPUB | matched source SVG titles | 10 |
| EPUB | figure-boundary paragraphs | 10 |
| DOCX | PNG media entries | 61 |
| DOCX | matched figure stems | 10 |
| DOCX | raw `.qmd` relationship targets | 0 |
| PDF | figure-boundary paragraphs | 10 |
| PDF | matched draft caption titles | 10 |

## Per-Figure Crosswalk

| Figure | EPUB SVG entry | DOCX stem | PDF caption title |
|---|---|---|---|
| `asi_stack_control_plane` | `EPUB/media/file1.svg` | `asi-stack-control-plane` | ASI Stack control plane |
| `authority_to_effect_path` | `EPUB/media/file5.svg` | `authority-to-effect-path` | Authority to effect path |
| `compression_and_generation_acceptance` | `EPUB/media/file37.svg` | `compression-and-generation-acceptance` | Compression and generation acceptance |
| `context_transaction_lifecycle` | `EPUB/media/file24.svg` | `context-transaction-lifecycle` | Context transaction lifecycle |
| `cyclic_substrate_adoption_gate` | `EPUB/media/file48.svg` | `cyclic-substrate-adoption-gate` | Cyclic substrate adoption gate |
| `evidence_state_ladder` | `EPUB/media/file9.svg` | `evidence-state-ladder` | Evidence state ladder |
| `intent_to_artifact_trace` | `EPUB/media/file19.svg` | `intent-to-artifact-trace` | Intent to artifact trace |
| `living_book_release_pipeline` | `EPUB/media/file58.svg` | `living-book-release-pipeline` | Living book release pipeline |
| `readiness_residual_quarantine_map` | `EPUB/media/file34.svg` | `readiness-residual-quarantine-map` | Readiness residual quarantine map |
| `route_selection_budget_tradeoff` | `EPUB/media/file43.svg` | `route-selection-budget-tradeoff` | Route selection budget tradeoff |

## Residuals

- EPUB still needs real e-reader or application inspection for image sizing, fallback behavior, navigation, and reading flow.
- DOCX still needs Word, LibreOffice GUI, or Google Docs review for image anchoring, page breaks, and caption flow.
- PDF still needs manual page-level layout and reading-flow review for figure scale, caption placement, and near-edge content.
- Audio still needs reviewed spoken treatment; the companion summaries are drafting notes, not narration approval.
- This probe does not approve final figure art, release any format artifact, create a reader edition release record, or promote any chapter core claim.

# Reader Key-Figure DOCX Layout Review

Last checked: 2026-07-05

Command:

```bash
python3 scripts/validate_reader_key_figure_docx_layout.py --write-manifest --write-doc
```

This local probe converts the current ignored curated-reader DOCX through LibreOffice headless Writer PDF export, then inspects the ten draft key-figure title pages in the converted PDF. It verifies exact title pages, title bounding-box margins, page raster dimensions, nonblank page ink, near-edge ink absence, and luminance variation. It is not Word review, not LibreOffice GUI review, not Google Docs review, not manual document review, not final figure-artifact approval, and not reader release approval.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_local_docx_key_figure_layout_probe` |
| Converted PDF pages | 512 |
| Key-figure title pages | 10 |
| Raster pages rendered | 10 |
| Standard page size count | 10 |
| Minimum title margin | 72.1 pt |
| Minimum page ink | 9.92% |
| Maximum near-edge ink | 0.0% |
| Minimum luminance standard deviation | 38.23 |

## Per-Figure Pages

| Figure | Title page | Title margin | Page ink | Near-edge ink | Luminance std |
|---|---:|---:|---:|---:|---:|
| `asi_stack_control_plane` | 4 | 72.1 pt | 10.08% | 0.0% | 38.69 |
| `authority_to_effect_path` | 21 | 72.1 pt | 10.42% | 0.0% | 39.33 |
| `evidence_state_ladder` | 39 | 72.1 pt | 11.97% | 0.0% | 39.0 |
| `intent_to_artifact_trace` | 107 | 72.1 pt | 11.47% | 0.0% | 38.58 |
| `context_transaction_lifecycle` | 143 | 72.1 pt | 11.68% | 0.0% | 38.24 |
| `readiness_residual_quarantine_map` | 225 | 72.1 pt | 12.65% | 0.0% | 39.55 |
| `route_selection_budget_tradeoff` | 285 | 72.1 pt | 10.52% | 0.0% | 38.23 |
| `compression_and_generation_acceptance` | 248 | 72.1 pt | 11.4% | 0.0% | 39.97 |
| `cyclic_substrate_adoption_gate` | 325 | 72.1 pt | 9.92% | 0.0% | 38.44 |
| `living_book_release_pipeline` | 402 | 72.1 pt | 29.56% | 0.0% | 38.67 |

## Residuals

- This probe checks the ten key-figure title pages in the LibreOffice-converted DOCX PDF, not every document page.
- It does not replace Word review, LibreOffice GUI review, Google Docs review, manual document review, or final visual approval.
- Figure-artifact approval and reader release approval still require an edition release record naming exact reviewed artifacts.

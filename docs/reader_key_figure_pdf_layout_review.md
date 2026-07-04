# Reader Key-Figure PDF Layout Review

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_key_figure_pdf_layout.py --write-manifest --write-doc
```

This local probe inspects the current ignored curated-reader PDF for the ten draft key-figure caption pages. It verifies exact caption pages, caption bounding-box margins, page raster dimensions, nonblank page ink, near-edge ink absence, and luminance variation. It is not manual page-by-page PDF review, not final figure-artifact approval, and not reader release approval.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_local_pdf_key_figure_layout_probe` |
| PDF pages | 504 |
| Key-figure caption pages | 10 |
| Raster pages rendered | 10 |
| Standard page size count | 10 |
| Minimum caption margin | 165.878 pt |
| Minimum page ink | 3.36% |
| Maximum near-edge ink | 0.0% |
| Minimum luminance standard deviation | 14.2 |

## Per-Figure Pages

| Figure | Caption page | Caption margin | Page ink | Near-edge ink | Luminance std |
|---|---:|---:|---:|---:|---:|
| `asi_stack_control_plane` | 29 | 205.489 pt | 3.9% | 0.0% | 16.54 |
| `authority_to_effect_path` | 45 | 206.4 pt | 3.91% | 0.0% | 15.23 |
| `evidence_state_ladder` | 63 | 212.133 pt | 5.94% | 0.0% | 16.34 |
| `intent_to_artifact_trace` | 129 | 206.083 pt | 5.43% | 0.0% | 16.03 |
| `context_transaction_lifecycle` | 164 | 192.889 pt | 5.94% | 0.0% | 16.59 |
| `readiness_residual_quarantine_map` | 242 | 178.243 pt | 6.23% | 0.0% | 16.8 |
| `route_selection_budget_tradeoff` | 296 | 186.66 pt | 4.68% | 0.0% | 15.91 |
| `compression_and_generation_acceptance` | 263 | 165.878 pt | 9.22% | 0.0% | 28.69 |
| `cyclic_substrate_adoption_gate` | 331 | 188.16 pt | 3.36% | 0.0% | 14.2 |
| `living_book_release_pipeline` | 403 | 194.847 pt | 6.77% | 0.0% | 24.27 |

## Residuals

- This probe checks the ten key-figure caption pages, not every PDF page.
- It does not replace manual page-by-page PDF review, PDF viewer review, or final visual approval.
- Figure-artifact approval and reader release approval still require an edition release record naming exact reviewed artifacts.

# Reader Key-Figure Raster Review

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_key_figure_raster_probe.py --write-manifest --write-doc
```

This automated review inspects the current ignored PNG raster artifacts generated for the curated reader figure fallbacks. It checks that all ten key figures rasterized to the expected 1200 x 760 canvas, are not blank or low-ink, preserve visual variation, and retain opaque page-area coverage. It is not manual aesthetic review, not final figure-artifact approval, not e-reader review, not DOCX/PDF application review, and not reader release approval.

## Summary

| Metric | Value |
|---|---:|
| Status | `passed_local_raster_artifact_probe` |
| Raster artifacts checked | 10 |
| Standard dimensions | 10 |
| Minimum opaque pixel coverage | 99.954% |
| Minimum luminance standard deviation | 27.64 |
| Minimum quantized color count | 116 |
| Minimum dark-pixel share | 0.51% |
| Minimum mid-tone share | 5.08% |
| Maximum transparent pixels | 420 |
| Minimum edge opaque coverage | 96.53% |
| Total raster bytes | 1671185 |

## Per-Figure Raster Rows

| Figure | Raster artifact | Size | Luminance std | Quantized colors | SHA-256 |
|---|---|---:|---:|---:|---|
| `asi_stack_control_plane` | `build/curated_reader_edition/assets/diagrams/format-png/asi-stack-control-plane.png` | 1200 x 760 | 34.87 | 156 | `2a6730e120980bac68818af138c4e69c82b742ccfe60d71ac43e08c500e32c93` |
| `authority_to_effect_path` | `build/curated_reader_edition/assets/diagrams/format-png/authority-to-effect-path.png` | 1200 x 760 | 31.58 | 154 | `de49d9780058711bccea4fd1b3192ee6e160456cd584afbac868ee364434f007` |
| `evidence_state_ladder` | `build/curated_reader_edition/assets/diagrams/format-png/evidence-state-ladder.png` | 1200 x 760 | 32.88 | 184 | `0ccea61e80682f94c5b7d266b8459cdb42a02366ce41f6f671fb1df4eb1c02ec` |
| `intent_to_artifact_trace` | `build/curated_reader_edition/assets/diagrams/format-png/intent-to-artifact-trace.png` | 1200 x 760 | 32.9 | 182 | `0bca4f5cd8cb48570bea4634ef6f3330a4cdb0f756aa049c85462a4d2c3272b8` |
| `context_transaction_lifecycle` | `build/curated_reader_edition/assets/diagrams/format-png/context-transaction-lifecycle.png` | 1200 x 760 | 33.56 | 172 | `ef26264bc957a3b065a70e94cd4de7b3920d60e06276c10e24761430b31d810a` |
| `readiness_residual_quarantine_map` | `build/curated_reader_edition/assets/diagrams/format-png/readiness-residual-quarantine-map.png` | 1200 x 760 | 34.12 | 173 | `2c1b7b8f1a8816542f0303c431d356a31250aa6db4fee10cbf38b4876250e444` |
| `route_selection_budget_tradeoff` | `build/curated_reader_edition/assets/diagrams/format-png/route-selection-budget-tradeoff.png` | 1200 x 760 | 33.0 | 162 | `c9f0681894f824e2936b33e98c18602caece473bcc81fb23bc55b3117823309d` |
| `compression_and_generation_acceptance` | `build/curated_reader_edition/assets/diagrams/format-png/compression-and-generation-acceptance.png` | 1200 x 760 | 32.99 | 144 | `d48d6e5f4143f9be21911a0669a4758ea3809ffc589e70b5977e3f82f7155d22` |
| `cyclic_substrate_adoption_gate` | `build/curated_reader_edition/assets/diagrams/format-png/cyclic-substrate-adoption-gate.png` | 1200 x 760 | 28.76 | 116 | `c77a9c14ce9825768f4344150b83ac646335ebac7d355946135992232979da4f` |
| `living_book_release_pipeline` | `build/curated_reader_edition/assets/diagrams/format-png/living-book-release-pipeline.png` | 1200 x 760 | 27.64 | 131 | `43e0039512b5a42aea75166804585bd8953d338c88791564f4f6b64c969652e8` |

## Residuals

- This automated raster review catches missing, blank, low-ink, or visually collapsed PNG fallbacks.
- It does not judge whether the figure is beautiful, editorially final, or optimal for a particular reader.
- EPUB still needs real e-reader review, DOCX still needs application review, and PDF still needs page-level layout review.
- Final figure-artifact approval and reader release approval still require an edition release record naming exact reviewed artifacts.

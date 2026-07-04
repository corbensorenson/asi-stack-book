# Reader Key-Figure Contrast Review

Last checked: 2026-07-04

Command:

```bash
python3 scripts/validate_reader_key_figure_contrast.py
```

Tracked result:

- `editions/reader_manuscript/v1_0/key_figure_contrast_manifest.json`

This review records a deterministic source-level SVG contrast and readability
gate for the ten draft key figures in the curated reader manuscript. It is not a release approval, not final figure-artifact approval, not manual visual
judgment, and not EPUB, DOCX, PDF, e-reader, HTML, MP3, M4B, or audio approval.

## Thresholds

| Check | Threshold | Observed minimum |
|---|---:|---:|
| minimum text contrast ratio | 4.5 | 5.19 |
| minimum flow-line contrast ratio | 3.0 | 3.96 |
| minimum marker contrast ratio | 3.0 | 3.96 |
| minimum SVG text size | 15 px | 15 px |

The validator parses each SVG, resolves the shared text color classes against
the light and pastel surface classes used in the figure, checks flow-line and
marker colors against the page and panel surfaces, and verifies that all text
nodes carry a known font-size class. The gate is intentionally source-level:
it catches contrast regressions and unreadable SVG text classes before render,
but it does not replace rendered format inspection.

## Figure Results

| Figure ID | Asset | Text contrast | Flow contrast | Marker contrast | Min text size | Status |
|---|---|---:|---:|---:|---:|---|
| `asi_stack_control_plane` | `assets/diagrams/asi-stack-control-plane.svg` | 5.42 | 3.96 | 3.96 | 15 px | pass |
| `authority_to_effect_path` | `assets/diagrams/authority-to-effect-path.svg` | 5.36 | 3.96 | 3.96 | 15 px | pass |
| `evidence_state_ladder` | `assets/diagrams/evidence-state-ladder.svg` | 5.25 | 5.54 | 5.73 | 15 px | pass |
| `intent_to_artifact_trace` | `assets/diagrams/intent-to-artifact-trace.svg` | 5.25 | 3.96 | 3.96 | 15 px | pass |
| `context_transaction_lifecycle` | `assets/diagrams/context-transaction-lifecycle.svg` | 5.25 | 5.54 | 5.73 | 15 px | pass |
| `readiness_residual_quarantine_map` | `assets/diagrams/readiness-residual-quarantine-map.svg` | 5.25 | 3.96 | 3.96 | 15 px | pass |
| `route_selection_budget_tradeoff` | `assets/diagrams/route-selection-budget-tradeoff.svg` | 5.36 | 5.54 | 5.73 | 15 px | pass |
| `compression_and_generation_acceptance` | `assets/diagrams/compression-and-generation-acceptance.svg` | 5.19 | 4.50 | 5.55 | 15 px | pass |
| `cyclic_substrate_adoption_gate` | `assets/diagrams/cyclic-substrate-adoption-gate.svg` | 5.20 | 4.57 | 4.57 | 15 px | pass |
| `living_book_release_pipeline` | `assets/diagrams/living-book-release-pipeline.svg` | 5.23 | 4.27 | 4.27 | 15 px | pass |

## Release Boundary

This gate closes only the measured source-SVG contrast/readability slice for
the current draft key figures. The figures still need manual aesthetic review,
format-specific layout review, e-reader behavior inspection, DOCX/PDF
application review, audio treatment review, and an edition release record
before they can be called final reader-release art.

## Non-Claims

- This review does not approve final figure art.
- This review does not approve EPUB, DOCX, PDF, e-reader, audio, or HTML release artifacts.
- This review does not prove any ASI Stack claim.
- This review does not promote any chapter core claim.

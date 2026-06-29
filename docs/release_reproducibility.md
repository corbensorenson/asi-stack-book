# Release Reproducibility

Last updated: 2026-06-29

This note records the toolchain and citation boundary for the tagged v1.0.0 living-book release. It is a reproducibility and citability record, not an approval of EPUB, DOCX, PDF, e-reader, or audio artifacts.

## CI Toolchain

| Surface | Pinned or controlled value | Source of truth |
|---|---|---|
| Quarto | `1.9.38` | `.github/workflows/publish.yml` |
| Python | `3.11` in CI; Python `3.9.23` is the current local validated interpreter | `.github/workflows/publish.yml`; local command output |
| Node | `22` in CI; `v22.15.0` is the current local validated runtime | `.github/workflows/publish.yml`; local command output |
| Lean | `leanprover/lean4:v4.31.0` | `lean/lean-toolchain` |
| Lake | `Lake version 5.0.0-src+68218e8` with Lean `4.31.0` locally | local command output |
| elan | `elan 4.2.2` locally | local command output |
| HTML render locale | `C.UTF-8` in CI render step | `.github/workflows/publish.yml` |
| PDF probe locale | `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8` when running the isolated PDF probe | `docs/reader_pdf_probe_manifest.md`; `docs/reader_format_dry_run.md` |

## Local Tool Paths Observed

| Tool | Observed path or status |
|---|---|
| `quarto` | `/Users/corbensorenson/miniforge3/bin/quarto` |
| `python3` | `/Users/corbensorenson/miniforge3/bin/python3` |
| `node` | `/opt/homebrew/opt/node@22/bin/node` |
| `libreoffice` | not found on `PATH` in the current shell during this audit |

The current shell reports `LANG=C.UTF-8` and `LC_ALL=C`. That is sufficient for the HTML validation run recorded here. PDF probing remains a separate path that must set `LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8` unless a later audit retests and records a different locale requirement.

## Reader-Format Dependencies

HTML is the primary living-book target. EPUB, DOCX, PDF, e-reader conversion, and audio are release-profile outputs with separate blocker ledgers. Local reader-format probes exist, but the public release rule remains stricter:

- EPUB approval requires application-level e-reader review and an edition release record naming the exact artifact.
- DOCX approval requires full application review of the converted document and an edition release record naming the exact artifact.
- PDF approval requires page-level layout review and an edition release record naming the exact artifact.
- Audio approval requires a reviewed reader edition, reviewed audio script, generated audio artifacts, packaging checks, and a release record naming the exact artifacts.

## Fonts And Layout

The HTML book currently relies on Quarto's generated site assets, the repository stylesheet in `assets/styles.scss`, rendered Mermaid diagrams, and the generated landing-page image. No custom book font is declared as a release-critical dependency. If a future reader, PDF, EPUB, or DOCX profile introduces custom fonts or layout-sensitive font substitutions, this file and the corresponding format-review row must name them before artifact approval.

## Citation Boundary

`CITATION.cff` now identifies the public book as version `1.0.0` with date `2026-06-29`. The exact source state is tag `v1.0.0` at commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`. The tracked living-book release record is `release_records/2026-06-29-v1.0.0-living-book-96d0ca3c.json`, and the GitHub Release is <https://github.com/corbensorenson/asi-stack-book/releases/tag/v1.0.0>.

How to cite v1.0.0:

- Cite the public site: `https://corbensorenson.github.io/asi-stack-book/`.
- Cite the repository: `https://github.com/corbensorenson/asi-stack-book`.
- Include the version string `1.0.0`.
- Include tag `v1.0.0` and source commit `96d0ca3c6b62f3530202535573941b1f6e50a83d`.
- Do not cite a DOI for v1.0.0; no DOI or Zenodo archive has been issued.

ORCID metadata is not recorded because no ORCID was provided during this audit. DOI/Zenodo metadata is explicitly pending until a real archive exists.

## Reproduction Commands

Run the full local gate from the repository root:

```bash
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py --check
python3 scripts/validate_release_reproducibility.py
python3 scripts/validate_publication.py
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
python3 scripts/validate_live_human_view.py
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

For the isolated PDF probe, use the documented UTF-8 locale:

```bash
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 python3 scripts/render_reader_formats.py --output build/reader_edition_pdf_probe_utf8 --formats pdf
```

## Non-Claims

This file does not claim that a DOI exists, that EPUB/DOCX/PDF/audio artifacts are approved, that local reader-format probes are release artifacts, that Lean proves broad system safety, or that any chapter core support state moved above `argument`.

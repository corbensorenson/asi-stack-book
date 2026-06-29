# Reader EPUB Probe Manifest

Last updated: 2026-06-28

This summary is synced from
`editions/reader_manuscript/v1_0/epub_probe_manifest.json`. It records the
latest tracked local EPUB metadata, navigation, spine, and source-card sampling
evidence for the generated reader EPUB snapshot. It is not a reader release,
not an EPUB release, not e-reader approval, and not a support-state promotion.

## Commands

```bash
python3 scripts/render_reader_formats.py --formats html epub docx
python3 scripts/inspect_reader_format_artifacts.py
python3 - <<'PY' ... inspect EPUB/content.opf, EPUB/nav.xhtml, text XHTML entries, evidence-boundary text, and reader source-card appendix entries ...
```

## EPUB Container Summary

| Field | Value |
|---|---:|
| Local artifact | `build/reader_edition/format_artifacts/epub/_reader_site/The-ASI-Stack.epub` |
| File size | 9,078,787 bytes |
| Zip entries | 130 |
| XHTML entries | 62 |
| Text XHTML entries | 61 |
| Image entries | 62 |
| OPF item count | 126 |
| OPF itemref count | 62 |
| Navigation href count | 866 |
| Navigation list-item count | 866 |
| Mimetype first | yes |
| Mimetype content | `application/epub+zip` |

Required EPUB entries are present: `mimetype`, `META-INF/container.xml`,
`EPUB/content.opf`, `EPUB/nav.xhtml`, `EPUB/toc.ncx`, and
`EPUB/text/title_page.xhtml`.

## Metadata Probe

| Field | Value |
|---|---|
| Title | The ASI Stack |
| Creator | Corben Sorenson |
| Language | en-US |
| Language source | generated Quarto config declares `lang: en-US` |
| Cover image present | yes |

The EPUB metadata previously depended on the render process locale. The live
and generated-reader Quarto scaffolds now declare `lang: en-US`, and the
structural inspector rejects EPUB snapshots that do not preserve that value.

## Spine Sampling

| Entry | Surface | Observation |
|---|---|---|
| `EPUB/text/ch001.xhtml` | Reader opening note | Reader Edition Note text is present in the first body XHTML entry. |
| `EPUB/text/ch003.xhtml` | Opening chapter support boundary | Compact evidence-boundary text is present in the opening chapter XHTML entry. |
| `EPUB/text/ch058.xhtml` | Corben/local source appendix cards | Reader Source List text and `proof_carrying_circular_computation` source-card text are present in the Corben/local source appendix XHTML entry. |
| `EPUB/text/ch059.xhtml` | External source appendix cards | Reader Source List, External Citation Policy, and `concrete_ai_safety` text are present in the external-source appendix XHTML entry. |

## Release Blockers Preserved

- `reader_release_record_not_created`
- `full_format_artifact_review_not_completed`
- `app_or_ereader_review_not_completed`

This is a structural EPUB metadata and source-spine probe, not an e-reader
application review in Apple Books, Kindle Previewer, Calibre, or physical
e-reader hardware.

## Non-Claims

- This manifest records a local EPUB structural and metadata probe in ignored build space only.
- This manifest is not a reader release, EPUB release, ebook release, edition release record, e-reader application review, or artifact approval.
- This manifest does not approve EPUB, DOCX, PDF, HTML, e-reader, document, audio, or audio-embedded EPUB artifacts for publication.
- This manifest does not check full editorial quality, full layout quality, application behavior, e-reader pagination, source interpretation, proof adequacy, benchmark behavior, runtime behavior, PDF output approval, DOCX output approval, or audio output.
- This manifest does not promote any claim support state.

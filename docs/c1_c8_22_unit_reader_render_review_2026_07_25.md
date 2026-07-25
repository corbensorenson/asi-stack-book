# C1–C8 22-Unit Reader Render Review

Recorded: 2026-07-25

## Artifact boundary

The current narrative candidate was generated from
`products/narrative_product_spine.json` and
`products/narrative_unit_crosswalk.json` into the ignored local workspace
`build/narrative_product`. It is a 22-unit derivative of the canonical
84-chapter source, not a parallel manuscript or release.

## Commands

```bash
python3 scripts/build_narrative_running_example.py
python3 scripts/validate_narrative_running_example.py
python3 scripts/validate_product_projections.py
python3 scripts/build_reader_edition.py \
  --narrative-spine products/narrative_product_spine.json \
  --output build/narrative_product
cd build/narrative_product
quarto render --to html
cd ../..
node scripts/validate_reader_html_artifact_browser.js \
  --strict \
  --site build/narrative_product/_reader_site \
  --manifest build/narrative_product/reader_manifest.json \
  --report build/narrative_product_browser_report.json
node scripts/validate_curated_reader_accessibility_tree.js \
  --standalone \
  --site build/narrative_product/_reader_site \
  --manifest build/narrative_product/reader_manifest.json \
  --report build/narrative_product_accessibility_tree_report.json
```

## Observed result

- Reader generation selected 22 representative chapters.
- Quarto rendered 27 HTML pages: index, preface, 22 chapters, and three source
  or glossary appendices.
- Strict local Chrome inspection passed 54 page-view pairs: desktop and mobile
  views for every rendered page.
- The candidate was regenerated after all 84 canonical chapters and current
  reader contracts changed the aspirational `Beyond the State of the Art`
  heading to the evidence-honest `Mature Research Target`; the same 27-page,
  54-pair render/browser checks passed again.
- The browser report recorded zero failing page views and no horizontal
  overflow at the tested 1280-by-900 and 390-by-844 viewports.
- Narrative contract validation passed 22 editorial contracts, 23 cumulative
  artifacts, and six rejecting continuity controls.
- Product validation passed 22 narrative units, 62 reference-routed chapters,
  all 84 reference chapters, 17 evidence routes, and four rejecting controls.
- The source was also rendered as the complete canonical book from a clean
  temporary copy: 97 HTML pages, all 84 chapters, all 11 appendices, and 439
  live-only headings and matching TOC targets passed the static Human-view
  check.
- The 22-unit candidate's automated accessibility-tree preparation probe
  passed 54 desktop/mobile page-view pairs: 54/54 language, title, one-H1,
  main landmark, navigation landmark, skip-link, focus-visible, and Chromium
  accessibility-tree checks; zero unnamed interactive elements, image-alt
  failures, table-header failures, duplicate-ID page views, live-marker leaks,
  or raw core-claim leaks. This is preparation evidence, not accessibility
  certification.

## Authorial compound-unit meaning review

The crosswalk routes reference chapters; it does not pretend that one
representative chapter contains their full content. The authorial pass checked
that each unit's question, repository-change example, objection, failure story,
change-of-conclusion condition, and handoff preserve the distinct jobs below.

| Unit | Representative | Meaning that must survive the condensed route | Result |
|---|---|---|---|
| 1 | Stack thesis | Responsibility boundaries and noninheritance, not modularity for its own sake. | Preserved. |
| 2 | Efficient ASI | Full-lifecycle, risk-adjusted efficiency rather than token price alone. | Preserved. |
| 3 | Authority and failure | Security, misuse, privacy, custody, provenance, and military risk remain reference owners; capability never becomes a grant. | Preserved and routed. |
| 4 | Evidence | Support changes remain claim-specific; oversight does not inherit independence. | Preserved and routed. |
| 5 | Constitutional governance | Values, objectives, human factors, persuasion, institutions, and resilience remain contestable rather than one scalar objective. | Preserved and routed. |
| 6 | Capability fields | Stable identity is separated from replacement qualification and rollback. | Preserved and routed. |
| 7 | Intent | Human ambiguity and legitimate authority remain distinct from executable command fields. | Preserved and routed. |
| 8 | Planning | A dependency graph remains a proposal, not execution permission. | Preserved. |
| 9 | World models | Perception, imagined branches, causal interventions, physical effects, and later observations remain distinct. | Preserved and routed. |
| 10 | Compilation | Semantic lowering exposes loss; relational and mathematical substrates remain optional owned mechanisms. | Preserved and routed. |
| 11 | Context ABI | Paging, caching, mounts, snapshots, taint, belief, and authority remain nonidentical. | Preserved and routed. |
| 12 | Memory | Durable semantic consolidation and procedural promotion remain separate lifecycles. | Preserved and routed. |
| 13 | Verification bandwidth | Having relevant text is not the same as having adequate independent comparison capacity. | Preserved. |
| 14 | Claim and proof review | Claims, belief revision, proof contracts, semantic depth, and white-box evidence retain different inference ceilings. | Preserved and routed. |
| 15 | Labor and artifacts | Human/agent jobs, organizations, protocols, stewardship, deployment, artifacts, and multi-agent effects retain owners. | Preserved and routed. |
| 16 | Runtime and operations | Approval, effect mediation, incident command, degradation, recovery, and decommissioning remain distinct. | Preserved and routed. |
| 17 | Routing and substrates | Heterogeneous architectures remain replaceable behind qualified fields; novelty does not inherit readiness. | Preserved and routed. |
| 18 | Developmental learning | Training, optimizer state, learning theory, feedback, data rights, causal experiment, memory, procedure, stabilization, and promotion remain joined but noncollapsed. | Preserved and routed. |
| 19 | Readiness and liveness | Benchmarks, adversarial evaluation, safety cases, thresholds, release, authenticity, residuals, and finite quarantine share a decision without collapsing into one score. | Preserved and routed. |
| 20 | Resource and recovery economics | Compute, memory, storage, energy, latency, labor, false blocks, rollback, and residuals share full-lifecycle accounting. | Preserved and routed. |
| 21 | Recursive integration | Open-ended and recursive proposals cannot self-ratify; replication, integration, Theseus, and roadmap gates remain bounded consumers. | Preserved and routed. |
| 22 | Living book | Sources, claims, corrections, derivatives, releases, and the open agenda remain accountable without record volume becoming research quality. | Preserved and routed. |

No canonical core-claim identity or support state changed in this condensation.
Every omitted chapter remains linked from its assigned unit in the generated
architecture reference.

## Closure boundary

This receipt closes current-route generation, the authorial compound-unit
meaning-preservation pass, complete canonical HTML render, basic link/page
loading, live-scaffold leakage, desktop/mobile smoke, and automated
accessibility preparation. It does not establish a final line edit, full
accessibility conformance, EPUB/PDF/DOCX/audio quality, reader comprehension,
release approval, deployment, or publication.

The new C1–C8 cross-owner links, retained-lineage ownership map, Developmental
Intelligence Loop figure, and minimum-trust/bounded-liveness figure close the
remaining organizational residuals named by the Phase 1 audit. Product and
canonical renders must be regenerated after any later prose change, and future
format-specific quality remains publication work rather than a reason to keep
ideas in planning.
No support state changes.

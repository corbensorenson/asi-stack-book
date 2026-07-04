# Key Figures Companion Note

Status: drafting companion note, not release reviewed.

Scope: ten draft key figures listed in
`editions/reader_manuscript/v1_0/manifest.json`.

Routing record: `docs/reader_key_figure_artifact_review.md`

This note helps e-reader and audio review for the reader-manuscript key
figures. It does not replace the chapter prose, figure captions, alt text, or
visible figure-boundary paragraphs. It is not final figure-artifact review, not
a narration script approval, not an EPUB/DOCX/PDF layout approval, and not an
audio release record.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
what each draft figure is trying to make memorable without mistaking the figure
for implementation evidence. The figures are orientation aids. They show
interfaces, records, gates, residuals, and release boundaries; they do not
prove deployed behavior, model quality, runtime safety, benchmark performance,
or support-state movement.

## Spoken Figure Summaries

| Figure | Asset | Spoken summary | Boundary |
|---|---|---|---|
| ASI Stack Control Plane | `assets/diagrams/asi-stack-control-plane.svg` | The stack starts with human intent, moves through governed planning, memory, claims, execution, routing, evidence, release records, residuals, and rollback, and only improves through recorded gates. | This is a draft orientation map, not evidence that an integrated ASI runtime exists. |
| Authority to Effect Path | `assets/diagrams/authority-to-effect-path.svg` | A request becomes an external effect only after permission class, authority ceiling, scoped approval, adapter handoff, receipt, denial, escalation, rollback, and incident paths are kept explicit. | This does not prove deployed authorization, revocation, rollback, adapter security, or incident response. |
| Evidence State Ladder | `assets/diagrams/evidence-state-ladder.svg` | Claim labels and support states are separate; promotions, no-change decisions, demotions, refutations, blockers, residuals, and non-claims move through review rather than through confident prose. | This does not promote any claim or prove that future evidence reviews will be correct. |
| Intent to Artifact Trace | `assets/diagrams/intent-to-artifact-trace.svg` | One request is followed through accepted intent, command contract, plan, typed job, authority gate, adapter effect, artifact node, evidence ledger, replay, feedback, refusal, residual, and re-contracting. | This does not prove parser quality, dispatcher enforcement, adapter safety, replay behavior, or artifact satisfaction. |
| Context Transaction Lifecycle | `assets/diagrams/context-transaction-lifecycle.svg` | Memory is treated as an accountable transaction: records, certificates, snapshots, mounts, taint, deletion closure, materialized views, faults, quarantine, adequacy, belief updates, and job handoffs stay linked. | This does not prove retrieval quality, runtime memory-store behavior, deletion closure, taint enforcement, or context adequacy. |
| Readiness, Residual, Quarantine Map | `assets/diagrams/readiness-residual-quarantine-map.svg` | A candidate route or replacement moves through readiness, limited use, residual escrow, quarantine, blocker handling, review reruns, and anti-laundering boundaries before any stronger claim is allowed. | This does not prove readiness-engine behavior, residual-ledger storage, quarantine enforcement, rollback behavior, or support-state promotion. |
| Route Selection Budget Tradeoff | `assets/diagrams/route-selection-budget-tradeoff.svg` | Route choice prices adequacy, authority, readiness, protected review cost, fallback, residual ownership, and negative controls before selecting what is cheaper enough and safe enough to try. | This does not prove deployed routing, production scheduler behavior, model quality, economic optimality, or core-claim promotion. |
| Compression and Generation Acceptance | `assets/diagrams/compression-and-generation-acceptance.svg` | Compact generation, fast generation, and artifact compression are useful only when verification, repair, fallback, residual burden, and consumer policy decide what is accepted. | This does not prove compression ratio, speed, task quality, reconstruction utility, verifier behavior, or model performance. |
| Cyclic Substrate Adoption Gate | `assets/diagrams/cyclic-substrate-adoption-gate.svg` | Cyclic substrates such as RoPE-like position schemes, circulant mixers, or cyclic memory enter only through structural receipts, symmetry baselines, measured tradeoffs, canary routing, and retirement paths. | This does not prove model quality, context-length improvement, hardware performance, training stability, transfer, or deployment. |
| Living Book Release Pipeline | `assets/diagrams/living-book-release-pipeline.svg` | The live book, human reader manuscript, proof/evidence artifacts, format builds, release records, open blockers, and future backlog stay separate so the project can publish without confusing drafts with approved artifacts. | This does not approve any reader release, EPUB, DOCX, PDF, audiobook, source adequacy, or support-state movement. |

## Audio Treatment

In a future narration script, do not read the visual layout of each figure as a
coordinate-by-coordinate description. Use the spoken summary to give the
listener the figure's purpose, then name the boundary that prevents the figure
from becoming evidence. If a figure carries a dense flow, route the full visual
detail to the e-reader or companion material and keep the main audio focused on
the governing question:

- What is being handed off?
- Which gate, receipt, residual, or rollback keeps the handoff honest?
- What would this figure be wrongly claiming if its boundary were omitted?

## E-Reader Treatment

For EPUB, PDF, DOCX, and e-reader review, keep the figure image, caption, alt
text, visible figure boundary, and this companion note aligned. If a format
shrinks a figure until its labels are hard to read, the spoken summary above is
the fallback text, not a replacement for layout review.

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not final figure-artifact approval.
- This companion note is not EPUB, DOCX, PDF, HTML, e-reader, MP3, M4B, or
  audio-embedded EPUB approval.
- This companion note does not produce or approve an audiobook or narration
  script.
- This companion note does not promote any chapter core claim above
  `argument`.
- This companion note does not prove deployed behavior, runtime safety, model
  quality, benchmark performance, economic outcome, source adequacy, release
  readiness, transfer, or ASI.

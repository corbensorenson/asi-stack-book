# Public Status Surface Inventory

Last updated: 2026-07-10

The canonical status builder owns global active metrics. README, landing,
candidate-status, and publication-readiness prose each contain exactly one
generated block. `sync_public_trust_metrics.py` obtains those values from
`build_canonical_public_status.py`, not from parallel count functions, and
`validate_public_status_consistency.py` rejects a missing, duplicate, stale,
or hand-edited block as well as contradictory active prose around it.

| Surface class | Authority | Rule |
|---|---|---|
| Active public summaries | generated canonical-status block | Exactly one block per configured surface; every count must equal the canonical object. |
| Navigation and chapter order | `book_structure.json` through Quarto/scaffold generation | Rendered sidebar paths, titles, order, uniqueness, and chapter H1 count are checked against canonical status. |
| Chapter status headers | per-chapter manifest fields | Headers may report that chapter's claim label, support state, sources, and proof hooks, but may not carry a separately maintained global chapter/source count. |
| Generated reader edition | `book_structure.json` plus release-profile builders | Ignored build manifests derive active chapter order and totals during generation; they are not hand-maintained public status. |
| Tracked v1.0 curated reader manifests | explicit `historical_release_snapshot` scope | Their 44-chapter frozen spine is historical and cannot override the active 54-chapter manifest. |
| Deployed site | tested bundle canonical status | Must identify one clean tested commit and pass the post-deployment graph crawl. |

This inventory does not make historical records current, approve a reader
artifact, or turn generated metadata into evidence for chapter claims.

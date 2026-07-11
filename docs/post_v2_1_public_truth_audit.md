# Post-v2.1 Public-Truth Audit

Audit date: 2026-07-10

Roadmap priority: P0 — Public truth reconciliation

State: complete; local reconciliation, clean tested deployment, and public
attestation passed

## Canonical identity

| Field | Canonical value | Authority |
|---|---|---|
| Latest immutable evidence release | `v2.1.0` | `status/versioned_release_policy.json` |
| Exact source commit | `cb3b86051c3f4bd82e8b3128c0fdf180e8a7cfa5` | v2.1.0 release record and policy |
| Immutable rendered archive SHA-256 | `c70534db9ffed722f33227b191930781b2daf1058d949b90d803bca9a47e375c` | versioned release policy |
| Active roadmap | `docs/post_v2_1_residual_and_transfer_roadmap.md` | machine roadmap status |
| Completed predecessor | `docs/post_v2_evidence_roadmap.md` | completion declaration and roadmap status |
| Core-claim state | 54 of 54 at `argument` | manifest and evidence vectors |
| Mutable channels | root site and `/latest/` | versioned release policy |
| v2.1.0 released formats | canonical live HTML and immutable HTML site archive | exact release record |
| Formats outside v2.1.0 scope | EPUB, DOCX, PDF, audio, curated reader | exact release record |
| DOI | none issued | root and historical citation records |

## Audited current surfaces

- `index.qmd`: release identity, active roadmap, claim boundary, mutable-channel
  boundary, fast-audit route, and optional-format boundary reconciled.
- `README.md`: active roadmap pointer, v2.1.0 status, rights tag, mutable-channel
  boundary, and optional-format boundary reconciled.
- `CITATION.cff`: v2.1.0 title, version, date, URL, and repository route retained;
  `citations/v1.0.0.cff` remains explicitly historical.
- `docs/release_reproducibility.md`: current v2.1.0 citation and immutable archive
  guidance added; v1.0.0 citation retained under a historical heading.
- `docs/publication_readiness.md`: active roadmap and latest-release authority
  added; v1.x roadmaps and v1.0 status relabeled historical.
- `docs/public_status_contract.md` and `status/public_status_config.json`: active
  version reconciled to v2.1.0 while the baseline field remains historical.
- `status/versioned_release_policy.json`: v2.1.0 URL, commit, archive state, and
  digest agree with the exact release record.
- `LICENSE.md`, `NOTICE.md`, and `README.md`: current grants remain tag-bound to
  v2.1.0; later or mutable-channel files receive no automatic grant.
- predecessor and completion documents: completed history retained while the
  active successor pointer is explicit.

## Guardrail

`scripts/validate_post_v2_1_public_truth.py` derives identity from the roadmap
status, release policy, exact release record, manifest/evidence vectors, and
citation metadata. It rejects stale release or roadmap identity, commit or
archive disagreement, wrong rights tags, optional-format invention, multiple
active roadmap headers, and current-count drift. Its six required mutations
cover stale version, stale roadmap, wrong commit, false archive state, wrong
rights tag, and invented format approval.

## Deployment and attestation closure

Reconciliation source commit:
`bee209ad57c5181ffb1d63f6f22831e04364042f`.

- Build run
  [29139819267](https://github.com/corbensorenson/asi-stack-book/actions/runs/29139819267)
  passed the generated-scaffold check, deep 270-unit registry, 66-job Lean
  build, clean 67-page render, canonical-status build, Human-view validation,
  browser smoke, tested-artifact verification, and commit-bound upload.
- Deployment run
  [29139918614](https://github.com/corbensorenson/asi-stack-book/actions/runs/29139918614)
  downloaded and verified that successful artifact without rebuilding, deployed
  it, and passed the commit-bound public status/chapter-graph attestation.
- An independent public read returned HTTP 200 and the expected identity for
  nine surfaces: root, `/latest/`, Narrative, Architecture Reference, Evidence
  Registry, root canonical status, `/latest/` canonical status,
  `/versions/index.json`, and the immutable v2.1.0 archive.
- Both public status objects named source commit
  `bee209ad57c5181ffb1d63f6f22831e04364042f` and active version `v2.1.0`.
- The versions index retained the immutable v2.1.0 source commit and archive
  identity; it did not represent `/latest/` as immutable.

This closes P0 and M1. The roadmap as a whole remains active, and no empirical
program, residual, chapter claim, or optional format is completed by this gate.

## Non-claims

- This audit creates no chapter evidence and no support-state transition.
- Publication consistency does not prove model quality, safety, transfer, or
  the truth of any chapter claim.
- Internal validation is not external-human or institutional review.
- P0 publication attestation is not evidence for an empirical program.

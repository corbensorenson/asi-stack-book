# Post-v2.1 Public-Truth Audit

Audit date: 2026-07-10

Roadmap priority: P0 — Public truth reconciliation

State: local reconciliation complete; clean tested deployment and public
attestation pending

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

## Deployment closure still required

P0 does not close from this local audit alone. The exact source state must pass
the complete registry, Lean, HTML, and all-page/all-viewport browser gates; the
tested artifact must deploy without rebuilding; and the public root, `/latest/`,
canonical status object, product routes, and v2.1.0 release/archive links must
be re-read and attested. Until that happens, roadmap status remains active and
M1 remains in progress.

## Non-claims

- This audit creates no chapter evidence and no support-state transition.
- Publication consistency does not prove model quality, safety, transfer, or
  the truth of any chapter claim.
- Internal validation is not external-human or institutional review.
- Local reconciliation is not deployment or public attestation.

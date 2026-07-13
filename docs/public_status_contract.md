# Canonical Public Status Contract

Last updated: 2026-07-11

This contract makes the public state of **The ASI Stack** a generated object
instead of a collection of manually synchronized prose claims. It closes the
most urgent publication-truth failure identified in the external AI review:
source, rendered, and deployed surfaces could previously disagree while their
individual validators still passed.

## Source of Truth

`status/public_status_config.json` contains policy and the list of active public
status surfaces. It does not store changing counts. At build time,
`scripts/build_canonical_public_status.py` derives a complete record from:

- `book_structure.json` for parts, chapter order, titles, claim labels, support
  states, appendices, and expected page paths;
- `sources/source_inventory.json` for the source count;
- chapter prose through the same placement logic as
  `scripts/validate_external_sota_positioning.py` for in-prose external
  positioning;
- `claim_decisions/v1_x_core_claim_dispositions.json` and accepted evidence
  transition records for claim-disposition and transition counts;
- `editions/release_profiles.json` for a release-profile digest; and
- Git for the full source commit and clean/dirty tree state.

The output must satisfy
`schemas/canonical_public_status.schema.json`. The builder also enforces
cross-field invariants that JSON Schema cannot express compactly, including
chapter/order agreement, claim-distribution totals, and external-positioning
bounds.

## Deployment Object

Release automation writes the generated record to
`_site/status/canonical-public-status.json` after a clean Quarto render. The
tested-build workflow binds it and every rendered file into
`tested-site-bundle.json`; the separate deployment workflow verifies and
uploads that already-tested bundle without rebuilding. A release build fails unless
the record says `source_tree_state: clean` and `build_context: tested_commit`.
A locally generated record from a dirty worktree is intentionally labeled
`local_worktree`; it is useful for diagnosis but is not a release attestation.

The record identifies the latest immutable release and historical baseline
separately. `active_version` currently reports the completed `v2.2.0` release, while
`baseline_release` retains `v1.0.0` for compatibility with the original
baseline field. The completed post-v2.1 roadmap is preserved as execution history.
The active successor is `docs/post_v2_2_implementation_completion_roadmap.md`,
with machine state in `roadmap_records/post_v2_2_implementation_completion_status.json`. Later
root or `/latest/` commits remain mutable and are not part of the immutable
v2.2.0 tag unless they exactly match that tagged release.

## Contradiction and Render Gates

`scripts/validate_public_status_consistency.py` performs two layers of checks.

The source-layer contract is now generative as well as relational. Each
configured active prose surface contains one exact block emitted by
`public_status_summary_block`; scaffold synchronization refreshes it from the
canonical builder, and validation rejects missing, duplicate, stale, or
hand-edited blocks. Chapter headers are separately scanned to keep global
counts out of per-chapter metadata. The complete routing inventory is in
`docs/public_status_surface_inventory.md`.

Before render, it scans the active README, landing page, v1.0 status surface,
and publication-readiness surface for count-bearing claims. Those values must
match the generated canonical object, and each surface must contain its
configured required metrics. Built-in mutation controls prove that a stale
manifest count and a mismatched positioning ratio are rejected.

After render, the same validator checks that:

- the deployed status object matches the current commit and canonical counts;
- every manifest chapter has a rendered page;
- every chapter page has exactly one H1;
- sidebar chapter URLs, titles, and order exactly match the manifest; and
- sidebar chapter URLs and titles are unique.

After Pages deployment, a separate attestation job waits for the commit-bound
status object, then repeats the status, sidebar, chapter-URL, and H1 checks
against the public URL. The deployment may already have occurred if this final
attestation fails, so the workflow records that state as a failed release
workflow rather than pretending the stale or malformed deployment passed.

The build/deploy authority split and residual boundary are specified in
`docs/tested_artifact_deployment_contract.md`.

These checks are intentionally relational. Merely finding a required phrase is
not sufficient.

## Historical Scope

Numbers that describe an older release, consolidation snapshot, or curated
edition may differ legitimately from the active living-book manifest. Such
material must identify its scope in prose and use one of the configured
markers when it would otherwise resemble an active status assertion:

```html
<!-- canonical-status:historical -->
<!-- canonical-status:historical-begin -->
<!-- canonical-status:historical-end -->
```

The one-line marker exempts only its line. The begin/end pair scopes a block.
These markers do not make a false statement acceptable; they only tell the
active-count detector that the statement belongs to an explicitly versioned
historical surface.

## Versioned Deployment Channels

The root remains a compatibility URL and `latest/` is built as a complete
moving mirror before the tested bundle is hashed. `versions/index.json` is an
honest metadata ledger; immutable full-site bundles belong to tag-bound GitHub
Release assets with a release record, exact URL, and SHA-256. The v1.0.0 row
records its real immutable source release and explicitly says that no full
site bundle is published. See `docs/versioned_release_channels.md`.

## Non-Claims

- A clean tested commit proves repository and render coherence, not model
  quality, safety, security, or the book's chapter-core claims.
- Complete external positioning does not prove exhaustive literature coverage
  or reproduction of external results.
- Schema-valid status metadata does not approve a reader, research, PDF, EPUB,
  DOCX, or audio artifact.
- This contract creates no evidence transition and promotes no chapter-core
  support state.

## Commands

```bash
python3 scripts/validate_public_status_consistency.py
quarto render --to html
python3 scripts/build_canonical_public_status.py --output _site/status/canonical-public-status.json
python3 scripts/validate_public_status_consistency.py --site _site
```

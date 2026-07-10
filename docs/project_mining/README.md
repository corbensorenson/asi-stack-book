# Old AI Project Mining Program

Started: 2026-07-10

This directory is the public-safe control ledger for mining the historical AI
projects staged outside this repository. It records provenance, extraction
state, architectural findings, evidence boundaries, chapter decisions, and
storage-bloat analysis. It does not copy private source trees, model weights,
datasets, credentials, raw benchmark cases, or unreviewed artifacts into the
book repository.

## Source boundary

The read-only intake location is `/Users/corbensorenson/Documents/old projects
to mine`. Project sources remain outside the public book repository. A local
project may support planning and source notes after it is pinned to a stable
snapshot, but it does not become empirical evidence merely because code,
reports, or benchmark-shaped files exist.

## Current intake snapshot

| Intake item | State on 2026-07-10 | Apparent size | Mining state |
|---|---:|---:|---|
| `cca/` | populated Git worktree; pinned at `bd9afd16fe5b11c68f8c495f85ad117cc61ccfc8` | about 21.5 GiB after verified rebuildable-output cleanup | first deep dossier and source note recorded; symbol/artifact provenance pass remains |
| `moecot-manifest/` | populated Git worktree; pinned at `8398335bd01569d4bce7bc4ca2792d3ef48832f9` | about 29.3 GiB after verified cleanup and lossless flood-log archival | deep architecture/research dossier and source note recorded; contract/symbol and cross-project provenance passes remain |
| `BeastBrain/` | extracted source worktree; root Git history is unborn, so pinned by deterministic tree digest `60aa8121...` | about 0.5 GiB after rebuildable target cleanup | deep architecture, implementation-reality, failure-log, source-note, and provisional chapter-boundary dossier recorded; symbol-level cross-project provenance remains |
| `BugBrain/` | extracted Git worktree; content pinned at `d5ddd37966e2057e8b5ee7fa7bd8f4c833a30dc5` with extraction-induced mode-only drift | about 9.7 GiB after rebuildable/staging cleanup | deep architecture, implementation-reality, security, readiness, retained-report, and host-test dossier recorded; cross-project provenance remains |
| `corbens best model possible/` | extracted Git worktree | about 8.5 GiB after rebuildable/cache cleanup | ready; deep mining pending |
| `corbens-trainer/` | clean extracted Git worktree; pinned at `59a57333b819a64f2ed70c077c4dbdb917337b1c` | about 0.8 GiB after rebuildable target cleanup | deep control-plane, retained-artifact, failure, dataset, benchmark-authenticity, promotion-revocation, and checkpoint dossier recorded; Best Model and cross-project provenance remain |

All six currently visible projects are extracted. No further cleanup is in
scope after the user's 2026-07-10 direction to prioritize idea mining. The
intake directory should be rescanned before the program is closed because
additional archives may still be unzipping outside this task.

## Mining completeness gate

A project is only fully mined when all of the following are recorded:

1. Stable identity: archive fingerprint or Git commit, branch, extraction
   completeness, dirty-state caveat, and source-publication boundary.
2. Structural inventory: languages, manifests, packages/crates, docs, tests,
   formal artifacts, experiments, reports, datasets, models, and generated
   outputs.
3. Concept inventory: problems, claims, mechanisms, interfaces, invariants,
   failure modes, minimum implementations, mature endpoints, and terminology.
4. Evidence audit: implemented source surfaces, test/proof artifacts,
   source-reported results, contradictory records, missing replay inputs, and
   explicit non-claims.
5. Book crosswalk: deduplication against the live chapter spine, exact existing
   chapter targets, proposed new boundaries, source-note state, and promotion
   blockers.
6. Negative-lesson pass: abandoned mechanisms, false starts, contaminated or
   misleading metrics, operational failures, and project-governance lessons.
7. Bloat audit: rebuildable caches, environments, vendored mirrors, duplicated
   worktrees, generated evidence, model/checkpoint duplication, and reachable
   Git-history blobs.
8. Safe-reduction plan: estimated reclaim, preservation requirements,
   verification steps, and explicit separation between reversible cleanup and
   history-rewriting/destructive actions.

## Storage classifications

- **Rebuildable:** compiler targets, package caches, virtual environments,
  bytecode, and derived site/build output with pinned inputs.
- **Regenerable evidence:** repeated local smoke outputs and intermediate
  checkpoints whose producing source, configuration, seed, and retained
  summary are sufficient for deliberate replay.
- **Vendored:** external repositories, datasets, and models that have stable
  upstream identities and may be fetched again.
- **Historical:** Git objects, local task histories, worktrees, reports, and
  failed-run artifacts that may carry unique lineage even when they are large.
- **Unique source:** architecture documents, manifests, source code, schemas,
  tests, proof sources, accepted result summaries, and irreplaceable local
  research records.

No storage class authorizes deletion by itself. Cleanup requires a preservation
decision, an integrity check, and user approval for destructive or
history-rewriting actions.

## Project dossiers

- [Compiled Cognitive Architecture](cca.md)
- [MoECOT Manifest](moecot-manifest.md)
- [BeastBrain](beastbrain.md)
- [BugBrain](bugbrain.md)
- Corben's Best Model Possible — pending deep mining
- [Corben's Trainer](corbens-trainer.md)

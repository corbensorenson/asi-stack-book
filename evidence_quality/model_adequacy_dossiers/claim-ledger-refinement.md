# Model-adequacy dossier: Claim Ledger append-only refinement

## Ownership

- Chapter: `claim-ledgers-and-belief-revision`
- Frozen targets: all four `lean:claims.ledger.*` targets
- Stronger model: `lean/AsiStackProofs/ClaimLedgerRefinement.lean`
- Independent consumer: `scripts/validate_claim_ledger_refinement.py`
- Result: `experiments/claim_ledger_refinement/results/2026-07-15-local.json`
- Support-state effect: exactly `none`

## Reachable model

The model owns a single-claim append-only event lifecycle with exact base,
identity, semantic-version, ontology-version, support-view, history,
non-overwrite, dependency, migration, residual, and surface bindings. It
separates proposal validation, append authorization, materialized-view update,
and exact surface acknowledgment. It records an evidence owner's authored
decision but cannot create evidence authority, truth, an external effect, or a
release.

## Consequences, countermodels, and consumer

General consequences preserve claim identity and external-effect count across
every accepted step. An accepted append advances both ledger version and append
count exactly once and binds the new head to the event digest. Countermodels
reject stale bases, substituted events, ledger self-approval, upward movement
under open contradiction, missing evidence-owner receipt, overwritten history,
missing residual or dependency closure, unacknowledged ontology migration, and
incomplete surface acknowledgment. A concrete four-event witness reaches the
acknowledged state.

The independent consumer covers all seventeen routes, consumes the exact 5/7
revision fixtures and 1/11 five-project contradiction lifecycle, and rejects
29 mutations of identity, versions, heads, support custody, contradictions,
history, non-overwrite, reasons, residuals, dependencies, migration, surfaces,
event order, and acknowledgment.

## Assumptions, exclusions, and adequacy verdict

The event fields, evidence-owner receipt, digests, dependency closure,
migration receipt, and surface receipts are trusted inputs. Digest collision
resistance is not formalized. The model is adequate for the exact represented
lifecycle, route priority, append-only accounting, and authority separation.
It is inadequate for natural claim extraction, semantic equivalence,
assumption completeness, evidence or reviewer quality, contradiction and
dependency discovery, concurrent event-store behavior, natural multi-surface
repair, causal benefit, reproduction, transfer, SOTA, AGI, ASI, or chapter-core
support.

## Disposition

Retire the two assumption-restating projection bridges and replace the fourteen
finite baseline route theorems with the reachable lifecycle. Retain the four
small legacy preservation or contradiction lemmas as bounded reusable lineage.
All four public proof targets move to the refinement module; no support state
changes.

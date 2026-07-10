# Validation Registry and CI Tiers

Last updated: 2026-07-10

`validation/registry.json` is the sole declarative inventory and execution plan
for repository validation. It currently contains 238 ordered units and 734
required artifacts.
Every unit names an execution tier, validation class, input/output contract,
claim scope, negative-control status, and prohibited inference.

## Completed migration boundary

The registry owns required artifacts, unit commands, order, tiers, classes, and
contracts. `validate_book.py` is only the structural base gate: it loads its
required-file list from the registry and contains no child-validator command
inventory. `scripts/run_validation_registry.py` runs that base and then the
selected registry units in order. `scripts/build_validation_registry.py`
normalizes/checks the authoritative JSON; it no longer discovers commands by
parsing Python. `scripts/validate_validation_registry.py` rejects any return of
the legacy list, dispatcher, child-suppression environment, or dual authority.

## Tiers

- `pr` runs the base structural gate plus 21 fast publication, status,
  product, contribution, outline, proof-manifest, schema, and registry checks.
- `deep` includes PR checks and the 193 deeper fixture, proof/evidence,
  reader-preparation, replay, and artifact checks. Pages build uses this tier.
- `release` adds 24 format/application/release-candidate checks and is manual;
  it does not approve artifacts merely because the tier exists.

The workflows are separated accordingly:

- `.github/workflows/validate-pr.yml` handles pull requests;
- `.github/workflows/deep-validation.yml` handles scheduled/manual deep checks;
- `.github/workflows/major-release-validation.yml` handles manual major-edition
  preparation; and
- `.github/workflows/build-pages-artifact.yml` validates, builds, renders, and
  uploads the tested bundle; `.github/workflows/publish.yml` consumes that
  successful-run artifact without rebuilding and then attests the public site.

## Class semantics

The five classes are publication gates, schema/structure checks, behavioral
fixtures, reader-artifact gates, and proof/evidence gates. Class contracts make
the default epistemic limit explicit. A behavioral fixture, for example, is
scoped to the named fixture or local replay and cannot imply deployment,
transfer, broad correctness, safety, or chapter-core promotion.

Class metadata does not prove every validator is semantically adequate. The
registry records `validator_owned` where a script declares expected-invalid,
mutation, or negative controls and `not_declared` otherwise. Future review must
upgrade generic inherited contracts to exact per-unit artifact inputs and
outputs where that precision changes a claim or release decision.

The first high-impact audit is recorded in
`validation/unit_contract_overrides.json`. It replaces inherited descriptions
for status/deployment integrity, supply-chain pins, release channels and
deterministic immutable-site archive preparation,
evidence-quality and reviewer records, decision/review packets, product and
contribution focus, executable product projections, licensing provenance, the governed vertical slice and trace invariants, proof
manifest synchronization, schemas, publication, and registry integrity with
exact input artifacts, output assertions, negative controls, scope, and
prohibited inference. These remain internal contract audits, not independent
semantic review.

## Commands

```bash
python3 scripts/build_validation_registry.py --check
python3 scripts/validate_validation_registry.py
python3 scripts/run_validation_registry.py --tier pr
python3 scripts/run_validation_registry.py --tier deep
python3 scripts/run_validation_registry.py --tier release
```

No tier proves ASI, model quality, safety, security, or chapter claims. No tier
promotes support state without an accepted evidence transition, and release
tier availability does not approve an edition artifact.

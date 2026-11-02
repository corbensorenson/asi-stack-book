# Licensing Provenance and File-Routing Audit

Last updated: 2026-10-02

This provenance inventory supplies the technical file classification used by
the separately decided delayed-opening policy. It began on July 10 before the
decision and release routing were completed. The current authority is
`LICENSE.md` together with the exact tagged rights-routing records; this
inventory itself grants no rights and does not establish ownership.

## Scope and method

`scripts/build_licensing_provenance_inventory.py` enumerates the exact
`v2.3.0` tree with `git ls-tree -r --name-only -z v2.3.0` when the tag is
available. Its pre-tag fallback enumerates tracked files and untracked,
non-ignored candidates with `git ls-files --cached --others --exclude-standard -z`.
The retained inventory covers 4,144 tagged paths, not today's uncommitted
working tree. Ordered declarative
rules in `licensing/provenance_policy.json` assign every path an artifact class,
provenance-review state, prospective lane, current legal effect, and blocking
reason. The inventory records a digest of the complete path set and policy.

The rules deliberately distinguish:

- the operative license document;
- external-source commentary and compilations;
- Corben-supplied, local-project, and source-corpus records;
- historical and generated derivatives;
- experiment fixtures, imported results, and review records;
- software, proofs, schemas, tests, and automation;
- figures and binary assets;
- book and project prose;
- public metadata and governance records; and
- unknown paths that must remain quarantined.

No rule uses `provenance_cleared`. Author-created-looking material remains
`author_ownership_assertion_required`; external, supplied, local-project,
historical, generated, and imported material carries stronger mixed-rights or
provenance review blockers.

## What this unblocks

The original audit supplied a deterministic path list for the author decision
and subsequent exact release routing. The current decision is recorded in
`governance/licensing_decision.json`; exact tagged grants and exclusions are
recorded separately. Later or changed files need their own applicable routing.

The original checklist below describes decisions and review authority; it is
not a claim that the implemented tagged policy remains undecided. New routing
or policy changes still require the corresponding authority:

1. assert authorship/ownership for candidate prose, software, metadata, and
   figures;
2. inspect quotations, copied snippets, source-derived descriptions, fonts,
   icons, AI-generation terms, and imported local-project records;
3. decide inbound contribution terms;
4. quarantine or separately license mixed files;
5. choose the outbound policy and effective version/date; and
6. implement exact license texts, notices, file routing, and release snapshots
   atomically.

## Validation and rejection controls

`scripts/validate_licensing_provenance_inventory.py` regenerates the inventory,
checks complete tagged path coverage and schemas, requires the decided
delayed-opening policy, preserves the inventory's non-grant effects, and verifies that external source notes and
assets remain in review lanes. Four controls reject an omitted path, automatic
clearance, external-source metadata laundering, and a premature outbound
license effect.

On October 2 the standard schema engine exposed obsolete constants that still
required an undecided policy. The two schemas now accept the retained initial
state and the exact already implemented tagged policy. Semantic validation
still requires the current decided state, deterministic inventory and four
rejecting controls. Neither the operative license, decision, final routing nor
any release snapshot was changed by this compatibility repair.

This audit is not legal advice, a license grant, an ownership determination, a
contributor agreement, or permission to reuse any repository material.

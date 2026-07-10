# Licensing Provenance and File-Routing Audit

Last updated: 2026-07-10

This audit completes the technical file-inventory prerequisite in the split
license decision packet without selecting a license or asserting ownership.
`LICENSE.md` remains operative and all rights remain reserved.

## Scope and method

`scripts/build_licensing_provenance_inventory.py` enumerates tracked files and
untracked, non-ignored release candidates with
`git ls-files --cached --others --exclude-standard -z`. Ordered declarative
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

The author and a qualified reviewer can now work from a complete deterministic
path list instead of an undefined future audit. They can resolve one class or
exception at a time, record evidence, and then decide whether a permissive,
controlled, delayed, or reserved policy is appropriate.

The following work still requires human authority or qualified advice:

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
checks complete path coverage and schemas, preserves the empty author decision
and all-rights-reserved effect, and verifies that external source notes and
assets remain in review lanes. Four controls reject an omitted path, automatic
clearance, external-source metadata laundering, and a premature outbound
license effect.

This audit is not legal advice, a license grant, an ownership determination, a
contributor agreement, or permission to reuse any repository material.

# Three Product Contracts

Last updated: 2026-07-26

**The ASI Stack** is one canonical research source tree projected into three
different products. Treating those products as one interface made the landing
page administratively heavy, made the chapter template tiring for continuous
reading, and made “the book” ambiguous during release review.

The machine contract is `products/product_contracts.json`. It binds each
product to an audience, reader question, entry points, content layers,
navigation and density rules, release profile, current status, review gate, and
forbidden inference.

## Narrative technical book

The narrative product answers: what is the architecture, why does it matter,
and how do its pieces fit together? Its generated entry is a 22-unit
thesis-to-method route over the complete 84-chapter reference, and each
representative chapter opens in Human view. Every
selected chapter has three deliberately separate claim projections—a
plain-language thesis, normative engineering rule, and bounded machine
contract—plus one reader question, running example, strongest objection,
failure story, evidence-changing condition, and canonical core-claim reference.
The machine contract must carry an explicit noninheritance boundary; it cannot
silently turn the readable thesis into stronger evidence, authority, readiness,
or release language.
It hides live status, test plans, proof-hook inventories, source crosswalks, and
repeated support boilerplate.

`products/narrative_unit_crosswalk.json` assigns every canonical chapter to
exactly one unit. The representative chapter does not absorb the claims or
evidence of its routed specialist owners; the crosswalk is navigation and
coverage control. The generated narrative page makes that relationship
reader-visible: each unit lists and directly links every specialist owner,
while sole-owner units say so explicitly.

The route and Human view are convenience projections. They are not the reviewed reader release.
A reader artifact still needs continuity, editorial, accessibility, figure,
and format-specific review plus an edition release record.

## Architecture reference specification

The reference product answers: what are the responsibilities, interfaces,
states, invariants, failure routes, and implementation horizons? Its generated
84-chapter index preserves canonical order and routes to each chapter in
AI/research view, supported by protocol schemas, implementation horizons,
glossary terms, formal hooks, and executable test plans.

The reference retains technical density that helps implementation. Evidence
totals and artifact inventories route to the registry so architecture prose
does not become a repeated dashboard. A complete reference record does not
establish deployed enforcement or system quality.

## Evidence, proof, and release registry

The registry answers: what is actually supported, by which source or artifact,
under what scope, and with which residuals? Its generated index begins with the
canonical public status, then routes to Appendix C, source-ownership appendices,
test and proof ledgers, release records, the changelog, and residual-specific
reports. Repository-backed records are published as content-addressed snapshots.

The registry prefers exact IDs, digests, commands, negative controls,
support-state effects, and non-claims. Record count, schema validity, and
validator success do not prove the architecture or chapter claims.

## Shared source and release rule

The products do not fork the canonical manuscript. The live source remains
authoritative; product projections may omit detail but may not omit uncertainty
that changes claim meaning. Availability, artifact approval, and support-state
evidence remain separate states. The product contracts change navigation and
review ownership only and promote no chapter-core claim.

The executable build, snapshot, and validation boundary is documented in
`docs/product_projection_artifacts.md`.

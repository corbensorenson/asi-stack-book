# Chapter Consolidation Dry Run: Constitutional Alignment And Agency

Last updated: 2026-06-29

This is the first dry-run merge package required by
`docs/v1_x_beyond_sota_roadmap.md` and
`docs/chapter_consolidation_pilot_plan.md`. It is a review artifact only. It
does not edit `book_structure.json`, delete a chapter, change a URL, rewrite a
chapter, change source mappings, change proof targets, change support states,
or approve a reader artifact.

Dry-run destination:
`constitutional-alignment-substrate`, retitled **Constitutional Alignment:
Agency, Dignity, and Corrigibility**.

Source chapters:

- `constitutional-alignment-substrate`
- `agency-dignity-and-corrigibility`

Continuity decision: keep `constitutional-alignment-substrate` as the public
continuity ID if this merge later proceeds. Treat
`agency-dignity-and-corrigibility` as a folded source chapter whose claim,
proof hooks, tests, reader path, and source mappings become named sections,
subclaims, and history records in the destination chapter.

## Non-Actions

- No manifest edit has been made.
- No chapter file has been removed or rewritten.
- No source note, external source, proof target, test result, or support state
  has changed.
- No claim is promoted above `argument`.
- No external comparator is treated as proving ASI Stack runtime behavior.
- No reader, EPUB, DOCX, PDF, or audio artifact is approved by this package.

## Proposed `book_structure.json` Diff

This proposed `book_structure.json` diff is illustrative and unapplied. If the
merge is later executed, apply one pilot merge in one commit, then regenerate
and validate every generated surface.

```diff
@@ Part I - Foundations, Alignment, and Governance
 {
   "id": "constitutional-alignment-substrate",
-  "title": "Constitutional Alignment Substrate",
+  "title": "Constitutional Alignment: Agency, Dignity, and Corrigibility",
   "file": "chapters/constitutional-alignment-substrate.qmd",
   "status": "conceptual",
   "evidence_level": "argument",
   "claim_label": "Design rationale",
   "source_ids": [
     "alignment_field",
     "field_of_god",
     "ethica_mechanica",
     "eternal_code",
     "coherence_exchange",
     "spinoza",
     "field_of_god_ai_constitution"
   ],
-  "problem": "The stack needs a normative substrate that constrains goals, plans, execution, and self-modification.",
-  "insufficient": "Reactive refusal policies do not define value continuity, moral uncertainty, agency preservation, anti-domination, or self-modification ethics.",
-  "core_claim": "Alignment should function as a constitutional substrate whose commitments are operationalized as constraints on plans and system changes.",
+  "problem": "The stack needs a constitutional substrate whose protected constraints remain usable in the human-facing rights and correction interfaces where optimization can become domination.",
+  "insufficient": "Reactive refusal policies and harm-only safety frames do not preserve value continuity, agency, dignity, corrigibility, anti-domination, contestability, or self-modification ethics under operational pressure.",
+  "core_claim": "Alignment should function as a constitutional substrate whose protected predicates encode agency, dignity, corrigibility, contestability, and correction paths as operational constraints on plans and system changes.",
   "minimal_implementation": "A compact constitution with operational predicates, open moral uncertainties, and scenario tests.",
-  "beyond_state_of_art": "A real constitutional layer acts as a constraint compiler for plans, tools, memory, routing, and self-improvement..."
+  "minimal_implementation": "A compact constitution plus an agency-rights checklist, with fixtures for protected predicates, review routes, rights usability, rollback, appeal, and self-modification weakening.",
+  "beyond_state_of_art": "A mature constitutional layer compiles protected commitments into plan, tool, memory, routing, human-control, and self-improvement gates while keeping correction, refusal, appeal, rollback, explanation, and accountable delegation materially available."
 }
-
-{
-  "id": "agency-dignity-and-corrigibility",
-  "title": "Agency, Dignity, and Corrigibility",
-  "file": "chapters/agency-dignity-and-corrigibility.qmd",
-  ...
-}
```

Manifest notes:

- The proposed Corben/local `source_ids` union is already present on
  `constitutional-alignment-substrate`: `alignment_field`, `field_of_god`,
  `ethica_mechanica`, `eternal_code`, `coherence_exchange`, `spinoza`, and
  `field_of_god_ai_constitution`.
- If the merge proceeds, remove only the `agency-dignity-and-corrigibility`
  chapter object after all claim, source, proof, reader, and handoff
  reconciliation steps pass.
- Run `python3 scripts/chapter_adjacency_report.py --if-removing
  agency-dignity-and-corrigibility` before editing the manifest. The current
  report says the destination chapter Handoff must name `Moral Uncertainty and
  Value Conflict` after the fold.

## Destination Section Outline

The merged chapter should use one chapter skeleton, not two pasted skeletons.

Recommended section sequence:

1. Chapter status: one status block with merged open evidence gaps.
2. Drafting guardrail: constitutional language is a runtime constraint design
   surface, not moral proof or deployed safety.
3. Human Reading Path: start from the reader question, "What must remain
   available to people when a powerful system acts?"
4. Problem: the stack needs protected constitutional commitments that remain
   available as human-facing correction, refusal, review, appeal, rollback,
   consent, explanation, delegation, exit, and audit paths.
5. Why existing approaches are insufficient: reactive refusal filters and
   harm-only safety frames miss continuity, domination, dependency,
   corrigibility collapse, value smuggling, and rights theater.
6. Core Claim: use the merged core claim below.
7. Claim-source mapping status: one table that separates constitutional
   predicate lineage from agency-rights lineage and keeps all support at
   `argument`.
8. Mechanism:
   - constitutional translation record;
   - predicate scope, conflict behavior, and migration policy;
   - agency-rights checklist attached to high-impact plans;
   - material-usability states for rights under pressure;
   - corrigibility as preserved correction, appeal, rollback, shutdown, audit,
     and update paths after transitions;
   - constitutional migrations for changes to protected predicates;
   - non-claim boundaries for metaphysics, moral correctness, deployed policy,
     reviewer quality, and social legitimacy.
9. Interfaces:
   - Constitutional Predicate Record;
   - Agency Rights Checklist;
   - constitutional change record;
   - plan, runtime, governance, evidence, and self-improvement handoffs.
10. Invariants:
    - dignity and agency constraints remain visible;
    - corrigibility cannot be optimized away;
    - speculative metaphysics stays labeled;
    - rights count only when materially usable before relevant effects;
    - denied or degraded rights produce residuals;
    - protected predicate changes require migration, review, and rollback.
11. Failure modes:
    - mystical framing replacing technical constraints;
    - power without care;
    - self-modification weakening protected commitments;
    - predicate drift;
    - conflict-default capture;
    - dependency lock-in;
    - covert manipulation;
    - rights theater;
    - late remedy laundering.
12. Minimum Viable Implementation: combine `constitutional_predicate_record`
    and `agency_rights_checklist` fixture suites. The MVI should require at
    least one protected-predicate weakening rejection, one predicate conflict
    routed to review, one high-impact action blocked for missing usable review,
    one degraded-right residual, and one accountable rollback/appeal path.
13. Beyond the State of the Art: describe a constitutional constraint compiler
    that binds plans, tools, memory, routes, human-control surfaces, and
    self-improvement, while keeping human correction paths materially usable.
    Preserve the claim boundary that this is an architectural endpoint, not a
    demonstrated deployed system.
14. Codex test plan: union the existing constitutional-alignment and
    agency-rights tests without claiming broader evidence.
15. Formalization hooks: keep both Lean modules and all four proof tags.
16. Source crosswalk: union Corben/local sources and external comparators.
17. Summary: one synthesis of predicate translation and human-facing rights.
18. Handoff: route directly to `moral-uncertainty-and-value-conflict`.

## Appendix C Row Plan

Proposed merged core row:

| Row | Chapter | Claim label | Support state | Source effect |
|---|---|---|---|---|
| `constitutional-alignment-substrate.core` | `constitutional-alignment-substrate` | Design rationale | argument | Union the source mappings from both source chapters; keep limits and passage-review notes. |

Proposed merged core claim:

> Alignment should function as a constitutional substrate whose protected
> predicates encode agency, dignity, corrigibility, contestability, and
> correction paths as operational constraints on plans and system changes.

Claim-history treatment for the folded source chapter:

| Existing row | Treatment if merge proceeds | Boundary |
|---|---|---|
| `constitutional-alignment-substrate.core` | Retain as the destination core row with merged text. | Support remains `argument`. |
| `agency-dignity-and-corrigibility.core` | Redirect to destination as a preserved subclaim and section family: agency, dignity, material usability, corrigibility, appeal, rollback, refusal, exit, audit, and accountability. | Do not silently delete; record the fold in changelog and any claim-decision/history surface required by validators. |

No-support-state-change language:

- The merged chapter remains `Design rationale` + `argument`.
- Existing synthetic harnesses and Lean records are bounded finite-record
  evidence only.
- External constitutional-AI, corrigibility, and off-switch sources are
  comparators and prior art, not reproduction evidence and not support-state
  promotion.

## Source Union

Corben/local source union:

- `alignment_field`
- `field_of_god`
- `ethica_mechanica`
- `eternal_code`
- `coherence_exchange`
- `spinoza`
- `field_of_god_ai_constitution`

Current source-note state to preserve:

- `alignment_field`, `field_of_god`, `ethica_mechanica`, `eternal_code`, and
  `field_of_god_ai_constitution` carry reviewed passage references for both
  chapters where applicable.
- `spinoza` carries reviewed passage references for the constitutional
  substrate.
- `coherence_exchange` remains connector-only/source-note mapped.

External-source union:

- `ext_constitutional_ai_2022`
- `ext_collective_constitutional_ai_2024`
- `ext_corrigibility_2015`
- `ext_off_switch_game_2016`

If the merge proceeds:

- preserve all four external records in Appendix H through
  `sources/source_inventory.json` and their source notes;
- update chapter targets and source-note supported-chapter lists only through
  the normal inventory/source-note workflow;
- keep `docs/chapter_external_grounding_status.md` and
  `docs/external_sota_positioning_audit.md` generated and validated;
- do not cite any new external source in prose until its source note exists.

## Lean Module And Proof-Manifest Treatment

Keep both Lean modules:

- `AsiStackProofs.Alignment`
- `AsiStackProofs.Corrigibility`

Keep all four proof tags:

- `lean:alignment.constitution.operational_invariant`
- `lean:alignment.constitution.failure_blocks_promotion`
- `lean:corrigibility.agency.operational_invariant`
- `lean:corrigibility.agency.failure_blocks_promotion`

Proof-manifest rule:

- If the source chapter is removed from `book_structure.json`, move the
  corrigibility proof targets into the destination chapter's outline table
  before running `python3 scripts/sync_proof_manifest.py`.
- Do not retire `AsiStackProofs.Corrigibility` merely because the chapter
  skeleton is folded. The module owns a distinct rights/correction-pathway
  record family.
- Keep limitation prose explicit: these proofs express finite-record gates and
  small derived review-route theorems. They do not prove moral correctness,
  deployed alignment, runtime corrigibility, consent quality, material rights
  usability, reviewer independence, or institutional adequacy.

## Test, Schema, And Harness Rows To Move

Preserve the constitutional-alignment harness lane:

- `docs/constitutional_alignment_harness.md`
- `scripts/validate_constitutional_alignment.py`
- `experiments/constitutional_alignment/results/2026-06-28-local.md`
- existing `constitutional_predicate_record` fixtures and schema/example
  validation

Preserve the agency-rights harness lane:

- `docs/agency_rights_harness.md`
- `scripts/validate_agency_rights.py`
- `experiments/agency_rights/results/2026-06-28-local.md`
- existing `agency_rights_checklist` fixtures and schema/example validation

No new result is created by this dry run. If the manifest merge proceeds, the
destination chapter's test plan should report both harness families with their
existing non-claims, and generated Appendix E should retain both test families.

## Reader Path, Handoff, And Review Repairs

Human Reading Path repair:

- Replace the current two separate Human Reading Paths with one lead-in that
  starts from constitutional constraints and immediately explains why
  correction, refusal, review, appeal, rollback, exit, audit, and accountability
  must remain materially usable.
- Do not keep two separate reader openings that repeat the same live scaffold.

Handoff repair:

- `chapters/human-intent-as-a-formal-input.qmd` should hand off to
  **Constitutional Alignment: Agency, Dignity, and Corrigibility**.
- The merged destination chapter should hand off to **Moral Uncertainty and
  Value Conflict**.
- The current `python3 scripts/chapter_adjacency_report.py --if-removing
  agency-dignity-and-corrigibility` output confirms this repair path.

Reader-overlay and reader-review treatment:

- No current reader overlay file exists for either source chapter.
- `docs/reader_chapter_review_matrix.md` currently lists both chapters as
  reviewed; a manifest merge would require regenerating or revising the review
  matrix so the folded chapter does not appear as a rendered current chapter.
- Any curated reader graduation should wait until this merge decision is
  executed or explicitly deferred, because polishing two repeated reader
  chapters would preserve the avoidable skeleton duplication this dry run is
  meant to remove.

## MVI And Beyond-SOTA Merge

Merged Minimum Viable Implementation:

> A compact constitution plus an agency-rights checklist. The MVI validates
> `constitutional_predicate_record` and `agency_rights_checklist` fixtures,
> including protected predicates, review routes, rights material-usability
> states, rollback/appeal handles, degradation residuals, and
> self-modification weakening rejection. It starts the idea honestly without
> claiming deployed constitutional alignment, moral correctness, human-control
> adequacy, or runtime rights preservation.

Merged Beyond-SOTA endpoint:

> A constitutional constraint compiler binds protected commitments to plans,
> tools, memory, routing, human-control surfaces, and self-improvement. The
> mature endpoint keeps correction, refusal, appeal, rollback, explanation,
> consent, delegation, exit, audit, and accountable repair materially available
> under operational pressure. It records predicate migrations, rights
> degradation, reviewer limitations, residual uncertainty, and rollback paths
> before downstream layers can treat a change as safe. This remains a target
> architecture until public-safe traces, stronger proofs, review evidence, and
> runtime artifacts justify narrower support-state transitions.

## URL, Redirect, And Retired-File Policy

Default policy for this pilot:

- Keep `chapters/constitutional-alignment-substrate.qmd` as the rendered URL.
- If the merge proceeds, remove `agency-dignity-and-corrigibility` from
  `book_structure.json` only after a redirect or historical-note policy is
  chosen.
- Do not preserve a stale rendered page for the retired chapter unless the
  project adds a deliberate redirect mechanism.
- Keep git history as the archive for the retired chapter file; do not delete
  source history or proof/history records.

## Expected Generated-File Updates If Applied

If this dry run becomes an actual manifest merge, expect updates to:

- `_quarto.yml` through `python3 scripts/sync_scaffold.py`;
- `docs/book_outline.md`;
- `proofs/proof_manifest.json`;
- `appendices/C_claim_evidence_matrix.qmd`;
- `appendices/E_codex_test_specs.qmd`;
- `appendices/F_changelog.qmd`;
- `appendices/K_implementation_horizons.qmd`;
- `docs/chapter_external_grounding_status.md`;
- `docs/external_sota_positioning_audit.md`;
- `docs/reader_chapter_review_matrix.md`;
- any reader-manuscript or overlay manifests that list current chapter IDs.

## Validation Commands Before Any Real Merge Commit

Run at minimum:

```bash
python3 scripts/chapter_adjacency_report.py --if-removing agency-dignity-and-corrigibility
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_chapter_consolidation_pilot_plan.py
python3 scripts/validate_chapter_handoffs.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_reader_overlays.py --check
python3 scripts/validate_reader_manuscript_manifest.py
python3 scripts/validate_chapter_external_grounding_status.py
python3 scripts/validate_external_sota_positioning.py --release
python3 scripts/validate_book.py
(cd lean && lake build)
quarto render --to html
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

## Open Review Questions

- Should the merged title be the long title above, or should the chapter retain
  the shorter rendered title while the section headings carry agency,
  dignity, and corrigibility?
- Should `agency-dignity-and-corrigibility.qmd` remain in the repository as an
  unrendered historical file after manifest removal, or should a redirect
  mechanism be added first?
- Should `ext_corrigibility_2015` and `ext_off_switch_game_2016` become direct
  manifest `source_ids` for the destination chapter, or remain external
  grounding records attached through inventory/source-note status?
- Should a future proof-depth pass combine the Alignment and Corrigibility
  theorem statements through an explicit shared record, or keep the modules
  separate but referenced by one chapter?


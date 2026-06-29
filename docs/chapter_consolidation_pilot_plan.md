# Chapter Consolidation Pilot Plan

Last updated: 2026-06-29

This plan is the first governed consolidation pilot for the v1.x roadmap. It
does not edit `book_structure.json`, remove chapters, change URLs, change
source mappings, change proof targets, change support states, or approve a
reader artifact. It exists so the highest-overlap cluster can be reconciled
before any manifest merge.

Pilot cluster: Part I alignment/governance philosophy.

Reason for selecting this cluster: the four chapters share overlapping source
families, repeated constitutional/governance skeletons, and safety-critical
Lean hooks. Consolidating them is likely to reduce repetition while making the
normative control story deeper, but only if claim identity and proof coverage
are preserved.

## Proposed Shape

| Proposed chapter | Source chapters | Proposed stable-ID policy | Purpose |
|---|---|---|---|
| `constitutional-alignment-substrate` retitled **Constitutional Alignment: Agency, Dignity, and Corrigibility** | `constitutional-alignment-substrate`; `agency-dignity-and-corrigibility` | Prefer keeping `constitutional-alignment-substrate` as the public continuity ID; retire or redirect the agency chapter only after handoffs and reader overlays are reconciled. | One chapter explains how constitutional predicates encode agency, dignity, corrigibility, appeal, and correction paths as operational constraints. |
| `moral-uncertainty-and-value-conflict` retitled **Moral Uncertainty, Value Conflict, and Contestable Governance** | `moral-uncertainty-and-value-conflict`; `governance-rights-fork-exit-and-audit` | Prefer keeping `moral-uncertainty-and-value-conflict` as the public continuity ID; retire or redirect the governance-rights chapter only after handoffs and reader overlays are reconciled. | One chapter explains unresolved value conflict and the fork, exit, audit, dissent, appeal, and contestability interfaces that keep conflict governable. |

## Claim Reconciliation

### Constitutional Alignment: Agency, Dignity, and Corrigibility

Proposed merged core claim:

> Alignment should function as a constitutional substrate whose protected
> predicates encode agency, dignity, corrigibility, contestability, and
> correction paths as operational constraints on plans and system changes.

Preserved source chapter claims:

- `constitutional-alignment-substrate`: Alignment should function as a
  constitutional substrate whose commitments are operationalized as constraints
  on plans and system changes.
- `agency-dignity-and-corrigibility`: A governed ASI stack should preserve
  human agency, dignity, corrigibility, and contestability as engineering
  requirements.

Preserved subclaim sections:

- protected constitutional predicates;
- predicate migration and self-modification weakening;
- agency and dignity as usability constraints, not slogans;
- correction, appeal, interruption, and high-impact review paths;
- least-sufficient-power behavior;
- non-claims about legal rights, deployed corrigibility, or validated
  institutional governance.

Source IDs to preserve by union:

- `alignment_field`
- `field_of_god`
- `ethica_mechanica`
- `eternal_code`
- `coherence_exchange`
- `spinoza`
- `field_of_god_ai_constitution`

Lean hooks to preserve:

- `lean:alignment.constitution.operational_invariant`
- `lean:alignment.constitution.failure_blocks_promotion`
- `lean:corrigibility.agency.operational_invariant`
- `lean:corrigibility.agency.failure_blocks_promotion`

External grounding to preserve or improve:

- `agency-dignity-and-corrigibility` currently carries
  `ext_corrigibility_2015` and `ext_off_switch_game_2016`.
- `constitutional-alignment-substrate` now carries source-noted constitutional
  comparators: `ext_constitutional_ai_2022` and
  `ext_collective_constitutional_ai_2024`.
- The merged chapter should keep the corrigibility/off-switch comparators, keep
  the Constitutional AI/public-input comparators, and continue mining the
  constitutional-alignment source queue for fair AI governance and
  normative-control baselines without claiming reproduced training or deployed
  constitutional enforcement.

### Moral Uncertainty, Value Conflict, and Contestable Governance

Proposed merged core claim:

> Value conflicts should be represented as explicit unresolved obligations,
> residuals, review paths, and bounded decisions, with fork, exit, audit,
> dissent, and contestability preserved as technical governance interfaces.

Preserved source chapter claims:

- `moral-uncertainty-and-value-conflict`: Value conflicts should be represented
  as explicit unresolved obligations, review paths, and bounded decisions rather
  than hidden inside reward functions.
- `governance-rights-fork-exit-and-audit`: Fork, exit, audit, dissent, and
  contestability should be treated as technical governance interfaces, not only
  political ideals.

Preserved subclaim sections:

- unresolved protected conflicts and residual conflict records;
- high-stakes conflict review and revisit paths;
- dissent preservation and bounded decisions;
- fork, exit, audit, redaction, appeal, and contestability interfaces;
- audit-preserving redaction and constrained fork obligations;
- non-claims about solving moral uncertainty, legal rights, deployed
  governance, or institutional adequacy.

Source IDs to preserve by union:

- `ethica_mechanica`
- `alignment_field`
- `coherence_exchange`
- `uat`
- `spinoza`
- `field_of_god_ai_constitution`
- `ladon_manhattan`

Lean hooks to preserve:

- `lean:values.conflict.operational_invariant`
- `lean:values.conflict.failure_blocks_promotion`
- `lean:governance.rights.operational_invariant`
- `lean:governance.rights.failure_blocks_promotion`

External grounding to preserve or improve:

- `governance-rights-fork-exit-and-audit` currently carries
  `ext_corrigibility_2015` and `ext_off_switch_game_2016`.
- `moral-uncertainty-and-value-conflict` now carries source-noted comparators:
  `ext_reinforcement_learning_moral_uncertainty_2020` and
  `ext_contestable_ai_design_2022`.
- The merged chapter should keep the corrigibility/off-switch comparators, keep
  the moral-uncertainty and contestable-AI comparators, and continue mining the
  moral-uncertainty and governance source queues for fair social-choice,
  deliberative-review, and contestable-governance baselines without claiming a
  solved moral theory or deployed institutional adequacy.

## Manifest Merge Steps

Do these only after this plan is reviewed:

1. Run `python3 scripts/chapter_adjacency_report.py --chapter <id>` for all
   four source chapters and save the handoff repair queue.
2. Produce a dry-run merge package before editing `book_structure.json`.
3. Edit `book_structure.json` only after the dry-run package is reviewed, and
   represent one pilot merge at a time, not both at once.
4. Preserve the destination chapter's stable ID unless a stronger public URL
   reason justifies a new slug.
5. Union `source_ids`; do not drop any source ID unless a source note or claim
   decision records why it no longer belongs.
6. Union proof targets and keep both Lean modules referenced unless a proof
   target is explicitly retired.
7. Rewrite the merged chapter with one chapter skeleton and named sub-sections,
   not two pasted skeletons.
8. Update `docs/book_outline.md`, Human Reading Path prose, Handoff sections,
   reader overlays, reader review matrices, Appendix C, Appendix K, proof
   manifests, external-grounding status, external-SOTA positioning, and the
   changelog.
9. Run the full local validation and render gate before committing.

## Dry-Run Merge Package

The first pilot deliverable should be a reviewable package, not an immediate
manifest edit. It should include:

- proposed `book_structure.json` diff for only one destination chapter;
- destination chapter section outline with one Problem/Insufficiency/Mechanism
  skeleton and named sub-sections for preserved ideas;
- Appendix C row plan: one merged core claim, preserved subclaims, retired or
  redirected claim rows, and no-support-state-change language;
- source union and external-source union;
- Lean module/proof-manifest treatment, including both existing modules unless
  a proof target is explicitly retired with a reason;
- test, schema, or harness rows that must move with the chapter;
- Human Reading Path, Handoff, reader-overlay, and reader-review changes;
- MVI and Beyond-SOTA implementation-horizon merge;
- URL, redirect, and retired-file policy;
- validation commands and expected generated-file updates.

## No-Action Decisions For This Pilot

- Do not merge any Circle, coil, Theseus, execution-artifact, or recursive
  self-improvement chapters in this pilot.
- Do not target a fixed final chapter count.
- Do not delete source notes, Lean modules, proof tags, claim history, or reader
  review records.
- Do not promote any chapter core claim.
- Do not claim that reduced repetition is itself evidence.

## Open Questions Before Manifest Edits

- Should destination slugs stay stable even when the displayed title changes?
  Default answer for the pilot: yes.
- Should retired chapter files remain as non-rendered historical stubs or be
  removed after manifest deletion? Default answer for the pilot: keep the public
  git history, but do not preserve stale rendered pages unless a redirect
  mechanism is added.
- Should the two proposed merges happen in one commit or two? Default answer for
  the pilot: two commits, one merge at a time.
- Which additional external comparator families are needed before prose merge?
  Default answer: mine and source-note them first; do not invent citations in
  the merged chapter, and do not treat existing comparators as proof that the
  merged governance mechanisms work.

## Validation

This plan, both dry-run packages, and the decision review,
`docs/chapter_consolidation_dry_run_constitutional_alignment.md` and
`docs/chapter_consolidation_dry_run_contestable_governance.md`, and
`docs/chapter_consolidation_decision_review.md`, are checked by
`python3 scripts/validate_chapter_consolidation_pilot_plan.py`.

Current dry-run package status:

- `docs/chapter_consolidation_dry_run_constitutional_alignment.md` records the
  proposed merge package for `constitutional-alignment-substrate` plus
  `agency-dignity-and-corrigibility`.
- It records an illustrative, unapplied manifest diff; one-skeleton destination
  outline; Appendix C row plan; source and external-source unions; Lean module
  and proof-manifest treatment; test/harness rows; reader and handoff repairs;
  MVI and Beyond-SOTA merge; URL/retired-file policy; generated-file updates;
  validation commands; and open review questions.
- `docs/chapter_consolidation_dry_run_contestable_governance.md` records the
  proposed merge package for `moral-uncertainty-and-value-conflict` plus
  `governance-rights-fork-exit-and-audit`.
- It records an illustrative, unapplied manifest diff; one-skeleton destination
  outline; Appendix C row plan; source and external-source unions; Lean module
  and proof-manifest treatment; test/harness rows; reader and handoff repairs;
  MVI and Beyond-SOTA merge; URL/retired-file policy; generated-file updates;
  validation commands; and open review questions.
- Neither package edits the manifest or authorizes a merge.
- `docs/chapter_consolidation_decision_review.md` records the current decision:
  defer manifest consolidation for this v1.x cycle, proceed with reader
  curation outside the pending Part I merge cluster, and require human or
  external review plus a reviewed destination chapter draft before executing
  either merge.

## Non-Claims

- This plan does not merge chapters.
- This plan does not change `book_structure.json`.
- This plan does not change any support state.
- This plan does not create source-derived, proof-derived, external-review, or
  test-derived evidence.
- This plan does not approve the human-reader manuscript, EPUB, DOCX, PDF, or
  audio artifacts.

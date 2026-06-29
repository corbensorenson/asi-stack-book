# Chapter Consolidation Dry Run: Verification And Adversarial Review

Last updated: 2026-06-29

This is a non-pilot dry-run package required by
`docs/v1_x_beyond_sota_roadmap.md` and
`docs/chapter_consolidation_sequence.md`. It is a review artifact only. It
does not edit `book_structure.json`, delete a chapter, change a URL, rewrite a
chapter, change source mappings, change proof targets, change support states,
or approve a reader artifact.

Dry-run destination:
`spinoza-verification-and-proof-carrying-claims`, retitled
**Proof-Carrying Claims and Adversarial Review**.

Source chapters:

- `spinoza-verification-and-proof-carrying-claims`
- `unified-adaptive-tribunal-and-adversarial-review`

Related chapter not merged by this package:

- `claim-ledgers-and-belief-revision`

Continuity decision:

- Keep `spinoza-verification-and-proof-carrying-claims` as the public
  continuity ID if this merge later proceeds, because it already owns the
  transition from ordinary claim records into proof-, citation-, procedure-,
  replay-, benchmark-, or review-carrying justification artifacts.
- Treat `unified-adaptive-tribunal-and-adversarial-review` as a folded source
  chapter whose dossier construction, reviewer roles, adversarial probes,
  dissent preservation, unchanged-evidence guard, verdict constraints, proof
  hooks, tests, source mappings, and reader path become named sections,
  subclaims, and history records in the destination chapter.
- Keep `claim-ledgers-and-belief-revision` standalone. It owns durable claim
  identity, support state, provenance, contradiction links, uncertainty,
  revision history, and ledger effects. Proof-carrying claims and tribunal
  verdicts are verification events that write back into that substrate; they
  are not the substrate itself.

## Non-Actions

- No manifest edit has been made.
- No chapter file has been removed or rewritten.
- No source note, external source, proof target, test result, or support state
  has changed.
- No support state changes are made or implied.
- No claim is promoted above `argument`.
- No external comparator is treated as proving ASI Stack verifier quality,
  theorem validity, citation accuracy, semantic equivalence, tribunal quality,
  reviewer independence, verdict correctness, runtime behavior, or deployment
  behavior.
- No reader, EPUB, DOCX, PDF, or audio artifact is approved by this package.
- No new result is created by this dry run.

## Proposed `book_structure.json` Diff

This proposed `book_structure.json` diff is illustrative and unapplied. If the
merge is later executed, apply one cluster merge in one commit, then regenerate
and validate every generated surface.

```diff
@@ Part II - Planning, Memory, Reasoning, and Execution
 {
   "id": "spinoza-verification-and-proof-carrying-claims",
-  "title": "Spinoza Verification and Proof-Carrying Claims",
+  "title": "Proof-Carrying Claims and Adversarial Review",
   "file": "chapters/spinoza-verification-and-proof-carrying-claims.qmd",
   "status": "conceptual",
   "evidence_level": "argument",
   "claim_label": "Design rationale",
   "source_ids": [
     "spinoza",
     "genesiscode",
     "coherence_exchange",
     "verification_bandwidth",
-    "treellm"
+    "treellm",
+    "uat",
+    "talos"
   ],
-  "problem": "The stack needs a way to move selected claims from generated prose toward auditable, proof-carrying objects.",
-  "insufficient": "Neural generation alone cannot guarantee semantic consistency, source grounding, or formal validity.",
-  "core_claim": "Spinoza-style verification should convert high-value claims into proof-carrying or justification-carrying artifacts with explicit tiers.",
-  "minimal_implementation": "A tiered proof-carrying claim schema with one non-philosophical invariant example.",
-  "beyond_state_of_art": "The mature version is a justification compiler for high-value claims..."
+  "problem": "High-value claims and high-risk artifacts need a governed verification path that can choose proof, citation, procedure, replay, benchmark, or adversarial-review treatment without laundering failed, mismatched, or contested evidence into support.",
+  "insufficient": "Neural generation, one-pass self-critique, and informal review can produce plausible justification language without preserving proof scope, verifier result, evidence dossier, dissent, failed attempts, verdict constraints, or downgrade routes.",
+  "core_claim": "Selected claims and artifacts should move through proof-carrying, justification-carrying, or adversarial-review envelopes that record tier, interpretation mapping, evidence dossier, verifier or tribunal result, dissent, limitations, failed attempts, required actions, residuals, and ledger effects.",
+  "minimal_implementation": "A proof-carrying-claim schema and tribunal-review schema with synthetic valid and expected-invalid fixtures for narrow formal passes, citation no-change, mismatch escalation, missing artifacts, failed verification, high-risk review, dissent, and prior-review laundering.",
+  "beyond_state_of_art": "A mature verification operating system routes each high-value claim or artifact to the cheapest adequate verifier or review process, then writes a bounded result back to the claim ledger without confusing artifact validity, verdict scope, semantic adequacy, or support-state effect."
 }
-
-{
-  "id": "unified-adaptive-tribunal-and-adversarial-review",
-  "title": "Unified Adaptive Tribunal and Adversarial Review",
-  "file": "chapters/unified-adaptive-tribunal-and-adversarial-review.qmd",
-  ...
-}
```

Manifest notes:

- The proposed Corben/local `source_ids` union is `spinoza`, `genesiscode`,
  `coherence_exchange`, `verification_bandwidth`, `treellm`, `uat`, and
  `talos`.
- If the merge proceeds, remove only the
  `unified-adaptive-tribunal-and-adversarial-review` chapter object after all
  claim, source, proof, reader, handoff, URL, and validation steps pass.
- Do not fold `claim-ledgers-and-belief-revision` into this destination. The
  ledger is the durable belief-state substrate that receives proof-carrying
  and tribunal outcomes; merging it would hide the difference between claim
  identity and verification events.
- Run `python3 scripts/chapter_adjacency_report.py --if-removing
  unified-adaptive-tribunal-and-adversarial-review` before editing the
  manifest.

## Destination Section Outline

The merged chapter should use one chapter skeleton, not two pasted skeletons.

Recommended section sequence:

1. Chapter status: one status block with merged evidence gaps.
2. Drafting guardrail: proof-carrying and tribunal records are not theorem
   validity, citation accuracy, reviewer independence, verdict correctness,
   open-domain formalization, or deployed review evidence.
3. Human Reading Path: start from the reader question, "What happens when a
   claim is important enough that ordinary prose is not enough?"
4. Problem: high-value claims and high-risk artifacts need a verification path
   that can select the right justification type and preserve failure,
   mismatch, dissent, and residuals.
5. Why existing approaches are insufficient: generated rationales and
   one-pass critiques can sound credible while losing proof scope, evidence
   boundaries, adversarial dissent, reviewer role separation, and downgrade
   routes.
6. Core Claim: use the merged core claim above.
7. Claim-source mapping status: one table that separates proof-carrying claim
   lineage from tribunal/adversarial-review lineage and keeps all support at
   `argument`.
8. Mechanism:
   - claim or artifact intake from the claim ledger, planning layer, or
     execution layer;
   - tier selection and justification type;
   - interpretation mapping and semantic adequacy check;
   - verifier artifact, citation dossier, procedure log, replay log, benchmark
     artifact, or tribunal dossier;
   - adversarial reviewer roles, probes, dissent, and cycle caps;
   - failed attempts, timeouts, mismatches, prior-review guards, and downgrade
     routes;
   - ledger effect, required actions, dispatch blockers, and residuals;
   - no-claim boundaries for verifier quality, semantic equivalence, reviewer
     independence, and verdict correctness.
9. Interfaces:
   - claim ledgers supply stable claim identity and receive ledger effects;
   - VCM and semantic cells supply source/evidence context;
   - verification bandwidth scopes adequacy and risk;
   - GenesisCode/Lean/Circle-style proof routes supply formal artifacts when
     appropriate;
   - UAT-style tribunal review handles contested, high-risk, or mismatched
     cases;
   - planning and execution receive constraints, blockers, required actions, or
     residuals.
10. Invariants:
    - proof tier is explicit;
    - formal tiers require formal proof artifacts;
    - failed or mismatched verification blocks promotion;
    - dissent remains visible;
    - accept verdicts require scoped evidence;
    - high-risk artifacts cannot bypass required tribunal review;
    - unchanged evidence cannot launder a prior rejection into acceptance.
11. Failure modes:
    - certified delusion;
    - invalid formalization;
    - missing justification artifact;
    - theorem laundering;
    - reviewer collusion;
    - consensus theater;
    - critique without action;
    - repeated-review laundering.
12. Minimum Viable Implementation: combine
    `schemas/proof_carrying_claim.schema.json`,
    `schemas/tribunal_review_record.schema.json`,
    `python3 scripts/validate_proof_carrying_claims.py`, and
    `python3 scripts/validate_tribunal_review.py`. The MVI should preserve the
    valid narrow formal pass, citation no-change, mismatch escalation,
    high-risk revise-with-dissent, scoped accept, and unchanged-evidence block
    cases plus expected-invalid missing-artifact, mismatch-promotion,
    timeout-overpromotion, missing-probe, missing-evidence, prior-review
    laundering, and dissent-hiding cases.
13. Beyond the State of the Art: describe a verification operating system that
    routes claims to proof, citation, procedure, replay, benchmark, or
    adversarial review and writes bounded effects back to ledgers. Preserve the
    claim boundary that this is an architectural endpoint, not a demonstrated
    open-domain verifier or institution.
14. Codex test plan: union existing proof-artifact presence, tier assignment,
    formalization mismatch, adversarial-review coverage, dissent preservation,
    and consensus-evidence tests.
15. Formalization hooks: keep both Lean modules and all four proof tags.
16. Source crosswalk: union Corben/local sources and external comparators.
17. Repetition-removal ledger: collapse two repeated verification/review
    skeletons into one verification-event chapter; reinvest space in
    interpretation mapping, mismatch handling, dissent preservation, and ledger
    effects.
18. Summary: one synthesis of tiered proof-carrying claims, tribunal review,
    adversarial probes, failed attempts, dissent, verdict constraints,
    residuals, and claim-ledger effects.
19. Handoff: route directly to `labor-os-and-typed-jobs`, while preserving the
    backward writeback interface to `claim-ledgers-and-belief-revision`.

## Appendix C Row Plan

Proposed merged core row:

| Row | Chapter | Claim label | Support state | Source effect |
|---|---|---|---|---|
| `spinoza-verification-and-proof-carrying-claims.core` | `spinoza-verification-and-proof-carrying-claims` | Design rationale | argument | Union the source mappings from both source chapters; keep limits and passage-review notes. |

Proposed merged core claim:

> Selected claims and artifacts should move through proof-carrying,
> justification-carrying, or adversarial-review envelopes that record tier,
> interpretation mapping, evidence dossier, verifier or tribunal result,
> dissent, limitations, failed attempts, required actions, residuals, and
> ledger effects.

Claim-history treatment for folded and protected chapters:

| Existing row | Proposed disposition | Required preservation |
|---|---|---|
| `unified-adaptive-tribunal-and-adversarial-review.core` | Redirect to destination as a subclaim about dossier boundaries, role-separated reviewers, adversarial probes, dissent, verdict constraints, cycle caps, unchanged-evidence guards, and required actions. | Preserve claim text in history, proof tags, source mappings, fixture/test rows, and no-promotion limits. |
| `claim-ledgers-and-belief-revision.core` | No merge in this package. | Keep claim identity, support states, provenance, contradictions, revision history, proof-status storage, and ledger effect handling standalone. |

No support state changes are authorized. All core and subclaim rows remain
`argument` unless a separate evidence-transition record later justifies a
change.

## Source Union

Corben/local source union:

- `spinoza`
- `genesiscode`
- `coherence_exchange`
- `verification_bandwidth`
- `treellm`
- `uat`
- `talos`

External-source union:

- `ext_lean4_theorem_proving`
- `ext_proof_carrying_code_1997`
- `ext_contestable_ai_design_2022`

Adjacent external comparators retained by `claim-ledgers-and-belief-revision`:

- `ext_alce_2023`
- `ext_checklist_2020`
- `ext_self_rag_2023`

These external records remain comparators and positioning sources. They do not
prove ASI Stack verifier quality, proof validity, citation accuracy,
semantic-equivalence checking, tribunal quality, reviewer independence, verdict
correctness, or deployment behavior.

## Lean Module And Proof-Manifest Treatment

Keep these modules:

- `AsiStackProofs.ProofCarryingClaims`
- `AsiStackProofs.Tribunal`

Keep these proof tags:

- `lean:spinoza.proof_carrying.operational_invariant`
- `lean:spinoza.proof_carrying.failure_blocks_promotion`
- `lean:tribunal.review.operational_invariant`
- `lean:tribunal.review.failure_blocks_promotion`

Do not move or retire the adjacent claim-ledger module or proof tags:

- `AsiStackProofs.ClaimLedger`
- `lean:claims.ledger.operational_invariant`
- `lean:claims.ledger.failure_blocks_promotion`

If the merge proceeds, `proofs/proof_manifest.json` should continue to record
both destination proof families. The folded source chapter ID may become a
historical source for proof lineage only after the outline and proof manifest
are updated deliberately.

## Tests, Schemas, And Fixtures

Preserve these schema and harness surfaces:

- `schemas/proof_carrying_claim.schema.json`
- `schemas/tribunal_review_record.schema.json`
- `schemas/claim_record.schema.json`
- `schemas/belief_revision_record.schema.json`
- `experiments/proof_carrying_claims/fixtures/valid_formal_narrow_pass.json`
- `experiments/proof_carrying_claims/fixtures/valid_citation_dossier_no_change.json`
- `experiments/proof_carrying_claims/fixtures/valid_mismatch_escalates.json`
- `experiments/proof_carrying_claims/fixtures/invalid_pass_missing_artifact_refs.json`
- `experiments/proof_carrying_claims/fixtures/invalid_mismatch_promotes.json`
- `experiments/proof_carrying_claims/fixtures/invalid_formal_tier_wrong_justification.json`
- `experiments/proof_carrying_claims/fixtures/invalid_timeout_overpromotes_support.json`
- `experiments/proof_carrying_claims/fixtures/invalid_negative_missing_failed_attempt.json`
- `experiments/tribunal_review/fixtures/valid_accept_with_scope_constraints.json`
- `experiments/tribunal_review/fixtures/valid_block_unchanged_evidence.json`
- `experiments/tribunal_review/fixtures/valid_high_risk_revise_with_dissent.json`
- `experiments/tribunal_review/fixtures/invalid_accept_missing_evidence.json`
- `experiments/tribunal_review/fixtures/invalid_high_risk_no_probes.json`
- `experiments/tribunal_review/fixtures/invalid_prior_review_laundering.json`
- `experiments/tribunal_review/fixtures/invalid_dissent_without_unresolved_issue.json`
- `experiments/tribunal_review/fixtures/invalid_weak_non_claims.json`
- `python3 scripts/validate_proof_carrying_claims.py`
- `python3 scripts/validate_tribunal_review.py`

The harness results remain the existing synthetic proof-carrying-claim and
tribunal-review record-discipline gates. This package does not create a new
test result, theorem-validity result, open-domain verifier, citation validator,
reviewer-independence audit, verdict-correctness result, runtime trace, or
deployed tribunal result.

## Reader Path, Handoff, And Review Repairs

If the merge is executed later:

- Rewrite the destination Human Reading Path to explain why important claims
  need proof, citation, procedure, replay, benchmark, or tribunal envelopes
  rather than better-sounding prose.
- Remove the separate
  `unified-adaptive-tribunal-and-adversarial-review` reader-review row only
  after preserving its reader path as a subsection or history note in the
  destination row.
- Update the predecessor handoff from `claim-ledgers-and-belief-revision` if
  the manifest order changes.
- Update the destination handoff so it points directly to
  `labor-os-and-typed-jobs`.
- Preserve a local explanation that claim ledgers remain the durable belief
  substrate and are not merged.
- Update reader overlays and curated-reader matrices only after the manifest
  merge is accepted.

## Repetition-Removal Ledger

Repeated skeleton load removed:

- Two separate Problem sections about stronger claim review become one problem
  about selecting adequate verification events for high-value claims and
  high-risk artifacts.
- Two Insufficiency sections about neural generation and single-pass review
  become one insufficiency section about plausible justification language
  without proof scope, evidence boundaries, dissent, or downgrade routes.
- Two Mechanism sections become one verification-event mechanism with proof
  tiers, interpretation mappings, verifier artifacts, tribunal dossiers,
  adversarial probes, failed attempts, dissent, verdict constraints, and ledger
  effects.
- Two MVI sections become one fixture/harness story over the existing
  proof-carrying-claim and tribunal-review schemas.

Saved-space reinvestment:

- Deeper explanation of interpretation mapping and semantic adequacy.
- Clearer treatment of failed verification, mismatches, timeouts, and negative
  evidence as anti-laundering records.
- Clearer tribunal lifecycle and unchanged-evidence guard.
- Stronger no-claim language around theorem validity, citation accuracy,
  reviewer independence, verdict correctness, and deployed behavior.

Reader-work disposition:

- Pause curated-reader graduation for the verification/adversarial-review pair
  until this package is reviewed and the merge is executed, explicitly
  deferred, or rejected/retained.
- Local prose cleanup may continue if it does not entrench duplicate chapter
  skeletons.
- Reader curation may continue for `claim-ledgers-and-belief-revision`, because
  this package protects that chapter boundary.

## Validation If Executed Later

If a future review accepts the merge, the execution commit should run at least:

```bash
python3 scripts/chapter_adjacency_report.py --if-removing unified-adaptive-tribunal-and-adversarial-review
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_source_evidence_audit.py
python3 scripts/validate_source_appendices.py
python3 scripts/validate_outline_consistency.py
python3 scripts/validate_implementation_horizons.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_book.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
python3 scripts/validate_proof_carrying_claims.py
python3 scripts/validate_tribunal_review.py
(cd lean && lake build)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

## Review Questions

- Does the destination preserve a clearer artifact boundary than the current
  two-chapter split?
- Does tribunal review become stronger as one verification modality inside the
  proof-carrying chapter, or does it still deserve standalone chapter
  ownership?
- Is `spinoza-verification-and-proof-carrying-claims` the right continuity ID,
  or should the URL/title policy preserve both public pages more visibly?
- Is the claim-ledger substrate protected strongly enough?
- Does the one-skeleton draft reduce reader repetition without hiding proof,
  source, or test limits?

## Non-Claims

- This dry run does not merge chapters.
- This dry run does not change `book_structure.json`.
- This dry run does not change Appendix C support states.
- This dry run does not create a source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support
  transition.
- This dry run does not prove theorem validity, citation accuracy, semantic
  equivalence, reviewer independence, verdict correctness, deployed review
  behavior, runtime behavior, or ASI capability.

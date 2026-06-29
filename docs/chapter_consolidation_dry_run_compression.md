# Chapter Consolidation Dry Run: Compact Generative Systems

Last updated: 2026-06-29

This is the first non-pilot dry-run package required by
`docs/v1_x_beyond_sota_roadmap.md` and
`docs/chapter_consolidation_sequence.md`. It is a review artifact only. It
does not edit `book_structure.json`, delete a chapter, change a URL, rewrite a
chapter, change source mappings, change proof targets, change support states,
or approve a reader artifact.

Dry-run destination:
`compact-generative-systems-and-residual-honesty`, retitled **Compact
Generative Systems: Generate, Verify, Repair, and Residual Honesty**.

Source chapters:

- `compact-generative-systems-and-residual-honesty`
- `generate-verify-repair-compression`
- `rankfold-neuralfold-and-artifact-compression`

Continuity decision:

- Keep `compact-generative-systems-and-residual-honesty` as the public
  continuity ID if this merge later proceeds.
- Treat `generate-verify-repair-compression` as a folded source chapter whose
  generate/verify/repair loop, exactness receipt, repair residual, consumer
  policy, proof hooks, tests, source mappings, and reader path become named
  sections, subclaims, and history records in the destination chapter.
- Treat `rankfold-neuralfold-and-artifact-compression` as conditional. The
  full-merge option folds it into the destination as the concrete artifact and
  tensor compression lane. The Conservative option keeps
  `rankfold-neuralfold-and-artifact-compression` standalone if review finds
  that RankFold/NeuralFold still owns a distinct technique, fixture family,
  artifact identity, or reader throughline.
- `semantic-representation-and-tree-structured-models` is not included in this
  merge package. It remains a `fold_review_candidate` only. A later
  representation package may decide whether semantic trees remain a standalone
  representation substrate or become a section elsewhere.

## Non-Actions

- No manifest edit has been made.
- No chapter file has been removed or rewritten.
- No source note, external source, proof target, test result, or support state
  has changed.
- No support state changes are made or implied.
- No claim is promoted above `argument`.
- No external comparator is treated as proving ASI Stack compression,
  reconstruction, runtime, model-quality, or deployment behavior.
- No reader, EPUB, DOCX, PDF, or audio artifact is approved by this package.
- No new result is created by this dry run.

## Proposed `book_structure.json` Diff

This proposed `book_structure.json` diff is illustrative and unapplied. If the
merge is later executed, apply one cluster merge in one commit, then regenerate
and validate every generated surface.

```diff
@@ Part III - Routing, Compression, Representation, and Substrates
 {
   "id": "compact-generative-systems-and-residual-honesty",
-  "title": "Compact Generative Systems and Residual Honesty",
+  "title": "Compact Generative Systems: Generate, Verify, Repair, and Residual Honesty",
   "file": "chapters/compact-generative-systems-and-residual-honesty.qmd",
   "status": "conceptual",
   "evidence_level": "argument",
   "claim_label": "Design rationale",
   "source_ids": [
     "cgs",
     "rgs",
     "bugbrain",
     "simulation_scaling",
     "rmi",
-    "project_theseus_whitepaper"
+    "project_theseus_whitepaper",
+    "bbvca_v9",
+    "bbvca_main",
+    "rankfold_neuralfold",
+    "rankfold_compressor"
   ],
-  "problem": "The architecture needs a theory of compact systems that generate useful behavior without hiding unresolved complexity.",
-  "insufficient": "Compression can look efficient while moving burden into unmeasured reconstruction, verification, or human review work.",
-  "core_claim": "A compact generative system is useful only when compactness, generativity, governance, verification, and residual burden are all explicit.",
-  "minimal_implementation": "A compactness ledger with seed, router/index, search/planning, generator/decoder, verifier/critic, residual correction, memory/governance hooks, exact remainder, verification, and residual fields.",
-  "beyond_state_of_art": "Compact generative systems earn their place as a burden-accounting layer for compression and generation..."
+  "problem": "Compact generators, exact repair receipts, and compressed artifacts need one claim-accounting surface so useful compression does not hide residual burden.",
+  "insufficient": "Seed-size, compression-ratio, and generated-reconstruction claims can hide verification, repair, fallback, downstream utility, metadata, interface, governance, and human-review costs.",
+  "core_claim": "Compact generative systems should store the smallest useful governed generator plus the cheapest exact or scoped residual, while preserving verification, fallback, consumer policy, and residual-burden records.",
+  "minimal_implementation": "A compact generative record, compression receipt, and compressed artifact record fixture suite with one lossy or blocked case, one verification-failed case, and one fallback/probe case.",
+  "beyond_state_of_art": "A mature compression control plane treats generators, repairs, residuals, compressed artifacts, consumer policies, and exact replay or fallback decisions as one audited representation market."
 }
-
-{
-  "id": "generate-verify-repair-compression",
-  "title": "Generate-Verify-Repair Compression",
-  "file": "chapters/generate-verify-repair-compression.qmd",
-  ...
-}
-
-{
-  "id": "rankfold-neuralfold-and-artifact-compression",
-  "title": "RankFold, NeuralFold, and Artifact Compression",
-  "file": "chapters/rankfold-neuralfold-and-artifact-compression.qmd",
-  ...
-}
```

Manifest notes:

- The proposed Corben/local `source_ids` union is `cgs`, `rgs`, `bugbrain`,
  `simulation_scaling`, `rmi`, `project_theseus_whitepaper`, `bbvca_v9`,
  `bbvca_main`, `rankfold_neuralfold`, and `rankfold_compressor`.
- If the full merge proceeds, remove only the
  `generate-verify-repair-compression` and
  `rankfold-neuralfold-and-artifact-compression` chapter objects after all
  claim, source, proof, reader, handoff, URL, and validation steps pass.
- If the Conservative option passes instead, remove only
  `generate-verify-repair-compression`; keep
  `rankfold-neuralfold-and-artifact-compression` as the technique-owning
  artifact-compression chapter.
- Run `python3 scripts/chapter_adjacency_report.py --if-removing
  generate-verify-repair-compression` before editing the manifest.
- Run `python3 scripts/chapter_adjacency_report.py --if-removing
  rankfold-neuralfold-and-artifact-compression` before any full merge.

## Destination Section Outline

The merged chapter should use one chapter skeleton, not three pasted
skeletons.

Recommended section sequence:

1. Chapter status: one status block with merged evidence gaps.
2. Drafting guardrail: compression is not evidence unless reconstruction,
   repair, fallback, residuals, and consumer policy are explicit.
3. Human Reading Path: start from the reader question, "When does a smaller
   representation still owe the truth?"
4. Problem: the stack needs one ledger for compact generators, generated
   reconstruction, exact repairs, compressed artifacts, consumer policy,
   fallback, and residual burden.
5. Why existing approaches are insufficient: raw ratio, seed size, or generated
   reconstruction can move work into verification, repair, metadata, fallback,
   downstream utility loss, governance review, or human interpretation.
6. Core Claim: use the merged core claim above.
7. Claim-source mapping status: one table that separates compact-generator
   lineage, GVR exactness lineage, and RankFold/NeuralFold artifact lineage
   while keeping all support at `argument`.
8. Mechanism:
   - compactness ledger;
   - generate/verify/repair receipt;
   - exact repair residual;
   - compressed artifact admission;
   - residual burden and fallback;
   - consumer policy and use envelope;
   - proxy-rate versus final-rate accounting;
   - no-claim boundaries for model quality, general compression, and deployed
     runtime performance.
9. Interfaces:
   - artifact graph and replay logs;
   - routing and specialist-core selection;
   - Virtual Context ABI and memory;
   - evidence states and claim promotion gates;
   - resource economics and token budgets;
   - fast-generation receipts.
10. Invariants:
    - exactness claims require verification and repair accounting;
    - compressed artifacts require task probes or fallback;
    - unresolved obligations remain residuals;
    - consumer policy scopes use;
    - metadata and interface costs are counted;
    - proxy compression rates do not become final rates.
11. Failure modes:
    - ratio laundering;
    - exactness theater;
    - repair cost hidden outside the receipt;
    - verifier too weak for the reconstruction claim;
    - probe overfitting;
    - fallback too expensive to be honest;
    - downstream utility collapse;
    - human or governance burden displaced into "review."
12. Minimum Viable Implementation: combine
    `compact_generative_record.valid.json`, `compression_receipt.valid.json`,
    and `compressed_artifact_record.valid.json` fixture suites. The MVI should
    include at least one lossy representation that cannot be marked exact, one
    failed verification that blocks exactness promotion, one task probe that
    routes to fallback, and one residual-burden record.
13. Beyond the State of the Art: describe a compression control plane where
    generators, exact repairs, compressed artifacts, consumer policies,
    residuals, replay, and fallback decisions form an audited representation
    market. Preserve the claim boundary that this is an architectural endpoint,
    not a demonstrated deployed compression system.
14. Codex test plan: union the existing compact-generative-system,
    generate/verify/repair, and artifact-compression tests without claiming
    broader evidence.
15. Formalization hooks: keep all three Lean modules and all six proof tags.
16. Source crosswalk: union Corben/local sources and external comparators.
17. Summary: one synthesis of compact generation, exact repairs, artifact
    admission, and residual honesty.
18. Handoff: route to `fast-generation-and-latency-hiding`, because fast
    generation inherits accepted-output and verifier-cost accounting from the
    compression chapter. The artifact-compression subsection should also point
    forward to `semantic-representation-and-tree-structured-models` and
    `resource-economics-and-token-budgets` where relevant.

## Appendix C Row Plan

Proposed merged core row:

| Row | Chapter | Claim label | Support state | Source effect |
|---|---|---|---|---|
| `compact-generative-systems-and-residual-honesty.core` | `compact-generative-systems-and-residual-honesty` | Design rationale | argument | Union the source mappings from all folded source chapters; keep limits and passage-review notes. |

Proposed merged core claim:

> Compact generative systems should store the smallest useful governed
> generator plus the cheapest exact or scoped residual, while preserving
> verification, fallback, consumer policy, and residual-burden records.

Claim-history treatment for folded source chapters:

| Existing row | Proposed disposition | Required preservation |
|---|---|---|
| `generate-verify-repair-compression.core` | Redirect to destination as a subclaim about exactness receipts, generated reconstruction, repair residuals, fallback thresholds, and consumer policy. | Preserve claim text in history, proof tags, source mappings, and no-promotion limits. |
| `rankfold-neuralfold-and-artifact-compression.core` | Full-merge option redirects to destination as an artifact-compression implementation subclaim. Conservative option keeps this as a standalone core claim. | Preserve RankFold/NeuralFold technique identity, probe-route fallback, residual coding, source mappings, proof tags, and restoration conditions. |
| `semantic-representation-and-tree-structured-models.core` | No change in this package. | Keep standalone until a later fold disposition proves that semantic representation is only a substrate section. |

No support state changes are authorized. All core and subclaim rows remain
`argument` unless a separate evidence-transition record later justifies a
change.

## Source Union

Corben/local source union:

- `cgs`
- `rgs`
- `bugbrain`
- `simulation_scaling`
- `rmi`
- `project_theseus_whitepaper`
- `bbvca_v9`
- `bbvca_main`
- `rankfold_neuralfold`
- `rankfold_compressor`

External-source union:

- `ext_deep_compression_2015`
- `ext_dreamcoder_2020`
- `ext_information_bottleneck_2000`
- `ext_knowledge_distillation_2015`
- `ext_mdl_tutorial_2004`
- `ext_codebleu_2020`
- `ext_gptq_2022`
- `ext_lora_2021`
- `ext_qlora_2023`

These external records remain comparators and positioning sources. They do not
prove the ASI Stack compression architecture, RankFold/NeuralFold behavior, or
any runtime result.

## Lean Module And Proof-Manifest Treatment

Keep these modules:

- `AsiStackProofs.CompactGenerativeSystems`
- `AsiStackProofs.GenerateVerifyRepair`
- `AsiStackProofs.ArtifactCompression`

Keep these proof tags:

- `lean:compression.cgs.operational_invariant`
- `lean:compression.cgs.failure_blocks_promotion`
- `lean:compression.gvr.operational_invariant`
- `lean:compression.gvr.failure_blocks_promotion`
- `lean:compression.artifacts.operational_invariant`
- `lean:compression.artifacts.failure_blocks_promotion`

Do not retire modules or proof tags in the merge. A merged chapter can carry
multiple proof families. Any later theorem consolidation must be a separate
formal-proof decision, not a side effect of table-of-contents cleanup.

## Tests, Schemas, And Fixtures

Preserve these fixture families:

- `compact_generative_record.valid.json`
- `compression_receipt.valid.json`
- `compressed_artifact_record.valid.json`

Preserve the planned tests from the outline:

- reconstruction quality;
- repair-cost accounting;
- bounded-search failure;
- consumer-policy enforcement;
- compression-ratio accounting;
- probe-route fallback;
- downstream utility checks;
- access-pattern admission;
- residual-burden recording.

If the merge is executed, update schema references, fixture paths, and chapter
crosswalks only after validators confirm that no fixture family became
orphaned.

## Reader Path, Handoff, And Review Repairs

Before any manifest edit:

- run both adjacency reports listed above;
- update Human Reading Path prose so the reader sees one compression argument
  rather than three repeated openings;
- update Handoff sections for the destination, previous chapter, and next
  chapter;
- update reader overlays and curated-reader review matrices so folded content
  remains discoverable;
- update `docs/chapter_external_grounding_status.md` and
  `docs/external_sota_positioning_audit.md` after scaffold generation;
- update Appendix C, Appendix K, proof manifests, repository map, README, and
  changelog;
- record URL, redirect, or historical-note policy for any folded chapter file.

The reader benefit must be tested explicitly: the destination chapter should
reduce repeated Problem/Insufficiency/Mechanism sections while adding more
specific mechanisms, negative cases, and external-positioning context.

## MVI And Beyond-SOTA Merge

Merged minimum viable implementation:

- one compact generative record;
- one compression receipt;
- one compressed artifact record;
- one lossy/blocked exactness case;
- one failed verification case;
- one probe/fallback case;
- one consumer-policy or residual-burden rejection.

Merged mature endpoint:

- a compression control plane that treats compact generators, generated
  reconstructions, exact repairs, residual burden, compressed artifacts,
  consumer policies, utility probes, fallback, replay, and governance review as
  one audited representation market.

This end state remains speculative architecture until a separate implementation
or evaluation lane produces public evidence.

## URL And Redirect Policy

If the merge is executed, do not silently delete reader-visible history. Choose
one of these before touching the manifest:

- keep folded `.qmd` files as historical notes excluded from the book order but
  linked from the destination chapter;
- add public redirect pages from folded chapter slugs to the destination
  chapter;
- keep a release-history note that names the last version where each folded
  chapter was standalone.

The chosen policy must be visible in the changelog and release notes.

## Expected Generated File Updates

If the merge is executed later, expect updates to:

- `_quarto.yml`
- `appendices/A_source_matrix.qmd`
- `appendices/C_claims_evidence_matrix.qmd`
- `appendices/K_proof_manifest.qmd`
- `appendices/F_changelog.qmd`
- `proofs/proof_manifest.json`
- `docs/book_outline.md`
- `docs/chapter_external_grounding_status.md`
- `docs/external_sota_positioning_audit.md`
- reader overlay and review records

This dry run does not make those generated updates.

## Validation Commands

Run these before any future merge commit:

```bash
python3 scripts/chapter_adjacency_report.py --if-removing generate-verify-repair-compression
python3 scripts/chapter_adjacency_report.py --if-removing rankfold-neuralfold-and-artifact-compression
python3 scripts/sync_scaffold.py
python3 scripts/sync_proof_manifest.py
python3 scripts/validate_chapter_consolidation_sequence.py
python3 scripts/validate_publication.py
python3 scripts/validate_release_profiles.py
python3 scripts/validate_reader_spine.py --check
python3 scripts/validate_book.py
python3 scripts/validate_visual_coverage.py
python3 scripts/validate_schemas.py
python3 scripts/validate_protocol_examples.py
(cd lean && lake build)
quarto render --to html
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

## Review Questions

- Should `rankfold-neuralfold-and-artifact-compression` remain standalone
  because it owns a concrete technique, fixture family, or reader arc?
- Does the destination chapter become too broad, or does it clarify the common
  artifact boundary?
- Should `semantic-representation-and-tree-structured-models` remain
  standalone until a separate representation review is complete? The default
  answer for this package is yes.
- Does the handoff to `fast-generation-and-latency-hiding` remain clear after
  the GVR source chapter is folded?
- Does the merged chapter remove repeated skeleton load while increasing
  mechanism depth, negative-case clarity, external positioning, proof routing,
  and reader flow?

## Non-Claims

- This dry run does not merge chapters.
- This dry run does not change `book_structure.json`.
- This dry run does not change Appendix C support states.
- This dry run does not create source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support.
- This dry run does not prove that a future merged chapter will be better.
- This dry run does not approve reader, ebook, PDF, DOCX, audio, DOI, archive,
  or release artifacts.
- This dry run does not validate any new compression, reconstruction, artifact,
  model-quality, speed, memory, or deployment result.

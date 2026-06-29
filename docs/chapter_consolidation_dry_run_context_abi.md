# Chapter Consolidation Dry Run: Static Context ABI

Last updated: 2026-06-29

This is a non-pilot dry-run package required by
`docs/v1_x_beyond_sota_roadmap.md` and
`docs/chapter_consolidation_sequence.md`. It is a review artifact only. It
does not edit `book_structure.json`, delete a chapter, change a URL, rewrite a
chapter, change source mappings, change proof targets, change support states,
or approve a reader artifact.

Dry-run destination:
`virtual-context-abi`, retitled **The Virtual Context ABI: Typed Pages, Cells,
and Certificates**.

Source chapters:

- `virtual-context-abi`
- `semantic-pages-context-cells-and-certificates`

Related chapters not merged by this package:

- `context-transactions-snapshots-mounts-and-taint`
- `verification-bandwidth-and-context-adequacy`
- `claim-ledgers-and-belief-revision`

Continuity decision:

- Keep `virtual-context-abi` as the public continuity ID if this merge later
  proceeds, because it already owns the stable interface between durable memory
  and model-visible working context.
- Treat `semantic-pages-context-cells-and-certificates` as a folded source
  chapter whose typed page/cell taxonomy, representation certificates, loss and
  use contracts, authority preservation rules, proof hooks, tests, source
  mappings, and reader path become named sections, subclaims, and history
  records in the destination chapter.
- Keep `context-transactions-snapshots-mounts-and-taint` standalone. It owns
  the dynamic temporal semantics: committed events, snapshots, mounts, branch
  isolation, taint propagation, deletion closure, and downstream derivative
  obligations.
- Keep `verification-bandwidth-and-context-adequacy` standalone. It owns the
  verification-capacity question: whether admitted context is adequate for a
  target claim, risk tier, and support-state effect.
- Keep `claim-ledgers-and-belief-revision` standalone. It consumes context
  cells and proof/adequacy signals, but its artifact is the durable claim
  ledger and revision system rather than the context ABI.

## Non-Actions

- No manifest edit has been made.
- No chapter file has been removed or rewritten.
- No source note, external source, proof target, test result, or support state
  has changed.
- No support state changes are made or implied.
- No claim is promoted above `argument`.
- No external comparator is treated as proving ASI Stack memory correctness,
  context compiler behavior, summary fidelity, transactional memory behavior,
  verification adequacy, model performance, or deployment behavior.
- No reader, EPUB, DOCX, PDF, or audio artifact is approved by this package.
- No new result is created by this dry run.

## Proposed `book_structure.json` Diff

This proposed `book_structure.json` diff is illustrative and unapplied. If the
merge is later executed, apply one cluster merge in one commit, then regenerate
and validate every generated surface.

```diff
@@ Part II - Planning, Memory, Reasoning, and Execution
 {
   "id": "virtual-context-abi",
-  "title": "Virtual Context ABI",
+  "title": "The Virtual Context ABI: Typed Pages, Cells, and Certificates",
   "file": "chapters/virtual-context-abi.qmd",
   "status": "conceptual",
   "evidence_level": "argument",
   "claim_label": "Design rationale",
   "source_ids": [
     "vcm_public",
     "context_engineer",
     "verification_bandwidth",
     "viea",
     "vcm_editable",
-    "moecot"
+    "moecot",
+    "spinoza"
   ],
-  "problem": "Long-horizon agents need a stable interface between durable memory and model-visible working context.",
-  "insufficient": "Long context windows and ordinary retrieval do not define addressability, evidence, authority, adequacy, or fault behavior.",
-  "core_claim": "Virtual Context Memory should expose a Virtual Context ABI with stable addresses, versions, mounts, snapshots, fault classes, representation contracts, and lifecycle operations.",
-  "minimal_implementation": "A context ABI table covering address, version, mount, snapshot, representation, adequacy states, and fault operations.",
-  "beyond_state_of_art": "The mature version is a memory operating interface for long-horizon AI work..."
+  "problem": "Long-horizon agents need a stable context interface whose addresses, versions, materializations, typed pages, context cells, certificates, authority labels, loss contracts, adequacy states, and faults remain inspectable across planning, reasoning, execution, and audit.",
+  "insufficient": "Long context windows, retrieval stores, and summaries can provide relevant text without defining stable addressability, representation authority, source bindings, omission records, permitted uses, adequacy boundaries, or typed failure behavior.",
+  "core_claim": "Virtual Context Memory should expose a Virtual Context ABI that materializes typed pages and context cells with stable addresses, versions, certificates, authority ceilings, loss/use contracts, adequacy states, residuals, and typed faults.",
+  "minimal_implementation": "A context ABI record plus semantic-page certificate fixtures validated by the context admission/adequacy harness, covering address, version, mount, snapshot, representation, source refs, authority ceiling, loss/use contract, adequacy state, residuals, and fault behavior.",
+  "beyond_state_of_art": "A mature Virtual Context ABI is the memory syscall layer for long-horizon AI work: planners, verifiers, workers, claim ledgers, reader editions, and auditors request typed context objects by stable address, version, mount, snapshot, representation need, authority label, adequacy target, certificate, lease, and residual boundary."
 }
-
-{
-  "id": "semantic-pages-context-cells-and-certificates",
-  "title": "Semantic Pages, Context Cells, and Certificates",
-  "file": "chapters/semantic-pages-context-cells-and-certificates.qmd",
-  ...
-}
```

Manifest notes:

- The proposed Corben/local `source_ids` union is `vcm_public`,
  `context_engineer`, `verification_bandwidth`, `viea`, `vcm_editable`,
  `moecot`, and `spinoza`.
- If the merge proceeds, remove only the
  `semantic-pages-context-cells-and-certificates` chapter object after all
  claim, source, proof, reader, handoff, URL, and validation steps pass.
- Do not fold `context-transactions-snapshots-mounts-and-taint` into this
  destination. Its transaction, snapshot, mount, branch, taint, and deletion
  semantics are a dynamic runtime layer, not just static context shape.
- Do not fold `verification-bandwidth-and-context-adequacy` into this
  destination. Its adequacy and verification-capacity records are consumers and
  governors of context packets, not merely fields in the static ABI.
- Run `python3 scripts/chapter_adjacency_report.py --if-removing
  semantic-pages-context-cells-and-certificates` before editing the manifest.

## Destination Section Outline

The merged chapter should use one chapter skeleton, not two pasted skeletons.

Recommended section sequence:

1. Chapter status: one status block with merged evidence gaps.
2. Drafting guardrail: a context ABI is not a deployed resolver, summary
   fidelity result, model-facing memory benchmark, transactional memory-store
   test, or verification-bandwidth measurement.
3. Human Reading Path: start from the reader question, "What exactly did the
   model receive, and what was it allowed to do with it?"
4. Problem: long-horizon agents need stable addresses, typed context objects,
   certificates, authority labels, adequacy states, and typed faults in one
   model-visible interface.
5. Why existing approaches are insufficient: retrieval, long context windows,
   and summaries can move text into a prompt without preserving addressability,
   provenance, omitted material, authority ceiling, permitted use, adequacy, or
   replay behavior.
6. Core Claim: use the merged core claim above.
7. Claim-source mapping status: one table that separates ABI/addressability
   lineage from semantic-page/certificate lineage and keeps all support at
   `argument`.
8. Mechanism:
   - context request and context address;
   - address, version, mount, snapshot, and materialization receipt;
   - typed semantic pages and context cells;
   - representation certificates;
   - source refs, omissions, loss contracts, and permitted uses;
   - authority ceiling and consumer policy;
   - adequacy state handoff without collapsing into proof;
   - typed faults for missing, unsafe, conflicting, stale, revoked, or
     unauthorized context;
   - no-claim boundaries for deployed resolver behavior, semantic fidelity, and
     model performance.
9. Interfaces:
   - planning requests context by task, address, authority, and adequacy need;
   - VCM materializes context packets and cells;
   - Spinoza and claim ledgers consume claim/evidence cells;
   - execution consumes only permitted representations;
   - artifact graphs store certificate references when context-derived objects
     become durable artifacts;
   - context transactions supply dynamic snapshot, mount, taint, and deletion
     semantics;
   - verification bandwidth evaluates adequacy for target claims.
10. Invariants:
    - addresses and versions are stable;
    - source bindings survive representation;
    - authority labels survive summarization;
    - loss and permitted-use contracts are explicit;
    - context admission and context adequacy remain distinct;
    - mandatory misses produce typed faults;
    - certificates cannot increase source authority ceilings.
11. Failure modes:
    - flat transcript memory;
    - stale context;
    - summary overconfidence;
    - provenance loss;
    - authority escalation through compression;
    - unsafe fit hidden as "relevant context";
    - adequacy laundering where admitted context is treated as proof.
12. Minimum Viable Implementation: combine
    `schemas/context_abi_record.schema.json`,
    `schemas/semantic_page_certificate.schema.json`,
    `schemas/context_packet.schema.json`,
    and `python3 scripts/validate_context_admission_adequacy.py`. The MVI
    should preserve the valid local-check and admitted-but-inadequate cases
    plus expected-invalid conflict-promotion, stale-certificate, and
    admission-as-verification cases.
13. Beyond the State of the Art: describe a memory syscall layer for AI work
    where every context packet arrives with address, version, certificate,
    authority, adequacy, lease, residual, and fault semantics. Preserve the
    boundary that this is an architectural endpoint, not a demonstrated
    deployed VCM memory system.
14. Codex test plan: union address/version stability, admission-vs-adequacy,
    conflict classification, fault behavior, certificate completeness,
    authority preservation, and summary-fidelity boundary tests.
15. Formalization hooks: keep both Lean modules and all four proof tags.
16. Source crosswalk: union Corben/local sources and external comparators.
17. Repetition-removal ledger: collapse two repeated context skeletons into one
    static ABI chapter; reinvest space in certificate semantics, authority/loss
    boundaries, and handoffs to dynamic transactions and adequacy.
18. Summary: one synthesis of stable context addressing, typed semantic cells,
    representation certificates, authority, adequacy, residuals, and faults.
19. Handoff: route directly to
    `context-transactions-snapshots-mounts-and-taint`, while preserving the
    later distinct handoff to `verification-bandwidth-and-context-adequacy`.

## Appendix C Row Plan

Proposed merged core row:

| Row | Chapter | Claim label | Support state | Source effect |
|---|---|---|---|---|
| `virtual-context-abi.core` | `virtual-context-abi` | Design rationale | argument | Union the source mappings from both source chapters; keep limits and passage-review notes. |

Proposed merged core claim:

> Virtual Context Memory should expose a Virtual Context ABI that materializes
> typed pages and context cells with stable addresses, versions, certificates,
> authority ceilings, loss/use contracts, adequacy states, residuals, and typed
> faults.

Claim-history treatment for folded and protected chapters:

| Existing row | Proposed disposition | Required preservation |
|---|---|---|
| `semantic-pages-context-cells-and-certificates.core` | Redirect to destination as a subclaim about typed semantic pages, context cells, representation certificates, source bindings, omissions, authority ceilings, loss contracts, and permitted uses. | Preserve claim text in history, proof tags, source mappings, fixture/test rows, and no-promotion limits. |
| `context-transactions-snapshots-mounts-and-taint.core` | No merge in this package. | Keep transactional memory semantics, snapshots, mounts, taint propagation, deletion closure, dynamic proof tags, and memory-store blockers standalone. |
| `verification-bandwidth-and-context-adequacy.core` | No merge in this package. | Keep adequacy, verification capacity, support-state effect, and mode-confusion blockers standalone. |
| `claim-ledgers-and-belief-revision.core` | No merge in this package. | Keep durable claim identity, contradiction, revision, support state, and ledger history standalone. |

No support state changes are authorized. All core and subclaim rows remain
`argument` unless a separate evidence-transition record later justifies a
change.

## Source Union

Corben/local source union:

- `vcm_public`
- `context_engineer`
- `verification_bandwidth`
- `viea`
- `vcm_editable`
- `moecot`
- `spinoza`

External-source union:

- `ext_alce_2023`
- `ext_longbench_2023`
- `ext_longllmlingua_2023`
- `ext_lost_in_middle_2023`
- `ext_memgpt_2023`
- `ext_rag_2020`
- `ext_ruler_2024`
- `ext_self_rag_2023`

These external records remain comparators and positioning sources. They do not
prove ASI Stack memory correctness, context compiler behavior, summary
fidelity, verification adequacy, model behavior, or deployment behavior.

## Lean Module And Proof-Manifest Treatment

Keep these modules:

- `AsiStackProofs.VirtualContextABI`
- `AsiStackProofs.ContextCertificates`

Keep these proof tags:

- `lean:vcm.abi.operational_invariant`
- `lean:vcm.abi.failure_blocks_promotion`
- `lean:vcm.certificates.operational_invariant`
- `lean:vcm.certificates.failure_blocks_promotion`

Do not move or retire these adjacent modules or proof tags:

- `AsiStackProofs.ContextTransactions`
- `lean:vcm.transactions.operational_invariant`
- `lean:vcm.transactions.failure_blocks_promotion`
- `AsiStackProofs.VerificationBandwidth`
- `lean:verification_bandwidth.adequacy.operational_invariant`
- `lean:verification_bandwidth.adequacy.failure_blocks_promotion`

If the merge proceeds, `proofs/proof_manifest.json` should continue to record
both destination proof families. The folded source chapter ID may become a
historical source for proof lineage only after the outline and proof manifest
are updated deliberately.

## Tests, Schemas, And Fixtures

Preserve these schema and harness surfaces:

- `schemas/context_abi_record.schema.json`
- `schemas/semantic_page_certificate.schema.json`
- `schemas/context_packet.schema.json`
- `schemas/context_adequacy_record.schema.json`
- `schemas/context_transaction_record.schema.json`
- `experiments/context_admission_adequacy/fixtures/valid_local_check_public_context.json`
- `experiments/context_admission_adequacy/fixtures/valid_admitted_but_inadequate.json`
- `experiments/context_admission_adequacy/fixtures/valid_conflict_escalation.json`
- `experiments/context_admission_adequacy/fixtures/invalid_admission_as_verification.json`
- `experiments/context_admission_adequacy/fixtures/invalid_conflict_promoted.json`
- `experiments/context_admission_adequacy/fixtures/invalid_stale_certificate_use.json`
- `python3 scripts/validate_context_admission_adequacy.py`

The harness result remains the existing synthetic context admission/adequacy
gate. This package does not create a new test result, deployed resolver
evidence, memory-store conformance result, summary-fidelity measurement,
contradiction-rate benchmark, or model-facing context result.

## Reader Path, Handoff, And Review Repairs

If the merge is executed later:

- Rewrite the destination Human Reading Path to explain why context must arrive
  as typed, permissioned, replayable objects rather than anonymous "relevant
  text."
- Remove the separate
  `semantic-pages-context-cells-and-certificates` reader-review row only after
  preserving its reader path as a subsection or history note in the destination
  row.
- Update the predecessor handoff from `cognitive-compilation-and-semantic-ir`
  if the manifest order changes.
- Update the destination handoff so it points directly to
  `context-transactions-snapshots-mounts-and-taint`.
- Preserve a local explanation that dynamic transactions and verification
  bandwidth remain separate protected chapters.
- Update reader overlays and curated-reader matrices only after the manifest
  merge is accepted.

## Repetition-Removal Ledger

Repeated skeleton load removed:

- Two separate Problem sections about compiled context become one problem about
  stable context object identity.
- Two Insufficiency sections about retrieval, long context, and summaries
  become one insufficiency section about text without address, provenance,
  authority, loss, adequacy, or replay semantics.
- Two Mechanism sections become one static ABI mechanism with typed pages,
  context cells, certificates, authority, loss, adequacy handoff, and faults.
- Two MVI sections become one fixture/harness story over the existing context
  ABI and certificate schemas.

Saved-space reinvestment:

- Deeper explanation of representation certificates and permitted-use
  contracts.
- Clearer static-versus-dynamic boundary between ABI/certificates and
  transactions/mounts/taint.
- Clearer admission-versus-adequacy boundary before the verification bandwidth
  chapter.
- Stronger no-claim language around model behavior and deployed memory
  correctness.

Reader-work disposition:

- Pause curated-reader graduation for the static ABI pair until this package is
  reviewed and the merge is executed, explicitly deferred, or rejected/retained.
- Local prose cleanup may continue if it does not entrench duplicate chapter
  skeletons.
- Reader curation may continue for
  `context-transactions-snapshots-mounts-and-taint` and
  `verification-bandwidth-and-context-adequacy`, because this package protects
  those chapter boundaries.

## Validation If Executed Later

If a future review accepts the merge, the execution commit should run at least:

```bash
python3 scripts/chapter_adjacency_report.py --if-removing semantic-pages-context-cells-and-certificates
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
python3 scripts/validate_context_admission_adequacy.py
(cd lean && lake build)
LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 quarto render --to html
node scripts/validate_live_human_view_browser.js --all-chapters --all-viewports
```

## Review Questions

- Does the destination preserve a clearer artifact boundary than the current
  two-chapter split?
- Does the semantic-page/certificate material become stronger as part of the
  ABI, or does it still deserve standalone chapter ownership?
- Is `virtual-context-abi` the right continuity ID, or should the URL/title
  policy preserve both public pages more visibly?
- Are dynamic transaction semantics and verification-bandwidth semantics
  protected strongly enough?
- Does the one-skeleton draft reduce reader repetition without hiding proof,
  source, or test limits?

## Non-Claims

- This dry run does not merge chapters.
- This dry run does not change `book_structure.json`.
- This dry run does not change Appendix C support states.
- This dry run does not create a source-derived, external-literature-backed,
  proof-derived, prototype-backed, synthetic-test-backed, or empirical support
  transition.
- This dry run does not prove deployed memory correctness, summary fidelity,
  context compiler behavior, model performance, runtime behavior, or ASI
  capability.

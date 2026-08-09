# Chapter Content Triage — 2026-08-08

Reviewer: Claude (external editorial review of the manuscript as a book)
Scope: all 85 files in `chapters/*.qmd` at commit `f39a73e88`
Purpose: decide where prose effort should be spent.

Codex adjudication status: **accepted as calibrated editorial input, not as an
automatic grading or completion authority.** This review is now consumed by
the active P7.1c reader-prose quality lane in
`docs/post_v2_3_maintenance_transfer_and_publication_roadmap.md`. The canonical
denominator is the current **85-chapter manifest**. The score table remains a
frozen account of Claude's scan at commit `f39a73e88`; current work is judged
against chapter meaning and current digests, not against the historical rank.

### What the project accepts from this review

- The book-wide concreteness deficit is real. Every chapter needs a
  subject-specific scene, trace, or explicit reference-chapter exemption that
  helps a reader see the mechanism operate, fail, or reach a decision.
- The three narrative anchors deserve the first substantive pass: Project
  Theseus should expose a real report-first run; Integrated Reference
  Architecture should make its existing showpiece trace carry the synthesis;
  and Resource Economics should join generation, verification, repair, human
  review, displaced cost, and residuals in one legible comparison.
- Mega-sentences, clause-pile core claims, repeated disclaimer language, and
  schema-shaped mechanism prose are material reading defects even when every
  underlying field is technically necessary.
- Human Reading Path prose must be chapter-specific and must influence the
  main argument's voice. A generated word budget is not evidence of a useful
  transition.
- Thinly grounded chapters need a source-role audit against the literature,
  especially where an established field offers obvious mechanism,
  limitation, competing-design, or evaluation anchors.

### What the project modifies or rejects

- Trigger phrases such as “for example” are discovery heuristics, not semantic
  proof that a chapter lacks a worked case. Existing headings, tables, traces,
  and measured result sections must be read before calling a result absent.
- A raw external-source threshold of eight or twelve is not an acceptance
  gate. Source quality, primary-source authority, role coverage, and relevance
  matter more than count; no citation is added merely to improve this score.
- A 60% prose ratio is not intrinsically superior. Tables remain when the
  comparison or state transition is the argument; bookkeeping tables move off
  the reading path when they merely repeat canonical records.
- Hedging is not deleted mechanically. Distinct limitations remain where a
  reader needs them; only duplicated or over-distributed caveats are
  consolidated into a clear chapter-level boundary.
- Not every reference chapter needs an invented anecdote. A documented trace,
  bounded illustrative vignette, counterexample, or explicit justified
  exemption may satisfy the concreteness obligation, but a generic schema
  restatement may not.

The completion authority is the digest-bound P7.1c packet and its semantic,
render, link, browser, and accessibility checks. Improving a numerical score
alone cannot close a chapter.

This is an assessment of **writing**, not correctness. It makes no support-state
claim and does not touch evidence, proofs, or the substance contract. No chapter
scored low because its thinking was wrong — the ideas in this book are
consistently stronger than the prose that carries them.

---

## 1. The scoring rubric (published in full, so every score is auditable)

Each chapter accumulates **penalty points** across five measured components.
Score = `100 − (penalty × 0.67)`. Maximum possible penalty is 90; observed range
is 20–73, producing scores of 51–87 with a median of 69.

| Component | Measures | Penalty thresholds |
|---|---|---|
| **Concreteness** | worked-example markers per 10k words (`for example`, `for instance`, `e.g.`, `consider a`, `suppose a`, `imagine`, `worked example`, `case study`, `walkthrough`) | `<1` → **30** · `<3` → **20** · `<6` → **8** · else **0** |
| **Hedging** | disclaimer phrases per 1,000 words (`does not prove/establish/validate/imply`, `no … is claimed/implied/reproduced`, `remains at argument`, `is not evidence`, …) | `density × 5`, capped at **20** |
| **Mega-sentences** | sentences over 60 words, prose only | `count × 1.5`, capped at **15** |
| **Prose ratio** | share of body lines that are prose (not table, list, heading, code, or fence) | `<45%` → **15** · `<60%` → **8** · else **0** |
| **Sourcing** | distinct `ext_*` external source references | `<6` → **10** · `<12` → **5** · else **0** |

### Why these five, and what was discarded

Three further components were computed and **removed because they do not
discriminate** — every chapter scored identically, so including them would have
inflated the appearance of rigour while adding nothing:

- *Human Reading Path length* — all 85 blocks fall between 174 and 184 words
  (stdev 3.8). Constant.
- *Figure presence* — zero chapters lack a figure or diagram. Constant.
- *Sentence-length variance* — every chapter exceeds the variance floor.
  Constant.

The five retained components each demonstrably move across the corpus:

| Component | Mean penalty | Std dev | Observed range |
|---|---:|---:|---|
| Concreteness | 27.4 | 5.1 | 0–30 |
| Sourcing | 5.5 | 3.6 | 0–10 |
| Prose ratio | 1.7 | 3.4 | 0–15 |
| Hedging | 6.9 | 3.0 | 1.6–20 |
| Mega-sentences | 4.9 | 3.0 | 0–15 |

Concreteness carries the largest weight because it is the book's dominant
deficit and the one most visible to a reader. Its high mean (27.4 of a possible
30) is itself the finding: nearly every chapter maxes this penalty.

### Calibration against reading

The rubric was checked against chapters I read in full before scoring.
`asi-is-a-stack-not-a-model` and `inner-alignment` read as among the strongest
writing in the book and score in the top quartile; `project-theseus-as-report-
first-implementation-reference` read as the most abstract chapter relative to
its purpose and scores last. The ranking matches the qualitative read at both
ends.

### What the score does not measure

Idea quality, correctness, proof adequacy, evidence strength, or importance to
the architecture. A chapter can score 87 and be conceptually minor, or score 51
and contain the book's most important material — `project-theseus` is exactly
that case.

---

## 2. Book-wide findings

**61 of 84 manifest chapters contain zero worked examples.** Median
concreteness across the manuscript is 0.0 per 10,000 words. In ~640,000 words
there are roughly ten instances of "for example", zero "for instance", three
"worked example", one "case study", and zero "walkthrough" or "vignette".

Every idea is stated as a category and never instantiated in a scene. The
noninheritance law — the strongest idea in the manuscript — is developed across
five separations and seven applications without a single concrete failure ever
being narrated. The reader is told the shape of the machinery and never shown it
running. Fixing this would improve the book more than another 50,000 words of
mechanism, and it is cheap: ~200 words × 84 chapters ≈ 17k words.

**Hedging is inversely correlated with substance.** 820 disclaimer phrases
book-wide. The thinnest chapters hedge roughly ten times more densely than the
most developed (`adversarial-machine-learning` 4.48/1k — one every 223 words —
versus `open-ended-improvement-engines` 0.32/1k). Where a chapter has little to
say, it says more about what it is not claiming.

**The Human Reading Path blocks are generated to a word budget**, not to their
subjects: 85 blocks, min 174, max 184, stdev 3.8. They are the best prose in the
book and they are interchangeable.

**Enumeration has replaced argument** in mechanism sections: eighteen-item
clause-pile lists, falsifiers stated as one sentence with nine numbered clauses,
core claims carrying ~20 comma-separated bindings.

### The fix pattern

Open each `## Problem` section with a concrete failure before generalizing:
**a specific actor, a specific action, a specific bad outcome, then the boundary
that should have caught it** — 150–250 words, then into the existing text.

Concreteness does not require inventing benchmark numbers. The repository
already contains unused material: Theseus traces and ledger rows; Circle
Calculus theorem statements and replay receipts; the KERC refutation (714-byte
packets against a 73.25-byte baseline at tied task quality, against a falsifier
written first); the P2 rank-4/rank-5 infrastructure failures; and the recorded
negative results in `evidence_transitions/`. **The book's own experimental
history is full of stories it never tells.**

---

## 3. Per-chapter reviews

Ordered worst score first. Each entry lists the measured evidence behind its
score and the specific actions to take. Every chapter has a named
worked-example suggestion drawn from its own subject matter.

### 1. `project-theseus-as-report-first-implementation-reference` — **51/100**

9,029 words · 0 examples · 2.1 hedges/1k · 10 mega-sentences · 56% prose · 4 external sources · penalty 73.5/90

- **Add a worked example** (currently 0 in 9,029 words). Suggested: one real Theseus run: goal, compiled request, route decision, dispatched work, emitted report, evidence packet — with actual commands and ledger rows.
- **Cut hedging** from 2.1/1k to ≤1.0 (~19 disclaimer phrases → ≤9). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- **Break 10 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Raise prose share from 56% toward 60% by converting argument-bearing tables.
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 2. `adversarial-machine-learning-and-model-attack-surface` — **58/100**

4,683 words · 0 examples · 4.48 hedges/1k · 2 mega-sentences · 82% prose · 5 external sources · penalty 63.0/90

- **Add a worked example** (currently 0 in 4,683 words). Suggested: three concrete attacks end to end: one jailbreak chain, one backdoor trigger, one extraction query budget.
- **Cut hedging** from 4.48/1k to ≤1.0 (~21 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 5). Target ≥8 canonical anchors for this field.

### 3. `coilra-multicoil-rope-and-cyclic-mixers` — **59/100**

6,551 words · 0 examples · 1.83 hedges/1k · 8 mega-sentences · 68% prose · 4 external sources · penalty 61.2/90

- **Add a worked example** (currently 0 in 6,551 words). Suggested: the RoPE certifier catching one positional violation, shown concretely.
- **Cut hedging** from 1.83/1k to ≤1.0 (~12 disclaimer phrases → ≤7). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- **Break 8 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 4. `circle-calculus-and-proof-carrying-ai-contracts` — **60/100**

6,953 words · 0 examples · 1.29 hedges/1k · 3 mega-sentences · 51% prose · 1 external sources · penalty 59.0/90

- **Add a worked example** (currently 0 in 6,953 words). Suggested: an actual Circle theorem statement, the RoPE certifier run, and the replay receipt it emits.
- Trim hedging from 1.29/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Raise prose share from 51% toward 60% by converting argument-bearing tables.
- **Add external sources** (currently 1). Target ≥8 canonical anchors for this field.

### 5. `compact-generative-systems-and-residual-honesty` — **61/100**

13,404 words · 0 examples · 0.82 hedges/1k · 7 mega-sentences · 59% prose · 10 external sources · penalty 57.6/90

- **Add a worked example** (currently 0 in 13,404 words). Suggested: one real artifact compressed: compact form, residual, reconstruction, and the honest rate accounting.
- **Break 7 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Raise prose share from 59% toward 60% by converting argument-bearing tables.
- Add external sources (currently 10); target ≥12.

### 6. `open-research-agenda-and-bibliography-plan` — **61/100**

6,816 words · 0 examples · 0.73 hedges/1k · 3 mega-sentences · 43% prose · 7 external sources · penalty 58.1/90

- **Add a worked example** (currently 0 in 6,816 words). Suggested: none needed — declare this a reference chapter.
- Split 3 over-long sentence(s).
- **Table-heavy** (43% prose). Convert argument-bearing tables to prose; keep reference tables. Target ≥60%.
- Add external sources (currently 7); target ≥12.

### 7. `autonomous-replication-proliferation-and-containment` — **62/100**

4,494 words · 0 examples · 2.67 hedges/1k · 2 mega-sentences · 84% prose · 1 external sources · penalty 56.3/90

- **Add a worked example** (currently 0 in 4,494 words). Suggested: a bounded replication evaluation: the capability ladder, the stop condition, the containment receipt.
- **Cut hedging** from 2.67/1k to ≤1.0 (~12 disclaimer phrases → ≤4). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 1). Target ≥8 canonical anchors for this field.

### 8. `integrated-reference-architecture` — **62/100**

14,856 words · 1 examples · 1.35 hedges/1k · 17 mega-sentences · 71% prose · 11 external sources · penalty 56.8/90

- **Add a worked example** (currently 1 in 14,856 words). Suggested: THE end-to-end walkthrough: one real task carried through every layer, with the artifact crossing each boundary.
- Trim hedging from 1.35/1k toward ≤1.0.
- **Break 17 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Add external sources (currently 11); target ≥12.

### 9. `multi-agent-dynamics-collective-intelligence-and-systemic-risk` — **63/100**

5,151 words · 0 examples · 2.14 hedges/1k · 3 mega-sentences · 82% prose · 5 external sources · penalty 55.2/90

- **Add a worked example** (currently 0 in 5,151 words). Suggested: two evaluators drifting into correlated agreement, and the independence test that catches it.
- **Cut hedging** from 2.14/1k to ≤1.0 (~11 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 3 over-long sentence(s).
- **Add external sources** (currently 5). Target ≥8 canonical anchors for this field.

### 10. `personal-compute-hives-and-federated-edge-intelligence` — **63/100**

10,158 words · 0 examples · 2.07 hedges/1k · 5 mega-sentences · 50% prose · 20 external sources · penalty 55.8/90

- **Add a worked example** (currently 0 in 10,158 words). Suggested: one task split across three heterogeneous devices with a partition failure mid-run.
- **Cut hedging** from 2.07/1k to ≤1.0 (~21 disclaimer phrases → ≤10). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- **Break 5 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Raise prose share from 50% toward 60% by converting argument-bearing tables.

### 11. `resource-economics-and-token-budgets` — **63/100**

16,097 words · 0 examples · 0.93 hedges/1k · 8 mega-sentences · 58% prose · 28 external sources · penalty 54.7/90

- **Add a worked example** (currently 0 in 16,097 words). Suggested: one task routed three ways with the complete ledger: generation, verification, repair, review, and residual.
- **Break 8 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Raise prose share from 58% toward 60% by converting argument-bearing tables.

### 12. `stable-capability-fields` — **63/100**

6,688 words · 0 examples · 2.09 hedges/1k · 3 mega-sentences · 63% prose · 3 external sources · penalty 54.9/90

- **Add a worked example** (currently 0 in 6,688 words). Suggested: swapping one summarizer implementation for another: exactly what must be preserved and what may change.
- **Cut hedging** from 2.09/1k to ≤1.0 (~14 disclaimer phrases → ≤7). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 3 over-long sentence(s).
- **Add external sources** (currently 3). Target ≥8 canonical anchors for this field.

### 13. `artifact-steward-agents-and-living-project-governance` — **64/100**

7,977 words · 0 examples · 1.88 hedges/1k · 6 mega-sentences · 61% prose · 9 external sources · penalty 53.4/90

- **Add a worked example** (currently 0 in 7,977 words). Suggested: a project that decays over six months and the steward intervention that arrests it.
- **Cut hedging** from 1.88/1k to ≤1.0 (~15 disclaimer phrases → ≤8). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- **Break 6 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Add external sources (currently 9); target ≥12.

### 14. `content-authenticity-watermarking-and-synthetic-media-integrity` — **64/100**

5,076 words · 0 examples · 2.36 hedges/1k · 1 mega-sentences · 82% prose · 3 external sources · penalty 53.3/90

- **Add a worked example** (currently 0 in 5,076 words). Suggested: a C2PA credential stripped in redistribution, with what the watermark and fingerprint each still recover.
- **Cut hedging** from 2.36/1k to ≤1.0 (~12 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 1 over-long sentence(s).
- **Add external sources** (currently 3). Target ≥8 canonical anchors for this field.

### 15. `durable-semantic-memory-and-knowledge-lattices` — **64/100**

6,114 words · 0 examples · 2.29 hedges/1k · 2 mega-sentences · 84% prose · 5 external sources · penalty 54.4/90

- **Add a worked example** (currently 0 in 6,114 words). Suggested: a fact that changes and must propagate through dependents without rewriting history.
- **Cut hedging** from 2.29/1k to ≤1.0 (~14 disclaimer phrases → ≤6). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 5). Target ≥8 canonical anchors for this field.

### 16. `human-ai-communication-persuasion-and-epistemic-security` — **64/100**

4,434 words · 0 examples · 2.48 hedges/1k · 1 mega-sentences · 80% prose · 5 external sources · penalty 53.9/90

- **Add a worked example** (currently 0 in 4,434 words). Suggested: a fluent, persuasive, wrong summary that passes human review — and the epistemic control that catches it.
- **Cut hedging** from 2.48/1k to ≤1.0 (~11 disclaimer phrases → ≤4). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 1 over-long sentence(s).
- **Add external sources** (currently 5). Target ≥8 canonical anchors for this field.

### 17. `mathematical-and-search-substrates` — **64/100**

7,280 words · 0 examples · 0.41 hedges/1k · 2 mega-sentences · 56% prose · 4 external sources · penalty 53.0/90

- **Add a worked example** (currently 0 in 7,280 words). Suggested: one search problem solved by two substrates with different cost profiles.
- Split 2 over-long sentence(s).
- Raise prose share from 56% toward 60% by converting argument-bearing tables.
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 18. `security-kernel-and-digital-scifs` — **64/100**

8,145 words · 0 examples · 1.23 hedges/1k · 3 mega-sentences · 57% prose · 10 external sources · penalty 53.7/90

- **Add a worked example** (currently 0 in 8,145 words). Suggested: an exfiltration attempt routed through a legitimately permitted channel.
- Trim hedging from 1.23/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Raise prose share from 57% toward 60% by converting argument-bearing tables.
- Add external sources (currently 10); target ≥12.

### 19. `societal-resilience-and-misuse-defense` — **64/100**

5,165 words · 0 examples · 2.52 hedges/1k · 1 mega-sentences · 86% prose · 4 external sources · penalty 54.1/90

- **Add a worked example** (currently 0 in 5,165 words). Suggested: one fraud campaign detected, countered, and reported without violating victim privacy.
- **Cut hedging** from 2.52/1k to ≤1.0 (~13 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 1 over-long sentence(s).
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 20. `capability-replacement-and-rollback` — **65/100**

7,094 words · 0 examples · 1.13 hedges/1k · 2 mega-sentences · 58% prose · 6 external sources · penalty 51.6/90

- **Add a worked example** (currently 0 in 7,094 words). Suggested: a canary that passes at 5% traffic and fails at 40%, with the rollback inventory.
- Trim hedging from 1.13/1k toward ≤1.0.
- Split 2 over-long sentence(s).
- Raise prose share from 58% toward 60% by converting argument-bearing tables.
- Add external sources (currently 6); target ≥12.

### 21. `capability-thresholds-and-deployment-commitments` — **65/100**

5,980 words · 0 examples · 0.84 hedges/1k · 5 mega-sentences · 78% prose · 4 external sources · penalty 51.7/90

- **Add a worked example** (currently 0 in 5,980 words). Suggested: one threshold crossed and the if-then commitment actually firing.
- **Break 5 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 22. `governed-objective-formation-value-learning-and-goal-integrity` — **65/100**

4,119 words · 0 examples · 1.94 hedges/1k · 2 mega-sentences · 84% prose · 4 external sources · penalty 52.7/90

- **Add a worked example** (currently 0 in 4,119 words). Suggested: an objective that drifts measurably across three feedback rounds.
- **Cut hedging** from 1.94/1k to ≤1.0 (~8 disclaimer phrases → ≤4). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 23. `human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty` — **65/100**

4,576 words · 0 examples · 1.75 hedges/1k · 2 mega-sentences · 72% prose · 4 external sources · penalty 51.8/90

- **Add a worked example** (currently 0 in 4,576 words). Suggested: a BCI consent boundary: what the interface may read, and who may authorize a change.
- **Cut hedging** from 1.75/1k to ≤1.0 (~8 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 24. `military-ai-autonomous-weapons-and-strategic-stability` — **65/100**

4,996 words · 0 examples · 1.8 hedges/1k · 2 mega-sentences · 75% prose · 4 external sources · penalty 52.0/90

- **Add a worked example** (currently 0 in 4,996 words). Suggested: an escalation scenario where meaningful human control is preserved under time pressure.
- **Cut hedging** from 1.8/1k to ≤1.0 (~9 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 25. `perception-sensor-fusion-and-observation-trust` — **65/100**

4,962 words · 0 examples · 1.41 hedges/1k · 3 mega-sentences · 76% prose · 5 external sources · penalty 51.5/90

- **Add a worked example** (currently 0 in 4,962 words). Suggested: three sensors disagreeing with one spoofed, and how trust is assigned.
- Trim hedging from 1.41/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- **Add external sources** (currently 5). Target ≥8 canonical anchors for this field.

### 26. `adversarial-evaluation-sandbagging-and-training-time-deception` — **66/100**

6,275 words · 0 examples · 1.27 hedges/1k · 6 mega-sentences · 76% prose · 9 external sources · penalty 50.3/90

- **Add a worked example** (currently 0 in 6,275 words). Suggested: a model behaving differently once it detects evaluation, and the observation design that catches it.
- Trim hedging from 1.27/1k toward ≤1.0.
- **Break 6 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Add external sources (currently 9); target ≥12.

### 27. `ai-deployment-transition-distribution-and-human-agency` — **66/100**

4,354 words · 0 examples · 1.61 hedges/1k · 2 mega-sentences · 85% prose · 3 external sources · penalty 51.1/90

- **Add a worked example** (currently 0 in 4,354 words). Suggested: one role materially changed by deployment, with the transition record.
- **Cut hedging** from 1.61/1k to ≤1.0 (~7 disclaimer phrases → ≤4). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 3). Target ≥8 canonical anchors for this field.

### 28. `data-engines-continual-learning-and-unlearning` — **66/100**

9,414 words · 0 examples · 1.7 hedges/1k · 5 mega-sentences · 70% prose · 11 external sources · penalty 51.0/90

- **Add a worked example** (currently 0 in 9,414 words). Suggested: an unlearning request plus the verification that it actually took effect in behavior.
- **Cut hedging** from 1.7/1k to ≤1.0 (~16 disclaimer phrases → ≤9). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- **Break 5 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Add external sources (currently 11); target ≥12.

### 29. `governed-operations-incident-command-and-graceful-degradation` — **66/100**

10,620 words · 0 examples · 1.41 hedges/1k · 2 mega-sentences · 63% prose · 3 external sources · penalty 50.0/90

- **Add a worked example** (currently 0 in 10,620 words). Suggested: one incident from page to postmortem, with the degradation ladder actually exercised.
- Trim hedging from 1.41/1k toward ≤1.0.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 3). Target ≥8 canonical anchors for this field.

### 30. `physical-compute-infrastructure-energy-and-environmental-constraints` — **66/100**

4,734 words · 0 examples · 2.53 hedges/1k · 2 mega-sentences · 80% prose · 7 external sources · penalty 50.6/90

- **Add a worked example** (currently 0 in 4,734 words). Suggested: a thermal or power constraint that changes a scheduling decision, with the numbers.
- **Cut hedging** from 2.53/1k to ≤1.0 (~12 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 31. `prototype-roadmap` — **66/100**

5,560 words · 0 examples · 1.08 hedges/1k · 2 mega-sentences · 53% prose · 11 external sources · penalty 51.4/90

- **Add a worked example** (currently 0 in 5,560 words). Suggested: the first milestone walked concretely: what gets built, what evidence it produces.
- Trim hedging from 1.08/1k toward ≤1.0.
- Split 2 over-long sentence(s).
- Raise prose share from 53% toward 60% by converting argument-bearing tables.
- Add external sources (currently 11); target ≥12.

### 32. `scientific-discovery-and-experimental-governance` — **66/100**

4,215 words · 0 examples · 1.66 hedges/1k · 2 mega-sentences · 87% prose · 1 external sources · penalty 51.3/90

- **Add a worked example** (currently 0 in 4,215 words). Suggested: one AI-generated hypothesis, its experiment, and an honest null result.
- **Cut hedging** from 1.66/1k to ≤1.0 (~7 disclaimer phrases → ≤4). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 1). Target ≥8 canonical anchors for this field.

### 33. `coil-attention-cyclic-memory-and-recurrence-contracts` — **67/100**

7,015 words · 0 examples · 1.14 hedges/1k · 6 mega-sentences · 66% prose · 8 external sources · penalty 49.7/90

- **Add a worked example** (currently 0 in 7,015 words). Suggested: a long-context task where KV freshness silently degrades, and the contract that detects it.
- Trim hedging from 1.14/1k toward ≤1.0.
- **Break 6 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Add external sources (currently 8); target ≥12.

### 34. `human-intent-as-a-formal-input` — **67/100**

6,563 words · 0 examples · 1.07 hedges/1k · 3 mega-sentences · 65% prose · 4 external sources · penalty 49.9/90

- **Add a worked example** (currently 0 in 6,563 words). Suggested: the request "clean up the repo" — every ambiguity the intent contract must pin before anything executes.
- Trim hedging from 1.07/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- **Add external sources** (currently 4). Target ≥8 canonical anchors for this field.

### 35. `planning-as-a-control-layer` — **67/100**

7,605 words · 0 examples · 1.31 hedges/1k · 2 mega-sentences · 62% prose · 1 external sources · penalty 49.6/90

- **Add a worked example** (currently 0 in 7,605 words). Suggested: a plan that must replan mid-execution after a dependency fails.
- Trim hedging from 1.31/1k toward ≤1.0.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 1). Target ≥8 canonical anchors for this field.

### 36. `relational-dimension-compilation-and-polyadic-cognition` — **67/100**

5,203 words · 0 examples · 1.54 hedges/1k · 1 mega-sentences · 70% prose · 1 external sources · penalty 49.2/90

- **Add a worked example** (currently 0 in 5,203 words). Suggested: one polyadic relation compiled and executed, showing the arity bound in action.
- Trim hedging from 1.54/1k toward ≤1.0.
- Split 1 over-long sentence(s).
- **Add external sources** (currently 1). Target ≥8 canonical anchors for this field.

### 37. `replaceable-cognitive-substrates-beyond-transformer-monoculture` — **67/100**

12,048 words · 1 examples · 1.16 hedges/1k · 4 mega-sentences · 55% prose · 42 external sources · penalty 49.8/90

- **Add a worked example** (currently 1 in 12,048 words). Suggested: swapping a Transformer core for an SSM behind the kernel ABI: what breaks, what holds.
- Trim hedging from 1.16/1k toward ≤1.0.
- **Break 4 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Raise prose share from 55% toward 60% by converting argument-bearing tables.

### 38. `system-boundaries-and-authority` — **67/100**

6,275 words · 0 examples · 1.75 hedges/1k · 4 mega-sentences · 62% prose · 8 external sources · penalty 49.8/90

- **Add a worked example** (currently 0 in 6,275 words). Suggested: a tool call whose scope silently widens mid-execution, and the exact record that refuses it.
- **Cut hedging** from 1.75/1k to ≤1.0 (~11 disclaimer phrases → ≤6). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- **Break 4 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Add external sources (currently 8); target ≥12.

### 39. `embodied-agency-real-time-control-and-physical-safety` — **68/100**

5,377 words · 0 examples · 1.67 hedges/1k · 3 mega-sentences · 76% prose · 6 external sources · penalty 47.8/90

- **Add a worked example** (currently 0 in 5,377 words). Suggested: a control loop missing its deadline, and the safe-state fallback.
- **Cut hedging** from 1.67/1k to ≤1.0 (~9 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 3 over-long sentence(s).
- Add external sources (currently 6); target ≥12.

### 40. `human-factors-and-meaningful-control-in-oversight` — **68/100**

8,217 words · 1 examples · 1.58 hedges/1k · 5 mega-sentences · 50% prose · 6 external sources · penalty 48.4/90

- **Add a worked example** (currently 1 in 8,217 words). Suggested: an approval queue at 200 items/day: where vigilance decays, and what the record shows at item 150.
- Trim hedging from 1.58/1k toward ≤1.0.
- **Break 5 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Raise prose share from 50% toward 60% by converting argument-bearing tables.
- Add external sources (currently 6); target ≥12.

### 41. `labor-os-and-typed-jobs` — **68/100**

6,903 words · 0 examples · 0.72 hedges/1k · 1 mega-sentences · 57% prose · 6 external sources · penalty 48.1/90

- **Add a worked example** (currently 0 in 6,903 words). Suggested: one job's full lifecycle from admission through retry to terminal receipt.
- Split 1 over-long sentence(s).
- Raise prose share from 57% toward 60% by converting argument-bearing tables.
- Add external sources (currently 6); target ≥12.

### 42. `learning-theory-generalization-and-scaling-science` — **68/100**

4,788 words · 0 examples · 2.09 hedges/1k · 2 mega-sentences · 79% prose · 10 external sources · penalty 48.4/90

- **Add a worked example** (currently 0 in 4,788 words). Suggested: a scaling forecast that misses by 2x, and the re-fit that follows.
- **Cut hedging** from 2.09/1k to ≤1.0 (~10 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 2 over-long sentence(s).
- Add external sources (currently 10); target ≥12.

### 43. `ai-supply-chain-integrity-and-lifecycle-provenance` — **69/100**

7,753 words · 0 examples · 1.29 hedges/1k · 3 mega-sentences · 67% prose · 10 external sources · penalty 46.0/90

- **Add a worked example** (currently 0 in 7,753 words). Suggested: a poisoned dependency entering a fine-tuning pipeline, traced through the BOM.
- Trim hedging from 1.29/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 10); target ≥12.

### 44. `failure-modes-of-ungoverned-intelligence` — **69/100**

7,863 words · 0 examples · 1.53 hedges/1k · 2 mega-sentences · 64% prose · 6 external sources · penalty 45.7/90

- **Add a worked example** (currently 0 in 7,863 words). Suggested: one narrated cascade: a small misgrounded claim propagating into an irreversible action across four layers.
- Trim hedging from 1.53/1k toward ≤1.0.
- Split 2 over-long sentence(s).
- Add external sources (currently 6); target ≥12.

### 45. `human-ai-organizations-delegation-and-accountability` — **69/100**

6,294 words · 0 examples · 1.43 hedges/1k · 3 mega-sentences · 81% prose · 8 external sources · penalty 46.6/90

- **Add a worked example** (currently 0 in 6,294 words). Suggested: a delegation chain where accountability is lost at the third hop.
- Trim hedging from 1.43/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 8); target ≥12.

### 46. `institutions-international-coordination-and-public-legitimacy` — **69/100**

4,929 words · 0 examples · 2.03 hedges/1k · 1 mega-sentences · 77% prose · 8 external sources · penalty 46.6/90

- **Add a worked example** (currently 0 in 4,929 words). Suggested: one cross-border incident requiring coordination between two regimes with incompatible thresholds.
- **Cut hedging** from 2.03/1k to ≤1.0 (~10 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 1 over-long sentence(s).
- Add external sources (currently 8); target ≥12.

### 47. `inter-stack-protocols-identity-and-economic-exchange` — **69/100**

6,888 words · 0 examples · 1.31 hedges/1k · 3 mega-sentences · 65% prose · 7 external sources · penalty 46.1/90

- **Add a worked example** (currently 0 in 6,888 words). Suggested: two stacks exchanging one claim under different ontologies, with the translation residual.
- Trim hedging from 1.31/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 48. `policy-optimization-and-learning-from-feedback` — **69/100**

8,906 words · 1 examples · 1.68 hedges/1k · 7 mega-sentences · 49% prose · 18 external sources · penalty 46.9/90

- **Add a worked example** (currently 1 in 8,906 words). Suggested: a reward hack discovered in feedback data, and the update that removes it.
- **Cut hedging** from 1.68/1k to ≤1.0 (~15 disclaimer phrases → ≤9). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- **Break 7 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Raise prose share from 49% toward 60% by converting argument-bearing tables.

### 49. `privacy-data-rights-and-information-flow-governance` — **69/100**

5,262 words · 0 examples · 1.33 hedges/1k · 3 mega-sentences · 69% prose · 11 external sources · penalty 46.2/90

- **Add a worked example** (currently 0 in 5,262 words). Suggested: a deletion request that must propagate to embeddings, caches, and fine-tuned descendants.
- Trim hedging from 1.33/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 11); target ≥12.

### 50. `recursive-self-improvement-boundaries` — **69/100**

6,316 words · 0 examples · 1.27 hedges/1k · 3 mega-sentences · 60% prose · 8 external sources · penalty 45.8/90

- **Add a worked example** (currently 0 in 6,316 words). Suggested: a self-proposed change that improves the benchmark and quietly weakens a guardrail.
- Trim hedging from 1.27/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 8); target ≥12.

### 51. `runtime-adapters-tool-permissions-and-human-approval` — **69/100**

11,455 words · 0 examples · 1.48 hedges/1k · 6 mega-sentences · 63% prose · 22 external sources · penalty 46.4/90

- **Add a worked example** (currently 0 in 11,455 words). Suggested: a permission escalation attempt blocked at the adapter, with the pre/post state.
- Trim hedging from 1.48/1k toward ≤1.0.
- **Break 6 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.

### 52. `benchmark-ratchets-and-anti-goodhart-evidence` — **70/100**

12,748 words · 1 examples · 0.94 hedges/1k · 7 mega-sentences · 62% prose · 26 external sources · penalty 45.2/90

- **Add a worked example** (currently 1 in 12,748 words). Suggested: a benchmark that got gamed, how it was detected, and the ratchet response.
- **Break 7 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.

### 53. `claim-ledgers-and-belief-revision` — **70/100**

8,330 words · 0 examples · 1.44 hedges/1k · 2 mega-sentences · 60% prose · 7 external sources · penalty 45.2/90

- **Add a worked example** (currently 0 in 8,330 words). Suggested: one claim contradicted by new evidence, walked through registration, challenge, and revision.
- Trim hedging from 1.44/1k toward ≤1.0.
- Split 2 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 54. `constitutional-alignment-substrate` — **70/100**

6,247 words · 0 examples · 1.12 hedges/1k · 3 mega-sentences · 67% prose · 7 external sources · penalty 45.1/90

- **Add a worked example** (currently 0 in 6,247 words). Suggested: a live conflict between two constitutional rules and the runtime resolution record.
- Trim hedging from 1.12/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 55. `open-weight-release-and-post-release-control` — **70/100**

4,804 words · 0 examples · 1.46 hedges/1k · 2 mega-sentences · 77% prose · 6 external sources · penalty 45.3/90

- **Add a worked example** (currently 0 in 4,804 words). Suggested: a released model fine-tuned to strip safety behavior, and what control genuinely survives.
- Trim hedging from 1.46/1k toward ≤1.0.
- Split 2 over-long sentence(s).
- Add external sources (currently 6); target ≥12.

### 56. `verification-bandwidth-and-context-adequacy` — **70/100**

7,055 words · 0 examples · 1.13 hedges/1k · 1 mega-sentences · 58% prose · 16 external sources · penalty 45.1/90

- **Add a worked example** (currently 0 in 7,055 words). Suggested: a review queue exceeding capacity, with the triage that preserves the highest-risk checks.
- Trim hedging from 1.13/1k toward ≤1.0.
- Split 1 over-long sentence(s).
- Raise prose share from 58% toward 60% by converting argument-bearing tables.

### 57. `artifact-graphs-audit-logs-and-replay` — **71/100**

13,650 words · 0 examples · 1.32 hedges/1k · 4 mega-sentences · 66% prose · 14 external sources · penalty 42.6/90

- **Add a worked example** (currently 0 in 13,650 words). Suggested: tracing one bad output backward to the source artifact that caused it.
- Trim hedging from 1.32/1k toward ≤1.0.
- **Break 4 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.

### 58. `context-transactions-snapshots-mounts-and-taint` — **71/100**

8,300 words · 0 examples · 0.84 hedges/1k · 1 mega-sentences · 59% prose · 19 external sources · penalty 43.7/90

- **Add a worked example** (currently 0 in 8,300 words). Suggested: a rollback that cannot reverse an external effect, and the compensation record that results.
- Split 1 over-long sentence(s).
- Raise prose share from 59% toward 60% by converting argument-bearing tables.

### 59. `living-book-methodology` — **71/100**

6,495 words · 0 examples · 0.62 hedges/1k · 3 mega-sentences · 64% prose · 9 external sources · penalty 42.6/90

- **Add a worked example** (currently 0 in 6,495 words). Suggested: the KERC story as the book's own method working: falsifier written first, refutation accepted, negative result retained.
- Split 3 over-long sentence(s).
- Add external sources (currently 9); target ≥12.

### 60. `safety-cases-and-structured-assurance` — **71/100**

5,795 words · 1 examples · 1.38 hedges/1k · 4 mega-sentences · 74% prose · 3 external sources · penalty 42.9/90

- **Add a worked example** (currently 1 in 5,795 words). Suggested: one hazard argued to a claim with its defeaters, shown as an actual argument tree.
- Trim hedging from 1.38/1k toward ≤1.0.
- **Break 4 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- **Add external sources** (currently 3). Target ≥8 canonical anchors for this field.

### 61. `cognitive-compilation-and-semantic-ir` — **72/100**

10,602 words · 1 examples · 0.57 hedges/1k · 3 mega-sentences · 67% prose · 7 external sources · penalty 42.3/90

- **Add a worked example** (currently 1 in 10,602 words). Suggested: one natural-language request compiled to semantic IR, shown in full, with what was lost.
- Split 3 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 62. `executable-specifications-and-lean-proof-envelope` — **72/100**

8,583 words · 1 examples · 1.51 hedges/1k · 6 mega-sentences · 69% prose · 9 external sources · penalty 41.5/90

- **Add a worked example** (currently 1 in 8,583 words). Suggested: one specification traced to its theorem and then to its runtime consumer.
- Trim hedging from 1.51/1k toward ≤1.0.
- **Break 6 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Add external sources (currently 9); target ≥12.

### 63. `governed-deliberation-and-test-time-scaling` — **72/100**

7,165 words · 0 examples · 0.56 hedges/1k · 3 mega-sentences · 65% prose · 7 external sources · penalty 42.3/90

- **Add a worked example** (currently 0 in 7,165 words). Suggested: one problem where more deliberation helps and one where it actively hurts, with costs.
- Split 3 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 64. `inner-alignment-mesa-optimization-and-learned-objective-integrity` — **72/100**

6,504 words · 1 examples · 1.38 hedges/1k · 3 mega-sentences · 82% prose · 5 external sources · penalty 41.4/90

- **Add a worked example** (currently 1 in 6,504 words). Suggested: a goal-misgeneralization case walked through the Learned-Objective Integrity Record: same training behavior, divergent held-out goal.
- Trim hedging from 1.38/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- **Add external sources** (currently 5). Target ≥8 canonical anchors for this field.

### 65. `intent-to-execution-contracts` — **72/100**

7,456 words · 0 examples · 1.07 hedges/1k · 4 mega-sentences · 71% prose · 12 external sources · penalty 41.4/90

- **Add a worked example** (currently 0 in 7,456 words). Suggested: one natural request lowered to a typed job with the actual contract shown at each step.
- Trim hedging from 1.07/1k toward ≤1.0.
- **Break 4 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.

### 66. `readiness-gates-residual-escrow-and-quarantine` — **72/100**

9,517 words · 0 examples · 0.95 hedges/1k · 5 mega-sentences · 60% prose · 17 external sources · penalty 42.3/90

- **Add a worked example** (currently 0 in 9,517 words). Suggested: a candidate passing nine of ten gates, and what happens to the tenth.
- **Break 5 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.

### 67. `spinoza-verification-and-proof-carrying-claims` — **72/100**

7,945 words · 0 examples · 0.63 hedges/1k · 2 mega-sentences · 60% prose · 7 external sources · penalty 41.1/90

- **Add a worked example** (currently 0 in 7,945 words). Suggested: a proof-carrying claim rejected at the consumer gate despite a valid proof.
- Split 2 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 68. `ai-work-surfaces-agent-harnesses-and-organizational-absorption` — **73/100**

4,787 words · 0 examples · 1.04 hedges/1k · 0 mega-sentences · 65% prose · 9 external sources · penalty 40.2/90

- **Add a worked example** (currently 0 in 4,787 words). Suggested: one workflow absorbed by an agent harness, with the accountability that moves and the accountability that does not.
- Trim hedging from 1.04/1k toward ≤1.0.
- Add external sources (currently 9); target ≥12.

### 69. `procedural-memory-and-cognitive-loop-closure` — **74/100**

9,425 words · 0 examples · 0.53 hedges/1k · 1 mega-sentences · 60% prose · 7 external sources · penalty 39.2/90

- **Add a worked example** (currently 0 in 9,425 words). Suggested: a compiled procedure that works for months then silently breaks on a dependency change.
- Split 1 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 70. `rankfold-neuralfold-and-artifact-compression` — **74/100**

9,255 words · 1 examples · 1.19 hedges/1k · 5 mega-sentences · 63% prose · 8 external sources · penalty 38.4/90

- **Add a worked example** (currently 1 in 9,255 words). Suggested: an actual compression run with the measured ratio and the residual bit cost.
- Trim hedging from 1.19/1k toward ≤1.0.
- **Break 5 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Add external sources (currently 8); target ≥12.

### 71. `routing-heads-and-specialist-cores` — **74/100**

11,375 words · 0 examples · 0.79 hedges/1k · 3 mega-sentences · 61% prose · 13 external sources · penalty 38.5/90

- **Add a worked example** (currently 0 in 11,375 words). Suggested: one query routed to the wrong specialist, and the recovery path.
- Split 3 over-long sentence(s).

### 72. `fast-generation-architectures` — **75/100**

12,723 words · 2 examples · 0.71 hedges/1k · 4 mega-sentences · 51% prose · 33 external sources · penalty 37.5/90

- **Add a worked example** (currently 2 in 12,723 words). Suggested: one speculative decode with a rejection, showing accepted tokens vs. wasted compute.
- **Break 4 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.
- Raise prose share from 51% toward 60% by converting argument-bearing tables.

### 73. `asi-is-a-stack-not-a-model` — **76/100**

7,011 words · 1 examples · 1.14 hedges/1k · 3 mega-sentences · 70% prose · 6 external sources · penalty 35.2/90

- **Add a worked example** (currently 1 in 7,011 words). Suggested: a confused-deputy failure: an agent holding a valid-but-stale grant deletes a production table; show which of the five separations should have caught it and where.
- Trim hedging from 1.14/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 6); target ≥12.

### 74. `governed-model-training-distributed-optimization-and-scaling` — **76/100**

9,274 words · 1 examples · 1.83 hedges/1k · 4 mega-sentences · 64% prose · 26 external sources · penalty 35.2/90

- **Add a worked example** (currently 1 in 9,274 words). Suggested: a training run failing mid-epoch, with checkpoint recovery and lineage preservation.
- **Cut hedging** from 1.83/1k to ≤1.0 (~17 disclaimer phrases → ≤9). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- **Break 4 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.

### 75. `moral-uncertainty-and-value-conflict` — **76/100**

7,136 words · 2 examples · 1.12 hedges/1k · 3 mega-sentences · 66% prose · 6 external sources · penalty 35.1/90

- **Add a worked example** (currently 2 in 7,136 words). Suggested: one decision with two defensible resolutions under different moral theories, and what the system records instead of picking silently.
- Trim hedging from 1.12/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 6); target ≥12.

### 76. `white-box-evidence-interpretability-and-activation-governance` — **76/100**

7,131 words · 1 examples · 1.4 hedges/1k · 3 mega-sentences · 64% prose · 10 external sources · penalty 36.5/90

- **Add a worked example** (currently 1 in 7,131 words). Suggested: one probe finding a feature, plus the construct-validity limit that stops it from certifying intent.
- Trim hedging from 1.4/1k toward ≤1.0.
- Split 3 over-long sentence(s).
- Add external sources (currently 10); target ≥12.

### 77. `dangerous-capability-domains-and-misuse-uplift` — **77/100**

5,176 words · 1 examples · 1.55 hedges/1k · 1 mega-sentences · 82% prose · 8 external sources · penalty 34.3/90

- **Add a worked example** (currently 1 in 5,176 words). Suggested: one uplift study designed end to end: cohorts, counterfactual, elicitation budget, stopping rule.
- Trim hedging from 1.55/1k toward ≤1.0.
- Split 1 over-long sentence(s).
- Add external sources (currently 8); target ≥12.

### 78. `open-ended-improvement-engines` — **77/100**

6,339 words · 1 examples · 0.32 hedges/1k · 2 mega-sentences · 74% prose · 5 external sources · penalty 34.6/90

- **Add a worked example** (currently 1 in 6,339 words). Suggested: an archive that stagnates after 200 generations, and the diagnosis.
- Split 2 over-long sentence(s).
- **Add external sources** (currently 5). Target ≥8 canonical anchors for this field.

### 79. `governed-world-models-and-reality-grounding` — **79/100**

9,257 words · 1 examples · 0.65 hedges/1k · 2 mega-sentences · 64% prose · 8 external sources · penalty 31.2/90

- **Add a worked example** (currently 1 in 9,257 words). Suggested: a model that is confidently wrong about the world, and the damage bound that holds anyway.
- Split 2 over-long sentence(s).
- Add external sources (currently 8); target ≥12.

### 80. `scalable-oversight-and-adversarial-ai-control` — **79/100**

7,280 words · 2 examples · 0.55 hedges/1k · 2 mega-sentences · 75% prose · 7 external sources · penalty 30.8/90

- **Add a worked example** (currently 2 in 7,280 words). Suggested: a critique round where a weaker verifier catches a stronger generator's error, and one where it fails.
- Split 2 over-long sentence(s).
- Add external sources (currently 7); target ≥12.

### 81. `model-weight-custody-and-hardware-roots-of-trust` — **80/100**

9,747 words · 2 examples · 0.82 hedges/1k · 4 mega-sentences · 70% prose · 14 external sources · penalty 30.1/90

- **Add a worked example** (currently 2 in 9,747 words). Suggested: an insider-access attempt defeated by attestation, and one that isn't.
- **Break 4 mega-sentences** (>60 words). Split enumerated falsifier/binding lists into a short prose claim plus a bulleted schema.

### 82. `evidence-states-and-claim-discipline` — **82/100**

7,283 words · 1 examples · 0.55 hedges/1k · 3 mega-sentences · 62% prose · 15 external sources · penalty 27.3/90

- **Add a worked example** (currently 1 in 7,283 words). Suggested: walk the KERC claim from `argument` to `refuted` — the prospective falsifier, the 714-vs-73.25-byte result, the N-level audit.
- Split 3 over-long sentence(s).

### 83. `virtual-context-abi` — **82/100**

9,597 words · 2 examples · 1.04 hedges/1k · 1 mega-sentences · 64% prose · 21 external sources · penalty 26.7/90

- **Add a worked example** (currently 2 in 9,597 words). Suggested: a context page fault walked end to end: miss, fetch, admission, eviction.
- Trim hedging from 1.04/1k toward ≤1.0.
- Split 1 over-long sentence(s).

### 84. `the-efficient-asi-hypothesis` — **83/100**

7,362 words · 1 examples · 0.81 hedges/1k · 1 mega-sentences · 60% prose · 18 external sources · penalty 25.6/90

- **Add a worked example** (currently 1 in 7,362 words). Suggested: one support ticket routed cheap vs. maximal, with the complete route ledger including the repair cost that erased the apparent saving.
- Split 1 over-long sentence(s).

### 85. `confidential-and-verifiable-ai-computation` — **87/100**

4,678 words · 3 examples · 1.71 hedges/1k · 1 mega-sentences · 72% prose · 3 external sources · penalty 20.1/90

- **Cut hedging** from 1.71/1k to ≤1.0 (~8 disclaimer phrases → ≤5). Keep one scoped non-claim per section; move the rest to the chapter-level non-claims block.
- Split 1 over-long sentence(s).
- **Add external sources** (currently 3). Target ≥8 canonical anchors for this field.


---

## 4. Full audited score table

Component columns are **penalty points** (higher = worse), so any score can be
recomputed by hand: `score = 100 − (penalty × 0.67)`.

| # | Score | Chapter | Words | ex | hedge | mega | prose | src | Penalty |
|---:|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | **51** | `project-theseus-as-report-first-implementation-reference` | 9,029 | 30 | 10.5 | 15 | 8 | 10 | 73.5 |
| 2 | **58** | `adversarial-machine-learning-and-model-attack-surface` | 4,683 | 30 | 20 | 3.0 | 0 | 10 | 63.0 |
| 3 | **59** | `coilra-multicoil-rope-and-cyclic-mixers` | 6,551 | 30 | 9.2 | 12.0 | 0 | 10 | 61.2 |
| 4 | **60** | `circle-calculus-and-proof-carrying-ai-contracts` | 6,953 | 30 | 6.5 | 4.5 | 8 | 10 | 59.0 |
| 5 | **61** | `compact-generative-systems-and-residual-honesty` | 13,404 | 30 | 4.1 | 10.5 | 8 | 5 | 57.6 |
| 6 | **61** | `open-research-agenda-and-bibliography-plan` | 6,816 | 30 | 3.6 | 4.5 | 15 | 5 | 58.1 |
| 7 | **62** | `autonomous-replication-proliferation-and-containment` | 4,494 | 30 | 13.3 | 3.0 | 0 | 10 | 56.3 |
| 8 | **62** | `integrated-reference-architecture` | 14,856 | 30 | 6.8 | 15 | 0 | 5 | 56.8 |
| 9 | **63** | `multi-agent-dynamics-collective-intelligence-and-systemic-risk` | 5,151 | 30 | 10.7 | 4.5 | 0 | 10 | 55.2 |
| 10 | **63** | `personal-compute-hives-and-federated-edge-intelligence` | 10,158 | 30 | 10.3 | 7.5 | 8 | 0 | 55.8 |
| 11 | **63** | `resource-economics-and-token-budgets` | 16,097 | 30 | 4.7 | 12.0 | 8 | 0 | 54.7 |
| 12 | **63** | `stable-capability-fields` | 6,688 | 30 | 10.4 | 4.5 | 0 | 10 | 54.9 |
| 13 | **64** | `artifact-steward-agents-and-living-project-governance` | 7,977 | 30 | 9.4 | 9.0 | 0 | 5 | 53.4 |
| 14 | **64** | `content-authenticity-watermarking-and-synthetic-media-integrity` | 5,076 | 30 | 11.8 | 1.5 | 0 | 10 | 53.3 |
| 15 | **64** | `durable-semantic-memory-and-knowledge-lattices` | 6,114 | 30 | 11.4 | 3.0 | 0 | 10 | 54.4 |
| 16 | **64** | `human-ai-communication-persuasion-and-epistemic-security` | 4,434 | 30 | 12.4 | 1.5 | 0 | 10 | 53.9 |
| 17 | **64** | `mathematical-and-search-substrates` | 7,280 | 30 | 2.0 | 3.0 | 8 | 10 | 53.0 |
| 18 | **64** | `security-kernel-and-digital-scifs` | 8,145 | 30 | 6.2 | 4.5 | 8 | 5 | 53.7 |
| 19 | **64** | `societal-resilience-and-misuse-defense` | 5,165 | 30 | 12.6 | 1.5 | 0 | 10 | 54.1 |
| 20 | **65** | `capability-replacement-and-rollback` | 7,094 | 30 | 5.6 | 3.0 | 8 | 5 | 51.6 |
| 21 | **65** | `capability-thresholds-and-deployment-commitments` | 5,980 | 30 | 4.2 | 7.5 | 0 | 10 | 51.7 |
| 22 | **65** | `governed-objective-formation-value-learning-and-goal-integrity` | 4,119 | 30 | 9.7 | 3.0 | 0 | 10 | 52.7 |
| 23 | **65** | `human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty` | 4,576 | 30 | 8.8 | 3.0 | 0 | 10 | 51.8 |
| 24 | **65** | `military-ai-autonomous-weapons-and-strategic-stability` | 4,996 | 30 | 9.0 | 3.0 | 0 | 10 | 52.0 |
| 25 | **65** | `perception-sensor-fusion-and-observation-trust` | 4,962 | 30 | 7.0 | 4.5 | 0 | 10 | 51.5 |
| 26 | **66** | `adversarial-evaluation-sandbagging-and-training-time-deception` | 6,275 | 30 | 6.3 | 9.0 | 0 | 5 | 50.3 |
| 27 | **66** | `ai-deployment-transition-distribution-and-human-agency` | 4,354 | 30 | 8.1 | 3.0 | 0 | 10 | 51.1 |
| 28 | **66** | `data-engines-continual-learning-and-unlearning` | 9,414 | 30 | 8.5 | 7.5 | 0 | 5 | 51.0 |
| 29 | **66** | `governed-operations-incident-command-and-graceful-degradation` | 10,620 | 30 | 7.0 | 3.0 | 0 | 10 | 50.0 |
| 30 | **66** | `physical-compute-infrastructure-energy-and-environmental-constraints` | 4,734 | 30 | 12.6 | 3.0 | 0 | 5 | 50.6 |
| 31 | **66** | `prototype-roadmap` | 5,560 | 30 | 5.4 | 3.0 | 8 | 5 | 51.4 |
| 32 | **66** | `scientific-discovery-and-experimental-governance` | 4,215 | 30 | 8.3 | 3.0 | 0 | 10 | 51.3 |
| 33 | **67** | `coil-attention-cyclic-memory-and-recurrence-contracts` | 7,015 | 30 | 5.7 | 9.0 | 0 | 5 | 49.7 |
| 34 | **67** | `human-intent-as-a-formal-input` | 6,563 | 30 | 5.4 | 4.5 | 0 | 10 | 49.9 |
| 35 | **67** | `planning-as-a-control-layer` | 7,605 | 30 | 6.6 | 3.0 | 0 | 10 | 49.6 |
| 36 | **67** | `relational-dimension-compilation-and-polyadic-cognition` | 5,203 | 30 | 7.7 | 1.5 | 0 | 10 | 49.2 |
| 37 | **67** | `replaceable-cognitive-substrates-beyond-transformer-monoculture` | 12,048 | 30 | 5.8 | 6.0 | 8 | 0 | 49.8 |
| 38 | **67** | `system-boundaries-and-authority` | 6,275 | 30 | 8.8 | 6.0 | 0 | 5 | 49.8 |
| 39 | **68** | `embodied-agency-real-time-control-and-physical-safety` | 5,377 | 30 | 8.3 | 4.5 | 0 | 5 | 47.8 |
| 40 | **68** | `human-factors-and-meaningful-control-in-oversight` | 8,217 | 20 | 7.9 | 7.5 | 8 | 5 | 48.4 |
| 41 | **68** | `labor-os-and-typed-jobs` | 6,903 | 30 | 3.6 | 1.5 | 8 | 5 | 48.1 |
| 42 | **68** | `learning-theory-generalization-and-scaling-science` | 4,788 | 30 | 10.4 | 3.0 | 0 | 5 | 48.4 |
| 43 | **69** | `ai-supply-chain-integrity-and-lifecycle-provenance` | 7,753 | 30 | 6.5 | 4.5 | 0 | 5 | 46.0 |
| 44 | **69** | `failure-modes-of-ungoverned-intelligence` | 7,863 | 30 | 7.7 | 3.0 | 0 | 5 | 45.7 |
| 45 | **69** | `human-ai-organizations-delegation-and-accountability` | 6,294 | 30 | 7.1 | 4.5 | 0 | 5 | 46.6 |
| 46 | **69** | `institutions-international-coordination-and-public-legitimacy` | 4,929 | 30 | 10.1 | 1.5 | 0 | 5 | 46.6 |
| 47 | **69** | `inter-stack-protocols-identity-and-economic-exchange` | 6,888 | 30 | 6.6 | 4.5 | 0 | 5 | 46.1 |
| 48 | **69** | `policy-optimization-and-learning-from-feedback` | 8,906 | 20 | 8.4 | 10.5 | 8 | 0 | 46.9 |
| 49 | **69** | `privacy-data-rights-and-information-flow-governance` | 5,262 | 30 | 6.7 | 4.5 | 0 | 5 | 46.2 |
| 50 | **69** | `recursive-self-improvement-boundaries` | 6,316 | 30 | 6.3 | 4.5 | 0 | 5 | 45.8 |
| 51 | **69** | `runtime-adapters-tool-permissions-and-human-approval` | 11,455 | 30 | 7.4 | 9.0 | 0 | 0 | 46.4 |
| 52 | **70** | `benchmark-ratchets-and-anti-goodhart-evidence` | 12,748 | 30 | 4.7 | 10.5 | 0 | 0 | 45.2 |
| 53 | **70** | `claim-ledgers-and-belief-revision` | 8,330 | 30 | 7.2 | 3.0 | 0 | 5 | 45.2 |
| 54 | **70** | `constitutional-alignment-substrate` | 6,247 | 30 | 5.6 | 4.5 | 0 | 5 | 45.1 |
| 55 | **70** | `open-weight-release-and-post-release-control` | 4,804 | 30 | 7.3 | 3.0 | 0 | 5 | 45.3 |
| 56 | **70** | `verification-bandwidth-and-context-adequacy` | 7,055 | 30 | 5.6 | 1.5 | 8 | 0 | 45.1 |
| 57 | **71** | `artifact-graphs-audit-logs-and-replay` | 13,650 | 30 | 6.6 | 6.0 | 0 | 0 | 42.6 |
| 58 | **71** | `context-transactions-snapshots-mounts-and-taint` | 8,300 | 30 | 4.2 | 1.5 | 8 | 0 | 43.7 |
| 59 | **71** | `living-book-methodology` | 6,495 | 30 | 3.1 | 4.5 | 0 | 5 | 42.6 |
| 60 | **71** | `safety-cases-and-structured-assurance` | 5,795 | 20 | 6.9 | 6.0 | 0 | 10 | 42.9 |
| 61 | **72** | `cognitive-compilation-and-semantic-ir` | 10,602 | 30 | 2.8 | 4.5 | 0 | 5 | 42.3 |
| 62 | **72** | `executable-specifications-and-lean-proof-envelope` | 8,583 | 20 | 7.5 | 9.0 | 0 | 5 | 41.5 |
| 63 | **72** | `governed-deliberation-and-test-time-scaling` | 7,165 | 30 | 2.8 | 4.5 | 0 | 5 | 42.3 |
| 64 | **72** | `inner-alignment-mesa-optimization-and-learned-objective-integrity` | 6,504 | 20 | 6.9 | 4.5 | 0 | 10 | 41.4 |
| 65 | **72** | `intent-to-execution-contracts` | 7,456 | 30 | 5.4 | 6.0 | 0 | 0 | 41.4 |
| 66 | **72** | `readiness-gates-residual-escrow-and-quarantine` | 9,517 | 30 | 4.8 | 7.5 | 0 | 0 | 42.3 |
| 67 | **72** | `spinoza-verification-and-proof-carrying-claims` | 7,945 | 30 | 3.1 | 3.0 | 0 | 5 | 41.1 |
| 68 | **73** | `ai-work-surfaces-agent-harnesses-and-organizational-absorption` | 4,787 | 30 | 5.2 | 0.0 | 0 | 5 | 40.2 |
| 69 | **74** | `procedural-memory-and-cognitive-loop-closure` | 9,425 | 30 | 2.7 | 1.5 | 0 | 5 | 39.2 |
| 70 | **74** | `rankfold-neuralfold-and-artifact-compression` | 9,255 | 20 | 5.9 | 7.5 | 0 | 5 | 38.4 |
| 71 | **74** | `routing-heads-and-specialist-cores` | 11,375 | 30 | 4.0 | 4.5 | 0 | 0 | 38.5 |
| 72 | **75** | `fast-generation-architectures` | 12,723 | 20 | 3.5 | 6.0 | 8 | 0 | 37.5 |
| 73 | **76** | `asi-is-a-stack-not-a-model` | 7,011 | 20 | 5.7 | 4.5 | 0 | 5 | 35.2 |
| 74 | **76** | `governed-model-training-distributed-optimization-and-scaling` | 9,274 | 20 | 9.2 | 6.0 | 0 | 0 | 35.2 |
| 75 | **76** | `moral-uncertainty-and-value-conflict` | 7,136 | 20 | 5.6 | 4.5 | 0 | 5 | 35.1 |
| 76 | **76** | `white-box-evidence-interpretability-and-activation-governance` | 7,131 | 20 | 7.0 | 4.5 | 0 | 5 | 36.5 |
| 77 | **77** | `dangerous-capability-domains-and-misuse-uplift` | 5,176 | 20 | 7.8 | 1.5 | 0 | 5 | 34.3 |
| 78 | **77** | `open-ended-improvement-engines` | 6,339 | 20 | 1.6 | 3.0 | 0 | 10 | 34.6 |
| 79 | **79** | `governed-world-models-and-reality-grounding` | 9,257 | 20 | 3.2 | 3.0 | 0 | 5 | 31.2 |
| 80 | **79** | `scalable-oversight-and-adversarial-ai-control` | 7,280 | 20 | 2.8 | 3.0 | 0 | 5 | 30.8 |
| 81 | **80** | `model-weight-custody-and-hardware-roots-of-trust` | 9,747 | 20 | 4.1 | 6.0 | 0 | 0 | 30.1 |
| 82 | **82** | `evidence-states-and-claim-discipline` | 7,283 | 20 | 2.8 | 4.5 | 0 | 0 | 27.3 |
| 83 | **82** | `virtual-context-abi` | 9,597 | 20 | 5.2 | 1.5 | 0 | 0 | 26.7 |
| 84 | **83** | `the-efficient-asi-hypothesis` | 7,362 | 20 | 4.1 | 1.5 | 0 | 0 | 25.6 |
| 85 | **87** | `confidential-and-verifiable-ai-computation` | 4,678 | 0 | 8.6 | 1.5 | 0 | 10 | 20.1 |

---

## 5. Recommended order of work

1. **The three narrative anchors** — `project-theseus` (#1), `integrated-
   reference-architecture`, and `resource-economics-and-token-budgets`. These
   are the chapters where one worked example changes how the whole book reads.
2. **The universal hedging cut** across all 84 chapters — mechanical, removes
   820 disclaimer phrases' worth of drag, needs no new research.
3. **Sourcing fixes** for the chapters at 1–5 external sources on
   well-documented topics: `circle-calculus` (1), `autonomous-replication` (1),
   `planning-as-a-control-layer` (1), `relational-dimension-compilation` (1),
   `scientific-discovery` (1), `adversarial-machine-learning` (5),
   `multi-agent-dynamics` (5).
4. **Worked examples for the rest**, ordered by score ascending.
5. **Regenerate the Human Reading Path blocks** against their subjects rather
   than a word budget.

## 6. What this review does not claim

No statement about the correctness of any claim, the adequacy of any proof, the
validity of any evidence transition, or any support state. Scores measure prose
delivery only.

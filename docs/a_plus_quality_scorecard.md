# A+ Quality Scorecard

Last updated: 2026-06-29

This scorecard translates the current project critique into concrete A+ targets.
It is a planning artifact, not evidence, not an external review, and not a
support-state transition.

The core diagnosis is simple: **The ASI Stack** is already unusually strong as
a disciplined living-book system, but it is still weak as a validated body of
knowledge. The v1.x roadmap should move both the reality and the cold-read
perception.

## North Star

A future A+ version should be:

- legible in 60 seconds to a skeptical reader;
- externally reviewed before it asks readers for belief;
- deep on a few defended contributions, not shallow across 54 topics;
- structurally willing to consolidate repeated chapter skeletons into fewer
  deeper chapters while preserving every claim, source, proof, and reader path;
- externally grounded chapter by chapter, so Corben-originated terms are
  related to known literature, systems, standards, and benchmarks before they
  are presented as architecture vocabulary;
- evidence-backed through public-safe replay, CI-verifiable artifacts,
  source-noted literature, Lean invariants, or explicit no-promotion records;
- readable as a human book while preserving the live AI/research book as the
  canonical evidence surface.

## Grade Closure Map

| Dimension | Current risk | A+ condition | Roadmap owner |
|---|---|---|---|
| Ambition and scope | The scope is coherent but can look like a theory-of-everything. | The public surface says the book is a research program with a small defended contribution set inside a broader architecture. | `docs/v1_x_beyond_sota_roadmap.md#milestone-05---sixty-second-trust-surface` |
| Epistemic honesty | Strong internally, but too hidden from cold readers. | A first-time visitor immediately sees current claim states, non-claims, validation, and what is unproven. | Milestone 0.5 and Milestone 1 |
| Engineering system | Strong, but can feel like process for process's sake. | The validation system is framed as the main methodological contribution and is checked by external review. | Milestone 1.5 and Contribution Track 1 |
| Core thesis | Sound but not obviously novel relative to compound/agentic systems. | The thesis is positioned as a synthesis architecture; novelty is claimed only for the specific mechanisms that survive prior-art review. | Milestone 6 and Milestone 9 |
| Distinctive ideas | Many promising ideas compete for attention. | Three to five contribution tracks are selected and defended to real depth. | Contribution Track Selection |
| Rigor and soundness | Internally coherent, but much is still argument-level. | Load-bearing claims have explicit formal, source, prototype, or review evidence; failed claims are demoted; each selected lane names a proof/evidence path or no-promotion blocker. | Milestones 2, 3, 4, 5, 5.5 and Negative Outcomes |
| Evidence | Three narrow non-core transitions exist, one Project Theseus static architecture-gate import is CI-verifiable by digest, and one Circle consumer gate is CI-verifiable by digest plus negative controls, but evidence remains thin. | At least one selected Theseus or Circle lane moves beyond guarded public fixtures into clean replay, archived public packs, or accepted bounded transitions where the evidence justifies it, and selected chapter-adjacent claims have accepted transitions. | Milestones 3, 4, and v1.x release gate |
| Formal rigor | Most Lean theorems are projection-style. | Safety-critical modules include derived/decomposed theorems, anti-projection conclusions, and negative cases. | Milestone 2 |
| Human readability | Human view exists, but many chapters remain dense and spec-like. | A curated reader pilot reads like a book and preserves evidence boundaries. | Milestone 7 |
| Structural cohesion | The 54-chapter shape is useful for coverage, but some overlapping clusters repeat the same skeleton around adjacent claims. | The governed consolidation sequence is reviewed cluster by cluster; accepted merges become deeper one-skeleton chapters, rejected merges stay separate with reasons, and no idea is silently dropped. | Milestone 6.5 |
| External grounding | External positioning exists, but literature was added late and unevenly. | Every chapter has a source-noted external comparator, adjacent literature family, candidate backlog, or explicit exception; likely sources are mined first from the chapter's linked Corben-paper bibliographies. | Milestone 5.5, Milestone 6, and Milestone 9 |
| Researcher/AI usefulness | Useful as a structured reference today. | Useful as a reproducible research program with selected defended contributions and clear open problems. | v1.x evidence release gate |
| Field impact odds | Low until external review and defended results exist. | At least one external reviewer, one reproducible evidence lane, and one prior-art-reviewed contribution extraction exist. | Keystone set |

## Defended Contribution Tracks

The project should not try to make all 54 chapters equally defensible in the
next cycle. It should select three to five contribution tracks and push those to
real depth.

Candidate tracks:

1. **Living evidence book methodology**
   - Claim: a technical book can be a CI-gated evidence system rather than a
     static anthology.
   - A+ bar: external review, release-gate record, visible non-core evidence,
     no-claim enforcement, and reproducible validation instructions.
2. **Claim support states and evidence laundering prevention**
   - Claim: support states, residuals, failed attempts, and non-claims should be
     first-class engineering objects.
   - A+ bar: non-core evidence ledger, Appendix C linkage, demotion/refutation
     path, and one source-noted prior-art/novelty comparison.
3. **Governed self-improvement boundary**
   - Claim: recursive improvement should be modeled as a bounded transition
     through protected invariants, evaluator independence, rollback, and
     residual custody.
   - A+ bar: safety-critical Lean depth, negative case, external safety review,
     and a public-safe Theseus architecture-gate trace or explicit blocker.
     The current static import clears the digest-verifiable trace boundary but
     still needs a clean live replay or archived public release before it can
     carry more than implementation-reference weight.
4. **Proof-carrying claims and proof-carrying AI contracts**
   - Claim: AI claims and cyclic/contract artifacts can carry checkable proof
     receipts without implying model quality.
   - A+ bar: the current Circle consumer gate is strengthened with clean replay
     or a vendored/archived public contract pack, malformed receipt negative
     controls stay enforced, and a source-noted proof-carrying-code baseline is
     added.
5. **Costed routing, residual accounting, and resource discipline**
   - Claim: routing decisions should be judged by adequacy, cost, residuals,
     fallback, and hidden/displaced cost, not cheapness alone.
   - A+ bar: extend the synthetic slice or record a public-safe trace with
     baseline, negative control, adequacy, cost, residuals, and no economic
     overclaim.

Selection rule: a future v1.x run should choose at most three tracks for deep
work before it widens to more. Track selection should prefer external review,
public replay, and source-noted novelty over internal fixture count.

Current selection: `docs/defended_contribution_tracks.md` selects all five
candidate tracks for v1.x focus and marks three as current deep-work tracks.
The selection record is a release-control surface only; it does not claim A+
completion or support-state movement. `docs/defended_contribution_prior_art_positioning.md`
now records a source-noted prior-art positioning pass for those five tracks,
including the remaining novelty, review, replay, proof, and routing
residual-governance gaps; it is not an external review, novelty proof, or
support-state transition.

## Cold-Read Risk Controls

A skeptical visitor should not have to inspect the repository to discover that
the project is honest. The README, landing page, and Human view should make
these facts visible quickly:

- all 54 chapter core claims remain `argument`;
- three bounded non-core transitions exist and are narrow;
- Lean coverage is broad but still shallow in safety-critical areas;
- external literature is an active grounding workstream, not a completed claim
  that every chapter is already well-cited;
- Project Theseus and Circle are related local/public projects; the current
  Theseus static import, Circle local receipt slice, and Circle consumer-gate
  fixture are narrow evidence lanes, not chapter-core promotions or independent
  third-party audits;
- external review is requested or pending;
- the book is a research program, not a validated ASI implementation.

## Non-Claims

- This scorecard does not grade the project as an external authority.
- This scorecard does not create external review, source-derived support,
  evidence transitions, proof results, reader artifacts, or release approval.
- This scorecard does not add new external sources, source notes, proof results,
  support-state transitions, or Circle replay artifacts beyond the separate
  tracked Project Theseus static import recorded in
  `docs/theseus_report_import_slice.md` and the separate Circle public consumer
  gate recorded in `docs/circle_public_replay_consumer_gate.md`.
- This scorecard does not promote any chapter core claim above `argument`.

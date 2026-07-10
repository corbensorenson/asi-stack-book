# Systems and Editorial External Review Packet

Status: ready for assignment; no reviewer assigned. Last updated: 2026-07-10.

## Reviewer capacity and independence

Use the `systems_editorial_reviewer` capacity role. The reviewer should cover
AI/software systems and experimental design, with technical-editing or
publishing judgment for the narrative product. A two-person review may split
systems and editorial competence, but each person's scope, conflicts, load,
response window, and authority must be recorded.

## Review boundary

This track tests whether the project is a coherent book and credible systems
program rather than an impressive administrative apparatus. It must distinguish
the narrative book, architecture reference, and evidence registry; evaluate
the three defended contributions rather than every coined term; and challenge
whether the vertical slice supports the prose it is used near. It does not
approve publication or establish novelty.

## Required artifacts

1. `README.md`, `index.qmd`, and a rendered Human view
2. `products/product_contracts.json`, `products/narrative_product_spine.json`,
   `docs/product_contracts.md`, and `docs/product_projection_artifacts.md`
3. `products/contribution_focus_contract.json` and `docs/three_defended_contributions.md`
4. `docs/governed_repository_change_slice.md`
5. `docs/governed_trace_invariants.md`
6. `docs/evidence_quality_vectors.md`
7. The generated 15-chapter narrative candidate, its product page and manifest,
   `docs/reader_continuity_audit.md`, and one representative curated chapter
8. `chapters/asi-is-a-stack-not-a-model.qmd`
9. `chapters/integrated-reference-architecture.qmd`
10. `docs/v1_x_beyond_sota_roadmap.md`

## Required questions

1. Can a new reader explain the book's three contributions after ten minutes?
2. Does the narrative product read continuously, or does release/evidence
   machinery repeatedly interrupt the argument?
3. Does the 15-chapter selection preserve the book's thesis-to-method arc, and
   are any of the 39 reference-routed chapters essential enough to replace a
   selected chapter? Name the replacement and tradeoff.
4. Are architecture-reference fields discoverable without making every
   chapter feel like a template?
5. Does the evidence registry expose the important negative state quickly, or
   reward readers for counting validators and theorems?
6. Is the repository-change workload representative enough to justify any
   systems-level governance or overhead statement? Identify the transfer gap.
7. Are the matched baseline, metrics, attacks, cost and latency accounting,
   operator burden, and rollback measurements fair?
8. Which terms duplicate established systems language and should be renamed,
   subordinated, or explicitly positioned?
9. Which chapters repeat one contribution without adding a distinct mechanism,
   failure mode, or empirical obligation?
10. Does the ASI framing clarify a stress case or impose avoidable credibility
   cost? Give concrete subtitle/framing alternatives without assuming authority
   to rename the work.
11. What is the smallest editorial and empirical program that would make the
    next release materially more credible?

## Adversarial review prompts

- Remove validator/theorem counts and ask whether the contribution remains clear.
- Compare the governed slice with a competent lightweight baseline rather than
  an intentionally permissive one.
- Read Human view without repository context and mark every administrative stop.
- Replace coined terms with standard systems terms and note any lost content.
- Treat the three products as separate deliverables and identify leaked density.

## Severity and disposition rubric

| Severity | Meaning | Default route |
|---|---|---|
| Critical | Public product or experiment materially misrepresents current evidence or release reality. | Block release claim; repair source and rendered surfaces. |
| High | Contribution, baseline, transfer, or reader contract is not credible at current framing. | Narrow/restructure and add empirical or editorial gate. |
| Medium | Repetition, jargon, navigation, or density significantly harms comprehension. | Consolidate prose/product routing with regression check. |
| Low | Local wording, figure, discoverability, or polish issue. | Editorial backlog. |

Use `accept`, `accept_with_narrowing`, `revise`, `block`, or
`reject_finding_with_reason` and name the artifact that would close the issue.

## Required response record

Provide finding ID, severity, product and contribution affected, exact surface,
reader/system failure, evidence inspected, proposed edit or experiment,
acceptance test, residual if deferred, and attribution boundary. Separate
systems findings from taste preferences and publication approval.

## Non-claims

- Packet readiness is not independent review.
- Packet readiness is not systems validation, editorial acceptance, novelty
  review, publication approval, or reader-release approval.
- A positive review cannot promote a chapter claim by itself.
- A coherent book does not imply an implemented, efficient, safe, or novel system.

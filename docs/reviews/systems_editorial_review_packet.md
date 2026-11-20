# Systems and Editorial External Review Packet

Status: ready for assignment; no reviewer assigned. Last updated: 2026-07-10.

## Focused post-publication review of effect reconciliation

**Purpose.** Assess the finding that receiving-service observation closes
some ambiguous operations that ordinary scoped Git change control correctly
leaves on hold. This request focuses on one comparison and its inference.

Use the source commit named by the snapshot invitation. From a clean checkout
with Python 3 and Git, run:

```bash
python3 scripts/compare_fresh_effect_workflows.py > /tmp/asi-fresh-effect-result.json
cmp /tmp/asi-fresh-effect-result.json \
  experiments/p5_u1_governed_repository_change/results/2026-11-20-fresh-effect-comparison.json
```

1. Reproduce the ten known-answer calibration cases and all 16 pairs.
   Report the commit, runtime versions, any failed reproduction, and the
   smallest record that exposes a discrepancy.
2. Inspect the conventional workflow's safe hold and deduplicated retry.
   Identify a competent conventional control that could close the four
   additional cases with similar observer access or less work. Separate its
   requirements from changes to the task or sink contract.
3. Check whether the receiving observation proves the effect with the
   payload and destination the request authorized. Identify a counterexample
   that would require a stronger receipt or a narrower claim.
4. Review the public wording against the denominator. The receiver is a
   scripted SQLite journal and the tasks are authored. Estimate neither
   production incidence nor human labor from these results.

Include independence or conflicts, evidence for each finding, and permission
to quote or publish your response. The project will record what changed
against the pinned revision. [Protocol](../../experiments/p5_u1_governed_repository_change/fresh_task_protocol.md) · [Raw paired outcomes](../../experiments/p5_u1_governed_repository_change/results/2026-11-20-fresh-effect-comparison.json)

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
7. The generated 22-unit narrative candidate, its product page, manifest,
   exact 84-chapter unit crosswalk, `docs/reader_continuity_audit.md`, and one
   representative compound unit
8. `chapters/asi-is-a-stack-not-a-model.qmd`
9. `chapters/integrated-reference-architecture.qmd`
10. `docs/v1_x_beyond_sota_roadmap.md`

## Required questions

1. Can a new reader explain the book's three contributions after ten minutes?
2. Does the narrative product read continuously, or does release/evidence
   machinery repeatedly interrupt the argument?
3. Does the 22-unit selection preserve the book's thesis-to-method arc, and
   does every one of the 62 reference-routed chapters have a semantically
   appropriate unit owner? Name any rerouting and tradeoff.
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

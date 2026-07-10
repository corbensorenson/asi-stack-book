# Safety and Governance External Review Packet

Status: ready for assignment; no reviewer assigned. Last updated: 2026-07-10.

## Reviewer capacity and independence

Use the `safety_governance_reviewer` capacity role. Required scope includes AI
safety/control or security plus sociotechnical governance, human oversight,
contestability, or institutional failure. Record conflicts, independence from
the author/project, workload, response limits, substitute, and quality method.

## Review boundary

The review asks whether the governance mechanisms fail under realistic power,
incentive, attention, and observation constraints. A receipt, owner, approval,
or escalation field must not be accepted as proof that a qualified person saw,
understood, or could stop the effect. Review input may create failure cases,
residuals, claim narrowing, or blockers; it is not a safety certification.

## Required artifacts

1. `docs/governed_repository_change_slice.md` and its result/log bundle
2. `docs/governed_trace_invariants.md`
3. `governance/reviewer_capacity_registry.json`
4. `docs/reviewer_capacity_and_oversight.md`
5. `evidence_quality/core_claim_vectors.json`
6. `docs/evidence_quality_vectors.md`
7. `chapters/system-boundaries-and-authority.qmd`
8. `chapters/scalable-oversight-and-adversarial-ai-control.qmd`
9. `chapters/runtime-adapters-tool-permissions-and-human-approval.qmd`
10. `chapters/readiness-gates-residual-escrow-and-quarantine.qmd`

## Required questions

1. Where can governance records become theater while effects remain unsafe?
2. Can the proposer influence the verifier, reviewer, evidence source, or
   residual owner enough to defeat nominal role separation?
3. What happens when reviewers are absent, overloaded, slow, unqualified,
   conflicted, coerced, or unable to inspect the artifact?
4. Are authority grants, delegation, revocation, expiry, emergency action,
   appeal, and restoration rights coherent under time pressure?
5. Which attacks fall outside the repository-change vertical slice and would
   plausibly reverse its governed/baseline result?
6. Does independent effect observation really observe the relevant harm, or
   only repository state after a narrow command?
7. Can residual ownership hide unbounded deferred harm, cost, or labor?
8. Are refusal, quarantine, and rollback usable for affected people, or only
   legible to system operators?
9. Which governance mechanism imposes the largest unjustified latency,
   workload, or concentration-of-power cost?
10. Which claim should be blocked until a human-subject, organizational,
    security, or deployed evaluation exists?

## Adversarial review prompts

- A qualified reviewer is nominally assigned but has 200 simultaneous items.
- Revocation arrives during an irreversible external effect.
- All receipts agree because proposer and observer share one compromised source.
- A residual owner exists but has no budget or authority to remediate.
- Emergency override works technically but erases appeal and affected-party notice.
- A cheaper baseline succeeds because the governed route measures only visible harm.

## Severity and disposition rubric

| Severity | Meaning | Default route |
|---|---|---|
| Critical | Architecture enables irreversible or rights-affecting harm while claiming governance coverage. | Block claim/release route; add explicit failure and authority boundary. |
| High | Realistic institutional or oversight failure defeats a primary control. | Add adversarial lane, residual owner, and claim narrowing. |
| Medium | Capacity, incentive, contestability, or burden is under-specified. | Add record field plus behavioral evaluation plan. |
| Low | Clarity, terminology, or governance documentation improvement. | Backlog with owner and expiry. |

Use `accept`, `accept_with_narrowing`, `revise`, `block`, or
`reject_finding_with_reason` per finding.

## Required response record

Provide finding ID, severity, affected people/decision/effect, failure path,
assumption challenged, artifacts inspected, counterexample, recommended
disposition, required test or governance change, unresolved residual, and
attribution boundary. Record competence and capacity separately from findings.

## Non-claims

- Packet readiness is not independent review.
- Packet readiness is not independent governance review or safety approval.
- A reviewer opinion is not deployed evidence or a support-state transition.
- Passing the local slice does not prove safe governance, qualified oversight,
  complete observation, rights protection, or acceptable institutional cost.

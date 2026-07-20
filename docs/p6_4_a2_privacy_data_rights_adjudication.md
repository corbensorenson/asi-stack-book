# P6.4-A2 adjudication: privacy, data rights, and information-flow governance

Date: 2026-07-19
Candidate: `privacy-data-rights-and-information-flow-governance`
Decision: **admit at argument support**
Manifest effect: one Part I chapter after Security Kernel and before Model-Weight Custody
Empirical/support/release/legal-compliance effect: none

## Decision

The candidate survives the source, boundary, competence, and reader-value
gates. It owns a previously fragmented transaction: whether information about a
person or affected group may move from collection through context, memory,
training, inference, output, audit, sharing, derivatives, correction, export,
deletion, and retirement for the exact purpose and authority claimed.

Security prevents unauthorized access. Privacy must also govern harmful
**authorized** processing. Data Engines owns datum admission, lineage, learning,
and unlearning mechanics, but not the purpose lease, subject-facing rights,
privacy accounting, inference risk, or remedies. Moral Uncertainty governs
contested values, not the execution of a rights request. The new owner answers a
question none of those chapters answers end to end: **is this information use
still within its purpose, rights, disclosure, privacy-loss, and remedy envelope?**

## Four-role source gate

| Required role | Admitted primary or official sources | Contribution | Ceiling |
|---|---|---|---|
| Mechanism or capability | Abadi et al.; W3C DPV v2; AlgoSpec | DP-SGD and accounting; machine-readable purpose/processing/rights vocabulary; a concrete purpose-restriction design. | Source mechanisms are not locally implemented, reproduced, or universal. DPV is a Community Group specification, not a W3C Recommendation. |
| Limitation or failure | Carlini et al.; Choquette-Choo et al.; NIST Privacy Framework | Training-data extraction, label-only membership inference, confidence-masking failure, and privacy harm from ordinary authorized processing. | Attacks are configuration-bound and do not prove leakage in every model or identify a lawful remedy. |
| Competing design | NIST Privacy Framework; GDPR; W3C DPV; AlgoSpec | Risk/outcome governance, jurisdiction-specific rights and principles, semantic policy records, and algorithm-specific restriction expose alternatives to access control or DP alone. | The book does not adjudicate law, certify compliance, or select one universal regime. |
| Measurement or evaluation | NIST SP 800-226; Mahloujifar et al.; GDPR | DP implementation-evaluation hazards, one-run empirical auditing, and accountable rights receipts. | An empirical audit can catch some flaws; it cannot prove the implementation, full lifecycle privacy, or legal compliance. |

The nine source notes record exact review basis, mechanisms, evidence, failure
modes, uses, and open questions. NIST Privacy Framework 1.0 remains the stable
official baseline; the still-draft 1.1 work is named only as a currentness note.
GDPR is used as one jurisdiction's authoritative vocabulary and never as
universal law or evidence that the ASI Stack complies with it.

The pinned `theseus_synthetic_data_curation` record is a separate local
implementation-pressure source. It contributes provenance receipts, split
exclusions, leakage gates, bounded synthetic-data admission, derivative
propagation, and revocation questions. No Theseus command or dataset was rerun,
and the record supplies no privacy, rights-completion, deletion, influence-
removal, data-quality, model-benefit, or compliance evidence.

## Exclusive-owner test

| Neighbor | Why returning the candidate there fails |
|---|---|
| Security Kernel | Authorized collection, inference, linkage, purpose drift, over-retention, and surveillance can be privacy failures without a security breach. |
| Data Engines | Learning and unlearning operations do not decide lawful basis, consent, purpose compatibility, correction/export response, privacy budget, or subject remedy. |
| Context Transactions | Taint and context isolation do not carry rights across training artifacts, outputs, audits, and downstream derivatives. |
| Model-Weight Custody | Holder/use authority for weights is not authority to process each person's data or satisfy each lifecycle right. |
| Moral Uncertainty | Value contestability does not implement purpose leases, minimization, privacy accounting, or rights receipts. |
| Governance, Rights, Fork, Exit, and Audit | Organizational exit and remedy governance cannot reconstruct the information-flow and derivative-obligation graph needed to execute a data right. |

Removing the chapter leaves purpose drift, cross-user memory, derivative rights,
privacy-budget composition, inference attacks, and deletion theater without one
reader owner. Its Part I placement is therefore necessary: the Security Kernel
controls access; this chapter controls permitted information use; Weight Custody
then controls model-family artifacts.

## Competence burden

The schema, fixture, validator, and Lean module are development controls only.
They establish consequences of authored predicates, not privacy in a deployed
system. A claim-bearing campaign must:

1. use an open, natural workload containing consent- and purpose-labeled data
   plus a realistic memory and small-model path;
2. compare ordinary processing, access control, minimization, DP, purpose-bound
   enforcement, and competent unlearning/remediation under matched utility and
   tuning opportunity;
3. freeze data subjects, affected groups, purposes, uses, recipients,
   retention, derivative rules, privacy unit, adjacency relation, accountant,
   threat model, attacks, rights requests, and nonclaims before outcomes;
4. demonstrate attack and rights-workflow positive controls before interpreting
   a null extraction, membership, correction, export, or deletion result;
5. use strong extraction and membership attacks, including label-only access,
   with an independently implemented evaluator;
6. trace raw records, context, memory, checkpoints, models, caches, logs,
   outputs, backups, and descendants rather than treating one storage deletion
   as total removal;
7. separate storage erasure, access revocation, behavioral forgetting,
   influence reduction, privacy loss, and legal-right completion;
8. retain every subject, canary, attempted attack, exclusion, rights request,
   failure, model, and configuration in its denominator;
9. measure utility, extraction, membership advantage at low false-positive
   rates, privacy accounting, flow coverage, purpose violations, rights latency
   and completeness, residual copies/influence, operator work, and resource
   cost together; and
10. invalidate rather than interpret a campaign with an incompetent baseline,
    broken attack, unverified lineage, undefined privacy unit, leaked held-out
    outcomes, lost denominator, or unexecutable rights request.

This burden prevents a naive defense or weak attack from creating a false
negative. No negative result may narrow the architecture unless the named
failure mode had a demonstrated opportunity to occur and be detected.

## Reader value

The chapter supplies four concepts readers cannot reliably reconstruct from its
neighbors:

- access authority, consent, purpose, and privacy guarantee are distinct;
- information rights must propagate through a visible derivative graph while
  explicitly recording unknown copies and influence;
- privacy claims require both formal parameters and implementation/attack
  evaluation; and
- a rights receipt must state what was corrected, exported, restricted,
  deleted, retained by exception, or left unresolved.

## Nonclaims and terminal disposition

Admission changes only the book's argument structure. It establishes no consent,
lawful basis, legal interpretation, compliance, privacy guarantee, differential
privacy implementation, successful attack, successful deletion, model
unlearning, group remedy, safety, support transition, readiness, release,
publication, transfer, SOTA, AGI, or ASI claim.

P6.4-A2 is terminal when the manifest, chapter, nine-source packet, source
matrix, glossary/outline/handoffs, transaction contract, formal targets,
prospective campaign, reader audit, validators, generated surfaces, render, and
clean-main attestation agree. Empirical work remains owned by the frozen
campaign and does not reopen the structural decision.

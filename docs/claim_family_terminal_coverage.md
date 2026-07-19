# Claim-family terminal coverage receipt

## Decision

The repository-wide CF-01 through CF-08 terminal audit is complete for its
frozen denominator of 3,745 structured claim atoms. This is a terminal
**disposition audit**, not a declaration that the book's claims are proved.
Every atom now has one exact outcome, every block names the proof lanes that
remain absent, and no chapter-core claim moved upward.

The authoritative machine result is
`experiments/claim_family_terminal_coverage/results/result.json`. The frozen
design, preregistration, preflight receipt, schema-repair receipt, and rejecting
validator preserve the attempt's lineage.

## Prospective lineage

The program froze a 3,745-atom denominator: 3,730 activation atoms plus the 15
atoms in the accepted replaceable-cognitive-substrates addendum. Before outcome
generation, the preflight rehashed all seven frozen inputs and recorded that
the result file did not yet exist. The evaluator then ran exactly once. Its
three attempt lanes all passed:

1. the PR validation registry;
2. the deep validation registry; and
3. the full Lean build.

The first generated result inherited two obsolete `nonmaterial_context`
labels from the frozen registry. Because that label was outside the terminal
schema, the validator rejected the result. The evaluator was not rerun. A
scope-limited repair changed only those two labels to
`blocked_after_full_attempt`, preserved their already recorded missing
`normative` lane, and recorded the original result digest. The repair therefore
makes the result more conservative and cannot manufacture support.

## Exact outcomes

| Family | Atoms | Blocked | Retained | Narrowed | Bounded promotion |
|---|---:|---:|---:|---:|---:|
| CF-01 | 274 | 234 | 36 | 3 | 1 |
| CF-02 | 559 | 555 | 0 | 4 | 0 |
| CF-03 | 457 | 457 | 0 | 0 | 0 |
| CF-04 | 524 | 522 | 0 | 2 | 0 |
| CF-05 | 390 | 390 | 0 | 0 | 0 |
| CF-06 | 539 | 538 | 0 | 0 | 1 |
| CF-07 | 545 | 545 | 0 | 0 | 0 |
| CF-08 | 457 | 457 | 0 | 0 | 0 |
| **Total** | **3,745** | **3,698** | **36** | **9** | **2** |

The two bounded promotions are not chapter-core claims:

- `system-boundaries-and-authority.invariant.001` preserves the accepted
  finite no-silent-expansion synthetic-test transition; and
- `circle-calculus-and-proof-carrying-ai-contracts.mechanism.003` preserves
  the accepted named-target and compiled-declaration receipt transition.

The nine narrowings preserve already accepted transition lineage. They cover
the constitutional-alignment, moral-uncertainty, stable-capability-field,
capability-replacement, rollback-outcome, security-kernel, recursive-
self-improvement, claim-ledger, and Spinoza core or subordinate atoms. None is
an upward support movement.

## What remains unproved

The 3,698 blocks are the principal result. The most common missing-lane
combinations are:

| Missing lanes | Atoms |
|---|---:|
| normative and transfer | 2,068 |
| causal, empirical, executable, formal, normative, and transfer | 1,299 |
| causal, empirical, normative, and transfer | 155 |
| causal, empirical, formal, normative, and transfer | 76 |
| empirical, causal, and transfer | 15 |

The exact per-atom lists remain in the machine result rather than being
duplicated into prose. A block means that the locally available repository
attempt was exhausted under the frozen audit and the named lanes still lack an
adequate route. It does not mean that the claim is false, successful, proved,
externally reproduced, transferable, safe, deployable, or ready for release.

The audit also does not satisfy the broader P5 completion gate by itself. That
gate separately requires at least one competent end-to-end or natural-work
bundle for every claim family, with relevant negative controls. Those family
campaigns remain work even though per-atom terminal gaps are now explicit.

## Mutation and authority boundaries

The validator rejects four laundering mutations: denominator loss, invented
chapter-core promotion, unsupported promotion, and erased missing lanes. The
result grants no publication or release authority. Its support effect is only
to preserve previously accepted exact transitions; it creates zero new
chapter-core movement.


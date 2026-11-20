# Generalization in Adaptive Data Analysis and Holdout Reuse

| Field | Value |
|---|---|
| Source ID | `ext_adaptive_holdout_reuse_2015` |
| Publication | Cynthia Dwork et al. (2015). [Primary source](https://arxiv.org/abs/1506.02629v2) |

## Thesis

The paper studies generalization under adaptive data reuse and gives algorithms for controlled reuse with formal conditions.

## Mechanisms

Iterating on results observed from a holdout can adapt the selection procedure to that holdout. Restricted mechanisms can support particular reusable validity guarantees.

## Evidence

The book uses the selected source passage for the decision in “Keep track of what the holdout taught the designer”.
The worked example is illustrative.

## Failure Modes

The guarantees depend on the mechanism and assumptions. Repeated conventional scoring does not inherit them. The paper's illustrative experiment is synthetic.

## Book Chapters Supported

- `benchmark-ratchets-and-anti-goodhart-evidence`

## Claims To Add Or Update

Use the source as a comparator for the chapter's worked decision.
Retain the evidence state of the chapter's core claim.

## Open Questions

What observation from the worked example would justify acting when the
source's assumptions or measured setting do not carry over?

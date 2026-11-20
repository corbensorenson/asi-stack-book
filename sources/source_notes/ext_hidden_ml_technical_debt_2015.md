# Hidden Technical Debt in Machine Learning Systems

| Field | Value |
|---|---|
| Source ID | `ext_hidden_ml_technical_debt_2015` |
| Publication | D. Sculley et al. (2015). [Primary source](https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf) |

## Thesis

The authors identify boundary erosion, entanglement, undeclared consumers and hidden feedback loops as sources of maintenance cost in ML systems.

## Mechanisms

Changing one shared data dependency or feature can change several consumers' behavior and create work for teams that did not request the change.

## Evidence

The book uses the selected source passage for the decision in “A temporary exception gains consumers”.
The worked example is illustrative.

## Failure Modes

This is a set of design observations and maintenance risks. It does not compare the book's proposed persistence policy against a baseline.

## Book Chapters Supported

- `adjudicated-persistence-and-the-adaptive-commit-boundary`

## Claims To Add Or Update

Use the source as a comparator for the chapter's worked decision.
Retain the evidence state of the chapter's core claim.

## Open Questions

What observation from the worked example would justify acting when the
source's assumptions or measured setting do not carry over?

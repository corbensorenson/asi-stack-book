# End-to-End Arguments in System Design

| Field | Value |
|---|---|
| Source ID | `ext_end_to_end_arguments_1984` |
| Publication | Jerome H. Saltzer, David P. Reed, and David D. Clark (1984). [Primary source](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf) |

## Thesis

The paper uses duplicate suppression and delivery acknowledgment to show how the application's requirements determine where a correctness check belongs.

## Mechanisms

A sender's attempt, the receiver's durable commit, and consumption by the intended application are different endpoints. Lower layers can reduce common failures or improve performance. The application still has to verify the semantics it promises.

## Evidence

The book uses the selected source passage for the decision in “Which endpoint can witness the claim?”.
The worked example is illustrative.

## Failure Modes

The argument concerns the placement of correctness functions. A receiving journal supports a durable-commit claim under stated assumptions. It leaves delivery and consumption open when those occur at a later boundary.

## Book Chapters Supported

- `runtime-adapters-tool-permissions-and-human-approval`

## Claims To Add Or Update

Use the source as a comparator for the chapter's worked decision.
Retain the evidence state of the chapter's core claim.

## Open Questions

What observation from the worked example would justify acting when the
source's assumptions or measured setting do not carry over?

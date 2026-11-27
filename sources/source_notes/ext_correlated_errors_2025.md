# Correlated Errors in Large Language Models

| Field | Value |
|---|---|
| Source ID | `ext_correlated_errors_2025` |

Elliot Kim, Avi Garg, Kenny Peng, Nikhil Garg. [Primary paper, arXiv 2506.07962v1](https://arxiv.org/html/2506.07962v1).

## Thesis

Agreement among fallible judges depends on the errors they share.

## Mechanisms

Compare the probability of matching wrong answers given joint failure with the probability of error given agreement.

## Evidence

In the HELM comparison, pairs chose the same wrong alternative about 60% of the time when both were wrong. Uniform independent selection among three wrong alternatives gives one third.

## Failure Modes

HELM paired-error analysis. This conditional rate alone leaves the frequency of joint failures and the accuracy of consensus unspecified. Task mixture and shared dependencies matter.

## Book Chapters Supported

- `verification-bandwidth-and-context-adequacy` — [How much evidence is a second opinion?](https://corbensorenson.github.io/asi-stack-book/chapters/verification-bandwidth-and-context-adequacy.html#how-much-evidence-is-a-second-opinion)

## Claims To Add Or Update

Estimate joint failures on the target task before treating a second vote as independent evidence.

## Open Questions

At fixed coverage, does changing the evidence source reduce joint errors more than adding a judge?

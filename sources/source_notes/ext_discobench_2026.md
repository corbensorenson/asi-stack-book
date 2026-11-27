# When Search Agents Should Ask: DiscoBench for Clarification-Aware Deep Search

| Field | Value |
|---|---|
| Source ID | `ext_discobench_2026` |

Tao et al. (2026). [Primary publication](https://arxiv.org/html/2606.27669v2).

## Thesis

Recognizing ambiguity and asking the particular question that resolves it require different decisions.

## Mechanisms

Score the question against the distinguishing clue, the next search decision and the interaction cost.

## Evidence

The authors evaluated 463 ambiguity instances in 211 search tasks across 11 domains. Models could detect an ambiguity yet ask a question that failed to resolve it.

## Failure Modes

Sections 4–5, limitations, and Appendix F. The user simulator reveals clues in
objective question-answering tasks. Appendix F specifies that the same
auxiliary model plays the user and judges intermediate steps. This gives the
two roles a shared dependency. Evaluating preferences, consent, or the cost
of interrupting real users requires different observations.

## Book Chapters Supported

- `human-intent-as-a-formal-input` — [Which release did the customer see?](https://corbensorenson.github.io/asi-stack-book/chapters/human-intent-as-a-formal-input.html#which-release-did-the-customer-see)

## Claims To Add Or Update

Check whether the reply changes the search path and whether the extra interaction was worth its cost.

## Open Questions

Would the same clarification policy still help with an actual user who can decline to answer?

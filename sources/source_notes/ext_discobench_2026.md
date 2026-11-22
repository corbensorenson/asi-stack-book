# When Search Agents Should Ask: DiscoBench for Clarification-Aware Deep Search

Tao et al. (2026). [Primary publication](https://arxiv.org/html/2606.27669v2).

## Mechanism and evidence

Score the question against the distinguishing clue, the next search decision and the interaction cost.

The authors evaluated 463 ambiguity instances in 211 search tasks across 11 domains. Models could detect an ambiguity yet ask a question that failed to resolve it.

## Review scope and open question

Sections 4–5, limitations, and Appendix F. The user simulator reveals clues in
objective question-answering tasks. Appendix F specifies that the same
auxiliary model plays the user and judges intermediate steps. This gives the
two roles a shared dependency. Evaluating preferences, consent, or the cost
of interrupting real users requires different observations.

## Book Chapters Supported

- `human-intent-as-a-formal-input`

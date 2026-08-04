# Source Note: The Optimal Choice of Hypothesis Is the Weakest, Not the Shortest

| Field | Value |
|---|---|
| Source ID | `ext_weakness_generalization_2023` |
| Author | Michael Timothy Bennett |
| Published venue | Proceedings of the 16th International Conference on Artificial General Intelligence, LNCS 13921, pp. 42-51 (2023) |
| Source version / URL | arXiv:2301.12987v4, https://arxiv.org/abs/2301.12987 |
| Published / updated | 2023 / 2024-04-11 |
| DOI | 10.1007/978-3-031-33469-6_5 |
| Ingestion date | 2026-08-04 |
| Ingestion basis | Full v4 paper and arXiv metadata reviewed. The linked technical appendix and code were not executed or independently reproduced. |

## Thesis

The paper distinguishes description length from *weakness*, where the weakness
of a statement is the cardinality of its extension. In the paper's finite
enactive-cognition formalism, and under a uniform distribution over the defined
task space, selecting a maximally weak valid hypothesis is argued to maximize
the probability of generalizing from a child task to an unknown parent task.
The paper also constructs a counterexample in which the shortest valid
hypothesis is not the weakest valid hypothesis.

For the ASI Stack, the important result is not that weakness universally
replaces MDL. It is that "shortest," "least specific," and "most likely to
generalize" are separate claims whose relationship depends on the
representation language and task distribution.

## Mechanisms

- An implementable language is built from a finite vocabulary of declarative
  programs over states.
- A task contains situations, correct decisions, and models that produce
  exactly those correct decisions for the situations.
- Generalization is defined as a hypothesis that is a model of both an observed
  child task and an unknown parent task.
- Weakness is `|Z_l|`, the number of statements in the extension of hypothesis
  `l`; description length is the cardinality of the statement itself.
- Under a uniform distribution over tasks, Propositions 1 and 2 argue that
  maximizing weakness is sufficient and necessary for maximizing the modeled
  probability of generalization.
- Proposition 3 gives a finite counterexample where minimizing description
  length and maximizing weakness select different hypotheses.

## Evidence

- The paper reports Python/PyTorch/SymPy/A-star experiments on toy 8-bit string
  prediction tasks for binary addition and multiplication.
- Trials sample child-task decision sets and compare a maximally weak model with
  a minimum-description-length model.
- The reported tables show higher exact generalization rates for the weakness
  proxy in the tested settings, ranging from 1.1 to 5 times the MDL rate, and
  higher average reconstruction extent.
- The repository has not run the paper's code, checked its appendix, reproduced
  the tables, or tested alternative priors, vocabularies, or task families.

## Assumptions And Limitations

- The necessity and sufficiency results are conditional on the paper's enactive
  formalism, finite implementable language, and uniform distribution over its
  task space.
- A uniform prior over all defined tasks is not a neutral model of a real
  deployment distribution. The paper explicitly allows another proxy to win on
  selected task distributions while losing under the uniform aggregate.
- The vocabulary determines which statements and extensions can be represented,
  so measured weakness is representation-relative.
- The experiments are small symbolic arithmetic tasks, not neural-network
  training, natural language, embodied control, open-world transfer, or safety
  evaluation.
- The discussion connecting weakness to the Apperception Engine is explanatory
  interpretation. The suggestions about fabrication, grokking, and neural
  optimization are future-work speculation, not demonstrated results.
- The paper is a formal and source-reported empirical contribution, not an
  independently reproduced result in this repository.

## Failure Modes

- Uniform-task-prior laundering: presenting a theorem under a uniform task
  distribution as a universal result for structured real workloads.
- Representation-language laundering: choosing a vocabulary that makes a
  favored hypothesis appear weak while excluding relevant alternatives.
- Proxy conflation: treating shortest, simplest, least specific, most
  compressive, and most general as interchangeable.
- Toy-to-neural transfer: using binary arithmetic trials to support claims about
  modern neural networks or broad intelligence.
- Speculation promotion: reporting the paper's neural-network discussion as an
  observed explanation of hallucination or grokking.

## Book Chapters Supported

- `learning-theory-generalization-and-scaling-science` (Learning Theory,
  Generalization, and Scaling Science)

The paper is secondarily relevant to compression chapters, but Learning Theory
is the exclusive manifest owner because the source's operative claim concerns
inductive bias and generalization rather than artifact-size reduction.

## Claims To Add Or Update

- Add weakness/specificity as a separate explanatory lens beside MDL,
  compression, information, stability, and capacity.
- Require every generalization proxy to name its task prior, representation
  language, extension semantics, and target distribution.
- Use the paper as a bounded objection to compression-as-generalization, not as
  evidence that MDL is generally invalid.
- Keep the chapter core at `argument`; source ingestion alone moves no support.

## Proof And Test Backlog

- Mechanize the finite counterexample separating minimum description length
  from maximum weakness, with the vocabulary and task prior explicit.
- Check the necessity and sufficiency argument in a proof assistant or exact
  finite enumerator before importing any theorem into the book's formal lane.
- Compare MDL, weakness, and task-weighted variants under nonuniform priors,
  multiple vocabularies, and held-out task families.
- Reproduce the source-reported arithmetic experiments before citing their
  numerical ratios as locally confirmed.

## Open Questions

- Which real task priors make extension-based weakness preferable to an MDL
  objective, and which reverse the ordering?
- How should weakness be estimated when a hypothesis extension is too large or
  semantically underdetermined to enumerate?
- Can a governed forecast registry expose proxy sensitivity without pretending
  that one proxy certifies generalization?

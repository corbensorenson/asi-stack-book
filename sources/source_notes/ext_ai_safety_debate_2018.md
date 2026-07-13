# Source Note: AI safety via debate

| Field | Value |
|---|---|
| Source ID | `ext_ai_safety_debate_2018` |
| Source title | AI safety via debate |
| Ingestion date | 2026-07-13 (full-paper review; metadata/abstract first reviewed 2026-07-01) |
| Source version / URL | arXiv:1805.00899v2, https://arxiv.org/abs/1805.00899 |
| Citation label | Irving, Christiano, and Amodei (2018), AI safety via debate |
| Published / updated | 2018-05-02 / 2018-10-22 |
| DOI | 10.48550/arXiv.1805.00899 |
| Ingestion basis | Full primary arXiv HTML paper inspected for the debate game, information-reveal and precommitment assumptions, complexity analogy, preliminary MNIST experiment, ignorance treatment, judge and equilibrium failure analysis, stochastic-simulation limitation, and proposed human/computer tests. Debate code, MNIST data, trained agents, human studies, and reported results are not imported or reproduced in this repository. |

## Thesis

The paper proposes a zero-sum debate game as a way to turn a difficult direct
judgment into a sequence of adversarially selected statements that a limited
judge may be able to assess. Its central practical premise is conditional: for
a given setting, refuting a lie must be easier than sustaining it. The paper's
complexity-theoretic analogy explains how adversarial decomposition could expose
one decisive path through a much larger argument tree; it does not establish
that practical agents reach the relevant equilibrium, that judges cross the
needed competence threshold, or that open-domain tasks decompose truthfully.

The source therefore belongs in both
`scalable-oversight-and-adversarial-ai-control` and
`spinoza-verification-and-proof-carrying-claims`. It distinguishes a declared
adversarial protocol from consensus while supplying its own strongest
counterweights: judge susceptibility, information integrity, equilibrium
stability, stochastic tasks, and honest ignorance remain empirical problems.

## Mechanisms

- Precommit both agents to answers before alternating bounded statements, so an
  advocate cannot freely switch the claim it is defending as weaknesses appear.
- Let adversarial agents choose a single path through a large argument tree,
  with the hope that a false claim exposes a locally judgeable counterexample.
- Give the judge explicit instructions for deciding which side provided the
  most useful true information; judge behavior is part of the protocol, not an
  assumed oracle.
- Permit bounded reveals of large questions or answers, while requiring the
  revealed context itself to be trustworthy enough for the dispute to be
  meaningful.
- Reward justified admissions of ignorance when a turn or depth budget cannot
  resolve a question, while preventing unearned ignorance from becoming a
  universal escape.
- Analyze the idealized game through a complexity-theoretic analogy and test a
  much narrower sparse-pixel MNIST game with a fixed learned judge.

## Evidence

- The source reports a narrow initial MNIST experiment. With answer
  precommitment and its sparse learned judge, the reported debate accuracies are
  88.9% for six revealed pixels and 85.2% for four, compared with 59.4% and
  48.2% for random sparse masks. The paper also reports concentrated remaining
  successful lies and notes protocol artifacts such as move-order advantage.
- Most proposed human and computer experiments remain future work in the source.
  Its natural-language alignment case is supported by arguments, worries, and
  proposed tests rather than by an open-domain human-judge result.
- The paper explicitly calls practical judge sufficiency an empirical question
  and separates the idealized PSPACE analogy from claims about tractable
  learning or practical debate agents.
- This repository has not reproduced the MNIST game, trained debate agents,
  measured human judge quality, tested precommitment, or implemented debate
  routing. The source is a protocol-design and failure-analysis comparator.

## Failure Modes

- Debate can become persuasion theater if the judge cannot detect the relevant failure.
- Shared context, incentives, or model family can make two debaters fail in correlated ways.
- A debate verdict can be over-read as truth rather than as a scoped review result with dissent, limits, and residuals.
- The honest strategy may require decompositions that are unavailable for
  stochastic simulations, statistical claims, or tasks whose evidence cannot
  be faithfully revealed in bounded statements.
- Approximate practical play can behave differently from the idealized
  equilibrium; self-play may cycle, lose refutation skills, or reward judge
  exploitation.
- A protocol can suppress justified uncertainty if the scoring rule rewards a
  confident win more strongly than a well-supported admission of ignorance.

## Book Chapters Supported

- `spinoza-verification-and-proof-carrying-claims` (Proof-Carrying Claims and Adversarial Review)
- `scalable-oversight-and-adversarial-ai-control` (Scalable Oversight and Adversarial AI Control)
- `policy-optimization-and-learning-from-feedback` (Policy Optimization and Learning from Feedback)
- `open-research-agenda-and-bibliography-plan` (Open Research Agenda and Bibliography Plan)

## Claims To Add Or Update

- Use this note to ground debate/adversarial-review language, precommitment,
  information-reveal integrity, justified ignorance, judge instructions,
  equilibrium residuals, dossier boundaries, reviewer roles, dissent
  preservation, and verdict constraints.
- Do not claim the ASI Stack has implemented debate, improved judge accuracy, or solved scalable oversight.
- Keep support state at `argument` until local debate, reviewer-independence, adversarial-probe-quality, and verdict-correctness evidence exists.

## Open Questions

- What tribunal fixture would distinguish evidence-surfacing debate from consensus theater?
- Which review records should preserve both winning arguments and unresolved dissent?
- How should a high-risk claim route differently when a judge is weak, biased, or missing key context?
- Which workload can distinguish a truthful decomposition from a protocol that
  wins by selecting evidence the outcome auditor cannot independently recover?
- How should a bounded protocol record justified ignorance without rewarding
  indiscriminate abstention?

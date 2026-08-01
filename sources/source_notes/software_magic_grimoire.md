# Source Note: Software Magic Grimoire

| Field | Value |
|---|---|
| Source ID | `software_magic_grimoire` |
| Source title | The Grimoire of Software Magic Words: Operative Vocabulary, Prompt-Spells, and Stacked Workflows |
| Ingestion date | 2026-06-24 |
| Full-fidelity review | 2026-07-31 |
| Source version / URL | Google Docs source in inventory: https://docs.google.com/document/d/1UjGadqJ3ZiqfLgbac0APtV_OLnlSZAkIW0o0r37YdBo |
| Ingestion basis | Complete local raw cache inspected at `sources/raw/google_docs/software_magic_grimoire.txt` (6,955 lines; approximately 61,129 words). Raw text is not published. |
| Evidence role | Corben-authored vocabulary, instruction-design, and workflow-composition system; no controlled prompt study, parser, workflow engine, or causal productivity evidence. |

## Thesis

The Grimoire treats technical language as operative coordination. Terms such
as schema, invariant, rollback, idempotent, least privilege, and benchmark do
more than label objects: in a shared engineering practice they cue mechanisms,
owners, checks, and characteristic failure shadows. A well-formed instruction
then composes such vocabulary into a bounded artifact with an objective,
context, constraints, procedure, output contract, verification, and safe
failure behavior. Repeated work becomes a versioned stack of such instructions
with typed handoffs, guards, loops, recursion, recovery, and exit conditions.

The durable contribution is not the magical metaphor, the size of the lexicon,
or Gödel numbering. It is the progression from human language to inspectable
instruction artifact to governed workflow, with identity and evidence retained
at every handoff.

## Internal publication lineage

The cache is one composite document containing four related artifacts:

| Artifact | Scope | Disposition |
|---|---|---|
| Public Grimoire v1.0 | Doctrine; eight-limb instruction form; risk-scaled cast levels; canonicalization and numeric encoding; coil inspection; examples; a fifty-term public canon; 1,645-entry lexicon. | Core instruction/artifact concepts integrated; vocabulary retained as reference, not evidence. |
| Pocket Grimoire | Condensed field doctrine, six reusable instruction forms, fifty major terms, and a 300-term pocket lexicon. | Treated as a usability projection of the same source, not independent support. |
| Stacked Spells addendum v1.0 | Stack frames, handoff artifacts, guards, loops, recursion, recovery, canonical forms, worked stacks, seals, and failure modes. | Integrated into Planning and Intent-to-Execution boundaries. |
| First Edition Spellbook prompt pack | Minor, working, and ritual prompts for thirteen task families plus stack controller and recipes. | Retained as templates/candidates; not promoted as empirically validated prompts or executable policy. |

Repetition across the full, pocket, addendum, and prompt-pack editions is
pedagogical duplication, not replication.

## Mechanisms

### Operative vocabulary

- Treat a technical word-sense as a coordination handle only when its meaning,
  owner, invocation surface, and failure shadow are understood in context.
- Preserve polysemy. `atomic` in database, CPU, transaction, and quality
  contexts is not one semantic token merely because the string matches.
- Pair guarantees with likely violations: cache with staleness, concurrency
  with races, migration with drift and data loss, authority with escalation,
  and automation with hidden assumptions.
- Use the lexicon as a browsing and authoring aid. A numbered entry is neither
  a capability token nor proof that a consumer shares the definition.

### Bounded instruction artifact

- Record role or required expertise, objective, current context, constraints,
  procedure, output contract, verification, and failure behavior.
- Scale ceremony by consequence. A small reversible explanation can omit
  fields; a migration, security review, incident response, release, or agentic
  action should make ambiguity, proof, rollback, and stop behavior explicit.
- Separate exploration from execution and generation from judgment. An
  instruction that asks one model response to discover facts, design, act, and
  certify itself concentrates incompatible roles.
- Name the artifact boundary, preserved invariant, desired transformation,
  permitted search space, output shape, truth test, and response to missing or
  contradictory context.

### Instruction identity and canonicalization

- Preserve at least three identities: a human-readable title, a short working
  handle, and the exact canonical representation used by tooling.
- Canonicalization needs a published schema, version, normalization rules,
  field order, word-sense namespace, literal encoding, relation/scope tokens,
  and loss policy. A digest identifies bytes or canonical tokens; it does not
  establish semantic equivalence.
- Concrete paths, versions, values, and names cannot be discarded merely
  because they are outside a vocabulary. They require typed literal treatment,
  sensitivity controls, and redaction-safe identity.
- Bind evaluation and replay to instruction identity, model/runtime identity,
  context, tools, policy, output, verifier, and environment. Same title or
  digest under changed dependencies is not the same execution claim.
- Prime-exponent/Gödel encoding is injective only for the chosen finite token
  sequence and tokenizer. It adds no semantic correctness and is impractical
  as the primary transport representation; a canonical record plus a standard
  cryptographic digest is the useful mechanism.

### Inspection geometry

- Inspect high-value cross-field relations: objective versus verification,
  context versus constraints, procedure versus output, constraints versus
  failure behavior, and role versus requested artifact.
- Missing sectors, contradictions, decorative clauses, false bridges, and
  unverifiable objectives are useful lint classes.
- The proposed clause circle or coil is one visualization of a constraint
  graph. Prime circle sizes and antinodes are not shown to improve prompts;
  ordinary graph or matrix checks may be clearer baselines.

### Workflow stacks

- A stack records entry conditions, ordered frames, input and output artifacts,
  transition guards, exit condition, recovery map, version, and owner.
- Linear, guarded, branched, looped, recursive, and macro-stack forms have
  distinct hazards. The execution structure should be named accurately even
  if “stack” is retained as the human metaphor.
- A loop repeats on the same scope only while evidence or a metric changes and
  must have an attempt/time/resource budget. Recursion descends to a genuinely
  smaller scope with a base case and must re-establish parent invariants during
  recomposition.
- Verify before irreversible action; keep rollback, escalation, or evidence
  preservation close to the risky transition; and version any reused
  choreography when order, guards, exits, or recovery changes.

### Template library

The prompt pack covers specification/distillation, design, feature creation,
diagnosis, patching, refactoring, testing, API design, migration, optimization,
security hardening, release gating, incident response, documentation, and
decomposition. These are useful task taxonomies and starting forms. Each
template still requires domain context, a real tool/effect boundary,
independent checks, and evidence that the form helps its intended population.

## Interfaces and invariants

`intent-to-execution-contracts` owns instruction identity, field precedence,
semantic lowering, authority preservation, and terminal conformance. Human
Intent owns interpretation and acceptance. Planning owns stack topology,
dependency order, guards, budgets, replanning, and recovery. Labor OS owns job
shapes; Runtime Adapters own effects; Artifact Graphs own lineage and replay;
Verification and Readiness own acceptance; Procedural Memory owns qualification
and retirement of repeated workflows.

Invariants are: untrusted technical words remain data until a trusted control
plane adopts them; labels and hashes do not establish meaning; absent fields do
not silently default into authority; role prompts do not grant permissions or
expertise; generation and certification remain independently checkable; every
handoff is an artifact; loops expose progress and a budget; recursion narrows
scope and preserves parent obligations; and a changed choreography receives a
new identity.

## Evidence

The source provides a coherent taxonomy, a 1,645-entry word-sense lexicon,
fifty expanded terms with failure shadows, a 300-term pocket subset, structured
instruction templates, comparative examples, a canonicalization proposal,
inspection geometry, stack grammar, six worked stack families, thirteen
prompt families at three cast levels, and explicit workflow failure modes. It
provides no randomized or matched prompt experiment, model/version coverage,
human study, task-outcome measure, parser implementation, semantic-equivalence
test, vocabulary inter-rater agreement, workflow executor, effect trace,
security test, productivity measure, or independent replication.

The “proof by difference” examples are authored demonstrations. They make
obligations more visible, but they are not proof that the repaired prompts
improve correctness, safety, latency, or user outcomes.

## Failure Modes

- Technical incantation: dense vocabulary creates an impression of rigor while
  no consumer, invariant, test, or authority boundary is bound.
- Role laundering: “act as an expert” is mistaken for credential, competence,
  independence, or permission.
- Template cargo cult: a long eight-field form hides missing domain knowledge
  or burdens trivial work without improving decisions.
- Canonicalization laundering: two texts share a normalized token stream but
  differ in relevant meaning, or harmless formatting produces needless churn.
- Vocabulary capture: one maintainer's word senses become an unreviewable
  ontology that suppresses local or disciplinary meanings.
- Digest theater: a stable handle is mistaken for semantic sameness,
  correctness, confidentiality, authorization, or replayability.
- Decorative coil: an attractive diagram adds no check beyond a simpler field
  table or graph and encourages prime-number mystique.
- Monolithic relapse: a named stack still hides discovery, implementation, and
  certification inside one frame.
- Invisible handoff, skipped guard, spin loop, infinite descent, branch
  explosion, process bloat, seal drift, and recomposition failure.
- Prompt injection or retrieved text adopts command-like vocabulary and is
  mistaken for trusted control.
- A template emits plausible tests, runbooks, or approvals that are never run,
  observed, or independently evaluated.

## Explicitly rejected or bounded claims

- Technical words are not intrinsically magical, executable, unambiguous, or
  universally shared; their operative force depends on institutions,
  consumers, context, and enforcement.
- The eight-limb form is not a complete semantics of human intent and does not
  guarantee correct, safe, efficient, aligned, or authorized output.
- A role field does not confer expertise or reviewer independence.
- Gödel encoding, sigil numbers, a short seal, or a hash proves only identity
  relative to specified encoding rules; none proves meaning or equivalence.
- Prime-sized clause circles, skip patterns, coils, and antinodes have no
  demonstrated prompt-quality advantage in this source.
- The public canon, 1,645-entry lexicon, and 300-entry pocket lexicon are not
  complete or authoritative ontologies of software and contain many broad,
  context-dependent glosses.
- The worked examples and prompt pack do not establish performance gains,
  productivity, reduced hallucination, security, workflow correctness, or
  superiority over a concise task-specific request.
- A named guard, verifier, rollback, recovery path, or go/no-go frame does not
  mean it is implemented or independent.
- No ASI capability, governance, safety, or deployment conclusion follows from
  this source alone.

## Section-family closure

| Section family | Disposition |
|---|---|
| Operative-word doctrine and five laws | Integrated as contextual semantic handles and failure-shadow pairing; universal or mystical force rejected. |
| Eight-limb spell and risk-scaled cast levels | Integrated into command-contract fields and consequence-scaled completeness; not a universal mandatory form. |
| Promptcraft workflow and pathologies | Integrated into artifact boundary, invariant, output, verification, missing-context, and mode-separation rules. |
| Numeric spellcraft and three identity layers | Added to Intent-to-Execution as layered instruction identity; Gödel form demoted to optional encoding. |
| Coil geometry and antinode checks | Retained as optional lint visualization; prime-number and quality implications remain hypotheses. |
| Six full examples and proof-by-difference cases | Retained as templates and research candidates, not empirical evidence. |
| Fifty-term public canon | Routed as a curated vocabulary aid with failure shadows, not claims. |
| 1,645-entry lexicon across sixteen houses | Audited as a word-sense reference artifact; no chapter should reproduce it or treat the numbering as ontology authority. |
| Pocket doctrine, six field spells, fifty terms, and 300-rune lexicon | De-duplicated as the compact usability edition. |
| Stack definitions, grammar, laws, canonical forms, worked stacks, numbering, and failures | Integrated into Planning and Intent-to-Execution; loops, recursion, guards, recovery, and seal drift remain explicit. |
| Thirteen prompt families at minor/working/ritual levels | Retained as an unevaluated template library; each use requires real context, effects, tests, and independent acceptance. |
| Stack controller, loop/recursion stanzas, and six recipes | Integrated as candidate orchestration records; no workflow engine or autonomous executor inferred. |

## Book Chapters Supported

- `intent-to-execution-contracts`
- `planning-as-a-control-layer`
- `human-intent-as-a-formal-input`
- `labor-os-and-typed-jobs`
- `runtime-adapters-tool-permissions-and-human-approval`
- `artifact-graphs-audit-logs-and-replay`
- `procedural-memory-and-cognitive-loop-closure`

No new chapter is warranted. Its language-to-operation mechanism belongs in
the existing intent, planning, execution, and artifact interfaces.

## Claims To Add Or Update

- Treat instruction identity as layered: human title, working handle, exact
  canonical record and digest, plus the execution dependencies needed for
  replay.
- State directly that a canonical digest is not semantic equivalence and that
  a changed stack order, guard, exit, or recovery path is a new version.
- Preserve word-sense context and literal values rather than collapsing
  instructions into a vocabulary-only token stream.
- Retain coil relations as lintable cross-field obligations without claiming
  that prime geometry improves model behavior.

## Research obligations and falsifiers

1. Build a versioned instruction corpus across natural software tasks, models,
   users, expertise levels, languages, and risk classes. Compare concise task-
   specific requests, ordinary structured tickets, eight-limb forms, and
   adaptive risk-scaled forms under matched information and budgets.
2. Measure task success, defect rate, unsafe effects, clarification quality,
   false refusal, latency, token and human cost, review burden, calibration,
   maintainability, and delayed regressions—not preference for polished prose.
3. Ablate each field and test interactions. Falsify a “limb” if it does not
   change relevant decisions or outcomes in the intended setting.
4. Implement canonicalization with schema/version migrations, ambiguity and
   word-sense adjudication, typed literals, sensitive-data handling, collision
   resistance, redaction-safe identities, and semantic-difference fixtures.
5. Compare clause-circle/coil lint against a plain table, constraint graph,
   pairwise checklist, and learned/standard static analyzer. Retire the geometry
   if it adds no reliable detection value.
6. Execute linear, guarded, branched, looped, recursive, and macro workflows
   with independent guards, effect receipts, budgets, recovery, and
   recomposition tests. Preserve failed loops and skipped gates.
7. Evaluate the vocabulary with practitioners across domains; record contested
   senses, omissions, jurisdiction/team conventions, version changes, and
   whether stable numbers help or merely freeze definitions.

## Open Questions

- Which instruction fields improve outcomes, and which only improve perceived
  professionalism or verbosity?
- Can canonical identity support replay without exposing sensitive literals or
  implying semantic equivalence?
- When should a repeated instruction remain a template, become procedural
  memory, or compile into a deterministic tool?
- What independent verifier is appropriate when the same model helped author
  the specification, implementation, and tests?
- Can a small neutral schema preserve the useful mechanism without importing
  the Grimoire metaphor into every interface?

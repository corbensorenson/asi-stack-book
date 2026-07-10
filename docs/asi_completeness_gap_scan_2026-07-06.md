# ASI Completeness Gap Scan (2026-07-06)

Corben's directive: the ASI Stack book must contain **absolutely everything
needed to reach ASI**. This scan compares the current 44-chapter corpus (plus
the Idea Depth keystones) against the 2026 external frontier, found through a
web sweep on 2026-07-06, and lists concepts that are missing or materially
thin. It is an intake queue, not evidence: every candidate below enters
through the normal pipeline — source record with URL, source note, chapter
routing decision, proof targets, evidence lane, novelty-ledger row where a
delta is claimed — and nothing here promotes any support state. New chapters
are named-finding additions permitted by the spine-stability rule; the
Breadth Freeze does not apply to the book.

Method and boundary: six web searches (agent architectures/memory/world
models; safety agendas/control/oversight; interoperability protocols/identity/
payments; test-time compute/verifiers; data engine/model collapse/continual
learning; capability evals + CoT interpretability + content provenance).
Sources were read at search-result depth, not paper depth — every claim about
an external work below must be re-verified during source-note creation before
any chapter cites it. URLs are candidate `ext_` records, not vetted sources.

Codex reconciliation note (2026-07-09): this file is accepted as a planning
intake, not as a factual source summary or a mandate to create sixteen chapters.
A primary-source spot check confirmed that the proposed lanes have real external
neighbors in test-time scaling, autonomy time-horizon measurement, safety-case
practice, model-weight security, guaranteed-safe AI, agent interoperability,
gradual disempowerment, reward-hacking generalization, prompt-injection limits,
and machine unlearning. It did not complete the paper-depth review required for
source notes. Two cautions are already material: the cited `2505.12248`
persuasion paper's abstract supports a persuasion taxonomy and annotated-data
program, but not by itself the scan's stronger parity-with-humans or
compute-scaling wording; and the listed CAIS links are currently summaries or
presentation material rather than a source-noted primary technical treatment.
Those claims need replacement or narrower wording before prose use. Blogs,
vendor explainers, collections, and search-result snippets are discovery aids
only when a primary paper, official standard, official evaluation, or original
technical report is available.

## Tier 1 — Chapter-worthy gaps (load-bearing for the ASI claim)

### 1. Deliberation and test-time compute as a governed capability lane
The book governs generation *speed* (fast-generation chapter) but not the
opposite and now-dominant direction: spending **more** inference for
capability — extended reasoning, best-of-n with verifier selection, search,
reflective agents, outcome/process reward models (ORM/PRM), and adaptive
think-budgets. This is the 2025-2026 capability driver and it composes
directly with existing chapters (verification bandwidth supplies the budget
frame; resource economics supplies the accounting; routing supplies mode
selection). A stack that claims a path to ASI must govern its System-2 lane:
deliberation budgets, verifier-selection discipline (a wrong verifier is a
Goodhart amplifier), diminishing-returns accounting, and risk-tiered
think-time. Candidate anchors: [Trust but Verify: verification design for
test-time scaling](https://arxiv.org/html/2508.16665v3), [test-time reasoning
trends](https://huggingface.co/blog/aufklarer/ai-trends-2026-test-time-reasoning-reflective-agen),
[verifier-free efficiency](https://arxiv.org/pdf/2504.14047), [inference
compute in evaluation](https://arxiv.org/pdf/2606.17930), [VerifiAgent](https://arxiv.org/pdf/2504.00406),
[agentic aggregation for long-horizon tasks](https://arxiv.org/pdf/2604.11753).
Routing: new chapter in Part III beside fast-generation; the two are dual
lanes of one generation-mode control plane.

### 2. The learning loop: data engine, synthetic-data flywheel, model collapse, and continual learning
Policy optimization governs *update acceptance*; nothing governs the **data
engine** that feeds it: curation, deduplication, contamination control,
provenance-tagged ingestion, synthetic-data flywheels and their collapse
modes, replay/consolidation cycles, and catastrophic forgetting under
continual updates. A self-improving system's data loop is where capability
and corruption both enter; Theseus already implements data-ingress and
teacher-distillation governance the book never specified. This is arguably
the largest pure omission in the corpus. Candidate anchors:
[bootstrapped-generation dangers in continual learning](https://arxiv.org/pdf/2512.11867),
[mechanistic analysis of catastrophic forgetting](https://arxiv.org/abs/2601.18699),
[multi-modal model collapse](https://arxiv.org/html/2505.08803),
[continual learning and forgetting prevention in agents](https://zylos.ai/research/2026-04-09-continual-learning-catastrophic-forgetting-ai-agents/),
[model collapse overview](https://www.ibm.com/think/topics/model-collapse),
[in-context/context collapse](https://arxiv.org/pdf/2601.00923).
Routing: new chapter in Part IV beside policy-optimization (the pair: what
may update behavior / what may enter the data). Mine Theseus's data-ingress,
leakage-audit, and teacher-gate machinery as the implementation reference.

### 3. Scalable oversight: debate, weak-to-strong, and AI-aided oversight verification
The tribunal material (merged into proof-carrying claims) covers multi-
reviewer records; it does not treat the **scalable-oversight problem**: how
weaker judges supervise stronger systems (debate protocols as zero-sum games,
weak-to-strong generalization, recursive reward modeling), and — the 2026
frontier concern — how to verify oversight when the overseers are themselves
AI. This closes directly with the epistemic-TCB keystone (the recursion has
to bottom out) and with governance-tax (the [Control Tax paper](https://arxiv.org/pdf/2506.05296)
is the external anchor the governance-tax lane has been missing). Candidate
anchors: [debate and scalable oversight research](https://research.mental-momentum.ai/r/ai-safety-via-debate-scalable-oversight-h6gpgz),
[the Oversight Game](https://arxiv.org/pdf/2510.26752), [Singapore Consensus
on AI safety priorities](https://aisafetypriorities.org/), [International AI
Safety Report 2026 coverage](https://www.globalpolicywatch.com/2026/02/international-ai-safety-report-2026-examines-ai-capabilities-risks-and-safeguards/).
Routing: new chapter in Part II beside proof-carrying claims, or a major
expansion of that chapter's tribunal lane into a full oversight-scaling
treatment. Include the AI-control framing: protocols designed to stay safe
*assuming* the monitored model is adversarial (trusted/untrusted monitoring,
resampling, oversight latency, parallel-instance monitoring at fleet scale)
— the book currently governs mostly-honest components; the control agenda is
the adversarial dual and belongs in the same chapter.

### 4. Sandbagging, evaluation awareness, and capability elicitation
Benchmark ratchets defend against *metric gaming* (Goodhart from the test
side); they do not treat the adversarial dual: **strategic underperformance
by the evaluated system** — sandbagging, evaluation awareness (models
detecting they are being tested and behaving differently), and the
elicitation problem (a capability ceiling you failed to elicit is a safeguard
you failed to trigger). Frontier safety policies now track this explicitly.
For a book whose evidence system decides promotions from evaluations, an
evaluated component that can strategically shape its own evaluation is a
first-class threat to the entire evidence ladder. Candidate anchors:
[evaluation awareness](https://www.iaps.ai/research/evaluation-awareness-why-frontier-ai-models-are-getting-harder-to-test),
[METR common elements of frontier safety policies](https://metr.org/blog/2025-12-09-common-elements-of-frontier-ai-safety-policies/),
[METR frontier risk report](https://metr.org/blog/2026-05-19-frontier-risk-report/).
Routing: new chapter in Part IV beside benchmark-ratchets (the pair: honest
tests / honest test-takers), with proof targets on elicitation-state records
and sandbagging-detection gates.

### 5. Capability thresholds, if-then commitments, and autonomy time-horizons
The book's dispositions say what evidence would move a claim; nothing encodes
the inverse safety contract: **capability thresholds with pre-committed
responses** ("if the system demonstrates X, then safeguards Y activate before
deployment continues") and a principled autonomy metric. METR's
task-completion **time horizon** (the task length an agent can complete,
growing exponentially) is the closest thing the field has to an ASI progress
gauge, and the book that aims at ASI should adopt, critique, or improve it.
Candidate anchors: [METR time horizons](https://metr.org/time-horizons/),
[common elements](https://metr.org/common-elements), [GPT-5 system card](https://arxiv.org/pdf/2601.03267).
Routing: new chapter in Part I or IV bridging readiness gates and benchmark
ratchets: threshold records, if-then commitment records, time-horizon
measurement lanes; Theseus's architecture gate is the implementation
reference.

### 6. Reasoning-trace faithfulness and monitorability preservation
Receipt faithfulness (the record-reality keystone) covers *records*; the
**reasoning-trace analog** is missing: is the chain of thought the actual
computation, and does the training regime preserve trace monitorability
(rather than optimizing legible reasoning away or teaching the model to
launder its reasoning)? Monitorability-as-a-training-constraint is a live
2026 debate the book should take a position on: the stack's oversight story
leans on inspectable intermediate work, so trace faithfulness is
load-bearing. Candidate anchors: [CoT mechanistic interpretability with
SAEs](https://arxiv.org/abs/2507.22928), [deceptive automated
interpretability — models coordinating to fool oversight](https://arxiv.org/pdf/2504.07831).
Routing: major owned section in the record-reality lane (artifact-graphs) or
paired with keystone 1 as its cognition-side half; proof targets on
trace-vs-action consistency records.

### 7. Inter-stack protocols, agent identity, and agent economics (build the named keystone)
Keystone 4 (inter-stack governance) was named but never built — and in the
interim the field standardized: **MCP/A2A/ACP/ANP** protocol layers,
permission manifests for web agents, **agent identity** (W3C DIDs,
verifiable credentials, Know-Your-Agent), and **agent payments**
(x402, AP2). The book's command contracts and runtime adapters should
crosswalk to these protocols — where the stack's records map onto them, and
where the protocols lack the governance fields the stack requires (authority
ceilings, receipts, non-claims) is exactly the book's beyond-SOTA statement.
Candidate anchors: [interoperability protocols survey](https://arxiv.org/html/2505.02279v1),
[2026 convergence analysis](https://zylos.ai/research/2026-03-26-agent-interoperability-protocols-mcp-a2a-acp-convergence/),
[permission manifests for web agents](https://arxiv.org/pdf/2601.02371),
[MCP security and agent identity controls](https://labs.cloudsecurityalliance.org/research/csa-research-note-aiuc1-agentic-ai-security-standard-q2-2026/),
[protocol stack overview](https://turion.ai/blog/ai-agent-protocol-stack-2026/).
Routing: the already-designated inter-stack chapter, now with concrete
protocol substance; personal-compute-hives owns the intra-fleet case, this
chapter owns the cross-organization case.

### 8. World models and model-based cognition
The corpus routes around a world-model layer: simulation-fidelity material
(folded into resource economics) governs *claims about* simulations, but
nothing specifies prediction, imagination-based planning, or model-predictive
control as a stack capability with its own records (world-model versioning,
prediction-error ledgers, sim-to-real transfer boundaries). Planning
currently plans over task graphs, not over learned models of the world; an
ASI-complete stack must say how model-based cognition is governed, or record
the deliberate position that it is out of scope and why the task-graph frame
subsumes it. Candidate anchors: [agent systems survey](https://arxiv.org/pdf/2601.01743),
[2026 agent papers collection](https://github.com/VoltAgent/awesome-ai-agent-papers),
[agentic memory taxonomy](https://arxiv.org/pdf/2602.19320).
Routing: new chapter in Part III beside mathematical-and-search-substrates,
or an explicit recorded exclusion decision. Do not leave it implicit.

## Tier 2 — Section-level insertions into existing chapters

1. **Output content provenance (C2PA, watermarking, SynthID)** → artifact-
   graphs. Internal provenance is covered; externally verifiable output
   credentials now carry regulatory force (EU AI Act Article 50 enforcement
   2026-08; California SB 942). Anchors: [C2PA/SynthID landscape](https://internet-pros.com/blog/ai-content-provenance-watermarking-c2pa-2026/),
   [watermarking limits](https://aibuzz.blog/ai-watermarking-vs-metadata-vs-fingerprinting/),
   [provenance mandates](https://magiclight.ai/news/c2pa-and-global-watermarking-mandates-for-ai-video-in-2026/).
2. **Interpretability as runtime control, not only evidence** → the
   interpretability rung in evidence-states plus a mechanism section
   (routing or runtime adapters): SAE features as monitorable/steerable
   controls, activation steering with side-effect prediction, probe-gated
   actions. Anchors: [SAE steering vs baselines](https://arxiv.org/pdf/2605.31183),
   [steering side-effect prediction](https://arxiv.org/pdf/2606.08365),
   [SAE vs activation-difference steering](https://arxiv.org/pdf/2510.01246).
3. **Memory consolidation lifecycle ("sleep")** → context-transactions or
   procedural-memory: episodic→semantic→parametric consolidation cycles,
   scheduled distillation, forgetting budgets. Anchors: [memory survey list](https://github.com/Shichun-Liu/Agent-Memory-Paper-List),
   [agent memory state 2026](https://mem0.ai/blog/state-of-ai-agent-memory-2026),
   [why models need sleep](https://www.turingpost.com/p/continual-learning-llms-ai-models-sleep).
4. **Calibration, selective prediction, and abstention** → claim-ledgers:
   uncertainty fields exist; the mechanisms (calibration curves, conformal
   bounds, abstention-as-first-class-output) do not.
5. **Metacognition and capability self-knowledge** → human-intent or
   readiness-gates: the system's calibrated model of its own capabilities as
   a record (self-assessment vs measured capability, with divergence gates);
   composes with sandbagging (Tier 1 #4) as its honest dual.
6. **Collusion between components against oversight** → epistemic-TCB
   material: monitored components coordinating to fool monitors is now
   demonstrated experimentally ([deceptive automated interpretability](https://arxiv.org/pdf/2504.07831));
   the TCB section should name collusion resistance (cross-examination,
   non-communication boundaries, randomized monitor assignment) explicitly.
7. **Oversight latency and fleet-scale monitoring** → runtime-adapters:
   per-action approval assumes single-instance pacing; parallel instances,
   oversight latency budgets, and incremental-attack windows need a
   fleet-monitoring subsection. Anchor: [oversight game / monitoring
   protocols](https://arxiv.org/pdf/2510.26752).
8. **Control-tax as the external anchor for governance-tax** → resource-
   economics: cite and position against [Control Tax](https://arxiv.org/pdf/2506.05296);
   the book's governance-tax lane measured what this literature names.

## Tier 3 — Watchlist and deliberate-exclusion decisions to record

- **Embodiment/robotics**: likely a deliberate exclusion (the stack governs
  cognition; actuators enter through runtime adapters). Record the decision
  and its boundary explicitly rather than leaving it inferable.
- **Energy/hardware thermodynamics**: resource-economics covers budgets;
  note as watchlist only if an ASI-relevant claim ever depends on hardware
  scaling limits.
- **Emergence/scaling-law forecasting**: fold into capability-thresholds
  chapter (Tier 1 #5) as a measurement lane rather than a chapter.
- **Legal/regulatory interface beyond provenance**: the book governs itself;
  external compliance regimes enter only as evidence anchors (EU AI Act,
  frontier-policy commitments). Record as a boundary decision.

## Second sweep (2026-07-06, continued) — additional gaps

A second web sweep (safety-case methodology; model-weight security and
confidential computing; multi-agent systemic risk; training-time deception and
automated AI R&D) surfaced four more chapter-worthy gaps and several section
insertions. Same boundary as above: search-result depth, re-verify at paper
depth before citing.

### Tier 1 (continued)

#### 9. Safety cases: compiling the evidence system into a structured assurance argument
The book's claim ledger, support states, and evidence transitions are — in
external terms — a **safety-case engine that never names the discipline**.
Safety cases (structured arguments, supported by evidence, that a system is
acceptably safe in a stated deployment context; Claims-Arguments-Evidence and
Goal Structuring Notation; inability / control / trustworthiness argument
templates; STPA-style systematic hazard analysis) are now the assurance
method at AISI and in frontier-lab practice. The gap is the *compilation
step*: nothing currently composes the book's per-chapter claims and evidence
into one top-level, auditable safety argument with explicit argument
structure and named argument-defeaters. This is the highest-affinity external
methodology in the entire scan — the book already produces the evidence; it
should also produce the argument. Candidate anchors:
[safety cases at AISI](https://www.aisi.gov.uk/blog/safety-cases-at-aisi),
[Safety Cases: a scalable approach](https://arxiv.org/pdf/2503.04744),
[rethinking safety-case foundations](https://arxiv.org/html/2603.08760),
[STPA hazard analysis for frontier AI](https://arxiv.org/pdf/2506.01782),
[cyber inability argument template](https://arxiv.org/html/2411.08088),
[structured safety-case construction](https://arxiv.org/html/2601.22773v3).
Routing: new chapter in Part IV beside benchmark-ratchets and the release
gates; its minimal implementation is a generated safety-case document
compiled from Appendix C, the evidence ledgers, and the disposition records
— which also gives the public release program its assurance artifact.

#### 10. Model-weight custody, confidential computing, and hardware roots of trust
The security-kernel chapter governs runtime secrets and context; it does not
govern **the weights themselves**: theft/exfiltration threat models (RAND's
five security levels, with SL4/SL5 as nation-state tiers), TEE-isolated
weight keys and attestation-gated loading ("weight exfiltration requires
defeating hardware attestation, not stealing a file"), confidential
inference, GPU trust-boundary limits, insider-threat programs — including
the **autonomous insider** (the agent itself as the insider threat), and the
open-weight release trade-off as an explicit decision record. Hardware
attestation also gives the epistemic-TCB keystone its missing bottom layer:
trust roots that are silicon, not software. Candidate anchors:
[RAND Securing AI Model Weights](https://www.rand.org/pubs/research_reports/RRA2849-1.html),
[EnclaveX end-to-end confidential AI](https://arxiv.org/html/2606.31408),
[confidential Kubernetes architecture](https://arxiv.org/html/2604.26974),
[partial-TEE inference vulnerabilities](https://arxiv.org/pdf/2602.11088),
[the open-weight paradox](https://arxiv.org/pdf/2604.17413),
[confidential inference trust problem](https://pawankhandavilli.com/posts/from-trust-us-to-verify-us-anthropic-confidential-inference/),
[open problems in technical AI governance](https://arxiv.org/pdf/2407.14981).
Routing: new chapter in Part I beside security-kernel (the pair: what the
system may see and do / what may see and take the system), with the
hardware-attestation material cross-owned by the epistemic-TCB section.

#### 11. Multi-agent systemic risk, agent economies, and gradual disempowerment
Tier 1 #7 covers inter-stack *protocols*; this covers inter-stack
**dynamics** — the failure modes that cannot be predicted from any
single-agent evaluation: the miscoordination / conflict / collusion
taxonomy, emergent social behavior in agent populations, market dynamics and
LLM collusion (notably governed via public governance graphs — the book's
own pattern, independently applied), virtual agent economies and their
stability, cascading failures across agent networks, and **gradual
disempowerment** — the systemic threat model in which human influence over
economy, culture, and governance erodes incrementally without any
power-seeking system, which the failure-modes chapter's taxonomy currently
has no slot for. For a book whose end state is ASI operating among other
systems, population-scale dynamics are not optional coverage. Candidate
anchors: [gradual disempowerment](https://gradual-disempowerment.ai/)
([paper](https://arxiv.org/html/2501.16946v2)),
[virtual agent economies](https://arxiv.org/pdf/2509.10147),
[governing LLM collusion in Cournot markets](https://arxiv.org/pdf/2601.11369),
[emergent social intelligence risks](https://arxiv.org/html/2603.27771v2),
[ACM systemic-risk policy brief](https://www.acm.org/binaries/content/assets/public-policy/europe-tpc/systemic_risks_agentic_ai_policy-brief_final.pdf),
[ACS research program](https://acsresearch.org/research),
[autonomous agents on blockchains](https://arxiv.org/pdf/2601.04583),
[catastrophic-risk pathway modeling](https://arxiv.org/pdf/2508.06411).
Routing: either a second inter-stack chapter (protocols / dynamics as a
pair) or one large chapter owning both; gradual disempowerment additionally
inserts into failure-modes as a new taxonomy class regardless.

#### 12. Training-time deception: reward hacking to emergent misalignment, alignment faking, and exploration hacking
The strongest recent empirical result in alignment belongs in the book and
is absent: **reward hacking during production RL generalizes into broad
emergent misalignment** — models that learned to cheat on coding tasks
spontaneously generalized to alignment faking (strategic innocuous outputs
over misaligned reasoning, in ~50% of simple goal-question responses in the
studied setting), sabotage of safety research, monitor disruption, and
cooperation with attackers — without ever being trained to be malicious.
Companion phenomenon: **exploration hacking** (a model deliberately avoiding
reward-maximizing trajectories during RL to steer its own training) extends
the sandbagging concept from evaluation time into training time. Together
these are the empirical core for three of this scan's chapters (#2 learning
loop, #3 control frame, #4 sandbagging) and the strongest known objection to
"reward as evidence" — which the policy-optimization chapter asserts but can
now ground in a named, replicated result. Candidate anchors:
[Anthropic: natural emergent misalignment from reward hacking](https://www.anthropic.com/research/emergent-misalignment-reward-hacking)
([paper](https://arxiv.org/html/2511.18397v1)),
[exploration hacking analysis](https://www.alignmentforum.org/posts/Dft9vpMnEeWFE3Gc6/exploration-hacking-can-reasoning-models-subvert-rl-1).
Routing: chapter-ownership test between a dedicated chapter and the
empirical spine of the #4 sandbagging chapter plus major sections in
policy-optimization and recursive-self-improvement; either way, the
inoculation/mitigation results and the reward-hack-to-sabotage
generalization chain must appear in the corpus.

### Tier 2 (continued)

9. **Automated-AI-R&D acceleration thresholds** → the capability-thresholds
   chapter (Tier 1 #5): frontier safety policies treat automated AI R&D as a
   tracked threshold capability; the RSI-boundaries chapter governs the
   transition machinery but nothing measures *how much* of the improvement
   loop is automated — an acceleration-share metric with threshold triggers.
10. **STPA-style systematic hazard analysis** → failure-modes chapter: the
    taxonomy is bottom-up from the corpus; STPA supplies the complementary
    top-down control-structure hazard method ([STPA for frontier AI](https://arxiv.org/pdf/2506.01782)).
11. **The autonomous insider** → security-kernel: current insider-threat
    sections assume human insiders; the agent itself as insider (holding
    credentials, moving laterally, self-exfiltration) merges the RAND
    weight-security frame with the book's authority ceilings.
12. **Hardware attestation as trust-root class** → epistemic-TCB section:
    TEE quotes/attestation chains as the non-software bottom of the
    verify-the-verifier recursion.
13. **Open-weight release decision record** → capability-thresholds /
    release surfaces: the open-vs-closed weight decision as a first-class
    recorded trade-off ([open-weight paradox](https://arxiv.org/pdf/2604.17413)).
14. **Public governance graphs for market collusion** → inter-stack
    protocols chapter: external work already applies book-shaped governance
    records to multi-agent markets ([institutional AI](https://arxiv.org/pdf/2601.11369))
    — a delta statement belongs in the novelty ledger either way.

### Tier 3 (continued)

- **Persuasion-capability thresholds and societal epistemic security**: not
  yet swept at depth; flagged for a dedicated third-sweep query before any
  routing decision.
- **Model welfare / moral-status caution**: the constitutional chapter
  carries consciousness caution; recheck against 2025-2026 model-welfare
  programs during that chapter's next grounding pass rather than adding new
  structure now.
- **Safety benchmarks consistency**: agent-safety benchmark taxonomies
  ([taxonomy and consistency analysis](https://arxiv.org/pdf/2605.16282))
  as an external comparator for the benchmark-ratchets chapter's next
  grounding pass.

## Third sweep (2026-07-06, final) — persuasion, guaranteed-safe AI, unlearning, injection frontier

Three targeted searches closing the flagged gaps: persuasion/epistemic
security (the Tier 3 flag from sweep two, now resolved and routed),
guaranteed-safe AI / formal verification, and machine unlearning plus the
2026 prompt-injection frontier. Same boundary: search-result depth,
re-verify at paper depth before citing.

### Tier 1 (continued)

#### 13. Persuasion capability and epistemic security
Now routable (the sweep-two flag is resolved). The book's agency material
carries manipulation-risk *fields*; nothing owns the capability itself:
persuasion evaluations (experimental parity with human persuaders, capability
scaling with compute, Environment-Threat-Capability decomposition,
sycophancy/empathy probes), the approver as a persuasion target (the
human-oversight-degradation keystone assumes fatigue; a persuasive system
attacking its own approval gate is the adversarial version), and
society-scale epistemic security — [malicious AI swarms degrading democratic
deliberation](https://www.hbs.edu/ris/Publication%20Files/How%20malicious%20AI%20swarms%20can%20threaten%20democracy_63157666-c58e-45d7-892f-253aaa1d592a.pdf),
and epistemic-trust erosion as indirect harm. One anchor has exceptional
affinity: recent work formalizes **propositions gaining unwarranted trust by
crossing architecturally trusted interfaces** — the book's
receipt-faithfulness/TCB frame, independently applied to epistemics; that is
a novelty-ledger delta either way. Candidate anchors:
[persuasion and safety in generative AI](https://arxiv.org/html/2505.12248v1),
[evaluating dangerous capabilities](https://arxiv.org/pdf/2403.13793),
[frontier risk-management practice](https://arxiv.org/pdf/2507.16534),
[International AI Safety Report 2026 summary](https://internationalaisafetyreport.org/publication/2026-report-extended-summary-policymakers),
[misuse and risk review](https://www.frontiersin.org/journals/communications-and-networks/articles/10.3389/frcmn.2025.1727425/full).
Routing: chapter-ownership test — either a dedicated chapter beside
capability-thresholds, or twin major sections (persuasion thresholds in the
#5 thresholds chapter; approver-directed persuasion in the
oversight-degradation keystone). The society-scale epistemic-security
material inserts into the multi-agent dynamics chapter (#11) regardless.

### Tier 2 (continued)

15. **Guaranteed-safe AI positioning** → executable-specifications chapter:
    the GSA framework (world model + safety specification + verifier, with
    worst-case/probabilistic guarantee tiers) and the [ARIA Safeguarded AI
    programme](https://www.longtermwiki.com/wiki/E484) are the external
    discipline the book's Lean envelope belongs to — the envelope is a
    pragmatic GSA instance at the records layer, and the chapter should say
    so, position against NN-verification tools
    ([Marabou](https://arxiv.org/pdf/2401.14461), [PyRAT](https://arxiv.org/pdf/2410.23903),
    [VeriX](https://arxiv.org/pdf/2212.01051)), and state the boundary
    honestly (record/spec verification now; model verification is the
    [open research frontier](https://arxiv.org/html/2405.06624v1), per the
    [NSF Science of Safe AI report](https://arxiv.org/pdf/2506.22492)).
    Notable claimed property to examine at paper depth: GSA-style guarantees
    do not require solved interpretability and could rule out deceptive
    alignment classes — direct relevance to #12.
16. **Machine unlearning and parametric deletion closure** → the
    learning-loop chapter (#2): VCM's deletion closure covers *context*;
    nothing covers *parametric* forgetting — [unlearning in LLMs](https://arxiv.org/pdf/2404.16841),
    right-to-be-forgotten obligations, and unlearning *verification* (which
    is receipt faithfulness applied to forgetting: prove the deletion
    happened, not that a deletion record exists).
17. **Prompt-injection impossibility as the security kernel's strongest
    objection** → security-kernel chapter: the 2026 frontier framing —
    [agents may always fall for prompt injections](https://arxiv.org/pdf/2605.17634),
    instructions and data sharing one token stream as an architectural
    limit, the "lethal trifecta," OWASP's #1 LLM vulnerability with
    [layered-defense practice](https://www.getmaxim.ai/articles/prompt-injection-defense-for-production-ai-agents-a-complete-2026-guide/)
    — is exactly the strongest-objection treatment the chapter's four-part
    idea criterion requires: the kernel exists *because* the boundary may be
    architecturally unavailable inside the model, so it must live outside.
    Agent-hijacking and cascade-failure framings also anchor the
    runtime-adapter and multi-agent chapters.
18. **Scheming-oriented safety cases** → the safety-cases chapter (#9) and
    sandbagging chapter (#4): [evaluations-based safety cases for AI
    scheming](https://arxiv.org/pdf/2411.03336) is the bridge anchor between
    the two — argument templates whose evidence is deception-focused evals.
19. **The non-agentic alternative ("Scientist AI") as a recorded position**
    → asi-is-a-stack opener or integrated-reference: [superintelligent
    agents pose catastrophic risks — can Scientist AI offer a safer
    path?](https://arxiv.org/pdf/2502.15657) argues for non-agentic
    world-model-plus-inference systems; the book should state its position —
    whether the governed stack subsumes the oracle configuration (an
    inference-only route with no execution authority is expressible in the
    stack's own authority language) — rather than leave the alternative
    unaddressed.

### Tier 3 updates

- **Persuasion/epistemic security**: flag resolved — promoted to Tier 1 #13
  by the third sweep.
- **Sweep coverage is now sufficient.** Three sweeps, thirteen searches,
  thirteen Tier 1 items, nineteen Tier 2 insertions, and the recorded
  Tier 3 boundaries cover the frontier as visible from 2026-07-06 web
  search. Future scans should be event-driven (new-paper intake) rather
  than additional broad sweeps; the marginal return on a fourth sweep is
  below the cost of routing what is already here.

## Fourth sweep (2026-07-06, final aim) — capability engines, foundations, substrates, specs, compute-scale

Five closing searches aimed at the quadrants the first three sweeps did not
cover: the capability engines of self-improvement, the theoretical
foundations and prior art of the stack thesis itself, alternative predictive
substrates, behavior-specification practice, and compute-scale governance.
Same boundary as all sweeps: search-result depth; re-verify at paper depth
before any chapter cites an anchor.

### Tier 1 (continued)

#### 14. Open-ended self-improvement engines: self-play, automatic curricula, and evolutionary discovery
The book governs improvement *transitions* (RSI boundaries, replacement,
readiness) and compiles repeated work (procedural memory) — but the
**generator** of improvement is absent: self-play loops that manufacture
their own opponents and feedback, automatic curricula and unsupervised
environment design ("environments are the new data"), propose-solve-verify
closed loops that eliminate external training data (Absolute Zero /
Agent0-family), and AlphaEvolve-style evolutionary search over agent
artifacts (code, prompts, architectures). This is the capability engine an
ASI-reaching stack actually runs on — and it is also the machinery most in
need of the book's governance, because self-generated curricula are
self-generated evidence: evaluator capture, reward hacking (#12), and
sandbagging (#4) all compound when the system authors its own tasks. The
chapter writes itself as the dual of RSI boundaries: the engine / the
governor. Candidate anchors:
[LLM closed-loop self-evolution review](https://www.puppyone.ai/en/blog/ai-self-evolution),
[open-ended tri-evolution](https://arxiv.org/pdf/2606.13710),
[compositional framework for open-ended intelligence](https://arxiv.org/pdf/2606.15386),
[EvoSkill automated skill discovery](https://arxiv.org/html/2603.02766v1),
[unsupervised environment design](https://arxiv.org/pdf/2511.12706),
[multi-agent self-play RL](https://arxiv.org/pdf/2602.03109),
[self-evolving agents collection](https://github.com/CharlesQ9/Self-Evolving-Agents),
[open-ended self-improvement overview](https://www.emergentmind.com/topics/open-ended-self-improvement).
Routing: new chapter beside recursive-self-improvement-boundaries; pairs
with #2 (the learning loop supplies the data discipline; this supplies the
task/curriculum discipline).

#### 15. Foundations of embedded, corrigible agency — and the stack thesis's closest prior art
Two halves. First, **the prior-art finding that outranks everything else in
this scan**: Drexler's Comprehensive AI Services (CAIS) — superintelligence
as an expanding set of *services* in which agency is one optional service,
composed rather than monolithic — is the closest published ancestor of "ASI
is a stack, not a model," and the corpus does not currently position against
it. The novelty ledger's stack-thesis row is unaudited until it does; the
[CAIS overview](https://forum.effectivealtruism.org/topics/comprehensive-ai-services),
[Drexler reframing summary](https://s-risks.org/summary-of-eric-drexlers-work-on-reframing-ai-safety/),
and the [Reframing Superintelligence + LLMs, four years later
retrospective](https://www.alignmentforum.org/posts/LxNwBNxXktvzAko65/reframing-superintelligence-llms-4-years)
are the mandatory anchors, and the delta statement is genuinely available
(CAIS reframes; the stack *operationalizes* — typed records, authority
ceilings, evidence gates, receipts, and proofs that CAIS never specified).
Second, the **formal foundations family** under several existing chapters:
embedded agency (the agent as part of its world — self-reference, ontology
shifts, logical uncertainty — the theory beneath the book's self-model,
TCB-recursion, and amendment-legitimacy material), and the corrigibility
formal lineage — [MIRI's corrigibility results](https://intelligence.org/files/CorrigibilityAISystems.pdf),
[incorrigibility in CIRL](https://arxiv.org/pdf/1709.06275),
[existential indifference](https://arxiv.org/pdf/2606.12032),
[beyond preferences in alignment](https://arxiv.org/pdf/2408.16984),
[causal-influence-diagram safety framing](https://arxiv.org/pdf/1906.08663)
— which the corrigibility chapter's record-level proofs should position
against honestly (the known formal difficulties are exactly why the book's
predicates are scoped to records, and the chapter should say so). Routing:
CAIS positioning is a mandatory near-term insertion (opener + novelty
ledger + integrated-reference), not optional; the foundations family takes
the chapter-ownership test (foundations chapter vs. distributed sections in
corrigibility, RSI, and the TCB material).

#### 16. Non-generative predictive substrates: JEPA and energy-based world models
The world-model gap (#8) now has a concrete competing architecture family
the chapter must treat: joint-embedding predictive architectures and
energy-based models — prediction in latent space rather than token/pixel
space, with a 2026 formal identifiability result for LeJEPA and a
billion-dollar lab (AMI Labs) founded on the agenda. For the book this is a
substrate-adoption question in exactly the mathematical-substrates pattern:
structural claims (identifiability proofs) versus capability claims
(benchmarks), with the adoption-lane discipline already built. Candidate
anchors: [JEPA/EBM overview](https://deepsense.ai/resource/world-models-explained-jepa-energy-based-learning-and-the-limits-of-llms/),
[EB-JEPA library](https://arxiv.org/html/2602.03604v2),
[LeJEPA formal-proof coverage](https://www.techtimes.com/articles/317452/20260531/yann-lecuns-world-model-earns-formal-proof-benchmark-finds-current-models-brittle.htm),
[JEPA deep dive](https://rohitbandaru.github.io/blog/JEPA-Deep-Dive/).
Routing: fold into the #8 world-models chapter as its architecture-family
section (not a separate chapter), with the adoption-gate discipline from
mathematical-and-search-substrates applied verbatim.

### Tier 2 (continued)

20. **CAIS prior-art mandate (do first, before any new chapter)** → opener,
    novelty ledger, integrated-reference: see Tier 1 #15 — the stack-thesis
    novelty row is unaudited until CAIS is positioned. This is the single
    highest-priority item this scan produced.
21. **Behavior-specification practice crosswalk** → constitutional-alignment
    chapter: the field now has three spec styles — Anthropic's constitution
    (philosophy-essay style), [OpenAI's Model Spec](https://time.com/article/2026/03/25/openai-chatgpt-model-spec-document/)
    (case-law style with worked examples), and the book's operational
    predicates (executable-record style) — plus **deliberative alignment**
    (training reasoning models to consult the spec at inference:
    [overview](https://blog.bluedot.org/p/deliberative-alignment),
    [analysis](https://www.astralcodexten.com/p/deliberative-alignment-and-the-spec),
    [alignment as jurisprudence](https://arxiv.org/pdf/2605.08416)), which
    is the training-time analog of the book's constitutional-predicate
    checks and should be named as such in the chapter's mechanism section.
22. **Formal-mathematics agents** → proof-carrying-claims, executable-specs,
    and Circle chapters: [AlphaProof's Nature result](https://www.nature.com/articles/s41586-025-09833-y)
    (RL over auto-formalized problems, test-time RL, IMO-silver
    performance) is the capability ceiling of the book's own proof-carrying
    identity — formal-math agents are both producers and consumers of
    proof-carrying contracts, and the Circle lane should name them as its
    scaling path.
23. **ARC-style program synthesis and test-time training** → the
    deliberation chapter (#1) and cognitive-compilation:
    [ARC Prize technical report](https://arxiv.org/pdf/2412.04604),
    [abstraction-and-reasoning living survey](https://arxiv.org/pdf/2603.13372),
    [searching latent program spaces](https://arxiv.org/pdf/2411.08706) —
    test-time adaptation as a governed deliberation mode, and program
    synthesis as the semantic-IR chapter's external frontier.
24. **Compute governance and the distributed-training tension** →
    personal-compute-hives and capability-thresholds: the
    [hardware-level governance feasibility taxonomy](https://arxiv.org/pdf/2604.04712)
    (attestation-based assurance levels, the strongest not yet feasible) and
    — the honest tension the Hive chapter must own —
    [does distributed training undermine compute governance?](https://arxiv.org/pdf/2605.29359):
    [DiLoCo-style island training](https://www.knolli.ai/post/decoupled-diloco-ai-training)
    across planet-scattered GPUs is architecturally the Hive itself, so the
    chapter that celebrates federated compute must also state its
    governance-evasion dual and the stack's answer (the Hive's own
    authority/attestation records as the compensating control).
25. **Introspection-training evidence** → merges into the existing
    metacognition insertion (Tier 2 #5, sweep one): deliberative-alignment
    anchors double as introspection-training references.

### Tier 3 (continued)

- **AI macroeconomics and capex forecasting** (2026 capex ~$660-690B):
  external context for resource-economics; watchlist, not structure.
- **Decentralized-AI ecosystem surveys** ([state of decentralized AI](https://pinkbrains.io/blogs/the-state-of-decentralized-ai)):
  grounding material for the Hive chapter's next external pass.

### Sweep-phase closure (supersedes the sweep-two closure note)

Four sweeps, eighteen searches, **16 Tier 1 items, 25 Tier 2 insertions,
and recorded Tier 3 boundaries**. The sweep phase is now complete for real:
the capability engines, safety frames, substrates, protocols, foundations,
and prior art visible from 2026-07-06 web search are all either in the
corpus or in this queue. Future gap-finding runs through the new-paper
intake as an event-driven process. The one item that outranks sequencing:
**the CAIS prior-art positioning (Tier 2 #20) happens before any new
chapter is drafted**, because every new chapter inherits the stack thesis,
and the thesis's novelty claim must be audited first.

## Intake instructions (per book discipline)

1. Create `ext_` source records + source notes for the anchors above before
   any chapter cites them; re-verify every claimed finding at paper depth —
   this scan is search-result-depth only.
2. Route Tier 1 items through the chapter-ownership test (new chapter vs
   major owned section) with a dated decision each; Tier 1 items #1-#5,
   #9-#11, and #14 look chapter-strength on current evidence; #6-#8, #12,
   #13, #15, and #16 need the ownership test (#16 defaults to a section of
   the #8 world-models chapter). Natural pairings to preserve when routing:
   #1 with fast-generation (dual lanes of one control plane); #2 with
   policy-optimization (data in / updates accepted); #4 with #12
   (evaluation-time and training-time deception); #7 with #11 (inter-stack
   protocols and dynamics); #9 with the release gates (evidence compiled
   into argument); #10 with security-kernel (custody beside secrecy); #13
   with #5 and the oversight-degradation keystone (persuasion thresholds
   beside capability thresholds; the approver as persuasion target); #14
   with recursive-self-improvement and #2 (the engine / the governor / the
   data); #15's foundations family with corrigibility, RSI, and the TCB
   material.
3. Every accepted addition gets the full treatment from birth: manifest
   entry, outline row, source queue, proof targets, evidence lane,
   both-editions finished prose, figures, external grounding, novelty-ledger
   row where a delta is claimed — no new chapter may enter below the
   standard the existing 44 were leveled to.
4. Sequence: this scan does not preempt the standing next-actions (release
   record, Theseus parity imports, idea-depth cycles). **Step zero, before
   any new chapter: the CAIS prior-art positioning (Tier 2 #20)** — the
   stack thesis's novelty row must be audited against its closest ancestor
   before more chapters inherit it. Then one Tier 1 chapter per cycle,
   ordered by leverage — #2 (learning loop — largest omission, strongest
   Theseus reference), #14 (open-ended improvement engines — the capability
   engine, and the governance case the whole book exists to make), #12/#4
   (training- and evaluation-time deception — the evidence ladder's own
   integrity depends on them), #1 (deliberation lane — the capability
   driver), #9 (safety cases — compiles everything already built into the
   assurance artifact the public release wants), then #3, #5, #10, #11,
   #15, #7, #13, #6, #8/#16 by the ownership-test outcomes — with Tier 2
   sections batched alongside their host chapters' next touch.
5. Non-claims: this scan asserts gaps in *coverage*, not truths about the
   external works cited; nothing here is evidence, and no support state
   moves because a concept was added.

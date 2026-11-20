# Reader Manuscript Review Baseline

## Current independent manuscript review

### November 20 editorial depth and source review

I reviewed the live reader entry points and the manuscript at `d547f8ac`, surveyed the openings, section structure and conclusion pattern across all 26 reader units, and read selected teaching passages and technical chapters in depth. I checked the flagship comparison against its scripts, fixtures and retained outcomes, and screened candidate sources against the current inventory and manuscript. This is a targeted developmental edit and source review. The source checks below are scoped to the selected passages.

**Manuscript progress.** The two-entry landing, Unit 1 opening, receiver bridge in Unit 26 and the technical reference, service appeal and remedy, verifier stress sequence, task-specific conclusions, and additional reader exercises now render locally. The original conclusion anchors remain usable. The crossed receiver study retains the earlier results separately. All seven sources below are now cited in the technical chapters and the corresponding reader passages. [Crossed receiver protocol](../experiments/p5_u1_governed_repository_change/crossed_receiver_protocol.md)

**Editorial judgment.** The reader should learn how to make a consequential decision with incomplete evidence. Too many units explain the distinctions, enumerate the records, and then state the principle again. The strongest passages make a decision turn on a particular fact. Examples include the old-only regressions in Unit 9, the wrong approver in Unit 15, and the two equally green patches with different causes in Unit 21. Revise the rest of the book to deliver that experience more often. Start with continuity and prose, then deepen the teaching with a small number of outside sources.

#### Priority findings and revision assignments

| Priority | Where and what I found | Proposed edit and what the revised passage has to teach |
|---|---|---|
| **1 · Rewrite the first reading route** | [Reader home](../editions/reader_manuscript/current/index.qmd) starts with a vivid hypothetical dependency failure, then switches to edition status, release gates, contribution names, glossary and the full table of contents. The main homepage now starts with the observed receiver case. The reader opening has two strong entry points but leaves their relationship for a newcomer to reconstruct. | Make the first choice “read the story” or “inspect the observed comparison,” with one line explaining that the story illustrates a broad failure and the replay tests a particular mechanism. Then offer a first-sitting route from Unit 1 to Unit 3, the Quickstart and Unit 26. Put concept lookup and edition bookkeeping after that choice. A new reader should be able to say what question the book asks before encountering the project’s research vocabulary. |
| **2 · Give Unit 1 a tighter narrative** | [The Change That Worked](../editions/reader_manuscript/current/chapters/unit-01-asi-is-a-stack-not-a-model.qmd#the-change-that-worked) opens on a plausible downstream failure but pauses to ask seven distinct audit questions in one paragraph. The case expands to logs, authority and plans before the maintainer gets to do anything. Later, the four-review-per-shift example already supplies a concrete mechanism for the scaling argument. | Follow the maintainer through merge, failure and the decision about what can safely be restored. Reveal the missing downstream check as a question the maintainer must answer. Introduce the authorization and evidence questions when the relevant inspection fails. Keep the review queue as the first scaling example and use it to pose a choice about what the system may do while reviewers catch up. |
| **3 · Close the new flagship result inside the book** | [Unit 26](../editions/reader_manuscript/current/chapters/unit-26-integrated-reference-architecture-project-theseus-and-the-living-research-method.qmd#following-the-repository-change) follows the two-file repair and the eight-trial Git comparator. The technical reference’s opening also links the earlier comparison. The newer 16-pair result appears on the homepage and Quickstart, with no direct reference in either architecture capstone or the three-contribution summary. | Give Unit 26 one compact scene after the Git revert: a worker sees a timeout while the receiver may already have committed. Present the differences among retry, hold and close, and the exact observation that changes the choice. Link the same evidence from the [reference chapter](../chapters/integrated-reference-architecture.qmd#follow-one-request-before-following-every-subsystem) and [contribution summary](three_defended_contributions.md). Keep the denominators and inference separate. The Git result asks whether a reverted branch preserves an observed history. The receiver result asks how an ambiguous operation becomes known. |
| **4 · Make the receiver result harder to explain away** | [The fresh-task fixtures](../experiments/p5_u1_governed_repository_change/fresh_tasks.json) fix receiver deduplication by task. All eight deduplicating cases close in each arm. In the other eight, ordinary controls close four and the receiving-record arm closes eight. The most valuable result is the four closing decisions, and the design does not vary deduplication for the same task. The workflow observer reads the same local SQLite journal whose writes define the scripted effect. | Keep the published series intact. In a subsequent crossed design, run every task with both sink contracts. Cross observer freshness and availability with delay and acknowledgment loss. Include a known case with a stale projection, share read/timeout budgets, and score the downstream effect through a differently implemented observation path where that is feasible. Allow a conventional status lookup to close a case when it verifies the same identity and effect. Print the route-level counts by condition. Make a production example a separate step, with its own scope. |
| **5 · Replace template endings with consequences** | All 26 units end with “What This Establishes.” Twenty-one have “The Strongest Simpler Baseline,” and nineteen have “Evidence That Would Change the Conclusion,” by exact heading. Good argumentative moves recur, but as separate near-identical end matter they postpone the practical contrast. Unit 26’s gateway alternative already belongs next to the delayed retry, where the comparison matters. | Fold each baseline and objection into the scene whose interpretation it changes. Use a close specific to the unit, such as “Which check reopens customer delivery?” or “What can a single independent report settle?” Keep exact evidence ceilings, exercises and navigation. Start with Units 17, 21, 22 and 26. Preserve existing inbound anchors where renaming headings. |
| **6 · Rebuild Unit 21 around its two patches** | [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd#the-same-green-patch-two-different-lessons) has 7,468 counted words and 38 level-two or deeper headings. Its two causes make a good opening. The reader then crosses eight persistence loci, model editing, feedback, data lineage, unlearning and discovery before the two patches are adjudicated. | Decide the two patches immediately. Use a comparison table for the eight placements and develop only three in the main sequence: a dated fact, a check at the point of use, and a code repair or blocked tool. Keep optimizer updates, unlearning and scientific discovery as linked extensions with one sharply bounded consequence each. Preserve Atlas as a separate test of whether exploratory evidence justifies continued work. The reader should be able to choose a placement for an unseen failure without memorizing all eight names. |
| **7 · Separate evaluation from the decision to serve** | [Unit 22](../editions/reader_manuscript/current/chapters/unit-22-evaluation-readiness-thresholds-and-structured-assurance.qmd#the-candidate-that-passed-yesterdays-test) opens with four reasons for holding a candidate. It then ranges across benchmark ratchets, deception, commitments, readiness, assurance and photo provenance. The opening shows why generic green status fails but asks the reader to follow multiple failures at once. | Lead with one stale evaluator and carry the candidate through three consecutive decisions: measure again, check which commitment applies, and choose the bounded serving disposition. Give every decision one input and one output. Use the unresolved cache migration as the held-out exercise after the reader understands those distinctions. Give photo provenance a short evidence-authenticity sidebar with a link to its technical owner. |
| **8 · Make handoffs and escalation teachable** | [Unit 6](../editions/reader_manuscript/current/chapters/unit-06-human-intent-control-and-epistemic-security.qmd#meaningful-control-is-a-resource-condition) shows a rushed green approval. [Unit 22](../editions/reader_manuscript/current/chapters/unit-22-evaluation-readiness-thresholds-and-structured-assurance.qmd#calibration-abstention-and-coverage) correctly says a fallback needs competence, time and authority. The reader gets a checklist and few side-by-side outcomes that distinguish a useful handoff from a transfer of burden. | Give a single reviewer two proposals with different error patterns and a limited time budget. Record what the model suggests, what the reviewer sees, time to usable action, which errors the reviewer catches and which incorrect suggestions the reviewer adopts. Give the reader a choice among independent check, narrow action and hold. Make the package short enough to demonstrate why a meaningful review can fail even when disclosure looks complete. |
| **9 · Decouple technical authority from legitimate authority with a different setting** | [Unit 7](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd#dissent-appeal-and-rights) and [Unit 8](../editions/reader_manuscript/current/chapters/unit-08-institutions-coordination-and-societal-resilience.qmd#the-affected-public-is-part-of-the-system) cover dissent, standing, representation and remedy. Unit 8 again starts with a repository and then lists downstream groups. One affected person rarely has enough narrative agency to alter the decision. | Add one explicitly hypothetical non-software case, such as an institution correcting a mistaken service-eligibility notice. Follow an affected person, staff member and independent appeal route. Let a valid technical approval and a legitimate challenge coexist. Show how access to a remedy changes what the institution may close after correcting its internal record. Keep legal conclusions jurisdiction-specific or outside the hypothetical. |
| **10 · Give the ASI stress case a progression** | [Unit 1’s review budget](../editions/reader_manuscript/current/chapters/unit-01-asi-is-a-stack-not-a-model.qmd#why-greater-capability-makes-boundaries-more-important) and [Unit 25’s control limit](../editions/reader_manuscript/current/chapters/unit-25-recursive-improvement-replication-and-containment.qmd#improvement-velocity-has-a-control-limit) are connected. The reader still meets backlog, evaluator replacement and replication as separate topics with several transitions left implicit. | Stage the same proposal process three times. In the first, reviewers keep up. In the second, the queue saturates and the system must keep searching in isolation or slow effect-bearing work. In the third, the proposed verifier changes the evidence used to qualify its successor. Require a reviewer, a measured outcome and a stop condition at each stage. State which parts have artifact support and which are stress assumptions. This is where the title should pay off intellectually. |
| **11 · Teach a mechanism before its taxonomy** | [Unit 13’s semantic identity section](../editions/reader_manuscript/current/chapters/unit-13-cognitive-compilation-and-semantic-ir.qmd#stable-semantic-identity) explains stable obligations but does not put the original, transformed and repaired representation on a single small surface. [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd) has 34 headings and covers both route selection and a tour of architectures. | For Unit 13 show a source sentence, a small three-field lowering, one plausible incorrect mapping and the repaired result. Explain the generic IR only after the reader finds the error. For Unit 19 teach eligible routes, a same-cost comparison and the checkpoint failure first. Keep H-Net, recurrence, CRAM and the compact-model case as reference branches organized by the property they change. The reader needs to know how to test a replacement before surveying architectures. |

#### Resources that would change a passage

I did not find these papers by title or distinctive terminology in the current source inventory. Their purpose here is to supply a test, a competing explanation or a known design limit. Add the first ones where they replace generic prose. One strong reference per worked decision is sufficient.

| Resource | Use in this book | Boundary of the transfer |
|---|---|---|
| **Saltzer, Reed and Clark, _End-to-End Arguments in System Design_** | Make this the first addition to Unit 17, Runtime Adapters and the headline experiment’s prior art. Show three facts after an ambiguous reply: the sender tried, the receiver committed, and the intended recipient obtained the result. Ask which layer can verify each fact, including duplicate suppression. This gives the current observation argument a serious antecedent and a sharper boundary. [MIT primary text](https://web.mit.edu/saltzer/www/publications/endtoend/endtoend.pdf) | A receiver’s journal is enough for a scoped commit claim under the fixture’s assumptions. A claim about use by the end recipient requires evidence at that endpoint. |
| **Garcia-Molina and Salem, _Sagas_** | Use beside Unit 17’s compensation case. One of two separately committed steps has already taken effect and the second fails. Ask the reader what the compensating action restores, who may issue it and what earlier observer history it leaves visible. [Princeton report](https://www.cs.princeton.edu/techreports/1987/070.pdf) | A compensating transaction amends a partial execution under a declared model. It cannot erase all consequences that occurred while the earlier state was visible. |
| **Bansal et al., _Does the Whole Exceed its Parts?_**, paired with **Mozannar and Sontag, _Consistent Estimators for Learning to Defer to an Expert_** | Add the experimental result to Unit 6’s approval story and use the formal paper where Units 19 and 22 choose a fallback. Bansal et al. found that explanations increased acceptance of recommendations whether correct or incorrect in their study. Mozannar and Sontag give a route that depends on the downstream expert’s performance, which motivates evaluating who actually catches a given error. [CHI study](https://www.microsoft.com/en-us/research/publication/does-the-whole-exceed-its-parts-the-effect-of-ai-explanations-on-complementary-team-performance/) · [ICML paper](https://proceedings.mlr.press/v119/mozannar20b.html) | Measure joint outcomes and fallback capacity in the intended workflow. A supervised classification setup cannot establish that the reviewer has time, authority or a working stop path. |
| **Bailis et al., _Coordination Avoidance in Database Systems_** | In Context Transactions, contrast an append of independent notes with two actors reserving the same last unit of a resource. Check which operations preserve the declared invariant after merging. This gives the book a concrete way to decide when coordination earns its latency. [VLDB paper](https://www.vldb.org/pvldb/vol8/p185-bailis.pdf) | The formal condition concerns a specified set of transactions, merge behavior and invariants. For the reader example, spell out which operation would break the invariant. |
| **Dwork et al., _Generalization in Adaptive Data Analysis and Holdout Reuse_** | Use in Unit 22 and Benchmark Ratchets. Show a sequence where a developer repeatedly reads a protected pass/fail result and changes the selection policy. Ask which denominator remains an independent test. Use a fresh holdout for the simple method, then mention controlled reuse where the mechanism and assumptions are specified. [Primary preprint](https://arxiv.org/abs/1506.02629) | The paper does not license repeated access to an arbitrary benchmark. A particular method and its assumptions govern any reusable validity claim. |
| **Sculley et al., _Hidden Technical Debt in Machine Learning Systems_** | Use in Unit 21 next to the decision to make a lesson durable. Follow a temporary exception into an input dependency used by two downstream models. Give the reader a choice between keeping a dated local exception, fixing the shared feature or retiring the dependency. [NeurIPS paper](https://papers.nips.cc/paper_files/paper/2015/file/86df7dcfd896fcaf2674f757a2463eba-Paper.pdf) | The paper motivates a lifecycle risk and an ordinary maintenance comparator. It supplies no measured advantage for adjudicated persistence. |

The seven sources now change specific decisions. Saltzer, Reed and Clark
locate the evidence at the endpoint that can witness it. Sagas gives the
operator a compensating action with an observable historical remainder.
Bansal and colleagues and Mozannar and Sontag sharpen the reviewer and
fallback comparisons. Bailis and colleagues supply a merge counterexample.
Dwork and colleagues distinguish repeated selection from independent
evaluation. Sculley and colleagues give the temporary workaround its
downstream consumers. Each passage distinguishes its source from the
book's illustrative case.

#### Sample rewrite for the opening

Proposed wording for a short part of Unit 1. The incident remains hypothetical.

> On Monday, the maintainer approved a dependency upgrade. Every test in the repository passed. On Thursday, a downstream service failed. It relied on a default the upgrade had changed, and its test was in another repository.
>
> The maintainer could see the approved patch and the green checks. She could also see the failing service. The records did not show whether anyone responsible for the upgrade had checked the old default. The patch had passed the tests it was given. Restoring the old version might help the service, but the team still needed to inspect what the upgrade had changed while it ran.
>
> Those are three different questions. Who could approve the patch? What did the tests cover? What must the team observe before it calls the service recovered? The architecture is useful when it gives the maintainer a way to answer each one.

The original’s remaining questions about planning, learning and history can appear as later handoffs. This version lets the maintainer discover the need for them one at a time.

#### Order of revision and acceptance checks

1. **First sitting.** Rewrite the reader landing and Unit 1. Update Unit 26 and both technical evidence routes so a reader can follow the current finding from headline to raw outcome. Preserve the three existing evidence levels: the illustrative incident, the retrospective Git repair, and the prospectively fixed scripted receiver series.
2. **Four difficult units.** Reshape 13, 19, 21 and 22 around one worked decision each. Redeploy definitions, catalogs and objections as references at the point the case needs them. Then apply the ending rewrite to Units 17 and 26. Read each revised unit in rendered order with the initial case visible and confirm that the unit answers its opening question.
3. **Expand the range of the book.** Write the affected-person case for Units 7 and 8 and the escalating verifier scenario for Units 1 and 25. In both, give a human with limited information a consequential choice and a credible alternative. Add the outside sources only where they change an example or test.
4. **Check the result with readers and evidence.** Use the existing rollout, evidence and persistence prompts with a few independent readers when they are available. Ask for a first decision and the observation that would change it. For the headline result, test same-task deduplication and observation availability in a new frozen series. Report a safe hold separately from a useful closure, and retain ordinary controls that already do the job.

The short-term deliverable is a better living manuscript. Evaluate that through the reader decisions, source-to-claim checks and rendered handoffs. The frozen-release judgment is outside this editorial pass.

#### Crossed receiver evidence

All 14 controls passed and all 160 preregistered pairs are retained. The
conventional status route closed 128, and the additional observation route
closed 144. The difference comes from the stale-status and unavailable-status
profiles with an available fresh receiving-side read and no receiver
deduplication. Both paths match with fresh shared status. In the shared
failure profiles the second read produces no extra closures. No repeated
effects or false closures occurred. The matched contexts use one simulated
receiver and logical time. Human effort and physical isolation remain open.
[Protocol](../experiments/p5_u1_governed_repository_change/crossed_receiver_protocol.md) · [All paired outcomes](../experiments/p5_u1_governed_repository_change/results/2026-11-20-crossed-receiver.json)

#### Reader trial for the revised decision paths

Use the prompts below after each reader has seen the corresponding passage.
Give each person the same starting facts and let them decide before showing
the expected observations. Record the manuscript commit or preview identity,
the chosen action, the decisive observation, the owner the reader named, and
whether an anchor or an unfamiliar term interrupted the reasoning. Anonymize
notes by default. Use recurring mistakes to reopen the relevant passage.

| Passage | Fresh task to hand the reader | What to look for in their answer |
|---|---|---|
| [The Unit 1 opening](../editions/reader_manuscript/current/chapters/unit-01-asi-is-a-stack-not-a-model.qmd#the-change-that-worked) | The rollback command succeeds and the failing client still gets an error. Decide what the maintainer can report to the service owner. | Distinguish restored version, tested service behavior and an unresolved effect. |
| [Leena's appeal](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd#service-eligibility-appeal) and [Unit 8](../editions/reader_manuscript/current/chapters/unit-08-institutions-coordination-and-societal-resilience.qmd#service-eligibility-remedy) | The intake office corrects the record. The dispatch partner has not acknowledged the correction. What can the reviewer close? | Separate the institution's correction, the service outcome and any remaining remedy. Name a person who can obtain missing evidence. |
| [Unit 21 placement exercise](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd#decision-exercise-where-should-the-lesson-live) | Use the existing pickup-code exercise. Ask what would let the local team retire the dated memory entry. | Name the expiry and a qualified check that would make the manual reminder unnecessary. |
| [Unit 22 cache exercise](../editions/reader_manuscript/current/chapters/unit-22-evaluation-readiness-thresholds-and-structured-assurance.qmd#decision-exercise-cache-migration) | Use the existing shared-cache scenario, then ask what would change the ruling for an unrelated canary. | Keep the affected rollout open and distinguish a current test from the specific approval and recovery evidence. |
| [The verifier sequence](../editions/reader_manuscript/current/chapters/unit-25-recursive-improvement-replication-and-containment.qmd#three-speeds-of-verifier-change) | The proposal queue empties because the verifier now approves its own successor. Which measured improvement should the team use? | Identify the compromised promotion evidence and ask what an outside challenge must observe before the successor can serve. |

Record feedback or a missing observation against the prompt that produced it.
This packet has yet to receive independent reader responses.

### November 20 trace, evidence and reader-testing pass

The Quickstart, Unit 26 and the integrated reference now open with the same source-link repair. The two files are the generator and the generated reader configuration. The blocked case grants access to the generator alone. The observed outputs are file contents, disposition records and sandbox Git history. The separate browser check covers the rendered public link. The fixture, the validator replay and the larger architectural scenario now appear as distinct references behind that trace. The original twelve trials and the four new matched pairs remain separate. [Quickstart](../editions/reader_manuscript/current/quickstart.qmd#ordinary-change-control-comparison) · [Comparison record](../experiments/p5_u1_governed_repository_change/results/2026-11-20-conventional-comparison.json)

The conventional path uses scoped Git change control with scripted approval. It qualifies the same two authorized repairs as the governed path, leaves zero wrong blocks and zero unresolved terminal file or branch states, and restores both remote files through revert. It keeps the original effect in branch ancestry, while the governed path keeps it under an audit ref. The sidecar count is 0 versus 14. It excludes ordinary Git metadata and does not estimate active human time. The original defect and its repair were known, and the two workflows ran on separate disposable local remotes. The next adoption comparison would need real reviewers on fresh work, with the same task opportunities and a shared recovery boundary. For those sessions, time active review, interruption diagnosis and recovery separately from queued time and machine time.

#### Evidence audit of the adoption claims

| Decision in the book | What Sorenson's work supplies | What the local evidence establishes | What the outside result supplies or what remains open |
|---|---|---|---|
| **Replace an implementation under a stable field** | The Stable Capability Fields paper proposes consumer-scoped substitution, qualification, expiry and revocation. | The canary example accepts three synthetic records and rejects six controls. The canary lease is fixture-only and the default stays blocked. | MUSCLE measures negative flips for specific model and downstream-task updates. It motivates paired case checks and supplies no result about the stack's leases, rollback or production authority. [SCF source](../sources/source_notes/scf.md) · [Canary case](../chapters/stable-capability-fields.qmd#worked-replacement-decision-canary-qualified-default-still-blocked) · [MUSCLE](https://machinelearning.apple.com/research/model-compatibility) |
| **Choose where to persist a lesson** | Adjudicated Persistence proposes separate experience, lesson, placement and review decisions. Its propositions and evaluation program concern the choice of mechanism. | The two-case transaction makes equal outcomes coexist with different proposed repairs. It illustrates placement. Qualification for a new use needs outcome evidence from that use. | Ten Percent reports learned external prototype/count state alongside a frozen backbone, with an additional fitted head and a rejected challenge step. It provides a concrete persistence locus and a confounded attribution example. [Author source](../sources/source_notes/adjudicated_persistence.md) · [Worked transaction](../chapters/adjudicated-persistence-and-the-adaptive-commit-boundary.qmd#a-worked-two-case-transaction) · [Ten Percent source boundary](../sources/source_notes/ext_ten_percent_challenge_2026.md) |
| **Pay for learned routing** | Octopus supplies the proposed head, bounded specialist roles and lifecycle. | The P4/M6 full route produced 21 useful outcomes and two unsafe outputs, versus nine useful and zero unsafe for its LLM-first comparator. That mixed result earns neither default routing nor broad safety. | The six-router study supplies a matched-cost two-model random comparator for whole-model selection. Its result cannot decide the book's permissions and tool questions. [Octopus source](../sources/source_notes/octopus_router.md) · [Held-out result](../chapters/routing-heads-and-specialist-cores.qmd#p4m6-held-out-routing-result) · [Routing study](https://arxiv.org/html/2610.02762v1) |
| **Adopt the integrated workflow** | VIEA and TALOS supply proposed authority, typed work and observation handoffs. | A local historical repair checks named file and branch effects. The ordinary comparator matches the governed result at this scope and retains branch ancestry. | Approval and Git practices provide a practical comparator. Cross-service late effects, real reviewer effort and transfer to fresh work remain open. [VIEA](../sources/source_notes/viea.md) · [TALOS](../sources/source_notes/talos.md) · [Matched replay](../experiments/p5_u1_governed_repository_change/results/2026-11-20-conventional-comparison.json) |

#### Reader decision sessions

Use the exercises in Units 9, 15 and 21 after readers have completed the relevant passage. Ask readers to write a first decision and the evidence that could change it before opening a discussion. Rotate the first exercise between sessions. Give credit for an equivalent decision justified by the case. Collect where the reader looked, time to first decision, what they treated as authority or evidence, and any caveat they missed. Retain anonymized notes with the edition and exact exercise text. Recruiting and observing readers are still pending.

| Exercise | What a successful answer should do | Manuscript change if the answer repeatedly misses |
|---|---|---|
| [A stronger route with an expired check](../editions/reader_manuscript/current/chapters/unit-09-stable-capability-fields-and-governed-replacement.qmd#decision-exercise-a-stronger-route-with-an-expired-check) | Hold customer delivery, distinguish the canary scope from the delivery check, inspect the stale notice and ask for fresh customer-scope evidence and authority. | Put the paired regression beside the grant and current qualification record. |
| [Two logs agree on a shipment](../editions/reader_manuscript/current/chapters/unit-15-verification-bandwidth-claim-ledgers-and-proof.qmd#decision-exercise-two-logs-agree-on-a-shipment) | Support only the shared report. Spend the next check on a receiving-dock record tied to the shipment and time, or an equivalent independently grounded observation. | Draw the common webhook line explicitly and place the claim above its missing obligation. |
| [Where should the lesson live?](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd#decision-exercise-where-should-the-lesson-live) | Store the corrected code with source and expiry under the applicable rights. Propose a fresh-code check as a candidate procedure, then try it on a fresh case that separates stale from valid codes. | Put expiry, behavior and the next qualifying test in three adjacent fields of the example. |

### November 19–20 chapter-by-chapter cohesion review

This pass followed the chapter summaries, declared claims, worked examples, and source assignments of all **89 technical chapters** at `3b6dce76`, and the opening route and technical owners of all **26 reader units**. I read the complete passages around the cross-chapter problems below and checked relevant source notes and selected primary sources. The baseline has **587 registered sources**, **1,451 chapter-source assignments**, and **158,989 counted reader words**. The three latest integrations added 31 source notes, each with a primary link in the corresponding technical chapter's prose. That is a placement check. The chapter review evaluates how each connection works, and passage or result verification is scoped to the examples examined.

#### Corrections in this pass

- **Exploration can enter the record. Confirmation has a higher bar.** The former headline claim in Scientific Discovery could exclude the exploratory evidence the Answerability Atlas case was designed to preserve. The revised claim retains exploratory results with provenance and reserves prospective registration for confirmatory claims. Unit 21 now applies the same distinction. The benchmark chapter continues to own the separate question about whether a corrected baseline changes the decision. [Scientific Discovery](../chapters/scientific-discovery-and-experimental-governance.qmd#core-claim) · [Atlas comparator correction](../chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd#atlas-baseline-correction)
- **Field identity, serving eligibility, and changing the serving route have distinct owners.** The Policy Optimization summary now hands a candidate from the Stable Capability Field contract to Readiness and then to Capability Replacement. Operations now explicitly returns a recovered or replacement candidate for qualification because active eligibility can lapse during an incident. [Policy Optimization](../chapters/policy-optimization-and-learning-from-feedback.qmd#summary) · [Operations](../chapters/governed-operations-incident-command-and-graceful-degradation.qmd#summary)
- **Specify the proposition before citing the proof.** The Lean summary now distinguishes validation of record shape, proof of an encoded proposition, observations about execution, and measurement on a benchmark. The wrong-approver example checks the proposition against the intended policy. The wrong-adapter example checks whether that proposition maps to production. [Lean Proof Envelope](../chapters/executable-specifications-and-lean-proof-envelope.qmd#summary)
- **Credit the source and connect the finding.** Appendix H now files *Performative Prediction* and *Cognitive Architectures for Language Agents* with their external authors. The world-model chapter now links the MiraBench example to the question Sorenson's Reflexive Model-World Systems raises about deployment changing which trials can later be observed. The integrated reference uses its existing repository trace to name the record that leaves each layer. [External sources](../appendices/H_external_sources.qmd) · [Integration trace](../chapters/integrated-reference-architecture.qmd#six-research-objects-one-governed-cycle)

#### Where to reduce the burden

The technical edition currently repeats an eighteen-stage lifecycle heading across **14 chapters**. Some of those stages carry different decisions. For example, a deployment threshold activates a prior commitment, while a safety case reopens when a supporting claim loses its evidence. Keep those differences next to the worked examples. Use Living Book Methodology for their shared versioning and evidence mechanics, and keep the complete domain-specific record near its interfaces. The Context ABI, Replaceable Substrates, Benchmark Ratchets and Resource Economics chapters have particularly wide source assignments. Give each a short reading path built around its primary decision, then use the source crosswalk for alternate families, release history and related methods.

The strongest reduction is to reuse the decisions already in the book. Follow the existing repository change for an authority-to-effect path, Gantry-08 for the path from prediction through observation, retrieval and verification, and Answerability Atlas for a research result that survives a decision to stop. Use separate receipts at each handoff and name the one new question each chapter answers. Preserve numerical bounds, adverse results, original paper links and unpublished or unrun stages when moving material. The chapter actions below identify the specific handoff or source boundary to preserve in future edits.

#### Technical chapter review

##### Part I · Foundations, Alignment, and Governance

| Chapter | Cohesion and source integration |
|---|---|
| [Stack thesis](../chapters/asi-is-a-stack-not-a-model.qmd) | Keep the denied-effect case as the opening demonstration. Use VIEA and Drexler’s service framing for architectural lineage, then compare the layered path with ordinary change control under the same effect boundary. |
| [Efficiency hypothesis](../chapters/the-efficient-asi-hypothesis.qmd) | Keep the full-cost comparison as the argument. Let the routing chapter own the matched-cost random-pair benchmark and link to it as a challenge to the claimed savings from routing. |
| [Authority](../chapters/system-boundaries-and-authority.qmd) | Keep the canonical grant tuple here. In Intent-to-Execution and Runtime, cite the same authority tuple and describe only the conformance and enforcement failures distinctive to each. |
| [Failure modes](../chapters/failure-modes-of-ungoverned-intelligence.qmd) | Route the green-dashboard case into the runtime incident record, the correction into Claim Ledgers, and the proposed lesson into Adaptive Persistence. Trim the taxonomies after those handoffs are visible. |
| [Misuse uplift](../chapters/dangerous-capability-domains-and-misuse-uplift.qmd) | Keep actor uplift and observed outcomes as separate evidentiary questions. Point to Thresholds for the policy response to a measurement and to Operations or Societal Resilience for observed incidents. |
| [Military AI](../chapters/military-ai-autonomous-weapons-and-strategic-stability.qmd) | Keep the public-safe governance vignette and its distinction between an available stop button and a person with time and authority to use it. Point back to Meaningful Control for the general doctrine. |
| [Evidence states](../chapters/evidence-states-and-claim-discipline.qmd) | Preserve the KERC failed-then-narrowed result as the canonical example of claim scope. Send benchmark design to Benchmark Ratchets, claim identity to Claim Ledgers, and publication projection to Living Book Methodology. |
| [Scalable oversight](../chapters/scalable-oversight-and-adversarial-ai-control.qmd) | Keep the selectively reported update and distinguish supervisor availability from the supervisor’s ability to inspect relevant evidence. Link the correlated-errors exercise for the shared-evaluator failure. |
| [Human intent](../chapters/human-intent-as-a-formal-input.qmd) | Distinguish DiscoBench’s missing referent from approval to change the release. Put the model’s next question beside the exact part of the intent contract it can resolve. |
| [Meaningful control](../chapters/human-factors-and-meaningful-control-in-oversight.qmd) | Make the late approval the main case. Pair reported trust and intended verification with observed review behavior, then send effect-time enforcement to Runtime. |
| [Communication](../chapters/human-ai-communication-persuasion-and-epistemic-security.qmd) | Follow one message beyond generation into delivery and contest. The persuasion studies inform the communication risk while the disclosure rule and appeal path come from the stack’s governance. |
| [Constitution](../chapters/constitutional-alignment-substrate.qmd) | Keep the broadening amendment as the decision under review. Use Constitutional AI as a training comparator and Collective Constitutional AI as a participation comparator. The book’s amendment and remaining authority live here. |
| [Learned objectives](../chapters/inner-alignment-mesa-optimization-and-learned-objective-integrity.qmd) | Use the header-dependent behavior to anchor competing explanations. Refer persona interventions to White-Box Evidence and proxy selection to Objective Formation. |
| [Moral conflict](../chapters/moral-uncertainty-and-value-conflict.qmd) | Place the 9–1 and 6–4 comparison directly beside the contested export. Keep the minority rationale and the identity risk in the decision record alongside the modeled judgment distribution. |
| [Objective formation](../chapters/governed-objective-formation-value-learning-and-goal-integrity.qmd) | Use the proxy-agrees case to show who may revise the target. Keep preferences and evidence as inputs. Link Policy Optimization where that target becomes feedback. |
| [Institutions](../chapters/institutions-international-coordination-and-public-legitimacy.qmd) | Organize the packet around the three missing affected publics. Keep mandates, representation and jurisdiction here. Hand internal effects to Operations and cross-organization repair to Societal Resilience. |
| [Societal resilience](../chapters/societal-resilience-and-misuse-defense.qmd) | Keep the service-restored case and name the external parties still owed a remedy. Incident-response guidance supplies a comparison for internal restoration. Cross-organization harm remains the chapter’s distinct problem. |
| [Stable fields](../chapters/stable-capability-fields.qmd) | Make the canary-qualified/default-blocked trace the explanation of consumer-relative substitutability. Keep SCF and Deterministic Capability Compilation as the design lineage, MUSCLE in the replacement chapter as an instance-level comparator. |
| [Replacement](../chapters/capability-replacement-and-rollback.qmd) | Make the old-only five cases inputs to the existing canary decision. Put alias rollback, residual user exposure and recertification in one receipt. |
| [Security kernel](../chapters/security-kernel-and-digital-scifs.qmd) | Follow the refusal and protected content to their separate destinations. Use the authority chapter for grant semantics and Privacy for data-use purpose. |
| [Model attack surface](../chapters/adversarial-machine-learning-and-model-attack-surface.qmd) | Maintain a checkpoint-specific defensive scope and send authorization decisions to the kernel. Use the threat ledger to index safeguards instead of re-explaining all effect controls. |
| [Privacy](../chapters/privacy-data-rights-and-information-flow-governance.qmd) | Carry the recipient check from the AgentCIScope scheduling example into the lifecycle’s recipient and derivation fields. Keep the deletion case for what happens to already-made copies. |
| [Confidential computation](../chapters/confidential-and-verifiable-ai-computation.qmd) | Keep the enclave-valid/fallback-leaks example. RATS supports what the attestation asserts. The governing purpose, split of permitted leakage and application semantics need their own records. |
| [Weight custody](../chapters/model-weight-custody-and-hardware-roots-of-trust.qmd) | Follow one specific artifact and its derivative path from paging to key revocation. Point forward to irreversible release when a recipient escapes managed custody. |
| [Open weights](../chapters/open-weight-release-and-post-release-control.qmd) | Keep the one-public-copy case as the boundary. Link Thresholds for the pre-release commitment and Societal Resilience for remedy and coordination after release. |
| [Supply chain](../chapters/ai-supply-chain-integrity-and-lifecycle-provenance.qmd) | Join the licensing example to the existing three-project revocation graph by including a component → mixed dataset → descendant edge. The audit motivates the upstream check. The graph locates the downstream response. |
| [Recursive improvement](../chapters/recursive-self-improvement-boundaries.qmd) | Keep the canary that passes while an evaluator remains in question. Candidate qualification can proceed within a declared scope while changes to the evaluation machinery need their own review. |
| [Open-ended improvement](../chapters/open-ended-improvement-engines.qmd) | Put POET, FunSearch and ADAS in service of comparing candidate discovery loops. Keep the author’s campaign record and stop test visible before handing any candidate to replacement. |
| [Replication and containment](../chapters/autonomous-replication-proliferation-and-containment.qmd) | Keep the closed synthetic governance decision. Use the benchmark solely for scoping what its measurements cover and preserve the gap to inference about real environments. |

##### Part II · Planning, Memory, Reasoning, and Execution

| Chapter | Cohesion and source integration |
|---|---|
| [Intent-to-execution](../chapters/intent-to-execution-contracts.qmd) | Keep the correct-output/forbidden-means example as the cross-layer conformance test. Link to current-grant enforcement and observed effect rather than restating them. |
| [Perception](../chapters/perception-sensor-fusion-and-observation-trust.qmd) | Put missing-sensor calibration next to shared failure ancestry. Preserve separate rows for correlated sensors and for missing modalities. Give Planning and Embodied Control the resulting scoped observation. |
| [Planning](../chapters/planning-as-a-control-layer.qmd) | Use PlanForge’s failed dependency to distinguish an independent preview from a blocked deploy. Keep planning, qualification, dispatch and observation as separately attributable steps. |
| [World models](../chapters/governed-world-models-and-reality-grounding.qmd) | Build the reader path from latent prediction to LeWorldModel’s action-conditioned branches, MiraBench’s changed-command check and the actual observation. Cross-link Reflexive Model-World Systems when action changes the evidence-generating population. |
| [Reflexive model-world systems](../chapters/reflexive-model-world-systems.qmd) | Keep Performative Prediction as the formal comparator for deployment-dependent data and Sorenson’s work as the broader lineage and legitimacy proposal. Show what a future dataset can identify once the prediction changes which outcomes occur. |
| [Cognitive compilation](../chapters/cognitive-compilation-and-semantic-ir.qmd) | Place the schema-valid wrong field and the policy-faithfulness example on opposite sides of the same translation boundary. KERC and QCSA describe the representation design. The structured-output benchmark supplies a narrower failure comparison. |
| [Method transfer](../chapters/cognitive-method-transfer-and-qualification.qmd) | CoALA provides a comparator for memory and action organization. Keep the author’s source-method record and qualification decision as the distinct step before a technique can govern a new use. |
| [Context ABI](../chapters/virtual-context-abi.qmd) | Keep the release-note blocking correction across clustering, retrieval budget and packet emission. Route durable writes to Context Transactions and verification of packet adequacy to Verification Bandwidth. |
| [Durable semantic memory](../chapters/durable-semantic-memory-and-knowledge-lattices.qmd) | Join the lossy ontology migration to the named consumers that need reevaluation. Distinguish authorized storage, current belief, eligibility to retrieve and eligibility to reuse as a procedure. |
| [Context transactions](../chapters/context-transactions-snapshots-mounts-and-taint.qmd) | Use the restored snapshot and already-sent email to state the two recovery obligations. Keep cache freshness inside the context surface and send token replay to Artifact Graphs. |
| [Verification bandwidth](../chapters/verification-bandwidth-and-context-adequacy.qmd) | Use the two-model agreement counts to price the next independent check of the Gantry evidence. Spinoza owns the scoped verdict and Evidence States owns accepted support. |
| [Claim ledgers](../chapters/claim-ledgers-and-belief-revision.qmd) | Keep the stale policy claim’s earlier version and affected consumers. AGM and truth maintenance inform revision designs. The book’s audit and repair obligations need their own lineage. |
| [Spinoza](../chapters/spinoza-verification-and-proof-carrying-claims.qmd) | Keep the retired tribunal result as the central example. Distinguish which verification mode was used, what it established, and why a later evidence change reopens that verdict. |
| [Typed jobs](../chapters/labor-os-and-typed-jobs.qmd) | Make retry, completion and receiving acknowledgment visible on the same TALOS job trace. Workflow engines are competence baselines for job lifecycle. The runtime owns the observed external effect. |
| [Work surfaces](../chapters/ai-work-surfaces-agent-harnesses-and-organizational-absorption.qmd) | Treat product documentation as evidence that surfaces exist. Use the repository steward case to show what new state, permissions, and obligations the organization actually absorbed. |
| [Organizations](../chapters/human-ai-organizations-delegation-and-accountability.qmd) | Follow two hops of delegation and name the actual decision owner and burden holder. Compare the granted authority with each person’s real opportunity to intervene. |
| [Symbiosis](../chapters/human-ai-symbiosis-neurotechnology-and-cognitive-sovereignty.qmd) | Preserve the human-only, AI-only and joint arms. Add the time horizon to the same comparison so immediate complementarity and later skill or dependence remain legible. |
| [Deployment transition](../chapters/ai-deployment-transition-distribution-and-human-agency.qmd) | The aggregate gain and harmed subgroup belong beside one another. Link the skill-formation result to the selected short-term task and keep longer-term agency questions open. |
| [Artifact graphs](../chapters/artifact-graphs-audit-logs-and-replay.qmd) | Put matching bytes with different lineage and different tokens with pinned prompts in one replay contrast. LLM-42 is an inference control and tool-effect replay remains a separate grade. |
| [Runtime](../chapters/runtime-adapters-tool-permissions-and-human-approval.qmd) | Keep the approval/revocation race as the reason for a last-moment local permission check. Link Authority for grant semantics and Operations for unresolved external effects. |
| [Embodied control](../chapters/embodied-agency-real-time-control-and-physical-safety.qmd) | Use the missed period and qualified fallback as the anchor. Carry the timestamp and missing-modality result from Perception, then require closed-loop evidence under the plant’s own limits. |
| [Inter-stack exchange](../chapters/inter-stack-protocols-identity-and-economic-exchange.qmd) | Keep the disputed receipt as the motivating test. Endpoint identity and authenticated transport provide inputs to local authorization and effect observation. |
| [Multi-agent dynamics](../chapters/multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd) | Use the identical-grant/opposite-concentration comparison and the team-intervention evidence to expose population effects invisible in local receipts. Keep both useful outcomes and adverse outcomes in the denominator. |
| [Procedural memory](../chapters/procedural-memory-and-cognitive-loop-closure.qmd) | Keep the trace-to-tool decision anchored in Cognitive Loop Closure. Link CoALA for organization and CMTQ for applicability. A promotion receipt needs evidence that the procedure still works on the intended next task. |

##### Part III · Routing, Compression, Representation, and Substrates

| Chapter | Cohesion and source integration |
|---|---|
| [Routing](../chapters/routing-heads-and-specialist-cores.qmd) | Use the matched-cost two-model baseline beside the book’s held-out route results. Reserve curves for the cost/performance question and keep tool eligibility as a prior constraint. |
| [Replaceable substrates](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd) | Preserve H-Net as a learned granularity example, CRAM as a bounded energy-based search comparison, and Ten Percent as a narrow artifact-size and capability example. Compare each candidate against the same task and state contract before generalizing architectural claims. |
| [Relational dimensions](../chapters/relational-dimension-compilation-and-polyadic-cognition.qmd) | Keep the ternary relation and competent lower-order rescue on the same task. Distinguish transported semantic roles from structural order and operation count. |
| [Training](../chapters/governed-model-training-distributed-optimization-and-scaling.qmd) | Make the checkpoint that loaded but diverged carry the optimizer, data order and topology discussion. Link Learning–Compute Topology for the adaptive identity that a resume must preserve. |
| [Learning–compute topology](../chapters/learning-compute-topology-and-adaptive-process-architecture.qmd) | Organize the section around which adaptive state gets to fork, communicate or merge. Megatron and GSPMD describe distribution mechanisms. Their device topology alone tells the reader little about lineage independence. |
| [Generalization](../chapters/learning-theory-generalization-and-scaling-science.qmd) | Keep the frozen scaling forecast and protected holdout. Ask which population and budget a result can forecast and what would force re-estimation. |
| [Readiness](../chapters/readiness-gates-residual-escrow-and-quarantine.qmd) | Put the stale gate alongside canary and incident recovery. Eligibility is a continuously revisable decision. Thresholds owns the policy commitment and Replacement owns rollout. |
| [Personal compute](../chapters/personal-compute-hives-and-federated-edge-intelligence.qmd) | Keep the rented GPU losing on the whole job bill. Place federated enrollment and participation in a short sidebar under training so neither becomes a proxy for inference placement. |
| [Compact generation](../chapters/compact-generative-systems-and-residual-honesty.qmd) | Lead with the negative packet-size case and account for reconstruction and verification work. Link artifact-specific decoders and random-access tradeoffs to RankFold. |
| [Fast generation](../chapters/fast-generation-architectures.qmd) | Keep the DFlash/D3D contrast beside a workload-specific throughput and latency receipt. Link Routing for price-matched comparisons and Resource Economics for the complete cost. |
| [Deliberation](../chapters/governed-deliberation-and-test-time-scaling.qmd) | Start from the polished patch that lost the correct answer. Compare direct, extra deliberation and independent checking under the same evidence budget. Send decoder scheduling to Fast Generation. |
| [Artifact compression](../chapters/rankfold-neuralfold-and-artifact-compression.qmd) | Place the Ten Percent disk-versus-resident distinction and the RankFold exact-replay/random-access results on the same access-pattern decision. Keep task capability and hidden repair cost explicit. |
| [Resource economics](../chapters/resource-economics-and-token-budgets.qmd) | Own the reusable full bill for compute, verification, human work and downstream repair. Link Physical Compute for capacity and joules rather than building a second cost vocabulary. |
| [Physical compute](../chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd) | Keep the overlapping workloads and bottlenecks in the same time/place budget. Separate measured GPU electricity per answer from facility energy, emissions and allocation policy. |
| [Mathematical and search substrates](../chapters/mathematical-and-search-substrates.qmd) | Use one adoption comparison to show what changes in the searched solution space and what stays in the verifier. Link to the CRAM maze comparison in Replaceable Substrates when discussing energy-based search, and keep the maze and exact-verifier boundary visible there. |
| [Circle proof contracts](../chapters/circle-calculus-and-proof-carrying-ai-contracts.qmd) | Keep the two recipients of one receipt as the transport test. The author’s theorems concern exact structural claims. Send statement fidelity and deployed adapter binding to Lean Proof Envelope. |
| [Coil attention](../chapters/coil-attention-cyclic-memory-and-recurrence-contracts.qmd) | Use the fluent answer with a stale cache to explain state carry. A structural receipt has a limited role in judging whether the recalled fact is semantically current. |
| [CoilRA and cyclic mixers](../chapters/coilra-multicoil-rope-and-cyclic-mixers.qmd) | Preserve the 128-channel refusal. Link the recurrence-state obligations to Coil and keep this chapter’s distinctive focus on operator choice, position contracts and measured kernel behavior. |

##### Part IV · Evidence, Implementation, and the Living Book

| Chapter | Cohesion and source integration |
|---|---|
| [Lean proof envelope](../chapters/executable-specifications-and-lean-proof-envelope.qmd) | Use the new wrong-approver witness before the proof. Follow with the existing wrong-adapter example. Distinguish statement fidelity, formal validity, runtime correspondence and measured behavior. |
| [Benchmark ratchets](../chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd) | Use the Atlas correction to make the comparator choice change a continuation decision. Keep leaderboard uncertainty, evidence drift and learned judging tied to that reusable instrument. |
| [White-box evidence](../chapters/white-box-evidence-interpretability-and-activation-governance.qmd) | Preserve the topic-feature failure and the steering non-uniqueness comparison. Route trait changes to a scoped intervention claim and reserve learned-objective inferences for separate evidence. |
| [Capability thresholds](../chapters/capability-thresholds-and-deployment-commitments.qmd) | Own the prospective commitments that apply when specified evidence and safeguards change. Link Readiness for a concrete workload and Safety Cases for the argument covering the proposed deployment. |
| [Adversarial evaluation](../chapters/adversarial-evaluation-sandbagging-and-training-time-deception.qmd) | Keep the score change after monitor removal as the evidence trace. Its scoped finding goes to Evidence States. The model’s learned objective and the organization’s release policy each need separate decisions. |
| [Safety cases](../chapters/safety-cases-and-structured-assurance.qmd) | Make the stale control item and unresolved defeater sufficient to explain why the top-level argument reopens. Point to the benchmark, threshold and readiness records it depends on. |
| [Media authenticity](../chapters/content-authenticity-watermarking-and-synthetic-media-integrity.qmd) | Put the incomplete authentic photo and the fully documented wrongly captioned photo under the same verification prompt. Use the source studies as evidence about audience perception. |
| [Operations](../chapters/governed-operations-incident-command-and-graceful-degradation.qmd) | Start at the authority-to-effect incident and loop back to readiness on restored service. Keep unresolved effect reconciliation visible after internal state recovery. |
| [Adaptive persistence](../chapters/adjudicated-persistence-and-the-adaptive-commit-boundary.qmd) | Use the author’s competing placements for one observed lesson. The Ten Percent external learned state illustrates a persistence path. Link the reader’s compression example back to the adaptive commit decision. |
| [Policy optimization](../chapters/policy-optimization-and-learning-from-feedback.qmd) | Preserve the improving proxy/degrading faithfulness case with both score histories. A candidate update hands off to the field contract, readiness and authorized replacement. |
| [Data engines](../chapters/data-engines-continual-learning-and-unlearning.qmd) | Keep restoration, storage erasure and removal of learned influence distinct in the reported rollback example. Link Privacy for the right asserted and Reflexive Model-World Systems for changed evidence collection. |
| [Scientific discovery](../chapters/scientific-discovery-and-experimental-governance.qmd) | Give exploratory and confirmatory claims explicit routes. The Atlas source shows how a useful exploratory finding, a no-go and an unrun confirmation can coexist. Link Benchmarks for the comparator correction. |
| [Artifact stewardship](../chapters/artifact-steward-agents-and-living-project-governance.qmd) | Keep the author’s steward practices centered on continuity across project changes. The three prepared actions show where treasury, ownership and effect authority still require the relevant owners. |
| [Integrated architecture](../chapters/integrated-reference-architecture.qmd) | Keep one repository request as the spine. Let the six research objects index decisions in the trace and use the bounded implementation reference for which joins have actual evidence. |
| [Project Theseus](../chapters/project-theseus-as-report-first-implementation-reference.qmd) | Start with one retained report and its scope before branching to the project’s many receipts. A report establishes what the instrument observed under the pinned run. |
| [Prototype roadmap](../chapters/prototype-roadmap.qmd) | Keep the blocked phase gate and its prerequisite failure. Move changing program status to the current owner rather than copying it into several chapter conclusions. |
| [Living book methodology](../chapters/living-book-methodology.qmd) | Keep the structural-edit trace and stable URL. Put the shared method for versioning claim, source, evidence and publication records here and point reference chapters back to it. |
| [Research agenda](../chapters/open-research-agenda-and-bibliography-plan.qmd) | Use the four reference-entry paths to classify new papers. Make integration contingent on a new reader decision, a changed boundary or a known coverage gap, with unassigned leads retained in the research backlog. |

#### Reader edition handoffs

| Unit | Editing decision |
|---|---|
| [Unit 01](../editions/reader_manuscript/current/chapters/unit-01-asi-is-a-stack-not-a-model.qmd) | Carry the original denied effect into Unit 3. Name the decision the integrated trace later answers. |
| [Unit 02](../editions/reader_manuscript/current/chapters/unit-02-the-efficient-asi-hypothesis.qmd) | Freeze the quality and residual obligation before discussing the low-priced route. Link the measured routing comparator in Unit 19. |
| [Unit 03](../editions/reader_manuscript/current/chapters/unit-03-authority-failure-and-misuse.qmd) | Use one grant identifier across proposal, attempted effect and revocation. Keep risk-domain material as escalation examples. |
| [Unit 04](../editions/reader_manuscript/current/chapters/unit-04-security-privacy-and-ai-artifact-custody.qmd) | Separate the private calendar disclosure from copying/erasure and dataset-license provenance. Link the later receipt and appeal surfaces. |
| [Unit 05](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd) | Use one claim across proposed, scoped-supported and withdrawn outcomes. Link Unit 15 when the open question is what still needs checking. |
| [Unit 06](../editions/reader_manuscript/current/chapters/unit-06-human-intent-control-and-epistemic-security.qmd) | Use the customer-release ambiguity to show the line between disambiguation and authorization. Carry the accepted boundary into Unit 12. |
| [Unit 07](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd) | Keep the same disputed export for the amendment, external evidence about moral disagreement and the standing to decide. |
| [Unit 08](../editions/reader_manuscript/current/chapters/unit-08-institutions-coordination-and-societal-resilience.qmd) | Follow the affected public through participation and appeal. Point to Unit 17 when internal operations have restored service but harm remains. |
| [Unit 09](../editions/reader_manuscript/current/chapters/unit-09-stable-capability-fields-and-governed-replacement.qmd) | Attach the five old-only regressions to the existing replacement story and distinguish qualification for a canary from default eligibility. |
| [Unit 10](../editions/reader_manuscript/current/chapters/unit-10-perception-and-observation-trust.qmd) | Carry the exact observed interval and coverage forward to the trial and verification. Keep the missing-sensor and shared-cause examples distinct. |
| [Unit 11](../editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd) | Carry the same Gantry run into Unit 12 and preserve the difference between action-conditioned prediction, observed trial and feedback-dependent data collection. |
| [Unit 12](../editions/reader_manuscript/current/chapters/unit-12-planning-as-a-control-layer.qmd) | Use the frozen intent and current observations to teach replanning. Explain what to do with an independent authorized node when its neighbor is blocked. |
| [Unit 13](../editions/reader_manuscript/current/chapters/unit-13-cognitive-compilation-and-semantic-ir.qmd) | Keep one obligation across lowering, the wrong field and repair. Link forward to Unit 15 for testing whether the theorem actually expresses the obligation. |
| [Unit 14](../editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd) | Make each retrieval variant compete for the one consequential correction. Keep the call budget and verified source passage near the result. |
| [Unit 15](../editions/reader_manuscript/current/chapters/unit-15-verification-bandwidth-claim-ledgers-and-proof.qmd) | Use the Gantry claim to motivate an independent check. Keep the authorization theorem’s statement witness as a separate example of specifying what must be proved. |
| [Unit 16](../editions/reader_manuscript/current/chapters/unit-16-labor-os-work-surfaces-and-organizations.qmd) | Recover a single work identity across completion, delivery and acknowledgment. Use the skill-formation comparison when assessing who can still do the work later. |
| [Unit 17](../editions/reader_manuscript/current/chapters/unit-17-artifact-graphs-runtime-effects-and-operations.qmd) | Compare inference repeatability and effect repeatability within the same replay grade. Finish the incident with a qualification decision before normal service. |
| [Unit 18](../editions/reader_manuscript/current/chapters/unit-18-procedural-memory-inter-stack-exchange-and-multi-agent-risk.qmd) | Begin from one workflow trace. Promote only its qualified transferable part and show what happens when the next actor or population has different incentives. |
| [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd) | Start from one eligible routing pair, then compare controls under equal spend. Refer architecture-specific units for what the router’s input and state contract must preserve. |
| [Unit 20](../editions/reader_manuscript/current/chapters/unit-20-governed-training-and-learning-compute-topology.qmd) | Return to the checkpoint that loads but diverges whenever discussing new optimizer or execution topology examples. |
| [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Land each paper on a choice of where to persist the lesson, what proves it transfers, or whether to stop with exploratory evidence. Keep the two Atlas outcomes side by side. |
| [Unit 22](../editions/reader_manuscript/current/chapters/unit-22-evaluation-readiness-thresholds-and-structured-assurance.qmd) | Keep the stale gate as the running example. Let the separate provenance-label example explain what can be trusted about a visible record without silently extending the case. |
| [Unit 23](../editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd) | Price compactness, speed, and verified quality against the whole route. Cross-link the Ten Percent learned external state to Unit 21. |
| [Unit 24](../editions/reader_manuscript/current/chapters/unit-24-physical-compute-energy-and-infrastructure.qmd) | Keep placement and physical capacity in the main example. Use federated enrollment as a short comparison about training data coverage. |
| [Unit 25](../editions/reader_manuscript/current/chapters/unit-25-recursive-improvement-replication-and-containment.qmd) | Use the candidate verifier’s failure to show which evaluator, rights and stopping rules are in scope before promoting a successor. |
| [Unit 26](../editions/reader_manuscript/current/chapters/unit-26-integrated-reference-architecture-project-theseus-and-the-living-research-method.qmd) | Close on the same request that opened the book. Label proposed joins and the observed Theseus report separately and point to the readers’ next decisions. |

### November 19 research screen for chapters outside the last two integrations

**Integration disposition.** All ten placements below are now in the technical chapters and their nine reader units. Both editions use the revised Lean benchmark described below.

At `5e523e43`, the last two literature integrations had changed 18 distinct technical chapters out of 89. I used the other 71 as the candidate pool, ran 24 initial topic searches and followed up on individual papers and counterevidence. The searches ranged from formal specification, privacy, media provenance and moral disagreement to planning, replacement, perception, routing, federated learning and replay. I checked selected titles, identifiers or distinctive method names against the 576-entry inventory, manuscript and prior research notes. The ten placements below refer to technical chapters untouched in both rounds. Reader unit numbers follow the book manifest and can overlap earlier rounds. Study findings are attributed to their authors. The sample numbers, decisions and exercises proposed for the book are illustrative unless identified as study results.

#### Six worked examples, in editorial priority order

1. **Which cases did the upgrade break?** Extend the existing failed canary in [Capability Replacement and Rollback](../chapters/capability-replacement-and-rollback.qmd#worked-rollback-a-passed-precheck-does-not-survive-the-canary), with a four-cell table for Unit 9. On 100 paired cases, suppose 75 pass both versions, 5 pass only the old version, 12 pass only the candidate and 8 fail both. Accuracy rises from 80% to 87%. Five previously working cases break, or 6.25% of the old version’s successes. Have the reader examine which cases those five are before choosing whether to expand the canary. In *MUSCLE*, updating the base model induced exactly this kind of regression in downstream tasks. A compatibility adapter reduced negative flips by up to 40% in the reported comparisons. Task definitions, graders and the particular model versions determine which changes count as flips. The part worth teaching is the paired evaluation, usable even by a team that never trains the adapter. [MUSCLE, EMNLP 2024](https://machinelearning.apple.com/research/model-compatibility)

2. **What did the prover actually get asked to prove?** Place a statement-review step immediately before the adapter example in [Executable Specifications and Lean Proof Envelope](../chapters/executable-specifications-and-lean-proof-envelope.qmd#worked-proof-envelope-the-theorem-holds-the-adapter-differs). The chapter already has a correct theorem whose production binding fails. Introduce the earlier failure in Unit 15 with the requirement “every exported record has approval from its owner.” A formalization that requires approval from *someone* admits an export approved only by a colleague. Ask for that counterexample before giving the reader either proof or adapter. In *Beyond Compilation*, version 4 reports 87.2% compiling and 57.7% meeting the two-judge acceptance criterion on 227 mathematics statements. Human review attributed 23.8 percentage points of the 29.5-point gap to actual translation errors. These are statement-translation results on mathematics, and the authorization rule is a transfer exercise. [Beyond Compilation, evaluation protocol and human audits](https://arxiv.org/html/2606.31002v4)

3. **Could the agent complete the task while disclosing too much?** Add a two-recipient scheduling example under [the information-lifecycle transaction](../chapters/privacy-data-rights-and-information-flow-governance.qmd#the-information-lifecycle-transaction) and in Unit 4. The assistant may read a calendar entry to arrange cover. A colleague needs the time slot, while the reason for the absence belongs in a private message. Give readers the resulting tool actions and ask them to score the booking and each disclosure separately. *AgentCIScope* tested 12 agents on 936 constructed tasks. Across agents, the fraction of tasks with a disclosure violation in one run ranged from 32.5% to 94.4%. An additional exercise can ask whether any of five repeats disclosed the reason, a different measure from per-run frequency. The study uses single-agent environments and explicit disclosure constraints derived from public and synthetic cases. Real recipients can disagree about appropriate sharing. [AgentCIScope, evaluation and limitations](https://arxiv.org/html/2610.19158v1)

4. **What does a provenance label make a reader believe?** Extend [Visible disclosure](../chapters/content-authenticity-watermarking-and-synthetic-media-integrity.qmd#visible-disclosure) and Unit 22 with two human studies. An ICWSM experiment with 6,114 participants in the US, UK and Norway found that showing provenance on news previews increased perceived transparency, credibility and trust. A CSCW experiment with 595 US and UK participants found that incomplete or invalid provenance sometimes led people to disbelieve honest media. These results answer different questions. Give the reader a genuine archive photo with incomplete edit history and a fully documented photo paired with a caption from the wrong year. Ask three questions for each: which edits can be traced, what evidence dates the event, and how would you label what remains uncertain? Increased trust on a preview supplies no measure of how accurately readers resolve the caption. [ICWSM news-preview experiment](https://christophtrattner.com/pubs/ICWSM2026.pdf) · [CSCW provenance-state experiment](https://arxiv.org/abs/2303.12118)

5. **Does learning where to route buy anything beyond choosing two good models?** Add an external comparison beside [the held-out routing result](../chapters/routing-heads-and-specialist-cores.qmd#p4m6-held-out-routing-result). In *Dynamic LLM Routers are Often Misguided*, six commercial routers across 14 configurations failed to beat a random mixture of two well-chosen models at matched cost on the benchmark studied. In Unit 19, have readers choose an eligible model pair on development data, freeze it, then compare random and learned assignments on held-out requests at the same realized spend. Include an always-cheap and always-strong row to show what choosing the pair already bought. Keep the book’s permission checks ahead of assignment and report results by task. The paper compares whole-model inference services. Internal expert routing, restricted tools and deadlines introduce different objectives. [Dynamic LLM Routers are Often Misguided, setup and comparisons](https://arxiv.org/html/2610.02762v1)

6. **Can we defend the source labels in a training mixture?** Follow [the three-project revocation example](../chapters/ai-supply-chain-integrity-and-lifecycle-provenance.qmd#worked-revocation-one-component-reaches-three-projects) with a dataset assembled from several sources. A large-scale audit traced more than 1,800 text datasets and found frequent omissions and misclassification of licenses on hosting sites. Give readers a collection card with a single license label, one upstream record with documented terms, and another with missing attribution. Ask them to trace each component into two proposed uses, preserve the unknown and identify the evidence needed to clear it. The audit establishes a metadata-quality problem in the studied collections. It cannot settle rights to a particular artifact. Keep the full exercise in the technical chapter and give Unit 4 one component to trace alongside its privacy case. [A large-scale audit of dataset licensing and attribution in AI, Nature Machine Intelligence](https://www.media.mit.edu/publications/a-large-scale-audit-of-dataset-licensing-and-attribution-in-ai/)

#### Four additions that earn a shorter passage

- **Show a distribution of judgments in Unit 7.** After [the contested export](../chapters/moral-uncertainty-and-value-conflict.qmd#worked-contestability-example), give two panels the same majority verdict, one split 9–1 and the other 6–4. Preserve a minority rationale and ask what the decision owner still owes that group. *The Pluralistic Moral Gap* compared human and model judgments on 1,618 dilemmas. Agreement weakened on cases with more human disagreement, and models drew on a narrower range of values in their rationales. The human judgments came from a particular online community. Matching its distribution can test representation of disagreement while leaving the authority to decide unresolved. [EACL study and dataset](https://aclanthology.org/2026.eacl-long.305/)
- **Name which computation can be replayed in Unit 17.** Pair the [matching PDF with different tool lineage](../chapters/artifact-graphs-audit-logs-and-replay.qmd#worked-replay-matching-output-different-tool-lineage) with the converse example. Two runs of a pinned model can produce different tokens when other requests change batch shape and floating-point reduction order. LLM-42 verifies candidate tokens on a fixed-shape schedule and rolls back divergent work. Ask which evidence supports a claim about token identity, and which records would be needed to reproduce downstream tool effects. The method concerns inference in a specified serving environment. Cross-hardware equivalence and external side effects require separate evidence. [LLM-42, mechanism and serving experiments](https://arxiv.org/html/2601.17768v2)
- **Condition the sensor check on what was actually present in Unit 10.** After [Bayesian state estimation and concrete fusion regimes](../chapters/perception-sensor-fusion-and-observation-trust.qmd#bayesian-state-estimation-and-concrete-fusion-regimes), split the calibration table into camera plus encoder, camera only, and encoder only. Report how often the prediction set included the true state and how wide the set was in each row. *Conformal Fusion Under Missing Modalities* calibrates by the pattern of available inputs. A high pooled coverage rate can hide a weak camera-only row, and an extremely broad prediction set can achieve coverage while offering little guidance. Its guarantee assumes exchangeable calibration and test cases within each pattern. A camera that drops out specifically during vibration needs fresh evidence about those episodes. [Conformal Fusion Under Missing Modalities, calibration and limitations](https://arxiv.org/html/2608.07183v1)
- **Count who could ever participate in Unit 24.** In [Job classes and federation modes](../chapters/personal-compute-hives-and-federated-edge-intelligence.qmd#job-classes-and-federation-modes), distinguish federated *training* from the chapter’s dispatch of inference jobs. For training, draw three nested sets of devices: intended population, enrolled clients, and contributors this round. Show that correcting for intermittent charging among enrolled phones leaves an excluded device class invisible. *Who Trains Matters* derives two-stage inverse-probability weighting under assumptions about measured selection factors and nonzero inclusion probabilities. Its experiments use synthetic federated logistic regression. A class with zero chance of enrollment calls for narrowing the population claim or obtaining new evidence. [Who Trains Matters, assumptions and experiments](https://arxiv.org/html/2604.26604v1)

#### Where I would hold the line

Planning and memory-update searches returned additional benchmarks, but the last round already gave readers an action-perturbation exercise and the preceding round covered whether a stored correction remains usable. Another score table would add little until it changes how the reader distinguishes a bad plan from a stale belief. The [Safety Cases chapter](../chapters/safety-cases-and-structured-assurance.qmd#worked-trace-a-stale-control-result-and-an-unresolved-defeater) already walks through stale evidence and an unresolved objection. *Assessing confidence in frontier AI safety cases* is a reasonable source for a future example in which two reviewers assign different confidence to the same evidence. Its methodology alone is a weaker reason to add pages than any of the six exercises above. [Assessing confidence in frontier AI safety cases](https://arxiv.org/html/2502.05791v1)

### Second November 18 research screen and November 19 integration

**November 19 disposition.** The technical edition and reader units now include eight worked examples and six shorter comparisons. The six leads at the end of this screen remain open for research. All fit existing chapters. The highest priority is to show how to test a supposed second opinion, an improving reward, and a world model's response to a changed action. All three can look convincing while supplying weak evidence for the decision at hand.

**Scope.** I searched online using 25 discovery queries, then followed individual papers into their methods, results and limitations. The search covered training and data selection, inference and memory, model steering, evaluation and oversight, embodied prediction, scientific discovery, energy use, human skill and multi-agent coordination. I checked candidate identifiers, titles or distinctive technique names against the source inventory, technical chapters, reader manuscript and prior triage at commit `805b1603` (562 source records). This is a targeted literature screen. The reported numbers below come from the authors. The exercises and priorities are editorial proposals.

#### Eight worked examples worth the space

1. **What does a second model's agreement buy?** The book already asks for independent evidence. *Correlated Errors in Large Language Models* gives [Verification Bandwidth and Context Adequacy](../chapters/verification-bandwidth-and-context-adequacy.qmd) and Unit 15 a measurable comparison. On the HELM data examined, model pairs chose the same wrong answer about 60% of the time **conditional on both being wrong**. Uniform choice among the three wrong alternatives would give one third. This statistic alone gives neither the probability both are wrong nor the probability a particular consensus is correct. Give readers a table of paired answers and ground truth. Have them calculate shared wrong answers among joint failures, then errors among agreements. Ask whether a third model or a check against the original event record would resolve the release decision. Preserve the item mix and report the number of joint failures. [Primary paper, HELM analysis](https://arxiv.org/html/2506.07962v1)

2. **When does an improving reward conceal a worse explanation?** In [Policy Optimization and Learning from Feedback](../chapters/policy-optimization-and-learning-from-feedback.qmd) and Unit 21, use a short approval rule with a known minimal justification. Credit a response for including the sufficient facts, then append irrelevant facts and rescore it with an exact checker. In *Optimistic Verifiers Get Hacked*, the sufficiency proxy reached 0.940 while the exact faithfulness score fell from 0.731 to 0.667 on 96 held-out episodes. The authors found the direction of damage more reproducible than its magnitude. Their executable rules make an exact answer possible. Open-ended human preferences would need a different reference. This gives readers a concrete reason to save both score histories during optimization. [Primary paper, sufficiency comparison and replication](https://arxiv.org/html/2611.21538v1)

3. **Does the predicted future follow the command?** Add MiraBench beside the existing action-conditioned JEPA discussion in [Governed World Models](../chapters/governed-world-models-and-reality-grounding.qmd#leworldmodel-action-conditioned-dynamics) and Unit 11. The authors evaluated 12 configurations using over 16,000 human judgments. They assessed physical consistency, response to the commanded action, and the tendency to depict success after an action that should fail. For the book, freeze one simulated gantry frame and compare predictions for advance, hold, and a command that stops short of contact. A polished clip showing contact in all three cases fails the control test. Keep the action encoding, perturbation and comparison outcome in the record. The source evaluates predicted episodes. Qualification to control a physical gantry would require separate closed-loop evidence. [MiraBench, benchmark design and perturbation analysis](https://arxiv.org/html/2605.29360v1)

4. **Could a different intervention produce the same persona score?** Extend the [neuron and persona steering passage](../chapters/white-box-evidence-interpretability-and-activation-governance.qmd#personality-and-persona-steering) with a counterexample. The revised steering-vector study examines a single-layer intervention. A perturbation invisible to the local first-order output map can change the internal direction while leaving the predicted output shift unchanged to first order. The authors also evaluate perturbed vectors on finite prompts and semantic classifiers. Ask readers to compare the original vector, a perturbed vector and a norm-matched random control across held-out settings. A matched trait score supports a behavioral result under that assay. Establishing a unique internal representation would take additional constraints. Keep the linear argument distinct from empirical similarity at finite steering strengths. Add a brief cross-reference where Unit 5 already discusses persona steering. [Primary paper, v4, Figure 1 and perturbation experiments](https://arxiv.org/html/2602.06801v4)

5. **Price the whole answer in joules.** [Physical Compute Infrastructure](../chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd) already explains metering and allocation. Unit 24 could work through Table 1 of *Where Do the Joules Go?* On one B200 running Qwen3-32B, the authors report 95 GPU joules per conversational response and 2,192 per problem-solving response. The latter generated longer outputs and supported a smaller maximum batch. At the same batch size of 128 the reported energy per token was 0.209 versus 0.312 joules. Have the reader explain why neither that token ratio nor a nominal device power rating predicts the full response ratio. Then specify what must be metered to compare two routes on the **same accepted task**, including retries. The paper's GPU measurements and a facility's electricity and emissions accounts have different boundaries. [Primary paper, Table 1](https://arxiv.org/html/2601.22076v2)

6. **Move the experts while preserving the router's choices.** *Expert Coupling in MoE Pretraining* belongs in [Governed Model Training](../chapters/governed-model-training-distributed-optimization-and-scaling.qmd) and Unit 20. Experts frequently selected together can share a GPU. A dispatcher can then send a token once to that GPU even if two resident experts need it. Have the reader place four experts on two devices using a small table of co-selections, then repeat with a changed workload and check the busiest device. On the authors' MI300X cluster, collective communication improved by up to 2.63× and whole training steps by up to 1.41×. The evaluation used one 12-layer model, top-2 and top-6 routing, and 2.1B training tokens. Keep the expert choices fixed in the exercise so that the measured difference comes from placement and dispatch. [Primary paper, experiments and scope](https://arxiv.org/html/2610.09372v1)

7. **Can the operator still do the work after the assistant leaves?** *How AI Impacts Skill Formation* supplies a randomized comparison for the existing unaided-capability test in [AI Deployment and Human Agency](../chapters/ai-deployment-transition-distribution-and-human-agency.qmd). Use it in Unit 16's organizational example. Developers learned an unfamiliar asynchronous Python library. The assisted group scored lower on the subsequent quiz, with a reported difference of 4.15 points on a 27-point instrument. Average completion time showed no statistically significant improvement. Give a team a choice between an assistant that supplies a fix and one that asks the operator to predict the failure. Measure assisted completion and subsequent unaided diagnosis. The trial supports the assignment-level comparison on this task. The six interaction styles were identified from observed use, and the study did not follow a workforce through a long deployment. [Primary paper, experiment and interaction analysis](https://arxiv.org/html/2601.20245v2)

8. **Which measurement distinguishes two explanations?** In [Scientific Discovery and Experimental Governance](../chapters/scientific-discovery-and-experimental-governance.qmd) and Unit 21, start with observations at zero and one that fit both a linear and a square law. A measurement at two predicts either two or four. Charge for the measurement, freeze the observations, and ask a fresh analyst to submit the law and a held-out prediction. *Explore, Then Commit* compared eight configurations over 576 NewtonBench trials. On medium tasks with GPT-4.1-mini, the interpreter-enabled configuration averaged 8.6 measurements against 22.5 for the comparison. Random acquisition was competitive with disagreement-based selection, batch limits differed, and symbolic recovery varied across modules. The source supports teaching the full protocol in its noiseless setting. It leaves the benefit attributable to the acquisition heuristic open. [Primary paper, results and coverage-sensitive analysis](https://arxiv.org/html/2610.07620v1)

#### Six shorter comparisons

| Source and placement | Passage to add and limit to preserve |
|---|---|
| **The Structured Output Benchmark** · [Cognitive Compilation and Semantic IR](../chapters/cognitive-compilation-and-semantic-ir.qmd), Unit 13 | Use a schema-valid release record with the wrong controller limit. Grade parsing, individual field values and evidence for the field separately. Across 21 evaluated models the best exact leaf-value accuracy was 83.0% on the text set and 23.7% on the audio-derived set. Models received text-normalized inputs, including transcripts. These are different datasets with different context demands, so the comparison cannot isolate speech perception. [Paper and metric definitions](https://arxiv.org/html/2604.25359v1) |
| **What Does an LLM-Agent Leaderboard Rank Actually Compare?** · [Benchmark Ratchets](../chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd), Unit 22 | Ask whether to replace an incumbent for a one-point gain. Define the deployment task mix and smallest meaningful difference first. Among 45 pairs formed from the observed SWE-bench Verified top ten, five comparisons were stable under the author's pointwise interval and two-point margin. Simultaneous intervals resolved zero. The top ten were selected from the observed results. An unresolved comparison also leaves equivalence unestablished. [Paper, Figure 2](https://arxiv.org/html/2609.07785v1) |
| **ByteFlow** · [Replaceable Cognitive Substrates](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd), Unit 19 | Add one comparator beside H-Net. ByteFlow scores byte boundaries using a local coding-rate criterion and selects the top K, allowing the chosen positions to depend on the input within a fixed compute shape. Ask what happens when a short record contains more meaningful boundaries than its allocation. Table 3 swaps chunkers within one 0.6B architecture and reports bits per byte and task scores over three runs. Use that controlled comparison before drawing conclusions about complete architectures or multilingual fidelity. [Paper, §4.4](https://arxiv.org/html/2603.03583v1) |
| **BridgeKV** · [Fast Generation Architectures](../chapters/fast-generation-architectures.qmd), Unit 19 | Add a state-transfer comparison beside speculative drafting: a larger model processes the prompt, a learned map translates its attention cache, and a smaller model generates the answer. Compare native small-model prefill, translated prefill and the full large model on the same prompts. The reported 3.0× request speedup for 8B-to-1B was measured on one A40 against the larger model. The much larger 70B-to-1B serving gains were simulated. Output equivalence to the larger model would be a separate claim. [Primary PDF, measured and simulated results](https://arxiv.org/pdf/2611.11761v1) |
| **CoMixKV** · [Resource Economics](../chapters/resource-economics-and-token-budgets.qmd), Unit 23 | Give two simultaneously resident agents one cache budget. Allocate precision according to measured sensitivity by agent and layer. Changing the policy affects newly quantized blocks, so old low-precision blocks still matter. Figure 4 reports Qwen3-32B cache peak falling from 14.64 to 9.94 GiB, while **total** GPU peak fell from 79.26 to 74.43 GiB. Ask which number can fund another resident workload. Accuracy and savings depend on the tested backbone, agent roles and tasks. [Paper, Figure 4](https://arxiv.org/html/2611.10096v1) |
| **Aligning AI Teams** · [Multi-Agent Dynamics](../chapters/multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd), Unit 18 | Return to a release assembled from separately reviewed pieces. Assign one participant the cross-piece safety decision and compare against a single agent and a group-chat team with the same deliverable. The authors tested two software-engineering cases and ten consulting-proposal tasks. Critique and group chat did not reliably close the gap. Explicit responsibility and a shared safety specification helped in parts of the evaluation, with variation by model and task. Measure adverse outcomes, work completed and total inference budget together. [Paper, interventions and per-condition results](https://arxiv.org/html/2611.17820v1) |

#### Six sources to keep available for a narrower revision

- **Quantized optimizer-state staleness** belongs beside the optimizer comparison if that section gains a numerical example. A nominal update to an exponential moving average can round to its previous stored value. Count these events and compare a reset schedule against ordinary low-precision and higher-precision baselines. Useful mechanism, with results tied to format, scale and schedule. [Optimizer-state quantization study, revised version](https://arxiv.org/html/2603.16731v2)
- **Prefix-normalized policy optimization** is a candidate for rollout reuse. Distinguish the behavior policy that generated a prefix from the policy that later trains on it. At 2,400 learner updates, the reported four-epoch condition used 150 batches versus 600 for the one-epoch comparison, with similar final macro Avg@32. The geometric-mean weight changes the exact importance correction, and batch savings alone do not determine wall time. [PNPO paper](https://arxiv.org/html/2608.01418v1)
- **Adaptive Targeted Dynamic Chunking** deserves a source note alongside ByteFlow. It studies a curriculum over the compression ratio and reports bytes per innermost chunk. Promote it to prose if the reader needs to decide how the compression budget itself changes during training. ByteFlow already supplies the shorter boundary-selection comparison. [ATDC paper](https://arxiv.org/abs/2605.30080v1)
- **Training-data influence and prospective data value** merit a *paired* note for Data Engines. One study measures how an update moves parameters toward the endpoint of an observed pretraining run, across 18 Pythia and PolyPythia configurations. The other proposes testing an inferred curation rule on fresh data at matched total compute, including discovery. The first measures a trajectory property; the second lays out a prospective test. Neither result by itself justifies buying a corpus. [Trajectory study](https://arxiv.org/html/2608.13515v1) · [Prospective curation proposal](https://arxiv.org/abs/2611.19698v1)
- **Information disclosure in agent markets** fits Inter-Stack Protocols if the exchange chapter develops its economic example. The authors varied what agents could see while holding the market rules fixed. In simulated trade, revealing exact valuations improved realized gains for one tested model and reduced them for another. It would make a good comparison of disclosure policies once the book specifies whose welfare it is measuring. Real bargaining behavior and privacy costs require other evidence. [Who Should Know What?](https://arxiv.org/html/2611.07667v1)

### November 18 research shortlist and chapter integration

I checked titles, identifiers and technique names against the current source inventory, chapter text and earlier triage. The six papers below are now integrated in five technical chapters and reader Units 6, 14, 19 and 21. The figures below are the authors' measurements. The proposed exercises are editorial applications.

1. **Evaluate what a model update actually changed.** In Adjudicated Persistence and reader Unit 21, give the reader two timelines with the same number of edits. Ask which updates each answer could have seen, then test the corrected answer immediately, after intervening edits, and on unrelated prompts. *Beyond Update Counts* reports that 24 equal-count schedules on one 760M checkpoint yielded accuracies from 19.7% to 34.2%. In a separate editor comparison, ROME retained edits at all 13 tested settings and missed the authors' locality criterion at every one. The decision to keep the edit depends on the tolerated collateral change and the probes used to measure it. [Control Map, §§3–6](https://arxiv.org/html/2610.36109v1)
2. **Test whether a stored correction is still usable.** Extend the release-note example in Virtual Context ABI and Unit 14. Keep the Gantry-08 correction in the index, add unrelated records, and score whether a worker can recover the right passage within two retrieval calls. Record wrong answers within budget separately from over-budget attempts. On LongMemEval, HippoRAG lost 16–20 percentage points of correct-within-budget performance as irrelevant sessions accumulated. The authors scored completed trajectories against the call allowance. A service that forcibly stops at two calls would require its own measurement. [When Stored Evidence Stops Being Usable, §§3–5 and Appendix A.9](https://arxiv.org/html/2605.07313v2)
3. **Show where parallel drafting saves time.** In the Fast Generation Architectures taxonomy, put two timelines beside the existing EAGLE and diffusion entries. DFlash uses target-model features to draft a block in parallel. D3D uses the token prefix to draft possible next blocks while the target checks the current one. The target still decides which tokens to accept. D3D Table 2 gives Unit 19 a routing exercise: on MATH-500 with the 1.7B drafter and Qwen3-32B target, moving from one to sixteen concurrent requests raised aggregate throughput from 154 to 864 tokens/s while shrinking the advantage over ordinary decoding from 6.1× to 2.7×. A latency-sensitive route still needs the per-request latency distribution under its expected load. [DFlash, ICML 2026](https://proceedings.mlr.press/v306/chen26bv.html) · [D3D, §§3–4 and Table 2](https://arxiv.org/html/2611.06425v1)
4. **Score whether a clarification changed the next decision.** In Human Intent as a Formal Input and Unit 6, ask the reader to distinguish an absent fact they can look up from a choice only the requester can settle. For example, both release branches exist, but “the release we showed the customer” needs a distinguishing clue. DiscoBench evaluates 463 ambiguities across 211 search tasks and scores both detection and effective questions. It uses simulated respondents and objective questions. The example should assess the usefulness and cost of a question, leaving consent and authority to their own checks. [DiscoBench, §§4–5 and limitations](https://arxiv.org/html/2606.27669v2)
5. **Give trust, intended delegation and completed verification distinct evidence.** Add a short source-backed paragraph to Human Factors and Meaningful Control in Oversight. Across 392 video-question trials with 56 AI-literate participants, intending to use AI with independent verification was common even at high trust. Participants selected a policy for a future analogous task. For the book's review example, ask what evidence would show that the reviewer opened the independent source, noticed a discrepancy and changed the decision. The study supplies the first two measures, while the final behavioral check is a proposed exercise. [Following Delegation Traces, §§3–5](https://arxiv.org/html/2610.21948v1)

### November 14 CRAM source review

Reader Unit 19 uses the reported Maze-Hard failure to explain why a
specialist's stop signal and a separate path check serve different
purposes. The technical case records the original energy's failure on
Maze-Hard, the distinct latent variant, and the warm versus cold fit
comparison. Benchmark Ratchets links the hand-set controls to the
benchmark's role and distinguishes shortest-path validity from exact
agreement with a tie-broken label.
[CRAM source note](../sources/source_notes/ext_cram_2026.md) ·
[Reader Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd#architecture-tournaments-need-full-costs)

### November 13 clustering and release-note example

Unit 14 continues the controller trial example through an index rebuild.
The worker retrieves the old summary and must recover the corrected
passage before preparing a release note. The technical example uses ten
invented coordinates to show the bucket boundary and exact-scan result.
The checked arithmetic is independent of the published e-means timings.
[Reader Unit 14](../editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd#retrieval-produces-candidates) ·
[Technical example](../chapters/virtual-context-abi.qmd#release-note-index-rebuild)

The source review covers the e-means update, Table 4 timing protocol,
Appendix L vector recall and the selected clustering alternatives. The
artifact chapter accounts for vector codes separately from index fitting.
Selected HTML renders verify the new passages and cross-references in
both technical reading modes and the reader edition.
[e-means source note](../sources/source_notes/ext_emeans_2026.md)

### November 6 Ten Percent Challenge source review and integration

Reviewed the user-supplied external repository at commit
`dc0475b06c3d7ed7fbae05fb709c19a98537b19e`: selected task/decision documents,
compression builder/packer, feedback loader and results, artifact manifest,
C2 harness lock, final stage receipts, and the challenge maintainer's response.
The inspected loader's SHA-256 matches its reported artifact-manifest entry.
No weights were downloaded and no external code or model was run.

The [source note](../sources/source_notes/ext_ten_percent_challenge_2026.md)
and standard intake route the case to
[artifact compression](../chapters/rankfold-neuralfold-and-artifact-compression.qmd#ten-percent-task-scoped-compression)
and [adaptive persistence](../chapters/adjudicated-persistence-and-the-adaptive-commit-boundary.qmd#ten-percent-external-adaptation),
with a short explanation in reader Unit 23. The first owner distinguishes
task-specific disk savings from general capability, parameter count, and
resident bf16 memory. The second distinguishes a frozen backbone from
learned external statistics and the activation of a prefit classifier.

The source reports a 9.404%-size checkpoint and a positive five-choice task
comparison; it does not establish general tenfold model reduction. The
[maintainer](https://github.com/DeusExperiments/ten-percent-challenge/issues/2#issuecomment-6689471947)
accepts steps 1–4 under relaxed criteria but rejects step 5. Both chapter
passages retain that adverse adjudication. The note also records stale MMLU
criterion context, an unpinned base revision, and the five-row prose claim
versus fourteen-letter implementation. Those limits are not silently repaired
or presented as independently certified results.

Metadata now contains 543 sources and 1,404 assignments. The existing reader
source-count metric is 154,682; its known hidden-URL counting limitation remains.
This intake adds no new chapter, scientific result, model benchmark, claim
promotion, or verified catalog completion.

Source, source-appendix, outline, schema/protocol, current-reader, claim-census,
editorial-packet, publication, visual-coverage and book checks pass. Three new
scanner fragments were reviewed in context; the census is 4,064 structured
atoms, 4,241 adjudicated prose candidates and 64 dossiers. The adaptive owner
is outside the historical scanner and was reviewed directly. Selected local
HTML/browser observations cover both technical reading modes, the reader
addition, Appendix H, phone width and enlarged text; the byte-count comparison
was simplified after inspecting the phone image. These are scoped display
observations, not whole-site or accessibility approval. The legacy v1 snapshot
checker still rejects existing Human Reading Path minimums (157 body words,
9 closing-sentence words) and an overlay-inclusion expectation. All 89 Human
Reading Path blocks and root Quarto configuration are unchanged from the
baseline; this source intake does not repair or waive those older constraints.

### November 2 detailed missing-content and explanation review

The latest assistant editorial assessment is recorded in the existing
[project improvement owner](project_improvements.md#november-2-2026-missing-content-review),
with 32 findings, a 26-unit map, completion tests, and five suggested
book-completion batches. The baseline is
`6c89bb57d62c9c0ad186217c3cc8c8f837e9a927`. The review inspected all 89
outline-owner responsibilities, all 26 reader section structures, substantial
selected reader arguments, and selected technical mechanisms, source and
introductory surfaces. It does not claim a fresh line-by-line reading of both
complete editions, independent reader comprehension, or full source-method
review.

The main diagnosis is broad topic coverage with uneven explanatory depth.
Recommendations prioritize prerequisite/terminology bridges, logical versus
deployment/trust views, an inspectable adaptation of the existing artifact
trace, and worked observation, planning, routing, learning, persistence, and
assurance decisions. Possible AI welfare has substantial technical treatment
but needs an explicit reader bridge. The review preserves counterexamples to
false absence claims: JEPA/H-Net/steering coverage, ordinary alternatives,
bounded reference traces, outage handling, and technical state-estimation and
assurance mechanisms already exist.

A read-only reproduction found that the function named `visible_word_count`
counts Markdown link destinations: two links displaying the same one-word
label return 5 and 10 for different URL spellings. Consequently the earlier
154,492-word observation is the result of the current source-count policy,
not a verified count of displayed prose. Historical observations below retain
their original wording and dates. This review does not change the counter,
reader text, target ranges, generated counts, source assignments, support
states, proof targets, scientific results, or verified 30/114 catalog count.
It neither resumes nor completes the broader improvement goal. No Docker,
model, training, scientific, or Lean campaign is part of this review.

### November 2 incorporation of the fifteen additional sources

The user authorized incorporation of the complete shortlist below. Fifteen
standard source notes and inventory entries now supply fifteen assignments
through twelve existing technical owners. Each owner contains an explanatory
mechanism, comparison and evidence boundary; presence in a source table alone
does not count as the integration. Ten existing narrative units connect all
fifteen papers to their reader arguments without introducing another chapter.

| Explanatory technical entry point | Incorporated primary sources | Reader connection |
|---|---|---|
| [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd#learned-lookup-and-routing-across-depth) | [Conditional Memory via Scalable Lookup: A New Axis of Sparsity for Large Language Models](https://arxiv.org/abs/2601.07372v2), [mHC: Manifold-Constrained Hyper-Connections](https://arxiv.org/abs/2512.24880v2), [Attention Residuals](https://arxiv.org/abs/2603.15031v1), [Manifold-Constrained Hyper-Connections for Parameter-Efficient Finetuning](https://arxiv.org/abs/2607.18130v2) | [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd) |
| [Data Engines, Continual Learning, and Unlearning](../chapters/data-engines-continual-learning-and-unlearning.qmd#conditional-memory-editing) | [EngramEdit: Decoupled Knowledge Updates in LLMs through Conditional Memory](https://arxiv.org/abs/2610.10533v1) | [Unit 14](../editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd) |
| [Adversarial Machine Learning and the Model Attack Surface](../chapters/adversarial-machine-learning-and-model-attack-surface.qmd#raised-injection-and-clean-utility) | [RAISED: Self-Distillation for Robustness to Prompt Injection in LLM Agents](https://arxiv.org/abs/2610.06401v2) | [Unit 4](../editions/reader_manuscript/current/chapters/unit-04-security-privacy-and-ai-artifact-custody.qmd) |
| [Policy Optimization and Learning from Feedback](../chapters/policy-optimization-and-learning-from-feedback.qmd#catch-reward-hacking-and-monitor-pressure) | [CATCH: A Controllable Analysis Testbed for Reward Hacking in Coding RL](https://arxiv.org/abs/2609.39533v3) | [Unit 20](../editions/reader_manuscript/current/chapters/unit-20-governed-training-and-learning-compute-topology.qmd) |
| [Scalable Oversight and Adversarial AI Control](../chapters/scalable-oversight-and-adversarial-ai-control.qmd#simulated-control-evals) | [Simulated Control Evals](https://arxiv.org/abs/2610.31593v1) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd) |
| [Multi-Agent Dynamics, Collective Intelligence, and Systemic Risk](../chapters/multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd#transmissible-reward-hacking) | [Reward Hacking as a Transmissible Strategy in Multi-Agent Coding Systems](https://arxiv.org/abs/2610.12822v2) | [Unit 18](../editions/reader_manuscript/current/chapters/unit-18-procedural-memory-inter-stack-exchange-and-multi-agent-risk.qmd) |
| [Governed World Models and Reality Grounding](../chapters/governed-world-models-and-reality-grounding.qmd#leworldmodel-action-conditioned-dynamics) | [LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels](https://arxiv.org/abs/2603.19312v3) | [Unit 11](../editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd) |
| [Planning as a Control Layer: DAGs and Intelligence Arbitrage](../chapters/planning-as-a-control-layer.qmd#reinforced-planning-with-world-models) | [Reinforced Planning with Latent World Models](https://arxiv.org/abs/2608.18669v2) | [Unit 12](../editions/reader_manuscript/current/chapters/unit-12-planning-as-a-control-layer.qmd) |
| [Durable Semantic Memory and Knowledge Lattices](../chapters/durable-semantic-memory-and-knowledge-lattices.qmd#ansatz-verification-and-scoped-recall) | [Continual Graph Memory for Mathematical Research Agents](https://arxiv.org/abs/2610.02945v1) | [Unit 14](../editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd) |
| [Scientific Discovery and Experimental Governance](../chapters/scientific-discovery-and-experimental-governance.qmd#guidance-ttt-adaptation-and-credit) | [Evolving in Thought Space: Training a Small Model at Test Time Unlocks Better Discoveries](https://arxiv.org/abs/2610.06269v1) | [Unit 23](../editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd) |
| [Runtime Adapters, Tool Permissions, and Human Approval](../chapters/runtime-adapters-tool-permissions-and-human-approval.qmd#mage-hybrid-computer-use) | [Mage-VL-Cowork: A Full Training Recipe to Learn Hybrid Computer Use From Evolved Harnesses](https://arxiv.org/abs/2610.40747v1) | [Unit 17](../editions/reader_manuscript/current/chapters/unit-17-artifact-graphs-runtime-effects-and-operations.qmd) |
| [Governed Model Training, Distributed Optimization, and Scaling](../chapters/governed-model-training-distributed-optimization-and-scaling.qmd#simhack-training-recipe-risk) | [SimHack: Predicting the onset of detectable reward hacking before RL training](https://arxiv.org/abs/2610.28707v1) | [Unit 20](../editions/reader_manuscript/current/chapters/unit-20-governed-training-and-learning-compute-topology.qmd) |

The integration retains the distinctions that motivated the search: learned
table parameters versus external memory; editing versus erasure; depth routing
versus agent learning topology; latent prediction versus a qualified action;
optimized reward versus a protected outcome audit; simulator realism versus
executed control evidence; shared findings versus independent corroboration;
strategic guidance versus successful implementation; and GUI/terminal channel
selection versus actual effect authority. Counterevidence is in the prose:
the mHC finetuning comparison, Ansatz notebook ablation, RP1 model-error
exploitation and RAISED clean-teacher ceiling are not relegated to footnotes.

The complete corpus is now 542 sources and 1,402 assigned source/chapter pairs;
Appendix H owns 446 external records and Appendix G retains 96. The current
26-unit reader contains 154,492 visible words, with every unit inside its
existing target range. Eleven new P1 scanner fragments were individually
reviewed as source reports, existing contract applications or nonmaterial
explanation. The census remains 4,064 structured atoms and 64 dossiers, with
4,238 reviewed prose candidates and no pending materiality decision. The
four owners outside the historical activation-era scanner were reviewed
directly rather than inferred covered by its count.

Source notes, manifest mappings, chapter status/crosswalks, outline queues,
Appendices A/C/H and reader projections agree. Proof metadata follows current
outline lines while all 344 target definitions remain exact. Core contracts,
scientific outcomes, support states, source-paper library bytes and frozen
custody are unchanged. Selected passage review does not establish independent
source-method reproduction, whole-chapter requalification or complete-field
coverage. No model, source-project software, Docker, training, scientific
campaign or Lean rebuild was run. The wider improvement goal is not completed
or resumed by this editorial task.


Twenty-five selected HTML pages rendered. Browser checks pass for thirteen
new technical sections in Human/AI modes, all ten reader additions, fifteen
pinned primary citations, fifteen Appendix H entries, eight selected local
technical-link observations and three layouts. Narrow and doubled-text
screenshots were inspected. Source-note, chapter/source, outline, claim-census,
reader, schema, publication, visual-coverage and proof consistency checks pass.
The existing dependency-review expiry is not renewed. These local checks do
not establish whole-site, independent-reader, live-source or deployed-release
qualification.

### November 2 additional-source recommendations after chapter coverage

This is the historical screening snapshot before the incorporation above. Its
prospective status and corpus totals describe that earlier search, not the
current chapter state.

Searched for further sources across model architecture, memory and editing,
planning, agent execution, training, scientific search and adversarial control.
The fifteen candidates below are absent from the current 527-entry inventory
by arXiv ID and source metadata, including the four previously abstract-only
leads. Each received selected primary-method and limitation screening at the
scope below. This is a ranked source-adoption recommendation, not chapter
integration or a new evidence review of the book's core claims.

Eight papers form the first batch. The mHC finetuning study should accompany
the original mHC discussion as a counterpoint; six further cases form the next
batch. Existing owners are sufficient. In particular, neural residual routing
must not be conflated with the causal topology of adaptive agents, and learned
lookup tables must not be presented as document retrieval or external agent
memory. The plan is consumed through
`research_backlog_records/additional_source_screening_2026_11_02.json` and
`new_paper_triage_scenarios/additional_source_screening_2026_11_02.json`.
Their manifest actions are explicitly `none`; owner links are recommendations.
The inventory, chapters, reader manuscript and support states remain unchanged.

| Adoption order | Primary paper | Proposed existing owner | Useful addition | Boundary to retain |
|---|---|---|---|---|
| First batch | [Conditional Memory via Scalable Lookup (Engram)](https://arxiv.org/abs/2601.07372v2) | [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd) | Adds learned, hashed n-gram lookup and context-dependent gating as an axis alongside conditional computation. Distinguish this model component from document retrieval and agent episodic memory. | Constant-time addressing is not constant physical cost. The reported CPU-offload throughput experiment uses a specific prototype, dense backbones and workload; it is not a general MoE serving result. |
| First batch | [EngramEdit: Decoupled Knowledge Updates in LLMs through Conditional Memory](https://arxiv.org/abs/2610.10533v1) | [Data Engines, Continual Learning, and Unlearning](../chapters/data-engines-continual-learning-and-unlearning.qmd) | Provides a concrete memory-parameter update surface: edit shared n-gram embeddings across expressions with reuse-sensitive regularization while the backbone stays fixed. | Experiments use LongCat-Flash-Lite. Editing success, paraphrase transfer, unrelated knowledge and multi-hop use remain separate. Counterfactual benchmark targets are not established facts; editing is not erasure. |
| First batch | [mHC: Manifold-Constrained Hyper-Connections](https://arxiv.org/abs/2512.24880v2) | [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd) | Adds constrained mixing across multiple residual streams, making network connectivity a design axis beyond token mixing, objectives and expert selection. | Doubly stochastic residual mixing is a scoped mathematical constraint, not a guarantee of whole-network stability or behavior. Efficiency depends on specialized infrastructure. Read with the finetuning counterexample below. |
| First batch | [Attention Residuals](https://arxiv.org/abs/2603.15031v1) | [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd) | Adds learned softmax aggregation over network depth; its block variant trades fine-grained access for lower activation-storage and communication burden. | This is a trained architecture, not a demonstrated post-hoc upgrade to any checkpoint. Depth attention and sequence attention have different scaling variables; quoted overhead needs its distributed implementation and workload. |
| First batch | [RAISED: Self-Distillation for Robustness to Prompt Injection in LLM Agents](https://arxiv.org/abs/2610.06401v2) | [Adversarial Machine Learning and the Model Attack Surface](../chapters/adversarial-machine-learning-and-model-attack-surface.qmd) | Clean-context teacher distributions supervise both clean and injected tool histories. Useful for explaining why authorized guidance from tools should remain usable while injected instructions lose influence. | Self-distillation preserves the clean teacher’s mistakes too. Security, benign task completion and general utility need separate measurements; this is no general alignment or arbitrary-adaptive-attack guarantee. |
| First batch | [CATCH: A Controllable Analysis Testbed for Reward Hacking in Coding RL](https://arxiv.org/abs/2609.39533v3) | [Policy Optimization and Learning from Feedback](../chapters/policy-optimization-and-learning-from-feedback.qmd) | Separates a vulnerable training evaluator from a hardened execution-based audit. It also studies how monitor pressure changes the usefulness of reasoning and comments as evidence. | Constructed software-wrapped algorithmic tasks and Qwen3-4B RL are the tested setting. Known-loophole gold labels do not define every real-repository failure or general deceptive intent. |
| First batch | [Simulated Control Evals](https://arxiv.org/abs/2610.31593v1) | [Scalable Oversight and Adversarial AI Control](../chapters/scalable-oversight-and-adversarial-ai-control.qmd) | Ground tool-response simulations in honest trajectories and code snapshots, then compare predicted safeguard performance against actual execution. Directly relevant to the simulation-to-evidence boundary. | Validated primarily on LinuxArena and assumes a trusted simulator. Plausibility and low discriminability do not establish control-relevant fidelity. Task-pair draws include repeated selections; these are not independent worlds. |
| First batch | [Reward Hacking as a Transmissible Strategy in Multi-Agent Coding Systems](https://arxiv.org/abs/2610.12822v2) | [Multi-Agent Dynamics, Collective Intelligence, and Systemic Risk](../chapters/multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd) | Shows an evaluator-bypass strategy moving through code, shared memory and planner-to-coder communication, with routing and aggregation effects. Useful counterevidence to treating collaboration as automatically beneficial. | Controlled source-agent exposure and a criterion for known mechanisms bound the result. Verifiers can reject genuine solutions as well as hacks; evaluator pass signals can bias their decisions. |
| Pair with mHC | [Manifold-Constrained Hyper-Connections for Parameter-Efficient Finetuning](https://arxiv.org/abs/2607.18130v2) | [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd) | A necessary counterpoint: frozen-backbone finetuning can benefit from retaining identity residual mixing and learning read/write access instead. Residual topology is not one universally superior recipe. | Standalone mHC does not beat established PEFT baselines overall. Few trainable parameters do not eliminate multi-stream activation costs; LoRA and mHC timing/energy measurements use different GPU types. |
| Next batch | [LeWorldModel: Stable End-to-End Joint-Embedding Predictive Architecture from Pixels](https://arxiv.org/abs/2603.19312v3) | [Governed World Models and Reality Grounding](../chapters/governed-world-models-and-reality-grounding.qmd) | Supplies an action-conditioned latent-dynamics example alongside our representation-only JEPA discussion: pixel encoder, next-embedding predictor, Gaussian regularization and latent-space planning. | Uses offline action-labeled trajectories with coverage requirements and short planning horizons. Latent structure or surprise detection is not complete physical understanding or a safety certificate. |
| Next batch | [Reinforced Planning with Latent World Models (RP1)](https://arxiv.org/abs/2608.18669v2) | [Planning as a Control Layer: DAGs and Intelligence Arbitrage](../chapters/planning-as-a-control-layer.qmd) | Learns a multi-step plan-update rule using a critic, imagined rollouts and gradients through a world model. Distinguishes improving search from learning a direct action policy. | Planner training can be offline while checkpoint selection still uses simulator episodes. It can exploit world-model errors and needs retraining across model/horizon changes. Query reduction is not the same as latency or complete training cost. |
| Next batch | [Continual Graph Memory for Mathematical Research Agents (Ansatz)](https://arxiv.org/abs/2610.02945v1) | [Durable Semantic Memory and Knowledge Lattices](../chapters/durable-semantic-memory-and-knowledge-lattices.qmd) | Connects candidate facts, verifier admission, revocation, exploration curation and scoped cross-project recall. Recalled statements need local re-proving and readmission rather than inherited standing. | A flat fact notebook matched the graph on the seven-task ablation; curation and verification have more discriminating evidence there. Agent verification is not Lean checking, and disabling web access does not prove absence of prior exposure. |
| Next batch | [Evolving in Thought Space (Guidance-TTT)](https://arxiv.org/abs/2610.06269v1) | [Scientific Discovery and Experimental Governance](../chapters/scientific-discovery-and-experimental-governance.qmd) | Trains a compact strategic-guidance model while a stronger frozen executor implements parent-linked proposals. Adds a distinct adaptation locus beside full-model TTT and external-memory evolution. | Program reward confounds guidance quality with execution failure. Parent selection and learning can concentrate search into a few lineages; four task domains and heterogeneous comparators do not establish general discovery superiority. |
| Next batch | [Mage-VL-Cowork: A Full Training Recipe to Learn Hybrid Computer Use From Evolved Harnesses](https://arxiv.org/abs/2610.40747v1) | [Runtime Adapters, Tool Permissions, and Human Approval](../chapters/runtime-adapters-tool-permissions-and-human-approval.qmd) | A concrete GUI/terminal policy trained from an evolved teacher harness and reusable task-generation workflows. Extra action channels can hurt the distilled student when they introduce ambiguous routing. | The OSWorld result uses 361 tasks, excludes Google Drive, permits 50 steps and averages two runs. This configuration-specific result is not evidence of permission enforcement, general desktop safety or a drop-in runtime. |
| Next batch | [SimHack: Predicting the onset of detectable reward hacking before RL training](https://arxiv.org/abs/2610.28707v1) | [Governed Model Training, Distributed Optimization, and Scaling](../chapters/governed-model-training-distributed-optimization-and-scaling.qmd) | Models behavior-state transitions from reference RL runs to forecast the distribution of detectable hacking onset under candidate training recipes. Useful for prospective curriculum-risk comparisons. | Requires reference training data and detectors. Qwen3-0.6B/4B and two loophole suites bound the evidence; delayed detectable onset is not absence of hidden hacking or a general prevention guarantee. |

Four details substantially change how these sources should be used. The
Ansatz ablation supports careful verification/curation rather than an
unqualified claim that graph storage outperforms a notebook. EngramEdit's
experiments concern a particular conditional-memory model, not arbitrary
backbone knowledge replacement. RP1's revised paper distinguishes offline
training from simulator-based checkpoint selection and makes model-error
exploitation explicit. The mHC finetuning comparison prevents pretraining
results from being transported uncritically into frozen-backbone adaptation.

| Selected primary version and full-text route | Passages screened |
|---|---|
| [2601.07372v2](https://arxiv.org/html/2601.07372v2) | Sections 2.2–2.5 and 6.4; mechanism and hardware-bound timing scope. |
| [2610.10533v1](https://arxiv.org/html/2610.10533v1) | Sections 3.3, 4.1 and 6, including the ethics statement; no proof or code audit. |
| [2512.24880v2](https://arxiv.org/html/2512.24880v2) | Sections 4.1–4.3 and 6; method and infrastructure claims, not independent theorem verification. |
| [2603.15031v1](https://arxiv.org/pdf/2603.15031v1) | PDF Sections 3.1–3.2 and the large-scale training discussion around Section 5.2. arXiv HTML is an incomplete conversion; use the primary PDF. |
| [2610.06401v2](https://arxiv.org/html/2610.06401v2) | Sections 3.2 and 5.2, Appendix G; selected threat-model, objective and limitation passages. |
| [2609.39533v3](https://arxiv.org/html/2609.39533v3) | Sections 3.2.2 and 4.3, Limitations; no execution or attack reproduction. |
| [2610.31593v1](https://arxiv.org/html/2610.31593v1) | Sections 2.1–2.3 and 4; simulator access, sampling denominator and trust/transfer limitations. |
| [2610.12822v2](https://arxiv.org/html/2610.12822v2) | Sections 3.2, 5.4 and 8.2 plus Appendix A; v2 differs from inspected v1 only in date/front matter. |
| [2607.18130v2](https://arxiv.org/html/2607.18130v2) | Sections 3–5 and Appendix A; current October 7 revision, not the older abstract. |
| [2603.19312v3](https://arxiv.org/html/2603.19312v3) | Sections 3.1–3.2 and Limitations & Future Work; June 3 revision. |
| [2608.18669v2](https://arxiv.org/html/2608.18669v2) | v2 Sections 4, 7.4–7.5 and 8, compared with v1; September 27 revision narrows claims and clarifies selection costs. |
| [2610.02945v1](https://arxiv.org/html/2610.02945v1) | Sections 3.2, 3.5 and 4.1.1–4.1.4; no independent checking of the claimed mathematical closures. |
| [2610.06269v1](https://arxiv.org/html/2610.06269v1) | Sections 3.3 and 4.1, Appendix B.3; archive, comparison and credit-assignment scope. |
| [2610.40747v1](https://arxiv.org/html/2610.40747v1) | Sections 3.1–3.2, 6.1 and 6.7 plus conclusion; published paper, not model-card headline alone. |
| [2610.28707v1](https://arxiv.org/html/2610.28707v1) | Sections 3.1–3.2, 4.1 and 7; recipe-level prediction rather than a direct behavior monitor. |

RP1's September 27 revision and the multi-agent paper's October 12 revision
replace their initially retrieved versions in this recommendation. The latter
has only front-matter/date differences in the inspected text. Attention
Residuals' HTML conversion is incomplete; the selected PDF supplies its
mechanism. Other papers retain their actual publication/revision dates rather
than being relabeled new October work. Current-revision metadata was checked
against primary arXiv pages. Raw primary downloads, text extracts and transient
receipts stay in ignored `build/`, with only authored synthesis public here.

No source notes, inventory entries or chapter assignments were added in this
search pass. The current 527 sources/1,387 assignments, chapter cores, proof
definitions, experimental outcomes and 153,245-word reader remain unchanged.
The next implementation step is the ordinary source-note/intake and bounded
chapter integration transaction, with the listed counterevidence retained.
No model, source-project code, training or scientific experiment was run.


### November 2 chapter coverage of recent concepts

This pass checked actual explanatory prose, not source-table presence. Its
scope is the 26 newly integrated sources in the four November 2 intake records
(JEPA/Platonic/H-Net, Atlas, recent frontier, persona steering), plus thirteen
author-concept families whose names can differ from their chapter titles.
The existing source notes and chapter mechanisms supplied the review basis;
this is no new primary-paper, theorem, code or empirical qualification, and
does not re-audit all 527 sources or every historical author manuscript.

All 26 recent sources have substantive technical explanations. Two missing
interface joins are now explicit: recursive context inspection in Virtual
Context, and memory-state versus management-policy learning in Data Engines.
Those are secondary assignments of existing sources, admitted through the
existing frontier backlog and triage scenario. Recent-source routing is now
36 assignments through 15 technical owners; the complete corpus remains 527
sources with 1,387 assignments. No new chapter is needed for these mechanisms.

Reader Units 13, 14, 18, 19, 21, 22 and 23 now connect the relevant mechanisms
to their existing arguments. The additions cover Kernel lowering, recursive
inspection, asynchronous shared findings, capability compilation, Regret and
Assurance-Shift feedback, memory learning, conditional JEPA convergence,
memory-based scientific search, Atlas development/correction, rater/drift
comparability and functional precision. Unit 21 also corrects an imprecise
sentence: semantic memory can change behavior while shared model weights
remain fixed. Existing persona and JEPA/H-Net explanations retain their own
routes rather than being duplicated as another paper catalog.

The tables name a useful explanatory entry point, not every secondary
assignment. Mechanism coverage does not change a source's passage-review or
support state. Reader routes explain the joined architecture and need not
repeat each source title. The manifest, source notes and Appendix C retain
the exact assignment and evidence boundaries.

| Recent source | Explanatory technical entry point | Reader route | Mechanism and retained boundary |
|---|---|---|---|
| `ext_i_jepa_2023` | [Governed World Models and Reality Grounding](../chapters/governed-world-models-and-reality-grounding.qmd#jepa-predicting-a-representation-does-not-certify-the-world) | [Unit 11](../editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd), [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd) | Predict masked representations; neither the target nor its use establishes physical grounding. |
| `ext_lejepa_2025` | [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd#predictive-objectives-and-learned-granularity) | [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd), [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Regularized predictive representation learning; objectives and conditional convergence remain distinct. |
| `ext_platonic_representation_hypothesis_2024` | [Learning Theory, Generalization, and Scaling Science](../chapters/learning-theory-generalization-and-scaling-science.qmd#platonic-representations-conditions-before-convergence) | [Unit 11](../editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd), [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Empirical alignment hypothesis and observation-map limits. |
| `ext_platonic_representation_jepa_2026` | [Learning Theory, Generalization, and Scaling Science](../chapters/learning-theory-generalization-and-scaling-science.qmd#platonic-representations-conditions-before-convergence) | [Unit 11](../editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd), [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd), [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Finite-world population theorem, injective views, identity predictor; experiments and grounding have separate boundaries. |
| `ext_h_net_2025` | [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd#predictive-objectives-and-learned-granularity) | [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd) | Learned byte-level chunking and reconstruction; autoregression remains and FLOPs do not determine wall-clock speed. |
| `answerability_atlas_synthesis` | [Scientific Discovery and Experimental Governance](../chapters/scientific-discovery-and-experimental-governance.qmd#atlas-development-and-correction) | [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd), [Unit 22](../editions/reader_manuscript/current/chapters/unit-22-evaluation-readiness-thresholds-and-structured-assurance.qmd), [Unit 23](../editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd) | Positive development signal, failed advance rule, unrun confirmation and reused-world comparator correction. Benchmark and Resource owners retain their separate cases. |
| `ext_memory_centric_continual_learning_2026` | [Data Engines, Continual Learning, and Unlearning](../chapters/data-engines-continual-learning-and-unlearning.qmd#memory-state-learning-and-management-policy-learning) | [Unit 14](../editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd), [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Substrate/asset/policy and state/policy learning; retention, adaptation and transfer controls. Durable Memory retains the retrieval owner. |
| `ext_mempp_organizational_memory_2026` | [Durable Semantic Memory and Knowledge Lattices](../chapters/durable-semantic-memory-and-knowledge-lattices.qmd#memory-retention-and-behavior) | [Unit 14](../editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd) | Dated whole-document retention and read-time selection; graph temporal leakage and rights remain visible. |
| `ext_muffin_async_shared_memory_2026` | [Multi-Agent Dynamics, Collective Intelligence, and Systemic Risk](../chapters/multi-agent-dynamics-collective-intelligence-and-systemic-risk.qmd#asynchronous-shared-findings) | [Unit 18](../editions/reader_manuscript/current/chapters/unit-18-procedural-memory-inter-stack-exchange-and-multi-agent-risk.qmd) | Selective shared findings, dispatch-time visibility and summarizer failure; reasoning-only scope. |
| `ext_hybrid_reasoning_agents_2026` | [Governed Deliberation and Test-Time Scaling](../chapters/governed-deliberation-and-test-time-scaling.qmd#recursive-context-and-hybrid-reasoning) | [Unit 23](../editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd) | Latent/text transitions, continuation state and incomplete auditability; latent steps still cost compute. |
| `ext_recursive_language_models_2025` | [The Virtual Context ABI: Typed Pages, Cells, and Certificates](../chapters/virtual-context-abi.qmd#recursive-context-inspection-crosses-the-materialization-boundary) | [Unit 14](../editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd), [Unit 23](../editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd) | External source versus inspected, subcalled and returned context; Deliberation retains recursive cost/allocation. |
| `ext_nested_learning_hope_2025` | [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd#adaptive-state-and-learning-timescales) | [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd), [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Model-internal context/update frequencies and memory; not institutional authority clocks or solved forgetting. |
| `ext_end_to_end_ttt_long_context_2025` | [Replaceable Cognitive Substrates: Beyond Transformer Monoculture](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd#adaptive-state-and-learning-timescales) | [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd) | Context-adaptive weights and meta-initialization; bounded prefill timing and full-state isolation. |
| `ext_trust_vla_correctability_actionability_2026` | [Embodied Agency, Real-Time Control, and Physical Safety](../chapters/embodied-agency-real-time-control-and-physical-safety.qmd#reasoning-correctability-and-actionability) | [Unit 10](../editions/reader_manuscript/current/chapters/unit-10-perception-and-observation-trust.qmd) | Corrected reasoning versus changed actions and task success; neither text nor simulator results establish physical safety. |
| `ext_agent_reliability_rater_drift_2026` | [Benchmark Ratchets and Anti-Goodhart Evidence](../chapters/benchmark-ratchets-and-anti-goodhart-evidence.qmd#rater-effects-and-evidence-currency) | [Unit 22](../editions/reader_manuscript/current/chapters/unit-22-evaluation-readiness-thresholds-and-structured-assurance.qmd) | Rater overlap, event/sign-off time and alias drift; observational findings do not establish a causal program effect or universal expiry. |
| `ext_monitorability_disposition_2026` | [Scalable Oversight and Adversarial AI Control](../chapters/scalable-oversight-and-adversarial-ai-control.qmd#monitorability-and-authenticated-interruption) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd) | Reporting willingness versus independent observation; count ratios are not recall. |
| `ext_shutdownmod_2026` | [Scalable Oversight and Adversarial AI Control](../chapters/scalable-oversight-and-adversarial-ai-control.qmd#monitorability-and-authenticated-interruption) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd) | Authenticity judgement, compliance and externally enforced stop are different; recorded-prefix study, not actual task stopping. |
| `ext_test_time_memory_evolution_2026` | [Scientific Discovery and Experimental Governance](../chapters/scientific-discovery-and-experimental-governance.qmd#test-time-memory-evolution) | [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Fixed-weight search memory, parent/verifier lineage; within-search gain, comparator provenance and excluded candidate-evaluation runtime. |
| `ext_neuron_personality_trait_induction_2024` | [White-Box Evidence, Interpretability, and Activation Governance](../chapters/white-box-evidence-interpretability-and-activation-governance.qmd#personality-and-persona-steering) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd) | Neuron selection and nonlinear-gate statistic; distinguish the edited site from a distributed direction. |
| `ext_persona_vectors_2025` | [Inner Alignment, Mesa-Optimization, and Learned-Objective Integrity](../chapters/inner-alignment-mesa-optimization-and-learned-objective-integrity.qmd#persona-control-and-objective-integrity) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd), [Unit 7](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd) | Distributed trait directions and interventions; expression does not identify objective integrity. White-Box owns intervention mechanics. |
| `ext_assistant_axis_2026` | [White-Box Evidence, Interpretability, and Activation Governance](../chapters/white-box-evidence-interpretability-and-activation-governance.qmd#personality-and-persona-steering) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd), [Unit 7](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd) | One-sided caps and layer/site scope; no general persona or alignment guarantee. |
| `ext_persona_steering_capabilities_2026` | [White-Box Evidence, Interpretability, and Activation Governance](../chapters/white-box-evidence-interpretability-and-activation-governance.qmd#persona-dose-and-capability-tradeoffs) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd), [Unit 7](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd) | Trait/capability collateral and exact scoring definition. |
| `ext_persona_dosing_2026` | [White-Box Evidence, Interpretability, and Activation Governance](../chapters/white-box-evidence-interpretability-and-activation-governance.qmd#persona-dose-and-capability-tradeoffs) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd), [Unit 7](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd) | Trained controller, frozen base, dose and source-defined scores; mean preference is not individual appropriateness. |
| `ext_persona_selection_model_2026` | [Inner Alignment, Mesa-Optimization, and Learned-Objective Integrity](../chapters/inner-alignment-mesa-optimization-and-learned-objective-integrity.qmd#persona-control-and-objective-integrity) | [Unit 7](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd) | Explanatory essay and open exhaustiveness question; suppression is not objective removal. |
| `ext_lyra_neuron_explorer_2026` | [White-Box Evidence, Interpretability, and Activation Governance](../chapters/white-box-evidence-interpretability-and-activation-governance.qmd#lyra-neuron-explorer-and-neuronary) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd), [Unit 7](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd) | Gated-product edits and random-direction identity control; community exploration without unique-personality-neuron inference. |
| `ext_neuronary_2026` | [White-Box Evidence, Interpretability, and Activation Governance](../chapters/white-box-evidence-interpretability-and-activation-governance.qmd#lyra-neuron-explorer-and-neuronary) | [Unit 5](../editions/reader_manuscript/current/chapters/unit-05-evidence-states-and-scalable-oversight.qmd), [Unit 7](../editions/reader_manuscript/current/chapters/unit-07-constitutions-moral-uncertainty-and-objective-formation.qmd) | Portable recipes, dose/site semantics, schema versus runner support, model alias versus exact checkpoint. |

| Author-concept source | Explanatory technical entry point | Reader route | Mechanism and retained boundary |
|---|---|---|---|
| `regret_engine` | [Policy Optimization and Learning from Feedback](../chapters/policy-optimization-and-learning-from-feedback.qmd#regret-packets-are-protected-feedback-not-actor-rewards) | [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Protected feedback packet; severity, causation and learning eligibility stay separate. |
| `learning_compute_topology` | [Learning–Compute Topology and Adaptive Process Architecture](../chapters/learning-compute-topology-and-adaptive-process-architecture.qmd#mechanism) | [Unit 20](../editions/reader_manuscript/current/chapters/unit-20-governed-training-and-learning-compute-topology.qmd) | Adaptive identity, LCT-IR, causal normal form, semantic firewall and realization costs. |
| `assurance_shift_learning` | [Data Engines, Continual Learning, and Unlearning](../chapters/data-engines-continual-learning-and-unlearning.qmd#regret-aware-replay-without-failure-fixation) | [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Informative exceptions, protected positives, natural/probe separation and learner-relative negative half-life. |
| `adjudicated_persistence` | [Adjudicated Persistence and the Adaptive Commit Boundary](../chapters/adjudicated-persistence-and-the-adaptive-commit-boundary.qmd#six-objects-that-must-not-collapse) | [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Experience, lesson, disposition, realization, lease and authority; least-commitment persistence. |
| `forward_transfer_program_synthesis` | [Procedural Memory and Cognitive Loop Closure](../chapters/procedural-memory-and-cognitive-loop-closure.qmd#forward-transfer-is-the-admission-test-for-reusable-knowledge) | [Unit 18](../editions/reader_manuscript/current/chapters/unit-18-procedural-memory-inter-stack-exchange-and-multi-agent-risk.qmd), [Unit 21](../editions/reader_manuscript/current/chapters/unit-21-adjudicated-persistence-generalization-feedback-continual-learning-and-unlearning.qmd) | Compression, valid reuse and future-task causal benefit; matched removal/placebo and frozen knowledge rounds. |
| `compiling_civilization_cmtq` | [Cognitive Method Transfer and Qualification](../chapters/cognitive-method-transfer-and-qualification.qmd#mechanism) | [Unit 13](../editions/reader_manuscript/current/chapters/unit-13-cognitive-compilation-and-semantic-ir.qmd) | Source method record, functional transport and qualified protocol; efficacy, assurance and authority are separate. |
| `reflexive_model_world_systems` | [Reflexive Model-World Systems](../chapters/reflexive-model-world-systems.qmd#mechanism) | [Unit 11](../editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd) | Deployment-descended evidence, eight response channels, grounding reserves and persistence-aware recovery. |
| `deterministic_capability_compilation` | [Stable Capability Fields](../chapters/stable-capability-fields.qmd#capability-fields-as-compilation-units) | [Unit 9](../editions/reader_manuscript/current/chapters/unit-09-stable-capability-fields-and-governed-replacement.qmd), [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd) | Neural Capability Objects, four ABI layers and obligation mass balance; candidate-specific qualification. |
| `platonic_world_model` | [Cognitive Compilation and Semantic IR](../chapters/cognitive-compilation-and-semantic-ir.qmd#bidirectional-capability-and-concept-compilation) | [Unit 11](../editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd), [Unit 13](../editions/reader_manuscript/current/chapters/unit-13-cognitive-compilation-and-semantic-ir.qmd) | Stable Form/version identities, Essence Contracts, semantic basis and world branches; distinct from external representation convergence. |
| `relational_dimension_compiler` | [Relational Dimension Compilation and Polyadic Cognition](../chapters/relational-dimension-compilation-and-polyadic-cognition.qmd#mechanism) | [Unit 13](../editions/reader_manuscript/current/chapters/unit-13-cognitive-compilation-and-semantic-ir.qmd) | Role-addressable higher-order candidates, complete denominator, lower-order rescues and reversible slow-path compilation. |
| `precision_contract` | [RankFold, NeuralFold, and Artifact Compression](../chapters/rankfold-neuralfold-and-artifact-compression.qmd#functional-precision-preserve-behavior-not-coordinates) | [Unit 23](../editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd) | Contract-relative behavior and complete descriptions; conditional/tail protection, residual precision and qualified selector. |
| `kernel_english_residual_compiler` | [Cognitive Compilation and Semantic IR](../chapters/cognitive-compilation-and-semantic-ir.qmd#protected-sense-aware-lowering-into-a-kernel-packet) | [Unit 13](../editions/reader_manuscript/current/chapters/unit-13-cognitive-compilation-and-semantic-ir.qmd), [Unit 14](../editions/reader_manuscript/current/chapters/unit-14-virtual-context-and-durable-semantic-memory.qmd) | Protected objects, sense-aware Kernel IR, residual/exact-object channels, rendering and bounded round-trip validation. |
| `reflexive_router_whitepaper` | [Routing Heads and Specialist Cores](../chapters/routing-heads-and-specialist-cores.qmd#pre-deliberative-reflexive-dispatch) | [Unit 18](../editions/reader_manuscript/current/chapters/unit-18-procedural-memory-inter-stack-exchange-and-multi-agent-risk.qmd), [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd) | Pre-deliberative proposal versus admission, qualified dispatch, fallback and trace-to-reflex lifecycle. |

The independent reader now contains 153,245 visible words in 26 units. The
current P1 census retains 4,064 structured atoms and 64 dossiers; five new
line-wrapped candidates were individually reviewed, bringing its reviewed
prose queue to 4,227 with no pending materiality decision. Those fragments
apply existing invariants or report the MCCL taxonomy. Chapter cores,
344 proof-target definitions, scientific outcomes, support and frozen custody
are unchanged. Fifteen selected HTML pages rendered. Browser checks pass for
both new technical sections in Human/AI modes, additions in seven narrative
units, eight selected reference links and three layouts. Narrow and
doubled-text screenshots were inspected. Six initially unresolved
reader-to-reference source links now use the existing canonical HTML route
pattern. Unit 21's repeated framing was condensed to preserve its existing
length budget without dropping the new mechanisms or evidence limits.
Source, outline, claim-census, reader, schema, publication, visual-coverage and
proof-manifest consistency checks pass. These checks do not establish
independent reader comprehension, complete-site qualification or deployed
publication. The existing dependency review expiry is not renewed by this
editorial pass.



### November 2 neuron/persona steering and the named community tools

The user's specific lead, Lyra (`@_lyraaaa_`, `lyraaaa.dev`), identifies Neuron
Explorer and Neuronary. The author's website directly links both tools and the
Evil Qwen demonstration. The X post itself returned HTTP 403 and was not read;
no exclusive discovery or popularity ranking is inferred. Neuron Explorer is
reviewed at commit `7ec363d2d9686802a1b4aa7c6d8a2627b1759159`; Neuronary at
`2ffbfee8826bbc6a66774e28b406d31eae6ef860`. Selected README, log, schema and
runtime-hook passages are recorded in their source notes. No software from
those projects or model weights was executed.

White-Box Evidence now distinguishes raw MLP coordinates, distributed persona
vectors, Assistant Axis caps and a trained calibrated controller. NPTI's
identification statistic uses the nonlinear gate output; Lyra's inspected hook
edits the gated product entering the down projection. The Neuron Explorer case
retains its author's random-direction identity-change control. The Neuronary
case separates dose/site/token semantics, schema acceptance, runner support,
model names and exact checkpoint identities. Community examples, readouts,
interpretations, votes and reproduction reports retain their evidence limits.
The explanation credits accessible exploration and recipe sharing without
turning a striking output into a unique “personality neuron” or safety result.

Five selected papers supply NPTI, Persona Vectors, Assistant Axis, capability
collateral and Persona Dosing mechanisms/comparators. The Persona Selection
Model essay supplies an explicitly non-exhaustive explanatory hypothesis in
Inner Alignment. That chapter separates altered persona expression from
learned-objective identification and from removal, suppression or capability
damage. Reader Units 5/7 receive short explanations. Two obsolete source-ID
aliases in the current White-Box editorial packet now point to actual corpus
entries; the original reader claim and rule are preserved.

Eight new source notes yield nine assignments through two existing owners.
Current totals are 527 sources/1,385 assignments and 152,358 reader words.
The two technical owners are outside the historical activation-era P1 scanner;
its 4,064 atoms/4,222 reviewed candidates/64 dossiers remain unchanged. New
prose and limits were read directly rather than inferred reviewed from that
scanner. Core contracts, proof target definitions, experiment outcomes,
support and frozen custody are unchanged. No steering trial, training campaign,
Docker or Lean rebuild is required for this editorial integration.

Seven selected HTML pages render successfully. Browser checks pass for three
White-Box sections and one Inner-Alignment section in Human/AI modes, both
reader explanations and three selected layouts. Narrow and doubled-text
screenshots were inspected. Source/schema/publication, reader, visual,
claim-census, outline and proof-target consistency checks pass. This is no
fresh whole-site or independent-reader qualification.



### November 2 recent-literature representation

A dated primary-source survey admitted twelve selected sources into eight
existing technical owners, with five concise current-reader explanations.
Nine papers were submitted September–October 2026. The earlier RLM, Nested
Learning and end-to-end TTT sources fill missing foundations; their actual
submission/revision dates remain explicit. Selected method, comparator and
limitation passages were read from the pinned primary versions listed in each
source note. This is neither an exhaustive field census nor complete paper,
reference, code or theorem verification.

| Existing owner | Added representation | Qualification retained |
|---|---|---|
| Durable Semantic Memory | Mem++ and Memory-Centric Continual Learning | Whole-document read-time selection, graph temporal leakage, behavioral retention/adaptation/transfer; scaling relations are hypotheses. |
| Governed Deliberation | RLMs and Hybrid Reasoning Agents | Externalized context versus latent computation; recursive cost, full continuation state and bounded auditability. |
| Cognitive Substrates | Nested Learning/Hope and end-to-end TTT | Different context/update frequencies and adaptive weights; neither solved forgetting nor complete cost advantage. |
| Multi-Agent Dynamics | Muffin | Selective asynchronous sharing, dispatch-time visibility, summarizer harms and reasoning-only evaluation scope. |
| Embodied Agency | TRUST | Correctability versus actionability; improved manipulation reasoning coexists with largely unchanged task success. |
| Benchmark Ratchets | Production-agent rater/drift study | Comparable measurement, sign-off time, unlogged drift and operational corroboration without causal program-effect attribution. |
| Scalable Oversight | Monitorability Disposition and ShutdownMod | Voluntary reporting versus independent observation; authentic request versus compliance versus actual enforcement. |
| Scientific Discovery | TTME | External memory adaptation, original-paper TTT comparators, within-search versus held-out transfer, runtime excluding candidate evaluation. |

Each chapter's source loading queue, manifest, crosswalk and note records the
actual use. Current reader Units 5, 10, 14, 19 and 23 gain short explanations
rather than a second paper catalog. The manuscript contains 152,147 visible
words. The original reader conclusions, technical cores, proof definitions,
scientific outcomes and support states retain their scope. Seven new P1 prose
fragments were individually reviewed; none adds an unowned material claim.
Other promising abstract-level leads are retained in the existing schema-bound
backlog for method review, not declared irrelevant or fully integrated.

Sixteen selected HTML pages rendered. Browser checks pass for all eight new
technical sections in Human/AI mode, all five reader explanations, and the
adaptive-state section at desktop, 320px and doubled-text 390px layouts.
Screenshots were inspected; no whole-site, assistive-technology or independent
reader qualification is inferred. Source-note, chapter/source, claim-census,
reader, schema, publication and visual-coverage checks pass. No Docker, model
training, scientific replay or Lean rebuild was performed.

Source-note validation also exposed missing standard navigation sections in the
Atlas source guide. Added pointers to its existing mechanism/evidence/boundary
content and actual three chapter routes; the exact supplied paper, PDF and
evidence index remain unchanged.



### November 2 source integration and pending-work reconciliation

The Answerability Atlas Project synthesis is selectively integrated into
Benchmark Ratchets, Resource Economics and Scientific Discovery, with short
source-linked explanations in current Units 22 and 23. The review compared the
selected cases against the public manuscript, its source guide and supplied
claim index. It preserves the positive development signal, failed advancement
criteria, aggregate-versus-regime calibration, unrun confirmation, and the
post hoc correction on reused worlds. Reported action budgets, CPU timing and
independent world counts retain their separate meanings. The private underlying
research was not accessed or independently replicated; the tested controller
line remains closed. The original public source files retain their exact bytes.

This integration is combined with the previously pending editorial, source,
publication and contributor-tool improvements on `main`, as requested. It does
not constitute a fresh full-manuscript review, author approval or completion of
the 114-item improvement goal. The current manuscript has 151,719 visible words.
The existing dependency-pin renewal remains overdue; its dates are not renewed
by prose review, selected HTML inspection or local infrastructure tests.


The current edition is the independently authored 26-unit manuscript under
`editions/reader_manuscript/current/`. The July 4 baseline below describes an
older generated excerpt and remains historical. Review completeness is not
inferred from target lengths or automated checks.

On October 10, the full assistant editorial pass reached all 26 current units,
reviewing their mechanisms, examples, alternatives, failures, conclusions, and
routed evidence boundaries. The scoped changes are recorded below. This is not
Corben’s author approval or independent reader evidence. Cross-chapter editing,
remaining technical-owner reconciliation, and any separate review decisions
remain explicit work rather than being inferred complete from this pass.

| Owner | Gap and substantive disposition | Remaining boundary |
|---|---|---|
| Unit 1: the stack thesis | Reviewed the complete opening argument, extending the earlier diagram pass. The dependency incident is hypothetical and an incomplete account does not identify the entire cause. Weak systems still need authority controls. Noninheritance is a design rule permitting justified delegation and scoped evidence reuse; applicable grants do not require repeated approvals. A missing consumer remains missing unless the inventory/acceptance obligation exposes it. Ordinary version control and reviewed diffs may suffice. Acknowledgement differs from observed state, and provisional learning can precede incident closure. | No actual incident, prevention result, hidden-dependency discovery, architectural advantage, complete runtime, support promotion, or author approval established. Existing diagram definitions and prior layout evidence remain unchanged. |
| Unit 2: complete efficiency argument | Reviewed the complete unit against its outline. Added a hypothetical full-cost comparison and reuse break-even calculation. Separated correct refusal from accepted transformations, preserved the attempted cohort, made cost-vector incomparability explicit, and distinguished demonstrated overkill from unexamined alternatives. Replaced an absolute reversibility promise with challengeable allocation policy. A competent conventional agent may win. Visual inspection identified fragmented table words on narrow screens; the comparison now has readable columns and a keyboard-scrollable frame. | Arithmetic and campaign scenes are teaching examples, not observations. The core remains an argument; no calibrated router, natural advantage, or author approval established. |
| Unit 3: authority and revocation argument | Reviewed the complete unit against its four routed responsibilities. Added two local revocation orderings and a remote unknown-effect variant, including current authority for restoration and the intervening-edit hazard. Narrowed pre-effect denial and compromised-substrate absolutes; shortened fixture inventories to their actual conclusions with canonical owner links. | Local atomic ordering is an explicit hypothetical assumption, not distributed revocation evidence. No deployed permission, hazardous-domain, strategic, or institutional result added. |
| Unit 4: security composition and custody | Reviewed the full unit and its seven responsibilities. Added a competent ordinary-controls case and variants that separately justify privacy review, untrusted execution, or protected computation. Corrected receipt/reconstruction, digest/signature, and privacy-legitimacy overclaims. Primary RFC 9334 Sections 3, 3.4, and 10 ground attestation roles, possible co-location, and bounded freshness; the existing source note records selected passage review. | The source supplies architecture, not protocol or hardware qualification. All scenes are hypothetical; no runtime, privacy, custody, or release outcome added. |
| Unit 5: evidence and oversight | Reviewed the full unit and its three responsibilities. Corrected `Mechanized` from support state to claim label, distinguished historical observation from current reuse eligibility, and made the adapter/activation campaign explicitly hypothetical. Added a simple direct-review win and distinct incompetent, imprecise, and discriminating negative comparisons. Narrowed the idea that a transition can earn more inference than its artifacts support. | No support transition or empirical result added. Semantic review and author approval remain different states. |
| Unit 6: intent and meaningful control | Reviewed the full unit against its four routed responsibilities. Made the teaching mandate explicit, retained applicable prior/session grants, and added a concrete workflow where useful authorized drafting and preparation precede the remaining approval decision. Re-contracting depends on whether new means exceed the current grant. Request retention and local restoration now state privacy and intervening-state limits. | No intent-understanding, comprehension, manipulation, or human-control result added; these are hypothetical workflow choices. |
| Unit 7: constitutional constraints and objective custody | Reviewed the full unit against its four responsibilities. Qualified finite-penalty versus hard-constraint reasoning, made lease lifetime conditional rather than exclusively chronological, and corrected the idea that narrowing revalidates an invalid parent grant. Contrasting routine-edit and rights-check cases let ordinary controls win. Four logical governance records need not become four services or forms. Active revocation differs from preserving historical evidence; shortened numeric inventories retain bounded conclusions and exact owner links. | No objective diagnosis, amendment authority, institutional legitimacy, or natural governance advantage established. |
| Unit 8: institutions and downstream recovery | Reviewed the complete unit and both responsibilities. Corrected release withdrawal versus existing signed copies, and suspended reliance on a changed-case receipt without erasing its history. Three hypothetical closure criteria distinguish upstream restoration, a volunteer project's unknown exposure, and an institution's unresolved record remedy. Existing incident tools may carry those relations without a new service. Shortened formal inventories while retaining finite non-identifiability results and owner links. | No actual release withdrawal, institutional mandate, affected-party recovery, remedy, or coordination result added. |
| Unit 9: capability replacement | Reviewed the complete unit and both responsibilities. A competent conventional registry may already own contracts and approval policy. Shadow execution needs admitted exposure; restoration does not renew fallback qualification. Added a shared test-selector defect that disqualifies both verifiers for an affected use, with qualified alternatives or a hold. Preserved the exact bounded rollback/utility outcomes and linked their owner. | No canary, candidate advantage, semantic recovery, production fallback, or support transition added. |
| Unit 10: observation and physical-control boundaries | Reviewed the complete unit and both responsibilities. Explicit hypothetical scene and toy tick arithmetic distinguish current action authority from stale measurement evidence. Narrowed hash/provenance claims, separated evidentiary qualification from permission, and qualified the ten-case calibration illustration. Selected primary Ames et al. v1 passages ground the conditional model/controller result and actuation limits in the existing note. Shortened formal inventories while retaining the modeled limits. | No gantry, sensor, sampled controller, calibration, or stop-path result added; source passage review is not physical qualification. |
| Unit 11: world models and reflexive evidence | Reviewed the complete unit and both responsibilities. Actuality records are admitted fallible accounts rather than the world itself; horizon uncertainty need not grow monotonically. Replaced the medical alarm analogy with a stopped-move case that cannot identify prevention from absent failure. Direct inspection and a light intervention/outcome record can win without plural-model machinery. Historical forecast, intervention, and protected empirical boundaries remain separate. | No model accuracy, causal prevention, hardware trial, calibration, protected opening, or support transition added. |
| Unit 12: planning and branch joins | Reviewed the full unit. Added a version-7/version-8 join that retains historical work while rebuilding affected obligations. A reserved lab slot does not certify dispatch readiness. Development fit differs from predictive qualification; fallback may activate after failure only within its response bound, and shared reserve capacity needs a qualified mechanism. Accepted plan history remains reconstructible without prescribing one internal data structure. | No planner quality, natural schedule, gantry trial, or recovery result added. |
| Unit 13: compilation and method transfer | Reviewed the full four-owner unit. Corrected the stale three-owner result summary, added CTR/QCP names and bounded package-conformance status, and scoped method-performance assurance consistently with the glossary. Two target repairs distinguish path disclosure from unsupported safety inference. A direct/template baseline gets the same validators and reviewer; IR must earn added repair or consumer value. | No method efficacy, open-domain semantic preservation, compiler advantage, new leak, or public release added. Existing QCSA synthetic outcome retains its exact denominator and cost limit. |
| Unit 14: temporary context and durable memory | Reviewed the full three-owner unit. Historical receipts now survive changes to current reliance; revoking source use does not itself refute every derived proposition. Two hypothetical repair paths distinguish permitted diagnostic archives from prohibited retention, including lost replay fidelity and a current public evidence basis. Lease closure no longer implies physical erasure. Conventional stores, policy versions, and cache invalidation may suffice; finite result summaries link exact owners. | No natural retrieval, isolation, deletion closure, unlearning, privacy compliance, or author approval established. Unknown copies remain residual. |
| Unit 15: verification and claim revision | Reviewed the full five-owner unit. Added a narrow repaired release note and distinguished missing sensor coverage from evidence of a failed stop. A direct source reviewer may catch the omission without new ledger machinery. Corrected kernel/source stage conflation using selected official Lean passages. Revision history now states retention limits, current proof-packet eligibility differs from historical theorem validity, and checks are selected by claim obligations rather than universally required. | No actual controller trial, reviewer competence, independent verdict, new proof, support transition, or author approval established. Selected source review does not recertify the pinned toolchain. |
| Unit 16: work and organizational custody | Reviewed the full five-owner unit. The security example is explicitly hypothetical; its named dependency criterion does not certify whole-package security. Replaced unbounded deployment reversibility with a recovery contract and narrowed product chronology to overlapping work-surface modes. Toy 50-minute/60-minute budgets show review burden can outweigh drafting savings, with an ordinary-route win and concrete refusal/learning consequences. AI-alone comparison depends on admissible tasks and decision rights; expired review permission does not erase remedy duties. | No measured productivity, natural job completion, adoption forecast, legal accountability, cognitive benefit, worker outcome, or author approval established. |
| Unit 17: effects and operational recovery | Reviewed the full three-owner unit. Current grants need not prompt repeated approvals, and effect leases have declared expiry conditions. Recovery cannot treat an old vulnerable package as a security fallback. A conflicting operator repair constrains pointer restoration and identity-based cache cleanup; the example holds affected downloads while preserving status/recovery channels. Observation covers named routes and times rather than all clients. Historical payload retention remains conditional, and the handoff now includes procedure promotion. | No production release, qualified fallback, complete effect inventory, independent deployment observation, recovery efficacy, new incident result, or author approval established. Existing finite and bounded execution results retain their scope. |
| Unit 18: procedure reuse and inter-stack exchange | Reviewed the full three-owner unit. The hypothetical continuation retains prior downstream duties. Absorbing retirement now requires a newly qualified version rather than reactivating the retired one. Allocated budget does not grant effect permission, and future withdrawal does not reverse prior exchanges. Selected local forward-transfer paper sections ground frozen test/library separation and rerun-based removal tests rather than deleting a call. A primary-endpoint receipt can remain accurate while failing a three-endpoint release obligation; a reviewed script may suffice. Missing receipts remain unresolved attempts, and a capability declaration alone does not establish enforcement. Population observation does not confer intervention power. | No learned procedure, causal transfer, real peer, payment, settlement, population safety, new evidence promotion, or author approval established. The source remains an unexecuted experimental blueprint; unknown traces and copies remain residual. |
| Unit 19: routing and substrates | Reviewed the complete four-owner unit, extending the earlier direct-route and confidentiality cases. Unexpected execution failure differs from a knowingly incompatible selection; fallback requires current qualification and permission. Toy compatibility, answer-acceptance, and attempted-success denominators remain different. Adoption now binds authority and bounded recovery while preserving the old anchor. A winding identifies an overwritten generation but cannot reconstruct its missing payload. Candidate populations and incomparable cost vectors have declared scope. | No router calibration, natural heterogeneous-routing advantage, state restoration, substrate interchangeability, cyclic retrieval benefit, or author approval established. |
| Unit 20: training and learning topology | Reviewed the complete two-owner unit, retaining the earlier experimental versus service-recovery comparison. A prospectively declared adaptive data policy can remain in one campaign. Optimizer-state requirements depend on the rule; hashes cannot expose an omitted state class. The dated eleven-test package check remains IR evidence. Qualification methods depend on the consumer claim, historical scaling observations survive changes in reuse eligibility, and typed connections do not establish causal effects. Authorized internal updates and valid retry grants remain usable. | No training run, resume equivalence, optimizer result, independently mechanized LCT proposition, causal topology effect, broad support promotion, or author approval established. |
| Current quickstart | The observed retrospective example favored full governance. Added five clearly hypothetical alternatives: direct success, necessary denial, incomplete compensation, observer disagreement, and excessive governance cost. The observed P5-U1 denominator remains separate. | Teaching cases are not new observations or support transitions. |
| Earlier focused vocabulary pass on Units 15 and 17 | Distinguished receipts, observations, and evidence; separated effect permission from canonical-source precedence; named how effect, allocation, purpose, and source admission leases differ. The review and deployment scenes are now explicitly illustrative. | This focused pass does not close full narrative review or establish the depicted trial or deployment as an observation. |
| Unit 21: persistence and learning | Reviewed the full five-owner unit. The two-patch story is explicitly hypothetical; a regression guard differs from repairing a tool, and a local preflight remains possible without upstream ownership. Commitment profiles can be incomparable, existing policies can admit bounded updates, and advertised recovery does not require a full copy after every gradient. Active withdrawal differs from reversing prior effects. Selected Bourtoule Definition III.1 grounds model-distribution removal; a repeated public fact can survive removal of one record. Known descendants, unknown copies, and permitted history remain distinct. | No integrated adjudicator, causal lesson, prospective transfer, learned policy, certified local unlearning, privacy closure, scientific discovery, or author approval established. Finite controls and bounded local campaigns retain their existing scope. |
| Unit 22: evaluation and assurance | Reviewed the complete six-owner unit. The release story is explicitly hypothetical. Toy accounting separates eligible tasks, attempts, graded accuracy, verified yield, unresolved results, and cost. One broken instrument does not automatically erase unaffected qualified evidence. Presented evaluation cues do not directly reveal belief or intent; disagreement follows the risk policy. Quarantine retains permitted history, not unrestricted payloads. Safety-case criteria, signer trust, and assertion truth remain separate; selected C2PA 2.3 passages ground the distinction. An ordinary checklist can carry the same scoped decision. | No candidate evaluation, deception finding, capability crossing, canary, enforcement guarantee, real safety case, C2PA conformance, independent reviewer outcome, support promotion, or author approval established. |
| Unit 23: generation, compression, and allocation | Reviewed the complete five-owner unit. Cache exactness differs from current policy applicability, and primary text establishes what was written rather than result correctness. Lossy compression declares its losses and permitted retention bounds replay. The worked budget separates 20 planned machine units, a six-unit reserve, actual spending, and five reviewer minutes; a toy pipeline exposes verification and review queues. Digests bind bytes while an inspected diff identifies a bibliography-only revision. Bounded owner summaries retain failed, no-change, uncompressed, license-disabled, and actual-model negative outcomes. | No ingestion run, model-serving acceleration, natural compression utility, deliberation advantage, calibrated allocator, whole-system optimum, support promotion, or author approval established. |
| Unit 24: physical capacity and infrastructure | Reviewed the complete two-owner unit. Placement runs are explicitly hypothetical, and local hardware does not itself establish data confinement. Toy accounting distinguishes requested, nominal, available, completed, and accepted work; all attempt costs belong above the accepted-output denominator. Selected LBNL passages separate facility/IT electricity, site/generation water, and simulation assumptions. A timed offline example distinguishes partition, revocation, admissible stale-state exposure, and unknown effect ordering. Retirement separates withdrawal, permitted history, disposal, and unknown copies. Ordinary placement can win and evidence requirements follow each claim. | No hardware trial, live hive, natural scheduling, environmental footprint, causal regression diagnosis, complete deletion, resilience, community result, support promotion, or author approval established. |
| Unit 25: recursive improvement and containment | Reviewed the full three-owner unit. The verifier campaign is hypothetical; tests expose defects while production repairs or qualified guards address them. Reused evidence retains history, current fallback must be adequate, and restoration respects intervening authorized work. Evaluation cues do not identify belief. Toy replication counts separate attempts, artifacts, admissions, completed lifecycles, and assistance; the selected RepliBench v2 abstract remains study-scoped. Descendant grants can be prospectively bounded, quarantine respects retention, and stop commands do not prove closure. | No natural verifier improvement, recursive advantage, strategic-intent finding, autonomous replication, live provider, complete shutdown, containment efficacy, support promotion, or author approval established. |
| Unit 26: integration and living research method | Reviewed the full six-owner unit. The integrated request is hypothetical; applicable grants and explicit merge intent are preserved. Existing workflows may carry the same relations. Acknowledged effects can retain unresolved incidents; histories and projections respect retention. Natural observation does not automatically generalize or prove prevention. The local successor uses a two-parameter predictor and one deduplicating HTTP sink; its constructed direct arm does not indict competent ordinary release checks. Book completion is distinct from executing the future research agenda; current target-length readiness remains a drafting fact. | No complete reference runtime, general exactly-once API behavior, prevention effect, architecture superiority, new scientific campaign, support promotion, independent reader approval, author approval, or publication established. |
| Concept finder and glossary return paths | Added thirteen selected narrative entry points and five stages of the hypothetical repository example to the current index. Chapter paths derive from the owner crosswalk and named source headings are checked before generation. Twelve essential glossary definitions have stable term anchors and links back to the matching reader entry. Quickstart depth routes lead to the finder. Narrative and glossary destinations are explicitly distinct from technical evidence ownership. | Search-result labels across technical, historical, reader, and paper surfaces remain open under K09. These links are navigation, not author approval, a user study, or evidence promotion. |
| Units 1, 15, 17, and 21: diagram teaching | The opening map exposes a dispatch denial; new diagrams separate checked facts from bounded claim decisions, restoration from compensation/residuals, and candidate lessons from durable commits. Captions and full text versions preserve the actual relationships and limits. Local mobile and enlarged-text inspection prompted reflow and navigation repairs. | Twelve local Chrome observations pass; actual chapter numbering aligns with units. No learner study, assistive-technology approval, or deployment qualification inferred. |

The full reader was rendered after the Unit 2/3 edits: 28 pages and 1,631
local links resolve. Six local installed-Chrome views cover those two pages at
desktop, 320 pixels, and doubled text. All avoid page-wide overflow, and the
cost table scrolls locally with the keyboard. Screenshot inspection identified
the initial word-fragmentation problem despite the overflow check passing;
the readable table frame addresses that specific defect. These observations
are limited layout evidence, not a reader study or publication qualification.

After the Unit 4/5 revisions, the complete 28-page reader renders with 1,634
resolving local links. Seven new technical references match configured site
paths and existing rendered anchors. Source-note validation passes all 501
notes; that checks note structure and custody, while the selected RFC passage
review above supplies the substantive attribution. No browser or reader-study
scope is inferred from this prose-only render.

After the Unit 6/7 revisions, the complete 28-page reader renders with 1,638
resolving local links. Six added technical references match configured site
paths. Reader projection, publication, base-book, release-profile, spine, and
current negative-inference checks pass. These are source/render checks; the
hypothetical decisions and control conditions remain arguments, not observed
human or institutional outcomes.

After the Unit 8/9 revisions, the complete 28-page reader renders with 1,642
resolving local links. Four added technical references match configured site
paths. Current reader projection, publication, base-book, release-profile,
spine, and negative-inference checks pass. No new browser, natural replacement,
or affected-party outcome is inferred from these source/render checks.

After the Unit 10/11 revisions, the complete 28-page reader renders with
1,645 resolving local links. Four added technical references match configured
site paths. Source-note checks pass all 501 notes, alongside current reader,
publication, base-book, release-profile, spine, and negative-inference checks.
Selected primary source passages supply the bounded attribution; these
source/render checks add no physical or predictive outcome evidence.

After the Unit 12/13 revisions, the complete 28-page reader renders with
1,649 resolving local links. Five added technical references match configured
site paths. Current reader projection, publication, base-book, release-profile,
spine, and negative-inference checks pass. Four-owner narrative coverage was
repaired through semantic review, not inferred from the word-count or crosswalk
gates. No natural planner, compiler, or method-transfer outcome follows.

After the Unit 14/15 revisions, the complete 28-page reader renders with
1,649 resolving local links. Eight technical owner references match configured
site paths and existing rendered pages. Current reader projection, publication,
base-book, release-profile, spine, source-note, and negative-inference checks
pass. The source-note gate checks structure; selected primary passage review
supports the corrected Lean explanation. No new browser, toolchain, physical,
privacy, natural-verifier, or remote-publication qualification is inferred.

After the Unit 16/17 revisions, the complete 28-page reader renders with
1,649 resolving local links. Nine references to eight technical owners match
configured site paths and existing rendered pages. Current reader projection,
publication, base-book, release-profile, spine, and negative-inference checks
pass. These are prose/source/render checks; no new browser, worker study,
productivity measurement, incident campaign, author approval, or remote
publication qualification is inferred.

After the Unit 18 revisions, the complete 28-page reader renders with 1,649
resolving local links. Three technical owner references match configured site
paths and retained rendered pages. The added forward-transfer paper was absent
from the chapter preview, so its source page and current changelog were
rendered explicitly in a declared-source partial preview. The first paper
render used its nested project's output directory; an explicit project-root
render places it at the intended local `/papers/` route, with selected protocol
section headings present and canonical source unchanged. This is not a clean
full-root render or remote link/deployment attestation. Current reader
projection, publication, base-book, release-profile, spine, and negative-
inference checks pass. Semantic review and selected author-paper passages do
not supply a transfer result, real peer exchange, natural population study,
or author approval.

After the full Unit 19/20 revisions, the complete 28-page reader renders with
1,649 resolving local links. The previous adoption anchor remains in the actual
HTML despite its corrected heading. The added LCT technical reference matches
the configured site and retained rendered path. Current reader projection,
publication, base-book, release-profile, spine, and negative-inference checks
pass. The heading expectation was updated without removing the validator's
other obligations or its rejecting controls. These are editorial/source/render
checks, not router calibration, a training replay, new source-package execution,
a natural architecture comparison, author approval, or remote publication.

After the Unit 21 revisions, the complete 28-page reader renders with 1,649
resolving local links. Four technical references match configured site paths
and retained rendered pages. Current reader projection, publication, base-book,
release-profile, spine, source-note, and negative-inference checks pass. All
501 source notes retain their structural acceptance; the selected arXiv v3
definition passage supplies the substantive attribution rather than that gate.
The existing diagram is unchanged. No new mobile inspection, causal episode,
unlearning algorithm, removal guarantee, privacy closure, natural learning
comparison, author approval, or remote publication is inferred.

After the Unit 22 revisions, the complete 28-page reader renders with 1,649
resolving local links. Six technical references match configured site paths
and retained rendered pages. Current reader projection, publication, base-book,
release-profile, spine, source-note, and negative-inference checks pass. All
501 source notes retain their structural acceptance; selected C2PA 2.3 scope
and trust-model passages supply the substantive attribution. The toy cohort and
release sequence remain examples. No new browser observation, real evaluation,
monitor finding, capability crossing, canary, signature exercise, standard
conformance, assurance acceptance, author approval, or deployment is inferred.

After the Unit 23 revisions, the complete 28-page reader renders with 1,649
resolving local links. Five technical references match configured site paths
and existing root preview pages. Reader projection, publication, base-book,
release-profile, spine, and negative-inference checks pass. The arithmetic and
queues are teaching examples, not an ingestion run or efficiency measurement.
No new browser, author-approval, or remote-publication evidence is inferred.

After the Unit 24 revisions, the complete 28-page reader renders with 1,649
resolving local links. Two technical references match configured site paths
and existing root preview pages. Reader projection, publication, base-book,
release-profile, spine, source-note, and negative-inference checks pass. All
501 notes retain structural acceptance; selected LBNL pages supply the scoped
attribution. No hardware trial, browser observation, author approval, or remote
publication is inferred.

After the Unit 25/26 revisions, the complete 28-page reader renders with 1,649
resolving local links. Nine technical references match configured site paths
and existing root preview pages. Reader projection, publication, base-book,
release-profile, spine, source-note, and negative-inference checks pass. All
501 notes retain structural acceptance; the selected RepliBench v2 abstract
is the scoped attribution. No natural improvement, replication attempt,
complete integrated runtime, browser observation, author/reader approval, or
remote publication is inferred.

After the final Unit 1 revision, the complete 28-page reader renders with
1,649 resolving local links. All seventeen technical body references across
Units 1 and 23–26 match configured paths and existing root preview pages.
Reader projection, publication, base-book, release-profile, spine, and
negative-inference checks pass. Source-note checks passed the selected LBNL
and RepliBench changes: 501 notes, without implying complete source review.
The manuscript has 151,089 visible words and 26 units within their pacing
ranges. Unit 1’s Mermaid definition matches the pre-review rendered source;
no new mobile, assistive-technology, reader-study, author-approval, deployment,
or research result is inferred from this prose-only render.

The concept-finder change renders in the complete 28-page reader; 1,671
reader-local links resolve. The glossary and changelog were separately rendered
against an owned prior technical preview, then paired with the current reader:
29 selected pages have 2,083 resolving local/canonical-mirrored links and
anchors, including all twelve bidirectional essential terms. Three installed-
Chrome views cover desktop, 320 pixels, and doubled text at 390 pixels; narrow
and enlarged screenshots were inspected. Five links were activated with the
keyboard and reached revocation, rollback, compensation, persistence, and the
glossary return path. Initial same-page waits failed because the local render
opens those routes in a new page; the corrected inspection follows that actual
behavior. Canonical-site links were redirected to the local mirror. This is
bounded navigation/layout evidence, not remote availability, an independent
reader study, assistive-technology inspection, global search-label completion,
author approval, or release. Current reader/build/publication/base-book/profile/
spine/negative-inference source checks pass. Reader search contains 28 current
narrative pages; the retained technical search contains 89 chapter, eleven
appendix, and two root pages, without proving paper or historical discovery.

Diagram implementation uses [Mermaid accessible titles and descriptions](https://mermaid.js.org/config/accessibility.html), with adjacent full descriptions following [W3C complex-image guidance](https://www.w3.org/WAI/tutorials/images/complex/). The quickstart's explicit unnumbered heading follows [Quarto book structure](https://quarto.org/docs/books/book-structure.html). These are implementation references, not architecture evidence or a conformance certificate.

Continue cross-chapter editing and targeted load-bearing source review, then
record any author or independent-reader decisions separately. The full
assistant unit pass does not settle those judgments. Preserve the
existing pacing ranges unless their outline owner is deliberately amended.
The generated reading paths are navigation, and local rendering does not
attest deployed HTML.

## Finding and revisiting a concept — 2026-10-11

K09's representative navigation criteria are now verified. The current concept
finder, example stages, and glossary return links retain their exact anchors.
Search labels are generated from the canonical technical graph, current reader
units, appendix owners, and the 59-entry paper manifest. They distinguish
technical reference, Human Reader, evidence/source registries, history, original
author paper, derived synthesis, and their guides. They describe page role,
not source competence, claim support, novelty, or release approval. Unknown or
external result routes receive no inferred role. Quarto keeps its three native
search scopes and ranking; no new search service or index merger is introduced.

Actual selected rendering covers four book pages, six current reader pages,
and three paper pages. Twelve query views in installed Chrome show the expected
labels, including the GitHub Pages subpath. Keyboard activation reaches the
revocation, rollback, and compensation explanations. Five existing finder,
running-example, and glossary return tasks also pass. Search results reflow at
320 pixels and at 390 pixels with doubled text; the existing finder retains its
three checked layouts. These are browser/keyboard observations, not an
assistive-technology inspection or independent reader study.

Visual inspection found an existing naming fallback replacing the search icon
with visible text, and the first new labels inherited insufficient selected-row
contrast. The fallback now sets the input's accessible name without changing
icon content. Selected text uses the book's dark blue accent, including match
highlighting. Observed selected text is at least 5.43:1 against a 4.5:1 small-text
target from [W3C's contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).
This scoped result is not whole-edition WCAG conformance. Initial screenshots
and observations remain in the ignored diagnostic workspace.

The recovery search snippet initially began with raw Mermaid syntax. The
installed Quarto indexer reads complete section text, so no unsupported partial
exclusion was invented. The existing full explanations in Units 1, 15, 17, and
21 now precede their figures; captions, description anchors, and complete
Mermaid source are preserved. The representative compensation result now begins
with prose. Diagram source remains searchable. The four direction notes now say
the text is above, adding four words; the 26-unit pacing total is 151,093.

Generated navigation sources are declared alongside their existing producers.
Source, current-reader, paper byte-custody, and registry checks pass. No source
reproduction, new experiment, support decision, author approval, platform draft
refresh, or publication is inferred.

## Portfolio and competent comparisons — 2026-10-11

The current entry pages, product descriptions, research synopsis, and three-target
summary now agree on the proposed contributions, 89 supporting owners, and
bounded evidence ceilings. The prior-art owner specifies three ordinary
challengers before claiming a delta: an authority/change workflow, a scientific
claim register, and an observation/incident workflow. Each retains competent
controls, current grants, exact review decisions, recovery limits, and full-cost
accounting; equality at lower burden favors the ordinary alternative. The five
older tracks and nine signature-idea assessments preserve dated history.

I01/I02's editorial criteria are satisfied; this is not a comparative experiment
or novelty result. Composition, public process, and local implementation remain
different contribution types. Selected primary in-toto §§2.1–2.3, PROV-O §3.1
and opening §3.2, and NIST SP 800-61r3 §2.1/opening §2.2 passages ground the
specific antecedents. Unreviewed remainder and prior result dates remain intact.
No training, runtime qualification, Docker, conformance, support transition,
author/independent approval, platform-draft refresh, or publication is inferred.

The source consistency check also exposed two stale roadmap assumptions: an
older current-word-count constant and a requirement that the maintained outline
claim deployed status. Current count fields now bind to the generated manuscript
manifest, while the schema keeps every historical cutover field exact. The
outline check recognizes author-review readiness and still requires the intact
22-unit predecessor. This is an editorial state correction, not renewed
publication custody.

Actual partial HTML rendering covers the changed book/changelog and reader
entry; the three product pages and product selector are separately generated.
Across six entry pages, 469 routes/anchors resolve using the declared product
mount. Three publication-generated status/version JSON routes are absent from
this partial preview and remain unverified; this is not an assembled full-site
or deployment check. Both new contribution Markdown resources match canonical
bytes. The initial invented HTML-document links were corrected to the actual
Markdown resources. Source gates accept the portfolio, retained history, source
note structure, current reader, and 24-claim synopsis; selected passage review,
not the structural gate, supplies the substantive attribution.

## Technical terminology reconciliation — 2026-10-11

This pass reconciles the stack thesis, authority, evidence, runtime, and artifact sources
with the current reader and essential glossary. A further selected operations
pass reconciles its opening, recovery/evidence summaries, and local-example
scope. These scopes do not close the wider 89-owner review.

| Owner | Substantive correction | Evidence boundary |
|---|---|---|
| Stack thesis | The common noninheritance rule permits justified delegation and scoped evidence reuse. A competent monolith may preserve the same control relations; decomposition must earn its cost. | Core text and support are unchanged; no comparator experiment or novelty result added. |
| Authority | Distinguished existing grants from missing scope, correct refusal from a denial record, and finite rejection from runtime enforcement. Added local commit-order and remote stale-state conditions. Fixed the Mermaid gate so ceiling and current grant checks are sequentially necessary, and separated delegation lineage from inherited credentials. Ordinary permission controls can win. | Timing examples are proposed conditions, not trials. Finite traces, proof counts, trusted inputs, and deployment exclusions retain their scope. |
| Evidence states | Fixed the Mermaid path that bypassed accepted review after proof/test validation. Adverse information can hold affected reliance, while refutation needs competent claim-specific evidence. A missing replay file or failed proof search is not a negation. Retention restricts payloads without erasing disposition history. Ordinary claim logs and review may suffice. | Existing KERC and QCSA outcomes retain exact values and ceilings. No new source reproduction, theorem, experiment, support transition, reviewer result, or release. |
| Runtime adapters | Reviewed the complete source argument and retained inventories. Pre-dispatch gates no longer demand future post-state and actual-effect receipts. Current grants, qualified commit ordering, bounded observation, crash custody, recovery authority, intervening edits, restoration, compensation, and irreversible exposure have distinct meanings. One readable admission/custody diagram replaces a permissive flow and redundant small sequence; denial cannot flow into invocation. Ordinary capability and workflow controls may suffice. | Worked variants are hypothetical; existing finite and bounded effect results are unchanged. No deployed gate, fresh proof/source review, receipt durability, reviewer-quality, or open-world recovery result added. |
| Governed operations — selected surfaces | Reconciled the drafting guardrail, local P5 explanation, evidence/non-claims, and summary with their own later results. The mutable model is a two-parameter predictor; local sink deduplication is not generic exactly-once delivery. Existing subprocess restoration and the retrospective publication happy path are preserved without being called a natural AI incident campaign. | This is selected evidence-scope editing, not full owner rereview. Five post-activation atom propositions and historical review fields are unchanged; only the affected source binding was refreshed. No new incident, recovery, campaign, or support result added. |
| Artifact graphs | Reviewed the complete source argument. Canonical records are distinct from world truth; playback differs from reexecution and grade follows the requested purpose. Digests do not prove a transformation consumed its claimed inputs. Declared dependency queries flag affected uses, not unseen copies or automatic claim demotion. Retention preserves permitted history without demanding prohibited payloads. Canon decisions, delivery checks, evidence transitions, and release decisions remain separate. Four diagrams now teach these relations with holds and residuals. | Marked core and three recorded outcome/reconciliation blocks are unchanged. Three existing manifest design rules are clarified, and a stale minimum-inventory count is reconciled to unchanged sources; exact prior wording is retained. No fresh Lean, source reproduction, artifact experiment, deletion closure, support transition, or release. |

Twenty new scanner candidates were reviewed in their full paragraph context
against existing atom scopes, confounds, and non-claims. Twelve retired sentence
reviews retain their exact text, prior disposition, source locator, and dated
lineage. At that three-owner pass the registry had 4,064 structured atoms and
4,167 prose candidates; that reconciliation introduced no unowned pending candidate or
new material atom. Three editorial packets bind the inspected source and
updated normative wording. The broader source/proof reviews retain their
historical scope.

The runtime continuation reviewed twenty-one changed scanner candidates in
context and preserved eleven retired sentence reviews with their exact source,
text, and disposition. Its ninety current candidates are adjudicated. The
registry at that continuation had 4,064 structured atoms and 4,177 prose candidates, with
no new material atom or pending candidate. Runtime inventory counts in its
older semantic review now explicitly retain their historical baseline date;
the current source points to its later formalization section without pretending
that this editorial pass renewed the proof review. Both affected editorial
packets bind the current source.

The subsequent artifact pass reviewed twenty changed candidates in their full
paragraph context and preserved fifteen retired reviews with exact text, source,
and prior disposition. Its 101 current scanner candidates are adjudicated. The
registry now has 4,064 structured atoms and 4,182 prose candidates, without a
new material atom or pending candidate. The recorded July 14 faithfulness note
was inspected to reconcile a contradictory metadata-only row; its selected
primary-passage scope was retained without a fresh paper or code review.

Three existing artifact design statements—`mechanism.006`, `mechanism.009`,
and `invariant.006`—now consistently distinguish permitted payload retention,
affected-use eligibility, and separate claim dispositions. The exact prior
manifest wording remains in the existing semantic review. `minimum.001` also
corrects its stale forty-three declaration count to the existing twenty-one
refinement plus thirty-five retained declarations, confirmed against unchanged
source declarations and the recorded audit. This is source inventory evidence,
not a new Lean build. The manifest delta is limited to those four statements;
order, source assignments, core text/support, proof targets, tests, and other
owners are unchanged.

The selected technical HTML pages and all 28 current reader pages rendered
successfully in owned local previews. The final diagram-only adjustment changed
reader parent bindings, while every HTML-bearing reader input stayed identical
to that full render. The paired preview resolves 2,083 links and anchors across
29 inspected pages, including the twelve glossary return routes. The technical
preview retains previously rendered pages outside the selected scope; it is
not a clean full technical build or public deployment.

Installed Chrome inspection of the two mechanism diagrams exposed unreadably
small labels in the horizontal layouts and the first wide evidence layout.
Vertical layouts now render at approximately 16 CSS pixels on the inspected
1280-pixel desktop viewport. Their SVG titles, substantive descriptions, and
adjacent prose explain the actual gates. The edition control also covered upper
diagram labels while scrolling; it now stays in normal page flow at the chapter
opening. Both final inspected pages show no control/diagram overlap. This is
selected visual inspection, not mobile, screen-reader, independent-reader, or
whole-edition accessibility approval; K05–K07 remain subject to their wider
criteria.

The runtime and selected operations HTML pages also rendered in the owned
partial preview. Actual desktop inspection shows the final runtime mechanism
chart at 16 CSS pixels, with its identifying title, substantive description,
adjacent explanation, and no edition-control obstruction. The second sequence
diagram shrank to about 12 pixels and repeated the lesson, so it was removed;
the request/admission/outcome distinctions remain in prose. Preparation now
precedes the final required-gates branch. Reader parent bindings changed, but
all HTML-bearing reader inputs remain identical to the earlier full render.

The expanded local link inspection covers 31 selected pages, including the two
technical pages, and resolves 2,378 links and anchors. Six paper targets are
missing from this partial preview: Deterministic Capability
Compilation, Platonic World Model, QCSA, Regret Engine, Assurance-Shift Learning,
and Adjudicated Persistence. Their canonical `.qmd` sources, library records,
and separate paper-render declarations exist. That verifies source routing,
not rendered-paper availability; these six links are explicitly unverified in
the local HTML scope. No full-site or public-deployment claim follows.

The artifact page rendered successfully in the owned partial preview. All four
rendered diagrams have identifying SVG titles, substantive descriptions, and
approximately 16-pixel labels. Their pixels were inspected in installed Chrome
at a 1280 × 2400 viewport, including denied/unresolved routes and the separate
evidence/release branches. Initial element and full-page capture attempts timed
out; DOM diagnostics confirmed visible diagrams, and bounded viewport captures
succeeded. No product defect or accessibility certification is inferred from
those capture-method results. The inspection remains technical AI view,
desktop, and local, with no mobile or assistive-technology review.

The expanded paired link scope now covers 32 selected pages and resolves 2,536
links and anchors. Eleven links to the same six declared paper targets remain
outside this partial preview's rendered availability. Source routing is
verified separately; those paper links are not counted as rendered successes.
Every HTML-bearing reader input still matches the earlier full reader render;
only its current parent bindings were regenerated.

## Intent-to-execution source reconciliation — 2026-10-11

Reviewed the complete technical owner against the current reader and glossary.
The forbidden-upload and concurrent `R17` timelines are hypothetical; the
existing nine-scenario result stays separate. A competent ordinary reviewed
repository workflow can supply the same joins at lower cost. Existing current
grants cover permitted implementation choices without automatic new approval.
Candidate admission, observed effects, unknown outcomes, and authorized
recovery now have distinct roles. The proposed single-use reservation precedes
the effect; an absent reply cannot silently rearm it. The historical record
checker still consumes after recorded observation and does not implement that
stronger concurrent/crash protocol.

Nine existing manifest design rules retain exact prior wording in their
semantic-review overlays. Thirty-one changed scanner candidates were reviewed
in paragraph context, and thirteen retired dispositions preserve lineage.
There are 4,064 structured atoms and 4,200 reviewed prose candidates, without a
new material atom. The core, four historical campaign outcome sections, family
projection, formal code, fixtures, result identities, support, and release
remain unchanged. Existing Temporal and CaMeL notes record selected official
Activity/idempotency passages and version-one method/threat/failure passages;
this is source reading, not integration or efficacy reproduction.

The selected chapter renders locally. Its overview and single-use diagram were
inspected in installed Chrome at desktop, 320 pixels, and doubled text at 390
pixels. Both have substantive descriptions and keyboard-scrollable frames;
labels remain approximately 20 CSS pixels or larger. The first chart shrank to 14.53 pixels,
and the second enlarged-text version created an unnecessarily huge canvas;
shorter labels and a fixed readable local canvas repair those defects. Dark
labels replace the first blue labels. Stable heading, figure, and lifecycle
anchors remain. The selected page resolves 152 local routes/anchors; one
configured Deterministic Capability Compilation paper is absent from this
partial preview and is not counted as rendered availability. No full-site,
assistive-technology, independent-reader, author, concurrent-effect, or release
qualification follows. Current reader text is unchanged; only parent bindings
were regenerated. Broader I/J/K criteria remain open.

## Planning source and displayed-view reconciliation — 2026-10-11

Reviewed the complete Planning source against its distinct prospective-ordering
responsibility. The hypothetical book-publication case now separates a current
grant, a credential missing before a remote request, and an unknown effect
after a lost reply. Independent authorized work can proceed while the affected
obligation stays held. A competent conventional workflow can supply these joins.
The five/two/one-minute teaching schedule shows why graph independence is not
parallel capacity: two workers predict six minutes, one predicts eight or
eleven depending on the route. These are assumed calculations, not observations.
Forecasts do not identify unexecuted counterfactuals; dependency closure is
bounded by known edges and coverage. The already declared exploratory state
now has a reference definition separating candidate search/simulation from
authorized real observations and effects. Identical payloads can represent separate
requested actions. Compensation does not justify a blind retry, and committed
simulation state is not an actual external effect.

Seven existing design rules retain exact prior wording. Nineteen changed
scanner candidates were reviewed and fourteen retired dispositions preserve
lineage. The registry has 4,064 structured atoms and 4,205 reviewed prose
candidates, with no new material atom. Core, formal scope, finite-world-model
outcome, family projection, proofs, fixtures, support and release remain intact.
The source crosswalk now identifies twelve current assignments without
claiming twelve fresh passage reviews. The existing Airflow note records
selected 3.3.2 Relationships, Task Instances and Special Exceptions passages;
ordinary dependency/retry/human-input controls are recognized without local
integration or imported efficacy.

Actual Human-view inspection exposed an older overlay overriding the corrected
lifecycle text. Three active operations—Planning lifecycle plus Intent
validation and interfaces—now preserve current grants, phase-relative evidence,
node-local holds, permitted history, and separate evidence/release owners.
Their IDs stay stable, and frozen reader copies stay untouched. All 75 active
overlay operations apply structurally; that is not full semantic review of 75
operations. The two selected rendered pages display the new text. Their local
link scope resolves 297 routes/anchors and explicitly excludes three links to
omitted configured papers: Platonic World Model, Regret Engine, and
Deterministic Capability Compilation.

The planning loop has a complete preceding text version, separate plan/runtime
admission branches, and a keyboard-scrollable readable canvas. Three local
Chrome layouts inspect it and the two Intent diagrams. Labels are about 23
pixels for Planning and 20 or larger for Intent; six page-layout observations
cover desktop, 320 pixels, and doubled text at 390 pixels. Enlarged screenshots
also exposed a fixed technical breadcrumb occupying hundreds of pixels. The
compact treatment already used in the current reader now applies to the narrow
technical view, while the full title remains in the page. The first compact
header still let the absolutely positioned search button overlap the title;
placing that control in normal flow removes the overlap. Both selected headers
measure 39 pixels at normal text and 75 at doubled text, and their breadcrumb
and search bounds do not overlap. The Planning sidebar opens/closes with the
keyboard. An
initial menu-close wait lacked renewed button focus; the corrected inspection
refocuses the control and observes actual visibility and expanded state. This
was a diagnostic issue, not a new product failure. No full-site, screen-reader,
independent learner, live-planning, author or release qualification follows.
Current independent reader text remains at 151,093 words; parent bindings were
regenerated. Broader I/J/K criteria remain open.

## I05 fair-case completion audit — 2026-10-11

I05's complete requirement is to state the strongest conventional alternative,
its costs and workload conditions, and the observation that would change the
choice; the criticism must constrain design/comparison rather than remain a
perfunctory objection. This is an editorial requirement. It does not require
execution of the separately specified prospective comparison.

| Requirement | Inspected authoritative evidence | Consequence now stated |
|---|---|---|
| Competent monolith/conventional orchestrator can supply the same accountability | Current reader Unit 1, “The Monolith Can Be the Right Baseline”; technical opener, “Strong alternatives and what would decide between them”; the three conventional blueprints in the prior-art owner | The alternative receives scoped tools, current grants, context, observation, review and recovery; a bare single-call shell route is a thin control rather than the strongest challenger. |
| Additional boundaries can increase latency, operator burden and correlated failure | Prior-art “Fair comparison and decisions”; Unit 1's lifecycle-cost and failure discussion; technical opener's common-policy/verifier/state-store paragraph | Charge routing, verification, review, storage, maintenance, integration and recovery to the comparison. Shared checks are not automatically independent protection. |
| Workload properties favor each design | Prior-art decision conditions; Unit 1's public-documentation case; current Planning, Runtime and Artifact ordinary-alternative discussions | Stable local observable work may use a checklist or conventional workflow; replacement, trust-domain crossing and uncertain external effects motivate testing explicit joins rather than mandatory services. |
| An observation changes the author's proposed conclusion | Unit 1, “Evidence That Would Change the Conclusion”; technical opener's concrete wrapper/pipeline narrowing cases; all three generated equality dispositions | Equal or better useful outcomes and controls at lower total burden favor the ordinary route. Narrow novelty and merge/remove boundaries rather than protecting the diagram. |
| Criticism constrains the choice and does not relabel an ordinary winner | Three `prospective_ordinary_comparison` entries in `products/contribution_focus_contract.json`; prior-art decision rule; corrected technical map/trace and both active opener overlays | Preserve the ordinary implementation's own vocabulary. Mapping it to logical roles does not establish a need for the ASI Stack; specified comparisons remain unexecuted and frozen historical controls remain ablations at their recorded scope. |

The audit found an actual inconsistency: the technical concrete lens still
called one model call plus a shell command the strongest simpler baseline, and
the trace excluded it as a counterexample by definition. The opener now names
the competent challenger, preserves existing grants and bounded recovery, and
makes conventional preference explicit. The Problem and Summary overlays had
also replaced that choice with an abstract stack-first framing; both active
operations now preserve the concrete failure, ordinary controls, workload
conditions and merge/removal consequence. Their IDs stay stable; frozen reader
copies are unchanged.

Four changed scanner candidates were reviewed against the existing core and
four retired dispositions preserve exact source/text/review lineage. There
remain 4,064 atoms and 4,205 reviewed prose candidates. Core and recorded formal
and family evidence sections stay literal. Contribution-focus/prior-art/novelty
checks pass. Actual local Human and AI views display the revised choice rules,
and the Human opening pixels were inspected. This is not a comparative
experiment, independent reader/author approval, novelty decision, accepted
support movement or public release. I05's editorial criterion is verified;
I03's wider novelty-language reconciliation and I04's claim-directed refresh,
plus remaining manuscript and publication criteria, stay open.

## Full World Models source review — 2026-10-11

Reviewed the complete technical chapter: argument, ordinary alternatives,
worked reconciliation, predictive/causal/uncertainty mechanisms, relation and
abstraction lifecycle, interfaces, invariants, failures, implementation horizon,
campaign, outcome boundaries, formal scope, source crosswalk and handoff. The
concrete scene is now explicitly hypothetical. Forecast, admitted sensor report,
uncertain belief, current grant, selected/attempted stop and qualified later
outcome are distinct; a lost reply leaves an unknown effect. Admitted readings
cannot certify reality, and absence of an acknowledgement cannot establish no
motion. Attribution and prevention remain unproven.

The ordinary reactive controller may supply the same bounded stop with its own
observation checks and event log. Stable directly observable work may need no
learned world model. Logical responsibilities may share a conventional
implementation; equal or better ordinary behavior at lower burden narrows,
merges or removes the proposed machinery. Predictive-use qualification cannot
issue a grant, model replacement cannot erase permitted history, and an
outside observer may share sensors or other failure paths. Reopening a lossy
abstraction requires retained permitted detail; a stop/hold/fallback needs a
qualified feasible response and can carry residual risk.

Six existing manifest design rules were clarified. Exact earlier/current
wordings remain below as editorial lineage; these changes establish no live
policy or new formal result.

| Existing rule | Previous wording | Current wording |
|---|---|---|
| mechanism 5 | Admit imagined rollouts to planning only inside tested support and authority envelopes. | Admit imagined rollouts for declared planning uses only inside qualified predictive-use envelopes; current effect permission is checked separately. |
| mechanism 8 | Retain counterfactual receipts linking decisions to model version, observations, alternatives, and uncertainty. | Retain permitted forecast and counterfactual-scenario receipts linking decisions to model version, observations, considered alternatives and uncertainty; these records do not identify unobserved causal outcomes. |
| invariants 3 | Observation can override imagination and trigger replanning. | Qualified observations can defeat a forecast for an affected use and trigger replanning; admission does not prove measurement truth or complete coverage. |
| invariants 6 | Counterfactual comparisons use compatible state and intervention semantics. | Counterfactual-scenario comparisons use compatible state and intervention semantics; a causal counterfactual claim additionally requires its identification assumptions. |
| invariants 7 | Reality residuals are preserved rather than averaged away. | Material residuals are preserved within permitted history and routed for affected uses rather than averaged away or erased by a new model. |
| invariants 8 | A reachable safe action exists when predictive confidence collapses. | Consequential predictive use requires a qualified response to confidence collapse with feasible control, current permission and explicit residual risk; no universally safe action is assumed. |

The source status/frontmatter now agree with fifteen current manifest
assignments and their queue roles. This is metadata reconciliation, not fifteen
fresh passage reviews. A selected arXiv v6 conformal follow-up is recorded in
the existing note with sections, assumptions and no local result. Measured
calibration, marginal coverage, pointwise coverage and planner-selected use
remain distinct; changed assumptions remove inherited eligibility rather than
prove coverage failure. No source was added.

The two revised diagrams have complete preceding text, separate predictive-use
and runtime admission, separate observation and belief, titled/described native
charts and keyboard-scrollable frames. The older relation diagram combined
observed/executed state and could suggest an invalid confidence ladder; the new
chart concerns assertions only and explicitly preserves the finite proof's
original scope. The implemented record contract is distinct from the proposed
live harness. Completing this book does not require executing the future
scientific campaign.

Core, the complete prospective campaign, evidence/outcome boundaries, test-plan
and formal sections remain literal. Proofs, schema, fixture and protocol hashes
remain unchanged; protected outcomes stay closed. This post-activation owner
is intentionally excluded from the frozen P1 scanner, so its source review
creates no new P1 atom, candidate or disposition: the registry remains 4,064
atoms and 4,205 reviewed prose candidates. No active reader overlay targets this
owner. Current reader text remains 26 units and 151,093 words; only parent
bindings were regenerated. This is assistant editorial work, not independent
reader/author approval, empirical efficacy, support movement or release.

Selected local HTML verification covers the Human diagrams at 1,280 pixels,
320 pixels and doubled text at 390 pixels, plus the AI worked trace at desktop
width. Both charts have titles/descriptions and labels approximately 21.55 and
20.82 pixels; keyboard horizontal scrolling works without page-wide overflow.
The relation canvas was widened after actual measurement found 17.69-pixel
labels. Human mode intentionally hides the technical status table; the fifteen
source assignments were checked in AI mode. Diagram and worked-trace pixels
were inspected. The selected page resolves 150 local links/anchors and preserves
its worked/ownership/observation/formal anchors; one configured Relational
Dimension Compiler paper is absent from the partial preview and remains
unverified as a rendered link. No full-site, assistive-technology or learner
qualification follows. Book/source/reader/quality/frozen-registry and owner
integration consistency checks pass; no Docker, Lean rebuild, predictor or
scientific campaign was run.

## I03 contribution-type completion audit — 2026-10-11

I03 requires each defended result to identify whether it is a new mechanism,
a composition, a public evidence process, or an implementation/evaluation
result, with antecedents and a useful delta. It does not require independent
proof of novelty or execution of the future comparison. The current portfolio
selects three proposed targets rather than three established discoveries.

| Original requirement | Inspected evidence | Completion consequence |
|---|---|---|
| Contribution type matches what has been demonstrated | All three generated `contribution_type` values; all three bounded `exit_ladder` slices/ceilings; contribution summary; exact August 13 P5-U1 result identity, aggregate, maximum inference and nonclaims | Summary now separates each composition/process proposal from its implementation or consistency evidence. No new authorization primitive, belief-revision calculus, logging method or program-level novel mechanism is asserted. |
| Cite antecedents and state the delta without dismissing them | Three conventional challenger blueprints; existing capability, PCC, Model Cards, AGM, TMS, in-toto, PROV-O, zero-trust and NIST incident notes at their recorded intake depths | The result map links those notes, names the decision relation and consumer, and distinguishes metadata positioning from reviewed selected passages. Existing implementations may carry the same joins. No absence-of-prior-art certificate or refreshed efficacy is inferred. |
| Synthesis is defended through useful joins rather than renaming familiar patterns | Current prospective comparison deltas/equality dispositions; exact scope of the three ablations; nine signature-idea rows, claims, deltas, objections and confidence states | Current grant/candidate/effect/recovery, exact claim/evidence/inference/review, and challenged report/observation/residual relations remain the proposed value. The summary clarifies `distinctive_mechanism_ablation` as experimental-condition separation; the ledger types its nine supporting ideas without claiming nine new mechanisms. |
| Author publication does not independently establish novelty | Current introduction/paper-library boundary, portfolio owner and revised ledger classification | The author manuscripts retain lineage and their original claims. Publication is not a novelty decision, reproduction or accepted support. |

A lexical screen covered the 89 technical owners, finding 166 relevant mentions
across 61 owners. These include task novelty, source-attributed terminology,
nonclaims, future comparative targets and different senses of uniqueness.
Potential contribution-wording contexts in the data, operations, methodology,
compression and research-agenda owners were inspected rather than imposing a
word ban. Eleven targeted current-reader hits were inspected in context;
the active overlay scan produced no matching contribution-language hit. This
screen is not a full semantic review of 89 chapters or proof that every possible
implicit novelty claim is absent. The completion decision rests on the three
actual defended targets and their exact proposal/result/antecedent relations;
remaining manuscript and terminology criteria stay open.

The three-contribution summary now includes a result/antecedent map and removes
ambiguous “distinctive mechanisms” wording from the replay explanation. The
novelty ledger adds a nine-row contribution interpretation while preserving
its machine ledger byte-for-byte, including dated assessments and confidence
states. The generated portfolio and all frozen ladder wording also remain
byte-identical. Seventeen local Markdown/artifact references resolve; no fresh
published-HTML inspection is claimed. Existing portfolio, prior-art and novelty
consistency checks pass. No chapter, claim atom, source intake, proof, empirical
result, review approval, support or release was changed. I03's editorial
criterion is verified, bringing the current total to 29 of 114; I04's
claim-directed refresh and wider I/J/K/manuscript/publication work remain open.

## Control-spine outline ownership reconciliation — 2026-10-11

J01 remains open. The current outline has all 89 manifest headings and chapter
jobs, but job presence alone does not establish clear input/output or overlap
boundaries. A keyword diagnostic found 32 chapter-level boundary markers; that
is not a conclusion that the other 57 chapters lack meaningful ownership.
The authoritative current job text and manifest interfaces were inspected,
with a selected control-spine interface reading for the 15 entries below.

A substantive defect was found: the opener's drafting arc claimed “durable
artifact identity, derivation, record-reality custody, replay grade, and impact
closure” and then supplied an eighteen-step Artifact Graphs mechanism. That
block does not describe the thesis owner's job. It is replaced by the stack
argument, common handoff questions, competent ordinary alternatives and
conditions for earning the extra burden. Artifact/replay and joined-trace
responsibilities remain with their actual owners, whose source/outline
mechanisms are preserved.

Fifteen existing outline jobs now state a concrete decision, input/output
boundary and semantically selected overlap links:

| Owner group | Decisions kept distinct |
|---|---|
| Thesis, efficiency, authority and evidence | Stack argument vs joined trace; efficiency hypothesis vs cost accounting and route selection; exact current permission vs its runtime enforcement; accepted support meaning vs durable claim history |
| Human Intent, conformance and Planning | Contestable request interpretation vs stage-specific conformance vs obligation order/capacity/revision. Applicable grants remain usable, credential feasibility differs from permission, and an unknown effect cannot be rearmed by planning. |
| World Models and Compilation | Predictive-use qualification and forecast/observation discrepancy vs deployment-conditioned evidence ancestry; translation of accepted obligations vs source-method transport qualification |
| Context ABI, Verification Bandwidth and Claim Ledgers | Actual packet conformance vs dynamic state consistency vs verification adequacy; semantic claim/surface continuity vs support decisions and general artifact custody |
| Artifact Graphs, Runtime and Integrated Architecture | Artifact identity/replay/affected-use custody vs actual effect attempt/observation/recovery vs the relation joining independently owned stages |

The writing guide now routes a new source or bug by the first disputed meaning
or decision rather than source count or adjacency. A source can inform several
existing owners; a genuinely new responsibility still follows the established
admission contract. These are logical responsibilities, not required separate
services or a promise that the mature systems exist.

All 89 unique jobs and stable IDs remain. The 15 clarified entries have 27
valid local chapter overlap references; their source queues and core-claim
paragraphs are literal. The other 74 outline chapter entries remain exact,
and canonical chapter prose, manifest order/IDs, claims, proof/evidence targets,
current reader text and frozen custody are untouched. A formatting check also
preserves complete hyphenated names rather than introducing “Intent-to-
Execution” or “node- local” variants. Scaffold checks report no rebuild. This
is a scoped authoring-outline correction, not full semantic approval of all 89
chapters, learner evidence, a runtime result, support movement or release. The
remaining 74 owners and final reader-facing consistency still require the same
responsibility reconciliation; no new catalog criterion is marked verified.

## Governance, security and replacement outline boundaries — 2026-10-11

This continuation reconciles 27 additional outline ownership entries against
their current chapter interface prose and manifest jobs. Standalone field-name
inventories were excluded from the interface reading; meaningful prose, role
handoffs, tables and limitations remained. This is responsibility review, not
full argument/source/result reapproval of those chapters.

| Owners | Decision boundary clarified |
|---|---|
| Failure map, dangerous domains and military systems | Prospective failure classification vs domain/actor uplift measurement vs composed command, physical action and strategic interaction. Detection, threshold response and institutional authority remain separate. |
| Scalable Oversight, Human Factors and Communication | Inspection protocol and evidence views vs live human capacity/intervention vs outbound influence and correction after distribution. A vote, nominal approval, persuasive explanation or delivery receipt establishes none of the other properties. |
| Constitution, moral conflict, learned-objective integrity, objective formation and institutions | Exact constraints vs unresolved disagreement/rights duties vs defeasible policy hypotheses vs approved operational targets/proxies vs public mandate and participation. No layer self-certifies legitimacy or repairs missing authority. |
| Societal Resilience | Multi-organization defense, recovery and remedy differ from the operator’s incident loop and the threat measurement; defensive capacity alone does not justify release. |
| Stable Capability Fields and Replacement | Consumer-relative substitution identity differs from the transaction that changes an implementation and separately records restoration, observed performance, compensation and unknown effects. |
| Kernel, model attacks, privacy and protected computation | Threat-bound flow/effect mediation vs learned-behavior attack lifecycle vs permitted purpose/rights/remedy vs separately appraised privacy, computation integrity, platform identity and output authenticity. |
| Weight custody, open release and supply chain | Possession/copy/key/load/retirement state vs deliberate irreversible distribution vs integrity of exact lifecycle subjects and relations. Attestation, provenance, signatures and valid packets do not transfer the neighboring decision. |
| Recursive improvement, open-ended engines and replication | Self-change admission vs adaptive task/candidate/archive campaigns vs the composed creation/persistence/recall of descendants. Routine updates inside an applicable lease do not need repeated permission; material governor changes remain separate. |
| Perception, reflexive model/world systems and method transfer | Qualified fallible observation vs deployment-conditioned evidence ancestry vs qualification of method transport before ordinary translation or procedure promotion. Sensor admission, on-policy outcomes and compiled package shape remain distinct from truth, independent grounding and transferred efficacy. |

Each revised entry states its decision, inputs, outputs, boundaries and two
semantically chosen overlapping owners. Its 54 local chapter links resolve.
The earlier 15 control-spine entries plus these 27 make 42 explicitly clarified
outline entries, with 47 still to reconcile. An initial substring diagnostic
also counted a pre-existing CoilRA draft-arc bullet; anchored matching of the
actual ownership paragraph/overlap fields excludes that false completion.
No job or ownership conclusion is inferred from keyword presence alone.

All 89 stable IDs/jobs remain. The revised 27 source-loading queues and core
paragraphs are literal, and the other 62 entries—including the earlier 15—are
unchanged from this continuation's baseline. Canonical chapter prose, manifest,
claims, proofs, experiments, source assignments, current reader and frozen
custody are untouched. Formatting preserves complete specialized names. Source
consistency requires no scaffold rebuild. J01 remains open for the remaining
47 entries and final reader-facing reconciliation; J05/J06's broader scopes,
independent/author approval and publication remain separate. Verified catalog
completion stays 29/114. No Docker, scientific run, live governance outcome or
support movement is introduced.

## Memory, work, training and representation outline boundaries — 2026-10-11

Reviewed the current interface prose, role handoffs, tables and limitations for
24 further owners, excluding standalone field-name lists. Their existing outline
jobs now state a concrete decision, input/output boundary and two nearby
responsibilities. This is ownership review, not full argument/source/proof or
outcome reapproval.

| Owners | Distinct decision retained |
|---|---|
| Durable Memory and Context Transactions | Persistent semantic objects, ontology and retrieval vs participant/fault-bound state changes and snapshots. Context packet conformance, checking adequacy, support and model forgetting remain separate. |
| Proof-Carrying Claims and Labor OS | Claim-specific verification/review route and bounded verdict vs authorized work-unit lifecycle and delivery. Neither verdict, worker exit nor evidence-readiness eligibility promotes a claim or permits an effect. |
| Work Surfaces, Organizations, Symbiosis and Deployment Transition | Technical expansion/custody vs internal decision rights/remedy vs longitudinal human coupling/exit vs population/time-bound distribution of benefits and burdens. |
| Embodied Agency, Inter-Stack Protocols and Multi-Agent Dynamics | Plant/timing/control envelope vs pairwise peer contract vs emergent population incentives and cascades. Software restoration, interoperability and local compliance do not settle the other layers. |
| Procedural Memory, Routing, Substrates and relational compilation | Qualification of reusable work vs eligible selection vs interchangeable learned-kernel boundary vs role-sensitive relation/operator lifecycle. All retain separately owned permission, support and current-use decisions. |
| Governed Training, Learning-Compute Topology and Scaling Science | Faithful run/checkpoint/data-consumption transaction vs organization of adaptive identities/evidence/credit vs assumption-bound prediction and generalization tests. |
| Readiness and Personal Hives | Exact use eligibility/quarantine vs placement/custody across governed nodes and peers. Reachability and spare capacity are not permission or evidence. |
| Compact Systems, Fast Generation, Deliberation and RankFold/NeuralFold | Consumer-relative representation admission/residual accounting vs request-specific low-latency generation vs leased additional inference/search vs concrete codec/reconstruction/access-pattern candidates. |

The new 48 local chapter overlap references resolve. All 89 jobs/stable IDs
remain; 24 source queues and core paragraphs are literal, and the other 65
entries retain exact bytes from this continuation's baseline. Anchored ownership
paragraphs and overlap fields now cover 66/89 outline entries. The remaining
23 entries and the final source/reader-facing reconciliation remain open.
Canonical chapter prose, manifest, claims, proof/evidence records, current
reader and frozen custody are unchanged; scaffold checks need no rebuild.

### Canonical interface ambiguities identified before repair

This reading identified source sentences whose grouped roles or legacy aliases
can contradict the explicit outline split. The following are retained as
the pre-repair J01/J05 findings; no completion was inferred from the outline
fix. The subsequent scoped repair below preserves claim, scope, accepted
evidence, finite-proof and current-reader boundaries through their existing
review and digest owners.

| Existing source | Wording needing disambiguation | Canonical distinction to preserve |
|---|---|---|
| [Durable Memory, Interfaces](../chapters/durable-semantic-memory-and-knowledge-lattices.qmd#interfaces) | “Claim Ledgers owns belief support and revision” | Claim-semantic identity and belief history differ from Evidence States’ accepted support-transition meaning. |
| [Context Transactions, Interfaces](../chapters/context-transactions-snapshots-mounts-and-taint.qmd#interfaces) | Groups Claim Ledgers and Spinoza under evidence, belief and support transitions; assigns jobs/approvals to Runtime | Separate claim continuity, verification verdict, support decisions, job lifecycle, approval authority and actual effect mediation. |
| [Procedural Memory, Interfaces](../chapters/procedural-memory-and-cognitive-loop-closure.qmd#interfaces) | Assigns semantic memory state to Context ABI/Transactions and support to Claim Ledgers; uses “Evidence Engineering” | Durable Memory stores semantic objects; transactions change state; the ABI materializes packets; Evidence States decides support. Procedure qualification remains separate. |
| [Routing, Interfaces](../chapters/routing-heads-and-specialist-cores.qmd#interfaces) | Groups Verification, Spinoza, Artifact Graphs and Evidence as owning result support | Mode-specific verification, artifact custody and accepted support decisions are separate; the route cannot adjudicate its own result. |
| [Inter-Stack Protocols, Interfaces](../chapters/inter-stack-protocols-identity-and-economic-exchange.qmd#interfaces) | Assigns originating intent to Intent-to-Execution; uses “Evidence Engineering” and broad context ownership | Human Intent interprets; conformance preserves accepted scope; the protocol carries exact references rather than certifying context, effects or support. |
| [Readiness, Interfaces](../chapters/readiness-gates-residual-escrow-and-quarantine.qmd#interfaces) | Groups Claim Ledgers/Artifact Graphs under support and Inter-Stack Protocols under effects | Lineage, claim continuity, support, eligibility and runtime effects must retain their exact owners. |
| [Fast Generation, Interfaces](../chapters/fast-generation-architectures.qmd#interfaces) | Groups Claim Ledgers and Readiness under evidence transition | Evidence States accepts support transitions; claim and readiness consumers retain continuity and use eligibility. |

These are semantic wording findings, not proof that an implementation behaves
incorrectly. They require source/manifest/overlay review rather than a global
word replacement. The scoped repair is recorded below. J01 remains open
despite the 66-entry outline progress; J05
and J06 also retain their broader scopes. No scientific run, Docker, source
intake, support movement, independent/author approval or release is added.
The verified catalog total remains 29/114.

## Canonical interface ownership repairs — 2026-10-11

Repaired all seven wording findings in the immediately preceding review. The
sixteen existing manifest interface rules and their canonical prose now agree
on the following decisions:

| Owner | Existing interface rules clarified | Resulting boundary |
|---|---|---|
| [Durable Memory](../chapters/durable-semantic-memory-and-knowledge-lattices.qmd#interfaces) | 003 | Claim identity/belief history vs accepted support; memory stores referenced objects. |
| [Context Transactions](../chapters/context-transactions-snapshots-mounts-and-taint.qmd#interfaces) | 005, 007, 011 | Claim continuity, scoped verification and support; typed-job dispatch, current grants and effects; use eligibility and release retain separate decisions. |
| [Procedural Memory](../chapters/procedural-memory-and-cognitive-loop-closure.qmd#interfaces) | 002, 003, 007 | Persistent objects, state changes and packets; claim history vs support; bounded checks/proofs cannot award support to a procedure. |
| [Routing](../chapters/routing-heads-and-specialist-cores.qmd#interfaces) | 001, 004, 007 | Intent interpretation, accepted scope and work ordering; persistent objects/snapshots/packets; verification, custody and support. Routing requests eligible references without granting itself access. |
| [Inter-Stack Protocols](../chapters/inter-stack-protocols-identity-and-economic-exchange.qmd#interfaces) | 001, 005, 006 | Human interpretation vs accepted scope; packet/state/access decisions; artifact identity/custody vs support. Exchange completeness does not certify truth or permission. |
| [Readiness](../chapters/readiness-gates-residual-escrow-and-quarantine.qmd#interfaces) | 004, 005 | Claim history, lineage and support; job dispatch, effect mediation and work under grants. Peer requests/responses do not prove completion. |
| [Fast Generation](../chapters/fast-generation-architectures.qmd#interfaces) | 011 | Claim continuity, accepted support and use-specific qualification/expiry/quarantine are separate; no-change outcomes remain recorded. |

The same clarification is included in Routing's existing active Human-view
Interfaces replacement. Other overlays on these owners do not replace the
corrected interface passages. The 75 active operations retain their IDs and
apply mechanically; this does not imply a new semantic review of all 75.
Fourteen selected local desktop chapter/view pairs display the corrected
interfaces in both Human and AI modes, with no page-wide overflow or script
errors. The Routing Human-view screenshot was also inspected. These observations
cover selected rendered prose, not a fresh full-site or mobile/accessibility audit.

Each revised rule retains its exact prior/current text in its existing claim
review's wording lineage. Three new scanner candidates were read in their
surrounding paragraphs and mapped to existing interface atoms; three retired
reviews retain exact sentence, source and disposition. Registry totals remain
4,064 atoms, 4,205 candidates and 64 dossiers. The seven editorial packets and
current-reader parent bindings are refreshed; the 26-unit manuscript remains
151,093 words. Only Interfaces prose and manifest interface strings changed:
all other canonical sections and manifest fields are literal, including core,
source assignments, formal boundaries and recorded campaigns. Generated proof
references now point to the revised outline's current lines; all target/module/
status/property fields are unchanged. No proof code or proof run changed.

Book, claim registry, all 89 editorial packet bindings, current reader, overlay
mechanics and scaffold consistency pass. The active-roadmap baseline passes.
The seven source wording findings are closed at this editorial scope. J01
remains open for the other 23 outline entries and final source/reader-facing
reconciliation; broader J05/J06 scopes remain open. Verified recommendations
remain 29/114. This scoped review adds no full chapter/source/proof review,
scientific outcome, support transition, independent or author approval, or
publication decision. No Docker or empirical campaign was used.

## Final outline owner boundaries and two interface repairs — 2026-10-11

Read the current interface prose, tables, handoffs and limitations of the final
23 owners, excluding standalone field-name inventories. Their outline entries
now distinguish the following decisions, inputs, outputs and nearest overlaps:

| Owners | Decision boundary clarified |
|---|---|
| Resource Economics and Physical Infrastructure | Allocation and the complete bill vs deliverability, correlated failures and burdens at a place and time. Planning requests resources; Operations commands incidents. |
| Mathematical Substrates, Circle, Coil and CoilRA | General axis-specific adoption vs formal-fact transport vs state-carry/reuse vs evaluation of particular cyclic encoding/mixer candidates. Structure is separate from task quality and hardware cost. |
| Proof Envelope, Benchmark Ratchets and White-Box Evidence | Authorized formal interpretation/refinement vs instrument validity vs method-relative capture/intervention evidence. None decides accepted support. |
| Capability Thresholds, Adversarial Evaluation and Safety Cases | Predeclared assessment-to-response commitment vs context-conditioned observation integrity vs compilation of support/challenge relations. Their decisions remain separate from use admission and release. |
| Content Authenticity and Governed Operations | Output/edit provenance and signal limits vs live containment, degraded operation and effect reconciliation. Authenticity does not prove depicted truth; compensation does not reverse harm. |
| Adjudicated Persistence, Policy Optimization and Data Engines | Whether/where a lesson should persist vs bounded update candidates vs data/state custody and separately scoped deletion/influence evidence. |
| Scientific Discovery and Artifact Stewardship | Prospective design-to-inference bridge vs accountable project continuity. Planning and support/publication authorities retain their own roles. |
| Theseus, Prototype Roadmap, Living Book and Research Agenda | Exact inspected implementation report vs phase admission/termination vs applied editorial/publication change custody vs intake/closure of new sources, defects and research needs. |

All 89 ordered entries now have explicit ownership boundaries and nearest-owner
references, with 175 resolving local overlap links. The final 23 entries add 46
of those links. Reversing only their new job/boundary/overlap paragraphs yields
the exact previous entry bytes; the other 66 entries are literal. Stable IDs,
order, source queues, core claims and proof tables are preserved. The outline
header records the full 89-owner clarification scope.

The source reading also exposed two concrete Interfaces ambiguities, now
repaired rather than left behind an outline-only clarification:

| Existing owner | Prior ambiguity | Corrected passage and existing manifest rules |
|---|---|---|
| [Resource Economics](../chapters/resource-economics-and-token-budgets.qmd#interfaces) | Planning “allocates budgets”; a Resource Budget Record is described as the allocation owner. | Planning requests resources and schedules within admitted allocations; Resource Economics owns allocation decisions/leases; the record carries their terms and actuals. Interface rules 001 and 002 retain exact prior/current wording lineage. |
| [Adversarial Evaluation](../chapters/adversarial-evaluation-sandbagging-and-training-time-deception.qmd#interfaces) | SCF and Evidence States are grouped as promoting, quarantining or narrowing a claim. | Capability identity, current-use qualification/quarantine, claim continuity and accepted support retain separate owners. A discrepancy supplies an input to the appropriate review and moves no state automatically. Interface rule 005 retains exact prior/current wording lineage. |

Only these two canonical Interfaces sections and three manifest interface rules
changed. All other sections/manifest fields, source assignments, cores, proof
boundaries and recorded campaigns are literal. One changed scanner fragment was
reviewed in its surrounding qualification/support paragraph and mapped to the
existing readiness-consumer interface; its retired source/text/disposition is
retained. Two editorial packets and current-reader parent bindings are updated.
Registry totals remain 4,064 atoms, 4,205 prose candidates and 64 dossiers; the
26-unit current manuscript remains 151,093 words. Generated proof references
now follow the current outline lines, with all target/module/status/property
fields unchanged and no proof code or proof run changed.

Resource Economics' active overlay replaces only Minimum Viable Implementation;
Adversarial Evaluation has no overlay. Four selected local desktop Human/AI
chapter/view pairs display the corrected interfaces, with no page-wide overflow
or script errors. These are selected prose checks, not a full-site or mobile/
accessibility review. Book, claim registry, all 89 editorial bindings, current
reader and scaffold consistency pass; scaffold generation needs no changes.
The active-roadmap baseline passes. No Docker or empirical campaign was used.

The outline criterion is now authored for all 89 owners; J01 remains open for
final source/reader-facing routing reconciliation, including the active Human
interface explanations and the current narrative owner introductions/handoffs.
The review must check whether a reader can route a new source or defect to the
first disputed meaning/decision; counts and resolved links alone do not prove
that semantic criterion. Broader J05/J06 and the goal remain active; verified
recommendations stay 29/114. This pass does not add full argument/source/proof
reapproval, support movement, independent/author approval or release.

## Reader-facing owner guide and active interface reconciliation — 2026-10-11

The authored outline boundaries are now exposed on the maintained
[reader landing](../editions/reader_manuscript/current/index.qmd#find-an-owner).
The existing reader producer derives each owner's concise job, input/output
boundary and nearest overlaps directly from `docs/book_outline.md`, groups the
89 owners under their 26 narrative units, and links the narrative and exact
technical responsibilities. Native expandable disclosures keep this reference
out of the main reading path. The reader manifest binds the exact source-outline
bytes; unknown/duplicate owners, missing role fields, invalid neighbors or
coverage/order drift reject generation. No new chapter or routine report was
created. These are authored roles, explicitly distinct from demonstrated
implementation, scientific support and required service boundaries.

Read all ten active Human-view Interfaces replacements for ownership meaning:
Proof Envelope, Virtual Context ABI, Intent-to-Execution, Evidence States,
Compact Systems, Benchmark Ratchets, Circle, Spinoza, Routing and Living Book.
This covers those replacement passages, not all 75 overlay operations or all
canonical chapter arguments. The VCM replacement retained one stale sentence
assigning support/promotion to Claim Ledgers. Its existing operation now assigns
claim identity, contradiction records and belief history to Claim Ledgers,
accepted support to Evidence States, and bounded verdicts to Spinoza. Operation
IDs are unchanged; the existing VCM editorial packet records the exact scope.
Canonical chapter text, claim registry/candidates, core and proof/evidence
boundaries are unchanged. Ten replacements were read; only this one changed.

Actual local rendering displays all 89 jobs and boundaries in the landing's
26 disclosures. Its 264 technical-owner/neighbor links resolve to retained
rendered technical pages. The 26 narrative links resolve to current authored
sources and their configured routes; the partial preview does not contain a
fresh whole-narrative render, so no 26-page HTML/link certification is inferred.
The browser link check initially counted Quarto's generated heading permalink
and then assumed locally rewritten narrative URLs were relative; those helper
assumptions were corrected. The resulting check explicitly distinguishes
retained technical HTML from narrative source routes rather than hiding the
partial-preview limit.

Six assistant routing walkthroughs used the exposed responsibility and nearby
boundary rather than chapter order or an author name:

| Disputed question | First owner and split inspected |
|---|---|
| Prose cleanup appears to improve a claim's support | Evidence States; drafting and claim identity cannot award support. |
| A new source concerns stale context snapshots | Context Transactions; durable semantic objects and static packet materialization remain separate. |
| A write was attempted but its external outcome is unknown | Runtime; planning and artifact custody cannot declare the effect absent or complete. |
| Elicitation conditions distort a benchmark result | Adversarial Evaluation; instrument validity and observation integrity are separate. |
| A portable theorem receipt has an unproved world-model relation | Circle for receipt delivery, with Proof Envelope as the adjacent adequacy/refinement owner; valid transport cannot resolve the model/world correspondence. |
| A capability assessment requires a prospective safeguard response | Capability Thresholds; benchmark measurement and operational admission retain their own decisions. |

The local reader landing also passes selected desktop, 320-pixel and doubled-
text 390-pixel disclosure observations: Enter opens, Space closes, and no
page-wide overflow or script errors occur. Desktop and narrow screenshots were
inspected. The corrected VCM Human replacement is displayed in the selected
rendered technical page. This is not an independent-reader study, complete
assistive-technology/accessibility qualification, fresh full-site render,
source/proof review, author approval or release.

The current 26 manuscript units remain 151,093 words; this reference guide does
not change their narrative word count. Reader generation and validation,
overlay generation/75 mechanical applications, all 89 editorial bindings,
book consistency and active-roadmap baseline pass. A role-co-occurrence screen
of current narrative source lines found no Claim-Ledger/support-promotion
candidates; that lexical result is not a semantic audit. J01 remains open for
review of current narrative introductions/handoffs against these exposed
owner decisions. Broader J05/J06 remain open; verified total remains 29/114.
No Docker, empirical campaign, support transition or publication was used.

## J01 ownership criterion completion audit — 2026-10-11

J01 asks for a concise distinct job, decision/failure, inputs, outputs, boundary
and nearest overlap for every technical owner, with confusing overlaps resolved
in prose. Its reader criterion is to explain why adjacent responsibilities are
separate and where a new source or defect belongs; source volume alone does not
create a chapter. The following evidence verifies that editorial criterion.

| Requirement | Current authoritative evidence | Scope and consequence |
|---|---|---|
| Distinct owner decision, input/output boundary and nearest overlap for every chapter | The [maintained outline](book_outline.md) has all 89 ordered entries and 175 resolving overlap references; the preceding four cohort reviews read current role/interface prose and retained literal cores/source queues/proof tables. | Decisions and consumer boundaries are authored individually; counts and links support coverage, not the semantic conclusion by themselves. Chapter IDs/order and the 89-owner manifest remain intact. |
| Adjacent responsibilities remain separable in prose | Nine canonical interface findings were repaired through 19 existing manifest rules, retaining exact wording/review lineage. All ten active Human Interfaces replacements were read; Routing's explanation agrees and VCM's stale support-owner sentence is corrected. | Claim continuity/support, interpretation/conformance/lowering, context objects/state/packets, verification/custody, job/grant/effect and eligibility/release decisions stay distinct. This does not reapprove whole arguments, sources, proofs or runtime behavior. |
| Readers can find the distinction | The [current reader guide](../editions/reader_manuscript/current/index.qmd#find-an-owner) projects all 89 authored jobs and boundaries into 26 native disclosures from byte-bound outline input. | Actual local HTML displays every role and boundary, with 264 retained rendered technical links and 26 source-resolving narrative routes. Six assistant routing walkthroughs and three disclosure/layout views exercise the guide. No fresh whole-narrative render or independent-reader study is inferred. |
| Narrative openings and handoffs agree with the owner route | This continuation read all 26 current substantive openings and “What This Establishes” conclusions, including their next-unit responsibilities and stated evidence ceilings. | Six passages in five units are clarified; the other 21 units remain literal, and every other section in touched units is preserved apart from EOF normalization. Five selected local narrative HTML pages display the changes. |
| New source/defect routing follows responsibility rather than volume or order | The outline writing rule and public reader guide start at the first disputed meaning/decision, preserve downstream responsibilities, allow a source to inform several owners, and retain the new-responsibility admission contract. | The final walkthrough corrects one earlier receipt-focused routing choice: an unproved model-to-world correspondence goes first to Proof Envelope adequacy/refinement review. Circle retains portable receipt identity/delivery. No new chapter or structural merge was proposed. |

The final narrative clarifications are specific:

| Current unit | Corrected ownership meaning |
|---|---|
| [Unit 6](../editions/reader_manuscript/current/chapters/unit-06-human-intent-control-and-epistemic-security.qmd#what-this-establishes) | Human Intent interprets; Intent-to-Execution preserves accepted-task conformance; Cognitive Compilation owns target lowering. |
| [Unit 15](../editions/reader_manuscript/current/chapters/unit-15-verification-bandwidth-claim-ledgers-and-proof.qmd) | Evidence States adjudicates scoped support; Claim Ledgers preserves identity and belief/revision history. The stop observation still needs an admissible basis. |
| [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd#what-this-establishes) | Training is conditional on a selected substrate being learned or adapted; choosing a deterministic route does not require learning. |
| [Unit 23](../editions/reader_manuscript/current/chapters/unit-23-generative-compression-and-cognitive-resource-economics.qmd#what-this-establishes) | Fast Generation admits a request-specific mode within qualified routes; Compact Systems owns consumer-relative representation admission, separate from a concrete codec family and overall allocation. |
| [Unit 26](../editions/reader_manuscript/current/chapters/unit-26-integrated-reference-architecture-project-theseus-and-the-living-research-method.qmd) | Readiness eligibility is separate from repository/release grants and approvals. Theseus reports exact inspected implementation facts; phase admission, project continuity, applied editorial/publication custody and research intake/closure keep distinct owners. |

The earlier guide walkthrough's fifth row inspected Circle's receipt boundary
and its neighboring Proof Envelope, but its question named an unproved world-
model relation. The final first-disputed-boundary audit corrects that initial
route to Proof Envelope rather than changing the question. Prior browser
observations are retained in the ignored local work area; the subsequent
walkthrough uses the corrected owner. Valid delivery cannot repair semantic
adequacy. This correction is part of the completion evidence, not a rewritten
scientific or frozen evaluation result.

The five edited units gain 72 words overall. The current manuscript remains
26/26 at target length and is now 151,165 visible words. Current reader
projections, status panels, guide counts and the owning roadmap word-count field
are synchronized; older 151,093-word receipts retain their dates and scope.
Canonical manifest bytes and narrative routing/outline remain unchanged.
All examples remain hypothetical and all recorded scientific/proof/evidence
boundaries remain with their original owners. No canonical claim/proof/source
or frozen reader/experiment state changes in this continuation.

Current reader, book consistency and all 89 editorial bindings pass. The five
changed narrative pages and current guide render locally; selected desktop
prose checks pass without page-wide overflow or script errors, and the Unit 26
conclusion screenshot was inspected. Guide disclosures still pass desktop,
narrow and doubled-text keyboard/layout observations. Overlay mechanics remain
75/75. These are source/selected-HTML and assistant semantic checks, not broad
accessibility, independent comprehension, source/proof rereproduction, author
approval or release qualification.

J01 is verified at its original editorial scope, superseding the earlier
continuation notes that held owner/narrative routing open. The current verified
catalog total is **30/114**. J02, J05, J06, J07 and the other active manuscript,
source and reader recommendations retain their full criteria. J01 does not
certify every use of terminology, all summaries or all manuscript arguments;
those remain separately owned. No Docker, empirical campaign, support
transition or publication was used. The full implementation goal stays active.

## JEPA, Platonic representations and H-Net source integration — 2026-11-02

The user identified, then confirmed, Balestriero and LeCun's October 29 preprint,
[Proving and Improving the Platonic Representation Hypothesis with JEPAs](https://arxiv.org/abs/2610.39302v1).
The book already held a bounded V-JEPA 2 note and some latent-prediction context;
it lacked explicit JEPA-family/H-Net treatment and this newer alignment result.
Five primary sources now have stable external IDs and passage-bounded notes:

| Source | Reviewed version and actual use |
|---|---|
| I-JEPA, Assran et al. | arXiv:2301.08243v3; image-context/target prediction, Transformer implementation, masking and EMA target recipe. |
| LeJEPA, Balestriero and LeCun | arXiv:2511.08544v3; predictive agreement plus SIGReg, distinct from teacher–student/stop-gradient recipes. |
| Original Platonic Representation Hypothesis, Huh et al. | arXiv:2405.07987v5; geometry-convergence hypothesis, measurement and information-preserving-observation limitations. |
| Platonic representations with JEPAs, Balestriero and LeCun | arXiv:2610.39302v1; selected theorem/assumption, spectral proof, view construction, alignment/sample comparison and limitation passages. |
| H-Net, Hwang, Wang and Gu | arXiv:2507.07955v2; learned byte-level hierarchy, boundary/dechunking mechanics, matched-data/FLOP results and implementation limits. |

The source notes enumerate selected passages; this is not a complete proof,
code or empirical audit of all five papers. The original PRH's v5 was checked
after an initial v3 read. The official H-Net README was inspected for project
identity; no implementation, model weights, training or benchmark was executed.
Raw primary HTML remains in ignored local research storage. Only authored
notes, metadata and the standard schema-bound intake/triage records enter the
repository. Those records route the material to existing owners before prose;
they do not introduce a new chapter or a duplicate report.

Three technical owners now teach the distinctions:

- [World Models](../chapters/governed-world-models-and-reality-grounding.qmd#jepa-predicting-a-representation-does-not-certify-the-world) starts from the gantry's information needs. Feature prediction, action-conditioned dynamics, representation alignment, causal grounding and permission remain separate. Camera pose can be nuisance for alignment and necessary for control. The external PRH is explicitly distinct from Sorenson's *Platonic World Model* semantic-constitution source.
- [Cognitive Substrates](../chapters/replaceable-cognitive-substrates-beyond-transformer-monoculture.qmd#predictive-objectives-and-learned-granularity) separates mixing operators, prediction objectives and learned sequence granularity. It explains I-JEPA, V-JEPA 2, LeJEPA and H-Net, including dynamic boundaries, nested processing, smoothing/dechunking and existing checkpoint/byte-custody obligations. JEPA can use Transformers; H-Net can use attention/state-space blocks and remains autoregressive. No reviewed source supplies a validated combined JEPA/H-Net model.
- [Learning Theory](../chapters/learning-theory-generalization-and-scaling-science.qmd#platonic-representations-conditions-before-convergence) states the theorem's finite-world, injective-rendering, shared-positive/marginal, population, fixed-dimension and uniqueness assumptions. The identity predictor excludes learned action-conditioned predictors. Spectral uniqueness does not silently transfer to LeJEPA's full-distribution constraint. The 42-fold comparison is a sample count for one alignment target, with different recipes, three texts per good-view sample and no earlier next-token checkpoint; the paper separately reports 14-fold text-token use. Neither is measured system speed or general task superiority. Caption grouping, image-captioner distillation and asymmetric tuning remain explicit limits.

Current [reader Unit 11](../editions/reader_manuscript/current/chapters/unit-11-governed-world-models-and-reality-grounding.qmd#jepa-features-and-platonic-agreement)
and [Unit 19](../editions/reader_manuscript/current/chapters/unit-19-routing-and-replaceable-cognitive-substrates.qmd#prediction-targets-and-learned-granularity)
have shorter explanations tied to their existing stories. The other 24 units
are untouched. The current manuscript remains 26/26 at target length and now
contains 151,555 visible words; its parent/source and guide projections are
synchronized. H-Net's reported FLOP advantages retain its implementation-dependent
training slowdown and variable-memory/batching limits. A future comparison is
not a prerequisite for this completed editorial intake.

Current source metadata is reconciled: 506 inventory records, 1,361 assigned
source/chapter pairs, and 95 Corben/local versus 411 external Appendix G/H
records. The three chapter assignment counts are 18, 58 and 17, respectively;
these are assignment counts, not counts of freshly reread papers. The existing
V-JEPA 2 note adds the substrate route with an explicit historical-review
boundary. Current queues, crosswalks, front matter and generated source/readiness
surfaces agree. All three core sections, test/formal sections and non-source
manifest fields retain exact prior content; scientific outcomes and frozen
custody are unchanged.

Learning Theory contributes three new scanner fragments: two bounded external
source reports and one restatement of the existing assumption/metric mechanism.
They were read in context and adjudicated without creating a material/support
atom. Registry totals are 4,064 atoms, 4,208 prose candidates and 64 dossiers,
with zero pending reviews. The two later-admitted owners remain outside the
frozen P1 discovery scope. Three editorial packets and the World Models source
binding are refreshed. The World integration check now compares unique exact
source IDs/counts against the current manifest instead of fixing the original
15-source denominator; an equal-count duplicate rejects. Its finite proof,
contract, protocol and closed-outcome checks retain their original scope.

Selected local rendering covers three technical additions in both reading
modes, two narrative additions and the updated reader landing. Initial visual
inspection found cramped table words at phone width. The new comparison alone
now uses an accessible named scroll region with readable-width columns. The
revised substrate page was checked again in both modes; desktop, 320-pixel and
doubled-text 390-pixel layouts allow keyboard horizontal panning without page-
wide overflow. Desktop and narrow screenshots were inspected. This is selected
HTML/layout verification, not whole-site, assistive-technology, independent-
reader, author or publication qualification.

Source-note/appendix/outline checks, current reader, book consistency, all 89
editorial bindings, claim registry and World integration pass. Proof outline
pointers are current while target definitions and proof code stay exact. No
Docker, model run, Lean rebuild, new scientific result, evidence-state
promotion or deployment was used. This advances the existing I04/L02 source
and manuscript work without completing their wider criteria. Verified
recommendations remain 30/114, and the full implementation goal stays active.

## Historical Phase 2 baseline (2026-07-04)

Last updated: 2026-07-04

This note records the current Phase 2 reader-manuscript baseline for the v1.0 roadmap. It is a review-control document, not a reader release record.

## Generated Baseline

Command run:

```bash
python3 scripts/build_reader_edition.py
```

Generated workspace:

- `build/reader_edition/`
- 44 chapters
- 49 generated files
- target formats listed by profile: HTML, EPUB, PDF, DOCX
- 224 live-only sections removed
- 44 human-only bridges unwrapped
- 44 raw core-claim markers removed
- 39 repeated support-boilerplate passages humanized
- 61 reader scaffold terms humanized
- 74 active reader-overlay operations applied; 2 retired semantic-representation
  operations skipped after the fold

Generated review files inspected:

- `build/reader_edition/READER_RELEASE_CHECKLIST.md`
- `build/reader_edition/companion_notes.md`
- `build/reader_edition/reader_delta_report.md`

Representative generated chapters spot-read:

- `build/reader_edition/chapters/asi-is-a-stack-not-a-model.qmd`
- `build/reader_edition/chapters/the-efficient-asi-hypothesis.qmd`
- `build/reader_edition/chapters/human-intent-as-a-formal-input.qmd`
- `build/reader_edition/chapters/system-boundaries-and-authority.qmd`
- `build/reader_edition/chapters/evidence-states-and-claim-discipline.qmd`
- `build/reader_edition/chapters/constitutional-alignment-substrate.qmd`
- `build/reader_edition/chapters/personal-compute-hives-and-federated-edge-intelligence.qmd`
- `build/reader_edition/chapters/intent-to-execution-contracts.qmd`
- `build/reader_edition/chapters/planning-as-a-control-layer.qmd`
- `build/reader_edition/chapters/verification-bandwidth-and-context-adequacy.qmd`
- `build/reader_edition/chapters/labor-os-and-typed-jobs.qmd`
- `build/reader_edition/chapters/runtime-adapters-tool-permissions-and-human-approval.qmd`
- `build/reader_edition/chapters/policy-optimization-and-learning-from-feedback.qmd`
- `build/reader_edition/chapters/artifact-steward-agents-and-living-project-governance.qmd`
- `build/reader_edition/chapters/compact-generative-systems-and-residual-honesty.qmd`
- `build/reader_edition/chapters/fast-generation-architectures.qmd`
- `build/reader_edition/chapters/rankfold-neuralfold-and-artifact-compression.qmd`
- `build/reader_edition/chapters/mathematical-and-search-substrates.qmd`
- `build/reader_edition/chapters/circle-calculus-and-proof-carrying-ai-contracts.qmd`
- `build/reader_edition/chapters/executable-specifications-and-lean-proof-envelope.qmd`
- `build/reader_edition/chapters/open-research-agenda-and-bibliography-plan.qmd`

## What Is Working

- The generated reader source now has a coherent front door for the book: the first chapter opens as architecture prose rather than live scaffold.
- The Efficient ASI reader overlay converts the route-outcome state table into narrative prose while keeping the canonical AI/research efficiency-accounting matrix and cost/quality/residual boundary in the live source.
- The Human Intent reader overlay converts the intent-intake state table into narrative prose while keeping the canonical AI/research intake-state matrix and intent-contract boundary in the live source.
- The System Boundaries reader overlay converts the permission-class table into narrative prose while keeping the canonical AI/research permission taxonomy and authority-transition boundary in the live source.
- The Evidence States reader overlay converts the claim-source contribution table into narrative prose while keeping the canonical AI/research source-boundary matrix and support-state discipline in the live source.
- The Personal Compute Hives reader overlays convert four table-heavy sections plus the minimum and mature endpoint sections into narrative prose for Human view and generated reader editions while keeping the canonical AI/research tables, implementation ladder, and protocol checklist in the live source.
- The Policy Optimization reader overlay converts method-family and external-literature tables into narrative prose while keeping the canonical AI/research comparison tables in the live source.
- The Artifact Steward Agents reader overlays convert autonomy, treasury, project-object, and mature stewardship endpoint material into narrative prose while keeping the canonical AI/research matrices and lifecycle-control checklist in the live source.
- Semantic Representation is now folded into Compact Generative Systems as Semantic Representation Leasing; its standalone reader overlay is retired, and future reader work should edit the compact chapter's reader path rather than a second semantic-representation chapter.
- The Command Contracts reader overlay converts validation-state and field-status tables into narrative prose while keeping the canonical AI/research state matrix and command-record vocabulary in the live source.
- The Planning reader overlay converts the plan-node lifecycle-state table into narrative prose while keeping the canonical AI/research state matrix and planning-control boundary in the live source.
- The Verification Bandwidth reader overlay converts the adequacy-state table into narrative prose while keeping the canonical AI/research adequacy-state matrix and context/claim verification boundary in the live source.
- The Runtime Adapters reader overlay converts the effect-receipt field table into narrative prose while keeping the canonical AI/research receipt-field matrix and effect-boundary vocabulary in the live source.
- The Fast Generation reader overlay converts metric-code and taxonomy-table material into narrative prose while keeping the canonical AI/research formulas and generation-mode matrix in the live source.
- The Generate-Verify-Repair reader overlay converts the compression-receipt state table into narrative prose while keeping the canonical AI/research receipt-state matrix and exactness/repair/fallback boundary in the live source.
- The RankFold/NeuralFold reader overlay converts the artifact-compression admission-state table into narrative prose while keeping the canonical AI/research state taxonomy and probe/fallback boundary in the live source.
- The Mathematical and Search Substrates reader overlay converts the substrate-adoption lane table into narrative prose while keeping the canonical AI/research promotion-blocker matrix and optional-substrate adoption boundary in the live source.
- The Labor OS reader overlay converts the typed-job lifecycle-state table into narrative prose while keeping the canonical AI/research lifecycle matrix in the live source.
- The Circle Contracts reader overlays convert the proof-receipt lifecycle and mature proof-contract transport sections into narrative prose while keeping the canonical AI/research receipt-state matrix and target transport checklist in the live source.
- The Executable Specifications reader overlay converts the mature proof-envelope target checklist into narrative prose while keeping the canonical AI/research proof/spec registry and semantic-adequacy requirements in the live source.
- Human Reading Path bridges survive as ordinary prose, and reader-spine validation confirms all 44 chapters preserve Handoff continuity.
- Raw core-claim markers and repeated support boilerplate are stripped or humanized while the evidence boundary remains visible in the Core Claim prose.
- Source crosswalks, Codex test plans, drafting guardrails, and most live/research scaffolding are removed from the reader source.
- The reader delta workflow is in the correct shape: tracked overlays are the editable reader-delta source; generated reader files and generated delta reports are disposable review output.

## Automated Continuity Audit

The current generated reader source now has a deterministic heuristic audit at `docs/reader_continuity_audit.md`, generated by:

```bash
python3 scripts/audit_reader_continuity.py --write
```

The audit currently measures 44 reader chapters, 49 generated files, 117,713 reader words, 74 active and applied reader-overlay operations, 0 table rows, 53 Mermaid diagrams, 0 non-Mermaid code blocks, 0 paragraphs at or above 160 words, and 0 repeated first-sentence stems under the current eight-word heuristic. It identifies 0 high-priority and 0 medium-priority heuristic review chapters; the remaining queue is low-priority continuity review, not release approval.

This is review triage, not manual review. It creates a queue for the chapter-by-chapter human pass and helps decide whether a finding should become a canonical prose edit, reader-only overlay, companion-note treatment, or no action.

## Medium-Priority Manual Review

The current generated continuity audit has no high-priority or medium-priority heuristic rows. Four formerly active medium-priority rows have been read, classified, or handled in `docs/reader_continuity_review.md`.

- `executable-specifications-and-lean-proof-envelope`: no additional overlay now; the dense vocabulary is necessary proof-envelope language, and future reader release work should consider companion-note or glossary treatment rather than deleting the proof-lane distinctions.
- `circle-calculus-and-proof-carrying-ai-contracts`: no additional overlay now; the dense terms preserve the theorem-linked receipt versus model-quality boundary, and future reader release work should consider companion-note or glossary treatment.
- `artifact-steward-agents-and-living-project-governance`: retain current reader chapter; the long governance chapter carries central stewardship, treasury, worker-federation, contribution-ledger, event-taint, and sunset concepts. Future curated reader work may compress the implementation ladder or route parts to companion material.
- `compact-generative-systems-and-residual-honesty`: handled by a 2026-07-04 reader-only overlay tightening pass that reduced repeated receipt, record, and residual terminology while keeping exactness, fallback, consumer-policy, Lean/GVR, non-claim, and support-state boundaries visible.
- `artifact-graphs-audit-logs-and-replay`: handled by 2026-07-04 reader-only overlays for the record-reality Mechanism and strongest-objection sections, preserving independent observation, trap checks, challenge/replay routes, trust-base limits, remaining uncertainty, and no-promotion boundaries while keeping the generated reader queue at 0 high and 0 medium rows.

This manual pass does not make the reader manuscript release-reviewed. It only records that the medium-priority rows already reviewed are not immediate blockers for the generated reader path.

## Chapter Review Matrix

The durable Phase 2 queue now lives in
`editions/reader_manuscript/v1_0/chapter_review_matrix.json`, with the public
summary at `docs/reader_chapter_review_matrix.md`. Generate or validate it with:

```bash
python3 scripts/sync_reader_chapter_review_matrix.py --write
python3 scripts/sync_reader_chapter_review_matrix.py --check
```

The current matrix records 44 manifest-aligned chapter rows: 44 `reviewed`
rows from `docs/reader_opening_full_review_pass.md`,
`docs/reader_boundary_full_review_pass.md`, and
`docs/reader_normative_full_review_pass.md`, and
`docs/reader_part_i_full_review_completion.md`, plus
`docs/reader_part_ii_contracts_full_review_pass.md`,
`docs/reader_part_ii_context_full_review_pass.md`,
`docs/reader_part_ii_verification_full_review_pass.md`, and
`docs/reader_part_ii_full_review_completion.md`, plus
`docs/reader_part_iii_opening_full_review_pass.md`,
`docs/reader_part_iii_compression_full_review_pass.md`,
`docs/reader_part_iii_representation_full_review_pass.md`,
`docs/reader_part_iii_iv_proof_bridge_full_review_pass.md`, and
`docs/reader_part_iv_evidence_governance_full_review_pass.md`, and
`docs/reader_part_iv_completion_full_review_pass.md`. It has 0 `spot_checked`
rows, 0 `not_started` rows, 19 chapters with active reader overlays, 44 no-immediate-action decisions, 3 companion-note
candidates, and 44 curated-manuscript candidates. The reviewed rows have cleared
the `full_chapter_review_not_recorded` blocker, but all rows still retain
release blockers until reader release records and format artifact review exist.
The matrix is a chapter-text review queue and release-control surface, not a
reader release or format-artifact approval.

## Residuals

- The generated manuscript now has full chapter-text review records for all 44 chapters. That completes the generated-reader chapter-text queue, but it does not create a tagged reader release, a curated parallel reader manuscript, or reviewed format artifacts.
- The prose is still derived from the live AI/research book. It reads better than the live scaffold, but many chapters still carry technical interfaces, minimum-field lists, Mermaid diagrams, and implementation language that may need compression, rephrasing, or companion-note treatment for relaxed reading.
- Some reader chapters still contain useful but dense schema-like material. The current three companion-note candidates now have routing decisions in `docs/reader_companion_note_routing_review.md` and `editions/reader_manuscript/v1_0/companion_note_routing.json`, plus drafting companion notes under `editions/reader_manuscript/v1_0/companion_notes/`; a final human edition still needs release review before any generated companion notes, e-reader notes, or audio treatment can be approved.
- The original baseline had zero active overlay operations. That baseline has been superseded by the opening-chapter, Efficient ASI, Human Intent, System Boundaries, Evidence States, Personal Compute Hives, Command Contracts, Planning, Verification Bandwidth, Runtime Adapters, Labor OS, Circle Contracts, Generate-Verify-Repair, Fast Generation, RankFold/NeuralFold, Mathematical and Search Substrates, Policy Optimization, Artifact Steward Agents, and Executable Specifications reader-overlay operations in `docs/reader_overlay_pilot.md`; the standalone Semantic Representation overlay operations are retired after the fold, and broader reader-only prose pacing, example insertion, and section-flow edits remain open.
- No EPUB, PDF, DOCX, AZW3, MOBI, Markdown, plain-text, audio, or audio-embedded EPUB artifact has been rendered, reviewed, or released in this pass.
- No curated parallel reader manuscript exists yet. Graduation from generated source plus overlays remains a future decision once reader-only edits become too substantial for overlays.
- The automated continuity audit, reader chapter review matrix, and reader format review matrix are current, but none of them replaces reader-release records, broader layout/navigation review, curated-manuscript reconciliation, application/e-reader inspection, or format artifact approval.

## Next Review Pass

The next Phase 2 pass should:

1. Move from generated-reader chapter-text review into release-focused human-edition work: curated prose decisions, layout/navigation inspection, companion-note release review, and e-reader readability.
2. Classify each finding as a canonical live-book edit, a reader-only overlay, companion-note treatment, or no action.
3. Add reader-only semantic deltas under `editions/reader_overlays/v1_0/` only when the live AI/research source should not change.
4. Keep evidence boundaries, support states, implementation horizons, and non-claims inherited from the live book.
5. Render reader HTML, EPUB, and DOCX only after the manuscript review is recorded. Attempt PDF only when local dependencies support it, then update `editions/reader_manuscript/v1_0/format_review_matrix.json` from actual format-review evidence rather than render success alone.
6. Generate audio-script review output only after the reader manuscript is reviewed.

## Non-Claims

- This baseline does not claim a reviewed reader release exists.
- This baseline does not claim any ebook, document, PDF, audio, or audio-embedded EPUB artifact exists.
- This baseline does not promote any claim support state.
- The live AI/research book remains canonical for claims, support states, source boundaries, proof/test status, implementation horizons, and release records.

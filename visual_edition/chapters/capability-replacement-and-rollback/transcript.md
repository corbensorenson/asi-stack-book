# Descriptive transcript — Capability Replacement and Rollback

Canonical live chapter:
<https://corbensorenson.github.io/asi-stack-book/chapters/capability-replacement-and-rollback.html>

Video ID: `asi-video-capability-replacement-and-rollback`

Lifecycle: local pilot; no YouTube publication is authorized

Current support: `argument`

Claim label: `Design rationale`

## 00:00–00:39 — Not a component swap

**Visual description.** A candidate square approaches a bounded capability
field. Behind the visible model block, labeled chips name optimizer, scheduler,
random state, cache, policy, route, backup, descendants, and external effects.

**Narration.** A capable component is not a light bulb that can be unscrewed and replaced. It may carry model weights, optimizer and scheduler state, random-number state, caches, credentials, policies, routes, backups, descendants, and commitments already made outside the machine. A replacement can look successful while half of that world still belongs to the old version. This chapter therefore treats replacement as a governed transaction over one declared Stable Capability Field. The transaction names the prior implementation, candidate, consumers, authority, evidence, recovery objective, and every state or effect surface before the result is known.

## 00:39–01:18 — Freeze and inventory

**Visual description.** A gold lock labeled “FROZEN PROSPECTIVELY” closes over
prior and candidate identities. Twelve inventory rows light up; an omitted row
routes to a magenta residual.

**Narration.** The first discipline is prospective identity. Before evaluation, freeze the field version, prior and candidate digests, dependency graph, change class, checkpoint authority, evaluator, monitor, canary scope, thresholds, owners, and expiry. Then inventory state and effects. Model parameters are only one row. Optimizer, scheduler, random-number generator, cache, backup, credential, policy, receipt, data, route, monitor, descendant, and external commitment need explicit rows too. Effects are classified as reversible, replayable, compensatable, forked, disclosure-like, externally owned, or irreversible. Anything omitted cannot later be called recovered.

## 01:18–01:58 — Phase-gated lifecycle

**Visual description.** Numbered nodes connect proposed, precheck, shadow,
canary, commit, and monitor. Failures branch downward to rollback, compensation,
quarantine, and residual rather than disappearing.

**Narration.** The candidate then moves through explicit states: proposed, precheck, isolated shadow, bounded canary, default candidate, committed, monitored, rolled back, compensated, quarantined, or retired. Shadow and canary routes have bounded data, tools, writes, network access, learning, and external effects. Qualification includes usefulness, historical regressions, critical-failure vetoes, adversarial cases, authority and rights preservation, state compatibility, complete cost, and transfer. The candidate cannot be its own sole proposer, evaluator, promoter, monitor, incident judge, and rollback authority. Shared dependencies are recorded because independence is a property to measure, not a label.

## 01:58–02:42 — Monitor-triggered rollback

**Visual description.** Five percent of traffic reaches planning kernel B. A
delayed monitor turns to “critical regression,” closes the promotion gate, and
sends the route back to A. Local state is checked row by row; a remote-copy
hexagon remains outside the rollback boundary with a residual owner.

**Narration.** Imagine replacing a planning kernel. The current route is version A. Version B passes prechecks and enters a five-percent canary without permission to train descendants or mutate the default cache. A delayed monitor detects a critical regression. The stop condition prevents default promotion. Recovery restores the prospectively chosen checkpoint and route A, then compares every declared state surface with its recovery objective. A changed remote copy cannot be reversed locally, so the transaction assigns compensation and an owner instead of announcing success. The terminal receipt records the failed candidate, the rollback, the unresolved external effect, cost, and every affected descendant.

## 02:42–03:20 — Recovery is a vector

**Visual description.** Six paired statements use a large not-equal sign:
artifact versus state, restart versus behavior, digest versus privacy,
compensation versus reversal, receipt versus observation, and declared
inventory versus complete reality.

**Narration.** This example separates six commonly collapsed outcomes. Restoring artifact bytes is not restoring all state. Restarting a service is not recovering behavior. Digest equality is not privacy repair. Compensation is not reversal. A receipt is not independent observation. And one exact local inventory is not proof that the inventory was complete. The strongest failure modes follow directly: checkpoint hindsight, regression deletion, evaluator capture, canary contamination, monitor blindness, partial commit, forward-only migration, authority smuggling, rollback theater, irreversibility laundering, rollback cascades, and repeated promote-rollback trials that hide accumulated cost and residuals.

## 03:20–04:04 — Evidence ledger

**Visual description.** Three neutral ledger cards show `15/15 local trees`,
`32/36 rollback; 2/36 useful release`, and `35/35 named local surfaces`.
Below them, unresolved remote, external, privacy, and semantic surfaces remain
outside a double proof boundary.

**Narration.** The chapter has real but narrow evidence. One prospective local campaign restored fifteen of fifteen declared transaction trees exactly, while six best-versus-final checkpoint disagreements showed why checkpoint authority must be fixed in advance. Another attack-control campaign achieved exact rollback in thirty-two of thirty-six cases but admitted useful release in only two of thirty-six, below both release gates. A larger bounded inventory exercise restored thirty-five of thirty-five named local surfaces, while immutable corpus, feature, checkpoint, raw-evidence, simulated remote, and external-descendant surfaces remained unresolved by design. These are useful tests of record and recovery discipline, not proof of production usefulness or effect-complete rollback.

## 04:04–04:45 — Boundary and handoff

**Visual description.** A double-line boundary encloses “bounded local non-core
governance effect only.” Production transfer, semantic recovery, privacy
erasure, safe self-improvement, and core promotion remain outside. The live-book
URL and next chapter appear.

**Narration.** The core claim therefore remains Design rationale at argument support. The maximum justified inference is bounded local non-core governance effect only. This visual does not establish a useful replacement, production transfer, semantic recovery, privacy erasure, independent evaluator quality, safe self-improvement, or chapter-core promotion. The practical rule is simple: no replacement is complete until identity, evidence, state, effects, authority, recovery, residuals, descendants, and terminal disposition are all explicit. The next chapter, Security Kernel and Digital SCIFs, asks how privileged execution can remain isolated while those replacement and recovery obligations are enforced.

## Source and evidence boundary

The visual is a derivative of the canonical chapter and all thirteen assigned
source IDs. It reproduces none of the external systems and changes no claim.

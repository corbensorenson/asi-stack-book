# P5 Natural Publication-Service Development Trace

**Recorded:** 2026-07-27

**Role:** retrospective natural happy-path development observation

**Source commit:** `5575d3cbf5f9dd9edfec8548c4279728b0da3995` on `main`

**Machine record:** `experiments/p5_natural_publication_service_trace/results/2026-07-27-development.json`

## Why this trace belongs in P5

The work item was ordinary maintained-book work, not a task written to make
P5 look successful. The book needed to reconcile the latest guarded Theseus
T0A preflight and publish that correction. The resulting path crossed a real
repository boundary, hosted build infrastructure, artifact storage, a
separate deployment workflow, GitHub Pages, and a post-deploy public crawler.
That makes it the first natural operational happy path available to P5.

It is also outcome-aware. The deployment had already succeeded before this
record was designed. The trace is therefore a **development observation**, not
a prospective experiment, held-out case, positive efficacy result, or release
decision. Its main value is architectural: it shows which identities and
joins a natural publication path can preserve, and it exposes what the next
competent fault and rollback campaign still has to measure.

## The observed path

1. Commit `5575d3cbf5f9dd9edfec8548c4279728b0da3995` recorded the actual
   currentness correction on `main`.
2. GitHub Actions run `30287899588` built that exact SHA. The deep validation
   tier, Lean build, clean HTML render, canonical-status checks, Human-view
   checks, tested-bundle construction, and artifact upload all succeeded.
3. The resulting 28,389,505-byte artifact was named with the complete source
   SHA and carried digest
   `sha256:84700830e2f110e1b4406dc1dbc3976b0b2cecc9020455040706d128c3741dc2`.
4. A separate workflow, run `30288922224`, downloaded that artifact, verified
   it against the same expected commit, did not rebuild the site, and deployed
   it to GitHub Pages.
5. A separate post-deploy job crawled the deployed canonical status and
   chapter graph. The deployment status became successful 873 seconds after
   the source commit, and the monitor completed after 893 seconds.

The observation therefore preserves an exact source-to-build-to-artifact-to-
deployment-to-public-monitor identity chain across three external service
boundaries. The monitor is operationally separate from the deploy job, but it
is not a separately owned evaluator or an independent institution.

## What the trace teaches the architecture

A useful governed trace should distinguish at least five things that are often
collapsed into “deployment succeeded”:

- the work item and source identity;
- the tested build result;
- the immutable artifact passed between operators;
- the material public effect; and
- the observation that the effect satisfies declared public invariants.

The no-rebuild handoff matters. If the deploy path could silently rebuild,
successful source tests would not identify the bytes that reached the public
service. The post-deploy crawl matters for the opposite reason: a correct
artifact receipt does not establish that the public service is serving it
coherently. Both joins are necessary, and neither is sufficient for content
truth, user usefulness, or safety.

The trace also sharpens “delayed outcome.” A public effect arrived roughly
fifteen minutes after the commit, but the only delayed outcome measured was
publication consistency. No delayed harm window, user task outcome,
unsafe-release opportunity, or downstream consequence was observed. Time
passing is not the same as measuring a delayed outcome.

## What remains unmeasured

This was a happy path. It exercised no fault, incident, rollback,
compensation, replica conflict, distributed partition, monitor corruption, or
operator overload. It measured neither unsafe-release rate nor false blocking.
Operator time and hosted compute were not instrumented. The public service is
a moving target, and the uploaded artifact expires from GitHub artifact
storage after fourteen days.

Accordingly, the trace cannot answer whether governed operations improves the
joint safe-useful frontier. It supplies no matched generic-SRE or stop-only
arm, no calibrated evaluator, no sealed outcome, no uncertainty estimate, and
no independent reproduction. A green public crawl proves only the declared
publication invariants for the named observation interval; it does not prove
every page true, useful, or safe.

## How it changes the next P5 transaction

The next P5 campaign should retain this identity chain while adding the
missing causal stress:

- prospectively freeze the natural work population, fault envelope, metrics,
  evaluator, and stopping rules before outcomes are visible;
- preserve the same source, tested-artifact, no-rebuild deployment, public
  effect, and independent-observation joins;
- add at least one stable natural happy path and one stable blocked,
  compensated, or rolled-back path;
- compare strong ordinary rollout controls, generic SRE, and stop-only
  behavior under matched resources;
- instrument useful throughput, unsafe release, false blocking, latency,
  recovery time, operator burden, compute, and residual effects jointly; and
- keep the evaluator and monitor under separate ownership from the mechanism
  being scored.

This record changes no chapter-core support state and grants no new release
decision. It is a development input to that prospective design, not a member
of its held-out denominator.

# Prospective receiver availability comparison

Design fixed November 22, 2026. This prospective local experiment tests
whether a second caller-facing endpoint earns its place after a request
times out. It also tests whether independent availability can be supplied
behind an ordinary endpoint. Each trial changes a synthetic document
through a disposable journal. Status services run in separate local
processes under the same operator. Results concern the controlled
workloads and schedules in this protocol.

## Arms

1. **Conventional status.** One ordinary status endpoint consults the
   primary projection. It accepts a fresh exact observation and
   conditionally retries a fresh, explicit pre-effect failure.
2. **Additional endpoint.** Use the same ordinary endpoint first. If
   evidence is unavailable or stale, the caller may ask a receiving-side
   service with a separate status projection. Apply the same acceptance and
   retry rules to either response.
3. **Conventional endpoint with matched access.** The caller uses a single
   conventional status endpoint that can consult both projections in the
   same order under the same deadline. It returns the same scoped evidence
   as the second arm. It may use a transactional conditional retry on the
   same terms. Count both the caller request and any work behind the
   endpoint.

Each endpoint sees the same operation identity, permitted effect, trusted
source revision, deadline and remaining retry allowance. A usable
primary observation ends lookup in all arms. A current, mismatched effect
is adverse evidence and requires escalation. A stale, missing, or
unverifiable answer cannot justify closure or retry. An exact current
pre-effect failure permits up to one conditional retry of the same
operation. A retry response alone does not close the trial. Its terminal
effect must be verified.

## Fixed comparison conditions

- Use four synthetic task lineages with distinct targets and expected
  payloads. Each task is replayed under every condition. Count lineages and
  design cells separately.
- Cross the two service states independently. Each is fresh, stale or
  unavailable. Report conditions with two fresh responses, only one
  available fresh response, a shared loss of usable evidence, and a
  response delivered now from an earlier source revision.
- Cross four operation states. The expected effect has committed, the
  operation failed before any effect, a wrong effect has committed, or
  more than one effect has already committed. Scope matching uses the task's
  operation identity, target and payload separately from the workflow's
  declared outcome.
- Cross receiver deduplication on and off. For each cell run three arms
  with fresh copies of the same starting journal state. Rotate arm
  execution order across cells. The full design has 288 paired cells and
  864 arm observations. No final sample excludes an arm that holds,
  escalates, times out or refuses to retry.
- Give the primary and secondary reads one logical tick each and reserve
  a third tick for an eligible conditional retry. An operation starts with
  a timeout at tick zero. Stop any further work at the same decision
  deadline in each arm. Actual wall time and IPC bytes are reported
  separately from these logical costs.

## Outcomes and instrument controls

Compare each arm's disposition with an independently scored terminal
journal. Record verified exact closure, false closure, wrong effect,
repeat effect, and remaining hold or escalation separately. Record
which wrong and repeat effects were already present and which the arm
introduced. Report ticks until decision, ticks held through the horizon,
logical status reads, retries, request and response bytes and wall time.
Count cases routed to an operator as work requests. This design does not
observe a human operator or estimate labor minutes.

Require controls for an exact authorized effect, a single wrong target,
a single wrong payload, repeated effects, a stale payload with a current
response timestamp, and a fresh confirmed pre-effect failure. A control
also supplies the same fresh receiver observation through the additional
endpoint and the single endpoint with matched access. A difference in
decision on that pair invalidates the instrument. A runner failure or
incomplete arm makes its comparison inconclusive. Retain the error and the
original design denominator.

## Decide before looking at results

- A route that introduces a wrong or repeated effect, or falsely closes an
  operation, cannot earn adoption on these cases. Report the failing cells
  and retain the corresponding evidence and ordinary comparator.
- Compare the second endpoint with matched conventional access first.
  If both make the same safe decisions with the same observation, prefer
  one caller-facing endpoint when it provides that availability at equal
  or lower full burden. Keep the tradeoff open if one arm reduces held
  time but adds distinct operating work.
- Compare either route with primary-only conventional status to locate
  availability-dependent differences. Report an advantage only within a
  prespecified condition where independently available observations change
  verified closure without causing harm. Equal fresh observations should
  yield equal decisions. A shared outage should leave the effect
  unresolved.
- Report per-condition counts and paired differences. The design has
  four authored task lineages and repeated conditions, so it cannot
  estimate an incident frequency or a population-level effect. Separate
  service ownership, deployment latency, separately administered failures,
  and human effort remain follow-up questions.

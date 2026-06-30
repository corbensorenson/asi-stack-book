# Source Note: CoilMoECOT Whitepaper v2.0

| Field | Value |
|---|---|
| Source ID | `coilmoecot` |
| Source title | CoilMoECOT Whitepaper v2.0 |
| Ingestion date | 2026-06-24 |
| Source version / URL | Version 2.0 design/implementation spec, 2026-03-03; https://drive.google.com/file/d/1iwhhRGr7vj_Sr4UwwM_yX_ESSyisoWur |
| Ingestion basis | Authenticated Google Drive connector fetch succeeded; local cache is an auth-gate placeholder and raw text is not published. |

## Thesis

CoilMoECOT combines the MoECOT runtime substrate with a coil/specialist-core family. It should be treated as a design and implementation specification for routed cyclic or specialist lanes, not as automatic evidence that those lanes improve performance.

## Mechanisms

- MoECOT-style governed orchestration with coil specialist cores.
- Coil lane routing under deterministic/fail-closed control-plane constraints.
- Mutation and promotion only through explicit approval, benchmarks, readiness gates, and residual handling.

## Evidence

- Connector access established that the source is readable.
- The source is a design/spec source, not a performance claim.
- No CoilMoECOT local benchmarks have been run in this repo.

## Failure Modes

- Treating coil lanes as load-bearing for the core stack before evidence exists.
- Allowing cyclic memory or recurrence claims to imply quality gains without baselines.
- Letting routed lanes mutate without control-plane approval.

## Book Chapters Supported

- Mathematical and Search Substrates
- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores; includes folded MoECOT Runtime Crosswalk)
- Coil Attention, Cyclic Memory, and Recurrence Contracts
- CoilRA, MultiCoil RoPE, and Cyclic Mixers
- Prototype Roadmap
- Open Research Agenda and Bibliography Plan

## Claims To Add Or Update

- Keep coil mechanisms optional/specialist unless tests and baselines justify promotion.
- Use CoilMoECOT as routed-substrate context for mathematical/search substrate chapters without treating coil lanes as proven superior search mechanisms.
- Use CoilMoECOT in the research agenda as an optional routed-substrate lane whose adoption depends on baselines, readiness gates, and residual evidence.
- Tie any coil claim to structural invariants, residuals, and ordinary benchmark tradeoff metrics.

## Open Questions

- Which coil mechanisms belong in the main architecture versus optional substrate chapters?
- Which minimum baselines are required before cyclic memory claims can move beyond `argument`?

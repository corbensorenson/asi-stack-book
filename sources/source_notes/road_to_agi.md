# Source Note: Road To AGI

| Field | Value |
|---|---|
| Source ID | `road_to_agi` |
| Source title | Road To AGI |
| Ingestion date | 2026-06-24 |
| Source version / URL | Remaining-work source, 2026-03-01; https://drive.google.com/file/d/1FfYjqa36tMQ4s4KLbPPnIOZNfQefuT7p |
| Ingestion basis | Authenticated Google Drive connector fetch succeeded; local cache is an auth-gate placeholder and raw text is not published. |

## Thesis

Road To AGI is a strategic remaining-work and status source for the MoECOT track. It records what work remained, which claims were source-reported, and which benchmark or runtime gaps needed closure.

## Mechanisms

- Roadmap framing for MoECOT and adjacent runtime tracks.
- Reported benchmark commands/results and readiness status.
- Remaining work categories, promotion blockers, and implementation sequencing.

## Evidence

- Connector access established that the source is readable.
- Reported benchmark commands/results are source-reported only; this book repo has not reproduced them.
- Use as roadmap and blocker context, not as empirical evidence unless artifacts are ingested.

## Failure Modes

- Accidentally reporting source-reported benchmarks as locally run tests.
- Treating a roadmap as an implementation guarantee.
- Losing negative or remaining-work items when summarizing the architecture.

## Book Chapters Supported

- `routing-heads-and-specialist-cores` (Routing Heads and Specialist Cores; includes folded MoECOT Runtime Crosswalk)
- Prototype Roadmap
- Benchmark Ratchets and Anti-Goodhart Evidence
- Integrated Reference Architecture
- Living Book Methodology
- Open Research Agenda and Bibliography Plan

## Claims To Add Or Update

- Add roadmap blockers and remaining-work constraints to the prototype roadmap chapter.
- Use Road To AGI to keep the living book and research agenda honest about source-reported status, remaining work, promotion blockers, and unreproduced benchmarks.
- Keep benchmark support states conservative until logs/artifacts are present.

## Open Questions

- Which reported commands/results can be reproduced locally?
- Which remaining-work items still apply after later MoECOT/CoilMoECOT sources?
- Should source-reported results get a distinct table from book-tested results?

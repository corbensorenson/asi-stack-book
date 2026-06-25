# Source Note: What's Ray Core?

| Field | Value |
|---|---|
| Source ID | `ext_ray_core_docs_2026` |
| Source title | What's Ray Core? |
| Ingestion date | 2026-06-25 |
| Source version / URL | https://docs.ray.io/en/latest/ray-core/walkthrough.html |
| Citation label | Ray Documentation (2026), What's Ray Core? |
| Published / updated | unknown / 2026 |
| Ingestion basis | Official public documentation inspected for the Personal Compute Hives external literature queue; no Ray cluster or workload was run from this repository. |

## Thesis

Ray Core is relevant as a distributed execution substrate with task, actor, and object primitives. It can inform hive worker design, but it does not provide the full identity, approval, data-locality, or governance layer by itself.

## Mechanisms

- Represent stateless distributed work as tasks.
- Represent stateful distributed workers as actors.
- Represent transferred or returned data through object references and a distributed object store.
- Support scaling Python functions and classes into distributed execution patterns.

## Evidence

- The official docs describe Ray Core primitives for tasks, actors, and objects, with examples of remote functions and actors.
- This repository has not installed Ray, run a Ray job, measured task performance, or tested object-store privacy.
- Use this source to ground distributed-work vocabulary for hive workers and project-hive execution.

## Failure Modes

- Distributed primitives can move data faster than policy can track it if VCM and data-class constraints are absent.
- Actor state can become hidden memory outside the chapter's evidence ledger.
- Task success does not imply claim support, user benefit, or safe authority.

## Book Chapters Supported

- `personal-compute-hives-and-federated-edge-intelligence` (Personal Compute Hives and Federated Edge Intelligence)

## Claims To Add Or Update

- Use this note to describe task/actor/object patterns as candidate implementation tools for hives.
- Keep all claims about safe scheduling and privacy at `argument` until implemented and tested.

## Open Questions

- Should hive execution use Ray-style task references or a simpler artifact-bundle contract first?
- How should VCM taint and revocation apply to distributed object refs?
- Can Ray actors represent long-lived specialist capabilities without hidden state risk?

# Personal Compute Hives Companion Note

Status: drafting companion note, not release reviewed.

Chapter: `personal-compute-hives-and-federated-edge-intelligence`

Routing record: `editions/reader_manuscript/v1_0/companion_note_routing.json`

Primary reader source:
`build/reader_edition/chapters/personal-compute-hives-and-federated-edge-intelligence.qmd`

Curated prose draft:
`editions/reader_manuscript/v1_0/chapters/personal-compute-hives-and-federated-edge-intelligence.qmd`

Evidence references:
`docs/curated_reader_personal_compute_hives_prose_pass.md`,
`schemas/device_resource_card.schema.json`, `schemas/portal_card.schema.json`,
`schemas/hive_job_contract.schema.json`, `schemas/hive_job_bid.schema.json`,
`schemas/hive_scheduling_decision.schema.json`,
`schemas/hive_approval_receipt.schema.json`,
`schemas/hive_federation_lease.schema.json`, and
`proofs/lean/AsiStackProofs/PersonalComputeHives.lean`.

This note helps e-reader and audio review for the Personal Compute Hives
chapter. It does not replace the chapter prose or the curated prose draft.
Meaning-critical limits must still stay in the reader spine: reachable devices
are not automatically schedulable resources; consent, privacy, family/project
roles, rented-node boundaries, revocation, and evidence return must remain
visible before any work can move across a hive.

## Reader Promise

After reading or hearing this companion note, a human should be able to follow
why the chapter treats personal compute as a governed fabric rather than a
larger pool of machines. A hive is useful only when the scheduler rejects
unlawful nodes before optimization and can explain where the work ran, what
data crossed the boundary, who approved it, and how the node can be revoked.

## Dense Material Routed Here

| Dense item | Plain meaning | Boundary |
|---|---|---|
| `DeviceResourceCard` | A record for a phone, laptop, NAS, local GPU, workshop computer, rented node, or project runner. | It describes capability and policy; it does not grant open-ended authority. |
| `PortalCard` | A record for a human-facing surface such as a phone, browser, shared screen, headset, or family tablet. | A portal is not the whole AI and not the owner's full authority. |
| `HiveJobContract` | The bounded work request compiled from intent, planning, context, tool needs, risk, budget, approval, verification, and residual policy. | The hive should not accept raw "do this somewhere" instructions. |
| `HiveJobBid` | A node's bounded offer with capability, latency, cost, energy, privacy fit, interruption risk, and policy reason. | Bids happen after policy filtering, not before it. |
| `HiveSchedulingDecision` | The placement record that names eligible nodes, rejected nodes, selected node, approval receipts, data placement, isolation, evidence refs, and expiration. | Optimization is subordinate to rejection reasons and authority limits. |
| `HiveApprovalReceipt` | A specific person or guardian approval bound to one job, one boundary, and one time window. | Consent is scoped; it is not a permanent capability grant. |
| `HiveFederationLease` | A bounded way for another person, project, rented node, or public market to borrow capacity. | Federation does not inherit private network access or private data authority. |

## Main Spine Must Keep

The reader chapter should not move these boundaries exclusively into companion
material:

- policy filtering happens before optimization;
- private, family-sensitive, physical-world, credentialed, and rented-node
  work require different authority paths;
- old devices, local machines, rented GPUs, project runners, and remote
  services are not interchangeable;
- cost savings cannot justify private-data leakage, consent bypass, background
  family-device operation, or hidden physical-world risk;
- the current repository has record-shape fixtures and finite proof predicates,
  not a live hive scheduler, secure network overlay, federation system, rented
  private-data execution path, or family-governance implementation.

## Audio Treatment

In an audio script, do not read every hive object field as a long catalog.
Narrate the chapter as a placement discipline:

- a hive begins with a job contract, not a free-form wish;
- devices carry cards, not authority;
- sensitive work needs approval receipts and revocation paths;
- rented or external nodes return artifact bundles, not durable footholds;
- federation can exist in records before it is enabled in the world.

Detailed schema fields can be routed to this companion note. The main audio
should keep the ordinary reader focused on the practical question: why was this
job allowed to run there?

## Non-Claims

- This companion note is not a reader release record.
- This companion note is not an EPUB, PDF, DOCX, HTML, MP3, M4B, or
  audio-embedded EPUB artifact review.
- This companion note does not promote any chapter core claim above `argument`.
- This companion note does not claim a live hive scheduler, secure network
  overlay, safe rented-node private-data execution, public federation,
  autonomous spend, family-governance correctness, device reliability, energy
  optimization, or edge-execution safety.
- This companion note does not prove model quality, reasoning ability, context
  length, speed, memory scaling, deployment safety, transfer, or ASI.
- This companion note does not make curated reader prose equal authority beside
  the live AI/research book.

# ExoMem: OS-Governed Memory for Local Large-LLM Inference on Mobile Edge Devices

| Field | Value |
|---|---|
| Source ID | `ext_exomem_2026` |
| Publication | You et al. (2026). [Primary source](https://liuzhidan.github.io/assets/pdf/2026-MobiCom-ExoMem.pdf) |
| Review | November 27, 2026. [Selected source text](https://liuzhidan.github.io/assets/pdf/2026-MobiCom-ExoMem.pdf) |

## Thesis

Test physical-page reclamation when memory exhaustion determines feasibility.

## Mechanisms

Framework operators keep stable virtual addresses while the OS can reclaim physical pages from dormant mappings.

## Evidence

The authors report inference with 72B-class models on 64 GB Jetson devices under the tested memory regime.

## Failure Modes

Memory feasibility alone does not settle latency, quality or energy requirements for a different service.

## Book Chapters Supported

- `physical-compute-infrastructure-energy-and-environmental-constraints`

## Claims To Add Or Update

Use this source to frame the worked comparison in [physical-compute-infrastructure-energy-and-environmental-constraints](../../chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd). The chapter core retains argument-level support.

## Open Questions

Could returning pages to Linux solve the appliance’s limiting problem?

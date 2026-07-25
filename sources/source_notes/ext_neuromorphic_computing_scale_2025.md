# Source Note: Neuromorphic Computing at Scale

| Field | Value |
|---|---|
| Source ID | `ext_neuromorphic_computing_scale_2025` |
| Source title | Neuromorphic computing at scale |
| Authors / date | Dhireesha Kudithipudi et al.; Nature; 2025 |
| Primary URL | https://www.nature.com/articles/s41586-024-08253-8 |
| DOI | `10.1038/s41586-024-08253-8` |
| Evidence boundary | Field review and scaling roadmap; not proof of general advantage over digital accelerators. |

## Thesis

The review treats neuromorphic computing as an ecosystem spanning devices,
circuits, architectures, algorithms, software, applications, and benchmarks.
It emphasizes event-driven and brain-inspired computation, system-scale
integration, hardware-specific constraints, and the need for benchmark and
tooling maturity.

## Failure Modes

- Energy or latency advantages are workload-, precision-, sparsity-, device-,
  and measurement-bound.
- Spike-based execution changes state, timing, training, programmability,
  calibration, and observability contracts.
- Hardware scale does not establish useful model capability or easy migration
  from dense workloads.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`: explicit
  event-driven substrate family.
- `physical-compute-infrastructure-energy-and-environmental-constraints`:
  system-level cost and lifecycle.

## Mechanisms

- Use event-driven communication, local state, sparse activation, and
  neuromorphic hardware at reported system scale.

## Evidence

The peer-reviewed system result establishes reported behavior under its
workloads and conditions. No general-AI or end-to-end advantage was reproduced.

## Claims To Add Or Update

- Admit neuromorphic compute as a replaceable substrate only with encoding,
  training, accuracy, state, toolchain, energy, reliability, and retirement
  accounting.

## Open Questions

- Which natural AI workloads retain useful sparsity and quality after complete
  host, conversion, memory, and software costs are included?

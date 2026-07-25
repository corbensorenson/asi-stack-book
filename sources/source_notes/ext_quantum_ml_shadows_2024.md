# Source Note: Shadows of Quantum Machine Learning

| Field | Value |
|---|---|
| Source ID | `ext_quantum_ml_shadows_2024` |
| Source title | Shadows of quantum machine learning |
| Authors / date | Hsin-Yuan Huang et al.; Nature Communications; 2024 |
| Primary URL | https://www.nature.com/articles/s41467-024-49877-8 |
| DOI | `10.1038/s41467-024-49877-8` |
| Evidence boundary | Source-specific theoretical and empirical results; not proof of general practical quantum advantage. |

## Thesis

The paper foregrounds a deployment problem often omitted from quantum-ML
claims: both training and inference may require scarce quantum hardware. It
studies classical shadow models as an intermediate deployment phase. The
architectural lesson is to include data loading, hardware access, sampling,
readout, training, inference, verification, and classical alternatives in the
same adoption gate.

## Failure Modes

- Quantum advantage depends on the task, data-access model, device, noise,
  encoding, measurement budget, and classical comparator.
- A theoretical query or runtime advantage can disappear in end-to-end loading
  and readout.
- Shadowing changes the artifact and must preserve its own approximation and
  scope record.

## Book Chapters Supported

- `replaceable-cognitive-substrates-beyond-transformer-monoculture`: quantum
  and classical-shadow substrate route.
- `physical-compute-infrastructure-energy-and-environmental-constraints`:
  scarce-device and end-to-end cost.

## Mechanisms

- Analyze quantum-machine-learning advantage claims against data loading,
  classical shadowing, noise, scale, readout, and strong classical baselines.

## Evidence

The peer-reviewed analysis identifies theoretical and benchmarking boundaries;
it is not a claim that every quantum approach fails.

## Claims To Add Or Update

- Require full-pipeline quantum/classical accounting and preserve when a
  shadow or approximation changes the evaluated artifact.

## Open Questions

- Which practically verifiable problem families retain an advantage after data
  access, noise, error management, tuning, and total system cost?

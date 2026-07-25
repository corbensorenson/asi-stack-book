# Source Note: zkLLM

| Field | Value |
|---|---|
| Source ID | `ext_zkllm_2024` |
| Source title | zkLLM: Zero Knowledge Proofs for Large Language Models |
| Authors / date | Haochen Sun, Jason Li, and Hongyang Zhang; 2024 |
| Primary URL | https://arxiv.org/abs/2404.16109 |
| Source type | peer-reviewed systems/cryptography paper and preprint record |
| Evidence boundary | Source-reported proof-system construction and measurements; no local reproduction or claim that arbitrary deployed inference is verifiable. |

## Thesis

zkLLM constructs zero-knowledge proofs for quantized LLM inference, including
specialized handling for non-arithmetic operations. The paper reports a
CUDA-based prover, sub-200-kB proofs, and proof generation under fifteen
minutes for a 13-billion-parameter model in its evaluated setting. It is a
concrete comparator showing that “verifiable inference” can refer to a
cryptographic statement about an exact encoded computation rather than a
semantic judgment about the answer.

## Failure Modes

- The proven statement is bounded by the circuit, quantization, commitment,
  model identity, input/output encoding, and cryptographic assumptions.
- A valid inference proof does not show that the model is truthful, safe,
  authorized, unbiased, current, or the right model for the task.
- Prover time, memory, preprocessing, hardware, and unsupported operations must
  be included in total cost.

## Book Chapters Supported

- `confidential-and-verifiable-ai-computation`: primary zkML comparator.
- `executable-specifications-and-lean-proof-envelope`: example of a formal
  artifact whose semantic ceiling must remain explicit.
- `model-weight-custody-and-hardware-roots-of-trust`: model-identity binding
  without revealing weights.

## Mechanisms

- Commit to model and inference values, encode the supported relation, produce
  a zero-knowledge proof, and verify it without revealing protected witnesses.

## Evidence

The paper reports prototype proof-size and latency results for its construction
and configurations. This repository has not reproduced them.

## Claims To Add Or Update

- Keep proof-system correctness, circuit correspondence, model identity,
  semantic validity, authorization, and total cost as separate claim classes.

## Open Questions

- How do proof cost and circuit fidelity scale across modern architectures,
  context lengths, sampling, retrieval, tools, quantization, and batching?

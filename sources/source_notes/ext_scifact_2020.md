# Fact or Fiction: Verifying Scientific Claims

| Field | Value |
|---|---|
| Source ID | `ext_scifact_2020` |
| Publication | Wadden et al. (2020), EMNLP. [Paper](https://aclanthology.org/2020.emnlp-main.609/) |
| Review | November 27, 2026. [Data format and annotation guide](https://github.com/allenai/scifact/blob/master/doc/data.md) |

## Thesis

Verification of a scientific claim requires an evidence-bearing document, a verdict, and the sentence set that justifies it.

## Mechanisms

A claim can have several acceptable rationales or require several sentences together. The original records preserve document identity and zero-based sentence indices.

## Evidence

The authors constructed about 1,400 expert-written claims with a corpus of 5,183 abstracts. The local study reserves labeled development claims for evaluation and uses paper-disjoint training claims to choose release thresholds.

## Failure Modes

Incomplete evidence annotations, public evaluation labels and domain-specific retrieval limit the interpretation of the local comparison. Textual entailment of a retrieved abstract cannot establish universal scientific truth.

## Book Chapters Supported

- `verification-bandwidth-and-context-adequacy`

## Claims To Add Or Update

Use the dataset for the bounded claim-and-citation comparison. Retain the architecture claim at argument-level support.

## Open Questions

How much does full-rationale coverage improve with a second retrieved document at a matched compute budget?

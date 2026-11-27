# Locating and Editing Factual Associations in GPT

| Field | Value |
|---|---|
| Source ID | `ext_rome_2022` |
| Publication | Meng et al. (2022). [Primary source](https://rome.baulab.info/) |
| Review | November 27, 2026. [Selected source text](https://rome.baulab.info/) |

## Thesis

Check specificity with neighboring facts as well as success on paraphrases.

## Mechanisms

ROME localizes and changes an MLP computation associated with a factual relation.

## Evidence

CounterFact probes the requested change, paraphrases and related subjects whose predictions should remain stable.

## Failure Modes

A targeted association edit establishes little about transplanting the edit to a second network.

## Book Chapters Supported

- `cognitive-compilation-and-semantic-ir`

## Claims To Add Or Update

Use this source to frame the worked comparison in [cognitive-compilation-and-semantic-ir](../../chapters/cognitive-compilation-and-semantic-ir.qmd). The chapter core retains argument-level support.

## Open Questions

Which neighboring facts should survive the edit?

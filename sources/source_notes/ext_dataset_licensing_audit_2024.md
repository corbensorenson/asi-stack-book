# A large-scale audit of dataset licensing and attribution in AI

| Field | Value |
|---|---|
| Source ID | `ext_dataset_licensing_audit_2024` |
| Publication | Shayne Longpre et al. (2024). [Primary publication](https://www.media.mit.edu/publications/a-large-scale-audit-of-dataset-licensing-and-attribution-in-ai/). |

## Thesis

Trace upstream components and attribution before relying on a collection-level label.

## Mechanisms

Recover identifiers, upstream components and terms across aggregators, then compare the recovered metadata with hosting-site labels.

## Evidence

An audit tracing over 1,800 text datasets found frequent license omissions and errors on hosting sites.

## Failure Modes

The metadata audit does not decide permissions for an individual use of a particular artifact.

## Book Chapters Supported

- `ai-supply-chain-integrity-and-lifecycle-provenance`

## Claims To Add Or Update

The chapter uses the paper as an external comparison in “Which source record travels with the mixture?” and retains its existing core support state.

## Open Questions

What versioned origin and terms can a downstream publisher recover for the mirrored component?

# Exokernel: An Operating System Architecture for Application-Level Resource Management

| Field | Value |
|---|---|
| Source ID | `ext_exokernel_1995` |
| Publication | Engler et al. (1995). [Primary source](https://pdos.csail.mit.edu/6.1810/2017/readings/engler95exokernel.pdf) |
| Review | November 27, 2026. [Selected source text](https://pdos.csail.mit.edu/6.1810/2017/readings/engler95exokernel.pdf) |

## Thesis

Record who protects each resource and who may schedule it.

## Mechanisms

A small privileged kernel protects physical resources while applications choose management policy through library operating systems.

## Evidence

The prototype evaluated primitives such as protected transfer and communication against contemporary systems.

## Failure Modes

Its microbenchmarks predate contemporary model serving. Their speedups cannot price a decoder.

## Book Chapters Supported

- `physical-compute-infrastructure-energy-and-environmental-constraints`

## Claims To Add Or Update

Use this source to frame the worked comparison in [physical-compute-infrastructure-energy-and-environmental-constraints](../../chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd). The chapter core retains argument-level support.

## Open Questions

Who can refuse an allocation when applications own scheduling policy?

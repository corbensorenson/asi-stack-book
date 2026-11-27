# NuraOS: a minimal Linux appliance for local inference

| Field | Value |
|---|---|
| Source ID | `ext_nuraos_2026` |
| Publication | NuraOS project (2026). [Primary source](https://github.com/YASSERRMD/NuraOS/blob/830b20a61de65a6063ead2c33807218ab7fd165d/README.md) |
| Review | November 27, 2026. [Selected source text](https://github.com/YASSERRMD/NuraOS/blob/830b20a61de65a6063ead2c33807218ab7fd165d/README.md) |

## Thesis

Identify who owns service restart when inference stops.

## Mechanisms

A Linux kernel and minimal userland start an inference server and agent services.

## Evidence

The pinned project README describes the boot path, service layout and Linux isolation facilities.

## Failure Modes

Project documentation establishes the intended topology. No physical boot or performance comparison was reproduced for this book.

## Book Chapters Supported

- `physical-compute-infrastructure-energy-and-environmental-constraints`

## Claims To Add Or Update

Use this source to frame the worked comparison in [physical-compute-infrastructure-energy-and-environmental-constraints](../../chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd). The chapter core retains argument-level support.

## Open Questions

What changes for the operator when the service fails but the kernel still runs?

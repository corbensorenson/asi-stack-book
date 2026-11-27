# Unikernels: Library Operating Systems for the Cloud

| Field | Value |
|---|---|
| Source ID | `ext_mirage_unikernels_2013` |
| Publication | Madhavapeddy et al. (2013). [Primary source](https://anil.recoil.org/papers/2013-asplos-mirage.pdf) |
| Review | November 27, 2026. [Selected source text](https://anil.recoil.org/papers/2013-asplos-mirage.pdf) |

## Thesis

Count the hypervisor in the boot and device dependency chain.

## Mechanisms

Compile application and selected OS libraries into a single-purpose image for a hypervisor.

## Evidence

The Mirage design and network-service examples leave the Xen boundary visible beneath the image.

## Failure Modes

A bootable guest image can still depend on a host or hypervisor for device access.

## Book Chapters Supported

- `physical-compute-infrastructure-energy-and-environmental-constraints`

## Claims To Add Or Update

Use this source to frame the worked comparison in [physical-compute-infrastructure-energy-and-environmental-constraints](../../chapters/physical-compute-infrastructure-energy-and-environmental-constraints.qmd). The chapter core retains argument-level support.

## Open Questions

Which dependency remains below the image at deployment?

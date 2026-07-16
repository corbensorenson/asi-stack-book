# Source Note: Guidelines for Media Sanitization

| Field | Value |
|---|---|
| Source ID | `ext_nist_media_sanitization_2025` |
| Source title | Guidelines for Media Sanitization |
| Ingestion date | 2026-07-14 |
| Source version / URL | NIST SP 800-88 Rev. 2 final, https://csrc.nist.gov/pubs/sp/800/88/r2/final |
| Citation label | Chandramouli and Hibbard (2025), NIST SP 800-88 Rev. 2 |
| Published / updated | 2025-09-26 / 2025-09-26 |
| DOI | 10.6028/NIST.SP.800-88r2 |
| Ingestion basis | Official final publication page reviewed for the current definition of media sanitization, sensitivity- and media-appropriate programs, cryptographic erase, and effort-relative infeasibility. No local media, memory, cache, backup, cloud replica, or weight artifact was sanitized or forensically tested. |

## Thesis

Deletion and zeroization are not binary metaphysical facts. A sanitization claim
must name the target data, media, method, sensitivity, threat/effort level,
validation, coverage, and residuals. Sanitizing one medium says nothing about
undiscovered copies, live memory, caches, backups, cloud replicas, recipients,
or derivative artifacts.

## Mechanisms

- Select a clear, purge, destroy, or cryptographic-erase approach appropriate to
  the data sensitivity, media type, reuse/disposal plan, and assumed effort.
- Inventory the exact target media and data scope before applying and validating
  the sanitization method.
- Record method, device/media identity, controller behavior, key dependency,
  validation evidence, failures, exceptions, and disposition.
- Treat cryptographic erase as dependent on key coverage, key destruction,
  algorithm/implementation assumptions, and absence of plaintext copies.
- Preserve residuals where sanitization cannot be validated or the inventory is
  incomplete.

## Evidence

- SP 800-88 Rev. 2 is the current final NIST media-sanitization guideline,
  published in September 2025.
- Its definition is effort-relative and programmatic; it does not claim physical
  impossibility of recovery under every adversary.
- This repository has not sanitized or forensically examined any model-weight
  storage, memory, accelerator, backup, cloud, or recipient surface.

## Failure Modes

- File deletion or a zeroization receipt is treated as proof that all physical
  or logical copies are inaccessible.
- Cryptographic erase targets one key while plaintext, wrapped keys, snapshots,
  caches, replicas, recovery material, or derivatives survive.
- A method appropriate for one medium or effort level is generalized to another.
- Validation checks command success rather than whether the target data became
  infeasible to access at the declared effort.
- Sanitization language is used to launder an already irreversible recipient or
  open-weight release into a reversible event.

## Book Chapters Supported

- `model-weight-custody-and-hardware-roots-of-trust`

## Claims To Add Or Update

- Replace generic “destroyed” or “zeroized” states with target-, method-, media-,
  validation-, effort-, and inventory-relative sanitization receipts.
- Separate key revocation, cryptographic erase, media sanitization, artifact
  retirement, recipient recall, and public disclosure.
- Require descendant and copy closure plus explicit unknown-copy residuals before
  any bounded erasure claim.

## Open Questions

- Which public-safe disposable artifacts can test file, cache, snapshot, and
  cryptographic-erase bookkeeping without implying forensic assurance?
- How should accelerator and confidential-workload memory be represented when
  direct validation is unavailable?
- What terminal states distinguish verified sanitization, attempted but
  unverified, failed, out of scope, irreversibly released, and unknown?

## Non-claims

- No media sanitization, forensic validation, cryptographic erase, copy closure,
  recipient recall, or weight erasure is established.
- A standards-aligned record does not prove the inventory complete or make an
  irreversible release reversible.

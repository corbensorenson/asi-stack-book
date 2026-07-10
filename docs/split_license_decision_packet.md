# Split-License Decision Packet

Last updated: 2026-07-10. Decision state: delayed opening selected; active
drafting rights remain all-rights-reserved.

The current repository is all-rights-reserved. Public visibility allows
inspection; it does not grant reuse, modification, redistribution, or
implementation rights. That protects control but sharply limits adoption of
the book's code, schemas, proofs, validators, figures, and prose.

`governance/licensing_decision.json` compares four paths: retain all rights;
use a permissive split; use a noncommercial or custom controlled split; or
open cleared material after the drafting phase. The author selected a delayed
opening because it matches the author-only prepublication process without
abandoning a future adoption path. At the first author-declared completed major
release, the intended cleared split is:

- CC BY 4.0 for author-owned prose and figures;
- Apache-2.0 for author-owned code, proofs, schemas, and scripts;
- no automatic dedication of public metadata; it remains reserved until
  record-level review selects and records a compatible license;
- explicit exclusions for third-party quotations/assets, raw source exports,
  private or local-project material without permission, trademarks, and
  endorsements; and
- a contribution policy opened only after completion and made compatible with
  the operative outbound lanes.

That selection is not a present permission grant and is not legal advice. Open grants are
generally difficult to retract for already released material, mixed-rights
files require careful routing, and contribution terms must be settled before
accepting contributed material. Until the completed-release transaction,
`LICENSE.md` remains the only operative policy and no SPDX, Creative Commons,
or Apache signal should imply otherwise.

## Official terms reviewed

The policy review used the official [CC BY 4.0 deed and legal-code
route](https://creativecommons.org/licenses/by/4.0/) and the Apache Software
Foundation's [Apache License 2.0 application
guidance](https://www.apache.org/legal/apply-license). CC BY 4.0 permits sharing
and adaptation, including commercial use, subject to attribution and change
indication; its official material warns licensors to use it only when they are
authorized to grant the rights. Apache's guidance describes the license as a
copyright-and-patent license and instructs distributors to include the exact
license text. Those features are why rights clearance and exact release texts
remain gates instead of being inferred from public repository visibility.

## Completed technical prerequisite

The path-enumeration and routing portion of the provenance audit is now
implemented in `licensing/provenance_inventory.json`. It deterministically
classifies 2,219 tracked or untracked nonignored repository candidates: 0 are
marked cleared, 206 remain explicit third-party/mixed external-source review,
159 are historical/generated derivative review, 722 are experiment/import
review, 114 require local-project or asset-specific review, and the remaining
candidate prose, software, metadata, and configuration paths still require
author ownership assertions.

This removes ambiguity about which files need decisions; it does not answer the
legal or factual ownership questions. The policy decision is closed, while
qualified review, author ownership assertions, exception resolution, exact
license texts, and release-specific implementation remain completion-stage
gates. Prepublication contributions are closed. `LICENSE.md` continues to
grant no present permission.

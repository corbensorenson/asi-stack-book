# Immutable Site Archive Pipeline

Last updated: 2026-10-10

An immutable site archive is derived only from the exact tested Pages bundle.
It is not rebuilt from Quarto source, does not substitute a moving Pages path,
and does not become published merely because a local tarball exists.

## v1.0.0 decision

The author declined a v1.0.0 full-site backfill on 2026-07-10. The exact tested
v1.0.0 Pages bundle was not preserved, and a later render could differ by
toolchain, generated metadata, or source behavior. Publishing that render as
the historical site would create false artifact identity. The source tag and
release remain valid history; the policy row remains `not_published` and names
the explicit no-backfill decision. Immutable full-site publication begins with
the next eligible clean tag-bound tested bundle.

## Deterministic candidate

`scripts/build_immutable_site_archive.py` reads `tested-site-bundle.json`,
requires the version and source commit to match a known release-policy row,
and writes a deterministic `tar.gz` named by
`status/versioned_release_policy.json`. Every tar header uses UID/GID zero,
empty owner names, normalized file/directory modes, lexicographic member order,
and epoch-zero timestamps. The gzip timestamp is also zero.

The archive contains one root directory, the tested-bundle manifest, and the
complete tested `site/` tree. It does not contain its own candidate manifest,
which avoids a self-referential digest. The adjacent candidate manifest records
archive size/SHA-256, source-bundle manifest and tree digests, release record,
candidate state, publication non-state, and non-claims.

Preparation now inspects the complete source bundle, including its metadata,
before reading payload bytes. It recomputes the bundle manifest and binds the
exact bytes used for archive members; stale inventories, links, special objects
and unregistered empty directories reject. The output, bundle and policy must
not overlap. Named policy/checking inputs and source bytes are checked again
before and after installation.

The builder prepares all three payload files in memory and applies the archive
consumer before installing a complete directory under the shared writer lock.

The October 10 C04 review reproduced a shared-inventory blind spot: changing
the producer's `source_members` function to omit `site/index.html` also changed
the consumer's expected inventory, allowing an incomplete candidate to pass.
The consumer now derives its member/content expectations directly from the
captured bundle bytes, without importing that transformation. A fixed regression
checks missing site content, a missing bundle manifest and rewritten content.
Self-consistent candidate/checksum metadata cannot make those artifacts pass;
the preparation gate rejects them before replacing the previous candidate.

| Acceptance boundary | Independence and shared assumptions |
|---|---|
| Archive member completeness and content | The consumer maps captured bundle bytes itself; it does not call the producer's member selector. Its bounded gzip/tar parser compares the actual members and their contents against that mapping. |
| Tar metadata, types and unexpected directories | The consumer checks headers itself. Path normalization remains a shared helper and could carry a shared path-grammar error. |
| Exact deterministic serialization | The consumer deliberately reuses `archive_bytes` for byte-level replay. This is consistency evidence, not an independent serializer implementation. |
| Source capture and bundle admission | `inspect_bundle`, regular-file reading, tested-bundle inventory/build checks and JSON/SHA-256 remain shared dependencies. A common capture or admission error is outside this tested separation. |
| Policy, schema and output custody | Policy selection, the schema engine and generated-directory ownership machinery remain shared. The archive consumer retains its own publication non-state, source/policy bindings and content comparisons; this phase does not independently qualify every policy or custody rule. |

These are authored mechanism tests for this archive consumer. The C03 independent
namespace model separately checks the product/archive installer. Neither check
establishes source truth, compiler correctness, independent institutional review,
natural-workload benefit or publication authority. Other consumers require their
own dependency review and sensitivity evidence.

`projection-install-manifest.json` is an additional local family/integrity
receipt; it is excluded from the tarball. Unknown candidate files/directories
are preserved. A legacy candidate may be adopted only if its three payload
files exactly match the current inspected result. Existing owned candidates
also retain their version, commit, archive digest and source-manifest identity;
another identity requires a fresh output. Metadata/receipt updates may replace
the directory while keeping those immutable bytes. Interrupted exchange or
uncertain post-install acceptance/fsync retains the prior tree and stage journal.
These authored macOS observations do not establish Linux or physical durability.

For a local diagnostic replay of the machinery, use a policy-eligible version
and bundle. The former v1.0.0 example below is retained only as a negative
historical illustration and must not be published:

```bash
python3 scripts/build_immutable_site_archive.py \
  --bundle build/pages-tested \
  --version v1.0.0 \
  --output build/immutable-site-archive \
  --allow-local

python3 scripts/validate_immutable_site_archive.py \
  --bundle build/pages-tested \
  --candidate build/immutable-site-archive \
  --allow-local
```

Without `--allow-local`, both builder and validator require
`source_tree_state=clean` and `build_context=tested_commit`.

Add `--check` to the builder with the same bundle, version, policy and output
arguments to check its installed receipt without writes or timestamp changes.
Its code/input identity must be current. Candidate consumption is different:
the validator can accept an older intact family receipt when its actual bytes
still satisfy the current domain contract. Checking-code changes alone do not
invalidate otherwise correct archive bytes by rewriting historical custody.
Candidates containing mutation files left by the earlier validator require
inspection and a fresh output; they are not silently cleaned up or adopted.

## Validation

`scripts/validate_immutable_site_archive.py` checks the candidate schema,
policy version and commit binding, archive filename, archive and bundle
digests, exact member bytes, safe paths and member types, clean/dirty candidate
state, and byte-identical deterministic replay. Four controls reject a wrong
source commit, false published state, changed archive bytes, and a traversal
member.

Validation now reads the complete candidate before acceptance, checks the
adjacent checksum and metadata bytes, and verifies the root directory, build
state and storage authority against the source/policy. Mutation controls run
in memory and do not write into the candidate. The tar parser rejects duplicate
members, extra directory objects, unsupported types and noncanonical header
metadata. Expansion is bounded by actual inspected source members plus header
overhead, rather than candidate-supplied size claims. Deterministic byte replay
remains a check against the same producer, not an independent archive oracle.
Seventeen infrastructure controls additionally cover ownership, no-op/check
purity, legacy adoption, source drift, overlaps, immutable identity, malformed
inputs, policy refusal, edits between positive acceptance and control completion, and
custody after exchange/fsync/collision failures. The complete CLI operation
rechecks candidate/source/policy inventories after the controls.

## Publication transaction

Publication is intentionally not automatic from a dirty worktree or merely
prepared candidate. The authorized release transaction must:

1. start from a clean, successful tested-bundle run for the exact tag commit;
2. build and validate the deterministic candidate without `--allow-local`;
3. review the archive and candidate manifest;
4. verify that the destination GitHub Release is attached to the same tag and
   commit and that no same-named asset exists;
5. upload the archive, candidate manifest, and checksum without overwrite;
6. download the public asset and recheck its SHA-256;
7. update the release record and versioned-release policy with the exact public
   URL and digest in the same governed release change; and
8. regenerate `/versions/index.json` and run deployed attestation.

Until those steps complete, the candidate manifest must retain
`local_candidate_not_published` and an empty URL. Local deterministic replay is
not durable storage, publication, independent review, or proof of the book's
claims.

# Immutable Site Archive Pipeline

Last updated: 2026-07-10

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

## Validation

`scripts/validate_immutable_site_archive.py` checks the candidate schema,
policy version and commit binding, archive filename, archive and bundle
digests, exact member bytes, safe paths and member types, clean/dirty candidate
state, and byte-identical deterministic replay. Four controls reject a wrong
source commit, false published state, changed archive bytes, and a traversal
member.

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

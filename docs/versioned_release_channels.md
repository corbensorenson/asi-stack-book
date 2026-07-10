# Versioned Release Channels

Last updated: 2026-07-10

The root Pages URL remains a compatibility surface. `/latest/` is a full copy
of the exact tested root site and moves when a newer tested commit is deployed.
`/versions/index.json` is a metadata index, not an archive. Durable immutable
site bundles belong in GitHub Release assets attached to an exact semantic
version tag, with a full source commit, public release record, artifact URL,
and SHA-256 recorded together.

This distinction prevents three forms of release laundering: calling the
moving Pages site v1.0.0, treating a source tag as proof that a frozen site
bundle exists, or treating the `versions/` metadata path as durable artifact
storage. The current v1.0.0 row therefore says `not_published` for the site
artifact while linking its real immutable source release. On 2026-07-10 the
author explicitly declined a v1.0.0 site-archive backfill because the exact
tested historical bundle was not preserved; a later render would fabricate
artifact identity. The row therefore remains unpublished permanently. Full-site
immutable archives begin with the next eligible clean tag-bound tested bundle.

`build_release_channels.py` creates the complete latest mirror and version
index before the tested site bundle is hashed. `validate_release_channels.py`
checks policy and release-record commits, enforces URL-plus-digest coupling for
published site artifacts, compares every latest file with the tested root, and
owns rejecting controls for an unbacked artifact claim, wrong latest commit,
and changed latest file.

`build_immutable_site_archive.py` now provides the production path that the
policy previously described only in prose. It packages the exact tested bundle
with normalized ownership, modes, order, and epoch-zero tar/gzip timestamps;
the archive candidate records both source-bundle and archive digests without
including itself in the tarball. `validate_immutable_site_archive.py --self-test`
builds a clean synthetic candidate, verifies exact members and deterministic
replay, and rejects commit mismatch, false publication, byte mutation, and path
traversal. `docs/immutable_site_archive_pipeline.md` defines the authorized
upload/redownload/reconciliation transaction.

This machinery does not backfill v1.0.0 by declaration. The builder rejects a
release-policy row whose historical backfill was declined, even if a later
bundle is pointed at that version. The absence is an honest historical record,
not an open publication task.

No channel policy proves model quality, safety, chapter claims, source
interpretation, or artifact durability beyond the named storage authority.

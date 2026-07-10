# External AI Review Live-Deployment Re-Audit

Observed at UTC: `2026-07-10T15:45:29Z`

This is a read-only observation of the public Pages site, GitHub Actions API,
and v1.0.0 GitHub Release after the local review-remediation implementation.
It does not treat a green workflow, an HTTP response, or an API record as
evidence for chapter claims.

## Public Pages observation

| Surface | Result |
|---|---|
| Root | HTTP 200; 243,099 bytes; SHA-256 `b8057eadfaa9a939d3b01a80e8c10dd72684c2cb99eba95dc5d474e8f7d81df7` |
| Root navigation | 53 unique `chapters/*.html` links |
| Active count prose | Three occurrences of 53-chapter language, one occurrence of 45-chapter language, two occurrences of 249 public-safe sources, and no 54-chapter or 271-source language |
| `/status/canonical-public-status.json` | HTTP 404; 9,379-byte GitHub Pages not-found response |
| `/versions/index.json` | HTTP 404; 9,379-byte GitHub Pages not-found response |
| `/products/narrative-book/` | HTTP 404; 9,379-byte GitHub Pages not-found response |

The public deployment therefore does not contain the current canonical-status,
version-channel, or product-projection controls. It remains a 53-chapter,
249-source generation with an additional stale 45-chapter phrase.

## GitHub Actions observation

The public Actions API reports run `29087187930`, workflow name
`Publish Quarto site`, for source commit
`e672ad07bc0ac6c5994b3fe9a65292f1573f158a`. It was created at
`2026-07-10T10:42:50Z`, triggered by `push`, and completed successfully.

That success is not a coherence attestation. The workflow predates the local
tested-build/deploy split now in the dirty worktree, and the deployed responses
above do not contain the new canonical status or product routes. A green legacy
publish run cannot satisfy the new build-to-deploy-to-attest contract.

## Immutable v1.0.0 observation

The GitHub Releases API reports tag `v1.0.0` targeting commit
`96d0ca3c6b62f3530202535573941b1f6e50a83d` and an empty release-asset array.
GitHub's automatically generated source archives are not uploaded site assets.
The policy row's `not_published` state for a full immutable site bundle remains
accurate.

## Disposition

- R01 and R05 remain open at the deployed boundary.
- R04 and R14 are implemented locally but absent from the public site.
- R06 now has deterministic archive production and validation locally, but no
  full site archive is published on v1.0.0.
- The next qualifying event is a successful run of the new clean tested-build
  producer, exact-artifact deploy consumer, and post-deployment attestation for
  one committed source state.

## Non-Claims

- This re-audit does not authorize a deployment, commit, push, release upload,
  title change, license change, or reviewer outreach.
- HTTP and GitHub API observations do not prove infrastructure completeness,
  artifact durability, security, or chapter truth.
- The local worktree remains dirty; its generated diagnostic bundle is not a
  deployable release artifact.

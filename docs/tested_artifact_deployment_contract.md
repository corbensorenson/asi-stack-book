# Tested-Artifact Deployment Contract

Last updated: 2026-10-03

The Pages release path has two authorities. `Build tested Pages artifact`
checks out one commit, runs the deep validation registry, builds Lean, renders
into an empty `_site`, creates canonical status, validates the rendered graph,
and uploads a commit-named tested bundle. The deployment workflow starts only
after that exact workflow run succeeds on `main`.

The handoff bundle contains the rendered site and
`tested-site-bundle.json`. Its manifest binds the full source commit, canonical
status ID and digest, every relative file path, every file size and SHA-256,
the total byte count, and a deterministic tree digest. Deployment downloads
the artifact from the triggering workflow-run ID, checks out the recorded head
commit only to obtain the verifier, recomputes the manifest, and checks the
expected commit before uploading the already-tested `site/` directory to
Pages. It does not render, build proofs, synchronize source, or run a fresh
source validation pass.

After Pages deployment, a separate job checks out the same tested commit and
crawls the deployed canonical status, sidebar order, chapter URLs, and H1
shape. This catches record/reality disagreement after the artifact boundary;
it does not retroactively prevent a deployment that Pages accepted.

`scripts/validate_tested_site_bundle.py` owns rejecting controls for a changed
file digest, wrong expected commit, and missing site file.
`scripts/validate_tested_artifact_deployment.py` owns rejecting controls for a
deploy-time rebuild, a current-run rather than triggering-run artifact, and a
missing commit binding.

## Residual boundary

- GitHub retains and transports the Actions artifact; the manifest detects
  changed content but does not make the storage or runner trustworthy.
- A passing bundle check proves identity and integrity relative to the
  manifest, not benign content, chapter truth, safety, or security.
- The public site remains unverified until post-deployment attestation passes.
- Artifact retention is finite; durable immutable releases require the
  separate versioned-release policy and recorded release assets.

## Candidate selection and local staging

Only an artifact whose tested source SHA equals the currently observed
`refs/heads/main` is eligible. The serialized deploy job checks this before
artifact download and again after upload, immediately before deployment. A
late older success cannot cancel an active deployment. A main-branch change
after the final check can still happen; the post-deployment observer must
report the actual revision rather than infer freshness from ordering.
An intentional rollback selects the exact earlier tested revision by moving
main through the normal authorized rollback process, then rerunning its tested
build. A stale successful event alone cannot select a rollback. Skipped
candidates do not create attestation records. Selector/network failure blocks
selection.

The local builder rejects source/root/directory/broken links, special files,
ancestry overlap and unowned destinations. It locks the output, builds and
verifies a complete sibling staging tree, checks copying against the original
manifest and exchanges two complete directories in one OS operation. Linux
`renameat2(RENAME_EXCHANGE)` and Darwin `renamex_np(RENAME_SWAP)` are the
supported replacement mechanisms; unavailable support fails with the prior
output in place. File/directory sync precedes exchange. Process-interruption
probes on macOS leave a complete old or new bundle; this does not certify
storage hardware behavior during physical power loss. An interrupted staging
area may be inspected and discarded after its owner confirms it is obsolete.

File inventories include the directories required by their file paths;
additional empty directories are unregistered objects and reject before
replacement. New destinations use an exclusive atomic rename, so a directory
created after the absence check is preserved. The verifier inspects the outer
bundle, including metadata and path ancestry, before reading its manifest.
After exchange, both the installed tree and displaced prior tree are checked.
An exception during installation or failed acceptance/fsync retains the sibling
stage and its journal. `installation_outcome_unconfirmed` means the helper may
have exchanged directories before raising; inspect both trees rather than
assuming the prior tree is still at the destination. No retained stage is
automatically adopted or deleted as recovery.

The browser gate requires the repository's locked Playwright installation.
A missing/mismatched module fails even when an ambient global installation
exists. A deliberately missing local module was rejected, and the available
locked runtime passed the rendered checks. Failure outcomes and screenshots
are retained through the CI diagnostics artifact. This remains local/static
verification until fresh Linux jobs execute the workflow.

The producer writes a versioned report bound to the complete checked site,
the canonical chapter manifest, the current reader crosswalk and its own
source bytes. Changes during the browser run reject. Reports/screenshots stay
outside the checked site; report replacement uses an individual staged file.
The following Python consumer requires a current `pass` report, every
canonical technical/reader route in both declared viewports, all six narrow
and enlarged control cases, and consistent reported interaction/layout
outcomes. Missing, skipped, duplicate, incomplete, stale or contradictory
reports reject before bundling. Fourteen static workflow mutations and eight
authored report-consumer tests pass locally. The consumer checks custody and
reported outcomes; it does not independently rerun DOM probes or establish
human accessibility review, editorial approval, Linux success or publication.

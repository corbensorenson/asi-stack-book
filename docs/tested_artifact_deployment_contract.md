# Tested-Artifact Deployment Contract

Last updated: 2026-07-10

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

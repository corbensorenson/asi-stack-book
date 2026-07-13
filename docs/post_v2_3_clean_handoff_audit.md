# Post-v2.3 Clean Handoff Audit

Audit date: 2026-07-13

Roadmap authority:
`docs/post_v2_3_handoff_reader_formats_and_evidence_renewal_roadmap.md`

State: pre-push audit complete; remote observation pending

## Scope

This audit covers the completed post-v2.3 quality-floor and reader cycle plus
the successor-roadmap activation that was added after its 166-path activation
snapshot. Immediately before this audit document was added, the candidate
working tree contained 172 dirty paths: 100 tracked modifications and 72
untracked path roots. The six-path increase over the activation snapshot is
successor authority, status, schema, pointer, validator, and regenerated-proof
work performed after that snapshot; it is not a second empirical campaign.

The candidate begins at
`cb7493ae57d576a8bf5fcc54f375683ecf929b54`, the recorded post-v2.3 activation
baseline and current `origin/main` tip at audit time.

## Publication-safety review

- Git ignored paths remain excluded, including `.DS_Store`, `_site/`, `build/`,
  private source caches, source inbox payloads, and Lean build output.
- A binary-size scan found no candidate file above 20 MB. The largest declared
  release binary is the 4.2 MB exact curated-reader HTML archive under
  `editions/reader_manuscript/v2_0/artifacts/`.
- A credential-pattern scan covered 339 candidate files and found zero private
  key, GitHub token, AWS key, Google API key, OpenAI key, or Slack token hits.
- No raw source inbox, private cache, local handoff packet, checkpoint, training
  row, or restricted Project Theseus payload is part of the candidate.
- Digest-bound raw model transcripts are exempted from Git's trailing-whitespace
  diagnostic only within
  `experiments/post_v2_3_evidence_campaigns/artifacts/model_outputs/*.txt`.
  Their exact byte digests are validated by the campaign adjudication; ordinary
  source, prose, schema, and result files retain normal whitespace checking.
- Rights remain all-rights-reserved except at already recorded exact historical
  tags. This handoff does not grant a new license, tag a release, or authorize a
  public reader artifact beyond existing records.

## Commit-shape decision

The quality packets, chapter prose, generated manifest fields, Lean modules,
fixtures, evidence transitions, reader v2.0 records, release/no-release truth,
proof manifest, registry, and validators are digest- and contract-coupled.
Artificially splitting them would create intermediate commits that fail the
repository's exact generated-artifact and evidence-consistency gates. The
completed cycle is therefore one atomic validation commit. A second commit will
record the observed commit SHA, GitHub Actions build, Pages deployment,
attestation result, and clean-tree state after the first commit is pushed.

Commit count is not treated as quality evidence. The boundary is justified by
an independently rerunnable validation surface, not by convenience.

## Required pre-push evidence

The exact staged candidate must pass:

1. generated scaffold and proof-manifest checks;
2. PR and deep validation-registry tiers;
3. Lean build;
4. clean Quarto HTML render;
5. live Human-view and all-chapter/all-viewport browser checks;
6. reader-spine, exact-reader-artifact, release-profile, schema, fixture,
   publication, public-truth, rights, and licensing gates;
7. credential-pattern, oversized-file, ignored/private-path, and `git diff
   --check` audits, with only the digest-bound raw-transcript exception above;
   and
8. a staged-path review before commit.

Passing these gates does not prove external review, legal clearance, model
quality, deployed safety, AGI, ASI, or support-state movement.

## Remote completion boundary

This audit is not the P0 completion receipt. P0 remains in progress until the
tested commit is pushed to `main`, the commit-bound build artifact succeeds,
the build-once Pages deployment succeeds, the deployed-site attestation
succeeds for the same source SHA, and the follow-up receipt is committed and
observed without leaving an unexplained local residual.

# Artifact Steward Agents Context Ingestion Report

Date: 2026-06-25

## Provenance

- Local browser discussion packet: `sources/inbox/artifact_steward_agents_browser_note_2026-06-25/`
- Public chapter added: `artifact-steward-agents-and-living-project-governance`
- Placement: Part IV - Evidence, Implementation, and the Living Book, after `policy-optimization-and-learning-from-feedback`

## Public handling

The packet was treated as author-intent and planning context only. The public chapter does not quote the private browser discussion verbatim, does not cite it as evidence, and does not use it to promote any claim support state.

## Material extracted

- The need for durable artifacts to carry bounded steward agents across inception, planning, funding, compute allocation, contributor coordination, release, maintenance, governance, and sunset.
- The distinction between steward, owner, maintainer, contributor, worker, reviewer, funder, and governance participant.
- The need for artifact steward charters, project work contracts, contribution ledgers, steward action decisions, treasury limits, governance rules, and sunset review records.
- The separation of authorship, review, evidence credit, compensation, reputation, and governance effects.
- The autonomy-mode ladder from manual to assisted, bounded autonomous, community governed, and sunset operation.
- The treasury-mode ladder for manual treasury, budgeted autonomy, bounty escrow, recurring operations, compute rental, governed treasury, and emergency freeze.
- The event-taint boundary for untrusted issues, pull requests, comments, workflow events, worker outputs, benchmark artifacts, and external prompts.
- The project-federation framing where artifact stewards, personal hives, public hives, CI runners, and rented compute interact only through explicit contracts and evidence bundles.
- Failure modes around mission drift, treasury drain, contribution gaming, governance capture, untrusted workflow injection, AI maintainer monopoly, and zombie project continuation.

## Evidence boundary

- Record-shape schemas and fixtures were later added for `ArtifactStewardCharter`, `ProjectWorkContract`, `ContributionLedgerEntry`, `TreasuryPolicyRecord`, `EventTaintRecord`, `StewardActionDecision`, and `SunsetReviewRecord`; narrow finite Lean predicates were implemented for dispatch boundaries, protected-action approval checks, release evidence gates, and sunset-work blocking.
- No steward bot, treasury executor, governance system, contributor ledger service, project-work dispatcher, or sunset protocol was implemented or behaviorally tested.
- External source records and conservative source notes now exist for selected adjacent systems and risks: GitHub webhooks, GitHub self-hosted runners, OpenZeppelin Governor, Open Collective, GitHub Sponsors, Akash, Golem, agentic workflow injection, and DAO delegation concentration.
- Those external notes ground nearby tooling and risk patterns only; they do not prove that the proposed steward layer is implemented, lawful, financially safe, or capture-resistant.
- The chapter remains `Design rationale` with `argument` support.

## Follow-up queue

- Add public source records and source notes for remaining governance and funding topics: grants, bounty platforms, package-maintainer sustainability, software supply-chain security, and legal/tax treatment of stewarded treasuries.
- Extend the schema family further only after a specific steward prototype requires narrower records for grants, bounties, supply-chain intake, or legal/tax review.
- Add behavioral steward, treasury, event-taint, project-federation, contribution-ledger, autonomy-transition, and sunset-protocol tests before claiming steward-agent behavior beyond finite record predicates.

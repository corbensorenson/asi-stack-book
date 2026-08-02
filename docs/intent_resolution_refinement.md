# Human Intent resolution-to-contract refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`lean/AsiStackProofs/IntentResolutionRefinement.lean` replaces two assumption-restating preservation/authority declarations and three literal intake-summary declarations with a reachable request-to-contract model. The model keeps root intent, contract version, constraint and stop-condition hashes, authority ceiling, approved authority, ambiguity, accepted-contract, re-contract, block, and logical-time state explicit.

Lean now gives each event kind explicit write ownership. Parse and accepted re-contract are the only payload writers; authority review and accepted re-contract are the only approved-authority writers. Across arbitrary successful runs, 25 declarations preserve root intent, the original ceiling, and approved-authority boundedness, extract recursive trace validity, and prove event-batch composition. Four witnesses cover re-contract, clarification, unchanged continuation, and rejection.

`python3 scripts/validate_intent_resolution_refinement.py` independently consumes the prior intake and re-contract results and the complete plan-execution fixture inventory. It checks 4 reachable traces/14 events, all 14 prefixes, 18 batch compositions, 4 valid and 6 invalid intake cases, 6 intake signals, 2 valid and 7 invalid re-contract cases, 13 plan fixtures, and 40/40 state-noninterfering semantic mutations.

## Exact boundary

This is structured finite-record evidence. It does not prove natural-language intent understanding, semantic completeness, user preference fidelity, legitimate authority extraction, prompt-injection containment, source privacy, downstream dispatch enforcement, user satisfaction, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. Hashes, authority, receipts, scenario labels, and source records are trusted inputs. No effect is executed and no support or release transition is created.

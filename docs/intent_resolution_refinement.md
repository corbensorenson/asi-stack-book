# Human Intent resolution-to-contract refinement receipt

Recorded: 2026-07-15
Roadmap: `post-v2.3-claim-proof-and-sota-challenge-roadmap` P2/M3
Support-state effect: `none`

## Outcome

`lean/AsiStackProofs/IntentResolutionRefinement.lean` replaces two assumption-restating preservation/authority declarations and three literal intake-summary declarations with a reachable request-to-contract model. The model keeps root intent, contract version, constraint and stop-condition hashes, authority ceiling, approved authority, ambiguity, accepted-contract, re-contract, block, and logical-time state explicit.

Lean proves that an accepted compile preserves the exact constraint hash, stop-condition hash, and approved authority; a material downstream delta enters re-contract state; and an accepted re-contract increments the version without exceeding the authority ceiling. A five-event witness reaches accepted contract version 2 after a material-means delta and explicit re-contract. Countermodels reject missing intent payload, prohibited action, hidden override, authority widening, constraint substitution, silent material-delta continuation, and re-contract without a receipt.

`python3 scripts/validate_intent_resolution_refinement.py` independently consumes the prior intake and re-contract results and the complete plan-execution fixture inventory. It records 4 valid and 6 invalid intake cases, 6 intake signals, 2 valid and 7 invalid re-contract cases, 13 plan fixtures (3 valid and 10 invalid), the five-event witness, and 30 of 30 rejected semantic mutations.

## Exact boundary

This is structured finite-record evidence. It does not prove natural-language intent understanding, semantic completeness, user preference fidelity, legitimate authority extraction, prompt-injection containment, source privacy, downstream dispatch enforcement, user satisfaction, natural-workload usefulness, reproduction, transfer, safety, SOTA, AGI, ASI, or chapter-core support. Hashes, authority, receipts, scenario labels, and source records are trusted inputs. No effect is executed and no support or release transition is created.

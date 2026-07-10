# Reviewer Capacity and Oversight

Last updated: 2026-07-10

A reviewer name or owner field is not an oversight guarantee. The capacity
registry separates seven questions: assignment, competence scope,
independence, conflicts, measured load, response limits and substitute, and
measured review quality. A decision that explicitly claims independent review
fails closed when any required capacity is missing, expired, conflicted,
overloaded, unmeasured, or outside the reviewer's competence.

The current state is intentionally blunt. The author/program-owner role is
assigned internally but is not independent, has structurally disclosed
conflicts, and has no measured load or review-quality claim. Formal-methods,
safety/governance, and systems/editorial roles are deferred until after the
author declares the book complete and have no assigned principals. They cannot
satisfy or create independent-review claims, but they are not prepublication
completion gates.
The internal owner may preserve a blocker, narrow a claim, or make an
authorial decision; that role cannot manufacture independent acceptance.

For any optional post-publication review, `principal_ref` should be a public or appropriately
anonymized identity, competence evidence must match the decision class,
conflicts must be disclosed, load must be observed against a stated maximum,
response commitments need expiry, and the substitute must have enough
authority and expertise for the fallback. Review quality requires sampled
decisions, a stated method, detected defects and known misses; completion
counts alone are not quality.

`scripts/validate_reviewer_capacity.py` rejects assignment without a principal,
an unmeasured capacity claim, measured quality without samples, and a missing
escalation substitute. The registry is governance preparation, not proof of
reviewer competence, availability, independent review, safety, or claim truth.

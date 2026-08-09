# Writing and Story Standard

## Contents

- Teaching order
- Promise selection
- Narration structure
- Sentence craft
- Compression pass
- Script acceptance
- Read-aloud review
- Failure patterns

## Teaching order

Use pedagogical order rather than book order. Begin with a concrete case the
viewer can hold in working memory. Let an abstraction earn its name by solving
that case. This follows Grant Sanderson's advice to put concrete examples
before general frameworks and to avoid starting with definitions.

The opening should make the promise and its consequence visible within 15
seconds. Use an information gap only when it is honest. Favor a specific
situation:

- a model update passes tests but breaks rollback;
- two routes return the same answer at very different governance cost;
- a permission label allows an effect its owner did not intend; or
- a memory system retrieves the right fact from the wrong authority domain.

When the visible evidence makes a prediction useful, ask what should happen
and allow time to reason. Resolve it by changing objects on screen, not by
announcing a thesis. Do not manufacture a misconception or question merely to
fit a preferred story shape.

The title and thumbnail make a promise. The opening should visibly begin
delivering that promise before it introduces context. Use the first 15 seconds
for the most concrete goal, relation, decision, or tension, not a logo, chapter
number, agenda, or recap.

## Promise selection

Write at least three candidate teaching promises before choosing one. A strong
promise describes one observable transfer: after watching, the viewer can
predict a route, explain a failure, distinguish two states, or apply a mechanism
to a changed case. Select for consequence, visual tractability, transfer value,
and fit with the chapter's evidence ceiling.

Reject a promise that is really a coverage list. “Trace the record through
identity, authority, custody, recovery, cost, and residuals” describes chapter
inventory, not learning. Keep one case, one central mechanism, relationship, or
tradeoff, one discriminating test or counterexample, one evidence boundary, and
at most three introduced terms. Everything else stays in the book or becomes
another visual abstract.

## Narration structure

Choose the story form that matches the explanation rather than imposing one
house arc:

- **Failure diagnosis:** visible symptom -> tempting diagnosis -> hidden cause
  -> intervention -> retest.
- **Comparison:** common input -> route A -> route B -> shared accounting
  boundary -> decision.
- **Construction:** concrete goal -> binding constraint -> minimum added
  structure -> preserved invariant -> stress test.
- **Counterexample:** plausible rule -> matched cases -> opposite outcomes ->
  missing variable -> narrower rule.
- **Visual proof or derivation:** objects and assumptions -> invariant -> legal
  transformations -> conclusion -> formal scope.
- **Open question:** observation -> competing explanations -> discriminating
  test -> current evidence -> unresolved residual.

These are reusable grammars, not mandatory beat counts. Combine forms only when
the handoff itself teaches something. Do not force a failure, question, reveal,
or identical section sequence onto a chapter that does not warrant it. The
listener should hear a coherent explanation, not metadata from a content
pipeline.

Write the opening and payoff as a pair. The final beat should resolve or
complicate the exact object, prediction, or failure introduced at the start.
If it does neither, the hook was probably decorative.

Four to six macro moves are usually enough. Timed visual cues may split those
moves into smaller synchronization beats, but a new cue must not quietly add a
new topic. Record each move as the viewer's current model, the visible event
that changes it, and the resulting model. Name the event with a verb phrase
such as “the copied sensor appears independent” or “lineage collapses two votes
into one.” If the event can only be named as a category, it is still abstract.

Keep a beat only when it changes a named viewer belief, tests a prediction,
delivers a necessary qualifier, or gives processing time after a real change.
Merge or delete it when it merely restates narration, changes decoration,
introduces a synonym, or exists to keep the screen busy. A hold cannot smuggle
in a new term or relation.

## Sentence craft

- Keep one main idea per sentence.
- Prefer actor–verb–object order.
- Prefer “the gate blocks the write” to “the write is blocked by the gate.”
- Replace nominalizations with verbs: “the verifier rejects,” not “rejection is
  performed by the verifier.”
- Replace vague references such as “this,” “it,” and “that process” when two
  plausible antecedents exist.
- Use the same name for the same object throughout the video.
- Define acronyms only when they recur enough to repay the cost.
- Give numbers a comparison or visible scale.
- Put qualifications next to the claim they limit.
- Use contractions when they sound natural. Avoid fake informality.

Treat 24 words as a review trigger, not an automatic deletion rule. Split a
sentence when it contains two causal claims, a list, nested qualifications, or
more than one visual action.

Write in coherent performance blocks of roughly one thought or 15–45 seconds.
Paragraph breaks should direct a real change in pace, stance, or scene, not
force the TTS engine to restart after every sentence.

## Compression pass

Perform these passes in order:

1. Delete chapter-navigation language and repeated setup.
2. Delete facts that do not serve the one teaching promise.
3. Replace abstract nouns with visible actors and actions.
4. Split multi-idea sentences.
5. Remove narration that merely reads labels already on screen.
6. Remove adjectives that do not change a decision.
7. Move necessary nuance into the exact beat where overgeneralization could
   occur.
8. Replace evidence recitals with one plain-language boundary beside the
   relevant inference.
9. Remove claim IDs, support-state vocabulary, fixture and theorem counts,
   validator results, paths, chapter navigation, and invitations to read the
   next chapter.

Do not compress by accelerating speech. Compress by choosing, sequencing, and
showing.

## Script acceptance

The normal visual abstract is 280–520 spoken words at roughly 110–145 words per
minute. This is a diagnostic range, never a fill target; a shorter script is
valid when its transfer test still passes. A 520–600 word draft receives a
mandatory compression review. A draft above 600 words needs a concrete
`duration_rationale`; a draft above 650 words must be split or reselected.
These limits govern the derivative video, not the chapter's depth.

Before synthesis or detailed scene work, co-design sparse semantic keyframes
with the narration and require all of the following:

- the teaching promise is one short transferable outcome, not a list;
- the opening shows its consequence within 15 seconds;
- one concrete object or case persists through the payoff;
- no more than three new terms are required to follow the mechanism;
- every paragraph changes the viewer's model rather than inventories coverage;
- the evidence boundary is natural, local, and brief;
- the changed-case transfer question has predeclared success criteria; and
- every spoken sentence has a picture, relationship, or intentional audio-only
  purpose.

Run the narration-only audit before a timed beat plan exists. A passing linter
does not approve truth, taste, or pedagogy; it only prevents known structural
failures from consuming animation and audio work.

Record the full treatment and bind the narration digest. The script passes
only after read-aloud, truth, and visualizability reviews pass with no open
defect. A cold audience proxy belongs at release, where it can see the actual
artifact without leaked answers.

## Read-aloud review

Read at the intended pace while tapping once for every visual beat. Revise when:

- one breath contains multiple logical branches;
- a noun arrives before the visual object exists;
- a pronoun could name two objects;
- a qualifier arrives after the viewer has already formed a broader claim;
- the sentence sounds like an abstract, roadmap, or validator report; or
- tapping reveals ten seconds of new ideas with no visual state change.

## Failure patterns

- “This chapter asks…” foregrounds document structure instead of curiosity.
- “The core claim is…” tells before showing.
- A seven-item list gives equal weight to unequal ideas.
- A teaching promise joined by repeated “and” clauses is a chapter synopsis.
- Repeating problem/mechanism/trace/failure/evidence/non-claim/handoff wording
  makes different chapters feel identical.
- Speaking evidence labels, proof counts, fixture names, source paths, or the
  next chapter turns an explanation into an internal status report.
- Dense spoken caveats at the end cannot repair an overbroad visual earlier.
- Questions with no pause are decorative punctuation, not participation.
- A sensational hook that the explanation never pays off breaks trust.
- Constant urgency, jokes, or visual novelty flattens emphasis instead of
  creating it.
- A text card plus verbatim narration overloads the same verbal channel twice.

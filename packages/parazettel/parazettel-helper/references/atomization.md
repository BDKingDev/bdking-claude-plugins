# Atomization Guide

## Atomicity Gate

Reject or split a permanent note if any of these are true:

- It contains more than one independent claim.
- It can be split at `and`, `so`, `because`, `therefore`, or `which means` into useful standalone notes.
- It mixes an observation with an implementation tactic.
- It mixes a tactic with an expected outcome.
- It mixes a claim with transcript-specific framing that should live in literature.
- Its title sounds like a topic or bucket rather than a claim.

Do not split a note just because two sibling clauses could stand alone grammatically. Keep them together when they function as one definition, one standard, or one tightly bound criterion.

## Claim-Type Split Test

When a draft feels too broad, check whether it is trying to do more than one of these jobs:

- observation: what is true
- tactic: what to do because of it
- outcome: what direct consequence the source explicitly claims
- process or framework: a reusable step-by-step flow, setup sequence, operating procedure, or decision path — the "how to do this" of the source
- metaphor or model: a vivid explanatory handle that carries durable meaning
- source-specific material: framing, sequence, examples, personal context, or implementation detail that matters for provenance but does not deserve a standalone permanent note

A concrete process or named thing can outrank the abstract lesson behind it. When a source is actually about a specific object, design, or "how to do this," draft the thing-level and process candidates before higher-order abstractions — do not let the candidate set become all meta commentary. Numbers and unit economics, named tools, verbatim scripts, worked examples, and diagnostic questions are concrete carriers too — each is its own atom, not detail to be folded into the lesson's headline.

If a single draft is trying to do more than one of those jobs at once, it probably needs to be split.

## Action-Item Fit

When the source should produce action-system material as well as knowledge notes, classify the action note explicitly instead of treating every actionable sentence as a generic task.

- task: one concrete next action, usually verb-led, small enough to complete in one sitting or one bounded work block
- project: an active multi-step outcome with a defined end state; use when the source implies more than one task or checkpoint is needed
- area: an ongoing responsibility or stewardship lane with no clear terminal "done" state

Split a draft if it mixes any of these jobs:

- a durable knowledge claim and an execution item
- a project outcome and the individual tasks needed to complete it
- an area-level responsibility and the current project or task that serves it

Do not create `task`, `project`, or `area` notes just because a claim is useful or could inspire action later. Use action-item notes only when the user wants operational capture or the source itself clearly contains commitments, outcomes, or responsibilities that should live in the PARA/GTD layer.

Treat `status`, `due_date`, `priority`, `remind_at`, and similar fields as routing metadata after the note type is clear. They do not replace atomization, and they should not be used to hide that a single draft is actually multiple notes.

## Preferred Permanent Note Shape

- Title: one claim
- Body: 1 to 3 sentences
- One concept only
- One short source line at the end
- Prefer wording that stays close to the source before abstracting into broader advice
- A permanent note may absorb 1 to 2 concrete source details, but it should not depend on a literature note to carry its core claim

## Pruning Filter

Cut a candidate as a standalone permanent note if any of these are true:

- it is weaker than another note that already contains the same point
- it is mostly setup, framing, or motivational fluff
- it only states a benefit that works better as the second sentence of another note
- it is too generic to be worth linking independently later
- it is valuable as transcript-specific context but not strong enough to survive as a permanent note on its own

When two clauses work together to define one standard, keep them in one note body rather than creating separate notes.

If a candidate fails as a permanent note but still preserves useful source context, it belongs in literature rather than as a standalone permanent note.

**A distinct reframe, inversion, or special case of an existing note is its own atom — not a fold.** Same topic is not the same claim. If a draft and its closest existing match point in different directions (e.g. "disgust is the resistance to fight" vs "recruit disgust deliberately as a lever"), or the draft is a sharper sibling sitting next to the match, keep it and wire the relationship (`refines`, `contradicts`, or `related`). Over-folding adjacent reframes is the most common way a dense cluster quietly loses real atoms.

## Outcome Note Test

Create a separate outcome note only if all of these are true:

- the source names the consequence directly
- the consequence can be restated as a standalone claim
- the note does not need to repeat the tactic sentence to make sense

If those checks fail, keep the consequence inside the tactic note instead of splitting it out.

## Literature Support Test

Material belongs primarily in a literature note when it is valuable because of source-specific framing rather than standalone claim strength.

Common literature-only material:

- transcript sequence
- speaker-specific examples
- personal program structure
- provenance or context that would weaken a permanent note if moved into the title
- implementation detail that clarifies the source but is not durable enough to stand alone

If a durable claim can stand alone without that source context, it should not stay trapped in literature.

Assume a literature note is invisible during normal retrieval. If future-you would expect to find a claim, example, contrast, named object, or sequence through an ordinary note search, it cannot live only in a literature note — pull it into a permanent, structure, or hub note body. After creating a literature note, run one more pass to externalize anything retrieval-worthy still trapped in it.

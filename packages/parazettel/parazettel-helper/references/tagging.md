# Tagging discipline (controlled vocabulary)

Tags are **secondary aids** — retrieval lives in titles, bodies, and links. A
tag earns its place only if you would deliberately *filter on it* to find this
note later.

The vault's tag vocabulary sprawled past 7,000 tags (≈80% used exactly once,
full of near-duplicates and one-off coinages) because every ingestion minted
freeform tags. A manual dedup cut it to ~4,500. The rules below are calibrated
from that cleanup so new tags don't re-grow the sprawl. **The owner's stance:
the sprawl lever is NOT aggressive merging — it's not minting junk in the first
place, while still keeping genuinely distinct, specific handles.**

## Selecting tags for a note

1. **Find existing tags semantically, per note**: call
   `pzk_suggest_tags(text=<the note's claim>)` for the closest existing tags by
   meaning. (`pzk_get_all_tags` lists every tag for a full sweep, or when
   embeddings are off.)
2. **Reuse an existing tag when it's a true synonym or a clean sub-instance** of
   the concept. Prefer the **more descriptive** spelling as canonical even if
   it's less used (`emotional-contagion` over `contagion`, `lead-generation`
   over `lead-gen`, `dnd` over `d-and-d`). Reuse the existing named tag if one
   exists (`lizard-brain`, not a new `crocbrain`).
3. **Do NOT force a distinct concept under a broad parent** just to reuse. If the
   distinction is search-useful, keep the specific handle — the owner values
   specificity (`ab-testing` stays itself, not folded into `testing`;
   `abandoned-cart` is not `email`; `impact-statement` is not `mission-statement`).
   When in doubt between reuse and a distinct handle, prefer the distinct handle;
   when in doubt between a new tag and nothing, prefer nothing.
4. **2–4 tags per note.** One domain tag, optionally one sub-topic tag, plus any
   workflow tag the skill requires (e.g. `chat-capture`). More tags dilute
   tag-based similarity rather than improve retrieval.
5. **Form**: lowercase, hyphen-separated, singular where natural
   (`structure-note`, not `Structure_Notes`). The server normalizes case and
   separators on write, but it **cannot merge synonyms** — that is your job at
   selection time.
6. **GTD context/energy tags** (`@home`, `high-energy`) are applied
   automatically by `pzk_create_task`'s `context`/`energy_level` parameters — do
   not add them manually.

## The keep test (mint a new tag only if it passes)

Mint a new tag only when the concept is genuinely **absent** from the vocabulary
*and* the tag would be a reusable search handle — a concept you expect to tag
**again**, not a description of this one note. A good new tag is one you'd later
type into a filter on purpose to pull up this note and its siblings.

**Always give a distinct tag to named entities** — people, tools, apps,
frameworks, strategies, named methods (`hormozi`, `canva`, `filmora`,
`robbie-framework`, `blue-ocean`). Never fold a named entity into a generic
parent; reuse its existing tag if there is one, otherwise mint it.

**Keep specific-but-niche handles even at single use** when they're a real
retrieval target (`ren-faire`, `magic-item`, `combat-payoff`, `sqlalchemy`,
`facebook-pixel`). A big general category is also fine to keep when nothing
closer exists (`seasoning`, `architecture`).

## Do NOT mint (these are the junk that caused the sprawl)

- **Vague one-word abstractions** incoherent across notes — `concreteness`,
  `dual-purpose`, `forensic-completeness`, `signal`, `boundary`, `output`.
- **Title-echoing one-offs** that just restate this note's claim —
  `not-a-question`, `out-of-your-head`, `decide-then-streamline`.
- **Bare non-descriptive words** unsearchable on their own — `understood`,
  `leeching`, `debunk`, `expert`, `verbs`, `busy`.
- **Generic adjectives / verbs / process-noise** — `actionable`, `robotic`,
  `salesy`, `read-back`, `go-deeper`.
- **One-off metaphors / analogies** — `scaffolding`, `sermon`,
  `fishing-analogy`. The metaphor belongs in the note body, not a tag.
- **The source instead of the concept** — `transcript`, `voice-memo`; the note's
  `source` field already records this.

If a candidate tag's concept is already carried by the note's other tags, don't
add it. When a call is ambiguous, **judge by what the note is actually about,
not the tag's name** — read the claim, not the label.

## Anti-patterns

- Minting a near-synonym of an existing tag (`adhd` when `add-adhd` exists) —
  pick one, reuse it, prefer the more descriptive form.
- Folding a specific, distinct concept into a broad generic parent to "reuse" —
  that loses the specificity that makes the tag useful.
- Matching on spelling, not sense (homographs / false near-dups):
  `carrier`≠`career`, `mourning`≠`morning`, `state`≠`stage`,
  `markers`≠`makers`. Confirm the meaning before reusing a look-alike tag.

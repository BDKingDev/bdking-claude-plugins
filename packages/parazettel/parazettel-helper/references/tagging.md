# Tagging discipline (controlled vocabulary)

Tags are **secondary aids** — retrieval lives in titles, bodies, and links.
The vault's tag vocabulary sprawled to 2000+ tags (half used once, full of
near-duplicates like `emotion-regulation`/`emotional-regulation`) because every
ingestion minted freeform tags. These rules stop that.

## Rules

1. **Fetch the vocabulary once per session before tagging anything**: call
   `pzk_get_all_tags` at the start of the tagging step and keep the list in
   working memory for every note in the batch.
2. **Reuse the closest existing tag.** If an existing tag covers the concept —
   even imperfectly — use it. Prefer the more-used, more-general spelling.
3. **Mint a new tag only when the concept is genuinely absent** from the
   vocabulary, not merely phrased differently. A new tag should be a concept
   you expect to tag again, not a description of this one note.
4. **2–4 tags per note.** One domain tag, optionally one sub-topic tag, plus
   any workflow tag the skill requires (e.g. `chat-capture`). More tags do not
   improve retrieval; they dilute tag-based similarity.
5. **Form**: lowercase, hyphen-separated, singular where natural
   (`structure-note`, not `Structure_Notes`). The server normalizes case and
   separators on write, but it cannot merge synonyms — that is your job at
   selection time.
6. **GTD context/energy tags** (`@home`, `high-energy`) are applied
   automatically by `pzk_create_task`'s `context`/`energy_level` parameters —
   do not add them manually.

## Anti-patterns

- Minting a near-synonym of an existing tag (`adhd` when `add-adhd` exists) —
  pick one, reuse it everywhere.
- Tagging the source instead of the concept (`transcript`, `voice-memo`) —
  the note's `source` field already records this.
- One-shot tags that describe the note's specific content — that's what the
  title is for.

---
name: pzk-personal-note
description: Converts a short or long source note, AI transcription, or personal voice memo into atomic linked Zettelkasten notes and action-item tasks using the parazettel MCP. Use whenever a user provides a raw transcript, Notion export, or markdown file to add to their knowledge base. Triggers on "process this note", "add this to my Zettelkasten", "atomize this", "convert this to Zettelkasten", or when a markdown file is provided with intent to add it to a vault.
compatibility: requires parazettel MCP (pzk_* tools); uses jdocmunch for long source files
---

Turn a source note into atomic permanent notes and action-item tasks via the parazettel MCP. Add a literature note only when source framing or provenance is worth preserving. Route action items to tasks via `pzk_create_task`.

**Treat literature notes as invisible during normal retrieval.** Anything future-you would search for — a claim, example, contrast, named object, or sequence — must live in a permanent, structure, or hub note body, not only in the literature note. After creating a literature note, run one more pass to externalize anything retrieval-worthy still trapped in it.

**These sources are typically personal voice memos or transcripts** — the speaker is also the vault owner. Their specific examples, reasoning chains, and personal framing are primary material, not noise to filter out.

**If jdocmunch is available** and the source is a long file: use `search_sections` / `get_section` to pull only relevant parts rather than loading the whole file into context. Process section by section — run the full two-phase workflow on each section, then do a final cross-section hub/structure check at the end.

## Workflow

### Phase 1 — Extract (graph-blind)

**If subagents are available:** spawn the `zettelkasten-helper:extractor` agent. If the source is a file, pass only the file path — the extractor has `Read` access and will read it directly. If the source is inline text (pasted into conversation), pass the text. The extractor returns a full candidate list with no graph awareness or pruning.

**If subagents are not available:** simulate the extractor by reading the source and writing out all candidates as if the vault were empty — no MCP calls, no consideration of existing notes. Treat this as a strict separate pass before any graph interaction.

The extractor surfaces:

- `observation`, `tactic`, `outcome` claims — see [atomization.md](../../references/atomization.md)
- `process-or-framework` — a reusable "how to do this" flow, setup sequence, or decision path; in personal transcripts this can outrank the abstract lesson behind it
- `action-item` — concrete things to do ("need to set up X", "should try Y this week")
- `object-or-design-decision` — specific choices about named things, tools, or mechanisms
- **Brainstorms, idea lists, and planning** — content/offer/module idea lists, course-design artifacts, swipe files, and loose "what could I make / what would help" ideation. Flag the whole brainstorm as a candidate (usually a `structure` note). This is durable provenance even when it is off-topic for the source, half-formed, rejected in the same breath, or a method the speaker was unsure about (flag those "to test"). The speaker searches for their own past ideas later — preserve them, and keep the reasoning for why an idea was set aside (that failure mode is often the sharpest note).
- **Metaphors and mental models** — if generative (applicable beyond this source), flag as its own candidate
- **Personal framing, lived examples, reasoning sequences** — flag for literature note even if not a standalone permanent
- **All topics present in the source, regardless of proportion** — a transcript that is 80% about marketing and 20% about relationships should produce permanent notes from both. Do not treat the minority topic as less worthy of capture; disparate, unexpected claims from an otherwise unrelated source are often the most valuable to pull.

Extract only what the **raw** source supports. If the source bundles an AI-generated summary, main points, or action-item list, use those as discovery aids — never mint a permanent-note claim that the raw transcript or body does not back up.

1. **Read** the source — via jdocmunch sections or from conversation context.
2. **Get the full candidate list** — do not consider existing notes yet.
3. **Decide on a literature note** — create one if the source is long, mixed, or has framing worth preserving. For personal transcripts, bias toward creating one. Keep the summary to 1–3 tight sentences stating the argument, not an abstract.

### Phase 2 — Prune and integrate

4. **Prune** — keep the smallest valid set of permanent notes. The goal is honest, specific insights grounded in what the source actually said — not general advice that could appear in any self-help article. Cut any candidate that: is generic enough to be true without this source, reads like conventional wisdom, or could have been written without the transcript. A pruned note should feel like something only this speaker, in this conversation, would say.
   - **Exception — brainstorms and planning are provenance, not pruned as "generic" or "transient":** a content/offer/module idea list, course-design artifact, or "what could I make" brainstorm is captured (usually as a `structure` note routed into the relevant cluster) and judged by provenance value, not by whether each line is a novel durable claim. The only ideation you skip is something already recorded in the graph. Never collapse a brainstorm into a no-note pass by calling it transient — including when it is off-topic for the source or was rejected in the same breath.
5. **Route action items** — candidates typed as `action-item` go to `pzk_create_task` instead of `pzk_create_note`. Use `source="voice"` for voice memos or `source="transcript"` for other transcripts, with `status="inbox"`. Follow the project resolution flow in [project-resolution.md](../../references/project-resolution.md).
6. **Enrichment pass** — for each **cut** knowledge candidate, search for the closest existing note and apply the atomicity gate (see [atomization.md](../../references/atomization.md)):
   - Keeps existing note at one idea → `pzk_update_note`
   - Would push existing note to two ideas → new note linked with `extends` or `supports`
   - No close match → drop or fold into literature note
7. **Graph comparison** — for each **surviving** knowledge candidate: search for duplicates. Link to existing if already covered; `pzk_update_note` if the source adds something durable.
8. **Create notes and links** — `pzk_create_note` then `pzk_create_link` immediately after each note. Tasks are created in step 5. **Tags follow the controlled vocabulary** (see [tagging.md](../../references/tagging.md)): call `pzk_get_all_tags` once before tagging the batch, reuse the closest existing tag, and mint a new one only when the concept is genuinely absent — never a near-synonym spelling of an existing tag. For large batches (5+ notes already pruned and deduped), `pzk_ingest_batch` creates all notes + links + tasks in one call with `#N` cross-references and a per-note dedup gate.
9. **Hub/structure check** — `pzk_find_central_notes` for the topic. Distinguish the two roles: a `hub` is a broad bucket/map of a cluster and its lanes; a `structure` note is the exact reusable scaffold — a sequence, flow, checklist, or decision path. Don't let one note do both jobs; if the cluster needs both a bucket and an exact flow, create both. Update an existing hub/structure note if found; create one only when several new permanents share a topic with no existing organizer.
10. **Post-create semantic audit** — run `pzk_find_similar_notes` on each note you just created, then make two passes over the neighbours it surfaces:
    - **Links** — add 1–2 high-value cross-vocabulary / cross-domain links the lexical sweep missed (`pzk_create_link`). Treat loosely-related hits as links, not fold/merge triggers.
    - **Tension check** — judge whether any close neighbour *conflicts* with the new note (an opposing claim, a competing recommendation, or a condition that contradicts it). `pzk_find_tensions` on the new note returns exactly this candidate set (unlinked same-topic neighbours) in one call. On a real tension, reconcile rather than ignore: link `contradicts` (the system auto-adds the reciprocal `contradicted_by`), or `refines` if one note is the special case that resolves the other, or `pzk_update_note` to add the qualifying condition — and surface the tension in the report.
    **Embeddings augment domain memory; they don't replace it.** A low or empty result *suggests* (does not prove) the note is novel — a few ideal matches sit in a different embedding region and surface in neither `search` nor `find_similar`. If you recall an obviously-relevant note that didn't appear, link it manually; several of the best links come only from memory.
11. **Verify** — `pzk_get_linked_notes` to confirm links.

## Tool Order

Use tools in this order unless there is a clear reason not to:

1. Draft and prune the local candidate set first (no MCP calls).
2. **Pre-create sweep** — `pzk_search_notes` (now hybrid lexical+semantic) on each surviving candidate's claim text. Candidates have no ID yet, so `pzk_find_similar_notes` can't run on them. Read the top score as a signal, not a verdict: a **low top score usually means novel → create** (but see the recall caveat in the audit step — it can also mean the best match sits in a different embedding region); a strong, on-claim match → **fold/update**, but first open the match and confirm it's the **same atomic claim, not just the same topic** (dense clusters score genuinely distinct atoms high — over-folding is worst exactly there); a moderate, loosely-related match is a **link candidate, not a fold**. Query with the **full claim** (title + a sentence), not a terse keyword — phrasing strongly affects recall; with embeddings on, `pzk_find_similar_to_text` runs this semantic check on the draft text directly (calibrated cosine).
3. `pzk_get_note` when an existing note might need updating.
4. `pzk_get_all_tags` once, before tagging — reuse existing tags per [tagging.md](../../references/tagging.md).
5. `pzk_create_note` / `pzk_update_note` / `pzk_create_task` to create items (or `pzk_ingest_batch` for a large pre-deduped batch).
6. `pzk_create_link` to connect source and derived notes immediately.
7. **Post-create audit** — `pzk_find_similar_notes` on each *newly created* note. This is the semantic pass: it catches cross-vocabulary / cross-domain links (and productive tensions) the lexical sweep missed — often 1–2 good links per note, though some notes the pass is purely confirmatory. Add those links; don't retro-fold loosely-related hits. `pzk_find_tensions` surfaces the unlinked-neighbour set for the tension judgment in one call.
8. `pzk_get_linked_notes` to verify the result.

## Note Content Formats

**Permanent note — pass as `content`:**

```text
[Body: 1–3 sentences. Title already states the claim — do not restate it.
Second sentence adds a specific detail, named consequence, or edge case
from the source. Cut any sentence that starts "this means" or "this is why"
— that is commentary, not a new fact.
Preserve the speaker's original tone and language where possible — atomize
the idea but don't sand off the voice. If the source uses a distinctive word
or phrase, keep it.]

Source: [path/filename or description of source]
```

**Literature note — pass as `content`:**

```text
Source note: [path/filename]
Source type: AI Transcription
Uploaded by: [name]
Recommended area: [area]
Created time: [original created time from source metadata]
Duration: [duration from source metadata, if present]
Original recording: [URL if present]

Summary:
[1–3 sentences stating the argument. Include one concrete anchor detail
from the source — a specific example, named analogy, or vivid particular.]
```

## Linking

Apply `pzk_create_link` immediately after each note — don't batch at the end. Pass the description as the `description` parameter on the tool call, not written into the note content body.

```text
pzk_create_link(
  source_id="...",
  target_id="...",
  link_type="supports",
  description="Source note defines the core workflow this permanent note distills."
)
```

- `supports` — literature/source → each derived permanent and task
- `refines` — more specific → more general
- `extends` — note adds a distinct consequence or application
- `related` — adjacent, neither specializes the other
- `contradicts` — the note makes a claim that conflicts with the target's (reciprocal `contradicted_by` is auto-added); use when the audit finds a genuine tension to reconcile
- `reference` — hub/structure → notes it indexes

Note: tasks created via `pzk_create_task` with a `project_id` are automatically linked to their project (PART_OF/HAS_PART). You still need to create `supports` links from the literature note to each task.

## Output Report

1. **Candidates** — full list from Phase 1, including literature note flags and action-item typing.
2. **Pruning** — what was cut and why; anything folded back in.
3. **Action items** — tasks created, with project assignment and status.
4. **Enrichment** — cut candidates that strengthened an existing note.
5. **Literature note** — created or skipped, and why.
6. **Notes created/updated** — title, type, note ID; new vs. updated.
7. **Links** — relationship type + one-line rationale each.
8. **Hub/structure actions** — what was done and why, or why nothing was needed.

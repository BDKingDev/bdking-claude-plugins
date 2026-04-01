---
name: pzk-personal-note
description: Converts a short or long source note, AI transcription, or personal voice memo into atomic linked Zettelkasten notes and action-item tasks using the parazettel MCP. Use whenever a user provides a raw transcript, Notion export, or markdown file to add to their knowledge base. Triggers on "process this note", "add this to my Zettelkasten", "atomize this", "convert this to Zettelkasten", or when a markdown file is provided with intent to add it to a vault.
compatibility: requires parazettel MCP (pzk_* tools); uses jdocmunch for long source files
---

Turn a source note into atomic permanent notes and action-item tasks via the parazettel MCP. Add a literature note only when source framing or provenance is worth preserving. Route action items to tasks via `pzk_create_task`.

**These sources are typically personal voice memos or transcripts** — the speaker is also the vault owner. Their specific examples, reasoning chains, and personal framing are primary material, not noise to filter out.

**If jdocmunch is available** and the source is a long file: use `search_sections` / `get_section` to pull only relevant parts rather than loading the whole file into context. Process section by section — run the full two-phase workflow on each section, then do a final cross-section hub/structure check at the end.

## Workflow

### Phase 1 — Extract (graph-blind)

**If subagents are available:** spawn the `zettelkasten-helper:extractor` agent. If the source is a file, pass only the file path — the extractor has `Read` access and will read it directly. If the source is inline text (pasted into conversation), pass the text. The extractor returns a full candidate list with no graph awareness or pruning.

**If subagents are not available:** simulate the extractor by reading the source and writing out all candidates as if the vault were empty — no MCP calls, no consideration of existing notes. Treat this as a strict separate pass before any graph interaction.

The extractor surfaces:

- `observation`, `tactic`, `outcome` claims — see [atomization.md](../../references/atomization.md)
- `action-item` — concrete things to do ("need to set up X", "should try Y this week")
- `object-or-design-decision` — specific choices about named things, tools, or mechanisms
- **Metaphors and mental models** — if generative (applicable beyond this source), flag as its own candidate
- **Personal framing, lived examples, reasoning sequences** — flag for literature note even if not a standalone permanent
- **All topics present in the source, regardless of proportion** — a transcript that is 80% about marketing and 20% about relationships should produce permanent notes from both. Do not treat the minority topic as less worthy of capture; disparate, unexpected claims from an otherwise unrelated source are often the most valuable to pull.

1. **Read** the source — via jdocmunch sections or from conversation context.
2. **Get the full candidate list** — do not consider existing notes yet.
3. **Decide on a literature note** — create one if the source is long, mixed, or has framing worth preserving. For personal transcripts, bias toward creating one. Keep the summary to 1–3 tight sentences stating the argument, not an abstract.

### Phase 2 — Prune and integrate

4. **Prune** — keep the smallest valid set of permanent notes. The goal is honest, specific insights grounded in what the source actually said — not general advice that could appear in any self-help article. Cut any candidate that: is generic enough to be true without this source, reads like conventional wisdom, or could have been written without the transcript. A pruned note should feel like something only this speaker, in this conversation, would say.
5. **Route action items** — candidates typed as `action-item` go to `pzk_create_task` instead of `pzk_create_note`. Use `source="voice"` for voice memos or `source="transcript"` for other transcripts, with `status="inbox"`. Follow the project resolution flow in [project-resolution.md](../../references/project-resolution.md).
6. **Enrichment pass** — for each **cut** knowledge candidate, search for the closest existing note and apply the atomicity gate (see [atomization.md](../../references/atomization.md)):
   - Keeps existing note at one idea → `pzk_update_note`
   - Would push existing note to two ideas → new note linked with `extends` or `supports`
   - No close match → drop or fold into literature note
7. **Graph comparison** — for each **surviving** knowledge candidate: search for duplicates. Link to existing if already covered; `pzk_update_note` if the source adds something durable.
8. **Create notes and links** — `pzk_create_note` then `pzk_create_link` immediately after each note. Tasks are created in step 5.
9. **Hub/structure check** — `pzk_find_central_notes` for the topic. Update an existing hub/structure note if found. Create a structure note only when several new permanents share a topic with no existing index.
10. **Verify** — `pzk_get_linked_notes` to confirm links.

## Tool Order

Use tools in this order unless there is a clear reason not to:

1. Draft and prune the local candidate set first (no MCP calls).
2. `pzk_find_similar_notes` on each surviving candidate as the first-pass similarity sweep.
3. `pzk_search_notes` for targeted duplicate checking and cross-domain link discovery.
4. `pzk_get_note` when an existing note might need updating.
5. `pzk_create_note` / `pzk_update_note` / `pzk_create_task` to create items.
6. `pzk_create_link` to connect source and derived notes immediately.
7. `pzk_get_linked_notes` to verify the result.

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

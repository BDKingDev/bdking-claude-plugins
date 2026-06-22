---
name: pzk-chat-session
description: Reviews the current conversation and captures Zettelkasten-worthy ideas as permanent notes and action items as tasks via the parazettel MCP, then runs a full linking pass to integrate them into the graph. Use at the end of a coding or problem-solving session to preserve architectural decisions, debugging insights, and design discoveries before the conversation ends. Triggers on "extract ideas from this chat", "capture insights from conversation", "save ideas to Zettelkasten", "/pzk-chat-session", or when the user asks to save or capture ideas from the current session.
argument-hint: "[optional: topic filter, e.g. 'only architecture decisions']"
---

Review the current conversation and create **permanent notes** for knowledge insights and tasks for action items, then run a **full linking pass** so every note is integrated into the graph rather than left orphaned. Notes are created directly as permanent notes with **no status** — capture at the quality bar of a durable note, not a draft to promote later.

## What to look for

**Capture as permanent notes (knowledge insights):**

- Architectural decisions and their rationale ("we chose X over Y because Z")
- Debugging insights that reveal non-obvious system behavior
- Design trade-offs articulated during discussion
- Pattern discoveries ("this is the third time we've seen X cause Y")
- Process improvements identified ("next time we should do X before Y")
- Mental models or analogies introduced that are generative beyond this conversation

**Capture as tasks (action items):**

- Concrete things to do identified during the session ("we need to refactor X", "should add tests for Y")
- Follow-up work committed to ("I'll open a PR for that", "need to check with the team about X")
- Route these through `pzk_create_task` with `source="chat"` and `status="inbox"`
- Follow the project resolution flow in [project-resolution.md](../../references/project-resolution.md)

**Skip:**

- Mechanical code changes (renamed a variable, fixed a typo)
- Routine CRUD operations with no design insight
- Configuration changes without interesting rationale
- Decisions that are entirely standard practice with no project-specific twist
- Information already well-covered in existing permanent notes (check with `pzk_search_notes` before creating)

## Workflow

1. **Scan the conversation** for items matching the capture criteria above. Work from memory — do not re-read files or run commands.

2. **Draft candidates** — for each idea, draft:
   - A claim-shaped title (not a topic bucket)
   - A 1–2 sentence body close to how the idea was expressed in the conversation — written to stand on its own as durable knowledge, with no session framing in the body (provenance goes on the `origin` param, step 4)
   - Relevant tags: `chat-capture` always, plus 1–2 topic tags REUSED from the vault. Get a meaning-ranked shortlist with `pzk_suggest_tags(text=<the draft claim>)` (the closest existing tags by meaning — no scanning the whole alphabetical list) and reuse the closest; mint a new tag only when the concept is genuinely absent. Falls back to `pzk_get_all_tags` when embeddings are off — see [tagging.md](../../references/tagging.md).
   - Type: `knowledge` (permanent note) or `action-item` (task)

3. **Pre-create check** — for each candidate, run `pzk_search_notes` (now hybrid lexical+semantic) on its claim text. (Candidates have no ID yet, so `pzk_find_similar_notes` can't run on them pre-create.) Read the top score as a signal, not a verdict: **low usually means novel → keep** (but see the recall caveat in the audit step); a **strong, on-claim match = skip or merge — after opening it to confirm it's the same atomic claim, not just the same topic** (dense clusters score distinct atoms high); a **moderate, loosely-related match = keep and link, not merge**. `pzk_create_note`'s own dedup confirm catches true paraphrase duplicates. Query with the **full claim**, not a terse keyword — phrasing strongly affects recall; with embeddings on, `pzk_find_similar_to_text` runs this semantic check on the draft text directly (calibrated cosine).

4. **Create items:**
   - Knowledge insights → `pzk_create_note` with `note_type="permanent"` and **no `status`** (leave it unset — these are durable notes, not inbox drafts). **Route each note to the area it belongs to**: find the best fit with `pzk_suggest_areas(text=<the draft claim>)` (a semantic shortlist of areas) or browse `pzk_list_areas`, or route under a project with `project_id` (the area is then inherited); ask the user if the area is ambiguous. Knowledge notes should live under an area, not float unrouted. Set `origin="chat session: <brief description>"` for provenance instead of writing session framing into the body.
   - Action items → `pzk_create_task` with `source="chat"`, `status="inbox"` — requires project resolution (see [project-resolution.md](../../references/project-resolution.md))

5. **Full linking pass** — every new note must be integrated, not orphaned. Do this for each note, immediately after it is created (don't batch to the end):

   - **Inter-note links** — link the new notes to each other where they relate, using the right type (below). Apply `pzk_create_link` right after creating each note; pass the rationale as the `description` parameter, not in the note body.
   - **Hub/structure check** — run `pzk_find_central_notes` for the topic. A `hub` is a broad map of a cluster; a `structure` note is an exact reusable scaffold (sequence, flow, checklist, decision path). Link each new permanent to the hub/structure it sits under (`reference`/`supports`). Update an existing organizer if the cluster has one; create a new hub/structure only when several new notes share a topic with no existing organizer.
   - **Semantic audit + tensions** — run `pzk_find_similar_notes` (or `pzk_find_tensions`) on each note you created, then two passes over the neighbours: (1) **links** — add 1–2 cross-vocabulary / cross-domain links the lexical sweep missed (`pzk_create_link`; link, don't fold loosely-related hits); (2) **tension check** — if a close neighbour *conflicts* with the new note (opposing claim, competing recommendation, contradicting condition), reconcile rather than ignore: link `contradicts` (reciprocal `contradicted_by` is auto-added) or `refines`, or `pzk_update_note` to add the resolving condition, and flag it in the report. Embeddings augment domain memory, not replace it — a low/empty result doesn't prove novelty; if you recall an obviously-relevant note that didn't surface, link it manually.

   Link-type quick reference: `supports` (general → specific evidence), `refines` (specific → general), `extends` (adds a distinct consequence or application), `related` (adjacent, neither specializes the other), `contradicts` (genuine tension to reconcile), `reference` (hub/structure → the notes it indexes). Tasks created with a `project_id` are auto-linked to their project (PART_OF/HAS_PART) — no manual link needed.

6. **Report** — present the created items as a numbered list (title + type + ID), grouped by type, followed by:
   - **Links** — each one's relationship type + a one-line rationale
   - **Hub/structure actions** — what was created/updated, or why nothing was needed
   - **Tensions** — any conflicts reconciled and how

   There is no promotion step — the notes are already permanent. Tasks are first-class objects with status tracking and need no promotion either.

## Note format

Pass as `content`:

```text
[1–2 sentences. Title already states the claim. Body adds the specific detail,
context, or consequence from the conversation. Keep it close to how it was
expressed — don't abstract prematurely. No "Session:" framing in the body.]
```

- Tags to always include: `chat-capture`
- Provenance: set `origin="chat session: <brief description of what the session was about>"` on the `pzk_create_note` call (keeps the permanent-note body clean while preserving where it came from)

## When nothing is worth capturing

If the conversation contains no ideas that pass the capture criteria — it was purely mechanical implementation with no design decisions or insights — say so explicitly rather than creating low-quality notes. A short message: "No Zettelkasten-worthy ideas found in this session — the work was primarily [description]."

---
name: pzk-chat-session
description: Reviews the current conversation and captures Zettelkasten-worthy ideas as fleeting notes and action items as tasks via the parazettel MCP. Use at the end of a coding or problem-solving session to preserve architectural decisions, debugging insights, and design discoveries before the conversation ends. Triggers on "extract ideas from this chat", "capture insights from conversation", "save ideas to Zettelkasten", "/pzk-chat-session", or when the user asks to save or capture ideas from the current session.
argument-hint: "[optional: topic filter, e.g. 'only architecture decisions']"
---

Review the current conversation and create fleeting notes for knowledge insights and tasks for action items. These are lightweight captures — at the end, show the created items and offer to promote fleeting notes to permanent notes.

## What to look for

**Capture as fleeting notes (knowledge insights):**

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
   - A 1–2 sentence body close to how the idea was expressed in the conversation
   - Relevant tags: `chat-capture` always, plus 1–2 topic tags REUSED from `pzk_get_all_tags` (fetch once per session; mint a new tag only when the concept is genuinely absent — see [tagging.md](../../references/tagging.md))
   - Type: `knowledge` (fleeting note) or `action-item` (task)

3. **Pre-create check** — for each candidate, run `pzk_search_notes` (now hybrid lexical+semantic) on its claim text. (Candidates have no ID yet, so `pzk_find_similar_notes` can't run on them pre-create.) Read the top score as a signal, not a verdict: **low usually means novel → keep** (but see the recall caveat in the audit step); a **strong, on-claim match = skip or merge — after opening it to confirm it's the same atomic claim, not just the same topic** (dense clusters score distinct atoms high); a **moderate, loosely-related match = keep and link, not merge**. `pzk_create_note`'s own dedup confirm catches true paraphrase duplicates. Query with the **full claim**, not a terse keyword — phrasing strongly affects recall; with embeddings on, `pzk_find_similar_to_text` runs this semantic check on the draft text directly (calibrated cosine).

4. **Create items:**
   - Knowledge insights → `pzk_create_note` with `note_type="fleeting"` — lightweight capture for user review
   - Action items → `pzk_create_task` with `source="chat"`, `status="inbox"` — requires project resolution (see [project-resolution.md](../../references/project-resolution.md))

5. **Post-create audit** — run `pzk_find_similar_notes` on each note you just created, then two passes over the neighbours: (1) **links** — add 1–2 cross-vocabulary / cross-domain links the lexical check missed (`pzk_create_link`; link, don't fold); (2) **tension check** — if a close neighbour *conflicts* with the new note (opposing claim, competing recommendation, contradicting condition), reconcile rather than ignore: link `contradicts` (reciprocal `contradicted_by` is auto-added) or `refines`, or `pzk_update_note` to add the resolving condition, and flag it in the report. Embeddings augment domain memory, not replace it — a low/empty result doesn't prove novelty; if you recall an obviously-relevant note that didn't surface, link it manually.

6. **Report and offer promotion** — present the created items as a numbered list (title + ID), grouped by type. Then ask:

   > "Would you like to promote any fleeting notes to permanent notes? If so, which ones? I can refine the title, strengthen the body, and reclassify them now."

   For each note the user selects: use `pzk_update_note` to set `note_type="permanent"` and refine the content to meet the permanent note standard — claim-shaped title, 1–3 sentence body, no session framing.

   Tasks do not need promotion — they are already first-class objects with status tracking.

## Note format

Pass as `content`:

```text
[1–2 sentences. Title already states the claim. Body adds the specific detail,
context, or consequence from the conversation. Keep it close to how it was
expressed — don't abstract prematurely.]

Session: [brief description of what the session was about]
```

Tags to always include: `chat-capture`

## When nothing is worth capturing

If the conversation contains no ideas that pass the capture criteria — it was purely mechanical implementation with no design decisions or insights — say so explicitly rather than creating low-quality notes. A short message: "No Zettelkasten-worthy ideas found in this session — the work was primarily [description]."

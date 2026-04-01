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
   - Relevant tags: `chat-capture` always, plus 1–2 topic tags (e.g., `architecture`, `debugging`, `performance`)
   - Type: `knowledge` (fleeting note) or `action-item` (task)

3. **Dedup check** — for each candidate, run `pzk_find_similar_notes` if a very close note seems likely to exist. Skip or merge if the vault already has this idea in equal or stronger form.

4. **Create items:**
   - Knowledge insights → `pzk_create_note` with `note_type="fleeting"` — lightweight capture for user review
   - Action items → `pzk_create_task` with `source="chat"`, `status="inbox"` — requires project resolution (see [project-resolution.md](../../references/project-resolution.md))

5. **Report and offer promotion** — present the created items as a numbered list (title + ID), grouped by type. Then ask:

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

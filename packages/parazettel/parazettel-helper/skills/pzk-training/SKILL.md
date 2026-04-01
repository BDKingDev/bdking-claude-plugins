---
name: pzk-training
description: Converts a company training video transcript or written SOP document into atomic linked Zettelkasten notes and action-item tasks using the parazettel MCP. Use whenever a user provides a transcript from an internal training video, onboarding recording, instructional session, standard operating procedure, or procedural document about company-specific services, tools, or workflows. Triggers on "process this training", "process this SOP", "training video to Zettelkasten", "capture this procedure doc", "extract from training transcript", "capture this onboarding video", or when a transcript or structured document is identified as internal training or procedural content.
compatibility: requires parazettel MCP (pzk_* tools); uses jdocmunch for long sources
---

Turn a company training source — video transcript or written SOP/procedure document — into atomic permanent notes and action-item tasks using the parazettel MCP. Training content maps to procedures, system knowledge, policies, and gotchas — preserve company-specific terminology and system names exactly as used in the source. Actionable practice items become tasks.

**Source type matters for extraction approach:**

- **Video transcripts**: conversational and rambling — extract signal from noise, infer structure from the presenter's sequence
- **SOP/procedure documents**: already structured (headings, numbered steps, warning boxes, tables) — respect the document's own organization rather than inferring it; deduplication against existing vault notes matters more here since SOPs are often updated versions of existing knowledge

**If jdocmunch is available** and the source is a long file: use `search_sections` / `get_section` to pull sections. Process section by section, then do a final structure note pass at the end to index related permanents.

## What training content to extract

Training transcripts yield four categories of permanent notes plus action items:

**Procedure sequences** — step-by-step workflows for performing a task in the system. High value: these are exactly what people need when performing the task. Title format: "How to [verb] [object] in [system]" or "[System]: steps to [action]". For SOP documents: preserve numbered step sequences exactly — do not paraphrase or reorder.

**System knowledge** — how an internal tool, service, or system works. What it does, what it doesn't do, its constraints. Title format: "[System] [does/stores/requires] [specific thing]".

**Policy and rules** — business rules, compliance requirements, approval thresholds, escalation criteria. Title format: "[Condition] requires [action]" or "[System] enforces [rule]".

**Gotchas and tips** — common mistakes, non-obvious behaviors, shortcuts. High signal-to-noise for operational value. Title format: "[System] [unexpected behavior]" or "Always [action] before [other action] in [system]". For SOP documents: warning boxes and note callouts map directly to gotcha notes.

**Action items** — actionable practice items ("implement this process", "set up this tool", "start doing Y on your team"). These become tasks via `pzk_create_task` with `source="transcript"` and `status="someday"` (training action items are aspirational — not immediately due unless the training specifies a deadline).

## Workflow

### Phase 1 — Extract (graph-blind)

**If subagents are available:** spawn the `zettelkasten-helper:extractor` agent. Pass the file path if the source is a file (the extractor has `Read` access); pass inline text if pasted directly. Include this instruction: "This is a company training transcript. Map each distinct idea to one of these types: `procedure` (step-by-step workflow), `system-knowledge` (how a tool/service works), `policy` (rule or requirement), `gotcha` (non-obvious behavior or tip), or `action-item` (something to implement or adopt). Treat company names, system names, and internal terminology as primary material — preserve exact wording."

**If subagents are not available:** simulate the extractor, reading the transcript and drafting candidates as if the vault were empty. Use the five types above.

1. **Read** the source — via jdocmunch sections for long transcripts.
2. **Get the full candidate list** — do not consider existing notes yet.
3. **Plan the literature note** — always create one. It anchors all derived notes to their source and preserves training context (system covered, date, presenter if known).

### Phase 2 — Prune and integrate

4. **Prune** — apply the atomicity gate from [atomization.md](../../references/atomization.md). For training content, the bar for keeping a note is: "Would someone performing this task need to look this up?" If yes, keep it. If it is obvious to anyone familiar with the domain, cut it.

   Special pruning rules for training:

   - **Keep** procedure sequences even if they seem basic — the exact steps matter operationally
   - **Keep** policy/rules even if brief — precision matters for compliance
   - **Cut** motivational framing and rationale unless it clarifies a non-obvious constraint
   - **Fold** minor gotchas into the relevant procedure note as a second sentence rather than creating a separate note

5. **Route action items** — candidates typed as `action-item` go to `pzk_create_task` with `source="transcript"` and `status="someday"`. If a deadline is stated in the training, set `due_date`. Follow the project resolution flow in [project-resolution.md](../../references/project-resolution.md).

6. **Graph comparison** — `pzk_search_notes` and `pzk_find_similar_notes` for each surviving knowledge candidate. If a procedure note already exists for a system, `pzk_update_note` to add new steps or correct outdated ones rather than creating a duplicate.

7. **Create notes and links** — literature note first, then permanents. `pzk_create_link` immediately after each note. Tasks are created in step 5.

8. **Structure note check** — `pzk_find_central_notes` for the system or service covered. Training content frequently warrants a structure note indexing all permanents about a given internal system. Create one if several permanents share a system and no index exists.

9. **Verify** — `pzk_get_linked_notes` to confirm links.

## Tool Order

Use tools in this order unless there is a clear reason not to:

1. Draft and prune the local candidate set first (no MCP calls).
2. `pzk_find_similar_notes` on each surviving candidate as the first-pass similarity sweep.
3. `pzk_search_notes` for targeted duplicate checking.
4. `pzk_get_note` when an existing note might need updating.
5. `pzk_create_note` / `pzk_update_note` / `pzk_create_task` to create items.
6. `pzk_create_link` to connect source and derived notes immediately.
7. `pzk_get_linked_notes` to verify the result.

## Note Content Formats

**Literature note (training) — pass as `content`:**

```text
Training title: [title or inferred description]
Source type: [Training video transcript / SOP document / Onboarding guide / Procedure doc]
System/service covered: [name]
Presenter/Author: [name or role, if identifiable]
Date: [date if available]
Source: [URL or file path]

Summary:
[1–3 sentences. State what the training covers and what operational knowledge it
provides. Name the system and at least one key procedure or policy covered.]
```

**Procedure note (permanent) — pass as `content`:**

```text
[Numbered steps or clear sequence. Use the exact system names and UI terminology
from the training — do not paraphrase. If the procedure has preconditions
(e.g., permissions required, prior steps), state them at the top.]

Source: [Training title]
```

**System knowledge / policy / gotcha note (permanent) — pass as `content`:**

```text
[1–3 sentences. Title already states the claim. Second sentence adds the specific
detail, constraint, or behavior from the training. Preserve system names and
internal terminology exactly.]

Source: [Training title]
```

## Linking

- `supports` — literature note → each derived permanent and task
- `reference` — structure note → all permanents about the same system
- `related` — between permanents covering adjacent parts of the same workflow
- `extends` — new training note adds to an existing permanent about the same system

Apply `pzk_create_link` immediately after each note. Pass the rationale as the `description` parameter.

Note: tasks created via `pzk_create_task` with a `project_id` are automatically linked to their project. You still need `supports` links from the literature note to each task.

## Output Report

1. **Candidates** — full list from Phase 1 with types (including action items).
2. **Pruning** — what was cut and why; anything folded back in.
3. **Action items** — tasks created, with project assignment and status.
4. **Literature note** — ID, system covered.
5. **Notes created/updated** — title, type, ID; by category (procedures / system knowledge / policies / gotchas).
6. **Links** — relationship type + one-line rationale each.
7. **Structure note actions** — what was indexed or why nothing was needed.

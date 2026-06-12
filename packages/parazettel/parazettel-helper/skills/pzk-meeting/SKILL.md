---
name: pzk-meeting
description: Converts a multi-speaker meeting transcript into atomic linked Zettelkasten notes and action-item tasks using the parazettel MCP. Use whenever a user provides a meeting recording transcript, team discussion notes, or collaborative session output. Triggers on "process this meeting", "meeting notes to Zettelkasten", "extract from meeting transcript", "capture this discussion", or when a transcript with multiple named speakers is provided.
compatibility: requires parazettel MCP (pzk_* tools); uses jdocmunch for long meeting transcripts
---

Turn a multi-speaker meeting transcript into atomic permanent notes, decisions, and action-item tasks via the parazettel MCP. Always create a literature note for the meeting itself. Action items become tasks with project routing. Maintain speaker attribution through extraction.

**The meeting literature note is invisible during normal retrieval.** Every decision, durable claim, and process insight worth finding later must become its own searchable permanent note — do not let it live only inside the meeting summary.

**If jdocmunch is available** and the transcript is long: use `search_sections` / `get_section` to pull sections rather than loading the full transcript. Process in segments, then reconcile at the end.

## Workflow

### Phase 1 — Identify and extract

1. **Identify speakers** — list all participants from the transcript. Note which (if any) is the vault owner.

2. **Extract** — spawn the `zettelkasten-helper:meeting-extractor` agent with the full transcript. The agent returns typed candidates with speaker attribution:
   - `decision` — explicit choices the group made
   - `action-item` — concrete next steps with assignees
   - `knowledge-claim` — durable insights worth preserving as permanent notes
   - `process-observation` — how the team currently works; implicit standards made explicit
   - `brainstorm-or-planning` — content/offer/module idea lists, design/planning ideation, "what should we build/make/try" exploration

   **If subagents are not available:** simulate the meeting-extractor by listing all candidates with type and speaker before any MCP interaction.

3. **Plan the literature note** — always create one for meetings. It captures: attendees, date, context, agenda (if stated), and a 1–3 sentence summary of what the meeting decided or concluded.

### Phase 1.5 — Project resolution (for action items)

Before creating any tasks, resolve the project context. Follow the flow in [project-resolution.md](../../references/project-resolution.md):

1. Run `pzk_list_projects` to get active projects.
2. If the meeting context clearly maps to a single project, use that project_id for all tasks.
3. If multiple projects are relevant (e.g., a standup covering several workstreams), group action items by project.
4. If no matching project exists, present the user with the action items and ask which project to assign them to (or whether to create one via `pzk_create_project`).

### Phase 2 — Prune and integrate

4. **Prune by type:**
   - **Decisions** — keep all explicit decisions. Title format: "Team decided [X] because [Y]" or, if no rationale given: "Decision: [X]". These almost always become permanent notes.
   - **Action items** — keep all. These become tasks via `pzk_create_task` (not fleeting notes). Each requires a `project_id` from Phase 1.5.
   - **Knowledge claims** — apply the atomicity gate from [atomization.md](../../references/atomization.md). Cut any claim generic enough to appear in any business article.
   - **Process observations** — keep if they reveal something non-obvious about how this team works. Cut if they are entirely standard.
   - **Brainstorms / planning** — capture content/offer/module idea lists and "what should we build" ideation as a `structure` note routed into the relevant cluster. Do not cut these as "generic" or fold them into the literature note; they are provenance even when off-topic, half-formed, or set aside in the same breath. Keep the reasoning for why an idea was rejected.

5. **Pre-create comparison** — for each surviving knowledge-claim and process-observation, run `pzk_search_notes` (now hybrid lexical+semantic) on its claim text. (Candidates have no ID yet, so `pzk_find_similar_notes` can't run on them pre-create.) A strong, on-claim match → link to existing, or `pzk_update_note` if the meeting adds something durable — but confirm it's the same atomic claim, not just the same topic (dense clusters score distinct atoms high); a loosely-related match → keep and link, not fold. Query with the **full claim**, not a terse keyword — phrasing strongly affects recall; with embeddings on, `pzk_find_similar_to_text` runs this semantic check on the draft text directly (calibrated cosine).

6. **Create notes, tasks, and links:**
   - Literature note first (`pzk_create_note` with `note_type="literature"`)
   - Then decisions (permanent notes)
   - Then knowledge-claims that survived (permanent notes)
   - Then process-observations (permanent or fold into literature note if borderline)
   - Then brainstorm/planning captures (`structure` notes routed into the relevant cluster)
   - Then action items as tasks:

     ```text
     pzk_create_task(
       title="[Assignee] will [action]",
       content="Context: [why this action was created]\n\nSource: [Meeting title or date]",
       project_id="[resolved in Phase 1.5]",
       status="inbox",
       source="meeting",
       due_date=[date if stated, else null],
       priority=[infer from urgency language: "critical"→4, "should"→2, default null]
     )
     ```

   - Apply `pzk_create_link` immediately after each note
   - Note: tasks created with `project_id` are automatically linked to their project (PART_OF/HAS_PART). You still need `supports` links from the literature note to each task.

7. **Post-create semantic audit** — run `pzk_find_similar_notes` on each note you just created (decisions and knowledge-claims), then two passes over the neighbours: (1) **links** — add 1–2 cross-vocabulary / cross-domain links the lexical pass missed (treat loosely-related hits as links, not folds); (2) **tension check** — if a new decision or claim *conflicts* with an existing note (a reversal of a prior decision, an opposing claim, a contradicting condition), reconcile rather than ignore: link `contradicts` (reciprocal `contradicted_by` is auto-added) or `refines`, or `pzk_update_note` to record the supersession — and surface it in the report. A superseded prior decision is especially worth flagging. Embeddings augment domain memory, not replace it — a low/empty result doesn't prove novelty; if you recall an obviously-relevant note that didn't surface, link it manually.

8. **Hub/structure check** — `pzk_find_central_notes` for the main topic areas. Update existing hub notes if relevant decisions or knowledge was added.

9. **Verify** — `pzk_get_linked_notes` to confirm links from literature note to permanents and tasks.

## Tool Order

Use tools in this order unless there is a clear reason not to:

1. Draft and prune the local candidate set first (no MCP calls).
2. `pzk_list_projects` for project resolution (action items).
3. **Pre-create sweep** — `pzk_search_notes` (hybrid lexical+semantic) on each surviving knowledge candidate's claim text. Candidates have no ID yet, so `pzk_find_similar_notes` can't run on them. Low top score = novel → create; strong on-claim match = fold/update; loosely-related = link candidate, not fold.
4. `pzk_get_note` when an existing note might need updating.
5. `pzk_get_all_tags` once before tagging — reuse existing tags per [tagging.md](../../references/tagging.md); mint a new tag only when the concept is genuinely absent.
6. `pzk_create_note` / `pzk_update_note` / `pzk_create_task` to create items (or `pzk_ingest_batch` for large batches — leave its dedup gate on; it creates-and-flags possible duplicates, and every line of its "Duplicate review" section must be judged: same claim → fold, same topic → keep and link).
7. `pzk_create_link` to connect source and derived notes immediately.
8. **Post-create audit** — `pzk_find_similar_notes` on each *newly created* note; add the cross-vocabulary links and tensions the lexical sweep missed.
9. `pzk_get_linked_notes` to verify the result.

## Note Content Formats

**Literature note (meeting) — pass as `content`:**

```text
Meeting date: [date]
Meeting type: [standup / planning / incident review / ad-hoc / etc.]
Attendees: [names/roles]
Context: [project or topic area]
Agenda: [stated agenda if present; omit field for standups and ad-hoc discussions]

Summary:
[1–3 sentences. State what was decided or concluded, not just what was discussed.
Include one concrete anchor — a key decision, a surprising finding, or a pivotal exchange.]
```

**Decision note (permanent) — pass as `content`:**

```text
[1–2 sentences. State the decision and the primary rationale.
If alternatives were considered, name them briefly in the second sentence.
Omit "we decided" — the title already carries that. Start with the substance.]

Source: [Meeting title or date]
```

**Knowledge-claim note (permanent) — pass as `content`:**

```text
[1–3 sentences. Title already states the claim.
Second sentence adds the specific detail, example, or evidence from the meeting.
Preserve the speaker's language where distinctive.]

Source: [Meeting title or date] — [Speaker if a single person articulated it]
```

## Linking

- `supports` — literature note → each derived permanent note and task
- `related` — between decisions that are connected
- `extends` — knowledge-claim that builds on an existing permanent note
- `contradicts` — a decision/claim that conflicts with an existing note (reciprocal `contradicted_by` is auto-added); use when the audit finds a real tension, e.g. a reversed decision
- `reference` — hub/structure → notes it indexes

Apply `pzk_create_link` immediately after each note. Pass the rationale as the `description` parameter.

## Output Report

1. **Speakers** — list of participants identified.
2. **Candidates** — full typed list from Phase 1.
3. **Project resolution** — which project(s) tasks were assigned to and how the mapping was determined.
4. **Pruning** — what was cut by type and why.
5. **Literature note** — ID, summary of what it captures.
6. **Notes created/updated** — title, type, ID; decisions / knowledge-claims separately.
7. **Tasks created** — title, ID, project, status, due date; grouped by project if multiple.
8. **Links** — relationship type + one-line rationale each.
9. **Hub/structure actions** — what was done or why nothing was needed.

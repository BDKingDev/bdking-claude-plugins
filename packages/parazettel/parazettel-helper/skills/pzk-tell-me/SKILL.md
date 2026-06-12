---
name: pzk-tell-me
description: Search and synthesize information from the Parazettel note system. Use when the user asks what the system contains about a topic, wants all notes related to a theme such as meal planning, or needs a retrieval-first summary grounded in existing notes, areas, projects, structure notes, and tasks rather than new note creation.
---

# PZK Tell Me

Retrieve and explain what is already in the Parazettel system.

Do not create, update, or relink notes unless the user explicitly asks for that after the retrieval pass.

## Default Goal

Turn a vague request like `tell me everything about meal planning` into:

- the best organizer notes to start from
- the core notes that carry the topic
- the adjacent notes that matter but are one step away
- any relevant `area`, `project`, or `task` layer
- a clean summary that separates direct matches from broader related material

## Search Order

Use tools in this order unless there is a clear reason not to:

1. `pzk_search_notes` with the user's topic as a natural query. Results are BM25-ranked, so read the `Relevance:` scores to gauge coverage.
2. Broaden with nearby terms, synonyms, component words, and likely subtopics **only when** the first pass is thin or low-relevance — it is no longer required to compensate for flat scoring.
3. Open the strongest hits with `pzk_get_note` (or several at once with `pzk_get_notes`).
4. If a strong hit is a `structure`, `hub`, `project`, or `area` note, expand from it with `pzk_get_linked_notes`.
5. If the topic sounds like an area or project lane, also use `pzk_list_areas`, `pzk_list_projects`, `pzk_get_area`, or `pzk_get_project`.
6. If the user wants current action or implementation status, use `pzk_get_tasks` or `pzk_get_project_tasks`.

## Retrieval Rules

- Start narrow, then widen — but let the `Relevance:` scores tell you whether widening is needed rather than always running every synonym pass.
- Prefer organizer notes first. A good `structure`, `hub`, `project`, or `area` note often gives the cleanest entry point.
- Expand through links, not just keywords.
- If the user asks for `all` of something, do at least one broadening pass after the first search.
- If a result is only loosely related, keep it in a separate `adjacent` bucket instead of mixing it into the core answer.
- Treat `permanent`, `structure`, `hub`, `project`, `area`, and `task` notes as different layers of the same system, not interchangeable objects.

## Topic Expansion

When the user asks about a broad topic, expand into the likely retrieval terms behind it.

Example: `meal planning`

- direct: `meal planning`, `meal plan`
- adjacent systems: `grocery`, `inventory`, `snack`, `produce`, `dinner`, `binder`, `cards`, `staple meal`, `sauce`, `protein`
- action layer: related `project` notes, `ready` tasks, or recurring system-building tasks

Do not blindly dump every hit. Group them into:

- `entry points`
- `core notes`
- `adjacent notes`
- `action layer`

## Output Shape

When answering the user:

- Name the best entry-point note or notes first.
- Group findings by role, not by search order.
- Distinguish direct topic notes from adjacent supporting notes.
- If the system has both knowledge notes and action notes, report that split clearly.
- Say when the answer is complete enough versus when it is a best-effort retrieval sweep.
- If the search surface looks thin, say which searches were tried and what was not found.

## Example Pattern

If the user asks `tell me all meal planning info`, aim to return something like:

- best entry points: meal planning map, baseline project, staple meal structure
- core systems: grocery list system, pantry inventory system, snack/produce board
- concrete processes: yogurt process, meal card system, staple meal cards
- supporting principles: convenience, bounded variety, ready-to-use proteins, sauce defaults
- action layer: any active meal-planning project or tasks

## Guardrails

- Retrieval first, mutation second.
- Do not invent coverage the graph does not actually contain.
- Do not collapse adjacent notes into one summary claim if the user asked for breadth.
- If the system clearly has a missing organizer note, mention that as an observation, but do not create it unless asked.

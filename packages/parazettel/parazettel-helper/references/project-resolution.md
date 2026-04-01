# Project Resolution

When a skill needs to create tasks via `pzk_create_task`, every task requires a `project_id`. Follow this flow to resolve the correct project:

## Resolution flow

1. **List active projects** — run `pzk_list_projects` to get the current project set.
2. **Match by context** — if the source (meeting topic, transcript subject, training module) clearly maps to a single project, use that project's ID for all tasks.
3. **Group by project** — if multiple projects are relevant (e.g., a standup covers several workstreams), group action items by project before creating tasks.
4. **Ask when ambiguous** — if no project matches or the mapping is unclear, present the user with the action items and ask which project to assign them to.
5. **Offer to create** — if no existing project fits, offer to create a new one via `pzk_create_project`. Ask for an `area_id` (use `pzk_list_areas` to show options).

## Rules

- **Never silently create a project.** Project creation is a structural decision the user should make.
- **Never skip the project.** `pzk_create_task` requires `project_id` — tasks without a project are rejected.
- **area_id auto-fills.** When a task is created with a `project_id`, the task's `area_id` is automatically derived from the project. You do not need to set it separately.
- **Task-to-project links are automatic.** `pzk_create_task` creates PART_OF/HAS_PART links between the task and its project. You do not need to call `pzk_create_link` for this relationship.

## Task field mapping from source material

| Source field | Task parameter | Example |
| --- | --- | --- |
| Who is assigned | Include in title | "Bailey will test is_California PR" |
| When it's due | `due_date` (YYYY-MM-DD) | "2026-04-01" |
| How urgent | `priority` (1-4) | Infer from language: "critical"→4, "should"→2 |
| Where to do it | `context` (auto-applies @tag) | "computer", "phone", "home" |
| How hard | `energy_level` (auto-applies tag) | "high", "medium", "low" |
| Where it came from | `source` | "meeting", "voice", "transcript", "chat" |
| When to check back | `remind_at` (YYYY-MM-DD) | For waiting/delegated items |

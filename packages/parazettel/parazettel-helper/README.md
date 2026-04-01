# parazettel-helper

Converts transcripts, meeting notes, and training videos into atomic Zettelkasten notes with PARA/GTD task management. Captures ideas and action items from coding conversations.

## Setup

Add the following to your project's `.claude/settings.local.json` (personal, gitignored) or `.claude/settings.json` (shared, committed) under the `env` key:

```json
{
  "env": {
    "PARAZETTEL_VENV_PYTHON": "/path/to/parazettel/.venv/bin/python",
    "PARAZETTEL_NOTES_DIR": "/path/to/parazettel/data/notes",
    "PARAZETTEL_DATABASE_PATH": "/path/to/parazettel/data/db/parazettel.db",
    "PARAZETTEL_LOG_LEVEL": "INFO"
  }
}
```

Claude Code reads this file before starting MCP servers, so no shell profile changes are needed. Use `settings.local.json` for personal paths that shouldn't be committed; use `settings.json` if the team shares a common parazettel location.

The parazettel MCP server requires a local Python venv. If you haven't set one up:

```bash
cd /path/to/parazettle
uv venv --python 3.13
uv sync --extra dev
```

## Skills

| Skill | Trigger | Use |
| --- | --- | --- |
| `pzk-personal-note` | "atomize this", "add this to my Zettelkasten", "process this note" | Personal transcripts, voice memos, Notion exports — creates notes + tasks |
| `pzk-meeting` | "process this meeting", "meeting notes to Zettelkasten" | Multi-speaker meetings — decisions as notes, action items as tasks with project routing |
| `pzk-training` | "process this training/SOP", "training video to Zettelkasten" | Training transcripts and SOPs — procedures as notes, practice items as tasks |
| `pzk-chat-session` | `/parazettel-helper:pzk-chat-session` | Capture ideas + action items from the current coding session |

## Hooks

### PreCompact (Extraction)

Fires before context compression on long conversations. Uses Claude Haiku to extract Zettelkasten-worthy insights from the conversation transcript and writes them as structured markdown to `/tmp/chat-insights-YYYYMMDD-HHMMSS.md`.

**What gets captured:**

- Atomic insights: architectural decisions, debugging findings, design trade-offs, gotchas
- Frameworks: mental models, system patterns (PARA, GTD, architectural patterns)
- Action items: concrete follow-up tasks

**Output format:**

```markdown
## [Claim-style title]
Type: note | structure | task
Tags: #chat-capture #domain-tag

[1-4 sentences with context]
```

**Debug mode:**

```bash
VERBOSE=1  # Writes extraction output to /tmp/chat-insights-*.md (always enabled)
```

### PostCompact (Integration)

Fires after context compression completes. Reads the markdown file from PreCompact and integrates insights into the vault:

**Phase 1 — Ingest:**

- Creates permanent notes with `status='inbox'` for human review
- Creates structure notes for frameworks/models with `note_type='structure'`
- Creates tasks with `status='inbox'` for action items

**Phase 2 — Prune & Link:**

1. **Find**: Searches for notes with `status='inbox'` and `tags='chat-capture'`
2. **Prune**: Deletes duplicates, strengthens survivors
3. **Link**: Creates semantic links using `pzk_find_similar_notes`

All notes remain with `status='inbox'` for human triage and promotion.

**Debug mode:**

```bash
VERBOSE=1  # Writes both phase outputs to /tmp/post-compact-{ingest,linking}-{PID}.log
```

## Available Tools (26 total)

### Knowledge management

`pzk_create_note`, `pzk_get_note`, `pzk_update_note`, `pzk_delete_note`, `pzk_create_link`, `pzk_remove_link`, `pzk_search_notes`, `pzk_get_linked_notes`, `pzk_get_all_tags`, `pzk_find_similar_notes`, `pzk_find_central_notes`, `pzk_find_orphaned_notes`, `pzk_list_notes_by_date`, `pzk_rebuild_index`

### Task management

`pzk_create_task`, `pzk_update_task`, `pzk_get_tasks`, `pzk_get_todays_tasks`, `pzk_get_reminders`

### Project and area management

`pzk_create_project`, `pzk_get_project`, `pzk_get_project_tasks`, `pzk_list_projects`, `pzk_create_area`, `pzk_get_area`, `pzk_list_areas`

## Note Types

The vault uses different note types for different purposes:

- **`fleeting`**: Temporary captures that need processing (inbox items, raw thoughts)
- **`permanent`**: Atomic, well-formed knowledge notes (single claims, decisions, patterns, gotchas)
- **`literature`**: Notes from external sources (books, articles, papers)
- **`structure`**: Major organizing hubs that house 10+ permanent notes

### Structure Notes

Structure notes are **broad organizing frameworks** that connect multiple related permanent notes. They can be:

1. **Concrete reference maps**: System flows, templates, navigation hubs
   - Example: "PE Jira Board" (templates, workflows, conventions)
   - Example: "eaze.com Checkout Flow" (page objects, test addresses, QA signals)

2. **Major organizing frameworks**: Complex systems that house many sub-concepts
   - Example: "Claude Hooks" (PreCompact, PostCompact, debugging, configuration)

**What is NOT a structure note:**

- ❌ Narrow frameworks with only 2-5 related concepts → use `permanent` note instead
- ❌ Single patterns or workflows → use `permanent` note with semantic links
- ❌ Abstract concepts without sub-structure → use `permanent` note

Use semantic link types (`supports`, `extends`, `part-of`, `reference`) to show hierarchical relationships between permanent notes and their organizing structures.

## CLAUDE.md Integration

**Option A — Dedicated parazettel repo** (repo whose only job is knowledge + task management):

```markdown
## Parazettle Assistant

Fetch and follow the system prompt from the parazettel project:
Read docs/prompts/system/system-prompt-with-protocol.md
```

**Option B — General repo or user-level `~/.claude/CLAUDE.md`**:

```markdown
### parazettel (knowledge + task management)

The vault is a permanent store of user-vetted knowledge and action items. Consult it at the start of any project or feature — search before writing. Capture new knowledge and tasks as they are produced.

- At the start of any project or feature: use `pzk_search_notes` and `pzk_find_central_notes` to surface relevant existing knowledge.
- Before creating: use `pzk_find_similar_notes` to avoid duplication. Use `pzk_update_note` if a close note exists.
- To save knowledge: use `pzk_create_note` (types: `fleeting`, `permanent`, `literature`, `structure`). Use `structure` only for major organizing hubs that house 10+ notes.
- To save action items: use `pzk_create_task` with `project_id`, `status`, `source`, and optionally `due_date`, `priority`, `energy_level`, `context`.
- To connect: use `pzk_create_link` immediately after each note — don't batch.
- To check tasks: use `pzk_get_todays_tasks` for the daily view, `pzk_get_reminders` for scheduled check-ins.
- When given a transcript, voice memo, or Notion export → trigger pzk-personal-note.
- When given a meeting transcript → trigger pzk-meeting.
- When given a training video or SOP document → trigger pzk-training.
- At session end: offer `/parazettel-helper:pzk-chat-session` to capture engineering insights and action items.
```

## Deeper Zettelkasten work

The plugin skills handle structured ingestion from known source types. For open-ended Zettelkasten work, the parazettel project includes chat prompts in `docs/prompts/chat/`:

- `chat-prompt-knowledge-exploration.md` — find how material connects to existing vault
- `chat-prompt-knowledge-synthesis.md` — bridge unconnected areas, create higher-order insights
- `chat-prompt-knowledge-creation.md` — process new information into atomic notes
- `chat-prompt-knowledge-creation-batch.md` — batch processing of larger sources

## Testing locally

```bash
claude --plugin-dir zettelkasten-helper
```

Verify the MCP connects: run `/mcp` and confirm the parazettel server shows all `pzk_*` tools.

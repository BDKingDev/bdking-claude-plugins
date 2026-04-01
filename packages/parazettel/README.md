# Parazettel — Zettelkasten + GTD/PARA for Claude Code

A complete knowledge management and task system that combines Zettelkasten (atomic notes + semantic links) with GTD and PARA workflows. Runs as an MCP server with Claude Code plugin for automatic insight extraction from conversations.

## What's Included

This package contains:

1. **Parazettel MCP Server** — Core Zettelkasten knowledge base with 26 tools for notes, tasks, projects, and areas
2. **Parazettel Helper Plugin** — Claude Code plugin with:
   - 4 skills for processing transcripts, meetings, and training materials
   - 2 agents for extracting atomic insights and meeting notes
   - 2 hooks (PreCompact + PostCompact) for automatic chat insight capture
   - References and documentation

## Quick Start

### 1. Install the MCP Server

```bash
# Clone or copy this package
cd parazettel-marketplace-package

# Create virtual environment
uv venv --python 3.13
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows

# Install with dev dependencies
uv sync --extra dev

# Test the installation
.venv/bin/python -m parazettel_mcp.main
```

### 2. Configure Environment Variables

Add to your shell profile (`.zshrc`, `.bashrc`, etc.) or Claude Code settings:

```bash
export PARAZETTEL_VENV_PYTHON="/path/to/parazettel-marketplace-package/.venv/bin/python"
export PARAZETTEL_NOTES_DIR="/path/to/your-notes-directory"
export PARAZETTEL_DATABASE_PATH="/path/to/your-notes-directory/parazettel.db"
export PARAZETTEL_LOG_LEVEL="INFO"
```

**Or** add to `.claude/settings.local.json` (personal, gitignored):

```json
{
  "env": {
    "PARAZETTEL_VENV_PYTHON": "/path/to/parazettel-marketplace-package/.venv/bin/python",
    "PARAZETTEL_NOTES_DIR": "/path/to/your-notes-directory",
    "PARAZETTEL_DATABASE_PATH": "/path/to/your-notes-directory/parazettel.db",
    "PARAZETTEL_LOG_LEVEL": "INFO"
  }
}
```

### 3. Create Notes Directory

```bash
mkdir -p /path/to/your-notes-directory
```

### 4. Add MCP Server to Claude Code

Add to `~/.claude.json`:

```json
{
  "mcpServers": {
    "parazettel": {
      "command": "${PARAZETTEL_VENV_PYTHON}",
      "args": [
        "-m",
        "parazettel_mcp.main"
      ],
      "env": {
        "PARAZETTEL_NOTES_DIR": "${PARAZETTEL_NOTES_DIR}",
        "PARAZETTEL_DATABASE_PATH": "${PARAZETTEL_DATABASE_PATH}",
        "PARAZETTEL_LOG_LEVEL": "${PARAZETTEL_LOG_LEVEL}"
      }
    }
  }
}
```

### 5. Install the Plugin

Copy the plugin to your Claude Code plugins directory:

```bash
# Copy to global plugins
cp -r parazettel-helper ~/.claude/plugins/

# Or for project-specific installation
cp -r parazettel-helper /path/to/your-project/.claude/plugins/
```

Enable the plugin in `~/.claude/settings.json`:

```json
{
  "enabledPlugins": [
    "parazettel-helper"
  ]
}
```

### 6. Verify Installation

Restart Claude Code, then test:

```bash
claude
/mcp
```

You should see `parazettel` with 26 tools listed.

## Features

### Zettelkasten Knowledge Management

- **Atomic notes** with unique timestamp-based IDs
- **Typed semantic links** (supports, extends, contradicts, part-of, reference, related)
- **Note types**: fleeting, permanent, literature, structure, hub
- **Full-text search** across titles, content, and tags
- **Graph operations**: find similar notes, central notes, orphaned notes
- **Dual storage**: Markdown files (source of truth) + SQLite index (fast queries)

### GTD + PARA Workflows

- **Tasks** with status lifecycle, priorities, energy levels, and GTD contexts
- **Projects** (time-bound outcomes) linked to areas
- **Areas** (ongoing responsibilities with no end date)
- **Today view** and reminder surfacing
- **Recurring tasks** that auto-spawn the next instance on completion
- **Status flow**: inbox → ready → active → done/cancelled

### Automatic Insight Capture (Plugin)

#### Skills

- **`pzk-personal-note`** — Process personal transcripts, voice memos, Notion exports
- **`pzk-meeting`** — Extract decisions and action items from multi-speaker meetings
- **`pzk-training`** — Convert training transcripts and SOPs into procedures and practice items
- **`pzk-chat-session`** — Capture ideas and action items from coding sessions

#### Hooks

- **PreCompact** — Extracts insights before context compression using Claude Haiku
- **PostCompact** — Ingests markdown insights, prunes duplicates, creates semantic links

Both hooks run automatically. Insights are saved to `~/.claude/temp/chat-insights-*.md` with:
- Atomic notes (architectural decisions, debugging findings, gotchas)
- Structure notes (major organizing frameworks that house 10+ notes)
- Projects (multi-hour/multi-day efforts)
- Tasks (concrete action items)

All created notes have `status='inbox'` for human review before promotion.

## Available MCP Tools (26 total)

### Knowledge Management

`pzk_create_note`, `pzk_get_note`, `pzk_update_note`, `pzk_delete_note`, `pzk_create_link`, `pzk_remove_link`, `pzk_search_notes`, `pzk_get_linked_notes`, `pzk_get_all_tags`, `pzk_find_similar_notes`, `pzk_find_central_notes`, `pzk_find_orphaned_notes`, `pzk_list_notes_by_date`, `pzk_rebuild_index`

### Task Management

`pzk_create_task`, `pzk_update_task`, `pzk_get_tasks`, `pzk_get_todays_tasks`, `pzk_get_reminders`

### Project and Area Management

`pzk_create_project`, `pzk_get_project`, `pzk_get_project_tasks`, `pzk_list_projects`, `pzk_create_area`, `pzk_get_area`, `pzk_list_areas`

## Usage Examples

### Creating Notes

```python
# Via MCP tools in Claude Code
pzk_create_note(
    title="BSD sed on macOS doesn't support GNU inline labels",
    content="macOS ships with BSD sed which rejects the GNU pattern `:a;N;$!ba;s/\n/\\n/g`...",
    note_type="permanent",
    tags="portability,macos,sed",
    source="chat"
)
```

### Creating Tasks

```python
pzk_create_task(
    title="Write tests for auth module",
    project_id="20260327T123259648500000",  # Optional project ID
    status="inbox",
    priority="high",
    energy_level="high",
    context="coding"
)
```

### Searching and Linking

```python
# Find similar notes
pzk_find_similar_notes(
    note_id="20260331T154631374857000",
    limit=5
)

# Create semantic link
pzk_create_link(
    source_note_id="20260331T154631374857000",
    target_note_id="20260331T200320831242000",
    link_type="related"
)
```

## CLAUDE.md Integration

Add to your project's `CLAUDE.md` or global `~/.claude/CLAUDE.md`:

```markdown
### Parazettel (knowledge + task management)

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

## Note Types

| Type | Description | Use Case |
| --- | --- | --- |
| `fleeting` | Quick, unprocessed captures | Temporary inbox items, raw thoughts |
| `permanent` | Atomic, well-formed knowledge notes | Single claims, decisions, patterns, gotchas |
| `literature` | Notes from external sources | Books, articles, papers |
| `structure` | Major organizing hubs | Frameworks that house 10+ permanent notes |
| `hub` | Entry points to major topics | Top-level navigation |
| `task` | Atomic actionable item | GTD next action |
| `project` | Time-bound outcome | Multi-hour/multi-day effort |
| `area` | Ongoing responsibility | No end date, continuous attention |

### Structure Notes

Structure notes are **broad organizing frameworks** that connect multiple related permanent notes. Examples:
- "Claude Hooks" (PreCompact, PostCompact, debugging, configuration)
- "PE Jira Board" (templates, workflows, conventions)
- "eaze.com Checkout Flow" (page objects, test addresses, QA signals)

**What is NOT a structure note:**
- ❌ Narrow frameworks with only 2-5 related concepts → use `permanent` note instead
- ❌ Single patterns or workflows → use `permanent` note with semantic links
- ❌ Abstract concepts without sub-structure → use `permanent` note

## Troubleshooting

### MCP Server Not Found

```bash
# Verify Python path
which python3
echo $PARAZETTEL_VENV_PYTHON

# Test MCP server directly
$PARAZETTEL_VENV_PYTHON -m parazettel_mcp.main
```

### Hooks Not Running

```bash
# Check hook configuration
cat ~/.claude/plugins/parazettel-helper/hooks/hooks.json

# Test PreCompact hook manually
TEST_MODE=1 VERBOSE=1 python3 ~/.claude/plugins/parazettel-helper/hooks/scripts/extract-chat-ideas.py < test-input.json

# Enable debug logging
export VERBOSE=1
```

### Notes Not Created

```bash
# Check temp directory
ls -la ~/.claude/temp/

# Verify insights file
cat ~/.claude/temp/chat-insights-*.md

# Check PostCompact logs
VERBOSE=1  # Writes logs to /tmp/post-compact-*.log
```

## Development

### Running Tests

```bash
# Run all tests
.venv/bin/python -m pytest tests/

# Run specific test file
.venv/bin/python -m pytest tests/test_zettel_service.py

# Run with coverage
.venv/bin/python -m pytest --cov=src/parazettel_mcp tests/
```

### Debugging

```bash
# Enable debug logging
export PARAZETTEL_LOG_LEVEL=DEBUG

# Verbose hook output
export VERBOSE=1

# Test mode (processes only last chunk)
export TEST_MODE=1
```

## License

MIT License - See source repository for details

## Credits

Fork of [zettelkasten-mcp](https://github.com/entanglr/zettelkasten-mcp) by Entanglr

Extended with:
- GTD + PARA workflow layer
- Status field for note lifecycle
- Task management with priorities, contexts, energy levels
- Project and area routing
- Claude Code plugin with skills, agents, and hooks
- Automatic insight extraction from conversations

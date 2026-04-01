# Installation Guide

Complete step-by-step instructions for installing Parazettel MCP server and Claude Code plugin.

## Prerequisites

- Python 3.13+ installed
- [uv](https://github.com/astral-sh/uv) package manager (or pip/virtualenv)
- Claude Code installed ([installation instructions](https://code.claude.com/docs/en/setup))
- Git for Windows (Windows only)

## Step 1: Install the MCP Server

### 1.1 Navigate to Package Directory

```bash
cd /path/to/parazettel-marketplace-package
```

### 1.2 Create Virtual Environment

**Using uv (recommended):**

```bash
uv venv --python 3.13
```

**Using venv:**

```bash
python3.13 -m venv .venv
```

### 1.3 Activate Virtual Environment

**macOS/Linux:**

```bash
source .venv/bin/activate
```

**Windows CMD:**

```cmd
.venv\Scripts\activate.bat
```

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 1.4 Install Dependencies

**Using uv:**

```bash
uv sync --extra dev
```

**Using pip:**

```bash
pip install -e ".[dev]"
```

### 1.5 Verify Installation

```bash
# Should start the MCP server without errors
.venv/bin/python -m parazettel_mcp.main

# Press Ctrl+C to exit
```

## Step 2: Configure Environment Variables

You need to tell Claude Code where to find the MCP server and where to store your notes.

### Option A: Shell Profile (Recommended)

Add to your shell profile (`~/.zshrc`, `~/.bashrc`, or `~/.bash_profile`):

```bash
# Parazettel MCP Configuration
export PARAZETTEL_VENV_PYTHON="/absolute/path/to/parazettel-marketplace-package/.venv/bin/python"
export PARAZETTEL_NOTES_DIR="/absolute/path/to/your-notes"
export PARAZETTEL_DATABASE_PATH="/absolute/path/to/your-notes/parazettel.db"
export PARAZETTEL_LOG_LEVEL="INFO"
```

**Replace paths with actual absolute paths!** For example:

```bash
export PARAZETTEL_VENV_PYTHON="/Users/bailey/parazettel-marketplace-package/.venv/bin/python"
export PARAZETTEL_NOTES_DIR="/Users/bailey/Documents/zettelkasten"
export PARAZETTEL_DATABASE_PATH="/Users/bailey/Documents/zettelkasten/parazettel.db"
```

**Windows PowerShell ($PROFILE):**

```powershell
$env:PARAZETTEL_VENV_PYTHON="C:\Users\YourName\parazettel-marketplace-package\.venv\Scripts\python.exe"
$env:PARAZETTEL_NOTES_DIR="C:\Users\YourName\Documents\zettelkasten"
$env:PARAZETTEL_DATABASE_PATH="C:\Users\YourName\Documents\zettelkasten\parazettel.db"
$env:PARAZETTEL_LOG_LEVEL="INFO"
```

Reload your shell profile:

```bash
source ~/.zshrc  # or ~/.bashrc
```

### Option B: Claude Code Settings (Alternative)

Create or edit `~/.claude/settings.local.json`:

```json
{
  "env": {
    "PARAZETTEL_VENV_PYTHON": "/absolute/path/to/parazettel-marketplace-package/.venv/bin/python",
    "PARAZETTEL_NOTES_DIR": "/absolute/path/to/your-notes",
    "PARAZETTEL_DATABASE_PATH": "/absolute/path/to/your-notes/parazettel.db",
    "PARAZETTEL_LOG_LEVEL": "INFO"
  }
}
```

## Step 3: Create Notes Directory

```bash
mkdir -p /absolute/path/to/your-notes
```

This directory will store:
- Markdown note files (e.g., `20260331T154631374857000.md`)
- SQLite database (e.g., `parazettel.db`)

## Step 4: Register MCP Server with Claude Code

### 4.1 Edit Claude Code MCP Configuration

Open or create `~/.claude.json`:

```bash
# macOS/Linux
code ~/.claude.json

# Or use any text editor
nano ~/.claude.json
```

### 4.2 Add Parazettel MCP Server

Add this to the `mcpServers` section:

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

**Full example with multiple servers:**

```json
{
  "mcpServers": {
    "parazettel": {
      "command": "${PARAZETTEL_VENV_PYTHON}",
      "args": ["-m", "parazettel_mcp.main"],
      "env": {
        "PARAZETTEL_NOTES_DIR": "${PARAZETTEL_NOTES_DIR}",
        "PARAZETTEL_DATABASE_PATH": "${PARAZETTEL_DATABASE_PATH}",
        "PARAZETTEL_LOG_LEVEL": "${PARAZETTEL_LOG_LEVEL}"
      }
    }
  }
}
```

## Step 5: Install the Claude Code Plugin

### 5.1 Copy Plugin to Claude Directory

**For global installation (all projects):**

```bash
# macOS/Linux
cp -r parazettel-helper ~/.claude/plugins/

# Windows PowerShell
Copy-Item -Recurse parazettel-helper "$env:USERPROFILE\.claude\plugins\"
```

**For project-specific installation:**

```bash
# macOS/Linux
cp -r parazettel-helper /path/to/your-project/.claude/plugins/

# Windows PowerShell
Copy-Item -Recurse parazettel-helper "C:\path\to\your-project\.claude\plugins\"
```

### 5.2 Enable the Plugin

Edit `~/.claude/settings.json`:

```json
{
  "enabledPlugins": [
    "parazettel-helper"
  ]
}
```

## Step 6: Verify Installation

### 6.1 Restart Claude Code

If Claude Code is running, restart it:

```bash
# Exit any running Claude session
exit

# Start fresh
claude
```

### 6.2 Check MCP Tools

In Claude Code, run:

```bash
/mcp
```

You should see:

```
Available MCP servers:
  parazettel (26 tools)
    - pzk_create_note
    - pzk_get_note
    - pzk_update_note
    - pzk_delete_note
    ...
```

### 6.3 Test Creating a Note

```bash
claude -p "Create a test note in my Zettelkasten with title 'Test Note' and content 'This is a test'"
```

Claude should respond with confirmation that a note was created.

### 6.4 Verify Note File

```bash
ls -la $PARAZETTEL_NOTES_DIR
```

You should see a `.md` file with a timestamp-based ID.

## Step 7: Configure CLAUDE.md (Optional but Recommended)

Create `~/.claude/CLAUDE.md` or add to your project's `CLAUDE.md`:

```markdown
### Parazettel (knowledge + task management)

The vault is a permanent store of user-vetted knowledge and action items. Consult it at the start of any project or feature — search before writing.

- At the start of any project: use `pzk_search_notes` and `pzk_find_central_notes`
- Before creating: use `pzk_find_similar_notes` to avoid duplication
- To save knowledge: use `pzk_create_note` (types: fleeting, permanent, literature, structure)
- To save action items: use `pzk_create_task` with project_id, status, source
- To connect: use `pzk_create_link` immediately after each note
- When given a transcript → trigger pzk-personal-note
- When given a meeting transcript → trigger pzk-meeting
- At session end: offer `/parazettel-helper:pzk-chat-session`
```

## Troubleshooting

### "MCP server 'parazettel' not found"

**Check environment variables:**

```bash
echo $PARAZETTEL_VENV_PYTHON
echo $PARAZETTEL_NOTES_DIR
```

If empty, your environment variables aren't set. Go back to Step 2.

**Verify Python path:**

```bash
$PARAZETTEL_VENV_PYTHON --version
```

Should output `Python 3.13.x` or similar.

### "Module not found: parazettel_mcp"

The MCP server wasn't installed correctly. Go back to Step 1.4:

```bash
cd /path/to/parazettel-marketplace-package
source .venv/bin/activate
uv sync --extra dev
```

### "Permission denied" on hooks

```bash
# Make hook scripts executable
chmod +x ~/.claude/plugins/parazettel-helper/hooks/scripts/*.py
```

### Plugin not showing up

```bash
# Check plugin is in correct location
ls -la ~/.claude/plugins/parazettel-helper/

# Verify plugin.json exists
cat ~/.claude/plugins/parazettel-helper/.claude-plugin/plugin.json

# Check settings.json
cat ~/.claude/settings.json
```

### Hooks not firing

**Enable verbose logging:**

```bash
export VERBOSE=1
claude
```

**Check temp directory:**

```bash
ls -la ~/.claude/temp/
```

**Check PreCompact hook output:**

After a long conversation that triggers compaction, check:

```bash
ls -la ~/.claude/temp/chat-insights-*.md
```

## Next Steps

- Read [parazettel-helper/README.md](parazettel-helper/README.md) for plugin usage
- See [docs/](docs/) for detailed documentation
- Try the skills: `/parazettel-helper:pzk-chat-session` to capture insights from your current conversation

## Getting Help

- Check [README.md](README.md) for feature overview
- See [docs/mcp-testing-guide.md](docs/mcp-testing-guide.md) for testing MCP tools
- Review [docs/para-gtd-guide.md](docs/para-gtd-guide.md) for task management workflow

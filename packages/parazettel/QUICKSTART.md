# Quick Start Guide

Get Parazettel running in 5 minutes.

## Prerequisites

- Python 3.13+
- [uv](https://github.com/astral-sh/uv) (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
- [Claude Code](https://code.claude.com/) installed

## Installation

```bash
# 1. Navigate to package
cd parazettel-marketplace-package

# 2. Install MCP server
uv venv --python 3.13
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync --extra dev

# 3. Create notes directory
mkdir -p ~/Documents/zettelkasten

# 4. Set environment variables (add to ~/.zshrc or ~/.bashrc)
export PARAZETTEL_VENV_PYTHON="$(pwd)/.venv/bin/python"
export PARAZETTEL_NOTES_DIR="$HOME/Documents/zettelkasten"
export PARAZETTEL_DATABASE_PATH="$HOME/Documents/zettelkasten/parazettel.db"
export PARAZETTEL_LOG_LEVEL="INFO"

# Reload shell
source ~/.zshrc  # or source ~/.bashrc

# 5. Add MCP server to Claude Code
# Edit ~/.claude.json and add:
```

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

```bash
# 6. Install plugin
cp -r parazettel-helper ~/.claude/plugins/

# 7. Enable plugin in ~/.claude/settings.json
```

```json
{
  "enabledPlugins": ["parazettel-helper"]
}
```

## Verify

```bash
# Restart Claude Code
claude

# Check MCP tools are loaded
/mcp

# Should show: parazettel (26 tools)
```

## First Steps

### Create a Note

```bash
claude -p "Create a note about Python virtual environments with tags python,devtools"
```

### Search Notes

```bash
claude -p "Search my notes for 'python'"
```

### Create a Task

```bash
claude -p "Create a task to write tests for the auth module with high priority"
```

### Capture Chat Insights

After any coding session:

```bash
/parazettel-helper:pzk-chat-session
```

This captures architectural decisions, debugging findings, and action items from your conversation.

## Automatic Capture

The plugin automatically extracts insights when conversations get long:

1. **PreCompact hook** — Before context compression, extracts insights to `~/.claude/temp/chat-insights-*.md`
2. **PostCompact hook** — After compression, creates notes with `status='inbox'` for review

All captured notes need human review before promotion to your permanent knowledge base.

## What's Next?

- **[README.md](README.md)** — Full feature overview
- **[INSTALL.md](INSTALL.md)** — Detailed installation guide
- **[parazettel-helper/README.md](parazettel-helper/README.md)** — Plugin skills, agents, and hooks
- **[docs/para-gtd-guide.md](docs/para-gtd-guide.md)** — Task management workflow

## Common Commands

```bash
# Today's tasks
claude -p "Show me today's tasks"

# Search for similar notes
claude -p "Find notes similar to <note-id>"

# Create semantic link
claude -p "Link these two notes with 'supports' relationship"

# Get project tasks
claude -p "Show all tasks for project <project-id>"

# Process a transcript
# (copy transcript to clipboard, then)
/parazettel-helper:pzk-personal-note
```

## Troubleshooting

**MCP server not found:**

```bash
# Check environment variables
echo $PARAZETTEL_VENV_PYTHON
echo $PARAZETTEL_NOTES_DIR

# Test server directly
$PARAZETTEL_VENV_PYTHON -m parazettel_mcp.main
```

**Plugin not working:**

```bash
# Verify plugin location
ls ~/.claude/plugins/parazettel-helper/

# Check enabled in settings
cat ~/.claude/settings.json
```

**Hooks not running:**

```bash
# Enable verbose logging
export VERBOSE=1
claude

# Check temp directory
ls ~/.claude/temp/
```

For more help, see [INSTALL.md](INSTALL.md) troubleshooting section.

# Version History

## v0.4.0 (Current Release)

**Release Date:** 2026-03-31

### Features

**MCP Server:**
- 26 MCP tools for note, task, project, and area management
- Dual storage: Markdown files (source of truth) + SQLite index (fast queries)
- WAL-mode SQLite with in-memory LRU cache for performance
- Semantic link types: supports, extends, contradicts, part-of, reference, related
- Full-text search with FTS5
- Graph operations: similar notes, central notes, orphaned notes
- Note types: fleeting, permanent, literature, structure, hub
- Status field for note lifecycle management
- Task management with GTD workflow (inbox → ready → active → done)
- PARA hierarchy (Projects + Areas)
- Recurring tasks that auto-spawn on completion

**Plugin:**
- 4 skills: pzk-personal-note, pzk-meeting, pzk-training, pzk-chat-session
- 2 agents: extractor (graph-blind), meeting-extractor (attribution-aware)
- 2 hooks: PreCompact (extraction), PostCompact (ingestion + linking)
- Automatic insight capture with parallel chunk processing
- Session-independent temp storage (`~/.claude/temp/`)
- Structure note threshold (10+ notes required)
- Project extraction for multi-hour/multi-day efforts

### Improvements

- Renamed from "parazettle" to "parazettel" (fixed typo)
- Environment variables: `ZETTELKASTEN_*` → `PARAZETTEL_*`
- Hooks use `~/.claude/temp/` instead of session-specific directories
- Parallel chunk processing (4× speedup for long transcripts)
- Refined structure note extraction criteria
- Comprehensive marketplace package with installation guides

### Bug Fixes

- Fixed hook environment variable access (stdin JSON vs env vars)
- Fixed session ID availability in continuation sessions
- Fixed Python 3.13 compatibility in hooks
- Fixed MCP config variable resolution in subprocesses

### Documentation

- Complete README with feature overview
- QUICKSTART.md for 5-minute setup
- INSTALL.md with detailed step-by-step instructions
- PACKAGE_CONTENTS.md showing directory structure
- marketplace.json for marketplace integration
- Updated plugin README with hook documentation

### Technical Details

- Python 3.13+ required
- SQLAlchemy 2.0+
- Pydantic 2.0+
- anthropic-mcp 1.2+
- Claude Code 1.0+

## v0.3.0

### Features

- Added status field to notes
- Task management with priorities and energy levels
- Project and area routing
- GTD context support
- Reminder system

## v0.2.0

### Features

- Semantic link types with inverse relationships
- Full-text search
- Graph similarity operations
- SQLite WAL mode with LRU caching

## v0.1.0

### Initial Release

- Basic Zettelkasten note creation
- Markdown + SQLite dual storage
- Simple tagging and search
- Fork of zettelkasten-mcp

---

## Upgrade Guide

### From v0.3.0 to v0.4.0

1. **Update environment variables:**
   ```bash
   # Change ZETTELKASTEN_* to PARAZETTEL_*
   export PARAZETTEL_VENV_PYTHON="..."
   export PARAZETTEL_NOTES_DIR="..."
   export PARAZETTEL_DATABASE_PATH="..."
   ```

2. **Update MCP configuration** in `~/.claude.json`:
   ```json
   {
     "mcpServers": {
       "parazettel": {  // Changed from "parazettle"
         "env": {
           "PARAZETTEL_NOTES_DIR": "...",  // Changed from ZETTELKASTEN_
           // ...
         }
       }
     }
   }
   ```

3. **Update plugin:**
   ```bash
   rm -rf ~/.claude/plugins/parazettle-helper  # Old name
   cp -r parazettel-helper ~/.claude/plugins/   # New name
   ```

4. **Update settings.json:**
   ```json
   {
     "enabledPlugins": ["parazettel-helper"]  // Changed from parazettle-helper
   }
   ```

5. **Reinstall MCP server:**
   ```bash
   cd parazettel-marketplace-package
   source .venv/bin/activate
   uv sync --extra dev
   ```

### Breaking Changes

- Environment variable prefix changed: `ZETTELKASTEN_*` → `PARAZETTEL_*`
- Package name changed: `parazettle` → `parazettel`
- Hook scripts now use stdin JSON instead of environment variables for session context

### Migration Notes

- Existing notes and database are fully compatible (no schema changes)
- Update all configuration files to use new names
- Hooks will automatically use `~/.claude/temp/` for insights storage

---

## Roadmap

### Planned Features

- Obsidian plugin integration
- Web interface for vault browsing
- Export to various formats (PDF, HTML)
- Advanced graph visualization
- Collaborative vaults with sync
- Mobile app for capture on the go

### Under Consideration

- AI-powered note suggestions
- Automatic tag extraction
- Citation management
- Bi-directional sync with other PKM tools
- Plugin API for custom workflows

---

## Support

For issues, feature requests, or questions:
- GitHub Issues: https://github.com/BDKingDev/bdking-claude-plugins/issues
- Documentation: [README.md](README.md)
- Installation help: [INSTALL.md](INSTALL.md)

# Package Contents

This package contains everything needed to run Parazettel: the MCP server, Claude Code plugin, documentation, and tests.

## Directory Structure

```
parazettel-marketplace-package/
├── README.md                      # Feature overview and usage guide
├── QUICKSTART.md                  # 5-minute installation guide
├── INSTALL.md                     # Detailed installation instructions
├── marketplace.json               # Marketplace metadata
├── LICENSE                        # MIT License
├── .gitignore                     # Git ignore rules
├── .mcp.json.example              # Example MCP server configuration
│
├── src/                           # MCP Server source code
│   └── parazettel_mcp/
│       ├── main.py                # MCP server entry point
│       ├── config.py              # Configuration management
│       ├── models/                # Data models (Note, Task, Project, etc.)
│       ├── server/                # MCP server implementation
│       ├── services/              # Business logic (ZettelService, SearchService)
│       └── storage/               # Repository layer (NoteRepository)
│
├── tests/                         # Test suite
│   ├── test_integration.py        # Integration tests
│   ├── test_mcp_server.py         # MCP server tests
│   ├── test_note_repository.py    # Storage tests
│   ├── test_zettel_service.py     # Service layer tests
│   └── ...
│
├── parazettel-helper/             # Claude Code Plugin
│   ├── README.md                  # Plugin usage documentation
│   ├── .mcp.json                  # Plugin MCP configuration
│   ├── .claude-plugin/            # Plugin metadata
│   │   └── plugin.json
│   ├── skills/                    # User-invocable commands
│   │   ├── pzk-personal-note/     # Process personal transcripts
│   │   ├── pzk-meeting/           # Process meeting transcripts
│   │   ├── pzk-training/          # Process training materials
│   │   └── pzk-chat-session/      # Capture session insights
│   ├── agents/                    # Specialized extraction agents
│   │   ├── extractor.md           # Personal note extraction
│   │   └── meeting-extractor.md   # Meeting note extraction
│   ├── hooks/                     # Automatic insight capture
│   │   ├── hooks.json             # Hook configuration
│   │   └── scripts/
│   │       ├── extract-chat-ideas.py     # PreCompact extraction
│   │       └── post-compact-prune.py     # PostCompact ingestion
│   └── references/                # Reference documentation
│       ├── atomization.md
│       └── project-resolution.md
│
├── docs/                          # Additional documentation
│   ├── mcp-testing-guide.md       # How to test MCP tools
│   ├── para-gtd-guide.md          # Task management workflow
│   ├── prompts/                   # Chat and system prompts
│   │   ├── chat/                  # Knowledge exploration prompts
│   │   └── system/                # System prompt examples
│   └── project-knowledge/         # Development knowledge
│       ├── dev/                   # Developer notes
│       └── user/                  # User guide notes
│
├── pyproject.toml                 # Python package configuration
└── setup.py                       # Legacy setup script
```

## File Descriptions

### Root Documentation

- **README.md** — Complete feature overview, usage examples, and API reference
- **QUICKSTART.md** — Minimal steps to get running in 5 minutes
- **INSTALL.md** — Step-by-step installation with troubleshooting
- **marketplace.json** — Package metadata for marketplace listings
- **LICENSE** — MIT License terms
- **.mcp.json.example** — Example MCP server configuration

### MCP Server (`src/parazettel_mcp/`)

The core Zettelkasten engine that runs as an MCP server.

**Key files:**
- `main.py` — Entry point, starts MCP server
- `config.py` — Environment variable configuration
- `models/db_models.py` — SQLAlchemy ORM models
- `models/schema.py` — Pydantic schemas for validation
- `server/mcp_server.py` — MCP tool definitions (26 tools)
- `services/zettel_service.py` — Note CRUD operations
- `services/search_service.py` — Full-text search and graph operations
- `storage/note_repository.py` — Database access layer with caching

**Features:**
- 26 MCP tools for notes, tasks, projects, and areas
- WAL-mode SQLite with LRU cache for performance
- Semantic link types with inverse relationships
- Full-text search with FTS5
- Graph operations (similar notes, central notes, orphans)

### Claude Code Plugin (`parazettel-helper/`)

Adds skills, agents, and hooks for automatic insight extraction.

**Skills** (user-invocable commands):
- `pzk-personal-note` — Process personal transcripts and voice memos
- `pzk-meeting` — Extract meeting decisions and action items
- `pzk-training` — Convert training materials to atomic notes
- `pzk-chat-session` — Capture insights from coding sessions

**Agents** (specialized extractors):
- `extractor` — Graph-blind candidate extraction
- `meeting-extractor` — Attribution-aware meeting extraction

**Hooks** (automatic capture):
- `PreCompact` — Extracts insights before context compression
- `PostCompact` — Ingests, prunes duplicates, creates links

**Configuration:**
- `.mcp.json` — MCP server configuration for plugin
- `.claude-plugin/plugin.json` — Plugin metadata

### Tests (`tests/`)

Comprehensive test suite for MCP server functionality.

**Test files:**
- `conftest.py` — Pytest fixtures and configuration
- `test_integration.py` — End-to-end workflow tests
- `test_mcp_server.py` — MCP tool invocation tests
- `test_note_repository.py` — Database layer tests
- `test_zettel_service.py` — Business logic tests
- `test_search_service.py` — Search and similarity tests
- `test_semantic_links.py` — Link type and inverse tests
- `test_task_model.py` — Task-specific tests
- `test_task_service.py` — Task workflow tests
- `test_models.py` — Schema validation tests

**Run tests:**
```bash
.venv/bin/python -m pytest tests/
```

### Documentation (`docs/`)

- `mcp-testing-guide.md` — How to test MCP tools interactively
- `para-gtd-guide.md` — Task management with GTD + PARA
- `prompts/chat/` — Chat prompts for knowledge exploration
- `prompts/system/` — System prompt examples
- `project-knowledge/` — Development notes and decisions

## Installation Summary

1. **Install MCP server** — `uv venv --python 3.13 && uv sync --extra dev`
2. **Set environment variables** — `PARAZETTEL_VENV_PYTHON`, `PARAZETTEL_NOTES_DIR`, etc.
3. **Create notes directory** — `mkdir -p ~/Documents/zettelkasten`
4. **Add to `~/.claude.json`** — Register MCP server
5. **Copy plugin** — `cp -r parazettel-helper ~/.claude/plugins/`
6. **Enable plugin** — Add to `~/.claude/settings.json`

See [QUICKSTART.md](QUICKSTART.md) or [INSTALL.md](INSTALL.md) for complete instructions.

## Dependencies

**MCP Server:**
- Python 3.13+
- SQLAlchemy 2.0+
- Pydantic 2.0+
- anthropic-mcp 1.2+

**Plugin:**
- Claude Code 1.0+
- Python 3.13+ (for hooks)

**Optional:**
- pytest (for running tests)
- uv (recommended package manager)

## License

MIT License — See [LICENSE](LICENSE) for details.

## Support

- GitHub Issues: https://github.com/BDKingDev/bdking-claude-plugins/issues
- Documentation: [README.md](README.md)
- Installation help: [INSTALL.md](INSTALL.md)

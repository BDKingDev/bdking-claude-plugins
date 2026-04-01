# Bailey's Claude Code Custom Marketplace

A personal collection of Claude Code plugins and MCP servers for knowledge management, task tracking, and development workflows.

## Available Packages

### [Parazettel](packages/parazettel/) — Zettelkasten + GTD/PARA

Complete knowledge management and task system combining Zettelkasten (atomic notes + semantic links) with GTD and PARA workflows.

**Features:**
- 26 MCP tools for notes, tasks, projects, and areas
- Automatic insight extraction from conversations
- Meeting and transcript processing
- Semantic linking and graph operations
- Full GTD/PARA workflow support

**Installation:** See [packages/parazettel/QUICKSTART.md](packages/parazettel/QUICKSTART.md)

## Installation

### Add This Marketplace to Claude Code

1. **Clone this repository:**
   ```bash
   git clone https://github.com/BDKingDev/bdking-claude-plugins.git
   cd bdking-claude-plugins
   ```

2. **Install a package:**
   ```bash
   cd packages/parazettel
   # Follow the package's QUICKSTART.md
   ```

### Browse Packages

Each package in `packages/` contains:
- Complete installation instructions
- MCP server source code (if applicable)
- Claude Code plugin files
- Documentation and examples

## Package Index

| Package | Version | Type | Description |
| --- | --- | --- | --- |
| [parazettel](packages/parazettel/) | 0.4.0 | MCP + Plugin | Zettelkasten knowledge management with GTD/PARA workflows |

## Contributing

Want to add your own packages? Fork this repo and submit a PR!

### Package Requirements

Each package should include:
1. **README.md** — Feature overview and usage guide
2. **QUICKSTART.md** — Fast installation instructions
3. **marketplace.json** — Package metadata
4. **MCP server code** (if applicable) — In `src/` directory
5. **Plugin files** (if applicable) — Complete plugin directory
6. **Tests** — Comprehensive test suite
7. **LICENSE** — Open source license

### Directory Structure

```
packages/
├── your-package-name/
│   ├── README.md
│   ├── QUICKSTART.md
│   ├── marketplace.json
│   ├── src/              # MCP server code
│   ├── plugin-name/      # Claude Code plugin
│   ├── tests/            # Test suite
│   └── docs/             # Additional documentation
```

## Support

For package-specific issues, see the package's documentation. For marketplace issues:
- GitHub Issues: https://github.com/BDKingDev/bdking-claude-plugins/issues

## License

This marketplace is MIT licensed. Individual packages may have different licenses—see each package's LICENSE file.

---

## About This Marketplace

This is a custom Claude Code marketplace for personal use and sharing. It follows the standard marketplace format:

- **Packages** — Self-contained in `packages/` directory
- **Metadata** — Each package has `marketplace.json`
- **Installation** — Each package has its own installation guide
- **Documentation** — Comprehensive docs for each package

## Quick Links

- [Parazettel Quick Start](packages/parazettel/QUICKSTART.md)
- [Parazettel Full Docs](packages/parazettel/README.md)
- [Package Index](marketplace-index.json)

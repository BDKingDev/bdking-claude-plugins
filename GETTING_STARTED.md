# Getting Started with Bailey's Claude Code Marketplace

This marketplace contains custom Claude Code plugins and MCP servers. Here's how to use it.

## For Users

### Browse Available Packages

See [README.md](README.md) for the full package list, or browse the `packages/` directory.

Currently available:
- **[Parazettel](packages/parazettel/)** — Zettelkasten + GTD/PARA knowledge management

### Install a Package

Each package has its own installation guide:

1. **Quick installation:** Follow the package's `QUICKSTART.md`
2. **Detailed installation:** Follow the package's `INSTALL.md`
3. **Troubleshooting:** See the package's `README.md`

Example:

```bash
# Navigate to a package
cd packages/parazettel

# Follow the quickstart guide
cat QUICKSTART.md

# Or the detailed guide
cat INSTALL.md
```

## For Contributors

### Adding Your Own Package

Want to share your Claude Code plugin or MCP server? See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed instructions.

**Quick overview:**

1. Fork this repo
2. Create your package in `packages/your-package-name/`
3. Include required files (README, QUICKSTART, marketplace.json, LICENSE)
4. Update `marketplace-index.json`
5. Test thoroughly
6. Submit a pull request

### Package Structure

```
packages/your-package-name/
├── README.md              # Feature overview
├── QUICKSTART.md          # Fast installation
├── marketplace.json       # Package metadata
├── LICENSE                # Package license
├── src/                   # MCP server code (if applicable)
├── plugin-name/           # Claude Code plugin (if applicable)
└── tests/                 # Test suite
```

## Repository Structure

```
.
├── README.md                    # Marketplace overview
├── marketplace-index.json       # Package registry
├── CONTRIBUTING.md              # Contribution guidelines
├── LICENSE                      # Marketplace license
│
├── packages/                    # All packages
│   └── parazettel/              # Example: Parazettel package
│       ├── README.md
│       ├── QUICKSTART.md
│       ├── marketplace.json
│       ├── src/                 # MCP server
│       └── parazettel-helper/   # Claude Code plugin
│
└── .github/                     # GitHub configuration
    ├── workflows/               # CI/CD workflows
    └── ISSUE_TEMPLATE/          # Issue templates
```

## Using This Marketplace with Claude Code

### Option 1: Clone Locally (Recommended)

```bash
git clone https://github.com/BDKingDev/bdking-claude-plugins.git
cd bdking-claude-plugins
cd packages/parazettel  # or any package
# Follow installation instructions
```

### Option 2: Direct Package Installation

If a package URL is available:

```bash
curl -L https://github.com/BDKingDev/bdking-claude-plugins/archive/main.zip -o marketplace.zip
unzip marketplace.zip
cd bdking-claude-plugins-main/packages/parazettel
# Follow installation instructions
```

## Support

### Getting Help

- **Package-specific issues:** See the package's README or open an issue tagged with the package name
- **Marketplace issues:** Open a general issue
- **Contributing questions:** See [CONTRIBUTING.md](CONTRIBUTING.md)

### Reporting Issues

Use the issue templates:
- [Bug Report](.github/ISSUE_TEMPLATE/bug_report.md)
- [Feature Request](.github/ISSUE_TEMPLATE/feature_request.md)

## Marketplace Metadata

This marketplace follows a standard format:

- **marketplace-index.json** — Central registry of all packages
- **packages/** — Individual package directories
- **Each package has marketplace.json** — Package-specific metadata

This makes it easy to:
- Browse packages programmatically
- Auto-update package lists
- Integrate with package managers (future)

## Updates

To update packages:

```bash
cd claude-code-marketplace
git pull origin main

# Update a specific package
cd packages/parazettel
# Follow update instructions in the package's README
```

## Community

- **Issues:** Report bugs or request features
- **Pull Requests:** Contribute packages or improvements
- **Discussions:** Ask questions or share ideas

## License

The marketplace infrastructure is MIT licensed. Individual packages may have different licenses—see each package's LICENSE file.

## Next Steps

1. **Browse packages:** See [README.md](README.md)
2. **Install a package:** Follow a package's QUICKSTART.md
3. **Contribute:** Read [CONTRIBUTING.md](CONTRIBUTING.md)

Happy coding with Claude! 🚀

# Contributing to Bailey's Claude Code Marketplace

Thank you for your interest in contributing! This marketplace accepts high-quality Claude Code plugins and MCP servers.

## How to Contribute

### Adding a New Package

1. **Fork this repository**

2. **Create your package directory:**
   ```bash
   mkdir -p packages/your-package-name
   cd packages/your-package-name
   ```

3. **Follow the package structure:**
   ```
   packages/your-package-name/
   ├── README.md              # Feature overview
   ├── QUICKSTART.md          # Fast installation
   ├── INSTALL.md             # Detailed instructions (optional)
   ├── marketplace.json       # Package metadata
   ├── LICENSE                # Package license
   ├── src/                   # MCP server code (if applicable)
   ├── plugin-name/           # Claude Code plugin (if applicable)
   ├── tests/                 # Test suite
   └── docs/                  # Additional documentation
   ```

4. **Create marketplace.json:**
   ```json
   {
     "name": "your-package",
     "displayName": "Your Package Name",
     "version": "1.0.0",
     "description": "Short description of your package",
     "author": "Your Name",
     "license": "MIT",
     "keywords": ["keyword1", "keyword2"],
     "category": "productivity",
     "mcp": {
       "server": "your-server-name",
       "tools": 10
     },
     "requirements": {
       "python": ">=3.11",
       "claudeCode": ">=1.0.0"
     }
   }
   ```

5. **Update marketplace-index.json:**
   Add your package to the `packages` array in the root `marketplace-index.json`

6. **Test your package:**
   - Verify installation instructions work
   - Test MCP server (if applicable)
   - Test plugin features (if applicable)
   - Run test suite

7. **Submit a pull request:**
   - Clear description of what your package does
   - Screenshots or demo GIFs (optional but encouraged)
   - Link to any external documentation

## Package Requirements

### Must Have

✅ **README.md** — Feature overview and usage examples
✅ **QUICKSTART.md** — Installation in 5-10 minutes
✅ **marketplace.json** — Complete metadata
✅ **LICENSE** — Open source license (MIT, Apache 2.0, GPL, etc.)
✅ **Working code** — Tested and functional
✅ **Documentation** — Clear usage instructions

### Should Have

⭐ **INSTALL.md** — Detailed step-by-step installation
⭐ **Tests** — Automated test suite
⭐ **Examples** — Usage examples and demos
⭐ **CONTRIBUTING.md** — How others can contribute to your package

### Nice to Have

💡 **Screenshots** — Visual examples
💡 **Demo videos** — Usage demonstrations
💡 **Changelog** — Version history
💡 **Troubleshooting** — Common issues and solutions

## Quality Standards

### Code Quality

- Follow Python PEP 8 style guide (for Python packages)
- Include type hints
- Handle errors gracefully
- Log appropriately
- No hardcoded secrets or credentials

### Documentation Quality

- Clear, concise writing
- Step-by-step instructions
- Code examples with comments
- Troubleshooting section
- Up-to-date with current version

### Testing

- Unit tests for core functionality
- Integration tests for MCP tools
- Hook tests (if applicable)
- Installation verification steps

## Categories

Choose the most appropriate category for your package:

- **productivity** — Task management, note-taking, workflow automation
- **development** — Dev tools, code analysis, CI/CD
- **knowledge** — PKM tools, knowledge graphs, note systems
- **communication** — Chat integrations, notifications
- **data** — Data processing, analysis, visualization
- **utilities** — General-purpose tools

## Package Naming

- Use lowercase with hyphens: `my-awesome-plugin`
- Be descriptive but concise
- Avoid generic names like "helper" or "utils"
- Check that the name isn't already taken

## Version Numbering

Follow [Semantic Versioning](https://semver.org/):

- **MAJOR.MINOR.PATCH** (e.g., 1.0.0)
- **MAJOR** — Breaking changes
- **MINOR** — New features (backward compatible)
- **PATCH** — Bug fixes

## License

Your package must have an open source license. Popular choices:

- **MIT** — Permissive, simple (recommended)
- **Apache 2.0** — Permissive with patent grant
- **GPL v3** — Copyleft, derivative works must also be GPL

The marketplace itself is MIT licensed, but packages can use different licenses.

## Maintenance

If you're adding a package:

- Be responsive to issues and PRs
- Keep documentation up-to-date
- Update dependencies regularly
- Fix critical bugs promptly
- Consider deprecation policy if you stop maintaining

## Review Process

Submissions will be reviewed for:

1. **Functionality** — Does it work as described?
2. **Quality** — Is the code well-written and tested?
3. **Documentation** — Are instructions clear and complete?
4. **Safety** — No security vulnerabilities or malicious code
5. **Value** — Does it provide useful functionality?

Reviews typically take 1-3 days. You may be asked to make changes before merging.

## Getting Help

- **Questions about contributing:** Open a Discussion
- **Bug reports:** Open an Issue
- **Feature requests:** Open an Issue with "enhancement" label
- **Security issues:** Email privately (don't open public issues)

## Code of Conduct

- Be respectful and professional
- Provide constructive feedback
- Welcome newcomers
- Focus on the work, not the person
- No harassment, discrimination, or inappropriate content

## Examples

Good examples of well-structured packages:

- [packages/parazettel/](packages/parazettel/) — Complete MCP + plugin with hooks

## Thank You!

Your contributions make this marketplace better for everyone. Thank you for sharing your work with the community! 🎉

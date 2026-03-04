# OpenClaw Skills Collection

This repository contains a collection of skills for [OpenClaw](https://github.com/openclaw/openclaw).

## Repository Structure

This is a **monorepo** using git subtrees. Each skill lives in its own subdirectory but can be managed independently.

```
openclaw-skills/
├── README.md                          # This file
├── lancedb-ollama-setup/              # Skill: LanceDB + Ollama setup
│   ├── SKILL.md                       # Skill definition
│   └── references/                    # Reference documents
│       ├── lancedb-pro-readme.md
│       └── ollama-autostart.md
└── adspower-rpa/                      # Skill: AdsPower RPA automation
    ├── SKILL.md                       # Skill definition
    ├── schema/                        # JSON schemas
    ├── templates/                     # Flow templates
    ├── examples/                      # Example flows
    └── usecase/                       # Tested use cases
```

## Skills

### lancedb-ollama-setup

Configure memory-lancedb-pro plugin with Ollama local embedding models.

**Features:**
- Ollama installation guide for Windows/macOS/Linux
- Embedding model configuration (nomic-embed-text, qwen3-embedding:4b)
- OpenClaw configuration examples
- Comprehensive testing guide
- Troubleshooting common issues
- Auto-start configuration for Ollama

See [lancedb-ollama-setup/SKILL.md](lancedb-ollama-setup/SKILL.md) for details.

### adspower-rpa

Generate RPA flow JSON for AdsPower fingerprint browser automation.

**Features:**
- Complete node type reference (gotoUrl, clickElement, inputContent, etc.)
- Excel import/export operations
- Data extraction and form filling examples
- JSON schema validation
- Ready-to-use templates

See [adspower-rpa/SKILL.md](adspower-rpa/SKILL.md) for details.

## Managing Skills

### For Users

Each skill is self-contained. To use a skill:

1. Copy the skill directory to your OpenClaw skills folder
2. Or install the `.skill` package directly

### For Contributors

#### Adding a New Skill

```bash
# Create skill in its own branch
git checkout -b my-new-skill
# ... create skill files ...
git push origin my-new-skill

# Add to main monorepo
git checkout main
git subtree add --prefix=my-new-skill origin/my-new-skill --squash
```

#### Updating an Existing Skill

**Method 1: Update from subtree branch**

```bash
git checkout main
git subtree pull --prefix=lancedb-ollama-setup origin/lancedb-ollama-setup --squash
```

**Method 2: Update subtree from main**

```bash
git checkout main
# Edit files in lancedb-ollama-setup/
git subtree push --prefix=lancedb-ollama-setup origin/lancedb-ollama-setup
```

## Git Subtree Workflow

This repository uses **git subtree** to manage skills:

- **Main branch (`main`)**: Contains all skills integrated together
- **Skill branches (`lancedb-ollama-setup`, etc.)**: Individual skill development

### Why Subtree?

- ✅ Skills can be developed independently
- ✅ Skills can be cloned/pulled separately
- ✅ Main repo always has complete picture
- ✅ No submodule complexity for users

## License

MIT - See individual skill directories for details.

## Contributing

1. Create your skill in a separate branch
2. Push the branch to this repository
3. Create a PR to add it as a subtree to main

---

**Note**: Token has been configured in environment variables for automated pushes.

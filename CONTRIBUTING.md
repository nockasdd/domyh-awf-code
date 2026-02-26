# Contributing to DOMYH Awesome Code

Thank you for your interest in contributing! 🎉

## Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/domyh-awf-code.git`
3. Create a feature branch: `git checkout -b feat/your-feature`
4. Make your changes
5. Submit a Pull Request

## Adding a New Skill

1. Create directory: `.agent/skills/{category}/{skill-name}/`
2. Add required files:
   - `META.yaml` — Metadata, keywords, version (T1: ~100-400 tokens)
   - `SKILL.md` — Full skill content (T2: ~1,500 tokens)
   - Optional: `data/*.yaml` — Pattern data files
3. Update `.agent/manifest.yaml` — Add skill to the appropriate category
4. Update `README.md` — Increment skill count

## Adding a New IDE Config

1. Create directory: `configs/{ide-name}/`
2. Add root config file: `root.{expected-filename}`
3. Follow the SLIM Config v7 template (see any existing Markdown config as reference)
4. Update `configs/README.md` and `IDE_COMPATIBILITY.md`

## Version Bumping

Use the version bump script (SSoT: `.agent/core/VERSION.yaml`):

```bash
node scripts/bump-version.mjs patch          # 6.4.5 → 6.4.6
node scripts/bump-version.mjs minor          # 6.4.5 → 6.5.0
node scripts/bump-version.mjs patch --dry-run  # Preview only
```

## Code Style

- YAML: `yamllint` with relaxed config (max line 200)
- Markdown: `markdownlint` (MD013/MD033/MD041 disabled)
- JSON: Valid syntax checked by CI

## Pull Request Guidelines

- Keep PRs focused — one feature/fix per PR
- Update relevant documentation
- Ensure CI passes (YAML lint, Markdown lint, JSON check, version consistency)

---

_DOMYH Awesome Code • MIT License • NockDev_

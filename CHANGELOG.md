# Changelog

All notable changes to DOMYH Awesome Code will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v6.1.2] - 2026-02-03

### Added

- **NPM Package Distribution** - `@domyh/cli` now available on npm
  - `domyh init` - Initialize DOMYH in any project
  - `domyh add <skills>` - Add specific skills
  - `domyh list` - List available skills and workflows
  - `domyh info` - Show project detection results
  - `domyh update` - Update to latest version
  - `domyh run <workflow>` - Run workflow info

- **Agent Skills Compatibility** - Compatible with [agentskills.io](https://agentskills.io/) specification
  - Works with `npx skills add nockdev/domyh-skills`
  - SKILL.md files now have YAML frontmatter
  - Progressive disclosure architecture

- **Project Detection** - Automatic stack detection
  - Detects React, Vue, Angular, Next.js, Nuxt, Go, Python, Rust, etc.
  - Recommends skills based on detected stack
  - Works with package.json, go.mod, pyproject.toml, Cargo.toml, etc.

- **Centralized Versioning** - VERSION.yaml as Single Source of Truth
  - All 28 workflow component versions tracked
  - `/sync-version` workflow for batch updates

### Changed

- Standardized all workflow headers to consistent format (e.g., `# 🔬 /ap — Audit Pro v6.1.2`)
- Updated skill count from 33 to 34
- Updated workflow count from 29 to 31

### Fixed

- Version drift across 17 IDE/Agent configuration files
- Badge versions in README.md
- Inconsistent version references in .cursorrules, .windsurfrules, etc.

## [5.1.0] - 2026-01-31

### Added

- Multi-IDE compatibility (14 IDEs supported)
- Audit Pro v6.1.2 with 5-Expert Panel
- Think Pro v6.1.2 with multi-mode reasoning

### Changed

- Improved Progressive Disclosure architecture
- Enhanced project detection patterns

## [5.0.0] - 2026-01-28

### Added

- Version 5.0 major release
- BRANDING.yaml for centralized branding
- International language support (Tiếng Việt primary)

### Changed

- Complete skill system overhaul
- New workflow architecture

---

_DOMYH Awesome Code v6.1.2 • NockDev_

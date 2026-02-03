# DOMYH IDE Compatibility v5.5

> **14 AI Coding Assistants** • **95%+ Market Coverage** • **Zero Format Errors**

## 🚀 Quick Start

```bash
# Install
npx domyh-awf install

# Validate
npx domyh-awf validate

# Diagnose
npx domyh-awf doctor
```

## 📊 Supported IDEs

| IDE              | Path                                     | Format           | Status |
| ---------------- | ---------------------------------------- | ---------------- | ------ |
| Cursor           | `.cursor/rules/*.mdc`                    | YAML frontmatter | ✅     |
| Cline            | `.clinerules/*.md`                       | YAML + paths     | ✅     |
| Continue.dev     | `.continue/rules/*.md`                   | YAML + name      | ✅     |
| Roo Code         | `.roo/rules/*.md`                        | Pure Markdown    | ✅     |
| GitHub Copilot   | `.github/instructions/*.instructions.md` | applyTo          | ✅     |
| Windsurf         | `.windsurf/rules/*.md`                   | Pure Markdown    | ✅     |
| JetBrains AI     | `.aiassistant/rules/*.md`                | Pure Markdown    | ✅     |
| Amazon Q         | `.amazonq/rules/*.md`                    | Pure Markdown    | ✅     |
| Claude Code      | `.claude/skills/*/SKILL.md`              | YAML frontmatter | ✅     |
| Gemini           | `.gemini/styleguide.md`                  | Pure Markdown    | ✅     |
| Zed              | `.zed/rules/*.mdc`                       | YAML frontmatter | ✅     |
| Aider            | `.aider.conf.yml`                        | YAML config      | ✅     |
| CodeRabbit       | `.coderabbit.yaml`                       | YAML config      | ✅     |
| Sourcegraph Cody | `.sourcegraph/*.md`                      | Pure Markdown    | ✅     |

## ⚠️ Critical Bugs Fixed

### ISS-001: Cursor Globs Space Bug

```yaml
# ❌ WRONG - Silent failure
globs: **/*.cpp, **/*.h

# ✅ CORRECT - No spaces!
globs: **/*.cpp,**/*.h
```

### ISS-003: Continue.dev Field Name

```yaml
# ❌ WRONG
title: "Rule Name"

# ✅ CORRECT
name: "Rule Name"
```

### ISS-004: Roo Code Frontmatter

```markdown
# ❌ WRONG - Roo ignores this

---

## description: "Rule"

# ✅ CORRECT - Pure Markdown only

# Rule Name
```

## 📦 Profiles

| Profile    | Tokens | Use Case          |
| ---------- | ------ | ----------------- |
| `minimal`  | ~400   | CI, quick checks  |
| `standard` | ~1500  | Daily development |
| `full`     | ~3000  | Complete coverage |

## 🔧 CLI Commands

```bash
# Install for specific IDE
dawf install cursor

# Install all IDEs with profile
dawf install --ide all --profile standard

# Validate configurations
dawf validate

# Diagnose load order and tokens
dawf doctor
```

---

_DOMYH v5.5 • NockDev_

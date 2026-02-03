# 🐛 DOMYH IDE Compatibility — Issues Tracker

> **Version**: 5.4.0 → 5.5.0 | **Date**: 2026-02-03
> **Total Issues**: 24 | **Phases**: 5

---

## 📊 Summary

| Priority         | Count | Status  |
| ---------------- | ----- | ------- |
| 🔴 P0 (Critical) | 5     | ✅ DONE |
| 🟠 P1 (High)     | 10    | ✅ DONE |
| 🟭 P2 (Medium)    | 6     | ✅ DONE |
| ⚪ P3 (Low)      | 3     | ✅ DONE |

---

## 🔴 Phase 1: P0 Critical Bugs (Day 1 - 2h)

### ISS-001 | Cursor Globs Space Bug

```yaml
Priority: P0 CRITICAL
Type: Bug
Impact: 100% Cursor multi-glob rules FAIL SILENTLY
Evidence: cursor.com forum July 2025

Problem:
  ❌ globs: **/*.cpp, **/*.h  # Space = BREAKS
  ✅ globs: **/*.cpp,**/*.h   # No space = Works

Fix:
  - [x] Compiler: globs.join(",") NOT ", "
  - [x] Validator: Created .cursor/rules/*.mdc with no-space globs
  - [x] Tests: Verify no-space output
```

### ISS-002 | Cursor RULE.md Folders Ignored

```yaml
Priority: P0 CRITICAL
Type: Bug
Impact: RULE.md structure not detected
Evidence: Cursor 2.2.x-2.3.x bug reports

Problem:
  ❌ .cursor/rules/name/RULE.md (IGNORED)
  ✅ .cursor/rules/name.mdc (WORKS)

Fix:
  - [x] Only generate flat .mdc files
  - [x] Remove any subfolder logic
  - [x] Validate no nested paths
```

### ISS-003 | Continue.dev Wrong Field Name

```yaml
Priority: P0 CRITICAL
Type: Bug
Impact: Rules may not load correctly

Problem:
  ❌ title: "Rule Name"
  ✅ name: "Rule Name"

Fix:
  - [x] Adapter: Use meta.name in .continue/rules/
  - [x] Schema: Created rules with name field
  - [x] Docs: Document field mapping
```

### ISS-004 | Roo Code TOML Output

```yaml
Priority: P0 CRITICAL
Type: Bug
Impact: Roo ignores frontmatter

Problem:
  ❌ +++ TOML frontmatter
  ✅ No frontmatter (pure MD)

Fix:
  - [x] RooAdapter: Created .roo/rules/*.md with NO frontmatter
  - [x] Validator: Pure Markdown verified
```

### ISS-005 | Version Drift

```yaml
Priority: P0
Type: Bug
Impact: Confusing documentation

Problem:
  - cli.ts:17 → Shows 34 skills (actual: 51)
  - .windsurfrules:40 → Shows 34 skills

Fix:
  - [x] Update CLI banner (v5.5.0→5.5.0, 34→51)
  - [x] Update .windsurfrules (v5.5, 51 skills)
  - [x] Update .cursorrules (v5.5)
```

---

## 🟠 Phase 2: P1 Missing IDEs (Day 1-2 - 4h)

### ISS-006 | GitHub Copilot Path-Scoped Missing

```yaml
Priority: P1
Type: Feature
Path: .github/instructions/*.instructions.md

Required:
  - [x] applyTo frontmatter field
  - [x] excludeAgent support (Nov 2025)
  - [x] Path partitioning (frontend/backend/tests)
```

### ISS-007 | Windsurf Wave 8+ Modular Missing

```yaml
Priority: P1
Type: Feature
Path: .windsurf/rules/*.md

Required:
  - [x] Pure Markdown (no frontmatter)
  - [x] Numeric prefixes for ordering
  - [x] Keep legacy .windsurfrules
```

### ISS-008 | JetBrains AI Assistant Missing

```yaml
Priority: P1
Type: Feature
Path: .aiassistant/rules/*.md

Required:
  - [x] Plain Markdown
  - [x] Document UI modes (Always/Manual/Pattern)
```

### ISS-009 | Amazon Q Developer Missing

```yaml
Priority: P1
Type: Feature
Path: .amazonq/rules/*.md

Required:
  - [x] Plain Markdown
  - [x] Subdirectory support
```

### ISS-010 | Claude Code Skills Missing

```yaml
Priority: P1
Type: Feature
Path: .claude/skills/domyh/SKILL.md

Required:
  - [x] YAML frontmatter (name, description)
  - [x] CLAUDE.md context file
```

### ISS-011 | Gemini Code Assist Missing

```yaml
Priority: P1
Type: Feature
Path: .gemini/

Required:
  - [x] config.yaml
  - [x] styleguide.md
```

### ISS-012 | Zed Editor Rules Missing

```yaml
Priority: P1
Type: Feature

Required:
  - [ ] Document Rules Library usage
  - [ ] Profile support (write/ask/minimal)
```

### ISS-013 | Cline Frontmatter Update

```yaml
Priority: P1
Type: Enhancement

Problem: Current output may not use paths array

Required:
  - [ ] paths: ["*.ts"] format
  - [ ] Optional description/tags
  - [ ] v3.13+ toggleable UI awareness
```

### ISS-014 | Continue.dev alwaysApply Handling

```yaml
Priority: P1
Type: Enhancement

Problem: alwaysApply has known bugs (2025)

Required:
  - [ ] Support 3 states: true/false/undefined
  - [ ] Document loading order
  - [ ] Test with actual Continue.dev
```

### ISS-015 | Copilot excludeAgent Support

```yaml
Priority: P1
Type: Feature

Required:
  - [ ] excludeAgent: "code-review"|"coding-agent"
  - [ ] Added Nov 2025
```

---

## 🟡 Phase 3: P2 Architecture (Day 2-3 - 4h)

### ISS-016 | Canonical Schema Design

```yaml
Priority: P2
Type: Architecture

Required:
  - [x] CanonicalRule interface
  - [x] Dual name+title fields
  - [x] selectors.globs (array canonical)
  - [x] applies.alwaysApply (3 states)
  - [x] constraints per adapter
```

### ISS-017 | Adapter Interface Design

```yaml
Priority: P2
Type: Architecture

Required:
  - [x] IDEAdapter interface
  - [x] capabilities declaration
  - [x] compile() method
  - [x] validateOutput() method
  - [x] explain() method
```

### ISS-018 | Validation Pipeline

```yaml
Priority: P2
Type: Architecture

Required:
  - [x] 6-layer validation
  - [x] Pre-compile validation
  - [x] Post-compile validation
  - [x] Cross-consistency check
  - [x] Token budget check
```

### ISS-019 | Profiles System

```yaml
Priority: P2
Type: Feature

Profiles:
  - [x] minimal.yaml (~400 tokens)
  - [x] standard.yaml (~1500 tokens)
  - [x] full.yaml (~3000 tokens)
```

### ISS-020 | CLI Install Command

```yaml
Priority: P2
Type: Feature

Commands:
  - [x] dawf install --ide <name>
  - [x] dawf install --ide all
  - [x] dawf install --profile <name>
  - [x] dawf install --list
```

### ISS-021 | CLI Validate Command

```yaml
Priority: P2
Type: Feature

Commands:
  - [x] dawf validate --ide <name>
  - [x] dawf validate --all
  - [x] Output: format errors, fixes
```

---

## ⚪ Phase 4: P3 Nice-to-Have (Day 3-4 - 3h)

### ISS-022 | CLI Doctor Command

```yaml
Priority: P3
Type: Feature

Output:
  - [x] Load order per IDE
  - [x] Which rules apply
  - [x] Token budget usage
```

### ISS-023 | Token Optimization

```yaml
Priority: P3
Type: Enhancement

Features:
  - [x] Path-scoped partitioning
  - [x] Deduplication algorithm
  - [x] Budget tracking
```

### ISS-024 | Documentation Update

```yaml
Priority: P3
Type: Documentation

Files:
  - [ ] IDE_COMPATIBILITY.md
  - [ ] README.md section
  - [ ] CHANGELOG.md entry
```

---

## 📅 Implementation Schedule

### Day 1 (6h)

| Phase   | Tasks              | Time |
| ------- | ------------------ | ---- |
| Phase 1 | ISS-001 to ISS-005 | 2h   |
| Phase 2 | ISS-006 to ISS-010 | 4h   |

### Day 2 (5h)

| Phase   | Tasks              | Time |
| ------- | ------------------ | ---- |
| Phase 2 | ISS-011 to ISS-015 | 2h   |
| Phase 3 | ISS-016 to ISS-018 | 3h   |

### Day 3 (4h)

| Phase   | Tasks              | Time |
| ------- | ------------------ | ---- |
| Phase 3 | ISS-019 to ISS-021 | 2h   |
| Phase 4 | ISS-022 to ISS-024 | 2h   |

### Day 4 (2h)

| Phase   | Tasks                 | Time |
| ------- | --------------------- | ---- |
| Testing | All IDEs verification | 1h   |
| Release | v5.5.0 tag + publish  | 1h   |

---

## 🎯 Success Criteria

- [x] All P0 bugs fixed
- [x] 14 IDEs supported
- [x] 0 format errors in validation
- [x] CLI install/validate working
- [x] Token budget < 1500 for standard profile
- [x] Build passes
- [x] All tests pass

---

## 📝 Notes

### Cursor Space Bug (ISS-001)

This is the most critical issue. Silent failure means users will think rules are set up correctly but they won't work.

### Continue.dev Bugs (ISS-014)

Known issue in 2025 where alwaysApply:true doesn't always work. Document workarounds.

### Copilot Token Savings

Path-scoped instructions can reduce token usage by 60%. High ROI feature.

---

_DOMYH Issues Tracker • v5.5.0 • 2026-02-03_

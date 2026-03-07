# 🔧 IDE Configs — DOMYH Awesome Code

> Root configuration files for 23 configs (22 unique IDEs — copilot merged into vscode).
> Template version: **v7** (enforced MCP/skills, optimized for IDE size limits)

## Structure

Each directory contains one root config file named according to the IDE's expected format:

| IDE | Config File | Format |
|-----|------------|--------|
| Aider | `root.CONVENTIONS.md` | Markdown |
| Amazon Q | `root.amazonq.md` | Markdown |
| Amp | `root.AGENTS.md` | Markdown |
| Antigravity | `root.GEMINI.md` | Markdown |
| Augment | `root.guidelines.md` | Markdown |
| Claude | `root.CLAUDE.md` | Markdown |
| Cline | `root.clinerules.md` | Markdown |
| CodeRabbit | `root.coderabbit.yaml` | YAML |
| Codex | `root.AGENTS.md` | Markdown |
| Cody | `root.commands.json` | JSON |
| Continue | `root.continue.md` | Markdown |
| Copilot | `root.copilot-instructions.md` | Markdown |
| Cursor | `root.cursorrules` | Markdown |
| Gemini | `root.GEMINI.md` | Markdown |
| JetBrains | `root.guidelines.md` | Markdown |
| Kiro | `root.kiro.md` | Markdown |
| OpenCode | `root.opencode.json` | JSON |
| Roo | `root.roorules.md` | Markdown |
| Tabnine | `root.guidelines.md` | Markdown |
| Trae | `root.trae.md` | Markdown |
| VS Code | `root.copilot-instructions.md` | Markdown |
| Windsurf | `root.windsurfrules` | Markdown |
| Zed | `root.settings.json` | JSON |

## Usage

These files are copied to the user's project root during `nock awf init`. The `root.` prefix is stripped and becomes the actual filename (e.g., `root.GEMINI.md` → `GEMINI.md`).

## Content (v7)

All Markdown configs share identical core structure (~58 lines, ~2.8KB):
- ⛔ Mandatory MCP bootstrap + skills enforcement
- ❌ NEVER list for MCP-connected violations
- 5 core rules (CORE_001-003, SAFE_001, PERF_001)
- Terminal safety (Windows pipe/pager/interactive prevention)
- Skill path + 8 categories (97 skills)
- MCP tools reference (20 tools)
- Personas list (11 roles)

JSON/YAML configs use IDE-native formats with equivalent content.

## IDE Limits (researched)

| IDE | Hard Limit | Current Usage |
|-----|-----------|---------------|
| Windsurf | 6,000 chars/file | ~2,800 (47%) ✅ |
| Cursor | ~100 lines optimal | 58 lines ✅ |
| Copilot | First 8 lines weighted | Critical rules in L1-9 ✅ |
| Codex | 32KB concatenated | ~2.8KB ✅ |

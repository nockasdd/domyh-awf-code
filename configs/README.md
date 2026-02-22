# 🔧 IDE Configs — DOMYH Awesome Code

> Root configuration files for 23 supported IDEs/Agents.

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

## Content

All Markdown configs share identical core structure:
- Header with project name and language config
- Core rules reference (SACRED_RULES.xml)
- Slash commands table
- Persona list
- MCP tools table

JSON/YAML configs use IDE-native formats with equivalent content.

# 📊 IDE / Agent Compatibility Matrix — DOMYH Awesome Code

> **Version**: 6.3.9 | **Cập nhật**: 2026-02-14 | **Official Docs Verified** | **Extension Storage Forensics**
> **Tổng**: 22 IDEs/Agents | 4 Tiers | 19 MCP configs | 16 Skills-enabled

---

## 📋 Bảng Tổng Quan (22 IDEs)

### 🆕 Tier 0: Just Launched (1)

| #   | IDE/Agent        | Value   | Config File | Skills |   MCP   | Rules | Extension | Verified |
| --- | ---------------- | ------- | ----------- | :----: | :-----: | :---: | --------- | :------: |
| 1   | **OpenAI Codex** | `codex` | `AGENTS.md` |   ✅   | ✅ TOML |  ✅   | `.md`     |    ✅    |

### ⭐ Tier 1: Major IDEs (6)

| #   | IDE/Agent             | Value         | Config File               | Skills |   MCP   | Rules | Extension | Verified |
| --- | --------------------- | ------------- | ------------------------- | :----: | :-----: | :---: | --------- | :------: |
| 2   | **Cursor**            | `cursor`      | `.cursorrules`            |   ✅   |   ✅    |  ✅   | `.mdc`    |    ✅    |
| 3   | **Claude Code**       | `claude`      | `CLAUDE.md`               |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 4   | **Gemini CLI**        | `gemini`      | `GEMINI.md`               |   ✅   |   ✅    |  ✅   | `.md`     |    ✅    |
| 5   | **VS Code + Copilot** | `vscode`      | `copilot-instructions.md` |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 6   | **Windsurf**          | `windsurf`    | `.windsurfrules`          |   ✅   |   ✅    |  ✅   | `.md`     |    ✅    |
| 7   | **Antigravity**       | `antigravity` | `GEMINI.md`               |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |

### 📦 Tier 2: Popular Agents (12)

| #   | IDE/Agent                | Value        | Config File            | Skills |   MCP   | Rules | Extension | Verified |
| --- | ------------------------ | ------------ | ---------------------- | :----: | :-----: | :---: | --------- | :------: |
| 8   | **Cline**                | `cline`      | `.clinerules`          |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 9   | **Continue.dev**         | `continue`   | `.continue/rules/`     |   🔄   | ✅ YAML |  ✅   | `.md`     |    ✅    |
| 10  | **Roo Code**             | `roo`        | `.roorules`            |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 11  | **JetBrains AI (Junie)** | `jetbrains`  | `.junie/guidelines.md` |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 12  | **Amazon Q**             | `amazonq`    | `.amazonq/rules/`      |   🔄   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 13  | **Kiro**                 | `kiro`       | `.kiro/specs/`         |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 14  | **Zed Editor**           | `zed`        | `.rules`               |   ❌   | ✅ JSON |  ✅   | `.json`   |    ✅    |
| 15  | **Aider**                | `aider`      | `CONVENTIONS.md`       |   ❌   |   ❌    |  ✅   | `.md`     |    ✅    |
| 16  | **CodeRabbit**           | `coderabbit` | `.coderabbit.yaml`     |   ❌   |   ❌    |  🔄   | `.yaml`   |    ✅    |
| 17  | **Sourcegraph Cody**     | `cody`       | `.cody/commands.json`  |   ❌   |   ✅    |  ❌   | `.json`   |    ✅    |
| 18  | **Tabnine**              | `tabnine`    | `.tabnine/guidelines/` |   ❌   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 19  | **Trae AI**              | `trae`       | `.trae/.rules`         |   🔄   | ✅ JSON |  ✅   | `.md`     |    ✅    |

### 🔧 Tier 3: Extended Agents (4)

| #   | IDE/Agent        | Value      | Config File  | Skills |   MCP   | Rules | Extension | Verified |
| --- | ---------------- | ---------- | ------------ | :----: | :-----: | :---: | --------- | :------: |
| 20  | **Amp AI**       | `amp`      | `AGENTS.md`  |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 21  | **OpenCode**     | `opencode` | `.opencode/` |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |
| 22  | **Augment Code** | `augment`  | `.augment/`  |   ✅   | ✅ JSON |  ✅   | `.md`     |    ✅    |

> **Ghi chú**: IDE #23 = `copilot` đã merge vào `vscode` (#5)

> [!WARNING]
> **Đã loại bỏ**: Bolt.new (web-only, không file system), Void Editor (development paused Jan 2026), Supermaven (sunset, merged → Cursor mid-2025).

---

## 📁 Cây Thư Mục Dự Án (Tất cả IDEs)

```
root/
│
│ ── Root Config Files ──────────────────────────────────────
├── AGENTS.md                       # [1] Codex + [20] Amp
├── CLAUDE.md                       # [3] Claude Code
├── GEMINI.md                       # [4] Gemini + [7] Antigravity
├── CONVENTIONS.md                  # [15] Aider
├── .cursorrules                    # [2] Cursor
├── .windsurfrules                  # [6] Windsurf
├── .clinerules                     # [8] Cline
├── .roorules                       # [10] Roo Code
├── .coderabbit.yaml                # [16] CodeRabbit
│
│ ── IDE-Specific Directories ───────────────────────────────
├── .agents/                        # [1] Codex + [20] Amp
│   ├── skills/                     #   ✅ SKILL.md format
│   └── rules/                      #   ✅ Rules files
│
├── .cursor/                        # [2] Cursor
│   ├── skills/                     #   ✅ SKILL.md format
│   ├── rules/                      #   ✅ .mdc rules
│   ├── hooks/                      #   ✅ Agent hooks
│   └── commands/                   #   ✅ Slash commands
│
├── .claude/                        # [3] Claude Code
│   ├── skills/                     #   ✅ SKILL.md format
│   ├── rules/                      #   ✅ .md rules
│   ├── commands/                   #   ✅ Slash commands
│   └── settings.json               #   ✅ Team settings
│
├── .gemini/                        # [4] Gemini CLI
│   ├── skills/                     #   ✅ SKILL.md format
│   └── commands/                   #   ✅ TOML commands
│
├── .github/                        # [5] VS Code + Copilot
│   ├── copilot-instructions.md     #   ✅ Project guidelines
│   ├── instructions/               #   ✅ Modular instructions
│   ├── agents/                     #   ✅ Custom Agents (.agent.md)
│   └── prompts/                    #   ✅ Prompt Files (.prompt.md)
│
├── .windsurf/                      # [6] Windsurf
│   ├── skills/                     #   ✅ SKILL.md (docs.windsurf.com verified)
│   ├── rules/                      #   ✅ 4 activation modes
│   └── workflows/                  #   ✅ YAML frontmatter
│
├── .agent/                         # [7] Antigravity
│   ├── skills/                     #   ✅ SKILL.md (semantic match)
│   ├── workflows/                  #   ✅ Custom commands
│   ├── rules/                      #   ✅ Constitutional rules
│   └── templates/                  #   ✅ Templates
│
├── .cline/                         # [8] Cline
│   ├── skills/                     #   ✅ SKILL.md (v3.48.0)
│   └── commands/                   #   ✅ Workflows (Phase 3)
│
├── .continue/                      # [9] Continue.dev
│   ├── rules/                      #   ✅ .md rules
│   │   └── skills/                 #   🔄 Skills (Phase 3 transform)
│   ├── commands/                   #   ✅ Workflows (Phase 3)
│   └── mcpServers/                 #   ✅ MCP YAML configs
│
├── .roo/                           # [10] Roo Code
│   ├── skills/                     #   ✅ SKILL.md (docs.roocode.com verified)
│   ├── skills-{mode}/              #   ✅ Mode-specific skills
│   ├── rules/                      #   ✅ .md rules
│   ├── rules-{mode}/               #   ✅ Mode-specific rules
│   └── mcp.json                    #   ✅ Project MCP (recommended)
│
├── .junie/                         # [11] JetBrains AI (Junie)
│   ├── guidelines.md               #   ✅ Root config
│   ├── guidelines/                 #   ✅ .md guidelines
│   ├── skills/                     #   ✅ Via Codex integration
│   └── mcp/mcp.json                #   ✅ MCP config
│
├── .amazonq/                       # [12] Amazon Q
│   ├── skills/                     #   🔄 Skills (Phase 3)
│   ├── commands/                   #   ✅ Workflows (Phase 3)
│   ├── rules/                      #   ✅ .md rules
│   └── mcp.json                    #   ✅ MCP config (aws docs verified)
│
├── .kiro/                          # [13] Kiro
│   ├── skills/                     #   ✅ SKILL.md
│   ├── specs/                      #   ✅ Steering files
│   ├── hooks/                      #   ✅ 8 hook types
│   └── settings/mcp.json           #   ✅ MCP config
│
├── .zed/                           # [14] Zed Editor
│   └── settings.json               #   ✅ JSON settings + context_servers (MCP)
├── .rules                          # [14] Zed rules (compat .cursorrules, CLAUDE.md etc.)
│
├── .cody/                          # [17] Sourcegraph Cody
│   └── commands.json               #   ✅ Custom commands
│
├── .tabnine/                       # [18] Tabnine
│   ├── guidelines/                 #   ✅ .md guidelines
│   └── mcp_servers.json            #   ✅ MCP config
│
├── .trae/                          # [19] Trae AI
│   ├── .rules                      #   ✅ Root rules
│   ├── skills/                     #   🔄 Skills (Phase 3, MCP-based)
│   ├── commands/                   #   ✅ Workflows (Phase 3)
│   └── mcp.json                    #   ✅ MCP config
│
├── .opencode/                      # [21] OpenCode
│   ├── agents/                     #   ✅ Markdown agents
│   ├── commands/                   #   ✅ Custom commands
│   └── opencode.json               #   ✅ Config
│
├── .augment/                       # [22] Augment Code
│   ├── skills/                     #   ✅ Primary skill location
│   └── commands/                   #   ✅ Workflows (Phase 3)
│
│ ── VS Code / Shared ──────────────────────────────────────
├── .vscode/                        # [5] VS Code + [20] Amp
│   └── mcp.json                    #   ✅ MCP Servers config
│
└── .mcp.json                       # [3] Claude Code (project MCP)
```

---

## 🔌 MCP Support Chi Tiết (20 IDEs)

| #   | IDE             | Config Path                                         | Format |       Scope       | Note                                                    |
| --- | --------------- | --------------------------------------------------- | :----: | :---------------: | ------------------------------------------------------- |
| 1   | **Codex**       | `~/.codex/config.toml`                              |  TOML  |      Global       | `[mcp_servers]` section                                 |
| 2   | **Cursor**      | `~/.cursor/mcp.json`                                |  JSON  |      Global       | Cline-compatible format                                 |
| 3   | **Claude**      | `.mcp.json` / `~/.claude.json`                      |  JSON  |       Both        | CLI: `.mcp.json` (project), Desktop: OS path            |
| 4   | **Gemini CLI**  | `~/.gemini/settings.json`                           |  JSON  |      Global       | `mcpServers` key                                        |
| 5   | **VS Code**     | `.vscode/mcp.json`                                  |  JSON  |      Project      | Also used by Amp, Void                                  |
| 6   | **Windsurf**    | `~/.codeium/windsurf/mcp_config.json`               |  JSON  |      Global       | Cascade integration                                     |
| 7   | **Antigravity** | `~/.gemini/antigravity/mcp_config.json`             |  JSON  |      Global       | Google IDE                                              |
| 8   | **Cline**       | globalStorage `cline_mcp_settings.json`             |  JSON  |      Per-IDE      | ⚠️ Isolated per IDE fork — see §Extension Storage       |
| 9   | **Continue**    | `~/.continue/config.yaml` `mcpServers`              |  YAML  |      Shared       | ⚠️ Shared across ALL IDE forks — see §Extension Storage |
| 10  | **Roo**         | globalStorage `mcp_settings.json` / `.roo/mcp.json` |  JSON  | Per-IDE + Project | ⚠️ Global=isolated, Project=shared — see §Ext Storage   |
| 11  | **JetBrains**   | `.junie/mcp/mcp.json`                               |  JSON  |       Both        | ⚠️ `mcp.json` NOT `servers.json`                        |
| 12  | **Amazon Q**    | `.amazonq/mcp.json` / `~/.aws/amazonq/mcp.json`     |  JSON  |       Both        | ✨ NEW: Confirmed mid-2025                              |
| 13  | **Kiro**        | `.kiro/settings/mcp.json`                           |  JSON  |      Project      | AWS integration                                         |
| 14  | **Zed**         | `settings.json` `context_servers`                   |  JSON  |      Global       | ✨ NEW: Extensions + custom servers                     |
| 17  | **Cody**        | `~/.config/cody/mcp_servers.json`                   |  JSON  |      Global       | Windows: `%USERPROFILE%/.config/cody/`                  |
| 18  | **Tabnine**     | `.tabnine/mcp_servers.json`                         |  JSON  |       Both        | Enterprise, STDIO/HTTP/SSE                              |
| 19  | **Trae**        | `.trae/mcp.json`                                    |  JSON  |      Project      | ByteDance                                               |
| 20  | **Amp**         | `.vscode/mcp.json`                                  |  JSON  |      Project      | Shares VS Code config                                   |
| 21  | **OpenCode**    | `opencode.json` `mcp` section                       |  JSON  |       Both        | ✨ NEW: Local+Remote+OAuth, per-agent                   |
| 22  | **Augment**     | `~/.augment/settings.json`                          |  JSON  |      Global       | Settings Panel UI + Easy MCP (Jul 2025)                 |

---

## 🗄️ Extension Storage Architecture (VS Code Forks)

> ⚠️ **Critical**: Extensions cài trên VS Code forks (Cursor, Windsurf, Antigravity, Trae) có **storage riêng biệt** cho mỗi fork.
> MCP settings trong globalStorage **KHÔNG SHARED** giữa các IDE forks.

### 3 Storage Strategies

| Strategy                             | Extensions                             | Lưu ở đâu                                             | Shared giữa IDE forks? |
| ------------------------------------ | -------------------------------------- | ----------------------------------------------------- | ---------------------- |
| **globalStorage** (per-IDE isolated) | Cline, Roo Code, Tabnine, Copilot Chat | `%APPDATA%\{IDE}\User\globalStorage\{ext-id}\`        | ❌ **KHÔNG**           |
| **Home Directory** (IDE-shared)      | Continue                               | `~/.continue/config.yaml`                             | ✅ **CÓ**              |
| **Home Directory** (IDE-shared)      | Continue, Augment                      | `~/.continue/config.yaml`, `~/.augment/settings.json` | ✅ **CÓ**              |

### AppData Folder Name theo IDE Fork

> Verified trực tiếp trên filesystem (Windows `%APPDATA%`)

| IDE Fork        | AppData Folder | Ví dụ Full Path                             |
| --------------- | -------------- | ------------------------------------------- |
| **VS Code**     | `Code`         | `%APPDATA%\Code\User\globalStorage\`        |
| **Cursor**      | `Cursor`       | `%APPDATA%\Cursor\User\globalStorage\`      |
| **Windsurf**    | `Windsurf`     | `%APPDATA%\Windsurf\User\globalStorage\`    |
| **Antigravity** | `Antigravity`  | `%APPDATA%\Antigravity\User\globalStorage\` |
| **Trae**        | `Trae`         | `%APPDATA%\Trae\User\globalStorage\`        |

> macOS: `~/Library/Application Support/{IDE}/User/globalStorage/`
> Linux: `~/.config/{IDE}/User/globalStorage/`

### Extension MCP Settings Map

| Extension        | Publisher ID                 | MCP Filename                                   | Storage                 |
| ---------------- | ---------------------------- | ---------------------------------------------- | ----------------------- |
| **Cline**        | `saoudrizwan.claude-dev`     | `settings/cline_mcp_settings.json`             | globalStorage (per-IDE) |
| **Roo Code**     | `rooveterinaryinc.roo-cline` | `settings/mcp_settings.json`                   | globalStorage (per-IDE) |
| **Continue**     | `continue.continue`          | `~/.continue/config.yaml` → key `mcpServers`   | Home dir (shared)       |
| **Tabnine**      | `tabnine.tabnine-vscode`     | (trong globalStorage)                          | globalStorage (per-IDE) |
| **Augment**      | `augmentcode.augment`        | `~/.augment/settings.json` (Settings Panel UI) | Home dir (shared)       |
| **Copilot Chat** | `github.copilot-chat`        | N/A (built-in)                                 | globalStorage (per-IDE) |

> **Source**: Filesystem forensics 2026-02-14 trên 4 IDE forks cùng máy Windows.
> **Docs**: [Roo Code MCP](https://docs.roocode.com/features/mcp/using-mcp-in-roo), [Continue MCP](https://docs.continue.dev/customize/model-providers/mcp), [VS Code Extension API](https://code.visualstudio.com/api/references/vscode-api#ExtensionContext)

### ⚠️ Hệ Quả Quan Trọng

1. **Cline trên VS Code ≠ Cline trên Antigravity**: MCP settings hoàn toàn riêng biệt
2. **Continue là ngoại lệ duy nhất**: Dùng `~/.continue/`, shared cho MỌI IDE fork
3. **Roo Code có 2 scope**: Global (globalStorage, per-IDE) + Project (`.roo/mcp.json`, shared)
4. **AWF installer**: Chỉ quản lý project-level files (rules, skills, workflows) — MCP trong globalStorage do extension quản lý

---

## 🎯 Skills Support Chi Tiết (16 IDEs)

| #   | IDE             | Skills Path                            |  Format  |      Activation      | Note                                            |
| --- | --------------- | -------------------------------------- | :------: | :------------------: | ----------------------------------------------- |
| 1   | **Codex**       | `.agents/skills/`                      | SKILL.md | `$skill-name` / auto | 6-tier Progressive Discovery                    |
| 2   | **Cursor**      | `.cursor/skills/`                      | SKILL.md |    Semantic match    | Auto-loaded by AI                               |
| 3   | **Claude**      | `.claude/skills/`                      | SKILL.md |    Semantic match    | Open Standard format                            |
| 4   | **Gemini**      | `.gemini/skills/`                      | SKILL.md |    Semantic match    | Via GEMINI.md                                   |
| 6   | **Windsurf**    | `.windsurf/skills/`                    | SKILL.md |    Auto / manual     | ✨ NEW: Global `~/.codeium/windsurf/skills/`    |
| 7   | **Antigravity** | `.agent/skills/`                       | SKILL.md |    Semantic match    | Full Skills+Workflows+Rules                     |
| 8   | **Cline**       | `.cline/skills/`                       | SKILL.md |      On-demand       | v3.48.0 (Jan 10, 2026)                          |
| 10  | **Roo Code**    | `.roo/skills/` + `.roo/skills-{mode}/` | SKILL.md |   Semantic + mode    | ✨ NEW: 4-level override, mode-specific         |
| 11  | **JetBrains**   | `.junie/skills/`                       | SKILL.md |      Via Codex       | Codex integration                               |
| 13  | **Kiro**        | `.kiro/skills/`                        | SKILL.md |      Via specs       | Steering files                                  |
| 20  | **Amp**         | `.agents/skills/`                      | SKILL.md |      Auto-match      | AGENTS.md standard                              |
| 21  | **OpenCode**    | `.opencode/agents/`                    |   .md    |      Config/CLI      | Markdown agents                                 |
| 22  | **Augment**     | `.augment/skills/`                     | SKILL.md |         Auto         | Also reads `.claude/skills/`, `.agents/skills/` |

#### 🔄 Phase 3: Newly Enabled (Transform)

| #   | IDE          | Skills Path               |  Format  | Activation | Note                        |
| --- | ------------ | ------------------------- | :------: | :--------: | --------------------------- |
| 9   | **Continue** | `.continue/rules/skills/` | SKILL.md | Transform  | Phase 3: via rules format   |
| 12  | **Amazon Q** | `.amazonq/skills/`        | SKILL.md | Transform  | Phase 3: AWS integration    |
| 19  | **Trae**     | `.trae/skills/`           | SKILL.md | Transform  | Phase 3: MCP-based delivery |

### ⚠️ Special Cases

| #   | IDE         | Status | Note                                     |
| --- | ----------- | :----: | ---------------------------------------- |
| 5   | **VS Code** | ⚠️ GUI | `.agent.md` Custom Agents (not SKILL.md) |

---

## 🪝 Hooks Support (3 IDEs)

| #   | IDE         |    Hook Types    | Note                                                                                                                                                   |
| --- | ----------- | :--------------: | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 2   | **Cursor**  | ✅ Project hooks | `.cursor/hooks/`                                                                                                                                       |
| 5   | **VS Code** |  ✅ Task hooks   | tasks.json integration                                                                                                                                 |
| 13  | **Kiro**    |  ✅ **8 types**  | `on_file_create`, `on_file_save`, `on_file_delete`, `on_prompt_submit`, `on_agent_stop`, `manual_trigger`, `pre_tool_use` (NEW), `post_tool_use` (NEW) |

---

## 🌐 Global Path Registry

| #   | IDE             | Global Path                     | Purpose                  |
| --- | --------------- | ------------------------------- | ------------------------ |
| 1   | **Codex**       | `~/.codex/`                     | Config + global skills   |
| 2   | **Cursor**      | `~/.cursor/rules/`              | Global rules             |
| 3   | **Claude**      | `~/.claude/`                    | Global config            |
| 4   | **Gemini**      | `~/.gemini/`                    | Global config            |
| 6   | **Windsurf**    | `~/.codeium/windsurf/`          | Skills + Memories        |
| 7   | **Antigravity** | `~/.gemini/antigravity/skills/` | Global skills            |
| 8   | **Cline**       | `~/Documents/Cline/Rules/`      | Global rules             |
| 9   | **Continue**    | `~/.continue/rules/`            | Global rules             |
| 10  | **Roo**         | `~/.roo/`                       | Global config            |
| 12  | **Amazon Q**    | `~/.aws/amazonq/`               | AWS config               |
| 15  | **Aider**       | `~/.aider.conf.yml`             | Global config            |
| 18  | **Tabnine**     | `~/.tabnine/`                   | Enterprise config        |
| 21  | **OpenCode**    | `~/.config/opencode/`           | Global agents + commands |
| 22  | **Augment**     | `~/.augment/`                   | Global settings          |

---

## 📊 Feature Matrix (Full)

### Bảng A — AWF Content Features

> Các features có source content trong `.agent/` — CLI install files thực tế

#### Legend

- ✅ = Direct (cùng format, copy trực tiếp từ `.agent/`)
- 🔄 = Transform (CLI chuyển đổi format khi install)
- ⚡ = Runtime-only (IDE hỗ trợ nhưng không install files từ AWF)
- ❌ = Không hỗ trợ

| #   | IDE         | Skills | Workflows | Rules | Personas | MCP | KI/Memory |
| --- | ----------- | :----: | :-------: | :---: | :------: | :-: | :-------: |
| 1   | Codex       |   ✅   |    ✅     |  ✅   |    🔄    | ✅  |    ✅     |
| 2   | Cursor      |   ✅   |    ✅     |  🔄   |    ✅    | ✅  |    ⚡     |
| 3   | Claude      |   ✅   |    ✅     |  ✅   |    ✅    | ✅  |    ❌     |
| 4   | Gemini      |   ✅   |    🔄     |  🔄   |    🔄    | ✅  |    🔄     |
| 5   | VS Code     |   ✅   |    🔄     |  ✅   |    🔄    | ✅  |    ❌     |
| 6   | Windsurf    |   ✅   |    🔄     |  ✅   |    🔄    | ✅  |    ⚡     |
| 7   | Antigravity |   ✅   |    ✅     |  ✅   |    🔄    | ✅  |    ✅     |
| 8   | Cline       |   ✅   |    🔄     |  ✅   |    🔄    | ✅  |    ❌     |
| 9   | Continue    |   🔄   |    🔄     |  ✅   |    🔄    | ✅  |    ❌     |
| 10  | Roo         |   ✅   |    ✅     |  ✅   |    🔄    | ✅  |    ❌     |
| 11  | JetBrains   |   🔄   |    🔄     |  ✅   |    🔄    | ✅  |    ❌     |
| 12  | Amazon Q    |   🔄   |    🔄     |  ✅   |    🔄    | ✅  |    ⚡     |
| 13  | Kiro        |   ✅   |    🔄     |  ✅   |    ❌    | ✅  |    ⚡     |
| 14  | Zed         |   🔄   |    ⚡     |  🔄   |    🔄    | ✅  |    ❌     |
| 15  | Aider       |   ❌   |    ⚡     |  🔄   |    🔄    | ❌  |    ❌     |
| 16  | CodeRabbit  |   ❌   |    ❌     |  🔄   |    ❌    | ❌  |    ❌     |
| 17  | Cody        |   🔄   |    ⚡     |  ❌   |    ❌    | ✅  |    ❌     |
| 18  | Tabnine     |   🔄   |    ⚡     |  ✅   |    ❌    | ✅  |    ❌     |
| 19  | Trae        |   🔄   |    🔄     |  🔄   |    ⚡    | ✅  |    ⚡     |
| 20  | Amp         |   ✅   |    ✅     |  ✅   |    ❌    | ✅  |    ⚡     |
| 21  | OpenCode    |   ✅   |    ✅     |  ✅   |    ❌    | ✅  |    ❌     |
| 22  | Augment     |   ✅   |    🔄     |  ✅   |    ❌    | ✅  |    ❌     |

### Bảng B — IDE-Native Features

> Features riêng của IDE, **không có source trong `.agent/`**. CLI inject config files nếu khả thi.

| #   | IDE        | Hooks | Mechanism                  | Config File             |
| --- | ---------- | :---: | -------------------------- | ----------------------- |
| 2   | Cursor     |  ✅   | `hooks.json` events        | `.cursor/hooks.json`    |
| 3   | Claude     |  ✅   | PreToolUse / PostToolUse   | `.claude/settings.json` |
| 5   | VS Code    |  🔄   | Limited via settings.json  | `.vscode/settings.json` |
| 13  | Kiro       |  ⚡   | Spec-driven events         | `.kiro/specs/`          |
| 14  | Zed        |  ⚡   | MCP context_servers        | `settings.json`         |
| 16  | CodeRabbit |  ⚡   | YAML hook config           | `.coderabbit.yaml`      |
| 19  | Trae       |  ⚡   | Agent events via SOLO mode | `.trae/.rules`          |
| —   | Others     |  ❌   | Không hỗ trợ hooks         | —                       |

### Thống kê — AWF Content

| Feature       | ✅ Direct | 🔄 Transform | ⚡ Runtime | ❌ None | Total hỗ trợ |
| ------------- | :-------: | :----------: | :--------: | :-----: | :----------: |
| **Skills**    |    13     |      5       |     0      |    4    |      18      |
| **Workflows** |     7     |      9       |     3      |    3    |      19      |
| **Rules**     |    14     |      6       |     0      |    2    |      20      |
| **Personas**  |     2     |      13      |     1      |    6    |      16      |
| **MCP**       |    19     |      0       |     0      |    3    |      19      |
| **KI/Memory** |     2     |      1       |     5      |   14    |      8       |

### Thống kê — IDE-Native

| Feature   | ✅ File-based | 🔄 Partial | ⚡ Runtime | ❌ None | Total hỗ trợ |
| --------- | :-----------: | :--------: | :--------: | :-----: | :----------: |
| **Hooks** |       2       |     1      |     4      |   15    |      7       |

---

## 🔄 Cách Cài Đặt

```bash
# Cài tất cả IDEs
nock awf install --all

# Cài theo tier
nock awf install --tier 1

# Cài IDE cụ thể
nock awf install --ide cursor
nock awf install --ide claude,gemini,antigravity

# Xem danh sách IDEs
nock awf install --list
```

---

_DOMYH Awesome Code v6.3.9 • 22 IDEs • Extension Storage Forensics • Platform Verified • Feb 14, 2026_

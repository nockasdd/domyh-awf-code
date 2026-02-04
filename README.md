<div align="center">

# 🚀 DOMYH Awesome Code v6.1.2

### **The Ultimate AI Coding Assistant for Developers**

[![npm version](https://img.shields.io/npm/v/domyh-awf?style=for-the-badge&color=blue)](https://www.npmjs.com/package/domyh-awf)
[![License](https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-51+-purple.svg?style=for-the-badge)](#-skills)
[![Workflows](https://img.shields.io/badge/workflows-31-orange.svg?style=for-the-badge)](#-commands)
[![IDEs](https://img.shields.io/badge/IDEs-22+-red.svg?style=for-the-badge)](#-ide-support)

**Portable** • **Multi-language** • **Universal IDE Support**

[Quick Start](#-quick-start) •
[Commands](#-commands) •
[Skills](#-skills) •
[IDE Support](#-ide-support) •
[Tiếng Việt](#-tiếng-việt)

---

<img src="https://raw.githubusercontent.com/github/explore/main/topics/artificial-intelligence/artificial-intelligence.png" width="120" alt="AI">

</div>

---

## 📖 Table of Contents

- [🚀 Quick Start](#-quick-start)
- [🎯 Commands](#-commands)
- [🧠 Skills (51+)](#-skills)
- [💻 IDE Support](#-ide-support)
- [📁 Project Structure](#-project-structure)
- [🇻🇳 Tiếng Việt](#-tiếng-việt)
- [📜 License](#-license)

---

## 🚀 Quick Start

### 📦 npm (Recommended)

```bash
# Install globally
npm install -g domyh-awf

# Initialize in your project
dawf init

# Or use npx without installing
npx domyh-awf init
```

### ⚡ Quick Install

```bash
# Quick install with Vietnamese
dawf init --lang vi -y

# Install for specific IDE (auto MCP setup)
dawf install --ide cursor
```

### 📋 Manual Installation

```bash
# Clone the repository
git clone https://github.com/nockasdd/domyh-awesome-code.git
cd domyh-awesome-code

# Copy to your project
cp -r .agent /path/to/your/project/
cp {CLAUDE.md,GEMINI.md,AGENTS.md,.cursorrules} /path/to/your/project/
```

> 💡 **During installation**, you'll be prompted to choose:
>
> - **Language**: English (default) or Vietnamese
> - **Target IDE**: Claude Code, Cursor, Gemini CLI, etc.

---

## 🎯 Commands

<details open>
<summary><h3>💻 Development</h3></summary>

| Command     | Description                                                                |
| :---------- | :------------------------------------------------------------------------- |
| `/code`     | 💻 Write production-ready code with proper error handling, types, and docs |
| `/dev`      | ▶️ Start development server: detect stack, run dev commands, validate      |
| `/debug`    | 🐛 Systematic debugging: reproduce → isolate → analyze → fix → verify      |
| `/test`     | ✅ Run tests and write new test cases with proper coverage                 |
| `/refactor` | 🔧 Refactoring: identify smells → plan → apply → verify tests pass         |
| `/generate` | 🏗️ Generate: models, APIs, components, services from templates             |

</details>

<details>
<summary><h3>📋 Planning & Design</h3></summary>

| Command      | Description                                                             |
| :----------- | :---------------------------------------------------------------------- |
| `/plan`      | 📋 Feature planning with impact analysis, task breakdown, estimation    |
| `/think`     | 💡 Brainstorming: explore ideas, research solutions, evaluate options   |
| `/visualize` | 🖼️ UI/UX: mockups, wireframes, component design, prototyping            |
| `/doc`       | 📝 Documentation: API docs, README, code comments, changelogs           |
| `/init`      | ✨ Initialize project with scaffolding, P0-P6 phases, progress tracking |

</details>

<details>
<summary><h3>🚀 Deployment & Ops</h3></summary>

| Command    | Description                                                  |
| :--------- | :----------------------------------------------------------- |
| `/deploy`  | 🚀 Deploy with pre-checks, rollback plan, post-verification  |
| `/env`     | 🔐 Environment: create, sync, validate .env, encrypt secrets |
| `/monitor` | 📡 Observability: logging, tracing, metrics, alerting        |
| `/perf`    | ⚡ Performance: CPU, memory, benchmarks, optimization        |
| `/revert`  | ⏪ Rollback: git, deployment, database                       |
| `/migrate` | 🗃️ Migrations: create, run, rollback, seed with safety       |

</details>

<details>
<summary><h3>🔍 Quality & Review</h3></summary>

| Command    | Description                                                                      |
| :--------- | :------------------------------------------------------------------------------- |
| `/ap`      | 🔬 **Audit Pro**: 5-expert panel (security, perf, arch, testing, best practices) |
| `/review`  | 👀 Code review for PRs: logic, quality, security, tests                          |
| `/modify`  | 🔧 Fix project: detect stack → analyze → plan → execute → verify                 |
| `/clean`   | 🧹 Cleanup: dead code, imports, unused dependencies                              |
| `/upgrade` | 📦 Dependencies: check outdated, safe updates, breaking changes                  |

</details>

<details>
<summary><h3>🛠️ Utility</h3></summary>

| Command        | Description                                               |
| :------------- | :-------------------------------------------------------- |
| `/status`      | 📊 Health: build, tests, coverage, lint, recent activity  |
| `/recap`       | 📖 Summary: completed tasks, files, decisions, next steps |
| `/suggest`     | ➡️ Smart suggestions based on project state               |
| `/orchestrate` | 🎭 Multi-Agent: coordinate tasks, delegate to specialists |
| `/help`        | ❓ All commands, examples, and language settings          |

</details>

---

## 🧠 Skills

<div align="center">

### **51+ Specialized Skills with Progressive Disclosure**

</div>

<table>
<tr>
<td width="33%" valign="top">

### 💬 Languages (14)

| Skill                                                                                                    | Version |
| :------------------------------------------------------------------------------------------------------- | :------ |
| ![Go](https://img.shields.io/badge/Go-00ADD8?style=flat&logo=go&logoColor=white)                         | 1.23+   |
| ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)             | 3.13    |
| ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat&logo=typescript&logoColor=white) | 5.x     |
| ![Rust](https://img.shields.io/badge/Rust-000000?style=flat&logo=rust&logoColor=white)                   | 2024    |
| ![C++](https://img.shields.io/badge/C++-00599C?style=flat&logo=cplusplus&logoColor=white)                | C++26   |
| ![C#](https://img.shields.io/badge/C%23-239120?style=flat&logo=csharp&logoColor=white)                   | 14      |
| ![Java](https://img.shields.io/badge/Java-ED8B00?style=flat&logo=openjdk&logoColor=white)                | 21+     |
| ![PHP](https://img.shields.io/badge/PHP-777BB4?style=flat&logo=php&logoColor=white)                      | 8.4     |
| ![Kotlin](https://img.shields.io/badge/Kotlin-7F52FF?style=flat&logo=kotlin&logoColor=white)             | 2.x     |
| ![Swift](https://img.shields.io/badge/Swift-F05138?style=flat&logo=swift&logoColor=white)                | 6       |
| ![Assembly](https://img.shields.io/badge/Assembly-654FF0?style=flat&logo=assemblyscript&logoColor=white) | x86/ARM |
| ![C](https://img.shields.io/badge/C-A8B9CC?style=flat&logo=c&logoColor=black)                            | C23     |
| ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) | ES2024  |
| ![Lua](https://img.shields.io/badge/Lua-2C2D72?style=flat&logo=lua&logoColor=white)                      | 5.5     |

</td>
<td width="33%" valign="top">

### 🖼️ Frameworks (8)

| Skill                                                                                                 | Version |
| :---------------------------------------------------------------------------------------------------- | :------ |
| ![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)             | 19      |
| ![Vue](https://img.shields.io/badge/Vue-4FC08D?style=flat&logo=vuedotjs&logoColor=white)              | 3.5     |
| ![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=nextdotjs&logoColor=white)     | 16      |
| ![Angular](https://img.shields.io/badge/Angular-DD0031?style=flat&logo=angular&logoColor=white)       | 19/20   |
| ![Nuxt](https://img.shields.io/badge/Nuxt-00DC82?style=flat&logo=nuxtdotjs&logoColor=white)           | 4       |
| ![Svelte](https://img.shields.io/badge/Svelte-FF3E00?style=flat&logo=svelte&logoColor=white)          | 5       |
| ![Flutter](https://img.shields.io/badge/Flutter-02569B?style=flat&logo=flutter&logoColor=white)       | 3.x     |
| ![Tailwind](https://img.shields.io/badge/Tailwind-06B6D4?style=flat&logo=tailwindcss&logoColor=white) | 4       |

</td>
<td width="33%" valign="top">

### ⚙️ DevOps & Support (11)

| Skill                                                                                                | Type          |
| :--------------------------------------------------------------------------------------------------- | :------------ |
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white)         | Containers    |
| ![Kubernetes](https://img.shields.io/badge/K8s-326CE5?style=flat&logo=kubernetes&logoColor=white)    | Orchestration |
| ![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonwebservices&logoColor=white)    | Cloud         |
| ![CI/CD](https://img.shields.io/badge/CI%2FCD-2088FF?style=flat&logo=githubactions&logoColor=white)  | Automation    |
| ![Database](https://img.shields.io/badge/Database-4479A1?style=flat&logo=postgresql&logoColor=white) | Data Layer    |
| ![Testing](https://img.shields.io/badge/Testing-14B8A6?style=flat&logo=vitest&logoColor=white)       | Quality       |
| ![Security](https://img.shields.io/badge/Security-D32F2F?style=flat&logo=owasp&logoColor=white)      | Core          |
| ![Coding Rules](https://img.shields.io/badge/Rules-6366F1?style=flat&logo=prettier&logoColor=white)  | Standards     |
| ![UI/UX](https://img.shields.io/badge/UI%2FUX-FF69B4?style=flat&logo=figma&logoColor=white)          | Design        |
| ![Electron](https://img.shields.io/badge/Electron-47848F?style=flat&logo=electron&logoColor=white)   | Desktop       |
| ![React Native](https://img.shields.io/badge/RN-61DAFB?style=flat&logo=react&logoColor=black)        | Mobile        |

</td>
</tr>
</table>

---

## 💻 IDE Support

<div align="center">

### 22 Supported IDEs & AI Agents

| Tier  | IDE                                                                                                             |        Config File        | Status |
| :---: | :-------------------------------------------------------------------------------------------------------------- | :-----------------------: | :----: |
| **1** | ![Claude](https://img.shields.io/badge/Claude_Code-CC785C?style=flat-square&logoColor=white)                    |        `CLAUDE.md`        |   ✅   |
| **1** | ![Gemini](https://img.shields.io/badge/Gemini_CLI-4285F4?style=flat-square&logo=google&logoColor=white)         |        `GEMINI.md`        |   ✅   |
| **1** | ![Cursor](https://img.shields.io/badge/Cursor-000000?style=flat-square&logoColor=white)                         |      `.cursorrules`       |   ✅   |
| **1** | ![Windsurf](https://img.shields.io/badge/Windsurf-00D4FF?style=flat-square&logoColor=white)                     |     `.windsurfrules`      |   ✅   |
| **1** | ![Copilot](https://img.shields.io/badge/GitHub_Copilot-000000?style=flat-square&logo=github&logoColor=white)    | `copilot-instructions.md` |   ✅   |
| **1** | ![VS Code](https://img.shields.io/badge/VS_Code-007ACC?style=flat-square&logo=visualstudiocode&logoColor=white) |   `.vscode/ai-rules.md`   |   ✅   |
| **2** | ![Cline](https://img.shields.io/badge/Cline-5D3FD3?style=flat-square&logoColor=white)                           |   `.clinerules/core.md`   |   ✅   |
| **2** | ![JetBrains](https://img.shields.io/badge/JetBrains_AI-000000?style=flat-square&logo=jetbrains&logoColor=white) |    `.idea/ai-rules.md`    |   ✅   |
| **2** | ![Amazon Q](https://img.shields.io/badge/Amazon_Q-FF9900?style=flat-square&logo=amazon&logoColor=white)         |    `.amazonq/rules.md`    |   ✅   |
| **2** | ![Codex](https://img.shields.io/badge/Codex-412991?style=flat-square&logoColor=white)                           |   `.codex/config.json`    |   ✅   |
| **2** | ![Aider](https://img.shields.io/badge/Aider-FF6B6B?style=flat-square&logoColor=white)                           |     `.aider.conf.yml`     |   ✅   |
| **2** | ![CodeRabbit](https://img.shields.io/badge/CodeRabbit-FF4081?style=flat-square&logoColor=white)                 |    `.coderabbit.yaml`     |   ✅   |
| **2** | ![Cody](https://img.shields.io/badge/Sourcegraph_Cody-FF5733?style=flat-square&logoColor=white)                 | `.sourcegraph/cody.json`  |   ✅   |

</div>

---

## 📁 Project Structure

```
domyh-awesome-code/
├── 📄 CLAUDE.md          # Claude Code config
├── 📄 GEMINI.md          # Gemini CLI config
├── 📄 AGENTS.md          # OpenHands config
├── 📄 .cursorrules       # Cursor config
├── 📁 .agent/
│   ├── 📄 manifest.yaml  # Agent configuration
│   ├── 📁 core/          # Engine configs (Router, Memory, Cache)
│   ├── 📁 rules/         # 17 modular rule files
│   ├── 📁 skills/        # 51 skill directories
│   ├── 📁 workflows/     # 31 command workflows
│   ├── 📁 mcp/           # HSA v5.0 MCP server (auto-built)
│   ├── 📁 i18n/          # en.yaml, vi.yaml
│   └── 📁 memory/        # Persistent state
├── 📁 domyh-awf-cli/     # CLI package (npm)
└── 📄 LICENSE            # MIT License
```

---

## 🇻🇳 Tiếng Việt

<details>
<summary><b>📖 Xem hướng dẫn tiếng Việt</b></summary>

### Cài Đặt Nhanh

```bash
# Cài đặt global
npm install -g domyh-awf

# Khởi tạo project
dawf init --lang vi -y

# Cài đặt cho Cursor
dawf install --ide cursor
```

### Các Lệnh Chính

| Lệnh      | Mô tả                              |
| :-------- | :--------------------------------- |
| `/code`   | 💻 Viết code production-ready      |
| `/debug`  | 🐛 Debug có hệ thống               |
| `/plan`   | 📋 Lên kế hoạch tính năng          |
| `/ap`     | 🔬 Audit chuyên sâu (5 chuyên gia) |
| `/deploy` | 🚀 Deploy lên production           |
| `/help`   | ❓ Xem tất cả lệnh                 |

### Ngôn Ngữ Hỗ Trợ

Agent hỗ trợ **51+ skills** bao gồm: Go, Python, TypeScript, Rust, C++, C#, Java, PHP, React, Vue, Next.js, Docker, Kubernetes, AWS, và nhiều hơn nữa.

</details>

---

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**Made with ❤️ by [NockDev](https://github.com/nockasdd)**

[![GitHub Stars](https://img.shields.io/github/stars/nockasdd/domyh-awesome-code?style=social)](https://github.com/nockasdd/domyh-awesome-code)
[![GitHub Forks](https://img.shields.io/github/forks/nockasdd/domyh-awesome-code?style=social)](https://github.com/nockasdd/domyh-awesome-code/fork)

**DOMYH Awesome Code v6.1.2** • 51 Skills • 31 Workflows • 22 IDEs

</div>

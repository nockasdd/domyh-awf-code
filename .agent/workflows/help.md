---
description: "❓ Show all available commands, usage examples, and language settings"
skills: { required: [], contextual: [] }
success_criteria: "All 44 commands listed with correct descriptions"
---

# ❓ /help — Command Reference

> 📋 44 Commands • 100 Skills • 26 IDEs

---

## 🚀 Start Here — 5 Essential Commands

> New to DOMYH? Start with these 5 commands. Everything else is optional.

| Command     | What It Does                | Example                    |
| ----------- | --------------------------- | -------------------------- |
| `/help`     | ❓ You're here — see all commands | `/help`               |
| `/code`     | 💻 Write or fix code        | `/code add login form`     |
| `/fix`      | ⚡ Quick-fix errors (<60s)  | `/fix build error`         |
| `/test`     | ✅ Run & write tests         | `/test`                    |
| `/suggest`  | ➡️ Smart next-step hints     | `/suggest`                 |

---

## 📚 Learning Path

```
Day 1:  /help → /code → /fix → /test → /suggest
Day 7:  + /plan → /think → /review → /refactor → /debug
Day 30: + /ap → /deploy → /orchestrate → /skill-create → /workflow
```

---

## Quick Reference

### 💻 Development (12 commands)

| Command              | Description                 | Example                        |
| -------------------- | --------------------------- | ------------------------------ |
| `/code [task]`       | 💻 Write & fix code         | `/code add login form`         |
| `/fix [error]`       | ⚡ Quick-fix (<60s)         | `/fix build error`             |
| `/debug [error]`     | 🐛 Systematic debugging     | `/debug timeout error`         |
| `/modify [target]`   | 🔄 Detect + analyze + fix   | `/modify auth module`          |
| `/refactor [target]` | 🔧 Code refactoring         | `/refactor extract utils`      |
| `/clean [scope]`     | 🧹 Remove dead code/imports | `/clean src/utils/`            |
| `/init [project]`    | ✨ Create new project        | `/init REST API with Go`       |
| `/scaffold [pattern]`| 🏗️ From project patterns    | `/scaffold crud Product`       |
| `/generate [type]`   | 🏗️ Code generation          | `/generate api Users`          |
| `/dev`               | ▶️ Start dev server          | `/dev`                         |
| `/git [cmd]`         | 🔀 Git operations            | `/git commit`                  |
| `/revert [target]`   | ⏪ Rollback changes          | `/revert last`                 |

### 📋 Planning & Thinking (4 commands)

| Command             | Description              | Example                    |
| ------------------- | ------------------------ | -------------------------- |
| `/plan [feature]`   | 📋 Feature planning      | `/plan shopping cart`      |
| `/think [topic]`    | 💡 Deep reasoning (6 methods) | `/think architecture` |
| `/prompt [task]`    | ✍️ Create AI prompts     | `/prompt system prompt`    |
| `/visualize [page]` | 🖼️ UI/UX mockups         | `/visualize dashboard`     |

### ✅ Quality & Testing (6 commands)

| Command            | Description                    | Example              |
| ------------------ | ------------------------------ | -------------------- |
| `/test`            | ✅ Run & write tests            | `/test UserService`  |
| `/tdd [feature]`   | 🔴🟢 Test-Driven Development   | `/tdd payment flow`  |
| `/e2e [scenario]`  | 🎭 End-to-End tests            | `/e2e checkout flow`  |
| `/ap`              | 🔬 Full 12-expert audit        | `/ap`                |
| `/review`          | 👀 Code review (5 categories)  | `/review pr #123`    |
| `/verify`          | ✔️ Build-Lint-Test loop         | `/verify`            |

### ⚙️ DevOps & Security (7 commands)

| Command          | Description                   | Example               |
| ---------------- | ----------------------------- | --------------------- |
| `/deploy`        | 🚀 Deploy to production       | `/deploy staging`     |
| `/security`      | 🔒 OWASP scan & remediation   | `/security scan`      |
| `/monitor`       | 📡 Observability setup        | `/monitor logs`       |
| `/env`           | 🔐 Environment config         | `/env scan`           |
| `/migrate`       | 🗃️ Database migrations        | `/migrate add column` |
| `/upgrade`       | 📦 Update dependencies        | `/upgrade`            |
| `/perf`          | ⚡ Performance profiling      | `/perf cpu`           |

### 🧰 Management & System (9 commands)

| Command          | Description                    | Example                  |
| ---------------- | ------------------------------ | ------------------------ |
| `/status`        | 📊 Project health              | `/status`                |
| `/doctor`        | 🩺 Environment check           | `/doctor`                |
| `/onboard`       | 📦 Project discovery            | `/onboard`               |
| `/recap`         | 📖 Session summary             | `/recap`                 |
| `/save`          | 💾 Save session state           | `/save`                  |
| `/suggest`       | ➡️ Smart next-step hints        | `/suggest`               |
| `/search`        | 🔍 Semantic search memory       | `/search auth patterns`  |
| `/doc`           | 📚 Generate documentation       | `/doc api`               |
| `/help`          | ❓ This command reference       | `/help`                  |

### 🔗 Advanced & Meta (6 commands)

| Command          | Description                        | Example                   |
| ---------------- | ---------------------------------- | ------------------------- |
| `/orchestrate`   | 🎯 Multi-agent coordination        | `/orchestrate refactor + test` |
| `/workflow`      | 🔄 Discover & chain workflows      | `/workflow list`          |
| `/skill-create`  | 🔨 Create/improve skills           | `/skill-create`           |
| `/sync-version`  | 🔄 Sync version across files       | `/sync-version`           |
| `/lang`          | 🌐 Switch language (EN ↔ VI)       | `/lang vi`                |
| `/feature`       | 🏗️ Feature lifecycle               | `/feature jwt-auth`       |

---

## 🔗 Workflow Chains

```
🆕 New Feature:    /plan → /code → /test → /review → /deploy
🐛 Bug Fix:        /debug → /fix → /test → /deploy
🔍 Quality Gate:   /ap → /refactor → /test → /review
🚀 Release:        /status → /sync-version → /test → /deploy
📦 New Team Member: /onboard → /status → /dev → /help
```

---

## 💡 Tips

- Commands auto-detect your tech stack
- Use `/help [command]` for details on any command
- `/suggest` recommends your next action based on context
- `/onboard domyh` shows DOMYH capabilities for your stack

### Having Issues?

1. `/fix` with error message (quick)
2. `/debug` for systematic diagnosis
3. `/doctor` for environment issues
4. `/status` for project health

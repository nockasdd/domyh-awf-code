---
description: "❓ Show all available commands, usage examples, and language settings"
skills: { required: [], contextual: [] }
success_criteria: "All commands listed with correct descriptions"
---

# ❓ /help — Command Reference

> 📋 See `core/COMMANDS.md` for full registry with skill requirements

---

## Quick Reference

### Development

| Command              | Description             | Example                   |
| -------------------- | ----------------------- | ------------------------- |
| `/code [task]`       | 💻 Write & fix code     | `/code add login form`    |
| `/debug [error]`     | 🐛 Systematic debugging | `/debug timeout error`    |
| `/test`              | ✅ Run & write tests    | `/test write UserService` |
| `/refactor [target]` | 🔧 Code refactoring     | `/refactor extract utils` |
| `/fix [error]`       | ⚡ Quick-fix (<60s)     | `/fix build error`        |
| `/dev`               | ▶️ Start dev server     | `/dev`                    |
| `/git [cmd]`         | 🔀 Git operations       | `/git commit`             |

### Planning & Design

| Command             | Description          | Example                |
| ------------------- | -------------------- | ---------------------- |
| `/plan [feature]`   | 📋 Feature planning  | `/plan shopping cart`  |
| `/feature [name]`   | 🏗️ Feature lifecycle | `/feature jwt-auth`    |
| `/think [topic]`    | 💡 Brainstorming     | `/think architecture`  |
| `/visualize [page]` | 🖼️ UI/UX mockups     | `/visualize dashboard` |

### Quality & Ops

| Command    | Description              | Example           |
| ---------- | ------------------------ | ----------------- |
| `/ap`      | 🔬 Full 12-expert audit  | `/ap`             |
| `/review`  | 👀 Code review           | `/review pr #123` |
| `/perf`    | ⚡ Performance profiling | `/perf cpu`       |
| `/deploy`  | 🚀 Deploy to production  | `/deploy staging` |
| `/monitor` | 📡 Observability setup   | `/monitor logs`   |

### Generation & Scaffold

| Command                   | Description              | Example                  |
| ------------------------- | ------------------------ | ------------------------ |
| `/generate [type] [name]` | 🏗️ Code generation       | `/generate api Users`    |
| `/scaffold [pattern]`     | 🏗️ From project patterns | `/scaffold crud Product` |
| `/doc`                    | 📚 Documentation         | `/doc api`               |

### Management

| Command    | Description           | Example        |
| ---------- | --------------------- | -------------- |
| `/status`  | 📊 Project health     | `/status`      |
| `/doctor`  | 🩺 Environment check  | `/doctor`      |
| `/recap`   | 📖 Session summary    | `/recap`       |
| `/upgrade` | 📦 Update deps        | `/upgrade`     |
| `/env`     | 🔐 Environment config | `/env scan`    |
| `/revert`  | ⏪ Rollback changes   | `/revert last` |

---

## 💡 Tips

- Commands auto-detect your tech stack
- Use `/help [command]` for details
- `/status` shows project health at a glance
- `/recap` summarizes your session

### Having Issues?

1. `/debug` with error message
2. `/status` for project health
3. `/recap` to see context

---

## 💾 SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`

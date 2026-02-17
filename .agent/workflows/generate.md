---
description: "🏗️ Code generation: models, APIs, components, services, and tests from templates"
skills: { required: [], contextual: [auto] }
---

# 🏗️ /generate — Alias for /scaffold

> ℹ️ **This command is an alias for `/scaffold`.**
> All generation features have been unified into `/scaffold` — Scaffold Pro.

## Usage

All `/generate` commands map directly to `/scaffold`:

| Type this...                   | Same as...                     |
| ------------------------------ | ------------------------------ |
| `/generate model User`         | `/scaffold model User`         |
| `/generate api /users`         | `/scaffold api /users`         |
| `/generate component UserCard` | `/scaffold component UserCard` |
| `/generate service Auth`       | `/scaffold service Auth`       |
| `/generate test auth.service`  | `/scaffold test auth.service`  |
| `/generate crud Product`       | `/scaffold module Product`     |
| `/generate hook useAuth`       | `/scaffold hook useAuth`       |
| `/generate page Dashboard`     | `/scaffold page Dashboard`     |
| `/generate middleware Auth`    | `/scaffold middleware Auth`    |
| `/generate dto CreateUser`     | `/scaffold dto CreateUser`     |

> 📖 See `/scaffold` for full documentation, framework templates, and convention matching.

---

## 💾 SESSION SAVE

After generation completes: update `memory/session.md` (generated files, patterns used) and `memory/state.json` (last_workflow: generate).

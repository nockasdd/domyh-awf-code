# DOMYH Awesome Code — Command Registry

> 40 active slash commands • 3-Layer Skill Resolution

---

## Core Commands (9)

| Command     | Description              | Skills Required     | Skills Contextual              |
| ----------- | ------------------------ | ------------------- | ------------------------------ |
| `/init`     | ✨ Initialize project    | —                   | [auto]                         |
| `/code`     | 💻 Write & fix code      | coding-rules        | [auto, domyh-design, tailwind] |
| `/debug`    | 🐛 Systematic debugging  | error-handling      | [auto]                         |
| `/test`     | ✅ Run and write tests   | testing             | [auto]                         |
| `/deploy`   | 🚀 Deploy to production  | ci-cd               | docker, kubernetes, aws        |
| `/refactor` | 🔧 Refactor & cleanup    | coding-rules        | [auto]                         |
| `/review`   | 👀 Code review           | security            | [auto]                         |
| `/ap`       | 🔬 Full audit (12-expert) | audit-pro           | [security, coding-rules, testing, observability, authentication] |
| `/modify`   | 🔧 Fix existing project  | coding-rules        | [auto]                         |

## Git & Fix Commands (3)

| Command   | Description           | Skills Required | Skills Contextual |
| --------- | --------------------- | --------------- | ----------------- |
| `/git`    | 🔀 Git operations hub | —               | —                 |
| `/fix`    | ⚡ Quick-fix pipeline | error-handling  | [auto]            |
| `/revert` | ⏪ Rollback changes   | —               | ci-cd             |

## Generation Commands (3)

| Command     | Description               | Skills Required | Skills Contextual |
| ----------- | ------------------------- | --------------- | ----------------- |
| `/generate` | ⚡ Code generation        | —               | [auto]            |
| `/scaffold` | 🏗️ Generate from patterns | coding-rules    | [auto]            |
| `/doc`      | 📚 Documentation          | —               | [auto]            |

## Planning & Design (6)

| Command      | Description            | Skills Required    | Skills Contextual |
| ------------ | ---------------------- | ------------------ | ----------------- |
| `/plan`      | 📋 Feature planning    | —                  | —                 |
| `/feature`   | 🏗️ Feature lifecycle   | —                  | [auto]            |
| `/think`     | 💡 Brainstorming Pro   | —                  | —                 |
| `/prompt`    | ✍️ AI prompt generator | prompt-engineering | [domyh-design]    |
| `/visualize` | 🖼️ UI/UX mockups       | domyh-design       | [auto]            |
| `/perf`      | 📈 Performance profile | web-perf           | [auto]            |

## DevOps Commands (7)

| Command      | Description                    | Skills Required        | Skills Contextual     |
| ------------ | ------------------------------ | ---------------------- | --------------------- |
| `/migrate`   | 🗄️ Database migrations         | database               | [auto]                |
| `/monitor`   | 📊 Observability setup         | observability, logging | [auto]                |
| `/env`       | 🔐 Environment management      | security               | [auto]                |
| `/upgrade`   | ⬆️ Dependency updates          | —                      | [auto]                |
| `/dev`       | ▶️ Start dev server            | —                      | [auto]                |
| `/doctor`    | 🩺 System diagnostics          | —                      | [auto]                |
| `/security`  | 🔒 Security scan & remediation | security               | [auto]                |

## Testing & Verification Commands (3)

| Command   | Description               | Skills Required       | Skills Contextual |
| --------- | ------------------------- | --------------------- | ----------------- |
| `/tdd`    | 🧪 TDD Red-Green-Refactor | tdd-workflow, testing | [auto]            |
| `/e2e`    | 🌐 E2E test generation    | testing, tdd-workflow | [auto]            |
| `/verify` | 🔄 Build-Lint-Test loop   | testing               | [auto]            |

## Utility Commands (9)

| Command        | Description                      | Skills |
| -------------- | -------------------------------- | ------ |
| `/recap`       | 📖 Session summary               | —      |
| `/status`      | 📊 Project status                | —      |
| `/help`        | ❓ Help                          | —      |
| `/workflow`    | 🔄 Workflow discovery & chaining | —      |
| `/orchestrate` | 🎭 Multi-agent coordination      | —      |
| `/onboard`     | 📦 Project onboarding guide      | —      |
| `/clean`       | 🧹 Remove dead code & imports    | —      |
| `/suggest`     | ➡️ Context-aware next steps      | —      |
| `/search`      | 🔍 Semantic search               | —      |

---

## Skill Resolution Flow

1. **L1: Deterministic (0ms)** — Load `skills.required` from workflow frontmatter
2. **L2: Contextual (<50ms)** — Detect from project files (`[auto]` = file pattern match)
3. **L3: Semantic (<200ms)** — Match user query keywords to skill META.yaml keywords
4. **L4: Skill-Internal (workflow-managed)** — Some skills (e.g. `audit-pro`) define
   `auto_load_skills` in META.yaml, mapping sub-skills per expert/phase.
   These are loaded during workflow execution, NOT at initial routing.
   → Result: Extended Skill Set (up to 14 for audit)

→ Final Result: Skill Set (max 5 from L1-L3, extended by L4 during execution)

---

# DOMYH Awesome Code — Command Registry

> 34 active slash commands • 3-Layer Skill Resolution

---

## Core Commands (9)

| Command     | Description              | Skills Required     | Skills Contextual              |
| ----------- | ------------------------ | ------------------- | ------------------------------ |
| `/init`     | ✨ Initialize project    | —                   | [auto]                         |
| `/code`     | 💻 Write & fix code      | coding-rules        | [auto, domyh-design, tailwind] |
| `/debug`    | 🐛 Systematic debugging  | error-handling      | [auto]                         |
| `/plan`     | 📋 Feature planning      | —                   | —                              |
| `/test`     | ✅ Run and write tests   | testing             | [auto]                         |
| `/deploy`   | 🚀 Deploy to production  | ci-cd               | docker, kubernetes, aws        |
| `/refactor` | 🔧 Refactor & cleanup    | coding-rules        | [auto]                         |
| `/review`   | 👀 Code review           | security            | [auto]                         |
| `/ap`       | 🔬 Full audit (5-expert) | security, audit-pro | [auto]                         |

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

## Planning & Design (4)

| Command      | Description            | Skills Required    | Skills Contextual |
| ------------ | ---------------------- | ------------------ | ----------------- |
| `/think`     | 💡 Brainstorming Pro   | —                  | —                 |
| `/prompt`    | ✍️ AI prompt generator | prompt-engineering | [domyh-design]    |
| `/visualize` | 🖼️ UI/UX mockups       | domyh-design       | —                 |
| `/perf`      | 📈 Performance profile | web-perf           | [auto]            |

## DevOps Commands (5)

| Command    | Description               | Skills Required        | Skills Contextual |
| ---------- | ------------------------- | ---------------------- | ----------------- |
| `/migrate` | 🗄️ Database migrations    | database               | [auto]            |
| `/monitor` | 📊 Observability setup    | observability, logging | [auto]            |
| `/env`     | 🔐 Environment management | security               | [auto]            |
| `/upgrade` | ⬆️ Dependency updates     | —                      | [auto]            |
| `/dev`     | ▶️ Start dev server       | —                      | [auto]            |

## Testing & Verification Commands (3)

| Command   | Description               | Skills Required       | Skills Contextual |
| --------- | ------------------------- | --------------------- | ----------------- |
| `/tdd`    | 🧪 TDD Red-Green-Refactor | tdd-workflow, testing | [auto]            |
| `/e2e`    | 🌐 E2E test generation    | testing, tdd-workflow | [auto]            |
| `/verify` | 🔄 Build-Lint-Test loop   | testing               | [auto]            |

## Utility Commands (5)

| Command        | Description                      | Skills |
| -------------- | -------------------------------- | ------ |
| `/recap`       | 📖 Session summary               | —      |
| `/status`      | 📊 Project status                | —      |
| `/help`        | ❓ Help                          | —      |
| `/workflow`    | 🔄 Workflow discovery & chaining | —      |
| `/orchestrate` | 🎭 Multi-agent coordination      | —      |

---

## Skill Resolution Flow

```
User: /command [args]
    │
    ▼
┌─────────────────────────────────┐
│ L1: Deterministic (0ms)         │
│ → Load skills.required from     │
│   manifest/frontmatter          │
├─────────────────────────────────┤
│ L2: Contextual (<50ms)          │
│ → Detect from project files     │
│ → [auto] = file pattern match   │
├─────────────────────────────────┤
│ L3: Semantic (<200ms)           │
│ → Match user query keywords     │
│ → to skill META.yaml keywords   │
└─────────────────────────────────┘
    │
    ▼
  Skill Set (max 5)
```

---

_DOMYH Awesome Code • 3-Layer Skill Resolution_

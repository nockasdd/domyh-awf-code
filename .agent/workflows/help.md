---
name: help
trigger: ["/help", "?", "commands", "trợ giúp", "hướng dẫn"]
persona: assistant
description: "❓ Show all available commands, usage examples, and language settings"
---

# ❓ /help — DOMYH Awesome Code Command Reference

> Your AI-Powered Development Assistant
> 📚 25+ Commands • Multi-language • Context-aware

---

## 🚀 QUICK START

```bash
# Most common workflows:
/plan [feature]   # Start planning a new feature
/code [task]      # Write production code
/debug [error]    # Fix bugs systematically
/test             # Run and write tests
/deploy           # Deploy to production
```

---

## 📋 COMMAND REFERENCE

### 🔬 Core Development

| Command              | Description             | Example                         |
| -------------------- | ----------------------- | ------------------------------- |
| `/code [task]`       | 💻 Write quality code   | `/code add user authentication` |
| `/debug [error]`     | 🐛 Systematic debugging | `/debug login fails with 401`   |
| `/test`              | ✅ Run and write tests  | `/test user.service.ts`         |
| `/refactor [target]` | 🔧 Code refactoring     | `/refactor extract utils`       |

### 📋 Planning & Design

| Command              | Description            | Example                        |
| -------------------- | ---------------------- | ------------------------------ |
| `/plan [feature]`    | 📋 Feature planning    | `/plan shopping cart`          |
| `/design [system]`   | 🎨 Technical design    | `/design payment flow`         |
| `/brainstorm [idea]` | 💡 Ideation & research | `/brainstorm caching strategy` |
| `/visualize [ui]`    | 🖼️ UI/UX mockup        | `/visualize dashboard`         |

### 🔍 Audit & Review

| Command          | Description           | Example                   |
| ---------------- | --------------------- | ------------------------- |
| `/ap`            | 🔬 Full project audit | `/ap backend`             |
| `/review [file]` | 👀 Code review        | `/review auth.service.ts` |
| `/audit`         | 🏥 Security audit     | `/audit`                  |

### 🛠️ DevOps & Infrastructure

| Command         | Description               | Example                 |
| --------------- | ------------------------- | ----------------------- |
| `/deploy [env]` | 🚀 Deploy to environment  | `/deploy staging`       |
| `/env`          | 🔐 Environment management | `/env validate`         |
| `/migrate`      | 🗃️ Database migrations    | `/migrate create users` |
| `/monitor`      | 📡 Setup observability    | `/monitor`              |

### 🏗️ Code Generation

| Command                   | Description               | Example                  |
| ------------------------- | ------------------------- | ------------------------ |
| `/generate [type] [name]` | 🏗️ Generate code          | `/generate crud Product` |
| `/init [type]`            | ✨ Initialize project     | `/init nextjs`           |
| `/doc [type]`             | 📝 Generate documentation | `/doc api`               |

### 🧹 Maintenance

| Command    | Description            | Example       |
| ---------- | ---------------------- | ------------- |
| `/clean`   | 🧹 Code cleanup        | `/clean dead` |
| `/upgrade` | 📦 Update dependencies | `/upgrade`    |

### 📊 Status & Navigation

| Command   | Description            | Example      |
| --------- | ---------------------- | ------------ |
| `/status` | 📊 Project health      | `/status`    |
| `/recap`  | 📖 Session summary     | `/recap`     |
| `/next`   | ➡️ Suggested next step | `/next`      |
| `/help`   | ❓ This help           | `/help code` |

---

## 🎯 COMMAND DETAILS

### `/code` — Write Production Code

```bash
# Basic usage
/code [description of what to build]

# Examples
/code add login form with validation
/code implement pagination for users API
/code fix the responsive layout on mobile

# With context
/code (while viewing file) improve this function
```

**What it does:**

1. Understands your request
2. Plans the implementation
3. Writes quality code with error handling
4. Adds tests if appropriate
5. Verifies the build

---

### `/debug` — Systematic Debugging

```bash
# Basic usage
/debug [error message or description]

# Examples
/debug TypeError: Cannot read property 'id' of undefined
/debug login always returns 401
/debug memory leak in production

# With trace
/debug --trace (verbose logging)
/debug --bisect (git bisect helper)
```

**6-Step Process:**

```
CAPTURE → REPRODUCE → ISOLATE → ANALYZE → FIX → VERIFY
```

---

### `/plan` — Feature Planning

```bash
# Basic usage
/plan [feature description]

# Examples
/plan user notifications system
/plan multi-tenancy support
/plan API rate limiting

# Output includes:
# - Requirements breakdown
# - Technical approach
# - Task list with estimates
# - Risk assessment
```

---

### `/deploy` — Production Deployment

```bash
# Basic usage
/deploy [environment]

# Examples
/deploy staging
/deploy production
/deploy --dry    # Preview only
/deploy --canary # Gradual rollout

# Pre-checks:
# ✅ Tests pass
# ✅ Code reviewed
# ✅ No P0 issues
# ✅ Rollback plan ready
```

---

### `/generate` — Code Generation

```bash
# Generate different types
/generate model User              # Model + Repository
/generate crud Product            # Full CRUD stack
/generate component Button        # React component
/generate api Orders              # API endpoints
/generate test user.service.ts    # Tests for file

# Output example for CRUD:
# ├── product.model.ts
# ├── product.service.ts
# ├── product.controller.ts
# ├── product.dto.ts
# └── product.test.ts
```

---

### `/ap` — Full Project Audit

```bash
# Basic usage
/ap [scope]

# Examples
/ap                    # Full audit
/ap backend            # Backend only
/ap frontend           # Frontend only
/ap security           # Security focus

# 5 Expert Panels:
# 🔒 Security (CWE/OWASP)
# 🏗️ Architecture (SOLID, patterns)
# ⚡ Performance (N+1, memory)
# 🧪 Quality (tests, docs)
# 🚀 DevOps (CI/CD, logging)
```

---

## 🌐 SUPPORTED STACKS

### Languages

| Backend | Frontend | Mobile       | Data   |
| ------- | -------- | ------------ | ------ |
| Go      | React    | Swift        | Python |
| Rust    | Vue      | Kotlin       | R      |
| Java    | Svelte   | Dart         | Julia  |
| Kotlin  | Angular  | React Native | SQL    |
| C#      | Next.js  | Flutter      |        |
| Python  | Nuxt     |              |        |
| Ruby    |          |              |        |
| PHP     |          |              |        |

### Frameworks

| Backend | Frontend  | Infrastructure |
| ------- | --------- | -------------- |
| Express | Next.js   | Docker         |
| NestJS  | Nuxt      | Kubernetes     |
| FastAPI | Remix     | Terraform      |
| Spring  | Vite      | AWS CDK        |
| Rails   | Astro     | Pulumi         |
| Laravel | SvelteKit |                |

---

## ⚙️ SETTINGS

### Language Switch

```bash
/lang vi    # Tiếng Việt
/lang en    # English
```

### Customize Behavior

```bash
/customize  # Open customization menu
```

Options:

- 🎯 Technical level (newbie → expert)
- 📝 Documentation style
- ⚡ Token optimization level
- 🔔 Confirmation preferences

---

## 💡 TIPS & TRICKS

### Be Specific

```bash
# ❌ Too vague
/code make it better

# ✅ Specific
/code add input validation to SignupForm with email and password rules
```

### Chain Commands

```bash
# Plan → Code → Test workflow
/plan user profile feature
/code (after reviewing plan)
/test
```

### Use Context

```bash
# While viewing a file:
/debug   # Debugs the current file
/test    # Generates tests for current file
/doc     # Documents current file
```

### Get Suggestions

```bash
/next    # What should I do next?
/recap   # What have we done?
/status  # How healthy is the project?
```

---

## 🆘 GETTING HELP

### For Specific Commands

```bash
/help code      # Details about /code
/help deploy    # Details about /deploy
```

### Having Issues?

1. Try `/debug` with error message
2. Use `/recap` to see context
3. Check `/status` for project health
4. Ask: "Why is X not working?"

### Feedback

Report issues or suggestions:

- GitHub: [repo-url]
- Discord: [discord-url]

---

## 📊 QUICK REFERENCE CARD

```
┌─────────────────────────────────────────────┐
│           DOMYH Awesome Code v5.5 Quick Ref        │
├─────────────────────────────────────────────┤
│ 💻 /code [task]    Write code               │
│ 🐛 /debug [error]  Fix bugs                 │
│ ✅ /test           Run tests                │
│ 📋 /plan [feat]    Plan feature             │
│ 🚀 /deploy [env]   Deploy                   │
│ 🔬 /ap             Full audit               │
│ 🏗️ /generate       Scaffold code           │
│ 🧹 /clean          Cleanup                  │
│ 📝 /doc            Documentation            │
│ ❓ /help           This help                │
├─────────────────────────────────────────────┤
│ 🌐 /lang vi|en     Switch language          │
│ 📊 /status         Project health           │
│ ➡️ /next           Suggested action         │
└─────────────────────────────────────────────┘
```

---

## 🤖 CONTEXT-AWARE HELP (v2.1)

```yaml
context_aware_help:
  description: "Smart suggestions based on your context"

  analyze:
    current_file: "What you're editing"
    recent_commands: "Workflow history"
    project_type: "Detected tech stack"
    errors: "Recent error messages"

  suggestions:
    proactive:
      description: "Anticipate your needs"
      examples:
        - "Editing test file → suggest /test"
        - "After /code → suggest /test or /debug"
        - "Error in terminal → suggest /debug"

    reactive:
      description: "Based on your questions"
      examples:
        - "'How do I...' → relevant command"
        - "'Why is...' → /debug suggestion"

  learning:
    user_patterns: "Remember preferences"
    success_rate: "Track what works"
    personalization: "Adapt to workflow"

  commands:
    smart: "/help smart"
    context: "/help context"
```

---

## 💡 SMART SUGGESTIONS (v2.1)

```yaml
smart_suggestions:
  description: "AI-powered next action recommendations"

  triggers:
    after_command:
      /code: ["test", "commit", "review"]
      /debug: ["test", "deploy"]
      /test: ["commit", "deploy"]
      /deploy: ["monitor", "rollback"]

    on_error:
      build_fail: "/debug with error"
      test_fail: "/debug failing test"
      lint_error: "/clean or /code fix"

    on_file_change:
      new_feature: "/test generate"
      config_change: "/env validate"

  commands:
    next: "/next"
    suggest: "/help suggest"
```

---

_DOMYH Awesome Code v5.5 • Help Pro v2.1 • Context-Aware + Smart Suggestions_

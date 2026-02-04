---
name: suggest
trigger: ["/suggest", "what next", "tiếp theo"]
persona: assistant
description: "➡️ Smart suggestions: context-aware next steps based on project state"
---

# ➡️ /suggest — Suggest Pro v3.1

> Context-Aware Next Steps
> 📚 Auto-detect • Prioritized • Actionable

---

## 🔄 SUGGEST FLOW

```
User: /suggest
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: ANALYZE CONTEXT                │
│ ▸ Recent activity                       │
│ ▸ Project state                         │
│ ▸ Pending tasks                         │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: GENERATE OPTIONS               │
│ ▸ Based on workflow stage               │
│ ▸ Prioritize by impact                  │
│ ▸ Consider dependencies                 │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: PRESENT                        │
│ ▸ Show top 5 suggestions                │
│ ▸ Explain rationale                     │
│ ▸ Quick action commands                 │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command           | Description       |
| ----------------- | ----------------- |
| `/suggest`        | Smart suggestions |
| `/suggest code`   | Code-focused next |
| `/suggest test`   | Testing next      |
| `/suggest deploy` | Deployment next   |

---

## 📊 SUGGESTION OUTPUT

```markdown
➡️ SMART SUGGESTIONS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Based on: Recent /code session + pending tests

## Context

| Factor       | Status            |
| ------------ | ----------------- |
| Last command | /code UserService |
| Tests        | 3 failing         |
| Coverage     | 72%               |
| Lint         | 5 warnings        |

## Top Suggestions

### 1️⃣ Fix Failing Tests (Recommended)

Priority: 🔴 High
Rationale: 3 tests broken after code changes
Command: `/test fix`

### 2️⃣ Improve Coverage

Priority: 🟠 Medium  
Rationale: Coverage dropped below 80% target
Command: `/test coverage`

### 3️⃣ Fix Lint Warnings

Priority: 🟡 Low
Rationale: 5 new warnings introduced
Command: `/clean lint`

### 4️⃣ Commit Changes

Priority: 🟡 Low
Rationale: 12 files modified, not committed
Command: `git commit`

### 5️⃣ Update Dependencies

Priority: 🔵 Optional
Rationale: 3 patch updates available
Command: `/upgrade patch`

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Quick: Enter 1-5 to run suggestion
```

---

## 🔧 CONTEXT DETECTION

````yaml
context_triggers:
  # After coding
  post_code:
    check: [tests, lint, coverage]
    suggest:
      - "Run tests"
      - "Check lint"
      - "Commit changes"

  # After testing
  post_test:
    if_pass:
      - "Commit and push"
      - "Create PR"
      - "Deploy to staging"
    if_fail:
      - "Fix failing tests"
      - "Debug errors"

  # After deploy
  post_deploy:
    check: [logs, metrics, errors]
    suggest:
      - "Monitor logs"
      - "Check health"
      - "Run smoke tests"

  # Project state
  project_checks:
    outdated_deps:
      - "Update dependencies"
    low_coverage:
      - "Write more tests"
    many_todos:
      - "Address TODOs"
    stale_branch:
      - "Merge or delete"
---

## 📝 GIT PREREQUISITE CHECK

```yaml
git_checks:
  before_deploy:
    # Check git status before suggesting deploy
    conditions:
      - check: ".git/ exists"
        fail_action: "Suggest: git init first"

      - check: "remote origin configured"
        fail_action: "Suggest: git remote add origin <url>"

      - check: "uncommitted changes"
        fail_action: "Suggest: git add . && git commit -m 'message'"

  example_output:
    no_git: |
      ⚠️ Git not initialized

      Before deploy, run:
      ```
      git init
      git remote add origin <your-repo-url>
      git add . && git commit -m "Initial commit"
      ```

      Command: git init
````

---

## 📋 WORKFLOW TRANSITIONS

```yaml
transitions:
  init: [plan, code]
  plan: [code, design]
  code: [test, review]
  test: [deploy, refactor] # deploy requires git check
  deploy: [monitor, recap]
  debug: [code, test]
  review: [refactor, merge]

guards:
  deploy:
    requires: [git_initialized, tests_pass, no_uncommitted]
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Auto-detect context
  - Top 5 only
  - One-line rationales
  - Cache git status
```

---

_DOMYH Awesome Code v6.1.2 • Suggest Pro v3.1 • Git-Aware Suggestions_

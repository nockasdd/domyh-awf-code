---
description: "➡️ Smart suggestions: context-aware next steps based on project state"
skills: { required: [], contextual: [auto] }
success_criteria: "Top suggestions presented with rationale and commands"
---

# ➡️ /suggest — Smart Suggestions Pro v3.0

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
  init: [env, dev, scaffold]
  plan: [code, scaffold]
  scaffold: [code]
  code: [test, review]
  test_pass: [git_commit, deploy]
  test_fail: [fix, debug]
  fix: [test, git_commit]
  deploy: [monitor, status]
  debug: [fix, test]
  review: [refactor, code_fix]
  refactor: [test, clean]
  ap: [refactor, fix]
  security: [fix, ap]
  security_pass: [deploy]
  migrate: [test, deploy]
  onboard: [plan, code, suggest]
  visualize: [scaffold, code]
  modify: [test, review]
  feature: [test, deploy]
  tdd: [code, test]
  orchestrate: [recap, deploy, test, verify]
  orchestrate_partial: [debug, fix, orchestrate_resume]

guards:
  deploy:
    requires: [git_initialized, tests_pass, no_uncommitted]
  revert:
    requires: [git_initialized, backup_created]
  upgrade_major:
    requires: [tests_pass, changelog_reviewed]
  migrate:
    requires: [backup_exists, tests_pass]
  security_fix:
    requires: [scan_completed, findings_reviewed]
  orchestrate:
    requires: [complexity_scored, dag_approved]
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

_DOMYH Awesome Code v6.4.3 • Suggest Pro v3.1 • Git-Aware Suggestions_

---

## REFLECTION CHECKPOINT

> Before saving session, verify: suggestions context-relevant? Git state checked? Recommended commands valid?

---

## 💾 SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`

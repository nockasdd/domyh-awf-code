---
name: clean
trigger: ["/clean", "cleanup", "dead code", "organize"]
persona: developer
description: "🧹 Code cleanup: remove dead code, organize imports, remove unused dependencies"
success_criteria: "Dead code removed, imports organized, build passes"
---

# 🧹 /clean — Code Cleanup Pro v2.0

> Intelligent code hygiene with safety gates
> 📚 Auto-detect stack, preview before changes

---

## 🔄 CLEANUP FLOW

```
User: /clean [option]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: DETECT (Auto - 5s)            │
│ ▸ Identify tech stack                   │
│ ▸ Find relevant tools                   │
│ ▸ Check tool availability               │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: SCAN (Auto - 30s)             │
│ ▸ Run analysis tools                    │
│ ▸ Collect dead code locations           │
│ ▸ Identify unused deps/imports          │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: PREVIEW                        │
│ ▸ Show what will be removed             │
│ ⛔ STOP - WAIT FOR USER CONFIRMATION    │
└─────────────────────────────────────────┘
    │ User: "y" or "1,3,5" (selective)
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: EXECUTE (With Backup)          │
│ ▸ Create backup (optional)              │
│ ▸ Apply selected changes                │
│ ▸ Run formatters                        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 5: VERIFY                         │
│ ▸ Run build to confirm no breaks        │
│ ▸ Show summary of changes               │
│ ▸ Offer rollback if issues              │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command                | Action                       | Risk Level |
| ---------------------- | ---------------------------- | ---------- |
| `/clean`               | Full analysis (preview only) | 🟢 Safe    |
| `/clean dead`          | Remove dead code             | 🟡 Medium  |
| `/clean imports`       | Organize imports             | 🟢 Safe    |
| `/clean deps`          | Remove unused dependencies   | 🟡 Medium  |
| `/clean cache`         | Clear build/test cache       | 🟢 Safe    |
| `/clean memory`        | Preview agent memory files   | 🟢 Safe    |
| `/clean memory reset`  | Reset memory (keep audit)    | 🟠 High    |
| `/clean memory audit`  | Reset audit logs only        | 🟡 Medium  |
| `/clean memory --hard` | Delete all memory            | 🔴 Danger  |
| `/clean all`           | Apply all fixes              | 🟠 High    |
| `/clean --dry`         | Preview without changes      | 🟢 Safe    |

---

## 📋 PHASE 1: DETECT

### Stack Detection (30+ Languages)

> Tool configs loaded from `workflows/data/clean-tools.yaml`
> Agent selects cleanup tools based on `hsa_detect_stack` result
> Schema per language: `markers`, `dead_code`, `imports`, `deps`, `format`, `lint`

### Output:

```
🔍 STACK DETECTED

Project: Monorepo (Multi-language)
├── Backend: ./backend
│   ├── Go (API Server)
│   ├── Python (ML Service)
│   └── Rust (Performance Module)
├── Frontend: ./frontend
│   ├── TypeScript (React)
│   └── Vue (Admin Panel)
├── Mobile: ./mobile
│   ├── Swift (iOS)
│   └── Kotlin (Android)
└── Infra: ./infra
    ├── Terraform
    └── Docker

Tools loaded: 12 languages detected
Scanning...
```

---

## 📋 PHASE 2: SCAN

### Analysis Commands by Stack:

**Go:**

```bash
# Dead code detection
go install golang.org/x/tools/cmd/deadcode@latest
deadcode ./...

# Unused imports (preview)
goimports -l .

# Unused dependencies
go mod tidy -v
```

**Node.js/TypeScript:**

```bash
# Dead exports
npx ts-prune

# Unused dependencies
npx depcheck

# Organize imports (preview)
npx organize-imports-cli --check
```

**Python:**

```bash
# Dead code
vulture .

# Organize imports
isort --check-only .

# Unused deps
pip-autoremove --list
```

---

## 📋 PHASE 3: PREVIEW

### Report Format:

```
🧹 CLEANUP REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 DEAD CODE (5 items)

| # | File | Line | Type | Code |
|---|------|------|------|------|
| 1 | auth/helper.go | 45 | func | `unusedValidator()` |
| 2 | auth/helper.go | 89 | func | `deprecatedCheck()` |
| 3 | utils/string.go | 12 | var | `oldPrefix` |
| 4 | handlers/user.go | 156 | func | `legacyHandler()` |
| 5 | models/temp.go | 1-50 | file | Entire file unused |

📦 UNUSED DEPENDENCIES (3 items)

| # | Package | Last Imported | Size |
|---|---------|---------------|------|
| 6 | github.com/old/lib | Never | 2.1MB |
| 7 | lodash | Never | 1.5MB |
| 8 | moment | Never | 0.8MB |

📥 UNUSED IMPORTS (12 files)

| # | File | Count | Imports |
|---|------|-------|---------|
| 9 | handlers/order.go | 3 | fmt, strings, time |
| 10| services/cache.go | 2 | context, sync |
| ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total: 5 dead code + 3 deps + 12 import files

⛔ SELECT ACTION:
  [y] Apply all
  [n] Cancel
  [1,2,6] Apply selected items only
  [--backup] Create backup first

Enter choice:
```

---

## 📋 PHASE 4: EXECUTE

### Execution Steps:

```yaml
step_4.1:
  action: "Create backup (if requested)"
  command: "git stash push -m 'Pre-cleanup backup'"

step_4.2:
  action: "Remove dead code"
  method: "Delete selected lines/files"
  verify: "Syntax check after each removal"

step_4.3:
  action: "Remove unused dependencies"
  commands:
    go: "go mod tidy"
    node: "npm uninstall {package}"
    python: "pip uninstall {package}"

step_4.4:
  action: "Organize imports"
  commands:
    go: "goimports -w ."
    node: "npx organize-imports-cli ."
    python: "isort ."

step_4.5:
  action: "Format code"
  commands:
    go: "gofmt -w ."
    node: "npx prettier --write ."
    python: "black ."
```

### Progress Output:

```
🔄 APPLYING CHANGES

[1/5] Removing dead code...
  ✅ auth/helper.go:45 (unusedValidator)
  ✅ auth/helper.go:89 (deprecatedCheck)
  ✅ utils/string.go:12 (oldPrefix)
  ✅ handlers/user.go:156 (legacyHandler)
  ✅ models/temp.go (deleted file)

[2/5] Removing unused dependencies...
  ✅ github.com/old/lib (2.1MB freed)
  ✅ lodash (1.5MB freed)
  ✅ moment (0.8MB freed)

[3/5] Organizing imports...
  ✅ 12 files updated

[4/5] Formatting code...
  ✅ 45 files formatted

[5/5] Running build verification...
  ⏳ go build ./...
```

---

## 📋 PHASE 5: VERIFY

### Verification Steps:

```yaml
verify_steps:
  - name: "Build check"
    commands:
      go: "go build ./..."
      node: "npm run build"
      python: "python -m py_compile *.py"

  - name: "Test check"
    commands:
      go: "go test ./... -short"
      node: "npm test -- --passWithNoTests"

  - name: "Lint check"
    commands:
      go: "golangci-lint run"
      node: "npm run lint"
```

### Final Report:

```
✅ CLEANUP COMPLETE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

SUMMARY:
├── Dead code removed: 5 items
├── Dependencies removed: 3 packages (4.4MB freed)
├── Imports organized: 12 files
├── Files formatted: 45 files
└── Build status: ✅ SUCCESS

VERIFICATION:
├── Build: ✅ Passed
├── Tests: ✅ 156/156 passed
└── Lint: ✅ No issues

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 NEXT STEPS:
1️⃣ Review changes: git diff
2️⃣ Commit: git commit -am "chore: code cleanup"
3️⃣ If issues: git stash pop (restore backup)

Enter number or command:
```

---

## ⚠️ SAFETY RULES

### Always Applied:

```yaml
safety:
  - Preview changes before any deletion
  - Show exact lines before removal
  - Offer backup option
  - Run build after changes
  - Provide rollback instructions
```

### Protected Patterns:

```yaml
protected_patterns:
  - Functions with "deprecated" comment (may be intentional)
  - Files with TODO markers
  - Test files (*_test.go, *.test.ts)
  - Config files (*.config.*, *.yaml)
  - Migration files
```

---

## 🔧 TOOL INSTALLATION

### First-time Setup:

**Go:**

```bash
go install golang.org/x/tools/cmd/deadcode@latest
go install golang.org/x/tools/cmd/goimports@latest
```

**Node.js:**

```bash
npm install -g ts-prune depcheck organize-imports-cli
```

**Python:**

```bash
pip install vulture isort black pip-autoremove
```

---

## 📜 RULES APPLIED

| Phase   | Rules                                  |
| ------- | -------------------------------------- |
| Detect  | `terminal-safety`                      |
| Scan    | `context-management`                   |
| Preview | `stop-conditions`, `edit-verification` |
| Execute | `safety`, `edit-verification`          |
| Verify  | `terminal-safety`, `evidence`          |

---

## 🔍 DEAD CODE DETECTION (v2.1)

```yaml
dead_code_detection:
  description: "Find and remove unused code safely"

  tools:
    javascript_ts:
      - "ts-prune"
      - "knip"
      - "depcheck"
    go:
      - "deadcode"
      - "unused"
    python:
      - "vulture"
      - "autoflake"
    rust:
      - "cargo-udeps"

  detection:
    unused_exports: "Exported but never imported"
    unused_functions: "Defined but never called"
    unused_variables: "Declared but never used"
    unused_imports: "Imported but never used"
    unreachable_code: "After return/throw"

  safe_mode:
    preview: "Show before delete"
    backup: "Create .backup before cleanup"
    git_safety: "Require clean working tree"
    one_at_a_time: "Process incrementally"

  commands:
    preview: "/clean dead preview"
    execute: "/clean dead execute"
    report: "/clean dead report"
```

---

## 📦 DEPENDENCY PRUNING (v2.1)

```yaml
dependency_pruning:
  description: "Remove unused and problematic dependencies"

  analysis:
    unused:
      description: "Not imported anywhere"
      tools: ["depcheck", "knip"]

    duplicate:
      description: "Multiple versions of same package"
      tools: ["npm dedupe", "yarn dedupe"]

    outdated:
      description: "Security vulnerabilities"
      tools: ["npm audit", "snyk"]

    bloat:
      description: "Large unused transitive deps"
      tools: ["bundle-analyzer", "source-map-explorer"]

  actions:
    remove_unused: true
    deduplicate: true
    upgrade_vulnerable: true
    replace_deprecated: true

  validation:
    build_after: true
    test_after: true
    size_comparison: true

  commands:
    analyze: "/clean deps analyze"
    prune: "/clean deps prune"
    audit: "/clean deps audit"
```

---

## 🧠 MEMORY CLEANUP (v2.2)

> Agent memory management - only runs when explicitly requested with `memory` keyword

```yaml
memory_cleanup:
  description: "Clean agent memory files"
  trigger: "/clean memory" # ONLY runs when user includes "memory" keyword

  files:
    # Session files (safe to reset)
    session:
      - memory/session.md
      - memory/consolidated.md
      - memory/insights.md
      - memory/active_memories.json
      - memory/cleanup_log.json

    # State files (contains project context)
    state:
      - memory/state.json
      - memory/metrics.json
      - memory/decisions.md

    # Audit history (important records)
    audit:
      - memory/audit_summary.json
      - memory/archive/*

  commands:
    preview: "/clean memory" # Safe - shows file sizes only
    reset: "/clean memory reset" # Resets session + state, keeps audit
    audit: "/clean memory audit" # Resets audit logs only
    hard: "/clean memory --hard" # ⚠️ Deletes everything

  safety:
    require_confirmation: true
    show_preview_first: true
    backup_before_delete: true
    require_manual_trigger: true
```

### Preview Format:

```
🧠 MEMORY STATUS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📁 SESSION FILES (safe to reset)
├── session.md           1.1 KB
├── consolidated.md      1.2 KB
├── insights.md          0.9 KB
├── active_memories.json 0.9 KB
└── cleanup_log.json     0.7 KB
    Subtotal: 4.8 KB

📁 STATE FILES (project context)
├── state.json           1.4 KB
├── metrics.json         0.8 KB
└── decisions.md         1.1 KB
    Subtotal: 3.3 KB

📁 AUDIT FILES (important records)
├── audit_summary.json   1.1 KB
└── archive/             (2 files)
    Subtotal: 1.5 KB

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Total: 9.6 KB

⛔ SELECT ACTION:
  [1] Reset session files only (4.8 KB)
  [2] Reset session + state (8.1 KB)
  [3] Reset audit logs only (1.5 KB)
  [4] Reset all (--hard) ⚠️ IRREVERSIBLE
  [n] Cancel

Enter choice:
```

### Reset Templates:

```yaml
# Session reset - creates fresh session files
session_reset:
  session.md: |
    # 📝 Session Notes
    Reset: {timestamp}

  consolidated.md: |
    # 🧠 Consolidated Memories
    Last reset: {timestamp}

  active_memories.json: |
    {
      "version": "1.0.0",
      "last_reset": "{timestamp}",
      "memories": []
    }

# State reset - keeps structure, clears data
state_reset:
  state.json: |
    {
      "version": "1.1.0",
      "last_updated": "{timestamp}",
      "project": null,
      "last_audit": null,
      "pending_tasks": []
    }

  metrics.json: |
    {
      "version": "1.0.0",
      "last_reset": "{timestamp}",
      "sessions": 0,
      "commands_executed": 0
    }

# Audit reset - preserves structure for new audits
audit_reset:
  audit_summary.json: |
    {
      "version": "1.1.0",
      "last_updated": "{timestamp}",
      "summary": {
        "total_audits": 0,
        "overall_score": null
      },
      "history": []
    }
```

---

## 🔧 SUB-COMMANDS (Updated)

| Command                | Description           |
| ---------------------- | --------------------- |
| `/clean`               | Full code cleanup     |
| `/clean dead preview`  | Preview dead code     |
| `/clean dead execute`  | Remove dead code      |
| `/clean deps analyze`  | Analyze dependencies  |
| `/clean deps prune`    | Remove unused deps    |
| `/clean imports`       | Organize imports      |
| `/clean memory`        | Preview memory files  |
| `/clean memory reset`  | Reset session + state |
| `/clean memory audit`  | Reset audit logs      |
| `/clean memory --hard` | Delete all memory ⚠️  |
| `/clean --safe`        | Extra safe mode       |

---

_DOMYH Awesome Code v6.3.2 • Clean Pro v2.2 • Dead Code + Dependency + Memory Cleanup_
---

## 💾 SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` — what changed, current status
2. Append summary to `memory/session.md`

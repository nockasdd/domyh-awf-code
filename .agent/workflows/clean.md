---
description: "🧹 Code cleanup: remove dead code, organize imports, remove unused dependencies"
skills: { required: [coding-rules], contextual: [auto] }
success_criteria: "Dead code removed, imports organized, build passes"
---

# 🧹 /clean — Code Cleanup Pro v2.0

> Intelligent code hygiene with safety gates
> 📚 Auto-detect stack, preview before changes

---

## 🔄 CLEANUP FLOW

1. **PHASE 1: DETECT (Auto - 5s)** — `hsa_declare_intent`, `hsa_detect_stack`, identifying tools.
2. **PHASE 2: SCAN (Auto - 30s)** — Run analysis tools. Collect dead code / unused deps.
3. **PHASE 3: PREVIEW** — Show proposed removals. ⛔ **STOP - WAIT FOR USER CONFIRMATION**.
4. **PHASE 4: EXECUTE** — Create backup (optional), apply selected changes, format.
5. **PHASE 5: VERIFY** — Run build/tests, show summary, offer rollback.
6. **PHASE 6: SYNC** — `hsa_check_changes` to update index.

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

> Output concisely: Project name, Stack, and Tools loaded.

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

> Present a concise table of dead code, unused dependencies, and imports. 
> Then prompt: ⛔ SELECT ACTION: [y] Apply all, [1,2,6] Selective items, [--backup] Backup first, [n] Cancel.

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

> Output progress incrementally as steps complete (e.g., `Removing dead code... ✅ auth/helper.go:45`).

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

> Show a concise summary of freed resources, updated files, and verification results (Build/Tests/Lint).
> Provide NEXT STEPS (e.g., review git diff, commit).

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
| Scan    | `perf-001`                             |
| Preview | `stop-conditions`, `edit-verification` |
| Execute | `safety`, `edit-verification`          |
| Verify  | `terminal-safety`, `exec-001`          |

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

> Show file sizes for Session, State, and Audit files. Prompt for reset level [1-4] or cancel.

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

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** — Update session memory:
   - Append task summary to `memory/session.md` (per SESSION_005 format)
   - If key decision made → append to `memory/decisions.md`
3. **SNAPSHOT** — If this is the last task in session:
   - Update `memory/CONTEXT_SNAPSHOT.md` (Recent Changes, Status, Decisions)
4. **ANCHOR** (if HSA available):
   - `hsa_track_progress(level: "action", label: "[workflow] completed", status: "completed")`
   - `hsa_save_anchor(content: "[SESSION] Done: [summary]. Files: [list].", category: "context")`


---
name: save
trigger: ["/save", "lưu", "persist", "save session"]
persona: Developer
description: "💾 Save current session state to memory files"
---

# 💾 /save — Session Memory Persistence

> Save session context to persistent memory files
> 📁 Files: session.md, state.json, decisions.md

---

## 🔄 SAVE FLOW

```
User: /save [scope]
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: COLLECT                        │
│ ▸ Gather session context                │
│ ▸ Identify changes since last save      │
│ ▸ Check memory file status              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: WRITE                          │
│ ▸ Update memory/session.md              │
│ ▸ Update memory/state.json              │
│ ▸ Append to memory/decisions.md         │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: CONFIRM                        │
│ ▸ Show files updated                    │
│ ▸ Show summary of changes               │
└─────────────────────────────────────────┘
```

---

## 📋 SAVE TARGETS

| Target        | File                        | Content                          |
| ------------- | --------------------------- | -------------------------------- |
| **session**   | `memory/session.md`         | Workflows executed, current task |
| **state**     | `memory/state.json`         | Flags, preferences, scores       |
| **decisions** | `memory/decisions.md`       | Key decisions made               |
| **audit**     | `memory/audit_summary.json` | Audit history                    |

---

## 🔧 SUB-COMMANDS

| Command           | Scope              | Description             |
| ----------------- | ------------------ | ----------------------- |
| `/save`           | All                | Save all memory files   |
| `/save session`   | session.md         | Save session notes only |
| `/save state`     | state.json         | Save project state only |
| `/save decisions` | decisions.md       | Save decisions only     |
| `/save audit`     | audit_summary.json | Save audit results      |

---

## 📊 OUTPUT FORMAT

```
💾 SAVE COMPLETE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Updated Files:
├── ✅ memory/session.md (+15 lines)
├── ✅ memory/state.json (2 fields)
└── ✅ memory/decisions.md (+1 decision)

Summary:
• Session: Recorded 3 workflows, 1 active task
• State: Updated audit score to 8.8
• Decisions: Added 1 new decision

Last saved: 2026-02-01 22:36
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## 🔄 AUTO-TRIGGER POINTS

These workflows automatically trigger save:

| Workflow  | Trigger               | Scope            |
| --------- | --------------------- | ---------------- |
| `/ap`     | After audit complete  | audit, state     |
| `/deploy` | After deployment      | state, decisions |
| `/recap`  | After session summary | session, state   |
| `/init`   | After project init    | all              |

---

## 📝 SESSION.MD TEMPLATE

```markdown
## Current Session

- **Started**: {auto}
- **Last Save**: {auto}

### Workflows Executed

| Time | Workflow | Status |
| ---- | -------- | ------ |
| ...  | ...      | ...    |

### Active Task

> {current task description}

### Notes

> {agent notes}
```

---

## 📁 STATE.JSON UPDATES

```json
{
  "last_updated": "{timestamp}",
  "workflows": {
    "last_executed": "{workflow}",
    "execution_count": { ... }
  },
  "audit": {
    "last_score": "{score}",
    "last_date": "{date}"
  },
  "context": {
    "current_phase": "{phase}",
    "pending_tasks": [ ... ]
  },
  "memory": {
    "last_sync": "{timestamp}"
  }
}
```

---

## 💡 USAGE EXAMPLES

```bash
# Save everything after a work session
/save

# Save only session notes
/save session

# Save after completing audit
/save audit

# Check what would be saved (dry run)
/save --dry
```

---

## 📜 RULES APPLIED

| Phase   | Rules                         |
| ------- | ----------------------------- |
| Collect | `context-management`          |
| Write   | `edit-verification`, `safety` |
| Confirm | `evidence`                    |

---

_DOMYH Awesome Code v6.1.2 • Memory Persistence • File-based Transparency_

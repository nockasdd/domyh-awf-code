---
name: recap
trigger: ["/recap", "summary", "tóm tắt"]
description: "📖 Session summary: completed tasks, changed files, decisions, and next steps"
---

# 📖 /recap — Session Recap Pro v3.0

> Intelligent Session Summary
> 📚 Auto-collect • Git-aware • Actionable

---

## 🔄 RECAP FLOW

```
User: /recap
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 0: LOAD MEMORY                    │
│ ▸ Load memory/state.json                │
│ ▸ Load memory/session.md                │
│ ▸ Load memory/decisions.md              │
│ ▸ Load memory/audit_summary.json        │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: COLLECT                        │
│ ▸ Chat history                          │
│ ▸ Git commits                           │
│ ▸ Modified files                        │
│ ▸ Decisions from memory                 │
│ ▸ Audit results from memory             │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: SUMMARIZE                      │
│ ▸ Group by category                     │
│ ▸ Highlight key outcomes                │
│ ▸ Identify blockers                     │
│ ▸ Cross-reference with decisions.md    │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: OUTPUT                         │
│ ▸ Generate report                       │
│ ▸ Suggest next steps                    │
│ ▸ Update session.md with recap          │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMANDS

| Command        | Description          |
| -------------- | -------------------- |
| `/recap`       | Full session summary |
| `/recap short` | Brief summary        |
| `/recap git`   | Git-focused summary  |
| `/recap save`  | Save to file         |

---

## 📊 OUTPUT FORMAT

```markdown
📖 SESSION RECAP

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Date: {date}
Duration: {duration}
Session ID: {id}

## ✅ Completed Tasks

| Task     | Status     |
| -------- | ---------- |
| {task_1} | ✅ Done    |
| {task_2} | ✅ Done    |
| {task_3} | 🔄 Partial |

## 📁 Files Changed

| File     | Action   | Lines   |
| -------- | -------- | ------- |
| `{file}` | Modified | +50/-20 |
| `{file}` | Created  | +100    |
| `{file}` | Deleted  | -80     |

## 📝 Key Decisions

| Decision     | Rationale |
| ------------ | --------- |
| {decision_1} | {why}     |
| {decision_2} | {why}     |

## 🔧 Git Activity
```

{git commits summary}

```

## ⚠️ Issues/Blockers

- {issue_1}
- {issue_2}

## ➡️ Next Steps

| Priority | Task | Effort |
|----------|------|--------|
| P0 | {next_task_1} | S |
| P1 | {next_task_2} | M |
| P2 | {next_task_3} | L |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 Continue with: `/code {next_task_1}`
```

---

## 🔍 AUTO-DETECTION

```yaml
sources:
  # Memory layers (NEW in v4.2)
  memory:
    session: memory/session.md
    state: memory/state.json
    decisions: memory/decisions.md
    audit: memory/audit_summary.json

  chat_history:
    - Task completions
    - Code discussions
    - Decisions made

  git:
    command: "git log --oneline -10"
    include: [commits, branches, tags]

  files:
    command: "git diff --stat HEAD~5"
    include: [modified, created, deleted]
```

---

## 🧠 MEMORY INTEGRATION

```yaml
memory_loading:
  # Load all memory layers on /recap
  on_recap:
    - load: memory/state.json
      extract: [project, last_audit, pending_tasks]

    - load: memory/session.md
      extract: [workflows_executed, notes, errors]

    - load: memory/decisions.md
      extract: [recent_decisions, count: 10]

    - load: memory/audit_summary.json
      extract: [latest_score, trend, issues_count]

  # Update memory after recap
  post_recap:
    - update: memory/session.md
      append: recap_generated_at

    - update: core/session_cache.json
      set: last_recap_time
```

---

## 📄 HANDOFF DOCUMENT GENERATION

```yaml
handoff_doc:
  command: "/recap handoff"
  description: "Generate structured document for session continuity"

  sections:
    project_context:
      - "Current state"
      - "Tech stack"
      - "Key dependencies"

    work_completed:
      - "Tasks done"
      - "Files changed"
      - "Key decisions made"

    pending_work:
      - "Open issues"
      - "Blocked items"
      - "Next priorities"

    critical_info:
      - "Gotchas to avoid"
      - "Non-obvious patterns"
      - "Known bugs"

  output_path: ".domyh/handoff_YYYY-MM-DD.md"
```

---

## 🧠 KNOWLEDGE EXTRACTION

```yaml
knowledge_extraction:
  description: "Extract learnings for future sessions"

  patterns_captured:
    - "Architectural decisions"
    - "Bug fixes and root causes"
    - "Performance optimizations"
    - "Security patches"

  storage:
    path: "memory/learned_patterns.json"
    format:
      pattern: "Description of pattern"
      context: "When to apply"
      example: "Code snippet"
      learned_at: "timestamp"

  auto_detect:
    - "Repeated solutions → Pattern"
    - "Common errors → Prevention rule"
    - "Successful approach → Best practice"
```

---

## 📦 CONTEXT COMPRESSION

```yaml
context_compression:
  description: "Summarize before token limit"

  triggers:
    - "Context window > 80%"
    - "Session > 2 hours"
    - "Major phase complete"

  strategy:
    1_identify: "Key accomplishments"
    2_extract: "Critical decisions"
    3_discard: "Process details"
    4_retain: "File references"

  output:
    short_summary: "~500 tokens"
    key_points: "Bullet list"
    artifacts: "File references only"
```

---

## 🚀 NEXT SESSION PREP

```yaml
next_session:
  command: "/recap next"

  generate:
    quick_start:
      - "1-line context restore"
      - "Priority task"
      - "Open questions"
      - "Suggested first command"

  output: |
    ## 🚀 Quick Start

    **Last session:** {summary}
    **Priority:** {next_task}
    **Blocker:** {if any}

    **Run:** `/code {next_task}`
```

---

## ⚙️ TOKEN OPTIMIZATION

```yaml
token_saving:
  - Only include relevant changes
  - Summarize vs. list everything
  - Focus on outcomes, not process
  - Use handoff for long sessions

memory_efficiency:
  - Load state.json first (~500 tokens)
  - Load session.md only if needed (~2000 tokens max)
  - Skip decisions.md if < 5 decisions
  - Never load semantic layer for recap

total_budget: 3500 # Max tokens for recap operation
```

---

## 📋 COMMANDS EXTENDED

| Command          | Description                      |
| ---------------- | -------------------------------- |
| `/recap`         | Full session summary with memory |
| `/recap short`   | Brief summary (state only)       |
| `/recap git`     | Git-focused summary              |
| `/recap memory`  | Show memory status only          |
| `/recap save`    | Save recap to file               |
| `/recap handoff` | Generate handoff document        |
| `/recap next`    | Prepare for next session         |

---

_DOMYH Awesome Code v4.3 • Recap Pro v3.2 • Session Continuity_

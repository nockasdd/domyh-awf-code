---
description: "📖 Session summary: completed tasks, changed files, decisions, and next steps"
skills: { required: [], contextual: [] }
success_criteria: "Session summary generated, decisions saved, next steps listed"
---

# 📖 /recap — Recap Pro

> Intelligent Session Summary
> 📚 Auto-detect • Memory Integration • Handoff • Context Compression

---

${RULES_RECAP}
## RECAP FLOW

0. **IDENTIFY PROJECT** — ⛔ MANDATORY first step before any data collection:
   - Run `hsa_detect(action='stack')` to identify project
   - If result is `unknown` / 0% confidence → this is an **umbrella/monorepo** directory
   - Scan immediate subdirectories for `.git` folders to find actual repos
   - Run `git log` in **EACH** discovered git repo, NOT at workspace root
   - ⚠️ NEVER use conversation history as primary data source — conversations may reference OTHER projects
   - Set `PROJECT_REPOS` list (e.g. `domyh-awf/`, `hsa-engine-ts/`) for subsequent steps
1. **COLLECT** — Git changes (`git log --oneline -20` **per repo from Step 0**), engine data (`hsa_export`), task list, decisions from memory, file system changes
2. **ANALYZE** — Categorize changes (features, fixes, refactors, docs), calculate metrics (files changed, lines added/removed)
3. **SUMMARIZE** — Group by category, generate structured report. Show: `Session: 2h 15m | 8 tasks | 23 files changed`
4. **PERSIST** — Save key decisions and context to `.agent/memory/state.json` for next session continuity
5. **SUGGEST** — Next steps with priority, suggest `/workflow chain` for follow-up

---

## COMMANDS

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

## 📄 RECAP FORMAT

```markdown
# Session Recap — [date] [duration]

## ✅ Completed (N tasks)

- [task 1] — [files changed]
- [task 2] — [files changed]

## 📊 Metrics

- Files changed: N | Lines +M / -K
- Tests: X passed, Y failed | Coverage: Z%
- Commits: N

## 🔑 Key Decisions

- [decision 1] — Rationale: [why]
- [decision 2] — Rationale: [why]

## 🚧 In Progress

- [WIP item] — [status, blocker]

## ➡️ Next Steps (Priority)

1. [P0] [next task]
2. [P1] [follow-up]
3. [P2] [improvement]
```

---

## 📄 HANDOFF DOCUMENT

Generate with `/recap handoff` for session continuity:

| Section         | Content                |
| --------------- | ---------------------- |
| Project Context | State, stack, key deps |
| Work Completed  | Tasks, commits, code   |
| Decisions Made  | With rationale         |
| Open Issues     | Blockers, TODO         |
| Next Steps      | Prioritized list       |

---

## 🔍 AUTO-DETECTION SOURCES

| Source       | What It Captures                   |
| ------------ | ---------------------------------- |
| Git log      | Commits, diffs, branch changes ⚠️ Run in **EACH sub-repo** if monorepo |
| Memory files | Session state, decisions, patterns |
| Chat history | Task completions, discussions ⚠️ **VERIFY project alignment first** |
| File system  | Modified files, new files, deleted |
| HSA index    | Changed context, invalidated cache |

> [!CAUTION]
> **Monorepo/Umbrella Detection**: If workspace root has NO `.git`, `package.json`, or `Cargo.toml`,
> this is likely an umbrella directory. MUST scan subdirectories for actual git repos.
> NEVER run `git log` at umbrella root — it will fail and cause recap to use wrong project data.

---

## 📦 CONTEXT COMPRESSION

Triggers: Context window > 80%, Session > 2 hours, Major phase complete

Strategy: Keep key decisions + critical code changes, compress repetitive details, save to memory for next session

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`


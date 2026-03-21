---
description: "🎭 Multi-Agent Orchestration: coordinate parallel tasks, delegate to specialists"
skills: { required: [], contextual: [auto] }
success_criteria: "all sub-tasks completed, outputs synthesized, conflicts resolved, log saved"
---

# 🎭 /orchestrate — Orchestrate Pro v2.0

> Multi-Agent Task Coordination with Auto-Detection
> 📚 Auto-Scoring • DAG Execution • Fault Tolerance • Checkpoints • Shared State

---

## 🔄 ORCHESTRATE FLOW (8 Steps)

1. **STEP 0: SCORE (Auto-Detection)** — Evaluate H1-H5 (`complexity-scoring`). Weighted score < 4.0 → route to single persona (EXIT). Score 4.0-6.5 → suggest orchestration. Score ≥ 6.5 or `/orchestrate` → proceed.
2. **STEP 1: INIT STATE** — `hsa_detect` (context), `hsa_session` (governance). Create `orchestration-state.yaml`. 
3. **STEP 2: DECOMPOSE** — Break into sub-tasks (DAG). `hsa_search` + `hsa_explore` for structure. Identify parallel groups.
4. **STEP 3: ASSIGN (Speaker Selection)** — Match tasks to specialist personas. `hsa_delegate` (context packet) + `hsa_delegate` per specialist. Define scope, constraints, deliverables.
5. **STEP 4: PLAN** — ⛔ **STOP & WAIT** for user approval before execution. Show complete DAG, assignments, and token budget. `hsa_session` (trajectory).
6. **STEP 5: EXECUTE** — Run tasks per DAG order (deps first) or parallel (independent). Checkpoint after each task completion. 
7. **STEP 6: MONITOR** — Track task lifecycle. `hsa_session` (scope drift). Handle failures (retry/reassign). Auto-save checkpoints.
8. **STEP 7: SYNTHESIZE** — Merge outputs, resolve conflicts. `hsa_check_changes` to verify integration. Cross-task validation (imports, types, deps).
9. **STEP 8: REPORT + SYNC** — Generate `orchestration-log.md`. `hsa_feedback` (rate relevance). Update `CONTEXT_SNAPSHOT.md`. Show summary to user.

---

## COMMANDS

| Command                  | Description                       |
| ------------------------ | --------------------------------- |
| `/orchestrate [task]`    | Coordinate complex task           |
| `/orchestrate status`    | Check progress                    |
| `/orchestrate merge`     | Synthesize results                |
| `/orchestrate resume`    | Resume from checkpoint            |
| `/orchestrate checkpoint`| Manual checkpoint save            |
| `/orchestrate --visual`  | Show DAG visualization            |
| *(auto-activated)*       | Weighted score ≥ 6.5 from complexity-scoring |

---

## 🔧 SPECIALIST ROLES

| Specialist | Skills                      | Workflow                     |
| ---------- | --------------------------- | ---------------------------- |
| Backend    | API, database, auth         | `/code`, `/test`, `/debug`   |
| Frontend   | UI, UX, components          | `/code`, `/visualize`        |
| DevOps     | Deploy, infra, monitoring   | `/deploy`, `/monitor`        |
| Quality    | Testing, review, audit      | `/test`, `/review`, `/ap`    |
| Security   | Audit, scanning, hardening  | `/security`, `/review`       |
| Data       | Migrations, seeding, schema | `/migrate`, `/generate`      |
| Docs       | README, API docs, changelog | `/doc`                       |

---

## ⚡ ORCHESTRATION PATTERNS

| Pattern                 | Description                            | Use When                    |
| ----------------------- | -------------------------------------- | --------------------------- |
| **Orchestrator-Worker** | Lead decomposes, delegates, aggregates | Default for complex tasks   |
| **Pipeline**            | Sequential stages, parallel within     | Build/deploy/CI pipelines   |
| **Fan-out/Fan-in**      | Distribute → collect → merge           | Multi-module refactoring    |
| **Feedback Loop**       | Draft → review → refine → repeat       | Iterative quality work      |
| **DAG-based**           | Dependency graph execution             | Tasks with prerequisites    |

### DAG Example

```
┌──────────┐     ┌──────────┐
│  DB Model │────→│ API Route │
└──────────┘     └────┬─────┘
                      │
┌──────────┐     ┌────▼─────┐     ┌──────────┐
│ Auth Mid │────→│ Frontend │────→│ E2E Test │
└──────────┘     └──────────┘     └──────────┘
```

---

## 🛡️ FAULT TOLERANCE

| Strategy             | Trigger           | Action                                         |
| -------------------- | ----------------- | ---------------------------------------------- |
| Retry                | Task fails        | 3x with exponential backoff (1s, 2s, 4s)       |
| Reassign             | Retry exhausted   | Re-assign to alternative persona               |
| Skip                 | Optional task     | Mark skipped, continue (no downstream deps)    |
| Escalate             | All exhausted     | Ask user for guidance (input_required)          |
| Checkpoint/Resume    | Recovery          | `/orchestrate resume [checkpoint_id]`          |
| Compensation         | Late failure      | Undo completed sub-tasks                       |

> See `workflows/data/checkpoint-resume.yaml` for full recovery spec.

---

## 📊 TOKEN BOUNDARIES

| Rule            | Description                       |
| --------------- | --------------------------------- |
| Per-agent limit | Explicit token caps per task      |
| Total budget    | 50,000 tokens max per orchestration|
| Timeout         | Max 30m per task, 2h total        |
| Loop prevention | Detect recursive/circular calls   |
| Alert           | Notify at 90% of limit            |
| Budget tracking | Show token usage per specialist   |

---

## 📁 RELATED FILES

| File | Purpose |
| ---- | ------- |
| `rules/modules/complexity-scoring.yaml` | Auto-detection scoring engine |
| `workflows/data/orchestration-state.yaml` | Shared state schema |
| `rules/modules/agent-communication.yaml` | Message protocol |
| `workflows/data/checkpoint-resume.yaml` | Recovery specification |
| `workflows/data/orchestration-log.md` | Log output template |
| `rules/modules/agent-delegation.yaml` | Delegation rules + permissions |
| `personas/orchestrator.md` | Persona definition |
| `rules/SACRED_RULES.xml` | MCP_004 enforcement |

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


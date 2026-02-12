---
description: "🎭 Multi-Agent Orchestration: coordinate parallel tasks, delegate to specialists"
skills: { required: [], contextual: [] }
---

# 🎭 /orchestrate — Orchestrate Pro

> Multi-Agent Task Coordination
> 📚 Parallel Execution • Fault Tolerance • Checkpoints • DAG-based Dependencies

---

## ORCHESTRATE FLOW

1. **DECOMPOSE** — Break complex task into sub-tasks, identify dependencies, build DAG (Directed Acyclic Graph). Show: `[Step 1/5] Decomposing into 4 parallel tasks...`
2. **ASSIGN** — Map sub-tasks to specialist personas, define interfaces between agents
3. **PLAN** — Define execution order, checkpoints, rollback points → ⛔ STOP for user approval. Show task DAG visualization
4. **EXECUTE** — Run parallel tasks, monitor progress, handle failures. Show: `[Task 2/4] Backend API ████████░░ 80%`
5. **SYNTHESIZE** — Merge results, resolve conflicts, verify integration. Run cross-task tests

---

## COMMANDS

| Command                 | Description             |
| ----------------------- | ----------------------- |
| `/orchestrate [task]`   | Coordinate complex task |
| `/orchestrate status`   | Check progress          |
| `/orchestrate merge`    | Synthesize results      |
| `/orchestrate resume`   | Resume from checkpoint  |
| `/orchestrate --visual` | Show DAG visualization  |

---

## 🔧 SPECIALIST ROLES

| Specialist | Skills                      | Delegates To               |
| ---------- | --------------------------- | -------------------------- |
| Backend    | API, database, auth         | `/code`, `/test`, `/debug` |
| Frontend   | UI, UX, components          | `/code`, `/visualize`      |
| DevOps     | Deploy, infra, monitoring   | `/deploy`, `/monitor`      |
| Quality    | Testing, review, audit      | `/test`, `/review`, `/ap`  |
| Security   | Audit, scanning, hardening  | `/ap security`, `/review`  |
| Data       | Migrations, seeding, schema | `/migrate`, `/generate`    |

---

## ⚡ ORCHESTRATION PATTERNS

| Pattern                 | Description                            | Use When                    |
| ----------------------- | -------------------------------------- | --------------------------- |
| **Orchestrator-Worker** | Lead decomposes, delegates, aggregates | Default for complex tasks   |
| **Pipeline**            | Sequential stages, parallel within     | Build/deploy/CI pipelines   |
| **Fan-out/Fan-in**      | Distribute → collect → merge           | Multi-module refactoring    |
| **Feedback Loop**       | Draft → review → refine → repeat       | Iterative quality work      |
| **DAG-based**           | Dependency graph execution             | Tasks with prerequisites    |
| **Peer-to-Peer**        | Agents communicate directly            | Distributed decision-making |

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

| Strategy             | Trigger           | Action                                |
| -------------------- | ----------------- | ------------------------------------- |
| Retry                | Task fails        | Retry 3x with exponential backoff     |
| Graceful degradation | Partial failure   | Continue with available results       |
| Circuit breaker      | Repeated failures | Stop after 3 fails in 5 attempts      |
| Checkpoint/Resume    | Recovery          | `/orchestrate resume [checkpoint_id]` |
| Compensation         | Late failure      | Undo completed sub-tasks              |

---

## 📊 EXECUTION MONITORING

```yaml
monitoring:
  per_task:
    - status: "pending | running | completed | failed"
    - progress: "percentage or step count"
    - duration: "elapsed time"
    - dependencies: "blocked by / blocking"

  overall:
    - total_tasks: N
    - completed: M
    - failed: F
    - eta: "estimated completion"

  alerts:
    - task_timeout: "30 minutes per sub-task"
    - stuck_detection: "No progress for 5 minutes"
    - loop_prevention: "Max 3 retries per task"
```

---

## 📊 TOKEN BOUNDARIES

| Rule            | Description                       |
| --------------- | --------------------------------- |
| Per-agent limit | Set explicit token caps per task  |
| Timeout         | Max execution time per task (30m) |
| Loop prevention | Detect recursive/circular calls   |
| Alert           | Notify at 90% of limit            |
| Budget tracking | Show token usage per specialist   |

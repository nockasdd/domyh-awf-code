---
description: "Multi-Agent Orchestration: coordinate parallel tasks, delegate to specialists"
skills: { required: [], contextual: [auto] }
success_criteria: "All sub-tasks completed, outputs synthesized, conflicts resolved"
---

# /orchestrate

## FLOW (8 Steps)

1. **SCORE** — Evaluate H1-H5 complexity. Score <4.0: route to single persona (EXIT). Score 4-6.5: suggest. Score >=6.5: proceed.
2. **INIT** — hsa_detect(context), hsa_session(governance). Create orchestration state.
3. **DECOMPOSE** — Break into sub-tasks (DAG). hsa_search + hsa_explore for structure. Identify parallel groups.
4. **ASSIGN** — Match tasks to specialist personas. hsa_delegate per specialist. Define scope, constraints, deliverables.
5. **PLAN** — STOP: show DAG, assignments, token budget. Wait for user approval.
6. **EXECUTE** — Run tasks per DAG order (deps first) or parallel (independent). Checkpoint after each.
7. **MONITOR** — Track lifecycle, handle failures (retry/reassign), auto-save checkpoints.
8. **SYNTHESIZE** — Merge outputs, resolve conflicts, cross-task validation (imports, types, deps). hsa_check_changes.

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/orchestrate [task]` | Coordinate complex task |
| `/orchestrate status` | Check progress |
| `/orchestrate merge` | Synthesize results |
| `/orchestrate resume` | Resume from checkpoint |
| `/orchestrate checkpoint` | Manual save |

## SPECIALIST ROLES

| Specialist | Workflows |
|:-----------|:----------|
| Backend | /code, /test, /debug |
| Frontend | /code, /visualize |
| DevOps | /deploy, /monitor |
| Quality | /test, /review, /ap |
| Security | /security, /review |
| Data | /migrate, /generate |
| Docs | /doc |

## PATTERNS

| Pattern | Use When |
|:--------|:---------|
| Orchestrator-Worker | Default for complex tasks |
| Pipeline | Build/deploy/CI pipelines |
| Fan-out/Fan-in | Multi-module refactoring |
| Feedback Loop | Iterative quality work |
| DAG-based | Tasks with prerequisites |

## FAULT TOLERANCE

- Task fails: retry once, then reassign to different approach
- 3 consecutive failures: STOP, report blockers to user
- Checkpoint after each task completion (auto-resume on crash)

## CHECKPOINT

1. Generate orchestration-log.md
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`

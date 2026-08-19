---
description: "Multi-Agent Orchestration: coordinate parallel subagents via SDD (Subagent-Driven Development) and 2-tier review gates"
skills: { required: [delegation-intelligence], contextual: [auto] }
success_criteria: "All sub-tasks completed, passed 2-tier review gates, outputs synthesized with zero regressions"
---

# /orchestrate

## FLOW (8 Steps — Superpowers SDD Rigor)

1. **SCORE** — Evaluate H1-H5 complexity. Score <4.0: route to single persona (EXIT). Score 4-6.5: suggest. Score >=6.5: proceed.
2. **INIT** — `hsa_detect(context)`, `hsa_session(governance)`. Create orchestration state in memory.
3. **DECOMPOSE** — Break into **bite-sized subtasks (2-5 mins)** (DAG). Identify parallel groups and dependency chains.
4. **CONTRACT (SDD)** — For each task: call `hsa_delegate({action:'prepare', task_type:'...', focus_files:[...]})`. Define strict focus scope, tool policy, acceptance criteria, and workspace mode (`branch`).
5. **PLAN & APPROVE** — ⛔ **STOP**: Present DAG, task contracts, token budgets, and verification plans to user. Wait for approval.
6. **EXECUTE (Native-First Dispatch)**:
   - **Antigravity**: `invoke_subagent` with `branch` workspace.
   - **Claude Code**: `.claude/agents/` in isolated git worktree.
   - **Codex**: `AGENTS.md` with scoped directory execution.
   - **Cursor/Fallback**: `hsa_delegate({action:'cascade'})` $\rightarrow$ poll `cascade_read`.
7. **2-TIER REVIEW GATE**:
   - **Tier 1 (Spec Compliance)**: `hsa_delegate({action:'verify', focus_files:[...], modified_files:[...]})`. Verify zero out-of-scope modifications.
   - **Tier 2 (Quality & TDD)**: Execute test runners and compiler checks (`npm test`, `tsc --noEmit`). If failed: re-dispatch fix.
8. **SYNTHESIZE & PERSIST**:
   - Merge branched worktree/workspace into main.
   - `hsa_check_changes` to refresh Merkle search index.
   - `hsa_session({action:'persist', task_summary:'...'})`.

## COMMANDS

| Command | Description |
|:---|:---|
| `/orchestrate [task]` | Coordinate complex task with SDD subagents |
| `/orchestrate status` | Check active subagents & DAG progress |
| `/orchestrate gate` | Run 2-Tier Quality Review Gate on subagent deliverable |
| `/orchestrate merge` | Synthesize and merge verified subagent results |
| `/orchestrate resume` | Resume from checkpoint |
| `/orchestrate checkpoint` | Manual state checkpoint |

## SPECIALIST ROLES

| Specialist | Workflows | Default Focus Scope |
|:---|:---|---|
| Developer | /code, /debug, /fix | Business logic, API endpoints, components |
| Tester | /test, /tdd, /e2e | Unit tests, mock suites, integration tests |
| Auditor | /review, /security, /ap | Code quality audit, security analysis (Read-Only) |
| DevOps | /deploy, /monitor | CI/CD pipelines, Docker, infrastructure |
| Researcher | /think, /plan, /onboard | Web exploration, dependency analysis (Read-Only) |

## FAULT TOLERANCE & RECOVERY

- **Gate Rejection**: If Tier 1 or Tier 2 fails, do NOT merge. Re-dispatch subagent with explicit failure diagnostics.
- **Max Retries**: 2 retries per subtask. On 3rd failure: STOP and escalate blocker to user.
- **Checkpointing**: Auto-checkpoint state after every passing task gate.

## CHECKPOINT

1. Generate `orchestration-log.md`
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`

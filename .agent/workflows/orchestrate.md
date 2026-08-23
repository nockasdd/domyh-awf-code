---
description: "Multi-Agent Orchestration: coordinate parallel subagents via SDD (Subagent-Driven Development), strict platform dispatch, and 2-tier review gates"
skills: { required: [delegation-intelligence], contextual: [auto] }
success_criteria: "All sub-tasks completed, passed 2-tier review gates, outputs synthesized with zero regressions"
---

# 🎼 /orchestrate — Multi-Agent Orchestration & SDD

## 🛡️ [GATE 0: PRE-FLIGHT ORCHESTRATION & PLATFORM SAFETY RULES]

1. **NO EXTERNAL BINARY/GUI SPAWNING**: NEVER attempt to execute arbitrary OS executables, desktop launchers, or mistranslated CLI commands (e.g. `orca`, `orca.exe`, screen readers, or unverified binaries). All agent orchestration occurs strictly WITHIN the active IDE/CLI agent harness.
2. **STRICT PLATFORM DISPATCH**: Always match the active platform's native agent capabilities before dispatching work (see Platform Dispatch Matrix below).
3. **SUBAGENT DELEGATION THRESHOLDS**:
   - **Mandatory Subagent**: Broad exploration (>10 unknown files), full project audit (`/ap`), or independent multi-module implementation.
   - **Direct Main Agent**: Targeted read/edit (<3 known files), single-function trace (`hsa_trace_flow`), or small surgical bugfix (<50 lines).
4. **ISOLATED WORKSPACE & READ-ONLY CONFINEMENT**: Subagents performing audits or research MUST be read-only. Modifying subagents MUST use branched/isolated workspaces.
5. **2-TIER REVIEW GATE**: Never merge subagent outputs without Tier 1 (Spec Compliance) and Tier 2 (Test & Quality Verification) validation.

---

## 🔀 PLATFORM & IDE DISPATCH MATRIX

```
┌───────────────────────────┬────────────────────────────────────────────────────────────────────────┐
│ ACTIVE PLATFORM / APP     │ DISPATCH MECHANISM & PROTOCOL                                          │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 1. Google Antigravity     │ • Native `invoke_subagent` with `Workspace: "branch"` or `"inherit"`  │
│                           │ • Use `research` role for read-only lookups, `self` for full refactor  │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 2. OpenAI Codex (App/CLI) │ • Dispatch via `AGENTS.md` persona routing & scoped task files        │
│                           │ • DO NOT launch GUI apps. Execute in workspace directory.              │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 3. Claude Code            │ • Native subagents in `.claude/agents/` using isolated Git worktrees   │
│                           │ • `git worktree add -b task-name ../worktrees/task-name`              │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 4. Cursor IDE             │ • Cursor Agent / Composer sub-flows or MCP `hsa_delegate({action})`    │
├───────────────────────────┼────────────────────────────────────────────────────────────────────────┤
│ 5. VS Code (Cline / Roo)  │ • Native Custom Modes (Architect, Code, Ask, Test)                    │
└───────────────────────────┴────────────────────────────────────────────────────────────────────────┘
```

---

## 📋 8-STEP ORCHESTRATION FLOW

### 1. SCORE & COMPLEXITY EVALUATION
*   Evaluate H1-H5 task complexity.
*   **Score < 4.0**: Simple task $\rightarrow$ Execute directly in Main Agent (EXIT).
*   **Score 4.0 – 6.5**: Moderate task $\rightarrow$ Suggest subagent decomposition to user.
*   **Score ≥ 6.5**: Complex / Multi-module task $\rightarrow$ Mandatory SDD Orchestration.

### 2. INITIALIZATION & STACK DETECTION
*   `hsa_detect(context)` $\rightarrow$ detect active platform, runtime, frameworks, and workspace.
*   `hsa_session(action="governance")` $\rightarrow$ initialize orchestration state machine in memory.

### 3. DECOMPOSITION (DAG & BITE-SIZED TASKS)
*   Break goal into **independent, bite-sized subtasks (2–5 minutes runtime)**.
*   Construct a Directed Acyclic Graph (DAG) distinguishing:
    *   *Parallel Groups*: Independent tasks with zero file overlap.
    *   *Sequential Chains*: Tasks dependent on predecessor deliverables.

### 4. SDD TASK CONTRACT FORMATION
For each subtask, generate an immutable Task Contract:
```yaml
contract_id: "sdd_task_{id}"
task_type: "code | test | review | research | audit"
focus_files: ["path/to/target.ts", "path/to/target.test.ts"] # Strict boundary
tool_policy: "read_only | full_write"
acceptance_criteria:
  - "Unit tests pass with 100% assertion coverage"
  - "Zero out-of-scope files modified"
  - "Typecheck clean (tsc --noEmit)"
```

### 5. PLAN & APPROVE GATE (⛔ STOP — Confirm with User)
*   Present DAG, assigned specialist roles, focus files, and token budgets.
*   ⛔ **STOP**: Await user confirmation before dispatching subagents.

### 6. DISPATCH & CONCURRENT EXECUTION
*   Dispatch subagents concurrently according to the active Platform Dispatch Matrix.
*   Ensure research/audit subagents run in **Read-Only mode** to keep parent context clean.
*   Collect compact findings/deliverables upon completion (no raw context dumping).

### 7. 2-TIER QUALITY REVIEW GATE
*   **Tier 1 (Spec Compliance)**: Verify that subagent touched ONLY files in `focus_files`. Any unapproved modifications $\rightarrow$ **REJECT & REVERT**.
*   **Tier 2 (Quality & TDD)**: Run test suites and linters (`npm test`, `pytest`, `tsc`). If broken $\rightarrow$ re-dispatch correction.

### 8. SYNTHESIZE & PERSIST
*   Merge verified deliverables into main branch/workspace.
*   `hsa_check_changes` $\rightarrow$ refresh Merkle semantic search index.
*   `hsa_session(action="persist", task_summary="Orchestrated N subtasks successfully with zero regressions")`.

---

## 👥 SPECIALIST ROLES & RESPONSIBILITIES

| Specialist | Role Focus | Tool Policy | Typical Delegation Trigger |
|:-----------|:-----------|:------------|:---------------------------|
| **Researcher** | Web exploration, library comparisons, unknown APIs | `read_only` | Unfamiliar tech, documentation lookups |
| **Auditor** | Security scan, taint flow, call graph, blast radius | `read_only` | Full codebase audit, pre-release review |
| **Developer** | Core business logic, component implementation | `full_write` | Scoped feature building in isolated files |
| **Tester** | Unit test suites, integration mocks, TDD validation | `full_write` | Test harness generation, regression tests |
| **DevOps** | CI/CD workflows, Docker configs, environment setup | `full_write` | Infrastructure changes |

---

## 🔁 FAULT TOLERANCE & RECOVERY PROTOCOL

- **Out-of-Scope Modification**: Subagent modified unauthorized files $\rightarrow$ discard diff, re-dispatch with tightened focus scope.
- **Assertion Failure**: Test suite failed $\rightarrow$ pass failure stacktrace back to subagent (Max 2 retries).
- **Stuck / Loop Detection**: Subagent takes > 5 turns without progress $\rightarrow$ terminate, reframe task, or escalate to user.
- **State Checkpoint**: Auto-save state in `.domyh/orchestration/` after every passing review gate.

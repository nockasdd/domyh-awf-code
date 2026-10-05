---
description: "Deep Interprocedural Project Audit: 12-Expert Panel with Subagent Delegation, Call Graph, API Contract Invariants, and Blast Radius Analysis"
skills: { required: [audit-pro], contextual: [security, coding-rules, testing, observability, authentication] }
related_workflows: [review, security, test, verify, fix]
success_criteria: "Audit report generated with score, deep interprocedural findings, call chain traces, and blast radius quantification"
---

# 🔬 /ap — Deep Interprocedural Audit Pro

## 🛡️ [GATE 0: PRE-FLIGHT AUDIT RULES — READ BEFORE AUDITING]

1. **NO SURFACE-ONLY AUDITING**: Never stop at intraprocedural (single-file/local) checks. Every P0/P1 finding MUST trace the entire interprocedural call graph (`hsa_trace_flow`) from Entry Point to Sink.
2. **SUBAGENT DELEGATION ON SCALE**: If codebase has ≥20 files or is a multi-package monorepo, Main Agent MUST act as Orchestrator and dispatch specialized subagents to prevent context saturation.
3. **PARALLEL TOOL BATCHING**: Always batch independent `view_file`, `hsa_search`, and `hsa_trace_flow` calls in PARALLEL in a SINGLE turn.
4. **EVIDENCE & BLAST RADIUS**: All findings MUST have concrete `file:line` citations, call chain paths, and quantified Direct, Transitive, and Systemic impact radius.
5. **SCOPE CONTRACT STOP**: MUST pause at Step 4 (Scope Contract) for explicit user scope confirmation before deep execution.
6. **EPISTEMIC HONESTY & RESIDUAL BOUNDS**: Every finding and verdict must classify its Proof Grade ([EMPIRICAL], [STATIC-ANALYSIS], [DEDUCTIVE-LOGIC], [THEORETICAL-MODEL], [RESIDUAL-RISK]). Never claim 100% security or complete flawlessness.

---

## 🔄 5 DEEP AUDIT PILLARS (INTERPROCEDURAL ANALYSIS)

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 1. ENTRY POINT HARVESTING   ➔ Map all Public APIs, Route Handlers, CLI & Event Listeners│
│ 2. CALL GRAPH & TAINT FLOW  ➔ Trace Source ➔ Sanitizer ➔ Mutator ➔ Sink (hsa_trace_flow)│
│ 3. API & FUNCTION CONTRACTS ➔ Verify Pre-conditions, Post-conditions, Null & Error Invariants│
│ 4. STATE MUTATION & ACID    ➔ Audit Database Rollbacks, Cache Invalidations, Idempotency│
│ 5. BLAST RADIUS MATRIX      ➔ Quantify Direct, Transitive & Systemic Failure Impact    │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🔀 EXECUTION MODE SELECTION (SCALE MATRIX)

| Codebase Scale | Trigger Condition | Execution Strategy |
|:---------------|:------------------|:-------------------|
| **Small (<20 files)** | Single module, focused repo | **Single Agent**: Sequential expert panel in main context. |
| **Large (≥20 files)** | Monorepo, complex system, or `--subagents` flag | **Subagent-Driven Auditing (SDA)**: Main Agent dispatches 3 specialized subagents concurrently. |

---

## 📋 11-STEP AUDIT FLOW

### 1. DISCOVERY & ENTRY POINT HARVESTING (30s)
*   `hsa_session("audit project")`, `hsa_detect(stack)` → extract runtime, frameworks, database, external dependencies.
*   `hsa_explore(repo_map)` → map directory structure and catalogue all **Public Entry Points** (HTTP Routes, RPC endpoints, Webhooks, Message Listeners, CLI commands).
*   `git diff --name-only HEAD~5..HEAD` → identify recent churn hotspots.
*   Load previous audit from `.domyh/audits/` → track score delta and unresolved findings.

### 2. RISK & HEURISTIC ASSESSMENT
```yaml
inputs: [project_type, file_count, dep_count, git_history, complexity_hotspots]
output:
  hot_zones: ["auth/", "api/", "payment/", "config/"] # High-risk → Full Interprocedural SCoT
  warm_zones: ["services/", "models/", "helpers/"]     # Medium → Standard SCoT
  cold_zones: ["docs/", "scripts/", "test/"]          # Low → Lightweight SCoT
  risk_score: X/10
```

### 3. SMART LOAD (Token-Optimized On-Demand Data, ~500 tok)
*   Tier 2 On-Demand Loading via MCP:
    *   Security Checklist: `hsa_search(action="skill_data", skill_id="audit-pro", section="security")`
    *   Architecture / Reliability: `hsa_search(action="skill_data", skill_id="audit-pro", section="architecture")`
    *   Weight Profile: `hsa_search(action="skill_data", skill_id="audit-pro", section="scoring")`
*   Load supplementary checklists only if domain detected (e.g. desktop, CLI, MCP, game).

### 4. SCOPE CONTRACT GATE (⛔ STOP — Confirm with User)
*   Display active expert panel, risk zones, execution mode (Single vs Subagents), and estimated token budget.
*   ⛔ **STOP**: Await user confirmation before beginning deep execution.

### 5. EXECUTE: SCoT DEEP INTERPROCEDURAL PANEL

#### Mode A: Subagent-Driven Auditing (for Large Repos ≥20 files)
Orchestrator dispatches 3 specialized subagents in parallel with isolated contexts:
1.  **Subagent Security**: `invoke_subagent` for Entry points, Authentication, Taint Flow, Secrets, and Injection analysis.
2.  **Subagent Architecture**: `invoke_subagent` for Interprocedural Call Graph, Module Boundaries, Circular Dependencies, and Blast Radius mapping.
3.  **Subagent Reliability**: `invoke_subagent` for Database Transactions (`$transaction`), Rollback safety, Idempotency, and Concurrency.

#### Mode B: Single Agent Panel (for Small Repos <20 files)
Sequential execution using 7-step Deep SCoT:
| Step | Action | Description |
|:-----|:-------|:------------|
| 1. LOCATE | `hsa_search` | Pin exact `file:line` references across module boundaries |
| 2. TRACE | `hsa_trace_flow` | Delineate full Call Graph from Entry Point (Source) to Sink |
| 3. CONTRACT | Function Invariants | Verify parameter sanity, return types, null safety, error codes |
| 4. MUTATE | Side-Effects & ACID | Check database transactions, shared memory mutations, race conditions |
| 5. BLAST | Impact Matrix | Quantify Direct (Callers), Transitive (Services), Systemic (Failures) |
| 6. COUNTER | Devil's Advocate | Challenge the finding: Is there a legitimate architectural trade-off? |
| 7. VERDICT | P0 / P1 / P2 / P3 | Assign severity with confidence score (1-10) |

### 6. CRITIQUE ROUND (Cross-Expert Challenge on P0/P1)
*   Security ↔ Architecture | Performance ↔ Quality | DevOps ↔ Reliability.
*   Outcomes: `AGREE` | `DISPUTE` (reasoned) | `ELEVATE` | `LOWER`.

### 7. HOLISTIC SYNTHESIS (5 Systemic Questions)
*   Q1: **Architecture Coherence**: Contradictions between modules or layer-skipping?
*   Q2: **Inter-Service Fragility**: Undocumented tight coupling or circular dependency?
*   Q3: **State Corruption Risk**: Can any partial failure leave orphaned or corrupt records?
*   Q4: **Cascading Blast Radius**: At 10x load or external API outage, what cascades first?
*   Q5: **Production Readiness**: Security, observability, and graceful degradation in place?

### 8. DEBATE ROUND (Triggered on Systemic-Critical or $\ge 3$ Systemic-Warnings)
*   Expert panel debates systemic findings to confirm or downgrade severity.

### 9. SELF-REVIEW & DEDUPLICATION
*   Deduplicate overlapping findings, verify evidence paths, resolve open disputes.

### 10. GENERATE DEEP AUDIT REPORT
*   Output overall score (0-10), P0-P3 breakdown with Call Chains and Blast Radius matrices.
*   Save report to `.domyh/audits/audit_YYYY-MM-DD.md`.

### 11. PERSIST SESSION
*   `hsa_session(action="persist", task_summary="Deep audit completed with interprocedural analysis and subagent orchestration")`.

---

## 📊 DEEP FINDING OUTPUT SCHEMA (MANDATORY FOR P0/P1)

```markdown
### 🔴 [P0/P1 - SEVERITY] Finding Title
- **Entry Point**: `METHOD /route` (`path/to/controller.ts:line`)
- **Interprocedural Call Chain**:
  `EntryController.handler()` ➔ `DomainService.execute()` ➔ `Repository.mutate()` ➔ `ExternalAPI.call()`
- **Contract & Logic Flaw**:
  [Exact description of violated invariants, unhandled edge cases, or missing transaction boundary]
- **Taint Flow & Side-Effects**:
  * Unsanitized data flow: `req.body.field` reaches `DB.query()` without boundary check.
  * Side-effects: Writes to Table A before Table B without atomic rollback (`$transaction`).
- **Blast Radius & Cascading Impact**:
  * *Direct (Callers)*: [Affected immediate consumers]
  * *Transitive (Services)*: [Downstream APIs, background queues, dependencies]
  * *Systemic Risk*: [Data corruption, deadlock, service crash, auth bypass]
- **Remediation**:
  [Concrete, actionable refactoring steps to restore contract and transaction safety]
```

---

## 🎯 [GATE 9: POST-FLIGHT AUDIT CHECKLIST — VERIFY BEFORE PRESENTING]

Before delivering the audit report, MUST verify:
1.  ✅ **Was Subagent Delegation triggered if the repo has ≥20 files to keep context unpolluted?**
2.  ✅ **Does every P0/P1 finding contain a complete Interprocedural Call Chain (`hsa_trace_flow`)?**
3.  ✅ **Are API and Function Contract Invariants explicitly checked (not just syntax)?**
4.  ✅ **Is the Blast Radius quantified across Direct, Transitive, and Systemic layers?**
5.  ✅ **Has the report been saved to `.domyh/audits/` and persisted in session memory?**
6.  ✅ **Are Proof Grades tagged on all conclusions and are known limitations/residual risks clearly bound?** *(Zero overclaiming)*
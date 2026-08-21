---
description: "Deep Interprocedural Project Audit: 12-Expert Panel with Call Graph, API Contract Invariants, Taint Flow, and Blast Radius Analysis"
skills: { required: [audit-pro], contextual: [security, coding-rules, testing, observability, authentication] }
related_workflows: [review, security, test, verify, fix]
success_criteria: "Audit report generated with score, deep interprocedural findings, call chain traces, and blast radius quantification"
---

# 🔬 /ap — Deep Interprocedural Audit Pro

## 🛡️ [GATE 0: PRE-FLIGHT AUDIT RULES — READ BEFORE AUDITING]

1. **NO SURFACE-ONLY AUDITING**: Never stop at intraprocedural (single-file/local) checks. Every P0/P1 finding MUST trace the entire interprocedural call graph (`hsa_trace_flow`) from Entry Point to Sink.
2. **EVIDENCE MANDATE**: All findings MUST have concrete `file:line` citations, exact call chain paths, and reproducible scenarios.
3. **COUNTER-ARGUMENT MANDATORY**: Every FAIL verdict MUST include a devil's advocate counter-argument explaining why the pattern might have been chosen.
4. **BLAST RADIUS QUANTIFICATION**: For every P0/P1 vulnerability or architectural defect, explicitly map Direct, Transitive, and Systemic impact radius.
5. **SCOPE CONTRACT STOP**: MUST pause at Step 4 (Scope Contract) for explicit user scope confirmation before running the full execution panel.

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

### 3. SMART LOAD (Token-Optimized, ~3000 tok)
*   Load active expert checklists from `data/checklists/{expert}.yaml`.
*   Load supplementary checklists if detected (desktop, CLI, library, MCP, game).
*   Auto-select weight profile from `scoring.yaml`.

### 4. SCOPE CONTRACT GATE (⛔ STOP — Confirm with User)
*   Display active expert panel, risk zones, previous score, and estimated token budget.
*   ⛔ **STOP**: Await user confirmation before beginning deep execution.

### 5. EXECUTE: SCoT DEEP INTERPROCEDURAL PANEL
Run Expert Panels sequentially with **SCoT Deep Tracing**:

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
*   `hsa_session(action="persist", task_summary="Deep audit completed with interprocedural analysis")`.

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
1.  ✅ **Does every P0/P1 finding contain a complete Interprocedural Call Chain (`hsa_trace_flow`)?**
2.  ✅ **Are API and Function Contract Invariants explicitly checked (not just syntax)?**
3.  ✅ **Is the Blast Radius quantified across Direct, Transitive, and Systemic layers?**
4.  ✅ **Is a counter-argument provided for every FAIL verdict to eliminate bias?**
5.  ✅ **Has the report been saved to `.domyh/audits/` and persisted in session memory?**
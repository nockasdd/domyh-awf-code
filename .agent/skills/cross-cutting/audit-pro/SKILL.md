---
name: audit-pro
description: "Deep Interprocedural Project Audit: 12-Expert Panel with Call Graph, API Contract Invariants, Taint Flow, and Blast Radius Analysis."
detect: []
priority: 1
category: cross-cutting
tier: 1
---

# Audit Pro — Deep Interprocedural Audit System

> 🔬 **12-Expert Panel** | **277+ Checkpoints** | **Interprocedural Analysis**
> 🧠 **Call Graph Tracing** | **Contract Invariants** | **Blast Radius Quantification**

---

## 1. Core Audit Methodology: Beyond Surface Checklists

Traditional auditing stops at single-file/intraprocedural inspection ("does this function have try-catch?"). Audit Pro enforces **Interprocedural & Contract Auditing**:

```
[1. ENTRY POINT] ➔ [2. CALL GRAPH TRACE] ➔ [3. CONTRACT INVARIANTS] ➔ [4. STATE MUTATION] ➔ [5. BLAST RADIUS]
```

### The 4 Deep Analysis Vectors:

| Vector | What To Audit | Primary Tool / Protocol |
|:-------|:--------------|:------------------------|
| **1. Interprocedural Call Graph** | Caller ⇄ Callee dependency tree, cyclic dependencies, deadlock potential, unreachable code | `hsa_trace_flow(entry, direction:"both")` |
| **2. Taint & Data Flow** | Untrusted Source ➔ Sanitizers/Validators ➔ Mutators ➔ Sensitive Sinks (SQL, Crypto, FS, Network) | Source-to-Sink Path Tracing |
| **3. API & Function Contracts** | Pre-conditions (boundary/null checks), Post-conditions, Return schemas, Consistent error codes | Design by Contract Invariant Verification |
| **4. State Mutation & Atomicity** | Partial database mutations, lack of transaction rollbacks (`$transaction`), Cache/Queue desync, Race conditions | ACID & Idempotency Analysis |

---

## 2. Blast Radius Quantification Protocol

For every identified vulnerability or architectural flaw, classify its impact across 3 concentric circles:

```
                  ┌─────────────────────────────────────────┐
                  │          3. SYSTEMIC IMPACT             │
                  │   (Cascading Failure, Service Outage,   │
                  │    Data Corruption, Security Breach)    │
                  │    ┌───────────────────────────────┐    │
                  │    │     2. TRANSITIVE IMPACT      │    │
                  │    │  (Downstream Services, Queues,│    │
                  │    │   Dependent APIs, Background) │    │
                  │    │    ┌─────────────────────┐    │    │
                  │    │    │  1. DIRECT IMPACT   │    │    │
                  │    │    │(Immediate Callers & │    │    │
                  │    │    │ Local Function State│    │    │
                  │    │    └─────────────────────┘    │    │
                  │    └───────────────────────────────┘    │
                  └─────────────────────────────────────────┘
```

### Blast Radius Scoring:
- **Low (Score 1-3)**: Isolated to single helper/pure function. No database mutation or public exposure.
- **Medium (Score 4-6)**: Affects multiple internal services or unhandled edge cases in non-critical endpoints.
- **High / Critical (Score 7-10)**: Reaches Public Entry Points, corrupts persistent database state without rollback, or causes cascading timeout/crash across multiple services.

---

## 3. Deep SCoT Protocol (Per Checkpoint)

```yaml
# 7-step Deep Structured Chain-of-Thought
deep_scot_protocol:
  1_locate: "Pin exact file:line references using hsa_search"
  2_trace: "Run hsa_trace_flow to map full Call Graph from Entry Point to Sink"
  3_contract: "Audit Pre-conditions, Post-conditions, Null-safety, and Error Invariants"
  4_mutation: "Verify State Mutations, Transaction Rollback safety, and Concurrency"
  5_blast_radius: "Quantify Direct, Transitive, and Systemic impact radius"
  6_counter: "Devil's advocate — examine valid engineering trade-offs / MVP rationale"
  7_verdict: "P0 / P1 / P2 / P3 verdict with calibrated confidence score (1-10)"
```

---

## 4. Deep Finding Output Schema (Mandatory for P0/P1)

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

## 5. Expert × Skill Matrix

| Expert | Core Skills Loaded | Deep Tracing Focus |
|:-------|:-------------------|:-------------------|
| **Security** | `security`, `authentication` | Public Entry Points, Taint Flow, Auth Bypass, Secrets, RBAC, Injection |
| **Architecture** | `coding-rules`, `api-design` | Interprocedural Call Graph, Module Boundaries, Cyclic Dependencies, Layers |
| **Reliability / SRE** | `observability`, `error-handling` | Transaction Boundaries, Rollbacks, Graceful Degradation, Circuit Breaking |
| **Performance** | `observability`, `web-perf` | Query N+1 in Call Chains, Memory Leaks, Heavy Blocking Operations |
| **Quality** | `testing`, `error-handling` | Contract Invariants, Null Safety, Boundary Limits, Error Code Consistency |
| **Data** | `database`, `sql` | ACID Transactions, Migration Invariants, Indexing Hotspots, Orphan Records |
| **DevOps** | `logging`, `ci-cd` | Supply Chain, Secrets in Configs, Deployment Blast Radius |

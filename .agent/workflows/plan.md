---
description: "Plan Pro: Outcome-focused feature planning with impact analysis, risk matrix, bite-sized tasks, and TDD granularity"
skills: { required: [], contextual: [auto] }
success_criteria: "Understanding lock passed, plan approved by user, bite-sized tasks broken down, saved to .domyh/plans/"
---

# /plan — Outcome-Focused Feature Planning

## 🛡️ [GATE 0: PRE-FLIGHT PLANNING RULES — READ BEFORE PLANNING]

1. **EVIDENCE-BASED DESIGN**: All technical decisions and architectural choices MUST be grounded in codebase inspection (`hsa_search`, `hsa_explore`, `view_file`). Never guess architecture.
2. **UNDERSTANDING LOCK MANDATE**: MUST lock and confirm understanding with user in Phase 1 before entering Phase 3 (Detailed Technical Design).
3. **SCOPE CREEP GUARD**: If new requirements or expansions arise during planning ➔ place them immediately into **Scope OUT**. Never expand scope silently.
4. **BITE-SIZED TASK GRANULARITY**: Every task step MUST be an **atomic action (2 - 5 minutes)** with exact file paths (`file:line`), complete code snippets, and verification commands.
5. **TDD / TEST-FIRST PRIORITY**: For logic-heavy features, mandate Test-First: `Write Test (RED) ➔ Implement (GREEN) ➔ Refactor ➔ Commit`.
6. **STOP FOR APPROVAL**: The implementation plan MUST be explicitly approved by user before transitioning to execution `/code`.

---

## 🔄 7-PHASE SYSTEMATIC PLAN FLOW

### PHASE 0: DEEP INTERVIEW
*   *Skip if user request already provides comprehensive context*.
*   If ambiguous: Ask **1 focused question per message** (do not overwhelm user with multi-part questions).
*   Offer 2 - 3 structured options with trade-offs to guide decisions.

### PHASE 1: UNDERSTAND & UNDERSTANDING LOCK (Hard Gate)
*   Initialize session: `hsa_session(action="intent", focus="plan: {feature}")`.
*   Survey landscape: `hsa_detect(stack)`, `hsa_explore(repo_map)`.
*   **🔒 UNDERSTANDING LOCK**: Summarize in 6 core points:
    1.  **Goal**: [One concise sentence]
    2.  **Target & Scale**: [Target users, expected load]
    3.  **Constraints**: [Language, framework, security invariants]
    4.  **Scope IN**: [Explicit features to implement]
    5.  **Scope OUT**: [Explicitly deferred features to prevent scope creep]
    6.  **Success Criteria**: [Concrete conditions for completion]
*   ⛔ **ASK USER**: *"Is this understanding accurate? Anything to adjust before technical design?"* ➔ **Proceed only upon explicit confirmation.**

### PHASE 2: IMPACT ANALYSIS & RISK MATRIX
*   Estimate complexity: `XS (<1h)` | `S (1-4h)` | `M (1-2d)` | `L (3-5d)` | `XL (>1w)`.
*   Catalogue affected files, new dependencies, potential breaking changes.
*   Construct Risk Matrix (Likelihood $\times$ Impact).

### PHASE 3: TECHNICAL DESIGN & CONTRACTS
*   Design architecture, data models, schemas, and API contracts.
*   Enforce YAGNI — select the simplest robust design.

### PHASE 4: BITE-SIZED TASK BREAKDOWN
*   Decompose plan into independent, bite-sized tasks with checkbox (`- [ ]`) steps.
*   Follow the standard atomic task template below.

### PHASE 5: VALIDATE & USER CONFIRMATION GATE (STOP)
*   Present complete implementation plan to user.
*   ⛔ **STOP**: Pause and wait for user's explicit approval before proceeding to `/code`.

### PHASE 6: PERSIST & SAVE
*   Save plan to: `.domyh/plans/YYYY-MM-DD_{feature_slug}/plan.md`.
*   If scope $\ge$ Size L: Also generate `impact.md` and `tasks.md`.
*   Update `active_plan` in `.agent/memory/state.json`.

---

## 🧱 ATOMIC TASK TEMPLATE (BITE-SIZED GRANULARITY)

```markdown
### Task 1: [Component / Module Name]
- **Target Files**: Create: `src/auth/token.ts` | Modify: `src/server.ts:45-60` | Tests: `tests/auth.test.ts`
- **Objective**: Implement JWT verification and secret key management.

- [ ] **Step 1 (Test RED)**: Write unit test for expired token in `tests/auth.test.ts`.
- [ ] **Step 2 (Run Test)**: Execute `pnpm test tests/auth.test.ts` (Verify test FAILS).
- [ ] **Step 3 (Implement GREEN)**: Add `verifyToken()` in `src/auth/token.ts`.
- [ ] **Step 4 (Read-Back Diff)**: Call `view_file` on `src/auth/token.ts` to verify syntax and diff.
- [ ] **Step 5 (Verify PASS)**: Run `pnpm test tests/auth.test.ts` (Verify 100% PASS).
- [ ] **Step 6 (Commit)**: `git commit -m "feat(auth): add jwt token verification"`.
```

---

## ⚡ SUB-COMMANDS

| Command | Description |
|:--------|:------------|
| `/plan [feature]` | Full 7-phase planning flow |
| `/plan quick [feature]` | Rapid plan for smaller tasks (skip Phase 0) |
| `/plan estimate [feature]` | Effort and sizing estimation (RICE / T-shirt) |
| `/plan list` | List saved plans in `.domyh/plans/` |
| `/plan open [slug]` | Open and resume execution of a saved plan |

---

## 🎯 [GATE 9: POST-FLIGHT PLANNING CHECKLIST — VERIFY BEFORE PRESENTING]

Before presenting plan to user, MUST self-audit these 5 golden criteria:
1.  ✅ **Has Understanding Lock been confirmed by user?**
2.  ✅ **Is every task broken down into 2-5 min atomic steps with exact file:line and commands?**
3.  ✅ **Is Scope OUT clearly documented to prevent scope creep?**
4.  ✅ **Are logic modules designed with Test-First / TDD sequencing?**
5.  ✅ **Is plan saved to `.domyh/plans/` and stopped for user approval?**

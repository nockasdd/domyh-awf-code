---
description: "Write production-ready code with double-ended rules, pre-read trace, post-read verification, and plan alignment"
skills: { required: [coding-rules], contextual: [auto, domyh-design, tailwind] }
success_criteria: "Pre-read verified, surgical change applied, post-read confirmed, build/tests passed, plan aligned"
---

# /code — Production Coding Workflow

## 🛡️ [GATE 0: PRE-FLIGHT HARD RULES — READ BEFORE CODING]

1. **NO BLIND WRITING**: NEVER write or modify code without reading the target file (`view_file` / `hsa_search`). Never act on assumptions.
2. **SURGICAL CHANGES**: Touch ONLY requested scope. Match existing style, syntax, and indentation 100%. No unsolicited refactoring ("clean only your own mess").
3. **SIZE SAFETY**: If changing >50 lines or creating >2 new files ➔ MUST STOP and confirm Implementation Plan with user.
4. **COMMENT POLICY**: Default NO comments describing WHAT (code explains itself). Only write concise comments for WHY (constraints, workarounds, surprises).
5. **READ-BACK MANDATE**: After EDITING any file, MUST read back the modified lines (`view_file`) to verify diff and syntax before proceeding.

---

## 🔄 6-PHASE SYSTEMATIC CODE FLOW

### PHASE 1: DISCOVER & ASSUMPTIONS
*   **Parse Intent**: Classify goal (`feature` | `bugfix` | `refactor` | `test` | `add`).
*   **Stack & Skill Detection**: Call `hsa_detect(stack)` and `hsa_search(query, action="skills")` to load appropriate patterns and rules.
*   **UI Intent**: If UI-related:
    *   New (T1): Load UI design skill.
    *   Modify (T2): Run design analysis.
    *   Complex (T3): Redirect to `/visualize`.
*   **Surface Assumptions**: State scope, format, technology choices, and constraints explicitly. STOP if ambiguous.

### PHASE 2: PRE-READ & TRACE FLOW (DRY Enforcement)
*   **Locate Target**: Pin exact file and line ranges to modify.
*   **Pre-Reading**: Call `view_file` to read full surrounding context (imports, interfaces, types, exports).
*   **Trace Flow**:
    *   If modifying function/class: Run `hsa_trace_flow(entry, direction:"both")` or grep callers to identify all dependents.
    *   If creating new code: Search `utils/`, `shared/`, `lib/` to reuse existing utilities before creating new ones.
*   **Edge Cases Gate**: Identify at least 3 test cases and 2 edge cases upfront.

### PHASE 3: SURGICAL IMPLEMENTATION & TDD
*   **TDD / Test-First**: For business logic or bug fixes, write reproducing test (RED) before implementation (GREEN).
*   **Precision Editing**:
    *   Use `replace_file_content` for localized chunk replacements.
    *   Use `write_to_file` when creating new standalone files.
*   **YAGNI & Simplicity**: Write minimum code that solves the problem. No speculative features.

### PHASE 4: POST-EDIT READ-BACK & DIFF VERIFICATION
*   **Mandatory Read-Back**: Call `view_file` on modified line ranges immediately after edit.
*   **Diff Quality Checklist**:
    *   [ ] Syntax, brackets, and indentation match existing file 100%?
    *   [ ] Zero unintended line removals or accidental whitespace changes?
    *   [ ] All new imports, types, variables properly declared and exported?
    *   [ ] Comment Policy respected (no redundant comments or version tags)?

### PHASE 5: RUN EVIDENCE & TEST LOOP
*   **Execution Evidence**: Run project test and build commands (`pnpm test`, `tsc --noEmit`, `pnpm build`, etc.).
*   **Auto Test Loop**: Edit ➔ Read-Back ➔ Test (Max 3 iterations).
*   **Escalation Gate**: If still failing after 3 attempts ➔ STOP immediately, analyze root cause via SCAMPER, and escalate to user.

### PHASE 6: PLAN & RULES PRE-REPORT AUDIT
*   **Plan Alignment**: Cross-check implemented code against every item in user request / approved Plan.
*   **Index Refresh**: Run `hsa_check_changes` to update Merkle tree and BM25F search index.
*   **Session Persistence**: Persist task summary via `hsa_session(action="persist")`.

---

## ⚡ SUB-COMMANDS

| Command | Mode | Description |
|:--------|:-----|:------------|
| `/code [task]` | Create / General | Implement new features or full module development |
| `/code fix [issue]` | Bugfix | Fix bugs: Reproduce ➔ Trace ➔ Surgical Fix ➔ Verify |
| `/code improve [area]` | Refactor | Code refactoring (requires 100% existing test pass) |
| `/code add [feature]` | Feature Extension | Add new endpoint, component, or sub-module |
| `/code test [feature]` | Test Suite | Write unit, integration, or E2E tests |

---

## 🤝 CASCADE & SUBAGENT DELEGATION

*   **Auto Cascade** (Complexity Score $\ge$ 6.5 or scope > 200 lines): Delegate to specialized subagents.
*   **Suggest Cascade** (Score 4.0 – 6.5 or scope 100 – 200 lines): Propose plan to user before decomposing.

---

## 🎯 [GATE 9: POST-FLIGHT CLOSING CHECKLIST — VERIFY BEFORE REPORTING]

Before sending final response to user, MUST self-audit these 5 golden questions:
1.  ✅ **Did I read target file BEFORE modifying?** *(With concrete file:line citations)*
2.  ✅ **Did I read back file AFTER modifying?** *(Confirmed clean diff and valid syntax)*
3.  ✅ **Did I execute real test/build commands for evidence?** *(Never say "should work")*
4.  ✅ **Do all changes trace 100% directly to the user's Plan?** *(No speculative code)*
5.  ✅ **Were Surgical Change and Comment Policy strictly respected?**

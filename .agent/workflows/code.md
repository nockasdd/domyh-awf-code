---
description: "💻 Write production-ready code, fix/improve existing projects, with proper error handling, types, and documentation"
skills: { required: [coding-rules], contextual: [auto, domyh-design, tailwind] }
success_criteria: "Feature implemented, build passes, tests written"
---

# 💻 /code — Code Pro

> Intelligent code generation & project improvement with language-specific patterns
> 📚 30+ Languages • Auto Test Loop • Fix/Improve Mode • Self-Review

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | Validate all user input, sanitize output | Security |
| R2 | No hardcoded secrets — use environment variables | Security |
| R3 | Parameterized queries only — no raw SQL | Security |
| R4 | Context-aware encoding, XSS prevention on output | Security |
| R5 | RBAC checks, secure sessions for auth | Security |
| R6 | Error handling at every boundary, non-revealing errors | Quality |
| R7 | Types/interfaces defined for all public APIs | Quality |
| R8 | Constants over magic numbers, named exports preferred | Quality |
| R9 | Tests written for all new code (>70% coverage target) | Quality |
| R10 | **Read + trace dependencies BEFORE modifying code** | Context |
| R11 | ⛔ STOP if major change (>50 lines) — confirm with user | Safety |

---

## CODE FLOW (6 Steps)

1. **DETECT** (Auto)
   - Parse intent: feature / bugfix / refactor
   - `hsa_detect(stack)` → languages, frameworks
   - `hsa_search(skills)` → load language-specific patterns
   - **UI Intent**: T1 (new UI) → load `domyh-design` skill | T2 (modify UI) → `hsa_design(analyze)` | T3 (design-only) → route to `/visualize`

2. **PLAN**
   - Break down into steps, identify dependencies
   - `hsa_prefetch` planned files
   - Show: `Plan: 4 steps, ~85 lines`
   - ⛔ STOP if major change (>50 lines) — confirm with user
   - **If UI** (T1/T2): `hsa_canvas(open)` → preview → ⛔ STOP: "Preview ready. Approve?"

3. **PRE-IMPLEMENTATION CHECK** (Hard Gate)
   > Verifiable actions — NOT self-reported checkboxes.

   ```
   1. Read original requirement → quote key criteria in output
   2. List planned test cases (minimum 3)
   3. List edge cases (minimum 2: empty/null/boundary)
   4. If touching auth/secrets → log security review notes
   5. If breaking changes → list affected consumers with file:line
   ⛔ Missing items = address before coding. Show: `Pre-check: 5/5 ✅`
   ```

4. **EXECUTE** — Context-Aware Implementation

   **Context Gathering Protocol** (MANDATORY before writing code):
   ```yaml
   mandatory:
     - "Read target file(s) BEFORE editing — never edit blind"
     - "hsa_trace_flow(entry_point) for functions being modified"
     - "Check imports/exports — what depends on this code?"
   conditional:
     - "If modifying API → hsa_search for all consumers"
     - "If modifying types/interfaces → hsa_search for all usages"
     - "If modifying config → check all environment variants"
     - "If modifying shared utility → trace upstream + downstream"
   ```

   **Canonical Write Protocol** (from AGENT_BEHAVIOR.md):
   LOCATE → UNDERSTAND → SIZE → WRITE → VERIFY
   - SIZE classification from `proportional-response.yaml` determines output scope
   - Write code following skill patterns, error handling + types
   - Add tests (auto test loop: write → run → fix → repeat, max 3)
   - Show progress: `[Step 2/4] Creating auth middleware...`

5. **VERIFY** — Run tests → Fix → Repeat (max 3), lint check
   - Agent re-reads ALL generated code and checks:
     Intent match? Edge cases? No magic numbers? Helpful errors? Naming conventions? No security anti-patterns?
   - If issues found → fix silently before output
   - **UI Quality Gate** (if UI intent):
     Visual QA Pipeline (score /100): Accessibility (30pts) + Visual Consistency (25pts) + Responsiveness (20pts) + Interaction (15pts) + Performance (10pts)
     Nielsen Heuristic Check: ≥8/10
     Result: ≥90 → SHIP ✅ | 70-89 → FIX MINOR ⚠️ | <70 → REDESIGN ❌
     Bonus: `hsa_design(health)` → Grade (A-F) | `hsa_canvas(capture)` → CLS, AX tree, console errors

6. **SYNC**
   - `hsa_check_changes` to update index
   - `hsa_feedback` on key files used
   - Output: summary of changes, confidence score (1-10), next steps
   - Persist key decisions to `.agent/memory/state.json`

---

## SUB-COMMANDS

| Command | Description | Mode |
|:--------|:------------|:-----|
| `/code [task]` | Generate code for task | Create |
| `/code fix [issue]` | Fix existing issue | Fix |
| `/code improve [area]` | Improve existing code | Refactor |
| `/code add [feature]` | Add feature to existing | Update |
| `/code test [feature]` | Generate tests only | Test |
| `/code secure [feature]` | Generate secure code | Create |
| `/code quality analyze [path]` | Static analysis | Analyze |

---

## FIX/IMPROVE MODE

DETECT → ANALYZE issue → PLAN fix → EXECUTE → VERIFY → SELF-REVIEW → SUMMARY

| Priority | Description | SLA | Action |
|:---------|:------------|:----|:-------|
| **P0** | Critical security/breaking | Immediate | Must fix now |
| **P1** | Affects core functionality | Same session | Fix before next task |
| **P2** | Code quality/maintainability | This sprint | Schedule fix |
| **P3** | Nice to have improvements | Backlog | Track |

---

## AI QUALITY GATES

| Layer | Name | What |
|:------|:-----|:-----|
| 1 | AI Auto-Fix | Linting, formatting, naming, comments |
| 2 | Static Analysis | Snyk, SonarQube, ESLint; cyclomatic < 10 |
| 3 | Self-Review | Agent self-critique before delivery |
| 4 | Human Review | Complex logic, security, infra, >100 lines |

---

## CASCADE EVALUATION (MCP)

> ⚠️ Evaluate before EXECUTE — see `delegation-intelligence` skill for scoring.

```
hsa_delegate({action:'cascade', cascade_text:'[prompt]', task_type:'code'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
```
**Auto-cascade** (score ≥6.5): >200 LOC, multi-file, complex algorithm
**Suggest cascade** (score 4.0-6.5): >100 LOC, moderate multi-file

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

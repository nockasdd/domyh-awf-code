---
description: "⚡ Quick-fix pipeline: capture error → identify → fix → verify (max 60s)"
skills: { required: [error-handling], contextual: [auto] }
success_criteria: "Error resolved, build passes, no regressions"
---

# ⚡ /fix — Fix Pro

> Fast, Targeted Error Resolution
> 📚 Single-Pass Fix • Auto-Retry • Max 60s

---

## FIX FLOW

1. **DETECT** (5s) — `hsa_session("quick fix: {error_summary}")`, parse error, detect stack via HSA (`hsa_detect`), load context (`hsa_search`), locate file + line, read surrounding code, classify fix category
   - **UI FIX DETECTED?** → `hsa_design_analyze({scope: "component", paths: [affected_file]})` → understand design context before fixing
   - **VISUAL FIX?** (layout/color/style changes) → generate before/after `.preview/{fix}.html` → open with `browser_subagent` → screenshot comparison → confirm with user
2. **EXECUTE** (30s) — Apply targeted fix, minimal changes only, preserve existing behavior
3. **VERIFY** (15s) — Build/syntax check, run affected tests. **If UI fix**: `hsa_design_health()` → verify design Grade stable. → If FAIL: retry (max 2) → If still FAIL: escalate to `/debug`
4. **SYNC** — `hsa_check_changes` to update index after edits

---

## COMMANDS

| Command        | Description             | Speed     |
| -------------- | ----------------------- | --------- |
| `/fix [error]` | Fix specific error      | ⚡ Fast   |
| `/fix last`    | Fix last terminal error | ⚡ Fast   |
| `/fix build`   | Fix build errors        | ⚡ Fast   |
| `/fix lint`    | Fix all lint errors     | ⚡ Fast   |
| `/fix types`   | Fix type errors         | ⚡ Fast   |
| `/fix imports` | Fix import errors       | ⚡ Fast   |
| `/fix tests`   | Fix failing tests       | 🔧 Medium |

---

## ⚡ vs 🐛 When to use /fix vs /debug?

| Use `/fix` when                               | Use `/debug` when                        |
| --------------------------------------------- | ---------------------------------------- |
| Clear error message (compile, type, import)   | Complex logic error, unclear root cause  |
| Know which file has the error                  | Runtime error intermittent               |
| Simple fix (< 10 lines)                        | Need root cause analysis                 |
| Need quick fix to unblock                      | Multiple files involved                  |
| —                                              | `/fix` failed after 2 attempts           |

---

## 🔧 FIX CATEGORIES

| Category    | Detect Pattern                          | Approach                       | Confidence |
| ----------- | --------------------------------------- | ------------------------------ | ---------- |
| Syntax      | SyntaxError, unexpected token           | Auto-fix syntax                | 95%        |
| Types       | TypeError, type mismatch, TS errors     | Add/update types               | 90%        |
| Imports     | ModuleNotFoundError, Cannot find module | Fix paths, add missing         | 95%        |
| Null safety | Cannot read property of null/undefined  | Null checks, optional chaining | 85%        |
| Build       | Build failed, compilation error         | Fix config, missing deps       | 80%        |
| Lint        | ESLint, golangci-lint, ruff             | Auto-fix or recommended        | 90%        |
| Dependency  | Version mismatch, peer dependency       | Update/install correct         | 85%        |

---

## 🎨 UI FIX CATEGORY

| Category  | Detect Pattern                                | Additional Steps                      |
| --------- | --------------------------------------------- | ------------------------------------- |
| CSS/Style | overflow, z-index, opacity, display, visible  | Load design tokens, check dark mode   |
| Layout    | flex/grid, position, float, alignment         | Verify responsive (mobile + desktop)  |
| Color     | color, background, gradient, contrast         | Verify WCAG contrast ≥ 4.5:1         |
| Font      | font-size, line-height, font-family           | Check typography scale compliance     |
| Animation | transition, transform, keyframes              | Check prefers-reduced-motion          |
| Dark Mode | dark: prefix, color-scheme, theme toggle      | Test both modes after fix             |

When UI fix detected → auto-load `domyh-design` skill, run `hsa_design_analyze({scope: "component"})`, apply UI quality checks. After fix → `hsa_design_health()` to verify no design regression.

---

## 🔄 ESCALATION

After 2 retries fail → activate **Progressive Escalation** (`rules/modules/progressive-escalation.yaml`):

1. 🪞 **REFLECT** — List all attempts in a table (# | Approach | Result | Why fail). Check 3 biases: Confirmation (only seeking supporting evidence?), Anchoring (same hypothesis unchanged?), Tunnel Vision (only modifying code, ignoring config/env/deps?)
2. 🔄 **REFRAME** — Invert: "If ALL code is correct, where does the bug come from?" Rubber Duck: explain expected vs actual flow step-by-step. Devil's Advocate: "Could my fix cause NEW problems?"
3. 🔍 **WIDEN** — Checklist: code ✓ config ✓ env ✓ deps ✓ data ✓ logs ✓. Run: `git log --oneline -10` for recent changes, check lockfile versions, verify env variables
4. 🧩 **DECOMPOSE** — Create minimal reproduction (smallest code that triggers bug). Binary search: comment out half the code, narrow to exact line
5. 👤 **ESCALATE** — Full report to user: error message, all attempts tried, evidence collected, 2-3 recommended actions

> Use `templates/reflection/pivot_analysis.md` for structured analysis at each level.
> Check episodic memory (`.domyh/debug/episodic_memory.yaml`) before retrying.

---

## 💡 EXAMPLE

<example>
User: "TypeError: Cannot read properties of undefined at auth.ts:42"
→ DETECT: Null reference in `user.session` at auth.ts:42
→ FIX: Add optional chaining: `user?.session?.token`
→ VERIFY: Build ✅ | Tests ✅ (auth.test.ts: 12/12)
</example>

---

## ⛔ SAFETY

- Max changed files: 3
- Max changed lines: 30
- Require confirmation if: > 3 files, > 30 lines, modifies test/config files

---

## 🔄 CASCADE DELEGATION (Optional — MCP)

For complex fix patterns, delegate to specialized model via cascade:
```
hsa_delegate({action:'cascade', cascade_text:'[detailed prompt]', task_type:'debug'})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
→ repeat cascade_read (3-5s intervals, max 10 polls)
```
Model auto-selected from user's dashboard routing. Use when:
- Fix requires deep analysis after 2 retry failures
- Multi-file fix pattern affecting >3 files
- User has configured stronger model for `debug` task_type

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...], auto_notify:true})`
   - If key decision → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`


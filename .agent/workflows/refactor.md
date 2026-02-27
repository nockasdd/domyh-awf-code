---
description: "🔧 Code refactoring & cleanup: identify smells, clean dead code, organize imports, restructure — verify tests pass"
skills: { required: [coding-rules], contextual: [auto, domyh-design] }
success_criteria: "Code improved, all tests pass, no behavior change"
---

# 🔧 /refactor — Refactor Pro

> Safe Code Transformation with Test Verification
> 📚 Code Smells • Analysis Tools • Characterization Tests

---

## REFACTOR FLOW

1. **DETECT** — `hsa_declare_intent("refactor: {target}")`, identify stack via HSA (`hsa_detect_stack`), load context (`hsa_get_context`), locate tests
2. **BASELINE** — Run tests, record passing state
3. **PLAN** — Define changes, confirm scope → `hsa_prefetch` target files
4. **EXECUTE** — Apply refactoring (one commit per change) → ⛔ STOP if tests fail at any point
5. **VERIFY** — Re-run tests, validate behavior unchanged
6. **SYNC** — `hsa_check_changes` to update index after edits

---

## COMMANDS

| Command                   | Description             |
| ------------------------- | ----------------------- |
| `/refactor [file]`        | Refactor specific file  |
| `/refactor [dir]`         | Refactor directory      |
| `/refactor extract`       | Extract method/function |
| `/refactor rename`        | Rename with references  |
| `/refactor simplify`      | Reduce complexity       |
| `/refactor clean imports` | Organize imports        |
| `/refactor clean dead`    | Remove dead code        |
| `/refactor clean all`     | Apply all cleanup       |
| `/refactor clean --dry`   | Preview without changes |

### Cleanup Safety Rules

- Preview changes before any deletion
- Show exact lines before removal
- Offer backup (`git stash`)
- Run build after changes
- Confirm before removing: deprecated functions, TODO files, test files, configs, migrations

---

## 🎨 UI REFACTOR SUB-COMMANDS

| Command                    | Description               | What It Does                                        |
| -------------------------- | ------------------------- | --------------------------------------------------- |
| `/refactor ui [component]` | Refactor UI component     | Break down, clean props, extract sub-components     |
| `/refactor layout [page]`  | Restructure page layout   | Reorganize grid/flex structure, simplify nesting    |
| `/refactor styles`         | Clean/organize CSS        | Remove dead CSS, merge duplicates, organize imports |
| `/refactor design-system`  | Migrate to design tokens  | Extract hardcoded values → CSS custom properties    |
| `/refactor responsive`     | Fix/add responsive design | Add container queries, fix breakpoints, fluid typo  |
| `/refactor a11y`           | Fix accessibility issues  | Add ARIA labels, fix contrast, keyboard navigation  |

### UI Refactor Flow (with VRT Baseline)

> Extends standard 6-step flow with screenshot comparison

1. **DETECT** — Stack + scan UI component structure + `hsa_design_analyze({scope: "full"})` → read Design DNA
2. **BASELINE** — Run tests + capture current screenshot (Playwright `toHaveScreenshot()`)
3. **PLAN** — Define UI changes using DNA insights (identify hardcoded values, low token adoption, missing a11y). For `/refactor design-system`: `hsa_design_tokens({format: "css"})` → get migration plan. → ⛔ **STOP — confirm before executing**
4. **EXECUTE** — Apply refactoring (one commit per change)
5. **COMPARE** — Screenshot after → pixelmatch diff → show visual delta
6. **VERIFY** — Tests pass + `hsa_design_health({strict: true})` → compare score before/after + a11y check + responsive check
7. **SYNC** — `hsa_check_changes` to update index

---

## CODE SMELLS CATALOG

### Bloaters (Size Issues)

| Smell               | Detect                | Fix              |
| ------------------- | --------------------- | ---------------- |
| Long Method         | > 20 lines            | Extract Method   |
| Large Class         | > 200 lines           | Extract Class    |
| Long Parameter List | > 3 params            | Parameter Object |
| Data Clumps         | Repeated field groups | Extract Class    |
| Primitive Obsession | Raw types everywhere  | Value Objects    |

### Change Preventers

| Smell                | Detect                        | Fix                       |
| -------------------- | ----------------------------- | ------------------------- |
| Divergent Change     | One class, many reasons       | SRP, Extract Class        |
| Shotgun Surgery      | One change → many files       | Move Method, Inline Class |
| Parallel Inheritance | Subclass in A → subclass in B | Merge hierarchies         |

### Dispensables

| Smell                  | Detect              | Fix                  |
| ---------------------- | ------------------- | -------------------- |
| Duplicate Code         | Copy-paste          | Extract Method/Class |
| Dead Code              | Unreachable         | Remove               |
| Speculative Generality | Unused abstractions | Collapse Hierarchy   |

### Couplers

| Smell                  | Detect                           | Fix                          |
| ---------------------- | -------------------------------- | ---------------------------- |
| Feature Envy           | Method uses another class's data | Move Method                  |
| Inappropriate Intimacy | Classes access internals         | Extract Class, Hide Delegate |

---

## REFACTORING PATTERNS

| Pattern                    | When                        | Example                                     |
| -------------------------- | --------------------------- | ------------------------------------------- |
| Extract Method             | Mixed logic in one function | Split into validateInput(), transformData() |
| Replace Magic Numbers      | Hardcoded values            | `STATUS_ACTIVE = 1`, `TIMEOUT_MS = 30000`   |
| Replace Conditional        | Complex if/else chains      | Strategy pattern, polymorphism              |
| Introduce Parameter Object | Many params                 | `CreateUserInput { name, email, role }`     |
| Replace Temp with Query    | Temp var used once          | Inline as method call                       |

---

## ANALYSIS TOOLS

| Language   | Complexity        | Duplication | Lint             |
| ---------- | ----------------- | ----------- | ---------------- |
| Go         | gocyclo           | dupl        | golangci-lint    |
| TypeScript | eslint complexity | jscpd       | eslint           |
| Python     | radon cc          | pylint      | ruff             |
| Rust       | cargo clippy      | —           | clippy           |
| Java       | PMD               | CPD         | Checkstyle       |
| C#         | —                 | —           | Roslyn analyzers |

---

## COMPLEXITY THRESHOLDS

| Metric          | Good | Warning | Critical |
| --------------- | ---- | ------- | -------- |
| Cyclomatic      | < 10 | 10-20   | > 20     |
| Cognitive       | < 15 | 15-25   | > 25     |
| Lines/function  | < 30 | 30-50   | > 50     |
| Params/function | ≤ 3  | 4-5     | > 5      |
| Nesting depth   | ≤ 3  | 4       | > 4      |
| Duplication     | < 3% | 3-10%   | > 10%    |

---

## CHARACTERIZATION TESTS

> For legacy code without tests — document existing behavior before refactoring

1. Run code with known inputs
2. Record actual outputs (even if "wrong")
3. Write tests capturing current behavior
4. Now refactor safely — tests catch regressions

### Mikado Method (Large Refactors)

1. Make one refactoring
2. Run tests → Pass? Commit. Fail? Revert.
3. Repeat

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
2. **PERSIST** — Update session memory:
   - Append task summary to `memory/session.md` (per SESSION_005 format)
   - If key decision made → append to `memory/decisions.md`
3. **SNAPSHOT** — If this is the last task in session:
   - Update `memory/CONTEXT_SNAPSHOT.md` (Recent Changes, Status, Decisions)
4. **ANCHOR** (if HSA available):
   - `hsa_track_progress(level: "action", label: "[workflow] completed", status: "completed")`
   - `hsa_save_anchor(content: "[SESSION] Done: [summary]. Files: [list].", category: "context")`


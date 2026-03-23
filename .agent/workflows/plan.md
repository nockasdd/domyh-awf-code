---
description: "📋 Feature planning with impact analysis, task breakdown, and effort estimation"
skills: { required: [], contextual: [auto] }
success_criteria: "plan approved by user, tasks broken down, saved to .domyh/plans/"
---

# 📋 /plan — Plan Pro

> Outcome-Focused Feature Planning
> 📚 Impact Analysis • Task Breakdown • RICE Scoring

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | All design decisions MUST cite evidence (codebase analysis, research) | Quality |
| R2 | ⛔ STOP before Phase 3 (Design) — UNDERSTANDING LOCK must pass | Safety |
| R3 | Scope creep guard: if new requirement surfaces during design → document in Scope OUT, don't silently expand | Anti-Drift |
| R4 | ONE question per message during interview — don't overwhelm user | UX |

---

## PLAN FLOW (7 Phases)

1. **PHASE 0: DEEP INTERVIEW** — Gather context (skip if clear) → ⛔ STOP if info missing
   - ONE question per message — wait for answer before next
   - Present 2-3 options with tradeoffs for design decisions → wait

2. **PHASE 1: UNDERSTAND** — `hsa_session("plan feature: {name}")`, parse request, detect stack (`hsa_detect`), load context (`hsa_search(output_mode='references')`), `hsa_explore(repo_map)`, clarify scope
   > **UNDERSTANDING LOCK** (Hard Gate — MUST pass before Phase 3):
   > Summarize understanding in 5-7 bullets: Goal, Users, Constraints, Scope IN, Scope OUT, Dependencies, Success criteria
   > Ask: **"Is this understanding correct? Anything to add/change?"**
   > ⛔ Only proceed after explicit confirmation. Skip = restart Phase 0.

3. **PHASE 2: ANALYZE** — Impact assessment, risk analysis, dependencies. `hsa_prefetch` target files.
   - Consider using `/think analyze` for multi-perspective impact analysis
   - Consider using `/think tradeoff` for approach comparison

4. **PHASE 3: DESIGN** — Technical design, architecture, API contracts. Propose 2-3 approaches → get user approval on direction

5. **PHASE 4: BREAKDOWN** — Task decomposition (bite-sized granularity), effort estimation → ⛔ STOP for user approval

6. **PHASE 5: VALIDATE** — Review with user, finalize plan
   - Optional: dispatch cascade reviewer (`hsa_delegate(cascade)`) for plan quality check

7. **PHASE 6: PERSIST** — Save to `.domyh/plans/YYYY-MM-DD_{slug}/plan.md`. If scope ≥ L: also save `impact.md` and `tasks.md`. Update `.agent/memory/state.json → active_plan`. Show: `📁 Saved: .domyh/plans/{date}_{slug}/`

---

## SCOPE CHECK

If spec covers multiple independent subsystems → suggest breaking into separate plans — one per subsystem. Each plan should produce working, testable software on its own.

---

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/plan [feature]` | Full planning flow |
| `/plan quick [feature]` | Rapid plan (skip Phase 0) |
| `/plan estimate [feature]` | Effort estimation only |
| `/plan specify [feature]` | Spec-driven (DoR + INVEST) |
| `/plan sprint` | Sprint planning (DoD/DoR) |
| `/plan uat [feature]` | UAT scenario planning |
| `/plan flow [sprint]` | Flow metrics for sprint |
| `/plan forecast [n]` | Forecast n items |
| `/plan list` | List saved plans in `.domyh/plans/` |
| `/plan open [slug]` | Open a saved plan |
| `/plan compare [a] [b]` | Compare two plan versions |

---

## PLAN DOCUMENT HEADER (Mandatory)

Every plan MUST start with:
```markdown
# [Feature Name] Implementation Plan
> **For agentic workers:** Use cascade-review skill for QA. Steps use checkbox syntax.
**Goal:** [One sentence] | **Architecture:** [2-3 sentences] | **Tech Stack:** [Key tech]
```

---

## BITE-SIZED TASK GRANULARITY

**Each step = ONE action (2-5 minutes):**

```markdown
### Task N: [Component Name]
**Files:** Create: `path/file.ts` | Modify: `path/existing.ts:123-145` | Test: `tests/file.test.ts`
- [ ] Step 1: [Concrete action with complete code, not "add validation"]
- [ ] Step 2: [Exact command with expected output]
- [ ] Step 3: [Commit]
```

**TDD Pattern** (recommended for logic-heavy code):
`Write test → Run → Fail → Implement → Run → Pass → Commit`

**Implementation First** (for config, docs, CI/CD, non-testable):
`Implement → Verify manually → Commit`

**Rules:** Exact file paths • Complete code • Exact commands • DRY, YAGNI

---

## PHASE 0: DEEP INTERVIEW

> Skip if user already provided enough context

### 3 Golden Questions

| # | Question | Purpose | Skip If |
|:--|:---------|:--------|:--------|
| 1 | What does this feature handle/manage? | Domain & scope | Request clear |
| 2 | Who uses it? How many users? | Scale & UX | Obvious |
| 3 | Any constraints? (deadline, budget, tech) | Boundaries | None |

**Follow-up:** Technical (endpoints? DB changes? perf reqs?) | Business (priority? deadline? success metrics?)

---

## IMPACT ANALYSIS

| Factor | Assessment | Notes |
|:-------|:-----------|:------|
| Code complexity | S/M/L/XL | {detail} |
| Files affected | {count} | {list} |
| Dependencies | {count} | {list} |
| Breaking changes | Yes/No | {detail} |
| Security impact | Low/Med/High | {detail} |

### Risk Matrix

|  | Low Likelihood | Medium | High |
|:--|:---------------|:-------|:-----|
| **High Impact** | 🟡 | 🔴 | 🔴 |
| **Med Impact** | 🟢 | 🟡 | 🔴 |
| **Low Impact** | 🟢 | 🟢 | 🟡 |

---

## TASK BREAKDOWN & ESTIMATION

| Size | Time | Examples |
|:-----|:-----|:---------|
| **XS** | < 1h | Config change, copy fix |
| **S** | 1-4h | Simple endpoint, UI tweak |
| **M** | 4h-2d | Feature with tests |
| **L** | 2-5d | Multi-component feature |
| **XL** | 1-2w | Cross-cutting feature |
| **XXL** | 2w+ | **Needs breakdown** |

> Include: testing (20-30%), buffer (10-20%), review time

---

## RICE SCORING

> Agent facilitates RICE scoring conversation — requires user estimates for Reach and Effort.

| Factor | Scale | Description |
|:-------|:------|:------------|
| **R**each | Number | Users affected per quarter |
| **I**mpact | 0.25-3 | 0.25=minimal → 3=massive |
| **C**onfidence | 0-100% | How sure about estimates |
| **E**ffort | Person-months | Dev time required |

> Formula: `(R × I × C) / E` → Higher = prioritize

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

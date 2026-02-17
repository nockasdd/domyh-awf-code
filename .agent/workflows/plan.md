---
description: "📋 Feature planning with impact analysis, task breakdown, and effort estimation"
skills: { required: [], contextual: [auto] }
---

# 📋 /plan — Plan Pro

> Outcome-Focused Feature Planning
> 📚 Impact Analysis • Task Breakdown • RICE Scoring

---

## PLAN FLOW

1. **PHASE 0: DEEP INTERVIEW** — Gather context (skip if clear) → ⛔ STOP if info missing
2. **PHASE 1: UNDERSTAND** — Parse request, detect stack via HSA (`hsa_detect_stack`), load context (`hsa_get_context` with `output_mode='references'` for quick overview), use `hsa_get_repo_map` for codebase overview, clarify scope
3. **PHASE 2: ANALYZE** — Impact assessment, risk analysis, dependencies. `hsa_prefetch` target files for deep analysis
4. **PHASE 3: DESIGN** — Technical design, architecture, API contracts
5. **PHASE 4: BREAKDOWN** — Task decomposition, effort estimation → ⛔ STOP for user approval
6. **PHASE 5: VALIDATE** — Review with user, finalize plan
7. **PHASE 6: PERSIST** — Save to `.domyh/plans/YYYY-MM-DD_{feature-slug}/plan.md`. If scope ≥ L, also save `impact.md` and `tasks.md`. Update `.agent/memory/state.json` → `phase_progress.active_plan`. Show: `📁 Saved: .domyh/plans/2026-02-12_payment-gateway/`

---

## COMMANDS

| Command                    | Description                         |
| -------------------------- | ----------------------------------- |
| `/plan [feature]`          | Full planning flow                  |
| `/plan quick [feature]`    | Rapid plan (skip Phase 0)           |
| `/plan estimate [feature]` | Effort estimation only              |
| `/plan flow [sprint]`      | Flow metrics for sprint             |
| `/plan forecast [n]`       | Forecast n items                    |
| `/plan specify [feature]`  | Spec-driven (DoR + INVEST)          |
| `/plan sprint`             | Sprint planning (DoD/DoR)           |
| `/plan uat [feature]`      | UAT scenario planning               |
| `/plan list`               | List saved plans in `.domyh/plans/` |
| `/plan open [slug]`        | Open a saved plan                   |
| `/plan compare [a] [b]`    | Compare two plan versions           |

---

## PLAN OUTPUT

```yaml
output:
  base: ".domyh/plans/"
  structure: "YYYY-MM-DD_{feature-slug}/"
  files:
    plan.md: "Main plan (always created)"
    impact.md: "Impact analysis (when scope ≥ L)"
    tasks.md: "Task breakdown (when scope ≥ L)"
  naming:
    slug: "kebab-case from plan title, max 30 chars"
    example: ".domyh/plans/2026-02-12_payment-gateway/"
  active_ref: "Update .agent/memory/state.json → phase_progress.active_plan"
  memory_sync: "Update .agent/memory/state.json with plan metadata"
```

---

## PHASE 0: DEEP INTERVIEW ⭐

> Skip if user already provided enough context

### 3 Golden Questions

| #   | Question                                     | Purpose          | Skip If                |
| --- | -------------------------------------------- | ---------------- | ---------------------- |
| 1   | What does this feature handle/manage?         | Domain & scope   | Request already clear   |
| 2   | Who uses it? How many users?                  | Scale & UX needs | Obvious from context    |
| 3   | Any constraints? (deadline, budget, tech)     | Boundaries       | No special constraints  |

### Follow-up Categories

| Category  | Key Questions                                     |
| --------- | ------------------------------------------------- |
| Technical | Existing endpoints? DB changes? Performance reqs? |
| Business  | Priority? Hard deadline? Success metrics?         |

---

## IMPACT ANALYSIS

| Factor           | Assessment   | Notes    |
| ---------------- | ------------ | -------- |
| Code complexity  | S/M/L/XL     | {detail} |
| Files affected   | {count}      | {list}   |
| Dependencies     | {count}      | {list}   |
| Breaking changes | Yes/No       | {detail} |
| Security impact  | Low/Med/High | {detail} |

### Risk Matrix

|                 | Low Likelihood | Medium | High |
| --------------- | -------------- | ------ | ---- |
| **High Impact** | 🟡             | 🔴     | 🔴   |
| **Med Impact**  | 🟢             | 🟡     | 🔴   |
| **Low Impact**  | 🟢             | 🟢     | 🟡   |

---

## TASK BREAKDOWN & ESTIMATION

### Effort Scale

| Size    | Time  | Examples                  |
| ------- | ----- | ------------------------- |
| **XS**  | < 1h  | Config change, copy fix   |
| **S**   | 1-4h  | Simple endpoint, UI tweak |
| **M**   | 4h-2d | Feature with tests        |
| **L**   | 2-5d  | Multi-component feature   |
| **XL**  | 1-2w  | Cross-cutting feature     |
| **XXL** | 2w+   | **Needs breakdown**       |

> Estimation rules: Include testing (20-30%), buffer (10-20%), code review time

---

## RICE SCORING

| Factor         | Scale         | Description                                        |
| -------------- | ------------- | -------------------------------------------------- |
| **R**each      | Number        | Users affected per quarter                         |
| **I**mpact     | 0.25-3        | 0.25=minimal, 0.5=low, 1=medium, 2=high, 3=massive |
| **C**onfidence | 0-100%        | How sure about estimates                           |
| **E**ffort     | Person-months | Dev time required                                  |

> Formula: `(R × I × C) / E` → Higher = prioritize
---

## SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`

---
description: "🏗️ Feature lifecycle: scaffold docs, implement with traceability, enforce SDLC phases"
skills: { required: [coding-rules], contextual: [auto] }
success_criteria: "All ACs verified via traceability matrix, phase docs complete"
---

# 🏗️ /feature — Feature Lifecycle Pro

> Spec-Driven Feature Development with Phase Gates
> 📚 Requirements → Design → Plan → Implement → Test → Ship
> ⭐ Traceability: AC → Task → Code → Test (full chain)

---

## FEATURE FLOW

1. **PHASE 0: CONTEXT** — `hsa_session("implement feature: {name}")`, detect stack via HSA (`hsa_detect`), gather codebase context (`hsa_search`), repo map (`hsa_explore`), understand existing patterns
2. **PHASE 1: REQUIREMENTS** — Define problem, user stories (INVEST), acceptance criteria (AC-xxx), constraints, out-of-scope → Scaffold `docs/features/{slug}/requirements.md` → ⛔ STOP for user approval
3. **PHASE 2: DESIGN** — Architecture decisions (ADR-xxx format), data models, API contracts, risk matrix → Create `design.md` with decision records → ⛔ STOP if breaking changes
4. **PHASE 3: PLANNING** — Task breakdown with traceability (T-xxx → AC-xxx), effort estimation (XS-XXL), dependency graph, RICE scoring → Create `planning.md` → ⛔ STOP for user approval
5. **PHASE 4: IMPLEMENTATION** — Execute tasks per plan, log decisions in `implementation.md`, `hsa_check_changes` after each milestone. Each code change references task ID (T-xxx)
6. **PHASE 5: TESTING** — Write tests per `testing.md` strategy, run coverage check, validate all ACs met → Update test results
7. **PHASE 6: SHIP** — Create summary, update `implementation.md` with final status, verify all phase docs complete, run `/verify` for final gate
8. **PHASE 7: SYNC** — `hsa_check_changes` to update index after all feature files created

---

## COMMANDS

| Command                     | Description                       |
| --------------------------- | --------------------------------- |
| `/feature [name]`           | Full lifecycle (Phase 0-6)        |
| `/feature spec [name]`      | Spec-only (Phase 0-3, no code)    |
| `/feature implement [slug]` | Resume from existing spec         |
| `/feature status [slug]`    | Show phase progress               |
| `/feature list`             | List features in `docs/features/` |

---

## FEATURE OUTPUT

```yaml
output:
  base: "docs/features/"
  structure: "{feature-slug}/"
  files:
    requirements.md: "Problem statement, user stories, ACs (Phase 1)"
    design.md: "Architecture, ADRs, data models (Phase 2)"
    planning.md: "Task breakdown, effort, dependencies (Phase 3)"
    implementation.md: "Code log, decisions, file changes (Phase 4)"
    testing.md: "Test strategy, cases, coverage results (Phase 5)"
  naming:
    slug: "kebab-case from feature name, max 30 chars"
    example: "docs/features/jwt-auth/"
```

---

## PHASE GATES

> Spec-driven development: requirements MUST be approved before code starts

| Gate | Trigger              | Requires      | Blocks      |
| ---- | -------------------- | ------------- | ----------- |
| G1   | After Phase 1 (Req)  | User approval | Phase 4,5,6 |
| G2   | After Phase 3 (Plan) | User approval | Phase 4     |
| G3   | After Phase 5 (Test) | All ACs pass  | Phase 6     |

### Gate Rules

- G1 (mandatory): Cannot write feature code without approved requirements
- G2 (recommended): Skip with `/feature --no-plan-gate`
- G3 (automated): ACs verified by test results

### Lightweight Mode (XS-S tasks)

For tasks estimated XS-S (< 4h), use streamlined flow:
- **Skip Phase 2 (Design)** — no ADR needed for trivial changes
- **Skip Phase 3 (Planning)** — go from requirements to implementation
- **Combine Phase 5+6** — test and ship in one step
- Triggered by: effort estimate ≤ S, or user flag `--quick`

---

## TRACEABILITY MATRIX

```
AC-001 ←→ T-001 ←→ file:50 ←→ TC-001
   ↓           ↓           ↓           ↓
Requirement   Task    Implementation  Test Case
```

| Source | Links To          | Format             |
| ------ | ----------------- | ------------------ |
| AC-xxx | T-xxx, TC-xxx     | `Ref: AC-001`      |
| T-xxx  | AC-xxx, file:line | `Task: T-001`      |
| DD-xxx | AC-xxx            | `Decision: DD-001` |
| TC-xxx | AC-xxx            | `Covers: AC-001`   |

---

## EFFORT ESTIMATION

| Size    | Time  | Examples                    |
| ------- | ----- | --------------------------- |
| **XS**  | < 1h  | Config change, copy fix     |
| **S**   | 1-4h  | Simple endpoint, UI tweak   |
| **M**   | 4h-2d | Feature with tests          |
| **L**   | 2-5d  | Multi-component feature     |
| **XL**  | 1-2w  | Cross-cutting feature       |
| **XXL** | 2w+   | **Needs breakdown → /plan** |

> Include: testing (20-30%), buffer (10-20%), review time

---

## INTEGRATION

| Related Command | When to Use                       |
| --------------- | --------------------------------- |
| `/plan`         | Complex planning (RICE scoring)   |
| `/scaffold`     | Generate boilerplate files        |
| `/code`         | Implementation (Phase 4)          |
| `/test`         | Test writing (Phase 5)            |
| `/verify`       | Final verification gate (Phase 6) |
| `/review`       | Code review before merge          |

---

## ⛔ SAFETY

- Complete Phase 1 gate (requirements approval) before proceeding
- Confirm before overwriting existing feature docs
- Warn if feature scope exceeds XL (suggest breakdown)
- All code changes must reference task IDs
- Log all architecture decisions in design.md

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


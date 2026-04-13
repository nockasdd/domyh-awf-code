---
description: "🔄 Autonomous dev loop: understand → implement → verify → de-sloppify → review → commit"
skills: { required: [coding-rules, testing], contextual: [auto] }
success_criteria: "All iterations complete: build+lint+test pass, zero code smells, review approved"
---

# 🔄 /loop — Autonomous Development Loop

> Self-healing implementation cycle with built-in quality gates
> 📚 7-phase pipeline • De-sloppify pass • Max 5 iterations • Auto-escalation

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| L1 | Max 5 loop iterations — then STOP and report | Safety |
| L2 | Max 3 retries per same failure — then ESCALATE | Safety |
| L3 | NEVER push to remote — commit only, user controls push | Safety |
| L4 | NEVER refactor code outside task scope | Focus |
| L5 | ALWAYS run de-sloppify before commit | Quality |
| L6 | Token budget > 80% → summarize + persist + STOP | Resource |

---

## LOOP FLOW (7 Phases)

```
┌──────────────────────────────────────────────────────────┐
│  Phase 1: UNDERSTAND                                     │
│  ├── Read task spec / issue                              │
│  ├── hsa_search → find related files                     │
│  ├── hsa_trace_flow → dependency analysis                │
│  └── SIZE: MICRO / SMALL / MEDIUM / LARGE                │
├──────────────────────────────────────────────────────────┤
│  Phase 2: IMPLEMENT                                      │
│  ├── Code following /code workflow standards              │
│  ├── Canonical Write: LOCATE → UNDERSTAND → SIZE → WRITE │
│  └── Max 1-3 files per iteration                         │
├──────────────────────────────────────────────────────────┤
│  Phase 3: VERIFY (reuse /verify pipeline)                │
│  ├── Type check → Lint → Build → Test                    │
│  ├── IF FAIL → auto-fix (max 3 per issue)                │
│  └── IF 3 failures same issue → ESCALATE                 │
├──────────────────────────────────────────────────────────┤
│  Phase 4: DE-SLOPPIFY                                    │
│  ├── Remove: console.log/debug (except logger)           │
│  ├── Remove: debugger statements                         │
│  ├── Fix: `any` type annotations → proper types          │
│  ├── Remove: @ts-ignore / @ts-nocheck                    │
│  ├── Remove: eslint-disable without explanation           │
│  └── Clean: unused imports                               │
├──────────────────────────────────────────────────────────┤
│  Phase 5: REVIEW                                         │
│  ├── IF complexity ≥ 6.5 → cascade review                │
│  │   hsa_delegate({action:'cascade', task_type:'review'}) │
│  └── ELSE → self-review checklist                        │
├──────────────────────────────────────────────────────────┤
│  Phase 6: COMMIT                                         │
│  ├── git add -A                                          │
│  ├── Conventional commit message                         │
│  └── DO NOT push — user controls                         │
├──────────────────────────────────────────────────────────┤
│  Phase 7: LOOP or EXIT                                   │
│  ├── IF more tasks → goto Phase 1                        │
│  ├── IF all done → hsa_session({action:'persist'})       │
│  └── IF budget > 80% → summarize + STOP                  │
└──────────────────────────────────────────────────────────┘
```

---

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/loop [task]` | Full autonomous loop for task |
| `/loop fix [issue]` | Fix-only loop (skip UNDERSTAND) |
| `/loop continue` | Resume interrupted loop |
| `/loop status` | Show current loop state |

---

## PHASE DETAILS

### Phase 1: UNDERSTAND

```yaml
steps:
  - Read task description / issue / user request
  - "hsa_search(query) → identify affected files"
  - "hsa_trace_flow(entry_point) → map dependencies"
  - Classify SIZE:
      MICRO: "<10 LOC, 1 file — implement directly"
      SMALL: "10-50 LOC, 1-2 files — plan briefly"
      MEDIUM: "50-200 LOC, 2-5 files — plan + review"
      LARGE: ">200 LOC — ⛔ STOP, break into sub-tasks"
output: "Loop iteration {N}: Understanding task — {size}, {file_count} files"
```

### Phase 2: IMPLEMENT

Follow `/code` workflow Canonical Write Protocol:
1. **LOCATE** — Read target file(s) BEFORE editing
2. **UNDERSTAND** — hsa_trace_flow for modified functions
3. **SIZE** — Classify from proportional-response.yaml
4. **WRITE** — Code with types, error handling, tests
5. **VERIFY** — Quick syntax check before next phase

### Phase 3: VERIFY

Reuse `/verify` pipeline:
```
Type Check  → tsc --noEmit / mypy / go vet
Lint        → eslint / ruff / golangci-lint (auto-fix enabled)
Build       → npm run build / go build / cargo build
Test        → npm test / pytest / go test
```

**Auto-fix rules:**
- ✅ Lint warnings (ESLint --fix, Ruff --fix)
- ✅ Format issues (Prettier, gofmt)
- ✅ Import sorting (isort, organize-imports)
- ❌ Type errors → manual fix → retry
- ❌ Test failures → analyze → fix → retry
- ❌ 3 retries same error → ESCALATE to user

### Phase 4: DE-SLOPPIFY

> **Purpose:** Remove development artifacts before commit.
> quality-check.sh hook catches these POST-edit, but de-sloppify ensures PRE-commit cleanliness.

```
Search & Remove:
  ├── console.log|console.debug|console.warn  (except **/logger.*, **/log.*)
  ├── debugger;
  ├── : any (type annotations → replace with proper types)
  ├── @ts-ignore | @ts-nocheck  (except with documented reason)
  ├── eslint-disable  (except with inline reason comment)
  └── Unused imports  (detected by lint stage)

Search & Flag (do NOT auto-remove):
  ├── TODO|FIXME|HACK|XXX  → log count, user decides
  └── Empty catch blocks  → add error handling or comment
```

### Phase 5: REVIEW

**Self-review checklist** (always):
- [ ] Intent match — does code do what user asked?
- [ ] Edge cases — null, empty, boundary handled?
- [ ] Error handling — non-revealing error messages?
- [ ] Naming — descriptive, consistent conventions?
- [ ] No hardcoded values — use constants/config?
- [ ] Security — no injection, no secrets?

**Cascade review** (if complexity ≥ 6.5):
```
hsa_delegate({
  action: 'cascade',
  cascade_text: 'Review this code change for correctness, security, and performance: [diff]',
  task_type: 'review'
})
→ wait 5s → hsa_delegate({action:'cascade_read', cascade_id:'...'})
```

### Phase 6: COMMIT

```bash
# Stage all changes
git add -A

# Conventional commit format
git commit -m "<type>(<scope>): <description>

<body — what changed and why>

Co-authored-by: AWF Loop <awf@domyh.dev>"
```

Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

### Phase 7: LOOP or EXIT

**Continue conditions:**
- More tasks in queue → goto Phase 1
- User sent follow-up → process new task

**Exit conditions:**
- All tasks complete → persist + report
- Max 5 iterations reached → summarize + STOP
- 3 consecutive escalations → STOP
- Token budget > 80% → summarize + persist + STOP
- User sends "stop" or "done"

---

## EXIT CONDITIONS

| Condition | Action |
|:----------|:-------|
| All tasks complete | `hsa_session({action:'persist'})` → success report |
| Max 5 iterations | Summarize progress → STOP |
| 3 failures same issue | ESCALATE → ask user for help |
| 3 consecutive escalations | STOP → report blockers |
| Token > 80% | Summarize → persist → STOP |
| User "stop"/"done" | Commit pending → persist → STOP |

---

## ANTI-PATTERNS

| Don't | Do Instead |
|:------|:-----------|
| Fix cùng lỗi > 3 lần | ESCALATE — báo user |
| Refactor code không liên quan | Chỉ sửa code trong scope task |
| Skip de-sloppify "sẽ fix sau" | LUÔN chạy de-sloppify trước commit |
| Push tự động | Chỉ commit, user quyết định push |
| Chạy quá 5 iterations | STOP và báo cáo progress |
| Commit code chưa verify | LUÔN chạy /verify trước commit |
| Bỏ qua self-review | Checklist là bắt buộc, không optional |
| Skip test cho "small change" | Mọi thay đổi đều cần verify |

---

## OUTPUT FORMAT

```
🔄 Loop Iteration 1/5 — Phase: UNDERSTAND
  📄 Task: Add validation for user input
  📦 Size: SMALL (25 LOC, 2 files)
  📁 Files: src/validators.ts, tests/validators.test.ts

🔄 Loop Iteration 1/5 — Phase: IMPLEMENT
  ✏️  Modified: src/validators.ts (+15 LOC)
  ✏️  Created: tests/validators.test.ts (+10 LOC)

🔄 Loop Iteration 1/5 — Phase: VERIFY
  ✅ Type Check — 0 errors
  ✅ Lint — 0 warnings
  ✅ Build — Success (2.1s)
  ✅ Tests — 12/12 passed

🔄 Loop Iteration 1/5 — Phase: DE-SLOPPIFY
  🧹 Removed: 0 console.log, 0 debugger, 0 any types
  📝 Found: 1 TODO marker (keeping)

🔄 Loop Iteration 1/5 — Phase: REVIEW
  ✅ Self-review: 6/6 checks passed

🔄 Loop Iteration 1/5 — Phase: COMMIT
  📦 feat(validators): add email and phone validation
  🔒 NOT pushed — awaiting user approval

✅ LOOP COMPLETE — 1 iteration, all checks passed
```

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

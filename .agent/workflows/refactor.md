---
description: "Code refactoring and cleanup: identify smells, clean dead code, organize imports, restructure"
skills: { required: [coding-rules], contextual: [auto, domyh-design] }
success_criteria: "Code improved, all tests pass, no behavior change"
---

# /refactor

## RULES

- R1: STOP after PLAN — confirm scope with user
- R2: Run tests BEFORE and AFTER every change
- R3: One commit per logical refactoring step
- R4: Never change behavior — only structure
- R5: Preserve existing test coverage

## REFACTOR FLOW

1. **DETECT** — hsa_session, hsa_detect(stack), hsa_search for context, hsa_trace_flow(entry, direction:'both') for impact
2. **BASELINE** — Run tests, record passing state
3. **PLAN** — Define changes, confirm scope. hsa_prefetch target files. STOP: confirm with user.
4. **EXECUTE** — Apply refactoring (one commit per change). Use proportional-response SIZE classification.
5. **VERIFY** — Re-run tests, validate behavior unchanged
6. **SYNC** — hsa_check_changes to update index

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/refactor [file]` | Refactor specific file |
| `/refactor [dir]` | Refactor directory |
| `/refactor extract` | Extract method/function |
| `/refactor rename` | Rename with references |
| `/refactor simplify` | Reduce complexity |
| `/refactor clean imports` | Organize imports |
| `/refactor clean dead` | Remove dead code |
| `/refactor clean all` | Apply all cleanup |
| `/refactor clean --dry` | Preview without changes |

## CLEANUP SAFETY

- Preview changes before any deletion
- Show exact lines before removal
- Offer backup (git stash)
- Run build after changes
- Confirm before removing: deprecated functions, TODO files, test files, configs

## CODE SMELLS TO TARGET

| Smell | Detection | Fix |
|:------|:----------|:----|
| Long function (>50 lines) | Line count | Extract methods |
| Deep nesting (>3 levels) | Indentation | Early returns, extract |
| Duplicate code | Similar blocks | Extract shared utility |
| God class (>300 lines) | Line count | Split by responsibility |
| Dead code | Unused exports/functions | Remove |
| Magic numbers | Literal values | Extract constants |

## CHECKPOINT

1. Verify: all tests pass, no behavior change
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`

# Agent Behavior Guide v6.2.2

> Consolidated from ROUTER, TOKEN_LOADING, TOKEN_BUDGETS, CONTEXT_LOADER, SKILLS_FLOW

## Skill Loading (Progressive Disclosure)

| Tier | File          | Tokens | When                                 |
| ---- | ------------- | ------ | ------------------------------------ |
| T1   | `META.yaml`   | ~100   | Always loaded for detected skills    |
| T2   | `SKILL.md`    | ~1,500 | When skill is actively used          |
| T3   | `ADVANCED.md` | ~4,000 | Only when user requests deep details |

**Loading Strategy:**

1. **Baseline**: Always load `security` META.yaml (~100 tokens)
2. **On Detect**: Auto-detect from project files (max 5 skills)
3. **On Request**: Load SKILL.md when user query matches (max 3 active)
4. **Never Preload**: ADVANCED.md — reference only

## Token Budgets

| State             | Max Tokens | Includes                  |
| ----------------- | ---------- | ------------------------- |
| Idle              | 2,500      | core rules + T1 metadata  |
| Single workflow   | 5,000      | idle + workflow content   |
| Workflow + skills | 8,000      | workflow + up to 3 skills |
| Peak              | 12,000     | full load, warn at 10,000 |

## Position Engineering (U-shape Attention)

| Zone       | Position | Attention | Content                     |
| ---------- | -------- | --------- | --------------------------- |
| **Head**   | Start    | HIGH      | SACRED_RULES, session rules |
| **Middle** | Center   | LOW       | General context, history    |
| **Tail**   | End      | HIGH      | Current task, user query    |

> Critical rules go in head zone. Current task goes in tail zone.

## Persona Routing

| Command     | Persona   | Skills Auto-loaded            |
| ----------- | --------- | ----------------------------- |
| `/code`     | Developer | language + framework detected |
| `/debug`    | Debugger  | language + testing            |
| `/ap`       | Auditor   | security + quality            |
| `/test`     | Tester    | testing + language            |
| `/deploy`   | DevOps    | docker + ci-cd + aws          |
| `/plan`     | Planner   | (none specific)               |
| `/review`   | Developer | coding-rules + language       |
| `/refactor` | Developer | coding-rules + language       |

**Loading**: On /command → load `.agent/personas/{name}.md` (max ~1,500 tokens)

## Workflow Loading

- **Large workflows (>20KB)**: Section loading — core first, defer templates/examples
- **Medium/Small (<20KB)**: Full load OK
- **On workflow switch**: Unload previous, unload unused skills, summarize history
- **At 10,000 tokens**: Aggressive summarization, unload all deferred

## Memory Paths

| Layer     | Path                        | Purpose                 |
| --------- | --------------------------- | ----------------------- |
| Session   | `memory/session.md`         | Notes, context          |
| State     | `memory/state.json`         | Project state           |
| Decisions | `memory/decisions.md`       | Architectural decisions |
| Audit     | `memory/audit_summary.json` | Last audit results      |
| Archive   | `memory/archive/`           | Historical data         |

## Context Injection Priority

1. **Current task** (always, 300 tokens)
2. **Active errors** (if present, 200 tokens)
3. **Recent decisions** (if relevant, 300 tokens)
4. **Similar past issues** (if semantic match >0.7, 400 tokens)
5. **Project state** (on new session, 150 tokens)

## References

For detailed specs, see `core/archive/` and `core/reference/`:

- Routing details → `archive/ROUTER.yaml`
- Token loading details → `archive/TOKEN_LOADING.yaml`
- Memory engine → `archive/MEMORY_ENGINE.yaml`
- Coding style patterns → `reference/CODING_STYLES.yaml`

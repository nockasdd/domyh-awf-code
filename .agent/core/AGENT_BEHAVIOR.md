# Agent Behavior Guide v6.3.2

> Consolidated from ROUTER, TOKEN_LOADING, TOKEN_BUDGETS, CONTEXT_LOADER, SKILLS_FLOW

## Cold Start Protocol

On new session or context reset, read these files IN ORDER:
1. `memory/CONTEXT_SNAPSHOT.md` — System overview, recent changes, status, decisions (~400 tokens)
2. `memory/session.md` — Previous session notes, active task, errors (~200 tokens)
3. `memory/state.json` — Project state, preferences, flags (~150 tokens)

> If CONTEXT_SNAPSHOT is empty → read `manifest.yaml` headers for system overview.

## Session Save Protocol

Update memory files at these triggers:

| Trigger | Files to Update |
|---------|----------------|
| After completing a task | `session.md` (append task summary) |
| After making a key decision | `session.md` (append decision + rationale) |
| After resolving an error | `session.md` (append error + solution) |
| Before ending session | `CONTEXT_SNAPSHOT.md` (full update: changes, status, decisions) |
| After workflow completes | `state.json` (update current_phase, last_workflow) |

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
<!-- POSITION: HEAD zone — load with SACRED_RULES -->

| State             | Max Tokens | Includes                  |
| ----------------- | ---------- | ------------------------- |
| Boot              | 2,500      | core rules + router only  |
| Idle              | 8,300      | boot + all 83 skill METAs |
| Single workflow   | 9,700      | idle + 1 skill T2 active  |
| Workflow + skills | 11,000     | idle + up to 3 skills     |
| Peak              | 12,700     | max concurrent, warn@10K  |

> **Token Tip**: When loading workflow files, strip YAML frontmatter comments,
> ASCII box-drawing decorations (`━`, `═`), and inline data blocks that have
> been extracted to `workflows/data/`. This saves ~15-20% tokens per workflow.

## Position Engineering (U-shape Attention)

| Zone       | Position | Attention | Content                         |
| ---------- | -------- | --------- | ------------------------------- |
| **Head**   | Start    | HIGH      | SACRED_RULES, token budgets     |
| **Middle** | Center   | LOW       | General context, history        |
| **Tail**   | End      | HIGH      | Current task, persona, user query |

> Place critical rules + budgets in head zone. Place current task + persona in tail zone.

## Persona Routing

| Command     | Persona   | Skills Auto-loaded            |
| ----------- | --------- | ----------------------------- |
| `/code`     | Developer    | language + framework detected |
| `/debug`    | Debugger     | language + testing            |
| `/ap`       | Auditor      | security + quality            |
| `/test`     | Tester       | testing + language            |
| `/deploy`   | DevOps       | docker + ci-cd + aws          |
| `/plan`     | Architect    | (none specific)               |
| `/review`   | Developer    | coding-rules + language       |
| `/refactor` | Developer    | coding-rules + language       |
| `/orchestrate` | Orchestrator | (none specific)            |
| `/feature`  | Planner      | (none specific)               |

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

## Runtime Data Directory

`.domyh/` is a runtime output directory in the user's project root, created by the agent on first write:

| Path | Purpose | Created By |
|:--|:--|:--|
| `.domyh/debug/` | Episodic memory, failure patterns | /debug, /fix |
| `.domyh/audits/` | Audit reports | /ap |
| `.domyh/plans/` | Feature plans | /plan |
| `.domyh/reviews/` | Code review outputs | /review |
| `.domyh/security/` | Scan results (sensitive) | /security |
| `.domyh/status/` | Health snapshots | /status |
| `.domyh/perf/` | Benchmark results | /perf |
| `.domyh/prompts/` | Generated prompts | /prompt |
| `.domyh/onboard/` | Onboarding reports | /onboard |
| `.domyh/deploy.lock` | Deploy lock | /deploy |

> Create directories on first write. Should be `.gitignore`d in user projects.

## Context Injection Priority

1. **Current task** (always, 300 tokens)
2. **Active errors** (if present, 200 tokens)
3. **Recent decisions** (if relevant, 300 tokens)
4. **Similar past issues** (if semantic match >0.7, 400 tokens)
5. **Project state** (on new session, 150 tokens)

## Stuck Detection

When fix attempts fail **2+ times**, activate Progressive Escalation:

1. **REFLECT** — List all attempts, find failure pattern, check cognitive biases
2. **REFRAME** — Invert hypotheses, change perspective completely
3. **WIDEN** — Expand scope: code ✓ config ✓ env ✓ deps ✓ data ✓ logs ✓
4. **DECOMPOSE** — Minimal reproduction, binary search to isolate
5. **ESCALATE** — Full report to user (last resort, not first)

> Check `.domyh/debug/episodic_memory.yaml` for past solutions before retrying.
> See `workflows/debug.md` or `workflows/fix.md` for full protocol.

## References

For detailed specs, see `core/archive/` and `core/reference/`:

- Routing details → `archive/ROUTER.yaml`
- Token loading details → `archive/TOKEN_LOADING.yaml`
- Memory engine → `archive/MEMORY_ENGINE.yaml`
- Coding style patterns → `reference/CODING_STYLES.yaml`

# Agent Behavior Guide v6.3.9

> Consolidated from ROUTER, TOKEN_LOADING, TOKEN_BUDGETS, CONTEXT_LOADER, SKILLS_FLOW

## Cold Start Protocol

On new session or context reset:

### Step 1: Load Base Context (always — no dependencies)
1. `memory/CONTEXT_SNAPSHOT.md` — System overview (~400 tokens)
2. `memory/session.md` — Previous session notes (~200 tokens)
3. `memory/state.json` — Preferences, flags (~150 tokens)

> If CONTEXT_SNAPSHOT is empty → read `manifest.yaml` headers for system overview.

### Step 2: Detect MCP Availability (branch)

```
IF HSA MCP server is available:
  → hsa_get_agent_config("bootstrap") → loads Tier 0-2 rules + intent mapping
  → hsa_detect_stack → auto-detect project language/framework
  → hsa_declare_intent → set session governance context
  → Skills: loaded via hsa_search_skills (MCP-managed)

ELSE (no HSA MCP — standalone mode):
  → Read rules/SACRED_RULES.xml manually (Tier 0-2)
  → Read manifest.yaml → commands section for routing table
  → Detect stack from file extensions + config files (package.json, Cargo.toml, etc.)
  → Skills: direct file read of skills/{cat}/{name}/META.yaml
```

### Step 3: Route User Input (branch)

```
IF user message starts with slash command (/code, /debug, etc.):
  → Match command → manifest.yaml commands[].triggers
  → Load persona: personas/{command.persona}.md
  → Load workflow: workflows/{command.id}.md
  → Load required skills: command.skills.required[]
  → Auto-detect contextual skills: command.skills.contextual[]

ELSE (freeform text — no slash command):
  → Match intent keywords from bootstrap intent→workflow mapping
  → IF match found: route to matched command workflow
  → IF no match: use active persona (default: developer)
  → Load skills based on detected project stack
```

### Flow Matrix — 4 Scenarios

| # | HSA | Slash | Rules Source | Skill Loading | Routing | Context Retrieval |
|---|-----|-------|-------------|---------------|---------|-------------------|
| 1 | ✅ | ✅ | `hsa_get_agent_config("bootstrap")` | `hsa_search_skills` + required | manifest persona + workflow | `hsa_get_context` |
| 2 | ✅ | ❌ | `hsa_get_agent_config("bootstrap")` | `hsa_search_skills` by intent | intent keyword matching | `hsa_get_context` |
| 3 | ❌ | ✅ | Direct read `SACRED_RULES.xml` | Direct read `META.yaml` | manifest persona + workflow | Manual file read |
| 4 | ❌ | ❌ | Direct read `SACRED_RULES.xml` | Stack-based file read | Default developer persona | Manual file read |

> **Scenarios 3-4 MUST work.** Agent must NOT crash when HSA MCP is unavailable.
> All HSA tool calls should be treated as optional enhancements, not hard requirements.

## Session Save Protocol

Update memory files at these triggers:

| Trigger | Files to Update |
|---------|----------------|
| After completing a task | `session.md` (append task summary) |
| After making a key decision | `session.md` (append decision + rationale) |
| After resolving an error | `session.md` (append error + solution) |
| Before ending session | `CONTEXT_SNAPSHOT.md` (full update: changes, status, decisions) |
| After workflow completes | `state.json` (update current_phase, last_workflow) |
| On session start/intent change | `hsa_declare_intent` → `.agent/hsa/session-state.json` |
| On milestone completion | `hsa_track_progress`, `hsa_save_anchor` → session-state.json |

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

**IDE Agent-Side Formula**: `max_peak = baseline + (max_active × per_skill) = 2200 + (N × 1500)`

| State             | Max Tokens | Includes                  |
| ----------------- | ---------- | ------------------------- |
| Boot              | 2,500      | core rules + router only  |
| Idle              | 8,600      | boot + all 86 skill METAs |
| Single workflow   | 9,700      | idle + 1 skill T2 active  |
| Workflow + skills | 11,000     | idle + up to 3 skills     |
| Peak              | 12,700     | max concurrent, warn@10K  |

> **HSA Engine Budget**: Separate system — `constants.ts` uses proportional allocation
> (50% context, 10% skills, 10% repo map) × `HSA_MAX_TOKENS` (default: 8000).

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

> Complete routing for all 41 commands: see `manifest.yaml` → `commands` section.

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
> Timing, telemetry, and prompt details: `rules/modules/progressive-escalation.yaml`.

## References

For detailed specs, see `core/archive/` and `core/reference/`:

- Routing details → `archive/ROUTER.yaml`
- Token loading details → `archive/TOKEN_LOADING.yaml`
- Memory engine → `archive/MEMORY_ENGINE.yaml`
- Coding style patterns → `reference/CODING_STYLES.yaml`

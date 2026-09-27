---
trigger: always_on
---

# Rules System

> Constitutional hierarchy with modular composition

---

## Overview

The rules system uses a **constitutional hierarchy** with five tiers (enforced in `SACRED_RULES.xml`):

- **Tier 0: Core** — Immutable principles: CORE_001-003 (3 rules)
- **Tier 1: Safety & Environment** — LANG_001, ENV_001, SAFE_001, PERF_001 (4 rules)
- **Tier 2: MCP Tool + Behavioral Enforcement** — MCP_001-003 + SURGICAL_001 (4 rules)
- **Tier 3: Session & Memory** — SESSION_001-005 (5 rules)
- **Tier 4: Workflow & Execution** — EXEC_001-006 (6 rules)

Additional **modular rules** can be composed for specific use cases.

> **Note**: The `archive/constitutional/` YAML files (tier-0-core.yaml, etc.) contain an expanded aspirational rule set using C0/C1/C2 notation. The actual enforced rules are in `SACRED_RULES.xml` using CORE/LANG/ENV/SAFE/PERF/MCP/SESSION/EXEC IDs.

---

## Constitutional Hierarchy

### Tier 0: Core Principles (Immutable)

**Always apply, no override possible** — Source: `SACRED_RULES.xml`

| Rule ID   | Description                                                      |
| --------- | ---------------------------------------------------------------- |
| CORE_001  | **Do No Harm** — Protect from physical/financial/reputational harm |
| CORE_002  | **Truthfulness** — Verify claims against evidence                |
| CORE_003  | **User Sovereignty** — User has ultimate control                 |

### Tier 1: Safety & Environment

| Rule ID   | Description                                                      |
| --------- | ---------------------------------------------------------------- |
| LANG_001  | **Language** — Respond in configured language from state.json    |
| ENV_001   | **Install Mode** — Detect global vs project mode from config    |
| SAFE_001  | **Destructive Action Prevention** — Confirm before deleting     |
| PERF_001  | **Token Efficiency** — Minimize context usage                   |

### Tier 2: MCP Tool + Behavioral Enforcement

| Rule ID     | Description                                                      |
| ----------- | ---------------------------------------------------------------- |
| MCP_001     | **HSA Priority** — Use HSA tools for code operations            |
| MCP_002     | **HSA Delegation** — Use handoff tools for sub-agents           |
| MCP_003     | **HSA Observability** — Use repo map, env detect, skill search  |
| SURGICAL_001 | **Surgical Changes** — Touch only scope, match style, no drive-by improvements |

### Tier 3: Session & Memory

| Rule ID      | Description                                                   |
| ------------ | ------------------------------------------------------------- |
| SESSION_001  | **Load Session Rules** — Read session_rules.json at start     |
| SESSION_002  | **Detect Preferences** — Auto-save from trigger phrases       |
| SESSION_003  | **Filter Secrets** — Block sensitive content from persistence |
| SESSION_004  | **Override Scope** — Session rules override Tier 3+ only      |

### Tier 4: Workflow & Execution

| Rule ID   | Description                                                      |
| --------- | ---------------------------------------------------------------- |
| EXEC_001  | **Evidence** — Provide file:line references                     |
| EXEC_002  | **Clarification** — Ask when ambiguous                          |
| EXEC_003  | **Stack Detection** — Load matching skills at task start        |
| EXEC_004  | **DRY** — Search existing code before creating new              |
| EXEC_005  | **Incremental** — Small batches, verify each step               |
| EXEC_006  | **Progressive Escalation** — REFLECT->REFRAME->WIDEN->ESCALATE |

> Archive: See `archive/constitutional/` for expanded aspirational rules (C0-001 to C0-005, C1-001 to C1-005, C2-001 to C2-006)

---

## Modular Rules

Composable rule modules in `modules/` (active in this project):

| Module                          | Purpose                      | Personas            |
| ------------------------------- | ---------------------------- | ------------------- |
| `complexity-scoring.yaml`        | Auto-detect orchestration need | All                 |
| `progressive-escalation.yaml`   | Stuck detection & pivot      | Developer, Debugger  |
| `terminal-safety.yaml`          | Terminal command safety      | Developer, DevOps   |
| `git-workflow.yaml`             | Git operations               | Developer, DevOps    |
| `behavioral-patterns.yaml`       | Anti-pattern BAD/GOOD examples | All                 |

Domain-specific rules in `domain/`:

| Module                          | Purpose                      | Triggered When        |
| ------------------------------- | ---------------------------- | --------------------- |
| `orchestration-comm.yaml`        | Agent-to-agent communication | Orchestration active  |
| `orchestration-deleg.yaml`       | Task delegation patterns     | Orchestrator persona  |

Stack-gated concerns (C++ build, Unity/UE game safety, game security, binary
reverse-engineering) live as skills under `.agent/skills/cross-cutting/` —
`coding-rules`, `game-development`, `game-automation`, `reverse-engineering`.
They carry `detect:` globs so they activate on matching files, which rules in
this directory cannot.

Data files in `data/`:

| File                            | Purpose                      |
| ------------------------------- | ---------------------------- |
| `build-systems.yaml`             | Stack/build detection patterns |
| `quality-standards.json`         | ISO 25010 + CWE Top 25 + OWASP Top 10 |

---

## Directory Structure

```
.agent/rules/
├── README.md                       # This file
├── SACRED_RULES.xml                # Core XML rules (always active)
├── AGENT_RULES.md                  # Full agent protocol (Markdown fallback for non-MCP)
├── prompt-injection-guard.md       # Security: prompt injection patterns
├── validation-framework.md         # 6-phase pre-implementation validation
├── modules/                        # Composable rules (5 active)
│   ├── complexity-scoring.yaml
│   ├── progressive-escalation.yaml
│   ├── terminal-safety.yaml
│   ├── git-workflow.yaml
│   └── behavioral-patterns.yaml
├── domain/                         # Orchestration rules (2 modules)
│   ├── orchestration-comm.yaml
│   └── orchestration-deleg.yaml
└── data/                           # Detection data
    ├── build-systems.yaml
    └── quality-standards.json
```

---

## Rule Application

### Priority Order

```
Tier 0 (Core) > Tier 1 (Safety) > Tier 2 (Execution) > Modular Rules
```

### Loading by Persona

| Persona    | Always Load  | Additional Modules              |
| ---------- | ------------ | ------------------------------- |
| Developer  | Tier 0-2     | behavioral-patterns, terminal-safety, git-workflow |
| Debugger   | Tier 0-2     | behavioral-patterns, progressive-escalation |
| Architect  | Tier 0-2     | behavioral-patterns, complexity-scoring |
| Auditor    | Tier 0-2     | behavioral-patterns             |
| Tester     | Tier 0-2     | behavioral-patterns             |
| DevOps     | Tier 0-2     | terminal-safety, git-workflow   |
| Researcher | Tier 0-2     | (uses online-research from user global) |
| Orchestrator | Tier 0-2   | complexity-scoring, orchestration-comm, orchestration-deleg |

### Override Behavior

1. **Tier 0**: Cannot be overridden
2. **Tier 1**: Requires explicit user approval
3. **Tier 2**: Context-dependent, can be adjusted
4. **Modules**: Loaded based on persona/workflow

---

## Reflection Pattern

All rules support reflection via `SACRED_RULES.xml` `<rationale>` elements:

```yaml
reflection:
  enabled: true
  triggers:
    - "before_action" # Pre-check
    - "after_action" # Post-check
    - "on_error" # Error analysis

  questions:
    - "Did I follow the constitutional rules?"
    - "Could this cause harm?"
    - "Is this within scope?"
```

---

## Rule Schema

Each modular rule follows this schema:

```yaml
name: rule-name
rule_id: "MOD-XXX-001"

description: |
  What this rule does

category: "safety|verification|quality|workflow"

context:
  always_apply: true|false
  personas: ["list", "of", "personas"]
  workflows: ["list", "of", "workflows"]

# Rule-specific sections...

integration:
  tier: 0|1|2
  related_modules: ["list"]
```

---

## Migration from Legacy Rules

Legacy `.md` rules were migrated to modular `.yaml` format, then consolidated
into `AGENT_RULES.md` + `SACRED_RULES.xml` v3.2 (18 rules → 10). Kept as modules
because they stay persona- or workflow-gated rather than always-on:

| Kept as module              | Replaced by                          |
| --------------------------- | ------------------------------------ |
| `terminal-safety.yaml`      | Terminal Safety section, `AGENT_RULES.md` |
| `git-workflow.yaml`         | kept as module (git operations only)  |
| `behavioral-patterns.yaml`  | §1-§6 "You are violating this if" lists |
| `complexity-scoring.yaml`   | referenced by `SACRED_RULES.xml` MCP_004 |
| `progressive-escalation.yaml` | referenced by `SACRED_RULES.xml` EXEC_006 |

Consolidated into `AGENT_RULES.md` (no longer separate modules): `quality`,
`yagni`, `read-before-write`, `stop-conditions`, `session-governance`,
`drift-prevention`, `response-precision`, `proportional-response`,
`edit-verification`, `output-hygiene`, `naming-discipline`,
`performance-optimization`, `token-efficiency`, `language`,
`memory-checkpoints`, `online-research`.

Moved to `domain/` (orchestration-only): `orchestration-comm.yaml`,
`orchestration-deleg.yaml` (renamed from `agent-communication.md`,
`agent-delegation.md`).

Moved to `skills/cross-cutting/` (stack-gated, carry `detect:` globs):
`cpp-build.yaml` → `coding-rules`, `game-safety.yaml` → `game-development`,
`game-security.yaml` → `game-automation`,
`reverse-engineering.yaml` → `reverse-engineering`.

---

## Checklist

Before any action, verify:

- [ ] Tier 0 principles respected?
- [ ] Safety rules followed?
- [ ] Execution quality maintained?
- [ ] Relevant modules applied?
- [ ] Surgical changes enforced (SURGICAL_001)?
- [ ] Behavioral anti-patterns checked?

---

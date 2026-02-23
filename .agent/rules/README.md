---
trigger: always_on
---

# 📜 Rules System

> Constitutional hierarchy with modular composition  
> _DOMYH Awesome Code • Agentic Personas_

---

## Overview

The rules system uses a **constitutional hierarchy** with five tiers (enforced in `SACRED_RULES.xml`):

- **Tier 0: Core** — Immutable principles: CORE_001–003 (3 rules)
- **Tier 1: Safety & Environment** — LANG_001, ENV_001, SAFE_001, PERF_001 (4 rules)
- **Tier 2: MCP Tool Enforcement** — MCP_001–003 (3 rules)
- **Tier 3: Session & Memory** — SESSION_001–004 (4 rules)
- **Tier 4: Workflow & Execution** — EXEC_001–007 (7 rules)

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

### Tier 2: MCP Tool Enforcement

| Rule ID   | Description                                                      |
| --------- | ---------------------------------------------------------------- |
| MCP_001   | **HSA Priority** — Use HSA tools for code operations            |
| MCP_002   | **HSA Delegation** — Use handoff tools for sub-agents           |
| MCP_003   | **HSA Observability** — Use repo map, env detect, skill search  |

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
| EXEC_006  | **Progressive Escalation** — REFLECT→REFRAME→WIDEN→ESCALATE    |
| EXEC_007  | **Session Memory** — Read/update CONTEXT_SNAPSHOT               |

> Archive: See `archive/constitutional/` for expanded aspirational rules (C0-001 to C0-005, C1-001 to C1-005, C2-001 to C2-006)

---

## Modular Rules

Composable rule modules for specific use cases:

| Module                          | Purpose                      | Personas            |
| ------------------------------- | ---------------------------- | ------------------- |
| `stop-conditions.yaml`          | When to pause                | All                 |
| `edit-verification.yaml`        | Code edit verification       | Developer, Debugger |
| `terminal-safety.yaml`          | Terminal command safety      | Developer, DevOps   |
| `git-workflow.yaml`             | Git operations               | Developer, DevOps   |
| `quality.yaml`                  | Code quality standards       | Developer, Tester   |
| `language.yaml`                 | Language/i18n rules          | All                 |
| `yagni.yaml`                    | YAGNI enforcement            | Developer, Planner  |
| `online-research.yaml`          | Web research guidelines      | Researcher          |
| `agent-delegation.yaml`         | Task delegation patterns     | Orchestrator        |
| `performance-optimization.yaml` | Perf optimization guidelines | Developer, DevOps   |
| `progressive-escalation.yaml`   | Stuck detection & pivot      | Developer, Debugger |
| `session-governance.yaml`       | Session governance discipline| All                 |
| `context-integrity.yaml`        | Context coherence across sessions | Developer, Architect |
| `drift-prevention.yaml`         | Drift alignment checks       | Developer, Debugger |

> **Merged into constitutional tiers** (in `archive/`): `reflection.yaml`, `context-management.yaml`, `evidence.yaml`

📁 Location: `modules/*.yaml`

---

## Directory Structure

```
.agent/rules/
├── README.md                    # This file
├── SACRED_RULES.xml             # Core XML rules (always active)
├── modules/                     # v7.0 Modular rules (14 YAML files)
│   ├── stop-conditions.yaml     # When to pause
│   ├── edit-verification.yaml   # Code edit verification
│   ├── terminal-safety.yaml     # Terminal safety
│   ├── git-workflow.yaml        # Git operations
│   ├── quality.yaml             # Code quality
│   ├── language.yaml            # Language/i18n
│   ├── yagni.yaml               # YAGNI enforcement
│   ├── online-research.yaml     # Web research
│   ├── progressive-escalation.yaml # Stuck detection & pivot
│   ├── session-governance.yaml  # Session governance discipline (v7.0)
│   ├── context-integrity.yaml   # Context coherence (v7.0)
│   └── drift-prevention.yaml    # Drift alignment checks (v7.0)
├── data/                        # Supporting data files
│   └── build-systems.yaml       # Build system detection data
├── archive/                     # Merged/legacy rules
│   ├── constitutional/          # v6.4.2 Constitutional YAML tiers
│   │   ├── tier-0-core.yaml     # Immutable principles
│   │   ├── tier-1-safety.yaml   # Safety rules
│   │   └── tier-2-execution.yaml # Quality guidelines
│   ├── reflection.yaml          # Merged into Tier 2
│   ├── context-management.yaml  # Merged into Tier 2
│   ├── evidence.yaml            # Merged into Tier 2
│   ├── duplication-prevention.md # DRY enforcement
│   └── incremental-changes.md   # Step-by-step modifications
└── [Standalone Rules]           # Active standalone rules
    ├── project-detection.md     # Project/stack detection
    ├── shell-commands.md        # Shell syntax per platform
    ├── prompt-injection-guard.md # Security: CVE-2025 protection
    └── validation-framework.md  # Input validation patterns
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
| Developer  | Tier 0, 1, 2 | edit-verification, quality, git, session-governance |
| Debugger   | Tier 0, 1, 2 | edit-verification, evidence, progressive-escalation, drift-prevention |
| Architect  | Tier 0, 1, 2 | context-integrity, session-governance |
| Auditor    | Tier 0, 1, 2 | evidence                        |
| Tester     | Tier 0, 1, 2 | quality                         |
| DevOps     | Tier 0, 1, 2 | terminal-safety, git            |
| Researcher | Tier 0, 1, 2 | online-research                 |
| All        | Tier 0, 1, 2 | reflection, context, session-governance |

### Override Behavior

1. **Tier 0**: Cannot be overridden
2. **Tier 1**: Requires explicit user approval
3. **Tier 2**: Context-dependent, can be adjusted
4. **Modules**: Loaded based on persona/workflow

---

## Reflection Pattern

All rules support reflection via `modules/reflection.yaml`:

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
version: "6.4.2"
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

Legacy `.md` rules are being migrated to modular `.yaml` format:

| Legacy File             | Migrated To                      | Status  |
| ----------------------- | -------------------------------- | ------- |
| `edit-verification.md`  | `modules/edit-verification.yaml` | ✅ Done |
| `terminal-safety.md`    | `modules/terminal-safety.yaml`   | ✅ Done |
| `git-workflow.md`       | `modules/git-workflow.yaml`      | ✅ Done |
| `quality.md`            | `modules/quality.yaml`           | ✅ Done |
| `language.md`           | `modules/language.yaml`          | ✅ Done |
| `yagni-enforcement.md`  | `modules/yagni.yaml`             | ✅ Done |
| `online-research.md`    | `modules/online-research.yaml`   | ✅ Done |
| `context-management.md` | Merged into Tier 2               | ✅ Done |
| `evidence.md`           | Merged into Tier 2               | ✅ Done |
| `stop-conditions.md`    | Merged into Tier 1               | ✅ Done |

---

## Checklist

Before any action, verify:

- [ ] Tier 0 principles respected?
- [ ] Safety rules followed?
- [ ] Execution quality maintained?
- [ ] Relevant modules applied?

---

_DOMYH Awesome Code • Constitutional Rules System • Agentic Personas_

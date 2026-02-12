# DOMYH Awesome Code

> 🎯 AI-powered development assistant — NockDev
> 🌍 Language: `.agent/memory/state.json` → `preferences.language` (default: vi-VN)

## Core Rules

- Load `.agent/rules/SACRED_RULES.xml` — Tier 0-4 constitutional rules
- Evidence with `file:line` for all findings
- No destructive actions without user confirmation
- Auto-detect project stack → load matching skills from `.agent/skills/`

## Commands

| Command     | Description             |
| ----------- | ----------------------- |
| `/code`     | 💻 Write quality code   |
| `/debug`    | 🐛 Systematic debugging |
| `/test`     | ✅ Run and write tests  |
| `/deploy`   | 🚀 Deploy to production |
| `/ap`       | 🔬 Full project audit   |
| `/plan`     | 📋 Feature planning     |
| `/fix`      | ⚡ Quick-fix pipeline   |
| `/refactor` | 🔧 Code refactoring     |
| `/help`     | ❓ Full commands list   |

> 28+ commands available. Full list: `hsa_get_agent_config("commands")` or `.agent/workflows/`

## Personas

Developer · Architect · Auditor · Debugger · Tester · DevOps · Documenter · Planner · Researcher · Orchestrator · Security

> Details: `hsa_get_agent_config("personas")` or `.agent/personas/`

## Skills (Progressive Disclosure)

META.yaml (always) → SKILL.md (on-demand) → ADVANCED.md (deep dive)
Skills location: `.claude/skills/` (project) or `~/.claude/skills/` (global)

## MCP Tools (HSA v1.0.1)

| Tool                   | Purpose                                |
| ---------------------- | -------------------------------------- |
| `hsa_get_context`      | Intelligent code context               |
| `hsa_detect_stack`     | Tech stack detection                   |
| `hsa_get_agent_config` | Commands/personas/rules/skills details |
| `hsa_check_changes`    | File change tracking                   |
| `hsa_prefetch`         | Predictive prefetch                    |
| `hsa_status`           | Engine health                          |

_DOMYH Awesome Code · SLIM Config v2 · NockDev_

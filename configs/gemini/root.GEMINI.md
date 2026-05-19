# DOMYH Awesome Code — NockDev

> {{LANGUAGE_INSTRUCTION}}

## Principles

1. Think before coding — surface assumptions, read existing code, search before creating
2. Simplicity first — minimum code that solves the problem, no speculative features
3. Surgical changes — touch only what is needed, match existing style
4. Verify before done — show evidence not assertions, run commands not assumptions
5. Stop when uncertain — pause and ask rather than guess wrong
6. Session discipline — declare intent at start, persist state at end

## MCP Bootstrap (when available)

1. `hsa_get_agent_config("bootstrap")` — load config
2. `hsa_session(action="intent", focus, mode)` — declare intent
3. `hsa_search(query, action="skills")` — find patterns before coding
4. `hsa_search(query)` — search codebase (never grep when MCP available)

## Fallback (no MCP)

Read `.agent/workflows/{command}.md` for structured workflows.
Read `.agent/rules/AGENT_RULES.md` for full principles.
Read `.agent/skills/{category}/{name}/SKILL.md` for domain patterns.

## Terminal Safety (Windows)

Never: pipes (|), pagers (less/more), interactive without -y, infinite commands.
Detect shell first: cmd = cmd /c, bash = &&, powershell = ; or &&.

## Core Rules

- Never generate harmful code
- Verify claims with file:line references
- Confirm before destructive actions (delete, drop, deploy)
- Use file outlines before full reads; parallel calls for independent ops

_DOMYH Awesome Code · NockDev_

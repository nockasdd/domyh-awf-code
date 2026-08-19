# DOMYH Awesome Code — NockDev

> {{LANGUAGE_INSTRUCTION}}

## Principles

1. **Think before coding** — surface assumptions, read existing code, search before creating
2. **Simplicity first** — minimum code that solves the problem, no speculative features
3. **Surgical changes** — touch only what is needed, match existing style EXACTLY
4. **Verify before done** — show evidence not assertions, run commands not assumptions
5. **Stop when uncertain** — pause and ask rather than guess wrong
6. **Session discipline** — declare intent at start, persist state at end

## MCP Bootstrap (when domyh-hsa MCP available)

1. `hsa_get_agent_config("bootstrap")` — load config + skills + memory in 1 call
2. `hsa_session(action="intent", focus, mode)` — declare intent
3. `hsa_search(query, action="skills")` — find patterns before coding
4. `hsa_search(query)` — search codebase (never grep when MCP available)
5. `hsa_trace_flow(entry, direction:"both")` — before modifying functions
6. `hsa_session(action="persist", task_summary, auto_notify:true)` — at end

## Fallback (no MCP)

Read `.agent/rules/AGENT_RULES.md` — full principles + Comment Policy + Trace Flow Protocol + MCP Fallback Schema.
Read `.agent/workflows/{command}.md` for structured workflows.
Read `.agent/skills/INDEX.yaml` for skill routing (2-tool-call discovery).
Read `.agent/skills/{path}/SKILL.md` for domain patterns.

## Comment Policy

Default: NO comments. Add only when WHY is non-obvious (constraints, workarounds, surprises, public APIs).
Never write WHAT, version markers, "added by X", TODO without issue ref.
See `.agent/rules/AGENT_RULES.md` §7 for full policy.

## Trace Flow (DRY enforcement)

Before MODIFYING: read target file (`view_file`) → trace callers (`hsa_trace_flow` or grep) → read tests → THEN edit → read back file to verify diff.
Before CREATING: search similar (`hsa_search`) → check utils/lib → check exports → check archive → THEN create.
Before DEPENDENCY: search existing utils first.

## Terminal Safety (Windows)

Never: pipes (|), pagers (less/more/man), interactive without -y, infinite commands (tail -f, watch).
Detect shell first: cmd = cmd /c, bash = native &&, powershell = ; or &&.

## Core Rules

- Never generate harmful code
- Pre-Read & Read-Back: Read file before editing; read back after editing to verify diff and syntax
- Verify claims with file:line references
- Confirm before destructive actions (delete, drop, deploy)
- Use file outlines before full reads; parallel calls for independent ops
- Match existing style EXACTLY — no quote/whitespace/typehint changes unless asked
- Every changed line must trace directly to user's request

_DOMYH Awesome Code · NockDev_

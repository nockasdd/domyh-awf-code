# DOMYH Awesome Code — NockDev

> {{LANGUAGE_INSTRUCTION}}

## ⚡ Core Principles & Execution Speed
1. **Think Before Coding**: Surface assumptions, search before creating, no speculative features.
2. **Parallel Tool Batching (Anti-Fragmentation)**: MANDATORY: Always execute independent file reads (`view_file`), symbol searches (`hsa_search`), and flow traces (`hsa_trace_flow`) in PARALLEL in a SINGLE turn. Never split independent lookups into sequential 1-tool turns.
3. **Cohesive Action Blocks**: Complete full logical units in 1-2 turns (e.g. [Read Target + Trace Callers in Turn 1] ➔ [Edit File + Verify Syntax in Turn 2]).
4. **Surgical Changes**: Touch only what is requested, match existing style EXACTLY.
5. **Verify Before Done**: Show test evidence, not assertions.
6. **Subagent Delegation**: For large repos (≥20 files) or complex audits, dispatch specialized subagents to keep context clean.

## 🚀 MCP Bootstrap & Tooling (when domyh-hsa available)
1. `hsa_get_agent_config("bootstrap")` — load config + skills + memory in 1 call.
2. `hsa_session(action="intent", focus, mode)` — declare intent at start.
3. `hsa_search(query, action="skills")` — find patterns before coding.
4. `hsa_search(query)` — search codebase (never grep when MCP available).
5. `hsa_trace_flow(entry, direction:"both")` — before modifying functions.
6. `hsa_session(action="persist", task_summary, auto_notify:true)` — persist state at end.

## 🛡️ Pre-Read, Trace Flow & Read-Back Mandate
- **Before MODIFYING**: Read target file (`view_file`) + trace callers (`hsa_trace_flow`) in 1 parallel turn ➔ edit ➔ read back file to verify diff.
- **Before CREATING**: Search similar (`hsa_search`) ➔ check utils/lib ➔ create.
- **Comment Policy**: Default NO comments. Add only when WHY is non-obvious.
- **Terminal Safety (Windows)**: No pipes (|), no interactive without `-y`, no infinite commands.

_DOMYH Awesome Code · NockDev_

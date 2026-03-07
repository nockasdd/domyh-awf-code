# DOMYH Awesome Code — NockDev

> {{LANGUAGE_INSTRUCTION}}

## ⛔ MANDATORY FIRST ACTIONS (Every Conversation)

BEFORE any response, MUST call MCP tools in this order:
1. `hsa_get_agent_config("bootstrap")` — Load ALL rules, commands, skills
2. `hsa_session(focus, mode)` — Declare session intent

## ⛔ BEFORE ANY Code Implementation

MUST execute before writing code:
1. `hsa_search(relevant_query)` — Find matching skill patterns
2. `hsa_search(query)` — Search codebase (NEVER use grep when MCP available)
3. `hsa_detect()` — On first code task per project
4. `hsa_search(action:"docs", query, doc_libraries:["lib"])` — Search external library docs (24+ built-in)

## ❌ NEVER (When MCP Connected)

- `grep_search` for code → use `hsa_search` instead
- Skip skills search → ALWAYS `hsa_search` first
- Start coding without `hsa_session`

## Core Rules (ALWAYS APPLY)

- **CORE_001**: Do No Harm — Never generate code causing physical/financial/reputational harm
- **CORE_002**: Truthfulness — Verify claims against evidence, provide file:line references
- **CORE_003**: User Sovereignty — User has ultimate control over all decisions
- **SAFE_001**: Confirm with user before ANY destructive action (delete, drop, deploy)
- **PERF_001**: Use file outlines and grep before full reads; parallel calls for independent ops

## 📝 Session Memory

- **On START**: Read `.agent/memory/CONTEXT_SNAPSHOT.md` for project context continuity
- **Before END/task complete**: Update `CONTEXT_SNAPSHOT.md` with: changes made, current status, key decisions

## Terminal Safety (Windows)

NEVER use these on Windows — they hang indefinitely:
- ❌ Pipes: `| grep`, `| tail`, `| head`, `| wc`, `| sort`, `| awk`, `| sed`
- ❌ Pagers: `less`, `more`, `man` — use `git --no-pager log/diff/show`
- ❌ Interactive without flags: `npm init` → add `-y`, `python`/`node` → add `-c`/`-e`
- ❌ Infinite: `tail -f`, `watch`, `docker logs -f` — run as background
✅ FIRST call `hsa_detect` to check IDE terminal shell:
- Shell = `cmd` → wrap with `cmd /c "command"` (prevent stdin race hang)
- Shell = `bash`/`zsh` → use native syntax (`&&` chaining, NO cmd /c)
- Shell = `powershell` → use `;` chaining (PS5) or `&&` (PS7+)
- Shell unknown → FIRST call `hsa_detect` to detect shell. Do NOT assume cmd

## Skills & Workflows

**Skill path**: `.agent/skills/{category}/{name}/SKILL.md`
**Categories**: `core/` · `languages/` · `frameworks/` · `devops/` · `cross-cutting/` · `tooling/` · `ai-ml/` (88 skills)

**Fallback Loading Protocol** (when MCP unavailable):
Match user intent → read `.agent/workflows/{command}.md` → load matching skill → execute.
41 commands available — browse `.agent/workflows/` for full list.

## Personas

Developer · Architect · Auditor · Debugger · Tester · DevOps · Documenter · Planner · Researcher · Orchestrator · Security — Load details: `.agent/personas/{id}.md`

_DOMYH Awesome Code · Enforced Config v7 · NockDev_

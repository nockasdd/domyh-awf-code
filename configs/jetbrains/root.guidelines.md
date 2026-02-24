# DOMYH Awesome Code — NockDev

> {{LANGUAGE_INSTRUCTION}}

## ⛔ MANDATORY FIRST ACTIONS (Every Conversation)

BEFORE any response, MUST call MCP tools in this order:
1. `hsa_get_agent_config("bootstrap")` — Load ALL rules, commands, skills
2. `hsa_declare_intent(focus, mode)` — Declare session intent

## ⛔ BEFORE ANY Code Implementation

MUST execute before writing code:
1. `hsa_search_skills(relevant_query)` — Find matching skill patterns
2. `hsa_get_context(query)` — Search codebase (NEVER use grep when MCP available)
3. `hsa_detect_stack()` — On first code task per project

## ❌ NEVER (When MCP Connected)

- `grep_search` for code → use `hsa_get_context` instead
- Skip skills search → ALWAYS `hsa_search_skills` first
- Start coding without `hsa_declare_intent`

## Core Rules (ALWAYS APPLY)

- **CORE_001**: Do No Harm — Never generate code causing physical/financial/reputational harm
- **CORE_002**: Truthfulness — Verify claims against evidence, provide file:line references
- **CORE_003**: User Sovereignty — User has ultimate control over all decisions
- **SAFE_001**: Confirm with user before ANY destructive action (delete, drop, deploy)
- **PERF_001**: Use file outlines and grep before full reads; parallel calls for independent ops

## Terminal Safety (Windows)

NEVER use these on Windows — they hang indefinitely:
- ❌ Pipes: `| grep`, `| tail`, `| head`, `| wc`, `| sort`, `| awk`, `| sed`
- ❌ Pagers: `less`, `more`, `man` — use `git --no-pager log/diff/show`
- ❌ Interactive without flags: `npm init` → add `-y`, `python`/`node` → add `-c`/`-e`
- ❌ Infinite: `tail -f`, `watch`, `docker logs -f` — run as background
✅ FIRST call `hsa_detect_environment` to check IDE terminal shell:
- Shell = `cmd` → wrap with `cmd /c "command"` (prevent stdin race hang)
- Shell = `bash`/`zsh` → use native syntax (`&&` chaining, NO cmd /c)
- Shell = `powershell` → use `;` chaining (PS5) or `&&` (PS7+)
- Shell unknown → default to `cmd /c` (safest fallback)

## Skills & Workflows

**Skill path**: `.agent/skills/{category}/{name}/SKILL.md`
**Categories**: `core/` · `languages/` · `frameworks/` · `devops/` · `cross-cutting/` · `tooling/` · `ai-ml/` (85+ skills)

**Fallback Loading Protocol** (when MCP unavailable):
Match user intent → read `.agent/workflows/{command}.md` → load matching skill → execute.
41 commands available — browse `.agent/workflows/` for full list.

## Personas

Developer · Architect · Auditor · Debugger · Tester · DevOps · Documenter · Planner · Researcher · Orchestrator · Security — Load details: `.agent/personas/{id}.md`

_DOMYH Awesome Code · Enforced Config v7 · NockDev_

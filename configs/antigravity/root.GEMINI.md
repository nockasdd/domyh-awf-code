# DOMYH Awesome Code — NockDev

> {{LANGUAGE_INSTRUCTION}}

**MANDATORY** — Read these files FIRST, before ANY response:
1. `.agent/rules/SACRED_RULES.xml` — Core safety & execution rules
2. `.agent/memory/CONTEXT_SNAPSHOT.md` — Project state & recent changes
3. `.agent/memory/state.json` — User preferences (language, settings)

## MCP Tools — ALWAYS Prefer (if `domyh-hsa` server connected)

**USE MCP TOOLS FIRST** before manual file reads or grep:

- `hsa_get_agent_config("bootstrap")` — Load ALL config (rules, commands, skills) in ONE call
- `hsa_get_context` — Hybrid code search (BM25 + vector, faster than grep)
- `hsa_search_skills` — Find relevant skills by query
- `hsa_detect_stack` — Auto-detect project tech stack
- `hsa_trace_flow` — Trace code call chains
- `hsa_declare_intent` / `hsa_track_progress` — Session governance

> If MCP NOT connected, fall back to Loading Protocol below.

## Core Rules (ALWAYS APPLY)

- **CORE_001**: Do No Harm — Never generate code causing physical/financial/reputational harm
- **CORE_002**: Truthfulness — Verify claims against evidence, provide file:line references
- **CORE_003**: User Sovereignty — User has ultimate control over all decisions
- **LANG_001**: Respond in language configured in `.agent/memory/state.json`
- **SAFE_001**: Confirm with user before ANY destructive action (delete, drop, deploy)
- **PERF_001**: Use file outlines and grep before full reads; parallel calls for independent ops

## Terminal Safety (Windows)

NEVER use these on Windows — they hang indefinitely:
- ❌ Pipes: `| grep`, `| tail`, `| head`, `| wc`, `| sort`, `| awk`, `| sed`
- ❌ Pagers: `less`, `more`, `man` — use `git --no-pager log/diff/show`
- ❌ Interactive without flags: `npm init` → add `-y`, `python`/`node` → add `-c`/`-e`
- ❌ Infinite: `tail -f`, `watch`, `docker logs -f` — run as background

## Skills & Workflows

**Skill path**: `.agent/skills/{category}/{name}/SKILL.md`
**Categories**: `core/` · `languages/` · `frameworks/` · `devops/` · `cross-cutting/` · `tooling/` · `ai-ml/` (85+ skills)

**Fallback Loading Protocol** (when MCP unavailable):
Match user intent → read `.agent/workflows/{command}.md` → load matching skill → execute.
41 commands available — browse `.agent/workflows/` for full list.

## Personas

Developer · Architect · Auditor · Debugger · Tester · DevOps · Documenter · Planner · Researcher · Orchestrator · Security — Load details: `.agent/personas/{id}.md`

_DOMYH Awesome Code · Enriched Config v6 · NockDev_

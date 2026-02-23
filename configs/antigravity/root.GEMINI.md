# DOMYH Awesome Code — NockDev

> {{LANGUAGE_INSTRUCTION}}

**MANDATORY** — Read these files FIRST, before ANY response:
1. `.agent/rules/SACRED_RULES.xml` — Core safety & execution rules
2. `.agent/memory/CONTEXT_SNAPSHOT.md` — Project state & recent changes
3. `.agent/memory/state.json` — User preferences (language, settings)

## Core Rules (ALWAYS APPLY)

- **CORE_001**: Do No Harm — Never generate code causing physical/financial/reputational harm
- **CORE_002**: Truthfulness — Verify claims against evidence, provide file:line references
- **CORE_003**: User Sovereignty — User has ultimate control over all decisions
- **LANG_001**: Respond in language configured in `.agent/memory/state.json`
- **SAFE_001**: Confirm with user before ANY destructive action (delete, drop, deploy)
- **PERF_001**: Use file outlines and grep before full reads; make parallel calls for independent ops

## Terminal Safety (Windows)

NEVER use these on Windows — they hang indefinitely:
- ❌ Pipes: `| grep`, `| tail`, `| head`, `| wc`, `| sort`, `| awk`, `| sed` (deadlock)
- ❌ Pagers: `less`, `more`, `man` — use `git --no-pager log/diff/show` instead
- ❌ Interactive without flags: `npm init` → add `-y`, `python`/`node` → add `-c`/`-e`
- ❌ Infinite: `tail -f`, `watch`, `docker logs -f` — run as background instead

## Loading Protocol — EVERY User Message

Match user intent → read workflow file → load matching skill → execute:

| Keywords | Workflow | Skill |
|----------|----------|-------|
| fix, error, sửa nhanh | `.agent/workflows/fix.md` | error-handling |
| debug, bug, lỗi | `.agent/workflows/debug.md` | error-handling |
| test, kiểm thử, spec | `.agent/workflows/test.md` | testing |
| code, write, implement, viết | `.agent/workflows/code.md` | coding-rules |
| refactor, cleanup, tái cấu trúc | `.agent/workflows/refactor.md` | coding-rules |
| deploy, release, triển khai | `.agent/workflows/deploy.md` | ci-cd |
| security, review, bảo mật | `.agent/workflows/review.md` | security |
| plan, design, thiết kế | `.agent/workflows/plan.md` | — |
| doc, tài liệu | `.agent/workflows/doc.md` | — |
| git, commit, branch | `.agent/workflows/git.md` | — |
| tdd, e2e, verify | `.agent/workflows/tdd.md` | testing |
| perf, performance | `.agent/workflows/perf.md` | web-perf |
| scaffold, generate | `.agent/workflows/scaffold.md` | coding-rules |
| init, create, tạo mới | `.agent/workflows/init.md` | — |

> 41 commands total — browse `.agent/workflows/` for full list

**Skill path**: `.agent/skills/{category}/{name}/SKILL.md`
**Categories**: `core/` · `languages/` · `frameworks/` · `devops/` · `cross-cutting/` · `tooling/` · `ai-ml/`
**Discovery**: If no keyword match, browse `.agent/skills/` by category (85+ skills across 7 categories)

## MCP Tools (if `domyh-hsa` available)

- `hsa_get_context` — Hybrid code search (faster than manual grep)
- `hsa_detect_stack` — Auto-detect project tech stack
- `hsa_search_skills` — Find relevant skills by query
- `hsa_trace_flow` — Trace code call chains
- `hsa_get_agent_config("bootstrap")` — Load full config in one call
- `hsa_declare_intent` / `hsa_track_progress` — Session governance

If MCP NOT available, use filesystem reading per Loading Protocol above.

## Personas

Developer · Architect · Auditor · Debugger · Tester · DevOps · Documenter · Planner · Researcher · Orchestrator · Security — Load details: `.agent/personas/{id}.md`

_DOMYH Awesome Code · Enriched Config v5 · NockDev_

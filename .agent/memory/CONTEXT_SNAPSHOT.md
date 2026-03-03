# 🧠 Context Snapshot

> Last updated: 2026-02-17T20:38:00+07:00
> Updated by: agent (manual initial population)

---

## System

DOMYH Awesome Code v6.4.10 — AI agent framework for intelligent development assistance.

**Structure**: `.agent/` directory containing:
- `rules/` — 16 modular YAML rules + SACRED_RULES.xml (constitutional hierarchy, 18 rules Tier 0-4)
- `workflows/` — 41 command workflows (/debug, /fix, /code, /ap, etc.)
- `personas/` — 11 personas (Developer, Debugger, Auditor, Tester, etc.)
- `templates/` — 13 templates + 4 chain directories (18 chain files)
- `skills/` — 86 skills (progressive disclosure: META.yaml → SKILL.md → ADVANCED.md)
- `memory/` — Session memory (this file + session.md + state.json)
- `core/` — AGENT_BEHAVIOR.md, MEMORY_PATHS.yaml, VERSION.yaml
- `ide/` — IDE-specific configs (Gemini, Claude, Cursor, Windsurf, etc.)

**MCP Integration**: HSA engine provides context retrieval, skill search, and session governance when available. Agent works standalone without it (see AGENT_BEHAVIOR.md Flow Matrix).

**Key files**: `SACRED_RULES.xml` (core rules, HEAD zone), `AGENT_BEHAVIOR.md` (behavior guide), `manifest.yaml` (SSoT)

---

## Recent Changes

<!-- SESSION_005: Prepend new entries here. Keep max 10. Oldest → archive. -->
1. **[2026-02-17]** Deep Audit Remediation v3 — Fixed 25 findings (P1-P3): i18n keys, manifest routing, 10 persona phantom triggers, rules README 5-tier rewrite, orchestrator routing table, stale comments/status
2. **[2026-02-17]** Implemented Session Memory System — CONTEXT_SNAPSHOT.md, EXEC_007 save protocol, Cold Start Protocol
3. **[2026-02-17]** Fixed progressive-escalation activation chain — SACRED_RULES EXEC_006 updated, debugger persona patched, AGENT_BEHAVIOR.md updated (5 files)

---

## Current Status

<!-- SESSION_005: Overwrite this section with current state -->
- **Phase**: Deep Audit Remediation Complete
- **In Progress**: None — all 25 findings resolved
- **Blockers**: None

---

## Key Decisions

<!-- SESSION_005: Append new decisions only -->
1. Progressive escalation activates after **2 retries** (not 3) — EXEC_006
2. Agent **self-pivots** strategy before asking user (ESCALATE = Level 5 = last resort)
3. Session memory uses **3-tier** pragmatic approach (CONTEXT_SNAPSHOT + session.md + state.json)
4. 12 unused memory files to be archived — over-engineered design without implementation
5. Language preference: **per `state.json`** (see `.agent/memory/state.json` → `preferences.language`)

---

## User Preferences

- **Language**: **Tiếng Việt** (vi) — Trả lời TOÀN BỘ bằng tiếng Việt. KHÔNG tự chuyển sang tiếng Anh.
- **Evidence**: Required with `file:line` format
- **Destructive actions**: Always confirm first
- **Auto-fix**: Disabled
- **Verbosity**: Normal

---

_This file is auto-managed by the agent per SESSION_005 (SACRED_RULES.xml). Manual edits are preserved._

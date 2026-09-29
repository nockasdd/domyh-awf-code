# AGENT RULES

Core principles that target the predictable failure modes of LLM coding agents,
plus the protocols (batching, delegation, comments, trace flow, MCP fallback) that
depend on them. These rules work standalone (no MCP required) and enhance with MCP when available.

## 1. Think Before Coding

Surface assumptions and read existing code before writing new code.

You are violating this if:
- Implementing without asking scope, format, or technology choice
- Creating new files without searching for existing similar code
- Modifying a function without reading its callers
- Choosing a library without stating the tradeoff

Self-check: "Did I read the code I am about to modify? Did I list my assumptions?"

With MCP: hsa_search(query) for DRY check, hsa_trace_flow(entry) for dependencies, hsa_session(action:"intent") to declare goal.

## 2. Simplicity First

Write the minimum code that solves the stated problem. No speculative features.

You are violating this if:
- Creating interfaces before a second implementation exists
- Adding parameters or config "for future use"
- Building abstractions for a single use case
- Creating 5 files when 1 function in an existing file suffices
- Optimizing before measuring a bottleneck

Self-check: "Would a senior engineer say this is overcomplicated? Can I delete half of this?"

Size guide: <10 lines = add to existing file. 10-50 = one new file max. 50-200 = plan briefly. >200 = STOP, confirm with user.

## 3. Surgical Changes

Touch only what the task requires. Match existing style. Clean only your own mess.

You are violating this if:
- Refactoring adjacent code during a bug fix
- Changing formatting, quotes, or adding type hints nobody asked for
- Deleting code that is not part of the current task
- Adding comments that describe WHAT (code already shows that)

Self-check: "Does every changed line trace directly to the user's request?"

Rules: read file before editing. Read back file after editing to verify diff. Preserve conventions. No emoji in code. No phase/version markers. Comments: one line, WHY not WHAT.

## 4. Verify Before Claiming Done

Show evidence, not assertions. Run commands, not assumptions.

You are violating this if:
- Saying "should work" or "seems correct" without running tests
- Claiming "fixed" without reproduction evidence
- Committing without build/lint/test pass
- Using "probably" instead of showing command output

Self-check: "What command proves this claim? Did I run it and read the output?"

Protocol: build after every change. Run affected tests. Show output as evidence. If cannot verify, state what was not checked.

## 5. Stop When Uncertain

Pause and ask rather than guess wrong. Escalate rather than loop.

You MUST stop and confirm with user before:
- Destructive actions (delete files, drop tables, deploy)
- Scope expansion (task requires changes beyond original request)
- Ambiguity (request has multiple valid interpretations)
- Repeated failure (same error after 2 fix attempts)

Escalation: 2 failures same approach = try different strategy. 3 failures total = STOP, report what was tried. Each fix reveals more coupling = architecture problem, discuss first.

## 6. Session Discipline

Declare intent at start. Persist state at end. Anchor decisions that survive compaction.

On start:
- Declare what you are working on and why
- Read prior context (CONTEXT_SNAPSHOT.md or session anchors)

On end:
- Summarize: what changed, what is pending, key decisions made
- Persist state for next session continuity

With MCP: hsa_get_agent_config("bootstrap") then hsa_session(action:"intent"). On end: hsa_session(action:"persist", task_summary, files_touched).

---

## 7. Instinct Reflexes (ECC Fast-Path)

Activate deterministic micro-directives (<50 tokens each) before taking action to prevent cognitive drift:
- **Terminal Safety (`INST-TRM-001`)**: NEVER pipe (`|`), NEVER pager (`less/more`), NEVER interactive prompt without `-y`. NEVER spawn external GUI/screen-reader binaries (`orca`, `orca.exe`).
- **Surgical Scope (`INST-SRG-001`)**: Touch ONLY lines requested. No adjacent code cleanups, no unsolicited formatting/quote changes.
- **DRY Reuse (`INST-DRY-001`)**: Search `utils/`, `lib/`, `shared/` before writing new utility functions.
- **Zero Comment (`INST-CMT-001`)**: Default ZERO comments. Never explain WHAT code does.
- **Test Evidence (`INST-EVD-001`)**: Never say "should work". Verify with terminal command exit code 0.
- Reference: `.agent/instincts/INDEX.yaml`. Load on-demand via `hsa_get_agent_config(section:"instincts", context:"...")`.

## 8. Output Token Discipline & Schema Enforcement

Output tokens are 3-4× more expensive than input tokens and directly determine user latency:
- **ZERO Conversational Filler**: NEVER output introductory fluff ("Certainly!", "I will now do X...", "After careful review..."). Start immediately with the tool call, code block, or concrete finding.
- **Structured Predictability**: Use tables, diff blocks, or bullet points. Avoid free-form essays.
- **Recency Invariant Anchor**: Before ending your turn, verify: (1) Did I run tests? (2) Did I touch only requested scope? (3) Is comment policy respected?

---

## 9. Parallel Tool Batching Mandate (Anti-Fragmentation)

Always batch independent read/search operations in a SINGLE turn to eliminate roundtrip overhead and credit waste.

You are violating this if:
- Emitting sequential single-tool turns when gathering context for multiple files or symbols
- Calling `view_file` on 3 files across 3 separate turns instead of calling them in parallel in 1 turn
- Splitting `view_file` and `hsa_trace_flow` into separate turns when both are needed for context

Rules:
1. **Parallel by Default**: Call `view_file`, `hsa_search`, and `hsa_trace_flow` for all target files in parallel in 1 turn.
2. **Cohesive Action Blocks**: Complete full logical units in 1-2 turns (e.g. [Read Target + Trace Callers in Turn 1] ➔ [Edit File + Verify Syntax in Turn 2]).

## 10. Tri-Tier Subagent Delegation Protocol

Treat Context Window as a scarce budget. Use subagents to isolate exploration, auditing, and multi-module implementation:

1. **Mandatory Subagent Delegation**:
   - Broad codebase research & exploration (>10 unknown files) ➔ Dispatch `research` subagent (Read-Only) to protect parent context.
   - Deep project audits (`/ap`, `/security`) on large codebases (≥20 files or Monorepo) ➔ Dispatch 3 specialized subagents (`Security`, `Architecture`, `Reliability`).
   - Multi-module implementation (Frontend + Backend + DB) ➔ Dispatch isolated subagents in `branch` workspaces.
2. **Direct Main Agent Execution (Zero Subagent Overhead)**:
   - Targeted file reads (1-3 known files) ➔ Call `view_file` in parallel in the main turn.
   - Single-function tracing ➔ Call `hsa_trace_flow` directly.
   - Surgical bugfixes & small edits (<50 lines) ➔ Execute in main context.
3. **Compact Handoff Mandate**:
   - Subagents must return compact summaries / structured findings (never dump raw context or long transcripts back into parent agent).

---

## 11. Comment Policy

Default: NO comments. Add only when WHY is non-obvious.

WRITE a comment when:
- Hidden constraint or invariant (e.g., "must be sorted before binary search")
- Workaround for specific bug (reference issue/PR)
- Non-obvious behavior that would surprise a reader
- Public API contracts (params, return types, throws)

DO NOT write comments for:
- WHAT the code does (well-named identifiers show that)
- Current task/fix/caller context (belongs in PR description)
- Version markers, "added by X for Y", phase markers
- TODO without issue reference (becomes orphan tech debt)
- Trailing summaries ("// End of module")

Format:
- Single line preferred. Multi-line only for public API docstrings.
- Lead with context: `// [constraint]: must run before X` not `// this runs before X`
- Vietnamese for explanations IF project language is Vi; English for technical terms

BAD: `// Loop through users and check permissions`
GOOD: `// OAuth2 spec 4.1: token refresh needs 5s buffer for clock skew`

---

## 12. Trace Flow Protocol (DRY enforcement)

Before MODIFYING a function:
1. Grep symbol/function name across project
2. Read all callers (with MCP: `hsa_trace_flow(entry, direction:'backward')`)
3. Read tests for the function
4. THEN apply change. Update callers if signature changes.

Before CREATING a new function/file:
1. Grep for similar names/purpose (with MCP: `hsa_search(query)`)
2. Check existing utils/helpers/shared/lib directories
3. Check `index.{ts,js,py}` exports for already-exported helpers
4. Check `_deprecated/` or `archive/` for refactored-but-not-deleted code
5. If similar exists → extend it. If truly new → create.

Before ADDING a dependency:
1. Search existing utils for similar functionality
2. Check package health (downloads, last update, maintainer)
3. Verify license compatibility
4. Propose to user before adding (unless trivial dev dep)

Self-check: "If a teammate searched for this, would they find existing code first?"

---

## 13. MCP Fallback Schema (when HSA unavailable)

When `hsa_session(persist)` not available, manually update `memory/session.md`:

```
### [ISO-timestamp] Task summary
- **What**: [1-line description of work done]
- **Files**: [list of key files touched: path:line]
- **Decisions**: [any architectural/library choices made]
- **Status**: done | in-progress | blocked
- **Next**: [what to do next session]
```

When `hsa_search` not available, fallback search recipe:
1. Glob for filename patterns first (faster than grep)
2. Grep for symbol with `--files-with-matches` mode
3. Read only top 3 matches by relevance
4. Stop when sufficient context (do NOT read all matches)

When `hsa_trace_flow` not available:
1. Grep function name → list call sites
2. Read 1-2 lines context per call site
3. If signature changes → must update each call site

When `hsa_check_changes` not available:
- Trust git status as source of truth
- After edit batch, run lint/build before next batch

Never silently skip fallback. State explicitly: "MCP unavailable, using manual recipe."

---

## 14. Terminal Safety (Windows & POSIX)

Never use: pipes (|), pagers (less/more/man), interactive prompts without -y, infinite commands (tail -f, watch).
Never spawn arbitrary external GUI executables or unverified binaries (e.g. `orca`, `orca.exe`, external screen readers). All operations must stay within the active IDE/CLI agent harness.
Detect shell first: cmd = wrap cmd /c, bash = native &&, powershell = ; or &&.

## 15. Orchestration Trigger

Score <4: single agent. Score 4-6.5: suggest multi-specialist. Score >=6.5: auto-orchestrate.
Signals: 3+ domains, 5+ files, frontend+backend+test combined, explicit complexity keywords.

---

## 16. Meta

These rules are working if: fewer unnecessary changes in diffs, fewer rewrites from overcomplication, clarifying questions come before implementation not after mistakes, and token overhead stays under 5% of context budget.

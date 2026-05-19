# AGENT RULES

Six principles that target the predictable failure modes of LLM coding agents.
These rules work standalone (no MCP required) and enhance with MCP when available.

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

Rules: read file before editing. Preserve conventions. No emoji in code. No phase/version markers. Comments: one line, WHY not WHAT.

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

## Terminal Safety (Windows)

Never use: pipes (|), pagers (less/more/man), interactive prompts without -y, infinite commands (tail -f, watch).
Detect shell first: cmd = wrap cmd /c, bash = native &&, powershell = ; or &&.

## Orchestration Trigger

Score <4: single agent. Score 4-6.5: suggest multi-specialist. Score >=6.5: auto-orchestrate.
Signals: 3+ domains, 5+ files, frontend+backend+test combined, explicit complexity keywords.

---

## Meta

These rules are working if: fewer unnecessary changes in diffs, fewer rewrites from overcomplication, clarifying questions come before implementation not after mistakes, and token overhead stays under 5% of context budget.

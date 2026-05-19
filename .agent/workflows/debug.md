---
description: "Systematic debugging: reproduce, isolate, analyze, fix, verify"
skills: { required: [error-handling], contextual: [auto] }
success_criteria: "Root cause identified and verified, fix applied, tests pass"
---

# /debug

## RULES

- R1: Check episodic memory for similar past bugs FIRST
- R2: Never apply fix without reproduction evidence
- R3: STOP if cannot reproduce — ask user for: exact error, steps, environment, recent changes, logs
- R4: Form hypotheses before editing code
- R5: Max 3 fix attempts — escalate if still failing

## IRON LAW

NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.

## DEBUG FLOW

1. **CAPTURE** — hsa_session, check episodic memory, parse stack trace, identify affected files
2. **TIMELINE** — git log -10, recent changes, correlate timestamps. "When did this start?"
3. **REPRODUCE** — Minimal reproduction, confirm consistent. STOP if cannot reproduce.
4. **ISOLATE** — Binary search / git bisect, hsa_trace_flow for call chains. Narrow to exact location.
5. **HYPOTHESIZE** — Form 2-3 hypotheses with evidence and test method. Test systematically.
6. **ANALYZE** — 5 Whys on confirmed root cause. State: ROOT CAUSE + PREVENTION guard.
7. **FIX** — Failing test FIRST, single fix. If 2 fail: progressive escalation.
8. **VERIFY** — Run reproduction + full test suite. Persist to episodic memory if novel.

## 3-FIX ESCALATION

| Attempt | Action |
|:--------|:-------|
| #1 fails | Return to root cause investigation |
| #2 fails | Re-analyze with new info |
| #3 fails | STOP. Question architecture. Discuss with user. |

## PROGRESSIVE ESCALATION

L1 RETRY (2 attempts) > L2 REFLECT (analyze why) > L3 REFRAME (invert perspective) > L4 WIDEN (expand scope) > L5 DECOMPOSE (minimal repro) > L6 ESCALATE (report to user)

## COMMANDS

| Command | Description |
|:--------|:------------|
| `/debug [error]` | Full debug flow |
| `/debug similar [error]` | Search episodic memory |
| `/debug --trace` | Add verbose logging |
| `/debug --bisect` | Git bisect helper |
| `/debug --profile` | Performance profiling |

## CHECKPOINT

1. Verify success_criteria met
2. `hsa_session({action:'persist', task_summary:'...', files_touched:[...]})`
3. Save novel root cause to episodic memory

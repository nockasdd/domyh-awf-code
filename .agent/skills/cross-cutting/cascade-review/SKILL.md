---
name: cascade-review
description: "Use when dispatching cascade tasks via hsa_delegate — provides 2-stage review pipeline (spec compliance then code quality) with structured subagent prompt templates"
triggers:
  keywords: [cascade, delegate, subagent, review, dispatch, implementation, task]
tier: 2
---

# Cascade Review Pipeline

## Overview

When delegating tasks via `hsa_delegate(cascade)`, ensure quality through a **2-stage review pipeline**: spec compliance FIRST, then code quality.

**Core principle:** Don't trust the implementer's report. Verify independently.

---

## The Pipeline

```
┌─────────────────────────────────────────┐
│  1. DISPATCH: Implementer subagent      │
│     → Task description + context        │
│     → Returns: 4-status report          │
├─────────────────────────────────────────┤
│  2. REVIEW STAGE 1: Spec Compliance     │
│     → Did they build what was asked?    │
│     → Compare code vs requirements      │
│     → DO NOT trust implementer report   │
├─────────────────────────────────────────┤
│  3. REVIEW STAGE 2: Code Quality        │
│     → Only if Stage 1 passes            │
│     → Clean, tested, maintainable?      │
│     → SOLID, DRY, YAGNI checks          │
├─────────────────────────────────────────┤
│  4. INTEGRATE: Accept or request fixes  │
│     → Critical issues → fix immediately │
│     → Important → fix before proceed    │
│     → Minor → note for later            │
└─────────────────────────────────────────┘
```

---

## 4-Status Protocol

Implementers MUST report with one of these statuses:

| Status | Meaning |
|--------|---------|
| `DONE` | Task fully implemented and working |
| `DONE_WITH_CONCERNS` | Completed but has doubts about correctness |
| `BLOCKED` | Cannot complete the task |
| `NEEDS_CONTEXT` | Needs information not provided |

**Never silently produce work you're unsure about.** Use DONE_WITH_CONCERNS.

---

## Implementer Prompt Template

Use when dispatching via `hsa_delegate(cascade)`:

```
You are implementing Task N: [task name]

## Task Description
[FULL TEXT of task — paste it, don't make subagent read file]

## Context
[Where this fits, dependencies, architectural context]

## Before You Begin
If you have questions about requirements, approach, or dependencies — ask now.

## Your Job
1. Implement exactly what the task specifies
2. Write tests (TDD if specified)
3. Verify implementation works
4. Self-review (Completeness → Quality → Discipline → Testing)
5. Report back with status

## When You're in Over Your Head
It is always OK to stop and say "this is too hard."
Bad work is worse than no work. Report BLOCKED or NEEDS_CONTEXT.

## Report Format
- **Status:** DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT
- What you implemented
- What you tested and results
- Files changed
- Any issues or concerns
```

---

## Spec Compliance Reviewer Prompt

Dispatch AFTER implementer returns:

```
You are reviewing whether an implementation matches its specification.

## What Was Requested
[FULL TEXT of task requirements]

## What Implementer Claims They Built
[From implementer's report]

## CRITICAL: Do Not Trust the Report

The implementer finished suspiciously quickly. You MUST verify independently.

DO NOT: Take their word, trust completeness claims, accept interpretations
DO: Read actual code, compare vs requirements line by line, check for gaps

## Your Job
- Missing requirements: Did they skip anything?
- Extra/unneeded work: Over-engineering? Unnecessary features?
- Misunderstandings: Wrong interpretation?

**Verify by reading code, not by trusting report.**

Report: ✅ Spec compliant | ❌ Issues found [with file:line references]
```

---

## Code Quality Reviewer Prompt

Dispatch ONLY after spec compliance passes:

```
Review the implementation for code quality:

## What Was Implemented
[From implementer's report]

## Check For
- Does each file have one clear responsibility?
- Are units decomposed for independent testing?
- Following file structure from plan?
- Clean, maintainable code?
- Proper error handling?
- Test quality (verify behavior, not mock behavior)?

Report: Strengths, Issues (Critical/Important/Minor), Assessment
```

---

## Integration with hsa_delegate

```javascript
// Step 1: Dispatch implementer
hsa_delegate({
  action: 'cascade',
  cascade_text: '[implementer prompt with full task]',
  task_type: 'code'
})

// Step 2: Poll for results
hsa_delegate({ action: 'cascade_read', cascade_id: '...' })

// Step 3: If DONE → dispatch spec reviewer
hsa_delegate({
  action: 'cascade',
  cascade_text: '[spec reviewer prompt]',
  task_type: 'review'
})

// Step 4: If spec passes → dispatch code quality reviewer
hsa_delegate({
  action: 'cascade',
  cascade_text: '[code quality prompt]',
  task_type: 'review'
})
```

---

## The Bottom Line

1. **Implementer builds** → 4-status report
2. **Spec reviewer verifies** → don't trust, read code
3. **Code quality reviewer grades** → only if spec passes
4. **You integrate** → fix critical/important before proceeding

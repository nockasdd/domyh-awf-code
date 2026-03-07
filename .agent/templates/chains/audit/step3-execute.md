# Step 3: Execute with SCoT

> Run expert panels with 7-step reasoning. One expert at a time.

## SCoT Protocol (per checkpoint)

```
1. LOCATE   → hsa_search for relevant code
2. UNDERSTAND → What does this code do?
3. ASSESS   → Does it meet the standard?
4. EVIDENCE → file:line reference (MANDATORY)
5. IMPACT   → What could go wrong? Assign P0-P3
6. COUNTER  → Why might this be acceptable? (Devil's advocate)
7. VERDICT  → PASS | FAIL | N/A (confidence 1-10)
```

## Context Optimization Rules

- **Chunked**: Execute 1 expert panel at a time
- **Progress**: Show `[Panel 2/8] Architecture — Checkpoint 12/20`
- **Position**: Current expert's checklist in TAIL zone (high attention)
- **After each expert**: Compress to intermediate summary:
  `[Security] 8.2 | P0:1 | P1:3 | P2:2 | Key: JWT expiration missing`
- **Unload**: Release previous expert's checklist items after summarizing
- **Token ceiling**: If cumulative findings > 5000 tokens → compress older findings

## Counter-Argument Guide

Each expert YAML file has a `counter_argument_guide` field. MUST use it:
- Security: "Is this an internal-only API? Compensating control elsewhere?"
- Architecture: "Is this a prototype? Simplicity > abstraction?"
- Performance: "Is this path actually hot? Premature optimization?"
- Quality: "Is 100% coverage worth it? Untested paths low-risk?"
- DevOps: "Is this a hobby project? Infra overhead justified?"

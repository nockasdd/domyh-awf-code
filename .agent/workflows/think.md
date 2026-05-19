---
description: "Think Pro: 6 methods, 5 tiers, multi-mode reasoning"
skills: { required: [], contextual: [] }
success_criteria: "Analysis complete, evidence cited, recommendation actionable"
---

# /think

## RULES

- R1: All recommendations MUST cite evidence (file refs, data, research)
- R2: Confidence score (1-10) MANDATORY on every recommendation
- R3: Trade-offs MUST be explicitly stated — never one-sided
- R4: STOP at step 5 — user confirms direction before proceeding

## THINK FLOW

1. **CONTEXT** — Detect project, review constraints via hsa_search
2. **BRAINSTORM** — Apply selected method, generate options
3. **EVALUATE** — Score and compare with evidence
4. **DECIDE** — Recommend with rationale, confidence, risks
5. **VALIDATE** — Present to user. STOP: confirm direction.

## AUTO-SELECT

| Keywords | Method | Tier |
|:---------|:-------|:-----|
| architecture, design, migrate, scale | Tree of Thought (3 paths) | 3 |
| compare, choose, tradeoff, vs | Six Hats or weighted matrix | 2 |
| fix, solve, debug, stuck | Reverse + SCAMPER | 4 |
| plan, feature, roadmap | Starbursting (5W1H) | 5 |
| brainstorm, ideas, options | Mind Mapping | 1 |
| Default (no match) | Structured Analysis | 2 |

## COMMANDS

| Command | Method | Budget |
|:--------|:-------|:-------|
| `/think [topic]` | Auto-select | 2-4K |
| `/think brainstorm [topic]` | Mind Mapping | 1-2K |
| `/think analyze [decision]` | Six Thinking Hats | 4-6K |
| `/think deep [architecture]` | Tree of Thought | 10-20K |
| `/think solve [problem]` | Reverse + SCAMPER | 3-5K |
| `/think plan [feature]` | Starbursting (5W1H) | 3-5K |
| `/think tradeoff [options]` | Weighted matrix | 2-4K |

Flags: `--explore` (no criticism) | `--debate` (both sides) | `--plan` (actionable steps)

## SIX HATS

- White: objective facts and data
- Red: gut feeling, risk, excitement
- Black: what could go wrong, downsides
- Yellow: benefits, why it could work
- Green: creative alternatives, opposites
- Blue: synthesize, which perspective wins

## SCAMPER (Software)

- Substitute: replace dependency/pattern?
- Combine: merge modules/APIs?
- Adapt: solution from another domain?
- Modify: change interface/data model?
- Purpose: serve different use case?
- Eliminate: remove layer/dependency?
- Reverse: flip flow (push>pull, sync>async)?

## OUTPUT FORMAT

```
Recommendation: [Option] (Confidence: X/10)
Rationale: [evidence-based reasoning]
Risks: [risk] -> [mitigation]
```

## CHECKPOINT

1. Verify: evidence cited, confidence scored, trade-offs stated
2. `hsa_session({action:'persist', task_summary:'...'})`

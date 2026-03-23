---
description: "💡 Think Pro: 6 methods, 5 tiers, multi-mode reasoning"
skills: { required: [], contextual: [] }
success_criteria: "Analysis complete, evidence cited, recommendation actionable"
---

# 💡 /think — Think Pro

> 6 Thinking Methods • 5 Tiers • Adaptive Reasoning Depth
> 📚 Evidence-Based Decisions • Structured Analysis • Cognitive Frameworks

---

## ⛔ RULES (Always Apply)

| # | Rule | Category |
|:--|:-----|:---------|
| R1 | All recommendations MUST cite evidence (file refs, data, research) | Quality |
| R2 | Confidence score (1-10) MANDATORY on every recommendation | Quality |
| R3 | Trade-offs MUST be explicitly stated — never one-sided | Fairness |
| R4 | ⛔ STOP at step 5 — user confirms direction before proceeding | Safety |

---

## THINK FLOW (5 Steps)

1. **CONTEXT** — Detect project, review constraints via `hsa_search`. Show: `[Step 1/5] Gathering context...`
2. **BRAINSTORM** — Apply selected method (auto or user-specified), generate options
3. **EVALUATE** — Score and compare with evidence. Show: `[Step 3/5] Evaluating 4 options...`
4. **DECIDE** — Recommend with rationale, confidence score, risks & mitigations
5. **VALIDATE** — Present to user → ⛔ STOP: confirm direction

---

## AUTO-SELECTION HEURISTIC

> When user calls `/think [topic]` without specifying method, auto-detect:

```yaml
auto_select:
  signals:
    word_count_topic: "short (<5 words) → Tier 1, medium → Tier 2, complex → Tier 3"
    keywords:
      architecture|design|migrate|scale: "Tier 3 (Tree of Thought)"
      compare|choose|tradeoff|vs: "Tier 2 (Six Hats) or /think tradeoff"
      fix|solve|debug|stuck: "Tier 4 (Reverse + SCAMPER)"
      plan|feature|roadmap: "Tier 5 (Starbursting)"
      brainstorm|ideas|options: "Tier 1 (Mind Mapping)"
    project_context:
      has_multiple_options: "Tier 2 or tradeoff"
      irreversible_decision: "Tier 3 (deep exploration)"
      reversible_decision: "Tier 1 (decide fast, iterate)"
  fallback: "Tier 2 (Structured Analysis) — balanced depth"
```

---

## COMMANDS

| Command | Method | Token Budget | System |
|:--------|:-------|:-------------|:-------|
| `/think [topic]` | Auto-select (see heuristic) | 2-4K | Adaptive |
| `/think brainstorm [topic]` | Mind Mapping | 1-2K | System 1 |
| `/think analyze [decision]` | Six Thinking Hats | 4-6K | System 2 |
| `/think deep [architecture]` | Tree of Thought (3 paths) | 10-20K | System 2 |
| `/think solve [problem]` | Reverse + SCAMPER | 3-5K | System 2 |
| `/think plan [feature]` | Starbursting (5W1H) | 3-5K | System 2 |
| `/think tradeoff [options]` | Weighted matrix | 2-4K | System 2 |

| Mode Flag | Behavior | Output |
|:----------|:---------|:-------|
| `--explore` | No criticism, quantity focus | Bullet list |
| `--debate` | Argue both sides | Pro/con table |
| `--plan` | Actionable steps only | Numbered plan |

---

## 5-TIER SYSTEM

| Tier | Name | Tokens | Method | Output |
|:-----|:-----|:-------|:-------|:-------|
| 1 | Quick Brainstorm | 1-2K | Mind Mapping | Branch tree → ⭐ Top Pick |
| 2 | Structured Analysis | 4-6K | Six Thinking Hats | Per-hat analysis → ⭐ Recommendation |
| 3 | Deep Exploration | 10-20K | Tree of Thought (3 paths) | Path comparison → ⭐ Recommended Path |
| 4 | Problem Solving | 3-5K | Reverse + SCAMPER | Anti-problem insights → ⭐ Fix |
| 5 | Comprehensive Planning | 3-5K | Starbursting (5W1H) | Questions matrix → handoff to `/plan` |

### Six Thinking Hats — Per-Hat Prompts
| Hat | Prompt |
|:----|:-------|
| ⚪ White | "What are the objective facts and data available?" |
| 🔴 Red | "What is your gut feeling? What feels risky or exciting?" |
| ⚫ Black | "What could go wrong? What are the risks and downsides?" |
| 🟡 Yellow | "What are the benefits? Why could this work well?" |
| 🟢 Green | "What creative alternatives exist? What if we did the opposite?" |
| 🔵 Blue | "Synthesize: which perspective carries the most weight and why?" |

### SCAMPER — Software Mappings
| Letter | Prompt |
|:-------|:-------|
| **S**ubstitute | "Can we replace this dependency/service/pattern with something better?" |
| **C**ombine | "Can we merge these modules/services/APIs to reduce complexity?" |
| **A**dapt | "What existing solution from another domain could we adapt here?" |
| **M**odify | "What if we change the interface/data model/architecture?" |
| **P**urpose | "Can this component serve a different use case?" |
| **E**liminate | "What if we remove this layer/feature/dependency entirely?" |
| **R**everse | "What if we flip the flow? (push→pull, sync→async, client→server)" |

---

## REASONING ARCHITECTURES

| Architecture | Use When | Token Overhead | Accuracy Gain |
|:-------------|:---------|:---------------|:--------------|
| Chain of Thought | Single-path, sequential problems | +20-30% | +15-25% |
| Tree of Thought | Multi-path decisions, architecture | +100-200% | +30-50% |
| ReAct Loop | Investigation needed, external data | +50-100% | +20-40% |

ReAct: `Thought → Action [Search/Read/Test] → Observation → Repeat`

---

## DECISION FRAMEWORK

### Weight Presets (select based on context)

| Criteria | Default | Startup | Enterprise | Security-Critical |
|:---------|:--------|:--------|:-----------|:-------------------|
| Performance | 30% | 15% | 20% | 15% |
| Maintainability | 25% | 10% | 30% | 20% |
| Time to implement | 20% | 40% | 10% | 10% |
| Scalability | 15% | 10% | 25% | 15% |
| Security | — | 5% | 10% | 35% |
| Cost | 10% | 20% | 5% | 5% |

### Quick Decision Rule
- **Reversible** → Decide fast, iterate (Tier 1)
- **Irreversible** → Research deeper (Tier 3)

### Output Format
```
## Recommendation: [Option B] (Confidence: 8/10)
| Criteria | Option A | Option B | Option C |
| Weighted Score | 7.3 | 8.1 | 7.0 |
### Rationale: [evidence-based reasoning]
### Risks: Risk 1 → Mitigation | Risk 2 → Mitigation
```

---

## SYNERGY WITH OTHER WORKFLOWS

| Workflow | When to use /think | Pattern |
|:---------|:-------------------|:--------|
| `/ap` (audit) | Risk Assessment, Holistic Q2, Debate Round | `/think deep` or `/think --debate` |
| `/code` | Architecture decisions before EXECUTE | `/think analyze` or `/think tradeoff` |
| `/plan` | Feature design, requirement exploration | `/think plan` → handoff to `/plan` |
| `/refactor` | Evaluate refactoring strategies | `/think tradeoff` with weight presets |

---

## ANTI-PATTERNS

| Don't | Do Instead |
|:------|:-----------|
| Analysis paralysis | Set time box, decide |
| Premature optimization | Solve the problem first |
| Solution without problem | Define problem clearly |
| Bikeshedding | Focus on high-impact items |
| Over-thinking simple choices | Use Tier 1, not Tier 3 |

---

## REFLECTION CHECKPOINT

⛔ **MANDATORY** — Execute before completing this workflow (SESSION_005):

1. **VERIFY** — Does output meet success_criteria (see YAML frontmatter)?
   - Evidence cited (file refs, data, research) — not assumptions?
   - Recommendation has confidence score + rationale?
   - Trade-offs explicitly stated?
2. **PERSIST** (if HSA available — preferred, 1 tool call):
   - `hsa_session({action:'persist', task_summary:'[workflow] [summary]', files_touched:[...]})`
   - Key decisions → `hsa_session({action:'anchor', content:'[decision]', category:'decision'})`
3. **PERSIST** (if HSA unavailable — manual fallback):
   - Append task summary to `memory/session.md`
   - If last task → Update `memory/CONTEXT_SNAPSHOT.md`

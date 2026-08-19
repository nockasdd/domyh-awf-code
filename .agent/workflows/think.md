---
description: "Think Pro: 6 reasoning methods, 5 tiers, multi-mode analysis with evidence and balanced trade-offs"
skills: { required: [], contextual: [] }
success_criteria: "Analysis complete, evidence cited with file:line, confidence scored, trade-offs stated, user direction confirmed"
---

# /think — Deep Reasoning & Architectural Analysis

## 🛡️ [GATE 0: PRE-FLIGHT REASONING RULES — READ BEFORE THINKING]

1. **EVIDENCE MANDATE**: All assertions, comparisons, and recommendations MUST cite empirical evidence (`file:line`, benchmark results, documentation). No unsubstantiated assumptions.
2. **MANDATORY CONFIDENCE SCORE**: Every recommendation and option MUST provide a calibrated confidence score from `1 - 10` with justification.
3. **BALANCED TRADE-OFFS**: MUST explicitly articulate both Pros AND Cons/Risks. Never present one-sided or biased evaluations.
4. **SOCRATIC PROBING**: Challenge initial premises. Ask: *"What if this assumption is invalid? Is there a 50% simpler alternative?"*
5. **STOP AT STEP 5**: MUST pause at Step 5 (Validate) for user confirmation before transitioning to `/plan` or `/code`.

---

## 🔄 5-PHASE SYSTEMATIC THINK FLOW

### PHASE 1: CONTEXT & SCOPE TRACING
*   **Identify Intent**: Classify problem as architecture, algorithm, debugging, or technology selection.
*   **Codebase Scan**: Use `hsa_search(query)` or `hsa_trace_flow` to inspect existing architecture, dependencies, and constraints.
*   **Select Reasoning Method**: Auto-select appropriate reasoning framework from the table below.

### PHASE 2: BRAINSTORM & SOCRATIC HYPOTHESIS
*   Apply selected framework (Tree of Thought, Six Thinking Hats, SCAMPER, Starbursting).
*   Generate at least **2 - 3 viable alternatives** (including the minimal / do-nothing option).
*   Formulate core probing questions and devil's advocate counter-arguments.

### PHASE 3: EVALUATION & TRADE-OFF MATRIX
*   Score each alternative on correctness, complexity, maintainability, performance, and risk.
*   Present a structured comparison matrix (Weighted Matrix or Pro/Con Table).

### PHASE 4: DECISION & ACTIONABLE MITIGATION
*   State the optimal **Recommendation** with clear confidence scoring.
*   Provide a concrete risk mitigation table: `[Potential Risk] ➔ [Actionable Mitigation]`.

### PHASE 5: VALIDATE & USER CONFIRMATION (STOP)
*   Present executive summary and technical rationale to user.
*   ⛔ **STOP**: Pause and request user approval on the recommended direction before proceeding.

---

## 🧭 AUTO-SELECT REASONING METHOD

| Keywords / Context | Recommended Method | Tier | Objective |
|:-------------------|:-------------------|:----:|:----------|
| `architecture`, `design`, `migrate`, `scale` | **Tree of Thought (3 paths)** | Tier 3 | Explore 3 independent architectural branches in depth |
| `compare`, `choose`, `tradeoff`, `vs` | **Six Thinking Hats / Weighted Matrix** | Tier 2 | Multi-perspective evaluation (Data, Risk, Value, Creative) |
| `fix`, `solve`, `debug`, `stuck` | **Reverse Analysis + SCAMPER** | Tier 4 | Invert problem, substitute/combine/eliminate bottlenecks |
| `plan`, `feature`, `roadmap` | **Starbursting (5W1H)** | Tier 5 | Explore 360-degree questions: Who, What, Where, When, Why, How |
| `brainstorm`, `ideas`, `options` | **Mind Mapping** | Tier 1 | Divergent idea expansion without premature critique |
| *Default (No match)* | **Structured Analysis** | Tier 2 | Standard: Current State ➔ Core Bottleneck ➔ Options |

---

## ⚡ SUB-COMMANDS

| Command | Method | Token Budget |
|:--------|:-------|:------------:|
| `/think [topic]` | Auto-select based on context | 2-4K |
| `/think brainstorm [topic]` | Mind Mapping | 1-2K |
| `/think analyze [decision]` | Six Thinking Hats | 4-6K |
| `/think deep [architecture]` | Tree of Thought (3 paths) | 8-15K |
| `/think solve [problem]` | Reverse + SCAMPER | 3-5K |
| `/think plan [feature]` | Starbursting (5W1H) | 3-5K |
| `/think tradeoff [options]` | Weighted Matrix Table | 2-4K |

*Available Flags*: `--explore` (divergent exploration) | `--debate` (two-sided debate) | `--plan` (actionable steps)

---

## 📋 OUTPUT FORMAT

```markdown
### 🎯 Recommendation: [Option] (Confidence: X/10)
- **Rationale**: [Evidence from codebase, benchmarks, best practices]
- **Trade-offs**: [Explicit gains vs acceptable compromises]
- **Risk & Mitigation**:
  * ⚠️ *Risk 1*: [Description] ➔ 🛡️ *Mitigation*: [Concrete action]
  * ⚠️ *Risk 2*: [Description] ➔ 🛡️ *Mitigation*: [Concrete action]
```

---

## 🎯 [GATE 9: POST-FLIGHT THINKING CHECKLIST — VERIFY BEFORE REPORTING]

Before sending response to user, MUST self-audit these 5 golden criteria:
1.  ✅ **Did I cite empirical evidence from codebase or documentation?** *(No unverified claims)*
2.  ✅ **Is confidence scored (1-10) with justification?**
3.  ✅ **Are trade-offs presented objectively on both sides?** *(No one-sided bias)*
4.  ✅ **Is there a concrete Risk & Mitigation breakdown?**
5.  ✅ **Did I STOP at Step 5 for user confirmation?**

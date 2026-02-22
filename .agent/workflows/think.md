---
description: "💡 Think Pro : 6 methods, 5 tiers, multi-mode reasoning"
skills: { required: [], contextual: [] }
success_criteria: "Analysis complete, evidence cited, recommendation actionable"
---

# 💡 /think — Think Pro

> 6 Thinking Methods • 5 Tiers • Multi-Mode Reasoning
> 📚 Evidence-Based Decisions • Structured Analysis • Cognitive Frameworks

---

## THINK FLOW

1. **CONTEXT** — Detect project, review constraints via HSA (`hsa_get_context`). Show: `[Step 1/5] Gathering context...`
2. **BRAINSTORM** — Apply selected method, generate options
3. **EVALUATE** — Score and compare ideas with evidence. Show: `[Step 3/5] Evaluating 4 options...`
4. **DECIDE** — Recommend with rationale and confidence score
5. **VALIDATE** — Present recommendation to user → ⛔ STOP: confirm direction

---

## COMMANDS

### Core

| Command                      | Method              | Token Budget |
| ---------------------------- | ------------------- | ------------ |
| `/think [topic]`             | Auto-select         | 2000-4000    |
| `/think brainstorm [topic]`  | Mind Mapping        | 1000-2000    |
| `/think analyze [decision]`  | Six Thinking Hats   | 4000-6000    |
| `/think deep [architecture]` | Tree of Thought     | 10000-20000  |
| `/think solve [problem]`     | Reverse + SCAMPER   | 3000-5000    |
| `/think plan [feature]`      | Starbursting (5W1H) | 3000-5000    |
| `/think tradeoff [options]`  | Weighted matrix     | 2000-4000    |

### Mode

| Command            | Mode    | Constraints                  |
| ------------------ | ------- | ---------------------------- |
| `/think --explore` | Explore | No criticism, quantity focus |
| `/think --debate`  | Debate  | Argue both sides             |
| `/think --plan`    | Plan    | Actionable steps only        |

---

## 📊 5-TIER SYSTEM

| Tier | Name                   | Tokens | Method                           | Output                                     |
| ---- | ---------------------- | ------ | -------------------------------- | ------------------------------------------ |
| 1    | Quick Brainstorm       | 1-2K   | Mind Mapping                     | Branch tree → ⭐ Top Pick                  |
| 2    | Structured Analysis    | 4-6K   | Six Thinking Hats (⚪🔴⚫🟡🟢🔵) | Per-hat analysis → ⭐ Recommendation       |
| 3    | Deep Exploration       | 10-20K | Tree of Thought (3 paths)        | Path comparison → ⭐ Recommended Path      |
| 4    | Problem Solving        | 3-5K   | Reverse + SCAMPER                | Anti-problem insights → ⭐ Recommended Fix |
| 5    | Comprehensive Planning | 3-5K   | Starbursting (5W1H)              | Questions matrix → handoff to `/plan`      |

---

## 🧠 REASONING ARCHITECTURES

| Architecture     | Use When             | Overhead  | Accuracy |
| ---------------- | -------------------- | --------- | -------- |
| Chain of Thought | Single-path problems | +20-30%   | +15-25%  |
| Tree of Thought  | Multi-path decisions | +100-200% | +30-50%  |
| ReAct Loop       | Investigation needed | +50-100%  | +20-40%  |

ReAct Pattern: `Thought → Action [Search/Read/Test] → Observation → Repeat until conclusion`

---

## 🎭 MODE SYSTEM

| Mode        | Allow                | Forbid                 | Output        |
| ----------- | -------------------- | ---------------------- | ------------- |
| **Explore** | Wild ideas, quantity | Criticism, feasibility | Bullet list   |
| **Debate**  | All perspectives     | Bias, one-sided        | Pro/con table |
| **Plan**    | Actionable steps     | Vague ideas            | Numbered plan |

---

## 🧮 DECISION FRAMEWORK

### Weighted Scoring (for `/think tradeoff`)

| Criteria          | Weight |
| ----------------- | ------ |
| Performance       | 30%    |
| Maintainability   | 25%    |
| Time to implement | 20%    |
| Scalability       | 15%    |
| Cost              | 10%    |

### Quick Decision Rule

- **Reversible** → Decide fast, iterate
- **Irreversible** → Research deeper (Tier 3)

### Output Format

```
## Recommendation: [Option B] (Confidence: 8/10)

### Scoring Matrix
| Criteria        | Option A | Option B | Option C |
| --------------- | -------- | -------- | -------- |
| Performance     | 7        | 9        | 6        |
| Maintainability | 8        | 7        | 9        |
| Weighted Score  | 7.3      | 8.1      | 7.0      |

### Rationale
[Evidence-based reasoning for recommendation]

### Risks & Mitigations
- Risk 1: [description] → Mitigation: [action]
```

---

## ⚠️ ANTI-PATTERNS

| Don't                    | Do Instead                 |
| ------------------------ | -------------------------- |
| Analysis paralysis       | Set time box, decide       |
| Premature optimization   | Solve the problem first    |
| Solution without problem | Define problem clearly     |
| Bikeshedding             | Focus on high-impact items |
---

## SESSION SAVE

After completing this workflow:
1. Update `memory/CONTEXT_SNAPSHOT.md` - what changed, current status
2. Append summary to `memory/session.md`

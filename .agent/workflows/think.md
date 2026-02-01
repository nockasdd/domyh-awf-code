---
name: think
trigger: ["/think", "brainstorm", "idea", "ý tưởng"]
persona: architect
description: "💡 Brainstorming Pro v4.0: 6 methods, 5 tiers, multi-mode reasoning"
---

# 💡 /think — Brainstorming Pro v4.0

> Advanced Ideation with Structured Methods & Reasoning Architectures
> 📚 6 Methods • 5 Tiers • Multi-Mode • Token-Optimized

---

## 🔄 THINK FLOW v4.0

```
User: /think [command] [topic]
    │
    ▼
┌─────────────────────────────────────────┐
│ TIER DETECTION                          │
│ ▸ Analyze complexity                    │
│ ▸ Select appropriate tier/method        │
│ ▸ Set token budget                      │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 1: UNDERSTAND                     │
│ ▸ Check codebase context first          │
│ ▸ Review project rules                  │
│ ▸ Identify constraints                  │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 2: BRAINSTORM                     │
│ ▸ Apply selected method                 │
│ ▸ Generate structured output            │
│ ▸ Use reasoning architecture            │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 3: EVALUATE                       │
│ ▸ Compare trade-offs                    │
│ ▸ Score options                         │
│ ▸ Apply decision framework              │
└─────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────┐
│ PHASE 4: RECOMMEND                      │
│ ▸ Present recommendation                │
│ ⛔ STOP → Confirm direction             │
└─────────────────────────────────────────┘
```

---

## 🎯 COMMAND REGISTRY

### Core Commands

| Command                  | Method            | Tokens  | Description              |
| ------------------------ | ----------------- | ------- | ------------------------ |
| `/think [topic]`         | Auto-select       | 3k-6k   | General brainstorming    |
| `/think quick [topic]`   | Big Mind Map      | 2k-3k   | Fast ideation, 3-5 ideas |
| `/think analyze [topic]` | Six Hats          | 4k-6k   | 6 perspectives analysis  |
| `/think deep [topic]`    | Tree of Thought   | 10k-20k | Multiple reasoning paths |
| `/think solve [problem]` | Reverse + SCAMPER | 3k-5k   | Root cause + solutions   |
| `/think plan [feature]`  | Starbursting      | 5k-8k   | 5W1H comprehensive       |

### Structured Methods

| Command                    | Method                | Output                           |
| -------------------------- | --------------------- | -------------------------------- |
| `/think mindmap [topic]`   | Big Mind Mapping      | 4-6 branches, 3-5 sub-ideas each |
| `/think reverse [problem]` | Reverse Brainstorming | 8-12 inversions → solutions      |
| `/think roles [feature]`   | Role Storming         | 6-8 persona perspectives         |
| `/think scamper [idea]`    | SCAMPER               | 7 dimensions analysis            |
| `/think hats [decision]`   | Six Thinking Hats     | 6 perspectives                   |
| `/think questions [plan]`  | Starbursting          | 15-25 Q&A (5W1H)                 |

### Mode Commands

| Command                   | Mode     | Constraints                     |
| ------------------------- | -------- | ------------------------------- |
| `/think explore [topic]`  | EXPLORE  | No criticism, no implementation |
| `/think innovate [topic]` | INNOVATE | Pros/cons only                  |
| `/think reason [topic]`   | REASON   | Deep reasoning (o1-style)       |
| `/think plan [topic]`     | PLAN     | Actionable steps only           |

---

## 📊 5-TIER SYSTEM

### Tier 1: Quick Ideation

```yaml
tier_1_quick:
  trigger: "/think quick" or simple topics
  method: "big_mind_mapping"
  tokens: 2000-3000
  reasoning: "chain_of_thought"

  output_format: |
    💡 QUICK IDEAS: {Topic}

    ├── 🌿 Branch 1: {Main idea}
    │   ├── {Sub-idea 1}
    │   └── {Sub-idea 2}
    ├── 🌿 Branch 2: {Main idea}
    │   ├── {Sub-idea 1}
    │   └── {Sub-idea 2}
    └── 🌿 Branch 3: {Main idea}
        └── {Sub-idea 1}

    ⭐ Top Pick: {Best idea with 1-line rationale}
```

### Tier 2: Structured Analysis

```yaml
tier_2_analyze:
  trigger: "/think analyze" or decisions
  method: "six_thinking_hats"
  tokens: 4000-6000
  reasoning: "chain_of_thought"

  output_format: |
    🎩 SIX HATS ANALYSIS: {Topic}

    ⚪ WHITE HAT (Facts):
    - Data point 1
    - Data point 2

    🔴 RED HAT (Emotions):
    - Team feeling about complexity
    - User sentiment prediction

    ⚫ BLACK HAT (Risks):
    - Potential failure 1
    - Potential failure 2

    🟡 YELLOW HAT (Benefits):
    - Advantage 1
    - Advantage 2

    🟢 GREEN HAT (Creativity):
    - Alternative approach 1
    - Alternative approach 2

    🔵 BLUE HAT (Process):
    - Decision criteria
    - Next steps

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ⭐ RECOMMENDATION: {Clear decision}
```

### Tier 3: Deep Exploration

```yaml
tier_3_deep:
  trigger: "/think deep" or complex architecture
  method: "tree_of_thought"
  tokens: 10000-20000
  reasoning: "o1_high_effort"

  output_format: |
    🌳 DEEP EXPLORATION: {Topic}

    ═══════════════════════════════
    PATH A: {Approach name}
    ───────────────────────────────
    Strategy: {Description}
    Pros: {List}
    Cons: {List}
    Confidence: 🟢 High / 🟡 Medium / 🔴 Low

    ═══════════════════════════════
    PATH B: {Approach name}
    ───────────────────────────────
    Strategy: {Description}
    Pros: {List}
    Cons: {List}
    Confidence: 🟢 High / 🟡 Medium / 🔴 Low

    ═══════════════════════════════
    PATH C: {Approach name}
    ───────────────────────────────
    Strategy: {Description}
    Pros: {List}
    Cons: {List}
    Confidence: 🟢 High / 🟡 Medium / 🔴 Low

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📊 REASONING SUMMARY:
    {Step-by-step reasoning explanation}

    ⭐ RECOMMENDED PATH: {A/B/C} because {rationale}
```

### Tier 4: Problem Solving

```yaml
tier_4_solve:
  trigger: "/think solve" or bug/error
  method: "reverse_brainstorming + scamper"
  tokens: 3000-5000
  reasoning: "react_loop"

  output_format: |
    🔧 PROBLEM SOLVING: {Problem}

    ═══════════════════════════════
    PHASE 1: REVERSE BRAINSTORMING
    ───────────────────────────────
    "How could we CAUSE this problem?"

    1. {Cause 1} → Inverse: {Solution 1}
    2. {Cause 2} → Inverse: {Solution 2}
    3. {Cause 3} → Inverse: {Solution 3}

    ═══════════════════════════════
    PHASE 2: SCAMPER (Top 3 Solutions)
    ───────────────────────────────
    | Dimension | Solution 1 | Solution 2 |
    |-----------|------------|------------|
    | Substitute | ... | ... |
    | Combine | ... | ... |
    | Adapt | ... | ... |
    | Modify | ... | ... |
    | Put to use | ... | ... |
    | Eliminate | ... | ... |
    | Reverse | ... | ... |

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    ⭐ RECOMMENDED FIX:
    {Solution with implementation steps}
```

### Tier 5: Comprehensive Planning

```yaml
tier_5_plan:
  trigger: "/think plan" or feature planning
  method: "starbursting"
  tokens: 5000-8000
  reasoning: "o1_high_effort"

  output_format: |
    📋 COMPREHENSIVE PLAN: {Feature}

    ═══════════════════════════════
    WHO (People)
    ───────────────────────────────
    Q: Who will use this?
    A: {Answer}

    Q: Who maintains it?
    A: {Answer}

    ═══════════════════════════════
    WHAT (Components)
    ───────────────────────────────
    Q: What are the core components?
    A: {Answer}

    Q: What data is needed?
    A: {Answer}

    ═══════════════════════════════
    WHERE (Integration)
    ───────────────────────────────
    Q: Where does it deploy?
    A: {Answer}

    Q: Where are the integration points?
    A: {Answer}

    ═══════════════════════════════
    WHEN (Timeline)
    ───────────────────────────────
    Q: When is the deadline?
    A: {Answer}

    Q: When are the milestones?
    A: {Answer}

    ═══════════════════════════════
    WHY (Business Value)
    ───────────────────────────────
    Q: Why is this needed?
    A: {Answer}

    Q: Why now?
    A: {Answer}

    ═══════════════════════════════
    HOW (Implementation)
    ───────────────────────────────
    Q: How will it be built?
    A: {Answer}

    Q: How will it be tested?
    A: {Answer}

    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    📊 IMPLEMENTATION ROADMAP
    {Numbered action plan}
```

---

## 🧠 REASONING ARCHITECTURES

### Chain of Thought (CoT)

```yaml
chain_of_thought:
  use_when: "Single-path problems, quick decisions"
  token_overhead: "+20-30%"
  accuracy_gain: "+15-25%"

  prompt_pattern: |
    Let me analyze this step by step:
    1. First, I observe...
    2. This leads to...
    3. Therefore...
```

### Tree of Thought (ToT)

```yaml
tree_of_thought:
  use_when: "Complex decisions, multiple solutions"
  token_overhead: "+150-300%"
  quality_gain: "+40-60%"

  prompt_pattern: |
    Exploring multiple paths:

    Path A: [Description] → Evaluate → Score: X/10
    Path B: [Description] → Evaluate → Score: X/10
    Path C: [Description] → Evaluate → Score: X/10

    Best path: [Selection with rationale]
```

### ReAct Loop

```yaml
react_loop:
  use_when: "Dynamic problems, tool-using scenarios"
  token_overhead: "+40-60%"
  completion_gain: "+35-45%"

  prompt_pattern: |
    Thought: I need to understand...
    Action: Check codebase for...
    Observation: Found that...

    Thought: Based on this, I should...
    Action: Search for solutions...
    Observation: The result shows...

    Conclusion: Therefore...
```

---

## 🎭 MODE SYSTEM (RIPER-5 Inspired)

### EXPLORE Mode

```yaml
explore_mode:
  constraints:
    - No criticism allowed
    - No implementation details
    - No feasibility judgment

  output: "Bullet points of raw ideas"

  prompt: |
    Generate ideas without judgment.
    Focus on quantity over quality.
    Wild ideas are welcome.
```

### INNOVATE Mode

```yaml
innovate_mode:
  constraints:
    - Pros/cons only
    - No final decisions
    - No code

  output: "Comparison tables"

  prompt: |
    For each idea, analyze:
    - Advantages (3-5 points)
    - Disadvantages (3-5 points)
    - Unique value proposition
```

### REASON Mode

```yaml
reason_mode:
  reasoning_model: "o1-style high effort"
  token_budget: 8000-15000

  output: "Detailed reasoning summary"

  ⚠️ WARNING:
    - Do NOT use "think step by step" (drops accuracy 60-80%)
    - Provide high-level goals, not explicit steps
    - Let model reason internally
```

### PLAN Mode

```yaml
plan_mode:
  constraints:
    - Actionable steps only
    - Clear ownership
    - Definite timeline

  output: "Numbered action plan with dates"
```

---

## 💾 TOKEN OPTIMIZATION

### Caching Strategy

```yaml
caching:
  method_templates:
    ttl: 604800 # 7 days
    content: "SCAMPER, Six Hats, Starbursting prompts"
    hit_rate: "60-80%"
    cost_reduction: "70-85%"

  project_context:
    ttl: 86400 # 24 hours
    content: "Architecture docs, conventions"
    hit_rate: "40-60%"

  session_results:
    ttl: 3600 # 1 hour
    semantic_similarity: 0.85
    hit_rate: "20-35%"
```

### Progressive Loading

```yaml
progressive:
  phase_1:
    tokens: 500-1000
    action: "Check internal knowledge + codebase"
    stop_if: "Answer is clear"

  phase_2:
    tokens: 2000-4000
    action: "Apply one brainstorming method"
    stop_if: "Sufficient coverage"

  phase_3:
    tokens: 8000-20000
    action: "Enable deep reasoning OR multi-agent"
    use_for: "Complex decisions only"
```

---

## 🔧 EVALUATION FRAMEWORKS

```yaml
frameworks:
  effort_risk_reward:
    effort: [Low, Medium, High]
    risk: [Low, Medium, High]
    reward: [Low, Medium, High]

  weighted_matrix:
    criteria:
      - name: "Technical fit"
        weight: 30%
      - name: "Time to implement"
        weight: 25%
      - name: "Team expertise"
        weight: 20%
      - name: "Maintainability"
        weight: 15%
      - name: "Cost"
        weight: 10%

  quick_decision:
    reversible: "Decide fast, iterate"
    irreversible: "Research deeper"
```

---

## ⚠️ CRITICAL ANTI-PATTERNS

```yaml
anti_patterns:
  - pattern: '"Think step by step" với o1'
    problem: "Drops accuracy 60-80%"
    solution: "Use high-level goals, trust internal reasoning"

  - pattern: "Mixed modes"
    problem: "Confuses exploration vs planning"
    solution: "Use explicit mode transitions"

  - pattern: "Over-specification"
    problem: "Constrains reasoning models"
    solution: "Provide goal + constraints only"

  - pattern: "Ignoring context"
    problem: "Wastes tokens on web search"
    solution: "Check codebase + project rules first"

  - pattern: "No reasoning summary"
    problem: "Can't understand decisions"
    solution: "Always enable summary output"
```

---

## 🔗 SKILL INTEGRATION

### Handoff to Multi-Agent

```yaml
multi_agent_handoff:
  trigger:
    - "High-risk decisions"
    - "Architecture changes"
    - "Security-critical features"

  action: "Invoke multi-agent-brainstorming skill"

  agents:
    - "Primary Designer"
    - "Skeptic/Challenger"
    - "Constraint Guardian"
    - "User Advocate"
    - "Integrator/Arbiter"
```

### Integration with /code

```yaml
code_handoff:
  trigger: "User confirms recommendation"
  action: "Transition to /code workflow"
  preserve:
    - "Decision rationale"
    - "Selected approach"
    - "Implementation constraints"
```

---

## 📋 SUB-COMMANDS REFERENCE

| Command                    | Description             | Tokens  |
| -------------------------- | ----------------------- | ------- |
| `/think [topic]`           | Auto-select best method | 3k-6k   |
| `/think quick [topic]`     | Fast ideation           | 2k-3k   |
| `/think analyze [topic]`   | Six Hats analysis       | 4k-6k   |
| `/think deep [topic]`      | Tree of Thought         | 10k-20k |
| `/think solve [problem]`   | Problem solving         | 3k-5k   |
| `/think plan [feature]`    | 5W1H planning           | 5k-8k   |
| `/think mindmap [topic]`   | Big Mind Mapping        | 3k-5k   |
| `/think reverse [problem]` | Reverse Brainstorming   | 2k-3k   |
| `/think roles [feature]`   | Role Storming           | 3k-4k   |
| `/think scamper [idea]`    | SCAMPER technique       | 2k-3k   |
| `/think hats [decision]`   | Six Thinking Hats       | 4k-6k   |
| `/think questions [plan]`  | Starbursting            | 3k-5k   |
| `/think explore [topic]`   | EXPLORE mode            | 2k-3k   |
| `/think innovate [topic]`  | INNOVATE mode           | 3k-5k   |
| `/think reason [topic]`    | REASON mode (o1)        | 8k-15k  |
| `/think compare`           | Compare options         | 2k-4k   |
| `/think decide`            | Make final decision     | 1k-2k   |

---

## ⚙️ RULES APPLIED

| Phase      | Rules                                   |
| ---------- | --------------------------------------- |
| Understand | `context-management`, `online-research` |
| Brainstorm | `quality`, `yagni-enforcement`          |
| Evaluate   | `evidence`, multi-source verification   |
| Recommend  | `stop-conditions`, `safety`             |

---

_DOMYH Agent v4.3 • Think Pro v4.0 • 6 Methods + 5 Tiers + Multi-Mode_

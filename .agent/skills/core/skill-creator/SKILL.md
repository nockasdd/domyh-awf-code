---
name: skill-creator
description: "Create, improve, and validate DOMYH skills. Use when creating new skills, improving existing ones, or optimizing skill descriptions for better trigger accuracy."
detect: ["SKILL.md", "META.yaml", "ADVANCED.md"]
category: core
tier: 1
---

# Skill Creator — DOMYH Awesome Code

> **Type**: Meta-skill (creates other skills)
> **Philosophy**: Model-agnostic, HSA-native, multi-IDE portable

---

## 🎯 When to Use This Skill

- User wants to **create a new skill**
- User wants to **improve an existing skill**
- User wants to **validate skill quality**
- User wants to **optimize skill description** for better triggering
- User mentions "skill", "create skill", "new pattern", "add to skills"

**NOT for**: Writing code directly (→ language-specific skills), configuring IDEs (→ awf install)

---

## 📦 DOMYH Skill Architecture

### Decision Tree

```
Task → Creating a new skill?
  ├─ Simple skill (patterns only)
  │   └─ SKILL.md (< 300 lines, frontmatter + body)
  ├─ Standard skill
  │   └─ SKILL.md + data/*.yaml
  ├─ Complex skill (deep-dive content)
  │   └─ SKILL.md + ADVANCED.md + data/ + references/
  └─ Expanding existing skill?
      └─ Check line count → Split if > 500 lines
```

### Folder Structure

```
.agent/skills/{category}/{name}/
├── SKILL.md         ← Required: frontmatter + instructions (≤500 lines)
├── ADVANCED.md      ← Optional: deep-dive content (tier 2)
├── data/            ← Optional: YAML pattern files
│   └── patterns.yaml
└── references/      ← Optional: detailed docs
    ├── {topic}-patterns.md
    └── migration-guide.md
```

### 7 Categories

| Category | Purpose | Example Skills |
|:---------|:--------|:---------------|
| `core/` | Cross-language fundamentals | security, api-design, error-handling |
| `languages/` | Language-specific patterns | go, python, typescript, rust |
| `frameworks/` | Framework guides | react, vue, nextjs, flutter |
| `devops/` | Infrastructure & deployment | docker, kubernetes, terraform |
| `cross-cutting/` | Multi-domain concerns | testing, database, microservices |
| `tooling/` | Developer tools | cli-dev, mcp, browser-agent |
| `ai-ml/` | AI/ML patterns | ai-agents, rag, prompt-engineering |

### 3-Tier Progressive Loading

```
Tier 1: YAML frontmatter  (~100 tokens)  — Always loaded for routing/search
Tier 2: SKILL.md body     (~1,500 tokens) — On-demand when skill triggered
Tier 3: ADVANCED.md       (~4,000 tokens) — Deep-dive only when needed
```

| Condition | Action |
|:----------|:-------|
| SKILL.md < 300 lines | Keep as-is |
| SKILL.md 300-500 lines | Consider splitting heavy sections to references/ |
| SKILL.md > 500 lines | **Must split** into core + references/ |

**Keep in SKILL.md**: Decision tree, Quick start, Essential patterns, Checklist
**Move to references/**: Detailed examples, Platform-specific, Migration guides, API tables
**Keep in ADVANCED.md**: Deep architecture, Performance tuning, Edge cases

---

## 📝 Creating a Skill

### Step 1: Discovery

Before writing anything, check what already exists:

```
hsa_search(action:"skills", query:"<topic>")
→ If skill exists: improve it, don't duplicate
→ If similar skill exists: consider extending it
```

Interview the user:
1. **What** should this skill enable? (specific outcomes)
2. **When** should it trigger? (file patterns, keywords, contexts)
3. **Who** is the target? (backend dev, frontend, devops, etc.)
4. **What category** fits best? (from 7 categories above)

### Step 2: Write the Frontmatter

The frontmatter is the **primary trigger mechanism**. It determines when HSA loads the skill.

```yaml
---
name: example-skill              # kebab-case, unique (max 30 chars)
description: "Clear description   # 50-200 chars, include trigger keywords
  of what this skill does and     # Be specific about contexts
  when to use it."                # Mention file types/frameworks
detect: ["*.ext", "config.json"]  # File patterns that auto-trigger
category: cross-cutting           # One of 7 categories
tier: 1                           # 1=standard, 2=deep-dive only
---
```

#### Frontmatter Field Reference

| Field | Required | Type | Constraints | Description |
|:------|:---------|:-----|:------------|:------------|
| `name` | ✅ | string | ≤30 chars, kebab-case | Unique skill identifier |
| `description` | ✅ | string | 50-200 chars | What + When — primary trigger mechanism |
| `detect` | ✅ | string[] | ≥1 pattern | File patterns for auto-detection |
| `category` | ✅ | enum | 7 categories | Routing and organization |
| `tier` | ✅ | int | 1 or 2 | Loading priority |

#### Description Writing Rules

The description determines whether the skill gets found by `hsa_search`. Write it to be "discoverable":

- **Include action verbs**: "Use when working with...", "Activate for..."
- **Include file types**: "docker-compose.yml", ".go files", "React components"
- **Include synonyms**: "container orchestration" AND "Docker" AND "docker-compose"
- **Be specific but not narrow**: Cover the breadth of when this skill is useful
- **Avoid generic phrases**: "best practices" alone says nothing — specify the domain

**Good**: `"Docker Compose patterns for multi-container apps. Use when working with docker-compose.yml, Dockerfile, or container orchestration including networking, volumes, and health checks."`

**Bad**: `"Helps with Docker stuff"`

### Step 3: Write the Body

Follow this standard structure. Not all sections are required — include what's relevant:

```markdown
# {Name} Patterns — DOMYH Awesome Code

> **Version**: ...
> **Philosophy**: one-line guiding principle

---

## 🎯 When to Use This Skill
## 📦 Recommended Stack (tables of tools)
## 🆕 Latest Features (code examples, 2025-2026)
## 📝 Core Patterns (3-5 real-world examples)
## 🛡️ Error Handling
## 🧪 Testing Patterns
## 📁 Project Structure
## ✅ Best Practices Checklist
```

### Step 4: Add Data Files (Optional)

For skills with pattern collections, use structured YAML:

```yaml
# data/patterns.yaml
patterns:
  - name: pattern-name
    description: "What this pattern does"
    when: "When to use it"
    example: |
      Code example here
```

### Writing Principles

1. **Explain the WHY** — Don't just say "always use X". Explain why X is better than alternatives. Models understand reasoning better than rigid rules.

2. **Show, don't tell** — Code examples are worth more than prose. Include real-world patterns, not abstract descriptions.

3. **Keep it lean** — Remove instructions that don't improve outcomes. Every line should earn its place. If a section isn't pulling weight, cut it.

4. **Generalize from examples** — Write patterns that work across many projects. Avoid overfitting to one use case.

5. **Use current versions** — Include 2025-2026 features. Outdated patterns create technical debt.

---

## ✅ Validation Checklist

### Schema

- [ ] `name` is kebab-case, unique across all skills, ≤30 chars
- [ ] `description` is 50-200 chars with trigger keywords
- [ ] `detect` has ≥1 file pattern
- [ ] `category` is one of the 7 valid categories
- [ ] `tier` is 1 or 2
- [ ] Body is ≤500 lines

### Content Quality

- [ ] Has "When to Use" section with clear scope
- [ ] Has decision tree (if multiple paths exist)
- [ ] Has ≥3 code examples with comments
- [ ] Has error handling patterns
- [ ] Has testing patterns
- [ ] Has best practices checklist
- [ ] Explains WHY, not just WHAT
- [ ] No duplicate keywords with existing skills

### Search Ranking

```
hsa_check_changes()                           → Re-index
hsa_search(action:"skills", query:"<topic>")  → Verify top 3
```

Test with 3-5 different query phrasings:
- Formal: "Docker container orchestration patterns"
- Casual: "help with docker compose"
- Implicit: "multi-container app setup"

---

## 🔧 Improving Existing Skills

1. Read the current SKILL.md
2. Identify gaps (missing patterns, outdated versions, unclear instructions)
3. Apply the writing principles above
4. Re-index and verify ranking didn't regress
5. If adding >200 lines of new content, split into ADVANCED.md or references/

---

## ❌ Common Mistakes

| Mistake | Impact |
|:--------|:-------|
| No decision tree | Agent doesn't know when to use which pattern |
| SKILL.md > 500 lines | Context bloat, slow loading |
| Missing `detect` patterns | No auto-detection |
| Generic description | Poor search ranking |
| No code examples | Agent can't produce correct patterns |
| Overlapping keywords with existing skills | Confused skill selection |
| Placeholder content | Wasted token budget |

---

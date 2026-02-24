---
name: skill-creator
version: "6.4.5"
category: cross-cutting
---

# Skill Creator — DOMYH Awesome Code

Guide for creating new domyh-awf skills with proper schema, progressive disclosure, and quality standards.

## Decision Tree

```
Task → Creating a new skill?
  ├─ Simple skill (patterns only)
  │   └─ META.yaml + SKILL.md (< 300 lines)
  ├─ Standard skill
  │   └─ META.yaml + SKILL.md + data/*.yaml
  ├─ Complex skill (deep-dive content)
  │   └─ META.yaml + SKILL.md + ADVANCED.md + data/ + references/
  └─ Expanding existing skill?
      └─ Check line count → Split if > 500 lines
```

## Quick Start — 6-Step Workflow

### Step 1: Choose Category & Directory

```yaml
categories:
  core: # Foundation skills (security, coding-rules)
  languages: # Programming languages (typescript, python, go)
  frameworks: # Frameworks (react, nextjs, vue)
  cross-cutting: # Multi-domain skills (testing, database, docker)
  devops: # Infrastructure (aws, kubernetes, ci-cd)
  tooling: # Dev tools (git, vscode)
  ai-ml: # AI/ML patterns (rag-patterns, prompt-engineering)
```

### Step 2: Create META.yaml

```yaml
# Template — META.yaml v2
name: my-skill # lowercase, hyphen-separated
version: "6.4.5"
display: My Skill # Human-readable name
category: cross-cutting # One of the 7 categories
tier: 2 # 1=core, 2=standard, 3=specialized
priority: 3 # 0-6 (lower = higher priority)

desc: "Short description — max 80 chars"

trigger_desc: | # NEW v2: Rich description for semantic matching
  When to activate this skill. Keywords, file patterns, common
  user questions that should trigger this skill. Max 1024 chars.

triggers:
  file_patterns:
    - "*.ext"
    - "config.file"
  keywords:
    - keyword1
    - keyword2
    - keyword3
  intents:
    - "action description 1"
    - "action description 2"

caps:
  - Capability 1
  - Capability 2
  - Capability 3

compatibility: "Runtime >= version" # NEW v2: Environment requirements

related_skills:
  - related-skill-1
  - related-skill-2

data_files:
  - data/patterns.yaml
```

### Step 3: Write SKILL.md (< 500 lines)

```markdown
# Skill Name

Short description of what this skill covers.

## Decision Tree ← REQUIRED: When to use which pattern

## Quick Start ← REQUIRED: Most common workflow

## Patterns ← Key patterns with code examples

## Best Practices ← Checklist format preferred

## Data Files ← Reference to data/ files

## Deep-Dive References ← Links to references/ (if split)
```

### Step 4: Create data/ files (YAML patterns)

```yaml
# data/patterns.yaml
patterns:
  - name: pattern-name
    description: "What this pattern does"
    when: "When to use it"
    example: |
      Code example here
```

### Step 5: Add references/ (if > 500 lines)

Split detailed content into `references/*.md` files:

```
my-skill/
├── META.yaml
├── SKILL.md (< 300 lines, core content)
├── ADVANCED.md (optional, deep-dive)
├── data/
│   └── patterns.yaml
└── references/
    ├── advanced-patterns.md
    └── migration-guide.md
```

### Step 6: Validate

```yaml
checklist:
  - [ ] META.yaml has all required fields (name, version, category, desc)
  - [ ] trigger_desc is under 1024 chars
  - [ ] SKILL.md is under 500 lines
  - [ ] Decision tree present in SKILL.md
  - [ ] Quick start section with working examples
  - [ ] data/ files use consistent YAML schema
  - [ ] references/ files linked from SKILL.md
  - [ ] No duplicate keywords with existing skills
```

## SKILL.md Best Practices

| Practice                   | Rule                                         |
| -------------------------- | -------------------------------------------- |
| **Line limit**             | < 500 lines (split to references/ if larger) |
| **Decision tree**          | Always include — guides agent routing        |
| **Code examples**          | Working, copy-pasteable code                 |
| **Checklist**              | Use `- [ ]` for actionable items             |
| **Cross-refs**             | Link to related skills and data files        |
| **Progressive disclosure** | Core in SKILL.md, details in references/     |

## Common Mistakes

❌ No decision tree → Agent doesn't know when to use patterns
❌ SKILL.md > 500 lines → Context bloat, slow loading
❌ Missing `desc` field → Broken HSA routing
❌ Missing `triggers.file_patterns` → No auto-detection
❌ Overlapping keywords → Confused skill selection
❌ Placeholder content → Wasted token budget

## References

- [META.yaml v2 Schema](references/schema-v2.md)
- [Progressive Disclosure Patterns](references/patterns.md)

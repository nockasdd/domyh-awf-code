---
name: "context-first-gatekeeping"
description: "Enforces 'understand before modify' principle. Context gate before any implementation. DRY check, stack-aware skill loading, and file reading protocol."
triggers:
  - "Before starting any implementation"
  - "Before creating new files or functions"
  - "Before modifying unfamiliar code"
  - "At task start — load context first"
---

# Context-First Gatekeeping

**Core principle:** Understand before modify. Read before write. Search before create.

## The Context Gate

Before ANY implementation, pass through this gate:

```
Ready to write code?
    │
    ├── 1. ANCHORS — Check prior decisions
    │   hsa_check_drift(include_anchors: true)
    │   Found relevant decisions? → Follow them
    │   ↓
    │
    ├── 2. FILES — Read the code you'll modify
    │   hsa_get_context(query: "relevant topic")
    │   Understand existing patterns? → Match them
    │   ↓
    │
    ├── 3. DRY — Does similar code already exist?
    │   hsa_get_context(query: "function/pattern name")
    │   Found existing? → Reuse, don't recreate
    │   ↓
    │
    ├── 4. SKILLS — Load relevant skill patterns
    │   hsa_search_skills(query: "relevant skill")
    │   Patterns loaded? → Follow them
    │   ↓
    │
    └── 5. INTENT — Is intent declared?
        hsa_declare_intent declared? → Proceed
        NOT declared? → Declare NOW, then proceed
```

## Step 1: Check Anchors (Prior Decisions)

```
hsa_check_drift(
  current_action: "About to implement {feature}",
  include_anchors: true
)
```

**Look for:**
- `[DECISION]` anchors about technology choices
- `[CONVENTION]` anchors about coding patterns
- `[CONSTRAINT]` anchors about limitations

**If found:** Follow them. Don't re-debate.

## Step 2: Read Before Write

### File Reading Protocol

```
# 1. Get overview of relevant code
hsa_get_context(
  query: "feature area you're working on",
  output_mode: "skeleton"    # Signatures only, ~1000 tokens
)

# 2. Read specific files you'll modify
hsa_get_context(
  query: "specific function or file",
  output_mode: "full",
  max_tokens: 4000
)

# 3. Understand the patterns used
# - Naming conventions
# - Error handling approach
# - Import style
# - Test structure
```

### What to Look For

| Aspect | Question | Action |
|--------|----------|--------|
| **Naming** | How are files/functions/variables named? | Match the convention |
| **Error handling** | try-catch? Result type? Error codes? | Follow existing pattern |
| **Imports** | Relative? Absolute? Barrels? | Match import style |
| **Tests** | Co-located? Separate folder? | Put tests where they expect |
| **Types** | Interfaces? Type aliases? Generics? | Match type style |

## Step 3: DRY Check (Search Before Create)

Before creating ANY new function, component, or utility:

```
# Search for existing implementations
hsa_get_context(
  query: "{what you're about to create}",
  output_mode: "references"    # File list only
)
```

### Decision Matrix

| Search Result | Action |
|--------------|--------|
| Exact match exists | **Reuse it.** Import and use. |
| Similar exists | **Extend it.** Add parameter or overload. |
| Nothing similar | **Create new.** But check one more time. |
| Partial match | **Refactor.** Extract shared logic, then specialize. |

### Common DRY Violations

| Violation | Better Approach |
|-----------|----------------|
| New `formatDate()` when one exists in utils | Import existing one |
| New API response wrapper when `response.ts` exists | Use existing wrapper |
| New validation logic when `validate.ts` exists | Extend existing validators |
| Duplicate error handling in every file | Extract to middleware/decorator |

## Step 4: Stack-Aware Skill Loading

```
# Auto-detect stack
hsa_detect_stack()

# Search for relevant skills
hsa_search_skills(query: "TypeScript error handling")
# or
hsa_search_skills(query: "React component patterns")
```

### Auto-Load Skills by Stack

| Detected Stack | Skills to Load |
|---------------|----------------|
| TypeScript + Node | `error-handling`, `api-design`, `testing` |
| React / Next.js | `react`, `nextjs`, `testing`, `web-perf` |
| Python | `error-handling`, `testing`, `api-design` |
| Go | `error-handling`, `testing` |
| Vue / Nuxt | `vue`, `nuxt`, `testing` |

## Step 5: Verify Intent

```
# Check if intent is declared
# If not:
hsa_declare_intent(
  focus: "Implementing {feature}",
  mode: "plan_driven",
  goals: ["Goal 1", "Goal 2"]
)
```

## Quick Context Gate (For Small Changes)

For changes < 10 lines, a lighter gate:

```
1. ✅ Read the file you're modifying (at minimum)
2. ✅ Check if similar code exists nearby
3. ✅ Match existing style
```

Skip: full anchor check, skill loading, intent declaration.

## Red Flags

| Thought | Reality |
|---------|---------|
| "I know what to write" | You know what to write IN ISOLATION. Context may change your approach. |
| "This is a simple change" | Simple changes in unfamiliar code cause subtle bugs. Read first. |
| "I'll create a new utility" | Search first. It probably exists already. |
| "I don't need to read the whole file" | Read at least the function signatures. Patterns matter. |
| "I'll match the style later" | Match it NOW. Inconsistency compounds. |

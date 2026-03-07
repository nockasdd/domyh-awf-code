---
description: 🔨 Create or improve DOMYH skills with guided workflow — scaffold, validate, iterate
---

# Skill Creator Workflow

> Meta-workflow for creating new skills or improving existing ones.
> Inspired by Anthropic's skill-creator, adapted for DOMYH's multi-IDE, model-agnostic ecosystem.

## Prerequisites

- HSA MCP server running (`nock awf hsa start`)
- Read skill-creator skill: `.agent/skills/core/skill-creator/SKILL.md`

---

## Step 1: Discovery

Determine what skill to create and verify it doesn't already exist.

```
1. hsa_search(action:"skills", query:"<topic>")
   → Check if skill exists or overlaps with existing

2. Interview user:
   - What should this skill do?
   - What file patterns trigger it? (e.g., *.go, docker-compose.yml)
   - What's the target audience? (backend dev, frontend, devops)
   - What category? (languages|frameworks|core|devops|cross-cutting|tooling|ai-ml)

3. hsa_search(action:"docs", doc_libraries:["<relevant-lib>"])
   → Gather reference material
```

## Step 2: Scaffold

Create the SKILL.md with DOMYH standard format.

```
1. Create folder: .agent/skills/{category}/{name}/

2. Create SKILL.md with frontmatter:
   ---
   name: skill-name           # kebab-case, unique
   description: "..."         # 50-200 chars, include trigger keywords
   detect: ["*.ext", "file"]  # File patterns that auto-trigger
   category: <category>       # One of 7 categories
   tier: 1                    # 1=standard, 2=deep-dive
   ---

3. Body structure:
   # {Name} Patterns — DOMYH Awesome Code
   > Version, Philosophy
   ## 🎯 When to Use This Skill
   ## 📦 Recommended Stack
   ## 🆕 Latest Features (code examples)
   ## 📝 Core Patterns
   ## 🛡️ Error Handling
   ## 🧪 Testing Patterns
   ## 📁 Project Structure
   ## ✅ Best Practices Checklist
```

## Step 3: Validate

Verify skill quality and searchability.

```
1. Schema check:
   - name: kebab-case? unique?
   - description: 50-200 chars? has trigger keywords?
   - detect: ≥1 pattern?
   - category: valid enum?
   - body: ≤500 lines?

2. BM25 trigger test:
   - hsa_check_changes() → re-index
   - hsa_search(action:"skills", query:"<test queries>")
   - Verify skill appears in top 3 results

3. Content quality:
   - ≥3 code examples?
   - Error handling section present?
   - Testing patterns included?
   - Best practices checklist?
```

## Step 4: Iterate

Improve based on testing and feedback.

```
Loop until user satisfied:
  1. User tests skill in their IDE
  2. Collect feedback on what's missing/wrong
  3. Improve SKILL.md content
  4. hsa_check_changes() → re-index
  5. Re-run BM25 trigger test
```

## Step 5: Register

Finalize and deploy.

```
1. Verify file is in correct path:
   .agent/skills/{category}/{name}/SKILL.md

2. Optional: Create ADVANCED.md for deep-dive content (tier 2)

3. hsa_check_changes() → final re-index

4. Verify with: hsa_search(action:"skills", query:"<topic>")
   → Should appear in top results

5. Done! Skill is live across all IDEs via HSA.
```

---

## Tips

- **Keep SKILL.md ≤500 lines** — use ADVANCED.md for extras
- **Explain the WHY** — not just WHAT to do, but WHY it matters
- **Include code examples** — real-world patterns > abstract rules
- **Use detect field wisely** — specific file patterns avoid false triggers
- **Test with edge cases** — unusual queries that should/shouldn't trigger

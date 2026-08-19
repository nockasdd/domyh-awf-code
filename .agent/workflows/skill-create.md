---
description: "Create or improve DOMYH skills with guided workflow — supports generic ecosystem skills and project-tailored codebase skills"
skills: { required: [skill-creator], contextual: [auto] }
success_criteria: "Skill created, indexed, BM25 trigger test passes, project patterns accurately captured"
---

# /skill-create — Intelligent Skill Creator Workflow

## 🛡️ [GATE 0: PRE-FLIGHT CREATION RULES — READ BEFORE CREATING SKILLS]

1. **NO DUPLICATE SKILLS**: Always search existing skills first (`hsa_search(query, action="skills")`). Extend existing skills if overlapping.
2. **PROJECT-AWARE TRACING**: When creating a project-specific skill, MUST inspect actual codebase files (`hsa_detect`, `hsa_explore`, `view_file`) to extract authentic conventions rather than generic boilerplate.
3. **REAL PRODUCTION PATTERNS**: Every skill MUST include $\ge 3$ concrete, battle-tested code examples and explicit error-handling patterns.
4. **STRICT SIZE BUDGET**: Keep `SKILL.md` $\le 500$ lines. Use `ADVANCED.md` or `references/` for deep-dive documentation.
5. **INDEX VALIDATION MANDATE**: After creating/editing a skill, MUST run `hsa_check_changes()` and verify BM25 top-3 retrieval before reporting done.

---

## 🧭 MODE SELECTION

| Mode | Command | Target Category | Use Case |
|:-----|:--------|:----------------|:---------|
| **Generic / Ecosystem** | `/skill-create [topic]` | `frameworks`, `languages`, `tooling`, `devops`, `core` | Universal skills applicable across multiple projects |
| **Project-Specific** | `/skill-create project [name]` | `projects` (`.agent/skills/projects/{slug}/`) | Custom codebase skill capturing internal APIs, DTOs, rules & conventions |

---

## 🔄 5-PHASE CREATION FLOW

### PHASE 1: DISCOVERY & CODEBASE TRACING
*   **Check Existence**: Run `hsa_search(query, action="skills")` to ensure no duplicate skill exists.
*   **If Project Mode (`/skill-create project`)**:
    1.  **Detect Tech Stack**: Call `hsa_detect(stack)` to extract runtime, frameworks, ORM, and build tools.
    2.  **Explore Architecture**: Run `hsa_explore(repo_map)` to map directory layout (`src/services/`, `controllers/`, `entities/`, `models/`).
    3.  **Harvest Idioms & Constraints**: Inspect 3-5 key source files to extract internal error classes, repository patterns, naming conventions, and forbidden anti-patterns in this repository.
*   **If Generic Mode**: Identify trigger keywords, target file patterns (`detect`), and gather official reference material.

### PHASE 2: SCAFFOLD & STRUCTURE
Create directory `.agent/skills/{category}/{name}/` and write `SKILL.md` with standard DOMYH frontmatter:

```markdown
---
name: skill-name           # kebab-case, unique identifier
description: "..."         # 50-200 chars, dense with semantic trigger keywords
detect: ["pattern/**"]     # Glob patterns that auto-trigger this skill
category: <category>       # languages | frameworks | core | devops | cross-cutting | tooling | ai-ml | projects
tier: 1                    # 1 = standard, 2 = deep-dive
---

# {Name} Architecture & Patterns

## 1. When To Use
- Specific scenarios, tasks, or file types that require this skill.

## 2. Architecture Invariants & Standards
- Core rules, internal API conventions, error-handling protocols.

## 3. Production Code Patterns (>= 3 concrete examples)
- Real, copy-pasteable idioms matching project style.

## 4. Forbidden Anti-Patterns
- Explicit list of what NOT to do in this domain / codebase.

## 5. Testing & Verification Patterns
- Standard unit/integration test patterns for this stack.
```

### PHASE 3: VALIDATE & SCHEMA AUDIT
*   **Frontmatter Audit**: Name in kebab-case, description contains search keywords, valid category, non-empty `detect` array.
*   **Quality Audit**: $\ge 3$ code examples, error handling section, forbidden anti-patterns section, $\le 500$ lines.

### PHASE 4: BM25 INDEXING & RETRIEVAL TEST
1.  **Refresh Index**: Call `hsa_check_changes()` to re-index all skills into BM25F SQLite engine.
2.  **Retrieval Test**: Call `hsa_search(query="<task scenario>", action="skills")`.
3.  **Pass Condition**: The newly created skill MUST rank in the Top 3 results for relevant queries.

### PHASE 5: ITERATE & FINALIZE
*   Test skill execution on a representative coding task.
*   Refine trigger keywords or code examples based on test results.
*   Persist session state via `hsa_session(action="persist")`.

---

## ⚡ SUB-COMMANDS

| Command | Description |
|:--------|:------------|
| `/skill-create [topic]` | Scaffold standard ecosystem skill (languages, frameworks, tools) |
| `/skill-create project [name]` | Auto-trace current codebase and scaffold project-tailored skill |
| `/skill-create test [name]` | Run BM25 search and trigger validation against a skill |
| `/skill-create refine [name]` | Iterate and improve an existing skill's code patterns |

---

## 🎯 [GATE 9: POST-FLIGHT CREATION CHECKLIST — VERIFY BEFORE REPORTING]

Before declaring skill creation complete, MUST self-audit these 5 golden criteria:
1.  ✅ **Did I verify no duplicate/overlapping skill already existed?**
2.  ✅ **Are code examples extracted from real, working patterns (no synthetic pseudocode)?**
3.  ✅ **Is `SKILL.md` strictly within the $\le 500$ lines limit?**
4.  ✅ **Did I run `hsa_check_changes()` and confirm Top-3 BM25 search ranking?**
5.  ✅ **Does the `detect` glob accurately match relevant project files?**

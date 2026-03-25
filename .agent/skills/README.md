# 🧠 Skills Directory

> 103 skills across 8 categories — Progressive Disclosure Architecture

---

## Directory Structure

```
skills/
├── INDEX.yaml              ← Universal routing index (all skills)
├── {category}/
│   ├── _index.yaml         ← Category registry (count, metadata)
│   └── {skill-name}/
│       ├── META.yaml       ← T1: Always loaded (~100 tokens)
│       ├── SKILL.md        ← T2: On-demand (~1,500 tokens)
│       ├── ADVANCED.md     ← T3: Referenced only (~4,000 tokens)
│       ├── data/           ← T3: Pattern/checklist YAML files
│       │   └── *.yaml
│       └── test/           ← Optional: Skill eval tests
│           └── eval.yaml   ← Evaluation prompts & assertions
└── README.md               ← This file
```

## 3-Tier Progressive Loading

| Tier | File | Tokens | When Loaded |
|:-----|:-----|:-------|:------------|
| **T1** | `META.yaml` | ~50-100 | Always (startup) |
| **T2** | `SKILL.md` | ~1,500 | When skill actively used |
| **T3** | `ADVANCED.md` + `data/` | ~4,000+ | Only on explicit request |

## META.yaml Schema

```yaml
# Required fields
name: skill-name            # Must match directory name
display: "Human Name"       # Display name
category: core              # core|cross-cutting|languages|frameworks|devops|tooling|ai-ml|governance
tier: 1                     # Always 1
priority: 3                 # Lower = higher (0=highest)

# Recommended fields
version: "1.0.0"            # SemVer — track skill changes
desc: "..."                 # For AI matching (<1024 chars, specific)

# Discovery
triggers:
  file_patterns: ["*.ts"]   # Auto-activate on these files
  keywords: [...]           # BM25 matching terms
  intents: [...]            # Semantic intent phrases

# Capabilities
caps: [...]                 # What this skill can do

# Optional
data_files: [...]           # T3 data file paths
related_skills: [...]       # Cross-references
```

## SKILL.md Convention

- **Frontmatter**: YAML with name, description, detect, category, tier
- **Body**: Markdown instructions, tables, code examples
- **Target**: ~1,500 tokens (max 500 lines)
- **Style**: Actionable patterns, checklists, tables — not essays

## data/ Directory Convention

For complex skills needing reference data:

```yaml
# data/patterns.yaml
patterns:
  - id: PATTERN-001
    name: Pattern Name
    description: When to use
    code: |
      // Example code
    related: [PATTERN-002]
```

Use `data_files:` in META.yaml to declare data files.

## test/ Directory Convention

For skill quality validation (see `core/reference/EVAL_SCHEMA.yaml`):

```yaml
# test/eval.yaml
evals:
  - name: eval_name
    prompt: "Input prompt"
    expected_skill: skill-id
    expected_output_contains: ["pattern1"]
    severity: critical | important | nice-to-have
```

Optional: skills are NOT required to have tests, but core skills SHOULD.

## Categories

| Category | Count | Priority | Description |
|:---------|:------|:---------|:------------|
| core | 9 | 0 | Security, auth, API, errors, logging, observability, context, skill-creator, graph-patterns |
| languages | 28 | 1 | Go, Python, TS, JS, Rust, C++, C, C#, Java, etc. |
| frameworks | 9 | 2 | React, Vue, Next.js, Angular, Nuxt, Svelte, Flutter, RN, Streamlit |
| devops | 7 | 3 | Docker, K8s, AWS, CI/CD, Terraform, Azure, GCP |
| cross-cutting | 26 | 4 | Testing, database, TDD, accessibility, SEO, etc. |
| tooling | 6 | 5 | MCP, IDE ext, CLI, API protocols, browser agent, HSA toolkit |
| ai-ml | 9 | 6 | AI agents, RAG, prompt eng, vector search, Gemini, ML pipelines |
| governance | 9 | 7 | Session memory, context integrity, delegation, evidence, context-compaction, etc. |

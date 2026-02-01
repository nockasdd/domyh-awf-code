# Skills Customization Framework

# DOMYH Agent v4.3

---

## Overview

The Skills Customization Framework allows users to:

1. Create custom skills
2. Modify existing skills
3. Configure skill loading behavior
4. Define project-specific patterns

---

## Creating a Custom Skill

### Directory Structure

```
.agent/skills/my-skill/
├── META.yaml      # Tier 1: Metadata (required)
├── SKILL.md       # Tier 2: Working patterns (required)
└── ADVANCED.md    # Tier 3: Deep reference (optional)
```

### META.yaml Template

```yaml
name: my-skill
display_name: My Custom Skill
category: custom
priority: 5

description: Short description under 60 chars

keywords: [keyword1, keyword2, keyword3]

detect: ["pattern/*.ext", "*.config"]

capabilities: [Cap1, Cap2, Cap3]
```

### SKILL.md Template

```markdown
# My Skill Patterns

## Quick Reference

- Pattern 1
- Pattern 2

## Common Tasks

### Task 1

[Steps and examples]

## Checklist

- [ ] Item 1
- [ ] Item 2
```

---

## Skill Categories

| Category  | Priority | Description                     |
| --------- | -------- | ------------------------------- |
| core      | 0        | Always-active skills (security) |
| language  | 1        | Programming languages           |
| framework | 2        | Frameworks (React, Vue, etc.)   |
| devops    | 3        | Infrastructure tools            |
| support   | 4        | Cross-cutting concerns          |
| custom    | 5        | User-defined skills             |

---

## Configuration Options

### Project-level (.agent/config.yaml)

```yaml
skills:
  disabled: [skill1, skill2] # Disable specific skills
  priority_override:
    my-skill: 0 # Make custom skill high priority

  custom:
    path: ./custom-skills/ # Custom skills directory
    auto_load: true
```

### Skill Loading Modes

| Mode        | Description                      | Use Case     |
| ----------- | -------------------------------- | ------------ |
| progressive | Load T1, activate T2 on-demand   | Default      |
| eager       | Preload all T2 for active skills | Low latency  |
| lazy        | Load only when explicitly needed | Token saving |

---

## Extending the System

### Adding Keywords to Existing Skills

Edit `skills/[skill]/META.yaml`:

```yaml
keywords:
  - existing_keyword
  - my_new_keyword # Add here
```

### Regenerate Embeddings

```bash
python scripts/semantic_selector.py --generate
```

---

## Best Practices

1. **Keep T1 under 100 tokens** — Concise metadata
2. **Keep T2 under 1500 tokens** — Working patterns only
3. **Use T3 for deep content** — Reference material
4. **Test semantic matching** — Verify detection works
5. **Document capabilities** — Clear skill boundaries

---

_DOMYH Agent v4.3 — Customization Framework_

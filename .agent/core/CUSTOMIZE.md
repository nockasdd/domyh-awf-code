# Skills Customization Framework

# DOMYH Awesome Code

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

private:
  path: ./private/ # Private skills directory
  auto_load: true
  override_public: true # Private takes precedence
  registry: ./private/_index.yaml
```

### Skill Loading Modes

| Mode        | Description                      | Use Case     |
| ----------- | -------------------------------- | ------------ |
| progressive | Load T1, activate T2 on-demand   | Default      |
| eager       | Preload all T2 for active skills | Low latency  |
| lazy        | Load only when explicitly needed | Token saving |

---

## 🔒 Private Skills

> Skills riêng cho dự án / công ty — **KHÔNG** commit vào repo public.

### Overview

Private skills are stored in `.agent/private/` which is **gitignored**. They follow the same 3-tier structure as public skills but have `priority: -1` (highest), meaning they override public skills with the same ID.

```
Skill Resolution:
  private/ (priority -1) → skills/ (priority 0-5)
```

### Creating a Private Skill

**Step 1**: Copy `.agent/private/_template/` to a new directory:

```bash
# PowerShell
Copy-Item -Recurse .agent/private/_template .agent/private/my-skill
```

**Step 2**: Edit the files:

| File          | Action                                               |
| ------------- | ---------------------------------------------------- |
| `META.yaml`   | Change `name`, `display`, `desc`, `triggers`, `caps` |
| `SKILL.md`    | Write patterns, checklists, examples                 |
| `data/*.yaml` | Add data files if needed                             |

**Step 3**: Register in `_index.yaml`:

```yaml
count: 1
skills:
  - { id: my-skill, has_advanced: false }
```

### Private Skill Categories

| Use Case                  | Example                                          |
| ------------------------- | ------------------------------------------------ |
| Company API conventions   | Internal naming, patterns, endpoints             |
| Project-specific patterns | Domain models, architecture decisions            |
| Client-specific code      | Custom integrations, proprietary logic           |
| Override public skills    | Replace `testing` with company testing standards |

### Override Rules

- Private skill with **same ID** as a public skill → private wins
- Private skills have `category: private` and `priority: -1`
- Listed in `private/_index.yaml`, not in `skills/_categories.yaml`

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
6. **Use private/ for internal skills** — Never commit company-specific patterns to public repo

---

_DOMYH Awesome Code — Customization Framework_

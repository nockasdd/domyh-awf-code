# 🎯 Implementation Plan v5 — IDE Compiler Architecture

> **Version**: 5.4.0 → 5.5.0 | **Time**: 10-12 hours
> **Coverage**: 35% → 95%+ | **IDEs**: 14

---

## 🏗️ Architecture Overview

```
domyh.rules/           ← Canonical Source (Single Truth)
    ├── manifest.yaml
    ├── core/*.rule.md
    ├── skills/**/*.rule.md
    ├── commands/*.rule.md
    └── profiles/
         ├── minimal.yaml
         ├── standard.yaml
         └── full.yaml

            ↓ Compiler Pipeline ↓

adapters/
    ├── cursor.ts      → .cursor/rules/*.mdc
    ├── cline.ts       → .clinerules/*.md
    ├── continue.ts    → .continue/rules/*.md
    ├── copilot.ts     → .github/instructions/*.md
    └── ...
```

---

## Phase 0: Critical Bug Fixes — 2 hours

### 0.1 Cursor Globs Space Bug (P0 CRITICAL)

```typescript
// adapters/cursor.ts
compile(rules: CanonicalRule[]): GeneratedFile[] {
  return rules.map(rule => {
    const globs = rule.selectors?.globs || ["**/*"]

    // CRITICAL: Join WITHOUT spaces
    const globsString = globs.join(",")  // NOT ", "!

    // Validate no spaces
    if (globsString.includes(", ")) {
      throw new AdapterError(
        "CURSOR_GLOBS_SPACE_BUG",
        `Globs cannot have spaces after commas: "${globsString}"`,
        { fix: globsString.replace(/, /g, ",") }
      )
    }

    const frontmatter = {
      description: rule.meta.name || rule.meta.title,
      globs: globsString,
      alwaysApply: rule.applies.alwaysApply ?? true
    }

    return {
      path: `.cursor/rules/${this.filename(rule)}.mdc`,
      content: this.render(frontmatter, rule.bodyMarkdown)
    }
  })
}

validateOutput(files: GeneratedFile[]): ValidationResult {
  const errors = []

  for (const file of files) {
    // Check flat structure
    if (file.path.split('/').length > 3) {
      errors.push({
        code: "CURSOR_NO_NESTED",
        message: "Cursor requires flat .mdc files"
      })
    }

    // Check globs format
    const match = file.content.match(/^globs:\s*(.+)$/m)
    if (match?.[1]?.includes(", ")) {
      errors.push({
        code: "CURSOR_GLOBS_SPACE",
        message: "Remove spaces after commas in globs",
        fix: match[1].replace(/, /g, ",")
      })
    }
  }

  return { valid: errors.length === 0, errors }
}
```

### 0.2 Continue.dev Name Field Fix

```typescript
// adapters/continue.ts
compile(rules: CanonicalRule[]): GeneratedFile[] {
  return rules.map(rule => {
    const frontmatter: any = {}

    // Use 'name' NOT 'title'!
    frontmatter.name = rule.meta.name || rule.meta.title

    // Handle alwaysApply (3 states)
    if (rule.applies.alwaysApply !== undefined) {
      frontmatter.alwaysApply = rule.applies.alwaysApply
    }
    // undefined = let Continue.dev decide

    return {
      path: `.continue/rules/${this.filename(rule)}.md`,
      content: this.render(frontmatter, rule.bodyMarkdown)
    }
  })
}
```

### 0.3 Cline Paths Array Support

```typescript
// adapters/cline.ts
compile(rules: CanonicalRule[]): GeneratedFile[] {
  return rules.map(rule => {
    const frontmatter: any = {}

    // Cline uses 'paths' array (not 'globs')
    if (rule.selectors?.globs?.length) {
      frontmatter.paths = rule.selectors.globs  // Array OK
    }

    if (rule.meta.description) {
      frontmatter.description = rule.meta.description
    }

    if (rule.meta.tags?.length) {
      frontmatter.tags = rule.meta.tags
    }

    // Numeric prefix for ordering
    const filename = `${String(rule.meta.priority).padStart(2, '0')}-${rule.meta.id}.md`

    return {
      path: `.clinerules/${filename}`,
      content: this.render(frontmatter, rule.bodyMarkdown)
    }
  })
}
```

---

## Phase 1: Canonical Schema — 2 hours

### 1.1 Schema Definition

```typescript
// src/schema/canonical.ts
interface CanonicalRule {
  meta: {
    id: string; // Unique ID
    name: string; // For Continue.dev
    title: string; // Human display
    scope: "core" | "skill" | "command" | "policy";
    priority: number; // 0-99
    description?: string;
    tags?: string[];
  };

  selectors: {
    globs?: string[]; // Array (canonical)
    paths?: string[]; // Cline format
    regex?: string[]; // Continue.dev
    languages?: string[];
  };

  applies: {
    alwaysApply?: boolean; // true|false|undefined
    strategy: "always" | "conditional" | "manual";
  };

  token: {
    budget?: number;
    verbosity?: "low" | "medium" | "high";
  };

  constraints: {
    cursorNoSpaceGlobs?: boolean;
    rooNoFrontmatter?: boolean;
    copilotExcludeAgent?: string;
  };

  bodyMarkdown: string;
}
```

### 1.2 Manifest

```yaml
# domyh.rules/manifest.yaml
version: 5.5.0
defaultProfile: standard
ruleFileGlob: "**/*.rule.md"

ordering:
  strategy: priority_then_path

defaults:
  token:
    core: 300
    skill: 600
    command: 200

adapters:
  enabled:
    - cursor
    - cline
    - continue
    - copilot
    - roo
    - windsurf
    - jetbrains
    - amazonq
    - claude
    - gemini
    - zed
```

---

## Phase 2: Adapter Implementation — 4 hours

### 2.1 Base Adapter Interface

```typescript
// src/adapters/base.ts
interface IDEAdapter {
  id: string;

  capabilities: {
    frontmatter: "required" | "optional" | "none";
    globsFormat: "comma-no-space" | "array" | "none";
    supportsConditional: boolean;
  };

  compile(rules: CanonicalRule[], ctx: Context): GeneratedFile[];
  validateOutput(files: GeneratedFile[]): ValidationResult;
  explain(rules: CanonicalRule[]): string;
}
```

### 2.2 IDE Configs Registry

```typescript
// src/adapters/registry.ts
const IDE_ADAPTERS = {
  cursor: {
    path: ".cursor/rules/",
    ext: ".mdc",
    frontmatter: "required",
    globsFormat: "comma-no-space", // CRITICAL!
    fields: ["description", "globs", "alwaysApply"],
  },
  cline: {
    path: ".clinerules/",
    ext: ".md",
    frontmatter: "optional",
    globsFormat: "array",
    fields: ["paths", "description", "tags"],
  },
  continue: {
    configPath: ".continue/config.yaml",
    rulesPath: ".continue/rules/",
    ext: ".md",
    frontmatter: "optional",
    fields: ["name", "alwaysApply", "globs"], // 'name' NOT 'title'
  },
  copilot: {
    repoWide: ".github/copilot-instructions.md",
    pathScoped: ".github/instructions/",
    ext: ".instructions.md",
    frontmatter: "required",
    fields: ["applyTo", "excludeAgent"],
  },
  roo: {
    path: ".roo/rules/",
    ext: ".md",
    frontmatter: "none", // NO frontmatter!
  },
  windsurf: {
    legacy: ".windsurfrules",
    modular: ".windsurf/rules/",
    ext: ".md",
    frontmatter: "none",
  },
  jetbrains: {
    path: ".aiassistant/rules/",
    ext: ".md",
    frontmatter: "none",
  },
  amazonq: {
    path: ".amazonq/rules/",
    ext: ".md",
    frontmatter: "none",
    supportsSubdirs: true,
  },
  claude: {
    skillsPath: ".claude/skills/",
    file: "SKILL.md",
    frontmatter: "required",
    fields: ["name", "description"],
  },
  gemini: {
    configPath: ".gemini/config.yaml",
    stylePath: ".gemini/styleguide.md",
  },
  zed: {
    rulesLibrary: true,
    profiles: ["write", "ask", "minimal"],
  },
};
```

---

## Phase 3: CLI Commands — 2 hours

### 3.1 Install Command

```bash
dawf install --ide cursor --profile standard
dawf install --ide all --profile minimal
dawf install --list  # Show all IDEs with market share
```

### 3.2 Validate Command

```bash
dawf validate --ide cursor
# ✓ Checking .mdc flat structure
# ✓ Checking globs format (no spaces)
# ✓ Checking required frontmatter fields
# ✓ All 3 rules valid

dawf validate --all
# cursor: 3/3 valid
# cline: 3/3 valid
# continue: 3/3 valid
# ...
```

### 3.3 Doctor Command

```bash
dawf doctor
# IDE: cursor
# Load Order:
#   1. 00-core.mdc (alwaysApply: true)
#   2. 20-frontend.mdc (globs: src/**/*.tsx)
#   3. 30-backend.mdc (globs: src/api/**)
#
# Token Budget:
#   Core: 250/300 tokens
#   Skills: 450/600 tokens
#   Total: 700/1500 tokens (47%)
```

---

## Phase 4: Validation Pipeline — 2 hours

### 4.1 Multi-Layer Validation

```typescript
// src/validation/pipeline.ts
async function validate(rules: CanonicalRule[], adapters: IDEAdapter[]) {
  const results: ValidationReport = {};

  // Layer 1: Schema validation
  results.schema = validateSchema(rules);

  // Layer 2: Per-adapter pre-validation
  for (const adapter of adapters) {
    results[`pre-${adapter.id}`] = adapter.validateCanonical?.(rules);
  }

  // Layer 3: Compile
  const compiled = new Map<string, GeneratedFile[]>();
  for (const adapter of adapters) {
    compiled.set(adapter.id, adapter.compile(rules, ctx));
  }

  // Layer 4: Post-compile validation
  for (const [id, files] of compiled) {
    const adapter = adapters.find((a) => a.id === id)!;
    results[`post-${id}`] = adapter.validateOutput(files);
  }

  // Layer 5: Cross-consistency
  results.consistency = validateConsistency(compiled);

  // Layer 6: Token budget
  results.tokenBudget = validateTokenBudget(rules, ctx.profile);

  return results;
}
```

---

## Output Structure (Complete)

```
project/
├── AGENTS.md
├── CLAUDE.md
├── .cursorrules                    # Legacy
├── .cursor/rules/
│   ├── 00-core.mdc                # FLAT, no subfolders!
│   ├── 20-frontend.mdc
│   └── 30-backend.mdc
├── .clinerules/
│   ├── 01-core.md
│   ├── 02-frontend.md
│   └── 03-backend.md
├── .continue/
│   ├── config.yaml
│   └── rules/
│       ├── 00-core.md             # name field
│       └── 20-frontend.md
├── .roo/rules/                    # NO frontmatter
│   ├── 00-core.md
│   └── 20-frontend.md
├── .github/
│   ├── copilot-instructions.md    # Repo-wide
│   └── instructions/
│       ├── frontend.instructions.md  # applyTo: src/**
│       └── backend.instructions.md
├── .aiassistant/rules/
│   └── 00-core.md
├── .amazonq/rules/
│   └── 00-core.md
├── .claude/skills/domyh/
│   └── SKILL.md
├── .gemini/
│   ├── config.yaml
│   └── styleguide.md
├── .windsurf/rules/
│   ├── 01-core.md
│   └── 02-frontend.md
└── .aider.conf.yml
```

---

## Priority Matrix

| Phase | Task                   | Priority | Time | Blocking |
| ----- | ---------------------- | -------- | ---- | -------- |
| 0.1   | Cursor globs space bug | **P0**   | 30m  | YES      |
| 0.2   | Continue name field    | **P0**   | 20m  | YES      |
| 0.3   | Cline paths array      | **P0**   | 20m  | YES      |
| 0.4   | Roo no frontmatter     | **P0**   | 15m  | YES      |
| 1.1   | Canonical schema       | P1       | 1h   |          |
| 1.2   | Manifest               | P1       | 30m  |          |
| 2.x   | All adapters           | P1       | 4h   |          |
| 3.x   | CLI commands           | P2       | 2h   |          |
| 4.x   | Validation             | P2       | 2h   |          |

---

## Expected Results

| Metric           | Before | After              |
| ---------------- | ------ | ------------------ |
| Production Score | 5.5/10 | **9.0/10**         |
| IDEs Supported   | 6      | **14**             |
| Format Errors    | 4      | **0**              |
| Token Savings    | 0%     | **-60%** (Copilot) |
| Market Coverage  | ~35%   | **95%+**           |

---

_DOMYH Implementation Plan v5 • Compiler Architecture • 2026-02-03_

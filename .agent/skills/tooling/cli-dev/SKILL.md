---
name: cli-dev
version: "6.4.0"
category: tooling
---

# CLI Tool Development

> Progressive Discovery • Subcommands • Structured Output  
> commander.js • clap • cobra • Click

---

## Khi Nào Dùng

- Build CLI tool cho developer (dev tooling)
- Interactive terminal applications
- Tạo CLI wrapper cho API/service

## Framework Selection

| Framework        | Language   | Strengths                           |
| ---------------- | ---------- | ----------------------------------- |
| **commander.js** | Node.js/TS | Simple, widely used, npm ecosystem  |
| **clap**         | Rust       | Type-safe, derive macros, fast      |
| **cobra**        | Go         | Subcommands, auto-docs, completions |
| **Click**        | Python     | Decorators, composable, testable    |
| **clack**        | Node.js    | Beautiful interactive prompts       |

## Core Patterns

### Progressive Discovery UX

```
Level 1: mycli              → Show help + suggest commands
Level 2: mycli --help       → Detailed help with examples
Level 3: mycli <cmd> --help → Command-specific help
Level 4: mycli suggest      → AI-powered suggestions
```

### Structured Output

```typescript
// Support multiple formats
if (flags.format === "json") {
  console.log(JSON.stringify(data, null, 2));
} else if (flags.format === "yaml") {
  console.log(yaml.stringify(data));
} else {
  console.log(table(data)); // Pretty table for humans
}
```

### Exit Codes

| Code | Meaning                  |
| ---- | ------------------------ |
| 0    | Success                  |
| 1    | General error            |
| 2    | Usage error (wrong args) |
| 130  | Interrupted (Ctrl+C)     |

### Error Handling

```typescript
try {
  await command.execute();
} catch (err) {
  if (err instanceof UsageError) {
    console.error(chalk.red(`Error: ${err.message}`));
    console.log(chalk.dim("Run --help for usage"));
    process.exit(2);
  }
  console.error(chalk.red(`Fatal: ${err.message}`));
  process.exit(1);
}
```

## Common Traps

| Trap                  | Fix                                         |
| --------------------- | ------------------------------------------- |
| No colors in CI       | Detect CI env, disable colors automatically |
| Global install issues | Use `npx` or `bunx` for zero-install        |
| No completions        | Add shell completion generator              |

---

_DOMYH Awesome Code • CLI Dev Skill v1.0.0_

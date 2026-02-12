# DOMYH Awesome Code — IDE Configurations

> Version 6.1.2 | Progressive Disclosure Architecture

## Supported AI Coding Assistants

| IDE                        | Config File  | Description             |
| -------------------------- | ------------ | ----------------------- |
| [Claude Code](claude.json) | CLAUDE.md    | Claude Code integration |
| [Cursor](cursor.json)      | .cursorrules | Cursor AI integration   |
| [Gemini CLI](gemini.json)  | GEMINI.md    | Gemini CLI integration  |

## Configuration Structure

Each IDE config contains:

```json
{
  "name": "DOMYH Awesome Code ",
  "version": "v6.2.3",

  "activation": {
    /* Trigger commands */
  },
  "skills": {
    /* Progressive loading */
  },
  "token_budget": {
    /* Token limits */
  }
}
```

## Session Rules

Session rules are **automatically handled** by the agent reading `GEMINI.md`:

1. Agent reads `## Session Rules (v6.0)` section in GEMINI.md
2. Agent detects trigger phrases in user messages
3. Agent saves preferences to `.agent/memory/session_rules.json`
4. Agent loads rules via CONTEXT_LOADER.yaml at start of each response

**No external scripts needed** — agent self-executes based on instructions.

---

_DOMYH Awesome Code • NockDev_

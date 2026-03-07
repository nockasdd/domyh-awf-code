---
description: 💾 Save session state to memory files for later context
---

# /save — Session Persistence

## Purpose

Save the current session state to memory files, enabling context continuity across conversations. This captures key decisions, changes made, and next steps.

## Steps

### 1. Gather Session Context

Collect from current conversation:
- **Changes made**: Files modified, features added, bugs fixed
- **Key decisions**: Architecture choices, trade-offs, conventions established
- **Current status**: What's working, what's pending
- **Next steps**: Planned work, open questions

### 2. Update CONTEXT_SNAPSHOT.md

Write to `.agent/memory/CONTEXT_SNAPSHOT.md`:

```markdown
# Context Snapshot
> Last updated: <timestamp>

## Current Status
<what's working, project state>

## Recent Changes
<files modified, features added>

## Key Decisions
<architecture choices, conventions>

## Next Steps
<planned work, open items>
```

### 3. MCP Session Persist (if available)

If MCP is connected:
```
hsa_session({
  action: 'persist',
  snapshot: {
    current_status: '...',
    recent_changes: '...',
    key_decisions: '...',
    next_steps: '...'
  }
})
```

### 4. Confirm

Report what was saved:
- Number of items captured
- File path(s) updated
- Notification sent (if Telegram configured)

## Examples

```
/save                    → Save full session state
/save Quick checkpoint   → Save with custom note
```

## Notes

- CONTEXT_SNAPSHOT.md is read at the start of every new conversation
- MCP persist also updates `session.md` with task history
- If Telegram is configured, a notification is sent confirming the save

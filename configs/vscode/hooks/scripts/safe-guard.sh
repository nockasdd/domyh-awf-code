#!/bin/bash
# DOMYH AWF Safe Guard — PreToolUse Hook
# Blocks dangerous commands before execution
#
# Input: JSON on stdin from Copilot
# Output: JSON with permissionDecision (allow/deny/ask)

INPUT=$(cat 2>/dev/null || echo '{}')
TOOL=$(echo "$INPUT" | jq -r '.toolName // empty' 2>/dev/null)

# Only check execute tool (terminal commands)
if [ "$TOOL" = "execute" ] || [ "$TOOL" = "terminal" ]; then
  CMD=$(echo "$INPUT" | jq -r '.input.command // empty' 2>/dev/null)
  
  # Block destructive patterns
  if echo "$CMD" | grep -qiE 'rm\s+-rf\s+/|rm\s+-rf\s+~|DROP\s+(TABLE|DATABASE)|TRUNCATE\s+TABLE|FORMAT\s+[A-Z]:'; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked by DOMYH safety hook: destructive command detected"}}'
    exit 0
  fi
  
  # Ask confirmation for potentially risky operations
  if echo "$CMD" | grep -qiE 'rm\s+-rf|git\s+push\s+--force|git\s+reset\s+--hard|npm\s+publish|docker\s+system\s+prune'; then
    echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"DOMYH safety: potentially destructive command requires confirmation"}}'
    exit 0
  fi
fi

# Allow by default
echo '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'

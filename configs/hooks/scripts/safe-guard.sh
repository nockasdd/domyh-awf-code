#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF PreToolUse Hook: Config-Driven Command Safety Guard
# Reads blocked-commands.json for deny/ask rules with safe_patterns
# Compatible with: VS Code Copilot, Claude Code, Cursor
#
# Protocol:
#   VS Code Copilot: exit 0 + JSON stdout {permissionDecision}
#   Claude Code:     exit 0 + JSON stdout OR exit 2 + stderr
#   Both support:    hookSpecificOutput → permissionDecision
#
# v3.1: Dynamic config resolution — multi-path fallback
# ═══════════════════════════════════════════════════════════════

set -uo pipefail

HOOK_INPUT=$(cat)
TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# Only check terminal/command tools
case "$TOOL_NAME" in
  runTerminalCommand|Bash|execute|run_command|send_command_input)
    ;;
  *)
    echo '{"continue":true}'
    exit 0
    ;;
esac

# Extract command from tool input (handle different IDE field names)
COMMAND=$(echo "$HOOK_INPUT" | jq -r '
  .tool_input.command //
  .tool_input.CommandLine //
  .tool_input.Input //
  .tool_input.cmd //
  empty
' 2>/dev/null)

if [ -z "$COMMAND" ]; then
  echo '{"continue":true}'
  exit 0
fi

# ── Dynamic Config Resolution ─────────────────────────────
# Multi-path fallback — works for project, global, and custom installs
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

find_hook_config() {
  local name="$1"
  # 1. Env var override (user/CI custom path)
  if [ -n "${AWF_HOOKS_CONFIG:-}" ] && [ -f "${AWF_HOOKS_CONFIG}/${name}" ]; then
    echo "${AWF_HOOKS_CONFIG}/${name}"; return 0
  fi
  # 2. Relative to script (AWF source: scripts/../config/)
  local relative="$SCRIPT_DIR/../config/$name"
  if [ -f "$relative" ]; then echo "$relative"; return 0; fi
  # 3. Flat structure (config next to scripts)
  local flat="$SCRIPT_DIR/config/$name"
  if [ -f "$flat" ]; then echo "$flat"; return 0; fi
  # 4-6. Project install locations (cwd-relative)
  local project_paths=(".github/hooks/config/$name" ".claude/hooks/config/$name" ".agent/hooks/config/$name")
  for p in "${project_paths[@]}"; do
    if [ -f "$p" ]; then echo "$p"; return 0; fi
  done
  # 7. Global fallback
  local home="${HOME:-${USERPROFILE:-}}"
  if [ -n "$home" ] && [ -f "$home/.gemini/antigravity/hooks/config/$name" ]; then
    echo "$home/.gemini/antigravity/hooks/config/$name"; return 0
  fi
  return 1
}

CONFIG=$(find_hook_config "blocked-commands.json") || { echo '{"continue":true}'; exit 0; }

# Validate JSON config
if ! jq empty "$CONFIG" 2>/dev/null; then
  echo '{"continue":true}'
  exit 0
fi

# Output blocking decision (protocol-compatible for both VS Code + Claude Code)
output_decision() {
  local action="$1"
  local reason="$2"
  jq -n \
    --arg action "$action" \
    --arg reason "[AWF Safety] $reason" \
    '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:$action,permissionDecisionReason:$reason}}'
  exit 0
}

# Check each rule in blocked-commands.json
RULE_COUNT=$(jq 'length' "$CONFIG" 2>/dev/null || echo 0)
i=0
while [ "$i" -lt "$RULE_COUNT" ]; do
  PATTERN=$(jq -r ".[$i].pattern" "$CONFIG" 2>/dev/null)
  ACTION=$(jq -r ".[$i].action" "$CONFIG" 2>/dev/null)
  REASON=$(jq -r ".[$i].reason" "$CONFIG" 2>/dev/null)

  if echo "$COMMAND" | grep -qEi "$PATTERN" 2>/dev/null; then
    IS_SAFE=false
    SAFE_COUNT=$(jq -r ".[$i].safe_patterns | length" "$CONFIG" 2>/dev/null || echo 0)
    j=0
    while [ "$j" -lt "$SAFE_COUNT" ]; do
      SAFE_PAT=$(jq -r ".[$i].safe_patterns[$j]" "$CONFIG" 2>/dev/null)
      if [ -n "$SAFE_PAT" ] && echo "$COMMAND" | grep -qF "$SAFE_PAT" 2>/dev/null; then
        IS_SAFE=true
        break
      fi
      j=$((j + 1))
    done

    if [ "$IS_SAFE" = false ]; then
      output_decision "$ACTION" "$REASON"
    fi
  fi

  i=$((i + 1))
done

echo '{"continue":true}'

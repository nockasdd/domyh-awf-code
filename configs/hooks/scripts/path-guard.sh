#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF PreToolUse Hook: File-Path Guard
# Blocks modification of protected files (.env, .git, locks, SSH)
# Reads protected-paths.json for configurable deny/ask rules
#
# v1.1: Dynamic config resolution — multi-path fallback
# ═══════════════════════════════════════════════════════════════

set -uo pipefail

HOOK_INPUT=$(cat)
TOOL_NAME=$(echo "$HOOK_INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# Only check file edit/create tools
case "$TOOL_NAME" in
  editFiles|createFile|Write|Edit|MultiEdit|write_to_file|replace_file_content|multi_replace_file_content)
    ;;
  *)
    echo '{"continue":true}'
    exit 0
    ;;
esac

# Extract file path
FILE_PATH=$(echo "$HOOK_INPUT" | jq -r '
  .tool_input.files[0] //
  .tool_input.path //
  .tool_input.TargetFile //
  .tool_input.file_path //
  empty
' 2>/dev/null)

if [ -z "$FILE_PATH" ]; then
  echo '{"continue":true}'
  exit 0
fi

# ── Dynamic Config Resolution ─────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

find_hook_config() {
  local name="$1"
  if [ -n "${AWF_HOOKS_CONFIG:-}" ] && [ -f "${AWF_HOOKS_CONFIG}/${name}" ]; then
    echo "${AWF_HOOKS_CONFIG}/${name}"; return 0
  fi
  local relative="$SCRIPT_DIR/../config/$name"
  if [ -f "$relative" ]; then echo "$relative"; return 0; fi
  local flat="$SCRIPT_DIR/config/$name"
  if [ -f "$flat" ]; then echo "$flat"; return 0; fi
  local project_paths=(".github/hooks/config/$name" ".claude/hooks/config/$name" ".agent/hooks/config/$name")
  for p in "${project_paths[@]}"; do
    if [ -f "$p" ]; then echo "$p"; return 0; fi
  done
  local home="${HOME:-${USERPROFILE:-}}"
  if [ -n "$home" ] && [ -f "$home/.gemini/antigravity/hooks/config/$name" ]; then
    echo "$home/.gemini/antigravity/hooks/config/$name"; return 0
  fi
  return 1
}

CONFIG=$(find_hook_config "protected-paths.json") || { echo '{"continue":true}'; exit 0; }

# Check each protected path rule
RULE_COUNT=$(jq '.protected_paths | length' "$CONFIG" 2>/dev/null || echo 0)
i=0
while [ "$i" -lt "$RULE_COUNT" ]; do
  PATTERN=$(jq -r ".protected_paths[$i].pattern" "$CONFIG" 2>/dev/null)
  ACTION=$(jq -r ".protected_paths[$i].action" "$CONFIG" 2>/dev/null)
  REASON=$(jq -r ".protected_paths[$i].reason" "$CONFIG" 2>/dev/null)

  if echo "$FILE_PATH" | grep -qEi "$PATTERN" 2>/dev/null; then
    jq -n \
      --arg action "$ACTION" \
      --arg reason "[AWF Path Guard] $REASON" \
      '{hookSpecificOutput:{hookEventName:"PreToolUse",permissionDecision:$action,permissionDecisionReason:$reason}}'
    exit 0
  fi

  i=$((i + 1))
done

echo '{"continue":true}'

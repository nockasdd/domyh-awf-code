#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF Stop Hook: Auto-Persist Session Context
# Fires when agent completes or user stops — saves session data
# Compatible with: Claude Code, Cursor, VS Code Copilot
#
# Protocol:
#   Outputs hookSpecificOutput JSON with session summary
#   Uses same pattern as inject-context.sh
#
# v1.0: Initial implementation — session end marker + git status
# ═══════════════════════════════════════════════════════════════

set -uo pipefail

# Drain stdin (Stop event may or may not send input)
cat > /dev/null 2>&1 || true

# ── Check AWF installation ─────────────────────────────────
# Try multiple known memory paths (IDE-dependent)
MEMORY_DIR=""
for candidate in ".agent/memory" ".claude/memory" ".cursor/memory"; do
  if [ -d "$candidate" ]; then
    MEMORY_DIR="$candidate"
    break
  fi
done

if [ -z "$MEMORY_DIR" ]; then
  echo '{"continue":true}'
  exit 0
fi

SESSION_FILE="$MEMORY_DIR/session.md"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

# ── Append session end marker ──────────────────────────────
if [ -f "$SESSION_FILE" ]; then
  {
    echo ""
    echo "### $TIMESTAMP — Session ended (auto-saved by AWF hook)"
  } >> "$SESSION_FILE" 2>/dev/null || true
fi

# ── Gather git status for context ──────────────────────────
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
DIRTY_COUNT=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0")
GIT_STATUS="clean"
if [ "$DIRTY_COUNT" -gt 0 ] 2>/dev/null; then
  GIT_STATUS="${DIRTY_COUNT} uncommitted"
fi

# ── Output JSON ────────────────────────────────────────────
jq -n \
  --arg branch "$BRANCH" \
  --arg git "$GIT_STATUS" \
  --arg ts "$TIMESTAMP" \
  '{hookSpecificOutput:{hookEventName:"Stop",additionalContext:("AWF session auto-saved at " + $ts + ". Branch: " + $branch + ", Git: " + $git)}}'

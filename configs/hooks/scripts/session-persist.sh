#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF Stop Hook: Auto-Persist Session Context
# Fires when agent completes or user stops — saves session data
# Compatible with: Claude Code, Cursor, VS Code Copilot
#
# v2.0: Rich context — git diff summary, recent files, structured snapshot
# ═══════════════════════════════════════════════════════════════

set -uo pipefail

# Drain stdin (Stop event may or may not send input)
cat > /dev/null 2>&1 || true

# ── Check AWF installation ─────────────────────────────────
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
SNAPSHOT_FILE="$MEMORY_DIR/CONTEXT_SNAPSHOT.md"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

# ── Gather git context ────────────────────────────────────
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
DIRTY_COUNT=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0")
GIT_STATUS="clean"
if [ "$DIRTY_COUNT" -gt 0 ] 2>/dev/null; then
  GIT_STATUS="${DIRTY_COUNT} uncommitted"
fi

# Get changed files (max 10)
CHANGED_FILES=$(git status --porcelain 2>/dev/null | head -10 | sed 's/^...//') || true

# Get recent commits (last 3)
RECENT_COMMITS=$(git log --oneline -3 --no-decorate 2>/dev/null) || true

# ── Append rich session end marker ────────────────────────
if [ -f "$SESSION_FILE" ]; then
  {
    echo ""
    echo "### $TIMESTAMP — Session ended (auto-saved by AWF hook)"
    echo "- **Branch**: $BRANCH"
    echo "- **Git**: $GIT_STATUS"
    if [ -n "$CHANGED_FILES" ]; then
      echo "- **Files changed**:"
      echo "$CHANGED_FILES" | while IFS= read -r f; do
        [ -n "$f" ] && echo "  - $f"
      done
    fi
    if [ -n "$RECENT_COMMITS" ]; then
      echo "- **Recent commits**:"
      echo "$RECENT_COMMITS" | while IFS= read -r c; do
        [ -n "$c" ] && echo "  - $c"
      done
    fi
  } >> "$SESSION_FILE" 2>/dev/null || true
fi

# ── Update CONTEXT_SNAPSHOT.md with latest state ──────────
if [ -f "$SNAPSHOT_FILE" ]; then
  SNAPSHOT_SECTION="## Session State (auto-updated $TIMESTAMP)

### Git Status
- Branch: $BRANCH
- Status: $GIT_STATUS
"
  if [ -n "$CHANGED_FILES" ]; then
    SNAPSHOT_SECTION="${SNAPSHOT_SECTION}
### Modified Files
$(echo "$CHANGED_FILES" | while IFS= read -r f; do [ -n "$f" ] && echo "- $f"; done)
"
  fi
  if [ -n "$RECENT_COMMITS" ]; then
    SNAPSHOT_SECTION="${SNAPSHOT_SECTION}
### Recent Commits
$(echo "$RECENT_COMMITS" | while IFS= read -r c; do [ -n "$c" ] && echo "- $c"; done)
"
  fi

  # Append if no existing auto-section, otherwise replace
  if grep -q "## Session State (auto-updated" "$SNAPSHOT_FILE" 2>/dev/null; then
    # Use sed to replace the auto-updated section
    sed -i '/## Session State (auto-updated/,/^## [^S]/{ /^## [^S]/!d; }' "$SNAPSHOT_FILE" 2>/dev/null || true
    echo "$SNAPSHOT_SECTION" >> "$SNAPSHOT_FILE"
  else
    echo "" >> "$SNAPSHOT_FILE"
    echo "$SNAPSHOT_SECTION" >> "$SNAPSHOT_FILE"
  fi
fi

# ── Trigger auto-cleanup via HSA MCP if available ─────────
if [ -n "${HSA_MCP_PORT:-}" ]; then
  curl -s -X POST "http://127.0.0.1:$HSA_MCP_PORT/cleanup" --max-time 3 > /dev/null 2>&1 || true
fi

# ── Output JSON ────────────────────────────────────────────
FILE_COUNT=$(echo "$CHANGED_FILES" | grep -c . 2>/dev/null || echo "0")
jq -n \
  --arg branch "$BRANCH" \
  --arg git "$GIT_STATUS" \
  --arg ts "$TIMESTAMP" \
  --arg files "$FILE_COUNT" \
  '{hookSpecificOutput:{hookEventName:"Stop",additionalContext:("AWF session auto-saved at " + $ts + ". Branch: " + $branch + ", Git: " + $git + ", Files: " + $files)}}'

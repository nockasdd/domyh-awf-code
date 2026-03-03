#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF SessionStart Hook: Project Context Injection
# v2.0: Fixed JSON escaping for commit messages with quotes
# ═══════════════════════════════════════════════════════════════

# Read stdin (SessionStart may or may not send input)
cat > /dev/null 2>&1 || true

# Read project info
PROJECT_INFO="Unknown project"
if [ -f "package.json" ]; then
  NAME=$(jq -r '.name // "unknown"' package.json 2>/dev/null || echo "unknown")
  VERSION=$(jq -r '.version // "unknown"' package.json 2>/dev/null || echo "unknown")
  PROJECT_INFO="${NAME} v${VERSION}"
fi

# Git info (with quote escaping)
BRANCH=$(git branch --show-current 2>/dev/null || echo "unknown")
LAST_COMMIT=$(git log -1 --format="%s" 2>/dev/null || echo "N/A")
# Escape quotes for JSON safety
LAST_COMMIT=$(echo "$LAST_COMMIT" | sed 's/"/\\"/g; s/\\/\\\\/g' 2>/dev/null)

# Runtime version
NODE_VER=$(node -v 2>/dev/null || echo "not installed")

# AWF version
AWF_VER="unknown"
if [ -f ".agent/memory/state.json" ]; then
  AWF_VER=$(jq -r '.awfVersion // "unknown"' .agent/memory/state.json 2>/dev/null || echo "unknown")
fi

# Git status summary
DIRTY_COUNT=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ' || echo "0")
GIT_STATUS="clean"
if [ "$DIRTY_COUNT" -gt 0 ]; then
  GIT_STATUS="${DIRTY_COUNT} modified"
fi

# Output JSON-safe context
jq -n \
  --arg project "$PROJECT_INFO" \
  --arg branch "$BRANCH" \
  --arg commit "$LAST_COMMIT" \
  --arg node "$NODE_VER" \
  --arg awf "$AWF_VER" \
  --arg git "$GIT_STATUS" \
  '{hookSpecificOutput:{hookEventName:"SessionStart",additionalContext:("AWF Session | Project: " + $project + " | Branch: " + $branch + " | Last: " + $commit + " | Node: " + $node + " | AWF: " + $awf + " | Git: " + $git)}}'

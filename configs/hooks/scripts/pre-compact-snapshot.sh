#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF PreCompact Hook: Save Context Snapshot Before Compaction
# Fires before Claude Code truncates conversation context
# Creates a backup of CONTEXT_SNAPSHOT.md so no data is lost
#
# Compatible with: Claude Code, Cursor
#
# v1.0: Initial implementation — backup snapshot + session marker
# ═══════════════════════════════════════════════════════════════

set -uo pipefail

# Drain stdin
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

SNAPSHOT="$MEMORY_DIR/CONTEXT_SNAPSHOT.md"
SESSION="$MEMORY_DIR/session.md"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date +"%Y-%m-%dT%H:%M:%SZ")

# ── Backup snapshot ────────────────────────────────────────
BACKED_UP=false
if [ -f "$SNAPSHOT" ]; then
  cp "$SNAPSHOT" "$SNAPSHOT.pre-compact.bak" 2>/dev/null && BACKED_UP=true
fi

# ── Mark session ───────────────────────────────────────────
if [ -f "$SESSION" ]; then
  {
    echo ""
    echo "### $TIMESTAMP — PreCompact triggered (context snapshot backed up)"
  } >> "$SESSION" 2>/dev/null || true
fi

# ── Output JSON ────────────────────────────────────────────
if [ "$BACKED_UP" = true ]; then
  jq -n \
    --arg ts "$TIMESTAMP" \
    '{hookSpecificOutput:{hookEventName:"PreCompact",additionalContext:("Context snapshot backed up at " + $ts + ". Restore from CONTEXT_SNAPSHOT.md.pre-compact.bak if needed.")}}'
else
  echo '{"hookSpecificOutput":{"hookEventName":"PreCompact","additionalContext":"No snapshot to backup — AWF memory not initialized."}}'
fi

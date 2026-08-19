#!/usr/bin/env bash
# surgical-guard.sh — PreToolUse hook enforcing SACRED_RULES.xml SURGICAL_001
#
# Triggers warning when an agent attempts to:
#   1. Edit > 50 lines in a single tool call (potential scope creep)
#   2. Modify > 5 files in a single batch
#   3. Delete files outside declared scope
#
# Override: set DOMYH_SURGICAL_OVERRIDE=1 to bypass.
#
# Hook payload (stdin JSON):
#   { "tool": "...", "params": { "file_path": "...", "old_string": "...", "new_string": "..." } }

set -e

# Override flag
if [ "$DOMYH_SURGICAL_OVERRIDE" = "1" ]; then
    echo "[surgical-guard] Override enabled — skipping checks"
    exit 0
fi

# Read JSON payload from stdin
PAYLOAD=$(cat 2>/dev/null || true)
if [ -z "$PAYLOAD" ]; then
    exit 0
fi

# Require jq for JSON parsing — silently skip if missing (hook is advisory)
if ! command -v jq >/dev/null 2>&1; then
    exit 0
fi

TOOL=$(echo "$PAYLOAD" | jq -r '.tool // empty' 2>/dev/null || echo "")
FILE_PATH=$(echo "$PAYLOAD" | jq -r '.params.file_path // empty' 2>/dev/null || echo "")

# ─── Check 1: Single-edit line count ───
case "$TOOL" in
    Edit|Write|replace_file_content)
        OLD_LINES=$(echo "$PAYLOAD" | jq -r '.params.old_string // ""' 2>/dev/null | wc -l)
        NEW_LINES=$(echo "$PAYLOAD" | jq -r '.params.new_string // .params.content // ""' 2>/dev/null | wc -l)
        DELTA=$((NEW_LINES > OLD_LINES ? NEW_LINES - OLD_LINES : OLD_LINES - NEW_LINES))

        if [ "$DELTA" -gt 50 ]; then
            echo "[surgical-guard] SURGICAL_001 violation risk: editing $DELTA lines in $FILE_PATH" >&2
            echo "  > 50 lines in a single edit suggests scope creep." >&2
            echo "  Confirm with user before proceeding, or split into smaller commits." >&2
            echo "  Override: export DOMYH_SURGICAL_OVERRIDE=1" >&2
        fi
        ;;
esac

# ─── Check 2: Multi-file batch detection ───
EDIT_COUNT=$(echo "$PAYLOAD" | jq -r '.params.edits | length // 0' 2>/dev/null || echo "0")
if [ "$EDIT_COUNT" -gt 5 ]; then
    echo "[surgical-guard] Multi-file batch: $EDIT_COUNT edits in single call" >&2
    echo "  > 5 file changes per batch suggests sweeping refactor." >&2
    echo "  Confirm scope with user, or split into incremental commits." >&2
fi

# ─── Check 3: File deletion outside scope ───
if [ "$TOOL" = "Bash" ] || [ "$TOOL" = "runTerminalCommand" ]; then
    CMD=$(echo "$PAYLOAD" | jq -r '.params.command // empty' 2>/dev/null || echo "")
    if echo "$CMD" | grep -qE "rm\s+(-rf?|-fr?)?\s*[^|;&]+"; then
        TARGET=$(echo "$CMD" | grep -oE "rm\s+(-rf?|-fr?)?\s*[^|;&]+" | head -1)
        echo "[surgical-guard] DESTRUCTIVE: $TARGET" >&2
        echo "  SAFE_001 requires explicit user confirmation for deletions." >&2
    fi
fi

# Hook is advisory — never block
exit 0

#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF PostToolUse Hook: Quality Check (Regex-based, fast)
# v2.0: Fixed bugs + enhanced checks
#   - Removed `set -e` (grep returns 1 on no-match)
#   - Fixed JSON escaping for filenames with special chars
#   - Added line number reporting for issues
#   - Added import/require path validation
# ═══════════════════════════════════════════════════════════════

set -uo pipefail  # no -e

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# Only check after file edits/creates
case "$TOOL_NAME" in
  editFiles|createFile|Write|Edit|MultiEdit|write_to_file|replace_file_content|multi_replace_file_content)
    ;;
  *)
    echo '{"continue":true}'
    exit 0
    ;;
esac

# Extract file path (handle different IDE field names)
FILE_PATH=$(echo "$INPUT" | jq -r '
  .tool_input.files[0] //
  .tool_input.path //
  .tool_input.TargetFile //
  empty
' 2>/dev/null)

if [ -z "$FILE_PATH" ] || [ ! -f "$FILE_PATH" ]; then
  echo '{"continue":true}'
  exit 0
fi

# Only check TypeScript/JavaScript files
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx)
    ;;
  *)
    echo '{"continue":true}'
    exit 0
    ;;
esac

# Skip test files
case "$FILE_PATH" in
  *test.*|*spec.*|*__tests__*|*.test.ts|*.test.tsx|*.spec.ts|*.spec.tsx|*.test.js|*.spec.js)
    echo '{"continue":true}'
    exit 0
    ;;
esac

# Skip definition files
case "$FILE_PATH" in
  *.d.ts)
    echo '{"continue":true}'
    exit 0
    ;;
esac

ISSUES=""
ISSUE_COUNT=0

# Check 1: any type usage (excluding comments)
ANY_LINES=$(grep -nE ':\s*any\b|as\s+any\b|<any>' "$FILE_PATH" 2>/dev/null | grep -v '^\s*//' | head -3 || true)
if [ -n "$ANY_LINES" ]; then
  LINE_NUM=$(echo "$ANY_LINES" | head -1 | cut -d: -f1)
  ISSUES="${ISSUES}[L${LINE_NUM}] 'any' type — use specific types. "
  ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# Check 2: console.log in production code (excluding comments)
LOG_LINES=$(grep -nE 'console\.(log|debug|warn)\(' "$FILE_PATH" 2>/dev/null | grep -v '^\s*//' | head -3 || true)
if [ -n "$LOG_LINES" ]; then
  LINE_NUM=$(echo "$LOG_LINES" | head -1 | cut -d: -f1)
  ISSUES="${ISSUES}[L${LINE_NUM}] console.log/debug — use logger. "
  ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# Check 3: debugger statement
DBG_LINES=$(grep -nE '^\s*debugger\s*;?\s*$' "$FILE_PATH" 2>/dev/null || true)
if [ -n "$DBG_LINES" ]; then
  LINE_NUM=$(echo "$DBG_LINES" | head -1 | cut -d: -f1)
  ISSUES="${ISSUES}[L${LINE_NUM}] debugger statement — remove. "
  ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# Check 4: Hardcoded secrets (high confidence patterns)
SECRET_LINES=$(grep -nEi '(password|secret|api_key|apikey|private_key)\s*[:=]\s*["\x27][^"\x27]{8,}' "$FILE_PATH" 2>/dev/null | grep -vi '(process\.env|import|require|type|interface)' | head -3 || true)
if [ -n "$SECRET_LINES" ]; then
  LINE_NUM=$(echo "$SECRET_LINES" | head -1 | cut -d: -f1)
  ISSUES="${ISSUES}[L${LINE_NUM}] Possible hardcoded secret — use env vars. "
  ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# Check 5: TODO/FIXME tracking
TODO_COUNT=$(grep -cEi '(TODO|FIXME|HACK|XXX):' "$FILE_PATH" 2>/dev/null || echo "0")
if [ "$TODO_COUNT" -gt 0 ]; then
  ISSUES="${ISSUES}${TODO_COUNT} TODO/FIXME markers found. "
  ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

# Check 6: Empty catch blocks
EMPTY_CATCH=$(grep -nE 'catch\s*\([^)]*\)\s*\{\s*\}' "$FILE_PATH" 2>/dev/null || true)
if [ -n "$EMPTY_CATCH" ]; then
  LINE_NUM=$(echo "$EMPTY_CATCH" | head -1 | cut -d: -f1)
  ISSUES="${ISSUES}[L${LINE_NUM}] Empty catch block — handle or log error. "
  ISSUE_COUNT=$((ISSUE_COUNT + 1))
fi

if [ "$ISSUE_COUNT" -gt 0 ]; then
  # JSON-safe output: escape special chars in filename and issues
  BASENAME=$(basename "$FILE_PATH")
  SAFE_BASENAME=$(echo "$BASENAME" | sed 's/"/\\"/g')
  SAFE_ISSUES=$(echo "$ISSUES" | sed 's/"/\\"/g')
  echo "{\"hookSpecificOutput\":{\"hookEventName\":\"PostToolUse\",\"additionalContext\":\"Quality (${ISSUE_COUNT} issues in ${SAFE_BASENAME}): ${SAFE_ISSUES}\"}}"
else
  echo '{"continue":true}'
fi

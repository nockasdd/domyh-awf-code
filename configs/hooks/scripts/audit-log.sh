#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF PreToolUse Hook: Audit Trail Logger
# Logs all tool invocations for security/compliance audit
# ═══════════════════════════════════════════════════════════════

set -euo pipefail

INPUT=$(cat)
TIMESTAMP=$(echo "$INPUT" | jq -r '.timestamp // empty')
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // "unknown"')
SESSION_ID=$(echo "$INPUT" | jq -r '.sessionId // "unknown"')

# Use env var or default log path
LOG_FILE="${AUDIT_LOG:-.github/hooks/audit.log}"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")" 2>/dev/null || true

# Append to log
echo "[${TIMESTAMP:-$(date -Iseconds)}] Session: ${SESSION_ID} | Tool: ${TOOL_NAME}" >> "$LOG_FILE" 2>/dev/null || true

echo '{"continue":true}'

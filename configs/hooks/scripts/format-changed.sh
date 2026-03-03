#!/bin/bash
# ═══════════════════════════════════════════════════════════════
# AWF PostToolUse Hook: Auto-Format Changed Files
# v2.0: Fixed operator precedence, added deno fmt support
# ═══════════════════════════════════════════════════════════════

set -uo pipefail  # no -e

INPUT=$(cat)
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty' 2>/dev/null)

# Only format after file edits/creates
case "$TOOL_NAME" in
  editFiles|createFile|Write|Edit|MultiEdit|write_to_file|replace_file_content|multi_replace_file_content)
    ;;
  *)
    echo '{"continue":true}'
    exit 0
    ;;
esac

# Extract file path
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

# Only format code files
case "$FILE_PATH" in
  *.ts|*.tsx|*.js|*.jsx|*.json|*.css|*.scss|*.html|*.md|*.yaml|*.yml)
    ;;
  *)
    echo '{"continue":true}'
    exit 0
    ;;
esac

# Detect and run formatter (priority order)
FORMATTED=false

# 1. Prettier (most common)
if [ "$FORMATTED" = false ] && command -v npx &>/dev/null; then
  if [ -f "node_modules/.bin/prettier" ] || [ -f ".prettierrc" ] || [ -f ".prettierrc.json" ] || [ -f "prettier.config.js" ] || [ -f "prettier.config.mjs" ]; then
    npx prettier --write "$FILE_PATH" 2>/dev/null && FORMATTED=true
  fi
fi

# 2. Biome
if [ "$FORMATTED" = false ] && command -v npx &>/dev/null; then
  if [ -f "biome.json" ] || [ -f "biome.jsonc" ]; then
    npx biome format --write "$FILE_PATH" 2>/dev/null && FORMATTED=true
  fi
fi

# 3. Deno fmt
if [ "$FORMATTED" = false ] && command -v deno &>/dev/null; then
  if [ -f "deno.json" ] || [ -f "deno.jsonc" ]; then
    deno fmt "$FILE_PATH" 2>/dev/null && FORMATTED=true
  fi
fi

echo '{"continue":true}'

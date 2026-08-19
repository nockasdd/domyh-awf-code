#!/usr/bin/env pwsh
# surgical-guard.ps1 — PreToolUse hook enforcing SACRED_RULES.xml SURGICAL_001
#
# Triggers warning when an agent attempts to:
#   1. Edit > 50 lines in a single tool call (potential scope creep)
#   2. Modify > 5 files in a single batch (sweeping refactor without confirmation)
#   3. Delete files outside declared scope
#
# Override: set DOMYH_SURGICAL_OVERRIDE=1 to bypass (for legitimate large refactors).
#
# Hook payload (stdin JSON):
#   { "tool": "...", "params": { "file_path": "...", "old_string": "...", "new_string": "..." } }

param()

$ErrorActionPreference = "Stop"

# Read JSON payload from stdin
$payload = $null
try {
    $stdin = [Console]::In.ReadToEnd()
    if ($stdin) { $payload = $stdin | ConvertFrom-Json }
} catch {
    # No payload or invalid JSON — exit silently (hook is advisory)
    exit 0
}

if (-not $payload) { exit 0 }

# Override flag
if ($env:DOMYH_SURGICAL_OVERRIDE -eq "1") {
    Write-Output "[surgical-guard] Override enabled — skipping checks"
    exit 0
}

$tool = $payload.tool
$params = $payload.params

# ─── Check 1: Single-edit line count ───
if ($tool -in @("Edit", "Write", "replace_file_content")) {
    $oldStr = if ($params.old_string) { $params.old_string } else { "" }
    $newStr = if ($params.new_string) { $params.new_string } else { $params.content }
    $oldLines = if ($oldStr) { ($oldStr -split "`n").Count } else { 0 }
    $newLines = if ($newStr) { ($newStr -split "`n").Count } else { 0 }
    $delta = [Math]::Abs($newLines - $oldLines)

    if ($delta -gt 50) {
        Write-Warning "[surgical-guard] SURGICAL_001 violation risk: editing $delta lines in $($params.file_path)"
        Write-Warning "  > 50 lines in a single edit suggests scope creep."
        Write-Warning "  Confirm with user before proceeding, or split into smaller commits."
        Write-Warning "  Override: set DOMYH_SURGICAL_OVERRIDE=1"
    }

    # Check 1b: detect quote/whitespace-only changes (style imposition anti-pattern SC-002)
    if ($oldStr -and $newStr) {
        $normalizedOld = $oldStr -replace '\s+', '' -replace '"', "'" -replace '`', "'"
        $normalizedNew = $newStr -replace '\s+', '' -replace '"', "'" -replace '`', "'"
        if ($normalizedOld -eq $normalizedNew -and $oldStr -ne $newStr) {
            Write-Warning "[surgical-guard] SC-002 detected: style-only change (quotes/whitespace) in $($params.file_path)"
            Write-Warning "  Style changes should NEVER be standalone. Match existing style EXACTLY."
        }
    }
}

# ─── Check 2: Multi-file batch detection ───
# (Hook fires per-call, so we check params.edits[] for MultiEdit-style tools)
if ($params.edits -and $params.edits.Count -gt 5) {
    Write-Warning "[surgical-guard] Multi-file batch: $($params.edits.Count) edits in single call"
    Write-Warning "  > 5 file changes per batch suggests sweeping refactor."
    Write-Warning "  Confirm scope with user, or split into incremental commits."
}

# ─── Check 3: File deletion outside scope ───
if ($tool -in @("Bash", "runTerminalCommand")) {
    $cmd = if ($params.command) { $params.command } else { "" }
    if ($cmd -match "rm\s+(-rf?\s+|-fr?\s+)?[^\s|;&]+") {
        $target = $matches[0] -replace "rm\s+(-rf?\s+|-fr?\s+)?", ""
        Write-Warning "[surgical-guard] DESTRUCTIVE: rm command targets '$target'"
        Write-Warning "  SAFE_001 requires explicit user confirmation for deletions."
    }
}

# Hook is advisory — never block (exit 0)
exit 0

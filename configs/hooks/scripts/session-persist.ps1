# ═══════════════════════════════════════════════════════════════
# AWF Stop Hook: Auto-Persist Session Context (PowerShell)
# Fires when agent completes or user stops — saves session data
# Compatible with: Claude Code, Cursor, VS Code Copilot (Windows)
#
# v1.0: Initial implementation — session end marker + git status
# ═══════════════════════════════════════════════════════════════

$ErrorActionPreference = "SilentlyContinue"

# Drain stdin
try { [Console]::In.ReadToEnd() | Out-Null } catch {}

# ── Check AWF installation ─────────────────────────────────
$memoryDir = $null
foreach ($candidate in @(".agent\memory", ".claude\memory", ".cursor\memory")) {
    if (Test-Path $candidate) {
        $memoryDir = $candidate
        break
    }
}

if (-not $memoryDir) {
    Write-Output '{"continue":true}'
    exit 0
}

$sessionFile = Join-Path $memoryDir "session.md"
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# ── Append session end marker ──────────────────────────────
if (Test-Path $sessionFile) {
    Add-Content $sessionFile "`n### $timestamp — Session ended (auto-saved by AWF hook)" -ErrorAction SilentlyContinue
}

# ── Gather git status for context ──────────────────────────
$branch = git branch --show-current 2>$null
if (-not $branch) { $branch = "unknown" }

$dirtyCount = 0
$gitStatus = "clean"
try {
    $porcelain = git status --porcelain 2>$null
    if ($porcelain) {
        $dirtyCount = ($porcelain -split "`n").Count
        $gitStatus = "$dirtyCount uncommitted"
    }
} catch {}

# ── Output JSON ────────────────────────────────────────────
$output = @{
    hookSpecificOutput = @{
        hookEventName = "Stop"
        additionalContext = "AWF session auto-saved at $timestamp. Branch: $branch, Git: $gitStatus"
    }
} | ConvertTo-Json -Depth 3 -Compress
Write-Output $output

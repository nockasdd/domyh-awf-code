# ═══════════════════════════════════════════════════════════════
# AWF Stop Hook: Auto-Persist Session Context (PowerShell)
# Fires when agent completes or user stops — saves session data
# Compatible with: Claude Code, Cursor, VS Code Copilot (Windows)
#
# v2.0: Rich context — git diff summary, recent files, structured snapshot
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
$snapshotFile = Join-Path $memoryDir "CONTEXT_SNAPSHOT.md"
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# ── Gather git context ────────────────────────────────────
$branch = git branch --show-current 2>$null
if (-not $branch) { $branch = "unknown" }

$dirtyCount = 0
$gitStatus = "clean"
$changedFiles = @()
try {
    $porcelain = git status --porcelain 2>$null
    if ($porcelain) {
        $lines = $porcelain -split "`n" | Where-Object { $_ -match '\S' }
        $dirtyCount = $lines.Count
        $gitStatus = "$dirtyCount uncommitted"
        $changedFiles = $lines | ForEach-Object { ($_ -replace '^\s*\S+\s+', '').Trim() } | Select-Object -First 10
    }
} catch {}

# ── Gather recent commits (last 3) ───────────────────────
$recentCommits = @()
try {
    $logOutput = git log --oneline -3 --no-decorate 2>$null
    if ($logOutput) {
        $recentCommits = $logOutput -split "`n" | Where-Object { $_ -match '\S' } | Select-Object -First 3
    }
} catch {}

# ── Append rich session end marker ────────────────────────
if (Test-Path $sessionFile) {
    $entry = @"

### $timestamp — Session ended (auto-saved by AWF hook)
- **Branch**: $branch
- **Git**: $gitStatus
"@
    if ($changedFiles.Count -gt 0) {
        $fileList = ($changedFiles | ForEach-Object { "  - $_" }) -join "`n"
        $entry += "`n- **Files changed**:`n$fileList"
    }
    if ($recentCommits.Count -gt 0) {
        $commitList = ($recentCommits | ForEach-Object { "  - $_" }) -join "`n"
        $entry += "`n- **Recent commits**:`n$commitList"
    }
    Add-Content $sessionFile $entry -ErrorAction SilentlyContinue
}

# ── Update CONTEXT_SNAPSHOT.md with latest state ──────────
if (Test-Path $snapshotFile) {
    $snapshotContent = @"
## Session State (auto-updated $timestamp)

### Git Status
- Branch: $branch
- Status: $gitStatus

"@
    if ($changedFiles.Count -gt 0) {
        $snapshotContent += "### Modified Files`n"
        foreach ($f in $changedFiles) {
            $snapshotContent += "- $f`n"
        }
        $snapshotContent += "`n"
    }
    if ($recentCommits.Count -gt 0) {
        $snapshotContent += "### Recent Commits`n"
        foreach ($c in $recentCommits) {
            $snapshotContent += "- $c`n"
        }
    }

    # Read existing snapshot, preserve user sections, update auto section
    $existing = Get-Content $snapshotFile -Raw -ErrorAction SilentlyContinue
    if ($existing -match '(?s)## Session State \(auto-updated.*?\)(.+?)(?=## |\z)') {
        $updated = $existing -replace '(?s)## Session State \(auto-updated.*?\)(.+?)(?=## |\z)', $snapshotContent
        Set-Content $snapshotFile $updated -NoNewline -ErrorAction SilentlyContinue
    } else {
        Add-Content $snapshotFile "`n$snapshotContent" -ErrorAction SilentlyContinue
    }
}

# ── Trigger auto-cleanup via HSA MCP if available ─────────
# This calls the cleanup endpoint to prune expired entries
$hsaPort = $env:HSA_MCP_PORT
if ($hsaPort) {
    try {
        Invoke-RestMethod -Uri "http://127.0.0.1:$hsaPort/cleanup" -Method POST -TimeoutSec 3 2>$null | Out-Null
    } catch {}
}

# ── Output JSON ────────────────────────────────────────────
$output = @{
    hookSpecificOutput = @{
        hookEventName = "Stop"
        additionalContext = "AWF session auto-saved at $timestamp. Branch: $branch, Git: $gitStatus, Files: $($changedFiles.Count)"
    }
} | ConvertTo-Json -Depth 3 -Compress
Write-Output $output

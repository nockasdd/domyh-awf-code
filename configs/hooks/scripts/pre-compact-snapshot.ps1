# ═══════════════════════════════════════════════════════════════
# AWF PreCompact Hook: Save Context Snapshot Before Compaction
# PowerShell version (Windows)
#
# v1.0: Initial implementation — backup snapshot + session marker
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

$snapshot = Join-Path $memoryDir "CONTEXT_SNAPSHOT.md"
$sessionFile = Join-Path $memoryDir "session.md"
$timestamp = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")

# ── Backup snapshot ────────────────────────────────────────
$backedUp = $false
if (Test-Path $snapshot) {
    Copy-Item $snapshot "$snapshot.pre-compact.bak" -Force -ErrorAction SilentlyContinue
    $backedUp = $true
}

# ── Mark session ───────────────────────────────────────────
if (Test-Path $sessionFile) {
    Add-Content $sessionFile "`n### $timestamp — PreCompact triggered (context snapshot backed up)" -ErrorAction SilentlyContinue
}

# ── Output JSON ────────────────────────────────────────────
if ($backedUp) {
    $output = @{
        hookSpecificOutput = @{
            hookEventName = "PreCompact"
            additionalContext = "Context snapshot backed up at $timestamp. Restore from CONTEXT_SNAPSHOT.md.pre-compact.bak if needed."
        }
    } | ConvertTo-Json -Depth 3 -Compress
    Write-Output $output
} else {
    Write-Output '{"hookSpecificOutput":{"hookEventName":"PreCompact","additionalContext":"No snapshot to backup — AWF memory not initialized."}}'
}

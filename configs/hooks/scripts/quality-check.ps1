# ═══════════════════════════════════════════════════════════════
# AWF PostToolUse Hook: Quality Check (PowerShell)
# v2.0: 6 checks, line numbers, JSON escaping, .d.ts exclusion
# ═══════════════════════════════════════════════════════════════

$ErrorActionPreference = "SilentlyContinue"

$rawInput = [Console]::In.ReadToEnd()
$hookInput = $rawInput | ConvertFrom-Json

$editTools = @("editFiles", "createFile", "Write", "Edit", "MultiEdit", "write_to_file", "replace_file_content", "multi_replace_file_content")
if ($hookInput.tool_name -notin $editTools) {
    Write-Output '{"continue":true}'
    exit 0
}

$filePath = $hookInput.tool_input.files[0]
if (-not $filePath) { $filePath = $hookInput.tool_input.path }
if (-not $filePath) { $filePath = $hookInput.tool_input.TargetFile }
if (-not $filePath -or -not (Test-Path $filePath)) {
    Write-Output '{"continue":true}'
    exit 0
}

$ext = [System.IO.Path]::GetExtension($filePath)
if ($ext -notin @(".ts", ".tsx", ".js", ".jsx")) {
    Write-Output '{"continue":true}'
    exit 0
}

$fileName = [System.IO.Path]::GetFileName($filePath)
# Skip test & definition files
if ($fileName -match '\.(test|spec)\.' -or $filePath -match '__tests__' -or $ext -eq ".d.ts") {
    Write-Output '{"continue":true}'
    exit 0
}

$content = Get-Content $filePath -Raw -ErrorAction SilentlyContinue
if (-not $content) {
    Write-Output '{"continue":true}'
    exit 0
}

$lines = Get-Content $filePath -ErrorAction SilentlyContinue
$issues = @()

# Check 1: any type (with line number)
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match ':\s*any\b|as\s+any\b|<any>' -and $lines[$i] -notmatch '^\s*//') {
        $ln = $i + 1
        $issues += "[L$ln] any type - use specific types"
        break
    }
}

# Check 2: console.log (with line number)
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match 'console\.(log|debug)\(' -and $lines[$i] -notmatch '^\s*//') {
        $ln = $i + 1
        $issues += "[L$ln] console.log/debug - use logger"
        break
    }
}

# Check 3: debugger
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -match '^\s*debugger\s*;?\s*$') {
        $ln = $i + 1
        $issues += "[L$ln] debugger statement - remove"
        break
    }
}

# Check 4: Hardcoded secrets
if ($content -match '(?i)(password|secret|api_key|apikey|private_key)\s*[:=]\s*[''"][^''\"]{8,}') {
    $issues += "Possible hardcoded secret - use env vars"
}

# Check 5: TODO/FIXME
$todoMatches = [regex]::Matches($content, '(?i)(TODO|FIXME|HACK|XXX):')
if ($todoMatches.Count -gt 0) {
    $issues += "$($todoMatches.Count) TODO/FIXME markers"
}

# Check 6: Empty catch blocks
if ($content -match 'catch\s*\([^)]*\)\s*\{\s*\}') {
    $issues += "Empty catch block - handle or log error"
}

if ($issues.Count -gt 0) {
    $basename = [System.IO.Path]::GetFileName($filePath)
    $ctx = "Quality ($($issues.Count) issues in $basename): " + ($issues -join ". ")
    # JSON-safe escaping
    $ctx = $ctx -replace '\\', '\\\\' -replace '"', '\"'
    $output = @{
        hookSpecificOutput = @{
            hookEventName = "PostToolUse"
            additionalContext = $ctx
        }
    } | ConvertTo-Json -Depth 3 -Compress
    Write-Output $output
} else {
    Write-Output '{"continue":true}'
}

# ═══════════════════════════════════════════════════════════════
# AWF PreToolUse Hook: File-Path Guard (PowerShell)
# Blocks modification of protected files (.env, .git, locks, SSH)
#
# v1.1: Dynamic config resolution — multi-path fallback
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
if (-not $filePath) { $filePath = $hookInput.tool_input.file_path }
if (-not $filePath) {
    Write-Output '{"continue":true}'
    exit 0
}

# ── Dynamic Config Resolution ─────────────────────────────
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Find-HookConfig {
    param([string]$Name)
    $envPath = $env:AWF_HOOKS_CONFIG
    if ($envPath -and (Test-Path (Join-Path $envPath $Name))) {
        return Join-Path $envPath $Name
    }
    $relative = Join-Path (Split-Path -Parent $scriptDir) "config" $Name
    if (Test-Path $relative) { return $relative }
    $flat = Join-Path $scriptDir "config" $Name
    if (Test-Path $flat) { return $flat }
    foreach ($prefix in @(".github\hooks", ".claude\hooks", ".agent\hooks")) {
        $projPath = Join-Path $prefix "config" $Name
        if (Test-Path $projPath) { return $projPath }
    }
    $home = if ($env:USERPROFILE) { $env:USERPROFILE } else { $env:HOME }
    if ($home) {
        $globalPath = Join-Path $home ".gemini" "antigravity" "hooks" "config" $Name
        if (Test-Path $globalPath) { return $globalPath }
    }
    return $null
}

$configPath = Find-HookConfig "protected-paths.json"
if (-not $configPath) {
    Write-Output '{"continue":true}'
    exit 0
}

try {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

foreach ($rule in $config.protected_paths) {
    if ($filePath -match $rule.pattern) {
        $output = @{
            hookSpecificOutput = @{
                hookEventName = "PreToolUse"
                permissionDecision = $rule.action
                permissionDecisionReason = "[AWF Path Guard] $($rule.reason)"
            }
        } | ConvertTo-Json -Depth 3 -Compress
        Write-Output $output
        exit 0
    }
}

Write-Output '{"continue":true}'

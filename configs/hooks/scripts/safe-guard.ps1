# ═══════════════════════════════════════════════════════════════
# AWF PreToolUse Hook: Config-Driven Command Safety Guard
# PowerShell version — reads blocked-commands.json
# Compatible with: VS Code Copilot, Claude Code, Cursor (Windows)
#
# v3.1: Dynamic config resolution — multi-path fallback
# ═══════════════════════════════════════════════════════════════

$ErrorActionPreference = "SilentlyContinue"

$rawInput = [Console]::In.ReadToEnd()
$hookInput = $rawInput | ConvertFrom-Json

# Only check terminal/command tools
$toolName = $hookInput.tool_name
$commandTools = @("runTerminalCommand", "Bash", "execute", "run_command", "send_command_input")
if ($toolName -notin $commandTools) {
    Write-Output '{"continue":true}'
    exit 0
}

# Extract command
$command = $hookInput.tool_input.command
if (-not $command) { $command = $hookInput.tool_input.CommandLine }
if (-not $command) { $command = $hookInput.tool_input.Input }
if (-not $command) { $command = $hookInput.tool_input.cmd }
if (-not $command) {
    Write-Output '{"continue":true}'
    exit 0
}

# ── Dynamic Config Resolution ─────────────────────────────
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

function Find-HookConfig {
    param([string]$Name)
    # 1. Env var override
    $envPath = $env:AWF_HOOKS_CONFIG
    if ($envPath -and (Test-Path (Join-Path $envPath $Name))) {
        return Join-Path $envPath $Name
    }
    # 2. Relative (scripts/../config/)
    $relative = Join-Path (Split-Path -Parent $scriptDir) "config" $Name
    if (Test-Path $relative) { return $relative }
    # 3. Flat (scripts/config/)
    $flat = Join-Path $scriptDir "config" $Name
    if (Test-Path $flat) { return $flat }
    # 4-6. Project locations
    foreach ($prefix in @(".github\hooks", ".claude\hooks", ".agent\hooks")) {
        $projPath = Join-Path $prefix "config" $Name
        if (Test-Path $projPath) { return $projPath }
    }
    # 7. Global fallback
    $home = if ($env:USERPROFILE) { $env:USERPROFILE } else { $env:HOME }
    if ($home) {
        $globalPath = Join-Path $home ".gemini" "antigravity" "hooks" "config" $Name
        if (Test-Path $globalPath) { return $globalPath }
    }
    return $null
}

$configPath = Find-HookConfig "blocked-commands.json"
if (-not $configPath) {
    Write-Output '{"continue":true}'
    exit 0
}

try {
    $rules = Get-Content $configPath -Raw | ConvertFrom-Json
} catch {
    Write-Output '{"continue":true}'
    exit 0
}

foreach ($rule in $rules) {
    if ($command -match $rule.pattern) {
        $isSafe = $false
        foreach ($safePat in $rule.safe_patterns) {
            if ($safePat -and $command.Contains($safePat)) {
                $isSafe = $true
                break
            }
        }

        if (-not $isSafe) {
            $output = @{
                hookSpecificOutput = @{
                    hookEventName = "PreToolUse"
                    permissionDecision = $rule.action
                    permissionDecisionReason = "[AWF Safety] $($rule.reason)"
                }
            } | ConvertTo-Json -Depth 3 -Compress
            Write-Output $output
            exit 0
        }
    }
}

Write-Output '{"continue":true}'

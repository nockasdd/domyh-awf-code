# DOMYH AWF Safe Guard — PreToolUse Hook (PowerShell)
# Blocks dangerous commands before execution
#
# Input: JSON on stdin from Copilot
# Output: JSON with permissionDecision (allow/deny/ask)

$ErrorActionPreference = "SilentlyContinue"

try {
    $input_json = [Console]::In.ReadToEnd()
    $data = $input_json | ConvertFrom-Json
    $tool = $data.toolName
} catch {
    $tool = ""
}

# Only check execute tool (terminal commands)
if ($tool -eq "execute" -or $tool -eq "terminal") {
    try {
        $cmd = $data.input.command
    } catch {
        $cmd = ""
    }

    # Block destructive patterns
    $blockPatterns = @(
        'rm\s+-rf\s+/',
        'rm\s+-rf\s+~',
        'DROP\s+(TABLE|DATABASE)',
        'TRUNCATE\s+TABLE',
        'FORMAT\s+[A-Z]:',
        'Remove-Item\s+.*-Recurse.*[/\\]$'
    )

    foreach ($pattern in $blockPatterns) {
        if ($cmd -match $pattern) {
            Write-Output '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"Blocked by DOMYH safety hook: destructive command detected"}}'
            exit 0
        }
    }

    # Ask confirmation for potentially risky operations
    $askPatterns = @(
        'rm\s+-rf',
        'git\s+push\s+--force',
        'git\s+reset\s+--hard',
        'npm\s+publish',
        'docker\s+system\s+prune',
        'Remove-Item.*-Recurse'
    )

    foreach ($pattern in $askPatterns) {
        if ($cmd -match $pattern) {
            Write-Output '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"DOMYH safety: potentially destructive command requires confirmation"}}'
            exit 0
        }
    }
}

# Allow by default
Write-Output '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"allow"}}'

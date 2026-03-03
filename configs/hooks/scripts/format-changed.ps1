# ═══════════════════════════════════════════════════════════════
# AWF PostToolUse Hook: Auto-Format Changed Files (PowerShell)
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
$codeExts = @(".ts", ".tsx", ".js", ".jsx", ".json", ".css", ".scss", ".html", ".md", ".yaml", ".yml")
if ($ext -notin $codeExts) {
    Write-Output '{"continue":true}'
    exit 0
}

# Detect formatter
if ((Test-Path "node_modules/.bin/prettier") -or (Test-Path ".prettierrc") -or (Test-Path "prettier.config.js")) {
    npx prettier --write $filePath 2>$null
} elseif ((Test-Path "biome.json") -or (Test-Path "biome.jsonc")) {
    npx biome format --write $filePath 2>$null
}

Write-Output '{"continue":true}'

# ============================================================================
# DOMYH Agent Library - Smart Installer for Windows
# Version: 2.0.0
# Developer: NockDev (https://github.com/nockasdd)
# PowerShell Script
# ============================================================================

param(
    [switch]$Help,
    [switch]$All,
    [switch]$Project,
    [string]$ProjectPath,
    [string]$Lang
)

# Script location
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$DomyhRoot = Split-Path -Parent (Split-Path -Parent $ScriptDir)

# Default language
$Global:Language = "en"

# ============================================================================
# Internationalization (i18n)
# ============================================================================

$Strings = @{
    "en" = @{
        "banner_title"          = "DOMYH Agent Library"
        "banner_subtitle"       = "AI-Powered Development Assistant"
        "banner_by"             = "Developed by NockDev"
        "detecting_os"          = "Operating System"
        "detecting_ides"        = "Detecting installed AI IDEs..."
        "select_language"       = "Select Language"
        "menu_title"            = "Installation Options"
        "menu_all"              = "Install to ALL detected IDEs"
        "menu_select"           = "Select specific IDEs"
        "menu_project"          = "Install to current project only"
        "menu_details"          = "Show IDE configuration details"
        "menu_language"         = "Change Language"
        "menu_exit"             = "Exit"
        "choose_option"         = "Choose option"
        "installing_to"         = "Installing to"
        "installation_complete" = "Installation complete!"
        "project_path"          = "Enter project path (or press Enter for current directory)"
        "files_created"         = "Files created"
        "goodbye"               = "Goodbye!"
        "invalid_option"        = "Invalid option. Please try again."
        "no_ides_detected"      = "No AI IDEs detected. You can still install manually."
        "press_enter"           = "Press Enter to continue..."
        "configured"            = "configured!"
        "version"               = "Version"
        "language_selected"     = "Selected: English"
    }
    "vi" = @{
        "banner_title"          = "DOMYH Agent Library"
        "banner_subtitle"       = "Trợ lý Phát triển Ứng dụng AI"
        "banner_by"             = "Phát triển bởi NockDev"
        "detecting_os"          = "Hệ điều hành"
        "detecting_ides"        = "Đang phát hiện các AI IDE đã cài đặt..."
        "select_language"       = "Chọn Ngôn ngữ"
        "menu_title"            = "Tùy chọn Cài đặt"
        "menu_all"              = "Cài đặt cho TẤT CẢ IDE đã phát hiện"
        "menu_select"           = "Chọn IDE cụ thể"
        "menu_project"          = "Cài đặt cho project hiện tại"
        "menu_details"          = "Xem chi tiết cấu hình IDE"
        "menu_language"         = "Đổi Ngôn ngữ"
        "menu_exit"             = "Thoát"
        "choose_option"         = "Chọn tùy chọn"
        "installing_to"         = "Đang cài đặt cho"
        "installation_complete" = "Cài đặt hoàn tất!"
        "project_path"          = "Nhập đường dẫn project (hoặc Enter cho thư mục hiện tại)"
        "files_created"         = "Các file đã tạo"
        "goodbye"               = "Tạm biệt!"
        "invalid_option"        = "Tùy chọn không hợp lệ. Vui lòng thử lại."
        "no_ides_detected"      = "Không phát hiện AI IDE. Bạn vẫn có thể cài đặt thủ công."
        "press_enter"           = "Nhấn Enter để tiếp tục..."
        "configured"            = "đã cấu hình!"
        "version"               = "Phiên bản"
        "language_selected"     = "Đã chọn: Tiếng Việt"
    }
}

function Get-String {
    param([string]$Key)
    return $Strings[$Global:Language][$Key]
}

# ============================================================================
# IDE Configuration
# ============================================================================

$IDEConfigs = @{
    "claude"          = @{
        Name     = "Claude Code CLI"
        Path     = "$env:USERPROFILE\.claude"
        File     = "CLAUDE.md"
        Detected = $false
    }
    "cursor"          = @{
        Name     = "Cursor IDE"
        Path     = "$env:USERPROFILE\.cursor"
        AppData  = "$env:APPDATA\Cursor"
        File     = ".cursorrules"
        Detected = $false
    }
    "windsurf"        = @{
        Name     = "Windsurf IDE"
        Path     = "$env:USERPROFILE\.windsurf"
        File     = "AGENTS.md"
        Detected = $false
    }
    "vscode"          = @{
        Name     = "VS Code (Copilot)"
        Path     = "$env:USERPROFILE\.vscode"
        AppData  = "$env:APPDATA\Code"
        File     = ".github\copilot-instructions.md"
        Detected = $false
    }
    "vscode-insiders" = @{
        Name     = "VS Code Insiders"
        Path     = "$env:USERPROFILE\.vscode-insiders"
        AppData  = "$env:APPDATA\Code - Insiders"
        File     = ".github\copilot-instructions.md"
        Detected = $false
    }
    "augment"         = @{
        Name     = "Augment Code"
        Path     = "$env:USERPROFILE\.augment"
        File     = "rules\"
        Detected = $false
    }
    "codex"           = @{
        Name     = "OpenAI Codex CLI"
        Path     = "$env:USERPROFILE\.codex"
        File     = "AGENTS.md"
        Detected = $false
    }
    "gemini"          = @{
        Name     = "Google Gemini CLI"
        Path     = "$env:USERPROFILE\.gemini"
        File     = "GEMINI.md"
        Detected = $false
    }
    "antigravity"     = @{
        Name     = "Antigravity (Claude)"
        Path     = "$env:USERPROFILE\.gemini\antigravity"
        File     = "global_workflows\"
        Detected = $false
    }
    "continue"        = @{
        Name     = "Continue.dev"
        Path     = "$env:USERPROFILE\.continue"
        File     = "AGENTS.md"
        Detected = $false
    }
}

# ============================================================================
# Functions
# ============================================================================

function Show-Banner {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
    Write-Host "║                    🚀 $(Get-String 'banner_title')                     ║" -ForegroundColor Cyan
    Write-Host "║              $(Get-String 'banner_subtitle')              ║" -ForegroundColor Cyan
    Write-Host "║                      $(Get-String 'version') 2.0.0                        ║" -ForegroundColor Cyan
    Write-Host "║                   $(Get-String 'banner_by')                   ║" -ForegroundColor Cyan
    Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
    Write-Host ""
}

function Select-Language {
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════════════╗" -ForegroundColor Magenta
    Write-Host "║                   🌍 Select Language / Chọn Ngôn ngữ             ║" -ForegroundColor Magenta
    Write-Host "╚══════════════════════════════════════════════════════════════════╝" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "  1) 🇺🇸 English (default)"
    Write-Host "  2) 🇻🇳 Tiếng Việt"
    Write-Host ""
    $choice = Read-Host "Choose / Chọn (1-2)"
    
    switch ($choice) {
        "2" { $Global:Language = "vi" }
        default { $Global:Language = "en" }
    }
    
    # Update config.yaml
    Update-LanguageConfig
    
    Write-Host ""
    Write-Host "✅ $(Get-String 'language_selected')" -ForegroundColor Green
}

function Update-LanguageConfig {
    $configFile = "$DomyhRoot\.agent\config.yaml"
    if (Test-Path $configFile) {
        $content = Get-Content $configFile -Raw
        if ($Global:Language -eq "vi") {
            $content = $content -replace 'default: "en"', 'default: "vi"'
        }
        else {
            $content = $content -replace 'default: "vi"', 'default: "en"'
        }
        $content | Set-Content $configFile -Encoding UTF8
    }
}

function Show-Help {
    Show-Banner
    Write-Host "Usage: .\install.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Yellow
    Write-Host "  -Help           Show this help message"
    Write-Host "  -All            Install to all detected IDEs"
    Write-Host "  -Project        Install to current project"
    Write-Host "  -ProjectPath    Specify project path"
    Write-Host "  -Lang           Set language (en, vi)"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Yellow
    Write-Host "  .\install.ps1                    # Interactive mode"
    Write-Host "  .\install.ps1 -All               # Install to all IDEs"
    Write-Host "  .\install.ps1 -Project           # Install to current dir"
    Write-Host "  .\install.ps1 -Lang vi -All      # Vietnamese, install all"
    Write-Host ""
}

function Detect-IDEs {
    Write-Host "🔍 $(Get-String 'detecting_ides')" -ForegroundColor Yellow
    Write-Host ""
    
    $detected = @()
    
    foreach ($key in $IDEConfigs.Keys) {
        $config = $IDEConfigs[$key]
        $found = $false
        
        if (Test-Path $config.Path) {
            $found = $true
        }
        elseif ($config.AppData -and (Test-Path $config.AppData)) {
            $found = $true
        }
        
        if ($found) {
            $IDEConfigs[$key].Detected = $true
            $detected += $key
            Write-Host "  ✅ $($config.Name)" -ForegroundColor Green -NoNewline
            Write-Host " — $($config.Path)" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    
    if ($detected.Count -eq 0) {
        Write-Host "❌ $(Get-String 'no_ides_detected')" -ForegroundColor Red
    }
    
    return $detected
}

function Show-Menu {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "📋 $(Get-String 'menu_title'):" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1) 🌍 $(Get-String 'menu_all')"
    Write-Host "  2) 🎯 $(Get-String 'menu_select')"
    Write-Host "  3) 📁 $(Get-String 'menu_project')"
    Write-Host "  4) 📖 $(Get-String 'menu_details')"
    Write-Host "  5) 🌐 $(Get-String 'menu_language')"
    Write-Host "  6) ❌ $(Get-String 'menu_exit')"
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    return Read-Host "$(Get-String 'choose_option') (1-6)"
}

function Install-ToIDE {
    param([string]$IDE)
    
    $config = $IDEConfigs[$IDE]
    $name = $config.Name
    $path = $config.Path
    
    Write-Host "📦 $(Get-String 'installing_to') $name..." -ForegroundColor Blue
    
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
    
    switch ($IDE) {
        "claude" {
            Copy-Item "$DomyhRoot\root\CLAUDE.md" -Destination "$path\CLAUDE.md" -Force
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$DomyhRoot\.agent\skills") {
                Copy-Item "$DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        "cursor" {
            $rulesPath = "$path\rules"
            if (-not (Test-Path $rulesPath)) {
                New-Item -ItemType Directory -Path $rulesPath -Force | Out-Null
            }
            Get-ChildItem "$DomyhRoot\.agent\rules\*.md" | ForEach-Object {
                $newName = $_.BaseName + ".mdc"
                Copy-Item $_.FullName -Destination "$rulesPath\$newName" -Force
            }
        }
        
        { "windsurf", "codex", "continue" -contains $_ } {
            Copy-Item "$DomyhRoot\root\AGENTS.md" -Destination "$path\AGENTS.md" -Force
        }
        
        "gemini" {
            Copy-Item "$DomyhRoot\root\GEMINI.md" -Destination "$path\GEMINI.md" -Force
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$DomyhRoot\.agent\skills") {
                Copy-Item "$DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        "augment" {
            $rulesPath = "$path\rules"
            if (-not (Test-Path $rulesPath)) {
                New-Item -ItemType Directory -Path $rulesPath -Force | Out-Null
            }
            Copy-Item "$DomyhRoot\.agent\rules\*.md" -Destination $rulesPath -Force
        }
        
        "antigravity" {
            $wfPath = "$path\global_workflows"
            if (-not (Test-Path $wfPath)) {
                New-Item -ItemType Directory -Path $wfPath -Force | Out-Null
            }
            Copy-Item "$DomyhRoot\.agent\workflows\*.md" -Destination $wfPath -Force
            
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$DomyhRoot\.agent\skills") {
                Copy-Item "$DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        default {
            Copy-Item "$DomyhRoot\root\AGENTS.md" -Destination "$path\AGENTS.md" -Force
        }
    }
    
    Write-Host "  ✅ $name $(Get-String 'configured')" -ForegroundColor Green
}

function Install-ToAllIDEs {
    param([array]$DetectedIDEs)
    
    Write-Host ""
    Write-Host "🚀 $(Get-String 'installing_to') all detected IDEs..." -ForegroundColor Green
    Write-Host ""
    
    foreach ($ide in $DetectedIDEs) {
        Install-ToIDE -IDE $ide
    }
    
    Write-Host ""
    Write-Host "✅ $(Get-String 'installation_complete')" -ForegroundColor Green
}

function Select-IDEs {
    param([array]$DetectedIDEs)
    
    Write-Host ""
    Write-Host "🎯 $(Get-String 'menu_select'):" -ForegroundColor Yellow
    Write-Host ""
    
    for ($i = 0; $i -lt $DetectedIDEs.Count; $i++) {
        $ide = $DetectedIDEs[$i]
        $name = $IDEConfigs[$ide].Name
        Write-Host "  $($i + 1)) $name"
    }
    
    Write-Host ""
    $selections = Read-Host "Enter choices (e.g., 1 3 5)"
    
    $numbers = $selections -split '\s+' | ForEach-Object { [int]$_ - 1 }
    
    foreach ($idx in $numbers) {
        if ($idx -ge 0 -and $idx -lt $DetectedIDEs.Count) {
            Install-ToIDE -IDE $DetectedIDEs[$idx]
        }
    }
    
    Write-Host ""
    Write-Host "✅ $(Get-String 'installation_complete')" -ForegroundColor Green
}

function Install-ToProject {
    param([string]$Path)
    
    if (-not $Path) {
        $Path = Read-Host "$(Get-String 'project_path')"
        if (-not $Path) {
            $Path = Get-Location
        }
    }
    
    if (-not (Test-Path $Path)) {
        Write-Host "❌ Directory does not exist: $Path" -ForegroundColor Red
        return
    }
    
    Write-Host "📦 $(Get-String 'installing_to') project: $Path" -ForegroundColor Blue
    
    Copy-Item "$DomyhRoot\.agent" -Destination $Path -Recurse -Force
    Copy-Item "$DomyhRoot\root\AGENTS.md" -Destination $Path -Force
    Copy-Item "$DomyhRoot\root\CLAUDE.md" -Destination $Path -Force
    Copy-Item "$DomyhRoot\root\GEMINI.md" -Destination $Path -Force
    Copy-Item "$DomyhRoot\root\.cursorrules" -Destination $Path -Force
    
    $githubPath = "$Path\.github"
    if (-not (Test-Path $githubPath)) {
        New-Item -ItemType Directory -Path $githubPath -Force | Out-Null
    }
    Copy-Item "$DomyhRoot\root\.github\copilot-instructions.md" -Destination $githubPath -Force
    
    Write-Host ""
    Write-Host "✅ $(Get-String 'installation_complete')" -ForegroundColor Green
    Write-Host ""
    Write-Host "$(Get-String 'files_created'):" -ForegroundColor Yellow
    Write-Host "  - .agent\           (Agent system)"
    Write-Host "  - AGENTS.md         (Universal)"
    Write-Host "  - CLAUDE.md         (Claude Code)"
    Write-Host "  - GEMINI.md         (Gemini CLI)"
    Write-Host "  - .cursorrules      (Cursor)"
    Write-Host "  - .github\copilot-instructions.md (Copilot)"
}

function Show-IDEDetails {
    Write-Host ""
    Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host "📖 IDE Configuration Details:" -ForegroundColor Yellow
    Write-Host ""
    
    Write-Host "1. Claude Code CLI" -ForegroundColor Blue
    Write-Host "   Global: ~/.claude/CLAUDE.md"
    Write-Host "   Skills: ~/.claude/skills/*/"
    Write-Host ""
    
    Write-Host "2. Cursor IDE" -ForegroundColor Blue
    Write-Host "   Global: ~/.cursor/rules/*.mdc"
    Write-Host "   Project: .cursor/rules/*.mdc, .cursorrules"
    Write-Host ""
    
    Write-Host "3. Windsurf IDE" -ForegroundColor Blue
    Write-Host "   Project: AGENTS.md (at root)"
    Write-Host ""
    
    Write-Host "4. VS Code (Copilot)" -ForegroundColor Blue
    Write-Host "   Project: .github/copilot-instructions.md"
    Write-Host ""
    
    Write-Host "5. Google Gemini CLI" -ForegroundColor Blue
    Write-Host "   Global: ~/.gemini/GEMINI.md"
    Write-Host "   Skills: ~/.gemini/skills/*/"
    Write-Host ""
    
    Write-Host "6. Continue.dev" -ForegroundColor Blue
    Write-Host "   Global: ~/.continue/AGENTS.md"
    Write-Host ""
    
    Write-Host "════════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
    Read-Host "$(Get-String 'press_enter')"
}

# ============================================================================
# Main
# ============================================================================

if ($Help) {
    Show-Help
    exit 0
}

# Set language from param
if ($Lang) {
    switch ($Lang.ToLower()) {
        "vi" { $Global:Language = "vi" }
        default { $Global:Language = "en" }
    }
}
else {
    Clear-Host
    Select-Language
}

Show-Banner
$detectedIDEs = Detect-IDEs

if ($All) {
    Install-ToAllIDEs -DetectedIDEs $detectedIDEs
    exit 0
}

if ($Project) {
    Install-ToProject -Path $ProjectPath
    exit 0
}

# Interactive mode
while ($true) {
    $choice = Show-Menu
    
    switch ($choice) {
        "1" { Install-ToAllIDEs -DetectedIDEs $detectedIDEs }
        "2" { Select-IDEs -DetectedIDEs $detectedIDEs }
        "3" { Install-ToProject }
        "4" { Show-IDEDetails }
        "5" { 
            Select-Language
            Show-Banner
        }
        "6" { 
            Write-Host "👋 $(Get-String 'goodbye')" -ForegroundColor Green
            exit 0
        }
        default {
            Write-Host "$(Get-String 'invalid_option')" -ForegroundColor Red
        }
    }
}

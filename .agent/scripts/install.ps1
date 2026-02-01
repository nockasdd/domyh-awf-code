# ==============================================================================
# DOMYH Awesome Code Library - Install Script for Windows PowerShell
# Version: 4.3.1
# Author: NockDev
# ==============================================================================

param (
    [switch]$Help,
    [switch]$All,
    [switch]$Project,
    [string]$ProjectPath = "",
    [string]$Lang = ""
)

# Script location
$DomyhRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
if ($DomyhRoot -eq "") {
    $DomyhRoot = Split-Path -Parent $PSScriptRoot
}

# Ensure we're in the correct directory
if (-not (Test-Path "$DomyhRoot\.agent")) {
    $DomyhRoot = Get-Location
}

# ==============================================================================
# IDE Configuration Registry (Verified 2025-2026)
# ==============================================================================
$IDEConfigs = @{
    "claude"          = @{
        Name        = "Claude Code CLI"
        GlobalPath  = "$env:USERPROFILE\.claude"
        ConfigFile  = "CLAUDE.md"
        SkillsDir   = "skills"
        Detected    = $false
        Description = "Anthropic Claude CLI for terminal"
    }
    "gemini"          = @{
        Name        = "Google Gemini CLI"
        GlobalPath  = "$env:USERPROFILE\.gemini"
        ConfigFile  = "GEMINI.md"
        SkillsDir   = "skills"
        Detected    = $false
        Description = "Google Gemini AI in terminal"
    }
    "antigravity"     = @{
        Name        = "Antigravity (Claude)"
        GlobalPath  = "$env:USERPROFILE\.gemini\antigravity"
        ConfigFile  = "CLAUDE.md"
        SkillsDir   = "skills"
        Detected    = $false
        Description = "Claude-based agent framework"
    }
    "codex"           = @{
        Name        = "OpenAI Codex CLI"
        GlobalPath  = "$env:USERPROFILE\.codex"
        ConfigFile  = "AGENTS.md"
        SkillsDir   = ""
        Detected    = $false
        Description = "OpenAI Codex terminal agent"
    }
    "continue"        = @{
        Name        = "Continue.dev"
        GlobalPath  = "$env:USERPROFILE\.continue"
        ConfigFile  = "config.yaml"
        RulesDir    = "rules"
        Detected    = $false
        Description = "Open-source AI code assistant"
    }
    "augment"         = @{
        Name        = "Augment Code"
        GlobalPath  = "$env:USERPROFILE\.augment"
        RulesDir    = "rules"
        Detected    = $false
        Description = "AI coding assistant"
    }
    "cursor"          = @{
        Name        = "Cursor IDE"
        GlobalPath  = "$env:USERPROFILE\.cursor"
        ProjectFile = ".cursorrules"
        Detected    = $false
        Description = "AI-first code editor"
    }
    "windsurf"        = @{
        Name         = "Windsurf IDE"
        GlobalPath   = "$env:USERPROFILE\.windsurf"
        ProjectFile  = ".windsurfrules"
        GlobalMemory = "$env:USERPROFILE\.codeium\windsurf\memories"
        Detected     = $false
        Description  = "Codeium AI IDE"
    }
    "vscode"          = @{
        Name        = "VS Code (Copilot)"
        GlobalPath  = "$env:USERPROFILE\.vscode"
        ProjectFile = ".github\copilot-instructions.md"
        Detected    = $false
        Description = "GitHub Copilot integration"
    }
    "vscode-insiders" = @{
        Name        = "VS Code Insiders"
        GlobalPath  = "$env:USERPROFILE\.vscode-insiders"
        ProjectFile = ".github\copilot-instructions.md"
        Detected    = $false
        Description = "VS Code preview builds"
    }
    "aider"           = @{
        Name        = "Aider"
        GlobalPath  = "$env:USERPROFILE\.aider"
        ConfigFile  = "aider.conf.yml"
        Detected    = $false
        Description = "AI pair programming CLI"
    }
}

# ==============================================================================
# Localization - English and Vietnamese
# ==============================================================================
$Strings = @{
    "en" = @{
        "title"                 = "DOMYH Awesome Code Library"
        "subtitle"              = "AI-Powered Development Assistant"
        "version"               = "Version 4.3.1"
        "developer"             = "Developed by NockDev"
        "select_language"       = "Select Language / Chon Ngon Ngu"
        "english"               = "English (default)"
        "vietnamese"            = "Tieng Viet"
        "choose"                = "Choose / Chon"
        "detecting"             = "Detecting installed AI IDEs..."
        "no_ides_detected"      = "No IDEs detected"
        "menu_title"            = "Installation Options"
        "menu_all"              = "Install to ALL detected IDEs"
        "menu_select"           = "Select specific IDEs"
        "menu_project"          = "Install to current project"
        "menu_details"          = "Show IDE details"
        "menu_language"         = "Change language"
        "menu_exit"             = "Exit"
        "select_option"         = "Select option"
        "installing_to"         = "Installing to"
        "installation_complete" = "Installation complete!"
        "files_created"         = "Files created"
        "configured"            = "configured"
        "invalid_option"        = "Invalid option"
        "press_enter"           = "Press Enter to continue..."
        "goodbye"               = "Goodbye!"
    }
    "vi" = @{
        "title"                 = "Thu Vien DOMYH Awesome Code"
        "subtitle"              = "Tro Ly Phat Trien Voi AI"
        "version"               = "Phien Ban 4.3.1"
        "developer"             = "Phat Trien Boi NockDev"
        "select_language"       = "Chon Ngon Ngu / Select Language"
        "english"               = "English"
        "vietnamese"            = "Tieng Viet (mac dinh)"
        "choose"                = "Chon / Choose"
        "detecting"             = "Dang phat hien cac IDE AI..."
        "no_ides_detected"      = "Khong phat hien IDE nao"
        "menu_title"            = "Tuy Chon Cai Dat"
        "menu_all"              = "Cai dat cho TAT CA IDE"
        "menu_select"           = "Chon IDE cu the"
        "menu_project"          = "Cai dat cho du an hien tai"
        "menu_details"          = "Xem chi tiet IDE"
        "menu_language"         = "Doi ngon ngu"
        "menu_exit"             = "Thoat"
        "select_option"         = "Chon tuy chon"
        "installing_to"         = "Dang cai dat vao"
        "installation_complete" = "Cai dat hoan tat!"
        "files_created"         = "Cac tep da tao"
        "configured"            = "da cau hinh"
        "invalid_option"        = "Tuy chon khong hop le"
        "press_enter"           = "Nhan Enter de tiep tuc..."
        "goodbye"               = "Tam biet!"
    }
}

$CurrentLang = "en"

function Get-String {
    param([string]$Key)
    return $Strings[$CurrentLang][$Key]
}

# ==============================================================================
# UI Functions
# ==============================================================================
function Show-Banner {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "                    $(Get-String 'title')                    " -ForegroundColor Yellow
    Write-Host "              $(Get-String 'subtitle')              " -ForegroundColor White
    Write-Host "                      $(Get-String 'version')                        " -ForegroundColor Gray
    Write-Host "                   $(Get-String 'developer')                   " -ForegroundColor Gray
    Write-Host "======================================================================" -ForegroundColor Cyan
}

function Show-LanguageSelection {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Magenta
    Write-Host "         $(Get-String 'select_language')         " -ForegroundColor Yellow
    Write-Host "======================================================================" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "  1) [EN] $(Get-String 'english')"
    Write-Host "  2) [VI] $(Get-String 'vietnamese')"
    Write-Host ""
    
    $choice = Read-Host "$(Get-String 'choose') (1-2)"
    
    switch ($choice) {
        "1" { $script:CurrentLang = "en" }
        "2" { $script:CurrentLang = "vi" }
        default { $script:CurrentLang = "en" }
    }
}

function Show-Help {
    Show-Banner
    Write-Host ""
    Write-Host "Usage: .\install.ps1 [options]" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "Options:" -ForegroundColor Cyan
    Write-Host "  -Help           Show this help message"
    Write-Host "  -All            Install to all detected IDEs"
    Write-Host "  -Project        Install to current project"
    Write-Host "  -ProjectPath    Specify project path"
    Write-Host "  -Lang           Set language (en, vi)"
    Write-Host ""
    Write-Host "Examples:" -ForegroundColor Cyan
    Write-Host "  .\install.ps1                    # Interactive mode"
    Write-Host "  .\install.ps1 -All               # Install to all IDEs"
    Write-Host "  .\install.ps1 -Project           # Install to current dir"
    Write-Host "  .\install.ps1 -Lang vi -All      # Vietnamese, install all"
    Write-Host ""
}

# ==============================================================================
# IDE Detection
# ==============================================================================
function Detect-IDEs {
    Write-Host ""
    Write-Host "[*] $(Get-String 'detecting')" -ForegroundColor Blue
    Write-Host ""
    
    $detected = @()
    
    foreach ($key in $IDEConfigs.Keys) {
        $config = $IDEConfigs[$key]
        $found = $false
        
        if (Test-Path $config.GlobalPath) {
            $found = $true
        }
        
        if ($found) {
            $IDEConfigs[$key].Detected = $true
            $detected += $key
            Write-Host "  [OK] $($config.Name)" -ForegroundColor Green -NoNewline
            Write-Host " - $($config.GlobalPath)" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    
    if ($detected.Count -eq 0) {
        Write-Host "[X] $(Get-String 'no_ides_detected')" -ForegroundColor Red
    }
    
    return $detected
}

# ==============================================================================
# Installation Functions
# ==============================================================================
function Install-ToIDE {
    param([string]$IDE)
    
    $config = $IDEConfigs[$IDE]
    $path = $config.GlobalPath
    $name = $config.Name
    
    # Ensure directory exists
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
    
    switch ($IDE) {
        "claude" {
            # ~/.claude/CLAUDE.md
            Copy-Item "$DomyhRoot\CLAUDE.md" -Destination "$path\CLAUDE.md" -Force
            # ~/.claude/skills/
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$DomyhRoot\.agent\skills") {
                Copy-Item "$DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        "gemini" {
            # ~/.gemini/GEMINI.md
            Copy-Item "$DomyhRoot\GEMINI.md" -Destination "$path\GEMINI.md" -Force
            # ~/.gemini/skills/
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$DomyhRoot\.agent\skills") {
                Copy-Item "$DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        "antigravity" {
            # ~/.gemini/antigravity/CLAUDE.md
            Copy-Item "$DomyhRoot\CLAUDE.md" -Destination "$path\CLAUDE.md" -Force
            # ~/.gemini/antigravity/skills/
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$DomyhRoot\.agent\skills") {
                Copy-Item "$DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        "codex" {
            # ~/.codex/AGENTS.md
            Copy-Item "$DomyhRoot\AGENTS.md" -Destination "$path\AGENTS.md" -Force
        }
        
        "continue" {
            # ~/.continue/rules/
            $rulesPath = "$path\rules"
            if (-not (Test-Path $rulesPath)) {
                New-Item -ItemType Directory -Path $rulesPath -Force | Out-Null
            }
            Copy-Item "$DomyhRoot\AGENTS.md" -Destination "$rulesPath\domyh-rules.md" -Force
        }
        
        "augment" {
            # ~/.augment/rules/
            $rulesPath = "$path\rules"
            if (-not (Test-Path $rulesPath)) {
                New-Item -ItemType Directory -Path $rulesPath -Force | Out-Null
            }
            Copy-Item "$DomyhRoot\AGENTS.md" -Destination "$rulesPath\domyh-rules.md" -Force
        }
        
        "cursor" {
            # Project file - no global install needed
            Write-Host "  [i] Cursor uses project-level .cursorrules file" -ForegroundColor Yellow
        }
        
        "windsurf" {
            # ~/.codeium/windsurf/memories/global_rules.md (if exists)
            $memoriesPath = "$env:USERPROFILE\.codeium\windsurf\memories"
            if (Test-Path $memoriesPath) {
                Copy-Item "$DomyhRoot\AGENTS.md" -Destination "$memoriesPath\global_rules.md" -Force
            }
        }
        
        "vscode" {
            # Project file - no global install needed
            Write-Host "  [i] VS Code Copilot uses project-level .github/copilot-instructions.md" -ForegroundColor Yellow
        }
        
        "vscode-insiders" {
            # Same as vscode
            Write-Host "  [i] VS Code Insiders uses project-level .github/copilot-instructions.md" -ForegroundColor Yellow
        }
        
        "aider" {
            # ~/.aider.conf.yml
            Copy-Item "$DomyhRoot\.aider.conf.yml" -Destination "$env:USERPROFILE\.aider.conf.yml" -Force
        }
        
        default {
            Copy-Item "$DomyhRoot\AGENTS.md" -Destination "$path\AGENTS.md" -Force
        }
    }
    
    Write-Host "  [OK] $name $(Get-String 'configured')" -ForegroundColor Green
}

function Install-ToAllIDEs {
    param([array]$DetectedIDEs)
    
    Write-Host ""
    Write-Host "[*] $(Get-String 'installing_to') all detected IDEs..." -ForegroundColor Green
    Write-Host ""
    
    foreach ($ide in $DetectedIDEs) {
        Install-ToIDE -IDE $ide
    }
    
    Write-Host ""
    Write-Host "[OK] $(Get-String 'installation_complete')" -ForegroundColor Green
}

function Install-ToProject {
    param([string]$Path)
    
    if ($Path -eq "") {
        $Path = Get-Location
    }
    
    Write-Host ""
    Write-Host "[*] $(Get-String 'installing_to') project: $Path" -ForegroundColor Blue
    Write-Host ""
    
    # Create directories
    if (-not (Test-Path "$Path\.agent")) {
        New-Item -ItemType Directory -Path "$Path\.agent" -Force | Out-Null
    }
    if (-not (Test-Path "$Path\.github")) {
        New-Item -ItemType Directory -Path "$Path\.github" -Force | Out-Null
    }
    
    # Copy .agent folder
    Copy-Item "$DomyhRoot\.agent\*" -Destination "$Path\.agent" -Recurse -Force
    
    # Copy root config files
    Copy-Item "$DomyhRoot\AGENTS.md" -Destination $Path -Force
    Copy-Item "$DomyhRoot\CLAUDE.md" -Destination $Path -Force
    Copy-Item "$DomyhRoot\GEMINI.md" -Destination $Path -Force
    Copy-Item "$DomyhRoot\.cursorrules" -Destination $Path -Force
    Copy-Item "$DomyhRoot\.windsurfrules" -Destination $Path -Force
    
    # Copy Copilot instructions
    Copy-Item "$DomyhRoot\.github\copilot-instructions.md" -Destination "$Path\.github" -Force
    
    Write-Host ""
    Write-Host "[OK] $(Get-String 'installation_complete')" -ForegroundColor Green
    Write-Host ""
    Write-Host "$(Get-String 'files_created'):" -ForegroundColor Yellow
    Write-Host "  - .agent\                           (Agent system)"
    Write-Host "  - AGENTS.md                         (Universal rules)"
    Write-Host "  - CLAUDE.md                         (Claude Code)"
    Write-Host "  - GEMINI.md                         (Gemini CLI)"
    Write-Host "  - .cursorrules                      (Cursor)"
    Write-Host "  - .windsurfrules                    (Windsurf)"
    Write-Host "  - .github\copilot-instructions.md   (GitHub Copilot)"
}

function Show-IDEDetails {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "                    IDE Configuration Details                    " -ForegroundColor Yellow
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host ""
    
    foreach ($key in $IDEConfigs.Keys | Sort-Object) {
        $config = $IDEConfigs[$key]
        $status = if ($config.Detected) { "[OK]" } else { "[--]" }
        $color = if ($config.Detected) { "Green" } else { "Gray" }
        
        Write-Host "$status $($config.Name)" -ForegroundColor $color
        Write-Host "    Path: $($config.GlobalPath)" -ForegroundColor Gray
        if ($config.ConfigFile) {
            Write-Host "    Config: $($config.ConfigFile)" -ForegroundColor Gray
        }
        if ($config.ProjectFile) {
            Write-Host "    Project: $($config.ProjectFile)" -ForegroundColor Gray
        }
        Write-Host ""
    }
}

function Show-Menu {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "[?] $(Get-String 'menu_title'):" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1) [GLOBAL] $(Get-String 'menu_all')"
    Write-Host "  2) [SELECT] $(Get-String 'menu_select')"
    Write-Host "  3) [PROJECT] $(Get-String 'menu_project')"
    Write-Host "  4) [INFO] $(Get-String 'menu_details')"
    Write-Host "  5) [LANG] $(Get-String 'menu_language')"
    Write-Host "  6) [EXIT] $(Get-String 'menu_exit')"
    Write-Host ""
}

# ==============================================================================
# Main Entry Point
# ==============================================================================
if ($Help) {
    Show-Help
    exit 0
}

# Set language from parameter
if ($Lang -ne "") {
    $CurrentLang = $Lang.ToLower()
    if ($CurrentLang -notin @("en", "vi")) {
        $CurrentLang = "en"
    }
}

# Show banner
Show-Banner

# Language selection if not specified
if ($Lang -eq "") {
    Show-LanguageSelection
    Show-Banner
}

# Detect IDEs
$detected = Detect-IDEs

# Handle command-line modes
if ($All) {
    Install-ToAllIDEs -DetectedIDEs $detected
    exit 0
}

if ($Project) {
    if ($ProjectPath -ne "") {
        Install-ToProject -Path $ProjectPath
    }
    else {
        Install-ToProject -Path (Get-Location)
    }
    exit 0
}

# Interactive mode
do {
    Show-Menu
    $choice = Read-Host "$(Get-String 'select_option') (1-6)"
    
    switch ($choice) {
        "1" {
            Install-ToAllIDEs -DetectedIDEs $detected
            Read-Host "$(Get-String 'press_enter')"
        }
        "2" {
            Write-Host ""
            Write-Host "Available IDEs:" -ForegroundColor Yellow
            $i = 1
            foreach ($ide in $detected) {
                Write-Host "  $i) $($IDEConfigs[$ide].Name)"
                $i++
            }
            Write-Host ""
            $selection = Read-Host "Enter numbers (comma-separated)"
            $indices = $selection -split "," | ForEach-Object { [int]$_.Trim() - 1 }
            foreach ($idx in $indices) {
                if ($idx -ge 0 -and $idx -lt $detected.Count) {
                    Install-ToIDE -IDE $detected[$idx]
                }
            }
            Read-Host "$(Get-String 'press_enter')"
        }
        "3" {
            $projectPath = Read-Host "Enter project path (or press Enter for current)"
            if ($projectPath -eq "") {
                Install-ToProject -Path (Get-Location)
            }
            else {
                Install-ToProject -Path $projectPath
            }
            Read-Host "$(Get-String 'press_enter')"
        }
        "4" {
            Show-IDEDetails
            Read-Host "$(Get-String 'press_enter')"
        }
        "5" {
            Show-LanguageSelection
            Show-Banner
            $detected = Detect-IDEs
        }
        "6" {
            Write-Host ""
            Write-Host "$(Get-String 'goodbye')" -ForegroundColor Cyan
            exit 0
        }
        default {
            Write-Host "[X] $(Get-String 'invalid_option')" -ForegroundColor Red
        }
    }
} while ($true)

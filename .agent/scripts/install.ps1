# ==============================================================================
# DOMYH Awesome Code Library - Install Script for Windows PowerShell
# Version: 4.3.1
# Author: NockDev
# 
# Usage:
#   Local:  .\install.ps1
#   Remote: iwr -useb https://raw.githubusercontent.com/nockasdd/domyh-awf-code/main/.agent/scripts/install.ps1 | iex
# ==============================================================================

# ==============================================================================
# Configuration
# ==============================================================================
$script:VERSION = "4.3.1"
$script:CurrentLang = "en"
$script:DomyhRoot = ""
$script:DETECTED_IDES = @()

# IDE Configuration Registry (Verified 2025-2026)
$script:IDEConfigs = @{
    "claude"          = @{
        Name       = "Claude Code CLI"
        GlobalPath = "$env:USERPROFILE\.claude"
        ConfigFile = "CLAUDE.md"
        SkillsDir  = "skills"
        Detected   = $false
    }
    "gemini"          = @{
        Name       = "Google Gemini CLI"
        GlobalPath = "$env:USERPROFILE\.gemini"
        ConfigFile = "GEMINI.md"
        SkillsDir  = "skills"
        Detected   = $false
    }
    "antigravity"     = @{
        Name       = "Antigravity (Claude)"
        GlobalPath = "$env:USERPROFILE\.gemini\antigravity"
        ConfigFile = "CLAUDE.md"
        SkillsDir  = "skills"
        Detected   = $false
    }
    "codex"           = @{
        Name       = "OpenAI Codex CLI"
        GlobalPath = "$env:USERPROFILE\.codex"
        ConfigFile = "AGENTS.md"
        Detected   = $false
    }
    "continue"        = @{
        Name       = "Continue.dev"
        GlobalPath = "$env:USERPROFILE\.continue"
        RulesDir   = "rules"
        Detected   = $false
    }
    "augment"         = @{
        Name       = "Augment Code"
        GlobalPath = "$env:USERPROFILE\.augment"
        RulesDir   = "rules"
        Detected   = $false
    }
    "cursor"          = @{
        Name        = "Cursor IDE"
        GlobalPath  = "$env:USERPROFILE\.cursor"
        ProjectFile = ".cursorrules"
        Detected    = $false
    }
    "windsurf"        = @{
        Name        = "Windsurf IDE"
        GlobalPath  = "$env:USERPROFILE\.windsurf"
        ProjectFile = ".windsurfrules"
        Detected    = $false
    }
    "vscode"          = @{
        Name        = "VS Code (Copilot)"
        GlobalPath  = "$env:USERPROFILE\.vscode"
        ProjectFile = ".github\copilot-instructions.md"
        Detected    = $false
    }
    "vscode-insiders" = @{
        Name        = "VS Code Insiders"
        GlobalPath  = "$env:USERPROFILE\.vscode-insiders"
        ProjectFile = ".github\copilot-instructions.md"
        Detected    = $false
    }
    "aider"           = @{
        Name       = "Aider"
        GlobalPath = "$env:USERPROFILE\.aider"
        ConfigFile = "aider.conf.yml"
        Detected   = $false
    }
}

# ==============================================================================
# Localization
# ==============================================================================
$script:Strings = @{
    "en" = @{
        "title"                 = "DOMYH Awesome Code Library"
        "subtitle"              = "AI-Powered Development Assistant"
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
        "downloading"           = "Downloading DOMYH library..."
        "clone_success"         = "Repository cloned successfully!"
        "enter_project"         = "Enter project path (or Enter for current)"
    }
    "vi" = @{
        "title"                 = "Thu Vien DOMYH Awesome Code"
        "subtitle"              = "Tro Ly Phat Trien Voi AI"
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
        "downloading"           = "Dang tai thu vien DOMYH..."
        "clone_success"         = "Da clone repository thanh cong!"
        "enter_project"         = "Nhap duong dan du an (hoac Enter cho thu muc hien tai)"
    }
}

function Get-LocalizedString {
    param([string]$Key)
    return $script:Strings[$script:CurrentLang][$Key]
}

# ==============================================================================
# UI Functions
# ==============================================================================
function Show-Banner {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "                    $(Get-LocalizedString 'title')                    " -ForegroundColor Yellow
    Write-Host "              $(Get-LocalizedString 'subtitle')              " -ForegroundColor White
    Write-Host "                      Version $script:VERSION                        " -ForegroundColor Gray
    Write-Host "                   Developed by NockDev                   " -ForegroundColor Gray
    Write-Host "======================================================================" -ForegroundColor Cyan
}

function Show-LanguageSelection {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Magenta
    Write-Host "         $(Get-LocalizedString 'select_language')         " -ForegroundColor Yellow
    Write-Host "======================================================================" -ForegroundColor Magenta
    Write-Host ""
    Write-Host "  1) [EN] $(Get-LocalizedString 'english')"
    Write-Host "  2) [VI] $(Get-LocalizedString 'vietnamese')"
    Write-Host ""
    
    $choice = Read-Host "$(Get-LocalizedString 'choose') (1-2)"
    
    switch ($choice) {
        "1" { $script:CurrentLang = "en" }
        "2" { $script:CurrentLang = "vi" }
        default { $script:CurrentLang = "en" }
    }
}

# ==============================================================================
# IDE Detection
# ==============================================================================
function Find-InstalledIDEs {
    Write-Host ""
    Write-Host "[*] $(Get-LocalizedString 'detecting')" -ForegroundColor Blue
    Write-Host ""
    
    $script:DETECTED_IDES = @()
    
    foreach ($key in $script:IDEConfigs.Keys) {
        $config = $script:IDEConfigs[$key]
        
        if (Test-Path $config.GlobalPath) {
            $script:IDEConfigs[$key].Detected = $true
            $script:DETECTED_IDES += $key
            Write-Host "  [OK] $($config.Name)" -ForegroundColor Green -NoNewline
            Write-Host " - $($config.GlobalPath)" -ForegroundColor Gray
        }
    }
    
    Write-Host ""
    
    if ($script:DETECTED_IDES.Count -eq 0) {
        Write-Host "[X] $(Get-LocalizedString 'no_ides_detected')" -ForegroundColor Red
    }
}

# ==============================================================================
# Download/Clone Repository
# ==============================================================================
function Get-DomyhRepository {
    $tempDir = "$env:TEMP\domyh-awesome-code-$(Get-Random)"
    
    Write-Host ""
    Write-Host "[*] $(Get-LocalizedString 'downloading')" -ForegroundColor Blue
    
    # Try git clone first
    $gitAvailable = Get-Command git -ErrorAction SilentlyContinue
    
    if ($gitAvailable) {
        try {
            git clone --depth 1 https://github.com/nockasdd/domyh-awf-code.git $tempDir 2>&1 | Out-Null
            if (Test-Path "$tempDir\.agent") {
                Write-Host "[OK] $(Get-LocalizedString 'clone_success')" -ForegroundColor Green
                return $tempDir
            }
        }
        catch {
            # Fall through to ZIP download
        }
    }
    
    # Fallback: Download ZIP
    try {
        $zipUrl = "https://github.com/nockasdd/domyh-awf-code/archive/refs/heads/main.zip"
        $zipPath = "$env:TEMP\domyh-$(Get-Random).zip"
        
        Invoke-WebRequest -Uri $zipUrl -OutFile $zipPath -UseBasicParsing
        
        Expand-Archive -Path $zipPath -DestinationPath $tempDir -Force
        Remove-Item $zipPath -Force
        
        # Find extracted folder
        $extracted = Get-ChildItem $tempDir -Directory | Select-Object -First 1
        if ($extracted) {
            $script:DomyhRoot = $extracted.FullName
            Write-Host "[OK] $(Get-LocalizedString 'clone_success')" -ForegroundColor Green
            return $extracted.FullName
        }
    }
    catch {
        Write-Host "[X] Download failed: $_" -ForegroundColor Red
        return $null
    }
    
    return $null
}

# ==============================================================================
# Installation Functions
# ==============================================================================
function Install-ToSingleIDE {
    param([string]$IDE)
    
    $config = $script:IDEConfigs[$IDE]
    $path = $config.GlobalPath
    $name = $config.Name
    
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
    }
    
    switch ($IDE) {
        "claude" {
            Copy-Item "$script:DomyhRoot\CLAUDE.md" -Destination "$path\CLAUDE.md" -Force
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$script:DomyhRoot\.agent\skills") {
                Copy-Item "$script:DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        "gemini" {
            Copy-Item "$script:DomyhRoot\GEMINI.md" -Destination "$path\GEMINI.md" -Force
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$script:DomyhRoot\.agent\skills") {
                Copy-Item "$script:DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        "antigravity" {
            Copy-Item "$script:DomyhRoot\CLAUDE.md" -Destination "$path\CLAUDE.md" -Force
            $skillsPath = "$path\skills"
            if (-not (Test-Path $skillsPath)) {
                New-Item -ItemType Directory -Path $skillsPath -Force | Out-Null
            }
            if (Test-Path "$script:DomyhRoot\.agent\skills") {
                Copy-Item "$script:DomyhRoot\.agent\skills\*" -Destination $skillsPath -Recurse -Force
            }
        }
        
        "codex" {
            Copy-Item "$script:DomyhRoot\AGENTS.md" -Destination "$path\AGENTS.md" -Force
        }
        
        "continue" {
            $rulesPath = "$path\rules"
            if (-not (Test-Path $rulesPath)) {
                New-Item -ItemType Directory -Path $rulesPath -Force | Out-Null
            }
            Copy-Item "$script:DomyhRoot\AGENTS.md" -Destination "$rulesPath\domyh-rules.md" -Force
        }
        
        "augment" {
            $rulesPath = "$path\rules"
            if (-not (Test-Path $rulesPath)) {
                New-Item -ItemType Directory -Path $rulesPath -Force | Out-Null
            }
            Copy-Item "$script:DomyhRoot\AGENTS.md" -Destination "$rulesPath\domyh-rules.md" -Force
        }
        
        "cursor" {
            Write-Host "  [i] Cursor uses project-level .cursorrules" -ForegroundColor Yellow
        }
        
        "windsurf" {
            $memoriesPath = "$env:USERPROFILE\.codeium\windsurf\memories"
            if (Test-Path $memoriesPath) {
                Copy-Item "$script:DomyhRoot\AGENTS.md" -Destination "$memoriesPath\global_rules.md" -Force
            }
        }
        
        "vscode" {
            Write-Host "  [i] VS Code uses project-level .github/copilot-instructions.md" -ForegroundColor Yellow
        }
        
        "vscode-insiders" {
            Write-Host "  [i] VS Code Insiders uses project-level files" -ForegroundColor Yellow
        }
        
        "aider" {
            if (Test-Path "$script:DomyhRoot\.aider.conf.yml") {
                Copy-Item "$script:DomyhRoot\.aider.conf.yml" -Destination "$env:USERPROFILE\.aider.conf.yml" -Force
            }
        }
        
        default {
            Copy-Item "$script:DomyhRoot\AGENTS.md" -Destination "$path\AGENTS.md" -Force
        }
    }
    
    Write-Host "  [OK] $name $(Get-LocalizedString 'configured')" -ForegroundColor Green
}

function Install-ToAllIDEs {
    Write-Host ""
    Write-Host "[*] $(Get-LocalizedString 'installing_to') all detected IDEs..." -ForegroundColor Green
    Write-Host ""
    
    foreach ($ide in $script:DETECTED_IDES) {
        Install-ToSingleIDE -IDE $ide
    }
    
    Write-Host ""
    Write-Host "[OK] $(Get-LocalizedString 'installation_complete')" -ForegroundColor Green
}

function Install-ToProject {
    param([string]$Path)
    
    if ([string]::IsNullOrEmpty($Path)) {
        $Path = Get-Location
    }
    
    Write-Host ""
    Write-Host "[*] $(Get-LocalizedString 'installing_to') project: $Path" -ForegroundColor Blue
    Write-Host ""
    
    # Create directories
    if (-not (Test-Path "$Path\.agent")) {
        New-Item -ItemType Directory -Path "$Path\.agent" -Force | Out-Null
    }
    if (-not (Test-Path "$Path\.github")) {
        New-Item -ItemType Directory -Path "$Path\.github" -Force | Out-Null
    }
    
    # Copy files
    Copy-Item "$script:DomyhRoot\.agent\*" -Destination "$Path\.agent" -Recurse -Force
    Copy-Item "$script:DomyhRoot\AGENTS.md" -Destination $Path -Force
    Copy-Item "$script:DomyhRoot\CLAUDE.md" -Destination $Path -Force
    Copy-Item "$script:DomyhRoot\GEMINI.md" -Destination $Path -Force
    Copy-Item "$script:DomyhRoot\.cursorrules" -Destination $Path -Force
    Copy-Item "$script:DomyhRoot\.windsurfrules" -Destination $Path -Force
    Copy-Item "$script:DomyhRoot\.github\copilot-instructions.md" -Destination "$Path\.github" -Force
    
    Write-Host ""
    Write-Host "[OK] $(Get-LocalizedString 'installation_complete')" -ForegroundColor Green
    Write-Host ""
    Write-Host "$(Get-LocalizedString 'files_created'):" -ForegroundColor Yellow
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
    
    foreach ($key in $script:IDEConfigs.Keys | Sort-Object) {
        $config = $script:IDEConfigs[$key]
        $status = if ($config.Detected) { "[OK]" } else { "[--]" }
        $color = if ($config.Detected) { "Green" } else { "Gray" }
        
        Write-Host "$status $($config.Name)" -ForegroundColor $color
        Write-Host "    Path: $($config.GlobalPath)" -ForegroundColor Gray
        Write-Host ""
    }
}

function Show-Menu {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Cyan
    Write-Host "[?] $(Get-LocalizedString 'menu_title'):" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1) [GLOBAL] $(Get-LocalizedString 'menu_all')"
    Write-Host "  2) [SELECT] $(Get-LocalizedString 'menu_select')"
    Write-Host "  3) [PROJECT] $(Get-LocalizedString 'menu_project')"
    Write-Host "  4) [INFO] $(Get-LocalizedString 'menu_details')"
    Write-Host "  5) [LANG] $(Get-LocalizedString 'menu_language')"
    Write-Host "  6) [EXIT] $(Get-LocalizedString 'menu_exit')"
    Write-Host ""
}

# ==============================================================================
# Main Entry Point
# ==============================================================================
function Start-DomyhInstaller {
    # Show banner
    Show-Banner
    
    # Language selection
    Show-LanguageSelection
    Show-Banner
    
    # Download repository
    $script:DomyhRoot = Get-DomyhRepository
    
    if (-not $script:DomyhRoot -or -not (Test-Path "$script:DomyhRoot\.agent")) {
        Write-Host "[X] Failed to download DOMYH library" -ForegroundColor Red
        return
    }
    
    # Detect IDEs
    Find-InstalledIDEs
    
    # Interactive menu
    do {
        Show-Menu
        $choice = Read-Host "$(Get-LocalizedString 'select_option') (1-6)"
        
        switch ($choice) {
            "1" {
                Install-ToAllIDEs
                Read-Host "$(Get-LocalizedString 'press_enter')"
            }
            "2" {
                Write-Host ""
                Write-Host "Available IDEs:" -ForegroundColor Yellow
                $i = 1
                foreach ($ide in $script:DETECTED_IDES) {
                    Write-Host "  $i) $($script:IDEConfigs[$ide].Name)"
                    $i++
                }
                Write-Host ""
                $selection = Read-Host "Enter numbers (comma-separated)"
                $indices = $selection -split "," | ForEach-Object { [int]$_.Trim() - 1 }
                foreach ($idx in $indices) {
                    if ($idx -ge 0 -and $idx -lt $script:DETECTED_IDES.Count) {
                        Install-ToSingleIDE -IDE $script:DETECTED_IDES[$idx]
                    }
                }
                Read-Host "$(Get-LocalizedString 'press_enter')"
            }
            "3" {
                $projectPath = Read-Host "$(Get-LocalizedString 'enter_project')"
                Install-ToProject -Path $projectPath
                Read-Host "$(Get-LocalizedString 'press_enter')"
            }
            "4" {
                Show-IDEDetails
                Read-Host "$(Get-LocalizedString 'press_enter')"
            }
            "5" {
                Show-LanguageSelection
                Show-Banner
            }
            "6" {
                Write-Host ""
                Write-Host "$(Get-LocalizedString 'goodbye')" -ForegroundColor Cyan
                
                # Cleanup temp directory
                if ($script:DomyhRoot -like "*\Temp\*") {
                    Remove-Item -Recurse -Force $script:DomyhRoot -ErrorAction SilentlyContinue
                }
                return
            }
            default {
                Write-Host "[X] $(Get-LocalizedString 'invalid_option')" -ForegroundColor Red
            }
        }
    } while ($true)
}

# Run the installer
Start-DomyhInstaller

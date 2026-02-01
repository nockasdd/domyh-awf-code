#!/bin/bash
# ============================================================================
# DOMYH Awesome Code Library - Smart Installer
# Version: 2.0.0
# Developer: NockDev (https://github.com/nockasdd)
# Supports: Linux, macOS, Windows (Git Bash/WSL)
# ============================================================================

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOMYH_ROOT="$(dirname "$(dirname "$SCRIPT_DIR")")"

# Default language
LANGUAGE="en"

# ============================================================================
# Internationalization (i18n)
# ============================================================================

# English strings
declare -A EN
EN[banner_title]="DOMYH Awesome Code Library"
EN[banner_subtitle]="AI-Powered Development Assistant"
EN[banner_by]="Developed by NockDev"
EN[detecting_os]="Detected OS"
EN[detecting_ides]="Detecting installed AI IDEs..."
EN[select_language]="Select Language"
EN[option_english]="English"
EN[option_vietnamese]="Tiếng Việt"
EN[menu_title]="Installation Options"
EN[menu_all]="Install to ALL detected IDEs"
EN[menu_select]="Select specific IDEs"
EN[menu_project]="Install to current project only"
EN[menu_details]="Show IDE configuration details"
EN[menu_exit]="Exit"
EN[choose_option]="Choose option"
EN[installing_to]="Installing to"
EN[installation_complete]="Installation complete!"
EN[project_path]="Enter project path (or press Enter for current directory)"
EN[files_created]="Files created"
EN[goodbye]="Goodbye!"
EN[invalid_option]="Invalid option. Please try again."
EN[no_ides_detected]="No AI IDEs detected. You can still install manually."
EN[press_enter]="Press Enter to continue..."
EN[configured]="configured!"
EN[version]="Version"

# Vietnamese strings
declare -A VI
VI[banner_title]="DOMYH Awesome Code Library"
VI[banner_subtitle]="Trợ lý Phát triển Ứng dụng AI"
VI[banner_by]="Phát triển bởi NockDev"
VI[detecting_os]="Hệ điều hành"
VI[detecting_ides]="Đang phát hiện các AI IDE đã cài đặt..."
VI[select_language]="Chọn Ngôn ngữ"
VI[option_english]="English"
VI[option_vietnamese]="Tiếng Việt"
VI[menu_title]="Tùy chọn Cài đặt"
VI[menu_all]="Cài đặt cho TẤT CẢ IDE đã phát hiện"
VI[menu_select]="Chọn IDE cụ thể"
VI[menu_project]="Cài đặt cho project hiện tại"
VI[menu_details]="Xem chi tiết cấu hình IDE"
VI[menu_exit]="Thoát"
VI[choose_option]="Chọn tùy chọn"
VI[installing_to]="Đang cài đặt cho"
VI[installation_complete]="Cài đặt hoàn tất!"
VI[project_path]="Nhập đường dẫn project (hoặc Enter cho thư mục hiện tại)"
VI[files_created]="Các file đã tạo"
VI[goodbye]="Tạm biệt!"
VI[invalid_option]="Tùy chọn không hợp lệ. Vui lòng thử lại."
VI[no_ides_detected]="Không phát hiện AI IDE. Bạn vẫn có thể cài đặt thủ công."
VI[press_enter]="Nhấn Enter để tiếp tục..."
VI[configured]="đã cấu hình!"
VI[version]="Phiên bản"

# Get localized string
t() {
    local key="$1"
    if [ "$LANGUAGE" == "vi" ]; then
        echo "${VI[$key]}"
    else
        echo "${EN[$key]}"
    fi
}

# ============================================================================
# IDE Configuration Paths
# ============================================================================

declare -A IDE_PATHS
declare -A IDE_NAMES
declare -A IDE_FILES

# Claude Code CLI
IDE_NAMES["claude"]="Claude Code CLI"
IDE_PATHS["claude"]="$HOME/.claude"
IDE_FILES["claude"]="CLAUDE.md"

# Cursor IDE  
IDE_NAMES["cursor"]="Cursor IDE"
IDE_PATHS["cursor"]="$HOME/.cursor"
IDE_FILES["cursor"]=".cursorrules"

# Windsurf IDE
IDE_NAMES["windsurf"]="Windsurf IDE"
IDE_PATHS["windsurf"]="$HOME/.windsurf"
IDE_FILES["windsurf"]="AGENTS.md"

# VS Code (Copilot)
IDE_NAMES["vscode"]="VS Code (Copilot)"
IDE_PATHS["vscode"]="$HOME/.vscode"
IDE_FILES["vscode"]=".github/copilot-instructions.md"

# VS Code Insiders
IDE_NAMES["vscode-insiders"]="VS Code Insiders"
IDE_PATHS["vscode-insiders"]="$HOME/.vscode-insiders"
IDE_FILES["vscode-insiders"]=".github/copilot-instructions.md"

# Augment Code
IDE_NAMES["augment"]="Augment Code"
IDE_PATHS["augment"]="$HOME/.augment"
IDE_FILES["augment"]="rules/"

# OpenAI Codex CLI
IDE_NAMES["codex"]="OpenAI Codex CLI"
IDE_PATHS["codex"]="$HOME/.codex"
IDE_FILES["codex"]="AGENTS.md"

# Gemini CLI
IDE_NAMES["gemini"]="Google Gemini CLI"
IDE_PATHS["gemini"]="$HOME/.gemini"
IDE_FILES["gemini"]="GEMINI.md"

# Antigravity (Claude Code extension)
IDE_NAMES["antigravity"]="Antigravity (Claude)"
IDE_PATHS["antigravity"]="$HOME/.gemini/antigravity"
IDE_FILES["antigravity"]="global_workflows/"

# Zed IDE
IDE_NAMES["zed"]="Zed Editor"
IDE_PATHS["zed"]="$HOME/.config/zed"
IDE_FILES["zed"]=".zed/settings.json"

# Continue.dev
IDE_NAMES["continue"]="Continue.dev"
IDE_PATHS["continue"]="$HOME/.continue"
IDE_FILES["continue"]="AGENTS.md"

# ============================================================================
# Functions
# ============================================================================

print_banner() {
    echo -e "${CYAN}"
    echo "╔══════════════════════════════════════════════════════════════════╗"
    echo "║                    🚀 $(t banner_title)                     ║"
    echo "║              $(t banner_subtitle)              ║"
    echo "║                      $(t version) 2.0.0                        ║"
    echo "║                   $(t banner_by)                   ║"
    echo "╚══════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

select_language() {
    echo ""
    echo -e "${MAGENTA}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${MAGENTA}║                   🌍 Select Language / Chọn Ngôn ngữ             ║${NC}"
    echo -e "${MAGENTA}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
    echo "  1) 🇺🇸 English (default)"
    echo "  2) 🇻🇳 Tiếng Việt"
    echo ""
    read -p "Choose / Chọn (1-2): " lang_choice
    
    case $lang_choice in
        2) LANGUAGE="vi" ;;
        *) LANGUAGE="en" ;;
    esac
    
    # Update config.yaml with selected language
    update_language_config
    
    echo ""
    if [ "$LANGUAGE" == "vi" ]; then
        echo -e "${GREEN}✅ Đã chọn: Tiếng Việt${NC}"
    else
        echo -e "${GREEN}✅ Selected: English${NC}"
    fi
}

update_language_config() {
    # Update default language in config.yaml
    local config_file="$DOMYH_ROOT/.agent/config.yaml"
    if [ -f "$config_file" ]; then
        if [ "$LANGUAGE" == "vi" ]; then
            sed -i.bak 's/default: "en"/default: "vi"/' "$config_file" 2>/dev/null || \
            sed -i '' 's/default: "en"/default: "vi"/' "$config_file"
        else
            sed -i.bak 's/default: "vi"/default: "en"/' "$config_file" 2>/dev/null || \
            sed -i '' 's/default: "vi"/default: "en"/' "$config_file"
        fi
        rm -f "${config_file}.bak"
    fi
}

detect_os() {
    case "$(uname -s)" in
        Linux*)     OS="Linux";;
        Darwin*)    OS="macOS";;
        CYGWIN*|MINGW*|MSYS*) OS="Windows";;
        *)          OS="Unknown";;
    esac
    echo -e "${BLUE}📦 $(t detecting_os): ${OS}${NC}"
}

detect_ides() {
    echo ""
    echo -e "${YELLOW}🔍 $(t detecting_ides)${NC}"
    echo ""
    
    DETECTED_IDES=()
    
    for ide in "${!IDE_PATHS[@]}"; do
        path="${IDE_PATHS[$ide]}"
        name="${IDE_NAMES[$ide]}"
        
        if [ -d "$path" ]; then
            DETECTED_IDES+=("$ide")
            echo -e "  ${GREEN}✅ $name${NC} — $path"
        fi
    done
    
    # Check for common project locations
    echo ""
    echo -e "${YELLOW}📁 Checking common IDE config locations...${NC}"
    echo ""
    
    # Additional checks for Windows paths via env vars
    if [ -n "$APPDATA" ]; then
        check_windows_ide "Cursor" "$APPDATA/Cursor"
        check_windows_ide "VS Code" "$APPDATA/Code"
        check_windows_ide "VS Code Insiders" "$APPDATA/Code - Insiders"
    fi
    
    if [ ${#DETECTED_IDES[@]} -eq 0 ]; then
        echo -e "${RED}❌ $(t no_ides_detected)${NC}"
    fi
}

check_windows_ide() {
    local name="$1"
    local path="$2"
    if [ -d "$path" ]; then
        echo -e "  ${GREEN}✅ $name (Windows)${NC} — $path"
    fi
}

show_menu() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}📋 $(t menu_title):${NC}"
    echo ""
    echo "  1) 🌍 $(t menu_all)"
    echo "  2) 🎯 $(t menu_select)"
    echo "  3) 📁 $(t menu_project)"
    echo "  4) 📖 $(t menu_details)"
    echo "  5) 🌐 Change Language / Đổi Ngôn ngữ"
    echo "  6) ❌ $(t menu_exit)"
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo ""
    read -p "$(t choose_option) (1-6): " choice
}

install_to_all() {
    echo ""
    echo -e "${GREEN}🚀 $(t installing_to) all detected IDEs...${NC}"
    echo ""
    
    for ide in "${DETECTED_IDES[@]}"; do
        install_to_ide "$ide"
    done
    
    echo ""
    echo -e "${GREEN}✅ $(t installation_complete)${NC}"
}

select_ides() {
    echo ""
    echo -e "${YELLOW}🎯 Select IDEs to install (space-separated numbers):${NC}"
    echo ""
    
    local i=1
    for ide in "${DETECTED_IDES[@]}"; do
        echo "  $i) ${IDE_NAMES[$ide]}"
        ((i++))
    done
    
    echo ""
    read -p "Enter choices (e.g., 1 3 5): " -a selections
    
    for sel in "${selections[@]}"; do
        local idx=$((sel - 1))
        if [ $idx -ge 0 ] && [ $idx -lt ${#DETECTED_IDES[@]} ]; then
            install_to_ide "${DETECTED_IDES[$idx]}"
        fi
    done
    
    echo ""
    echo -e "${GREEN}✅ $(t installation_complete)${NC}"
}

install_to_ide() {
    local ide="$1"
    local name="${IDE_NAMES[$ide]}"
    local path="${IDE_PATHS[$ide]}"
    local file="${IDE_FILES[$ide]}"
    
    echo -e "${BLUE}📦 $(t installing_to) $name...${NC}"
    
    # Create directory if not exists
    mkdir -p "$path"
    
    case "$ide" in
        "claude")
            cp "$DOMYH_ROOT/CLAUDE.md" "$path/CLAUDE.md"
            mkdir -p "$path/skills"
            cp -r "$DOMYH_ROOT/.agent/skills/"* "$path/skills/" 2>/dev/null || true
            ;;
        
        "cursor")
            mkdir -p "$path/rules"
            for rule in "$DOMYH_ROOT/.agent/rules/"*.md; do
                if [ -f "$rule" ]; then
                    local basename=$(basename "$rule" .md)
                    cp "$rule" "$path/rules/$basename.mdc"
                fi
            done
            ;;
        
        "windsurf"|"codex"|"continue")
            cp "$DOMYH_ROOT/AGENTS.md" "$path/AGENTS.md"
            ;;
        
        "gemini")
            cp "$DOMYH_ROOT/GEMINI.md" "$path/GEMINI.md"
            mkdir -p "$path/skills"
            cp -r "$DOMYH_ROOT/.agent/skills/"* "$path/skills/" 2>/dev/null || true
            ;;
        
        "augment")
            mkdir -p "$path/rules"
            for rule in "$DOMYH_ROOT/.agent/rules/"*.md; do
                if [ -f "$rule" ]; then
                    cp "$rule" "$path/rules/"
                fi
            done
            ;;
        
        "antigravity")
            mkdir -p "$path/global_workflows"
            for wf in "$DOMYH_ROOT/.agent/workflows/"*.md; do
                if [ -f "$wf" ]; then
                    cp "$wf" "$path/global_workflows/"
                fi
            done
            mkdir -p "$path/skills"
            cp -r "$DOMYH_ROOT/.agent/skills/"* "$path/skills/" 2>/dev/null || true
            ;;
        
        *)
            cp "$DOMYH_ROOT/AGENTS.md" "$path/AGENTS.md"
            ;;
    esac
    
    echo -e "  ${GREEN}✅ $name $(t configured)${NC}"
}

install_to_project() {
    echo ""
    read -p "$(t project_path): " project_path
    
    if [ -z "$project_path" ]; then
        project_path="$(pwd)"
    fi
    
    if [ ! -d "$project_path" ]; then
        echo -e "${RED}❌ Directory does not exist: $project_path${NC}"
        return 1
    fi
    
    echo -e "${BLUE}📦 $(t installing_to) project: $project_path${NC}"
    
    # Copy .agent folder
    cp -r "$DOMYH_ROOT/.agent" "$project_path/"
    
    # Copy root files
    cp "$DOMYH_ROOT/AGENTS.md" "$project_path/"
    cp "$DOMYH_ROOT/CLAUDE.md" "$project_path/"
    cp "$DOMYH_ROOT/GEMINI.md" "$project_path/"
    cp "$DOMYH_ROOT/.cursorrules" "$project_path/"
    cp "$DOMYH_ROOT/.windsurfrules" "$project_path/"
    
    # Create .github for Copilot
    mkdir -p "$project_path/.github"
    cp "$DOMYH_ROOT/.github/copilot-instructions.md" "$project_path/.github/"
    
    echo -e "${GREEN}✅ $(t installation_complete)${NC}"
    echo ""
    echo "$(t files_created):"
    echo "  - .agent/           (Agent system)"
    echo "  - AGENTS.md         (Universal)"
    echo "  - CLAUDE.md         (Claude Code)"
    echo "  - GEMINI.md         (Gemini CLI)"
    echo "  - .cursorrules      (Cursor)"
    echo "  - .windsurfrules    (Windsurf)"
    echo "  - .github/copilot-instructions.md (Copilot)"
}

show_ide_details() {
    echo ""
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    echo -e "${YELLOW}📖 IDE Configuration Details:${NC}"
    echo ""
    
    echo -e "${BLUE}1. Claude Code CLI${NC}"
    echo "   Global: ~/.claude/CLAUDE.md"
    echo "   Skills: ~/.claude/skills/*/"
    echo ""
    
    echo -e "${BLUE}2. Cursor IDE${NC}"
    echo "   Global: ~/.cursor/rules/*.mdc"
    echo "   Project: .cursor/rules/*.mdc, .cursorrules"
    echo ""
    
    echo -e "${BLUE}3. Windsurf IDE${NC}"
    echo "   Project: AGENTS.md (at root)"
    echo ""
    
    echo -e "${BLUE}4. VS Code (Copilot)${NC}"
    echo "   Project: .github/copilot-instructions.md"
    echo ""
    
    echo -e "${BLUE}5. Google Gemini CLI${NC}"
    echo "   Global: ~/.gemini/GEMINI.md"
    echo "   Skills: ~/.gemini/skills/*/"
    echo ""
    
    echo -e "${BLUE}6. Continue.dev${NC}"
    echo "   Global: ~/.continue/AGENTS.md"
    echo ""
    
    echo -e "${CYAN}════════════════════════════════════════════════════════════════════${NC}"
    read -p "$(t press_enter)"
}

# ============================================================================
# Main
# ============================================================================

main() {
    clear
    select_language
    print_banner
    detect_os
    detect_ides
    
    while true; do
        show_menu
        
        case $choice in
            1) install_to_all ;;
            2) select_ides ;;
            3) install_to_project ;;
            4) show_ide_details ;;
            5) 
                select_language
                print_banner
                ;;
            6) 
                echo -e "${GREEN}👋 $(t goodbye)${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}$(t invalid_option)${NC}"
                ;;
        esac
    done
}

main "$@"

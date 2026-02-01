#!/bin/bash
# ==============================================================================
# DOMYH Awesome Code Library - Install Script for Linux/macOS/WSL
# Version: 4.3.1
# Author: NockDev
# ==============================================================================

set -e

# Script location
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOMYH_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"

# If .agent not found, try current directory
if [ ! -d "$DOMYH_ROOT/.agent" ]; then
    DOMYH_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
fi

# ==============================================================================
# Colors
# ==============================================================================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
GRAY='\033[0;37m'
NC='\033[0m' # No Color

# ==============================================================================
# Configuration
# ==============================================================================
VERSION="4.3.1"
LANG_CODE="en"

# IDE Configuration Registry (Verified 2025-2026)
declare -A IDE_NAMES=(
    ["claude"]="Claude Code CLI"
    ["gemini"]="Google Gemini CLI"
    ["antigravity"]="Antigravity (Claude)"
    ["codex"]="OpenAI Codex CLI"
    ["continue"]="Continue.dev"
    ["augment"]="Augment Code"
    ["cursor"]="Cursor IDE"
    ["windsurf"]="Windsurf IDE"
    ["vscode"]="VS Code (Copilot)"
    ["aider"]="Aider"
)

declare -A IDE_PATHS=(
    ["claude"]="$HOME/.claude"
    ["gemini"]="$HOME/.gemini"
    ["antigravity"]="$HOME/.gemini/antigravity"
    ["codex"]="$HOME/.codex"
    ["continue"]="$HOME/.continue"
    ["augment"]="$HOME/.augment"
    ["cursor"]="$HOME/.cursor"
    ["windsurf"]="$HOME/.windsurf"
    ["vscode"]="$HOME/.vscode"
    ["aider"]="$HOME/.aider"
)

declare -A IDE_DETECTED=()

# ==============================================================================
# Localization
# ==============================================================================
declare -A STRINGS_EN=(
    ["title"]="DOMYH Awesome Code Library"
    ["subtitle"]="AI-Powered Development Assistant"
    ["select_language"]="Select Language / Chon Ngon Ngu"
    ["english"]="English (default)"
    ["vietnamese"]="Tieng Viet"
    ["detecting"]="Detecting installed AI IDEs..."
    ["no_ides"]="No IDEs detected"
    ["menu_title"]="Installation Options"
    ["menu_all"]="Install to ALL detected IDEs"
    ["menu_select"]="Select specific IDEs"
    ["menu_project"]="Install to current project"
    ["menu_details"]="Show IDE details"
    ["menu_language"]="Change language"
    ["menu_exit"]="Exit"
    ["select_option"]="Select option"
    ["installing_to"]="Installing to"
    ["complete"]="Installation complete!"
    ["files_created"]="Files created"
    ["configured"]="configured"
    ["invalid"]="Invalid option"
    ["press_enter"]="Press Enter to continue..."
    ["goodbye"]="Goodbye!"
)

declare -A STRINGS_VI=(
    ["title"]="Thu Vien DOMYH Awesome Code"
    ["subtitle"]="Tro Ly Phat Trien Voi AI"
    ["select_language"]="Chon Ngon Ngu / Select Language"
    ["english"]="English"
    ["vietnamese"]="Tieng Viet (mac dinh)"
    ["detecting"]="Dang phat hien cac IDE AI..."
    ["no_ides"]="Khong phat hien IDE nao"
    ["menu_title"]="Tuy Chon Cai Dat"
    ["menu_all"]="Cai dat cho TAT CA IDE"
    ["menu_select"]="Chon IDE cu the"
    ["menu_project"]="Cai dat cho du an hien tai"
    ["menu_details"]="Xem chi tiet IDE"
    ["menu_language"]="Doi ngon ngu"
    ["menu_exit"]="Thoat"
    ["select_option"]="Chon tuy chon"
    ["installing_to"]="Dang cai dat vao"
    ["complete"]="Cai dat hoan tat!"
    ["files_created"]="Cac tep da tao"
    ["configured"]="da cau hinh"
    ["invalid"]="Tuy chon khong hop le"
    ["press_enter"]="Nhan Enter de tiep tuc..."
    ["goodbye"]="Tam biet!"
)

t() {
    local key="$1"
    if [ "$LANG_CODE" = "vi" ]; then
        echo "${STRINGS_VI[$key]:-${STRINGS_EN[$key]}}"
    else
        echo "${STRINGS_EN[$key]}"
    fi
}

# ==============================================================================
# UI Functions
# ==============================================================================
show_banner() {
    echo ""
    echo -e "${CYAN}======================================================================${NC}"
    echo -e "${YELLOW}                    $(t title)                    ${NC}"
    echo -e "${NC}              $(t subtitle)              ${NC}"
    echo -e "${GRAY}                      Version $VERSION                        ${NC}"
    echo -e "${GRAY}                   Developed by NockDev                   ${NC}"
    echo -e "${CYAN}======================================================================${NC}"
}

show_language_select() {
    echo ""
    echo -e "${CYAN}======================================================================${NC}"
    echo -e "${YELLOW}         $(t select_language)         ${NC}"
    echo -e "${CYAN}======================================================================${NC}"
    echo ""
    echo "  1) [EN] $(t english)"
    echo "  2) [VI] $(t vietnamese)"
    echo ""
    read -p "Choose / Chon (1-2): " choice
    
    case "$choice" in
        1) LANG_CODE="en" ;;
        2) LANG_CODE="vi" ;;
        *) LANG_CODE="en" ;;
    esac
}

show_help() {
    show_banner
    echo ""
    echo -e "${YELLOW}Usage: ./install.sh [options]${NC}"
    echo ""
    echo -e "${CYAN}Options:${NC}"
    echo "  -h, --help     Show this help message"
    echo "  -a, --all      Install to all detected IDEs"
    echo "  -p, --project  Install to current project"
    echo "  --path PATH    Specify project path"
    echo "  --lang LANG    Set language (en, vi)"
    echo ""
    echo -e "${CYAN}Examples:${NC}"
    echo "  ./install.sh                # Interactive mode"
    echo "  ./install.sh --all          # Install to all IDEs"
    echo "  ./install.sh --project      # Install to current dir"
    echo "  ./install.sh --lang vi -a   # Vietnamese, install all"
    echo ""
}

# ==============================================================================
# IDE Detection
# ==============================================================================
detect_ides() {
    echo ""
    echo -e "${BLUE}[*] $(t detecting)${NC}"
    echo ""
    
    DETECTED_IDES=()
    
    for ide in "${!IDE_PATHS[@]}"; do
        path="${IDE_PATHS[$ide]}"
        name="${IDE_NAMES[$ide]}"
        
        if [ -d "$path" ]; then
            IDE_DETECTED[$ide]=1
            DETECTED_IDES+=("$ide")
            echo -e "  ${GREEN}[OK]${NC} $name ${GRAY}- $path${NC}"
        fi
    done
    
    echo ""
    
    if [ ${#DETECTED_IDES[@]} -eq 0 ]; then
        echo -e "${RED}[X] $(t no_ides)${NC}"
    fi
}

# ==============================================================================
# Installation Functions
# ==============================================================================
install_to_ide() {
    local ide="$1"
    local path="${IDE_PATHS[$ide]}"
    local name="${IDE_NAMES[$ide]}"
    
    # Ensure directory exists
    mkdir -p "$path"
    
    case "$ide" in
        "claude")
            # ~/.claude/CLAUDE.md
            cp "$DOMYH_ROOT/CLAUDE.md" "$path/CLAUDE.md"
            # ~/.claude/skills/
            mkdir -p "$path/skills"
            cp -r "$DOMYH_ROOT/.agent/skills/"* "$path/skills/" 2>/dev/null || true
            ;;
        
        "gemini")
            # ~/.gemini/GEMINI.md
            cp "$DOMYH_ROOT/GEMINI.md" "$path/GEMINI.md"
            # ~/.gemini/skills/
            mkdir -p "$path/skills"
            cp -r "$DOMYH_ROOT/.agent/skills/"* "$path/skills/" 2>/dev/null || true
            ;;
        
        "antigravity")
            # ~/.gemini/antigravity/CLAUDE.md
            cp "$DOMYH_ROOT/CLAUDE.md" "$path/CLAUDE.md"
            # ~/.gemini/antigravity/skills/
            mkdir -p "$path/skills"
            cp -r "$DOMYH_ROOT/.agent/skills/"* "$path/skills/" 2>/dev/null || true
            ;;
        
        "codex")
            # ~/.codex/AGENTS.md
            cp "$DOMYH_ROOT/AGENTS.md" "$path/AGENTS.md"
            ;;
        
        "continue")
            # ~/.continue/rules/
            mkdir -p "$path/rules"
            cp "$DOMYH_ROOT/AGENTS.md" "$path/rules/domyh-rules.md"
            ;;
        
        "augment")
            # ~/.augment/rules/
            mkdir -p "$path/rules"
            cp "$DOMYH_ROOT/AGENTS.md" "$path/rules/domyh-rules.md"
            ;;
        
        "cursor")
            # Project file - info only
            echo -e "  ${YELLOW}[i] Cursor uses project-level .cursorrules file${NC}"
            ;;
        
        "windsurf")
            # ~/.codeium/windsurf/memories/global_rules.md (if exists)
            local memories="$HOME/.codeium/windsurf/memories"
            if [ -d "$memories" ]; then
                cp "$DOMYH_ROOT/AGENTS.md" "$memories/global_rules.md"
            fi
            ;;
        
        "vscode")
            # Project file - info only
            echo -e "  ${YELLOW}[i] VS Code Copilot uses project-level .github/copilot-instructions.md${NC}"
            ;;
        
        "aider")
            # ~/.aider.conf.yml
            cp "$DOMYH_ROOT/.aider.conf.yml" "$HOME/.aider.conf.yml" 2>/dev/null || true
            ;;
        
        *)
            cp "$DOMYH_ROOT/AGENTS.md" "$path/AGENTS.md"
            ;;
    esac
    
    echo -e "  ${GREEN}[OK]${NC} $name $(t configured)"
}

install_to_all() {
    echo ""
    echo -e "${GREEN}[*] $(t installing_to) all detected IDEs...${NC}"
    echo ""
    
    for ide in "${DETECTED_IDES[@]}"; do
        install_to_ide "$ide"
    done
    
    echo ""
    echo -e "${GREEN}[OK] $(t complete)${NC}"
}

install_to_project() {
    local project_path="${1:-$(pwd)}"
    
    echo ""
    echo -e "${BLUE}[*] $(t installing_to) project: $project_path${NC}"
    echo ""
    
    # Create directories
    mkdir -p "$project_path/.agent"
    mkdir -p "$project_path/.github"
    
    # Copy .agent folder
    cp -r "$DOMYH_ROOT/.agent/"* "$project_path/.agent/"
    
    # Copy root config files
    cp "$DOMYH_ROOT/AGENTS.md" "$project_path/"
    cp "$DOMYH_ROOT/CLAUDE.md" "$project_path/"
    cp "$DOMYH_ROOT/GEMINI.md" "$project_path/"
    cp "$DOMYH_ROOT/.cursorrules" "$project_path/"
    cp "$DOMYH_ROOT/.windsurfrules" "$project_path/"
    
    # Copy Copilot instructions
    cp "$DOMYH_ROOT/.github/copilot-instructions.md" "$project_path/.github/"
    
    echo ""
    echo -e "${GREEN}[OK] $(t complete)${NC}"
    echo ""
    echo -e "${YELLOW}$(t files_created):${NC}"
    echo "  - .agent/                           (Agent system)"
    echo "  - AGENTS.md                         (Universal rules)"
    echo "  - CLAUDE.md                         (Claude Code)"
    echo "  - GEMINI.md                         (Gemini CLI)"
    echo "  - .cursorrules                      (Cursor)"
    echo "  - .windsurfrules                    (Windsurf)"
    echo "  - .github/copilot-instructions.md   (GitHub Copilot)"
}

show_ide_details() {
    echo ""
    echo -e "${CYAN}======================================================================${NC}"
    echo -e "${YELLOW}                    IDE Configuration Details                    ${NC}"
    echo -e "${CYAN}======================================================================${NC}"
    echo ""
    
    for ide in $(echo "${!IDE_NAMES[@]}" | tr ' ' '\n' | sort); do
        local name="${IDE_NAMES[$ide]}"
        local path="${IDE_PATHS[$ide]}"
        
        if [ "${IDE_DETECTED[$ide]}" = "1" ]; then
            echo -e "${GREEN}[OK]${NC} $name"
        else
            echo -e "${GRAY}[--] $name${NC}"
        fi
        echo -e "${GRAY}    Path: $path${NC}"
        echo ""
    done
}

show_menu() {
    echo ""
    echo -e "${CYAN}======================================================================${NC}"
    echo -e "${YELLOW}[?] $(t menu_title):${NC}"
    echo ""
    echo "  1) [GLOBAL] $(t menu_all)"
    echo "  2) [SELECT] $(t menu_select)"
    echo "  3) [PROJECT] $(t menu_project)"
    echo "  4) [INFO] $(t menu_details)"
    echo "  5) [LANG] $(t menu_language)"
    echo "  6) [EXIT] $(t menu_exit)"
    echo ""
}

# ==============================================================================
# Parse Arguments
# ==============================================================================
INSTALL_ALL=0
INSTALL_PROJECT=0
PROJECT_PATH=""

while [[ $# -gt 0 ]]; do
    case "$1" in
        -h|--help)
            show_help
            exit 0
            ;;
        -a|--all)
            INSTALL_ALL=1
            shift
            ;;
        -p|--project)
            INSTALL_PROJECT=1
            shift
            ;;
        --path)
            PROJECT_PATH="$2"
            shift 2
            ;;
        --lang)
            LANG_CODE="$2"
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# ==============================================================================
# Main Entry Point
# ==============================================================================

# Show banner
show_banner

# Language selection if not specified via args
if [ -z "$LANG_CODE" ] || [ "$LANG_CODE" = "" ]; then
    LANG_CODE="en"
fi

if [ "$INSTALL_ALL" -eq 0 ] && [ "$INSTALL_PROJECT" -eq 0 ]; then
    show_language_select
    show_banner
fi

# Detect IDEs
detect_ides

# Handle command-line modes
if [ "$INSTALL_ALL" -eq 1 ]; then
    install_to_all
    exit 0
fi

if [ "$INSTALL_PROJECT" -eq 1 ]; then
    if [ -n "$PROJECT_PATH" ]; then
        install_to_project "$PROJECT_PATH"
    else
        install_to_project "$(pwd)"
    fi
    exit 0
fi

# Interactive mode
while true; do
    show_menu
    read -p "$(t select_option) (1-6): " choice
    
    case "$choice" in
        1)
            install_to_all
            read -p "$(t press_enter)"
            ;;
        2)
            echo ""
            echo -e "${YELLOW}Available IDEs:${NC}"
            i=1
            for ide in "${DETECTED_IDES[@]}"; do
                echo "  $i) ${IDE_NAMES[$ide]}"
                ((i++))
            done
            echo ""
            read -p "Enter numbers (comma-separated): " selection
            IFS=',' read -ra indices <<< "$selection"
            for idx in "${indices[@]}"; do
                idx=$((idx - 1))
                if [ $idx -ge 0 ] && [ $idx -lt ${#DETECTED_IDES[@]} ]; then
                    install_to_ide "${DETECTED_IDES[$idx]}"
                fi
            done
            read -p "$(t press_enter)"
            ;;
        3)
            read -p "Enter project path (or Enter for current): " project_path
            if [ -z "$project_path" ]; then
                install_to_project "$(pwd)"
            else
                install_to_project "$project_path"
            fi
            read -p "$(t press_enter)"
            ;;
        4)
            show_ide_details
            read -p "$(t press_enter)"
            ;;
        5)
            show_language_select
            show_banner
            detect_ides
            ;;
        6)
            echo ""
            echo -e "${CYAN}$(t goodbye)${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}[X] $(t invalid)${NC}"
            ;;
    esac
done

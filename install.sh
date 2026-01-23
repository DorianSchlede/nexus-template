#!/bin/bash
#
# Nexus One-Command Installer
# Install Claude Code, uv, Git, and Nexus template in one command
#
# Usage:
#   curl -fsSL https://raw.githubusercontent.com/DorianSchlede/nexus-template/main/install.sh | bash
#

set -e  # Exit on error

# ============================================================================
# COLORS & OUTPUT
# ============================================================================

if [ -t 1 ]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    BOLD='\033[1m'
    RESET='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    BOLD=''
    RESET=''
fi

info() {
    echo -e "${BLUE}ℹ${RESET} $1"
}

success() {
    echo -e "${GREEN}✓${RESET} $1"
}

warning() {
    echo -e "${YELLOW}⚠${RESET} $1"
}

error() {
    echo -e "${RED}✗${RESET} $1"
}

header() {
    echo ""
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo -e "${BOLD}$1${RESET}"
    echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
    echo ""
}

# ============================================================================
# PLATFORM DETECTION
# ============================================================================

detect_platform() {
    OS=$(uname -s)
    ARCH=$(uname -m)

    case "$OS" in
        Linux*)     PLATFORM="Linux" ;;
        Darwin*)    PLATFORM="macOS" ;;
        MINGW*|MSYS*|CYGWIN*)  PLATFORM="Windows" ;;
        *)          PLATFORM="Unknown" ;;
    esac

    info "Platform: $PLATFORM ($ARCH)"
}

# ============================================================================
# TOOL CHECKS
# ============================================================================

PATH_UPDATED=false

check_tool() {
    local tool=$1
    local name=$2

    if command -v "$tool" &> /dev/null; then
        success "$name is already installed"
        return 0
    else
        warning "$name is not installed"
        return 1
    fi
}

# ============================================================================
# INSTALLATIONS
# ============================================================================

install_claude_code() {
    header "Installing Claude Code"

    if check_tool "claude" "Claude Code"; then
        return 0
    fi

    info "Downloading and installing Claude Code..."

    # Call official installer
    if curl -fsSL https://claude.ai/install.sh | bash; then
        PATH_UPDATED=true

        # Verify installation
        if command -v claude &> /dev/null; then
            success "Claude Code installed successfully"
        else
            warning "Claude Code installed but not in PATH yet (restart terminal after installation)"
        fi
    else
        error "Failed to install Claude Code"
        return 1
    fi
}

install_uv() {
    header "Installing uv"

    if check_tool "uv" "uv"; then
        return 0
    fi

    info "Downloading and installing uv..."

    # Call official installer
    if curl -LsSf https://astral.sh/uv/install.sh | sh; then
        PATH_UPDATED=true

        # Verify installation
        if command -v uv &> /dev/null; then
            success "uv installed successfully"
        else
            warning "uv installed but not in PATH yet (restart terminal after installation)"
        fi
    else
        error "Failed to install uv"
        return 1
    fi
}

install_git() {
    header "Installing Git"

    if check_tool "git" "Git"; then
        return 0
    fi

    info "Installing Git..."

    case "$PLATFORM" in
        macOS)
            # macOS: Check if Xcode Command Line Tools installed
            if xcode-select -p &> /dev/null; then
                success "Git available via Xcode Command Line Tools"
            else
                info "Installing Xcode Command Line Tools (includes Git)..."
                xcode-select --install
                warning "Please complete the Xcode Command Line Tools installation and re-run this script"
                exit 1
            fi
            ;;
        Linux)
            # Linux: Try package manager
            if command -v apt-get &> /dev/null; then
                info "Using apt-get to install Git..."
                sudo apt-get update && sudo apt-get install -y git
            elif command -v yum &> /dev/null; then
                info "Using yum to install Git..."
                sudo yum install -y git
            elif command -v dnf &> /dev/null; then
                info "Using dnf to install Git..."
                sudo dnf install -y git
            elif command -v pacman &> /dev/null; then
                info "Using pacman to install Git..."
                sudo pacman -S --noconfirm git
            else
                error "No supported package manager found. Please install Git manually."
                return 1
            fi
            success "Git installed successfully"
            ;;
        Windows)
            # Git Bash on Windows - should already have Git
            if check_tool "git" "Git"; then
                success "Git is available"
            else
                error "Git Bash should include Git. Please install Git for Windows manually."
                return 1
            fi
            ;;
        *)
            error "Unsupported platform: $PLATFORM"
            return 1
            ;;
    esac
}

# ============================================================================
# VS CODE PROMPT
# ============================================================================

prompt_vscode() {
    header "VS Code Installation"

    if command -v code &> /dev/null; then
        success "VS Code is already installed"
        VSCODE_INSTALLED=true
        return 0
    fi

    echo "Do you want to install VS Code?"
    echo ""
    echo "  1. Yes - Install VS Code"
    echo "  2. No - Skip VS Code"
    echo ""
    read -p "Your choice (1 or 2): " vscode_choice

    case "$vscode_choice" in
        1|yes|y|Y)
            install_vscode
            ;;
        2|no|n|N)
            info "Skipping VS Code installation"
            VSCODE_INSTALLED=false
            ;;
        *)
            warning "Invalid choice. Skipping VS Code installation"
            VSCODE_INSTALLED=false
            ;;
    esac
}

install_vscode() {
    info "Opening VS Code download page..."

    case "$PLATFORM" in
        macOS)
            open "https://code.visualstudio.com/download"
            ;;
        Linux)
            xdg-open "https://code.visualstudio.com/download" 2>/dev/null || info "Please visit: https://code.visualstudio.com/download"
            ;;
        *)
            info "Please visit: https://code.visualstudio.com/download"
            ;;
    esac

    warning "Please install VS Code and re-run this script to complete setup"
    VSCODE_INSTALLED=false
}

# ============================================================================
# NEXUS CLONE
# ============================================================================

clone_nexus() {
    header "Cloning Nexus Template"

    echo "Where do you want to install Nexus?"
    echo ""
    read -p "Directory path (default: $HOME/nexus): " nexus_dir

    if [ -z "$nexus_dir" ]; then
        nexus_dir="$HOME/nexus"
    fi

    # Expand ~ to $HOME
    nexus_dir="${nexus_dir/#\~/$HOME}"

    # Check if directory exists
    if [ -d "$nexus_dir" ]; then
        error "Directory $nexus_dir already exists"
        read -p "Do you want to remove it and clone fresh? (y/N): " confirm
        case "$confirm" in
            y|Y)
                rm -rf "$nexus_dir"
                ;;
            *)
                warning "Skipping Nexus clone"
                return 1
                ;;
        esac
    fi

    info "Cloning Nexus to $nexus_dir..."

    if git clone https://github.com/DorianSchlede/nexus-template.git "$nexus_dir"; then
        success "Nexus cloned successfully to $nexus_dir"
        NEXUS_DIR="$nexus_dir"
        return 0
    else
        error "Failed to clone Nexus"
        return 1
    fi
}

# ============================================================================
# VS CODE LAUNCH
# ============================================================================

launch_vscode() {
    if [ "$VSCODE_INSTALLED" = true ] && [ -n "$NEXUS_DIR" ]; then
        header "Opening VS Code"

        if command -v code &> /dev/null; then
            info "Opening $NEXUS_DIR in VS Code..."
            code "$NEXUS_DIR"
            success "VS Code opened"
        else
            warning "VS Code command not found. Please open $NEXUS_DIR manually."
        fi
    fi
}

# ============================================================================
# SUMMARY
# ============================================================================

show_summary() {
    header "Installation Summary"

    echo ""
    echo -e "${BOLD}Installed:${RESET}"

    if command -v claude &> /dev/null; then
        echo -e "  ${GREEN}✓${RESET} Claude Code"
    else
        echo -e "  ${YELLOW}⚠${RESET} Claude Code (not in PATH)"
    fi

    if command -v uv &> /dev/null; then
        echo -e "  ${GREEN}✓${RESET} uv"
    else
        echo -e "  ${YELLOW}⚠${RESET} uv (not in PATH)"
    fi

    if command -v git &> /dev/null; then
        echo -e "  ${GREEN}✓${RESET} Git"
    else
        echo -e "  ${RED}✗${RESET} Git"
    fi

    if [ "$VSCODE_INSTALLED" = true ]; then
        echo -e "  ${GREEN}✓${RESET} VS Code"
    fi

    if [ -n "$NEXUS_DIR" ]; then
        echo -e "  ${GREEN}✓${RESET} Nexus Template (${NEXUS_DIR})"
    fi

    echo ""

    # PATH warning
    if [ "$PATH_UPDATED" = true ]; then
        echo -e "${BOLD}${YELLOW}⚠  PATH was updated during installation${RESET}"
        echo ""
        echo "Choose one option to apply changes:"
        echo ""
        echo "  ${BOLD}1. Quick${RESET} (current session only):"

        # Detect shell config file
        if [ -n "$ZSH_VERSION" ]; then
            echo "     source ~/.zshrc"
        elif [ -n "$BASH_VERSION" ]; then
            echo "     source ~/.bashrc"
        else
            echo "     source ~/.profile"
        fi

        echo ""
        echo "  ${BOLD}2. Reliable${RESET} (all sessions):"
        echo "     Restart your terminal"
        echo ""
        echo -e "${BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${RESET}"
        echo ""
    fi

    # Next steps
    echo -e "${BOLD}Next Steps:${RESET}"
    echo ""

    if [ "$PATH_UPDATED" = true ]; then
        echo "  1. Restart your terminal (or source your shell config)"
    fi

    if [ -n "$NEXUS_DIR" ]; then
        echo "  2. cd $NEXUS_DIR"
        echo "  3. claude"
    else
        echo "  1. Clone Nexus: git clone https://github.com/DorianSchlede/nexus-template.git"
        echo "  2. cd nexus-template"
        echo "  3. claude"
    fi

    echo ""
    success "Installation complete!"
    echo ""
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    clear

    echo ""
    echo -e "${BOLD}    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗${RESET}"
    echo -e "${BOLD}    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝${RESET}"
    echo -e "${BOLD}    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗${RESET}"
    echo -e "${BOLD}    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║${RESET}"
    echo -e "${BOLD}    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║${RESET}"
    echo -e "${BOLD}    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝${RESET}"
    echo ""
    echo -e "${BOLD}         One-Command Installer${RESET}"
    echo ""

    detect_platform

    # Install tools
    install_claude_code
    install_uv
    install_git

    # VS Code prompt
    prompt_vscode

    # Clone Nexus
    clone_nexus

    # Launch VS Code if installed
    launch_vscode

    # Show summary
    show_summary
}

# Run main
main

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
    echo -e "${BLUE}[INFO]${RESET} $1"
}

success() {
    echo -e "${GREEN}[OK]${RESET} $1"
}

warning() {
    echo -e "${YELLOW}[!]${RESET} $1"
}

error() {
    echo -e "${RED}[FAIL]${RESET} $1"
}

header() {
    echo ""
    echo -e "${BOLD}------------------------------------${RESET}"
    echo -e "${BOLD}$1${RESET}"
    echo -e "${BOLD}------------------------------------${RESET}"
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

# NOTE: Git installation removed - we use ZIP download instead of git clone
# This means no Git dependency for installation

# ============================================================================
# VS CODE INSTALLATION
# ============================================================================

install_vscode() {
    header "Installing VS Code"

    if command -v code &> /dev/null; then
        success "VS Code is already installed"
        return 0
    fi

    warning "VS Code is not installed"

    case "$PLATFORM" in
        macOS)
            # Try Homebrew first
            if command -v brew &> /dev/null; then
                info "Installing VS Code via Homebrew..."
                if brew install --cask visual-studio-code; then
                    success "VS Code installed successfully"
                    return 0
                fi
            fi

            # Fallback: direct download
            info "Downloading VS Code directly..."
            local tmp_dir=$(mktemp -d)
            local zip_file="$tmp_dir/VSCode.zip"
            local app_path="/Applications/Visual Studio Code.app"

            if curl -fsSL "https://code.visualstudio.com/sha/download?build=stable&os=darwin-universal" -o "$zip_file"; then
                info "Extracting VS Code..."
                unzip -q "$zip_file" -d "$tmp_dir"
                mv "$tmp_dir/Visual Studio Code.app" "$app_path"
                rm -rf "$tmp_dir"

                # Add code command to PATH
                if [ -f "$app_path/Contents/Resources/app/bin/code" ]; then
                    mkdir -p /usr/local/bin 2>/dev/null || true
                    ln -sf "$app_path/Contents/Resources/app/bin/code" /usr/local/bin/code 2>/dev/null || true
                fi

                success "VS Code installed to /Applications"
                return 0
            fi
            ;;

        Linux)
            # Try snap (most universal)
            if command -v snap &> /dev/null; then
                info "Installing VS Code via snap..."
                if sudo snap install code --classic; then
                    success "VS Code installed successfully"
                    return 0
                fi
            fi

            # Try apt (Debian/Ubuntu)
            if command -v apt &> /dev/null; then
                info "Installing VS Code via apt..."
                curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | sudo gpg --dearmor -o /usr/share/keyrings/packages.microsoft.gpg 2>/dev/null
                echo "deb [arch=amd64 signed-by=/usr/share/keyrings/packages.microsoft.gpg] https://packages.microsoft.com/repos/code stable main" | sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
                if sudo apt update && sudo apt install -y code; then
                    success "VS Code installed successfully"
                    return 0
                fi
            fi
            ;;
    esac

    # Final fallback: manual
    error "Could not install VS Code automatically"
    info "Please install VS Code manually from: https://code.visualstudio.com/download"

    case "$PLATFORM" in
        macOS)
            open "https://code.visualstudio.com/download"
            ;;
        Linux)
            xdg-open "https://code.visualstudio.com/download" 2>/dev/null || true
            ;;
    esac

    return 1
}

# ============================================================================
# NEXUS DOWNLOAD (ZIP - no Git required)
# ============================================================================

NEXUS_REPO_URL="https://github.com/DorianSchlede/nexus-template"
NEXUS_ZIP_URL="$NEXUS_REPO_URL/archive/refs/heads/main.zip"

download_nexus() {
    header "Downloading Nexus"

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
        read -p "Do you want to remove it and start fresh? (y/N): " confirm
        case "$confirm" in
            y|Y)
                rm -rf "$nexus_dir"
                ;;
            *)
                warning "Skipping Nexus download"
                return 1
                ;;
        esac
    fi

    # Create temp directory for download
    local tmp_dir=$(mktemp -d)
    local zip_file="$tmp_dir/nexus.zip"

    info "Downloading Nexus from GitHub..."

    # Download ZIP (no Git required, no auth required)
    if curl -fsSL "$NEXUS_ZIP_URL" -o "$zip_file"; then
        success "Downloaded Nexus archive"
    else
        error "Failed to download Nexus"
        rm -rf "$tmp_dir"
        return 1
    fi

    info "Extracting..."

    # Extract ZIP
    if command -v unzip &> /dev/null; then
        unzip -q "$zip_file" -d "$tmp_dir"
    else
        # Fallback: try Python's zipfile
        python3 -c "import zipfile; zipfile.ZipFile('$zip_file').extractall('$tmp_dir')"
    fi

    # Move extracted folder to destination
    # GitHub ZIP extracts to nexus-template-main/
    mkdir -p "$(dirname "$nexus_dir")"
    mv "$tmp_dir/nexus-template-main" "$nexus_dir"

    # Cleanup
    rm -rf "$tmp_dir"

    success "Nexus installed to $nexus_dir"
    NEXUS_DIR="$nexus_dir"
    return 0
}

# NOTE: Claude settings (permission bypass) and VS Code settings (markdown preview)
# are now configured interactively via Claude chat after installation.
# See /setup skill for the interactive configuration workflow.

# ============================================================================
# INSTALL NEXUS CLI
# ============================================================================

install_nexus_cli() {
    header "Installing Nexus CLI Tools"

    if [ -z "$NEXUS_DIR" ]; then
        warning "Nexus not cloned, skipping CLI installation"
        return 1
    fi

    # Refresh PATH to pick up newly installed uv
    # Add common uv/cargo install locations
    export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

    # Verify uv is now available
    if ! command -v uv &> /dev/null; then
        warning "uv not found in PATH after refresh"
        info "You can install CLI tools manually later: cd $NEXUS_DIR && uv tool install ."
        return 1
    fi

    info "Installing Nexus CLI tools globally..."

    # Install the nexus-cli package as a tool
    if (cd "$NEXUS_DIR" && uv tool install . --force) 2>&1; then
        success "Nexus CLI tools installed"
    else
        warning "Failed to install Nexus CLI tools"
        info "You can install manually later: cd $NEXUS_DIR && uv tool install ."
    fi
}

# ============================================================================
# CLAUDE EXTENSION INSTALLATION
# ============================================================================

install_claude_extension() {
    header "Installing Claude Extension"

    if ! command -v code &> /dev/null; then
        warning "VS Code not found, skipping extension installation"
        return 1
    fi

    info "Installing Claude extension for VS Code..."

    if code --install-extension anthropic.claude-code --force 2>/dev/null; then
        success "Claude extension installed"
    else
        warning "Failed to install Claude extension"
        info "You can install it manually from the VS Code Extensions marketplace"
    fi
}

# ============================================================================
# VS CODE LAUNCH
# ============================================================================

launch_vscode() {
    if [ -n "$NEXUS_DIR" ]; then
        header "Opening VS Code"

        if command -v code &> /dev/null; then
            info "Opening $NEXUS_DIR in VS Code..."
            code "$NEXUS_DIR"
            success "VS Code opened - click the Claude icon in the sidebar and say 'hi'!"
        else
            warning "VS Code command not found."
            info "Please open VS Code manually and open the folder: $NEXUS_DIR"
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
        echo -e "  ${GREEN}[OK]${RESET} Claude Code"
    else
        echo -e "  ${YELLOW}[!]${RESET} Claude Code (not in PATH)"
    fi

    if command -v uv &> /dev/null; then
        echo -e "  ${GREEN}[OK]${RESET} uv"
    else
        echo -e "  ${YELLOW}[!]${RESET} uv (not in PATH)"
    fi

    if command -v code &> /dev/null; then
        echo -e "  ${GREEN}[OK]${RESET} VS Code"
    fi

    if [ -n "$NEXUS_DIR" ]; then
        echo -e "  ${GREEN}[OK]${RESET} Nexus Template (${NEXUS_DIR})"
    fi

    echo ""

    # PATH warning
    if [ "$PATH_UPDATED" = true ]; then
        echo -e "${BOLD}${YELLOW}[!]  PATH was updated during installation${RESET}"
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
        echo -e "${BOLD}------------------------------------${RESET}"
        echo ""
    fi

    # Next steps
    echo -e "${BOLD}Next Steps:${RESET}"
    echo ""

    if command -v code &> /dev/null && [ -n "$NEXUS_DIR" ]; then
        echo "  VS Code should have opened automatically."
        echo ""
        echo "  1. Click the Claude icon in the sidebar"
        echo "  2. Say 'hi'"
        echo "  3. Claude will guide you from there!"
    else
        echo "  1. Open VS Code"
        echo "  2. Open the folder: $NEXUS_DIR"
        echo "  3. Click the Claude icon in the sidebar"
        echo "  4. Say 'hi'"
    fi

    echo ""
    success "Installation complete! Enjoy Nexus!"
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

    # Install VS Code (if not already installed)
    if ! install_vscode; then
        warning "VS Code is required. Please install it and re-run this installer."
        exit 1
    fi

    # Download Nexus (ZIP - no Git required)
    download_nexus

    # Install Nexus CLI tools
    install_nexus_cli

    # Install Claude extension for VS Code
    install_claude_extension

    # Launch VS Code
    launch_vscode

    # Show summary
    show_summary
}

# Run main
main

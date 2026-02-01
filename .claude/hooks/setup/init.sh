#!/bin/bash
#
# Nexus Setup Init Script
# Runs when: claude --init
# Purpose: Install dependencies and set up the codebase
#

set -e

# ============================================================================
# CONFIG
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
LOG_FILE="$PROJECT_DIR/.claude/logs/install.log"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

# ============================================================================
# LOGGING
# ============================================================================

log() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" | tee -a "$LOG_FILE"
}

log_section() {
    echo "" | tee -a "$LOG_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
    echo "$1" | tee -a "$LOG_FILE"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" | tee -a "$LOG_FILE"
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

run() {
    log "Running: $1"
    if eval "$1" >> "$LOG_FILE" 2>&1; then
        log "[OK] Success: $1"
        return 0
    else
        log "[FAIL] Failed: $1"
        return 1
    fi
}

check_command() {
    if command -v "$1" &> /dev/null; then
        log "[OK] Found: $1"
        return 0
    else
        log "[FAIL] Missing: $1"
        return 1
    fi
}

# ============================================================================
# MAIN INSTALLATION
# ============================================================================

main() {
    # Clear previous log
    echo "" > "$LOG_FILE"

    log_section "NEXUS INSTALLATION STARTED"
    log "Project directory: $PROJECT_DIR"
    log "Log file: $LOG_FILE"

    # Check prerequisites
    log_section "CHECKING PREREQUISITES"

    local prereqs_ok=true

    if ! check_command "python3"; then
        prereqs_ok=false
    fi

    if ! check_command "uv"; then
        prereqs_ok=false
    fi

    # Note: git is optional - Nexus can be installed via ZIP download
    if check_command "git"; then
        log "[OK] Found: git (optional)"
    else
        log "[INFO] git not found (optional - Nexus works without it)"
    fi

    if [ "$prereqs_ok" = false ]; then
        log "Some prerequisites are missing. See log for details."
    fi

    # Install Python dependencies
    log_section "INSTALLING PYTHON DEPENDENCIES"

    cd "$PROJECT_DIR"

    if [ -f "pyproject.toml" ]; then
        run "uv sync"
    else
        log "No pyproject.toml found, skipping Python dependencies"
    fi

    # Install Nexus CLI tools
    log_section "INSTALLING NEXUS CLI TOOLS"

    if [ -f "pyproject.toml" ]; then
        run "uv tool install . --force" || log "CLI tools installation optional"
    fi

    # Verify core files exist
    log_section "VERIFYING NEXUS STRUCTURE"

    local structure_ok=true

    if [ -f "$PROJECT_DIR/00-system/core/orchestrator.md" ]; then
        log "[OK] Orchestrator found"
    else
        log "[FAIL] Orchestrator missing"
        structure_ok=false
    fi

    if [ -d "$PROJECT_DIR/01-memory" ]; then
        log "[OK] Memory directory found"
    else
        log "[FAIL] Memory directory missing"
        structure_ok=false
    fi

    if [ -d "$PROJECT_DIR/02-builds" ]; then
        log "[OK] Builds directory found"
    else
        log "[FAIL] Builds directory missing"
        structure_ok=false
    fi

    # Summary
    log_section "INSTALLATION SUMMARY"

    if [ "$prereqs_ok" = true ] && [ "$structure_ok" = true ]; then
        log "STATUS: SUCCESS"
        log "Nexus is ready to use."
    else
        log "STATUS: PARTIAL"
        log "Some components may need attention. Review the log above."
    fi

    log ""
    log "Run 'just cli' or 'claude' to start Nexus."
    log "Run 'just install' for agentic validation of this installation."
}

# Run main
main "$@"

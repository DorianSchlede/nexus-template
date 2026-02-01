#!/bin/bash
#
# Nexus Maintenance Script
# Runs when: claude --maintenance
# Purpose: Update dependencies, clean artifacts, run health checks
#

set -e

# ============================================================================
# CONFIG
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/../../.." && pwd)"
LOG_FILE="$PROJECT_DIR/.claude/logs/maintenance.log"

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

# ============================================================================
# MAINTENANCE TASKS
# ============================================================================

main() {
    # Clear previous log
    echo "" > "$LOG_FILE"

    log_section "NEXUS MAINTENANCE STARTED"
    log "Project directory: $PROJECT_DIR"
    log "Log file: $LOG_FILE"

    cd "$PROJECT_DIR"

    # Update Python dependencies
    log_section "UPDATING DEPENDENCIES"

    if [ -f "pyproject.toml" ]; then
        run "uv sync"
        run "uv tool install . --force" || log "CLI tools update optional"
    fi

    # Clean temporary files
    log_section "CLEANING ARTIFACTS"

    # Clean Python cache
    if [ -d "__pycache__" ]; then
        run "find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true"
        log "Cleaned Python cache directories"
    fi

    # Clean .pyc files
    run "find . -type f -name '*.pyc' -delete 2>/dev/null || true"
    log "Cleaned .pyc files"

    # Clean old session files (older than 7 days)
    if [ -d ".claude/sessions" ]; then
        local old_sessions=$(find .claude/sessions -type f -mtime +7 2>/dev/null | wc -l)
        if [ "$old_sessions" -gt 0 ]; then
            run "find .claude/sessions -type f -mtime +7 -delete 2>/dev/null || true"
            log "Cleaned $old_sessions old session files"
        else
            log "No old session files to clean"
        fi
    fi

    # Health checks
    log_section "HEALTH CHECKS"

    # Check disk space
    local disk_usage=$(df -h "$PROJECT_DIR" | awk 'NR==2 {print $5}' | tr -d '%')
    if [ "$disk_usage" -gt 90 ]; then
        log "[!] Warning: Disk usage is at ${disk_usage}%"
    else
        log "[OK] Disk usage: ${disk_usage}%"
    fi

    # Check git status
    if git status --porcelain > /dev/null 2>&1; then
        local uncommitted=$(git status --porcelain | wc -l)
        if [ "$uncommitted" -gt 0 ]; then
            log "[!] $uncommitted uncommitted changes"
        else
            log "[OK] Working directory clean"
        fi
    fi

    # Check for outdated dependencies
    log_section "DEPENDENCY STATUS"

    if command -v uv &> /dev/null; then
        # Just log that we synced, uv doesn't have a built-in outdated check
        log "[OK] Python dependencies synced via uv"
    fi

    # Summary
    log_section "MAINTENANCE SUMMARY"

    log "STATUS: COMPLETE"
    log "Last maintenance: $(date '+%Y-%m-%d %H:%M:%S')"
    log ""
    log "Run 'just maintain' for agentic validation of maintenance."
}

# Run main
main "$@"

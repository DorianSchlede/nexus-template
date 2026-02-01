#!/bin/bash
#
# Cross-platform setup hook runner
# Detects OS and runs the appropriate script
#
# Usage: run-setup.sh [init|maintenance]
#

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MODE="${1:-init}"

# Detect platform
case "$(uname -s)" in
    Darwin*|Linux*)
        # Unix-like: run bash script
        if [ "$MODE" = "maintenance" ]; then
            "$SCRIPT_DIR/maintenance.sh"
        else
            "$SCRIPT_DIR/init.sh"
        fi
        ;;
    MINGW*|MSYS*|CYGWIN*)
        # Windows via Git Bash/MSYS
        if [ "$MODE" = "maintenance" ]; then
            "$SCRIPT_DIR/maintenance.sh"
        else
            "$SCRIPT_DIR/init.sh"
        fi
        ;;
    *)
        echo "Unknown platform: $(uname -s)"
        exit 1
        ;;
esac

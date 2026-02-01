# Nexus Command Runner
# A minimalist launchpad for Nexus commands and agents
#
# Usage: just <command>
# List all commands: just

# Default: show available commands
default:
    @just --list

# ============================================================================
# INSTALLATION & MAINTENANCE
# ============================================================================

# Initialize codebase (runs setup hook + agentic validation)
install:
    claude --init -p "/install"

# Initialize with interactive mode (human-in-the-loop)
install-interactive:
    claude --init -p "/install --interactive"

# Run codebase maintenance (updates, cleanup, health checks)
maintain:
    claude --maintenance -p "/maintain"

# Run maintenance with interactive mode
maintain-interactive:
    claude --maintenance -p "/maintain --interactive"

# ============================================================================
# QUICK CLAUDE COMMANDS
# ============================================================================

# Start Claude Code in this directory
cli:
    claude

# Start Claude with init hook only (no prompt)
init:
    claude --init

# Start Claude with maintenance hook only (no prompt)
maintenance:
    claude --maintenance

# Resume last session
resume:
    claude --resume

# ============================================================================
# NEXUS SKILLS
# ============================================================================

# Prime Claude with codebase context
prime:
    claude -p "/prime"

# Show Nexus main menu
menu:
    claude -p "/menu"

# List all available skills
skills:
    claude -p "/skills"

# Start a new build
build:
    claude -p "/build"

# ============================================================================
# DEVELOPMENT
# ============================================================================

# Run Python tests
test:
    uv run pytest

# Sync Python dependencies
sync:
    uv sync

# Install Nexus CLI tools globally
install-cli:
    uv tool install . --force

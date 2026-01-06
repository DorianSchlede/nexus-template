"""CLI scripts for dynamic subagent system.

Scripts:
    generate_dynamic_research_subagent.py
        Main entry point for generating task-specific subagent prompts.
        Creates prompts with domain personas, forced reading contracts,
        and exact output schemas.

    verify_subagent_reading.py
        Post-execution verification that subagent actually read everything.
        Checks 3-point evidence, hash verification, spot checks.

    handover_manager.py
        Structured handover protocol implementation.
        Creates tickets, generates prompts, verifies completion receipts.
"""

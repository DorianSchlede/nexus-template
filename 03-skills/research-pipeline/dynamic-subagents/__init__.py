"""Dynamic Subagent System for Research Pipeline.

HIGH QUALITY DATA TRANSFER through FORCED COMPLETE READING.

Structure:
    core/
        dynamic_subagent_factory.py  - Domain personas and task templates
        forced_reading_contract.py   - Anti-skimming mechanisms

    scripts/
        generate_dynamic_research_subagent.py  - Main prompt generator
        verify_subagent_reading.py             - Post-execution verification
        handover_manager.py                    - Structured handover protocol

    docs/
        README.md                        - System documentation
        ULTRASEARCH_HANDOVER_PATTERNS.md - Handover protocol patterns

Usage:
    # Generate prompt for paper analysis
    python scripts/generate_dynamic_research_subagent.py \\
        02-projects/02-ontologies-research \\
        paper_analysis \\
        --paper-id 02-Knowledge_Graphs

    # Verify subagent reading
    python scripts/verify_subagent_reading.py \\
        02-projects/02-ontologies-research \\
        --paper-id 02-Knowledge_Graphs

    # Create handover ticket
    python scripts/handover_manager.py create \\
        02-projects/02-ontologies-research \\
        paper_analysis \\
        --paper-id 02-Knowledge_Graphs \\
        --output ticket.yaml
"""

__version__ = "1.0.0"
__author__ = "Research Pipeline"

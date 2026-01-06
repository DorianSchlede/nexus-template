"""Core components for dynamic subagent generation."""

from .dynamic_subagent_factory import (
    DOMAIN_REGISTRY,
    TASK_METHODOLOGIES,
    detect_domain,
    generate_input_contract,
    generate_output_schema,
    generate_subagent_prompt,
    SubagentPrompt,
    InputContract,
    OutputSchema
)

from .forced_reading_contract import (
    generate_forced_reading_contract,
    generate_anti_skimming_prompt,
    generate_chunk_processing_instructions,
    generate_reading_verification_checklist,
    extract_reading_proof,
    validate_reading_proof,
    ReadingProof
)

__all__ = [
    # Factory
    'DOMAIN_REGISTRY',
    'TASK_METHODOLOGIES',
    'detect_domain',
    'generate_input_contract',
    'generate_output_schema',
    'generate_subagent_prompt',
    'SubagentPrompt',
    'InputContract',
    'OutputSchema',

    # Forced Reading
    'generate_forced_reading_contract',
    'generate_anti_skimming_prompt',
    'generate_chunk_processing_instructions',
    'generate_reading_verification_checklist',
    'extract_reading_proof',
    'validate_reading_proof',
    'ReadingProof'
]

"""
Shared Constants for Research Pipeline

This file is the SINGLE SOURCE OF TRUTH for values used across multiple skills.
Import from here instead of defining locally to prevent drift.

Usage:
    from constants import TOKEN_FORMULA, SCHEMA_VERSION
"""

# Token estimation formula
# Used by: paper-analyze-core, generate_paper_corpus, build_synthesis_routing
# Formula: characters divided by 4 (standard approximation)
TOKEN_FORMULA = lambda chars: chars // 4

# Alternative: chars / 5 * 1.3 (more conservative)
# TOKEN_FORMULA_CONSERVATIVE = lambda chars: int(chars / 5 * 1.3)

# Current schema version
SCHEMA_VERSION = "2.3"

# Maximum tokens per subagent batch
MAX_TOKENS_PER_BATCH = 70000

# Maximum concurrent subagents
MAX_CONCURRENT_SUBAGENTS = 15

# Timeout per paper (seconds)
TIMEOUT_PER_PAPER = 300  # 5 minutes

# Sparsity warning threshold (Gap G19)
SPARSITY_THRESHOLD = 0.80  # Warn if field matches >80% of chunks

# Field states for chunk_index.fields_found
FIELD_STATE_TRUE = True      # Extractable content present
FIELD_STATE_PARTIAL = "partial"  # Mentioned but not detailed
FIELD_STATE_FALSE = False    # Not present in chunk

# Verification sample rate (Level 5)
VERIFICATION_SAMPLE_RATE = 0.10  # 10% of patterns

# Verification pass threshold
VERIFICATION_PASS_THRESHOLD = 0.90  # 90% must verify

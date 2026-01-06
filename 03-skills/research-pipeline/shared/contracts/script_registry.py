#!/usr/bin/env python3
"""
Script Registry - Documentation for all research pipeline scripts.

This module provides structured documentation about each script in the pipeline,
including what it does, inputs, outputs, and usage examples.

Used by visualize_pipeline.py to add depth to the workflow visualization.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional

@dataclass
class ScriptDoc:
    """Documentation for a single script."""
    name: str
    path: str
    purpose: str  # One-line purpose
    description: str  # Full description
    level: Optional[int]  # 7-level architecture level (1-7 or None)
    inputs: List[Dict[str, str]] = field(default_factory=list)  # [{path, description}]
    outputs: List[Dict[str, str]] = field(default_factory=list)  # [{path, description}]
    usage: str = ""
    key_features: List[str] = field(default_factory=list)


# ============================================================================
# SCRIPT REGISTRY
# ============================================================================

SCRIPT_REGISTRY: Dict[str, ScriptDoc] = {

    # =========================================================================
    # PAPER SEARCH & DOWNLOAD
    # =========================================================================

    "paper_search.py": ScriptDoc(
        name="paper_search.py",
        path="skills/paper-search/scripts/paper_search.py",
        purpose="Search and download academic papers from 9 open access APIs",
        description="""
Multi-source academic paper search engine. Queries Semantic Scholar (200M+ papers),
OpenAlex (250M+ works), arXiv (2M+ preprints), CrossRef (130M+ DOIs), PubMed (35M+
biomedical), CORE (300M+ full-text), BASE (300M+ German), DOAJ (9M+ OA articles),
and Unpaywall for PDF URLs. Deduplicates results across sources.
        """.strip(),
        level=None,
        inputs=[
            {"path": "--query / --title / --doi / --arxiv", "description": "Search query, title, DOI, or arXiv ID"},
        ],
        outputs=[
            {"path": "stdout", "description": "List of papers with title, authors, year, citations, OA status"},
            {"path": "--output/*.pdf", "description": "Downloaded PDFs (with --download flag)"},
        ],
        usage="python paper_search.py --query 'knowledge graphs LLM' --limit 20 --download",
        key_features=[
            "9 academic APIs queried in parallel",
            "Automatic PDF URL resolution via Unpaywall",
            "Deduplication by title similarity",
            "Rate limiting per source"
        ]
    ),

    "paper_download.py": ScriptDoc(
        name="paper_download.py",
        path="skills/paper-search/scripts/paper_download.py",
        purpose="Batch download papers with multi-source fallback and retry logic",
        description="""
Robust paper downloader with intelligent URL resolution. Reads _selection_log.md
or JSON input, resolves PDFs via arXiv, Semantic Scholar, OpenAlex, and Unpaywall.
Parallel downloads with progress tracking, PDF magic byte verification, exponential
backoff retry, and per-source rate limiting.
        """.strip(),
        level=None,
        inputs=[
            {"path": "_selection_log.md", "description": "Markdown table with paper IDs, titles, URLs"},
            {"path": "papers.json", "description": "JSON list of papers with DOI/arXiv/URLs"},
        ],
        outputs=[
            {"path": "output/{id}-{title}.pdf", "description": "Downloaded PDF files"},
            {"path": "output/_download_report.md", "description": "Download success/failure report"},
        ],
        usage="python paper_download.py --input _selection_log.md --output ./papers/ --parallel 5",
        key_features=[
            "Multi-source URL resolution (arXiv > S2 > Unpaywall)",
            "PDF verification (magic bytes check)",
            "Exponential backoff retry (3 attempts)",
            "Parallel downloads with semaphore"
        ]
    ),

    # =========================================================================
    # PDF PROCESSING
    # =========================================================================

    "pdf_to_markdown.py": ScriptDoc(
        name="pdf_to_markdown.py",
        path="skills/pdf-preprocess/scripts/pdf_to_markdown.py",
        purpose="Convert PDFs to chunked markdown files for LLM consumption",
        description="""
PDF extraction using pymupdf4llm for high-quality markdown output. Auto-chunks
content to max N lines with configurable overlap for context continuity.
Creates one folder per PDF containing numbered chunk files and _metadata.json.
Preserves headings, tables, and formatting.
        """.strip(),
        level=None,
        inputs=[
            {"path": "input.pdf", "description": "Source PDF file"},
            {"path": "--max-lines", "description": "Max lines per chunk (default: 1000)"},
            {"path": "--overlap", "description": "Overlap lines between chunks (default: 100)"},
        ],
        outputs=[
            {"path": "{name}/{name}_1.md", "description": "First markdown chunk"},
            {"path": "{name}/{name}_N.md", "description": "Subsequent chunks"},
            {"path": "{name}/_metadata.json", "description": "Chunk metadata (sizes, counts)"},
        ],
        usage="python pdf_to_markdown.py ./papers/ --batch --max-lines 800 --overlap 50",
        key_features=[
            "pymupdf4llm for quality extraction",
            "Smart paragraph-boundary chunking",
            "Configurable overlap for context",
            "Batch processing mode"
        ]
    ),

    # =========================================================================
    # 7-LEVEL SYNTHESIS ARCHITECTURE
    # =========================================================================

    "build_synthesis_routing.py": ScriptDoc(
        name="build_synthesis_routing.py",
        path="validation/scripts/build_synthesis_routing.py",
        purpose="Level 1: Build routing table from chunk_index.fields_found",
        description="""
First level of 7-Level Synthesis Architecture. Reads all index.md files with
chunk_index (Schema 2.3+), builds a routing table mapping extraction fields
to specific paper chunks. Uses boolean lookup (no full-text search) for
deterministic routing. Warns if field matches >80% of chunks (Gap G19 sparsity).
        """.strip(),
        level=1,
        inputs=[
            {"path": "02-resources/_briefing.md", "description": "Extraction schema definition"},
            {"path": "02-resources/papers/*/index.md", "description": "Paper indices with chunk_index"},
        ],
        outputs=[
            {"path": "02-resources/_synthesis_routing.yaml", "description": "Field → chunks routing table"},
        ],
        usage="python build_synthesis_routing.py PROJECT_PATH --output 02-resources/_synthesis_routing.yaml",
        key_features=[
            "Boolean lookup from chunk_index.fields_found",
            "Sparsity warning (Gap G19) if field matches >80%",
            "Per-chunk token counts for budget planning",
            "Deterministic (no LLM needed)"
        ]
    ),

    "calculate_subagent_allocation.py": ScriptDoc(
        name="calculate_subagent_allocation.py",
        path="validation/scripts/calculate_subagent_allocation.py",
        purpose="Level 2: Greedy bin-packing of chunks into subagent batches",
        description="""
Second level of 7-Level Architecture. Takes routing table and packs chunks
into batches respecting 70K token budget per batch. Uses greedy bin-packing,
groups chunks by paper when possible. Also calculates Level 7 token budget
for final report (Gap G2 fix).
        """.strip(),
        level=2,
        inputs=[
            {"path": "_synthesis_routing.yaml", "description": "Routing table from Level 1"},
        ],
        outputs=[
            {"path": "_subagent_plan.yaml", "description": "Batch assignments with token budgets"},
        ],
        usage="python calculate_subagent_allocation.py PROJECT --input routing.yaml --output plan.yaml",
        key_features=[
            "Greedy bin-packing algorithm",
            "70K tokens per batch budget",
            "Level 7 budget calculation (Gap G2)",
            "Estimated duration per batch"
        ]
    ),

    "generate_subagent_prompts.py": ScriptDoc(
        name="generate_subagent_prompts.py",
        path="validation/scripts/generate_subagent_prompts.py",
        purpose="Level 3: Generate prompts with INPUT CONTRACT for each batch",
        description="""
Third level of 7-Level Architecture. Creates subagent prompt files with strict
INPUT CONTRACT (Gap G13) listing exact files to read. Includes research_purpose
(Gap G22a) and synthesis_goals (Gap G22b) from _briefing.md and _analysis_kit.md.
Generates output schema template with citation format.
        """.strip(),
        level=3,
        inputs=[
            {"path": "_subagent_plan.yaml", "description": "Batch assignments from Level 2"},
            {"path": "_briefing.md", "description": "research_purpose field"},
            {"path": "_analysis_kit.md", "description": "synthesis_goals field"},
        ],
        outputs=[
            {"path": "03-working/_prompt_{field}_{N}.md", "description": "Subagent prompt files"},
        ],
        usage="python generate_subagent_prompts.py PROJECT --input plan.yaml --output-dir 03-working/",
        key_features=[
            "INPUT CONTRACT (Gap G13) - strict file list",
            "research_purpose context (Gap G22a)",
            "synthesis_goals context (Gap G22b)",
            "Output schema with citation format"
        ]
    ),

    # Level 4 is subagent execution (no script, done by Claude)

    "verify_subagent_output.py": ScriptDoc(
        name="verify_subagent_output.py",
        path="validation/scripts/verify_subagent_output.py",
        purpose="Level 5: Verify extraction outputs with quote-line checking",
        description="""
Fifth level of 7-Level Architecture. Samples patterns from batch outputs and
verifies quoted text exists at cited line numbers (Gap G15). Checks chunk_ref
format, file existence, and quote presence with 5-line tolerance. Requires
90% verification rate to pass.
        """.strip(),
        level=5,
        inputs=[
            {"path": "03-working/_batch_*.yaml", "description": "Subagent extraction outputs"},
            {"path": "02-resources/papers/*/*.md", "description": "Source chunk files for verification"},
        ],
        outputs=[
            {"path": "_verification_report.yaml", "description": "Pass/fail with failure details"},
        ],
        usage="python verify_subagent_output.py PROJECT --input-dir 03-working/ --sample-rate 0.1",
        key_features=[
            "Quote-line verification (Gap G15)",
            "10% sample rate by default",
            "5-line tolerance for matching",
            "90% threshold to pass"
        ]
    ),

    "aggregate_patterns.py": ScriptDoc(
        name="aggregate_patterns.py",
        path="validation/scripts/aggregate_patterns.py",
        purpose="Level 6: Deduplicate and aggregate patterns across batches",
        description="""
Sixth level of 7-Level Architecture. Reads all batch outputs, uses fuzzy matching
(70% threshold) to deduplicate patterns while preserving all source citations.
Creates per-field synthesis files combining patterns from multiple papers.
        """.strip(),
        level=6,
        inputs=[
            {"path": "03-working/_batch_*.yaml", "description": "Verified batch outputs"},
        ],
        outputs=[
            {"path": "04-outputs/_synthesis_{field}.yaml", "description": "Aggregated per-field patterns"},
        ],
        usage="python aggregate_patterns.py PROJECT --input-dir 03-working/ --output-dir 04-outputs/",
        key_features=[
            "Fuzzy name matching (70% threshold)",
            "Source preservation (all citations kept)",
            "Deduplication rate reporting",
            "Per-field output files"
        ]
    ),

    # Level 7 is final report generation (done by Claude with budget from Level 2)

    # =========================================================================
    # PAPER MANAGEMENT
    # =========================================================================

    "paper_manage.py": ScriptDoc(
        name="paper_manage.py",
        path="skills/paper-manage/scripts/paper_manage.py",
        purpose="Manage paper collections: list, status, rebuild indices",
        description="""
Paper collection management utility. Lists all collections with paper counts,
shows detailed status for a collection (analyzed/pending, topics, tokens),
rebuilds _collection.md index files, and aggregates stats across all collections.
        """.strip(),
        level=None,
        inputs=[
            {"path": "04-workspace/papers/*/", "description": "Paper collection folders"},
        ],
        outputs=[
            {"path": "_collection.md", "description": "Collection index with paper table"},
            {"path": "stdout", "description": "Status/stats output"},
        ],
        usage="python paper_manage.py --status TA_LLM --rebuild",
        key_features=[
            "Collection listing with counts",
            "Detailed per-collection status",
            "Topic aggregation across papers",
            "Token estimation"
        ]
    ),

    # =========================================================================
    # SYNTHESIS HELPERS
    # =========================================================================

    "aggregate_field.py": ScriptDoc(
        name="aggregate_field.py",
        path="skills/paper-synthesize/scripts/aggregate_field.py",
        purpose="Aggregate a specific extraction field across all papers with sources",
        description="""
Reads ALREADY EXTRACTED data from index.md frontmatter and aggregates it with
full source citations. No re-reading of chunks needed. Produces cross-paper
synthesis with pattern frequency, source papers, and chunk references.
        """.strip(),
        level=None,
        inputs=[
            {"path": "02-resources/papers/*/index.md", "description": "Paper indices with extracted fields"},
        ],
        outputs=[
            {"path": "04-outputs/_synthesis_{field}.md", "description": "Markdown synthesis with sources"},
            {"path": "04-outputs/_synthesis_{field}.yaml", "description": "YAML for programmatic use"},
        ],
        usage="python aggregate_field.py PROJECT --field ai_integration --format markdown",
        key_features=[
            "Pattern normalization for dedup",
            "Multi-source tracking per pattern",
            "Frequency-sorted output",
            "Markdown and YAML formats"
        ]
    ),

    "prepare_synthesis_chunks.py": ScriptDoc(
        name="prepare_synthesis_chunks.py",
        path="skills/paper-query/scripts/prepare_synthesis_chunks.py",
        purpose="Map extraction fields to relevant chunks using 'Load when' hints",
        description="""
Analyzes index.md files and creates a routing table mapping fields to chunks.
Uses 'Load when' hints from chunk navigation, concept keywords, and title matching
to score chunk relevance per field. Alternative to build_synthesis_routing.py
using heuristic matching instead of chunk_index.
        """.strip(),
        level=None,
        inputs=[
            {"path": "_briefing.md", "description": "Extraction schema"},
            {"path": "papers/*/index.md", "description": "Paper indices with chunk navigation"},
        ],
        outputs=[
            {"path": "_synthesis_routing.yaml", "description": "Field → chunks routing"},
        ],
        usage="python prepare_synthesis_chunks.py 02-projects/02-ontologies-research",
        key_features=[
            "Keyword-based chunk scoring",
            "'Load when' hint parsing",
            "Top 3 chunks per field per paper",
            "Heuristic (no chunk_index required)"
        ]
    ),
}


def get_script_doc(script_name: str) -> Optional[ScriptDoc]:
    """Get documentation for a script by name."""
    # Try exact match
    if script_name in SCRIPT_REGISTRY:
        return SCRIPT_REGISTRY[script_name]

    # Try basename match
    for key, doc in SCRIPT_REGISTRY.items():
        if key == script_name or doc.path.endswith(script_name):
            return doc

    return None


def get_scripts_by_level(level: int) -> List[ScriptDoc]:
    """Get all scripts for a given 7-level architecture level."""
    return [doc for doc in SCRIPT_REGISTRY.values() if doc.level == level]


def get_all_scripts() -> Dict[str, ScriptDoc]:
    """Get all script documentation."""
    return SCRIPT_REGISTRY


# Output file documentation
OUTPUT_FILES = {
    "_briefing.md": {
        "description": "Research project definition with goals, questions, and extraction schema",
        "created_by": "create-research-project orchestrator",
        "contains": ["research_purpose", "extraction_schema", "paper_requirements"],
    },
    "_analysis_kit.md": {
        "description": "Analysis configuration with comparison/identification goals",
        "created_by": "create-research-project orchestrator",
        "contains": ["comparison_goal", "identification_goal", "analysis_goal"],
    },
    "_extraction_guide.md": {
        "description": "Instructions for subagents on how to extract patterns",
        "created_by": "create-research-project orchestrator",
        "contains": ["extraction_rules", "citation_format", "quality_requirements"],
    },
    "_selection_log.md": {
        "description": "Paper selection decisions with URLs and status",
        "created_by": "paper-search skill",
        "contains": ["paper_table", "selection_rationale", "download_status"],
    },
    "_synthesis_routing.yaml": {
        "description": "Routing table mapping fields to paper chunks",
        "created_by": "build_synthesis_routing.py (Level 1)",
        "contains": ["field_mappings", "chunk_references", "token_counts"],
    },
    "_subagent_plan.yaml": {
        "description": "Batch assignments for parallel extraction",
        "created_by": "calculate_subagent_allocation.py (Level 2)",
        "contains": ["batch_assignments", "token_budgets", "level7_budget"],
    },
    "_batch_{field}_{N}.yaml": {
        "description": "Extracted patterns from one batch of chunks",
        "created_by": "Subagent execution (Level 4)",
        "contains": ["patterns", "chunk_refs", "quotes", "descriptions"],
    },
    "_verification_report.yaml": {
        "description": "Quote-line verification results",
        "created_by": "verify_subagent_output.py (Level 5)",
        "contains": ["verification_rate", "failures", "verdict"],
    },
    "_synthesis_{field}.yaml": {
        "description": "Aggregated patterns for one extraction field",
        "created_by": "aggregate_patterns.py (Level 6)",
        "contains": ["deduplicated_patterns", "sources", "frequency"],
    },
    "_synthesis_report.md": {
        "description": "Final cross-paper synthesis report",
        "created_by": "Subagent execution (Level 7)",
        "contains": ["executive_summary", "findings_by_field", "citations"],
    },
    "index.md": {
        "description": "Paper analysis index with frontmatter and chunk navigation",
        "created_by": "analyze-research-project orchestrator",
        "contains": ["paper_metadata", "chunk_index", "extracted_fields", "chunk_navigation"],
    },
    "_analysis_log.md": {
        "description": "Detailed analysis log for a single paper",
        "created_by": "paper-analyze-core skill",
        "contains": ["analysis_notes", "extraction_details", "quality_flags"],
    },
}


if __name__ == "__main__":
    # Print registry for debugging
    print("Script Registry")
    print("=" * 60)
    for name, doc in SCRIPT_REGISTRY.items():
        level_str = f"Level {doc.level}" if doc.level else "Utility"
        print(f"\n{name} ({level_str})")
        print(f"  {doc.purpose}")
        print(f"  Inputs: {len(doc.inputs)}, Outputs: {len(doc.outputs)}")

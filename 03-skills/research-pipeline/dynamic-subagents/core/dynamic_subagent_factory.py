#!/usr/bin/env python3
"""Dynamic Subagent Factory for Research Pipeline.

Generates task-specific subagent prompts with:
- Strict INPUT CONTRACT (what files to read)
- Exact OUTPUT SCHEMA (structured format)
- Domain-specific PERSONA (expertise vocabulary)
- VERIFICATION RULES (for post-output validation)

HIGH QUALITY DATA TRANSFER is the primary goal.

Usage:
    python dynamic_subagent_factory.py <project_path> <task_type> [options]

Task Types:
    paper_analysis    - Analyze a single paper → index.md
    batch_extraction  - Extract patterns for a field → _batch_{field}_{N}.yaml
    field_aggregation - Merge batches → _synthesis_{field}.yaml
    final_synthesis   - Generate report → _synthesis_report.md
"""

import yaml
import hashlib
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import sys
import re


# =============================================================================
# DOMAIN REGISTRY - Domain-specific personas and vocabulary
# =============================================================================

DOMAIN_REGISTRY = {
    "ontology": {
        "name": "Ontologie-Ingenieur",
        "expertise": [
            "Foundational Ontologies (BFO, DOLCE, UFO, SUMO)",
            "Entity-Hierarchien und Taxonomien",
            "Axiomatische Definitionen und Constraints",
            "Mereologie, Topologie, Dependence Relations"
        ],
        "vocabulary": {
            "Endurant": "Entity wholly present at any time (continuant)",
            "Perdurant": "Entity that unfolds over time (occurrent)",
            "Universal": "Type/class in ontology",
            "Particular": "Instance of a universal",
            "Subsumption": "Is-a relationship between universals",
            "Parthood": "Part-of relationship (mereology)"
        },
        "focus": "Achte auf formale Definitionen, Axiome, und Hierarchie-Strukturen",
        "detection_keywords": ["ontology", "ontologie", "BFO", "DOLCE", "UFO", "entity", "universal"]
    },

    "nlp": {
        "name": "NLP/LLM-Forscher",
        "expertise": [
            "Transformer-Architekturen und Attention",
            "Fine-Tuning, RLHF, Instruction Tuning",
            "Prompt Engineering und In-Context Learning",
            "Evaluation Metrics und Benchmarks"
        ],
        "vocabulary": {
            "Attention": "Mechanism for weighing token relevance",
            "Embedding": "Dense vector representation",
            "Token": "Basic unit of text processing",
            "Perplexity": "Model uncertainty measure",
            "Fine-tuning": "Adapting pre-trained model to task"
        },
        "focus": "Achte auf Modellgrößen, Trainingsdetails, Hyperparameter, Benchmarks",
        "detection_keywords": ["LLM", "transformer", "GPT", "BERT", "fine-tuning", "prompt", "token"]
    },

    "multi_agent": {
        "name": "Multi-Agent-Systems Experte",
        "expertise": [
            "Agent Coordination Patterns",
            "Communication Protocols und Message Passing",
            "Task Allocation und Scheduling",
            "Emergent Behavior und Swarm Intelligence"
        ],
        "vocabulary": {
            "Handover": "Transfer of control between agents",
            "Orchestration": "Central coordination of agents",
            "Choreography": "Decentralized agent coordination",
            "Delegation": "Assigning subtasks to other agents",
            "Consensus": "Agreement protocol among agents"
        },
        "focus": "Achte auf Interaktionsmuster, Koordinationsmechanismen, Fehlerbehandlung",
        "detection_keywords": ["agent", "multi-agent", "MAS", "coordination", "orchestration", "handover"]
    },

    "knowledge_graph": {
        "name": "Knowledge Graph Spezialist",
        "expertise": [
            "Graph-Datenmodelle (RDF, Property Graphs)",
            "Ontologie-basiertes Reasoning",
            "Knowledge Graph Embedding",
            "SPARQL und Graph Query Languages"
        ],
        "vocabulary": {
            "Triple": "Subject-Predicate-Object statement",
            "Node": "Entity in knowledge graph",
            "Edge": "Relationship between nodes",
            "Embedding": "Vector representation of entity/relation",
            "Reasoning": "Inferring new knowledge from graph"
        },
        "focus": "Achte auf Graph-Strukturen, Schemata, Reasoning-Regeln",
        "detection_keywords": ["knowledge graph", "KG", "RDF", "triple", "SPARQL", "embedding"]
    },

    "default": {
        "name": "Wissenschaftlicher Analyst",
        "expertise": [
            "Systematische Literaturanalyse",
            "Informationsextraktion",
            "Vergleichende Analyse",
            "Evidenz-basierte Synthese"
        ],
        "vocabulary": {},
        "focus": "Extrahiere strukturierte Informationen mit präzisen Quellenangaben",
        "detection_keywords": []
    }
}


# =============================================================================
# TASK METHODOLOGIES - Task-specific steps and output schemas
# =============================================================================

TASK_METHODOLOGIES = {
    "paper_analysis": {
        "description": "Analyze a single paper and produce index.md with chunk_index",
        "steps": [
            "1. Read _briefing.md to understand research question and fields",
            "2. Read _metadata.json to get chunk count and structure",
            "3. For EACH chunk in order:",
            "   a. Read full chunk content (not just headers)",
            "   b. Assess EVERY field: true/partial/false",
            "   c. Extract items with chunk:line references",
            "   d. Record 3-point evidence (start/mid/end + hash)",
            "4. Compile index.md with chunk_index frontmatter",
            "5. Validate: all fields assessed, all chunks read",
            "6. Write _analysis_log.md with step completion"
        ],
        "output_files": [
            {"name": "index.md", "format": "yaml_frontmatter_markdown"},
            {"name": "_analysis_log.md", "format": "yaml_frontmatter_markdown"}
        ],
        "output_schema": {
            "index.md": {
                "required_frontmatter": [
                    "paper_id", "title", "chunks_expected", "chunks_read",
                    "analysis_complete", "schema_version", "chunk_index"
                ],
                "chunk_index_schema": {
                    "token_count": "int, calculated as len(content)//4",
                    "hash": "SHA256 of chunk content",
                    "fields_found": "dict mapping field_name to true/partial/false"
                }
            }
        },
        "anti_hallucination": True,
        "citation_format": "Chunk N:Line-Line"
    },

    "batch_extraction": {
        "description": "Extract patterns for a specific field from assigned chunks",
        "steps": [
            "1. Read _briefing.md for field definition and research_purpose",
            "2. For EACH chunk in batch (read COMPLETELY):",
            "   a. Find all instances of the target field",
            "   b. Extract with exact quote (100-150 chars)",
            "   c. Record chunk:line reference",
            "   d. Note context and description",
            "3. Output structured YAML with patterns array"
        ],
        "output_files": [
            {"name": "_batch_{field}_{N}.yaml", "format": "yaml"}
        ],
        "output_schema": {
            "_batch_{field}_{N}.yaml": {
                "required_fields": ["batch_id", "field", "extracted_at", "chunks_read", "patterns_found"],
                "patterns_schema": {
                    "name": "string, pattern name",
                    "chunk_ref": "string, format: Paper-ID (Chunk N:Line-Line)",
                    "quote": "string, 100-150 chars exact text",
                    "description": "string, full context"
                }
            }
        },
        "anti_hallucination": True,
        "citation_format": "Paper-ID (Chunk N:Line-Line)"
    },

    "field_aggregation": {
        "description": "Merge batch outputs into field synthesis (SCRIPT, not subagent)",
        "steps": [
            "1. Read all _batch_{field}_*.yaml files",
            "2. Merge patterns by name (fuzzy match 90%)",
            "3. Combine sources from multiple batches",
            "4. Output aggregated YAML"
        ],
        "output_files": [
            {"name": "_synthesis_{field}.yaml", "format": "yaml"}
        ],
        "is_script": True  # Not a subagent task
    },

    "final_synthesis": {
        "description": "Generate comprehensive synthesis report from aggregated fields",
        "steps": [
            "1. Read _briefing.md for research question and purpose",
            "2. Read all _synthesis_{field}.yaml files",
            "3. Answer research question with evidence",
            "4. Identify cross-field patterns",
            "5. Include block quotes with citations",
            "6. Generate full reference list"
        ],
        "output_files": [
            {"name": "_synthesis_report.md", "format": "markdown"}
        ],
        "output_schema": {
            "_synthesis_report.md": {
                "required_sections": [
                    "Executive Summary", "Key Findings", "Cross-Field Insights",
                    "Recommendations", "Limitations", "Appendix A: Field Summaries",
                    "Appendix B: Full Reference List"
                ],
                "citation_format": "[Paper-ID (Chunk:Line)]"
            }
        },
        "anti_hallucination": False,  # Works on already-validated data
        "citation_format": "[Paper-ID (Chunk:Line)]"
    }
}


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class InputContract:
    """Defines what a subagent MUST and MUST NOT read."""
    must_read: List[Dict[str, str]]
    must_not_read: List[str]
    validation_message: str = "VIOLATION = Output rejected"

    def to_markdown(self) -> str:
        lines = ["## INPUT CONTRACT (STRICT)", ""]
        lines.append("### Files You MUST Read (in this order)")
        for i, file in enumerate(self.must_read, 1):
            lines.append(f"{i}. `{file['path']}`")
            if 'purpose' in file:
                lines.append(f"   - Purpose: {file['purpose']}")
            if 'hash' in file:
                lines.append(f"   - Expected hash: `{file['hash'][:16]}...`")

        lines.append("")
        lines.append("### Files You MUST NOT Read")
        for pattern in self.must_not_read:
            lines.append(f"- `{pattern}`")

        lines.append("")
        lines.append(f"**{self.validation_message}**")
        return "\n".join(lines)


@dataclass
class OutputSchema:
    """Defines the exact output format for a subagent."""
    format: str  # yaml, markdown, yaml_frontmatter_markdown
    required_fields: List[str]
    field_schemas: Dict[str, Any]
    validation_rules: List[str]

    def to_markdown(self) -> str:
        lines = ["## OUTPUT SCHEMA (EXACT)", ""]
        lines.append(f"**Format**: {self.format}")
        lines.append("")
        lines.append("### Required Fields")
        for field in self.required_fields:
            schema = self.field_schemas.get(field, "any")
            lines.append(f"- `{field}`: {schema}")

        if self.validation_rules:
            lines.append("")
            lines.append("### Validation Rules")
            for rule in self.validation_rules:
                lines.append(f"- {rule}")

        return "\n".join(lines)


@dataclass
class SubagentPrompt:
    """Complete subagent prompt with all components."""
    task_id: str
    task_type: str
    persona: Dict[str, Any]
    input_contract: InputContract
    output_schema: OutputSchema
    methodology: List[str]
    context: Dict[str, str]
    critical_rules: List[str]

    def to_markdown(self) -> str:
        """Generate full markdown prompt."""
        lines = [
            f"# {self.task_type.replace('_', ' ').title()}: {self.task_id}",
            "",
            "---",
            ""
        ]

        # Persona
        lines.append("## ROLLE")
        lines.append("")
        lines.append(f"Du bist **{self.persona['name']}**.")
        lines.append("")
        lines.append("**Expertise:**")
        for exp in self.persona.get('expertise', []):
            lines.append(f"- {exp}")

        if self.persona.get('vocabulary'):
            lines.append("")
            lines.append("**Fachvokabular:**")
            for term, definition in self.persona['vocabulary'].items():
                lines.append(f"- **{term}**: {definition}")

        lines.append("")
        lines.append(f"**Fokus:** {self.persona.get('focus', '')}")
        lines.append("")

        # Input Contract
        lines.append(self.input_contract.to_markdown())
        lines.append("")

        # Context
        lines.append("## KONTEXT")
        lines.append("")
        for key, value in self.context.items():
            lines.append(f"**{key}**: {value}")
        lines.append("")

        # Methodology
        lines.append("## METHODOLOGIE")
        lines.append("")
        for step in self.methodology:
            lines.append(step)
        lines.append("")

        # Output Schema
        lines.append(self.output_schema.to_markdown())
        lines.append("")

        # Critical Rules
        lines.append("## KRITISCHE REGELN")
        lines.append("")
        for rule in self.critical_rules:
            lines.append(f"- {rule}")

        return "\n".join(lines)


# =============================================================================
# FACTORY FUNCTIONS
# =============================================================================

def detect_domain(briefing: dict) -> str:
    """Detect research domain from briefing content."""
    text = json.dumps(briefing).lower()

    # Check each domain's keywords
    scores = {}
    for domain, config in DOMAIN_REGISTRY.items():
        if domain == "default":
            continue
        score = sum(1 for kw in config.get('detection_keywords', []) if kw.lower() in text)
        if score > 0:
            scores[domain] = score

    if scores:
        return max(scores, key=scores.get)
    return "default"


def load_yaml_frontmatter(file_path: Path) -> dict:
    """Load YAML frontmatter from markdown file."""
    content = file_path.read_text(encoding='utf-8')
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return yaml.safe_load(content[3:end]) or {}
    return {}


def compute_file_hash(file_path: Path) -> str:
    """Compute SHA256 hash of file content."""
    content = file_path.read_text(encoding='utf-8')
    return hashlib.sha256(content.encode()).hexdigest()


def generate_input_contract(
    task_type: str,
    project_path: Path,
    batch_context: Optional[dict] = None
) -> InputContract:
    """Generate INPUT CONTRACT based on task type."""

    must_read = []
    must_not_read = [
        "*.pdf",
        "04-outputs/*",
        "../*",
        ".git/*",
        "*.pyc"
    ]

    if task_type == "paper_analysis":
        paper_path = batch_context.get('paper_path')
        paper_id = batch_context.get('paper_id')

        # Briefing
        briefing_path = project_path / "02-resources/_briefing.md"
        must_read.append({
            "path": str(briefing_path),
            "purpose": "Research question and extraction schema"
        })

        # Analysis kit
        kit_path = project_path / "02-resources/_analysis_kit.md"
        if kit_path.exists():
            must_read.append({
                "path": str(kit_path),
                "purpose": "Subagent context and synthesis goals"
            })

        # Extraction guide
        guide_path = project_path / "02-resources/_extraction_guide.md"
        if guide_path.exists():
            must_read.append({
                "path": str(guide_path),
                "purpose": "Field examples and controlled vocabulary"
            })

        # Metadata
        meta_path = Path(paper_path) / "_metadata.json"
        must_read.append({
            "path": str(meta_path),
            "purpose": "Chunk count and structure"
        })

        # Chunks
        chunks = batch_context.get('chunks', [])
        for chunk_num in chunks:
            chunk_path = Path(paper_path) / f"{paper_id}_{chunk_num}.md"
            must_read.append({
                "path": str(chunk_path),
                "purpose": f"Chunk {chunk_num} content"
            })

        # Don't read other papers
        must_not_read.append("02-resources/papers/*/")  # Other paper folders

    elif task_type == "batch_extraction":
        # Briefing
        briefing_path = project_path / "02-resources/_briefing.md"
        must_read.append({
            "path": str(briefing_path),
            "purpose": "Research question and field definition"
        })

        # Specific chunks for this batch
        for chunk_info in batch_context.get('chunks', []):
            paper_id = chunk_info['paper_id']
            chunk_num = chunk_info['chunk']
            chunk_path = project_path / f"02-resources/papers/{paper_id}/{paper_id}_{chunk_num}.md"
            must_read.append({
                "path": str(chunk_path),
                "purpose": f"Chunk content for extraction",
                "hash": chunk_info.get('hash', '')[:16] if chunk_info.get('hash') else None
            })

        # Don't read other batches
        must_not_read.append("03-working/_batch_*")

    elif task_type == "final_synthesis":
        # Briefing
        must_read.append({
            "path": str(project_path / "02-resources/_briefing.md"),
            "purpose": "Research question and purpose"
        })

        # All synthesis files
        for field in batch_context.get('fields', []):
            must_read.append({
                "path": str(project_path / f"04-outputs/_synthesis_{field}.yaml"),
                "purpose": f"Aggregated patterns for {field}"
            })

        # Don't read raw chunks
        must_not_read.append("02-resources/papers/*/")

    return InputContract(
        must_read=must_read,
        must_not_read=must_not_read
    )


def generate_output_schema(task_type: str, batch_context: Optional[dict] = None) -> OutputSchema:
    """Generate OUTPUT SCHEMA based on task type."""

    methodology = TASK_METHODOLOGIES.get(task_type, {})
    schema_config = methodology.get('output_schema', {})

    if task_type == "paper_analysis":
        return OutputSchema(
            format="yaml_frontmatter_markdown",
            required_fields=[
                "paper_id", "title", "chunks_expected", "chunks_read",
                "analysis_complete", "schema_version", "chunk_index"
            ],
            field_schemas={
                "paper_id": "string, folder name",
                "chunks_expected": "int, from _metadata.json",
                "chunks_read": "int, must equal chunks_expected",
                "schema_version": "string, must be '2.3'",
                "chunk_index": "dict, see chunk_index_schema below"
            },
            validation_rules=[
                "chunks_read MUST equal chunks_expected",
                "schema_version MUST be '2.3'",
                "chunk_index MUST have entry for every chunk",
                "fields_found MUST assess EVERY field from _briefing.md",
                "Each extraction MUST have chunk:line reference"
            ]
        )

    elif task_type == "batch_extraction":
        field = batch_context.get('field', 'unknown')
        batch_num = batch_context.get('batch_num', 1)
        return OutputSchema(
            format="yaml",
            required_fields=["batch_id", "field", "extracted_at", "chunks_read", "patterns_found", "patterns"],
            field_schemas={
                "batch_id": f"string, must be '{field}_{batch_num}'",
                "field": f"string, must be '{field}'",
                "patterns": "array of pattern objects",
                "pattern.name": "string, descriptive name",
                "pattern.chunk_ref": "string, format: Paper-ID (Chunk N:Line-Line)",
                "pattern.quote": "string, 100-150 chars exact text from source",
                "pattern.description": "string, context and explanation"
            },
            validation_rules=[
                "chunk_ref MUST match regex: ^[\\w-]+ \\(Chunk \\d+:\\d+-\\d+\\)$",
                "quote MUST be 100-150 characters",
                "quote MUST exist at cited line in source chunk",
                "chunks_read MUST match number of chunks in INPUT CONTRACT"
            ]
        )

    elif task_type == "final_synthesis":
        return OutputSchema(
            format="markdown",
            required_fields=[
                "Executive Summary", "Key Findings", "Cross-Field Insights",
                "Recommendations", "Limitations", "Appendix B: Full Reference List"
            ],
            field_schemas={
                "Executive Summary": "3-4 paragraphs answering research question with inline citations",
                "Key Findings": "5-8 findings with evidence tables and block quotes",
                "Cross-Field Insights": "Patterns spanning multiple fields",
                "Reference List": "All papers cited with chunk references"
            },
            validation_rules=[
                "Every claim MUST have inline citation: [Paper-ID (Chunk:Line)]",
                "Include at least 3 block quotes with citations",
                "Reference list MUST include all papers cited"
            ]
        )

    return OutputSchema(format="yaml", required_fields=[], field_schemas={}, validation_rules=[])


def generate_subagent_prompt(
    project_path: Path,
    task_type: str,
    batch_context: dict
) -> SubagentPrompt:
    """Generate complete subagent prompt with all components."""

    # Load briefing for domain detection
    briefing_path = project_path / "02-resources/_briefing.md"
    briefing = load_yaml_frontmatter(briefing_path) if briefing_path.exists() else {}

    # Detect domain
    domain = detect_domain(briefing)
    persona = DOMAIN_REGISTRY.get(domain, DOMAIN_REGISTRY['default'])

    # Get methodology
    methodology = TASK_METHODOLOGIES.get(task_type, {})

    # Generate components
    input_contract = generate_input_contract(task_type, project_path, batch_context)
    output_schema = generate_output_schema(task_type, batch_context)

    # Build context
    context = {
        "Research Question": briefing.get('research_question', 'Not specified'),
        "Research Purpose": briefing.get('research_purpose', 'Not specified'),
        "Domain": domain,
        "Task": methodology.get('description', task_type)
    }

    if task_type == "batch_extraction":
        context["Field"] = batch_context.get('field', 'unknown')
        context["Batch"] = f"{batch_context.get('batch_num', 1)} of {batch_context.get('total_batches', 1)}"

    # Critical rules based on task type
    critical_rules = [
        "Lies JEDEN Chunk VOLLSTÄNDIG - kein Überfliegen",
        "Halte dich EXAKT an das OUTPUT SCHEMA",
        "Jede Extraktion MUSS chunk:line Referenz haben",
        "Bei Unsicherheit: [UNCERTAIN: reason] markieren"
    ]

    if methodology.get('anti_hallucination'):
        critical_rules.extend([
            "Record 3-point evidence: start (100 chars) + mid (100 chars) + end (100 chars)",
            "Compute SHA256 hash for each chunk read",
            "Quotes will be VERIFIED against source - inaccuracy = failure"
        ])

    return SubagentPrompt(
        task_id=batch_context.get('task_id', f"{task_type}_{datetime.now().strftime('%H%M%S')}"),
        task_type=task_type,
        persona=persona,
        input_contract=input_contract,
        output_schema=output_schema,
        methodology=methodology.get('steps', []),
        context=context,
        critical_rules=critical_rules
    )


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    """CLI entry point."""
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    project_path = Path(sys.argv[1])
    task_type = sys.argv[2]

    if not project_path.exists():
        print(f"Error: Project path not found: {project_path}")
        sys.exit(1)

    if task_type not in TASK_METHODOLOGIES:
        print(f"Error: Unknown task type: {task_type}")
        print(f"Valid types: {', '.join(TASK_METHODOLOGIES.keys())}")
        sys.exit(1)

    # Example batch context (would come from _subagent_plan.yaml in real use)
    batch_context = {
        "task_id": f"{task_type}_001",
        "field": "entity_types",
        "batch_num": 1,
        "total_batches": 6,
        "chunks": [
            {"paper_id": "02-Knowledge_Graphs", "chunk": 2, "hash": "a7b8c9d4e5f6"},
            {"paper_id": "02-Knowledge_Graphs", "chunk": 6, "hash": "g7h8i9j0k1l2"}
        ]
    }

    # For paper analysis
    if task_type == "paper_analysis":
        batch_context = {
            "task_id": "paper_analysis_02-KG",
            "paper_id": "02-Knowledge_Graphs",
            "paper_path": str(project_path / "02-resources/papers/02-Knowledge_Graphs"),
            "chunks": [1, 2, 3, 4]
        }

    # Generate prompt
    prompt = generate_subagent_prompt(project_path, task_type, batch_context)

    # Output
    output_dir = project_path / "03-working/prompts"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"_prompt_{prompt.task_id}.md"
    output_path.write_text(prompt.to_markdown(), encoding='utf-8')

    print(f"Generated prompt: {output_path}")
    print(f"Domain detected: {prompt.context.get('Domain', 'default')}")
    print(f"Persona: {prompt.persona['name']}")
    print(f"Input files: {len(prompt.input_contract.must_read)}")
    print(f"Critical rules: {len(prompt.critical_rules)}")


if __name__ == '__main__':
    main()

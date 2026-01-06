#!/usr/bin/env python3
"""Generate Dynamic Research Subagent with HIGH-QUALITY DATA TRANSFER.

This is the main entry point for creating task-specific subagents
that are FORCED to read EVERYTHING and produce VERIFIED outputs.

Key Features:
1. Domain-specific persona (ontology, NLP, multi-agent, etc.)
2. Strict INPUT CONTRACT (explicit file allowlist)
3. FORCED READING CONTRACT (3-point evidence, hash, spot checks)
4. Exact OUTPUT SCHEMA (YAML structure with validation)
5. Post-output VERIFICATION rules

Usage:
    python generate_dynamic_research_subagent.py <project_path> <task_type> <task_config.yaml>

Task Types:
    paper_analysis    - Analyze single paper → index.md
    batch_extraction  - Extract patterns → _batch_{field}_{N}.yaml
    final_synthesis   - Generate report → _synthesis_report.md

Example:
    python generate_dynamic_research_subagent.py \\
        02-projects/02-ontologies-research \\
        paper_analysis \\
        --paper-id 02-Knowledge_Graphs
"""

import sys
import yaml
import hashlib
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional
import argparse

# Import from core modules
sys.path.insert(0, str(Path(__file__).parent.parent / 'core'))
from dynamic_subagent_factory import (
    DOMAIN_REGISTRY,
    TASK_METHODOLOGIES,
    detect_domain,
    generate_input_contract,
    generate_output_schema,
    load_yaml_frontmatter
)
from forced_reading_contract import (
    generate_forced_reading_contract,
    generate_anti_skimming_prompt,
    generate_chunk_processing_instructions,
    generate_reading_verification_checklist,
    extract_reading_proof
)


# =============================================================================
# PROMPT TEMPLATES
# =============================================================================

PROMPT_HEADER = """---
name: {task_id}
description: {description}
tools: Read, Glob, Grep
model: inherit
---

# {title}

**Generated**: {timestamp}
**Task Type**: {task_type}
**Domain**: {domain}

---
"""

PERSONA_SECTION = """## DEINE ROLLE

Du bist **{persona_name}**.

### Expertise
{expertise_list}

### Fachvokabular
{vocabulary_table}

### Dein Fokus
{focus}

---
"""

CONTEXT_SECTION = """## KONTEXT

**Research Question**: {research_question}

**Research Purpose**: {research_purpose}

**Synthesis Goals**: {synthesis_goals}

---
"""

OUTPUT_CONTRACT = """## OUTPUT CONTRACT

### Dateiformat
**{format}**

### Output-Datei
`{output_path}`

### Pflichtfelder
{required_fields_list}

### Feldschemas
{field_schemas_table}

### Validierungsregeln
{validation_rules_list}

---
"""

CRITICAL_SECTION = """## KRITISCHE REGELN

{rules_list}

### Bei Verstoß
- Output wird ABGELEHNT
- Du musst von vorne beginnen
- Keine Teilausgaben akzeptiert

---
"""


# =============================================================================
# PROMPT BUILDER
# =============================================================================

class DynamicSubagentPromptBuilder:
    """Builds complete subagent prompts with all verification mechanisms."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.briefing = self._load_briefing()
        self.domain = detect_domain(self.briefing)
        self.persona = DOMAIN_REGISTRY.get(self.domain, DOMAIN_REGISTRY['default'])

    def _load_briefing(self) -> dict:
        """Load briefing with fallback."""
        briefing_path = self.project_path / "02-resources/_briefing.md"
        if briefing_path.exists():
            return load_yaml_frontmatter(briefing_path)
        return {}

    def _load_analysis_kit(self) -> dict:
        """Load analysis kit for synthesis goals."""
        kit_path = self.project_path / "02-resources/_analysis_kit.md"
        if kit_path.exists():
            return load_yaml_frontmatter(kit_path)
        return {}

    def build_prompt(
        self,
        task_type: str,
        task_config: dict
    ) -> str:
        """Build complete prompt with all sections."""

        sections = []

        # Header
        sections.append(self._build_header(task_type, task_config))

        # Persona
        sections.append(self._build_persona())

        # Input Contract
        input_contract = generate_input_contract(
            task_type, self.project_path, task_config
        )
        sections.append(input_contract.to_markdown())

        # Context
        sections.append(self._build_context())

        # Methodology
        sections.append(self._build_methodology(task_type))

        # FORCED READING (if applicable)
        if task_type in ['paper_analysis', 'batch_extraction']:
            chunk_paths = self._get_chunk_paths(task_config)
            if chunk_paths:
                sections.append("\n---\n")
                sections.append(generate_anti_skimming_prompt())
                sections.append(generate_chunk_processing_instructions(len(chunk_paths)))
                sections.append(generate_forced_reading_contract(chunk_paths, task_type))
                sections.append(generate_reading_verification_checklist(chunk_paths))

        # Output Contract
        output_schema = generate_output_schema(task_type, task_config)
        sections.append(self._build_output_contract(task_type, task_config, output_schema))

        # Critical Rules
        sections.append(self._build_critical_rules(task_type))

        return "\n".join(sections)

    def _build_header(self, task_type: str, task_config: dict) -> str:
        """Build prompt header."""
        task_id = task_config.get('task_id', f"{task_type}_{datetime.now().strftime('%H%M%S')}")
        methodology = TASK_METHODOLOGIES.get(task_type, {})

        return PROMPT_HEADER.format(
            task_id=task_id,
            description=methodology.get('description', task_type),
            title=task_type.replace('_', ' ').title(),
            timestamp=datetime.now().isoformat(),
            task_type=task_type,
            domain=self.domain
        )

    def _build_persona(self) -> str:
        """Build persona section."""
        # Expertise list
        expertise_list = "\n".join(f"- {e}" for e in self.persona.get('expertise', []))

        # Vocabulary table
        vocab = self.persona.get('vocabulary', {})
        if vocab:
            vocab_lines = ["| Term | Definition |", "|------|------------|"]
            for term, definition in vocab.items():
                vocab_lines.append(f"| **{term}** | {definition} |")
            vocabulary_table = "\n".join(vocab_lines)
        else:
            vocabulary_table = "*Keine domänenspezifischen Begriffe definiert*"

        return PERSONA_SECTION.format(
            persona_name=self.persona.get('name', 'Wissenschaftlicher Analyst'),
            expertise_list=expertise_list,
            vocabulary_table=vocabulary_table,
            focus=self.persona.get('focus', '')
        )

    def _build_context(self) -> str:
        """Build context section."""
        kit = self._load_analysis_kit()

        return CONTEXT_SECTION.format(
            research_question=self.briefing.get('research_question', '*Not specified*'),
            research_purpose=self.briefing.get('research_purpose', '*Not specified*'),
            synthesis_goals=kit.get('synthesis_goals', '*See _analysis_kit.md*')
        )

    def _build_methodology(self, task_type: str) -> str:
        """Build methodology section."""
        methodology = TASK_METHODOLOGIES.get(task_type, {})
        steps = methodology.get('steps', [])

        lines = ["## METHODOLOGIE", ""]
        for step in steps:
            lines.append(step)
        lines.append("")

        return "\n".join(lines)

    def _build_output_contract(
        self,
        task_type: str,
        task_config: dict,
        output_schema
    ) -> str:
        """Build output contract section."""

        # Output path
        if task_type == 'paper_analysis':
            paper_path = task_config.get('paper_path', '')
            output_path = f"{paper_path}/index.md"
        elif task_type == 'batch_extraction':
            field = task_config.get('field', 'unknown')
            batch_num = task_config.get('batch_num', 1)
            output_path = f"{self.project_path}/03-working/_batch_{field}_{batch_num}.yaml"
        elif task_type == 'final_synthesis':
            output_path = f"{self.project_path}/04-outputs/_synthesis_report.md"
        else:
            output_path = f"{self.project_path}/03-working/output.yaml"

        # Required fields list
        required_fields_list = "\n".join(f"- `{f}`" for f in output_schema.required_fields)

        # Field schemas table
        schema_lines = ["| Field | Schema |", "|-------|--------|"]
        for field, schema in output_schema.field_schemas.items():
            schema_lines.append(f"| `{field}` | {schema} |")
        field_schemas_table = "\n".join(schema_lines)

        # Validation rules list
        validation_rules_list = "\n".join(f"- {r}" for r in output_schema.validation_rules)

        return OUTPUT_CONTRACT.format(
            format=output_schema.format,
            output_path=output_path,
            required_fields_list=required_fields_list,
            field_schemas_table=field_schemas_table,
            validation_rules_list=validation_rules_list
        )

    def _build_critical_rules(self, task_type: str) -> str:
        """Build critical rules section."""

        rules = [
            "**LIES JEDEN CHUNK VOLLSTÄNDIG** - Kein Überfliegen, kein Auslassen",
            "**HALTE DICH EXAKT AN DAS OUTPUT SCHEMA** - Keine Abweichungen",
            "**JEDE EXTRAKTION BRAUCHT CHUNK:LINE REFERENZ** - Format: `Chunk N:Line-Line`",
            "**RECORD 3-POINT EVIDENCE** für jeden Chunk (start/mid/end + hash)",
            "**BEANTWORTE SPOT CHECK FRAGEN** - Falsche Antwort = Ablehnung"
        ]

        methodology = TASK_METHODOLOGIES.get(task_type, {})
        if methodology.get('anti_hallucination'):
            rules.extend([
                "**QUOTES WERDEN VERIFIZIERT** - Falsche Zitate = Ablehnung",
                "**HASH MUSS STIMMEN** - Falscher Hash = inkomplettes Lesen vermutet"
            ])

        rules_list = "\n".join(f"{i+1}. {r}" for i, r in enumerate(rules))

        return CRITICAL_SECTION.format(rules_list=rules_list)

    def _get_chunk_paths(self, task_config: dict) -> List[Path]:
        """Get list of chunk file paths for this task."""
        chunk_paths = []

        if 'paper_path' in task_config:
            # Paper analysis - get all chunks
            paper_path = Path(task_config['paper_path'])
            paper_id = task_config.get('paper_id', paper_path.name)

            # Check for _metadata.json to get chunk count
            meta_path = paper_path / "_metadata.json"
            if meta_path.exists():
                with open(meta_path) as f:
                    meta = json.load(f)
                chunk_count = meta.get('chunks', meta.get('total_chunks', 0))
                for i in range(1, chunk_count + 1):
                    chunk_path = paper_path / f"{paper_id}_{i}.md"
                    if chunk_path.exists():
                        chunk_paths.append(chunk_path)
            else:
                # Fallback: glob for chunks
                chunk_paths = sorted(paper_path.glob(f"{paper_id}_*.md"))

        elif 'chunks' in task_config:
            # Batch extraction - specific chunks
            for chunk_info in task_config['chunks']:
                paper_id = chunk_info['paper_id']
                chunk_num = chunk_info['chunk']
                chunk_path = self.project_path / f"02-resources/papers/{paper_id}/{paper_id}_{chunk_num}.md"
                if chunk_path.exists():
                    chunk_paths.append(chunk_path)

        return chunk_paths


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description='Generate dynamic research subagent with forced reading contract'
    )
    parser.add_argument('project_path', type=Path, help='Path to research project')
    parser.add_argument('task_type', choices=['paper_analysis', 'batch_extraction', 'final_synthesis'])
    parser.add_argument('--paper-id', help='Paper ID for paper_analysis task')
    parser.add_argument('--field', help='Field name for batch_extraction task')
    parser.add_argument('--batch-num', type=int, default=1, help='Batch number')
    parser.add_argument('--config', type=Path, help='YAML config file for task')
    parser.add_argument('--output', type=Path, help='Output path for prompt')

    args = parser.parse_args()

    # Build task config
    if args.config and args.config.exists():
        with open(args.config) as f:
            task_config = yaml.safe_load(f)
    else:
        task_config = {}

    # Override with CLI args
    if args.paper_id:
        paper_path = args.project_path / f"02-resources/papers/{args.paper_id}"
        task_config['paper_id'] = args.paper_id
        task_config['paper_path'] = str(paper_path)
        task_config['task_id'] = f"paper_analysis_{args.paper_id}"

    if args.field:
        task_config['field'] = args.field
        task_config['batch_num'] = args.batch_num
        task_config['task_id'] = f"{args.field}_{args.batch_num}"

    # Build prompt
    builder = DynamicSubagentPromptBuilder(args.project_path)
    prompt = builder.build_prompt(args.task_type, task_config)

    # Output
    if args.output:
        output_path = args.output
    else:
        output_dir = args.project_path / "03-working/prompts"
        output_dir.mkdir(parents=True, exist_ok=True)
        task_id = task_config.get('task_id', f"{args.task_type}_{datetime.now().strftime('%H%M%S')}")
        output_path = output_dir / f"_prompt_{task_id}.md"

    output_path.write_text(prompt, encoding='utf-8')

    print(f"✓ Generated prompt: {output_path}")
    print(f"  Domain: {builder.domain}")
    print(f"  Persona: {builder.persona['name']}")
    print(f"  Task: {args.task_type}")

    # Also create as .claude/agents/ subagent if project-level
    agent_dir = args.project_path / ".claude/agents"
    agent_dir.mkdir(parents=True, exist_ok=True)
    agent_path = agent_dir / f"{task_config.get('task_id', args.task_type)}.md"
    agent_path.write_text(prompt, encoding='utf-8')
    print(f"✓ Created agent: {agent_path}")


if __name__ == '__main__':
    main()

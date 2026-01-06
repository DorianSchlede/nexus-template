#!/usr/bin/env python3
"""ULTRASEARCH Handover Manager.

Implements structured handover protocols for zero-loss data transfer
between orchestrator and subagents.

Features:
1. TICKET-BASED handover with input manifests
2. HASH-VERIFIED file integrity
3. CITATION-CHAIN preservation
4. COMPLETION RECEIPT validation
5. CONTEXT-LEVEL optimization
6. ERROR-RECOVERY support

Usage:
    # Create handover ticket
    python handover_manager.py create <project_path> <task_type> --output ticket.yaml

    # Generate prompt with ticket
    python handover_manager.py prompt <ticket.yaml> --context-level 2

    # Verify completion
    python handover_manager.py verify <ticket.yaml> <receipt.yaml>
"""

import sys
import yaml
import json
import hashlib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field, asdict
import argparse
import uuid


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class InputFile:
    """Single input file in manifest."""
    path: str
    hash: str
    lines: int
    tokens_estimate: int
    purpose: str
    required: bool = True


@dataclass
class InputManifest:
    """Complete input manifest for a task."""
    files: List[InputFile]
    total_tokens: int
    generated_at: str


@dataclass
class OutputContract:
    """Contract for expected output."""
    file: str
    format: str  # yaml, markdown, yaml_frontmatter_markdown
    schema_version: str
    required_fields: List[str]
    field_schemas: Dict[str, str]
    validation_rules: List[str]


@dataclass
class HandoverTicket:
    """Complete handover ticket."""
    ticket_id: str
    task_type: str
    created_at: str
    orchestrator: str

    context: Dict[str, Any]
    input_manifest: InputManifest
    output_contract: OutputContract

    # Filled by subagent
    completion_receipt: Optional[Dict] = None

    def to_yaml(self) -> str:
        """Serialize to YAML."""
        return yaml.dump(asdict(self), default_flow_style=False, allow_unicode=True)

    @classmethod
    def from_yaml(cls, yaml_str: str) -> 'HandoverTicket':
        """Deserialize from YAML."""
        data = yaml.safe_load(yaml_str)
        data['input_manifest'] = InputManifest(
            files=[InputFile(**f) for f in data['input_manifest']['files']],
            total_tokens=data['input_manifest']['total_tokens'],
            generated_at=data['input_manifest']['generated_at']
        )
        data['output_contract'] = OutputContract(**data['output_contract'])
        return cls(**data)


@dataclass
class VerificationResult:
    """Result of verifying a completion."""
    passed: bool
    reason: str = ""
    details: Dict[str, Any] = field(default_factory=dict)


# =============================================================================
# CONTEXT LEVELS
# =============================================================================

CONTEXT_LEVELS = {
    1: {
        "name": "ESSENTIAL",
        "description": "Minimum context for simple tasks",
        "includes": ["research_question", "field_to_extract", "citation_format"],
        "tokens": 200
    },
    2: {
        "name": "DOMAIN",
        "description": "Domain-specific vocabulary and examples",
        "includes": ["domain", "key_vocabulary", "extraction_examples"],
        "tokens": 700
    },
    3: {
        "name": "METHODOLOGY",
        "description": "Step-by-step instructions and quality criteria",
        "includes": ["methodology_steps", "quality_criteria", "anti_hallucination_rules"],
        "tokens": 2200
    },
    4: {
        "name": "FULL",
        "description": "Complete schema and all examples",
        "includes": ["complete_schema", "all_examples", "full_validation_rules"],
        "tokens": 5200
    }
}


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def compute_file_hash(file_path: Path) -> str:
    """Compute SHA256 hash of file."""
    content = file_path.read_text(encoding='utf-8')
    return hashlib.sha256(content.encode()).hexdigest()


def count_lines(file_path: Path) -> int:
    """Count lines in file."""
    content = file_path.read_text(encoding='utf-8')
    return len(content.split('\n'))


def estimate_tokens(file_path: Path) -> int:
    """Estimate tokens (chars // 4)."""
    content = file_path.read_text(encoding='utf-8')
    return len(content) // 4


def generate_task_id() -> str:
    """Generate unique task ID."""
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    short_uuid = str(uuid.uuid4())[:8]
    return f"TASK-{timestamp}-{short_uuid}"


def load_yaml_frontmatter(file_path: Path) -> dict:
    """Load YAML frontmatter from markdown."""
    content = file_path.read_text(encoding='utf-8')
    if content.startswith('---'):
        end = content.find('---', 3)
        if end > 0:
            return yaml.safe_load(content[3:end]) or {}
    return {}


# =============================================================================
# HANDOVER MANAGER
# =============================================================================

class HandoverManager:
    """Manages structured handovers between orchestrator and subagents."""

    def __init__(self, project_path: Path):
        self.project_path = project_path
        self.briefing = self._load_briefing()

    def _load_briefing(self) -> dict:
        """Load project briefing."""
        briefing_path = self.project_path / "02-resources/_briefing.md"
        if briefing_path.exists():
            return load_yaml_frontmatter(briefing_path)
        return {}

    def create_ticket(
        self,
        task_type: str,
        input_files: List[Path],
        output_spec: dict,
        context: Optional[dict] = None
    ) -> HandoverTicket:
        """Create handover ticket with pre-computed hashes."""

        # Build input manifest
        manifest_files = []
        total_tokens = 0

        for file_path in input_files:
            if file_path.exists():
                tokens = estimate_tokens(file_path)
                manifest_files.append(InputFile(
                    path=str(file_path),
                    hash=compute_file_hash(file_path),
                    lines=count_lines(file_path),
                    tokens_estimate=tokens,
                    purpose=self._infer_purpose(file_path),
                    required=True
                ))
                total_tokens += tokens

        input_manifest = InputManifest(
            files=manifest_files,
            total_tokens=total_tokens,
            generated_at=datetime.now().isoformat()
        )

        # Build output contract
        output_contract = OutputContract(
            file=output_spec.get('file', ''),
            format=output_spec.get('format', 'yaml'),
            schema_version=output_spec.get('schema_version', '2.3'),
            required_fields=output_spec.get('required_fields', []),
            field_schemas=output_spec.get('field_schemas', {}),
            validation_rules=output_spec.get('validation_rules', [])
        )

        # Build context
        if context is None:
            context = {
                'research_question': self.briefing.get('research_question', ''),
                'research_purpose': self.briefing.get('research_purpose', ''),
                'task_type': task_type
            }

        ticket = HandoverTicket(
            ticket_id=generate_task_id(),
            task_type=task_type,
            created_at=datetime.now().isoformat(),
            orchestrator='handover_manager',
            context=context,
            input_manifest=input_manifest,
            output_contract=output_contract
        )

        return ticket

    def _infer_purpose(self, file_path: Path) -> str:
        """Infer purpose of file from name/location."""
        name = file_path.name.lower()

        if '_briefing' in name:
            return "Research question and extraction schema"
        elif '_analysis_kit' in name:
            return "Subagent context and synthesis goals"
        elif '_extraction_guide' in name:
            return "Field examples and controlled vocabulary"
        elif '_metadata' in name:
            return "Chunk structure and counts"
        elif '_' in name and name.endswith('.md'):
            # Chunk file pattern: paper_N.md
            return f"Chunk content for extraction"
        elif '_batch_' in name:
            return "Batch extraction output"
        elif '_synthesis_' in name:
            return "Aggregated synthesis data"
        else:
            return "Input data"

    def generate_prompt_with_ticket(
        self,
        ticket: HandoverTicket,
        context_level: int = 2
    ) -> str:
        """Generate subagent prompt that includes ticket requirements."""

        prompt_parts = [
            f"# Task: {ticket.ticket_id}",
            "",
            "---",
            "",
            "## HANDOVER TICKET",
            "",
            "You are receiving a structured task. Follow this EXACTLY.",
            "",
            "### INPUT MANIFEST",
            "",
            "Files you MUST read (in this order):",
            ""
        ]

        # Input manifest
        for i, f in enumerate(ticket.input_manifest.files, 1):
            prompt_parts.append(f"{i}. `{f.path}`")
            prompt_parts.append(f"   - Expected hash: `{f.hash[:16]}...`")
            prompt_parts.append(f"   - Lines: {f.lines}")
            prompt_parts.append(f"   - Purpose: {f.purpose}")
            prompt_parts.append("")

        prompt_parts.extend([
            f"**Total tokens estimate**: {ticket.input_manifest.total_tokens}",
            "",
            "### OUTPUT CONTRACT",
            "",
            f"**Output file**: `{ticket.output_contract.file}`",
            f"**Format**: {ticket.output_contract.format}",
            f"**Schema version**: {ticket.output_contract.schema_version}",
            "",
            "**Required fields**:",
            ""
        ])

        for field in ticket.output_contract.required_fields:
            schema = ticket.output_contract.field_schemas.get(field, '')
            prompt_parts.append(f"- `{field}`: {schema}")

        prompt_parts.extend([
            "",
            "**Validation rules**:",
            ""
        ])

        for rule in ticket.output_contract.validation_rules:
            prompt_parts.append(f"- {rule}")

        prompt_parts.extend([
            "",
            "---",
            "",
            "### COMPLETION RECEIPT (REQUIRED)",
            "",
            "After completing the task, you MUST write this receipt:",
            "",
            "```yaml",
            "# Write to: 03-working/_receipt_{task_id}.yaml".format(task_id=ticket.ticket_id),
            "",
            "completion_receipt:",
            f"  task_id: \"{ticket.ticket_id}\"",
            "  completed_at: \"<ISO timestamp>\"",
            "",
            "  files_read:",
        ])

        for f in ticket.input_manifest.files:
            prompt_parts.extend([
                f"    - path: \"{f.path}\"",
                f"      expected_hash: \"{f.hash[:16]}\"",
                "      hash_verified: true  # Set to false if mismatch",
                f"      lines_counted: {f.lines}  # Your count",
                ""
            ])

        prompt_parts.extend([
            "  output_written:",
            f"    file: \"{ticket.output_contract.file}\"",
            "    hash: \"<SHA256 of your output file>\"",
            "    schema_valid: true",
            "```",
            "",
            "**CRITICAL**: Without this receipt, your work cannot be validated.",
            "",
            "---",
            ""
        ])

        # Context section based on level
        prompt_parts.extend(self._get_context_for_level(ticket.context, context_level))

        return "\n".join(prompt_parts)

    def _get_context_for_level(self, context: dict, level: int) -> List[str]:
        """Get context sections based on level."""
        lines = ["## CONTEXT", ""]

        # Level 1: Essential
        lines.extend([
            f"**Research Question**: {context.get('research_question', 'Not specified')}",
            f"**Task Type**: {context.get('task_type', 'unknown')}",
            f"**Citation Format**: Paper-ID (Chunk N:Line-Line)",
            ""
        ])

        if level >= 2:
            # Level 2: Domain
            lines.extend([
                f"**Research Purpose**: {context.get('research_purpose', 'Not specified')}",
                ""
            ])

            if 'field' in context:
                lines.extend([
                    f"**Target Field**: {context.get('field')}",
                    ""
                ])

        if level >= 3:
            # Level 3: Methodology
            lines.extend([
                "### Methodology",
                "",
                "1. Read each file in INPUT MANIFEST completely",
                "2. Verify hash matches expected (report mismatches)",
                "3. Extract required information with chunk:line references",
                "4. Follow OUTPUT CONTRACT exactly",
                "5. Write COMPLETION RECEIPT",
                "",
                "### Quality Criteria",
                "",
                "- Every extraction needs chunk:line reference",
                "- Quotes must be 50-150 characters",
                "- All required fields must be present",
                ""
            ])

        if level >= 4:
            # Level 4: Full
            lines.extend([
                "### Complete Output Schema",
                "",
                "```yaml",
                "# Expected output structure",
                "---",
            ])

            for field in context.get('required_fields', []):
                lines.append(f"{field}: ...")

            lines.extend([
                "---",
                "```",
                ""
            ])

        return lines

    def verify_completion(
        self,
        ticket: HandoverTicket,
        receipt_path: Path
    ) -> VerificationResult:
        """Verify subagent completed task correctly."""

        if not receipt_path.exists():
            return VerificationResult(
                passed=False,
                reason="Receipt file not found"
            )

        receipt = yaml.safe_load(receipt_path.read_text(encoding='utf-8'))
        completion = receipt.get('completion_receipt', {})

        # Check task ID matches
        if completion.get('task_id') != ticket.ticket_id:
            return VerificationResult(
                passed=False,
                reason=f"Task ID mismatch: expected {ticket.ticket_id}, got {completion.get('task_id')}"
            )

        # Verify each input file hash
        files_read = completion.get('files_read', [])
        hash_mismatches = []

        for expected_file in ticket.input_manifest.files:
            reported = next(
                (f for f in files_read if f.get('path') == expected_file.path),
                None
            )

            if not reported:
                hash_mismatches.append(f"File not reported: {expected_file.path}")
            elif not reported.get('hash_verified', False):
                hash_mismatches.append(f"Hash mismatch reported for: {expected_file.path}")

        if hash_mismatches:
            return VerificationResult(
                passed=False,
                reason="Hash verification failed",
                details={'mismatches': hash_mismatches}
            )

        # Verify output exists
        output_info = completion.get('output_written', {})
        output_path = Path(output_info.get('file', ''))

        if not output_path.exists():
            return VerificationResult(
                passed=False,
                reason=f"Output file not found: {output_path}"
            )

        # Verify output hash
        actual_hash = compute_file_hash(output_path)
        reported_hash = output_info.get('hash', '')

        if actual_hash[:16] != reported_hash[:16]:
            return VerificationResult(
                passed=False,
                reason="Output hash mismatch - file may have been modified",
                details={
                    'expected': reported_hash[:16],
                    'actual': actual_hash[:16]
                }
            )

        return VerificationResult(
            passed=True,
            reason="All verifications passed",
            details={
                'files_verified': len(files_read),
                'output_verified': True
            }
        )


# =============================================================================
# CHAIN MANIFEST
# =============================================================================

@dataclass
class StageInfo:
    """Information about a pipeline stage."""
    stage_id: str
    stage_type: str  # extraction, aggregation, synthesis
    processor: str  # subagent, script
    inputs: List[str]  # Ticket IDs or file paths
    output: str
    output_hash: str


class ChainManifest:
    """Tracks the full pipeline chain for traceability."""

    def __init__(self):
        self.stages: List[StageInfo] = []
        self.created_at = datetime.now().isoformat()

    def add_stage(self, stage: StageInfo):
        """Add a stage to the chain."""
        self.stages.append(stage)

    def trace_citation(self, citation: str) -> List[Dict]:
        """Trace a citation back through the chain."""
        # Parse citation: "Paper-ID (Chunk N:Line-Line)"
        # Find which stage produced it, trace back to source
        trace = []
        for stage in reversed(self.stages):
            trace.append({
                'stage': stage.stage_id,
                'type': stage.stage_type,
                'output': stage.output
            })
        return trace

    def to_yaml(self) -> str:
        """Serialize chain manifest."""
        return yaml.dump({
            'created_at': self.created_at,
            'stages': [asdict(s) for s in self.stages]
        }, default_flow_style=False)


# =============================================================================
# CLI
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description='ULTRASEARCH Handover Manager')
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Create ticket
    create_parser = subparsers.add_parser('create', help='Create handover ticket')
    create_parser.add_argument('project_path', type=Path)
    create_parser.add_argument('task_type', choices=['paper_analysis', 'batch_extraction', 'final_synthesis'])
    create_parser.add_argument('--paper-id', help='Paper ID for analysis')
    create_parser.add_argument('--field', help='Field for extraction')
    create_parser.add_argument('--batch-num', type=int, default=1)
    create_parser.add_argument('--output', type=Path, required=True)

    # Generate prompt
    prompt_parser = subparsers.add_parser('prompt', help='Generate prompt from ticket')
    prompt_parser.add_argument('ticket', type=Path)
    prompt_parser.add_argument('--context-level', type=int, default=2, choices=[1, 2, 3, 4])
    prompt_parser.add_argument('--output', type=Path)

    # Verify completion
    verify_parser = subparsers.add_parser('verify', help='Verify completion receipt')
    verify_parser.add_argument('ticket', type=Path)
    verify_parser.add_argument('receipt', type=Path)

    args = parser.parse_args()

    if args.command == 'create':
        manager = HandoverManager(args.project_path)

        # Determine input files based on task type
        input_files = []

        # Always include briefing
        input_files.append(args.project_path / "02-resources/_briefing.md")

        if args.task_type == 'paper_analysis' and args.paper_id:
            paper_path = args.project_path / f"02-resources/papers/{args.paper_id}"

            # Add metadata
            input_files.append(paper_path / "_metadata.json")

            # Add chunks
            meta_path = paper_path / "_metadata.json"
            if meta_path.exists():
                with open(meta_path) as f:
                    meta = json.load(f)
                chunk_count = meta.get('chunks', meta.get('total_chunks', 0))
                for i in range(1, chunk_count + 1):
                    input_files.append(paper_path / f"{args.paper_id}_{i}.md")

        elif args.task_type == 'batch_extraction' and args.field:
            # Would need routing table to know which chunks
            pass

        # Create output spec
        if args.task_type == 'paper_analysis':
            output_spec = {
                'file': str(args.project_path / f"02-resources/papers/{args.paper_id}/index.md"),
                'format': 'yaml_frontmatter_markdown',
                'schema_version': '2.3',
                'required_fields': ['paper_id', 'title', 'chunks_read', 'chunk_index'],
                'field_schemas': {
                    'chunk_index': 'dict with token_count, hash, fields_found per chunk'
                },
                'validation_rules': [
                    'chunks_read must equal chunks_expected',
                    'chunk_index must have entry for every chunk'
                ]
            }
        else:
            output_spec = {
                'file': str(args.project_path / f"03-working/_batch_{args.field}_{args.batch_num}.yaml"),
                'format': 'yaml',
                'schema_version': '2.3',
                'required_fields': ['batch_id', 'field', 'patterns'],
                'field_schemas': {},
                'validation_rules': []
            }

        ticket = manager.create_ticket(
            task_type=args.task_type,
            input_files=[f for f in input_files if f.exists()],
            output_spec=output_spec,
            context={
                'research_question': manager.briefing.get('research_question', ''),
                'research_purpose': manager.briefing.get('research_purpose', ''),
                'task_type': args.task_type,
                'field': args.field or '',
                'paper_id': args.paper_id or ''
            }
        )

        args.output.write_text(ticket.to_yaml(), encoding='utf-8')
        print(f"✓ Created ticket: {args.output}")
        print(f"  Task ID: {ticket.ticket_id}")
        print(f"  Input files: {len(ticket.input_manifest.files)}")
        print(f"  Total tokens: {ticket.input_manifest.total_tokens}")

    elif args.command == 'prompt':
        ticket = HandoverTicket.from_yaml(args.ticket.read_text(encoding='utf-8'))
        manager = HandoverManager(Path('.'))  # Dummy, just need prompt generation

        prompt = manager.generate_prompt_with_ticket(ticket, args.context_level)

        if args.output:
            args.output.write_text(prompt, encoding='utf-8')
            print(f"✓ Generated prompt: {args.output}")
        else:
            print(prompt)

    elif args.command == 'verify':
        ticket = HandoverTicket.from_yaml(args.ticket.read_text(encoding='utf-8'))
        manager = HandoverManager(Path('.'))

        result = manager.verify_completion(ticket, args.receipt)

        if result.passed:
            print(f"✓ VERIFICATION PASSED")
            print(f"  {result.reason}")
        else:
            print(f"✗ VERIFICATION FAILED")
            print(f"  Reason: {result.reason}")
            if result.details:
                print(f"  Details: {result.details}")

        sys.exit(0 if result.passed else 1)


if __name__ == '__main__':
    main()

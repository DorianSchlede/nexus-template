#!/usr/bin/env python3
"""
Research Pipeline Visualizer v7 - Deep Content Extraction
Comprehensive extraction of code blocks, tables, templates, validation checks.
"""

import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Set
from collections import defaultdict

# ============================================================================
# DATA MODELS - Enhanced for rich content
# ============================================================================

@dataclass
class CodeBlock:
    """Represents a code block with language and content."""
    language: str
    content: str
    context: str = ""  # Surrounding text for context

@dataclass
class Table:
    """Represents a markdown table."""
    headers: List[str]
    rows: List[List[str]]
    context: str = ""

@dataclass
class Template:
    """Represents a template or example."""
    name: str
    content: str
    type: str = "template"  # template, example, pattern

@dataclass
class ValidationCheck:
    """Represents a validation check or requirement."""
    check_type: str  # assertion, requirement, must, should
    content: str
    critical: bool = False

@dataclass
class ErrorHandler:
    """Represents error handling instructions."""
    error_type: str
    solution: str

@dataclass
class Script:
    """Represents a script or command."""
    name: str
    command: str
    purpose: str = ""
    parameters: List[str] = field(default_factory=list)

@dataclass
class GapFix:
    """Represents a gap fix reference."""
    gap_id: str  # e.g., "G5", "G13", "G22a"
    description: str
    step_context: str = ""

@dataclass
class ArchitecturePattern:
    """Represents an architecture pattern or algorithm."""
    name: str
    description: str
    code_example: str = ""
    rationale: str = ""

@dataclass
class FileRef:
    """File reference with path and type."""
    path: str
    type: str  # input, output
    description: str = ""

@dataclass
class SubagentConfig:
    """Subagent configuration details."""
    model: str
    timeout: int
    budget: str
    concurrency: int
    purpose: str = ""

@dataclass
class Step:
    """Enhanced step with rich content."""
    number: int
    title: str
    description: str
    phase: str
    skill: str

    # Rich content
    code_blocks: List[CodeBlock] = field(default_factory=list)
    tables: List[Table] = field(default_factory=list)
    templates: List[Template] = field(default_factory=list)
    validation_checks: List[ValidationCheck] = field(default_factory=list)
    error_handlers: List[ErrorHandler] = field(default_factory=list)
    scripts: List[Script] = field(default_factory=list)
    gap_fixes: List[GapFix] = field(default_factory=list)
    architecture_patterns: List[ArchitecturePattern] = field(default_factory=list)

    # Connections
    inputs: List[FileRef] = field(default_factory=list)
    outputs: List[FileRef] = field(default_factory=list)
    subagent: Optional[SubagentConfig] = None
    substeps: List[str] = field(default_factory=list)

    # Metadata
    is_gate: bool = False
    gate_criteria: List[str] = field(default_factory=list)

@dataclass
class Phase:
    """Phase container."""
    letter: str
    title: str
    steps: List[Step] = field(default_factory=list)

@dataclass
class Skill:
    """Skill/orchestrator container."""
    name: str
    description: str
    phases: List[Phase] = field(default_factory=list)
    all_steps: List[Step] = field(default_factory=list)

# ============================================================================
# CONTENT EXTRACTORS - Deep parsing
# ============================================================================

def extract_code_blocks(content: str) -> List[CodeBlock]:
    """Extract code blocks with language and context."""
    blocks = []

    # Pattern: ```language\ncode\n```
    pattern = r'```(\w+)?\n(.*?)\n```'
    matches = re.finditer(pattern, content, re.DOTALL)

    for match in matches:
        language = match.group(1) or "text"
        code = match.group(2).strip()

        # Get context (text before the code block)
        start_pos = match.start()
        context_start = max(0, start_pos - 200)
        context = content[context_start:start_pos].strip()

        # Extract last sentence as context
        if context:
            sentences = re.split(r'[.!?]\s+', context)
            context = sentences[-1] if sentences else context[:100]

        blocks.append(CodeBlock(
            language=language,
            content=code,
            context=context
        ))

    return blocks

def extract_tables(content: str) -> List[Table]:
    """Extract markdown tables."""
    tables = []

    # Find table blocks (lines starting with |)
    lines = content.split('\n')
    i = 0
    while i < len(lines):
        line = lines[i].strip()

        if line.startswith('|') and '|' in line[1:]:
            # Found potential table start
            table_lines = []
            context_start = max(0, i - 3)
            context = '\n'.join(lines[context_start:i]).strip()

            # Collect all table lines
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i].strip())
                i += 1

            if len(table_lines) >= 3:  # Header + separator + at least 1 row
                # Parse table
                headers = [h.strip() for h in table_lines[0].split('|')[1:-1]]
                rows = []

                for row_line in table_lines[2:]:  # Skip separator
                    cells = [c.strip() for c in row_line.split('|')[1:-1]]
                    if cells:
                        rows.append(cells)

                tables.append(Table(
                    headers=headers,
                    rows=rows,
                    context=context
                ))
            continue

        i += 1

    return tables

def extract_templates(content: str) -> List[Template]:
    """Extract templates and examples."""
    templates = []

    # Pattern 1: **Template:** followed by content
    pattern1 = r'\*\*Template[:\s]+([^*]+?)\*\*\s*\n(.*?)(?=\n##|\n\*\*|$)'
    for match in re.finditer(pattern1, content, re.DOTALL | re.IGNORECASE):
        name = match.group(1).strip()
        template_content = match.group(2).strip()
        templates.append(Template(
            name=name,
            content=template_content,
            type="template"
        ))

    # Pattern 2: Example sections
    pattern2 = r'### Example[:\s]+([^\n]+)\n(.*?)(?=\n##|\n###|$)'
    for match in re.finditer(pattern2, content, re.DOTALL | re.IGNORECASE):
        name = match.group(1).strip()
        example_content = match.group(2).strip()
        templates.append(Template(
            name=name,
            content=example_content,
            type="example"
        ))

    # Pattern 3: Format specifications
    pattern3 = r'(?:Format|Structure):\s*\n((?:[-*]\s+.+\n)+)'
    for match in re.finditer(pattern3, content, re.IGNORECASE):
        format_content = match.group(1).strip()
        templates.append(Template(
            name="Format Specification",
            content=format_content,
            type="pattern"
        ))

    return templates

def extract_validation_checks(content: str) -> List[ValidationCheck]:
    """Extract validation checks, requirements, assertions."""
    checks = []

    # Pattern 1: MUST/CRITICAL requirements
    pattern1 = r'(?:MUST|CRITICAL)[:\s]+([^\n]+)'
    for match in re.finditer(pattern1, content, re.IGNORECASE):
        checks.append(ValidationCheck(
            check_type="critical",
            content=match.group(1).strip(),
            critical=True
        ))

    # Pattern 2: Assertion blocks
    pattern2 = r'(?:Assert|Verify|Check)[:\s]+([^\n]+)'
    for match in re.finditer(pattern2, content, re.IGNORECASE):
        checks.append(ValidationCheck(
            check_type="assertion",
            content=match.group(1).strip(),
            critical=False
        ))

    # Pattern 3: SHOULD requirements
    pattern3 = r'SHOULD[:\s]+([^\n]+)'
    for match in re.finditer(pattern3, content, re.IGNORECASE):
        checks.append(ValidationCheck(
            check_type="should",
            content=match.group(1).strip(),
            critical=False
        ))

    # Pattern 4: Numbered validation steps
    pattern4 = r'^\d+\.\s+(?:Verify|Check|Ensure)[:\s]+([^\n]+)'
    for match in re.finditer(pattern4, content, re.MULTILINE | re.IGNORECASE):
        checks.append(ValidationCheck(
            check_type="requirement",
            content=match.group(1).strip(),
            critical=False
        ))

    return checks

def extract_error_handlers(content: str) -> List[ErrorHandler]:
    """Extract error handling instructions."""
    handlers = []

    # Pattern 1: Error tables (Error | Solution format)
    tables = extract_tables(content)
    for table in tables:
        if len(table.headers) >= 2:
            error_col = None
            solution_col = None

            # Find error and solution columns
            for i, header in enumerate(table.headers):
                if re.search(r'error|issue|problem', header, re.IGNORECASE):
                    error_col = i
                if re.search(r'solution|fix|action', header, re.IGNORECASE):
                    solution_col = i

            if error_col is not None and solution_col is not None:
                for row in table.rows:
                    if len(row) > max(error_col, solution_col):
                        handlers.append(ErrorHandler(
                            error_type=row[error_col],
                            solution=row[solution_col]
                        ))

    # Pattern 2: "If X, then Y" error handling
    pattern2 = r'If\s+(.+?),\s+(?:then\s+)?(.+?)(?:\.|$)'
    for match in re.finditer(pattern2, content, re.IGNORECASE):
        error = match.group(1).strip()
        solution = match.group(2).strip()
        if any(word in error.lower() for word in ['error', 'fail', 'timeout', 'missing']):
            handlers.append(ErrorHandler(
                error_type=error,
                solution=solution
            ))

    return handlers

def extract_scripts(content: str) -> List[Script]:
    """Extract script commands and execution details."""
    scripts = []

    # Pattern 1: python script.py commands
    pattern1 = r'python\s+([^\s]+\.py)(?:\s+([^\n]+))?'
    for match in re.finditer(pattern1, content):
        script_name = match.group(1)
        params = match.group(2).strip() if match.group(2) else ""

        # Get context (lines before command)
        start_pos = match.start()
        context_start = max(0, start_pos - 200)
        context = content[context_start:start_pos]

        # Extract purpose from context
        purpose_match = re.search(r'(?:Purpose|Script)[:\s]+([^\n]+)', context, re.IGNORECASE)
        purpose = purpose_match.group(1).strip() if purpose_match else ""

        scripts.append(Script(
            name=script_name,
            command=f"python {script_name} {params}".strip(),
            purpose=purpose,
            parameters=params.split() if params else []
        ))

    # Pattern 2: bash script.sh commands
    pattern2 = r'bash\s+([^\s]+\.sh)(?:\s+([^\n]+))?'
    for match in re.finditer(pattern2, content):
        script_name = match.group(1)
        params = match.group(2).strip() if match.group(2) else ""

        scripts.append(Script(
            name=script_name,
            command=f"bash {script_name} {params}".strip(),
            purpose="",
            parameters=params.split() if params else []
        ))

    return scripts

def extract_gap_fixes(content: str) -> List[GapFix]:
    """Extract gap fix references."""
    gaps = []

    # Pattern: Gap GXX or G##x format
    pattern = r'\b(G(?:ap\s+)?([G0-9]+[a-z]?))[:\s]+(.*?)(?:\n|$)'
    for match in re.finditer(pattern, content, re.IGNORECASE):
        gap_id = match.group(2).upper()
        description = match.group(3).strip()

        # Get broader context
        start_pos = match.start()
        context_start = max(0, start_pos - 100)
        context_end = min(len(content), match.end() + 200)
        step_context = content[context_start:context_end].strip()

        gaps.append(GapFix(
            gap_id=gap_id,
            description=description,
            step_context=step_context[:300]
        ))

    return gaps

def extract_architecture_patterns(content: str) -> List[ArchitecturePattern]:
    """Extract architecture patterns and algorithms."""
    patterns = []

    # Pattern 1: Algorithm sections
    algo_pattern = r'(?:Algorithm|Pattern)[:\s]+([^\n]+)\n(.*?)(?=\n##|\n\*\*|$)'
    for match in re.finditer(algo_pattern, content, re.DOTALL | re.IGNORECASE):
        name = match.group(1).strip()
        description = match.group(2).strip()[:500]

        # Check if followed by code block
        code_match = re.search(r'```\w*\n(.*?)\n```', description, re.DOTALL)
        code_example = code_match.group(1) if code_match else ""

        patterns.append(ArchitecturePattern(
            name=name,
            description=description,
            code_example=code_example,
            rationale=""
        ))

    # Pattern 2: Level X: descriptions (for 7-level architecture)
    level_pattern = r'(?:Level|L)(\d+)[:\s]+([^\n]+)\n(.*?)(?=\n(?:Level|L)\d+|\n##|$)'
    for match in re.finditer(level_pattern, content, re.DOTALL | re.IGNORECASE):
        level_num = match.group(1)
        name = match.group(2).strip()
        description = match.group(3).strip()[:400]

        patterns.append(ArchitecturePattern(
            name=f"Level {level_num}: {name}",
            description=description,
            code_example="",
            rationale=""
        ))

    return patterns

def extract_description(content: str, max_chars: int = 800) -> str:
    """Extract meaningful description from step content - enhanced."""
    lines = []
    in_code_block = False

    for line in content.split('\n'):
        stripped = line.strip()

        # Skip empty lines
        if not stripped:
            continue

        # Track code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue

        # Skip content inside code blocks
        if in_code_block:
            continue

        # Skip headers
        if stripped.startswith('#'):
            continue

        # Handle bold text like **Use skill:** - extract the text
        if stripped.startswith('**') and '**' in stripped[2:]:
            match = re.match(r'\*\*(.+?)\*\*[:\s]*(.*)', stripped)
            if match:
                text = match.group(1)
                rest = match.group(2).strip()
                if rest:
                    lines.append(f"{text}: {rest}")
                else:
                    lines.append(text)
                continue

        # Skip lines that are just markdown syntax
        if re.match(r'^[\*\-\+>]+\s*$', stripped):
            continue

        # Handle list items - keep the content
        if re.match(r'^[\*\-\+]\s+', stripped):
            text = re.sub(r'^[\*\-\+]\s+', '', stripped)
            if text and not text.startswith('**'):
                lines.append(text)
            continue

        # Regular text
        lines.append(stripped)

        # Stop if we have enough
        total = sum(len(l) for l in lines)
        if total > max_chars:
            break

    result = ' '.join(lines)
    if len(result) > max_chars:
        result = result[:max_chars] + '...'

    return result

def extract_files(content: str, file_type: str) -> List[FileRef]:
    """Extract file references - inputs vs outputs based on context."""
    files = []
    seen = set()

    if file_type == "input":
        # Input-specific patterns - very strict to avoid false positives
        patterns = [
            r'(?:from|using|reads?)\s+`([^`]+(?:\.md|\.yaml|\.json))`',
            r'Use template from[:\s]+`([^`]+)`',
            r'Reads?[:\s]+`([^`]+(?:\.md|\.yaml|\.json))`',
            r'MUST\s+[Rr]ead[^`]*`([^`]+(?:\.md|\.yaml|\.json))`',
            r'(?:Input|Source)[:\s]+`([^`]+(?:\.md|\.yaml|\.json))`',
        ]
    else:
        # Output-specific patterns - strict to real outputs
        patterns = [
            r'\*\*Output\*\*[:\s]+`([^`]+)`',
            r'^Output[:\s]+`([^`]+)`',
            r'Creates?[:\s]+`([^`]+(?:\.md|\.yaml|\.json))`',
            r'[Ww]rite\s+(?:to\s+)?`([^`]+(?:\.md|\.yaml|\.json))`',
            r'^\s*[→>]\s*`([^`]+(?:\.md|\.yaml|\.json))`',
            r'Generates?[:\s]+`([^`]+(?:\.md|\.yaml|\.json))`',
        ]

    for pattern in patterns:
        for match in re.finditer(pattern, content, re.MULTILINE):
            path = match.group(1)

            # Skip if already seen
            key = f"{file_type}:{path}"
            if key in seen:
                continue
            seen.add(key)

            # Extract description from context
            match_pos = match.start()
            context_start = max(0, match_pos - 100)
            context = content[context_start:match_pos + 200]

            # Get sentence containing the file
            sentences = re.split(r'[.!?\n]+', context)
            description = ""
            for sent in sentences:
                if path in sent:
                    description = sent.strip()
                    break

            files.append(FileRef(
                path=path,
                type=file_type,
                description=description[:200] if description else ""
            ))

    # Deduplicate - if file appears as both input and output, prefer output
    if file_type == "output":
        output_paths = {f.path for f in files}
        # This will be used in the calling code to filter inputs

    return files

def extract_subagent_config(content: str) -> Optional[SubagentConfig]:
    """Extract subagent configuration if present."""
    # Look for subagent configuration patterns
    patterns = {
        'model': r'model[:\s]+(?:`)?([^`\n]+)',
        'timeout': r'timeout[:\s]+(\d+)\s*(?:min|minutes)',
        'budget': r'(?:token\s+)?budget[:\s]+([0-9,]+k?)',
        'concurrency': r'(?:max|concurrent)[:\s]+(\d+)\s+(?:subagents?|concurrent)',
    }

    config = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            value = match.group(1).strip('`').strip()
            if key == 'timeout':
                config[key] = int(value)
            elif key == 'concurrency':
                config[key] = int(value)
            else:
                config[key] = value

    if config:
        # Extract purpose
        purpose_match = re.search(r'(?:purpose|spawns?)[:\s]+([^\n.]+)', content, re.IGNORECASE)
        purpose = purpose_match.group(1).strip() if purpose_match else ""

        return SubagentConfig(
            model=config.get('model', 'sonnet'),
            timeout=config.get('timeout', 5),
            budget=config.get('budget', '70k'),
            concurrency=config.get('concurrency', 15),
            purpose=purpose
        )

    return None

def extract_substeps(content: str) -> List[str]:
    """Extract sub-steps or numbered actions within a step."""
    substeps = []

    # Pattern: numbered items (1., 2., etc.)
    pattern = r'^\s*(\d+)\.\s+([^\n]+)'
    for match in re.finditer(pattern, content, re.MULTILINE):
        substeps.append(match.group(2).strip())

    return substeps

def extract_gate_criteria(content: str) -> List[str]:
    """Extract gate criteria/conditions."""
    criteria = []

    # Pattern: checkbox items or criteria lists
    patterns = [
        r'^\s*[-*]\s*\[\s*\]\s+([^\n]+)',  # [ ] checkbox
        r'^\s*[-*]\s+(?:Criterion|Criteria|Condition)[:\s]+([^\n]+)',
        r'^\s*\d+\.\s+(?:Check|Verify|Ensure)[:\s]+([^\n]+)',
    ]

    for pattern in patterns:
        for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
            criteria.append(match.group(1).strip())

    return criteria

# ============================================================================
# STEP PARSING - Enhanced with rich content
# ============================================================================

def parse_step_content(step_num: int, title: str, content: str, phase: str, skill: str) -> Step:
    """Parse step content and extract all rich content."""

    # Check if this is a gate
    is_gate = 'gate' in title.lower()

    # Extract all content types
    code_blocks = extract_code_blocks(content)
    tables = extract_tables(content)
    templates = extract_templates(content)
    validation_checks = extract_validation_checks(content)
    error_handlers = extract_error_handlers(content)
    scripts = extract_scripts(content)
    gap_fixes = extract_gap_fixes(content)
    architecture_patterns = extract_architecture_patterns(content)

    # Extract file references
    inputs = extract_files(content, "input")
    outputs = extract_files(content, "output")

    # Deduplicate: remove inputs that also appear as outputs
    output_paths = {f.path for f in outputs}
    inputs = [f for f in inputs if f.path not in output_paths]

    # Extract other metadata
    subagent = extract_subagent_config(content)
    substeps = extract_substeps(content)
    gate_criteria = extract_gate_criteria(content) if is_gate else []

    # Extract description (cleaned text)
    description = extract_description(content)

    return Step(
        number=step_num,
        title=title,
        description=description,
        phase=phase,
        skill=skill,
        code_blocks=code_blocks,
        tables=tables,
        templates=templates,
        validation_checks=validation_checks,
        error_handlers=error_handlers,
        scripts=scripts,
        gap_fixes=gap_fixes,
        architecture_patterns=architecture_patterns,
        inputs=inputs,
        outputs=outputs,
        subagent=subagent,
        substeps=substeps,
        is_gate=is_gate,
        gate_criteria=gate_criteria
    )

def parse_skill(skill_path: Path) -> Skill:
    """Parse a SKILL.md file and extract all content."""
    content = skill_path.read_text(encoding='utf-8')

    # Extract YAML frontmatter
    yaml_match = re.search(r'^---\n(.*?)\n---', content, re.DOTALL)
    metadata = {}
    if yaml_match:
        try:
            metadata = yaml.safe_load(yaml_match.group(1))
        except:
            pass

    skill_name = metadata.get('name', skill_path.parent.name)
    skill_desc = metadata.get('description', '')

    # Find all phase headers
    phase_pattern = r'^# PHASE\s+([A-Z])[:\s]+(.+)$'
    phase_matches = list(re.finditer(phase_pattern, content, re.MULTILINE | re.IGNORECASE))

    # Find all step headers
    step_pattern = r'^## Step\s+(\d+)[:\s]+(.+)$'
    step_matches = list(re.finditer(step_pattern, content, re.MULTILINE | re.IGNORECASE))

    phases = []
    all_steps = []

    # Create phases
    for i, phase_match in enumerate(phase_matches):
        phase_letter = phase_match.group(1).upper()
        phase_title = phase_match.group(2).strip()

        phase = Phase(
            letter=phase_letter,
            title=phase_title
        )
        phases.append(phase)

    # Parse each step
    current_phase_idx = 0
    for i, step_match in enumerate(step_matches):
        step_num = int(step_match.group(1))
        step_title = step_match.group(2).strip()

        # Extract content for this step (from current step to next step or end)
        start_pos = step_match.end()
        if i + 1 < len(step_matches):
            end_pos = step_matches[i + 1].start()
        else:
            end_pos = len(content)

        step_content = content[start_pos:end_pos]

        # Determine which phase this step belongs to
        step_pos = step_match.start()
        phase_label = "?"

        for j, phase_match in enumerate(phase_matches):
            if phase_match.start() <= step_pos:
                if j + 1 < len(phase_matches):
                    if step_pos < phase_matches[j + 1].start():
                        phase_label = phase_matches[j].group(1).upper()
                        current_phase_idx = j
                        break
                else:
                    phase_label = phase_matches[j].group(1).upper()
                    current_phase_idx = j
                    break

        # Parse step with content extraction
        step = parse_step_content(
            step_num=step_num,
            title=step_title,
            content=step_content,
            phase=phase_label,
            skill=skill_name
        )

        # Add to appropriate phase
        if current_phase_idx < len(phases):
            phases[current_phase_idx].steps.append(step)

        all_steps.append(step)

    return Skill(
        name=skill_name,
        description=skill_desc,
        phases=phases,
        all_steps=all_steps
    )

# ============================================================================
# HTML GENERATION - Enhanced with rich content display
# ============================================================================

def generate_html(skills: List[Skill], output_path: Path):
    """Generate comprehensive HTML visualization with all extracted content."""

    # Collect stats
    total_steps = sum(len(s.all_steps) for s in skills)
    total_phases = sum(len(s.phases) for s in skills)
    total_files = len(set(
        f.path for skill in skills
        for step in skill.all_steps
        for f in step.inputs + step.outputs
    ))
    total_code_blocks = sum(
        len(step.code_blocks)
        for skill in skills
        for step in skill.all_steps
    )
    total_tables = sum(
        len(step.tables)
        for skill in skills
        for step in skill.all_steps
    )
    total_validations = sum(
        len(step.validation_checks)
        for skill in skills
        for step in skill.all_steps
    )
    total_scripts = sum(
        len(step.scripts)
        for skill in skills
        for step in skill.all_steps
    )
    total_gaps = sum(
        len(step.gap_fixes)
        for skill in skills
        for step in skill.all_steps
    )
    total_patterns = sum(
        len(step.architecture_patterns)
        for skill in skills
        for step in skill.all_steps
    )

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Pipeline v8 - Complete Documentation</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        :root {{
            --bg-primary: #0a0e27;
            --bg-secondary: #141937;
            --bg-tertiary: #1e2447;
            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;
            --text-primary: #e2e8f0;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border: #2d3554;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }}

        /* HERO SECTION */
        .hero {{
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
            padding: 3rem 2rem;
            border-bottom: 2px solid var(--border);
        }}

        .hero h1 {{
            font-size: 2.5rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .hero p {{
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 2rem;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            max-width: 1200px;
        }}

        .stat-card {{
            background: var(--bg-tertiary);
            padding: 1.5rem;
            border-radius: 8px;
            border: 1px solid var(--border);
        }}

        .stat-value {{
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent-blue);
            display: block;
        }}

        .stat-label {{
            color: var(--text-muted);
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        /* LAYOUT */
        .container {{
            display: flex;
            max-width: 100vw;
            min-height: calc(100vh - 200px);
        }}

        .sidebar {{
            width: 300px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            position: sticky;
            top: 0;
            height: 100vh;
            overflow-y: auto;
            padding: 2rem 1rem;
        }}

        .main-content {{
            flex: 1;
            padding: 2rem;
            overflow-y: auto;
        }}

        /* SIDEBAR NAV */
        .nav-section {{
            margin-bottom: 2rem;
        }}

        .nav-section h3 {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-bottom: 0.5rem;
            padding: 0.5rem;
        }}

        .nav-item {{
            padding: 0.75rem 1rem;
            margin-bottom: 0.25rem;
            border-radius: 6px;
            cursor: pointer;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }}

        .nav-item:hover {{
            background: var(--bg-tertiary);
            border-left-color: var(--accent-blue);
        }}

        .nav-item.active {{
            background: var(--bg-tertiary);
            border-left-color: var(--accent-purple);
        }}

        .nav-step-num {{
            display: inline-block;
            width: 30px;
            height: 30px;
            background: var(--accent-blue);
            color: white;
            border-radius: 50%;
            text-align: center;
            line-height: 30px;
            font-weight: bold;
            margin-right: 0.5rem;
            font-size: 0.9rem;
        }}

        .nav-gate .nav-step-num {{
            background: var(--accent-yellow);
        }}

        /* SKILL SECTIONS */
        .skill-section {{
            margin-bottom: 4rem;
        }}

        .skill-header {{
            background: var(--bg-secondary);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border: 1px solid var(--border);
        }}

        .skill-header h2 {{
            font-size: 2rem;
            margin-bottom: 0.5rem;
            color: var(--accent-blue);
        }}

        /* PHASE SECTIONS */
        .phase-section {{
            margin-bottom: 3rem;
        }}

        .phase-header {{
            background: var(--bg-tertiary);
            padding: 1rem 1.5rem;
            border-radius: 8px;
            margin-bottom: 1.5rem;
            border-left: 4px solid var(--accent-purple);
        }}

        .phase-header h3 {{
            font-size: 1.5rem;
            color: var(--accent-purple);
        }}

        /* STEP CARDS */
        .step-card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            transition: all 0.3s;
        }}

        .step-card:hover {{
            border-color: var(--accent-blue);
            box-shadow: 0 4px 20px rgba(59, 130, 246, 0.1);
        }}

        .step-card.gate {{
            border-left: 4px solid var(--accent-yellow);
            background: linear-gradient(135deg, var(--bg-secondary) 0%, rgba(245, 158, 11, 0.05) 100%);
        }}

        .step-header {{
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
            gap: 1rem;
        }}

        .step-number {{
            width: 50px;
            height: 50px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: white;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: bold;
            flex-shrink: 0;
        }}

        .step-card.gate .step-number {{
            background: linear-gradient(135deg, var(--accent-yellow), var(--accent-red));
        }}

        .step-title {{
            flex: 1;
        }}

        .step-title h4 {{
            font-size: 1.5rem;
            margin-bottom: 0.25rem;
        }}

        .step-meta {{
            color: var(--text-muted);
            font-size: 0.9rem;
        }}

        .step-description {{
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
            line-height: 1.8;
        }}

        /* CONTENT SECTIONS */
        .content-section {{
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
        }}

        .content-section-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 1rem;
            cursor: pointer;
            padding: 0.75rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
            transition: all 0.2s;
        }}

        .content-section-header:hover {{
            background: rgba(59, 130, 246, 0.1);
        }}

        .content-section-title {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-weight: 600;
            color: var(--accent-blue);
        }}

        .content-badge {{
            background: var(--accent-blue);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.8rem;
            font-weight: bold;
        }}

        .expand-icon {{
            color: var(--text-muted);
            transition: transform 0.2s;
        }}

        .content-section-body {{
            margin-top: 1rem;
            display: none;
        }}

        .content-section-body.expanded {{
            display: block;
        }}

        .content-section-header.expanded .expand-icon {{
            transform: rotate(90deg);
        }}

        /* CODE BLOCKS */
        .code-block {{
            margin-bottom: 1.5rem;
        }}

        .code-header {{
            background: var(--bg-tertiary);
            padding: 0.75rem 1rem;
            border-radius: 6px 6px 0 0;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border: 1px solid var(--border);
            border-bottom: none;
        }}

        .code-language {{
            color: var(--accent-green);
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
        }}

        .code-context {{
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        .code-content {{
            background: #0d1117;
            padding: 1rem;
            border-radius: 0 0 6px 6px;
            border: 1px solid var(--border);
            overflow-x: auto;
        }}

        .code-content pre {{
            margin: 0;
            color: #c9d1d9;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
            line-height: 1.6;
        }}

        /* TABLES */
        .table-wrapper {{
            margin-bottom: 1.5rem;
            overflow-x: auto;
        }}

        .table-context {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
            padding: 0.5rem;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            background: var(--bg-tertiary);
            border-radius: 6px;
            overflow: hidden;
        }}

        th {{
            background: var(--bg-primary);
            padding: 0.75rem 1rem;
            text-align: left;
            color: var(--accent-blue);
            font-weight: 600;
            border-bottom: 2px solid var(--border);
        }}

        td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid var(--border);
        }}

        tr:last-child td {{
            border-bottom: none;
        }}

        tr:hover {{
            background: rgba(59, 130, 246, 0.05);
        }}

        /* TEMPLATES */
        .template-item {{
            margin-bottom: 1.5rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
            padding: 1rem;
            border-left: 3px solid var(--accent-purple);
        }}

        .template-header {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 0.75rem;
        }}

        .template-type {{
            background: var(--accent-purple);
            color: white;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            text-transform: uppercase;
        }}

        .template-name {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        .template-content {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            white-space: pre-wrap;
        }}

        /* VALIDATION CHECKS */
        .validation-list {{
            list-style: none;
        }}

        .validation-item {{
            padding: 0.75rem 1rem;
            margin-bottom: 0.5rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
            border-left: 3px solid var(--accent-green);
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        }}

        .validation-item.critical {{
            border-left-color: var(--accent-red);
            background: rgba(239, 68, 68, 0.05);
        }}

        .validation-icon {{
            flex-shrink: 0;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: var(--accent-green);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            margin-top: 0.1rem;
        }}

        .validation-item.critical .validation-icon {{
            background: var(--accent-red);
        }}

        .validation-type {{
            display: inline-block;
            background: var(--accent-green);
            color: white;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            text-transform: uppercase;
            margin-right: 0.5rem;
        }}

        .validation-item.critical .validation-type {{
            background: var(--accent-red);
        }}

        /* ERROR HANDLERS */
        .error-handler {{
            margin-bottom: 1rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}

        .error-type {{
            background: rgba(239, 68, 68, 0.1);
            padding: 0.75rem 1rem;
            color: var(--accent-red);
            font-weight: 600;
            border-bottom: 1px solid var(--border);
        }}

        .error-solution {{
            padding: 0.75rem 1rem;
            color: var(--text-secondary);
        }}

        /* FILES */
        .file-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            margin-bottom: 1rem;
        }}

        .file-ref {{
            background: var(--bg-tertiary);
            padding: 0.5rem 1rem;
            border-radius: 6px;
            border: 1px solid var(--border);
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
        }}

        .file-ref.input {{
            border-left: 3px solid var(--accent-blue);
        }}

        .file-ref.output {{
            border-left: 3px solid var(--accent-green);
        }}

        /* SUBAGENT CONFIG */
        .subagent-config {{
            background: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 6px;
            border-left: 3px solid var(--accent-purple);
        }}

        .config-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            margin-top: 0.75rem;
        }}

        .config-item {{
            display: flex;
            flex-direction: column;
        }}

        .config-label {{
            color: var(--text-muted);
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .config-value {{
            color: var(--text-primary);
            font-weight: 600;
            margin-top: 0.25rem;
        }}

        /* SUBSTEPS */
        .substeps-list {{
            list-style: none;
            counter-reset: substep;
        }}

        .substep-item {{
            counter-increment: substep;
            padding: 0.75rem 1rem;
            padding-left: 3rem;
            margin-bottom: 0.5rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
            position: relative;
        }}

        .substep-item::before {{
            content: counter(substep);
            position: absolute;
            left: 1rem;
            width: 24px;
            height: 24px;
            background: var(--accent-blue);
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: bold;
        }}

        /* SCRIPTS */
        .script-item {{
            margin-bottom: 1rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
            padding: 1rem;
            border-left: 3px solid var(--accent-blue);
        }}

        .script-header {{
            margin-bottom: 0.5rem;
        }}

        .script-name {{
            font-family: 'Consolas', 'Monaco', monospace;
            font-weight: 600;
            color: var(--accent-blue);
            font-size: 1.1rem;
        }}

        .script-purpose {{
            color: var(--text-secondary);
            margin-bottom: 0.75rem;
            font-size: 0.95rem;
        }}

        .script-command {{
            background: #0d1117;
            padding: 0.75rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
        }}

        .script-command code {{
            color: #c9d1d9;
            font-family: 'Consolas', 'Monaco', monospace;
        }}

        .script-params {{
            color: var(--text-muted);
            font-size: 0.85rem;
        }}

        .script-params code {{
            background: var(--bg-primary);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            color: var(--accent-green);
        }}

        /* GAP FIXES */
        .gap-fix-item {{
            margin-bottom: 1rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
            padding: 1rem;
            border-left: 3px solid var(--accent-yellow);
        }}

        .gap-fix-header {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }}

        .gap-id {{
            background: var(--accent-yellow);
            color: var(--bg-primary);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.85rem;
        }}

        .gap-description {{
            color: var(--text-primary);
            font-weight: 600;
        }}

        .gap-context {{
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 0.5rem;
            padding: 0.75rem;
            background: rgba(245, 158, 11, 0.05);
            border-radius: 4px;
        }}

        /* ARCHITECTURE PATTERNS */
        .pattern-item {{
            margin-bottom: 1.5rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
            padding: 1rem;
            border-left: 3px solid var(--accent-purple);
        }}

        .pattern-header {{
            margin-bottom: 0.75rem;
        }}

        .pattern-name {{
            font-weight: 600;
            color: var(--accent-purple);
            font-size: 1.1rem;
        }}

        .pattern-description {{
            color: var(--text-secondary);
            margin-bottom: 0.75rem;
            line-height: 1.6;
        }}

        .pattern-code {{
            background: #0d1117;
            padding: 1rem;
            border-radius: 4px;
            margin-top: 0.75rem;
        }}

        .pattern-code pre {{
            margin: 0;
        }}

        .pattern-code code {{
            color: #c9d1d9;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.85rem;
        }}

        /* GATE CRITERIA */
        .criteria-list {{
            list-style: none;
        }}

        .criteria-item {{
            padding: 0.75rem 1rem;
            padding-left: 3rem;
            margin-bottom: 0.5rem;
            background: rgba(245, 158, 11, 0.05);
            border-radius: 6px;
            border-left: 3px solid var(--accent-yellow);
            position: relative;
        }}

        .criteria-item::before {{
            content: '✓';
            position: absolute;
            left: 1rem;
            color: var(--accent-yellow);
            font-size: 1.2rem;
            font-weight: bold;
        }}

        /* SCROLLBAR */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}

        ::-webkit-scrollbar-track {{
            background: var(--bg-primary);
        }}

        ::-webkit-scrollbar-thumb {{
            background: var(--border);
            border-radius: 4px;
        }}

        ::-webkit-scrollbar-thumb:hover {{
            background: var(--accent-blue);
        }}

        /* OVERVIEW PANEL */
        .overview-panel {{
            background: var(--bg-secondary);
            border: 2px solid var(--accent-purple);
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem auto;
            max-width: 1200px;
        }}

        .overview-title {{
            font-size: 1.8rem;
            color: var(--accent-purple);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .overview-title::before {{
            content: '📋';
            font-size: 2rem;
        }}

        .overview-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }}

        .overview-section {{
            background: var(--bg-tertiary);
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid var(--accent-blue);
        }}

        .overview-section-title {{
            font-size: 1.2rem;
            color: var(--accent-blue);
            margin-bottom: 0.75rem;
            font-weight: 600;
        }}

        .overview-section p {{
            color: var(--text-secondary);
            line-height: 1.8;
            margin-bottom: 0.5rem;
        }}

        .overview-list {{
            list-style: none;
            padding-left: 0;
        }}

        .overview-list li {{
            padding: 0.5rem 0;
            color: var(--text-secondary);
            border-bottom: 1px solid var(--border);
        }}

        .overview-list li:last-child {{
            border-bottom: none;
        }}

        .overview-list li::before {{
            content: '→ ';
            color: var(--accent-blue);
            font-weight: bold;
            margin-right: 0.5rem;
        }}

        /* LEGEND */
        .legend-panel {{
            background: var(--bg-secondary);
            border: 2px solid var(--accent-green);
            border-radius: 12px;
            padding: 2rem;
            margin: 2rem auto;
            max-width: 1200px;
        }}

        .legend-title {{
            font-size: 1.6rem;
            color: var(--accent-green);
            margin-bottom: 1.5rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }}

        .legend-title::before {{
            content: '🗺️';
            font-size: 1.8rem;
        }}

        .legend-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 1rem;
        }}

        .legend-item {{
            display: flex;
            align-items: center;
            gap: 1rem;
            padding: 1rem;
            background: var(--bg-tertiary);
            border-radius: 6px;
        }}

        .legend-icon {{
            font-size: 1.5rem;
            min-width: 40px;
            text-align: center;
        }}

        .legend-text {{
            flex: 1;
        }}

        .legend-label {{
            font-weight: 600;
            color: var(--text-primary);
            display: block;
            margin-bottom: 0.25rem;
        }}

        .legend-desc {{
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        /* HELP TOOLTIP */
        .help-tooltip {{
            position: relative;
            display: inline-block;
            cursor: help;
            color: var(--accent-yellow);
            margin-left: 0.5rem;
            font-size: 0.9rem;
        }}

        .help-tooltip:hover::after {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: 125%;
            left: 50%;
            transform: translateX(-50%);
            background: var(--bg-primary);
            color: var(--text-primary);
            padding: 0.75rem 1rem;
            border-radius: 6px;
            border: 1px solid var(--accent-yellow);
            white-space: nowrap;
            z-index: 1000;
            font-size: 0.85rem;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}

        .help-tooltip:hover::before {{
            content: '';
            position: absolute;
            bottom: 115%;
            left: 50%;
            transform: translateX(-50%);
            border: 6px solid transparent;
            border-top-color: var(--accent-yellow);
            z-index: 1000;
        }}

        /* PHASE DIVIDER */
        .phase-divider {{
            margin: 3rem 0 2rem 0;
            padding: 1.5rem;
            background: linear-gradient(90deg, transparent, var(--bg-secondary), transparent);
            border-top: 2px solid var(--accent-purple);
            border-bottom: 2px solid var(--accent-purple);
            text-align: center;
        }}

        .phase-divider-title {{
            font-size: 1.8rem;
            color: var(--accent-purple);
            font-weight: 700;
            letter-spacing: 2px;
            text-transform: uppercase;
        }}

        .phase-divider-desc {{
            color: var(--text-secondary);
            margin-top: 0.5rem;
            font-size: 1.1rem;
        }}

        /* CONTENT BADGES */
        .content-type-badge {{
            display: inline-block;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-right: 0.5rem;
        }}

        .badge-code {{ background: rgba(59, 130, 246, 0.2); color: var(--accent-blue); }}
        .badge-table {{ background: rgba(16, 185, 129, 0.2); color: var(--accent-green); }}
        .badge-validation {{ background: rgba(245, 158, 11, 0.2); color: var(--accent-yellow); }}
        .badge-script {{ background: rgba(139, 92, 246, 0.2); color: var(--accent-purple); }}
        .badge-gap {{ background: rgba(239, 68, 68, 0.2); color: var(--accent-red); }}
        .badge-pattern {{ background: rgba(236, 72, 153, 0.2); color: #ec4899; }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Research Pipeline v8</h1>
        <p>Complete Documentation - Ultra-Clear Workflow Visualization with Full Context</p>
        <div class="stats-grid">
            <div class="stat-card">
                <span class="stat-value">{len(skills)}</span>
                <span class="stat-label">Orchestrators</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_phases}</span>
                <span class="stat-label">Phases</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_steps}</span>
                <span class="stat-label">Steps</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_files}</span>
                <span class="stat-label">Files</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_code_blocks}</span>
                <span class="stat-label">Code Blocks</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_tables}</span>
                <span class="stat-label">Tables</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_validations}</span>
                <span class="stat-label">Validations</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_scripts}</span>
                <span class="stat-label">Scripts</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_gaps}</span>
                <span class="stat-label">Gap Fixes</span>
            </div>
            <div class="stat-card">
                <span class="stat-value">{total_patterns}</span>
                <span class="stat-label">Patterns</span>
            </div>
        </div>
    </div>

    <!-- OVERVIEW PANEL -->
    <div class="overview-panel">
        <div class="overview-title">Pipeline Architecture Overview</div>
        <div class="overview-grid">
            <div class="overview-section">
                <div class="overview-section-title">📥 Phase 1: Create (Acquisition)</div>
                <p><strong>Purpose:</strong> Collect and organize research papers with AI-powered field suggestions</p>
                <ul class="overview-list">
                    <li>Initialize project structure with metadata</li>
                    <li>Download papers with URL resolution priority</li>
                    <li>Organize into standardized folder structure</li>
                    <li>Auto-generate research fields using AI (Gap G5)</li>
                </ul>
            </div>
            <div class="overview-section">
                <div class="overview-section-title">🔍 Phase 2: Analyze (Deep Extraction)</div>
                <p><strong>Purpose:</strong> Extract structured data from papers using multi-agent parallel processing</p>
                <ul class="overview-list">
                    <li>Chunk papers into processable segments</li>
                    <li>Spawn parallel subagents (max 15 concurrent)</li>
                    <li>Extract patterns with Schema v2.3 routing</li>
                    <li>Verify quotes with ±5 line tolerance (Gap G15)</li>
                </ul>
            </div>
            <div class="overview-section">
                <div class="overview-section-title">📊 Phase 3: Synthesize (Integration)</div>
                <p><strong>Purpose:</strong> Merge findings into comprehensive reports using 7-Level Architecture</p>
                <ul class="overview-list">
                    <li>Route chunks to L4/L7 based on field assessment</li>
                    <li>Run deterministic scripts (L1-L5)</li>
                    <li>AI aggregation with token budget management</li>
                    <li>Generate final synthesis report with citations</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- LEGEND PANEL -->
    <div class="legend-panel">
        <div class="legend-title">Content Type Legend</div>
        <div class="legend-grid">
            <div class="legend-item">
                <div class="legend-icon">💻</div>
                <div class="legend-text">
                    <span class="legend-label">Code Blocks</span>
                    <span class="legend-desc">Implementation examples and configuration snippets</span>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">📊</div>
                <div class="legend-text">
                    <span class="legend-label">Tables</span>
                    <span class="legend-desc">Structured data, comparisons, and reference matrices</span>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">✓</div>
                <div class="legend-text">
                    <span class="legend-label">Validations</span>
                    <span class="legend-desc">Quality checks, assertions, and verification rules</span>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">⚙️</div>
                <div class="legend-text">
                    <span class="legend-label">Scripts</span>
                    <span class="legend-desc">Executable Python/Bash commands with parameters</span>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">🔧</div>
                <div class="legend-text">
                    <span class="legend-label">Gap Fixes</span>
                    <span class="legend-desc">References to known issues and their solutions (G5, G13, G15, etc.)</span>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">🏗️</div>
                <div class="legend-text">
                    <span class="legend-label">Architecture Patterns</span>
                    <span class="legend-desc">Design patterns, algorithms, and system architectures (7-Level, Bin-Packing, etc.)</span>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">📁</div>
                <div class="legend-text">
                    <span class="legend-label">Input Files</span>
                    <span class="legend-desc">Files read by this step (templates, configs, data sources)</span>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">📤</div>
                <div class="legend-text">
                    <span class="legend-label">Output Files</span>
                    <span class="legend-desc">Files created by this step (reports, analyses, indexes)</span>
                </div>
            </div>
            <div class="legend-item">
                <div class="legend-icon">🤖</div>
                <div class="legend-text">
                    <span class="legend-label">Subagents</span>
                    <span class="legend-desc">Parallel AI agents spawned for concurrent processing</span>
                </div>
            </div>
        </div>
    </div>

    <div class="container">
        <nav class="sidebar">
"""

    # Generate sidebar navigation
    for skill in skills:
        html += f"""            <div class="nav-section">
                <h3>{skill.name}</h3>
"""
        for step in skill.all_steps:
            gate_class = " nav-gate" if step.is_gate else ""
            html += f"""                <div class="nav-item{gate_class}" onclick="scrollToStep({step.number})">
                    <span class="nav-step-num">{step.number}</span>
                    <span>{step.title}</span>
                </div>
"""
        html += """            </div>
"""

    html += """        </nav>

        <main class="main-content">
"""

    # Generate main content
    for skill in skills:
        html += f"""            <div class="skill-section" id="skill-{skill.name.lower().replace(' ', '-')}">
                <div class="skill-header">
                    <h2>{skill.name}</h2>
                    <p>{skill.description}</p>
                </div>
"""

        for phase in skill.phases:
            html += f"""                <div class="phase-section">
                    <div class="phase-header">
                        <h3>Phase {phase.letter}: {phase.title}</h3>
                    </div>
"""

            for step in phase.steps:
                gate_class = " gate" if step.is_gate else ""
                html += f"""                    <div class="step-card{gate_class}" id="step-{step.number}">
                        <div class="step-header">
                            <div class="step-number">{step.number}</div>
                            <div class="step-title">
                                <h4>{step.title}</h4>
                                <div class="step-meta">Phase {step.phase} · {skill.name}</div>
                            </div>
                        </div>

                        <div class="step-description">
                            {step.description}
                        </div>

                        <!-- Content Type Badges -->
                        <div style="margin-top: 1rem;">
"""
                # Add content badges
                if step.code_blocks:
                    html += f"""                            <span class="content-type-badge badge-code">💻 {len(step.code_blocks)} Code</span>
"""
                if step.tables:
                    html += f"""                            <span class="content-type-badge badge-table">📊 {len(step.tables)} Tables</span>
"""
                if step.validation_checks:
                    html += f"""                            <span class="content-type-badge badge-validation">✓ {len(step.validation_checks)} Validations</span>
"""
                if step.scripts:
                    html += f"""                            <span class="content-type-badge badge-script">⚙️ {len(step.scripts)} Scripts</span>
"""
                if step.gap_fixes:
                    html += f"""                            <span class="content-type-badge badge-gap">🔧 {len(step.gap_fixes)} Gaps</span>
"""
                if step.architecture_patterns:
                    html += f"""                            <span class="content-type-badge badge-pattern">🏗️ {len(step.architecture_patterns)} Patterns</span>
"""

                html += """                        </div>
"""

                # Substeps
                if step.substeps:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>📋 Sub-Steps</span>
                                    <span class="content-badge">""" + str(len(step.substeps)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
                                <ul class="substeps-list">
"""
                    for substep in step.substeps:
                        html += f"""                                    <li class="substep-item">{substep}</li>
"""
                    html += """                                </ul>
                            </div>
                        </div>
"""

                # Gate Criteria
                if step.gate_criteria:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>🎯 Gate Criteria</span>
                                    <span class="content-badge">""" + str(len(step.gate_criteria)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
                                <ul class="criteria-list">
"""
                    for criterion in step.gate_criteria:
                        html += f"""                                    <li class="criteria-item">{criterion}</li>
"""
                    html += """                                </ul>
                            </div>
                        </div>
"""

                # Code Blocks
                if step.code_blocks:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>💻 Code Blocks</span>
                                    <span class="content-badge">""" + str(len(step.code_blocks)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
"""
                    for code in step.code_blocks:
                        context_html = f"<div class='code-context'>{code.context}</div>" if code.context else ""
                        html += f"""                                <div class="code-block">
                                    <div class="code-header">
                                        <span class="code-language">{code.language}</span>
                                        {context_html}
                                    </div>
                                    <div class="code-content">
                                        <pre>{code.content}</pre>
                                    </div>
                                </div>
"""
                    html += """                            </div>
                        </div>
"""

                # Tables
                if step.tables:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>📊 Tables</span>
                                    <span class="content-badge">""" + str(len(step.tables)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
"""
                    for table in step.tables:
                        context_html = f"<div class='table-context'>{table.context}</div>" if table.context else ""
                        html += f"""                                <div class="table-wrapper">
                                    {context_html}
                                    <table>
                                        <thead>
                                            <tr>
"""
                        for header in table.headers:
                            html += f"""                                                <th>{header}</th>
"""
                        html += """                                            </tr>
                                        </thead>
                                        <tbody>
"""
                        for row in table.rows:
                            html += """                                            <tr>
"""
                            for cell in row:
                                html += f"""                                                <td>{cell}</td>
"""
                            html += """                                            </tr>
"""
                        html += """                                        </tbody>
                                    </table>
                                </div>
"""
                    html += """                            </div>
                        </div>
"""

                # Templates
                if step.templates:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>📝 Templates & Examples</span>
                                    <span class="content-badge">""" + str(len(step.templates)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
"""
                    for template in step.templates:
                        html += f"""                                <div class="template-item">
                                    <div class="template-header">
                                        <span class="template-type">{template.type}</span>
                                        <span class="template-name">{template.name}</span>
                                    </div>
                                    <div class="template-content">{template.content}</div>
                                </div>
"""
                    html += """                            </div>
                        </div>
"""

                # Validation Checks
                if step.validation_checks:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>✅ Validation Checks</span>
                                    <span class="content-badge">""" + str(len(step.validation_checks)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
                                <ul class="validation-list">
"""
                    for check in step.validation_checks:
                        critical_class = " critical" if check.critical else ""
                        icon = "!" if check.critical else "✓"
                        html += f"""                                    <li class="validation-item{critical_class}">
                                        <div class="validation-icon">{icon}</div>
                                        <div>
                                            <span class="validation-type">{check.check_type}</span>
                                            {check.content}
                                        </div>
                                    </li>
"""
                    html += """                                </ul>
                            </div>
                        </div>
"""

                # Error Handlers
                if step.error_handlers:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>🔧 Error Handlers</span>
                                    <span class="content-badge">""" + str(len(step.error_handlers)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
"""
                    for handler in step.error_handlers:
                        html += f"""                                <div class="error-handler">
                                    <div class="error-type">{handler.error_type}</div>
                                    <div class="error-solution">{handler.solution}</div>
                                </div>
"""
                    html += """                            </div>
                        </div>
"""

                # Files (Inputs/Outputs)
                if step.inputs or step.outputs:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>📁 Files</span>
                                    <span class="content-badge">""" + str(len(step.inputs) + len(step.outputs)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
"""
                    if step.inputs:
                        html += """                                <h5 style="color: var(--accent-blue); margin-bottom: 0.5rem;">Inputs</h5>
                                <div class="file-list">
"""
                        for file in step.inputs:
                            html += f"""                                    <div class="file-ref input" title="{file.description}">{file.path}</div>
"""
                        html += """                                </div>
"""
                    if step.outputs:
                        html += """                                <h5 style="color: var(--accent-green); margin-bottom: 0.5rem; margin-top: 1rem;">Outputs</h5>
                                <div class="file-list">
"""
                        for file in step.outputs:
                            html += f"""                                    <div class="file-ref output" title="{file.description}">{file.path}</div>
"""
                        html += """                                </div>
"""
                    html += """                            </div>
                        </div>
"""

                # Scripts
                if step.scripts:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>⚙️ Scripts</span>
                                    <span class="content-badge">""" + str(len(step.scripts)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
"""
                    for script in step.scripts:
                        purpose_html = f"<div class='script-purpose'>{script.purpose}</div>" if script.purpose else ""
                        params_html = ""
                        if script.parameters:
                            params_html = "<div class='script-params'>Parameters: " + ", ".join(f"<code>{p}</code>" for p in script.parameters) + "</div>"
                        html += f"""                                <div class="script-item">
                                    <div class="script-header">
                                        <span class="script-name">{script.name}</span>
                                    </div>
                                    {purpose_html}
                                    <div class="script-command"><code>{script.command}</code></div>
                                    {params_html}
                                </div>
"""
                    html += """                            </div>
                        </div>
"""

                # Gap Fixes
                if step.gap_fixes:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>🔧 Gap Fixes</span>
                                    <span class="content-badge">""" + str(len(step.gap_fixes)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
"""
                    for gap in step.gap_fixes:
                        html += f"""                                <div class="gap-fix-item">
                                    <div class="gap-fix-header">
                                        <span class="gap-id">{gap.gap_id}</span>
                                        <span class="gap-description">{gap.description}</span>
                                    </div>
                                    <div class="gap-context">{gap.step_context}</div>
                                </div>
"""
                    html += """                            </div>
                        </div>
"""

                # Architecture Patterns
                if step.architecture_patterns:
                    html += """                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>🏗️ Architecture Patterns</span>
                                    <span class="content-badge">""" + str(len(step.architecture_patterns)) + """</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
"""
                    for pattern in step.architecture_patterns:
                        code_html = ""
                        if pattern.code_example:
                            code_html = f"""<div class="pattern-code">
                                        <pre><code>{pattern.code_example}</code></pre>
                                    </div>"""
                        html += f"""                                <div class="pattern-item">
                                    <div class="pattern-header">
                                        <span class="pattern-name">{pattern.name}</span>
                                    </div>
                                    <div class="pattern-description">{pattern.description}</div>
                                    {code_html}
                                </div>
"""
                    html += """                            </div>
                        </div>
"""

                # Subagent Config
                if step.subagent:
                    html += f"""                        <div class="content-section">
                            <div class="content-section-header" onclick="toggleSection(this)">
                                <div class="content-section-title">
                                    <span>🤖 Subagent Configuration</span>
                                </div>
                                <span class="expand-icon">▶</span>
                            </div>
                            <div class="content-section-body">
                                <div class="subagent-config">
                                    <p style="color: var(--text-secondary); margin-bottom: 0.75rem;">{step.subagent.purpose}</p>
                                    <div class="config-grid">
                                        <div class="config-item">
                                            <span class="config-label">Model</span>
                                            <span class="config-value">{step.subagent.model}</span>
                                        </div>
                                        <div class="config-item">
                                            <span class="config-label">Timeout</span>
                                            <span class="config-value">{step.subagent.timeout} min</span>
                                        </div>
                                        <div class="config-item">
                                            <span class="config-label">Budget</span>
                                            <span class="config-value">{step.subagent.budget}</span>
                                        </div>
                                        <div class="config-item">
                                            <span class="config-label">Concurrency</span>
                                            <span class="config-value">{step.subagent.concurrency}</span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
"""

                html += """                    </div>
"""

            html += """                </div>
"""

        html += """            </div>
"""

    html += """        </main>
    </div>

    <script>
        function scrollToStep(stepNum) {
            const element = document.getElementById(`step-${stepNum}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Update active nav item
                document.querySelectorAll('.nav-item').forEach(item => {
                    item.classList.remove('active');
                });
                event.target.closest('.nav-item').classList.add('active');
            }
        }

        function toggleSection(header) {
            const body = header.nextElementSibling;
            header.classList.toggle('expanded');
            body.classList.toggle('expanded');
        }

        // Highlight active section on scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const stepNum = entry.target.id.replace('step-', '');
                    document.querySelectorAll('.nav-item').forEach(item => {
                        item.classList.remove('active');
                    });
                    const activeNav = document.querySelector(`[onclick="scrollToStep(${stepNum})"]`);
                    if (activeNav) {
                        activeNav.classList.add('active');
                    }
                }
            });
        }, { threshold: 0.5 });

        document.querySelectorAll('.step-card').forEach(card => {
            observer.observe(card);
        });
    </script>
</body>
</html>
"""

    output_path.write_text(html, encoding='utf-8')
    print(f"[+] Generated: {output_path}")
    print(f"  - {total_steps} steps across {total_phases} phases")
    print(f"  - {total_code_blocks} code blocks")
    print(f"  - {total_tables} tables")
    print(f"  - {total_validations} validation checks")
    print(f"  - {total_scripts} scripts")
    print(f"  - {total_gaps} gap fixes")
    print(f"  - {total_patterns} architecture patterns")
    print(f"  - {total_files} unique files")

# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point."""
    base_path = Path(__file__).parent / "orchestrators"

    # Parse all three orchestrators
    skill_paths = [
        base_path / "create-research-project" / "SKILL.md",
        base_path / "analyze-research-project" / "SKILL.md",
        base_path / "synthesize-research-project" / "SKILL.md",
    ]

    skills = []
    for skill_path in skill_paths:
        if skill_path.exists():
            print(f"Parsing {skill_path.name}...")
            skill = parse_skill(skill_path)
            skills.append(skill)
            print(f"  [+] {len(skill.all_steps)} steps, {len(skill.phases)} phases")
        else:
            print(f"  [-] Not found: {skill_path}")

    # Generate HTML
    output_path = Path(__file__).parent / "research_pipeline_v8.html"
    generate_html(skills, output_path)

if __name__ == "__main__":
    main()

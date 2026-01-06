#!/usr/bin/env python3
"""
Research Pipeline Visualizer v6 - 10x Better Edition
Generates an interactive HTML visualization with:
- Rich step content with full descriptions
- Visual flow connections between steps
- Summary stats cards with key metrics
- Enhanced script/command display
- Sub-steps accordion
- Handoff visualization between orchestrators
- File flow graph
- Level indicators for 7-level architecture
- Progress tracking
"""

import re
import json
import sys
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class FileRef:
    path: str
    type: str
    format: str = ""
    description: str = ""

@dataclass
class SubagentConfig:
    type: str = "general-purpose"
    concurrency: int = 1
    timeout: str = "5 min"
    retry: int = 1
    input_contract: List[str] = field(default_factory=list)
    output_contract: List[str] = field(default_factory=list)

@dataclass
class GateOption:
    key: str
    label: str
    target: str = ""

@dataclass
class Gate:
    name: str
    options: List[GateOption] = field(default_factory=list)

@dataclass
class SubStep:
    number: str
    name: str
    description: str = ""

@dataclass
class Step:
    id: str
    number: str
    name: str
    phase: str
    phase_name: str
    description: str = ""
    full_content: str = ""
    sub_steps: List[SubStep] = field(default_factory=list)
    inputs: List[FileRef] = field(default_factory=list)
    outputs: List[FileRef] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    script_names: List[str] = field(default_factory=list)
    skills_used: List[str] = field(default_factory=list)
    subagent: Optional[SubagentConfig] = None
    gate: Optional[Gate] = None
    handoff_to: Optional[str] = None
    is_script: bool = False
    level: Optional[int] = None
    validation_checks: List[str] = field(default_factory=list)
    key_outputs: List[str] = field(default_factory=list)

@dataclass
class Phase:
    letter: str
    name: str
    steps: List[Step] = field(default_factory=list)

@dataclass
class Orchestrator:
    name: str
    path: str
    description: str
    phases: List[Phase] = field(default_factory=list)
    handoff_from: Optional[str] = None
    handoff_to: Optional[str] = None
    total_steps: int = 0
    total_gates: int = 0
    key_outputs: List[str] = field(default_factory=list)
    version: str = ""

# ============================================================================
# ENHANCED PARSING
# ============================================================================

def get_file_format(path: str) -> str:
    if '.md' in path: return 'md'
    if '.yaml' in path or '.yml' in path: return 'yaml'
    if '.json' in path: return 'json'
    if '.py' in path: return 'py'
    if '.pdf' in path: return 'pdf'
    return 'file'

def extract_description(content: str, max_chars: int = 500) -> str:
    """Extract meaningful description from step content."""
    lines = []
    in_code_block = False

    for line in content.split('\n'):
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Skip empty lines
        if not stripped:
            continue

        # Skip headers, tables
        if stripped.startswith(('#', '|', '>')):
            continue

        # Skip standalone backtick lines
        if stripped.startswith('`') and stripped.endswith('`') and len(stripped) < 50:
            continue

        # Handle bold text like **Use skill:** - extract the text
        if stripped.startswith('**') and '**' in stripped[2:]:
            # Extract text between ** **
            match = re.match(r'\*\*(.+?)\*\*[:\s]*(.*)', stripped)
            if match:
                text = match.group(1)
                rest = match.group(2).strip()
                if rest:
                    lines.append(f"{text}: {rest}")
                else:
                    lines.append(text)
                continue

        # Skip pure list markers but keep list content
        if stripped.startswith(('-', '*')) and len(stripped) > 2:
            list_content = stripped[1:].strip()
            if list_content.startswith('-'):
                list_content = list_content[1:].strip()
            if len(list_content) > 10:
                lines.append(list_content)
            continue

        # Skip short lines that look like labels
        if len(stripped) < 15 and stripped.endswith(':'):
            continue

        lines.append(stripped)

        if len(' '.join(lines)) > max_chars:
            break

    desc = ' '.join(lines)[:max_chars]
    if len(desc) == max_chars:
        desc = desc.rsplit(' ', 1)[0] + '...'
    return desc

def parse_subagent_config(content: str) -> Optional[SubagentConfig]:
    has_task_spawn = bool(re.search(r'Task\s*\(\s*\n?\s*subagent_type', content))
    has_spawn_instruction = bool(re.search(r'[Ss]pawn\s+(?:subagent|batch|extraction|final)', content))

    if not (has_task_spawn or has_spawn_instruction):
        return None

    config = SubagentConfig()

    type_match = re.search(r'subagent_type\s*=\s*["\']([^"\']+)["\']', content)
    if type_match:
        config.type = type_match.group(1)

    conc_match = re.search(r'(?:max|concurrency|parallel|concurrent)\s*[=:]\s*(\d+)', content, re.IGNORECASE)
    if conc_match:
        config.concurrency = int(conc_match.group(1))

    timeout_match = re.search(r'timeout\s*[=:]\s*["\']?(\d+\s*(?:min|sec|hour)[s]?)["\']?', content, re.IGNORECASE)
    if timeout_match:
        config.timeout = timeout_match.group(1)

    retry_match = re.search(r'retry\s*[=:]\s*(\d+)', content, re.IGNORECASE)
    if retry_match:
        config.retry = int(retry_match.group(1))

    # Parse input contract
    contract_match = re.search(r'INPUT CONTRACT.*?\n((?:[-•*#]\s*.+\n?)+)', content, re.IGNORECASE | re.DOTALL)
    if contract_match:
        contract_lines = re.findall(r'[-•*]\s*(.+)', contract_match.group(1))
        config.input_contract = [l.strip()[:100] for l in contract_lines if l.strip()][:5]

    return config

def parse_gate(step_name: str, content: str) -> Optional[Gate]:
    if not re.search(r'(?:gate|decision|approval|user\s+confirms?|Ready\s+to|Continue)', step_name + content, re.IGNORECASE):
        return None

    gate = Gate(name=step_name)

    option_patterns = [
        (r'\[Y\]\s*([^\n\[]+)', 'Y'),
        (r'\[N\]\s*([^\n\[]+)', 'N'),
        (r'\[S\]\s*([^\n\[]+)', 'S'),
        (r'\[R\]\s*([^\n\[]+)', 'R'),
        (r'\[A\]\s*([^\n\[]+)', 'A'),
    ]

    for pattern, key in option_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            gate.options.append(GateOption(key=key, label=match.group(1).strip()[:80]))

    return gate if gate.options else None

def extract_files(content: str, file_type: str) -> List[FileRef]:
    """Extract file references - inputs vs outputs based on context."""
    files = []
    seen = set()

    if file_type == "input":
        # Input-specific patterns - very strict to avoid false positives
        patterns = [
            # "from `file`" pattern
            r'(?:from|using|reads?)\s+`([^`]+(?:\.md|\.yaml|\.json))`',
            # "Use template from:" pattern
            r'Use template from[:\s]+`([^`]+)`',
            # "Reads:" explicit marker
            r'Reads?[:\s]+`([^`]+(?:\.md|\.yaml|\.json))`',
            # Files You MUST Read
            r'MUST\s+[Rr]ead[^`]*`([^`]+(?:\.md|\.yaml|\.json))`',
        ]
    else:
        # Output-specific patterns - strict to real outputs
        patterns = [
            # "**Output:**" pattern - THE primary pattern
            r'\*\*Output\*\*[:\s]+`([^`]+)`',
            # "Output:" without bold
            r'^Output[:\s]+`([^`]+)`',
            # "Creates:" pattern
            r'Creates?[:\s]+`([^`]+(?:\.md|\.yaml|\.json))`',
            # "Write to" pattern
            r'[Ww]rite\s+(?:to\s+)?`([^`]+(?:\.md|\.yaml|\.json))`',
            # Arrow output pattern on its own line
            r'^\s*[→>]\s*`([^`]+(?:\.md|\.yaml|\.json))`',
        ]

    for pattern in patterns:
        for match in re.finditer(pattern, content, re.MULTILINE | re.IGNORECASE):
            path = match.group(1) if match.lastindex else match.group(0)
            path = path.strip().strip('`').strip()

            # Clean up path
            if not path:
                continue
            if path.startswith(('{', '$', '#')):
                continue
            # Must have a file extension
            if not any(path.endswith(ext) for ext in ['.md', '.yaml', '.json', '.py', '.pdf']):
                continue
            # Skip template references
            if 'template' in path.lower() and file_type == "output":
                continue
            if path in seen:
                continue

            seen.add(path)
            files.append(FileRef(
                path=path,
                type=file_type,
                format=get_file_format(path)
            ))

    return files[:8]  # Limit

def extract_scripts(content: str) -> tuple[List[str], List[str]]:
    """Extract script commands and names."""
    scripts = []
    script_names = []

    # Find python commands
    for match in re.finditer(r'python\s+([^\s]+\.py)(?:\s+[^\n]*)?', content):
        full_cmd = match.group(0).strip()[:150]
        script_name = match.group(1).split('/')[-1]
        if full_cmd not in scripts:
            scripts.append(full_cmd)
            script_names.append(script_name)

    # Find bash code blocks
    for match in re.finditer(r'```(?:bash|sh)\n([^`]+)```', content, re.DOTALL):
        block = match.group(1).strip()
        lines = [l.strip() for l in block.split('\n') if l.strip() and not l.strip().startswith('#')]
        for line in lines[:3]:
            if 'python' in line and line not in scripts:
                scripts.append(line[:150])
                py_match = re.search(r'(\w+\.py)', line)
                if py_match:
                    script_names.append(py_match.group(1))

    return scripts[:5], script_names[:5]

def extract_substeps(content: str) -> List[SubStep]:
    """Extract numbered sub-steps like 2.1, 2.2, etc."""
    substeps = []

    # Match patterns like ### 2.1: Name or ### 12.1 Name
    pattern = r'^###\s+(\d+\.\d+)[.:\s]+(.+?)$'
    for match in re.finditer(pattern, content, re.MULTILINE):
        num = match.group(1)
        name = match.group(2).strip()

        # Get description (next few lines)
        start = match.end()
        end = start + 500
        desc_content = content[start:end]
        desc = extract_description(desc_content, 150)

        substeps.append(SubStep(number=num, name=name, description=desc))

    return substeps[:10]

def extract_validation_checks(content: str) -> List[str]:
    """Extract validation assertions."""
    checks = []

    # Look for assert statements
    for match in re.finditer(r'assert\s+([^\n,]+)', content):
        check = match.group(1).strip()[:100]
        if check and check not in checks:
            checks.append(check)

    # Look for validation bullets
    for match in re.finditer(r'[-•*]\s*(?:✓|✗|⚠️?)?\s*([A-Z][^\n]+(?:exists?|valid|check|verify))', content, re.IGNORECASE):
        check = match.group(1).strip()[:100]
        if check and check not in checks:
            checks.append(check)

    return checks[:8]

def extract_key_outputs(content: str) -> List[str]:
    """Extract key output file descriptions."""
    outputs = []

    # Look for output table rows
    for match in re.finditer(r'\|\s*`([^`]+)`\s*\|\s*([^|]+)\s*\|', content):
        path = match.group(1).strip()
        desc = match.group(2).strip()[:60]
        if path.endswith(('.md', '.yaml', '.json')):
            outputs.append(f"{path}: {desc}")

    return outputs[:5]

def parse_skill_md(content: str, file_path: Path) -> Orchestrator:
    """Parse a SKILL.md file into an Orchestrator structure."""
    name = file_path.parent.name
    path = str(file_path)

    orch = Orchestrator(name=name, path=path, description="")

    # Extract frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm_content = fm_match.group(1)
        name_match = re.search(r'^name:\s*(.+)$', fm_content, re.MULTILINE)
        desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', fm_content, re.MULTILINE)
        if name_match:
            orch.name = name_match.group(1).strip()
        if desc_match:
            orch.description = desc_match.group(1).strip()[:300]

    # Extract version
    version_match = re.search(r'\*\*Version\*\*:\s*([^\n]+)', content)
    if version_match:
        orch.version = version_match.group(1).strip()

    # Extract handoff info
    handoff_from = re.search(r'[Rr]eceives?\s+from[:\s]+[`"]?([a-z-]+)', content)
    handoff_to = re.search(r'[Hh]ands?\s+off\s+to[:\s]+[`"]?([a-z-]+)', content)
    if handoff_from:
        orch.handoff_from = handoff_from.group(1).strip()
    if handoff_to:
        orch.handoff_to = handoff_to.group(1).strip()

    # Extract key outputs from "Files Created" section
    files_section = re.search(r'## Files Created.*?\n((?:\|[^\n]+\n)+)', content, re.DOTALL)
    if files_section:
        orch.key_outputs = extract_key_outputs(files_section.group(1))

    phases = {}

    # Phases use # PHASE A: format
    phase_pattern = r'#\s*PHASE\s+([A-Z]):\s*(.+?)(?=\n)'
    phase_positions = [(m.start(), m.group(1), m.group(2).strip())
                       for m in re.finditer(phase_pattern, content)]

    for _, letter, pname in phase_positions:
        phases[letter] = Phase(letter=letter, name=pname)

    # Steps use ## Step N: format
    step_pattern = r'^##\s*[Ss]tep\s+(\d+(?:\.\d+)?)\s*:?\s*(.+?)$'
    step_matches = list(re.finditer(step_pattern, content, re.MULTILINE))

    def get_phase_at_pos(pos: int) -> tuple:
        current = ("A", "Setup")
        for phase_pos, letter, pname in phase_positions:
            if phase_pos < pos:
                current = (letter, pname)
            else:
                break
        return current

    for i, match in enumerate(step_matches):
        step_num = match.group(1)
        step_name = match.group(2).strip()

        # Get step content
        start = match.end()
        end = step_matches[i + 1].start() if i + 1 < len(step_matches) else len(content)
        step_content = content[start:end]

        # Get phase
        phase_letter, phase_name = get_phase_at_pos(match.start())

        if phase_letter not in phases:
            phases[phase_letter] = Phase(letter=phase_letter, name=phase_name)

        phase_name = phases[phase_letter].name

        # Extract rich description
        desc = extract_description(step_content, 400)

        # Extract sub-steps
        sub_steps = extract_substeps(step_content)

        # Extract files with deduplication between inputs and outputs
        inputs = extract_files(step_content, "input")
        outputs = extract_files(step_content, "output")

        # Remove any outputs that appear in inputs (prefer output classification)
        input_paths = {f.path for f in inputs}
        output_paths = {f.path for f in outputs}

        # If same file in both, keep only in outputs
        inputs = [f for f in inputs if f.path not in output_paths]

        # Extract scripts
        scripts, script_names = extract_scripts(step_content)

        # Check if script-based
        is_script = bool(re.search(r'(?:Script|SCRIPT|python\s+\w+\.py|deterministic|\.py)', step_content))

        # Extract level
        level = None
        level_match = re.search(r'[Ll]evel\s+(\d+)', step_name) or re.search(r'[Ll]evel\s+(\d+)', step_content[:300])
        if level_match:
            level = int(level_match.group(1))

        # Parse subagent and gate
        subagent = parse_subagent_config(step_content)
        gate = parse_gate(step_name, step_content)
        if gate:
            orch.total_gates += 1

        # Extract validation checks
        validation_checks = extract_validation_checks(step_content)

        # Extract key outputs
        key_outputs = extract_key_outputs(step_content)

        # Handoff
        handoff = None
        handoff_match = re.search(r'(?:handoff|hand\s+off|proceed)\s+to[:\s]+[`"]?([a-z-]+)', step_content, re.IGNORECASE)
        if handoff_match:
            handoff = handoff_match.group(1).strip()

        step = Step(
            id=f"step_{step_num.replace('.', '_')}",
            number=step_num,
            name=step_name,
            phase=phase_letter,
            phase_name=phase_name,
            description=desc,
            full_content=step_content[:2000],
            sub_steps=sub_steps,
            inputs=inputs,
            outputs=outputs,
            scripts=scripts,
            script_names=script_names,
            subagent=subagent,
            gate=gate,
            handoff_to=handoff,
            is_script=is_script,
            level=level,
            validation_checks=validation_checks,
            key_outputs=key_outputs
        )

        phases[phase_letter].steps.append(step)
        orch.total_steps += 1

    orch.phases = [phases[k] for k in sorted(phases.keys())]

    return orch

def build_file_graph(orchestrators: List[Orchestrator]) -> Dict:
    nodes = {}
    edges = []
    for orch in orchestrators:
        for phase in orch.phases:
            for step in phase.steps:
                step_id = f"{orch.name}:{step.number}"
                for inp in step.inputs:
                    if inp.path not in nodes:
                        nodes[inp.path] = {"type": "file", "format": inp.format, "producers": [], "consumers": []}
                    nodes[inp.path]["consumers"].append(step_id)
                    edges.append({"source": inp.path, "target": step_id, "type": "input"})
                for out in step.outputs:
                    if out.path not in nodes:
                        nodes[out.path] = {"type": "file", "format": out.format, "producers": [], "consumers": []}
                    nodes[out.path]["producers"].append(step_id)
                    edges.append({"source": step_id, "target": out.path, "type": "output"})
    return {"nodes": nodes, "edges": edges}

# ============================================================================
# HTML GENERATION - v6 10X BETTER EDITION
# ============================================================================

def serialize(obj):
    if hasattr(obj, '__dataclass_fields__'):
        result = {}
        for field_name in obj.__dataclass_fields__:
            value = getattr(obj, field_name)
            result[field_name] = serialize(value)
        return result
    elif isinstance(obj, list):
        return [serialize(item) for item in obj]
    elif isinstance(obj, dict):
        return {k: serialize(v) for k, v in obj.items()}
    else:
        return obj

def generate_html(orchestrators: List[Orchestrator], file_graph: Dict) -> str:
    """Generate enhanced HTML with rich content."""

    # Calculate stats
    total_steps = sum(o.total_steps for o in orchestrators)
    total_gates = sum(o.total_gates for o in orchestrators)
    total_phases = sum(len(o.phases) for o in orchestrators)
    total_scripts = sum(
        len(step.scripts)
        for o in orchestrators
        for p in o.phases
        for step in p.steps
    )
    total_subagents = sum(
        1 for o in orchestrators
        for p in o.phases
        for step in p.steps
        if step.subagent
    )

    data = {
        "orchestrators": [serialize(o) for o in orchestrators],
        "file_graph": file_graph,
        "stats": {
            "total_steps": total_steps,
            "total_gates": total_gates,
            "total_phases": total_phases,
            "total_scripts": total_scripts,
            "total_subagents": total_subagents,
            "total_files": len(file_graph["nodes"]),
        },
        "pipeline": [
            {
                "name": o.name,
                "steps": o.total_steps,
                "gates": o.total_gates,
                "phases": len(o.phases),
                "handoff_to": o.handoff_to,
                "description": o.description,
                "version": o.version,
                "key_outputs": o.key_outputs[:3]
            }
            for o in orchestrators
        ]
    }

    data_json = json.dumps(data, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Pipeline - 10x Visualization</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #09090b;
            --bg-secondary: #0f0f12;
            --bg-tertiary: #18181b;
            --bg-elevated: #1f1f23;
            --bg-card: #141417;
            --bg-hover: #1c1c20;
            --border: #27272a;
            --border-subtle: #1f1f23;
            --border-bright: #3f3f46;
            --text-primary: #fafafa;
            --text-secondary: #a1a1aa;
            --text-muted: #71717a;
            --text-dim: #52525b;

            /* Vibrant accent colors */
            --accent-emerald: #10b981;
            --accent-blue: #3b82f6;
            --accent-violet: #8b5cf6;
            --accent-amber: #f59e0b;
            --accent-rose: #f43f5e;
            --accent-cyan: #06b6d4;
            --accent-lime: #84cc16;
            --accent-pink: #ec4899;

            /* Glow effects */
            --glow-emerald: rgba(16, 185, 129, 0.15);
            --glow-blue: rgba(59, 130, 246, 0.15);
            --glow-violet: rgba(139, 92, 246, 0.15);

            /* Phase colors */
            --phase-a: #22c55e;
            --phase-b: #3b82f6;
            --phase-c: #f59e0b;
            --phase-d: #a855f7;
            --phase-e: #ec4899;
            --phase-f: #14b8a6;
            --phase-g: #6366f1;
            --phase-h: #f97316;
            --phase-i: #8b5cf6;

            --sidebar-width: 340px;
            --header-height: 64px;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            overflow-x: hidden;
        }}

        /* ===== LAYOUT ===== */
        .app {{
            display: flex;
            min-height: 100vh;
        }}

        /* ===== SIDEBAR ===== */
        .sidebar {{
            width: var(--sidebar-width);
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            position: fixed;
            top: 0;
            left: 0;
            height: 100vh;
            overflow: hidden;
            z-index: 100;
            display: flex;
            flex-direction: column;
        }}

        .sidebar-header {{
            padding: 20px 24px;
            border-bottom: 1px solid var(--border);
            background: linear-gradient(180deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
            flex-shrink: 0;
        }}

        .logo {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }}

        .logo-icon {{
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-emerald) 0%, var(--accent-cyan) 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}

        .logo-text {{
            font-size: 18px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-emerald) 0%, var(--accent-cyan) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .logo-version {{
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 500;
        }}

        /* Mini stats in sidebar */
        .sidebar-stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 8px;
        }}

        .sidebar-stat {{
            background: var(--bg-primary);
            border-radius: 8px;
            padding: 10px 8px;
            text-align: center;
        }}

        .sidebar-stat-value {{
            font-size: 18px;
            font-weight: 700;
            color: var(--accent-cyan);
        }}

        .sidebar-stat-label {{
            font-size: 9px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .nav {{
            flex: 1;
            overflow-y: auto;
            padding: 12px 0;
        }}

        .nav::-webkit-scrollbar {{
            width: 6px;
        }}

        .nav::-webkit-scrollbar-track {{
            background: transparent;
        }}

        .nav::-webkit-scrollbar-thumb {{
            background: var(--border);
            border-radius: 3px;
        }}

        .nav-section {{
            margin-bottom: 4px;
        }}

        .nav-section-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 20px;
            cursor: pointer;
            transition: all 0.2s;
            border-left: 3px solid transparent;
            position: relative;
        }}

        .nav-section-header:hover {{
            background: var(--bg-hover);
        }}

        .nav-section-header.active {{
            background: var(--glow-blue);
            border-left-color: var(--accent-blue);
        }}

        .nav-section-header::after {{
            content: '›';
            position: absolute;
            right: 16px;
            font-size: 14px;
            color: var(--text-muted);
            transition: transform 0.2s;
        }}

        .nav-section.expanded .nav-section-header::after {{
            transform: rotate(90deg);
        }}

        .nav-section-icon {{
            width: 36px;
            height: 36px;
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            flex-shrink: 0;
        }}

        .nav-section-icon.create {{
            background: linear-gradient(135deg, var(--phase-a) 0%, #059669 100%);
            box-shadow: 0 4px 12px rgba(34, 197, 94, 0.3);
        }}
        .nav-section-icon.analyze {{
            background: linear-gradient(135deg, var(--phase-b) 0%, #2563eb 100%);
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.3);
        }}
        .nav-section-icon.synthesize {{
            background: linear-gradient(135deg, var(--phase-d) 0%, #7c3aed 100%);
            box-shadow: 0 4px 12px rgba(168, 85, 247, 0.3);
        }}

        .nav-section-info {{
            flex: 1;
            min-width: 0;
        }}

        .nav-section-title {{
            font-size: 13px;
            font-weight: 600;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .nav-section-meta {{
            font-size: 11px;
            color: var(--text-muted);
            display: flex;
            gap: 8px;
        }}

        .nav-items {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
            background: rgba(0,0,0,0.2);
        }}

        .nav-section.expanded .nav-items {{
            max-height: 3000px;
        }}

        .nav-phase {{
            padding: 10px 20px 6px 52px;
            font-size: 10px;
            font-weight: 700;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 1px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .nav-phase::before {{
            content: '';
            width: 20px;
            height: 1px;
            background: var(--border);
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 20px 10px 52px;
            cursor: pointer;
            transition: all 0.15s;
            border-left: 3px solid transparent;
            font-size: 12px;
            color: var(--text-secondary);
        }}

        .nav-item:hover {{
            background: var(--bg-hover);
            color: var(--text-primary);
        }}

        .nav-item.active {{
            background: rgba(6, 182, 212, 0.1);
            border-left-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }}

        .nav-item-step {{
            width: 28px;
            height: 22px;
            background: var(--bg-elevated);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            flex-shrink: 0;
        }}

        .nav-item.active .nav-item-step {{
            background: var(--accent-cyan);
            color: var(--bg-primary);
        }}

        .nav-item-name {{
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .nav-item-badges {{
            display: flex;
            gap: 4px;
            flex-shrink: 0;
        }}

        .nav-badge {{
            width: 18px;
            height: 18px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
        }}

        .nav-badge.gate {{ background: var(--accent-amber); color: #000; }}
        .nav-badge.subagent {{ background: var(--accent-violet); color: #fff; }}
        .nav-badge.script {{ background: var(--accent-cyan); color: #000; }}
        .nav-badge.level {{ background: var(--accent-rose); color: #fff; font-size: 9px; font-weight: 700; }}

        /* ===== MAIN CONTENT ===== */
        .main {{
            flex: 1;
            margin-left: var(--sidebar-width);
            min-height: 100vh;
        }}

        /* ===== HERO ===== */
        .hero {{
            background: linear-gradient(180deg, var(--bg-tertiary) 0%, var(--bg-primary) 100%);
            padding: 48px 48px 40px;
            border-bottom: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }}

        .hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-violet), transparent);
        }}

        .hero-content {{
            position: relative;
            z-index: 1;
        }}

        .hero-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: rgba(6, 182, 212, 0.1);
            border: 1px solid rgba(6, 182, 212, 0.3);
            border-radius: 20px;
            padding: 6px 14px;
            font-size: 11px;
            font-weight: 600;
            color: var(--accent-cyan);
            margin-bottom: 16px;
        }}

        .hero-title {{
            font-size: 42px;
            font-weight: 800;
            margin-bottom: 12px;
            letter-spacing: -1px;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--text-secondary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .hero-subtitle {{
            font-size: 16px;
            color: var(--text-secondary);
            margin-bottom: 32px;
            max-width: 600px;
        }}

        /* Stats Cards */
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(6, 1fr);
            gap: 12px;
            margin-bottom: 40px;
        }}

        .stat-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px;
            text-align: center;
            transition: all 0.2s;
        }}

        .stat-card:hover {{
            border-color: var(--accent-cyan);
            transform: translateY(-2px);
        }}

        .stat-value {{
            font-size: 28px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .stat-label {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-top: 4px;
        }}

        /* Pipeline Diagram */
        .pipeline-diagram {{
            display: flex;
            align-items: stretch;
            justify-content: center;
            gap: 0;
            margin: 0 -24px;
        }}

        .pipeline-node {{
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 20px;
            padding: 28px 32px;
            min-width: 280px;
            text-align: left;
            position: relative;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .pipeline-node:hover {{
            transform: translateY(-6px);
        }}

        .pipeline-node.create {{
            border-color: var(--phase-a);
            box-shadow: 0 8px 32px rgba(34, 197, 94, 0.15);
        }}
        .pipeline-node.create:hover {{ box-shadow: 0 16px 48px rgba(34, 197, 94, 0.25); }}

        .pipeline-node.analyze {{
            border-color: var(--phase-b);
            box-shadow: 0 8px 32px rgba(59, 130, 246, 0.15);
        }}
        .pipeline-node.analyze:hover {{ box-shadow: 0 16px 48px rgba(59, 130, 246, 0.25); }}

        .pipeline-node.synthesize {{
            border-color: var(--phase-d);
            box-shadow: 0 8px 32px rgba(168, 85, 247, 0.15);
        }}
        .pipeline-node.synthesize:hover {{ box-shadow: 0 16px 48px rgba(168, 85, 247, 0.25); }}

        .pipeline-node-header {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 16px;
        }}

        .pipeline-node-icon {{
            width: 48px;
            height: 48px;
            border-radius: 14px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }}

        .pipeline-node.create .pipeline-node-icon {{ background: linear-gradient(135deg, var(--phase-a) 0%, #059669 100%); }}
        .pipeline-node.analyze .pipeline-node-icon {{ background: linear-gradient(135deg, var(--phase-b) 0%, #2563eb 100%); }}
        .pipeline-node.synthesize .pipeline-node-icon {{ background: linear-gradient(135deg, var(--phase-d) 0%, #7c3aed 100%); }}

        .pipeline-node-title {{
            font-size: 16px;
            font-weight: 700;
        }}

        .pipeline-node-phase {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .pipeline-node-desc {{
            font-size: 12px;
            color: var(--text-secondary);
            line-height: 1.5;
            margin-bottom: 16px;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .pipeline-node-stats {{
            display: flex;
            gap: 16px;
            padding-top: 16px;
            border-top: 1px solid var(--border-subtle);
        }}

        .pipeline-node-stat {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: var(--text-muted);
        }}

        .pipeline-node-stat strong {{
            color: var(--text-primary);
            font-weight: 600;
        }}

        .pipeline-arrow {{
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 0 8px;
            flex-shrink: 0;
        }}

        .pipeline-arrow-line {{
            width: 60px;
            height: 3px;
            background: linear-gradient(90deg, var(--border) 0%, var(--text-muted) 50%, var(--border) 100%);
            position: relative;
        }}

        .pipeline-arrow-line::after {{
            content: '→';
            position: absolute;
            right: -12px;
            top: 50%;
            transform: translateY(-50%);
            font-size: 18px;
            color: var(--text-muted);
        }}

        /* Key Outputs */
        .pipeline-outputs {{
            margin-top: 12px;
        }}

        .pipeline-output {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            color: var(--text-dim);
            padding: 4px 0;
        }}

        .pipeline-output-icon {{
            color: var(--accent-emerald);
        }}

        /* ===== SECTIONS ===== */
        .section {{
            padding: 48px;
            border-bottom: 1px solid var(--border);
            scroll-margin-top: 20px;
        }}

        .section-header {{
            display: flex;
            align-items: flex-start;
            gap: 20px;
            margin-bottom: 36px;
            padding-bottom: 24px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .section-icon {{
            width: 56px;
            height: 56px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            flex-shrink: 0;
        }}

        .section-icon.create {{
            background: linear-gradient(135deg, var(--phase-a) 0%, #059669 100%);
            box-shadow: 0 8px 24px rgba(34, 197, 94, 0.3);
        }}
        .section-icon.analyze {{
            background: linear-gradient(135deg, var(--phase-b) 0%, #2563eb 100%);
            box-shadow: 0 8px 24px rgba(59, 130, 246, 0.3);
        }}
        .section-icon.synthesize {{
            background: linear-gradient(135deg, var(--phase-d) 0%, #7c3aed 100%);
            box-shadow: 0 8px 24px rgba(168, 85, 247, 0.3);
        }}

        .section-info {{
            flex: 1;
        }}

        .section-info h2 {{
            font-size: 28px;
            font-weight: 700;
            margin-bottom: 8px;
            letter-spacing: -0.5px;
        }}

        .section-info p {{
            color: var(--text-secondary);
            font-size: 14px;
            max-width: 600px;
        }}

        .section-meta {{
            display: flex;
            gap: 16px;
            margin-top: 12px;
        }}

        .section-meta-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Phase Headers */
        .phase-header {{
            display: flex;
            align-items: center;
            gap: 16px;
            padding: 18px 24px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 14px;
            margin-bottom: 20px;
            margin-top: 40px;
        }}

        .phase-header:first-of-type {{
            margin-top: 0;
        }}

        .phase-letter {{
            width: 42px;
            height: 42px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 18px;
            color: var(--bg-primary);
        }}

        .phase-letter.A {{ background: var(--phase-a); }}
        .phase-letter.B {{ background: var(--phase-b); }}
        .phase-letter.C {{ background: var(--phase-c); }}
        .phase-letter.D {{ background: var(--phase-d); }}
        .phase-letter.E {{ background: var(--phase-e); }}
        .phase-letter.F {{ background: var(--phase-f); }}
        .phase-letter.G {{ background: var(--phase-g); }}
        .phase-letter.H {{ background: var(--phase-h); }}
        .phase-letter.I {{ background: var(--phase-i); }}

        .phase-info {{
            flex: 1;
        }}

        .phase-name {{
            font-size: 16px;
            font-weight: 700;
        }}

        .phase-meta {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* ===== STEP CARDS ===== */
        .step-card {{
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            margin-bottom: 16px;
            overflow: hidden;
            transition: all 0.2s;
            scroll-margin-top: 20px;
        }}

        .step-card:hover {{
            border-color: var(--accent-blue);
        }}

        .step-card.expanded {{
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        }}

        .step-card-header {{
            display: flex;
            align-items: flex-start;
            gap: 16px;
            padding: 20px 24px;
            cursor: pointer;
            transition: background 0.2s;
        }}

        .step-card-header:hover {{
            background: var(--bg-hover);
        }}

        .step-number {{
            min-width: 44px;
            height: 44px;
            background: var(--bg-elevated);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
            font-weight: 700;
            color: var(--accent-cyan);
            flex-shrink: 0;
            transition: all 0.2s;
        }}

        .step-card.expanded .step-number {{
            background: var(--accent-cyan);
            color: var(--bg-primary);
        }}

        .step-info {{
            flex: 1;
            min-width: 0;
        }}

        .step-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 6px;
        }}

        .step-description {{
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.6;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .step-card.expanded .step-description {{
            -webkit-line-clamp: unset;
        }}

        .step-meta {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
            margin-top: 10px;
        }}

        .step-meta-badge {{
            font-size: 10px;
            padding: 4px 10px;
            border-radius: 6px;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .step-meta-badge.level {{
            background: rgba(244, 63, 94, 0.15);
            color: var(--accent-rose);
            border: 1px solid rgba(244, 63, 94, 0.3);
        }}

        .step-meta-badge.script {{
            background: rgba(6, 182, 212, 0.15);
            color: var(--accent-cyan);
            border: 1px solid rgba(6, 182, 212, 0.3);
        }}

        .step-meta-badge.subagent {{
            background: rgba(139, 92, 246, 0.15);
            color: var(--accent-violet);
            border: 1px solid rgba(139, 92, 246, 0.3);
        }}

        .step-meta-badge.gate {{
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-amber);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }}

        .step-badges {{
            display: flex;
            gap: 8px;
            flex-shrink: 0;
            align-items: flex-start;
        }}

        .step-expand {{
            width: 28px;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-muted);
            transition: all 0.2s;
        }}

        .step-card.expanded .step-expand {{
            transform: rotate(180deg);
        }}

        /* Step Content */
        .step-content {{
            display: none;
            padding: 0 24px 24px;
            border-top: 1px solid var(--border-subtle);
        }}

        .step-card.expanded .step-content {{
            display: block;
        }}

        .content-section {{
            margin-top: 20px;
        }}

        .content-section-title {{
            font-size: 11px;
            font-weight: 700;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}

        .content-section-title::after {{
            content: '';
            flex: 1;
            height: 1px;
            background: var(--border-subtle);
        }}

        /* Sub-steps */
        .substeps {{
            display: grid;
            gap: 8px;
        }}

        .substep {{
            display: flex;
            gap: 12px;
            padding: 14px 16px;
            background: var(--bg-tertiary);
            border-radius: 10px;
            border: 1px solid var(--border-subtle);
        }}

        .substep-number {{
            width: 28px;
            height: 28px;
            background: var(--bg-elevated);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            flex-shrink: 0;
        }}

        .substep-info {{
            flex: 1;
        }}

        .substep-name {{
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .substep-desc {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Files Grid */
        .files-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 10px;
        }}

        .file-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 14px;
            background: var(--bg-tertiary);
            border: 1px solid var(--border-subtle);
            border-radius: 10px;
            transition: all 0.2s;
        }}

        .file-item:hover {{
            border-color: var(--accent-blue);
            background: var(--bg-hover);
        }}

        .file-icon {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            flex-shrink: 0;
        }}

        .file-icon.input {{
            background: rgba(59, 130, 246, 0.15);
            color: var(--accent-blue);
        }}

        .file-icon.output {{
            background: rgba(16, 185, 129, 0.15);
            color: var(--accent-emerald);
        }}

        .file-info {{
            flex: 1;
            min-width: 0;
        }}

        .file-path {{
            font-size: 12px;
            font-family: 'JetBrains Mono', monospace;
            color: var(--text-secondary);
            word-break: break-all;
        }}

        .file-format {{
            font-size: 10px;
            color: var(--text-dim);
            text-transform: uppercase;
            margin-top: 2px;
        }}

        /* Scripts */
        .scripts-list {{
            display: grid;
            gap: 10px;
        }}

        .script-item {{
            background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(6, 182, 212, 0.02) 100%);
            border: 1px solid rgba(6, 182, 212, 0.2);
            border-radius: 12px;
            overflow: hidden;
        }}

        .script-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 14px 16px;
            background: rgba(0,0,0,0.2);
        }}

        .script-icon {{
            width: 36px;
            height: 36px;
            background: var(--accent-cyan);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
        }}

        .script-name {{
            font-size: 14px;
            font-weight: 600;
            color: var(--accent-cyan);
        }}

        .script-command {{
            padding: 14px 16px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: var(--text-secondary);
            background: rgba(0,0,0,0.3);
            border-radius: 0 0 12px 12px;
            overflow-x: auto;
        }}

        .script-command::before {{
            content: '$ ';
            color: var(--accent-emerald);
        }}

        /* Subagent Config */
        .subagent-card {{
            background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(139, 92, 246, 0.02) 100%);
            border: 1px solid rgba(139, 92, 246, 0.25);
            border-radius: 14px;
            padding: 20px;
        }}

        .subagent-header {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 16px;
        }}

        .subagent-icon {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--accent-violet) 0%, #6d28d9 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 16px rgba(139, 92, 246, 0.3);
        }}

        .subagent-title {{
            font-size: 16px;
            font-weight: 700;
        }}

        .subagent-type {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .subagent-stats {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }}

        .subagent-stat {{
            background: var(--bg-primary);
            border-radius: 10px;
            padding: 14px;
            text-align: center;
        }}

        .subagent-stat-value {{
            font-size: 24px;
            font-weight: 700;
            color: var(--accent-violet);
        }}

        .subagent-stat-label {{
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .subagent-visual {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .subagent-slot {{
            width: 32px;
            height: 32px;
            background: var(--accent-violet);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            color: #fff;
            animation: pulse 2s ease-in-out infinite;
        }}

        .subagent-slot:nth-child(2n) {{ animation-delay: 0.5s; }}
        .subagent-slot:nth-child(3n) {{ animation-delay: 1s; }}

        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.6; }}
        }}

        /* Gate Card */
        .gate-card {{
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.02) 100%);
            border: 1px solid rgba(245, 158, 11, 0.25);
            border-radius: 14px;
            padding: 20px;
        }}

        .gate-header {{
            display: flex;
            align-items: center;
            gap: 14px;
            margin-bottom: 16px;
        }}

        .gate-icon {{
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--accent-amber) 0%, #d97706 100%);
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            box-shadow: 0 4px 16px rgba(245, 158, 11, 0.3);
        }}

        .gate-title {{
            font-size: 16px;
            font-weight: 700;
        }}

        .gate-subtitle {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        .gate-options {{
            display: grid;
            gap: 8px;
        }}

        .gate-option {{
            display: flex;
            align-items: center;
            gap: 14px;
            padding: 14px 16px;
            background: var(--bg-primary);
            border-radius: 10px;
            transition: all 0.2s;
            cursor: pointer;
        }}

        .gate-option:hover {{
            background: var(--bg-tertiary);
        }}

        .gate-key {{
            width: 36px;
            height: 36px;
            background: var(--accent-amber);
            color: #000;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            font-size: 16px;
        }}

        .gate-label {{
            flex: 1;
            font-size: 14px;
        }}

        /* Validation Checks */
        .validation-list {{
            display: grid;
            gap: 6px;
        }}

        .validation-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            background: var(--bg-tertiary);
            border-radius: 8px;
            font-size: 12px;
            color: var(--text-secondary);
        }}

        .validation-icon {{
            color: var(--accent-emerald);
            font-weight: bold;
        }}

        /* Footer */
        .footer {{
            padding: 40px 48px;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            text-align: center;
        }}

        .footer-content {{
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }}

        .footer-logo {{
            font-size: 16px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-violet) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}

        .footer-meta {{
            font-size: 12px;
            color: var(--text-muted);
        }}

        /* Scroll Progress */
        .scroll-progress {{
            position: fixed;
            top: 0;
            left: var(--sidebar-width);
            right: 0;
            height: 3px;
            background: var(--bg-tertiary);
            z-index: 1000;
        }}

        .scroll-progress-bar {{
            height: 100%;
            background: linear-gradient(90deg, var(--accent-cyan) 0%, var(--accent-violet) 100%);
            width: 0%;
            transition: width 0.1s;
        }}

        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .animate-in {{
            animation: fadeIn 0.4s ease forwards;
        }}

        /* Mobile responsive */
        @media (max-width: 1200px) {{
            .stats-grid {{
                grid-template-columns: repeat(3, 1fr);
            }}
        }}

        @media (max-width: 900px) {{
            .sidebar {{
                display: none;
            }}
            .main {{
                margin-left: 0;
            }}
            .scroll-progress {{
                left: 0;
            }}
            .pipeline-diagram {{
                flex-direction: column;
            }}
            .pipeline-arrow {{
                transform: rotate(90deg);
            }}
        }}
    </style>
</head>
<body>
    <div class="scroll-progress">
        <div class="scroll-progress-bar" id="progressBar"></div>
    </div>

    <div class="app">
        <nav class="sidebar" id="sidebar"></nav>
        <main class="main" id="main"></main>
    </div>

    <script>
    const DATA = {data_json};

    let expandedSections = new Set(['create-research-project']);
    let expandedSteps = new Set();

    function getClass(name) {{
        if (name.includes('create')) return 'create';
        if (name.includes('analyze')) return 'analyze';
        if (name.includes('synthesize')) return 'synthesize';
        return 'create';
    }}

    function getIcon(name) {{
        if (name.includes('create')) return '🚀';
        if (name.includes('analyze')) return '🔬';
        if (name.includes('synthesize')) return '✨';
        return '📦';
    }}

    function formatName(name) {{
        return name.replace(/-/g, ' ').replace(/\\b\\w/g, c => c.toUpperCase());
    }}

    function renderNav() {{
        const nav = document.getElementById('sidebar');
        let html = `
            <div class="sidebar-header">
                <div class="logo">
                    <div class="logo-icon">⚡</div>
                    <div>
                        <div class="logo-text">Research Pipeline</div>
                        <div class="logo-version">v6 · 10x Visualization</div>
                    </div>
                </div>
                <div class="sidebar-stats">
                    <div class="sidebar-stat">
                        <div class="sidebar-stat-value">${{DATA.stats.total_steps}}</div>
                        <div class="sidebar-stat-label">Steps</div>
                    </div>
                    <div class="sidebar-stat">
                        <div class="sidebar-stat-value">${{DATA.stats.total_phases}}</div>
                        <div class="sidebar-stat-label">Phases</div>
                    </div>
                    <div class="sidebar-stat">
                        <div class="sidebar-stat-value">${{DATA.stats.total_gates}}</div>
                        <div class="sidebar-stat-label">Gates</div>
                    </div>
                </div>
            </div>
            <div class="nav" id="nav">
        `;

        DATA.orchestrators.forEach(orch => {{
            const isExpanded = expandedSections.has(orch.name);
            const cls = getClass(orch.name);

            html += `
                <div class="nav-section ${{isExpanded ? 'expanded' : ''}}" data-orch="${{orch.name}}">
                    <div class="nav-section-header" onclick="toggleSection('${{orch.name}}')">
                        <div class="nav-section-icon ${{cls}}">${{getIcon(orch.name)}}</div>
                        <div class="nav-section-info">
                            <div class="nav-section-title">${{formatName(orch.name)}}</div>
                            <div class="nav-section-meta">
                                <span>${{orch.total_steps}} steps</span>
                                <span>${{orch.total_gates}} gates</span>
                            </div>
                        </div>
                    </div>
                    <div class="nav-items">
            `;

            orch.phases.forEach(phase => {{
                html += `<div class="nav-phase">Phase ${{phase.letter}} · ${{phase.name}}</div>`;
                phase.steps.forEach(step => {{
                    const badges = [];
                    if (step.level) badges.push(`<span class="nav-badge level">${{step.level}}</span>`);
                    if (step.gate) badges.push('<span class="nav-badge gate">⚡</span>');
                    if (step.subagent) badges.push('<span class="nav-badge subagent">🤖</span>');
                    if (step.is_script) badges.push('<span class="nav-badge script">⚙</span>');

                    html += `
                        <div class="nav-item" data-step="${{orch.name}}-${{step.id}}" onclick="scrollToStep('${{orch.name}}-${{step.id}}')">
                            <span class="nav-item-step">${{step.number}}</span>
                            <span class="nav-item-name">${{step.name}}</span>
                            <span class="nav-item-badges">${{badges.join('')}}</span>
                        </div>
                    `;
                }});
            }});

            html += '</div></div>';
        }});

        html += '</div>';
        nav.innerHTML = html;
    }}

    function toggleSection(name) {{
        if (expandedSections.has(name)) {{
            expandedSections.delete(name);
        }} else {{
            expandedSections.add(name);
        }}
        renderNav();
    }}

    function toggleStep(stepId) {{
        const card = document.querySelector(`[data-step-card="${{stepId}}"]`);
        if (card) {{
            card.classList.toggle('expanded');
            expandedSteps.has(stepId) ? expandedSteps.delete(stepId) : expandedSteps.add(stepId);
        }}
    }}

    function scrollToStep(stepId) {{
        const element = document.querySelector(`[data-step-card="${{stepId}}"]`);
        if (element) {{
            element.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            element.classList.add('expanded');
            expandedSteps.add(stepId);
        }}
    }}

    function scrollToSection(name) {{
        const section = document.querySelector(`[data-section="${{name}}"]`);
        if (section) {{
            section.scrollIntoView({{ behavior: 'smooth' }});
            expandedSections.add(name);
            renderNav();
        }}
    }}

    function renderMain() {{
        const main = document.getElementById('main');
        let html = '';

        // Hero
        html += `
            <section class="hero">
                <div class="hero-content">
                    <div class="hero-badge">⚡ 3-Skill Chain · 7-Level Architecture</div>
                    <h1 class="hero-title">Research Pipeline</h1>
                    <p class="hero-subtitle">Complete end-to-end workflow for academic paper research, analysis, and synthesis with full provenance tracking.</p>

                    <div class="stats-grid">
                        <div class="stat-card">
                            <div class="stat-value">${{DATA.stats.total_steps}}</div>
                            <div class="stat-label">Total Steps</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${{DATA.stats.total_phases}}</div>
                            <div class="stat-label">Phases</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${{DATA.stats.total_gates}}</div>
                            <div class="stat-label">User Gates</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${{DATA.stats.total_scripts}}</div>
                            <div class="stat-label">Scripts</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${{DATA.stats.total_subagents}}</div>
                            <div class="stat-label">Subagent Steps</div>
                        </div>
                        <div class="stat-card">
                            <div class="stat-value">${{DATA.stats.total_files}}</div>
                            <div class="stat-label">File Types</div>
                        </div>
                    </div>

                    <div class="pipeline-diagram">
        `;

        DATA.pipeline.forEach((node, i) => {{
            const cls = getClass(node.name);
            const outputs = node.key_outputs || [];

            html += `
                <div class="pipeline-node ${{cls}}" onclick="scrollToSection('${{node.name}}')">
                    <div class="pipeline-node-header">
                        <div class="pipeline-node-icon">${{getIcon(node.name)}}</div>
                        <div>
                            <div class="pipeline-node-title">${{formatName(node.name)}}</div>
                            <div class="pipeline-node-phase">Phase ${{i + 1}} · v${{node.version || '?'}}</div>
                        </div>
                    </div>
                    <div class="pipeline-node-desc">${{node.description || ''}}</div>
                    <div class="pipeline-node-stats">
                        <div class="pipeline-node-stat"><strong>${{node.steps}}</strong> steps</div>
                        <div class="pipeline-node-stat"><strong>${{node.phases}}</strong> phases</div>
                        <div class="pipeline-node-stat"><strong>${{node.gates}}</strong> gates</div>
                    </div>
                    ${{outputs.length > 0 ? `
                        <div class="pipeline-outputs">
                            ${{outputs.slice(0, 2).map(o => `
                                <div class="pipeline-output">
                                    <span class="pipeline-output-icon">→</span>
                                    <span>${{o}}</span>
                                </div>
                            `).join('')}}
                        </div>
                    ` : ''}}
                </div>
            `;

            if (i < DATA.pipeline.length - 1) {{
                html += `
                    <div class="pipeline-arrow">
                        <div class="pipeline-arrow-line"></div>
                    </div>
                `;
            }}
        }});

        html += '</div></div></section>';

        // Sections
        DATA.orchestrators.forEach(orch => {{
            const cls = getClass(orch.name);

            html += `
                <section class="section" id="${{orch.name}}" data-section="${{orch.name}}">
                    <div class="section-header">
                        <div class="section-icon ${{cls}}">${{getIcon(orch.name)}}</div>
                        <div class="section-info">
                            <h2>${{formatName(orch.name)}}</h2>
                            <p>${{orch.description || ''}}</p>
                            <div class="section-meta">
                                <span class="section-meta-item"><strong>${{orch.total_steps}}</strong> steps</span>
                                <span class="section-meta-item"><strong>${{orch.phases.length}}</strong> phases</span>
                                <span class="section-meta-item"><strong>${{orch.total_gates}}</strong> gates</span>
                                ${{orch.version ? `<span class="section-meta-item">v${{orch.version}}</span>` : ''}}
                            </div>
                        </div>
                    </div>
            `;

            orch.phases.forEach(phase => {{
                html += `
                    <div class="phase-header">
                        <div class="phase-letter ${{phase.letter}}">${{phase.letter}}</div>
                        <div class="phase-info">
                            <div class="phase-name">${{phase.name}}</div>
                            <div class="phase-meta">${{phase.steps.length}} steps</div>
                        </div>
                    </div>
                `;

                phase.steps.forEach(step => {{
                    const stepId = `${{orch.name}}-${{step.id}}`;
                    const isExpanded = expandedSteps.has(stepId);

                    html += `
                        <div class="step-card ${{isExpanded ? 'expanded' : ''}}" data-step-card="${{stepId}}" id="${{stepId}}">
                            <div class="step-card-header" onclick="toggleStep('${{stepId}}')">
                                <div class="step-number">${{step.number}}</div>
                                <div class="step-info">
                                    <div class="step-title">${{step.name}}</div>
                                    <div class="step-description">${{step.description || ''}}</div>
                                    <div class="step-meta">
                                        ${{step.level ? `<span class="step-meta-badge level">Level ${{step.level}}</span>` : ''}}
                                        ${{step.is_script ? '<span class="step-meta-badge script">⚙️ Script</span>' : ''}}
                                        ${{step.subagent ? '<span class="step-meta-badge subagent">🤖 Subagent</span>' : ''}}
                                        ${{step.gate ? '<span class="step-meta-badge gate">⚡ Gate</span>' : ''}}
                                    </div>
                                </div>
                                <div class="step-expand">▼</div>
                            </div>
                            <div class="step-content">
                                ${{renderStepContent(step)}}
                            </div>
                        </div>
                    `;
                }});
            }});

            html += '</section>';
        }});

        // Footer
        html += `
            <footer class="footer">
                <div class="footer-content">
                    <div class="footer-logo">Research Pipeline Visualizer v6</div>
                    <div class="footer-meta">Generated ${{new Date().toLocaleString()}} · 10x Better Edition</div>
                </div>
            </footer>
        `;

        main.innerHTML = html;
    }}

    function renderStepContent(step) {{
        let html = '';

        // Sub-steps
        if (step.sub_steps && step.sub_steps.length > 0) {{
            html += `
                <div class="content-section">
                    <div class="content-section-title">📋 Sub-steps (${{step.sub_steps.length}})</div>
                    <div class="substeps">
                        ${{step.sub_steps.map(ss => `
                            <div class="substep">
                                <div class="substep-number">${{ss.number}}</div>
                                <div class="substep-info">
                                    <div class="substep-name">${{ss.name}}</div>
                                    ${{ss.description ? `<div class="substep-desc">${{ss.description}}</div>` : ''}}
                                </div>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
        }}

        // Inputs
        if (step.inputs && step.inputs.length > 0) {{
            html += `
                <div class="content-section">
                    <div class="content-section-title">📥 Inputs (${{step.inputs.length}})</div>
                    <div class="files-grid">
                        ${{step.inputs.map(f => `
                            <div class="file-item">
                                <div class="file-icon input">→</div>
                                <div class="file-info">
                                    <div class="file-path">${{f.path}}</div>
                                    <div class="file-format">${{f.format}}</div>
                                </div>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
        }}

        // Outputs
        if (step.outputs && step.outputs.length > 0) {{
            html += `
                <div class="content-section">
                    <div class="content-section-title">📤 Outputs (${{step.outputs.length}})</div>
                    <div class="files-grid">
                        ${{step.outputs.map(f => `
                            <div class="file-item">
                                <div class="file-icon output">✓</div>
                                <div class="file-info">
                                    <div class="file-path">${{f.path}}</div>
                                    <div class="file-format">${{f.format}}</div>
                                </div>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
        }}

        // Scripts
        if (step.scripts && step.scripts.length > 0) {{
            html += `
                <div class="content-section">
                    <div class="content-section-title">⚙️ Scripts (${{step.scripts.length}})</div>
                    <div class="scripts-list">
                        ${{step.scripts.map((cmd, i) => `
                            <div class="script-item">
                                <div class="script-header">
                                    <div class="script-icon">⚙️</div>
                                    <div class="script-name">${{step.script_names && step.script_names[i] ? step.script_names[i] : 'Script'}}</div>
                                </div>
                                <div class="script-command">${{cmd}}</div>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
        }}

        // Subagent
        if (step.subagent) {{
            const sa = step.subagent;
            html += `
                <div class="content-section">
                    <div class="content-section-title">🤖 Subagent Configuration</div>
                    <div class="subagent-card">
                        <div class="subagent-header">
                            <div class="subagent-icon">🤖</div>
                            <div>
                                <div class="subagent-title">Parallel Subagents</div>
                                <div class="subagent-type">${{sa.type}}</div>
                            </div>
                        </div>
                        <div class="subagent-stats">
                            <div class="subagent-stat">
                                <div class="subagent-stat-value">${{sa.concurrency}}</div>
                                <div class="subagent-stat-label">Max Parallel</div>
                            </div>
                            <div class="subagent-stat">
                                <div class="subagent-stat-value">${{sa.timeout}}</div>
                                <div class="subagent-stat-label">Timeout</div>
                            </div>
                            <div class="subagent-stat">
                                <div class="subagent-stat-value">${{sa.retry}}</div>
                                <div class="subagent-stat-label">Retries</div>
                            </div>
                        </div>
                        <div class="subagent-visual">
                            ${{Array(Math.min(sa.concurrency, 15)).fill(0).map(() => '<div class="subagent-slot">▶</div>').join('')}}
                        </div>
                    </div>
                </div>
            `;
        }}

        // Gate
        if (step.gate) {{
            html += `
                <div class="content-section">
                    <div class="content-section-title">⚡ User Decision Gate</div>
                    <div class="gate-card">
                        <div class="gate-header">
                            <div class="gate-icon">⚡</div>
                            <div>
                                <div class="gate-title">${{step.gate.name || 'Decision Point'}}</div>
                                <div class="gate-subtitle">User approval required</div>
                            </div>
                        </div>
                        <div class="gate-options">
                            ${{step.gate.options.map(opt => `
                                <div class="gate-option">
                                    <div class="gate-key">${{opt.key}}</div>
                                    <div class="gate-label">${{opt.label}}</div>
                                </div>
                            `).join('')}}
                        </div>
                    </div>
                </div>
            `;
        }}

        // Validation checks
        if (step.validation_checks && step.validation_checks.length > 0) {{
            html += `
                <div class="content-section">
                    <div class="content-section-title">✓ Validation Checks</div>
                    <div class="validation-list">
                        ${{step.validation_checks.map(check => `
                            <div class="validation-item">
                                <span class="validation-icon">✓</span>
                                <span>${{check}}</span>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
        }}

        return html || '<div style="color: var(--text-muted); padding: 20px;">No additional details for this step.</div>';
    }}

    // Scroll spy
    function updateScrollSpy() {{
        const sections = document.querySelectorAll('[data-section]');
        const steps = document.querySelectorAll('[data-step-card]');
        const scrollY = window.scrollY;
        const windowHeight = window.innerHeight;

        // Progress bar
        const docHeight = document.documentElement.scrollHeight - windowHeight;
        const progress = (scrollY / docHeight) * 100;
        document.getElementById('progressBar').style.width = progress + '%';

        // Current section
        let currentSection = null;
        sections.forEach(section => {{
            const rect = section.getBoundingClientRect();
            if (rect.top <= windowHeight / 3) {{
                currentSection = section.dataset.section;
            }}
        }});

        document.querySelectorAll('.nav-section-header').forEach(header => {{
            const section = header.closest('.nav-section');
            if (section && section.dataset.orch === currentSection) {{
                header.classList.add('active');
            }} else {{
                header.classList.remove('active');
            }}
        }});

        // Current step
        let currentStep = null;
        steps.forEach(step => {{
            const rect = step.getBoundingClientRect();
            if (rect.top <= windowHeight / 2 && rect.bottom > 0) {{
                currentStep = step.dataset.stepCard;
            }}
        }});

        document.querySelectorAll('.nav-item').forEach(item => {{
            if (item.dataset.step === currentStep) {{
                item.classList.add('active');
            }} else {{
                item.classList.remove('active');
            }}
        }});
    }}

    let scrollTimeout;
    window.addEventListener('scroll', () => {{
        if (scrollTimeout) return;
        scrollTimeout = setTimeout(() => {{
            updateScrollSpy();
            scrollTimeout = null;
        }}, 50);
    }});

    // Init
    renderNav();
    renderMain();
    updateScrollSpy();
    </script>
</body>
</html>'''

    return html

# ============================================================================
# MAIN
# ============================================================================

def main():
    pipeline_dir = Path(__file__).parent / "orchestrators"

    if not pipeline_dir.exists():
        print(f"Error: {pipeline_dir} not found", file=sys.stderr)
        sys.exit(1)

    skill_files = list(pipeline_dir.glob("*/SKILL.md"))

    if not skill_files:
        print(f"Error: No SKILL.md files found in {pipeline_dir}", file=sys.stderr)
        sys.exit(1)

    PIPELINE_ORDER = {
        'create-research-project': 0,
        'analyze-research-project': 1,
        'synthesize-research-project': 2,
    }

    skill_files.sort(key=lambda p: PIPELINE_ORDER.get(p.parent.name, 99))

    print(f"Found {len(skill_files)} orchestrators:")

    orchestrators = []
    for skill_file in skill_files:
        print(f"  Parsing: {skill_file.parent.name}")
        content = skill_file.read_text(encoding='utf-8')
        orch = parse_skill_md(content, skill_file)
        print(f"    - {orch.total_steps} steps, {len(orch.phases)} phases, {orch.total_gates} gates")
        orchestrators.append(orch)

    file_graph = build_file_graph(orchestrators)
    print(f"\nFile graph: {len(file_graph['nodes'])} files, {len(file_graph['edges'])} edges")

    html = generate_html(orchestrators, file_graph)

    output_file = Path(__file__).parent / "research_pipeline_v6.html"
    output_file.write_text(html, encoding='utf-8')
    print(f"\nGenerated: {output_file}")

if __name__ == "__main__":
    main()

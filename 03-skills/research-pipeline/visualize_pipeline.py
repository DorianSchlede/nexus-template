#!/usr/bin/env python3
"""
Research Pipeline Visualizer v4 - Full Depth Edition
Parses all 3 orchestrator SKILL.md files and generates a comprehensive
interactive HTML visualization with:
- Multi-orchestrator pipeline view
- Hierarchical drill-down (phases → steps → sub-steps)
- File dependency graph
- Subagent spawn visualization
- Token budgets and concurrency indicators
- User gates with decision branches
- SCRIPT DOCUMENTATION with inputs/outputs/purpose
- OUTPUT FILE EXPLANATIONS
"""

import re
import json
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any

# Import script registry for documentation
try:
    from shared.contracts.script_registry import SCRIPT_REGISTRY, OUTPUT_FILES, get_script_doc
except ImportError:
    # Fallback if running standalone
    SCRIPT_REGISTRY = {}
    OUTPUT_FILES = {}
    def get_script_doc(name): return None

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class FileRef:
    path: str
    type: str  # input, output, config
    format: str = ""  # md, yaml, json, py

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
    key: str  # Y, N, S
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

@dataclass
class ScriptInfo:
    """Documentation for a script used in a step."""
    name: str
    purpose: str = ""
    description: str = ""
    level: Optional[int] = None
    inputs: List[Dict[str, str]] = field(default_factory=list)
    outputs: List[Dict[str, str]] = field(default_factory=list)
    key_features: List[str] = field(default_factory=list)

@dataclass
class OutputFileInfo:
    """Documentation for an output file."""
    path: str
    description: str = ""
    created_by: str = ""
    contains: List[str] = field(default_factory=list)

@dataclass
class Step:
    id: str
    number: str
    name: str
    phase: str
    phase_name: str
    description: str = ""
    sub_steps: List[SubStep] = field(default_factory=list)
    inputs: List[FileRef] = field(default_factory=list)
    outputs: List[FileRef] = field(default_factory=list)
    scripts: List[str] = field(default_factory=list)
    script_docs: List[ScriptInfo] = field(default_factory=list)  # NEW: Script documentation
    output_docs: List[OutputFileInfo] = field(default_factory=list)  # NEW: Output file docs
    skills_used: List[str] = field(default_factory=list)
    subagent: Optional[SubagentConfig] = None
    gate: Optional[Gate] = None
    handoff_to: Optional[str] = None
    is_script: bool = False  # vs LLM subagent
    level: Optional[int] = None  # For synthesis levels
    raw_content: str = ""

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

# ============================================================================
# PARSING
# ============================================================================

def get_file_format(path: str) -> str:
    """Extract file format from path."""
    if '.md' in path: return 'md'
    if '.yaml' in path or '.yml' in path: return 'yaml'
    if '.json' in path: return 'json'
    if '.py' in path: return 'py'
    return 'unknown'

def parse_subagent_config(content: str) -> Optional[SubagentConfig]:
    """Extract subagent configuration from step content."""
    # Check for actual Task() spawn pattern - must have Task( with subagent_type
    # or explicit "Spawn" instruction with subagent context
    has_task_spawn = bool(re.search(r'Task\s*\(\s*\n?\s*subagent_type', content))
    has_spawn_instruction = bool(re.search(r'[Ss]pawn\s+(?:subagent|batch|extraction|final)', content))

    # Exclude if it's just describing subagent behavior or referencing subagents
    is_just_reference = bool(re.search(r'(?:subagent\s+(?:reads|output|prompt)|for\s+subagents)', content, re.IGNORECASE))

    if not (has_task_spawn or has_spawn_instruction) or is_just_reference:
        return None

    config = SubagentConfig()

    # Extract type
    type_match = re.search(r'subagent_type\s*=\s*["\']([^"\']+)["\']', content)
    if type_match:
        config.type = type_match.group(1)

    # Extract concurrency
    conc_match = re.search(r'(?:max|Max)\s+(\d+)\s+(?:concurrent|parallel)', content, re.IGNORECASE)
    if conc_match:
        config.concurrency = int(conc_match.group(1))

    # Extract timeout
    timeout_match = re.search(r'[Tt]imeout.*?(\d+)\s*(min|sec|hour)', content)
    if timeout_match:
        config.timeout = f"{timeout_match.group(1)} {timeout_match.group(2)}"

    # Extract retry
    retry_match = re.search(r'[Rr]etry.*?(\d+)', content)
    if retry_match:
        config.retry = int(retry_match.group(1))

    # Extract INPUT CONTRACT
    input_section = re.search(r'Files You MUST Read.*?Files You MUST NOT', content, re.DOTALL)
    if input_section:
        inputs = re.findall(r'`([^`]+\.(?:md|yaml|json|py))`', input_section.group(0))
        config.input_contract = inputs[:8]

    # Extract outputs
    output_patterns = re.findall(r'(?:Write|Output).*?`([^`]+\.(?:md|yaml|json))`', content, re.IGNORECASE)
    config.output_contract = list(set(output_patterns))[:4]

    return config

def parse_gate(step_name: str, content: str) -> Optional[Gate]:
    """Extract user gate configuration."""
    if not re.search(r'\[Y\]|\[N\]|\[S\]|[Gg]ate|[Uu]ser\s+[Aa]pproval', content):
        return None

    gate = Gate(name=step_name)

    # Extract options
    for m in re.finditer(r'\[([YNS])\]\s*[:\-]?\s*(.+?)(?=\n|\[|$)', content):
        key = m.group(1)
        label = m.group(2).strip()[:60]

        # Find target
        target = ""
        if '->' in label or '→' in label:
            parts = re.split(r'->|→', label)
            if len(parts) > 1:
                target = parts[1].strip()
                label = parts[0].strip()

        gate.options.append(GateOption(key=key, label=label, target=target))

    if not gate.options:
        gate.options.append(GateOption(key="Y", label="Continue", target="next step"))
        gate.options.append(GateOption(key="N", label="Go back", target="previous"))

    return gate

def parse_skill_md(content: str, file_path: Path) -> Orchestrator:
    """Parse a SKILL.md file into an Orchestrator structure."""

    orch = Orchestrator(
        name=file_path.parent.name,
        path=str(file_path),
        description=""
    )

    # Extract frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm_content = fm_match.group(1)
        name_match = re.search(r'^name:\s*(.+)$', fm_content, re.MULTILINE)
        desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', fm_content, re.MULTILINE)
        if name_match:
            orch.name = name_match.group(1).strip()
        if desc_match:
            orch.description = desc_match.group(1).strip()[:200]

    # Extract handoff info
    handoff_from = re.search(r'[Rr]eceives?\s+from[:\s]+[`"]?([^`"\n]+)', content)
    handoff_to = re.search(r'[Hh]ands?\s+off\s+to[:\s]+[`"]?([^`"\n]+)', content)
    if handoff_from:
        orch.handoff_from = handoff_from.group(1).strip()
    if handoff_to:
        orch.handoff_to = handoff_to.group(1).strip()

    # Find phases
    phase_pattern = r'#\s*PHASE\s+([A-Z]):\s*(.+?)(?=\n)'
    phase_positions = [(m.start(), m.group(1), m.group(2).strip())
                       for m in re.finditer(phase_pattern, content)]

    phases: Dict[str, Phase] = {}

    def get_phase_at_pos(pos: int) -> tuple:
        current = ("A", "Setup")
        for phase_pos, letter, name in phase_positions:
            if phase_pos < pos:
                current = (letter, name)
            else:
                break
        return current

    # Find all steps
    step_pattern = r'^##\s*[Ss]tep\s+(\d+(?:\.\d+)?)\s*:?\s*(.+?)$'
    step_matches = list(re.finditer(step_pattern, content, re.MULTILINE))

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

        # Extract description
        desc = ""
        desc_match = re.search(r'\*\*([^*]{10,200})\*\*', step_content[:600])
        if desc_match:
            desc = desc_match.group(1).strip()

        # Extract sub-steps
        sub_steps = []
        for m in re.finditer(rf'###\s+{step_num}\.(\d+)\s*:?\s*(.+?)(?=\n)', step_content):
            sub_steps.append(SubStep(
                number=f"{step_num}.{m.group(1)}",
                name=m.group(2).strip()[:80]
            ))

        # Extract inputs
        inputs = []
        input_patterns = [
            r'[Rr]ead\s+`([^`]+\.(?:md|yaml|json))`',
            r'[Ll]oad\s+`([^`]+\.(?:md|yaml|json))`',
            r'[Ii]nput:\s*`([^`]+)`',
            r'from\s+`([^`]+\.(?:md|yaml|json))`',
        ]
        for pattern in input_patterns:
            for m in re.finditer(pattern, step_content):
                path = m.group(1)
                if path and not any(i.path == path for i in inputs):
                    inputs.append(FileRef(path=path, type="input", format=get_file_format(path)))

        # Extract outputs
        outputs = []
        output_patterns = [
            r'[Oo]utput:\s*`([^`]+)`',
            r'[Ww]rite\s+to:\s*`?([^`\n]+)`?',
            r'[Cc]reates?:\s*`([^`]+)`',
            r'[Ss]ave\s+to:\s*`?([^`\n]+)`?',
            r'→\s*([^\n]+\.(?:md|yaml|json))',
        ]
        for pattern in output_patterns:
            for m in re.finditer(pattern, step_content):
                path = m.group(1).strip().strip('`')
                if path and '/' in path or path.endswith(('.md', '.yaml', '.json')):
                    if not any(o.path == path for o in outputs):
                        outputs.append(FileRef(path=path, type="output", format=get_file_format(path)))

        # Extract scripts and their documentation
        scripts = []
        script_docs = []
        script_blocks = re.findall(r'```(?:bash|python|sh)\n(.*?)```', step_content, re.DOTALL)
        for block in script_blocks:
            lines = [l.strip() for l in block.strip().split('\n')
                    if l.strip() and not l.strip().startswith('#')]
            if lines:
                cmd = lines[0][:100]
                if cmd and cmd not in scripts:
                    scripts.append(cmd)

                    # Look up script documentation
                    script_name = None
                    py_match = re.search(r'(\w+\.py)', cmd)
                    if py_match:
                        script_name = py_match.group(1)

                    if script_name and SCRIPT_REGISTRY:
                        doc = get_script_doc(script_name)
                        if doc:
                            script_docs.append(ScriptInfo(
                                name=doc.name,
                                purpose=doc.purpose,
                                description=doc.description.strip()[:500],
                                level=doc.level,
                                inputs=doc.inputs[:5],
                                outputs=doc.outputs[:5],
                                key_features=doc.key_features[:5]
                            ))

        # Extract output file documentation
        output_docs = []
        if OUTPUT_FILES:
            for out in outputs:
                # Match by filename pattern
                filename = out.path.split('/')[-1] if '/' in out.path else out.path
                for pattern, doc in OUTPUT_FILES.items():
                    # Handle patterns like _batch_{field}_{N}.yaml
                    pattern_regex = pattern.replace('{field}', r'\w+').replace('{N}', r'\d+')
                    if re.match(pattern_regex, filename) or filename == pattern:
                        output_docs.append(OutputFileInfo(
                            path=out.path,
                            description=doc.get('description', ''),
                            created_by=doc.get('created_by', ''),
                            contains=doc.get('contains', [])[:5]
                        ))
                        break

        # Check if step uses script vs subagent
        is_script = bool(re.search(r'(?:Script|SCRIPT|python\s+\w+\.py|deterministic)', step_content))

        # Extract level number (for synthesis)
        level = None
        level_match = re.search(r'[Ll]evel\s+(\d+)', step_name) or re.search(r'[Ll]evel\s+(\d+)', step_content[:200])
        if level_match:
            level = int(level_match.group(1))

        # Extract subagent config
        subagent = parse_subagent_config(step_content)

        # Extract gate
        gate = parse_gate(step_name, step_content)
        if gate:
            orch.total_gates += 1

        # Extract handoff
        handoff = None
        handoff_match = re.search(r'(?:handoff|hand\s+off|proceed)\s+to[:\s]+[`"]?([^`"\n]+)', step_content, re.IGNORECASE)
        if handoff_match:
            handoff = handoff_match.group(1).strip()

        step = Step(
            id=f"step_{step_num.replace('.', '_')}",
            number=step_num,
            name=step_name,
            phase=phase_letter,
            phase_name=phase_name,
            description=desc,
            sub_steps=sub_steps[:10],
            inputs=inputs[:10],
            outputs=outputs[:10],
            scripts=scripts[:5],
            script_docs=script_docs[:5],
            output_docs=output_docs[:5],
            subagent=subagent,
            gate=gate,
            handoff_to=handoff,
            is_script=is_script,
            level=level
        )

        phases[phase_letter].steps.append(step)
        orch.total_steps += 1

    orch.phases = [phases[k] for k in sorted(phases.keys())]
    return orch

def build_file_graph(orchestrators: List[Orchestrator]) -> Dict:
    """Build a file dependency graph across all orchestrators."""
    nodes = {}  # file_path -> {type, format, producers, consumers}
    edges = []  # {source, target, type}

    for orch in orchestrators:
        for phase in orch.phases:
            for step in phase.steps:
                step_id = f"{orch.name}:{step.number}"

                for inp in step.inputs:
                    if inp.path not in nodes:
                        nodes[inp.path] = {"type": inp.type, "format": inp.format, "producers": [], "consumers": []}
                    nodes[inp.path]["consumers"].append(step_id)
                    edges.append({"source": inp.path, "target": step_id, "type": "input"})

                for out in step.outputs:
                    if out.path not in nodes:
                        nodes[out.path] = {"type": out.type, "format": out.format, "producers": [], "consumers": []}
                    nodes[out.path]["producers"].append(step_id)
                    edges.append({"source": step_id, "target": out.path, "type": "output"})

    return {"nodes": nodes, "edges": edges}

# ============================================================================
# HTML GENERATION
# ============================================================================

def serialize_orchestrator(orch: Orchestrator) -> dict:
    """Convert Orchestrator to JSON-serializable dict."""
    def serialize_dataclass(obj):
        if hasattr(obj, '__dataclass_fields__'):
            result = {}
            for field_name in obj.__dataclass_fields__:
                value = getattr(obj, field_name)
                result[field_name] = serialize_dataclass(value)
            return result
        elif isinstance(obj, list):
            return [serialize_dataclass(item) for item in obj]
        elif isinstance(obj, dict):
            return {k: serialize_dataclass(v) for k, v in obj.items()}
        else:
            return obj

    return serialize_dataclass(orch)

def generate_html(orchestrators: List[Orchestrator], file_graph: Dict) -> str:
    """Generate the complete HTML visualization with endless scroll and sticky sidebar."""

    data = {
        "orchestrators": [serialize_orchestrator(o) for o in orchestrators],
        "file_graph": file_graph,
        "pipeline": [
            {"name": o.name, "steps": o.total_steps, "gates": o.total_gates,
             "phases": len(o.phases), "handoff_to": o.handoff_to}
            for o in orchestrators
        ]
    }

    data_json = json.dumps(data, indent=2)

    html = f'''<!DOCTYPE html>
<html lang="en" class="smooth-scroll">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Pipeline - Full Visualization</title>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --bg-elevated: #30363d;
            --border: #30363d;
            --border-subtle: #21262d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-purple: #a371f7;
            --accent-orange: #d29922;
            --accent-red: #f85149;
            --accent-pink: #db61a2;
            --accent-cyan: #39c5cf;
            --phase-a: #238636;
            --phase-b: #1f6feb;
            --phase-c: #9e6a03;
            --phase-d: #8957e5;
            --phase-e: #bf4b8a;
            --phase-f: #1a7f37;
            --phase-g: #0969da;
            --phase-h: #bc4c00;
            --phase-i: #6e40c9;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.5;
            overflow-x: hidden;
        }}

        /* Header */
        .header {{
            background: linear-gradient(180deg, var(--bg-secondary) 0%, var(--bg-primary) 100%);
            border-bottom: 1px solid var(--border);
            padding: 20px 32px;
            position: sticky;
            top: 0;
            z-index: 100;
        }}
        .header-top {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 16px;
        }}
        .header h1 {{
            font-size: 24px;
            font-weight: 600;
            background: linear-gradient(90deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .header-actions {{
            display: flex;
            gap: 8px;
        }}
        .btn {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            color: var(--text-secondary);
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            cursor: pointer;
            transition: all 0.15s;
        }}
        .btn:hover {{
            background: var(--bg-elevated);
            color: var(--text-primary);
        }}
        .btn.active {{
            background: var(--accent-blue);
            border-color: var(--accent-blue);
            color: white;
        }}

        /* Pipeline Overview */
        .pipeline {{
            display: flex;
            align-items: center;
            gap: 0;
            padding: 8px 0;
        }}
        .pipeline-node {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border);
            border-radius: 12px;
            padding: 16px 20px;
            min-width: 200px;
            cursor: pointer;
            transition: all 0.2s;
            position: relative;
        }}
        .pipeline-node:hover {{
            border-color: var(--accent-blue);
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(88, 166, 255, 0.1);
        }}
        .pipeline-node.active {{
            border-color: var(--accent-blue);
            background: rgba(88, 166, 255, 0.1);
        }}
        .pipeline-node h3 {{
            font-size: 14px;
            font-weight: 600;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .pipeline-node h3::before {{
            content: '';
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background: var(--accent-green);
        }}
        .pipeline-stats {{
            display: flex;
            gap: 12px;
            font-size: 11px;
            color: var(--text-muted);
        }}
        .pipeline-stat {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .pipeline-arrow {{
            width: 40px;
            height: 2px;
            background: var(--border);
            position: relative;
        }}
        .pipeline-arrow::after {{
            content: '';
            position: absolute;
            right: 0;
            top: -4px;
            border: 5px solid transparent;
            border-left-color: var(--border);
        }}

        /* Main Layout */
        .main {{
            display: flex;
            height: calc(100vh - 140px);
        }}

        /* Sidebar - Phase List */
        .sidebar {{
            width: 280px;
            background: var(--bg-secondary);
            border-right: 1px solid var(--border);
            overflow-y: auto;
            flex-shrink: 0;
        }}
        .phase-group {{
            border-bottom: 1px solid var(--border-subtle);
        }}
        .phase-header {{
            padding: 12px 16px;
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            background: var(--bg-primary);
            display: flex;
            align-items: center;
            gap: 8px;
            cursor: pointer;
        }}
        .phase-header .phase-badge {{
            width: 20px;
            height: 20px;
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            font-weight: 700;
            color: white;
        }}
        .step-item {{
            padding: 10px 16px 10px 44px;
            font-size: 13px;
            color: var(--text-secondary);
            cursor: pointer;
            border-left: 3px solid transparent;
            transition: all 0.1s;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .step-item:hover {{
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }}
        .step-item.active {{
            background: rgba(88, 166, 255, 0.1);
            border-left-color: var(--accent-blue);
            color: var(--text-primary);
        }}
        .step-num {{
            font-size: 10px;
            font-weight: 600;
            color: var(--text-muted);
            background: var(--bg-tertiary);
            padding: 2px 6px;
            border-radius: 4px;
            min-width: 24px;
            text-align: center;
        }}
        .step-name {{
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .step-badges {{
            display: flex;
            gap: 4px;
        }}
        .mini-badge {{
            font-size: 9px;
            padding: 2px 4px;
            border-radius: 3px;
        }}
        .mini-badge.gate {{
            background: rgba(210, 153, 34, 0.3);
            color: var(--accent-orange);
        }}
        .mini-badge.subagent {{
            background: rgba(163, 113, 247, 0.3);
            color: var(--accent-purple);
        }}
        .mini-badge.script {{
            background: rgba(57, 197, 207, 0.3);
            color: var(--accent-cyan);
        }}

        /* Content Panel */
        .content {{
            flex: 1;
            overflow-y: auto;
            padding: 24px 32px;
        }}
        .content-header {{
            margin-bottom: 24px;
            padding-bottom: 16px;
            border-bottom: 1px solid var(--border);
        }}
        .content-header h2 {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .content-header .phase-tag {{
            font-size: 12px;
            color: var(--text-muted);
            font-weight: 400;
        }}
        .content-header .desc {{
            color: var(--text-secondary);
            font-size: 14px;
            margin-top: 8px;
        }}

        /* Cards */
        .card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            margin-bottom: 16px;
            overflow: hidden;
        }}
        .card-header {{
            padding: 12px 16px;
            background: var(--bg-tertiary);
            border-bottom: 1px solid var(--border);
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .card-header svg {{
            width: 14px;
            height: 14px;
        }}
        .card-content {{
            padding: 16px;
        }}

        /* Sub-steps */
        .sub-step {{
            display: flex;
            align-items: flex-start;
            gap: 10px;
            padding: 8px 0;
            border-bottom: 1px solid var(--border-subtle);
        }}
        .sub-step:last-child {{
            border-bottom: none;
        }}
        .sub-step-num {{
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            background: var(--bg-tertiary);
            padding: 2px 8px;
            border-radius: 4px;
            flex-shrink: 0;
        }}
        .sub-step-name {{
            font-size: 13px;
            color: var(--text-secondary);
        }}

        /* File list */
        .file-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 12px;
            background: var(--bg-tertiary);
            border-radius: 6px;
            margin-bottom: 6px;
            font-family: 'SF Mono', SFMono-Regular, ui-monospace, monospace;
            font-size: 12px;
        }}
        .file-icon {{
            width: 16px;
            height: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            flex-shrink: 0;
        }}
        .file-icon.input {{ color: var(--accent-blue); }}
        .file-icon.output {{ color: var(--accent-green); }}
        .file-path {{
            flex: 1;
            word-break: break-all;
            color: var(--text-secondary);
        }}
        .file-format {{
            font-size: 10px;
            padding: 2px 6px;
            background: var(--bg-elevated);
            border-radius: 3px;
            color: var(--text-muted);
        }}

        /* Output documentation card */
        .output-doc-card {{
            background: linear-gradient(135deg, rgba(63, 185, 80, 0.08) 0%, rgba(63, 185, 80, 0.03) 100%);
            border: 1px solid rgba(63, 185, 80, 0.2);
            border-radius: 8px;
            padding: 12px;
            margin-bottom: 8px;
        }}
        .output-doc-card .file-item {{
            margin-bottom: 8px;
            background: transparent;
            padding: 0;
        }}
        .output-description {{
            color: var(--text-muted);
            font-size: 12px;
            line-height: 1.4;
            margin-bottom: 8px;
        }}
        .output-created-by {{
            font-size: 11px;
            color: var(--text-muted);
            margin-bottom: 6px;
        }}
        .output-created-by span {{
            color: var(--accent-cyan);
        }}
        .output-contains {{
            margin-top: 8px;
        }}
        .contains-label {{
            font-size: 11px;
            color: var(--text-muted);
            font-weight: 600;
        }}
        .contains-list {{
            list-style: none;
            padding: 0;
            margin: 4px 0 0 0;
        }}
        .contains-list li {{
            font-size: 11px;
            color: var(--text-muted);
            padding: 2px 0 2px 14px;
            position: relative;
        }}
        .contains-list li::before {{
            content: '→';
            position: absolute;
            left: 0;
            color: var(--accent-green);
        }}

        /* Script block */
        .script-block {{
            background: var(--bg-tertiary);
            border-radius: 6px;
            padding: 12px;
            font-family: 'SF Mono', SFMono-Regular, ui-monospace, monospace;
            font-size: 12px;
            color: var(--accent-cyan);
            margin-bottom: 6px;
            border-left: 3px solid var(--accent-cyan);
        }}
        .script-block::before {{
            content: '$ ';
            color: var(--text-muted);
        }}

        /* Script documentation card */
        .script-doc-card {{
            background: linear-gradient(135deg, rgba(56, 139, 253, 0.08) 0%, rgba(56, 139, 253, 0.03) 100%);
            border: 1px solid rgba(56, 139, 253, 0.25);
            border-radius: 10px;
            padding: 16px;
            margin-bottom: 12px;
        }}
        .script-doc-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 10px;
        }}
        .script-icon {{
            font-size: 18px;
        }}
        .script-name {{
            font-weight: 600;
            font-size: 14px;
            color: var(--accent-cyan);
        }}
        .script-level {{
            background: var(--accent-orange);
            color: #000;
            padding: 2px 8px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 600;
            margin-left: auto;
        }}
        .script-purpose {{
            color: var(--text-secondary);
            font-size: 13px;
            margin-bottom: 10px;
            font-weight: 500;
        }}
        .script-description {{
            color: var(--text-muted);
            font-size: 12px;
            line-height: 1.5;
            margin-bottom: 12px;
            padding: 10px;
            background: rgba(0,0,0,0.2);
            border-radius: 6px;
        }}
        .script-io {{
            margin-bottom: 10px;
        }}
        .script-io-header {{
            color: var(--text-secondary);
            font-size: 12px;
            font-weight: 600;
            margin-bottom: 6px;
        }}
        .script-io-item {{
            display: flex;
            gap: 10px;
            padding: 4px 0;
            font-size: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}
        .script-io-item:last-child {{
            border-bottom: none;
        }}
        .io-name {{
            color: var(--accent-cyan);
            font-family: monospace;
            min-width: 120px;
        }}
        .io-desc {{
            color: var(--text-muted);
        }}
        .script-features {{
            margin-bottom: 10px;
        }}
        .feature-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .feature-list li {{
            font-size: 12px;
            color: var(--text-muted);
            padding: 3px 0;
            padding-left: 16px;
            position: relative;
        }}
        .feature-list li::before {{
            content: '•';
            position: absolute;
            left: 0;
            color: var(--accent-green);
        }}
        .script-doc-card .script-block {{
            margin-top: 10px;
            margin-bottom: 0;
            font-size: 11px;
        }}

        /* Subagent config */
        .subagent-config {{
            background: linear-gradient(135deg, rgba(163, 113, 247, 0.1) 0%, rgba(163, 113, 247, 0.05) 100%);
            border: 1px solid rgba(163, 113, 247, 0.3);
            border-radius: 8px;
            padding: 16px;
        }}
        .subagent-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 12px;
        }}
        .subagent-icon {{
            width: 32px;
            height: 32px;
            background: var(--accent-purple);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 16px;
        }}
        .subagent-title {{
            font-weight: 600;
        }}
        .subagent-type {{
            font-size: 12px;
            color: var(--text-muted);
        }}
        .subagent-grid {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 12px;
            margin-bottom: 16px;
        }}
        .subagent-stat {{
            background: var(--bg-tertiary);
            padding: 10px 12px;
            border-radius: 6px;
        }}
        .subagent-stat-label {{
            font-size: 10px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .subagent-stat-value {{
            font-size: 16px;
            font-weight: 600;
            color: var(--accent-purple);
        }}
        .concurrency-slots {{
            display: flex;
            gap: 4px;
            flex-wrap: wrap;
            margin-top: 8px;
        }}
        .concurrency-slot {{
            width: 20px;
            height: 20px;
            background: var(--bg-tertiary);
            border: 1px solid var(--accent-purple);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
            color: var(--accent-purple);
        }}

        /* Gate */
        .gate-config {{
            background: linear-gradient(135deg, rgba(210, 153, 34, 0.1) 0%, rgba(210, 153, 34, 0.05) 100%);
            border: 1px solid rgba(210, 153, 34, 0.3);
            border-radius: 8px;
            padding: 16px;
        }}
        .gate-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            margin-bottom: 16px;
        }}
        .gate-icon {{
            font-size: 24px;
        }}
        .gate-title {{
            font-weight: 600;
            color: var(--accent-orange);
        }}
        .gate-options {{
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .gate-option {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px;
            background: var(--bg-tertiary);
            border-radius: 6px;
        }}
        .gate-key {{
            width: 28px;
            height: 28px;
            background: var(--accent-orange);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: white;
            font-size: 12px;
        }}
        .gate-label {{
            flex: 1;
            font-size: 13px;
        }}
        .gate-target {{
            font-size: 11px;
            color: var(--text-muted);
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .gate-target::before {{
            content: '→';
            color: var(--accent-orange);
        }}

        /* Handoff */
        .handoff-box {{
            background: linear-gradient(135deg, rgba(248, 81, 73, 0.1) 0%, rgba(248, 81, 73, 0.05) 100%);
            border: 1px solid rgba(248, 81, 73, 0.3);
            border-radius: 8px;
            padding: 16px;
            display: flex;
            align-items: center;
            gap: 12px;
        }}
        .handoff-icon {{
            font-size: 20px;
        }}
        .handoff-content {{
            flex: 1;
        }}
        .handoff-label {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}
        .handoff-target {{
            font-weight: 600;
            color: var(--accent-red);
        }}

        /* Level indicator (for synthesis) */
        .level-indicator {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            background: var(--bg-tertiary);
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 600;
        }}
        .level-num {{
            width: 18px;
            height: 18px;
            background: var(--accent-blue);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 10px;
        }}
        .level-type {{
            color: var(--text-muted);
        }}
        .level-type.script {{ color: var(--accent-cyan); }}
        .level-type.subagent {{ color: var(--accent-purple); }}

        /* Grid for two columns */
        .two-col {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
        }}

        /* Token budget */
        .token-budget {{
            background: var(--bg-tertiary);
            border-radius: 8px;
            padding: 16px;
        }}
        .budget-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }}
        .budget-title {{
            font-weight: 600;
        }}
        .budget-total {{
            font-size: 14px;
            color: var(--text-muted);
        }}
        .budget-bar {{
            height: 8px;
            background: var(--bg-primary);
            border-radius: 4px;
            overflow: hidden;
            margin-bottom: 12px;
        }}
        .budget-fill {{
            height: 100%;
            background: linear-gradient(90deg, var(--accent-green) 0%, var(--accent-blue) 100%);
            border-radius: 4px;
        }}
        .budget-items {{
            display: flex;
            flex-direction: column;
            gap: 6px;
        }}
        .budget-item {{
            display: flex;
            justify-content: space-between;
            font-size: 12px;
        }}
        .budget-item-label {{
            color: var(--text-secondary);
        }}
        .budget-item-value {{
            font-family: 'SF Mono', monospace;
            color: var(--text-muted);
        }}

        /* Empty state */
        .empty {{
            text-align: center;
            padding: 60px 20px;
            color: var(--text-muted);
        }}
        .empty-icon {{
            font-size: 48px;
            margin-bottom: 16px;
            opacity: 0.5;
        }}

        /* Phase colors */
        .phase-A {{ background: var(--phase-a); }}
        .phase-B {{ background: var(--phase-b); }}
        .phase-C {{ background: var(--phase-c); }}
        .phase-D {{ background: var(--phase-d); }}
        .phase-E {{ background: var(--phase-e); }}
        .phase-F {{ background: var(--phase-f); }}
        .phase-G {{ background: var(--phase-g); }}
        .phase-H {{ background: var(--phase-h); }}
        .phase-I {{ background: var(--phase-i); }}

        /* Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
            height: 8px;
        }}
        ::-webkit-scrollbar-track {{
            background: var(--bg-primary);
        }}
        ::-webkit-scrollbar-thumb {{
            background: var(--bg-elevated);
            border-radius: 4px;
        }}
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--text-muted);
        }}
    </style>
</head>
<body>
    <div class="header">
        <div class="header-top">
            <h1>Research Pipeline Workflow</h1>
            <div class="header-actions">
                <button class="btn" onclick="expandAll()">Expand All</button>
                <button class="btn" onclick="collapseAll()">Collapse All</button>
            </div>
        </div>
        <div class="pipeline" id="pipeline"></div>
    </div>

    <div class="main">
        <div class="sidebar" id="sidebar"></div>
        <div class="content" id="content">
            <div class="empty">
                <div class="empty-icon">📋</div>
                <p>Select an orchestrator and step to see details</p>
            </div>
        </div>
    </div>

    <script>
    const DATA = {data_json};

    let currentOrchestrator = 0;
    let currentStep = null;

    // Render pipeline overview
    function renderPipeline() {{
        const container = document.getElementById('pipeline');
        let html = '';

        DATA.pipeline.forEach((orch, i) => {{
            if (i > 0) {{
                html += '<div class="pipeline-arrow"></div>';
            }}
            html += `
                <div class="pipeline-node ${{i === currentOrchestrator ? 'active' : ''}}"
                     onclick="selectOrchestrator(${{i}})">
                    <h3>${{orch.name}}</h3>
                    <div class="pipeline-stats">
                        <span class="pipeline-stat">${{orch.steps}} steps</span>
                        <span class="pipeline-stat">${{orch.phases}} phases</span>
                        <span class="pipeline-stat">${{orch.gates}} gates</span>
                    </div>
                </div>
            `;
        }});

        container.innerHTML = html;
    }}

    // Render sidebar
    function renderSidebar() {{
        const orch = DATA.orchestrators[currentOrchestrator];
        const container = document.getElementById('sidebar');
        let html = '';

        orch.phases.forEach(phase => {{
            html += `
                <div class="phase-group">
                    <div class="phase-header">
                        <span class="phase-badge phase-${{phase.letter}}">${{phase.letter}}</span>
                        ${{phase.name}}
                    </div>
            `;

            phase.steps.forEach(step => {{
                const badges = [];
                if (step.gate) badges.push('<span class="mini-badge gate">G</span>');
                if (step.subagent) badges.push('<span class="mini-badge subagent">S</span>');
                if (step.is_script) badges.push('<span class="mini-badge script">PY</span>');

                html += `
                    <div class="step-item ${{currentStep?.id === step.id ? 'active' : ''}}"
                         onclick="selectStep('${{step.id}}')">
                        <span class="step-num">${{step.number}}</span>
                        <span class="step-name">${{step.name}}</span>
                        <div class="step-badges">${{badges.join('')}}</div>
                    </div>
                `;
            }});

            html += '</div>';
        }});

        container.innerHTML = html;
    }}

    // Render step details
    function renderContent() {{
        if (!currentStep) {{
            document.getElementById('content').innerHTML = `
                <div class="empty">
                    <div class="empty-icon">📋</div>
                    <p>Select a step to see details</p>
                </div>
            `;
            return;
        }}

        const step = currentStep;
        const container = document.getElementById('content');
        let html = '';

        // Header
        html += `
            <div class="content-header">
                <h2>
                    Step ${{step.number}}: ${{step.name}}
                    ${{step.level ? `<span class="level-indicator"><span class="level-num">${{step.level}}</span><span class="level-type ${{step.is_script ? 'script' : 'subagent'}}">${{step.is_script ? 'Script' : 'Subagent'}}</span></span>` : ''}}
                </h2>
                <div class="phase-tag">Phase ${{step.phase}}: ${{step.phase_name}}</div>
                ${{step.description ? `<p class="desc">${{step.description}}</p>` : ''}}
            </div>
        `;

        // Sub-steps
        if (step.sub_steps && step.sub_steps.length > 0) {{
            html += `
                <div class="card">
                    <div class="card-header">
                        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M2 4a1 1 0 100-2 1 1 0 000 2zm3.75-1.5a.75.75 0 000 1.5h8.5a.75.75 0 000-1.5h-8.5zm0 5a.75.75 0 000 1.5h8.5a.75.75 0 000-1.5h-8.5zm0 5a.75.75 0 000 1.5h8.5a.75.75 0 000-1.5h-8.5zM3 8a1 1 0 11-2 0 1 1 0 012 0zm-1 6a1 1 0 100-2 1 1 0 000 2z"></path></svg>
                        Sub-steps (${{step.sub_steps.length}})
                    </div>
                    <div class="card-content">
                        ${{step.sub_steps.map(s => `
                            <div class="sub-step">
                                <span class="sub-step-num">${{s.number}}</span>
                                <span class="sub-step-name">${{s.name}}</span>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
        }}

        // Inputs/Outputs grid
        if ((step.inputs && step.inputs.length > 0) || (step.outputs && step.outputs.length > 0)) {{
            html += '<div class="two-col">';

            if (step.inputs && step.inputs.length > 0) {{
                html += `
                    <div class="card">
                        <div class="card-header">
                            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 110 16A8 8 0 018 0zM1.5 8a6.5 6.5 0 1013 0 6.5 6.5 0 00-13 0zm4.879-2.773l4.264 2.559a.25.25 0 010 .428l-4.264 2.559A.25.25 0 016 10.559V5.442a.25.25 0 01.379-.215z"></path></svg>
                            Inputs (${{step.inputs.length}})
                        </div>
                        <div class="card-content">
                            ${{step.inputs.map(f => `
                                <div class="file-item">
                                    <span class="file-icon input">→</span>
                                    <span class="file-path">${{f.path}}</span>
                                    <span class="file-format">${{f.format}}</span>
                                </div>
                            `).join('')}}
                        </div>
                    </div>
                `;
            }}

            if (step.outputs && step.outputs.length > 0) {{
                html += `
                    <div class="card">
                        <div class="card-header">
                            <svg viewBox="0 0 16 16" fill="currentColor"><path d="M3.5 1.75v11.5c0 .09.048.173.126.217a.75.75 0 01-.752 1.298A1.75 1.75 0 012 13.25V1.75C2 .784 2.784 0 3.75 0h5.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v8.086a1.75 1.75 0 01-1.75 1.75h-.25a.75.75 0 010-1.5h.25a.25.25 0 00.25-.25V6h-2.75A1.75 1.75 0 018 4.25V1.5H3.75a.25.25 0 00-.25.25z"></path></svg>
                            Outputs (${{step.outputs.length}})
                        </div>
                        <div class="card-content">
                            ${{step.outputs.map(f => {{
                                // Find matching output doc
                                const doc = step.output_docs && step.output_docs.find(d => d.path === f.path);
                                if (doc && doc.description) {{
                                    return `
                                        <div class="output-doc-card">
                                            <div class="file-item">
                                                <span class="file-icon output">✓</span>
                                                <span class="file-path">${{f.path}}</span>
                                                <span class="file-format">${{f.format}}</span>
                                            </div>
                                            <div class="output-description">${{doc.description}}</div>
                                            ${{doc.created_by ? `<div class="output-created-by">Created by: <span>${{doc.created_by}}</span></div>` : ''}}
                                            ${{doc.contains && doc.contains.length > 0 ? `
                                                <div class="output-contains">
                                                    <span class="contains-label">Contains:</span>
                                                    <ul class="contains-list">
                                                        ${{doc.contains.map(c => `<li>${{c}}</li>`).join('')}}
                                                    </ul>
                                                </div>
                                            ` : ''}}
                                        </div>
                                    `;
                                }} else {{
                                    return `
                                        <div class="file-item">
                                            <span class="file-icon output">✓</span>
                                            <span class="file-path">${{f.path}}</span>
                                            <span class="file-format">${{f.format}}</span>
                                        </div>
                                    `;
                                }}
                            }}).join('')}}
                        </div>
                    </div>
                `;
            }}

            html += '</div>';
        }}

        // Scripts with documentation
        if (step.scripts && step.scripts.length > 0) {{
            html += `
                <div class="card">
                    <div class="card-header">
                        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.72 3.22a.75.75 0 011.06 1.06L2.06 8l3.72 3.72a.75.75 0 11-1.06 1.06L.47 8.53a.75.75 0 010-1.06l4.25-4.25zm6.56 0a.75.75 0 10-1.06 1.06L13.94 8l-3.72 3.72a.75.75 0 101.06 1.06l4.25-4.25a.75.75 0 000-1.06l-4.25-4.25z"></path></svg>
                        Scripts / Commands (${{step.scripts.length}})
                    </div>
                    <div class="card-content">
                        ${{step.scripts.map((s, i) => {{
                            const doc = step.script_docs && step.script_docs[i];
                            if (doc) {{
                                return `
                                    <div class="script-doc-card">
                                        <div class="script-doc-header">
                                            <span class="script-icon">⚙️</span>
                                            <span class="script-name">${{doc.name}}</span>
                                            ${{doc.level ? `<span class="script-level">Level ${{doc.level}}</span>` : ''}}
                                        </div>
                                        <div class="script-purpose">${{doc.purpose}}</div>
                                        ${{doc.description ? `<div class="script-description">${{doc.description}}</div>` : ''}}
                                        ${{doc.inputs && doc.inputs.length > 0 ? `
                                            <div class="script-io">
                                                <div class="script-io-header">📥 Inputs:</div>
                                                ${{doc.inputs.map(inp => `
                                                    <div class="script-io-item">
                                                        <span class="io-name">${{inp.name}}</span>
                                                        <span class="io-desc">${{inp.description}}</span>
                                                    </div>
                                                `).join('')}}
                                            </div>
                                        ` : ''}}
                                        ${{doc.outputs && doc.outputs.length > 0 ? `
                                            <div class="script-io">
                                                <div class="script-io-header">📤 Outputs:</div>
                                                ${{doc.outputs.map(out => `
                                                    <div class="script-io-item">
                                                        <span class="io-name">${{out.name}}</span>
                                                        <span class="io-desc">${{out.description}}</span>
                                                    </div>
                                                `).join('')}}
                                            </div>
                                        ` : ''}}
                                        ${{doc.key_features && doc.key_features.length > 0 ? `
                                            <div class="script-features">
                                                <div class="script-io-header">✨ Key Features:</div>
                                                <ul class="feature-list">
                                                    ${{doc.key_features.map(f => `<li>${{f}}</li>`).join('')}}
                                                </ul>
                                            </div>
                                        ` : ''}}
                                        <div class="script-block">${{s}}</div>
                                    </div>
                                `;
                            }} else {{
                                return `<div class="script-block">${{s}}</div>`;
                            }}
                        }}).join('')}}
                    </div>
                </div>
            `;
        }}

        // Subagent config
        if (step.subagent) {{
            const sa = step.subagent;
            html += `
                <div class="card">
                    <div class="card-header">
                        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8.878.392a1.75 1.75 0 00-1.756 0l-5.25 3.045A1.75 1.75 0 001 4.951v6.098c0 .624.332 1.2.872 1.514l5.25 3.045a1.75 1.75 0 001.756 0l5.25-3.045c.54-.313.872-.89.872-1.514V4.951c0-.624-.332-1.2-.872-1.514L8.878.392z"></path></svg>
                        Subagent Spawn
                    </div>
                    <div class="card-content">
                        <div class="subagent-config">
                            <div class="subagent-header">
                                <div class="subagent-icon">🤖</div>
                                <div>
                                    <div class="subagent-title">Parallel Subagents</div>
                                    <div class="subagent-type">${{sa.type}}</div>
                                </div>
                            </div>
                            <div class="subagent-grid">
                                <div class="subagent-stat">
                                    <div class="subagent-stat-label">Concurrency</div>
                                    <div class="subagent-stat-value">${{sa.concurrency}}</div>
                                </div>
                                <div class="subagent-stat">
                                    <div class="subagent-stat-label">Timeout</div>
                                    <div class="subagent-stat-value">${{sa.timeout}}</div>
                                </div>
                                <div class="subagent-stat">
                                    <div class="subagent-stat-label">Retry</div>
                                    <div class="subagent-stat-value">${{sa.retry}}</div>
                                </div>
                            </div>
                            <div class="concurrency-slots">
                                ${{Array(Math.min(sa.concurrency, 15)).fill(0).map((_, i) => `<div class="concurrency-slot">▶</div>`).join('')}}
                            </div>
                        </div>
                    </div>
                </div>
            `;

            // Input contract
            if (sa.input_contract && sa.input_contract.length > 0) {{
                html += `
                    <div class="card">
                        <div class="card-header">INPUT CONTRACT</div>
                        <div class="card-content">
                            ${{sa.input_contract.map(f => `
                                <div class="file-item">
                                    <span class="file-icon input">→</span>
                                    <span class="file-path">${{f}}</span>
                                </div>
                            `).join('')}}
                        </div>
                    </div>
                `;
            }}
        }}

        // Gate
        if (step.gate) {{
            const gate = step.gate;
            html += `
                <div class="card">
                    <div class="card-header" style="color: var(--accent-orange)">
                        <svg viewBox="0 0 16 16" fill="currentColor"><path d="M9.585.52a2.678 2.678 0 00-3.17 0l-.928.68a1.178 1.178 0 01-.518.215L3.83 1.59a2.678 2.678 0 00-2.24 2.24l-.175 1.14a1.178 1.178 0 01-.215.518l-.68.928a2.678 2.678 0 000 3.17l.68.928c.113.153.186.33.215.518l.175 1.138a2.678 2.678 0 002.24 2.24l1.138.175c.187.029.365.102.518.215l.928.68a2.678 2.678 0 003.17 0l.928-.68a1.17 1.17 0 01.518-.215l1.138-.175a2.678 2.678 0 002.241-2.241l.175-1.138c.029-.187.102-.365.215-.518l.68-.928a2.678 2.678 0 000-3.17l-.68-.928a1.179 1.179 0 01-.215-.518L14.41 3.83a2.678 2.678 0 00-2.24-2.24l-1.138-.175a1.179 1.179 0 01-.518-.215L9.585.52z"></path></svg>
                        User Decision Gate
                    </div>
                    <div class="card-content">
                        <div class="gate-config">
                            <div class="gate-header">
                                <span class="gate-icon">🚪</span>
                                <span class="gate-title">${{gate.name}}</span>
                            </div>
                            <div class="gate-options">
                                ${{gate.options.map(opt => `
                                    <div class="gate-option">
                                        <span class="gate-key">${{opt.key}}</span>
                                        <span class="gate-label">${{opt.label}}</span>
                                        ${{opt.target ? `<span class="gate-target">${{opt.target}}</span>` : ''}}
                                    </div>
                                `).join('')}}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }}

        // Handoff
        if (step.handoff_to) {{
            html += `
                <div class="handoff-box">
                    <span class="handoff-icon">➡️</span>
                    <div class="handoff-content">
                        <div class="handoff-label">Hands off to</div>
                        <div class="handoff-target">${{step.handoff_to}}</div>
                    </div>
                </div>
            `;
        }}

        container.innerHTML = html;
    }}

    // Event handlers
    function selectOrchestrator(index) {{
        currentOrchestrator = index;
        currentStep = null;
        renderPipeline();
        renderSidebar();
        renderContent();
    }}

    function selectStep(stepId) {{
        const orch = DATA.orchestrators[currentOrchestrator];
        for (const phase of orch.phases) {{
            for (const step of phase.steps) {{
                if (step.id === stepId) {{
                    currentStep = step;
                    break;
                }}
            }}
        }}
        renderSidebar();
        renderContent();
    }}

    function expandAll() {{
        // Future: implement expand/collapse
    }}

    function collapseAll() {{
        // Future: implement expand/collapse
    }}

    // Initial render
    renderPipeline();

    // Auto-select first orchestrator and step
    if (DATA.orchestrators.length > 0) {{
        currentOrchestrator = 0;
        const orch = DATA.orchestrators[0];
        if (orch.phases.length > 0 && orch.phases[0].steps.length > 0) {{
            currentStep = orch.phases[0].steps[0];
        }}
        renderSidebar();
        renderContent();
    }}
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

    # Find all orchestrator SKILL.md files
    skill_files = list(pipeline_dir.glob("*/SKILL.md"))

    if not skill_files:
        print(f"Error: No SKILL.md files found in {pipeline_dir}", file=sys.stderr)
        sys.exit(1)

    # Define pipeline order: create -> analyze -> synthesize
    PIPELINE_ORDER = {
        'create-research-project': 0,
        'analyze-research-project': 1,
        'synthesize-research-project': 2,
    }

    # Sort by pipeline order, unknown names go last
    skill_files.sort(key=lambda p: PIPELINE_ORDER.get(p.parent.name, 99))

    print(f"Found {len(skill_files)} orchestrators:")

    orchestrators = []
    for skill_file in skill_files:
        print(f"  Parsing: {skill_file.parent.name}")
        content = skill_file.read_text(encoding='utf-8')
        orch = parse_skill_md(content, skill_file)
        orchestrators.append(orch)
        print(f"    - {orch.total_steps} steps, {len(orch.phases)} phases, {orch.total_gates} gates")

    # Build file dependency graph
    file_graph = build_file_graph(orchestrators)
    print(f"\nFile graph: {len(file_graph['nodes'])} files, {len(file_graph['edges'])} edges")

    # Generate HTML
    html = generate_html(orchestrators, file_graph)

    output_path = pipeline_dir.parent / "research_pipeline_flow.html"
    output_path.write_text(html, encoding='utf-8')
    print(f"\nGenerated: {output_path}")

if __name__ == "__main__":
    main()

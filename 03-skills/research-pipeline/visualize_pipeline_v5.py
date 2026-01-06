#!/usr/bin/env python3
"""
Research Pipeline Visualizer v5 - Endless Scroll Edition
Generates an interactive HTML visualization with:
- Sticky sidebar navigation
- Endless scroll through all orchestrators/phases/steps
- Scroll-spy highlighting current section
- Beautiful pipeline flow diagram
- Full script and output documentation
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
    SCRIPT_REGISTRY = {}
    OUTPUT_FILES = {}
    def get_script_doc(name): return None

# ============================================================================
# DATA CLASSES (same as v4)
# ============================================================================

@dataclass
class FileRef:
    path: str
    type: str
    format: str = ""

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

@dataclass
class ScriptInfo:
    name: str
    purpose: str = ""
    description: str = ""
    level: Optional[int] = None
    inputs: List[Dict[str, str]] = field(default_factory=list)
    outputs: List[Dict[str, str]] = field(default_factory=list)
    key_features: List[str] = field(default_factory=list)

@dataclass
class OutputFileInfo:
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
    script_docs: List[ScriptInfo] = field(default_factory=list)
    output_docs: List[OutputFileInfo] = field(default_factory=list)
    skills_used: List[str] = field(default_factory=list)
    subagent: Optional[SubagentConfig] = None
    gate: Optional[Gate] = None
    handoff_to: Optional[str] = None
    is_script: bool = False
    level: Optional[int] = None
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
# PARSING (same as v4)
# ============================================================================

def get_file_format(path: str) -> str:
    if '.md' in path: return 'md'
    if '.yaml' in path or '.yml' in path: return 'yaml'
    if '.json' in path: return 'json'
    if '.py' in path: return 'py'
    return 'unknown'

def parse_subagent_config(content: str) -> Optional[SubagentConfig]:
    has_task_spawn = bool(re.search(r'Task\s*\(\s*\n?\s*subagent_type', content))
    has_spawn_instruction = bool(re.search(r'[Ss]pawn\s+(?:subagent|batch|extraction|final)', content))
    is_just_reference = bool(re.search(r'(?:subagent\s+(?:reads|output|prompt)|for\s+subagents)', content, re.IGNORECASE))

    if not (has_task_spawn or has_spawn_instruction) or is_just_reference:
        return None

    config = SubagentConfig()

    type_match = re.search(r'subagent_type\s*=\s*["\']([^"\']+)["\']', content)
    if type_match:
        config.type = type_match.group(1)

    conc_match = re.search(r'(?:max|concurrency|parallel)\s*[=:]\s*(\d+)', content, re.IGNORECASE)
    if conc_match:
        config.concurrency = int(conc_match.group(1))

    timeout_match = re.search(r'timeout\s*[=:]\s*["\']?(\d+\s*(?:min|sec|hour)[s]?)["\']?', content, re.IGNORECASE)
    if timeout_match:
        config.timeout = timeout_match.group(1)

    retry_match = re.search(r'retry\s*[=:]\s*(\d+)', content, re.IGNORECASE)
    if retry_match:
        config.retry = int(retry_match.group(1))

    contract_match = re.search(r'INPUT CONTRACT:?\s*\n((?:[-•*]\s*.+\n?)+)', content, re.IGNORECASE)
    if contract_match:
        contract_lines = re.findall(r'[-•*]\s*(.+)', contract_match.group(1))
        config.input_contract = [l.strip() for l in contract_lines if l.strip()][:5]

    return config

def parse_gate(step_name: str, content: str) -> Optional[Gate]:
    if not re.search(r'(?:gate|decision|approval|user\s+confirms?)', step_name + content, re.IGNORECASE):
        return None

    gate = Gate(name=step_name)

    option_patterns = [
        (r'\[Y\][:\s]*([^\n\[]+)', 'Y'),
        (r'\[N\][:\s]*([^\n\[]+)', 'N'),
        (r'\[S\][:\s]*([^\n\[]+)', 'S'),
    ]

    for pattern, key in option_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            gate.options.append(GateOption(key=key, label=match.group(1).strip()[:50]))

    return gate if gate.options else None

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
            orch.description = desc_match.group(1).strip()[:200]

    # Extract handoff info
    handoff_from = re.search(r'[Rr]eceives?\s+from[:\s]+[`"]?([^`"\n]+)', content)
    handoff_to = re.search(r'[Hh]ands?\s+off\s+to[:\s]+[`"]?([^`"\n]+)', content)
    if handoff_from:
        orch.handoff_from = handoff_from.group(1).strip()
    if handoff_to:
        orch.handoff_to = handoff_to.group(1).strip()

    phases = {}

    # Phases use # PHASE A: format (single #)
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

        # Get step content (until next step or end)
        start = match.end()
        end = step_matches[i + 1].start() if i + 1 < len(step_matches) else len(content)
        step_content = content[start:end]

        # Get phase
        phase_letter, phase_name = get_phase_at_pos(match.start())

        if phase_letter not in phases:
            phases[phase_letter] = Phase(letter=phase_letter, name=phase_name)

        phase_name = phases[phase_letter].name

        desc_lines = []
        for line in step_content.split('\n')[:5]:
            line = line.strip()
            if line and not line.startswith(('#', '-', '*', '`', '|', '>')):
                desc_lines.append(line)
        desc = ' '.join(desc_lines)[:300] if desc_lines else ""

        sub_steps = []
        substep_pattern = re.compile(r'^####?\s+(\d+\.\d+)[.:\s]+(.+?)$', re.MULTILINE)
        for sm in substep_pattern.finditer(step_content):
            sub_steps.append(SubStep(number=sm.group(1), name=sm.group(2).strip()[:100]))

        inputs = []
        input_patterns = [
            r'INPUT[S]?:\s*\n((?:[-•*]\s*.+\n?)+)',
            r'Read[s]?:\s*`([^`]+)`',
            r'Load[s]?:\s*`([^`]+)`',
        ]
        for pattern in input_patterns:
            for m in re.finditer(pattern, step_content, re.IGNORECASE):
                if '\n' in m.group(0):
                    paths = re.findall(r'[-•*]\s*`?([^`\n]+)`?', m.group(1))
                    for path in paths:
                        path = path.strip()
                        if path and '/' in path or path.endswith(('.md', '.yaml', '.json')):
                            if not any(i.path == path for i in inputs):
                                inputs.append(FileRef(path=path, type="input", format=get_file_format(path)))
                else:
                    path = m.group(1).strip()
                    if path and not any(i.path == path for i in inputs):
                        inputs.append(FileRef(path=path, type="input", format=get_file_format(path)))

        outputs = []
        output_patterns = [
            r'OUTPUT[S]?:\s*\n((?:[-•*]\s*.+\n?)+)',
            r'Write[s]?:\s*`([^`]+)`',
            r'Create[s]?:\s*`([^`]+)`',
            r'Produce[s]?:\s*`([^`]+)`',
        ]
        for pattern in output_patterns:
            for m in re.finditer(pattern, step_content, re.IGNORECASE):
                if '\n' in m.group(0):
                    paths = re.findall(r'[-•*]\s*`?([^`\n]+)`?', m.group(1))
                    for path in paths:
                        path = path.strip()
                        if path and '/' in path or path.endswith(('.md', '.yaml', '.json')):
                            if not any(o.path == path for o in outputs):
                                outputs.append(FileRef(path=path, type="output", format=get_file_format(path)))
                else:
                    path = m.group(1).strip()
                    if path and not any(o.path == path for o in outputs):
                        outputs.append(FileRef(path=path, type="output", format=get_file_format(path)))

        scripts = []
        script_docs = []
        script_blocks = re.findall(r'```(?:bash|python|sh)\n(.*?)```', step_content, re.DOTALL)
        for block in script_blocks:
            lines = [l.strip() for l in block.strip().split('\n') if l.strip() and not l.strip().startswith('#')]
            if lines:
                cmd = lines[0][:100]
                if cmd and cmd not in scripts:
                    scripts.append(cmd)
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

        output_docs = []
        if OUTPUT_FILES:
            for out in outputs:
                filename = out.path.split('/')[-1] if '/' in out.path else out.path
                for pattern, doc in OUTPUT_FILES.items():
                    pattern_regex = pattern.replace('{field}', r'\w+').replace('{N}', r'\d+')
                    if re.match(pattern_regex, filename) or filename == pattern:
                        output_docs.append(OutputFileInfo(
                            path=out.path,
                            description=doc.get('description', ''),
                            created_by=doc.get('created_by', ''),
                            contains=doc.get('contains', [])[:5]
                        ))
                        break

        is_script = bool(re.search(r'(?:Script|SCRIPT|python\s+\w+\.py|deterministic)', step_content))

        level = None
        level_match = re.search(r'[Ll]evel\s+(\d+)', step_name) or re.search(r'[Ll]evel\s+(\d+)', step_content[:200])
        if level_match:
            level = int(level_match.group(1))

        subagent = parse_subagent_config(step_content)
        gate = parse_gate(step_name, step_content)
        if gate:
            orch.total_gates += 1

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

    handoff_match = re.search(r'handoff\s+to[:\s]+([a-z-]+)', content, re.IGNORECASE)
    if handoff_match:
        orch.handoff_to = handoff_match.group(1)

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
# HTML GENERATION - v5 ENDLESS SCROLL EDITION
# ============================================================================

def serialize_orchestrator(orch: Orchestrator) -> dict:
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
    """Generate endless scroll HTML with sticky sidebar navigation."""

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
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Pipeline - Endless Scroll Visualization</title>
    <style>
        :root {{
            --bg-primary: #0a0c10;
            --bg-secondary: #12161e;
            --bg-tertiary: #1a1f2e;
            --bg-elevated: #242a3a;
            --bg-card: #161b26;
            --border: #2d3548;
            --border-subtle: #232838;
            --text-primary: #e8ecf4;
            --text-secondary: #9aa5bb;
            --text-muted: #5d6a82;
            --accent-blue: #4dabf5;
            --accent-green: #4ade80;
            --accent-purple: #a78bfa;
            --accent-orange: #fb923c;
            --accent-red: #f87171;
            --accent-pink: #f472b6;
            --accent-cyan: #22d3ee;
            --accent-yellow: #facc15;
            --glow-blue: rgba(77, 171, 245, 0.15);
            --glow-purple: rgba(167, 139, 250, 0.15);
            --glow-green: rgba(74, 222, 128, 0.15);
            --phase-a: #22c55e;
            --phase-b: #3b82f6;
            --phase-c: #f59e0b;
            --phase-d: #a855f7;
            --phase-e: #ec4899;
            --phase-f: #14b8a6;
            --phase-g: #6366f1;
            --phase-h: #f97316;
            --phase-i: #8b5cf6;
            --sidebar-width: 320px;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        html {{
            scroll-behavior: smooth;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
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
            overflow-y: auto;
            z-index: 100;
            display: flex;
            flex-direction: column;
        }}

        .sidebar-header {{
            padding: 24px;
            border-bottom: 1px solid var(--border);
            background: linear-gradient(135deg, var(--bg-tertiary) 0%, var(--bg-secondary) 100%);
        }}

        .logo {{
            font-size: 20px;
            font-weight: 700;
            background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 4px;
        }}

        .logo-sub {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 1px;
        }}

        .nav {{
            flex: 1;
            overflow-y: auto;
            padding: 16px 0;
        }}

        .nav-section {{
            margin-bottom: 8px;
        }}

        .nav-section-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 20px;
            cursor: pointer;
            transition: all 0.2s;
            border-left: 3px solid transparent;
        }}

        .nav-section-header:hover {{
            background: var(--bg-tertiary);
        }}

        .nav-section-header.active {{
            background: var(--glow-blue);
            border-left-color: var(--accent-blue);
        }}

        .nav-section-icon {{
            width: 32px;
            height: 32px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            flex-shrink: 0;
        }}

        .nav-section-icon.create {{ background: linear-gradient(135deg, var(--phase-a) 0%, #16a34a 100%); }}
        .nav-section-icon.analyze {{ background: linear-gradient(135deg, var(--phase-b) 0%, #2563eb 100%); }}
        .nav-section-icon.synthesize {{ background: linear-gradient(135deg, var(--phase-d) 0%, #7c3aed 100%); }}

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

        .nav-section-stats {{
            font-size: 11px;
            color: var(--text-muted);
        }}

        .nav-items {{
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.3s ease;
        }}

        .nav-section.expanded .nav-items {{
            max-height: 2000px;
        }}

        .nav-phase {{
            padding: 8px 20px 8px 56px;
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .nav-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 8px 20px 8px 56px;
            cursor: pointer;
            transition: all 0.15s;
            border-left: 3px solid transparent;
            font-size: 13px;
            color: var(--text-secondary);
        }}

        .nav-item:hover {{
            background: var(--bg-tertiary);
            color: var(--text-primary);
        }}

        .nav-item.active {{
            background: rgba(77, 171, 245, 0.1);
            border-left-color: var(--accent-cyan);
            color: var(--accent-cyan);
        }}

        .nav-item-number {{
            font-size: 11px;
            font-weight: 600;
            color: var(--text-muted);
            min-width: 28px;
        }}

        .nav-item-name {{
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}

        .nav-item-badge {{
            font-size: 9px;
            padding: 2px 6px;
            border-radius: 10px;
            font-weight: 600;
        }}

        .nav-item-badge.gate {{
            background: var(--accent-orange);
            color: #000;
        }}

        .nav-item-badge.subagent {{
            background: var(--accent-purple);
            color: #fff;
        }}

        .nav-item-badge.script {{
            background: var(--accent-cyan);
            color: #000;
        }}

        /* ===== MAIN CONTENT ===== */
        .main {{
            flex: 1;
            margin-left: var(--sidebar-width);
            min-height: 100vh;
        }}

        /* ===== HERO / DIAGRAM ===== */
        .hero {{
            background: linear-gradient(180deg, var(--bg-tertiary) 0%, var(--bg-primary) 100%);
            padding: 60px 48px;
            border-bottom: 1px solid var(--border);
        }}

        .hero-title {{
            font-size: 36px;
            font-weight: 700;
            margin-bottom: 12px;
            background: linear-gradient(135deg, var(--accent-cyan) 0%, var(--accent-blue) 50%, var(--accent-purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .hero-subtitle {{
            font-size: 16px;
            color: var(--text-secondary);
            margin-bottom: 40px;
        }}

        /* Pipeline Flow Diagram */
        .pipeline-diagram {{
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0;
            padding: 32px 0;
        }}

        .pipeline-node {{
            background: var(--bg-card);
            border: 2px solid var(--border);
            border-radius: 16px;
            padding: 24px 32px;
            min-width: 240px;
            text-align: center;
            position: relative;
            transition: all 0.3s ease;
            cursor: pointer;
        }}

        .pipeline-node:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.4);
        }}

        .pipeline-node.create {{
            border-color: var(--phase-a);
            box-shadow: 0 0 30px var(--glow-green);
        }}
        .pipeline-node.create:hover {{ box-shadow: 0 0 50px var(--glow-green); }}

        .pipeline-node.analyze {{
            border-color: var(--phase-b);
            box-shadow: 0 0 30px var(--glow-blue);
        }}
        .pipeline-node.analyze:hover {{ box-shadow: 0 0 50px var(--glow-blue); }}

        .pipeline-node.synthesize {{
            border-color: var(--phase-d);
            box-shadow: 0 0 30px var(--glow-purple);
        }}
        .pipeline-node.synthesize:hover {{ box-shadow: 0 0 50px var(--glow-purple); }}

        .pipeline-node-icon {{
            font-size: 32px;
            margin-bottom: 12px;
        }}

        .pipeline-node-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
        }}

        .pipeline-node-stats {{
            display: flex;
            justify-content: center;
            gap: 16px;
            font-size: 12px;
            color: var(--text-muted);
        }}

        .pipeline-node-stat {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}

        .pipeline-arrow {{
            display: flex;
            align-items: center;
            padding: 0 8px;
        }}

        .pipeline-arrow svg {{
            width: 48px;
            height: 24px;
            fill: var(--text-muted);
        }}

        /* ===== SECTIONS (Endless Scroll) ===== */
        .section {{
            padding: 48px;
            border-bottom: 1px solid var(--border);
            scroll-margin-top: 20px;
        }}

        .section-header {{
            display: flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 32px;
            padding-bottom: 20px;
            border-bottom: 1px solid var(--border-subtle);
        }}

        .section-icon {{
            width: 48px;
            height: 48px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
        }}

        .section-icon.create {{ background: linear-gradient(135deg, var(--phase-a) 0%, #16a34a 100%); }}
        .section-icon.analyze {{ background: linear-gradient(135deg, var(--phase-b) 0%, #2563eb 100%); }}
        .section-icon.synthesize {{ background: linear-gradient(135deg, var(--phase-d) 0%, #7c3aed 100%); }}

        .section-info h2 {{
            font-size: 24px;
            font-weight: 700;
            margin-bottom: 4px;
        }}

        .section-info p {{
            color: var(--text-secondary);
            font-size: 14px;
        }}

        /* Phase Headers */
        .phase-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 16px 20px;
            background: var(--bg-tertiary);
            border-radius: 12px;
            margin-bottom: 16px;
            margin-top: 32px;
        }}

        .phase-header:first-of-type {{
            margin-top: 0;
        }}

        .phase-letter {{
            width: 36px;
            height: 36px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 16px;
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

        .phase-name {{
            font-size: 16px;
            font-weight: 600;
        }}

        /* Step Cards */
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
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }}

        .step-card-header {{
            display: flex;
            align-items: flex-start;
            gap: 16px;
            padding: 20px 24px;
            cursor: pointer;
        }}

        .step-number {{
            background: var(--bg-elevated);
            border-radius: 8px;
            padding: 8px 12px;
            font-size: 14px;
            font-weight: 700;
            color: var(--accent-cyan);
            flex-shrink: 0;
        }}

        .step-info {{
            flex: 1;
        }}

        .step-title {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
        }}

        .step-description {{
            font-size: 13px;
            color: var(--text-secondary);
            line-height: 1.5;
        }}

        .step-badges {{
            display: flex;
            gap: 8px;
            flex-shrink: 0;
        }}

        .step-badge {{
            font-size: 10px;
            padding: 4px 10px;
            border-radius: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }}

        .step-badge.gate {{
            background: rgba(251, 146, 60, 0.2);
            color: var(--accent-orange);
            border: 1px solid rgba(251, 146, 60, 0.3);
        }}

        .step-badge.subagent {{
            background: rgba(167, 139, 250, 0.2);
            color: var(--accent-purple);
            border: 1px solid rgba(167, 139, 250, 0.3);
        }}

        .step-badge.script {{
            background: rgba(34, 211, 238, 0.2);
            color: var(--accent-cyan);
            border: 1px solid rgba(34, 211, 238, 0.3);
        }}

        .step-badge.level {{
            background: rgba(250, 204, 21, 0.2);
            color: var(--accent-yellow);
            border: 1px solid rgba(250, 204, 21, 0.3);
        }}

        .step-content {{
            padding: 0 24px 24px;
            display: none;
        }}

        .step-card.expanded .step-content {{
            display: block;
        }}

        .step-expand-icon {{
            color: var(--text-muted);
            transition: transform 0.2s;
        }}

        .step-card.expanded .step-expand-icon {{
            transform: rotate(180deg);
        }}

        /* Content Cards */
        .content-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 16px;
            margin-top: 16px;
        }}

        .content-card {{
            background: var(--bg-tertiary);
            border: 1px solid var(--border-subtle);
            border-radius: 12px;
            overflow: hidden;
        }}

        .content-card-header {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 14px 16px;
            background: var(--bg-elevated);
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-secondary);
        }}

        .content-card-header svg {{
            width: 16px;
            height: 16px;
            fill: currentColor;
        }}

        .content-card-body {{
            padding: 16px;
        }}

        /* File Items */
        .file-item {{
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 10px 12px;
            background: var(--bg-primary);
            border-radius: 8px;
            margin-bottom: 8px;
            font-size: 12px;
            font-family: 'JetBrains Mono', 'Fira Code', monospace;
        }}

        .file-item:last-child {{ margin-bottom: 0; }}

        .file-icon {{
            width: 20px;
            height: 20px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            flex-shrink: 0;
        }}

        .file-icon.input {{ color: var(--accent-blue); }}
        .file-icon.output {{ color: var(--accent-green); }}

        .file-path {{
            flex: 1;
            color: var(--text-secondary);
            word-break: break-all;
        }}

        .file-format {{
            font-size: 10px;
            padding: 2px 8px;
            background: var(--bg-elevated);
            border-radius: 4px;
            color: var(--text-muted);
        }}

        /* Script Documentation */
        .script-doc {{
            background: linear-gradient(135deg, rgba(34, 211, 238, 0.08) 0%, rgba(34, 211, 238, 0.02) 100%);
            border: 1px solid rgba(34, 211, 238, 0.2);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 16px;
        }}

        .script-doc:last-child {{ margin-bottom: 0; }}

        .script-doc-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}

        .script-doc-icon {{
            font-size: 24px;
        }}

        .script-doc-name {{
            font-size: 15px;
            font-weight: 600;
            color: var(--accent-cyan);
        }}

        .script-doc-level {{
            margin-left: auto;
            background: var(--accent-orange);
            color: #000;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 11px;
            font-weight: 700;
        }}

        .script-doc-purpose {{
            font-size: 14px;
            color: var(--text-secondary);
            margin-bottom: 12px;
            font-weight: 500;
        }}

        .script-doc-description {{
            font-size: 13px;
            color: var(--text-muted);
            line-height: 1.6;
            padding: 12px;
            background: rgba(0,0,0,0.3);
            border-radius: 8px;
            margin-bottom: 16px;
        }}

        .script-io-section {{
            margin-bottom: 12px;
        }}

        .script-io-title {{
            font-size: 12px;
            font-weight: 600;
            color: var(--text-secondary);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .script-io-item {{
            display: flex;
            gap: 12px;
            padding: 8px 0;
            font-size: 12px;
            border-bottom: 1px solid rgba(255,255,255,0.05);
        }}

        .script-io-item:last-child {{ border-bottom: none; }}

        .script-io-name {{
            color: var(--accent-cyan);
            font-family: monospace;
            min-width: 140px;
            flex-shrink: 0;
        }}

        .script-io-desc {{
            color: var(--text-muted);
        }}

        .script-features {{
            margin-top: 12px;
        }}

        .script-features ul {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}

        .script-features li {{
            font-size: 12px;
            color: var(--text-muted);
            padding: 4px 0 4px 20px;
            position: relative;
        }}

        .script-features li::before {{
            content: '✓';
            position: absolute;
            left: 0;
            color: var(--accent-green);
            font-weight: bold;
        }}

        .script-command {{
            background: var(--bg-primary);
            border-radius: 8px;
            padding: 12px;
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            color: var(--accent-cyan);
            margin-top: 12px;
            border-left: 3px solid var(--accent-cyan);
        }}

        .script-command::before {{
            content: '$ ';
            color: var(--text-muted);
        }}

        /* Subagent Config */
        .subagent-config {{
            background: linear-gradient(135deg, rgba(167, 139, 250, 0.1) 0%, rgba(167, 139, 250, 0.03) 100%);
            border: 1px solid rgba(167, 139, 250, 0.25);
            border-radius: 12px;
            padding: 20px;
        }}

        .subagent-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
        }}

        .subagent-icon {{
            width: 40px;
            height: 40px;
            background: var(--accent-purple);
            border-radius: 10px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 20px;
        }}

        .subagent-title {{
            font-size: 16px;
            font-weight: 600;
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
            border-radius: 8px;
            padding: 12px;
            text-align: center;
        }}

        .subagent-stat-value {{
            font-size: 20px;
            font-weight: 700;
            color: var(--accent-purple);
        }}

        .subagent-stat-label {{
            font-size: 11px;
            color: var(--text-muted);
            text-transform: uppercase;
        }}

        .subagent-slots {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}

        .subagent-slot {{
            width: 28px;
            height: 28px;
            background: var(--accent-purple);
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            color: #fff;
        }}

        /* Gate */
        .gate-card {{
            background: linear-gradient(135deg, rgba(251, 146, 60, 0.1) 0%, rgba(251, 146, 60, 0.03) 100%);
            border: 1px solid rgba(251, 146, 60, 0.25);
            border-radius: 12px;
            padding: 20px;
        }}

        .gate-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 16px;
            color: var(--accent-orange);
        }}

        .gate-header svg {{
            width: 24px;
            height: 24px;
            fill: currentColor;
        }}

        .gate-title {{
            font-size: 16px;
            font-weight: 600;
        }}

        .gate-options {{
            display: grid;
            gap: 10px;
        }}

        .gate-option {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 12px 16px;
            background: var(--bg-primary);
            border-radius: 8px;
            transition: all 0.2s;
        }}

        .gate-option:hover {{
            background: var(--bg-tertiary);
        }}

        .gate-key {{
            width: 32px;
            height: 32px;
            background: var(--accent-orange);
            color: #000;
            border-radius: 6px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 14px;
        }}

        .gate-label {{
            flex: 1;
            font-size: 14px;
        }}

        /* Footer */
        .footer {{
            padding: 32px 48px;
            background: var(--bg-secondary);
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--text-muted);
            font-size: 12px;
        }}

        /* Scroll indicator */
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
            background: linear-gradient(90deg, var(--accent-cyan) 0%, var(--accent-purple) 100%);
            width: 0%;
            transition: width 0.1s;
        }}

        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}

        .animate-in {{
            animation: fadeIn 0.3s ease forwards;
        }}
    </style>
</head>
<body>
    <div class="scroll-progress">
        <div class="scroll-progress-bar" id="progressBar"></div>
    </div>

    <div class="app">
        <nav class="sidebar" id="sidebar">
            <div class="sidebar-header">
                <div class="logo">Research Pipeline</div>
                <div class="logo-sub">Workflow Visualization</div>
            </div>
            <div class="nav" id="nav">
                <!-- Generated by JS -->
            </div>
        </nav>

        <main class="main" id="main">
            <!-- Generated by JS -->
        </main>
    </div>

    <script>
    const DATA = {data_json};

    // State
    let expandedSections = new Set(['create-research-project']);
    let expandedSteps = new Set();

    // Get orchestrator class
    function getOrchestratorClass(name) {{
        if (name.includes('create')) return 'create';
        if (name.includes('analyze')) return 'analyze';
        if (name.includes('synthesize')) return 'synthesize';
        return 'create';
    }}

    // Get orchestrator icon
    function getOrchestratorIcon(name) {{
        if (name.includes('create')) return '🚀';
        if (name.includes('analyze')) return '🔬';
        if (name.includes('synthesize')) return '✨';
        return '📦';
    }}

    // Format orchestrator name
    function formatOrchestratorName(name) {{
        return name.replace(/-/g, ' ').replace(/\\b\\w/g, c => c.toUpperCase());
    }}

    // Render sidebar navigation
    function renderNav() {{
        const nav = document.getElementById('nav');
        let html = '';

        DATA.orchestrators.forEach((orch, orchIndex) => {{
            const isExpanded = expandedSections.has(orch.name);
            const cls = getOrchestratorClass(orch.name);

            html += `
                <div class="nav-section ${{isExpanded ? 'expanded' : ''}}" data-orch="${{orch.name}}">
                    <div class="nav-section-header" onclick="toggleSection('${{orch.name}}')">
                        <div class="nav-section-icon ${{cls}}">${{getOrchestratorIcon(orch.name)}}</div>
                        <div class="nav-section-info">
                            <div class="nav-section-title">${{formatOrchestratorName(orch.name)}}</div>
                            <div class="nav-section-stats">${{orch.total_steps}} steps · ${{orch.total_gates}} gates</div>
                        </div>
                    </div>
                    <div class="nav-items">
            `;

            orch.phases.forEach(phase => {{
                html += `<div class="nav-phase">Phase ${{phase.letter}}: ${{phase.name}}</div>`;
                phase.steps.forEach(step => {{
                    const badges = [];
                    if (step.gate) badges.push('<span class="nav-item-badge gate">G</span>');
                    if (step.subagent) badges.push('<span class="nav-item-badge subagent">S</span>');
                    if (step.is_script) badges.push('<span class="nav-item-badge script">⚙</span>');

                    html += `
                        <div class="nav-item" data-step="${{orch.name}}-${{step.id}}" onclick="scrollToStep('${{orch.name}}-${{step.id}}')">
                            <span class="nav-item-number">${{step.number}}</span>
                            <span class="nav-item-name">${{step.name}}</span>
                            ${{badges.join('')}}
                        </div>
                    `;
                }});
            }});

            html += '</div></div>';
        }});

        nav.innerHTML = html;
    }}

    // Toggle section expansion
    function toggleSection(name) {{
        if (expandedSections.has(name)) {{
            expandedSections.delete(name);
        }} else {{
            expandedSections.add(name);
        }}
        renderNav();
    }}

    // Toggle step expansion
    function toggleStep(stepId) {{
        const card = document.querySelector(`[data-step-card="${{stepId}}"]`);
        if (card) {{
            card.classList.toggle('expanded');
            if (card.classList.contains('expanded')) {{
                expandedSteps.add(stepId);
            }} else {{
                expandedSteps.delete(stepId);
            }}
        }}
    }}

    // Scroll to step
    function scrollToStep(stepId) {{
        const element = document.querySelector(`[data-step-card="${{stepId}}"]`);
        if (element) {{
            element.scrollIntoView({{ behavior: 'smooth', block: 'center' }});
            // Expand it
            element.classList.add('expanded');
            expandedSteps.add(stepId);
        }}
    }}

    // Render main content
    function renderMain() {{
        const main = document.getElementById('main');
        let html = '';

        // Hero section with diagram
        html += `
            <section class="hero">
                <h1 class="hero-title">Research Pipeline Visualization</h1>
                <p class="hero-subtitle">Complete workflow for academic paper research, analysis, and synthesis</p>

                <div class="pipeline-diagram">
        `;

        DATA.pipeline.forEach((node, i) => {{
            const cls = getOrchestratorClass(node.name);
            html += `
                <div class="pipeline-node ${{cls}}" onclick="scrollToSection('${{node.name}}')">
                    <div class="pipeline-node-icon">${{getOrchestratorIcon(node.name)}}</div>
                    <div class="pipeline-node-title">${{formatOrchestratorName(node.name)}}</div>
                    <div class="pipeline-node-stats">
                        <div class="pipeline-node-stat"><span>${{node.steps}}</span> steps</div>
                        <div class="pipeline-node-stat"><span>${{node.phases}}</span> phases</div>
                        <div class="pipeline-node-stat"><span>${{node.gates}}</span> gates</div>
                    </div>
                </div>
            `;

            if (i < DATA.pipeline.length - 1) {{
                html += `
                    <div class="pipeline-arrow">
                        <svg viewBox="0 0 48 24"><path d="M0 12h40M32 4l12 8-12 8" stroke="currentColor" fill="none" stroke-width="2"/></svg>
                    </div>
                `;
            }}
        }});

        html += '</div></section>';

        // Orchestrator sections
        DATA.orchestrators.forEach(orch => {{
            const cls = getOrchestratorClass(orch.name);

            html += `
                <section class="section" id="${{orch.name}}" data-section="${{orch.name}}">
                    <div class="section-header">
                        <div class="section-icon ${{cls}}">${{getOrchestratorIcon(orch.name)}}</div>
                        <div class="section-info">
                            <h2>${{formatOrchestratorName(orch.name)}}</h2>
                            <p>${{orch.description || `${{orch.total_steps}} steps across ${{orch.phases.length}} phases`}}</p>
                        </div>
                    </div>
            `;

            orch.phases.forEach(phase => {{
                html += `
                    <div class="phase-header">
                        <div class="phase-letter ${{phase.letter}}">${{phase.letter}}</div>
                        <div class="phase-name">${{phase.name}}</div>
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
                                </div>
                                <div class="step-badges">
                                    ${{step.level ? `<span class="step-badge level">Level ${{step.level}}</span>` : ''}}
                                    ${{step.is_script ? '<span class="step-badge script">Script</span>' : ''}}
                                    ${{step.subagent ? '<span class="step-badge subagent">Subagent</span>' : ''}}
                                    ${{step.gate ? '<span class="step-badge gate">Gate</span>' : ''}}
                                </div>
                                <div class="step-expand-icon">▼</div>
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
                Research Pipeline Visualizer v5 · Generated ${{new Date().toLocaleString()}}
            </footer>
        `;

        main.innerHTML = html;
    }}

    // Render step content
    function renderStepContent(step) {{
        let html = '<div class="content-grid">';

        // Inputs
        if (step.inputs && step.inputs.length > 0) {{
            html += `
                <div class="content-card">
                    <div class="content-card-header">
                        <svg viewBox="0 0 16 16"><path d="M4.5 3.5a.5.5 0 00-.5.5v8a.5.5 0 00.5.5h8a.5.5 0 00.5-.5V6H10a1 1 0 01-1-1V2H4.5z"/></svg>
                        Inputs (${{step.inputs.length}})
                    </div>
                    <div class="content-card-body">
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

        // Outputs
        if (step.outputs && step.outputs.length > 0) {{
            html += `
                <div class="content-card">
                    <div class="content-card-header">
                        <svg viewBox="0 0 16 16"><path d="M4.5 3.5a.5.5 0 00-.5.5v8a.5.5 0 00.5.5h8a.5.5 0 00.5-.5V6H10a1 1 0 01-1-1V2H4.5z"/></svg>
                        Outputs (${{step.outputs.length}})
                    </div>
                    <div class="content-card-body">
                        ${{step.outputs.map(f => `
                            <div class="file-item">
                                <span class="file-icon output">✓</span>
                                <span class="file-path">${{f.path}}</span>
                                <span class="file-format">${{f.format}}</span>
                            </div>
                        `).join('')}}
                    </div>
                </div>
            `;
        }}

        html += '</div>';

        // Script Documentation
        if (step.script_docs && step.script_docs.length > 0) {{
            step.script_docs.forEach((doc, i) => {{
                const cmd = step.scripts && step.scripts[i] ? step.scripts[i] : '';
                html += `
                    <div class="script-doc">
                        <div class="script-doc-header">
                            <div class="script-doc-icon">⚙️</div>
                            <div class="script-doc-name">${{doc.name}}</div>
                            ${{doc.level ? `<div class="script-doc-level">Level ${{doc.level}}</div>` : ''}}
                        </div>
                        <div class="script-doc-purpose">${{doc.purpose}}</div>
                        ${{doc.description ? `<div class="script-doc-description">${{doc.description}}</div>` : ''}}

                        ${{doc.inputs && doc.inputs.length > 0 ? `
                            <div class="script-io-section">
                                <div class="script-io-title">📥 Inputs</div>
                                ${{doc.inputs.map(inp => `
                                    <div class="script-io-item">
                                        <span class="script-io-name">${{inp.name || inp.path || ''}}</span>
                                        <span class="script-io-desc">${{inp.description || ''}}</span>
                                    </div>
                                `).join('')}}
                            </div>
                        ` : ''}}

                        ${{doc.outputs && doc.outputs.length > 0 ? `
                            <div class="script-io-section">
                                <div class="script-io-title">📤 Outputs</div>
                                ${{doc.outputs.map(out => `
                                    <div class="script-io-item">
                                        <span class="script-io-name">${{out.name || out.path || ''}}</span>
                                        <span class="script-io-desc">${{out.description || ''}}</span>
                                    </div>
                                `).join('')}}
                            </div>
                        ` : ''}}

                        ${{doc.key_features && doc.key_features.length > 0 ? `
                            <div class="script-features">
                                <div class="script-io-title">✨ Key Features</div>
                                <ul>
                                    ${{doc.key_features.map(f => `<li>${{f}}</li>`).join('')}}
                                </ul>
                            </div>
                        ` : ''}}

                        ${{cmd ? `<div class="script-command">${{cmd}}</div>` : ''}}
                    </div>
                `;
            }});
        }} else if (step.scripts && step.scripts.length > 0) {{
            // Fallback: just show script commands without documentation
            step.scripts.forEach(cmd => {{
                html += `<div class="script-command">${{cmd}}</div>`;
            }});
        }}

        // Subagent config
        if (step.subagent) {{
            const sa = step.subagent;
            html += `
                <div class="subagent-config">
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
                            <div class="subagent-stat-label">Concurrency</div>
                        </div>
                        <div class="subagent-stat">
                            <div class="subagent-stat-value">${{sa.timeout}}</div>
                            <div class="subagent-stat-label">Timeout</div>
                        </div>
                        <div class="subagent-stat">
                            <div class="subagent-stat-value">${{sa.retry}}</div>
                            <div class="subagent-stat-label">Retry</div>
                        </div>
                    </div>
                    <div class="subagent-slots">
                        ${{Array(Math.min(sa.concurrency, 15)).fill(0).map(() => '<div class="subagent-slot">▶</div>').join('')}}
                    </div>
                </div>
            `;
        }}

        // Gate
        if (step.gate) {{
            html += `
                <div class="gate-card">
                    <div class="gate-header">
                        <svg viewBox="0 0 24 24"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
                        <div class="gate-title">User Decision Gate</div>
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
            `;
        }}

        return html;
    }}

    // Scroll to section
    function scrollToSection(name) {{
        const section = document.querySelector(`[data-section="${{name}}"]`);
        if (section) {{
            section.scrollIntoView({{ behavior: 'smooth' }});
            // Expand in nav
            expandedSections.add(name);
            renderNav();
        }}
    }}

    // Scroll spy
    function updateScrollSpy() {{
        const sections = document.querySelectorAll('[data-section]');
        const steps = document.querySelectorAll('[data-step-card]');
        const scrollY = window.scrollY;
        const windowHeight = window.innerHeight;

        // Update progress bar
        const docHeight = document.documentElement.scrollHeight - windowHeight;
        const progress = (scrollY / docHeight) * 100;
        document.getElementById('progressBar').style.width = progress + '%';

        // Find current section
        let currentSection = null;
        sections.forEach(section => {{
            const rect = section.getBoundingClientRect();
            if (rect.top <= windowHeight / 3) {{
                currentSection = section.dataset.section;
            }}
        }});

        // Update nav section highlight
        document.querySelectorAll('.nav-section-header').forEach(header => {{
            const section = header.closest('.nav-section');
            if (section && section.dataset.orch === currentSection) {{
                header.classList.add('active');
            }} else {{
                header.classList.remove('active');
            }}
        }});

        // Find current step
        let currentStep = null;
        steps.forEach(step => {{
            const rect = step.getBoundingClientRect();
            if (rect.top <= windowHeight / 2 && rect.bottom > 0) {{
                currentStep = step.dataset.stepCard;
            }}
        }});

        // Update nav item highlight
        document.querySelectorAll('.nav-item').forEach(item => {{
            if (item.dataset.step === currentStep) {{
                item.classList.add('active');
            }} else {{
                item.classList.remove('active');
            }}
        }});
    }}

    // Throttle scroll handler
    let scrollTimeout;
    window.addEventListener('scroll', () => {{
        if (scrollTimeout) return;
        scrollTimeout = setTimeout(() => {{
            updateScrollSpy();
            scrollTimeout = null;
        }}, 50);
    }});

    // Initialize
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

    output_file = Path(__file__).parent / "research_pipeline_flow.html"
    output_file.write_text(html, encoding='utf-8')
    print(f"\nGenerated: {output_file}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Skill Flow Visualizer v2
Parses SKILL.md files and generates interactive HTML visualization.
"""

import re
import json
import sys
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import Optional

@dataclass
class Step:
    id: str
    number: str
    name: str
    phase: str
    phase_name: str
    description: str = ""
    inputs: list = field(default_factory=list)  # Files/context loaded
    outputs: list = field(default_factory=list)  # Files created
    scripts: list = field(default_factory=list)  # Commands run
    skills_used: list = field(default_factory=list)  # Sub-skills invoked
    user_gate: bool = False
    user_options: list = field(default_factory=list)  # Y/N options
    handoff_to: Optional[str] = None
    sub_steps: list = field(default_factory=list)  # 2.1, 2.2, etc.
    raw_content: str = ""

def extract_between(content: str, start_pattern: str, end_patterns: list) -> str:
    """Extract content between start pattern and any of the end patterns."""
    start_match = re.search(start_pattern, content)
    if not start_match:
        return ""

    start_pos = start_match.end()
    end_pos = len(content)

    for end_pattern in end_patterns:
        end_match = re.search(end_pattern, content[start_pos:])
        if end_match:
            end_pos = min(end_pos, start_pos + end_match.start())

    return content[start_pos:end_pos].strip()

def parse_skill_md(content: str) -> tuple[list[Step], dict]:
    """Extract steps from SKILL.md content with full detail."""
    steps = []
    metadata = {}

    # Extract frontmatter
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        fm_content = fm_match.group(1)
        name_match = re.search(r'^name:\s*(.+)$', fm_content, re.MULTILINE)
        desc_match = re.search(r'^description:\s*["\']?(.+?)["\']?\s*$', fm_content, re.MULTILINE)
        if name_match:
            metadata['name'] = name_match.group(1).strip()
        if desc_match:
            metadata['description'] = desc_match.group(1).strip()

    # Find phases
    phase_pattern = r'#\s*PHASE\s+([A-Z]):\s*(.+?)(?=\n)'
    phases = {}
    for m in re.finditer(phase_pattern, content):
        phases[m.group(1)] = m.group(2).strip()

    # Find all step headers
    step_pattern = r'^##\s*Step\s+(\d+):\s*(.+?)$'
    step_matches = list(re.finditer(step_pattern, content, re.MULTILINE))

    # Determine current phase for each step
    phase_positions = [(m.start(), m.group(1), m.group(2)) for m in re.finditer(phase_pattern, content)]

    def get_phase_at_position(pos):
        current_phase = ("A", "Setup")
        for phase_pos, letter, name in phase_positions:
            if phase_pos < pos:
                current_phase = (letter, name)
            else:
                break
        return current_phase

    for i, match in enumerate(step_matches):
        step_num = match.group(1)
        step_name = match.group(2).strip()

        # Get content until next step or phase header
        start = match.end()
        if i + 1 < len(step_matches):
            end = step_matches[i + 1].start()
        else:
            end = len(content)

        step_content = content[start:end]

        # Get phase
        phase_letter, phase_name = get_phase_at_position(match.start())

        # Extract description (first paragraph or bold text)
        desc = ""
        desc_match = re.search(r'\*\*([^*]+)\*\*', step_content[:500])
        if desc_match:
            desc = desc_match.group(1).strip()

        # Extract inputs (files loaded/read)
        inputs = []
        input_patterns = [
            (r'(?:Read|Load|Use)\s+`([^`]+)`', 'file'),
            (r'from\s+`([^`]+\.(?:md|yaml|json))`', 'file'),
            (r'--input\s+"([^"]+)"', 'file'),
            (r'See\s+\[([^\]]+)\]\(([^)]+)\)', 'reference'),
        ]
        for pattern, ptype in input_patterns:
            for m in re.finditer(pattern, step_content, re.IGNORECASE):
                val = m.group(1) if ptype == 'file' else f"{m.group(1)}"
                if val and val not in inputs and not val.startswith('{'):
                    inputs.append(val)

        # Extract outputs (files created)
        outputs = []
        output_patterns = [
            r'\*\*Output:\s*`([^`]+)`\*\*',
            r'Output:\s*`([^`]+)`',
            r'Creates?:\s*`([^`]+)`',
            r'Save to:\s*([^\n]+)',
            r'--output\s+"([^"]+)"',
            r'Result.*?:\s*\n```\n([^\n]+)',
        ]
        for pattern in output_patterns:
            for m in re.finditer(pattern, step_content, re.IGNORECASE):
                val = m.group(1).strip().strip('`')
                if val and val not in outputs and not val.startswith('{') and '/' in val or val.endswith('.md'):
                    outputs.append(val)

        # Extract scripts/commands
        scripts = []
        script_blocks = re.findall(r'```bash\n(.*?)```', step_content, re.DOTALL)
        for block in script_blocks:
            # Get first meaningful line
            lines = [l.strip() for l in block.strip().split('\n') if l.strip() and not l.strip().startswith('#')]
            if lines:
                cmd = lines[0][:80]
                if cmd not in scripts:
                    scripts.append(cmd)

        # Extract skills used
        skills_used = []
        skill_patterns = [
            r'\[Load\s+([^\]]+)\s+skill\]',
            r'Use\s+`([^`]+)`\s+skill',
            r'Use\s+([a-z-]+)\s+skill',
        ]
        for pattern in skill_patterns:
            for m in re.finditer(pattern, step_content, re.IGNORECASE):
                skill = m.group(1).strip()
                if skill and skill not in skills_used:
                    skills_used.append(skill)

        # Check for user gate
        user_gate = False
        user_options = []
        if re.search(r'\[Y\]|\[N\]|\[S\]', step_content):
            user_gate = True
            for m in re.finditer(r'\[([YNS])\]\s*([^\n]+)', step_content):
                user_options.append(f"[{m.group(1)}] {m.group(2).strip()}")
        if 'user approval' in step_content.lower() or 'gate' in step_name.lower():
            user_gate = True

        # Check for handoff
        handoff_to = None
        handoff_match = re.search(r'(?:handoff|hand off|proceed)\s+to[:\s]+[`"]?([^`"\n]+)[`"]?', step_content, re.IGNORECASE)
        if handoff_match:
            handoff_to = handoff_match.group(1).strip()

        # Extract sub-steps (### 2.1, ### 2.2)
        sub_steps = []
        for m in re.finditer(rf'###\s+{step_num}\.(\d+)\s*:?\s*(.+?)(?=\n)', step_content):
            sub_steps.append(f"{step_num}.{m.group(1)}: {m.group(2).strip()}")

        steps.append(Step(
            id=f"step_{step_num}",
            number=step_num,
            name=step_name,
            phase=phase_letter,
            phase_name=phase_name,
            description=desc,
            inputs=inputs[:6],
            outputs=outputs[:6],
            scripts=scripts[:4],
            skills_used=skills_used,
            user_gate=user_gate,
            user_options=user_options[:4],
            handoff_to=handoff_to,
            sub_steps=sub_steps[:5],
            raw_content=""  # Don't include raw content in JSON
        ))

    return steps, metadata

def generate_html(steps: list[Step], metadata: dict) -> str:
    """Generate interactive HTML visualization with React Flow-like design."""

    skill_name = metadata.get('name', 'Skill')
    skill_desc = metadata.get('description', '')

    steps_json = json.dumps([asdict(s) for s in steps], indent=2)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{skill_name} - Flow Visualization</title>
    <style>
        :root {{
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --border: #30363d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --text-muted: #6e7681;
            --accent-green: #3fb950;
            --accent-blue: #58a6ff;
            --accent-purple: #a371f7;
            --accent-orange: #d29922;
            --accent-red: #f85149;
            --accent-pink: #db61a2;
            --phase-a: #238636;
            --phase-b: #1f6feb;
            --phase-c: #9e6a03;
            --phase-d: #8957e5;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.5;
        }}

        /* Header */
        .header {{
            background: var(--bg-secondary);
            border-bottom: 1px solid var(--border);
            padding: 16px 24px;
        }}
        .header h1 {{
            font-size: 20px;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        .header .desc {{
            color: var(--text-secondary);
            font-size: 14px;
        }}
        .header .stats {{
            display: flex;
            gap: 16px;
            margin-top: 12px;
        }}
        .stat {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 12px;
            color: var(--text-secondary);
        }}
        .stat-value {{
            font-weight: 600;
            color: var(--text-primary);
        }}

        /* Main layout */
        .main {{
            display: flex;
            height: calc(100vh - 100px);
        }}

        /* Canvas */
        .canvas {{
            flex: 1;
            overflow: auto;
            padding: 24px;
            background:
                radial-gradient(circle at 1px 1px, var(--border) 1px, transparent 0);
            background-size: 24px 24px;
        }}

        /* Flow container */
        .flow {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            max-width: 320px;
        }}

        /* Phase group */
        .phase-group {{
            margin-bottom: 16px;
        }}
        .phase-label {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-bottom: 8px;
            padding-left: 4px;
        }}

        /* Node */
        .node {{
            background: var(--bg-secondary);
            border: 1px solid var(--border);
            border-radius: 8px;
            padding: 12px 14px;
            cursor: pointer;
            transition: all 0.15s ease;
            position: relative;
        }}
        .node:hover {{
            border-color: var(--text-muted);
            transform: translateX(2px);
        }}
        .node.selected {{
            border-color: var(--accent-blue);
            box-shadow: 0 0 0 3px rgba(88, 166, 255, 0.15);
        }}
        .node-header {{
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        .node-number {{
            font-size: 10px;
            font-weight: 600;
            color: var(--text-muted);
            background: var(--bg-tertiary);
            padding: 2px 6px;
            border-radius: 4px;
        }}
        .node-name {{
            font-size: 13px;
            font-weight: 500;
            flex: 1;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .node-badges {{
            display: flex;
            gap: 4px;
            margin-top: 6px;
        }}
        .badge {{
            font-size: 10px;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 500;
        }}
        .badge-gate {{
            background: rgba(210, 153, 34, 0.2);
            color: var(--accent-orange);
        }}
        .badge-handoff {{
            background: rgba(248, 81, 73, 0.2);
            color: var(--accent-red);
        }}
        .badge-skill {{
            background: rgba(163, 113, 247, 0.2);
            color: var(--accent-purple);
        }}

        /* Phase colors */
        .node[data-phase="A"] {{ border-left: 3px solid var(--phase-a); }}
        .node[data-phase="B"] {{ border-left: 3px solid var(--phase-b); }}
        .node[data-phase="C"] {{ border-left: 3px solid var(--phase-c); }}
        .node[data-phase="D"] {{ border-left: 3px solid var(--phase-d); }}

        /* Connector line */
        .connector {{
            width: 2px;
            height: 16px;
            background: var(--border);
            margin-left: 24px;
        }}

        /* Details panel */
        .panel {{
            width: 400px;
            background: var(--bg-secondary);
            border-left: 1px solid var(--border);
            overflow-y: auto;
        }}
        .panel-header {{
            padding: 16px 20px;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            background: var(--bg-secondary);
        }}
        .panel-header h2 {{
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 4px;
        }}
        .panel-header .phase-tag {{
            font-size: 12px;
            color: var(--text-secondary);
        }}
        .panel-content {{
            padding: 16px 20px;
        }}

        /* Sections */
        .section {{
            margin-bottom: 20px;
        }}
        .section-title {{
            font-size: 11px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            color: var(--text-muted);
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .section-title svg {{
            width: 14px;
            height: 14px;
        }}

        /* Items */
        .item {{
            display: flex;
            align-items: flex-start;
            gap: 8px;
            padding: 8px 10px;
            background: var(--bg-tertiary);
            border-radius: 6px;
            margin-bottom: 6px;
            font-size: 12px;
            font-family: 'SF Mono', SFMono-Regular, ui-monospace, monospace;
        }}
        .item-icon {{
            flex-shrink: 0;
            width: 16px;
            height: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 10px;
        }}
        .item-input .item-icon {{ color: var(--accent-blue); }}
        .item-output .item-icon {{ color: var(--accent-green); }}
        .item-script .item-icon {{ color: var(--accent-orange); }}
        .item-text {{
            flex: 1;
            word-break: break-all;
        }}

        /* User gate */
        .gate-box {{
            background: rgba(210, 153, 34, 0.1);
            border: 1px solid rgba(210, 153, 34, 0.3);
            border-radius: 6px;
            padding: 12px;
        }}
        .gate-option {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 0;
            font-size: 13px;
        }}
        .gate-key {{
            font-weight: 600;
            color: var(--accent-orange);
        }}

        /* Sub-steps */
        .sub-step {{
            padding: 6px 10px;
            background: var(--bg-tertiary);
            border-radius: 4px;
            margin-bottom: 4px;
            font-size: 12px;
            color: var(--text-secondary);
        }}

        /* Empty state */
        .empty {{
            color: var(--text-muted);
            font-size: 13px;
            padding: 20px;
            text-align: center;
        }}

        /* Legend */
        .legend {{
            display: flex;
            gap: 12px;
            padding: 8px 0;
        }}
        .legend-item {{
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 11px;
            color: var(--text-secondary);
        }}
        .legend-dot {{
            width: 10px;
            height: 10px;
            border-radius: 2px;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{skill_name}</h1>
        <p class="desc">{skill_desc[:100]}{'...' if len(skill_desc) > 100 else ''}</p>
        <div class="stats">
            <div class="stat"><span class="stat-value">{len(steps)}</span> steps</div>
            <div class="stat"><span class="stat-value">{len(set(s.phase for s in steps))}</span> phases</div>
            <div class="stat"><span class="stat-value">{sum(1 for s in steps if s.user_gate)}</span> user gates</div>
        </div>
        <div class="legend">
            <div class="legend-item"><div class="legend-dot" style="background:var(--phase-a)"></div> Phase A</div>
            <div class="legend-item"><div class="legend-dot" style="background:var(--phase-b)"></div> Phase B</div>
            <div class="legend-item"><div class="legend-dot" style="background:var(--phase-c)"></div> Phase C</div>
            <div class="legend-item"><div class="legend-dot" style="background:var(--phase-d)"></div> Phase D</div>
        </div>
    </div>

    <div class="main">
        <div class="canvas">
            <div class="flow" id="flow"></div>
        </div>
        <div class="panel" id="panel">
            <div class="empty">Click a step to see details</div>
        </div>
    </div>

    <script>
    const steps = {steps_json};

    // Group by phase
    const phases = {{}};
    steps.forEach(s => {{
        if (!phases[s.phase]) phases[s.phase] = {{name: s.phase_name, steps: []}};
        phases[s.phase].steps.push(s);
    }});

    // Render flow
    const flow = document.getElementById('flow');
    let first = true;

    Object.keys(phases).sort().forEach(phase => {{
        const group = document.createElement('div');
        group.className = 'phase-group';

        const label = document.createElement('div');
        label.className = 'phase-label';
        label.textContent = `Phase ${{phase}}: ${{phases[phase].name}}`;
        group.appendChild(label);

        phases[phase].steps.forEach((step, i) => {{
            if (!first) {{
                const conn = document.createElement('div');
                conn.className = 'connector';
                group.appendChild(conn);
            }}
            first = false;

            const node = document.createElement('div');
            node.className = 'node';
            node.dataset.phase = step.phase;
            node.dataset.id = step.id;

            let badges = '';
            if (step.user_gate) badges += '<span class="badge badge-gate">Gate</span>';
            if (step.handoff_to) badges += '<span class="badge badge-handoff">Handoff</span>';
            if (step.skills_used.length) badges += '<span class="badge badge-skill">Skill</span>';

            node.innerHTML = `
                <div class="node-header">
                    <span class="node-number">${{step.number}}</span>
                    <span class="node-name">${{step.name}}</span>
                </div>
                ${{badges ? `<div class="node-badges">${{badges}}</div>` : ''}}
            `;

            node.onclick = () => selectStep(step);
            group.appendChild(node);
        }});

        flow.appendChild(group);
    }});

    function selectStep(step) {{
        // Update selection
        document.querySelectorAll('.node').forEach(n => n.classList.remove('selected'));
        document.querySelector(`[data-id="${{step.id}}"]`).classList.add('selected');

        // Render panel
        const panel = document.getElementById('panel');
        let html = `
            <div class="panel-header">
                <h2>Step ${{step.number}}: ${{step.name}}</h2>
                <div class="phase-tag">Phase ${{step.phase}}: ${{step.phase_name}}</div>
            </div>
            <div class="panel-content">
        `;

        if (step.description) {{
            html += `<div class="section">
                <div class="section-title">Description</div>
                <p style="font-size:13px;color:var(--text-secondary)">${{step.description}}</p>
            </div>`;
        }}

        if (step.sub_steps.length) {{
            html += `<div class="section">
                <div class="section-title">
                    <svg viewBox="0 0 16 16" fill="currentColor"><path d="M2 4a1 1 0 100-2 1 1 0 000 2zm3.75-1.5a.75.75 0 000 1.5h8.5a.75.75 0 000-1.5h-8.5zm0 5a.75.75 0 000 1.5h8.5a.75.75 0 000-1.5h-8.5zm0 5a.75.75 0 000 1.5h8.5a.75.75 0 000-1.5h-8.5zM3 8a1 1 0 11-2 0 1 1 0 012 0zm-1 6a1 1 0 100-2 1 1 0 000 2z"></path></svg>
                    Sub-steps
                </div>
                ${{step.sub_steps.map(s => `<div class="sub-step">${{s}}</div>`).join('')}}
            </div>`;
        }}

        if (step.inputs.length) {{
            html += `<div class="section">
                <div class="section-title">
                    <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8 0a8 8 0 110 16A8 8 0 018 0zM1.5 8a6.5 6.5 0 1013 0 6.5 6.5 0 00-13 0zm4.879-2.773l4.264 2.559a.25.25 0 010 .428l-4.264 2.559A.25.25 0 016 10.559V5.442a.25.25 0 01.379-.215z"></path></svg>
                    Inputs / Context Loaded
                </div>
                ${{step.inputs.map(f => `<div class="item item-input"><span class="item-icon">&#8594;</span><span class="item-text">${{f}}</span></div>`).join('')}}
            </div>`;
        }}

        if (step.outputs.length) {{
            html += `<div class="section">
                <div class="section-title">
                    <svg viewBox="0 0 16 16" fill="currentColor"><path d="M3.5 1.75v11.5c0 .09.048.173.126.217a.75.75 0 01-.752 1.298A1.75 1.75 0 012 13.25V1.75C2 .784 2.784 0 3.75 0h5.586c.464 0 .909.184 1.237.513l2.914 2.914c.329.328.513.773.513 1.237v8.086a1.75 1.75 0 01-1.75 1.75h-.25a.75.75 0 010-1.5h.25a.25.25 0 00.25-.25V6h-2.75A1.75 1.75 0 018 4.25V1.5H3.75a.25.25 0 00-.25.25zm6.75.062V4.25c0 .138.112.25.25.25h2.688l-.011-.013-2.914-2.914-.013-.011z"></path></svg>
                    Outputs / Files Created
                </div>
                ${{step.outputs.map(f => `<div class="item item-output"><span class="item-icon">&#10003;</span><span class="item-text">${{f}}</span></div>`).join('')}}
            </div>`;
        }}

        if (step.scripts.length) {{
            html += `<div class="section">
                <div class="section-title">
                    <svg viewBox="0 0 16 16" fill="currentColor"><path d="M4.72 3.22a.75.75 0 011.06 1.06L2.06 8l3.72 3.72a.75.75 0 11-1.06 1.06L.47 8.53a.75.75 0 010-1.06l4.25-4.25zm6.56 0a.75.75 0 10-1.06 1.06L13.94 8l-3.72 3.72a.75.75 0 101.06 1.06l4.25-4.25a.75.75 0 000-1.06l-4.25-4.25z"></path></svg>
                    Scripts / Commands
                </div>
                ${{step.scripts.map(s => `<div class="item item-script"><span class="item-icon">$</span><span class="item-text">${{s}}</span></div>`).join('')}}
            </div>`;
        }}

        if (step.skills_used.length) {{
            html += `<div class="section">
                <div class="section-title">
                    <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8.878.392a1.75 1.75 0 00-1.756 0l-5.25 3.045A1.75 1.75 0 001 4.951v6.098c0 .624.332 1.2.872 1.514l5.25 3.045a1.75 1.75 0 001.756 0l5.25-3.045c.54-.313.872-.89.872-1.514V4.951c0-.624-.332-1.2-.872-1.514L8.878.392z"></path></svg>
                    Skills Used
                </div>
                ${{step.skills_used.map(s => `<div class="item"><span class="item-icon" style="color:var(--accent-purple)">&#9670;</span><span class="item-text">${{s}}</span></div>`).join('')}}
            </div>`;
        }}

        if (step.user_gate) {{
            html += `<div class="section">
                <div class="section-title" style="color:var(--accent-orange)">
                    <svg viewBox="0 0 16 16" fill="currentColor"><path d="M9.585.52a2.678 2.678 0 00-3.17 0l-.928.68a1.178 1.178 0 01-.518.215L3.83 1.59a2.678 2.678 0 00-2.24 2.24l-.175 1.14a1.178 1.178 0 01-.215.518l-.68.928a2.678 2.678 0 000 3.17l.68.928c.113.153.186.33.215.518l.175 1.138a2.678 2.678 0 002.24 2.24l1.138.175c.187.029.365.102.518.215l.928.68a2.678 2.678 0 003.17 0l.928-.68a1.17 1.17 0 01.518-.215l1.138-.175a2.678 2.678 0 002.241-2.241l.175-1.138c.029-.187.102-.365.215-.518l.68-.928a2.678 2.678 0 000-3.17l-.68-.928a1.179 1.179 0 01-.215-.518L14.41 3.83a2.678 2.678 0 00-2.24-2.24l-1.138-.175a1.179 1.179 0 01-.518-.215L9.585.52zM7.303 1.728c.415-.305.979-.305 1.394 0l.928.68c.348.256.752.423 1.18.489l1.136.174c.51.078.909.478.987.987l.174 1.137c.066.427.233.831.489 1.18l.68.927c.305.415.305.98 0 1.394l-.68.928a2.678 2.678 0 00-.489 1.18l-.174 1.136a1.178 1.178 0 01-.987.987l-1.137.174a2.678 2.678 0 00-1.18.489l-.927.68c-.415.305-.98.305-1.394 0l-.928-.68a2.678 2.678 0 00-1.18-.489l-1.136-.174a1.178 1.178 0 01-.987-.987l-.174-1.137a2.678 2.678 0 00-.489-1.18l-.68-.927a1.178 1.178 0 010-1.394l.68-.928c.256-.348.423-.752.489-1.18l.174-1.136c.078-.51.478-.909.987-.987l1.137-.174a2.678 2.678 0 001.18-.489l.927-.68z"></path><path d="M8 5.5a.75.75 0 01.75.75v2.5a.75.75 0 01-1.5 0v-2.5A.75.75 0 018 5.5zm0 5.5a1 1 0 110 2 1 1 0 010-2z"></path></svg>
                    User Approval Gate
                </div>
                <div class="gate-box">
                    ${{step.user_options.length ? step.user_options.map(o => {{
                        const parts = o.match(/\\[([^\\]]+)\\]\\s*(.+)/);
                        return parts ? `<div class="gate-option"><span class="gate-key">[${{parts[1]}}]</span> ${{parts[2]}}</div>` : `<div class="gate-option">${{o}}</div>`;
                    }}).join('') : '<div class="gate-option">Requires user confirmation to proceed</div>'}}
                </div>
            </div>`;
        }}

        if (step.handoff_to) {{
            html += `<div class="section">
                <div class="section-title" style="color:var(--accent-red)">
                    <svg viewBox="0 0 16 16" fill="currentColor"><path d="M8.22 2.97a.75.75 0 011.06 0l4.25 4.25a.75.75 0 010 1.06l-4.25 4.25a.751.751 0 01-1.042-.018.751.751 0 01-.018-1.042l2.97-2.97H3.75a.75.75 0 010-1.5h7.44L8.22 4.03a.75.75 0 010-1.06z"></path></svg>
                    Handoff
                </div>
                <div class="item" style="border-left:3px solid var(--accent-red)">
                    <span class="item-text" style="color:var(--text-primary)">${{step.handoff_to}}</span>
                </div>
            </div>`;
        }}

        html += '</div>';
        panel.innerHTML = html;
    }}

    // Select first step
    if (steps.length) selectStep(steps[0]);
    </script>
</body>
</html>'''

    return html


def main():
    if len(sys.argv) < 2:
        skill_path = Path(__file__).parent / "orchestrators/create-research-project/SKILL.md"
    else:
        skill_path = Path(sys.argv[1])

    if not skill_path.exists():
        print(f"Error: {skill_path} not found", file=sys.stderr)
        sys.exit(1)

    print(f"Parsing: {skill_path}")
    content = skill_path.read_text(encoding='utf-8')

    steps, metadata = parse_skill_md(content)
    print(f"Found {len(steps)} steps across {len(set(s.phase for s in steps))} phases")

    for step in steps:
        gate = " [GATE]" if step.user_gate else ""
        handoff = f" -> {step.handoff_to}" if step.handoff_to else ""
        print(f"  Step {step.number}: {step.name}{gate}{handoff}")
        if step.inputs:
            print(f"    IN:  {step.inputs[:2]}")
        if step.outputs:
            print(f"    OUT: {step.outputs[:2]}")

    html = generate_html(steps, metadata)

    output_path = skill_path.parent / f"{skill_path.stem}_flow.html"
    output_path.write_text(html, encoding='utf-8')
    print(f"\nGenerated: {output_path}")


if __name__ == "__main__":
    main()

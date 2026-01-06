#!/usr/bin/env python3
"""
Research Pipeline Visualizer v11 - CONTENT-FIRST

Focus: Rich, meaningful descriptions with context and insights.
Goal: Make each step's PURPOSE and IMPORTANCE crystal clear.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class Step:
    """Represents a pipeline step with rich content."""
    number: int
    title: str
    description: str
    phase: str
    orchestrator: str

    # Rich content
    purpose: str  # WHY this step exists
    context: str  # WHEN/WHERE this happens in the flow
    details: List[str]  # Key implementation details
    outputs_produced: List[str]  # What gets created
    validation_gates: List[str]  # Quality checks
    gap_fixes: List[str]  # What problems this solves
    scripts: List[str]  # Automation used
    importance: str  # Critical/High/Medium
    dependencies: List[str]  # What this step needs

def parse_rich_step(step_num: int, title: str, content: str, phase: str, orchestrator: str) -> Step:
    """Extract deep insights from step content."""

    # 1. EXTRACT DESCRIPTION (cleaned)
    description = ""
    in_code_block = False

    for line in content.split('\n')[:80]:  # Look deeper
        stripped = line.strip()

        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue
        if not stripped or stripped.startswith(('#', '|', '---', '>')):
            continue
        if stripped.startswith('**') and stripped.endswith('**'):
            continue
        if '**MANDATORY' in stripped or '**Gap' in stripped or '**Use' in stripped:
            continue
        if stripped.startswith(('python ', 'bash ', '$ ', 'npm ', 'git ')):
            continue

        # Clean bullets and numbers
        if stripped.startswith(('-', '*', '•')):
            stripped = stripped.lstrip('-*•').strip()
        if re.match(r'^\d+[\.)]\s', stripped):
            stripped = re.sub(r'^\d+[\.)]\s+', '', stripped)

        if len(stripped) > 40:
            description = stripped
            break

    if not description:
        description = title

    # 2. EXTRACT PURPOSE (WHY this step exists)
    purpose = ""
    purpose_patterns = [
        r'(?:Purpose|Why|Goal|Objective)[:\s]+([^\n]+)',
        r'This\s+(?:step|ensures?|validates?)\s+([^\n]+)',
        r'(?:Critical|Important|Key)[:\s]+([^\n]+)'
    ]
    for pattern in purpose_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            purpose = match.group(1).strip()
            break

    if not purpose:
        # Infer from description
        if 'validate' in description.lower() or 'verify' in description.lower():
            purpose = "Quality assurance and validation"
        elif 'generate' in description.lower() or 'create' in description.lower():
            purpose = "Artifact generation"
        elif 'consolidate' in description.lower() or 'aggregate' in description.lower():
            purpose = "Data consolidation"
        else:
            purpose = "Pipeline execution"

    # 3. EXTRACT CONTEXT (WHEN/WHERE)
    context = f"Step {step_num} in {orchestrator}"
    if step_num == 0:
        context += " (initialization)"
    elif 'gate' in title.lower():
        context += " (user approval gate)"
    elif 'validate' in title.lower() or 'verify' in title.lower():
        context += " (validation checkpoint)"

    # 4. EXTRACT DETAILS (implementation specifics)
    details = []

    # Find bullet points and numbered lists
    detail_pattern = r'^[\s]*[-•*]\s+(.+)$|^[\s]*\d+[\.)]\s+(.+)$'
    for match in re.finditer(detail_pattern, content, re.MULTILINE):
        detail = match.group(1) or match.group(2)
        if detail and len(detail) > 20 and len(detail) < 200:
            # Filter out common noise
            if not any(x in detail.lower() for x in ['mandatory', 'gap g', 'python ', '```']):
                details.append(detail.strip())

    details = details[:5]  # Top 5 most important

    # 5. EXTRACT OUTPUTS
    outputs_produced = []
    output_patterns = [
        r'\*\*Output\*\*[:\s]+`([^`]+)`',
        r'(?:Creates?|Generates?|Produces?)[:\s]+`([^`]+)`',
        r'(?:Writes?|Saves?)[:\s]+`([^`]+\.(?:md|yaml|json|py))`'
    ]
    for pattern in output_patterns:
        outputs_produced.extend(re.findall(pattern, content))
    outputs_produced = list(set(outputs_produced))[:5]

    # 6. EXTRACT VALIDATION GATES
    validation_gates = []
    validation_patterns = [
        r'(?:Verify|Validate|Check|Ensure)[:\s]+([^\n]+)',
        r'(?:Must|Should|Required)[:\s]+([^\n]+)',
        r'✓\s+([^\n]+)'
    ]
    for pattern in validation_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        validation_gates.extend(matches[:3])
    validation_gates = [v.strip() for v in validation_gates if len(v) > 20][:4]

    # 7. EXTRACT GAP FIXES (what problems this solves)
    gap_fixes = []
    gap_pattern = r'(?:Gap|G)[\s]+(G?\d+[a-z]?)[:\s]+([^\n]+)'
    for match in re.finditer(gap_pattern, content, re.IGNORECASE):
        gap_id = match.group(1).upper()
        gap_desc = match.group(2).strip()
        gap_fixes.append(f"{gap_id}: {gap_desc}")
    gap_fixes = gap_fixes[:4]

    # 8. EXTRACT SCRIPTS
    scripts = []
    script_pattern = r'python\s+([^\s]+\.py)(?:\s+([^\n]+))?'
    for match in re.finditer(script_pattern, content):
        script_name = match.group(1)
        scripts.append(script_name)
    scripts = list(set(scripts))[:5]

    # 9. DETERMINE IMPORTANCE
    importance = "Medium"
    if step_num == 0:
        importance = "High"
    elif 'gate' in title.lower() or 'approval' in title.lower():
        importance = "Critical"
    elif 'validate' in title.lower() or 'verify' in title.lower():
        importance = "High"
    elif any(word in content.lower() for word in ['critical', 'mandatory', 'essential', 'required']):
        importance = "High"

    # 10. EXTRACT DEPENDENCIES
    dependencies = []
    dep_patterns = [
        r'(?:Requires?|Needs?|Depends on)[:\s]+`([^`]+)`',
        r'(?:From|Using|Reads?)[:\s]+`([^`]+\.(?:md|yaml|json))`',
        r'After\s+Step\s+(\d+)',
    ]
    for pattern in dep_patterns:
        dependencies.extend(re.findall(pattern, content, re.IGNORECASE))
    dependencies = list(set(dependencies))[:4]

    return Step(
        number=step_num,
        title=title,
        description=description,
        phase=phase,
        orchestrator=orchestrator,
        purpose=purpose,
        context=context,
        details=details,
        outputs_produced=outputs_produced,
        validation_gates=validation_gates,
        gap_fixes=gap_fixes,
        scripts=scripts,
        importance=importance,
        dependencies=dependencies
    )

def parse_skill_rich(skill_path: Path, orchestrator_name: str) -> List[Step]:
    """Parse SKILL.md with deep content extraction."""
    content = skill_path.read_text(encoding='utf-8')

    step_pattern = r'^## Step\s+(\d+)[:\s]+(.+)$'
    step_matches = list(re.finditer(step_pattern, content, re.MULTILINE | re.IGNORECASE))

    phase_pattern = r'^# PHASE\s+([A-Z])[:\s]+(.+)$'
    phase_matches = list(re.finditer(phase_pattern, content, re.MULTILINE | re.IGNORECASE))

    steps = []
    for i, step_match in enumerate(step_matches):
        step_num = int(step_match.group(1))
        step_title = step_match.group(2).strip()

        start_pos = step_match.end()
        end_pos = step_matches[i + 1].start() if i + 1 < len(step_matches) else len(content)
        step_content = content[start_pos:end_pos]

        phase_label = "?"
        step_pos = step_match.start()
        for phase_match in phase_matches:
            if phase_match.start() <= step_pos:
                phase_label = phase_match.group(1).upper()

        step = parse_rich_step(step_num, step_title, step_content, phase_label, orchestrator_name)
        steps.append(step)

    return steps

def generate_html(all_steps: List[Step]) -> str:
    """Generate content-rich HTML visualization."""

    # Group by orchestrator
    orchestrators = {}
    for step in all_steps:
        if step.orchestrator not in orchestrators:
            orchestrators[step.orchestrator] = []
        orchestrators[step.orchestrator].append(step)

    # Orchestrator metadata
    orch_meta = {
        'create-research-project': {
            'icon': '🎯',
            'name': 'Phase 1: Planning & Acquisition',
            'mission': 'Build research corpus from search to preprocessed chunks',
            'key_outputs': ['_briefing.md', 'PDFs', '_chunks/*.md'],
            'complexity': '14 steps - highest manual intervention'
        },
        'analyze-research-project': {
            'icon': '🔬',
            'name': 'Phase 2: Analysis',
            'mission': 'Per-paper deep extraction with multi-point evidence',
            'key_outputs': ['index.md per paper', 'chunk_index Schema 2.3'],
            'complexity': '5 steps - 15 parallel subagents'
        },
        'synthesize-research-project': {
            'icon': '✨',
            'name': 'Phase 3: Synthesis',
            'mission': 'Cross-paper pattern extraction via 7-level architecture',
            'key_outputs': ['_synthesis_*.yaml', '_synthesis_report.md'],
            'complexity': '10 steps - 6/7 levels are deterministic scripts'
        }
    }

    total_steps = len(all_steps)
    critical_steps = sum(1 for s in all_steps if s.importance == "Critical")
    total_outputs = sum(len(s.outputs_produced) for s in all_steps)
    total_validations = sum(len(s.validation_gates) for s in all_steps)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Pipeline v11 - Content-Rich</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0a0e27;
            --bg-card: #1a1f3a;
            --bg-section: #141937;

            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;

            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-red: #ef4444;

            --border-subtle: #2d3554;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #141937 100%);
            color: var(--text-primary);
            line-height: 1.8;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }

        /* HERO */
        .hero {
            text-align: center;
            margin-bottom: 3rem;
        }

        .hero h1 {
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
        }

        .hero-stats {
            display: flex;
            gap: 1.5rem;
            justify-content: center;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }

        .hero-stat {
            background: var(--bg-card);
            padding: 0.75rem 1.5rem;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
            font-size: 0.875rem;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-blue);
            margin-right: 0.5rem;
        }

        /* ORCHESTRATOR SECTION */
        .orchestrator-section {
            margin-bottom: 4rem;
        }

        .orch-header {
            background: var(--bg-section);
            padding: 2rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            border-left: 4px solid var(--accent-purple);
        }

        .orch-title {
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
        }

        .orch-mission {
            color: var(--text-secondary);
            font-size: 1.1rem;
            margin-bottom: 1rem;
            font-style: italic;
        }

        .orch-meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1rem;
            margin-top: 1.5rem;
        }

        .orch-meta-item {
            background: var(--bg-primary);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
        }

        .orch-meta-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-blue);
            margin-bottom: 0.5rem;
            font-weight: 600;
        }

        .orch-meta-value {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        .orch-meta-value code {
            background: rgba(59, 130, 246, 0.1);
            padding: 0.2rem 0.4rem;
            border-radius: 4px;
            color: var(--accent-green);
            font-size: 0.85rem;
        }

        /* STEP CARD */
        .step-card {
            background: var(--bg-card);
            border-radius: 12px;
            padding: 2rem;
            margin-bottom: 2rem;
            border: 1px solid var(--border-subtle);
            position: relative;
        }

        .step-number {
            position: absolute;
            top: 1.5rem;
            left: 1.5rem;
            width: 40px;
            height: 40px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
        }

        .step-header {
            margin-left: 60px;
            margin-bottom: 1.5rem;
        }

        .step-title-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
            flex-wrap: wrap;
        }

        .step-title {
            font-size: 1.3rem;
            font-weight: 600;
            color: var(--text-primary);
        }

        .importance-badge {
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .importance-critical {
            background: rgba(239, 68, 68, 0.15);
            color: var(--accent-red);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .importance-high {
            background: rgba(245, 158, 11, 0.15);
            color: var(--accent-yellow);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .importance-medium {
            background: rgba(59, 130, 246, 0.15);
            color: var(--accent-blue);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .step-context {
            color: var(--text-muted);
            font-size: 0.875rem;
            margin-bottom: 1rem;
        }

        .step-description {
            color: var(--text-secondary);
            font-size: 1rem;
            line-height: 1.8;
            margin-bottom: 1.5rem;
            padding: 1rem;
            background: rgba(59, 130, 246, 0.05);
            border-left: 3px solid var(--accent-blue);
            border-radius: 4px;
        }

        .step-purpose {
            background: rgba(16, 185, 129, 0.1);
            border-left: 3px solid var(--accent-green);
            padding: 1rem;
            border-radius: 4px;
            margin-bottom: 1.5rem;
        }

        .step-purpose-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-green);
            font-weight: 700;
            margin-bottom: 0.5rem;
        }

        .step-purpose-text {
            color: var(--text-secondary);
            font-size: 0.95rem;
        }

        /* CONTENT SECTIONS */
        .content-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .content-box {
            background: var(--bg-section);
            padding: 1.25rem;
            border-radius: 8px;
            border: 1px solid var(--border-subtle);
        }

        .content-box-header {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            margin-bottom: 1rem;
            padding-bottom: 0.75rem;
            border-bottom: 1px solid var(--border-subtle);
        }

        .content-box-icon {
            font-size: 1.2rem;
        }

        .content-box-title {
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 700;
            color: var(--text-primary);
        }

        .content-box-count {
            margin-left: auto;
            background: rgba(59, 130, 246, 0.2);
            color: var(--accent-blue);
            padding: 0.2rem 0.6rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .content-list {
            list-style: none;
        }

        .content-list li {
            padding: 0.5rem 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
            line-height: 1.6;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        }

        .content-list li:last-child {
            border-bottom: none;
        }

        .content-list li::before {
            content: '▸';
            color: var(--accent-blue);
            margin-right: 0.5rem;
            font-weight: 700;
        }

        .content-list code {
            background: rgba(59, 130, 246, 0.1);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            color: var(--accent-green);
            font-size: 0.85rem;
            font-family: 'Consolas', monospace;
        }

        .gap-fix-item {
            background: rgba(245, 158, 11, 0.1);
            border-left: 3px solid var(--accent-yellow);
            padding: 0.75rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
        }

        .gap-fix-item:last-child {
            margin-bottom: 0;
        }

        /* EMPTY STATE */
        .empty-state {
            color: var(--text-muted);
            font-size: 0.875rem;
            font-style: italic;
        }

        /* RESPONSIVE */
        @media (max-width: 768px) {
            .container {
                padding: 2rem 1rem;
            }

            .content-grid {
                grid-template-columns: 1fr;
            }

            .step-header {
                margin-left: 0;
                margin-top: 60px;
            }

            .step-number {
                left: 50%;
                transform: translateX(-50%);
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HERO -->
        <div class="hero">
            <h1>Research Pipeline Architecture</h1>
            <p style="color: var(--text-secondary); font-size: 1.1rem;">
                Comprehensive 3-Phase System for Academic Paper Analysis
            </p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <span class="stat-value">""" + str(total_steps) + """</span>
                    <span>Total Steps</span>
                </div>
                <div class="hero-stat">
                    <span class="stat-value">""" + str(critical_steps) + """</span>
                    <span>Critical Gates</span>
                </div>
                <div class="hero-stat">
                    <span class="stat-value">""" + str(total_outputs) + """</span>
                    <span>Artifacts Produced</span>
                </div>
                <div class="hero-stat">
                    <span class="stat-value">""" + str(total_validations) + """</span>
                    <span>Validation Checks</span>
                </div>
            </div>
        </div>
"""

    # Generate orchestrator sections
    for orch_name, orch_steps in orchestrators.items():
        meta = orch_meta.get(orch_name, {})
        icon = meta.get('icon', '📦')
        name = meta.get('name', orch_name)
        mission = meta.get('mission', '')
        key_outputs = meta.get('key_outputs', [])
        complexity = meta.get('complexity', '')

        html += f"""
        <!-- ORCHESTRATOR: {orch_name} -->
        <div class="orchestrator-section">
            <div class="orch-header">
                <div class="orch-title">
                    <span>{icon}</span>
                    <span>{name}</span>
                </div>
                <div class="orch-mission">{mission}</div>
                <div class="orch-meta">
                    <div class="orch-meta-item">
                        <div class="orch-meta-label">Key Outputs</div>
                        <div class="orch-meta-value">
                            {', '.join(f'<code>{o}</code>' for o in key_outputs)}
                        </div>
                    </div>
                    <div class="orch-meta-item">
                        <div class="orch-meta-label">Complexity</div>
                        <div class="orch-meta-value">{complexity}</div>
                    </div>
                </div>
            </div>
"""

        # Generate step cards
        for step in orch_steps:
            importance_class = f"importance-{step.importance.lower()}"

            html += f"""
            <div class="step-card">
                <div class="step-number">{step.number}</div>
                <div class="step-header">
                    <div class="step-title-row">
                        <div class="step-title">{step.title}</div>
                        <span class="importance-badge {importance_class}">{step.importance}</span>
                    </div>
                    <div class="step-context">{step.context}</div>
                </div>

                <div class="step-description">{step.description}</div>

                <div class="step-purpose">
                    <div class="step-purpose-label">🎯 Purpose</div>
                    <div class="step-purpose-text">{step.purpose}</div>
                </div>

                <div class="content-grid">
"""

            # OUTPUTS
            if step.outputs_produced:
                html += f"""
                    <div class="content-box">
                        <div class="content-box-header">
                            <span class="content-box-icon">📤</span>
                            <span class="content-box-title">Outputs</span>
                            <span class="content-box-count">{len(step.outputs_produced)}</span>
                        </div>
                        <ul class="content-list">
"""
                for output in step.outputs_produced:
                    html += f"""
                            <li><code>{output}</code></li>
"""
                html += """
                        </ul>
                    </div>
"""

            # VALIDATION GATES
            if step.validation_gates:
                html += f"""
                    <div class="content-box">
                        <div class="content-box-header">
                            <span class="content-box-icon">✅</span>
                            <span class="content-box-title">Validations</span>
                            <span class="content-box-count">{len(step.validation_gates)}</span>
                        </div>
                        <ul class="content-list">
"""
                for validation in step.validation_gates:
                    html += f"""
                            <li>{validation}</li>
"""
                html += """
                        </ul>
                    </div>
"""

            # IMPLEMENTATION DETAILS
            if step.details:
                html += f"""
                    <div class="content-box">
                        <div class="content-box-header">
                            <span class="content-box-icon">🔧</span>
                            <span class="content-box-title">Details</span>
                            <span class="content-box-count">{len(step.details)}</span>
                        </div>
                        <ul class="content-list">
"""
                for detail in step.details:
                    html += f"""
                            <li>{detail}</li>
"""
                html += """
                        </ul>
                    </div>
"""

            # SCRIPTS
            if step.scripts:
                html += f"""
                    <div class="content-box">
                        <div class="content-box-header">
                            <span class="content-box-icon">⚙️</span>
                            <span class="content-box-title">Scripts</span>
                            <span class="content-box-count">{len(step.scripts)}</span>
                        </div>
                        <ul class="content-list">
"""
                for script in step.scripts:
                    html += f"""
                            <li><code>{script}</code></li>
"""
                html += """
                        </ul>
                    </div>
"""

            # DEPENDENCIES
            if step.dependencies:
                html += f"""
                    <div class="content-box">
                        <div class="content-box-header">
                            <span class="content-box-icon">🔗</span>
                            <span class="content-box-title">Dependencies</span>
                            <span class="content-box-count">{len(step.dependencies)}</span>
                        </div>
                        <ul class="content-list">
"""
                for dep in step.dependencies:
                    html += f"""
                            <li>{dep}</li>
"""
                html += """
                        </ul>
                    </div>
"""

            # GAP FIXES
            if step.gap_fixes:
                html += f"""
                    <div class="content-box">
                        <div class="content-box-header">
                            <span class="content-box-icon">🔧</span>
                            <span class="content-box-title">Gap Fixes</span>
                            <span class="content-box-count">{len(step.gap_fixes)}</span>
                        </div>
"""
                for gap in step.gap_fixes:
                    html += f"""
                        <div class="gap-fix-item">{gap}</div>
"""
                html += """
                    </div>
"""

            html += """
                </div>
            </div>
"""

        html += """
        </div>
"""

    html += """
    </div>
</body>
</html>
"""

    return html

def main():
    """Generate content-rich visualization."""
    base_path = Path(__file__).parent

    orchestrators = [
        ('create-research-project', base_path / 'orchestrators/create-research-project/SKILL.md'),
        ('analyze-research-project', base_path / 'orchestrators/analyze-research-project/SKILL.md'),
        ('synthesize-research-project', base_path / 'orchestrators/synthesize-research-project/SKILL.md'),
    ]

    all_steps = []
    for orch_name, skill_path in orchestrators:
        if skill_path.exists():
            print(f"Parsing {orch_name}...")
            steps = parse_skill_rich(skill_path, orch_name)
            all_steps.extend(steps)
            print(f"  [+] {len(steps)} steps with rich content")
        else:
            print(f"  [-] Not found: {skill_path}")

    html = generate_html(all_steps)
    output_path = base_path / "research_pipeline_v11_content_rich.html"
    output_path.write_text(html, encoding='utf-8')

    print(f"\n[+] Generated: {output_path}")
    print(f"  - {len(all_steps)} steps")
    print(f"  - Focus: CONTENT QUALITY - purpose, context, insights")

if __name__ == "__main__":
    main()

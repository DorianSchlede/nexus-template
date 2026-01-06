#!/usr/bin/env python3
"""
Research Pipeline Visualizer v10 - ULTRA POLISHED

Focus: Flow-first design with gorgeous visuals and expandable details.
Style: Modern, clean, professional - like a premium product documentation.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List
import re

@dataclass
class Step:
    """Represents a pipeline step with minimal metadata."""
    number: int
    title: str
    description: str
    phase: str
    orchestrator: str

    # Simple metadata
    action: str
    inputs: List[str]
    outputs: List[str]

    # Counts for badges
    code_count: int = 0
    script_count: int = 0
    validation_count: int = 0

def parse_simple_step(step_num: int, title: str, content: str, phase: str, orchestrator: str) -> Step:
    """Extract only what matters for understanding flow."""

    # Extract description - find the first explanatory paragraph
    description = ""
    in_code_block = False
    found_paragraph = False

    for line in content.split('\n')[:50]:  # First 50 lines
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith('```'):
            in_code_block = not in_code_block
            continue

        if in_code_block:
            continue

        # Skip empty lines, headers, tables
        if not stripped or stripped.startswith(('#', '|', '---', '>')):
            continue

        # Skip bold labels/markers (MANDATORY, Gap, etc.)
        if stripped.startswith('**') and stripped.endswith('**'):
            continue
        if '**MANDATORY' in stripped or '**Gap' in stripped or '**Use' in stripped:
            continue

        # Skip code/script commands
        if stripped.startswith(('python ', 'bash ', '$ ', 'npm ', 'git ')):
            continue

        # Skip bullet points unless they're descriptive
        if stripped.startswith(('-', '*', '•')):
            # Allow bullets that are full sentences (>60 chars)
            if len(stripped) < 60:
                continue
            # Remove bullet marker
            stripped = stripped.lstrip('-*•').strip()

        # Skip numbered list items
        if re.match(r'^\d+[\.)]\s', stripped):
            # Remove number prefix
            stripped = re.sub(r'^\d+[\.)]\s+', '', stripped)

        # FOUND: First real explanatory paragraph
        if len(stripped) > 40:  # Minimum sentence length
            description = stripped
            found_paragraph = True
            break

    # Fallback: use title if no description found
    if not description:
        description = title

    # Extract action (use title or first sentence)
    action = title

    # Count content types (quick regex)
    code_count = len(re.findall(r'```', content))
    script_count = len(re.findall(r'python\s+\w+\.py', content))
    validation_count = len(re.findall(r'(?:verify|check|validate|ensure)', content, re.I))

    # Extract files (simplified)
    inputs = re.findall(r'(?:from|using|reads?)\s+`([^`]+\.(?:md|yaml|json))`', content)[:3]
    outputs = re.findall(r'\*\*Output\*\*[:\s]+`([^`]+)`', content)[:3]

    return Step(
        number=step_num,
        title=title,
        description=description,
        phase=phase,
        orchestrator=orchestrator,
        action=action,
        inputs=inputs,
        outputs=outputs,
        code_count=code_count // 2,  # Each code block has 2 ```
        script_count=script_count,
        validation_count=validation_count
    )

def parse_skill_simple(skill_path: Path, orchestrator_name: str) -> List[Step]:
    """Parse SKILL.md - extract only flow essentials."""
    content = skill_path.read_text(encoding='utf-8')

    # Find steps
    step_pattern = r'^## Step\s+(\d+)[:\s]+(.+)$'
    step_matches = list(re.finditer(step_pattern, content, re.MULTILINE | re.IGNORECASE))

    # Find phases for context
    phase_pattern = r'^# PHASE\s+([A-Z])[:\s]+(.+)$'
    phase_matches = list(re.finditer(phase_pattern, content, re.MULTILINE | re.IGNORECASE))

    steps = []
    for i, step_match in enumerate(step_matches):
        step_num = int(step_match.group(1))
        step_title = step_match.group(2).strip()

        # Extract step content
        start_pos = step_match.end()
        end_pos = step_matches[i + 1].start() if i + 1 < len(step_matches) else len(content)
        step_content = content[start_pos:end_pos]

        # Determine phase
        phase_label = "?"
        step_pos = step_match.start()
        for phase_match in phase_matches:
            if phase_match.start() <= step_pos:
                phase_label = phase_match.group(1).upper()

        step = parse_simple_step(step_num, step_title, step_content, phase_label, orchestrator_name)
        steps.append(step)

    return steps

def generate_html(all_steps: List[Step]) -> str:
    """Generate ultra-polished HTML with premium design."""

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
            'color': '#3b82f6',
            'desc': 'Planning & Acquisition',
            'phase': 'Phase 1'
        },
        'analyze-research-project': {
            'icon': '🔬',
            'color': '#10b981',
            'desc': 'Analysis',
            'phase': 'Phase 2'
        },
        'synthesize-research-project': {
            'icon': '✨',
            'color': '#8b5cf6',
            'desc': 'Synthesis (7-Level)',
            'phase': 'Phase 3'
        }
    }

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Pipeline v10 - Ultra Polished</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg-primary: #0a0e27;
            --bg-secondary: #141937;
            --bg-tertiary: #1e2447;
            --bg-card: #1a1f3a;

            --text-primary: #f8fafc;
            --text-secondary: #cbd5e1;
            --text-muted: #94a3b8;
            --text-dim: #64748b;

            --accent-blue: #3b82f6;
            --accent-purple: #8b5cf6;
            --accent-green: #10b981;
            --accent-yellow: #f59e0b;
            --accent-pink: #ec4899;

            --border-subtle: #2d3554;
            --border-bright: #3b82f6;

            --shadow-sm: 0 1px 3px rgba(0, 0, 0, 0.3);
            --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.4);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.5);
            --shadow-glow: 0 0 20px rgba(59, 130, 246, 0.3);
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #0a0e27 0%, #141937 100%);
            color: var(--text-primary);
            line-height: 1.7;
            min-height: 100vh;
        }

        /* CONTAINER */
        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 3rem 2rem;
        }

        /* HERO SECTION */
        .hero {
            text-align: center;
            margin-bottom: 4rem;
            padding: 3rem 0;
        }

        .hero h1 {
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 50%, #ec4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }

        .hero p {
            color: var(--text-muted);
            font-size: 1.25rem;
            max-width: 600px;
            margin: 0 auto;
        }

        .hero-stats {
            display: flex;
            gap: 2rem;
            justify-content: center;
            margin-top: 2rem;
            flex-wrap: wrap;
        }

        .hero-stat {
            background: var(--bg-card);
            padding: 1rem 2rem;
            border-radius: 12px;
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-md);
        }

        .hero-stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: var(--accent-blue);
        }

        .hero-stat-label {
            font-size: 0.875rem;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* FLOW OVERVIEW */
        .flow-overview {
            background: linear-gradient(135deg, var(--bg-secondary) 0%, var(--bg-tertiary) 100%);
            border-radius: 24px;
            padding: 3rem;
            margin-bottom: 4rem;
            border: 2px solid var(--border-bright);
            box-shadow: var(--shadow-lg), var(--shadow-glow);
            position: relative;
            overflow: hidden;
        }

        .flow-overview::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: linear-gradient(90deg, #3b82f6, #8b5cf6, #ec4899);
        }

        .flow-title {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 2.5rem;
            text-align: center;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
        }

        .flow-stages {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 2rem;
            position: relative;
        }

        .flow-stage {
            background: var(--bg-primary);
            padding: 2rem;
            border-radius: 16px;
            border: 2px solid var(--border-subtle);
            position: relative;
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-md);
        }

        .flow-stage:hover {
            border-color: var(--accent-blue);
            transform: translateY(-4px);
            box-shadow: var(--shadow-lg);
        }

        .flow-stage-icon {
            font-size: 3rem;
            margin-bottom: 1rem;
            display: block;
        }

        .flow-stage-phase {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-blue);
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .flow-stage-name {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.75rem;
        }

        .flow-stage-desc {
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-bottom: 1rem;
            line-height: 1.6;
        }

        .flow-stage-steps {
            display: inline-block;
            background: rgba(59, 130, 246, 0.1);
            color: var(--accent-blue);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.875rem;
            font-weight: 600;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        /* ORCHESTRATOR SECTIONS */
        .orchestrator-section {
            margin-bottom: 5rem;
        }

        .orchestrator-header {
            background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
            padding: 2rem;
            border-radius: 20px;
            margin-bottom: 2.5rem;
            border: 1px solid var(--border-subtle);
            box-shadow: var(--shadow-md);
            display: flex;
            align-items: center;
            gap: 1.5rem;
            position: relative;
            overflow: hidden;
        }

        .orchestrator-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            width: 6px;
            background: var(--accent-purple);
        }

        .orchestrator-icon {
            font-size: 3.5rem;
            line-height: 1;
        }

        .orchestrator-content h2 {
            font-size: 2rem;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 0.5rem;
        }

        .orchestrator-meta {
            display: flex;
            gap: 1rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .orchestrator-badge {
            background: rgba(139, 92, 246, 0.15);
            color: var(--accent-purple);
            padding: 0.4rem 1rem;
            border-radius: 12px;
            font-size: 0.875rem;
            font-weight: 600;
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        /* TIMELINE */
        .steps-timeline {
            position: relative;
            padding-left: 4rem;
        }

        .steps-timeline::before {
            content: '';
            position: absolute;
            left: 2rem;
            top: 2rem;
            bottom: 2rem;
            width: 3px;
            background: linear-gradient(180deg, var(--accent-blue) 0%, var(--accent-purple) 100%);
            border-radius: 2px;
        }

        /* STEP CARD */
        .step-card {
            background: var(--bg-card);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 2rem;
            position: relative;
            border: 1px solid var(--border-subtle);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            box-shadow: var(--shadow-sm);
        }

        .step-card:hover {
            border-color: var(--accent-blue);
            transform: translateX(8px);
            box-shadow: var(--shadow-md);
        }

        .step-card::before {
            content: attr(data-step);
            position: absolute;
            left: -4rem;
            top: 2rem;
            width: 48px;
            height: 48px;
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 1.1rem;
            border: 4px solid var(--bg-primary);
            box-shadow: var(--shadow-md);
        }

        .step-header {
            margin-bottom: 1.25rem;
        }

        .step-title-row {
            display: flex;
            align-items: center;
            gap: 1rem;
            margin-bottom: 0.75rem;
            flex-wrap: wrap;
        }

        .step-title {
            font-size: 1.35rem;
            color: var(--text-primary);
            font-weight: 600;
            flex: 1;
            min-width: 200px;
        }

        .step-phase {
            background: rgba(59, 130, 246, 0.15);
            color: var(--accent-blue);
            padding: 0.35rem 0.85rem;
            border-radius: 8px;
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .step-description {
            color: var(--text-secondary);
            margin-bottom: 1.5rem;
            line-height: 1.8;
            font-size: 1rem;
        }

        /* META BADGES */
        .step-meta {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }

        .meta-badge {
            background: var(--bg-tertiary);
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-size: 0.875rem;
            color: var(--text-muted);
            border: 1px solid var(--border-subtle);
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s ease;
        }

        .meta-badge.has-content {
            background: rgba(59, 130, 246, 0.1);
            border-color: rgba(59, 130, 246, 0.4);
            color: var(--accent-blue);
            font-weight: 600;
        }

        .meta-badge:hover {
            transform: translateY(-2px);
        }

        .badge-icon {
            font-size: 1rem;
        }

        /* TOGGLE DETAILS */
        .toggle-details {
            background: linear-gradient(135deg, var(--accent-blue), var(--accent-purple));
            color: white;
            border: none;
            padding: 0.65rem 1.5rem;
            border-radius: 10px;
            font-size: 0.875rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.2s ease;
            box-shadow: var(--shadow-sm);
            display: inline-flex;
            align-items: center;
            gap: 0.5rem;
        }

        .toggle-details:hover {
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }

        .toggle-details:active {
            transform: translateY(0);
        }

        /* DETAILS PANEL */
        .step-details {
            display: none;
            margin-top: 1.5rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border-subtle);
            animation: slideDown 0.3s ease-out;
        }

        .step-details.show {
            display: block;
        }

        @keyframes slideDown {
            from {
                opacity: 0;
                transform: translateY(-10px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        .details-section {
            margin-bottom: 1.5rem;
        }

        .details-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--accent-blue);
            font-weight: 700;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .details-content {
            background: var(--bg-tertiary);
            padding: 1rem;
            border-radius: 10px;
            border: 1px solid var(--border-subtle);
        }

        .file-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        .file-item {
            background: var(--bg-secondary);
            padding: 0.65rem 1rem;
            border-radius: 8px;
            font-family: 'JetBrains Mono', 'Consolas', monospace;
            font-size: 0.875rem;
            color: var(--accent-green);
            border: 1px solid rgba(16, 185, 129, 0.2);
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .file-icon {
            color: var(--accent-blue);
        }

        /* FOOTER */
        .footer {
            text-align: center;
            padding: 3rem 0;
            color: var(--text-dim);
            font-size: 0.875rem;
            border-top: 1px solid var(--border-subtle);
            margin-top: 4rem;
        }

        /* SCROLLBAR */
        ::-webkit-scrollbar {
            width: 12px;
        }

        ::-webkit-scrollbar-track {
            background: var(--bg-secondary);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--accent-blue);
            border-radius: 6px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--accent-purple);
        }

        /* RESPONSIVE */
        @media (max-width: 768px) {
            .container {
                padding: 2rem 1rem;
            }

            .hero h1 {
                font-size: 2.5rem;
            }

            .flow-stages {
                grid-template-columns: 1fr;
            }

            .steps-timeline {
                padding-left: 3rem;
            }

            .steps-timeline::before {
                left: 1.5rem;
            }

            .step-card::before {
                left: -3rem;
                width: 40px;
                height: 40px;
                font-size: 0.95rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HERO -->
        <div class="hero">
            <h1>Research Pipeline</h1>
            <p>3-Phase Architecture • 29 Steps • 7-Level Synthesis</p>
            <div class="hero-stats">
                <div class="hero-stat">
                    <div class="hero-stat-value">3</div>
                    <div class="hero-stat-label">Phases</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-value">29</div>
                    <div class="hero-stat-label">Steps</div>
                </div>
                <div class="hero-stat">
                    <div class="hero-stat-value">11</div>
                    <div class="hero-stat-label">Components</div>
                </div>
            </div>
        </div>

        <!-- FLOW OVERVIEW -->
        <div class="flow-overview">
            <div class="flow-title">
                <span>🚀</span>
                <span>Pipeline Flow</span>
            </div>
            <div class="flow-stages">
"""

    # Generate flow stages
    for i, (orch_name, orch_steps) in enumerate(orchestrators.items(), 1):
        meta = orch_meta.get(orch_name, {})
        icon = meta.get('icon', '📦')
        phase = meta.get('phase', f'Phase {i}')
        desc = meta.get('desc', orch_name)

        html += f"""
                <div class="flow-stage">
                    <span class="flow-stage-icon">{icon}</span>
                    <div class="flow-stage-phase">{phase}</div>
                    <div class="flow-stage-name">{desc}</div>
                    <div class="flow-stage-desc">{orch_name.replace('-', ' ').title()}</div>
                    <div class="flow-stage-steps">{len(orch_steps)} steps</div>
                </div>
"""

    html += """
            </div>
        </div>
"""

    # Generate orchestrator sections with steps
    for orch_name, orch_steps in orchestrators.items():
        meta = orch_meta.get(orch_name, {})
        icon = meta.get('icon', '📦')
        phase = meta.get('phase', 'Phase')
        desc = meta.get('desc', orch_name)

        html += f"""
        <!-- ORCHESTRATOR: {orch_name} -->
        <div class="orchestrator-section">
            <div class="orchestrator-header">
                <div class="orchestrator-icon">{icon}</div>
                <div class="orchestrator-content">
                    <h2>{desc}</h2>
                    <div class="orchestrator-meta">
                        <span class="orchestrator-badge">{phase}</span>
                        <span class="orchestrator-badge">{len(orch_steps)} Steps</span>
                        <span class="orchestrator-badge">{orch_name}</span>
                    </div>
                </div>
            </div>

            <div class="steps-timeline">
"""

        # Generate step cards
        for step in orch_steps:
            # Determine if step has content
            has_code = step.code_count > 0
            has_scripts = step.script_count > 0
            has_validations = step.validation_count > 0
            has_inputs = len(step.inputs) > 0
            has_outputs = len(step.outputs) > 0

            html += f"""
                <div class="step-card" data-step="{step.number}">
                    <div class="step-header">
                        <div class="step-title-row">
                            <div class="step-title">{step.title}</div>
                            <span class="step-phase">Phase {step.phase}</span>
                        </div>
                        <div class="step-description">{step.description}</div>
                    </div>

                    <div class="step-meta">
                        <div class="meta-badge {'has-content' if has_code else ''}">
                            <span class="badge-icon">📝</span>
                            <span>{step.code_count} code blocks</span>
                        </div>
                        <div class="meta-badge {'has-content' if has_scripts else ''}">
                            <span class="badge-icon">⚙️</span>
                            <span>{step.script_count} scripts</span>
                        </div>
                        <div class="meta-badge {'has-content' if has_validations else ''}">
                            <span class="badge-icon">✅</span>
                            <span>{step.validation_count} validations</span>
                        </div>
                    </div>
"""

            # Add toggle button if there's detail content
            if has_inputs or has_outputs:
                html += f"""
                    <button class="toggle-details" onclick="toggleDetails(this)">
                        <span>📋</span>
                        <span>Show Details</span>
                    </button>

                    <div class="step-details">
"""

                if has_inputs:
                    html += f"""
                        <div class="details-section">
                            <div class="details-label">
                                <span>📥</span>
                                <span>Input Files</span>
                            </div>
                            <div class="details-content">
                                <ul class="file-list">
"""
                    for file in step.inputs:
                        html += f"""
                                    <li class="file-item">
                                        <span class="file-icon">📄</span>
                                        <code>{file}</code>
                                    </li>
"""
                    html += """
                                </ul>
                            </div>
                        </div>
"""

                if has_outputs:
                    html += f"""
                        <div class="details-section">
                            <div class="details-label">
                                <span>📤</span>
                                <span>Output Files</span>
                            </div>
                            <div class="details-content">
                                <ul class="file-list">
"""
                    for file in step.outputs:
                        html += f"""
                                    <li class="file-item">
                                        <span class="file-icon">📄</span>
                                        <code>{file}</code>
                                    </li>
"""
                    html += """
                                </ul>
                            </div>
                        </div>
"""

                html += """
                    </div>
"""

            html += """
                </div>
"""

        html += """
            </div>
        </div>
"""

    # Footer
    html += """
        <div class="footer">
            <p>Research Pipeline v10 • Generated with ❤️ • Flow-First Design</p>
        </div>
    </div>

    <script>
        function toggleDetails(button) {
            const card = button.closest('.step-card');
            const details = card.querySelector('.step-details');
            const buttonText = button.querySelector('span:last-child');

            details.classList.toggle('show');

            if (details.classList.contains('show')) {
                buttonText.textContent = 'Hide Details';
                button.style.background = 'linear-gradient(135deg, #10b981, #3b82f6)';
            } else {
                buttonText.textContent = 'Show Details';
                button.style.background = 'linear-gradient(135deg, #3b82f6, #8b5cf6)';
            }
        }

        // Add smooth scroll behavior
        document.querySelectorAll('a[href^="#"]').forEach(anchor => {
            anchor.addEventListener('click', function (e) {
                e.preventDefault();
                const target = document.querySelector(this.getAttribute('href'));
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
            });
        });

        // Animate cards on scroll
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateY(0)';
                }
            });
        }, { threshold: 0.1 });

        document.querySelectorAll('.step-card').forEach(card => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            observer.observe(card);
        });
    </script>
</body>
</html>
"""

    return html

def main():
    """Generate the visualization."""
    base_path = Path(__file__).parent

    # Parse all orchestrators
    orchestrators = [
        ('create-research-project', base_path / 'orchestrators/create-research-project/SKILL.md'),
        ('analyze-research-project', base_path / 'orchestrators/analyze-research-project/SKILL.md'),
        ('synthesize-research-project', base_path / 'orchestrators/synthesize-research-project/SKILL.md'),
    ]

    all_steps = []
    for orch_name, skill_path in orchestrators:
        if skill_path.exists():
            print(f"Parsing {orch_name}...")
            steps = parse_skill_simple(skill_path, orch_name)
            all_steps.extend(steps)
            print(f"  [+] {len(steps)} steps")
        else:
            print(f"  [-] Not found: {skill_path}")

    # Generate HTML
    html = generate_html(all_steps)
    output_path = base_path / "research_pipeline_v10_ultra.html"
    output_path.write_text(html, encoding='utf-8')

    print(f"\n[+] Generated: {output_path}")
    print(f"  - {len(all_steps)} total steps")
    print(f"  - Focus: ULTRA POLISHED with expandable details")

if __name__ == "__main__":
    main()

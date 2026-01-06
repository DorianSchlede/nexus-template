#!/usr/bin/env python3
"""
Research Pipeline Visualizer v9 - UX Mental Model Approach
Radical simplification: Show the FLOW, hide complexity until needed
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Optional
import re

@dataclass
class Step:
    """Single step in the pipeline."""
    number: int
    title: str
    description: str
    phase: str
    orchestrator: str

    # What it does (simple)
    action: str = ""  # ONE sentence: "Downloads papers from URLs"
    why: str = ""     # ONE sentence: "To collect source materials"

    # Details (hidden by default)
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)

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
    inputs = re.findall(r'(?:from|using)\s+`([^`]+\.(?:md|yaml|json))`', content)[:3]
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
    """Generate ultra-simple HTML with flow visualization."""

    # Group by orchestrator
    orchestrators = {}
    for step in all_steps:
        if step.orchestrator not in orchestrators:
            orchestrators[step.orchestrator] = []
        orchestrators[step.orchestrator].append(step)

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Pipeline - Flow View</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0a0e27;
            color: #e2e8f0;
            line-height: 1.6;
            padding: 2rem;
        }

        .hero {
            text-align: center;
            margin-bottom: 3rem;
        }

        .hero h1 {
            font-size: 2.5rem;
            background: linear-gradient(135deg, #3b82f6, #8b5cf6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        .hero p {
            color: #94a3b8;
            font-size: 1.1rem;
        }

        /* FLOW OVERVIEW - The Key Innovation */
        .flow-overview {
            background: linear-gradient(135deg, #141937, #1e2447);
            border-radius: 16px;
            padding: 2rem;
            margin-bottom: 3rem;
            border: 2px solid #3b82f6;
        }

        .flow-title {
            font-size: 1.8rem;
            color: #3b82f6;
            margin-bottom: 2rem;
            text-align: center;
        }

        .flow-stages {
            display: flex;
            gap: 2rem;
            align-items: center;
            justify-content: center;
            flex-wrap: wrap;
        }

        .flow-stage {
            background: #0a0e27;
            padding: 2rem;
            border-radius: 12px;
            border: 2px solid #3b82f6;
            min-width: 250px;
            position: relative;
        }

        .flow-stage::after {
            content: '→';
            position: absolute;
            right: -2.5rem;
            top: 50%;
            transform: translateY(-50%);
            font-size: 2rem;
            color: #3b82f6;
        }

        .flow-stage:last-child::after {
            content: '';
        }

        .stage-number {
            background: #3b82f6;
            color: white;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.2rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }

        .stage-name {
            font-size: 1.3rem;
            font-weight: 600;
            color: #e2e8f0;
            margin-bottom: 0.5rem;
        }

        .stage-desc {
            color: #94a3b8;
            font-size: 0.95rem;
        }

        .stage-steps {
            margin-top: 1rem;
            color: #64748b;
            font-size: 0.85rem;
        }

        /* PIPELINE STEPS - Simple Cards */
        .orchestrator-section {
            margin-bottom: 4rem;
        }

        .orchestrator-header {
            background: #141937;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #8b5cf6;
            margin-bottom: 2rem;
        }

        .orchestrator-header h2 {
            color: #8b5cf6;
            font-size: 1.6rem;
        }

        .steps-timeline {
            position: relative;
            padding-left: 3rem;
        }

        .steps-timeline::before {
            content: '';
            position: absolute;
            left: 20px;
            top: 0;
            bottom: 0;
            width: 2px;
            background: linear-gradient(180deg, #3b82f6, #8b5cf6);
        }

        .step-card {
            background: #141937;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 2rem;
            position: relative;
            border: 1px solid #2d3554;
            transition: all 0.3s ease;
        }

        .step-card:hover {
            border-color: #3b82f6;
            transform: translateX(5px);
        }

        .step-card::before {
            content: attr(data-step);
            position: absolute;
            left: -3rem;
            top: 1.5rem;
            width: 40px;
            height: 40px;
            background: #3b82f6;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            border: 3px solid #0a0e27;
        }

        .step-header {
            margin-bottom: 1rem;
        }

        .step-title {
            font-size: 1.2rem;
            color: #e2e8f0;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }

        .step-phase {
            display: inline-block;
            background: rgba(59, 130, 246, 0.2);
            color: #3b82f6;
            padding: 0.25rem 0.75rem;
            border-radius: 12px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
        }

        .step-description {
            color: #94a3b8;
            margin-bottom: 1rem;
            line-height: 1.7;
        }

        /* Simple badges - less is more */
        .step-meta {
            display: flex;
            gap: 0.75rem;
            flex-wrap: wrap;
        }

        .meta-badge {
            background: #1e2447;
            padding: 0.4rem 0.8rem;
            border-radius: 6px;
            font-size: 0.85rem;
            color: #94a3b8;
            border: 1px solid #2d3554;
        }

        .meta-badge.has-content {
            background: rgba(59, 130, 246, 0.1);
            border-color: #3b82f6;
            color: #3b82f6;
        }

        /* Toggle details button */
        .toggle-details {
            background: #3b82f6;
            color: white;
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.9rem;
            margin-top: 1rem;
            transition: background 0.2s;
        }

        .toggle-details:hover {
            background: #2563eb;
        }

        .step-details {
            display: none;
            margin-top: 1rem;
            padding-top: 1rem;
            border-top: 1px solid #2d3554;
        }

        .step-details.visible {
            display: block;
        }

        .detail-section {
            margin-bottom: 1rem;
        }

        .detail-label {
            color: #64748b;
            font-size: 0.85rem;
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .detail-list {
            list-style: none;
        }

        .detail-list li {
            color: #94a3b8;
            padding: 0.5rem;
            background: #0a0e27;
            border-radius: 4px;
            margin-bottom: 0.25rem;
            font-size: 0.9rem;
        }

        .detail-list li::before {
            content: '→ ';
            color: #3b82f6;
        }
    </style>
</head>
<body>
    <div class="hero">
        <h1>Research Pipeline</h1>
        <p>Simple flow visualization - """ + str(len(all_steps)) + """ steps across 3 orchestrators</p>
    </div>

    <!-- FLOW OVERVIEW - THE KEY TO UNDERSTANDING -->
    <div class="flow-overview">
        <div class="flow-title">The Complete Flow (3 Phases)</div>
        <div class="flow-stages">
            <div class="flow-stage">
                <div class="stage-number">1</div>
                <div class="stage-name">Create</div>
                <div class="stage-desc">Download and organize research papers</div>
                <div class="stage-steps">14 steps</div>
            </div>
            <div class="flow-stage">
                <div class="stage-number">2</div>
                <div class="stage-name">Analyze</div>
                <div class="stage-desc">Extract patterns using AI agents</div>
                <div class="stage-steps">5 steps</div>
            </div>
            <div class="flow-stage">
                <div class="stage-number">3</div>
                <div class="stage-name">Synthesize</div>
                <div class="stage-desc">Merge findings into final report</div>
                <div class="stage-steps">10 steps</div>
            </div>
        </div>
    </div>

"""

    # Generate step cards for each orchestrator
    orch_order = ["create-research-project", "analyze-research-project", "synthesize-research-project"]
    orch_names = {
        "create-research-project": "Phase 1: Create (Acquisition)",
        "analyze-research-project": "Phase 2: Analyze (Extraction)",
        "synthesize-research-project": "Phase 3: Synthesize (Integration)"
    }

    for orch_key in orch_order:
        if orch_key not in orchestrators:
            continue

        steps = orchestrators[orch_key]
        html += f"""
    <div class="orchestrator-section">
        <div class="orchestrator-header">
            <h2>{orch_names.get(orch_key, orch_key)}</h2>
        </div>
        <div class="steps-timeline">
"""

        for step in steps:
            has_code = "has-content" if step.code_count > 0 else ""
            has_scripts = "has-content" if step.script_count > 0 else ""
            has_validations = "has-content" if step.validation_count > 0 else ""

            inputs_html = ""
            if step.inputs:
                inputs_html = f"""
                <div class="detail-section">
                    <div class="detail-label">Inputs</div>
                    <ul class="detail-list">
                        {"".join(f"<li>{inp}</li>" for inp in step.inputs)}
                    </ul>
                </div>
"""

            outputs_html = ""
            if step.outputs:
                outputs_html = f"""
                <div class="detail-section">
                    <div class="detail-label">Outputs</div>
                    <ul class="detail-list">
                        {"".join(f"<li>{out}</li>" for out in step.outputs)}
                    </ul>
                </div>
"""

            details_html = ""
            if inputs_html or outputs_html:
                details_html = f"""
                <button class="toggle-details" onclick="this.nextElementSibling.classList.toggle('visible')">
                    Show Details
                </button>
                <div class="step-details">
                    {inputs_html}
                    {outputs_html}
                </div>
"""

            html += f"""
            <div class="step-card" data-step="{step.number}">
                <div class="step-header">
                    <div class="step-title">{step.title}</div>
                    <span class="step-phase">Phase {step.phase}</span>
                </div>
                <div class="step-description">{step.description}</div>
                <div class="step-meta">
                    <span class="meta-badge {has_code}">Code: {step.code_count}</span>
                    <span class="meta-badge {has_scripts}">Scripts: {step.script_count}</span>
                    <span class="meta-badge {has_validations}">Validations: {step.validation_count}</span>
                </div>
                {details_html}
            </div>
"""

        html += """
        </div>
    </div>
"""

    html += """
</body>
</html>
"""

    return html

def main():
    """Main entry point."""
    base_path = Path(__file__).parent / "orchestrators"

    skill_paths = [
        ("create-research-project", base_path / "create-research-project" / "SKILL.md"),
        ("analyze-research-project", base_path / "analyze-research-project" / "SKILL.md"),
        ("synthesize-research-project", base_path / "synthesize-research-project" / "SKILL.md"),
    ]

    all_steps = []
    for orch_name, skill_path in skill_paths:
        if skill_path.exists():
            print(f"Parsing {skill_path.name}...")
            steps = parse_skill_simple(skill_path, orch_name)
            all_steps.extend(steps)
            print(f"  [+] {len(steps)} steps")
        else:
            print(f"  [-] Not found: {skill_path}")

    # Generate HTML
    html = generate_html(all_steps)
    output_path = Path(__file__).parent / "research_pipeline_v9_simple.html"
    output_path.write_text(html, encoding='utf-8')
    print(f"\n[+] Generated: {output_path}")
    print(f"  - {len(all_steps)} total steps")
    print(f"  - Focus: FLOW FIRST, details on demand")

if __name__ == "__main__":
    main()

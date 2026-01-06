#!/usr/bin/env python3
"""
Research Pipeline Visualizer v12 - HUMAN-READABLE CONTENT

Focus: Clear, concise, actionable information.
Goal: Make every piece of text immediately understandable.
"""

from pathlib import Path
from dataclasses import dataclass
from typing import List, Optional
import re

@dataclass
class Step:
    """Represents a pipeline step with human-friendly content."""
    number: int
    title: str

    # Core info (always present)
    what: str  # What this step does (1-2 sentences, plain English)
    why: str  # Why it's important
    when: str  # When it runs (initialization/middle/gate/etc)

    # Rich details (optional)
    how: List[str]  # How it works (key actions)
    creates: List[str]  # Files/artifacts created
    uses: List[str]  # Files/artifacts consumed
    checks: List[str]  # Quality validations
    scripts: List[str]  # Automation
    solves: List[str]  # Problems fixed (gap IDs)

    # Metadata
    phase: str
    orchestrator: str
    criticality: str  # MUST-PASS / IMPORTANT / STANDARD

def clean_text(text: str) -> str:
    """Clean and humanize text."""
    # Remove bullet markers
    text = re.sub(r'^[-•*]\s+', '', text.strip())
    # Remove number prefixes
    text = re.sub(r'^\d+[\.)]\s+', '', text)
    # Remove bold markers
    text = text.replace('**', '')
    # Normalize whitespace
    text = ' '.join(text.split())
    return text

def extract_what(content: str) -> str:
    """Extract WHAT this step does - plain English, actionable."""

    # Priority 1: Look for explicit "This step..." or "Creates..." statements
    explicit_patterns = [
        r'This\s+step\s+([^.]+\.[^\n]*)',
        r'This\s+(?:creates?|generates?|produces?|validates?|ensures?)\s+([^.]+\.[^\n]*)',
        r'(?:Creates?|Generates?|Produces?|Validates?|Ensures?)\s+([^.]+\.[^\n]*)',
    ]

    for pattern in explicit_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            result = clean_text(match.group(1))
            if len(result) > 30:
                return result[:300]

    # Priority 2: First substantial paragraph
    lines = content.split('\n')
    in_code = False

    for line in lines[:60]:
        stripped = line.strip()

        # Track code blocks
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue

        # Skip structural elements
        if not stripped or stripped.startswith(('#', '|', '---', '>', '**MANDATORY', '**Gap', '**Use')):
            continue
        if stripped.startswith(('python ', 'bash ', '$ ', 'npm ', 'git ')):
            continue

        # Clean bullets and numbers
        cleaned = clean_text(stripped)

        # Must be substantial
        if len(cleaned) > 50 and len(cleaned) < 300:
            return cleaned

    return "Executes pipeline step"

def extract_why(content: str, title: str, step_num: int) -> str:
    """Extract WHY this matters - the value/purpose."""

    # Look for explicit purpose statements
    why_patterns = [
        r'(?:Purpose|Why|Goal|Objective|Critical|Important)[:\s]+([^.\n]+)',
        r'This\s+(?:ensures?|prevents?|enables?|allows?)\s+([^.\n]+)',
        r'Without\s+this[,\s]+([^.\n]+)',
    ]

    for pattern in why_patterns:
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            result = clean_text(match.group(1))
            if len(result) > 20:
                return result[:200]

    # Infer from content
    lower_content = content.lower()

    if step_num == 0:
        return "Establishes foundation for all subsequent steps"
    elif 'gate' in title.lower() or 'approval' in title.lower():
        return "Requires user review before proceeding - prevents wasted effort"
    elif 'validate' in lower_content or 'verify' in lower_content:
        return "Ensures quality and correctness before moving forward"
    elif 'consolidate' in lower_content or 'aggregate' in lower_content:
        return "Reduces redundancy and improves efficiency"
    elif 'generate' in lower_content or 'create' in lower_content:
        return "Produces artifacts needed for downstream steps"
    else:
        return "Advances pipeline execution"

def extract_when(step_num: int, title: str, phase: str) -> str:
    """Extract WHEN this runs - temporal context."""

    if step_num == 0:
        return f"First step - initializes Phase {phase}"
    elif 'gate' in title.lower():
        return f"Checkpoint - requires user approval in Phase {phase}"
    elif 'validate' in title.lower() or 'verify' in title.lower():
        return f"Validation point in Phase {phase}"
    elif 'final' in title.lower() or 'complete' in title.lower():
        return f"Final step of Phase {phase}"
    else:
        return f"Step {step_num} in Phase {phase}"

def extract_how(content: str) -> List[str]:
    """Extract HOW it works - key actions in plain English."""

    actions = []

    # Find action-oriented bullet points and numbered lists
    action_pattern = r'^[\s]*(?:[-•*]|\d+[\.)])\s+(.+)$'

    for match in re.finditer(action_pattern, content, re.MULTILINE):
        text = match.group(1).strip()
        cleaned = clean_text(text)

        # Filter criteria
        if len(cleaned) < 20 or len(cleaned) > 200:
            continue
        if any(skip in cleaned for skip in ['python ', '```', 'Gap G', 'MANDATORY']):
            continue

        # Prioritize action verbs
        action_verbs = ['reads', 'writes', 'creates', 'generates', 'validates', 'checks',
                       'ensures', 'filters', 'combines', 'extracts', 'processes', 'analyzes']

        if any(verb in cleaned.lower() for verb in action_verbs):
            actions.append(cleaned)
        elif cleaned[0].isupper():  # Proper sentence
            actions.append(cleaned)

    # Return top 6 most relevant
    return actions[:6]

def extract_creates(content: str) -> List[str]:
    """Extract files/artifacts CREATED."""

    creates = []

    # Pattern 1: Explicit output markers
    patterns = [
        r'\*\*Output\*\*[:\s]+`([^`]+)`',
        r'(?:Creates?|Generates?|Produces?|Writes?)[:\s]+`([^`]+\.(?:md|yaml|json|py|txt))`',
        r'Output[:\s]+`([^`]+)`',
    ]

    for pattern in patterns:
        creates.extend(re.findall(pattern, content, re.IGNORECASE))

    # Pattern 2: File paths in context
    file_pattern = r'`([^`]+/[^`]+\.(?:md|yaml|json|py|txt))`'
    for match in re.finditer(file_pattern, content):
        file_path = match.group(1)
        # Check if context suggests output
        context_start = max(0, match.start() - 50)
        context = content[context_start:match.end()]
        if any(word in context.lower() for word in ['create', 'generate', 'write', 'save', 'output', 'produce']):
            creates.append(file_path)

    # Deduplicate and limit
    creates = list(dict.fromkeys(creates))[:5]
    return creates

def extract_uses(content: str) -> List[str]:
    """Extract files/artifacts USED/READ."""

    uses = []

    # Pattern 1: Explicit input markers
    patterns = [
        r'(?:From|Using|Reads?|Requires?|Depends on)[:\s]+`([^`]+\.(?:md|yaml|json|py|txt))`',
        r'Input[:\s]+`([^`]+)`',
    ]

    for pattern in patterns:
        uses.extend(re.findall(pattern, content, re.IGNORECASE))

    # Pattern 2: File paths with input context
    file_pattern = r'`([^`]+/[^`]+\.(?:md|yaml|json|py|txt))`'
    for match in re.finditer(file_pattern, content):
        file_path = match.group(1)
        context_start = max(0, match.start() - 50)
        context = content[context_start:match.end()]
        if any(word in context.lower() for word in ['read', 'use', 'from', 'input', 'load', 'require']):
            uses.append(file_path)

    uses = list(dict.fromkeys(uses))[:5]
    return uses

def extract_checks(content: str) -> List[str]:
    """Extract quality CHECKS/VALIDATIONS."""

    checks = []

    # Look for validation statements
    check_patterns = [
        r'(?:Verify|Validate|Check|Ensure|Confirm)[:\s]+([^.\n]+)',
        r'(?:Must|Should|Required to)[:\s]+([^.\n]+)',
        r'✓\s+([^\n]+)',
    ]

    for pattern in check_patterns:
        for match in re.finditer(pattern, content, re.IGNORECASE):
            text = clean_text(match.group(1))
            if 20 < len(text) < 200:
                checks.append(text)

    return checks[:5]

def extract_scripts(content: str) -> List[str]:
    """Extract Python/Bash SCRIPTS used."""

    scripts = []

    # Python scripts
    py_pattern = r'python\s+([^\s]+\.py)'
    scripts.extend(re.findall(py_pattern, content))

    # Bash scripts
    sh_pattern = r'bash\s+([^\s]+\.sh)'
    scripts.extend(re.findall(sh_pattern, content))

    return list(dict.fromkeys(scripts))[:5]

def extract_solves(content: str) -> List[str]:
    """Extract gap fixes/problems SOLVED."""

    solves = []

    # Pattern: Gap G## or G##x
    gap_pattern = r'(?:Gap\s+)?(G\d+[a-z]?)[:\s]+([^\n]+)'

    for match in re.finditer(gap_pattern, content, re.IGNORECASE):
        gap_id = match.group(1).upper()
        gap_desc = clean_text(match.group(2))
        if len(gap_desc) > 15:
            solves.append(f"{gap_id}: {gap_desc[:150]}")

    return solves[:4]

def determine_criticality(step_num: int, title: str, content: str) -> str:
    """Determine if step is MUST-PASS, IMPORTANT, or STANDARD."""

    lower_title = title.lower()
    lower_content = content.lower()

    # MUST-PASS: gates, critical validations
    if 'gate' in lower_title or 'approval' in lower_title:
        return "MUST-PASS"
    if step_num == 0:
        return "MUST-PASS"
    if any(word in lower_content for word in ['critical', 'mandatory', 'essential', 'required']):
        if 'validate' in lower_content or 'verify' in lower_content:
            return "MUST-PASS"

    # IMPORTANT: validations, key transformations
    if 'validate' in lower_title or 'verify' in lower_title:
        return "IMPORTANT"
    if any(word in lower_content for word in ['important', 'ensure', 'prevent']):
        return "IMPORTANT"

    return "STANDARD"

def parse_human_step(step_num: int, title: str, content: str, phase: str, orchestrator: str) -> Step:
    """Parse step with human-readable extraction."""

    return Step(
        number=step_num,
        title=title,
        what=extract_what(content),
        why=extract_why(content, title, step_num),
        when=extract_when(step_num, title, phase),
        how=extract_how(content),
        creates=extract_creates(content),
        uses=extract_uses(content),
        checks=extract_checks(content),
        scripts=extract_scripts(content),
        solves=extract_solves(content),
        phase=phase,
        orchestrator=orchestrator,
        criticality=determine_criticality(step_num, title, content)
    )

def parse_skill_human(skill_path: Path, orchestrator_name: str) -> List[Step]:
    """Parse SKILL.md with human-readable extraction."""
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

        step = parse_human_step(step_num, step_title, step_content, phase_label, orchestrator_name)
        steps.append(step)

    return steps

def generate_html(all_steps: List[Step]) -> str:
    """Generate human-readable HTML."""

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
            'name': 'Planning & Acquisition',
            'tagline': 'From research question to preprocessed chunks',
            'outcome': 'Ready-to-analyze paper corpus with metadata and chunks'
        },
        'analyze-research-project': {
            'icon': '🔬',
            'name': 'Deep Analysis',
            'tagline': 'Per-paper extraction with evidence citations',
            'outcome': 'Structured insights with chunk-level provenance'
        },
        'synthesize-research-project': {
            'icon': '✨',
            'name': 'Cross-Paper Synthesis',
            'tagline': '7-level architecture for pattern discovery',
            'outcome': 'Unified insights across entire research corpus'
        }
    }

    html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Research Pipeline - Human-Readable Guide</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        :root {
            --bg: #0a0e27;
            --card: #1a1f3a;
            --border: #2d3554;

            --text: #f8fafc;
            --text-dim: #cbd5e1;
            --text-muted: #94a3b8;

            --blue: #3b82f6;
            --purple: #8b5cf6;
            --green: #10b981;
            --yellow: #f59e0b;
            --red: #ef4444;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica', sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
            padding: 2rem 1rem;
        }

        .container {
            max-width: 900px;
            margin: 0 auto;
        }

        /* HEADER */
        .header {
            text-align: center;
            margin-bottom: 3rem;
        }

        .header h1 {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 0.5rem;
            color: var(--blue);
        }

        .header p {
            color: var(--text-dim);
            font-size: 1.1rem;
        }

        /* PHASE */
        .phase {
            margin-bottom: 3rem;
        }

        .phase-header {
            background: var(--card);
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid var(--purple);
            margin-bottom: 1.5rem;
        }

        .phase-title {
            font-size: 1.5rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }

        .phase-tagline {
            color: var(--text-dim);
            font-size: 1rem;
            margin-bottom: 0.75rem;
        }

        .phase-outcome {
            background: rgba(16, 185, 129, 0.1);
            padding: 0.75rem;
            border-radius: 6px;
            border-left: 3px solid var(--green);
            font-size: 0.95rem;
            color: var(--text-dim);
        }

        .phase-outcome::before {
            content: '✓ ';
            color: var(--green);
            font-weight: 700;
        }

        /* STEP */
        .step {
            background: var(--card);
            padding: 1.5rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            border: 1px solid var(--border);
        }

        .step-header {
            margin-bottom: 1rem;
        }

        .step-number-title {
            display: flex;
            align-items: baseline;
            gap: 0.75rem;
            margin-bottom: 0.5rem;
        }

        .step-number {
            background: linear-gradient(135deg, var(--blue), var(--purple));
            color: white;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            font-size: 0.9rem;
            flex-shrink: 0;
        }

        .step-title {
            font-size: 1.2rem;
            font-weight: 600;
            color: var(--text);
        }

        .step-badges {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 1rem;
        }

        .badge {
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .badge-must-pass {
            background: rgba(239, 68, 68, 0.15);
            color: var(--red);
            border: 1px solid rgba(239, 68, 68, 0.3);
        }

        .badge-important {
            background: rgba(245, 158, 11, 0.15);
            color: var(--yellow);
            border: 1px solid rgba(245, 158, 11, 0.3);
        }

        .badge-standard {
            background: rgba(59, 130, 246, 0.15);
            color: var(--blue);
            border: 1px solid rgba(59, 130, 246, 0.3);
        }

        .badge-when {
            background: rgba(139, 92, 246, 0.15);
            color: var(--purple);
            border: 1px solid rgba(139, 92, 246, 0.3);
        }

        /* WHAT/WHY */
        .what {
            font-size: 1rem;
            line-height: 1.7;
            color: var(--text-dim);
            margin-bottom: 1rem;
            padding-left: 1rem;
            border-left: 3px solid var(--blue);
        }

        .why {
            background: rgba(16, 185, 129, 0.08);
            padding: 0.75rem 1rem;
            border-radius: 6px;
            border-left: 3px solid var(--green);
            font-size: 0.95rem;
            color: var(--text-dim);
            margin-bottom: 1rem;
            font-style: italic;
        }

        .why::before {
            content: '💡 ';
        }

        /* SECTIONS */
        .sections {
            display: grid;
            grid-template-columns: 1fr;
            gap: 1rem;
            margin-top: 1rem;
        }

        .section {
            background: rgba(255, 255, 255, 0.03);
            padding: 1rem;
            border-radius: 8px;
            border: 1px solid var(--border);
        }

        .section-title {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--blue);
            font-weight: 700;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .section-list {
            list-style: none;
        }

        .section-list li {
            padding: 0.4rem 0;
            color: var(--text-dim);
            font-size: 0.9rem;
            line-height: 1.6;
        }

        .section-list li::before {
            content: '→ ';
            color: var(--blue);
            font-weight: 700;
            margin-right: 0.5rem;
        }

        .section-list code {
            background: rgba(59, 130, 246, 0.1);
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            color: var(--green);
            font-size: 0.85rem;
            font-family: 'Consolas', monospace;
        }

        .gap-item {
            background: rgba(245, 158, 11, 0.1);
            padding: 0.5rem;
            border-radius: 4px;
            margin-bottom: 0.5rem;
            font-size: 0.85rem;
            color: var(--text-dim);
        }

        .gap-item:last-child {
            margin-bottom: 0;
        }

        /* RESPONSIVE */
        @media (min-width: 768px) {
            .sections {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        /* EMPTY STATE */
        .empty {
            color: var(--text-muted);
            font-size: 0.85rem;
            font-style: italic;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Research Pipeline Architecture</h1>
            <p>29 steps across 3 phases - human-readable guide</p>
        </div>
"""

    # Generate phases
    for orch_name, orch_steps in orchestrators.items():
        meta = orch_meta.get(orch_name, {})
        icon = meta.get('icon', '📦')
        name = meta.get('name', orch_name)
        tagline = meta.get('tagline', '')
        outcome = meta.get('outcome', '')

        html += f"""
        <div class="phase">
            <div class="phase-header">
                <div class="phase-title">
                    <span>{icon}</span>
                    <span>{name}</span>
                </div>
                <div class="phase-tagline">{tagline}</div>
                <div class="phase-outcome">{outcome}</div>
            </div>
"""

        # Generate steps
        for step in orch_steps:
            criticality_class = f"badge-{step.criticality.lower().replace('_', '-')}"

            html += f"""
            <div class="step">
                <div class="step-header">
                    <div class="step-number-title">
                        <span class="step-number">{step.number}</span>
                        <h3 class="step-title">{step.title}</h3>
                    </div>
                    <div class="step-badges">
                        <span class="badge {criticality_class}">{step.criticality}</span>
                        <span class="badge badge-when">{step.when}</span>
                    </div>
                </div>

                <div class="what">{step.what}</div>
                <div class="why">{step.why}</div>

                <div class="sections">
"""

            # HOW
            if step.how:
                html += """
                    <div class="section">
                        <div class="section-title">🔧 How It Works</div>
                        <ul class="section-list">
"""
                for action in step.how:
                    html += f"""
                            <li>{action}</li>
"""
                html += """
                        </ul>
                    </div>
"""

            # CREATES
            if step.creates:
                html += """
                    <div class="section">
                        <div class="section-title">📤 Creates</div>
                        <ul class="section-list">
"""
                for file in step.creates:
                    html += f"""
                            <li><code>{file}</code></li>
"""
                html += """
                        </ul>
                    </div>
"""

            # USES
            if step.uses:
                html += """
                    <div class="section">
                        <div class="section-title">📥 Uses</div>
                        <ul class="section-list">
"""
                for file in step.uses:
                    html += f"""
                            <li><code>{file}</code></li>
"""
                html += """
                        </ul>
                    </div>
"""

            # CHECKS
            if step.checks:
                html += """
                    <div class="section">
                        <div class="section-title">✅ Quality Checks</div>
                        <ul class="section-list">
"""
                for check in step.checks:
                    html += f"""
                            <li>{check}</li>
"""
                html += """
                        </ul>
                    </div>
"""

            # SCRIPTS
            if step.scripts:
                html += """
                    <div class="section">
                        <div class="section-title">⚙️ Automation</div>
                        <ul class="section-list">
"""
                for script in step.scripts:
                    html += f"""
                            <li><code>{script}</code></li>
"""
                html += """
                        </ul>
                    </div>
"""

            # SOLVES
            if step.solves:
                html += """
                    <div class="section">
                        <div class="section-title">🔧 Problem Fixes</div>
"""
                for gap in step.solves:
                    html += f"""
                        <div class="gap-item">{gap}</div>
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
    """Generate human-readable visualization."""
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
            steps = parse_skill_human(skill_path, orch_name)
            all_steps.extend(steps)
            print(f"  [+] {len(steps)} steps (human-readable)")
        else:
            print(f"  [-] Not found: {skill_path}")

    html = generate_html(all_steps)
    output_path = base_path / "research_pipeline_v12_human.html"
    output_path.write_text(html, encoding='utf-8')

    print(f"\n[+] Generated: {output_path}")
    print(f"  - {len(all_steps)} steps")
    print(f"  - Focus: HUMAN-READABLE - clear, concise, actionable")

if __name__ == "__main__":
    main()

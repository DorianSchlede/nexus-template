#!/usr/bin/env python3
"""
Notion Export Validator - Checks if skill is ready for Notion export

Usage:
    python validate_for_notion.py <path/to/skill-folder>

Returns:
    Exit code 0 if ready, 1 if warnings, 2 if errors
"""

import sys
import re
from pathlib import Path

# Import basic validation
try:
    from quick_validate import validate_skill
except ImportError:
    # Fallback if not in same directory
    sys.path.insert(0, str(Path(__file__).parent))
    from quick_validate import validate_skill


def validate_for_notion(skill_path):
    """
    Validate skill for Notion export readiness.

    Returns:
        tuple: (is_ready, warnings, suggestions)
    """
    skill_path = Path(skill_path).resolve()
    skill_md = skill_path / 'SKILL.md'

    # First run basic validation
    valid, message = validate_skill(skill_path)
    if not valid:
        return False, [], [f"[ERROR] Basic validation failed: {message}"]

    if not skill_md.exists():
        return False, [], ["[ERROR] SKILL.md not found"]

    content = skill_md.read_text(encoding='utf-8')
    warnings = []
    suggestions = []

    # Check for Purpose section
    if not re.search(r'^## Purpose', content, re.MULTILINE):
        warnings.append("[!]  No '## Purpose' section found")
        suggestions.append("   -> Add a Purpose section - Notion uses this for the Purpose field")

    # Check if description is specific enough
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if match:
        frontmatter_text = match.group(1)
        desc_match = re.search(r'description:\s*(.+?)(?:\n|$)', frontmatter_text, re.DOTALL)
        if desc_match:
            description = desc_match.group(1).strip()

            # Check for TODO markers
            if 'TODO' in description or '[TODO' in description:
                warnings.append("[!]  Description contains TODO markers")
                suggestions.append("   -> Complete the description before exporting")

            # Check for generic descriptions
            generic_patterns = [
                r'\[TODO',
                r'tool$',
                r'helper$',
                r'utility$',
                r'^Load when',  # Description shouldn't start with trigger phrase
            ]
            if any(re.search(pattern, description, re.IGNORECASE) for pattern in generic_patterns):
                warnings.append(f"[!]  Description may be too generic")
                suggestions.append(f"   -> Current: '{description[:60]}...'")
                suggestions.append("   -> Make it more specific with triggers and use cases")

            # Check length
            if len(description) < 50:
                warnings.append("[!]  Description is very short (< 50 chars)")
                suggestions.append("   -> Add more detail about when and how to use this skill")

    # Check for integration hints (for Team inference)
    integrations_detected = []
    integrations_map = {
        'notion': 'Notion',
        'linear': 'Linear',
        'beam': 'Beam AI',
        'agent': 'Beam AI',
        'airtable': 'Airtable',
        'slack': 'Slack',
        'github': 'GitHub',
    }

    content_lower = content.lower()
    for keyword, integration in integrations_map.items():
        if keyword in content_lower and integration not in integrations_detected:
            integrations_detected.append(integration)

    if not integrations_detected:
        suggestions.append("[TIP] No integrations detected - AI will infer Team from content")
    else:
        suggestions.append(f"[OK] Detected integrations: {', '.join(integrations_detected)}")

    # Check for workflow structure (helps with Team inference)
    has_workflow = bool(re.search(r'^## Workflow', content, re.MULTILINE))
    has_steps = bool(re.search(r'^### Step \d+:', content, re.MULTILINE))

    if not (has_workflow or has_steps):
        suggestions.append("[TIP] No clear workflow structure detected")
        suggestions.append("   -> Consider adding a Workflow section for clarity")

    # Check for scripts, references, or assets (quality indicator)
    scripts_dir = skill_path / 'scripts'
    references_dir = skill_path / 'references'
    assets_dir = skill_path / 'assets'

    has_scripts = scripts_dir.exists() and any(scripts_dir.iterdir())
    has_references = references_dir.exists() and any(references_dir.iterdir())
    has_assets = assets_dir.exists() and any(assets_dir.iterdir())

    bundled_resources = []
    if has_scripts:
        bundled_resources.append('scripts')
    if has_references:
        bundled_resources.append('references')
    if has_assets:
        bundled_resources.append('assets')

    if bundled_resources:
        suggestions.append(f"[OK] Bundled resources: {', '.join(bundled_resources)}")
    else:
        suggestions.append("[TIP] No bundled resources (scripts/references/assets)")
        suggestions.append("   -> This is fine for simple skills")

    # Return overall readiness
    is_ready = len(warnings) == 0
    return is_ready, warnings, suggestions


def main():
    """Main entry point"""
    # Configure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            pass

    if len(sys.argv) != 2:
        print("Usage: python validate_for_notion.py <skill_directory>")
        print("\nExample:")
        print("  python validate_for_notion.py 03-skills/my-skill")
        sys.exit(1)

    skill_path = sys.argv[1]

    print(f"[CHECK] Validating skill for Notion export: {skill_path}\n")

    is_ready, warnings, suggestions = validate_for_notion(skill_path)

    # Print warnings
    if warnings:
        print("[!]  WARNINGS:")
        for w in warnings:
            print(f"  {w}")
        print()

    # Print suggestions
    if suggestions:
        print("[TIP] SUGGESTIONS:")
        for s in suggestions:
            print(f"  {s}")
        print()

    # Print result
    if is_ready:
        print("[OK] Skill is ready for Notion export!")
        sys.exit(0)
    else:
        print("[!]  Skill has warnings - review before exporting")
        sys.exit(1)


if __name__ == "__main__":
    main()

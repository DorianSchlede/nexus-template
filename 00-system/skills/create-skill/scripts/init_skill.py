#!/usr/bin/env python3
"""
Skill Initializer - Creates a new skill from template

Usage:
    init_skill.py <skill-name> --path <path>

Examples:
    init_skill.py my-new-skill --path skills/public
    init_skill.py my-api-helper --path skills/private
    init_skill.py custom-skill --path /custom/location
"""

import sys
from pathlib import Path


SKILL_TEMPLATE = """---
name: {skill_name}
description: [TODO: Complete and informative explanation of what the skill does and when to use it. Include WHEN to use this skill - specific scenarios, file types, or tasks that trigger it. Be specific and include key terms for discoverability.]
---

# {skill_title}

[TODO: One-line purpose statement - what this skill does in 1 sentence]

## Purpose

[TODO: 2-3 sentences explaining:
- What this skill does
- When to use it
- Why it's useful]

**Key Features** (optional):
- [TODO: Feature 1]
- [TODO: Feature 2]
- [TODO: Feature 3]

**Time Estimate** (optional): [TODO: X-Y minutes]

---

## Workflow

### Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] [TODO: First step description]
- [ ] [TODO: Second step description]
- [ ] [TODO: Third step description]
- [ ] [TODO: Additional steps as needed]
- [ ] Close session to save progress
```

This creates transparency and allows progress tracking.

**Mark tasks complete as you finish each step.**

---

### Step 2: [TODO: First Work Step Name]

[TODO: Describe what happens in this step]

**Actions**:
1. [TODO: Action 1]
2. [TODO: Action 2]
3. [TODO: Action 3]

**If loading resources:**
- Load [references/file-name.md](references/file-name.md) for [purpose]
- Execute scripts/script-name.py for [task]

**Mark this todo complete before proceeding.**

---

### Step 3: [TODO: Second Work Step Name]

[TODO: Describe what happens in this step]

**Mark this todo complete before proceeding.**

---

### Step N: [TODO: Add More Steps as Needed]

[TODO: Add additional workflow steps here]

**Mark this todo complete before proceeding.**

---

### Final Step: Close Session

Once the workflow is complete, **automatically trigger the close-session skill**:

```
Auto-triggering close-session to save progress...
```

The close-session skill will:
- Update system memory
- Save context for next session
- Create session report
- Clean up temporary files

**This is the final mandatory step.** Do not skip - it ensures all progress is preserved.

---

## Resources

This skill includes example resource directories for bundled resources:

### scripts/
Executable code (Python/Bash/etc.) for deterministic operations.

**Example**: scripts/example.py - Placeholder script (customize or delete)

### references/
Documentation loaded into context as needed.

**Example**: references/api_reference.md - Placeholder docs (customize or delete)

### assets/
Files used in output, not loaded into context.

**Example**: assets/example_asset.txt - Placeholder asset (customize or delete)

**Delete any unneeded directories.** Not every skill requires all three types of resources.

---

## Notes

[TODO: Add any important notes, tips, warnings, or best practices]

**About [Topic]:**
- [TODO: Note 1]
- [TODO: Note 2]
"""

EXAMPLE_SCRIPT = '''#!/usr/bin/env python3
"""
Example helper script for {skill_name}
"""

def main():
    print("This is an example script for {skill_name}")
    # TODO: Add actual script logic here

if __name__ == "__main__":
    main()
'''

EXAMPLE_REFERENCE = """# Reference Documentation for {skill_title}

This is a placeholder for detailed reference documentation.
Replace with actual reference content or delete if not needed.
"""

EXAMPLE_ASSET = """# Example Asset File

This placeholder represents where asset files would be stored.
"""


def title_case_skill_name(skill_name):
    """Convert hyphenated skill name to Title Case for display."""
    return ' '.join(word.capitalize() for word in skill_name.split('-'))


def get_skill_path(skill_name, path=None):
    """
    Get skill path, auto-detecting Nexus structure if path not provided.
    """
    if path:
        return Path(path).resolve() / skill_name

    # Auto-detect Nexus structure
    cwd = Path.cwd()

    # Check if running in Nexus-v3 context
    nexus_user_skills = cwd / "03-skills"
    nexus_system_skills = cwd / "00-system" / "skills"

    if nexus_user_skills.exists() and nexus_user_skills.is_dir():
        return nexus_user_skills / skill_name
    elif nexus_system_skills.exists() and nexus_system_skills.is_dir():
        return nexus_system_skills / skill_name
    else:
        return cwd / "skills" / skill_name


def init_skill(skill_name, path=None):
    """
    Initialize a new skill directory with template SKILL.md.
    """
    skill_dir = get_skill_path(skill_name, path)

    if skill_dir.exists():
        print(f"[ERROR] Skill directory already exists: {skill_dir}")
        return None

    try:
        skill_dir.mkdir(parents=True, exist_ok=False)
        print(f"[OK] Created skill directory: {skill_dir}")
    except Exception as e:
        print(f"[ERROR] Error creating directory: {e}")
        return None

    skill_title = title_case_skill_name(skill_name)
    skill_content = SKILL_TEMPLATE.format(
        skill_name=skill_name,
        skill_title=skill_title
    )

    skill_md_path = skill_dir / 'SKILL.md'
    try:
        skill_md_path.write_text(skill_content)
        print("[OK] Created SKILL.md")
    except Exception as e:
        print(f"[ERROR] Error creating SKILL.md: {e}")
        return None

    try:
        # Create scripts/ directory
        scripts_dir = skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)
        example_script = scripts_dir / 'example.py'
        example_script.write_text(EXAMPLE_SCRIPT.format(skill_name=skill_name))
        print("[OK] Created scripts/example.py")

        # Create references/ directory
        references_dir = skill_dir / 'references'
        references_dir.mkdir(exist_ok=True)
        example_reference = references_dir / 'api_reference.md'
        example_reference.write_text(EXAMPLE_REFERENCE.format(skill_title=skill_title))
        print("[OK] Created references/api_reference.md")

        # Create assets/ directory
        assets_dir = skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)
        example_asset = assets_dir / 'example_asset.txt'
        example_asset.write_text(EXAMPLE_ASSET)
        print("[OK] Created assets/example_asset.txt")
    except Exception as e:
        print(f"[ERROR] Error creating resource directories: {e}")
        return None

    print(f"\n[OK] Skill '{skill_name}' initialized successfully at {skill_dir}")
    print("\nNext steps:")
    print("1. Edit SKILL.md to complete the TODO items and update the description")
    print("2. Customize or delete the example files in scripts/, references/, and assets/")
    print("3. Run the validator when ready to check the skill structure")

    return skill_dir


def main():
    # Configure UTF-8 output for cross-platform compatibility (Windows/macOS/Linux)
    if sys.stdout.encoding != 'utf-8':
        try:
            sys.stdout.reconfigure(encoding='utf-8')
        except AttributeError:
            # Python < 3.7 fallback
            import io
            sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    if len(sys.argv) < 2:
        print("Usage: init_skill.py <skill-name> [--path <path>]")
        sys.exit(1)

    skill_name = sys.argv[1]
    path = None

    if len(sys.argv) >= 4 and sys.argv[2] == '--path':
        path = sys.argv[3]

    print(f"[INIT] Initializing skill: {skill_name}")
    if path:
        print(f"   Location: {path} (explicit)")
    else:
        print(f"   Location: auto-detecting context...")
    print()

    result = init_skill(skill_name, path)

    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()

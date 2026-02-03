Display this menu EXACTLY as shown (single code block), then follow instructions.

```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝


GOAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{goal}


BUILD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Create & build your system
Start something new, or continue where you left off.

{builds_section}


WORK
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run your automations
Skills are reusable workflows you build once, run often.

{skills_section}


CHAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Just talk
No structure needed. Ask anything, I'll help directly.

```

================================================================================
CLAUDE INSTRUCTIONS
================================================================================

STATE: Post-onboarding main menu

Display the menu above EXACTLY as formatted. The menu is complete - do not add
explanatory text, suggestions, or CTAs after it.

Wait for user input, then route:

BUILD triggers:
- "plan" or "new build" → load plan-build skill
- "#N" or "N" (number) → load execute-build for build at that index
- "manage" → show all builds with status
- "roadmap" → view and manage roadmap

WORK triggers:
- [skill name] → load that skill
- "create" or "new skill" → load plan-build skill in skill mode
- "list" or "list skills" → load list-skills skill

CHAT (implicit):
- Any other input → respond naturally, no forced workflow


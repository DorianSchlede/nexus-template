Display this menu EXACTLY as shown (single code block), then follow instructions.

```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝
    Build yourself the AI copilot system of your dreams.


GOAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{goal}


BUILD
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Create & build your system

{builds_section}

Commands
› plan [skill]         Create new skill
› plan [integration]   Connect new service
› plan [anything]      Describe what you want
› #1                   Continue build
› roadmap              View all builds


SKILLS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Run your automations

{skills_section}

Commands
› list              Show all skills
› analyze context   Import & analyze files
› integrations      View prebuilt integrations


LEARN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Understand the system

› learn builds        How builds work
› learn skills        How skills work
› learn integrations  Understanding integrations
› learn nexus         Deep dive into the system


SETTINGS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Configure your system

› setup goals         Adjust your goals
› update workspace    Update workspace map
› update nexus        Update system
› reset               Start fresh


━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
What can I help you with?

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
- "plan skill" or "create skill" → load plan-build skill in skill mode
- "plan integration" or "add integration" → load add-integration skill
- "#N" or "N" (number) → load execute-build for build at that index
- "roadmap" → view and manage roadmap

SKILLS triggers:
- [skill name] → load that skill
- "list" or "list skills" → load list-skills skill
- "analyze context" → load analyze-context skill
- "integrations" → show available integrations

LEARN triggers:
- "learn builds" → load learn-builds skill
- "learn skills" → load learn-skills skill
- "learn integrations" → load learn-integrations skill
- "learn nexus" → load learn-nexus skill

SETTINGS triggers:
- "setup goals" → load setup-goals skill
- "update workspace" → load update-workspace-map skill
- "update nexus" → load update-nexus skill
- "reset" → load reset-instance skill

CHAT (implicit):
- Any other input → respond naturally, no forced workflow


Display this menu in a SINGLE markdown code block, then follow the instructions below.

```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝ v4

         Your 10x Operating System

🧠 MEMORY
   [Show role and focus from <user-goals>]

📦 PROJECTS ⭐ ACTIVE WORK
   [Show each project from <active-projects>:]
   • [name] | [status] | [progress]%

🔧 SKILLS
   [Show from <skills> metadata]

📁 WORKSPACE
   [Show configured status from <state>]

🔌 INTEGRATIONS
   [Show from skills with *-connect pattern]

💡 SUGGESTED NEXT STEPS
   1. 'continue [project]' - resume at [progress]% ⭐ RECOMMENDED
   2. [other contextual suggestions]
```

================================================================================
STATE: ACTIVE PROJECTS
================================================================================

Current work:
{project_list}

Route user input:
- "continue [project name/ID]" → Load execute-project immediately
- New request → Check if it relates to existing project first
- Unclear → Ask: "Continue existing project or start something new?"

Wait for user input.

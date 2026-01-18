Display this menu EXACTLY as shown (single code block), then follow instructions.

```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

         Your AI Productivity System

🧠 MEMORY
   {memory_status}

📋 CURRENT WORK
   {work_status}

🔧 SKILLS
   50+ available

📁 FOLDERS
   {folders_status}

🔌 INTEGRATIONS
   {integrations_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 START BUILDING

   {getting_started}
```

================================================================================
CLAUDE INSTRUCTIONS
================================================================================

STATE: Fresh workspace (goals configured, no work yet)

After the menu, explain the two working modes and give recommendations.

Say:
"You're all set up! Nexus has two modes:

**BUILD** - Create something new (projects, research, content)
**EXECUTE** - Run skills for quick tasks

Here's what you can do:

1. 'I want to build something' - Start your first build (Recommended)
2. 'add integration' - Connect external tools (Slack, APIs, etc.)
3. 'list skills' - See all available skills

What would you like to do? Say '1' to start building!"

Routing:
- "1" or "build" or work description → load plan-build skill
- "2" or "integration" → load add-integration skill
- "3" or "skills" → load list-skills skill
- Skill trigger → match and load relevant skill

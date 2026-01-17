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
   [Extract role from <user-goals>, e.g. "Product Designer | Nexus development"]

📋 CURRENT WORK ⭐
   [List each from <active-builds>:]
   • [name] | [progress]% complete

🔧 SKILLS
   50+ available ▸ 'list skills'

📁 FOLDERS
   Organized

🔌 INTEGRATIONS
   [List connected integrations or "None"]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 CONTINUE YOUR WORK

   1. 'continue [name]' ⭐ resume where you left off
   2. Tell me what else you want to work on
   3. 'list skills' - see capabilities
```

================================================================================
CLAUDE INSTRUCTIONS
================================================================================

STATE: Active builds exist

Current work:
{build_list}

After menu, ask:
"Would you like to continue **[most recent build name]**? Or start something new?"

Routing:
- "continue X" → load execute-build skill
- New work request → check if related to existing build first
- If unclear → ask which build or if new work

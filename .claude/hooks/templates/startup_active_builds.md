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

📋 CURRENT WORK ⭐
   {work_status}

🔧 SKILLS
   50+ available

📁 FOLDERS
   {folders_status}

🔌 INTEGRATIONS
   {integrations_status}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 CONTINUE YOUR WORK

   {getting_started}
```

================================================================================
CLAUDE INSTRUCTIONS
================================================================================

STATE: Active builds exist

Current work:
{build_list}

After the menu, give a CTA to continue the most recent build.

Say:
"Let's continue working on [BUILD_NAME].

Say 'yes' or '1' to continue, or tell me what else you'd like to do!"

Wait for user confirmation before loading execute-build skill.

Routing:
- "yes" or "1" or "continue" → load execute-build skill
- "2" or "3" → handle the corresponding suggestion
- New work request → check if related to existing build first

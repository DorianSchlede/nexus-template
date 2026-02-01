FRESH INSTALL DETECTED - RUNNING INITIAL SETUP

This is the first time Nexus is starting after installation.
Execute the /setup skill immediately to configure essential settings.

## MANDATORY: Load and Execute /setup Skill

Load the setup skill from: 00-system/skills/system/setup/SKILL.md

Then follow these steps:

### Step 1: Welcome
Display a brief welcome message:
"Welcome to Nexus! Let me configure a few settings before we begin. This only takes about 1 minute."

### Step 2: Permission Settings
Ask user using AskUserQuestion:

Question: "How should I handle permissions?"
Header: "Permissions"

Options:
1. Label: "Automatic (Recommended)"
   Description: "I can read, write, and run commands without asking each time. This is how Nexus works best - smooth and uninterrupted. You can change this anytime in .claude/settings.local.json"

2. Label: "Ask each time"
   Description: "I'll ask permission before every file edit or command. More control, but many interruptions during workflows."

If "Automatic": Create `.claude/settings.local.json` with:
```json
{
  "permissions": {
    "allow": ["Bash(*)", "Edit", "Write", "Read", "Glob", "Grep", "WebFetch", "WebSearch"]
  }
}
```

If "Ask each time": Skip file creation (user will be prompted for each tool).

### Step 3: VS Code Settings (AUTOMATIC)
Create `.vscode/settings.json` automatically (no question needed):
```json
{
  "markdown.preview.breaks": true,
  "markdown.preview.typographer": true,
  "files.associations": {
    "*.md": "markdown"
  }
}
```

These settings just improve markdown rendering for Nexus documents.

### Step 4: Mark Setup Complete
Create marker file: `.claude/.setup_complete`
Content: `setup_completed=<timestamp>`

### Step 5: Transition
After setup, display:
"Setup complete! Now let's personalize Nexus for how you work."

Then check onboarding status and proceed to onboarding or main menu.

DO NOT show the normal menu. Execute /setup first.

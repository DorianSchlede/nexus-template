---
name: quick-start
description: "Complete onboarding: welcome, language, goals, integrations, workspace, first BUILD, permissions."
onboarding: true
priority: critical
duration: "15-20 min"
cross_session_continuity: true
version: "2.0"
---

# Quick Start

Complete onboarding flow: welcome, language selection, optionally upload context, capture your goal, **discover integrations**, optionally create a roadmap, set up your workspace **(with concrete proposals)**, plan your first BUILD **(using plan-build skill)**, configure permissions, **clear session restart instructions**.

**This skill is auto-injected by the SessionStart hook when onboarding is not complete.**

---

## Pre-Execution

**State Initialization**: The SessionStart hook automatically initializes onboarding state when this skill is loaded.

---

## Resume Logic

If resuming from compaction, check `onboarding.quick_start_state.step_completed` and resume from step + 1.

```python
def get_resume_step():
    step_completed = config.onboarding.quick_start_state.step_completed
    return step_completed + 1
```

---

## STEP 0/11: Welcome & Language (1 min)

**Display the welcome banner**:
```
    ███╗   ██╗███████╗██╗  ██╗██╗   ██╗███████╗
    ████╗  ██║██╔════╝╚██╗██╔╝██║   ██║██╔════╝
    ██╔██╗ ██║█████╗   ╚███╔╝ ██║   ██║███████╗
    ██║╚██╗██║██╔══╝   ██╔██╗ ██║   ██║╚════██║
    ██║ ╚████║███████╗██╔╝ ██╗╚██████╔╝███████║
    ╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚══════╝

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
              Your AI operating system
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ChatGPT gives you answers. Nexus enables you to build.

What people actually use it for:

  → Job Search
     Search 15 job boards every morning, prioritize matches,
     and generate tailored CVs from your stored stories.

  → Health System
     Talk to your fitness data, log meals from photos,
     get personalized training plans that adapt to your progress.

  → Content Engine
     Interview yourself to capture stories, plan your calendar,
     auto-generate posts that sound like you.

The difference: Everything you build is always remembered.
Context compounds. Every session makes it smarter.

Ready?
```

**Then display language selection**:
```
What language do you want to work in?

1. English
2. Deutsch
3. Español
4. Français
5. Italiano
6. 日本語
7. 中文
8. Other (type your language)

(All future sessions will use this language)

Type the number (1-8):
```

**When user responds**:
- If 1-7: Map to language code (en, de, es, fr, it, ja, zh)
- If 8: Ask "Which language?" and accept their input

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 0,
    "onboarding.language_preference": "<selected_language_code>",
    "user_preferences.language": "<selected_language_name>"
})
```

**IMPORTANT**: After language selection, ALL subsequent content must be displayed in the user's chosen language.

---

## STEP 1/11: How Nexus Works (30 sec)

**Display**:
```
STEP 1/11: How Nexus Works
----------------------------------------------------

Here's the key idea:

This Nexus folder IS your project. Everything lives here.
I remember what we work on. Every session compounds.

  01-memory/     → Your context (I pre-load this every session)
  02-builds/     → Where we plan and build things together
  03-skills/     → Your process automations
  04-workspace/  → Your outputs and files

No accounts. No cloud. The whole system is just this folder.
Close the chat, come back tomorrow - I pick up where we left off.

Ready?
```

**Wait for confirmation**

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 1
})
```

---

## STEP 2/11: Context Upload (Optional) (2-3 min if used)

**Display**:
```
STEP 2/11: Context Upload (Optional)
----------------------------------------------------

Have files that show what you work on?

If yes, I'll analyze them and learn:
  - What you do (role, domain)
  - Patterns in your work
  - Tools you use
  - Ideas for what to build

This takes 2-3 minutes but makes everything more personalized.
```

**Use AskUserQuestion**:
```
Question: "Want to upload context files?"
Options:
- "Yes, I have files" - I'll analyze them now
- "Skip for now" - We can do this later anytime
```

**If "Yes, I have files"**:
```
LOAD SKILL: analyze-context

The skill will:
1. Guide file upload to 01-memory/input/
2. Run SubAgent analysis (parallel)
3. Save insights to 01-memory/input/_analysis/
4. Auto-add "Organize Initial Context" to roadmap

After skill completes, continue to Step 3.
```

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 2,
    "onboarding.quick_start_state.context_uploaded": True/False
})
```

---

## STEP 3/11: Your Goal (2-3 min)

**Display**:
```
STEP 3/11: Your Goal
----------------------------------------------------

What's your goal for this Nexus?

What's the PURPOSE of having this AI system?
What should it help you achieve?

{If context uploaded: "Based on your files, I noticed: {key insights}"}

Examples:
- "Automate my content creation workflow"
- "Build a system for managing client projects"
- "Create a research organization system"

Tell me your goal:
```

**User responds**

**Use AskUserQuestion** with DYNAMIC options based on goal:

```
Question 1: "What does success look like in 3 months?" (multiSelect: true)
Options: {dynamically generated based on goal + context}

Question 2: "What's your biggest friction right now?" (multiSelect: true)
Options: {dynamically generated}
```

**Create goals.md**:
```markdown
# Your Goals

> This file loads every session - it's how I stay relevant to YOU.

## Goal

{user's stated goal}

## Success Looks Like

{from Question 1}

## Current Friction

{from Question 2}

## Context

{additional context from file analysis if available}

---

**Created**: {today}
```

**Save to**: `01-memory/goals.md`

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 3,
    "onboarding.quick_start_state.goal_captured": True,
    "first_encounters.memory_updated": True
})
```

---

## STEP 4/11: Integrations (NEW) (1-2 min)

**Display**:
```
STEP 4/11: Integrations
----------------------------------------------------

Nexus can connect to external tools and services.

When connected, I can:
  - Send messages to Slack
  - Create tasks in your project manager
  - Read/write to Google Docs
  - Track data in your CRM
  - And more...

{If context uploaded and tools detected:}
I noticed you use: {detected tools}
```

**Use AskUserQuestion**:
```
Question: "Which tools do you want to connect?" (multiSelect: true)
Header: "Integrations"
Options (DYNAMIC based on goal domain):

For Content/Marketing goals:
- "Slack" - Team communication, notifications
- "Google Workspace" - Docs, Sheets, Calendar
- "LinkedIn" - Direct posting (coming soon)
- "Notion" - Notes and databases
- "None for now" - I'll set these up later

For Sales/CRM goals:
- "HubSpot" - CRM, contacts, deals
- "Slack" - Team communication
- "Google Workspace" - Email, calendar
- "Airtable" - Databases, tracking
- "None for now"

For Development goals:
- "GitHub" - Repos, issues, PRs
- "Slack" - Team updates
- "Jira" - Project tracking
- "None for now"

Default (no specific domain):
- "Slack" - Team communication
- "Google Workspace" - Docs, Sheets, Calendar
- "Notion" - Notes and databases
- "None for now"
```

**Store selected integrations**:
```python
# Save to goals.md under new section
append_to_goals("""
## Integrations to Connect

{for each selected integration}
- [ ] {integration_name} - {purpose}
""")

# Also save to state for roadmap generation
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 4,
    "onboarding.quick_start_state.integrations_selected": ["slack", "google", ...]
})
```

**If integrations selected, show**:
```
Got it! These integrations will appear in your roadmap.

To connect them later, just say:
  "connect slack"
  "connect hubspot"
  etc.

Each integration has a setup wizard.
```

---

## STEP 5/11: Create Roadmap (Optional) (2-3 min if used)

**Display**:
```
STEP 5/11: Create Roadmap (Optional)
----------------------------------------------------

Your goal: {goal_summary}

{If integrations selected:}
Integrations to set up: {list}

Want to plan what you'll build to achieve this?

A roadmap helps you:
  - See the big picture
  - Know what comes after each build
  - Organize your workspace around your plans

{If context uploaded: "I found {N} build ideas in your files."}
```

**Use AskUserQuestion**:
```
Question: "Create a roadmap now?"
Options:
- "Yes, let's plan" - I'll suggest items based on your goal
- "Skip for now" - We'll pick one thing to build
```

**If "Yes, let's plan"**:
```
LOAD SKILL: create-roadmap

The skill will:
1. Suggest items based on goal + context + integrations
2. Auto-include integration setup for selected tools
3. Let you add/remove/prioritize
4. Save to 01-memory/roadmap.yaml

The roadmap will inform your workspace structure.

After skill completes, continue to Step 6.
```

**If skipped, continue to Step 6**

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 5,
    "onboarding.quick_start_state.roadmap_created": True/False
})
```

---

## STEP 6/11: Your Workspace (IMPROVED) (2-3 min)

**Display**:
```
STEP 6/11: Your Workspace
----------------------------------------------------

Here's something important:

I'm going to generate A LOT of stuff for you.
Plans, content, research, documents, templates...

Without structure, you'll drown in AI output.

04-workspace/ is where YOUR outputs live.
It's navigatable by both you AND me.
```

**STEP 6a: Generate and Show Proposals**

**CRITICAL**: Don't just ask preference - SHOW concrete proposals based on goal/roadmap.

**Generate 2-3 proposals based on context**:

```python
def generate_workspace_proposals(goal, roadmap_items, integrations):
    """
    Generate 2-3 concrete workspace proposals.
    Each proposal is a complete folder structure with explanations.
    """

    proposals = []

    # Proposal A: By Content Stage / Workflow Stage
    proposal_a = {
        "name": "By Stage",
        "description": "Organize by where things are in your workflow",
        "structure": generate_stage_based_structure(goal),
        "best_for": "Clear workflow, easy to find current work"
    }

    # Proposal B: By Project / Topic
    proposal_b = {
        "name": "By Project",
        "description": "Separate folder for each initiative",
        "structure": generate_project_based_structure(roadmap_items),
        "best_for": "Multiple parallel projects, clear boundaries"
    }

    # Proposal C: Hybrid / Custom based on domain
    proposal_c = {
        "name": "Hybrid",
        "description": "Mix of stages and projects",
        "structure": generate_hybrid_structure(goal, roadmap_items),
        "best_for": "Flexibility, grows naturally"
    }

    return [proposal_a, proposal_b, proposal_c]
```

**Example for LinkedIn Content goal**:

```
I'll show you 3 workspace options. Pick the one that fits how you think:

----------------------------------------------------
OPTION A: By Stage
----------------------------------------------------
04-workspace/
├── 1-ideen/              # Raw ideas, inspiration
├── 2-planung/            # Content being planned
├── 3-entwuerfe/          # Drafts in progress
├── 4-fertig/             # Ready to publish
├── 5-veroeffentlicht/    # Published archive
└── referenzen/           # Inspiration, examples

Best for: Clear workflow, always know what's "in progress"

----------------------------------------------------
OPTION B: By Project (from your roadmap)
----------------------------------------------------
04-workspace/
├── ideen-bank/           # For: Content Ideen-Bank build
├── stories/              # For: Deine Story-Sammlung build
├── templates/            # For: Content Templates build
├── kalender/             # For: Content Kalender build
├── posts/                # All post drafts & final
└── tracking/             # Analytics & engagement

Best for: Each roadmap item has its home

----------------------------------------------------
OPTION C: Hybrid
----------------------------------------------------
04-workspace/
├── content/              # All content work
│   ├── ideen/
│   ├── entwuerfe/
│   └── fertig/
├── system/               # Your processes & templates
│   ├── templates/
│   └── workflows/
├── tracking/             # Analytics & progress
└── referenzen/           # Inputs & inspiration

Best for: Balance of workflow and organization
```

**Use AskUserQuestion**:
```
Question: "Which structure fits how you think?"
Header: "Workspace"
Options:
- "Option A: By Stage" - Clear workflow stages
- "Option B: By Project" - Matches your roadmap
- "Option C: Hybrid" - Flexible mix
- "Show me something else" - I'll customize
```

**If "Show me something else"**:
```
Tell me how you naturally organize things:
- By time? (this week, this month, archive)
- By type? (documents, images, data)
- By client/person?
- Something specific?

I'll create a custom structure.
```

**After selection, create the folders and workspace-map.md**

**Display**:
```
Created workspace structure
----------------------------------------------------

Your folders are ready in 04-workspace/

IMPORTANT: You can change this anytime.

Move files, add folders, reorganize however you want.
Then say "update workspace map" and I'll sync.

This is YOUR space. It grows with you.
```

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 6,
    "onboarding.quick_start_state.workspace_created": True,
    "first_encounters.workspace_used": True
})
```

---

## STEP 7/11: Your First Build (2 min)

**Display**:
```
STEP 7/11: Your First Build
----------------------------------------------------

{If roadmap exists:}
Your roadmap has {N} items. Let's start with the first one:

  → {first_roadmap_item}

{If context uploaded and has "Organize Initial Context":}
Note: You also have "Organize Initial Context" in your roadmap.
You can do that first, or start with {first_roadmap_item}.

{If no roadmap:}
Your GOAL is: {goal_summary}

Let's pick something concrete to build that moves you forward.

What can you build in Nexus?
  - Content      → Posts, guides, documentation
  - Strategy     → Plans, decisions, roadmaps
  - Research     → Analysis, synthesis, reports
  - Process      → Workflows, automations, systems
  - Software     → Features, tools, integrations
  - Skills       → Reusable workflows for later

----------------------------------------------------

WHY PLANNING MATTERS:

Plan well → execution will be (almost) perfect.

I'll ask questions that sharpen your thinking.
You'll discover what you actually want.

This is AI enhancing your critical thinking, not replacing it.
```

**If roadmap exists**:

**Use AskUserQuestion**:
```
Question: "Start with this?"
Options:
- "Yes, let's plan {first_item}"
- "Pick a different item from roadmap"
- "Something else entirely"
```

**If no roadmap**:

**Use AskUserQuestion** with DYNAMIC options based on goal:
```
Question: "Which feels like the right first step?"
Options:
- {BUILD idea 1} - {why}
- {BUILD idea 2} - {why}
- {BUILD idea 3} - {why}
- Other (tell me)
```

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 7,
    "onboarding.quick_start_state.build_chosen": True
})
```

---

## STEP 8/11: Plan the Build (IMPROVED) (3-4 min)

**CRITICAL CHANGE**: Load the actual plan-build skill instead of manually running questions.

**Display**:
```
STEP 8/11: Plan the Build
----------------------------------------------------

Now I'll load the planning workflow.

This will:
1. Ask discovery questions specific to your build type
2. Research best practices (if needed)
3. Create a detailed execution plan
4. Save everything to the build folder

Let's go!
```

**LOAD SKILL: plan-build**

```bash
uv run nexus-load --skill plan-build
```

**Pass context to plan-build**:
```python
# The plan-build skill needs to know:
# 1. Build name (from step 7)
# 2. Build type (detected from goal/name)
# 3. That this is onboarding (simplified mode)

# Plan-build will:
# 1. Create build structure with nexus-init-build
# 2. Run type-specific discovery
# 3. Generate plan and steps
# 4. Link to roadmap if applicable
```

**After plan-build completes**:

**Display**:
```
Planning complete!

Your build now has:
  - 01-overview.md (purpose & scope)
  - 02-discovery.md (your answers)
  - 03-plan.md (what we'll create)
  - 04-steps.md (execution roadmap)

See what happened? Every answer is now part of your build.
This is how Nexus compounds - input becomes persistent context.
```

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 8,
    "onboarding.quick_start_state.planning_complete": True,
    "first_encounters.build_created": True
})
```

---

## STEP 9/11: What You Built (1 min)

**Display**:
```
STEP 9/11: What You Built
----------------------------------------------------

Here's what you've created so far:

  ✓ Goal defined         → 01-memory/goals.md
  {If integrations:}
  ✓ Integrations noted   → Ready to connect
  {If roadmap:}
  ✓ Roadmap created      → 01-memory/roadmap.yaml
  ✓ Workspace ready      → 04-workspace/
  ✓ First build planned  → 02-builds/active/{name}/
  {If context:}
  ✓ Context analyzed     → 01-memory/input/

----------------------------------------------------

HOW NEXUS WORKS:

  One session = one focus.

  This session was PLANNING.
  Next session will be EXECUTION.

----------------------------------------------------

Almost done! Two more steps.
```

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 9
})
```

---

## STEP 10/11: Permissions Setup (1-2 min)

**Display**:
```
STEP 10/11: Permissions Setup
----------------------------------------------------

One last thing before we finish.

Nexus works best when I can read files, make edits, and run commands
without asking you each time. This is called "automatic" mode.

Here's what automatic mode allows:
  - Read any file in this project
  - Edit and create files
  - Run shell commands (git, npm, python, etc.)
  - Search the web for documentation

SAFEGUARDS (even in automatic mode):
  - I'll pause for important decisions (architecture, strategy, scope)
  - Destructive git commands are automatically blocked (force push, reset --hard)
  - I'll never commit without your explicit request
  - I won't touch sensitive files (.env, credentials, secrets)
  - Nexus hooks monitor for risky patterns and block them

Automatic mode means fewer interruptions, not zero oversight.
You stay in control of what matters.

You can change this anytime by editing .claude/settings.local.json
```

**Use AskUserQuestion**:
```
Question: "How should I handle permissions?"
Header: "Permissions"
Options:
- "Automatic (Recommended)" - I can work without interruptions. Best for productivity.
- "Ask each time" - I'll ask before every action. More control, more prompts.
```

### If user chose "Automatic":

**Check and create files**:

1. Check if `.claude/settings.local.json` exists
2. Check if `.vscode/settings.json` exists
3. Show what will be created/changed
4. Ask confirmation

**Create `.claude/settings.local.json`**:
```json
{
  "permissions": {
    "allow": ["Bash(*)", "Edit", "Write", "Read", "Glob", "Grep", "WebFetch", "WebSearch"]
  }
}
```

**Create/update `.vscode/settings.json`** (merge with existing if present):
```json
{
  "markdown.preview.breaks": true,
  "markdown.preview.typographer": true,
  "files.associations": {
    "*.md": "markdown"
  },
  "claudeCode.allowDangerouslySkipPermissions": true,
  "claudeCode.initialPermissionMode": "bypassPermissions"
}
```

**Create setup marker**: `.claude/.setup_complete`

### If user chose "Ask each time":

**Create only markdown preview settings** in `.vscode/settings.json`:
```json
{
  "markdown.preview.breaks": true,
  "markdown.preview.typographer": true,
  "files.associations": {
    "*.md": "markdown"
  }
}
```

**Create setup marker**: `.claude/.setup_complete`

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 10,
    "onboarding.quick_start_state.permissions_configured": True
})
```

---

## STEP 11/11: Start Fresh (IMPROVED) (1 min)

**Display summary**:
```
STEP 11/11: Start Fresh
----------------------------------------------------

Setup complete! Here's what you built:

  ✓ Goal defined         → 01-memory/goals.md
  {If integrations:}
  ✓ Integrations noted   → {list}
  {If roadmap:}
  ✓ Roadmap created      → 01-memory/roadmap.yaml ({N} items)
  ✓ Workspace ready      → 04-workspace/
  ✓ First build planned  → 02-builds/active/{name}/
  {If context:}
  ✓ Context analyzed     → 01-memory/input/
```

**Display IDE-specific restart instructions**:

```
----------------------------------------------------
TO START YOUR NEXT SESSION:
----------------------------------------------------

The permissions need a fresh session to activate.
Here's how to start a new session:

┌─────────────────────────────────────────────────┐
│  IN VS CODE:                                    │
│                                                 │
│  1. Click the "+" button in the Claude panel    │
│     (top right of this chat)                    │
│                                                 │
│     OR press: Cmd+Shift+P (Mac) / Ctrl+Shift+P │
│     Then type: "Claude: New Chat"               │
│                                                 │
│  2. In the new chat, type: Hi                   │
│                                                 │
│  That's it! I'll show your build, ready to go.  │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  IN TERMINAL:                                   │
│                                                 │
│  1. Type: exit                                  │
│     (or press Ctrl+C)                           │
│                                                 │
│  2. Start again: claude                         │
│                                                 │
│  3. Type: Hi                                    │
└─────────────────────────────────────────────────┘

----------------------------------------------------

WHAT HAPPENS NEXT:

When you say "Hi" in a new session:
  → I load your goals, roadmap, and active build
  → I show you where we left off
  → We start EXECUTING your first build

Your context is saved. Nothing is lost.
Every session picks up where we left off.

----------------------------------------------------

See you in the next session! 👋
```

**Save completion state**:
```python
from datetime import datetime
from nexus.state_writer import update_multiple_paths

update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 11,
    "onboarding.status": "complete",
    "onboarding.in_progress_skill": None,
    "onboarding.completed_at": datetime.now().isoformat(),
    "learning_tracker.completed.quick_start": True
})
```

---

## Post-Completion State

**Final state in user-config.yaml**:
```yaml
onboarding:
  status: "complete"
  path_chosen: "quick_start"
  language_preference: "en"
  started_at: "..."
  completed_at: "..."

  quick_start_state:
    step_completed: 11
    context_uploaded: true/false
    goal_captured: true
    integrations_selected: ["slack", "google"]  # NEW
    roadmap_created: true/false
    workspace_created: true
    build_chosen: true
    planning_complete: true
    permissions_configured: true

first_encounters:
  build_created: true
  workspace_used: true
  memory_updated: true
```

**Files Created**:
```
.claude/
  settings.local.json         # Permissions (if automatic)
  .setup_complete             # Marker file

.vscode/
  settings.json               # VS Code settings

01-memory/
  goals.md                    # PERMANENT (includes integrations section)
  roadmap.yaml                # PERMANENT (if created)
  input/                      # TEMPORARY (if files uploaded)
    {uploaded files}
    _analysis/                # SubAgent outputs (temporary)
      analysis-summary.md
      {theme}-insights.md

02-builds/
  active/
    {ID}-{name}/
      01-planning/
        01-overview.md
        02-discovery.md
        03-plan.md
        04-steps.md
        resume-context.md
      02-resources/
      03-working/
      04-outputs/

04-workspace/
  {folders based on selected proposal}/
  workspace-map.md
```

---

## Flow Summary

```
Step 0:  Welcome & Language
          ↓
Step 1:  How Nexus Works
          ↓
Step 2:  Context Upload (optional)
          ↓ informs
Step 3:  Your Goal
          ↓ informs
Step 4:  Integrations (NEW)          ← Ask about tools
          ↓ informs
Step 5:  Create Roadmap (optional)   ← Includes integrations
          ↓ informs
Step 6:  Your Workspace              ← Show concrete proposals
          ↓ informs
Step 7:  Your First Build (choose)
          ↓
Step 8:  Plan the Build              ← Load plan-build skill
          ↓
Step 9:  What You Built (summary)
          ↓
Step 10: Permissions Setup
          ↓
Step 11: Start Fresh                 ← Clear IDE instructions
```

**Key Changes from v1**:
1. **Step 4 (NEW)**: Integrations question - what tools to connect
2. **Step 6 (IMPROVED)**: Show 2-3 concrete workspace proposals
3. **Step 8 (IMPROVED)**: Load actual plan-build skill
4. **Step 11 (IMPROVED)**: IDE-specific session restart instructions

---

## Error Handling

| Issue | Solution |
|-------|----------|
| analyze-context fails | Log error, continue without context |
| create-roadmap fails | Log error, continue to workspace |
| plan-build fails | Fall back to manual questions |
| User gives vague goal | Ask clarifying question |
| Session compacts | Resume from step_completed + 1 |

---

## Implementation Notes

**Modular Skills**:
- `analyze-context` - File analysis (Step 2)
- `create-roadmap` - Roadmap creation (Step 5)
- `plan-build` - Build planning (Step 8) ← NEW
- All standalone, called from quick-start when needed

**Dynamic Generation**:
- All options generated from goal + context + roadmap
- Workspace proposals generated from goal/roadmap
- multiSelect: true where multiple answers make sense
- Always include "Other" option

**Language Support**:
- After Step 0, ALL content must be in user's chosen language
- Supported: en, de, es, fr, it, ja, zh, or custom

**Total Time**: ~15-20 minutes
- Step 0: 1 min (welcome + language)
- Step 1: 30 sec
- Step 2: 0-3 min (optional)
- Step 3: 2-3 min
- Step 4: 1-2 min (integrations) ← NEW
- Step 5: 0-3 min (optional)
- Step 6: 2-3 min (workspace proposals)
- Step 7: 2 min
- Step 8: 3-4 min (plan-build skill)
- Step 9: 1 min
- Step 10: 1-2 min
- Step 11: 1 min

---

*Quick Start v2.0 - Complete onboarding with integrations, proposals, and clear instructions*

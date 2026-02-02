---
name: quick-start
description: "Complete onboarding: welcome, language, goals, workspace, first BUILD, permissions."
onboarding: true
priority: critical
duration: "12-18 min"
cross_session_continuity: true
---

# Quick Start

Complete onboarding flow: welcome, language selection, optionally upload context, capture your goal, optionally create a roadmap, set up your workspace (informed by roadmap), plan your first BUILD, configure permissions.

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

## STEP 0/10: Welcome & Language (1 min)

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

  > Job Search
     Search 15 job boards every morning, prioritize matches,
     and generate tailored CVs from your stored stories.

  > Health System
     Talk to your fitness data, log meals from photos,
     get personalized training plans that adapt to your progress.

  > Content Engine
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

## STEP 1/10: How Nexus Works (30 sec)

**Display**:
```
STEP 1/10: How Nexus Works
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

## STEP 2/10: Context Upload (Optional) (2-3 min if used)

**Display**:
```
STEP 2/10: Context Upload (Optional)
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

## STEP 3/10: Your Goal (2-3 min)

**Display**:
```
STEP 3/10: Your Goal
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

## STEP 4/10: Create Roadmap (Optional) (2-3 min if used)

**Display**:
```
STEP 4/10: Create Roadmap (Optional)
----------------------------------------------------

Your goal: {goal_summary}

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
1. Suggest items based on goal + context
2. Let you add/remove/prioritize
3. Save to 01-memory/roadmap.md

The roadmap will inform your workspace structure.

After skill completes, continue to Step 5.
```

**If skipped, continue to Step 5**

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 4,
    "onboarding.quick_start_state.roadmap_created": True/False
})
```

---

## STEP 5/10: Your Workspace (2 min)

**Display**:
```
STEP 5/10: Your Workspace
----------------------------------------------------

Here's something important:

I'm going to generate A LOT of stuff for you.
Plans, content, research, documents, templates...

Without structure, you'll drown in AI output.

04-workspace/ is where YOUR outputs live.
It's navigatable by both you AND me.

Let's set it up based on {your roadmap / your goal}.
```

**STEP 5a: Ask structure preference**

**Use AskUserQuestion**:
```
Question: "How do you naturally organize things?"
Options:
- "By type" - drafts, final, references
- "By project" - separate folders per initiative
- "By stage" - inbox, working, done
- "Keep it simple" - minimal folders
```

**STEP 5b: Propose folders**

**If roadmap exists**: Use roadmap items to suggest folders
**If no roadmap**: Use goal to suggest folders

```
Example with roadmap items:
04-workspace/
├── content-calendar/        # For your Content Calendar build
├── client-templates/        # For your Client Templates build
├── research/                # For research outputs
└── references/              # Inspiration and inputs

Example without roadmap:
04-workspace/
├── drafts/                  # Work in progress
├── published/               # Final versions
└── references/              # Inputs and inspiration
```

**Use AskUserQuestion**:
```
Question: "Does this work?"
Options:
- "Yes, create it"
- "Tweak it"
- "Show different approach"
```

**After creating folders**:
```
Created workspace structure
----------------------------------------------------

IMPORTANT: You can change this anytime.

Move files, add folders, reorganize however you want.
Then say "update workspace map" and I'll sync.

This is YOUR space. It grows with you.
```

**Create workspace-map.md**

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 5,
    "onboarding.quick_start_state.workspace_created": True,
    "first_encounters.workspace_used": True
})
```

---

## STEP 6/10: Your First Build (2 min)

**Display**:
```
STEP 6/10: Your First Build
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

**Create BUILD structure**:
```
02-builds/{ID}-{name}/
├── 01-planning/
│   └── 01-overview.md
├── 02-resources/
├── 03-working/
└── 04-outputs/
```

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 6,
    "onboarding.quick_start_state.build_chosen": True,
    "first_encounters.build_created": True
})
```

---

## STEP 7/10: Plan the Build (3-4 min)

**Display**:
```
STEP 7/10: Plan the Build
----------------------------------------------------

Let me understand what we're building.

I'll ask a few questions. Each answer gets saved.
When we execute next session, I'll reference all of this.
```

**3 Rounds of questions** (DYNAMICALLY GENERATED):

### Round 1: Context
```
Question 1: "Who is this for?"
Question 2: "What problem does this solve?" (multiSelect: true)
```

### Round 2: Specifics
```
Question 3: "What's ONE example of what 'good' looks like?"
Question 4: "Any constraints?" (multiSelect: true)
```

### Round 3: Scope
```
Question 5: "What's the minimum viable version?"
Question 6: "What would be nice-to-have later?" (multiSelect: true)
```

**Generate planning documents**:
- `02-discovery.md`
- `03-plan.md`
- `04-steps.md`

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
    "onboarding.quick_start_state.step_completed": 7,
    "onboarding.quick_start_state.planning_complete": True
})
```

---

## STEP 8/10: What You Built (1 min)

**Display**:
```
STEP 8/10: What You Built
----------------------------------------------------

Here's what you've created so far:

  - Goal defined         → 01-memory/goals.md
  {If roadmap:}
  - Roadmap created      → 01-memory/roadmap.md
  - Workspace ready      → 04-workspace/
  - First build planned  → 02-builds/{name}/
  {If context:}
  - Context analyzed     → 01-memory/input/

----------------------------------------------------

HOW NEXUS WORKS:

  One session = one focus.

  This session was PLANNING.
  Next session will be EXECUTION.

----------------------------------------------------

Almost done! One more step to configure permissions.
```

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 8
})
```

---

## STEP 9/10: Permissions Setup (1-2 min)

**Display**:
```
STEP 9/10: Permissions Setup
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
    "onboarding.quick_start_state.step_completed": 9,
    "onboarding.quick_start_state.permissions_configured": True
})
```

---

## STEP 10/10: Start Fresh (30 sec)

**Display**:
```
STEP 10/10: Start Fresh
----------------------------------------------------

Setup complete! Here's what you built:

  - Goal defined         → 01-memory/goals.md
  {If roadmap:}
  - Roadmap created      → 01-memory/roadmap.md
  - Workspace ready      → 04-workspace/
  - First build planned  → 02-builds/{name}/
  {If context:}
  - Context analyzed     → 01-memory/input/

----------------------------------------------------

TO ACTIVATE AUTOMATIC MODE:

  1. Close this chat
  2. Open a new chat
  3. Type: Hi

The new session will have full permissions.
I'll show you your build, ready to execute.

All your progress is saved. Nothing is lost.

----------------------------------------------------

See you in the next session!
```

**Save completion state**:
```python
from datetime import datetime
from nexus.state_writer import update_multiple_paths

update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 10,
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
    step_completed: 10
    context_uploaded: true/false
    goal_captured: true
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
  goals.md                    # PERMANENT
  roadmap.md                  # PERMANENT (if created)
  input/                      # TEMPORARY (if files uploaded)
    {uploaded files}
    _analysis/                # SubAgent outputs (temporary)
      analysis-summary.md
      {theme}-insights.md

02-builds/
  {ID}-{name}/
    01-planning/
      01-overview.md
      02-discovery.md
      03-plan.md
      04-steps.md
    02-resources/
    03-working/
    04-outputs/

04-workspace/
  {folders based on roadmap or goal}/
  workspace-map.md
```

---

## Flow Summary

```
Step 0: Welcome & Language
         ↓
Step 1: How Nexus Works
         ↓
Step 2: Context Upload (optional)
         ↓ informs
Step 3: Your Goal
         ↓ informs
Step 4: Create Roadmap (optional)
         ↓ informs
Step 5: Your Workspace (uses roadmap for structure)
         ↓ informs
Step 6: Your First Build (from roadmap or goal)
         ↓
Step 7: Plan the Build
         ↓
Step 8: What You Built (summary)
         ↓
Step 9: Permissions Setup
         ↓
Step 10: Start Fresh (close → new chat)
```

**Key insight**: Welcome + language first ensures all content is in user's language.
**Key insight**: Roadmap before Workspace means folder structure reflects what you're building.
**Key insight**: Permissions at end ensures new chat has full automatic mode.

---

## Error Handling

| Issue | Solution |
|-------|----------|
| analyze-context fails | Log error, continue without context |
| create-roadmap fails | Log error, continue to workspace |
| User gives vague goal | Ask clarifying question |
| Session compacts | Resume from step_completed + 1 |

---

## Implementation Notes

**Modular Skills**:
- `analyze-context` - File analysis (Step 2)
- `create-roadmap` - Roadmap creation (Step 4)
- Both standalone, called from quick-start when needed

**Dynamic Generation**:
- All options generated from goal + context + roadmap
- multiSelect: true where multiple answers make sense
- Always include "Other" option

**Language Support**:
- After Step 0, ALL content must be in user's chosen language
- Supported: en, de, es, fr, it, ja, zh, or custom

**Total Time**: ~12-18 minutes
- Step 0: 1 min (welcome + language)
- Step 1: 30 sec
- Step 2: 0-3 min (optional)
- Step 3: 2-3 min
- Step 4: 0-3 min (optional)
- Step 5: 2 min
- Step 6: 2 min
- Step 7: 3-4 min
- Step 8: 1 min
- Step 9: 1-2 min
- Step 10: 30 sec

---

*Quick Start - the complete onboarding path for Nexus*

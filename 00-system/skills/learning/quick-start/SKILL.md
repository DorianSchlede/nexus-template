---
name: quick-start
description: "Quick 10-15 minute start: optional context upload, goal, optional roadmap, workspace, first BUILD."
onboarding: true
priority: critical
duration: "10-15 min"
cross_session_continuity: true
---

# Quick Start

Onboarding flow: optionally upload context, capture your goal, optionally create a roadmap, set up your workspace (informed by roadmap), and plan your first BUILD.

**New Flow**: Roadmap comes BEFORE workspace, so your roadmap items can inform folder structure.

---

## Pre-Execution

**IMPORTANT**: This skill assumes language selection is already complete (handled by startup_first_run.md).

**State Initialization**:
```python
from nexus.state_writer import update_multiple_paths
from datetime import datetime

update_multiple_paths(config_path, {
    "onboarding.status": "in_progress",
    "onboarding.path_chosen": "quick_start",
    "onboarding.in_progress_skill": "quick-start",
    "onboarding.started_at": datetime.now().isoformat()
})
```

---

## Resume Logic

If resuming from compaction, check `onboarding.quick_start_state.step_completed` and resume from step + 1.

```python
def get_resume_step():
    step_completed = config.onboarding.quick_start_state.step_completed
    return step_completed + 1
```

---

## STEP 0/7: How Nexus Works (30 sec)

**Display**:
```
STEP 0/7: How Nexus Works
----------------------------------------------------

Here's the key idea:

This Nexus folder IS your project. Everything lives here.
I remember what we work on. You never start from zero.

  01-memory/     → Your context (I pre-load this every session)
  02-builds/     → Where we plan and build things together
  03-skills/     → Your process automations
  04-workspace/  → Your outputs and files

No accounts. No cloud. The whole system is just this folder.
Close the chat, come back tomorrow - I pick up where we left off.

Ready?
```

**Wait for confirmation**

---

## STEP 1/7: Context Upload (Optional) (2-3 min if used)

**Display**:
```
STEP 1/7: Context Upload (Optional)
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

After skill completes, continue to Step 2.
```

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 1,
    "onboarding.quick_start_state.context_uploaded": True/False
})
```

---

## STEP 2/7: Your Goal (2-3 min)

**Display**:
```
STEP 2/7: Your Goal
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
    "onboarding.quick_start_state.step_completed": 2,
    "onboarding.quick_start_state.goal_captured": True,
    "first_encounters.memory_updated": True
})
```

---

## STEP 3/7: Create Roadmap (Optional) (2-3 min if used)

**Display**:
```
STEP 3/7: Create Roadmap (Optional)
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

After skill completes, continue to Step 4.
```

**If skipped, continue to Step 4**

**Save state**:
```python
update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 3,
    "onboarding.quick_start_state.roadmap_created": True/False
})
```

---

## STEP 4/7: Your Workspace (2 min)

**Display**:
```
STEP 4/7: Your Workspace
----------------------------------------------------

Here's something important:

I'm going to generate A LOT of stuff for you.
Plans, content, research, documents, templates...

Without structure, you'll drown in AI output.

04-workspace/ is where YOUR outputs live.
It's navigatable by both you AND me.

Let's set it up based on {your roadmap / your goal}.
```

**STEP 4a: Ask structure preference**

**Use AskUserQuestion**:
```
Question: "How do you naturally organize things?"
Options:
- "By type" - drafts, final, references
- "By project" - separate folders per initiative
- "By stage" - inbox, working, done
- "Keep it simple" - minimal folders
```

**STEP 4b: Propose folders**

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
    "onboarding.quick_start_state.step_completed": 4,
    "onboarding.quick_start_state.workspace_created": True,
    "first_encounters.workspace_used": True
})
```

---

## STEP 5/7: Your First Build (2 min)

**Display**:
```
STEP 5/7: Your First Build
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
    "onboarding.quick_start_state.step_completed": 5,
    "onboarding.quick_start_state.build_chosen": True,
    "first_encounters.build_created": True
})
```

---

## STEP 6/7: Plan the Build (3-4 min)

**Display**:
```
STEP 6/7: Plan the Build
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
    "onboarding.quick_start_state.step_completed": 6,
    "onboarding.quick_start_state.planning_complete": True
})
```

---

## STEP 7/7: What's Next (1 min)

**Display**:
```
STEP 7/7: What's Next
----------------------------------------------------

Here's what you built:

  - Goal defined         → 01-memory/goals.md
  {If roadmap:}
  - Roadmap created      → 01-memory/roadmap.md
  - Workspace ready      → 04-workspace/
  - First build planned  → 02-builds/{name}/
  {If context:}
  - Context analyzed     → 01-memory/input/ (temporary, organize next)

----------------------------------------------------

HOW NEXUS WORKS:

  One session = one focus.

  This session was PLANNING.
  Next session will be EXECUTION.

----------------------------------------------------

WHAT TO DO NOW:

  1. Close this chat
  2. Open a new chat
  3. Type: Hi

That's it. I'll show you your build, ready to execute.

All your progress is saved. Nothing is lost.
You'll pick up exactly where we left off.

----------------------------------------------------

See you in the next session!
```

**Save completion state**:
```python
from datetime import datetime
from nexus.state_writer import update_multiple_paths

update_multiple_paths(config_path, {
    "onboarding.quick_start_state.step_completed": 7,
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
  started_at: "..."
  completed_at: "..."

  quick_start_state:
    step_completed: 7
    context_uploaded: true/false
    goal_captured: true
    roadmap_created: true/false
    workspace_created: true
    build_chosen: true
    planning_complete: true

first_encounters:
  build_created: true
  workspace_used: true
  memory_updated: true
```

**Files Created**:
```
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
Step 0: How Nexus Works
         ↓
Step 1: Context Upload (optional)
         ↓ informs
Step 2: Your Goal
         ↓ informs
Step 3: Create Roadmap (optional)
         ↓ informs
Step 4: Your Workspace (uses roadmap for structure)
         ↓ informs
Step 5: Your First Build (from roadmap or goal)
         ↓
Step 6: Plan the Build
         ↓
Step 7: What's Next
```

**Key insight**: Roadmap before Workspace means folder structure reflects what you're building.

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
- `analyze-context` - File analysis (Step 1)
- `create-roadmap` - Roadmap creation (Step 3)
- Both standalone, called from quick-start when needed

**Dynamic Generation**:
- All options generated from goal + context + roadmap
- multiSelect: true where multiple answers make sense
- Always include "Other" option

**Total Time**: ~10-15 minutes
- Step 0: 30 sec
- Step 1: 0-3 min (optional)
- Step 2: 2-3 min
- Step 3: 0-3 min (optional)
- Step 4: 2 min
- Step 5: 2 min
- Step 6: 3-4 min
- Step 7: 1 min

---

*Quick Start - the main onboarding path for Nexus*

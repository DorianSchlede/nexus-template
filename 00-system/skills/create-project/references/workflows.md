# create-project Workflows

Complete workflows for both workspace setup and project creation modes.

---

## Table of Contents

### Workspace Setup Workflow
- [Step WS-1: Load User Context](#step-ws-1-load-user-context)
- [Step WS-2: Suggest Folder Structure](#step-ws-2-suggest-folder-structure)
- [Step WS-3: Iterate on Structure](#step-ws-3-iterate-on-structure)
- [Step WS-4: Create User-Folders Structure](#step-ws-4-create-user-folders-structure)
- [Step WS-5: Update project-map.md](#step-ws-5-update-project-mapmd)
- [Step WS-6: Completion Message](#step-ws-6-completion-message)
- [Step WS-7: Auto-Trigger close-session](#step-ws-7-auto-trigger-close-session)

### Project Creation Workflow
- [Step 1: Initialize TodoList](#step-1-initialize-todolist)
- [Step 2: Initial Discovery](#step-2-initial-discovery)
- [Step 3: Validate Inputs](#step-3-validate-inputs)
- [Step 4: Create Folder Structure](#step-4-create-folder-structure)
- [Step 5: Fill overview.md](#step-5-fill-overviewmd-quick)
- [Step 6: INTERACTIVE - requirements.md](#step-6-️-interactive---requirementsmd)
- [Step 7: INTERACTIVE - design.md](#step-7-️-interactive---designmd)
- [Step 8: INTERACTIVE - tasks.md](#step-8-️-interactive---tasksmd)
- [Step 9: Update project-map.md](#step-9-update-project-mapmd)
- [Step 10: Display Complete Structure](#step-10-display-complete-project-structure)
- [Step 11: CRITICAL - Separate Session](#step-11-️-critical-instruction---separate-session)
- [Step 12: Auto-Trigger close-session](#step-12-auto-trigger-close-session)

---

# Workspace Setup Workflow

**Purpose**: Create initial User-Folders/ structure based on user's work context.

**Time Estimate**: 10-15 minutes

---

## Step WS-1: Load User Context

**CRITICAL**: Load 01-memory/goals.md FIRST before asking any questions.

```markdown
Loading your goals and work context...
```

Read `01-memory/goals.md` and extract:
- Role / Primary Focus
- Work Organization Pattern
- Workload (number of active work streams)
- Key Challenge
- Success Criteria
- Goals (short-term and long-term)

**Context Loaded Confirmation**:
```markdown
✓ Loaded your context:
  - Role: {role from goals.md}
  - Work Pattern: {organization pattern}
  - Workload: {X} active work streams
  - Key Challenge: {challenge from goals.md}
```

---

## Step WS-2: Suggest Folder Structure

Based on loaded context, suggest folder structure. Use mental model: **Systems Thinking** (organize by function/domain).

**Display to User**:
```markdown
Based on your work context, I can see you're {role description} managing {X} work streams
focused on {key areas from goals}.

Let me suggest a folder structure that matches how you work:

User-Folders/
├── {folder-name-1}/  # {Purpose based on user's work}
├── {folder-name-2}/  # {Purpose based on user's work}
├── {folder-name-3}/  # {Purpose based on user's work}
└── _archive/         # Completed or inactive items

---

This structure is based on:
- Your work pattern: {organization pattern from goals.md}
- Your workload: {X} streams needing separation
- Your goals: {relevant goal connection}

Does this structure work for you? Feel free to:
- Add folders that are missing
- Remove folders you don't need
- Rename anything to match your terminology
- Suggest a completely different structure

What would you like to adjust?
```

**Important Heuristics for Suggestions**:
- **Client-focused work**: Suggest `Clients/`, `Projects/`, `Proposals/`
- **Product work**: Suggest `Features/`, `Roadmap/`, `Research/`
- **Management**: Suggest `Team/`, `1-on-1s/`, `Planning/`
- **Creative work**: Suggest `Ideas/`, `Drafts/`, `Published/`
- **Consulting**: Suggest `Engagements/`, `Deliverables/`, `Templates/`
- **Generic fallback**: Suggest `Active/`, `Planning/`, `Reference/`, `_archive/`

**Always include**: `_archive/` for completed items

---

## Step WS-3: Iterate on Structure

**IF** user provides feedback:
- Listen to suggested changes
- Ask clarifying questions if needed
- Present updated structure
- Pause for review
- Repeat until user confirms

**IF** user says "looks good" / "this works" / "let's go":
- Confirm: "Perfect! Creating your workspace structure..."
- Proceed to Step WS-4

---

## Step WS-4: Create User-Folders Structure

Create the confirmed folder structure:

```bash
mkdir -p User-Folders/{folder1} User-Folders/{folder2} ... User-Folders/_archive
```

Add `.gitkeep` files to each folder:
```bash
touch User-Folders/{folder1}/.gitkeep User-Folders/{folder2}/.gitkeep ...
```

**Display Confirmation**:
```markdown
✅ Workspace Created!

📁 User-Folders/
├── 📂 {folder1}/ ✓
├── 📂 {folder2}/ ✓
├── 📂 {folder3}/ ✓
└── 📂 _archive/ ✓

All folders created with .gitkeep files for git tracking.

---

Your workspace is ready! You can now:
- Add files to any folder
- Create subfolders as needed
- Use _archive/ for completed items
- Ask me to "organize files" or "create project" anytime
```

---

## Step WS-5: Update project-map.md

Load `02-projects/project-map.md` and update the "Current Focus" section:

```markdown
## Current Focus

Workspace setup complete! Ready for real work.
Last session: {current_timestamp}
```

Write updated `02-projects/project-map.md`.

---

## Step WS-6: Completion Message

Display:
```markdown
🎉 Workspace Setup Complete!

Your User-Folders/ structure is now ready based on your work context.

---

**What happens next?**

You're now fully operational! In your next session:
- Say "create project" to plan new work
- Say "organize files" to structure existing work
- Say "what's next" to see current priorities
- Or just start working—Nexus will guide you!

---

Ready to close this session and save everything?
```

**Wait for user acknowledgment**, then proceed to Step WS-7.

---

## Step WS-7: Auto-Trigger close-session

Auto-trigger the `close-session` skill to save progress.

**Format**:
```markdown
Auto-triggering close-session to save your workspace...

[close-session workflow executes]

✅ Session saved! Your workspace is ready.

See you next time—ready to do real work! 🚀
```

---

# Project Creation Workflow

**Purpose**: Full collaborative project planning (20-30 minutes)

**When to use**: When `User-Folders/` exists and user wants to create a new project.

---

## Step 1: Initialize TodoList

Create TodoWrite with all workflow steps:
```
- [ ] Initial discovery
- [ ] Validate inputs
- [ ] Create folder structure
- [ ] Fill overview.md
- [ ] Interactive requirements.md (with pause)
- [ ] Interactive design.md (with pause)
- [ ] Interactive tasks.md (with pause)
- [ ] Update 02-projects/project-map.md
- [ ] Display complete structure
- [ ] Instruct separate session execution
- [ ] Auto-trigger close-session
```

This creates transparency and allows progress tracking during project creation.

**Mark tasks complete as you finish each step throughout this workflow.**

---

## Step 2: Initial Discovery

Ask user:

**Question 1**: "What's this project about?" (1-2 sentences)
- Capture user's response
- Summarize understanding

**Question 2**: "What would you like to call this project?"
- Suggest ID based on existing projects in 02-projects/project-map.md
  - Example: If highest project ID is 05, suggest 06
  - If no projects yet (only onboarding), suggest 05
- Suggest name format: lowercase-with-hyphens
- Example: "I'd suggest: `06-client-proposal-system`. Sound good?"
- User confirms or provides alternative

**Important**: Be conversational and collaborative, not robotic!

---

## Step 3: Validate Inputs

Check:
- [ ] ID is numeric, zero-padded (00, 01, ..., 10, 11, ...)
- [ ] Name is lowercase-with-hyphens format
- [ ] Name is unique (check against 02-projects/project-map.md)
- [ ] Project folder doesn't already exist in Projects/

**If validation fails**:
- Explain issue clearly
- Suggest correction
- Ask for revised input

**If validation passes**:
- Confirm: "Perfect! Creating project `{ID}-{name}`..."

---

## Step 4: Create Folder Structure

Create:
```
Projects/{ID}-{name}/
├── /planning
│   ├── overview.md
│   ├── requirements.md
│   ├── design.md
│   └── tasks.md
└── /outputs
    └── .gitkeep
```

Confirm creation:
```
✓ Created Projects/{ID}-{name}/
✓ Created /planning folder
✓ Created /outputs folder
```

---

## Step 5: Fill overview.md (Quick)

Write `Projects/{ID}-{name}/planning/overview.md` with YAML frontmatter and basic content.

Confirm: "✓ overview.md created"

---

## Step 6: ⚠️ INTERACTIVE - requirements.md

**Load Mental Models**: Read `mental-models.md`

**Offer Mental Models to User** (let them pick!):

Based on project type, offer 2-3 relevant models. See [mental-models.md](mental-models.md) for complete catalog.

**Elicitation Process**:
1. Ask opening questions from selected mental model
2. Listen to user responses
3. Ask deepening and clarifying questions
4. Probe on unclear areas
5. Validate understanding
6. Continue until comprehensive understanding

**Collaborative Writing**:
1. Draft requirements.md based on elicitation
2. Present draft to user

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛑 MANDATORY PAUSE - DO NOT SKIP! 🛑
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**STOP HERE** - User must review before proceeding!

```
Here's the requirements document based on our discussion:

[Display requirements.md content in full]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Let's review this together. Does this capture everything?

Take your time to read through. Let me know:
- Does this accurately reflect what you need?
- Is anything missing?
- Should anything be changed or clarified?
- Are you happy with this?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQUIRED: Reply with your feedback, or say "this looks good" to proceed.

DO NOT CONTINUE until user confirms satisfaction!
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Iteration Loop**:
- **IF** user provides feedback: Make changes, present updated version, pause again
- **IF** user confirms: Write final version, proceed to Step 7

---

## Step 7: ⚠️ INTERACTIVE - design.md

Same collaborative process as Step 6:
1. Offer mental models
2. User picks model(s)
3. Elicitation process
4. Draft design.md
5. MANDATORY PAUSE for user review
6. Iteration until confirmed
7. Write final version

---

## Step 8: ⚠️ INTERACTIVE - tasks.md

Same collaborative process as Step 6:
1. Offer mental models
2. User picks model(s)
3. Elicitation process
4. Draft tasks.md with checkboxes
5. MANDATORY PAUSE for user review
6. Iteration until confirmed
7. Write final version

---

## Step 9: Update project-map.md

Load `02-projects/project-map.md` and update:

1. Count tasks from tasks.md (total checkboxes)
2. Add project entry to Active Projects section
3. Update Current Focus section
4. Update "Last Updated" timestamp

Write updated file.

---

## Step 10: Display Complete Project Structure

Show user the complete structure:

```
✅ Project Created Successfully!

📁 Projects/{ID}-{name}/
├── 📂 planning/
│   ├── ✓ overview.md
│   ├── ✓ requirements.md
│   ├── ✓ design.md
│   └── ✓ tasks.md
└── 📂 outputs/
    └── (deliverables will go here)

---

Status: PLANNING
Total Tasks: {X}
Estimated Time: {from tasks.md}

---

All planning documents are ready! 📋
```

---

## Step 11: ⚠️ CRITICAL INSTRUCTION - Separate Session

Display this message:

```
🎯 IMPORTANT: Context Management Best Practice

This project is now fully planned and ready to execute.

To maintain clean context boundaries and better focus, please work
on this project in a SEPARATE SESSION (not right now).

Why separate sessions?
- Clean mental context for execution
- Better focus without planning overhead
- Proper memory management (close-session preserves state)
- Easier to pause and resume work

---

What to do next:

1. Close this session: Say "done for now" or "close session"
2. Return later: Load Nexus and say "continue working" or "work on {project-name}"
3. System will resume: Loads your project and shows the first task

This ensures your work sessions stay focused and organized!

---

Ready to close this session?
```

**Wait for user acknowledgment** before proceeding to Step 12.

---

## Step 12: Auto-Trigger close-session

Auto-trigger the `close-session` skill to:
- Update 02-projects/project-map.md with final state
- Create session report
- Clean up temporary files
- Display session summary

**Format**:
```
Auto-triggering close-session skill to save your progress...

[close-session workflow executes]

Session saved! ✅

See you next time when you're ready to work on {project-name}! 🚀
```

---

**END OF WORKFLOWS**

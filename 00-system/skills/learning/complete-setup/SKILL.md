---
name: setup-system
description: "Set up your Nexus system: goals, roadmap, workspace, projects. 10-15 min."
onboarding: true
priority: critical
duration: "10-15 min"
cross_session_continuity: true
---

# Setup System

Initialize your Nexus system with goals, roadmap, workspace structure, and project scaffolds.

---

## Pre-Execution

**CRITICAL**: Before showing Step 1, automatically create the onboarding project:

```python
def initialize_setup_system():
    # Create onboarding project structure
    create_folder("02-builds/00-onboarding-session/01-planning/")
    create_folder("02-builds/00-onboarding-session/02-resources/")
    create_folder("02-builds/00-onboarding-session/03-working/")
    create_folder("02-builds/00-onboarding-session/04-outputs/")

    # Create overview
    write_file("02-builds/00-onboarding-session/01-planning/01-overview.md", OVERVIEW_CONTENT)

    # Create steps tracker
    write_file("02-builds/00-onboarding-session/01-planning/04-steps.md", STEPS_CONTENT)

    # Create symlink for input files
    symlink("04-workspace/input/", "02-builds/00-onboarding-session/03-working/input/")

    # Set active build
    set_active_build("00-onboarding-session")
```

---

## Resume Logic

If resuming from compaction, check `onboarding.setup_system_state.step_completed` and resume from step + 1.

```python
def get_resume_step():
    step_completed = config.onboarding.setup_system_state.step_completed
    return step_completed + 1  # Resume from next incomplete step
```

---

## STEP 1: Context Upload (Optional)

**Display**:
```
STEP 1/7: Context Upload (Optional)

Want to upload files for me to learn about you?
(Documents, code, data, spreadsheets - anything relevant)

You can:
1. Upload files now
2. Skip this step

If you upload files, I'll analyze them to understand:
- What you work on
- Potential systems to build
- Integration opportunities
- How to organize your workspace

Choose 1 or 2:
```

**If user chooses 1 (upload)**:
```
Great! Upload your files to: 04-workspace/input/

You can drag and drop multiple files.
When you're done, let me know and I'll analyze them.

(This might take 1-2 minutes depending on file count)
```

Then trigger SubAgent analysis (see SubAgent section below).

**If user chooses 2 (skip)**:
```python
update_config({
    "onboarding.setup_system_state.step_completed": 1,
    "onboarding.setup_system_state.files_uploaded": False
})
```

Continue to Step 2.

---

## STEP 2: Define Your Goals

**Display**:
```
STEP 2/7: Define Your Goals

Who are you, OR what do you want to achieve/build with this system?

You can answer:
- Your role: "I'm a sales consultant in B2B SaaS..."
- Your goal: "I want to automate proposal generation..."
- Both: "I'm a PM and I want to build a product roadmap system..."

Tell me about yourself or your goal:
```

**AI Extracts**:
- Role (if mentioned or inferred)
- Short-term goal (3-6 months, specific)
- Long-term vision (1-3 years, if mentioned)
- System type (sales, content, research, product, client, etc.)
- Work patterns (what they do regularly)

**Follow-up if needed**:
- If no short-term goal: "What's your main goal for the next 3-6 months?"
- If no long-term vision: "(Optional) What's your 1-3 year vision? (or 'skip')"

**State Update**:
```python
update_config({
    "onboarding.setup_system_state.step_completed": 2,
    "onboarding.setup_system_state.role_captured": True,
    "onboarding.setup_system_state.goals_captured": True
})
```

---

## STEP 3: Generate Roadmap

**Display**:
```
STEP 3/7: Your Roadmap

Based on what you've told me, here's what I think you should build:
```

**AI Generates Roadmap**:
- 3-7 items (builds, skills, integrations)
- Each item has: name, type, priority, dependencies, rationale
- Ordered by dependencies (foundational items first)

**Display Format**:
```
ROADMAP:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. Sales Playbook (BUILD)
   Priority: high
   → Foundation for all sales automation - captures your methodology

2. Proposal Generator (SKILL)
   Priority: high (after: Sales Playbook)
   → Automates proposal creation using your playbook as template

3. HubSpot CRM Integration (INTEGRATION)
   Priority: medium (after: Proposal Generator)
   → Pulls client data automatically for proposals

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**User Confirmation**:
```
Looks good? (yes/add item/remove item/change priority)
```

Allow user to modify roadmap before continuing.

**State Update**:
```python
update_config({
    "onboarding.setup_system_state.step_completed": 3,
    "onboarding.setup_system_state.roadmap_created": True
})
```

---

## STEP 4: Create Workspace Structure

**Display**:
```
STEP 4/7: Workspace Structure

Based on your roadmap, here's your suggested folder structure:
```

**Generate folders from**:
- File analysis themes (if files uploaded)
- Roadmap item themes (if no files)

**Display Format**:
```
WORKSPACE STRUCTURE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

04-workspace/
├── clients/
│   ├── acme/
│   ├── beta/
│   → Client project files organized by company
├── sales/
│   ├── playbooks/
│   ├── templates/
│   → Sales materials and templates
├── research/
│   → Market research and competitive intelligence

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Good? (yes/modify)
```

**Actions**:
1. Create all folders
2. Move files from input/ to organized folders (if files uploaded)
3. Generate workspace-map.md

**State Update**:
```python
update_config({
    "onboarding.setup_system_state.step_completed": 4,
    "onboarding.setup_system_state.workspace_created": True
})
```

---

## STEP 5: Initiate Projects

**Display**:
```
STEP 5/7: Initiating Projects

Creating project scaffolds...
```

**For each roadmap item**:
1. Generate project_id (e.g., "01-sales-playbook")
2. Create 4 folders: 01-planning, 02-resources, 03-working, 04-outputs
3. Generate overview.md with AI (purpose, success criteria, context)
4. Create empty templates: discovery.md, plan.md, steps.md
5. Create resume-context.md with dependencies

**Display progress**:
```
  ✓ Created: 01-sales-playbook
  ✓ Created: 02-proposal-generator
  ✓ Created: 03-hubspot-integration
```

**State Update**:
```python
update_config({
    "onboarding.setup_system_state.step_completed": 5,
    "onboarding.setup_system_state.projects_initiated": True
})
```

---

## STEP 6: Save Everything

**Display**:
```
STEP 6/7: Saving Your System

Saving all configuration...
```

**Actions**:
1. Save goals.md to 01-memory/
2. Save roadmap.md to 01-memory/
3. workspace-map.md already in 04-workspace/
4. Copy outputs to onboarding project (for archive)
5. Archive onboarding project to 05-archived/

**State Update**:
```python
update_config({
    "onboarding.status": "system_setup_complete",
    "onboarding.setup_system_state.step_completed": 6,
    "onboarding.in_progress_skill": null,
    "learning_tracker.completed.setup_memory": true,
    "learning_tracker.completed.create_folders": true,
    "learning_tracker.completed.create_roadmap": true
})
```

---

## STEP 7: End Session

**Display**:
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SETUP COMPLETE ✓
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Your Nexus system is initialized!

Created:
✓ goals.md (your context, loaded every session)
✓ roadmap.md (your plan with X projects)
✓ workspace-map.md (your folder structure)
✓ X project scaffolds (ready to start)

Your progress saves automatically.

IMPORTANT: Clean session boundaries matter in Nexus.
Each session = one focus.

This session: System setup (DONE)
Next session: Start your first build

→ Open a NEW chat/session when ready to continue
```

---

## SubAgent File Analysis

When user uploads files in Step 1:

### KB-Based Agent Assignment

```python
def calculate_agent_count(total_kb):
    if total_kb < 1000:      return 1
    elif total_kb < 3000:    return 2
    elif total_kb < 5000:    return 3
    elif total_kb < 10000:   return 5
    elif total_kb < 20000:   return 8
    else:                    return min(ceil(total_kb / 2500), 10)
```

### Auto-File-Splitting

Files >2MB are split into chunks of max 1.5MB with 50-line overlap.

### Thematic Clustering

Pattern matching on filenames:
- "client"/"customer" → clients
- "sales"/"proposal" → sales
- "research"/"paper" → research
- "financial"/"invoice" → finance
- .py/.js/.ts → code
- Everything else → general

Show clusters to user for confirmation.

### SubAgent Prompt

Use prompt at: `00-system/core/nexus/prompts/subagent-file-analysis.md`

### Synthesis

After all SubAgents complete:
1. Combine all file_analyses arrays
2. Merge professional_context (take most detailed)
3. Dedupe integration_opportunities by (name, type)
4. Merge workspace_structure_suggestion folders

Save to:
- `02-builds/00-onboarding-session/02-resources/file-analysis.json`
- `02-builds/00-onboarding-session/02-resources/file-analysis-summary.md`

---

## Error Handling

| Issue | Solution |
|-------|----------|
| No files in input/ | Continue to Step 2 |
| SubAgent timeout | Retry with smaller batches |
| User abandons mid-skill | State preserved via step_completed |
| Session compaction | Resume from step_completed + 1 |

---

## State Management

Track granular progress for cross-session continuity:

```yaml
onboarding:
  setup_system_state:
    step_completed: 0-7
    files_uploaded: boolean
    file_analysis_done: boolean
    role_captured: boolean
    goals_captured: boolean
    roadmap_created: boolean
    workspace_created: boolean
    projects_initiated: boolean
```

This enables resume from any step if session compacts mid-skill.

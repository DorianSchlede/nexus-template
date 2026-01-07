# plan-project Workflows

Complete workflows for workspace setup and router-based project creation.

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

### Project Creation Workflow (Router Pattern)
- [Phase 1: Type Detection & Setup](#phase-1-type-detection--setup)
- [Phase 2: Discovery](#phase-2-discovery)
- [Phase 3: Mental Models](#phase-3-mental-models)
- [Phase 4: Re-Discovery](#phase-4-re-discovery-if-needed)
- [Phase 5: Finalization](#phase-5-finalization)
- [Phase 6: Close Session](#phase-6-close-session)

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
Workspace Created!

User-Folders/
├── {folder1}/ ✓
├── {folder2}/ ✓
├── {folder3}/ ✓
└── _archive/ ✓

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
Workspace Setup Complete!

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

Session saved! Your workspace is ready.

See you next time—ready to do real work!
```

---

# Project Creation Workflow (Router Pattern)

**Purpose**: Full collaborative project planning with mandatory router.

**Time Estimate**: 20-30 minutes

**Key Principle**: Discovery BEFORE Mental Models

---

## Phase 1: Type Detection & Setup

### Step 1.1: Initialize TodoList

Create TodoWrite with router workflow phases:
```
- [ ] Type detection
- [ ] Project setup (init_project.py)
- [ ] Discovery (skill-based or inline)
- [ ] Mental models (after discovery)
- [ ] Re-discovery (if gaps found)
- [ ] Finalization (plan.md, steps.md)
- [ ] Update resume-context.md
- [ ] Close session
```

### Step 1.2: Detect Project Type

**Read all _type.yaml files**:
```bash
# AI reads templates/types/*/_type.yaml descriptions
```

**Semantic Matching**:
- Compare user input against each type's description
- Select best match OR ask user to choose if ambiguous

**Type Detection Table**:

| Type | Description Pattern | Discovery Method |
|------|---------------------|------------------|
| build | software, feature, tool, system | Inline |
| integration | API, webhook, external service | Skill: add-integration |
| research | papers, academic, systematic review | Skill: create-research-project |
| strategy | business decision, planning, analysis | Inline |
| content | marketing, documentation, creative | Inline |
| process | workflow, automation, optimization | Inline |
| skill | Nexus skill, automation capability | Skill: create-skill |
| generic | anything else | Inline |

**If ambiguous**, ask user:
```markdown
I detected this could be a few different project types:

1. **Build** - Creating software/tools
2. **Integration** - Connecting external APIs

Which type best matches what you're building?
```

### Step 1.3: Create Project Structure

```bash
python 00-system/skills/projects/plan-project/scripts/init_project.py \
  "Project Name" --type {detected_type} --path 02-projects
```

**Output**:
```
02-projects/{ID}-{name}/
├── 01-planning/
│   ├── 01-overview.md     (from type template)
│   ├── 02-discovery.md    (from type template)
│   ├── 03-plan.md         (from type template)
│   ├── 04-steps.md        (from type template)
│   └── resume-context.md  (initialized)
├── 02-resources/
├── 03-working/
└── 04-outputs/
```

### Step 1.4: Initialize Resume Context

Write initial resume-context.md:
```yaml
---
session_ids: ["{current_session_id}"]
project_id: "{ID}-{name}"
project_name: "{Human Readable Name}"
current_phase: "planning"

next_action: "plan-project"
files_to_load:
  - "01-planning/02-discovery.md"

rediscovery_round: 0
discovery_complete: false

current_section: 1
tasks_completed: 0
---
```

---

## Phase 2: Discovery

**CRITICAL**: Discovery MUST complete before mental models.

### Check Discovery Method

Read `templates/types/{type}/_type.yaml`:

```yaml
discovery:
  skill: add-integration  # If present → skill-based
  inline: true            # If true → inline discovery
```

### Skill-Based Discovery (integration, research, skill)

```bash
# Update resume-context.md
current_skill: "add-integration"

# Load skill normally
python 00-system/core/nexus-loader.py --skill add-integration
```

**Skill runs its workflow**:
- add-integration: WebSearch for API docs, endpoint selection
- create-research-project: Paper search, RQ definition
- create-skill: Skill-worthiness check, scaffolding

**Skill writes findings to**:
```
{project}/01-planning/02-discovery.md
```

**When skill completes**:
```yaml
# Clear skill from resume
current_skill: ""
discovery_complete: true
```

### Inline Discovery (build, strategy, content, process, generic)

**Load discovery template**:
```bash
# Read templates/types/{type}/discovery.md
```

**Ask discovery questions interactively**:

For **build** type (EARS requirements):
```markdown
Let's define the requirements for your project.

**What should the system DO?**
(I'll help format these as EARS requirements)

Example: "The API should validate user input"
→ THE API SHALL validate all user input before processing

What's the first requirement?
```

For **strategy** type:
```markdown
Let's understand your strategic decision.

1. What decision are you trying to make?
2. What are the key constraints?
3. Who are the stakeholders?
4. What does success look like?
```

**Write answers to**:
```
{project}/01-planning/02-discovery.md
```

**Update resume**:
```yaml
discovery_complete: true
```

---

## Phase 3: Mental Models

**CRITICAL**: Run AFTER discovery, not before.

### Step 3.1: Load Mental Models

```bash
python 00-system/mental-models/scripts/select_mental_models.py --format brief
```

### Step 3.2: AI Selects 2-3 Relevant Models

Based on:
- Discovery findings
- Project type
- Complexity

**Present to user**:
```markdown
Based on your discovery findings, I recommend these mental models:

1. **First Principles** - Strip assumptions, find fundamental truths
   Good for: Your requirements involve novel patterns

2. **Pre-Mortem** - Imagine failure before implementation
   Good for: Identifying risks in your integration points

Which would you like to apply? (or suggest others)
```

### Step 3.3: Load Selected Model Files

```bash
# Example
Read: 00-system/mental-models/models/cognitive/first-principles.md
Read: 00-system/mental-models/models/diagnostic/pre-mortem.md
```

### Step 3.4: Apply Models to Discovery

**Key Insight**: Questions are INFORMED by discovery:

```markdown
## First Principles (informed by discovery)

Looking at your requirements from discovery:
- REQ-1: THE system SHALL validate all inputs
- REQ-2: WHEN validation fails, THE system SHALL return errors

**What assumptions are embedded here?**
- Are you assuming all inputs come from trusted sources?
- Is real-time validation always necessary?

**What's the fundamental problem you're solving?**
```

### Step 3.5: Capture Outputs

- **Success criteria**: What must be true for success?
- **Risks**: What could go wrong?
- **Gaps**: What don't we know yet?

**Update 03-plan.md** with mental model outputs.

---

## Phase 4: Re-Discovery (If Needed)

### Check for Gaps

```
IF gaps identified AND rediscovery_round < 2:
    → Go to Step 4.1
ELSE:
    → Go to Phase 5
```

### Step 4.1: Update Resume

```yaml
rediscovery_round: 1  # or 2
```

### Step 4.2: Focused Re-Discovery

Only address identified gaps:

```markdown
Mental models identified these gaps:
1. "What happens when the external API is unavailable?"
2. "How do we handle rate limiting?"

Let's fill in these gaps before finalizing the plan.
```

### Step 4.3: Return to Phase 3

Re-apply mental models with new information.

### If Max Rounds Reached

```markdown
## Open Questions

After 2 discovery rounds, these remain unknown:
- [ ] Exact rate limits for external API
- [ ] Authentication token refresh timing

Proceeding with known unknowns. Will validate during execution.
```

---

## Phase 5: Finalization

### Step 5.1: Merge Into 03-plan.md

Combine:
- Discovery findings (from 02-discovery.md)
- Mental model outputs (success criteria, risks)
- Open questions / unknowns

**Present to user**:
```markdown
Here's your complete project plan:

[Display plan.md content]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REVIEW PAUSE

Does this capture everything?
- Any missing requirements?
- Any risks not addressed?
- Ready to proceed?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5.2: Finalize 04-steps.md

Use steps.md template as base:
- Fill in concrete tasks from discovery
- Add checkpoint tasks every 3-5 steps
- Reference requirements: `- [ ] Implement X **[REQ-2]**`

**Present to user**:
```markdown
Here are your execution steps:

[Display steps.md content]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REVIEW PAUSE

Are these steps clear and complete?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Step 5.3: Update Resume Context

```yaml
---
current_phase: "execution"
next_action: "execute-project"
files_to_load:
  - "01-planning/02-discovery.md"
  - "01-planning/03-plan.md"
  - "01-planning/04-steps.md"
discovery_complete: true
---
```

### Step 5.4: Display Completion

```markdown
Project Planning Complete!

{ID}-{name}/
├── 01-planning/
│   ├── 01-overview.md ✓
│   ├── 02-discovery.md ✓
│   ├── 03-plan.md ✓
│   ├── 04-steps.md ✓
│   └── resume-context.md ✓
├── 02-resources/
├── 03-working/
└── 04-outputs/

Status: READY FOR EXECUTION
Tasks: {X} total
Type: {type}

---

To execute this project, say "continue project" in a new session.
```

---

## Phase 6: Close Session

### Step 6.1: Explain Separate Session

```markdown
IMPORTANT: Context Management

This project is now planned and ready to execute.

For clean context boundaries:
1. Close this session now
2. Return later and say "continue project {name}"
3. execute-project will load your context

Why separate sessions?
- Clean mental context for execution
- Better focus without planning overhead
- Proper memory management

Ready to close?
```

### Step 6.2: Trigger close-session

```bash
python 00-system/core/nexus-loader.py --skill close-session
```

---

## Summary: Router Workflow Sequence

```
1. TYPE DETECTION
   └── Semantic match against _type.yaml descriptions

2. PROJECT SETUP
   └── init_project.py with --type flag

3. DISCOVERY (skill-based OR inline)
   └── Writes to 02-discovery.md (MANDATORY)

4. MENTAL MODELS (AFTER discovery)
   └── Informed by discovery findings

5. RE-DISCOVERY (if gaps, max 2 rounds)
   └── Fill specific gaps

6. FINALIZATION
   └── Merge into plan.md, steps.md

7. CLOSE SESSION
   └── Save state, ready for execution
```

**Key Principle**: Discovery BEFORE Mental Models ensures informed questioning.

---

**END OF WORKFLOWS**

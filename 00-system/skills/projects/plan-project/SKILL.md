---
name: plan-project
description: "create project, new project, start project, plan project, build [X]."
---

## Onboarding Awareness (CHECK BEFORE STARTING)

**Before creating a project, AI MUST check user-config.yaml for incomplete onboarding:**

### Pre-Flight Check (MANDATORY)

```yaml
# Check learning_tracker.completed in user-config.yaml
learn_projects: false  → SUGGEST 'learn projects' skill FIRST
```

**If `learn_projects: false` AND this is user's FIRST project:**
```
Before creating your first project, would you like a quick 8-minute tutorial
on how Nexus projects work? It covers:
- When to use projects vs skills (avoid common mistakes)
- Project structure and lifecycle
- How to track progress effectively

Say 'learn projects' to start the tutorial, or 'skip' to create directly.
```

**If user says 'skip':** Proceed with project creation but add this note at the end:
```
Tip: Run 'learn projects' later if you want to understand the project system deeply.
```

**If `learn_projects: true`:** Proceed normally without suggestion.

---

## MANDATORY ROUTER PATTERN

**plan-project is the ONLY entry point for all project creation.**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
WORKFLOW SEQUENCE (DO NOT SKIP STEPS)

1. TYPE DETECTION      → Semantic match from _type.yaml descriptions
2. PROJECT SETUP       → Run init_project.py with detected type
3. DISCOVERY           → Skill-based OR inline (depends on type)
4. MENTAL MODELS       → Run AFTER discovery (informed questioning)
5. RE-DISCOVERY        → If gaps found (max 2 rounds)
6. FINALIZATION        → Merge into plan.md, generate steps.md
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Critical Rules

- Discovery happens BEFORE mental models (can't stress-test what you don't understand)
- 02-discovery.md is MANDATORY output (preserves intelligence across compaction)
- Skills are invoked normally (no special contract needed)
- Steps + TodoWrite enforce sequence
- Update resume-context.md at every phase transition

---

## Type Detection

**8 Project Types** - AI semantically matches user input against descriptions:

| Type | When to Use | Discovery Method |
|------|-------------|------------------|
| **build** | Creating software, features, tools | Inline |
| **integration** | Connecting APIs, external services | Skill: add-integration |
| **research** | Academic papers, systematic analysis | Skill: create-research-project |
| **strategy** | Business decisions, planning | Inline |
| **content** | Marketing, documentation, creative | Inline |
| **process** | Workflow optimization, automation | Inline |
| **skill** | Creating Nexus skills | Skill: create-skill |
| **generic** | Anything else | Inline |

### Detection Flow

```
User: "plan project for X"
    │
    ├── Read all templates/types/*/_type.yaml
    ├── Compare user input against each description
    ├── Select best match OR ask user to choose
    │
    └── Proceed with detected type
```

**No keyword triggers** - Type detection is semantic from description field.

---

## Mode Detection Logic

**CRITICAL**: Before starting any workflow, detect which mode to use.

1. **Check for 02-projects/**:
   ```bash
   ls -d 02-projects/ 2>/dev/null
   ```
   - IF exists → **PROJECT_CREATION mode**
   - IF not exists → **WORKSPACE_SETUP mode** (System not initialized)

```
02-projects/ exists?
├── YES → PROJECT_CREATION mode
└── NO → WORKSPACE_SETUP mode
```

---

## Router Workflow

### Phase 1: Setup

```bash
# 1.1 Detect type from user input (semantic matching)
# 1.2 Create project structure
python 00-system/skills/projects/plan-project/scripts/init_project.py "Project Name" --type {type} --path 02-projects

# 1.3 Load templates from types/{type}/
# 1.4 Initialize resume-context.md
```

**Output**: Project folder with 4 directories + planning file templates

### Phase 2: Discovery

**Check _type.yaml for discovery method:**

#### Skill-Based Discovery (integration, research, skill)

```bash
# Update resume-context.md with current_skill
# Load skill normally:
python 00-system/core/nexus-loader.py --skill {skill-name}

# Skill runs its workflow and writes to project's 02-discovery.md
# Clear current_skill when complete
```

| Type | Skill to Load |
|------|---------------|
| integration | add-integration |
| research | create-research-project |
| skill | create-skill |

#### Inline Discovery (build, strategy, content, process, generic)

```bash
# Load discovery.md template from templates/types/{type}/
# Ask discovery questions interactively
# Write answers to project's 02-discovery.md
```

**CRITICAL**: Discovery MUST complete before mental models.

### Phase 3: Mental Models (After Discovery)

```bash
# Load mental models dynamically
python 00-system/mental-models/scripts/select_mental_models.py --format brief
```

1. AI selects 2-3 relevant models based on discovery findings
2. Present options to user
3. Load selected model files from `00-system/mental-models/models/{category}/`
4. Apply model questions to discovery findings
5. Capture: success_criteria, risks, gaps
6. Update 03-plan.md with outputs

**Key Insight**: Questions are INFORMED by discovery:
- "Given what we found about [X], what's truly essential?"
- "Given these constraints, what could break?"
- "Given this plan, imagine it failed. Why?"

### Phase 4: Re-Discovery (If Gaps Found)

```
IF gaps exist AND rediscovery_round < 2:
    → Increment rediscovery_round in resume-context.md
    → Focus discovery on identified gaps
    → Return to Phase 3

ELSE IF gaps exist AND rediscovery_round >= 2:
    → Log unknowns in plan.md "Open Questions" section
    → Note: "Proceeding with known unknowns after 2 rounds"
    → Continue to Phase 5
```

### Phase 5: Finalization

1. **Merge into 03-plan.md**:
   - Discovery findings (from 02-discovery.md)
   - Mental model outputs (success criteria, risks)
   - Open questions / unknowns

2. **Finalize 04-steps.md**:
   - Use steps.md template as base
   - Fill in concrete tasks from discovery
   - Add checkpoint tasks every 3-5 steps

3. **Update resume-context.md**:
   ```yaml
   current_phase: "execution"
   next_action: "execute-project"
   files_to_load: [all relevant resources]
   ```

4. **Project Ready for Execution**

---

## Resume Context Updates

**Update at EVERY phase transition:**

```yaml
# resume-context.md frontmatter
---
session_ids: ["uuid-1", "uuid-2"]
project_id: "30-project-name"
project_name: "Human Readable Name"
current_phase: "planning|execution"

# LOADING
next_action: "plan-project|execute-project"
files_to_load:
  - "01-planning/02-discovery.md"  # MANDATORY
  - "01-planning/03-plan.md"
  - "01-planning/04-steps.md"

# SKILL TRACKING (optional)
current_skill: ""  # Set when skill loaded, clear when complete

# DISCOVERY STATE
rediscovery_round: 0  # 0, 1, or 2
discovery_complete: false

# PROGRESS
current_section: 1
tasks_completed: 0
---
```

---

## EARS Requirements (Build/Skill Types Only)

For **build** and **skill** project types, discovery.md includes EARS-formatted requirements:

| Pattern | Template |
|---------|----------|
| Ubiquitous | THE `<system>` SHALL `<response>` |
| Event-driven | WHEN `<trigger>`, THE `<system>` SHALL `<response>` |
| State-driven | WHILE `<condition>`, THE `<system>` SHALL `<response>` |
| Unwanted | IF `<condition>`, THEN THE `<system>` SHALL `<response>` |
| Optional | WHERE `<option>`, THE `<system>` SHALL `<response>` |
| Complex | [WHERE] [WHILE] [WHEN/IF] THE `<system>` SHALL `<response>` |

**See**: [references/ears-patterns.md](references/ears-patterns.md) for full guide.

---

## Resources

### scripts/
- **init_project.py**: Project template generator with `--type` flag
  - Usage: `python scripts/init_project.py "Name" --type build --path 02-projects`
  - Auto-generates structure with type-specific templates

### templates/types/
```
types/
├── build/          # Inline discovery, EARS requirements
├── integration/    # Routes to add-integration skill
├── research/       # Routes to create-research-project skill
├── strategy/       # Inline discovery, decision frameworks
├── content/        # Inline discovery, creative brief
├── process/        # Inline discovery, workflow optimization
├── skill/          # Routes to create-skill skill, EARS requirements
└── generic/        # Minimal inline discovery
```

Each type folder contains:
- `_type.yaml` - Type configuration and description
- `overview.md` - Overview template
- `discovery.md` - Discovery questions/structure
- `plan.md` - Plan template
- `steps.md` - Steps template

### references/
- **routing-logic.md**: Router decision tree and workflow
- **ears-patterns.md**: EARS requirement templates
- **incose-rules.md**: INCOSE quality rules
- **project-types.md**: Type descriptions and guidance
- **workflows.md**: Detailed workflow documentation

---

## Error Handling

### Invalid Project ID/Name
- Explain validation rule clearly
- Show example of correct format
- Suggest correction

### Project Already Exists
- Inform user project exists
- Offer options: different name, different ID, or load existing

### Memory Files Missing
- Warn user: "Memory files not initialized"
- Suggest: "Please run 00-setup-memory project first"
- DO NOT create project

### Discovery Skill Not Found
- Fall back to inline discovery.md template
- Log warning for user

### User Abandons Mid-Creation
- Save partial work to temp file
- Inform: "Progress saved. Say 'continue project creation' to resume."

---

## Why This Design?

**Why Mandatory Router?**
- Single entry point ensures consistent quality
- All projects get proper discovery and mental model application
- Prevents shortcuts that lead to poor planning

**Why Discovery BEFORE Mental Models?**
- Can't stress-test what you don't understand
- Mental models are INFORMED by discovery findings
- Questions become specific, not abstract

**Why 8 Types?**
- Semantic detection (not keywords) handles edge cases
- Each type has appropriate discovery method
- Build/Skill get EARS requirements; others get simpler discovery

**Why Skills Invoked Normally?**
- No special contract needed (v2.4 simplification)
- Skills write to project's 02-discovery.md
- Steps + TodoWrite enforce sequence

**Why Separate Sessions?**
- Context management: Clean boundaries between planning and execution
- Focus: Execution session loads only execution context
- Memory: close-session properly saves state between phases

---

**Integration**:
- close-session automatically updates project state every session
- validate-system checks project structure integrity
- Skills can reference project outputs in their workflows
- execute-project continues from where plan-project finishes

---

**Remember**: This is a COLLABORATIVE DESIGN SESSION with proper discovery and mental model application. The router ensures every project gets the depth it deserves!

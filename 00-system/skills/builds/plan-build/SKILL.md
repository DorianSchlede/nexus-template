---
name: plan-build
description: "create build, new build, start build, plan build, build [X]."
---

## Onboarding Awareness (CHECK BEFORE STARTING)

**Before creating a build, AI MUST check user-config.yaml for incomplete onboarding:**

### Pre-Flight Check (MANDATORY)

```yaml
# Check learning_tracker.completed in user-config.yaml
learn_builds: false  → SUGGEST 'learn builds' skill FIRST
```

**If `learn_builds: false` AND this is user's FIRST build:**
```
Before creating your first build, would you like a quick 8-minute tutorial
on how Nexus builds work? It covers:
- When to use builds vs skills (avoid common mistakes)
- Build structure and lifecycle
- How to track progress effectively

Say 'learn builds' to start the tutorial, or 'skip' to create directly.
```

**If user says 'skip':** Proceed with build creation but add this note at the end:
```
Tip: Run 'learn builds' later if you want to understand the build system deeply.
```

**If `learn_builds: true`:** Proceed normally without suggestion.

---

## MANDATORY ROUTER PATTERN

**plan-build is the ONLY entry point for all build creation.**

-------------------------------------------------------
WORKFLOW SEQUENCE (DO NOT SKIP STEPS)

1. TYPE DETECTION      → Semantic match from _type.yaml descriptions
2. BUILD SETUP         → Run init_build.py with detected type
3. DISCOVERY           → 3-phase flow (inline) OR skill-based
   3a. Discovery Questions → Understand what user wants to build
   3b. Active Research     → AI explores based on answers
   3c. Informed Follow-ups → Questions + optional follow-up research
       ↳ Loop to 3b if new areas discovered (max 2 loops)
4. MENTAL MODELS       → **MANDATORY** - Run AFTER discovery
5. RE-DISCOVERY        → If mental models reveal gaps (max 2 rounds)
6. FINALIZATION        → Fill 03-plan.md, fill 04-steps.md
-------------------------------------------------------

**CRITICAL CHECKPOINTS:**
- After Phase 3: plan.md MUST have success criteria + risks (from mental models)
- After Phase 6: plan.md MUST be filled (not template), steps.md MUST have concrete tasks

### Critical Rules

- Discovery happens BEFORE mental models (can't stress-test what you don't understand)
- 02-discovery.md is MANDATORY output (preserves intelligence across compaction)
- Skills are invoked normally (no special contract needed)
- Steps + TodoWrite enforce sequence
- Update resume-context.md at every phase transition

---

## Type Detection

**8 Build Types** - AI semantically matches user input against descriptions:

| Type | When to Use | Discovery Method |
|------|-------------|------------------|
| **build** | Creating software, features, tools | Inline |
| **integration** | Connecting APIs, external services | Skill: add-integration |
| **research** | Academic papers, systematic analysis | Skill: create-research-build |
| **strategy** | Business decisions, planning | Inline |
| **content** | Marketing, documentation, creative | Inline |
| **process** | Workflow optimization, automation | Inline |
| **skill** | Creating Nexus skills | Skill: create-skill |
| **generic** | Anything else | Inline |

### Detection Flow

```
User: "plan build for X"
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

1. **Check for 02-builds/**:
   ```bash
   ls -d 02-builds/ 2>/dev/null
   ```
   - IF exists → **BUILD_CREATION mode**
   - IF not exists → **WORKSPACE_SETUP mode** (System not initialized)

```
02-builds/ exists?
├── YES → BUILD_CREATION mode
└── NO → WORKSPACE_SETUP mode
```

---

## Router Workflow

### Phase 1: Setup

```bash
# 1.1 Detect type from user input (semantic matching)
# 1.2 Create build structure
nexus-init-build "Build Name" --type {type} --path 02-builds/active

# 1.3 Load templates from types/{type}/
# 1.4 Initialize resume-context.md
# 1.5 Check roadmap and link if match found (see below)
```

**Output**: Build folder with 4 directories + planning file templates

#### Step 1.5: Roadmap Linking (REQ-2)

**If `01-memory/roadmap.yaml` exists**, check if build name matches a roadmap item:

```python
# Roadmap linking logic (executed inline by AI)
from pathlib import Path
import re

def slugify(name: str) -> str:
    """Convert name to slug: lowercase, replace spaces with hyphens, remove non-alphanumeric."""
    slug = name.lower().replace(" ", "-")
    slug = re.sub(r"[^a-z0-9-]", "", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug

roadmap_path = Path("01-memory/roadmap.yaml")
if roadmap_path.exists():
    import yaml
    with open(roadmap_path) as f:
        roadmap = yaml.safe_load(f)

    build_name = "Build Name"  # The name being created
    build_id = "XX-build-name"  # The generated build ID

    for item in roadmap.get("items", []):
        if item.get("build_id"):
            continue  # Already linked

        # Match: slugified item name contained in build ID slug
        item_slug = slugify(item["name"])
        build_slug = slugify(build_id)

        if item_slug in build_slug:
            # LINK: Set build_id on roadmap item
            item["build_id"] = build_id
            with open(roadmap_path, "w") as f:
                yaml.dump(roadmap, f, default_flow_style=False, allow_unicode=True)
            print(f"Linked roadmap item '{item['name']}' to build '{build_id}'")
            break
```

**CRITICAL - Slug Matching Rules**:
- Slugify both item name and build ID
- Match if item slug is CONTAINED in build slug (handles numbered prefixes like "01-content-calendar")
- Example: "Content Calendar" → "content-calendar" matches "01-content-calendar"

### Phase 2: Discovery (3-Phase Flow)

**Discovery follows ASK → RESEARCH → ASK (+ optional loop) pattern:**

```
Phase 2a: Discovery Questions (understand the build)
    ↓
Phase 2b: Active Research (targeted by answers)
    ↓
Phase 2c: Informed Follow-ups + Optional Follow-up Research
    ↓ (if gaps found)
    Loop back to 2b for deeper research
```

**Check _type.yaml for discovery method:**

#### Skill-Based Discovery (integration, research, skill)

```bash
# Update resume-context.md with current_skill
# Load skill normally:
nexus-load --skill {skill-name}

# Skill runs its workflow and writes to build's 02-discovery.md
# Clear current_skill when complete
```

| Type | Skill to Load |
|------|---------------|
| integration | add-integration |
| research | create-research-build |
| skill | create-skill |

**Note**: Skill-based types skip the 3-phase flow - their skills handle discovery.

#### Inline Discovery (build, strategy, content, process, generic)

**Phase 2a: Discovery Questions**

Ask type-specific discovery questions FIRST to understand what the user wants:

```markdown
Let me understand what you're building:

1. **What are you building?**
   - Describe the feature/system in 1-2 sentences

2. **What problem does this solve?**
   - Why is this needed? What pain point does it address?

3. **Who/what will use this?**
   - Users? Other systems? Internal tools?

4. **Any constraints or requirements?**
   - Must integrate with existing systems?
   - Performance requirements?
   - Technology preferences or restrictions?

5. **What does success look like?**
   - How will you know this build is complete?
```

**AI then uses these answers to target research** (see [active-discovery-guide.md](references/active-discovery-guide.md)).

**Phase 2b: Active Research**

AI-driven research BASED ON discovery answers from Phase 2a:

**Step 1: Determine Search Targets from Answers**

Extract search targets from user's discovery answers:
- Build description → keywords for codebase search
- Problem statement → related patterns to find
- Integration mentions → systems to check
- Constraints → areas that might conflict

**Step 2: Assess Complexity**
```
Simple (single file/function)  → 0 agents, direct Grep/Glob
Medium (component/feature)     → 1-2 targeted agents
Complex (multi-component)      → 3-5 specialized agents
```

**Step 3: Dynamic Subagent Exploration** (for medium/complex)

AI determines BOTH number AND purpose of agents based on:
- Build description from Phase 2a (e.g., "auth feature" → explore auth, security, users)
- Problem statement (what systems might be affected)
- Codebase structure (what exists to explore)

```python
# Spawn ALL agents in a single message for parallel execution
for purpose in agent_purposes:
    Task(
        subagent_type="Explore",
        prompt=generate_agent_prompt(purpose, build_description, discovery_answers),
        description=f"Exploring {purpose['focus_area']}"
    )
```

**Step 4: Related Builds Check**
- Scan `02-builds/active/` and `02-builds/complete/` for similar names/purposes
- Warn if duplicates found (don't block)
- Document in "Related Builds & Skills" section

**Step 5: Related Skills Check**
- Scan `03-skills/` and `00-system/skills/` for reusable skills
- Check if build would affect existing skills
- Document findings

**Step 6: Integration Check** (if relevant)
- Query `01-memory/integrations/` for relevant integrations
- Check if existing integrations provide context for this build

**Step 7: Web Search** (for best practices)
- Max 3 queries based on build topic (see [active-discovery-guide.md](references/active-discovery-guide.md))
- Ask user: "Should I search the web for best practices on {topic}?"
- Document best practices found

**Step 8: Present Consolidated Findings**

Display research results BEFORE follow-up questions:

```
RESEARCH COMPLETE
----------------------------------------------------
Based on your description of {build_summary}:

Codebase: Found {N} related files in {areas}
  - {file1} - {why relevant}
  - {file2} - {why relevant}

Related Work: {N} builds, {N} skills could be affected
  - {build/skill} - {relationship}

Web Research: {N} best practices found (if performed)
  - {practice} - {source}

I have some follow-up questions based on what I found...
```

**Phase 2c: Informed Follow-ups + Optional Follow-up Research**

Ask follow-up questions INFORMED by research findings:

```markdown
Given I found {finding from research}:
- {Question about how to handle this}

Given {another finding}:
- {Another question informed by what AI discovered}
```

Example informed questions:
- "Given I found existing session management in src/auth/, should we extend it or create new?"
- "Given Build 02-auth-refactor is also modifying auth files, should we coordinate or wait?"
- "The web search suggests using JWT for this. Your current system uses sessions. Migrate or keep both?"

**Follow-up Research (if needed):**

If user's answers reveal new areas to explore:
```
Your answer mentions {new_area} that I didn't search earlier.
Should I research {new_area} before we continue?
```

If yes → Loop back to Phase 2b with targeted search
If no → Continue to mental models

**Write all findings to build's 02-discovery.md** (not just chat output).

**CRITICAL**: Discovery phases MUST complete before mental models. Max 2 research loops to avoid infinite discovery.

### Phase 3: Mental Models (After Discovery) - MANDATORY

**DO NOT SKIP THIS PHASE.** Mental models ensure build quality.

#### Step 3.1: Load Available Models

```bash
# List available mental models
nexus-mental-models --format brief
```

#### Step 3.2: Select Models (AI + User)

Based on discovery findings, select 2-3 relevant models:

| Build Type | Recommended Models |
|--------------|-------------------|
| Build/Skill | First Principles, Pre-Mortem, Inversion |
| Integration | Pre-Mortem, Systems Thinking |
| Research | First Principles, Socratic Method |
| Strategy | SWOT, Pre-Mortem, Second-Order Thinking |
| Content | Jobs-to-be-Done, First Principles |
| Process | Systems Thinking, Inversion |

Present options to user:
```
Based on your [build_type] build, I recommend these mental models:
1. [Model A] - [Why relevant to this build]
2. [Model B] - [Why relevant to this build]

Which would you like to apply? (or suggest others)
```

#### Step 3.3: Apply Models to Discovery

Load selected model file and apply questions:

```bash
# Read model file
cat 00-system/mental-models/models/{category}/{model-slug}.md
```

**Key Questions** (informed by discovery):
- "Given what we found about [X], what's truly essential?"
- "Given these constraints [from discovery], what could break?"
- "Given this plan [from discovery], imagine it failed. Why?"

#### Step 3.4: Capture Outputs

Update 03-plan.md with:
- **Success Criteria**: Refined from discovery + mental model analysis
- **Risks**: Identified through Pre-Mortem/Inversion
- **Gaps**: Areas needing more discovery

#### Step 3.5: Verify Completion

Before proceeding to Phase 4/5:
- [ ] At least 2 mental models applied
- [ ] Success criteria refined in 03-plan.md
- [ ] Risks documented in 03-plan.md
- [ ] Gaps identified (if any)

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

### Phase 5: Finalization - FILL ALL TEMPLATES

**DO NOT leave templates with placeholder text.** All files must have real content.

#### Step 5.1: Fill 03-plan.md Completely

The plan.md file MUST contain:

```markdown
## Approach
[Actual strategy description - NOT placeholder text]

## Key Decisions
| Decision | Choice | Rationale |
|----------|--------|-----------|
| [Real decision] | [Real choice] | [Real rationale] |

## Success Criteria (from Mental Models)
- [ ] [Specific, measurable criterion 1]
- [ ] [Specific, measurable criterion 2]

## Risks & Mitigations (from Mental Models)
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Real risk] | [H/M/L] | [H/M/L] | [Real mitigation] |

## Dependencies (from Discovery)
- [Real dependencies from 02-discovery.md]
```

**VERIFY**: No `{{placeholder}}` or `[To be filled]` text remains.

#### Step 5.2: Fill 04-steps.md Completely

Replace generic phases with concrete tasks:

```markdown
## Phase 2: [Actual Phase Name]
- [ ] [Concrete task with expected output]
- [ ] [Concrete task with expected output]
- [ ] **CHECKPOINT**: Verify [what] works

## Phase 3: [Actual Phase Name]
- [ ] [Concrete task]
- [ ]* [Optional task] (marked with *)
```

**VERIFY**: No `[Step 1]` or `[Name this phase]` text remains.

#### Step 5.3: Update resume-context.md

```yaml
current_phase: "execution"
next_action: "execute-build"
discovery_complete: true
files_to_load:
  - "01-planning/01-overview.md"
  - "01-planning/02-discovery.md"
  - "01-planning/03-plan.md"
  - "01-planning/04-steps.md"
```

#### Step 5.4: Final Verification Checklist

Before declaring planning complete:
- [ ] 03-plan.md has actual content (no placeholders)
- [ ] 03-plan.md has success criteria from mental models
- [ ] 03-plan.md has risks from mental models
- [ ] 04-steps.md has concrete tasks (no placeholders)
- [ ] 04-steps.md has checkpoint tasks
- [ ] resume-context.md updated with discovery_complete: true

**Build Ready for Execution**

---

## Resume Context Updates

### Auto-Synced by Hooks (don't manually update)

PreCompact hook automatically syncs these fields:
- `session_ids` - List of all sessions that touched this build
- `last_updated` - Timestamp of last activity
- `total_tasks`, `tasks_completed` - Checkbox counts from 04-steps.md
- `current_section`, `current_task` - Position tracking
- `current_phase` - Detected from Phase 1 completion
- `next_action` - "plan-build" or "execute-build"

### Claude Must Update

Update these fields at session end:

1. **continue_at** - Specific pointer for next agent:
   ```yaml
   continue_at: "02-discovery.md Phase 2"  # or specific line reference
   ```

2. **blockers** - List any blockers:
   ```yaml
   blockers: []  # or ["Waiting for user input on scope"]
   ```

3. **files_to_load** - Context files (AUTO-LOADED in COMPACT mode):
   ```yaml
   files_to_load:
     - "01-planning/02-discovery.md"   # Research findings
     - "01-planning/03-plan.md"        # Approach decisions
     - "02-resources/decisions.md"     # Key decisions made
   ```

   **Pattern**: Write context to FILES → Add to `files_to_load`
   - Made decision? → Write to `02-resources/decisions.md` → Add to list
   - Hook AUTO-LOADS these files for next session

4. **Context for Next Agent** - Prose that POINTS to files:
   ```markdown
   ### Latest Session (YYYY-MM-DD)

   **Completed this session:**
   - [x] Created 02-discovery.md with 12 problems
   - [x] Applied Pre-Mortem mental model

   **Key files:**
   - See `decisions.md` for approach rationale

   **Next steps:**
   1. Continue at `continue_at` location
   ```

> **Philosophy**: Don't capture context in prose. Write it to FILES, add to `files_to_load`. Prose just POINTS to files.

### Standard Field Values

| Field | Values | Description |
|-------|--------|-------------|
| `current_phase` | `planning`, `execution`, `complete` | Build lifecycle stage |
| `next_action` | `plan-build`, `execute-build` | Which skill to load on resume |
| `build_type` | `build`, `integration`, `research`, `strategy`, `content`, `process`, `skill`, `generic` | Type from init |

### Phase Transition Checklist

**Planning Start:**
```yaml
current_phase: "planning"
next_action: "plan-build"
files_to_load: [overview, discovery, plan, steps]
discovery_complete: false
```

**Planning Complete (ready for execution):**
```yaml
current_phase: "execution"
next_action: "execute-build"
files_to_load: [discovery, plan, steps]  # drop overview
discovery_complete: true
```

**Build Complete:**
```yaml
current_phase: "complete"
next_action: "execute-build"  # or archive-build
```

---

## EARS Requirements (Build/Skill Types Only)

For **build** and **skill** build types, discovery.md includes EARS-formatted requirements:

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
- **init_build.py**: Build template generator with `--type` flag
  - Usage: `nexus-init-build "Name" --type build --path 02-builds/active`
  - Auto-generates structure with type-specific templates

### templates/types/
```
types/
├── build/          # Inline discovery, EARS requirements
├── integration/    # Routes to add-integration skill
├── research/       # Routes to create-research-build skill
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
- **build-types.md**: Type descriptions and guidance
- **workflows.md**: Detailed workflow documentation

---

## Error Handling

### Invalid Build ID/Name
- Explain validation rule clearly
- Show example of correct format
- Suggest correction

### Build Already Exists
- Inform user build exists
- Offer options: different name, different ID, or load existing

### Memory Files Missing
- Warn user: "Memory files not initialized"
- Suggest: "Please run 'quick start' first to configure your goals"
- DO NOT create build

### Discovery Skill Not Found
- Fall back to inline discovery.md template
- Log warning for user

### User Abandons Mid-Creation
- Save partial work to temp file
- Inform: "Progress saved. Say 'continue build creation' to resume."

---

## Why This Design?

**Why Mandatory Router?**
- Single entry point ensures consistent quality
- All builds get proper discovery and mental model application
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
- Skills write to build's 02-discovery.md
- Steps + TodoWrite enforce sequence

**Why Separate Sessions?**
- Context management: Clean boundaries between planning and execution
- Focus: Execution session loads only execution context
- Memory: close-session properly saves state between phases

---

**Integration**:
- close-session automatically updates build state every session
- validate-system checks build structure integrity
- Skills can reference build outputs in their workflows
- execute-build continues from where plan-build finishes

---

**Remember**: This is a COLLABORATIVE DESIGN SESSION with proper discovery and mental model application. The router ensures every build gets the depth it deserves!

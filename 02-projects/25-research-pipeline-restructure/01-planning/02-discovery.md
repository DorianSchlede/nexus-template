# Discovery: Project 25 - Research Pipeline Restructure

**Time**: ~10 min discovery
**Date**: 2026-01-04

---

## 1. Dependencies (Files/Systems This Project Will Touch)

### Files to Modify

| File | What Changes |
|------|--------------|
| `00-system/skills/projects/create-project/SKILL.md` | Add discovery step to CRITICAL EXECUTION REQUIREMENTS |
| `00-system/skills/projects/create-project/references/workflows.md` | Insert Step 4.5: Discovery after init_project.py |
| `00-system/skills/projects/create-project/scripts/init_project.py` | No change needed - already creates resume-context.md for session resume |

### New Files to Create

| File | Purpose |
|------|---------|
| `00-system/skills/projects/create-project/scripts/templates/discovery-template.md` | Template for discovery.md output |

### Templates That Exist (Context)

Current templates in `create-project/scripts/templates/`:
- `template-build.md` - Build/Create projects
- `template-research.md` - Research/Analysis projects (25 lines, minimal)
- `template-strategy.md` - Strategy projects
- `template-content.md` - Content projects
- `template-process.md` - Process projects
- `template-generic.md` - Generic projects

**Note**: `template-research.md` is a project TYPE, not a discovery template. No conflict.

---

## 2. Existing Patterns to Reuse

### Pattern: Workflow Step Insertion
From `workflows.md` analysis:
- Steps are numbered (Step 1, Step 2, etc.)
- Current flow: Step 4 (Create Folder Structure) → Step 5 (Fill overview.md)
- Discovery should be **Step 4.5** or renumber as Step 5

### Pattern: AI Proposal with Skip Option
From mental-models integration in `workflows.md`:
```
Want to apply structured thinking? ...
Options:
1. Continue without mental models (faster)
2. Apply Pre-Mortem...
```
Discovery should follow same pattern:
```
Before we plan, let me do a quick dependency scan (5 min).
1. Run discovery (recommended)
2. Skip and proceed to overview
```

### Pattern: Auto-Population
From `project-types.md` line 316-356:
- AI already scans codebase for related files
- AI populates Dependencies & Links section
- **Insight**: Discovery formalizes what AI already does informally

### Pattern: Template Injection
From `init_project.py` line 435-440:
- Type-specific sections injected before "## Mental Models Applied"
- Can use same pattern for discovery findings → Dependencies section

### Pattern: Resume Context (from Project 24)
From `init_project.py` line 462-495:
- `resume-context.md` created automatically by init_project.py
- Contains YAML frontmatter with project state for session resume
- Discovery step should run AFTER init (resume file exists) but BEFORE filling overview.md

---

## 3. Risks & Unknowns

### High Risk: Discovery Feels Like Overhead
**Mitigation**:
- Time-box to 5 min
- Clear value proposition: "avoid mid-project surprises"
- Trivial skip path

### Medium Risk: Confusion with template-research.md
**Mitigation**:
- Name it `discovery-template.md` (not research)
- Output file is `discovery.md` (not research.md)
- Document distinction in SKILL.md

### Medium Risk: Discovery Output Not Used
**Mitigation**:
- Auto-populate plan.md Dependencies section
- Show immediate value from discovery time

### Low Risk: Discovery Takes Too Long
**Mitigation**:
- Strict 5-15 min time-box in template
- Only 3 focused sections
- AI-driven scan, not collaborative exploration

### Unknown: Where in Workflow?
**Options**:
1. After init_project.py, before overview.md (Step 4.5)
2. Before init_project.py (exploration before structure)

**Recommendation**: After init (Step 4.5) - structure exists, discovery can reference project folder

### Unknown: Output Format for Auto-Population
**Need to define**:
- How discovery.md sections map to plan.md Dependencies
- Whether to use YAML frontmatter or markdown parsing

### Decision: Output Location
**Resolved**: `01-planning/discovery.md` (NOT `02-resources/`)
- Discovery is part of planning, not a resource
- Keeps all planning artifacts together
- Consistent with overview.md, plan.md, steps.md, resume-context.md

---

## Auto-Populate for plan.md Dependencies

Based on this discovery, here's what should go in plan.md Dependencies:

**Files Impacted**:
- `00-system/skills/projects/create-project/SKILL.md` - Add discovery documentation
- `00-system/skills/projects/create-project/references/workflows.md` - Insert Step 4.5
- `00-system/skills/projects/create-project/scripts/templates/discovery-template.md` - NEW

**External Systems**: None

**Related Projects**:
- Project 24: Hook/Resume System - Parent project (research phase moved here)

**Skills/Workflows**:
- `create-project` - Primary skill being enhanced
- `mental-models` - Pattern for AI proposals with skip option

---

## Next Steps

1. Create `discovery-template.md` with 3 focused sections
2. Update `workflows.md` to insert discovery step
3. Update `SKILL.md` to document always-propose behavior
4. Test discovery flow

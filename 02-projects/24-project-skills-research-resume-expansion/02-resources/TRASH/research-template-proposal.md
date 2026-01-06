# Research Template Proposal

**Purpose**: Template for pre-planning research phase in create-project workflow

---

## Template Structure

```markdown
# {Project Name} - Research

**Research Date**: {date}
**Researcher**: {AI/User}
**Project Type**: {Build/Research/Strategy/etc.}

---

## 1. Domain Exploration

**Goal**: Understand what exists in the codebase related to this project domain

### Codebase Scan
[Results from grep/glob searches for domain keywords]

**Files Found**:
- `path/to/file.py` - [Brief description]
- `path/to/another-file.md` - [Brief description]

**Patterns Identified**:
- [Pattern 1]
- [Pattern 2]

---

## 2. Dependency Analysis

**Goal**: Identify all files, skills, and systems this project will touch

### Direct Dependencies
**Files That Will Change**:
- `path/to/file` - [What will change]

**Files To Reference**:
- `path/to/file` - [Why needed]

### Skill Dependencies
**Existing Skills to Reuse**:
- `skill-name` - [How it's used]

**New Skills Needed**:
- [Skill description] - [Why needed]

### External System Dependencies
**Integrations Required**:
- [System name] - [Connection details]

**APIs/Services**:
- [Service name] - [Usage]

---

## 3. Pattern Discovery

**Goal**: Find existing patterns, conventions, or best practices to follow

### Code Patterns
[Similar implementations found in codebase]

### Naming Conventions
[How similar things are named]

### Architecture Patterns
[How similar features are structured]

### Anti-Patterns to Avoid
[What NOT to do based on codebase review]

---

## 4. Technical Requirements

**Goal**: Identify technical constraints and requirements

### Technology Stack
[Languages, frameworks, tools used]

### Performance Requirements
[Speed, scale, resource constraints]

### Security Requirements
[Auth, permissions, data handling]

### Compatibility Requirements
[Versions, platforms, integrations]

---

## 5. Risk Assessment

**Goal**: Identify potential blockers or challenges early

### Known Risks
- [ ] Risk 1 - [Impact: High/Med/Low]
- [ ] Risk 2 - [Impact: High/Med/Low]

### Unknowns
- [ ] Unknown 1 - [Needs investigation]
- [ ] Unknown 2 - [Needs investigation]

### Mitigation Strategies
[How to address identified risks]

---

## 6. Research Findings Summary

**Key Insights**:
1. [Insight 1]
2. [Insight 2]
3. [Insight 3]

**Recommended Approach**:
[Based on research, what's the best path forward?]

**Pre-Populated Dependencies for plan.md**:
```markdown
## Dependencies & Links

**Files Impacted**:
- `path/to/file` - [What changes]

**External Systems**:
- [System name] - [How it's used]

**Related Projects**:
- Project NN - [Relationship]

**Skills/Workflows**:
- [Skill name] - [How it's invoked]
```

---

## Research Checklist

**Domain Exploration**:
- [ ] Searched codebase for domain keywords
- [ ] Identified similar existing implementations
- [ ] Documented relevant files and patterns

**Dependency Analysis**:
- [ ] Listed all files that will be modified
- [ ] Identified existing skills to reuse
- [ ] Checked integration configurations

**Pattern Discovery**:
- [ ] Reviewed similar features for patterns
- [ ] Documented naming conventions
- [ ] Identified anti-patterns to avoid

**Technical Requirements**:
- [ ] Verified technology stack compatibility
- [ ] Identified performance requirements
- [ ] Checked security requirements

**Risk Assessment**:
- [ ] Listed known risks and impacts
- [ ] Identified unknowns requiring investigation
- [ ] Drafted mitigation strategies

---

*Next: Use findings to fill plan.md Dependencies & Links section*
```

---

## Usage in create-project Workflow

### When to Offer Research Phase
After `init_project.py` creates structure, before filling overview.md:

```
AI: "Project structure created! Would you like to research before planning?

Research phase (optional, 5-15 min):
✓ Scans codebase for related patterns
✓ Identifies dependencies and integrations
✓ Discovers existing code to reuse
✓ Pre-populates plan.md dependencies

This is especially helpful for:
- Projects touching existing code
- Projects with many dependencies
- Technical projects requiring pattern research

Skip research if this is:
- Standalone/greenfield project
- Simple project with no dependencies
- You already know all the patterns

Would you like to do research? (yes/no/maybe - I'll explain more)"
```

### Research Workflow
1. Create `02-resources/research.md` from template
2. Execute research tasks (grep, glob, file reads)
3. Fill in sections as findings emerge
4. Summarize key insights
5. Use findings to pre-populate plan.md Dependencies section
6. Continue to overview.md planning

---

## Subagent Integration (Optional)

For complex projects, offer to spawn research subagents:

```
AI: "This looks like a complex project with many dependencies.
Would you like me to spawn parallel research agents?

I can launch agents to:
1. Scan codebase for domain patterns (2-3 min)
2. Analyze integration dependencies (2-3 min)
3. Review similar projects for conventions (2-3 min)

Or I can do sequential research myself (5-10 min).

Your preference?"
```

---

## Benefits

1. **Better Planning**: Informed decisions based on codebase reality
2. **Reuse Discovery**: Find existing code to leverage
3. **Risk Reduction**: Identify blockers before implementation
4. **Dependency Clarity**: Know all system touchpoints upfront
5. **Pattern Consistency**: Follow established conventions

---

## Implementation Notes

1. **Template Location**: `00-system/skills/projects/create-project/scripts/templates/template-research.md`
2. **Created As**: `02-resources/research.md` in project folder
3. **Timing**: After init_project.py, before overview.md
4. **Optional**: User can skip if not needed
5. **Integration**: Findings flow into plan.md Dependencies section

---

**Status**: Proposal
**Next**: Review with stakeholder, refine, implement

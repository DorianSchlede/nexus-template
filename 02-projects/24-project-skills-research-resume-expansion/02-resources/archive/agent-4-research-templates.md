# Agent 4: Research Template System Design

**Created**: 2026-01-03
**Author**: Agent 4 - Research Template System Designer
**Purpose**: Design 3 research template variants and selection logic for create-project workflow

---

## Executive Summary

This document defines a **3-tier research template system** for the create-project skill:

1. **template-research-build.md** - For build/implementation projects (codebase analysis, technical research)
2. **template-research-analysis.md** - For research/analysis projects (web research, paper search, competitive analysis)
3. **template-research-simple.md** - For simple/greenfield projects (minimal research, quick validation)

**Key Design Decisions**:
- Research outputs go to `01-planning/research.md` (NOT 02-resources!)
- Research findings pre-populate `plan.md` Dependencies section
- Research phase is **OPTIONAL** with intelligent auto-suggestion
- Templates include both **Codebase** and **External** research (GitHub, web, paper-search skill)
- Selection logic uses project type + complexity detection

---

## Template 1: Research Build Template

**File**: `00-system/skills/projects/create-project/scripts/templates/template-research-build.md`

**When to Use**: Build/Create projects (software, integrations, systems, tools)

**Target Project Types**: Build/Create

**Complexity**: Medium-High (5-20 min research)

### Template Content

```markdown
# Research Phase: [Project Name]

**Project Type**: Build/Create
**Research Date**: [Auto-generated timestamp]
**Status**: In Progress

---

## Purpose

**What we're researching**: [Auto-filled from project description]

**Why research matters**: Understanding existing patterns, dependencies, and technical constraints before implementation prevents rework and ensures compatibility.

**Time Budget**: 10-15 minutes (focused research)

---

## 1. Codebase Analysis

### 1.1 Existing Implementations
**Goal**: Find similar implementations, reusable patterns, or related systems

**Search Strategy**:
```bash
# Search for related files
grep -r "[keyword]" --include="*.py" --include="*.js" --include="*.md"
glob "**/*[keyword]*"

# Look for similar patterns
grep -r "class.*[Pattern]" --include="*.py"
```

**Findings**:
- [ ] File: [path] - [What it does, how it relates]
- [ ] File: [path] - [What it does, how it relates]
- [ ] Pattern: [description] - [Where used, applicability]

**Reuse Opportunities**:
- [What can be reused vs. built new]

---

### 1.2 Integration Points
**Goal**: Identify files, systems, and APIs this project will interact with

**Questions**:
- What existing modules/classes will this integrate with?
- What APIs/services will it call?
- What data schemas will it use?
- What configuration files will it modify?

**Findings**:
- **Files to Modify**: [List with paths]
- **Files to Import From**: [List with paths]
- **External Systems**: [APIs, databases, services]
- **Configuration**: [Config files, env vars]

---

### 1.3 Technical Constraints
**Goal**: Understand technical limitations and requirements

**Questions**:
- What technology stack is already in use?
- What versions/dependencies are locked?
- What performance requirements exist?
- What security/auth patterns must be followed?

**Findings**:
- **Tech Stack**: [Languages, frameworks, libraries]
- **Version Constraints**: [Locked versions, compatibility issues]
- **Performance**: [Requirements, benchmarks]
- **Security**: [Auth patterns, data handling rules]

---

## 2. External Research

### 2.1 GitHub/Open Source Search
**Goal**: Find reference implementations, libraries, or examples

**Search Queries**:
```
GitHub: "[technology] + [use case]"
Example: "Python Airtable automation"
```

**Findings**:
- [ ] Repo: [name] (stars: X) - [What it does, relevance]
- [ ] Library: [name] - [Features, license, integration effort]
- [ ] Example: [link] - [What it demonstrates]

**Selection Criteria**:
- Stars/activity level (maintained?)
- License compatibility
- Integration complexity (drop-in vs. custom)
- Documentation quality

---

### 2.2 Technical Documentation
**Goal**: Review official docs for technologies/APIs being used

**Sources**:
- [ ] Official docs: [link] - [Key sections reviewed]
- [ ] API reference: [link] - [Endpoints, auth, rate limits]
- [ ] Best practices: [link] - [Recommendations, warnings]

**Key Learnings**:
- [Important patterns, gotchas, recommendations]

---

### 2.3 Stack Overflow / Community Knowledge
**Goal**: Find common issues, solutions, and best practices

**Search Queries**:
```
"[technology] + [problem/feature]"
Example: "Next.js API routes authentication"
```

**Findings**:
- [ ] Issue: [description] - Solution: [approach]
- [ ] Best practice: [description] - Why: [rationale]
- [ ] Warning: [gotcha to avoid]

---

## 3. Dependency Mapping

**Goal**: Create complete picture of all dependencies for `plan.md`

### 3.1 Internal Dependencies
**Files to be created/modified** (for plan.md Dependencies section):
- `[path]` - [Purpose, changes needed]
- `[path]` - [Purpose, changes needed]

### 3.2 External Dependencies
**Systems/APIs/Services**:
- [System name] - [What it provides, auth/config needed]
- [API name] - [Endpoints used, rate limits]

### 3.3 Related Projects
**Existing projects in 02-projects/**:
- Project [ID]: [name] - [How it relates, shared dependencies]

### 3.4 Skills/Workflows
**Existing skills in 03-skills/**:
- Skill: [name] - [How it could be reused or referenced]

---

## 4. Risk Assessment

**Goal**: Identify technical risks early

**Questions**:
- What could block implementation?
- What unknowns need prototyping?
- What dependencies could break?
- What performance bottlenecks might exist?

**Findings**:
- [ ] Risk: [description] - Impact: [High/Med/Low] - Mitigation: [approach]
- [ ] Unknown: [what needs testing] - Plan: [how to validate]
- [ ] Dependency: [what could break] - Fallback: [alternative]

---

## 5. Architecture Insights

**Goal**: Sketch high-level approach before detailed planning

**Key Decisions**:
- **Approach**: [High-level strategy based on research]
- **Technology Choices**: [What to use and why]
- **Integration Pattern**: [How this fits into existing system]
- **Data Flow**: [How data moves through the system]

**Open Questions** (to be resolved in planning):
- [ ] [Question requiring deeper investigation]
- [ ] [Decision point needing stakeholder input]

---

## 6. Research Summary

**Time Spent**: [X minutes]

**Key Findings** (copy to plan.md Dependencies section):
1. [Finding 1 - actionable insight]
2. [Finding 2 - actionable insight]
3. [Finding 3 - actionable insight]

**Reuse Opportunities**:
- [What existing code/patterns can be leveraged]

**Unknowns Remaining**:
- [What still needs investigation during implementation]

**Recommendation**:
- [Confident to proceed / Need more research / Pivot suggested]

---

**Next Step**: Use findings to fill plan.md Dependencies section and inform Approach section.
```

---

## Template 2: Research Analysis Template

**File**: `00-system/skills/projects/create-project/scripts/templates/template-research-analysis.md`

**When to Use**: Research/Analysis projects (academic research, competitive analysis, market research)

**Target Project Types**: Research/Analysis

**Complexity**: Medium-High (10-25 min research)

### Template Content

```markdown
# Research Phase: [Project Name]

**Project Type**: Research/Analysis
**Research Date**: [Auto-generated timestamp]
**Status**: In Progress

---

## Purpose

**Research Question**: [Auto-filled from project description]

**Why this research matters**: [Auto-filled - value statement]

**Time Budget**: 15-25 minutes (comprehensive research setup)

---

## 1. Codebase Context

### 1.1 Previous Research
**Goal**: Find related research projects or analyses already done

**Search Strategy**:
```bash
# Search for related research in 02-projects/
ls 02-projects/ | grep -i "[keyword]"

# Check 02-resources/ in existing projects
find 02-projects/*/02-resources/ -name "*.md" -o -name "*.pdf"
```

**Findings**:
- [ ] Project [ID]: [name] - [Related research, reusable findings]
- [ ] Resource: [path] - [What it contains, relevance]
- [ ] Pattern: [approach used in past research]

**Reuse Opportunities**:
- [Prior research to build on vs. duplicate]
- [Existing datasets, sources, methodologies]

---

### 1.2 Existing Data/Resources
**Goal**: Identify internal data sources and knowledge bases

**Questions**:
- What internal documents/data could inform this research?
- What prior knowledge exists in the codebase?
- What tools/scripts already exist for analysis?

**Findings**:
- **Data Sources**: [Internal files, databases, logs]
- **Knowledge Bases**: [Documentation, wikis, notes]
- **Analysis Tools**: [Scripts, notebooks, dashboards]

---

## 2. External Research

### 2.1 Academic Paper Search
**Goal**: Find relevant academic research using paper-search skill

**Search Strategy**:
```bash
# Use paper-search skill for academic sources
python 03-skills/research-pipeline/skills/paper-search/scripts/paper_search.py \
  --query "[research topic keywords]" \
  --limit 10
```

**Search Queries**:
- Query 1: "[primary topic]" - [Rationale]
- Query 2: "[secondary topic]" - [Rationale]
- Query 3: "[methodology/framework]" - [Rationale]

**Initial Results** (to be refined in selection phase):
- [ ] Paper: [title] (Year, Authors) - [Relevance, key contribution]
- [ ] Paper: [title] (Year, Authors) - [Relevance, key contribution]
- [ ] Survey: [title] - [Scope, usefulness]

**Selection Criteria**:
- Relevance to research question (High/Med/Low)
- Recency (prefer last 3 years unless foundational)
- Citation count (impact/authority)
- Accessibility (open access priority)

**Papers to Download** (final list):
- [ ] [Paper 1] - [Why selected]
- [ ] [Paper 2] - [Why selected]

---

### 2.2 Web Research
**Goal**: Find practitioner perspectives, case studies, and current discourse

**Search Queries**:
```
Google/Web: "[topic] + [year]"
Examples:
- "LLM agents best practices 2025"
- "competitive analysis framework B2B SaaS"
```

**Sources to Check**:
- [ ] Industry blogs: [links] - [Key insights]
- [ ] Case studies: [links] - [Applicable patterns]
- [ ] Forums/Communities: [links] - [Common issues, solutions]
- [ ] Documentation: [links] - [Official guidance]

**Key Findings**:
- [Finding 1 - trend, pattern, insight]
- [Finding 2 - best practice, warning]
- [Finding 3 - tool, resource, methodology]

---

### 2.3 Competitive/Comparative Analysis
**Goal**: Understand existing solutions and approaches

**Questions**:
- Who else has tackled this problem?
- What methodologies do they use?
- What tools/frameworks exist?
- What gaps remain?

**Findings**:
- **Competitor/Alternative 1**: [name] - [Approach, strengths, weaknesses]
- **Competitor/Alternative 2**: [name] - [Approach, strengths, weaknesses]
- **Tools/Frameworks**: [name] - [Features, applicability]

**Differentiation Opportunities**:
- [What's missing in existing solutions]
- [What could be done better/differently]

---

## 3. Research Methodology Design

**Goal**: Plan how research will be conducted

### 3.1 Research Framework
**Methodology**: [Qualitative/Quantitative/Mixed Methods/Systematic Review/etc.]

**Approach**:
- [How data will be collected]
- [How findings will be analyzed]
- [How insights will be synthesized]

**Rationale**: [Why this methodology fits the research question]

---

### 3.2 Data Sources
**Primary Sources**:
- [ ] [Source type] - [What it provides, how to access]
- [ ] [Source type] - [What it provides, how to access]

**Secondary Sources**:
- [ ] [Source type] - [What it provides, how to access]
- [ ] [Source type] - [What it provides, how to access]

**Source Selection Criteria**:
- [Credibility, relevance, accessibility, recency]

---

### 3.3 Analysis Framework
**How findings will be analyzed**:
- [Thematic analysis / Statistical analysis / Comparative analysis / etc.]
- [Tools to be used: paper-analysis, synthesis, visualization]

**Synthesis Plan**:
- [How individual findings will be integrated]
- [How insights will be structured and presented]

---

## 4. Research Scope & Constraints

**Goal**: Define boundaries to keep research focused

### 4.1 Scope Definition
**In Scope**:
- [What will be researched]
- [What questions will be answered]
- [What deliverables will be produced]

**Out of Scope**:
- [What will NOT be researched]
- [What questions are deferred]
- [What's explicitly excluded]

**Rationale**: [Why these boundaries]

---

### 4.2 Time & Resource Constraints
**Time Budget**: [X hours/days]
**Resource Availability**: [What tools, data, expertise available]
**Constraints**: [What limits depth or breadth]

**Trade-offs**:
- [Depth vs. breadth decisions]
- [Quality vs. speed considerations]

---

## 5. Expected Outputs

**Goal**: Define what "done" looks like

**Deliverables**:
- [ ] [Deliverable 1] - [Format, content, purpose]
- [ ] [Deliverable 2] - [Format, content, purpose]
- [ ] [Deliverable 3] - [Format, content, purpose]

**Quality Criteria**:
- [How quality will be assessed]
- [What constitutes success]

**Stakeholders**:
- [Who will use these outputs]
- [How findings will be applied]

---

## 6. Research Summary

**Time Spent**: [X minutes]

**Key Insights** (copy to plan.md):
1. [Insight 1 - what research revealed]
2. [Insight 2 - what research revealed]
3. [Insight 3 - what research revealed]

**Methodology Recommendation**:
- [Recommended approach based on research]

**Papers/Resources to Acquire**:
- [Final list for download/review]

**Open Questions** (to be answered during research):
- [ ] [Question 1]
- [ ] [Question 2]

**Readiness Assessment**:
- [Confident to proceed / Need more prep / Pivot suggested]

---

**Next Step**: Use findings to fill plan.md Research Methodology section and define detailed steps.
```

---

## Template 3: Research Simple Template

**File**: `00-system/skills/projects/create-project/scripts/templates/template-research-simple.md`

**When to Use**: Simple/Greenfield projects (minimal dependencies, quick validation needed)

**Target Project Types**: Generic, Simple Build, Quick Content

**Complexity**: Low (2-5 min quick validation)

### Template Content

```markdown
# Research Phase: [Project Name]

**Project Type**: Simple/Greenfield
**Research Date**: [Auto-generated timestamp]
**Status**: Quick Validation

---

## Purpose

**What we're validating**: [Auto-filled from project description]

**Why minimal research**: This is a greenfield/simple project with minimal dependencies. Quick validation ensures we're not reinventing the wheel.

**Time Budget**: 2-5 minutes (quick check)

---

## 1. Quick Codebase Check

**Goal**: Ensure we're not duplicating existing work

```bash
# Quick search for similar files
grep -r "[keyword]" --include="*.md"
ls 02-projects/ | grep -i "[keyword]"
```

**Findings**:
- [ ] Found: [path] - [Relevant? Yes/No - How to handle]
- [ ] Found: [path] - [Relevant? Yes/No - How to handle]

**Decision**:
- [ ] ✅ No conflicts - proceed
- [ ] ⚠️ Overlap found - [How to handle: merge/separate/rename]

---

## 2. Quick External Check

**Goal**: Verify no obvious tools/solutions already exist

**Quick Search**:
```
Google: "[what you're building] + tool"
Example: "markdown todo tracker tool"
```

**Findings**:
- [ ] Tool exists: [name] - Decision: [Use it / Build anyway because X]
- [ ] No tool found - Proceed with build

**Validation**:
- [ ] ✅ Building this makes sense
- [ ] ⚠️ Consider using existing: [name]

---

## 3. Dependency Quick List

**Files this might interact with**:
- [List any obvious files/systems]

**External systems/APIs** (if any):
- [List any external dependencies]

**Configuration** (if any):
- [Environment vars, config files]

---

## 4. Quick Risk Check

**Potential blockers** (if any obvious ones):
- [ ] [Blocker] - [Quick mitigation]

**Unknowns to test** (if any):
- [ ] [What needs quick validation]

**Decision**:
- [ ] ✅ No major risks - proceed
- [ ] ⚠️ Risk identified - [How to address]

---

## 5. Summary

**Research Time**: [X minutes]

**Key Finding**: [One-liner: proceed / use alternative / adjust approach]

**Dependencies for plan.md**:
- [Minimal list of files/systems]

**Recommendation**:
- ✅ Ready to plan and build

---

**Next Step**: Proceed to plan.md with minimal dependencies noted.
```

---

## Template Selection Logic

### Selection Algorithm

**Input**: Project description, project type (if known), user preference

**Output**: Recommended template + justification

### Decision Tree

```
START: User creates project with description

1. CHECK: Project Type Selected
   ├── IF "Build/Create" → EVALUATE complexity
   │   ├── IF mentions: integration, API, existing system, codebase
   │   │   → RECOMMEND: template-research-build.md
   │   │   → REASON: "Needs codebase + integration research"
   │   ├── ELSE IF: simple, greenfield, standalone
   │   │   → RECOMMEND: template-research-simple.md
   │   │   → REASON: "Minimal dependencies, quick validation"
   │   └── ELSE (uncertain)
   │       → OFFER: build vs. simple (ask user)
   │
   ├── IF "Research/Analysis" → EVALUATE scope
   │   ├── IF mentions: papers, academic, survey, literature
   │   │   → RECOMMEND: template-research-analysis.md
   │   │   → REASON: "Needs paper search + methodology design"
   │   ├── ELSE IF mentions: quick, validation, feasibility
   │   │   → RECOMMEND: template-research-simple.md
   │   │   → REASON: "Just need quick validation"
   │   └── ELSE (uncertain)
   │       → OFFER: analysis vs. simple (ask user)
   │
   ├── IF "Strategy/Planning" → OFFER research
   │   → RECOMMEND: template-research-simple.md (optional)
   │   → REASON: "Strategy may benefit from competitive research"
   │   → OPTIONAL: Offer to skip entirely
   │
   ├── IF "Content/Creative" → OFFER research
   │   → RECOMMEND: template-research-simple.md (optional)
   │   → REASON: "May want to check existing content/examples"
   │   → OPTIONAL: Offer to skip entirely
   │
   ├── IF "Process/Operations" → EVALUATE scope
   │   ├── IF mentions: existing process, workflow, system
   │   │   → RECOMMEND: template-research-build.md
   │   │   → REASON: "Needs understanding of current state"
   │   └── ELSE
   │       → RECOMMEND: template-research-simple.md
   │       → REASON: "Quick check for existing processes"
   │
   └── IF "Generic/Flexible" → ASK user
       → OFFER: All three options with brief descriptions
       → ALLOW: Skip research entirely

2. PRESENT RECOMMENDATION
   Format:
   """
   Based on your [project type] project focused on [description],
   I recommend a [template name] research phase ([time estimate]).

   This will help you:
   - [Benefit 1]
   - [Benefit 2]
   - [Benefit 3]

   Would you like to:
   1. Do this research now (recommended) - [X] minutes
   2. Use a simpler/different research approach
   3. Skip research and go straight to planning

   What would you prefer?
   """

3. HANDLE USER RESPONSE
   ├── IF "Yes" / "1" / "Do research"
   │   → LOAD template
   │   → GUIDE through research sections
   │   → SAVE to 01-planning/research.md
   │   → PRE-POPULATE plan.md Dependencies
   │
   ├── IF "Different approach" / "2"
   │   → OFFER other template options
   │   → EXPLAIN differences
   │   → PROCEED with user's choice
   │
   └── IF "Skip" / "3" / "No"
       → CONFIRM: "Understood. We'll proceed directly to planning."
       → PROCEED to overview.md (normal flow)
       → NOTE: Dependencies section in plan.md will be minimal

4. RESEARCH EXECUTION (if selected)
   → Guide user through template sections
   → Offer to run searches/scripts where applicable
   → Collect findings in structured format
   → Save to 01-planning/research.md
   → Extract key findings for plan.md

5. TRANSITION TO PLANNING
   → Load overview.md (normal flow continues)
   → When reaching plan.md:
      → IF research.md exists:
         → AUTO-POPULATE Dependencies section from research findings
         → REFERENCE research.md in Approach section
      → ELSE:
         → Minimal Dependencies section
         → Proceed normally

END
```

---

## Keyword Detection Rules

**For Build/Create Projects**:
- **Build Template Triggers**: integration, API, codebase, system, existing, modify, connect, deploy, database, auth, workflow
- **Simple Template Triggers**: new, greenfield, standalone, simple, quick, minimal, script, tool, utility

**For Research/Analysis Projects**:
- **Analysis Template Triggers**: paper, academic, research, literature, survey, systematic, analysis, competitive, market, study
- **Simple Template Triggers**: feasibility, validation, quick check, explore, investigate (brief)

**For All Projects**:
- **Skip Research Triggers**: "skip research", "no research needed", "just plan", "I know what I need"

---

## Integration Points in create-project Workflow

### Current Workflow (from workflows.md)

```
Step 1: Initialize TodoList
Step 2: Initial Discovery
Step 3: Validate Inputs
Step 4: Create Folder Structure (run init_project.py)
Step 5: Fill overview.md
Step 6: Interactive plan.md
Step 7: Interactive steps.md
Step 9: Update project-map.md
Step 10: Display Complete Structure
Step 11: Separate Session Instruction
Step 12: Auto-trigger close-session
```

### NEW Workflow (with Research Phase)

```
Step 1: Initialize TodoList
Step 2: Initial Discovery
Step 3: Validate Inputs
Step 4: Create Folder Structure (run init_project.py)

[NEW] Step 4.5: Research Phase Offering
├── Detect project type + complexity
├── Recommend research template (build/analysis/simple)
├── Present research value proposition
├── Handle user choice (do research / different approach / skip)
└── IF research selected:
    ├── Load appropriate template
    ├── Create 01-planning/research.md
    ├── Guide through research sections
    ├── Offer to run searches/scripts
    ├── Save completed research.md
    └── Extract findings for plan.md

Step 5: Fill overview.md (unchanged)

[MODIFIED] Step 6: Interactive plan.md
├── All existing steps (mental models, Socratic questions, etc.)
├── When reaching Dependencies & Links section:
│   ├── IF research.md exists:
│   │   → Auto-populate from research findings
│   │   → Add reference: "See research.md for details"
│   │   → Expand with additional AI research
│   └── ELSE:
│       → Normal dependency research flow (codebase scan)
└── Continue normal plan.md workflow

Step 7: Interactive steps.md (unchanged)
Step 9: Update project-map.md (unchanged)
Step 10: Display Complete Structure (unchanged)
Step 11: Separate Session Instruction (unchanged)
Step 12: Auto-trigger close-session (unchanged)
```

---

## Research Phase User Experience

### Example Interaction Flow 1: Build Project (Research Accepted)

```
User: "Create project for lead qualification workflow"

AI: [Detects Build type, integration keywords]

AI: "I'll create a project for lead qualification workflow.

This looks like a Build/Create project with integrations.

Before we dive into planning, I recommend a brief research phase (10-15 min)
to explore:
- Existing qualification logic in the codebase
- Integration points with Airtable/Slack
- Technical constraints and auth patterns

This research will save time during implementation by identifying reusable
patterns and avoiding conflicts.

Would you like to:
1. Do this research now (recommended) - 10-15 min
2. Skip research and plan directly
3. Use a simpler research approach (5 min quick check)

What would you prefer?"

User: "Yes, let's do the research"

AI: "Great! I'll guide you through focused research.

[Creates 01-planning/research.md from template-research-build.md]

Let's start with codebase analysis. I'll search for existing qualification
logic and related files...

[Runs searches, populates findings]

Section 1: Codebase Analysis
✓ Found: 03-skills/lead-qualification/SKILL.md (existing workflow!)
✓ Found: 04-workspace/airtable-schemas/leads.json (data schema)
✓ Found: Integration pattern in /auth (Slack auth)

[Continues through research sections...]

Research complete! Key findings:
1. Existing lead-qualification skill can be enhanced (don't rebuild)
2. Airtable base "Leads" already configured
3. Slack auth pattern established in /auth module

Saved to: 01-planning/research.md

Now let's use these findings to inform your plan..."

[Proceeds to overview.md, then plan.md with auto-populated Dependencies]
```

### Example Interaction Flow 2: Research Project (Research Accepted)

```
User: "Create project for ontologies research"

AI: [Detects Research type]

AI: "I'll create a project for ontologies research.

This is a Research/Analysis project. I recommend a comprehensive research
phase (15-20 min) to:
- Search for relevant academic papers
- Identify research methodology frameworks
- Check for related research already done

This will help define your research approach and avoid duplicating work.

Would you like to:
1. Do this research now (recommended) - 15-20 min
2. Skip research and plan directly
3. Use a simpler research approach

What would you prefer?"

User: "Yes, let's do the research"

AI: "Perfect! I'll guide you through research setup.

[Creates 01-planning/research.md from template-research-analysis.md]

First, let me search for related research projects...

[Searches 02-projects/ for similar research]

✓ Found: Project 16 - Ontologies Research V3 (completed)
  - 23 papers analyzed, synthesis complete
  - This could inform your approach!

Now let's search for academic papers on your topic.

What specific aspect of ontologies are you researching?
(e.g., foundational ontologies, process ontologies, AI integration)"

User: "Process ontologies for AI agent workflows"

AI: "Got it. I'll search academic sources...

[Runs paper-search skill]

python 03-skills/research-pipeline/skills/paper-search/scripts/paper_search.py \
  --query "process ontology AI agent" --limit 10

Found 10 papers. Top candidates:
1. "PROV-AGENT: Unified Provenance for AI Agents" (2024, 45 citations)
2. "BFO Process Classification" (2022, 120 citations)
3. "OCEL 2.0 Specification" (2024, 30 citations)

[Continues through research sections...]

Research complete! Summary:
- 10 relevant papers identified (5 selected for deep reading)
- Methodology: Systematic review + thematic synthesis
- Prior work: Project 16 provides foundation
- Time estimate: 2-3 weeks

Saved to: 01-planning/research.md

Now let's define your research plan..."

[Proceeds to overview.md, then plan.md with methodology pre-filled]
```

### Example Interaction Flow 3: Simple Project (Research Skipped)

```
User: "Create project for cleaning up old markdown files"

AI: [Detects Generic/Simple type]

AI: "I'll create a project for cleaning up old markdown files.

This looks like a simple maintenance task. I can offer a quick research
phase (2-5 min) to check for existing cleanup scripts or patterns.

Would you like to:
1. Do a quick check (5 min) - ensure we're not reinventing the wheel
2. Skip research and plan directly

What would you prefer?"

User: "Skip it, I know what needs to be done"

AI: "Understood. We'll proceed directly to planning.

[Runs init_project.py]

✓ Created project structure
✓ Created planning files

Let's fill in overview.md..."

[Proceeds to overview.md normally, plan.md will have minimal Dependencies]
```

---

## Research Output Format

### File Location
**Path**: `01-planning/research.md`

**Rationale**: Research is part of planning phase, not resources. Resources are acquired materials (papers, data). Planning includes research findings that inform approach.

### File Structure

```markdown
# Research Phase: [Project Name]

**Project Type**: [Build/Analysis/Simple]
**Research Date**: [ISO timestamp]
**Time Spent**: [X minutes]
**Status**: Complete

---

[Template sections filled in during research]

---

## Summary for Planning

**Key Findings** (copy to plan.md Dependencies):
1. [Finding 1]
2. [Finding 2]
3. [Finding 3]

**Recommendations**:
- [Recommendation 1]
- [Recommendation 2]

**Open Questions**:
- [Question 1]
- [Question 2]

---

**Next Step**: Use findings to inform plan.md
```

### Integration with plan.md

When plan.md is created after research:

```markdown
## Dependencies & Links

**Research Phase**: See [research.md](research.md) for detailed findings.

**Files Impacted** (from research):
- `[path]` - [purpose] (identified in codebase analysis)
- `[path]` - [purpose] (identified in codebase analysis)

**External Systems** (from research):
- [System] - [purpose] (identified in integration research)

**Related Projects** (from research):
- Project [ID]: [name] - [relationship] (identified in project scan)

**Additional Research** (AI's own dependency scan):
- [Additional files/systems found by AI during plan.md creation]

**Key Insights from Research**:
1. [Insight 1 from research summary]
2. [Insight 2 from research summary]
3. [Insight 3 from research summary]
```

---

## Template Files Summary

### File 1: template-research-build.md
- **Location**: `00-system/skills/projects/create-project/scripts/templates/template-research-build.md`
- **Size**: ~300 lines
- **Sections**: 6 (Codebase Analysis, External Research, Dependency Mapping, Risk Assessment, Architecture Insights, Summary)
- **Time**: 10-15 min
- **For**: Build/Create projects with integrations/dependencies

### File 2: template-research-analysis.md
- **Location**: `00-system/skills/projects/create-project/scripts/templates/template-research-analysis.md`
- **Size**: ~350 lines
- **Sections**: 6 (Codebase Context, External Research, Methodology Design, Scope & Constraints, Expected Outputs, Summary)
- **Time**: 15-25 min
- **For**: Research/Analysis projects requiring methodology design

### File 3: template-research-simple.md
- **Location**: `00-system/skills/projects/create-project/scripts/templates/template-research-simple.md`
- **Size**: ~100 lines
- **Sections**: 5 (Quick Codebase Check, Quick External Check, Dependency Quick List, Quick Risk Check, Summary)
- **Time**: 2-5 min
- **For**: Simple/Greenfield projects needing minimal validation

---

## Implementation Checklist

### Phase 1: Template Creation
- [ ] Create `template-research-build.md` with all sections
- [ ] Create `template-research-analysis.md` with all sections
- [ ] Create `template-research-simple.md` with all sections
- [ ] Test templates with dummy data

### Phase 2: Selection Logic
- [ ] Implement project type detection in create-project
- [ ] Implement keyword detection for complexity assessment
- [ ] Implement template recommendation algorithm
- [ ] Create user prompts for research offering
- [ ] Handle user responses (yes/different/skip)

### Phase 3: Workflow Integration
- [ ] Update `create-project/SKILL.md` with research phase docs
- [ ] Update `create-project/references/workflows.md` with new Step 4.5
- [ ] Update `create-project/references/project-types.md` with research recommendations
- [ ] Implement research.md creation and guidance flow
- [ ] Implement auto-population of plan.md Dependencies from research.md

### Phase 4: Testing
- [ ] Test with Build project (accept research)
- [ ] Test with Research project (accept research)
- [ ] Test with Simple project (skip research)
- [ ] Test with Generic project (different template)
- [ ] Verify plan.md auto-population works
- [ ] Verify research.md structure correct

### Phase 5: Documentation
- [ ] Update create-project skill documentation
- [ ] Add research phase examples
- [ ] Document template selection logic
- [ ] Add troubleshooting guide

---

## Success Metrics

**Research Phase Success**:
- [ ] Research findings reduce implementation rework
- [ ] Dependencies section in plan.md is comprehensive
- [ ] Research time stays within budget (5-25 min depending on template)
- [ ] Users understand when to use vs. skip research

**User Experience Success**:
- [ ] Research offering feels helpful, not forced
- [ ] Skip option is clear and guilt-free
- [ ] Templates guide research efficiently
- [ ] Findings transition smoothly to planning

**Technical Success**:
- [ ] Templates work for all project types
- [ ] Selection logic is accurate (>80% appropriate recommendations)
- [ ] Integration with plan.md is seamless
- [ ] Backward compatible (projects without research work fine)

---

## Future Enhancements

**Version 1.1**:
- [ ] Add research resume state (for long research sessions)
- [ ] Integrate with subagent system (parallel research tasks)
- [ ] Add research template customization (user can modify templates)
- [ ] Research time tracking and analytics

**Version 2.0**:
- [ ] AI-driven research automation (auto-run searches, summarize findings)
- [ ] Research collaboration mode (multiple people contribute)
- [ ] Research reuse across projects (research library)
- [ ] Advanced paper analysis integration (auto-extract key findings)

---

## Conclusion

This research template system provides:

1. **3 Templates** tailored to project complexity (Build, Analysis, Simple)
2. **Intelligent Selection** based on project type and keywords
3. **Optional but Encouraged** research phase (user retains control)
4. **Seamless Integration** with existing create-project workflow
5. **Structured Outputs** that feed directly into plan.md Dependencies

**Key Principles**:
- Research is planning (goes in `01-planning/research.md`)
- User choice is paramount (always offer skip option)
- Templates guide, don't constrain (sections are flexible)
- Findings are actionable (must inform plan.md)
- Time-boxed and focused (no endless research)

**Implementation Priority**: High (Phase 2 of Project 24)

---

**Document Status**: COMPLETE - Ready for implementation
**Next Step**: Create template files and integrate into create-project workflow

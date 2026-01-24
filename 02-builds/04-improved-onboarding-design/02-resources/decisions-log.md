# Decisions Log - Improved Onboarding Design

> **Build**: 04-improved-onboarding-design
> **Date**: 2026-01-24
> **Status**: Planning Complete - Ready to Write Plan

---

## **FINAL DECISIONS**

### **1. Heroic Intro**

**Style**: Real examples with personality, no BS marketing speak

**Structure**:
- ASCII art header
- "Welcome to Nexus (Powered by Claude Code)"
- Old model vs New model comparison
- 5 named real-world systems with icons
- Why it works (compounds)
- Call to action

**Named Systems**:
1. 🔬 "MedScan" - Medical Research Platform
2. 💼 "JobTracker" - Application Automation
3. 🏃 "FitPlan" - Personal Performance Lab
4. 📝 "ContentEngine" - LinkedIn Production System
5. 🗺️ "ProductOS" - Strategy & Roadmap System

**Key Messages**:
- "ChatGPT gives you answers. Nexus builds you SYSTEMS."
- Real dad/girlfriend stories (MRI analysis, job tracking, smartwatch)
- "Used throughout our company, people dropped required tools"
- "You build it once. It works forever."

---

### **2. Onboarding Flow**

**Session 1 Structure**:
```
1. Heroic Intro
2. Language Selection
3. Fork Decision:
   → Path A: Tour (how-nexus-works skill, ~7 min)
   → Path B: Direct (setup-system skill, ~10-15 min)
4. End with session boundary teaching
5. User opens NEW chat for next step
```

**Session 2+ Structure**:
```
IF tour_complete AND NOT setup_complete:
  → Load setup-system skill (mandatory)

ELIF setup_complete AND NOT first_build_started:
  → Show roadmap, suggest first build
  → Load plan-build skill
  → Include learn-builds explanation (first-time only)

ELSE:
  → Normal operation (menu)
```

**Key Principle**: Clean session boundaries, one focus per session

---

### **3. Merged setup-system Skill**

**Combines**: setup-memory + create-roadmap + create-folders + project initiation

**Duration**: 10-15 minutes (including SubAgent analysis if files uploaded)

**Flow**:
1. **Context Upload** (optional)
   - User drops files → 04-workspace/input/
   - SubAgent analysis → file-analysis.json

2. **Core Question**: "Who are you, OR what do you want to achieve/build?"
   - Extracts: role, goals, system type

3. **Generate Roadmap**
   - Based on: user answer + file insights + integrations
   - User confirms/refines

4. **Create Workspace Structure**
   - Based on: roadmap + file themes + work patterns
   - User confirms/refines

5. **Initiate Projects**
   - Create full scaffold for each roadmap item
   - Fill ONLY 01-overview.md
   - Include dependencies

6. **Save Everything**
   - goals.md, roadmap.md, workspace-map.md
   - Archive onboarding project

7. **End Session**
   - Teach session boundaries
   - Prompt to open new chat

**Cross-Session Continuity**:
- State tracking: `setup_system_state.step_completed: 0-6`
- Resume from last completed step if session compacts

---

### **4. SubAgent File Analysis**

**Assignment Logic**:
- **Based on KB, not file count**
- No max agent limit (can go beyond 10 if needed)
- Every ~2MB = 1 agent

**File Handling**:
- Auto-split files >2MB (context risk)
- Thematic clustering by filename
- Ask user to confirm/refine clusters

**SubAgent Invocation**:
- Prompt file: `00-system/core/nexus/prompts/subagent-file-analysis.md`
- Parallel execution (up to 10+ agents)
- Pass: prompt path + files to analyze + metadata

**Output Contract**:
```json
{
  "file_analyses": [
    {
      "filename": "...",
      "path": "...",
      "type": "document|spreadsheet|code|data",
      "summary_short": "One sentence",
      "summary_detailed": "Full understanding of content",
      "theme": "clients|sales|research|etc",
      "detected_entities": ["names", "companies", "amounts"],
      "suggested_folder": "relative/path/"
    }
  ],
  "professional_context": {...},
  "integration_opportunities": [
    {
      "name": "HubSpot CRM",
      "type": "CRM",
      "evidence": "...",
      "suggestion": "..."
    }
  ],
  "workspace_structure_suggestion": {...}
}
```

**No file_map.md**: Analysis stored in onboarding project instead

---

### **5. File Organization Strategy**

**Onboarding Project Approach** (FINAL):

```
02-builds/00-onboarding-session/
├── 01-planning/
│   ├── 01-overview.md (purpose: "Set up YOUR Nexus system")
│   └── 04-steps.md (onboarding checklist)
│
├── 02-resources/
│   ├── file-analysis.json (SubAgent output - full detail)
│   └── file-analysis-summary.md (human-readable)
│
├── 03-working/
│   └── input/ → symlink to 04-workspace/input/
│
└── 04-outputs/
    ├── goals.md (moves to 01-memory/)
    ├── roadmap.md (moves to 01-memory/)
    └── workspace-structure.md (proposed folders)
```

**Lifecycle**:
1. Create on Session 1 start
2. SubAgent saves analysis to 02-resources/
3. During setup: files moved from input/ → organized folders
4. After complete: Archive to 05-archived/

**workspace-map.md gets clean version**:
- Folder structure with purposes
- File organization principle
- Usage notes
- Reference to archived analysis

**Benefits**:
- Traceable (can review analysis later)
- Follows system patterns (it's a build!)
- Clear lifecycle (active → archived)
- No redundant files in 01-memory/

---

### **6. Project Scaffolding**

**Full Structure Created**:
```
02-builds/XX-name/
├── 01-planning/
│   ├── 01-overview.md (FILLED)
│   ├── 02-discovery.md (EMPTY)
│   ├── 03-plan.md (EMPTY)
│   ├── 04-steps.md (EMPTY)
│   └── resume-context.md (standard)
├── 02-resources/
├── 03-working/
└── 04-outputs/
```

**01-overview.md Contents**:
- Purpose (from roadmap)
- Success criteria (AI-generated, 3 items)
- Context (user goal + file insights)
- Dependencies (from roadmap)
- Next steps (how to start)

**For Integration Projects**:
- Same structure
- Type: "integration"
- Overview includes: what to connect, why, how

---

### **7. State Management**

**Granular Status Values**:
```yaml
onboarding:
  status:
    - "not_started"
    - "tour_complete"
    - "system_setup_complete"
    - "first_build_started"
    - "complete"

  in_progress_skill: null | "how-nexus-works" | "setup-system"

  setup_system_state:
    step_completed: 0-6
    files_uploaded: bool
    file_analysis_done: bool
    role_captured: bool
    goals_captured: bool
    roadmap_created: bool
    workspace_created: bool
    projects_initiated: bool

  language_preference: "en" | "de" | "es" | etc.
  chosen_path: "tour" | "direct"
```

**SessionStart Resume Logic**:
- Check `in_progress_skill`
- If "setup-system" → load state, resume from step
- If "how-nexus-works" → resume skill
- Else → route based on status

---

### **8. Session Boundary Teaching**

**When Taught**:
1. End of how-nexus-works skill
2. End of setup-system skill
3. End of first build (in learn-builds explanation)
4. When user switches topics mid-session (detection)

**Message**:
```
"Your progress saves automatically.

IMPORTANT: Clean session boundaries matter in Nexus.
Each session = one focus.

This session: [what was accomplished] ✓
Next session: [what comes next]

→ Open a NEW chat when ready to continue"
```

**Don't say**: "Say 'close' to end session"
**Do say**: "Open a NEW chat/session"

---

## **KEY IMPLEMENTATION TASKS**

### **Priority 1: Core Skills**
1. Create `how-nexus-works` skill (7 min tour)
2. Create `setup-system` skill (merged, 10-15 min)
3. Create SubAgent prompt file (`subagent-file-analysis.md`)

### **Priority 2: Templates**
4. Write heroic intro copy (startup_first_run.md)
5. Update SessionStart templates (all 7)
6. Create language selection screen

### **Priority 3: State & Infrastructure**
7. Update user-config.yaml schema (granular status)
8. Implement SessionStart resume logic
9. Add onboarding project auto-creation

### **Priority 4: SubAgent Logic**
10. Implement KB-based agent assignment
11. Implement auto-file-splitting (>2MB)
12. Implement thematic clustering
13. Create synthesis logic (combine agent outputs)

### **Priority 5: Project Scaffolding**
14. Implement full scaffold creation
15. Implement overview.md template with AI generation
16. Add dependency tracking

---

## **WHAT WE'RE NOT DOING**

❌ No separate file_map.md in 01-memory/
❌ No mandatory linear onboarding (fork allows choice)
❌ No fixed agent count (KB-based, can scale beyond 10)
❌ No file count limits for SubAgent analysis
❌ No "say close" messaging (new chat instead)
❌ No default menu (blocked until setup complete)
❌ No separate create-folders skill (merged into setup-system)
❌ No separate create-roadmap skill (merged into setup-system)

---

## **SUCCESS CRITERIA**

**Onboarding Complete When**:
1. ✅ User has completed setup-system skill
2. ✅ goals.md exists with real content
3. ✅ roadmap.md exists with projects
4. ✅ workspace-map.md exists with structure
5. ✅ At least 1 project scaffold created
6. ✅ User understands session boundaries

**Quality Metrics**:
- Onboarding completion rate >90%
- Time to first build <20 minutes
- User returns for Session 2 >80%
- Churn during onboarding <5%

---

**Last Updated**: 2026-01-24
**Status**: Planning Complete - Ready to execute

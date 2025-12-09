# Workshop Context System - Complete Overview

**Created**: 2025-11-25
**Purpose**: Document the complete workshop context system for Nexus product introduction
**Status**: Production Ready

---

## 🎯 System Overview

The workshop context system programs the Nexus onboarding experience for Solutions Engineers attending the 90-minute product introduction workshop. It guides participants toward Skills-first thinking while allowing them to import existing work for immediate value.

---

## 📁 Files Created

### 1. **WORKSHOP-CONTEXT.md**
**Location**: `04-workspace/input/WORKSHOP-CONTEXT.md`
**Type**: MANDATORY AI context file
**Loaded**: During Project 00 (Define Goals) when present

**Purpose**:
- Guide AI to provide workshop-specific onboarding experience
- Program goals/roadmap creation toward Skills library focus
- Provide Solutions Engineer context (7-phase client lifecycle)
- Enable import analysis and Skills extraction opportunities

**Key Features**:
- ✅ Workshop participant profile templates
- ✅ Goal templates aligned with 7-phase lifecycle
- ✅ Roadmap milestones focused on Skills creation
- ✅ Import detection and analysis guidance
- ✅ Real workshop quotes and scenarios (Hassan, Jack, Fahad, Muj, Dorian)
- ✅ Workshop success metrics checklist
- ✅ Post-workshop next steps (90-day plan)
- ✅ Facilitator notes and common scenarios
- ✅ "Workshop magic moments" to create

**AI Behavior Changes When Loaded**:
1. **Skills-first mindset**: Guides toward reusable workflows, not one-time projects
2. **Import analysis**: Analyzes files in `04-workspace/input/` for Skills extraction
3. **Real examples**: Uses participant's actual work to ground Skills creation
4. **Team multiplier vision**: Reinforces Dorian's "10 people automating each other"
5. **Workshop timing**: Optimized for 55-minute hands-on session
6. **Success validation**: Checks workshop metrics before close-session

---

### 2. **IMPORT-INSTRUCTIONS.md**
**Location**: `04-workspace/input/IMPORT-INSTRUCTIONS.md`
**Type**: User reference guide
**Read**: BEFORE starting Project 00 onboarding

**Purpose**:
- Instruct participants on importing existing work
- Explain what to import (old Nexus v2, scattered files, templates)
- Show what AI will do with imported files
- Provide real examples (Hassan's import scenario)

**Key Features**:
- ✅ Import examples (old Nexus v2, client projects, templates, process docs)
- ✅ Import checklist (what to bring)
- ✅ What happens during onboarding (AI analysis steps)
- ✅ Real workshop example (Hassan's staging/production pain)
- ✅ What NOT to import (sensitive data, large files)
- ✅ Post-workshop import usage (ongoing inbox pattern)

**Import Categories Supported**:
1. **Old Nexus v2 workspaces** → Upgrade to v3
2. **Scattered client files** → Organize into 4-folder pattern
3. **Templates & workflows** → Convert to Skills
4. **Team documentation** → Extract reusable processes

---

### 3. **workspace-map.md** (Updated)
**Location**: `04-workspace/workspace-map.md`
**Type**: AI navigation file
**Loaded**: Every session via --startup

**Changes Made**:
- ✅ Added `input/` folder documentation
- ✅ Explained WORKSHOP-CONTEXT.md auto-detection
- ✅ Explained IMPORT-INSTRUCTIONS.md purpose
- ✅ Documented import workflow for AI
- ✅ Clarified workshop vs regular user modes

---

## 🔄 How the System Works

### Auto-Detection Flow

```
Session starts
    ↓
AI loads workspace-map.md (via --startup)
    ↓
Check: 04-workspace/input/WORKSHOP-CONTEXT.md exists?
    ↓
┌──YES─────────────────────┐  ┌──NO──────────────────┐
│ WORKSHOP PARTICIPANT MODE │  │ REGULAR USER MODE    │
│                           │  │                      │
│ 1. Load WORKSHOP-CONTEXT  │  │ 1. Standard Project  │
│ 2. Check for imports in   │  │    00 onboarding     │
│    04-workspace/input/    │  │ 2. No import         │
│ 3. Analyze imported files │  │    analysis          │
│ 4. Extract Skills opps    │  │ 3. Generic goals     │
│ 5. Use SE templates       │  │                      │
│ 6. Skills-first guidance  │  │                      │
└───────────────────────────┘  └──────────────────────┘
```

### Workshop Onboarding Flow (55 minutes)

```
Minute 0-10: Import Analysis
    ↓
AI: "I see you imported [files/folders]. Let's analyze..."
    • Detect old Nexus v2 → offer upgrade
    • Detect scattered files → show organization opportunity
    • Detect templates → identify Skills extraction
    • Detect process docs → extract workflows
    ↓
Minute 10-25: Goals Creation (Workshop Templates)
    ↓
AI uses WORKSHOP-CONTEXT.md templates:
    • Current Role: Solutions Engineer at [Company]
    • Current Client: [FinTech/etc.] in Phase [X]
    • 3-Month Goal: Build Skills library from actual work
    • Success Metrics: 10+ Skills, team reuse, 50% speedup
    ↓
Minute 25-40: Roadmap Creation (7-Phase Lifecycle Focus)
    ↓
AI suggests milestones aligned with participant's work:
    • Milestone 1: Organize current client (Weeks 1-2)
    • Milestone 2: Extract 3 Skills (Weeks 3-4)
    • Milestone 3: Team multiplier (Month 2)
    • Milestone 4: Exponential growth (Month 3)
    ↓
Minute 40-50: First Skill Identification (Not Built Yet)
    ↓
AI: "From your imported files, I found these repetitive workflows:
     1. Weekly client updates (4 hrs → 30 min)
     2. Test report generation (3 hrs → 20 min)
     3. API doc gathering (40% of discovery)

     Which pain point hurts most? That's your first Skill."
    ↓
Minute 50-55: Workshop Success Validation
    ↓
AI checks workshop metrics:
    ✅ goals.md created with current client context
    ✅ roadmap.md with 4 milestones
    ✅ 1-3 Skills identified (with time savings estimates)
    ✅ Understanding: Projects vs Skills
    ✅ "Aha moment" about team multiplier
    ↓
close-session → All work saved
```

---

## 🎓 Workshop Integration

### Pre-Workshop (Facilitator Setup)

1. **Slide deck ready**: [slides-solutions-version.md](../03-working/slides-solutions-version.md) (10 slides, 30 min)
2. **Workshop guide ready**: [workshop-guide.md](workshop-guide.md) (facilitator playbook)
3. **Context files in place**: WORKSHOP-CONTEXT.md + IMPORT-INSTRUCTIONS.md

### During Workshop (Phase 2: Hands-On, 55 minutes)

**Facilitator announces**:
> "Before we start, please import your existing work:
>  - Copy old Nexus workspaces into `04-workspace/input/`
>  - Copy scattered client folders from Desktop/Downloads
>  - Copy email templates you reuse every week
>  - Copy any workflow you do for EVERY client
>
>  During onboarding, AI will analyze what you imported and
>  help you extract Skills from your actual work."

**Participants work through**:
- Project 00 (Define Goals) with AI guidance
- AI auto-detects workshop context
- AI analyzes imported files
- AI guides toward Skills-first goals
- AI suggests roadmap milestones

### Post-Workshop (Weeks 1-4)

**Week 1-2: Foundation**
- Continue using Nexus for current client
- Experience instant context (close-session → reload)
- Zero time hunting for files

**Week 3-4: First Skill**
- Pick most painful repetitive task
- Use create-skill to convert to workflow
- Test on current client
- Share with 1 team member

**Month 2-3: Team Multiplier & Exponential Growth**
- Share Skills with entire team
- Start second client using Skills library
- Measure 50% speedup
- Prove path to 2x capacity

---

## 📊 Success Metrics

### Workshop Completion (End of 90 minutes)

**Participants should have**:
- ✅ Nexus workspace set up
- ✅ goals.md with current client context
- ✅ roadmap.md with 4 Skills-focused milestones
- ✅ 1-3 Skills identified from actual work
- ✅ Understanding of Projects vs Skills
- ✅ "Aha moment" about team multiplier vision

### Week 4 (First Skill Built)

- ✅ 1 working Skill from most painful task
- ✅ 80% time savings on that task
- ✅ Tested on current client work
- ✅ Shared with 1 team member for feedback

### Month 3 (Exponential Growth Proven)

- ✅ 10+ Skills in library (from first client)
- ✅ Team using 5+ Skills on their clients
- ✅ Second client 50% faster than first
- ✅ <10% rework rate
- ✅ Measurable path to 2x team capacity

---

## 🔑 Key Design Decisions

### 1. **Non-Forcing Guidance**
- WORKSHOP-CONTEXT.md GUIDES goals/roadmap creation
- Does NOT force specific goals
- Participant still sets their own objectives
- Templates are suggestions, not requirements
- **Principle**: Guided autonomy, not prescription

### 2. **Import-First Philosophy**
- Participants import BEFORE onboarding starts
- AI analyzes real work, not abstract examples
- Skills extracted from actual pain points
- Immediate value: "My work → organized + automated"
- **Principle**: Start with reality, not theory

### 3. **Skills-First Mindset**
- Every template emphasizes reusable workflows
- Questions probe for repetitive patterns
- Projects = one-time, Skills = every time
- Team multiplier vision reinforced throughout
- **Principle**: Build library, not individual projects

### 4. **7-Phase Lifecycle Alignment**
- All templates reference SE's actual client lifecycle
- Pain points mapped to specific phases
- Skills organized by which phase they accelerate
- Roadmap milestones align with lifecycle progression
- **Principle**: Framework fits the work, not vice versa

### 5. **Real Workshop Language**
- Uses actual quotes from Nov 2024 workshop
- Hassan's "20 days lost", Jack's "integration time"
- Dorian's "10 people automating each other"
- Fahad's "consistency over speed"
- **Principle**: Authentic language, not marketing speak

---

## 🛠️ Technical Implementation

### File Detection (AI Logic)

```python
# During --startup or Project 00 load
workshop_context_path = "04-workspace/input/WORKSHOP-CONTEXT.md"

if file_exists(workshop_context_path):
    mode = "workshop_participant"
    load_file(workshop_context_path)  # MANDATORY
    analyze_imports("04-workspace/input/")  # Check for imported files
else:
    mode = "regular_user"
    # Standard Project 00 onboarding
```

### Import Analysis (AI Logic)

```python
# When WORKSHOP-CONTEXT.md is loaded
import_folder = "04-workspace/input/"
imported_items = scan_directory(import_folder, exclude=["*.md"])

for item in imported_items:
    if is_directory(item):
        if contains_nexus_v2_structure(item):
            suggest_upgrade_to_v3(item)
        elif contains_scattered_files(item):
            suggest_4_folder_organization(item)

    if is_template_file(item):
        suggest_skill_extraction(item)

    if is_process_doc(item):
        suggest_workflow_skill(item)
```

### Skills Extraction (AI Logic)

```python
# Identify repetitive patterns
def identify_skills_opportunities(imported_files):
    patterns = []

    # Email templates
    email_templates = find_files(imported_files, pattern="*email*template*")
    if len(email_templates) >= 3:
        patterns.append({
            "type": "Weekly Client Updates",
            "files": email_templates,
            "time_savings": "4 hours → 30 minutes",
            "skill_name": "update-automation"
        })

    # Test reports
    test_files = find_files(imported_files, pattern="*test*report*")
    if len(test_files) >= 3:
        patterns.append({
            "type": "Test Report Generation",
            "files": test_files,
            "time_savings": "3 hours → 20 minutes",
            "skill_name": "report-builder"
        })

    # API docs
    api_docs = find_files(imported_files, pattern="*api*spec*")
    if len(api_docs) >= 2:
        patterns.append({
            "type": "API Documentation Gathering",
            "files": api_docs,
            "time_savings": "40% of discovery phase",
            "skill_name": "api-doc-gatherer"
        })

    return patterns
```

---

## 📝 Usage Examples

### Example 1: Workshop Participant (With Imports)

**Participant**: Sarah, SE at AI Agent Company
**Imported**: Scattered FinTech client files (47 files across Desktop/Downloads)

**AI Experience**:
```
AI: "Welcome Sarah! I see you imported 'fintech-client-scattered/'
     with 47 files. Let me analyze...

     Found:
     • 15 email templates (weekly client updates)
     • 8 test result CSVs with manual reports
     • 12 API spec PDFs

     You're in Phase 4 (Build & Implement) of the 7-phase lifecycle.

     Your biggest time sinks:
     1. Weekly updates: 4 hours every Friday
     2. Test reports: 3 hours per report
     3. API doc gathering: 40% of discovery time

     Let's build your goals around turning these into Skills.

     Suggested 3-month goal:
     'Build Skills library from FinTech client to enable 2x capacity'

     Does this resonate with what you want to achieve?"
```

### Example 2: Workshop Participant (Old Nexus v2)

**Participant**: Hassan
**Imported**: Old Nexus v2 workspace with staging/production duplication

**AI Experience**:
```
AI: "Hassan, I see you imported an old Nexus v2 workspace.
     Great! We can upgrade this to v3 and extract Skills.

     I noticed a pattern:
     • client-a-staging/ and client-a-production/ (duplicates)
     • Only difference: API keys
     • You mentioned '20 days lost' in the workshop

     This is your Phase 7 pain point: Manual environment migrations.

     Let's build a 'Version Rollout Skill' that automates
     staging → production with one command.

     That's your first Skill. Want to make that your Week 3-4 milestone?"
```

### Example 3: Regular User (No Workshop Context)

**User**: Regular Nexus user, not in workshop
**Imported**: Nothing in `04-workspace/input/`

**AI Experience**:
```
AI: "Welcome to Nexus! Let's start by defining your goals.

     ## Current Role
     [What's your current role and work context?]

     ## Short-Term Goal (3 months)
     [What do you want to achieve in the next 3 months?]

     ## Long-Term Vision (1-3 years)
     [Where do you want to be in 1-3 years?]"
```

**Note**: Standard Project 00 onboarding, no workshop-specific guidance.

---

## 🚀 Future Enhancements

### Potential Additions (Not Implemented Yet)

1. **Skills Library Browser**: Show pre-built Skills from other workshop participants
2. **Team Dashboard**: Visualize team Skills usage and time savings
3. **ROI Calculator**: Auto-calculate time savings from Skills creation
4. **Skills Marketplace**: Share Skills across different Solutions teams
5. **Migration Tool**: Automated Nexus v2 → v3 upgrade script

---

## ✅ Validation Checklist

**Before workshop, verify**:
- [ ] WORKSHOP-CONTEXT.md exists in `04-workspace/input/`
- [ ] IMPORT-INSTRUCTIONS.md exists in `04-workspace/input/`
- [ ] workspace-map.md documents input/ folder
- [ ] Slides ready ([slides-solutions-version.md](../03-working/slides-solutions-version.md))
- [ ] Workshop guide ready ([workshop-guide.md](workshop-guide.md))
- [ ] Test AI auto-detection (create WORKSHOP-CONTEXT.md, start session, verify mode)

**During workshop, verify**:
- [ ] AI detects workshop mode when WORKSHOP-CONTEXT.md present
- [ ] AI analyzes imported files and suggests Skills
- [ ] AI uses workshop templates for goals/roadmap
- [ ] AI reinforces Skills-first mindset
- [ ] Workshop success metrics met before close-session

**After workshop, verify**:
- [ ] Participants have goals.md with Skills focus
- [ ] Participants have roadmap.md with 4 milestones
- [ ] Participants identified 1-3 Skills from actual work
- [ ] Participants understand team multiplier vision
- [ ] Participants ready for Week 3-4 Skill creation

---

**Document Status**: Complete
**System Status**: Production Ready
**Files Created**: 3 (WORKSHOP-CONTEXT.md, IMPORT-INSTRUCTIONS.md, workspace-map.md update)
**Integration**: Fully integrated with Project 00 onboarding flow
**Testing Required**: AI auto-detection, import analysis, Skills extraction logic

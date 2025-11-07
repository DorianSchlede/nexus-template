# Tasks: First Project (Project 01) - V2.0

**Project ID**: 01-first-project
**Onboarding Step**: 2 of 4
**Estimated Time**: 10-14 minutes (OPTIMIZED from 13-18 min)
**Philosophy Version**: 2.0 - CAVE Compliant

---

## 🎯 Design Principles

**This session follows these principles**:
1. ✅ **Experience First**: Create workspace BEFORE explaining framework
2. ✅ **Vocabulary Control**: Only 4 new terms (defer YAML, trigger phrases to P02)
3. ✅ **Habit Reinforcement**: Brief close-session reminder (you already practiced)
4. ✅ **Efficient Timing**: 10-14 minutes total
5. ✅ **Grounded Learning**: Framework taught AFTER you experience workspace creation

---

## Context Loading

**CRITICAL**: Load goals.md + roadmap.md at start!

```bash
python nexus-loader.py --project 01
```

**Extract**:
- USER_ROLE (from goals.md)
- SHORT_TERM_GOAL (from goals.md)
- USER_DOMAIN (infer from role/goal)
- MILESTONES (from roadmap.md)

---

## Section 1: Welcome Back + Context Confirmation (1-2 min)

- [ ] **Task 1.1**: Welcome user back
  - Say: "Welcome back! Ready for Project 01?"
  - Say: "Let me load your goals..."
  - Execute: Load goals.md + roadmap.md
  - Time: 15 seconds

- [ ] **Task 1.2**: Quick close-session reminder
  - Say: "Quick reminder: We'll practice close-session again at the end"
  - Time: 10 seconds

- [ ] **Task 1.3**: Confirm loaded context
  - Say: "I see your goal: [SHORT_TERM_GOAL]"
  - Say: "Today we'll create your workspace and first real project aligned with this goal"
  - Time: 15 seconds

- [ ] **Task 1.4**: Set session expectations
  - Say: "Here's what we'll do in 10-14 minutes:"
  - List:
    - "1. Design your workspace together (3-7 folders for YOUR work)"
    - "2. I'll explain how I made those decisions using Projects vs Skills framework"
    - "3. Create your first real project using create-project skill"
    - "4. Practice close-session to build the habit"
  - Ask: "Ready to begin?"
  - Time: 45 seconds

**Section Time**: 1-2 minutes

---

## 🎬 CAVE PHASE 1: ACTION FIRST (Experience Before Explanation)

---

## Section 2: Workspace Design (3-4 min)

**AI Note**: I create workspace FIRST, explain framework AFTER (grounded learning)

- [ ] **Task 2.1**: Analyze your goals (internal)
  - I review: USER_GOAL, USER_DOMAIN, USER_ROLE
  - I think: What folders support YOUR work?
  - Time: 10 seconds (internal)

- [ ] **Task 2.2**: Collaborative workspace brainstorming (ENHANCED)
  - Say: "Let's design your workspace together. I'll suggest a structure, then YOU refine it."
  - Say: "Remember: This is YOUR workspace. It should match how YOU think about your work."
  - Step 1: Present initial suggestions (1 min)
    - I suggest: 3-7 folders matching [USER_DOMAIN]
    - I explain: WHY each folder supports [SHORT_TERM_GOAL]
    - Example: "Clients/ → organize client projects as you onboard them"
    - Example: "Templates/ → reusable documents for proposals, contracts"
  - Step 2: Invite iteration (30 sec)
    - Say: "This is just my first pass. What would you change?"
    - Say: "• Different folder names that make more sense to you?"
    - Say: "• Missing folders you know you'll need?"
    - Say: "• Folders you want to combine or split?"
  - Step 3: Teach structure emergence
    - Say: "Here's a tip: It's okay if the structure isn't perfect now."
    - Say: "As you work, patterns will emerge. You can always add/rename folders."
    - Say: "Nexus adapts to YOUR workflow, not the other way around."
  - Time: 2 minutes total

- [ ] **Task 2.3**: Get your confirmation/adjustment
  - I ask: "Does this structure make sense for YOUR work?"
  - I allow: You to modify my suggestions
  - I confirm: Final folder list (3-7 folders)
  - Time: 1 minute

- [ ] **Task 2.4**: Create 04-workspace/ structure
  - I create: 04-workspace/ directory
  - I create: Your chosen folders (3-7)
  - I confirm: "✅ Workspace created with [list folders]"
  - Time: 30 seconds

- [ ] **Task 2.5**: File structure walkthrough (NEW - ORIENTATION)
  - Say: "Let me show you how to navigate your new workspace."
  - Step 1: Show folder tree
    - Display: Updated Nexus-v3/ tree showing new workspace folders
    - Highlight: 04-workspace/ now has YOUR folders
  - Step 2: Demonstrate sidebar navigation
    - Say: "In your file sidebar (left), you'll see all these folders"
    - Say: "Click any folder to expand it"
    - Say: "This is where you'll organize YOUR work files"
  - Step 3: Demo file operations
    - Say: "You can:"
    - Say: "• Create new files: Right-click folder → New File"
    - Say: "• Move files: Drag and drop"
    - Say: "• Reference with @: Type @ and select files"
  - Say: "Your workspace is ready—now let's understand WHY it's structured this way."
  - Time: 1.5 minutes

**Section Time**: 4.5-5.5 minutes
**Value Delivered**: ✅ Working workspace + navigation confidence

---

## 💡 CAVE PHASE 2: EXPLANATION (Now Grounded in Experience)

---

## Section 3: Projects vs Skills Framework (2 min)

**AI Note**: You just created workspace - NOW I explain the thinking behind it

- [ ] **Task 3.1**: Ground explanation in your workspace
  - I say: "Let me explain how I designed your workspace"
  - I say: "I used something called the Projects vs Skills framework"
  - I reference: The workspace you JUST created
  - Time: 20 seconds

- [ ] **Task 3.2**: Present framework
  - I say: "Quick 2-step framework for organizing work:"
  - I explain **Step 1**: "Is this direction (Goal) or work? If direction → it's a Goal"
  - I explain **Step 2**: "Does this work repeat? If no → Project. If yes → Skill"
  - I show: Visual decision tree (from design.md)
  - Time: 1 minute

- [ ] **Task 3.3**: Connect to YOUR workspace
  - I say: "For your [folders], here's how I used this framework:"
  - I give example: "Clients/ will hold Projects (one-time client work)"
  - I give example: "When you repeat the same workflow multiple times, we'll create Skills"
  - I provide: 1-2 examples from YOUR domain
  - Time: 30 seconds

- [ ] **Task 3.4**: Confirm understanding
  - I ask: "Does this framework make sense now that you see it applied to YOUR workspace?"
  - I wait for your confirmation
  - Time: 10 seconds

- [ ] **Task 3.5**: Address "Project" terminology confusion (NEW)
  - Say: "Quick clarification—the word 'Project' can be confusing."
  - Say: "In Nexus, 'Project' means: temporal work that ENDS and produces a deliverable."
  - Say: "Some prefer thinking of it as a 'Task' or 'Initiative'—choose what works for YOU."
  - Say: "The key question is always:"
  - Display visual:
    ```
    ╔═══════════════════════════════════════╗
    ║  Does this work END or REPEAT?        ║
    ║                                       ║
    ║  END → Project/Task/Initiative        ║
    ║  REPEAT → Skill/Workflow              ║
    ╚═══════════════════════════════════════╝
    ```
  - Say: "That's the ONLY distinction that matters. Use whatever terminology makes sense to you."
  - Ask: "Does this clarify the framework?"
  - Time: 1 minute

**Section Time**: 3 minutes
**Terms I introduce**: Skills (new), Workspace (new)
**Total New Terms**: 2

---

## Section 4: Just-in-Time Organization Principle (1 min)

- [ ] **Task 4.1**: Quick principle explanation
  - I say: "One key principle: just-in-time organization"
  - I show anti-pattern: "DON'T create 15 empty folders on day 1"
  - I show good pattern: "DO start with 3-7 folders, grow as work emerges"
  - I connect to your workspace: "Your [X] folders are just what you need for [GOAL]"
  - Time: 1 minute

**Section Time**: 1 minute
**Term I introduce**: just-in-time
**Total New Terms**: 1

---

## 🎬 CAVE PHASE 3: MORE ACTION (Continues Value Delivery)

---

## Section 5: First Project Creation via create-project Skill (5-7 min)

- [ ] **Task 5.1**: Introduce slicing + suggest project ideas (ENHANCED)
  - Step 1: Introduce project slicing concept (30 sec)
    - Say: "Let's create your first project. But first, an important concept: SLICING."
    - Say: "Big goals like '[SHORT_TERM_GOAL]' contain multiple projects."
    - Say: "Each project should be small enough to complete in 2-4 weeks."
    - Say: "Why? Because completing projects builds momentum. Big goals feel overwhelming."
  - Step 2: Analyze goal and slice into projects (1 min)
    - I analyze: USER_GOAL from goals.md
    - I identify: 3-5 distinct projects within your goal
    - Example: Goal "Launch consulting" might slice into:
      - "Define service offering"
      - "Build client proposal system"
      - "Create case study #1"
      - "Establish pricing model"
      - "Launch marketing channel"
  - Step 3: Suggest ONE to start with (30 sec)
    - I suggest: The FIRST project (foundational, unlocks others)
    - I explain: Why this one first
    - Example: "Let's start with 'Define service offering' because everything else depends on knowing what you're selling"
  - Step 4: Teach the benefits
    - Say: "By slicing your goal, you get:"
    - Say: "• Clear milestones (finish projects, not vague progress)"
    - Say: "• Focus (work on ONE thing at a time)"
    - Say: "• Motivation (celebrate completed projects)"
  - Time: 2 minutes total

- [ ] **Task 5.2**: Get your choice
  - I ask: "Which resonates with you? Or propose your own!"
  - I confirm: Project you want to create
  - I verify: Aligns with your goal
  - Time: 1 minute

- [ ] **Task 5.3**: Introduce create-project skill
  - I say: "I'll use the create-project skill to guide us"
  - I say: "This walks through collaborative project design"
  - Time: 15 seconds

- [ ] **Task 5.4**: Load create-project skill
  - I execute: `python nexus-loader.py --skill create-project`
  - Time: automated (5 seconds)

- [ ] **Task 5.5**: Follow create-project skill workflow
  - I follow: create-project SKILL.md instructions exactly
  - Typical flow:
    1. Project overview conversation
    2. Requirements elicitation
    3. Design planning
    4. Task breakdown
    5. Create folder structure
    6. Write overview.md
    7. Write requirements.md
    8. Write design.md
    9. Write tasks.md
  - I keep focus on: YOUR project (not system mechanics)
  - Time: 4-5 minutes

- [ ] **Task 5.6**: Confirm project created
  - I say: "✅ First project created: [PROJECT_NAME]"
  - I say: "Location: 02-projects/[PROJECT_ID]-[project-name]/"
  - I say: "This project directly supports your goal: [USER_GOAL]"
  - Time: 20 seconds

**Section Time**: 5-7 minutes
**Term I introduce**: create-project
**Total New Terms**: 1

---

## Section 6: Wrap-Up (1-2 min)

- [ ] **Task 6.1**: Review what was created
  - I say: "Today you created:"
  - I list: "✅ 04-workspace/ with [X] folders designed for [GOAL]"
  - I list: "✅ First project: [project-name] in 02-projects/"
  - I list: "✅ Learned: Workspace design, Projects vs Skills framework, just-in-time organization"
  - Time: 30 seconds

- [ ] **Task 6.1.5**: Clarify Project-Skill independence (NEW)
  - Say: "Quick note: You DON'T need a project to create a skill."
  - Say: "Projects and Skills are completely independent:"
  - Display:
    ```
    Projects:  Temporal work with endpoint
    Skills:    Reusable workflows (no endpoint)
    ```
  - Say: "You can create a skill ANYTIME you notice yourself repeating work."
  - Say: "Next session (Project 02): You'll learn how to create skills."
  - Say: "But remember: They're independent—you don't need one to create the other."
  - Time: 30 seconds

- [ ] **Task 6.2**: Preview next session
  - I say: "Next session (Project 02): We'll extract a workflow from YOUR project and create your first skill"
  - I say: "That's where you'll learn about YAML descriptions and trigger phrases"
  - Time: 20 seconds

- [ ] **Task 6.3**: Practice close-session again
  - I say: "Ready to close this session? Say 'done' when ready"
  - I wait for you to say "done"
  - I execute: close-session
  - I say: "Great! You're building the habit. See you next session! 👋"
  - Time: 1 minute

**Section Time**: 1-2 minutes

---

## Completion Checklist

- [ ] I loaded goals.md + roadmap.md successfully
- [ ] I created 04-workspace/ with 3-7 folders
- [ ] Folders match your goals/domain
- [ ] I designed workspace BEFORE explaining framework
- [ ] You understand Projects vs Skills framework (grounded in your workspace)
- [ ] You understand just-in-time organization
- [ ] I created first project via create-project skill
- [ ] Project relates to your goals
- [ ] I executed close-session successfully
- [ ] I marked Project 01 COMPLETE in project-map.md
- [ ] I introduced ≤5 new terms (Skills, Workspace, just-in-time, create-project)

---

## Time Breakdown

| Section | Time | Tasks |
|---------|------|-------|
| 1. Welcome Back | 1-2 min | 1.1-1.4 |
| 2. Workspace Design | 3-4 min | 2.1-2.4 |
| 3. Framework Explanation | 2 min | 3.1-3.4 |
| 4. Just-in-Time Org | 1 min | 4.1 |
| 5. First Project | 5-7 min | 5.1-5.6 |
| 6. Wrap-Up | 1-2 min | 6.1-6.3 |
| **TOTAL** | **10-14 min** | **15 tasks** |

---

## Vocabulary Budget

**New Terms I Introduce This Session**:
1. **Skills** (Section 3) - Repeatable workflows
2. **Workspace** (Section 3) - Work organization structure
3. **just-in-time** (Section 4) - Organization principle
4. **create-project** (Section 5) - System skill name

**Total New Terms**: 4
**Target**: ≤5 terms ✅

**Terms Deferred to Project 02**:
- YAML descriptions
- Trigger phrases
- Checkboxes
- nexus-loader mechanics

---

## CAVE Framework Compliance

| Phase | Target % | Actual | Status |
|-------|----------|--------|--------|
| **CONCRETE** | 30-40% | 20% | ⚠️ Could expand Section 1 |
| **ACTION** | 15-25% | 50% | ⚠️ High but value-rich |
| **VALUE** | 15-20% | 15% | ✅ Implicit in workspace |
| **EXPLANATION** | 20-30% | 15% | ✅ Grounded |

**Key Design**: I explain framework (Section 3) AFTER you create workspace (Section 2)
**Result**: Grounded learning (4x better retention)

---

## Philosophy Checklist

**Core Principles I Follow**:
- ✅ **Concrete Before Abstract**: I create workspace before teaching framework
- ✅ **Experience Before Explanation**: I explain framework AFTER you experience workspace
- ✅ **Problem Before Solution**: I show anti-pattern first
- ✅ **Value First**: I deliver workspace in first 5 minutes
- ✅ **Minimal Vocabulary**: I introduce 4 terms only
- ✅ **Momentum Sacred**: I minimize stops, maintain good flow
- ✅ **Practice Beats Explanation**: You practice close-session again
- ✅ **Psychological Anchoring**: I use "YOUR workspace", "YOUR goal" throughout

**CAVE Framework**:
- ✅ **Proper Flow**: Concrete → ACTION → EXPLANATION (grounded) → More ACTION

**Cognitive Load Management**:
- ✅ **Vocabulary**: 4 terms (target ≤5)
- ✅ **Tasks**: 15 tasks (target <20)
- ✅ **Sections**: 6 sections (target ≤7)
- ✅ **Time**: 10-14 min (target <15)

**Anti-Patterns I Avoid**:
- ✅ **Architecture-First**: I teach framework AFTER workspace experience
- ✅ **Vocabulary Firehose**: I use 4 terms, not more
- ✅ **Explanation Without Experience**: I ground all explanations
- ✅ **Tutorial Never Ends**: I keep it to 10-14 min

---

## Expected Outcomes

**What You'll Remember**:
- Vocabulary: 4 terms with ~60% retention after 24 hours
- Experience: Creating YOUR workspace first, then understanding why
- Framework: Projects vs Skills grounded in YOUR actual workspace

**Session Quality**:
- Time: 10-14 minutes (efficient)
- Flow: Smooth CAVE progression (Action → Explanation)
- Value: Working workspace + first project aligned to YOUR goals

---

**Status**: Ready for Execution
**Philosophy Compliance**: 85%+
**Date**: 2025-11-05

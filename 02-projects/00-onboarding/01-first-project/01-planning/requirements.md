# Requirements: First Project (Project 01)

**Project ID**: 01-first-project
**Onboarding Step**: 2 of 4
**Created**: 2025-11-03

---

## Overview

Second onboarding project that creates workspace and first real project while teaching Projects vs Skills decision framework, just-in-time organization, and YAML/checkbox mechanics. Uses create-project skill for guided project creation.

**Critical**: Load goals.md + roadmap.md and use USER's actual goals to personalize everything!

---

## Functional Requirements

### FR-2.1: Projects vs Skills Decision Framework (CRITICAL)

**Priority**: CRITICAL
**Time**: 2 minutes
**When**: After loading goals, before workspace design

**Must Teach**:
- Clear 2-step decision tree: (1) DIRECTION or WORK? (2) REPEAT or NOT?
- Present framework with visual decision tree
- Give 2-3 examples FROM THEIR DOMAIN (one goal, one project, one skill)
- Confirm understanding with simple yes/no
- Apply immediately to workspace and first project

**Example Flow**:
```
[Load goals.md to see USER_DOMAIN]
[Load design.md for complete framework reference]

"Let me explain the Universal Decision Framework:

Step 1: Is this DIRECTION or WORK?
  - DIRECTION → Goal (where you want to be)
  - WORK → Go to Step 2

Step 2: Does this work REPEAT?
  - NO → Project (one-time, has endpoint)
  - YES → Skill (repeatable workflow)

Here are examples from YOUR [domain]:
1. [Example GOAL from their domain]
2. [Example PROJECT from their domain]
3. [Example SKILL from their domain]

Does this framework make sense?"

[Wait for confirmation]
"Great! We'll apply this as we design your workspace and first project."
```

**Scenario Templates by Domain**:

**Consulting**:
1. "Create proposal template for clients" → Skill (repeatable)
2. "Onboard Acme Corp as new client" → Project (one-time for this client)
3. "Weekly status update to clients" → Skill (repeats weekly)
4. "Launch your consulting business website" → Project (one-time launch)
5. "Generate monthly invoices" → Skill (repeats monthly)

**Research**:
1. "Create paper annotation process" → Skill (use for each paper)
2. "Complete literature review for Chapter 2" → Project (specific deliverable)
3. "Weekly progress report to advisor" → Skill (repeats)
4. "Design and run Experiment A" → Project (specific experiment)
5. "Data analysis workflow" → Skill (same steps each dataset)

**Product**:
1. "Create feature spec template" → Skill (use for each feature)
2. "Ship v2.0 authentication system" → Project (specific feature)
3. "Weekly sprint planning" → Skill (repeats)
4. "Conduct Q2 user research study" → Project (specific study)
5. "Stakeholder update generation" → Skill (repeats)

**Success Metric**: User correctly classifies 4/5 or 5/5 scenarios

---

### FR-2.2: Just-in-Time Organization Philosophy

**Priority**: HIGH
**Time**: 2 minutes
**When**: Before workspace design

**Must Teach with Examples**:

**Anti-Pattern** (what NOT to do):
```
Creating structure before content:
- Clients/
  - Acme/
  - Beta/
  - Gamma/
  - Delta/
  (all empty!)

Problem: Premature organization, maintenance burden, no actual work yet
```

**Good Pattern** (what TO do):
```
Start simple, grow as needed:
Session 1: Create Clients/ (just one folder)
Session 5: Add Clients/Acme/ (when you GET Acme)
Session 10: Add Clients/Beta/ (when you GET Beta)

Structure emerges from real work!
```

**Key Principle**: "If you don't have content for a folder, don't create it yet"

**Success Metric**: User creates ≤3 workspace folders initially

---

### FR-2.3: Workspace Design (DYNAMIC - uses goals.md)

**Priority**: HIGH
**Time**: 3 minutes
**When**: After just-in-time teaching

**Must Load**: goals.md + roadmap.md via `nexus-loader.py --project 01`

**Must Analyze**: USER's role, goals, work pattern → Suggest appropriate folders

**Folder Suggestions by Domain**:
- Consulting: "Clients/", "Templates/", "Proposals/"
- Research: "Studies/", "Data/", "Papers/"
- Product: "Features/", "Research/", "Roadmaps/"
- Content: "Scripts/", "Assets/", "Published/"
- Startup: "Experiments/", "User-Research/", "Pitch-Decks/"

**Must Explain**: "These folders support YOUR goal: [USER'S GOAL]"

**Must Create**: 04-workspace/ with 3-7 folders matching their work

**Success Metric**: Workspace folders directly relate to user's goals

---

### FR-2.4: First Real Project Creation (CRITICAL - use create-project skill)

**Priority**: CRITICAL
**Time**: 8-10 minutes
**When**: After workspace created

**Must Load**: goals.md + roadmap.md to see USER's goals

**Must Extract**: Project idea from THEIR stated goals

**Examples**:
- Goal: "Launch consulting business" → Suggest: "client-proposal-system" or "service-offering-design"
- Goal: "Complete PhD" → Suggest: "dissertation-chapter-1" or "experiment-design"
- Goal: "Ship v2.0" → Suggest: "v2-authentication" or "user-research-synthesis"

**CRITICAL**: Must use create-project skill!
1. Explain: "I'm using the create-project skill to guide us through proper setup"
2. Load create-project skill
3. Follow skill's workflow (overview, requirements, design, tasks)
4. Teach skill mechanics during execution
5. User sees collaborative design process

**User Choice**: They pick from suggestions OR propose their own (must align with goals)

**NEVER**: Generic project names like "my-first-project" or "test-project"

**Success Metric**: Project directly relates to user's goals from Project 00

---

### FR-2.5: YAML Description Teaching (CRITICAL)

**Priority**: CRITICAL
**Time**: 2 minutes (embedded in project creation)
**When**: While creating project overview.md via create-project skill

**Must Explain**:
- "AI generates YAML description based on our conversation"
- "Description does TWO things: trigger phrases + documentation"
- "You review and approve—can request changes"

**Show Contrasting Examples**:

**Bad YAML** (vague):
```yaml
description: Website project
```
Problem: Too vague, no triggers, not helpful

**Good YAML** (specific):
```yaml
description: Load when user mentions "website redesign", "new site", "homepage update", "relaunch site". Redesigning company website with modern stack (Next.js, Tailwind). Target launch Q2 2025.
```
Why good: 4 trigger phrases + tech context + timeline

**Process**:
1. AI generates description based on conversation
2. User reviews: "Does this capture your project?"
3. User can request: "Add more trigger phrases" or "Make it more specific"
4. Check: 3+ trigger phrases? Meaningful context? Makes sense in 6 months?

**Success Metric**: Generated YAML includes 3+ trigger phrases + context

---

### FR-2.6: Checkbox-Driven State Teaching

**Priority**: MEDIUM
**Time**: 1 minute (embedded in project creation)
**When**: While creating tasks.md via create-project skill

**Must Explain**:
- Checkboxes = single source of truth for progress
- nexus-loader.py counts `[ ]` and `[x]` automatically
- `- [ ]` becomes `- [x]` when completed
- Progress % updates automatically

**Show Example**:
```
tasks.md has:
- [x] Task 1 (done!)
- [x] Task 2 (done!)
- [ ] Task 3 (working on this)
- [ ] Task 4 (not started)

System calculates: 2/4 = 50% progress
```

**Success Metric**: User understands checkboxes drive project status

---

### FR-2.7: Close-Session Reinforcement

**Priority**: HIGH
**Time**: 30 seconds
**When**: End of session

**Must Do**:
- Remind: "Ready to close this session? Just say 'done'"
- Wait for user to say "done"
- Execute close-session
- Reinforce: "Great habit! You're building the pattern."

**Success Metric**: User closes session properly again

---

## Non-Functional Requirements

### NFR-1: Personalization
- ALL scenarios from user's domain
- ALL folder suggestions match user's goals
- First project relates to user's actual goal
- Zero generic content

### NFR-2: Cognitive Load
- One concept at a time
- Embed teaching in doing (not lectures)
- Examples before theory

### NFR-3: Skill Integration
- create-project skill MUST be used (not optional)
- Explain skill as it runs
- User sees collaborative design process

---

## Success Criteria

- [ ] User confirmed understanding of Projects vs Skills decision framework
- [ ] User understands just-in-time organization
- [ ] 04-workspace/ created with 3-7 folders matching user's work
- [ ] First project created via create-project skill
- [ ] Project name/content relates to user's goals
- [ ] YAML description has 3+ trigger phrases
- [ ] User understands checkbox-driven state
- [ ] close-session executed successfully

---

**Requirements Version**: 1.0
**Last Updated**: 2025-11-03
**Status**: Ready for Implementation

# nexus-product-intro-presentation - Execution Steps

**Last Updated**: 2025-11-24

**IMPORTANT**: This file tracks project progress. Mark tasks complete with [x] as you finish them.

---

## Phase 1: Planning & Setup ✅

- [x] Complete overview.md
- [x] Complete plan.md (with JTBD 7-phase lifecycle integration)
- [x] Complete steps.md
- [x] Review plan with stakeholders

**Status**: COMPLETE - Ready for execution session

---

## Phase 2: Create Workshop Facilitator Guide (PRIORITY #1)

**Why first?**: Workshop guide is 50% of workshop success. Create before slides to ensure delivery quality.

**Location**: `02-resources/workshop-guide.md`

### Tasks:
- [x] **Section 1: Workshop Overview**
  - [x] Write workshop objectives (dual-audience value prop)
  - [x] Define facilitator role and responsibilities
  - [x] List required materials and pre-work

- [x] **Section 2: Phase-by-Phase Timing Breakdown**
  - [x] Phase 1 - Foundation (30 min): Slides + Guide walkthrough
  - [x] Phase 2 - Live Onboarding (55 min): Project 00 guided session
  - [x] Phase 3 - Wrap-Up (5 min): Recap + next steps

- [x] **Section 3: Facilitator Talking Points**
  - [x] Slide 1-2: Problem framing (both audiences)
  - [x] Slide 3-5: Solution architecture (memory + structure)
  - [x] Slide 6: Skills with 7-phase lifecycle (Solutions team focus)
  - [x] Slide 7-9: How it works + examples
  - [x] Slide 10-11: Transition to hands-on

- [x] **Section 4: Troubleshooting Scenarios**
  - [x] Claude Code setup issues (pre-workshop checklist)
  - [x] Network/firewall problems during hands-on
  - [x] Sales team confusion on technical concepts
  - [x] Solutions team dismisses as "too basic"
  - [x] Workshop running behind schedule (skip strategies)

- [x] **Section 5: FAQ Handling Strategies**
  - [x] "How is this different from X?" (X = Cursor, GitHub Copilot, etc.)
  - [x] "What if I already have my own system?"
  - [x] "How long does onboarding really take?"
  - [x] "Can I use this for [non-AI-Agent-Company use case]?"

- [x] **Section 6: Audience Engagement Techniques**
  - [x] Check-ins for Sales team (ensure not lost)
  - [x] Depth questions for Solutions team (maintain engagement)
  - [x] Celebration moments ("Great! Your memory is working!")
  - [x] Pause points for questions

- [x] **Section 7: Real-Time Pacing Tips**
  - [x] 30-min mark checkpoint (should be starting Project 00)
  - [x] 60-min mark checkpoint (should be in Section 2 of Project 00)
  - [x] 80-min mark checkpoint (wrapping up Project 00)
  - [x] "Running behind" contingency strategies

**Estimated Time**: 3-4 hours

---

## Phase 3: Create JTBD Skills Mapping Document (PRIORITY #2)

**Why second?**: This is the PRIMARY DELIVERABLE for Solutions team value prop. Needed before creating Slide 6.

**Location**: `02-resources/jtbd-skills-mapping.md`

### Tasks:
- [x] **Section 1: Executive Summary**
  - [x] Total ROI calculation (12-21 weeks → 6-10 weeks)
  - [x] Team capacity increase (1x → 2x clients)
  - [x] Key pain points solved

- [x] **Section 2: 7-Phase Lifecycle Breakdown**
  - [x] Phase 1: Pre-Contract Assessment (with skill details)
  - [x] Phase 2: Project Setup (with skill details)
  - [x] Phase 3: Discovery and Scoping (with 2 skills)
  - [x] Phase 4: Build & Implement (with skill details)
  - [x] Phase 5: Testing and Optimization (with skill details)
  - [x] Phase 6: Go Live (with skill details)
  - [x] Phase 7: Maintenance (with 2 skills)

- [x] **Section 3: Skill Implementation Details**
  - [x] For each of 10 skills: SKILL.md structure, inputs, outputs, MCP integrations
  - [x] Reusability examples (Client A → Client B → Client C)
  - [x] Team collaboration patterns (Consultant 1 builds, entire team uses)

- [x] **Section 4: MCP Integration Hub**
  - [x] Airtable integration points (Phases 1, 3)
  - [x] HubSpot integration points (Phase 1)
  - [x] Notion integration points (Phases 2, 3, 7)
  - [x] Linear integration points (Phases 2, 6, 7)
  - [x] Gmail integration points (Phase 7)

- [x] **Section 5: Real JTBD Quotes**
  - [x] "Include solutions team early in discovery" → Skill solution
  - [x] "Share timeline with action points" → Skill solution
  - [x] "Gather detailed process information" → Skill solution
  - [x] "Monitor task executions" → Skill solution
  - [x] "Create automation that generates Mermaid charts" → Skill solution

- [x] **Section 6: Before/After Comparison**
  - [x] Time investment per phase (before vs after)
  - [x] Manual effort breakdown (before vs after)
  - [x] Rework rate reduction (30-40% → <10%)

**Estimated Time**: 3-4 hours

---

## Phase 4: Create Example Scenarios Document

**Location**: `02-resources/example-scenarios.md`

### Tasks:
- [x] **Sales Team Example: Client Proposal Workflow**
  - [x] Scenario: Sales rep creating proposal for new prospect
  - [x] Before Nexus: Manual template hunting, copy-paste chaos
  - [x] With Nexus: Load proposal-builder skill, reuse structure
  - [x] Key benefits: Consistency, speed, team sharing

- [x] **Solutions Team Example: Client Implementation Tracking**
  - [x] Scenario: Consultant managing 3 concurrent client projects
  - [x] Before Nexus: Scattered docs, manual status updates, lost work
  - [x] With Nexus: 7-phase Skills library, automated dashboards, project templates
  - [x] Key benefits: Reusability, institutional knowledge, 2x capacity

- [x] **Universal Example: Projects as Templates**
  - [x] Visual showing: Create once → Clone for Client B → Clone for Client C
  - [x] Sandbox pattern explanation (same structure, different experiments)
  - [x] Team collaboration flow (Skills shared across team)

**Estimated Time**: 2 hours

---

## Phase 5: Create Presentation Slides (11 Slides)

**Location**: `03-working/slides.md`

### Tasks:
- [x] **Slide 1: The 3 Universal Problems**
  - [x] Problem #1: Lost Work (both audiences' pain)
  - [x] Problem #2: No Reuse (both audiences' pain)
  - [x] Problem #3: Can't Share Knowledge (both audiences' pain)
  - [x] Visual: Split-screen showing Sales vs Solutions examples

- [x] **Slide 2: Why These Problems Exist**
  - [x] Web AI = stateless (no memory)
  - [x] Claude Code alone = no structure (files everywhere)
  - [x] Diagram: Current state visualization

- [x] **Slide 3: The Nexus Solution - Architecture**
  - [x] 5-folder system diagram (00-system, 01-memory, 02-projects, 03-skills, 04-workspace)
  - [x] Clear boundaries (what AI manages vs what you control)
  - [x] Visual: System map with folder icons

- [x] **Slide 4: Solution #1 - Memory System**
  - [x] goals.md example (code snippet)
  - [x] Persistence across sessions
  - [x] Visual: Session 1 → close-session → Session 2 (AI remembers)

- [x] **Slide 5: Solution #2 - Project Structure**
  - [x] 4-folder pattern (01-planning, 02-resources, 03-working, 04-outputs)
  - [x] Visual: Folder tree showing project organization

- [x] **Slide 6: Solution #3 - Skills (7-Phase Lifecycle)**
  - [x] **PRIMARY SLIDE**: Solutions team 7-phase lifecycle → Nexus Skills
  - [x] Before: 12-21 weeks per client (manual)
  - [x] After: 6-10 weeks per client (Skills library)
  - [x] Visual: 7 phases with skill icons + ROI numbers
  - [x] Use content from `jtbd-skills-mapping.md`

- [x] **Slide 7: How It Works - 3-Step Process**
  - [x] Step 1: Load context (skills, memory, projects)
  - [x] Step 2: Work together (AI + human collaboration)
  - [x] Step 3: Save everything (close-session)
  - [x] Visual: Workflow diagram

- [x] **Slide 8: Real Example - Projects as Templates**
  - [x] Sales: Proposal template → Reuse for every prospect
  - [x] Solutions: Client A implementation → Clone for Client B
  - [x] Visual: Template reuse pattern (create once → use many times)

- [x] **Slide 9: Before vs After**
  - [x] Table format:
    - Before: Lost work, no reuse, siloed knowledge
    - After: Everything saved, template reuse, team sharing
  - [x] Visual: Side-by-side comparison

- [x] **Slide 10: Workshop Preview - What We'll Build Together**
  - [x] Next 60 min: Project 00 onboarding (guided)
  - [x] You'll build: Workspace, memory system, first project
  - [x] Sales example: "Client proposal workflow"
  - [x] Solutions example: "Client implementation tracking"
  - [x] Visual: Workshop roadmap with timing

- [x] **Slide 11: Ready to Start?**
  - [x] Call-to-action: "Let's build your Nexus workspace together"
  - [x] Transition statement: "Any questions before we dive in?"

**Estimated Time**: 4-5 hours

**Dependencies**:
- Must complete `workshop-guide.md` first (for talking points)
- Must complete `jtbd-skills-mapping.md` first (for Slide 6 content)

---

## Phase 6: Review & Refinement

### Tasks:
- [ ] **Internal Review**
  - [ ] Read all slides aloud (check flow and timing)
  - [ ] Test transitions between slides
  - [ ] Verify all examples work for both audiences

- [ ] **Workshop Guide Validation**
  - [ ] Walk through guide as if facilitating
  - [ ] Ensure troubleshooting covers common scenarios
  - [ ] Verify timing estimates realistic

- [ ] **Dual-Audience Check**
  - [ ] Every slide addresses both Sales + Solutions
  - [ ] No jargon without explanation
  - [ ] Visual/no-code friendly (no raw code unless necessary)

- [ ] **JTBD Integration Check**
  - [ ] Slide 6 accurately represents 7-phase lifecycle
  - [ ] Real JTBD quotes included ("mentioned by all team members")
  - [ ] ROI numbers match (12-21 weeks → 6-10 weeks)

**Estimated Time**: 2 hours

---

## Phase 7: Export & Finalize

### Tasks:
- [ ] **Export Production Slides**
  - [ ] Create `04-outputs/final-presentation.md` (clean version)
  - [ ] Choose presentation format (Markdown, Google Slides, or Keynote)
  - [ ] Format for screen presentation (font sizes, colors)

- [ ] **Package Deliverables**
  - [ ] `02-resources/workshop-guide.md` (facilitator reference)
  - [ ] `02-resources/jtbd-skills-mapping.md` (Solutions team deep dive)
  - [ ] `02-resources/example-scenarios.md` (real use cases)
  - [ ] `04-outputs/final-presentation.md` (slides)

- [ ] **Pre-Workshop Checklist**
  - [ ] Test Claude Code + Nexus on facilitator machine
  - [ ] Prepare troubleshooting backup plans
  - [ ] Send pre-work to participants (Claude Code setup)
  - [ ] Book backup facilitator for technical support

**Estimated Time**: 1-2 hours

---

## Quality Gates (Must Pass Before Completion)

### Gate 1: Dual-Audience Test
- [ ] Sales team member reviews: "Do I see myself in these examples?"
- [ ] Solutions team member reviews: "Does Slide 6 solve my real problems?"

### Gate 2: Timing Validation
- [ ] Dry run: Can you deliver 11 slides in 20 minutes?
- [ ] Workshop guide: Can facilitator follow it without confusion?

### Gate 3: JTBD Accuracy
- [ ] 7-phase lifecycle matches `jobs-to-be-done.md`
- [ ] Real quotes included with attribution
- [ ] ROI calculations verified

### Gate 4: Pareto Check
- [ ] Content extracted: 20% of Beam presentation → 80% of value
- [ ] Slides focused: No feature overload, clear message

---

## Total Estimated Time

**Planning**: 1-2 hours (COMPLETE)
**Execution**: 15-20 hours total
- Workshop Guide: 3-4 hours
- JTBD Mapping: 3-4 hours
- Example Scenarios: 2 hours
- Slides: 4-5 hours
- Review: 2 hours
- Export: 1-2 hours

**Total Project**: ~17-22 hours from start to delivery-ready

---

## Notes

**Current Status**: Planning complete. Ready for execution session.

**Next Session Actions**:
1. Start with `workshop-guide.md` (PRIORITY #1)
2. Then `jtbd-skills-mapping.md` (PRIORITY #2)
3. Then slides (depends on first two)

**Critical Success Factors**:
- Workshop guide must be created BEFORE slides (not after)
- Slide 6 (7-phase lifecycle) is the Solutions team's "aha moment"
- Every slide must work for BOTH audiences simultaneously
- Real JTBD quotes build credibility ("mentioned by all team members")

**Key Files Reference**:
- Source material: `00-system/documentation/presentation-materials/beam-presentation-10-slides-v2.md`
- JTBD source: `04-workspace/input/jobs-to-be-done.md`
- Project 00 reference: `02-projects/00-onboarding/00-define-goals/`

---

*Mark tasks complete with [x] as you finish them during execution session*

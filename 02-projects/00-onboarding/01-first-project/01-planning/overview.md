---
id: 01-first-project
created: 2025-11-03
name: First Project
onboarding: true
status: PLANNING
description: Load when user mentions "first project", "workspace", "project 01", "continue onboarding". Second onboarding project that creates workspace structure using just-in-time organization, teaches Projects vs Skills decision framework with user's scenarios, and guides creation of first real project using create-project skill and user's actual goals.
tasks_total: 0
tasks_completed: 0
progress: 0.0
---

# Project Overview: First Project

**Project ID**: 01
**Created**: 2025-11-03
**Type**: Onboarding Project (Step 2 of 4)
**Duration**: 12-17 minutes

---

## Purpose

Create your workspace structure and first real project while learning:
- Projects vs Skills decision framework (with YOUR scenarios)
- Just-in-time organization philosophy
- YAML descriptions and auto-loading
- Checkbox-driven progress tracking
- How to use create-project skill

**Critical**: This project uses YOUR goals (from Project 00) to personalize everything!

---

## What You'll Learn

### 1. Projects vs Skills Decision Framework
- Clear 2-step decision tree (Direction vs Work, One-time vs Repeating)
- Examples from YOUR domain to illustrate the concepts
- Learn by application rather than testing

### 2. Just-in-Time Organization
- Start simple (3-7 folders), grow as needed
- Avoid premature over-organization
- Structure emerges from real work

### 3. Workspace Design
- Create 04-workspace/ with folders that match YOUR goals
- Based on YOUR role and work pattern

### 4. First Real Project Creation
- Use create-project skill (guided workflow)
- Project directly relates to YOUR goals from Project 00
- Learn collaborative design process

### 5. YAML Description Writing
- AI generates description with trigger phrases
- You review and approve
- Learn what makes good YAML

### 6. Checkbox-Driven State
- tasks.md checkboxes = single source of truth
- nexus-loader.py counts automatically
- Progress tracking happens automatically

---

## What You'll Create

By the end of this project, you'll have:

1. **04-workspace/** - 3-7 folders matching YOUR work (e.g., Clients/, Templates/, Research/, Projects/, Documentation/, Assets/, Archive/)
2. **02-projects/XX-[your-project]/** - First real project via create-project skill
   - 01-planning/ with overview.md, requirements.md, design.md, tasks.md
   - YAML with 3+ trigger phrases
   - Tasks aligned with YOUR goal
3. **Updated project-map.md** - Now tracks your first project

**All personalized to YOUR goals!**

---

## Context Flow

**Input**:
- goals.md (YOUR role, goals, motivation)
- roadmap.md (YOUR milestones, priorities)

**Loaded via**: `python nexus-loader.py --project 01` (automatic)

**Output**:
- 04-workspace/ structure
- First project in 02-projects/
- Updated project-map.md

**Next Project Will Use**: Your first project to extract workflows (Project 02)

---

## Success Criteria

You've successfully completed this project when:

- [ ] You understand the Projects vs Skills decision framework
- [ ] You understand just-in-time organization (don't over-organize upfront)
- [ ] You've created 04-workspace/ with 3-7 initial folders
- [ ] You've used create-project skill to create first real project
- [ ] Project relates directly to YOUR goals from Project 00
- [ ] Project YAML has 3+ trigger phrases
- [ ] You understand checkbox-driven progress tracking
- [ ] close-session practiced again (building habit!)

---

## Time Estimate

**12-17 minutes**
- Projects vs Skills framework: 2 min
- Workspace design: 3 min
- Create first project (via skill): 8-10 min
- Wrap-up: 2 min

---

## Current Status

**Status**: PLANNING
**Progress**: 0/TBD tasks complete
**Next Step**: Execute tasks.md in sequence

---

**Onboarding Step**: 2 of 4
**Focus**: Workspace + First Project + Decision Framework

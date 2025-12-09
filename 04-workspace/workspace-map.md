# Workspace Map

<!-- AI CONTEXT FILE -->
<!-- Purpose: Help AI understand user's custom folder structure -->
<!-- Updated by: User (when reorganizing workspace) -->

**Last Updated**: [TODO: Update when workspace changes]

> **Purpose**: Help AI agent understand your custom folder structure in `04-workspace/`
>
> **Audience**: AI (loaded every session via --startup)
>
> **Your role**: Update this when you reorganize folders so AI knows what each folder contains

---

## How This Works

**You organize `04-workspace/` however you want** (clients, departments, topics, etc.)
- Create folders that match YOUR work
- No predefined structure - organize naturally

**This file helps AI understand your structure:**
- AI reads this file every session
- Brief descriptions help AI route to right folders
- Update this when you reorganize or add folders

---

## Your Workspace Structure

```
04-workspace/
├── input/                                   # IMPORT YOUR EXISTING WORK HERE
│   ├── WORKSHOP-CONTEXT.md                  # Workshop guidance (MANDATORY for AI)
│   ├── IMPORT-INSTRUCTIONS.md               # Import guide (read BEFORE onboarding)
│   ├── skills-ideas-catalog.md              # 20+ Skill ideas with templates
│   ├── workshop-quick-start-guide.md        # 30-day transformation roadmap
│   └── [Your imported files/folders]
│
└── [Your custom folders will be created during onboarding or as needed]
```

---

## Folder Descriptions

### **input/**
**Purpose**: Import existing work BEFORE starting onboarding

**Contains**:
- **WORKSHOP-CONTEXT.md**: MANDATORY AI instructions for workshop participants
  - Guides goal/roadmap creation toward Skills focus
  - Provides Solutions Engineer context (7-phase lifecycle)
  - Templates for workshop-specific onboarding
  - Auto-loaded during Project 00 if present

- **IMPORT-INSTRUCTIONS.md**: User guide for importing existing work
  - Read BEFORE starting Project 00 onboarding
  - Examples of what to import (old Nexus v2, scattered client files, templates)
  - What AI will do with imported files
  - Real workshop examples (Hassan's import)

- **skills-ideas-catalog.md**: 20+ Skill ideas with implementation templates
  - Quick Wins section (Weekly Update, Test Reports, Prompt Templates)
  - Phase-by-phase Skills (all 7 lifecycle phases covered)
  - Real pain points from workshop (Hassan, Jack, Fahad)
  - Time savings calculations (4 hrs → 30 min, etc.)
  - AI uses this to suggest specific Skills during onboarding

- **workshop-quick-start-guide.md**: 30-day transformation roadmap
  - Week 1: Organize client lifecycle (7 phase projects)
  - Week 2-3: Build first Skills (Quick Wins)
  - Week 4: Team multiplier + continuous aggregation
  - AI uses this to structure roadmap milestones

- **[Your imported folders/files]**: Your existing work to analyze
  - Old Nexus v2 workspaces → upgrade to v3
  - Scattered client project files → organize into Nexus structure
  - Email/report templates → convert to Skills
  - Process docs → extract as reusable workflows

**When AI loads workspace**:
1. Check for WORKSHOP-CONTEXT.md → workshop participant mode
2. Analyze imported files/folders → extract Skills opportunities
3. Use during Project 00 → guide goals toward Skills creation
4. Reference real examples → grounded in participant's actual work

**Workshop participants**: Import ALL existing work here first!
**Regular users**: Use as "inbox" for files to organize later

---

## Tips

- **Keep it simple**: Don't over-organize - only create folders you actually use
- **Use consistent naming**: Lowercase-with-hyphens recommended
- **Add context**: Brief descriptions help AI understand what each folder contains
- **Update regularly**: Keep this map current when you reorganize

---

**Remember**: The workspace is YOURS - organize it however makes sense for your work!

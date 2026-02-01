---
name: list-skills
description: "list skills, show skills, what skills, available skills."
---

# List Skills

Display all available skills organized by category with descriptions.

## Purpose

Help users discover available skills in Nexus. Shows both system skills (built-in) and user skills (custom) organized by category.

**Time Estimate**: Instant

---

## Workflow

### Step 1: Run Skill Scanner

```bash
nexus-load --list-skills
```

Parse the JSON output to get all skills with their names and descriptions.

---

### Step 2: Organize by Category

Group skills by their folder location:

| Category | Location | Description |
|----------|----------|-------------|
| **Learning** | `00-system/skills/learning/` | Onboarding and tutorials |
| **Builds** | `00-system/skills/builds/` | Build management |
| **Skill Dev** | `00-system/skills/skill-dev/` | Skill creation and sharing |
| **System** | `00-system/skills/system/` | System utilities |
| **Tools** | `00-system/skills/tools/` | Productivity tools |
| **Integrations** | `00-system/skills/notion/`, `airtable/`, `beam/` | External tool connections |
| **User Skills** | `03-skills/` | Your custom skills |

---

### Step 3: Display Skills

Output format:

```
# Available Skills

## Learning (onboarding)
- setup-goals: Personalize Nexus with your goals and role
- create-folders: Configure your workspace folder structure
- learn-builds: Tutorial on build system
- learn-skills: Tutorial on skill system
- learn-nexus: Advanced system mastery

## Builds
- plan-build: Create a new build with guided planning
- execute-build: Work on a build systematically
- archive-build: Archive completed builds
- bulk-complete: Mark multiple tasks complete

## System
- close-session: Save progress and end session
- list-skills: This skill - show all available skills
- validate-system: Check system health
- validate-workspace-map: Sync workspace documentation

## Tools
- mental-models: 30+ thinking frameworks for decisions
- generate-philosophy-doc: Create best practices documents

## Integrations
- notion-connect: Connect to Notion databases
- airtable-connect: Connect to Airtable bases
- beam-*: Beam.ai agent management (10 skills)

## User Skills
[List any skills in 03-skills/ or "None yet - say 'create skill' to add one!"]

---
Tip: Say the skill name or trigger phrase to use it.
```

---

## Notes

- User skills in `03-skills/` take priority over system skills
- Skill triggers are in the description (e.g., "say 'create build'")
- Some skills are internal (e.g., master skills) and not directly triggered

---

## Success Criteria

- [ ] All system skills listed by category
- [ ] All user skills listed (or "none yet" message)
- [ ] Each skill shows name and brief description
- [ ] Tip provided on how to use skills

# Your Skills

This folder contains **your custom skills** — reusable workflows you create.

## How Skills Work

Say a trigger phrase → AI loads the skill → Executes the workflow → Consistent result every time.

## Creating a Skill

1. Do something useful in a session
2. Say `"create skill"`
3. AI captures the workflow as a reusable skill

## Skill Structure

```
03-skills/
└── weekly-status-report/
    ├── SKILL.md          # Required: trigger + workflow
    ├── references/       # Optional: supporting docs
    ├── scripts/          # Optional: automation
    └── assets/           # Optional: templates, images
```

## Example SKILL.md

```yaml
---
name: weekly-status-report
description: Load when user says "status report", "weekly update".
---

## Workflow

1. Load goals.md for current objectives
2. Scan session-reports/ from last 7 days
3. Extract completed tasks from active projects
4. Generate summary with metrics
5. Save to workspace/reports/
```

---

**Note:** Your skills here take priority over system skills in `00-system/skills/`.

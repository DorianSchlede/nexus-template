---
name: learn-skills
description: "Learn how Nexus skills work - identifying workflows, skill-worthiness criteria, creating skills. Load when user says 'learn skills', 'skill tutorial', 'how do skills work', 'what is a skill', 'understand workflows', 'explain skills', 'teach me skills', 'skill basics', 'how skills work', 'skill guide', 'when to create skill', 'skill worthiness', 'reusable workflows', 'workflow automation', 'what makes a skill', 'skill structure', or asks about when/how to create reusable workflows. Teaches when and how to create reusable workflows. Takes 10-12 minutes."
---

# Learn Skills

Teach how to identify skill-worthy workflows and create effective skills.

## Purpose

Help user understand what makes something skill-worthy, how skills are structured, and how skill triggering works. Includes hands-on practice identifying their own workflows.

**Time Estimate**: 10-12 minutes

---

## Workflow

### Step 1: Concrete Examples

```
✅ SKILLS (repeating workflows):
- Weekly status report (same format weekly)
- Qualify sales lead (same questions each time)
- Process expense reports (same steps)

❌ NOT SKILLS (one-time):
- Research competitor Acme (one-time)
- Build Q1 marketing plan (one-time)

Key question: Will I do this AGAIN?
```

---

### Step 2: Skill-Worthiness Framework

```
Three questions:

1. FREQUENCY: 2+ times per month?
   YES → keep evaluating

2. REPEATABILITY: Steps mostly the same?
   YES → keep evaluating

3. VALUE: Saves >5 minutes per execution?
   YES → Create a skill!

ALL 3 YES = Skill-worthy
ANY NO = Just do it manually
```

---

### Step 3: Skill Structure

```
📁 weekly-status-report/
├── SKILL.md       # Instructions + triggers
├── references/    # Documentation (optional)
├── scripts/       # Automation (optional)
└── assets/        # Templates (optional)
```

---

### Step 4: How Triggering Works

```
AI checks your message against ALL skill descriptions.
Match found = skill loads.

Example description:
"Load when user says 'status report', 'weekly update',
 'progress summary'"

ANY of these triggers it:
• "Generate my status report"
• "Weekly update please"
• "Progress summary"
```

---

### Step 5: Practice

**Ask**: "What did you do last week that you'll probably do again?"

For each: apply 3-criteria framework, brainstorm trigger phrases.

---

### Step 6: How to Create

```
To create a skill, say:
• "create skill for [workflow]"
• "new skill: [name]"

YOUR skills go in 03-skills/ (prioritized!)
SYSTEM skills in 00-system/skills/
```

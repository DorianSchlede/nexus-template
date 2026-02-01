---
name: learn-skills
description: "Learn how Nexus skills work. Load when user mentions: learn skills, how do skills work, what is a skill, skill tutorial, skill structure, understand skills, explain skills, when to create skill, skill vs build. 10-12 min."
onboarding: true
priority: high
---

## 🎯 Build-First Onboarding (CONTEXTUAL SUGGESTION)

**This is a learning skill. With Build-First onboarding, suggest AFTER first task execution, not before.**

### Auto-Complete via Checkpoint

```yaml
# In user-config.yaml
build_first.checkpoints.first_task_executed: true  → learn_skills auto-completed!
```

When user completes their first section in execute-build, `learn_skills` is **automatically marked complete** via `auto_complete_map`. They learned by DOING.

### When to Proactively Suggest (Pattern Detection)

Check both:
- `learning_tracker.completed.learn_skills` - explicit completion
- `build_first.checkpoints.first_task_executed` - auto-completion

**PROACTIVELY SUGGEST when user:**
1. **Pattern detected** - does something similar to previous work ("I notice you've done this type of task before...")
2. Creates multiple similar builds (report-jan, report-feb anti-pattern)
3. Describes repeating work patterns ("every week I...", "I always have to...")
4. Explicitly asks to learn about skills/automation

**Suggestion Pattern (After Pattern Detection):**
```
💡 I notice you've done similar work before. Want to understand how to
turn repeating workflows into Skills?

'learn skills' covers:
- The 3-criteria skill-worthiness framework
- How skills are structured
- How AI triggers skills automatically

Say 'learn skills' for the deep-dive (10 min), or continue working.
```

**Anti-Pattern Detection:**
```
If user creates: report-jan, report-feb, report-mar...
→ "I notice you're creating similar items. This is a perfect use case for
   a SKILL instead of multiple builds. Want to 'learn skills' to understand
   how to capture this as a reusable workflow?"
```

**DO NOT suggest if:**
- User is working on their FIRST build/task (let them DO first)
- User explicitly says "skip" or dismisses
- User is mid-task and focused
- No repeating pattern detected

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

---

### Step 7: Finalize

**Actions** (MUST complete all):

1. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       learn_skills: true  # ADD THIS LINE
   ```

2. **Display completion**:
   ```
   ✅ Learn Skills Complete!

   You now understand:
   • Skills = reusable workflows (do AGAIN → skill)
   • 3-criteria framework (Frequency + Repeatability + Value)
   • Skill structure (SKILL.md + optional references/scripts)
   • Trigger mechanism (keywords in description)

   Next steps:
   • 'create skill' - Create your first skill
   • 'learn builds' - Learn about temporal work
   • 'learn nexus' - System mastery
   ```

3. **Session ending tip**:
   ```
   💡 When you're done, open a NEW chat for your next topic.
   ```

---

## Success Criteria

- [ ] User understands skill vs build distinction
- [ ] User can apply 3-criteria skill-worthiness framework
- [ ] User knows skill folder structure
- [ ] User understands trigger mechanism
- [ ] User identified at least one potential skill from their work
- [ ] `learning_tracker.completed.learn_skills: true` in user-config.yaml

---
name: learn-builds
description: "Learn how Nexus builds work. Load when user mentions: learn builds, how do builds work, builds vs skills, build tutorial, what is a build, build structure, build lifecycle, understand builds, explain builds. 8-10 min."
onboarding: true
priority: high
---

## 🎯 Build-First Onboarding (CONTEXTUAL SUGGESTION)

**This is a learning skill. With Build-First onboarding, suggest AFTER first build, not before.**

### Auto-Complete via Checkpoint

```yaml
# In user-config.yaml
build_first.checkpoints.first_build_created: true  → learn_builds auto-completed!
```

When user creates their first build, `learn_builds` is **automatically marked complete** via `auto_complete_map`. They learned by DOING.

### When to Proactively Suggest (Post-Experience)

Check both:
- `learning_tracker.completed.learn_builds` - explicit completion
- `build_first.checkpoints.first_build_created` - auto-completion

**PROACTIVELY SUGGEST when user:**
1. **AFTER first build** - asks "how does this build system work?" (wants deeper understanding)
2. Expresses confusion about builds vs skills (after having used builds)
3. Starts creating multiple similar "builds" (anti-pattern detection)
4. Explicitly asks to learn/understand builds

**Suggestion Pattern (Post-Experience):**
```
💡 You've already created a build! Want to understand the system more deeply?

'learn builds' covers:
- When to use builds vs skills (avoid anti-patterns)
- Build lifecycle and best practices
- How to track progress effectively

Say 'learn builds' for the deep-dive (8 min), or continue working.
```

**If user already created build, acknowledge it:**
```
You've got practical experience now! This tutorial will deepen your understanding
of WHY the system works this way.
```

**DO NOT suggest if:**
- User is creating their FIRST build (let them DO first)
- User explicitly says "skip" or dismisses
- User is mid-task and focused

---

# Learn Builds

Teach how Nexus builds work through examples and decision framework.

## Purpose

Help user understand when to create builds vs skills, how builds are structured, and the build lifecycle. Uses concrete examples before abstract concepts.

**Time Estimate**: 8-10 minutes

---

## Workflow

### Step 1: Concrete Examples

Show what IS and ISN'T a build:
```
✅ BUILDS:
- Build client proposal for Acme Corp
- Research competitors and write analysis
- Create onboarding docs for new hires

❌ NOT BUILDS (these are skills):
- Generate weekly status reports (repeating)
- Qualify incoming leads (repeating)
- Format documents (repeating)

Pattern: Builds END. Skills REPEAT.
```

**Ask**: "What work are YOU planning? Let's classify it."

---

### Step 2: Decision Framework

```
Question 1: Direction or Work?
  • Direction = Goal (goals.md)
  • Work = Build or Skill

Question 2: Does it repeat?
  • NO → BUILD (has endpoint)
  • YES → SKILL (reusable)

ANTI-PATTERN:
❌ "weekly-report-week-1", "weekly-report-week-2"...
✅ ONE "weekly-report" SKILL used every week
```

---

### Step 3: Build Structure

```
📁 02-builds/05-client-proposal/
├── 01-planning/
│   ├── overview.md    # What & why
│   ├── plan.md        # How
│   └── steps.md       # Tasks (checkboxes)
├── 02-resources/      # Reference materials
├── 03-working/        # Work in progress
└── 04-outputs/        # Final deliverables
```

---

### Step 4: Lifecycle

```
PLANNING → IN_PROGRESS → COMPLETE → ARCHIVED
```

Explain each state briefly.

---

### Step 5: Practice

**Ask**: "Tell me 3 things you're planning to work on."

For each: apply decision framework together, explain reasoning.

---

### Step 6: How to Create

```
To create a build, say:
• "create build for [description]"
• "new build: [name]"

Ready? Say "create build" to start one!
```

---

### Step 7: Finalize

**Actions** (MUST complete all):

1. **Mark skill complete** in user-config.yaml:
   ```yaml
   learning_tracker:
     completed:
       learn_builds: true  # ADD THIS LINE
   ```

2. **Display completion**:
   ```
   ✅ Learn Builds Complete!

   You now understand:
   • Builds vs Skills (builds END, skills REPEAT)
   • Decision framework (Direction → Work → Repeat?)
   • Build structure (planning → resources → working → outputs)
   • Lifecycle states (PLANNING → IN_PROGRESS → COMPLETE)

   Next steps:
   • 'create build' - Start your first build
   • 'learn skills' - Learn about reusable workflows
   • 'learn nexus' - System mastery
   ```

3. **Session ending tip**:
   ```
   💡 When you're done, open a NEW chat for your next topic.
   ```

---

## Success Criteria

- [ ] User understands build vs skill distinction
- [ ] User can apply decision framework
- [ ] User knows build folder structure
- [ ] User understands lifecycle states
- [ ] `learning_tracker.completed.learn_builds: true` in user-config.yaml
